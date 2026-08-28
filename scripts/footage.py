#!/usr/bin/env python3
"""Dikey video klip bulma, indirme ve önbellekleme (Pexels → Pixabay).

Kanalın en büyük kalite darboğazı konu başına tek durağan fotoğraftı. Bu
modül her çekim için gerçek video klip getiriyor.

İki eleme kuralı var, ikisi de "donuk kare" şikâyetine karşı:

* **Hareket eşiği.** Stok kütüphanelerinde tripod üzerinde çekilmiş,
  neredeyse hiç hareket etmeyen klipler çok yaygın. `motion_score()` ardışık
  karelerin ortalama farkını ölçüyor; eşiğin altında kalan aday atlanıp
  sıradaki deneniyor.
* **Süre eşiği.** Çekim süresinden kısa klipler döngüye alınınca görünür
  şekilde tekrar ediyor; mümkünse yeterince uzun olan seçiliyor.

Klipler `footage/` altında önbelleklenir — aynı terim ikinci kez indirilmez.

CLI:
    python scripts/footage.py "golden retriever wagging tail" --min-duration 6
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keys import get as key_get  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_ROOT / "footage"
INDEX_PATH = CACHE_DIR / "index.json"

PEXELS_URL = "https://api.pexels.com/videos/search"
PIXABAY_URL = "https://pixabay.com/api/videos/"

TARGET_H = 1920
MIN_H = 900          # bunun altındaki dikey klip 1080x1920'de yumuşak kalır
MOTION_FLOOR = 1.6   # ortalama kare farkı (0-255). Altı "donuk" sayılır.
CANDIDATES = 8       # bir terim için denenecek en fazla aday

# Konu doğrulaması. Stok aramalar sessizce alakasız sonuç dönebiliyor —
# ölçüldü: "dog face close up looking at camera" araması yüzü boyalı bir
# İNSAN klibi getirdi. Sağlayıcının kendi metadata'sında (Pexels sayfa
# slug'ı / alt metni, Pixabay etiketleri) konu kelimesi geçmiyorsa aday
# elenir. Ucuz ama bu hata sınıfını tamamen kapatıyor.
SUBJECTS = ("dog", "puppy", "cat", "kitten", "lion", "tiger", "pet")


def required_subjects(query: str) -> list[str]:
    lowered = query.lower()
    return [word for word in SUBJECTS if word in lowered]


def _mentions_subject(haystack: str, required: list[str]) -> bool:
    if not required:
        return True
    lowered = haystack.lower()
    return any(word in lowered for word in required)


@dataclass
class Clip:
    provider: str
    video_id: int
    path: str
    source_page: str
    duration: float
    width: int
    height: int
    motion: float
    query: str


# --------------------------------------------------------------------------
# Arama
# --------------------------------------------------------------------------

def _pexels_candidates(query: str, api_key: str, min_duration: float) -> list[dict]:
    try:
        response = requests.get(
            PEXELS_URL,
            headers={"Authorization": api_key},
            params={"query": query, "orientation": "portrait", "per_page": 20},
            timeout=25,
        )
    except requests.RequestException as error:
        print(f"    Pexels isteği başarısız: {error}")
        return []
    if response.status_code != 200:
        print(f"    Pexels HTTP {response.status_code}: {response.text[:160]}")
        return []

    out: list[dict] = []
    for video in response.json().get("videos", []):
        duration = float(video.get("duration") or 0)
        files = [
            f for f in video.get("video_files", [])
            if f.get("link", "").endswith(".mp4") and (f.get("height") or 0) >= MIN_H
        ]
        if not files:
            continue
        files.sort(key=lambda f: f.get("height") or 0)
        # Hedefi karşılayan en küçük dosya: gereksiz 4K indirmemek için.
        enough = [f for f in files if (f.get("height") or 0) >= TARGET_H]
        chosen = enough[0] if enough else files[-1]
        out.append({
            "provider": "pexels", "id": video["id"], "url": chosen["link"],
            "page": video.get("url", ""), "duration": duration,
            "width": chosen.get("width") or 0, "height": chosen.get("height") or 0,
            "long_enough": duration >= min_duration,
            # Sayfa slug'ı klibin konusunu içeriyor:
            # ".../video-of-dog-wagging-its-tail-6666532/"
            "meta": f"{video.get('url', '')} {video.get('alt', '')}",
        })
    # Yeterince uzun olanlar önce denensin.
    out.sort(key=lambda c: (not c["long_enough"], -c["height"]))
    return out


def _pixabay_candidates(query: str, api_key: str, min_duration: float) -> list[dict]:
    try:
        response = requests.get(
            PIXABAY_URL,
            params={"key": api_key, "q": query, "video_type": "film",
                    "orientation": "vertical", "per_page": 20},
            timeout=25,
        )
    except requests.RequestException as error:
        print(f"    Pixabay isteği başarısız: {error}")
        return []
    if response.status_code != 200:
        print(f"    Pixabay HTTP {response.status_code}: {response.text[:160]}")
        return []

    out: list[dict] = []
    for video in response.json().get("hits", []):
        duration = float(video.get("duration") or 0)
        streams = video.get("videos", {})
        for quality in ("large", "medium", "small"):
            stream = streams.get(quality)
            if stream and (stream.get("height") or 0) >= MIN_H:
                out.append({
                    "provider": "pixabay", "id": video["id"], "url": stream["url"],
                    "page": video.get("pageURL", ""), "duration": duration,
                    "width": stream.get("width") or 0, "height": stream.get("height") or 0,
                    "long_enough": duration >= min_duration,
                    "meta": f"{video.get('pageURL', '')} {video.get('tags', '')}",
                })
                break
    out.sort(key=lambda c: (not c["long_enough"], -c["height"]))
    return out


# --------------------------------------------------------------------------
# Hareket ölçümü
# --------------------------------------------------------------------------

def motion_score(path: Path, samples: int = 24) -> float:
    """Ardışık kareler arası ortalama mutlak fark (0-255).

    Küçük gri kareler üzerinden ölçülür — tam çözünürlükte okumak gereksiz
    pahalı ve sonucu değiştirmiyor. Düşük değer = kamera da özne de sabit,
    yani kullanıcının "donuk kare" dediği klip.
    """
    side = 96  # en-boy bilerek bozuluyor: kare başına bayt sayısı sabit kalsın
    try:
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(path),
             "-vf", f"fps=6,scale={side}:{side}:flags=fast_bilinear,format=gray",
             "-frames:v", str(samples), "-f", "rawvideo", "-"],
            capture_output=True, check=True,
        ).stdout
    except subprocess.CalledProcessError:
        return 0.0

    per_frame = side * side
    count = len(raw) // per_frame
    if count < 2:
        return 0.0
    stack = (np.frombuffer(raw[: count * per_frame], dtype=np.uint8)
             .reshape(count, per_frame).astype(np.int16))
    return float(np.mean(np.abs(np.diff(stack, axis=0))))


# --------------------------------------------------------------------------
# İndirme + önbellek
# --------------------------------------------------------------------------

def _load_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {}


def _save_index(index: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")


def _download(url: str, target: Path) -> bool:
    try:
        with requests.get(url, stream=True, timeout=90) as response:
            if response.status_code != 200:
                print(f"    indirme HTTP {response.status_code}")
                return False
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("wb") as handle:
                for part in response.iter_content(chunk_size=1 << 16):
                    handle.write(part)
        return True
    except requests.RequestException as error:
        print(f"    indirme başarısız: {error}")
        return False


def fetch_clip(
    query: str,
    min_duration: float = 4.0,
    motion_floor: float = MOTION_FLOOR,
    exclude: set[str] | None = None,
    refresh: bool = False,
    must_include: list[str] | None = None,
) -> Clip | None:
    """Terim için uygun bir dikey klip döner; önbellekte varsa indirmez."""
    exclude = exclude or set()
    index = _load_index()
    cache_key = hashlib.sha1(f"{query}|{min_duration}".encode()).hexdigest()[:12]

    cached = index.get(cache_key)
    if cached and not refresh and cached["path"] not in exclude:
        path = PROJECT_ROOT / cached["path"]
        if path.exists():
            print(f"    önbellek: {cached['path']}  (hareket {cached['motion']:.1f})")
            return Clip(**cached)

    pexels_key = key_get("PEXELS_API_KEY")
    pixabay_key = key_get("PIXABAY_API_KEY")
    candidates: list[dict] = []
    if pexels_key:
        candidates += _pexels_candidates(query, pexels_key, min_duration)
    if pixabay_key:
        candidates += _pixabay_candidates(query, pixabay_key, min_duration)
    if not candidates:
        print(f"    '{query}' için aday klip bulunamadı")
        return None

    required = must_include if must_include is not None else required_subjects(query)
    relevant = [c for c in candidates if _mentions_subject(c.get("meta", ""), required)]
    dropped = len(candidates) - len(relevant)
    if dropped:
        print(f"    {dropped} aday konu dışı elendi (aranan: {', '.join(required)})")
    if not relevant:
        print(f"    '{query}': konuyla eşleşen aday yok")
        return None

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    for candidate in relevant[:CANDIDATES]:
        name = f"{candidate['provider']}-{candidate['id']}.mp4"
        target = CACHE_DIR / name
        rel = f"footage/{name}"
        if rel in exclude:
            continue
        if not target.exists() and not _download(candidate["url"], target):
            continue
        motion = motion_score(target)
        if motion < motion_floor:
            print(f"    elendi (donuk, hareket {motion:.1f}): {name}")
            target.unlink(missing_ok=True)
            continue
        clip = Clip(
            provider=candidate["provider"], video_id=candidate["id"], path=rel,
            source_page=candidate["page"], duration=candidate["duration"],
            width=candidate["width"], height=candidate["height"],
            motion=round(motion, 2), query=query,
        )
        index[cache_key] = asdict(clip)
        _save_index(index)
        print(f"    indirildi: {rel}  {clip.width}x{clip.height}  "
              f"{clip.duration:.0f} sn  hareket {motion:.1f}")
        return clip

    print(f"    '{query}': adayların hepsi elendi (hepsi donuk ya da indirilemedi)")
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Dikey stok klip bul ve indir")
    parser.add_argument("query")
    parser.add_argument("--min-duration", type=float, default=4.0)
    parser.add_argument("--motion-floor", type=float, default=MOTION_FLOOR)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    clip = fetch_clip(args.query, args.min_duration, args.motion_floor, refresh=args.refresh)
    if clip is None:
        return 1
    print(json.dumps(asdict(clip), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

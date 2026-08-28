#!/usr/bin/env python3
"""v2 caption üretici — content/storyboards.json'dan yayına hazır açıklama.

v1'deki (make_captions.py) caption'lardan farkı ve nedeni:

* İlk satır videonun kancasıyla aynı. Instagram akışta caption'ın yalnızca
  ilk ~125 karakterini gösterir; v1 orada nötr bir soru cümlesi kullanıyordu.
* CTA tek ve spesifik. "Kaydet, arkadaşına gönder, takip et" üç ayrı istek
  yapıyor ve hiçbirini net sormuyor; v2 tek bir yanıtlanabilir soru sorar —
  yorum, Reels sıralamasında en güçlü erken sinyallerden biri.
* Etiketler daralttı. #hayvanlaralemi / #dogabilgisi gibi geniş ve kanalın
  konusuyla ilgisiz etiketler yerine kedi/köpek nişine ait 5 etiket.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORYBOARDS = PROJECT_ROOT / "content" / "storyboards.json"
MUSIC_LIBRARY = PROJECT_ROOT / "content" / "music_library.json"
BUILD_LOG = PROJECT_ROOT / "content" / "build_log.json"
OUT_DIR = PROJECT_ROOT / "captions" / "reels_v2"

BASE_TAGS = ["#patisifresi", "#kedibilgisi", "#kopekbilgisi", "#evcilhayvan"]
SPECIES_TAG = {"kedi": "#kedi", "kopek": "#kopek"}


def species_of(slug: str) -> str:
    return "kedi" if "kedi" in slug else "kopek"


def footage_credit(slug: str, build_log: dict) -> str:
    """Kullanılan stok kliplerin sağlayıcı künyesi.

    Pexels ve Pixabay atıf zorunlu tutmuyor ama şeffaflık kanalın güven
    iddiasının parçası — hangi görüntünün kanala ait olmadığı görünsün.
    """
    entry = build_log.get(slug)
    if not entry:
        return ""
    providers = sorted({
        shot["provider"] for shot in entry.get("shots", []) if shot.get("provider")
    })
    if not providers:
        return ""
    return "🎬 Video klipler: " + " · ".join(p.capitalize() for p in providers) + " (telifsiz)"


def build_caption(board: dict, music_by_id: dict, build_log: dict) -> str:
    beats = board["beats"]
    hook = next(b for b in beats if b.get("role") == "hook")["vo"]
    cta = next((b for b in beats if b.get("role") == "cta"), None)
    body = " ".join(
        b["vo"] for b in beats
        if b.get("role") not in {"hook", "cta"}
    )

    lines = [hook, "", body, ""]
    if cta:
        lines += [cta["vo"], ""]
    if board.get("image_is_ai", True):
        lines.append("🎨 Temsili AI görseli kullanılmıştır.")
    lines.append(f"📚 Kaynak: {board['source_name']}")
    lines.append(f"🔗 {board['source_url']}")
    credit = footage_credit(board["slug"], build_log)
    if credit:
        lines.append(credit)

    track = music_by_id.get(board.get("music_id", ""))
    if track:
        lines += ["", f"🎵 {track['title']} — {track['artist']} — {track['license']}"]

    tags = BASE_TAGS + [SPECIES_TAG[species_of(board["slug"])]]
    lines += ["", " ".join(tags)]
    return "\n".join(lines)


def main() -> int:
    boards = json.loads(STORYBOARDS.read_text(encoding="utf-8"))
    music_by_id = {
        track["id"]: track
        for track in json.loads(MUSIC_LIBRARY.read_text(encoding="utf-8"))["tracks"]
    }
    build_log = json.loads(BUILD_LOG.read_text(encoding="utf-8")) if BUILD_LOG.exists() else {}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for board in boards:
        path = OUT_DIR / f"{board['slug']}.txt"
        path.write_text(build_caption(board, music_by_id, build_log), encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

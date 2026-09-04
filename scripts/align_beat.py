#!/usr/bin/env python3
"""Yeniden kaydedilen bir beat'i kırpar ve kelime zamanlarını sidecar'a yazar.

    python scripts/align_beat.py 32-kopek-heves-terk alternatif
    python scripts/align_beat.py <slug> <rol> [<rol> ...] --model medium

Neden var (2026-09-04): bir beat'in metni yayından sonra değişip yeniden
seslendirildiğinde, o beat'in `.words.json` sidecar'ı eski kayda ait kalıyor.
`build_reel.py` kart kelime sayısıyla sidecar kelime sayısını karşılaştırıyor;
tutmazsa hizalamayı bırakıp altyazıyı TAHMİN ediyor — yani kelime kilidi
sessizce kayboluyor. Tek beat yeniden kaydedildiğinde çalıştırılacak script
buydu, elle yapılınca kaçan şey de buydu.

Yaptığı iş, `voice_recordings/<slug>/beat_NN_<rol>.wav` için:
  1. baştaki/sondaki sessizliği kırpar (ilk kelime ~0.02 sn'de başlar),
  2. faster-whisper ile kelime zamanlarını çıkarır,
  3. `beat_NN_<rol>.words.json` dosyasını yeniden yazar,
  4. storyboard'daki `chunks` kelime sayısıyla karşılaştırıp uyuşmazlığı
     yüksek sesle bildirir (uyuşmazsa `build_reel` hizalamayı kullanamaz).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORYBOARDS = PROJECT_ROOT / "content" / "storyboards.json"

# make_words.py (2026-09-04) ile birebir aynı kırpma; sidecar zamanları
# KIRPILMIŞ dosyaya göre yazıldığı için bu filtre değişirse sidecar kayar.
TRIM = ("silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB:detection=peak,"
        "areverse,"
        "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB:detection=peak,"
        "areverse")
HEAD = 0.02


def load_board(slug: str) -> dict:
    for entry in json.loads(STORYBOARDS.read_text(encoding="utf-8")):
        if entry.get("slug") == slug:
            return entry
    raise SystemExit(f"'{slug}' content/storyboards.json içinde yok.")


def wav_of(board: dict, index: int, beat: dict) -> Path:
    declared = beat.get("voice_file")
    name = Path(declared).name if declared else f"beat_{index:02d}_{beat.get('role', 'beat')}.wav"
    return PROJECT_ROOT / "voice_recordings" / board["slug"] / name


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True).stdout.strip()
    return float(out or 0.0)


def trim_in_place(wav: Path) -> None:
    tmp = wav.with_suffix(".trim.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(wav),
                    "-af", TRIM, "-ar", "48000", "-ac", "1", str(tmp)], check=True)
    tmp.replace(wav)


def transcribe(wav: Path, model_size: str) -> list[dict]:
    try:
        from faster_whisper import WhisperModel
    except ImportError:  # pragma: no cover - ortam kurulumu
        raise SystemExit("faster-whisper kurulu değil: pip install faster-whisper")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(wav), language="tr", word_timestamps=True)
    words: list[dict] = []
    for segment in segments:
        for word in segment.words or []:
            words.append({"text": word.word.strip(),
                          "start": float(word.start), "end": float(word.end)})
    if not words:
        raise SystemExit(f"{wav.name}: kelime çözümlenemedi")
    base = words[0]["start"]
    return [{"text": w["text"],
             "start": round(w["start"] - base + HEAD, 3),
             "end": round(w["end"] - base + HEAD, 3)} for w in words]


def main() -> int:
    parser = argparse.ArgumentParser(description="Yeniden kaydedilen beat'i kırpar ve hizalar")
    parser.add_argument("slug")
    parser.add_argument("roles", nargs="+", help="Beat rolü (ör. alternatif) ya da sıra numarası")
    parser.add_argument("--model", default="medium", help="faster-whisper modeli (varsayılan: medium)")
    parser.add_argument("--no-trim", action="store_true", help="Kırpmayı atla (dosya zaten kırpılmışsa)")
    args = parser.parse_args()

    board = load_board(args.slug)
    beats = board["beats"]
    mismatch = False

    for token in args.roles:
        picked = [i for i, b in enumerate(beats) if b.get("role") == token]
        if not picked and token.isdigit() and int(token) < len(beats):
            picked = [int(token)]
        if not picked:
            roles = ", ".join(b.get("role", "?") for b in beats)
            raise SystemExit(f"'{token}' bu storyboard'da yok. Roller: {roles}")

        index = picked[0]
        beat = beats[index]
        wav = wav_of(board, index, beat)
        if not wav.exists():
            raise SystemExit(f"kayıt yok: {wav}")

        if not args.no_trim:
            trim_in_place(wav)
        words = transcribe(wav, args.model)
        sidecar = wav.parent / (wav.stem + ".words.json")
        sidecar.write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")

        cards = sum(len(c.split()) for c in (beat.get("chunks") or [beat.get("vo", "")]))
        span, total = words[-1]["end"], duration(wav)
        print(f"{wav.name:28s} {len(words):2d} kelime · dosya {total:5.2f} sn · son kelime {span:5.2f} sn")
        print(f"   çözümlenen: {' '.join(w['text'] for w in words)}")
        if cards != len(words):
            mismatch = True
            print(f"   UYARI: altyazı kartları {cards} kelime, kayıt {len(words)} kelime — "
                  "build_reel hizalamayı KULLANAMAZ. chunks'ı kayda göre düzelt.")
        if abs(total - span) > 0.45:
            print("   UYARI: son kelimeden sonra 0,45 sn'den uzun sessizlik var — kayıt fazla uzun.")

    if mismatch:
        print("\nKart/kayıt uyuşmazlığı var; düzeltmeden build_reel.py çalıştırma.")
        return 1
    print(f"\nSonra:  python scripts/build_reel.py {args.slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate publish-ready caption .txt files for every Reel.

Reel captions are built from content/reel_specs.json (there is no separate
caption source for Reels yet).

Every caption includes the mandatory AI-image disclosure and the source
name, per CONTENT_AND_COMMERCE_RULES.md.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HASHTAGS = "#hayvanbilgisi #dogabilgisi #hayvanlaralemi #patisifresi"


def build_reel_caption(item: dict, music_by_id: dict) -> str:
    track = music_by_id.get(item.get("music_id", ""))
    music_line = (
        f"🎵 Müzik: {track['title']} - {track['artist']} - {track['license']}\n\n"
        if track else ""
    )
    image_line = (
        "" if item.get("image_is_ai", True) is False
        else "🎨 Temsili AI görseli kullanılmıştır. "
    )
    return (
        f"{item['question']}\n\n"
        f"{item['fact']} 🐾\n\n"
        f"Kaydet, arkadaşına gönder, takip et.\n\n"
        f"{image_line}Kaynak: {item['source_name']}\n\n"
        f"{music_line}"
        f"{HASHTAGS}"
    )


def write_reel_captions() -> int:
    specs = json.loads((PROJECT_ROOT / "content" / "reel_specs.json").read_text(encoding="utf-8"))
    music_by_id = {
        t["id"]: t for t in json.loads((PROJECT_ROOT / "content" / "music_library.json").read_text(encoding="utf-8"))["tracks"]
    }
    out_dir = PROJECT_ROOT / "captions" / "reels"
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in specs:
        (out_dir / f"{item['slug']}.txt").write_text(build_reel_caption(item, music_by_id), encoding="utf-8")
    return len(specs)


def main() -> int:
    reel_count = write_reel_captions()
    print(f"{reel_count} Reel caption dosyası -> captions/reels/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

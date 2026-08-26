#!/usr/bin/env python3
"""Pick the next background-music track for a new Reel, enforcing rotation.

Rule (content/music_library.json): the same track must not repeat within
any 7 consecutive published Reels. Looks at content/publish_log.json,
takes the most recently published entries in chronological order, and
returns the first library track whose id is not among the last 7 used.

Usage: python scripts/pick_music.py
Prints the chosen track's id, file path, title, artist, and license line.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = PROJECT_ROOT / "content" / "music_library.json"
LOG_PATH = PROJECT_ROOT / "content" / "publish_log.json"
WINDOW = 7


def main() -> int:
    library = json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))["tracks"]
    log = json.loads(LOG_PATH.read_text(encoding="utf-8")) if LOG_PATH.exists() else {}

    published = [
        entry for entry in log.values()
        if entry.get("published") and entry.get("music_id")
    ]
    published.sort(key=lambda e: e.get("published_at", ""))
    recent_ids = {e["music_id"] for e in published[-WINDOW:]}

    for track in library:
        if track["id"] not in recent_ids:
            print(json.dumps(track, ensure_ascii=False, indent=2))
            print(f"\nCaption satiri: Muzik: {track['title']} - {track['artist']} - {track['license']}")
            return 0

    print("Tum parcalar son 7 yayinda kullanildi -- kutuphaneye yeni parca ekle.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

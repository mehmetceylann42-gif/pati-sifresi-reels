#!/usr/bin/env python3
"""Generate publish-ready caption .txt files for every Reel and feed post.

Reel captions are built from content/reel_specs.json (there is no separate
caption source for Reels yet). Feed-post captions already live fully formed
in content/feed_posts_plan.json; this script just writes them out as files
so both content types are published the same way (publish_reel.py and any
future feed-post publisher both expect a caption *file*).

Every caption includes the mandatory AI-image disclosure and the source
name, per CONTENT_AND_COMMERCE_RULES.md.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HASHTAGS = "#hayvanbilgisi #dogabilgisi #hayvanlaralemi #patisifresi"


def build_reel_caption(item: dict) -> str:
    return (
        f"{item['question']}\n\n"
        f"{item['fact']} 🐾\n\n"
        f"Kaydet, arkadaşına gönder, takip et.\n\n"
        f"🎨 Temsili AI görseli kullanılmıştır. Kaynak: {item['source_name']}\n\n"
        f"{HASHTAGS}"
    )


def write_reel_captions() -> int:
    specs = json.loads((PROJECT_ROOT / "content" / "reel_specs.json").read_text(encoding="utf-8"))
    out_dir = PROJECT_ROOT / "captions" / "reels"
    out_dir.mkdir(parents=True, exist_ok=True)
    for item in specs:
        (out_dir / f"{item['slug']}.txt").write_text(build_reel_caption(item), encoding="utf-8")
    return len(specs)


def write_post_captions() -> int:
    plan = json.loads((PROJECT_ROOT / "content" / "feed_posts_plan.json").read_text(encoding="utf-8"))
    out_dir = PROJECT_ROOT / "captions" / "posts"
    out_dir.mkdir(parents=True, exist_ok=True)
    for post in plan["posts"]:
        slug = Path(post["file"]).stem
        (out_dir / f"{slug}.txt").write_text(post["caption"], encoding="utf-8")
    return len(plan["posts"])


def main() -> int:
    reel_count = write_reel_captions()
    post_count = write_post_captions()
    print(f"{reel_count} Reel caption dosyası -> captions/reels/")
    print(f"{post_count} feed gönderisi caption dosyası -> captions/posts/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

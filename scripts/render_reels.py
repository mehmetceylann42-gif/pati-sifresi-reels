#!/usr/bin/env python3
"""Render Reels from content/reel_specs.json.

Replaces the old render_silent_reel.py / render_reel_batch.py /
render_pet_reels.py, which duplicated the same drawing code three times.
Usage:
    python scripts/render_reels.py --out-dir videos
    python scripts/render_reels.py --out-dir videos --only 07-kedi-tatli-tadi,08-kedi-dili
"""

from __future__ import annotations

import argparse
from pathlib import Path

from reel_kit import PROJECT_ROOT, load_specs, render_item, resolve_image


def main() -> int:
    parser = argparse.ArgumentParser(description="Pati Şifresi Reel render aracı")
    parser.add_argument("--specs", type=Path, default=PROJECT_ROOT / "content" / "reel_specs.json")
    parser.add_argument("--out-dir", type=Path, default=PROJECT_ROOT / "videos")
    parser.add_argument("--only", help="Virgülle ayrılmış slug listesi (boşsa hepsi üretilir)")
    args = parser.parse_args()

    only = set(args.only.split(",")) if args.only else None
    args.out_dir.mkdir(parents=True, exist_ok=True)

    specs = load_specs(args.specs)
    if only:
        specs = [item for item in specs if item["slug"] in only]
        missing = only - {item["slug"] for item in specs}
        if missing:
            print(f"Uyarı: specs içinde bulunamayan slug'lar: {', '.join(sorted(missing))}")

    for item in specs:
        image_path = resolve_image(item, args.specs)
        if not image_path.exists():
            print(f"Atlandı ({item['slug']}): görsel bulunamadı -> {image_path}")
            continue
        output = render_item(item, image_path, args.out_dir)
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

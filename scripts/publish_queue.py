#!/usr/bin/env python3
"""Work through unpublished Reels one at a time via the official Meta API.

Wraps publish_reel.py's logic in a loop driven by content/reel_specs.json,
and tracks what has already gone out in content/publish_log.json so the
same Reel is never posted twice. Dry-run by default, same as publish_reel.py.

A public HTTPS URL per video is required by Meta's API (a local C:\\ path
is not enough) -- pass it with --video-url-template, e.g.:
    --video-url-template "https://videos.example.com/{slug}.mp4"

Usage:
    python scripts/publish_queue.py --video-url-template "https://.../{slug}.mp4"
    python scripts/publish_queue.py --video-url-template "..." --publish --limit 1
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_reel import get_json, load_env, post_form  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPECS_PATH = PROJECT_ROOT / "content" / "reel_specs.json"
LOG_PATH = PROJECT_ROOT / "content" / "publish_log.json"
CAPTIONS_DIR = PROJECT_ROOT / "captions" / "reels"


def load_log() -> dict:
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return {}


def save_log(log: dict) -> None:
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def publish_one(slug: str, video_url: str, caption: str, endpoint: str, user_id: str, access_token: str) -> dict:
    container = post_form(
        f"{endpoint}/{user_id}/media",
        {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "share_to_feed": "true",
            "access_token": access_token,
        },
    )
    container_id = container.get("id")
    if not container_id:
        return {"ok": False, "container": container}

    deadline = time.monotonic() + 60
    status: dict = {}
    while time.monotonic() < deadline:
        status = get_json(f"{endpoint}/{container_id}", {"fields": "status_code,status", "access_token": access_token})
        if status.get("status_code") in {"FINISHED", "ERROR", "EXPIRED"}:
            break
        time.sleep(5)

    if status.get("status_code") != "FINISHED":
        return {"ok": False, "container": container, "status": status}

    published = post_form(f"{endpoint}/{user_id}/media_publish", {"creation_id": container_id, "access_token": access_token})
    return {"ok": True, "container": container, "status": status, "published": published}


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser(description="Pati Şifresi Reel yayın kuyruğu")
    parser.add_argument("--video-url-template", required=True, help='Örn. "https://videos.example.com/{slug}.mp4"')
    parser.add_argument("--publish", action="store_true", help="Gerçekten yayınla (yoksa kuru çalıştırma)")
    parser.add_argument("--limit", type=int, default=1, help="Bu çalıştırmada yayınlanacak en fazla Reel sayısı")
    args = parser.parse_args()

    specs = json.loads(SPECS_PATH.read_text(encoding="utf-8"))
    log = load_log()

    pending = [item for item in specs if not log.get(item["slug"], {}).get("published")]
    if not pending:
        print("Yayınlanmamış Reel kalmadı.")
        return 0

    version = os.getenv("IG_API_VERSION", "v24.0")
    user_id = os.getenv("IG_USER_ID", "")
    access_token = os.getenv("IG_ACCESS_TOKEN", "")
    endpoint = f"https://graph.instagram.com/{version}"

    batch = pending[: args.limit]
    for item in batch:
        slug = item["slug"]
        caption_path = CAPTIONS_DIR / f"{slug}.txt"
        if not caption_path.exists():
            print(f"Atlandı ({slug}): caption dosyası yok -> {caption_path}. Önce scripts/make_captions.py çalıştır.")
            continue
        caption = caption_path.read_text(encoding="utf-8").strip()
        video_url = args.video_url_template.format(slug=slug)

        if not args.publish:
            print(json.dumps({"mode": "dry_run", "slug": slug, "endpoint": f"{endpoint}/{user_id or '<IG_USER_ID>'}/media", "video_url": video_url}, ensure_ascii=False, indent=2))
            continue

        if not user_id or not access_token:
            print("IG_USER_ID ve IG_ACCESS_TOKEN olmadan yayın yapılamaz.", file=sys.stderr)
            return 2

        try:
            result = publish_one(slug, video_url, caption, endpoint, user_id, access_token)
        except (HTTPError, URLError, TimeoutError) as error:
            print(f"Meta API isteği başarısız ({slug}): {error}", file=sys.stderr)
            continue

        print(json.dumps({"slug": slug, **result}, ensure_ascii=False, indent=2))
        if result.get("ok"):
            log[slug] = {"published": True, "published_at": datetime.now(timezone.utc).isoformat()}
            save_log(log)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

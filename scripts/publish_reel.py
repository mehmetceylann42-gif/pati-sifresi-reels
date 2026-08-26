#!/usr/bin/env python3
"""Publish a Reel through Meta's official API, with dry-run as the default."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_env(env_path: Path = PROJECT_ROOT / ".env") -> None:
    """Load KEY=VALUE lines from .env into the process environment.

    Minimal by design (no extra dependency). Existing environment variables
    always win, so `IG_ACCESS_TOKEN=x python script.py` still overrides .env.
    """
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip()


def post_form(url: str, data: dict) -> dict:
    request = Request(
        url,
        data=urlencode(data).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(url: str, params: dict) -> dict:
    with urlopen(f"{url}?{urlencode(params)}", timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser(description="Instagram Reels resmi API yayıncısı")
    parser.add_argument("--video-url", required=True, help="Meta'nın erişebileceği herkese açık MP4/MOV URL")
    parser.add_argument("--caption-file", required=True, type=Path)
    parser.add_argument("--publish", action="store_true", help="Gerçekten container oluşturup yayınla")
    args = parser.parse_args()

    caption = args.caption_file.read_text(encoding="utf-8").strip()
    version = os.getenv("IG_API_VERSION", "v24.0")
    user_id = os.getenv("IG_USER_ID", "")
    access_token = os.getenv("IG_ACCESS_TOKEN", "")
    endpoint = f"https://graph.instagram.com/{version}"
    payload = {
        "media_type": "REELS",
        "video_url": args.video_url,
        "caption": caption,
        "share_to_feed": "true",
    }

    if not args.publish:
        print(json.dumps({"mode": "dry_run", "endpoint": f"{endpoint}/{user_id or '<IG_USER_ID>'}/media", "payload": payload}, ensure_ascii=False, indent=2))
        print("Gerçek yayın için ayrıca --publish ve IG_USER_ID / IG_ACCESS_TOKEN gerekir.")
        return 0

    if not user_id or not access_token:
        print("IG_USER_ID ve IG_ACCESS_TOKEN ortam değişkenleri olmadan yayın yapılamaz.", file=sys.stderr)
        return 2

    try:
        container = post_form(
            f"{endpoint}/{user_id}/media",
            {**payload, "access_token": access_token},
        )
        container_id = container.get("id")
        if not container_id:
            print(json.dumps(container, ensure_ascii=False, indent=2))
            return 3

        deadline = time.monotonic() + 60
        status = {}
        while time.monotonic() < deadline:
            status = get_json(
                f"{endpoint}/{container_id}",
                {"fields": "status_code,status", "access_token": access_token},
            )
            if status.get("status_code") in {"FINISHED", "ERROR", "EXPIRED"}:
                break
            time.sleep(5)

        if status.get("status_code") != "FINISHED":
            print(json.dumps({"container": container, "status": status}, ensure_ascii=False, indent=2))
            return 4

        published = post_form(
            f"{endpoint}/{user_id}/media_publish",
            {"creation_id": container_id, "access_token": access_token},
        )
        print(json.dumps({"container": container, "status": status, "published": published}, ensure_ascii=False, indent=2))
        return 0
    except (HTTPError, URLError, TimeoutError) as error:
        print(f"Meta API isteği başarısız: {error}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())


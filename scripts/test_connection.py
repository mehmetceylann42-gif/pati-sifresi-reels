#!/usr/bin/env python3
"""Read-only sanity check: confirms .env's IG_USER_ID/IG_ACCESS_TOKEN actually
work against the Graph API. Makes a single GET call, publishes nothing.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_reel import get_json, load_env  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    load_env()
    version = os.getenv("IG_API_VERSION", "v24.0")
    user_id = os.getenv("IG_USER_ID", "")
    access_token = os.getenv("IG_ACCESS_TOKEN", "")

    if not user_id or not access_token:
        print("IG_USER_ID / IG_ACCESS_TOKEN .env içinde bulunamadı.", file=sys.stderr)
        return 2

    endpoint = f"https://graph.instagram.com/{version}/{user_id}"
    try:
        result = get_json(endpoint, {"fields": "id,username,account_type,media_count", "access_token": access_token})
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(f"Bağlantı başarısız (HTTP {error.code}):\n{body}", file=sys.stderr)
        return 3
    except URLError as error:
        print(f"Bağlantı başarısız: {error}", file=sys.stderr)
        return 3

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Safely validate an Instagram Login token without printing the token."""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_env() -> None:
    for line in (PROJECT_ROOT / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    load_env()
    host = os.getenv("IG_API_HOST", "graph.instagram.com")
    version = os.getenv("IG_API_VERSION", "v24.0")
    token = os.environ["IG_ACCESS_TOKEN"]
    url = f"https://{host}/{version}/me?" + urlencode({"fields": "id,username", "access_token": token})
    with urlopen(url, timeout=30) as response:
        profile = json.loads(response.read().decode("utf-8"))
    print(json.dumps({"connected": True, "instagram_id": profile.get("id"), "username": profile.get("username")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""API anahtarlarının tek okuma noktası.

Sıra: önce projenin kendi `.env`'i, sonra `EXTERNAL_ENV` ile gösterilen
harici `.env`. Anahtarlar kopyalanmıyor, referansla okunuyor — aynı sır iki
dosyada durursa biri iptal edildiğinde diğeri sessizce eskiyor, ve sızma
yüzeyi ikiye katlanıyor (bkz. `.env.example`'daki 2026-08-28 notu).

`EXTERNAL_ENV` Hayvan-Kanali/.env içinde tanımlanır, örn:
    EXTERNAL_ENV=C:\\Users\\efeka\\Projeler\\youtube otomasyon türkçe\\.env
"""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


_cache: dict[str, str] | None = None


def all_keys() -> dict[str, str]:
    global _cache
    if _cache is not None:
        return _cache
    merged = _read_env_file(PROJECT_ROOT / ".env")
    external = merged.get("EXTERNAL_ENV") or os.environ.get("EXTERNAL_ENV", "")
    if external:
        for key, value in _read_env_file(Path(external)).items():
            merged.setdefault(key, value)
    _cache = merged
    return merged


def get(name: str, default: str = "") -> str:
    """Ortam değişkeni her zaman .env'i ezer (tek seferlik override için)."""
    return os.environ.get(name) or all_keys().get(name, default)


def require(name: str, hint: str = "") -> str:
    value = get(name)
    if not value:
        raise SystemExit(
            f"{name} bulunamadı. Hayvan-Kanali/.env'e yaz ya da EXTERNAL_ENV ile "
            f"anahtarı olan bir .env'i göster." + (f"\n{hint}" if hint else "")
        )
    return value

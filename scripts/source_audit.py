#!/usr/bin/env python3
"""Kaynak denetimi: iddia sınıfı, tazelik, yetki alanı ve link canlılığı.

    python scripts/source_audit.py                  # tüm storyboard'ları denetle
    python scripts/source_audit.py --slug 29-...    # tek bir Reel'i yayın öncesi denetle
    python scripts/source_audit.py --offline        # ağa çıkma, yalnızca alan kontrolü

Neden var (2026-09-03): `25-hayvana-siddet-farkindalik` Reel'i kanalın en çok
izlenen videosu oldu (9.656 izlenme, 181 paylaşım) ama yorumların çoğu
"bilgi yanlış / bizim ülkemizden bahsetmiyorsunuz" dedi. Denetimde çıkan üç
kusur, mevcut "tek ve sağlam kaynak" kuralının yakalayamadığı türdendi:

  1. TAZELİK  — 2021 tarihli 7332 s. Kanun anlatıldı, onu değiştiren
     30/7/2024 tarihli 7527 s. Kanun hiç geçmedi. Hakemli bir davranış
     çalışması 3 yılda eskimez; bir kanun eskir.
  2. YETKİ ALANI — ABD kaynaklı FBI/NIBRS verisi, Türkiye hukuku
     anlatan bir argümanın içinde "kimin verisi" denmeden kullanıldı.
  3. KAYNAK-İDDİA UYUŞMAZLIĞI — `source_name` Türk kanunlarını sayıyordu
     ama `source_url` fbi.gov'a gidiyordu; Türk hukuku iddiasının birincil
     kaynağı hiç yoktu.

Bu yüzden kaynağın prestiji (üniversite/hakemli dergi) tek başına yetmiyor.
Her iddia bir SINIFA yazılır ve sınıfına göre farklı kapıdan geçer:

  A · KALICI    anatomi, fizyoloji, hakemli davranış çalışması.
                Yaş sınırı yok. Gereken: çalışmaya çözülebilir link.
  B · DEĞİŞKEN  istatistik, kurum verisi, hizmet, uygulama, fiyat.
                Son 365 günde yeniden doğrulanmış olmalı.
  C · HUKUK     kanun, ceza, ihbar hattı, resmî prosedür.
                Son 180 günde doğrulanmalı + konsolide mevzuat linki +
                yetki alanı beyanı + kapsam cümlesi zorunlu.

Storyboard alanları (A sınıfı için yalnızca `claim_class` yeterli):

    "claim_class": "C",
    "verified_on": "2026-09-03",
    "jurisdiction": "TR",
    "scope_note": "Ceza 5199 s.K. 28/A'da 'ev hayvanı veya evcil hayvan'
                   için yazılı; sahipsiz sokak hayvanının kapsama girip
                   girmediği yargıda tartışmalı.",
    "extra_sources": ["https://www.mevzuat.gov.tr/..."]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORYBOARDS = PROJECT_ROOT / "content" / "storyboards.json"

MAX_AGE_DAYS = {"A": None, "B": 365, "C": 180}

# Sınıf tahmini yalnızca bir UYARI üretir; beyan edilen `claim_class` esastır.
CLASS_HINTS = {
    "C": ("mevzuat.gov.tr", "resmigazete.gov.tr", "kanun", "sayılı", "r.g.", "yönetmelik", "tbmm"),
    "A": ("pubmed", "pnas.org", "nature.com", "cell.com", "sciencedirect", "science.org",
          "springer", "biomedcentral", "wiley", "doi.org", ".edu"),
}

USER_AGENT = "PatiSifresi-SourceAudit/1.0 (+link liveness check)"

# P8 — Kurum kapısı (KANAL_REHBERI.md §6, 2026-09-04). Türkiye'de barınak
# koşulları güvenli sayılamadığı için hiçbir video/caption bir hayvanın
# barınağa (ya da "yetkililere") teslim edilmesini TAVSİYE edemez. Barınak
# koşullarını ANLATMAK serbest — yasak olan tavsiye kipi, o yüzden kalıp
# kurum adını değil, kurum + devretme fiilini arıyor.
SHELTER_ADVICE = [
    re.compile(r"barına[ğk]\w*(\s+\S+){0,2}\s+(teslim|ver|bırak|götür|gönder)\w*", re.IGNORECASE),
    re.compile(r"(yetkili\w*|belediye\w*|geçici bakımev\w*)(\s+\S+){0,2}\s+teslim\s+et\w*", re.IGNORECASE),
]


def shelter_advice_hits(entry: dict) -> list[str]:
    """Beat metinlerinde ve caption'da barınağa teslim tavsiyesi arar."""
    hits: list[str] = []
    for index, beat in enumerate(entry.get("beats") or []):
        blob = " ".join([beat.get("vo", "")] + list(beat.get("chunks") or []))
        for pattern in SHELTER_ADVICE:
            found = pattern.search(blob)
            if found:
                hits.append(f"beat {index} ({beat.get('role', '?')}): “{found.group(0)}”")
                break

    caption = PROJECT_ROOT / "captions" / "reels_v2" / f"{entry.get('slug', '')}.txt"
    if caption.exists():
        text = caption.read_text(encoding="utf-8")
        for pattern in SHELTER_ADVICE:
            found = pattern.search(text)
            if found:
                hits.append(f"caption: “{found.group(0)}”")
                break
    return hits


def guess_class(name: str, url: str) -> str:
    blob = f"{name} {url}".lower()
    for label in ("C", "A"):
        if any(hint in blob for hint in CLASS_HINTS[label]):
            return label
    return "B"


def host_of(url: str) -> str:
    match = re.match(r"https?://([^/]+)", url or "")
    return match.group(1).lower() if match else ""


def check_link(url: str, timeout: int = 15) -> tuple[str, str]:
    """('canli' | 'olu' | 'bilinmiyor', açıklama).

    'bilinmiyor', sunucunun bir şey söylemediği durumdur: zaman aşımı, DNS,
    TLS zinciri. Bu, linkin öldüğü anlamına GELMEZ — bu makineden
    doğrulanamadığı anlamına gelir (ör. mevzuat.gov.tr bazı ağlardan
    açılmıyor). Ölü linkle karıştırılırsa doğru kaynak yanlışlıkla elenir.
    """
    if not url:
        return "olu", "link yok"
    request = Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            return "canli", f"HTTP {response.status}"
    except HTTPError as error:
        # 403 genelde bot korumasıdır, sayfanın ölü olduğu anlamına gelmez.
        return ("canli" if error.code == 403 else "olu"), f"HTTP {error.code}"
    except (URLError, TimeoutError, OSError) as error:
        return "bilinmiyor", f"ulaşılamadı ({type(error).__name__})"


def audit(entry: dict, offline: bool, today: date) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    name = entry.get("source_name", "")
    url = entry.get("source_url", "")
    declared = (entry.get("claim_class") or "").upper()
    guessed = guess_class(name, url)

    if declared not in MAX_AGE_DAYS:
        errors.append(f"claim_class eksik/geçersiz ({declared or 'yok'}); tahmin: {guessed}")
        declared = guessed
    elif declared != guessed:
        warnings.append(f"claim_class '{declared}' beyan edildi, kaynak '{guessed}' gibi görünüyor")

    if not url:
        errors.append("source_url boş")

    # Kaynak-iddia uyuşmazlığı: Türk mevzuatı anlatan bir iddianın linki
    # yabancı bir siteye gidiyorsa, birincil kaynak aslında hiç yok demektir.
    turkish_law = any(hint in name.lower() for hint in ("sayılı kanun", "r.g.", "yönetmelik", "5199", "7332", "7527"))
    if turkish_law:
        sources = [url] + list(entry.get("extra_sources") or [])
        if not any(host_of(s).endswith(("mevzuat.gov.tr", "resmigazete.gov.tr", "tbmm.gov.tr")) for s in sources):
            errors.append("Türk mevzuatı iddiası var ama mevzuat.gov.tr/resmigazete.gov.tr linki yok")

    limit = MAX_AGE_DAYS[declared]
    verified_on = entry.get("verified_on")
    if limit is not None:
        if not verified_on:
            errors.append(f"{declared} sınıfı için 'verified_on' zorunlu (en fazla {limit} gün)")
        else:
            try:
                age = (today - datetime.strptime(verified_on, "%Y-%m-%d").date()).days
                if age > limit:
                    errors.append(f"doğrulama {age} gün önce yapılmış, {declared} sınıfı sınırı {limit} gün")
                elif age > limit * 0.75:
                    warnings.append(f"doğrulama {age} gün önce; {limit} güne yaklaşıyor")
            except ValueError:
                errors.append(f"verified_on okunamadı: {verified_on!r} (YYYY-AA-GG bekleniyor)")

    if declared in ("B", "C"):
        if not entry.get("jurisdiction"):
            errors.append(f"{declared} sınıfı için 'jurisdiction' zorunlu (ör. \"TR\")")
        foreign = [s for s in [url] + list(entry.get("extra_sources") or [])
                   if host_of(s).endswith((".gov", ".gov.uk")) and not host_of(s).endswith(".gov.tr")]
        if foreign and entry.get("jurisdiction") == "TR" and not entry.get("foreign_data_labeled"):
            errors.append(
                "TR iddiasında yabancı resmî kaynak var; videoda 'kimin verisi' söylenmeli "
                "ve 'foreign_data_labeled': true işaretlenmeli — " + ", ".join(host_of(s) for s in foreign)
            )

    if declared == "C" and not (entry.get("scope_note") or "").strip():
        errors.append("C sınıfı için 'scope_note' zorunlu (iddianın kimi/neyi kapsadığı videoda söylenmeli)")

    # P8 — kurum kapısı: barınağa teslim tavsiyesi yayını durdurur.
    for hit in shelter_advice_hits(entry):
        errors.append(
            "P8 kurum kapısı: barınağa/yetkiliye teslim tavsiyesi var — " + hit
            + " · yerine sahiplendirme yolu söylenmeli (KANAL_REHBERI.md §6 P8)"
        )

    if not offline:
        manual_ok = bool(entry.get("link_checked_manually"))
        for link in [url] + list(entry.get("extra_sources") or []):
            if not link:
                continue
            state, detail = check_link(link)
            if state == "olu":
                errors.append(f"link açılmıyor ({detail}): {link}")
            elif state == "bilinmiyor":
                message = f"link bu makineden doğrulanamadı ({detail}): {link}"
                if declared == "C" and not manual_ok:
                    errors.append(
                        message + " — C sınıfı: linki elle aç, doğruysa "
                        "'link_checked_manually': true ekle"
                    )
                else:
                    warnings.append(message + " — elle doğrula")
            elif not detail.startswith("HTTP 2"):
                # 403 çoğunlukla yayıncının bot koruması; sayfa ölü değil ama
                # elle bir kez açıp doğrulamak gerekir.
                warnings.append(f"link {detail} (elle doğrula): {link}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Kaynak sınıfı, tazelik ve link denetimi")
    parser.add_argument("--slug", help="Yalnızca bu slug'ı denetle")
    parser.add_argument("--offline", action="store_true", help="Ağa çıkma, yalnızca alan kontrolü yap")
    args = parser.parse_args()

    entries = json.loads(STORYBOARDS.read_text(encoding="utf-8"))
    if args.slug:
        entries = [e for e in entries if e.get("slug") == args.slug]
        if not entries:
            print(f"'{args.slug}' storyboards.json içinde yok.", file=sys.stderr)
            return 2

    today = date.today()
    failed = 0
    for entry in entries:
        errors, warnings = audit(entry, args.offline, today)
        if not errors and not warnings:
            print(f"[GEÇTİ ] {entry['slug']}")
            continue
        mark = "[KALDI ]" if errors else "[UYARI ]"
        print(f"{mark} {entry['slug']}")
        for message in errors:
            print(f"          HATA   {message}")
        for message in warnings:
            print(f"          uyarı  {message}")
        failed += bool(errors)

    print(f"\n{len(entries)} kayıt denetlendi, {failed} tanesi yayın kapısından geçemedi.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

# Hayvan Kanali — Pati Şifresi

Hayvan davranışları ve şaşırtıcı biyoloji bilgileri üzerine, dikey Instagram Reels üretim projesi.

## Mevcut çıktı

- 11 adet MP4 Reel (`videos/`) + 10 adet feed görseli (`posts/`)
- Temsili AI görselleri (`assets/`)
- Tüm Reel'leri tek kaynaktan üreten render motoru (`scripts/reel_kit.py` + `scripts/render_reels.py`)
- Yayına hazır başlık/caption dosyaları (`captions/`)
- Konu, kaynak ve yayın notları (`content/`)

## Hızlı devam

1. `AI_HANDOFF.md` dosyasını oku.
2. `content/reel_specs.json` içindeki kaynakları ve yayın notlarını kontrol et.
3. Yeni görselleri `assets/` içine ekle, `content/reel_specs.json`'a yeni bir kayıt olarak ekle.
4. `python scripts/render_reels.py --out-dir videos` ile videoyu üret.
5. `python scripts/make_captions.py` ile caption dosyasını üret.
6. Görsellerin yapay zekâ ile üretildiğini açıklamada şeffaf biçimde belirt.
7. Yayın öncesi kaynak, telif/görüntü hakkı ve hayvan refahı kontrolünü tamamla.

## Teknik not

Videolar 1080×1920, H.264, 30 fps olarak üretilir. Seslendirme yoktur; altyazı videoya gömülüdür. Instagram içinde uygun ses eklenebilir. Render, `requirements.txt`'teki paketleri kuran herhangi bir Python 3.11+ ile çalışır (`pip install -r requirements.txt`); Windows'ta Segoe UI fontları kullanılır (`scripts/reel_kit.py` içindeki `BOLD`/`REGULAR` yolları).


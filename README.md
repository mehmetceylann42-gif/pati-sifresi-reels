# Hayvan Kanali — Pati Şifresi

Kedi ve köpek davranışları, fizyolojisi ve şaşırtıcı bilim bilgileri üzerine, dikey Instagram Reels üretim projesi. (2026-08-27: kanal yalnızca kedi/köpeğe odaklandı, diğer hayvan içeriği kaldırıldı.)

## Mevcut çıktı

- 6 adet MP4 Reel (`videos/`, yalnızca kedi/köpek), her birinde telifsiz arka plan müziği (`audio/`, bkz. `content/music_library.json`)
- Görseller çoğunlukla AI üretimi (`assets/`), uygun olduğunda gerçek/CC0 fotoğraf tercih ediliyor
- Tüm Reel'leri tek kaynaktan üreten render motoru (`scripts/reel_kit.py` + `scripts/render_reels.py`)
- Yayına hazır başlık/caption dosyaları (`captions/reels/`)
- Konu, kaynak ve yayın notları (`content/`)
- Meta Graph API bağlantısı canlı, günlük otomatik yayın görevi kurulu (bkz. `AI_HANDOFF.md`)

## Hızlı devam

1. `AI_HANDOFF.md` dosyasını oku.
2. `CONTENT_AND_COMMERCE_RULES.md` → "İçerik özgünlüğü kriteri"ni kontrol et: yeni fact yalnızca kedi/köpek olmalı ve "herkes zaten biliyor" testinden geçmeli.
3. Yeni görseli `assets/` içine ekle (önce gerçek/CC0 fotoğraf ara, yoksa AI), `content/reel_specs.json`'a yeni bir kayıt olarak ekle.
4. `python scripts/pick_music.py` ile rotasyona uygun müziği seç, `music_id` alanına yaz.
5. `python scripts/render_reels.py --only {slug}` ile videoyu üret, ardından ffmpeg ile müziği göm (bkz. `AI_HANDOFF.md`'deki komut).
6. `python scripts/make_captions.py` ile caption dosyasını üret.
7. Görsellerin yapay zekâ ile üretildiğini açıklamada şeffaf biçimde belirt (gerçek fotoğrafta bu satır otomatik atlanır).
8. Yayın öncesi kaynak, telif/görüntü hakkı ve hayvan refahı kontrolünü tamamla; yeni Reel'i kullanıcı onayı olmadan otomatik kuyruğa/yayına ekleme.

## Teknik not

Videolar 1080×1920, H.264, 30 fps olarak üretilir. Altyazı videoya gömülüdür, artık hepsinde arka plan müziği de var (seslendirme henüz yok). Render, `requirements.txt`'teki paketleri kuran herhangi bir Python 3.11+ ile çalışır (`pip install -r requirements.txt`); Windows'ta Segoe UI fontları kullanılır (`scripts/reel_kit.py` içindeki `BOLD`/`REGULAR` yolları).


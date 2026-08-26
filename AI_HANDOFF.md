# Başka yapay zekâ için devam notu

## Amaç

Instagram hesabı: **Pati Şifresi**. Ana vaat: “Hayvanların davranışlarını ve şaşırtıcı özelliklerini 30 saniyede açıkla.”

## Mevcut durum (güncellendi: 2026-08-27)

- 11 Reel üretildi (`videos/`), 10 feed görseli hazır (`posts/`).
- Her video sessiz, altyazılı, 16–18 saniye, 1080×1920 H.264/30 fps.
- Görseller AI ile üretildi; gerçek görüntü gibi sunulmamalı. Her caption'da “Temsili AI görseli kullanılmıştır.” + kaynak adı otomatik olarak yer alıyor (`scripts/make_captions.py`).
- Tüm Reel/gönderi caption'ları `captions/` altında dosya olarak hazır; `publish_reel.py` ve `publish_queue.py` bunları doğrudan kullanabilir.
- **Meta API bağlantısı canlı.** Hesap: `@patisifresi` (Instagram Login akışı, `graph.instagram.com`, hesap türü Creator). Kimlik bilgileri yalnızca `.env` içinde (`IG_USER_ID`, `IG_ACCESS_TOKEN`, `IG_API_VERSION`) — bu dosya `.gitignore`'da, Git'e hiç girmedi. Başka bir oturum/AI bu kanala erişmek istediğinde token'ı sohbete yazmasın/yeniden istemesin, doğrudan `Hayvan-Kanali/.env` dosyasını okusun.
- **Video hosting canlı.** Videolar public GitHub reposu `https://github.com/mehmetceylann42-gif/pati-sifresi-reels` (main branch) içinde; Meta API'ye doğru `Content-Type: video/mp4` ile servis etmek için GitHub raw değil **jsDelivr CDN** kullanılıyor.
  **Önemli — `@main` KULLANMA:** jsDelivr'in `@main` cache'i içerik değiştiğinde saatlerce bayat dosya döndürebiliyor (purge API'si de her zaman anında işlemiyor); bunun yerine commit hash'e sabitlenmiş URL kullan, her push sonrası garanti güncel:
  `https://cdn.jsdelivr.net/gh/mehmetceylann42-gif/pati-sifresi-reels@{commit-hash}/videos/{slug}.mp4`
  Yeni video/müzik/caption push edildiğinde `git rev-parse HEAD` ile yeni hash'i al ve hem `scripts/daily_publish.ps1`'deki `$template` hem de elle yapılacak yayınlardaki URL'yi güncelle.
- **Müzik eklendi (2026-08-27).** Tüm 11 video artık telifsiz arka plan müziği içeriyor: *Monkeys Spinning Monkeys* — Kevin MacLeod (incompetech.com), CC BY 4.0. Kaynak dosya `audio/monkeys-spinning-monkeys.mp3`; ffmpeg ile `-c:v copy -c:a aac` (video kalitesi korunarak) muxlandı, son 1 saniyede fade-out var. Her caption dosyasına atıf satırı otomatik ekleniyor (`scripts/make_captions.py` → `MUSIC_CREDIT`). Yeni bir Reel eklenirken aynı ffmpeg deseni tekrarlanmalı (bkz. git geçmişi, commit `a9797aa`) veya farklı bir telifsiz parça seçilebilir — API Instagram'ın kendi lisanslı müzik kütüphanesine erişim vermiyor, yalnızca dosyaya gömülü ses yayınlanabilir.
- **Yayınlanmış medya API ile silinemiyor.** `DELETE /{media-id}` çağrısı `IGApiException` (code 100, subcode 33) ile reddediliyor — Instagram Content Publishing API bunu desteklemiyor. Bir gönderiyi kaldırmak gerekirse yalnızca hesap sahibi Instagram uygulamasından elle silebilir; bunu otomasyona bağlama.
- **İlk gerçek yayın (sessiz, artık geçersiz):** `11-kopek-renk-gorusu` → https://www.instagram.com/reel/DchHwVWkUfv/ (media id `18121301962667160`). API ile silinemedi, hesap sahibi elle silecek.
- **Güncel yayın (müzikli):** `11-kopek-renk-gorusu` → https://www.instagram.com/reel/DchNkKlD2dj/ (media id `18116998064511740`). `content/publish_log.json`'da bu kayıtlı.
- **Günlük otomatik yayın açık.** Windows Görev Zamanlayıcı görevi `PatiSifresiDailyReel`, her gün saat 10:00'da `scripts/daily_publish.ps1`'i çalıştırıp kuyruktaki bir sonraki Reel'i **gerçekten yayınlar** (`publish_queue.py --publish --limit 1`). Bu, kullanıcının 2026-08-27 tarihli açık talebiyle kuruldu ve aşağıdaki "İlk 14 gün insan onayı" kuralını bu kuyruk için geçersiz kılar (bkz. `INSTAGRAM_SETUP.md`). Yeni/farklı içerik türleri (yorum otomasyonu, ticari/Guezzo paylaşım vb.) için o kural hâlâ geçerli.
  - Log: `logs/publish_YYYY-MM-DD_HHMMSS.log`
  - Kayıt: `content/publish_log.json` (hangi slug ne zaman/ hangi media id ile gitti)
  - Görevi durdurmak: `schtasks /end /tn "PatiSifresiDailyReel"` çalıştırmaz sadece bekleyeni durdurur; kalıcı silmek için `schtasks /delete /tn "PatiSifresiDailyReel" /f`.
  - Görevi kontrol: `schtasks /query /tn "PatiSifresiDailyReel" /v /fo list`.
- Kuyrukta kalan Reel sayısı: `python scripts/publish_queue.py --video-url-template "https://cdn.jsdelivr.net/gh/mehmetceylann42-gif/pati-sifresi-reels@main/videos/{slug}.mp4"` (dry-run, `--publish` olmadan) ile görülebilir; `content/publish_log.json`'da `published: true` olmayanlar bekliyordur.
- Bağlantıyı test etmek için (salt okunur, hiçbir şey yayınlamaz): `python scripts/test_connection.py`.

## Dosya haritası

- `videos/`: Yayına hazırlanan MP4 taslakları (11 adet).
- `posts/`: Feed görselleri (10 adet, `content/feed_posts_plan.json` ile eşleşir).
- `assets/`: Videolarda/gönderilerde kullanılan yapay zekâ görselleri.
- `scripts/reel_kit.py`: Tüm Reel render mantığının tutulduğu paylaşılan motor (önceki üç ayrı script buraya birleştirildi).
- `scripts/render_reels.py`: `content/reel_specs.json` üzerinden tek veya toplu Reel üretir (`--only slug1,slug2` ile seçili).
- `scripts/make_captions.py`: Her Reel/gönderi için yayına hazır caption dosyası üretir (`captions/`).
- `scripts/publish_reel.py`: Meta Graph API üzerinden tek bir Reel'i yayınlar (varsayılan kuru çalıştırma).
- `scripts/publish_queue.py`: `content/reel_specs.json` + `content/publish_log.json` üzerinden sırayla yayın kuyruğunu işler.
- `content/reel_specs.json`: Tüm Reel'lerin tek kaynağı — render girdisi (görsel, başlık, soru, cevap) ve yayın metadatası (fact, kaynak adı/URL) burada.
- `content/feed_posts_plan.json`: Feed gönderilerinin planı ve hazır caption'ları.
- `content/publish_log.json`: Hangi Reel'in ne zaman yayınlandığının kaydı (publish_queue.py tarafından güncellenir).
- `requirements.txt`: Yerel video üretimi için Python paketleri.

## Yeni Reel üretim kuralı

1. Önce güvenilir kaynak bul: üniversite, müze, bilim kurumu, hakemli araştırma veya resmi hayvan refahı kuruluşu.
2. Tek videoda sadece bir ana iddia kullan.
3. “Kesin teşhis”, tedavi önerisi, hayvanı strese sokacak uygulama, sahte kurtarma ve çalıntı Reels kullanma.
4. AI görseli kullanılıyorsa bunu açıklamada belirt; gerçek doğa görüntüsü izlenimi vermek için kaynak/etiket gizleme.
5. Yeni üretilen bir Reel'i doğrudan otomatik yayın kuyruğuna (`content/reel_specs.json` + `publish_queue.py`) ekleme — önce kullanıcıya göster, onay aldıktan sonra ekle. Kuyruğa zaten eklenmiş, onaylı 11 Reel için günlük otomatik yayın (`PatiSifresiDailyReel` görevi) zaten açık ve bu ayrı bir onay gerektirmez.

## Önerilen sonraki iş

1. Her Reel için Türkçe seslendirme ve telifsiz/Instagram içi ses ekle.
2. Mevcut 11 Reel kuyruğu tükenmeden önce (günde 1 gönderiyle ~10 gün) yeni Reel/caption üretimini planla, yoksa `PatiSifresiDailyReel` görevi "Yayınlanmamış Reel kalmadı" diyerek boşa döner.
3. Feed gönderileri (`posts/`, `content/feed_posts_plan.json`) için de bir yayın mekanizması kurulmadı — henüz yalnızca Reels otomatikleşti.
4. 24 ve 72. saat metrikleriyle en çok kaydedilen/paylaşılan formatı çoğalt (`instagram_business_manage_insights` izni bunun için alındı, henüz kullanılmadı).


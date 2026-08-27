# Başka yapay zekâ için devam notu

## Amaç

Instagram hesabı: **Pati Şifresi**. Ana vaat: “Hayvanların davranışlarını ve şaşırtıcı özelliklerini 30 saniyede açıkla.”

## Mevcut durum (güncellendi: 2026-08-27, dördüncü güncelleme)

- **(2026-08-27) Kanal kedi/köpek dışı tüm içerikten temizlendi.** Kullanıcının açık talebiyle 6 Reel (ahtapot, arı, karga, deniz samuru, fil, baykuş) ve 10 feed gönderisinin tamamı (hepsi kedi/köpek dışıydı) videosu/görseli/caption'ı/kapağıyla birlikte silindi; `content/reel_specs.json`'da yalnızca kedi/köpek Reel'leri kaldı. `content/feed_posts_plan.json` ve `captions/posts/`, `posts/`, `assets/feed-source-visuals/` tamamen kaldırıldı — `scripts/make_captions.py`'den feed-post üretim kodu da çıkarıldı. Bundan sonra üretilecek her Reel yalnızca kedi veya köpek konulu olacak (bkz. `CONTENT_AND_COMMERCE_RULES.md` → "Kanal konumu").
- 7 Reel var (`videos/`): `07-kedi-tatli-tadi`, `08-kedi-dili`, `09-kedi-uykusu`, `10-kopek-burun-izi`, `11-kopek-renk-gorusu`, `12-kedi-mirilti-sifasi`, `13-kopek-kuyruk-yonu`. İlk 5'i AI görseliyle, 12 ve 13'ü gerçek/CC0 lisanslı fotoğrafla üretildi (12: Wikimedia Commons/Unsplash, Scott Webb; 13: Wikimedia Commons/PublicDomainPictures.net, Karen Arnold — "Golden-retriever-dog.jpg", CC0) — AI görseli zorunlu değil, gerçek+telifsiz bir fotoğraf bulunabiliyorsa o tercih edilir (daha güvenilir görünüyor, AI uyarısı gerekmiyor).
- **jsDelivr'in 20MB dosya boyutu limiti var — render sonrası kontrol et.** `reel_kit.py`'nin sabit `quality=8` ayarı, tüylü/dokulu gerçek fotoğraflarda (13'te olduğu gibi) çok daha büyük dosya üretebiliyor (ilk deneme 33MB oldu, jsDelivr "File size exceeded the configured limit of 20 MB" ile 403 döndürdü). Müzik gömüldükten sonra dosya 20MB'ı geçiyorsa: `ffmpeg -y -i videos/{slug}.mp4 -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy videos/{slug}.small.mp4` ile yeniden kodla (CRF 18 görsel olarak kayıpsıza yakın, dosyayı güvenle 20MB altına indiriyor), sonra `videos/{slug}.mp4` üzerine taşı. Push'tan önce `curl -sI https://cdn.jsdelivr.net/gh/.../{hash}/videos/{slug}.mp4` ile 200 döndüğünü doğrula.
- Her video altyazılı, 16–18 saniye, 1080×1920 H.264/30 fps, artık hepsinde arka plan müziği var (aşağıya bakın).
- AI görseli kullanılan Reel'lerde caption'da “Temsili AI görseli kullanılmıştır.” otomatik yer alır; gerçek fotoğraf kullanılanlarda (`item.image_is_ai: false`) bu satır otomatik atlanır (`scripts/make_captions.py`).
- **Profesyonellik/kalite kriteri eklendi (bkz. `CONTENT_AND_COMMERCE_RULES.md` → "Profesyonellik ve kalite kriteri").** Özet: (1) ilk 20 içerik kontrol noktasında Guezzo oranının yanında genel organik performans (kaydetme, paylaşım, tamamlanma) da gözden geçirilecek — en zayıf formatlar tekrarlanmayacak; (2) seslendirme eklenip eklenmeyeceğine sessiz+müzikli formatın ilk 20 gönderilik verisine bakılarak karar verilecek, sezgiyle değil; (3) yayın öncesi 5 maddelik kalite kontrol checklist'i (kaynak linki, yazım, AI etiketi, müzik atfı, altyazı zamanlaması) zorunlu.
- **İçerik özgünlüğü kriteri revize edildi (bkz. `CONTENT_AND_COMMERCE_RULES.md` → "İçerik özgünlüğü kriteri").** Amaç: hızlı takipçi büyümesi, bunun için herkesin bildiği fact'ler artık kabul edilmiyor; yeni her fact "sokak testi" + "şaşırtma anı" + tek sağlam kaynak kriterinden geçmeli. Kalan Reel'lerden `09-kedi-uykusu` bu kritere göre hâlâ zayıf (çok bilinen) — sırası geldiğinde kullanıcıya danışıp daha şaşırtıcı bir kedi fact'iyle değiştirmeyi öner, sessizce silme.
- Tüm Reel/gönderi caption'ları `captions/` altında dosya olarak hazır; `publish_reel.py` ve `publish_queue.py` bunları doğrudan kullanabilir.
- **Meta API bağlantısı canlı.** Hesap: `@patisifresi` (Instagram Login akışı, `graph.instagram.com`, hesap türü Creator). Kimlik bilgileri yalnızca `.env` içinde (`IG_USER_ID`, `IG_ACCESS_TOKEN`, `IG_API_VERSION`) — bu dosya `.gitignore`'da, Git'e hiç girmedi. Başka bir oturum/AI bu kanala erişmek istediğinde token'ı sohbete yazmasın/yeniden istemesin, doğrudan `Hayvan-Kanali/.env` dosyasını okusun.
- **Video hosting canlı.** Videolar public GitHub reposu `https://github.com/mehmetceylann42-gif/pati-sifresi-reels` (main branch) içinde; Meta API'ye doğru `Content-Type: video/mp4` ile servis etmek için GitHub raw değil **jsDelivr CDN** kullanılıyor.
  **Önemli — `@main` KULLANMA:** jsDelivr'in `@main` cache'i içerik değiştiğinde saatlerce bayat dosya döndürebiliyor (purge API'si de her zaman anında işlemiyor); bunun yerine commit hash'e sabitlenmiş URL kullan, her push sonrası garanti güncel:
  `https://cdn.jsdelivr.net/gh/mehmetceylann42-gif/pati-sifresi-reels@{commit-hash}/videos/{slug}.mp4`
  Yeni video/müzik/caption push edildiğinde `git rev-parse HEAD` ile yeni hash'i al ve hem `scripts/daily_publish.ps1`'deki `$template` hem de elle yapılacak yayınlardaki URL'yi güncelle.
- **Müzik kütüphanesi ve rotasyon kuralı (2026-08-27).** Artık 8 parçalık telifsiz (Kevin MacLeod, incompetech.com, CC BY 4.0) bir kütüphane var: `content/music_library.json` (dosyalar `audio/*.mp3`). Kural: aynı parça art arda en fazla 7 gönderide bir tekrar edebilir. Yeni bir Reel render edilmeden önce **`python scripts/pick_music.py`** çalıştır — `content/publish_log.json`'daki son 7 yayının `music_id`'sine bakıp kullanılmamış bir parça önerir. Her `reel_specs.json` girdisine seçilen parçanın `music_id`'si yazılır; `make_captions.py` caption'a otomatik atıf satırı ekler. Video render edildikten sonra müziği gömme deseni:
  ```
  ffmpeg -y -i videos/{slug}.mp4 -ss 0 -t {sure} -i audio/{track}.mp3 \
    -filter_complex "[1:a]afade=t=out:st={sure-1}:d=1,volume=0.85[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -shortest videos/{slug}.tmp.mp4
  ```
  (`-c:v copy` orijinal video kalitesini bozmadan sadece ses ekler.) API Instagram'ın kendi lisanslı müzik kütüphanesine erişim vermiyor, yalnızca dosyaya gömülü ses yayınlanabilir.
- **Yayınlanmış medya API ile silinemiyor.** `DELETE /{media-id}` çağrısı `IGApiException` (code 100, subcode 33) ile reddediliyor — Instagram Content Publishing API bunu desteklemiyor. Bir gönderiyi kaldırmak gerekirse yalnızca hesap sahibi Instagram uygulamasından elle silebilir; bunu otomasyona bağlama.
- **İlk gerçek yayın (sessiz, artık geçersiz):** `11-kopek-renk-gorusu` → https://www.instagram.com/reel/DchHwVWkUfv/ (media id `18121301962667160`). API ile silinemedi, hesap sahibi elle silecek.
- **Güncel yayın (müzikli):** `11-kopek-renk-gorusu` → https://www.instagram.com/reel/DchNkKlD2dj/ (media id `18116998064511740`). `content/publish_log.json`'da bu kayıtlı.
- **12. Reel yayınlandı:** `12-kedi-mirilti-sifasi` → https://www.instagram.com/reel/DchZ9hGEkyy/ (media id `18159692227492822`), müzik `Gymnopedie No. 1`.
- **13. Reel yayınlandı:** `13-kopek-kuyruk-yonu` → https://www.instagram.com/reel/DchdvEegjTF/ (media id `18097113848055000`), müzik `Carefree`. Kullanıcının açık "üret ve paylaş" talebiyle, üretimden yayına insan onayı beklenmeden tek seferde yapıldı (bkz. "Yeni Reel üretim kuralı" madde 7 — bu, o maddenin varsayılan "önce göster" akışına istisnadır, açık talep olduğu için). `content/publish_log.json`'da her iki kayıt da var. Yeni bir Reel üretilip onaylandığında aynı akış tekrarlanır: (1) GitHub'a push, (2) `git rev-parse HEAD` ile yeni commit hash'i al, (3) jsDelivr'in 200 döndüğünü doğrula (20MB limiti için yukarıya bak), (4) `daily_publish.ps1`'deki `$template`'i güncelle, (5) `publish_reel.py` ile yayınla, (6) `publish_log.json`'a `music_id` dahil kaydet.
- **Günlük otomatik yayın açık.** Windows Görev Zamanlayıcı görevi `PatiSifresiDailyReel`, her gün saat 10:00'da `scripts/daily_publish.ps1`'i çalıştırıp kuyruktaki bir sonraki Reel'i **gerçekten yayınlar** (`publish_queue.py --publish --limit 1`). Bu, kullanıcının 2026-08-27 tarihli açık talebiyle kuruldu ve aşağıdaki "İlk 14 gün insan onayı" kuralını bu kuyruk için geçersiz kılar (bkz. `INSTAGRAM_SETUP.md`). Yeni/farklı içerik türleri (yorum otomasyonu, ticari/Guezzo paylaşım vb.) için o kural hâlâ geçerli.
  - Log: `logs/publish_YYYY-MM-DD_HHMMSS.log`
  - Kayıt: `content/publish_log.json` (hangi slug ne zaman/ hangi media id ile gitti)
  - Görevi durdurmak: `schtasks /end /tn "PatiSifresiDailyReel"` çalıştırmaz sadece bekleyeni durdurur; kalıcı silmek için `schtasks /delete /tn "PatiSifresiDailyReel" /f`.
  - Görevi kontrol: `schtasks /query /tn "PatiSifresiDailyReel" /v /fo list`.
- Kuyrukta kalan Reel sayısı: `python scripts/publish_queue.py --video-url-template "https://cdn.jsdelivr.net/gh/mehmetceylann42-gif/pati-sifresi-reels@main/videos/{slug}.mp4"` (dry-run, `--publish` olmadan) ile görülebilir; `content/publish_log.json`'da `published: true` olmayanlar bekliyordur.
- Bağlantıyı test etmek için (salt okunur, hiçbir şey yayınlamaz): `python scripts/test_connection.py`.

## Dosya haritası

- `videos/`: Yayına hazırlanan, müzikli MP4'ler — yalnızca kedi/köpek (7 adet: `07`–`13`).
- `assets/`: Reel görselleri — çoğu AI üretimi, `12-kedi-mirilti-sifasi.jpg` ve `13-kopek-kuyruk-yonu.jpg` gerçek/CC0 fotoğraf. (Feed gönderisi/diğer hayvan görselleri 2026-08-27'de kaldırıldı.)
- `audio/`: Müzik kütüphanesi (8 mp3, hepsi CC BY 4.0 / Kevin MacLeod).
- `content/music_library.json`: Müzik kütüphanesi kataloğu + rotasyon kuralı metni.
- `scripts/pick_music.py`: Yeni Reel için son 7 yayında kullanılmamış bir parça önerir.
- `scripts/reel_kit.py`: Tüm Reel render mantığının tutulduğu paylaşılan motor (önceki üç ayrı script buraya birleştirildi).
- `scripts/render_reels.py`: `content/reel_specs.json` üzerinden tek veya toplu Reel üretir (`--only slug1,slug2` ile seçili).
- `scripts/make_captions.py`: Her Reel için yayına hazır caption dosyası üretir (`captions/reels/`). Feed-post üretimi 2026-08-27'de kaldırıldı.
- `scripts/publish_reel.py`: Meta Graph API üzerinden tek bir Reel'i yayınlar (varsayılan kuru çalıştırma).
- `scripts/publish_queue.py`: `content/reel_specs.json` + `content/publish_log.json` üzerinden sırayla yayın kuyruğunu işler.
- `content/reel_specs.json`: Tüm Reel'lerin tek kaynağı — render girdisi (görsel, başlık, soru, cevap) ve yayın metadatası (fact, kaynak adı/URL) burada. Artık yalnızca kedi/köpek Reel'leri içerir.
- `content/publish_log.json`: Hangi Reel'in ne zaman yayınlandığının kaydı (publish_queue.py tarafından güncellenir).
- `requirements.txt`: Yerel video üretimi için Python paketleri.

## Yeni Reel üretim kuralı

1. **Yalnızca kedi veya köpek** (2026-08-27'den itibaren kesin kural, bkz. `CONTENT_AND_COMMERCE_RULES.md` → "Kanal konumu"). Başka türe çıkılmaz.
2. Güvenilir kaynak bul: üniversite, müze, bilim kurumu, hakemli araştırma veya resmi hayvan refahı kuruluşu.
3. Fact, `CONTENT_AND_COMMERCE_RULES.md` → "İçerik özgünlüğü kriteri"nden geçmeli: sokak testi (herkes zaten biliyor mu?), şaşırtma anı, tek sağlam kaynak. Geçemiyorsa üretme.
4. Tek videoda sadece bir ana iddia kullan.
5. “Kesin teşhis”, tedavi önerisi, hayvanı strese sokacak uygulama, sahte kurtarma ve çalıntı Reels kullanma.
6. Görsel için önce gerçek + telifsiz/CC0 bir fotoğraf ara (ör. Wikimedia Commons, lisansı `CC0` veya `Public domain` olanlar — `CC BY-SA` atıf ister, mümkünse ondan kaçın). Uygun gerçek görsel yoksa AI görseli kullan ve `image_is_ai: true` bırak (varsayılan); AI kullanıldığında caption'da açıkça belirtilir, gerçek doğa görüntüsü izlenimi verilmez.
7. `python scripts/pick_music.py` ile rotasyona uygun müziği seç, `reel_specs.json`'daki `music_id` alanına yaz, video render edildikten sonra ffmpeg ile göm (desen için "Müzik kütüphanesi" bölümüne bak).
8. Yeni üretilen bir Reel'i doğrudan otomatik yayın kuyruğuna (`content/reel_specs.json` + `publish_queue.py`) ekleme — önce kullanıcıya göster, onay aldıktan sonra ekle (kullanıcı üretim + yayını tek seferde açıkça istemedikçe). Kuyruğa zaten eklenmiş, onaylı Reel'ler için günlük otomatik yayın (`PatiSifresiDailyReel` görevi) zaten açık ve bu ayrı bir onay gerektirmez.

## Önerilen sonraki iş

1. Her Reel için Türkçe seslendirme ekle (müzik artık var, seslendirme hâlâ yok) — ama "Profesyonellik ve kalite kriteri" kuralına göre bu karar veriyle verilecek, sezgiyle değil.
2. `09-kedi-uykusu` özgünlük kriterini geçemiyor; daha şaşırtıcı bir kedi fact'iyle değiştirmeyi kullanıcıya öner — kuyruktan sessizce çıkarma.
3. Mevcut Reel kuyruğu tükenmeden önce (günde 1 gönderiyle ilerliyor, kalan 4 Reel ~4 gün sonra biter) yeni kedi/köpek Reel'i üretimini planla, yoksa `PatiSifresiDailyReel` görevi "Yayınlanmamış Reel kalmadı" diyerek boşa döner.
4. Feed gönderisi formatı 2026-08-27'de tamamen kaldırıldı (hepsi kedi/köpek dışıydı) — istenirse yeniden kurulacaksa yalnızca kedi/köpek temalı olmalı.
5. 24 ve 72. saat metrikleriyle en çok kaydedilen/paylaşılan formatı çoğalt (`instagram_business_manage_insights` izni bunun için alındı, henüz kullanılmadı).


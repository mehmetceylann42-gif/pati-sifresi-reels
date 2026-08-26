# Başka yapay zekâ için devam notu

## Amaç

Instagram hesabı: **Pati Şifresi**. Ana vaat: “Hayvanların davranışlarını ve şaşırtıcı özelliklerini 30 saniyede açıkla.”

## Mevcut durum

- 11 Reel üretildi (`videos/`), 10 feed görseli hazır (`posts/`).
- Her video sessiz, altyazılı, 16–18 saniye, 1080×1920 H.264/30 fps.
- Görseller AI ile üretildi; gerçek görüntü gibi sunulmamalı. Her caption'da “Temsili AI görseli kullanılmıştır.” + kaynak adı otomatik olarak yer alıyor (`scripts/make_captions.py`).
- Tüm Reel/gönderi caption'ları `captions/` altında dosya olarak hazır; `publish_reel.py` ve `publish_queue.py` bunları doğrudan kullanabilir.
- Instagram hesabı, Meta API bağlantısı ve yayın izni henüz yapılandırılmadı — bkz. `INSTAGRAM_SETUP.md` (tek ve güncel kurulum kaynağı).
- Videolar için herkese açık bir HTTPS host'u (Meta yayın API'sinin gerektirdiği) henüz seçilmedi; `publish_queue.py --video-url-template` bunu bekliyor.

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
5. Yayın öncesi insan onayı olmadan otomatik paylaşım yapma.

## Önerilen sonraki iş

1. Her Reel için Türkçe seslendirme ve telifsiz/Instagram içi ses ekle.
2. Video dosyalarını yayınlayabilmek için bir herkese açık HTTPS host'u seç ve bağla (kullanıcı kararı gerekir).
3. `INSTAGRAM_SETUP.md`'deki adımları kullanıcıyla birlikte tamamla: profesyonel hesap, Meta geliştirici uygulaması, izinler, `.env` token.
4. 7 günlük yayın sırası oluştur (`content/reel_specs.json` + `content/feed_posts_plan.json` sırasına göre).
5. 24 ve 72. saat metrikleriyle en çok kaydedilen/paylaşılan formatı çoğalt.


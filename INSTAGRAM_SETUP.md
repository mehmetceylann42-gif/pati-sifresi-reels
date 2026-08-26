# Pati Şifresi — Instagram + Meta API kurulumu

Bu dosya, önceki üç ayrı ve birbiriyle kısmen çelişen kurulum notunun
(META_SETUP.md, INSTAGRAM_FIRST_SETUP.md, META_AUTOMATION_DECISION.md)
yerini alan tek ve güncel kaynaktır. Kanal yalnızca **resmî Meta API**
üzerinden yönetilir: şifre paylaşılmaz, toplu takip/spam yorum/sahte
etkileşim aracı kullanılmaz.

## Karar

- Instagram kullanıcı adı: `@patisifresi`.
- Hesap türü: **Professional → Business** (Creator da API ile çalışır, ama
  Business; Guezzo satışı, Meta Business Suite ve ileride reklam/ölçüm
  için daha uygun).
- Bağlantı yolu: **Instagram API with Instagram Login**. Bu yol, klasik
  Facebook Login akışının aksine bağlı bir Facebook Sayfası **gerektirmez**.
- Buna rağmen bir Facebook Sayfası + Meta Business Portfolio kurmak
  **önerilir** (içerik/varlık yönetimi ve ileride reklam ölçümü için) ama
  zorunlu değildir. Kişisel Instagram hesabı bu iş için kullanılmaz.

## Kullanıcının yapacağı adımlar (yalnızca kendi cihazında)

Bu adımlar hiçbir zaman AI'a şifre söylenerek veya sohbette paylaşılan bir
token ile yaptırılmaz — giriş, 2FA ve izin onayı ekranları kullanıcı
tarafından tamamlanır:

1. `@patisifresi` hesabını oluştur veya kendi cihazından giriş yap; hesabı
   herkese açık yap ve iki aşamalı doğrulamayı aç.
2. Ayarlar → Hesap türü ve araçlar → Profesyonel hesaba geç → **Business**.
3. (Önerilir) Aynı adla bir Facebook Sayfası ve Meta Business Portfolio
   oluştur, Instagram hesabını bu Sayfaya bağla.
4. `https://developers.facebook.com/apps/` adresinden yeni bir uygulama
   oluştur; **Instagram API / Instagram Business Login** ürününü ekle.
5. İlk test için kendi Instagram hesabını uygulamanın yönetici veya test
   kullanıcısı rolüne ekle.
6. İzin ekranı açıldığında Instagram hesabınla giriş yap ve yalnızca
   aşağıdaki izinleri onayla.

## İstenen minimum API izinleri

- `instagram_business_basic` — profil ve hesap kimliği.
- `instagram_business_content_publish` — Reel/feed yayınlama.
- `instagram_business_manage_comments` — yorumları okuma ve onaylı yanıt akışı.
- `instagram_business_manage_insights` — performans metrikleri.

## Erişim seviyesi

- **Başlangıç:** Uygulama geliştirme modunda, yalnızca kendi hesabınla test
  yayını yapılabilir.
- **Geniş kullanım:** Başka hesaplar veya daha yüksek kullanım için Meta
  App Review / Advanced Access başvurusu gerekir. Bu proje kapsamında
  şimdilik gerekmiyor.

## Token ve güvenlik kuralı

- Instagram/Facebook şifresi hiçbir zaman proje dosyasına, sohbete veya
  başka bir AI aracına yazılmaz.
- OAuth izin ekranı tamamlandığında alınan erişim token'ı yalnızca yerel
  `.env` dosyasına yazılır (`.env.example`'ı kopyala, `.gitignore`'da).
  Token Git'e, ekran görüntüsüne veya sohbete eklenmez.
- Token süresi dolmadan yenileme planlanır.

## Proje tarafında yapılacaklar

1. `.env.example` dosyasını `.env` olarak kopyala.
2. `IG_USER_ID`, `IG_ACCESS_TOKEN` ve güncel `IG_API_VERSION` değerlerini
   yerelde doldur.
3. Reel videosu Meta'nın erişebileceği herkese açık bir HTTPS URL'sinde
   olmalı — yerel `C:\` yolu yeterli değildir (video hosting seçeneği
   ayrıca kararlaştırılmalı, bkz. AI_HANDOFF.md "Önerilen sonraki iş").
4. Önce kuru çalıştırma yap: `python scripts/publish_reel.py --video-url ... --caption-file ...`
   veya toplu kuyruk için `python scripts/publish_queue.py --video-url-template ...`.
   Gerçek yayın ancak `--publish` bayrağıyla başlar.

## Otomasyon sınırı

- AI: konu araştırması, video/görsel taslağı, caption, yorum yanıt taslağı,
  planlama ve performans özeti üretir.
- Yorumlara AI taslak cevap üretir; otomatik göndermez.
- Ticari (Guezzo) içerikler için onay her zaman insana aittir — bu asla
  değişmez.
- **Güncelleme (2026-08-27):** Kullanıcı, Reel kuyruğunun (`content/reel_specs.json`
  + `content/publish_log.json`) günde bir video olacak şekilde **insan
  onayı olmadan, otomatik olarak** yayınlanmasını açıkça istedi. Bu artık
  Windows Görev Zamanlayıcı görevi `PatiSifresiDailyReel` ile her gün
  10:00'da çalışıyor (bkz. `AI_HANDOFF.md`). Aşağıdaki "yayın öncesi insan
  onayı" kuralı yalnızca bu otomatik Reel kuyruğu için geçersizdir; yeni bir
  içerik türü (yorum otomasyonu, ticari paylaşım, farklı bir hesap/kuyruk)
  eklenmeden önce yine kullanıcıya sorulmalıdır.

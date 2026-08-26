# Pati Şifresi — içerik ve Guezzo ticari kullanım kuralları

Bu dosya, Pati Şifresi projesinde içerik üretirken uyulacak ana kural setidir. Diğer içerik notlarıyla çelişirse bu dosya önceliklidir.

## Kanal konumu

- Kanal adı: **Pati Şifresi**.
- Ana odak: kedi ve köpek sahiplerine kısa, güvenilir, paylaşılabilir bilgi ve günlük yaşam içeriği sunmak.
- Diğer hayvanlar yalnızca kanalı tazelemek için, seyrek biçimde kullanılır.
- Kanal bir reklam vitrini değil; güven inşa eden bir medya hesabıdır. Guezzo, bu güvenin içine yalnızca alakalı bir çözüm olarak girer.

## İçerik dengesi

İlk 20 Reel/feed paylaşımı için hedef dağılım:

- %70: Kedi-köpek bilgisi, davranışı, günlük bakım farkındalığı ve eğlenceli keşifler (14 paylaşım).
- %15: Soru, anket, yorum tetikleyici, takipçi deneyimi ve topluluk içeriği (3 paylaşım).
- %10: Guezzo ile doğal bağ kuran ticari paylaşım (2 paylaşım).
- %5: Diğer hayvanlarla merak/çeşitlilik içeriği (1 paylaşım).

Başlangıçta Guezzo oranı %10'u geçmez. Son 20 içerikte kaydetme, izlenme, profil tıklaması ve satış verileri olumluysa oran en fazla %15'e çıkarılır. %20 oranı, ancak ticari içerikler organik içeriklerin erişimini ve takipçi artışını düşürmüyorsa test edilir.

## Guezzo paylaşım biçimi

Her Guezzo içeriği şu akışla hazırlanır:

1. Sahiplerin yaşadığı gerçek bir problemi veya ihtiyacı anlat.
2. Önce tarafsız, uygulanabilir kısa bilgi ver.
3. Guezzo ürününü ihtiyaca uygun **opsiyonel çözüm** olarak göster.
4. Tek, yumuşak bir harekete geçirici mesaj kullan: profil bağlantısı, ürün sayfası veya indirim kodu.

Yapılmayacaklar:

- Arka arkaya iki Guezzo Reel/feed paylaşımı yapmak.
- Her içerikte fiyat, kampanya veya “hemen al” dili kullanmak.
- Veteriner teşhisi, tedavi, kesin sağlık sonucu veya kanıtsız performans iddiası kullanmak.
- Guezzo ile ilgisiz hayvan bilgisine ürünü zorla bağlamak.
- Ticari ilişkiyi gizlemek.

Ticari/affiliate/hediyeli ürün içeriğinde açıklamaya uygun reklam/iş birliği bildirimi eklenir ve platformdaki ücretli ortaklık etiketi kullanılabiliyorsa kullanılır.

## Ölçüm ve satış disiplini

- Her Guezzo kampanyası için ayrı UTM bağlantısı veya tekil kod kullan: ör. `PATI10`.
- Her ticari içerik için şu metrikleri kaydet: erişim, 3 sn izlenme, tamamlama, kaydetme, paylaşım, profil tıklaması, bağlantı tıklaması, kod kullanımı ve net satış.
- Bir ticari format iki denemede zayıf kalırsa daha fazla reklam eklemek yerine kanca, ürün–ihtiyaç uyumu ve teklif gözden geçirilir.
- Organik içerik başarı metriği yalnızca izlenme değildir: kaydetme, paylaşım ve takip dönüşümü önceliklidir.

## İçerik özgünlüğü kriteri (2026-08-27)

Amaç kısa sürede çok takipçiye ulaşmak; bunun önündeki en büyük engel herkesin
zaten bildiği bir bilgiyi "yeni bir şeymiş gibi" sunmak. Yeni bir fact/Reel
onaylanmadan önce şu testten geçer:

1. **Sokak testi:** Ortalama bir hayvan sahibi bunu lise biyolojisinden, bir
   belgeselden veya "ilginç bilgiler" listesinden zaten biliyor mu? Cevap
   "muhtemelen evet" ise reddedilir. (Örnek reddedilecekler: ahtapotun 3
   kalbi, arı dansı, baykuşun boynunu 270° çevirmesi, kedinin günde 12+ saat
   uyuması — bunlar klişeleşmiş, düşük özgünlüklü fact'ler.)
2. **Şaşırtma anı:** Videoyu izleyen "bunu bilmiyordum, biri daha görsün"
   diye kaydetmeli/paylaşmalı. Cevabın kendisi bir "aha" anı taşımalı, sadece
   bir tanım tekrarı olmamalı.
3. **Tek ve sağlam kaynak:** Üniversite, müze, hakemli dergi veya resmi
   kurum. Kaynak popüler bir "10 ilginç bilgi" listesi/blog ise kabul edilmez.
4. **Kedi/köpek önceliği korunur:** Kanalın ana odağı kedi-köpek olduğu için
   şaşırtıcı fact bulmak zorsa önce bu iki türde derinleşilir (davranış,
   fizyoloji, duyu farkları), diğer hayvanlara nadiren çıkılır.

Mevcut ilk 11 Reel'den şunlar bu kritere göre zayıf (çok bilinen), ileride
değiştirilmesi önerilir ama şimdilik yayın kuyruğunda kalıyor: `01-ahtapot-uc-kalp`,
`02-arilar-yol-tarifi`, `06-baykus-gozleri`, `09-kedi-uykusu`. Yeni üretilecek
Reel'ler doğrudan bu kritere göre seçilir (bkz. `12-kedi-mirilti-sifasi` — kedi
mırıltı frekansının kemik iyileşmesiyle örtüşmesi, çoğu sahibin bilmediği,
üniversite kaynaklı bir fact).

## Müzik çeşitliliği kuralı (2026-08-27)

- Aynı arka plan müziği **art arda en fazla 7 gönderide bir tekrar edebilir**;
  8 parçalık kütüphane bunun için yeterli döngüyü sağlar (bkz.
  `content/music_library.json`).
- Yeni bir Reel render edilmeden önce `python scripts/pick_music.py` çalıştırılır;
  script son 7 yayının müziğini `content/publish_log.json`'dan okuyup
  kullanılmamış bir parça önerir.
- Her parça telifsiz/CC BY 4.0 (Kevin MacLeod, incompetech.com); caption'a
  otomatik atıf satırı eklenir (`scripts/make_captions.py`). Meta'nın resmî
  API'si Instagram'ın lisanslı müzik kütüphanesine erişim vermediği için
  müzik her zaman video dosyasının içine gömülü olmak zorunda (bkz.
  `AI_HANDOFF.md`).
- Kütüphane 8 parçanın altına düşerse (örn. yeni bir tema gerekiyorsa) yeni
  parça eklenir, asla aynı parça daha sık tekrar ettirilmez.

## Yapay zekâ çalışma sınırı

- AI; konu araştırması, video/görsel taslağı, caption, yanıt taslağı, planlama ve performans özeti üretir.
- Yayın öncesinde kaynak, reklam bildirimi, ürün iddiası ve bağlantı insan tarafından onaylanır.
- Resmî Meta API dışında şifre isteyen, takipçi/yorum satın alan, toplu takip yapan veya spam davranışı sergileyen araç kullanılmaz.
- Temsili AI görseli kullanılmışsa caption içinde açıkça belirtilir.


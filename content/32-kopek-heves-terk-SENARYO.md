# 32 — Heves Bitince Terk (seslendirme: kullanıcı)

**Slug:** `32-kopek-heves-terk` · **Format:** 9:16 Reel · **Hedef süre:** ~48–52 sn
**Aile:** 1 (Hak ve prosedür) + 2 (duygusal/kimliksel) karışımı — legal çıpa var ama video duygusal anlatım üzerine kurulu.

---

## 1. Neden bu açı? (viral mantığı)

Kanalın en iyi performans veren videosu (`DcsuTrLkc4b`, 13.264 izlenme) iki şeyi
birlikte yaptı: az bilinen bir hukuki gerçek + izleyiciyi suçlamayan ama
rahatsız eden bir çerçeve. Bu senaryo aynı iskeleti "hayvana şiddet"ten
"hayvanı terk etme"ye taşıyor — çünkü terk, şiddetten çok daha yaygın ve çok
daha az "ben asla yapmam" dedirten bir suç. İzleyicinin çoğu kendini bir
hayvana kötü davranan biri olarak görmüyor; ama heves bitince bir evcil
hayvanı bırakmayı "kötü ama anlaşılır" bir şey olarak görüyor olabilir. Video
tam bu noktayı kırıyor.

**P0 — Paylaşım cümlesi:** *"Ben bir canı, canı sıkılınca bırakmam."*
**P1 — Alıcı:** *"Bunu yeni bir hayvan almayı düşünen ya da yeni aldığı için
hâlâ heves aşamasında olan birine gönder."*
**P2 — İtiraz (videoda karşılanan):** "Bazen gerçekten elde değil, imkân
kalmıyor." → Beat 6'da karşılanıyor: terk etmek yerine somut alternatif
(barınak, ilan, devir) veriliyor. Video "asla bırakma" demiyor, "sokağa
bırakmak seçenek değil" diyor.
**P3 — İddia sınıfı:** C · terk etme fiilinin idari para cezası olduğu,
5199 s.K. m.14/1-n ve m.28 (7527 s.K. ile 2024'te değişik) ile doğrulandı
(bkz. §4). **Tutar söylenmiyor** — KANAL_REHBERI.md Ek Kural gereği (yıllık
yeniden değerleme ile değişiyor).
**P5 — Kapsam:** Bu ceza *sahipli/ev hayvanı* için geçerli — sahipsiz sokak
hayvanına yönelik ayrı bir terk hükmü değil. Video bunu "onu eve getirdin"
çerçevesiyle zaten sahipli hayvana kilitliyor, ayrıca sözlü belirtmeye gerek
yok.
**P6 — İlk üç saniye:** Ters yön — beklenen suçlama ("onu dövdün, aç
bıraktın") yapılmıyor; tam tersi söyleniyor, sonra asıl suçlama geliyor.
**P7 — Zarar kapısı:** CTA "elde değilse bile bırakma" diyor ve gerçek bir
alternatif sunuyor (barınak/ilan/devir) — izleyiciyi çaresiz bırakmıyor.

**Hiçbir yerde şiddet/gore görüntüsü yok.** En sert görsel: bir köpeğin yol
kenarında arabanın arkasından bakması. Bilinçli — grafik içerik erişimi
platformda kısıtlatır ve izleyici acıyı görünce paylaşmadan kaydırır.

---

## 2. Seslendirme metni

Beat isimleri ve `beat_NN_*.wav` dosya adları, kayıt tamamlandığında
`scripts/build_reel.py`'nin beklediği yapıyla uyumlu olsun diye şimdiden
verildi (bkz. [[hayvan-kanali-aup3-seslendirme]] — Audacity'den tek parça
`.aup3` olarak gelirse otomatik beat'lere bölünecek, ayrı ayrı export
gerekmiyor).

| # | Dosya | Metin | Ton |
|---|---|---|---|
| 0 | `beat_00_hook.wav` | Onu hiç dövmedin. Hiç aç bırakmadın. Ama yine de ona hayatının en kötü gününü sen yaşattın. | Sert, alçak, yavaş — üç kısa cümle, aralarda nefes payı bırak. |
| 1 | `beat_01_turn.wav` | Her şey bir hevesle başladı: sosyal medyada gördün, sevimli geldi, aynı gün eve getirdin. | Sıcak, nostaljik — hook'un sertliğinden sonra yumuşama. |
| 2 | `beat_02_mechanism.wav` | Sonra heves bitti. Tüyü evi kirletti, sesi rahatsız etti, bakması zorlaştı. Bir gün onu arabaya bindirdin. | Tempo düşer, gerçekçi, suçlayıcı değil — sadece anlatıyor. |
| 3 | `beat_03_verdict.wav` | Şehir dışında bir yerde durdun, kapıyı açtın, indirdin ve gaza bastın. O, arabanın arkasından koşabildiği kadar koştu. | Videonun en sert anı — net, yavaş, dramatize etmeden. |
| 4 | `beat_04_proof.wav` | Ve büyük ihtimalle bunun bir suç sayılmadığını düşünüyorsun. Yanılıyorsun: kanun buna bir isim koydu — "ev hayvanını terk etmek" — ve hayvan başına idari para cezası öngörüyor. | Soğuk, haber spikeri — "yanılıyorsun"a hafif vurgu. |
| 5 | `beat_05_turn2.wav` | Ama asıl bedeli sen ödemiyorsun. O, yol kenarında günlerce senin dönmeni bekliyor — çünkü sana güvenmişti. | Videonun en yavaş, en alçak cümlesi. "güvenmişti" son kelime gibi bırakılsın. |
| 6 | `beat_06_cta.wav` | Gerçekten elinde değilse bile sokağa bırakmak bir seçenek değil: barınağa teslim et, bir platformda ilan ver, birine devret. Bunu yeni bir hayvan almayı düşünen birine gönder. | Talimat tonu — duygu yok, net bilgi. |
| 7 | `beat_07_closer.wav` | Bir hayvanı sahiplenmek bir heves değil, bir sözdür. Sözünü tutan biri ol. | Sıcak ama kararlı — hook'taki "heves" kelimesiyle kapanış bağlansın. |

Toplam ~123 kelime → deneyimli tempoyla ~48–52 sn civarı bekleniyor (25.
videonun 140 kelime / 53,5 sn oranına yakın).

---

## 3. Görsel yön (öneri — henüz footage indirilmedi)

Önceki videolardaki gibi Pexels'ten dikey (1080×1920) ücretsiz klip aranacak.
Bu bir öneri listesi, `footage/` içine henüz hiçbir şey inmedi:

| # | Beat | Sahne önerisi | Hareket |
|---|---|---|---|
| 0 | hook | Sakin, düz kadraj — sahibiyle mutlu görünen bir köpek/yavru köpek (kontrast için "gayet normal" görünmeli) | static/push_in |
| 1 | turn | Telefonla yavru köpek videosu izleme / pet shop'ta yavru köpek seçme | push_in |
| 2 | mechanism | Ev içinde dağınıklık — kemirilmiş eşya, boşta duran tasma | pan |
| 3 | verdict | Kırsal yol kenarı, uzaklaşan araba, arkadan bakan köpek (**önceki 25. videoda kullanılan boş yağmurlu sokak kliplerine benzer duygusal boşluk mantığı** — hayvan kadrajda kalabilir ama şiddet/gore yok) | pull_out |
| 4 | proof | Kanun kitabı / tokmak yakın plan (25. videoda kullanılan `pexels-6101349.mp4` tekrar kullanılabilir) | pull_out |
| 5 | turn2 | Yalnız köpek, gece, yol kenarında oturmuş, bekliyor | static, çok yavaş zoom |
| 6 | cta | Telefonda barınak/ilan sitesine yazı yazan el | push_in |
| 7 | closer | Barınak gönüllüsü köpeği sahipleniyor/kucaklıyor (25. videoda kullanılan `pexels-7474508.mp4` tekrar kullanılabilir) | pull_out |

Kayıt bittiğinde bu listeyi netleştirip gerçek Pexels linkleriyle
doğrulamak, storyboard'a `media` alanı olarak sabitlemek ve
`content/objections/32-kopek-heves-terk.md` dosyasını yazmak (P2 kalıcı
kayıt için) sıradaki adım — ama önce seslendirme.

---

## 4. Kaynak doğrulama

- **5199 sayılı Hayvanları Koruma Kanunu, m.14/1-n:** yasak fiiller arasında
  "Ev hayvanını terk etmek" açıkça sayılıyor.
- **m.28:** bu fiil için hayvan başına idari para cezası öngörüyor (adli/hapis
  cezası değil — m.28/A yalnızca eziyet, cinsel saldırı, kasten öldürme gibi
  fiiller için hapis cezası düzenliyor, terk etmeyi kapsamıyor).
- **7527 sayılı Kanun (R.G. 02.08.2024):** m.28'deki ceza tutarlarını
  güncelledi. Video ve caption'da **tutar söylenmiyor** — mikroçip cezası
  örneğinde olduğu gibi tutarlar yıllık yeniden değerlemeyle değişiyor,
  rakam vermek videoyu birkaç ay içinde yanlış hâle getirir.
- Kaynaklar: mevzuat.gov.tr — 5199 sayılı Kanun konsolide metni;
  turmob.org.tr — 7527 sayılı Kanun, R.G. 02.08.2024, S.32620.

**Yayın öncesi zorunlu:** `python scripts/source_audit.py --slug
32-kopek-heves-terk` geçmeden yayınlama (KANAL_REHBERI.md §6, P3).

---

## 5. Yayın metni taslağı (açıklama)

> Bir hayvanı almak bir heves değil, bir karar olmalı.
>
> 5199 sayılı Hayvanları Koruma Kanunu'nun 14. maddesinin (n) bendi "ev
> hayvanını terk etmek"i açıkça yasaklıyor; 28. madde bu fiil için hayvan
> başına idari para cezası öngörüyor (tutar her yıl yeniden değerlemeyle
> güncelleniyor, en son 7527 sayılı Kanun'la 2024'te değişti).
>
> Gerçekten bakamayacak durumdaysan bile sokağa bırakmak bir seçenek değil:
> barınağa teslim et, güvenilir bir platformda ilan ver ya da güvendiğin
> birine devret.
>
> Kaynak: 5199 s.K. m.14/1-n, m.28 · 7527 s.K. (R.G. 02.08.2024, S.32620)
>
> #hayvanhaklari #patişifresi #sokakhayvanları #evhayvanı #terketme #köpek
> #kedi #sahiplenme #farkındalık

**Sabitlenecek ilk yorum (yorum motoru):**

> Heves bitince bırakılan bir hayvana hiç tanık oldun mu — sen olsan ne
> yapardın?

---

## 6. Not

Bu senaryo yalnızca metin/seslendirme aşaması için hazırlandı — storyboard
kaydı, footage indirme ve render henüz yapılmadı. Seslendirme
`OneDrive\Desktop\32-kopek-heves-terk-SENARYO.md` içindeki aynı metinle
kaydedilip masaüstüne bırakıldığında ([[hayvan-kanali-aup3-seslendirme]]
yöntemiyle) çıkarılıp beat'lere bölünecek ve pipeline'a bağlanacak.

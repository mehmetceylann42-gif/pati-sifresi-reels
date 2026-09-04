# Pati Şifresi — kanal rehberi v2

**Tarih:** 2026-09-04 · **Kanal verisi:** `content/metrics/snapshot-20260903T2123.json`
(21 Reel, resmî Graph API) · **Rakip verisi:** 12 hesap, 2026-09-04 taraması (§3)

Bu dosya v1'in (2026-09-03) yerine geçer. v1 tek bir videonun 70 kat performans
farkını açıklamaya çalışıyordu; bu sürüm **aynı veriyi bir gün sonraki hâliyle,
artı 12 rakip hesabın performansıyla** birlikte okuyor ve v1'in ana tezini
düzeltiyor. `CONTENT_AND_COMMERCE_RULES.md` ile çeliştiği yerde bu dosya
önceliklidir.

**Bir cümlede karar:** Kanal "ilginç kedi-köpek bilgisi" anlatmayı bırakıyor;
**Türkiye'de bir hayvanla karşılaştığında ne yapacağını söyleyen** hesaba
dönüşüyor.

---

## 1. Veri: bir günde ne değişti

v1, 2 Eylül snapshot'ıyla yazıldı. 3 Eylül'de çekilen snapshot aykırı videonun
**hâlâ hızlanarak** dağıtıldığını gösteriyor:

| | 2 Eylül | 3 Eylül | Değişim |
|---|---|---|---|
| İzlenme | 9.656 | **13.264** | +%37 |
| Erişim | 7.934 | **10.748** | +%35 |
| Paylaşım | 181 | **264** | +%46 |
| Kaydetme | 75 | **113** | +%51 |
| Yorum | 73 | **97** | +%33 |
| Ortalama izleme | 17,0 sn | **18,0 sn** | +1 sn |
| Etkileşim/erişim | %14,0 | **%15,0** | — |

Paylaşım / erişim = **%2,46.** v1'in koyduğu %1 hedefinin 2,5 katı.
Video yayından 4 gün sonra ölmedi, ivmesi arttı — ve **ortalama izleme süresi
yükseldi**, yani sonradan gelen izleyici öncekinden daha ilgili.

Hesabın tamamı (21 Reel, medyan izlenme 141):

| Kademe | Reel | İzlenme | Medyanın katı | Paylaşım |
|---|---|---|---|---|
| **Aykırı** | `DcsuTrLkc4b` hayvana şiddet / kanun | **13.264** | **94,1x** | **264** |
| Orta | `Dclg1XijL9y` kuyruk yönü | 1.290 | 9,1x | 11 |
| | `DcqrygygOpa` şiddetin izi | 1.155 | 8,2x | 2 |
| | `DclwH2Kkm61` suçluluk bakışı | 1.153 | 8,2x | 1 |
| Taban (17 Reel) | kalanların tamamı | 44 – 245 | 0,3 – 1,7x | 0 – 10 |

### 1.1. Asıl kırık: dönüşüm

**13.264 izlenme, 10.748 erişim → takipçi 77'den 84'e çıktı. +7 kişi.**

Dönüşüm oranı **%0,065.** Bir viral videodan beklenen aralık %1–3'tür. Yani
kanalın sorunu artık "dağıtım alamıyorum" değil:

> **Dağıtım geldi ve kanal onu tutamadı.**

Bu, v1'in gözden kaçırdığı en pahalı bulgudur. 10.748 kişi videoyu gördü,
1.021'i beğendi, 264'ü paylaştı — ve 7'si takip etti. Beğenenlerin %99,3'ü
profile hiç uğramadı ya da uğrayıp geri döndü. Sebebi §5'te.

---

## 2. v1'in tezi kısmen yanlıştı

v1 şunu söylüyordu: *"İzleyiciye bir iş ver. Cevap 'öğrenecek' ise video
üretilmez."* (K1 sonuç kapısı.)

Bu kapıdan geçen ilk video **`30-kopek-ovgu-tonu`** 3 Eylül'de yayınlandı.
Kapının istediği her şeye sahipti — somut eylem ("bu akşam dene, aferin'i
gerçekten överek söyle"), gönderilecek kişi ("köpeğiyle monoton konuşan birine
gönder"), hakemli kaynak (Andics ve ark., 2016, *Science*).

**Sonuç: 102 izlenme.** Taban kademe.

Tek video hipotezi çürütmez ve videonun üzerinden bir gün geçmişti. Ama K1'in
**tek başına yeterli olmadığını** gösteriyor. Rakip verisi (§3) bunu doğruluyor:
iş veren ama paylaşılmayan içerik diye bir şey var, ve fazlasıyla var.

### Eksik olan ne

İnsanlar bir videoyu, o video **kendileri hakkında bir şey söylediği için**
paylaşır. Paylaşmak bir bilgi aktarımı değil, bir kimlik beyanıdır.

Aykırı videoyu paylaşan kişi şunu demiş oluyor: **"Ben gördüğümde susmam."**
`30-kopek-ovgu-tonu`'nu paylaşan kişi ise: *"Ben köpeğime doğru tonda aferin
diyorum."* İkincisi kimseye söylenmeye değmez.

Bu, K1'in yerine geçmez — üstüne biner ve onu keskinleştirir.

### Elenen bir açıklama: "aykırı video manuel sesliydi"

Aykırı video kullanıcının kendi sesiyle seslendirilmişti; akla gelen ilk
açıklama bu. **Veri bunu desteklemiyor.** Manuel seslendirmeyle üretilen dört
videodan üçü taban kademede: `19-kopek-uzgun-bakis` 143, `26-kopek-kalp-senkronu`
131, `27-kedi-adini-biliyor` 245 izlenme. Ses kalitesi bir eşik olabilir ama
dağıtımı açan şey değil.

---

## 3. Rakip taraması: 12 hesap

Yöntem: Instagram profil ve Reel verileri arama motoru indeksinden okundu
(Instagram profil sayfaları anonim erişime kapalı, Reel sayfaları kısmen açık).
Beğeni/yorum sayıları indekslenmiş anlık değerlerdir; izlenme sayısı Instagram
tarafından dışarı verilmiyor. Bu yüzden aşağıdaki karşılaştırma
**hesap-içi görecelidir** — mutlak sayılar değil, aynı hesabın kendi içindeki
30–100 katlık farklar sinyaldir.

### 3.1. Hesaplar

| # | Hesap | Takipçi | Gönderi | Takipçi/gönderi | Tip |
|---|---|---|---|---|---|
| 1 | `@evinizdekopekegitimi` | 132K | 1.651 | 80 | Uzman (eğitmen) |
| 2 | `@ver_patini_kopek_egitimi` | 130K | 411 | 316 | Uzman (eğitmen) |
| 3 | `@ilgincbilgilermm` | 116K | 7.874 | 15 | Faceless genel bilgi |
| 4 | **`@hayvananatomi`** | **107K** | **161** | **664** | **Faceless hayvan** |
| 5 | `@kedifanatikleri` | 66K | 7.156 | 9 | Derleme/eğlence |
| 6 | `@kedikopekflix` | 35K | 1.899 | 18 | Derleme/eğlence |
| 7 | `@superkopektv` | 27K | 813 | 33 | Uzman + YouTube |
| 8 | `@yaramazkopekler` | 17K | 225 | 76 | Uzman (eğitmen) |
| 9 | `@gizemlerantolojisi` | 16K | 4.465 | 4 | Faceless genel bilgi |
| 10 | `@psiko.vet` | 13K | 785 | 17 | Uzman (veteriner) |
| 11 | `@dogscallmegina` | 11K | 1.716 | 6 | Uzman (davranış) |
| 12 | `@hayvanatlas` | 6,3K | 159 | 40 | Faceless hayvan |
| — | **`@patisifresi`** | **84** | **21** | **4** | **Faceless hayvan** |

### 3.2. Aynı hesap içinde, konuya göre performans

Bu tablonun tamamı tek tek hesapların **kendi** gönderilerinden:

**`@ver_patini_kopek_egitimi` (130K, köpek eğitmeni):**

| İçerik | Beğeni | Yorum |
|---|---|---|
| "Köpeklerin görevi ne? Gerçeği duyunca kalbine dokunacak…" | **14.000** | 423 |
| "Bazı vedalar sessiz olur… Senin de veda ettiğin bir dostun oldu mu?" | **3.429** | **340** |
| "Reaktif köpek neden bir anda değişir?" (davranış bilgisi) | 361 | 22 |
| "Köpeğin yalnız kalınca ağlamıyor, seni çağırıyor" (davranış bilgisi) | 266 | 31 |
| "Yetişkin köpek eğitimi için geç mi kaldınız?" (bilgi) | 141 | 18 |
| Uluslararası ödül duyurusu (kurumsal) | 23 | 2 |

**Duygusal/kimliksel içerik ile saf davranış bilgisi arasında 40–100 kat fark.**
Aynı hesap, aynı kitle, aynı hafta.

**`@psiko.vet` (13K, veteriner):**

| İçerik | Beğeni |
|---|---|
| Ulusal kanalda haber olma (otorite anı) | 5.882 |
| Sokak hayvanı politikası / "sokakları tilkiler basıyor" (toplumsal öfke) | 1.326 |
| "Zoomiler" — köpeğin evde deli gibi koşması (ilişkilendirilebilir davranış) | 625 |
| Kurtarılan köpeğin eğitimi (hikâye) | 125 |
| Eğitmenlik kursu duyurusu | 42 |

**`@hayvananatomi` (107K, faceless, kanalın format ikizi):**

| İçerik | Beğeni | Yorum |
|---|---|---|
| Öküzkakan kuşu / impala ortakyaşamı (Haziran) | 6.858 | 53 |
| **Aynı konu**, bir ay sonra tekrar (Temmuz) | 533 | 6 |

Bu ikisi kanalımız için en öğretici satır: **aynı hesap, aynı bilgi, 13 kat
fark.** Konu tek başına performansı belirlemiyor. Ayrıca dikkat: 6.858 beğeni
alan videoda yorum oranı %0,8. Bizim aykırı videomuzda 1.021 beğeniye 97 yorum —
**%9,5.** Yorum üretme gücümüz 107K'lık hesabın 12 katı.

### 3.3. Taramadan çıkan dört sonuç

**a) Türkiye'de "faceless kedi-köpek bilgi hesabı" diye başarılı bir kategori
yok.** 100K+ çıkan tek faceless hayvan hesabı `@hayvananatomi` ve o da vahşi
yaşam gösterisi yapıyor — kedi-köpek değil, ve bilgi değil **görüntü** satıyor.
Kedi-köpek tarafında 100K+ olan herkesin ya bir yüzü var (eğitmen, veteriner) ya
da eğlence derliyor.

**b) Uzman hesapları bile bilgiyle büyümüyor.** 130K takipçili bir eğitmenin
davranış bilgisi videoları 141–361 beğeni alıyor. Onu 130K'ya çıkaran şey
duygusal içerik. Yani "daha iyi bilgi vererek" o seviyeye çıkma yolu kapalı.

**c) İngilizce tarafta bu format çökmüş.** "Dog facts" arayan bir taramada
çıkan yeni hesapların beğeni sayıları 0–253 arasında; büyük kısmı AI ile
üretilmiş, birbirinin aynı. Global olarak bu kategori metalaşmış.

**d) Buna karşılık talep boş duruyor.** Aynı konu ("köpeğin uyku pozisyonu ne
anlatıyor") İngilizce'de 28 milyon izlenmeye ulaşmışken Türkçe'deki en iyi
karşılığı 266 bin. **Türkçe pazarda doygunluk yok; nitelikli üretim yok.**

Bu dördü birlikte tek bir yön gösteriyor: kanal, kimsenin iyi yapmadığı ve
kalabalıklaşmamış bir kesişimde durmalı — ve o kesişim "ilginç bilgi" değil.

---

## 4. Karar: yeni yön

### Kanal ne oluyor

> **Türkiye'de bir kedi veya köpekle karşılaştığında ne yapacağını söyleyen
> hesap.**

Kendi hayvanın olabilir, sokaktaki olabilir, komşunun olabilir. Kanal artık
bilgi anlatmıyor; **karar anında lazım olan şeyi** veriyor.

Bu, aykırı videonun kopyası değil — **kategorisi**. O video işe yaradı çünkü
izleyiciye bir rol, bir eylem ve gönderecek bir sebep verdi. Aynı yapı hukuk
dışındaki konularda da kurulabilir ve kurulacak.

### Üç içerik ailesi ve payları

| Aile | Pay | Ne | İddia sınıfı |
|---|---|---|---|
| **1. Hak ve prosedür** | %40 | Kanun, ihbar, belediye yükümlülüğü, veteriner masrafı, mikroçip, sahiplendirme, komşu/site, kayıp hayvan | Çoğunlukla C |
| **2. Yanlış okuma** | %40 | Davranış — ama **her zaman** bir sonucu olan: bugün eve gidince göreceğin/yapacağın bir şey | A |
| **3. Tartışma bitirici** | %20 | İzleyicinin gerçekten yaşadığı tartışmayı bitiren kanıt ("kediler sahibini tanımaz" diyen kişiye gönderilecek şey) | A |

**Saf "ilginç bilgi": %0.** Kanalın taban kademesindeki 17 videonun tamamı bu
türdendi ve toplamı aykırı videonun onda birine ulaşmıyor. Bu tür üretilmeyecek.

### Aile 1 hakkında dürüst uyarı

v1 "bu temayı çoğaltma, hesap aktivizm hesabına döner" diyordu. **Bu kararı
değiştiriyorum, gerekçesiyle:**

Aktivizm ile hak bilgisi aynı şey değil. Aktivizm öfke üretir ve öfkenin
gideceği bir yer yoktur; hak bilgisi ise izleyiciye **kullanabileceği bir şey**
verir. `@psiko.vet`'in politik öfke videosunda 1.326 beğeni ve **0 yorum**
olması bunu gösteriyor — öfke tüketiliyor, konuşulmuyor.

Ayrım şu kuralla korunuyor: **Aile 1'deki her video, izleyicinin bugün
yapabileceği yasal ve kişisel bir eylemle biter.** Eylemi olmayan öfke içeriği
üretilmez. Kimseyi hedef gösteren, bir kurumu veya grubu suçlayan, "katliam"
türü çerçeve kullanan içerik üretilmez.

### Kedi–köpek notu

Aykırı/orta kademedeki dört videonun dördü de köpek. Ama iki kedi videosu
(`DcvLt_jlzmG` ad tanıma, `DcwEAEZjZVW` top getirme) doğru yapıdaydı ve 245/198'de
kaldı — çünkü ikisi de "yanlış okuma"nın sonuçsuz hâliydi. **"Köpek çek, kedi
çekme" sonucu veriye dayanmıyor.** Kedi içeriği devam eder, aynı kapılardan
geçer.

---

## 5. Dönüşüm: takipçiye çevirmenin altyapısı

§1.1'deki %0,065'lik dönüşüm, içerik kararlarından bağımsız olarak düzeltilmesi
gereken bir altyapı sorunudur. Üç sebebi var ve üçü de bu turda düzeltiliyor:

**a) Biyografi izlenen şeyle alakasız.** Eski hâli:

> 🐾 Kedi & köpek sahipleri için kısa, güvenilir bilgiler
> 🎬 Her gün yeni bir pati şifresi
> ✨ Temsili AI görselleri içerir

Hayvan hakları videosundan gelen 10.748 kişiye bu satır hiçbir şey vaat etmiyor.
Üstelik üçüncü satır ("temsili AI görselleri") ilk izlenimde **güvenilirliği
düşürüyor** — kanalın en büyük varlığı kaynak gösteren ciddiyeti iken, profilin
söylediği ilk şeylerden biri "buradaki görüntüler sahte". (Videolar artık
Pexels stok çekimi kullanıyor, AI görsel değil; satır ayrıca teknik olarak da
eskimiş.) Yeni bio `PROFILE_BIO.txt` içinde.

**b) Marka adı yayındaki videolarda yanlış yazılmış.** `CONTENT_AND_COMMERCE_RULES.md`
"PATI ŞİFRESİ yazımı yanlıştır ve kullanılmaz" diyor; yayındaki 21 videonun
tamamında marka etiketi **PATI ŞİFRESİ** (noktasız I) olarak render edilmiş.
Sebebi `scripts/reel_kit_v2.py` içindeki dizgiydi; çalışma ağacında düzeltilmiş
ama henüz commit edilmemiş ve hiçbir yayınlanmış videoya yansımamış. **Bundan
sonra üretilecek her video doğru yazımla çıkar** (doğrulandı: 34 px Segoe UI
Black ile "İ" glifi sorunsuz basılıyor). Eski videolar yeniden yüklenmez.

**c) Grid'de tutarlılık yok.** Profile gelen kişi 17 tane birbirinin aynı
"ilginç bilgi" videosu görüyor. §4'teki üç aile bunu kendiliğinden düzeltecek,
ama ilk 6 yeni videonun **üçü Aile 1'den** olmalı — profile gelen kişi kanalın
ne yaptığını ilk ekranda anlamalı.

---

## 6. Kural seti: sekiz kapı

Her Reel üretime girmeden önce sekiz kapıdan geçer. Bir kapı takılırsa fikir
düzeltilir ya da düşürülür. **P0–P2 yeni, P3–P5 v1'den korundu, P6–P8 yeni.**

### P0 — Paylaşım cümlesi kapısı  ⟵ *yeni birincil kapı*

Üretimden önce tek cümle yazılır:

> **"Bunu paylaşan kişi, paylaşarak ne demiş oluyor?"**

Cevap birinci ya da ikinci tekil bir cümle olmalı ve **kişi hakkında** bir şey
söylemeli:

| ✅ Geçer | ❌ Geçmez |
|---|---|
| "Ben gördüğümde susmam." (aykırı video) | "Ben kedinin dilinde kepçe olduğunu biliyorum." |
| "Sen bunu yanlış biliyorsun, işte doğrusu." | "Bu ilginç bir bilgi." |
| "Ben o an ne yapacağımı bilirim." | "Ben köpeğime doğru tonda aferin diyorum." |

Cümle yazılamıyorsa video üretilmez. Bu kapı `storyboards.json` →
`share_claim` alanına yazılır.

### P1 — Alıcı kapısı  ⟵ *yeni*

Videonun sonunda **tanımlı, gerçek bir kişiye** gönderme talimatı olmalı.
"Herkese gönder", "arkadaşlarınla paylaş" geçersizdir. Alıcı, izleyicinin
telefonunda ismini bulabileceği biri olmalı:

- ✅ "Bunu araba kullanan birine gönder."
- ✅ "Bunu 'nasılsa ceza yok' diyen birine gönder."
- ✅ "Bunu köpeğiyle monoton konuşan birine gönder."
- ❌ "Paylaşmayı unutma."

Rakip taramasındaki en yüksek performanslı cümleler tam olarak bu biçimde
(`@ver_patini`: "kendine karşı fazla sert olan birine gönder" — 14.000 beğeni).
`storyboards.json` → `recipient`.

### P2 — İtiraz kapısı  ⟵ *v1'in K5'i, artık zorunlu ve genişletildi*

Yayından önce en güçlü üç itiraz yazılır (`content/objections/<slug>.md`) ve
**en güçlüsü videonun içinde karşılanır.** v1'de bu yalnızca B ve C sınıfı için
zorunluydu; artık **her video için** zorunlu.

Sebebi: aykırı videonun 97 yorumundaki enerjinin büyük kısmı "yakaladım"
enerjisiydi. İtirazı kendin söylediğinde izleyicinin yakalayacağı bir şey
kalmıyor ve itiraz argümana dönüşüyor.

### P3 — İddia sınıfı kapısı  *(v1 K2, değişmedi)*

| Sınıf | Kapsam | Tazelik | Ek zorunluluk |
|---|---|---|---|
| **A · Kalıcı** | anatomi, fizyoloji, hakemli davranış çalışması | yok | çözülebilir kaynak linki |
| **B · Değişken** | istatistik, kurum verisi, hizmet, uygulama, fiyat | 365 gün | `verified_on`, `jurisdiction` |
| **C · Hukuk / prosedür** | kanun, ceza, ihbar hattı, resmî uygulama | 180 gün | `verified_on`, `jurisdiction`, `scope_note`, **konsolide mevzuat linki** |

C sınıfında konsolide metin zorunlu: `mevzuat.gov.tr`'nin birleştirilmiş kanun
metni. Bir değişiklik kanununun Resmî Gazete sayısı tek başına yetmez.

**Ek kural (yeni):** C sınıfında **para tutarı söylenmez.** İdari para cezaları
her yıl yeniden değerleme oranıyla artıyor (örnek: mikroçip cezası 2021'de
1.200 TL, 2026'da 8.306–10.423 TL). Bir rakam söylemek videoyu 4 ay içinde
yanlış hâle getirir. Bunun yerine: *"idari para cezası var; tutarı her yıl
yeniden değerlemeyle güncelleniyor."*

**Ek kural 2 — hizmet/hat/uygulama iddiaları (2026-09-04'te acıyla öğrenildi):**
Bir ihbar hattı, mobil uygulama, kurum birimi ya da hizmet tavsiye edilecekse,
**kurumsal sayfanın ayakta olması ve uygulamanın mağazada durması yeterli
kanıt değildir.** Doğrulanacak olan sayfa değil, **hizmetin arkasındaki
teşkilatın hâlâ çalışıp çalışmadığıdır.** Aranacak şey: "kapatıldı",
"kaldırıldı", "birim lağvedildi", "hizmet dışı" + kurum adı; ve son 12 ayın
haberleri. Bu tür iddialar B sınıfıdır (365 gün) ama **canlı bir tavsiye olarak
videoda geçecekse 90 gün** tazelik sınırına tabidir.

**Ek kural 3 — izleyici yorumu bir kaynak sinyalidir.** `DcsuTrLkc4b` altında
bir izleyici HAYDİ'nin kaldırıldığını yazmıştı; kontrolde EGM sayfası ve
Play Store listesi ayakta göründüğü için itiraz "yanlış görünüyor" diye
işaretlendi. **İzleyici haklıydı.** Bir yorum somut bir olgusal itiraz
içeriyorsa, kurumsal sayfa onu çürütmez — konuyu ayrıca haber taramasıyla
kontrol et.

`python scripts/source_audit.py --slug <slug>` — geçmeden yayın yok.

### P4 — Yetki alanı kapısı  *(v1 K3, değişmedi)*

Türkiye'yi anlatan bir argümanın içinde yabancı veri kullanılacaksa videoda
**sesli olarak** kimin verisi olduğu söylenir ("ABD'de FBI…").
`foreign_data_labeled: true`.

### P5 — Kapsam cümlesi kapısı  *(v1 K4, değişmedi)*

C sınıfı her videoda iddianın **sınırı** videonun içinde söylenir. Örnek:
*"Bu ceza kanunda ev ve evcil hayvan için yazılı; sahipsiz sokak hayvanının
kapsama girip girmediği hâlâ tartışmalı."*

### P6 — İlk üç saniye kapısı  ⟵ *yeni*

Hook bir **bilgi vaadi** olamaz. Üçünden birini yapmalı:

1. **Kayıp/risk:** izleyicinin yanlış yaptığı ya da kaçırdığı bir şey.
2. **İtiraz:** izleyicinin zaten söylediği cümleyi ona söylemek ("Yasa var ama
   uygulanmıyor diyorsunuz. Haklısınız.").
3. **Ters yön:** beklenen suçlamayı yapmamak ("Çarpıp durmadıysan sebebi
   vicdansızlık değil.").

❌ "Kedinin dilinde gizli bir sünger var." — bilgi vaadi. 122 izlenme.
✅ "2021'e kadar bu ülkede bir sokak köpeğini öldürmenin karşılığı hapis
değildi." — kayıp/şok. 13.264 izlenme.

**Süre notu:** taban kademedeki videolar 16–36 saniye, aykırı video 53 saniye.
Kısa video daha iyi tutmuyor — aykırı videonun ortalama izlenmesi 18 sn iken
16 saniyelik videoların ortalaması 3,8 sn. **Kısalık hedef değildir; her beat
kendi yerini hak etmelidir.**

### P7 — Zarar kapısı  ⟵ *yeni, 2026-09-04*

Videonun verdiği eylem tavsiyesi **birebir uygulanırsa** hayvana zarar verebilir
mi? Hukuken doğru olmak yeterli değildir.

Bu kapı `31-arac-hayvan-carpma` videosu üretildikten **sonra** eklendi, çünkü o
video tam bu duvara çarptı: kanunun "veya götürülmesini sağlamak" ifadesine
dayanarak "hayvanı kendi arabana almak zorunda değilsin, belediyeyi ara"
diyordu. Hukuken kusursuz. Pratikte, kanaması olan bir hayvanda **belediyeyi
beklemek ölüm demek.** Videoyu izleyip bekleyen bir kişi hayvanı kaybederse
bunu yapan biz oluruz — ve kanalın kitlesi bunu ilk yorumda söyler.

Kontrol soruları:

1. İzleyici bu tavsiyeye **harfiyen** uyarsa en kötü sonuç ne olur?
2. Tavsiye bir **gecikme** üretiyor mu? Acil bir durumda gecikme tavsiye
   edilemez.
3. Tavsiye izleyiciyi hukuken haklı ama fiilen çaresiz mi bırakıyor?
4. Yerine geçen bir "önce şunu yap" cümlesi var mı?

Kapıdan geçmeyen fikir düzeltilir; düzeltilemiyorsa düşürülür. Bu kanalda
**hız gerektiren hiçbir konuda "bekle/ara" ilk adım olamaz.**

### P8 — Kurum kapısı: barınak tavsiye edilmez  ⟵ *yeni, 2026-09-04*

**Hiçbir videoda, caption'da ya da sabit yorumda bir hayvanın barınağa
teslim edilmesi tavsiye edilmez.** Belediye barınağı, geçici bakımevi,
"yetkililere teslim et" gibi dolaylı biçimleri de dahil.

Sebep: Türkiye'de barınak koşulları tekdüze değil ve kamuoyunun büyük
kısmı barınağı güvenli bir yer saymıyor. İzleyicinin gözünde "barınağa
ver" tavsiyesi, hayvanı kurtarmanın değil **sorumluluğu devretmenin**
adı — ve kanalın kendi mesajını (terk etme) çürütüyor.

Bu kapı `32-kopek-heves-terk` yayınlandıktan **sonra** eklendi: video
"barınağa teslim et" diyordu ve tepki tam bu cümleye geldi. `content/objections/32-kopek-heves-terk.md`
bu itirazı üretimden önce zaten öngörmüştü ("Barınağa vermek zaten ölüme
terk etmek") ama itiraz "videoda karşılanmıyor" notuyla geçildi. **Öngörülen
bir itiraz karşılanmadan yayına çıkarsa, o itiraz yoruma dönüşür.**

Yerine söylenecek olan — hepsi sorumluluğu izleyicide bırakır:

| ❌ Söylenmez | ✅ Yerine |
|---|---|
| "Barınağa teslim et." | "Sahiplendirme ilanı ver, yeni sahibini sen bul." |
| "Belediyeye/yetkililere ver." | "Güvendiğin birine devret, teslim edeceğin kişiyi tanı." |
| "Geçici bakımevine bırak." | "Bulana kadar sorumluluk sende." |

**İstisna:** barınak koşullarının *kendisi* konu olan bir video barınaktan
söz edebilir — yasak olan **tavsiye**, kelimenin kendisi değil. Ayrıca
`scripts/source_audit.py` her storyboard'ın beat metinlerini tarar; barınağa
teslim tavsiyesi içeren bir cümle yayın kapısını otomatik olarak kapatır.

---

## 7. Ölçüm

**Birincil metrik: erişim başına paylaşım.** (v1'den korundu; §1'de doğrulandı.)
**İkincil ve eşit önemde: erişim başına takip.** (§1.1'deki asıl kırık.)

Hedefler (erişim > 1.000 olan videolar için; altındakiler gürültü sayılır):

| Metrik | Bugünkü medyan | Aykırı video | Hedef |
|---|---|---|---|
| Paylaşım / erişim | ~%0 | %2,46 | **≥ %1** |
| **Takip / erişim** | **%0,065** | %0,065 | **≥ %0,5** |
| Kaydetme / erişim | ~%0,3 | %1,05 | ≥ %0,8 |
| Ortalama izleme | 7,0 sn | 18,0 sn | ≥ 11 sn |
| Etkileşim / erişim | ~%3 | %15,0 | ≥ %6 |

**Hipotez testi:** Sonraki 10 Reel'in tamamı P0–P6'dan geçirilerek üretilir.
10. videodan sonra `python scripts/metrics.py` çalıştırılır.

- Paylaşım/erişim medyanı %1'i **ve** takip/erişim %0,5'i geçtiyse → kural seti
  kalıcı olur.
- Paylaşım hedefi tutup takip tutmadıysa → sorun içerikte değil profildedir;
  §5 yeniden ele alınır.
- İkisi de tutmadıysa → P0 hipotezi çürütülmüştür; sorun format değil dağıtımdır
  ve tez yeniden yazılır.

Sezgiyle "işe yarıyor galiba" denmez.

---

## 8. Araçlar ve açık borçlar

### Çalışan araçlar

**`scripts/metrics.py`** — tüm Reel metriklerini çeker, arşivler, medyanın 3
katını aşan aykırıları listeler. Yalnızca okuma yapar.

**`scripts/source_audit.py`** — P3–P5 kapılarının kod hâli. Geriye dönük
çalıştırıldığında aykırı videonun dört kusurunu da yakalıyor.

### Kapatılması gereken eksikler

1. **`instagram_business_manage_comments` izni alınmamış — 1 numaralı iş.**
   Graph API 97 yorumun 0'ını döndürüyor. Kanalın en değerli geri bildirim
   kanalı otomasyona görünmez. Meta uygulamasını bu izinle yeniden yetkilendirip
   token yenilenmeli. `metrics.py` bu durumu tespit edip uyarı basıyor.
2. **Sızmış token hâlâ Git geçmişinde** (`AI_HANDOFF.md` madde 2). İptal
   edilmedi. Güvenlik açısından listedeki en acil madde.
3. **Marka yazımı düzeltmesi commit edilmedi** (§5b). `scripts/reel_kit_v2.py`,
   `scripts/reel_kit.py`, `scripts/render_reel_covers.py` çalışma ağacında
   düzeltilmiş durumda.
4. **İki paralel içerik kaynağı:** `reel_specs.json` (v1, 9 kayıt, donmuş) ve
   `storyboards.json` (v2, 21 kayıt). v1 kaldırılmalı.
5. **`29-hayvana-eziyet-sorusturma-sarti` üretilmedi.** Storyboard'u ve itiraz
   provası hazır, video yok. Aykırı videonun 97 yorumundaki en güçlü itiraza
   ("yasa var ama uygulanmıyor") cevap veriyor ve talebi kanıtlı.

---

## 8.1. Geçersiz kaynaklar kütüğü

Bir kez doğrulanmış ve **artık kullanılmaması gereken** şeyler. Yeni video
yazarken önce buraya bakılır.

| Ne | Durum | Doğrulandığı tarih |
|---|---|---|
| **HAYDİ (Hayvan Durum İzleme) uygulaması** | **KULLANILMAZ.** Aralık 2025'te EGM, 81 il emniyet müdürlüğüne yazı göndererek Çevre, Doğa ve Hayvanları Koruma Şube Müdürlükleri ile büro amirliklerini kapattı; jandarmadaki karşılıkları da sonlandırıldı. HAYDİ ihbarlarını karşılayan birimler bunlardı. `asayis.pol.tr` sayfası ve Play Store listesi hâlâ ayakta — **bunlar hizmetin çalıştığını göstermiyor.** | 2026-09-04 |
| **155 / 156 / 110 ayrı ayrı** | Kullanılmaz. 112 Acil Çağrı Merkezi'ne entegre edildi; aranırsa yönlendiriliyor. Videoda **tek numara söylenir: 112.** Panik anında iki numara karar maliyeti yaratır. | 2026-09-04 |
| **ALO 174** | Hayvan hakkı ihbarı için kullanılmaz — gıda güvenliği hattıdır. | 2026-09-04 |

**Yerine ne söylenir:** 112 (telefon veya SMS). Acil olmayan, kayda geçmesi
istenen başvurular için CİMER. Sahipsiz hayvanın bakım/tedavisi için belediyenin
veteriner işleri müdürlüğü — ama **P7 gereği acil durumda ilk adım olarak
değil.**

### Yayındaki videoya etkisi

`DcsuTrLkc4b` (13.264 izlenme) hem seslendirmesinde hem caption'ında HAYDİ'ye
yönlendiriyor. Video silinmez — kanalın tek gerçek dağıtım varlığı. **Sabitlenmiş
düzeltme yorumu bu maddeyi de içermeli** ve caption elle güncellenmeli (§9).

---

## 9. Şimdi yapılacaklar

**Canlı videoya dair (elle, API'den yapılamaz):**

1. **Sabitlenmiş düzeltme yorumu yaz.** Videoyu silme — 13.264 izlenme ve 264
   paylaşım kanalın tek gerçek dağıtım varlığı. Yorum **dört** şeyi söylesin:
   (a) **HAYDİ birimleri Aralık 2025'te kapatıldı, ihbar artık 112'ye yapılır** —
   videoda ve caption'da HAYDİ geçiyor, bu madde ilk sırada olmalı; (b) 2024'te
   7527 sayılı Kanun'la mevzuatın bir kez daha değiştiği; (c) FBI verisinin ABD
   verisi olduğu; (d) cezanın kanundaki kapsamının tartışmalı olduğu.
2. **`DcsuTrLkc4b` caption'ını elle güncelle:** "HAYDİ uygulamasından ya da acil
   durumda 112'den" → "112'den (telefon veya SMS)". Caption düzenlemesi izlenmeyi
   sıfırlamaz.
3. **Biyografiyi değiştir** (`PROFILE_BIO.txt`).

**Üretim:**

4. **`29-hayvana-eziyet-sorusturma-sarti` — üretildi (61,6 sn), yayın onayı bekliyor** (§10).
5. `31-arac-hayvan-carpma` — P7 kapısında düştü, yayınlanmayacak (§11). Konu yeniden yazılabilir.

**Altyapı:**

6. Yorum iznini al, token'ı yenile.
7. Sızmış token'ı Meta'dan iptal et.
8. 10 Reel sonra §7'deki testi çalıştır.

---

## 10. Sıradaki video: `29-hayvana-eziyet-sorusturma-sarti`

**Konu:** "Yasa var ama kimse ceza almıyor" itirazının gerçek cevabı —
5199 s.K. m.28/A son fıkrasındaki **muhakeme şartı**. Şikâyet dilekçesi tek
başına dosya açmıyor; Tarım ve Orman Bakanlığı il/ilçe müdürlüğünün savcılığa
yazılı başvurusu gerekiyor. Tek istisna suçüstü.

| Kapı | Durum |
|---|---|
| **P0 paylaşım cümlesi** | "Ben neden ceza çıkmadığını biliyorum — ve hangi kapının çalınacağını da." ✅ |
| **P1 alıcı** | "Bunu 'nasılsa ceza yok' diyen birine gönder." ✅ |
| **P2 itiraz** | Videonun tamamı `DcsuTrLkc4b`'nin 97 yorumundaki en güçlü itirazın cevabı ✅ |
| **P3 iddia sınıfı** | C · konsolide metin indirilip m.28/A son fıkrası satır satır okundu; ceza tutarı ve dava sayısı yok ✅ |
| **P4 yetki alanı** | Tamamen TR ✅ |
| **P5 kapsam cümlesi** | Sahipli/sahipsiz ayrımı ve "başka bir kişi" koşulu videoda söyleniyor ✅ |
| **P6 ilk üç saniye** | İtiraz tipi; hook bağımsız çalışacak şekilde yeniden yazıldı ✅ |
| **P7 zarar** | Acil durumda ilk adım 112; hiçbir tavsiye bekleme önermiyor ✅ |

**Doygunluk taraması (2026-09-04):** `site:instagram.com` üzerinde konu araması
**sıfır sonuç** döndürdü. Yalnızca hukuk bloglarında, orada da kanun metni
birebir kopyalanarak var — hiçbiri pratikte ne anlama geldiğini anlatmıyor.
**Talep kanıtlı (97 yorum), doygunluk sıfır, açı farkı net.** Kanalın bugüne
kadarki en temiz doygunluk sonucu bu.

Üretildi: `videos_v2/29-hayvana-eziyet-sorusturma-sarti.mp4`, 61,6 sn.
Yayınlanmadı.

### Değerlendirilip düşürülen fikir: apartmanda hayvan yasağı

Kat Mülkiyeti Kanunu m.28 (yönetim planı değişikliği için beşte dört çoğunluk)
ve m.33 (kurul kararına karşı bir aylık iptal davası) üzerine kurulacak bir
video hazırlandı ve **doygunluk kapısında düşürüldü:** konu Instagram'da en az
altı hukuk hesabı tarafından işlenmiş (Ceylan Hukuk, Av. Ceren Önal ve
diğerleri). Ayrıca dayanak içtihat — Yargıtay HGK 2017/3018 E., 2022/6 K. —
hukuk kaynaklarında **çelişkili** yorumlanıyor: bir kısmı yönetim planındaki
yasağın mutlak olduğunu, bir kısmı somut rahatsızlığın ayrıca araştırılması
gerektiğini söylüyor. Bu belirsizlik C sınıfı bir videoya taşınamaz.

---

## 11. Geri çekilen video: `31-arac-hayvan-carpma`

> **2026-09-04 — bu video P7 kapısında düştü ve yayınlanmayacak.** Üretildi
> (57,9 sn), sonra iki sebeple geri çekildi:
>
> 1. **Zarar (P7):** "Hayvanı kendi arabana almak zorunda değilsin, belediyeyi
>    ara" mesajı hukuken doğru ama pratikte gecikme üretiyor. Kanaması olan bir
>    hayvanda beklemek ölüm demek.
> 2. **Geçersiz kaynak (§8.1):** CTA'sı HAYDİ'ye yönlendiriyordu.
>
> Konu ölü değil — **yeniden yazılabilir**, ama kilit cümlesi tersine çevrilerek:
> "önce sen götür, götüremiyorsan kanun arattırmayı da yeterli sayıyor." Bu
> hâliyle P7'den geçer. Dosyalar `content/objections/31-arac-hayvan-carpma.md`
> ve storyboard kaydında duruyor; video `videos_v2/` altında, yayınlanmadı.

### Kapı dökümü (kayıt için)

**Konu:** Bir hayvana çarpan sürücünün kanuni yükümlülüğü — ve maddenin
kimsenin okumadığı yarısı.

| Kapı | Durum |
|---|---|
| **P0 paylaşım cümlesi** | "Ben o an ne yapacağımı bilirim — sen de bil." ✅ |
| **P1 alıcı** | "Bunu araba kullanan birine gönder." ✅ |
| **P2 itiraz** | `content/objections/31-arac-hayvan-carpma.md`; en güçlüsü videoda ✅ |
| **P3 iddia sınıfı** | C · 5199 s.K. m.21 + m.4/j, konsolide metin doğrulandı ✅ |
| **P4 yetki alanı** | Tamamen TR; yabancı veri yok ✅ |
| **P5 kapsam cümlesi** | Masrafı kimin ödediği videoda söyleniyor ✅ |
| **P6 ilk üç saniye** | Ters yön: beklenen suçlama yapılmıyor ✅ |

**Doygunluk taraması:** Madde 21'in metni Instagram'da çok kez paylaşılmış —
ama istisnasız hepsi kanun metnini alıntılayan afiş/bildiri biçiminde. Hiçbiri
(a) "götürülmesini sağlamak" ifadesinin ne anlama geldiğini, (b) masrafı kimin
ödediğini, (c) neden ceza kesilmediğini açıklamıyor. YouTube'daki en iyi
karşılık 7 yıllık ve 2,2 bin izlenmeli. **Talep kanıtlı, doygunluk yok, açı
farkı net.**

Senaryo `content/storyboards.json` içinde; gerekçesi ve kaynak dökümü
`content/objections/31-arac-hayvan-carpma.md` içinde.

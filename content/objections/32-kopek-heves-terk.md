# P2 itiraz provası — 32-kopek-heves-terk

**Tarih:** 2026-09-04 · **İddia sınıfı:** C · **Yetki alanı:** TR
**Kapılar:** P0–P7 (`KANAL_REHBERI.md` §6) · **Süre:** 64,8 sn · **Seslendirme:** kullanıcı

---

## Kapı cevapları

**P0 — Bunu paylaşan kişi ne demiş oluyor?**
> "Ben bir canı, canım sıkılınca bırakmam."

Kişi hakkında bir şey söylüyor ve söylenmeye değer. Aykırı videonun ("Ben
gördüğümde susmam") aynı ailesinden: paylaşan kişi kendini "heveslenip bırakan"
değil "sözünü tutan" tarafa yazıyor.

**P1 — Alıcı kim?**
> "Bunu yeni bir hayvan almayı düşünen birine gönder."

Adı olan biri: izleyicinin çevresinde şu an yavru köpek/kedi bakan, "ben de
alsam mı" diyen biri neredeyse her zaman var. "Herkese gönder" değil.

**P6 — İlk üç saniye tipi:** ters yön. Video beklenen suçlamayı yapmıyor
("hayvana kötü davrandın") — tam tersini söylüyor: *"Onu hiç dövmedin, hiç aç
bırakmadın."* Asıl suçlama dördüncü cümlede geliyor. Savunmaya geçen izleyici
paylaşmaz; önce suçsuz çıkarılan izleyici izlemeye devam eder.

**P7 — Zarar kapısı:** Video hiçbir gecikme önermiyor ve izleyiciyi çaresiz
bırakmıyor. "Asla bırakma" demek yerine bırakmak zorunda kalana **somut
alternatif** veriyor (barınak, ilan, devir). Tavsiyenin birebir uygulanması
hayvana zarar vermiyor.

---

## En güçlü üç itiraz

### 1. "Herkes vicdansızlıktan bırakmıyor. Taşındım / alerji çıktı / param yetmedi." — EN GÜÇLÜ

Videonun hook'u sert ve doğrudan izleyiciyi suçluyor ("hayatının en kötü gününü
sen yaşattın"). Gerçekten çaresiz kaldığı için hayvanını veren biri bu cümleyi
haksız bulacak ve savunmaya geçecek — savunmaya geçen izleyici paylaşmaz.

**Video bunu içinde karşılıyor (beat 11).** İtiraz reddedilmiyor, kabul ediliyor:
*"Gerçekten elinde değilse bile sokağa bırakmak bir seçenek değil."* Yani video
"hayvanını asla devretme" demiyor — **"sokağa atma"** diyor. Ayrım videonun
tamamını taşıyan ayrım bu ve açıkça söyleniyor, üstelik yerine ne yapılacağı da
söyleniyor (barınak / ilan). Suçlanan şey çaresizlik değil, çözüm aramadan
bırakmak.

### 2. "Barınağa vermek zaten ölüme terk etmek. Türkiye'de barınak ne demek biliyor musun?"

**GERÇEKLEŞTİ — 2026-09-04.** Video yayınlandıktan sonra tepkinin geldiği yer
tam burası oldu. Türkiye'de belediye barınaklarının kamuoyundaki itibarı düşük;
"barınağa teslim et" tavsiyesi bir kesim için tavsiye değil suçlama gibi duyuldu.

**Alınan karar:** barınak tavsiyesi videodan çıkarıldı. `alternatif` beat'i
yeniden yazıldı ve yeniden seslendiriliyor:

> Gerçekten elinde değilse bile sokağa bırakmak bir seçenek değil.
> Sahiplendirme ilanı ver, yeni sahibini sen bul. Bulana kadar sorumluluk sende.

Kural olarak sabitlendi: `KANAL_REHBERI.md` §6 **P8 — Kurum kapısı**; ihlali
`scripts/source_audit.py` otomatik yakalıyor.

**Ders (bu dosyanın kendisiyle ilgili):** bu itiraz üretimden ÖNCE burada
yazılmıştı ve "videoda karşılanmıyor" notuyla geçildi. Öngörülen bir itiraz
karşılanmadan yayına çıkarsa, o itiraz yoruma dönüşüyor.

**O günkü kısmi savunma (yetersiz kaldı):** barınak tek seçenek olarak
sunulmuyordu, "Bir platformda ilan ver" cümlesi hemen ardından geliyordu.
Yorumlarda bu ayrım işe yaramadı — cümlenin ilk sırada olması yetti.

Sabitlenecek yorumda konu açıkça karşılanmalı:
sokağa bırakmakla kıyaslandığında hangisinin daha yüksek hayatta kalma şansı
verdiği, ve mümkünse önce sahiplendirme denenmesi gerektiği. İleride ayrı bir
Reel konusu: *"Hayvanını veremiyorsan sırayla ne denenir?"*

### 3. "Kimse bu cezayı almıyor ki. Kim ispatlayacak, kamera mı var?"

Kanalın tekrar eden itirazı (`DcsuTrLkc4b` altındaki 97 yorumun baskın teması:
"yasa var ama uygulanmıyor"). Video bunu **içinde karşılamıyor** — çünkü videonun
iddiası "yakalanırsın" değil, "kanun bu fiile bir isim koymuş". Yani argüman
caydırıcılık değil, meşruiyet: *terk etmek kişisel bir tercih değil, yasak bir
fiil.*

Buna rağmen yorum gelecektir. Cevabı hazır olmalı ve `29-hayvana-eziyet-
sorusturma-sarti` videosuna bağlanmalı (o video tam olarak bu itirazın cevabı).

---

## Kaynak dökümü (P3 · C sınıfı)

**Birincil kaynak — konsolide metin:**
`https://www.mevzuat.gov.tr/MevzuatMetin/1.5.5199.doc`
5199 sayılı Hayvanları Koruma Kanunu, güncel birleştirilmiş metin.
2026-09-04'te indirildi ve ilgili maddeler doğrudan okundu.

**Madde 14/1-(n) — yasak fiiller:**
> "Ev hayvanını terk etmek."

Terk yasağı bu bentte, açık ve tek cümlelik bir yasak fiil olarak duruyor.

**Madde 28 — idari para cezaları:** 14. maddeye aykırı davrananlara **hayvan
başına idari para cezası** öngörüyor. Ceza tutarları 30/7/2024 tarihli **7527
sayılı Kanun**'un 10. maddesiyle güncellendi (R.G. 02.08.2024, S. 32620).

**Madde 28/A ile ilişkisi — kapsam sınırı (P5):** m.28/A yalnızca **adli**
cezaları (hapis) düzenliyor: eziyet, cinsel saldırı, kasten öldürme. **Terk
etmek 28/A kapsamında değildir** — yani terk, hapis cezası gerektiren bir suç
değil, idari yaptırıma bağlı bir yasak fiildir. Video bu ayrımı bozmuyor:
"suç sayılmadığını düşünüyorsun, yanılıyorsun" derken hapis demiyor, **"idari
para cezası öngörüyor"** diyor.

**Sahipli/sahipsiz ayrımı (P5):** Hüküm **ev hayvanı** içindir; sahiplenilmiş
bir hayvanı sokağa bırakmayı kapsar. Videonun anlatısı zaten baştan sona
sahiplenilmiş bir hayvanı anlatıyor ("aynı gün eve getirdin"), bu yüzden kapsam
sözlü olarak ayrıca söylenmedi — anlatı kapsamı kendiliğinden kilitliyor.

**P4 — yetki alanı:** Tamamen TR. Videoda yabancı veri kullanılmıyor.

---

## P3 ek kuralı: para tutarı söylenmiyor

İdari para cezaları her yıl yeniden değerleme oranıyla artıyor. Rakam söylemek
videoyu birkaç ay içinde yanlış hâle getirir. Video **cezanın varlığından** söz
ediyor, tutarından değil. (`KANAL_REHBERI.md` §6 P3 ek kuralı.)

---

## Yapılmayanlar

- **Barınak koşulları tartışılmıyor.** Yukarıdaki 2. itiraz; ayrı bir Reel
  konusu, bu videoyu odaktan düşürür.
- **Sahiplendirme prosedürü anlatılmıyor.** "Platformda ilan ver" deniyor ama
  hangi platform, nasıl güvenli devredilir söylenmiyor — bu da ayrı bir video.
- **Kimse hedef gösterilmiyor.** Belediye, barınak ya da bir grup suçlanmıyor
  (`KANAL_REHBERI.md` §4).
- **Şiddet/gore görüntüsü yok.** En sert görsel: boşalan bir yol ve yol kenarında
  bekleyen bir köpek.

---

## Üretim notu — kayıt senaryodan üç yerde ayrıldı

Kullanıcı seslendirmesi (`adsız.wav`, 64,8 sn) whisper `small` ve `medium`
modelleriyle iki kez çözümlendi:

1. **"birine devret" söylenmedi.** Senaryodaki üç alternatiften biri kayıtta yok;
   altyazıdan da çıkarıldı. CTA "barınağa teslim et / platformda ilan ver" ile
   bitiyor.
2. **Sonu belirsiz duyulan kelimeler:** "gördüm/gördün", "durdu/durdun",
   "güvenmiştin/güvenmişti". Altyazıda dilbilgisel olarak doğru biçim yazıldı;
   fonetik fark tek bir genizsi ünsüz.
3. **"Barınağa"** iki modelde de "varınağı/varına" olarak çözümlendi — b/v
   karışması; senaryodaki doğru biçim kullanıldı.

**Süre uyarısı:** 64,8 sn. Kanalın en iyi videosu 53,5 sn ve pipeline 42 sn üstü
için uyarı basıyor. Kısaltma gerekirse en güvenli aday beat 8 ("ve büyük
ihtimalle bunun bir suç sayılmadığını düşünüyorsun. Yanılıyorsun.") — çıkarılırsa
hukuki bölüm doğrudan beat 9 ile başlar ve yaklaşık 4,5 sn kazanılır.

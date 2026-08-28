# v2 üretim hattı

2026-08-28'de kuruldu. Amaç: Reel'i "fotoğrafın üstünde metin kutusu"
olmaktan çıkarıp **gerçek video klipler + doğal Türkçe seslendirme + sese
birebir oturan kinetik altyazı** taşıyan bir videoya dönüştürmek.

## Tek komut

```bash
python scripts/build_reel.py 13-kopek-kuyruk-yonu
python scripts/make_captions_v2.py
```

Çıktı: `videos_v2/{slug}.mp4` ve `captions/reels_v2/{slug}.txt`.

Windows'ta projenin Python'u:
`"C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.2800.0_x64__qbz5n2kfra8p0\python3.12.exe"`
(Git Bash'teki `python` 3.11 ve numpy'siz — o çalışmaz.)

## Dosyalar

| Dosya | İş |
|---|---|
| `content/storyboards.json` | Senaryonun tek kaynağı: beat'ler, çekimler, arama terimleri, vurgular |
| `scripts/keys.py` | API anahtarlarının tek okuma noktası |
| `scripts/voice.py` | Seslendirme: Edge TTS (ücretsiz, varsayılan) + ölçüm; ElevenLabs isteğe bağlı |
| `scripts/footage.py` | Dikey stok video bulma/indirme/önbellekleme (Pexels → Pixabay) |
| `scripts/reel_kit_v2.py` | Render motoru: kadraj, kinetik altyazı, loop |
| `scripts/build_reel.py` | Uçtan uca: ses → klipler → görüntü → miksaj → MP4 |
| `scripts/make_captions_v2.py` | Storyboard'dan yayına hazır açıklama |

## Anahtarlar

Anahtarlar bu projede **tutulmuyor**; `Hayvan-Kanali/.env` içindeki
`EXTERNAL_ENV` satırı, anahtarların bulunduğu `.env`'i gösteriyor:

```
EXTERNAL_ENV=C:\Users\efeka\Projeler\youtube otomasyon türkçe\.env
```

Oradan okunanlar: `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`,
`PEXELS_API_KEY`, `PIXABAY_API_KEY`. Aynı sırrı iki dosyada tutmamak bilinçli
bir karar — biri iptal edildiğinde diğeri sessizce eskimesin, ve sızma
yüzeyi ikiye katlanmasın (bkz. `.env.example`'daki 2026-08-28 notu).

## Ses: ücretsiz, sevimli, senkron

**Motor: Edge TTS (ücretsiz, varsayılan).** ElevenLabs kodda duruyor ama
kapalı; `--paid-voice` bayrağıyla açılıyor. Kullanıcı kararı (2026-08-28):
ses ücretsiz olacak.

**Ses: `tr-TR-EmelNeural`.** Edge TTS'te Türkçe için yalnızca iki ses var.
Ahmet (erkek) "çok kalın ve ürkütücü" bulundu; Emel, Microsoft'un kendi
etiketiyle "Friendly, Positive" — kanalın tonuna uyan bu. Varsayılan
`rate +5%`, `pitch +4Hz` (hafif yukarı kaydırma sesi biraz daha genç ve
sıcak yapıyor; +12Hz üstü yapaylığı geri getiriyor).

**Doğallaştırma zinciri** (`VOICE_SHAPE`) sesin kalınlığını almak üzere
yeniden ayarlandı: 110 Hz altı kesiliyor, 280 Hz ("çamur") azaltılıyor,
1,9 kHz ve 4,2 kHz yükseltiliyor (sıcaklık + berraklık), ardından de-esser,
yumuşak kompresyon ve çok kısa oda yansıması. Ham TTS kuru ve "kabin
içinde" duyuluyor; kulağın yapaylık olarak okuduğu ipuçlarının büyük kısmı
telaffuzda değil bu tınıda.

**Hız düşürüldü.** İlk sürümde `+18%` idi; hızlandırılmış konuşmada tonlama
düzleşiyor ve robotik duyuluyordu.

**Kendi sesin.** Bir beat'e `voice_file` verilirse sentez atlanır ve o kayıt
kullanılır (yine kırpılır ve aynı zincirden geçer). Doğallık sorununun kesin
ve ücretsiz çözümü bu — kanala özgü tek ses de bu olur.

### Altyazı senkronu nasıl çözüldü

Şikâyet: "altyazıyla ses eş zamanlı gitmiyor." Ölçüldüğünde iki ayrı sebep
çıktı, ikisi de düzeltildi:

1. **Sessizlik payı.** Edge TTS her klibin başına 0,18-0,36 sn, sonuna
   0,6-1,0 sn sessizlik koyuyor. Motor altyazıyı bu sessizlikler dahil tüm
   dosya süresine yayıyordu: "hook" beat'inde 1,86 sn'lik konuşma 3,02 sn'ye
   yayılmıştı — altyazı hem erken başlıyor hem %38 yavaş ilerliyordu. Artık
   her klip konuşmaya kırpılıp ölçülüyor.
2. **Kart sınırları yanlış tahmin ediliyordu.** Önce karakter uzunluğuna
   göre, sonra her kartı ayrı sentezleyip ölçerek. İkisi de şaşıyor: izole
   edilmiş parça kendi başlangıç/bitiş artikülasyonunu taşıyor ve kısa
   kartlar orantısız ağırlık kazanıyor. Artık **kümülatif önek** ölçülüyor —
   ilk N kart birlikte sentezlenip süresi alınıyor, bu doğrudan o kartın
   bittiği an. İki yöntem arasında 0,26 sn'ye varan fark ölçüldü.

Doğrulama (13-kopek-kuyruk-yonu, Edge TTS, beat başlangıçları):

```
ilk kart                     gösterim    ses     fark
Köpeğin kuyruk salladı diye    0.04s    0.10s   +0.00s
Mesele sallaması değil         2.55s    2.63s   +0.02s
Sağa sallıyorsa                6.51s    6.59s   +0.02s
Sola sallıyorsa                8.61s    8.69s   +0.02s
Çünkü kaygıyı                 10.52s   10.61s   +0.02s
Trento Üniversitesi ölçtü:    14.95s   15.03s   +0.02s
Bu akşam köpeğine bak         20.16s   20.24s   +0.02s
```

En büyük sapma 0,02 sn ve hepsi pozitif: altyazı sesten birkaç kare **önce**
beliriyor. Bu kasıtlı (`CARD_LEAD = 0.06`) — göz metni okumaya kulaktan önce
başladığı için senkron algısı böyle daha iyi.

**Ölçüm önbelleklenir** (`voice_cache/measure/`), yani aynı storyboard tekrar
üretildiğinde onlarca TTS çağrısı yeniden yapılmaz.

### Kart kelimeleri VO kelimelerini bölmeli

ElevenLabs yolu açıldığında (`--paid-voice`) kart süreleri karakter bazlı
hizalamadan birebir kurulur; bunun çalışması için bir beat'in `chunks`
dizisindeki toplam kelime sayısı `vo` metnindekine **eşit** olmalı. Ücretsiz
yolda bu şart değil ama kartların VO'yu sırayla bölmesi yine de doğru
sonuç verir.

## Video klipler

`shots[].query` verilen her çekim için Pexels (yoksa Pixabay) taranıp dikey
klip indiriliyor. Klipler `footage/` altında önbellekleniyor; `footage/index.json`
hangi terimin hangi klibe çözüldüğünü tutuyor.

İki eleme, ikisi de ölçülmüş sorunlara karşı:

* **Hareket eşiği** (`MOTION_FLOOR = 1.6`). Stokta tripod üzerinde çekilmiş,
  pratikte donuk klipler çok yaygın. `motion_score()` ardışık karelerin
  ortalama farkını ölçüyor, eşiğin altı elenip sıradaki aday deneniyor.
* **Konu doğrulaması.** Ölçüldü: `"dog face close up looking at camera"`
  araması yüzü boyalı bir **insan** klibi getirdi. Artık sağlayıcının kendi
  metadata'sında (Pexels sayfa slug'ı/alt metni, Pixabay etiketleri) konu
  kelimesi (`dog`, `cat`, `kitten`…) geçmeyen aday eleniyor. Eleme sert —
  20 adaydan tipik olarak 14-19'u düşüyor — ama kalanlar konuya ait oluyor.
  `shots[].must_include` ile terimler elle verilebilir.

Klip bulunamazsa `shots[].fallback_media` (fotoğraf) devreye giriyor; bu
durumda eski Ken Burns hareketi uygulanıyor. Her çekimde `fallback_media`
tanımlı olmalı.

Tek başına arama denemek için:

```bash
python scripts/footage.py "cat stalking crouching" --min-duration 6
```

## Storyboard formatı

```jsonc
{
  "slug": "13-kopek-kuyruk-yonu",
  "source_name": "Current Biology · Trento Üniversitesi, 2013",
  "source_url": "https://...",
  "music_id": "carefree",            // content/music_library.json'daki id
  "voice": "tr-TR-EmelNeural",       // tr-TR-AhmetNeural (erkek) de var
  "rate": "+5%",
  "image_is_ai": false,
  "shots": [
    { "query": "dog wagging tail",              // stok arama terimi
      "fallback_media": "assets/x.jpg",         // klip bulunamazsa
      "must_include": ["dog"],                  // opsiyonel konu doğrulaması
      "start_at": 1.5,                          // klibin ilk saniyelerini atla
      "motion": "push_in",                      // yalnızca fotoğrafta
      "focus": [0.32, 0.30],                    // yalnızca fotoğrafta
      "crop":  [0.16, 0.22, 0.94, 1.0] }        // yalnızca fotoğrafta
  ],
  "beats": [
    { "role": "hook",                // hook | turn | payoff | mechanism | proof | cta
      "shot": 0,                     // shots dizisindeki indeks
      "vo": "Seslendirilecek cümle.",
      "chunks": ["Ekranda", "görünecek kartlar"],   // kelime sayısı vo ile eşit olmalı
      "emph": ["vurgulanacak", "kelimeler"],        // amber renk
      "y": 900, "size": 84,          // opsiyonel konum/boyut
      "speed": 1.08,                 // opsiyonel, ElevenLabs
      "pitch": "+8Hz",               // opsiyonel, Edge TTS yedeği
      "voice_file": "recordings/hook.wav",          // varsa sentez atlanır
      "pause_after": 0.24 }
  ]
}
```

## v1'e göre neler değişti ve neden

| v1 | v2 | Gerekçe |
|---|---|---|
| Tek fotoğraf, 16 sn doğrusal zoom | Gerçek video klipler, beat'lere bölünmüş çekimler | Tek kare = slayt gösterisi |
| Sessiz | Türkçe seslendirme (Edge TTS) + ducking'li müzik | Orijinal ses sinyali; sesi açık tutmak için sebep |
| Paragraf kutusu, 6 sn sabit | Ölçülmüş kinetik kartlar (sapma 0,02 sn) | Reels'te paragraf okunmaz |
| Ekranın %45'i koyu dikdörtgen | Gradyan scrim + metnin şeklini izleyen hale | Fotoğraf açıkta kalır, metin her zeminde okunur |
| Metin `y=1812–1880` | Her şey `y=300–1400` güvenli alanında | O bant Instagram arayüzünün altında kalıyordu |
| Statik son kart | Son 0,55 sn ilk kareye çapraz geçiş | Kesintisiz döngü → tekrar izleme |
| Sabit `quality=8` → 15–19 MB | `-crf 21` + hedef bit hızıyla küçültme | Sabit CRF ile küçültme gerçek videoda dosyayı BÜYÜTEBİLİYOR (ölçüldü: 28,1 → 29,5 MB) |
| Rastgele ses seviyesi | `loudnorm I=-14` | Her Reel aynı yükseklikte |

## Bilinen sınırlar

* **Türkçe Edge TTS'te iki ses var, o kadar.** Emel ve Ahmet. Daha fazla
  çeşitlilik ya ücretli bir servis ya da kendi kaydın gerektirir.
* **ElevenLabs varsayılan kapalı.** `--paid-voice` ile açılır; kotası
  `youtube otomasyon türkçe` projesiyle ORTAKTIR.
* **Stok klip, kendi çekimin değil.** Aynı klipler başka kanallarda da
  görünebilir. Kanala özgü görüntü ancak kendi çekiminle olur.
* **Konu doğrulaması sağlayıcı metadata'sına güveniyor.** Slug'ında "dog"
  geçen ama konuyla ilgisiz bir klip yine geçebilir; render sonrası gözle
  kontrol hâlâ gerekli.

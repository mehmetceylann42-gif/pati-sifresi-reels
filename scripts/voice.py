#!/usr/bin/env python3
"""Türkçe seslendirme: Edge TTS (varsayılan, ücretsiz) — ElevenLabs isteğe bağlı.

## Neden iki motor

Edge TTS ücretsiz ve her zaman çalışıyor, ama iki zayıflığı var:

1. **Doğallık.** Ham çıktı düz ve "kabin içinde" duyuluyor; yapay olduğu
   belli oluyor.
2. **Zamanlama.** Türkçe neural sesler `WordBoundary` olayı yaymıyor
   (yalnızca `SentenceBoundary`), yani altyazı kartlarının süresi ancak
   tahmin edilebiliyor.

ElevenLabs `/with-timestamps` uç noktası ikisini birden çözüyor: sesi belirgin
şekilde daha doğal, ve yanıtta **karakter bazlı hizalama** dönüyor — her
harfin kaçıncı saniyede söylendiği. Altyazı senkronu böylece tahmin değil
ölçüm oluyor.

Anahtar yoksa veya kota bittiyse Edge TTS'e düşülür; o durumda kart süreleri
`measure_chunks()` ile (her kartı ayrı sentezleyip ölçerek) tahmin edilir.

## Sessizlik kırpması

Her iki motor da klibin başına/sonuna sessizlik koyuyor (Edge TTS'te ölçülen:
baş ~0,18-0,36 sn, son ~0,6-1,0 sn). Kırpılmadan ölçülen süre konuşmanın
gerçek süresinden %30-40 uzun çıkıyor; altyazı hem erken başlıyor hem sesin
gerisinde sürükleniyordu. Artık her klip konuşmaya kırpılıp ölçülüyor.

## Kendi sesin

Bir beat'e `voice_file` verilirse sentez atlanır, o kayıt kullanılır.
"""

from __future__ import annotations

import asyncio
import base64
import json
import re
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import hashlib
import shutil

import edge_tts
import requests
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from keys import get as key_get  # noqa: E402

VOICE_MALE = "tr-TR-AhmetNeural"
VOICE_FEMALE = "tr-TR-EmelNeural"
# Edge TTS'te Türkçe için yalnızca bu iki ses var. Ahmet "çok kalın ve
# ürkütücü" bulundu (2026-08-28 kullanıcı geri bildirimi); Emel, Microsoft'un
# kendi etiketiyle "Friendly, Positive" — kedi/köpek kanalının tonuna uyan
# olan bu.
DEFAULT_VOICE = VOICE_FEMALE

# Doğal Türkçe anlatım hızı. Önceki "+18%" ayarı sesi tekdüze ve robotik
# yapıyordu — hızlandırılmış konuşmada tonlama düzleşiyor.
DEFAULT_RATE = "+5%"
# Hafif yukarı kaydırma sesi biraz daha genç/sıcak yapıyor. Daha fazlası
# (+12Hz üstü) yapaylığı geri getiriyor.
DEFAULT_PITCH = "+4Hz"

SR = 48000

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
# eleven_multilingual_v2, previous_text/next_text ("request stitching")
# destekleyen model. v3 desteklemiyor; stitching olmadan her beat bağımsız bir
# "ilk cümle" gibi okunuyor ve beat sınırları duyuluyor.
ELEVEN_MODEL = "eleven_multilingual_v2"
ELEVEN_SETTINGS = {
    "stability": 0.45,          # düşük = daha ifadeli; kısa Reels beat'leri için
    "similarity_boost": 0.85,
    "style": 0.35,              # anlatım enerjisi
    "use_speaker_boost": True,
    # ElevenLabs Türkçe'yi Edge TTS'ten belirgin şekilde yavaş okuyor. 1.08
    # süreyi ~%7 kısaltıyor ama tonlamayı bozmuyor; daha yükseği (1.2'ye doğru)
    # yeniden robotik duyulmaya başlıyor.
    "speed": 1.08,
}

# Konuşmanın gerçek başlangıç/bitişini bulmak için eşik. -45 dB, nefes ve
# yumuşak ünsüzleri (f, s, h) konuşma sayacak kadar düşük.
_TRIM = (
    "silenceremove=start_periods=1:start_silence=0.02:start_threshold=-45dB:detection=peak,"
    "areverse,"
    "silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB:detection=peak,"
    "areverse"
)

# Doğallaştırma zinciri. Amaç sesi değiştirmek değil, ham TTS çıktısının
# kuru/ince karakterini almak — kulağın "yapay" olarak okuduğu ipuçlarının
# büyük kısmı telaffuzda değil bu tınıda.
VOICE_SHAPE = (
    # 2026-08-28: önceki zincir 190 Hz'i yükseltip sesi kalınlaştırıyordu.
    # "Çok kalın ve ürkütücü" geri bildirimi üzerine yön değişti: gövde
    # yerine berraklık ve sıcaklık.
    "highpass=f=110,"                                   # kalınlık/uğultu kesildi
    "equalizer=f=280:t=q:w=1.1:g=-2.0,"                 # "çamur" bandı azaltıldı
    "equalizer=f=1900:t=q:w=1.2:g=1.2,"                 # sıcaklık/varlık
    "equalizer=f=4200:t=q:w=1.4:g=2.0,"                 # berraklık, "sevimli" tını
    "deesser=i=0.34,"                                   # berraklık artınca 's' de artar
    "acompressor=threshold=-18dB:ratio=2.2:attack=10:release=200:makeup=1.8,"
    "aecho=0.92:0.86:11|19:0.042|0.024"                 # çok kısa oda yansıması
)

_TR_LOWER = str.maketrans({"I": "ı", "İ": "i", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç"})

# Seslendirme önbelleği. İki nedeni var:
#   * ElevenLabs kotası `youtube otomasyon türkçe` projesiyle ORTAK — aynı
#     cümleyi her render'da yeniden sentezlemek boşa kredi harcıyor.
#   * `stability 0.45` çağrılar arasında kasıtlı varyans üretiyor; önbellek
#     olmadan aynı storyboard iki kez üretildiğinde süre değişiyor
#     (ölçüldü: 34,37 sn → 36,0 sn) ve render tekrarlanabilir olmuyor.
# Anahtar metni VE sesi belirleyen tüm ayarları kapsar; ayar değişirse
# önbellek kendiliğinden ıskalar.
CACHE_DIR = Path(__file__).resolve().parent.parent / "voice_cache"


def _cache_key(text: str, previous: str, following: str, speed: float | None) -> str:
    payload = json.dumps({
        "text": text, "previous": previous, "following": following,
        "model": ELEVEN_MODEL, "voice": key_get("ELEVENLABS_VOICE_ID"),
        "settings": {**ELEVEN_SETTINGS, **({"speed": speed} if speed else {})},
    }, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


@dataclass
class Word:
    text: str
    start: float
    end: float


@dataclass
class VoiceClip:
    index: int
    text: str
    path: Path
    duration: float
    engine: str = "edge"
    # Kırpılmış klibin başlangıcına göre kelime zamanları. Yalnızca ElevenLabs
    # yolunda dolu; Edge TTS'te boş kalır ve süreler tahmin edilir.
    words: list[Word] = field(default_factory=list)


# --------------------------------------------------------------------------
# ffmpeg yardımcıları
# --------------------------------------------------------------------------

def _run(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def audio_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(out.stdout)["format"]["duration"])


def trim_to_speech(src: Path, dst: Path) -> float:
    """Baştaki/sondaki sessizliği sezerek atar, mono 48k WAV yazar."""
    _run(["-i", str(src), "-af", _TRIM, "-ar", str(SR), "-ac", "1", str(dst)])
    return audio_duration(dst)


def _recorded_words(source: Path) -> list[Word]:
    """Kaydın yanındaki `<kayıt>.words.json` varsa kelime zamanlarını okur.

    Zamanlar kırpılmış klibin başlangıcına göre olmalı. Sidecar yoksa boş
    döner ve kart süreleri tahmine düşer.
    """
    sidecar = source.with_suffix(".words.json")
    if not sidecar.exists():
        return []
    data = json.loads(sidecar.read_text(encoding="utf-8"))
    return [Word(w["text"], float(w["start"]), float(w["end"])) for w in data]


def cut(src: Path, dst: Path, start: float, end: float) -> float:
    """Bilinen aralığı keser (hizalama varken sezmeye gerek yok)."""
    _run(["-i", str(src), "-ss", f"{max(start, 0):.3f}", "-to", f"{end:.3f}",
          "-ar", str(SR), "-ac", "1", str(dst)])
    return audio_duration(dst)


def shape_voice(src: Path, dst: Path) -> None:
    _run(["-i", str(src), "-af", VOICE_SHAPE, "-ar", str(SR), "-ac", "1", str(dst)])


def speakable(text: str) -> str:
    """Ekran kartını sentezlenebilir metne çevirir.

    Altyazı kartları vurgu için BÜYÜK HARF olabiliyor ("TEDİRGİN"); TTS bunu
    kısaltma sanıp harf harf okuyabilir ve ölçülen süre bozulur.
    """
    if sum(c.isupper() for c in text) > len(text) * 0.6:
        return text.translate(_TR_LOWER).lower()
    return text


# --------------------------------------------------------------------------
# ElevenLabs
# --------------------------------------------------------------------------

def eleven_available() -> bool:
    return bool(key_get("ELEVENLABS_API_KEY") and key_get("ELEVENLABS_VOICE_ID"))


def _alignment_to_words(alignment: dict, text: str) -> list[Word]:
    """Karakter bazlı hizalamayı kelime aralıklarına toplar."""
    chars = alignment.get("characters") or []
    starts = alignment.get("character_start_times_seconds") or []
    ends = alignment.get("character_end_times_seconds") or []
    if not chars or len(chars) != len(starts) or len(chars) != len(ends):
        return []
    words: list[Word] = []
    buffer, first, last = "", None, None
    for char, start, end in zip(chars, starts, ends):
        if char.isspace():
            if buffer:
                words.append(Word(buffer, first, last))
                buffer, first, last = "", None, None
            continue
        if first is None:
            first = start
        last = end
        buffer += char
    if buffer:
        words.append(Word(buffer, first, last))
    return words


def _eleven_request(text: str, previous: str, following: str,
                    speed: float | None = None) -> dict | None:
    api_key = key_get("ELEVENLABS_API_KEY")
    voice_id = key_get("ELEVENLABS_VOICE_ID")
    body: dict[str, Any] = {
        "text": text,
        "model_id": ELEVEN_MODEL,
        # Türkçe metinde varsayılan "auto" rakamları açmıyor ("135" olduğu gibi
        # kalıyor); "on" ile ElevenLabs kendi normalleştiricisini çalıştırıyor.
        "apply_text_normalization": "on",
        "voice_settings": {**ELEVEN_SETTINGS, **({"speed": speed} if speed else {})},
    }
    # Seslendirilmez, yalnızca prozodi bağlamı verir: model cümlenin bir
    # konuşmanın ortasında geçtiğini bilir ve tonlamayı ona göre kurar.
    if previous:
        body["previous_text"] = previous
    if following:
        body["next_text"] = following

    wait = 2.0
    for attempt in range(1, 4):
        try:
            response = requests.post(
                ELEVEN_URL.format(voice_id=voice_id),
                headers={"xi-api-key": api_key, "Content-Type": "application/json",
                         "Accept": "application/json"},
                json=body, timeout=90,
            )
        except requests.RequestException as error:
            print(f"      ağ hatası ({attempt}/3): {error}")
            time.sleep(wait); wait *= 2
            continue

        if response.status_code == 200:
            return response.json()
        if response.status_code in (401, 403):
            detail = response.text[:300]
            # ElevenLabs kota bitince de 401 dönüyor — "anahtar geçersiz" ile
            # "kota bitti" bambaşka iki durum, karıştırılırsa yanlış yerde aranır.
            if "quota" in detail.lower():
                remaining = re.search(r"You have ([\d,]+) credits remaining", detail)
                print(f"      ElevenLabs KOTASI BİTTİ"
                      f"{f' (kalan: {remaining.group(1)})' if remaining else ''} — Edge TTS'e düşülüyor")
            else:
                print(f"      ElevenLabs HTTP {response.status_code} (anahtar/yetki) — Edge TTS'e düşülüyor")
            return None
        if 400 <= response.status_code < 500:
            print(f"      ElevenLabs HTTP {response.status_code}: {response.text[:160]}")
            return None
        print(f"      ElevenLabs HTTP {response.status_code} ({attempt}/3)")
        time.sleep(wait); wait *= 2
    return None


def _synth_eleven(
    text: str, raw: Path, wav: Path, previous: str, following: str,
    speed: float | None = None,
) -> tuple[float, list[Word]] | None:
    key = _cache_key(text, previous, following, speed)
    cached_wav = CACHE_DIR / f"{key}.wav"
    cached_meta = CACHE_DIR / f"{key}.json"
    if cached_wav.exists() and cached_meta.exists():
        meta = json.loads(cached_meta.read_text(encoding="utf-8"))
        shutil.copyfile(cached_wav, wav)
        return meta["duration"], [Word(**w) for w in meta["words"]]

    result = _eleven_request(text, previous, following, speed)
    if result is None:
        return None
    raw.write_bytes(base64.b64decode(result["audio_base64"]))
    words = _alignment_to_words(result.get("alignment") or {}, text)
    if not words:
        # Hizalama gelmediyse sessizliği sezerek kırp; süre doğru olur ama
        # kelime zamanları olmaz.
        return trim_to_speech(raw, wav), []

    head = max(words[0].start - 0.05, 0.0)
    tail = words[-1].end + 0.08
    duration = cut(raw, wav, head, tail)
    shifted = [Word(w.text, w.start - head, w.end - head) for w in words]

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(wav, cached_wav)
    cached_meta.write_text(json.dumps({
        "text": text, "duration": duration,
        "words": [{"text": w.text, "start": w.start, "end": w.end} for w in shifted],
    }, ensure_ascii=False), encoding="utf-8")
    return duration, shifted


# --------------------------------------------------------------------------
# Edge TTS (yedek)
# --------------------------------------------------------------------------

async def _edge_stream(text: str, out_path: Path, voice: str, rate: str, pitch: str) -> None:
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    with out_path.open("wb") as handle:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                handle.write(chunk["data"])


def _synth_edge(text: str, raw: Path, wav: Path, voice: str, rate: str, pitch: str) -> float:
    asyncio.run(_edge_stream(text, raw, voice, rate, pitch))
    return trim_to_speech(raw, wav)


# --------------------------------------------------------------------------
# Genel arayüz
# --------------------------------------------------------------------------

def synth_beats(
    specs: list[dict[str, Any]],
    out_dir: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
    prefer_eleven: bool = False,
) -> list[VoiceClip]:
    """Her beat'i seslendirir (veya kaydını alır), konuşmaya kırpar, ölçer."""
    out_dir.mkdir(parents=True, exist_ok=True)
    use_eleven = prefer_eleven and eleven_available()
    clips: list[VoiceClip] = []

    for index, spec in enumerate(specs):
        wav = out_dir / f"vo_{index:02d}.wav"
        recorded = spec.get("voice_file")
        if recorded:
            source = Path(recorded)
            if not source.exists():
                raise SystemExit(f"Kayıt bulunamadı: {source}")
            clips.append(VoiceClip(index, spec["text"], wav,
                                   trim_to_speech(source, wav), engine="kayıt",
                                   words=_recorded_words(source)))
            continue

        text = spec["text"]
        raw = out_dir / f"raw_{index:02d}.mp3"
        if use_eleven:
            previous = specs[index - 1]["text"] if index > 0 else ""
            following = specs[index + 1]["text"] if index + 1 < len(specs) else ""
            result = _synth_eleven(text, raw, wav, previous, following,
                                   spec.get("speed"))
            if result is not None:
                duration, words = result
                clips.append(VoiceClip(index, text, wav, duration, "elevenlabs", words))
                continue
            use_eleven = False  # bir kez düştüyse kalan beat'lerde tekrar deneme

        duration = _synth_edge(
            text, raw, wav,
            spec.get("voice", voice), spec.get("rate", rate), spec.get("pitch", pitch),
        )
        clips.append(VoiceClip(index, text, wav, duration, "edge"))

    return clips


def measure_chunks(
    chunks: list[str],
    out_dir: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> list[float]:
    """Kart sınırlarını KÜMÜLATİF ÖNEK sentezleyerek tahmin eder.

    Neden önek: her kartı ayrı sentezleyip sürelerini toplamak yanlış çıkıyor,
    çünkü izole edilmiş her parça kendi başlangıç/bitiş artikülasyonunu taşıyor
    ve kısa kartlar orantısız ağırlık kazanıyor. İlk N kartı BİRLİKTE
    sentezleyip ölçmek, o kartın bittiği anı doğrudan verir. Ölçüldü
    (2026-08-28, "Çünkü kaygıyı / beynin sağ yarım küresi / ..." beat'i):
    iki yöntem arasında 0,26 sn'ye varan fark var.

    Dönüş: kart başına ağırlık (ardışık önek sürelerinin farkı). `build_cards`
    bunları beat'in gerçek süresine ölçekliyor.

    Ses olarak bu klipler KULLANILMAZ — yalnızca ölçüm için. Oynatılan ses,
    beat'in bütün hâlinde, doğal tonlamayla sentezlenmiş olanı.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    prefixes: list[float] = []
    for index in range(len(chunks)):
        text = " ".join(speakable(chunk) for chunk in chunks[: index + 1])
        prefixes.append(_measure_cached(text, out_dir / f"p_{index:02d}", voice, rate, pitch))

    weights: list[float] = []
    previous = 0.0
    for value in prefixes:
        # Ölçüm gürültüsü önekleri ara sıra geriye düşürebiliyor; ağırlık
        # negatif olamaz, yoksa kart sırası bozulur.
        weights.append(max(value - previous, 0.05))
        previous = max(value, previous)
    return weights


_MEASURE_CACHE = Path(__file__).resolve().parent.parent / "voice_cache" / "measure"


def _measure_cached(text: str, stem: Path, voice: str, rate: str, pitch: str) -> float:
    """Ölçüm sonucunu diske yazar — aynı storyboard tekrar üretildiğinde
    onlarca TTS çağrısı yeniden yapılmasın."""
    key = hashlib.sha256(f"{text}|{voice}|{rate}|{pitch}".encode("utf-8")).hexdigest()[:20]
    cached = _MEASURE_CACHE / f"{key}.json"
    if cached.exists():
        return json.loads(cached.read_text(encoding="utf-8"))["duration"]
    duration = _synth_edge(text, stem.with_suffix(".mp3"), stem.with_suffix(".wav"),
                           voice, rate, pitch)
    _MEASURE_CACHE.mkdir(parents=True, exist_ok=True)
    cached.write_text(json.dumps({"text": text, "duration": duration}, ensure_ascii=False),
                      encoding="utf-8")
    return duration


def concat_with_gaps(clips: list[VoiceClip], gaps: list[float], out_path: Path) -> float:
    """Klipleri aralarına sessizlik koyarak tek bir WAV'a birleştirir."""
    inputs: list[str] = []
    filters: list[str] = []
    labels: list[str] = []
    for i, clip in enumerate(clips):
        inputs += ["-i", str(clip.path)]
        filters.append(f"[{i}:a]aresample={SR},aformat=sample_fmts=s16:channel_layouts=mono[a{i}]")
        labels.append(f"[a{i}]")
        gap = gaps[i] if i < len(gaps) else 0.0
        if gap > 0.001:
            filters.append(
                f"aevalsrc=0:d={gap:.3f}:s={SR}:c=mono,"
                f"aformat=sample_fmts=s16:channel_layouts=mono[g{i}]"
            )
            labels.append(f"[g{i}]")
    graph = ";".join(filters) + ";" + "".join(labels) + f"concat=n={len(labels)}:v=0:a=1[out]"
    _run([*inputs, "-filter_complex", graph, "-map", "[out]", str(out_path)])
    return audio_duration(out_path)

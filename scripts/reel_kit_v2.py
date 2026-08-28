"""Pati Şifresi v2 render motoru — kinetik altyazı + seslendirme senkronu.

v1'den (reel_kit.py) farkları ve nedenleri:

1. Paragraf kutusu YOK. v1, 40+ kelimelik fact'i tek bir koyu kutuda 6 saniye
   ekranda tutuyordu; Reels izleyicisi bunu okumaz. v2 metni 2-3 kelimelik
   kinetik kartlara böler ve seslendirmeyle birebir senkron oynatır.
2. Metin güvenli alanda. v1'in kaynak satırı (y=1850) ve ilerleme çubuğu
   (y=1812) Instagram'ın kendi arayüzünün altında kalıyordu — pratikte
   görünmüyorlardı. v2 tüm metni y=300..1400 bandında tutar.
3. Sert kenarlı koyu dikdörtgenler yerine yumuşak gradyan scrim.
4. Beat başına kadraj değişimi + zoom punch: tek bir yavaş zoom yerine
   kesme hissi veren hareket.
5. Sonu başına bağlanır (seamless loop) — replay watch-time sinyali için.

Motor tek girdi olarak content/storyboards.json'u kullanır.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

PROJECT_ROOT = Path(__file__).resolve().parent.parent

W, H, FPS = 1080, 1920, 30

# Marka paleti
AMBER = (255, 187, 78)
WHITE = (255, 255, 255)
INK = (8, 12, 18)

# Instagram Reels arayüzünün kapattığı bölgeler dışında kalan güvenli alan.
# Sağdaki aksiyon butonları ~x>930'u, alttaki caption/ses bandı ~y>1450'yi,
# üstteki başlık ~y<260'ı yer yer kapatır.
SAFE_TOP = 300
SAFE_BOTTOM = 1400
TEXT_MAX_W = 800

BLACK_FONT = r"C:\Windows\Fonts\seguibl.ttf"   # Segoe UI Black — kanca ve altyazı
BOLD_FONT = r"C:\Windows\Fonts\segoeuib.ttf"   # Segoe UI Bold — marka/kaynak

# Kadrajın taban ölçeği: kaynak görsel bu oranda büyütülüp içinden pencere
# kırpılır, böylece zoom/pan yaparken kenar boşluğu oluşmaz.
BASE_ZOOM = 1.28


# --------------------------------------------------------------------------
# Yardımcılar
# --------------------------------------------------------------------------

def ease_out_cubic(t: float) -> float:
    return 1 - pow(1 - t, 3)


def ease_out_back(t: float, overshoot: float = 1.7) -> float:
    c3 = overshoot + 1
    return 1 + c3 * pow(t - 1, 3) + overshoot * pow(t - 1, 2)


_TR_LOWER = str.maketrans({"I": "ı", "İ": "i", "Ş": "ş", "Ğ": "ğ", "Ü": "ü", "Ö": "ö", "Ç": "ç"})


def normalize_word(word: str) -> str:
    """Vurgu eşleşmesi için kelimeyi sadeleştirir.

    Türkçe'ye özel: Python'un `casefold()`'u "İ" harfini birleşik noktalı bir
    "i̇" yapar, bu da "TEDİRGİN" ile "tedirgin"in eşleşmemesine yol açar.
    Bu yüzden önce Türkçe küçültme tablosu uygulanır.
    """
    lowered = word.translate(_TR_LOWER).lower()
    return re.sub(r"[^\wçğıöşü]", "", lowered, flags=re.UNICODE)


def chunk_text(text: str, max_words: int = 3, max_chars: int = 24) -> list[str]:
    """VO cümlesini ekranda tek seferde okunabilecek kartlara böler."""
    chunks: list[str] = []
    current: list[str] = []
    for word in text.split():
        candidate = current + [word]
        if len(candidate) > max_words or len(" ".join(candidate)) > max_chars:
            if current:
                chunks.append(" ".join(current))
                current = [word]
            else:
                chunks.append(word)
                current = []
        else:
            current = candidate
    if current:
        chunks.append(" ".join(current))
    return chunks or [text]


# --------------------------------------------------------------------------
# Metin karosu (bir kez çizilir, animasyonda yeniden ölçeklenir)
# --------------------------------------------------------------------------

@dataclass
class TextTile:
    image: Image.Image
    width: int
    height: int


def render_text_tile(
    text: str,
    size: int,
    emph: set[str],
    max_width: int = TEXT_MAX_W,
    stroke: int = 6,
) -> TextTile:
    """Metni satırlara sarıp şeffaf bir RGBA karoya çizer.

    Vurgulu kelimeler amber, diğerleri beyaz; hepsinde kalın siyah kontur —
    hangi fotoğrafın üstüne düşerse düşsün okunabilir kalması için.
    """
    font = ImageFont.truetype(BLACK_FONT, size)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    lines: list[list[str]] = []
    current: list[str] = []
    for word in text.split():
        candidate = current + [word]
        if probe.textlength(" ".join(candidate), font=font) > max_width and current:
            lines.append(current)
            current = [word]
        else:
            current = candidate
    if current:
        lines.append(current)

    space_w = probe.textlength(" ", font=font)
    line_h = int(size * 1.16)
    pad = stroke * 2 + 34  # hale bulanıklığının karo kenarında kesilmemesi için
    widths = [probe.textlength(" ".join(line), font=font) for line in lines]
    tile_w = int(max(widths)) + pad * 2
    tile_h = line_h * len(lines) + pad * 2

    tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)
    for row, line in enumerate(lines):
        x = (tile_w - widths[row]) / 2
        y = pad + row * line_h
        for word in line:
            color = AMBER if normalize_word(word) in emph else WHITE
            draw.text((x, y), word, font=font, fill=color,
                      stroke_width=stroke, stroke_fill=(0, 0, 0, 235))
            x += probe.textlength(word, font=font) + space_w

    # Metnin şeklini takip eden yumuşak koyu hale. Parlak arka planlarda
    # (çimen, kar, gökyüzü) sadece kontur yetmiyor; bu hale metni her
    # fotoğrafın üstünde okunur tutar ve kutu çizgisi bırakmaz.
    glow = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    glow.putalpha(tile.getchannel("A").filter(ImageFilter.GaussianBlur(18)).point(lambda v: min(int(v * 2.1), 190)))
    glow.alpha_composite(tile)
    return TextTile(glow, tile_w, tile_h)


def paste_tile(canvas: Image.Image, tile: TextTile, center_y: int, scale: float, alpha: float) -> None:
    if alpha <= 0.01:
        return
    if abs(scale - 1.0) > 0.002:
        new_w = max(1, int(tile.width * scale))
        new_h = max(1, int(tile.height * scale))
        image = tile.image.resize((new_w, new_h), Image.Resampling.BILINEAR)
    else:
        image = tile.image
        new_w, new_h = tile.width, tile.height
    if alpha < 0.99:
        image = image.copy()
        image.putalpha(image.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(image, ((W - new_w) // 2, center_y - new_h // 2))


# --------------------------------------------------------------------------
# Scrim / vignette (bir kez üretilir)
# --------------------------------------------------------------------------

def build_scrim() -> Image.Image:
    """Alt ve üst yumuşak karartma + hafif vignette.

    v1'deki sert kenarlı dikdörtgenlerin yerini alır: fotoğrafın üstünde
    görünür bir 'kutu çizgisi' bırakmaz ama metni okunur tutar.
    """
    gradient = np.zeros((H, W, 4), dtype=np.uint8)
    ys = np.arange(H, dtype=np.float32)

    top = np.clip((360 - ys) / 360, 0, 1) ** 1.5 * 130
    bottom = np.clip((ys - 780) / (H - 780), 0, 1) ** 1.4 * 175
    alpha = np.maximum(top, bottom)
    gradient[..., 3] = alpha[:, None].astype(np.uint8)
    gradient[..., 0:3] = np.array(INK, dtype=np.uint8)

    layer = Image.fromarray(gradient, "RGBA")

    xs = np.linspace(-1, 1, W, dtype=np.float32)[None, :]
    yy = np.linspace(-1, 1, H, dtype=np.float32)[:, None]
    radial = np.sqrt(xs ** 2 + (yy * 0.62) ** 2)
    vig = (np.clip((radial - 0.72) / 0.75, 0, 1) ** 1.7 * 120).astype(np.uint8)
    vignette = np.zeros((H, W, 4), dtype=np.uint8)
    vignette[..., 3] = vig
    layer.alpha_composite(Image.fromarray(vignette, "RGBA"))
    return layer


# --------------------------------------------------------------------------
# Zaman çizelgesi
# --------------------------------------------------------------------------

@dataclass
class Card:
    text: str
    start: float
    end: float
    size: int
    center_y: int
    emph: set[str] = field(default_factory=set)
    tile: TextTile | None = None


@dataclass
class Shot:
    media: Path
    start: float
    end: float
    motion: str = "push_in"
    # Video çekimlerde ffmpeg ile 1080x1920/30fps'e hazırlanmış klibin yolu.
    # Doluysa hareket kaynağı klibin kendisidir; Ken Burns uygulanmaz.
    clip_path: Path | None = None
    # `focus`, kaynak fotoğrafın hangi bölgesinin dikey kadraja alınacağını
    # belirler (0,0 = sol üst, 1,1 = sağ alt). Yatay bir fotoğrafta hayvanın
    # yüzü solda kaldığında (0.5, ...) merkez kırpması yüzü keser — bu yüzden
    # her çekim kendi odağını taşır.
    focus: tuple[float, float] = (0.5, 0.42)
    crop: tuple[float, float, float, float] | None = None
    base: Image.Image | None = None


# Altyazı, sesin birkaç kare öncesinde belirdiğinde senkron algısı daha
# iyi olur — göz metni okumaya kulaktan önce başlar. Altyazı standartlarında
# yerleşik bir pratik.
CARD_LEAD = 0.06


def beat_chunks(beat: dict[str, Any]) -> list[str]:
    is_hook = beat.get("role") == "hook"
    text = beat.get("caption", beat["vo"])
    return beat.get("chunks") or chunk_text(text, max_words=4 if is_hook else 3)


def _card(beat: dict[str, Any], text: str, start: float, end: float, emph: set[str]) -> Card:
    is_hook = beat.get("role") == "hook"
    return Card(
        text=text,
        start=max(start - CARD_LEAD, 0.0),
        end=end,
        size=beat.get("size", 82 if is_hook else 76),
        center_y=beat.get("y", 780 if is_hook else 1130),
        emph=emph,
    )


def cards_from_alignment(
    beat: dict[str, Any], start: float, words: list[Any], emph: set[str]
) -> list[Card] | None:
    """Kart sürelerini ElevenLabs'in kelime zamanlarından birebir kurar.

    Kartların kelimeleri, seslendirilen metnin kelimelerini sırayla bölmek
    zorunda. Bölmüyorsa (kart metni VO'dan farklı yazılmışsa) None döner ve
    çağıran tahmine düşer — sessizce yanlış hizalamak yerine.
    """
    pieces = beat_chunks(beat)
    counts = [len(piece.split()) for piece in pieces]
    if sum(counts) != len(words):
        return None

    cards: list[Card] = []
    cursor = 0
    for piece, count in zip(pieces, counts):
        span = words[cursor:cursor + count]
        cards.append(_card(beat, piece, start + span[0].start, start + span[-1].end, emph))
        cursor += count
    # Kartlar arasında boşluk kalmasın: her kart bir sonraki başlayana kadar
    # ekranda kalsın — kelimeler arası duraklarda ekran boşalmasın diye.
    for current, following in zip(cards, cards[1:]):
        current.end = max(current.end, following.start + CARD_LEAD)
    return cards


def build_cards(
    beats: list[dict[str, Any]],
    starts: list[float],
    durations: list[float],
    weights: list[list[float]] | None = None,
    word_times: list[list[Any]] | None = None,
) -> list[Card]:
    """Beat'in konuşma süresini altyazı kartlarına paylaştırır.

    `weights` verilirse (her kartın ayrı sentezlenip ölçülmüş süresi) o
    kullanılır; verilmezse karakter uzunluğuna düşer. Ölçülmüş ağırlık,
    virgül/iki nokta taşıyan parçalarda belirgin şekilde daha isabetli.
    """
    cards: list[Card] = []
    for index, (beat, start, duration) in enumerate(zip(beats, starts, durations)):
        emph = {normalize_word(w) for w in beat.get("emph", [])}
        words = word_times[index] if word_times else None
        if words:
            aligned = cards_from_alignment(beat, start, words, emph)
            if aligned:
                cards.extend(aligned)
                continue

        pieces = beat_chunks(beat)
        share = (weights[index] if weights else None) or [float(max(len(p), 6)) for p in pieces]
        total = sum(share) or 1.0
        cursor = start
        for piece, weight in zip(pieces, share):
            span = duration * weight / total
            cards.append(_card(beat, piece, cursor, cursor + span, emph))
            cursor += span
    return cards


def load_shot_base(
    path: Path,
    focus: tuple[float, float] = (0.5, 0.45),
    crop: tuple[float, float, float, float] | None = None,
) -> Image.Image:
    """Kaynak fotoğrafı, odak bölgesini koruyarak dikey tabana oturtur.

    `crop` verilirse (kaynak genişlik/yüksekliğin 0-1 oranı olarak
    x0,y0,x1,y1) fotoğraf önce o bölgeye kırpılır. Tek fotoğraftan
    "geniş plan / yakın plan" iki ayrı çekim çıkarmayı sağlar — asset
    kütüphanesi darken görsel çeşitliliği yaratmanın en ucuz yolu.
    """
    source = Image.open(path).convert("RGB")
    if crop:
        w, h = source.size
        source = source.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    return ImageOps.fit(
        source, (int(W * BASE_ZOOM), int(H * BASE_ZOOM)),
        Image.Resampling.LANCZOS, centering=focus,
    )


def crop_window(base: Image.Image, zoom: float, pan: tuple[float, float]) -> Image.Image:
    """Taban görselden verilen zoom ve pan konumunda bir pencere kırpar.

    `pan` (0.5, 0.5) tabanın merkezidir; taban zaten çekimin odağına göre
    kırpıldığı için varsayılan merkezdir.
    """
    zoom = min(max(zoom, 1.0), BASE_ZOOM)
    cw = int(W * BASE_ZOOM / zoom)
    ch = int(H * BASE_ZOOM / zoom)
    max_x = max(base.width - cw, 0)
    max_y = max(base.height - ch, 0)
    left = int(np.clip(pan[0] * base.width - cw / 2, 0, max_x))
    top = int(np.clip(pan[1] * base.height - ch / 2, 0, max_y))
    window = base.crop((left, top, left + cw, top + ch))
    if window.size != (W, H):
        window = window.resize((W, H), Image.Resampling.BILINEAR)
    return window


def shot_frame(shot: Shot, elapsed: float) -> Image.Image:
    span = max(shot.end - shot.start, 0.001)
    progress = min(max((elapsed - shot.start) / span, 0.0), 1.0)

    # Kesme hissi: her çekimin ilk 0.22 saniyesinde kısa bir zoom punch.
    punch_t = min(max((elapsed - shot.start) / 0.22, 0.0), 1.0)
    punch = (1 - ease_out_cubic(punch_t)) * 0.045

    if shot.motion == "pull_out":
        zoom = 1.0 + 0.20 * (1 - ease_out_cubic(progress))
    elif shot.motion == "hold":
        zoom = 1.06
    else:  # push_in
        zoom = 1.0 + 0.18 * ease_out_cubic(progress)

    pan = (0.5, 0.5)
    if shot.motion == "pan_right":
        pan = (0.34 + 0.32 * progress, 0.5)
        zoom = 1.14
    elif shot.motion == "pan_left":
        pan = (0.66 - 0.32 * progress, 0.5)
        zoom = 1.14

    return crop_window(shot.base, zoom + punch, pan)


def draw_chrome(canvas: Image.Image, source_name: str, elapsed: float, total: float) -> None:
    """Marka etiketi + kaynak künyesi — ikisi de güvenli alanda."""
    draw = ImageDraw.Draw(canvas)
    brand_font = ImageFont.truetype(BLACK_FONT, 34)
    source_font = ImageFont.truetype(BOLD_FONT, 24)

    draw.text((84, 96), "PATI ŞİFRESİ", font=brand_font, fill=AMBER,
              stroke_width=4, stroke_fill=(0, 0, 0, 200))
    draw.rounded_rectangle((84, 148, 300, 155), radius=4, fill=(*AMBER, 235))

    label = f"Kaynak: {source_name}"
    while draw.textlength(label, font=source_font) > 720 and "(" in label:
        label = label[: label.rindex("(")].strip()
    draw.text((84, 176), label, font=source_font, fill=(226, 236, 244),
              stroke_width=3, stroke_fill=(0, 0, 0, 190))


class _ClipReader:
    """Hazırlanmış çekim klibinden sırayla kare verir.

    Klip zaten 1080x1920/30fps ve çekim süresine kesilmiş olarak geliyor, bu
    yüzden kare kare okumak yeterli; kare biterse son kare dondurulur (yuvarlama
    farkından doğan 1-2 karelik açığı kapatmak için).
    """

    def __init__(self, path: Path) -> None:
        self._reader = imageio.get_reader(path)
        self._iterator = iter(self._reader)
        self._last: Image.Image | None = None

    def next_frame(self) -> Image.Image:
        try:
            self._last = Image.fromarray(next(self._iterator))
        except StopIteration:
            if self._last is None:
                raise
        return self._last

    def close(self) -> None:
        self._reader.close()


def render_timeline(
    shots: list[Shot],
    cards: list[Card],
    source_name: str,
    total: float,
    writer,
    loop_tail: float = 0.55,
) -> None:
    scrim = build_scrim()
    for card in cards:
        card.tile = render_text_tile(card.text, card.size, card.emph)

    readers: dict[int, _ClipReader] = {}
    first_frame: Image.Image | None = None
    frame_count = int(round(total * FPS))
    for number in range(frame_count):
        elapsed = number / FPS
        index, shot = next(
            ((i, s) for i, s in enumerate(shots) if s.start <= elapsed < s.end),
            (len(shots) - 1, shots[-1]),
        )
        if shot.clip_path is not None:
            if index not in readers:
                readers[index] = _ClipReader(shot.clip_path)
            canvas = readers[index].next_frame().convert("RGBA")
        else:
            canvas = shot_frame(shot, elapsed).convert("RGBA")
        canvas.alpha_composite(scrim)

        for card in cards:
            if not (card.start - 0.02 <= elapsed < card.end):
                continue
            age = elapsed - card.start
            life = card.end - card.start
            if age < 0.13:
                t = max(age, 0) / 0.13
                scale = 0.82 + 0.18 * ease_out_back(t)
                alpha = min(t * 1.8, 1.0)
            elif age > life - 0.09:
                t = (life - age) / 0.09
                scale = 0.97 + 0.03 * t
                alpha = max(t, 0.0)
            else:
                scale, alpha = 1.0, 1.0
            paste_tile(canvas, card.tile, card.center_y, scale, alpha)

        draw_chrome(canvas, source_name, elapsed, total)
        frame = canvas.convert("RGB")

        if first_frame is None:
            first_frame = frame.copy()
        # Sonu başa bağla: son yarım saniyede ilk kareye çapraz geçiş yapılır,
        # video döngüye girdiğinde kesme görünmez ve replay süresi artar.
        remaining = total - elapsed
        if remaining < loop_tail:
            mix = 1 - remaining / loop_tail
            frame = Image.blend(frame, first_frame, min(mix, 1.0) * 0.92)

        writer.append_data(np.asarray(frame))

    for reader in readers.values():
        reader.close()

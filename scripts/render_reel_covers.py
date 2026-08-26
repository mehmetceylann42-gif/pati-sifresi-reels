"""Create branded 9:16 Instagram Reel cover images from project source visuals."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "covers"
W, H = 1080, 1920
BOLD = Path("C:/Windows/Fonts/segoeuib.ttf")
REGULAR = Path("C:/Windows/Fonts/segoeui.ttf")

ITEMS = [
    ("07-kedi-tatli-tadi", "07-kedi-tatli-tadi.png", "Kediler tatlı tadını algılar mı?"),
    ("08-kedi-dili", "08-kedi-dili.png", "Kedi dili neden zımpara gibi?"),
    ("09-kedi-uykusu", "09-kedi-uykusu.png", "Kediler günde 14 saat uyur mu?"),
    ("10-kopek-burun-izi", "10-kopek-burun-izi.png", "Her köpeğin burun izi farklı mı?"),
    ("11-kopek-renk-gorusu", "11-kopek-renk-gorusu.png", "Köpekler dünyayı siyah-beyaz mı görür?"),
    ("12-kedi-mirilti-sifasi", "12-kedi-mirilti-sifasi.jpg", "Kedi mırıltısı kemikleri iyileştirebilir mi?"),
]


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    result: list[str] = []
    line: list[str] = []
    for word in text.split():
        candidate = " ".join(line + [word])
        if draw.textbbox((0, 0), candidate, font=font)[2] <= width:
            line.append(word)
        else:
            result.append(" ".join(line))
            line = [word]
    if line:
        result.append(" ".join(line))
    return result


def render(slug: str, image_name: str, title: str) -> None:
    with Image.open(ASSETS / image_name) as source:
        base = ImageOps.fit(source.convert("RGB"), (W, H), Image.Resampling.LANCZOS, centering=(0.5, 0.5)).convert("RGBA")

    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shade_draw = ImageDraw.Draw(shade)
    for y in range(H):
        top_alpha = int(132 * max(0, 1 - y / 780))
        bottom_alpha = int(172 * max(0, (y - 980) / 940))
        shade_draw.line((0, y, W, y), fill=(2, 15, 25, max(top_alpha, bottom_alpha)))
    image = Image.alpha_composite(base, shade)
    draw = ImageDraw.Draw(image)
    brand = ImageFont.truetype(str(BOLD), 36)
    eyebrow = ImageFont.truetype(str(BOLD), 28)
    title_font = ImageFont.truetype(str(BOLD), 72)
    footer = ImageFont.truetype(str(REGULAR), 28)
    amber = (255, 187, 78, 255)

    draw.rounded_rectangle((64, 68, 370, 126), radius=29, fill=(3, 24, 35, 180), outline=(255, 255, 255, 65), width=2)
    draw.text((92, 79), "PATI ŞİFRESİ", font=brand, fill=(255, 255, 255, 255))
    draw.rectangle((64, 162, 286, 170), fill=amber)

    draw.rounded_rectangle((64, 680, 1016, 1080), radius=34, fill=(3, 21, 31, 205))
    draw.text((106, 730), "HAYVANLAR DÜNYASI", font=eyebrow, fill=amber)
    lines = wrap(draw, title, title_font, 800)
    y = 790
    for line in lines:
        line_width = draw.textbbox((0, 0), line, font=title_font)[2]
        draw.text(((W - line_width) // 2, y), line, font=title_font, fill=(255, 255, 255, 255), stroke_width=1, stroke_fill=(0, 0, 0, 110))
        y += 88

    draw.text((64, 1780), "KAYDET • PAYLAŞ • TAKİP ET", font=footer, fill=(255, 255, 255, 230))
    image.convert("RGB").save(OUTPUT / f"{slug}.jpg", quality=95, subsampling=0)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for item in ITEMS:
        render(*item)
    print(f"{len(ITEMS)} kapak oluşturuldu: {OUTPUT}")


if __name__ == "__main__":
    main()

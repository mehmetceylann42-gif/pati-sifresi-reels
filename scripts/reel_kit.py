"""Shared Reel-rendering engine for Pati Şifresi.

Consolidates what used to be three near-identical scripts
(render_silent_reel.py, render_reel_batch.py, render_pet_reels.py) into one
engine driven by content/reel_specs.json. Kept as a library (not a CLI) so
render_reels.py stays a thin wrapper.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

PROJECT_ROOT = Path(__file__).resolve().parent.parent

W, H, FPS = 1080, 1920, 30
DEFAULT_DURATION = 16
BRAND = "PATI ŞİFRESİ"
AMBER = (255, 187, 78)
WHITE = (255, 255, 255)

BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
REGULAR = r"C:\Windows\Fonts\segoeui.ttf"


def resolve_image(item: dict[str, Any], specs_path: Path) -> Path:
    """Resolve an item's image path relative to the project root.

    Falls back to resolving relative to the specs file itself, so both
    "assets/x.png" (preferred) and legacy absolute paths keep working.
    """
    raw = Path(item["image"])
    if raw.is_absolute():
        return raw
    candidate = PROJECT_ROOT / raw
    if candidate.exists():
        return candidate
    return specs_path.resolve().parent / raw


def _wrap_and_draw_box(draw: ImageDraw.ImageDraw, content: str, y: int, font_file: str, size: int, amber: bool = False) -> None:
    font = ImageFont.truetype(font_file, size)
    lines: list[str] = []
    current = ""
    for word in content.split():
        proposal = f"{current} {word}".strip()
        if draw.textbbox((0, 0), proposal, font=font)[2] < 880:
            current = proposal
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    heights = [draw.textbbox((0, 0), line, font=font)[3] for line in lines]
    total = sum(heights) + 14 * (len(lines) - 1)
    draw.rounded_rectangle((72, y - 28, 1008, y + total + 28), radius=24, fill=(0, 15, 26, 210))
    color = AMBER if amber else WHITE
    for line, height in zip(lines, heights):
        line_width = draw.textbbox((0, 0), line, font=font)[2]
        draw.text(((W - line_width) // 2, y), line, font=font, fill=color, stroke_width=1, stroke_fill=(0, 0, 0))
        y += height + 14


def compose_frame(photo: Image.Image, elapsed: float, duration: int, item: dict[str, Any]) -> Image.Image:
    canvas = photo.convert("RGBA")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, 0, W, 860), fill=(0, 10, 18, 105))
    draw.rectangle((0, 1670, W, H), fill=(0, 10, 18, 155))
    label = ImageFont.truetype(BOLD, 30)
    draw.text((72, 72), BRAND, font=label, fill=AMBER)
    draw.rectangle((72, 125, 320, 133), fill=AMBER)

    t1 = duration * 3 / 16
    t2 = duration * 5.5 / 16
    t3 = duration * 11.5 / 16
    t4 = duration * 14 / 16

    if elapsed < t1:
        _wrap_and_draw_box(draw, item["title"], 265, BOLD, 60)
    elif elapsed < t2:
        _wrap_and_draw_box(draw, item["question"], 265, BOLD, 58)
    elif elapsed < t3:
        _wrap_and_draw_box(draw, item["answer"], 265, BOLD, 62, True)
        _wrap_and_draw_box(draw, item["fact"], 505, REGULAR, 42)
    elif elapsed < t4:
        _wrap_and_draw_box(draw, "Bunu daha önce biliyor muydun?", 265, BOLD, 56)
    else:
        _wrap_and_draw_box(draw, "Kaydet · paylaş · takip et", 265, BOLD, 56, True)

    draw.rounded_rectangle((72, 1812, 1008, 1824), radius=6, fill=(255, 255, 255, 75))
    draw.rounded_rectangle((72, 1812, 72 + int(936 * elapsed / duration), 1824), radius=6, fill=(*AMBER, 255))
    draw.text((72, 1850), f"Kaynak: {item['source_name']}", font=label, fill=(235, 245, 248))
    return Image.alpha_composite(canvas, overlay).convert("RGB")


def render_item(item: dict[str, Any], image_path: Path, out_dir: Path) -> Path:
    duration = int(item.get("duration", DEFAULT_DURATION))
    output = out_dir / f"{item['slug']}.mp4"
    source = Image.open(image_path).convert("RGB")
    with imageio.get_writer(output, fps=FPS, codec="libx264", quality=8, macro_block_size=1) as writer:
        total_frames = FPS * duration
        for number in range(total_frames):
            amount = 1 + 0.06 * number / (total_frames - 1)
            base = ImageOps.fit(source, (W, H), Image.Resampling.LANCZOS, centering=(0.5, 0.48))
            moved = base.resize((int(W * amount), int(H * amount)), Image.Resampling.LANCZOS)
            left, top = (moved.width - W) // 2, (moved.height - H) // 2
            cropped = moved.crop((left, top, left + W, top + H))
            frame = compose_frame(cropped, number / FPS, duration, item)
            writer.append_data(np.asarray(frame))
    return output


def load_specs(specs_path: Path) -> list[dict[str, Any]]:
    return json.loads(specs_path.read_text(encoding="utf-8"))

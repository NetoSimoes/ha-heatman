"""Generate Heatman brand icons for Home Assistant / HACS."""

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "custom_components" / "heatman" / "brand"

NAVY = (15, 42, 58, 255)
AMBER = (242, 140, 40, 255)
CREAM = (255, 236, 210, 255)


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius: int, fill) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = int(size * 0.04)
    rounded_rect(draw, (pad, pad, size - pad - 1, size - pad - 1), int(size * 0.18), NAVY)

    # Heat-pump body
    body_l = int(size * 0.28)
    body_t = int(size * 0.42)
    body_r = int(size * 0.72)
    body_b = int(size * 0.78)
    rounded_rect(draw, (body_l, body_t, body_r, body_b), int(size * 0.06), CREAM)

    # Grill lines
    grill_l = int(size * 0.34)
    grill_r = int(size * 0.66)
    for i in range(4):
        y = int(size * (0.50 + i * 0.055))
        draw.line((grill_l, y, grill_r, y), fill=NAVY, width=max(2, size // 64))

    # Heat waves above the unit
    cx = size // 2
    for i, (w, a) in enumerate(((0.16, 255), (0.22, 200), (0.28, 140))):
        y0 = int(size * (0.36 - i * 0.07))
        x0 = int(cx - size * w)
        x1 = int(cx + size * w)
        color = (*AMBER[:3], a)
        draw.arc((x0, y0 - int(size * 0.06), x1, y0 + int(size * 0.08)), 200, 340, fill=color, width=max(3, size // 28))

    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    draw_icon(256).save(OUT / "icon.png", "PNG")
    draw_icon(512).save(OUT / "icon@2x.png", "PNG")
    print(f"Wrote {OUT / 'icon.png'} and {OUT / 'icon@2x.png'}")


if __name__ == "__main__":
    main()

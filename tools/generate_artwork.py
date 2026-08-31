"""Generate aligned vector and 300 dpi sticker artwork."""

from pathlib import Path
import sys

from PIL import Image, ImageDraw

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_spec import LABEL, PANEL_FEATURES


MM_TO_PX = LABEL["dpi"] / 25.4
PALETTE = {
    "background": "#FFF4D6",
    "ink": "#27364B",
    "red": "#F4A6A6",
    "yellow": "#F5D76E",
    "orange": "#F3AA63",
    "blue": "#8FD2ED",
    "mint": "#9EDDBB",
    "purple": "#C5B2E8",
    "cut": "#FFFFFF",
}


def px(mm):
    return round(mm * MM_TO_PX)


def svg_circle(cx, cy, radius, **attrs):
    rendered = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return f'<circle cx="{cx}" cy="{cy}" r="{radius}" {rendered}/>'


def cutout_svg(feature):
    x = feature["x"] + LABEL["bleed"]
    y = feature["y"] + LABEL["bleed"]
    common = 'fill="#FFFFFF" stroke="#27364B" stroke-width="0.45" stroke-dasharray="1.5 1.5"'
    if feature["kind"] == "rect":
        return (
            f'<rect x="{x - feature["width"] / 2}" y="{y - feature["height"] / 2}" '
            f'width="{feature["width"]}" height="{feature["height"]}" rx="1" {common}/>'
        )
    if feature["kind"] == "pattern":
        holes = [svg_circle(x, y, 1.5, fill="#FFFFFF", stroke="#27364B", stroke_width="0.35")]
        for angle in range(0, 360, 60):
            import math
            hx = x + 6.2 * math.cos(math.radians(angle))
            hy = y + 6.2 * math.sin(math.radians(angle))
            holes.append(svg_circle(hx, hy, 1.5, fill="#FFFFFF", stroke="#27364B", stroke_width="0.35"))
        return "".join(holes)
    return svg_circle(x, y, feature["radius"], fill="#FFFFFF", stroke="#27364B", stroke_width="0.45", stroke_dasharray="1.5 1.5")


def generate_svg():
    panels = [
        (15, 8, 54, 72, PALETTE["red"]),
        (75, 8, 54, 72, PALETTE["yellow"]),
        (135, 8, 54, 72, PALETTE["orange"]),
        (15, 87, 54, 67, PALETTE["blue"]),
        (75, 87, 54, 67, PALETTE["mint"]),
        (135, 87, 54, 67, PALETTE["purple"]),
    ]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="204mm" height="164mm" viewBox="0 0 204 164">',
        f'<rect width="204" height="164" rx="15" fill="{PALETTE["background"]}"/>',
    ]
    for x, y, width, height, color in panels:
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{color}"/>')

    # Light rays, power, brightness, and sound icons are simple child-readable geometry.
    for center_x in (42, 102, 162):
        for dx in (-9, -5, 5, 9):
            parts.append(f'<path d="M {center_x + dx} 14 L {center_x + dx * 0.72} 19" stroke="{PALETTE["ink"]}" stroke-width="1.3" stroke-linecap="round"/>')
    parts.extend([
        f'<path d="M 42 92 v 7 M 35 96 a 9 9 0 1 0 14 0" fill="none" stroke="{PALETTE["ink"]}" stroke-width="1.7" stroke-linecap="round"/>',
        f'<path d="M 88 139 A 17 17 0 0 1 116 139" fill="none" stroke="{PALETTE["ink"]}" stroke-width="1.5"/>',
        f'<path d="M 102 141 L 111 135" stroke="{PALETTE["ink"]}" stroke-width="1.8" stroke-linecap="round"/>',
        f'<path d="M 174 96 q 8 6 0 12 M 178 92 q 13 10 0 20" fill="none" stroke="{PALETTE["ink"]}" stroke-width="1.5" stroke-linecap="round"/>',
    ])
    parts.extend(cutout_svg(feature) for feature in PANEL_FEATURES)
    parts.append('<rect id="trim-line" x="2" y="2" width="200" height="160" rx="14" fill="none" stroke="#D84A4A" stroke-width="0.3" stroke-dasharray="2 1"/>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def mm_box(box):
    return tuple(px(value) for value in box)


def draw_dashed_ellipse(draw, box, fill, width=4):
    for start in range(0, 360, 24):
        draw.arc(box, start=start, end=start + 13, fill=fill, width=width)


def draw_preview():
    image = Image.new("RGB", (px(LABEL["width"]), px(LABEL["height"])), PALETTE["background"])
    draw = ImageDraw.Draw(image)
    panels = [
        (15, 8, 69, 80, PALETTE["red"]),
        (75, 8, 129, 80, PALETTE["yellow"]),
        (135, 8, 189, 80, PALETTE["orange"]),
        (15, 87, 69, 154, PALETTE["blue"]),
        (75, 87, 129, 154, PALETTE["mint"]),
        (135, 87, 189, 154, PALETTE["purple"]),
    ]
    for x1, y1, x2, y2, color in panels:
        draw.rounded_rectangle(mm_box((x1, y1, x2, y2)), radius=px(12), fill=color)

    ink = PALETTE["ink"]
    for center_x in (42, 102, 162):
        for dx in (-9, -5, 5, 9):
            draw.line(
                mm_box((center_x + dx, 14, center_x + dx * 0.72, 19)),
                fill=ink,
                width=px(1.3),
            )
    draw.line(mm_box((42, 90, 42, 96)), fill=ink, width=px(1.7))
    draw.arc(mm_box((33, 92, 51, 110)), start=315, end=225, fill=ink, width=px(1.7))
    draw.arc(mm_box((85, 121, 119, 151)), start=200, end=340, fill=ink, width=px(1.5))
    draw.line(mm_box((102, 141, 111, 135)), fill=ink, width=px(1.8))
    draw.arc(mm_box((166, 94, 182, 110)), start=290, end=70, fill=ink, width=px(1.5))
    draw.arc(mm_box((168, 90, 190, 114)), start=290, end=70, fill=ink, width=px(1.5))

    bleed = LABEL["bleed"]
    for feature in PANEL_FEATURES:
        cx, cy = feature["x"] + bleed, feature["y"] + bleed
        if feature["kind"] == "rect":
            half_w, half_h = feature["width"] / 2, feature["height"] / 2
            box = mm_box((cx - half_w, cy - half_h, cx + half_w, cy + half_h))
            draw.rounded_rectangle(box, radius=px(1), fill=PALETTE["cut"], outline=PALETTE["ink"], width=4)
        elif feature["kind"] == "pattern":
            import math
            centers = [(cx, cy)] + [
                (cx + 6.2 * math.cos(math.radians(angle)), cy + 6.2 * math.sin(math.radians(angle)))
                for angle in range(0, 360, 60)
            ]
            for hx, hy in centers:
                box = mm_box((hx - 1.5, hy - 1.5, hx + 1.5, hy + 1.5))
                draw.ellipse(box, fill=PALETTE["cut"], outline=PALETTE["ink"], width=3)
        else:
            radius = feature["radius"]
            box = mm_box((cx - radius, cy - radius, cx + radius, cy + radius))
            draw.ellipse(box, fill=PALETTE["cut"])
            draw_dashed_ellipse(draw, box, PALETTE["ink"])

    trim = mm_box((2, 2, 202, 162))
    draw.rounded_rectangle(trim, radius=px(14), outline="#D84A4A", width=3)
    return image


def generate_a4_pdf(label):
    page = Image.new("RGB", (px(210), px(297)), "white")
    left = round((page.width - label.width) / 2)
    top = px(12)
    page.paste(label, (left, top))
    draw = ImageDraw.Draw(page)
    square_left, square_top = px(15), px(205)
    draw.rectangle(
        (square_left, square_top, square_left + px(20), square_top + px(20)),
        outline="black",
        width=3,
    )
    draw.text((square_left + px(24), square_top + px(6)), "20 mm KONTROL KARESI", fill="black")
    return page


def main():
    output = Path("artwork")
    output.mkdir(parents=True, exist_ok=True)
    (output / "activity-box-label.svg").write_text(generate_svg(), encoding="utf-8")
    preview = draw_preview()
    preview.save(output / "activity-box-label-preview.png", dpi=(LABEL["dpi"], LABEL["dpi"]))
    generate_a4_pdf(preview).save(
        output / "activity-box-label-a4.pdf", "PDF", resolution=float(LABEL["dpi"])
    )
    print("wrote sticker SVG, PNG, and A4 PDF")


if __name__ == "__main__":
    main()

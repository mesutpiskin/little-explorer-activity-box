"""Generate an annotated guide for the component fit-test coupon."""

from math import cos, radians, sin
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_spec import FIT_TEST


DPI = 300
MM_TO_PX = DPI / 25.4
CANVAS = (240, 130)
PLATE_ORIGIN = (20, 34)
COLORS = {
    "background": "#FFF9E9",
    "plate": "#E9EEF3",
    "ink": "#263548",
    "muted": "#64748B",
    "hole": "#FFFFFF",
    "led": "#E85D68",
    "dc184": "#E5B82E",
    "dc180": "#43A86B",
    "dc131a": "#4B9AD1",
    "buzzer": "#8A6BC2",
    "pot": "#E68C3A",
    "shaft": "#A56F45",
    "dc120": "#2D9C95",
    "dial": "#5C78C7",
}


def px(mm):
    return round(mm * MM_TO_PX)


def svg_y(model_y):
    return PLATE_ORIGIN[1] + FIT_TEST["size"][1] - model_y


def svg_circle(cx, cy, diameter, color, text_value=None, css_class=None):
    class_attr = f' class="{css_class}"' if css_class else ""
    parts = [
        f'<circle{class_attr} cx="{cx}" cy="{cy}" r="{diameter / 2}" '
        f'fill="{COLORS["hole"]}" stroke="{color}" stroke-width="0.8"/>'
    ]
    if text_value:
        parts.append(
            f'<text x="{cx}" y="{cy + 0.8}" text-anchor="middle" '
            f'class="size">{text_value}</text>'
        )
    return "".join(parts)


def decimal(value):
    return f"{value:.1f}".replace(".", ",")


def group_label(x, y, text_value, color, target_y):
    return (
        f'<path d="M{x} {y + 2} V{target_y}" stroke="{color}" '
        'stroke-width="0.6" stroke-dasharray="1.5 1"/>'
        f'<text x="{x}" y="{y}" text-anchor="middle" class="group" '
        f'fill="{color}">{text_value}</text>'
    )


def generate_svg():
    plate_x, plate_y = PLATE_ORIGIN
    plate_w, plate_h = FIT_TEST["size"]
    top_y = svg_y(FIT_TEST["top_y"])
    bottom_y = svg_y(FIT_TEST["bottom_y"])
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="240mm" height="130mm" viewBox="0 0 240 130">',
        '<style>text{font-family:Arial,sans-serif;fill:#263548}.title{font-size:6px;font-weight:bold}.subtitle{font-size:3px}.group{font-size:3.2px;font-weight:bold}.size{font-size:2.25px;font-weight:bold}.note{font-size:2.55px}</style>',
        f'<rect width="240" height="130" fill="{COLORS["background"]}"/>',
        '<text x="120" y="8" text-anchor="middle" class="title">KOMPONENT UYUM TESTİ KILAVUZU</text>',
        '<text x="120" y="15" text-anchor="middle" class="subtitle">MODEL: 200 × 76 mm · Soldaki seçenek daha sıkı, sağdaki daha rahattır</text>',
        f'<rect id="coupon-outline" x="{plate_x}" y="{plate_y}" width="{plate_w}" height="{plate_h}" rx="{FIT_TEST["corner_radius"]}" fill="{COLORS["plate"]}" stroke="{COLORS["ink"]}" stroke-width="0.8"/>',
        '<text x="23" y="39" class="note" fill="#64748B">ÜST</text>',
    ]

    top_groups = (
        (FIT_TEST["led_x"], FIT_TEST["led_diameters"], "10 mm LED", "led"),
        (FIT_TEST["dc184_x"], FIT_TEST["dc184_diameters"], "DC184", "dc184"),
        (FIT_TEST["dc180_x"], FIT_TEST["dc180_diameters"], "DC180", "dc180"),
        (FIT_TEST["dc131a_x"], FIT_TEST["dc131a_diameters"], "DC131A", "dc131a"),
    )
    for x_values, diameters, label, color_key in top_groups:
        color = COLORS[color_key]
        center_x = plate_x + sum(x_values) / len(x_values)
        parts.append(group_label(center_x, 27, label, color, plate_y))
        for x_value, diameter in zip(x_values, diameters):
            parts.append(
                svg_circle(
                    plate_x + x_value,
                    top_y,
                    diameter,
                    color,
                    decimal(diameter),
                    f"fit-{color_key}",
                )
            )

    buzzer_x = plate_x + FIT_TEST["buzzer_xy"][0]
    parts.append(group_label(buzzer_x, 24.5, "12 mm AKTİF BUZZER", COLORS["buzzer"], plate_y))
    parts.append(
        f'<circle cx="{buzzer_x}" cy="{top_y}" r="8.5" fill="#FFFFFF" '
        f'stroke="{COLORS["buzzer"]}" stroke-width="0.8" stroke-dasharray="1.5 1"/>'
    )
    for angle in range(0, 360, 60):
        hx = buzzer_x + 6.2 * cos(radians(angle))
        hy = top_y + 6.2 * sin(radians(angle))
        parts.append(f'<circle cx="{hx}" cy="{hy}" r="1.5" fill="{COLORS["ink"]}"/>')
    parts.extend(
        (
            f'<circle cx="{buzzer_x}" cy="{top_y}" r="1.5" fill="{COLORS["ink"]}"/>',
            f'<text x="{buzzer_x}" y="{top_y + 12}" text-anchor="middle" class="note">arka yuva Ø12,4</text>',
        )
    )

    for x_value, diameter in zip(
        FIT_TEST["pot_bushing_x"], FIT_TEST["pot_bushing_diameters"]
    ):
        parts.append(
            svg_circle(
                plate_x + x_value,
                bottom_y,
                diameter,
                COLORS["pot"],
                None,
                "fit-pot-bushing",
            )
        )
        parts.append(
            f'<text x="{plate_x + x_value}" y="{bottom_y + 8}" text-anchor="middle" class="size">{decimal(diameter)}</text>'
        )

    for x_value, diameter in zip(FIT_TEST["shaft_x"], FIT_TEST["shaft_diameters"]):
        x = plate_x + x_value
        parts.extend(
            (
                f'<circle cx="{x}" cy="{bottom_y}" r="6" fill="#D9C5B4" stroke="{COLORS["shaft"]}" stroke-width="0.8"/>',
                svg_circle(x, bottom_y, diameter, COLORS["shaft"], None, "fit-shaft"),
                f'<text x="{x}" y="{bottom_y + 8}" text-anchor="middle" class="size">{decimal(diameter)}</text>',
            )
        )

    for x_value, size in zip(FIT_TEST["dc120_x"], FIT_TEST["dc120_sizes"]):
        x = plate_x + x_value
        parts.extend(
            (
                f'<rect class="fit-dc120" x="{x - size[0] / 2}" y="{bottom_y - size[1] / 2}" width="{size[0]}" height="{size[1]}" rx="1" fill="#FFFFFF" stroke="{COLORS["dc120"]}" stroke-width="0.8"/>',
                f'<text x="{x}" y="{bottom_y + 0.8}" text-anchor="middle" class="size">{decimal(size[0])}×{decimal(size[1])}</text>',
            )
        )

    dial_x = plate_x + FIT_TEST["dial_xy"][0]
    parts.append(
        svg_circle(dial_x, bottom_y, 34.0, COLORS["dial"], "Ø34,0", "fit-dial")
    )

    bottom_labels = (
        (36, "POT BURCU", "pot"),
        (74, "POT MİLİ", "shaft"),
        (127, "DC120", "dc120"),
        (173, "ÇARK AÇIKLIĞI", "dial"),
    )
    for x, label, color_key in bottom_labels:
        parts.append(group_label(x, 123, label, COLORS[color_key], plate_y + plate_h))

    parts.append('</svg>')
    return "\n".join(parts) + "\n"


FONT_PATHS = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)


def font(size_mm, bold=False):
    candidates = list(FONT_PATHS)
    if bold:
        candidates.insert(0, "/System/Library/Fonts/Supplemental/Arial Bold.ttf")
        candidates.insert(1, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, px(size_mm))
    return ImageFont.load_default()


def mm_box(box):
    return tuple(px(value) for value in box)


def draw_text(draw, xy, value, size, fill=None, bold=False, anchor="mm"):
    draw.text(
        (px(xy[0]), px(xy[1])),
        value,
        font=font(size, bold),
        fill=fill or COLORS["ink"],
        anchor=anchor,
    )


def draw_circle(draw, x, y, diameter, color, text_value=None):
    radius = diameter / 2
    draw.ellipse(
        mm_box((x - radius, y - radius, x + radius, y + radius)),
        fill=COLORS["hole"],
        outline=color,
        width=px(0.8),
    )
    if text_value:
        draw_text(draw, (x, y), text_value, 2.25, bold=True)


def draw_group_label(draw, x, y, text_value, color, target_y):
    draw.line(mm_box((x, y + 2, x, target_y)), fill=color, width=px(0.6))
    draw_text(draw, (x, y), text_value, 3.2, color, bold=True)


def draw_png():
    image = Image.new("RGB", (px(CANVAS[0]), px(CANVAS[1])), COLORS["background"])
    draw = ImageDraw.Draw(image)
    plate_x, plate_y = PLATE_ORIGIN
    plate_w, plate_h = FIT_TEST["size"]
    top_y = svg_y(FIT_TEST["top_y"])
    bottom_y = svg_y(FIT_TEST["bottom_y"])

    draw_text(draw, (120, 8), "KOMPONENT UYUM TESTİ KILAVUZU", 6, bold=True)
    draw_text(
        draw,
        (120, 15),
        "MODEL: 200 × 76 mm  •  Soldaki seçenek daha sıkı, sağdaki daha rahattır",
        3,
    )
    draw.rounded_rectangle(
        mm_box((plate_x, plate_y, plate_x + plate_w, plate_y + plate_h)),
        radius=px(FIT_TEST["corner_radius"]),
        fill=COLORS["plate"],
        outline=COLORS["ink"],
        width=px(0.8),
    )
    draw_text(draw, (23, 39), "ÜST", 2.55, COLORS["muted"], anchor="lm")

    top_groups = (
        (FIT_TEST["led_x"], FIT_TEST["led_diameters"], "10 mm LED", "led"),
        (FIT_TEST["dc184_x"], FIT_TEST["dc184_diameters"], "DC184", "dc184"),
        (FIT_TEST["dc180_x"], FIT_TEST["dc180_diameters"], "DC180", "dc180"),
        (FIT_TEST["dc131a_x"], FIT_TEST["dc131a_diameters"], "DC131A", "dc131a"),
    )
    for x_values, diameters, label, color_key in top_groups:
        color = COLORS[color_key]
        center_x = plate_x + sum(x_values) / len(x_values)
        draw_group_label(draw, center_x, 27, label, color, plate_y)
        for x_value, diameter in zip(x_values, diameters):
            draw_circle(draw, plate_x + x_value, top_y, diameter, color, decimal(diameter))

    buzzer_x = plate_x + FIT_TEST["buzzer_xy"][0]
    draw_group_label(draw, buzzer_x, 24.5, "12 mm AKTİF BUZZER", COLORS["buzzer"], plate_y)
    draw.ellipse(
        mm_box((buzzer_x - 8.5, top_y - 8.5, buzzer_x + 8.5, top_y + 8.5)),
        fill=COLORS["hole"],
        outline=COLORS["buzzer"],
        width=px(0.8),
    )
    for angle in range(0, 360, 60):
        hx = buzzer_x + 6.2 * cos(radians(angle))
        hy = top_y + 6.2 * sin(radians(angle))
        draw.ellipse(mm_box((hx - 1.5, hy - 1.5, hx + 1.5, hy + 1.5)), fill=COLORS["ink"])
    draw.ellipse(mm_box((buzzer_x - 1.5, top_y - 1.5, buzzer_x + 1.5, top_y + 1.5)), fill=COLORS["ink"])
    draw_text(draw, (buzzer_x, top_y + 12), "arka yuva Ø12,4", 2.55)

    for x_value, diameter in zip(FIT_TEST["pot_bushing_x"], FIT_TEST["pot_bushing_diameters"]):
        x = plate_x + x_value
        draw_circle(draw, x, bottom_y, diameter, COLORS["pot"])
        draw_text(draw, (x, bottom_y + 8), decimal(diameter), 2.25, bold=True)

    for x_value, diameter in zip(FIT_TEST["shaft_x"], FIT_TEST["shaft_diameters"]):
        x = plate_x + x_value
        draw.ellipse(
            mm_box((x - 6, bottom_y - 6, x + 6, bottom_y + 6)),
            fill="#D9C5B4",
            outline=COLORS["shaft"],
            width=px(0.8),
        )
        draw_circle(draw, x, bottom_y, diameter, COLORS["shaft"])
        draw_text(draw, (x, bottom_y + 8), decimal(diameter), 2.25, bold=True)

    for x_value, size in zip(FIT_TEST["dc120_x"], FIT_TEST["dc120_sizes"]):
        x = plate_x + x_value
        draw.rounded_rectangle(
            mm_box((x - size[0] / 2, bottom_y - size[1] / 2,
                    x + size[0] / 2, bottom_y + size[1] / 2)),
            radius=px(1),
            fill=COLORS["hole"],
            outline=COLORS["dc120"],
            width=px(0.8),
        )
        draw_text(draw, (x, bottom_y), f"{decimal(size[0])}×{decimal(size[1])}", 2.25, bold=True)

    dial_x = plate_x + FIT_TEST["dial_xy"][0]
    draw_circle(draw, dial_x, bottom_y, 34.0, COLORS["dial"], "Ø34,0")

    for x, label, color_key in (
        (36, "POT BURCU", "pot"),
        (74, "POT MİLİ", "shaft"),
        (127, "DC120", "dc120"),
        (173, "ÇARK AÇIKLIĞI", "dial"),
    ):
        draw_group_label(draw, x, 123, label, COLORS[color_key], plate_y + plate_h)

    return image


def main():
    output = Path("docs")
    output.mkdir(parents=True, exist_ok=True)
    (output / "component-fit-test-guide.svg").write_text(
        generate_svg(), encoding="utf-8"
    )
    draw_png().save(
        output / "component-fit-test-guide.png", dpi=(DPI, DPI)
    )
    print("wrote component fit-test SVG and PNG guide")


if __name__ == "__main__":
    main()

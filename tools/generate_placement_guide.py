"""Generate the front, side, and rear component placement guide."""

from html import escape
from math import cos, radians, sin
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_spec import PANEL_FEATURES


DPI = 300
MM_TO_PX = DPI / 25.4
CANVAS = (320, 230)
FRONT_ORIGIN = (18, 29)
FRONT_SCALE = 0.9
COLORS = {
    "background": "#FFF8E8",
    "panel": "#E8F0F5",
    "panel_line": "#263548",
    "ink": "#263548",
    "muted": "#5C6D7E",
    "white": "#FFFFFF",
    "red": "#DF4C52",
    "yellow": "#E9B92D",
    "green": "#3BA66B",
    "blue": "#438DCA",
    "black": "#303640",
    "purple": "#7A63B5",
    "orange": "#E6893B",
    "card": "#FFFFFF",
    "rail": "#B9C7D3",
}

ITEMS = (
    (1, "red_led", "KIRMIZI 10 mm LED", "Ø10,2 · içten tak", "red"),
    (2, "red_button", "KIRMIZI DC184", "Ø12,0 · somun içte", "red"),
    (3, "yellow_led", "SARI 10 mm LED", "Ø10,2 · içten tak", "yellow"),
    (4, "yellow_button", "SARI DC184", "Ø12,0 · somun içte", "yellow"),
    (5, "green_led", "YEŞİL 10 mm LED", "Ø10,2 · içten tak", "green"),
    (6, "green_button", "SİYAH DC180", "Ø16,0 · somun içte", "black"),
    (7, "switch_led", "MAVİ 10 mm LED", "Ø10,2 · içten tak", "blue"),
    (8, "rocker", "DC131A", "Ø20,2 · somun içte", "red"),
    (9, "dimmer_led", "BEYAZ 10 mm LED", "Ø10,2 · içten tak", "white"),
    (10, "dial", "1K POT + ÇARK", "burç Ø7,0 · mil Ø6,2", "orange"),
    (11, "buzzer", "12 mm AKTİF BUZZER", "içteki kaba yerleştir", "purple"),
    (12, "buzzer_button", "MAVİ DC180", "Ø16,0 · somun içte", "blue"),
)

FEATURES = {feature["id"]: feature for feature in PANEL_FEATURES}
FONT_PATHS = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
BOLD_FONT_PATHS = (
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


def px(mm):
    return round(mm * MM_TO_PX)


def mm_box(box):
    return tuple(px(value) for value in box)


def font(size_mm, bold=False):
    candidates = BOLD_FONT_PATHS if bold else FONT_PATHS
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, px(size_mm))
    return ImageFont.load_default()


def svg_text(x, y, value, css_class, anchor="start", fill=None):
    color = f' fill="{fill}"' if fill else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'class="{css_class}"{color}>{escape(value)}</text>'
    )


def front_xy(feature):
    return (
        FRONT_ORIGIN[0] + feature["x"] * FRONT_SCALE,
        FRONT_ORIGIN[1] + feature["y"] * FRONT_SCALE,
    )


def component_radius(feature):
    if feature["id"] == "dial":
        return 17 * FRONT_SCALE
    if feature["kind"] == "pattern":
        return 8 * FRONT_SCALE
    return max(feature["radius"] * FRONT_SCALE, 4.2)


def component_svg(number, feature_id, color_key):
    feature = FEATURES[feature_id]
    cx, cy = front_xy(feature)
    radius = component_radius(feature)
    fill = COLORS[color_key]
    number_fill = COLORS["ink"] if color_key in ("white", "yellow") else COLORS["white"]
    parts = [f'<g id="placement-{feature_id}">']
    if feature["kind"] == "pattern":
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{COLORS["white"]}" '
            f'stroke="{fill}" stroke-width="1.2"/>'
        )
        for angle in range(0, 360, 60):
            hx = cx + 5.2 * cos(radians(angle))
            hy = cy + 5.2 * sin(radians(angle))
            parts.append(f'<circle cx="{hx}" cy="{hy}" r="1.2" fill="{fill}"/>')
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="3.3" fill="{fill}"/>')
    else:
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{fill}" '
            f'stroke="{COLORS["ink"]}" stroke-width="1"/>'
        )
        if feature_id == "dial":
            parts.append(
                f'<path d="M{cx} {cy - radius + 2} V{cy - 4}" '
                f'stroke="{COLORS["white"]}" stroke-width="1.4" stroke-linecap="round"/>'
            )
    parts.append(svg_text(cx, cy + 1.2, str(number), "badge", "middle", number_fill))
    parts.append("</g>")
    return "".join(parts)


def generate_svg():
    panel_w = 200 * FRONT_SCALE
    panel_h = 160 * FRONT_SCALE
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="320mm" height="230mm" viewBox="0 0 320 230">',
        '<style>text{font-family:Arial,sans-serif;fill:#263548}.title{font-size:7px;font-weight:bold}.subtitle{font-size:3.2px}.view{font-size:3.6px;font-weight:bold}.badge{font-size:3.2px;font-weight:bold;dominant-baseline:middle}.legend-title{font-size:3.1px;font-weight:bold}.legend-detail{font-size:2.35px}.small{font-size:2.7px}.note{font-size:2.45px}</style>',
        f'<rect width="320" height="230" fill="{COLORS["background"]}"/>',
        svg_text(160, 10, "MİNİK KEŞİF KUTUSU — BİLEŞEN YERLEŞİMİ", "title", "middle"),
        svg_text(160, 17, "Parçaları ön yüzden bu sıraya göre yerleştir; somun ve kablolar kutunun içinde kalır.", "subtitle", "middle", COLORS["muted"]),
        svg_text(FRONT_ORIGIN[0], 25, "ÖNDEN GÖRÜNÜŞ", "view"),
        f'<rect x="{FRONT_ORIGIN[0]}" y="{FRONT_ORIGIN[1]}" width="{panel_w}" height="{panel_h}" rx="12.6" fill="{COLORS["panel"]}" stroke="{COLORS["panel_line"]}" stroke-width="1.2"/>',
    ]

    zone_colors = ("#F8D6D7", "#FAEDB9", "#D3EDDB", "#D7E9F6", "#D9EFE4", "#E5DCF4")
    for index, (column, row) in enumerate(
        ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1))
    ):
        x = FRONT_ORIGIN[0] + (15 + column * 60) * FRONT_SCALE
        y = FRONT_ORIGIN[1] + (8 + row * 79) * FRONT_SCALE
        parts.append(
            f'<rect x="{x}" y="{y}" width="{54 * FRONT_SCALE}" '
            f'height="{65 * FRONT_SCALE}" rx="8" fill="{zone_colors[index]}"/>'
        )

    for number, feature_id, _, _, color_key in ITEMS:
        parts.append(component_svg(number, feature_id, color_key))

    legend_x, legend_y, legend_w = 207, 27, 105
    parts.extend(
        (
            f'<rect x="{legend_x}" y="{legend_y}" width="{legend_w}" height="147" rx="6" fill="{COLORS["card"]}" stroke="{COLORS["rail"]}" stroke-width="0.8"/>',
            svg_text(legend_x + 5, legend_y + 7, "NUMARA → TAKILACAK PARÇA", "view"),
        )
    )
    for index, (number, _, label, detail, color_key) in enumerate(ITEMS):
        row_y = legend_y + 14 + index * 10.8
        parts.extend(
            (
                f'<circle cx="{legend_x + 6}" cy="{row_y}" r="3.2" fill="{COLORS[color_key]}" stroke="{COLORS["ink"]}" stroke-width="0.5"/>',
                svg_text(legend_x + 6, row_y + 0.9, str(number), "badge", "middle", COLORS["ink"] if color_key in ("white", "yellow") else COLORS["white"]),
                svg_text(legend_x + 12, row_y - 0.5, label, "legend-title"),
                svg_text(legend_x + 12, row_y + 3, detail, "legend-detail", fill=COLORS["muted"]),
            )
        )

    parts.extend(
        (
            '<rect x="18" y="179" width="82" height="39" rx="6" fill="#FFFFFF" stroke="#B9C7D3" stroke-width="0.8"/>',
            svg_text(24, 186, "SAĞ YAN", "view"),
            '<rect x="25" y="190" width="60" height="20" rx="5" fill="#E8F0F5" stroke="#263548" stroke-width="0.8"/>',
            '<rect x="48" y="192" width="19" height="13" rx="1" fill="#DF4C52" stroke="#263548" stroke-width="0.8"/>',
            svg_text(57.5, 199.5, "DC120 2P", "legend-title", "middle", COLORS["white"]),
            svg_text(57.5, 215, "19×13 mm · tırnakla", "small", "middle"),
            '<rect x="106" y="179" width="122" height="39" rx="6" fill="#FFFFFF" stroke="#B9C7D3" stroke-width="0.8"/>',
            svg_text(112, 186, "ARKA KAPAK", "view"),
            '<rect x="113" y="190" width="50" height="21" rx="3" fill="#E8F0F5" stroke="#263548" stroke-width="0.8"/>',
            '<rect x="170" y="190" width="50" height="21" rx="3" fill="#E8F0F5" stroke="#263548" stroke-width="0.8"/>',
            svg_text(138, 199, "2×AA", "legend-title", "middle"),
            svg_text(195, 199, "2×AA", "legend-title", "middle"),
            svg_text(166.5, 215, "2×AA PİL YUVASI ×2 · ayrı raylara", "small", "middle"),
            '<rect x="234" y="179" width="78" height="39" rx="6" fill="#FFFFFF" stroke="#B9C7D3" stroke-width="0.8"/>',
            svg_text(240, 186, "MONTAJ YÖNÜ", "view"),
            svg_text(240, 192, "• LED lensi dışarı, flanşı içeri", "note"),
            svg_text(240, 197.5, "• Somunlar kutunun içinde", "note"),
            svg_text(240, 203, "• Pot gövdesi içeride, çark dışarıda", "note"),
            svg_text(240, 208.5, "• Buzzer deliklere dönük", "note"),
            svg_text(240, 214, "• Kabloları kapaktan uzak tut", "note"),
            "</svg>",
        )
    )
    return "\n".join(parts) + "\n"


def draw_text(draw, xy, value, size, fill=None, bold=False, anchor="la"):
    draw.text(
        (px(xy[0]), px(xy[1])),
        value,
        font=font(size, bold),
        fill=fill or COLORS["ink"],
        anchor=anchor,
    )


def draw_component(draw, number, feature_id, color_key):
    feature = FEATURES[feature_id]
    cx, cy = front_xy(feature)
    radius = component_radius(feature)
    fill = COLORS[color_key]
    box = mm_box((cx - radius, cy - radius, cx + radius, cy + radius))
    if feature["kind"] == "pattern":
        draw.ellipse(box, fill=COLORS["white"], outline=fill, width=px(1.2))
        for angle in range(0, 360, 60):
            hx = cx + 5.2 * cos(radians(angle))
            hy = cy + 5.2 * sin(radians(angle))
            draw.ellipse(mm_box((hx - 1.2, hy - 1.2, hx + 1.2, hy + 1.2)), fill=fill)
        draw.ellipse(mm_box((cx - 3.3, cy - 3.3, cx + 3.3, cy + 3.3)), fill=fill)
    else:
        draw.ellipse(box, fill=fill, outline=COLORS["ink"], width=px(1))
        if feature_id == "dial":
            draw.line(
                [(px(cx), px(cy - radius + 2)), (px(cx), px(cy - 4))],
                fill=COLORS["white"],
                width=px(1.4),
            )
    number_fill = COLORS["ink"] if color_key in ("white", "yellow") else COLORS["white"]
    draw_text(draw, (cx, cy), str(number), 3.2, number_fill, True, "mm")


def draw_png():
    image = Image.new("RGB", (px(CANVAS[0]), px(CANVAS[1])), COLORS["background"])
    draw = ImageDraw.Draw(image)
    panel_w = 200 * FRONT_SCALE
    panel_h = 160 * FRONT_SCALE
    draw_text(draw, (160, 10), "MİNİK KEŞİF KUTUSU — BİLEŞEN YERLEŞİMİ", 7, bold=True, anchor="mm")
    draw_text(
        draw,
        (160, 17),
        "Parçaları ön yüzden bu sıraya göre yerleştir; somun ve kablolar kutunun içinde kalır.",
        3.2,
        COLORS["muted"],
        anchor="mm",
    )
    draw_text(draw, (FRONT_ORIGIN[0], 25), "ÖNDEN GÖRÜNÜŞ", 3.6, bold=True)
    draw.rounded_rectangle(
        mm_box((FRONT_ORIGIN[0], FRONT_ORIGIN[1], FRONT_ORIGIN[0] + panel_w, FRONT_ORIGIN[1] + panel_h)),
        radius=px(12.6),
        fill=COLORS["panel"],
        outline=COLORS["panel_line"],
        width=px(1.2),
    )
    zone_colors = ("#F8D6D7", "#FAEDB9", "#D3EDDB", "#D7E9F6", "#D9EFE4", "#E5DCF4")
    for index, (column, row) in enumerate(
        ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1))
    ):
        x = FRONT_ORIGIN[0] + (15 + column * 60) * FRONT_SCALE
        y = FRONT_ORIGIN[1] + (8 + row * 79) * FRONT_SCALE
        draw.rounded_rectangle(
            mm_box((x, y, x + 54 * FRONT_SCALE, y + 65 * FRONT_SCALE)),
            radius=px(8),
            fill=zone_colors[index],
        )
    for number, feature_id, _, _, color_key in ITEMS:
        draw_component(draw, number, feature_id, color_key)

    legend_x, legend_y, legend_w = 207, 27, 105
    draw.rounded_rectangle(
        mm_box((legend_x, legend_y, legend_x + legend_w, legend_y + 147)),
        radius=px(6),
        fill=COLORS["card"],
        outline=COLORS["rail"],
        width=px(0.8),
    )
    draw_text(draw, (legend_x + 5, legend_y + 7), "NUMARA → TAKILACAK PARÇA", 3.6, bold=True)
    for index, (number, _, label, detail, color_key) in enumerate(ITEMS):
        row_y = legend_y + 14 + index * 10.8
        draw.ellipse(
            mm_box((legend_x + 2.8, row_y - 3.2, legend_x + 9.2, row_y + 3.2)),
            fill=COLORS[color_key],
            outline=COLORS["ink"],
            width=px(0.5),
        )
        number_fill = COLORS["ink"] if color_key in ("white", "yellow") else COLORS["white"]
        draw_text(draw, (legend_x + 6, row_y), str(number), 3.2, number_fill, True, "mm")
        draw_text(draw, (legend_x + 12, row_y - 1.1), label, 3.1, bold=True, anchor="lm")
        draw_text(draw, (legend_x + 12, row_y + 2.4), detail, 2.35, COLORS["muted"], anchor="lm")

    cards = ((18, 179, 100, 218), (106, 179, 228, 218), (234, 179, 312, 218))
    for card in cards:
        draw.rounded_rectangle(
            mm_box(card), radius=px(6), fill=COLORS["card"], outline=COLORS["rail"], width=px(0.8)
        )
    draw_text(draw, (24, 186), "SAĞ YAN", 3.6, bold=True)
    draw.rounded_rectangle(mm_box((25, 190, 85, 210)), radius=px(5), fill=COLORS["panel"], outline=COLORS["ink"], width=px(0.8))
    draw.rounded_rectangle(mm_box((48, 192, 67, 205)), radius=px(1), fill=COLORS["red"], outline=COLORS["ink"], width=px(0.8))
    draw_text(draw, (57.5, 198.5), "DC120 2P", 3.1, COLORS["white"], True, "mm")
    draw_text(draw, (57.5, 215), "19×13 mm · tırnakla", 2.7, anchor="mm")

    draw_text(draw, (112, 186), "ARKA KAPAK", 3.6, bold=True)
    for x in (113, 170):
        draw.rounded_rectangle(mm_box((x, 190, x + 50, 211)), radius=px(3), fill=COLORS["panel"], outline=COLORS["ink"], width=px(0.8))
        draw_text(draw, (x + 25, 199), "2×AA", 3.1, bold=True, anchor="mm")
    draw_text(draw, (166.5, 215), "2×AA PİL YUVASI ×2 · ayrı raylara", 2.7, anchor="mm")

    draw_text(draw, (240, 186), "MONTAJ YÖNÜ", 3.6, bold=True)
    for index, note in enumerate(
        (
            "• LED lensi dışarı, flanşı içeri",
            "• Somunlar kutunun içinde",
            "• Pot gövdesi içeride, çark dışarıda",
            "• Buzzer deliklere dönük",
            "• Kabloları kapaktan uzak tut",
        )
    ):
        draw_text(draw, (240, 192 + index * 5.5), note, 2.45)
    return image


def main():
    output = Path("docs")
    output.mkdir(parents=True, exist_ok=True)
    (output / "component-placement-guide.svg").write_text(
        generate_svg(), encoding="utf-8"
    )
    draw_png().save(output / "component-placement-guide.png", dpi=(DPI, DPI))
    print("wrote component placement SVG and PNG guide")


if __name__ == "__main__":
    main()

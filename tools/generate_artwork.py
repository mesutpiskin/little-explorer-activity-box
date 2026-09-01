"""Generate aligned vector and 300 dpi sticker artwork."""

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

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
SCENE = {
    "navy": "#27364B",
    "gold": "#F3C34F",
    "cream": "#FFF8E8",
    "teal": "#2D9C95",
    "red": "#D94B3D",
    "red_dark": "#A93632",
    "sky": "#55B7D9",
}
LABEL_SPECS = {
    "LAMBA": (42, 84, 3.8),
    "AMPUL": (102, 84, 3.8),
    "FENER": (162, 84, 3.8),
    "AÇ/KAPAT": (42, 157.2, 3.4),
    "AZ–ÇOK": (102, 157.2, 3.4),
    "İTFAİYE": (162, 157.2, 3.4),
}


def px(mm):
    return round(mm * MM_TO_PX)


def svg_circle(cx, cy, radius, **attrs):
    rendered = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return f'<circle cx="{cx}" cy="{cy}" r="{radius}" {rendered}/>'


def cutout_svg(feature):
    x = feature["x"] + LABEL["bleed"]
    y = feature["y"] + LABEL["bleed"]
    cutout_id = f'cutout-{feature["id"].replace("_", "-")}'
    common = 'fill="#FFFFFF" stroke="#27364B" stroke-width="0.45" stroke-dasharray="1.5 1.5"'
    if feature["kind"] == "rect":
        return (
            f'<rect id="{cutout_id}" x="{x - feature["width"] / 2}" y="{y - feature["height"] / 2}" '
            f'width="{feature["width"]}" height="{feature["height"]}" rx="1" {common}/>'
        )
    if feature["kind"] == "pattern":
        holes = [svg_circle(x, y, 1.5, id=cutout_id, fill="#FFFFFF", stroke="#27364B", stroke_width="0.35")]
        for angle in range(0, 360, 60):
            import math
            hx = x + 6.2 * math.cos(math.radians(angle))
            hy = y + 6.2 * math.sin(math.radians(angle))
            holes.append(svg_circle(hx, hy, 1.5, fill="#FFFFFF", stroke="#27364B", stroke_width="0.35"))
        return "".join(holes)
    return svg_circle(x, y, feature["radius"], id=cutout_id, fill="#FFFFFF", stroke="#27364B", stroke_width="0.45", stroke_dasharray="1.5 1.5")


def svg_label(text):
    x, y, size = LABEL_SPECS[text]
    return (
        f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" fill="{SCENE["navy"]}" '
        f'stroke="none" font-size="{size}" font-weight="700">{text}</text>'
    )


def educational_scenes_svg():
    ink = SCENE["navy"]
    gold = SCENE["gold"]
    red = SCENE["red"]
    red_dark = SCENE["red_dark"]
    teal = SCENE["teal"]
    return f"""
<g id="scene-table-lamp" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M26 36 L32 22 Q42 18 52 22 L58 36 Z" fill="{gold}" stroke-width="1.5"/>
  <path d="M30 38 Q25 43 27 51" fill="none" stroke-width="2.2"/>
  <path d="M24 52 H35" fill="none" stroke-width="2.2"/>
  <path d="M22 30 H17 M25 22 L21 18 M59 30 H64 M56 22 L60 18" fill="none" stroke="{gold}" stroke-width="1.8"/>
  {svg_label("LAMBA")}
</g>
<g id="scene-hanging-bulb" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M102 8 V20" fill="none" stroke-width="1.8"/>
  <path d="M94 29 Q94 20 102 20 Q110 20 110 29 Q110 35 106 38 H98 Q94 35 94 29 Z" fill="{gold}" stroke-width="1.5"/>
  <path d="M98 39 H106 M99 42 H105" fill="none" stroke-width="1.5"/>
  <path d="M88 27 H83 M91 19 L87 15 M116 27 H121 M113 19 L117 15" fill="none" stroke="{gold}" stroke-width="1.8"/>
  <path d="M102 46 V48" fill="none" stroke-width="1.5" stroke-dasharray="1 2"/>
  {svg_label("AMPUL")}
</g>
<g id="scene-lighthouse" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M153 34 Q162 20 171 34 Z" fill="{gold}" stroke-width="1.5"/>
  <path d="M156 36 L154 42 H170 L168 36 Z" fill="{SCENE['cream']}" stroke-width="1.6"/>
  <path d="M155 41 L169 37" fill="none" stroke="{red}" stroke-width="2.2"/>
  <path d="M153 42 H171" fill="none" stroke-width="2"/>
  <path d="M150 26 H142 M174 26 H182 M151 20 L145 16 M173 20 L179 16" fill="none" stroke="{gold}" stroke-width="2"/>
  {svg_label("FENER")}
</g>
<g id="scene-room-switch" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M31 108 L35 96 H49 L53 108 Z" fill="{gold}" stroke-width="1.5"/>
  <path d="M42 90 V96" fill="none" stroke-width="1.6"/>
  <path d="M34 111 L31 115 M42 111 V116 M50 111 L53 115" fill="none" stroke="{gold}" stroke-width="1.6"/>
  <rect x="28" y="118" width="28" height="27" rx="4" fill="{SCENE['cream']}" stroke-width="1.3"/>
  {svg_label("AÇ/KAPAT")}
</g>
<g id="scene-dimmer" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M84 105 A7 7 0 1 0 90 114 A5.3 5.3 0 0 1 84 105 Z" fill="{SCENE['cream']}" stroke-width="1.3"/>
  <circle cx="120" cy="109" r="5" fill="{gold}" stroke-width="1.3"/>
  <path d="M120 100 V97 M120 118 V121 M111 109 H108 M129 109 H132 M114 103 L112 101 M126 115 L128 117 M126 103 L128 101 M114 115 L112 117" fill="none" stroke="{gold}" stroke-width="1.4"/>
  <path d="M88 121 Q102 111 116 121" fill="none" stroke="{teal}" stroke-width="1.7" stroke-dasharray="1 2"/>
  {svg_label("AZ–ÇOK")}
</g>
<g id="scene-fire-engine" stroke="{ink}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M154 106 Q154 94 162 92 Q170 94 170 106 Z" fill="{red}" stroke-width="1.4"/>
  <path d="M151 95 H144 M173 95 H180 M151 90 L146 86 M173 90 L178 86" fill="none" stroke="{red}" stroke-width="1.8"/>
  <path d="M139 105 H169 L176 98 H183 Q186 98 186 103 V114 H139 Z" fill="{red}" stroke-width="1.6"/>
  <path d="M176 101 H182 V108 H171 Z" fill="{SCENE['sky']}" stroke-width="1.2"/>
  <path d="M140 96 L181 86 M142 100 L183 90 M147 94 L150 101 M158 91 L161 98 M169 88 L172 95" fill="none" stroke="{SCENE['cream']}" stroke-width="1.6"/>
  <circle cx="149" cy="112" r="4" fill="{red_dark}" stroke-width="1.4"/>
  <circle cx="178" cy="112" r="4" fill="{red_dark}" stroke-width="1.4"/>
  <path d="M137 114 H188" fill="none" stroke-width="2"/>
  {svg_label("İTFAİYE")}
</g>"""


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
        '<svg xmlns="http://www.w3.org/2000/svg" width="204mm" height="164mm" viewBox="0 0 204 164" font-family="Arial, sans-serif">',
        f'<rect width="204" height="164" rx="15" fill="{PALETTE["background"]}"/>',
    ]
    for x, y, width, height, color in panels:
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{color}"/>')
    parts.append(educational_scenes_svg())
    parts.extend(cutout_svg(feature) for feature in PANEL_FEATURES)
    parts.append('<rect id="trim-line" x="2" y="2" width="200" height="160" rx="14" fill="none" stroke="#D84A4A" stroke-width="0.3" stroke-dasharray="2 1"/>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def mm_box(box):
    return tuple(px(value) for value in box)


def draw_dashed_ellipse(draw, box, fill, width=4):
    for start in range(0, 360, 24):
        draw.arc(box, start=start, end=start + 13, fill=fill, width=width)


def point_mm(x, y):
    return (px(x), px(y))


def draw_line_mm(draw, points, fill, width, joint="curve"):
    draw.line([point_mm(x, y) for x, y in points], fill=fill, width=px(width), joint=joint)


def draw_label(draw, x, y, text, size=3.8):
    font = ImageFont.truetype(
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf", px(size)
    )
    draw.text(point_mm(x, y), text, font=font, fill=SCENE["navy"], anchor="mm")


def draw_named_label(draw, text):
    x, y, size = LABEL_SPECS[text]
    draw_label(draw, x, y, text, size)


def draw_educational_scenes(draw):
    ink = SCENE["navy"]
    gold = SCENE["gold"]
    cream = SCENE["cream"]
    red = SCENE["red"]
    teal = SCENE["teal"]

    # Table lamp: the real LED sits in the shade and the real button becomes its base.
    draw.polygon([point_mm(*p) for p in ((26, 36), (32, 22), (42, 19), (52, 22), (58, 36))], fill=gold)
    draw_line_mm(draw, ((26, 36), (32, 22), (42, 19), (52, 22), (58, 36)), ink, 1.5)
    draw.arc(mm_box((20, 36, 34, 55)), 115, 245, fill=ink, width=px(2.2))
    draw_line_mm(draw, ((24, 52), (35, 52)), ink, 2.2)
    for start, end in (((22, 30), (17, 30)), ((25, 22), (21, 18)), ((59, 30), (64, 30)), ((56, 22), (60, 18))):
        draw_line_mm(draw, (start, end), gold, 1.8)
    draw_named_label(draw, "LAMBA")

    # Hanging bulb.
    draw_line_mm(draw, ((102, 8), (102, 20)), ink, 1.8)
    draw.ellipse(mm_box((94, 20, 110, 38)), fill=gold, outline=ink, width=px(1.5))
    draw.rectangle(mm_box((98, 36, 106, 42)), fill=cream, outline=ink, width=px(1.2))
    for start, end in (((88, 27), (83, 27)), ((91, 19), (87, 15)), ((116, 27), (121, 27)), ((113, 19), (117, 15))):
        draw_line_mm(draw, (start, end), gold, 1.8)
    draw_named_label(draw, "AMPUL")

    # Lighthouse with the real orange LED as its beacon.
    draw.polygon([point_mm(*p) for p in ((153, 34), (162, 20), (171, 34))], fill=gold)
    draw_line_mm(draw, ((153, 34), (162, 20), (171, 34), (153, 34)), ink, 1.5)
    draw.polygon([point_mm(*p) for p in ((156, 36), (168, 36), (170, 42), (154, 42))], fill=cream)
    draw_line_mm(draw, ((156, 36), (154, 42), (170, 42), (168, 36)), ink, 1.6)
    draw_line_mm(draw, ((155, 41), (169, 37)), red, 2.2)
    for start, end in (((150, 26), (142, 26)), ((174, 26), (182, 26)), ((151, 20), (145, 16)), ((173, 20), (179, 16))):
        draw_line_mm(draw, (start, end), gold, 2)
    draw_named_label(draw, "FENER")

    # Room lamp and wall switch.
    draw_line_mm(draw, ((42, 89), (42, 96)), ink, 1.6)
    draw.polygon([point_mm(*p) for p in ((31, 108), (35, 96), (49, 96), (53, 108))], fill=gold)
    draw_line_mm(draw, ((31, 108), (35, 96), (49, 96), (53, 108), (31, 108)), ink, 1.5)
    draw.rounded_rectangle(mm_box((28, 118, 56, 145)), radius=px(4), fill=cream, outline=ink, width=px(1.3))
    for start, end in (((34, 111), (31, 115)), ((42, 111), (42, 116)), ((50, 111), (53, 115))):
        draw_line_mm(draw, (start, end), gold, 1.6)
    draw_named_label(draw, "AÇ/KAPAT")

    # Dimmer: moon to sun, with the real dial centered below the lesson.
    draw.ellipse(mm_box((77, 102, 91, 116)), fill=cream, outline=ink, width=px(1.3))
    draw.ellipse(mm_box((82, 100, 94, 112)), fill=PALETTE["mint"])
    draw.ellipse(mm_box((115, 104, 125, 114)), fill=gold, outline=ink, width=px(1.2))
    for start, end in (((120, 100), (120, 97)), ((120, 118), (120, 121)), ((111, 109), (108, 109)), ((129, 109), (132, 109))):
        draw_line_mm(draw, (start, end), gold, 1.4)
    draw.arc(mm_box((87, 113, 117, 132)), 200, 340, fill=teal, width=px(1.7))
    draw_named_label(draw, "AZ–ÇOK")

    # Fire engine: buzzer holes become its roof siren; blue button becomes a wheel.
    draw.pieslice(mm_box((154, 92, 170, 108)), 180, 360, fill=red, outline=ink, width=px(1.4))
    draw.polygon([point_mm(*p) for p in ((139, 105), (169, 105), (176, 98), (183, 98), (186, 103), (186, 114), (139, 114))], fill=red)
    draw_line_mm(draw, ((139, 105), (169, 105), (176, 98), (183, 98), (186, 103), (186, 114), (139, 114), (139, 105)), ink, 1.6)
    draw.polygon([point_mm(*p) for p in ((176, 101), (182, 101), (182, 108), (171, 108))], fill=SCENE["sky"])
    draw_line_mm(draw, ((140, 96), (181, 86)), cream, 1.6)
    draw_line_mm(draw, ((142, 100), (183, 90)), cream, 1.6)
    draw.ellipse(mm_box((145, 108, 153, 116)), fill=SCENE["red_dark"], outline=ink, width=px(1.4))
    draw.ellipse(mm_box((174, 108, 182, 116)), fill=SCENE["red_dark"], outline=ink, width=px(1.4))
    draw_named_label(draw, "İTFAİYE")


def draw_round_component(draw, center, outer_diameter, color):
    cx, cy = center
    outer_radius = outer_diameter / 2
    inner_radius = outer_radius - 2
    draw.ellipse(
        mm_box((cx - outer_radius, cy - outer_radius, cx + outer_radius, cy + outer_radius)),
        fill="#202A37",
    )
    draw.ellipse(
        mm_box((cx - inner_radius, cy - inner_radius, cx + inner_radius, cy + inner_radius)),
        fill=color,
        outline="#FFFFFF",
        width=px(0.5),
    )
    draw.ellipse(
        mm_box((cx - inner_radius * 0.55, cy - inner_radius * 0.62,
                cx - inner_radius * 0.1, cy - inner_radius * 0.25)),
        fill="#FFFFFF",
    )


def draw_assembled_preview():
    image = draw_preview().convert("RGB")
    draw = ImageDraw.Draw(image)
    draw_round_component(draw, (42, 59), 33, "#DF4C52")
    draw_round_component(draw, (102, 59), 33, "#F1C52F")
    draw_round_component(draw, (162, 59), 33, "#F08B2E")
    draw_round_component(draw, (162, 132), 33, "#3B82D0")

    for center, color in (
        ((42, 30), "#E33C45"),
        ((102, 30), "#FFD52E"),
        ((162, 30), "#F39A2E"),
        ((42, 103), "#F8F5D8"),
        ((102, 103), "#F8F5D8"),
    ):
        draw_round_component(draw, center, 10.5, color)

    draw.rounded_rectangle(
        mm_box((29, 121, 55, 141)),
        radius=px(2),
        fill="#202A37",
    )
    draw.rounded_rectangle(
        mm_box((31.5, 123, 52.5, 139)),
        radius=px(1.4),
        fill="#4B87C5",
        outline="#D7E9FF",
        width=px(0.5),
    )

    draw_round_component(draw, (102, 130), 32, "#4B87C5")
    draw_line_mm(draw, ((102, 130), (111, 122)), "#FFFFFF", 1.2)
    return image


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

    draw_educational_scenes(draw)

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
    draw_assembled_preview().save(
        output / "activity-box-assembled-preview.png",
        dpi=(LABEL["dpi"], LABEL["dpi"]),
    )
    generate_a4_pdf(preview).save(
        output / "activity-box-label-a4.pdf", "PDF", resolution=float(LABEL["dpi"])
    )
    print("wrote sticker SVG, PNG, and A4 PDF")


if __name__ == "__main__":
    main()

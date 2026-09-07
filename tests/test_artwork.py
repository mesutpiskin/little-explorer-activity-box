import pathlib
import unittest
import xml.etree.ElementTree as ET

from PIL import Image, ImageColor, ImageDraw

from tools.generate_artwork import (
    draw_assembled_preview,
    draw_preview,
    font,
    generate_a4_pdf,
    generate_svg,
    px,
)
from tools.project_spec import BOX, LABEL, PANEL_FEATURES


class ArtworkTest(unittest.TestCase):
    def test_svg_has_exact_physical_size_and_trim(self):
        text = pathlib.Path("artwork/activity-box-label.svg").read_text(
            encoding="utf-8"
        )
        self.assertIn('width="204mm"', text)
        self.assertIn('height="164mm"', text)
        self.assertIn('id="trim-line"', text)

    def test_preview_is_300_dpi_size(self):
        with Image.open("artwork/activity-box-label-preview.png") as image:
            self.assertEqual(image.size, (2409, 1937))

    def test_preview_contains_instruction_icons(self):
        with Image.open("artwork/activity-box-label-preview.png") as image:
            ink = ImageColor.getrgb("#27364B")
            icon_band = image.crop((250, 120, 2150, 270))
            ink_pixels = sum(pixel == ink for pixel in icon_band.getdata())
            self.assertGreater(ink_pixels, 100)

    def test_a4_pdf_is_generated(self):
        pdf = pathlib.Path("artwork/activity-box-label-a4.pdf").read_bytes()
        self.assertTrue(pdf.startswith(b"%PDF"))

    def test_a4_layout_matches_the_box_exterior_view(self):
        label = draw_preview()
        page = generate_a4_pdf(label)
        left = round((page.width - label.width) / 2)
        self.assertEqual(
            page.getpixel((left + px(30), px(12 + 70))),
            ImageColor.getrgb("#A8DDA7"),
        )
        self.assertEqual(
            page.getpixel((left + px(150), px(12 + 70))),
            ImageColor.getrgb("#F4A6A6"),
        )

    def test_assembled_preview_is_generated_at_label_size(self):
        with Image.open("artwork/activity-box-assembled-preview.png") as image:
            self.assertEqual(image.size, (2409, 1937))

    def test_assembled_preview_matches_purchased_component_colors(self):
        image = draw_assembled_preview()
        expected_centers = {
            (42, 59): "#111820",  # siyah DC180
            (162, 131): "#303844",  # yuvarlak DC131A
            (42, 132): "#2878C8",  # mavi DC180
            (42, 30): "#35B86B",  # yeşil LED
            (162, 103): "#3F8FE8",  # mavi LED
            (102, 103): "#F4F7FF",  # beyaz LED
        }
        for center, color in expected_centers.items():
            self.assertEqual(image.getpixel((px(center[0]), px(center[1]))), ImageColor.getrgb(color))

    def test_svg_contains_six_educational_scenes(self):
        svg = generate_svg()
        scene_ids = (
            "scene-table-lamp",
            "scene-hanging-bulb",
            "scene-lighthouse",
            "scene-room-switch",
            "scene-dimmer",
            "scene-fire-engine",
        )
        for scene_id in scene_ids:
            self.assertIn(f'id="{scene_id}"', svg)
        for label in ("LAMP", "BULB", "BEACON", "ON/OFF", "DIMMER", "FIRE ENGINE"):
            self.assertIn(f">{label}</text>", svg)
        self.assertIn("font-family:'DejaVu Sans',sans-serif", svg)

    def test_svg_labels_use_the_same_center_anchor_as_the_png(self):
        root = ET.fromstring(generate_svg())
        labels = [element for element in root.iter() if element.tag.endswith("text")]
        self.assertEqual(len(labels), 6)
        for label in labels:
            self.assertEqual(label.attrib.get("dominant-baseline"), "middle")

    def test_svg_keeps_every_cutout_at_the_cad_coordinates(self):
        root = ET.fromstring(generate_svg())
        elements = {
            element.attrib.get("id"): element for element in root.iter()
        }
        for feature in PANEL_FEATURES:
            element = elements[f'cutout-{feature["id"].replace("_", "-")}']
            expected_x = LABEL["bleed"] + BOX["width"] - feature["x"]
            expected_y = feature["y"] + LABEL["bleed"]
            if feature["kind"] == "rect":
                actual_x = float(element.attrib["x"]) + float(element.attrib["width"]) / 2
                actual_y = float(element.attrib["y"]) + float(element.attrib["height"]) / 2
            else:
                actual_x = float(element.attrib["cx"])
                actual_y = float(element.attrib["cy"])
                if feature["kind"] == "circle":
                    self.assertAlmostEqual(
                        float(element.attrib["r"]), feature["radius"]
                    )
            self.assertAlmostEqual(actual_x, expected_x)
            self.assertAlmostEqual(actual_y, expected_y)

    def test_preview_renders_fire_engine_illustration(self):
        image = draw_preview()
        fire_engine_red = ImageColor.getrgb("#D94B3D")
        fire_engine_panel = image.crop((100, 1000, 900, 1800))
        red_pixels = sum(pixel == fire_engine_red for pixel in fire_engine_panel.getdata())
        self.assertGreater(red_pixels, 1000)

    def test_labels_clear_real_component_bezels_by_two_mm(self):
        root = ET.fromstring(generate_svg())
        text_elements = {
            element.text: element for element in root.iter() if element.tag.endswith("text")
        }
        component_bottoms = {
            "LAMP": 75.5,
            "BULB": 75.5,
            "BEACON": 75.5,
            "ON/OFF": 141.0,
            "DIMMER": 146.0,
            "FIRE ENGINE": 148.5,
        }
        draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        for label, component_bottom in component_bottoms.items():
            element = text_elements[label]
            size_mm = float(element.attrib["font-size"])
            label_font = font(size_mm, bold=True)
            baseline = (px(float(element.attrib["x"])), px(float(element.attrib["y"])))
            box = draw.textbbox(baseline, label, font=label_font, anchor="mm")
            label_top_mm = box[1] / (300 / 25.4)
            self.assertGreaterEqual(
                label_top_mm - component_bottom,
                2.0,
                f"{label} component bezelinin fazla yakınında",
            )

    def test_bottom_labels_stay_inside_three_mm_trim_safe_area(self):
        image = draw_preview()
        ink = ImageColor.getrgb("#27364B")
        safe_bottom = px(159)
        for label, x1, x2 in (
            ("ON/OFF", 28, 56),
            ("DIMMER", 88, 116),
            ("FIRE ENGINE", 148, 176),
        ):
            crop = image.crop((px(x1), px(154), px(x2), px(162)))
            ink_rows = [
                y
                for y in range(crop.height)
                for x in range(crop.width)
                if crop.getpixel((x, y)) == ink
            ]
            self.assertGreater(len(ink_rows), 100, f"{label} etiketi bulunamadı")
            self.assertLessEqual(
                px(154) + max(ink_rows),
                safe_bottom,
                f"{label} kesim güvenli alanının dışında",
            )


if __name__ == "__main__":
    unittest.main()

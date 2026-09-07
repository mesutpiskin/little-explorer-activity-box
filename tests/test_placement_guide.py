import pathlib
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

from PIL import Image


class PlacementGuideTest(unittest.TestCase):
    def test_generator_creates_printable_svg_and_png(self):
        generator = pathlib.Path("tools/generate_placement_guide.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(generator)],
                cwd=directory,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            svg_path = pathlib.Path(directory) / "docs/component-placement-guide.svg"
            png_path = pathlib.Path(directory) / "docs/component-placement-guide.png"
            self.assertTrue(svg_path.exists())
            self.assertTrue(png_path.exists())

            root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
            self.assertEqual(root.attrib["width"], "320mm")
            self.assertEqual(root.attrib["height"], "230mm")
            with Image.open(png_path) as image:
                self.assertEqual(image.size, (3780, 2717))

    def test_guide_covers_front_side_and_back_components(self):
        guide = pathlib.Path("docs/component-placement-guide.svg")
        self.assertTrue(guide.exists())
        text = guide.read_text(encoding="utf-8")
        for label in (
            "RED 10 mm LED",
            "RED DC184",
            "YELLOW 10 mm LED",
            "YELLOW DC184",
            "GREEN 10 mm LED",
            "BLACK DC180",
            "BLUE 10 mm LED",
            "DC131A",
            "WHITE 10 mm LED",
            "1K POT + DIAL",
            "12 mm ACTIVE BUZZER",
            "BLUE DC180",
            "DC120 2P",
            "2×AA BATTERY HOLDER ×2",
            "FRONT VIEW",
            "RIGHT SIDE",
            "BACK PLATE",
        ):
            self.assertIn(label, text)

    def test_front_numbers_follow_the_box_exterior_view(self):
        root = ET.parse("docs/component-placement-guide.svg").getroot()
        elements = {element.attrib.get("id"): element for element in root.iter()}
        red_led = next(iter(elements["placement-red_led"]))
        green_led = next(iter(elements["placement-green_led"]))
        self.assertAlmostEqual(float(red_led.attrib["cx"]), 162.0)
        self.assertAlmostEqual(float(green_led.attrib["cx"]), 54.0)

    def test_public_guides_display_the_placement_image(self):
        for path in ("README.md", "docs/assembly.md"):
            text = pathlib.Path(path).read_text(encoding="utf-8")
            self.assertIn("component-placement-guide.png", text)

    def test_docs_target_generates_placement_guide(self):
        result = subprocess.run(
            ["make", "-n", "docs"], check=True, capture_output=True, text=True
        )
        self.assertIn("tools/generate_placement_guide.py", result.stdout)


if __name__ == "__main__":
    unittest.main()

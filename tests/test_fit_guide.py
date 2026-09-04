import pathlib
import subprocess
import unittest
import xml.etree.ElementTree as ET

from PIL import Image


class FitGuideTest(unittest.TestCase):
    def test_guide_files_are_generated(self):
        svg_path = pathlib.Path("docs/component-fit-test-guide.svg")
        png_path = pathlib.Path("docs/component-fit-test-guide.png")
        self.assertTrue(svg_path.exists())
        self.assertTrue(png_path.exists())
        root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
        self.assertEqual(root.attrib["width"], "240mm")
        self.assertEqual(root.attrib["height"], "130mm")
        with Image.open(png_path) as image:
            self.assertEqual(image.size, (2835, 1535))

    def test_guide_names_every_fit_area_and_size(self):
        text = pathlib.Path("docs/component-fit-test-guide.svg").read_text(
            encoding="utf-8"
        )
        for label in (
            "10 mm LED",
            "DC184",
            "DC180",
            "DC131A",
            "12 mm AKTİF BUZZER",
            "POT BURCU",
            "POT MİLİ",
            "DC120",
            "ÇARK AÇIKLIĞI",
            "10,0",
            "10,2",
            "12,0",
            "12,2",
            "16,0",
            "16,2",
            "20,0",
            "20,2",
            "5,8",
            "6,0",
            "6,2",
            "19,0×13,0",
            "19,4×13,4",
            "Ø34,0",
        ):
            self.assertIn(label, text)

    def test_docs_target_generates_fit_guide(self):
        result = subprocess.run(
            ["make", "-n", "docs"], check=True, capture_output=True, text=True
        )
        self.assertIn("tools/generate_fit_guide.py", result.stdout)

    def test_readme_displays_fit_guide(self):
        text = pathlib.Path("README.md").read_text(encoding="utf-8")
        self.assertIn("![Komponent test plakası kılavuzu]", text)
        self.assertIn("docs/component-fit-test-guide.png", text)


if __name__ == "__main__":
    unittest.main()

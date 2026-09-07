import pathlib
import subprocess
import sys
import tempfile
import time
import unittest
import xml.etree.ElementTree as ET

from tools.generate_artwork import font as artwork_font
from tools.generate_fit_guide import font as fit_guide_font
from tools.generate_placement_guide import font as placement_guide_font


ROOT = pathlib.Path(__file__).resolve().parents[1]


class LocalizationTest(unittest.TestCase):
    def run_generator(self, name, directory):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / name)],
            cwd=directory,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_generators_publish_complete_english_and_turkish_sets(self):
        with tempfile.TemporaryDirectory() as directory:
            for generator in (
                "generate_artwork.py",
                "generate_docs.py",
                "generate_fit_guide.py",
                "generate_placement_guide.py",
            ):
                self.run_generator(generator, directory)

            generated = pathlib.Path(directory)
            expected = (
                "artwork/activity-box-label.svg",
                "artwork/activity-box-label-preview.png",
                "artwork/activity-box-label-a4.pdf",
                "artwork/tr/activity-box-label.svg",
                "artwork/tr/activity-box-label-preview.png",
                "artwork/tr/activity-box-label-a4.pdf",
                "docs/assembly.md",
                "docs/BOM.csv",
                "docs/circuit.svg",
                "docs/component-fit-test-guide.svg",
                "docs/component-placement-guide.svg",
                "docs/tr/assembly.md",
                "docs/tr/BOM.csv",
                "docs/tr/circuit.svg",
                "docs/tr/component-fit-test-guide.svg",
                "docs/tr/component-placement-guide.svg",
            )
            missing = [path for path in expected if not (generated / path).exists()]
            self.assertEqual(missing, [])

    def test_artwork_locales_keep_identical_cutout_geometry(self):
        with tempfile.TemporaryDirectory() as directory:
            self.run_generator("generate_artwork.py", directory)
            generated = pathlib.Path(directory) / "artwork"
            turkish_path = generated / "tr/activity-box-label.svg"
            self.assertTrue(turkish_path.exists())
            english = ET.parse(generated / "activity-box-label.svg").getroot()
            turkish = ET.parse(turkish_path).getroot()

            def cutouts(root):
                return {
                    element.attrib["id"]: {
                        key: value
                        for key, value in element.attrib.items()
                        if key in {"x", "y", "cx", "cy", "r", "width", "height"}
                    }
                    for element in root.iter()
                    if element.attrib.get("id", "").startswith("cutout-")
                }

            self.assertEqual(cutouts(english), cutouts(turkish))
            english_text = (generated / "activity-box-label.svg").read_text(
                encoding="utf-8"
            )
            turkish_text = (generated / "tr/activity-box-label.svg").read_text(
                encoding="utf-8"
            )
            self.assertIn(">FIRE ENGINE</text>", english_text)
            self.assertIn(">İTFAİYE</text>", turkish_text)

    def test_generated_guides_use_the_selected_language(self):
        with tempfile.TemporaryDirectory() as directory:
            for generator in (
                "generate_docs.py",
                "generate_fit_guide.py",
                "generate_placement_guide.py",
            ):
                self.run_generator(generator, directory)

            docs = pathlib.Path(directory) / "docs"
            self.assertIn(
                "COMPONENT FIT TEST GUIDE",
                (docs / "component-fit-test-guide.svg").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "KOMPONENT UYUM TESTİ KILAVUZU",
                (docs / "tr/component-fit-test-guide.svg").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertIn(
                "COMPONENT PLACEMENT",
                (docs / "component-placement-guide.svg").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertIn(
                "Use this front-view layout",
                (docs / "component-placement-guide.svg").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertIn(
                "BİLEŞEN YERLEŞİMİ",
                (docs / "tr/component-placement-guide.svg").read_text(
                    encoding="utf-8"
                ),
            )
            self.assertIn(
                "Assembly and verification guide",
                (docs / "assembly.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Montaj ve kontrol kılavuzu",
                (docs / "tr/assembly.md").read_text(encoding="utf-8"),
            )

    def test_artwork_pdf_generation_is_reproducible(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            self.run_generator("generate_artwork.py", first)
            time.sleep(1.1)
            self.run_generator("generate_artwork.py", second)
            for relative in (
                "artwork/activity-box-label-a4.pdf",
                "artwork/tr/activity-box-label-a4.pdf",
            ):
                self.assertEqual(
                    (pathlib.Path(first) / relative).read_bytes(),
                    (pathlib.Path(second) / relative).read_bytes(),
                )

    def test_raster_generators_use_the_bundled_font(self):
        for factory in (artwork_font, fit_guide_font, placement_guide_font):
            selected = pathlib.Path(factory(3, bold=True).path).resolve()
            self.assertIn("assets/fonts", selected.as_posix())

    def test_svg_generators_reference_the_bundled_fonts(self):
        with tempfile.TemporaryDirectory() as directory:
            for generator in (
                "generate_artwork.py",
                "generate_docs.py",
                "generate_fit_guide.py",
                "generate_placement_guide.py",
            ):
                self.run_generator(generator, directory)

            generated = pathlib.Path(directory)
            for relative in (
                "artwork/activity-box-label.svg",
                "docs/circuit.svg",
                "docs/component-fit-test-guide.svg",
                "docs/component-placement-guide.svg",
            ):
                text = (generated / relative).read_text(encoding="utf-8")
                self.assertIn("../assets/fonts/DejaVuSans.ttf", text)
                self.assertIn("../assets/fonts/DejaVuSans-Bold.ttf", text)
            for relative in (
                "artwork/tr/activity-box-label.svg",
                "docs/tr/circuit.svg",
                "docs/tr/component-fit-test-guide.svg",
                "docs/tr/component-placement-guide.svg",
            ):
                text = (generated / relative).read_text(encoding="utf-8")
                self.assertIn("../../assets/fonts/DejaVuSans.ttf", text)
                self.assertIn("../../assets/fonts/DejaVuSans-Bold.ttf", text)


if __name__ == "__main__":
    unittest.main()

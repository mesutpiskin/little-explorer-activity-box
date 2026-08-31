import pathlib
import unittest

from PIL import Image
from PIL import ImageColor


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


if __name__ == "__main__":
    unittest.main()

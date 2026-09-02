import csv
import pathlib
import re
import unittest


class DocumentationTest(unittest.TestCase):
    def test_public_readme_leads_the_builder_through_the_project(self):
        text = pathlib.Path("README.md").read_text(encoding="utf-8")
        steps = (
            "1. Malzemeleri hazırlayın",
            "2. Önce test parçalarını basın",
            "3. Ana parçaları basın",
            "4. Etiketi hazırlayın",
            "5. Bileşenleri yerleştirin",
            "6. Devreyi bağlayın",
            "7. Test edin ve kapatın",
        )
        positions = [text.index(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for component in ("DC184", "DC180", "DC131A", "DC120", "330 Ω", "2×AA"):
            self.assertIn(component, text)

    def test_public_readme_relative_links_exist(self):
        root = pathlib.Path(".")
        text = (root / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^]]*\]\(([^)#]+)(?:#[^)]+)?\)", text)
        self.assertGreater(len(links), 5)
        for link in links:
            self.assertTrue((root / link).exists(), f"README bağlantısı eksik: {link}")

    def test_raw_inventory_and_reference_photo_are_not_published(self):
        self.assertFalse(pathlib.Path("docs/items.txt").exists())
        self.assertFalse(pathlib.Path("docs/example.png").exists())
        self.assertFalse(pathlib.Path("docs/superpowers").exists())

    def test_bom_contains_safety_parts(self):
        with pathlib.Path("docs/BOM.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        names = {row["parca"] for row in rows}
        self.assertTrue(
            {
                "2xAA yarı kapalı pil yuvası",
                "1 A sigorta",
                "330 ohm 1 W direnç",
                "DC184 anlık buton",
                "DC180 anlık buton",
            }
            <= names
        )

    def test_bom_uses_repository_line_endings(self):
        data = pathlib.Path("docs/BOM.csv").read_bytes()
        self.assertNotIn(b"\r\n", data)

    def test_assembly_contains_measured_checks(self):
        text = pathlib.Path("docs/assembly.md").read_text(encoding="utf-8")
        for phrase in (
            "20 mA",
            "kısa devre",
            "20 mm kontrol karesi",
            "iki servis mandalı",
            "iki pil yuvasını seri",
            "DC184",
            "DC180",
        ):
            self.assertIn(phrase, text)

    def test_circuit_contains_all_six_branches(self):
        text = pathlib.Path("docs/circuit.svg").read_text(encoding="utf-8")
        for branch in (
            "KIRMIZI",
            "SARI",
            "YEŞİL",
            "AÇ/KAPA",
            "DİMMER",
            "SES",
        ):
            self.assertIn(branch, text)
        self.assertIn("330 Ω", text)
        self.assertIn("2×AA", text)

    def test_assembly_excludes_unsafe_or_unused_connections(self):
        text = pathlib.Path("docs/assembly.md").read_text(encoding="utf-8")
        for phrase in (
            "DC131A'nın 12 V lamba ucu boş kalır",
            "breadboard kullanmayın",
            "nötr kürlenen silikon",
        ):
            self.assertIn(phrase, text)

    def test_circuit_uses_compact_text_inside_battery_holders(self):
        text = pathlib.Path("docs/circuit.svg").read_text(encoding="utf-8")
        self.assertIn(".power{font-size:13px", text)
        self.assertEqual(text.count('class="power"'), 2)

    def test_circuit_draws_each_led_resistor_as_an_inline_part(self):
        text = pathlib.Path("docs/circuit.svg").read_text(encoding="utf-8")
        self.assertEqual(text.count('class="series-resistor"'), 5)
        self.assertEqual(text.count('class="series-led"'), 5)


if __name__ == "__main__":
    unittest.main()

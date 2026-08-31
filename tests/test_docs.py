import csv
import pathlib
import unittest


class DocumentationTest(unittest.TestCase):
    def test_bom_contains_safety_parts(self):
        with pathlib.Path("docs/BOM.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        names = {row["parca"] for row in rows}
        self.assertTrue(
            {"4xAA pil yuvası", "1 A sigorta", "220 ohm direnç"} <= names
        )

    def test_assembly_contains_measured_checks(self):
        text = pathlib.Path("docs/assembly.md").read_text(encoding="utf-8")
        for phrase in (
            "20 mA",
            "kısa devre",
            "20 mm kontrol karesi",
            "iki servis mandalı",
        ):
            self.assertIn(phrase, text)

    def test_circuit_contains_all_six_branches(self):
        text = pathlib.Path("docs/circuit.svg").read_text(encoding="utf-8")
        for branch in (
            "KIRMIZI",
            "SARI",
            "TURUNCU",
            "AÇ/KAPA",
            "DİMMER",
            "SES",
        ):
            self.assertIn(branch, text)


if __name__ == "__main__":
    unittest.main()

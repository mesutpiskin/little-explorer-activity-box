import csv
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest


class DocumentationTest(unittest.TestCase):
    def test_public_entry_points_are_bilingual_and_generic(self):
        english_path = pathlib.Path("README.md")
        turkish_path = pathlib.Path("README.tr.md")
        self.assertTrue(turkish_path.exists())
        english = english_path.read_text(encoding="utf-8")
        turkish = turkish_path.read_text(encoding="utf-8")

        self.assertIn("English", english)
        self.assertIn("Türkçe", english)
        self.assertIn("Build order", english)
        self.assertIn("Yapım sırası", turkish)
        self.assertIn("README.tr.md", english)
        self.assertIn("README.md", turkish)

        public_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (english_path, turkish_path, pathlib.Path("output/stl/README.md"))
        )
        for private_phrase in ("şirket " + "bilgisayarı", "/" + "Users/"):
            self.assertNotIn(private_phrase.casefold(), public_text.casefold())

    def test_open_source_policy_files_define_license_scope(self):
        expected = (
            pathlib.Path("LICENSE"),
            pathlib.Path("LICENSES/MIT.txt"),
            pathlib.Path("LICENSES/README.md"),
            pathlib.Path("LICENSES/README.tr.md"),
            pathlib.Path("CONTRIBUTING.md"),
            pathlib.Path("CONTRIBUTING.tr.md"),
        )
        self.assertEqual([str(path) for path in expected if not path.exists()], [])
        scope = pathlib.Path("LICENSES/README.md").read_text(encoding="utf-8")
        self.assertIn("CERN-OHL-P-2.0", scope)
        self.assertIn("MIT", scope)

    def test_public_readme_leads_the_builder_through_the_project(self):
        text = pathlib.Path("README.md").read_text(encoding="utf-8")
        steps = (
            "1. Prepare the parts",
            "2. Print the test parts first",
            "3. Print the enclosure",
            "4. Print and apply the label",
            "5. Install the components",
            "6. Wire the circuit",
            "7. Verify and close",
        )
        positions = [text.index(step) for step in steps]
        self.assertEqual(positions, sorted(positions))
        for component in ("DC184", "DC180", "DC131A", "DC120", "330 Ω", "2×AA"):
            self.assertIn(component, text)

    def test_public_readme_relative_links_exist(self):
        root = pathlib.Path(".")
        for readme in ("README.md", "README.tr.md"):
            text = (root / readme).read_text(encoding="utf-8")
            links = re.findall(r"\[[^]]*\]\(([^)#]+)(?:#[^)]+)?\)", text)
            self.assertGreater(len(links), 5)
            for link in links:
                self.assertTrue(
                    (root / link).exists(), f"Missing link in {readme}: {link}"
                )

    def test_raw_inventory_and_reference_photo_are_not_published(self):
        self.assertFalse(pathlib.Path("docs/items.txt").exists())
        self.assertFalse(pathlib.Path("docs/example.png").exists())
        self.assertFalse(pathlib.Path("docs/superpowers").exists())
        public_guides = "\n".join(
            pathlib.Path(path).read_text(encoding="utf-8")
            for path in (
                "README.md",
                "README.tr.md",
                "docs/assembly.md",
                "docs/tr/assembly.md",
            )
        )
        for inventory_reference in (
            "DHT11",
            "Parts intentionally not used",
            "Bilerek kullanılmayan parçalar",
        ):
            self.assertNotIn(inventory_reference, public_guides)

    def test_bom_contains_safety_parts(self):
        with pathlib.Path("docs/BOM.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        names = {row["part"] for row in rows}
        self.assertTrue(
            {
                "2×AA semi-enclosed battery holder",
                "1 A fuse",
                "330 ohm 1 W resistor",
                "DC184 momentary push button",
                "DC180 momentary push button",
                "AA alkaline battery",
            }
            <= names
        )

    def test_bom_uses_repository_line_endings(self):
        data = pathlib.Path("docs/BOM.csv").read_bytes()
        self.assertNotIn(b"\r\n", data)

    def test_generated_bom_uses_public_four_column_schema(self):
        generator = pathlib.Path("tools/generate_docs.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [sys.executable, str(generator)],
                cwd=directory,
                check=True,
                capture_output=True,
                text=True,
            )
            with (pathlib.Path(directory) / "docs/BOM.csv").open(
                encoding="utf-8-sig"
            ) as handle:
                rows = list(csv.reader(handle))
            bom_bytes = (pathlib.Path(directory) / "docs/BOM.csv").read_bytes()

        self.assertEqual(rows[0], ["quantity", "part", "specification", "use"])
        self.assertTrue(all(len(row) == 4 for row in rows))
        self.assertEqual(
            rows[-1],
            ["print", "approximately 450 g", "1.75 mm PETG filament", "Body, back plate, and dial"],
        )
        self.assertFalse(bom_bytes.startswith(b"\xef\xbb\xbf"))

    def test_assembly_contains_measured_checks(self):
        text = pathlib.Path("docs/assembly.md").read_text(encoding="utf-8")
        for phrase in (
            "20 mA",
            "no short",
            "control square measures exactly 20 mm",
            "service latches are pressed",
            "connect the holders in series",
            "DC184",
            "DC180",
        ):
            self.assertIn(phrase, text)

    def test_circuit_contains_all_six_branches(self):
        text = pathlib.Path("docs/circuit.svg").read_text(encoding="utf-8")
        for branch in (
            "RED",
            "YELLOW",
            "GREEN",
            "ON/OFF",
            "DIMMER",
            "SOUND",
        ):
            self.assertIn(branch, text)
        self.assertIn("330 Ω", text)
        self.assertIn("2×AA", text)

    def test_assembly_excludes_unsafe_or_unused_connections(self):
        text = pathlib.Path("docs/assembly.md").read_text(encoding="utf-8")
        for phrase in (
            "Leave the DC131A 12 V lamp terminal disconnected",
            "Do not leave breadboards",
            "neutral-cure silicone",
        ):
            self.assertIn(phrase, text)

    def test_safety_inspection_is_required_before_every_use(self):
        english = "\n".join(
            pathlib.Path(path).read_text(encoding="utf-8")
            for path in ("README.md", "docs/assembly.md")
        )
        turkish = "\n".join(
            pathlib.Path(path).read_text(encoding="utf-8")
            for path in ("README.tr.md", "docs/tr/assembly.md")
        )
        self.assertGreaterEqual(english.casefold().count("before each use"), 2)
        self.assertGreaterEqual(turkish.casefold().count("her kullanımdan önce"), 2)

    def test_stl_readmes_document_print_orientation(self):
        english = pathlib.Path("output/stl/README.md").read_text(encoding="utf-8")
        turkish = pathlib.Path("output/stl/README.tr.md").read_text(encoding="utf-8")
        for phrase in ("front face down", "outer face down", "flange down"):
            self.assertIn(phrase, english)
        for phrase in ("ön yüzü tablaya", "dış yüzü tablaya", "flanşı tablaya"):
            self.assertIn(phrase, turkish)

    def test_turkish_contributing_uses_turkish_license_scope(self):
        text = pathlib.Path("CONTRIBUTING.tr.md").read_text(encoding="utf-8")
        self.assertIn("LICENSES/README.tr.md", text)

    def test_makefile_supports_cli_and_macos_openscad_installs(self):
        text = pathlib.Path("Makefile").read_text(encoding="utf-8")
        self.assertIn("command -v openscad", text)
        self.assertIn("/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD", text)

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

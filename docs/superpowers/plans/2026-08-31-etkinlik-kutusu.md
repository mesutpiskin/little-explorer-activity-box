# Etkinlik Kutusu Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a printable, screw-free activity-box model, aligned sticker artwork, wiring diagram, bill of materials, and Turkish assembly instructions for the approved six-activity design.

**Architecture:** A small Python geometry contract is the single source for panel coordinates and electrical values. It generates an OpenSCAD dimensions include, then OpenSCAD generates the enclosure parts while separate Python generators create the dimensionally aligned SVG/PNG/PDF artwork and documentation artifacts. A standard-library validator checks dimensions, electrical limits, file signatures, and STL topology/bounds.

**Tech Stack:** Python 3 standard library, Pillow 11+, OpenSCAD CLI, SVG 1.1, ASCII/binary STL, Markdown, CSV.

**Spec:** `docs/superpowers/specs/2026-08-31-etkinlik-kutusu-design.md`

## Global Constraints

- Overall enclosure size is exactly 200 × 160 × 52 mm with 14 mm corner radius.
- The front panel uses the coordinates and default cutouts in the approved spec.
- Power is 4×AA alkaline through a 1 A fuse and the recessed SS12F15 master switch; no lithium cell is used.
- Every LED branch has at least 220 ohm fixed resistance; calculated current must remain below 20 mA at 6.4 V.
- The back is screw-free and requires both recessed service latches to be released.
- LED holders and the rotary dial must be mechanically captive from behind.
- The label is 204 × 164 mm including 2 mm bleed and has a 200 × 160 mm trim line.
- No final artifact may contain a TODO/TBD placeholder.
- This directory is not a Git repository, so commit steps are intentionally omitted.

---

### Task 1: Shared design contract and baseline validation

**Files:**
- Create: `tools/project_spec.py`
- Create: `tools/generate_dimensions.py`
- Create: `tools/validate_outputs.py`
- Create: `tests/test_project_spec.py`
- Create: `Makefile`

**Interfaces:**
- Produces: `BOX`, `PANEL_FEATURES`, `ELECTRICAL`, and `LABEL` dictionaries from `tools.project_spec`.
- Produces: `cad/generated_dimensions.scad` with OpenSCAD scalar/list assignments.
- Produces: `python3 tools/validate_outputs.py` as the final artifact validator.

- [ ] **Step 1: Write contract tests**

```python
import unittest
from tools.project_spec import BOX, ELECTRICAL, LABEL, PANEL_FEATURES

class ProjectSpecTest(unittest.TestCase):
    def test_envelope_fits_print_bed(self):
        self.assertEqual((BOX["width"], BOX["height"], BOX["depth"]), (200, 160, 52))
        self.assertLessEqual(max(BOX["width"], BOX["height"]), 220)

    def test_led_currents_are_below_twenty_milliamps(self):
        for vf in ELECTRICAL["led_forward_voltages"].values():
            self.assertLess((ELECTRICAL["supply_max"] - vf) / ELECTRICAL["resistor"], 0.0201)

    def test_features_have_safe_margin(self):
        for feature in PANEL_FEATURES:
            self.assertGreaterEqual(feature["x"] - feature["radius"], 8)
            self.assertGreaterEqual(feature["y"] - feature["radius"], 8)
            self.assertLessEqual(feature["x"] + feature["radius"], BOX["width"] - 8)
            self.assertLessEqual(feature["y"] + feature["radius"], BOX["height"] - 8)

    def test_label_bleed(self):
        self.assertEqual((LABEL["width"], LABEL["height"], LABEL["bleed"]), (204, 164, 2))
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `python3 -m unittest tests/test_project_spec.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'tools.project_spec'`.

- [ ] **Step 3: Implement the exact dictionaries and dimensions generator**

`project_spec.py` defines the approved dimensions and the five LED forward-voltage assumptions: red 2.0 V, yellow 2.1 V, orange 2.1 V, and two white LEDs at 3.0 V. `generate_dimensions.py` serializes box dimensions, wall/panel thickness, feature centers, button diameter, rocker size, dial opening, buzzer hole pattern, and snap tolerance to valid OpenSCAD assignments.

- [ ] **Step 4: Add Makefile targets**

```make
dimensions:
	python3 tools/generate_dimensions.py

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 tools/validate_outputs.py
```

- [ ] **Step 5: Run baseline tests**

Run: `make dimensions test`

Expected: all contract tests PASS and `cad/generated_dimensions.scad` exists.

---

### Task 2: Parametric enclosure, back, captive dial, and fit coupon

**Files:**
- Create: `cad/activity_box.scad`
- Consume: `cad/generated_dimensions.scad`
- Modify: `Makefile`
- Test: `tests/test_cad_source.py`

**Interfaces:**
- Consumes: generated OpenSCAD names from Task 1.
- Produces: modules `body()`, `back()`, `dial()`, and `snap_fit_test()` selected by `part`.
- Produces: four STL files under `output/stl/`.

- [ ] **Step 1: Write source-structure tests**

```python
import pathlib, unittest

class CadSourceTest(unittest.TestCase):
    def test_required_modules_and_generated_include(self):
        text = pathlib.Path("cad/activity_box.scad").read_text()
        self.assertIn("include <generated_dimensions.scad>", text)
        for name in ("body", "back", "dial", "snap_fit_test"):
            self.assertIn(f"module {name}(", text)
```

- [ ] **Step 2: Verify the source test fails**

Run: `python3 -m unittest tests/test_cad_source.py -v`

Expected: FAIL because `cad/activity_box.scad` is absent.

- [ ] **Step 3: Implement the enclosure geometry**

Create a rounded rectangular shell with 2.6 mm walls and 3.2 mm front; subtract the specified LED, button, rocker, dial, buzzer, and side master-switch openings. Add rear LED capture guards, buzzer cup, wiring clips, the maximum 112 × 26 × 18 mm slim inline battery-holder bay between the two control rows, and cable channels. Use Minkowski/offset geometry only where it does not produce zero-thickness faces.

- [ ] **Step 4: Implement the screw-free closure and dial**

The back uses a perimeter tongue with 0.25 mm per-side clearance and four inward clips. Two opposite locking clips align with 3 mm × 12 mm service passages. The dial is inserted from behind, has a 46 mm captive flange, a 32 mm front grip that passes through the 34 mm opening, and a 6.2 mm D-shaft socket. The fit coupon reproduces one tongue, groove, latch, and service passage.

- [ ] **Step 5: Add STL build commands**

```make
stl: dimensions
	mkdir -p output/stl
	openscad -o output/stl/activity-box-body.stl -D 'part="body"' cad/activity_box.scad
	openscad -o output/stl/activity-box-back.stl -D 'part="back"' cad/activity_box.scad
	openscad -o output/stl/activity-box-dial.stl -D 'part="dial"' cad/activity_box.scad
	openscad -o output/stl/snap-fit-test.stl -D 'part="snap_test"' cad/activity_box.scad
```

- [ ] **Step 6: Install OpenSCAD only if the CLI remains unavailable**

Run: `brew install --cask openscad`

Expected: `/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD` exists; create a Makefile `OPENSCAD` fallback to that executable when `openscad` is not on PATH.

- [ ] **Step 7: Generate and inspect the STL files**

Run: `make stl`

Expected: four non-empty STL files and no OpenSCAD geometry errors.

---

### Task 3: Dimensionally aligned sticker artwork

**Files:**
- Create: `tools/generate_artwork.py`
- Create: `tests/test_artwork.py`
- Modify: `Makefile`
- Generate: `artwork/activity-box-label.svg`
- Generate: `artwork/activity-box-label-a4.pdf`
- Generate: `artwork/activity-box-label-preview.png`

**Interfaces:**
- Consumes: `BOX`, `LABEL`, and `PANEL_FEATURES` from `tools.project_spec`.
- Produces: an SVG with millimetre dimensions, a 300 dpi preview, and an A4 300 dpi PDF.

- [ ] **Step 1: Write artwork metadata tests**

```python
import pathlib, unittest
from PIL import Image

class ArtworkTest(unittest.TestCase):
    def test_svg_has_exact_physical_size_and_trim(self):
        text = pathlib.Path("artwork/activity-box-label.svg").read_text()
        self.assertIn('width="204mm"', text)
        self.assertIn('height="164mm"', text)
        self.assertIn('id="trim-line"', text)

    def test_preview_is_300_dpi_size(self):
        with Image.open("artwork/activity-box-label-preview.png") as image:
            self.assertEqual(image.size, (2409, 1937))
```

- [ ] **Step 2: Verify tests fail before generation**

Run: `python3 -m unittest tests/test_artwork.py -v`

Expected: FAIL because artwork files are absent.

- [ ] **Step 3: Generate the vector label**

Draw six rounded pastel station panels on a warm cream background. Add deterministic vector symbols for light rays, power, brightness, and sound. Add centered cut guides from `PANEL_FEATURES`, a 200 × 160 mm trim line offset by the 2 mm bleed, and a 20 mm calibration square outside the trim but inside the printable page workflow.

- [ ] **Step 4: Generate 300 dpi PNG and A4 PDF**

Use Pillow drawing primitives with the same millimetre-to-pixel conversion (`300 / 25.4`) rather than rasterizing the SVG. Place the 204 × 164 mm label at 100% size on a 210 × 297 mm white A4 canvas and save with `resolution=300.0`.

- [ ] **Step 5: Run artwork tests**

Run: `python3 tools/generate_artwork.py && python3 -m unittest tests/test_artwork.py -v`

Expected: all artwork tests PASS.

---

### Task 4: Wiring diagram, BOM, and assembly guide

**Files:**
- Create: `tools/generate_docs.py`
- Create: `tests/test_docs.py`
- Modify: `Makefile`
- Generate: `docs/circuit.svg`
- Generate: `docs/BOM.csv`
- Generate: `docs/assembly.md`

**Interfaces:**
- Consumes: `ELECTRICAL` and feature names from `tools.project_spec`.
- Produces: a color-coded parallel-branch schematic, procurement-ready CSV, and ordered Turkish instructions.

- [ ] **Step 1: Write documentation tests**

```python
import csv, pathlib, unittest

class DocumentationTest(unittest.TestCase):
    def test_bom_contains_safety_parts(self):
        rows = list(csv.DictReader(pathlib.Path("docs/BOM.csv").open()))
        names = {row["parca"] for row in rows}
        self.assertTrue({"4xAA pil yuvası", "1 A sigorta", "220 ohm direnç"} <= names)

    def test_assembly_contains_measured_checks(self):
        text = pathlib.Path("docs/assembly.md").read_text()
        for phrase in ("20 mA", "kısa devre", "20 mm kontrol karesi", "iki servis mandalı"):
            self.assertIn(phrase, text)
```

- [ ] **Step 2: Verify tests fail before generation**

Run: `python3 -m unittest tests/test_docs.py -v`

Expected: FAIL because generated documents are absent.

- [ ] **Step 3: Generate the exact wiring diagram and BOM**

Draw the fuse and master switch in series before a positive bus, six labeled parallel branches, the correct polarity for five LEDs, the B1K wiper tied to one end terminal, and a common negative bus. BOM rows distinguish available parts from items to buy and include the exact assumed panel cutout dimensions.

- [ ] **Step 4: Generate Turkish assembly instructions**

Document tolerance-coupon printing, physical part measurement before the long print, print settings, label cutting, rear-first component insertion, soldering, continuity/current tests, latch testing, and supervised-use warnings. Include explicit warnings not to substitute the existing 0/1 ohm resistors and not to use loose jumper wires.

- [ ] **Step 5: Run documentation tests**

Run: `python3 tools/generate_docs.py && python3 -m unittest tests/test_docs.py -v`

Expected: all documentation tests PASS.

---

### Task 5: Final artifact validation and visual inspection

**Files:**
- Modify: `tools/validate_outputs.py`
- Modify: `tests/test_project_spec.py`
- Generate: all outputs from Tasks 1–4

**Interfaces:**
- Consumes: every generated output.
- Produces: a non-zero exit on missing, malformed, oversized, non-manifold, or electrically unsafe output.

- [ ] **Step 1: Add failing validator tests for missing artifacts and malformed STL**

Test the STL reader against a minimal valid tetrahedron and against one triangle with open edges. Test that every required artifact path is included in `REQUIRED_OUTPUTS`.

- [ ] **Step 2: Implement STL and artifact validation**

Support binary and ASCII STL parsing; calculate bounds and count rounded undirected edges. Require every edge to occur exactly twice. Confirm body bounds do not exceed 200.2 × 160.2 × 52.2 mm, all outputs are non-empty, SVG physical dimensions are exact, PNG dimensions are exact, PDF begins `%PDF`, and no text artifact contains `TODO` or `TBD`.

- [ ] **Step 3: Run the full reproducible build**

Run: `make clean all test validate`

Expected: four STL files, three artwork files, three documents, all unit tests PASS, and validator ends with `VALIDATION PASSED`.

- [ ] **Step 4: Inspect rendered artifacts**

Open the PNG label preview and OpenSCAD renders of body/back/dial. Confirm every control circle is centered in its colored station, icons do not overlap cutouts, the dial flange is larger than its front opening, LED guards cover each holder, and both service channels reach the locking clips.

- [ ] **Step 5: Record unavoidable fabrication assumptions**

In the final handoff, state that the 24.2 mm button, 21.2 × 15.2 mm rocker, 6 mm D shaft, LED holder, and battery holder are parameter defaults and must be checked with calipers before the full print. Report exact verification commands and their observed results.

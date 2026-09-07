PYTHON ?= python3
OPENSCAD ?= $(shell if command -v openscad >/dev/null 2>&1; then command -v openscad; elif [ -x /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD ]; then echo /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD; else echo openscad; fi)

.PHONY: all dimensions stl artwork docs test validate validate-source clean

all: dimensions stl artwork docs

dimensions:
	$(PYTHON) tools/generate_dimensions.py

test:
	$(PYTHON) -m unittest discover -s tests -v

stl: dimensions
	mkdir -p output/stl
	$(OPENSCAD) -o output/stl/activity-box-body.stl -D 'part="body"' cad/activity_box.scad
	$(OPENSCAD) -o output/stl/activity-box-back.stl -D 'part="back"' cad/activity_box.scad
	$(OPENSCAD) -o output/stl/activity-box-dial.stl -D 'part="dial"' cad/activity_box.scad
	$(OPENSCAD) -o output/stl/snap-fit-test.stl -D 'part="snap_test"' cad/activity_box.scad
	$(OPENSCAD) -o output/stl/component-fit-test.stl -D 'part="component_test"' cad/activity_box.scad

artwork:
	$(PYTHON) tools/generate_artwork.py

docs:
	$(PYTHON) tools/generate_docs.py
	$(PYTHON) tools/generate_fit_guide.py
	$(PYTHON) tools/generate_placement_guide.py

validate:
	$(PYTHON) tools/validate_outputs.py

validate-source:
	$(PYTHON) tools/validate_outputs.py --allow-missing-stl

clean:
	rm -rf output/stl/*.stl artwork/activity-box-label.svg artwork/activity-box-label-a4.pdf artwork/activity-box-label-preview.png artwork/activity-box-assembled-preview.png artwork/tr docs/circuit.svg docs/BOM.csv docs/assembly.md docs/component-fit-test-guide.svg docs/component-fit-test-guide.png docs/component-placement-guide.svg docs/component-placement-guide.png docs/tr cad/generated_dimensions.scad

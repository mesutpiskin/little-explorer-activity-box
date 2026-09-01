PYTHON ?= python3
OPENSCAD ?= $(shell command -v openscad 2>/dev/null || echo /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD)

.PHONY: all dimensions stl artwork docs test validate clean

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

validate:
	$(PYTHON) tools/validate_outputs.py

validate-source:
	$(PYTHON) tools/validate_outputs.py --allow-missing-stl

clean:
	rm -rf output/stl artwork/activity-box-label.svg artwork/activity-box-label-a4.pdf artwork/activity-box-label-preview.png artwork/activity-box-assembled-preview.png docs/circuit.svg docs/BOM.csv docs/assembly.md cad/generated_dimensions.scad

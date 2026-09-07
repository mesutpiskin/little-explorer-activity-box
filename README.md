# Little Explorer Activity Box

[English](README.md) | [Türkçe](README.tr.md)

A no-code, no-PCB activity box that teaches cause and effect through lights,
switches, a dimmer, and sound. The enclosure is parametric, printable on a
standard 3D printer, and closed with serviceable snap fits instead of screws.

![Completed activity box](artwork/activity-box-assembled-preview.png)

> [!WARNING]
> This community hardware project is not a certified toy. A child aged 18
> months must use it only under direct adult supervision. Pull-test every
> exposed component and the back plate before each use. Remove the batteries
> immediately if anything cracks, loosens, leaks, or becomes warm.

## What children can explore

| Activity | Input | Result |
|---|---|---|
| Lamp | Red DC184 button | Red LED lights |
| Bulb | Yellow DC184 button | Yellow LED lights |
| Beacon | Black DC180 button | Green LED lights |
| On/off | DC131A switch | Blue LED stays on or off |
| Dimmer | 1K potentiometer dial | White LED changes brightness |
| Fire engine | Blue DC180 button | Active buzzer sounds |

The six functions are simple parallel branches. No microcontroller,
breadboard, firmware, or custom PCB is required.

## Build order

### 1. Prepare the parts

Core hardware:

| Qty | Part | Purpose |
|---:|---|---|
| 2 | Semi-enclosed 2×AA battery holder | Four AA cells in series |
| 4 | AA alkaline cell | Nominal 6 V supply |
| 2 | DC184 momentary button, red and yellow | Red/yellow LED branches |
| 2 | DC180 momentary button, black and blue | Green LED and buzzer |
| 1 | DC131A 20 mm on/off switch | Blue LED branch |
| 1 | DC120 2P on/off switch | Main power |
| 1 | 1K potentiometer | White LED dimmer |
| 5 | 10 mm LED: red, yellow, green, blue, white | Light outputs |
| 5 | 330 Ω / 1 W resistor | One per LED |
| 1 | 12 mm active buzzer, 5–12 V | Sound output |
| 1 | 1 A fuse with enclosed holder | Battery short-circuit protection |
| — | Stranded wire, heat-shrink, neutral-cure silicone | Safe assembly |
| — | PETG filament | Body, back plate, and dial |

See the printable [bill of materials](docs/BOM.csv) for exact specifications.

### 2. Print the test parts first

Generate the models with:

```sh
make stl
```

Print these before the full enclosure:

- `output/stl/component-fit-test.stl` checks the purchased component sizes.
- `output/stl/snap-fit-test.stl` checks the screwless back-plate clips.

![Component fit-test guide](docs/component-fit-test-guide.png)

The selected defaults are LED Ø10.2 mm, DC184 Ø12.0 mm, DC180 Ø16.0 mm,
DC131A Ø20.2 mm, DC120 19.0×13.0 mm, pot bushing/shaft Ø7.0/Ø6.2 mm,
and a Ø34 mm dial opening. If another fit works better, update
[`tools/project_spec.py`](tools/project_spec.py) and run `make dimensions`.

### 3. Print the enclosure

`make stl` produces:

- `activity-box-body.stl`
- `activity-box-back.stl`
- `activity-box-dial.stl`
- `snap-fit-test.stl`
- `component-fit-test.stl`

Recommended settings: PETG, 0.20 mm layers, at least four walls, five top and
bottom layers, and 25% infill. The captive dial uses a Ø36 mm × 4 mm flange
inside a Ø34 mm panel opening.

### 4. Print and apply the label

Print [the A4 label](artwork/activity-box-label-a4.pdf) at **actual size / 100%**
with “fit to page” and mirror/transfer printing disabled. The control square
must measure exactly 20 mm. Apply the label before installing components.

Editable vector source: [activity-box-label.svg](artwork/activity-box-label.svg).

### 5. Install the components

![Component placement guide](docs/component-placement-guide.png)

Insert LEDs from inside so their wider flange remains captive. Use component
nuts or built-in clips as the primary retainers. Neutral-cure silicone may
support LEDs against vibration but must not be the only mechanical retention.
Keep the buzzer sound holes open.

The complete procedure is in the [assembly guide](docs/assembly.md).

### 6. Wire the circuit

![Wiring diagram](docs/circuit.svg)

Build the supply first, with all batteries removed:

```text
Holder A black ───────────────────────────────────── negative bus
Holder A red ─── Holder B black
Holder B red ─── 1 A fuse ─── DC120 main switch ─── positive bus
```

Then add the six branches in parallel:

```text
Positive → red DC184    → 330 Ω → red LED    → negative
Positive → yellow DC184 → 330 Ω → yellow LED → negative
Positive → black DC180  → 330 Ω → green LED  → negative
Positive → DC131A       → 330 Ω → blue LED   → negative
Positive → 1K pot       → 330 Ω → white LED  → negative
Positive → blue DC180           → active buzzer → negative
```

Use only the two switching contacts on the DC131A; leave its 12 V lamp terminal
disconnected. Identify the contacts with a multimeter instead of assuming pin
order. Join the pot wiper to the outer terminal being used.

### 7. Verify and close

1. With batteries removed, verify there is no short between the buses.
2. Confirm battery current is zero with the DC120 switched off.
3. Test one branch at a time; each LED must stay below 20 mA.
4. Route every insulated wire away from the snap clips.
5. Engage all four back-plate clips.
6. Pull-test every exposed part and the back plate before each use.

## Repository layout

| Path | Contents |
|---|---|
| [`cad/`](cad/activity_box.scad) | Parametric OpenSCAD source |
| [`artwork/`](artwork/activity-box-label.svg) | English printable label and previews |
| [`artwork/tr/`](artwork/tr/activity-box-label.svg) | Turkish printable label and previews |
| [`docs/`](docs/assembly.md) | English assembly, BOM, circuit, and placement guides |
| [`docs/tr/`](docs/tr/assembly.md) | Turkish documentation set |
| [`assets/fonts/`](assets/fonts/LICENSE.txt) | Bundled font and its upstream license for reproducible graphics |
| [`tools/`](tools/project_spec.py) | Shared dimensions and deterministic generators |
| [`tests/`](tests/test_project_spec.py) | Geometry, output, and documentation checks |

## Rebuild and verify

Python 3 and Pillow generate the documents and artwork. OpenSCAD is required
only for STL export.

```sh
python3 -m pip install -r requirements.txt
make dimensions artwork docs
make test
make stl
make validate
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes.

## License

Hardware design, CAD, artwork, and documentation are licensed under
[CERN-OHL-P-2.0](LICENSE). Build scripts and tests are licensed under the
[MIT License](LICENSES/MIT.txt). See [license scope](LICENSES/README.md).

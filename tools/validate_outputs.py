"""Validate generated activity-box artifacts without third-party packages."""

import argparse
from collections import Counter
from pathlib import Path
import re
import struct
import sys

from PIL import Image

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_spec import BOX, ELECTRICAL, LABEL


STL_OUTPUTS = [
    Path("output/stl/activity-box-body.stl"),
    Path("output/stl/activity-box-back.stl"),
    Path("output/stl/activity-box-dial.stl"),
    Path("output/stl/snap-fit-test.stl"),
]

NON_STL_OUTPUTS = [
    Path("cad/activity_box.scad"),
    Path("cad/generated_dimensions.scad"),
    Path("artwork/activity-box-label.svg"),
    Path("artwork/activity-box-label-a4.pdf"),
    Path("artwork/activity-box-label-preview.png"),
    Path("docs/circuit.svg"),
    Path("docs/BOM.csv"),
    Path("docs/assembly.md"),
]

REQUIRED_OUTPUTS = NON_STL_OUTPUTS + STL_OUTPUTS


def read_stl_triangles(path):
    data = Path(path).read_bytes()
    if len(data) >= 84:
        triangle_count = struct.unpack_from("<I", data, 80)[0]
        if 84 + triangle_count * 50 == len(data):
            triangles = []
            offset = 84
            for _ in range(triangle_count):
                values = struct.unpack_from("<12fH", data, offset)
                triangles.append(
                    (
                        tuple(values[3:6]),
                        tuple(values[6:9]),
                        tuple(values[9:12]),
                    )
                )
                offset += 50
            return triangles

    text = data.decode("ascii", errors="strict")
    vertices = [
        tuple(float(value) for value in match)
        for match in re.findall(
            r"vertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)",
            text,
        )
    ]
    if len(vertices) % 3:
        raise ValueError(f"invalid ASCII STL vertex count: {len(vertices)}")
    return [tuple(vertices[index : index + 3]) for index in range(0, len(vertices), 3)]


def normalized_vertex(vertex):
    return tuple(round(float(value), 5) for value in vertex)


def is_closed_manifold(triangles):
    if len(triangles) < 4:
        return False
    edges = Counter()
    for triangle in triangles:
        vertices = [normalized_vertex(vertex) for vertex in triangle]
        for start, end in zip(vertices, vertices[1:] + vertices[:1]):
            edges[tuple(sorted((start, end)))] += 1
    return bool(edges) and all(count == 2 for count in edges.values())


def mesh_bounds(triangles):
    vertices = [vertex for triangle in triangles for vertex in triangle]
    minima = tuple(min(vertex[axis] for vertex in vertices) for axis in range(3))
    maxima = tuple(max(vertex[axis] for vertex in vertices) for axis in range(3))
    return tuple(maxima[axis] - minima[axis] for axis in range(3))


def validate_project(root, allow_missing_stl=False):
    root = Path(root)
    errors = []
    warnings = []

    for relative in NON_STL_OUTPUTS:
        path = root / relative
        if not path.exists() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {relative}")

    missing_stl = [relative for relative in STL_OUTPUTS if not (root / relative).exists()]
    if missing_stl:
        message = "STL export deferred: " + ", ".join(str(path) for path in missing_stl)
        if allow_missing_stl:
            warnings.append(message)
        else:
            errors.append(message)

    for relative in STL_OUTPUTS:
        path = root / relative
        if not path.exists():
            continue
        try:
            triangles = read_stl_triangles(path)
        except (OSError, UnicodeError, ValueError, struct.error) as exc:
            errors.append(f"cannot parse {relative}: {exc}")
            continue
        if not is_closed_manifold(triangles):
            errors.append(f"not a closed two-manifold: {relative}")
        if relative.name == "activity-box-body.stl":
            bounds = mesh_bounds(triangles)
            limits = (BOX["width"] + 0.2, BOX["height"] + 0.2, BOX["depth"] + 0.2)
            if any(actual > limit for actual, limit in zip(bounds, limits)):
                errors.append(f"body exceeds envelope: {bounds}")

    svg_path = root / "artwork/activity-box-label.svg"
    if svg_path.exists():
        svg = svg_path.read_text(encoding="utf-8")
        if f'width="{LABEL["width"]}mm"' not in svg or f'height="{LABEL["height"]}mm"' not in svg:
            errors.append("label SVG physical dimensions are incorrect")

    png_path = root / "artwork/activity-box-label-preview.png"
    if png_path.exists():
        with Image.open(png_path) as image:
            expected = (
                round(LABEL["width"] * LABEL["dpi"] / 25.4),
                round(LABEL["height"] * LABEL["dpi"] / 25.4),
            )
            if image.size != expected:
                errors.append(f"label PNG dimensions {image.size}, expected {expected}")

    pdf_path = root / "artwork/activity-box-label-a4.pdf"
    if pdf_path.exists() and not pdf_path.read_bytes().startswith(b"%PDF"):
        errors.append("A4 label is not a PDF")

    for name, forward_voltage in ELECTRICAL["led_forward_voltages"].items():
        current = (ELECTRICAL["supply_max"] - forward_voltage) / ELECTRICAL["resistor"]
        if current > 0.020:
            errors.append(f"{name} LED current exceeds 20 mA: {current * 1000:.2f} mA")

    text_outputs = [
        Path("cad/activity_box.scad"),
        Path("cad/generated_dimensions.scad"),
        Path("artwork/activity-box-label.svg"),
        Path("docs/circuit.svg"),
        Path("docs/BOM.csv"),
        Path("docs/assembly.md"),
    ]
    for relative in text_outputs:
        path = root / relative
        if path.exists():
            text = path.read_text(encoding="utf-8-sig")
            if re.search(r"\b(?:TODO|TBD)\b", text, flags=re.IGNORECASE):
                errors.append(f"placeholder found in {relative}")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-missing-stl",
        action="store_true",
        help="Allow source-only delivery when OpenSCAD is blocked.",
    )
    args = parser.parse_args()
    errors, warnings = validate_project(Path("."), args.allow_missing_stl)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        raise SystemExit(1)
    suffix = " (STL export deferred)" if warnings else ""
    print(f"VALIDATION PASSED{suffix}")


if __name__ == "__main__":
    main()


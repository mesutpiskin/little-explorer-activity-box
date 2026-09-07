"""Validate generated activity-box artifacts without third-party packages."""

import argparse
from collections import Counter
from pathlib import Path
import re
import subprocess
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
    Path("output/stl/component-fit-test.stl"),
]

NON_STL_OUTPUTS = [
    Path("README.md"),
    Path("README.tr.md"),
    Path("CONTRIBUTING.md"),
    Path("CONTRIBUTING.tr.md"),
    Path("LICENSE"),
    Path("LICENSES/MIT.txt"),
    Path("LICENSES/README.md"),
    Path("LICENSES/README.tr.md"),
    Path("requirements.txt"),
    Path("assets/fonts/DejaVuSans.ttf"),
    Path("assets/fonts/DejaVuSans-Bold.ttf"),
    Path("assets/fonts/LICENSE.txt"),
    Path("media/activity-box-hero.jpg"),
    Path("media/activity-box-demo-poster.jpg"),
    Path("media/activity-box-demo.mp4"),
    Path("cad/activity_box.scad"),
    Path("cad/generated_dimensions.scad"),
    Path("artwork/activity-box-label.svg"),
    Path("artwork/activity-box-label-a4.pdf"),
    Path("artwork/activity-box-label-preview.png"),
    Path("artwork/activity-box-assembled-preview.png"),
    Path("artwork/tr/activity-box-label.svg"),
    Path("artwork/tr/activity-box-label-a4.pdf"),
    Path("artwork/tr/activity-box-label-preview.png"),
    Path("artwork/tr/activity-box-assembled-preview.png"),
    Path("docs/circuit.svg"),
    Path("docs/component-fit-test-guide.svg"),
    Path("docs/component-fit-test-guide.png"),
    Path("docs/component-placement-guide.svg"),
    Path("docs/component-placement-guide.png"),
    Path("docs/BOM.csv"),
    Path("docs/assembly.md"),
    Path("docs/tr/circuit.svg"),
    Path("docs/tr/component-fit-test-guide.svg"),
    Path("docs/tr/component-fit-test-guide.png"),
    Path("docs/tr/component-placement-guide.svg"),
    Path("docs/tr/component-placement-guide.png"),
    Path("docs/tr/BOM.csv"),
    Path("docs/tr/assembly.md"),
    Path("output/stl/README.md"),
    Path("output/stl/README.tr.md"),
]

REQUIRED_OUTPUTS = NON_STL_OUTPUTS + STL_OUTPUTS

PUBLIC_TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".scad",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
PRIVATE_REFERENCE_PATTERNS = (
    re.compile("/" + r"Users/[^/\s]+", re.IGNORECASE),
    re.compile("/" + r"home/[^/\s]+", re.IGNORECASE),
    re.compile(r"\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s]+", re.IGNORECASE),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    re.compile("şirket " + "bilgisayar", re.IGNORECASE),
)


def public_text_files(root):
    """Yield publishable text artifacts while ignoring local and VCS state."""
    excluded_parts = {".git", ".pytest_cache", "__pycache__", "local"}
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        result = None

    if result is not None and result.returncode == 0:
        candidates = (root / relative for relative in result.stdout.split("\0") if relative)
    else:
        candidates = root.rglob("*")

    for path in candidates:
        if not path.is_file() or excluded_parts.intersection(path.relative_to(root).parts):
            continue
        if path.suffix.casefold() in PUBLIC_TEXT_SUFFIXES or path.name in {
            ".gitignore",
            "LICENSE",
            "Makefile",
        }:
            yield path


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

    for artwork_dir in (Path("artwork"), Path("artwork/tr")):
        svg_path = root / artwork_dir / "activity-box-label.svg"
        if svg_path.exists():
            svg = svg_path.read_text(encoding="utf-8")
            if (
                f'width="{LABEL["width"]}mm"' not in svg
                or f'height="{LABEL["height"]}mm"' not in svg
            ):
                errors.append(f"label SVG physical dimensions are incorrect: {svg_path}")

        png_path = root / artwork_dir / "activity-box-label-preview.png"
        if png_path.exists():
            with Image.open(png_path) as image:
                expected = (
                    round(LABEL["width"] * LABEL["dpi"] / 25.4),
                    round(LABEL["height"] * LABEL["dpi"] / 25.4),
                )
                if image.size != expected:
                    errors.append(
                        f"label PNG dimensions {image.size}, expected {expected}: {png_path}"
                    )

        pdf_path = root / artwork_dir / "activity-box-label-a4.pdf"
        if pdf_path.exists() and not pdf_path.read_bytes().startswith(b"%PDF"):
            errors.append(f"A4 label is not a PDF: {pdf_path}")

    for name, forward_voltage in ELECTRICAL["led_forward_voltages"].items():
        current = (ELECTRICAL["supply_max"] - forward_voltage) / ELECTRICAL["resistor"]
        if current > 0.020:
            errors.append(f"{name} LED current exceeds 20 mA: {current * 1000:.2f} mA")

    for path in public_text_files(root):
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8-sig")
        placeholder_pattern = r"\b(?:TO" + r"DO|T" + r"BD)\b"
        if re.search(placeholder_pattern, text, flags=re.IGNORECASE):
            errors.append(f"placeholder found in {relative}")
        if any(pattern.search(text) for pattern in PRIVATE_REFERENCE_PATTERNS):
            errors.append(f"private environment reference found in {relative}")

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

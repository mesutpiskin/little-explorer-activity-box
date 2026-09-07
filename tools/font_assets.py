"""Load the repository-bundled fonts used by generated raster artwork."""

from pathlib import Path

from PIL import ImageFont


FONT_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts"
REGULAR_FONT = FONT_DIR / "DejaVuSans.ttf"
BOLD_FONT = FONT_DIR / "DejaVuSans-Bold.ttf"


def load_font(pixel_size, bold=False):
    """Return a pinned local font so output does not depend on the host OS."""
    path = BOLD_FONT if bold else REGULAR_FONT
    if not path.is_file():
        raise FileNotFoundError(f"bundled font is missing: {path}")
    return ImageFont.truetype(str(path), pixel_size)


def svg_font_faces(asset_directory):
    """Return SVG CSS that references both bundled DejaVu Sans weights."""
    return (
        "@font-face{font-family:'DejaVu Sans';"
        f"src:url('{asset_directory}/DejaVuSans.ttf') format('truetype');"
        "font-weight:400}"
        "@font-face{font-family:'DejaVu Sans';"
        f"src:url('{asset_directory}/DejaVuSans-Bold.ttf') format('truetype');"
        "font-weight:700}"
    )

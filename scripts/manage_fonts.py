#!/usr/bin/env python3
"""Register fonts bundled with tao-style in the current Matplotlib process."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


PREFERRED_FONT = "Helvetica"
BUNDLED_FONT_DIR = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "helvetica"
FONT_SUFFIXES = {".otf", ".ttf", ".ttc"}


def bundled_font_files() -> list[Path]:
    """Return bundled font files in deterministic order."""

    if not BUNDLED_FONT_DIR.is_dir():
        raise RuntimeError(f"Bundled font directory not found: {BUNDLED_FONT_DIR}")
    files = sorted(
        path for path in BUNDLED_FONT_DIR.iterdir() if path.suffix.lower() in FONT_SUFFIXES
    )
    if not files:
        raise RuntimeError(f"No font files found in {BUNDLED_FONT_DIR}")
    return files


def _matplotlib_font_names() -> set[str] | None:
    try:
        from matplotlib import font_manager
    except ImportError:
        return None

    return {entry.name.casefold() for entry in font_manager.fontManager.ttflist}


def font_available(font_name: str = PREFERRED_FONT) -> bool:
    """Return whether the requested family is available to this Matplotlib process."""

    names = _matplotlib_font_names()
    return names is not None and font_name.casefold() in names


def register_bundled_fonts() -> list[Path]:
    """Register bundled fonts for this Python process without system changes."""

    try:
        from matplotlib import font_manager
    except ImportError as exc:
        raise RuntimeError("Matplotlib is required for process-local font registration") from exc

    files = bundled_font_files()
    for path in files:
        font_manager.fontManager.addfont(path)
    return files


def ensure_matplotlib_font(font_name: str = PREFERRED_FONT) -> str:
    """Ensure a font is usable now and return ``environment`` or ``bundled``."""

    if font_available(font_name):
        return "environment"
    if font_name.casefold() != PREFERRED_FONT.casefold():
        raise RuntimeError(f"No bundled files are available for {font_name}")
    register_bundled_fonts()
    if not font_available(font_name):
        raise RuntimeError(f"Bundled {font_name} files could not be registered")
    return "bundled"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check whether Matplotlib can use Helvetica. If needed, register the "
            "bundled files in this process without modifying system fonts."
        )
    )
    parser.add_argument("--check", action="store_true", help="Check process-local availability.")
    parser.add_argument("--font", default=PREFERRED_FONT, help="Font family to check.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        source = ensure_matplotlib_font(args.font)
    except (OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    detail = "existing environment" if source == "environment" else "bundled, process-local"
    print(f"{args.font}: available ({detail})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

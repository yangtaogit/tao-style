#!/usr/bin/env python3
"""Check and explicitly install fonts bundled with tao-style."""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
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

    manager = font_manager._load_fontmanager(try_read_cache=False)
    return {entry.name.casefold() for entry in manager.ttflist}


def _platform_font_names() -> set[str]:
    system = platform.system()
    if system == "Linux" and shutil.which("fc-list"):
        result = subprocess.run(
            ["fc-list", "--format", "%{family}\n"],
            check=False,
            capture_output=True,
            text=True,
        )
        names: set[str] = set()
        for line in result.stdout.splitlines():
            names.update(part.strip().casefold() for part in line.split(",") if part.strip())
        return names

    if system == "Windows":
        try:
            import winreg
        except ImportError:
            return set()
        names = set()
        key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                index = 0
                while True:
                    try:
                        name, _, _ = winreg.EnumValue(key, index)
                    except OSError:
                        break
                    names.add(name.rsplit(" (", 1)[0].casefold())
                    index += 1
        except FileNotFoundError:
            pass
        return names

    if system == "Darwin" and shutil.which("system_profiler"):
        result = subprocess.run(
            ["system_profiler", "SPFontsDataType"],
            check=False,
            capture_output=True,
            text=True,
        )
        return {
            line.strip().rstrip(":").casefold()
            for line in result.stdout.splitlines()
            if line.startswith("    ") and line.rstrip().endswith(":")
        }

    return set()


def font_available(font_name: str = PREFERRED_FONT) -> bool:
    """Return whether the requested family is available to the plotting runtime."""

    names = _matplotlib_font_names()
    if names is None:
        names = _platform_font_names()
    return font_name.casefold() in names


def user_font_directory() -> Path:
    """Return the current platform's user-level font directory."""

    system = platform.system()
    if system == "Linux":
        return Path.home() / ".local" / "share" / "fonts" / "tao-style"
    if system == "Darwin":
        return Path.home() / "Library" / "Fonts"
    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if not local_app_data:
            raise RuntimeError("LOCALAPPDATA is not set; cannot locate the Windows user font directory.")
        return Path(local_app_data) / "Microsoft" / "Windows" / "Fonts"
    raise RuntimeError(f"Unsupported platform for automatic font installation: {system}")


def _register_windows_fonts(files: list[Path]) -> None:
    import ctypes
    import winreg

    key_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        for path in files:
            kind = "OpenType" if path.suffix.lower() == ".otf" else "TrueType"
            winreg.SetValueEx(key, f"{path.stem} ({kind})", 0, winreg.REG_SZ, path.name)

    hwnd_broadcast = 0xFFFF
    wm_fontchange = 0x001D
    smto_abortifhung = 0x0002
    ctypes.windll.user32.SendMessageTimeoutW(
        hwnd_broadcast,
        wm_fontchange,
        0,
        0,
        smto_abortifhung,
        1000,
        None,
    )


def refresh_font_caches(target: Path, installed_files: list[Path]) -> None:
    """Refresh available user-level caches without requiring administrator access."""

    system = platform.system()
    if system == "Linux" and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f", str(target)], check=True)
    elif system == "Windows":
        _register_windows_fonts(installed_files)

    try:
        from matplotlib import font_manager
    except ImportError:
        return
    font_manager._load_fontmanager(try_read_cache=False)


def install_bundled_fonts() -> list[Path]:
    """Install all bundled Helvetica files into the current user's font directory."""

    source_files = bundled_font_files()
    target = user_font_directory()
    target.mkdir(parents=True, exist_ok=True)

    installed = []
    for source in source_files:
        destination = target / source.name
        shutil.copy2(source, destination)
        installed.append(destination)

    refresh_font_caches(target, installed)
    return installed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Check or explicitly install the Helvetica files bundled with tao-style. "
            "Run --install only after the user approves font installation."
        )
    )
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true", help="Check whether the font is available.")
    action.add_argument(
        "--install",
        action="store_true",
        help="Install bundled fonts for the current user and refresh font caches.",
    )
    parser.add_argument("--font", default=PREFERRED_FONT, help="Font family to check.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.check:
        available = font_available(args.font)
        state = "available" if available else "missing"
        print(f"{args.font}: {state}")
        return 0 if available else 1

    if args.font.casefold() != PREFERRED_FONT.casefold():
        print(
            f"error: bundled installation is available only for {PREFERRED_FONT}",
            file=sys.stderr,
        )
        return 2

    try:
        installed = install_bundled_fonts()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for path in installed:
        print(f"installed: {path}")

    if not font_available(PREFERRED_FONT):
        print(
            "error: Helvetica was copied but is not visible to the plotting runtime",
            file=sys.stderr,
        )
        return 2

    print(f"{PREFERRED_FONT}: available")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


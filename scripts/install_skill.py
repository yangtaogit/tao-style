#!/usr/bin/env python3
"""Install or update the tao-style Skill from this development repository."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


SKILL_NAME = "tao-style"
INSTALLABLE_ENTRIES = (
    "SKILL.md",
    "agents",
    "assets",
    "references",
    "scripts",
)
IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache", ".DS_Store")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_skills_dir() -> Path:
    return default_skills_dir_for_target("codex")


def default_skills_dir_for_target(target: str) -> Path:
    if target == "claude-code":
        return Path.home() / ".claude" / "skills"

    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def validate_source(root: Path) -> None:
    skill_file = root / "SKILL.md"
    if not skill_file.is_file():
        raise RuntimeError(f"Missing required file: {skill_file}")
    for entry in INSTALLABLE_ENTRIES:
        if not (root / entry).exists():
            raise RuntimeError(f"Missing installable entry: {root / entry}")


def remove_existing_target(target: Path, *, dry_run: bool) -> None:
    if target.name != SKILL_NAME:
        raise RuntimeError(f"Refusing to remove unexpected target name: {target}")

    if dry_run:
        print(f"[dry-run] remove existing {target}")
        return

    if target.is_symlink() or target.is_file():
        target.unlink()
    elif target.is_dir():
        shutil.rmtree(target)
    else:
        raise RuntimeError(f"Target exists but is not removable by this script: {target}")


def copy_install(root: Path, target: Path, *, force: bool, dry_run: bool) -> None:
    if target.resolve() == root.resolve():
        raise RuntimeError("Copy target is the repository root; refusing to overwrite the source.")

    if target.exists() or target.is_symlink():
        if not force:
            raise RuntimeError(f"Target already exists: {target}. Re-run with --force to replace it.")
        remove_existing_target(target, dry_run=dry_run)

    if dry_run:
        print(f"[dry-run] create directory {target}")
    else:
        target.mkdir(parents=True, exist_ok=False)

    for entry in INSTALLABLE_ENTRIES:
        source = root / entry
        destination = target / entry
        if dry_run:
            print(f"[dry-run] copy {source} -> {destination}")
            continue
        if source.is_dir():
            shutil.copytree(source, destination, ignore=IGNORE_PATTERNS)
        else:
            shutil.copy2(source, destination)


def symlink_install(root: Path, target: Path, *, force: bool, dry_run: bool) -> None:
    if target.is_symlink() and target.resolve() == root.resolve():
        print(f"Already linked: {target} -> {root}")
        return

    if target.exists() or target.is_symlink():
        if not force:
            raise RuntimeError(f"Target already exists: {target}. Re-run with --force to replace it.")
        remove_existing_target(target, dry_run=dry_run)

    if dry_run:
        print(f"[dry-run] symlink {target} -> {root}")
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.symlink_to(root, target_is_directory=True)
    except OSError as exc:
        raise RuntimeError(
            "Could not create symlink. If the target skills directory is on Windows "
            "or another filesystem, use --mode copy instead."
        ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or update the tao-style Skill.")
    parser.add_argument(
        "--target",
        choices=("codex", "claude-code", "all"),
        default="codex",
        help=(
            "Tool target to install for. codex uses $CODEX_HOME/skills or ~/.codex/skills; "
            "claude-code uses ~/.claude/skills; all installs to both default locations."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "symlink"),
        default="copy",
        help="Installation mode. Use copy for cross-filesystem installs; symlink for live development.",
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=None,
        help=(
            "Override the directory that contains skills. Only valid for a single target. "
            "For Claude Code project skills, pass a project .claude/skills directory here."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing tao-style target.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without changing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()

    if args.skills_dir is not None and args.target == "all":
        print("error: --skills-dir cannot be used with --target all", file=sys.stderr)
        return 1

    targets = ("codex", "claude-code") if args.target == "all" else (args.target,)

    try:
        validate_source(root)
        print(f"Source: {root}")
        print(f"Mode: {args.mode}")
        for tool_target in targets:
            skills_dir = (
                args.skills_dir.expanduser()
                if args.skills_dir is not None
                else default_skills_dir_for_target(tool_target)
            )
            target = skills_dir / SKILL_NAME
            print(f"Target ({tool_target}): {target}")
            if not args.dry_run:
                skills_dir.mkdir(parents=True, exist_ok=True)
            if args.mode == "copy":
                copy_install(root, target, force=args.force, dry_run=args.dry_run)
            else:
                symlink_install(root, target, force=args.force, dry_run=args.dry_run)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    action = "checked" if args.dry_run else "installed"
    print(f"tao-style {action} for {', '.join(targets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

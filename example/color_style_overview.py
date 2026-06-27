#!/usr/bin/env python3
"""Example: Tao Style color system overview."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    GRADIENT_COLORMAPS,
    CORE_PALETTE,
    PALETTE,
    TAU_PALETTE,
    matplotlib_rcparams,
)


def draw_palette(ax, title: str, colors: list[str]) -> None:
    ax.set_xlim(0, len(colors))
    ax.set_ylim(0, 1)
    ax.set_title(title, loc="left", pad=5)
    ax.set_yticks([])
    ax.set_xticks(np.arange(len(colors)) + 0.5)
    ax.set_xticklabels(colors, rotation=0)
    ax.tick_params(axis="x", which="both", length=0, pad=4)
    for index, color in enumerate(colors):
        ax.add_patch(
            plt.Rectangle((index + 0.08, 0.22), 0.84, 0.5, facecolor=color, edgecolor="black", linewidth=0.35)
        )
    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_gradient(ax, title: str, colors: list[str]) -> None:
    cmap = LinearSegmentedColormap.from_list(title, colors)
    rgb = np.array([to_rgb(cmap(i / 255.0)) for i in range(256)]).reshape(1, 256, 3)
    ax.imshow(rgb, aspect="auto", extent=(0, 1, 0, 1))
    ax.set_title(title, loc="left", pad=5)
    ax.set_yticks([])
    ax.set_xticks(np.linspace(0.0, 1.0, len(colors)))
    ax.set_xticklabels(colors)
    ax.tick_params(axis="x", which="both", length=0, pad=4)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.6)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    fig = plt.figure(figsize=(7.2, 4.9))
    grid = fig.add_gridspec(
        nrows=6,
        ncols=1,
        height_ratios=[0.82, 0.82, 0.82, 0.72, 0.72, 0.72],
        hspace=0.95,
    )

    draw_palette(fig.add_subplot(grid[0, 0]), "Core anchors", CORE_PALETTE)
    draw_palette(fig.add_subplot(grid[1, 0]), "Default sequence", PALETTE)
    draw_palette(fig.add_subplot(grid[2, 0]), "τ palette", TAU_PALETTE)
    draw_gradient(fig.add_subplot(grid[3, 0]), "Dark-blue gradient", GRADIENT_COLORMAPS["dark-blue"])
    draw_gradient(fig.add_subplot(grid[4, 0]), "Gray gradient", GRADIENT_COLORMAPS["gray"])
    draw_gradient(fig.add_subplot(grid[5, 0]), "τ gradient", GRADIENT_COLORMAPS["tau"])

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

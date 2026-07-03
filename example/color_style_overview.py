#!/usr/bin/env python3
"""Example: Tao Style color system overview."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    CORE_PALETTE,
    categorical_palette,
    gradient_stops,
    matplotlib_colormap,
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


def draw_gradient(ax, title: str, key: str) -> None:
    cmap = matplotlib_colormap(key)
    rgb = np.array([to_rgb(cmap(i / 255.0)) for i in range(256)]).reshape(1, 256, 3)
    stops = gradient_stops(key)
    ax.imshow(rgb, aspect="auto", extent=(0, 1, 0, 1))
    ax.set_title(title, loc="left", pad=5)
    ax.set_yticks([])
    ax.set_xticks([position for position, _ in stops])
    ax.set_xticklabels([color for _, color in stops])
    ax.tick_params(axis="x", which="both", length=0, pad=4)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.6)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    fig = plt.figure(figsize=(7.2, 6.2))
    grid = fig.add_gridspec(
        nrows=7,
        ncols=1,
        height_ratios=[0.72, 0.72, 0.62, 0.62, 0.62, 0.62, 0.62],
        hspace=0.78,
    )

    draw_palette(fig.add_subplot(grid[0, 0]), "tao-core anchors", CORE_PALETTE)
    draw_palette(fig.add_subplot(grid[1, 0]), "tao palette", categorical_palette("tao"))
    draw_gradient(fig.add_subplot(grid[2, 0]), "tao blue gradient", "tao-blue")
    draw_gradient(fig.add_subplot(grid[3, 0]), "tao gray gradient", "tao-gray")
    draw_gradient(fig.add_subplot(grid[4, 0]), "tao green gradient", "tao-green")
    draw_gradient(fig.add_subplot(grid[5, 0]), "tao red gradient", "tao-red")
    draw_gradient(fig.add_subplot(grid[6, 0]), "tao gradient", "tao")

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

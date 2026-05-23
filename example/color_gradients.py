#!/usr/bin/env python3
"""Example: Tao Style gradient color outputs."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.apply_tao_style import (  # noqa: E402
    DEFAULT_ASPECT,
    GRADIENT_COLORMAPS,
    figure_size,
    gradient_colormap,
    matplotlib_rcparams,
)


def interpolate_colors(colors: list[str], count: int) -> list[str]:
    cmap = LinearSegmentedColormap.from_list("tao_gradient", colors)
    return [matplotlib.colors.to_hex(cmap(i / max(count - 1, 1))) for i in range(count)]


def plot_gradient_row(ax, name: str, colors: list[str]) -> None:
    samples = interpolate_colors(colors, 256)
    rgb = np.array([to_rgb(color) for color in samples]).reshape(1, 256, 3)
    ax.imshow(rgb, aspect="auto", extent=(0, 1, 0, 1))
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_ylabel(name, rotation=0, ha="right", va="center")
    for spine in ax.spines.values():
        spine.set_visible(True)


def plot_curve_panel(ax, gradient_name: str, colors: list[str], count: int) -> None:
    x_values = np.linspace(0.0, 2.0 * np.pi, 300)
    sampled_colors = interpolate_colors(colors, count)
    for index, color in enumerate(sampled_colors):
        phase = index * 0.18
        amplitude = 0.55 + index * 0.03
        offset = index * 0.18
        y_values = amplitude * np.sin(x_values + phase) + offset
        ax.plot(x_values, y_values, color=color, linewidth=1.0)
    ax.set_title(gradient_name)
    ax.set_xlabel("X Label")
    ax.set_ylabel("Y Label")
    ax.set_xlim(0.0, 2.0 * np.pi)
    ax.minorticks_on()


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    fig = plt.figure(figsize=figure_size(DEFAULT_ASPECT, width=6.0))
    grid = fig.add_gridspec(
        nrows=3,
        ncols=2,
        height_ratios=[0.26, 1.0, 1.0],
        hspace=0.38,
        wspace=0.28,
    )

    for column, name in enumerate(sorted(GRADIENT_COLORMAPS)):
        colors = gradient_colormap(name)
        plot_gradient_row(fig.add_subplot(grid[0, column]), name, colors)
        plot_curve_panel(fig.add_subplot(grid[1:, column]), name, colors, count=10)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

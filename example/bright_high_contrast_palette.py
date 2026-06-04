#!/usr/bin/env python3
"""Example: Tao Style optional bright high-contrast palette."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    categorical_palette,
    gradient_colormap,
    matplotlib_rcparams,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    palette = categorical_palette("bright-high-contrast")
    cmap = LinearSegmentedColormap.from_list(
        "tao_bright_high_contrast",
        gradient_colormap("bright-high-contrast"),
    )

    x = np.linspace(-3.0, 3.0, 220)
    y = np.linspace(-2.0, 2.0, 170)
    xx, yy = np.meshgrid(x, y)
    z = np.exp(-0.55 * ((xx + 1.0) ** 2 + 1.35 * yy**2))
    z += 0.75 * np.exp(-0.8 * ((xx - 1.15) ** 2 + 0.55 * (yy - 0.45) ** 2))
    z += 0.18 * np.sin(2.4 * xx) * np.cos(1.7 * yy)

    fig = plt.figure(figsize=(6.3, 3.15))
    grid = fig.add_gridspec(
        nrows=2,
        ncols=3,
        width_ratios=[1.0, 1.0, 0.08],
        height_ratios=[0.38, 1.0],
        hspace=0.34,
        wspace=0.28,
    )

    ax_palette = fig.add_subplot(grid[0, :2])
    ax_palette.set_xlim(0, len(palette))
    ax_palette.set_ylim(0, 1)
    ax_palette.set_yticks([])
    ax_palette.set_xticks(np.arange(len(palette)) + 0.5)
    ax_palette.set_xticklabels([str(index + 1) for index in range(len(palette))])
    ax_palette.tick_params(axis="x", which="both", top=False, bottom=False, pad=1.5)
    for index, color in enumerate(palette):
        ax_palette.add_patch(
            plt.Rectangle((index + 0.08, 0.2), 0.84, 0.58, facecolor=color, edgecolor="none")
        )

    ax_img = fig.add_subplot(grid[1, 0])
    image = ax_img.imshow(
        z,
        origin="lower",
        extent=(x.min(), x.max(), y.min(), y.max()),
        cmap=cmap,
        aspect="auto",
    )
    ax_img.set_xlabel("X Label [Unit]")
    ax_img.set_ylabel("Y Label [Unit]")
    ax_img.minorticks_on()

    ax_curves = fig.add_subplot(grid[1, 1])
    curve_x = np.linspace(0.0, 10.0, 360)
    for index, color in enumerate(palette):
        y_curve = 0.08 * index + 0.15 * np.sin(0.9 * curve_x + 0.45 * index) * np.exp(-curve_x / 8.0)
        y_curve += 0.018 * curve_x
        ax_curves.plot(curve_x, y_curve, color=color, linewidth=1.0)
    ax_curves.set_xlabel("X Label [Unit]")
    ax_curves.set_ylabel("Y Label [Unit]")
    ax_curves.set_xlim(0, 10)
    ax_curves.minorticks_on()

    cax = fig.add_subplot(grid[1, 2])
    cbar = fig.colorbar(image, cax=cax)
    cbar.set_label("Signal [a.u.]")
    cbar.outline.set_linewidth(1.0)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

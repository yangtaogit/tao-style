#!/usr/bin/env python3
"""Example: Tao Style palette and gradient display."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    GRADIENT_COLORMAPS,
    LINE_WIDTH,
    matplotlib_rcparams,
)


def sample_colors(cmap, count: int) -> list:
    return [cmap(value) for value in np.linspace(0.08, 0.96, count)]


def map_data() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-3.0, 3.0, 220)
    y = np.linspace(-2.0, 2.0, 170)
    xx, yy = np.meshgrid(x, y)
    z = np.exp(-0.55 * ((xx + 1.0) ** 2 + 1.35 * yy**2))
    z += 0.75 * np.exp(-0.8 * ((xx - 1.15) ** 2 + 0.55 * (yy - 0.45) ** 2))
    z += 0.18 * np.sin(2.4 * xx) * np.cos(1.7 * yy)
    return x, y, z


def draw_curve_panel(ax, cmap, row_index: int) -> None:
    curve_x = np.linspace(0.0, 10.0, 360)
    for index, color in enumerate(sample_colors(cmap, 7)):
        y_curve = 0.07 * index + 0.15 * np.sin(0.9 * curve_x + 0.45 * index) * np.exp(-curve_x / 8.0)
        y_curve += 0.018 * curve_x + 0.015 * row_index
        ax.plot(curve_x, y_curve, color=color, linewidth=LINE_WIDTH)
    ax.set_xlabel("X Label [Unit]")
    ax.set_ylabel("Y Label [Unit]")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 0.78)
    ax.minorticks_on()


def draw_map_panel(fig, ax, cax, cmap) -> None:
    x, y, z = map_data()
    image = ax.imshow(
        z,
        origin="lower",
        extent=(x.min(), x.max(), y.min(), y.max()),
        cmap=cmap,
        aspect="auto",
    )
    ax.set_xlabel("X Label [Unit]")
    ax.set_ylabel("")
    ax.minorticks_on()
    cbar = fig.colorbar(image, cax=cax)
    cbar.set_label("Signal", labelpad=2)
    cbar.ax.tick_params(pad=1)
    cbar.outline.set_linewidth(0.8)


def draw_contour_panel(fig, ax, cax, cmap) -> None:
    x, y, z = map_data()
    levels = np.linspace(float(z.min()), float(z.max()), 8)
    discrete = ListedColormap(sample_colors(cmap, len(levels) - 1))
    norm = BoundaryNorm(levels, discrete.N)
    contour = ax.contourf(x, y, z, levels=levels, cmap=discrete, norm=norm)
    ax.contour(x, y, z, levels=levels, colors="black", linewidths=0.35, alpha=0.45)
    ax.set_xlabel("X Label [Unit]")
    ax.set_ylabel("")
    ax.minorticks_on()
    cbar = fig.colorbar(contour, cax=cax, ticks=levels[::2])
    cbar.set_label("Signal", labelpad=2)
    cbar.ax.tick_params(pad=1)
    cbar.outline.set_linewidth(0.8)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    gradient_names = ["τ", "dark-blue", "gray"]
    gradient_keys = ["tau", "dark-blue", "gray"]

    fig = plt.figure(figsize=(11.2, 8.2))
    grid = fig.add_gridspec(
        nrows=3,
        ncols=4,
        width_ratios=[0.06, 1.0, 1.08, 1.08],
        hspace=0.62,
        wspace=0.38,
    )

    for row_index, (display_name, key) in enumerate(zip(gradient_names, gradient_keys)):
        cmap = LinearSegmentedColormap.from_list(f"tao_{key}", GRADIENT_COLORMAPS[key])

        label_ax = fig.add_subplot(grid[row_index, 0])
        label_ax.axis("off")
        label_ax.text(0.5, 0.5, display_name, rotation=90, ha="center", va="center")

        draw_curve_panel(fig.add_subplot(grid[row_index, 1]), cmap, row_index)

        map_grid = grid[row_index, 2].subgridspec(nrows=1, ncols=2, width_ratios=[1.0, 0.05], wspace=0.06)
        draw_map_panel(
            fig,
            fig.add_subplot(map_grid[0, 0]),
            fig.add_subplot(map_grid[0, 1]),
            cmap,
        )

        contour_grid = grid[row_index, 3].subgridspec(nrows=1, ncols=2, width_ratios=[1.0, 0.05], wspace=0.06)
        draw_contour_panel(
            fig,
            fig.add_subplot(contour_grid[0, 0]),
            fig.add_subplot(contour_grid[0, 1]),
            cmap,
        )

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

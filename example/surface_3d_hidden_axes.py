#!/usr/bin/env python3
"""Test: 3D surface with hidden axes, inside colorbar, and compact XYZ marker."""

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
    GRADIENT_COLORMAPS,
    add_matplotlib_3d_xyz_marker,
    hide_matplotlib_3d_axes,
    matplotlib_rcparams,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    x = np.linspace(-2.8, 2.8, 72)
    y = np.linspace(-2.4, 2.4, 66)
    xx, yy = np.meshgrid(x, y)
    radius = np.sqrt(xx**2 + yy**2)
    zz = 0.42 * np.cos(1.7 * radius) * np.exp(-0.12 * radius**2)
    zz += 0.18 * np.exp(-0.55 * ((xx - 1.05) ** 2 + 1.5 * (yy + 0.45) ** 2))

    cmap = LinearSegmentedColormap.from_list("tao_dark_blue", GRADIENT_COLORMAPS["dark-blue"])
    elev, azim = 24, -58

    fig = plt.figure(figsize=(4.8, 3.15))
    ax = fig.add_axes([0.035, 0.035, 0.855, 0.93], projection="3d")
    surface = ax.plot_surface(
        xx,
        yy,
        zz,
        cmap=cmap,
        linewidth=0.2,
        edgecolor=(0.18, 0.18, 0.18, 0.16),
        antialiased=True,
        rcount=52,
        ccount=52,
    )

    ax.set_xlim(float(x.min()), float(x.max()))
    ax.set_ylim(float(y.min()), float(y.max()))
    ax.set_zlim(float(zz.min()) * 1.08, float(zz.max()) * 1.08)
    try:
        ax.set_box_aspect((1.0, 0.88, 0.58), zoom=1.12)
    except TypeError:
        ax.set_box_aspect((1.0, 0.88, 0.58))
        ax.dist = 7.0
    ax.view_init(elev=elev, azim=azim)
    hide_matplotlib_3d_axes(ax)
    add_matplotlib_3d_xyz_marker(fig, elev=elev, azim=azim)

    cax = fig.add_axes([0.825, 0.20, 0.030, 0.60])
    cbar = fig.colorbar(surface, cax=cax)
    cbar.set_label("Value", labelpad=3)
    cbar.outline.set_linewidth(0.6)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

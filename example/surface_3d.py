#!/usr/bin/env python3
"""Example: Tao Style 3D surface using Matplotlib's default 3D axes."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    add_matplotlib_3d_colorbar,
    apply_matplotlib_3d_style,
    matplotlib_colormap,
    matplotlib_rcparams,
    set_equal_xyz_box_aspect,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    x = np.linspace(-2.8, 2.8, 72)
    y = np.linspace(-2.4, 2.4, 66)
    xx, yy = np.meshgrid(x, y)
    radius = np.sqrt(xx**2 + yy**2)
    zz = 1.10 * np.cos(1.7 * radius) * np.exp(-0.12 * radius**2)
    zz += 0.48 * np.exp(-0.55 * ((xx - 1.05) ** 2 + 1.5 * (yy + 0.45) ** 2))
    zz -= 0.18 * np.exp(-0.65 * ((xx + 1.35) ** 2 + 1.25 * (yy - 0.7) ** 2))

    cmap = matplotlib_colormap("tao-blue")
    fig = plt.figure(figsize=(4.8, 3.15))
    ax = fig.add_subplot(111, projection="3d")
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
    ax.view_init(elev=24, azim=-58)
    apply_matplotlib_3d_style(
        ax,
        xlabel="X",
        ylabel="Y",
        zlabel="Z",
        zoom=1.2,
        max_ticks=5,
        tick_pad=-1.5,
        labelpad=-3.0,
    )

    set_equal_xyz_box_aspect(
        ax,
        xlim=(float(x.min()), float(x.max())),
        ylim=(float(y.min()), float(y.max())),
        zlim=(float(zz.min()) * 1.08, float(zz.max()) * 1.08),
        zoom=1.2,
    )

    cbar = add_matplotlib_3d_colorbar(fig, ax, surface)
    cbar.set_label("Value", labelpad=4)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Example: 4D voxel data with hidden axes and a compact XYZ direction marker."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    add_matplotlib_3d_xyz_marker,
    hide_matplotlib_3d_axes,
    matplotlib_colormap,
    matplotlib_rcparams,
)


def midpoints(values: np.ndarray) -> np.ndarray:
    result = values
    sl = ()
    for _ in range(values.ndim):
        result = (result[sl + np.index_exp[:-1]] + result[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return result


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    radius, theta, z = np.mgrid[0:1:11j, 0 : np.pi * 2 : 25j, -0.5:0.5:11j]
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)

    radius_c = midpoints(radius)
    theta_c = midpoints(theta)
    z_c = midpoints(z)

    voxels = (radius_c - 0.7) ** 2 + (z_c + 0.2 * np.cos(theta_c * 2.0)) ** 2 < 0.2**2
    value = 0.55 * theta_c / (np.pi * 2.0) + 0.30 * radius_c + 0.15 * (z_c + 0.5)

    cmap = matplotlib_colormap("tau")
    norm = Normalize(vmin=float(value[voxels].min()), vmax=float(value[voxels].max()))
    facecolors = cmap(norm(value))
    facecolors[..., 3] = 0.9
    edgecolors = facecolors.copy()
    edgecolors[..., :3] = np.clip(edgecolors[..., :3] * 0.68, 0.0, 1.0)
    edgecolors[..., 3] = 0.95

    elev, azim = 22, -55
    fig = plt.figure(figsize=(4.8, 3.15))
    ax = fig.add_axes([0.035, 0.035, 0.855, 0.93], projection="3d")
    ax.voxels(
        x,
        y,
        z,
        voxels,
        facecolors=facecolors,
        edgecolors=edgecolors,
        linewidth=0.25,
    )

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-0.5, 0.5)
    try:
        ax.set_box_aspect((1.0, 1.0, 0.58), zoom=1.26)
    except TypeError:
        ax.set_box_aspect((1.0, 1.0, 0.58))
        ax.dist = 7.0
    ax.view_init(elev=elev, azim=azim)
    hide_matplotlib_3d_axes(ax)
    add_matplotlib_3d_xyz_marker(fig, elev=elev, azim=azim)

    mappable = ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cax = fig.add_axes([0.845, 0.20, 0.030, 0.60])
    cbar = fig.colorbar(mappable, cax=cax)
    cbar.set_label("Value", labelpad=3)
    cbar.outline.set_linewidth(0.6)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

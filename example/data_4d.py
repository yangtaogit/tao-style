#!/usr/bin/env python3
"""Example: Tao Style 4D voxel data shown as XYZ volume plus value color."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    GRADIENT_COLORMAPS,
    apply_matplotlib_3d_style,
    matplotlib_rcparams,
)


def midpoints(values: np.ndarray) -> np.ndarray:
    """Return cell-centered values for an N-dimensional grid."""

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

    cmap = LinearSegmentedColormap.from_list("tao_tau", GRADIENT_COLORMAPS["tau"])
    norm = Normalize(vmin=float(value[voxels].min()), vmax=float(value[voxels].max()))
    facecolors = cmap(norm(value))
    facecolors[..., 3] = 0.88
    edgecolors = facecolors.copy()
    edgecolors[..., :3] = np.clip(edgecolors[..., :3] * 0.68, 0.0, 1.0)
    edgecolors[..., 3] = 0.92

    fig = plt.figure(figsize=(4.8, 3.15))
    ax = fig.add_subplot(111, projection="3d")
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
    ax.set_box_aspect((1.0, 1.0, 0.58))
    ax.view_init(elev=22, azim=-55)
    apply_matplotlib_3d_style(ax, xlabel="X", ylabel="Y", zlabel="Z")

    mappable = ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = fig.colorbar(mappable, ax=ax, fraction=0.035, pad=0.16, shrink=0.72)
    cbar.set_label("Value", labelpad=4)
    cbar.outline.set_linewidth(0.8)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

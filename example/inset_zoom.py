#!/usr/bin/env python3
"""Example: Tao Style curve with an inset zoom panel."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    DEFAULT_ASPECT,
    LINE_WIDTH,
    PALETTE,
    axes_box_size,
    save_fixed_height_figure,
    set_fixed_axes_box,
    matplotlib_rcparams,
)


def main() -> None:
    x = np.linspace(0.0, 10.0, 520)
    y = 0.42 + 0.16 * np.sin(1.35 * x) * np.exp(-x / 8.5)
    y += 0.035 * x + 0.018 * np.sin(6.2 * x)
    y2 = y + 0.07 * np.exp(-0.5 * ((x - 6.2) / 0.85) ** 2)

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    ax.plot(x, y, color=PALETTE[0], linewidth=LINE_WIDTH, label="Reference")
    ax.plot(x, y2, color=PALETTE[1], linewidth=LINE_WIDTH, linestyle="--", label="Sample")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Signal [a.u.]")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.26, 0.98)
    ax.minorticks_on()

    inset = ax.inset_axes([0.11, 0.54, 0.42, 0.38])
    inset.plot(x, y, color=PALETTE[0], linewidth=LINE_WIDTH)
    inset.plot(x, y2, color=PALETTE[1], linewidth=LINE_WIDTH, linestyle="--")
    inset.set_xlim(5.0, 7.2)
    inset.set_ylim(0.62, 0.86)
    inset.minorticks_on()
    inset.set_xlabel("")
    inset.set_ylabel("")
    inset.tick_params(axis="both", which="major", labelsize=7)


    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)
    output = Path(__file__).with_suffix(".svg")
    save_fixed_height_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

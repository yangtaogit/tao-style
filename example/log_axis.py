#!/usr/bin/env python3
"""Example: Tao Style base-10 logarithmic axis."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    DEFAULT_ASPECT,
    FIT_LINE_STYLES,
    LINE_WIDTH,
    PALETTE,
    apply_matplotlib_legend,
    apply_matplotlib_log10_axis,
    axes_box_size,
    save_fixed_height_figure,
    set_fixed_axes_box,
    matplotlib_rcparams,
)


def main() -> None:
    x = np.linspace(0, 600, 260)
    scales = [0.7, 1.3, 2.2]
    offsets = [85, 130, 175]

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    for index, (scale, offset) in enumerate(zip(scales, offsets)):
        color = PALETTE[index]
        y = 1e-10 + scale * 8e-11 * np.exp((x - offset) / 145.0)
        y += scale * 1.8e-10 * (x / 600.0) ** 2
        ax.plot(
            x,
            y,
            color=color,
            linestyle=FIT_LINE_STYLES[index],
            linewidth=LINE_WIDTH,
            label=f"Sample {index + 1}",
        )

    ax.set_xlabel("Bias Voltage [V]")
    ax.set_ylabel("Current [A]")
    ax.set_xlim(0, 600)
    ax.set_ylim(1e-10, 1e-6)
    ax.minorticks_on()
    apply_matplotlib_log10_axis(ax, axis="y")
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)

    output = Path(__file__).with_suffix(".svg")
    save_fixed_height_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

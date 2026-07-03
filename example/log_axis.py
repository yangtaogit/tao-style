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
    LINE_STYLES,
    LINE_WIDTH,
    PALETTE,
    apply_matplotlib_legend,
    apply_matplotlib_log10_axis,
    axes_box_size,
    save_adaptive_figure,
    set_fixed_axes_box,
    matplotlib_rcparams,
)


def main() -> None:
    x = np.linspace(0, 600, 260)
    bases = [1.1e-9, 2.8e-9, 7.0e-9]
    growth_rates = [3.0, 3.35, 3.75]
    curvature = [0.45, 0.62, 0.82]

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    for index, (base, growth, bend) in enumerate(zip(bases, growth_rates, curvature)):
        color = PALETTE[index]
        normalized_x = x / x.max()
        y = base * 10 ** (growth * normalized_x)
        y *= 1.0 + bend * normalized_x**2
        ax.plot(
            x,
            y,
            color=color,
            linestyle=LINE_STYLES[index],
            linewidth=LINE_WIDTH,
            label=f"Sample {index + 1}",
        )

    ax.set_xlabel("Bias Voltage [V]")
    ax.set_ylabel("Current [A]")
    ax.set_xlim(0, 600)
    ax.set_ylim(8e-10, 1e-4)
    ax.minorticks_on()
    apply_matplotlib_log10_axis(ax, axis="y")
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)

    output = Path(__file__).with_suffix(".svg")
    save_adaptive_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

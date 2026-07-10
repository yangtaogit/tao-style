#!/usr/bin/env python3
"""Example: Tao Style optional major-tick grid on a base-10 log axis."""

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
    apply_matplotlib_grid,
    apply_matplotlib_legend,
    apply_matplotlib_log10_axis,
    axes_box_size,
    matplotlib_rcparams,
    save_adaptive_figure,
    set_fixed_axes_box,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    x = np.linspace(0, 500, 260)
    bases = [1.4e-9, 3.5e-9, 8.8e-9]
    rates = [3.0, 3.3, 3.65]

    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))
    normalized_x = x / x.max()
    for index, (base, rate) in enumerate(zip(bases, rates)):
        y = base * 10 ** (rate * normalized_x) * (1.0 + 0.35 * normalized_x**2)
        ax.plot(
            x,
            y,
            color=PALETTE[index],
            linestyle=LINE_STYLES[index],
            linewidth=LINE_WIDTH,
            label=f"Sample {index + 1}",
        )

    ax.set_xlabel("Bias Voltage [V]")
    ax.set_ylabel("Current [A]")
    ax.set_xlim(0, 500)
    ax.set_ylim(8e-10, 2e-5)
    ax.minorticks_on()
    apply_matplotlib_log10_axis(ax, axis="y")
    apply_matplotlib_grid(ax)
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)
    output = Path(__file__).with_suffix(".svg")
    save_adaptive_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

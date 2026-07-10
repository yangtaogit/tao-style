#!/usr/bin/env python3
"""Example: Tao Style optional major-tick grid on a linear XY plot."""

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
    apply_matplotlib_grid,
    apply_matplotlib_legend,
    axes_box_size,
    matplotlib_rcparams,
    save_adaptive_figure,
    series_colors,
    set_fixed_axes_box,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    x = np.linspace(0.0, 10.0, 300)
    series = [
        (0.72, 0.0, "Sample A"),
        (0.54, 0.7, "Sample B"),
        (0.38, 1.4, "Sample C"),
    ]

    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))
    colors = series_colors(len(series))
    for index, (scale, phase, label) in enumerate(series):
        y = 1.6 + scale * np.sin(1.35 * x + phase) + 0.18 * x
        ax.plot(
            x,
            y,
            color=colors[index],
            linestyle=LINE_STYLES[index],
            linewidth=LINE_WIDTH,
            label=label,
        )

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Signal [a.u.]")
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 4.3)
    ax.minorticks_on()
    apply_matplotlib_grid(ax)
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)
    output = Path(__file__).with_suffix(".svg")
    save_adaptive_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

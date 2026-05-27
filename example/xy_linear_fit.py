#!/usr/bin/env python3
"""Example: Tao Style linear data with fitted curves."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    FIT_LINE_STYLES,
    LINE_WIDTH,
    MARKER_SIZE,
    PALETTE,
    apply_matplotlib_legend,
    axes_box_size,
    save_fixed_height_figure,
    set_fixed_axes_box,
    matplotlib_rcparams,
)


def main() -> None:
    rng = np.random.default_rng(20260522)
    x = np.linspace(0.5, 9.5, 13)
    series = [
        (0.72, 0.35, "Device A"),
        (0.48, 1.15, "Device B"),
        (0.31, 1.85, "Device C"),
    ]

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=axes_box_size("5:3"))

    fit_x = np.linspace(0.0, 10.0, 300)
    for index, (slope, intercept, label) in enumerate(series):
        color = PALETTE[index]
        y = slope * x + intercept + rng.normal(0.0, 0.12, size=x.size)
        fit = np.polyfit(x, y, deg=1)

        ax.plot(
            x,
            y,
            linestyle="none",
            marker="o",
            markersize=MARKER_SIZE,
            color=color,
            label=label,
        )
        ax.plot(
            fit_x,
            np.polyval(fit, fit_x),
            linestyle=FIT_LINE_STYLES[index],
            linewidth=LINE_WIDTH,
            color=color,
        )

    ax.set_xlabel("Bias Voltage [V]")
    ax.set_ylabel("Response [a.u.]")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, "5:3")

    output = Path(__file__).with_suffix(".svg")
    save_fixed_height_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

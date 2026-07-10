#!/usr/bin/env python3
"""Example: Tao Style three curves with filled confidence bands."""

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
    axes_box_size,
    matplotlib_rcparams,
    save_adaptive_figure,
    series_colors,
    set_fixed_axes_box,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    rng = np.random.default_rng(42)
    x = np.linspace(0, 8, 300)
    colors = series_colors(3)
    datasets = [
        (np.exp(-0.3 * x) * np.sin(2 * x), 0.10, "Run 1", "-"),
        (np.exp(-0.2 * x) * np.cos(1.5 * x), 0.13, "Run 2", "--"),
        (np.exp(-0.15 * x) * np.sin(x + 1), 0.09, "Run 3", ":"),
    ]

    fig, ax = plt.subplots(figsize=axes_box_size())
    for (yi, err, label, ls), color in zip(datasets, colors):
        ax.fill_between(x, yi - err, yi + err, color=color, alpha=0.16, linewidth=0)
        ax.plot(x, yi, color=color, linewidth=1.0, linestyle=ls, label=label)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Response")
    ax.legend(fontsize=8, frameon=False)

    set_fixed_axes_box(fig, ax)
    output = Path(__file__).with_suffix(".svg")
    save_adaptive_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

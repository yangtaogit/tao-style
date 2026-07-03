#!/usr/bin/env python3
"""Example: Tao Style multiple filled histograms."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    DEFAULT_ASPECT,
    series_colors,
    apply_matplotlib_legend,
    axes_box_size,
    save_adaptive_figure,
    set_fixed_axes_box,
    matplotlib_rcparams,
    plot_matplotlib_histogram,
)


def main() -> None:
    rng = np.random.default_rng(20260526)
    bins = np.arange(-4.5, 4.51, 0.25)
    mode = "probability_density"
    samples = [
        rng.normal(-0.45, 0.95, size=900),
        rng.normal(0.05, 1.15, size=900),
        rng.normal(0.48, 1.35, size=900),
        rng.normal(0.90, 1.55, size=900),
    ]
    labels = ["σ = 0.95", "σ = 1.15", "σ = 1.35", "σ = 1.55"]
    colors = series_colors(len(samples))

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    for data, label, color in zip(samples, labels, colors):
        plot_matplotlib_histogram(
            ax,
            data,
            bins,
            mode,
            unit="mm",
            color=color,
            label=label,
        )

    ax.set_xlabel("Measurement [mm]")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(0, 0.46)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)

    output = Path(__file__).with_suffix(".svg")
    save_adaptive_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

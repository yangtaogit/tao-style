#!/usr/bin/env python3
"""Example: Tao Style binned Gaussian data with error bars."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    ERRORBAR_CAP_SIZE,
    ERRORBAR_LINE_WIDTH,
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


def gaussian_pdf(x: np.ndarray, sigma: float) -> np.ndarray:
    return np.exp(-0.5 * (x / sigma) ** 2) / (sigma * np.sqrt(2.0 * np.pi))


def main() -> None:
    rng = np.random.default_rng(20260523)
    sigmas = [0.75, 1.05, 1.45]
    bins = np.arange(-4.5, 4.51, 0.55)
    centers = 0.5 * (bins[:-1] + bins[1:])
    x_fit = np.linspace(-4.5, 4.5, 400)

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=axes_box_size("5:3"))

    for index, sigma in enumerate(sigmas):
        color = PALETTE[index]
        samples = rng.normal(0.0, sigma, size=360)
        counts, _ = np.histogram(samples, bins=bins)
        density = counts / (counts.sum() * np.diff(bins))
        error = np.sqrt(np.maximum(counts, 1)) / (counts.sum() * np.diff(bins))
        error *= 1.9

        ax.errorbar(
            centers,
            density,
            yerr=error,
            fmt="o",
            markersize=MARKER_SIZE,
            elinewidth=ERRORBAR_LINE_WIDTH,
            capsize=ERRORBAR_CAP_SIZE,
            color=color,
            label=f"σ = {sigma:.2f}",
        )
        ax.plot(
            x_fit,
            gaussian_pdf(x_fit, sigma),
            color=color,
            linestyle=FIT_LINE_STYLES[index],
            linewidth=LINE_WIDTH,
        )

    ax.set_xlabel("Position [mm]")
    ax.set_ylabel("Probability Density [1/mm]")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(0, 0.7)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)

    set_fixed_axes_box(fig, ax, "5:3")

    output = Path(__file__).with_suffix(".svg")
    save_fixed_height_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

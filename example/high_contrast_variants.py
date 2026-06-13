#!/usr/bin/env python3
"""Example variants using Tao Style's bright high-contrast palette."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    DEFAULT_ASPECT,
    ERRORBAR_CAP_SIZE,
    ERRORBAR_LINE_WIDTH,
    FIT_LINE_STYLES,
    GRADIENT_COLORMAPS,
    LINE_WIDTH,
    MARKER_SIZE,
    apply_matplotlib_legend,
    apply_matplotlib_log10_axis,
    axes_box_size,
    categorical_palette,
    matplotlib_rcparams,
    plot_matplotlib_histogram,
    save_fixed_height_figure,
    set_fixed_axes_box,
)


PALETTE = categorical_palette("bright-high-contrast")


def save_single_panel(fig, ax, filename: str) -> None:
    set_fixed_axes_box(fig, ax, DEFAULT_ASPECT)
    save_fixed_height_figure(fig, Path(__file__).with_name(filename))
    plt.close(fig)


def gaussian_pdf(x: np.ndarray, sigma: float) -> np.ndarray:
    return np.exp(-0.5 * (x / sigma) ** 2) / (sigma * np.sqrt(2.0 * np.pi))


def xy_linear_fit() -> None:
    rng = np.random.default_rng(20260522)
    x = np.linspace(0.5, 9.5, 13)
    series = [(0.72, 0.35, "Device A"), (0.48, 1.15, "Device B"), (0.31, 1.85, "Device C")]
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))
    fit_x = np.linspace(0.0, 10.0, 300)

    for index, (slope, intercept, label) in enumerate(series):
        color = PALETTE[index]
        y = slope * x + intercept + rng.normal(0.0, 0.12, size=x.size)
        fit = np.polyfit(x, y, deg=1)
        ax.plot(x, y, linestyle="none", marker="o", markersize=MARKER_SIZE, color=color, label=label)
        ax.plot(fit_x, np.polyval(fit, fit_x), linestyle=FIT_LINE_STYLES[index], linewidth=LINE_WIDTH, color=color)

    ax.set_xlabel("Bias Voltage [V]")
    ax.set_ylabel("Response [a.u.]")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)
    save_single_panel(fig, ax, "xy_linear_fit_high_contrast.svg")


def gaussian_errorbar() -> None:
    rng = np.random.default_rng(20260523)
    sigmas = [0.75, 1.05, 1.45]
    bins = np.arange(-4.5, 4.51, 0.55)
    centers = 0.5 * (bins[:-1] + bins[1:])
    x_fit = np.linspace(-4.5, 4.5, 400)
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

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
            label=f"sigma = {sigma:.2f}",
        )
        ax.plot(x_fit, gaussian_pdf(x_fit, sigma), color=color, linestyle=FIT_LINE_STYLES[index], linewidth=LINE_WIDTH)

    ax.set_xlabel("Position [mm]")
    ax.set_ylabel("Probability Density [1/mm]")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(0, 0.7)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)
    save_single_panel(fig, ax, "gaussian_errorbar_high_contrast.svg")


def log_axis() -> None:
    x = np.linspace(0, 600, 260)
    scales = [0.7, 1.3, 2.2]
    offsets = [85, 130, 175]
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    for index, (scale, offset) in enumerate(zip(scales, offsets)):
        y = 1e-10 + scale * 8e-11 * np.exp((x - offset) / 145.0)
        y += scale * 1.8e-10 * (x / 600.0) ** 2
        ax.plot(x, y, color=PALETTE[index], linestyle=FIT_LINE_STYLES[index], linewidth=LINE_WIDTH, label=f"Sample {index + 1}")

    ax.set_xlabel("Bias Voltage [V]")
    ax.set_ylabel("Current [A]")
    ax.set_xlim(0, 600)
    ax.set_ylim(1e-10, 1e-6)
    ax.minorticks_on()
    apply_matplotlib_log10_axis(ax, axis="y")
    apply_matplotlib_legend(ax)
    save_single_panel(fig, ax, "log_axis_high_contrast.svg")


def many_curves_gradient() -> None:
    x = np.linspace(0, 12, 320)
    temperatures = np.arange(80, 241, 20)
    cmap = LinearSegmentedColormap.from_list("tao_bright_high_contrast", GRADIENT_COLORMAPS["bright-high-contrast"])
    colors = [cmap(value) for value in np.linspace(0.04, 1.0, len(temperatures))]
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    for index, (temperature, color) in enumerate(zip(temperatures, colors)):
        amplitude = 0.34 + 0.0022 * (temperature - temperatures[0])
        baseline = 0.018 * index
        y = baseline + amplitude * np.exp(-x / (3.8 + 0.012 * temperature))
        y *= 1.0 + 0.12 * np.sin(1.1 * x + index * 0.28)
        ax.plot(x, y, color=color, linestyle=FIT_LINE_STYLES[index % len(FIT_LINE_STYLES)], linewidth=LINE_WIDTH, label=f"{temperature} K")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Normalized Signal [a.u.]")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 0.95)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)
    save_single_panel(fig, ax, "many_curves_gradient_high_contrast.svg")


def multiple_histograms() -> None:
    rng = np.random.default_rng(20260526)
    bins = np.arange(-4.5, 4.51, 0.25)
    mode = "probability_density"
    samples = [
        rng.normal(-0.45, 0.95, size=900),
        rng.normal(0.05, 1.15, size=900),
        rng.normal(0.48, 1.35, size=900),
        rng.normal(0.90, 1.55, size=900),
    ]
    labels = ["sigma = 0.95", "sigma = 1.15", "sigma = 1.35", "sigma = 1.55"]
    fig, ax = plt.subplots(figsize=axes_box_size(DEFAULT_ASPECT))

    for data, label, color in zip(samples, labels, PALETTE):
        plot_matplotlib_histogram(ax, data, bins, mode, unit="mm", color=color, label=label)

    ax.set_xlabel("Measurement [mm]")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(0, 0.46)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)
    save_single_panel(fig, ax, "multiple_histograms_high_contrast.svg")


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    xy_linear_fit()
    gaussian_errorbar()
    log_axis()
    many_curves_gradient()
    multiple_histograms()


if __name__ == "__main__":
    main()

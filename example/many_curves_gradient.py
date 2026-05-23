#!/usr/bin/env python3
"""Example: Tao Style many curves with an outside framed legend."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apply_tao_style import (  # noqa: E402
    FIT_LINE_STYLES,
    GRADIENT_COLORMAPS,
    LINE_WIDTH,
    apply_matplotlib_legend,
    figure_size,
    matplotlib_rcparams,
)


def main() -> None:
    x = np.linspace(0, 12, 320)
    temperatures = np.arange(80, 241, 20)
    cmap = LinearSegmentedColormap.from_list("tao_dark_blue", GRADIENT_COLORMAPS["dark-blue"])
    colors = [cmap(value) for value in np.linspace(0.18, 1.0, len(temperatures))]

    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))
    fig, ax = plt.subplots(figsize=figure_size("5:3"))

    for index, (temperature, color) in enumerate(zip(temperatures, colors)):
        amplitude = 0.34 + 0.0022 * (temperature - temperatures[0])
        baseline = 0.018 * index
        y = baseline + amplitude * np.exp(-x / (3.8 + 0.012 * temperature))
        y *= 1.0 + 0.12 * np.sin(1.1 * x + index * 0.28)
        ax.plot(
            x,
            y,
            color=color,
            linestyle=FIT_LINE_STYLES[index % len(FIT_LINE_STYLES)],
            linewidth=LINE_WIDTH,
            label=f"{temperature} K",
        )

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Normalized Signal [a.u.]")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 0.95)
    ax.minorticks_on()
    apply_matplotlib_legend(ax)

    output = Path(__file__).with_suffix(".svg")
    fig.savefig(output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

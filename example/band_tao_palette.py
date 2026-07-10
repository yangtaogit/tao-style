#!/usr/bin/env python3
"""Example: Tao Style five curves with filled bands using the tao palette."""

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
    TAO_PALETTE,
    axes_box_size,
    matplotlib_rcparams,
    save_adaptive_figure,
    set_fixed_axes_box,
)


def main() -> None:
    plt.rcParams.update(matplotlib_rcparams(svg_fonttype="path"))

    x = np.linspace(0, 8, 300)
    n = 5
    colors = TAO_PALETTE[:n]
    labels = [f"Channel {i + 1}" for i in range(n)]
    offsets = np.linspace(-1.0, 1.0, n)
    errors = [0.10, 0.13, 0.11, 0.14, 0.12]

    fig, ax = plt.subplots(figsize=axes_box_size())
    for i, (off, err, label, color) in enumerate(zip(offsets, errors, labels, colors)):
        y = np.sin(x + i * 0.5) * np.exp(-0.1 * x) + off
        ax.fill_between(x, y - err, y + err, color=color, alpha=0.18, linewidth=0)
        ax.plot(x, y, color=color, linewidth=1.0, label=label)

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Signal")
    ax.legend(fontsize=8, frameon=False)

    set_fixed_axes_box(fig, ax)
    output = Path(__file__).with_suffix(".svg")
    save_adaptive_figure(fig, output)
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.apply_tao_style import (  # noqa: E402
    PALETTE,
    apply_matplotlib_legend,
    axes_box_size,
    matplotlib_rcparams,
    save_adaptive_figure,
    set_fixed_axes_box,
)

plt.rcParams.update(matplotlib_rcparams())

OUT = Path(__file__).resolve().parent
ASPECT = "2:3"

x = np.linspace(0, 8, 300)
fig, ax = plt.subplots(figsize=axes_box_size(ASPECT))

ax.plot(x, 0.85 + 0.28 * np.sin(x), color=PALETTE[0], label="Sample 1")
ax.plot(x, 0.55 + 0.22 * np.cos(1.2 * x), color=PALETTE[1], linestyle="--", label="Sample 2")
ax.plot(x, 0.32 + 0.18 * np.sin(0.8 * x + 1.0), color=PALETTE[2], linestyle=":", label="Sample 3")

ax.set_xlabel("X Label [Unit]")
ax.set_ylabel("Y Label [Unit]")
ax.set_xlim(0, 8)
ax.set_ylim(0, 1.25)
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
apply_matplotlib_legend(ax, outside=False, loc="upper right")

set_fixed_axes_box(fig, ax, aspect=ASPECT)
save_adaptive_figure(fig, OUT / "portrait_2_3_curves.svg")
plt.close(fig)

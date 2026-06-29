#!/usr/bin/env python3
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap
from matplotlib.ticker import AutoMinorLocator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.apply_tao_style import (  # noqa: E402
    add_matplotlib_colorbar,
    axes_box_size,
    gradient_colormap,
    matplotlib_rcparams,
    save_fixed_canvas_figure,
    set_fixed_axes_box,
)

plt.rcParams.update(matplotlib_rcparams())

OUT = Path(__file__).resolve().parent
ASPECT = "2:3"

x = np.linspace(-3, 3, 180)
y = np.linspace(-3, 3, 220)
xx, yy = np.meshgrid(x, y)
zz = (
    np.exp(-((xx - 0.8) ** 2 + (yy + 0.7) ** 2) / 1.2)
    + 0.65 * np.exp(-((xx + 1.1) ** 2 + (yy - 1.0) ** 2) / 0.8)
)

levels = np.linspace(zz.min(), zz.max(), 9)
cmap = LinearSegmentedColormap.from_list("tao_dark_blue", gradient_colormap("dark-blue"), N=len(levels) - 1)
norm = BoundaryNorm(levels, cmap.N)

fig, ax = plt.subplots(figsize=axes_box_size(ASPECT))
filled = ax.contourf(xx, yy, zz, levels=levels, cmap=cmap, norm=norm)
ax.contour(xx, yy, zz, levels=levels, colors="#000000", linewidths=0.25, alpha=0.45)

ax.set_xlabel("X Label [Unit]")
ax.set_ylabel("Y Label [Unit]")
ax.set_xlim(x.min(), x.max())
ax.set_ylim(y.min(), y.max())
ax.xaxis.set_minor_locator(AutoMinorLocator(2))
ax.yaxis.set_minor_locator(AutoMinorLocator(2))

set_fixed_axes_box(fig, ax, aspect=ASPECT)
cbar = add_matplotlib_colorbar(fig, ax, filled, pad=0.13, width=0.08)
cbar.set_label("Signal [Unit]")
save_fixed_canvas_figure(fig, OUT / "portrait_2_3_contour.svg", aspect=ASPECT)
plt.close(fig)

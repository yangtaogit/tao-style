#!/usr/bin/env python3
"""Starter plotting style helper for tao-style.

The values are intentionally conservative until Tao confirms specific
preferences in references/style-profile.md.
"""

from __future__ import annotations

import argparse
import json
import math

try:
    from cycler import cycler as _cycler_factory
except ImportError:  # pragma: no cover - Matplotlib installs usually include cycler.
    _cycler_factory = None


CORE_PALETTE = [
    "#2A2F80",
    "#000000",
    "#808080",
]
EMPHASIS_PALETTE = [
    "#B04A4A",
]
PALETTE = [
    "#2A2F80",
    "#000000",
    "#808080",
    "#BDBDBD",
    "#4378BC",
    "#6FCCDE",
    "#3953A5",
]
EXTENDED_PALETTE = [
    "#BDBDBD",
    "#4378BC",
    "#6FCCDE",
    "#3953A5",
]
TAU_PALETTE = [
    "#2A2F80",
    "#3953A5",
    "#4378BC",
    "#6FCCDE",
    "#99CB6F",
    "#F6EB14",
    "#F67F21",
    "#EE2024",
    "#7D1415",
]
CATEGORICAL_PALETTES = {
    "default": PALETTE,
    "core": CORE_PALETTE,
    "extended": EXTENDED_PALETTE,
    "emphasis": EMPHASIS_PALETTE,
    "tau": TAU_PALETTE,
}
GRADIENT_COLORMAPS = {
    "dark-blue": ["#EEF1F8", "#C8D2EA", "#8799CF", "#4E5CA4", "#2A2F80"],
    "gray": ["#EDEDED", "#C9C9C9", "#9A9A9A", "#5F5F5F", "#000000"],
    "tau": TAU_PALETTE,
}

FONT_FAMILY = [
    "Helvetica",
    "Arimo",
    "Noto Sans",
    "Nimbus Sans",
    "SimSun",
    "Songti SC",
    "Noto Serif CJK SC",
    "DejaVu Sans",
]
MATH_FONTSET = "cm"

AXIS_COLOR = "#000000"
AXIS_LINE_WIDTH = 0.6
MAJOR_TICK_WIDTH = 0.6
MINOR_TICK_WIDTH = 0.3
AXIS_LABEL_SIZE = 9
TICK_LABEL_SIZE = 8
LEGEND_FONT_SIZE = 8
LEGEND_MANY_ITEMS_THRESHOLD = 5
LEGEND_OUTSIDE_MAX_ROWS = 8
LINE_WIDTH = 1.0
FIT_LINE_WIDTH = LINE_WIDTH
FIT_LINE_STYLES = ["-", "--", ":", "-."]
FIT_LINE_STYLE = FIT_LINE_STYLES[0]
FIT_LINE_ALPHA = 1.0
MARKER_SIZE = 3.2
MARKER_EDGE_WIDTH = 0.7
ERRORBAR_LINE_WIDTH = 0.6
ERRORBAR_CAP_SIZE = 1.6
HISTOGRAM_FILL_ALPHA = 0.28
COLORBAR_WIDTH_IN = 0.08
COLORBAR_PAD_IN = 0.12
DEFAULT_ASPECT = "3:2"
DEFAULT_AXES_HEIGHT_IN = 2.0
DEFAULT_AXES_WIDTH_IN = 3.0
DEFAULT_CANVAS_LEFT_IN = 0.42
DEFAULT_CANVAS_BOTTOM_IN = 0.35
DEFAULT_CANVAS_RIGHT_IN = 0.08
DEFAULT_CANVAS_TOP_IN = 0.05
DEFAULT_FIGURE_WIDTH_IN = DEFAULT_AXES_WIDTH_IN
DEFAULT_PLOTLY_HEIGHT_PX = 400
DEFAULT_PLOTLY_WIDTH_PX = 600
HISTOGRAM_Y_MODES = ("count", "probability_density")
FIGURE_ASPECTS = {
    "1:1": 1.0,
    "3:2": 3.0 / 2.0,
    "5:3": 5.0 / 3.0,
    "2:3": 2.0 / 3.0,
    "3:5": 3.0 / 5.0,
}
FIXED_WIDTH_ASPECTS = {"2:3", "3:5"}
SUPERSCRIPT_TRANSLATION = str.maketrans(
    {
        "-": "⁻",
        "+": "⁺",
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
    }
)


def axes_box_size(
    aspect: str = DEFAULT_ASPECT,
    width: float | None = None,
    height: float = DEFAULT_AXES_HEIGHT_IN,
) -> tuple[float, float]:
    """Return the target physical size of the plotting axes box in inches.

    By default Tao Style fixes landscape/square axes-box height at 2.0 in and
    derives the width from the requested ratio: 1:1 -> 2.0 x 2.0 in, 3:2 ->
    3.0 x 2.0 in, and 5:3 -> 3.33 x 2.0 in. Portrait ratios are treated as the
    rotated forms of the landscape sizes and fix width at 2.0 in: 2:3 -> 2.0 x
    3.0 in and 3:5 -> 2.0 x 3.33 in. Passing width keeps backward-compatible
    behavior for target-medium-specific figures.
    """

    if aspect not in FIGURE_ASPECTS:
        allowed = ", ".join(sorted(FIGURE_ASPECTS))
        raise ValueError(f"Unknown aspect ratio {aspect!r}. Allowed: {allowed}")
    ratio = FIGURE_ASPECTS[aspect]
    if width is not None:
        return (width, width / ratio)
    if aspect in FIXED_WIDTH_ASPECTS:
        return (height, height / ratio)
    return (height * ratio, height)


def figure_size(
    aspect: str = DEFAULT_ASPECT,
    width: float | None = None,
    height: float = DEFAULT_AXES_HEIGHT_IN,
) -> tuple[float, float]:
    """Return the legacy initial Matplotlib figure size for a target axes box.

    Tao Style now fixes the axes box size, not the final canvas size. Use this
    value as a convenient initial figure size, then call set_fixed_axes_box()
    before saving so labels and outside legends can expand the canvas without
    changing the plotting box.
    """

    return axes_box_size(aspect, width=width, height=height)


def set_fixed_axes_box(
    fig,
    ax,
    aspect: str = DEFAULT_ASPECT,
    width: float | None = None,
    *,
    height: float = DEFAULT_AXES_HEIGHT_IN,
    left: float = DEFAULT_CANVAS_LEFT_IN,
    bottom: float = DEFAULT_CANVAS_BOTTOM_IN,
    right: float = DEFAULT_CANVAS_RIGHT_IN,
    top: float = DEFAULT_CANVAS_TOP_IN,
):
    """Resize a Matplotlib figure so the axes box has a fixed inch size.

    The axes rectangle itself remains fixed, making the visual plotting box
    consistent across figures. Pair this with save_adaptive_figure() so the
    exported canvas can expand naturally for titles, labels, legends, colorbars,
    and annotations without changing the plotting-box size.
    """

    axes_width, axes_height = axes_box_size(aspect, width=width, height=height)
    figure_width = left + axes_width + right
    figure_height = bottom + axes_height + top
    fig.set_size_inches(figure_width, figure_height, forward=True)
    ax.set_position([
        left / figure_width,
        bottom / figure_height,
        axes_width / figure_width,
        axes_height / figure_height,
    ])
    return fig, ax


def equal_xy_axes_box_size(
    x_range: float,
    y_range: float,
    *,
    x_width: float = DEFAULT_AXES_WIDTH_IN,
) -> tuple[float, float]:
    """Return axes-box size for equal-unit XY plots with fixed X width.

    Use when X and Y represent comparable physical lengths or positions and one
    data unit should have the same visual length in both directions. The X-axis
    box width stays at the default 3.0 in; the Y-axis height follows the data
    range ratio.
    """

    if x_range <= 0 or y_range <= 0:
        raise ValueError("x_range and y_range must be positive for equal XY axes")
    return (x_width, x_width * y_range / x_range)


def set_equal_xy_axes_box(
    fig,
    ax,
    *,
    xlim: tuple[float, float] | None = None,
    ylim: tuple[float, float] | None = None,
    x_width: float = DEFAULT_AXES_WIDTH_IN,
    left: float = DEFAULT_CANVAS_LEFT_IN,
    bottom: float = DEFAULT_CANVAS_BOTTOM_IN,
    right: float = DEFAULT_CANVAS_RIGHT_IN,
    top: float = DEFAULT_CANVAS_TOP_IN,
):
    """Resize a Matplotlib axes box for equal-unit XY geometry plots.

    The X-axis box width is fixed, while the Y-axis box height follows the
    plotted data range so equal X/Y units have equal visual length.
    """

    if xlim is None:
        xlim = ax.get_xlim()
    else:
        ax.set_xlim(*xlim)
    if ylim is None:
        ylim = ax.get_ylim()
    else:
        ax.set_ylim(*ylim)

    x_range = abs(float(xlim[1]) - float(xlim[0]))
    y_range = abs(float(ylim[1]) - float(ylim[0]))
    axes_width, axes_height = equal_xy_axes_box_size(x_range, y_range, x_width=x_width)
    figure_width = left + axes_width + right
    figure_height = bottom + axes_height + top
    fig.set_size_inches(figure_width, figure_height, forward=True)
    ax.set_position([
        left / figure_width,
        bottom / figure_height,
        axes_width / figure_width,
        axes_height / figure_height,
    ])
    ax.set_aspect("equal", adjustable="box")
    return fig, ax


def _set_axes_position_inches(fig, ax, bounds: tuple[float, float, float, float]):
    """Set an axes position from inch bounds in figure coordinates."""

    figure_width, figure_height = fig.get_size_inches()
    left, bottom, width, height = bounds
    ax.set_position([
        left / figure_width,
        bottom / figure_height,
        width / figure_width,
        height / figure_height,
    ])


def add_matplotlib_colorbar(
    fig,
    ax,
    mappable,
    *,
    side: str = "right",
    width: float = COLORBAR_WIDTH_IN,
    pad: float = COLORBAR_PAD_IN,
    expand_canvas: bool = True,
    **kwargs,
):
    """Add a Tao Style colorbar without changing the fixed axes-box size.

    For a right-side vertical colorbar, the helper positions the colorbar in
    physical inch units relative to the axes box. If needed, it expands the
    canvas width and restores the original axes-box inch bounds, so portrait
    figures keep their fixed plotting-box width while avoiding colorbar overlap.
    """

    side = side.lower()
    if side not in {"right"}:
        raise ValueError("Only side='right' is currently supported")

    figure_width, figure_height = fig.get_size_inches()
    ax_pos = ax.get_position()
    ax_bounds = (
        ax_pos.x0 * figure_width,
        ax_pos.y0 * figure_height,
        ax_pos.width * figure_width,
        ax_pos.height * figure_height,
    )
    left, bottom, axes_width, axes_height = ax_bounds
    cbar_left = left + axes_width + pad
    cbar_bottom = bottom
    cbar_width = width
    cbar_height = axes_height
    required_width = cbar_left + cbar_width + DEFAULT_CANVAS_RIGHT_IN

    if expand_canvas and required_width > figure_width:
        fig.set_size_inches(required_width, figure_height, forward=True)
        _set_axes_position_inches(fig, ax, ax_bounds)
        figure_width = required_width

    cax = fig.add_axes([
        cbar_left / figure_width,
        cbar_bottom / figure_height,
        cbar_width / figure_width,
        cbar_height / figure_height,
    ])
    colorbar = fig.colorbar(mappable, cax=cax, **kwargs)
    colorbar.outline.set_linewidth(AXIS_LINE_WIDTH)
    fig._tao_style_right_external_artist = True
    return colorbar


def fixed_height_bbox_inches(fig, *, pad_inches: float | None = None):
    """Return a savefig bbox with fixed canvas height and adaptive width.

    The vertical export range is the full current figure height. The horizontal
    range expands as needed to include artists found by Matplotlib's tight-bbox
    pass, such as long y tick labels, y labels, outside legends, or colorbars.
    """

    from matplotlib import rcParams
    from matplotlib.transforms import Bbox

    if pad_inches is None:
        pad_inches = float(rcParams.get("savefig.pad_inches", 0.03))

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    tight = fig.get_tightbbox(renderer)
    figure_width, figure_height = fig.get_size_inches()
    x0 = min(0.0, tight.x0 - pad_inches)
    x1 = max(float(figure_width), tight.x1 + pad_inches)
    return Bbox.from_extents(x0, 0.0, x1, float(figure_height))


def fixed_width_bbox_inches(fig, *, pad_inches: float | None = None):
    """Return a savefig bbox with fixed canvas width and adaptive height.

    This is the portrait counterpart to fixed_height_bbox_inches(). The
    horizontal export range is the full current figure width. The vertical range
    expands as needed to include artists found by Matplotlib's tight-bbox pass.
    """

    from matplotlib import rcParams
    from matplotlib.transforms import Bbox

    if pad_inches is None:
        pad_inches = float(rcParams.get("savefig.pad_inches", 0.03))

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    tight = fig.get_tightbbox(renderer)
    figure_width, figure_height = fig.get_size_inches()
    y0 = min(0.0, tight.y0 - pad_inches)
    y1 = max(float(figure_height), tight.y1 + pad_inches)
    return Bbox.from_extents(0.0, y0, float(figure_width), y1)


def adaptive_bbox_inches(fig, *, pad_inches: float | None = None):
    """Return a tight savefig bbox with Tao Style's default safety margin."""

    from matplotlib import rcParams

    if pad_inches is None:
        pad_inches = float(rcParams.get("savefig.pad_inches", 0.03))

    fig.canvas.draw()
    return "tight", pad_inches


def save_adaptive_figure(fig, filename, *, pad_inches: float | None = None, **kwargs):
    """Save a Tao Style figure with fixed axes box and adaptive canvas.

    Use this after set_fixed_axes_box(). The axes box keeps its physical size,
    while the exported canvas is cropped around all visible content, including
    titles, tick labels, axis labels, legends, colorbars, and annotations.
    """

    bbox_inches, resolved_pad = adaptive_bbox_inches(fig, pad_inches=pad_inches)
    kwargs.setdefault("bbox_inches", bbox_inches)
    kwargs.setdefault("pad_inches", resolved_pad)
    return fig.savefig(filename, **kwargs)


def save_fixed_canvas_figure(
    fig,
    filename,
    *,
    aspect: str = DEFAULT_ASPECT,
    fixed_dimension: str = "auto",
    pad_inches: float | None = None,
    **kwargs,
):
    """Save a figure with a fixed exported canvas dimension.

    This is a legacy/special-purpose helper. Tao Style's default is now
    save_adaptive_figure(), which fixes the axes box and lets the canvas adapt
    to all visible content. Use this only when a target layout explicitly
    requires a fixed exported canvas height or width.
    """

    if aspect not in FIGURE_ASPECTS:
        allowed = ", ".join(sorted(FIGURE_ASPECTS))
        raise ValueError(f"Unknown aspect ratio {aspect!r}. Allowed: {allowed}")
    if fixed_dimension == "auto":
        fixed_dimension = "height"
    if fixed_dimension not in {"width", "height"}:
        raise ValueError("fixed_dimension must be 'auto', 'width', or 'height'")
    if fixed_dimension == "width":
        bbox_inches = fixed_width_bbox_inches(fig, pad_inches=pad_inches)
    else:
        bbox_inches = fixed_height_bbox_inches(fig, pad_inches=pad_inches)
    kwargs.setdefault("bbox_inches", bbox_inches)
    kwargs.setdefault("pad_inches", 0.0)
    return fig.savefig(filename, **kwargs)


def save_fixed_height_figure(fig, filename, *, pad_inches: float | None = None, **kwargs):
    """Save a Matplotlib figure with fixed height and adaptive width.

    Legacy helper. Prefer save_adaptive_figure() unless a target layout
    explicitly requires fixed exported canvas height.
    """

    kwargs.setdefault("bbox_inches", fixed_height_bbox_inches(fig, pad_inches=pad_inches))
    kwargs.setdefault("pad_inches", 0.0)
    return fig.savefig(filename, **kwargs)


def plotly_dimensions(
    aspect: str = DEFAULT_ASPECT,
    width: int | None = None,
    height: int = DEFAULT_PLOTLY_HEIGHT_PX,
) -> dict[str, int]:
    """Return Plotly pixel dimensions for a width:height aspect ratio.

    Plotly needs explicit pixel dimensions. Use the axes-box ratio as a
    starting point, then let layout margins adapt to titles, labels, legends,
    colorbars, and annotations where the target renderer supports it.
    """

    if aspect not in FIGURE_ASPECTS:
        allowed = ", ".join(sorted(FIGURE_ASPECTS))
        raise ValueError(f"Unknown aspect ratio {aspect!r}. Allowed: {allowed}")
    ratio = FIGURE_ASPECTS[aspect]
    if width is not None:
        return {"width": width, "height": round(width / ratio)}
    return {"width": round(height * ratio), "height": height}


def matplotlib_rcparams(serializable: bool = False, svg_fonttype: str = "path") -> dict[str, object]:
    """Return a starter rcParams dictionary for Tao Style plots.

    The default SVG export converts text to paths so font appearance does not
    depend on the fonts installed where the SVG is opened. PDF export keeps
    embedded TrueType text by default via ``pdf.fonttype = 42``.
    """

    if svg_fonttype not in {"none", "path"}:
        raise ValueError("svg_fonttype must be 'none' or 'path'")

    prop_cycle = _cycler_expr("color", PALETTE)
    if not serializable and _cycler_factory is not None:
        prop_cycle = _cycler_factory("color", PALETTE)

    return {
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.03,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": AXIS_COLOR,
        "axes.labelcolor": "#111111",
        "axes.linewidth": AXIS_LINE_WIDTH,
        "axes.grid": False,
        "axes.spines.left": True,
        "axes.spines.right": True,
        "axes.spines.top": True,
        "axes.spines.bottom": True,
        "axes.prop_cycle": prop_cycle,
        "font.family": "sans-serif",
        "font.sans-serif": FONT_FAMILY,
        "mathtext.fontset": MATH_FONTSET,
        "font.size": TICK_LABEL_SIZE,
        "axes.titlesize": AXIS_LABEL_SIZE,
        "axes.labelsize": AXIS_LABEL_SIZE,
        "xtick.labelsize": TICK_LABEL_SIZE,
        "ytick.labelsize": TICK_LABEL_SIZE,
        "legend.fontsize": LEGEND_FONT_SIZE,
        "legend.edgecolor": AXIS_COLOR,
        "lines.linewidth": LINE_WIDTH,
        "lines.markersize": MARKER_SIZE,
        "lines.markeredgewidth": MARKER_EDGE_WIDTH,
        "xtick.color": AXIS_COLOR,
        "ytick.color": AXIS_COLOR,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "xtick.major.size": 4.0,
        "ytick.major.size": 4.0,
        "xtick.minor.size": 2.4,
        "ytick.minor.size": 2.4,
        "xtick.major.width": MAJOR_TICK_WIDTH,
        "ytick.major.width": MAJOR_TICK_WIDTH,
        "xtick.minor.width": MINOR_TICK_WIDTH,
        "ytick.minor.width": MINOR_TICK_WIDTH,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "pdf.use14corefonts": False,
        "ps.fonttype": 42,
        "ps.useafm": False,
        "svg.fonttype": svg_fonttype,
    }


def matplotlib_legend_kwargs(outside: bool = False, n_items: int | None = None) -> dict[str, object]:
    """Return Tao Style legend keyword arguments for Matplotlib."""

    if outside:
        ncol = 1
        if n_items is not None and n_items > LEGEND_OUTSIDE_MAX_ROWS:
            ncol = math.ceil(n_items / LEGEND_OUTSIDE_MAX_ROWS)
        return {
            "loc": "center left",
            "bbox_to_anchor": (1.02, 0.5),
            "frameon": True,
            "ncol": ncol,
            "borderaxespad": 0.0,
        }
    return {"frameon": False}


def apply_matplotlib_legend(ax, outside=None, **kwargs):
    """Apply Tao Style legend placement and frame styling to a Matplotlib axes."""

    handles, labels = ax.get_legend_handles_labels()
    if outside is None:
        outside = len(labels) > LEGEND_MANY_ITEMS_THRESHOLD

    legend_kwargs = matplotlib_legend_kwargs(outside, len(labels))
    legend_kwargs.update(kwargs)
    legend = ax.legend(**legend_kwargs)
    if outside and legend is not None:
        frame = legend.get_frame()
        frame.set_edgecolor(AXIS_COLOR)
        frame.set_linewidth(AXIS_LINE_WIDTH)
        frame.set_facecolor("white")
        frame.set_alpha(1.0)
        ax.figure._tao_style_right_external_artist = True
    return legend


def base10_log_tick_label(value: float, _position=None) -> str:
    """Return a plain-text superscript label such as 10⁻⁶ for log ticks."""

    if value <= 0:
        return ""

    exponent = math.log10(value)
    rounded = round(exponent)
    if not math.isclose(exponent, rounded, rel_tol=0.0, abs_tol=1e-10):
        return ""
    return "10" + str(int(rounded)).translate(SUPERSCRIPT_TRANSLATION)


def apply_matplotlib_log10_axis(ax, axis: str = "y"):
    """Apply Tao Style base-10 log tick formatting to a Matplotlib axis."""

    from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter

    if axis == "x":
        ax.set_xscale("log")
        target_axis = ax.xaxis
    elif axis == "y":
        ax.set_yscale("log")
        target_axis = ax.yaxis
    else:
        raise ValueError("axis must be 'x' or 'y'")

    target_axis.set_major_locator(LogLocator(base=10))
    target_axis.set_minor_locator(LogLocator(base=10, subs=tuple(i / 10 for i in range(2, 10))))
    target_axis.set_major_formatter(FuncFormatter(base10_log_tick_label))
    target_axis.set_minor_formatter(NullFormatter())
    return target_axis


def normalize_histogram_y_mode(mode: str) -> str:
    """Return a validated Tao Style histogram y-axis mode."""

    normalized = mode.strip().lower().replace("-", "_")
    aliases = {
        "counts": "count",
        "raw_count": "count",
        "raw_counts": "count",
        "density": "probability_density",
        "pdf": "probability_density",
        "probability_density": "probability_density",
        "normalized_density": "probability_density",
        "normalised_density": "probability_density",
    }
    normalized = aliases.get(normalized, normalized)
    if normalized not in HISTOGRAM_Y_MODES:
        allowed = ", ".join(HISTOGRAM_Y_MODES)
        raise ValueError(f"Unknown histogram y-axis mode {mode!r}. Allowed: {allowed}")
    return normalized


def histogram_ylabel(mode: str, unit: str = "Unit") -> str:
    """Return the y-axis label for a Tao Style histogram mode."""

    normalized = normalize_histogram_y_mode(mode)
    if normalized == "count":
        return "Count"
    return f"Probability Density [1/{unit}]"


def histogram_density(mode: str) -> bool:
    """Return the Matplotlib density flag for a Tao Style histogram mode."""

    normalized = normalize_histogram_y_mode(mode)
    return normalized == "probability_density"


def histogram_kwargs(mode: str) -> dict[str, bool]:
    """Return Matplotlib hist keyword arguments for a Tao Style y-axis mode."""

    return {"density": histogram_density(mode)}


def plot_matplotlib_histogram(
    ax,
    data,
    bins,
    mode: str,
    *,
    unit: str = "Unit",
    color: str = PALETTE[0],
    label: str | None = None,
    fill_alpha: float = HISTOGRAM_FILL_ALPHA,
    linewidth: float = LINE_WIDTH,
    **kwargs,
):
    """Draw a Tao Style histogram as bin-edge steps with light fill."""

    base_kwargs = histogram_kwargs(mode)
    base_kwargs.update(kwargs)
    fill = ax.hist(
        data,
        bins=bins,
        histtype="stepfilled",
        facecolor=color,
        edgecolor="none",
        alpha=fill_alpha,
        label=None,
        **base_kwargs,
    )
    outline = ax.hist(
        data,
        bins=bins,
        histtype="step",
        color=color,
        linewidth=linewidth,
        label=label,
        **base_kwargs,
    )
    ax.set_ylabel(histogram_ylabel(mode, unit=unit))
    return fill, outline


def apply_matplotlib_3d_style(
    ax,
    *,
    xlabel: str = "X",
    ylabel: str = "Y",
    zlabel: str = "Z",
    labelpad: float = -4.0,
    tick_pad: float = -3.0,
    projection: str = "persp",
):
    """Apply Tao typography to Matplotlib's default 3D axes style."""

    if projection:
        ax.set_proj_type(projection)

    ax.set_xlabel(xlabel, labelpad=labelpad)
    ax.set_ylabel(ylabel, labelpad=labelpad)
    ax.set_zlabel(zlabel, labelpad=labelpad)
    ax.tick_params(labelsize=TICK_LABEL_SIZE, colors=AXIS_COLOR, pad=tick_pad)
    ax.grid(True)

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        try:
            axis.pane.set_facecolor((0.95, 0.95, 0.95, 1.0))
            axis.pane.set_edgecolor((0.95, 0.95, 0.95, 1.0))
        except AttributeError:
            pass
        try:
            axis._axinfo["grid"]["color"] = (0.62, 0.62, 0.62, 1.0)
            axis._axinfo["grid"]["linestyle"] = ":"
            axis._axinfo["grid"]["linewidth"] = 0.2
            axis._axinfo["tick"]["inward_factor"] = 0.0
            axis._axinfo["tick"]["outward_factor"] = 0.2
        except (AttributeError, KeyError):
            pass

    for label in (ax.xaxis.label, ax.yaxis.label, ax.zaxis.label):
        label.set_size(AXIS_LABEL_SIZE)
        label.set_color("#111111")

    return ax


def hide_matplotlib_3d_axes(ax):
    """Hide Matplotlib 3D axes, ticks, panes, and grid for data-first 3D figures."""

    ax.set_axis_off()
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        try:
            axis.pane.set_visible(False)
            axis.line.set_color((1, 1, 1, 0))
        except AttributeError:
            pass
        try:
            axis._axinfo["grid"]["color"] = (1, 1, 1, 0)
            axis._axinfo["tick"]["color"] = (1, 1, 1, 0)
        except (AttributeError, KeyError):
            pass
    ax.set_facecolor((1, 1, 1, 0))
    return ax


def add_matplotlib_3d_xyz_marker(
    fig,
    *,
    elev: float,
    azim: float,
    position=(0.155, 0.145, 0.125, 0.125),
    length: float = 0.78,
    label_size: float = 6.5,
    linewidth: float = 0.8,
):
    """Add a compact in-figure XYZ direction marker for hidden-axis 3D figures."""

    marker = fig.add_axes(position, projection="3d")
    marker.view_init(elev=elev, azim=azim)
    marker.set_proj_type("persp")
    hide_matplotlib_3d_axes(marker)

    label_pos = length + 0.14
    label_kw = {"color": AXIS_COLOR, "fontsize": label_size, "ha": "center", "va": "center"}
    marker.quiver(0, 0, 0, length, 0, 0, color=AXIS_COLOR, linewidth=linewidth, arrow_length_ratio=0.22)
    marker.quiver(0, 0, 0, 0, length, 0, color=AXIS_COLOR, linewidth=linewidth, arrow_length_ratio=0.22)
    marker.quiver(0, 0, 0, 0, 0, length, color=AXIS_COLOR, linewidth=linewidth, arrow_length_ratio=0.22)
    marker.text(label_pos, 0, 0, "X", **label_kw)
    marker.text(0, label_pos, 0, "Y", **label_kw)
    marker.text(0, 0, label_pos, "Z", **label_kw)
    marker.set_xlim(0, 1.0)
    marker.set_ylim(0, 1.0)
    marker.set_zlim(0, 1.0)
    marker.set_box_aspect((1, 1, 1))
    return marker


def apply_matplotlib_hidden_3d_style(ax, fig=None, *, elev: float | None = None, azim: float | None = None):
    """Apply Tao Style's optional hidden-axis 3D layout helpers."""

    ax.set_proj_type("persp")
    hide_matplotlib_3d_axes(ax)
    if fig is not None and elev is not None and azim is not None:
        add_matplotlib_3d_xyz_marker(fig, elev=elev, azim=azim)
    return ax


def plotly_axis_style() -> dict[str, object]:
    """Return Tao Style axis settings for Plotly xaxes/yaxes."""

    return {
        "showline": True,
        "showticklabels": True,
        "linecolor": AXIS_COLOR,
        "linewidth": AXIS_LINE_WIDTH,
        "ticks": "inside",
        "tickwidth": MAJOR_TICK_WIDTH,
        "tickcolor": AXIS_COLOR,
        "mirror": "allticks",
        "minor_ticks": "inside",
        "minor_tickwidth": MINOR_TICK_WIDTH,
        "gridcolor": "rgba(0,0,0,0)",
        "zeroline": False,
    }


def plotly_legend_style(outside: bool = False) -> dict[str, object]:
    """Return Tao Style legend settings for Plotly."""

    if outside:
        return {
            "orientation": "v",
            "xanchor": "left",
            "x": 1.02,
            "yanchor": "top",
            "y": 1.0,
            "bgcolor": "white",
            "bordercolor": AXIS_COLOR,
            "borderwidth": AXIS_LINE_WIDTH,
        }
    return {
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
    }


def plotly_layout_style(aspect: str = DEFAULT_ASPECT, width: int | None = None) -> dict[str, object]:
    """Return Tao Style layout settings that are independent of data traces."""

    return {
        **plotly_dimensions(aspect, width),
        "plot_bgcolor": "white",
        "paper_bgcolor": "white",
        "colorway": PALETTE,
        "legend": plotly_legend_style(False),
        "margin": {"l": 0, "r": 8, "t": 30, "b": 0},
    }


def apply_plotly_style(
    fig,
    aspect: str = DEFAULT_ASPECT,
    width: int | None = None,
    legend_outside: bool = False,
):
    """Apply Tao Style axis and layout settings to a Plotly figure."""

    fig.update_layout(**plotly_layout_style(aspect, width))
    fig.update_layout(legend=plotly_legend_style(legend_outside))
    axis_style = plotly_axis_style()
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    return fig


def categorical_palette(name: str = "default") -> list[str]:
    """Return a preferred Tao Style categorical palette."""

    if name not in CATEGORICAL_PALETTES:
        allowed = ", ".join(sorted(CATEGORICAL_PALETTES))
        raise ValueError(f"Unknown categorical palette {name!r}. Allowed: {allowed}")
    return CATEGORICAL_PALETTES[name]


def gradient_colormap(name: str = "dark-blue") -> list[str]:
    """Return a preferred Tao Style color gradient."""

    if name not in GRADIENT_COLORMAPS:
        allowed = ", ".join(sorted(GRADIENT_COLORMAPS))
        raise ValueError(f"Unknown gradient colormap {name!r}. Allowed: {allowed}")
    return GRADIENT_COLORMAPS[name]


def _cycler_expr(key: str, values: list[str]) -> str:
    """Return a cycler expression string for JSON and mplstyle output."""

    quoted = ", ".join(repr(value) for value in values)
    return f"cycler('{key}', [{quoted}])"


def _as_mplstyle(style: dict[str, object]) -> str:
    lines = []
    for key in sorted(style):
        value = style[key]
        if isinstance(value, list):
            rendered = ", ".join(str(item) for item in value)
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Print starter Tao Style plotting settings.")
    parser.add_argument(
        "--target",
        choices=("matplotlib", "plotly"),
        default="matplotlib",
        help="Style target to print.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "mplstyle"),
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--aspect",
        choices=sorted(FIGURE_ASPECTS),
        default=DEFAULT_ASPECT,
        help="Output figure width:height ratio.",
    )
    args = parser.parse_args()

    if args.target == "plotly":
        if args.format == "mplstyle":
            parser.error("--format mplstyle is only valid with --target matplotlib")
        print(
            json.dumps(
                {
                    "layout": plotly_layout_style(args.aspect),
                    "xaxis": plotly_axis_style(),
                    "yaxis": plotly_axis_style(),
                    "legend": {
                        "inside": plotly_legend_style(False),
                        "outside": plotly_legend_style(True),
                    },
                    "gradients": GRADIENT_COLORMAPS,
                    "palettes": CATEGORICAL_PALETTES,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return

    style = matplotlib_rcparams(serializable=True)
    if args.format == "json":
        print(
            json.dumps(
                {
                    "aspect": args.aspect,
                    "axes_box_size": axes_box_size(args.aspect),
                    "canvas_rule": "adaptive_to_visible_content",
                    "figure_size": figure_size(args.aspect),
                    "legend": {
                        "inside": matplotlib_legend_kwargs(False),
                        "outside": matplotlib_legend_kwargs(True),
                    },
                    "gradients": GRADIENT_COLORMAPS,
                    "palettes": CATEGORICAL_PALETTES,
                    "histogram": {
                        "y_modes": HISTOGRAM_Y_MODES,
                        "fill_alpha": HISTOGRAM_FILL_ALPHA,
                        "labels": {
                            mode: histogram_ylabel(mode)
                            for mode in HISTOGRAM_Y_MODES
                        },
                    },
                    "rcParams": style,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(_as_mplstyle(style), end="")


if __name__ == "__main__":
    main()

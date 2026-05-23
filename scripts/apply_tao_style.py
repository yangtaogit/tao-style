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


PALETTE = [
    "#000080",
    "#6CA6CD",
    "#000000",
    "#808080",
    "#B04A4A",
]
GRADIENT_COLORMAPS = {
    "dark-blue": ["#E6EEF6", "#AFCBE3", "#6CA6CD", "#2F5F9F", "#000080"],
    "gray": ["#EDEDED", "#C9C9C9", "#9A9A9A", "#5F5F5F", "#000000"],
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
AXIS_LINE_WIDTH = 1.0
MAJOR_TICK_WIDTH = 1.0
MINOR_TICK_WIDTH = 0.5
AXIS_LABEL_SIZE = 9
TICK_LABEL_SIZE = 8
LEGEND_FONT_SIZE = 8
LEGEND_MANY_ITEMS_THRESHOLD = 5
LINE_WIDTH = 1.0
FIT_LINE_WIDTH = LINE_WIDTH
FIT_LINE_STYLES = ["-", "--", ":", "-."]
FIT_LINE_STYLE = FIT_LINE_STYLES[0]
FIT_LINE_ALPHA = 1.0
MARKER_SIZE = 3.2
MARKER_EDGE_WIDTH = 0.7
ERRORBAR_LINE_WIDTH = 0.6
ERRORBAR_CAP_SIZE = 1.6
DEFAULT_ASPECT = "5:3"
DEFAULT_FIGURE_WIDTH_IN = 3.6
DEFAULT_PLOTLY_WIDTH_PX = 600
HISTOGRAM_Y_MODES = ("count", "probability_density")
FIGURE_ASPECTS = {
    "1:1": 1.0,
    "3:2": 3.0 / 2.0,
    "5:3": 5.0 / 3.0,
}
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


def figure_size(aspect: str = DEFAULT_ASPECT, width: float = DEFAULT_FIGURE_WIDTH_IN) -> tuple[float, float]:
    """Return a Matplotlib figure size for a width:height aspect ratio."""

    if aspect not in FIGURE_ASPECTS:
        allowed = ", ".join(sorted(FIGURE_ASPECTS))
        raise ValueError(f"Unknown aspect ratio {aspect!r}. Allowed: {allowed}")
    return (width, width / FIGURE_ASPECTS[aspect])


def plotly_dimensions(aspect: str = DEFAULT_ASPECT, width: int = DEFAULT_PLOTLY_WIDTH_PX) -> dict[str, int]:
    """Return Plotly pixel dimensions for a width:height aspect ratio."""

    if aspect not in FIGURE_ASPECTS:
        allowed = ", ".join(sorted(FIGURE_ASPECTS))
        raise ValueError(f"Unknown aspect ratio {aspect!r}. Allowed: {allowed}")
    return {"width": width, "height": round(width / FIGURE_ASPECTS[aspect])}


def matplotlib_rcparams(serializable: bool = False, svg_fonttype: str = "none") -> dict[str, object]:
    """Return a starter rcParams dictionary for Tao Style plots."""

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
        "ps.fonttype": 42,
        "svg.fonttype": svg_fonttype,
    }


def matplotlib_legend_kwargs(outside: bool = False) -> dict[str, object]:
    """Return Tao Style legend keyword arguments for Matplotlib."""

    if outside:
        return {
            "loc": "center left",
            "bbox_to_anchor": (1.02, 0.5),
            "frameon": True,
            "ncol": 1,
            "borderaxespad": 0.0,
        }
    return {"frameon": False}


def apply_matplotlib_legend(ax, outside=None, **kwargs):
    """Apply Tao Style legend placement and frame styling to a Matplotlib axes."""

    if outside is None:
        _, labels = ax.get_legend_handles_labels()
        outside = len(labels) > LEGEND_MANY_ITEMS_THRESHOLD

    legend_kwargs = matplotlib_legend_kwargs(outside)
    legend_kwargs.update(kwargs)
    legend = ax.legend(**legend_kwargs)
    if outside and legend is not None:
        frame = legend.get_frame()
        frame.set_edgecolor(AXIS_COLOR)
        frame.set_linewidth(AXIS_LINE_WIDTH)
        frame.set_facecolor("white")
        frame.set_alpha(1.0)
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


def plotly_layout_style(aspect: str = DEFAULT_ASPECT, width: int = DEFAULT_PLOTLY_WIDTH_PX) -> dict[str, object]:
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
    width: int = DEFAULT_PLOTLY_WIDTH_PX,
    legend_outside: bool = False,
):
    """Apply Tao Style axis and layout settings to a Plotly figure."""

    fig.update_layout(**plotly_layout_style(aspect, width))
    fig.update_layout(legend=plotly_legend_style(legend_outside))
    axis_style = plotly_axis_style()
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    return fig


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
                    "figure_size": figure_size(args.aspect),
                    "legend": {
                        "inside": matplotlib_legend_kwargs(False),
                        "outside": matplotlib_legend_kwargs(True),
                    },
                    "gradients": GRADIENT_COLORMAPS,
                    "histogram": {
                        "y_modes": HISTOGRAM_Y_MODES,
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

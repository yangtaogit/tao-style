# Scientific Plotting

Status: first active Tao Style module.

## Scope

Use this reference for research data plots, figure panels, publication graphics, and exploratory plots that may later become manuscript, report, or presentation figures.

The skill is language-agnostic. Default to Python/Matplotlib when the user has not chosen a stack, because Python is Tao's default environment for plotting and validation and Matplotlib is Tao's default plotting backend. If the user's data, code, or workflow is already in another language or plotting library, apply the same style principles in that stack instead of translating the whole workflow without a reason.

## Backend Selection

- Python: use Matplotlib by default for static scientific figures; use Seaborn only for statistical plot convenience when it does not obscure control; use Plotly only when interactive output is requested.
- R: use ggplot2 themes and scales that mirror the profile.
- MATLAB: set root/default graphics properties or local axes properties.
- Julia: use Makie or Plots themes matching the profile.
- C++: use the plotting framework already present in the project, such as ROOT, matplotlib-cpp, or generated data plus a plotting script.
- LaTeX: use pgfplots/TikZ when the user needs native TeX typography or Beamer integration.

## Default Scientific Figure Principles

- Preserve data honesty: do not smooth, interpolate, remove outliers, change axis scales, or normalize data unless the user requests it or the method is explicit.
- Prefer direct visual comparison over decoration.
- Keep units in axis labels when units are known.
- Use consistent significant figures and tick formatting.
- Make legends, labels, and annotations readable at the final target size, not only on a large preview.
- Use vector output for publication-style line art when possible.
- Save a raster preview when helpful for quick inspection.

## Typography

- Use Helvetica as the first-choice English font.
- Use `Arimo`, `Noto Sans`, or `Nimbus Sans` only as Helvetica-compatible local preview fallbacks when the system does not provide Helvetica. Prefer a fallback with complete superscript glyphs for log-axis labels.
- Use 宋体 for Chinese text. In code, prefer cross-platform font names in this order: `SimSun`, `Songti SC`, `Noto Serif CJK SC`.
- Keep font selection explicit in plotting code when the environment may not have the preferred fonts installed.
- Make axis labels/titles slightly larger than tick labels. Use axis labels at `9 pt` and tick labels at `8 pt` by default.
- Use Computer Modern as the default math font for real mathematical expressions.
- For ordinary axis labels, tick labels, legends, and annotations, use plain text with the Tao Style font stack instead of Matplotlib mathtext. Avoid `$...$` for simple labels such as `x`, `y`, `y = sin(x)`, or `π/2`, because mathtext uses a separate math font.
- Keep coordinate-axis labels and tick labels in the ordinary text font whenever possible, including log-axis exponents.
- Reserve mathtext or LaTeX rendering for real equations; when using Matplotlib mathtext, set `mathtext.fontset` to `cm`.

## Axis Labels and Units

- Use square brackets for units in axis labels: `Quantity [Unit]`.
- Examples: `Bias Voltage [V]`, `Current [A]`, `Time [s]`, `Temperature [K]`.
- Keep the quantity name in plain text. Use math rendering only for real mathematical symbols or expressions that need it.

## Axis and Tick Style

- Use a boxed axis by default for XY scientific curves: show left, right, top, and bottom spines.
- Use black axis spines and black ticks.
- Use axis line width `1.0`.
- Draw both major and minor ticks inward.
- Show ticks on all four sides of the plotting box when the backend supports it.
- Mirror all ticks in Plotly using `mirror="allticks"`.
- Enable minor ticks for continuous numeric axes unless they make the axis visually crowded.
- Use major tick width `1.0`.
- Use minor tick width `0.5`.
- Do not use grid lines by default.

## Log Axes

- For base-10 log axes, format major tick labels visually as `10^{n}` rather than `1eN` or plain exponent notation.
- In Matplotlib, prefer plain-text Unicode superscripts such as `10⁻⁶` instead of mathtext labels such as `$10^{-6}$`, because Unicode text preserves the ordinary axis font while still showing a true superscript.
- If the active Helvetica-compatible font lacks superscript glyphs, switch to a plain sans fallback with complete superscript coverage rather than using mathtext.
- Avoid `LogFormatterMathtext` for Tao Style axes unless the user explicitly wants mathematical fonts on ticks.
- Keep minor ticks visible on log axes unless they overcrowd the plot.

## Color

- Prefer a cool, restrained categorical palette: dark blue/Navy `#000080`, soft blue `#6CA6CD`, black `#000000`, and gray `#808080`.
- Use red with lower priority unless the data or user request specifically calls for emphasis, contrast, warning, or a warm-category encoding.
- When red is needed, prefer muted red `#B04A4A` over saturated red.
- For many curves or ordered series that need a color gradient, prefer dark-blue gradients or grayscale gradients.
- Avoid rainbow-like or highly saturated multi-hue gradients unless the user specifically asks for them.
- Preferred dark-blue gradient: `#E6EEF6`, `#AFCBE3`, `#6CA6CD`, `#2F5F9F`, `#000080`.
- Preferred grayscale gradient: `#EDEDED`, `#C9C9C9`, `#9A9A9A`, `#5F5F5F`, `#000000`.
- Use this list consistently across supported backends unless the user provides a data-specific color mapping.
- Keep the list easy to extend as Tao adds more preferred colors.

## Markers and Error Bars

- Use relatively small markers by default for binned or dense scientific data.
- For dense 2D XY data, prefer line-only rendering and omit markers to avoid visual clutter from overcrowded points.
- Start with Matplotlib marker size `3.2 pt` and marker edge width `0.7 pt`.
- Increase marker size only when the figure is sparse or the output medium needs larger symbols.
- For marker-only errorbar plots, keep error bar lines visually lighter than the data markers.
- Start with errorbar line width `0.6 pt` and cap size `1.6 pt`.

## Histograms

- Before plotting a histogram, ask which y-axis mode to use: raw `Count` or normalized `Probability Density [1/Unit]`.
- Use `Count` for raw bin counts. Label the y axis `Count`.
- Use `Probability Density [1/Unit]` when Tao asks for normalized histograms. The unit should be the inverse of the x-axis unit, for example `Probability Density [1/mm]`.
- In Matplotlib, use `density=True` for `Probability Density [1/Unit]`.
- Do not use bin probability (`bin count / total sample count`) unless Tao explicitly asks for probability per bin.
- Render ordinary histograms as a stepped bin outline with a light fill color by default. This means tracing the outer edges of the histogram bins, not drawing a line through bin centers.
- In Matplotlib, use `histtype="stepfilled"` for the fill and, when a crisp boundary is needed, overlay `histtype="step"` with the same bin edges.
- Do not represent a default histogram as a connected line plot of bin-center values. Use bin-center marker/line/errorbar plots only for special binned-data cases.
- Use marker + errorbar histogram-style points only for special cases, such as large bin widths, low statistics, or when the binned data need to be fitted and the per-bin uncertainty should be visible.

## Lines and Fits

- Use line width `1.0 pt` for fitted curves and ordinary continuous curves by default.
- Use line-only rendering for dense 2D data unless the user explicitly wants markers or the markers carry additional meaning.
- When multiple fitted curves appear in the same plot, distinguish them with both color and line style. Use solid, dashed, dotted, then dash-dot as the default sequence.
- Use the same color for a fitted curve and its corresponding data markers/error bars unless another mapping is specified.
- Keep fitted curves visually secondary to the data points when judging fit quality; adjust line width or opacity if the fit overpowers markers/error bars.

## Legend

- For legends inside the plotting frame, do not draw a legend border.
- When many curves make the legend large or likely to cover data, place the legend outside the plotting frame on the right.
- Outside legends should be vertical, single-column, and framed.
- Use the same frame color and line width as the XY axis box for outside legend borders: black, `1.0 pt`.
- Prefer the outside-right legend for more than about five legend items, or earlier if the legend overlaps important data.

## Figure Aspect Ratio

- For a single-plot scientific figure, use `3.6 in` as the default physical width when Tao does not specify the target medium.
- For a single-plot canvas, use `5:3` as the default output width:height ratio when Tao does not specify otherwise.
- Therefore, the default single-plot figure size is `3.6 in x 2.16 in`.
- With the same default width, `1:1` gives `3.6 in x 3.6 in`, and `3:2` gives `3.6 in x 2.4 in`.
- Keep `1:1`, `3:2`, and `5:3` as the common ratio options when Tao asks to choose or compare.
- Treat the ratio as the output figure or plotting-area width:height ratio, not as an equal data-unit aspect constraint.
- Multi-panel canvases are not constrained by the single-plot ratio rule. Choose the figure size and layout based on the number of panels, shared axes, label space, legend placement, and the data relationship.
- If the target medium has a known final figure width, such as a journal column, slide placeholder, poster panel, or report layout, confirm or infer that target width first and choose `figsize` so the figure is not heavily scaled later.

## Python Starter

When using Matplotlib, import `scripts/apply_tao_style.py` if the skill files are available locally:

```python
from scripts.apply_tao_style import figure_size, matplotlib_rcparams

plt.rcParams.update(matplotlib_rcparams())
fig, ax = plt.subplots(figsize=figure_size("5:3"))
```

For legends, use the helper when available:

```python
from scripts.apply_tao_style import apply_matplotlib_legend

apply_matplotlib_legend(ax)
```

For base-10 log axes, use the helper formatter when available:

```python
from scripts.apply_tao_style import apply_matplotlib_log10_axis

apply_matplotlib_log10_axis(ax, axis="y")
```

This helper formats major log tick labels as ordinary text with Unicode superscripts, preserving the same font family as other axis tick labels.

For histograms, ask for the y-axis mode first, then use the helper when available:

```python
from scripts.apply_tao_style import plot_matplotlib_histogram

mode = "probability_density"  # or "count", after asking Tao
plot_matplotlib_histogram(ax, data, bins, mode, unit="mm", color="#000080", label="Sample")
```

This helper draws the histogram as bin-edge steps with light fill; it does not connect bin centers.

If the skill is installed but the script path is not directly importable, copy the relevant rcParams values or generate them from:

```bash
python scripts/apply_tao_style.py --aspect 5:3 --format json
```

For Plotly, use the helper functions when available:

```python
from scripts.apply_tao_style import apply_plotly_style

fig = apply_plotly_style(fig, aspect="5:3")
```

Or inspect the Plotly axis/layout dictionary:

```bash
python scripts/apply_tao_style.py --target plotly --aspect 5:3 --format json
```

## Output Defaults

- Preview: PNG at 150-200 DPI.
- Final raster: PNG or TIFF at 300 DPI unless the target venue requires otherwise.
- Final vector: PDF or SVG for line art and editable figures.
- Keep text editable in SVG/PDF when the backend supports it.
- For README, web, or cross-machine previews where exact font appearance matters more than editability, export SVG text as paths using Matplotlib `svg.fonttype = "path"`.
- For final editable SVG, use `svg.fonttype = "none"` only when the target machine or editor has the required fonts available.

## Figure QA Checklist

- Axis labels include names and units when known.
- Tick labels are readable and not overcrowded.
- Legend does not cover important data.
- Colors remain distinguishable in grayscale or for common color-vision deficiencies.
- Multi-panel figures align axes, labels, and panel spacing.
- Exported files do not clip titles, labels, legends, or annotations.
- Final file format matches the user's target use: notebook, manuscript, slide, report, or web.

## Open Preferences

- TODO: Confirm Tao's default journal and slide figure sizes.
- TODO: Extend the common categorical color list beyond Navy, black, and gray.
- TODO: Confirm sequential and diverging colormaps.
- TODO: Confirm final default errorbar cap size and errorbar line width after visual review.
- TODO: Confirm final default fitted-line width and opacity after visual review.
- TODO: Confirm preferred major tick length and minor tick length.
- TODO: Confirm whether `5:3` or `1:1` should be the default when Tao asks the assistant to choose.
- TODO: Add representative input data and expected figure examples.

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
- Check Helvetica availability before rendering with `python scripts/manage_fonts.py --check`. The Skill includes font files under `assets/fonts/helvetica/`; when Helvetica is missing, tell the user and ask whether to install them with `python scripts/manage_fonts.py --install`. Do not install fonts automatically.
- Use `Arimo`, `Noto Sans`, or `Nimbus Sans` as Helvetica-compatible local preview fallbacks only after the user declines installation or installation is unavailable. State the chosen substitution, and prefer a fallback with complete superscript glyphs for log-axis labels.
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
- Use axis line width `0.6`.
- Draw both major and minor ticks inward.
- Show ticks on all four sides of the plotting box when the backend supports it.
- Mirror all ticks in Plotly using `mirror="allticks"`.
- Enable minor ticks for continuous numeric axes unless they make the axis visually crowded.
- Use major tick width `0.6` and major tick length `2.5 pt`.
- Use minor tick width `0.3` and minor tick length `1.5 pt`.
- Do not use grid lines by default. When grid lines are needed, show only major-tick grid lines, using gray dotted lines with color `#9E9E9E`, linestyle `":"`, and linewidth `0.2 pt`; do not show minor-tick grid lines.

## Three-Dimensional Axes

- For 3D scientific plots, show the visible X/Y/Z coordinate box and grid by default, but render the three inner panes transparent so the box reads as a black wireframe rather than shaded panels.
- Use orthographic projection by default, `projection="ortho"`: vertical lines stay vertical on screen and equal heights remain comparable along the depth direction. Perspective tilts the Z axis toward a vanishing point and distorts height comparison.
- Use perspective (`projection="persp"`, optionally with a larger `focal_length` such as 4 to reduce distortion) only when Tao asks for a presentation-style depth effect.
- Make the three 3D panes transparent (`1, 1, 1, 0` in Matplotlib RGBA) and give each pane edge and axis line a black `0.6 pt` stroke, so only the black wireframe box and the grid show, with no shaded backgrounds.
- Matplotlib strokes only the three panes facing the viewer, so the rear vertical edge where the two back panes meet is left unstroked and the wireframe box looks open. Close it with the helper `add_matplotlib_3d_box_edge(fig, ax)`, which draws that edge at the true rendered box bounds so it aligns exactly with the grid box. Do not add other manual frames.
- Show only major-tick grid lines on 3D panes, using gray dotted lines with color `#9E9E9E` (`0.62, 0.62, 0.62, 1.0`), linestyle `":"`, and linewidth `0.2 pt`.
- Use inward ticks. In Matplotlib 3D, set `inward_factor=0.0` and `outward_factor=0.2` for the current Tao Style visual direction.
- Reclaim 3D space in layers rather than with aggressive negative padding: first enlarge the axes rectangle with `apply_matplotlib_3d_style(..., zoom=1.2)` (it enlarges the axes rectangle about its center, not `set_box_aspect(zoom=)`) and rely on content-adaptive cropping to remove outer whitespace; then limit each axis to about five major ticks and shorten tick text with unit scaling, putting the scale in the axis label, such as `Time [μs]`; finally close the remaining gap with mild `tick_pad=-1.5` and `labelpad=-3.0`. Do not use `set_box_aspect(zoom=)` for compactness: it decouples the data coordinate system from the pane rendering, which makes the manually drawn rear box edge miss the grid box.
- Give the Z axis title a tighter pad than X/Y: Matplotlib offsets each axis title from the outer edge of its tick labels, and Z tick numbers are horizontal text whose width sets that edge, so a uniform labelpad leaves the Z title visually far from its numbers. Use `zlabelpad=-6.0` as the starting value, and keep Z tick text short via unit scaling.
- Treat `zoom` and the pad values as starting values and verify them at the final view angle, because negative pads depend on the view angle and tick-label length.
- Apply Tao Style typography to 3D axes: ordinary text font, axis labels at `9 pt`, tick labels at `8 pt`, and Computer Modern only for real mathematical expressions.
- Use plain `X`, `Y`, and `Z` labels unless Tao specifies physical quantities and units. When units are known, keep the same square-bracket format as 2D axes, such as `X Position [mm]`.
- For 3D scalar fields, surfaces, or 4D data shown as spatial coordinates plus a value, encode the value with the preferred gradients and place the colorbar outside the right side of the axes.
- Position 3D colorbars from the axes' tight bounding box, not the axes rectangle: Matplotlib draws 3D tick and axis labels outside the axes rectangle, so `fig.colorbar(pad=...)` can overlap them. Use the helper `add_matplotlib_3d_colorbar(fig, ax, mappable)`, which measures the label extent, uses a larger default gap (`pad=0.28 in`) than 2D colorbars, keeps a compact `shrink=0.50` so the bar does not tower over the box, and expands the canvas to the right when needed. Add the colorbar only after the content, style, view angle, and box aspect are final.
- 3D figures are not constrained by the single-panel 2D XY axes-box rule; choose the canvas, view angle, and colorbar placement so the full 3D coordinate box and data remain readable.
- Equal-unit 3D plots are an exception to the default box: when X, Y, and Z all represent comparable physical lengths, positions, spatial coordinates, or geometry dimensions that require true scale, set the 3D box aspect from the displayed data ranges so one data unit has equal visual length on all three axes. In Matplotlib use `ax.set_box_aspect((x_range, y_range, z_range))` or the helper `set_equal_xyz_box_aspect`, after setting the displayed limits. Keep `set_equal_xyz_box_aspect(..., zoom=1.0)` so it only fixes the ratio; reclaim whitespace through the axes-rectangle enlargement in `apply_matplotlib_3d_style` so the rear box edge stays aligned.
- If the equal-unit range ratio is extreme and the box becomes hard to read, ask Tao whether to crop the displayed range or fall back to the default box, and state the deviation.
- Hidden-axis 3D/4D figures are optional and must be used only when Tao explicitly asks to hide coordinates, remove the 3D coordinate box, or emphasize the data body over coordinate reading. The default 3D style remains the visible Matplotlib 3D coordinate box.
- For hidden-axis 3D/4D figures, hide the main X/Y/Z axes, tick marks, tick labels, axis titles, pane backgrounds, and grid lines. Keep the data body complete and uncropped.
- Add a compact in-figure `XYZ` direction marker in a natural empty area, usually the lower-left region. Use the same `elev` and `azim` as the main 3D view. Keep the marker small, about `12.5%` of the figure width/height, with arrow length about `0.78`, line width `0.8 pt`, and `XYZ` label size `6.5 pt` as starting values.
- For hidden-axis scalar fields or 4D data, keep the colorbar when color encodes value. Place it inside the figure in a natural right-side empty area when possible, with a black `0.6 pt` outline and Tao Style typography. The colorbar and `XYZ` marker must not cover the data body.
- Hidden-axis 3D/4D figures should use content-adaptive cropping by default, including the data body, in-figure colorbar, and in-figure `XYZ` marker, with a small safety margin such as `pad_inches=0.02-0.04`. If Tao asks for a fixed ratio, add padding after the content crop rather than cropping or compressing the data.

## Log Axes

- For base-10 log axes, format major tick labels visually as `10^{n}` rather than `1eN` or plain exponent notation.
- In Matplotlib, prefer plain-text Unicode superscripts such as `10⁻⁶` instead of mathtext labels such as `$10^{-6}$`, because Unicode text preserves the ordinary axis font while still showing a true superscript.
- If the active Helvetica-compatible font lacks superscript glyphs, switch to a plain sans fallback with complete superscript coverage rather than using mathtext.
- Avoid `LogFormatterMathtext` for Tao Style axes unless the user explicitly wants mathematical fonts on ticks.
- Keep minor ticks visible on log axes unless they overcrowd the plot.

## Color

- Prefer cool, restrained colors by default: deep blue `#2A2F80`, black `#000000`, and gray `#808080` are the core anchors, exposed as `categorical_palette("tao-core")`.
- Per-count series colors: the color set and its order both depend on the number of ordinary series; use the sequence for the actual series count instead of truncating or extending another count's sequence. 1: `#2A2F80`. 2: `#2A2F80`, `#808080`. 3: `#2A2F80`, `#808080`, `#000000`.
- More than three ordinary series: prefer the tao palette, taking its colors in order; for ordered series, switch to a tao blue or tao gradient instead.
- Use red with lower priority unless the data or user request specifically calls for emphasis, contrast, warning, or a warm-category encoding. When red is needed, prefer muted red `#B04A4A` over saturated red. Red is not part of the default ordinary multi-series sequence.
- For many curves or ordered series that need a color gradient, prefer tao blue gradients or tao gray gradients by default.
- Use the tao palette as an optional alternative when Tao asks for stronger visual separation, a presentation-style figure, or a dedicated colorbar/heatmap: `#2A2F80`, `#3953A5`, `#4378BC`, `#6FCCDE`, `#99CB6F`, `#F6EB14`, `#F67F21`, `#EE2024`, `#7D1415`.
- Treat the tao palette as a deliberate alternative, not the default. It is closer to a vivid blue-cyan-green-yellow-orange-red colorbar than the restrained cool palette.
- Avoid rainbow-like or highly saturated multi-hue gradients unless Tao specifically asks for them or chooses the tao palette.
- Preferred tao blue gradient, based on deep blue `#2A2F80`: `#EEF1F8`, `#C8D2EA`, `#8799CF`, `#4E5CA4`, `#2A2F80`.
- Preferred tao gray gradient: `#EDEDED`, `#C9C9C9`, `#9A9A9A`, `#5F5F5F`, `#000000`.
- Additional family gradients when the data semantics call for green or red: tao green gradient `#EFF9EA`, `#C7EBB4`, `#92D982`, `#55BE55`, `#2BA13C`, `#158029`, `#0E5A20`; tao red gradient `#FCEFEC`, `#F8C4BA`, `#F09083`, `#DD4B3E`, `#9E1A15`. These two are deliberately brighter than the categorical colors; the emphasis red `#B04A4A` is a categorical color and not part of the tao red gradient.
- Optional tao gradient: `#2A2F80`, `#3953A5`, `#4378BC`, `#6FCCDE`, `#99CB6F`, `#F6EB14`, `#F67F21`, `#EE2024`, `#7D1415`.
- Colorbars should sit outside the right side of the corresponding axes, use a vertical layout, and keep a black outline with the same line width as the axes box. For portrait single-panel figures, keep the axes-box width fixed and allow the canvas to expand rightward for the colorbar; do not squeeze the axes box or let the colorbar overlap tick labels.
- Use these lists consistently across supported backends unless the user provides a data-specific color mapping.
- Keep the lists easy to extend as Tao adds more preferred colors.

## Markers and Error Bars

- Use relatively small markers by default for binned or dense scientific data.
- For dense 2D XY data, prefer line-only rendering and omit markers to avoid visual clutter from overcrowded points.
- Start with Matplotlib marker size `3.2 pt` and marker edge width `0.7 pt`.
- Increase marker size only when the figure is sparse or the output medium needs larger symbols.
- For marker-only errorbar plots, keep error bar lines visually lighter than the data markers.
- Start with errorbar line width `0.6 pt` and cap size `1.6 pt`.

## Histograms

- If the y-axis mode is unspecified and not clear from context, default to raw `Count` and state the assumption; ask only when normalization materially affects the result, such as comparing datasets with different sample sizes.
- Use `Count` for raw bin counts. Label the y axis `Count`.
- Use `Probability Density [1/Unit]` when Tao asks for normalized histograms. The unit should be the inverse of the x-axis unit, for example `Probability Density [1/mm]`.
- In Matplotlib, use `density=True` for `Probability Density [1/Unit]`.
- Do not use bin probability (`bin count / total sample count`) unless Tao explicitly asks for probability per bin.
- Render ordinary histograms as a stepped bin outline with a light fill color by default. This means tracing the outer edges of the histogram bins, not drawing a line through bin centers.
- In Matplotlib, use `histtype="stepfilled"` for the fill and, when a crisp boundary is needed, overlay `histtype="step"` with the same bin edges.
- Do not represent a default histogram as a connected line plot of bin-center values. Use marker + errorbar plots only for special binned-data cases.
- Use marker + errorbar histogram-style points only for special cases, such as large bin widths, low statistics, or when the binned data need to be fitted and the per-bin uncertainty should be visible.

## Lines and Fits

- Use line width `1.0 pt` for ordinary continuous curves and fitted curves by default.
- Use line-only rendering for dense 2D data unless the user explicitly wants markers or the markers carry additional meaning.
- When multiple ordinary curves or fitted curves appear in the same plot with categorical colors, distinguish them with both color and line style. Use solid, dashed, dotted, then dash-dot as the default line-style sequence.
- When curves use a gradient color scheme, keep all curves solid so the gradient order remains visually clear.
- Use the same color for a fitted curve and its corresponding data markers/error bars unless another mapping is specified.
- Keep fitted curves visually secondary to the data points when judging fit quality; adjust line width or opacity if the fit overpowers markers/error bars.

## Legend

- For legends inside the plotting frame, do not draw a legend border.
- When many curves make the legend large or likely to cover data, place the legend outside the plotting frame on the right.
- Outside legends should prefer a vertical single-column layout and be framed.
- If an outside single-column legend exceeds the axes-box height, split the entries evenly into multiple columns to keep the legend compact.
- Use the same frame color and line width as the XY axis box for outside legend borders: black, `0.6 pt`.
- Prefer the outside-right legend for more than about five legend items, or earlier if the legend overlaps important data.

## Axes Box Size and Aspect Ratio

- For a single-plot scientific figure, fix the physical size of the axes box, meaning the black XY plotting frame, rather than fixing the whole output canvas.
- Use `2.0 in` as the default reference size when Tao does not specify the target medium.
- Use `3:2` as the default axes-box width:height ratio, so the default axes box is `3.0 in x 2.0 in`.
- For landscape and square single-plot ratios, keep the axes-box height fixed at `2.0 in`: `1:1 = 2.0 in x 2.0 in`, `3:2 = 3.0 in x 2.0 in`, and `5:3 = 3.33 in x 2.0 in`.
- For portrait ratios, treat them as rotated forms of the landscape sizes and keep the axes-box width fixed at `2.0 in`: `2:3 = 2.0 in x 3.0 in` and `3:5 = 2.0 in x 3.33 in`.
- Keep `1:1`, `3:2`, `5:3`, `2:3`, and `3:5` as the common axes-box ratio options when Tao asks to choose or compare.
- Equal-unit XY plots are an exception to the default single-plot ratios. Use this when X and Y both represent comparable physical lengths, positions, spatial coordinates, map coordinates, device geometry, or other quantities where one X unit and one Y unit should have the same visual length.
- For equal-unit XY plots, fix the X-axis box width at `3.0 in` by default and compute the Y-axis box height from the displayed data range: `Y box height = 3.0 in * (Y range / X range)`. Use equal data aspect, such as Matplotlib `ax.set_aspect("equal", adjustable="box")`.
- Equal-unit XY plots are not constrained by `1:1`, `3:2`, `5:3`, `2:3`, or `3:5` default ratios. The exported canvas still adapts to all visible titles, labels, legends, colorbars, and annotations. If the resulting height is extreme, ask Tao whether to change the fixed X width or crop/limit the displayed data range.
- Do not fix the exported canvas height or width by default. After fixing the axes-box size, let the exported canvas adapt to all visible content, including titles, tick labels, axis labels, legends, colorbars, and annotations.
- Use content-adaptive cropping with a small safety margin, such as `pad_inches=0.02-0.04`. Never crop text, legends, colorbars, annotations, or tick labels to preserve a canvas edge.
- Outside elements must not change the final physical size of the XY plotting frame. They should expand the surrounding canvas instead of moving or resizing the axes box.
- Treat the ratio as the plotting-frame width:height ratio, not as an equal data-unit aspect constraint.
- Multi-panel canvases are not constrained by the single-plot ratio rule. Choose the canvas size and panel axes-box sizes based on the number of panels, shared axes, label space, legend placement, and the data relationship.
- If the target medium has a known final figure width, such as a journal column, slide placeholder, poster panel, or report layout, confirm or infer that target width first and choose the axes-box size and surrounding canvas so the figure is not heavily scaled later.

## Python Starter

When using Matplotlib, import `scripts/apply_tao_style.py` if the skill files are available locally. The import requires the skill root as the working directory or on `sys.path`; otherwise use the CLI fallback below to generate the values path-independently.

```python
from scripts.apply_tao_style import (
    axes_box_size,
    matplotlib_rcparams,
    save_adaptive_figure,
    set_fixed_axes_box,
    set_equal_xy_axes_box,
)

plt.rcParams.update(matplotlib_rcparams())
aspect = "3:2"
fig, ax = plt.subplots(figsize=axes_box_size(aspect))
# After plotting labels/legends and before saving:
set_fixed_axes_box(fig, ax, aspect=aspect)
save_adaptive_figure(fig, "figure.svg")
```

The per-count series orders (up to three) are also available programmatically; the fixed `prop_cycle` already matches them. With more than three ordinary series, use `categorical_palette("tao")` in order, or a gradient for ordered series:

```python
from scripts.apply_tao_style import series_colors

colors = series_colors(3)
```

For equal-unit XY plots such as spatial coordinates or geometry, fix the X-axis box width and let the Y-axis height follow the data range:

```python
from scripts.apply_tao_style import set_equal_xy_axes_box, save_adaptive_figure

# After setting x/y limits for physical coordinates:
set_equal_xy_axes_box(fig, ax, xlim=(0, 10), ylim=(0, 5))
save_adaptive_figure(fig, "equal_xy_figure.svg")
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

For right-side colorbars, set the fixed axes box first, then add the colorbar with the helper so the adaptive canvas can include it without changing the axes-box size:

```python
from scripts.apply_tao_style import add_matplotlib_colorbar

set_fixed_axes_box(fig, ax, aspect=aspect)
cbar = add_matplotlib_colorbar(fig, ax, image, pad=0.12, width=0.08)
cbar.set_label("Signal [Unit]")
save_adaptive_figure(fig, "figure.svg")
```

For gradient colormaps, build them with the helper:

```python
from scripts.apply_tao_style import matplotlib_colormap

cmap = matplotlib_colormap("tao-blue")  # or "tao-gray", "tao-green", "tao-red", "tao"
```

For histograms, determine the y-axis mode (default `count` when unspecified and clear from context), then use the helper when available:

```python
from scripts.apply_tao_style import plot_matplotlib_histogram

mode = "count"  # default; use "probability_density" when Tao asks for normalized histograms
plot_matplotlib_histogram(ax, data, bins, mode, unit="mm", color="#2A2F80", label="Sample")
```

This helper draws the histogram as bin-edge steps with light fill; it does not connect bin centers.

For Matplotlib 3D axes, apply Tao typography with the helper (transparent panes plus a black wireframe box), then close the rear box edge that Matplotlib leaves unstroked:

```python
from scripts.apply_tao_style import apply_matplotlib_3d_style, add_matplotlib_3d_box_edge

ax = fig.add_subplot(111, projection="3d")
apply_matplotlib_3d_style(ax, xlabel="X", ylabel="Y", zlabel="Z")  # zoom=1.2 enlarges the axes rectangle
add_matplotlib_3d_box_edge(ax, fig)  # after view angle and box aspect are final
```

For 3D colorbars, add them last, after the content, style, view angle, box aspect, and box edge are final, so the label extent is known:

```python
from scripts.apply_tao_style import add_matplotlib_3d_colorbar

cbar = add_matplotlib_3d_colorbar(fig, ax, surface)  # default pad=0.28 in
cbar.set_label("Signal [Unit]")
```

For equal-unit 3D data such as spatial coordinates, trajectories, or device geometry, set the box aspect from the displayed ranges after applying the style and setting limits, keeping `zoom=1.0` so only the ratio is fixed:

```python
from scripts.apply_tao_style import set_equal_xyz_box_aspect

apply_matplotlib_3d_style(ax, xlabel="X [mm]", ylabel="Y [mm]", zlabel="Z [mm]")
set_equal_xyz_box_aspect(ax, xlim=(0, 40), ylim=(0, 20), zlim=(0, 10), zoom=1.0)
add_matplotlib_3d_box_edge(ax, fig)
```

If the skill is installed but the script path is not directly importable, copy the relevant rcParams values or generate them from:

```bash
python scripts/apply_tao_style.py --aspect 3:2 --format json
```

For Plotly, use the helper functions when available:

```python
from scripts.apply_tao_style import apply_plotly_style

fig = apply_plotly_style(fig)
```

Or inspect the Plotly axis/layout dictionary:

```bash
python scripts/apply_tao_style.py --target plotly --aspect 3:2 --format json
```

## Output Defaults

- Preview: PNG at 150-200 DPI.
- Final raster: PNG or TIFF at 300 DPI unless the target venue requires otherwise.
- Final vector: PDF or SVG for line art.
- Default SVG export should be font-stable across viewing environments: convert text to paths using Matplotlib `svg.fonttype = "path"`.
- Default PDF export should embed fonts so the visual appearance does not depend on fonts installed where the PDF is opened; in Matplotlib use `pdf.fonttype = 42` and keep `pdf.use14corefonts = False`.
- Keep editable text in SVG/PDF only when the user explicitly needs text editing and the target machine or editor has the required fonts available.

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
- TODO: Confirm a diverging colormap for signed data.
- Confirmed: major tick length `2.5 pt`, minor tick length `1.5 pt`.
- Confirmed: 3D boxed style uses transparent panes with a black wireframe box, `add_matplotlib_3d_box_edge` for the rear edge, and axes-rectangle enlargement (`zoom=1.2`) rather than `set_box_aspect(zoom=)`.

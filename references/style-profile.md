# Tao Style Profile

Status: draft template. Replace TODO entries as preferences are confirmed.

## Invocation

- Ask whether to use Tao Style when the user requests a plot, figure, diagram, generated image, or scientific slide report and has not already opted in or out.
- For scientific slide reports, ask whether to use Beamer when the output format is not already specified.
- Apply Tao Style directly when the user invokes `$tao-style`, says "Tao Style", or asks for "my style".
- If a preference is unknown, prefer a clean publication-style default and note the assumption briefly.

## Scientific Plot Defaults

See `references/scientific-plotting.md` for the active plotting workflow and backend guidance. Keep confirmed reusable preferences here so future modules, such as LaTeX Beamer or document templates, can share the same visual identity.

- Histograms: ask whether the y axis should be raw `Count` or normalized `Probability Density [1/Unit]` before plotting; render default histograms as stepped bin outlines with light fill, not as connected bin-center lines.

## Typography

- Primary Latin font: Helvetica.
- Primary CJK font: 宋体, using `SimSun` on Windows, `Songti SC` on macOS, and `Noto Serif CJK SC` as a Linux fallback when 宋体 is unavailable.
- Math font: Computer Modern.
- Coordinate-axis labels and tick labels: prefer ordinary text fonts over math fonts; for log axes, use plain-text superscripts such as `10⁻⁶` with a sans fallback that supports the required glyphs.
- Title size: TODO.
- Axis label size: TODO.
- Tick label size: TODO.
- Legend size: inside legends have no frame; many-curve legends should sit outside the right side of the axes, preferably as a vertical single column with a black `0.6 pt` frame. If an outside single-column legend exceeds the axes-box height, split entries evenly into multiple columns.
- Annotation size: TODO.
- Font-stable export: default SVG text should be converted to paths, and default PDF output should embed fonts. Keep editable SVG/PDF text only when explicitly requested and when the target environment has the required fonts.

## Lines, Markers, and Error Bars

- Line width: TODO.
- Marker size: TODO.
- Marker edge style: TODO.
- Error bar style: TODO.
- Smoothing or interpolation: do not smooth raw scientific data unless the user explicitly requests it or the method is stated.
- Uncertainty: show error bars, confidence intervals, or shaded bands when they are part of the data and improve interpretation.

## Color

- Core color anchors: deep blue `#2A2F80`, black `#000000`, gray `#808080`; use them first for ordinary multi-series plots and keep this order. Use muted red `#B04A4A` only for explicit emphasis.
- Default multi-series color sequence: use `#2A2F80`, `#000000`, and `#808080` first. Only when there are more than three ordinary series, add extension colors with a reasonable visual order, prioritizing light gray first: `#BDBDBD`, then blue extensions `#4378BC`, `#6FCCDE`, then darker blue `#3953A5` if still needed. Red `#B04A4A` is not part of the default sequence and should be used only for emphasis.
- Optional τ palette: `#2A2F80`, `#3953A5`, `#4378BC`, `#6FCCDE`, `#99CB6F`, `#F6EB14`, `#F67F21`, `#EE2024`, `#7D1415`. Use it only when a stronger τ color alternative is desired.
- Sequential colormap: prefer dark-blue gradients and grayscale gradients for many curves or ordered series; use the τ gradient as an optional alternative for dedicated colorbars or heatmaps.
- Colorbar placement: put colorbars outside the right side of the corresponding axes, vertical, with a black outline matching the axes box. For portrait single-panel figures, keep the axes-box width fixed and allow the canvas to expand rightward for the colorbar instead of squeezing or overlapping the axes.
- Diverging colormap: TODO.
- Categorical color count: TODO.
- Accessibility: prefer colorblind-aware palettes and avoid encoding critical distinctions by color alone.
- Contrast: ensure text, markers, and lines remain readable on the final background.

## Layout and Composition

- Margins: avoid clipped labels and overly tight legends.
- Multi-panel spacing: TODO.
- Shared axes: use when it improves comparison and does not hide important scale differences.
- Axes box size: fix the physical size of the single-plot XY axes box rather than the whole canvas; use `2.0 in` as the default reference size when the target medium is not specified.
- Aspect ratio: use `3:2` by default for a single-plot axes box, giving `3.0 in x 2.0 in`; keep `2.0 in` as the fixed axes-box height for `1:1`, `3:2`, and `5:3` (`2.0 in x 2.0 in`, `3.0 in x 2.0 in`, `3.33 in x 2.0 in`); for portrait ratios, keep `2.0 in` as the fixed axes-box width (`2:3 = 2.0 in x 3.0 in`, `3:5 = 2.0 in x 3.33 in`). Do not fix exported canvas height or width by default; after the axes box is fixed, crop the canvas adaptively around all visible content with a small safety margin. Titles, labels, legends, colorbars, annotations, and long tick labels must expand the surrounding canvas without changing the fixed axes-box size. For equal-unit XY plots where X and Y are comparable physical lengths or positions, do not use the default single-plot ratios; fix the X-axis box width at `3.0 in` and set the Y-axis box height from the displayed range ratio so one data unit has equal visual length in X and Y. Multi-panel canvases should be sized by layout, panel axes boxes, label space, and data relationship rather than the single-plot default.
- 3D axes: use perspective projection by default, keep light-gray pane backgrounds, show only major-tick grid lines as very thin gray dotted lines, do not add extra pane boundary lines or manual frames, use inward ticks, keep tick labels very close to axes and keep axis labels compact, and apply Tao Style fonts and sizes. By default, 3D plots should show coordinates; use hidden-axis 3D/4D style only when Tao asks to hide coordinates or emphasize the data body. In hidden-axis style, hide the main coordinate box, place a compact in-figure `XYZ` direction marker and any colorbar in empty regions without covering data, and crop by content with a small safety margin.
- Annotations: keep them close to the data they describe and avoid covering important points.

## Generated Images and Diagrams

- Overall mood: TODO.
- Preferred visual density: TODO.
- Preferred background style: TODO.
- Preferred color treatment: TODO.
- Text in generated images: avoid unless necessary; if necessary, verify spelling and legibility.
- Scientific diagrams: prioritize clarity, correct labels, and clean spatial hierarchy over decoration.

## Scientific Slides and Beamer

- Status: active initial module. See `references/scientific-slides.md`.
- Beamer template: use `https://github.com/yangtaogit/tao-slides` when Tao chooses Beamer for a scientific slide report.
- Font stack: TODO.
- Math style: TODO.
- Color theme: TODO.
- Figure/table caption style: TODO.
- Code block style: TODO.

## Matplotlib Starter Defaults

Use `scripts/apply_tao_style.py` as a conservative starting point for Matplotlib plots. Update that script when this profile gains confirmed, reusable defaults.

## Preference Backlog

- TODO: Confirm default journal/presentation figure sizes.
- TODO: Confirm color palette and colormap preferences.
- TODO: Confirm line, marker, and axis styling.
- TODO: Add example figures that represent the desired style.
- TODO: Expand scientific slide and Beamer style after testing `yangtaogit/tao-slides` on real reports.

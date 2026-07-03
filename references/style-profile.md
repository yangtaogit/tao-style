# Tao Style Profile

Status: active style profile. Follow the confirmed rules in this file and the referenced module files. When an area is not specified, use a conservative publication-style default and state the assumption only if it materially affects the result.

## Invocation

- Ask whether to use Tao Style when the user requests a plot, figure, diagram, generated image, scientific slide report, or academic document and has not already opted in or out.
- For scientific slide reports, ask whether to use Beamer when the output format is not already specified.
- For academic documents, ask whether to use the `yangtaogit/tao-document` template when the template is not already specified.
- Apply Tao Style directly when the user invokes `$tao-style`, says "Tao Style", or asks for "my style".
- Combine any needed questions—style opt-in, output format or template, and required details—into one concise message instead of asking sequentially.

## Scientific Plot Defaults

See `references/scientific-plotting.md` for the active plotting workflow and backend guidance. Keep confirmed reusable preferences here so future modules, such as LaTeX Beamer or document templates, can share the same visual identity.

- Default backend: Python/Matplotlib when the user does not specify a plotting stack.
- Formal output: prefer vector formats such as SVG and PDF.
- Font-stable export: default SVG text should be converted to paths, and default PDF output should embed fonts. Keep editable SVG/PDF text only when explicitly requested and when the target environment has the required fonts.
- Histograms: if the y-axis mode is unspecified and not clear from context, default to raw `Count` and state the assumption; ask only when normalization materially affects the result. Render default histograms as stepped bin outlines with light fill, not as connected bin-center lines.

## Typography

- Primary Latin font: Helvetica.
- Primary CJK font: 宋体, using `SimSun` on Windows, `Songti SC` on macOS, and `Noto Serif CJK SC` as a Linux fallback when 宋体 is unavailable.
- Math font: Computer Modern.
- Coordinate-axis labels and tick labels: prefer ordinary text fonts over math fonts; for log axes, use plain-text superscripts such as `10⁻⁶` with a sans fallback that supports the required glyphs.
- Axis label size: `9 pt`.
- Tick label size: `8 pt`.
- Legend size: `8 pt`.
- Annotation size: start from `8 pt` and verify readability at the final figure size.
- Titles are not required by default; when used, keep them compact and visually consistent with the axis-label scale.

## Lines, Markers, and Error Bars

- Ordinary continuous curves and fitted curves: default line width `1.0 pt`.
- Dense 2D XY data: prefer line-only plots to avoid overcrowded markers.
- Multi-curve categorical line styles: solid, dashed, dotted, then dash-dot.
- Multi-curve gradient color schemes: use solid lines for all curves.
- Marker size: `3.2 pt`.
- Marker edge width: `0.7 pt`.
- Error bar line width: `0.6 pt`.
- Error bar cap size: `1.6 pt`.
- Smoothing or interpolation: do not smooth raw scientific data unless the user explicitly requests it or the method is stated.
- Uncertainty: show error bars, confidence intervals, or shaded bands when they are part of the data and improve interpretation.

## Color

- Core color anchors: deep blue `#2A2F80`, black `#000000`, gray `#808080`. Deep blue and black are hard to tell apart, so they must never be adjacent in a series order, and black enters only from three series onward. Use muted red `#B04A4A` only for explicit emphasis; it is never part of the ordinary sequence.
- Per-count series colors: the color set and its order both depend on the number of ordinary series. Use the sequence for the actual series count; do not truncate or extend another count's sequence. 1 series: `#2A2F80`. 2 series: `#2A2F80`, `#808080`. 3 series: `#2A2F80`, `#808080`, `#000000`. 4 series: `#2A2F80`, `#808080`, `#000000`, `#BDBDBD`. 5 series: `#2A2F80`, `#BDBDBD`, `#4378BC`, `#000000`, `#808080`.
- More than five ordinary series: switch to a tao blue or tao gray gradient instead of extending the categorical sequence. Only when the categories are unordered and a gradient would mislead, extend from the pool `#BDBDBD`, `#4378BC`, `#8799CF`, `#3953A5`, keep `#2A2F80` first, and reorder so adjacent series differ in both hue family and lightness; never place two grays or two similar blues next to each other.
- Optional tao palette: `#2A2F80`, `#3953A5`, `#4378BC`, `#6FCCDE`, `#99CB6F`, `#F6EB14`, `#F67F21`, `#EE2024`, `#7D1415`. Use it only when a stronger tao color alternative is desired. `#6FCCDE` stays in the tao palette and tao gradient but is not used as a standalone categorical color; the standalone light blue is `#8799CF` from the tao blue gradient.
- Sequential colormap: prefer tao blue gradients and tao gray gradients for many curves or ordered series; use the tao gradient as an optional alternative for dedicated colorbars or heatmaps.
- Preferred tao blue gradient, based on deep blue `#2A2F80`: `#EEF1F8`, `#C8D2EA`, `#8799CF`, `#4E5CA4`, `#2A2F80`.
- Preferred tao gray gradient: white to black.
- Colorbar placement: put colorbars outside the right side of the corresponding axes, vertical, with a black outline matching the axes box. For portrait single-panel figures, keep the axes-box width fixed and allow the canvas to expand rightward for the colorbar instead of squeezing or overlapping the axes.
- Accessibility: prefer colorblind-aware palettes and avoid encoding critical distinctions by color alone.
- Contrast: ensure text, markers, and lines remain readable on the final background.

## Layout and Composition

- Margins: avoid clipped labels and overly tight legends.
- Multi-panel spacing: choose by panel count, shared axes, label space, legend placement, and the data relationship; multi-panel canvases are not constrained by the single-plot ratio rule.
- Shared axes: use when it improves comparison and does not hide important scale differences.
- Axes box size: fix the physical size of the single-plot XY axes box rather than the whole canvas; use `2.0 in` as the default reference size when the target medium is not specified.
- Aspect ratio: use `3:2` by default for a single-plot axes box, giving `3.0 in x 2.0 in`; keep `2.0 in` as the fixed axes-box height for `1:1`, `3:2`, and `5:3` (`2.0 in x 2.0 in`, `3.0 in x 2.0 in`, `3.33 in x 2.0 in`); for portrait ratios, keep `2.0 in` as the fixed axes-box width (`2:3 = 2.0 in x 3.0 in`, `3:5 = 2.0 in x 3.33 in`). Do not fix exported canvas height or width by default; after the axes box is fixed, crop the canvas adaptively around all visible content with a small safety margin. Titles, labels, legends, colorbars, annotations, and long tick labels must expand the surrounding canvas without changing the fixed axes-box size. For equal-unit XY plots where X and Y are comparable physical lengths or positions, do not use the default single-plot ratios; fix the X-axis box width at `3.0 in` and set the Y-axis box height from the displayed range ratio so one data unit has equal visual length in X and Y. Multi-panel canvases should be sized by layout, panel axes boxes, label space, and data relationship rather than the single-plot default.
- Legend placement: inside legends have no frame. When many curves make the legend large or likely to cover data, place it outside the right side of the axes, preferably as a vertical single column with a black `0.6 pt` frame. If an outside single-column legend exceeds the axes-box height, split entries evenly into multiple columns.
- 3D axes: use orthographic projection by default (`projection="ortho"`) so the vertical Z axis stays vertical on screen and heights remain comparable; use perspective only when Tao asks for a presentation-style depth effect; keep pane backgrounds `#F2F2F2`; show only major-tick grid lines with color `#9E9E9E`, linestyle `":"`, and linewidth `0.2 pt`; do not add extra pane boundary lines or manual frames; use inward ticks with `inward_factor=0.0` and `outward_factor=0.2`; reclaim space in layers: enlarge the data box with `set_box_aspect(None, zoom=1.2)` and rely on content-adaptive cropping, limit each axis to about five major ticks with short tick text via unit scaling, then close the remaining gap with mild `tick_pad=-1.5` and `labelpad=-3.0`; treat zoom and pad values as starting values to verify at the final view angle; apply Tao Style fonts and sizes. Position 3D colorbars from the axes' tight bounding box (labels included) rather than the axes rectangle so they never overlap 3D tick or axis labels; in Matplotlib use `add_matplotlib_3d_colorbar` with default `pad=0.28 in`. By default, 3D plots should show coordinates; use hidden-axis 3D/4D style only when Tao asks to hide coordinates or emphasize the data body. Equal-unit 3D plots are an exception to the default box: when X, Y, and Z all represent comparable physical lengths, positions, spatial coordinates, or geometry dimensions that require true scale, set the 3D box aspect from the displayed data ranges (`set_box_aspect((x_range, y_range, z_range))`) so one data unit has equal visual length on all three axes; if the ratio is extreme, ask whether to crop the displayed range. In hidden-axis style, hide the main coordinate box, place a compact in-figure `XYZ` direction marker and any colorbar in empty regions without covering data, and crop by content with a small safety margin.
- Annotations: keep them close to the data they describe and avoid covering important points.

## Generated Images and Diagrams

- Generated images and diagrams are part of Tao Style, but the current detailed specification is intentionally lighter than the scientific plotting module.
- Use the same general visual identity when relevant: clean composition, restrained colors, readable labels, and clear spatial hierarchy.
- Text in generated images: avoid unless necessary; if necessary, verify spelling and legibility.
- Scientific diagrams: prioritize clarity, correct labels, and clean spatial hierarchy over decoration.

## Scientific Slides and Beamer

- See `references/scientific-slides.md` for the active slide-report workflow.
- Beamer template: use `https://github.com/yangtaogit/tao-slides` when Tao chooses Beamer for a scientific slide report.
- For plots included in slides, apply the scientific plotting module unless Tao asks otherwise.

## Academic Documents

- See `references/academic-documents.md` for the active academic-document workflow.
- Document template: use `https://github.com/yangtaogit/tao-document` when Tao chooses the document template.
- For plots included in documents, apply the scientific plotting module unless Tao asks otherwise.

## Matplotlib Starter Defaults

Use `scripts/apply_tao_style.py` as the Matplotlib implementation of the current scientific plotting profile. Update that script whenever confirmed reusable Matplotlib defaults change.

## Open Areas

- Further refine generated-image, scientific-diagram, multi-panel, slide, and document details when Tao adds explicit preferences.
- Add backend-specific helper scripts for non-Matplotlib stacks only when repeated use justifies them.

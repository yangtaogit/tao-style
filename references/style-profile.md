# Tao Style Profile

Status: draft template. Replace TODO entries as preferences are confirmed.

## Invocation

- Ask whether to use Tao Style when the user requests a plot, figure, diagram, generated image, or scientific slide report and has not already opted in or out.
- For scientific slide reports, ask whether to use Beamer when the output format is not already specified.
- Apply Tao Style directly when the user invokes `$tao-style`, says "Tao Style", or asks for "my style".
- If a preference is unknown, prefer a clean publication-style default and note the assumption briefly.

## Scientific Plot Defaults

See `references/scientific-plotting.md` for the active plotting workflow and backend guidance. Keep confirmed reusable preferences here so future modules, such as LaTeX Beamer or document templates, can share the same visual identity.

- Histograms: ask whether the y axis should be raw `Count` or normalized `Probability Density [1/Unit]` before plotting.

## Typography

- Primary Latin font: Helvetica.
- Primary CJK font: 宋体, using `SimSun` on Windows, `Songti SC` on macOS, and `Noto Serif CJK SC` as a Linux fallback when 宋体 is unavailable.
- Math font: Computer Modern.
- Coordinate-axis labels and tick labels: prefer ordinary text fonts over math fonts; for log axes, use plain-text superscripts such as `10⁻⁶` with a sans fallback that supports the required glyphs.
- Title size: TODO.
- Axis label size: TODO.
- Tick label size: TODO.
- Legend size: TODO.
- Annotation size: TODO.
- Font embedding: prefer editable text in final SVG/PDF when the required fonts are available; use path-converted SVG text for README/web previews where stable cross-machine appearance is more important than text editability.

## Lines, Markers, and Error Bars

- Line width: TODO.
- Marker size: TODO.
- Marker edge style: TODO.
- Error bar style: TODO.
- Smoothing or interpolation: do not smooth raw scientific data unless the user explicitly requests it or the method is stated.
- Uncertainty: show error bars, confidence intervals, or shaded bands when they are part of the data and improve interpretation.

## Color

- Primary palette: Navy `#000080`, soft blue `#6CA6CD`, black `#000000`, gray `#808080`, muted red `#B04A4A` as a lower-priority accent.
- Sequential colormap: prefer dark-blue gradients and grayscale gradients for many curves or ordered series.
- Diverging colormap: TODO.
- Categorical color count: TODO.
- Accessibility: prefer colorblind-aware palettes and avoid encoding critical distinctions by color alone.
- Contrast: ensure text, markers, and lines remain readable on the final background.

## Layout and Composition

- Margins: avoid clipped labels and overly tight legends.
- Multi-panel spacing: TODO.
- Shared axes: use when it improves comparison and does not hide important scale differences.
- Figure size: use `3.6 in` as the default single-plot width when the target medium is not specified.
- Aspect ratio: use `5:3` by default for a single-plot canvas, giving `3.6 in x 2.16 in`; multi-panel canvases should be sized by layout, label space, and data relationship rather than the single-plot default.
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

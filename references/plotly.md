# Plotly and Interactive HTML

Read this reference when using Plotly or producing interactive scientific HTML figures. Apply the shared palette, typography and data rules from [style-profile.md](style-profile.md); the implementation below translates them to Plotly. Prefer Plotly when Tao requests interactive HTML. Keep Matplotlib as the default for unspecified static plotting tasks.

## Existing Helper Coverage

`scripts/apply_tao_style.py::apply_plotly_style()` is a starter, not a complete Plotly implementation. It supplies 2D axes, mirrored ticks, basic palette and legend settings. It does not fully set fonts, pt-to-px sizes, trace styling, fixed axes-box dimensions, log labels, colorscales, colorbars or 3D scenes. Apply the missing settings at the Plotly source layer after calling it; do not assume Matplotlib rcParams affect Plotly. In particular, override its canvas dimensions and pixel widths where necessary.

Keep installed usage self-contained: read bundled references and helpers relative to the loaded skill root. Development tests are not installed and must not be runtime dependencies.

## Typography and Units

- Retain Helvetica as the specified Latin font in HTML. Do not remove the font requirement just to reduce file size; use shared resources instead. Keep the shared profile's CJK and mathematical font choices when those characters or expressions occur.
- Load bundled `assets/fonts/helvetica/Helvetica.ttf` with a document-local `@font-face` alias such as `Tao Helvetica`. Use that alias first in `layout.font.family` and hover-label fonts, followed by compatible fallbacks. Axis titles, ticks, legends, annotations and colorbars should inherit it unless a glyph-specific fallback is needed. Never install fonts into system or user font directories.
- Store the font data once in a shared `tao-fonts.css`, referenced by each HTML. A base64 font data URL inside that shared CSS is suitable for offline `file://` viewing; do not repeat the font payload inside every HTML. If using separate font URLs, verify loading in the actual viewing environment.
- Wait for the specific font to load **before** `Plotly.newPlot`, including WebGL figures. `document.fonts.ready` alone may resolve before an unused font is requested. For the alias above, use `await document.fonts.load('12px "Tao Helvetica"')`.
- Plotly numeric sizes use CSS pixels. Convert profile points with `px = pt * 96 / 72`; do not copy point values directly into pixel properties. Axis labels use 12 px; ticks, legends and ordinary annotations use approximately 10.67 px. Browser zoom affects apparent physical size.

## 2D Axes, Traces and Layout

- Use white plot/paper backgrounds. Prevent a default template from adding unwanted styling, for example with `template="none"`.
- Box XY axes with black lines, `showline=True`, `ticks="inside"`, `mirror="allticks"` and `zeroline=False`. Keep both major and minor grid lines off by default; enable minor inward ticks for continuous axes where readable.
- Convert the profile's widths and lengths: axes and major ticks 0.6 pt; minor ticks 0.3 pt; major length 2.5 pt; minor length 1.5 pt. When grids are requested, use major grids only, `#9E9E9E`, dotted, 0.2 pt.
- Fix the **inner XY plotting box**, not the canvas ratio. Convert `axes_box_size(aspect)` to CSS pixels at 96 px/in: the default 3×2 in box is 288×192 px, and a 1:1 box is 192×192 px. Preserve the profile's portrait and equal-unit exceptions. Do not generalize a particular test heatmap's dimensions to all spatial plots.
- Add margins for labels, legends and colorbars around the fixed box. Expand the canvas when outside content needs room; do not let automatic margins squeeze the box. Check actual rendered dimensions and text bounds. Responsive pages may scroll around a fixed-size plot; do not silently stretch its scientific aspect ratio.
- For comparable X/Y physical units, apply `scaleanchor`/`scaleratio=1` and size the box from the displayed ranges as in the shared profile.
- Set per-series colors explicitly when needed: use the actual ordinary-series count, not the number of auxiliary traces for bands or error representations. Use categorical dashes `solid`, `dash`, `dot`, then `dashdot`; gradient-ordered curves stay solid.
- Apply 1.0 pt curve width, 3.2 pt marker size and 0.7 pt marker-edge width after conversion. For error bars use `thickness=0.6*96/72` and cap `width=1.6*96/72`. Preserve actual uncertainties and use line-only rendering for dense curves.
- Histograms retain raw Count unless density is requested. Render a light-filled outline along bin edges, not connected bin centers. Precompute counts with the original bin edges when reproducing another backend; do not silently rebin or normalize. For bands, group the band and its curve so legend toggles preserve their relationship.
- Use ordinary-font superscript log labels such as `10⁻⁶`, with tick positions at the actual powers of ten. Cover the displayed range, keep minor ticks readable and verify zoomed-axis labels when interactive zoom is required.
- Inside legends have no border. Move legends outside right when needed to avoid covering data, with a black 0.6 pt frame; reserve canvas space and follow the shared overflow/column rule.
- Set heatmap/surface `colorscale` explicitly from `gradient_stops(...)` or the profile. Put vertical colorbars outside right with a black outline matching the axis box, and explicit label/tick sizes. Avoid smoothing raw heatmaps unless requested or scientifically justified.

## Native 3D Rendering

- Use `scene.camera.projection.type="orthographic"`, visible native coordinates, transparent panes (`showbackground=False`), black axis lines and restrained major grid lines. Apply font sizes to scene axes separately; XY-axis updates do not style a 3D scene.
- Keep colorbars outside the data and labels, and preserve equal physical scale when coordinates have comparable units. Use `scene.aspectmode="data"` or a manual aspect ratio from displayed ranges as appropriate. Canvas dimensions and camera framing may be chosen for readability; the single-panel XY box rule does not constrain 3D scenes.
- **Native Plotly/Matplotlib rendering differences are accepted.** Do not change the accepted Plotly surface appearance, camera, lighting, coordinate-box edges or ticks solely to imitate Matplotlib. Do not add custom frame traces or port Matplotlib's rear-edge repair to force visual equivalence. This does not waive data accuracy, meaningful scale or readable labels.
- If the installed Plotly version cannot draw dotted 3D grids, use thin gray solid grids. Backend-native surface shading, tick placement and box appearance are normal differences, not defects requiring further adjustment.
- Keep 3D rotation and hover available. Hide axes only when Tao explicitly asks, following the shared hidden-axis rules where practical.

## Compact Offline HTML Export

- For interactive requests, deliver HTML without unsolicited static SVG/PNG/PDF copies. Use one shared, version-matched `plotly.min.js` in the output directory rather than embedding the full library in every page. Generate the JS from the same installed Plotly used to generate the figures, for example with `plotly.offline.get_plotlyjs()`.
- Reference the shared `plotly.min.js` and `tao-fonts.css` with relative paths. This is an offline folder bundle: when delivering or sharing, include the HTML and both companion files. Prefer this bundle over CDN dependencies by default. If Tao explicitly requires a single self-contained file, embed its resources once and accept the larger size.
- Serialize each figure only once. Reuse its `data` and `layout` in `Plotly.newPlot`; do not emit the entire figure JSON twice to access each property. Share one JS/font payload across plots in a combined page as well.
- Keep hover, zoom, pan, legend toggles and 3D rotation available as appropriate. A compact modebar with `displaylogo=False` is suitable. Preserve data precision and sampling when reducing file size.
- Example page initialization after loading the shared stylesheet and JS:

```javascript
async function renderFigure(figure) {
  // Pass the figure object that was serialized once into the page.
  await document.fonts.load('12px "Tao Helvetica"');
  await Plotly.newPlot('figure', figure.data, figure.layout,
    {displaylogo: false, responsive: false, scrollZoom: true});
}
```

- A toolbar SVG download does not automatically embed shared webfonts or convert text to paths. Do not describe it as the profile's font-stable publication SVG without separately verifying font preservation.

## Verification

Verify the exported folder in a browser, including offline loading of JS and the actual font face, labels/colorbars, fixed XY box sizes and relevant interactions. Test hover, legend toggles, zoom and rotation as applicable. When comparing to another backend, verify the numerical data, uncertainties and bins, rather than requiring pixel-identical rendering. Temporary screenshots are for QA; do not deliver extra image formats unless requested.

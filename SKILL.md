---
name: tao-style
description: Portable personal visual-style guidance for Tao's preferred output style. Use when the assistant is asked to create, edit, format, or export scientific plots, charts, data visualizations, figure panels, publication graphics, scientific slide reports, Beamer presentations, academic documents, manuscripts, reports, notes, handouts, diagrams, generated images, LaTeX/Beamer visual themes, or other artifacts where fonts, colors, labels, line widths, layout, or export settings matter. Apply directly when the user explicitly invokes $tao-style or asks to use Tao Style. When selected implicitly because the task may benefit from Tao Style, ask for confirmation and do not apply Tao Style until the user agrees.
---

# Tao Style

## Overview

Use this skill to apply Tao's personal visual style across portable AI tools and local development environments. Treat the current profile as the authoritative style specification: follow confirmed rules exactly, keep genuinely unspecified areas conservative, and avoid inventing strict requirements when the style has not been specified yet.

The current repository location is only a development and validation workspace. Resolve bundled resources relative to this `SKILL.md`; do not assume the current working directory, WSL, Python command name, or any fixed local path is available when the installed skill is used elsewhere.

## First Response Protocol

- Treat an explicit invocation such as `$tao-style`, "use Tao Style", or "use my saved style" as consent and apply it without an additional style-confirmation question.
- When this skill is selected implicitly because a plot, chart, scientific figure, diagram, image, presentation, or document may benefit from Tao Style, ask once whether to use it. Do not apply any Tao Style profile rules until the user agrees.
- If the user asks to generate a scientific slide report or presentation, ask whether to use Beamer unless the user already specified the output format.
- If the user asks to generate an academic document, manuscript, report, note, or handout and has not specified a template, ask whether to use the `yangtaogit/tao-document` template.
- If the user says yes, apply the current profile in `references/style-profile.md`.
- If the user says no, proceed with the requested output without Tao Style.
- If a required style detail is explicitly unspecified and materially affects the result, ask one concise question or use a neutral publication-style default and state the assumption.
- Combine any needed questions—style opt-in, output format or template, and required details—into one concise message instead of asking sequentially.
- Treat preferences stated for the current artifact as task-local unless Tao explicitly asks to save, remember, or update them as persistent Tao Style preferences.

## Composition with Artifact Skills

- Treat Tao Style as the visual-specification layer, not as a replacement for an available artifact-specific workflow.
- When another available skill handles the requested format—such as presentations, documents, PDFs, generated images, or interactive visualizations—follow that skill's creation, editing, rendering, and QA requirements while applying Tao Style to visual choices.
- If requirements conflict, follow the user's explicit request first, then the artifact-specific workflow, then Tao Style defaults.

## Plotting Workflow

1. Read `references/style-profile.md` before choosing visual parameters.
2. For scientific plots, read `references/scientific-plotting.md` and match the user's existing plotting stack. Default to Python/Matplotlib when the user leaves the stack open, but do not force Matplotlib when the task is already in R, MATLAB, Julia, C++, Gnuplot, LaTeX, Plotly, or another tool.
3. Load preferred fonts from bundled assets within the current rendering process when the backend supports local font registration. For Matplotlib, `matplotlib_rcparams()` performs this automatically; run `<skill-root>/scripts/manage_fonts.py --check` with an available Python runtime to verify it. Never copy bundled fonts into system or user font directories. If local loading is unsupported or fails, use a compatible fallback and disclose the substitution.
4. Prefer styling at the source plotting layer, such as Matplotlib rcParams, Seaborn themes, Plotly templates, ggplot themes, MATLAB defaults, Makie themes, ROOT styles, or pgfplots settings, instead of post-processing rendered images.
5. Apply typography, palette, line widths, marker sizes, tick style, legend placement, panel labels, and export settings consistently.
6. When the user does not specify an output format, save only one SVG file. Do not also create PNG, PDF, TIFF, or preview copies. Generate another format only when explicitly requested or required by the target medium.
7. Check that labels, units, legends, annotations, color scales, and tick text remain readable at the target output size.
8. Verify the rendered figure when possible, especially for clipping, overlapping text, low contrast, and illegible symbols.

## Scientific Slides Workflow

1. Read `references/style-profile.md` and `references/scientific-slides.md`.
2. When the user requests a scientific slide report, ask whether to use Beamer unless the user has already chosen Beamer, PowerPoint, Markdown slides, or another format.
3. If Tao chooses Beamer, base the report on the `yangtaogit/tao-slides` template. Inspect the template before editing and follow its actual file layout and build commands.
4. If Tao does not choose Beamer, use the requested format while preserving the confirmed Tao Style visual preferences where practical.
5. For plots included in slides, apply the scientific plotting module unless the user asks otherwise.

## Academic Documents Workflow

1. Read `references/style-profile.md` and `references/academic-documents.md`.
2. When the user requests an academic document, manuscript, report, note, or handout, ask whether to use the `yangtaogit/tao-document` template unless the user already chose or rejected a template.
3. If Tao chooses `tao-document`, base the document on `https://github.com/yangtaogit/tao-document`. Inspect the template before editing and follow its actual file layout and build commands.
4. Generate content in a copied template or a new document project directory. Do not modify the template source unless explicitly requested.
5. For plots included in documents, apply the scientific plotting module unless the user asks otherwise.

## Resource Map

- `references/style-profile.md`: Canonical style profile and shared Tao Style preferences.
- `references/scientific-plotting.md`: First concrete module, focused on research data visualization across plotting languages.
- `references/scientific-slides.md`: Scientific slide report rules, including Beamer template selection.
- `references/academic-documents.md`: Academic document rules, including the `yangtaogit/tao-document` template.
- `scripts/apply_tao_style.py`: Starter Matplotlib style helper that can be imported or used to print a style dictionary. Treat it as the Python implementation of the broader profile, not as the only supported backend.
- `scripts/manage_fonts.py`: Register bundled fonts only in the current Matplotlib process and verify availability.
- `assets/fonts/helvetica/`: Bundled Helvetica font files supplied for portable Tao Style setup.
- `assets/`: Store fonts, palettes, templates, example figures, or other reusable visual assets.

## Expansion Notes

- Keep scientific plotting rules in `references/scientific-plotting.md`.
- Keep scientific slide report and Beamer rules in `references/scientific-slides.md`.
- Keep academic document and `tao-document` template rules in `references/academic-documents.md`.
- Keep reusable implementation helpers in `scripts/`, grouped by backend when needed.

## Update Rules

- Update `references/style-profile.md` only when Tao explicitly asks to save, remember, or update a persistent visual preference. Do not persist a one-off artifact instruction automatically.
- Keep this `SKILL.md` concise; detailed examples, palettes, export presets, and font notes belong in `references/` or `assets/`.
- Do not add unrelated documentation files. Skills should contain only files that directly support the workflow.

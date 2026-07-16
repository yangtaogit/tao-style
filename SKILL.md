---
name: tao-style
description: Portable personal visual-style guidance for Tao's preferred output style. Use when the assistant is asked to create, edit, format, or export scientific plots, charts, data visualizations, figure panels, publication graphics, scientific slide reports, Beamer presentations, academic documents, manuscripts, reports, notes, handouts, diagrams, generated images, LaTeX/Beamer visual themes, or other artifacts where fonts, colors, labels, line widths, layout, or export settings matter. When triggered, ask whether to apply Tao Style unless the user already explicitly requested or rejected it.
---

# Tao Style

## Overview

Use this skill to apply Tao's personal visual style across portable AI tools and local development environments. Treat the current profile as the authoritative style specification: follow confirmed rules exactly, keep genuinely unspecified areas conservative, and avoid inventing strict requirements when the style has not been specified yet.

The current repository location is only a development and validation workspace. Do not assume WSL, Python, or any local path is available when the installed skill is used elsewhere.

## First Response Protocol

- If the user asks to generate or edit a plot, chart, scientific figure, diagram, or image and has not explicitly asked for Tao Style, ask once whether to use Tao Style.
- If the user asks to generate a scientific slide report or presentation, ask whether to use Beamer unless the user already specified the output format.
- If the user asks to generate an academic document, manuscript, report, note, or handout and has not specified a template, ask whether to use the `yangtaogit/tao-document` template.
- If the user says yes, apply the current profile in `references/style-profile.md`.
- If the user says no, proceed with the requested output without Tao Style.
- If the user already mentions `$tao-style`, "Tao Style", "my style", or a saved style preference, apply it without asking again.
- If a required style detail is explicitly unspecified and materially affects the result, ask one concise question or use a neutral publication-style default and state the assumption.
- Combine any needed questions—style opt-in, output format or template, and required details—into one concise message instead of asking sequentially.

## Plotting Workflow

1. Read `references/style-profile.md` before choosing visual parameters.
2. For scientific plots, read `references/scientific-plotting.md` and match the user's existing plotting stack. Default to Python/Matplotlib when the user leaves the stack open, but do not force Matplotlib when the task is already in R, MATLAB, Julia, C++, Gnuplot, LaTeX, Plotly, or another tool.
3. Check whether the preferred fonts are available before rendering. For Helvetica, run `python scripts/manage_fonts.py --check`. If it is missing, tell the user that the Skill includes a bundled copy and ask whether to install it. Do not install fonts without approval. If installation is declined or unavailable, then choose a compatible fallback with the user and state the substitution.
4. Prefer styling at the source plotting layer, such as Matplotlib rcParams, Seaborn themes, Plotly templates, ggplot themes, MATLAB defaults, Makie themes, ROOT styles, or pgfplots settings, instead of post-processing rendered images.
5. Apply typography, palette, line widths, marker sizes, tick style, legend placement, panel labels, and export settings consistently.
6. Check that labels, units, legends, annotations, color scales, and tick text remain readable at the target output size.
7. Verify the rendered figure when possible, especially for clipping, overlapping text, low contrast, and illegible symbols.

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
- `scripts/manage_fonts.py`: Check for and explicitly install bundled fonts after user approval.
- `assets/fonts/helvetica/`: Bundled Helvetica font files supplied for portable Tao Style setup.
- `assets/`: Store fonts, palettes, templates, example figures, or other reusable visual assets.

## Expansion Notes

- Keep scientific plotting rules in `references/scientific-plotting.md`.
- Keep scientific slide report and Beamer rules in `references/scientific-slides.md`.
- Keep academic document and `tao-document` template rules in `references/academic-documents.md`.
- Keep reusable implementation helpers in `scripts/`, grouped by backend when needed.

## Update Rules

- When Tao confirms a concrete visual preference, update `references/style-profile.md` instead of relying only on conversation memory.
- Keep this `SKILL.md` concise; detailed examples, palettes, export presets, and font notes belong in `references/` or `assets/`.
- Do not add unrelated documentation files. Skills should contain only files that directly support the workflow.

---
name: tao-style
description: Portable personal visual-style guidance for Tao's preferred output style. Use when Codex is asked to create, edit, format, or export scientific plots, charts, data visualizations, figure panels, publication graphics, diagrams, generated images, LaTeX/Beamer visual themes, or other artifacts where fonts, colors, labels, line widths, layout, or export settings matter. When triggered, ask whether to apply Tao Style unless the user already explicitly requested or rejected it.
---

# Tao Style

## Overview

Use this skill to apply Tao's personal visual style across portable AI tools and local development environments. Treat the current profile as a draft template: preserve confirmed preferences, mark unknowns as TODO, and avoid inventing strict requirements when the style has not been specified yet.

The current repository location is only a development and validation workspace. Do not assume WSL, Python, or any local path is available when the installed skill is used elsewhere.

## First Response Protocol

- If the user asks to generate or edit a plot, chart, scientific figure, diagram, or image and has not explicitly asked for Tao Style, ask once whether to use Tao Style.
- If the user says yes, apply the current profile in `references/style-profile.md`.
- If the user says no, proceed with the requested output without Tao Style.
- If the user already mentions `$tao-style`, "Tao Style", "my style", or a saved style preference, apply it without asking again.
- If a required style detail is still TODO and materially affects the result, ask one concise question or use a neutral publication-style default and state the assumption.

## Plotting Workflow

1. Read `references/style-profile.md` before choosing visual parameters.
2. For scientific plots, read `references/scientific-plotting.md` and match the user's existing plotting stack. Prefer Python when the user leaves the stack open, but do not force Python when the task is already in R, MATLAB, Julia, C++, Gnuplot, LaTeX, or another tool.
3. Prefer styling at the source plotting layer, such as Matplotlib rcParams, Seaborn themes, Plotly templates, ggplot themes, MATLAB defaults, Makie themes, ROOT styles, or pgfplots settings, instead of post-processing rendered images.
4. Apply typography, palette, line widths, marker sizes, tick style, legend placement, panel labels, and export settings consistently.
5. Check that labels, units, legends, annotations, color scales, and tick text remain readable at the target output size.
6. Verify the rendered figure when possible, especially for clipping, overlapping text, low contrast, and illegible symbols.

## Resource Map

- `references/style-profile.md`: Canonical style profile and TODO list for Tao's preferences.
- `references/scientific-plotting.md`: First concrete module, focused on research data visualization across plotting languages.
- `scripts/apply_tao_style.py`: Starter Matplotlib style helper that can be imported or used to print a style dictionary. Treat it as the Python implementation of the broader profile, not as the only supported backend.
- `assets/`: Store future fonts, palettes, templates, example figures, or other reusable visual assets.

## Expansion Notes

- Start with scientific plotting and keep its rules in `references/scientific-plotting.md`.
- Add future domains as separate references, for example `references/latex-beamer.md`, once Tao starts defining presentation or document style preferences.
- Keep reusable implementation helpers in `scripts/`, grouped by backend when needed.

## Update Rules

- When Tao confirms a concrete visual preference, update `references/style-profile.md` instead of relying only on conversation memory.
- Keep this `SKILL.md` concise; detailed examples, palettes, export presets, and font notes belong in `references/` or `assets/`.
- Do not add unrelated documentation files. Skills should contain only files that directly support the workflow.

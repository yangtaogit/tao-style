# tao-style Agent Notes

This repository is Tao's personal visual-style Skill. Use these notes when a new AI coding session opens this project.

## Project State

- Repository path: `/home/tao/git_repository/tao-style`
- Remote: `git@github.com:yangtaogit/tao-style.git`
- Skill name: `tao-style`
- Release tags: check `git tag --sort=-creatordate` for the current tagged release; do not assume this note is authoritative.
- Main installed WSL targets:
  - Codex: `/home/tao/.codex/skills/tao-style`
  - Claude Code: `/home/tao/.claude/skills/tao-style`

## What To Read First

1. Read `SKILL.md` for trigger behavior and workflow.
2. Read `references/style-profile.md` for cross-cutting Tao Style preferences.
3. For scientific plotting work, read `references/scientific-plotting.md`.
4. For scientific slide reports or Beamer work, read `references/scientific-slides.md`.
5. For academic documents or `tao-document` work, read `references/academic-documents.md`.
6. Use `scripts/apply_tao_style.py` as the Python/Matplotlib implementation helper.

## Active Style Modules

- Scientific plotting is the mature first module.
- Scientific slides/Beamer is the active second module.
- Academic documents with the `tao-document` template are the active third module.
- When generating scientific slide reports, ask whether to use Beamer if the output format is not specified.
- If Beamer is chosen, base the report on `https://github.com/yangtaogit/tao-slides` after inspecting the template structure.
- When generating academic documents, ask whether to use `https://github.com/yangtaogit/tao-document/` if no template is specified; inspect the template structure before generating.

## Important Scientific Plotting Rules

- Default plotting backend: Python/Matplotlib unless the user's stack is already different.
- Default single-plot axes box height: `1.8 in`; default `3:2` axes box is `2.7 in x 1.8 in`; keep exported single-panel canvas height fixed; use `0.42 in` as the initial left layout margin, but allow canvas width to expand left/right to avoid cropped labels and legends.
- Common single-plot ratios use the same default axes-box height: `1:1 = 1.8 in x 1.8 in`, `3:2 = 2.7 in x 1.8 in`, `5:3 = 3.0 in x 1.8 in`.
- Axis label font size: `9 pt`; tick label size: `8 pt`; legend size: `8 pt`.
- Preferred Latin font: Helvetica; preferred Chinese font: 宋体; math font: Computer Modern.
- Font-stable vector export: default SVG text should be converted to paths; default PDF output should embed fonts. Keep editable SVG/PDF text only when explicitly requested and target fonts are available.
- Axis box: black boxed axes, inward ticks on all sides, axis linewidth `0.6 pt`, major tick width `0.6`, minor tick width `0.3`, no grid by default.
- Units use square brackets: `Quantity [Unit]`.
- Log tick labels use plain-text superscripts such as `10⁻⁶`, not Matplotlib mathtext.
- Histograms must ask y-axis mode first: raw `Count` or `Probability Density [1/Unit]`.
- Default histograms use stepped bin outlines with light fill, not connected bin-center lines.
- Dense 2D data should usually use line-only rendering to avoid marker crowding.
- Preferred core palette: deep blue `#2A2F80`, black `#000000`, gray `#808080`; muted red `#B04A4A` only for explicit emphasis. For multiple curves, use deep blue, black, and gray first; use blue `#4378BC`, light gray, or other extension colors when more colors are needed; do not use red without emphasis semantics.
- Optional τ palette exists for special cases; it should not replace the default cool palette unless Tao asks.
- 3D plots: use perspective projection `projection="persp"`; pane color `#F2F2F2`; major-tick grid only with color `#9E9E9E`, dotted linestyle `":"`, and linewidth `0.2 pt`; no extra pane boundary lines or manual frames; inward ticks using `inward_factor=0.0` and `outward_factor=0.2`; `tick_pad=-3.0`; `labelpad=-4.0`; right-side colorbars with example spacing `pad=0.16`, `fraction=0.035`, `shrink=0.72`.

## README Audience Policy

- Keep `README.md` user-facing: describe what the Skill does, show examples, and explain installation, updating, and usage.
- Do not put personal development notes, local WSL paths, validation workflows, repository maintenance rules, or release-management reminders in `README.md` unless they are necessary for users.
- Put agent/developer-facing instructions in `AGENTS.md` instead.
- When the Skill changes, update corresponding user-facing README content only if public behavior, installation, usage, or documented style output changes.
- Keep README Chinese first; keep the English version synchronized when changing user-facing content.

## Development Workflow

- Keep reusable rules in `references/`.
- Keep deterministic plotting helpers in `scripts/apply_tao_style.py`.
- Keep formal examples in `example/`; keep throwaway visual tests in `test/`.
- `test/` is ignored by git and is not installed.
- When a visual preference is confirmed, update `references/style-profile.md` and the relevant module reference.
- When scientific plotting behavior changes, update `references/scientific-plotting.md` and regenerate affected examples.
- When scientific slide behavior changes, update `references/scientific-slides.md`.
- When academic document behavior changes, update `references/academic-documents.md`.
- When helper behavior changes, update `scripts/apply_tao_style.py` and run representative examples.
- Do not commit throwaway files from `test/`.

## Repository Layout

```text
tao-style/
|-- SKILL.md                          # Skill entry point and usage workflow
|-- AGENTS.md                         # Project guidance for coding agents
|-- agents/openai.yaml                # Codex UI metadata
|-- references/style-profile.md       # Overall τ Style preferences
|-- references/scientific-plotting.md # Scientific plotting rules
|-- references/scientific-slides.md   # Scientific report / slides and Beamer rules
|-- references/academic-documents.md  # Academic document and tao-document rules
|-- scripts/apply_tao_style.py        # Python plotting style helper
|-- scripts/install_skill.py          # Install/update script
|-- example/                          # Committed plotting examples and SVG outputs
|-- assets/                           # Assets such as logo files
`-- test/                             # Local debugging scripts and outputs; ignored by git
```

A `copy` installation copies `SKILL.md`, `agents/`, `assets/`, `references/`, and `scripts/`. `README.md`, `example/`, and `test/` are development/support files and are not required at runtime. `agents/openai.yaml` is Codex UI metadata; in Claude Code it is only a supporting file and does not affect how Claude Code reads `SKILL.md`.

## Local Validation

Run Skill validation after changing `SKILL.md`, `references/`, `scripts/`, install behavior, or agent metadata:

```bash
python3 /mnt/c/Users/yangt/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/tao/git_repository/tao-style
```

Compile Python helpers and examples when scripts change:

```bash
python3 -m py_compile scripts/apply_tao_style.py example/*.py
```

Regenerate examples when plotting behavior changes:

```bash
for script in example/*.py; do python3 "$script"; done
```

## Local Install And Sync

Update WSL-installed skills after copy-installable changes:

```bash
python3 scripts/install_skill.py --target all --mode copy --force
```

Useful Windows Codex Desktop target:

```bash
python3 scripts/install_skill.py --target codex --mode copy --skills-dir /mnt/c/Users/yangt/.codex/skills --force
```

For local WSL debugging where edits should take effect immediately:

```bash
python3 scripts/install_skill.py --target claude-code --mode symlink --force
```

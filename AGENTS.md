# tao-style Agent Notes

This repository is Tao's personal visual-style Skill. Use these notes when a new AI coding session opens this project.

## Project State

- Repository path: `/home/tao/git_repository/tao-style`
- Remote: `git@github.com:yangtaogit/tao-style.git`
- Skill name: `tao-style`
- Current release tag: `v0.1`
- Main installed WSL targets:
  - Codex: `/home/tao/.codex/skills/tao-style`
  - Claude Code: `/home/tao/.claude/skills/tao-style`

## What To Read First

1. Read `SKILL.md` for trigger behavior and workflow.
2. Read `references/style-profile.md` for cross-cutting Tao Style preferences.
3. For scientific plotting work, read `references/scientific-plotting.md`.
4. For scientific slide reports or Beamer work, read `references/scientific-slides.md`.
5. Use `scripts/apply_tao_style.py` as the Python/Matplotlib implementation helper.

## Active Style Modules

- Scientific plotting is the mature first module.
- Scientific slides/Beamer is the active second module.
- When generating scientific slide reports, ask whether to use Beamer if the output format is not specified.
- If Beamer is chosen, base the report on `https://github.com/yangtaogit/tao-slides` after inspecting the template structure.

## Important Scientific Plotting Rules

- Default plotting backend: Python/Matplotlib unless the user's stack is already different.
- Default single-plot axes box size: `3.0 in x 1.8 in` (`5:3`); keep exported single-panel canvas height fixed; use `0.42 in` as the initial left layout margin, but allow canvas width to expand left/right to avoid cropped labels and legends.
- Common single-plot ratios: `1:1`, `3:2`, `5:3`.
- Axis label font size: `9 pt`; tick label size: `8 pt`; legend size: `8 pt`.
- Preferred Latin font: Helvetica; preferred Chinese font: 宋体; math font: Computer Modern.
- Axis box: black boxed axes, inward ticks on all sides, axis linewidth `1.0 pt`, no grid by default.
- Units use square brackets: `Quantity [Unit]`.
- Log tick labels use plain-text superscripts such as `10⁻⁶`, not Matplotlib mathtext.
- Histograms must ask y-axis mode first: raw `Count` or `Probability Density [1/Unit]`.
- Default histograms use stepped bin outlines with light fill, not connected bin-center lines.
- Dense 2D data should usually use line-only rendering to avoid marker crowding.
- Preferred palette: Navy `#000080`, soft blue `#6CA6CD`, black, gray, muted red as low-priority accent.

## Development Workflow

- Keep reusable rules in `references/`.
- Keep deterministic plotting helpers in `scripts/apply_tao_style.py`.
- Keep formal examples in `example/`; keep throwaway visual tests in `test/`.
- When the Skill changes, update the corresponding README content in the same work session, including the English default section and Chinese version when user-facing behavior or documented rules change.
- `test/` is ignored by git and is not installed.
- Validate after Skill edits:

```bash
python3 /mnt/c/Users/yangt/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/tao/git_repository/tao-style
```

- Update WSL-installed skills after changes:

```bash
python3 scripts/install_skill.py --target all --mode copy --force
```
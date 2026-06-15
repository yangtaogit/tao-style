# τ Style

<p align="center">
  <img src="assets/tao-style-logo.png" alt="tau Style logo" width="420">
</p>

<p align="center">
  <a href="#chinese-version">Chinese Version / 中文版本</a>
</p>

`τ Style` is a personal visual-style Skill for generating scientific plots and slide reports with a consistent publication-oriented look. It currently focuses on scientific plotting, with initial support for Beamer-based scientific slide reports.

Use it when you want an AI coding assistant to apply Tao's preferred typography, colors, axes, legends, histogram conventions, and export behavior instead of starting from generic plotting defaults.

## What It Provides

- Scientific plotting style rules for Python/Matplotlib by default, with principles that can be adapted to Plotly, R, MATLAB, Julia, ROOT, and LaTeX/pgfplots.
- A reusable Matplotlib helper in `scripts/apply_tao_style.py`.
- Example figures showing the current plotting style.
- Slide-report guidance: when Beamer is chosen, use the public `yangtaogit/tao-slides` template.
- Installer support for Codex and Claude Code personal Skill directories.

## Style Summary

- Fonts: Helvetica for English text, Songti/宋体 for Chinese text, and Computer Modern for mathematical expressions.
- Axis text: axis labels use `9 pt`; tick labels use `8 pt`; legends use `8 pt`.
- Axes: boxed black axes, inward ticks on all sides, `1.0 pt` axis lines, minor ticks enabled, no grid by default.
- Labels and units: use square brackets, for example `Bias Voltage [V]` and `Current [A]`.
- Single-panel size: fixed physical XY axes box, default `3.0 in x 2.0 in` with a `3:2` ratio; common options are `1:1`, `3:2`, and `5:3`.
- Log axes: prefer plain-text superscripts such as `10⁻⁶` rather than Matplotlib mathtext.
- Colors: default cool palette with Navy `#000080`, soft blue `#6CA6CD`, black, gray, and muted red as a low-priority accent. A bright high-contrast palette is available as an optional alternative.
- Histograms: ask whether the y-axis should be raw `Count` or normalized `Probability Density [1/Unit]`; default histograms use stepped bin outlines with light fill.
- Output: prefer vector formats for line art and scientific figures.

For the full rule set, see `references/scientific-plotting.md` and `references/style-profile.md`.

## Plotting Examples

<table width="100%">
  <tr>
    <td width="50%">XY Data and Linear Fit</td>
    <td>Gaussian Error Bar</td>
  </tr>
  <tr>
    <td><img src="example/xy_linear_fit.svg" alt="XY linear fit example" height="190"></td>
    <td><img src="example/gaussian_errorbar.svg" alt="Gaussian error bar example" height="190"></td>
  </tr>
  <tr>
    <td width="50%">Log Axis</td>
    <td>Many Curves with External Legend</td>
  </tr>
  <tr>
    <td><img src="example/log_axis.svg" alt="Log axis example" height="190"></td>
    <td><img src="example/many_curves_gradient.svg" alt="Many curves gradient example" height="190"></td>
  </tr>
  <tr>
    <td width="50%">Color Gradients</td>
    <td>Bright High-Contrast Palette</td>
  </tr>
  <tr>
    <td><img src="example/color_gradients.svg" alt="Color gradient example" height="190"></td>
    <td><img src="example/bright_high_contrast_palette.svg" alt="Bright high-contrast palette example" height="190"></td>
  </tr>
  <tr>
    <td width="50%">Multiple Filled Histograms</td>
    <td></td>
  </tr>
  <tr>
    <td><img src="example/multiple_histograms.svg" alt="Multiple filled histograms example" height="190"></td>
    <td></td>
  </tr>
</table>

## Installation

Install this repository as a `tao-style/` folder under the target AI tool's `skills` directory. The installer supports Codex and Claude Code.

Clone the repository, then run one of the commands below from the repository root:

```bash
git clone https://github.com/yangtaogit/tao-style.git
cd tao-style
```

Install to Codex:

```bash
python3 scripts/install_skill.py --target codex --mode copy --force
```

Install to Claude Code:

```bash
python3 scripts/install_skill.py --target claude-code --mode copy --force
```

Install or update both:

```bash
python3 scripts/install_skill.py --target all --mode copy --force
```

Use `--skills-dir /path/to/skills` when you want to install to a custom Skill directory. Use `--dry-run` to preview the operation before copying files.

## Updating

To update an installed copy:

```bash
git pull
python3 scripts/install_skill.py --target all --mode copy --force
```

If you installed with `--mode symlink`, pulling or editing this repository is usually enough because the installed Skill points back to the working tree.

## Usage

Mention the Skill when asking an AI assistant to generate or revise a scientific figure:

```text
Please use $tao-style to generate this scientific figure.
```

In Claude Code, `/tao-style` can also be used directly. If the Skill is active and you ask for a scientific figure without explicitly requesting Tao Style, the assistant should ask whether to apply it before generating the plot.

## Chinese Version

<a id="chinese-version"></a>

`τ Style` 是一个个人视觉风格 Skill，用于让 AI 编程助手按照统一的科研绘图和报告风格生成输出。当前重点是科研绘图，并初步支持基于 Beamer 的科研 slides 报告。

当你希望 AI 使用 Tao 偏好的字体、配色、坐标轴、legend、直方图和导出规则，而不是使用通用默认绘图样式时，可以使用这个 Skill。

## 提供内容

- 默认面向 Python/Matplotlib 的科研绘图风格规则，也可迁移到 Plotly、R、MATLAB、Julia、ROOT 和 LaTeX/pgfplots。
- `scripts/apply_tao_style.py` 中的 Matplotlib helper。
- 展示当前绘图风格的示例图。
- 科研 slides 规则：当选择 Beamer 时，使用公开仓库 `yangtaogit/tao-slides` 模板。
- 支持安装到 Codex 和 Claude Code 的个人 Skill 目录。

## 风格概览

- 字体：英文使用 Helvetica，中文使用宋体，数学公式使用 Computer Modern。
- 字号：坐标轴标题 `9 pt`；tick 数字 `8 pt`；legend `8 pt`。
- 坐标轴：黑色封闭坐标框，四边 tick 向内，坐标轴线宽 `1.0 pt`，显示 minor ticks，默认不使用 grid。
- 标签与单位：单位使用方括号，例如 `Bias Voltage [V]`、`Current [A]`。
- 单图尺寸：固定 XY 坐标框物理尺寸，默认 `3.0 in x 2.0 in`，比例 `3:2`；常用比例包括 `1:1`、`3:2`、`5:3`。
- Log 坐标：优先使用 `10⁻⁶` 这类普通文本上标，而不是 Matplotlib mathtext。
- 颜色：默认冷色调配色，包括 Navy `#000080`、soft blue `#6CA6CD`、黑色、灰色，muted red 作为低优先级强调色；另有明亮高对比度配色作为可选方案。
- 直方图：绘制前询问 y 轴使用 raw `Count` 还是归一化 `Probability Density [1/Unit]`；默认使用阶梯状 bin 外轮廓加浅填充色。
- 输出：线图和科研图优先使用矢量格式。

完整规则见 `references/scientific-plotting.md` 和 `references/style-profile.md`。

## 绘图样例

<table width="100%">
  <tr>
    <td width="50%">XY 离散数据与拟合</td>
    <td>高斯分布样本误差棒</td>
  </tr>
  <tr>
    <td><img src="example/xy_linear_fit.svg" alt="XY linear fit example" height="190"></td>
    <td><img src="example/gaussian_errorbar.svg" alt="Gaussian error bar example" height="190"></td>
  </tr>
  <tr>
    <td width="50%">Log 坐标</td>
    <td>多曲线与外置 Legend</td>
  </tr>
  <tr>
    <td><img src="example/log_axis.svg" alt="Log axis example" height="190"></td>
    <td><img src="example/many_curves_gradient.svg" alt="Many curves gradient example" height="190"></td>
  </tr>
  <tr>
    <td width="50%">颜色梯度</td>
    <td>明亮高对比度配色</td>
  </tr>
  <tr>
    <td><img src="example/color_gradients.svg" alt="Color gradient example" height="190"></td>
    <td><img src="example/bright_high_contrast_palette.svg" alt="Bright high-contrast palette example" height="190"></td>
  </tr>
  <tr>
    <td width="50%">多个直方图填充</td>
    <td></td>
  </tr>
  <tr>
    <td><img src="example/multiple_histograms.svg" alt="Multiple filled histograms example" height="190"></td>
    <td></td>
  </tr>
</table>

## 安装

将本仓库安装为目标 AI 工具 `skills` 目录下的 `tao-style/` 文件夹。安装脚本支持 Codex 和 Claude Code。

先克隆仓库并进入目录：

```bash
git clone https://github.com/yangtaogit/tao-style.git
cd tao-style
```

安装到 Codex：

```bash
python3 scripts/install_skill.py --target codex --mode copy --force
```

安装到 Claude Code：

```bash
python3 scripts/install_skill.py --target claude-code --mode copy --force
```

同时安装或更新两者：

```bash
python3 scripts/install_skill.py --target all --mode copy --force
```

如果需要安装到自定义 Skill 目录，可添加 `--skills-dir /path/to/skills`。如果想先查看将执行的操作，可添加 `--dry-run`。

## 更新

更新已安装的 copy 版本：

```bash
git pull
python3 scripts/install_skill.py --target all --mode copy --force
```

如果使用 `--mode symlink` 安装，通常只需要更新或修改本仓库，因为安装目录会指向当前工作树。

## 使用

生成或修改科研图时，可以显式提到：

```text
请用 $tao-style 生成这张科研图。
```

在 Claude Code 中也可以直接使用 `/tao-style`。如果 Skill 已启用，而你请求生成科研图但没有明确指定是否使用 Tao Style，助手应先询问是否应用该风格。

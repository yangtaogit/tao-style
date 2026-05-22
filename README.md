# Tao Style

`Tao Style` 是一个个人 Codex Skill，用来保存和复用 Tao 的作图与视觉格式偏好。当前阶段只维护科研绘图部分；后续可以继续扩展到 LaTeX Beamer、文档、示意图等其它输出风格。

这个仓库是开发版 Skill 仓库，放在 WSL 下是为了方便调用 Python、C++ 等环境快速生成测试图。真正安装到 Codex 时，可以把它复制或链接到目标 `skills` 目录。

## 当前范围

- 科研数据绘图优先使用 Python，但风格规则应保持语言无关。
- 默认字体：英文 Helvetica，中文宋体，数学字体 Computer Modern。
- 坐标轴：封闭黑色坐标框，tick 向内，顶部和右侧也显示 tick，坐标轴线宽 1.0 pt。
- 坐标轴标题：9 pt；tick 数字：8 pt。
- 常用比例：`1:1`、`3:2`、`5:3`，生成图前应询问或确认。
- 单位格式：`Quantity [Unit]`。
- 常用颜色：冷色调、暗蓝、柔和蓝、黑色、灰色优先；红色仅低优先级强调色。
- 多曲线：优先使用暗蓝或灰度梯度；曲线很多时 legend 放在图框外右侧，竖向排列并带边框。

更完整的规则在 `references/style-profile.md` 和 `references/scientific-plotting.md` 中维护；Python helper 在 `scripts/apply_tao_style.py` 中维护。

## 绘图风格样例

下面的 SVG 图片由 `example/` 中的脚本生成，用来直观看当前科研绘图风格是否符合预期。重新生成全部样例：

```bash
for script in example/*.py; do python3 "$script"; done
```

### XY 离散数据与拟合

![XY linear fit example](example/xy_linear_fit.svg)

这个样例展示离散 marker、同色拟合线、冷色/黑灰优先色板、无边框框内 legend，以及 `Quantity [Unit]` 坐标轴标题格式。

### Gaussian Error Bar

![Gaussian error bar example](example/gaussian_errorbar.svg)

这个样例展示较小 marker、较细 error bar、Computer Modern 数学字体，以及多组数据对应同色拟合曲线。

### Log 坐标

![Log axis example](example/log_axis.svg)

这个样例展示 y 轴 base-10 log 坐标，主刻度使用 `10^{n}` 形式，tick 向内且上下左右都有 tick。

### 多曲线与外置 Legend

![Many curves gradient example](example/many_curves_gradient.svg)

这个样例展示超过 5 条曲线时的外置右侧竖向 legend。legend 带边框，边框线宽和 XY 坐标框一致；多曲线颜色优先使用暗蓝梯度。

## 安装

安装目标是某个 Codex `skills` 目录下的 `tao-style/` 文件夹。脚本支持两种模式：

- `copy`：复制可安装的 Skill 文件，适合从 WSL 仓库安装到 Windows Codex 目录，最稳妥。
- `symlink`：创建符号链接，适合同一文件系统内开发调试；后续改仓库即可立即更新。

在本机 WSL 仓库中运行：

```bash
cd /home/tao/git_repository/TaoStyle
```

推荐安装到 Windows Codex Desktop 的 skills 目录：

```bash
python3 scripts/install_skill.py --mode copy --skills-dir /mnt/c/Users/yangt/.codex/skills --force
```

如果只在 WSL 内调试 Codex，并希望仓库修改立即生效：

```bash
python3 scripts/install_skill.py --mode symlink --skills-dir ~/.codex/skills --force
```

先查看将要执行的操作：

```bash
python3 scripts/install_skill.py --mode copy --skills-dir /mnt/c/Users/yangt/.codex/skills --dry-run
```

## 更新

后续修改 Skill 后，按这个流程更新：

1. 修改 `SKILL.md`、`references/` 或 `scripts/apply_tao_style.py`。
2. 在 `test/` 中生成测试图，确认视觉效果。
3. 运行 Skill 校验。
4. 如果使用 `copy` 安装，重新运行安装命令；如果使用 `symlink` 安装，通常不需要额外同步。

校验命令：

```bash
python3 /mnt/c/Users/yangt/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/tao/git_repository/TaoStyle
```

更新到 Windows Codex Desktop：

```bash
python3 scripts/install_skill.py --mode copy --skills-dir /mnt/c/Users/yangt/.codex/skills --force
```

## 仓库结构

```text
TaoStyle/
├── SKILL.md                         # Skill 入口和触发/使用流程
├── agents/openai.yaml               # Codex UI 元数据
├── references/style-profile.md      # Tao Style 总体偏好
├── references/scientific-plotting.md # 科研绘图规则
├── scripts/apply_tao_style.py       # Python 绘图风格 helper
├── scripts/install_skill.py         # 安装/更新脚本
├── example/                         # 可提交的绘图风格样例脚本与 SVG 输出
├── assets/                          # 未来字体、模板、色板等资产
└── test/                            # 本地调试脚本与输出图，不复制到 copy 安装包
```

`copy` 安装只复制 `SKILL.md`、`agents/`、`assets/`、`references/` 和 `scripts/`。`README.md`、`example/` 和 `test/` 用于开发维护，不是 Skill 运行时必须内容。

## 使用

在需要作图时，可以显式提到：

```text
请用 $tao-style 生成这张科研图。
```

如果没有显式提到，但任务是生成或修改科研绘图，Skill 的设计是先询问是否采用 Tao Style，再根据你的确认应用风格。

## 维护原则

- 新确认的风格偏好优先写入 `references/style-profile.md`。
- 科研绘图细节写入 `references/scientific-plotting.md`。
- 可复用、可执行的确定性逻辑写入 `scripts/apply_tao_style.py`。
- 可提交的风格展示图放在 `example/`，用于 README 和长期对比。
- 测试脚本和输出图放在 `test/`，用于迭代视觉效果，不作为正式安装内容。

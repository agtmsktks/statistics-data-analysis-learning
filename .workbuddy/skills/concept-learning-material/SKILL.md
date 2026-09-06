---
name: concept-learning-material
description: 为「统计与数据分析」课程仓库生成标准化的概念学习资料（笔记 + 可运行 Python 示例 + 练习）。当用户要求讲解、生成、整理某个统计或数据分析概念的学习资料时触发，例如"帮我生成假设检验的学习资料"、"给我讲讲置信区间并配上例题"、"为回归分析创建学习笔记"。
agent_created: true
---

# 概念学习资料生成（Concept Learning Material）

## 概述

本技能用于为「统计与数据分析」课程仓库（`statistics-data-analysis-learning`）的任意概念生成一套**结构统一、可运行、可验证**的学习资料，包含笔记、示例脚本和练习三件套，并遵循仓库既有目录约定。

## 工作流程

按顺序执行以下步骤。产出三件套 = 1 个笔记 + 1 个示例脚本 + 1 个练习文件。

### 第 1 步：确定章节归属

根据概念主题，映射到对应章节目录（详见 `references/repo-conventions.md` 的映射表）：

| 概念举例 | 目录 |
|---------|------|
| 均值、中位数、分位数、异常值 | `01-描述性统计/` |
| 条件概率、贝叶斯、期望、常见分布 | `02-概率论基础/` |
| 中心极限定理、置信区间、假设检验、p 值 | `03-统计推断/` |
| 最小二乘、多元回归、残差分析 | `04-回归分析/` |
| 直方图、箱线图、散点图、图表选择 | `05-数据可视化/` |
| numpy / pandas / matplotlib 用法 | `06-Python数据分析工具/` |

若概念不属于任何现有章节，则新建 `NN-主题名/` 目录（编号顺延），并在仓库 README 中登记。

### 第 2 步：生成三件套

从 `assets/` 复制模板到章节目录（不在模板上直接改写，保持模板可复用）：

1. **笔记** `{概念名}-笔记.md` ← 复制 `assets/note-template.md`
2. **示例脚本** `{概念名}-示例.py` ← 复制 `assets/example-script-template.py`
3. **练习** `{概念名}-练习.md` ← 复制 `assets/exercise-template.md`

命名与写作规范见 `references/repo-conventions.md`。核心要求：
- 全部使用简体中文；公式用 `$...$`（行内）和 `$$...$$`（独立行）LaTeX 语法
- 笔记遵循"一句话理解 → 直观解释 → 数学定义 → Python 实战 → 常见误区 → 自测问题"的递进结构
- 示例脚本优先只用 Python 标准库（`statistics`、`math`、`random` 等）；确有必要才用 numpy/pandas
- 练习分"基础题 / 应用题 / 挑战题"三档，答案放在可折叠的 `<details>` 区块中

### 第 3 步：运行验证（必做，不可跳过）

写完脚本后立即运行，确保无错误：

```bash
python "{概念名}-示例.py"
```

（本机使用受管 Python：`C:/Users/Lenovo/.workbuddy/binaries/python/versions/3.13.12/python.exe`，运行含中文输出的脚本时加 `-X utf8` 参数避免控制台乱码。）

### 第 4 步：数值核对（必做，不可跳过）

**笔记中出现的所有计算结果数值，必须与脚本实际运行输出逐一对齐。** 先跑脚本，再根据真实输出填写笔记中的数字，不要先写估计值。示例数据若超过 20 条，优先放在 `datasets/` 目录下作为 CSV 文件，脚本从文件读取。

### 第 5 步：登记作业

若练习值得作为课后作业，在 `exercises/README.md` 的作业清单中追加一行：概念名、所属章节、练习文件路径、布置日期。

### 第 6 步：提交

```bash
git add -A
git commit -m "学习资料: {概念名}（笔记+示例+练习）"
```

推送（`git push`）前先询问用户确认；若网络阻断，参考仓库所在工作区根目录的 `push_via_api.py`（GitHub API 通道推送方案）。

## 资源说明

- `assets/note-template.md` — 笔记模板
- `assets/example-script-template.py` — 示例脚本模板
- `assets/exercise-template.md` — 练习模板
- `references/repo-conventions.md` — 仓库目录约定、写作风格、命名规范

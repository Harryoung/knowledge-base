# knowledge-base

[![CI](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

[English](./README.md) | 简体中文

面向开发者、运营人员和普通办公用户的本地优先知识库工具。它的目标很直接：把混乱的办公文档转成结构化 Markdown，并通过支持 Skill 的 Agent 软件直接使用这些能力。

如果你正需要下面这些能力，这个仓库值得你直接试用或 fork：

- 把 `DOCX`、`DOC`、`PDF`、`PPTX`、`PPT` 转成可落地的 Markdown
- 在 Excel 入库前先做复杂度判断，而不是一把梭硬解析
- 初始化一个带 `README`、`FAQ`、`BADCASE` 约定的本地知识库
- 复用一层小而清晰的文档收录能力，而不是从大项目里自己拆
- 把这套能力作为 Skill 分发给终端用户，而不是教每个人手工搭流程

## 这个仓库解决什么问题

知识库不好用，通常不是因为“没有模型”，而是因为输入层太脏：

- Office 文档格式不统一
- PDF 有数字版和扫描版两套现实
- 表格结构复杂，不能靠单一路径处理
- FAQ、README 导航、失败案例没有沉淀机制

`knowledge-base` 只做底层真正关键的部分：

- 文档转 Markdown
- Excel 复杂度路由
- 本地知识库初始化与迁移
- 基于 FAQ / README / 原文精读 / BADCASE 的检索纪律

它故意保持很小。原因很简单：越小越容易安装、审查、fork、改造和嵌入到你自己的 agent 工作流里。

## 核心能力

### 1. 面向真实输入的文档转换

- `DOCX` -> Markdown，基于 Pandoc
- `DOC` -> 先转 `DOCX`，再转 Markdown
- 数字版 `PDF` -> Markdown，基于 PyMuPDF4LLM
- 扫描版 `PDF` -> 明确检测并转交 OCR，而不是假装成功
- `PPTX` -> Markdown，基于 `pptx2md`
- `PPT` -> 先转 `PPTX`，再转 Markdown

如果文档里带图片，转换结果会把图片资产一起落到相邻目录。

### 2. Excel 复杂度分析

`scripts/complexity_analyzer.py` 会先看工作表结构，再告诉你这张表更适合走标准表路径还是复杂布局路径。这个步骤看起来朴素，但它决定了你的入库流程是稳定，还是迟早被脏表格拖垮。

### 3. 最小但够用的知识库约定

`scripts/kb_init.py` 会初始化一套最基础的本地知识库结构：

- `README.md`：导航入口
- `FAQ.md`：高频问答沉淀
- `BADCASE.md`：答不好的问题与缺口
- `contents_overview/`：内容收录目录

这套结构不大，但足够实用。

## 快速开始

### 方式 1：作为本地 Skill 安装

这是最干净的使用方式。适用于 Claude Code、Codex、OpenClaw，以及其他支持本地 Skill 的 Coding Agent 或通用 Agent 客户端。

1. 克隆或下载这个仓库。
2. 把 Skill 内容放到你的本地 Skills 目录，或者把当前仓库配置为本地 Skill 来源。
3. 在客户端里让 Agent 安装或使用 `knowledge-base` 这个 Skill。

真正的运行时准备工作，会在 Skill 被实际调用时按其工作流自动完成。

### 方式 2：打包后导入客户端

如果你的客户端支持导入 Skill 包，那么先打包成 `.zip` 或 `.skill`，再通过客户端的 Skill 导入界面安装即可。

注意，导入包应该只包含 Skill 运行真正需要的内容，而不是整个仓库的说明文档。

## 典型用法

### 把文件收录进你自己的知识库

1. 先确认知识库路径。
2. 把源文件转成 Markdown。
3. 将 Markdown 和图片资产放入知识库。
4. 对重要内容更新 README 导航或 FAQ。

常用命令：

```bash
python scripts/kb_config.py --check
python scripts/smart_convert.py ./deck.pptx --json-output
```

### 作为一个可复用的 Skill 来运行

真正的 agent 工作流约定写在 [SKILL.md](./SKILL.md) 里。如果你要接到自己的 agent 框架里，应该优先看那个文件。

## 为什么值得使用或 fork

- 你只想要文档收录层，不想继承整套 agent 架构
- 你需要一个 Office 文档转 Markdown 的参考实现
- 你希望办公用户通过支持 Skill 的客户端直接安装使用，而不是学习内部脚本
- 你希望本地知识库流程足够简单，方便当天就改造
- 你更接受“扫描 PDF 明确失败并转 OCR”，而不是静默产出垃圾结果
- 你希望起点就带测试、CI 和 Apache-2.0 许可

## 仓库结构

```text
knowledge-base/
├── .github/workflows/ci.yml
├── assets/
├── references/
├── scripts/
├── tests/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── NOTICE
```

## 开发

安装开发依赖并运行测试：

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

CI 会在 Python `3.10`、`3.11`、`3.12` 上执行相同检查。

## 打包成可分发的 Skill

按 Skill 的打包模型，分发包里应该只放 Skill 本体，以及它运行时真正需要的文件。

也就是说：

- 应该包含 `SKILL.md`
- 应该包含运行时需要的 `scripts/`、`references/`、`assets/`、`requirements.txt`
- 不应该把 `README.md`、`README.zh-CN.md`、`CHANGELOG.md`、`CONTRIBUTING.md`、`.git/`、`.github/` 这些仓库级文档或元信息塞进安装包

在仓库根目录执行下面这段代码，会生成：

- `dist/knowledge-base.zip`
- `dist/knowledge-base.skill`

其中 `.skill` 本质上仍然是 zip 容器，只是扩展名不同，方便支持 Skill 导入的客户端识别。

```bash
python - <<'PY'
from pathlib import Path
import shutil
import tempfile
import zipfile

root = Path.cwd().resolve()
dist = root / "dist"
dist.mkdir(exist_ok=True)

skill_name = "knowledge-base"
include = [
    "SKILL.md",
    "requirements.txt",
    "assets",
    "references",
    "scripts",
]

zip_path = dist / f"{skill_name}.zip"
skill_path = dist / f"{skill_name}.skill"

with tempfile.TemporaryDirectory() as tmp:
    stage_root = Path(tmp) / skill_name
    stage_root.mkdir()

    for item in include:
        src = root / item
        dst = stage_root / item
        if src.is_dir():
            shutil.copytree(
                src,
                dst,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
            )
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(stage_root.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(stage_root.parent))

shutil.copyfile(zip_path, skill_path)

print(f"Created: {zip_path}")
print(f"Created: {skill_path}")
PY
```

这套打包方式是刻意收紧过的：

- 产出的是干净 Skill 包，而不是整个仓库快照
- 仓库文档不会被误打进安装包
- 压缩包内部保留了标准的 Skill 目录结构
- 打包逻辑只存在于 README，不污染 `scripts/`

## 限制和非目标

- 这个仓库不内置 OCR
- 扫描版 PDF 会被检测出来并显式分流
- 它不是一个托管式 SaaS 知识库
- 它不假装所有 Excel 都能用同一种方式处理

这些限制不是缺点描述不全，而是设计边界。边界不写清楚，只会让项目表面更好看，实际更难用。

## 与上游项目的关系

当前仓库是原始项目 [Harryoung/efka](https://github.com/Harryoung/efka) 中知识库能力的独立抽取版本。

如果你需要更完整的 agent 上下文、集成流程和上游演进路径，可以去看那个仓库。  
如果你只想要更小、更干净、更容易维护的知识库层，这个仓库就是更合适的入口。

## 项目元信息

- License: [Apache-2.0](./LICENSE)
- 贡献说明: [CONTRIBUTING.md](./CONTRIBUTING.md)
- 变更记录: [CHANGELOG.md](./CHANGELOG.md)
- 上游派生说明: [NOTICE](./NOTICE)

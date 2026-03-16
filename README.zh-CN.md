# knowledge-base

[![CI](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

English README: [README.md](./README.md)

面向开发者的本地优先知识库工具。它的目标很直接：把混乱的办公文档转成结构化 Markdown，并在此之上建立一个可维护、可复用的本地知识库工作流。

如果你正需要下面这些能力，这个仓库值得你直接试用或 fork：

- 把 `DOCX`、`DOC`、`PDF`、`PPTX`、`PPT` 转成可落地的 Markdown
- 在 Excel 入库前先做复杂度判断，而不是一把梭硬解析
- 初始化一个带 `README`、`FAQ`、`BADCASE` 约定的本地知识库
- 复用一层小而清晰的文档收录能力，而不是从大项目里自己拆

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

它故意保持很小。原因很简单：越小越容易审查、fork、改造和嵌入到你自己的 agent 工作流里。

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

### 环境要求

- Python `3.10+`
- 首次运行需要联网，以便自动补 Pandoc
- 如果要处理 `.doc` 或 `.ppt`，需要 LibreOffice

### 安装运行时依赖

```bash
python scripts/ensure_deps.py
```

### 初始化知识库

```bash
python scripts/kb_config.py --set ~/my-kb
python scripts/kb_init.py ~/my-kb
```

### 转换文档

```bash
python scripts/smart_convert.py ./example.pdf --json-output
```

### 分析 Excel

```bash
python scripts/complexity_analyzer.py ./report.xlsx
```

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

## 为什么值得 fork

- 你只想要文档收录层，不想继承整套 agent 架构
- 你需要一个 Office 文档转 Markdown 的参考实现
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

如果你想得到一个干净的分发包，但又不想把打包逻辑塞进 `scripts/`，可以直接在仓库根目录执行下面这段代码。它会生成：

- `dist/knowledge-base-skill.zip`
- `dist/knowledge-base-skill.skill`

其中 `.skill` 本质上就是 zip 容器，只是换了扩展名，方便下游工具按 skill 包处理。

```bash
python - <<'PY'
from pathlib import Path
import shutil
import zipfile

root = Path.cwd().resolve()
dist = root / "dist"
dist.mkdir(exist_ok=True)

package_name = "knowledge-base-skill"
include = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "NOTICE",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "assets",
    "references",
    "scripts",
]

zip_path = dist / f"{package_name}.zip"
skill_path = dist / f"{package_name}.skill"

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for item in include:
        path = root / item
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and "__pycache__" not in child.parts:
                    arcname = Path(package_name) / child.relative_to(root)
                    zf.write(child, arcname)
        elif path.is_file():
            arcname = Path(package_name) / path.relative_to(root)
            zf.write(path, arcname)

shutil.copyfile(zip_path, skill_path)

print(f"Created: {zip_path}")
print(f"Created: {skill_path}")
PY
```

这套打包方式是刻意收敛过的：

- 只打包真正需要的 skill 内容和元数据
- 不带 `.git`、`.github`、测试缓存、虚拟环境等噪音
- 打包逻辑留在 README，不污染运行时 `scripts/` 目录

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

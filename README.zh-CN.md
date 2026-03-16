# local-knowledge-base

[![CI](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

[English](./README.md) | 简体中文

**把你的本地文件夹变成一个结构化、可问答的知识库 —— 由 AI Agent 驱动。**

大多数文档管理工具要么把你绑在云服务上，要么要求你搭向量数据库。`local-knowledge-base` 走了一条不同的路：它给你的 AI Agent（Claude Code、Codex、OpenClaw 等）赋予了文档收录、索引维护和知识问答的能力 —— 全程基于本地纯文件，不依赖任何外部服务。

## 核心能力

| 能力 | 做什么 | 为什么重要 |
|------|--------|-----------|
| **文档格式转换** | DOCX、DOC、PDF、PPTX、PPT → Markdown | 保留完整结构（表格、列表、图片），不只是提取文字 |
| **扫描版 PDF 检测** | 识别扫描 PDF 并分流到 OCR | 不再静默输出乱码垃圾 |
| **Excel 智能路由** | 处理前分析表格复杂度 | 简单表格走 Pandas 快速解析，复杂报表走 HTML 语义模式 |
| **五级问答链** | FAQ → README 导航 → 精读 → 关键词搜索 → BADCASE 记录 | 优先快速命中，全文检索是最后手段 |
| **知识库初始化与迁移** | 创建目录结构、迁移已有知识库 | 一条命令起步，迁移不丢数据 |

## 工作原理

```
         ┌─────────────────────────────────────────────┐
         │           你的 AI Agent（宿主应用）            │
         └──────────────────┬──────────────────────────┘
                            │ 安装并调用
                            ▼
┌──────────────────────────────────────────────────────────┐
│                local-knowledge-base Skill                 │
│                                                          │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ 文档收录  │  │   知识问答    │  │   知识库管理       │  │
│  │          │  │              │  │                    │  │
│  │ DOCX ───┐│  │ FAQ ────────┐│  │ 初始化 / 迁移 /   │  │
│  │ PDF  ───┤│  │ README ─────┤│  │ 配置              │  │
│  │ PPTX ───┤│  │ 精读 ───────┤│  └────────────────────┘  │
│  │ Excel ──┘│  │ 搜索 ───────┤│                          │
│  └──────────┘  │ BADCASE ────┘│                          │
│                └──────────────┘                          │
└──────────────────────────────────────────────────────────┘
                            │ 读写本地文件
                            ▼
              ┌──────────────────────────┐
              │   ~/your-knowledge-base   │
              │                          │
              │   README.md  (索引导航)   │
              │   FAQ.md     (高频问答)   │
              │   BADCASE.md (待补充)     │
              │   docs/      (文档内容)   │
              └──────────────────────────┘
```

这个 Skill 是 **AI Agent 的插件**，不是独立的命令行工具。它通过结构化工作流和 Python 脚本，教会你的 Agent *如何*管理一个知识库。可以理解为：给你的 Agent 增加了一项专业能力。

## 快速开始

### 1. 安装 Skill

```bash
# 克隆仓库
git clone https://github.com/Harryoung/local-knowledge-base.git

# Skill 本体是 local-knowledge-base/ 子目录
# 把这个目录指定为你 AI 客户端的本地 Skill 即可
```

兼容所有支持 Skill 格式的客户端：**Claude Code**、**Codex**、**OpenClaw** 等。

### 2. 直接用

安装后，用自然语言和 Agent 对话即可：

- *"在 ~/work/kb 建一个知识库"*
- *"把这份 PDF 收录到知识库"*
- *"入职文档里关于年假的规定是什么？"*
- *"把知识库迁移到新目录"*

Skill 会自动处理格式转换、冲突检测、索引维护和检索问答。

## 支持的格式

| 格式 | 转换方式 | 说明 |
|------|---------|------|
| DOCX | Pandoc | 完整保留文档结构 |
| DOC | LibreOffice → Pandoc | 先转 DOCX 再处理 |
| PDF（电子版） | PyMuPDF4LLM | 高速、高保真提取 |
| PDF（扫描版） | 检测 → `paddleocr-doc-parsing` OCR 分流 | 返回 `needs_ocr: true`；OCR 明确依赖 `https://clawhub.ai/Bobholamovic/paddleocr-doc-parsing` |
| PPTX | pptx2md | 保留幻灯片结构和演讲者注记 |
| PPT | LibreOffice → pptx2md | 先转 PPTX 再处理 |
| Excel | 复杂度分析器 | 简单表 → Pandas，复杂报表 → HTML 语义模式 |

## 仓库结构

仓库把 **Skill 运行时** 和 **开发文件** 分开管理：

```
.
├── local-knowledge-base/        ← Skill 本体（安装时只需要这个）
│   ├── SKILL.md                    入口 & 工作流定义
│   ├── requirements.txt            运行时依赖
│   ├── scripts/                    Python 脚本（转换、分析、初始化）
│   ├── assets/                     模板文件
│   └── references/                 详细工作流文档
│
├── tests/                       ← 单元测试（不属于 Skill）
├── .github/workflows/ci.yml    ← CI 流水线
├── pyproject.toml               ← 项目元数据
└── requirements-dev.txt         ← 开发依赖
```

这意味着打包非常简单 —— 直接压缩 `local-knowledge-base/` 就是一个干净的 Skill 包，不会混入任何仓库文件。

## 设计决策

几个让这个项目与众不同的选择：

- **扫描 PDF 的诚实处理。** 不会静默生成空白或乱码 Markdown。扫描版 PDF 会被明确检测并标记。这个项目里，扫描版 PDF 的 OCR 明确依赖 `https://clawhub.ai/Bobholamovic/paddleocr-doc-parsing`，而不是含糊地写成任意 OCR 工具。

- **Excel 复杂度路由。** 不是所有表格都一样。一个 10,000 行的数据表和一份带合并单元格的财务报表，需要完全不同的解析策略。复杂度分析器在处理前就做好路由决策。

- **语义冲突检测。** 收录新文档时，重复检测看的是内容含义，不是文件名。两个名字不同但内容相同的文件会被识别出来。

- **原子性文件更新。** FAQ、BADCASE 和 README 文件永远不会被部分覆盖。完整内容先在内存中准备好，再原子性替换，防止文件损坏。

- **速度优先的检索链。** 问答时先查 FAQ 和 README 导航，再做文件精读和 grep 搜索。大多数问题不需要扫描整个知识库。

## 开发

```bash
# 安装开发依赖
python -m pip install -r requirements-dev.txt

# 运行测试
python -m unittest discover -s tests -v

# 语法检查
python -m py_compile local-knowledge-base/scripts/*.py tests/*.py
```

### 打包 Skill

```bash
python - <<'PY'
from pathlib import Path
import shutil, zipfile

root = Path.cwd().resolve()
skill_dir = root / "local-knowledge-base"
dist = root / "dist"
dist.mkdir(exist_ok=True)

zip_path = dist / "local-knowledge-base.zip"
skill_path = dist / "local-knowledge-base.skill"

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(skill_dir.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            zf.write(path, path.relative_to(root))

shutil.copyfile(zip_path, skill_path)
print(f"Created: {zip_path}")
print(f"Created: {skill_path}")
PY
```

## 上游项目

从 [Harryoung/efka](https://github.com/Harryoung/efka) 中独立提取。如果你需要完整的 Agent 系统，去看那个仓库。如果只需要知识库能力作为可复用 Skill，这里是更轻量的入口。

## 许可证

[Apache-2.0](./LICENSE)

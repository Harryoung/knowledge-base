# local-knowledge-base

[![CI](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

[English](./README.md) | 简体中文

`local-knowledge-base` 是一个独立的 Skill 仓库。真正的 Skill 本体放在 [local-knowledge-base/](./local-knowledge-base) 目录下，仓库根目录只保留开发、测试、CI 和发布相关文件。

这个项目适合三类人：

- 想要一个小而干净的文档收录 Skill，而不是从大而杂的 Agent 系统里自己拆能力的开发者
- 使用支持 Skill 的客户端，希望直接安装就能用的办公团队和普通白领
- 需要本地优先文档转换、Excel 路由、FAQ 维护和知识库初始化能力的运营或实施人员

## 这个 Skill 能做什么

这个 Skill 只做本地知识库工作流里真正关键的底层部分：

- 把 `DOCX`、`DOC`、`PDF`、`PPTX`、`PPT` 转成 Markdown
- 在处理 Excel 前先做复杂度路由
- 初始化和迁移本地知识库
- 基于 FAQ、README 导航、原文精读和 BADCASE 进行问答

对于扫描版 PDF，它会明确检测并分流到 OCR，而不是假装转换成功。

## 仓库结构

这个仓库分成两层：

- [local-knowledge-base/](./local-knowledge-base)：Skill 本体
- 仓库根目录：文档、测试、CI、许可证、变更记录和贡献说明

### Skill 目录结构

```text
local-knowledge-base/
├── SKILL.md
├── requirements.txt
├── assets/
├── references/
└── scripts/
```

### 仓库根目录结构

```text
.
├── .github/workflows/ci.yml
├── local-knowledge-base/
├── tests/
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE
├── pyproject.toml
└── requirements-dev.txt
```

## 快速开始

### 方式 1：直接安装 Skill 文件夹

这是最干净的方式。适用于 Claude Code、Codex、OpenClaw，以及其他支持本地 Skill 的客户端。

1. 克隆或下载这个仓库。
2. 直接使用 [local-knowledge-base/](./local-knowledge-base) 这个文件夹作为 Skill 安装目录。
3. 把它放进本地 Skills 目录，或者在客户端里将其配置为本地 Skill 来源。
4. 让 Agent 安装或使用 `local-knowledge-base`。

### 方式 2：导入打包后的 Skill 包

如果你的客户端支持导入 `.zip` 或 `.skill`，那么把 `local-knowledge-base/` 目录打包后，通过客户端的 Skill 导入界面安装即可。

## 打包这个 Skill

现在 Skill 已经有了独立的顶层目录，所以打包时应该直接打包这个文件夹，而不是再从仓库根目录里拼装。

在仓库根目录执行：

```bash
python - <<'PY'
from pathlib import Path
import shutil
import zipfile

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

这样打出来的包是干净的，因为它只包含 Skill 文件夹本身：

- 会包含 `SKILL.md`、`requirements.txt`、`assets/`、`references/`、`scripts/`
- 不会混入 `README.md`、`CHANGELOG.md`、`CONTRIBUTING.md`、`.git/`、`.github/` 这些仓库级文件
- 压缩包内部会保留标准的 `local-knowledge-base/` 目录名

## 开发

安装开发依赖并运行测试：

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m py_compile local-knowledge-base/scripts/*.py tests/*.py
```

如果你在仓库根目录直接调试 Skill 脚本，应该使用 `local-knowledge-base/` 下的路径，例如：

```bash
python local-knowledge-base/scripts/kb_config.py --check
python local-knowledge-base/scripts/smart_convert.py ./example.pdf --json-output
```

## 为什么值得使用或 fork

- 你要的是一个独立 Skill，不是一个臃肿的大型 Agent 项目
- 你希望办公用户通过客户端安装 Skill，而不是学习内部脚本
- 你需要扫描版 PDF 的显式 OCR 分流，而不是静默产生垃圾结果
- 你希望仓库把 Skill 运行时文件和开发发布文件明确分层

## 与上游项目的关系

这个仓库是原始项目 [Harryoung/efka](https://github.com/Harryoung/efka) 中知识库能力的独立抽取版本。

如果你需要更完整的 Agent 上下文和上游演进路径，可以去看那个仓库。  
如果你只想要可复用的本地知识库 Skill，这个仓库是更小、更干净、更容易维护的入口。

## 项目元信息

- Skill 入口：[local-knowledge-base/SKILL.md](./local-knowledge-base/SKILL.md)
- License: [LICENSE](./LICENSE)
- 变更记录：[CHANGELOG.md](./CHANGELOG.md)
- 贡献说明：[CONTRIBUTING.md](./CONTRIBUTING.md)
- 上游说明：[NOTICE](./NOTICE)

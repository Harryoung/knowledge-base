# knowledge-base

独立可发布的本地知识库 Skill。它从 EFKA 中抽取了最核心的两类能力：

- 文档收录：DOCX / DOC / PDF / PPTX / PPT 转 Markdown，Excel 复杂度分析，知识库初始化与迁移
- 知识问答：FAQ 优先、README 导航、目标文件精读、关键词兜底、BADCASE 回流

## Upstream Relationship

当前仓库是从原始项目 [Harryoung/efka](https://github.com/Harryoung/efka) 中抽取并独立发布的知识库能力子集。
如需查看完整上下文、原始实现背景或上游演进，请回到该仓库。

## Repository Layout

```text
knowledge-base/
├── .github/workflows/ci.yml
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── NOTICE
├── SKILL.md
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .gitignore
├── assets/
├── references/
├── scripts/
└── tests/
```

## Runtime Requirements

- Python 3.10+
- 网络可用时首次自动安装 Pandoc
- 处理 `.doc` / `.ppt` 需要 LibreOffice

## GitHub Release Readiness

- Apache-2.0 许可证: [LICENSE](./LICENSE)
- 派生说明: [NOTICE](./NOTICE)
- 变更记录: [CHANGELOG.md](./CHANGELOG.md)
- 贡献说明: [CONTRIBUTING.md](./CONTRIBUTING.md)
- CI: [`.github/workflows/ci.yml`](./.github/workflows/ci.yml)

## Quick Start

```bash
python scripts/ensure_deps.py
python scripts/kb_config.py --set ~/my-kb
python scripts/kb_init.py ~/my-kb
```

然后按 [SKILL.md](./SKILL.md) 工作流执行收录或问答。

## Script Entry Points

- `python scripts/ensure_deps.py`
- `python scripts/kb_config.py --check`
- `python scripts/kb_config.py --set <path>`
- `python scripts/kb_config.py --migrate <new_path>`
- `python scripts/kb_init.py <path>`
- `python scripts/smart_convert.py <file> --json-output`
- `python scripts/complexity_analyzer.py <excel_file>`

## Testing

安装开发依赖后运行：

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

测试会使用临时目录和临时 `HOME`，不会污染用户真实配置。

GitHub Actions 会在 Python 3.10 / 3.11 / 3.12 上自动执行同一套检查。

## Publishing As A Standalone Repository

如果你要把当前目录直接推成独立仓库，最小步骤就是：

```bash
cd knowledge-base
git init
git add .
git commit -m "Initial standalone release"
```

然后在 GitHub 上新建同名仓库并推送。

## Design Corrections Relative To The Original Plan

- FAQ / BADCASE / README 更新使用原子替换，而不是假设“永远无并发”
- 扫描版 PDF 只做检测与分流，不伪装为已完成 OCR

## Sources

- EFKA document conversion and Excel parsing workflows
- Current library interfaces verified locally for `pypandoc`, `pymupdf4llm`, and `pptx2md`

# knowledge-base

[![CI](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

Chinese README: [README.zh-CN.md](./README.zh-CN.md)

Local-first knowledge base tooling for developers who want to turn messy office documents into structured Markdown and build a reusable Q&A workflow on top.

This repository is useful if you want to:

- convert `DOCX`, `DOC`, `PDF`, `PPTX`, and `PPT` into Markdown with predictable outputs
- route Excel files before ingestion instead of blindly parsing every spreadsheet the same way
- bootstrap a local knowledge base with `README`, `FAQ`, and `BADCASE` conventions
- fork a small, auditable document-ingestion layer instead of extracting it yourself from a larger agent project

## Why This Repo Exists

Most internal knowledge bases fail for boring reasons: the source files are inconsistent, office formats do not round-trip cleanly, and nobody maintains a disciplined place for FAQs and failure cases.

`knowledge-base` focuses on the lowest-level pieces that matter:

- document conversion into Markdown
- Excel complexity routing
- local knowledge-base initialization and migration
- retrieval discipline based on FAQ, README navigation, source reading, and BADCASE feedback

It is intentionally small. That makes it easier to fork, inspect, and adapt to your own agent or document workflow.

## What You Get

### 1. Document Conversion That Matches Real Inputs

- `DOCX` -> Markdown via Pandoc
- `DOC` -> `DOCX` via LibreOffice, then Markdown
- digital `PDF` -> Markdown via PyMuPDF4LLM
- scanned `PDF` detection with explicit OCR handoff instead of fake success
- `PPTX` -> Markdown via `pptx2md`
- `PPT` -> `PPTX` via LibreOffice, then Markdown

The converter also keeps extracted images in a sibling folder when needed.

### 2. Excel Routing Before You Burn Tokens or Time

`scripts/complexity_analyzer.py` inspects workbook structure and tells you whether a sheet looks like a standard table or a more complex layout. That is the difference between a pipeline that scales and one that collapses on the first ugly spreadsheet.

### 3. A Minimal Local Knowledge-Base Contract

`scripts/kb_init.py` creates a starter knowledge base with:

- `README.md` for navigation
- `FAQ.md` for repeated questions
- `BADCASE.md` for unanswered or weakly answered cases
- `contents_overview/` for organized intake

This is enough structure to be useful without dragging in a full platform.

## Quick Start

### Requirements

- Python `3.10+`
- internet access on first run so Pandoc can be installed automatically when missing
- LibreOffice if you need `.doc` or `.ppt` support

### Install Runtime Dependencies

```bash
python scripts/ensure_deps.py
```

### Initialize a Knowledge Base

```bash
python scripts/kb_config.py --set ~/my-kb
python scripts/kb_init.py ~/my-kb
```

### Convert a Document

```bash
python scripts/smart_convert.py ./example.pdf --json-output
```

### Analyze an Excel File

```bash
python scripts/complexity_analyzer.py ./report.xlsx
```

## Example Workflows

### Ingest a File Into Your Own KB

1. Set or check the KB path.
2. Convert the source file to Markdown.
3. Place the Markdown and extracted assets into your KB.
4. Update KB navigation or FAQ entries when the document is important.

Relevant commands:

```bash
python scripts/kb_config.py --check
python scripts/smart_convert.py ./deck.pptx --json-output
```

### Run the Project as a Reusable Skill

The operational workflow for agent usage lives in [SKILL.md](./SKILL.md). Use that file if you want the exact decision rules for ingestion, Q&A, migration, FAQ maintenance, and BADCASE updates.

## Why Developers Fork It

- You want the ingestion layer without inheriting an entire agent framework.
- You need a reference implementation for office-document to Markdown conversion.
- You want a local-first KB workflow that is simple enough to modify in an afternoon.
- You prefer explicit failure on scanned PDFs over silent garbage output.
- You want tests, CI, and an Apache-2.0 license before building on top of it.

## Repository Layout

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

## Development

Install dev dependencies and run tests:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

CI runs the same checks on Python `3.10`, `3.11`, and `3.12`.

## Package for Distribution

If you want a clean distributable archive without adding packaging logic to `scripts/`, run the following from the repository root. It creates both `dist/knowledge-base-skill.zip` and `dist/knowledge-base-skill.skill`.

`.skill` is just a zip archive with a different extension so downstream tools can treat it as a skill bundle.

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

This packaging approach is intentionally narrow:

- it includes the runtime scripts and skill metadata
- it excludes `.git`, `.github`, test artifacts, caches, and local virtual environments
- it keeps packaging logic out of the skill's actual runtime directory structure

## Limits and Non-Goals

- This repo does not perform OCR itself.
- Scanned PDFs are detected and routed out for OCR handling.
- It is not a hosted SaaS knowledge base.
- It does not pretend every spreadsheet should be parsed the same way.

Those constraints are deliberate. Hiding them would make the project look better for five minutes and worse forever.

## Upstream Relationship

This repository is an extracted, standalone subset of the original [Harryoung/efka](https://github.com/Harryoung/efka) project.

If you want the broader agent context, integrated workflows, or the upstream evolution path, start there. If you only want the knowledge-base layer, this repository is the smaller and more maintainable entry point.

## Project Metadata

- License: [Apache-2.0](./LICENSE)
- Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Notice for upstream derivation: [NOTICE](./NOTICE)

# knowledge-base

[![CI](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

English | [简体中文](./README.zh-CN.md)

Local-first knowledge-base tooling for developers, operators, and office users who want to turn messy documents into structured Markdown and use that knowledge through Skill-enabled agent software.

This repository is useful if you want to:

- convert `DOCX`, `DOC`, `PDF`, `PPTX`, and `PPT` into Markdown with predictable outputs
- route Excel files before ingestion instead of blindly parsing every spreadsheet the same way
- bootstrap a local knowledge base with `README`, `FAQ`, and `BADCASE` conventions
- fork a small, auditable document-ingestion layer instead of extracting it yourself from a larger agent project
- ship the capability as an installable Skill instead of teaching each user a manual workflow

## Why This Repo Exists

Most internal knowledge bases fail for boring reasons: the source files are inconsistent, office formats do not round-trip cleanly, and nobody maintains a disciplined place for FAQs and failure cases.

`knowledge-base` focuses on the lowest-level pieces that matter:

- document conversion into Markdown
- Excel complexity routing
- local knowledge-base initialization and migration
- retrieval discipline based on FAQ, README navigation, source reading, and BADCASE feedback

It is intentionally small. That makes it easier to install, fork, inspect, and adapt to your own agent or document workflow.

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

### Option 1. Install as a Local Skill Folder

This is the cleanest path for coding agents and general agents that support local skills, such as Claude Code, Codex, OpenClaw, or similar clients.

1. Clone or download this repository.
2. Copy the skill contents into your local skills directory, or add the repository as a local skill source if your client supports that.
3. Ask the agent to install or use the `knowledge-base` skill.

The runtime setup is handled by the skill workflow itself when it is actually used.

### Option 2. Import a Packaged Skill Bundle

If your client supports importing a bundle, create a `.zip` or `.skill` package and import it through the client's Skill UI.

The bundle should contain only the files the skill actually needs at runtime, not repository-only documentation.

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

## Why People Use or Fork It

- You want the ingestion layer without inheriting an entire agent framework.
- You need a reference implementation for office-document to Markdown conversion.
- You want office users to install the capability through a Skill-enabled client instead of learning internal scripts.
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

According to the skill packaging model, the distributable bundle should contain the skill itself and only the files required by that skill at runtime.

That means:

- include `SKILL.md`
- include required runtime resources such as `scripts/`, `references/`, `assets/`, and `requirements.txt`
- exclude repository-only files such as `README.md`, `README.zh-CN.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.git/`, and `.github/`

Run the following from the repository root to create both `dist/knowledge-base.zip` and `dist/knowledge-base.skill`.

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

This packaging approach is intentionally strict:

- it produces a clean skill bundle instead of a repository snapshot
- it keeps repository documentation out of the installed skill
- it preserves the expected skill folder structure inside the archive
- it keeps packaging logic out of `scripts/`

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

# local-knowledge-base

[![CI](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

English | [简体中文](./README.zh-CN.md)

**Turn your local folder into a structured, queryable knowledge base — powered by AI agents.**

Most document management tools either lock you into a cloud service or require a vector database. `local-knowledge-base` takes a different approach: it gives your AI agent (Claude Code, Codex, OpenClaw, etc.) the ability to ingest documents, maintain a navigable index, and answer questions — all from plain files on your machine.

## Key Features

| Feature | What it does | Why it matters |
|---------|-------------|----------------|
| **Document Conversion** | Converts DOCX, DOC, PDF, PPTX, PPT → Markdown | Preserves structure (tables, lists, images), not just raw text |
| **Scanned PDF Detection** | Identifies scanned PDFs and routes to OCR | No more silent garbage output from image-based pages |
| **Excel Smart Routing** | Analyzes spreadsheet complexity before processing | Simple tables get fast Pandas parsing; complex reports get semantic HTML |
| **5-Level Q&A Chain** | FAQ → README navigation → targeted reading → keyword search → BADCASE logging | Fast answers first, full-text search as last resort |
| **KB Initialization & Migration** | Sets up directory structure, moves existing KBs | One command to start; non-destructive migration |

## How It Works

```
         ┌─────────────────────────────────────────────┐
         │           Your AI Agent (host app)           │
         └──────────────────┬──────────────────────────┘
                            │ installs & invokes
                            ▼
┌──────────────────────────────────────────────────────────┐
│                  local-knowledge-base Skill               │
│                                                          │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │ Ingestion │  │  Q&A Engine  │  │  KB Management     │  │
│  │          │  │              │  │                    │  │
│  │ DOCX ───┐│  │ FAQ ────────┐│  │ Init / Migrate /  │  │
│  │ PDF  ───┤│  │ README nav ─┤│  │ Config             │  │
│  │ PPTX ───┤│  │ File read ──┤│  └────────────────────┘  │
│  │ Excel ──┘│  │ Grep ───────┤│                          │
│  └──────────┘  │ BADCASE ────┘│                          │
│                └──────────────┘                          │
└──────────────────────────────────────────────────────────┘
                            │ reads & writes
                            ▼
              ┌──────────────────────────┐
              │   ~/your-knowledge-base   │
              │                          │
              │   README.md  (index)     │
              │   FAQ.md     (Q&A pairs) │
              │   BADCASE.md (gaps)      │
              │   docs/      (content)   │
              └──────────────────────────┘
```

The Skill is a **plugin for AI agents**, not a standalone CLI app. It teaches your agent *how* to manage a knowledge base through structured workflows and Python scripts. Think of it as giving your agent a new professional capability.

## Quick Start

### 1. Install as a Skill

```bash
# Clone the repository
git clone https://github.com/Harryoung/local-knowledge-base.git

# The Skill is the local-knowledge-base/ subdirectory.
# Point your AI client to this folder as a local Skill.
```

Works with any client that supports the Skill format: **Claude Code**, **Codex**, **OpenClaw**, and others.

### 2. Use It

Once installed, just talk to your agent naturally:

- *"Set up a knowledge base at ~/work/kb"*
- *"Ingest this PDF into the knowledge base"*
- *"What does our onboarding doc say about vacation policy?"*
- *"Move the knowledge base to a new folder"*

The Skill handles format conversion, conflict detection, index maintenance, and retrieval automatically.

## Supported Formats

| Format | Method | Notes |
|--------|--------|-------|
| DOCX | Pandoc | Full structure preservation |
| DOC | LibreOffice → Pandoc | Converts to DOCX first |
| PDF (digital) | PyMuPDF4LLM | Fast, high-fidelity extraction |
| PDF (scanned) | Detected → OCR routing | Returns `needs_ocr: true` instead of garbage |
| PPTX | pptx2md | Preserves slide structure and speaker notes |
| PPT | LibreOffice → pptx2md | Converts to PPTX first |
| Excel | Complexity analyzer | Routes to Pandas (simple) or HTML semantic mode (complex) |

## Repository Structure

The repo separates the **Skill runtime** from **development files**:

```
.
├── local-knowledge-base/        ← The Skill (what gets installed)
│   ├── SKILL.md                    Entry point & workflow definitions
│   ├── requirements.txt            Runtime dependencies
│   ├── scripts/                    Python scripts (convert, analyze, init)
│   ├── assets/                     Templates
│   └── references/                 Detailed workflow documentation
│
├── tests/                       ← Unit tests (not part of the Skill)
├── .github/workflows/ci.yml    ← CI pipeline
├── pyproject.toml               ← Project metadata
└── requirements-dev.txt         ← Dev dependencies
```

This means packaging is trivial — just archive `local-knowledge-base/` and you have a clean Skill bundle with zero repo noise.

## Design Decisions

A few choices that set this project apart:

- **Scanned PDF honesty.** Instead of silently producing empty or garbled Markdown, scanned PDFs are detected and explicitly flagged. The agent knows to route them to OCR rather than pretending the conversion worked.

- **Excel complexity routing.** Not all spreadsheets are equal. A 10,000-row data table and a financial report with merged cells need completely different parsing strategies. The complexity analyzer decides before processing begins.

- **Semantic conflict detection.** When ingesting a new document, duplicates are checked by content meaning, not just filename. Two files named differently but covering the same topic get caught.

- **Atomic file updates.** FAQ, BADCASE, and README files are never partially overwritten. The full content is prepared in memory and replaced atomically to prevent corruption.

- **Speed-first retrieval.** The Q&A chain checks FAQ and README navigation before doing any file reads or grep searches. Most questions are answered without scanning the full corpus.

## Development

```bash
# Install dev dependencies
python -m pip install -r requirements-dev.txt

# Run tests
python -m unittest discover -s tests -v

# Syntax check
python -m py_compile local-knowledge-base/scripts/*.py tests/*.py
```

### Package the Skill

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

## Upstream

Extracted from [Harryoung/efka](https://github.com/Harryoung/efka). If you want the full agent system, start there. If you just want the knowledge-base capability as a reusable Skill, this is the lighter entry point.

## License

[Apache-2.0](./LICENSE)

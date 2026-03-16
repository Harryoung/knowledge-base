# local-knowledge-base

[![CI](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml/badge.svg)](https://github.com/Harryoung/local-knowledge-base/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)

English | [简体中文](./README.zh-CN.md)

`local-knowledge-base` is a standalone Skill repository. The actual Skill bundle lives in [local-knowledge-base/](./local-knowledge-base), while the repository root contains development, testing, CI, and publishing files.

This project is useful for:

- developers who want a small, auditable document-ingestion skill instead of extracting one from a larger agent system
- office teams who use Skill-enabled clients and want to install the capability directly
- operators who need a local-first workflow for document conversion, Excel routing, FAQ maintenance, and KB initialization

## What the Skill Does

The Skill focuses on the lowest-level pieces that matter in a local knowledge-base workflow:

- convert `DOCX`, `DOC`, `PDF`, `PPTX`, and `PPT` into Markdown
- route Excel files before choosing a processing path
- initialize and migrate a local knowledge base
- answer from FAQ, README navigation, source reading, and BADCASE feedback

Scanned PDFs are detected and explicitly routed to OCR instead of pretending conversion succeeded.

## Repository Structure

The repository is split into two layers:

- [local-knowledge-base/](./local-knowledge-base): the Skill itself
- repository root: documentation, tests, CI, license, changelog, and contribution files

### Skill Layout

```text
local-knowledge-base/
├── SKILL.md
├── requirements.txt
├── assets/
├── references/
└── scripts/
```

### Repository Root

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

## Quick Start

### Option 1. Install the Skill Folder

This is the cleanest path for Claude Code, Codex, OpenClaw, and other clients that support local Skills.

1. Clone or download this repository.
2. Use the [local-knowledge-base/](./local-knowledge-base) folder as the installed Skill folder.
3. Add that folder to your local Skills directory, or configure your client to load it as a local Skill.
4. Ask the agent to install or use `local-knowledge-base`.

### Option 2. Import a Packaged Skill Bundle

If your client supports importing a `.zip` or `.skill` bundle, package the `local-knowledge-base/` folder and import the result through the client's Skill UI.

## Package the Skill

Because the Skill now lives in its own top-level folder, packaging should archive that folder directly instead of trying to reconstruct the bundle from repository files.

Run the following from the repository root:

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

This produces a clean bundle because it packages only the Skill folder:

- includes `SKILL.md`, `requirements.txt`, `assets/`, `references/`, and `scripts/`
- excludes repository-only files such as `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `.git/`, and `.github/`
- preserves the expected `local-knowledge-base/` folder name inside the archive

## Development

Install dev dependencies and run tests:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -m py_compile local-knowledge-base/scripts/*.py tests/*.py
```

If you want to run the Skill scripts directly from the repository root during development, use paths under `local-knowledge-base/`, for example:

```bash
python local-knowledge-base/scripts/kb_config.py --check
python local-knowledge-base/scripts/smart_convert.py ./example.pdf --json-output
```

## Why People Use or Fork It

- You want a standalone Skill instead of a monolithic agent project.
- You want office users to install a Skill through a client instead of learning internal scripts.
- You want explicit OCR routing for scanned PDFs instead of silent garbage output.
- You want a repository that cleanly separates Skill runtime files from development and publishing files.

## Upstream Relationship

This repository is an extracted, standalone subset of the original [Harryoung/efka](https://github.com/Harryoung/efka) project.

If you want the broader agent context and upstream evolution path, start there. If you only want the local knowledge-base layer as a reusable Skill, this repository is the smaller and more maintainable entry point.

## Project Metadata

- Skill entry: [local-knowledge-base/SKILL.md](./local-knowledge-base/SKILL.md)
- License: [LICENSE](./LICENSE)
- Changelog: [CHANGELOG.md](./CHANGELOG.md)
- Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- Upstream notice: [NOTICE](./NOTICE)

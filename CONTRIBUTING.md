# Contributing

## Scope

This repository is intentionally small. Contributions should preserve that.

- Keep the skill standalone
- Do not reintroduce EFKA web-service architecture, Redis, or IM adapters
- Prefer simple filesystem-based workflows over framework-heavy abstractions

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements-dev.txt
```

## Before Opening A Pull Request

Run:

```bash
python -m unittest discover -s tests -v
python -m py_compile scripts/*.py tests/*.py
```

Check these manually:

- JSON CLI modes keep `stdout` machine-readable
- `FAQ.md`, `BADCASE.md`, and `README.md` update patterns remain atomic
- scanned PDF path still returns `needs_ocr: true` instead of pretending OCR succeeded

## Pull Request Expectations

- Explain the problem in concrete terms
- Keep changes narrowly scoped
- Update `README.md` or `CHANGELOG.md` when behavior changes

#!/usr/bin/env python3
"""Initialize a new knowledge-base directory structure."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parent.parent
README_TEMPLATE = SKILL_ROOT / "assets" / "kb_readme_template.md"

FAQ_TEMPLATE = """# FAQ - Frequently Asked Questions

| Question | Answer | Usage Count |
| --- | --- | --- |
"""

BADCASE_TEMPLATE = """# BADCASE - Gaps To Improve
"""


def write_file(path: Path, content: str) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/kb_init.py <kb_path>", file=sys.stderr)
        return 1

    kb_path = Path(sys.argv[1]).expanduser().resolve()
    kb_path.mkdir(parents=True, exist_ok=True)
    (kb_path / "contents_overview").mkdir(exist_ok=True)

    readme_template = README_TEMPLATE.read_text(encoding="utf-8")
    readme = readme_template.replace("{{DATE}}", date.today().isoformat()).replace("{{KB_PATH}}", str(kb_path))

    write_file(kb_path / "README.md", readme)
    write_file(kb_path / "FAQ.md", FAQ_TEMPLATE)
    write_file(kb_path / "BADCASE.md", BADCASE_TEMPLATE)

    print(
        json.dumps(
            {
                "success": True,
                "kb_path": str(kb_path),
                "created": ["README.md", "FAQ.md", "BADCASE.md", "contents_overview/"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

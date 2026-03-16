#!/usr/bin/env python3
"""Install runtime dependencies for the local-knowledge-base skill on first use."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".local-knowledge-base"
STAMP_FILE = STATE_DIR / ".deps_installed"
REQUIREMENTS_FILE = SKILL_ROOT / "requirements.txt"


def build_stamp() -> dict[str, str]:
    content = REQUIREMENTS_FILE.read_text(encoding="utf-8")
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "requirements_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
    }


def stamp_matches(expected: dict[str, str]) -> bool:
    if not STAMP_FILE.exists():
        return False
    try:
        current = json.loads(STAMP_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return current == expected


def ensure_requirements() -> None:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        check=True,
    )


def ensure_pandoc() -> None:
    import pypandoc

    try:
        pypandoc.get_pandoc_version()
    except OSError:
        pypandoc.download_pandoc()


def write_stamp(stamp: dict[str, str]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = STAMP_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(stamp, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_file.replace(STAMP_FILE)


def main() -> int:
    stamp = build_stamp()
    if stamp_matches(stamp):
        print(json.dumps({"success": True, "installed": False, "reason": "up_to_date"}, ensure_ascii=False))
        return 0

    ensure_requirements()
    ensure_pandoc()
    write_stamp(stamp)
    print(json.dumps({"success": True, "installed": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

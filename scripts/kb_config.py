#!/usr/bin/env python3
"""Persist and manage knowledge-base path configuration."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

STATE_DIR = Path.home() / ".knowledge-base-skill"
CONFIG_FILE = STATE_DIR / "config.json"
DEPS_STAMP_FILE = STATE_DIR / ".deps_installed"


def normalize_path(raw_path: str) -> Path:
    return Path(raw_path).expanduser().resolve()


def read_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def write_config(payload: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = CONFIG_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_file.replace(CONFIG_FILE)


def command_check() -> int:
    config = read_config()
    kb_path = config.get("kb_path")
    print(
        json.dumps(
            {
                "configured": bool(kb_path),
                "kb_path": kb_path,
                "deps_ready": DEPS_STAMP_FILE.exists(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def command_set(path_str: str) -> int:
    kb_path = normalize_path(path_str)
    write_config({"kb_path": str(kb_path)})
    print(json.dumps({"success": True, "kb_path": str(kb_path)}, ensure_ascii=False, indent=2))
    return 0


def command_get() -> int:
    config = read_config()
    kb_path = config.get("kb_path")
    print(json.dumps({"kb_path": kb_path}, ensure_ascii=False, indent=2))
    return 0


def command_migrate(path_str: str) -> int:
    config = read_config()
    current_path_raw = config.get("kb_path")
    if not current_path_raw:
        print(json.dumps({"success": False, "error": "Knowledge base path is not configured yet."}, ensure_ascii=False))
        return 1

    current_path = normalize_path(current_path_raw)
    new_path = normalize_path(path_str)
    new_path.mkdir(parents=True, exist_ok=True)

    for item in current_path.iterdir():
        destination = new_path / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(item, destination)

    write_config({"kb_path": str(new_path)})
    print(
        json.dumps(
            {
                "success": True,
                "old_path": str(current_path),
                "kb_path": str(new_path),
                "note": "Files were copied. The old knowledge base directory was left in place.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage knowledge-base skill configuration.")
    parser.add_argument("--check", action="store_true", help="Check whether the knowledge base is configured")
    parser.add_argument("--get", action="store_true", help="Get the configured knowledge base path")
    parser.add_argument("--set", metavar="PATH", help="Set the knowledge base path")
    parser.add_argument("--migrate", metavar="NEW_PATH", help="Copy the knowledge base to a new path and update config")
    args = parser.parse_args()

    if args.check:
        return command_check()
    if args.get:
        return command_get()
    if args.set:
        return command_set(args.set)
    if args.migrate:
        return command_migrate(args.migrate)

    parser.error("Choose one of: --check, --get, --set PATH, --migrate NEW_PATH")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

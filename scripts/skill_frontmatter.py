#!/usr/bin/env python3
"""Frontmatter parser for Harness skill files."""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import NoReturn

CODEX_MIRROR_IGNORED_DIRS = {"__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
CODEX_MIRROR_IGNORED_NAMES = {".DS_Store"}
CODEX_MIRROR_IGNORED_SUFFIXES = {".pyc", ".pyo"}


def should_include_codex_mirror_file(path: Path) -> bool:
    if any(part in CODEX_MIRROR_IGNORED_DIRS for part in path.parts):
        return False
    if path.name in CODEX_MIRROR_IGNORED_NAMES:
        return False
    return path.suffix not in CODEX_MIRROR_IGNORED_SUFFIXES


def fail(message: str) -> NoReturn:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(f"INVALID FRONTMATTER: {path} must start with ---")
    try:
        end = lines.index("---", 1)
    except ValueError:
        fail(f"INVALID FRONTMATTER: {path} missing closing ---")

    def parse_scalar(field: str, raw: str) -> str:
        value = raw.strip()
        if not value:
            fail(f"EMPTY FRONTMATTER VALUE: {path} field {field}")
        if value[0] in ("'", '"'):
            try:
                parsed = ast.literal_eval(value)
            except (SyntaxError, ValueError) as exc:
                fail(f"INVALID FRONTMATTER QUOTE: {path} field {field}: {exc}")
            if not isinstance(parsed, str):
                fail(f"INVALID FRONTMATTER VALUE: {path} field {field} must be a string")
            return parsed
        if ": " in value:
            fail(f"UNQUOTED FRONTMATTER COLON: {path} field {field}")
        return value

    fields: dict[str, str] = {}
    in_metadata = False
    for raw_line in lines[1:end]:
        if not raw_line.strip():
            continue
        if raw_line.startswith("  "):
            if not in_metadata:
                fail(f"INVALID FRONTMATTER INDENT: {path}: {raw_line!r}")
            key, sep, raw_value = raw_line.strip().partition(":")
            if not sep:
                fail(f"INVALID FRONTMATTER LINE: {path}: {raw_line!r}")
            if key == "version":
                fields["version"] = parse_scalar("metadata.version", raw_value)
            continue
        in_metadata = False
        key, sep, raw_value = raw_line.partition(":")
        if not sep:
            fail(f"INVALID FRONTMATTER LINE: {raw_line!r}")
        if key == "metadata":
            if raw_value.strip():
                fail(f"INVALID FRONTMATTER METADATA: {path} metadata must be a mapping")
            in_metadata = True
        elif key in {"name", "description", "when_to_use", "dispatch_intent"}:
            fields[key] = parse_scalar(key, raw_value)

    name = fields.get("name")
    description = fields.get("description")
    if not name or not name.strip():
        fail(f"MISSING name: in {path}")
    if not description or not description.strip():
        fail(f"MISSING description: in {path}")

    if "version" in fields:
        fail(f"STALE metadata.version: remove per-skill version; use top-level VERSION file")

    return {
        "name": name.strip(),
        "description": description.strip(),
        "when_to_use": fields.get("when_to_use", "").strip(),
        "dispatch_intent": fields.get("dispatch_intent", "").strip(),
    }


def parse_when_to_use_keywords(when_to_use: str) -> set[str]:
    return {kw.strip().lower() for kw in when_to_use.split(",") if kw.strip()}

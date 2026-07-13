#!/usr/bin/env python3
"""Validate Zack skill metadata and references."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_frontmatter import parse_frontmatter, fail


def check_skill_files(root: Path):
    skill_files = sorted((root / "skills").glob("**/SKILL.md"))
    if not skill_files:
        fail("ERROR: no SKILL.md files found under skills/")
    skill_descriptions = {}
    for path in skill_files:
        fields = parse_frontmatter(path)
        skill_descriptions[fields["name"]] = fields["description"]
    return skill_files, skill_descriptions


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skill_files, skill_descriptions = check_skill_files(root)
    for name, desc in skill_descriptions.items():
        if not desc.strip():
            fail(f"ERROR: skill {name} has empty description")
    if not (root / "VERSION").exists():
        fail("ERROR: VERSION file missing")
    version = (root / "VERSION").read_text().strip()
    print(f"ok: {len(skill_files)} skills, VERSION={version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

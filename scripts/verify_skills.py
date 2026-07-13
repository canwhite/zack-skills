#!/usr/bin/env python3
"""Validate Zack skill metadata and references."""

from __future__ import annotations

import re
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


def check_per_skill_check_update(root: Path, version: str) -> None:
    """Catch the BUG-12 class: per-skill check-update.sh must carry the current VERSION."""
    expected = f'LOCAL_VERSION="${{LOCAL_VERSION:-v{version}}}"'
    pattern = re.compile(r'LOCAL_VERSION="\$\{LOCAL_VERSION:-v\d+\.\d+\.\d+\}"')
    for cu in sorted(root.glob("skills/**/scripts/check-update.sh")):
        text = cu.read_text()
        match = pattern.search(text)
        if not match:
            fail(f"ERROR: {cu.relative_to(root)} missing LOCAL_VERSION pattern")
        if match.group(0) != expected:
            fail(
                f"ERROR: {cu.relative_to(root)} LOCAL_VERSION drifted "
                f"(found {match.group(0)!r}, expected {expected!r}). "
                f"Run `make regenerate`."
            )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skill_files, skill_descriptions = check_skill_files(root)
    for name, desc in skill_descriptions.items():
        if not desc.strip():
            fail(f"ERROR: skill {name} has empty description")
    if not (root / "VERSION").exists():
        fail("ERROR: VERSION file missing")
    version = (root / "VERSION").read_text().strip()
    check_per_skill_check_update(root, version)
    print(f"ok: {len(skill_files)} skills, VERSION={version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Zack Skills CLI - Manage your skill toolkit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILLS_DIR = ROOT / "skills"
PLUGIN_FILE = ROOT / ".claude-plugin" / "plugin.json"


def load_skills():
    """Load all skills from skills/ directory."""
    skills = []
    for path in sorted(SKILLS_DIR.glob("**/SKILL.md")):
        name = path.parent.name
        category_path = path.parent.relative_to(SKILLS_DIR)
        text = path.read_text()
        lines = text.splitlines()

        description = ""
        for line in lines:
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                description = desc
                break

        skills.append({"name": name, "description": description, "category_path": str(category_path)})
    return skills


def load_plugin():
    """Load plugin.json."""
    if not PLUGIN_FILE.exists():
        return {"name": "zack-skills", "skills": []}
    return json.loads(PLUGIN_FILE.read_text())


def save_plugin(data):
    """Save plugin.json."""
    PLUGIN_FILE.parent.mkdir(parents=True, exist_ok=True)
    PLUGIN_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def cmd_list(skills, plugin_data):
    """List available and installed skills."""
    installed = set(plugin_data.get("skills", []))
    print("\n Available skills\n Install once, then say 'Use zack-…' in your agent\n")
    for s in skills:
        name = s["name"]
        desc = s["description"].split(". Use when")[0] if s["description"] else ""
        # truncate description
        if len(desc) > 60:
            desc = desc[:57] + "..."
        if desc:
            desc = " " + desc
        status = "installed" if f"./skills/{s['category_path']}" in installed else ""
        mark = "◆" if status else "○"
        print(f"  {mark} {name}{desc}")
        if status:
            print(f"    (installed)")
    print()


def cmd_add(skill_name, plugin_data):
    """Add a skill to plugin.json."""
    skills = load_skills()
    skill_entry = next((s for s in skills if s["name"] == skill_name), None)
    if not skill_entry:
        print(f"Unknown skill: {skill_name}")
        available = ", ".join(s["name"] for s in skills)
        print(f"Available: {available}")
        sys.exit(1)
    skill_path = f"./skills/{skill_entry['category_path']}"
    current_skills = set(plugin_data.get("skills", []))

    if skill_path in current_skills:
        print(f"Already installed: {skill_name}")
        return

    plugin_data["skills"] = sorted(list(current_skills) + [skill_path])
    save_plugin(plugin_data)
    print(f"Added: {skill_name}")


def cmd_remove(skill_name, plugin_data):
    """Remove a skill from plugin.json."""
    skills = load_skills()
    skill_entry = next((s for s in skills if s["name"] == skill_name), None)
    if not skill_entry:
        print(f"Unknown skill: {skill_name}")
        return
    skill_path = f"./skills/{skill_entry['category_path']}"
    current_skills = set(plugin_data.get("skills", []))

    if skill_path not in current_skills:
        print(f"Not installed: {skill_name}")
        return

    plugin_data["skills"] = sorted(current_skills - {skill_path})
    save_plugin(plugin_data)
    print(f"Removed: {skill_name}")


def cmd_init(plugin_data):
    """Initialize plugin.json with all skills."""
    skills = load_skills()
    plugin_data = {
        "name": "zack-skills",
        "skills": sorted([f"./skills/{s['category_path']}" for s in skills])
    }
    save_plugin(plugin_data)
    print(f"Initialized with {len(skills)} skills")


def cmd_all(plugin_data):
    """Add all missing skills to plugin.json (skips already-installed)."""
    skills = load_skills()
    current_skills = set(plugin_data.get("skills", []))
    added = []
    skipped = []
    for s in skills:
        skill_path = f"./skills/{s['category_path']}"
        if skill_path in current_skills:
            skipped.append(s["name"])
        else:
            current_skills.add(skill_path)
            added.append(s["name"])
    plugin_data["skills"] = sorted(current_skills)
    save_plugin(plugin_data)
    print(f"Added {len(added)} skill(s): {', '.join(added) if added else 'none'}")
    if skipped:
        print(f"Skipped {len(skipped)} already-installed: {', '.join(skipped)}")


def main():
    parser = argparse.ArgumentParser(prog="zack-skills")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List available skills")
    sub.add_parser("init", help="Initialize plugin.json with all skills")
    sub.add_parser("all", help="Add all missing skills (skips already-installed)")

    add_p = sub.add_parser("add", help="Add a skill")
    add_p.add_argument("skill", help="Skill name to add")

    remove_p = sub.add_parser("remove", help="Remove a skill")
    remove_p.add_argument("skill", help="Skill name to remove")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    skills = load_skills()
    plugin_data = load_plugin()

    if args.cmd == "list":
        cmd_list(skills, plugin_data)
    elif args.cmd == "add":
        cmd_add(args.skill, plugin_data)
    elif args.cmd == "remove":
        cmd_remove(args.skill, plugin_data)
    elif args.cmd == "init":
        cmd_init(plugin_data)
    elif args.cmd == "all":
        cmd_all(plugin_data)


if __name__ == "__main__":
    main()

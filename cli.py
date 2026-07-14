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


def _global_skills_dir():
    return Path.home() / ".claude" / "skills"


def _ensure_global_symlink(name, target_path):
    """Create or repair ~/.claude/skills/<name> symlink to target_path.
    Returns one of: 'created', 'repointed', 'ok', 'missing-dir', 'blocked'.

    - 'created'   : new symlink added
    - 'repointed' : existing symlink had different target; replaced
    - 'ok'        : symlink already points at this target
    - 'missing-dir': ~/.claude/skills/ does not exist (nothing to do)
    - 'blocked'   : path exists but is not a symlink (refuse to clobber)
    """
    import os
    gdir = _global_skills_dir()
    if not gdir.exists():
        return "missing-dir"
    link = gdir / name
    target = str(Path(target_path).resolve())
    if link.is_symlink():
        try:
            current = os.readlink(link)
        except OSError:
            current = None
        if current is not None and (current == target or str(Path(current)) == target):
            return "ok"
        link.unlink()
        os.symlink(target, link)
        return "repointed"
    if link.exists():
        return "blocked"
    os.symlink(target, link)
    return "created"


def _remove_global_symlink(name):
    """Remove ~/.claude/skills/<name> if it's a symlink. Returns True if removed."""
    link = _global_skills_dir() / name
    if link.is_symlink():
        link.unlink()
        return True
    return False


def cmd_add(skill_name, plugin_data):
    """Add a skill: update plugin.json AND ensure ~/.claude/skills/<name> symlink."""
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
        print(f"plugin.json: already has {skill_name}")
    else:
        plugin_data["skills"] = sorted(list(current_skills) + [skill_path])
        save_plugin(plugin_data)
        print(f"plugin.json: added {skill_name}")

    action = _ensure_global_symlink(skill_name, ROOT / "skills" / skill_entry["category_path"])
    if action == "created":
        print(f"~/.claude/skills/{skill_name}: linked")
    elif action == "repointed":
        print(f"~/.claude/skills/{skill_name}: repointed")
    elif action == "ok":
        print(f"~/.claude/skills/{skill_name}: already linked")
    elif action == "blocked":
        print(f"~/.claude/skills/{skill_name}: ⚠ blocked — a non-symlink exists at that path")
        sys.exit(1)
    elif action == "missing-dir":
        print(f"~/.claude/skills/: dir not found, skipped link")


def cmd_remove(skill_name, plugin_data):
    """Remove a skill: update plugin.json AND remove ~/.claude/skills/<name> symlink."""
    skills = load_skills()
    skill_entry = next((s for s in skills if s["name"] == skill_name), None)
    if not skill_entry:
        print(f"Unknown skill: {skill_name}")
        return
    skill_path = f"./skills/{skill_entry['category_path']}"
    current_skills = set(plugin_data.get("skills", []))

    if skill_path in current_skills:
        plugin_data["skills"] = sorted(current_skills - {skill_path})
        save_plugin(plugin_data)
        print(f"plugin.json: removed {skill_name}")
    else:
        print(f"plugin.json: {skill_name} was not installed")

    if _remove_global_symlink(skill_name):
        print(f"~/.claude/skills/{skill_name}: symlink removed")
    else:
        print(f"~/.claude/skills/{skill_name}: no symlink to remove")


def _ensure_global_symlinks_bulk(skills):
    """Bulk-create ~/.claude/skills/<name> symlinks for every skill in `skills`.
    Mutates global state; returns a count summary string."""
    if not skills:
        return ""
    created = repointed = ok = blocked = missing = 0
    for s in skills:
        action = _ensure_global_symlink(s["name"], ROOT / "skills" / s["category_path"])
        if action == "created":
            created += 1
        elif action == "repointed":
            repointed += 1
        elif action == "ok":
            ok += 1
        elif action == "blocked":
            blocked += 1
        elif action == "missing-dir":
            missing += 1
    parts = []
    if created:
        parts.append(f"{created} linked")
    if repointed:
        parts.append(f"{repointed} repointed")
    if ok:
        parts.append(f"{ok} already linked")
    if blocked:
        parts.append(f"{blocked} blocked")
    if missing:
        parts.append(f"global dir missing")
    return ", ".join(parts) if parts else "no-op"


def cmd_init(plugin_data):
    """Initialize plugin.json with all skills AND bulk-link ~/.claude/skills/."""
    skills = load_skills()
    plugin_data = {
        "name": "zack-skills",
        "skills": sorted([f"./skills/{s['category_path']}" for s in skills])
    }
    save_plugin(plugin_data)
    print(f"plugin.json: initialized with {len(skills)} skills")
    summary = _ensure_global_symlinks_bulk(skills)
    if summary:
        print(f"~/.claude/skills/: {summary}")


def cmd_all(plugin_data):
    """Add all missing skills to plugin.json AND bulk-link ~/.claude/skills/."""
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
    print(f"plugin.json: added {len(added)}, skipped {len(skipped)}")
    # Always bulk-sync (cheap, idempotent, catches missing links).
    summary = _ensure_global_symlinks_bulk(skills)
    if summary:
        print(f"~/.claude/skills/: {summary}")


def cmd_refresh(plugin_data, clear_cache=False, sync_global=False):
    """Compare local skills vs Claude Code plugin cache. Optionally sync global symlinks and clear cache."""
    import os
    import shutil

    version_file = ROOT / "VERSION"
    local_version = version_file.read_text().strip() if version_file.exists() else "?"

    cache_root = Path.home() / ".claude" / "plugins" / "cache" / "zack-skills" / "zack-skills"
    if cache_root.exists():
        cache_versions = sorted([d.name for d in cache_root.iterdir() if d.is_dir()])
        local_skill_names = {p.parent.name for p in (ROOT / "skills").glob("**/SKILL.md")}
        cache_skill_names = {p.parent.name for p in cache_root.glob("*/skills/**/SKILL.md")}
    else:
        cache_versions = []
        local_skill_names = {p.parent.name for p in (ROOT / "skills").glob("**/SKILL.md")}
        cache_skill_names = set()

    added = sorted(local_skill_names - cache_skill_names)
    removed = sorted(cache_skill_names - local_skill_names)

    print("\n Plugin refresh\n")
    print(f"  Local VERSION : {local_version}")
    if cache_versions:
        print(f"  Cache VERSION : {', '.join(cache_versions)}")
    else:
        print("  Cache VERSION : (no cache)")
    if not added and not removed:
        print("  Skills        : in sync")
    else:
        if added:
            print(f"  ↗ New in local, missing in cache: {', '.join(added)}")
        if removed:
            print(f"  ↘ Removed locally, stale in cache: {', '.join(removed)}")

    if added or removed:
        print("\n Slash commands like /planning will fail until cache refreshes.")
        print(" Next steps:")
        print("   1. Push local to github (or set marketplace source to local)")
        print("   2. Run: /plugin install zack-skills")
        if not clear_cache:
            print("\n Re-run with --clear-cache to wipe cache and force re-fetch.")

    if clear_cache and cache_root.exists():
        for d in cache_root.iterdir():
            shutil.rmtree(d)
        print(f"\n Cache cleared: {cache_root}")
        print(" Next /plugin install zack-skills will re-fetch from source.")

    if sync_global:
        global_dir = Path.home() / ".claude" / "skills"
        if not global_dir.exists():
            print("\n Global skills dir not found, skipping: " + str(global_dir))
        else:
            actions_renamed = []
            actions_added = []
            actions_orphan = []

            def frontmatter_field(skill_md: Path, field: str):
                """Read a frontmatter scalar field. Returns None on miss."""
                try:
                    text = skill_md.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    return None
                if not text.startswith("---"):
                    return None
                for line in text.splitlines()[1:]:
                    if line.strip() == "---":
                        break
                    if line.startswith(field + ":"):
                        return line.split(":", 1)[1].strip().strip('"').strip("'")
                return None

            def frontmatter_name(skill_md: Path):
                return frontmatter_field(skill_md, "name")

            def frontmatter_description(skill_md: Path):
                return frontmatter_field(skill_md, "description")

            # Build map of local skills: frontmatter name -> path
            local_by_name = {}
            for skill_md in sorted((ROOT / "skills").glob("**/SKILL.md")):
                fname = frontmatter_name(skill_md)
                if fname:
                    local_by_name[fname] = skill_md.parent

            # 1) Walk existing symlinks; if target's `name` frontmatter exists in local → rename.
            #    Fallback: match by description (catches rename where upstream + local diverged).
            for entry in list(global_dir.iterdir()):
                if not entry.is_symlink():
                    continue
                try:
                    real = Path(os.path.realpath(entry))
                except OSError:
                    continue
                target_skill_md = real / "SKILL.md" if real.is_dir() else None
                if not target_skill_md or not target_skill_md.exists():
                    continue
                fname = frontmatter_name(target_skill_md)
                if not fname or fname not in local_by_name:
                    # Fallback: match by description
                    target_desc = frontmatter_description(target_skill_md)
                    if target_desc:
                        for local_name, local_dir in local_by_name.items():
                            if frontmatter_description(local_dir / "SKILL.md") == target_desc:
                                fname = local_name
                                break
                if not fname or fname not in local_by_name:
                    continue  # not one of ours
                if entry.name == fname:
                    continue  # already correct
                # Stale rename detected. Re-point to project copy under new name.
                new_target = str(local_by_name[fname].resolve())
                entry.unlink()
                os.symlink(new_target, global_dir / fname)
                actions_renamed.append(f"{entry.name} → {fname} (re-pointed to project)")

            # 2) Add symlinks for any local skill missing a global entry.
            #    Re-scan after step 1 — renamed entries now appear under their new name.
            present_names = {e.name for e in global_dir.iterdir()}
            for fname, skill_dir in local_by_name.items():
                if fname in present_names:
                    continue
                os.symlink(str(skill_dir.resolve()), global_dir / fname)
                actions_added.append(fname)

            # 3) Report orphans (symlinks whose target is gone and name isn't local).
            for entry in list(global_dir.iterdir()):
                if not entry.is_symlink():
                    continue
                if entry.name in local_by_name:
                    continue
                try:
                    real = Path(os.path.realpath(entry))
                except OSError:
                    actions_orphan.append(entry.name)
                    continue
                if not real.exists():
                    actions_orphan.append(entry.name)

            print("\n Global symlink sync (~/.claude/skills/):")
            if actions_renamed:
                print(f"  ↻ Renamed: {', '.join(actions_renamed)}")
            if actions_added:
                print(f"  + Added  : {', '.join(actions_added)}")
            if actions_orphan:
                print(f"  ? Orphan (target gone): {', '.join(actions_orphan)}")
            if not (actions_renamed or actions_added or actions_orphan):
                print("  (already in sync)")

    print()


def main():
    parser = argparse.ArgumentParser(prog="zack-skills")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List available skills")
    sub.add_parser("init", help="Initialize plugin.json with all skills")
    sub.add_parser("all", help="Add all missing skills (skips already-installed)")

    refresh_p = sub.add_parser("refresh", help="Diff local skills vs Claude Code plugin cache")
    refresh_p.add_argument("--clear-cache", action="store_true",
                            help="Wipe ~/.claude/plugins/cache/zack-skills/ to force re-fetch")
    refresh_p.add_argument("--sync-global", action="store_true",
                            help="Align ~/.claude/skills/ symlinks with local skill names")

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
    elif args.cmd == "refresh":
        cmd_refresh(plugin_data, clear_cache=args.clear_cache, sync_global=args.sync_global)


if __name__ == "__main__":
    main()

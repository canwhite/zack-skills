# CLI: `uv run cli.py` (Local Development Tool)

This doc covers `cli.py` — the local development tool for managing skills from your git clone.

**Not for end users.** This tool lives in the repo; end users installing via `npx` or `/plugin` don't need it.

---

## What It Is

`cli.py` is a Python project-local CLI. It manages two things:

1. **`.claude-plugin/plugin.json`** — the umbrella skill manifest (which skills are registered)
2. **`~/.claude/skills/<name>` symlinks** — point to your local `skills/` directory

It does NOT touch `~/.claude/plugins/cache/` (that's the plugin system's job).

---

## Source of Truth

The source of truth is the **`skills/` directory** in your local clone:

```
/Users/Admin/Desktop/zack-skills/           ← run cli.py from here
    skills/
        engineering/diagnose/SKILL.md
        engineering/planning/SKILL.md
        ...
    .claude-plugin/
        plugin.json                         ← generated from skills/
```

`load_skills()` scans `skills/**/*.md` and reads the `name:` field from each SKILL.md frontmatter. Everything flows from this scan.

---

## Commands

### `uv run cli.py list`

Scans `skills/` and prints every skill with install status (◆ = installed in `plugin.json`, ○ = not installed).

```
◆ diagnose    (installed)
○ improve-architecture
◆ planning    (installed)
```

### `uv run cli.py add <name>`

Adds a single skill to `plugin.json` AND creates the global symlink:

```python
# What happens internally (simplified):
skill_path = f"./skills/{category_path}"
plugin_data["skills"].append(skill_path)  # update manifest
save_plugin(plugin_data)                   # write .claude-plugin/plugin.json
_ensure_global_symlink(name, ROOT / "skills" / category_path)  # symlink to local
```

Example:
```bash
uv run cli.py add planning
# plugin.json: added planning
# ~/.claude/skills/planning: linked → /Users/Admin/Desktop/zack-skills/skills/engineering/planning
```

### `uv run cli.py remove <name>`

Removes from `plugin.json` AND removes the global symlink:

```python
plugin_data["skills"].remove(skill_path)
save_plugin(plugin_data)
_remove_global_symlink(name)  # removes ~/.claude/skills/<name>
```

### `uv run cli.py init`

Rebuilds `plugin.json` from scratch (scans all SKILL.md) + creates all symlinks:

```python
plugin_data = {
    "name": "zack-skills",
    "skills": sorted([f"./skills/{s['category_path']}" for s in skills])
}
save_plugin(plugin_data)
_ensure_global_symlinks_bulk(skills)  # symlink ALL skills
```

Use when: you added a new skill and want to register it everywhere at once.

### `uv run cli.py all`

Adds all missing skills to `plugin.json` (non-destructive) + bulk syncs symlinks:

```python
# Adds only skills not yet in plugin.json
# Then _ensure_global_symlinks_bulk(skills) — idempotent, safe to always run
```

### `uv run cli.py refresh`

Compares local `skills/` against the plugin cache (`~/.claude/plugins/cache/zack-skills/...`).

```
 Plugin refresh
  Local VERSION : 1.9.3
  Cache VERSION : 1.9.2
  ↗ New in local, missing in cache: improve-architecture
  Slash commands like /planning will fail until cache refreshes.
```

With `--sync-global`: also realigns `~/.claude/skills/` symlinks to match your local `skills/` (handles renames).

With `--clear-cache`: wipes `~/.claude/plugins/cache/zack-skills/` so next `/plugin install` re-copies from scratch.

### `uv run cli.py refresh --sync-global --clear-cache`

Full sync after local edits:

1. Compare local vs cache skill lists → report drift
2. Wipe plugin cache
3. Rename/add/remove `~/.claude/skills/` symlinks to match local `skills/` (uses frontmatter `name:` to detect renames)

---

## Symlink Logic

`_ensure_global_symlink(name, target_path)`:

```
~/.claude/skills/<name>
    │
    ├── symlink exists, target matches  → ok (no-op)
    ├── symlink exists, target differs  → repoint (replace with new target)
    ├── real file exists (not symlink)  → blocked (refuse to clobber)
    └── nothing exists                  → created
```

Idempotent: safe to run multiple times.

The `refresh --sync-global` variant also detects **renames** by reading the `name:` frontmatter field from the symlink target's SKILL.md and comparing against the symlink name.

---

## Plugin.json vs Symlinks

| File | Purpose | Managed by |
|---|---|---|
| `.claude-plugin/plugin.json` | Umbrella manifest: which skill paths are registered | `cli.py add/remove/init/all` |
| `~/.claude/skills/<name>` | Per-skill symlink: how `/<name>` resolves | `cli.py add/remove/init/all/refresh --sync-global` |

Both stay in sync automatically after `add`/`remove`. `init` and `all` rebuild both from the `skills/` scan.

---

## How It Fits With the Other Paths

```
Local clone (cli.py manages)
    ↓  push to GitHub
GitHub repo
    ↓  marketplace update + plugin install
Plugin cache (managed by Claude Code, NOT cli.py)
```

`cli.py` never touches the plugin cache. It only manages your local clone's `plugin.json` and `~/.claude/skills/` symlinks.

Use `cli.py` when developing skills locally. When done, push → `marketplace update` → `plugin install` to propagate.

---

## Common Workflows

### Start developing a skill locally
```bash
# Edit skills/engineering/improve-architecture/SKILL.md
uv run cli.py add improve-architecture   # register + link
/diagnose                               # test immediately (slash resolves via symlink)
```

### Add a new skill
```bash
# Create skills/engineering/new-skill/SKILL.md
uv run cli.py init                       # register all + link all at once
```

### Push local changes to GitHub
```bash
git add . && git commit -m "feat: add new-skill"
git push
# Then on any machine:
/plugin marketplace update zack-skills
/plugin install zack-skills
```

### Sync after renaming a skill
```bash
# Renamed improve-codebase-architecture → improve-architecture
uv run cli.py refresh --sync-global
# ↻ Renamed: improve-codebase-architecture → improve-architecture (re-pointed to project)
```

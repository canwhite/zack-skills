# Install Paths: Three Independent Mechanisms

Three ways to make `/diagnose`, `/planning`, `/caveman` etc. available to Claude Code. **They are completely independent — pick one, don't mix.**

---

## Quick Reference

| Path | Source | Link/Copy | Global? | Use when |
|---|---|---|---|---|
| `npx skills add -g` | GitHub bundle | symlink | yes | want all skills, auto-update on reinstall |
| `/plugin install` | GitHub bundle | **physical copy** | yes | want selective skills, stable across pushes |
| `uv run cli.py add` | **local project** | symlink | yes | developing skills locally |

---

## Path 1: `npx skills add -g` (skills-cli, npm)

### Mechanism

```
GitHub repo
    ↓  npx download (tarball)
~/.claude/skills/zack-skills/          ← bundle root (real dir)
    skills/
        engineering/diagnose/SKILL.md
        engineering/planning/SKILL.md
        ...
    setup.sh                           ← auto-run post-install
```

`setup.sh` runs automatically after `npx` downloads the bundle. It delegates to `scripts/link-skills.sh`.

### Core Code

**`setup.sh`** (root, what npx auto-runs):
```bash
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
exec bash "$HERE/scripts/link-skills.sh"
```

**`scripts/link-skills.sh`** (idempotent, scans bundle → creates symlinks):
```bash
REPO="$HERE"               # bundle root, e.g. ~/.claude/skills/zack-skills
SKILLS_DIR="$REPO/skills"

for skill_md in $(find "$SKILLS_DIR" -name SKILL.md); do
  name=$(grep '^name:' "$skill_md" | cut -d: -f2 | tr -d ' ')
  target="$HOME/.claude/skills/$name"

  if [ -L "$target" ]; then
    current_target="$(readlink "$target")"
    # resolve to absolute for comparison
    ...
    if [ "$current_real" = "$src_real" ]; then
      echo "ok     $name (already linked)"
      continue
    fi
    echo "kept   $name (existing target: $current_target; not overwriting local-dev)"
    continue
  fi
  [ -f "$target" ] && echo "kept  $name (real file exists, not overwriting)" && continue
  ln -sfn "$src" "$target"
  echo "linked $name → $src"
done
```

**Result**: `~/.claude/skills/diagnose` → symlink to bundle's diagnose dir.

### Properties

- Reinstall with `npx skills add -g -f` → re-runs `setup.sh` → symlinks refresh
- Bundle updates: `npx skills add -g -f` redownloads, symlinks re-created
- Local development: if `~/.claude/skills/diagnose` already exists as a local-dev symlink (pointing to your project), it's **preserved** (not overwritten)

---

## Path 2: `/plugin install` (Claude Code plugin system)

### Mechanism

```
GitHub repo
    ↓  /plugin marketplace add (one-time git clone)
~/.claude/plugins/marketplaces/zack-skills/   ← live git clone, .git/ intact

    ↓  /plugin install zack-<skill>
~/.claude/plugins/cache/zack-skills/<plugin-name>/<version>/   ← physical copy (no .git/)
    SKILL.md
    scripts/
```

**No symlinks anywhere.** The plugin system copies files and registers slash commands from the manifest.

### Key Insight: Two-Level Structure

```
~/.claude/plugins/
    marketplaces/   ← live git clone, source of truth for updates
    cache/         ← "installed" copy, what plugin runtime reads
```

- `marketplace add` → `git clone` into `marketplaces/`
- `marketplace update` → `git pull` in `marketplaces/`
- `plugin install` → **physical copy** (stripping `.git/`) from marketplace clone into `cache/`
- `plugin uninstall` → delete `cache/` entry + deregister slash command

### Manifest-Driven Registration

The cache contains a manifest that tells Claude Code which slash commands exist:

**`.claude-plugin/plugin.json`** (in cache root):
```json
{
  "name": "zack-skills",
  "skills": [
    "./skills/engineering/diagnose",
    "./skills/engineering/planning",
    "./skills/engineering/pre-mortem",
    ...
  ]
}
```

The plugin system reads this manifest, **not** the filesystem, to discover slash commands. Skills not listed here are not registered even if their SKILL.md exists on disk.

### Umbrella vs Per-Skill

| Command | Cache location | Skills registered |
|---|---|---|
| `/plugin install zack-skills` | `cache/zack-skills/zack-skills/<v>/` | All 10 (via `plugin.json`) |
| `/plugin install zack-diagnose` | `cache/zack-skills/zack-diagnose/<v>/` | `/diagnose` only |

**Umbrella** copies the whole repo; slash command list comes from `plugin.json`.

**Per-skill** copies only that skill's subdirectory; slash command is inferred from the single SKILL.md.

### Source vs Marketplace.json

In `marketplace.json` at the repo root:
```json
{
  "plugins": [
    {
      "name": "zack-skills",
      "source": "./",                    ← whole repo
      "skills": ["./"]                   ← all skills
    },
    {
      "name": "zack-diagnose",
      "source": "./skills/engineering/diagnose",
      "skills": ["./"]
    }
  ]
}
```

The `source` field tells `plugin install` **what to copy**. The `skills` array tells it **which slash commands to register**.

---

## Path 3: `uv run cli.py add` (local development)

### Mechanism

```
/Users/Admin/Desktop/zack-skills/           ← your local clone (git repo)
    skills/
        engineering/diagnose/SKILL.md
        engineering/planning/SKILL.md
        ...

~/.claude/skills/diagnose  →  symlink to /Users/Admin/Desktop/zack-skills/skills/engineering/diagnose
~/.claude/skills/planning  →  symlink to /Users/Admin/Desktop/zack-skills/skills/engineering/planning
```

Unlike the other two paths, **the source is your local project**, not GitHub.

### Core Code

**`cli.py` `cmd_add`** (simplified):
```python
def cmd_add(name, sync_global=False):
    skill_entry = find_skill(name)          # locate SKILL.md by name field
    src = ROOT / "skills" / skill_entry["category_path"]   # e.g. skills/engineering/diagnose
    dest = Path.home() / ".claude" / "skills" / name       # ~/.claude/skills/diagnose

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.is_symlink() or dest.exists():
        dest.unlink()                      # remove old link
    dest.symlink_to(src)                   # create new symlink
    print(f"linked {name} → {src}")
```

**Key difference from `setup.sh`**: `cli.py` resolves skills by scanning `plugin.json` (which was built from `skills/`), then creates symlinks. `setup.sh` scans the filesystem directly.

### Refresh After Local Edits

```bash
uv run cli.py refresh --sync-global --clear-cache
```

1. `clear_cache`: wipe `~/.claude/plugins/cache/zack-skills/` → forces `/plugin install` to re-copy
2. `sync_global`: realign `~/.claude/skills/` symlinks to match local `skills/` directory
3. Bump `VERSION` → `marketplace update` sees new version on next pull

### When to Use

- **Developing skills locally**: edit `skills/engineering/diagnose/SKILL.md`, immediately test `/diagnose`
- **Pushing updates**: push to GitHub, then run `marketplace update` + `plugin install` to propagate
- **Not for end users**: ordinary users should use `npx skills add` or `/plugin install`

---

## Why Three Paths?

| Concern | skills-cli (npm) | plugin system | cli.py (local) |
|---|---|---|---|
| Updates | Reinstall to update | `marketplace update` + `plugin install` | Edit locally, no install needed |
| Selective install | All or nothing (via setup.sh) | Per-skill granular | Per-skill granular |
| Skill development | Poor (symlinks to bundle) | Poor (copies bundle) | **Ideal** (symlinks to source) |
| Stability | Bundle can change between runs | Cache is frozen at install version | Source is live |
| Auto-link on install | Yes (`setup.sh`) | No (plugin copies, no symlinks) | Manual per command |

**Recommendation**:
- End users: `npx skills add -g` (all skills) or `/plugin install zack-caveman` (selective)
- Local development: `uv run cli.py add` + push + `marketplace update` + `plugin install`

---

## Uninstall

| Path | How |
|---|---|
| skills-cli | `rm -rf ~/.claude/skills/zack-skills` |
| plugin | `/plugin uninstall zack-<skill>` (per-skill) or `/plugin uninstall zack-skills` (umbrella) |
| cli.py | manual: `rm ~/.claude/skills/<name>` (symlinks only, no bundle removal) |

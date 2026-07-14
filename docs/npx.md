# `npx skills add`: skills-cli Install Path

This covers the `npx skills add -g` install path — the recommended way for end users to install all skills.

---

## What It Does

```
GitHub repo (tarball download)
    ↓
~/.claude/skills/zack-skills/           ← bundle root (real directory)
    ├── skills/
    │   ├── engineering/{diagnose, planning, ...}/
    │   └── productivity/{caveman, markdown-to-itmz}/
    ├── setup.sh                         ← auto-run post-install
    ├── scripts/link-skills.sh           ← creates ~/.claude/skills/<name> symlinks
    └── ...
```

Then `setup.sh` runs automatically, creating per-skill symlinks:

```
~/.claude/skills/diagnose  →  ~/.claude/skills/zack-skills/skills/engineering/diagnose
~/.claude/skills/planning  →  ~/.claude/skills/zack-skills/skills/engineering/planning
~/.claude/skills/caveman   →  ~/.claude/skills/zack-skills/skills/productivity/caveman
...
```

---

## How `npx` Triggers `setup.sh`

The `skills-cli` tool (from `@vercel-labs/skills`) auto-runs a setup script after install. It looks for one of:

- `setup.sh`
- `setup.py`
- `install.sh`
- `install.py`

at the **root** of the installed package. If found, it executes it.

`zack-skills/setup.sh` is that hook:

```bash
#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
exec bash "$HERE/scripts/link-skills.sh"
```

---

## `link-skills.sh`: The Core Logic

Scans `skills/**/*.md` in the bundle → reads `name:` from each SKILL.md frontmatter → creates symlinks in `~/.claude/skills/`.

```bash
for skill_md in $(find "$SKILLS_DIR" -name SKILL.md); do
  name=$(grep '^name:' "$skill_md" | cut -d: -f2 | tr -d ' ')
  target="$HOME/.claude/skills/$name"
  src=$(cd "$(dirname "$skill_md")" && pwd)

  if [ -L "$target" ]; then
    current_target="$(readlink "$target")"
    current_real="$(cd "$(dirname "$target")" && cd "$(dirname "$current_target")" && pwd)/$(basename "$current_target")"
    if [ "$current_real" = "$src_real" ]; then
      echo "ok     $name (already linked)"
      continue          # ← idempotent: same target, skip
    fi
    echo "kept   $name (existing target: $current_target; not overwriting local-dev)"
    continue            # ← preserve local-dev symlinks
  fi
  [ -f "$target" ] && echo "kept  $name (real file exists)" && continue
  ln -sfn "$src" "$target"
  echo "linked $name → $src"
done
```

**Output branches**:

| Condition | Action | Output |
|---|---|---|
| Symlink exists, same target | Skip | `ok` |
| Symlink exists, different target | Skip | `kept` (preserves local-dev) |
| Real file exists | Skip | `kept` |
| Nothing exists | Create | `linked` |

---

## Idempotency

Running `npx skills add -g -f` (force reinstall) re-runs `setup.sh`. The idempotent logic means:

- **Same target**: `ok` — no change
- **Different target** (e.g. local dev symlink to your project): `kept` — your local symlink is preserved
- **Only `linked` when truly new**

---

## Uninstall

```bash
rm -rf ~/.claude/skills/zack-skills
```

This removes both the bundle and all per-skill symlinks created by `setup.sh`.

---

## vs `/plugin install`

| | `npx skills add -g` | `/plugin install` |
|---|---|---|
| Installs | Whole bundle | Whole bundle or per-skill |
| Symlinks | `~/.claude/skills/<name>` (via `setup.sh`) | None — direct file copy |
| Updates | Reinstall (`-f`) redownloads + re-links | `marketplace update` + `plugin install` |
| Per-skill selective | Not supported (all or nothing) | Supported |
| Skill source | Bundle (can lag behind repo) | Marketplace clone (can `marketplace update`) |

---

## Why Not `/plugin install`?

`npx skills add` is recommended for most users because:

1. **Simpler**: one command, no marketplace setup
2. **Auto-symlink**: `setup.sh` creates `~/.claude/skills/<name>` links automatically
3. **Familiar**: standard npm/npx ecosystem

Trade-offs: no per-skill selective install, and updates require force-reinstall vs `marketplace update`.

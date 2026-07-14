# Claude Code Plugin System: How `/plugin install` Works

This documents the mechanics of the Claude Code plugin system as it applies to `zack-skills`.

---

## Architecture: Two-Level Storage

```
~/.claude/plugins/
├── marketplaces/                      # live git clones (source of truth)
│   └── zack-skills/                   # git clone from GitHub
│       ├── .git/
│       ├── skills/                    # source files
│       ├── plugins/
│       └── .claude-plugin/
│           └── plugin.json            # skill manifest
│
├── cache/                            # "installed" copies (what runtime uses)
│   └── zack-skills/
│       ├── zack-skills/1.9.2/        # umbrella: whole repo
│       │   ├── skills/               # ← copied from marketplaces/
│       │   └── .claude-plugin/
│       │       └── plugin.json       # ← copied from marketplaces/
│       └── zack-diagnose/1.9.2/      # per-skill: single skill subtree
│           ├── SKILL.md
│           └── scripts/
│
└── installed_plugins.json             # registry: what plugins are "installed"
```

**Key principle**: `marketplaces/` is a live git clone. `cache/` is a static copy with `.git/` stripped.

---

## Command Flow

### 1. `/plugin marketplace add zack-skills`

```bash
# What runs internally:
git clone https://github.com/canwhite/zack-skills \
  ~/.claude/plugins/marketplaces/zack-skills/
```

- One-time operation. Registers the marketplace so Claude Code knows where to find it.
- The clone has `.git/` intact — can `git pull` to update.
- Result: `~/.claude/plugins/marketplaces/zack-skills/` exists with full repo contents.

### 2. `/plugin marketplace update zack-skills`

```bash
# What runs internally:
cd ~/.claude/plugins/marketplaces/zack-skills/
git pull
```

- Refreshes the marketplace clone to the latest commit on the remote.
- **Must run after pushing new commits** — otherwise `plugin install` pulls the old version.
- Does NOT touch `cache/`.

### 3. `/plugin install zack-<skill>`

```bash
# What runs internally (per-skill, e.g. zack-diagnose):
cp -r ~/.claude/plugins/marketplaces/zack-skills/skills/engineering/diagnose \
      ~/.claude/plugins/cache/zack-skills/zack-diagnose/1.9.2/
```

```bash
# What runs internally (umbrella, zack-skills):
cp -r ~/.claude/plugins/marketplaces/zack-skills/ \
      ~/.claude/plugins/cache/zack-skills/zack-skills/1.9.2/
# Then strip .git/
rm -rf ~/.claude/plugins/cache/zack-skills/zack-skills/1.9.2/.git
```

- **Physical copy** — files are duplicated, not symlinked.
- Strips `.git/` directory (not needed at runtime, reduces size).
- Version determined by `VERSION` file in marketplace clone at install time.
- Writes entry to `~/.claude/plugins/installed_plugins.json`.

### 4. Runtime: Slash Command Registration

Claude Code reads `cache/` on startup (or when plugin is first referenced). For each plugin:

1. Reads `plugin.json` (or infers from single `SKILL.md` for per-skill installs).
2. Extracts `skills[]` array — these are the registered slash commands.
3. Makes slash commands available globally (user scope = all projects).

**The `skills[]` array is the source of truth for what slash commands exist.** A SKILL.md file on disk but not listed in `skills[]` will NOT be registered as a slash command.

### 5. `/plugin uninstall zack-<skill>`

```bash
rm -rf ~/.claude/plugins/cache/zack-skills/zack-diagnose/
# Also removes from installed_plugins.json
```

- Only deletes from `cache/`.
- Does NOT touch `marketplaces/`.
- Slash command deregistered globally.

---

## Umbrella vs Per-Skill

When you install `zack-skills` (umbrella, source=`./`):

```
cache/zack-skills/zack-skills/1.9.2/
├── .claude-plugin/plugin.json   ← lists ALL 9 skills
├── skills/
│   ├── engineering/{diagnose, planning, ...}
│   └── productivity/{caveman, markdown-to-itmz}
└── ...
```

When you install `zack-diagnose` (per-skill, source=`./skills/engineering/diagnose`):

```
cache/zack-skills/zack-diagnose/1.9.2/
├── SKILL.md                     ← only this skill
└── scripts/
    └── check-update.sh
```

Slash command registration is driven by `skills[]` in `plugin.json`, not by scanning the filesystem.

---

## `marketplace.json`: The Plugin Catalog

Located at the repo root, this file defines what plugins the marketplace offers:

```json
{
  "plugins": [
    {
      "name": "zack-skills",          // ← npm-style name
      "source": "./",                  // what to copy (relative to repo root)
      "skills": ["./"]                 // what to register (./ = all from plugin.json)
    },
    {
      "name": "zack-diagnose",
      "source": "./skills/engineering/diagnose",
      "skills": ["."]
    }
  ]
}
```

`source` tells `plugin install` **what subtree to copy**.
`skills` tells it **which slash commands to register**.

---

## Versioning and Cache Invalidation

Plugin versions come from the `VERSION` file at the repo root.

- Each `plugin install` stamps the current `VERSION` into the cache path.
- Re-running `plugin install` with the same version does **nothing** (cache already exists).
- To force reinstall: `marketplace update` first (pulls new VERSION), then `plugin install` again.

Installed version is visible in `~/.claude/plugins/installed_plugins.json`:

```json
"zack-skills@zack-skills": {
  "version": "1.9.2",
  "installPath": "/Users/Admin/.claude/plugins/cache/zack-skills/zack-skills/1.9.2"
}
```

---

## `installed_plugins.json`: The Registry

```json
{
  "plugins": {
    "zack-skills@zack-skills": [{
      "scope": "user",
      "installPath": "~/.claude/plugins/cache/zack-skills/zack-skills/1.9.2",
      "version": "1.9.2",
      "gitCommitSha": "f8109f7..."
    }]
  }
}
```

- `scope: "user"` means global across all projects.
- `installPath` points to cache, not marketplace.
- `gitCommitSha` pins to a specific commit.

---

## Key Takeaways

1. **No symlinks in plugin path.** Everything is physical copy.
2. **`~/.claude/skills/` is irrelevant to the plugin system.** That directory is only for `skills-cli` (`npx`).
3. **Slash commands come from `skills[]` in `plugin.json`, not filesystem scan.**
4. **`marketplace update` is required after pushing new commits** — it does NOT auto-pull.
5. **Cache and marketplace are independent.** Cache is a static snapshot; marketplace is a live clone.
6. **Uninstall only touches cache** — marketplace clone remains.

---

## Common Workflows

### Fresh install (one-time)
```bash
/plugin marketplace add zack-skills
/plugin marketplace update zack-skills
/plugin install zack-skills         # umbrella: all 9 skills
```

### Update after pushing new commits
```bash
/plugin marketplace update zack-skills
/plugin install zack-skills         # re-copies with new version
```

### Per-skill selective install
```bash
/plugin install zack-caveman
/plugin install zack-diagnose
# only /caveman and /diagnose available
```

### Uninstall
```bash
/plugin uninstall zack-skills       # removes umbrella
/plugin uninstall zack-caveman      # removes just caveman
```

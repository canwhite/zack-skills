# Zack Skills

A toolkit of engineering workflow skills for Claude Code: pre-mortem, post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, and markdown-to-mind-map. Each skill is a Markdown workflow with frontmatter-driven dispatch; one `VERSION` file is the single source of truth for all generated artifacts (marketplace metadata, npm package, Codex mirror, dispatcher table, per-skill update check).

## Skills

| Skill | Description |
|-------|-------------|
| `caveman` | Ultra-compressed communication mode. |
| `diagnose` | Disciplined diagnosis loop for hard bugs and performance regressions. |
| `improve-architecture` | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. |
| `markdown-to-itmz` | Generate an iThoughts (.itmz) mind map from any Markdown file. |
| `planning` | Plan a task, feature, or change by clarifying the question, writing a structured plan markdown to docs/, and recommending a follow-up pre-mortem. |
| `post-mortem` | Post-mortem analysis with diagnose capabilities. |
| `pre-mortem` | Pre-mortem analysis that updates a plan markdown inline with all risks and mitigations. |
| `rice` | RICE prioritization framework for scoring and ranking tasks. |
| `setup-zack-skills` | Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitHub or local markdown), triage label vocabulary, and domain doc layout. |
| `zoom-out` | Tell the agent to zoom out and give broader context or a higher-level perspective. |

## Install

### Via skills-cli (recommended)

```bash
npx skills add https://github.com/canwhite/zack-skills -g
```

### Claude Code plugin

```bash
/plugin marketplace add zack-skills             # tell Claude Code where to find the skill catalog (one-time)
/plugin marketplace update zack-skills          # re-pull the catalog after pushing new commits
/plugin install zack-<skill>                    # install per-skill, e.g. zack-caveman
```

Available per-skill plugins: `zack-caveman`, `zack-diagnose`, `zack-improve-architecture`,
`zack-markdown-to-itmz`, `zack-planning`, `zack-post-mortem`, `zack-pre-mortem`,
`zack-rice`, `zack-setup-zack-skills`, `zack-zoom-out`.

Pick only what you need. The marketplace also exposes an umbrella `zack-skills` that
loads everything at once — prefer the per-skill installs above.

> Have multiple marketplaces registered? Use `zack-<skill>@zack-skills` to disambiguate.

## Uninstall

### Plugin (Claude Code)

```bash
/plugin uninstall zack-<skill>                  # uninstall per-skill
```

### skills-cli (npm)

```bash
rm -rf ~/.claude/skills/zack-skills              # removes bundle + symlinks created by setup.sh
```

## CLI (managing your local copy)

The repo ships `cli.py` for keeping `marketplace.json`, `plugin.json`, VERSION,
and `~/.claude/skills/` symlinks aligned with whatever is in `skills/`. The
CLI is project-local — it always runs from the repo root, so it knows which
skills exist before any slash command does.

### Requirements

- [`uv`](https://docs.astral.sh/uv/) (>= 0.11). On macOS: `brew install uv`.

### Common commands

```bash
uv run cli.py list                 # show all available skills + install state
uv run cli.py init                 # rebuild .claude-plugin/plugin.json from scratch
uv run cli.py all                  # add any missing skills to plugin.json
uv run cli.py add <name>           # install a single skill
uv run cli.py remove <name>        # uninstall a single skill
uv run cli.py refresh              # diff local skills vs Claude Code plugin cache
uv run cli.py refresh --sync-global   # also realign ~/.claude/skills/ symlinks
uv run cli.py refresh --clear-cache   # wipe ~/.claude/plugins/cache/zack-skills/
```

### Sync workflow after editing skills

Whenever you rename, add, or remove a skill in `skills/`, run:

```bash
uv run cli.py refresh --sync-global --clear-cache
```

This:

1. Bumps VERSION (forces marketplace re-fetch on next `/plugin install`).
2. Renames / adds / prunes `~/.claude/skills/` symlinks so slash commands
   (`/planning`, `/improve-architecture`, etc.) stay addressable.
3. Wipes `~/.claude/plugins/cache/zack-skills/` so the next
   `/plugin install zack-skills` rebuilds the cache from your local skills.

Then push to GitHub (or point the marketplace source at the local path) and
re-run `/plugin install zack-skills` to re-fetch.

### Plain Python (no uv)

```bash
python3 cli.py list
```

Works identically. `uv run` only adds dependency resolution + faster cold-start.

## Development

```bash
make test              # verify frontmatter + scripts + drift
make regenerate        # rebuild all generated artifacts
make verify-generated  # CI: fail if generated files drift from source
```

See [`docs/zoom-out.md`](docs/zoom-out.md) for the architecture reference (modules, dispatch flow, packaging model).

## License

MIT

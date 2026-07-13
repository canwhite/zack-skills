# Zack Skills

A toolkit of engineering workflow skills for Claude Code: code review, agent health audits, pre-mortem, post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, and markdown-to-mind-map. Each skill is a Markdown workflow with frontmatter-driven dispatch; one `VERSION` file is the single source of truth for all generated artifacts (marketplace metadata, npm package, Codex mirror, dispatcher table, per-skill update check).

## Skills

| Skill | Description |
|-------|-------------|
| `caveman` | Ultra-compressed communication mode. |
| `check` | Reviews code diffs, PRs, commits, and project audits. |
| `diagnose` | Disciplined diagnosis loop for hard bugs and performance regressions. |
| `health` | Runs an engineering health audit for instruction drift, hooks, MCP tool drift, and AI maintainability. |
| `markdown-to-itmz` | Generate an iThoughts (.itmz) mind map from any Markdown file. |
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
/plugin marketplace add zack-skills
/plugin install zack-skills@zack-skills
```

### Via CLI (local clone)

Clone the repo and run `cli.py` directly:

```bash
git clone https://github.com/canwhite/zack-skills.git
cd zack-skills

python3 cli.py list                  # List available skills
python3 cli.py init                  # Initialize plugin.json with all skills
python3 cli.py add <skill>           # Add a skill
python3 cli.py remove <skill>        # Remove a skill
```

## Uninstall

```bash
rm -rf ~/.claude/skills/zack-skills
```

## Development

```bash
make test              # verify frontmatter + scripts + drift
make regenerate        # rebuild all generated artifacts
make verify-generated  # CI: fail if generated files drift from source
```

See [`docs/zoom-out.md`](docs/zoom-out.md) for the architecture reference (modules, dispatch flow, packaging model).

## License

MIT

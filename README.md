# Zack Skills

Engineering skills for Claude Code: code review, agent health audits, pre-mortem, post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, and markdown to mind map.

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

## Uninstall

```bash
rm -rf ~/.claude/skills/zack-skills
```

# Zack Skills

Engineering skills for Claude Code: code review, agent health audits, pre-mortem, post-mortem, diagnose, zoom-out, and caveman compression.

## Skills

| Skill | When | What it does |
| :--- | :--- | :--- |
| `/check` | After a task, before merging | Reviews diffs, checks type safety, error handling, JSDoc, and project quality. |
| `/health` | Auditing agent configuration | Checks CLAUDE.md drift, hooks, MCP tools, and AI maintainability. |
| `pre-mortem` | Before starting | Anticipate failures and plan mitigations. |
| `post-mortem` | After completing work | Review work, find logic errors and gaps. |
| `diagnose` | When something is broken | Reproduce → minimise → hypothesise → instrument → fix → regression-test. |
| `zoom-out` | Exploring codebase | Understand architecture, map modules and relationships. |
| `caveman` | Any time | Ultra-compressed communication — drop filler, keep technical accuracy. |
| `markdown-to-itmz` | Converting markdown | Generate iThoughts mind map from Markdown. |
| `rice` | Ranking tasks | Score and rank tasks by RICE framework. |

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

# Zack Skills

Engineering skills for Claude Code: pre-mortem, post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, and markdown-to-mind-map.

## Skills

| Skill | When | What it does |
| :--- | :--- | :--- |
| `pre-mortem` | Before starting | Anticipate failures and plan mitigations. |
| `planning` | Starting a new task/feature | Clarify intent, then write a structured plan markdown to `docs/` following Plan / Think / Do / Adjust. |
| `post-mortem` | After completing work | Review work, find logic errors and gaps. |
| `diagnose` | When something is broken | Reproduce → minimise → hypothesise → instrument → fix → regression-test. |
| `zoom-out` | Exploring codebase | Understand architecture, map modules and relationships. |
| `caveman` | Any time | Ultra-compressed communication — drop filler, keep technical accuracy. |
| `markdown-to-itmz` | Converting markdown | Generate iThoughts mind map from Markdown. |
| `rice` | Ranking tasks | Score and rank tasks by RICE framework. |
| `setup-zack-skills` | First-time repo setup | Wires issue tracker, triage labels, and domain docs into AGENTS.md/CLAUDE.md so other skills have repo context. Run once before `/diagnose`, `/zoom-out`, or any triage skill. |

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

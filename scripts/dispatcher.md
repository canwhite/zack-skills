# Zack Skills Dispatcher

🥷 Zack — engineering skill toolkit for Claude Code.

## Available Skills

| Skill | Description |
|-------|-------------|
| check | Code review for diffs, PRs, commits, and project audits |
| health | Agent health audit for configuration drift and AI maintainability |
| pre-mortem | Anticipate failures before starting |
| post-mortem | Review completed work, find logic errors |
| diagnose | Reproduce → minimise → hypothesise → instrument → fix → regression-test |
| zoom-out | Explore codebase, understand architecture |
| caveman | Ultra-compressed communication mode |
| markdown-to-itmz | Convert Markdown to iThoughts mind map |
| rice | RICE prioritization for scoring and ranking tasks |
| setup-zack-skills | First-time repo setup: wires issue tracker, triage labels, and domain docs into AGENTS.md |

## Routing Table

<!-- routing-table:start -->
| Intent | Skill | File |
|--------|-------|------|
|  | caveman | `skills/productivity/caveman/SKILL.md` |
| Code review, before merge, release gates, safety sinks, project-wide audit scorecard | check | `skills/engineering/check/SKILL.md` |
|  | diagnose | `skills/engineering/diagnose/SKILL.md` |
| Agent configuration audit, instruction drift detection, hooks/MCP verification, AI maintainability scorecard | health | `skills/engineering/health/SKILL.md` |
|  | markdown-to-itmz | `skills/productivity/markdown-to-itmz/SKILL.md` |
|  | post-mortem | `skills/engineering/post-mortem/SKILL.md` |
|  | pre-mortem | `skills/engineering/pre-mortem/SKILL.md` |
|  | rice | `skills/engineering/rice/SKILL.md` |
|  | setup-zack-skills | `skills/engineering/setup-zack-skills/SKILL.md` |
|  | zoom-out | `skills/engineering/zoom-out/SKILL.md` |
<!-- routing-table:end -->

## Output Convention

All skills prefix the first line inline with 🥷.

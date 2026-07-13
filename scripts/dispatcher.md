# Harness Skills Dispatcher

🥷 Harness — engineering skill toolkit for Claude Code.

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

## Routing Table

<!-- routing-table:start -->
| Intent | Skill | File |
|--------|-------|------|
|  | caveman | `skills/caveman/SKILL.md` |
| Code review, before merge, release gates, safety sinks, project-wide audit scorecard | check | `skills/check/SKILL.md` |
|  | diagnose | `skills/diagnose/SKILL.md` |
| Agent configuration audit, instruction drift detection, hooks/MCP verification, AI maintainability scorecard | health | `skills/health/SKILL.md` |
|  | markdown-to-itmz | `skills/markdown-to-itmz/SKILL.md` |
|  | post-mortem | `skills/post-mortem/SKILL.md` |
|  | pre-mortem | `skills/pre-mortem/SKILL.md` |
|  | rice | `skills/rice/SKILL.md` |
|  | setup-zack-skills | `skills/setup-zack-skills/SKILL.md` |
|  | zoom-out | `skills/zoom-out/SKILL.md` |
<!-- routing-table:end -->

## Output Convention

All skills prefix the first line inline with 🥷.

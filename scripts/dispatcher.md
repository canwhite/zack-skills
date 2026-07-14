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

## Routing Table

<!-- routing-table:start -->
| Intent | Skill | File |
|--------|-------|------|
|  | caveman | `skills/productivity/caveman/SKILL.md` |
|  | diagnose | `skills/engineering/diagnose/SKILL.md` |
| Find refactor opportunities that turn shallow modules into deep ones; report candidates with files, problem, solution, benefits; ask user which to explore before proposing interfaces. | improve-architecture | `skills/engineering/improve-architecture/SKILL.md` |
|  | markdown-to-itmz | `skills/productivity/markdown-to-itmz/SKILL.md` |
| Interactive planning: clarify intent, write plan to docs/ following Plan/Think/Do/Adjust structure, then recommend pre-mortem | planning | `skills/engineering/planning/SKILL.md` |
|  | post-mortem | `skills/engineering/post-mortem/SKILL.md` |
|  | pre-mortem | `skills/engineering/pre-mortem/SKILL.md` |
|  | rice | `skills/engineering/rice/SKILL.md` |
|  | zoom-out | `skills/engineering/zoom-out/SKILL.md` |
<!-- routing-table:end -->

## Output Convention

All skills prefix the first line inline with 🥷.

# Zack Skill Resolver

## Shared Output Marker

All skills prefix the first line inline with `🥷`, not as its own paragraph.

## Skill Routing Table

| Trigger | Skill |
|---------|-------|
| Pre-mortem / anticipate failures / risk planning | `skills/engineering/pre-mortem/SKILL.md` |
| Planning / design / how to build / propose a solution | `skills/engineering/planning/SKILL.md` |
| Post-mortem / review completed work / find errors | `skills/engineering/post-mortem/SKILL.md` |
| Diagnose / debug / reproduce root cause | `skills/engineering/diagnose/SKILL.md` |
| Zoom-out / explore codebase / architecture | `skills/engineering/zoom-out/SKILL.md` |
| Improve architecture / deepen modules / refactor for testability | `skills/engineering/improve-architecture/SKILL.md` |
| Caveman / compressed communication / brief | `skills/productivity/caveman/SKILL.md` |
| markdown-to-itmz / convert markdown to mind map | `skills/productivity/markdown-to-itmz/SKILL.md` |
| rice / RICE prioritization / score tasks | `skills/engineering/rice/SKILL.md` |
| Bootstrap / first-run / setup issue tracker and triage labels | `skills/engineering/setup-zack-skills/SKILL.md` |

## Disambiguation

1. **Planning flow**: ambiguous request → `/planning` writes plan → `/pre-mortem` hardens it → `/post-mortem` after execution
2. **Pre-build vs post-build**: new features, planning → `/pre-mortem`; implementation done → `/post-mortem`
3. **Meta skills**: pre-mortem, post-mortem, diagnose, zoom-out, improve-architecture, caveman — invoked directly by name
4. **Zoom-out vs improve-architecture**: explain how the code fits → `/zoom-out`; refactor a module to be deeper/more testable → `/improve-architecture`

## Chaining

- `/setup-zack-skills` (once) → other skills gain repo context
- `/planning` → writes plan to `docs/plan-<slug>.md` → `/pre-mortem <plan-file>` → ready to implement
- `/pre-mortem` done → ready to implement

## Project Context

Apply skill to current project: read README, CI config, package.json, and git status before acting.
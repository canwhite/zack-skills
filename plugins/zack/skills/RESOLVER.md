# Zack Skill Resolver

## Shared Output Marker

All skills prefix the first line inline with `🥷`, not as its own paragraph.

## Skill Routing Table

| Trigger | Skill |
|---------|-------|
| Code review / PR review / diff review / "review this" / "check this code" / merge gate / pre-merge | `skills/engineering/check/SKILL.md` |
| Project audit / scorecard / quality check / health check | `skills/engineering/check/SKILL.md` |
| Audit agent config / CLAUDE.md drift / hooks / MCP / instruction drift / AI maintainability | `skills/engineering/health/SKILL.md` |
| Pre-mortem / anticipate failures / risk planning | `skills/engineering/pre-mortem/SKILL.md` |
| Post-mortem / review completed work / find errors | `skills/engineering/post-mortem/SKILL.md` |
| Diagnose / debug / reproduce root cause | `skills/engineering/diagnose/SKILL.md` |
| Zoom-out / explore codebase / architecture | `skills/engineering/zoom-out/SKILL.md` |
| Caveman / compressed communication / brief | `skills/productivity/caveman/SKILL.md` |
| markdown-to-itmz / convert markdown to mind map | `skills/productivity/markdown-to-itmz/SKILL.md` |
| rice / RICE prioritization / score tasks | `skills/engineering/rice/SKILL.md` |
| Bootstrap / first-run / setup issue tracker and triage labels | `skills/engineering/setup-zack-skills/SKILL.md` |

## Disambiguation

1. **Review vs Audit**: code review → `/check`; agent/config audit → `/health`
2. **Bug/hunt vs review**: code doesn't work → `/diagnose`; code works but needs review → `/check`
3. **Pre-build vs post-build**: new features, planning → `/pre-mortem`; implementation done → `/check`
4. **Meta skills**: pre-mortem, post-mortem, diagnose, zoom-out, caveman — invoked directly by name

## Chaining

- `/setup-zack-skills` (once) → other skills gain repo context
- `/check` review done → user decides next step
- `/health` audit done → user decides fix → re-run `/health` to verify
- `/diagnose` done → fix → `/check` to verify

## Project Context

Apply skill to current project: read README, CI config, package.json, and git status before acting.
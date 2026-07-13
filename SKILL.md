---
name: harness
description: "Engineering skill toolkit for Claude Code: code review, pre/post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, mind map. Invoked as /harness or by skill name."
when_to_use: "review, code review, pre-merge, project audit, health check, CLAUDE.md drift, diagnose, debug, explore architecture, caveman, rice, mind map"
dispatch_intent: "Code review, pre-mortem planning, post-mortem analysis, bug diagnosis, codebase exploration, compressed communication, task prioritization, markdown to mind map"
---

# Harness Skills

🥷 Engineering skill toolkit for Claude Code.

## Available Skills

All skills live under the `skills/` subdirectory. Invoke by name.

### /check

Code review for diffs, PRs, commits, and project audits.

- **Entry**: `skills/check/SKILL.md`
- **Triggers**: review, code review, pre-merge, PR review, diff review, project audit, 合并前, 代码审查
- **Covers**: type safety, error handling, JSDoc, security, performance

### /health

Agent health audit for configuration drift and AI maintainability.

- **Entry**: `skills/health/SKILL.md`
- **Triggers**: health, 体检, audit, agent audit, CLAUDE.md drift, hooks, MCP, AI maintainability
- **Covers**: CLAUDE.md drift, hooks validity, MCP tool availability, memory system, context completeness

### /caveman

Ultra-compressed communication — drop filler, articles, pleasantries. Keep technical accuracy.

- **Entry**: `skills/caveman/SKILL.md`
- **Triggers**: caveman, compressed, brief, terse, minimal

### /diagnose

Disciplined bug diagnosis: reproduce → minimise → hypothesise → instrument → fix → regression-test.

- **Entry**: `skills/diagnose/SKILL.md`
- **Triggers**: diagnose, debug, bug, fix, root cause

### /markdown-to-itmz

Generate iThoughts mind map (.itmz) from any Markdown file.

- **Entry**: `skills/markdown-to-itmz/SKILL.md`
- **Triggers**: markdown-to-itmz, mind map, itmz, 思维导图

### /post-mortem

Review completed work, find logic errors and implementation gaps. Fix immediately.

- **Entry**: `skills/post-mortem/SKILL.md`
- **Triggers**: post-mortem, review, find errors

### /pre-mortem

Imagine catastrophic failure, work backwards to identify risks and mitigations.

- **Entry**: `skills/pre-mortem/SKILL.md`
- **Triggers**: pre-mortem, failure modes, risk planning

### /rice

RICE prioritization: score and rank tasks by Reach, Impact, Confidence, Effort.

- **Entry**: `skills/rice/SKILL.md`
- **Triggers**: rice, prioritize, score, rank

### /zoom-out

Explore codebase architecture, map modules and relationships.

- **Entry**: `skills/zoom-out/SKILL.md`
- **Triggers**: zoom-out, architecture, explore, map modules

## Routing Table

| Trigger | Skill |
|---------|-------|
| Code review, PR review, merge gate | `skills/check/SKILL.md` |
| Project audit, quality scorecard | `skills/check/SKILL.md` |
| Agent config audit, CLAUDE.md drift | `skills/health/SKILL.md` |
| Hooks/MCP check | `skills/health/SKILL.md` |
| Caveman/compressed communication | `skills/caveman/SKILL.md` |
| Bug diagnosis/debug | `skills/diagnose/SKILL.md` |
| Post-mortem/review completed work | `skills/post-mortem/SKILL.md` |
| Pre-mortem/risk planning | `skills/pre-mortem/SKILL.md` |
| RICE prioritization | `skills/rice/SKILL.md` |
| Codebase architecture exploration | `skills/zoom-out/SKILL.md` |
| Markdown to mind map | `skills/markdown-to-itmz/SKILL.md` |

## Output Convention

All skills prefix the first line inline with 🥷. Findings include specific file:line references and actionable recommendations.

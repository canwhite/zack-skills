---
name: zack-skills
description: "Engineering skill toolkit for Claude Code: planning, pre/post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, mind map. Invoked as /zack-skills or by skill name."
when_to_use: "plan, planning, design, diagnose, debug, explore architecture, caveman, rice, mind map, pre-mortem, post-mortem, pain-decomposition, 痛点拆解, 功能点, MVP 路径"
dispatch_intent: "Interactive planning, pre-mortem risk analysis, post-mortem analysis, bug diagnosis, codebase exploration, compressed communication, task prioritization, markdown to mind map, pain point decomposition with feature + MVP launch path"
---

# Zack Skills

🥷 Engineering skill toolkit for Claude Code.

## Available Skills

All skills live under the `skills/` subdirectory. Invoke by name.

### /caveman

Ultra-compressed communication — drop filler, articles, pleasantries. Keep technical accuracy.

- **Entry**: `skills/productivity/caveman/SKILL.md`
- **Triggers**: caveman, compressed, brief, terse, minimal

### /diagnose

Disciplined bug diagnosis: reproduce → minimise → hypothesise → instrument → fix → regression-test.

- **Entry**: `skills/engineering/diagnose/SKILL.md`
- **Triggers**: diagnose, debug, bug, fix, root cause

### /markdown-to-itmz

Generate iThoughts mind map (.itmz) from any Markdown file.

- **Entry**: `skills/productivity/markdown-to-itmz/SKILL.md`
- **Triggers**: markdown-to-itmz, mind map, itmz, 思维导图

### /planning

Interactive planning: clarify the request, then write a structured plan markdown to `docs/` following Plan / Think / Do / Adjust.

- **Entry**: `skills/engineering/planning/SKILL.md`
- **Triggers**: plan, planning, design, how to build, 怎么实现, 方案

### /pain-decomposition

Pain point identification and decomposition: summarize core pain, split into noun/verb/adjective&adverb (entities/actions/rules), then derive metrics + data schema, business flow, latent requirements, and roll up into Features + MVP launch path. Output to `docs/painpoint-<slug>.md`.

- **Entry**: `skills/engineering/pain-decomposition/SKILL.md`
- **Triggers**: pain point, 痛点拆解, 痛点分解, 痛点识别, decompose pain, 分析痛点, MVP 路径, 功能点拆解

### /post-mortem

Review completed work, find logic errors and implementation gaps. Fix immediately.

- **Entry**: `skills/engineering/post-mortem/SKILL.md`
- **Triggers**: post-mortem, review, find errors

### /pre-mortem

Imagine catastrophic failure, work backwards to identify risks and mitigations.

- **Entry**: `skills/engineering/pre-mortem/SKILL.md`
- **Triggers**: pre-mortem, failure modes, risk planning

### /rice

RICE prioritization: score and rank tasks by Reach, Impact, Confidence, Effort.

- **Entry**: `skills/engineering/rice/SKILL.md`
- **Triggers**: rice, prioritize, score, rank

### /zoom-out

Explore codebase architecture, map modules and relationships.

- **Entry**: `skills/engineering/zoom-out/SKILL.md`
- **Triggers**: zoom-out, architecture, explore, map modules

## Routing Table

| Trigger | Skill |
|---------|-------|
| Caveman/compressed communication | `skills/productivity/caveman/SKILL.md` |
| Bug diagnosis/debug | `skills/engineering/diagnose/SKILL.md` |
| Post-mortem/review completed work | `skills/engineering/post-mortem/SKILL.md` |
| Pre-mortem/risk planning | `skills/engineering/pre-mortem/SKILL.md` |
| RICE prioritization | `skills/engineering/rice/SKILL.md` |
| Codebase architecture exploration | `skills/engineering/zoom-out/SKILL.md` |
| Markdown to mind map | `skills/productivity/markdown-to-itmz/SKILL.md` |
| Pain point decomposition / 痛点拆解 | `skills/engineering/pain-decomposition/SKILL.md` |
| Plan / design / how to build | `skills/engineering/planning/SKILL.md` |

## Output Convention

All skills prefix the first line inline with 🥷. Findings include specific file:line references and actionable recommendations.
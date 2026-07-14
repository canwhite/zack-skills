---
name: planning
description: "Plan a task, feature, or change by clarifying the question, writing a structured plan markdown to docs/, and recommending a follow-up pre-mortem. Use when the user says 'plan this', 'how should we build X', 'design a solution', or asks for an implementation approach before any code is written."
triggers:
  - /planning
  - plan this
  - plan a
  - how should we build
  - how to build
  - design a solution
  - propose a solution
  - implementation approach
  - 怎么实现
  - 设计一下
  - 规划
  - 方案
when_to_use: "plan, planning, design, how to build, how should we, propose a solution, implementation approach, 怎么实现, 设计一下, 规划, 方案"
dispatch_intent: "Interactive planning: clarify intent, write plan to docs/ following Plan/Think/Do/Adjust structure, then recommend pre-mortem"
---

# Planning: From Request to Plan Markdown

🥷 Interactive planning. Clarify → write plan → recommend pre-mortem.

## Core Principles

A good plan is **small, verifiable, and reversible**. This skill applies these constraints consistently:

- **Plan / Think / Do / Adjust** — every plan uses these four sections, in this order.
- **Debug at boundaries** — when execution starts, log at framework entry points, check logs first, read source before guessing.
- **Verification is required** — build, static analysis, and runtime verification are not optional. No "I'll verify later."
- **Logic correctness** — list every affected execution path, prove each return value, cover edge cases.
- **Global scan after fix** — one-place patches are technical debt. Find the pattern, fix the pattern.

## When to Ask vs When to Write

**Ask the user (via AskUserQuestion) when ANY of these is true:**

- The request names a feature/goal but does NOT specify scope, success criteria, or constraints.
- Multiple reasonable approaches exist and the trade-offs change the plan structure (e.g., batch vs stream, sync vs async, library choice).
- The plan would touch a system whose current state is unknown (e.g., "add auth" but unclear which auth model, which provider, where users live).
- The request has conflicting goals (e.g., "fast MVP" + "production-grade security").

**Just write the plan (no questions) when:**

- The request is concrete: "add a `cli.py all` subcommand that installs every skill, skipping already-installed ones" → clear, write directly.
- The user has already given scope in a previous turn (use it as ground truth).
- The trade-off is conventional (e.g., which Python version) — pick a sensible default, note it in the plan.

**Bias toward writing.** If you can produce a useful plan with stated assumptions, write it and call out the assumptions in the "Open Questions" section. Don't block on perfect information.

## Workflow

### 1. Receive and Parse the Request

Identify:

- **Goal** — what the user wants to exist or change.
- **Constraints** — known limits (time, tech stack, compatibility, performance).
- **Unknowns** — what must be asked or assumed.

If `Unknowns` is non-empty and would change the plan, jump to Step 2. Otherwise jump to Step 3.

### 2. Clarify (if needed)

Use AskUserQuestion to resolve the highest-leverage unknowns. Ask **at most 2-3 questions per round** — never interrogate. Each question must change the plan structure, not just refine wording.

Prefer multi-choice questions with sensible defaults over open-ended questions.

### 3. Choose Plan Location

Default path: `docs/plan-<slug>.md` where `<slug>` is a short kebab-case summary (e.g., `cli-all-command`, `auth-jwt-migration`).

If a plan with that slug already exists, append a date suffix: `docs/plan-<slug>-YYYY-MM-DD.md`.

If the user explicitly specifies a path, use that path.

### 4. Write the Plan

Use the template below. Fill every section — empty sections are a smell. If a section genuinely doesn't apply, write "N/A — <reason>" rather than omitting.

```markdown
# Plan: <Title>

> One-sentence goal of this plan.

## Context

Why this plan exists now. What problem it solves. What constraints shape it.

## Goal

The end state when this plan is done. Measurable if possible.

## Plan

Numbered steps in execution order. Each step is one logical unit of work.

1. ...
2. ...
3. ...

## Think — Debug Methodology

What debugging approach to apply when execution starts:

- Where to add logs (framework boundaries, not business logic).
- What to read first (source > docs > StackOverflow).
- How to localize the problem (upstream first, then downstream).
- What to grep for (`[DEBUG-` prefix convention, or whatever the codebase uses).

## Do — Verification Strategy

Required verification gates before declaring done:

- **Build**: `<command>` — must pass.
- **Static analysis / type check**: `<command>` — zero errors.
- **Runtime verification**: what server starts, what curl/browser command proves it works.
- **Logic correctness**: which execution paths must be manually walked through.

## Adjust — Rollback and Global Scan

- **Rollback plan**: how to undo this change cleanly if it goes wrong.
- **Global scan**: after the fix, what analogous places to check for the same pattern. Don't leave latent twins.
- **Backwards compatibility**: if applicable, what shim or migration is needed.

## Open Questions

Things still uncertain after this plan. Either to be resolved during execution, or to be tracked as separate work.

- ...

## Out of Scope

What this plan explicitly does NOT do.

- ...

---

> Next step: run `/pre-mortem <plan-file>` to identify failure modes and harden this plan.
```

### 5. Save and Confirm

After writing:

1. State the path to the file.
2. State the next step: "Run `/pre-mortem docs/plan-<slug>.md` to harden this plan against failure modes."
3. Stop. Do not start executing the plan.

## Output Convention

Output prefix (first line, inline): `🥷`.

After saving the file, the response is just the path + next step + a one-line summary of what the plan covers. Don't restate the plan content — it's in the file.

## Constraints (do not violate)

- **Never start coding** as part of this skill. Output is a plan markdown, nothing else.
- **Never silently skip the Plan / Think / Do / Adjust sections.** They are the value.
- **Never auto-generate risks** — that's `/pre-mortem`'s job. Leave a clean "Next step" pointer.
- **Never write to a file outside `docs/`** unless the user explicitly directs.

## Pro Tips

- **Slug naming matters**: a good slug makes the plan findable later. Prefer noun-verb (`auth-migration`, `cli-all-cmd`) over vague names (`plan1`, `new-feature`).
- **Plan length scales with risk**: a typo fix is a 5-line plan; a migration is 100+ lines. Match detail to stakes.
- **Bias to assumptions over questions**: if you can write a working plan with stated assumptions, do that. Questions are for things that would change the plan structure.
- **Link related plans**: if this plan supersedes or depends on another plan file, link it in the Context section.
- **Date stamps help**: append `-YYYY-MM-DD` if you ever write multiple plans on the same topic (e.g., a redesign).
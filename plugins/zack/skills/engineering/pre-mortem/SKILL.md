---
name: pre-mortem
description: Pre-mortem analysis that updates a plan markdown inline with all risks and mitigations. Use when user invokes /pre-mortem with a plan file, asks to anticipate risks on a plan, or wants failure modes analysis with automatic plan updates.
---

# Pre-Mortem Analysis

## Philosophy

A pre-mortem is a technique where we **imagine the project has catastrophically failed** and work backwards to identify what could have caused that failure. Unlike a post-mortem (done after failure), a pre-mortem is done *before* starting work, when we're still optimistic and can take preventive action.

**Core principle**: The goal is to identify failure modes *before* they happen, not to be pessimistic. We're hedging against risk, not predicting doom.

**Key rule**: EVERY identified risk MUST have a mitigation solution before the pre-mortem ends. No risk is left without a response plan.

## Input

When invoked with `/pre-mortem <plan-file>`, the first step is to **read the plan markdown** to understand the project scope and context. All subsequent analysis is based on this plan.

## Workflow

### 1. Read and Set the Stage

1. Read the plan markdown file to understand the project context.
2. State the project clearly based on the plan.
3. Dramatically announce:

> "It's six months into the future. This project has failed catastrophically. The worst possible version of this has happened. What went wrong?"

### 2. Generate Failure Modes (Brainstorm) — FULLY AUTOMATIC LOOP

**Automatically loop until no new HIGH RISKS are found (Risk Score > 12).**

**DO NOT ask the user for confirmation during the loop. Keep generating and assessing until convergence.**

Loop iterations:
1. Generate a batch of failure hypotheses across all categories (technical, team, external). Do NOT filter.
2. For each hypothesis, assess:
   - **Severity**: How bad would this be? (1-5)
   - **Likelihood**: How likely is this? (1-5)
   - **Detectability**: Would we see it coming? (1-5)
   - **Risk Score**: Severity × Likelihood × (1 - Detectability)
3. Flag risks with Risk Score > 12 as **HIGH RISK**.
4. **Immediately** update the plan markdown with each risk and its mitigation (see Step 3).
5. **Continue to next iteration** — do NOT ask the user anything.
6. **Stop condition**: When an entire iteration produces zero new HIGH RISKS, the loop ends.

Categories to explore across iterations:

**Technical failures:**
- Architecture doesn't scale to real usage
- Key dependency becomes unmaintained or incompatible
- Performance problems emerge under production load
- Security vulnerabilities discovered late
- Data loss or corruption
- Integration failures with external services

**Team/organizational failures:**
- Scope creep overwhelms the team
- Key team member leaves or is reassigned
- Misaligned expectations with stakeholders
- Insufficient documentation for future maintainers
- Communication breakdown

**External failures:**
- Market conditions change, making the project irrelevant
- Competitor releases something better
- Regulatory changes impact the approach
- Vendor lock-in or price changes

Common categories to explore:

**Technical failures:**
- Architecture doesn't scale to real usage
- Key dependency becomes unmaintained or incompatible
- Performance problems emerge under production load
- Security vulnerabilities discovered late

**Team/organizational failures:**
- Scope creep overwhelms the team
- Key team member leaves or is reassigned
- Misaligned expectations with stakeholders
- Insufficient documentation for future maintainers

**External failures:**
- Market conditions change, making the project irrelevant
- Competitor releases something better
- Regulatory changes impact the approach

### 3. Develop Mitigations — UPDATE PLAN INLINE (AUTOMATIC)

**For EVERY identified risk, immediately develop a mitigation and update the plan markdown.** This happens automatically inside the loop — do NOT batch updates or wait.

```markdown
### [Risk] {Risk Title}

**Severity**: {1-5} | **Likelihood**: {1-5} | **Detectability**: {1-5}
**Risk Score**: {Severity × Likelihood × (1 - Detectability)}

**Failure Scenario**: {What happens if this risk materializes}

**Mitigation**:
- {Specific action to reduce likelihood or impact}
- {Additional action if applicable}
```

**Critical**: Every risk entry MUST have a Mitigation section before moving to the next risk.

### 4. Final Review

After the loop ends (zero new HIGH RISKS in an iteration):
1. Output a brief summary: "Pre-mortem complete. Found X HIGH RISKS, Y medium/low risks. All have mitigations."
2. List all HIGH RISKS and their mitigations for quick reference.
3. Done — do NOT ask the user anything else.

## Plan Markdown Format

The plan markdown should be updated to include a pre-mortem section. If the plan doesn't have one, append:

```markdown
---

## Pre-Mortem Risks

<!-- AUTO-GENERATED: New risks will be appended below -->

```

Then append each risk with its mitigation as described in Step 3.

## Pro Tips

- **Go absurd first**: Start with the most ridiculous failure scenario to get people comfortable with saying "what if." Then dial back to realistic.
- **Not just technical**: Half of real project failures are organizational, not technical. Make sure to explore team, process, and external risks.
- **Psychological safety**: The pre-mortem must be a safe space to surface concerns. Frame it as "what could we do differently" not "whose fault would this be."
- **Every risk gets a mitigation**: No exceptions. If you can't think of a good mitigation, that's a signal the risk is very high and needs creative thinking — keep iterating until you have a concrete plan.
- **Inline updates**: Update the plan markdown as you go, not at the end. This keeps the mitigation work fresh and actionable.
- **Don't over-do it**: For small tasks, a 5-minute pre-mortem is fine. Reserve deep pre-mortems for significant projects.

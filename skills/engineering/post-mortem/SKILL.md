---
name: post-mortem
description: Post-mortem analysis with diagnose capabilities. Reviews completed work, finds logic errors, implementation gaps, and potential bugs, then fixes them. Use when user invokes /post-mortem, asks to review completed features, wants to audit implemented code, or asks to find bugs in existing implementation.
---

# Post-Mortem Analysis

## Philosophy

A post-mortem is a disciplined review of **completed work** to find what went wrong, what could be better, and what bugs lurk unseen. Unlike a pre-mortem (done before starting), a post-mortem examines actual implementation.

**Core principle**: Just because code works doesn't mean it works correctly. Hidden bugs, logic errors, and implementation gaps cost more the later they're found.

**Key rules**:
1. **Find it, fix it**: Every discovered issue is fixed immediately. No bug lists, no deferred fixes.
2. **Survey first**: Understand the territory before diving into details.
3. **Prevention > Cure**: Root cause analysis prevents future occurrences.

## Input

When invoked with `/post-mortem <target>`, the target can be:
- A plan/feature markdown — review the implementation against the plan
- A directory — review all code in that area
- A specific file — deep-dive that file

First, read the target to understand context. If it's a plan, also read the implementation to understand what was built.

## Workflow

### Phase 1 — Survey the Territory

Establish a mental model before digging in. This saves time and prevents missing context.

1. **Map modules** — identify key modules and their relationships
2. **Trace entry/exit points** — where does data enter and leave?
3. **Note data flows** — inputs → transformations → outputs
4. **Check existing coverage** — what tests already exist?
5. **Apply domain vocabulary** — use the project's glossary terms
6. **Check ADRs** — respect documented architectural decisions

**Deletion Test** (from `/improve-codebase-architecture`): If deleting a module makes complexity vanish, it was a pass-through — suspicious. If complexity reappears across N callers, it was earning its keep.

**Deliverable**: A brief map comment confirming your understanding. Proceed only when you have a clear picture.

---

### Phase 2 — Diagnose Known Issues

Apply the full `/diagnose` discipline to any **known, reported issues**:

**2.1 — Build a feedback loop**
Construct a pass/fail signal:
- Failing test at the bug seam → HTTP script → CLI fixture → headless browser → replay trace → throwaway harness → bisection harness

**2.2 — Reproduce**
Confirm the bug reproduces. Capture the exact symptom.

**2.3 — Hypothesise**
Generate 3-5 ranked, falsifiable hypotheses:
> "If X is the cause, then changing Y will make it disappear."

Show ranked list to user before testing — they often have domain knowledge that re-ranks.

**2.4 — Instrument**
One variable at a time. Use debugger or tagged logs `[DEBUG-xxx]`.

**2.5 — Fix + regression test**
Write failing test first → apply fix → verify passes → run original loop to confirm.

**2.6 — Cleanup**
Remove debug instrumentation. State the correct hypothesis in commit/PR.

---

### Phase 3 — Systematic Audit

**Audit the entire codebase systematically. Do not wait to be told what to check.**

#### 3.1 Data Flow
- [ ] Trace every input — where does it come from? Who controls it?
- [ ] Trace every output — where does it go? What's downstream?
- [ ] Boundary conditions: empty, null, zero, negative, max values
- [ ] Race conditions: concurrent access, async ordering
- [ ] Data consistency: same data in multiple places, sync issues

#### 3.2 Control Flow
- [ ] Every branch taken? (if/else, switch, ternary)
- [ ] Every error path exercised? (try/catch, .catch(), error boundaries)
- [ ] Every loop termination guaranteed? (infinite loop risks)
- [ ] State machine violations? (illegal transitions)

#### 3.3 Contracts
- [ ] Function preconditions checked?
- [ ] Function postconditions guaranteed?
- [ ] API contracts honored at boundaries?
- [ ] Assumptions documented vs actual?

#### 3.4 Security
- [ ] Input validation on all entry points
- [ ] Output sanitization on all exits
- [ ] Authentication/authorization at boundaries
- [ ] Sensitive data exposure (logs, errors, responses)

#### 3.5 Performance
- [ ] N+1 queries
- [ ] Unbounded loops over large datasets
- [ ] Memory leaks (growing caches, unclosed resources)
- [ ] Unnecessary recomputation

#### 3.6 Architecture (from `/improve-codebase-architecture`)
- [ ] Deletion test: pass-through modules?
- [ ] Shallow modules: interface ≈ implementation complexity?
- [ ] Tight coupling across seams?

#### 3.7 Hidden Bugs

These slip through even when the audit looks clean:

- Off-by-one errors (loops, indices, pagination)
- Null/undefined mishandling (destructuring from null, optional chaining abuse)
- Async edge cases (race conditions, unhandled rejections, forgotten awaits)
- Type coercion bugs (== vs ===, string vs number, parseInt radix)
- Error swallowing (catch blocks that silently continue)
- Resource leaks (unclosed connections, file handles, timers)
- Hardcoded assumptions ("always < 1000", "always returns JSON")
- Timezone/date edge cases (DST, locale, epoch)
- Copy-paste errors (similar code that diverged)
- Comment/code drift (comments contradict code)

**For every issue found: immediately apply the fix.**

---

### Phase 4 — Spec vs Implementation (from `/grill-with-docs`)

If a plan/spec exists, cross-reference it against the code:

- [ ] All features in spec implemented?
- [ ] All edge cases handled as specified?
- [ ] Error handling matches spec?
- [ ] Performance/security/observability requirements met?

**When spec ≠ code, surface it immediately:**
> "Your plan says partial cancellation is supported, but the code only handles full order cancellation."

This is a bug — fix it.

---

### Phase 5 — Prevention (from `/to-issues`)

After all fixes are applied:

1. **Summarize** what was found and fixed
2. **Root cause analysis** — why was each bug introduced?
3. **Classify prevention as HITL or AFK**:
   - **AFK**: Can be implemented without human interaction (regression test, input validation)
   - **HITL**: Requires human judgment, design review, or external access

4. **Present as actionable tasks** with acceptance criteria:

```markdown
### Prevention Task: {Title}

**Type**: AFK | HITL
**Root Cause**: {Why the bug happened}
**Prevention**: {What would have caught this}

**Acceptance Criteria**:
- [ ] {Criterion 1}
```

5. **Offer to create issues** for AFK tasks immediately. Ask user which HITL tasks to pursue.

---

## Output

### Per-Issue Documentation

```markdown
### [BUG-{N}] {Title}

**Location**: `{file}:{line}`
**Severity**: {Critical/High/Medium/Low}
**Type**: {Logic Error/Off-by-one/Contract Violation/etc}

**Description**: {What the bug is}
**Why it's wrong**: {Logic error / assumption violation}
**Fix**: ```{language}
{Before} → {After}
```
**Test**: {What would catch this}
```

### Final Summary

```markdown
## Post-Mortem: {Target}

**Date**: {date}

### Issues Fixed

| # | Severity | Type | Location |
|---|----------|------|----------|
| 1 | High | Race Condition | auth/session.ts:42 |
| 2 | Medium | Off-by-one | utils/pagination.ts:18 |

### Root Causes
1. {Root cause 1}
2. {Root cause 2}

### Prevention Tasks

| Task | Type |
|------|------|
| Add regression test for auth refresh | AFK |
| Refactor payment module seam | HITL |

### Files Modified
- {list}
```

---
name: check
description: "Reviews code diffs, PRs, commits, and project audits. Use when the user asks for code review, pre-merge checks, issue triage, or project quality scoring. Not for debugging runtime errors or planning new features."
when_to_use: "review, 看看代码, 检查一下, 有没有问题, 是否需要优化, 合并前, code review, code-review, pre-merge, PR review, diff review, audit, project audit, 项目体检, 项目评分, 代码质量"
dispatch_intent: "Code review, before merge, release gates, safety sinks, project-wide audit scorecard"
---

# Check: Code Review

🥷 Code review for diffs, PRs, commits, and project audits.

## Outcome Contract

- Outcome: a review grounded in the current diff, project context, and live evidence.
- Done when: findings are stated with specific file:line references and actionable suggestions.
- Evidence: git diff, project docs, CI config, package contents.
- Output: concise findings first, then verification summary.

## Review Checklist

1. **Type safety** — are types correct and explicit?
2. **Error handling** — are errors caught and handled gracefully?
3. **JSDoc** — are public functions documented?
4. **Security** — any obvious vulnerabilities (injection, hardcoded secrets)?
5. **Performance** — any obvious bottlenecks or O(n²) patterns?

## Worktree Safety Preflight

Before the review, run:

```bash
git status --short --branch -uall
```

## Output Format

```
🥷 [brief summary line]

## Findings

### Problems
- **<file>:<line>** — <description>

### Suggestions
- ...

### Security
- ...

## Score: X/10
**Issues found**: N
**Recommendation**: ...
```

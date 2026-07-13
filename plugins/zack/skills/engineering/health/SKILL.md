---
name: health
description: "Runs an engineering health audit for instruction drift, hooks, MCP tool drift, and AI maintainability. Use when the user asks to audit agent configuration, check CLAUDE.md drift, verify hooks, or assess project health."
when_to_use: "health, 体检, 健康检查, audit, agent audit, CLAUDE.md drift, hooks check, MCP tools, 配置审计, AI maintainability, instruction drift"
dispatch_intent: "Agent configuration audit, instruction drift detection, hooks/MCP verification, AI maintainability scorecard"
---

# Health: Engineering Health Audit

🥷 Agent health audit for configuration drift and AI maintainability.

## Outcome Contract

- Outcome: an audit report covering instruction drift, tool availability, and maintainability signals.
- Done when: findings are stated with specific files, drift evidence, and recommended actions.
- Evidence: CLAUDE.md, .claude/settings.json, hooks, MCP config, agent instructions.
- Output: audit findings with severity labels.

## Audit Checklist

1. **CLAUDE.md drift** — do agent instructions match current project practices?
2. **Hooks** — are pre/post hooks still relevant and pointing to valid paths?
3. **MCP tools** — are configured MCP servers still available and authorized?
4. **Memory system** — is MEMORY.md relevant and up to date?
5. **Context completeness** — does the agent have enough project context to act correctly?

## Worktree Preflight

```bash
git status --short --branch -uall
ls -la .claude/ 2>/dev/null || echo "No .claude directory"
cat CLAUDE.md 2>/dev/null | head -20
```

## Output Format

```
🥷 [brief summary line]

## Audit Findings

### High
- **<area>** — <description> → <action>

### Medium
- ...

### Low
- ...

## Health Score: X/10
**Drift detected**: N
**Recommendation**: ...
```

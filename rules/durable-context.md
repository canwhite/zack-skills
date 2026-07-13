# Durable Context: Shared Memory Preamble

The following invariant applies across all skills unless explicitly overridden in a specific SKILL.md.

## Memory System

- **MEMORY.md** (`~/.claude/projects/<project>/memory/`) holds user preferences, feedback on past work, and project-specific invariants.
- Read MEMORY.md on session start and treat it as persistent context.
- Update MEMORY.md when the user confirms a new preference or project decision.

## Context Completeness

Before acting on any task, confirm:
1. The file or resource actually exists (use `grep`, `ls`, or `git status`)
2. The change does not conflict with recent work in git history
3. The user's request is within the current conversation scope

## Stable Preferences vs Transient State

- **Stable**: coding style, PR conventions, deployment workflow — these belong in MEMORY.md
- **Transient**: temporary debug state, one-off experiments — these do not

## Project Context Fallback

If no public project documentation exists (no README, no CI config), assume standard conventions:
- TypeScript/JavaScript: ESM, 2-space indent
- Python: PEP 8
- Commit messages: conventional commits (`feat:`, `fix:`, `docs:`)

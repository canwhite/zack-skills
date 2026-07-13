# Anti-Patterns: Cross-Skill AI Behavior

Always-on behavioral guardrails. These apply regardless of which skill is active. Per-skill gotchas stay in each SKILL.md.

| # | Pattern | Wrong | Right |
|---|---------|-------|-------|
| 1 | Act before reading | Start editing after the first sentence | Read the entire message, then act |
| 2 | Hallucinate paths | Reference `src/components/Auth.tsx` from memory | `grep -r` to confirm the file exists |
| 3 | Serial interrogation | Ask 5 separate questions across 5 messages | Batch all questions into one message |
| 4 | Do more than asked | "Fix X" becomes fix X plus refactor Y and Z | Build the smallest change that satisfies the request |
| 5 | Claim without evidence | "This should work" with no command output | Run the command and paste output |
| 6 | Trust stale memory | "We discussed this earlier" | Re-verify current state before acting |
| 7 | Format overkill | Simple answer wrapped in headers + list + summary | Match response complexity to question complexity |
| 8 | Announce instead of act | "I will now proceed to update the file" | Update the file, state what changed |
| 9 | Summarize unsolicited | Append a "changes made" recap after every edit | Stop after the deliverable unless the user asks |
| 10 | Invent missing data | Fill a gap with plausible-sounding content | Mark the gap and ask the user |
| 11 | Ignore error output | Command fails, continue as if it passed | Read the error, diagnose, fix or report |
| 12 | Unsolicited version bump | Bump version number without being asked | Only bump when the user explicitly requests it |
| 13 | Create files unprompted | Create new files the user never asked for | Only create files requested or required by the task |
| 14 | Retry without new evidence | Same command failed twice, try a third time | Gather new evidence before retrying |
| 15 | Attribution leak | Include `Co-Authored-By: Claude` in commits | Never add AI attribution to public-facing text |
| 16 | Implicit authorization escalation | User says "ok", agent executes destructive action | Only execute destructive actions when explicitly requested |
| 17 | Compile-only UI verification | Mark UI bug fixed because code compiled | Run the app/page or state the exact runtime check |
| 18 | Security fix without rollback | Patch a security path without documenting revert | Include rollback path and regression checks |
| 19 | Provenance leak into durable rules | Copy private paths, secrets into shared skills | Extract only stable transferable invariants |
| 20 | Mishandle a bundle of asks | User packs several requests; agent acts on first and drops rest | Enumerate every distinct ask, act only on accepted subset |
| 21 | Fix one instance, ignore siblings | Fix exact line user pointed at and stop | After fixing a class-of-bug, grep for the same shape |
| 22 | Hidden dependency | Move logic into helper requiring undeclared package | Declare dependency in CI/docs or remove it |
| 23 | Scorecard without contract | Say change is "8/10" without naming the contract | Replace with actionable constraints |
| 24 | Review request as worktree authorization | Switch branches, stash, reset during review | Start with `git status --short --branch -uall` |

# Zack Skills

A toolkit of engineering workflow skills for Claude Code: pre-mortem, post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, and markdown-to-mind-map. Each skill is a Markdown workflow with frontmatter-driven dispatch; one `VERSION` file is the single source of truth for all generated artifacts (marketplace metadata, npm package, Codex mirror, dispatcher table, per-skill update check).

## Skills

| Skill | Description |
|-------|-------------|
| `caveman` | Ultra-compressed communication mode. |
| `diagnose` | Disciplined diagnosis loop for hard bugs and performance regressions. |
| `improve-architecture` | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. |
| `markdown-to-itmz` | Generate an iThoughts (.itmz) mind map from any Markdown file. |
| `pain-decomposition` | Identify the core pain from a description, split it by parts of speech into nouns (Entity), verbs (Action), and adjectives/adverbs (Rules), then derive core metrics + data schema, business flow, and latent requirements, and finally roll these up into deliverable Features and an MVP launch path. |
| `planning` | Plan a task, feature, or change by clarifying the question, writing a structured plan markdown to docs/, and recommending a follow-up pre-mortem. |
| `post-mortem` | Post-mortem analysis with diagnose capabilities. |
| `pre-mortem` | Pre-mortem analysis that updates a plan markdown inline with all risks and mitigations. |
| `rice` | RICE prioritization framework for scoring and ranking tasks. |
| `zoom-out` | Tell the agent to zoom out and give broader context or a higher-level perspective. |

## Install

### Via skills-cli (recommended)

```bash
npx skills add https://github.com/canwhite/zack-skills -g
```

### Claude Code plugin

```bash
/plugin marketplace add zack-skills
/plugin install zack-skills@zack-skills
```

## Uninstall

```bash
rm -rf ~/.claude/skills/zack-skills
```

## Development

```bash
make test              # verify frontmatter + scripts + drift
make regenerate        # rebuild all generated artifacts
make verify-generated  # CI: fail if generated files drift from source
```

See [`docs/zoom-out.md`](docs/zoom-out.md) for the architecture reference (modules, dispatch flow, packaging model).

## License

MIT

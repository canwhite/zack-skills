---
name: rice
description: RICE prioritization framework for scoring and ranking tasks. Use when user invokes /rice, asks to prioritize tasks, score features, or rank items by impact vs effort.
---

# RICE Prioritization

## RICE Formula

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

| Factor | Definition | Scale |
|--------|------------|-------|
| **Reach** | How many people will this affect per quarter? | Number (person count) |
| **Impact** | How much does it impact each person? | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| **Confidence** | How confident are we in the estimates? | 100% = high, 80% = medium, 50% = low |
| **Effort** | How many person-weeks to implement? | Number (weeks) |

Higher score = higher priority.

## Workflow

### 1. Gather Tasks

List all tasks/features to prioritize. One per row.

### 2. Score Each Task

For each task, assess:

| Task | Reach | Impact | Confidence | Effort | RICE Score |
|------|-------|--------|------------|--------|------------|
| Feature A | 1000 | 2 | 80% | 3 | (1000×2×0.8)/3 = 533 |
| Feature B | 200 | 3 | 50% | 2 | (200×3×0.5)/2 = 150 |
| ... | | | | | |

### 3. Rank by Score

Sort descending by RICE score.

### 4. Present Results

```markdown
## RICE Prioritization

| Task | Reach | Impact | Confidence | Effort | RICE Score | Rank |
|------|-------|--------|------------|--------|------------|------|
| Auth improvements | 2000 | 2 | 100% | 2 | 2000 | 1 |
| Dashboard redesign | 500 | 3 | 80% | 5 | 240 | 2 |
| Export feature | 300 | 1 | 80% | 3 | 80 | 3 |

**Recommendation**: Focus on top 3. Lower scores suggest: reduce scope, increase confidence, or kill.
```

## Quick Reference

- **Score > 100**: Strong candidate
- **Score 50-100**: Consider if capacity allows
- **Score < 50**: Low priority or reconsider scope

## Pro Tips

- **Reach vs Effort**: A small effort reaching many beats a big effort reaching few.
- **Confidence matters**: Low confidence = high risk. Probe assumptions.
- **Impact is subjective**: Use consistent rubric across all tasks.
- **Effort in weeks**: 1 week = 1 person working full-time.

## When to Use

- Sprint planning
- Roadmap prioritization
- Feature selection when capacity is limited
- Quarterly planning

---
name: pain-decomposition
description: Identify the core pain from a description, split it by parts of speech into nouns (Entity), verbs (Action), and adjectives/adverbs (Rules), then derive core metrics + data schema, business flow, and latent requirements, and finally roll these up into deliverable Features and an MVP launch path. Output document is written in Chinese to docs/painpoint-<slug>.md. Use when the user asks to decompose a pain point, analyze a pain point, identify pain points, 拆解痛点, 痛点分析, 痛点识别, 需求拆解.
when_to_use: "pain point, 痛点拆解, 痛点分析, 痛点识别, 拆解痛点, decompose pain, 功能点拆解, MVP 路径"
triggers:
  - /pain-decomposition
  - /pain-decompose
  - pain point
  - painpoint
  - pain point decomposition
  - decompose pain
  - 痛点拆解
  - 痛点分解
  - 痛点识别
  - 痛点分析
  - 拆解痛点
  - 分析痛点
  - 需求拆解
  - 功能点拆解
  - MVP 路径
dispatch_intent: "Read pain description → summarize core pain → POS split (noun/verb/adj-adv) → derive metrics+schema, flow, latent requirements → roll up to Features + MVP launch path → write to docs/painpoint-<slug>.md (Chinese output)"
---

# Pain Decomposition: Pain Identification and Decomposition

🥷 Turn a fuzzy pain description into: **metrics + data schema + flow + latent requirements + Features + MVP launch path**.

> **Note**: All output in `docs/painpoint-*.md` is written in Chinese. This SKILL.md (the prompt itself) is in English to align with the rest of the toolkit. Trigger words support both English and Chinese.

## When to Use

- User interview transcripts, support tickets, or sales feedback are still unstructured text.
- You want to reverse-engineer pain points into: what to measure, what fields to model, what flows to draw, and what latent needs to cover.
- Before entering `/planning` or `/pre-mortem`, to flatten a fuzzy problem space first.

**When NOT to use**:

- Already-structured PRD / RFC → go directly to `/planning`.
- Pure technical selection / architecture evaluation → use `/zoom-out` or `/planning`.
- Already have an issue backlog that needs ranking → use `/rice`.

## Core Idea

In a pain description, **parts of speech are themselves analytical signals**:

| POS | Role in the pain | Derived output |
|------|----------------|----------------|
| **Noun** | Entity — who, what thing | Core metrics + data schema (entity tables + fields) |
| **Verb** | Action — what is done, in what order | Business flow (happy path + sad path + branches) |
| **Adjective / Adverb** | Rules — under what condition, to what extent, in what scenario | Latent requirements, edge scenarios, non-functional requirements |
| **All three rolled up** | Synthesis | **Features + MVP launch path** |

This correspondence runs through the entire skill: **section 2 splits it out → sections 3-5 trace back → section 7 rolls up into deliverables**. Every derivative must point back to a specific word in section 2.

## Workflow

### 1. Receive Input

Determine in this order:

1. **File path** (e.g., `./interview.md`, `/abs/path/feedback.txt`) → use the `Read` tool to get the full text.
2. **Free text** (pain description given directly in the chat) → use as-is.
3. **Mixed content** (meeting notes, ticket collections, user stories) → extract the pain-related paragraphs; ignore chit-chat.
4. **Short or vague input** — ask follow-up questions if ANY of these is true:
   - Total length < 50 chars
   - Only vague emotion words ("slow", "laggy", "hard to use", "卡", "慢", "难用")
   - After extracting the core pain in step 2, one or more of the four elements (who / scenario / cause / consequence) is missing
   
   Use `AskUserQuestion` for 2-3 highest-leverage questions: who hurts? how long? how do they cope today? what's the blast radius? Then loop back to step 2.

### 2. Identify the Core Pain (Pain Summary)

Compress the input into **1-sentence core pain + 3-5 pain branches**:

```
Core pain: <who> in <scenario>, because <cause>, suffers <consequence>.
```

Key points:

- **Do NOT include a solution** — only describe the problem.
- The four elements (who + scenario + cause + consequence) — if any is missing, ask or explicitly mark "to clarify" in the output.
- If the input contains **multiple independent pains** (multiple tickets / multiple feedback items), decompose each one separately, using sub-headings `## Pain A` / `## Pain B`. Features are then listed **per-pain** (each Feature carries a `pain trace` back to its parent pain), and the MVP launch path **crosses pains by P0 severity** (P0s from all pains go into Phase 1; P1s in Phase 2; etc.).

### 3. POS Decomposition

**This is the heart of the skill** — strictly split by parts of speech.

#### 3.1 Nouns (Entities)

List every noun that appears in the core pain + pain branches. One per row, judge:

- **Role**: subject (who) or object (what)?
- **State**: persistent entity (user, order, product) or transient context (cart, session, message)?
- **Granularity**: core entity or peripheral entity?

**Keep only business-core entities (≤ 7)**. Counting "every field as an entity" will explode metrics and schema downstream.

#### 3.2 Verbs (Actions)

List every verb. One per row, judge:

- **Direction**: forward (create / confirm) or backward (cancel / refund)?
- **Trigger**: user-initiated or system-driven?
- **End state**: after the action completes, how does the entity's state change?

**Sort verbs by time order** — the verb chain is the flow skeleton.

#### 3.3 Adjectives / Adverbs (Rules)

List all qualifier words: adjectives (fast, expensive, hard), adverbs (immediately, batch, concurrent), numerals (100ms, 99.9%), scenario words (peak hours, overseas, new user).

For each Rule, label:

- **Constraint target**: which entity or action does it limit?
- **Implicit condition**: what happens if we remove this Rule?

This step is the seed library for "latent requirements" — much product differentiation ("real-time", "batch", "offline") hides in here.

### 4. Noun Derivatives: Core Metrics + Data Schema

#### 4.1 Core Metrics

Derive "what to observe" from entities. At least 1-2 metrics per core entity.

| Metric type | Meaning | Example |
|-------------|---------|---------|
| **Reach** | how many people / how much volume is affected | DAU, order volume, SKU count |
| **Quality** | how well it works | conversion rate, retention, complaint rate |
| **Latency** | how fast it works | checkout time, payment time, refund duration |

Each metric must be labeled with **calculation method + measurement frequency + business meaning**. For each one, ask: "**If this metric suddenly doubled or halved, what is the first reaction of the business owner?**" If you can't answer, the metric is meaningless.

#### 4.2 Data Schema

Render core entities as a schema (YAML or TypeScript interface). Key points:

- Only list **core fields** — don't list 30+. Too many fields means granularity is wrong; go back to 3.1.
- Transient entities (Cart / Session / Token) are labeled separately — they **imply TTL / GC / cleanup logic**.
- Relationships use references (`ref(User)`), not nested expansion.

### 5. Verb Derivatives: Business Flow

Convert the verb chain into a flow.

#### 5.1 Happy Path

String the verbs in time order; each action = one step. Recommended: mermaid or numbered steps:

```mermaid
flowchart LR
  A[浏览商品] --> B[加入购物车] --> C[提交订单] --> D[支付] --> E[发货]
```

#### 5.2 Sad Path

For **each step** of the happy path, ask inversely: "What if this step fails / interrupts / times out?". Each failure point corresponds to one sad-path entry:

| Trigger point | Failure scenario | System response |
|----------------|------------------|-----------------|
| Stock check | Insufficient stock | Notify user + release cart |
| Payment | Timeout | Auto-cancel order + notify user |
| Logistics | Lost package | Trigger refund + compensate user |

#### 5.3 Decision Branches

Turn "branch condition" Rules from 3.3 into if/else: `if peak-hours → enable fast lane`, `if VIP → manual review`.

### 6. Adjective / Adverb Derivatives: Latent Requirements

Look at the Rules from 3.3 **in reverse**: each Rule implies a latent requirement.

#### 6.1 Implicit Constraints

For each adjective / adverb ask: "**What happens if we remove it?**"

- "real-time notification" → implies push capability, message queue, reconnection logic
- "no lag in peak hours" → implies rate limiting, graceful degradation, load testing
- "new users can use it" → implies onboarding flow, tooltips

#### 6.2 Edge Scenarios

Extract boundaries from numerals + scenario words:

- "respond within 100ms" → boundary is 100ms; monitor P95 / P99
- "overseas users" → boundary is multi-language, multi-currency, compliance
- "run batch at dawn" → boundary is low-traffic window, avoid disturbing users

#### 6.3 Non-Functional Requirements

Group into categories:

- **Performance**: QPS / latency / throughput
- **Availability**: SLA (99.9% / 99.99%)
- **Security**: permissions, encryption, audit
- **Compliance**: GDPR / 等保 / industry regulations
- **Observability**: logs / metrics / alerts

### 7. Synthesis: Features + MVP Launch Path

Roll up all artifacts from sections 1-6 to answer two questions: "**What Features should we build?**" and "**What order should we build them in?**"

#### 7.1 Feature Decomposition

Reverse from pain: every pain corresponds to "if I had Feature X, would this be solved?". **Each Feature is an independently-deliverable capability unit**, not an Issue and not a User Story. Name Features with **verb-object structure** ("用户管理", "接入支付", "消息推送" — Chinese verb-object).

**Derivation paths** — each Feature must have ≥ 1 source:

| Pattern | Example |
|---------|---------|
| **Noun + Verb** | noun "user" + verb "manage" → 「用户管理」 |
| **Noun + Rule** | noun "user" + rule "VIP" → 「用户分层」 |
| **Verb + Rule** | verb "checkout" + rule "peak hours" → 「高峰期快速通道」 |
| **Sad path** | sad path "payment timeout" → 「订单自动取消」 |
| **Latent need** | latent need "real-time notification" → 「消息推送」 |
| **Flow node** | happy path "validate stock" → 「库存校验服务」 |
| **Composite sources** | Feature derived from a combination of multiple discoveries (e.g., flow node + sad path + latent need combined) | write explicit derivation rationale in section 9 |

If a Feature does not fit any of the 7 patterns, do not invent a derivation — flag the Feature in section 9 as "needs derivation rationale" and either justify it or cut it.

**Feature card** (mandatory fields per Feature):

| Field | Meaning | Trace back to |
|-------|---------|---------------|
| **ID** | F-001 / F-002 ... | unique, referenced by ID elsewhere |
| **Name** | verb-object structure | — |
| **Description** | one sentence: what the user can do / what capability the system provides | — |
| **Pain trace** | Pain X / section X | → 1.x |
| **POS trace** | noun "X" + verb "Y" [+ rule "Z" if applicable] | → 2.x |
| **Entity deps** | which entities are needed (section 4.2) | → 4.2 |
| **Feature deps** | which F-XXX it depends on | chain |
| **Priority** | P0 / P1 / P2 | see 7.2 |
| **Validation metric** | which metric changes (section 4.1) | → 4.1 |

**Feature count guidance** (count inflation signals wrong granularity; defaults can be exceeded with rationale logged in section 9):

- Single pain → 3-8 Features
- Multiple pains → ≤ 5 per pain, ≤ 15 total. Features are listed per-pain (each Feature carries a `pain trace` back to its parent pain).
- Over this → either go back to section 3 and re-split entities / verbs, or keep the overage and document the rationale.

#### 7.2 MVP Launch Path

Order Features into a phased path by **P0/P1/P2 + dependency**. For multi-pain input, the path **crosses pains by severity**: all P0 Features from any pain go into Phase 1, P1 in Phase 2, P2 in Phase 3 — regardless of which pain they came from.

**Priority determination** — combine three dimensions:

1. **Pain severity**: does it block the core scenario? is it high-frequency? does it happen daily?
2. **Reach**: how many users / how much order volume is affected? share of DAU?
3. **Dependency complexity**: can it ship independently? how many prerequisite Features?

**Rules**:

- **P0 (must do first)**: blocks core scenario + large reach + shippable independently or with low deps. **Without it, no launch**.
- **P1 (enhancement)**: solves experience issues / covers edge scenarios / partially depends on P0. **Fill in within 1-2 iterations after launch**.
- **P2 (nice-to-have)**: addresses latent needs / fallback scenarios / experience polish. **Only schedule if resources allow**.

**Default to three phases**. If more than 3 are genuinely needed, that is a signal P2 wasn't cut hard enough — either trim P2, or merge phases and explicitly note the overage rationale in section 9.

```markdown
### Phase 1: MVP (suggest 4-6 weeks)
- **Goal**: validate the minimum closed loop — the core pain can be solved
- **Included Features**: F-001, F-002, F-003
- **Rationale**: all P0, independently shippable or low-dep; covers Pain X, Y
- **Validation metric** (from 4.1): core funnel conversion ≥ X%, DAU ≥ X
- **Exit condition**: core pain-branch metrics are stable — e.g., P95 latency fluctuates < 5% across 2 consecutive weeks, or retention rate has no significant change for 2 weeks

### Phase 2: Enhancement (suggest +4 weeks)
- **Goal**: cover P1 pains + edge scenarios
- **Included Features**: F-004, F-005
- **Rationale**: depends on Phase 1 F-001; covers Pain Z
- **Validation metric**: retention ≥ X%, complaint rate ≤ X%
- **Exit condition**: P1 pain-branch metrics improve ≥ 20%

### Phase 3: Polish (suggest +6 weeks)
- **Goal**: P2 fallback + nice-to-haves
- **Included Features**: F-006, F-007, F-008
- **Rationale**: address latent requirements, raise experience ceiling
- **Validation metric**: NPS ≥ X, SLA achievement ≥ 99.9%
- **Exit condition**: all pain branches covered
```

**Phase durations are just reference** — what really determines "enter next phase" is **whether all P0 are done + validation metrics are met**, not the calendar.

### 8. Output: Write to docs/painpoint-<slug>.md

Output file path:

```
docs/painpoint-<slug>.md
```

`<slug>` is a kebab-case keyword (≤ 4 words) extracted from the core pain. Examples:

- `docs/painpoint-checkout-slow.md`
- `docs/painpoint-refund-friction.md`
- `docs/painpoint-onboarding-drop.md`

**File versioning policy**:

- **Default**: if a file with the same name exists, append a date suffix `docs/painpoint-<slug>-YYYY-MM-DD.md` (creates a snapshot; old version is preserved).
- **Overwrite**: if the user explicitly says "overwrite", "update", "rewrite", or "覆盖" / "更新", replace the existing file in place.
- **Ask**: if intent is ambiguous (e.g., user says "re-run" without specifying), ask the user once before writing.

Confirm `docs/` exists before writing; if not, `mkdir -p docs`.

**Output language: Chinese**. The output document is written entirely in Chinese (with English proper nouns preserved: API names, library names, product names).

### 9. Output Template

```markdown
# 痛点拆解：<Title>

> 核心痛点（一句话）：<谁> 在 <场景> 下，因为 <原因>，导致 <后果>。
>
> 来源：<文件路径 or 对话输入> ｜ 拆解时间：<YYYY-MM-DD>

## 1. 痛点分支

- 痛点 A: <一句话>
- 痛点 B: <一句话>
- 痛点 C: <一句话>

## 2. 词性拆解

### 2.1 名词（Entities）
| 实体 | 含义 | 角色 | 状态 |
|------|------|------|------|
| ... | ... | 主体 / 客体 | 持久 / 临时 |

### 2.2 动词（Actions）
| 动作 | 触发 | 终结状态 | 时序 |
|------|------|----------|------|
| ... | 用户主动 / 系统被动 | ... | #1 |

### 2.3 形容词 / 副词（Rules）
| 限定词 | 含义 | 限定对象 |
|--------|------|----------|
| ... | ... | ... |

## 3. 名词衍生：核心指标 & 数据结构

### 3.1 核心指标
| 指标 | 计算方式 | 业务意义 | 度量频率 |
|------|----------|----------|----------|
| ... | ... | ... | 日 / 周 / 月 |

### 3.2 数据结构
\`\`\`yaml
EntityName:
  field: type              # 字段说明
  ...

RelatedEntity:
  field: ref(EntityName)
  ...
\`\`\`

## 4. 动词衍生：业务流程

### 4.1 主流程
\`\`\`mermaid
flowchart LR
  A[动作 1] --> B[动作 2] --> C[动作 3]
\`\`\`

### 4.2 异常流程
| 触发点 | 失败场景 | 系统响应 |
|--------|----------|----------|
| ... | ... | ... |

### 4.3 决策分支
- `if <规则>` → `<分支动作>`

## 5. 形容词 / 副词衍生：潜在需求

### 5.1 隐含约束
- ...

### 5.2 边界场景
- ...

### 5.3 非功能性需求
- **性能**: ...
- **可用性**: ...
- **安全 / 合规**: ...
- **可观测**: ...

## 6. 功能点拆解（Features）

### F-001: <动宾结构>
| 字段 | 内容 |
|------|------|
| **功能描述** | <一句话> |
| **痛点溯源** | 痛点 X / 第 X 节 |
| **词性溯源** | 名词"X" + 动词"Y" + 规则"Z" |
| **依赖实体** | ...（回 3.2） |
| **依赖功能** | F-XXX（无则填"无"） |
| **优先级** | P0 / P1 / P2 |
| **验证指标** | 指标名（回 3.1） |

### F-002: <动宾结构>
| 字段 | 内容 |
|------|------|
| ... | ... |

### F-003: ...

## 7. MVP 启动路径

### Phase 1: MVP（建议 4-6 周）
- **目标**：<一句话>
- **包含功能**：F-001, F-002, F-003
- **理由**：<为什么是这个顺序>
- **验证指标**：<回 3.1>
- **退出条件**：<具体可观测的阈值>

### Phase 2: 增强（建议 +4 周）
- **目标**：...
- **包含功能**：F-004, F-005
- **理由**：...
- **验证指标**：...
- **退出条件**：...

### Phase 3: 完善（建议 +6 周）
- **目标**：...
- **包含功能**：F-006, F-007, F-008
- **理由**：...
- **验证指标**：...
- **退出条件**：...

## 8. 衍生 Issue 建议

- [ ] Issue: <标题>（源自：第 X 章 / Feature F-XXX / 第 Y 节 / 某个指标或流程节点）
- [ ] ...

## 9. 待澄清

- 含义不清的名词 / 边界模糊的动词 / 歧义大的限定词 / 优先级待确认的 Feature。

> Next step:
> - 把第 6 章 Feature 用 `/rice` 排 P0/P1/P2 优先级 + Effort 估时，砍掉不进 MVP 的。
> - 对单个 P0 Feature 用 `/planning` 写实现方案。
> - 整体路径用 `/pre-mortem` 做风险扫描。
```

## Constraints (do not violate)

- **Never give a technical implementation approach** ("use Redis for caching", "add Kafka") — that's `/planning`'s job.
- **MVP phase ordering IS allowed** — it's a product-level answer to "what Features first", not a technical solution.
- **Never omit the three 2.x POS sections** — they are the core value of the skill.
- **Every Feature must have a trace** — pain / POS / entity / metric, must pick ≥ 1 to exist. Features that appear out of nowhere get cut.
- **Do NOT pile metrics / fields / Features**. Each derivative must trace back to a word in 2.x.
- **P0 ideally ≤ 5**. If a pain genuinely requires more P0s, justify each one in section 9 (Why each P0 is mandatory). Otherwise demote the rest to P1 / P2.
- **Do NOT paste the whole document back into chat** — only reply with: path + one-sentence core pain + Next step.
- **Output language**: the document written to `docs/painpoint-*.md` is in Chinese by default. Preserve English proper nouns (API names, library names, product names). If the user explicitly requests English output (e.g., "用英文产出", "for the US team"), produce the document in English instead — same structure, just translated.

## Pro Tips

- **Adjectives / adverbs are the most underrated part** — list more, not less. Most product differentiation hides here.
- **Draw the verb chain twice**: once for happy path, once for sad path. Drawing them separately reveals failure modes.
- **Mark "transient entities" in the data schema** (Cart, Session, Token) — they imply TTL / GC / cleanup logic.
- **Metric reverse-test**: after writing each metric, ask "if this metric suddenly doubled / halved, what's the business owner's first reaction?" — no answer means the metric is meaningless.
- **Feature reverse-test** — three questions per Feature:
  1. "**Without this Feature, does the pain still hold?**" Yes → cut.
  2. "**Which pain in 1.x does this Feature solve?**" Mismatch → re-classify.
  3. "**Which metric in 4.1 does this Feature's validation metric trace to?**" Mismatch → validation metric is wrong.
- **MVP cut hard**: once P0 exceeds 5, force re-evaluation — either merge Features, or cut non-core scenarios. MVP's purpose is "validate first, then expand", not "do everything".
- **Check Open Questions at the end**: nouns with unclear meaning, verbs with fuzzy boundaries, qualifiers with large ambiguity, Features with unconfirmed priority — list separately in section 9.
- **Chained invocation**:

```
/pain-decomposition <pain.md>
    ↓
/rice <docs/painpoint-*.md>          # rank Features / metrics / needs by RICE
    ↓
/planning <P0-feature>               # write implementation plan for one P0 Feature
    ↓
/pre-mortem <plan-file>              # risk scan
```

## Output Convention

- First line inline prefix: `🥷`
- After writing the file, the reply contains only: file path + one-sentence core pain + Next step. **Do NOT paste the entire document back into chat**.

## When to Use (recap)

- After user interviews, when landing is needed
- Customer support ticket aggregate analysis
- Sales / CS feedback consolidation
- Pre-PRD requirement exploration
- Pre-POC problem-space flattening for new directions
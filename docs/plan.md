# Skill System Design

## Context

需要设计一个可插拔的 skill 系统，让 AI agent 能够根据用户需求动态加载不同的技能模块。每个 skill 是独立的、功能单一的、可组合的。

## Problem

如何实现一个 skill 系统，支持：
1. 每个 skill 独立打包，自包含指令和脚本
2. 用户可选择性地添加/移除 skill
3. AI 能根据 description 自动判断何时触发哪个 skill
4. 多个 skill 共享配置（如 issue tracker、标签词汇等）

## Solution

### 1. 目录结构

```
project/
├── skills/                    # 所有 skills 的根目录
│   ├── [category]/           # 按用途分类
│   │   ├── skill-a/
│   │   │   ├── SKILL.md     # 必需：主指令文件
│   │   │   ├── README.md    # 可选：分类说明
│   │   │   ├── REF-*.md     # 可选：参考文档
│   │   │   └── scripts/     # 可选：辅助脚本
│   │   └── skill-b/
│   │       └── ...
├── docs/
│   └── agents/              # 共享配置文件
│       ├── issue-tracker.md
│       ├── triage-labels.md
│       └── domain.md
└── .claude-plugin/
    └── plugin.json          # Skill 注册表
```

### 2. SKILL.md 格式

```yaml
---
name: skill-name
description: >
  一句话功能描述. Use when [触发条件关键词列表].
---

# Skill Name

## 快速开始
[最小可用示例]

## 工作流
[分步骤说明]

## 高级用法
[参考其他文档]
```

**description 是 AI 选择的核心**：
- 第一句：功能概述
- 第二句：触发条件（用户说了什么/什么情况下调用）

### 3. plugin.json 注册机制

```json
{
  "name": "my-skills",
  "skills": [
    "./skills/engineering/skill-a",
    "./skills/engineering/skill-b",
    "./skills/productivity/skill-c"
  ]
}
```

**选择添加 = 增删数组元素**：
- 添加 skill：加入路径到数组
- 移除 skill：从数组删除路径

### 4. 分类隔离

| 目录 | 出现在 README | 说明 |
|------|--------------|------|
| `engineering/` | ✅ | 工程相关 skills |
| `productivity/` | ✅ | 通用工作流 |
| `misc/` | ✅ | 临时/保留 |
| `personal/` | ❌ | 个人专用 |
| `deprecated/` | ❌ | 已废弃 |

### 5. 共享配置模式

需要多 skill 协作时：
1. 用 `setup-*` skill 生成 `docs/agents/*.md`
2. 其他 skill 读取这些文件获取上下文
3. 通过文件名约定（`issue-tracker.md`、`triage-labels.md`）实现松耦合

### 6. Skill 命名约定

- 目录名 = skill 名（小写、连字符）
- 触发方式：`/skill-name` 或自然语言描述
- description 中列出所有触发关键词

## Consequences

**优点**：
- 最小化耦合：skill 间通过文件约定通信，不直接依赖
- 可插拔：plugin.json 控制加载哪些 skill
- 可组合：多个 skills 可以协作（如 setup + 业务 skill）
- AI 自动选择：description 驱动，无需硬编码

**缺点**：
- 共享配置需要约定文件名，存在隐式耦合
- skill 删除后残留配置文档需手动清理

## Pre-mortem

### Risks

| Risk | Likelihood | Impact | Severity |
|------|------------|--------|----------|
| description 写得不好，AI 选错 skill | High | Medium | **High** |
| 多 skill 同时触发，AI 选错优先级 | Medium | Medium | **Medium** |
| 共享配置文件被误删/改名，相关 skill 失效 | Low | High | **Medium** |
| setup skill 生成的配置无法覆盖 edge case | Medium | Low | **Low** |
| skill 数量膨胀，plugin.json 难以维护 | Medium | Low | **Low** |

### Mitigations

| Risk | Mitigation |
|------|------------|
| description 写得不好 | 编写 SKILL.md 时必须包含 "Use when..." 触发条件；review checklist 检查 description 完整性 |
| 选错优先级 | description 精确区分场景；复杂场景拆成独立 skill |
| 配置失效 | 约定配置文件名 + 文档说明；setup skill 提供一致性检查 |
| edge case 无法覆盖 | setup skill 支持 "Other" 选项，允许用户自定义 workflow |
| plugin.json 膨胀 | 按 category 分组；超过 20 个 skill 时考虑拆分成多个 plugin |

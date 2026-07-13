# Skill Collection 架构设计文档

本文档描述 Skill Collection（技能集合）的通用架构。以 [Waza](https://github.com/tw93/Waza) 为具体实例。

---

## 1. 核心概念

**Skill Collection** = 一组可被 AI agent 调用的专项技能，工作流导向，每个技能负责一类任务。

与单一通用工具的区别：技能有判断能力，能根据上下文决定下一步；脚本只做确定性操作。

| 组件 | 作用 |
|------|------|
| **Skill** | Markdown 工作流，含判断逻辑、模式匹配、输出规范 |
| **Rule** | 跨技能共享的行为约束（anti-pattern、写作规范等） |
| **Resolver** | 触发词到技能的路由表 |
| **Dispatcher** | 实际执行分发的入口文件 |

---

## 2. 目录结构

```
{project}/
├── VERSION                     # 版本号（单点真实来源）
├── packaging.allowlist         # 打包白名单（默认拒绝）
├── Makefile                    # 构建/测试/打包入口
│
├── skills/                     # 技能定义（源文件）
│   ├── RESOLVER.md             # 人工可读的路由表
│   ├── {skill}/SKILL.md       # 单个技能入口
│   └── {skill}/
│       ├── agents/             # 专家评审提示词（可选）
│       ├── references/         # 参考文档（可选）
│       └── scripts/            # 确定性辅助脚本（可选）
│
├── rules/                      # 共享行为规则
│   ├── anti-patterns.md       # 跨技能 AI 行为红线
│   ├── durable-context.md      # 内存上下文 preamble（可选）
│   └── {lang}.md              # 写作规范（可选）
│
├── scripts/                    # 构建/验证脚本
│   ├── build_metadata.py      # codegen 驱动
│   ├── verify_skills.py       # 验证入口
│   └── dispatcher-template.md  # 分发器模板
│
├── .claude-plugin/            # 【生成】Marketplace 元数据
├── .github/workflows/          # CI/CD
└── tests/                      # 冒烟测试
```

---

## 3. 技能设计规范

### 3.1 每个技能的结构

```
SKILL.md frontmatter:
---
name: {skill}
description: 一句话描述（用于自动路由匹配）
metadata.version: {version}
---

# Skill Name

🥷 一句话 tagline

## Outcome Contract
做什么、什么算完成、输出什么格式

## Durable Context Preflight   # 可选
引用 memory 中的上下文

## Modes
不同场景下的分支

## Hard Rules
必须遵守的约束

## Gotchas
常见坑点

## Output
输出格式说明
```

### 3.2 触发路由设计

技能通过**触发词**匹配用户意图。触发词分两类：

| 类型 | 描述 | 示例 |
|------|------|------|
| **阶段触发** | 按工作流阶段分路 | Pre-build（设计）、Post-build（review）、Diagnostic（debug） |
| **意图触发** | 按具体操作分路 | 报错→hunt、review→check、URL→read |

### 3.3 消歧规则

多技能可能同时匹配时，按以下顺序消歧：

1. **最具体优先** — 具体任务词优先于泛化词
2. **内容类型二次分流** — 如 URL 后接研究意图则 chain to learn
3. **错误状态判断** — 代码已交付 vs 代码异常
4. **上下文类型判断** — 配置问题 vs 代码错误
5. **动作 vs 结果** — 执行发布 vs 写发布文案
6. **审美 vs 回归** — 视觉投诉 vs 功能回退
7. **从零 vs 润色** — 新建 vs 改稿
8. **兜底** — 读双方的 "Not for" 排除

---

## 4. 版本管理

**单点真实来源**：`VERSION` 文件（不含引号的一行字符串，如 `3.31.2`）

所有涉及版本的地方都从这读取：
- Marketplace 元数据
- 安装器默认值
- 更新检查器本地版本
- npm package.json

**版本号规范**：`v{version}`（release tag），如 `v3.31.2`

---

## 5. 构建/再生系统

### 5.1 Codegen 驱动

```
scripts/build_metadata.py
    读取 VERSION + SKILL.md frontmatter
    生成 marketplace.json、README、dispatcher.md、installer defaults
```

**两种模式**：
- `--write`（默认）：重写所有生成文件
- `--check`：与已提交文件比较，漂移则报错（CI 用）

### 5.2 典型生成文件

| 文件 | 说明 |
|------|------|
| `marketplace.json` | 各平台的插件市场元数据 |
| `README.md` | 安装 URL 指向 release assets |
| `dispatcher.md` | 从 frontmatter 生成的路由分发器 |
| `scripts/check-update.sh` | 含 LOCAL_VERSION 的更新检查 |
| `skills/*/references/durable-context.md` | 共享 preamble 的技能本地副本 |

### 5.3 验证层

- `scripts/verify_skills.py` — frontmatter 校验、链接校验、路由表一致性
- `make verify-generated` — codegen 漂移检测
- `scripts/check_routing_drift.py` — RESOLVER.md 和 dispatcher.md 同步检测

---

## 6. 打包与分发

### 6.1 分发路径

通常 3 条路径：

| 路径 | 目标用户 | 产物 |
|------|---------|------|
| `npx skills add {owner}/{repo}` | Claude Code / Codex / Cursor | skills 目录 |
| `/plugin marketplace add {name}` | Claude Code 插件市场 | marketplace.json |
| 手动上传 zip | Claude Desktop | `project.zip` |

### 6.2 打包原则

- **默认拒绝**：`packaging.allowlist` 是显式发货清单，清单外均排除
- **单一入口**：zip 包生成单一根 `SKILL.md`，内联所有技能内容
- **完整性校验**：打包后运行校验脚本确认内容完整

### 6.3 平台差异处理

不同 AI 平台有不同的安装格式和目录结构，需要生成对应镜像：

```
plugins/{name}/              # Codex 插件镜像
  .codex-plugin/plugin.json  # Codex 插件清单
  skills/                    # 技能目录镜像
  rules/                    # 规则目录镜像
```

---

## 7. 规则系统

### 7.1 跨技能规则

`rules/anti-patterns.md` 定义所有技能共享的行为红线。

格式：`| # | Pattern | Wrong | Right |`

| 典型类别 | 说明 |
|---------|------|
| 执行前必读 | 不读完就动手 |
| 路径幻觉 | 未确认文件存在就引用 |
| 过度执行 | 超出请求范围添加功能 |
| 隐式授权升级 | 用户说"ok"就执行危险操作 |
| 外部内容信任 | 把抓取的网页当指令来源 |

### 7.2 写作规范

语言特定的写作规则（如 `rules/english.md`、`rules/chinese.md`），控制输出风格一致性。

---

## 8. 测试策略

### 8.1 冒烟测试

每个独立表面配一个冒烟测试，Makefile 自动发现：

```make
smoke-%:
    tests/test_*.sh   # 每个文件一个 target
```

共享工具在 `tests/test_helpers.sh`，提供 tmpdir / repo-copy / stub-curl 工厂。

### 8.2 冒烟覆盖范围

| 表面 | 验证内容 |
|------|---------|
| 技能发现 | 每个 skill 目录可读 |
| 路由解析 | RESOLVER.md 与 dispatcher.md 一致 |
| 安装器 | 脚本在干净环境可执行 |
| 打包 | zip 内容完整性 |
| 网络 | 可访问的外部 URL 可抓取 |

---

## 9. 安装器设计

| 脚本 | 目标平台 | 关键设计 |
|------|---------|---------|
| `setup-rule.sh` | Claude Code + Codex | 使用 HTML 注释标记实现幂等重跑 |
| `setup-statusline.sh` | Claude Code | 覆盖前需用户确认 |
| `check-update.sh` | 所有 | 每日最多一次、只读公开文件、不发数据 |

---

## 10. 架构模式总结

| 模式 | 说明 |
|------|------|
| **Fat Skill / Thin Script** | 技能管判断，脚本管执行 |
| **Default-Deny Packaging** | 白名单控制发货内容 |
| **Single Source of Truth** | VERSION + frontmatter 是唯一来源 |
| **Codegen Over Drift** | 多份元数据从单一来源生成 |
| **Idempotent Installers** | 使用标记实现安全重跑 |
| **Auto-Discovered Tests** | Makefile wildcard 自动发现冒烟 |
| **Non-Blocking Update** | 更新检查不影响主流程 |
| **Separation of Concerns** | 验证、codegen、打包、路由各自独立 |

---

## 11. 关键文件索引

| 文件 | 作用 |
|------|------|
| `VERSION` | 版本单点来源 |
| `skills/RESOLVER.md` | 路由表入口 |
| `skills/*/SKILL.md` | 技能定义 |
| `rules/anti-patterns.md` | 跨技能红线 |
| `scripts/build_metadata.py` | codegen 源头 |
| `scripts/verify_skills.py` | 验证入口 |
| `packaging.allowlist` | 打包白名单 |
| `Makefile` | 构建入口 |

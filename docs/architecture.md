# Zack Skills 架构

工程工作流 skill 工具集,面向 Claude Code。当前版本 `VERSION` = 1.9.1。

## 核心原则

- **单源真相 (SSOT)**: 根目录的 `VERSION` 文件驱动所有生成物 — marketplace 元数据、npm 包版本、Codex 镜像、dispatcher 表、每个 skill 的 update check。
- **frontmatter 驱动 dispatch**: 每个 skill 是带 YAML frontmatter 的 Markdown,`description` / `when_to_use` / `dispatch_intent` 决定路由与触发词。
- **源码 vs 生成物分离**: 根目录的 `SKILL.md` / `dispatcher.md` / `.claude-plugin/plugin.json` 都不是手写的,而是由 `scripts/build_metadata.py` 从 `skills/` 下重建。

## Skill 清单 (10 个)

按目录分组:

| 分类 | Skill | 用途 |
|---|---|---|
| `engineering/` | `check` | 代码审查 (diff / PR / commit / 项目质量打分) |
| `engineering/` | `health` | Agent 配置漂移审计 (CLAUDE.md / hooks / MCP / AI 可维护性) |
| `engineering/` | `diagnose` | 调试诊断循环:reproduce → minimise → hypothesise → instrument → fix → regression-test |
| `engineering/` | `post-mortem` | 复盘已完成工作,查找逻辑错误与实现漏洞 |
| `engineering/` | `pre-mortem` | 想象灾难性失败,反向推导风险与缓解 |
| `engineering/` | `rice` | RICE 框架打分排序任务 |
| `engineering/` | `zoom-out` | 探索代码库架构,绘制模块关系图 |
| `engineering/` | `setup-zack-skills` | 首次仓库引导:把 issue tracker / triage label / 域文档布局写入 AGENTS.md |
| `productivity/` | `caveman` | 极简通信模式,去除填充词保留技术精度 |
| `productivity/` | `markdown-to-itmz` | Markdown → iThoughts 思维导图 (.itmz) |

入口文件全部是 `skills/<category>/<name>/SKILL.md`。

## 安装路径

三种安装方式并列存在:

1. **skills-cli (npm,推荐)**: `npx skills add https://github.com/canwhite/zack-skills -g`
2. **Claude Code plugin**: `/plugin marketplace add zack-skills` + `/plugin install zack-skills@zack-skills`
3. **CLI 直调 (local clone)**: `git clone` 后 `python3 cli.py <list|init|add|remove>` — 需手动 clone

## 构建 / 校验链

`Makefile` 暴露 4 个 target:

| Target | 作用 |
|---|---|
| `make test` | 跑 `verify-docs` (frontmatter 校验) + `verify-scripts` (语法/lint/diff check) |
| `make verify-generated` | CI 用:校验生成物是否与源码漂离 |
| `make regenerate` | 跑 `scripts/build_metadata.py` 重建所有生成物 |
| — (隐式) | `verify-scripts` 还跑 `python3 -m py_compile` 对所有 Python 脚本做语法检查 |

**scripts/ 目录职责**:

| 脚本 | 角色 |
|---|---|
| `verify_skills.py` | frontmatter 合规性校验 |
| `build_metadata.py` | 从 `skills/` 源生成根目录产物 |
| `skill_frontmatter.py` | 共享 frontmatter 解析库 |
| `check-update.sh` | 远程版本检查 (`VERSION` 比对) |
| `link-skills.sh` | 本地软链 skill 到 `~/.claude/skills/` (Makefile 未暴露) |

## CLI (`cli.py`)

Python argparse 工具,管理 `.claude-plugin/plugin.json` 中的 skill 注册表。4 个子命令:

- `list` — 列出可用 + 已安装 skill,带 ✓/○ 标记
- `init` — 把 `skills/` 下所有 skill 一次性写入 plugin.json
- `add <name>` / `remove <name>` — 增删单 skill

**当前局限**: `cli.py` 未进 `package.json` 的 `files` 数组,npm 用户拿不到;无 `pyproject.toml`,未发 pip。

## 已知缺口

- `cli.py` 与 npm 包脱节 — npm 安装路径下用户拿不到 CLI
- `scripts/link-skills.sh` 没有 Makefile target,需要手动调用
- `setup-zack-skills` 依赖 `docs/agents/` 布局,首次安装需手动触发才能让其他 skill 拿到 repo 上下文

## 目录结构

```
zack-skills/
├── VERSION                     # SSOT,所有产物版本号来源
├── SKILL.md                    # 生成:总入口 + 路由表
├── cli.py                      # 本地 CLI 工具
├── package.json                # npm 包元数据 + pi.skills 注册
├── Makefile                    # test / regenerate / verify-generated
├── README.md                   # 用户文档
├── docs/                       # 架构与计划文档
├── scripts/                    # build/verify/parse 脚本
├── skills/
│   ├── engineering/<skill>/SKILL.md    # 8 个工程 skill
│   ├── productivity/<skill>/SKILL.md   # 2 个效率 skill
│   ├── deprecated/                     # 归档 skill
│   ├── misc/                           # 杂项
│   ├── personal/                       # 个人专用
│   └── RESOLVER.md                     # 路由解析说明
└── .claude-plugin/plugin.json  # 生成:plugin 注册表
```
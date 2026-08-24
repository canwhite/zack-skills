# Skill 安装渠道速查

zack-skills 提供 **6 个独立渠道**让用户安装 skill。可以混用，但渠道之间**不自动同步状态**——任意一个渠道的更新不会反映到其他渠道。

> 深入机制见 [`install-paths.md`](install-paths.md)（仅覆盖前 3 个主要渠道）。

## 快速对比

| # | 渠道 | 命令 | 来源 | 物理形态 | 全局可见 | 适用场景 |
|---|------|------|------|----------|----------|----------|
| 1 | **NPM skills-cli** | `npx skills add <url> -g` | GitHub 仓库 | 软链接 | ✅ | 终端用户首选，一键装全部 |
| 2 | **Claude Code Marketplace** | `/plugin install zack-<name>` | GitHub 仓库 | 物理拷贝 | ✅ | 按需装单个 skill，版本冻结 |
| 3 | **Codex 镜像** | (平台内自动) | `plugins/zack/` 镜像 | 物理拷贝 | ✅ | Codex 平台用户 |
| 4 | **本地 CLI** | `python3 cli.py add <name>` | 本地 clone | 软链接 | ✅ | 本地开发者调试 |
| 5 | **手动复制** | `cp -r skills/<name> ~/.claude/skills/` | 任意 | 物理文件 | ✅ | 离线 / air-gapped / 自定义部署 |
| 6 | **手动 symlink** | `ln -s <path> ~/.claude/skills/<name>` | 任意 | 软链接 | ✅ | 多版本切换 / 多分支并行 |

## 渠道详解

### ① NPM skills-cli（终端用户推荐）

```bash
npx skills add https://github.com/canwhite/zack-skills -g
```

- 下载整包到 `~/.claude/skills/zack-skills/`
- 触发 `setup.sh` → `scripts/link-skills.sh`，把每个 skill 软链接到 `~/.claude/skills/<name>`
- 一次装全部；重装：`npx skills add -g -f`
- 卸载：`rm -rf ~/.claude/skills/zack-skills`

### ② Claude Code Marketplace（按需安装）

```bash
/plugin marketplace add zack-skills             # 一次性注册源
/plugin marketplace update zack-skills          # 拉新版本
/plugin install zack-pain-decomposition         # 装单个 skill
```

- `marketplace.json` 列出每个 skill 独立条目 + 一个 umbrella
- 安装是物理拷贝到 `~/.claude/plugins/cache/zack-skills/`
- 优势：选择性安装；版本冻结
- 卸载：`/plugin uninstall zack-<name>`

### ③ Codex 镜像

通过 `plugins/zack/.codex-plugin/plugin.json` + `plugins/zack/skills/` 镜像整树分发。

- 单 bundle 模式，`marketplace.json` 只列一个 `zack-skills` plugin
- 通过 `plugins/zack/skills/` 目录镜像整个 `skills/` 树
- 适用：Codex 平台消费者

### ④ 本地 CLI（开发者用）

```bash
python3 cli.py add <name>          # 装单个
python3 cli.py all                 # 装全部缺的
python3 cli.py refresh --sync-global --clear-cache   # 编辑后同步
```

- 源 = 本地仓库 `skills/<category>/<name>`
- 软链接到 `~/.claude/skills/<name>`
- 编辑 `SKILL.md` 后立即生效，无需重装
- 卸载：`rm ~/.claude/skills/<name>`（只删 symlink）

### ⑤ 手动复制

```bash
cp -r skills/engineering/pain-decomposition ~/.claude/skills/
```

- 完全独立，绕过所有自动机制
- 适用：air-gapped 环境 / 离线部署 / 自定义路径

### ⑥ 手动 symlink

```bash
ln -s $(pwd)/skills/engineering/pain-decomposition ~/.claude/skills/pain-decomposition
```

- 类似 `cli.py add`，但绕过 cli 检测
- 适用：本地多版本切换 / 同时维护多个分支

## pain-decomposition 当前覆盖（2026-08-24）

| 渠道 | 状态 | 验证 |
|------|------|------|
| ① NPM | ✅ ready | `make regenerate` → `package.json` 含 v1.9.3 |
| ② Marketplace | ✅ ready | `.claude-plugin/marketplace.json` 含 `zack-pain-decomposition` 条目 |
| ③ Codex | ✅ ready | `plugins/zack/skills/engineering/pain-decomposition/` 已建 |
| ④ 本地 CLI | ✅ linked | `~/.claude/skills/pain-decomposition` → `skills/engineering/pain-decomposition` |
| ⑤ 手动复制 | ✅ ready | 源文件 `skills/engineering/pain-decomposition/SKILL.md` 存在 |
| ⑥ 手动 symlink | ✅ ready | 同 ④，本机 symlink 已建 |

**6/6 全部 ready。** 任意渠道调用即可分发该 skill。

## 关键差异提醒

- **物理形态不同**：①④⑥是软链接（编辑立即生效），②③⑤是物理拷贝（需重新分发才能更新）。
- **同步是单向的**：本地 CLI 改了 SKILL.md，不影响 GitHub 已发布版本；GitHub push 后需重新 `npx skills add -f` 或 `/plugin marketplace update` 才能同步到本地。
- **同一 skill 可被多个渠道装**：例如 CLI 创建 symlink 后，再用 `/plugin install` 会再拷贝一份到 cache——两者并存，Claude Code 路由到先注册的那个。
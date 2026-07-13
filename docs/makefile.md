# Makefile 说明

## Targets

| Target | 作用 |
|--------|------|
| `make test` | 完整检查（verify-docs + verify-scripts） |
| `make verify-docs` | 运行 `scripts/verify_skills.py`，验证所有 SKILL.md frontmatter 是否合法 |
| `make verify-scripts` | `git diff --check` + `bash -n *.sh` + `py_compile *.py` — 语法检查 |
| `make regenerate` | 运行 `scripts/build_metadata.py`，从 VERSION + SKILL.md frontmatter 重新生成所有元数据文件 |
| `make verify-generated` | 运行 `build_metadata.py --check`，检查生成文件是否有漂移 |

## 工作流

### 本地修改后

```bash
make test
```

全部通过说明没损坏。

### 发布新版本

```bash
# 1. 改 VERSION
vim VERSION

# 2. 重新生成所有元数据
make regenerate

# 3. 检查生成文件
make verify-generated

# 4. 推送
git add . && git commit -m "release: v$(cat VERSION)" && git push
```

### CI 场景

```bash
make test        # PR 检查
make verify-generated  # 检测元数据是否和 SKILL.md 同步
```

## 生成文件（不要手动改）

这些文件由 `build_metadata.py` 自动生成，手动改会被覆盖：

```
.claude-plugin/marketplace.json   — Claude Code 插件市场元数据
.agents/plugins/marketplace.json  — Codex 插件市场元数据
plugins/zack/                    — Codex 插件镜像（skills + rules）
package.json                      — npm/Pi 包元数据
scripts/dispatcher.md             — 路由表（从 SKILL.md frontmatter 生成）
skills/*/scripts/check-update.sh — 各技能的更新检查脚本
```

改任何源文件（SKILL.md、VERSION、rules/）后，必须 `make regenerate`。

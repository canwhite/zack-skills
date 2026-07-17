# Plan: LLM-Based Markdown Hierarchy Optimization for markdown-to-itmz

> 用 LLM 分析 Markdown 标题层级，语义不合理时重写结构，再交由脚本生成 itmz。

## Context

当前 `markdown-to-itmz` 直接用脚本解析 Markdown 生成 itmz，不检查标题层级语义合理性。当文档出现 `# Title` 后跳到 `### Subsection`（语义上可能合理也可能不合理），或标题层级超过 6 时，生成的 itmz 结构不可预测。需要在转换前用 LLM 审视层级语义，必要时重写。

## Goal

用户调用 `markdown-to-itmz` skill 时：
1. LLM 先读取 markdown，分析标题层级结构
2. LLM 判断层级是否语义合理（如 `#` → `###` 在该文档上下文中是否说得通）
3. 如不合理，LLM 直接重写 markdown（仅调整标题层级，不要修改正文内容）
4. 用优化后的 markdown 调用 `itmz_converter.py` 生成 itmz

## Plan

1. **修改 `SKILL.md` 工作流**
   - Step 1：LLM 读取 Markdown，分析层级结构
   - 如有问题，LLM 重写后写入临时文件，进入 Step 2；如无问题，直接进入 Step 2
   - Step 2：调用 `itmz_converter.py` 生成 itmz
   - Step 3：删除临时文件

2. **LLM prompt 设计**
   ```
   ## 任务
   分析以下 Markdown 文档的标题层级结构，判断是否存在语义不合理的跳跃或层级混乱。
   如存在，重写整个 Markdown（仅调整标题层级，不要修改正文内容）。

   ## 判断标准
   - 层级跳跃（如 # → ###）在有明确上下文时可能是合理的（如文档结构需要）
   - 超过 6 层的标题必须警告并降级
   - 层级应反映文档的大纲结构：同属一个主题的子内容应在同一父标题下

   ## 输出格式
   如无需修改：输出"无需修改"并说明理由
   如需修改：输出完整重写后的 Markdown（**仅调整标题层级，不要修改正文内容**）
   ```

3. **LLM 重写后的文件传递机制**
   - LLM 输出重写后的 Markdown → agent 用 Python `tempfile.NamedTemporaryFile(delete=False)` 创建临时文件，路径传入脚本
   - 临时文件路径格式：`/tmp/ithoughtsx_optimized_<uuid>.md`（UUID 避免并发冲突）
   - `itmz_converter.py` 读取该临时文件生成 itmz
   - 生成完毕后 agent 删除临时文件（脚本异常退出时为 best-effort）

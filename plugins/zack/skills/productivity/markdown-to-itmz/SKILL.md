---
name: markdown-to-itmz
description: Generate an iThoughts (.itmz) mind map from any Markdown file. Uses LLM to validate and optimize heading hierarchy before conversion. Use when user wants to convert markdown to itmz, create a mind map from documentation, or visualize markdown structure as a思维导图.
---

# Markdown to iThoughts Mind Map Generator

## Purpose

Convert any Markdown file into an iThoughts (.itmz) mind map format.

## Input

- Source Markdown file path
- Output itmz path (optional, defaults to `~/Documents/ithoughtsx/<stem>.itmz`)

## Workflow

### Step 1: LLM 分析 Markdown 层级结构

读取用户的 Markdown 文件，用 LLM 分析标题层级是否语义合理。

**Prompt 模板**：
```
## 任务
分析以下 Markdown 文档的标题层级结构，判断是否存在语义不合理的跳跃或层级混乱。
如存在，重写整个 Markdown（仅调整标题层级，不要修改正文内容）。

## 判断标准
- 层级跳跃（如 # → ###）在有明确上下文时可能是合理的（如文档结构需要）
- 超过 6 层的标题必须警告并降级
- 层级应反映文档的大纲结构：同属一个主题的子内容应在同一父标题下

## Markdown 内容
（粘贴用户文件内容）

## 输出格式
如无需修改：输出"无需修改"并说明理由
如需修改：输出完整重写后的 Markdown（**仅调整标题层级，不要修改正文内容**）
```

- 如 LLM 返回"无需修改"，直接进入 Step 2
- 如 LLM 返回重写后的 Markdown（**仅调整标题层级，不要修改正文内容**）：agent 用 Python `tempfile.NamedTemporaryFile(delete=False)` 写入临时文件（路径如 `/tmp/ithoughtsx_optimized_<uuid>.md`），用该文件进入 Step 2

### Step 2: 调用脚本生成 itmz

```bash
python3 ~/.claude/skills/markdown-to-itmz/itmz_converter.py <input.md> <output.itmz>
```

- 如 Step 1 无需修改：`input.md` 为用户原文件路径
- 如 Step 1 进行了重写：`input.md` 为 agent 通过 `tempfile` 创建的临时文件路径（如 `/tmp/ithoughtsx_optimized_<uuid>.md`）

Example:
```bash
python3 ~/.claude/skills/markdown-to-itmz/itmz_converter.py docs/api_guide.md ~/Documents/ithoughtsx/api_guide.itmz
```

### Step 3: Output Location

默认输出目录为 `~/Documents/ithoughtsx/`。若未指定 output path，脚本自动使用 `<input_stem>.itmz` 作为文件名。

### Step 4: Verify Output

Check the generated itmz:
```python
import zipfile
with zipfile.ZipFile('output.itmz', 'r') as z:
    print("Files:", z.namelist())
    xml = z.read('mapdata.xml').decode('utf-8')
    topic_count = xml.count('<topic ')
    print(f"Topics: {topic_count}")
```

### Step 5: Cleanup

如 Step 1 创建了临时文件，生成 itmz 后 agent 删除该临时文件。若脚本中途异常退出，临时文件可能残留（best-effort 清理）。

## itmz Format

The converter produces:
```
itmz = zip([
    mapdata.xml,      # Mind map data (XML format)
    style.xml,        # Visual styling
    manifest.plist,   # Metadata (topic count, app info)
    preview.png       # Thumbnail placeholder
])
```

### mapdata.xml Structure

- Nested `<topic>` elements with position attributes
- UUIDs with hyphens: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Position format: `position="{x, y}"`
- Code blocks wrapped in ` ``` ` within text attribute

### Position Layout Algorithm

- X coordinate: `depth * 150` (each level indented 150px)
- Y coordinate: depth <= 1 uses y=0, deeper levels alternate around parent
- Sibling offset: `(index - sibling_count/2) * 10`

## Key Features

### LLM 层级优化

转换前用 LLM 审视 Markdown 标题层级，语义不合理时自动重写（仅调整标题层级，不要修改正文内容）。

### Code Block Handling

```python
# Code blocks are wrapped in ``` and stored in text attribute
# Text shows "代码块" followed by the code
```

### Markdown Parsing（脚本层）

- `#` to `######` → hierarchy levels 1-6
- ` ```code``` ` → code block nodes with code visible
- `---` → ignored (separator)
- `[text](url)` → stripped to just `text`
- `**bold**` → stripped to just `bold`
- `` `code` `` → stripped
- `| table |` → converted to plain text table

## Files

- `itmz_converter.py` - The converter script
- `SKILL.md` - This skill definition

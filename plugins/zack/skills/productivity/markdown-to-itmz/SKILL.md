---
name: markdown-to-itmz
description: Generate an iThoughts (.itmz) mind map from any Markdown file. Use when user wants to convert markdown to itmz, create a mind map from documentation, or visualize markdown structure as a思维导图.
---

# Markdown to iThoughts Mind Map Generator

## Purpose

Convert any Markdown file into an iThoughts (.itmz) mind map format.

## Input

- Source Markdown file path
- Output itmz path (optional, defaults to `~/Documents/ithoughtsx/<stem>.itmz`)

## Workflow

### Step 1: Run Conversion

```bash
python3 ~/.claude/skills/markdown-to-itmz/itmz_converter.py <input.md> <output.itmz>
```

Example:
```bash
python3 ~/.claude/skills/markdown-to-itmz/itmz_converter.py docs/api_guide.md ~/Documents/ithoughtsx/api_guide.itmz
```

### Step 2: Default Behavior

If only input is provided, output defaults to `~/Documents/ithoughtsx/<input_stem>.itmz`:
```bash
python3 ~/.claude/skills/markdown-to-itmz/itmz_converter.py docs/notes.md
# Output: ~/Documents/ithoughtsx/notes.itmz
```

### Step 3: Verify Output

Check the generated itmz:
```python
import zipfile
with zipfile.ZipFile('output.itmz', 'r') as z:
    print("Files:", z.namelist())
    xml = z.read('mapdata.xml').decode('utf-8')
    topic_count = xml.count('<topic ')
    print(f"Topics: {topic_count}")
```

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

### Code Block Handling

```python
# Code blocks are wrapped in ``` and stored in text attribute
# Text shows "代码块" followed by the code
```

### Markdown Parsing

- `#` to `######` → hierarchy levels 1-6
- ` ```code``` ` → code block nodes with code visible
- `---` → ignored (separator)
- `[text](url)` → stripped to just `text`
- `**bold**` → stripped to just `bold`
- `` `code` `` → stripped
- `| table |` → converted to plain text table

## Output Location

Default: `~/Documents/ithoughtsx/`

## Files

- `itmz_converter.py` - The converter script
- `SKILL.md` - This skill definition

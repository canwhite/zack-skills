#!/usr/bin/env python3
"""Generate Zack distribution metadata from VERSION + SKILL.md frontmatter."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from skill_frontmatter import parse_frontmatter, should_include_codex_mirror_file

OWNER = "canwhite"
REPO = "canwhite/zack-skills"
HOMEPAGE = f"https://github.com/{REPO}"

AUTHOR_NAME = "Zack"
AUTHOR_EMAIL = "admin@example.com"

CLAUDE_MARKETPLACE_TOP = {
    "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
    "name": "zack-skills",
    "owner": {"name": AUTHOR_NAME, "email": AUTHOR_EMAIL},
}


def build_marketplace_description(skills: list[dict]) -> str:
    """Generate marketplace top-level description from current skill names."""
    names = ", ".join(s["name"] for s in sorted(skills, key=lambda x: x["name"]))
    return f"Zack engineering skills for Claude Code: {names}."

CATEGORY = "development"
CODEX_CATEGORY = "Developer Tools"
CHECK_UPDATE_SCRIPT = Path("scripts/check-update.sh")
DURABLE_CONTEXT_RULE = Path("rules/durable-context.md")
DURABLE_CONTEXT_COPY = Path("references/durable-context.md")


def read_version(root: Path) -> str:
    v = (root / "VERSION").read_text().strip()
    if not v:
        raise SystemExit("ERROR: VERSION is empty")
    return v


def collect_skill_metadata(root: Path):
    skills = []
    for path in sorted((root / "skills").glob("**/SKILL.md")):
        fields = parse_frontmatter(path)
        # skill name from frontmatter must match directory name
        skill_dir = path.parent.name
        if fields["name"] != skill_dir:
            raise SystemExit(f"ERROR: {path} frontmatter name '{fields['name']}' != directory '{skill_dir}'")
        # store relative path from skills/ for source resolution
        rel = path.parent.relative_to(root / "skills")
        fields["category_path"] = str(rel)
        skills.append(fields)
    if not skills:
        raise SystemExit("ERROR: no SKILL.md files found under skills/")
    return skills


def build_marketplace(version: str, skills: list[dict]) -> dict:
    plugins = [{"name": "zack-skills", "description": "Full Zack skill toolkit.", "version": version, "category": CATEGORY, "source": "./", "homepage": HOMEPAGE}]
    for s in sorted(skills, key=lambda x: x["name"]):
        plugins.append({"name": f"zack-{s['name']}", "description": s["description"], "version": version, "category": CATEGORY, "source": f"./skills/{s['category_path']}", "homepage": HOMEPAGE, "skills": ["./"], "strict": False})
    top = {**CLAUDE_MARKETPLACE_TOP, "description": build_marketplace_description(skills)}
    return {**top, "plugins": plugins}


def build_codex_marketplace() -> dict:
    return {"name": "zack-skills", "interface": {"displayName": "Zack"}, "plugins": [{"name": "zack-skills", "source": {"source": "local", "path": "./plugins/zack"}, "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}, "category": CODEX_CATEGORY}]}


def build_package_json(version: str) -> str:
    return json.dumps({"name": "zack-skills", "version": version, "description": "Zack engineering skills for Claude Code.", "license": "MIT", "repository": {"type": "git", "url": f"git+https://github.com/{REPO}.git"}, "homepage": f"{HOMEPAGE}#readme", "keywords": ["claude-code", "skills", "zack"], "files": ["README.md", "skills", "rules", "scripts/check-update.sh", "!**/__pycache__/**"], "publishConfig": {"access": "public"}, "pi": {"skills": ["./skills", "!skills/RESOLVER.md"]}}, indent=2, ensure_ascii=False) + "\n"


ROUTING_TABLE_START = "<!-- routing-table:start -->"
ROUTING_TABLE_END = "<!-- routing-table:end -->"


def render_dispatcher(template: str, skills: list[dict]) -> str:
    rows = ["| Intent | Skill | File |", "|--------|-------|------|"]
    for s in sorted(skills, key=lambda x: x["name"]):
        rows.append(f"| {s.get('dispatch_intent','')} | {s['name']} | `skills/{s['category_path']}/SKILL.md` |")
    block = f"{ROUTING_TABLE_START}\n{chr(10).join(rows)}\n{ROUTING_TABLE_END}"
    pat = re.compile(re.escape(ROUTING_TABLE_START) + r".*?" + re.escape(ROUTING_TABLE_END), re.DOTALL)
    return pat.sub(block, template)


def render_root_readme(skills: list[dict]) -> str:
    """Generate root README.md from SKILL.md frontmatter so the skill list cannot drift."""
    rows = ["| Skill | Description |", "|-------|-------------|"]
    for s in sorted(skills, key=lambda x: x["name"]):
        first_sentence = s["description"].split(". ")[0].rstrip(".")
        rows.append(f"| `{s['name']}` | {first_sentence}. |")
    table = "\n".join(rows)
    return (
        "# Zack Skills\n"
        "\n"
        "A toolkit of engineering workflow skills for Claude Code: pre-mortem, post-mortem, diagnose, zoom-out, caveman compression, RICE prioritization, and markdown-to-mind-map. Each skill is a Markdown workflow with frontmatter-driven dispatch; one `VERSION` file is the single source of truth for all generated artifacts (marketplace metadata, npm package, Codex mirror, dispatcher table, per-skill update check).\n"
        "\n"
        "## Skills\n"
        "\n"
        f"{table}\n"
        "\n"
        "## Install\n"
        "\n"
        "### Via skills-cli (recommended)\n"
        "\n"
        "```bash\n"
        "npx skills add https://github.com/canwhite/zack-skills -g\n"
        "```\n"
        "\n"
        "### Claude Code plugin\n"
        "\n"
        "```bash\n"
        "/plugin marketplace add zack-skills\n"
        "/plugin install zack-skills@zack-skills\n"
        "```\n"
        "\n"
        "## Uninstall\n"
        "\n"
        "```bash\n"
        "rm -rf ~/.claude/skills/zack-skills\n"
        "```\n"
        "\n"
        "## Development\n"
        "\n"
        "```bash\n"
        "make test              # verify frontmatter + scripts + drift\n"
        "make regenerate        # rebuild all generated artifacts\n"
        "make verify-generated  # CI: fail if generated files drift from source\n"
        "```\n"
        "\n"
        "See [`docs/zoom-out.md`](docs/zoom-out.md) for the architecture reference (modules, dispatch flow, packaging model).\n"
        "\n"
        "## License\n"
        "\n"
        "MIT\n"
    )


def diff(label: str, expected: str, actual: str) -> str:
    return "".join(difflib.unified_diff(actual.splitlines(keepends=True), expected.splitlines(keepends=True), fromfile=f"committed:{label}", tofile=f"generated:{label}"))


def collect_skill_shared_assets(root: Path, check_update: str) -> dict[str, bytes]:
    generated: dict[str, bytes] = {}
    durable_bytes = (root / DURABLE_CONTEXT_RULE).read_bytes() if (root / DURABLE_CONTEXT_RULE).exists() else None
    for skill_file in sorted((root / "skills").glob("**/SKILL.md")):
        skill_dir = skill_file.parent.relative_to(root)
        generated[(skill_dir / CHECK_UPDATE_SCRIPT).as_posix()] = check_update.encode()
        if DURABLE_CONTEXT_COPY.as_posix() in skill_file.read_text() and durable_bytes:
            generated[(skill_dir / DURABLE_CONTEXT_COPY).as_posix()] = durable_bytes
    return generated


def collect_codex_plugin_tree(root: Path, plugin_json: str, shared: dict[str, bytes]) -> dict[str, bytes]:
    generated = {"plugins/zack/.codex-plugin/plugin.json": plugin_json.encode()}
    for src_name in ("skills", "rules"):
        src_root = root / src_name
        if not src_root.exists():
            continue
        for path in sorted(src_root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if should_include_codex_mirror_file(path.relative_to(src_root)):
                generated[f"plugins/zack/{rel}"] = path.read_bytes()
    for rel, content in shared.items():
        generated[f"plugins/zack/{rel}"] = content
    return generated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()

    version = read_version(root)
    skills = collect_skill_metadata(root)
    marketplace = build_marketplace(version, skills)
    codex_mp = build_codex_marketplace()
    package_json = build_package_json(version)

    check_script = root / CHECK_UPDATE_SCRIPT
    check_actual = check_script.read_text() if check_script.exists() else ""
    local_ver_re = re.compile(r'LOCAL_VERSION="\$\{LOCAL_VERSION:-v\d+\.\d+\.\d+\}"')
    check_update = local_ver_re.sub(f'LOCAL_VERSION="${{LOCAL_VERSION:-v{version}}}"', check_actual)

    shared = collect_skill_shared_assets(root, check_update)
    codex_plugin_json = json.dumps({"name": "zack-skills", "version": version, "description": "Engineering workflow skills for Codex.", "author": {"name": AUTHOR_NAME, "email": AUTHOR_EMAIL}, "homepage": HOMEPAGE, "repository": HOMEPAGE, "license": "MIT", "keywords": ["codex", "skills"], "skills": "./skills/", "interface": {"displayName": "Zack", "shortDescription": "Engineering workflow skills for Codex", "longDescription": "Zack packages engineering habits as Codex skills.", "developerName": AUTHOR_NAME, "category": CODEX_CATEGORY, "capabilities": ["Interactive", "Write"], "websiteURL": HOMEPAGE, "brandColor": "#111827"}}, indent=2, ensure_ascii=False) + "\n"
    codex_tree = collect_codex_plugin_tree(root, codex_plugin_json, shared)

    dispatcher_template = root / "scripts" / "dispatcher-template.md"
    dispatcher_target = root / "scripts" / "dispatcher.md"
    dispatcher_actual = dispatcher_target.read_text() if dispatcher_target.exists() else ""
    if dispatcher_template.exists():
        dispatcher_rendered = render_dispatcher(dispatcher_template.read_text(), skills)
    else:
        dispatcher_rendered = dispatcher_actual

    readme_target = root / "README.md"
    readme_rendered = render_root_readme(skills)

    if args.check:
        drift = False
        targets = [
            (root / ".claude-plugin" / "marketplace.json", json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n"),
            (root / ".agents" / "plugins" / "marketplace.json", json.dumps(codex_mp, indent=2, ensure_ascii=False) + "\n"),
            (readme_target, readme_rendered),
        ]
        for path, expected in targets:
            actual = path.read_text() if path.exists() else ""
            if actual != expected:
                rel = path.relative_to(root).as_posix()
                print(f"DRIFT: {rel} is out of sync. Run scripts/build_metadata.py to regenerate.", file=sys.stderr)
                sys.stderr.write(diff(rel, expected, actual))
                drift = True
        for rel, expected in codex_tree.items():
            path = root / rel
            actual = path.read_bytes() if path.exists() else b""
            if actual != expected:
                print(f"DRIFT: {rel} is out of sync.", file=sys.stderr)
                drift = True
        if dispatcher_actual != dispatcher_rendered:
            print("DRIFT: scripts/dispatcher.md is out of sync.", file=sys.stderr)
            drift = True
        return 1 if drift else 0

    # Write
    (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote: .claude-plugin/marketplace.json")
    (root / ".agents" / "plugins").mkdir(parents=True, exist_ok=True)
    (root / ".agents" / "plugins" / "marketplace.json").write_text(json.dumps(codex_mp, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote: .agents/plugins/marketplace.json")
    (root / "package.json").write_text(package_json)
    print(f"wrote: package.json (v{version})")
    for rel, content in codex_tree.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    print(f"wrote: plugins/zack/ ({len(codex_tree)} files)")
    for skill_file in sorted((root / "skills").glob("**/SKILL.md")):
        skill_dir = skill_file.parent.relative_to(root)
        cu_path = skill_dir / CHECK_UPDATE_SCRIPT
        if cu_path.as_posix() in shared:
            path = root / cu_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(shared[cu_path.as_posix()])
            print(f"wrote: {cu_path}")
    if dispatcher_template.exists() and dispatcher_rendered != dispatcher_actual:
        dispatcher_target.write_text(dispatcher_rendered)
        print(f"wrote: scripts/dispatcher.md")
    readme_actual = readme_target.read_text() if readme_target.exists() else ""
    if readme_rendered != readme_actual:
        readme_target.write_text(readme_rendered)
        print(f"wrote: README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

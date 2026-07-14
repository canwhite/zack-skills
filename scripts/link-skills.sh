#!/usr/bin/env bash
set -euo pipefail

# Links all skills in the repository to ~/.claude/skills, so that
# they can be used by the local Claude CLI.
# Idempotent: leaves existing symlinks alone unless they already point
# inside this repo (in which case it normalizes them to the canonical src).
# This way, `npx skills add` post-install won't clobber a developer's
# local-dev symlinks pointing at e.g. ~/Desktop/zack-skills/skills/.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.claude/skills"

# If ~/.claude/skills is a symlink that resolves into this repo, we'd end up
# writing the per-skill symlinks back into the repo's own skills/ tree. Detect
# and bail out instead of polluting the working copy.
if [ -L "$DEST" ]; then
  resolved="$(readlink -f "$DEST")"
  case "$resolved" in
    "$REPO"|"$REPO"/*)
      echo "error: $DEST is a symlink into this repo ($resolved)." >&2
      echo "Remove it (rm \"$DEST\") and re-run; the script will recreate it as a real dir." >&2
      exit 1
      ;;
  esac
fi

mkdir -p "$DEST"

# Resolve REPO and any per-skill src to absolute paths so we can compare
# an existing symlink's target deterministically (avoids .././foo churn).
repo_real="$(cd "$REPO" && pwd)"

find "$REPO/skills" -name SKILL.md -not -path '*/node_modules/*' -print0 |
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  src_real="$(cd "$src" && pwd)"
  name="$(basename "$src_real")"
  target="$DEST/$name"

  # 1) Already a symlink pointing at the canonical src — no-op.
  if [ -L "$target" ]; then
    current_target="$(readlink "$target")"
    current_real="$(cd "$(dirname "$target")" && cd "$(dirname "$current_target")" && pwd)/$(basename "$current_target")" 2>/dev/null || echo "$current_target"
    if [ "$current_real" = "$src_real" ]; then
      echo "ok     $name (already linked)"
      continue
    fi
    # 2) Existing symlink points elsewhere (e.g., user's local-dev repo).
    #    Leave it alone — do NOT clobber.
    echo "kept   $name (existing target: $current_target; not overwriting)"
    continue
  fi

  # 3) Real file/dir at target path → clobber and link.
  if [ -e "$target" ]; then
    rm -rf "$target"
  fi

  ln -sfn "$src_real" "$target"
  echo "linked $name -> $src_real"
done

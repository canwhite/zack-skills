#!/usr/bin/env bash
set -euo pipefail

# Auto-run by `npx skills add -g <url>` post-install.
# `npx skills` looks for {setup.sh, setup.py, install.sh, install.py} at the
# root of the installed skill package and runs the first it finds.
# This wrapper delegates to the canonical script under scripts/ so the
# symlink logic lives in one place.
HERE="$(cd "$(dirname "$0")" && pwd)"
exec bash "$HERE/scripts/link-skills.sh"

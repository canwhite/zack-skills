#!/usr/bin/env bash
set -euo pipefail

make_tmpdir() {
    mktemp -d "${TMPDIR:-/tmp}/zack-test.XXXXXX"
}

copy_repo() {
    local dest="$1"
    cp -a "$(dirname "${BASH_SOURCE[0]}")/.." "$dest"
}

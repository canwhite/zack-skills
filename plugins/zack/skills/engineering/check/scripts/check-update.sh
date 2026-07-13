#!/usr/bin/env bash
set -u
SKILL="zack-skills"
REPO="canwhite/zack-skills"
LOCAL_VERSION="${LOCAL_VERSION:-v1.9.1}"
REMOTE_URL="${WAZA_UPDATE_URL:-https://raw.githubusercontent.com/${REPO}/main/VERSION}"
local_ver="$(printf '%s' "${LOCAL_VERSION}" | sed 's/^v//')"
[ -n "${local_ver}" ] || exit 0
day="$(date +%F 2>/dev/null)" || exit 0
cache_dir="${XDG_CACHE_HOME:-${HOME}/.cache}/${SKILL}"
marker="${cache_dir}/last-check"
[ "$(cat "${marker}" 2>/dev/null)" = "${day}" ] && exit 0
mkdir -p "${cache_dir}" 2>/dev/null || exit 0
rm -f "${cache_dir}"/update-checked-* 2>/dev/null
printf '%s' "${day}" > "${marker}" 2>/dev/null || exit 0
command -v curl >/dev/null 2>&1 || exit 0
remote_ver="$(curl -fsSL --max-time 3 "${REMOTE_URL}" 2>/dev/null | tr -d '[:space:]')"
[ -n "${remote_ver}" ] || exit 0
[ "${remote_ver}" = "${local_ver}" ] && exit 0
highest="$(printf '%s\n%s\n' "${local_ver}" "${remote_ver}" | sort -V 2>/dev/null | tail -1)"
[ "${highest}" = "${remote_ver}" ] || exit 0
echo "Zack ${remote_ver} is available (you have ${local_ver}). Update: npx skills update -g"
exit 0

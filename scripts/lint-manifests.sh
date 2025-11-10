#!/usr/bin/env bash
set -euo pipefail
root_dir="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required." >&2
  exit 2
fi

fail=0
lint() {
  local path="$1" id="$2" key="$3"
  local expr
  case "$id" in
    communication) expr='has("id") and has("meta") and has("logs")';;
    docs) expr='has("id") and has("meta") and has("documents")';;
    domains) expr='has("id") and has("meta") and has("domains")';;
    people) expr='has("id") and has("meta") and has("people")';;
    repositories) expr='has("id") and has("meta") and has("repositories")';;
    repo-structure) expr='has("id") and has("meta") and has("structure")';;
    workflow) expr='has("id") and has("meta") and has("workplaces") and has("tools") and has("git_policy")';;
    *) expr='has("id") and has("meta")';;
  esac
  if jq -e "$expr and (.meta|has(\"version\") and has(\"updated\"))" "$path" >/dev/null; then
    echo "OK  - $key"
  else
    echo "ERR - $key" >&2
    fail=1
  fi
}

for f in "$root_dir"/manifests/*.manifest.json; do
  base=$(basename "$f")
  id="${base%%.manifest.json}"
  lint "$f" "$id" "manifests/$base"
done
exit "$fail"


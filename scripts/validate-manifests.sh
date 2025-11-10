#!/usr/bin/env bash
set -euo pipefail
root_dir="$(cd "$(dirname "$0")/.." && pwd)"
shopt -s nullglob

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required. Install jq and retry." >&2
  exit 2
fi

fail=0
for f in "$root_dir"/*.manifest.json "$root_dir"/manifests/*.manifest.json; do
  [ -f "$f" ] || continue
  if jq empty "$f" 2>/dev/null; then
    echo "OK  - $(realpath --relative-to="$root_dir" "$f")"
  else
    echo "ERR - $(realpath --relative-to="$root_dir" "$f")" >&2
    fail=1
  fi
done
exit "$fail"

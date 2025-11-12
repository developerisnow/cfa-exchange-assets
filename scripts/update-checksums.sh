#!/usr/bin/env bash
set -euo pipefail
root_dir="$(cd "$(dirname "$0")/.." && pwd)"
proj="$root_dir/project.manifest.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required." >&2
  exit 2
fi

tmp=$(mktemp)
cp "$proj" "$tmp"

# Build a map of id->checksum
declare -A sums
while IFS= read -r line; do
  file=$(echo "$line" | awk '{print $2}')
  sum=$(echo "$line" | awk '{print $1}')
  base=$(basename "$file")
  id="${base%%.manifest.json}"
  case "$id" in
    communication|docs|domains|people|repositories|repo-structure|workflow)
      ;; # ok
    *) continue;;
  esac
  sums["$id"]="$sum"
done < <(sha256sum "$root_dir"/manifests/*.manifest.json)

# Update indices checksums
jq --argjson now "$(date +'%Y')" '.schemaVersion |= "1.2"' "$tmp" > "$tmp.1" && mv "$tmp.1" "$tmp"

for id in "${!sums[@]}"; do
  jq --arg id "$id" --arg sum "${sums[$id]}" '
    (.indices[] | select(.id==$id) | .checksum) |= $sum
  ' "$tmp" > "$tmp.1" && mv "$tmp.1" "$tmp"
done

mv "$tmp" "$proj"
echo "Checksums updated in project.manifest.json"


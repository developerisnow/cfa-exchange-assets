#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
proj="$root_dir/project.manifest.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required." >&2
  exit 2
fi

tmp="$(mktemp)"
cp "$proj" "$tmp"

# Ensure schemaVersion is up to date (idempotent)
jq '.schemaVersion |= "1.2"' "$tmp" > "${tmp}.1" && mv "${tmp}.1" "$tmp"

# For each known manifest, compute checksum and update corresponding index entry.
for f in "$root_dir"/manifests/*.manifest.json; do
  [ -f "$f" ] || continue
  base="$(basename "$f")"
  id="${base%%.manifest.json}"
  case "$id" in
    communication|docs|domains|people|repositories|repo-structure|workflow)
      ;;
    *)
      continue
      ;;
  esac

  sum="$(sha256sum "$f" | awk '{print $1}')"

  jq --arg id "$id" --arg sum "$sum" '
    (.indices[] | select(.id==$id) | .checksum) |= $sum
  ' "$tmp" > "${tmp}.1" && mv "${tmp}.1" "$tmp"
done

mv "$tmp" "$proj"
echo "Checksums updated in project.manifest.json"

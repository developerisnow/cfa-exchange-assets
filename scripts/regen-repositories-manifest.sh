#!/usr/bin/env bash
set -euo pipefail
root_dir="$(cd "$(dirname "$0")/.." && pwd)"
out="$root_dir/manifests/repositories.manifest.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required." >&2
  exit 2
fi

declare -a ids
declare -A path url

while IFS= read -r name; do
  mod="${name#submodule \"}"
  mod="${mod%\"}"
  p=$(git -C "$root_dir" config -f "$root_dir/.gitmodules" --get submodule."$mod".path)
  u=$(git -C "$root_dir" config -f "$root_dir/.gitmodules" --get submodule."$mod".url)
  ids+=("$mod")
  path["$mod"]="$p"
  url["$mod"]="$u"
done < <(git -C "$root_dir" config -f "$root_dir/.gitmodules" --name-only --get-regexp submodule\..*\.path || true)

existing=$(jq -c '.' "$out" 2>/dev/null || echo '{"id":"repositories","description":"","meta":{"version":"auto","updated":""},"repositories":[]}')

# Build new list for submodules
tmp=$(mktemp)
printf '{"repositories":[' > "$tmp"
first=1
for id in "${ids[@]}"; do
  [ $first -eq 1 ] || printf ',' >> "$tmp"
  first=0
  # Simple id mapping: use last path segment
  rid=$(basename "${path[$id]}")
  printf '{"id":%q,"path":%q,"remotes":{"origin":%q},"default_branch":"main","submodule":true}' \
    "$rid" "./${path[$id]}" "${url[$id]}" >> "$tmp"
done
printf ']}' >> "$tmp"

# Merge with roles/notes from existing file by id
jq -s '
  def toMap: map({(.id): .}) | add;
  def mergeRepo(a;b): a + {
    role:(b.role // a.role // null),
    notes:(b.notes // a.notes // null),
    remotes:(a.remotes + (b.remotes // {})),
    default_branch:(b.default_branch // a.default_branch // "main"),
    submodule:(b.submodule // a.submodule // false)
  };
  
  {existing:(.[0].repositories // [] | toMap), fresh:(.[1].repositories // [] | toMap)}
  | .result = ( ( .fresh | to_entries | map( mergeRepo(.value; (.existing[.key] // {})) ) ) )
  | {id:(.[0].id // "repositories"), description:(.[0].description // "Code repositories relevant to the project."), meta:{version:(.[0].meta.version // "auto"), updated: (now | todate)}, repositories: .result}
' "$out" "$tmp" > "$out.new"
mv "$out.new" "$out"
rm -f "$tmp"
echo "Rebuilt manifests/repositories.manifest.json from .gitmodules"


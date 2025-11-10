#!/usr/bin/env bash
set -euo pipefail

# Rewire symlinks to be relative (portable) or absolute (macOS local policy).
# Default: auto (Darwin => absolute, else => relative)
# Usage:
#   scripts/symlinks_rewire.sh auto|relative|absolute

MODE=${1:-auto}

repo_root() {
  git rev-parse --show-toplevel
}

mklink() {
  local target="$1" linkpath="$2"
  mkdir -p "$(dirname "$linkpath")"
  rm -f "$linkpath"
  ln -sfn "$target" "$linkpath"
}

relative_to() {
  # Compute relative path from $2 to $1
  # relpath target base
  python3 - "$1" "$2" <<'PY'
import os,sys
t,b = sys.argv[1], sys.argv[2]
print(os.path.relpath(t, start=os.path.dirname(b)))
PY
}

main() {
  local root
  root=$(repo_root)

  # Map: link => target (absolute path)
  local link_docs="$root/memory-bank/repo-cfa-rwa"
  local target_docs="$root/repositories/customer-gitlab/docs-cfa-rwa"

  case "$MODE" in
    auto)
      if [[ "$(uname -s)" == "Darwin" ]]; then MODE=absolute; else MODE=relative; fi
      ;&
    relative)
      local rel
      rel=$(relative_to "$target_docs" "$link_docs")
      mklink "$rel" "$link_docs"
      ;;
    absolute)
      # Use absolute path from current FS root
      mklink "$target_docs" "$link_docs"
      ;;
    *)
      echo "Usage: $0 {auto|relative|absolute}" >&2; exit 2
      ;;
  esac
}

main "$@"


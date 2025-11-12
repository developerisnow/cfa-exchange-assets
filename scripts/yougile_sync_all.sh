#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CTX_DIR="$BASE_DIR/memory-bank/context/yougile-mcp"
PY="/Users/user/__Repositories/yougile/yougile-mcp__justrussian/venv/bin/python"

# load env for exporter
if [ -f "$CTX_DIR/.env.local" ]; then
  set -a; source "$CTX_DIR/.env.local"; set +a
elif [ -f "$CTX_DIR/.env" ]; then
  set -a; source "$CTX_DIR/.env"; set +a
fi

cd "$BASE_DIR"

# ensure main branch
git checkout main

# 1) Export by-creator only (no assignee folders)
"$PY" "$CTX_DIR/20251110-0704-yougile-export-tasks.py" \
  --out "$CTX_DIR" \
  --all-assignees \
  --by-creator \
  --max-tasks "${MAX_TASKS:-5000}"

# (no intermediate commit)

# 2) Rebuild links catalogs (verbose + unique)
"$PY" "$CTX_DIR/20251110-1015-yougile-links-catalog.py" \
  --base "$CTX_DIR" \
  --include-comments || true

# (no intermediate commit)

# 3) Rebuild weekly summary v2
"$PY" "$CTX_DIR/20251110-1050-yougile-weekly-summary-v2.py" \
  --base "$CTX_DIR" || true

# (no intermediate commit)

"$PY" "$CTX_DIR/20251110-1027-yougile-index.py" || true
if ! git diff --quiet -- "$CTX_DIR"; then
  git add -A "$CTX_DIR"
  TS=$(date +"%Y%m%d-%H%M")
  MSG=$(cat <<EOF
data(sync): [co-6519] - Yougile by-creator sync $TS
• Exported by-creator tasks (no rewrites on no-change)
• Rebuilt links (verbose+unique), weekly v2, unique index
agentID=019a5914-6519-7752-a558-3a161f0a2407
EOF
)
  git commit -m "$MSG"
fi

echo "Sync completed"

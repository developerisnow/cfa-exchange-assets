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

# ensure branch
BR="codex/yougile-mcp-export"
if ! git rev-parse --verify "$BR" >/dev/null 2>&1; then
  git checkout -b "$BR"
else
  git checkout "$BR"
fi

# 1) Export by-creator only (no assignee folders)
"$PY" "$CTX_DIR/20251110-0704-yougile-export-tasks.py" \
  --out "$CTX_DIR" \
  --all-assignees \
  --by-creator \
  --max-tasks "${MAX_TASKS:-5000}"

# Commit export changes (semantic commit #1)
if ! git diff --quiet -- "$CTX_DIR/by-creator"; then
  git add -A "$CTX_DIR/by-creator"
  MSG=$(cat <<EOF
data(export): [co-6519] - Yougile by-creator export
• Updated creator-grouped tasks (no assignee folders)
agentID=019a5914-6519-7752-a558-3a161f0a2407
EOF
)
  git commit -m "$MSG"
fi

# 2) Rebuild links catalogs (verbose + unique)
"$PY" "$CTX_DIR/20251110-1015-yougile-links-catalog.py" \
  --base "$CTX_DIR" \
  --include-comments || true

# Commit links (semantic commit #2)
if ! git diff --quiet -- "$CTX_DIR/links-catalog.csv" "$CTX_DIR/links-unique-registry.csv"; then
  git add "$CTX_DIR/links-catalog.csv" "$CTX_DIR/links-unique-registry.csv"
  MSG=$(cat <<EOF
data(links): [co-6519] - Rebuilt links catalogs (verbose + unique)
• Updated links-catalog.csv and links-unique-registry.csv
agentID=019a5914-6519-7752-a558-3a161f0a2407
EOF
)
  git commit -m "$MSG"
fi

# 3) Rebuild weekly summary v2
"$PY" "$CTX_DIR/20251110-1050-yougile-weekly-summary-v2.py" \
  --base "$CTX_DIR" || true

# Commit weekly summary (semantic commit #3)
if ! git diff --quiet -- "$CTX_DIR"/*yougile-weekly-summary*.md; then
  git add "$CTX_DIR"/*yougile-weekly-summary*.md
  MSG=$(cat <<EOF
data(summary): [co-6519] - Weekly summary v2 updated
• Email — role — name, wiki links + external links
agentID=019a5914-6519-7752-a558-3a161f0a2407
EOF
)
  git commit -m "$MSG"
fi

# 4) Rebuild unique index
"$PY" "$CTX_DIR/20251110-1027-yougile-index.py" || true
if ! git diff --quiet -- "$CTX_DIR/yougile-index.csv"; then
  git add "$CTX_DIR/yougile-index.csv"
  MSG=$(cat <<EOF
chore(index): [co-6519] - Rebuilt unique tasks index
• yougile-index.csv (id, title, creator, assignees, paths_count)
agentID=019a5914-6519-7752-a558-3a161f0a2407
EOF
)
  git commit -m "$MSG"
fi

echo "Sync completed"

#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CTX_DIR="$BASE_DIR/memory-bank/context/yougile-mcp"
PY="/Users/user/__Repositories/yougile/yougile-mcp__justrussian/venv/bin/python"

if [ -f "$CTX_DIR/.env.local" ]; then
  set -a; source "$CTX_DIR/.env.local"; set +a
elif [ -f "$CTX_DIR/.env" ]; then
  set -a; source "$CTX_DIR/.env"; set +a
fi

exec "$PY" "$CTX_DIR/20251110-0704-yougile-export-tasks.py" --out "$CTX_DIR" --all-assignees --max-tasks "${MAX_TASKS:-5000}"


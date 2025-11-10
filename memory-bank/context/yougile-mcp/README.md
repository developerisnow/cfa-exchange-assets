---
created: 2025-11-10 10:58
type: docs
sphere: operations
topic: yougile export + sync pipeline
author: Alex
agentID: 019a5914-6519-7752-a558-3a161f0a2407
partAgentID: [co-6519]
version: 0.2.1
tags: [yougile, sync, summary, links, creator]
---

# Yougile Sync Pipeline (by-creator)

## TL;DR
- Default grouping: by-creator only → `by-creator/<email>/*.md` (1 file = 1 task)
- Every 2h: export → links (verbose+unique) → weekly summary v2 → index → single git commit
- Local secrets: `.env.local` (preferred) or `.env` in this folder (ignored by git)

## Layout
- Tasks (by creator): `by-creator/<email>/*.md`
- Aliases (ID↔email/name): `users-aliases.csv`
- Links (verbose): `links-catalog.csv`
- Links (unique): `links-unique-registry.csv`
- Weekly report(s): `*yougile-weekly-summary.md`
- Unique index: `yougile-index.csv`

## Setup
1) Fill `.env.local` here (copy from `.env.example`):
   - `YOUGILE_EMAIL`, `YOUGILE_PASSWORD` or `YOUGILE_API_KEY`
   - `YOUGILE_COMPANY_ID` (UUID)
   - `YOUGILE_MCP_SRC`, `YOUGILE_VENV` (paths to yougile-mcp repo/venv)
2) One-time run (manual):
   ```bash
   /Users/user/__Repositories/yougile/yougile-mcp__justrussian/venv/bin/python \
     memory-bank/context/yougile-mcp/20251110-0704-yougile-export-tasks.py \
     --out memory-bank/context/yougile-mcp --all-assignees --by-creator
   ```

## Auto-sync (2h)
- Plist: `~/Library/LaunchAgents/com.cfa.yougile.sync.plist` (already loaded)
- Runs: `scripts/yougile_sync_all.sh`
  - export (by-creator only)
  - links (verbose + unique)
  - summary v2 (role/name + wiki links)
  - index (unique tasks)
  - Single semantic git commit per run (only on diff)

## Aliases (manual)
- File: `/Users/user/____Sandruk/___PARA/__Areas/_5_CAREER/DEVOPS/automations/zsh/aliases/project-hypetrain.zsh`
- Commands:
  - `yg_sync_creator` — full by-creator export
  - `yg_links` — rebuild links (with comments)
  - `yg_sync_all` — `make yougile-export-all` (uses Makefile target)

## Scripts (what they do)
- Exporter: `20251110-0704-yougile-export-tasks.py`
  - Reads `.env(.local)`, re-executes under venv
  - Downloads tasks per user, enriches project/board/status/timestamp
  - Writes by-creator (default). Per-assignee can be enabled `--assignee-folders`
- Links: `20251110-1015-yougile-links-catalog.py`
  - Extracts URLs from descriptions (+comments option)
  - Outputs `links-catalog.csv` and `links-unique-registry.csv`
- Weekly v2: `20251110-1050-yougile-weekly-summary-v2.py`
  - Last 7 days by timestamp; per user section with role/name; wiki links
- Index: `20251110-1027-yougile-index.py`
  - Counts unique tasks by `yougile.id` and paths

## FAQ
- Per-assignee папки? Код оставлен, но по умолчанию выключен. Включить добавив флаг `--assignee-folders` в вызов экспортера.
- HAR events? Выключено. Скрипт `*events-fetch.py` опционален и не участвует в пайплайне.
- MCP vs scripts?
  - READ/SYNC: надёжнее скриптами (контроль ретраев, дедуп, файловая иерархия, idempotency, авто-коммиты)
  - WRITE/INTERACTIVE: MCP удобен как инструмент в LLM (создание/изменение задач, комментарии, планирование спринтов)
  - Гибрид: LLM через MCP создаёт/обновляет артефакты, а sync-скрипты обеспечивают детерминированный сбор и архив.

## Troubleshooting
- `httpx`/`mcp` not found — проверьте `YOUGILE_VENV` и корректные пути.
- Пустой weekly — убедитесь, что есть `by-creator/<email>/*.md` и у задач актуальный `yougile.timestamp`.
- Креды — храните только в `.env.local` (git-ignored). `.mcp.json` не обязателен для sync.

## Commit Policy
- Авто-коммиты каждые 2 часа (3 шага): export, links, summary (и index как отдельный chore при изменении)
- Вручную — любые скрипты можно запускать через алиасы; коммиты фиксируют только изменения

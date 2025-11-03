---
created: 2025-10-31 11:55
updated: 2025-10-31 11:55
type: init-prompt
sphere: [devops]
topic: [remote-setup, rsync]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [eywa1, transfer, rsync]
---

Goal
- Перенести локальный репозиторий в рабочую директорию на удалённом сервере eywa1, сохранив историю git и структуру файлов. После переноса — короткая валидация и фиксация актуальной ветки.

Context
- Локальный путь (macOS): `/Users/user/__Repositories/prj_Cifra-rwa-exachange-assets`
- SSH alias: `ssh eywa1` (уже настроен и работает)
- Удалённый сервер: `user@eywa-ubuntu-8gb-hel1-2`
- Целевая база на сервере: `/home/user/__Repositories/yury-customer`
- Внутри базы уже есть подпапка для этого репозитория (если нет — создать): `/home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets`

Assumptions
- На локальной машине есть права на чтение исходной папки.
- На сервере достаточно места (≥2 GB запас) и права пользователя `user` на целевой путь.
- Сохранить `.git` (ветки и история), симлинки — как есть.

Plan (DoD)
1) Проверить доступ по SSH (`ssh eywa1`) и наличие целевого пути.
2) Создать папку репозитория на сервере, если отсутствует.
3) Выполнить rsync (dry‑run), затем реальный перенос с сохранением прав/времён, удалением лишнего.
4) Верифицировать: `git status`, активная ветка `codex/jump-into-project-20251030`, несколько выборочных файлов.
5) Отчёт: вывести итоги (кол-во файлов, размер), зафиксировать время и команды.

Commands (run locally)
```bash
set -euo pipefail

# 0) Вводные
LOCAL_REPO="/Users/user/__Repositories/prj_Cifra-rwa-exachange-assets"
REMOTE_HOST="eywa1"
REMOTE_BASE="/home/user/__Repositories/yury-customer"
REMOTE_REPO="${REMOTE_BASE}/prj_Cifra-rwa-exachange-assets"

# 1) SSH доступ и базовая валидация
ssh ${REMOTE_HOST} "mkdir -p ${REMOTE_REPO} && echo REMOTE_OK && hostname && pwd && df -h ${REMOTE_BASE}"

# 2) DRY‑RUN перенос (просмотр изменений)
rsync -avh --dry-run --delete \
  --exclude='.DS_Store' \
  --exclude='node_modules/' \
  "${LOCAL_REPO}/" "${REMOTE_HOST}:${REMOTE_REPO}/"

# 3) Реальный перенос
rsync -avh --progress --delete \
  --exclude='.DS_Store' \
  --exclude='node_modules/' \
  "${LOCAL_REPO}/" "${REMOTE_HOST}:${REMOTE_REPO}/"

# 4) Пост‑проверки на сервере
ssh ${REMOTE_HOST} "set -e; cd ${REMOTE_REPO}; \
  echo '=== GIT STATUS ==='; git status; \
  echo '=== BRANCH ==='; git rev-parse --abbrev-ref HEAD || true; \
  echo '=== SAMPLE FILES ==='; ls -la memory-bank | head -n 20; \
  echo '=== SIZE ==='; du -sh ."
```

Notes
- `--delete` в rsync делает зеркалирование: на сервере удалит файлы, удалённые локально (safe при осознанном применении).
- Если alias `eywa1` не работает, проверить `~/.ssh/config` (Host eywa1; User user; HostName eywa-ubuntu-8gb-hel1-2; IdentityFile ...).
- Если на сервере уже лежит рабочая копия — rsync обновит только изменённые файлы, `.git` сохранит историю/ветки.

Validation (DoD)
- Доступ по `ssh eywa1` есть; целевой путь существует.
- Репозиторий скопирован, `git status` без ошибок, ветка отображается (`codex/jump-into-project-20251030` или текущая активная).
- Размер папки на сервере разумный (сопоставим с локальным), выборочные файлы на месте.

Handover
- По завершении сообщить: время, результат dry‑run, итоговый размер, активная ветка, заметки (если были конфликты/ошибки).


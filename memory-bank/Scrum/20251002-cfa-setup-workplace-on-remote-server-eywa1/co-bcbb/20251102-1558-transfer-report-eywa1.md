---
created: 2025-11-02 15:58
updated: 2025-11-02 15:58
type: execution-report
sphere: [devops]
topic: [remote-setup, rsync]
author: codex
agentID: bcbb
partAgentID: [co-bcbb]
version: 1.0.0
tags: [eywa1, transfer, rsync, ssh]
---

TL;DR
- Репозиторий синхронизирован на eywa1 с сохранением .git и структуры
- Активная ветка: codex/jump-into-project-20251030; git status без ошибок исполнения (есть 1 отличие по Unicode)
- Итог: 637 файлов, 262 каталогов, размер ~75M; dry‑run показал ~900 элементов к проверке

Steps
1) Проверка SSH и целевого пути; создание директории
2) rsync dry‑run с зеркалированием (delete)
3) rsync реальный перенос с прогрессом
4) Пост‑валидации: git status, ветка, листинг, размер, подсчёт файлов/папок

Summary
- Host: eywa1 (hostname: eywa-ubuntu-8gb-hel1-2)
- Remote path: /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets
- Branch: codex/jump-into-project-20251030
- Size: 75M
- Files: 637; Dirs: 262
- Notable: обнаружено различие именования файла (Unicode normalization) — 1 deleted + 1 untracked с визуально похожим именем

Commands
```bash
# Вводные
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
  echo '=== SIZE ==='; du -sh .; \
  echo -n 'FILES_COUNT='; find . -type f | wc -l; \
  echo -n 'DIRS_COUNT='; find . -type d | wc -l; \
  true"
```

Key Outputs
```text
[SSH check]
REMOTE_OK
eywa-ubuntu-8gb-hel1-2
/home/user
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       150G   75G   70G  52% /

[rsync --dry-run]
Transfer starting: ~900 files (по списку rsync)

[post-check]
=== GIT STATUS ===
On branch codex/jump-into-project-20251030
Changes not staged for commit:
  deleted:    ".../01-platform_functionality__tables_20251026-115409/Витрина_предложений_3_5_vypuski_cfa_1.tsv"

Untracked files:
  ".../01-platform_functionality__tables_20251026-115409/Витрина_предложений̆_3_5_vypuski_cfa_1.tsv"

=== BRANCH ===
codex/jump-into-project-20251030
=== SIZE ===
75M	.
FILES_COUNT=637
DIRS_COUNT=262
```

Notes
- Разница в именах файла — классическая проблема NFC/NFD (macOS vs Linux). В Git это отражается как удаление старого и появление нового пути. Функционально — не блокер; опционально можно нормализовать имена и зафиксировать коммит на сервере.
- rsync выполнялся с флагом --delete (зеркалирование) и исключениями: .DS_Store, node_modules/.

Next Actions
- Нужна ли нормализация Unicode имён (NFC) и фиксация коммита на сервере? Могу выполнить.
- При необходимости — добавить nightly rsync/backup job (systemd timer + unit).

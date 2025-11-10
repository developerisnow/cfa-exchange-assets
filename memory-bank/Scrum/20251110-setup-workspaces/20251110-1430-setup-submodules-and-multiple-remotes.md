---
created: 2025-11-10 14:30
updated: 2025-11-10 14:30
type: [planning, execution-report]
sphere: [devops, repositories]
topic: [submodules, mirrors, symlinks, eywa1]
author: Alex A
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [git, submodules, pushurl, github, gitlab, ssh, eywa1]
---

TL;DR
- Слил ветки в `main` и добавил 2 субмодуля (`ois-cfa`, `velvet`), создал 3 приватных зеркала в GitHub и настроил зеркальный push.
- В монорепо и субмодулях включён multi-push (`origin.pushurl` → GitLab+GitHub) и `push.recurseSubmodules=on-demand`.
- Добавлены утилиты: `make mirror/setup|push` и переносимые симлинки `make symlinks/auto|relative|absolute` (сервер → relative).

DoD (Definition of Done)
- [x] `main` содержит работу из `codex/jump-into-project-20251030` и `codex/yougile-mcp-export` (без конфликтов).
- [x] Субмодули подключены: `repositories/customer-gitlab/{ois-cfa,velvet}` → GitLab URLs, зафиксированы в `.gitmodules`.
- [x] Созданы приватные GH зеркала: `developerisnow/{cfa-exchange-assets,cfa-ois-cfa,cfa-velvet}` и получатели `alex` добавлены.
- [x] Зеркальный push настроен: любой `git push origin` в монорепо подпинывает недостающие коммиты субмодулей и пушит в GitLab+GitHub.
- [x] Репорт/план оформлен (этот файл) с шагами для `eywa1` и правилами симлинков.

Kickoff Tasks
1) Монорепо (локально)
   - [x] Merge веток → `main`
   - [x] Добавить субмодули: `ois-cfa`, `velvet`
   - [x] Настроить зеркала и проверить push
   - [x] Добавить `Makefile` цели и скрипты (`scripts/git_mirror.sh`, `scripts/symlinks_rewire.sh`)
   - [x] Обновить `manifests/repositories.manifest.json`
2) Сервер `eywa1`
   - [ ] Клонировать/синхронизировать монорепо в: `/home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets`
   - [ ] `git checkout main && git submodule update --init --recursive`
   - [ ] `make mirror/setup` (создаст локальные pushurl в origin и `alex` remotes)
   - [ ] `make symlinks/auto` (на Linux создаст относительные симлинки)
   - [ ] Тест: `make mirror/push` (необязательно; убедиться, что пушится в GitLab и зеркалится в GitHub)

Что сделано (детали)
- Merge: `codex/jump-into-project-20251030` → `codex/yougile-mcp-export` (уже включено), затем → `main`.
- Submodules: `git@git.telex.global:npk/ois-cfa.git` и `git@git.telex.global:npk/velvet.git` добавлены и инициализированы.
- GH private repos созданы через `gh`: `cfa-exchange-assets`, `cfa-ois-cfa`, `cfa-velvet`; в монорепо добавлен `remote alex`.
- Mirroring: `push.recurseSubmodules=on-demand` + у каждого `origin` добавлены 2 pushurl (GitLab+GitHub). Любой `git push origin` зеркалит.
- Утилиты:
  - `make mirror/setup|push` → `scripts/git_mirror.sh`
  - `make symlinks/auto|relative|absolute` → `scripts/symlinks_rewire.sh`

eywa1 (контекст)
- См. отчёт: `memory-bank/Scrum/20251002-cfa-setup-workplace-on-remote-server-eywa1/co-bcbb/20251102-1558-transfer-report-eywa1.md`
- Доступ: `ssh eywa1`; базовый путь: `/home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets`
- Отличия macOS/Linux: Unicode (NFC/NFD) на именах, симлинки: на сервере используем относительные.

Инструкции для сервера (пошагово)
```bash
ssh eywa1
cd /home/user/__Repositories/yury-customer
# Если репо ещё не склонировано:
git clone git@github.com:developerisnow/cfa-exchange-assets.git prj_Cifra-rwa-exachange-assets
cd prj_Cifra-rwa-exachange-assets

# Переключиться на main, подтянуть субмодули
git checkout main
git submodule update --init --recursive

# Включить локальное зеркалирование (origin pushurl + alex)
make mirror/setup

# Перестроить симлинки под Linux (relative)
make symlinks/auto

# Проверка пуша (опционально):
make mirror/push
```

Симлинки: подход
- В кодовой базе храним симлинки как артефакт структуры, но не полагаемся на абсолютные пути.
- На macOS (Darwin) можно использовать абсолютный путь внутри рабочей машины (KISS). На серверах — относительные (`ln -sfn <rel>`).
- Автоматизация: `make symlinks/auto` вызовет относительные на Linux и абсолютные на macOS.

Таблица — ключевые решения
- Мердж веток → main: завершено, конфликтов нет
- Субмодули (`ois-cfa`, `velvet`): добавлены, GitLab URLs
- Зеркала GH: созданы приватные, добавлен `alex`
- Mirroring: `push.recurseSubmodules=on-demand` + multiple `pushurl`
- Сервер `eywa1`: план действий и команды даны
- Симлинки: portable-скрипт и Make цели

Next Actions
- [ ] Выполнить серверные шаги на `eywa1` (см. инструкции)
- [ ] Проверить доступы GitLab (второй ключ добавлен) и тестовый пуш субмодулей
- [ ] Принять решение: нормализовать ли Unicode имена (NFC) на сервере и закоммитить
- [ ] (Опционально) pre-push hook для авто-настройки зеркал у разработчиков (`core.hooksPath`)


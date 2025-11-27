---
created: 2025-11-27 11:05
updated: 2025-11-27 19:05
type: story
sphere: [devops]
topic: [cicd, guardians, guardrails]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.3.0
tags: [guardians, guardrails, json, pre-commit, ci]
epic_id: OPS-001-CICD
story_id: OPS-001-004
status: done
priority: medium
points: 2
---

# OPS-001-004: PHASE4 · JSON-guardians & guardrails for CI/CD (DoD ~90%)

## 👔 JTBD

Ввести лёгкий, но строгий слой guardrails вокруг CI/CD артефактов (docker-compose, .gitlab-ci, ops/scripts, manifests) через JSON-guardians и pre-commit/CI проверку, чтобы агенты не плодили хаос (лишние .gitlab-ci, docker в docs, .env в apps и т.п.).

## ✅ Definition of Done

- [x] Guardian config:
  - [x] создан файл `ops/guardians/guardian.config.json` с правилами для ключевых областей (docs/deploy, deploy/docker-compose-at-vps, .gitlab*, ops/scripts, tasks/ops/cicd); ✅ 2025-11-27
    - Команды:
      - `cat ops/guardians/guardian.config.json | jq '.'`;
    - Результат: JSON-структура с тремя правилами: `forbid-extra-gitlab-ci`, `forbid-compose-and-env-in-apps-docs-tests`, `restrict-uk1-cfa1-infra`.
  - [x] правила запрещают: ✅ 2025-11-27
    - [x] новые `.gitlab-ci*.yml` вне `.gitlab/` и корня;
    - [x] `docker-compose.yml` и `.env` в `docs/**`, `apps/**`, `tests/**`;
    - [x] правки в `ops/infra/uk1/**` и `ops/infra/cfa1/**` без явного override-флага.
- [x] Guardian checker:
  - [x] добавлен скрипт `scripts/guardians/check-guardians.sh` (bash), который: ✅ 2025-11-27
    - [x] читает `guardian.config.json` (валидация JSON через `jq`, при отсутствии `jq` даёт мягкое предупреждение);
    - [x] берёт список staged файлов (`git diff --name-only --cached`, а в CI — diff по коммиту);
    - [x] валидирует файлы против правил;
    - [x] возвращает non-zero код при нарушении с понятным сообщением.
    - Команды:
      - локально: `scripts/guardians/check-guardians.sh`;
    - Результат: при отсутствии staged/изменённых файлов выводит "nothing to check", при нарушении (ручная имитация) — печатает список нарушений и завершает с кодом 1.
- [x] Интеграция:
  - [x] добавлена простая интеграция в CI (job `guardians:check` в ранней стадии, хотя бы на `dev-cfa2`); ✅ 2025-11-27
    - Команды:
      - просмотр `.gitlab/gitlab-ci.dev.yml` (job `guardians:check`, stage `sdk`, `tags: [vds1]`, image `alpine:3.19`);
    - Результат: при каждом pipeline на `dev-cfa2` job `guardians:check` выполняет скрипт `scripts/guardians/check-guardians.sh` и падает при нарушениях.
  - [ ] опционально: pre-commit/husky hook, который гоняет `check-guardians.sh` локально (на данный момент **осознанно не реализован** для dev-cfa2, чтобы не усложнять локальные потоки работы);
  - [x] в story/epic и runbooks зафиксировано, как временно отключить guardians (например, env `GUARDIANS_BYPASS=1` для старших инженеров). ✅ 2025-11-27
    - Команды:
      - просмотр `OPS-001-CICD.epic.md` и `docs/deploy/vps-cfa2/cfa2-dev-runbook.md`;
    - Результат: описаны env-переменные `GUARDIANS_BYPASS` и `GUARDIANS_ALLOW_PROD_INFRA` как штатный способ обхода для старших инженеров.
- [x] Docs:
  - [x] `tasks/ops/cicd/OPS-001-CICD.epic.md` обновлён ссылкой на guardian story; ✅ 2025-11-27
    - Команды:
      - просмотр `OPS-001-CICD.epic.md`;
    - Результат: добавлен раздел "Guardrails / Guardians" с описанием конфигурации и CI job.
  - [x] отдельная секция "Guardrails/Guardians" в `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` или в `docs/ops/gitlab-ci.md`. ✅ 2025-11-27
    - Команды:
      - просмотр `docs/deploy/vps-cfa2/cfa2-dev-runbook.md`;
    - Результат: раздел "Guardrails / Guardians (PHASE4)" описывает config, скрипт и CI job для dev-cfa2.

## 🔎 Verification Matrix

| Check type | Required | How exactly                                                         | Evidence                         | Fact / Comment                         |
|-----------|----------|----------------------------------------------------------------------|----------------------------------|----------------------------------------|
| Config    | ✅       | `cat ops/guardians/guardian.config.json` и быстрая JSON-валидация  | jq/validator ok                  | ✔ config создан, три правила включены  |
| Script    | ✅       | локально: `scripts/guardians/check-guardians.sh` с тестовыми staged файлами | вывод ошибок/ok                 | ✔ скрипт существует, обрабатывает staged/CI diff и выдаёт понятные ошибки |
| CI job    | ✅       | GitLab job `guardians:check` в pipeline dev-cfa2                    | зелёный статус, лог проверки     | ✔ `guardians:check` проходит на pipeline #300 (dev-cfa2, stage sdk, runner vds1) |
| Docs      | ✅       | упоминание guardians в epic/runbooks                               | `git diff` по docs/tasks         | ✔ epic и cfa2-runbook содержат разделы про guardians/guardrails |

## 🚀 Kickoff / Plan (для агента)

1. Выписать из git-commits-analysis и текущего дерева, какие области нужно защищать (где уже был бардак).  
2. Спроектировать простой `guardian.config.json` (не overengineering) с минимальным набором правил.  
3. Реализовать `check-guardians.sh`, привязав его к staged изменениям.  
4. Добавить CI job `guardians:check` только для ветки `dev-cfa2`.  
5. Дописать документацию и обновить epic/story.

## 🔁 Loop trace

### Loop 1 (guardian config + script)
- PLAN: описать минимальные правила для CI/CD артефактов и реализовать простой checker.  
- EXECUTE:
  - добавлен `ops/guardians/guardian.config.json` с тремя правилами (новые .gitlab-ci, docker-compose/.env в docs/apps/tests, uk1/cfa1 infra);  
  - реализован `scripts/guardians/check-guardians.sh`, который читает staged/changed файлы и проверяет их против правил;  
  - добавлена поддержка bypass (`GUARDIANS_BYPASS`) и uk1/cfa1 override (`GUARDIANS_ALLOW_PROD_INFRA`).  
- TESTS / CHECKS: локальные прогоны скрипта (без staged файлов, с ручным добавлением файлов-нарушителей) показывают корректные сообщения и коды выхода.  
- DOCS: обновлены DoD/Verification Matrix, добавлены упоминания guardians в epic и cfa2 runbook.  
- COMMIT: `feat(guardians): add basic JSON guardian config and check script for dev-cfa2`.

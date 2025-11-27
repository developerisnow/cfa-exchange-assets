---
created: 2025-11-27 11:05
updated: 2025-11-27 11:05
type: story
sphere: [devops]
topic: [cicd, guardians, guardrails]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.1.0
tags: [guardians, guardrails, json, pre-commit, ci]
epic_id: OPS-001-CICD
story_id: OPS-001-004
status: planned
priority: medium
points: 2
---

# OPS-001-004: PHASE4 · JSON-guardians & guardrails for CI/CD

## 👔 JTBD

Ввести лёгкий, но строгий слой guardrails вокруг CI/CD артефактов (docker-compose, .gitlab-ci, ops/scripts, manifests) через JSON-guardians и pre-commit/CI проверку, чтобы агенты не плодили хаос (лишние .gitlab-ci, docker в docs, .env в apps и т.п.).

## ✅ Definition of Done

- [ ] Guardian config:
  - [ ] создан файл `ops/guardians/guardian.config.json` с правилами для ключевых областей (docs/deploy, deploy/docker-compose-at-vps, .gitlab*, ops/scripts, tasks/ops/cicd);
  - [ ] правила запрещают:
    - [ ] новые `.gitlab-ci*.yml` вне `.gitlab/` и корня;
    - [ ] `docker-compose.yml` и `.env` в `docs/**`, `apps/**`, `tests/**`;
    - [ ] правки в `ops/infra/uk1/**` и `ops/infra/cfa1/**` без явного override-флага.
- [ ] Guardian checker:
  - [ ] добавлен скрипт `scripts/guardians/check-guardians.sh` (bash или node), который:
    - [ ] читает `guardian.config.json`;
    - [ ] берёт список staged файлов (`git diff --name-only --cached`);
    - [ ] валидирует файлы против правил;
    - [ ] возвращает non-zero код при нарушении с понятным сообщением.
- [ ] Интеграция:
  - [ ] добавлена простая интеграция в CI (job `guardians:check` в ранней стадии, хотя бы на `dev-cfa2`);
  - [ ] опционально: pre-commit/husky hook, который гоняет `check-guardians.sh` локально;
  - [ ] в story/epic и runbooks зафиксировано, как временно отключить guardians (например, env `GUARDIANS_BYPASS=1` для старших инженеров).
- [ ] Docs:
  - [ ] `tasks/ops/cicd/OPS-001-CICD.epic.md` обновлён ссылкой на guardian story;
  - [ ] отдельная секция "Guardrails/Guardians" в `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` или в `docs/ops/gitlab-ci.md`.

## 🔎 Verification Matrix

| Check type | Required | How exactly                                                         | Evidence                         |
|-----------|----------|----------------------------------------------------------------------|----------------------------------|
| Config    | ✅       | `cat ops/guardians/guardian.config.json` и быстрая JSON-валидация  | jq/validator ok                  |
| Script    | ✅       | локально: `scripts/guardians/check-guardians.sh` с тестовыми staged файлами | вывод ошибок/ok                 |
| CI job    | ✅       | GitLab job `guardians:check` в pipeline dev-cfa2                    | зелёный статус, лог проверки     |
| Docs      | ✅       | упоминание guardians в epic/runbooks                               | `git diff` по docs/tasks         |

## 🚀 Kickoff / Plan (для агента)

1. Выписать из git-commits-analysis и текущего дерева, какие области нужно защищать (где уже был бардак).  
2. Спроектировать простой `guardian.config.json` (не overengineering) с минимальным набором правил.  
3. Реализовать `check-guardians.sh`, привязав его к staged изменениям.  
4. Добавить CI job `guardians:check` только для ветки `dev-cfa2`.  
5. Дописать документацию и обновить epic/story.

## 🔁 Loop trace

> Будет заполнен, когда фактическая реализация guardians начнётся (отдельной сессией). Сейчас story служит каркасом и индексом требований.

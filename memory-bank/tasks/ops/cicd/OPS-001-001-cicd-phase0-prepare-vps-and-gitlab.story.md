---
created: 2025-11-27 10:50
updated: 2025-11-27 11:50
type: story
sphere: [devops]
topic: [cfa2, vds1, gitlab, runner]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.1.1
tags: [cfa2, vds1, gitlab-runner, registry, glab]
epic_id: OPS-001-CICD
story_id: OPS-001-001
status: in_progress
priority: high
points: 2
---

# OPS-001-001: PHASE0 · Prepare vps + GitLab for dev-cfa2

## 👔 JTBD

Сделать так, чтобы `vds1` (runner) и `cfa2` (VPS) были подготовлены под dev-cfa2 CI/CD: runner online с тегом `vds1`, registry/SSH доступы и glab/токены на eywa1 зафиксированы и описаны.

## ✅ Definition of Done

- [ ] Runner vds1:
  - [x] gitlab-runner установлен и зарегистрирован в проекте `npk/ois-cfa`; ✅ 2025-11-27
    - Как проверяем: через GitLab UI (Settings → CI/CD → Runners) и/или `glab api /runners?scope=project&per_page=20`.
  - [x] runner показывает статус **online** в GitLab UI и имеет тег `vds1`; ✅ 2025-11-27
  - [ ] есть короткий чеклист/команда проверки статуса (make/скрипт или glab) с зафиксированными примерами вывода.
- [x] GitLab/Registry: ✅ 2025-11-27
  - [x] есть рабочий GitLab personal access token для пользователя `cicd` (переменная в `.env` на eywa1); ✅ 2025-11-27
  - [x] `glab auth status --hostname git.telex.global` зелёный и задокументирован; ✅ 2025-11-27
  - [x] `glab pipeline list --repo npk/ois-cfa --per-page 3` работает и указан в runbook. ✅ 2025-11-27
- [ ] cfa2:
  - [x] на `92.51.38.126` существует `/srv/cfa`, user `user` в sudoers; ✅ 2025-11-27
  - [x] установлен Docker + docker compose, `docker ps` и `docker compose version` работают; ✅ 2025-11-27
  - [ ] SSH-ключ `id_ed25519` для user@cfa2 зафиксирован и понятно, какой именно ключ использовать в CI (и как он должен выглядеть в CI variable).
- [ ] CI variables:
  - [ ] в GitLab CI/CD Variables создана `SSH_PRIVATE_KEY_CFA2` (masked, Unprotected для dev) с приватным ключом `user@cfa2`; **факт наличия ключа в UI есть, формат/значение ещё не подтверждены — deploy падает.**
  - [x] GITLAB_USER_CICD_TOKEN сохранён в `.env` на eywa1 и используется glab; ✅ 2025-11-27
  - [ ] переменные registry (`CI_REGISTRY`, `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`) рабочие (check docker login в job’е).
    - Как проверить из CI: отдельный debug job `docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"` и убедиться, что он зелёный.
- [ ] Docs:
  - [ ] в `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` есть раздел "PHASE0 / prerequisites" с описанием runner, SSH, glab и CI vars (с командами проверки);
  - [x] epic `OPS-001-CICD` обновлён ссылками на эту story. ✅ 2025-11-27

## 🔎 Verification Matrix

| Check type  | Required | How exactly                                                    | Evidence                            |
| ----------- | -------- | -------------------------------------------------------------- | ----------------------------------- |
| Runner      | ✅        | `make check-runner-status` или `glab api /runners`             | вывод команды, скрин GitLab runners |
| Registry    | ✅        | `docker login $CI_REGISTRY` из тестового job                   | успешный login в логах CI           |
| glab        | ✅        | `glab pipeline list --repo npk/ois-cfa --per-page 3` на eywa1  | вывод команды (в oracle / runbook)  |
| SSH to cfa2 | ✅        | `ssh user@92.51.38.126 "hostname && docker ps"`                | команда отрабатывает без пароля     |
| CI vars     | ✅        | debug-job, который эхоит, что `SSH_PRIVATE_KEY_CFA2` не пустая | лог job, отсутствие ошибок ssh-add  |

## 🚀 Kickoff / Plan (для агента)

1. Проверить runner: `make check-runner-status` или `./ops/scripts/check-gitlab-runners.sh`, свериться с GitLab UI.  
2. Проверить glab: подтянуть токен из `.env`, выполнить `glab auth status` и `glab pipeline list`.  
3. Проверить доступ на cfa2: `ssh user@92.51.38.126 "cd /srv && ls && docker ps"`.  
4. Настроить/проверить `SSH_PRIVATE_KEY_CFA2` в GitLab CI/CD Variables.  
5. Обновить runbook `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` с результатами.  
6. Зафиксировать Loop trace (см. ниже) и сделать commit.

## 🔁 Loop trace

### Loop 1 (runner + glab)
- PLAN: убедиться, что vds1 online и glab работает с git.telex.global.  
- EXECUTE:  
  - `make check-runner-status` / `./ops/scripts/check-gitlab-runners.sh`;  
  - `glab auth status --hostname git.telex.global`;  
  - `glab pipeline list --repo npk/ois-cfa --per-page 3`.  
- TESTS / CHECKS: runner online, glab команды без ошибок.  
- DOCS: обновлён раздел "CI/CD overview" в cfa2 runbook.  
- COMMIT: `chore(ops): document vds1 runner and glab setup for dev-cfa2`.

### Loop 2 (SSH + CI vars)
- PLAN: удостовериться, что CI может логиниться по SSH на cfa2.  
- EXECUTE:  
  - Настроить `SSH_PRIVATE_KEY_CFA2` в GitLab UI;  
  - добавить/запустить простой debug job, который делает `ssh-add` и `ssh user@cfa2 "hostname"`.  
- TESTS / CHECKS: в job нет ошибок libcrypto/ssh-add, ssh проходит.  
- DOCS: дописан раздел "SSH key / CI variables" в cfa2 runbook.  
- COMMIT: `fix(ci): wire SSH_PRIVATE_KEY_CFA2 for cfa2 deploy debug`.

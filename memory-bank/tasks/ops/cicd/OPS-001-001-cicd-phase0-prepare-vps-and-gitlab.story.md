---
created: 2025-11-27 10:50
updated: 2025-11-27 18:20
type: story
sphere: [devops]
topic: [cfa2, vds1, gitlab, runner]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.2.0
tags: [cfa2, vds1, gitlab-runner, registry, glab]
epic_id: OPS-001-CICD
story_id: OPS-001-001
status: done
priority: high
points: 2
---

# OPS-001-001: PHASE0 · Prepare vps + GitLab for dev-cfa2 (DoD ~100%)

## 👔 JTBD

Сделать так, чтобы `vds1` (runner) и `cfa2` (VPS) были подготовлены под dev-cfa2 CI/CD: runner online с тегом `vds1`, registry/SSH доступы и glab/токены на eywa1 зафиксированы и описаны.

## ✅ Definition of Done

- [x] Runner vds1:
  - [x] gitlab-runner установлен и зарегистрирован в проекте `npk/ois-cfa`; ✅ 2025-11-27
    - Команды:
      - `glab api '/projects/npk%2Fois-cfa/runners' | jq '.[] | {id,description,status,tag_list}'`
      - GitLab UI: Settings → CI/CD → Runners
    - Результат: runner `vds1` присутствует в списке, статус `online`, теги содержат `vds1`.
  - [x] runner показывает статус **online** в GitLab UI и имеет тег `vds1`; ✅ 2025-11-27
    - Команды:
      - та же `glab api /projects/.../runners`
    - Результат: статус `online`, `tag_list` включает `vds1`.
  - [x] есть короткий чеклист/команда проверки статуса (make/скрипт или glab) с зафиксированными примерами вывода; ✅ 2025-11-27
    - Команды:
      - `make check-runner-status` (обёртка над `./ops/scripts/check-runner-status.sh` с fallback в GitLab API mode);
      - `./ops/scripts/check-gitlab-runners.sh "$GITLAB_TOKEN" npk/ois-cfa`.
    - Результат: при отсутствии kubeconfig скрипт предупреждает и показывает список project runners через `glab api` (в т.ч. `vds1-auto-runner` online); вывод сохранён в runbook/verification.
- [x] GitLab/Registry: ✅ 2025-11-27
  - [x] есть рабочий GitLab personal access token для пользователя `cicd` (переменная в `.env` на eywa1); ✅ 2025-11-27
    - Команды:
      - `cd prj_Cifra-rwa-exachange-assets && glab auth status --hostname git.telex.global`
    - Результат: статус `Logged in as cicd`, REST/GraphQL endpoints доступны.
  - [x] `glab auth status --hostname git.telex.global` зелёный и задокументирован; ✅ 2025-11-27
    - См. выше.
  - [x] `glab pipeline list --repo npk/ois-cfa --per-page 3` работает и указан в runbook. ✅ 2025-11-27
    - Команды:
      - `glab pipeline list --repo npk/ois-cfa --per-page 3`
    - Результат: список последних pipeline’ов для dev-cfa2 выводится без ошибок.
- [x] cfa2:
  - [x] на `92.51.38.126` существует `/srv/cfa`, user `user` в sudoers; ✅ 2025-11-27
    - Команды:
      - `ssh cfa2 "hostname && ls -d /srv/cfa"`
    - Результат: хостнейм cfa2, каталог `/srv/cfa` существует.
  - [x] установлен Docker + docker compose, `docker ps` и `docker compose version` работают; ✅ 2025-11-27
    - Команды:
      - `ssh cfa2 "docker ps && docker compose version"`
    - Результат: docker/compose команды выполняются без ошибок.
  - [x] SSH-ключ `id_ed25519` для user@cfa2 зафиксирован и понятно, какой именно ключ использовать в CI (и как он должен выглядеть в CI variable); ✅ 2025-11-27
    - Команды:
      - `ssh cfa2 "ssh-keygen -lf ~/.ssh/id_ed25519.pub"`
    - Результат: fingerprint ED25519-ключа задокументирован; именно этот ключ используется в GitLab CI variable `SSH_PRIVATE_KEY_CFA2` для job `deploy-cfa2`.
- [x] CI variables:
  - [x] в GitLab CI/CD Variables создана `SSH_PRIVATE_KEY_CFA2` (masked, Unprotected для dev) с приватным ключом `user@cfa2`; ✅ 2025-11-27 (значение сейчас base64-privkey, формат исправлен d742)
    - Команды:
      - `glab api /projects/npk%2Fois-cfa/variables | jq '.[] | select(.key==\"SSH_PRIVATE_KEY_CFA2\")'`
      - проверка deploy job: `deploy-cfa2` в pipeline `#287` и последующих
    - Результат: переменная существует, `protected=false`, `masked=true`, deploy падал на старом ключе, после перезаливки ключа `deploy` прошёл.
  - [x] GITLAB_USER_CICD_TOKEN сохранён в `.env` на eywa1 и используется glab; ✅ 2025-11-27
    - Команды:
      - `cd prj_Cifra-rwa-exachange-assets && source .env; glab pipeline list --repo npk/ois-cfa --per-page 1`
    - Результат: команды glab работают, используя токен из `.env`.
  - [x] переменные registry (`CI_REGISTRY`, `CI_REGISTRY_USER`, `CI_REGISTRY_PASSWORD`) рабочие (check docker login в job’е); ✅ 2025-11-27
    - Команды:
      - просмотр `.gitlab/gitlab-ci.dev.yml` (`docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"` в шаблонах build/deploy);
      - GitLab pipelines `#290–#295` (успешные `build-*` и `deploy-cfa2`);
      - новый debug-job `registry:login-check` (stage `build`) с `ENABLE_REGISTRY_DEBUG=1` как механизм явной проверки login.
    - Результат: во всех успешных `build-*`/`deploy-cfa2` job’ах docker login проходит; при необходимости можно отдельно запускать `registry:login-check` для проверки связки CI_REGISTRY*.
- [x] Docs:
  - [x] в `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` есть раздел "PHASE0 / prerequisites" с описанием runner, SSH, glab и CI vars (с командами проверки); ✅ 2025-11-27
    - Команды:
      - просмотр `docs/deploy/vps-cfa2/cfa2-dev-runbook.md`;
    - Результат: runbook описывает `make check-runner-status`, glab, SSH к cfa2 и ключевые CI-переменные (включая `SSH_PRIVATE_KEY_CFA2` и registry).
  - [x] epic `OPS-001-CICD` обновлён ссылками на эту story. ✅ 2025-11-27
    - Команды:
      - обзор `OPS-001-CICD.epic.md`
    - Результат: в таблице Stories Index присутствует эта story.

## 🔎 Verification Matrix

| Check type  | Required | How exactly                                                    | Evidence                            | Fact / Comment                                      |
| ----------- | -------- | -------------------------------------------------------------- | ----------------------------------- |-----------------------------------------------------|
| Runner      | ✅        | `make check-runner-status` или `glab api /runners`             | вывод команды, скрин GitLab runners | ✔ `./ops/scripts/check-runner-status.sh` падает в GitLab API mode и показывает project runners (vds1 online) |
| Registry    | ✅        | `docker login $CI_REGISTRY` из тестового job                   | успешный login в логах CI           | ✔ docker login выполняется в backend/frontend build jobs и может быть явно проверен через `registry:login-check` |
| glab        | ✅        | `glab pipeline list --repo npk/ois-cfa --per-page 3` на eywa1  | вывод команды (в oracle / runbook)  | ✔ команды glab выполняются на eywa1 (`cicd` user)   |
| SSH to cfa2 | ✅        | `ssh user@92.51.38.126 "hostname && docker ps"`                | команда отрабатывает без пароля     | ✔ ssh alias `cfa2` работает, docker ps на хосте     |
| CI vars     | ✅        | debug-job, который эхоит, что `SSH_PRIVATE_KEY_CFA2` не пустая | лог job, отсутствие ошибок ssh-add  | ✔ `deploy-cfa2` использует новый ключ; старый libcrypto error устранён |

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

### Loop 3 (registry login + PHASE0 docs)
- PLAN: зафиксировать работоспособность registry vars и добавить явную проверку login.  
- EXECUTE:  
  - в `.gitlab/gitlab-ci.dev.yml` добавлен debug-job `registry:login-check` (stage `build`, запускается при `ENABLE_REGISTRY_DEBUG=1`);  
  - подтверждено, что существующие `build-*` и `deploy-cfa2` jobs используют `docker login` с `CI_REGISTRY*`;  
  - обновлён runbook `cfa2-dev-runbook.md` (разделы PHASE0 / Backend dev pipeline / Frontends and SDK).  
- TESTS / CHECKS: успешные pipeline’ы `#290–#295` показывают зелёные `build-*` и `deploy-cfa2` (docker login не падает).  
- DOCS: обновлены story DoD/Verification Matrix и PHASE0-разделы runbook + CI-BUILD-MATRIX.  
- COMMIT: `chore(ci): add registry login debug job and document PHASE0 checks for dev-cfa2`.

---
created: 2025-11-27 10:55
updated: 2025-11-27 18:25
type: story
sphere: [devops]
topic: [cfa2, cicd, backend]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.2.0
tags: [cfa2, backend, docker-compose, gitlab-ci, dev-cfa2]
epic_id: OPS-001-CICD
story_id: OPS-001-002
status: done
priority: high
points: 3
---

# OPS-001-002: PHASE1 · Backend dev pipeline for cfa2 (DoD ~100%)

## 👔 JTBD

Сделать так, чтобы ветка `dev-cfa2` собирала и деплоила все backend-сервисы (`api-gateway`, `identity`, `issuance`, `registry`, `settlement`, `compliance`, `bank-nominal`) на `cfa2` через статичный `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` без генерации файлов на деплое.

## ✅ Definition of Done

- [x] Compose/Env:
  - [x] `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` содержит postgres, keycloak, minio, redis и все backend-сервисы;
    - Команды:
      - `cd ois-cfa && sed -n '1,260p' deploy/docker-compose-at-vps/cfa2/docker-compose.yml`
      - `ssh cfa2 "cd /srv/cfa && docker compose ps"`
    - Результат: на cfa2 подняты `postgres`, `keycloak`, `minio`, `redis` и все backend-сервисы (identity/issuance/registry/settlement/compliance/bank-nominal) плюс api-gateway.
  - [x] все образы backend’ов используют `${REGISTRY_IMAGE}/<service>:${TAG}` без прямого `CI_REGISTRY_IMAGE`;
    - Команды:
      - просмотр compose: значения image выглядят как `${REGISTRY_IMAGE}/<service>:${TAG}`
    - Результат: compose ссылается на `${REGISTRY_IMAGE}`/`${TAG}`, CI публикует `:dev` тег.
  - [x] `.env.cfa2` содержит `REGISTRY_IMAGE`, фиксированный `TAG` (например, `dev`), порты и KAFKA/Keycloak настройки.
    - Команды:
      - `ssh cfa2 "cd /srv/cfa && cat .env"`
    - Результат: есть `REGISTRY_IMAGE=git.telex.global:5050/npk/ois-cfa`, `TAG=dev`, порты 5808x/300x, `KAFKA_ENABLED=false`.
- [x] CI build (backend):
  - [x] в `.gitlab/gitlab-ci.dev.yml` есть jobs `build-api-gateway`, `build-identity`, `build-issuance`, `build-registry`, `build-settlement`, `build-compliance`, `build-bank-nominal`;
    - Команды:
      - `sed -n '100,220p' .gitlab/gitlab-ci.dev.yml`
    - Результат: все перечисленные jobs присутствуют и наследуют `*build_backend_template`.
  - [x] каждый job использует `docker:24` + `docker:24-dind` и логинится в `$CI_REGISTRY`;
    - Команды:
      - просмотр шаблона `.build_backend_template` в `.gitlab/gitlab-ci.dev.yml`
    - Результат: шаблон содержит `image: docker:24.0`, `services: [docker:24.0-dind]` и `docker login ... "$CI_REGISTRY"`.
  - [x] каждый job пушит `$CI_REGISTRY_IMAGE/<image>:$CI_COMMIT_SHORT_SHA` и, для ветки `dev-cfa2`, тегирует как `:$DEPLOY_TAG`;
    - Команды:
      - чтение скрипта в шаблоне `*build_backend_template`
    - Результат: `docker build -t "$CI_REGISTRY_IMAGE/${IMAGE_NAME}:$CI_COMMIT_SHORT_SHA" ...`, далее tag/push `:${DEPLOY_TAG}` при `dev-cfa2`.
  - [x] jobs имеют `rules` для `dev-cfa2` (+ позже path-based changes, см. след. story).
    - Команды:
      - `sed -n '114,220p' .gitlab/gitlab-ci.dev.yml`
    - Результат: `rules` с `if: '$CI_COMMIT_BRANCH == "dev-cfa2"'` и `changes:`+`FORCE_BUILD_ALL`, а path-based behavior завязан на `CI_PIPELINE_SOURCE=="push"`.
- [x] CI deploy:
  - [x] job `deploy-cfa2` в стадии `deploy` использует runner `vds1` и `SSH_PRIVATE_KEY_CFA2`;
    - Команды:
      - `sed -n '260,340p' .gitlab/gitlab-ci.dev.yml`
      - GitLab pipeline `#287`, `#290`, `#291`
    - Результат: `tags: [vds1]`, `before_script` собирает ключ из `SSH_PRIVATE_KEY_CFA2`, deploy jobs выполняются на vds1.
  - [x] job выполняет `docker login` в registry и затем по SSH: `cd /srv/cfa && REGISTRY_IMAGE=$CI_REGISTRY_IMAGE TAG=$DEPLOY_TAG docker compose pull && docker compose up -d`;
    - Команды:
      - лог `deploy-cfa2` в pipeline `#287` и `#290`
    - Результат: в job выполняются команды pull/up через SSH на cfa2.
  - [x] job **не** заменяет `.env.cfa2` или `docker-compose.yml` на cfa2, только использует их.
    - Результат: deploy job не копирует файлы, только использует уже лежащий bundle в `/srv/cfa`.
- [x] Runtime:
  - [x] после успешного deploy `ssh user@cfa2 "cd /srv/cfa && docker compose ps"` показывает все backend-контейнеры в состоянии `running` (без CrashLoop);
    - Команды:
      - `ssh cfa2 "cd /srv/cfa && docker compose ps"`
    - Результат: все backend сервисы и gateway в статусе `Up`.
  - [x] `curl http://92.51.38.126:58081/swagger` и swagger остальных сервисов отвечают 200/HTML без 5xx;
    - Команды:
      - `curl -v --max-time 5 http://92.51.38.126:58081/swagger`
    - Результат: 301/200 на swagger index; другие сервисы по swagger-URL проверены ранее в w4/w21 сессиях.
  - [x] KAFKA опционально выключен (`Kafka__Enabled=false`) для стабильности, как описано в документации.
    - Команды:
      - `ssh cfa2 "cd /srv/cfa && grep KAFKA_ENABLED .env"`
    - Результат: `KAFKA_ENABLED=false`.
- [x] Docs:
  - [x] `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` содержит секцию "Backend dev pipeline" с: стадиями, именами jobs, портами, примером проверки; ✅ 2025-11-27
    - Команды:
      - просмотр `docs/deploy/vps-cfa2/cfa2-dev-runbook.md`;
    - Результат: разделы "PHASE0 / prerequisites" и "Backend dev pipeline" описывают runner/registry/SSH, список backend build jobs, stage-порядок (`sdk → build → deploy`), порты и ручную проверку через `docker compose ps` + swagger.
  - [x] `docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md` отражает backend jobs и их пути. ✅ 2025-11-27
    - Команды:
      - просмотр `docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md`;
    - Результат: матрица содержит строки `build-*` backend’ов с корректными `services/*` + `packages/contracts|domain|types`, а также общий раздел про стадии и переменные (`FORCE_BUILD_ALL`, `CI_PIPELINE_SOURCE=="push"`).

## 🔎 Verification Matrix

| Check type | Required | How exactly                                                                                      | Evidence                             | Fact / Comment                               |
|-----------|----------|---------------------------------------------------------------------------------------------------|--------------------------------------|----------------------------------------------|
| Compose   | ✅       | `docker compose --env-file deploy/.../.env.cfa2 -f deploy/.../docker-compose.yml config`         | команда 0 exit, без ошибок           | ✔ текущий compose корректен, stack работает  |
| Build     | ✅       | GitLab pipeline на `dev-cfa2`: все `build-*` backend зелёные                                      | ссылка на pipeline, список jobs      | ✔ `#287`, `#290`, `#291` — backend `build-*` success |
| Deploy    | ✅       | job `deploy-cfa2` успешен, нет ошибок ssh-agent/libcrypto/docker compose                          | лог job в GitLab                     | ✔ `deploy-cfa2` зелёный после фикса SSH key  |
| Runtime   | ✅       | `ssh user@cfa2 "cd /srv/cfa && docker compose ps"`, curl swagger/health                          | вывод команд, HTTP 200               | ✔ все backend контейнеры Up, swagger доступен |
| Docs      | ✅       | diff по `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` и `CI-BUILD-MATRIX.md`                        | `git diff` в отчёте агента           | ✔ Docs обновлены: backend секция в runbook + backend строки в CI-BUILD-MATRIX согласованы с pipelines #287–#295 |

## 🚀 Kickoff / Plan (для агента)

1. Прочитать текущий `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` и `.env.cfa2`, сверить с портами/сервисами из docs.  
2. Проверить `.gitlab/gitlab-ci.dev.yml` на наличие всех backend build jobs и deploy-cfa2.  
3. Прогнать локально `docker compose config` (env-файл из deploy/cfa2).  
4. Синхронизировать bundle на cfa2 через `./ops/scripts/sync-compose-cfa2.sh user@92.51.38.126 /srv/cfa`.  
5. Пуш в `dev-cfa2`, дождаться pipeline, проверить `build-*` и `deploy-cfa2`.  
6. Обновить runbook + CI-BUILD-MATRIX, зафиксировать Loop trace и сделать commit.

## 🔁 Loop trace

### Loop 1 (compose/env)
- PLAN: убедиться, что compose/env для cfa2 корректны и в одном месте.  
- EXECUTE: правки `deploy/docker-compose-at-vps/cfa2/*`, `docker compose config`, `sync-compose-cfa2.sh`.  
- TESTS / CHECKS: локальный и удалённый `docker compose config` успешны.  
- DOCS: минимум — короткая пометка в runbook о пути к compose/env.  
- COMMIT: `chore(deploy): align cfa2 compose/env under deploy/docker-compose-at-vps`.

### Loop 2 (build jobs)
- PLAN: довести backend build jobs до зелёного состояния.  
- EXECUTE: правки `.gitlab/gitlab-ci.dev.yml`, пуш в `dev-cfa2`.  
- TESTS / CHECKS: pipeline, все `build-*` backend зелёные.  
- DOCS: обновлён CI-BUILD-MATRIX.  
- COMMIT: `chore(ci): stabilize backend builds for dev-cfa2`.

### Loop 3 (deploy job)
- PLAN: добиться успешного `deploy-cfa2` и рабочих swagger’ов.  
- EXECUTE: отладка SSH ключа/переменных, перезапуск pipeline.  
- TESTS / CHECKS: `deploy-cfa2` успешен, swagger отвечает.  
- DOCS: runbook: шаги "Как задеплоить backend stack на cfa2".  
- COMMIT: `fix(ci): make deploy-cfa2 green for dev-cfa2`.

### Loop 4 (backend docs + CI matrix)
- PLAN: зафиксировать сделанную работу по backend pipeline в документации.  
- EXECUTE:  
  - дополнен runbook `cfa2-dev-runbook.md` (секции "Backend dev pipeline" и ручные проверки swagger/портов);  
  - обновлена матрица `CI-BUILD-MATRIX.md` для backend jobs и стадий.  
- TESTS / CHECKS: пересмотрены успешные pipeline’ы `#287–#295` (все backend `build-*` + `deploy-cfa2` зелёные и соответствуют описанию).  
- DOCS: обновлены DoD/Verification Matrix для PHASE1 и epic.  
- COMMIT: `docs(ci): document backend dev pipeline and CI build matrix for dev-cfa2`.

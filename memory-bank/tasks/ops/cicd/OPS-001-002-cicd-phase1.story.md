---
created: 2025-11-27 10:55
updated: 2025-11-27 11:50
type: story
sphere: [devops]
topic: [cfa2, cicd, backend]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.1.1
tags: [cfa2, backend, docker-compose, gitlab-ci, dev-cfa2]
epic_id: OPS-001-CICD
story_id: OPS-001-002
status: in_progress
priority: high
points: 3
---

# OPS-001-002: PHASE1 · Backend dev pipeline for cfa2

## 👔 JTBD

Сделать так, чтобы ветка `dev-cfa2` собирала и деплоила все backend-сервисы (`api-gateway`, `identity`, `issuance`, `registry`, `settlement`, `compliance`, `bank-nominal`) на `cfa2` через статичный `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` без генерации файлов на деплое.

## ✅ Definition of Done

- [ ] Compose/Env:
  - [ ] `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` содержит postgres, keycloak, minio, redis и все backend-сервисы;
  - [ ] все образы backend’ов используют `${REGISTRY_IMAGE}/<service>:${TAG}` без прямого `CI_REGISTRY_IMAGE`;
  - [ ] `.env.cfa2` содержит `REGISTRY_IMAGE`, фиксированный `TAG` (например, `dev`), порты и KAFKA/Keycloak настройки.
- [ ] CI build (backend):
  - [ ] в `.gitlab/gitlab-ci.dev.yml` есть jobs `build-api-gateway`, `build-identity`, `build-issuance`, `build-registry`, `build-settlement`, `build-compliance`, `build-bank-nominal`;
  - [ ] каждый job использует `docker:24` + `docker:24-dind` и логинится в `$CI_REGISTRY`;
  - [ ] каждый job пушит `$CI_REGISTRY_IMAGE/<image>:$CI_COMMIT_SHORT_SHA` и, для ветки `dev-cfa2`, тегирует как `:$DEPLOY_TAG`;
  - [ ] jobs имеют `rules` для `dev-cfa2` (+ позже path-based changes, см. след. story).
- [ ] CI deploy:
  - [ ] job `deploy-cfa2` в стадии `deploy` использует runner `vds1` и `SSH_PRIVATE_KEY_CFA2`;
  - [ ] job выполняет `docker login` в registry и затем по SSH: `cd /srv/cfa && REGISTRY_IMAGE=$CI_REGISTRY_IMAGE TAG=$DEPLOY_TAG docker compose pull && docker compose up -d`;
  - [ ] job **не** заменяет `.env.cfa2` или `docker-compose.yml` на cfa2, только использует их.
- [ ] Runtime:
  - [ ] после успешного deploy `ssh user@cfa2 "cd /srv/cfa && docker compose ps"` показывает все backend-контейнеры в состоянии `running` (без CrashLoop);
  - [ ] `curl http://92.51.38.126:58081/swagger` и swagger остальных сервисов отвечают 200/HTML без 5xx;
  - [ ] KAFKA опционально выключен (`Kafka__Enabled=false`) для стабильности, как описано в документации.
- [ ] Docs:
  - [ ] `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` содержит секцию "Backend dev pipeline" с: стадиями, именами jobs, портами, примером проверки;
  - [ ] `docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md` отражает backend jobs и их пути.

## 🔎 Verification Matrix

| Check type | Required | How exactly                                                                                      | Evidence                             |
|-----------|----------|---------------------------------------------------------------------------------------------------|--------------------------------------|
| Compose   | ✅       | `docker compose --env-file deploy/.../.env.cfa2 -f deploy/.../docker-compose.yml config`         | команда 0 exit, без ошибок           |
| Build     | ✅       | GitLab pipeline на `dev-cfa2`: все `build-*` backend зелёные                                      | ссылка на pipeline, список jobs      |
| Deploy    | ✅       | job `deploy-cfa2` успешен, нет ошибок ssh-agent/libcrypto/docker compose                          | лог job в GitLab                     |
| Runtime   | ✅       | `ssh user@cfa2 "cd /srv/cfa && docker compose ps"`, curl swagger/health                          | вывод команд, HTTP 200               |
| Docs      | ✅       | diff по `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` и `CI-BUILD-MATRIX.md`                        | `git diff` в отчёте агента           |

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

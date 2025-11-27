---
created: 2025-11-27 11:00
updated: 2025-11-27 18:30
type: story
sphere: [devops]
topic: [cfa2, cicd, frontend, sdk, rules]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.2.0
tags: [cfa2, frontends, portal-issuer, portal-investor, backoffice, sdk, rules]
epic_id: OPS-001-CICD
story_id: OPS-001-003
status: in_progress
priority: high
points: 3
---

# OPS-001-003: PHASE2 · Frontends + path-based builds + SDK jobs (DoD ~90%)

## 👔 JTBD

Сделать так, чтобы фронты (`portal-issuer`, `portal-investor`, `backoffice`) собирались и деплоились через dev-cfa2 pipeline вместе с backend’ами, с path-based rules для всех build jobs и отдельными `sdk` jobs (validate-specs/generate-sdks), которые триггерятся только при изменении contracts/SDK.

## ✅ Definition of Done

- [x] Compose (frontends):
  - [x] в `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` есть сервисы `portal-issuer`, `portal-investor`, `backoffice`;
  - [x] каждый фронт использует `${REGISTRY_IMAGE}/<image>:${TAG}` и пробрасывает `NEXT_PUBLIC_*` в соответствии с cfa2 (API gateway + Keycloak);
  - [x] порты: 3001/3002/3003 на хосте cfa2 указаны в `.env` на cfa2 и документации.
- [x] CI build (frontends):
  - [x] есть jobs `build-portal-issuer`, `build-portal-investor`, `build-backoffice`;
  - [x] каждый job:
    - [x] выполняет `npm ci && npm run build` в соответствующем `apps/*` перед docker build;
    - [x] прокидывает `NEXT_PUBLIC_*` (API_BASE_URL, KEYCLOAK_URL, REALM, CLIENT_ID) через `--build-arg`;
    - [x] пушит образы в `$CI_REGISTRY_IMAGE/<image>:$CI_COMMIT_SHORT_SHA` и `:$DEPLOY_TAG` на `dev-cfa2`.
- [x] SDK stage:
  - [x] stage `sdk` присутствует перед `build` в `.gitlab/gitlab-ci.dev.yml`;
  - [x] job `validate-specs` валидирует OpenAPI/AsyncAPI/JSON Schemas (`make validate-specs` или эквивалент) и отрабатывает только при изменениях в `packages/contracts/**` и `packages/types/**` (для push-пайплайнов);
  - [x] job `generate-sdks` перегенерирует TS SDK (`packages/sdks/ts`) и запускается только при ENABLE_SDK_JOBS == 1 и изменениях в `packages/contracts/**`, `packages/sdks/**`, `packages/types/**` (для push-пайплайнов);
  - [x] build jobs помечены `needs` на sdk jobs (optional), чтобы ломанный контракт ломал сборку раньше.
- [x] Path-based rules:
  - [x] для backend jobs настроены `rules:changes`, которые ограничивают запуск соответствующими `services/<name>/**` + общими пакетами;
  - [x] для frontend jobs `rules:changes` включают `apps/<app>/**`, `apps/shared-ui/**`, `packages/contracts/**`, `packages/sdks/**`, `packages/types/**`;
  - [x] для sdk jobs заданы `rules:changes` по contracts/sdks/types, и они срабатывают только при `CI_PIPELINE_SOURCE=="push"` (API-пайплайны не триггерят path-based).
- [x] Runtime:
  - [x] после deploy `curl http://92.51.38.126:3001`/`3002`/`3003` возвращает HTML (Next.js заголовки Issuer/Investor/Backoffice видны);
  - [ ] фронты корректно обращаются к gateway/Keycloak на cfa2 (env ссылками, без localhost) — требуется отдельная донастройка Keycloak/NextAuth (сейчас есть `/api/auth/error?error=Configuration` на investor).
- [x] Docs:
  - [x] `docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md` отражает path-based rules и sdk stage; ✅ 2025-11-27
    - Команды:
      - просмотр `docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md`;
    - Результат: матрица содержит строки для `validate-specs`/`generate-sdks`, всех backend и frontend `build-*` jobs, а также `deploy-cfa2` и `registry:login-check` с указанием paths и условий (`CI_PIPELINE_SOURCE=="push"`, `FORCE_BUILD_ALL`, `ENABLE_SDK_JOBS`).
  - [x] `docs/deploy/vps-cfa2/cfa2.md` / `cfa2-dev-runbook.md` содержат секцию "Frontends on cfa2" с портами и проверками. ✅ 2025-11-27
    - Команды:
      - просмотр `docs/deploy/vps-cfa2/cfa2-dev-runbook.md`;
    - Результат: runbook дополнили разделы "Frontends and SDK (PHASE2)" и список портов 3001/3002/3003 с базовыми curl-проверками HTML.

## 🔎 Verification Matrix

| Check type      | Required | How exactly                                                                                  | Evidence                           | Fact / Comment                                                                 |
|----------------|----------|-----------------------------------------------------------------------------------------------|------------------------------------|-------------------------------------------------------------------------------|
| Frontend build | ✅       | локально или в CI: `npm ci && npm run build` для каждого apps/*                            | успешный build, отсутствие ошибок  | ✔ локально `npm run build` для portal-issuer/investor/backoffice зелёные     |
| CI rules       | ✅       | GitLab pipeline: при правке только одного сервиса/приложения запускаются только нужные jobs | скрин pipeline, список jobs        | ✔ TC1–TC3 на push: 289 (CI-only), 290 (registry-only), 291 (issuer-only)     |
| SDK jobs       | ✅       | при изменении contracts/types запускаются `validate-specs`/`generate-sdks`                   | логи sdk stage                     | ✔ validate-specs и generate-sdks завязаны на contracts/types + ENABLE_SDK_JOBS |
| Runtime        | ✅       | `curl http://92.51.38.126:3001`/`3002`/`3003` + базовый логин-флоу (минимум, без e2e)        | вывод curl/скрин UI                | ◑ HTML фронтов открывается; логин через Keycloak ещё доводится в OPS-001-005 |

### Test Cases (path-based CI on push)

- **TC1 – CI-only change (no services/apps/packages)**  
  - Commit: только `.gitlab/gitlab-ci.dev.yml` / `AGENTS.md` / docs.  
  - Pipeline: `#289` (source: `push`, SHA `6a77272...`).  
  - Jobs: `deploy-cfa2` = success; `validate-specs`/`generate-sdks` и все `build-*` jobs = skipped (path-based rules не трогают CI-only изменения).  
  - Статус: **PASS** (path-based logic для "CI-only" работает, лишних сборок нет).  
- **TC2 – single backend change (registry-only)**  
  - Change: `services/registry/ci-tc2-registry.md`.  
  - Pipeline: `#290` (source: `push`, SHA `3855d3b2...`).  
  - Jobs: `build-registry` + `deploy-cfa2` = success; другие backend/frontend build jobs = skipped.  
  - Статус: **PASS** (меняется только registry, билдится только `build-registry`).  
- **TC3 – single frontend change (portal-issuer-only)**  
  - Change: `apps/portal-issuer/ci-tc3-portal-issuer.md`.  
  - Pipeline: `#291` (source: `push`, SHA `a72f4897...`).  
  - Jobs: `build-portal-issuer` + `deploy-cfa2` = success; остальные фронты и все backend build jobs = skipped.
  - Статус: **PASS** (меняется только portal-issuer, билдится только соответствующий frontend image).

## 🚀 Kickoff / Plan (для агента)

1. Проверить Dockerfile’ы фронтов и убедиться, что они принимают `NEXT_PUBLIC_*` через ARG/ENV (при необходимости доработать).  
2. Убедиться, что compose для cfa2 содержит фронты и корректные порты.  
3. Настроить frontend build jobs: добавить `APP_PATH`, `npm ci && npm run build`, build-args.  
4. Добавить/уточнить sdk stage (`validate-specs`, `generate-sdks`) и dependencies.  
5. Настроить `rules:changes` для всех jobs по архитектурной карте (`artifacts/AlexA/ois-cfa.reposcan.json`).  
6. Запустить pipeline на `dev-cfa2` (при необходимости с `FORCE_BUILD_ALL=1`) и убедиться, что все фронты и sdk jobs работают.  
7. Обновить CI-BUILD-MATRIX + runbooks, зафиксировать Loop trace и сделать commit.

## 🔁 Loop trace

### Loop 1 (front build + compose)
- PLAN: собрать и поднять фронты на cfa2 вместе с backend’ами.  
- EXECUTE: правки Dockerfile’ов/compose, локальные `npm run build`, sync на cfa2 и manual `docker compose up`.  
- TESTS / CHECKS: локальные build’ы зелёные, фронты открываются по IP/портам.  
- DOCS: дописана секция "Frontends on cfa2" в runbook.  
- COMMIT: `feat(ci): add cfa2 frontends containers and builds`.

### Loop 2 (sdk stage)
- PLAN: вынести validate-specs/generate-sdks в отдельную стадию.  
- EXECUTE: добавить sdk jobs в `.gitlab/gitlab-ci.dev.yml`, настроить `rules:changes`.  
- TESTS / CHECKS: при правке contracts/types/sdk sdk stage запускается и падает/проходит ожидаемо.  
- DOCS: отражено в CI-BUILD-MATRIX.  
- COMMIT: `feat(ci): add sdk stage for contracts and sdks`.

### Loop 3 (path-based rules)
- PLAN: минимизировать лишние сборки, чтобы не гонять все образы при каждой правке.  
- EXECUTE: настроить `rules:changes` для backend/frontend/sdk jobs по реальным путям.  
- TESTS / CHECKS: несколько экспериментальных коммитов с правкой только одного сервиса/приложения.  
- DOCS: CI-BUILD-MATRIX показывает маппинг "service → paths".  
- COMMIT: `chore(ci): tighten path-based rules for dev-cfa2`.

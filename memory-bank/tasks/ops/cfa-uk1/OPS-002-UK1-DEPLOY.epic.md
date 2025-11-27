---
created: 2025-11-27 12:25
updated: 2025-11-27 12:25
type: epic
sphere: [devops]
topic: [uk1, cfa, deploy]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.1.0
tags: [uk1, devops, deploy, develop, vps, cloudflare, playwright]
epic_id: OPS-002-UK1-DEPLOY
status: in_progress
---

# OPS-002-UK1-DEPLOY: Safe deploy of `develop` to UK1

## 🎯 Epic JTBD

Сделать так, чтобы ветка `develop` могла стабильно деплоиться на сервер `uk1` (`185.168.192.214`, домены `*.cfa.llmneighbors.com`) без риска поломать текущий рабочий снапшот `/opt/ois-cfa`, с понятным rollback-планом, health-checkами и e2e‑проверками через Playwright.

Источник контекста и начальный план:  
`memory-bank/Scrum/20251126-cicd-cfa2/20251127-1208-deploy-develop-branch-on-uk1-carefully.report.md`.

## 🗂 Stories Index (Story-JTBD)

| Story ID    | File path                                                                 | JTBD (кратко)                                                     | Status      |
|------------|---------------------------------------------------------------------------|-------------------------------------------------------------------|------------|
| OPS-002-001 | `tasks/ops/cfa-uk1/OPS-002-001-uk1-phase0-snapshot-and-branch.story.md`  | Зафиксировать текущее состояние UK1 и выбрать release‑ветку      | planned    |
| OPS-002-002 | `tasks/ops/cfa-uk1/OPS-002-002-uk1-phase1-new-release-folder.story.md`   | Подготовить безопасный git‑базированный release‑каталог на UK1   | planned    |
| OPS-002-003 | `tasks/ops/cfa-uk1/OPS-002-003-uk1-phase2-health-and-swap.story.md`      | Прогнать health/e2e и аккуратно переключить runtime на release   | planned    |

## 🔍 Acceptance (Epic-level DoD)

- [ ] Определена и зафиксирована ветка‑источник для UK1 (например, `release/uk1-develop-YYYYMMDD`, основанная на `develop`), с кратким changelog по сравнению с текущим снапшотом UK1.
- [ ] На UK1 существует отдельный release‑каталог (`/opt/ois-cfa_releases/ois-cfa_YYYYMMDD`) с чистым git‑репозиторием и понятной структурой (`docker-compose*.yml`, `.env`, `apps/*/.env.local`).
- [ ] Перед переключением выполнены и зафиксированы:
  - [ ] HTTP health‑чеки (`/health`, `/health/ready`, порталы/Keycloak);
  - [ ] минимум один Playwright‑сценарий логина (Issuer/Investor или Backoffice).
- [ ] Выполнен как минимум один успешный swap:
  - [ ] старый `/opt/ois-cfa` сохранён (например, `/opt/ois-cfa_old_YYYYMMDD-HHMM`);
  - [ ] новый release‑каталог становится основным `/opt/ois-cfa`, все сервисы работают.
- [ ] В `memory-bank/Scrum/20251126-cicd-cfa2/` есть финальный отчёт по этому Epic (с командами, выводами, указанием commit‑hash’ей `develop`/release).

## 🔁 Epic Loop trace

> Заполняется по мере выполнения stories: ссылки на отчёты в memory‑bank, коммиты ветки `develop`/`release/uk1-*`, даты деплоев и проблем/фиксов.


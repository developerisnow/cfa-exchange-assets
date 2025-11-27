---
created: 2025-11-27 19:42
updated: 2025-11-27 19:42
type: story
sphere: [devops]
topic: [cicd, observability, monitoring]
author: alex
agentID: to-be-decided
version: 0.1.0
tags: [otel, signoz, prometheus, grafana, alerts]
epic_id: OPS-001-CICD
story_id: OPS-001-006
status: planned
priority: medium
points: 3
---

# OPS-001-006: PHASE5 · CI/CD observability & monitoring (Signoz / OTEL / Prometheus)

## 👔 JTBD

Сделать так, чтобы CI/CD и runtime cfa2 были наблюдаемыми:

- есть базовый мониторинг здоровья (pipelines, runner vds1, deploy jobs, key services на cfa2),
- есть минимальная трассировка/метрики (через OTEL → Signoz или стек Prometheus+Grafana),
- есть уведомления по ключевым инцидентам (pipeline failures, TLS expiry, недоступность порталов/API).

## ✅ Definition of Done

- [ ] CI-level observability:
  - [ ] определён и реализован источник метрик/логов по GitLab pipelines/dev-cfa2 (например, GitLab webhooks → Signoz/Prometheus или отдельный exporter);
  - [ ] есть дашборд “dev-cfa2 CI health” (pipelines success rate, duration, queue time, guardians failures);
  - [ ] есть базовые алерты: “dev-cfa2 pipeline consecutively failing”, “guardians:check fails N раз подряд”.
- [ ] Runtime-level observability (cfa2):
  - [ ] собраны метрики по ключевым компонентам (`api-gateway`, ключевые backend сервисы, порталы, keycloak);
  - [ ] есть дашборды:
    - [ ] “cfa2 backend” — HTTP 5xx/latency по api-gateway и сервисам;
    - [ ] “cfa2 portals” — login error rate (NextAuth/Keycloak), response times;
    - [ ] “cfa2 system” — CPU/RAM/disk.
- [ ] Telemetry stack:
  - [ ] принято решение: единый OTEL→Signoz или связка Prometheus+Grafana (или гибрид);
  - [ ] выбран и описан способ доставки сигналов (sidecar, agent, export через OTEL SDK/collector);
  - [ ] зафиксирован минимальный набор стандартных labels/tags (service, env, version, pipeline_id).
- [ ] Alerts & notifications:
  - [ ] настроены уведомления по TLS expiry (LE) с указанием:
    - источника истины (certbot / cert-manager / Signoz/Prometheus),
    - каналов доставки (Telegram, email, GitLab alerts);
  - [ ] настроен хотя бы один alert → Telegram/канал/бот (credentials и чат-id описаны в секрете / docs).
- [ ] Docs:
  - [ ] обновлён `OPS-001-CICD.epic.md` разделом “Observability”;
  - [ ] добавлен runbook `docs/ops/observability-cicd.md`:
    - архитектура стека,
    - какие dashboards есть и как их читать,
    - как добавлять новые метрики/алерты.

## 🔎 Verification Matrix

| Check type | Required | How exactly | Evidence | Fact / Comment |
|-----------|----------|-------------|----------|----------------|
| CI dashboards | ✅ | открыть дашборд “dev-cfa2 CI health” и убедиться, что данные обновляются | скриншоты / ссылки | ☐ ещё не делалось |
| Runtime dashboards | ✅ | открыть дашборды backend/portals/system | скриншоты / ссылки | ☐ ещё не делалось |
| TLS alerts | ✅ | спровоцировать near-expiry (или dry-run) и увидеть alert | логи alerting-системы | ☐ не реализовано |
| Telegram/GitLab alerts | ✅ | отправить тестовое уведомление | сообщение в канале / GitLab | ☐ не реализовано |

## 🚀 Kickoff / Plan (для будущего агента)

1. Собрать текущий контекст: какие метрики/логи уже доступны (GitLab, cfa2, uk1/cfa1), какие инструменты уже развернуты (если есть Signoz/Prometheus).  
2. Предложить минимальный стек (например, OTEL collector + Signoz “all-in-one” на отдельном VPS) и согласовать его.  
3. Подключить GitLab CI (webhooks/API) и cfa2 (exporters/OTEL) к выбранному стеку.  
4. Сконфигурировать базовые дашборды и алерты, проверить их.  
5. Описать всё в docs + отметить DoD/Verification Matrix в этой story.


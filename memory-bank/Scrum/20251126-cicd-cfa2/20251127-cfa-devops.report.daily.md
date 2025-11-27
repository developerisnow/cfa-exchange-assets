---
created: 2025-11-27 20:10
updated: 2025-11-27 20:10
type: daily-report
sphere: [devops]
topic: [cfa2, cicd, cloudflare, portals]
author: alex
version: 0.1.0
tags: [daily, report, cfa2, dev-cfa2]
---

# Ежедневный отчёт — 2025-11-27 — DevOps (cfa2 / dev-cfa2)

## Что делал (по факту, 10:00–20:00)

- Утро: поднял и синхронизировал контекст по OPS-001 (PHASE0–PHASE3) для dev-cfa2:
  - перечитал все сториз `OPS-001-001..005`, AGENTS, cicd-cheatsheet, старые сессии по uk1/cfa1;
  - выровнял описание runner’а vds1, SSH к cfa2, GitLab/glab, CI vars в `OPS-001-001` и runbook’е.
- Днём: стабилизировал dev-cfa2 CI pipeline (backend + front + SDK):
  - проверил и задокументировал path-based rules (TC1–TC3) для backend и фронтов (pipelines #289–291);
  - добавил debug‑job `registry:login-check` и обновил `check-runner-status.sh` (fallback в GitLab API режим);
  - оформил `docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md` и `cfa2-dev-runbook.md` так, чтобы по ним можно было понять кто что билдит и в каком порядке.
- После обеда: занялся Cloudflare/Keycloak/порталами на cfa2:
  - сверил DNS/ingress по теlex.global и настройку vhost’а `cfa2-portals.conf` с uk1/cfa1;
  - привёл Keycloak realm `ois` и клиенты `portal-issuer|investor|backoffice` к доменной схеме `*.cfa2.telex.global`;
  - убедился, что `NEXT_PUBLIC_*` и `NEXTAUTH_URL` на cfa2 смотрят только на домены (без IP и без `:58080`).
- Вечер: подготовил архитектурную документацию и “операторские” шпаргалки:
  - нарисовал mermaid‑диаграммы CI/CD и ingress в `OPS-001-CICD-architecture.md`
    (как образы идут через vds1 → GitLab Registry → deploy-cfa2 → cfa2);
  - сделал ADHD‑friendly cheatsheet `OPS-001-CICD-cheatsheet.md` с командами для runner/glab, build/deploy, Playwright и guardians;
  - сменил контактный email для Let’s Encrypt на cfa2 (`certbot update_account --email alex.ocr.ai.llm@gmail.com`) и прописал это в сториз.
- Параллельно: готовил промпты/инструкции для следующих агентов:
  - собрал финализирующий промпт для Cloudflare/Keycloak агента `OPS-001-005-cfa2-cloudflare-finalizer.prompt.md`;
  - добавил story `OPS-001-006` под observability/monitoring CI/CD (Signoz/OTEL/Prometheus и TLS‑alerts в Telegram).

## Что получилось / основные результаты

- PHASE0–PHASE2 по dev-cfa2:
  - runner vds1, SSH к cfa2 и GitLab/glab теперь описаны и проверяются одной командой (`check-runner-status.sh`);
  - backend и фронтовые сборки на dev-cfa2 работают по path‑based правилам, без лишних билдов для “CI‑only” коммитов;
  - SDK‑стадия вынесена отдельно и завязана на contracts/sdks/types, описана в CI‑матрице.
- Cloudflare/Keycloak/порталы на cfa2:
  - DNS и TLS для `*.cfa2.telex.global` в порядке, nginx‑vhost отражён в сториз;
  - realm `ois`, клиенты и env порталов приведены к чистой HTTPS‑схеме (без `https://...:58080`), логин‑формы грузятся с Keycloak по домену.
- Документация:
  - есть единый архитектурный файл для OPS‑001 (CI, registry, ingress, certs);
  - есть cheatsheet для быстрых операций DevOps по dev-cfa2 (build/deploy, Playwright, guardians).
- Безопасность/надёжность:
  - контактный email LE на cfa2 переведён на `alex.ocr.ai.llm@gmail.com`, чтобы письма об истечении шли на живой адрес;
  - заложен каркас story для метрик/мониторинга CI/CD и TLS‑alerts.

## Что ещё осталось / куда двигаться дальше

- Дожать до конца авторизацию порталов по доменам:
  - дочистить Playwright `public-auth.spec.ts` (селекторы, логин issuer/investor/backoffice);
  - собрать скриншоты успешного логина с разных IP и закрыть Runtime DoD в `OPS-001-003` и `OPS-001-005`.
- Настроить мониторинг:
  - выбрать стек (Signoz/OTEL vs Prometheus+Grafana);
  - завести базовые дашборды по CI и cfa2, плюс alerts (в т.ч. в Telegram).

## Самооценка по дню

- Фактически день ушёл на: выравнивание CI/dev‑infra по dev-cfa2, доведение Cloudflare/Keycloak до рабочей схемы и приведение всей этой истории в читаемую документацию и промпты для следующих агентов.


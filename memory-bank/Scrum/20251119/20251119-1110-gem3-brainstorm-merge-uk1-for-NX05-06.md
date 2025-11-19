# Prompt
изучи все файлы, сессию которую сделал

 You are an Expert .NET 9 + Next.js + Kubernetes/Infra architect and AI pair-programmer.

  You are helping to continue a real production-grade project with strict spec-first rules and existing context.
  DO NOT invent new architecture or contracts from scratch.
  Always align with the attached files and explicitly mark any SPEC DIFF (difference between code and OpenAPI/AsyncAPI).

Смотри я сейчас тебе кормлю всю сессию (0.5мб) [eywa1-p-cfa-w10.p1-20251119-1035.session.txt] и сессию агента(1.3мб) [memory-bank/Scrum/20251111-1518-cfa1-deploy/eywa1-p-cfa-w6.p1-20251118-1503-co-3dd7.session.md] и весь контекст, но весь исходный

  Хочу чтобы  ты учел что сделано и что агентом co-3dd7 до мельчайших деталей, учтет текущую сессию дать ему нужно весь дальше контекст и попросить скорректироват ькак дальше делать задачи на NX-5,6 хосте `uk1` где успешно, или `cfa1` (на полпути) там эксперименты
  а то если работает не трогать - заодно доточить заново мои runbook сделанные успешно на uk1 что воспроизводятся на новом, у меня есть еще сервера us1, vps1, germ1 если что
  Ну вот такие цели поможешь?



p.s.
=====================
  PROJECT & CONTEXT
  =====================

  We are working on the "ois-cfa" backend app (submodule in a larger monorepo) and its documentation repo "docs-cfa-rwa".

  Tech stack:
  - Backend: .NET 9, ASP.NET Core, EF Core, Kafka (MassTransit), Prometheus/OpenTelemetry, Keycloak, API Gateway.
  - Frontend: Next.js portals (Issuer/Investor/Backoffice) using TS SDKs generated from OpenAPI.
  - Approach: spec-first (OpenAPI + AsyncAPI + JSON Schemas), with tasks NX-* driving refactors.

  Git / branches:
  - Active backend branch: `tasks/NX-01-spec-validate-and-matrix` in repo `ois-cfa`.
  - Target branch for MR: `infra.defis.deploy` (temporary pre-develop).
  - Important: this branch currently contains work for NX-01, NX-02, NX-03, NX-04 (not just NX-01) — this is a conscious deviation from strict gitflow.

  Environments:
  - `uk1` — currently working environment; rule: "if it works, don't break it".
  - `cfa1` — experimental / partially configured environment; objective: align it with uk1 using reproducible runbooks.
  - Future hosts: `us1`, `vps1`, `germ1` — should be able to reuse the same runbook with minimal changes.

  User preferences for your output:
  - Language: Russian with B2-level English terms/slang preserved.
  - Structure: Why → What → How → Result.
  - Formatting:
    - Start with TL;DR (3–7 bullets).
    - Then numbered Steps.
    - Then a compact table (≤6 rows per table) where it helps.
    - End with clear "Next actions" for a human engineer.
  - No marketing fluff, no overengineering, no hallucinations. Be brutally honest about unknowns and risks.

  =====================
  WHAT HAS BEEN DONE (NX‑01..NX‑04)
  =====================

  IMPORTANT: Treat NX‑01..NX‑04 as already implemented on branch `tasks/NX-01-spec-validate-and-matrix`, based on the attached files:

  - Daily report:
    - `repositories/customer-gitlab/docs-cfa-rwa/reports/20251118-1800-Alex-A.daily.report.md`
      - This is the main status report describing what was actually done for NX‑01..NX‑04, including commands, test status, and artifacts.

  - Context docs:
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROJECT-CONTEXT.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/FRONTEND-CONTEXT.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/RULES-SUMMARY.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/WBS-OIS.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROMPTS-MAP.md`

  - NX artifacts and reports:
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/spec-lint-openapi.txt`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/spec-validate-asyncapi.txt`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/spec-validate-jsonschema.txt`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-endpoints-coverage-report.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-test-report.txt`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/gateway-routing-report.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/registry-flow-report.md`

  - Structure and map:
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/project-C4.diagram.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/ois-cfa.reposcan.json`

  - Task specs:
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-01-spec-validate-and-matrix.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-02-gateway-routing-and-health.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-03-issuance-endpoints-coverage.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-04-registry-orders-flow.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-05-issuer-dashboard-and-reports.md`
    - `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-06-issuer-payout-schedule-spec-and-ui.md`

  Interpretation (high-level, you should double-check from files):
  - NX‑01: spec validation across OpenAPI/AsyncAPI/JSON Schemas, API/Event matrix and Gap List (including events like `ois.payout.scheduled`, `ois.transfer.completed`).
  - NX‑02: gateway routing alignment, health/metrics endpoints, and `gateway-routing-report.md` with verification commands (`make check-health`, etc.).
  - NX‑03: issuance endpoints/tests wired to .NET 9, with one known test issue (404 vs 500) documented in `issuance-test-report.txt` and coverage report.
  - NX‑04: registry order flow implemented (create → reserve → paid) with outbox events (`ois.order.created`, `ois.order.placed`, `ois.order.paid`, `ois.order.confirmed`, `ois.registry.transferred`), tests passing, and `registry-flow-report.md`
  documenting REST↔️code↔️events.

  Do NOT re-invent or re-do NX‑01..NX‑04 unless explicitly needed for NX‑05/NX‑06.
  Assume that branch `tasks/NX-01-spec-validate-and-matrix` is the current truth for backend behavior, plus the documented known gaps.

  =====================
  SESSIONS / INFRA CONTEXT
  =====================

  Additionally, you have attached:
  - My current session log on eywa1 (approx. 0.5MB): recent work on NX tasks and infra.
  - Previous agent session:
    - `memory-bank/Scrum/20251111-1518-cfa1-deploy/eywa1-p-cfa-w6.p1-20251118-1503-co-3dd7.session.md`
      - Detailed attempts to deploy on host `cfa1`, including experiments, partial successes, and problems.
  Потом ТЫ (gemini3) будешь моим учителем, наставником, коучем, архитектором аналитиком и сделаешь для   новой сессии Cli-agent дать вводный промпт чтобы доделать Nx5,6 и дальше но с учетом что я устноавил на сервере

=====================
  YOUR MISSION
  =====================

  Your main job now is NOT to change code directly, but to act as a high-signal consultant and planner for the next tasks and infra rollout.

  Focus on three directions:

  1) NX‑05 — Issuer Dashboard & Reports (frontend + backend integration)
  ---------------------------------------------------------------------

  Goal:
  - Use the current spec-first contracts and already implemented backend (NX‑01..NX‑04) to design a realistic, incremental plan for NX‑05:
    - Issuer dashboard (metrics, statuses, aggregates).
    - Reports (issuances, orders, payouts where applicable).

  Using:
  - `FRONTEND-CONTEXT.md`
  - `PROJECT-CONTEXT.md`
  - `NX-05-issuer-dashboard-and-reports.md`
  - OpenAPI/AsyncAPI contracts from the repo (as referenced in artifacts and the contracts code2prompt snapshot).

  Deliverables for NX‑05:
  - A clear Why → What → How → Result breakdown:
    - Why: what business holes NX‑05 should close, based on context.
    - What: which endpoints, entities, and events should be used/extended (with explicit references to OpenAPI paths and AsyncAPI topics).
    - How:
      - Backend: which services/controllers/handlers to touch (namespaces, projects, likely files).
      - Frontend: which Next.js app(s)/routes/components, how to structure API clients (e.g., `apps/portal-issuer/...`).
      - Tests: unit, integration, and at least one e2e smoke flow (issuer login → dashboard → reports).
    - Result: what “Done” looks like in terms of working flows and updated artifacts.

  - Output format:
    - TL;DR bullets.
    - Detailed numbered steps that a senior engineer can follow on uk1/cfa1.
    - A compact table (≤6 rows) mapping “Feature block” → “Endpoints” → “Service” → “Frontend route” → “Tests”.

  Constraints:
  - DO NOT break existing working flows on uk1.
  - Prefer reusing existing endpoints/events rather than inventing new ones.
  - If contracts are insufficient, propose SPEC DIFFs explicitly and tie them back to NX‑tasks/docs.

  2) NX‑06 — Issuer Payout Schedule Spec and UI
  ---------------------------------------------

  Goal:
  - Design how payouts scheduling and tracking should work for the issuer, spec-first and UI-wise.

  Using:
  - `PROJECT-CONTEXT.md`
  - `FRONTEND-CONTEXT.md`
  - `NX-06-issuer-payout-schedule-spec-and-ui.md`
  - Contracts snapshots (code2prompt contracts + AsyncAPI/OpenAPI).
  - Current artifacts from NX‑01..NX‑04 (especially gaps in payouts/transfer events).

  Deliverables for NX‑06:
  - List current relevant endpoints and events (if any) for payouts.
  - Identify what is missing in:
    - OpenAPI (REST endpoints for scheduling, listing, cancelling payouts).
    - AsyncAPI (events for payout scheduled/processed/failed).
  - Propose minimal SPEC DIFFs:
    - New/updated paths and schemas in OpenAPI.
    - New/updated topics and payloads in AsyncAPI.
  - UI flow design for portal-issuer:
    - Pages/routes and main components for viewing and scheduling payouts.
    - How to show state transitions and errors.

  - Output format:
    - TL;DR.
    - Detailed plan (backend + frontend + tests).
    - Small table mapping “User action” → “REST endpoint” → “AsyncAPI event(s)” → “State change”.

  Constraints:
  - Stay consistent with existing domains (issuance/registry/settlement).
  - Call out clearly any cross-service interactions (e.g., Registry ↔️ Settlement).
  - Do NOT specify crazy overcomplicated flows; keep it pragmatic and implementable in the current codebase.

  3) Infra Runbooks — uk1 vs cfa1 (and future hosts)
  ---------------------------------------------------

  Goal:
  - Extract from sessions and artifacts:
    - A canonical deployment runbook for uk1 (which already works).
    - A portable, clean runbook that can be applied to cfa1/us1/vps1/germ1 without breaking uk1.

  Using:
  - The attached session logs (especially co‑3dd7 on cfa1) and aggregated infra snapshots.
  - Makefile targets, docker-compose/k8s descriptions, any infra notes referenced in PROJECT-CONTEXT and artifacts.

  Deliverables:
  - High-level architecture of deployment:
    - Components (API gateway, services, Kafka, Keycloak, DB, Prometheus, SMTP, etc.).
    - How they are wired on uk1 (entrypoints, DNS/Cloudflare, ports).
  - Two runbooks:
    - “uk1 — current & safe”:
      - Only minimal maintenance/refactor steps.
      - Emphasis on health checks, smoke tests (e.g., playwright or simple curl).
      - Clear warnings on what NOT to touch without full plan.
    - “new host (cfa1/us1/vps1/germ1) — reproducible setup”:
      - Step-by-step from clean VM to working stack:
        - System packages.
        - Docker/docker-compose or k8s setup.
        - Configuration of Keycloak URLs/clients.
        - Environment variables and secrets placeholders (without real secrets).
        - Commands to start services and verify `/health`, metrics, and key user flows.
      - Mark risky steps explicitly (e.g., DB migrations, certs).

  - Output format:
    - For each runbook: numbered steps and a small checklist table (Step → Command/Tool → Expected result/health check).

  Constraints:
  - Do NOT propose invasive changes on uk1.
  - Prefer idempotent scripts/composes that can be rerun.
  - Respect that some experiments on cfa1 are half-done; indicate clearly what should be reset/cleaned vs reused.

  4) Open Issues and Risk Register (for NX‑05/NX‑06 and infra)
  ------------------------------------------------------------

  Based on all attached context:
  - List remaining gaps and risks that may affect NX‑05/NX‑06 and deployments, for example:
    - Issuance test `Publish_NonExistent_Should_Return_404` currently failing (404 vs 500).
    - AsyncAPI events that still have no producers.
    - Health/metrics endpoints not fully wired for some services.
  - For each gap:
    - Why it matters.
    - What minimal change is needed.
    - Where it should be implemented (service/project/file level).
    - Whether it must be fixed before/with NX‑05/06 or can be postponed.

  =====================
  OUTPUT FORMAT (VERY IMPORTANT)
  =====================

  Please respond in Russian, but keep technical terms, file paths, endpoints, and code-level identifiers in English.

  Structure your answer like this:

  1) TL;DR
     - 3–7 bullets summarizing the main decisions and plans.

  2) Steps
     - Numbered sections:
       - 2.1 NX‑05 plan
       - 2.2 NX‑06 plan
       - 2.3 Infra runbooks (uk1/cfa1)
       - 2.4 Risk register / open issues

  3) Table(s)
     - Up to 2–3 compact tables (≤6 rows each) to map:
       - Key features ↔️ endpoints ↔️ services ↔️ frontend routes.
       - Runbook steps ↔️ commands ↔️ expected checks.

  4) Next actions
     - Short checklist of concrete tasks that a senior engineer should do next on uk1/cfa1 (with explicit commands where appropriate).

  If something is unclear or the attached files contradict each other, DO NOT guess.
  Instead, state assumptions explicitly and mark them as “ASSUMPTION”.



Вот детальный план и архитектурный анализ для продолжения работы, основанный на изучении сессий (твоей и агента `co-3dd7`), а также текущего состояния репозитория.

### TL;DR

*   **Status Quo:** Ветка `tasks/NX-01-spec-validate-and-matrix` (влитая в `infra.defis.deploy`) содержит выполненные NX-01, NX-02, NX-04 и почти выполненный NX-03 (один тест падает).
*   **Infra:** Сервер `uk1` — эталон (Hybrid deployment: Backend в Docker, Frontend в PM2, Nginx на хосте, Postfix локально). Сервер `cfa1` требует выравнивания конфигурации по образу `uk1`.
*   **NX-05 (Dashboard):** Требует реализации агрегации данных. В текущем OpenAPI нет эндпоинтов для агрегатов (`/summary`), поэтому фронтенд сейчас считает это "на лету", что плохо для продакшена. Нужен SPEC DIFF.
*   **NX-06 (Payouts):** Самая сложная часть. В `issuance` сервисе нет логики расписания выплат, только поле `scheduleJson`. Требуется проектирование контракта.
*   **Next Step:** Я подготовил промпт для следующего агента, чтобы он закрыл долг по NX-03, реализовал NX-05/06 и синхронизировал `cfa1`.

---

### 2. Detailed Steps & Plan

#### 2.1. NX-05 Plan: Issuer Dashboard & Reports
*   **Why:** Эмитенту нужно видеть сводку (сколько денег собрано) и выгружать реестр инвесторов/выплат.
*   **What (Gaps):**
    *   В `openapi-gateway.yaml` нет эндпоинтов для аналитики (KPIs).
    *   В `apps/portal-issuer` страницы `/dashboard` и `/reports` на моках или неэффективных запросах.
*   **How:**
    1.  **Backend:**
        *   Создать SPEC DIFF: добавить `GET /v1/issuances/summary` (возвращает `totalVolume`, `activeCount`, `closedCount`).
        *   Реализовать в `IssuanceService.cs` метод `GetSummaryAsync` (EF Core `GroupBy` / `Sum`).
        *   Добавить `GET /v1/reports/issuances` с поддержкой фильтрации и пагинации (или CSV стриминг).
    2.  **Frontend:**
        *   В `apps/portal-issuer/lib/api` добавить методы вызова новых эндпоинтов.
        *   Подключить реальные данные в компоненты Dashboard.
    3.  **Tests:**
        *   Интеграционный тест: создать 3 выпуска, дернуть `/summary`, проверить цифры.

#### 2.2. NX-06 Plan: Issuer Payout Schedule
*   **Why:** Эмитент должен знать, когда и сколько платить инвесторам.
*   **What (Gaps):**
    *   Сейчас `scheduleJson` — это просто blob. Нет валидации и управления.
*   **How:**
    1.  **Spec:**
        *   SPEC DIFF: Определить схему `PayoutScheduleItem` (date, amount, currency, status).
        *   Добавить эндпоинты `GET/PUT /v1/issuances/{id}/schedule`.
    2.  **Backend (`services/issuance`):**
        *   Добавить Value Object `PayoutSchedule` в Domain.
        *   Реализовать валидацию: сумма выплат не должна превышать объем выпуска (или % ставки).
    3.  **Frontend:**
        *   Страница `/issuances/[id]/schedule`. Таблица с датами.
        *   Статусы: `Scheduled` -> `Processing` -> `Paid` (интеграция с Settlement в будущем).

#### 2.3. Infra Runbooks (UK1 vs New Hosts)

**Архитектура деплоя (Hybrid):**
*   **Core:** Docker Compose (`postgres`, `kafka`, `keycloak`, `minio`, .NET services).
*   **Edge:** Nginx (Host-level) -> proxy_pass на порты контейнеров/PM2.
*   **Front:** Node.js (PM2) -> `localhost:300x`.
*   **Mail:** Postfix (Host-level) -> relay.

**Runbook: UK1 (Current & Safe)**
*   *Maintenance:* Только `git pull`, `docker compose up -d --build <service>`, `pm2 restart <app>`.
*   *Monitoring:* `make check-health` (проверяет `:5000/health` и остальные).
*   *Warning:* Не трогать `nginx.conf` и `postfix` без бэкапа. Сертификаты Let's Encrypt обновляются через certbot timer.

**Runbook: New Host (CFA1/US1/etc.) — Reproducible Setup**
1.  **OS Prep:** `apt install docker.io docker-compose-v2 nginx postfix opendkim git nodejs npm`. Установить NVM + Node 20.
2.  **Repo:** `git clone ...`, `git submodule update --init`.
3.  **Env:** Скопировать `.env.example` -> `.env`. Заполнить `CLOUDFLARE_API_TOKEN` (если нужен DNS) и секреты Keycloak.
4.  **Backend:**
    *   `docker compose up -d postgres kafka zookeeper keycloak`.
    *   `docker exec ... kcadm.sh` (импорт реалма `ois-dev` или настройка руками по `KEYCLOAK-SETUP.md`).
    *   `docker compose up -d` (остальные сервисы).
5.  **Frontend:**
    *   `cd apps/portal-* && npm ci`.
    *   Настройка `.env.local` (указать IP/домен нового хоста).
    *   `pm2 start ...` (использовать скрипты из `ops/scripts/pm2/` или создать их).
6.  **Ingress:**
    *   Настроить Nginx (копия конфига из `ops/infra/uk1/nginx-cfa-portals.conf` с заменой доменов).
    *   Certbot для SSL.

#### 2.4. Risk Register / Open Issues
1.  **NX-03 Test Failure:** `Publish_NonExistent_Should_Return_404` падает с 500.
    *   *Impact:* Грязные логи, некорректная обработка ошибок клиентом.
    *   *Fix:* В `IssuanceService.cs` обернуть поиск в `try-catch` или проверить `null` до обращения к свойствам, убедиться что Global Exception Handler не перехватывает 404 как 500.
2.  **AsyncAPI Gaps:** `ois.payout.scheduled` не имеет продюсера.
    *   *Impact:* Settlement сервис не узнает, когда платить.
    *   *Fix:* Реализовать в NX-06.
3.  **Hardcoded Secrets in PM2:** В сессии `co-3dd7` секреты прописывались в команды запуска PM2.
    *   *Fix:* Использовать `ecosystem.config.js` и `.env` файлы, не передавать секреты в аргументах CLI.

---

### 3. Tables

#### Feature Mapping (NX-05/06)

| Feature | Endpoint (OpenAPI) | Service | Frontend Route | Tests Needed |
| :--- | :--- | :--- | :--- | :--- |
| **Dashboard Stats** | `GET /v1/issuances/summary` (New) | Issuance | `/dashboard` | Unit + Integration |
| **Issuance Report** | `GET /v1/reports/issuances` (New) | Issuance | `/reports` | Integration |
| **Payout Schedule** | `GET/PUT /v1/issuances/{id}/schedule` | Issuance | `/issuances/[id]/schedule` | Unit (Domain logic) |
| **Payout Events** | `ois.payout.scheduled` (AsyncAPI) | Issuance -> Settlement | N/A (Background) | Integration (Outbox) |

#### Deployment Checklist (New Host)

| Step | Command | Expected Check |
| :--- | :--- | :--- |
| 1. Infra | `docker compose ps` | All containers `Up (healthy)` |
| 2. Database | `docker exec ois-postgres ...` | DB `keycloak` & `ois` exist |
| 3. Auth | `curl localhost:8080/health/ready` | `200 OK` |
| 4. Backend | `make check-health` | All services `OK` |
| 5. Frontend | `pm2 list` | 3 apps `online` |
| 6. Ingress | `curl https://<domain>/admin` | `302` (Redirect to Keycloak) |

---

### 4. Next Actions (Prompt for the next agent)

Скопируй блок ниже и отдай следующему агенту. Это полный контекст и задание.

***

**ROLE:** Senior .NET/Next.js DevOps Engineer.
**CONTEXT:**
We are finalizing the MVP for OIS-CFA.
- **Repo:** `ois-cfa` (submodule). Branch: `tasks/NX-01-spec-validate-and-matrix` (contains NX-01..04).
- **Live Env:** `uk1` (185.168.192.214). Fully functional (HTTPS, Keycloak, Postfix).
- **Target:** Finish NX-05, NX-06 and fix NX-03 technical debt. Then align `cfa1` host.

**INPUT FILES:**
- `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROJECT-CONTEXT.md` (Architecture & Status)
- `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-test-report.txt` (NX-03 bug details)
- `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-05-issuer-dashboard-and-reports.md`
- `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-06-issuer-payout-schedule-spec-and-ui.md`

**YOUR MISSION:**

1.  **Fix NX-03 Technical Debt:**
    *   Analyze `services/issuance/Services/IssuanceService.cs` and `Program.cs`.
    *   Fix `Publish_NonExistent_Should_Return_404` test (currently 500). Ensure it returns 404 cleanly.
    *   Run `dotnet test tests/issuance.Tests/issuance.Tests.csproj` to verify.

2.  **Implement NX-05 (Dashboard & Reports):**
    *   **Spec:** Create `tasks/NX-05-SPEC-DIFF.md`. Define `GET /v1/issuances/summary` and `GET /v1/reports/issuances`.
    *   **Backend:** Implement endpoints in `IssuanceService`. Use EF Core projections for performance.
    *   **Frontend:** Update `apps/portal-issuer/app/dashboard/page.tsx` to use real API.

3.  **Implement NX-06 (Payout Schedule):**
    *   **Spec:** Create `tasks/NX-06-SPEC-DIFF.md`. Define CRUD for `/v1/issuances/{id}/schedule`.
    *   **Backend:** Add `PayoutSchedule` VO to `Issuance` aggregate. Implement persistence.
    *   **Frontend:** Add Schedule tab to Issuance Details page.

4.  **Refine Runbooks:**
    *   Create `ops/runbooks/setup-new-host.md` based on the `uk1` experience (Docker + PM2 + Nginx).
    *   Ensure `cfa1` can be provisioned using this runbook.

**EXECUTION RULES:**
*   **Spec-First:** Always write/update OpenAPI YAML before C# code.
*   **Test-First:** Write a failing test for the new endpoints before implementing.
*   **Commit Strategy:** Commit incrementally (`fix(nx-03): ...`, `feat(nx-05): ...`).
*   **Verification:** Use `curl` and `dotnet test` to prove your work.

**GO!** Start by fixing the NX-03 test failure.
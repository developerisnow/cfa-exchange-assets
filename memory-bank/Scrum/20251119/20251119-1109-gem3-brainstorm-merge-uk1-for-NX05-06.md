# Prompt
You are an Expert .NET 9 + Next.js + Kubernetes/Infra architect and AI pair-programmer.

  You are helping to continue a real production-grade project with strict spec-first rules and existing context.
  DO NOT invent new architecture or contracts from scratch.
  Always align with the attached files and explicitly mark any SPEC DIFF (difference between code and OpenAPI/AsyncAPI).

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
  documenting REST↔code↔events.

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

  You may also see aggregated context snapshots like:
  - `memory-bank/snapshots-aggregated-context-duplicates/20251118-c2p_20251118-0905-context-reposcan-agents-structure-and-codemachine.txt`
  - `memory-bank/snapshots-aggregated-context-duplicates/20251117-c2p_reposcan.txt`
  - `memory-bank/snapshots-aggregated-context-duplicates/20251117-c2p_agents-structures.txt`
  - `memory-bank/snapshots-aggregated-context-duplicates/20251117-c2p_codemachine.txt`
  - `memory-bank/snapshots-aggregated-context-duplicates/20251118-1950-code2prompt-ois-cfa-contracts.txt`
  - `memory-bank/snapshots-aggregated-context-duplicates/20251118-1950-code2prompt-ois-cfa-services-core.txt`

  Treat these as secondary helpers: only use them to clarify structure and infra behavior if needed.
  Primary truth is: PROJECT/FRONTEND/RULES/WBS, NX task files, artifacts, and the daily report.

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
  - Call out clearly any cross-service interactions (e.g., Registry ↔ Settlement).
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
       - Key features ↔ endpoints ↔ services ↔ frontend routes.
       - Runbook steps ↔ commands ↔ expected checks.

  4) Next actions
     - Short checklist of concrete tasks that a senior engineer should do next on uk1/cfa1 (with explicit commands where appropriate).

  If something is unclear or the attached files contradict each other, DO NOT guess.
  Instead, state assumptions explicitly and mark them as “ASSUMPTION”.

  ———

  ### 2. Что приложить к files (шпаргалка)

  Когда будешь вызывать oracle_gpt5.oracle_query / Gemini, в files положи минимум:

  - repositories/customer-gitlab/docs-cfa-rwa/reports/20251118-1800-Alex-A.daily.report.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROJECT-CONTEXT.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/FRONTEND-CONTEXT.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/RULES-SUMMARY.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/WBS-OIS.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROMPTS-MAP.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/spec-lint-openapi.txt
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/spec-validate-asyncapi.txt
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/spec-validate-jsonschema.txt
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-endpoints-coverage-report.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-test-report.txt
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/gateway-routing-report.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/registry-flow-report.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/project-C4.diagram.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/ois-cfa.reposcan.json
  - repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-01-spec-validate-and-matrix.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-02-gateway-routing-and-health.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-03-issuance-endpoints-coverage.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-04-registry-orders-flow.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-05-issuer-dashboard-and-reports.md
  - repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-06-issuer-payout-schedule-spec-and-ui.md
  - плюс выбранные агрегаты / сессии (по бюджету): хотя бы твой свежий лог и eywa1-p-cfa-w6.p1-20251118-1503-co-3dd7.session.md.

# Output
Вот подготовленный пакет для делегирования задачи GPT-5 Pro (Oracle).

Я отобрал файлы так, чтобы они покрывали **контекст (Trunk)**, **текущее состояние кода (Branch)** и **историю действий (Session logs)**, укладываясь в лимиты контекста.

### 1. Список файлов для прикрепления (Files to attach)

При вызове `oracle_query` передай этот список. Это "золотой набор", описывающий состояние "как есть" после выполнения NX-01..NX-04.

**Core Context & Rules:**
1. `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROJECT-CONTEXT.md` (SSOT состояния)
2. `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/FRONTEND-CONTEXT.md` (Для NX-05/06)
3. `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/WBS-OIS.md` (План)
4. `repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/RULES-SUMMARY.md` (Правила)

**Status & Execution Logs (Critical):**
5. `repositories/customer-gitlab/docs-cfa-rwa/reports/20251118-1800-Alex-A.daily.report.md` (Самый важный файл: что реально сделано и работает)
6. `memory-bank/Scrum/20251111-1518-cfa1-deploy/eywa1-p-cfa-w6.p1-20251118-1503-co-3dd7.session.md` (История настройки cfa1/uk1, Postfix, DNS)

**Task Definitions:**
7. `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-05-issuer-dashboard-and-reports.md`
8. `repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-06-issuer-payout-schedule-spec-and-ui.md`

**Artifacts (Evidence of work):**
9. `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/registry-flow-report.md` (NX-04 result)
10. `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-test-report.txt` (NX-03 result & bugs)
11. `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/gateway-routing-report.md` (NX-02 result)
12. `repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/project-C4.diagram.md` (Архитектура)

**Contracts (Reference):**
13. `repositories/customer-gitlab/wt__ois-cfa__NX01/packages/contracts/openapi-gateway.yaml`
14. `repositories/customer-gitlab/wt__ois-cfa__NX01/packages/contracts/asyncapi.yaml`

---

### 2. Промпт для GPT-5 Pro

Скопируй этот текст в поле `prompt`.

```text
You are an Expert .NET 9 + Next.js + Kubernetes/Infra architect and AI pair-programmer.

You are helping to continue a real production-grade project with strict spec-first rules and existing context.
DO NOT invent new architecture or contracts from scratch.
Always align with the attached files and explicitly mark any SPEC DIFF (difference between code and OpenAPI/AsyncAPI).

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
- NX‑04: registry order flow implemented (create → reserve → paid) with outbox events (`ois.order.created`, `ois.order.placed`, `ois.order.paid`, `ois.order.confirmed`, `ois.registry.transferred`), tests passing, and `registry-flow-report.md` documenting REST↔code↔events.

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

You may also see aggregated context snapshots like:
- `memory-bank/snapshots-aggregated-context-duplicates/20251118-c2p_20251118-0905-context-reposcan-agents-structure-and-codemachine.txt`
- `memory-bank/snapshots-aggregated-context-duplicates/20251117-c2p_reposcan.txt`
- `memory-bank/snapshots-aggregated-context-duplicates/20251117-c2p_agents-structures.txt`
- `memory-bank/snapshots-aggregated-context-duplicates/20251117-c2p_codemachine.txt`
- `memory-bank/snapshots-aggregated-context-duplicates/20251118-1950-code2prompt-ois-cfa-contracts.txt`
- `memory-bank/snapshots-aggregated-context-duplicates/20251118-1950-code2prompt-ois-cfa-services-core.txt`

Treat these as secondary helpers: only use them to clarify structure and infra behavior if needed.
Primary truth is: PROJECT/FRONTEND/RULES/WBS, NX task files, artifacts, and the daily report.

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
  - Call out clearly any cross-service interactions (e.g., Registry ↔ Settlement).
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
     - Key features ↔ endpoints ↔ services ↔ frontend routes.
     - Runbook steps ↔ commands ↔ expected checks.

4) Next actions
   - Short checklist of concrete tasks that a senior engineer should do next on uk1/cfa1 (with explicit commands where appropriate).

If something is unclear or the attached files contradict each other, DO NOT guess.
Instead, state assumptions explicitly and mark them as “ASSUMPTION”.
```
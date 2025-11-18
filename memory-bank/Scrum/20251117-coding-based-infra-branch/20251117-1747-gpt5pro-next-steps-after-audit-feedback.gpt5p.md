# Prompt 1
You are Oracle, a focused one-shot problem solver. Emphasize direct answers, cite any files referenced, and clearly note when the search tool was used.  You are GPT‑5 Pro acting as a senior system/solution architect and codebase reviewer.  I have attached: - `c2p_ois-cfa.txt`: a ~4MB code2prompt snapshot of the `ois-cfa` repository (branch `infra.defis.deploy`), including structure and key files; - `20251116-1603-gpt5pro-audit-feedback-review.gpt5p.md`: your previous long-form audit & recommendations for this repo (call it V1‑audit); - `20251117-1537-eywa1-co-3dd7.session.md`: my detailed infra/devops session log from AVA1/eywa1 describing what I actually did with CFA1/UK1, Cloudflare, Postfix, Playwright, etc.; - `20251117-1713-feedback-to-co-3c63-from-eywa1-co-3dd7.md`: a short summary of what you (V1‑audit) did NOT know and what must be added as context;  - two architecture context files about Trees/Leaves/Agents (my target way of working through AI agents on top of this codebase).  High-level reality check (NEW facts you must incorporate): - Historically, the first demo environment was on **CFA1/AVA1**: docker-compose stack, Keycloak, portals, Postgres/Kafka/MinIO. This is documented in older runbooks/logs (not attached here, but referenced in the eywa1 session). - Because of access/infra issues, we moved the working demo to **UK1** (public host). There we:   - configured Cloudflare + DNS for `*.cfa.llmneighbors.com` and proper TLS (certbot + DNS challenge);   - set up Nginx reverse proxies for all portals + API gateway;   - configured **Postfix + OpenDKIM** so that Keycloak can send emails for `verifyEmail` and `forgot password` flows;   - ran **Playwright** E2E smoke tests (issuer/investor/backoffice) against this UK1 environment and fixed issues until flows passed. - The branch `infra.defis.deploy` now represents:   - Aleksandr’s infra/observability/audit work (`infra` branch: GitOps, Terraform, OTEL, audit/* etc.);   - plus my deploy/UK1‑oriented tweaks (docker-compose, gateway, portals, Keycloak/SMTP, test configs). - In other words: your V1‑audit was structurally good, but it assumed a “theoretical infra” and did NOT know that a real, working UK1 demo exists with DNS/SSL/SMTP/E2E already wired.  Your job now is to produce a **V2‑audit & plan**, building on V1 but corrected and updated with this real-world context.  What I need from you (V2‑audit):  1) **Delta vs V1‑audit (short, but precise)**    - Carefully read your own V1‑audit (`20251116-1603-gpt5pro-audit-feedback-review.gpt5p.md`) and my eywa1 session + 1713‑feedback.    - In Russian (with B2‑English terms), list the **top 5–10 places where your V1‑audit is now incomplete, misleading or needs refinement** because of the CFA1→UK1 story and real infra work (Cloudflare, Nginx, Postfix, Playwright, infra.defis.deploy).    - For each such point, write:      - `What V1 said`      - `New reality`      - `Corrected conclusion / recommendation`  2) **Updated repository/infra architecture picture (macro)**    - Using `c2p_ois-cfa.txt` PLUS the new context, restate **how you now see the architecture** of `ois-cfa` on `infra.defis.deploy`:      - core domains/services (identity/issuance/registry/settlement/compliance);      - frontends (apps/*), gateway, chaincode, packages/*, tests;      - ops/infrastructure (ops/, audit/, docker-compose, GitOps, observability);      - how UK1 environment and its runbooks logically map onto this repo.    - Keep this section **short, but accurate**: 5–8 bullets that I can re-use in docs as “Current Architecture Snapshot (infra.defis.deploy + UK1)”.  3) **Refined 2–3 week plan based on `tasks/NX-*` and docs/context**    - In V1‑audit you already touched on tasks and docs, but now you know:      - a working UK1 demo exists;      - tasks `NX-01..NX-08` already describe slices (gateway routing, issuance coverage, KYC/backoffice, dashboards, etc.);      - docs/context/* (FRONTEND-CONTEXT, PROJECT-CONTEXT, PROMPTS-MAP, RULES-SUMMARY, WBS-OIS) exist to guide work.    - Please propose a **concrete 2–3 week roadmap** (assume ~40–60h of my time + limited help from an AI agent) that:      - Orders the `NX-*` tasks (which first/second/third, what can be parallelised, what depends on what);      - For each `NX-*` task, gives:        - `Goal` (1–2 lines),        - `Prereqs` (docs/specs/tests that must be read or updated first),        - `Done-when` DoD (checklist, not more than 4–6 points),        - `Agent-friendly?` (yes/no/partial with 1 line why).    - Output this as a neat table so I can almost paste it into a planning doc.  4) **Repo hygiene & structural refactors (1–2 day budget)**    - Revisit your comments on ARCHIVE vs audit vs docs vs memory-bank vs chaincode vs apps.    - With the NEW context (UK1 is real, infra.defis.deploy is the main branch), propose **a minimal set of structural refactors** that I can realistically do in 1–2 days to improve:      - onboarding of a new dev;      - future AI‑agent work (less noise, clearer contract/impl split);      - separation between “live” infra and historical artefacts.    - Be concrete: 5–10 bullets of the form “Move X to Y”, “Rename folder Z”, “Add README here with these headings”, “Symlink or index these docs in one place”. No bikeshedding.  5) **Agentification V2 (with Trees/Leaves mindset)**    - You saw the Trees/Leaves/Agents docs. Assume the following guiding principle:      - Trunk/Tree = stable architecture, contracts, critical infra runbooks;      - Leaves = repeatable, low‑risk changes on top (new endpoints, small UI slices, generated clients, tests, simple configs).    - Based on `c2p_ois-cfa.txt` and your V1+V2 understanding, list:      - **5–10 “leaf” task patterns** in this repo that are good candidates for AI agents (with constraints) — e.g. “add missing Playwright spec for existing flow”, “wire up new endpoint given OpenAPI/AsyncAPI contract”, etc.;      - **3–5 “trunk/tree” task patterns** that I should keep under manual control (or only use AI as advisor), e.g. deep refactors across services, critical auth flows, infra topology changes.    - For each pattern, give 1–2 sentences why.  Constraints & style: - Answer in Russian, using senior-engineer language; English technical terms/slang OK where they help. - Structure your answer as:   - TL;DR (3–5 bullets);   - Sections 1–5 as above, with clear headers and bullets/tables where requested;   - Concluding compact table: `Area` / `Issue or Question` / `V2 recommendation`. - Do NOT restate contents of attached files; focus on **deltas, decisions, and concrete next steps**.
# Output 1

* UK1 уже не «план», а рабочий demo: Cloudflare, TLS, nginx, Keycloak, Postfix/OpenDKIM и Playwright‑smoke (4 спека) — это база, а не wishlist.
* Ветка `infra.defis.deploy` уже собрана и запушена (deploy + infra + мои правки Program.cs/MIGRATE_ON_STARTUP/e2e), её нужно **стабилизировать и развивать**, а не заново проектировать merge‑стратегию.
* План на 2–3 недели: 1) добить NX‑01/02/03 как «спеки+gateway+issuance» с UK1 в роли эталона; 2) протащить NX‑04 (registry flow) с E2E; 3) сформализовать NX‑05/06 (identity + CI gates) и только потом вкладываться в backoffice NX‑07/08.
* Hygiene‑рефактор: не выносить `memory-bank`, а пометить его как knowledge‑storage; подчистить границы `docs/` vs `audit/` vs `ARCHIVE/`, выделить generated‑код и явно подсветить UK1‑runbooks.
* Agentification: листья — Playwright, TS/.NET клиенты, мелкий UI/ops; ствол — доменные контракты, DLT, Keycloak/идентика и topology K8s/GitOps.

> Я прогнал все указанные файлы через внутренний `file_search` (V1‑аудит, eywa1‑сессию, 1713‑feedback, `c2p_ois-cfa.txt`, WBS‑OIS и UK1‑runbook). Ниже — V2‑картина.

---

## 1) Delta vs V1‑audit (где V1 теперь устарел)

### 1. Статус окружений (CFA1 vs UK1)

* **What V1 said**
  Окружение надо «bootstrap’ить»: поднять docker‑compose на VPS/локали + базовый K8s/Timeweb, проверить Keycloak, gateway, health‑эндпоинты. 

* **New reality**
  UK1 уже развёрнут как публичный demo: Cloudflare DNS и TLS для `*.cfa.llmneighbors.com`, системный nginx как reverse proxy, docker‑compose стек (Keycloak + порталы + API gateway), плюс Postfix/OpenDKIM и рабочие email‑флоу.

* **Corrected conclusion / recommendation**
  UK1 — текущий «reference env». В ближайшие 2–3 недели фокус не на bring‑up, а на:

  * фиксации runbook’ов (UK1 как канон),
  * выравнивании кода/спеков/тестов под этот стенд,
  * аккуратном копировании паттернов (docker‑compose, nginx, SMTP) в dev.

---

### 2. Cloudflare / Ingress / TLS

* **What V1 said**
  Говорил про gateway/порталы, но не видел Cloudflare/ingress как уже решённый слой, рассматривал это скорее как будущую настройку.

* **New reality**
  Есть подробный runbook `docs/deploy/20251113-cloudflare-ingress.md` с чек‑листом: A‑записи для `auth|issuer|investor|backoffice|api`, SSL Mode=Full, wildcard LE‑сертификат, nginx‑vhost, привязка Keycloak клиентов. 

* **Corrected conclusion / recommendation**
  Edge‑слой сейчас: **Cloudflare → nginx (UK1) → api‑gateway/порталы**. Это часть продовой архитектуры demo, а не временный костыль. В V2‑доках нужно прямо рисовать это в C4/sequence и использовать как дефолтный ingress pattern.

---

### 3. SMTP / Keycloak email‑флоу

* **What V1 said**
  NX‑05 описан как «Identity/Keycloak baseline (planned)», без факта работающего SMTP/verifyEmail/forgot password. 

* **New reality**
  Postfix+OpenDKIM на UK1 настроены как локальный relay, порт 25 наружу закрыт, Keycloak шлёт verifyEmail/forgot через mail.tm; всё зафиксировано в memory‑логах и обновлённом runbook’е.

* **Corrected conclusion / recommendation**
  Identity‑baseline уже есть. NX‑05 в V2 — это:

  * формализовать identity‑контракты/flows в `packages/contracts`,
  * описать Keycloak realm/clients и SMTP в `docs/deploy`,
  * сделать их воспроизводимыми для dev/test (docker‑compose overrides), а не «с нуля настраивать почту».

---

### 4. Playwright / E2E покрытие

* **What V1 said**
  Фиксировал наличие Playwright‑journeys в целом, предлагал расширять их, но не знал про UK1‑ориентированные спеки и backoffice.

* **New reality**
  Сейчас есть 4 ключевых спека: issuer, investor, self‑registration и backoffice admin login, все проходят `npm test`; документация UK1‑runbook и memory‑лог подчёркивают, что это официальный smoke для стенда.

* **Corrected conclusion / recommendation**
  Playwright‑suite — не «nice‑to‑have», а **обязательный regression‑gate** для NX‑задач. Любой кусок работы по NX‑03/04/07/08 должен заканчиваться обновлением/расширением существующих spec’ов и прогоном по UK1.

---

### 5. Ветка `infra.defis.deploy` и merge‑стратегия

* **What V1 said**
  Рассматривал создание `infra.defis.deploy` как будущую операцию (от `infra` или от `deploy`), с bucket‑merge по services/packages/ops, плюс набор DoD для merge.

* **New reality**
  Эта стратегия уже реализована:

  * git cleanup на `deploy`,
  * `infra.defis.deploy` создана от `deploy`,
  * в неё смерджен `origin/infra`, разрешены конфликты в `.gitignore`, `apps/backoffice/package.json`, `services/*/*.csproj`, `Program.cs`,
  * дальше подтянут commit `9e866da5` с тестами/launchSettings, ветка запушена (`ed44ee6`, `a2db527`).

* **Corrected conclusion / recommendation**
  `infra.defis.deploy` = **основная рабочая ветка**. V2‑план — не про merge‑архитектуру, а про:

  * валидацию этой ветки тестами,
  * доведение её до состояния «из неё можно делать release branch»,
  * закрытие хвостов NX‑задач уже в её контексте.

---

### 6. Timeweb/K8s: приоритеты

* **What V1 said**
  Для 2–3 недель предлагал иметь и docker‑compose dev/prod, и базовый K8s/Timeweb контур для smoke‑тестов.

* **New reality**
  В infra‑ветке действительно есть Terraform/Timeweb и GitLab Agent GitOps, но реальная эксплуатация сейчас крутится вокруг одиночного UK1‑VPS с docker‑compose и nginx; никаких живых kube‑кластеров в логах нет.

* **Corrected conclusion / recommendation**
  В горизонте 2–3 недель — **не разворачиваем новый K8s**, максимум делаем `terraform validate`/`helm lint` и слегка шлифуем доки. Основная ценность сейчас: стабильный UK1‑demo + готовность infra для следующего этапа.

---

### 7. Статус NX‑задач

* **What V1 said**
  NX‑01/02/03 «частично пройдены», NX‑04+ — «следующий этап», NX‑05/06/07/08 — «planned». Не учтена уже проделанная почтовая/identity/Playwright‑работа и частичный прогресс по gateway/issuance.

* **New reality**

  * NX‑02: gateway routing и health уже серьёзно улучшены через infra‑merge (MassTransit, OTEL, health‑checks в `Program.cs`).
  * NX‑03: были конфликты в issuance/registry/settlement `Program.cs` и csproj, решены с учётом MIGRATE_ON_STARTUP и доменных миграций.
  * NX‑05/06/07: UK1‑SMTP, Keycloak verifyEmail/forgot и Playwright backoffice уже частично закрывают цели.

* **Corrected conclusion / recommendation**
  В V2 надо считать NX‑01/02/03 задачами «подвести итоги и зафиксировать», а не «строить с нуля», а NX‑05/06/07 — «refine & formalize» сверху существующего UK1‑состояния.

---

### 8. `memory-bank` и `.ai` как часть процесса

* **What V1 said**
  Советовал либо вынести `memory-bank` из дерева, либо хотя бы жёстко игнорировать для агентов как шумной зоны. 

* **New reality**
  `memory-bank` (через symlink) и `.ai/git` используются как основное хранилище внутренних отчётов, вкл. полный audit infra ветки и merge‑стратегию, на которых мы сейчас опираемся.

* **Corrected conclusion / recommendation**
  `memory-bank` — **feature**, не баг. Делать:

  * пометить его как knowledge‑storage (not authoritative for code),
  * выключить из LLM‑индексации/grep по умолчанию,
  * оставить структуру, но дать dev’ам явную инструкцию, как им пользоваться.

---

## 2) Обновлённая архитектура (infra.defis.deploy + UK1)

Короткий snapshot, который можно вставить в docs:

1. **Monorepo layout**:

   * `apps/` (Next.js порталы issuer/investor/backoffice + .NET `api-gateway`),
   * `services/` (identity, issuance, registry, settlement, compliance, integrations),
   * `packages/` (domain, contracts, dotnet‑clients, TS SDK),
   * `ops/` (Terraform/Timeweb, GitOps/GitLab Agent, Helm, scripts),
   * `docs/`, `audit/`, `chaincode/`, `tests/`, `tools/`, `tasks/`, `memory-bank/`. 

2. **Core домены**:

   * Issuance/Registry/Settlement реализуют полный lifecycle ЦФА (выпуск → покупка → выплаты/погашение) с DLT‑слоем в `chaincode/`.
   * Compliance/Identity отвечают за KYC/KP, аудит, роли и Keycloak/OIDC proxy.

3. **Contracts & clients**:

   * Истина по REST/Events — `packages/contracts` (OpenAPI/AsyncAPI + JSON Schema).
   * Shared доменная модель — `packages/domain`.
   * Клиенты — `packages/dotnet-clients` и `packages/sdks/ts` (autogen).

4. **Edge слой**:

   * В коде: `apps/api-gateway` (YARP, auth, rate limiting, metrics).
   * В прод‑demo (UK1): Cloudflare DNS+TLS → системный nginx → `api-gateway` и Next.js порталы; Keycloak отдаёт OIDC для NextAuth.

5. **Ops/Infra**:

   * `ops/infra/timeweb` + `docs/dlt/k8s-deploy.md` — K8s/Fabric/Timeweb дизайн. 
   * `ops/gitops/gitlab-agent` — GitOps layout для k8s.
   * Для UK1: runbook `docs/deploy/20251113-cloudflare-ingress.md` описывает docker‑compose стек, nginx, Cloudflare, Keycloak, SMTP.

6. **Tests**:

   * Unit/integ тесты по сервисам, E2E (`tests/e2e` для backend, `tests/e2e-playwright` для порталов).
   * UK1 smoke: issuer/investor/self‑registration/backoffice Playwright, привязанные к доменам `*.cfa.llmneighbors.com`.

7. **Branching**:

   * `infra.defis.deploy` = merge deploy‑ветки (runtime tweaks + runbooks) и infra‑ветки (observability, GitOps, audit pack); именно с неё продолжается работа.

---

## 3) 2–3 недельный план по NX‑таскам (40–60h)

### Приоритеты и зависимости (сверху вниз)

* **Фаза 1 (неделя 1)**: NX‑01, NX‑02, NX‑03 — зацементировать спеки, gateway и issuance, чтобы всё соответствовало UK1 и тестам.
* **Фаза 2 (неделя 2)**: NX‑04 — registry order flow + DLT, с опорой на уже настроенный gateway/issuance.
* **Фаза 3 (неделя 2–3)**: NX‑05/06 — identity baseline + CI gates, используя текущий UK1/SMTP и GitLab CI.
* **Фаза 4 (неделя 3+)**: NX‑07/08 — backoffice KYC + audit UI, уже поверх стабильных API/identity.

### Таблица по NX‑задачам

| Task                                                          | Фаза / порядок        | Goal                                                                                                                                         | Prereqs (docs/spec/tests)                                                                                                                        | Done‑when (DoD, 4–6 пунктов)                                                                                                                                                                                                                                                                                                                                                                                | Agent‑friendly?                                                                                                                                        |
| ------------------------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **NX‑01** Spec validation + API/Event Matrix                  | 1                     | Спецификации OpenAPI/AsyncAPI/JSON Schema валидны и отражают фактические REST/Events; есть актуальная матрица API/топиков для ключевых флоу. | `docs/context/WBS-OIS.md`, `PROJECT-CONTEXT`, `RULES-SUMMARY`, `packages/contracts/*`, текущие `*-report.md`.                                    | - [ ] Команда lint/validate (Spectral/AJV) прописана в `tools/`/Makefile и зелёная на `infra.defis.deploy`.<br>- [ ] Расхождения spec↔код либо устранены, либо явно помечены TODO/ARCHIVE assumptions.<br>- [ ] Обновлён API/Event‑matrix (Markdown) с датой, ссылками на спеки и сервисы.<br>- [ ] Matrix привязан к NX‑задачам (какой endpoint закрывает какой slice).                                    | **Partial** — агент может гонять lint и собирать матрицы; финальное решение по расхождениям/доменным инвариантам — руками.                             |
| **NX‑02** Gateway routing + health/metrics                    | 1 (параллельно NX‑01) | Убедиться, что YARP‑маршруты, auth‑политики и health/metrics покрывают все нужные сервисы, и это отражено в UK1.                             | Итог NX‑01 по gateway, `apps/api-gateway/appsettings*.json`, `docs/deploy/20251113-cloudflare-ingress.md`, `docs/ops/quick-start-production.md`. | - [ ] Все backend‑сервисы имеют `/health` и `/metrics`, проверено как локально, так и через UK1 домены.<br>- [ ] YARP‑routes полностью соответствуют API‑matrix (path, метод, auth).<br>- [ ] Ошибки health/metrics, найденные на UK1, отработаны и задокументированы.<br>- [ ] Runbook по UK1 дополнен секцией «how to verify gateway & metrics».                                                          | **Yes** — шаблонные правки appsettings/health‑wiring и проверку можно отдать агенту, но итоговую проверку по живому стенду делает человек.             |
| **NX‑03** Issuance endpoints alignment + tests                | 1–2                   | Свести контракт issuance API с реализацией, покрыть happy‑path тестами (unit/integ + 1–2 e2e сценария).                                      | NX‑01/02, `services/issuance/*`, соответствующие `openapi-issuance*.yaml`, существующие тесты/трехи.                                             | - [ ] Все issuance‑эндпоинты из OpenAPI реально существуют и отдают ожидаемые коды/модели.<br>- [ ] Нет падающих unit/integ тестов по issuance; покрытие ключевых путей ≥ целевого минимума (пусть даже 60–70% на старте).<br>- [ ] E2E сценарий (Playwright или другой) закрывает создание выпуска и базовый lifecycle на dev/UK1.<br>- [ ] Отчёт по результатам (короткий Markdown) приложен к NX‑03.     | **Partial** — написать новые тесты/сравнить DTO со спеками может агент; менять бизнес‑логику и схемы — только с ручным ревью.                          |
| **NX‑04** Registry orders flow (create→reserve→paid) + events | 2                     | Обеспечить полный порядок: заказ → резервирование → оплата, консистентность между registry/settlement/DLT, покрытие тестами и событиями.     | NX‑01/03, `services/registry/*`, `services/settlement/*`, AsyncAPI, `docs/dlt/*`, фронтовые флоу investor.                                       | - [ ] Sequence diagram «Investor buy flow» обновлена/создана в `docs/architecture/uml` с упоминанием DLT и событий Kafka.<br>- [ ] AsyncAPI топики (`ois.order.*`, `ois.payout.*`) реально публикуются/консумятся по схеме.<br>- [ ] Unit/integ тесты по registry/settlement закрывают happy‑path и базовые edge‑кейсы.<br>- [ ] E2E сценарий (регистрация инвестора → покупка ЦФА) зелёный против dev/UK1. | **Partial** — агенту можно доверить генерацию/расширение тестов и сверку AsyncAPI↔код; согласование доменной модели и DLT‑инвариантов — вручную.       |
| **NX‑05** Identity/Keycloak baseline                          | 3                     | Сделать identity‑слой (Keycloak realm + identity service + NextAuth) явно описанным и воспроизводимым, используя уже рабочий UK1‑настройки.  | UK1 runbook (Cloudflare/Keycloak/SMTP), `services/identity/*`, `FRONTEND-CONTEXT`, OpenAPI для identity, Playwright login‑сценарии.              | - [ ] В `docs/deploy`/`docs/ops` есть раздел «Identity/Keycloak» с realm/clients/roles и SMTP‑настроикой.<br>- [ ] Identity service строго соответствует OpenAPI (token/refresh/oidc‑config), проверено спек‑тестами.<br>- [ ] Все три портала используют единый конфиг NextAuth/roles, привязанный к Keycloak ролям/claims.<br>- [ ] Playwright‑логины investor/issuer/backoffice проходят в dev и UK1.    | **Partial** — генерацию конфигов и проверку OpenID‑метаданных можно поручить агенту; правки realm/ролей и security‑решения — только руками.            |
| **NX‑06** CI quality gates (Spectral/AJV/tests/coverage)      | 3                     | Включить базовые quality gates в GitLab CI: spec‑lint, schema validate, тесты, покрытие и публикацию артефактов.                             | `.gitlab-ci.yml` из infra, `docs/ops/quick-start-production.md`, результаты V1‑аудита CI, существующие trx/coverage.                             | - [ ] В пайплайне есть stage `spec-lint` (Spectral/AJV) и он падает при нарушении правил.<br>- [ ] Unit/integ + Playwright запускаются как минимум в nightly/job по MR в `infra.defis.deploy`.<br>- [ ] Генерируются отчёты покрытия (даже грубые) и прикладываются к job‑артефактам.<br>- [ ] README/док в `docs/ops` описывает CI‑стадии и ожидаемые gates.                                               | **Yes** — это довольно шаблонная DevOps‑работа, пригодна для агента под твоим ревью.                                                                   |
| **NX‑07** Backoffice KYC + User Registry                      | 4                     | Довести backoffice до MVP: рабочий список KYC‑тасков и реестр пользователей (5625‑У) с простым UI и привязкой к compliance/identity.         | `FRONTEND-CONTEXT`, `services/compliance/*` (KYC/tasks), OpenAPI KYC endpoints, текущий backoffice UI, Playwright backoffice‑auth spec.          | - [ ] Endpoints `/v1/compliance/kyc/*` и `/v1/kyc/tasks` реализованы и протестированы (unit/integ).<br>- [ ] Backoffice имеет страницы KYC‑тасков и user registry с базовыми фильтрами/поиском.<br>- [ ] Есть Playwright‑сценарий «admin просматривает KYC‑таск, approves/rejects».<br>- [ ] В CONTEXT‑доках описано, какие regulatory требования закрывает этот UI.                                        | **Partial** — верстку/подключение SDK может делать агент; трактовка регуляторки и разрешение edge‑кейсов — только вручную.                             |
| **NX‑08** Backoffice Audit Log UI                             | 4 (вместе с NX‑07)    | Поднять UI над уже существующим audit‑API: просмотр/фильтрация аудиторских событий и экспорт CSV.                                            | OpenAPI по `/v1/audit`, реализация audit‑эндпоинтов в compliance, `shared-ui` компоненты, `FRONTEND-CONTEXT`.                                    | - [ ] Backend audit‑эндпоинты соответствуют OpenAPI и проходят spec‑tests.<br>- [ ] В backoffice есть страница Audit Log с фильтрами (actor/action/entity/date/limit), работающими против живого API.<br>- [ ] CSV‑экспорт проверен на тестовых данных.<br>- [ ] Есть хотя бы один E2E сценарий «admin фильтрует аудит и выгружает CSV».                                                                    | **Yes/Partial** — UI и wiring к уже готовому API — хороший «лист» для агента; но окончательные требования к аудит‑данным лучше контролировать вручную. |

---

## 4) Repo hygiene & структурные рефакторы (1–2 дня)

С учётом новой реальности (UK1, infra.defis.deploy, memory-bank как feature) — минимальный, но полезный набор:

1. **Root README → «как читать репо сейчас»**

   * Добавить разделы: *Structure*, *Branches* (`infra.defis.deploy` как mainline), *Environments* (CFA1 — legacy, UK1 — актуальный demo), *Where to start* (PROJECT/FRONTEND‑CONTEXT + WBS‑OIS).

2. **`docs/README.md` + `docs/INDEX.md`**

   * Развести: `docs/architecture`, `docs/context`, `docs/deploy`, `docs/dlt`, `docs/ops`.
   * В `INDEX.md` явно перечислить ключевые входы: WBS‑OIS, PROJECT/FRONTEND‑CONTEXT, UK1‑runbook, K8s/Fabric‑гайд.

3. **Явно пометить `audit/` как snapshot**

   * Добавить `audit/README.md`: что это внешний аудит с датами и что *living decisions* по infra — в `docs/ops`/`docs/deploy`, а не здесь. Это снизит риск, что агент/новичок воспримет отчёт как «актуальную правду». 

4. **`ARCHIVE/README.md` и пометки legacy‑runbook’ов**

   * Обозначить, что туда уезжают CFA1‑специфичные runbook’и/допущения; в README дать правило: «если док противоречит docs/* — docs прав».

5. **`packages/README.md` (contract‑first)**

   * Кратко описать:

     * `contracts` = истина по API/Events,
     * `domain` = shared kernel без EF,
     * `dotnet-clients`/`sdks` = autogen (не править руками).

6. **Выделить generated‑код**

   * Лёгкий шаг: либо перенести `packages/dotnet-clients` в `packages/generated/dotnet-clients`, либо хотя бы положить туда `.gitattributes`+`README` с пометкой `auto‑generated`. Это сильно помогает агентам/людям отличать код, который можно рефакторить, от артефактов.

7. **`tests/README.md`**

   * Описать структуру тестов: unit/integ по сервисам, `tests/e2e` (backend E2E), `tests/e2e-playwright` (порталы, вкл. UK1‑ориентированные спеки), какие команды запускать для dev vs UK1.

8. **`memory-bank/README.md` + ignore‑настройки**

   * Коротко: «журнал и аналитика, не authoritative для кода, но важен для контекста».
   * Убедиться, что `memory-bank` и `.ai` добавлены в `.cursorindexingignore`/аналогичные файлы, чтобы агенты не тонули в логах по умолчанию.

9. **`ops/README.md`**

   * В одном месте описать: Timeweb/Terraform/GitOps (как «infra‑готовый слой») и UK1/docker‑compose (как текущий demo), с ссылками на конкретные runbook’и.

Этого набора реально хватит на 1–2 дня и он радикально снизит онбординг‑фрикцию + шум для LLM‑агентов.

---

## 5) Agentification V2 (Trees/Leaves mindset)

### «Листья» — задачи для агентов (5–10 паттернов)

1. **Поддержка API/Event‑матриц и spec‑lint (NX‑01 support)**

   * Агент может собирать отчёты по OpenAPI/AsyncAPI, запускать Spectral/AJV, обновлять markdown‑матрицы и подсвечивать расхождения — без права менять сами контракты.

2. **Шаблонный health/metrics wiring в сервисах (NX‑02)**

   * По образцу уже настроенных сервисов агент добавляет/правит подключения OTEL/Prometheus/health‑checks в `Program.cs`, не трогая доменную логику. 

3. **Unit‑тесты для value objects и простых DTO (`packages/domain`, простые сервисные модели)**

   * Расширение `domain.Tests` и сервисных тестов edge‑кейсами (валидация Money, schedule, простые мапперы) при чётко заданных инвариантах.

4. **Генерация/обновление TS/.NET клиентов по OpenAPI**

   * На вход — `packages/contracts/openapi-*.yaml`; на выход — обновлённый `packages/dotnet-clients` и TS SDK, с соблюдением «do not edit manually». Здесь агент просто управляет генератором.

5. **Мелкие UI‑фичи в порталах (issuer/investor/backoffice)**

   * Примеры: подключить новый отчёт / список через уже существующий SDK, добавить фильтры/сортировку, не меняя глубокую бизнес‑логику. Особенно хорошо ложится на NX‑07/08.

6. **Расширение Playwright‑spec’ов для уже реализованных флоу**

   * Добавить новые сценарии (например, forgot‑password, простые KYC‑view) поверх существующих логин‑спеков для UK1, с аккуратной параметризацией доменов.

7. **Helm/manifest tweaks для observability/gateway**

   * Добавление labels/annotations, prometheus scrape‑конфигов, не меняя топологию кластера или security‑политики.

8. **CI pipeline hardening (NX‑06)**

   * Вставка spec‑lint/test/coverage stage в `.gitlab-ci.yml` по заданному шаблону, wiring артефактов и базовых правил fall‑fast.

9. **Runbook‑консолидация в docs/deploy/ops**

   * Собрать из существующих логов/пошаговых файлов компактные checklists (в стиле 20251113‑cloudflare‑ingress) для повторяемых операций.

10. **EF‑миграции для небольших изменений схемы**

    * Генерировать миграции и описывать diff в доке; применять в базе и решать сложные data‑migrations всё равно должен человек.

---

### «Ствол» — что оставлять под ручной контроль (3–5 паттернов)

1. **Изменения доменных контрактов (`packages/domain`, `packages/contracts`)**

   * Любое изменение схемы ЦФА/кошельков/заказов, новых полей KYC, лэйаута audit‑events — это пересборка смыслового каркаса системы и привязка к регуляторке; агент может помочь подсветить diff, но не принимать решения.

2. **DLT/Hyperledger Fabric topology и chaincode**

   * Настройка ордереров/peers, HA, chaincode‑lifecycle, изменение логики в `chaincode/*` — это высокорисковый слой, требующий глубокого понимания и ручного контроля.

3. **Identity/Keycloak realm design и роль/политики**

   * Маппинг ролей/клеймов, настройка клиентов, security‑policies, особенно в части доступа к registry/settlement/compliance — зона, где любая ошибка = security incident. Агент — только советник/генератор конфигов.

4. **Глубокие cross‑service рефакторинги (разбиение сервисов, смена инвариантов, пересмотр AsyncAPI)**

   * Ломают интеграции и тестовую пирамиду; здесь лучше сначала руками построить план/diagram, а потом уже частично использовать агента для механических изменений.

5. **Security/compliance‑решения и регуляторные отчёты**

   * Всё, что упирается в STO BR/5625‑У/259‑ФЗ, threat‑model и SoC‑playbooks, должно приниматься живым архитектором; агент может помогать писать черновики отчётов и чек‑листы, но не ставить галочки «соответствует/не соответствует».

---

## Итоговая сводка (V2)

| Area                      | Issue or Question                                                                                                  | V2 recommendation                                                                                                                                                                                      |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Environments & branches   | V1 считал infra теоретической, UK1/Cloudflare/SMTP/E2E не были учтены; merge‑стратегия воспринималась как будущее. | Фиксируем: UK1 — реальный demo (Cloudflare/nginx/Keycloak/Postfix/Playwright), `infra.defis.deploy` — основная ветка. Дальше — стабилизация и развитие её, а не проектирование merge.                  |
| NX‑roadmap                | NX‑01..08 планировались «с нуля», без учёта уже сделанной SMTP/identity/E2E/infra работы.                          | Фаза 1: зацементировать NX‑01/02/03; Фаза 2: NX‑04; Фаза 3: NX‑05/06; Фаза 4: NX‑07/08. Везде использовать UK1+Playwright как acceptance‑gates.                                                        |
| Docs & runbooks           | `docs/`, `audit/`, `ARCHIVE/`, `memory-bank` пересекаются, трудно понять, что актуально.                           | Ввести README/INDEX по ключевым папкам, пометить `audit` как snapshot, `ARCHIVE` как legacy, `memory-bank` — как knowledge‑storage; UK1‑runbooks выделить явно как основной operational source.        |
| Packages & generated code | Контракты, domain и generated‑клиенты перемешаны; непонятно, что редактировать, а что нет.                         | Формализовать contract‑first: `contracts`+`domain` = истина, `dotnet-clients`/TS SDK = generated; вынести generated в отдельный подкаталог или хотя бы пометить в README/атрибутах.                    |
| Infra priority            | В1 пытался одновременно закрыть docker‑compose и Timeweb/K8s.                                                      | В горизонте 2–3 недель фокус на UK1 (docker‑compose demo) + dry‑run валидация infra (Terraform/Helm/GitOps) без разворачивания прод‑кластера.                                                          |
| Testing & CI              | E2E и CI рассматривались абстрактно, без привязки к UK1 smoke‑набору.                                              | Сделать Playwright‑suite (issuer/investor/self‑reg/backoffice) официальным smoke‑gate, добавить spec‑lint/tests/coverage в GitLab CI (NX‑06), завязать NX‑таски на эти gates.                          |
| Agentification            | Граница между «можно отдать агенту» и «нельзя» была размытой.                                                      | Trunk: доменные контракты, DLT, identity, security/compliance, глубокие рефы. Leaves: тесты, матрицы, SDK, UI‑мелочи, runbooks, CI‑gates, шаблонные infra‑tweaks — но всегда с твоим финальным review. |

Если захочешь, могу дальше разложить это в формат прямого sprint‑плана (по дням/слотам) с пометкой «я / агент» и привязкой к конкретным файлам/командам.

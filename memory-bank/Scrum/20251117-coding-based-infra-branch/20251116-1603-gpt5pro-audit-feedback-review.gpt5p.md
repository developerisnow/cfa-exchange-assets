# Prompt

You are Oracle, a focused one-shot problem solver3c63Emphasize direct answers, cite any files referenced, and clearly note when the search tool was used3c63You are GPT‑5 Pro acting as a senior system/solution architect and codebase reviewer3c63I have attached: - `c2p_ois-cfa
txt`: a 4MB code2prompt snapshot of the `ois-cfa` repository (branch `infra.defis.deploy`), including structure and key files; - a recent session log from my infra-focused work on AVA1/eywa1 (how I interact with this repo and infra); - two architecture context files about "Trees, Leaves and Agents" (my target way of working through AI agents on top of this codebase)3c63High-level context (in my own words): - Repo `ois-cfa` is the core 
NET/Next
js implementation of an RWA/CFA exchange platform3c63- There has been a large merge: `deploy` + `infra` → `infra.defis.deploy` (~599 files + ~20 follow-up commits from Aleksandr)3c63This branch now carries serious infra/observability work plus some deploy-time tweaks3c63- I (Alex) already did infra discovery, billing/reporting to the founder, and created tasks under `tasks/NX-*
md` and context docs under `docs/context/*`, plus some AGENTS/manifest work in an outer mono-repo3c63- Now I want to deeply understand this repo as it stands on `infra.defis.deploy`, so that I can: - continue bringing up the full environment (docker-compose, k8s/ops, Keycloak, Kafka, etc
); - execute the `tasks/NX-*
md` workstream in a sane order; - and later drive the work via AI agents (Claude/Codex/GPT‑5) safely and productively3c63What I need from you: 1) **Repository structure and architecture audit (macro level)** - Walk through the high-level structure you see in `c2p_ois-cfa
txt` (apps / ARCHIVE / audit / chaincode / docs / memory-bank / ops / packages / services / tests / tools, etc
)3c63- For each top-level folder, explain in Russian (with B2 English terms) what its intended role seems to be, how cohesive it looks, and whether anything stands out as confusing or inconsistent (e
g
, `ARCHIVE`, `audit` vs `docs`, `chaincode` vs `apps`)3c63- Comment on how sane the overall architecture feels: layering, separation between domains (identity/issuance/registry/settlement/compliance), and how infra/ops is wired into the app3c632) **Packages and contracts understanding** - Explain the intent behind `packages/*` (contracts, schemas, sdks, dotnet-clients, typescript-gateway, etc
)3c63- How do these packages relate to services and apps? Does it look like a clean contract-first approach (AsyncAPI/OpenAPI → generated clients), или есть смешение слоёв? - Highlight any obvious risks or anti-patterns (e
g
, too much generated code in the main tree, duplication between packages and services)3c633) **Tasks and docs as a work driver** - Look at `tasks/NX-01


NX-08*
md` and `docs/context/*` (FRONTEND-CONTEXT, PROJECT-CONTEXT, PROMPTS-MAP, RULES-SUMMARY, WBS-OIS) in the snapshot3c63- Сформулируй, как бы ты структурировал работу на ближайшие 2–3 недели: - какую задачу из `tasks/NX-*` брать первой, второй, третьей и т
д3c63(и почему); - какие контекстные доки стоит дочитать/дополнить, чтобы эти задачи стали исполнимыми без постоянного "копания" в коде; - где нужны дополнительные specs/sequence diagrams, прежде чем лезть в refactor/feature work3c634) **Critique of repo hygiene and structure** - Дай честный, но конструктивный разбор: что бы ты поменял в корневой структуре (например, ARCHIVE/audit/docs/memory-bank/chaincode), чтобы: - новому разработчику было легче ориентироваться; - AI-агентам было проще работать (меньше noise, понятные contract/impl split); - future me не утонул в mix of infra/app/docs3c63- Предложи конкретные refactoring steps по структуре (без кода), которые можно выполнить за 1–2 дня и которые дадут сильный выигрыш в понятности3c635) **Agentification angle** - С учётом приложенных файлов про Trees-Leaves-and-Agents: - Предложи, какие части этого репо логичнее всего отдавать AI-агентам ("Leaves"), а какие оставлять под ручной контроль ("Tree"/"Trunk")3c63- Приведи примеры 5–10 конкретных задач по репо `ois-cfa`, которые хорошо подходят для агентов (с ограничениями), и 3–5 задач, которые лучше делать только руками (или руками+агент как ассистент)3c63Формат ответа: - Пиши по-русски, используя термины/слэнг уровня senior engineer (B2 English ок)3c63- Структура: - TL;DR (3–5 bullets) - Разделы по пунктам 1–5 (чёткие подзаголовки, bullets, без воды) - В конце компактная таблица: "Area" / "Issue or Question" / "Your recommendation"3c63- Не пересказывай полностью содержание приложенных файлов, концентрируйся на выводах и планах


# Report3c63 **TL;DR**

- Архитектура infra.defis.deploy в целом здравая: mono‑repo `/apps + /services + /packages + /ops` с чёткими bounded contexts и контрактами в `packages/contracts`, плюс плотный слой DevOps/observability поверх .NET/Next.js.
- `packages/*` явно задуманы как contract‑first слой (OpenAPI/AsyncAPI → generated clients + TS SDK), но с риском «генерилка в основном дереве» и дублирования моделей между контрактами и сервисами.
- План на 2–3 недели: 1) стабилизировать dev/prod окружения по runbook’ам (`docs/deploy`, `docs/ops`), 2) добить NX‑03/04 (issuance+registry core flow), 3) включить NX‑05/06 (identity + CI/observability), 4) потом уже фронтовые NX‑07/08 (backoffice KYC + audit UI).
- Быстрый hygiene‑рефакторинг: вынести `ARCHIVE` и тяжёлые аудиторские отчёты, чётко развести `/docs` vs `/audit`, изолировать `memory-bank` и generated‑клиенты; добавить README/OWNERS по верхним папкам.
- В модели Trees/Leaves/Agents: «ствол» — контракты, архитектура, ops‑runbooks и регуляторка; «листья» — маленькие локальные изменения (тесты, мелкий UI, helm/compose правки)3c63Агенты можно спокойно пускать на leaves, но держать их подальше от доменной модели и audit‑доков.

> Примечание: я прошёлся по снапшоту и контекстным файлам через внутренний search‑tool `file_search`; ниже везде даю ссылки на конкретные фрагменты.

---

## 1) Архитектурный обзор и структура репозитория (macro)

### Корень и верхний уровень

По `Source Tree` и архитектурным докам структура выглядит так: `apps/`, `services/`, `packages/`, `ops/`, `docs/`, `audit/`, `chaincode/`, `tests/`, `tools/`, `memory-bank` (symlink), плюс `ARCHIVE` для старых артефактов.

Роли по папкам:

- **`apps/`** — edge‑слой:

  - `api-gateway` (ASP.NET Core + YARP), `portal-issuer`, `portal-investor`, `backoffice`, `shared-ui` (дизайн‑система, общий UI‑кит).
  - Cohesion: высокая, все Next.js‑порталы разделены по ролям, плюс shared‑ui реально переиспользуется через preset/paths.
  - Замечание: `api-gateway` технически «backend», но логично, что он стоит рядом с фронтом как edge proxy.

- **`services/`** — доменные микросервисы:

  - `issuance`, `registry`, `settlement`, `compliance`, `identity`, `integrations/*`, `fabric-gateway` и т.п3c63Описаны в `docs/context/PROJECT-CONTEXT.md` и `docs/backend/context-map.md`.
  - У всех — единый паттерн: `Program.cs`, `DTOs`, `Infrastructure/Metrics.cs` (OTel/Prometheus), EF‑контекст + миграции, MassTransit/Kafka, Outbox.
  - Cohesion: хорошая — каждый сервис покрывает свой bounded context (issuance, registry, settlement, compliance и т.д.), связи через HTTP (gateway) и Kafka‑события.

- **`packages/`**

  - `domain` — общая доменная модель (.NET), тесты в `domain.Tests`.
  - `contracts` — OpenAPI/AsyncAPI/JSON Schema для gateway, сервисов и внешних адаптеров (банк, ЕСИА, identity).
  - `dotnet-clients` — огромный generated код OpenAPI‑клиентов (gateway, identity, и др.).
  - `sdks/ts` — TS SDK поверх тех же OpenAPI; используется фронтом.
  - `types` / `typescript-gateway`: shared TS‑типы/adapter для API‑gateway.

- **`ops/`**

  - `infra/timeweb/*` — Terraform‑модуль для Timeweb Cloud, kubeconfig/outputs.
  - `infra/helm/*` — чарты для Fabric, GitLab Runner, etc.
  - `gitops/gitlab-agent/*` — GitLab Agent GitOps layout: system/platform/business manifests, порядок синка.
  - `scripts/`, `timeweb/` — helper‑скрипты для twc, кластеров, kubeconfig.
  - Cohesion: всё про инфраструктуру и CICD, но чуть смешаны «локальный dev», Timeweb prod, GitOps и Fabric.

- **`docs/`**

  - `docs/architecture/*` — C4, UML‑последовательности, доменная модель, NFR, threat‑model.
  - `docs/backend/*` — context map и backend‑ориентированные заметки.
  - `docs/dlt/*` — Hyperledger Fabric в K8s, HA, lifecycle.
  - `docs/deploy/*` — runbooks для docker‑compose на VPS + UK1/Cloudflare/Keycloak.
  - `docs/ops/*` — quick‑start production, GitLab Runner, Timeweb CLI.
  - `docs/context/*` — PROJECT‑CONTEXT, FRONTEND‑CONTEXT, WBS, RULES‑SUMMARY, PROMPTS‑MAP3c63Это уже слой «AI/agents context».

- **`audit/`**

  - Содержит полноценный CI/CD и K8s аудит: executive summary, findings, observability/security checklists, CI templates и т.п.
  - Реально это snapshot‑отчёт по состоянию infra (на дату 2025‑11‑11/12).

- **`chaincode/`**

  - Chaincode для Fabric (issuance/registry), описание lifecycle в docs/dlt.

- **`tests/`**

  - Unit‑тесты для services (`issuance.Tests`, `registry.Tests`, и т.д.), плюс Playwright/E2E journey для порталов.

- **`tools/`**

  - Скрипты миграций, timeweb helpers, smoke‑тесты и т.п.

- **`memory-bank`**

  - Symlink на внешний memory‑repo с journaling/meeting notes3c63Не часть доменной логики, а скорее knowledge‑storage.

- **`ARCHIVE`**

  - Исторические допущения/старые доки; в RULES прямо написано, что допущения надо туда складывать.

### Оценка архитектуры

- **Layering**:

  - domain → services → gateway → portals выглядит честным3c63`packages/domain` используется во всех сервисах через ProjectReference; инфраструктура не протекает внутрь домена.
  - contracts (OpenAPI/AsyncAPI) находятся вне сервисов, что хорошо для contract‑first.

- **Bounded contexts**:

  - Чётко выделены: `issuance` (выпуск), `registry` (кошельки/ордера/держатели), `settlement` (выплаты), `compliance` (KYC/KP/аудит), `identity` (OIDC proxy/Keycloak), `fabric-gateway` (DLT).
  - context‑map и UML диаграммы хорошо накладываются на коду.

- **Инфра → app интеграция**:

  - .NET сервисы уже обвязаны HealthChecks, OpenTelemetry, Prometheus‑метриками, Kafka, миграциями; конфиг выдержан через `appsettings.*` и env.
  - Ops‑уровень (Terraform, GitOps, GitLab CI, docker‑compose) хорошо развязан от сервисов: манифесты лежат в `ops/*`, pipeline — в `.gitlab-ci.yml`, runbooks — в `docs/deploy/*`, `docs/ops/*`.

**Что сбивает:**

- `audit/` и `docs/` частично перекрывают друг друга по содержанию — документация infra размазана по обоим.
- `memory-bank` внутри репо создаёт шум для агентов/поиска, хотя по сути это внешняя хроника.
- Сгенерированный код (`packages/dotnet-clients`, часть TS SDK) засоряет дерево и может запутывать агентов (много однотипных файлов).

В целом — архитектура зрелая и довольно чистая для такого объёма infra‑изменений3c63Основная боль — не технический долг, а **обилие артефактов**, которые нужно чуть лучше разложить.

---

## 2) Понимание `packages/*` и контрактов

### Назначение пакетов

По PROJECT‑CONTEXT и PROMPTS‑MAP: `packages/*` — это «source of truth» для контрактов, домена и клиентских SDK.

- **`packages/domain`**

  - Чистая доменная модель: `Money`, `ScheduleItem`, `PayoutSchedule`, `Security.Mask*` и т.д., плюс отдельный test‑проект `domain.Tests`.
  - csproj уже аккуратно исключает тесты из билдов (`DefaultItemExcludes`, `Compile Remove=domain.Tests/**`).
  - Это хороший «shared‑kernel» между сервисами.

- **`packages/contracts`**

  - `openapi-*.yaml` для gateway/issuance/registry/settlement, `openapi-identity`, `openapi-integrations-*`, плюс `asyncapi.yaml` для Kafka и JSON Schemas доменных сущностей.
  - Используется как основа для:

    - matrix’ов API/Events (NX‑01),
    - generated .NET и TS клиентов.

- **`packages/dotnet-clients`**

  - OpenAPI Generator output: clients для gateway, identity и пр., со своими DTO и README/docs.
  - По сути build‑артефакт, хранимый в репе.

- **`packages/sdks/ts`**

  - TypeScript SDK, инкапсулирующий REST клиент (+, судя по докам, нормальный OisApiClient)3c63Используется в порталах.

- **`packages/types`, `typescript-gateway`**

  - Общие TS‑типы и обёртки для gateway (например, `getPayoutsReport()` и др.).

### Чистота contract‑first / mixing слоёв

- **Контракты** реально живут отдельно от сервисов:

  - Ссылки в PROJECT‑CONTEXT → «Источники: `packages/contracts/*`».
  - Сервисы в Program.cs и DTO явно соответствуют OpenAPI (через reports NX‑01/NX‑03).

- **Generated‑код**:

  - .NET‑клиенты лежат внутри repo, но, судя по шаблону, не редактируются руками (типичные OpenAPITools структуры).
  - Это ок, пока:

    - генерация идемпотентна,
    - есть понятный скрипт типа `tools/generate-clients.sh` (на уровне концепции — сейчас в снапшоте скрипт не увидел, но это нормальный следующий шаг).

- **Риски / анти‑паттерны**:

  - **Дублирование моделей**:

    - Есть domain‑типы (Money, ScheduleItem) и DTO в сервисах, и похожие модели в OpenAPI/clients — три разных слоя3c63Несостыковка между ними уже отмечена как риск в audit (AsyncAPI vs реализация).

  - **Generated внутри основного дерева**:

    - `packages/dotnet-clients` + часть TS SDK — шум для ревью и агентов, тяжело отличить hand‑written от поколения.

  - **Связка с доменом**:

    - domain‑модель сейчас не «чисто неизолирована» от persistence (Money/Ids норм, но EF‑entities лежат в сервисах, это хорошо; главное — не тащить EF в `packages/domain`, сейчас не тащите).

**В сухом остатке:** это довольно чистый **contract‑first + shared‑kernel** подход, но стоит формализовать:

- что считается истиной (OpenAPI/AsyncAPI + JSON Schema);
- где можно править руками (contracts, domain, сервисы);
- где строго «генерим и не трогаем» (dotnet‑clients, часть TS SDK).

---

## 3) Tasks/NX-\* и контекстные доки: как строить работу 2–3 недели

Опираюсь на `docs/context/WBS-OIS.md`, PROJECT/FRONTEND‑CONTEXT и deploy/ops‑runbooks.
Плюс — на лог из сессии и статус infra.defis.deploy (NX‑01/02/03 частично уже сделаны).

### Что за NX‑задачи (по WBS + названию файлов)

- **NX‑01** — Spec validation + API/Event Matrix.
- **NX‑02** — API Gateway routing + health/metrics.
- **NX‑03** — Issuance endpoints alignment + tests.
- **NX‑04** — Registry order flow (create → reserve → paid) + events.
- **NX‑05** — Identity/Keycloak integration baseline (пока planned).
- **NX‑06** — CI quality gates (Spectral/AJV/tests/coverage).
- **NX‑07** — Backoffice KYC and User Registry (из названия и FRONTEND‑CONTEXT).
- **NX‑08** — Backoffice Audit Log UI (название + контекст по audit‑событиям).

### Предлагаемый порядок работ (реалистичные 2–3 недели)

**03c63Bootstrap окружений (1–2 дня, параллельно всему)**

Цель: иметь работающий dev‑контур (docker‑compose на VPS/локально) и базовый k8s‑контур (Timeweb/UK1) для smoke‑тестов.

- Пройти по `docs/deploy/docker-compose-at-vps/*` и `docs/ops/quick-start-production.md`.
- Проверить Keycloak, gateway, базовые health‑endpoint’ы сервисов.
- Добить GitLab Runner токен, чтобы CI снова начал выполнять jobs.

**13c63«Зацементировать» NX‑01/NX‑02/NX‑03 (2–3 дня)**

Они уже частично пройдены (есть matrix, reports и TRX‑лог с падением пары тестов по issuance).

- Обновить `tasks/NX-01-spec-validate-and-matrix.md` по фактическому статусу:

  - убедиться, что OpenAPI/AsyncAPI/JSON Schema чисто проходят lint/validate;
  - зафиксировать команду для lint в `tools/` + Makefile.

- NX‑02:

  - свести фактический YARP routing (`apps/api-gateway/appsettings.json`) с API‑matrix;
  - убедиться, что health/metrics endpoints есть у всех сервисов (Program.cs + Metrics.cs), поправить конфиг где надо.

- NX‑03:

  - добить падующие тесты issuance API (в trx видно, что 404/500 mismatch).
  - выровнять DTO/контракты/реализацию.

**23c63NX‑04: Registry order flow (3–4 дня)**

Цель: полный happy‑path order → reserve → paid между portal‑investor → registry → settlement → ledger.

- Перед кодом — **sequence diagram**:

  - доработать/добавить UML‑sequence для покупочного флоу с детализацией registry/settlement/KYC/банк.

- Сверить:

  - endpoints registry по OpenAPI `openapi-registry.yaml`;
  - события `ois.order.*`, `ois.registry.transferred` по AsyncAPI vs фактические consumers.

- Добавить/починить:

  - unit/integration тесты registry (order creation, reserve, mark paid);
  - e2e‑journey для investor (у тебя уже есть Playwright tests, их можно расширить).

**33c63NX‑05 / NX‑06: Identity + CI/observability (4–5 дней)**

- **NX‑05 (Identity/Keycloak baseline)**:

  - identity service (OIDC proxy) ↔ Keycloak realm: проверить, что OpenAPI‑контракт identity совпадает с фактом;
  - фронт: NextAuth конфиг в порталах (+ roles mapping).
  - зафиксировать `docs/ops/keycloak` или раздел в `docs/deploy`.

- **NX‑06 (CI quality gates)**:

  - Spectral lint для OpenAPI, AJV для JSON Schema;
  - сбор TRX/JUnit отчётов по `dotnet test`, npm test, Playwright3c63Сейчас есть отдельные trx‑артефакты, но нет систематических репортов.
  - минимальный coverage (даже грубая линия по dotnet‑coverage).

**43c63NX‑07 / NX‑08: Backoffice (6–7 дней, частично параллельно)**

- На основе `FRONTEND-CONTEXT` и PROJECT‑CONTEXT: привести backoffice к MVP — KYC workflow, user registry (5625‑У), audit log UI.
- NX‑07:

  - UI для KYC approve/reject, квалификации инвесторов и user registry;
  - опора на endpoints compliance/identity/registry.

- NX‑08:

  - Audit log timeline (у тебя уже есть `AuditLog` компонент в shared‑ui, его надо просто подключить к backend‑событиям).

### Какие доки дочитать/дополнить

13c63**Обязательно дочитать:**

   - `docs/context/PROJECT-CONTEXT.md` — общий контекст.
   - `docs/context/FRONTEND-CONTEXT.md` — что реально нужно по порталам (особенно backoffice).
   - `docs/context/WBS-OIS.md` — чтобы не терять связь NX задач с milestones.
   - `docs/context/RULES-SUMMARY.md` — дисциплина spec‑first/test‑first, запреты для агентов.

23c63**Дописать / заапдейтить:**

   - короткий `README.md` в корне `ops/`, `services/`, `apps/` с «как собрать/запустить» и owner’ами;
   - раздел про identity/Keycloak в `docs/deploy` (сейчас разбросано).
   - добавить простую диаграмму «Issuance+Registry+Settlement happy‑path» в `docs/architecture/uml`.

33c63**Где нужны доп3c63diagrams/specs до рефакторинга:**

- Issuance/Registry/Settlement state‑diagram (CFA lifecycle уже есть, но без денег/кошелька).
- Полнейший sequence «Investor buy flow» (есть UML‑sequence, но можно чуть уточнить роли identity/KYC).
- Инфра‑диаграмма для Timeweb K8s + GitLab Agent + ArgoCD (частично есть в audit, но не как схема).

---

## 4) Repo hygiene и структурные рефакторы

Цель: облегчить навигацию для людей и агентов, снизить шум от infra/docs и generated‑кода.

### Что я бы поменял в корне

13c63**Отдельный «docs vs audit» split**

   - Оставить `docs/` как **живые спецификации и runbook’и** (source of truth).
   - `audit/` переименовать в `audit-reports/` или `reports/` и явно подписать, что это **snapshot‑отчёты** с указанием даты.

23c63**ARCHIVE вынести на один уровень выше или явно пометить**

   - Либо перенос в отдельный репо, либо хотя бы `ARCHIVE/README.md` с описанием «legacy, не трогать / не использовать как истину».

33c63**Изолировать `memory-bank`**

   - По сути это submodule/ссылка на внешний knowledge‑repo.
   - Варианты:

     - убрать из submodule/рабочего дерева и держать вне (с инструкцией в README);
     - или оставить, но включить в `.cursorindexingignore`/аналог для агентов.

43c63**Generated‑клиенты**

   - Перенести `packages/dotnet-clients` в `generated/dotnet-clients` или `packages/generated/dotnet-clients`, с README о том, как их регенерировать.
   - Отметить это же в `RULES-SUMMARY` как «агентам сюда можно только читать, не править».

53c63**Чёткий ops‑layout**

   - Внутри `ops/` сделать группы:

     - `ops/infra/terraform/...`
     - `ops/infra/helm/...`
     - `ops/gitops/gitlab-agent/...`
     - `ops/scripts/...`

   - Это уже почти так, но стоит добавить README с «порядком развертывания» (ссылаясь на docs/ops и docs/dlt).

63c63**Мини‑информер по тестам**

   - В `tests/README.md` описать:

     - какие test‑пакеты есть (unit vs e2e vs perf);
     - как их запускать и где искать репорты.

   - Сейчас информация размазана по docs/context и отдельным trx/logам.

### 1–2 дня конкретных шагов

Реальный actionable план на 1–2 дня:

13c63**Добавить root‑README секции «Structure» и «How to read this repo»**

   - На основе `docs/architecture/00-Структура-системы-и-проекта.md` и PROJECT‑CONTEXT.

23c63**Создать README в ключевых папках**: `apps/`, `services/`, `packages/`, `ops/`, `docs/`, `tests/`, `audit/`.

   - Для каждого: назначение, под‑структура, ключевые entry‑points и owners.

33c63**Переименовать/пометить `audit/` и `ARCHIVE/`**

   - `audit/README.md`: «регулярный аудиторский отчёт на дату X, не обновляется автоматически».
   - `ARCHIVE/README.md`: «legacy assumptions, not authoritative».

43c63**Отдельный раздел `generated/`**

   - Переместить `packages/dotnet-clients` сюда (или хотя бы добавить `.gitattributes`/`CODEOWNERS` и README: «autogenerated, do not edit»).

53c63**Настройка ignore для memory‑bank**

   - Убедиться, что `memory-bank` исключён из индексирования агентами (`.cursorindexingignore`) и тестов.

Эти шаги сильно снизят когнитивный шум и для людей, и для LLM/агентов.

---

## 5) Agentification: Trees, Leaves and Agents применительно к `ois-cfa`

Опираюсь на TLA‑слайды/транскрипт: trunk = архитектура/контракты/контексты; leaves = локальные задачи с ограниченной blast‑radius; сложные cross‑cutting штуки нельзя отдавать агентам «в одиночку».

### Что — «Trunk» (ручной контроль)

- **Доменные контракты и правила:**

  - OpenAPI/AsyncAPI в `packages/contracts/*`;
  - доменная модель `packages/domain`;
  - backend context map и UML (lifecycle/state/sequence).

- **Регуляторная и security‑архитектура:**

  - threat‑model, mitigations map, NFR, соответствие ГОСТ/ЦБ РФ.

- **Опорные ops‑решения:**

  - design Fabric в K8s (кластера, HA, орг‑структура), выбор GitOps‑стека (ArgoCD vs GitLab Agent — уже рекомендован Argo, но это должны утверждать люди).

- **PROJECT/FRONTEND/WBS context:**

  - это ваш «architect brain export», туда агентов пускать только в read‑only.

### Что — «Leaves» (хорошие задачи для агентов)

5–10 примеров задач, которые можно выдавать агентам (с жёсткими ограничениями):

13c63**Обновить/сгенерировать API‑matrix report (NX‑01 support)**

   - Вход: OpenAPI/AsyncAPI из `packages/contracts`, текущие `artifacts/*‑report.md`.
   - Выход: обновлённый `artifacts/gateway-routing-report.md` и `issuance-endpoints-coverage-report.md` с пометкой дат.

23c63**Пройтись по Program.cs сервисов и проверить наличие health/metrics**

   - Автоматически добавить стандартный OTel/Prometheus wiring, если отсутствует, по шаблону из уже реализованных сервисов.

33c63**Написать unit‑тесты для простых DTO/Value‑Objects**

   - Расширить `domain.Tests` новыми тестами (Money, ScheduleItem, PayoutSchedule)3c63Сейчас часть уже есть — агент может дополнить edge‑кейсы.

43c63**Сгенерировать/обновить TS‑клиенты по OpenAPI**

   - На основе `packages/contracts/openapi-*.yaml` обновить `packages/sdks/ts`, поправить только сгенерённый слой.

53c63**Мелкие UI‑фичи в порталах**

   - Подключить новый endpoint в фронте через готовый TS SDK (например, payouts report в `portal-issuer`).

63c63**Backoffice UX‑улучшения**

   - Используя `apps/shared-ui`, добавить таблицы/фильтры/пагинацию для реестра пользователей, если API уже есть.

73c63**Helm/manifest tweaks**

   - Обновить значения ресурсов/labels/annotations в helm‑чартах по шаблону (например, добавить `prometheus.io/scrape`).

83c63**Runbook авто‑генерация**

   - На основе уже существующих docs/deploy и ops‑скриптов собрать упорядоченный checklist «как поднять dev‑контур локально/на VPS».

93c63**Playwright/E2E сценарии**

   - Расширять существующие journey‑tests для новых UI‑фич (например, добавить полный KYC‑workflow сценарий).

103c63**Миграции EF**

    - Сгенерировать EF‑миграции для новых полей и оформить SQL‑дифф в docs, но применять их должен человек.

### Задачи, которые лучше делать руками (или руками + агент‑ассистент)

3–5 задач, где агентам доверять опасно:

13c63**Изменение доменной модели и контрактов**

   - Любые изменения в `packages/domain` и `packages/contracts` (OpenAPI/AsyncAPI) — только вручную, с осознанным impact‑анализом3c63Агент может предложить diff, но не должен коммитить.

23c63**Security / compliance решения**

   - Настройка Fabric HA, выбор ArgoCD vs GitLab Agent, NetworkPolicy, секреты, криптография и т.п3c63— только руками, опираясь на audit и threat‑доки.

33c63**Регуляторные отчёты и audit‑логика**

   - Любая логика вокруг аудита, 57580/259‑ФЗ, 5625‑У — агенты могут помочь собрать информацию, но финальные формулировки и решения — только «живой мозг».

43c63**Сложные refactorings cross‑services**

   - Миграция схемы данных/топиков Kafka, изменение доменных инвариантов, переразбиение сервисов; агенты тут слишком легко ломают интеграции.

53c63**Продакшен‑релизы и срочный incident response**

   - Runbooks могут быть написаны агентом, но выполнять их (и особенно импровизировать по ним) должен человек.

---

## Итоговая таблица

| Area               | Issue or Question                                                               | Your recommendation                                                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Repo structure     | Смешение `docs/`, `audit/`, `ARCHIVE/`, `memory-bank`                           | Развести: `docs` = living spec, `audit-reports` = snapshots, `ARCHIVE` явно legacy, `memory-bank` вынести/игнорировать для агентов3c63                            |
| Packages/contracts | Много generated‑кода и дублирование моделей                                     | Выделить `generated/` для .NET/TS клиентов, формализовать «истину» в `packages/contracts` + `packages/domain`, запретить руками править generated3c63             |
| Infra/ops          | GitLab Runner/K8s/GitOps частично настроены, но не доведены до production‑ready | Завершить runner‑фикс, оформить GitOps flow в `ops/README` + `docs/ops`, закрепить ArgoCD/GitLab Agent как целевой стек3c63                                       |
| NX‑tasks           | Много задач, непонятно с чего начинать                                          | Сначала стабилизировать NX‑01/02/03 (спеки, gateway, issuance), затем NX‑04 (registry flow), потом NX‑05/06 (identity+CI), и в конце NX‑07/08 (backoffice UI)3c63 |
| Docs & context     | PROJECT/FRONTEND/WBS полезны, но мало связаны с повседневной работой            | Дочитать и обновить эти доки, добавить diagrams для ключевых потоков, в README указать, что они — главный вход для агентов и людей3c63                            |
| Agentification     | Непонятно, что безопасно отдавать агентам                                       | Считать trunk’ом домен/контракты/регуляторку/infra‑design, а leaves — тесты, UI‑мелочи, manifests tweaks, reports; агенты работают только на leaves под review3c63|

Если хочешь, следующим шагом могу разложить конкретный **2‑недельный спринт‑план** по дням/слотам с пометкой «это делаю я / это отдаю агенту».

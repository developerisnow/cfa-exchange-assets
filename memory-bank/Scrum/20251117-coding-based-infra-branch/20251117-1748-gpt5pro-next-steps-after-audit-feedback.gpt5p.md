# Prompt 1

You are Oracle, a focused one-shot problem solver. Emphasize direct answers, cite any files referenced, and clearly note when the search tool was used.  You are GPT‑5 Pro acting as a senior system/solution architect and codebase reviewer.  I have attached: - `c2p_ois-cfa.txt`: a ~4MB code2prompt snapshot of the `ois-cfa` repository (branch `infra.defis.deploy`), including structure and key files; - `20251116-1603-gpt5pro-audit-feedback-review.gpt5p.md`: your previous long-form audit & recommendations for this repo (call it V1‑audit); - `20251117-1537-eywa1-co-3dd7.session.md`: my detailed infra/devops session log from AVA1/eywa1 describing what I actually did with CFA1/UK1, Cloudflare, Postfix, Playwright, etc.; - `20251117-1713-feedback-to-co-3c63-from-eywa1-co-3dd7.md`: a short summary of what you (V1‑audit) did NOT know and what must be added as context;  - two architecture context files about Trees/Leaves/Agents (my target way of working through AI agents on top of this codebase).  High-level reality check (NEW facts you must incorporate): - Historically, the first demo environment was on CFA1/AVA1: docker-compose stack, Keycloak, portals, Postgres/Kafka/MinIO. - Because of access/infra issues, we moved the working demo to UK1 (public host) and finished wiring DNS/Cloudflare, TLS, Nginx reverse proxies, Postfix/OpenDKIM for Keycloak email flows, and Playwright E2E smokes. - The branch `infra.defis.deploy` now represents Aleksandr’s infra/observability/audit work (old `infra` branch) + my deploy/UK1‑oriented tweaks (docker-compose, gateway, portals, Keycloak/SMTP, test configs). - Your V1‑audit was structurally good, but it assumed a “theoretical infra” and did NOT know that a real, working UK1 demo already exists.  Your job now is to produce a V2‑audit & plan, building on V1 but corrected and updated with this real-world context.  What I need from you (V2‑audit): 1) Delta vs V1‑audit (top 5–10 corrections, each with: what V1 said / new reality / corrected recommendation). 2) Updated macro-architecture snapshot for `infra.defis.deploy` + UK1 (5–8 bullets, suitable for docs). 3) Refined 2–3 week roadmap based on `tasks/NX-*` and `docs/context/*`: ordered NX tasks, per-task Goal/Prereqs/DoD/Agent-friendly?, in a table. 4) Minimal 1–2 day repo-structure refactor plan (ARCHIVE/audit/docs/memory-bank/chaincode/apps/ops) to improve onboarding and agent work. 5) Agentification V2 (Trees/Leaves): 5–10 leaf-task patterns for agents, 3–5 trunk-task patterns for manual work, each with 1–2 sentence rationale.  Answer in Russian, senior-engineer tone, with B2-level English terms; structure output as TL;DR, sections 1–5, then a final compact table Area / Issue or Question / V2 recommendation.

# Output 1
TL;DR

* `infra.defis.deploy` уже не «план», а рабочая ветка: в неё вмерджены `infra`+`deploy`, UK1‑стенд живёт именно на ней, с Cloudflare, nginx, Postfix/OpenDKIM и Playwright e2e (4 спека).
* 2–3 недели: добиваем NX‑02/03/04 вокруг реального UK1 (gateway routing+health, issuance+registry happy‑path), поднимаем минимальные CI‑гейты и фиксируем UK1 как «reference env» в доках/скриптах.
* За 1–2 дня наводим порядок в структуре (`docs/*`, `ops/*`, `ARCHIVE`, `memory-bank`) и описываем Trees/Leaves‑паттерны: что можно отдавать агентам (lint, матрицы, e2e, runbooks), а что остаётся trunk‑работой (decision‑making, security, merge‑стратегии).

> Я прошёлся по V1‑аудиту, UK1‑runbook’ам, session‑логу, WBS/NX‑таскам и TLA‑файлам через внутренний поиск по загруженным файлам (аналог `file_search`), все выводы и ссылки ниже на это опираются.

---

## 1) Delta vs V1‑audit (коррекции 5–10 шт.)

### 1.1. Статус окружений: «теория» vs реальный UK1

* **Что говорил V1**
  «Bootstrap окружений (1–2 дня)»: сделать рабочий dev‑контур (docker‑compose на VPS/локально) + базовый k8s‑контур, починить Runner и только потом опираться на него. 

* **Новая реальность**
  UK1 уже развёрнут на `/opt/ois-cfa` с docker‑compose, Cloudflare DNS+TLS, nginx vhost, Keycloak public URL, pm2‑порталами и API gateway; чек‑лист в `docs/deploy/20251113-cloudflare-ingress.md` полностью пройден.

* **Исправленная рекомендация**
  Считать UK1 «reference dev/demo env» (не «будущим»), а CFA1 и k8s‑кластер — вспомогательными. Фокус не на bootstrap, а на формализации: привести UK1‑runbook’и к v1.0, добавить быстрый smoke‑скрипт (curl health + Playwright), зафиксировать, что все NX‑таски проверяются именно там.

---

### 1.2. Состояние NX‑01/02/03

* **V1**
  NX‑01/02/03 описаны как частично сделанные, но без привязки к реальному окружению; план: сначала добить NX‑01 (spec‑lint + матрицы), потом NX‑02/03.

* **Реальность**

  * NX‑01: уже есть API/Event‑матрица и spec‑lint артефакты (OpenAPI/AsyncAPI/JSON Schema вычищены, warnings сведены).
  * NX‑02: gateway маршруты/health частично проверены, но консистентность со спекой и health/metrics ещё не «замкнуты». 
  * NX‑03: есть issuance.Tests и TRX‑лог с падением из‑за конфигурационных проблем EF и mock‑ledger’а. 

* **Исправленная рекомендация**

  * NX‑01 перевести в «maintenance»: один Make‑таргет, который гоняет весь spec‑lint и обновляет матрицу.
  * Основной фокус 2–3 недель: довести NX‑02/03 до «зелёного happy‑path» именно на UK1, а не в «абстрактном dev».

---

### 1.3. E2E‑тесты: Playwright

* **V1**
  Упор на классические e2e/k6 из `ops/infra`/CI, Playwright как harness не фигурировал.

* **Реальность**
  Есть `tests/e2e-playwright` с 4 сценариями: issuer login, investor login, investor self‑registration (через mail.tm), backoffice admin login; всё привязано к доменам `*.cfa.llmneighbors.com` и локальному SMTP.

* **Исправленная рекомендация**
  Сделать Playwright основным e2e‑сигналом для демо‑стенда (обязательный smoke перед merge в main и перед «показом»). В CI этот job можно запускать только для `infra.defis.deploy`/`main`, чтобы не убить Runner.

---

### 1.4. SMTP / Keycloak‑email

* **V1**
  Email‑инфраструктура видится как «to do»: нужен verifyEmail / self‑registration, SMTP пока теоретический.

* **Реальность**
  На UK1 развёрнут Postfix+OpenDKIM, SPF/DKIM/DMARC настроены; Postfix слушает только `127.0.0.1` и `172.18.0.1`; внешний 25 закрыт; Keycloak realm `ois-dev` использует локальный relay, verifyEmail/self‑registration реально работают (через mail.tm).

* **Исправленная рекомендация**
  Фиксировать это как production‑grade baseline: задокументировать схему безопасности (нет внешнего 25, DKIM/DMARC ok) и добавить периодический SMTP‑smoke (одно письмо + проверка в mail.tm) в runbook и, опционально, в ночной job.

---

### 1.5. Статус ветки `infra.defis.deploy`

* **V1**
  Рекомендовал создать ветку `infra.defis.deploy` по схеме «база = infra, поверх deploy», с bucket‑мерджем services/packages/ops; это рассматривалось как план.

* **Реальность**
  Ветка уже создана, сводит `origin/infra` и `deploy`, конфликты в Program.cs/csproj решены с приоритетом infra‑реализаций и deploy‑runtime‑фич (динамический `MigrationsAssembly`, `MIGRATE_ON_STARTUP`). Коммит `a2db527` зафиксирован и используется как основа UK1.

* **Исправленная рекомендация**
  Относиться к `infra.defis.deploy` как к текущему «источнику правды» для backend’а. Следующий шаг — оформить MR в main с чётким DoD: dotnet tests, Playwright, базовые health‑checks и, по возможности, dry‑run CI в k8s.

---

### 1.6. GitLab Runner и CI

* **V1**
  Runner рассматривался как «полу‑настроенный блокер»: 403, неправильные токены/state file, нет устойчивого CI.

* **Реальность**

  * Конфигурационные проблемы Runner’а (state_file, writable volume, тип токена) уже разобраны и исправлены в `docs/ops/gitlab-runner-*.md`; остаётся операционная рутина — обновлять registration token и иногда форс‑перерегистрировать runner.
  * Runner сейчас не «дизайн‑баг», а обслуживаемая часть инфраструктуры.

* **Исправленная рекомендация**
  Сместить акцент с «чинить Runner» на «минимальный, но стабильный CI‑путь»: один pipeline для `infra.defis.deploy`/`main` с job’ами: `dotnet test`, `npm test` (unit), `playwright:smoke`, `spectral-lint`. Runner‑токен — просто check‑point в ops‑runbook.

---

### 1.7. k8s/Timeweb vs UK1/docker‑compose

* **V1**
  Делал упор на Timeweb‑кластер и GitOps как основной target, docker‑compose на VPS — как временный dev.

* **Реальность**

  * k8s‑кластер и GitLab Agent настроены, но в нём пока только тестовый nginx‑pod и runner; продуктовый стек живёт на UK1 (docker‑compose).
  * UK1‑runbook даёт воспроизводимую схему доступа по доменам `*.cfa.llmneighbors.com`. 

* **Исправленная рекомендация**
  На горизонте 2–3 недель не пытаться догнать k8s до UK1 по функционалу. Использовать k8s как будущий prod‑target и площадку для экспериментов с GitOps/runner’ом, но все NX‑таски и демо‑flows завязывать на UK1.

---

### 1.8. Repo‑структура и роль `memory-bank`

* **V1**
  Хотел более жёстко отделить `ARCHIVE`, `audit` и «боевые» доки, а `memory-bank` воспринимал как вторичный источник. 

* **Реальность**
  `memory-bank` уже содержит важные decision‑логи и отчёты (`20251114-discovery-infra-branch/*`, UK1‑deploy, SMTP‑lockdown), которые реально нужны для понимания ветки `infra.defis.deploy` и её истории.

* **Исправленная рекомендация**
  Не прятать `memory-bank`, а формализовать: в корне `docs/` сделать «шлюз» (`docs/README` с ссылками на ключевые memory‑записи как на источники) и явно пометить его как «source of truth for decisions». Структурный рефактор — в разделе 4.

---

## 2) Обновлённый macro‑architecture snapshot (`infra.defis.deploy` + UK1)

1. **Codebase layout (ветка `infra.defis.deploy`)**

   * Backend: `services/*` (issuance, registry, settlement, compliance, identity), `apps/api-gateway`, `packages/*` (domain, contracts, sdks), `chaincode/*` (Fabric), тесты (`tests/*` + `tests/e2e-playwright`).
   * Ops/Infra: `ops/infra/timeweb` (Terraform+K8s), `ops/infra/k8s/gitlab-runner`, `ops/gitops/*`, `docs/ops/*.md`.

2. **Runtime topology — UK1 (primary dev/demo)**

   * VPS `185.168.192.214`, папка `/opt/ois-cfa`. Docker‑compose поднимает Postgres, Kafka, MinIO, Keycloak, .NET‑сервисы и portaled Next.js‑приложения.
   * System nginx + Cloudflare: TLS‑offload, A‑записи `auth|issuer|investor|backoffice|api.cfa.llmneighbors.com` → UK1, wildcard Let’s Encrypt, режим `Full`.

3. **Identity & Access**

   * Keycloak realm `ois-dev`: клиенты `portal-issuer`, `portal-investor`, `backoffice` с OIDC, demo users (`issuer@test.com`, `investor@test.com`, `admin@test.com`) и ролями issuer/investor/backoffice. Bootstrap скрипт в `ops/infra/keycloak-bootstrap*.sh`/docs.

4. **Email / Notifications**

   * Локальный SMTP (Postfix + OpenDKIM) на UK1, слушает только localhost и docker‑bridge; домен `cfa.llmneighbors.com` с SPF/DKIM/DMARC, Keycloak verifyEmail/self‑registration используются в prod‑подобном режиме.

5. **Async & Observability**

   * Kafka topics и AsyncAPI‑контракты (например, `ois.issuance.published`, `ois.registry.transferred`, `ois.compliance.flagged`) синхронизированы с MassTransit‑конфигурацией в сервисах; OpenTelemetry, Prometheus‑метрики и health‑endpoints включены в Program.cs большинства сервисов.

6. **E2E Journeys**

   * Playwright‑пакет тестирует issuer/investor login, self‑registration и backoffice admin на доменах UK1, используя тот же SMTP и Keycloak, что и реальные пользователи.

7. **k8s / GitOps (secondary target)**

   * Timeweb‑кластер с namespace’ами `ois-cfa`, `gitlab-agent`, `gitlab-runner`, test‑nginx ingress, GitLab Agent, Runner; GitOps/CI описаны в `docs/ops/gitlab-*.md` и `docs/dlt/*` для Fabric. Сейчас это заготовка под будущий prod‑контур, а не основная демка.

8. **Docs as part of architecture**

   * `docs/context/*` (PROJECT/FRONTEND/WBS/RULES) и `docs/deploy/docker-compose-*` + `docs/deploy/20251113-cloudflare-ingress.md` являются «верхним слоем» над кодом, описывающим, что именно считается MVP‑готовым по порталам и API‑flows.

---

## 3) 2–3‑недельный roadmap по NX‑таскам

Ниже — порядок NX‑задач с учётом того, что UK1 уже живой. Нумерация — приоритет выполнения.

### Таблица NX‑тасок

| Order | NX‑task                                                  | Goal (кратко)                                                                                                                    | Prereqs                                                                                                 | DoD (Definition of Done)                                                                                                                                                                                                    | Agent‑friendly?                                                                                                                                                                 |
| ----- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | **NX‑01** Spec validation + API/Event Matrix             | Консолидировать OpenAPI/AsyncAPI/JSONSchema‑lint в один сценарий и обновить матрицу API↔events как «живой артефакт».             | UK1 не нужен; достаточно репо + dockerized lint‑tools.                                                  | `make spec-lint` проходит; матрица обновлена в `artifacts/*` и ссылается из `docs/context/WBS-OIS.md`; task‑файл NX‑01 отмечен как «Done/Next review date».                                                                 | **Да, 80%** — идеально для агента: линтеры, генерация markdown‑матрицы, минимальный ручной review.                                                                              |
| 2     | **NX‑02** API Gateway routing + health/metrics           | Убедиться, что YARP‑маршруты и health/metrics всех сервисов согласованы со спекой и живут на UK1.                                | NX‑01 (матрица endpoint’ов), живой UK1, базовый Playwright smoke.                                       | Для всех публичных маршрутов: есть запись в матрице; gateway route → конкретный сервис; `/health` и `/metrics` отдают ожидаемый формат; есть markdown‑таблица «Gateway routes vs Services» в `docs/ops/gateway-routing.md`. | **Частично, ~60%** — агенту отдаём сверку и обновление таблиц; финальное решение по спорным маршрутам и именованию — руками.                                                    |
| 3     | **NX‑03** Issuance endpoints alignment + tests           | Свести issuance API (publish/close, pricing) к спеке и добиться зелёных unit/integration тестов.                                 | NX‑01 (спека), базовый UK1 или локальный compose, рабочий миграционный флоу через `MIGRATE_ON_STARTUP`. | Все тесты из `tests/issuance.Tests` зелёные; EF‑конфиги без конфликтов (один провайдер); documented known mocks (ledger mock mode); в `tasks/NX-03-*.md` зафиксирован перечень покрытых endpoints + ссылки на TRX.          | **Да, но под присмотром (~70%)** — агент хорошо добивает тесты и конфиг, но финальный check EF‑конфигурации и бизнес‑допущений — руками.                                        |
| 4     | **NX‑04** Registry order flow (create→reserve→paid)      | Реализовать и протестировать core‑flow order→reserve→paid между portal‑investor, registry, settlement и ledger (mock или real).  | NX‑02 (gateway routing), NX‑03 (issuance готов), доступный UK1 или полноценный dev‑compose.             | E2E‑journey (через Playwright или API‑скрипт) от investor UI до ledger/dltTxHash; unit/integration tests на registry/settlement; события `ois.registry.transferred`/`ois.payout.executed` зафиксированы и проверены.        | **Смешанный** — агент пишет тесты и wiring; человек принимает решения по допущениям ledger/chaincode.                                                                           |
| 5     | **NX‑05** Identity/Keycloak baseline                     | Описать и зафиксировать базовый identity‑контур: Keycloak realm/clients/roles ↔ identity service ↔ NextAuth в порталах.          | Реально работающая конфигурация UK1 (уже есть), docs по Keycloak bootstrap/runbook.                     | `docs/ops/keycloak-baseline.md` (или раздел в `docs/deploy`) с: схемой realm, списком clients/roles, URL redirect’ов; identity‑service OpenAPI ≈ фактическим endpoint’ам; smoke‑тест: логин с каждой ролью через портал.    | **Да для документации/скриптов, нет для дизайна** — агент фиксирует текущее состояние и генерит smoke‑скрипты; решение о password‑policy, MFA, future ESIA‑интеграции — руками. |
| 6     | **NX‑06** CI quality gates (Spectral/AJV/tests/coverage) | Включить минимальные, но реальные quality‑гейты: spec‑lint, dotnet tests, npm tests, Playwright smoke, базовый coverage.         | Runner в состоянии «Online», NX‑01/03 уже структурируют тесты и spec‑lint.                              | `.gitlab-ci.yml` содержит stage `validate/test/e2e`; pipeline на `infra.defis.deploy`/`main` фейлится при падении spec‑lint или тестов; есть ссылки на отчёты в `docs/ops/gitlab-ci.md`.                                    | **Да, 80–90%** — типичная «агентская» работа (правка CI YAML, wiring jobs). Нужен только финальный human‑review.                                                                |
| 7     | **NX‑07** Backoffice KYC & User Registry UI              | Довести backoffice до MVP по KYC и user registry (5625‑У): approve/reject KYC, статусы инвесторов, базовый реестр пользователей. | NX‑02/03/04 (API готов), NX‑05 (Identity baseline), FRONTEND‑CONTEXT для требований.                    | Backoffice отображает список пользователей/инвесторов, KYC‑статус; действия пишут audit‑events; есть e2e‑сценарий KYC→approve/reject.                                                                                       | **Частично** — агенты могут дописать UI/сценарии, но бизнес‑логика соответствия 5625‑У и UX‑решения требуют manual‑контроля.                                                    |
| 8     | **NX‑08** Backoffice Audit Log UI                        | Поднять UI для audit‑логов (операции, KYC, изменения реквизитов) на основе уже имеющихся событий и компонентов.                  | Базовая событийная модель (AsyncAPI/audit), готовый компонент audit log в shared‑ui.                    | Backoffice показывает фильтруемый список событий с basic search/filters; есть e2e‑сценарий, который генерит несколько событий и проверяет отображение.                                                                      | **Да (~70%)** — UI и wiring может делать агент, при условии, что человек задаст фильтры/retention‑policy.                                                                       |

---

## 4) 1–2‑дневный план рефакторинга структуры репо

Цель — сделать структуру дружелюбной для онбординга и для Trees/Leaves‑агентов без массовых переносов кода.

### Шаги (практично, на 1–2 дня)

1. **Root‑README + «карта директорий»**

   * В корне `ois-cfa` обновить `README.md`: раздел «Directory map» с 1–2 строками на `apps/`, `services/`, `packages/`, `ops/`, `docs/`, `audit/`, `ARCHIVE/`, `memory-bank/`, `chaincode/`, с пометкой, какие каталоги являются «source of truth», а какие — архив/линейка решений.

2. **Упорядочить `docs/*` и `audit/*`**

   * В `docs/` ввести логическую подсетку:

     * `docs/context/*` — high‑level контекст и WBS (уже есть).
     * `docs/deploy/*` — runbooks по окружениям (CFA1, UK1, docker‑compose).
     * `docs/ops/*` — CI, runner, k8s, timeweb, GitOps.
     * `docs/dlt/*` — Fabric/chaincode.
   * В `audit/` добавить короткий `README` с описанием, что это «внутренний DevOps/обсервабилити audit pack», по которому backoffice/Audit‑UI будет ссылаться. 

3. **`ops/` как явный entrypoint для infra**

   * Добавить `ops/README.md`: где k8s, где timeweb, где UK1 (nginx, docker‑compose overrides), где скрипты (`ops/scripts/*`).
   * В `ops/infra/uk1` положить ссылку на `docs/deploy/20251113-cloudflare-ingress.md` и основные nginx/compose‑файлы, чтобы UK1‑картина видна из одного места.

4. **`apps/` и `services/` — минимальные README**

   * `apps/README.md`: перечислить `api-gateway`, `portal-issuer`, `portal-investor`, `backoffice` + как их запускать локально (dev) и на UK1 (docker).
   * `services/README.md`: перечислить core‑сервисы и указать, что все Program.cs уже с OTEL/health/Kafka/RateLimiting, плюс ссылка на AsyncAPI/контракты.

5. **`ARCHIVE` и `memory-bank` — ярлыки для новичков и агентов**

   * В `ARCHIVE/` завести `README` с правилами: сюда складывать устаревшие доки/промпты, но не активные runbook’и.
   * В `memory-bank/README` описать, что это «журнал сессий и решений», и дать 3–5 прямых ссылок на ключевые файлы (infra‑discovery, UK1‑deploy, SMTP lockdown, V1/V2‑аудиты), чтобы агент мог стартовать оттуда.

6. **Лёгкий cleanup для agent‑friendly работы**

   * Явно отметить в `docs/context/RULES-SUMMARY.md`, какие каталоги агенту разрешено изменять (например, `docs/deploy/*`, `docs/ops/*`, `tests/*`, `apps/*`), а какие требуют ручного review/approval (`audit/*`, `docs/legal/*`, `docs/security/*`).

Реально это можно сделать в одном MR за 1–2 дня, без опасных перемещений кода.

---

## 5) Agentification V2 (Trees/Leaves)

Ориентируюсь на твою TLA‑архитектуру: маленькие leaf‑таски с жёсткими рамками и несколько trunk‑тасков, которые человек держит в голове (и, максимум, использует агентов как советчиков).

### 5.1. Leaf‑patterns (агенты)

5–10 типовых шаблонов, которые можно смело автоматизировать.

1. **Spec‑lint & Matrix Update (NX‑01)**
   Агент запускает Spectral/AJV/AsyncAPI‑lint, обновляет матрицу API/Event‑соответствий и пишет краткий report в `artifacts/NX-01-report.md`. Почему: чисто механика правил+CLI, мало бизнес‑логики.

2. **Gateway Route Consistency Check (часть NX‑02)**
   Листает `apps/api-gateway` конфиги и OpenAPI, собирает таблицу «path → service → method → auth» и подсвечивает расхождения. Человек только решает, что исправлять.

3. **Health/metrics endpoint templating**
   Для сервисов без `MapHealthChecks`/`MapPrometheusScrapingEndpoint` агент добавляет стандартный шаблон и простые unit‑тесты (Smoke). Это повторяемый паттерн по всем `Program.cs`.

4. **Issuance/Registry test‑extensions (NX‑03/04)**
   Агент расширяет существующие xUnit‑тесты (новые кейсы, edge‑cases) и обновляет TRX‑описание, не меняя бизнес‑правила, только явно документируя допущения.

5. **Playwright scenario scaffolding**
   На основе текущих e2e‑спеков агент генерирует новые сценарии (например, KYC approve/reject, audit log filter), придерживаясь существующего стиля и хелперов. Человек проверяет только смысл шагов и доменную корректность.

6. **Runbook checklists & command blocks**
   В `docs/deploy` и `docs/ops` агент может дописывать/уточнять чек‑листы, команды и verified‑output блоки (пример: GitLab Runner, Cloudflare, Fabric troubleshooting), не принимая архитектурных решений.

7. **Keycloak bootstrap scripts во вторую итерацию**
   Агент может синхронизировать существующие ручные инструкции по Keycloak с bash‑скриптами/`kcadm`‑скриптами, не меняя структуру realm/roles, а только делая provisioning повторяемым.

8. **CI job wiring (NX‑06)**
   Добавление/правка job’ов в `.gitlab-ci.yml` (подключить `make spec-lint`, `dotnet test`, `npm test`, `playwright:smoke`) и написание `Makefile`‑таргетов — классический leaf‑паттерн.

9. **Docs cross‑linking и TOC‑обновления**
   Агент может поднимать качество документации: добавлять содержимое, ссылки между `docs/context`, `docs/deploy`, `docs/ops`, не меняя юридический смысл legal/security‑доков.

10. **Hyperledger Fabric troubleshooting snippets**
    По `docs/dlt/*` агент может добавлять готовые troubleshooting‑шаги, примеры curl/CLI, не трогая дизайн сети/HSM.

---

### 5.2. Trunk‑patterns (ручная работа + оркестрация)

3–5 типов задач, которые должны оставаться под контролем архитектора/tech‑lead.

1. **Env‑strategy & migration plan (UK1 ↔ k8s/Timeweb)**
   Решение, когда и как мигрировать от docker‑compose на UK1 к k8s GitOps (и надо ли вообще), требует понимания SLA, бюджета и рисков runner/k8s. Агент может собрать варианты, но final‑decision и phased‑plan — trunk.

2. **Security & Compliance boundary (259‑ФЗ, 746‑П, 5625‑У)**
   Маппинг требований ЦБ на конкретные сервисы, роли, реестр пользователей и DLT — доменная задача; агентов можно использовать для проверки чек‑листов, но не для выбора control‑set’ов и рисковых trade‑off’ов.

3. **Merge‑стратегия и эволюция `infra.defis.deploy`**
   Выбор стратегии слияния веток, принятие решения о моменте MR в main, управлении fallback’ом `deploy`/старых конфигов и compat‑рисках — это человеческая ответственность. Агент может подсветить diff’ы и bucket’ы, но не решать, что выкинуть.

4. **DLT & ledger‑design (Fabric topology, chaincode responsibilities)**
   Решения по архитектуре Fabric (кол‑во orderer/peer, org layout, chaincode boundaries, security HSM) сильно завязаны на нефункциональные требования и регуляторку; агентов лучше использовать как «research+draft», а не как авторов конечной схемы.

5. **Backoffice domain logic (KYC, risk, audit)**
   Тонкие места UI/flows backoffice (какие статусы показывать, как логи агрегируются, что видит оператор) завязаны на людям/процессах; агент может предложить UI и запросы, но UX+compliance‑решения остаются trunk‑функцией.

---

## Итоговая компактная таблица (V2‑рекомендации)

| Area            | Issue / Question                                                                              | V2‑рекомендация                                                                                                                                                                            |
| --------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Environments    | V1 считал окружения «теоретическими»; UK1 уже работает с Cloudflare/nginx/Postfix/Playwright. | Зафиксировать UK1 как reference dev/demo env, обновить runbook до v1.0 и использовать его как базу для всех NX‑тасков и демо.                                                              |
| Branch strategy | `infra.defis.deploy` в V1 был лишь рекомендован; сейчас он уже собран и используется.         | Считать `infra.defis.deploy` canonical‑веткой, готовить MR в main после закрепления NX‑02/03 и минимальных CI‑гейтов.                                                                      |
| NX‑roadmap      | V1 ставил «bootstrap окружений» первым шагом, NX‑задачи — вторым.                             | Перестроить план: NX‑01 в режим maintenance, фокус 2–3 недель на NX‑02/03/04 + NX‑05/06 (identity+CI), всё через UK1.                                                                      |
| CI/CD & Runner  | Ранее Runner рассматривался как «блокер» из‑за 403 и неправильного state.                     | Признать, что конфиг Runner’а уже исправлен; строить вокруг него минимальный pipeline (lint+tests+e2e), а работу с токенами держать в ops‑runbook’ах.                                      |
| SMTP / Identity | Email‑поток и Keycloak воспринимались как незавершённые.                                      | Зафиксировать существующую схему Postfix+OpenDKIM+Keycloak как baseline; оформить NX‑05 поверх текущей реализации, не изобретая заново.                                                    |
| Repo structure  | Много «слоёв» (`docs`, `audit`, `ARCHIVE`, `memory-bank`), непонятно новичку и агенту.        | За 1–2 дня добавить README‑карты для корня, `docs/`, `ops/`, `apps/`, `services/`, и формализовать роль `memory-bank` как журнала решений.                                                 |
| Tests & E2E     | Playwright не был в фокусе V1, упор делался на «абстрактные e2e».                             | Сделать Playwright основным smoke‑сигналом для UK1, интегрировать его в NX‑03/04 и CI‑pipeline.                                                                                            |
| Agent usage     | V1 описал Trees/Leaves достаточно общо, без учёта UK1/NX контекста.                           | Использовать описанные leaf‑паттерны (lint, матрицы, e2e, runbooks, CI) и trunk‑паттерны (env‑strategy, merge, security, DLT, backoffice‑домен) как явные границы для агентов в этом репо. |

Если хочешь, следующим шагом можно сделать очень узкий план: «какой именно NX‑task и какой leaf‑паттерн отдаём первому агенту завтра» — но это уже поверх этой V2‑картины.

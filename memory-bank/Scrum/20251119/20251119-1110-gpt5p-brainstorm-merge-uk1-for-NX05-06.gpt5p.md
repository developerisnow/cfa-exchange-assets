# Prompt

# Output

## 1) TL;DR

* NX‑05: берём уже описанные в OpenAPI отчётные эндпоинты (`/v1/reports/issuances`, `/v1/reports/issuer/payouts` через gateway → settlement), подключаем их к `portal-issuer` для `/dashboard` и `/reports`, без новых контрактов; расхождения фиксируем как SPEC DIFF, но не ломаем uk1.
* NX‑06: спецификация payout schedule = SPEC DIFF по NX‑06: `POST/GET/PATCH/DELETE /v1/issuances/{id}/payouts/schedule` + `PayoutScheduleItem` (id/date/amount/status), бэкенд работает поверх существующего `Issuance.scheduleJson`, UI сначала read‑only на `/issuances/[id]`.
* Infra: uk1 — канонический docker‑compose стенд с Cloudflare/Nginx/Keycloak/Postfix, его трогаем минимально (build → up → `make check-health` + e2e smoke). Новый хост (cfa1/us1/vps1/germ1) — чистый runbook: OS+docker, repo, compose‑стек, Keycloak realm, dev frontends 3001/2/3, SSH‑туннели, smoke по `/health` и basic UI.
* Критические риски: (1) тест `Publish_NonExistent_Should_Return_404` до сих пор даёт 500, значит на стендах может быть старый образ issuance; (2) в AsyncAPI есть топики без продьюсеров (`ois.payout.scheduled`, `ois.transfer.completed` и др.); (3) расхождения OpenAPI↔gateway по путям `/issuances`/`/v1/issuances`; (4) часть health/metrics/SMTP/Keycloak ещё не доведена до «reproducible».
* Для NX‑05/NX‑06 жёстко опираемся на существующие домены Issuance/Registry/Settlement и отчётные схемы (`IssuerIssuancesReportResponse`, `IssuerPayoutsReportResponse`, `PayoutsReportResponse`), новые контракты — только там, где NX‑06 прямым текстом требует SPEC DIFF.

---

## 2) Steps

### 2.1 NX‑05 — Issuer Dashboard & Reports

#### 2.1.1 Почему (Why)

* Сейчас `/dashboard` и `/reports` у эмитента почти пустые/заглушки, при этом в спеках есть отчётные эндпойнты и AsyncAPI события. Бизнесу нечем управлять выпусками и выплатами, нет даже базовой видимости KPI.
* Мандат NX‑05: сделать эти страницы полезными, но не изобретая отдельный reporting‑сервис — использовать уже описанные в OpenAPI отчётные эндпойнты и данные settlement/registry.

#### 2.1.2 Что (What)

**Ключевые контракты:**

* **Reports API через gateway → settlement**

  * `/v1/reports/issuances` → `IssuerIssuancesReportResponse` (агрегаты по выпускам эмитента).
  * `/v1/reports/issuer/payouts` → `IssuerPayoutsReportResponse` (агрегаты по выплатам эмитента с `granularity` day/week/month/quarter).
  * `/v1/reports/payouts` → `PayoutsReportResponse` (общий payout‑репорт, пригоден для будущих backoffice/регуляторных отчётов, но для NX‑05 не обязателен).
  * Все `/v1/reports/**` так и так уже маршрутизируются через gateway: маршрут `/v1/reports/{**catch-all}` → cluster `settlement`. 

* **Issuance API через gateway → issuance**

  * `/issuances` (gateway) → `/v1/issuances` (service) POST.
  * `/issuances/{id}` (gateway) → `/v1/issuances/{id}` (service) GET.
  * Дополнительно у Issuance есть `scheduleJson` в `CreateIssuanceRequest`/`IssuanceResponse` — пригодится позже для NX‑06. 

* **AsyncAPI события (используем только косвенно)**

  * `ois.issuance.published`, `ois.issuance.closed` — уже продьюсятся Issuance. 
  * `ois.payout.executed` — продьюсится Settlement, и по нему можно строить отчётность. 
  * На уровне NX‑05 они остаются backend‑деталью, UI работает по REST репортам.

**Фичи NX‑05:**

1. **Dashboard `/dashboard`**

   * Плитки с агрегатами:

     * `activeIssuancesCount`, `closedIssuancesCount`.
     * `totalNominalAmount` по активным выпускам.
     * При наличии данных — `totalInvestors`.
   * Source of truth: `IssuerIssuancesReportResponse.summary`. 

2. **Reports `/reports`**

   * Вкладка **Issuances**: табличный отчёт по выпускам эмитента (кол-во, объём, статусы, даты выпуска/погашения).

     * Source: `IssuerIssuancesReportResponse.items[]`.
   * Вкладка **Payouts**: график/таблица «Payouts Over Time» (как уже заложено в e2e тесте) с granularities.

     * Source: `IssuerPayoutsReportResponse.items[]` (помесячные суммы, количество выплат, инвесторов). 
   * Export CSV/XLSX поверх тех же DTO (никакого отдельного отчётного эндпойнта).

3. **Тестовый smoke‑флоу Issuer**

   * Keycloak login → `/dashboard` → `/reports` → переключение табов → проверка визуализации и экспорта.
   * Отражается в Playwright spec, который уже сейчас маршрутизует `**/v1/reports/issuances**` и `**/v1/reports/payouts**` (тестовые стабы, которые нужно перевести на реальные ответы / или оставить только как fallback).

#### 2.1.3 Как (How)

##### Backend

1. **Проверить реализацию settlement‑отчётов**

   * Проверить в `services/settlement/*` наличие маршрутов, соответствующих `/v1/reports/issuances` и `/v1/reports/issuer/payouts` из OpenAPI: либо минимальные handlers, либо TODO.
   * Если код отсутствует или не завершён:

     * Имплементировать end‑to‑end:

       * `GET /v1/reports/issuances` — агрегаты по выпускам эмитента на основе таблиц Issuance/Registry (join по issuerId).
       * `GET /v1/reports/issuer/payouts` — агрегация из payout‑таблиц settlement (по issuerId + период + granularitу).
     * DTO строго по OpenAPI схемам `IssuerIssuancesReportResponse` и `IssuerPayoutsReportResponse`. (SPEC DIFF не нужен, пока держимся ровно схем). 

2. **Gateway**

   * Убедиться, что маршруты `/v1/reports/{**catch-all}` реально заведены в `apps/api-gateway/appsettings.json` и проверены NX‑02 (`gateway-routing-report.md` уже показывает `Status = ✅`). 
   * SPEC DIFF по NX‑02: OpenAPI‑gateway использует `/issuances` без `/v1`, YARP — `/v1/issuances`. Для NX‑05 это не блочит, но надо явно отметить как **уже существующий SPEC DIFF**, не плодя новый. 

3. **Проверка на uk1**

   * После build сервисов (`docker compose ... build identity-service issuance-service registry-service settlement-service compliance-service bank-nominal api-gateway`) поднять стек и прогнать `make check-health`.
   * Отдельно проверить:

     * `curl -sf http://localhost:5000/health`
     * `curl -sf "http://localhost:5000/v1/reports/issuances?issuerId=...&from=2025-01-01&to=2025-12-31"`
     * `curl -sf "http://localhost:5000/v1/reports/issuer/payouts?issuerId=...&from=...&to=...&granularity=month"`

##### Frontend (portal‑issuer)

1. **SDK и data‑layer**

   * Проверить наличие TS SDK по `openapi-gateway.yaml` в `packages/sdks/ts`. Если SDK устарел → перегенерировать по текущей спеки (точную команду лучше взять из `package.json` SDK, **ASSUMPTION**: есть что‑то вроде `npm run generate:gateway`).
   * В `apps/portal-issuer` завести модуль, условно `src/services/reports.ts` (имя для примера), который инкапсулирует вызовы:

     * `getIssuerIssuancesReport({ issuerId, from, to })` → `/v1/reports/issuances`.
     * `getIssuerPayoutsReport({ issuerId, from, to, granularity })` → `/v1/reports/issuer/payouts`.

2. **`/dashboard`**

   * В `apps/portal-issuer/app/dashboard/page.tsx` (или аналогичном route) заменить моковые данные на вызов `getIssuerIssuancesReport` с дефолтным диапазоном (например, `last 12 months`). 
   * Маппинг:

     * `summary.totalIssuances` → «Total issuances».
     * `summary.activeIssuances`/`closedIssuances` (если есть в контракте; если нет — считаем по items.status, это **не SPEC DIFF**, а просто расчёт на фронте).
     * `summary.totalAmount` → «Total nominal».
   * UI должен явно показывать «No data» в случае пустого отчёта, чтобы не маскировать проблемы на backend.

3. **`/reports`**

   * Структура страниц (частично уже есть в коде и e2e):

     * Header `Reports`.
     * Tabs: `Issuances` / `Payouts`.
   * Вкладка Issuances:

     * Таблица `items[]` из `IssuerIssuancesReportResponse` + фильтры по дате/статусу.
     * Кнопки `Export CSV/XLSX` делают клиентский экспорт текущего набора.
   * Вкладка Payouts:

     * Линейный/бар‑граф `items[].period` vs `items[].totalAmount`.
     * Внизу таблица с теми же данными.
     * На старте можно использовать тот же fake‑dataset, что в Playwright, но **целевой статус** — реальные данные с бэкенда (стабы только как fallback в тестах). 

4. **Тесты**

   * **Unit**:

     * Тесты маппинга DTO → view‑модели (`reports.mapper.test.ts`, `dashboard.mapper.test.ts`).
   * **Integration** (Next.js + SDK):

     * Тест на то, что data‑сервис вызывает корректные эндпойнты с нужными query‑параметрами.
   * **E2E (Playwright)**:

     * Дообновить существующий e2e сценарий для `/reports` так, чтобы:

       * В режиме CI он может либо работать на живом backend, либо подменять ответы, но **endpoints** должны соответствовать OpenAPI (`/v1/reports/issuances`, `/v1/reports/payouts`/`/v1/reports/issuer/payouts`).
     * Добавить smoke: issuer login → `/dashboard` камень → `/reports` → проверка базовых метрик.

#### 2.1.4 Результат (Done)

* `/dashboard` и `/reports` работают на реальных backend‑данных через gateway.
* В `artifacts/issuer-dashboard-and-reports.md` зафиксированы:

  * Список использованных эндпойнтов с примерами ответов.
  * Скриншоты или описания UI.
  * Ссылка на e2e прогон. 
* SPEC DIFF’ы только документальные (gateway `/issuances` vs `/v1/issuances` и т.п.), новых эндпойнтов для NX‑05 не добавляем.

---

### 2.2 NX‑06 — Issuer Payout Schedule Spec & UI

#### 2.2.1 Почему (Why)

* В контексте явно написано: **«Нет управления расписанием выплат (payout schedule) — требует SPEC DIFF в OpenAPI»** и это MVP‑критичный gap для Portal Issuer.
* Существуют payout‑события (`ois.payout.scheduled`, `ois.payout.executed`), но только `executed` реально продьюсится, `scheduled` декларативен.
* Issuance уже содержит `scheduleJson`, но нет ни явных REST‑эндпойнтов, ни UI, чтобы этим управлять/хотя бы смотреть.

#### 2.2.2 Что (What)

**Текущее состояние:**

* REST:

  * Нет эндпойнтов вида `/v1/issuances/{id}/payouts/schedule` в OpenAPI‑issuance/gateway.
  * Отчётные `/v1/reports/issuer/payouts` и `/v1/investors/{id}/payouts` дают историю фактических выплат, но не план.
* Events:

  * `PayoutScheduledPayload` и `PayoutExecutedPayload` уже описаны в AsyncAPI.
  * `ois.payout.scheduled` обозначен как **SPEC DIFF: есть в AsyncAPI, нет продьюсера**. 
* Domain:

  * Issuance DTO содержит `scheduleJson` (Dictionary) — фактическое хранилище сырого расписания. 

**Не хватает:**

1. CRUD по расписанию выплат на уровне OpenAPI (NX‑06 прямо диктует набор эндпойнтов).
2. Привязки CRUD‑действий к `ois.payout.scheduled` (producer).
3. Read‑only UI в Issuer portal, чтобы эмитент хотя бы видел будущие выплаты.

#### 2.2.3 SPEC DIFF (минимальный, но чёткий)

> Всё ниже — SPEC DIFF, как и требует NX‑06 (отдельный YAML‑патч в `tasks/NX-06-payout-schedule-SPEC-DIFF.md`). 

**OpenAPI (issuance + gateway)**

Добавить в `openapi-issuance.yaml` и `openapi-gateway.yaml`:

* `POST /v1/issuances/{id}/payouts/schedule`

  * Назначение: создать/заменить расписание выплат по выпуску.
  * Запрос:

    * Path param `id` (uuid).
    * Body:

      * `{ items: PayoutScheduleItem[] }`.
  * Ответ 200/201: актуальная версия расписания.
* `GET /v1/issuances/{id}/payouts/schedule`

  * Возвращает `{ items: PayoutScheduleItem[], lastUpdatedAt, currency? }`.
* `PATCH /v1/issuances/{id}/payouts/schedule/{itemId}`

  * Частичное изменение одного элемента (например, перенос даты либо статус).
* `DELETE /v1/issuances/{id}/payouts/schedule/{itemId}`

  * Логическая отмена payout‑слота (status → `cancelled` / `skipped`).

**Schema `PayoutScheduleItem` (OpenAPI + JSON Schema)**

* Поля (минимум):

  * `id: uuid`
  * `date: string (date)`
  * `amount: number` (тот же формат, что и в Issuance nominal/totalAmount)
  * `status: string` — enum: `planned | confirmed | executed | cancelled`.
* Можно разместить рядом с уже существующими payout‑схемами (`Payout`, `PayoutBatch`, `PayoutsReportResponse`), чтобы не ломать структуру.

**Gateway**

* Дополнительных YARP‑маршрутов не требуется:

  * уже есть `/issuances/{**catch-all}` → `/v1/issuances/{**catch-all}` → Issuance service.

**AsyncAPI**

* Уточнить и задокументировать использование `ois.payout.scheduled`:

  * Producer: Issuance service при создании/изменении расписания.
  * Payload: существующий `PayoutScheduledPayload`, дополнить при необходимости ссылкой на `PayoutScheduleItem` (если текущая схема это не делает — добавить как SPEC DIFF в AsyncAPI).

#### 2.2.4 Как (How)

##### Backend

1. **Issuance service: реализация endpoint’ов**

   * В `services/issuance/Program.cs` повесить новые маршруты:

     * `api.MapPost("/v1/issuances/{id:guid}/payouts/schedule", ...)`.
     * `api.MapGet("/v1/issuances/{id:guid}/payouts/schedule", ...)`.
     * и т.д. — по схеме SPEC DIFF.
   * В сервисном слое:

     * `IssuanceService` (или новый `PayoutScheduleService`) реализует чтение/запись `scheduleJson` у Issuance.
     * `scheduleJson` хранит массив `PayoutScheduleItem` в JSON, полностью совместимый со схемой. 

2. **Producer для `ois.payout.scheduled`**

   * После успешного создания/обновления расписания:

     * Собрать `PayoutScheduled` DTO, заполнить `batchId`/`issuanceId`/`scheduledFor`/`totalAmount` и т.п. по текущей схеме. 
     * Отправить через MassTransit Kafka producer из Issuance, аналогично тому, как уже делается для `ois.issuance.published`.

3. **Settlement/Registry (минимум)**

   * На уровне NX‑06 достаточно, чтобы settlement уже умел обрабатывать `PayoutExecuted` (есть сейчас) и не ломался от появления новых `PayoutScheduled`.
   * Дальнейший функционал (автоматический запуск payoutов по расписанию) можно вынести в отдельный NX, сейчас — только spec+UI.

##### Frontend (portal‑issuer)

1. **Read‑only UI в `/issuances/[id]`**

   * На странице деталей выпуска, описанной в FRONTEND‑контексте, добавить вкладку/раздел **Payout schedule**.
   * Загрузка данных:

     * Если SPEC DIFF уже реализован: дергать `GET /v1/issuances/{id}/payouts/schedule`.
     * Пока нет — fallback: использовать поле `scheduleJson` из `IssuanceResponse` и маппить его на `PayoutScheduleItem[]` (**ASSUMPTION**: форма JSON совместима или легко маппится).
   * Отображение: таблица (date, amount, status) + подсуммы.

2. **Валидация и UX**

   * До реализации редактирования держим UI read‑only, но сразу закладываем структуру компонента так, чтобы позже можно было добавить:

     * Inline‑редактирование дат/сумм.
     * Кнопку «Generate schedule» (равномерный график по maturityDate).
   * Явно показываем статус: если расписания нет → «Payout schedule not defined (see NX‑06 SPEC DIFF)».

3. **Тесты**

   * Unit:

     * Маппинг scheduleJson/REST → таблица.
   * Integration:

     * Тест `GET /v1/issuances/{id}/payouts/schedule` (через SDK) и корректный рендер.
   * E2E:

     * Расширить существующий issuer journey: после создания выпуска зайти в детали и убедиться, что вкладка Payout schedule не падает (даже если список пуст).

#### 2.2.5 Результат (Done)

* SPEC DIFF по payout schedule формализован (YAML‑патч + обновлённый AsyncAPI) и согласован.
* В Issuer portal страница `/issuances/[id]` показывает расписание выплат в read‑only, минимум на основе scheduleJson.
* Producer `ois.payout.scheduled` реализован и документирован в `registry-flow-report`/новом артефакте по payouts.

---

### 2.3 Infra runbooks — uk1 vs cfa1/новые хосты

#### 2.3.1 Почему (Why)

* uk1 — единственная реально рабочая среда с Cloudflare, Nginx, Keycloak, Postfix, e2e‑smoke; её ломать опасно.
* cfa1 использовалась исторически, частично сломана; задача — иметь воспроизводимый runbook, который можно применить к cfa1/us1/vps1/germ1 без ручной магии.

#### 2.3.2 Архитектура деплоя (high‑level)

* Компоненты:

  * API Gateway (`apps/api-gateway`) → .NET 9, YARP, health `/health`. 
  * Backend‑сервисы: Issuance, Registry, Settlement, Compliance, Identity (все с `/health`, часть с `/metrics`).
  * Infra: Postgres, Kafka/Zookeeper, Keycloak (+ keycloak‑proxy), Prometheus/Grafana/Loki/OTel collector, Bank nominal mock, ESIA adapter и т.д.
  * SMTP: Postfix + OpenDKIM на хосте, Keycloak использует SMTP для verifyEmail/forgot password.
  * Frontends: `portal-issuer`, `portal-investor`, `backoffice` (Next.js, порты 3001/2/3).
  * Внешняя обвязка uk1: Cloudflare DNS + wildcard TLS, Nginx vhost для `auth|issuer|investor|backoffice|api.cfa.llmneighbors.com`.

#### 2.3.3 Runbook: uk1 — current & safe

**Цель:** поддерживать и перезапускать стенд, не меняя архитектуру, домены, TLS и SMTP.

1. **Проверить состояние Docker‑стека**

   * `ssh -p 51821 root@uk1`
   * `cd /opt/ois-cfa`
   * `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` — убедиться, что Postgres, Kafka, Keycloak уже живы.

2. **Поднять/пересобрать keycloak+proxy (если нужно)**

   * `docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.health.yml -f docker-compose.keycloak-proxy.yml up -d keycloak keycloak-proxy` 
   * Проверка:

     * `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/health/ready` → `200`. 

3. **Сервисы .NET и gateway**

   * Build (при изменениях кода):

     * `DOCKER_BUILDKIT=1 docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.health.yml -f docker-compose.keycloak-proxy.yml -f docker-compose.services.yml build identity-service issuance-service registry-service settlement-service compliance-service bank-nominal api-gateway` 
   * Run:

     * `docker compose ... up -d identity-service issuance-service registry-service settlement-service compliance-service bank-nominal api-gateway`

4. **Health/metrics smoke**

   * `make check-health` (из корня репо). 
   * Точечные проверки:

     * `curl -sf http://localhost:5000/health && echo "Gateway OK"`
     * `curl -sf http://localhost:5002/metrics | head -30` (пример — Issuance/Registry/Settlement).

5. **SMTP/Keycloak**

   * Убедиться, что Postfix слушает только локальные адреса (план: изменить `inet_interfaces` с `all` → `127.0.0.1,172.17.0.1,172.18.0.1`, но **это change с риском**, сейчас стенд работает).
   * Проверить, что Keycloak отправляет письма (verifyEmail/forgot password) — через Playwright self‑registration сценарий.

6. **E2E smoke**

   * `cd tests/e2e-playwright && npm test` — issuer/investor/backoffice journeys.
   * При падении — фиксировать в отдельном `memory-bank/Scrum/...` лог‑файле, не трогать nginx/Cloudflare без отдельного плана.

**Что НЕ трогать на uk1 без отдельного RFC:**

* Конфигурацию Cloudflare DNS/TLS и Nginx vhosts. 
* Базовую структуру docker‑compose файлов.
* SMTP порты/DMARC/SPF, кроме аккуратного ограничения `inet_interfaces`.

#### 2.3.4 Runbook: новый хост (cfa1/us1/vps1/germ1)

**Цель:** запустить минимальный dev‑/staging‑стенд, совместимый с uk1 runbooks, но без обязательного Cloudflare/Nginx (можно добавить позже).

1. **Base setup**

   * Установить: `docker`, docker compose plugin, `git`, `curl`, `nvm`/Node 20, (опционально) `make`.
   * Создать пользователя для деплоя (`ois`), выдать ему доступ к docker.

2. **Клонировать репо и ветку**

   * `git clone <monorepo>`
   * `cd ois-cfa` (submodule) → checkout `infra.defis.deploy`.
   * Заполнить `.env` / compose env‑файлы (DB passwords и т.п.) — **только плейсхолдеры**, реальные секреты — через vault/CI.

3. **База + Kafka + Keycloak**

   * `docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.health.yml up -d postgres ois-zookeeper ois-kafka`
   * `docker compose ... up -d keycloak` (можно без keycloak‑proxy на первом шаге).
   * Проверка: `curl http://localhost:8080/health/ready` → `200`.
   * Применить `docs/deploy/KEYCLOAK-SETUP.md`: создать realm `ois-dev`, клиенты для issuer/investor/backoffice.

4. **Backend‑сервисы + gateway**

   * Build + up как на uk1 (но без keycloak‑proxy и bank‑nominal при необходимости).
   * Проверка: `curl http://localhost:5000/health`.

5. **Frontends (dev)**

   * На хосте:

     * Установить Node 20 через nvm.
     * В `apps/portal-issuer`, `apps/portal-investor`, `apps/backoffice`: `npm install`, `npm run dev -- --port 3001/3002/3003`.
   * Keycloak redirect URIs должны указывать на `http://<host>:3001` и т.п. (или на туннелированные порты).

6. **Удалённый доступ / туннели**

   * С `eywa1` сделать туннели на cfa1 (примеры уже есть в DoD):

     * `ssh -N -L 15500:localhost:5000 -L 15808:localhost:8080 -L 15301:localhost:3001 -L 15302:localhost:3002 -L 15303:localhost:3003 user@cfa1`
   * После этого на локальной машине:

     * `curl http://localhost:15500/health`
     * Открыть порталы/Keycloak в браузере.

7. **Smoke‑проверки**

   * `make check-health` на новом хосте. 
   * Хотя бы один Playwright smoke (можно на `eywa1`, используя туннели).
   * Записать все команды/выводы в новый memory‑bank лог (как уже делалось для uk1/cfa1).

**Рискованные шаги:**

* DB migrations: использовать `MIGRATE_ON_STARTUP=true` только для первого деплоя; потом выключать.
* SMTP: на новых хостах лучше изолировать Postfix сразу (слушать только localhost/bridge‑сеть).

---

### 2.4 Risk register / Open issues (NX‑05/NX‑06 + infra)

Я кратко, но по делу.

1. **Issuance API: 404 vs 500 для Publish_NonExistent**

   * **Что:** тест `Publish_NonExistent_Should_Return_404` ожидает 404, фактически 500.
   * **Почему важно:** некорректный status code ломает idempotent‑клиентов и e2e‑тесты, особенно при работе портала/клиентов поверх ошибок.
   * **Минимальное изменение:** убедиться, что на всех стендах собрана версия с проверкой существования Issuance перед `PublishAsync/CloseAsync` (логика уже внедрена в Program.cs по NX‑03). Возможно, проблема только в старом образе на uk1.
   * **Где:** `services/issuance/Program.cs` + деплой образа `issuance-service`.
   * **Когда:** до/вместе с NX‑05 (иначе репорты/дашборд могут упираться в 500 при edge‑cases).

2. **AsyncAPI: события без продьюсеров (`ois.payout.scheduled`, `ois.transfer.completed`, `ois.order.placed`, `ois.order.confirmed`)**

   * **Что:** объявлены в AsyncAPI, не имеют продьюсеров в коде (SPEC DIFF уже зафиксирован).
   * **Почему важно:**

     * Для NX‑06 `ois.payout.scheduled` — ключевой для downstream сервисов, аналитики и аудита.
     * События order.* влияют на сквозной реестр/settlement flow.
   * **Минимальное изменение:**

     * Для NX‑06: реализовать producer `ois.payout.scheduled` в Issuance (см. выше).
     * Остальные события можно оставить на отдельный NX (order/transfer), но нужно явно отметить в Gap‑листе.
   * **Где:** `services/issuance`, `services/registry` (outbox‑publisher’ы) и `asyncapi.yaml`.
   * **Когда:** `ois.payout.scheduled` — вместе с NX‑06; остальные можно отложить.

3. **Gateway OpenAPI vs фактические маршруты (`/issuances` vs `/v1/issuances`, `/orders/{id}`)**

   * **Что:** OpenAPI‑gateway не полностью совпадает с YARP‑маршрутами (prefix `/v1`, `orders` и т.п.).
   * **Почему важно:** TS SDK и фронты генерируются по OpenAPI; несоответствие может выстрелить при подключении новых клиентов или строгой проверке контрактов.
   * **Минимальное изменение:**

     * Обновить `openapi-gateway.yaml` под фактические пути YARP (хотя бы для `/issuances` и `/v1/orders/{**catch-all}`).
   * **Где:** `packages/contracts/openapi-gateway.yaml` + при необходимости `apps/api-gateway/appsettings.json`.
   * **Когда:** разумно вклинить в NX‑05, т.к. фронт по отчётам/дашборду активно полагается на gateway spec.

4. **Health/metrics & gateway observability**

   * **Что:** health есть практически у всех сервисов, но у gateway нет Prometheus‑метрик; часть интеграций ещё без health (ESIA/EDO). 
   * **Почему важно:** для укладки в NX‑05/06 smoke‑проверки и k6‑нагрузку важно иметь базовую observability.
   * **Минимальное изменение:**

     * Добавить Prometheus exporter в gateway (по аналогии с Issuance/Registry/Settlement).
     * Для интеграций — простые `/health` endpoints + включить их в `make check-health`.
   * **Где:** `apps/api-gateway/Program.cs`; соответствующие integration services.
   * **Когда:** можно параллельно NX‑05/06, не блокирует, но улучшит диагностику.

5. **SMTP/Keycloak на uk1**

   * **Что:** Postfix сейчас слушает `inet_interfaces = all`; план — ограничить до локальных IP, плюс fail2ban.
   * **Почему важно:** открытый порт 25 на публичном лице = спам/blacklist риск.
   * **Минимальное изменение:**

     * Обновить конфиг Postfix (inet_interfaces) и перезапустить, сверив `ss -ltnp | grep :25`.
   * **Где:** `/etc/postfix/main.cf` на uk1.
   * **Когда:** хорошо бы до активной эксплуатации e‑mail фич; но изменение рисковое, требует отдельного windows и явного smoke (Keycloak forgot password).

6. **Состояние cfa1 (долг по восстановлению)**

   * **Что:** по последним логам доступ по SSH нестабилен, старый compose‑стек, нет чёткого statе.
   * **Почему важно:** cfa1 рассматривается как будущий прод/стейджинг; пока нет гарантированной воспроизводимости.
   * **Минимальное изменение:**

     * Применить новый runbook (см. 2.3.4), зафиксировать результат в отдельном Scrum‑репорте.
   * **Когда:** после стабилизации uk1, но до вывода новых регионов (us1/vps1/germ1).

---

## 3) Tables

### 3.1 Feature ↔ Endpoints ↔ Services ↔ Frontend ↔ Tests

| Feature block                    | REST endpoints                                                                | Service    | Frontend route         | Tests                                                  |
| -------------------------------- | ----------------------------------------------------------------------------- | ---------- | ---------------------- | ------------------------------------------------------ |
| Issuer dashboard summary         | `GET /v1/reports/issuances`                                                   | Settlement | `/dashboard`           | Unit: dashboard mapper; E2E: issuer login → dashboard  |
| Issuances report (issuer)        | `GET /v1/reports/issuances`                                                   | Settlement | `/reports` (Issuances) | Playwright `/reports` issuances tab                    |
| Payouts report (issuer)          | `GET /v1/reports/issuer/payouts`                                              | Settlement | `/reports` (Payouts)   | Playwright `/reports` payouts tab (обновить endpoints) |
| Issuance details (with schedule) | `GET /issuances/{id}` → `/v1/issuances/{id}`                                  | Issuance   | `/issuances/[id]`      | E2E issuer journey (create → view details)             |
| Payout schedule read‑only        | `GET /v1/issuances/{id}/payouts/schedule` (**SPEC DIFF**) или `scheduleJson`  | Issuance   | `/issuances/[id]` tab  | New E2E: open payout schedule tab                      |
| Payout schedule CRUD             | `POST/GET/PATCH/DELETE /v1/issuances/{id}/payouts/schedule/*` (**SPEC DIFF**) | Issuance   | (future edit mode)     | Unit/integration: schedule service & events            |

### 3.2 Runbook (uk1) — шаги ↔ команды ↔ проверки

| Step                   | Command/Tool                                                                                                                   | Expected check                                 |                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- | ---------------------------------------------- |
| Docker baseline        | `docker ps`                                                                                                                    | Postgres/Kafka/Keycloak up                     |                                                |
| Keycloak up            | `docker compose ... up -d keycloak keycloak-proxy`                                                                             | `curl http://localhost:8080/health/ready` =200 |                                                |
| Services build+run     | `DOCKER_BUILDKIT=1 docker compose ... build ...` + `docker compose ... up -d ... api-gateway`                                  | `docker ps` показывает сервисы Up              |                                                |
| Health & metrics       | `make check-health`; `curl http://localhost:5000/health`; `curl [http://localhost:5002/metrics](http://localhost:5002/metrics) | head`                                          | All health OK, metrics не 500                  |
| SMTP safety (optional) | `postconf inet_interfaces`; `ss -ltnp                                                                                          | grep :25`                                      | Port 25 слушает только 127.0.0.1/172.17/172.18 |
| E2E smoke (Playwright) | `cd tests/e2e-playwright && npm test`                                                                                          | Issuer/Investor/Backoffice scenarios pass      |                                                |

### 3.3 Runbook (new host) — шаги ↔ команды ↔ проверки

| Step                    | Command/Tool                                                                                              | Expected check                                     |
| ----------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Base install            | `apt/yum install docker git curl` + nvm/Node                                                              | `docker --version`, `node -v` ok                   |
| Clone & branch          | `git clone ... && cd .../ois-cfa && git checkout infra.defis.deploy`                                      | `git status` clean on `infra.defis.deploy`         |
| DB+Kafka+Keycloak       | `docker compose ... up -d postgres ois-zookeeper ois-kafka keycloak`                                      | `curl http://localhost:8080/health/ready` =200     |
| .NET services + gateway | `docker compose ... build ... && docker compose ... up -d ... api-gateway`                                | `curl http://localhost:5000/health` =200           |
| Frontends dev           | `npm install && npm run dev -- --port 3001/2/3` в порталах                                                | Порталы открываются локально                       |
| SSH tunnels + smoke     | `ssh -N -L 15500:localhost:5000 -L 15808:localhost:8080 -L 15301:3001 ... user@host`; `make check-health` | Health OK, порталы/Keycloak доступны через туннель |

---

## 4) Next actions (для инженера)

**Backend / NX‑05:**

* [ ] На ветке `infra.defis.deploy` локально убедиться, что settlement реализует `GET /v1/reports/issuances` и `GET /v1/reports/issuer/payouts` строго по спекам; при необходимости допилить хендлеры + интеграционные тесты.
* [ ] Обновить/проверить `openapi-gateway.yaml` для `/v1/reports/**` и `/issuances` vs `/v1/issuances`; зафиксировать SPEC DIFF в соответствующем task‑md, не меняя уже работающие YARP‑маршруты.
* [ ] Перегенерировать TS SDK для gateway (если отстаёт), подключить в `apps/portal-issuer`, реализовать data‑layer для отчётов и дашборда, заменить заглушки.

**Frontend / NX‑05:**

* [ ] В `/dashboard` подключить реальный `IssuerIssuancesReportResponse` и отрисовать базовые KPI.
* [ ] В `/reports` привязать вкладки Issuances/Payouts к `/v1/reports/issuances` и `/v1/reports/issuer/payouts`, оставить CSV/XLSX экспорт поверх тех же данных.
* [ ] Обновить Playwright‑тесты для `/reports`, чтобы они использовали реальные endpoint’ы (с возможной подменой ответов в тест‑режиме).

**NX‑06 (Spec & UI):**

* [ ] Подготовить YAML‑патч SPEC DIFF с эндпойнтами `POST/GET/PATCH/DELETE /v1/issuances/{id}/payouts/schedule` и схемой `PayoutScheduleItem`, положить в `tasks/NX-06-payout-schedule-SPEC-DIFF.md`. 
* [ ] Реализовать на Issuance service CRUD по расписанию поверх `scheduleJson`, добавить producer `ois.payout.scheduled`.
* [ ] Добавить вкладку Payout schedule на `/issuances/[id]` в `portal-issuer` (read‑only), плюс unit/e2e тесты на рендер и отсутствие ошибок.

**Infra / uk1:**

* [ ] На uk1 аккуратно прогнать: `docker compose ... build` + `docker compose ... up -d ...` + `make check-health`, убедиться, что api‑gateway и сервисы поднялись.
* [ ] Проверить, что тест `Publish_NonExistent_Should_Return_404` зелёный против текущего кода/образов (при необходимости пересобрать `issuance-service`).
* [ ] Запустить e2e Playwright (issuer/investor/backoffice) и приложить результаты в очередной UK1‑деплой отчёт.

**Infra / новый хост (первым кандидатом cfa1):**

* [ ] Поднять базовый стек по новому runbook’у (Postgres+Kafka+Keycloak+сервисы+gateway), поднять фронты dev‑режиме на 3001/2/3, настроить Keycloak realm `ois-dev`.
* [ ] Организовать SSH‑туннели с `eywa1` и проверить `/health`, логин в порталы, базовый issuer flow (создать выпуск → посмотреть в UI).
* [ ] Зафиксировать все шаги и выводы в новом memory‑bank Scrum‑отчёте по cfa1, чтобы следующий агент видел актуальное состояние.

Если нужно, можем следующим шагом углубиться в конкретный блок (например, только NX‑06 SPEC DIFF с примером YAML‑патча или конкретную разметку дашборда в `portal-issuer`).

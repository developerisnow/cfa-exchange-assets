1. TL;DR

* NX‑05: дашборд и отчёты делаем **на существующих settlement‑контрактах** (`/v1/reports/issuances`, `/v1/reports/issuer/payouts`, `/v1/reports/payouts`) через gateway `/v1/reports/**`. Сначала добиваем backend‑эндпойнты и SDK, потом уже шлифуем UI и e2e.【turn8file0†file_00000000ac6c722fb7e9d3cb71fdf6da】【turn8file2†file_000000004f6c722fade4dab16629f0b7】
* NX‑06: payout schedule — это **осознанный SPEC DIFF**: добавляем CRUD эндпойнты `/v1/issuances/{id}/payouts/schedule*` в OpenAPI (issuance+gateway), реализуем CRUD поверх `Issuance.scheduleJson` и наконец-то вводим producer для `ois.payout.scheduled`. UI — вкладка *Payout schedule* на `/issuances/[id]` в issuer‑портале.【turn7file2†file_00000000ac6c722fb7e9d3cb71fdf6da】【turn7file5†file_0000000048f0722fbdf9d3f178eb2ff3】
* Infra: на **uk1** — аккуратный runbook “ничего не ломаем”: docker‑stack + pm2 Next.js, Keycloak, Cloudflare/Nginx, health и базовый issuer‑flow. Для **новых хостов (cfa1/us1/vps1/germ1)** — чистый reproducible runbook от голой VM до работающих `/health` + порталов (без переноса живых данных).【turn9file8†file_0000000048f0722fbdf9d3f178eb2ff3】【turn8file11†file_000000003fec722fb560954089a284ed】
* Риски: 500 вместо 404 в issuance‑API, события AsyncAPI без продьюсеров, расхождения OpenAPI ↔ gateway/YARP, незавершённые NX‑05 фронтовые заготовки, полуразобранный cfa1 и возможные хвосты от агента NX01020304 — всё это надо явно в “risk register” и по очереди гасить.【turn7file6†file_00000000dc7871f5b1700aac00dd4888】【turn7file8†file_0000000048f0722fbdf9d3f178eb2ff3】
* В конце даю готовый **seed‑промпт для CLI‑агента**, который учитывает NX‑01..04, uk1/cfa1 и твои правила (spec‑first, “don’t break uk1”).

---

## 2. Steps

### 2.1 NX‑05 plan — Issuer Dashboard & Reports

#### 2.1.1 Why (зачем)

* По FRONTEND‑CONTEXT сейчас: `/dashboard` и `/reports` у эмитента либо заглушки, либо частично “на моках”. MVP‑пробел: нет нормальной отчётности по выпускам и выплатам.【turn9file8†file_0000000048f0722fbdf9d3f178eb2ff3】
* В контрактах уже есть отчётные эндпойнты в gateway/settlement (`/v1/reports/...`), но реализация и фронт до конца не доведены.【turn8file0†file_00000000ac6c722fb7e9d3cb71fdf6da】
* Твои последние шаги по NX‑05: сделан черновой UI (`apps/portal-issuer/app/dashboard`, `/reports`), API‑клиент `lib/api/issuances.ts` и временный SPEC DIFF для `/v1/issuances/summary` (агрегаты на клиенте). Всё ещё in progress.【turn9file1†file_00000000787871fbb20dd1f5f43ce5f5】【turn9file6†file_00000000787871fbb20dd1f5f43ce5f5】

**Вывод:** NX‑05 надо доделать так, чтобы:

* бизнес‑KPI на дашборде шли из settlement‑отчётов,
* отчёты `/reports` опирались на `/v1/reports/issuances` и `/v1/reports/issuer/payouts`,
* любые дополнительные агрегаты (типа `/v1/issuances/summary`) были чётко помечены как SPEC DIFF (и не ломали существующую архитектуру).

---

#### 2.1.2 What (что именно делаем)

**Backend / Contracts**

* Используем уже существующие спецификации в `openapi-gateway.yaml` для отчётов:

  * `GET /v1/reports/issuances` → `IssuerIssuancesReportResponse` (issuerId, from, to).【turn8file0†file_00000000ac6c722fb7e9d3cb71fdf6da】
  * `GET /v1/reports/issuer/payouts` → `IssuerPayoutsReportResponse` (issuerId, период, granularity).【turn8file0†file_00000000ac6c722fb7e9d3cb71fdf6da】
  * `GET /v1/reports/payouts` → общий payout‑репорт (может идти на backoffice/internals, но gateway уже маршрутизирует `/v1/reports/**` в settlement).【turn8file5†file_00000000ac6c722fb7e9d3cb71fdf6da】【turn8file2†file_000000004f6c722fade4dab16629f0b7】

**SPEC DIFF (уже сейчас):**

* В `services/settlement/Program.cs` реализован только `GET /reports/payouts` без issuer‑специфичных эндпойнтов — это расхождение с OpenAPI, где описаны `/v1/reports/issuances` и `/v1/reports/issuer/payouts`. **SPEC DIFF: OpenAPI > код settlement**.【turn6file10†file_000000002c3c722fbe42dfae64bfe362】【turn8file0†file_00000000ac6c722fb7e9d3cb71fdf6da】

**Frontend**

* Feature‑блоки NX‑05:

  1. **Dashboard `/dashboard`**

     * Плитки: `activeIssuancesCount`, `closedIssuancesCount`, `totalNominalAmount`, опционально `totalInvestors`.
     * Источник: `IssuerIssuancesReportResponse.summary` (агрегаты по эмитенту).【turn9file15†file_00000000217871f5ba710cf45772911c】

  2. **Reports `/reports`**

     * Вкладка **Issuances**: табличный отчёт по выпускам эмитента (кол-во, объёмы, статусы, даты). Source: `IssuerIssuancesReportResponse.items[]`.
     * Вкладка **Payouts**: график/таблица “Payouts Over Time” по issuer’у (используем `IssuerPayoutsReportResponse` с granularity=month/day).【turn9file15†file_00000000217871f5ba710cf45772911c】
     * Export CSV/XLSX поверх этих DTO, без отдельных “export” эндпойнтов.

  3. **E2E issuer‑flow**

     * Login через Keycloak → `/dashboard` → `/reports` → переключение табов, проверка рендера и экспорта.

---

#### 2.1.3 How (как делаем)

**Backend (settlement service)**

1. **Дотянуть реализацию отчётов до контракта**

   * В `services/settlement/Program.cs` добавить маршруты с префиксом `/v1` (как в OpenAPI) к API‑группе, которая уже обслуживает `/v1/settlement/**` и `/v1/reports/**`. Сейчас Program.cs явно мапит только `/reports/payouts` (без `/v1`).【turn6file10†file_000000002c3c722fbe42dfae64bfe362】
   * Внутри сервисного слоя (условный `ReportsService`) реализовать методы:

     * `GetIssuerIssuancesReportAsync(Guid issuerId, DateOnly? from, DateOnly? to)` → `IssuerIssuancesReportResponse`.
     * `GetIssuerPayoutsReportAsync(Guid issuerId, DateOnly? from, DateOnly? to, string granularity)` → `IssuerPayoutsReportResponse`.
   * Реализацию строим на уже существующем домене settlement/registry (`Payout`, `PayoutItem`, `RegistryTx`, etc.). Контракты есть в JSON Schemas (`Payout.json`, `PayoutBatch.json`, пр.).【turn7file13†file_00000000ac6c722fb7e9d3cb71fdf6da】

2. **Синхронизация с OpenAPI**

   * Проверить, что `openapi-settlement.yaml` и `openapi-gateway.yaml` описывают эти маршруты именно как `/v1/reports/issuances` и `/v1/reports/issuer/payouts` — это уже так по коду contracts.【turn8file0†file_00000000ac6c722fb7e9d3cb71fdf6da】
   * Если в gateway‑спеке ещё есть устаревшие пути без `/v1` — зафиксировать **SPEC DIFF: OpenAPI‑gateway vs YARP** и поправить, чтобы TS SDK генерировался из актуальных путей.【turn7file5†file_0000000048f0722fbdf9d3f178eb2ff3】

3. **Тесты backend**

   * Юнит/интеграционные тесты в `services/settlement/settlement.Tests` (или новый проект, если его нет):

     * happy‑path: данные есть → корректные агрегаты;
     * empty‑data: ответ с пустыми массивами/нулями;
     * валидация параметров (некорректные даты → 400).

**Frontend (portal‑issuer)**

4. **API‑слой**

   * Обновить/дополнить TS SDK: в `packages/sdks/ts` пересгенерировать клиенты по `openapi-gateway.yaml` (уже настроено через `openapitools.json` и `Makefile generate-sdks`).【turn7file13†file_00000000ac6c722fb7e9d3cb71fdf6da】

   * В `apps/portal-issuer/lib/api/` завести/обновить модули:

     * `reports.ts`:

       * `getIssuerIssuancesReport(issuerId, range)` → использует `GET /v1/reports/issuances`.
       * `getIssuerPayoutsReport(issuerId, range, granularity)` → `GET /v1/reports/issuer/payouts`.
     * `issuances.ts`: оставить уже сделанные вызовы `GET /v1/issuances`, но убрать временный “/summary” SPEC DIFF, если он не закреплён в контрактах (либо оформить его как отдельный, но **по умолчанию** строить дашборд из отчётного эндпойнта).【turn9file1†file_00000000787871fbb20dd1f5f43ce5f5】

   * В запросах по возможности прокидывать `x-request-id`, `traceparent`, `x-client-app`, если это уже делается централизованным fetch‑wrapper’ом (иначе — TODO для отдельной NX).【turn9file5†file_00000000f9e0722fb7d0868fe674fd1d】

5. **UI `/dashboard`**

   * Заменить текущую клиентскую агрегацию списка выпусков на дергание `getIssuerIssuancesReport`.
   * Маппинг `summary` → карточки:

     * `activeCount`, `closedCount`, `totalAmount`, опционально `investorsCount`.
   * Покрыть компонент юнит‑тестами (React Testing Library):

     * корректный рендер при нормальном ответе, пустом ответе, ошибке.

6. **UI `/reports`**

   * Вкладка **Issuances**:

     * таблица по `IssuerIssuancesReportResponse.items[]`.
     * фильтры по периоду.
     * кнопка Export → клиентский CSV.
   * Вкладка **Payouts**:

     * график/таблица на основе `IssuerPayoutsReportResponse.items[]` (использовать уже задуманный сценарий “Payouts Over Time”).
   * E2E‑тесты (Playwright):

     * re‑use существующие спеки, которые сейчас подменяют `**/v1/reports/payouts**` — перевести их на реальные данные или минимальный stub gateway, но не ломать контракты.

**Tests & artifacts**

7. **End‑to‑end**

   * В `tests/e2e-playwright` добавить spec для issuer‑дашборда/отчётов (если ещё нет):

     * login → `/dashboard` → проверка метрик,
     * переход на `/reports`, переключение табов, проверка таблиц и экспорта.
   * Отдельный артефакт `artifacts/issuer-dashboard-and-reports.md` обновить:

     * перечислить использованные эндпойнты,
     * привести примеры JSON‑ответов,
     * ссылку на успешный e2e‑run.【turn9file6†file_00000000787871fbb20dd1f5f43ce5f5】

---

#### 2.1.4 Result (“Done”)

* В settlement реализованы `/v1/reports/issuances` и `/v1/reports/issuer/payouts` строго по OpenAPI, gateway прокидывает `/v1/reports/**`.
* Portal‑issuer `/dashboard` и `/reports` работают на реальных данных через gateway, без моков.
* Есть e2e smoke‑флоу “issuer login → dashboard → reports” и артефакт `issuer-dashboard-and-reports.md` с фиксированными SPEC DIFF’ами (если остаются).

---

### 2.2 NX‑06 plan — Issuer Payout Schedule (Spec + UI)

#### 2.2.1 Why

* В FRONTEND‑CONTEXT прямо написано: **нет управления расписанием выплат (payout schedule) — нужен SPEC DIFF в OpenAPI**, это MVP‑критичный gap для эмитента.【turn9file8†file_0000000048f0722fbdf9d3f178eb2ff3】
* В AsyncAPI уже есть `PayoutScheduled` / `PayoutExecuted` сообщения и топик `ois.payout.scheduled`, но без продьюсера — SPEC DIFF: событие есть в спеках, нет в коде.【turn7file2†file_00000000ac6c722fb7e9d3cb71fdf6da】【turn7file6†file_00000000dc7871f5b1700aac00dd4888】
* Domain уже умеет хранить график: `Issuance` содержит `scheduleJson` (JSON‑график выплат).【turn1file10†file_00000000ac6c722fb7e9d3cb71fdf6da】

**Вывод:** NX‑06 — это не новая архитектура, а “достать наружу” уже существующее поле через spec‑first CRUD и завести событие `ois.payout.scheduled`.

---

#### 2.2.2 What (текущее состояние vs надо)

**Сейчас:**

* OpenAPI‑issuance/gateway: **нет** `.../payouts/schedule` эндпойнтов (требует SPEC DIFF).【turn9file9†file_00000000f9e0722fb7d0868fe674fd1d】
* AsyncAPI: `PayoutScheduledPayload` описан, канал `ois.payout.scheduled` объявлен, но продьюсеров нет — SPEC DIFF (спецификация опережает код).【turn7file2†file_00000000ac6c722fb7e9d3cb71fdf6da】
* Portal‑issuer `/issuances/[id]`: есть publish/close, но нет UI для расписания выплат (FRONTEND‑CONTEXT).【turn9file8†file_0000000048f0722fbdf9d3f178eb2ff3】

**Надо (минимально):**

1. **SPEC DIFF: OpenAPI (issuance+gateway)**
   Добавить в `openapi-issuance.yaml` и `openapi-gateway.yaml` эндпойнты:

   * `GET /v1/issuances/{id}/payouts/schedule`
   * `POST /v1/issuances/{id}/payouts/schedule` (create/replace)
   * `PATCH /v1/issuances/{id}/payouts/schedule/{itemId}`
   * `DELETE /v1/issuances/{id}/payouts/schedule/{itemId}`

   Всё с телами, построенными вокруг новой схемы `PayoutScheduleItem[]`. Это осознанный SPEC DIFF NX‑06 (отдельный YAML‑патч в `tasks/NX-06-payout-schedule-SPEC-DIFF.md`).【turn7file0†file_00000000217871f5ba710cf45772911c】

2. **SPEC DIFF: JSON Schemas**

   * Добавить схему `PayoutScheduleItem` рядом с текущими payout‑схемами (`Payout.json`, `PayoutBatch.json`). Поля минимум:

     * `id: uuid`
     * `date: date`
     * `amount: decimal`
     * `status: enum[planned, confirmed, executed, cancelled]`.【turn7file1†file_00000000217871f5ba710cf45772911c】

3. **AsyncAPI**

   * Уточнить использование `ois.payout.scheduled`:

     * Producer: Issuance service при создании/изменении расписания по выпуску.
     * Payload: `PayoutScheduledPayload` (уже описан); при необходимости добавить ссылку на `PayoutScheduleItem` (новый SPEC DIFF для AsyncAPI).【turn7file2†file_00000000ac6c722fb7e9d3cb71fdf6da】

4. **UI**

   * В Portal Issuer на `/issuances/[id]` добавить вкладку **Payout schedule** с read‑only табличкой: дата, сумма, статус.
   * Пока CRUD на фронте можно не включать (read‑only UX): главное — корректно отображать расписание из backend (через новые эндпойнты либо через `scheduleJson` как fallback).【turn7file14†file_00000000217871f5ba710cf45772911c】

---

#### 2.2.3 How (backend, frontend, tests)

**Backend (Issuance service)**

1. **CRUD по расписанию**

   * В `services/issuance/Program.cs` добавить маршруты:【turn7file10†file_00000000217871f5ba710cf45772911c】

     ```csharp
     api.MapGet("/v1/issuances/{id:guid}/payouts/schedule", ...);
     api.MapPost("/v1/issuances/{id:guid}/payouts/schedule", ...);
     api.MapPatch("/v1/issuances/{id:guid}/payouts/schedule/{itemId:guid}", ...);
     api.MapDelete("/v1/issuances/{id:guid}/payouts/schedule/{itemId:guid}", ...);
     ```
   * Сервисный слой (`IssuanceService` или отдельный `PayoutScheduleService`):

     * Чтение `scheduleJson` у сущности `Issuance`,
     * Маппинг JSON ↔ `PayoutScheduleItem[]`,
     * Валидация (даты > today, сумма ≥ 0, статус).

2. **Producer `ois.payout.scheduled`**

   * После успешного POST/PATCH/DELETE:

     * Формируем объект `PayoutScheduledPayload` (batchId, scheduledFor, totalAmount, items). Спецификация уже описана в AsyncAPI.【turn7file19†file_00000000ac6c722fb7e9d3cb71fdf6da】
     * Публикуем в Kafka через MassTransit, аналогично тому, как сейчас отправляется `ois.issuance.published` из Outbox publisher’а (см. `services/issuance/Background/OutboxPublisher.cs`).【turn7file9†file_00000000787871fbb20dd1f5f43ce5f5】【turn7file9†file_00000000787871fbb20dd1f5f43ce5f5】

3. **SPEC DIFF фиксация**

   * Обновить `PROJECT-CONTEXT.md` Gap List: убрать `ois.payout.scheduled` из списка “без продьюсеров”, когда producer будет реализован; пока оставить `ois.transfer.completed` и order.* как отдельный долг.【turn7file3†file_00000000787871fbb20dd1f5f43ce5f5】

4. **Тесты backend**

   * Unit:

     * сериализация/десериализация `scheduleJson` ↔ `PayoutScheduleItem[]`,
     * доменная валидация.
   * Integration/API:

     * полный CRUD по расписанию для выпуска,
     * проверка, что `ois.payout.scheduled` добавляется в outbox.

**Frontend (portal‑issuer)**

5. **Вкладка Payout schedule**

   * Страница `/issuances/[id]` (уже есть publish/close):

     * добавить таб/секцию *Payout schedule*;
     * источник данных:

       * **основной**: `GET /v1/issuances/{id}/payouts/schedule`;
       * fallback (ASSUMPTION, нужно проверить): чтение `scheduleJson` из `IssuanceResponse` и локальный маппинг в `PayoutScheduleItem[]`, если спецификация и код так позволяют.【turn7file14†file_00000000217871f5ba710cf45772911c】

   * Рендер: простая таблица (дата, сумма, статус) + totals. Пока **read‑only**.

6. **Тесты frontend**

   * Unit: маппинг DTO → UI, поведение при пустом списке.
   * Integration: запрос `GET /v1/issuances/{id}/payouts/schedule` через SDK, проверка рендера.
   * E2E: расширить issuer‑journey: после создания выпуска открыть вкладку Payout schedule и убедиться, что страница не падает и корректно отрабатывает пустой/заполненный schedule.

---

#### 2.2.4 Result (“Done”)

* Подготовлен и согласован YAML‑патч SPEC DIFF для payout schedule (OpenAPI + JSON Schemas + AsyncAPI).
* Issuance service реализует полный CRUD по расписанию выплат и публикует `ois.payout.scheduled`.
* `PROJECT-CONTEXT` и Gap List обновлены: `ois.payout.scheduled` → “✅ producer implemented”.
* Portal‑issuer показывает расписание выплат на `/issuances/[id]` (минимум read‑only).

---

### 2.3 Infra runbooks — uk1 vs cfa1/новые хосты

#### 2.3.1 High‑level архитектура деплоя

**Компоненты (по контексту + co‑3dd7):**

* Core сервисы: `api-gateway`, `issuance`, `registry`, `settlement`, `compliance`, `identity`, интеграционные адаптеры (bank, esia, edo).【turn7file5†file_0000000048f0722fbdf9d3f178eb2ff3】
* Инфра: `postgres`, `kafka`, (schema registry, zookeeper — если есть в compose), Prometheus/Grafana, SMTP (postfix+opendkim).【turn9file10†file_000000003fec722fb560954089a284ed】
* Auth: Keycloak (realm `ois-dev`, клиенты `portal-issuer`, `portal-investor`, `backoffice`, роли issuer/investor/admin).【turn9file17†file_00000000dc7871f5b1700aac00dd4888】
* Frontends: Next.js apps `portal-issuer` (3001), `portal-investor` (3002), `backoffice` (3003), на uk1 крутятся через shell‑скрипты `/root/.local/bin/run-portal-*.sh` под pm2/forever.【turn9file4†file_000000003fec722fb560954089a284ed】
* Edge: Nginx + Cloudflare (`docs/deploy/20251113-cloudflare-ingress.md`, `ops/infra/uk1/nginx-cfa-portals.conf`).【turn8file7†file_000000003fec722fb560954089a284ed】

---

#### 2.3.2 Runbook: uk1 — “current & safe”

**Цель:** уметь обновить backend/фронты и проверить health, не ломая существующий HTTPS/Cloudflare/Keycloak/email.

1. **Подключиться и зафиксировать состояние**

   * SSH на uk1 (как у тебя в alias).
   * Проверить, что репо/директория: `/opt/ois-cfa` (или актуальный путь).
   * `docker compose ps` — убедиться, что postgres, keycloak, core‑services живы.

2. **Обновить код (по необходимости)**

   * Внутри `/opt/ois-cfa`:

     ```bash
     git fetch origin
     git checkout infra.defis.deploy
     git pull --rebase origin infra.defis.deploy
     ```
   * **Не трогать** Nginx/Cloudflare конфиги без отдельного плана (они задокументированы в `docs/deploy/20251113-cloudflare-ingress.md`).【turn8file7†file_000000003fec722fb560954089a284ed】

3. **Бэкенд‑стек**

   * Билд+подъём сервисов (без трогания БД/Keycloak, если не нужно мигрировать):

     ```bash
     docker compose pull
     docker compose up -d api-gateway issuance-service registry-service settlement-service compliance-service identity-service
     ```
   * Если **нужно прогнать миграции** — *одноразово* выставить `MIGRATE_ON_STARTUP=true` в env для нужного сервиса (registry/settlement/compliance/issuance) — это уже провязано в Program.cs через чтение env и `MigrationsAssembly` из реального assembly, а не хардкода.【turn8file11†file_000000003fec722fb560954089a284ed】
   * После первого запуска обязательно вернуть `MIGRATE_ON_STARTUP=false` и перезапустить сервисы.

4. **Keycloak**

   * `docker compose ps keycloak keycloak-proxy` — проверить, что оба контейнера живы.
   * Если нужно поднять — использовать `docker compose -f docker-compose.yml -f ops/infra/uk1/docker-compose.keycloak-proxy.yml up -d keycloak keycloak-proxy`.【turn8file7†file_000000003fec722fb560954089a284ed】
   * Настройки realm/clients/users — по `KEYCLOAK-SETUP.md` (уже есть док).

5. **Frontends на uk1**

   * Не трогать `/root/.local/bin/run-portal-*.sh`, если всё работает.
   * При необходимости restart:

     ```bash
     ssh root@uk1 'pm2 restart run-portal-issuer run-portal-investor run-backoffice'
     ```

     (Или соответствующие systemd‑units, если перенастроено.)

6. **Health & smoke**

   * На самом сервере (или через ssh‑туннели):

     ```bash
     curl -f http://localhost:5000/health
     curl -f http://localhost:5000/metrics || echo "no metrics for gateway (known gap)"
     ```
   * Снаружи (через домены Cloudflare):

     * `curl -Ik https://investor.cfa...`, `https://issuer.cfa...` — статус 200/302 от Next.js.【turn9file10†file_000000003fec722fb560954089a284ed】
   * Smoke e2e (из репо tests/e2e или tests/e2e-playwright):

     ```bash
     cd tests/e2e-playwright
     npm test  # или npx playwright test issuer-smoke.spec.ts
     ```

7. **Что НЕ трогать без плана**

   * Cloudflare DNS/SSL, Nginx конфиги (`ops/infra/uk1/nginx-cfa-portals.conf`), Postfix/opendkim и Keycloak realm.
   * Любые “горячие” настройки uk1, которые уже используются боевой/демо‑аудиторией.

---

#### 2.3.3 Runbook: новый хост (cfa1/us1/vps1/germ1)

**Цель:** из чистой VM сделать среду, на которой можно запускать NX‑05/NX‑06 и е2е, *не трогая uk1*.

1. **Базовая подготовка системы**

   ```bash
   sudo apt-get update
   sudo apt-get install -y git docker.io docker-compose-plugin nginx
   # Node / pnpm по твоему стандартному скрипту (nvm use 20.x)
   ```

2. **Клонирование монорепо**

   ````bash
   git clone git@github.com:developerisnow/cfa-exchange-assets.git
   cd cfa-exchange-assets
   git submodule update --init --recursive
   cd repositories/customer-gitlab/ois-cfa
   git checkout infra.defis.deploy
   ```【turn8file16†file_000000003fec722fb560954089a284ed】  

   ````

3. **Docker‑стек**

   * В `.env` или compose‑override задать connection strings, порты, `MIGRATE_ON_STARTUP=true` для первого запуска.
   * Запустить базовую инфру:

     ```bash
     docker compose up -d postgres kafka zookeeper
     docker compose up -d keycloak
     docker compose up -d api-gateway issuance-service registry-service settlement-service compliance-service identity-service
     ```
   * После первого старта — отключить `MIGRATE_ON_STARTUP`.

4. **Keycloak “ois-dev”**

   * Открыть http://<host>:8080, логин admin/admin.
   * Создать realm `ois-dev`, clients `portal-issuer`, `portal-investor`, `backoffice`, роли `issuer`, `investor`, `admin`, тест‑пользователи (см. KEYCLOAK-SETUP).【turn9file17†file_00000000dc7871f5b1700aac00dd4888】

5. **Frontend dev‑режим**

   ````bash
   # Portal Issuer
   cd apps/portal-issuer && npm install && npm run dev -- -p 3001
   # Portal Investor
   cd ../portal-investor && npm install && npm run dev -- -p 3002
   # Backoffice
   cd ../backoffice && npm install && npm run dev -- -p 3003
   ```【turn9file17†file_00000000dc7871f5b1700aac00dd4888】  

   - Для устойчивости: оформить это через pm2 (как на uk1) или systemd‑services.  

   ````

6. **SSH‑туннели с eywa1 (чтобы запускать тесты там)**

   ````bash
   ssh -N \
     -L 15500:localhost:5000 \
     -L 15808:localhost:8080 \
     -L 15301:localhost:3001 \
     -L 15302:localhost:3002 \
     -L 15303:localhost:3003 \
     user@cfa1
   ```【turn7file18†file_00000000217871f5ba710cf45772911c】  

   - После этого с eywa1:  
     ```bash
     curl -f http://localhost:15500/health
     # открыть порталы и Keycloak в браузере через локальные порты
   ````

7. **Smoke‑тесты**

   * `make check-health` (если Makefile уже адаптирован).【turn7file7†file_00000000787871fbb20dd1f5f43ce5f5】
   * Из `tests/e2e-playwright` на eywa1 (через туннели) прогнать базовый issuer/investor login и один happy‑path.
   * Все команды/вывод сложить в новый memory‑bank лог для cfa1 (по аналогии с уже существующими).【turn9file13†file_000000003fec722fb560954089a284ed】

**Риски для нового хоста:**

* Миграции: не забыть выключить `MIGRATE_ON_STARTUP` после первого прогона.
* SMTP: на новых хостах лучше ограничить Postfix только на loopback/bridge; полноценная почта — отдельная сессия (ты это уже помечал).【turn9file10†file_000000003fec722fb560954089a284ed】

---

### 2.4 Risk register / Open issues

Явно фиксируем ключевые дыры, которые влияют на NX‑05/06 и деплой.

1. **Issuance API: 404 vs 500 для Publish_NonExistent**

* **Что:** тест `Publish_NonExistent_Should_Return_404` всё ещё ловит 500, несмотря на guard в Program.cs (NX‑03).【turn7file15†file_00000000dc7871f5b1700aac00dd4888】
* **Почему важно:** некорректный статус ломает клиентов и e2e, особенно когда порталы дергают publish/close.
* **Минимальное изменение:**

  * Локально на eywa1:

    ````bash
    cd repositories/customer-gitlab/wt__ois-cfa__NX01
    $HOME/.dotnet/dotnet test tests/issuance.Tests/issuance.Tests.csproj -v minimal
    ```【turn7file15†file_00000000dc7871f5b1700aac00dd4888】  
    ````
  * Если тест всё ещё падает: доработать обработку несуществующего Issuance (проверка `GetByIdAsync` + корректная мапа исключения в 404).
  * Убедиться, что на uk1 деплоится образ с этой логикой (не старый билд).【turn8file4†file_00000000787871fbb20dd1f5f43ce5f5】
* **Где:** `services/issuance/Program.cs`, `IssuanceService` и деплой образа `issuance-service`.
* **Когда:** до/вместе с NX‑05 (чтобы дашборд/отчёты не натыкались на странные ошибки).

---

2. **AsyncAPI события без продьюсеров**

* **Что:** `ois.order.placed`, `ois.order.confirmed`, `ois.payout.scheduled`, `ois.transfer.completed` объявлены в AsyncAPI, но продьюсеров нет (подтверждено в Gap List).【turn7file3†file_00000000787871fbb20dd1f5f43ce5f5】
* **Почему важно:**

  * Для NX‑06 `ois.payout.scheduled` — ключевой для downstream‑аналитики и аудита.
  * `order.*` и `transfer.*` важны для полной трассировки реестра/settlement.
* **Минимальное изменение:**

  * В рамках NX‑06 — реализовать producer `ois.payout.scheduled` (см. 2.2).
  * Для `order.placed/confirmed` и `transfer.completed` — оставить как отдельный NX‑gap, но держать в Gap List.
* **Где:** Issuance/Registry services (`OutboxPublisher`), `asyncapi.yaml`.
* **Когда:** `ois.payout.scheduled` — вместе с NX‑06, остальное можно отложить.

---

3. **Gateway OpenAPI vs YARP path‑prefixы**

* **Что:** некоторые пути в `openapi-gateway.yaml` расходятся с фактическими маршрутами YARP (`/issuances` vs `/v1/issuances`, `/orders/{id}`, отчётные пути и т.п.). Это уже отмечено как SPEC DIFF в контексте NX‑02.【turn7file5†file_0000000048f0722fbdf9d3f178eb2ff3】
* **Почему важно:** TS‑SDK и фронты опираются на OpenAPI; при строгой валидации или новом клиенте это выстрелит.
* **Минимальное изменение:**

  * Сверить `appsettings.json` YARP routes с `openapi-gateway.yaml` (особенно `orders`, `issuances`, `reports`).【turn8file2†file_000000004f6c722fade4dab16629f0b7】
  * Либо править OpenAPI под YARP, либо добавить дубль маршрута в YARP, но **явно задокументировать** SPEC DIFF.
* **Где:** `apps/api-gateway/appsettings.json`, `packages/contracts/openapi-gateway.yaml`, `artifacts/gateway-routing-report.md`.
* **Когда:** по-хорошему — завершить в хвосте NX‑02 перед активным использованием NX‑05/06.

---

4. **NX‑05 фронтовые черновики (feature/nx-05-issuer-dashboard)**

* **Что:** сейчас реализованы client‑агрегации (`/v1/issuances`, `/v1/issuances/summary`), SPEC DIFF под `/v1/reports/issuances` в черновике, отчёты частично висят на моках.【turn9file1†file_00000000787871fbb20dd1f5f43ce5f5】
* **Риск:** появятся два источника “правды”: settlement‑репорты и client‑агрегаты.
* **Минимальное изменение:**

  * В новой итерации NX‑05 перейти на settlement‑эндпойнты как первичные, дефолтные.
  * Эндпойнт `/v1/issuances/summary` либо оформить как бонусный SPEC DIFF, либо убрать из фронта.
* **Где:** `apps/portal-issuer/lib/api/issuances.ts`, `/dashboard`, `/reports`, `tasks/NX-05-issuer-reports-SPEC-DIFF.md`.
* **Когда:** в основной доработке NX‑05 (сейчас).

---

5. **Infra на cfa1 + хвосты от агента NX01020304**

* **Что:** cfa1 частично настроен, есть зачатки e2e‑инфры, Playwright, SMTP/Keycloak‑потоки, но состояние неоднородное; плюс ранние агенты (deploy/NX01020304) могли оставить несогласованные изменения (csproj, dockerignore, etc.).【turn8file12†file_000000003fec722fb560954089a284ed】【turn8file6†file_000000003fec722fb560954089a284ed】
* **Риск:** запуск тестов/деплоя на cfa1 будет давать непредсказуемое поведение; самые скрытые баги — от “половинчатых” изменений.
* **Минимальное изменение:**

  * Явно пройтись по `git status`, `git diff` на cfa1, зафиксировать все локальные отличия от `infra.defis.deploy` в отдельном отчёте.
  * По возможности откатить “лишние” изменения до чистого состояния deploy‑ветки и строить новый runbook поверх неё.
* **Где:** `repositories/customer-gitlab/ois-cfa` на cfa1, ветки `deploy`, `infra.defis.deploy`.
* **Когда:** до того, как использовать cfa1 как базовый стенд для NX‑05/06.

---

6. **Gateway metrics и observability**

* **Что:** gateway имеет `/health`, но `/metrics` не провязан (рекомендация уже в контексте).【turn7file5†file_0000000048f0722fbdf9d3f178eb2ff3】
* **Почему важно:** для боевого мониторинга (Prometheus/Grafana) нужен единый источник метрик на входе.
* **Минимальное изменение:**

  * Добавить `UseOpenTelemetryMetrics()` в gateway и промаршрутизировать `/metrics`.
  * Описать это в `PROJECT-CONTEXT` и `gateway-routing-report.md`.
* **Когда:** можно после NX‑05, но до полноценного продакшена.

---

## 3) Tables

### 3.1 Feature ↔ Endpoints ↔ Services ↔ Routes ↔ Tests

| Feature block                      | Endpoints (REST)                                                                 | Service    | Frontend route                        | Tests                                            |
| ---------------------------------- | -------------------------------------------------------------------------------- | ---------- | ------------------------------------- | ------------------------------------------------ |
| Issuer dashboard metrics           | `GET /v1/reports/issuances`                                                      | settlement | `/dashboard`                          | settlement unit/integration; issuer e2e          |
| Issuer issuances report            | `GET /v1/reports/issuances`                                                      | settlement | `/reports` → tab “Issuances”          | settlement tests; Playwright “issuer reports”    |
| Issuer payouts report              | `GET /v1/reports/issuer/payouts`                                                 | settlement | `/reports` → tab “Payouts”            | settlement tests; Playwright “Payouts Over Time” |
| Investor payout history (ref only) | `GET /v1/investors/{id}/payouts`                                                 | settlement | investor `/portfolio` (future)        | investor e2e (later NX)                          |
| Payout schedule CRUD (NX‑06)       | `GET/POST/PATCH/DELETE /v1/issuances/{id}/payouts/schedule*` **(SPEC DIFF)**     | issuance   | `/issuances/[id]` → “Payout schedule” | issuance tests + issuer e2e                      |
| Payout scheduled event             | Topic `ois.payout.scheduled` (AsyncAPI), producer в Issuance **(SPEC DIFF now)** | issuance   | —                                     | unit for publisher + event‑flow tests            |

---

### 3.2 Runbook steps ↔ Commands ↔ Expected checks

**uk1 (safe)**

| Step                        | Command/Tool (пример)                                                          | Expected result / check                   |
| --------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------- |
| Check services              | `docker compose ps`                                                            | все core контейнеры в статусе `Up`        |
| Update backend services     | `docker compose pull && docker compose up -d api-gateway issuance-service ...` | новые образы, сервисы поднялись           |
| Run migrations (если нужно) | `MIGRATE_ON_STARTUP=true` в env + `docker compose up -d <service>`             | миграции применены, потом флаг выключен   |
| Check health                | `curl -f http://localhost:5000/health`                                         | HTTP 200 + JSON `status: healthy`         |
| External HTTPS check        | `curl -Ik https://issuer.cfa...`                                               | 200/302, корректный сертификат            |
| Issuer smoke e2e            | `cd tests/e2e-playwright && npx playwright test issuer-smoke.spec.ts`          | сценарий логина/дашборда/репортов зелёный |

**Новый хост (cfa1/us1/…)**

| Step                             | Command/Tool (пример)                                                                    | Expected result / check                  |
| -------------------------------- | ---------------------------------------------------------------------------------------- | ---------------------------------------- |
| Install base stack               | `apt-get install docker.io docker-compose-plugin git nginx`                              | docker+nginx установлены                 |
| Clone repo + checkout branch     | `git clone ... && git submodule update --init && git checkout infra.defis.deploy`        | код актуален, без конфликтов             |
| Start infra services             | `docker compose up -d postgres kafka keycloak ...`                                       | сервера БД/кластера/Keycloak поднялись   |
| Start core backend               | `docker compose up -d api-gateway issuance-service ...`                                  | `/health` отдаёт 200                     |
| Start frontends dev              | `npm run dev -p 3001/3002/3003`                                                          | порталы доступны по `http://host:300x`   |
| Smoke via SSH tunnels from eywa1 | `ssh -N -L 15500:localhost:5000 ... user@cfa1` + `curl -f http://localhost:15500/health` | health OK, е2е-тесты ходят через туннели |

---

## 4) Next actions (для человека) + seed‑промпт для CLI‑агента

### 4.1 Checklist для тебя (uk1/cfa1)

1. **Зафиксировать текущее состояние веток / контекста**

   ```bash
   cd ~/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets
   git status
   cd repositories/customer-gitlab/ois-cfa
   git status
   git branch -vv
   ```

2. **Перепроверить NX‑03 Issuance tests на eywa1**

   ```bash
   cd repositories/customer-gitlab/wt__ois-cfa__NX01
   $HOME/.dotnet/dotnet test tests/issuance.Tests/issuance.Tests.csproj -v minimal
   ```

   * Зафиксировать итог в `artifacts/issuance-test-report.txt`: всё ещё 500 или уже 404.

3. **Подготовить рабочую ветку для NX‑05/NX‑06**

   * В `ois-cfa` (submodule):

     ```bash
     git checkout infra.defis.deploy
     git pull --rebase origin infra.defis.deploy
     git checkout -b feature/NX-05-06-issuer-reports-and-schedule
     ```

4. **На uk1 — аккуратный health‑ран**

   ```bash
   # на uk1, в каталоге /opt/ois-cfa
   docker compose ps
   docker compose up -d api-gateway issuance-service registry-service settlement-service compliance-service identity-service
   curl -f http://localhost:5000/health
   ```

5. **На новом хосте (первый кандидат cfa1) — поднять базовый стек**

   * По runbook 2.3.3: install → clone → docker compose → Keycloak → frontends → ssh‑туннели и один e2e‑smoke.
   * Всё логировать в новый файл `memory-bank/Scrum/20251119-cfa1-nx05-06/bootstrap.session.md`.

6. **Создать/обновить артефакты**

   * `artifacts/issuer-dashboard-and-reports.md` — описать текущие/планируемые эндпойнты и UI.
   * `tasks/NX-06-payout-schedule-SPEC-DIFF.md` — YAML‑патч для payout schedule.

---

### 4.2 Seed‑промпт для новой CLI‑сессии агента (можно просто скопировать)

```text
You are an Expert .NET 9 + Next.js + Kubernetes/Infra engineer and AI pair-programmer.

CONTEXT
- Monorepo: cfa-exchange-assets.
- Backend submodule: repositories/customer-gitlab/ois-cfa (branch: infra.defis.deploy).
- Spec-first: OpenAPI + AsyncAPI + JSON Schemas in packages/contracts.
- Completed/assumed done on infra.defis.deploy: NX-01..NX-04 (spec validation, gateway routing, issuance endpoints/tests, registry order flow). See:
  - docs/context/PROJECT-CONTEXT.md
  - docs/context/FRONTEND-CONTEXT.md
  - artifacts/spec-*.txt, issuance-endpoints-coverage-report.md, registry-flow-report.md.
- Working env: host "uk1" (do NOT break it).
- Experimental env: "cfa1" (may be dirty, treat as experimental).
- Important SPEC DIFFs:
  - AsyncAPI topics without producers: ois.order.placed, ois.order.confirmed, ois.payout.scheduled, ois.transfer.completed.
  - Issuance events have extra dltTxHash.
  - Gateway OpenAPI vs YARP path prefixes (/v1, /orders/{id}, /reports/**).
- Known test issue: tests/issuance.Tests – Publish_NonExistent_Should_Return_404 currently returns 500.

YOUR ROLE
- Act as a disciplined, spec-first CLI agent.
- Do NOT invent new architecture or contracts from scratch.
- Always align with existing OpenAPI/AsyncAPI/JSON Schemas and current code on branch infra.defis.deploy.
- Every time you introduce or rely on a SPEC DIFF (code vs OpenAPI/AsyncAPI), mark it explicitly in the plan and in docs.

TASKS FOCUS (NOW)
1) NX-05 — Portal Issuer dashboard & basic reports
   - Goal: make /dashboard and /reports in apps/portal-issuer use real backend data via API gateway.
   - Primary report endpoints (do NOT redesign, just implement/use them):
     - GET /v1/reports/issuances → IssuerIssuancesReportResponse
     - GET /v1/reports/issuer/payouts → IssuerPayoutsReportResponse
     - GET /v1/reports/payouts → PayoutsReportResponse (if needed)
   - Plan:
     - Check and implement missing handlers in services/settlement to match openapi-settlement.yaml.
     - Keep gateway routing consistent (apps/api-gateway/appsettings.json, openapi-gateway.yaml).
     - In apps/portal-issuer:
       - use TS SDK generated from openapi-gateway.yaml;
       - implement lib/api/reports.ts with calls to the report endpoints;
       - wire /dashboard and /reports to these APIs, replacing any temporary “/v1/issuances/summary” hacks (unless explicitly accepted as SPEC DIFF).
     - Add tests:
       - settlement unit/integration for reports;
       - portal-issuer unit tests for dashboard and reports;
       - at least one Playwright e2e flow: login → /dashboard → /reports (tabs Issuances/Payouts).

2) NX-06 — Issuer payout schedule spec + UI
   - Goal: spec-first CRUD for payout schedule on issuances + basic read-only UI.
   - Current facts:
     - No /v1/issuances/{id}/payouts/schedule endpoints in OpenAPI.
     - AsyncAPI defines PayoutScheduled/PayoutExecuted messages, ois.payout.scheduled has no producer.
     - Issuance domain contains scheduleJson for payout schedule.
   - Plan:
     - Prepare SPEC DIFF patch (do NOT edit full files inline; work as patch fragment) for:
       - openapi-issuance.yaml + openapi-gateway.yaml:
         - GET /v1/issuances/{id}/payouts/schedule
         - POST /v1/issuances/{id}/payouts/schedule
         - PATCH /v1/issuances/{id}/payouts/schedule/{itemId}
         - DELETE /v1/issuances/{id}/payouts/schedule/{itemId}
         - schemas: PayoutScheduleItem with id/date/amount/status.
       - JSON Schemas: add PayoutScheduleItem.json next to Payout.json/PayoutBatch.json.
       - AsyncAPI: clarify producer of ois.payout.scheduled (Issuance service), payload using PayoutScheduledPayload (+ optional reference to schedule items).
     - Implement in services/issuance:
       - CRUD handlers in Program.cs;
       - service layer using Issuance.scheduleJson (serialize/deserialize PayoutScheduleItem[]).
       - Outbox producer for ois.payout.scheduled on schedule changes.
     - Portal-issuer:
       - add Payout schedule tab to /issuances/[id];
       - primary source: GET /v1/issuances/{id}/payouts/schedule;
       - temporary fallback (if needed): map Issuance.scheduleJson → UI.
     - Tests:
       - Issuance unit/integration tests for schedule CRUD and outbox;
       - frontend unit tests for schedule UI;
       - issuer e2e extended to open payout schedule tab.

3) Infra runbooks
   - You MAY run commands on:
     - uk1: only to check status and run safe rebuilds (docker compose, health checks), but do NOT change nginx/Cloudflare/Keycloak/email configs.
     - cfa1/us1/vps1/germ1: can be used as fresh hosts following a reproducible runbook.
   - Keep two modes:
     - “uk1-safe”: minimal changes, focus on health checks and e2e smoke.
     - “new-host”: from clean VM → docker stack → Keycloak → dev frontends → health/e2e checks.

GENERAL RULES
- Always start by reading existing docs:
  - docs/context/PROJECT-CONTEXT.md
  - docs/context/FRONTEND-CONTEXT.md
  - tasks/NX-05-issuer-dashboard-and-reports.md
  - tasks/NX-06-issuer-payout-schedule-spec-and-ui.md
- Before coding: write a short, numbered plan with explicit:
  - What repo/branch;
  - What files to change;
  - Which specs/tests to update;
  - Which SPEC DIFFs you rely on.
- After each change:
  - Run minimal relevant tests (dotnet test, npm test, playwright);
  - Note exact commands and outcomes in artifacts (issuer-dashboard-and-reports.md, issuance-test-report.txt, etc.);
  - Call out any remaining SPEC DIFFs or TODOs.

If something in specs vs code conflicts, DO NOT guess. Prefer:
- Quote the relevant openapi/asyncapi fragment (path/topic/schema).
- Show the actual code (Program.cs/controller/service).
- Explicitly mark the difference as SPEC DIFF and propose the minimal fix.
```

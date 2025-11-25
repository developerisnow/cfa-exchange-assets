# Objectives
- [ ] run locally full apps and check swaggers
- [ ] understand all deeply for future finalization CI/CD gitlab pipeline

## Context (eywa1 main workspace, d792 log 20251125-1201)
- Swagger на cfa1: gateway/identity 200; issuance/registry/settlement/compliance 404 (образы без Swagger секции). Нужно пересобрать образы с `Swagger__Enabled=true` и `Kafka__Enabled=false` для стабильности, затем прогнать Playwright swagger-all-services.
- AsyncAPI валиден (warn задокументированы), compliance dotnet tests проходили. Kafka на cfa1 временно выключали из-за MassTransit падений.
- Ветка: `codex/fix-cfa1-regressions` (не ребейзить на develop, конфликты решает Илья).

## Questions → Answers
- [ ] before start must be in context what's done on a main workspace `eywa1` (ubuntu vps server by other codex-cli agent `d792` @/Users/user/Backups/tmux/eywa1/p-cfa/eywa1-p-cfa-w16.p1-20251125-1201.session.txt )
  - См. Context выше: Swagger частично 200 (gateway/identity), остальное требует пересборки; AsyncAPI валиден; Kafka временно off; ветка `codex/fix-cfa1-regressions`.
- [ ] `make seed` - nothing happens, why?
  - Таргет в Makefile: `docker-compose exec api-gateway dotnet run --project services/seed -- seed-db`. Если контейнер `api-gateway` не запущен (`docker-compose up` не делали) или сервис стартует долго, команда молчит до старта/ошибки. Проверь `docker ps` на наличие `api-gateway`; если контейнера нет, `docker-compose exec` завершится с ошибкой (видно по `$?`). Для явной диагностики: `docker-compose exec api-gateway dotnet run --project services/seed -- seed-db -v` или добавить `set -x`/`-T`.
- [ ] `make e2e`  error
  - В указанных логах нет вывода `make e2e`; нужно перезапустить и зафиксировать stderr. Подозрение: либо зависимости Playwright не установлены, либо переменные окружения (BASE_URL/creds) не заданы.
- [ ] `make generate-sdks`  error @/Users/user/Backups/tmux/local/p-cfa/local-p-cfa-w2.p2-20251125-1155-1.session.txt
  - Ошибка из openapi-generator: дублированные пути `/v1/complaints` и `/v1/complaints/{id}` + отсутствующие схемы `KycTask`, `ComplaintReplyRequest`, `ComplaintResolveRequest`. Source: `packages/contracts/openapi-gateway.yaml` (см. spectral и generator stacktrace). Нужно починить контракты перед генерацией.
- [ ] `curl http://localhost:5000/health` - empty output means what, is it run? how to clearly check result?
  - Пустой stdout означает, что curl не показал тело; важен код. Используй `curl -i -w "\nHTTP:%{http_code}\n" http://localhost:5000/health`. Если сервис не отвечает — будет timeout/connection refused; если 200 с пустым телом — сервис жив, но health endpoint без body. Можно смотреть `docker-compose logs api-gateway` для подтверждения.
- [ ] `make validate-specs` has error, explain details in terms of knowing existing session log
  - После установки `@stoplight/spectral-cli` ошибка:  
    - `#/components/schemas/KycTask` отсутствует.  
    - Дубликаты путей `/v1/complaints`, `/v1/complaints/{id}`.  
    - Отсутствуют схемы `ComplaintReplyRequest`, `ComplaintResolveRequest`.  
    Это блокирует и `make generate-sdks`.

# JTBD Jobs
- J1: Локально поднять стек (compose) и убедиться, что health + Swagger отвечают (gateway + core services).
- J2: Разрулить ошибки контрактов, чтобы `make validate-specs` и `make generate-sdks` проходили.
- J3: Понять/починить `make e2e` на локали (зависимости, env), подготовить к CI/CD.

# DoD of JTBDs
- D1 (for J1): `make health` зелёный; `curl -i http://localhost:5000/health` даёт 200; Swagger локально открывается на сервисах (или честно задокументирован недоступен).
- D2 (for J2): `make validate-specs` 0 exit; `make generate-sdks` проходит; контракты без дубликатов путей и с заполненными схемами.
- D3 (for J3): `make e2e` отрабатывает с корректно настроенными env (или зафиксирован список блокеров/недостающих deps); плейрайнт/витест зависимости установлены.

# Kickoff of DoDs
- K1 (J1): `docker-compose up -d` (base services) → `docker ps` проверить `api-gateway`/core → `curl -i -w "\nHTTP:%{http_code}\n" http://localhost:5000/health` → открыть локальные `/swagger` (gateway/core).
- K2 (J2): Открыть `packages/contracts/openapi-gateway.yaml`, удалить дубли `/v1/complaints*`, добавить схемы `KycTask`, `ComplaintReplyRequest`, `ComplaintResolveRequest` → `make validate-specs` → `make generate-sdks`.
- K3 (J3): Проверить `make e2e` вывод (указать BASE_URL/creds) → при необходимости `npm ci` в `tests/e2e-playwright` и установить Playwright browsers → зафиксировать pass/fail и причины.

# K1 progress (2025-11-25)
- Выполнено: base infra уже была запущена (kafka/zookeeper/postgres/keycloak/minio/redis).  
- Попытка `docker compose -f docker-compose.yml -f docker-compose.services.yml up -d ...` (с и без `--no-deps`) завершилась ошибкой сборки .NET образов:  
  - global.json требует SDK `9.0.109`, а базовый образ `mcr.microsoft.com/dotnet/sdk:9.0` содержит `9.0.308` → сборка `api-gateway` и `bank-nominal` падает `SDK not found` (exit 145).  
  - `bank-nominal` тянется как depends_on для compliance; даже при `--no-deps` сборка gateway упала на той же проблеме с SDK.  
- Итог: сервисы (`api-gateway`, `identity`, `issuance`, `registry`, `settlement`, `compliance`) не собраны/не подняты, health/Swagger проверить нельзя до решения SDK версии.

### K1 unblock plan
- Обновить образ SDK в Dockerfile-ах на тег с 9.0.1xx/9.0.109 (или установить нужный SDK через dotnet-install).  
- Альтернатива: добавить `DOTNET_ROLL_FORWARD=Major` (или `latestMajor`) в build-env, если допустимо, чтобы 9.0.308 удовлетворил global.json.  
- Временный обход: исключить `bank-nominal` из depends_on для локального запуска и использовать образ SDK с нужной версией для gateway/services.

# K1 progress update (2025-11-25, later)
- Сделано:  
  - global.json скорректирован на 9.0.100; все Dockerfile .NET переведены на `mcr.microsoft.com/dotnet/sdk:9.0.100` + `DOTNET_ROLL_FORWARD=LatestMajor`.  
  - `bank-nominal` закомментирован в compose (и убран из depends_on settlement) для ускорения локального старта.  
  - `docker compose ... build api-gateway identity-service issuance-service registry-service settlement-service compliance-service` — успешно.  
  - `docker compose ... up -d` для сервисов — успешно, health 200:  
    - gateway 55000, identity 55001, issuance 55005, registry 55006, compliance 55008.  
  - Добавлены `ASPNETCORE_ENVIRONMENT=Development` + `Swagger__Enabled=true` + `DisableHttpsRedirection=true` в compose для всех сервисов; после перезапуска `/swagger/index.html` → HTTP 200 на 55000/55001/55005/55006/55008.  
- Что осталось по K1: на ветке main или другой compose без этих env по-прежнему 404 (см. вывод пользователя). Нужно либо перенести env/флаг в основной compose, либо включить Swagger в код (по флагу). Health локально пройден. 

## K1/K3 локальная проверка UI + Keycloak (2025-11-25 Codex)
- PM2 очищен (`pm2 delete all && pm2 flush`), фронты запущены по одному c env: `NEXT_PUBLIC_API_BASE_URL=http://localhost:55000`, `NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:58080`, `KEYCLOAK_INTERNAL_URL=http://localhost:58080`, `NEXT_PUBLIC_KEYCLOAK_REALM=ois`, `NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=<portal-issuer|portal-investor|backoffice>`, `KEYCLOAK_CLIENT_SECRET=secret`, `NEXTAUTH_URL=http://localhost:<3001|3002|3003>`. PM2 статус: portal-issuer@3001, portal-investor@3002, backoffice@3003 — online.  
- Исправлена сборка фронтов: после `npm install` в корне подтянулся `autoprefixer`; собран `apps/shared-ui` (`npm run build --workspace apps/shared-ui`) → ошибка “Cannot find module '@ois/shared-ui'” снята.  
- Keycloak: создан realm `ois`; клиенты `portal-issuer`/`portal-investor`/`backoffice` (confidential, secret=secret, redirect `http://localhost:300{1,2,3}/api/auth/callback/keycloak`, web origins `http://localhost:300{1,2,3}`), роли `issuer`/`investor`/`backoffice`. Пользователи: `issuer@demo.local`/`investor@demo.local`/`backoffice@demo.local` пароли `demo123`, emailVerified=true, first/last name заполнены, роли выданы.  
- Проверка авторизации: password grant через `/realms/ois/protocol/openid-connect/token` успешен для всех клиентов/пользователей (получены access_token/refresh_token). Фронты отвечают 307 на `/auth/signin` (редирект на Keycloak). 

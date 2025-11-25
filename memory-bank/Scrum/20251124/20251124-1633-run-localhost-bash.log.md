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

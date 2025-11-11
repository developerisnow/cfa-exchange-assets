---
created: 2025-11-11 14:40
updated: 2025-11-11 14:40
type: runbook
sphere: [finance, blockchain]
topic: [local-deploy, ois-cfa]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [junior, step-by-step, macos, ubuntu]
---

# OIS‑CFA — Local Deploy Runbook (macOS + Ubuntu)

## TL;DR
- Инфраструктура (Postgres, Kafka, Keycloak, Minio) — через `docker-compose`.
- Бэкенды .NET — через `dotnet run` на фиксированных портах.
- API Gateway (YARP) — переопределяем адреса сервисов через env.

## 0) Пререквизиты
- macOS: Docker Desktop, Homebrew (`brew install jq curl node@20`), .NET 9 SDK (`brew install dotnet@9`), npm (Node 20).
- Ubuntu: Docker, Docker Compose plugin, curl, jq, Node 20 (опционально), .NET 9 SDK (если запускать сервисы не в контейнерах).

## 1) Запускаем инфраструктуру
```bash
cd /Users/user/__Repositories/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa
docker-compose up -d

# Проверка
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Сервисы и порты:
- Postgres 16: 5432/tcp
- Kafka 3.6 + Zookeeper 7.5: 9092, 2181 (на Apple Silicon может работать медленнее)
- Keycloak 25.0: 8080/tcp
- Minio: 9000/9001/tcp

## 2) Фиксируем порты приложений
Выберем порты (совпадают с OpenAPI servers):
- Gateway: 5000
- Identity: 5001
- ESIA Adapter: 5002
- Bank Nominal: 5003
- EDO Connector: 5004
- Issuance: 5005
- Registry: 5006
- Settlement: 5007
- Compliance: 5008

## 3) Переопределяем кластеры YARP (Gateway)
Запускаем Gateway так, чтобы кластеры указывали на `localhost` порты:
```bash
export ReverseProxy__Clusters__identity__Destinations__default__Address=http://localhost:5001
export ReverseProxy__Clusters__issuance__Destinations__default__Address=http://localhost:5005
export ReverseProxy__Clusters__registry__Destinations__default__Address=http://localhost:5006
export ReverseProxy__Clusters__settlement__Destinations__default__Address=http://localhost:5007
export ReverseProxy__Clusters__compliance__Destinations__default__Address=http://localhost:5008

export ASPNETCORE_URLS=http://localhost:5000
dotnet run --project apps/api-gateway
```

## 4) Запускаем .NET сервисы (каждый в отдельном терминале)
```bash
# Identity (OIDC mock)
export ASPNETCORE_URLS=http://localhost:5001
dotnet run --project services/identity

# ESIA Adapter (mock)
export ASPNETCORE_URLS=http://localhost:5002
dotnet run --project services/integrations/esia-adapter

# Bank Nominal (mock)
export ASPNETCORE_URLS=http://localhost:5003
dotnet run --project services/integrations/bank-nominal

# EDO Connector (mock)
export ASPNETCORE_URLS=http://localhost:5004
dotnet run --project services/integrations/edo-connector

# Issuance
export ASPNETCORE_URLS=http://localhost:5005
dotnet run --project services/issuance

# Registry
export ASPNETCORE_URLS=http://localhost:5006
dotnet run --project services/registry

# Settlement
export ASPNETCORE_URLS=http://localhost:5007
dotnet run --project services/settlement

# Compliance
export ASPNETCORE_URLS=http://localhost:5008
dotnet run --project services/compliance
```

## 5) Проверка (health + Swagger)
```bash
# Health
curl -s http://localhost:5000/health | jq .

# Swagger UI
open http://localhost:5000/swagger
open http://localhost:5001/swagger
open http://localhost:5005/swagger
open http://localhost:5006/swagger
open http://localhost:5007/swagger
open http://localhost:5008/swagger
```

## 6) Быстрый smoke (без аутентификации)
```bash
# Create issuance (через Gateway → Issuance)
curl -s -X POST http://localhost:5000/issuances \
  -H 'Content-Type: application/json' \
  -d '{"assetId":"00000000-0000-0000-0000-000000000000","issuerId":"00000000-0000-0000-0000-000000000000","totalAmount":1000,"nominal":100,"issueDate":"2025-01-01","maturityDate":"2025-12-31"}' | jq .

# Place order (Idempotency-Key обязателен)
curl -s -X POST http://localhost:5000/v1/orders \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 11111111-1111-1111-1111-111111111111' \
  -d '{"investorId":"00000000-0000-0000-0000-000000000001","issuanceId":"00000000-0000-0000-0000-000000000000","amount":100}' | jq .

# Wallet
curl -s http://localhost:5000/v1/wallets/00000000-0000-0000-0000-000000000001 | jq .

# Settlement run
curl -s -X POST http://localhost:5000/v1/settlement/run | jq .
```

## 7) Частые проблемы
- Kafka на Apple Silicon может работать медленно (образ `apache/kafka:3.6` без native arm64) — допустимо для dev; для стабильности используйте Ubuntu сервер (CFA1).
- `make seed` — место‑держатель: контейнера `api-gateway` в compose нет, `services/seed` отсутствует. Используйте ручной smoke (см. выше).
- Keycloak в dev не требует realm для mock Identity сервиса; для реального OIDC — см. ESIA/OIDC sequence в docs.

## 8) Альтернатива: удалённый сервер (CFA1, Ubuntu)
- Плюсы: стабильные образы, выше производительность Kafka/Keycloak/Postgres.
- Минусы: нужен SSH, проброс портов или nginx.

Шаги идентичны: ставите Docker, поднимаете `docker-compose up -d`, запускаете .NET сервисы с фиксированными `ASPNETCORE_URLS`, настраиваете Gateway через `ReverseProxy__Clusters__*` env.

## Ссылки
- Репозиторий: repositories/customer-gitlab/ois-cfa
- OpenAPI/AsyncAPI: repositories/customer-gitlab/ois-cfa/packages/contracts
- DoD MVP: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1413-dod-mvp-ois-cfa.md

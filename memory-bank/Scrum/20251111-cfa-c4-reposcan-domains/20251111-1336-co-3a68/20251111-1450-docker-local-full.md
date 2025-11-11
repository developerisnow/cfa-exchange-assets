---
created: 2025-11-11 14:50
updated: 2025-11-11 14:50
type: runbook
sphere: [finance, blockchain]
topic: [docker-compose, local-deploy]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [checklist, commands, keycloak, ports]
---

# Local Docker Deploy — Full Checklist + Commands

## Before you start
- [ ] Свободное место: ≥ 10–12 GB
  - Образы: dotnet runtime+sdk, keycloak, postgres, kafka, zookeeper, minio ≈ 6–8 GB
  - Томa: pgdata, minio ≈ 1–2 GB (растут)
- [ ] Docker Desktop (macOS) / Docker Engine+Compose (Ubuntu)
- [ ] Порт‑конфликты проверены (используем нестандартные)

## 0) Переходим в репозиторий
```bash
cd /Users/user/__Repositories/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa
```

## 1) Переменные окружения (.env)
- Файл создан: `repositories/customer-gitlab/ois-cfa/.env`
- Проверить/править при необходимости (порты/креды):
```bash
cat .env
```

Ключевые значения:
- Postgres: `${POSTGRES_USER}/${POSTGRES_PASSWORD}` на порту `${POSTGRES_HOST_PORT}`
- Keycloak admin: `${KEYCLOAK_ADMIN}/${KEYCLOAK_ADMIN_PASSWORD}` на `http://localhost:${KEYCLOAK_HOST_PORT}`
- Gateway/Services порты: `${GATEWAY_HOST_PORT}`, `${ISSUANCE_HOST_PORT}`, …

## 2) Поднимаем инфраструктуру + сервисы
```bash
docker compose \
  -f docker-compose.yml \
  -f docker-compose.override.yml \
  -f docker-compose.services.yml \
  up -d --build
```

Проверка контейнеров:
```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

## 3) Админки и эндпоинты (URL)
- Gateway Swagger: http://localhost:${GATEWAY_HOST_PORT}/swagger
- Identity Swagger: http://localhost:${IDENTITY_HOST_PORT}/swagger
- Issuance Swagger: http://localhost:${ISSUANCE_HOST_PORT}/swagger
- Registry Swagger: http://localhost:${REGISTRY_HOST_PORT}/swagger
- Settlement Swagger: http://localhost:${SETTLEMENT_HOST_PORT}/swagger
- Compliance Swagger: http://localhost:${COMPLIANCE_HOST_PORT}/swagger
- Keycloak: http://localhost:${KEYCLOAK_HOST_PORT}
  - Admin: `${KEYCLOAK_ADMIN}/${KEYCLOAK_ADMIN_PASSWORD}`
- Minio Console: http://localhost:${MINIO_CONSOLE_PORT} (user/pass: `${MINIO_ROOT_USER}/${MINIO_ROOT_PASSWORD}`)

Health:
```bash
curl -s http://localhost:${GATEWAY_HOST_PORT}/health | jq .
```

## 4) Smoke сценарии (без auth)
```bash
# Create issuance
curl -s -X POST http://localhost:${GATEWAY_HOST_PORT}/issuances \
  -H 'Content-Type: application/json' \
  -d '{"assetId":"00000000-0000-0000-0000-000000000000","issuerId":"00000000-0000-0000-0000-000000000000","totalAmount":1000,"nominal":100,"issueDate":"2025-01-01","maturityDate":"2025-12-31"}' | jq .

# Place order (idempotent)
curl -s -X POST http://localhost:${GATEWAY_HOST_PORT}/v1/orders \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: 11111111-1111-1111-1111-111111111111' \
  -d '{"investorId":"00000000-0000-0000-0000-000000000001","issuanceId":"00000000-0000-0000-0000-000000000000","amount":100}' | jq .

# Wallet
curl -s http://localhost:${GATEWAY_HOST_PORT}/v1/wallets/00000000-0000-0000-0000-000000000001 | jq .

# Settlement run
curl -s -X POST http://localhost:${GATEWAY_HOST_PORT}/v1/settlement/run | jq .
```

## 5) Логи и отладка
```bash
# Все логи контейнера
docker logs -f api-gateway
docker logs -f issuance-service
docker logs -f registry-service
docker logs -f settlement-service
docker logs -f compliance-service
docker logs -f identity-service

# Инфраструктура
docker logs -f ois-postgres
docker logs -f ois-kafka
docker logs -f ois-keycloak

# Диск
docker system df
docker volume ls
```

## 6) Остановка и очистка
```bash
docker compose \
  -f docker-compose.yml \
  -f docker-compose.override.yml \
  -f docker-compose.services.yml \
  down

# (опц.) удалить тома БД/Minio
docker compose -f docker-compose.yml down -v
```

## Примечания
- Для ускорения на macOS (Apple Silicon) рекомендуются Linux‑сервера (CFA1) для Kafka/Keycloak/Postgres.
- Fabric/ledger отключён (Ledger__UseMock=true) — включим отдельно, когда будет готов gateway/k8s‑сеть.
- Seed цель в Makefile — placeholder; используйте smoke выше.


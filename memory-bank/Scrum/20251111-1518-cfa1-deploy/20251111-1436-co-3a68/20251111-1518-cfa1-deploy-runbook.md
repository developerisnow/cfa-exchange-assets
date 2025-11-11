---
created: 2025-11-11 15:18
updated: 2025-11-11 15:18
type: runbook
sphere: [devops]
topic: [remote-deploy, docker, ubuntu]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [checklist, cfa1, ssh, logs]
---

# CFA1 Deploy — Docker Infra + Services (SSH)

## Host
- Alias: `cfa1` (87.249.49.56, Ubuntu, root)
- FS: `/` free 26G

## Checklist
- [x] SSH доступ (root)
- [x] Установка Docker + Compose plugin
- [x] Rsync проекта /opt/ois-cfa (без .git)
- [x] Kafka override (Confluent image)
- [ ] docker compose up (rate-limit hub → нужен docker login)

## Commands + Output (key excerpts)

1) Проверка SSH и среды
```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 cfa1 'echo REMOTE_OK && uname -a && id -u && command -v docker || echo NO_DOCKER'
# REMOTE_OK
# Linux ... x86_64 GNU/Linux
# 0
# NO_DOCKER
```

2) Установка Docker CE и compose plugin
```bash
ssh cfa1 'export DEBIAN_FRONTEND=noninteractive; \
  apt-get update -y && apt-get install -y ca-certificates curl gnupg lsb-release jq && \
  install -m 0755 -d /etc/apt/keyrings && \
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
  chmod a+r /etc/apt/keyrings/docker.gpg && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) stable" > /etc/apt/sources.list.d/docker.list && \
  apt-get update -y && \
  apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
  systemctl enable docker && systemctl start docker && docker version'
# ... Docker Engine - Community 29.0.0 (client/server)
```

3) Дисковое пространство
```bash
ssh cfa1 'df -h / | tail -1; docker system df || true'
# /dev/sda1 29G total, 26G free
```

4) Rsync проекта на сервер
```bash
rsync -avz --delete --exclude '.git' --exclude 'apps/*/node_modules' --exclude '*/bin' --exclude '*/obj' \
  repositories/customer-gitlab/ois-cfa/ cfa1:/opt/ois-cfa/
```

5) Kafka override (Docker Hub apache/kafka:3.6 недоступен)
```bash
# Добавлен override: docker-compose.kafka.override.yml (confluentinc/cp-kafka:7.5.0)
rsync -avz repositories/customer-gitlab/ois-cfa/docker-compose.kafka.override.yml cfa1:/opt/ois-cfa/
```

6) Подъём стеков (infra + services)
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose \
  -f docker-compose.yml \
  -f docker-compose.override.yml \
  -f docker-compose.kafka.override.yml \
  -f docker-compose.services.yml \
  up -d --build'
# FAIL: error from registry: You have reached your unauthenticated pull rate limit.
```

## Next steps (action required)
- Выполнить на `cfa1` авторизацию Docker Hub (или задать mirror):
```bash
ssh cfa1
docker login  # ввести Docker Hub creds
exit
```
- Повторить поднятие:
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose \
  -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d --build'
```

## URLs (после запуска)
- Gateway Swagger: http://<server-ip>:${GATEWAY_HOST_PORT:-55000}/swagger
- Identity Swagger: http://<server-ip>:${IDENTITY_HOST_PORT:-55001}/swagger
- Issuance Swagger: http://<server-ip>:${ISSUANCE_HOST_PORT:-55005}/swagger
- Registry Swagger: http://<server-ip>:${REGISTRY_HOST_PORT:-55006}/swagger
- Settlement Swagger: http://<server-ip>:${SETTLEMENT_HOST_PORT:-55007}/swagger
- Compliance Swagger: http://<server-ip>:${COMPLIANCE_HOST_PORT:-55008}/swagger
- Keycloak: http://<server-ip>:${KEYCLOAK_HOST_PORT:-58080} (admin/admin123)
- Minio Console: http://<server-ip>:${MINIO_CONSOLE_PORT:-59001} (minioadmin/minioadmin)

## Notes
- Порты/креды заданы в /opt/ois-cfa/.env (нестандартные, чтобы избегать конфликтов).
- Ledger (Fabric) отключён (UseMock=true) для dev.
- Seed в Makefile — placeholder, используйте smoke (curl) из локального runbook.


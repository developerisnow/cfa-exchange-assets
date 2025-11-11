---
created: 2025-11-11 17:26
updated: 2025-11-11 17:56
type: runbook
sphere: [devops, sre]
topic: [deploy, docker, cfa1]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [compose, dotnet, low-ram, swap]
---

# CFA1 Deploy — Runbook (Dev Compose)

## Context
- Host: `cfa1` (Ubuntu 6.8 kernel), RAM ~2GB, no swap initially.
- Path: `/opt/ois-cfa` (contains repo snapshot, not a git clone).
- Compose files: `docker-compose.yml`, `docker-compose.override.yml`, `docker-compose.kafka.override.yml`, `docker-compose.services.yml`.
- Env: `.env` with non‑standard ports (see AGENTS.md).

## Steps Executed

1) Baseline checks
```bash
ssh cfa1 'uname -a && df -hT | sed -n "1,10p" && docker --version && docker compose version'
```

2) Add 2G swap (low‑RAM mitigation for .NET builds)
```bash
ssh cfa1 'fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048; chmod 600 /swapfile; mkswap /swapfile; swapon /swapfile; echo "/swapfile none swap sw 0 0" >> /etc/fstab'
```

3) Infra up (Postgres, Kafka/ZooKeeper, Keycloak, Minio)
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml up -d'
ssh cfa1 'docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
# Result: postgres healthy, zookeeper/kafka up, keycloak up (58080), minio healthy (59000/59001)
```

4) Identity service (build + up)
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build identity-service && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d identity-service'
ssh cfa1 'curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55001/health'  # 200
```

5) Registry service (fix + build + up)
- Code change: removed hardcoded `MigrationsAssembly("OIS.Registry")` and gated migrations by `MIGRATE_ON_STARTUP`.
```bash
rsync -az --delete repositories/customer-gitlab/ois-cfa/ cfa1:/opt/ois-cfa/
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build --no-cache registry-service && MIGRATE_ON_STARTUP=false docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d registry-service'
ssh cfa1 'curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55006/health'  # 200
```

6) Compliance service (build + up)
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build compliance-service && MIGRATE_ON_STARTUP=false docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d compliance-service'
ssh cfa1 'curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55008/health'  # 503 (expected until health checks implemented)
```

7) Issuance/Settlement (build + up)
- Fixes committed:
  - `issuance.csproj`: add `Polly` dependency.
  - Remove hardcoded `MigrationsAssembly` + gate migrations by env in `issuance/settlement`.
- Next:
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build --no-cache issuance-service && MIGRATE_ON_STARTUP=false docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d --force-recreate issuance-service && curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55005/health'
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build settlement-service && MIGRATE_ON_STARTUP=false docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d settlement-service && curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55007/health'
```

8) API Gateway (after all services)
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build api-gateway && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d api-gateway && curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55000/health'

9) YARP route fix (redeem)
- Error: YARP invalid path '/v1/issuances/{**catch-all}/redeem'.
- Fix: change to '/v1/issuances/{id}/redeem' in `apps/api-gateway/appsettings.json`.
```bash
ssh cfa1 'cd /opt/ois-cfa && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml build api-gateway && docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml up -d --force-recreate api-gateway && curl -sS -o /dev/null -w "%{http_code}\n" http://localhost:55000/health'
```
```

## Current Status Snapshot
```txt
identity-service   → 200 /health
registry-service   → 200 /health
issuance-service   → 503 /health (service running)
settlement-service → 503 /health (service running)
compliance-service → 503 /health (service running)
api-gateway        → 200 /health
keycloak          → http://<cfa1-ip>:58080 (admin/admin123)
minio             → http://<cfa1-ip>:59001 (minioadmin/minioadmin)
kafka/zookeeper   → up; postgres healthy
```

## Notes / Troubleshooting
- If DB connect flaps at startup, confirm `MIGRATE_ON_STARTUP=false` and retry container.
- If builds OOM, verify swap active (`free -m`) and build services sequentially.
- Health endpoints: `/health` on each service port above. Logs: `docker logs -f <container>`.
 - External access: cloud firewall may block high ports. For mac testing, use SSH port forwards:
   - `ssh -N -L 155000:localhost:55000 -L 155001:localhost:55001 -L 155006:localhost:55006 -L 158080:localhost:58080 cfa1-mux`
   - Then open `http://localhost:155000/health`, `http://localhost:155001/health`, `http://localhost:155006/health`, Keycloak: `http://localhost:158080/`.

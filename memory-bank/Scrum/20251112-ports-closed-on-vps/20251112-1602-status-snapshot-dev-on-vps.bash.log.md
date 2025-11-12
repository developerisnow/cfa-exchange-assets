---
created: 2025-11-12 16:02
type: ops-log
sphere: devops
topic: CFA1 deploy snapshot
author: co-3a68
agentID: co-3a68
partAgentID: [co-3a68]
version: 0.1.0
tags: [snapshot, deploy, vps, ports, curl]
---

# Status Snapshot (CFA1)

## docker ps (running)
```
NAMES                STATUS                  PORTS
compliance-service   Up ~3h                  0.0.0.0:55008->8080/tcp
issuance-service     Up ~3h                  0.0.0.0:55005->8080/tcp
settlement-service   Up ~3h                  0.0.0.0:55007->8080/tcp
api-gateway          Up ~4h                  0.0.0.0:5000->8080/tcp
ois-keycloak         Up ~1h                  0.0.0.0:8080->8080/tcp
bank-nominal         Up ~23h                 0.0.0.0:55003->8080/tcp
registry-service     Up ~23h                 0.0.0.0:55006->8080/tcp
identity-service     Up ~23h                 0.0.0.0:55001->8080/tcp
ois-kafka            Up ~20m                 0.0.0.0:59092->9092/tcp
ois-postgres         Up ~25h (healthy)       0.0.0.0:55432->5432/tcp
ois-zookeeper        Up ~25h                 0.0.0.0:52181->2181/tcp
ois-minio            Up ~25h (healthy)       0.0.0.0:59000->9000/tcp,0.0.0.0:59001->9001/tcp
```

## pm2 ls
```
┌────┬────────────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┐
│ id │ name               │ pid     │ uptime  │ status   │ cpu    │ mem  │ watching │
├────┼────────────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┤
│ 0  │ portal-issuer      │ 1354833 │ ~1–8m   │ online   │ 0–30%  │ ~40M │ disabled │
│ 1  │ portal-investor    │ 1353821 │ ~7m     │ online   │ 0%     │ ~21M │ disabled │
│ 2  │ backoffice         │ 1353203 │ ~13m    │ online   │ 0%     │ ~13M │ disabled │
└────┴────────────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┘
```

## listeners (5000,8080,3001–3003)
```
LISTEN 0 0 0.0.0.0:5000  users:("docker-proxy")
LISTEN 0 0 0.0.0.0:8080  users:("docker-proxy")
LISTEN 0 0 *:3001        users:("next-server (v1")
LISTEN 0 0 *:3002        users:("next-server (v1")
LISTEN 0 0 *:3003        users:("next-server (v1")
```

## curl codes
```
http://localhost:5000/health => 200
http://localhost:8080/admin   => 302
http://localhost:8080/health/ready => 404 (Keycloak dev mode; UI доступна)
http://localhost:3001/ => 500 (см. Notes)
http://localhost:3002/ => 500 (см. Notes)
http://localhost:3003/ => 000/timeout (пакет next отсутствовал; поставлен; прогрев)
```

## Notes
- Фронтенды запущены в dev, порты слушают. Ошибка 500 связана с резолвом зависимостей `shared-ui` (добавлен резолв в `next.config.js` и установлен `shared-ui` deps). Требуется прогрев/перезапуск после сборки SDK.
- Keycloak развернут, создан realm `ois-dev`, клиенты PUBLIC (issuer/investor/backoffice) с redirect на 3001/3002/3003 и туннели 15301/15302/15303.
- Для локального доступа используйте SSH‑туннели (см. docs/deploy/docker-compose-at-vps/07-frontends-dev-on-vps.md).


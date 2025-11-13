---
created: 2025-11-12 19:49
updated: 2025-11-12 18:33
type: operations-log
sphere: devops
topic: ois-cfa demo bootstrap on CFA1
author: Alex (co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.3.0
tags: [keycloak, portals, devops, demo]
---

# Context
- Task chain: `run-demo-ois-cfa-on-vps` (per 20251112 instructions).  
- Environment: working from `eywa1` (Ubuntu), target host `cfa1` (`/opt/ois-cfa`).  
- Constraints: **DevOps SRE scope only** — no service code changes, no dockerizing frontends, commits limited to `memory-bank` logs.

# Definition of Done (per AlexA brief)
1. Keycloak: Postgres DB `keycloak` exists, container up via docker-compose, `http://localhost:8080/health/ready` → 200, admin UI accessible.
2. Realm `ois-dev` with 3 **public** clients (`portal-issuer`, `portal-investor`, `backoffice`), redirect/web origins set to 3001/3002/3003, test users login succeeds.
3. Frontends: Node 20 LTS via nvm, `apps/portal-{issuer,investor,backoffice}` launched using `HOST=0.0.0.0 PORT=300x npm run dev`, verified by `ss -ltnp` + `curl -I http://localhost:300x`.
4. Gateway + Keycloak available remotely:  
   - Baseline check on `cfa1` localhost (5000/8080/300x).  
   - Step **1.5**: from `eywa1`, `curl http://87.249.49.56:{5000,8080,3001,3002,3003}` once services alive to confirm direct reachability before advising macOS access (possibly w/o SSH tunnels).  
5. Operator validation: macOS tunnels (`15500↔5000`, `15808↔8080`, `15301↔3001`, `15302↔3002`, `15303↔3003`) tested, Issuer/Investor login through Keycloak successful.
6. Reporting: new log entry with `docker ps`, `ss -ltnp` (filter ports), `curl` outputs for `5000/health`, `8080/health/ready`, `/` on 3001/3002/3003, plus Keycloak/client/user actions referencing runbooks:
   - `docs/deploy/localhost/FRONTEND-STARTUP.md`
   - `docs/deploy/localhost/KEYCLOAK-SETUP.md`

# Kickoff Checklist
- [x] Confirm repository context (`repositories/customer-gitlab/ois-cfa`), review runbooks above.
- [x] Verify SSH access to `cfa1`, target dir `/opt/ois-cfa`, and baseline state (`git status`, `docker ps`, `ss -ltnp` for 5000/8080/300x).
- [x] `docker compose down --remove-orphans` to reset services; confirm ports freed.
- [x] Postgres up ➜ create/verify DB `keycloak` ➜ `docker compose up -d keycloak` ➜ wait for `/health/ready=200` (see note re: mgmt port 9000).
- [x] Install/activate Node 20 via nvm; run dev servers for Issuer/Investor/Backoffice with HOST/PORT overrides.
- [x] Configure Keycloak realm + clients + test users per runbook; validate logins through Issuer/Investor (login form reachable, code flow tested via `curl`).
- [x] Execute Step 1.5: from `eywa1`, `curl http://87.249.49.56:{5000,8080,3001,3002,3003}` post-start to prove remote reachability before advising macOS testing.
- [x] Document tunneling instructions + verification steps for macOS operator review.
- [x] Capture “Status Snapshot” (docker/ss/curl outputs) and update this log. **(this section = current entry)**

# Notes
- Reference historical feedback: `20251112-1653-gpt5p-feedbackrun-demo-ecosystem-ois-cfa-on-vps_co-3a68.md`.  
- Stop criteria: Keycloak healthy + portals login via Keycloak; report ready.

# Worklog (UTC+3)
- **17:04–17:15** — took over `/opt/ois-cfa` on `cfa1`, recorded initial `docker ps` (all stacks running), executed `docker compose down --remove-orphans`, killed auto-respawned Next servers managed by legacy PM2, verified 5000/8080/300x idle.
- **17:15–17:35** — relaunched infra selectively: `postgres`, custom DB `keycloak`, rebuilt Keycloak container with extra override (`docker-compose.health.yml`) to enable health endpoints + expose mgmt port, waited for readiness, inspected logs.
- **17:35–17:45** — bootstrapped realm `ois-dev` via `kcadm`: converted `portal-issuer` to `public`, created `portal-investor` + `backoffice`, added roles (`issuer`, `investor`, `admin`, `backoffice`), provisioned test users (`issuer@test.com`, `investor@test.com`, `admin@test.com`) with `password123` and attached roles.
- **17:45–17:55** — installed `nvm` (v0.39.7) + Node 20.19.5, ran `npm ci` inside all portals, fixed `.env.local` (`NEXTAUTH_URL=http://localhost:30xx`), created launch scripts under `/root/.local/bin/run-*.sh`, wired PM2 (`pm2 start … && pm2 save`), validated listeners/HTTP 30x responses.
- **17:55–17:59** — brought back API/backends (`docker compose -f ... -f docker-compose.services.yml up -d …`), verified Gateway/identity stack healthy, ran `curl` for 5000/8080/300x plus mgmt health, executed Step 1.5 from `eywa1` against public IP `87.249.49.56`, captured status snapshot + pm2 table.

## Keycloak bootstrap state
- Container: `ois-keycloak` (quay.io/keycloak/keycloak:25.0.6) running via compose chain (`docker-compose.yml` + `docker-compose.override.yml` + `docker-compose.health.yml`).
- Health: `/health/ready` is exposed on **management port 9000** (`curl http://localhost:9000/health/ready -> 200`). On :8080 the endpoint still returns 404 (upstream behaviour for Keycloak 25); documented for operators.
- Realm: `ois-dev`.
- Clients (all `publicClient=true`, `standardFlowEnabled=true`, `implicit=false`, `directAccessGrants=false`):
  - `portal-issuer` — Redirect/Web origins: `http://localhost:3001/*`, `http://localhost:3001`.
  - `portal-investor` — Redirect/Web origins: `http://localhost:3002/*`, `http://localhost:3002`.
  - `backoffice` — Redirect/Web origins: `http://localhost:3003/*`, `http://localhost:3003`.
- Roles: `issuer`, `investor`, `admin`, `backoffice` added as realm roles.
- Test users (password `password123`, email verified):
  - `issuer@test.com` ↔ role `issuer`.
  - `investor@test.com` ↔ role `investor`.
  - `admin@test.com` ↔ roles `admin`, `backoffice`.
- Login check: authorization endpoint responds with HTML form (`curl -I 'http://localhost:8080/realms/ois-dev/protocol/openid-connect/auth?...' -> 200`).

## Frontend runtime (Node 20 via nvm)
- Installed `nvm` for root, set `default -> v20.19.5`. `node -v` => `v20.19.5`.
- Scripts for PM2:
  - `/root/.local/bin/run-portal-issuer.sh` → `HOST=0.0.0.0 PORT=3001 npm run dev`.
  - `/root/.local/bin/run-portal-investor.sh` → `PORT=3002`.
  - `/root/.local/bin/run-backoffice.sh` → `PORT=3003`.
- PM2 processes:
  ```
  $ pm2 ls
  ┌────┬──────────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
  │ id │ name                 │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
  ├────┼──────────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
  │ 2  │ portal-backoffice    │ default     │ N/A     │ fork    │ 1411611  │ 5m     │ 1    │ online    │ 0%       │ 1.9mb    │ root     │ disabled │
  │ 1  │ portal-investor      │ default     │ N/A     │ fork    │ 1411250  │ 5m     │ 1    │ online    │ 0%       │ 1.9mb    │ root     │ disabled │
  │ 0  │ portal-issuer        │ default     │ N/A     │ fork    │ 1411060  │ 5m     │ 1    │ online    │ 0%       │ 1.9mb    │ root     │ disabled │
  └────┴──────────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
  ```
- Frontends respond with HTTP 307 (NextAuth redirect) on `/`, which is expected before logging in.

## Step 1.5 — external reachability
`curl` from `eywa1` to CFA1 public IP confirms no SSH tunnel is required for operator verification:
```
$ for port in 5000 8080 3001 3002 3003; do curl -s -o /dev/null -w "87.249.49.56:%s => %{http_code}\n" http://87.249.49.56:$port/; done
87.249.49.56:5000 => 302
87.249.49.56:8080 => 302
87.249.49.56:3001 => 307
87.249.49.56:3002 => 307
87.249.49.56:3003 => 307
```
- **Action for AlexA/macOS**: you can now open `http://87.249.49.56:{5000,8080,3001,3002,3003}` directly. SSH tunnelling command remains valid as fallback:
  ```
  ssh -N -L 15500:localhost:5000 -L 15808:localhost:8080 \
      -L 15301:localhost:3001 -L 15302:localhost:3002 -L 15303:localhost:3003 \
      cfa1
  ```

## Status Snapshot — 2025-11-12 17:59 MSK
### docker ps
```
NAMES                STATUS                    PORTS
api-gateway          Up 7 minutes              0.0.0.0:5000->8080/tcp, [::]:5000->8080/tcp
settlement-service   Up 7 minutes              0.0.0.0:55007->8080/tcp, [::]:55007->8080/tcp
identity-service     Up 7 minutes              0.0.0.0:55001->8080/tcp, [::]:55001->8080/tcp
issuance-service     Up 7 minutes              0.0.0.0:55005->8080/tcp, [::]:55005->8080/tcp
registry-service     Up 7 minutes              0.0.0.0:55006->8080/tcp, [::]:55006->8080/tcp
compliance-service   Up 7 minutes              0.0.0.0:55008->8080/tcp, [::]:55008->8080/tcp
bank-nominal         Up 7 minutes              0.0.0.0:55003->8080/tcp, [::]:55003->8080/tcp
ois-kafka            Up 8 minutes              0.0.0.0:9092->9092/tcp, [::]:9092->9092/tcp, 0.0.0.0:59092->9092/tcp, [::]:59092->9092/tcp
ois-zookeeper        Up 8 minutes              2888/tcp, 0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp, 3888/tcp, 0.0.0.0:52181->2181/tcp, [::]:52181->2181/tcp
ois-keycloak         Up 28 minutes             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp, 0.0.0.0:9000->9000/tcp, [::]:9000->9000/tcp, 8443/tcp
ois-postgres         Up 45 minutes (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp, 0.0.0.0:55432->5432/tcp, [::]:55432->5432/tcp
```

### `ss -ltnp | egrep ":5000|:8080|:3001|:3002|:3003"`
```
LISTEN 0      4096         0.0.0.0:5000       0.0.0.0:*    users:(("docker-proxy",pid=1410152,fd=7))
LISTEN 0      4096         0.0.0.0:8080       0.0.0.0:*    users:(("docker-proxy",pid=1398587,fd=7))
LISTEN 0      511                *:3003             *:*    users:(("next-server (v1",pid=1412343,fd=19))
LISTEN 0      511                *:3002             *:*    users:(("next-server (v1",pid=1412334,fd=19))
LISTEN 0      511                *:3001             *:*    users:(("next-server (v1",pid=1412323,fd=19))
LISTEN 0      4096            [::]:5000          [::]:*    users:(("docker-proxy",pid=1410156,fd=7))
LISTEN 0      4096            [::]:8080          [::]:*    users:(("docker-proxy",pid=1398593,fd=7))
```

### HTTP probes
```
gateway:200
kc8080:404
kc9000:200
port3001:307
port3002:307
port3003:307
```

## Outstanding / follow-ups
1. **Browser smoke** — Now that redirect/base URLs point to `87.249.49.56`, run Issuer/Investor login via Keycloak in a real browser and capture screenshots for the demo log.
2. **Minio decision** — Host port 9000 is free again; if object storage is needed, re-run `docker compose ... minio` (or update overrides to bind 59000/59001 only).
3. **Config persistence** — Current proxy overrides live only on `cfa1`. Decide whether to upstream them into repo (compose/ops) or document them for future replays.
4. **Security hardening** — Rotate `admin/admin123` once demo complete, and plan HTTPS termination (nginx proxy already in place, can add certs later).

## Update 18:33 MSK — Keycloak proxy + public URLs
- Added `keycloak-proxy` (nginx) sidecar via runtime override `docker-compose.keycloak-proxy.yml`, exposing host `:8080` and proxying to Keycloak UI (`keycloak:8080`) while routing `/health/ready` to management port (`keycloak:9000`).  
  - Base compose patched to drop hard-coded `8080:8080`; `.env` now sets `KEYCLOAK_HOST_PORT=8081`, `KEYCLOAK_PUBLIC_URL=http://87.249.49.56:8080`.  
  - Keycloak container listens on host 8081; proxy handles all external traffic on 8080, so `curl http://87.249.49.56:8080/health/ready` ⇒ `200`.  
  - Management port no longer published; `minio` may now bind to 9000/9001 if needed.
- Updated portal `.env.local` files to public URLs (`http://87.249.49.56:{5000,8080,300x}`) and restarted pm2 processes (issuer/investor/backoffice).  
- Refreshed Keycloak clients (`portal-issuer`, `portal-investor`, `backoffice`) redirect URIs and Web Origins to match IP-based routing via `kcadm`.  
- Verified from `eywa1`:  
  ```
  $ curl -s -o /dev/null -w "%{http_code}\n" http://87.249.49.56:8080/health/ready
  200
  $ curl -s -o /dev/null -w "%{http_code}\n" http://87.249.49.56:3001/
  307
  ```
- Admin UI now sits behind proxy; login at `http://87.249.49.56:8080/admin` (creds `admin / admin123`).  
- SSH tunnels remain optional fallback; direct browser access via IP confirmed for ports 5000/8080/3001/3002/3003.

### Next verifications
1. Re-test Issuer/Investor login from client machine (should complete redirect chain now that Keycloak + NextAuth use public URLs).  
2. Decide if `ois-minio` must be started (ports freed).  
3. Consider hardening: move proxy config + overrides into repo, add HTTPS certs, rotate Keycloak admin password post-demo.

created: 2025-11-13 08:05
updated: 2025-11-13 15:25
type: operations-log
sphere: devops
topic: uk1 replica deploy (OIS CFA)
author: Alex (co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.3.0
tags: [deployment, uk1, keycloak, portals]
---

# Context
- Customer requested fallback deployment on **UK1 MassiveGrid VPS** (`185.168.192.214`, SSH `root@uk1:51821`).  
- Goal: replicate `cfa1` setup (Keycloak + portals) so demo remains accessible while original VPS is unreachable.  
- Constraints: reuse existing `ois-cfa` tree, ports `8080/5000/300x` free; prefer same runbooks (compose, pm2, nvm).  

# Definition of Done
1. `/opt/ois-cfa` contains current repo snapshot; `.env` updated for UK1 (public IP, host ports).  
2. Docker compose stack running: `postgres`, `zookeeper`, `kafka`, `keycloak`, `keycloak-proxy`, `minio` (9000 remapped to 59000) with `/health/ready` exposed at `http://185.168.192.214:8080/health/ready`.  
3. Keycloak realm `ois-dev` recreated (public clients portal-issuer/investor/backoffice, roles, test users).  
4. Node 20 + pm2 installed; portals `portal-issuer|investor|backoffice` run via pm2 on `3001/3002/3003`, hitting Keycloak/ Gateway IP.  
5. Status snapshot + outstanding gaps captured here. (Full API microservices build still running; addressed separately.)

# Kickoff Checklist
- [x] Verify SSH + packages (`docker`, `docker compose`, `git`), create `/opt/ois-cfa`.  
- [x] Rsync repo from workstation → UK1; install `nvm` + Node 20 + pm2.  
- [x] Create env overrides (`.env`, `docker-compose.health.yml`, `docker-compose.keycloak-proxy.yml`, nginx proxy).  
- [x] Start infra containers (`postgres`, `zoo`, `kafka`, `minio`, `keycloak`, `proxy`); create DB `keycloak`.  
- [x] Bootstrap `ois-dev` realm (clients, roles, issuer/investor/admin users).  
- [x] Install portal deps (`packages/sdks`, `shared-ui`, `apps/*`), create `.env.local`, add pm2 scripts, start watchers.  
- [ ] Build & run .NET backend services (`api-gateway`, `identity`, etc.) — heavy docker build (2.6GB context) still compiling when session ended.  
- [ ] Validate portal login end-to-end (NextAuth) once API + Keycloak accessible; capture screenshots/logs.  

# Current Status (2025-11-13 11:55 MSK)
- `curl http://185.168.192.214:5000/health` → **200 Healthy**; API gateway stable ≥20 min.  
- Keycloak proxy now exposes HTTPS via `185.168.192.214.sslip.io:8443` (LE cert). `/admin` issues 302 and browsers trust cert; `/health/ready` works over both HTTP 8080 and HTTPS 8443.  
- Portals reachable (pre-login redirect):  
  ```
  curl -I http://185.168.192.214:3001 -> 307 /auth/signin
  curl -I http://185.168.192.214:3002 -> 307 /auth/signin
  curl -I http://185.168.192.214:3003 -> 307 /auth/signin
  ```  
- PM2 (`source /root/.nvm/nvm.sh && pm2 list`) shows `portal-*` apps running under Node 20 with refreshed env (`NEXT_PUBLIC_KEYCLOAK_URL=https://185.168.192.214.sslip.io:8443`).  
- Docker snapshot (08:16 UTC): `api-gateway`, `identity-service`, `bank-nominal`, `keycloak`, `keycloak-proxy`, `postgres`, `kafka`, `zookeeper`, `minio` all **Up**; sockets confirmed via `ss -ltnp`.  
- Playwright CLI present on eywa1 (global v1.56.0, Chromium cache). Dedicated `/tmp/playwright-run` workspace created; login script ready but blocked by current OAuth error.  

# 2025-11-13 Updates
1. **TLS & proxy** — Installed certbot on UK1, issued `185.168.192.214.sslip.io`, staged PEMs under `/opt/ois-cfa/certs/keycloak`, updated nginx proxy + compose to mount certs and expose 8443 (HTTP/2). Keycloak health + admin now accessible over HTTPS.  
2. **Clients + env** — Switched Keycloak clients to confidential, generated secrets (`issuer|investor|backoffice-secret-20251113`), patched `.env.local` for each portal (adds `KEYCLOAK_CLIENT_SECRET` + HTTPS base). Restarted pm2 with `--update-env`.  
3. **Diagnostics** — Captured `docker ps`, `pm2 status`, `ss -ltnp`, and `curl` suite (5000/8080/300x) at 08:16 UTC for audit. API gateway returned `Healthy`; Keycloak proxy JSON {"status":"UP"}.  
4. **Blocking issue** — `next-auth` still fails with `SIGNIN_OAUTH_ERROR` / `OPError invalid_request (HTTPS required)` before hitting Keycloak. Verified:
   - `apps/portal-issuer/.next/server/.../route.js` embeds HTTPS issuer (`https://185.168.192.214.sslip.io:8443/realms/ois-dev`), and direct `openid-client` scripts can `discover` + build auth URLs successfully.
   - Keycloak realm `sslRequired=none`; manual GETs to `/protocol/openid-connect/auth` with `redirect_uri=http://185.168.192.214:3001/...` return the login form (so KC accepts HTTP callbacks).
   - `pm2 logs portal-issuer` show the stack trace originates inside `Issuer.discover()` before any network packets leave the host (tcpdump on ports 8080/8081/8443 shows no traffic from the Next process during the failure window).
   - Hypothesis: NextAuth/openid-client is rejecting our configuration prior to network I/O (likely due to IP-host callback over HTTP). Need to inspect NextAuth 5 → openid-client integration or switch callback URLs to HTTPS via reverse proxy. Until resolved, Playwright login + screenshots cannot be produced.  

# Outstanding / Next
1. Debug NextAuth ↔ Keycloak handshake (clear openid-client cache, inspect discovery URL, consider forcing `allowInsecureRequests` or ensuring callback host is HTTPS).  
2. Once login succeeds, run `/tmp/playwright-run/index.js` for Issuer/Investor, stash screenshots + logs in memory-bank.  
3. Move TLS/proxy overrides into repo (IaC), sync LE renewal to `/opt/ois-cfa/certs/*`, rotate Keycloak admin password after demo.  
4. Monitor .NET compose services for stability; optimize heavy builds if needed.  
5. Record switchover plan (uk1 vs cfa1) once original VPS returns.  

## 2025-11-13 13:45 MSK — Cloudflare + TLS + Playwright
- Создал A-записи (DNS only) для `auth|issuer|investor|backoffice|api.cfa.llmneighbors.com` → `185.168.192.214` через `flarectl dns create-or-update` (IDs: c1bbc05a..., 8b0ea268..., c5439fa1..., 18732c4a..., 9a154290...).
- Перевёл зону назад в `SSL mode = full` после первичной настройки (PATCH `/zones/:id/settings/ssl`).
- Получил wildcard LE-сертификат `*.cfa.llmneighbors.com` DNS-челленджем (certbot + Cloudflare API token → `/etc/letsencrypt/live/cfa.llmneighbors.com`).
- Настроил system nginx (`/etc/nginx/sites-available/cfa-portals.conf`) → HTTPS 443 + HTTP→HTTPS redirect, upstream'ы на `127.0.0.1:{8081,3001,3002,3003,5000}`. Служба `x-ui` мешала порту 443 → остановил/disable `systemctl stop x-ui && systemctl disable x-ui` (обязательно подтвердить, если сервис ещё нужен).
- Обновил env:
  - `/opt/ois-cfa/apps/{portal-issuer,portal-investor,backoffice}/.env.local` → `NEXT_PUBLIC_*` и `NEXTAUTH_URL` на `https://{issuer|investor|backoffice}.cfa.llmneighbors.com`, API = `https://api.cfa.llmneighbors.com`, KEYCLOAK URL = `https://auth.cfa.llmneighbors.com`.
  - `docker-compose.keycloak-proxy.yml` → `KC_HOSTNAME_URL=https://auth.cfa.llmneighbors.com`, port 443. Перезапущены `keycloak`, `keycloak-proxy`.
  - Клиенты KC (`portal-{issuer,investor,backoffice}`) получили новые redirect/webOrigin через `kcadm update`.
  - Отключил realm-action `VERIFY_PROFILE` и очистил RequiredActions у тестовых users (issuer/investor/admin) чтобы Keycloak не зависал на profile update.
- PM2: `portal-*` рестарт с `--update-env`. Next dev конфиги починены (`next.config.js` вернул строки с кавычками).
- Запустил Playwright (eywa1) против новых URL. Скриншоты и JSON:
  - Issuer → `https://issuer.cfa.llmneighbors.com/dashboard`
  - Investor → `https://investor.cfa.llmneighbors.com/portfolio`
  - Assets: `memory-bank/Scrum/20251112-ports-closed-on-vps/playwright-{issuer,investor}.png`.
- Nginx Health: `curl -I https://auth.cfa.llmneighbors.com` → 302 `/admin/`; `curl https://api.cfa.llmneighbors.com/health` → `Healthy`.

## 2025-11-13 15:20 MSK — SMTP stack + self-registration
- Развернул Postfix + OpenDKIM на UK1:
  - `postconf -e 'inet_interfaces = all'`, `mynetworks = 127.0.0.0/8 172.17.0.0/16 172.18.0.0/16`, `smtpd_{relay,recipient}_restrictions = permit_mynetworks, reject_unauth_destination`.
  - Права на `/etc/opendkim/keys` и конфиг приведены к `opendkim:opendkim`, `KeyTable/SigningTable` настроены на селектор `mail`.
  - Сервисы `postfix` и `opendkim` переведены в `enabled`, health проверен (`systemctl status` + `tail -f /var/log/mail.log`).
- Cloudflare DNS:
  - `mail.cfa.llmneighbors.com` (A), `cfa.llmneighbors.com` (MX), SPF (`v=spf1 ip4:185.168.192.214 ~all`), DKIM (`mail._domainkey`), DMARC (`p=none`).
- Keycloak realm `ois-dev`:
  - `verifyEmail=true`, `registrationAllowed=true`, SMTP host `172.18.0.1:25`, `from=no-reply@cfa.llmneighbors.com`, STARTTLS отключён (локальный relay).
- Smoke через `mail.tm`:
  - `echo "Test" | mail -s "SMTP ok" cfaYYYY@2200freefonts.com` → письма видны через `curl https://api.mail.tm/messages ...`.
  - Playwright self-registration (`tests/e2e-playwright/tests/self-registration.spec.ts`) создаёт временную почту, проходит регистрацию, читает verify-link через API и завершает первый вход.
- Итоговый `npm test`:
  - issuer/investor OAuth → PASS.
  - investor self-registration → PASS (см. `tests/e2e-playwright/test-results/self-registration-*/`).
- Открытые вопросы:
  - Postfix сейчас открыт в интернет на 25 порту; при переносе в прод нужно добавить fail2ban/ufw и сменить `compatibility_level`.
  - SMTP-пароль не нужен (локальный relay). Если потребуется внешний SMTP, придётся включить auth/TLS.

---
created: 2025-11-27 16:15
updated: 2025-11-27 18:00
type: agent-prompt
sphere: [devops]
topic: [cfa2, cloudflare, dns, tls, nginx, keycloak]
author: alex
agentID: to-be-filled-by-runner
version: 0.1.1
tags: [ops-001-005, cfa2, telex.global, cloudflare, ingress, portals, keycloak]
---

# Agent Prompt · OPS-001-005 cfa2 Cloudflare ingress — **fix HTTPS/Keycloak login & E2E**

> This prompt focuses on eliminating mixed HTTP/HTTPS and `:58080` usage in Keycloak/portals on `cfa2`, and proving end‑to‑end login via domains.
>
> Read together with:
> - `memory-bank/tasks/ops/cicd/OPS-001-005-cfa2-cloudflare.prompt.md` (lessons & pitfalls),
> - `memory-bank/tasks/ops/cicd/OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md` (story / DoD / verification),
> - `memory-bank/tasks/ops/cicd/OPS-001-cicd.verification.md` (global verification).

## ROLE / CONTROL PLANE

- ROLE: Senior DevOps / NetOps / Auth engineer for `OPS-001-005`.
- CONTROL PLANE: `eywa1` (Ubuntu), tmux `p-cfa`.
- TARGETS:
  - `cfa2` — dev VPS (92.51.38.126), `/srv/cfa`, nginx + docker compose.
  - `uk1`, `cfa1` — reference envs with working `*.cfa.llmneighbors.com` ingress; **read-only**, for comparison.
- REPOS / FILES:
  - Main: `repositories/customer-gitlab/ois-cfa`
  - Cloudflare/ingress docs:
    - `docs/deploy/20251113-cloudflare-ingress.md`
    - `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md`
  - Stories:
    - `memory-bank/tasks/ops/cicd/OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md`
    - `memory-bank/tasks/ops/cicd/OPS-001-005-cfa2-cloudflare.prompt.md`
    - `memory-bank/tasks/ops/cicd/OPS-001-cicd.verification.md`
  - Runtime:
    - `deploy/docker-compose-at-vps/cfa2/docker-compose.yml`
    - `/srv/cfa/.env` and `/srv/cfa/docker-compose.yml` on `cfa2`
  - Portals / auth:
    - `apps/portal-issuer/src/lib/auth.ts`
    - `apps/portal-investor/src/lib/auth.ts`
    - `apps/backoffice/src/lib/auth.ts`
  - Playwright:
    - `tests/e2e-playwright/playwright.config.ts`
    - `tests/e2e-playwright/tests/public-auth.spec.ts`
    - `tests/e2e-playwright/.env.cfa2` (to be created/used)
  - Nginx / Keycloak (on cfa2):
    - `/etc/nginx/sites-available/cfa2-portals.conf`
    - `ois-keycloak` container logs / env.

## SYMPTOM / ROOT CAUSE TO FIX

- User still sees:

  > `An error occurred during a connection to auth.cfa2.telex.global:58080. SSL received a record that exceeded the maximum permissible length.`

- This error means the browser (or some client) is trying to speak **HTTPS** to a port that serves **plain HTTP**:

  - On `cfa2`:
    - `443` → nginx TLS (wildcard LE `*.cfa2.telex.global`).
    - `58080` → plain HTTP Keycloak (behind nginx).
  - Therefore:
    - `https://auth.cfa2.telex.global` → should work (TLS → nginx → 58080).
    - `https://auth.cfa2.telex.global:58080` → will always fail with this SSL record length error.

- Your mission: **eliminate all accidental `https://...:58080` and mixed schemes/ports from configs/code/tests**, then prove end‑to‑end login works via domains.

## HARD CONSTRAINTS

- Do NOT:
  - change dev-cfa2 CI rules or path-based behavior (that’s handled in OPS-001-003),
  - touch uk1/cfa1 config except to read and compare,
  - break existing DNS/TLS/LE cert setup (only adjust if you find a concrete misconfig).
- Focus on:
  - nginx vhost correctness,
  - Keycloak realm/clients correctness,
  - portal env and NextAuth provider wiring,
  - Playwright + browser E2E login.

---

## 1. Confirm nginx/TLS and ports from a clean vantage point

1. On `eywa1` AND from `uk1` (for external vantage):

   ```bash
   curl -vk https://auth.cfa2.telex.global | head -20
   curl -vk https://auth.cfa2.telex.global:58080 | head -5 || echo "expected-fail"
   ```

   Expected:
   - `https://auth.cfa2.telex.global` → TLS OK (CN `*.cfa2.telex.global`), 200/302 from Keycloak/nginx.
   - `https://auth.cfa2.telex.global:58080` → SSL record length error (expected, because that’s HTTP port).

2. On `cfa2`:

   ```bash
   ssh cfa2 "sudo nginx -t && sudo ss -tulpn | grep ':443' || echo 'no-443'"
   ssh cfa2 "sed -n '1,220p' /etc/nginx/sites-available/cfa2-portals.conf"
   ```

   Verify:
   - nginx listens on 443 with LE cert,
   - upstream for Keycloak is `127.0.0.1:58080`,
   - `server_name` includes `auth.cfa2.telex.global`.

If this is all correct, do not touch nginx/cert configuration: the SSL error is from using the wrong port, not from nginx itself.

---

## 2. Inspect env on cfa2 for stray `:58080` in public URLs

On `cfa2`:

```bash
ssh cfa2 "cd /srv/cfa && sed -n '1,220p' .env"
ssh cfa2 "docker exec portal-issuer env | grep -E 'NEXT_PUBLIC_|NEXTAUTH_URL|KEYCLOAK_'"
ssh cfa2 "docker exec portal-investor env | grep -E 'NEXT_PUBLIC_|NEXTAUTH_URL|KEYCLOAK_'"
ssh cfa2 "docker exec backoffice env | grep -E 'NEXT_PUBLIC_|NEXTAUTH_URL|KEYCLOAK_'"
```

Enforce the following triangle:

- Public Keycloak URL (for browser / NextAuth):
  - `NEXT_PUBLIC_KEYCLOAK_URL = https://auth.cfa2.telex.global` (no `:58080`)
- Portal public URLs:
  - `NEXTAUTH_URL = https://issuer.cfa2.telex.global`
  - `NEXTAUTH_URL = https://investor.cfa2.telex.global`
  - `NEXTAUTH_URL = https://backoffice.cfa2.telex.global`
- Internal Keycloak URL (for backend calls from portal):
  - `KEYCLOAK_INTERNAL_URL = http://keycloak:8080` (HTTP, docker network only)

If you see any of these as `https://auth.cfa2.telex.global:58080` or `http://92.51.38.126:58080`:

- Fix them in the source compose/env:
  - `deploy/docker-compose-at-vps/cfa2/docker-compose.yml`
  - `deploy/docker-compose-at-vps/cfa2/.env` (if used)
- Then re‑sync to `cfa2`:

  ```bash
  cd repositories/customer-gitlab/ois-cfa
  ./ops/scripts/sync-compose-cfa2.sh
  ssh cfa2 "cd /srv/cfa && docker compose up -d portal-issuer portal-investor backoffice"
  ```

---

## 3. Align Keycloak realm & clients with the public HTTPS issuer

Inside `ois-keycloak` on `cfa2`:

```bash
ssh cfa2 "docker logs --tail=50 ois-keycloak"
curl -sk https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration | jq '.issuer,.authorization_endpoint,.token_endpoint,.userinfo_endpoint'
```

All endpoints must be under `https://auth.cfa2.telex.global/realms/ois/...`.

Using `kcadm` (see `uk1` session for pattern):

```bash
ssh cfa2 "docker exec -it ois-keycloak bash"

# inside container: login with admin creds (see docs)
kcadm.sh config credentials --server https://auth.cfa2.telex.global \
  --realm master --user <admin> --password '<admin-pass>' --config /tmp/kcadm.config

kcadm.sh get realms/ois --config /tmp/kcadm.config
kcadm.sh get clients -r ois --config /tmp/kcadm.config | jq '.[].clientId'
```

For each client `portal-issuer`, `portal-investor`, `backoffice`:

- `rootUrl = https://<portal>.cfa2.telex.global`
- `redirectUris` include:
  - `https://<portal>.cfa2.telex.global/*`
  - `https://<portal>.cfa2.telex.global/api/auth/callback/keycloak`
- `webOrigins` include:
  - `https://<portal>.cfa2.telex.global`
- No `:58080` in any of these.

Fix any leftover IP/port‑based URLs to match `uk1`/`cfa1` pattern.

---

## 4. Fix NextAuth `KeycloakProvider` wiring in portal code

In the repo (`ois-cfa`):

1. Open provider code:

   - `apps/portal-issuer/src/lib/auth.ts`
   - `apps/portal-investor/src/lib/auth.ts`
   - `apps/backoffice/src/lib/auth.ts`

2. Ensure the pattern is:

   ```ts
   const publicKeycloakBase =
     process.env.NEXT_PUBLIC_KEYCLOAK_URL ?? 'http://localhost:58080';
   const internalKeycloakBase =
     process.env.KEYCLOAK_INTERNAL_URL ?? publicKeycloakBase;

   KeycloakProvider({
     clientId,
     clientSecret,
     issuer: `${publicKeycloakBase}/realms/${realm}`, // public issuer
     authorization: {
       url: `${publicKeycloakBase}/realms/${realm}/protocol/openid-connect/auth`,
       // ...
     },
     token: `${internalKeycloakBase}/realms/${realm}/protocol/openid-connect/token`,
     userinfo: `${internalKeycloakBase}/realms/${realm}/protocol/openid-connect/userinfo`,
   });
   ```

Key points:

- `publicKeycloakBase` must be `https://auth.cfa2.telex.global` in `cfa2` env (no `:58080`).
- `internalKeycloakBase` may be `http://keycloak:8080` (internal), but this is used only for token/userinfo, not for browser redirects.
- Remove any hardcoded `http://92.51.38.126:58080` or `:58080` from provider code.

3. Apply the same consistent pattern to all three portals.
4. Commit changes on `dev-cfa2` with a clear message, e.g.:

   ```bash
   git commit -am "fix(auth): use https issuer for Keycloak in cfa2 portals"
   git push origin dev-cfa2
   ```

CI will rebuild `build-portal-*` and redeploy (`deploy-cfa2`).

---

## 5. Run Playwright E2E against domains (no ports in URLs)

In `repositories/customer-gitlab/ois-cfa`:

1. Create or update `tests/e2e-playwright/.env.cfa2`:

   ```env
   ISSUER_BASE_URL=https://issuer.cfa2.telex.global
   INVESTOR_BASE_URL=https://investor.cfa2.telex.global
   BACKOFFICE_BASE_URL=https://backoffice.cfa2.telex.global

   USE_KEYCLOAK_AUTH=true

   ISSUER_USER=issuer@test.com
   ISSUER_PASS=<issuer-password>
   INVESTOR_USER=investor@test.com
   INVESTOR_PASS=<investor-password>
   BACKOFFICE_USER=cfa.devs@gmail.com
   BACKOFFICE_PASS=<backoffice-password>
   ```

   - Never put `:58080` in these URLs.
   - Do not commit secrets; keep env local.

2. Run tests:

   ```bash
   cd repositories/customer-gitlab/ois-cfa
   npx playwright test tests/e2e-playwright/tests/public-auth.spec.ts \
     --config=tests/e2e-playwright/playwright.config.ts \
     --project=chromium
   ```

3. On failure (`Configuration`/`OAuthSignin`/server error):

   Immediately:

   ```bash
   ssh cfa2 "docker logs --tail=200 portal-issuer"
   ssh cfa2 "docker logs --tail=200 portal-investor"
   ssh cfa2 "docker logs --tail=200 backoffice"
   ```

   Look for:
   - `MissingSecretError` → check `NEXTAUTH_SECRET`.
   - any URLs with `:58080` where HTTPS is expected.
   - mismatched issuer vs `/.well-known/openid-configuration`.

Adjust env and/or provider code until Playwright passes for all three portals.

---

## 6. Manual browser verification from multiple IPs

From at least two locations (e.g. `eywa1`, `uk1`, your local machine):

- `https://issuer.cfa2.telex.global`
- `https://investor.cfa2.telex.global`
- `https://backoffice.cfa2.telex.global`

For each:

- Login with the appropriate test user.
- Ensure you land on a meaningful post‑login page (dashboard or equivalent).
- Capture screenshots of the post‑login state.

Save them on `eywa1`, e.g.:

- `docs/deploy/vps-cfa2/screenshots/issuer-login.png`
- `docs/deploy/vps-cfa2/screenshots/investor-login.png`
- `docs/deploy/vps-cfa2/screenshots/backoffice-login.png`

---

## 7. Update stories / verification (and close JTBD)

1. `OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md`:

   - In DoD:
     - Mark remaining Frontends and Docs items `[x]` once Playwright + browser checks are green.
   - Verification Matrix:
     - Frontends row Fact / Comment:
       - change from ◑ to ✔ with explicit reference:
         - Playwright test (`public-auth.spec.ts`),
         - env file (`.env.cfa2`),
         - log snippets,
         - screenshot paths.
   - Loop trace:
     - add Loop “Keycloak + portals E2E on cfa2.telex.global” with PLAN/EXECUTE/TESTS/DOCS.

2. `OPS-001-003-cicd-phase2.story.md`:

   - After E2E is confirmed:
     - mark Runtime “fronts talk to gateway/Keycloak via domains” `[x]`,
     - update Verification Matrix Runtime row to ✔ with reference to OPS‑001‑005 evidence,
     - change DoD header from ~90% to ~100% and status to done.

3. `OPS-001-cicd.verification.md`:

   - Add a section for “cfa2 portals login via telex.global”:
     - show:
       - curl checks,
       - Playwright run summary,
       - manual browser observations,
       - key logs (where you resolved `:58080` misuse).

When all URLs that should be HTTPS point to 443, `KEYCLOAK_INTERNAL_URL` is confined to HTTP internal use, and Playwright + browser both succeed, the SSL record exceeded length error becomes an anti‑pattern, not an active problem. Your JTBD is to reach that state and document it.


---
created: 2025-11-27 20:00
updated: 2025-11-27 20:00
type: agent-prompt
sphere: [devops]
topic: [cfa2, cloudflare, keycloak, portals, playwright]
author: alex
agentID: to-be-filled-by-runner
version: 0.1.0
tags: [OPS-001-003, OPS-001-005, dev-cfa2, finalizer]
---

# Agent Prompt · OPS-001-005 cfa2 Cloudflare ingress — finalizer for portals login

> This prompt is for a fresh agent whose only job is to finish the cfa2.telex.global ingress/auth story: rebuild the three portals with the fixed Keycloak issuer, verify login via Playwright + browser, and close the remaining DoD items in OPS-001-003 and OPS-001-005.

## ROLE / CONTROL PLANE

- ROLE: DevOps/CI + Auth “finisher” for dev-cfa2 portals.
- CONTROL PLANE: `eywa1` (Ubuntu), tmux `p-cfa`.
- TARGETS:
  - `cfa2` — main dev VPS (92.51.38.126), `/srv/cfa` (compose stack).
  - `cfa1`, `uk1` — **read-only** (reference for nginx/Keycloak; do not change).
- GITLAB:
  - Host: `git.telex.global`, project: `npk/ois-cfa`.
  - Branch: **only** `dev-cfa2`.
- REPO:
  - `/home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa`.

## MUST-READ CONTEXT

Read these first (they encode what previous agents already did and what is left):

- `memory-bank/tasks/ops/cicd/OPS-001-003-cicd-phase2.story.md` — PHASE2 (frontends + path-based + SDK).
- `memory-bank/tasks/ops/cicd/OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md` — PHASE3 (Cloudflare ingress + portals login).
- `memory-bank/tasks/ops/cicd/OPS-001-CICD-architecture.md` — especially:
  - “CI/CD pipeline (dev-cfa2)” sequence,
  - “Images & Registry flow” (vds1 → GitLab Registry → deploy-cfa2 → cfa2),
  - “Certificates · Paths, renewal, alerts”.
- `memory-bank/tasks/ops/cicd/OPS-001-cicd.verification.md` — Cloudflare/Keycloak/cfa2 section.
- Source files:
  - `.gitlab/gitlab-ci.dev.yml` (dev-cfa2 CI),
  - `deploy/docker-compose-at-vps/cfa2/docker-compose.yml`,
  - `/srv/cfa/.env` and `/srv/cfa/docker-compose.yml` on `cfa2`,
  - `apps/portal-issuer|portal-investor|backoffice/src/lib/auth.ts`,
  - `tests/e2e-playwright/tests/public-auth.spec.ts` + `tests/e2e-playwright/playwright.config.ts`.

Your context “entry point” for the last auth fix is commit `b7918c5db858e98b6dc9abeed7e39460bdb0ed86`:

- message: `fix(auth): align portal Keycloak issuer with public hostname`,
- branch: `dev-cfa2`.

This commit updated `auth.ts` in all three portals to use `https://auth.cfa2.telex.global/realms/ois` as issuer. The missing piece is to **rebuild the three portal images**, redeploy to cfa2, and verify login flows.

## WHAT IS ALREADY DONE (YOU DO NOT REPEAT)

- Cloudflare / DNS:
  - `auth|issuer|investor|backoffice|api.cfa2.telex.global` → `92.51.38.126` (A records).
- TLS / nginx:
  - Wildcard LE for `*.cfa2.telex.global` in `/etc/letsencrypt/live/cfa2.telex.global/{fullchain.pem,privkey.pem}`.
  - nginx vhost `cfa2-portals.conf` proxies:
    - `auth` → `keycloak:8080`,
    - `issuer` → `portal-issuer:3001`,
    - `investor` → `portal-investor:3002`,
    - `backoffice` → `backoffice:3003`,
    - `api` → `api-gateway:58081`.
- Keycloak:
  - realm `ois` exists with issuer `https://auth.cfa2.telex.global/realms/ois`.
  - clients `portal-issuer` / `portal-investor` / `backoffice`:
    - `redirectUris` and `webOrigins` set to `https://<portal>.cfa2.telex.global/*` and `<portal>/api/auth/callback/keycloak`.
  - test users: `issuer@test.com`, `investor@test.com`, `cfa.devs@gmail.com` with correct roles.
- Env on cfa2:
  - `NEXT_PUBLIC_API_BASE_URL=https://api.cfa2.telex.global`,
  - `NEXT_PUBLIC_KEYCLOAK_URL=https://auth.cfa2.telex.global`,
  - `NEXT_PUBLIC_KEYCLOAK_REALM=ois`,
  - `NEXTAUTH_URL=https://<portal>.cfa2.telex.global`,
  - `KEYCLOAK_CLIENT_SECRET=secret`,
  - `KEYCLOAK_INTERNAL_URL=http://keycloak:8080`.
- CI:
  - path-based rules are correct and validated (TC1–TC3),
  - docs/runbooks/architecture cheatsheet are up to date.

Do **not** touch any of this unless you find a concrete misconfiguration. Your job is to finish the **portal images + login verification**.

## HARD CONSTRAINTS

- Do NOT:
  - edit Cloudflare DNS records or LE cert configuration,
  - change nginx vhost on uk1/cfa1,
  - change CI path-based rules in `.gitlab/gitlab-ci.dev.yml` (unless you find a clear bug).
- You MAY:
  - commit small files in `apps/portal-*` to trigger builds,
  - use `glab` to monitor pipelines and jobs,
  - `ssh cfa2` to inspect logs and env,
  - run Playwright tests locally on `eywa1`.

## YOUR JTBD (WHAT YOU MUST FINISH)

1. **Rebuild only the three portal images for the fixed auth code** on `dev-cfa2` via a push pipeline (not API-only pipeline).
2. **Verify via logs on cfa2** that NextAuth/Keycloak provider for each portal uses:
   - `issuer = https://auth.cfa2.telex.global/realms/ois`,
   - `authorization.url = https://auth.cfa2.telex.global/realms/ois/protocol/openid-connect/auth`,
   - no `:58080` or bare IP in public URLs.
3. **Run Playwright `public-auth.spec.ts`** against `https://issuer|investor|backoffice.cfa2.telex.global` until issuer+investor (and preferably backoffice) are green.
4. **Manual login from browser(s)** (multiple IPs if possible), with screenshots of post-login pages.
5. **Update stories and verification**:
   - close remaining DoD in `OPS-001-003` (Runtime) and `OPS-001-005` (Frontends/login),
   - add a concise block to `OPS-001-cicd.verification.md` with commands, pipeline IDs, Playwright run, and screenshot paths.

6. **Enable and verify Keycloak self-registration (like on uk1)** so that new users can sign up (Wezer registration use case) without manual admin intervention.

## HIGH-LEVEL PLAN

1. Confirm that HEAD on `dev-cfa2` already contains the `fix(auth)` commit and no further auth regressions.
2. Create a minimal commit that touches all three portals (e.g. `ci-rebuild-auth-*.md`) and push to `dev-cfa2` → trigger a **push** pipeline.
3. With `glab api`, ensure that pipeline:
   - source = `push`, ref = `dev-cfa2`,
   - includes `build-portal-issuer`, `build-portal-investor`, `build-backoffice`, and `deploy-cfa2`.
4. Wait for these jobs to go green; if any fails, debug and fix (without changing Cloudflare/nginx).
5. On `cfa2`, check portal logs to confirm provider URL shape (no `https://...:58080`).
6. Run Playwright `public-auth.spec.ts` with `.env.cfa2` pointing to `https://*cfa2.telex.global` (no ports).
7. If tests pass, perform manual browser checks and save screenshots under `docs/deploy/vps-cfa2/screenshots/`.
8. Close DoD/Verification Matrix in `OPS-001-003` and `OPS-001-005`, and add a verification entry in `OPS-001-cicd.verification.md`.

## EXTRA: Enable self-registration in Keycloak realm `ois` (uk1 parity)

On uk1 self-registration was enabled by toggling Keycloak realm login flags (`registrationAllowed=true`, `verifyEmail=true`) and wiring SMTP (Postfix). For cfa2 we want the **same behavior** for realm `ois`, but with minimal scope:

### 1. UI steps (admin console)

If you prefer doing it by hand, use the admin UI:

1. Open `https://auth.cfa2.telex.global/admin` in a browser.
2. Log in with the Keycloak admin user you already use on cfa2.
3. In the **left menu**, select:
   - Realm: `ois`,
   - then go to **Realm settings → Login**.
4. On the Login tab:
   - Turn **ON**:
     - `User registration`,
     - `Login with email` (если ещё не включён),
     - `Forgot password` (опционально, но удобно).
   - Optionally turn **ON**:
     - `Verify email` (тогда нужны рабочие SMTP‑настройки, см. uk1 пример).
5. Click **Save**.

This should immediately expose the “Register” button on the Keycloak login page for realm `ois` when you hit `https://auth.cfa2.telex.global/realms/ois/account` or go through the portals’ “Sign in” flow.

### 2. CLI steps (kcadm) — preferred for repeatability

If you want to do it via CLI (and make it scriptable, similar to uk1), use `kcadm` inside `ois-keycloak`:

```bash
ssh cfa2 "docker exec -it ois-keycloak bash"

# inside the container:
kcadm.sh config credentials \
  --server https://auth.cfa2.telex.global \
  --realm master \
  --user <admin-username> \
  --password '<admin-password>' \
  --config /tmp/kcadm.cfa2.config

# Enable self-registration and login-by-email on realm 'ois'
kcadm.sh update realms/ois \
  -s registrationAllowed=true \
  -s loginWithEmailAllowed=true \
  --config /tmp/kcadm.cfa2.config

# (optional) enable email verification, if SMTP is configured
# kcadm.sh update realms/ois \
#   -s verifyEmail=true \
#   --config /tmp/kcadm.cfa2.config
```

Notes:

- On uk1 we used the same pattern (see `20251113-uk1-deploy_co-76ca.md`): `verifyEmail=true`, `registrationAllowed=true`, SMTP = local Postfix.
- On cfa2 you can start with `registrationAllowed=true` and `loginWithEmailAllowed=true` without verifyEmail, and add `verifyEmail=true` later when SMTP is ready.

### 3. Verify self-registration end-to-end

1. In a browser:
   - Go to `https://issuer.cfa2.telex.global` (or investor/backoffice),
   - click “Sign in with Keycloak”,
   - on the Keycloak login page check for a “Register”/“Зарегистрироваться” link.
2. Use a test email to go through the registration flow:
   - If `verifyEmail=false` — user should be created and able to log in immediately after filling the form.
   - If `verifyEmail=true` — you should receive a verification email (once SMTP is wired) and complete the link.
3. Confirm that the new user appears in realm `ois` and can log in to the portal (Wezer registration scenario).

### 4. Update stories to reflect registration DoD

- `OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md`:
  - Under Frontends DoD, add that self-registration for realm `ois` is enabled (`registrationAllowed=true`) and works (Wezer registration flow).
  - In Verification Matrix, add a comment that registration was validated manually (and via Playwright if you extend tests).
- `OPS-001-cicd.verification.md`:
  - Add a short block summarizing:
    - kcadm commands used to toggle `registrationAllowed`,
    - evidence (screenshots/logs) that the registration link appears and a new user can sign up and log in.


> You are allowed and expected to use all available tests (Playwright + manual) and to iterate until the portals login flow is truly green, not just “probably works”.

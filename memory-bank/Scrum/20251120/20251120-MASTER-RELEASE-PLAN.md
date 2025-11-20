# Master Plan: OIS-CFA Stabilization (CFA1 / llmneighbors)

## 🎯 Objective
Achieve a fully functional environment on `cfa1` (`*.cfa1.llmneighbors.com`) by fixing Infrastructure/Auth issues and completing NX-07 Backend. Migration to `telex.global` is DEFERRED.

## 📦 Phase 1: Infrastructure & Auth Repair (Priority: Critical)
**Target:** `cfa1` accessible via `https://*.cfa1.llmneighbors.com` with working Login.
- [ ] **Permissions:** Update `deploy-node.sh` to enforce `chown -R user:user` (fix `npm EACCES`).
- [ ] **Env Config:** Ensure `.env.local` on `cfa1` uses `cfa1.llmneighbors.com` for all URLs.
- [ ] **Auth Fix:** Create and run `ops/scripts/auth/fix-redirects.sh` to update Keycloak Client URIs to `https://*.cfa1.llmneighbors.com/*`.
- [ ] **Nginx:** Verify `cfa1-portals.conf` is active and SSL is valid.

## 📦 Phase 2: Backend Gap Fill (NX-07)
**Target:** Codebase in `infra.defis.deploy` implements missing API.
- [ ] **Compliance:** Implement `GET /v1/compliance/kyc` and `POST decision` in .NET.
- [ ] **Identity:** Implement `GET /v1/identity/users`.
- [ ] **Audit:** Ensure `/v1/audit` routing works.

## 📦 Phase 3: Verification
**Target:** Green E2E Tests.
- [ ] **Deploy:** Push the fixed code to `cfa1`.
- [ ] **E2E:** Run Playwright tests against `cfa1.llmneighbors.com`.
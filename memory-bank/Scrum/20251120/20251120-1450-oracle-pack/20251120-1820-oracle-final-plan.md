# Oracle Pack — Final JTBD Plan (Phased)
Generated: 2025-11-20 18:20 UTC  
Sources: 20251120-1553-gpt5p-p1.oracle.md, 20251120-1529-gpt5p-p2.oracle.md, 20251120-1557-gpt5p-p3.oracle.md, 20251120-1712-eval-on-eval.gpt5p.oracle.md, context.txt/prompt.md (20251120-1412-oracle-evaluator)

## Overall DoD
- [ ] Oracle package (context.txt + prompt v3) is consumed by an Evaluator run, issues logged.
- [ ] NX-07 readiness gaps are captured as actionable items (API alignment, user registry, tests).
- [ ] Auth on cfa1 is fixed or a migration plan to `*.cfa{n}.telex.global` is ready with secrets/env.
- [ ] Deployment playbook for new VPS/domains is consolidated (Cloudflare creds, env matrices, scripts).
- [ ] Zip/tags/branches stay clean after changes.
- [ ] Ante / Job (from oracle-output) captured in task specs: Ante = нужен полный анализ + приведение контракта/деплоя к готовности; Job = довести NX05/06/08 до проверяемого состояния, закрыть NX07 блокеры, подготовить новый домен.

## Phase 0 — Oracle Package Re-run (baseline validation)
### Kickoff
- Ensure latest context: `context.txt` (2.3MB code2prompt) + `prompt.md` v3 in `.../20251120-1412-oracle-evaluator/`.
- Confirm zip tags list matches merged branches `NX-01/03/05/06/08`; active worktree only NX-07.
- Attach extra sessions: `eywa1-p-cfa-w12...`, `eywa1-p-cfa-w11...`, `20251119-20-gem3-aistudio-thread-code-session-NX05-08.oracle.session.json`.
### Do
- Run Oracle v3 prompt once; capture findings (table + mermaid) into `.../20251120-1450-oracle-pack/final-eval.md`.
### Acceptance
- Findings include: NX-07 blockers, auth gap cfa1 vs uk1, telex.global delta, deploy checklist.

## Phase 1 — NX-07 Readiness (API/UI/tests alignment)
### Kickoff
- Inventory current Compliance/Identity endpoints vs Backoffice client (`apps/backoffice/src/lib/api/compliance.ts`) and NX-07 spec.
- Decide contract owner: either align UI to existing endpoints (`/v1/kyc/tasks`, `/v1/compliance/kyc/investors/{id}/approve|reject`) or expose new endpoints matching UI.
### Do
- Implement chosen contract in Compliance (and Identity, if `GET /v1/identity/users` required).
- Update gateway routes + TS SDK + Backoffice client/pages to real APIs.
- Add tests: backend integration for KYC decisions, frontend component/e2e (Playwright) for KYC/User registry.
### Acceptance
- Backoffice KYC and Users no longer mock; pass e2e on target environment; spec/docs updated.

## Phase 2 — Auth & Domain Migration (cfa1 → telex.global-ready)
### Kickoff
- Collect current env on cfa1 vs uk1 (Keycloak realms/clients, redirect URIs, NextAuth configs).
- Prepare new Cloudflare env: `/home/user/__Repositories/cloudflare__developerisnow/.env` with `telex.global` creds (EMAIL/PASS/API/TOKEN/ACCOUNT_ID).
- Define target names: `api/auth/issuer/investor/backoffice.cfa{n}.telex.global`.
### Do
- Fix cfa1 auth: rerun Keycloak bootstrap (kcadm path), regenerate client secrets, sync `.env.*` for gateway/apps, redeploy.
- Duplicate configs for `telex.global`: DNS via `cloudflare-dns-upsert.sh`, TLS strategy (CF or certbot), nginx host mappings `/srv/cfa`.
- Deploy `infra.defis.deploy` to new node (or reuse cfa1) with corrected env; rerun smoke/e2e (auth + issuer/backoffice flows).
### Acceptance
- Auth works on cfa1 and on telex.global hostnames; health and login flows pass; docs updated with new env file templates.

## Phase 3 — Deployment Playbook Consolidation
### Kickoff
- Gather runbooks: `10-eywa1-control-plane-runbook.md`, `docker-compose-at-vps/0x-*.md`, `MULTI_ACCOUNT_SETUP.md`, scripts (`provision-node.sh`, `deploy-node.sh`, `cloudflare-dns-upsert.sh`).
- Identify path differences (`/srv/cfa` vs `/opt/ois-cfa`) and env matrices.
### Do
- Write a single `DEPLOY-CHECKLIST.md` (per-env matrix of vars: API_BASE, KEYCLOAK auth, CF_ZONE_ID/ACCOUNT_ID, DB creds, JWT/Keycloak secrets, ports).
- Add examples for `*.telex.global` `.env` and `.cloudflare.*.env`.
- Note CI guardrail idea: optional hook to remind zip/tag after merge.
### Acceptance
- One authoritative checklist exists; new VPS/domain setup can be followed without mixing old/ new docs.

## Phase 4 — Zip/Branch Hygiene
### Kickoff
- Verify `zip/*` tags still match merged branches; ensure NX-07 not zipped.
### Do
- If new merges happen, update `artifacts/git/branch-zip-*.txt`, rerun `scripts/git/zip_branches.sh`.
### Acceptance
- `git branch -a` lists only active branches; tags record all archived work; doc points to workflow.

## Next Actions (chronological)
1) Run Oracle prompt v3 now; log findings in `final-eval.md` under oracle-pack.  
2) Decide API contract for NX-07; create tasks for backend/gateway/UI/test alignment.  
3) Fix cfa1 auth; prepare telex.global env files and DNS; redeploy infra.defis.deploy; run smoke/e2e.  
4) Author `DEPLOY-CHECKLIST.md` with env matrix (include telex.global creds) and merge into docs.  
5) Maintain zip hygiene after any merges.

---
created: 2025-11-11 17:25
updated: 2025-11-11 17:25
type: planning
sphere: [engineering, architecture]
topic: [JTBD, playbook]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [jtbd, trunk-branch-leaf, runbook]
---

# JTBD — Senior Engineer & Architect (OIS-CFA)

## TL;DR
- Bring-up dev env fast (compose) with clear health checks and creds.
- Codify architecture (C4/ERD) as SSOT in one MD; keep reposcan JSON.
- Define DoD MVP + smoke flows; gate migrations; prefer increment over refactors.

## Checklist (DoD)
- [x] Reposcan JSON placed (shotgun-pro format)
- [x] Combined C4 (C1–C4) + ERD in one MD
- [x] DoD MVP doc with acceptance checks
- [x] CFA1 deploy runbook; low-RAM strategies (swap, sequential builds)
- [x] Identity + Registry + Compliance up with health
- [ ] Issuance + Settlement up and smoke flows via Gateway
- [ ] Seed demo data; Postman/K6 smoke script
- [ ] CI: build images, basic compose up on runner

## Sources (SSOT)
- `repositories/customer-gitlab/ois-cfa` (services, compose, docs)
- `memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/*`
- `repositories/customer-gitlab/temp-ai-ois-cfa-20251111-1243/reposcan/shtgn/20251111-1336-co-3a68/*`

## Next Actions
1) Build/start `issuance-service` and `settlement-service` (gate migrations).
2) Start `api-gateway`; verify `/swagger` and route health.
3) Smoke: create issuance → place order (Idempotency-Key) → wallet → settlement run.
4) Capture commands/logs to runbook and commit to `deploy`.


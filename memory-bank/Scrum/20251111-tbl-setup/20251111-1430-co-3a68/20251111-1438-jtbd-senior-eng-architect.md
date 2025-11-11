---
created: 2025-11-11 14:35
updated: 2025-11-11 14:35
type: planning
sphere: [finance, blockchain]
topic: [jtbd, roadmap, mvp]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [jobs-to-be-done, architecture, senior-engineer]
---

# JTBD — Senior Engineer/Architect (MVP Primary)

## Outcomes (MVP exit criteria)
- Primary issuance E2E: issuance → order (idempotent) → wallet update → redeem → settlement batch → payouts report.
- Auth via Keycloak (OIDC), ESIA mocked and documented.
- Bank nominal integration via sandbox/stub with contract tests.
- Observability baseline: structured logs, metrics, basic alerts.
- SSOT governance in place (Trunk gating, indices up-to-date).

## Cross‑cutting JTBD
- [ ] Trunk governance (CI gates)
  - [ ] Add workflows: validate‑manifests, lint‑manifests, update‑checksums on PR to Trunk
  - [ ] Block merge on failures; publish short report in PR
- [ ] Branch lifecycle
  - [ ] Branch templates (goals/APIs/docs/risks/DoD links)
  - [ ] Weekly domain review: owners update status vs DoD
- [ ] Leaf ingestion
  - [ ] Script "branch‑sync": discover new leaves (YYYYMMDD‑HHMM), update Branch + Trunk indices
  - [ ] Enforce anchors to source files (OpenAPI/DbContext/Services)

## Domain JTBD
Identity (Owner: aleksandr‑o)
- [ ] Keycloak realm export (clients/roles)
- [ ] ESIA mock provider (/.well-known, /authorize, /token, /userinfo)
- [ ] OIDC smoke tests scripted (curl + Postman collection)
Done‑when: OpenAPI passes, smoke green locally (compose), realm exported.

Issuance (Owner: alex‑a)
- [ ] Create/Publish/Close endpoints wired to EF + Outbox
- [ ] Fabric adapter path verified (feature‑flag off by default)
- [ ] Unit/service tests for status transitions
Done‑when: 201/200 per spec; events in Outbox; tests green.

Registry (Owner: alex‑a)
- [ ] /v1/orders idempotency enforced; wallet update path
- [ ] Outbox publisher covers order events
- [ ] Wallet query performance (indexing)
Done‑when: duplicate order returns 409; wallet reflects fills.

Settlement (Owner: aleksandr‑o)
- [ ] /v1/settlement/run enqueues batch; reconciliation path
- [ ] Bank nominal stub/sandbox + contract tests
- [ ] Payouts report correctness on synthetic data
Done‑when: 202 Accepted; report matches expected dataset.

Compliance (Owner: yury‑m)
- [ ] /v1/compliance/kyc/check persists KycResult
- [ ] /v1/compliance/qualification/evaluate policy documented
- [ ] Complaints endpoints (create/get) ready for audit
Done‑when: endpoints return per spec; audit trail present.

Custody (Owner: aleksandr‑o)
- [ ] Wallet lifecycle documented (MVP level)
- [ ] HSM/MPC options compared; decision deferred → v1.1
Done‑when: decision record exists; risks logged.

## NFR/Observability JTBD
- [ ] Logging: correlation id, structured fields (service, requestId, userId)
- [ ] Metrics: req/sec, p95 latency, error rate across services
- [ ] Alerts: 5xx burst, DB connectivity, Kafka lag (if enabled)
Done‑when: /metrics exposed; basic alert rules saved.

## Security/Compliance JTBD
- [ ] STRIDE context validated vs current endpoints
- [ ] ГОСТ 57580 checklist: baseline controls mapped to services
- [ ] Secrets handling documented (env, vault TBD)
Done‑when: checklist file updated; gaps logged with owners.

## CI/CD & DevEx JTBD
- [ ] Add make targets for smoke, sdk‑gen, validate‑specs
- [ ] OpenAPI → SDK TS generation in CI (artifact)
- [ ] Pre‑commit formatting/lint (where applicable)
Done‑when: one‑command flows exist; CI publishes SDK.

## Docs JTBD (SSOT)
- [ ] High‑Level updated with current C4/ERD links
- [ ] DataModel.md synced with ERD (MVP entities)
- [ ] ESIA/OIDC sequence reflects Keycloak realm and mock
Done‑when: links resolve; owners signed off.

## Timeline (suggested)
Week 1–2: Trunk gates, Identity (realm+mock), Issuance basics, ERD sync
Week 3–4: Registry (idempotency+wallet), Settlement stub, Observability
Week 5–6: Compliance endpoints, Reports, Contract tests, CI artifacts
Week 7–8: Buffer for external integrations, NFR polish, Docs sign‑off

## Dependencies/Risks
- ESIA: access to test profiles → mock until granted
- Bank nominal: sandbox contract → stub + contract tests until real
- Fabric: test network deployment capacity → feature‑flagged

## Links
- DoD MVP: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1413-dod-mvp-ois-cfa.md
- C4+ERD: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1336-c4-diagrams.md
- Trunk Index: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/trunk-index.md


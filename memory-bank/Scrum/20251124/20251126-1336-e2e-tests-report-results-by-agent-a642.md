---
created: 2025-11-26 13:36
updated: 2025-11-26 13:36
type: report
sphere: exchange
topic: e2e-tests-report
author: codex
agentID: unknown
partAgentID: [co-76ca]
version: 0.1.0
tags: [playwright, swagger, cfa1]
---

| e2e-title | playwright | filename | status | Description | Comment |
| --- | --- | --- | --- | --- | --- |
| Swagger gateway availability | yes | tests/swagger-availability.spec.ts | work | Gateway swagger index reachable (HTTP 200) on CFA1 | Passed with default env; trace kept in playwright report |
| Swagger all services | yes | tests/swagger-all-services.spec.ts | notWork | Issuance/registry/settlement/compliance swagger endpoints return 404 on CFA1 | Needs redeploy with `SWAGGER_ENABLED=true` for core services |
| Issuer reports flow | no | tests/issuer-reports.spec.ts | notRun | Not executed in this session | Run after swagger endpoints fixed if needed |
| Backoffice KYC | no | tests/backoffice-kyc.spec.ts | notRun | Not executed in this session | Run on demand after config changes |

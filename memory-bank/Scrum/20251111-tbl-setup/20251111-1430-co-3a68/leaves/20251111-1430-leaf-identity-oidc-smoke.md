---
created: 2025-11-11 14:30
updated: 2025-11-11 14:30
type: checklist
sphere: [finance, blockchain]
topic: [leaf, identity, smoke]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [leaf, smoke, oidc]
---

# Leaf — Identity OIDC Smoke Plan

Source APIs: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-identity.yaml

## Steps
- [ ] GET /.well-known/openid-configuration (200) — base URLs present
- [ ] GET /authorize (302) — redirect (mock/Keycloak)
- [ ] POST /token (200) — returns access_token
- [ ] GET /userinfo (200) — subject and claims available

## Notes
- Use docker-compose stack; create test realm/clients; mock ESIA callback.
- Record curl examples in DoD MVP smoke block.

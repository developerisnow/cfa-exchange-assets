---
created: 2025-11-11 14:30
updated: 2025-11-11 14:30
type: planning
sphere: [finance, blockchain]
topic: [domain, identity]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [branch, oidc, esia]
---

# Domain Branch — Identity

Owner: aleksandr-o
Status: planned
Capabilities: kyc, kyb, authn, authz
Repos: ois-cfa, main-docs

## Goals (MVP)
- OIDC/Auth (Keycloak), базовый флоу ESIA (mock).
- Realm конфигурация: клиенты/роли, экспорт.

## APIs
- Gateway (auth surface): repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-gateway.yaml
- Identity: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-identity.yaml

## Key Docs
- ESIA/OIDC sequence: memory-bank/repo-cfa-rwa/architecture/11-Sequence-ESIA-OIDC.md
- HLA context: memory-bank/repo-cfa-rwa/architecture/10-HighLevel-Architecture.md

## C4/ERD Anchors
- C1/C2/C3/ERD: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1336-c4-diagrams.md

## Risks
- ESIA редиректы и атрибуты; Keycloak realm миграции.

## DoD
- См. DoD MVP: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1413-dod-mvp-ois-cfa.md

## Leaf Examples
- OIDC mock smoke: /.well-known, /authorize, /token, /userinfo.

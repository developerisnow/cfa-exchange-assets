---
created: 2025-11-11 14:30
updated: 2025-11-11 14:30
type: planning
sphere: [finance, blockchain]
topic: [domain, tokenization]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [branch, issuance]
---

# Domain Branch — Tokenization

Owner: alex-a
Status: planned
Capabilities: minting, issuance, corp-actions
Repos: ois-cfa, main-docs

## Goals (MVP)
- Создать/публиковать/закрывать выпуск; redeem; базовые корпоративные действия позже.

## APIs
- Gateway (issuances): repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-gateway.yaml
- Issuance: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-issuance.yaml

## Key Docs
- Правила ИС (template): memory-bank/repo-cfa-rwa/legal/01-ПравилаИС-template.md
- Data Model: memory-bank/repo-cfa-rwa/architecture/12-DataModel.md

## C4/ERD Anchors
- C2/C3/ERD: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1336-c4-diagrams.md

## Risks
- Связка с ledger (Fabric) через gateway; корректность жизненного цикла в БД.

## DoD
- См. DoD MVP

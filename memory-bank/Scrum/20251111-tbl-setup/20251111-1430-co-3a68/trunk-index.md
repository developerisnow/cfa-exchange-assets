---
created: 2025-11-11 14:30
updated: 2025-11-11 14:30
type: architecture
sphere: [finance, blockchain]
topic: [trunk-branch-leaf, ssot-index]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [ssot, index, navigation]
---

# Trunk · SSOT Index (Cifra RWA)

## Purpose
- Единая точка входа (Trunk) для архитектуры, API, data, security и деплоя.
- Отсюда ссылки на Branch‑страницы доменов и Leaf‑артефакты.

## Key SSOT Docs (Docs repo)
- High‑Level Architecture: memory-bank/repo-cfa-rwa/architecture/10-HighLevel-Architecture.md
- ESIA/OIDC Sequence: memory-bank/repo-cfa-rwa/architecture/11-Sequence-ESIA-OIDC.md
- Data Model: memory-bank/repo-cfa-rwa/architecture/12-DataModel.md
- Non‑Functional Targets: memory-bank/repo-cfa-rwa/architecture/14-NonFunctional-Targets.md
- Threat Model (STRIDE): memory-bank/repo-cfa-rwa/architecture/threat/STRIDE-Context.md
- Threat Mitigations: memory-bank/repo-cfa-rwa/architecture/threat/Mitigations-Map.md
- Security Checklist (ГОСТ 57580): memory-bank/repo-cfa-rwa/security/20-ГОСТ57580-Чеклист.md
- Legal — Правила ИС: memory-bank/repo-cfa-rwa/legal/01-ПравилаИС-template.md
- Legal — Описание ИС: memory-bank/repo-cfa-rwa/legal/02-ОписаниеИС-template.md

## APIs (OpenAPI/AsyncAPI)
- Gateway: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-gateway.yaml
- Identity: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-identity.yaml
- Issuance: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-issuance.yaml
- Registry: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-registry.yaml
- Settlement: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-settlement.yaml
- Compliance: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-compliance.yaml
- Integrations Bank: repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-integrations-bank.yaml
- AsyncAPI: repositories/customer-gitlab/ois-cfa/packages/contracts/asyncapi.yaml

## Deploy
- Local: repositories/customer-gitlab/ois-cfa/docker-compose.yml
- HLF Helm: repositories/customer-gitlab/ois-cfa/ops/helm/

## Manifests (SSOT indices)
- Project: project.manifest.json
- Indices: manifests/people.manifest.json, manifests/domains.manifest.json, manifests/repositories.manifest.json, manifests/workflow.manifest.json, manifests/docs.manifest.json, manifests/repo-structure.manifest.json

## Domain Branches
- Identity: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/branches/identity.md
- Tokenization: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/branches/tokenization.md
- Exchange: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/branches/exchange.md
- Settlement: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/branches/settlement.md
- Compliance: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/branches/compliance.md
- Custody: memory-bank/Scrum/20251111-tbl-setup/20251111-1430-co-3a68/branches/custody.md

## Leaf Artifacts (Examples)
- Reposcan JSON + C4+ERD: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/
- DoD MVP: memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1413-dod-mvp-ois-cfa.md

## Process Guards
- Validate JSON: scripts/validate-manifests.sh
- Lint manifests/links: scripts/lint-manifests.sh
- Update checksums: scripts/update-checksums.sh

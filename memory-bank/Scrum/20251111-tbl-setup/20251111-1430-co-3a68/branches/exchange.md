---
created: 2025-11-11 14:30
updated: 2025-11-11 14:30
type: planning
sphere: [finance, blockchain]
topic: [domain, exchange]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [branch, orderbook]
---

# Domain Branch — Exchange

Owner: alex-a
Status: planned
Capabilities: orderbook, matching, market-data (после MVP)
Repos: ois-cfa, velvet, main-docs

## Goals (MVP)
- Вторичный рынок исключён. На MVP используем Registry /orders как прием заявок (primary placement).

## APIs
- Registry (orders): repositories/customer-gitlab/ois-cfa/packages/contracts/openapi-registry.yaml

## Key Docs
- HLA: memory-bank/repo-cfa-rwa/architecture/10-HighLevel-Architecture.md
- Velvet (legacy exchange) как справочник: repositories/customer-gitlab/velvet

## Risks
- Перенос в v1.1/v1.2: RFQ/OTC → аукционы/книги.

## DoD
- На MVP — нет. Ссылка на DoD MVP для primary.

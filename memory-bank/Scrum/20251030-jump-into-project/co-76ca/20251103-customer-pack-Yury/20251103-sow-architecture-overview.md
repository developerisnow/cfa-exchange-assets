---
created: 2025-11-03 15:34
updated: 2025-11-03 15:34
type: sow-architecture
sphere: [architecture, planning]
topic: [sow, c4, domains]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [sow, architecture, c4]
---
next: [[roadmap]]
previous: [[README-v2]]
related: [[20251004-estimation-from-outsource-company]], [[20251030-1925-gpt5h-conversion-development-capital-platform-diagrams]], [[20251030-1926-son4.5-conversion-development-capital-platform-diagrams]], [[../ge-4V2i/20251103-1506-gem2.5p-ge-4V2i.session]]
# Why → What → How → Result

- Why: за 20 часов ресёрча выстроить единое архитектурное видение ОИС «Капитал» (только первичка), согласованное с рыночной практикой РФ ЦФА и с исходной оценкой подрядчика.
- What: обзор C4 (Context/Containers), список доменов и интеграций, SoW Discovery‑блока (50h), принципы реализации и критерии приёмки.
- How: используем референс‑док «Оценка от подрядчика» + диаграммы (GPT5h/Son4.5) как основу, уточняем через конкурентный обзор (20 платформ), фиксируем DoD и шаги.
- Result: утверждённый SoW Discovery (50h) и маршрут к MVP (10–12 недель) с минимальными рисками.

# References

- [[../../context/current-context/additional-info-for-analysing/20251004-estimation-from-outsource-company/20251004-estimation-from-outsource-company.md]]
- [[../../context/current-context/additional-info-for-analysing/20251004-estimation-from-outsource-company/20251030-1925-gpt5h-conversion-development-capital-platform-diagrams.md]]
- [[../../context/current-context/additional-info-for-analysing/20251004-estimation-from-outsource-company/20251030-1926-son4.5-conversion-development-capital-platform-diagrams.md]]
- [[../ge-4V2i/20251103-1506-gem2.5p-ge-4V2i.session.md]] (Prompt‑2: акценты и план)
- [[competitors-all-in-one]] (20 платформ РФ)

# C4 — Context/Containers (summary)

- Context: Эмитент, Инвестор, Профучастник/Брокер, Банк/НСПК, Регулятор → Платформа «Капитал» (ОИС ЦФА)
- Containers (MVP):
  - Gateway (OAuth2/OIDC, WAF)
  - Registry (участники/роли), Identity/KYC (KEP/УКЭП), Tokenization (выпуск и условия), Settlement (DvP T+0 с 1 банком), Custody (HSM/MPC), Disclosure/Reporting
  - Ledger (permissioned DLT или audit‑core) — решение после Discovery

# Domains & Integrations (MVP)

- Identity/KYC (KEP/УКЭП 63‑ФЗ), Registry (ABAC), Tokenization (выпуск/корп.действия базовые), Settlement (DvP T+0), Custody (HSM/MPC), Disclosure (раскрытия, отчётность минимум)
- Интеграции: банк‑rails (ISO 20022/SBP), УКЭП‑провайдеры, TSA; позже — вторичка (RFQ/OTC)

# SoW — Discovery Block (50h, paid)

- Deliverables (измеримые):
  - C4 Context/Containers (обновляемые исходя из требований Юрия)
  - Каталог доменных событий и схем (согласованный)
  - Черновики API‑контрактов (ключевые эндпоинты per‑domain)
  - Ledger‑memo: Fabric/Besu vs audit‑core (immudb). Решение — затем, после сопоставления рисков
  - Shortlist: банк (1–2) для DvP, УКЭП/ГОСТ провайдер (1–2) с SDK/SLAs
  - MVP‑план (10–12 недель) и DoD per‑slice
- Acceptance (DoD):
  - Согласованная C4 (Context/Containers)
  - Утверждённые события/контракты API (черновой уровень)
  - Принятый shortlist (банк/УКЭП) и критерии выбора
  - Утверждённый MVP‑план (primary only)

# Principles & Non‑Functionals (ориентиры)

- Security/Compliance: 259‑ФЗ, 63‑ФЗ (УКЭП), AML/CFT; шифрование, локализация 152‑ФЗ
- Observability/DR: логи, метрики, трассировка; бэкапы, DR‑план
- Extensibility: event‑first + adapter к ledger для anti‑lock‑in

# Result → Roadmap (см. [[roadmap]])

- MVP 10–12 недель, параллельные треки: архитектура/события, банк‑rails/УКЭП, compliance, data/reporting, UX прототипы


---
created: 2025-11-03 12:00
updated: 2025-11-03 12:00
type: presentation
sphere: [client]
topic: [mvp, discovery]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [slides, brief]
---

Заголовок
- ОИС ЦФА — стартовый пакет: Discovery 40h и MVP 10–12 недель (только первичный рынок).

TL;DR
- MVP Scope: Registry/KYC, Tokenization, Custody (HSM/MPC), Settlement DvP T+0 (1 банк), Disclosure/Audit.
- Подход: Spec‑first (OpenAPI + event‑schemas), CQRS/Kafka, ledger‑adapter, аудит‑след ≥7 лет.
- Комплаенс: 259‑ФЗ, 63‑ФЗ (КЭП/УКЭП), AML/CFT, PDН, TSA/time‑stamps.

Discovery 40h — Deliverables
- C4 (Context/Containers) и каталог доменных событий.
- Черновики API‑контрактов и список интеграций.
- Ledger memo (Fabric/Besu vs immudb audit‑core) без финального выбора.
- Shortlist: банк‑rails (1–2) и УКЭП/ГОСТ вендоры.
- План MVP (10–12 недель) и DoD.

Рынок РФ (итог ресёрча)
- 20 платформ — витрина (DLT/DvP/вторичка/API/лицензии). 4 платформы в глубину (Batch‑1).
- Lighthouse DvP = unknown (честная фиксация, нет достоверных подтверждений в публичных источниках).

Архитектура (направление)
- Permissioned DLT (Fabric/Besu) или быстрый audit‑core (immudb) с путём к полной DLT.
- Event‑first, ledger‑adapter (без lock‑in), независимое якорение хэшей.

Команда и каденс
- Арх/Лид, 2 BE, 1 FE, 1 DevOps/Sec, 0.5 BA, 0.5 QA. Еженедельные демо.

Сроки/бюджет (ориентир)
- Discovery: 40h ($2k–$2.5k). MVP core: 400–600h ($20k–$30k при $50/h) + интеграции.

Next Steps
- Утвердить Discovery 40h и провести 90‑мин Kickoff.
- Подтвердить shortlist: Ledger (направление), Банк‑rails, УКЭП/ГОСТ.
- Зафиксировать acceptance/DoD и согласовать формат отчётности.


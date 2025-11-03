---
created: 2025-11-03 12:05
updated: 2025-11-03 12:05
type: call-brief
sphere: [client]
topic: [call, agenda]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
agentIDPart: 76ca
partAgentID: [co-76ca]
version: 1.0.0
tags: [brief, agenda]
---

Цель звонка (30–60 минут)
- Уверенно показать «что сделано», «что предлагаем», «какие решения нужны».
- Оставить только 10% айсберга: достижения, выборки и конкретные шаги.

Agenda (предложение)
- 0–5 мин — Контекст и цель (почему сейчас, что важно).
- 5–15 мин — Достижения недели (витрина конкурентов 20; глубина 4; MVP план/архитектура; SOW/Discovery 40h).
- 15–25 мин — Ключевые решения и трейд‑оффы (Ledger, Банк‑rails, УКЭП/ГОСТ) — по 2–3 тезиса с «почему».
- 25–35 мин — План Discovery 40h и DoD (что сдаём, как измеряем, риски/mitigation).
- 35–45 мин — Вопросы/ответы; фиксация решений и следующих шагов.
- 45–60 мин — Буфер либо завершаем раньше.

Что достигнуто (10% выжимка)
- Конкуренты РФ: 20 платформ (DLT/DvP/вторичка/API/лицензии), 4 в глубину с источниками и QA. Lighthouse DvP = unknown (честно).
- MVP план (только первичка): Registry/KYC, Tokenization, Custody (HSM/MPC), DvP T+0 с 1 банком, Disclosure/Audit.
- Архитектурное направление: spec‑first, CQRS/Kafka, ledger‑adapter; audit‑core (immudb) как быстрый старт с путём к Fabric/Besu.
- Client‑pack: презентация, weekly‑report, SOW Kickoff, roadmap, глоссарий.

Ключевые решения (нужны от Юрия)
- Ledger подход на Discovery: (A) immudb audit‑core → путь к Fabric/Besu, или (B) сразу Fabric/Besu (ops сложнее).
- Банк‑rails shortlist: 1–2 кандидата для DvP T+0 (escrow, ISO 20022, reconciliation).
- УКЭП/ГОСТ провайдеры shortlist: 2–3 вендора (SDK/SLAs/цены).

Почему так (коротко)
- Быстрый регуляторно‑готовый MVP, без lock‑in; честные unknowns и измеримые DoD.

Next Steps
- Подтвердить Discovery 40h и назначить 90‑мин Kickoff (C4/события/API/решения/риски).
- Зафиксировать решения и даты (decision‑log), старт интеграционных контактов.


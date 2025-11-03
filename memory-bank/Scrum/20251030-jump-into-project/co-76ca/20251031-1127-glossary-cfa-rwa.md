---
created: 2025-10-31 11:27
updated: 2025-10-31 11:27
type: glossary
sphere: [rwa, cfa, fintech]
topic: [terms, roles, processes]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [glossary, dictionary]
---

TL;DR
- Сводный словарь терминов по ЦФА/РВА (регуляторика, роли, процессы, технологии, интеграции, отчётность).
- Формат: краткое определение + «где в проекте» + «что проверить/мерить».

Регуляторика (RU)
- 259‑ФЗ — ЦФА/ОИС: что можно, обязанности, оператор обмена.
- 63‑ФЗ — КЭП/УКЭП: ГОСТ, провайдеры подписей, хранение ключей.
- 152‑ФЗ — ПДн/локализация: хранение данных в РФ.

Роли и контуры
- ОИС (оператор информационной системы) — платформа выпуска/учёта ЦФА.
- Оператор обмена — организация вторичного рынка ЦФА.
- Депозитарий/Регистр — учёт прав, корпоративные действия.

Процессы
- Эмиссия — подготовка условий, выпуск токена, раскрытия.
- Размещение — сбор заявок, распределение.
- DvP (Delivery‑vs‑Payment) — атомарная поставка «ЦФА↔деньги» (T+0/T+1).
- Вторичка — RFQ/OTC → ордербуки/аукционы.

Технологии
- DLT: Hyperledger Fabric (каналы, RAFT/SmartBFT), Besu/Quorum (IBFT/RAFT), Masterchain/Waves (локальные стеки), immudb (audit‑core).
- Custody: HSM/MPC, M‑of‑N, BYOK, key rotation.
- УКЭП/ГОСТ: CryptoPro, КриптоПро HSM/СКЗИ, TSA.

Интеграции
- Банки/НСПК/СБП, ISO 20022, webhooks.
- Госуслуги/ЕСИА (KYC/KYB), санкционные списки/AML.

Отчётность/Аудит
- XBRL/ISO 20022 выгрузки, Disclosure/раскрытия, retention 5–7 лет, hash‑anchoring.

Метрики
- Latency/finality (ledger), TPS, p95 end‑to‑end (Emission→DvP), SLA банков/УКЭП.

Glossary Table (to expand)

| RU term | EN analog | Domain | Why important | Key differences | Related | Checks/Metrics |
|---|---|---|---|---|---|---|
| ОИС (оператор инф. системы) | OIS/CFA platform | regulation | Правовой статус платформы | Оператор обмена ≠ ОИС | Регистратор, Депозитарий | Лицензии ЦБ, реестр |
| ЦФА | DFA/CFA | finance | Базовый объект учёта | Security vs Utility | Токенизация, облигации | Disclosure, XBRL |
| DvP | Delivery‑vs‑Payment | settlement | Атомарность расчётов | T+0 vs T+1 | ISO 20022, СБП | Finality, отказоустойчивость |
| УКЭП | QES (qualified e‑signature) | compliance | Юр. значимость операций | ГОСТ/СКЗИ | CryptoPro, TSA | Подписи, журналы |

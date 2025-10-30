TL;DR
- Набор промптов для MCP/LLM‑исследования по критическим решениям MVP.
- Сфокусировано на регуляторике РФ (ЦФА), DLT‑вариантах, КЭП/УКЭП, AML, банках.
- Структура: блоки Why→What→How→Deliverable, чтобы экономить токены.

Prompts — Ledger Selection
1) Why: permissioned DLT vs audit‑core для ОИС ЦФА в РФ.
   What: сравнить Fabric/Besu/immudb по ops‑сложности, приватности, аудит‑следам, latency.
   How: собрать 6–8 практических отзывов (StackOverflow, HN, Reddit), 3–5 prod‑кейсов.
   Deliverable: таблица 6×6 + рекомендация для MVP и миграционного пути.

Prompts — KEP/УКЭП Integration (63‑ФЗ)
2) Why: связка аккаунтов с КЭП/УКЭП и mTLS.
   What: провайдеры/SDK в РФ, стоимость/SLAs, примеры интеграций.
   How: собрать SDK, API, требования по хранению ключей, ГОСТ crypto.
   Deliverable: чеклист внедрения + риски.

Prompts — AML/CFT
3) Why: сценарии мониторинга для ЦФА.
   What: провайдеры санкционных списков, правила тревог, PEP.
   How: best‑practices РФ/ЕС, кейсы внедрения.
   Deliverable: конфиг‑матрица правил (низк/сред/высокий риск).

Prompts — DvP Rails
4) Why: атомарные расчёты с одним банком.
   What: схемы escrow, reconciliation, ISO 20022 сообщения.
   How: примеры из НРД/СПБ/СБП; требования SLA.
   Deliverable: sequence‑диаграмма и risk‑лог.

Prompts — Secondary Market
5) Why: RFQ/OTC до ордербуков.
   What: модели доступа/допусков, авторизация заявок, комплаенс‑контроль.
   How: кейсы российских площадок ЦФА.
   Deliverable: спецификация RFQ API + события.

Prompts — Sanctions/BRICS Stack
6) Why: стек без санкционных рисков.
   What: HSM/MPC отечественные аналоги, регуляторные ограничения.
   How: опрос производителей/интеграторов.
   Deliverable: shortlist с плюсами/минусами.

Meta
- agentID=019a362f-76ca-7272-909e-362716cf233d partAgentID=76ca

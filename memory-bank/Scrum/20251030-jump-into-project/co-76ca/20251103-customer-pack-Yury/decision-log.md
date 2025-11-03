---
created: 2025-11-03 12:20
updated: 2025-11-03 12:20
type: decision-log
sphere: [governance]
topic: [decisions]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
agentIDPart: 76ca
partAgentID: [co-76ca]
version: 1.0.0
tags: [log, decisions]
---

TL;DR
- Единый журнал решений для короткого созвона: что уже зафиксировано, что требуется решить, опции и обоснование.

Формат
- DEC_ID | Тема | Статус | Владелец | Дата/дедлайн | Опции | Выбор | Обоснование | Ссылки | Next

Решения

| DEC_ID | Тема | Статус | Владелец | Дата/дедлайн | Опции | Выбор | Обоснование | Ссылки | Next |
|---|---|---|---|---|---|---|---|---|---|
| DEC-001 | MVP Scope (только первичка) | decided | Alex | 2025-10-31 | Primary‑only vs Primary+Secondary | Primary‑only | Быстрый ценностный MVP, снижение сложности, вторичка в v1.1 | 76ca/presentation.md; 76ca/roadmap.md | Зафиксировать DoD и тест‑кейсы |
| DEC-002 | Ledger подход на Discovery | pending | Yury | 2025-11-06 | (A) immudb audit‑core → путь к Fabric/Besu; (B) сразу Fabric/Besu | — | (A) быстрее и проще по ops; (B) богаче возможности, но setup тяжелее | 76ca/presentation.md; 76ca/weekly-report.md | Выбрать направление, заморозить интерфейсы |
| DEC-003 | Банк‑rails shortlist (DvP T+0) | pending | Yury | 2025-11-08 | Банк‑A, Банк‑B (escrow, ISO 20022, reconciliation) | — | Для MVP нужна атомарность расчётов и SLA | 76ca/weekly-report.md | Утвердить shortlist, согласовать контакт |
| DEC-004 | УКЭП/ГОСТ провайдеры shortlist | pending | Yury | 2025-11-08 | Поставщик‑1/2/3 (SDK, SLAs, цены) | — | Связность аккаунтов и подписей по 63‑ФЗ | 76ca/weekly-report.md | Выбрать 2–3, старт интеграции |
| DEC-005 | Discovery 40h SOW | proposed | Alex | 2025-11-04 | Принять/не принять | Принять | Быстрый риск‑снятие и выработка C4/событий/API/shortlists | 76ca/kickoff-pack.md | Назначить 90‑мин Kickoff |
| DEC-006 | Reporting cadence (TimeLog v2, Weekly) | decided | Alex | 2025-10-31 | Разные форматы | TimeLog v2 + Weekly | Прозрачность, трассировка DoD и затрат | repo reporting docs; 76ca/weekly-report.md | Применять еженедельно |
| DEC-007 | Lighthouse DvP статус | acknowledged | Alex | 2025-10-31 | confirmed/likely/unknown | unknown | Нет достоверных источников в доступной пачке | 76ca/batch1-qa.md | Повторная проверка в Discovery |

Примечания
- owner Alex = исполнитель/архитектор; Yury = заказчик/согласователь. Имена можно подставить точные при Kickoff.


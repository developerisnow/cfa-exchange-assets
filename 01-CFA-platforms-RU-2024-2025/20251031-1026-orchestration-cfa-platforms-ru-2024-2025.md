---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-orchestration
sphere: [automation]
topic: [runner, curation]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [runner, jsonl, thread-mode]
---

TL;DR
- Runner по платформам: батчи по 4, Thread Mode, JSONL‑карточки + markdown сводка и mermaid.
- Early‑stop: прекращаем, если по ключевым полям ≥2 независимых источника или данных нет (unknown) — дополнительные прогоны не дадут прироста.

Steps
1) Batch: брать 4 платформы → запускать 5 провайдеров (по 1 прогону) → собирать JSON cards.
2) Thread Mode: файл «competitors-thread.md» с H1 на платформу; в конце — JSON карточка.
3) Export: карточки в `competitors.jsonl` (по 1 в строке), сводка в `competitors.md`.
4) Index: обновлять manifest и локальный index с полями {name, last_checked, files}.
5) Early‑stop: если поля dlt/ukep/dvp подтверждены ≥2 источниками, а прочее повторяет найденное → стоп.

Table — Naming
- `01-CFA-platforms-RU-2024-2025/{yyyymmdd-hhmm}-{provider}-{model}-CFA-platforms-RU-2024-2025.deepresearch.{md|json|jsonl}`

Next actions
- Запуск по первому батчу (Атомайз, НРД, Сбер, Лайтхаус), затем расширение по списку.


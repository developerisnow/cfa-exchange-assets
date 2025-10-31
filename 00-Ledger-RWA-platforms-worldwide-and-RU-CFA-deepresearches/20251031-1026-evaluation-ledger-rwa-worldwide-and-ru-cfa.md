---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-evaluation
sphere: [metrics]
topic: [quality, decision]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [scoring, early-stop]
---

TL;DR
- Метрики: Coverage, Precision, Novelty, Actionability, Consistency, Cost. Пороговые значения и ранняя остановка.
- Решение: нужен ли 2‑й прогон/ещё провайдер — по приросту качества и стоимости.

Steps (Scoring)
1) Coverage (0–1): покрытие ключевых разделов (ledger types, ops, privacy, latency, tooling, RU‑CFA).
2) Precision (0–1): доля claims с high‑confidence, проверенных ≥2 источниками ≤24 мес.
3) Novelty (0–1): доля уникальных claims относительно существующего пула.
4) Actionability (0–1): есть конкретные PoC шаги/метрики/конфигурации.
5) Consistency (0–1): отсутствие внутренних противоречий; пометки contested.
6) Cost: $ по отчёту (включая время на обработку).

Decision Rules
- Если Coverage≥0.8, Precision≥0.8, Novelty прирост<0.1 → стоп прогоны.
- Если любой из Coverage/Precision<0.6 → добавить ещё 1 прогон другого провайдера.
- Если Actionability<0.6 → запросить уточняющий промпт (PoC‑детализация).

Table — Weights (composite score)
- Coverage 0.25; Precision 0.25; Novelty 0.15; Actionability 0.2; Consistency 0.1; Cost −0.05.

Next actions
- Применить на текущих 20 отчётах; выбрать финальный стек (Besu/Quorum vs Fabric vs immudb) и PoC‑план.


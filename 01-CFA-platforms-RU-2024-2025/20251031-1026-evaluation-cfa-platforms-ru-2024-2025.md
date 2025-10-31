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
tags: [scoring, ru]
---

TL;DR
- Метрики для платформ РФ: Evidence Count, Freshness, Field Coverage, Consistency, Conflict Resolution, Effort.
- Решаем: достаточно ли 1 провайдера×1 прогон или добавлять ещё, по приросту уверенности.

Steps (Scoring)
1) Evidence Count (0–1): среднее подтверждений на критичное поле (dlt/ukep/dvp) — нормировать к 2+ источникам.
2) Freshness (0–1): доля источников ≤24 мес.
3) Field Coverage (0–1): доля заполненных полей в карточке платформы.
4) Consistency (0–1): отсутствие внутренних противоречий; contested → штраф.
5) Conflict Resolution (0–1): наличие объяснённого выбора между версиями (с confidence).
6) Effort (−): время/стоимость отчёта.

Decision Rules
- Если Evidence Count≥0.8, Freshness≥0.8, Field Coverage≥0.8 → достаточно; не запускаем дополнительные прогоны.
- Если любой <0.6 → добавить провайдера с иным профилем (напр., Perplexity → source‑heavy).

Next actions
- Оценить текущие отчёты, выделить платформы с недостаточными данными и перезапустить только их.


---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-pipeline
sphere: [ledger, rwa, cfa]
topic: [worldwide, ru]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [pipeline, extraction, consolidation]
---

TL;DR
- Четырёхслойный pipeline: Raw → Claims → Resolution → Deliverables, с ID‑трассировкой по каждому отчёту.
- Выходы: JSONL claims, consolidated facts, сравнение Ledger (Besu/Quorum vs Fabric vs Audit‑core), PoC‑план.
- Контроль качества: coverage, precision, novelty, actionability; ранняя остановка при достижении порогов.

Steps
1) Ingest (Raw): собрать все отчёты (OpenAI/Anthropic/Perplexity/Gemini/Parallel) и присвоить runID=`{case}-{yyyymmdd-hhmm}-{provider}-{model}-{n}`.
2) Extract (Claims): парсинг в JSONL (1 claim/row) с полями: claim_id, text, provider, sources[], date, confidence.
3) Resolve (Dedup/Conflicts): кластеризация похожих claims (cosine≥0.85), выбор опорных фактов по source‑весу/дате/перекрёстным подтверждениям.
4) Consolidate (Facts): формирование нормализованных фактов + контрфактов; фиксация статуса: confirmed/likely/contested/unknown.
5) Synthesize (Deliverables):
   - Сравнение Ledger: Fabric vs Besu/Quorum vs Audit‑core (immudb) по RU‑CFA требованиям.
   - PoC‑план: Besu RAFT/IBFT, сценарии Emission/DvP/Anchoring, метрики latency/finality/ops.
6) QA & Sign‑off: чек‑лист качества, acceptance для DoD.

Table — Data Model (Claims JSONL)
- claim_id: string (UUID)
- run_id: string
- provider: string (gpt5p|opus4.1|son4.5|gem2.5p|perplexity|parallel)
- case: string (ledger-rwa-worldwide-ru-cfa)
- text: string
- sources: [{url, title, date, reliability: high|mid|low}]
- extracted_at: ISO datetime
- confidence: high|mid|low

Table — Consolidation Heuristics
- Cross‑sources ≥2 независимых → +2 балла
- Свежесть (≤24 мес) → +1 балл
- Официальный источник (регулятор/вендор) → +2 балла
- Косвенный (вакансии/репо) → +0.5 балла
- Итог: ≥4 → confirmed; 3–3.5 → likely; 2–2.5 → contested; <2 → unknown

Next actions
- Сгенерировать claims JSONL для всех 20 отчётов; прогнать резолвер; собрать сводку сравнения Ledger и PoC‑план.

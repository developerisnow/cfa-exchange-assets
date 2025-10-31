---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-pipeline
sphere: [market, cfa]
topic: [russia, platforms]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [pipeline, verification]
---

TL;DR
- Seed из локальных датасетов → per‑platform сбор → JSON cards → консолидация → сводная таблица и диаграммы.
- Верифицируем: DLT/ledger, custody/HSM/MPC, УКЭП/ГОСТ, DvP/банки, вторичка, API/хостинг, метрики, регстатус.

Steps
1) Seed: список платформ из «Статус платформ ЦФА в России» и «CFA_operators» (Основной/Рэнкинг/Фичи).
2) Collect: по каждой платформе собрать источники (RU‑first) и claims JSON (как в схеме из competitor‑prompt).
3) Normalize: привести поля к единой схеме; проставить confidence.
4) Consolidate: объединить противоречивые claims; отметить contested/unknown.
5) Synthesize: таблица сводки + Mermaid по статусам и DLT‑типам.
6) QA: каждый критичный атрибут подтверждён ≥2 источниками или помечен unknown.

Table — Card Fields (short)
- name, status, role[], dlt{type,evidence[]}, custody{type,vendors[]}, ukep{providers[],gost}, dvp{model,banks[],iso20022,sbp}, secondary{rfq,orderbook}, apis, hosting, metrics, issuers[], regulatory, sources[], last_checked, confidence_overall, notes.

Next actions
- Сформировать JSONL cards для 4 приоритетных платформ (Атомайз, НРД, Сбер, Лайтхаус) и сводный md.

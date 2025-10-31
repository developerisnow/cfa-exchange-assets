---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-orchestration
sphere: [ledger]
topic: [automation]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [runner, naming, thread-mode]
---

TL;DR
- Runner‑процедура: 5 провайдеров × до 2 прогонов, единая схема имён, Thread Mode для связности, артефакты JSONL/MD.
- Early‑stop: прекращаем дополнительные прогоны при достижении coverage/novelty порогов.

Steps
1) Naming: `00-Ledger/.../{yyyymmdd-hhmm}-{provider}-{model}-{short}-Ledger-RWA...{.md|.json|.jsonl}`.
2) Thread Mode: один мастер‑файл на провайдера, H1 для каждого прогона; claims JSON — в конец.
3) Export: сохранять md/docx→md; claims JSON выносить в отдельный `.jsonl` (1 claim/line).
4) Index: обновлять project.manifest.json (documents.versioned) и локальный `claims.index.json` (paths, runIDs).
5) Early‑stop правила:
   - Coverage ≥ 80% доменных разделов; Novelty прирост < 10%; Accuracy ≥ порога (см. evaluation).
6) Handoff: передать в pipeline (extract/resolve/synthesize).

Table — Providers
- OpenAI GPT‑5 Pro — высокий сигнал, дорогой; 1 прогон
- Anthropic Opus/Sonnet — 1–2 прогона (разные акценты)
- Perplexity — source‑heavy; 1 прогон
- Gemini 2.5p — хороший код/PoC; 1 прогон
- Parallel — альтернативные пути; опционально 1 прогон

Next actions
- Прописать небольшие скрипты для экспорта claims и индексации; затем запуск по провайдерам.


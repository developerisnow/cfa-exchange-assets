---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-prompts
sphere: [market, cfa]
topic: [russia, platforms]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [prompts, verification]
---

TL;DR
- Единый промпт для верификации per‑platform + провайдер‑специфика; выход: JSON‑карточка и сводный markdown.
- Упор на 2024–2025, RU‑источники, ≥2 подтверждения по ключевым полям.

Base Prompt (all providers)
Goal: Verify and document technology and operations of Russian CFA platforms (2024–2025). For each platform, fill fields: dlt, custody, ukep/gost, dvp/banks/iso20022/sbp, secondary (rfq/orderbook), apis, hosting, metrics, regulatory, issuers. Provide sources with dates.
Output:
  1) Platform JSON card (schema compliant)
  2) One‑line summary row for a markdown table
Constraints:
  - RU‑first sources (official sites/docs, CBR register, NRD, SPB Exchange, reputable media); add English if needed
  - Mark confidence for each field and overall; if unknown → state unknown

Provider Overrides
- OpenAI/Anthropic: focus on high‑confidence facts and multiple independent sources
- Perplexity: list sources with snippets first, then synthesize
- Gemini: add brief “how to integrate” notes (APIs/auth)
- Parallel: produce alternative interpretations when data conflicts, with confidence per version

Answer Style
- Вопрос — Ответ (если нужен уточняющий блок) → JSON card → Markdown row.

Next actions
- Прогнать по топ‑4 платформам, затем расширить на остальные из seed‑списка; передать в pipeline.


---
created: 2025-10-31 10:26
updated: 2025-10-31 10:26
type: research-prompts
sphere: [ledger, rwa]
topic: [worldwide, ru]
author: codex
agentID: 019a362f-76ca-7272-909e-362716cf233d
partAgentID: [co-76ca]
version: 1.0.0
tags: [prompts, standardization]
---

TL;DR
- Унифицированные промпты для 5 провайдеров + провайдер‑специфика; выход: markdown + claims JSON.
- Фокус: 2023–2025 прод‑кейсы, RU‑CFA применимость, ops/privacy/latency/tooling.

Base Prompt (all providers)
Goal: Compare permissioned Ethereum (Besu/Quorum), Hyperledger Fabric, and audit‑core (immudb/append‑only) for RWA/CFA. Focus 2023–2025 production cases, ops complexity, privacy, latency/finality, tooling, and RU‑CFA constraints (259‑ФЗ, УКЭП/ГОСТ, HSM).
Output:
  1) Summary (bullets)
  2) Comparison table (≤12 rows, clear trade‑offs)
  3) PoC plan (phases, metrics)
  4) Claims JSON (array) with fields: {text, sources:[{url,title,date}], confidence}
Constraints:
  - Cite sources inline with [title — yyyy‑mm] and include URLs.
  - Prefer official docs, regulator posts, vendor blogs, reputable media; avoid speculation.
  - RU context: mention УКЭП/ГОСТ/HSM compatibility options and privacy patterns (Tessera/channels).

Provider Overrides
- OpenAI (GPT‑5 Pro): add “produce concise claims array ≤ 50 items with deduped facts”.
- Anthropic (Opus 4.1/Sonnet 4.5): enforce “no hallucinations; if unknown → state unknown; list open questions”.
- Perplexity: “source‑first; enumerate top sources with snippets before synthesis”.
- Gemini 2.5p: “generate PoC steps with k8s manifests outline for Besu/IBFT”.
- Parallel: “multi‑branch; return three alternative PoC paths ranked by feasibility”.

Answer Style
- TL;DR (3 bullets) → Steps → Table → Next actions.
- Claims JSON at the end in a fenced code block labeled json.

Next actions
- Вставить промпт в каждый инструмент (1–2 прогона), сохранить отчёты и claims JSON, следовать pipeline.


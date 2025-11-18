---
created: 2025-11-18 13:10
updated: 2025-11-18 13:10
type: docs
sphere: meta
topic: claude-commands
author: Alex (co-3c63)
agentID: co-019a915c-3c63-7311-b21c-af448053d646
partAgentID: [co-3c63]
version: 0.1.0
tags: [agents, commands, meta]
---

# `.claude/commands` — каркас для команд Meta-Guard Architect

Это каталог для определения типовых команд/поручений, которые будут вызываться
из Meta-Guard Architect и других агентов (Codex/Claude/GPT‑5).

Идея:
- каждая команда описывается отдельным файлом (YAML/JSON/Markdown),
- внутри задаются:
  - тип задачи (NX-00 / NX-0X / utility),
  - целевой уровень (trunk / branch / leaf),
  - рекомендуемый инструмент (Oracle / Codex / CodeMachine / human),
  - минимальный набор входных файлов.

На данный момент каталог служит каркасом; конкретные команды будут добавляться
после фиксации NX‑00 серии и CodeMachine workflow.


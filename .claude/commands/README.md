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

## Available Commands

### Git & Repos
| Command | Description |
|---------|-------------|
| `/commit` | Smart git commits with conventional format |
| `/add-repos` | Discover GitHub repos from markdown and add as submodules |
| `/analyze-repos` | Analyze GitHub repositories and add to registry |
| `/mirror-repos` | Mirror submodule repositories to web3stealth GitHub |

### CI/CD (ois-cfa)
| Command | Description |
|---------|-------------|
| `/cicd-status` | Check pipelines, runners, variables status |
| `/cicd-run` | Trigger GitLab pipeline (optional: force, sdk flags) |
| `/cicd-vars` | Manage CI/CD variables (list, check, unprotect) |
| `/cicd-logs` | Get job logs and traces for debugging |

## Related Files
- `.claude/agents/` - Agent definitions
- `.claude/skills/` - Skills and knowledge bases
- `.claude/cicd-cheatsheet.md` - Quick reference for CI/CD commands


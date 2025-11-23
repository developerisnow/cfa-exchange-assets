---
created: 2025-11-23 17:10
updated: 2025-11-23 17:10
type: runbook
sphere: [devops, llm]
topic: [composers, code2prompt, repomix, yek]
author: alex-a (documented by co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [context, oracle, code2prompt, repomix, yek, aliases]
---

# Composer Aliases (code2prompt / repomix / yek)

## ✅ How to use
- [ ] `source scripts/composer-aliases.sh`
- [ ] Поставь переменные при необходимости: `CFA_REPO`, `CONTEXT_DIR`, `C2P_TEMPLATES_DIR` (по умолчанию repo `../repositories/customer-gitlab/ois-cfa`, контекст `memory-bank/snapshots-aggregated-context-duplicates`).
- [ ] Запусти нужную функцию (см. ниже), файлы сложатся в `CONTEXT_DIR` с timestamp `YYYYMMDD-HHMM-*`.
- [ ] Для CI/Oracle: используй `repomix_*` (XML + compress) как основной input; `c2p_*` для кастомных шаблонов; `yek_budget` если нужен быстрый срез с жёстким токен-лимитом.

## 🛠 Алиасы/функции
- `c2p_core_arch` — docs/audit/artifacts/compose/openapi (tokens cl100k), output `*-code2prompt-ois-cfa-core-arch.txt`.
- `c2p_contracts` — contracts + domain + openapi.
- `c2p_services_core` — Program.cs, csproj, appsettings*, gateway configs.
- `c2p_tests` — tests/** без `tests/e2e-playwright/test-results/**`.
- `c2p_commit_msg` — шаблон `write-git-commit.hbs` по staged changes.
- `c2p_pr_desc [from] [to]` — PR-описание, diff/log между ветками (default: main → current HEAD), шаблон `write-github-pull-request.hbs`.
- `repomix_full` — весь репо в XML + compress (Claude-friendly).
- `repomix_contracts` — только contracts в XML + compress.
- `repomix_token_tree` — токены >1000 per file (анализ «тяжёлых» файлов).
- `yek_budget [budget]` — быстрый plain-text dump с лимитом токенов (default 120k), с учётом приоритезации yek.
- `list_composer_aliases` — вывести список доступных функций.

## 📦 Best practices (из deep-research 2025-11-22)
- **repomix**: дефолт → `--compress --style xml`, хранить конфиг в git (`repomix.config.*`), хорош для Oracle/Claude, есть secretlint.
- **yek**: использовать для больших дампов под токен-лимит (`--tokens 100k/120k`), порядок файлов от менее → более важных, быстрый.
- **code2prompt**: использовать Handlebars шаблоны (`write-git-commit.hbs`, `write-github-pull-request.hbs`); для базовых контекстов — паттерны как в alias c2p_*; включать `--tokens --encoding=cl100k_base` для оценки объёма.
- **Формат для Oracle**: XML (repomix) предпочтительно; plain (yek) вторично; markdown (code2prompt) для кастомных шаблонов.

## 🔗 Полезные paths
- Конфиг guardians: `repositories/customer-gitlab/ois-cfa/packages/architecture-guarduials.yaml` (trunk/branches/leaves globs).
- Последний git-дифф отчёт: `memory-bank/Scrum/20251121/gitlab-discovery/git-20251123-1246/` (категории + uncategorized).
- Пример свежего ранa: `memory-bank/Scrum/20251121/gitlab-discovery/git-20251121-1614/` (17–21 Nov).

## 🧭 Шаблонный workflow (Oracle)
- [ ] `repomix_full` → XML контекст для основной ревью.
- [ ] `c2p_services_core` или `c2p_contracts` → прицельный контекст (если нужен фокус).
- [ ] `yek_budget 120k` → быстрый общий дамп, если нужен plain.
- [ ] Перед отправкой в Oracle добавь метаданные (дата генерации, токен-бюджет, ветка).

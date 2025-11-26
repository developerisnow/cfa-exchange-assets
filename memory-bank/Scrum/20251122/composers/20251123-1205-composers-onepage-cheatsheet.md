---
created: 2025-11-23 12:05
updated: 2025-11-23 12:05
type: runbook
sphere: [devops, llm]
topic: [context-composers, code2prompt, repomix, yek, git-reporter]
author: alex-a (compiled by co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [cheatsheet, context, repomix, code2prompt, yek, git]
---

# One-Page Context Composers Cheatsheet

## Code2prompt (curated)
| Use | Command (from repo root) | Inputs (includes/excludes) | Output | Notes |
|---|---|---|---|---|
| Curated core (services/apps/contracts/deploy/ops) | `source scripts/composer-aliases.sh && c2p_core_arch_hbs` | Includes: services {issuance,registry,compliance,identity}, apps {backoffice,portal-issuer,portal-investor} src, api-gateway Program/appsettings, packages/contracts, docs/deploy, ops/scripts, scripts/git/*.sh. Excludes: bin/obj/node_modules/dotnet-clients/sdks/types/artifacts/memory-bank | `memory-bank/snapshots-aggregated-context-duplicates/composers/code2prompt/20251123-1046-code2prompt-curated.txt` | Plain text + pruned tree at top; template `scripts/code2prompt-curated.hbs` |
| Config-driven core (same с YAML) | `source scripts/composer-aliases.sh && c2p_core_config` | Uses `scripts/composer-config.yaml` (include_sets.core + defaults.exclude) | `composers/code2prompt/<ts>-c2p-core-config.txt` | Быстрый запуск без ручных include |

## Repomix (curated)
| Use | Command | Inputs | Output | Notes |
|---|---|---|---|---|
| Curated core XML <1 MB | `source scripts/composer-aliases.sh && repomix_curated` | Те же include/exclude, stdin find → repomix `--style xml` | `memory-bank/snapshots-aggregated-context-duplicates/composers/repomix/20251125-1150-repomix-curated.xml` | Claude/Oracle-friendly XML; pruned tree: `.../20251125-1150-repomix-curated.tree.txt` |
| Config-driven core | `source scripts/composer-aliases.sh && repomix_core_config` | include_sets.core + defaults.exclude (`scripts/composer-config.yaml`) | `composers/repomix/<ts>-repomix-core-config.xml` | Удобно менять через YAML |

## Yek (plain fallback)
| Use | Command | Inputs | Output | Notes |
|---|---|---|---|---|
| Curated plain concat (fallback) | `source scripts/composer-aliases.sh && yek_curated_fallback` | Жёсткий список ключевых файлов (Program/Services/DTOs + FE pages + contracts + deploy scripts) | `memory-bank/snapshots-aggregated-context-duplicates/composers/yek/20251123-1025-yek-curated.txt` | Лёгкий plain (~220 KB); Yek-cli не читает .git submodule, поэтому concat |
| Config-driven concat | `source scripts/composer-aliases.sh && yek_core_config` | include_sets.core + defaults.exclude (`scripts/composer-config.yaml`) | `composers/yek/<ts>-yek-core-config.txt` | Быстрый plain без зависимостей от yek бинаря |

## Git changes reporter (Python)
| Use | Command (from repo root) | Output | Notes |
|---|---|---|---|
| Diff by date (develop ois-cfa) | `python3 scripts/git-changes-reporter.py --since 2025-11-23 --until 2025-11-23 --preset default --include-uncategorized --repo repositories/customer-gitlab/ois-cfa` | `memory-bank/Scrum/20251121/gitlab-discovery/git-20251123-2008/` | Конфиги: `scripts/git-report-config.yaml`, `scripts/git-report-presets.yaml`; архитектурные globs: `repositories/customer-gitlab/ois-cfa/packages/architecture-guarduials.yaml` |

## Быстрый навигатор по файлам
- Алиасы/скрипты: `scripts/composer-aliases.sh`, `scripts/composer-config.yaml`, `scripts/code2prompt-curated.hbs`
- Свежие контексты:  
  - repomix: `.../repomix/20251125-1150-repomix-curated.xml` + tree  
  - code2prompt: `.../code2prompt/20251123-1046-code2prompt-curated.txt`  
  - yek: `.../yek/20251123-1025-yek-curated.txt`
- Best practices deep-dive: `memory-bank/Scrum/20251122/composers/20251122-0641-son4.5.deepresearch.analyse-best-practices-composers-code2promp-repomix-yek.md`

## Мини-QuickStart
1) `source scripts/composer-aliases.sh`  
2) Хотите XML для Claude → `repomix_curated` (или `repomix_core_config`)  
3) Хотите plain с деревом → `c2p_core_arch_hbs` (или `c2p_core_config`)  
4) Нужен лёгкий plain → `yek_curated_fallback`  
5) Diff за дату → `python3 scripts/git-changes-reporter.py --since YYYY-MM-DD --until YYYY-MM-DD --preset default --include-uncategorized --repo repositories/customer-gitlab/ois-cfa`

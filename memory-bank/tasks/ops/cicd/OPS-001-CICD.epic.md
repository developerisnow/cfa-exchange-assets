---
created: 2025-11-27 10:45
updated: 2025-11-27 18:35
type: epic
sphere: [devops]
topic: [cfa2, cicd, vps]
author: alex
agentID: fdfe6b1e-e4ee-4505-a723-e892922472f9
partAgentID: [co-76ca]
version: 0.2.0
tags: [cfa2, devops, cicd, docker-compose, gitlab]
epic_id: OPS-001-CICD
status: in_progress
---

# OPS-001-CICD: DevOps CI/CD for cfa2 (VPS)

## 🎯 Epic JTBD

Собрать рабочий, документированный CI/CD-поток для ветки `dev-cfa2`, который:
- билдит backend и frontend образы в GitLab Registry с path-based rules,
- деплоит их на `cfa2` через статичный docker-compose из репозитория,
- имеет явные guardrails (JSON-guardians, DoD, проверки) и истории-единицы работы.

## 🗂 Stories Index (Story-JTBD)

| Story ID | File | JTBD (кратко) | Status |
| --- | --- | --- | --- |
| OPS-001-001 | `tasks/ops/cicd/OPS-001-001-cicd-phase0-prepare-vps-and-gitlab.story.md` | Подготовить vds1/cfa2 и GitLab (runner, registry, glab) под dev-cfa2 | done |
| OPS-001-002 | `tasks/ops/cicd/OPS-001-002-cicd-phase1.story.md` | Стабилизировать backend dev pipeline для cfa2 (compose + build/deploy) | done |
| OPS-001-003 | `tasks/ops/cicd/OPS-001-003-cicd-phase2.story.md` | Добавить фронты в pipeline/compose и внедрить path-based builds + SDK jobs | in_progress |
| OPS-001-004 | `tasks/ops/cicd/OPS-001-004-cicd-phase4.story.md` | Ввести JSON-guardians и pre-commit guardrails для CI/CD артефактов | in_progress |
| OPS-001-005 | `tasks/ops/cicd/OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md` | Cloudflare ingress для cfa2 (telex.global, домены+TLS) | in_progress |

## 🔍 Acceptance (Epic-level DoD)

- [ ] Все четыре истории имеют заполненный Story-JTBD шаблон (JTBD, DoD, Verification Matrix, Kickoff, Loop trace).
- [ ] Для J1–J3 есть хотя бы по одному завершённому WORKFLOW LOOP (в Loop trace stories).
- [ ] dev-cfa2 pipeline зелёный хотя бы один раз (build backend+frontend + deploy-cfa2).
- [ ] Есть единый quick-runbook для cfa2 (`docs/deploy/vps-cfa2/*`) и он согласован со stories.
- [ ] Guardrails/guardians для CI/CD артефактов описаны и включены в pipeline (`guardians:check` + JSON-config).

## 🛡 Guardrails / Guardians

- История `OPS-001-004` задаёт минимальный набор правил guardian’ов:
  - запрет новых `.gitlab-ci*.yml` вне корня и каталога `.gitlab/`;
  - запрет `docker-compose.yml` и `.env` под `docs/**`, `apps/**`, `tests/**`;
  - защита production-инфраструктуры `ops/infra/uk1/**` и `ops/infra/cfa1/**` через override-переменную.
- Конфигурация: `ops/guardians/guardian.config.json`.
- Скрипт-проверка: `scripts/guardians/check-guardians.sh` (используется локально и в CI).
- CI job: `guardians:check` (stage `sdk`, ветка `dev-cfa2`), который должен проходить без нарушений или быть явно обойдён через `GUARDIANS_BYPASS=1` / `GUARDIANS_ALLOW_PROD_INFRA=1` (для старших инженеров).

## 🔁 Loop trace (Epic)

> Заполняется по мере работы: ссылки на коммиты, pipeline IDs, ключевые выводы. Пока оставляем пустым.

---
created: 2025-11-14 10:55
updated: 2025-11-14 10:55
type: analysis
sphere: profession
topic: devops
author: Alex (co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [devops, investigation-infrastructure, merge-strategy]
prompt: "Оценить сценарии слияния веток infra и deploy (infra.defis.deploy vs deploy+infra), дать рекомендации и поэтапный план."
---

# Merge Strategy — infra vs deploy

## 📋 Request Checklist
What you asked for:
- [x] Сравнить два сценария: «fork от infra и вмерджить deploy» vs «fork от deploy и вмерджить infra»
- [x] Привести метрики расхождения (коммиты, LOC)
- [x] Нарисовать план действий (mermaid + таблица), отметить риски
- [x] Рекомендовать рабочий DoD перед merge (тесты, проверки)

## 🎯 Your Original Request
> «После аудита infra оцени, как лучше объединять её с моей веткой deploy (dpo). Возможно создать новую `infra.defis.deploy`. Подготовь риски и пошаговый план.»

## 🧠 Sequential Thinking
Ручной анализ: `git rev-list --left-right --count origin/deploy...origin/infra` → `39 27`; `git diff --shortstat origin/deploy..origin/infra` → `611 files changed, +75 609 / −1 858`. Выводы ниже.

## 🎯 Output

### 1. Comparison Snapshot (на 2025‑11‑14)
| Метрика | Deploy | Infra | Комментарий |
| --- | --- | --- | --- |
| Уникальных коммитов ↔︎ | 39 (лев.) | 27 (прав.) | `git rev-list --left-right --count origin/deploy...origin/infra` |
| LOC diff | — | `+75 609 / −1 858` | `git diff --shortstat origin/deploy..origin/infra` |
| Ключевые области | .NET сервисы (рабочие правки dpo) | CI/CD, GitOps, AsyncAPI, Audit | Высокий риск конфликтов в `services/*` и `packages/*` |
| Состояние рабочей ветки | грязная (см. `apps/api-gateway` … `.dockerignore`) | чистая (worktree infra) | Перед merge нужно застейджить/закоммитить deploy-правки |

### 2. Options Matrix
| Опция | Пошагово | Pros | Cons |
| --- | --- | --- | --- |
| **A. infra.defis.deploy** (база = `origin/infra`) | 1) `git fetch && git worktree add ../infra.defis.deploy origin/infra` 2) `git merge origin/deploy` 3) Разрешить конфликты, приоритезируя infra CI/ops 4) Прогнать тесты/compose 5) Откатить ненужные deploy-хаков | + Сохраняем новейшие ops/CI без бэктрекинга + Дальше легче upstream → main | − Много конфликтов в .NET сервисах (deploy впереди) − Потребуется адаптировать дпо-патчи к новым contracts/AsyncAPI |
| **B. deploy+infra** (база = `origin/deploy`) | 1) `git worktree add ../deploy.plus.infra origin/deploy` 2) `git merge origin/infra` 3) Вручную перенести CI/ops (risk overwrite) 4) Снова запускать terraform/gitops | + Быстрее получить работоспособный backend (dpo) + Меньше конфликтов в сервисах | − Высокий шанс потерять audit/CI улучшения − Придётся cherry-pick ops/infra файлы (>300) вручную |
| **C. Double-track (интеграционный слой)** | 1) Создать `infra.defis.deploy` (как в A) 2) Параллельно оставить `deploy` как «source of truth» до завершения тестов 3) Исп. feature flags | + Понижаем риск простоя, есть fallback | − Максимальные трудозатраты; нужен CI matrix |

**Рекомендация**: ⚙️ **Опция A** (база = `origin/infra`). Причины: (1) infra уже содержит стратегические активы (GitLab agent, Terraform, audit runbooks) → потеря приведёт к откату DevOps maturity; (2) deploy-специфика ограничена сервисами и может быть портирована поверх `infra`; (3) Следующие работы (KYC бизнес-кейс) требуют готовой событийной шины/AsyncAPI, которая уже в `infra`.

### 3. Proposed Plan — Option A
```mermaid
flowchart TD
    A[Prep] --> B[Create branch infra.defis.deploy]
    B --> C[Merge origin/deploy --no-commit]
    C --> D{Conflicts buckets}
    D -->|services| E[Resolve .NET services (api-gateway, compliance,...)]
    D -->|packages| F[Align contracts/domain DTO]
    D -->|ops/docs| G[Keep infra versions]
    E --> H[dotnet test + npm test]
    F --> H
    G --> H
    H --> I[docker compose up --build]
    I --> J[git commit + push]
    J --> K[MR → infra or new release branch]
```

### 4. Conflict Buckets & Owners
| Bucket | Файлы | Подход |
| --- | --- | --- |
| .NET Services | `services/*/Program.cs`, `apps/api-gateway/appsettings.json` | Переносим deploy-логику (e.g., backport dto) поверх новых OTEL/MT настроек из infra; фиксируем миграции EF. |
| Domain Packages | `packages/domain/*.csproj`, `packages/domain/**/DTO.cs` | Применяем `git checkout --ours packages/domain` чтобы сохранить AsyncAPI-compatible версии, затем поверх вносим dpo-правки. |
| Contracts/tests | `tests/e2e/*`, `tests/k6/*` | Сводим спецификации, избегаем отката новых journey spec. |
| CI/Ops | `.gitlab-ci.yml`, `ops/**`, `audit/**` | При конфликте всегда оставляем версию из infra (ours). |

### 5. DoD before Merge
1. **Git Hygiene**: закоммитить текущие локальные изменения для `deploy` (список из `apps/api-gateway`, `services/*`, `.dockerignore`).
2. **Automated tests**: `dotnet test`, `npm test` (порталы), `tests/e2e` smoke (issuer/investor/backoffice), `tests/k6` optional.
3. **Infra validation**: `terraform validate` (ops/infra/timeweb), `helm lint ops/helm/*`, `kubectl kustomize` (если есть overlays).
4. **CI dry run**: локально выполнить `gitlab-runner exec docker build:api-gateway` для критичных образов либо `docker build` через compose.
5. **Docs sync**: обновить `audit/` версию (e.g., v0.2 → v0.3) после внедрения quick wins.

### 6. Risk Mitigation
| Риск | Митигатор |
| --- | --- |
| 75k LOC diff приводит к «merge hell» | Работать в отдельном worktree, коммитить по модулям (services, packages, ops), использовать `git add -p`. |
| Потеря работоспособности deploy backend | До push держать `deploy` ветку нетронутой, иметь docker-compose snapshot, записать smoke steps. |
| CI взорвётся из-за новых job | Временно задизейблить деплой-джобы (set `when: manual`) до завершения тестов. |
| Terraform/Argo secrets отсутствуют | Добавить `.example` values + описать, какие переменные требуются, прежде чем запускать apply. |

### 7. Next Actions
1. На стороне `deploy` — зафиксировать текущие незакоммиченные изменения (минимум 12 файлов) → «baseline».
2. Создать ветку `infra.defis.deploy` от `origin/infra` и выполнить `git merge origin/deploy --no-ff` с описанной стратегией.
3. Резолвить конфликты по bucket-подходу; каждый блок фиксировать отдельным коммитом (e.g., `merge: services`, `merge: contracts`).
4. После успешных тестов → Pull/Merge Request > `infra` (или новая `release/infra-dpo`).
5. Только после ревью — удалять/архивировать старую `deploy`.

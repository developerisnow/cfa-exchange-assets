## 2025-11-14 – Git merge infra → deploy (infra.defis.deploy)

### Context
- Базовая ветка: `origin/deploy` (последний коммит f99f549).
- Инфраструктурная ветка: `origin/infra` (коммит ac0e0fb…).
- Цель: собрать рабочие runtime-фиксы (deploy) с полной DevOps-инфрой (infra) в новой ветке `infra.defis.deploy`.

### Выполненные шаги
1. **Закоммитили локальные правки `deploy`**, пропушили на GitLab/GitHub.
2. **Создали ветку `infra.defis.deploy`** от чистого `deploy`.
3. **Смерджили `origin/infra`** → получили ~500 файлов изменений.
4. **Разрешили конфликты** (10 файлов) по buckets:
   - `.gitignore` (объединение правил).
   - `apps/backoffice/package.json` (замена зависимостей на infra-версию).
   - `services/*/*.csproj` (MassTransit + health checks + DefaultItemExcludes).
   - `services/*/Program.cs` (Auth/Z, rate limiter, MassTransit, OTEL + наш `MIGRATE_ON_STARTUP`).
5. **Коммит `ed44ee6`** и push ветки в GitLab и GitHub.

### Итог
- `infra.defis.deploy` содержит одновременно рабочие runbooks + свежую infra-архитектуру Александра.
- Конфликты закрыты, тесты пока не гонялись (по плану).
- Ветки для MR:
  - `deploy -> main` (статус FYI).
  - `infra -> deploy` (через `infra.defis.deploy`).

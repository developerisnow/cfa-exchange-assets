## 2025-11-14 – Q&A по merge стратегии

### Вопросы
1. Что делать с сервисными файлами (`services/issuance/Program.cs` и др.) – брать версию deploy или infra?
2. Есть ли смысл сохранять 59 deploy-правок, если infra ушла далеко?
3. Какая стратегия merge выбрана: infra→deploy или наоборот?

### Ответы
- **Program.cs / csproj:** в `infra.defis.deploy` оставлены *infra*-реализации (Auth, RateLimiter, Kafka, OTEL, Hosted Outbox) + наши runtime-фичи (динамический `MigrationsAssembly`, `MIGRATE_ON_STARTUP`). То есть ничего «от фонаря» нет, взяли код Александра и адаптировали под рабочее окружение.
- **Deploy-правки нужны.** Это Dockerfile/compose, Keycloak bootstrap, gateway и порталы – без них стенд не заводится. Поэтому они уже живут поверх infra, конфликт минимальный.
- **Стратегия A:** база = `origin/infra`, поверх вмерджен `deploy` → получена ветка `infra.defis.deploy`. Это позволяет не потерять infra-артефакты (CI/GitOps/AsyncAPI), и при этом сохранить рабочую конфигурацию из deploy.

### Статус
- `infra.defis.deploy` готова к дальнейшему ревью / smoke.
- MR не создавали (ждём созвона), но ветка доступна в GitLab/GitHub.

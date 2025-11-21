---
created: 2025-11-21 17:45
updated: 2025-11-21 17:45
type: analysis
sphere: [devops]
topic: [git, dotnet, services]
author: alex-a (summarized by co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [git-log, diff, dotnet]
---

# Changed .NET files — services (commits since 2025-11-17)

Диапазон: `git diff --name-status --diff-filter=AMCR 2789f579e5c4d6c879ce21978f39296a9b18d074..HEAD` (ветка `infra.defis.deploy`). Фильтр: `.cs`, `.csproj`, `.sln`, `.props`, `.targets`.

## Файлы и статус
- A services/compliance/DTOs/KycRequestDto.cs
- M services/compliance/Program.cs
- M services/identity/Program.cs
- M services/issuance/Background/OutboxPublisher.cs
- A services/issuance/DTOs/IssuerIssuancesReportResponse.cs
- M services/issuance/Program.cs
- M services/issuance/Services/IssuanceService.cs
- M services/issuance/issuance.Tests.csproj
- M services/issuance/issuance.csproj
- M services/registry/Background/OutboxPublisher.cs
- M services/registry/Services/RegistryService.cs
- M services/registry/registry.Tests/OrderFlowTests.cs
- M services/settlement/Program.cs

## Notes
- Добавлены новые DTO для compliance и issuance; обновлены программы и сервисы issuance/registry/settlement.
- Проекты issuance (app и tests) изменены — вероятно новые ссылки/конфиг.

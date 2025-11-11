---
created: 2025-11-11 13:52
updated: 2025-11-11 13:52
type: analysis
sphere: [finance, blockchain]
topic: [ois-cfa, repo-assessment, estimation]
author: alex-a
agentID: co-3a68
partAgentID: [co-3a68]
version: 1.0.0
tags: [assessment, mvp, architecture, estimation]
---

# Оценка проекта ois-cfa (A. Ozherelev) и идеи оценки

## TL;DR
- Репозиторий ois-cfa структурно зрелый: Spec‑first (OpenAPI/AsyncAPI), EF Core per‑service, Outbox, фронты (Next.js), Docker Compose, Helm для Fabric — хороший фундамент для MVP первички.
- Идея оценки «6000 часов от аутсорса» завышена для MVP первички; разумный диапазон MVP: 10–14 недель core team (3–5 инженеров) при фокусе на первичном размещении и базовом комплаенсе.
- Риски: ESIA/Keycloak интеграция и банк‑номинал (договоры, сроки), Fabric‑контур (staging), регуляторные артефакты. Митигация: мок‑контуры, контракты, чек‑листы из docs.

## Steps
1) Прочитал c2p_ois-cfa.txt (структура/артефакты) и исходники в `repositories/customer-gitlab/ois-cfa`.
2) Изучил оценки/артефакты: 20251004‑estimation‑from‑outsource‑company, GPT конверсии диаграмм, W44 artefacts (C4/диаграммы/competitors/analysis).
3) Сопоставил с текущими OpenAPI/EF/Compose/Helm в репозитории.
4) Сформировал выводы, риски, DoD для MVP и корректировку оценки.

## Snapshot оценивания (сжато)

| Area | Status | Evidence | Risk | Effort (MVP) |
| --- | --- | --- | --- | --- |
| API спецификации | High (готово) | packages/contracts/openapi-*.yaml | Поддержка актуальности | Низкий |
| Бэкенд‑сервисы | Medium‑High | services/* (EF DbContexts, Services, Outbox) | ES для событий (консумеры) | Средний |
| Идентификация/OIDC | Medium | openapi-identity.yaml, Keycloak в compose | ESIA прокси/флоу | Средний |
| Settlement/DvP | Medium | openapi‑settlement.yaml, bank‑nominal integration | Договор/песочница банка | Средне‑высокий |
| Ledger/Fabric | Medium | ops/helm/*, chaincode/* | Сетап HLF, CI/CD, тестовая сеть | Средний |
| Frontends (Next.js) | Medium | apps/* portals | AuthZ, интеграция API | Средний |
| НФ‑требования | Medium | docs/architecture/*, security/* | ГОСТ57580 практики/чек‑листы | Средний |

Примечания
- Outbox реализован (services/issuance/OutboxService.cs), но потребители событий и конечные подписчики в JSON/коде не детализированы — это нормально для MVP, но учесть в планировании.
- Открытые спецификации по доменам (issuance/registry/settlement/compliance/identity) — сильная база для «contract‑first» разработки и автогенерации SDK (packages/sdks/ts).
- Docker Compose даёт быстрый локальный контур (Postgres/Kafka/Keycloak/Minio), Helm‑чарты для Fabric показывают путь к staging.

## Идея оценки: качество и калибровка
- Внешняя оценка «~6000 ч.» (20251004‑estimation‑from‑outsource‑company.md) — вероятно включает полный спектр (вторичка, ISO 20022, прод‑безопасность, отчётность, мобильный, DR), и резерв по неопределённости.
- По фактам из репо + W44 артефактов (C4, конкуренты, анализ): MVP первички без вторички реалистичен быстрее.
  - Бенчмарк из 2025‑11‑03 comprehensive‑analysis указывает ~3.5 мес (560 ч) — при условии зрелой команды и фокуса. Это нижняя граница.
- Рекомендация: калибровать оценку на 10–14 недель (2.5–3.5 мес активной разработки + 2–4 недели буфер под интеграции ESIA/банк):
  - Команда: 1 TL .NET/DevOps, 2 BE .NET, 1 FE (Next.js), 0.5 Tech Writer/BA, 0.5 QA.
  - Скоуп: первичка (issuance→orders→redeem→payout), OIDC/Keycloak, базовый комплаенс, отчёты минимальные.

## Вывод: зрелость репозитория A.Ozherelev
- Сильные стороны: spec‑first, разделение доменов, EF Core per‑service, Eventing (Outbox), фронты, чёткие OpenAPI.
- Зоны внимания: ESIA (user journey/redirects), интеграция банка (номинал/счета), консумеры событий/оркестрации, NFR (логирование/метрики/алерты), регуляторные артефакты (docs/security/legal).
- Соответствие W44 C4/диаграммам и «референс‑архитектуре» высокое: отличия в стеке (Node vs .NET) уже учтены — текущий репозиторий реализует .NET.

## Next actions (минимум)
- Зафиксировать DoD MVP (primary only) и freeze требования.
- Пройтись по OpenAPI → сгенерировать SDK и smoke‑интеграции фронтов.
- Поднять локальный контур (compose) и отработать базовые флоу: issuance→order→wallet→redeem→settlement.
- ESIA: описать happy‑path и мок‑провайдер; Keycloak realm/export под проект.
- Банк‑номинал: sandbox договор/интерфейсы, стаб для автотестов.
- Fabric: минимальная тестовая сеть (1 орг, 2 peer) + chaincode deploy из helm.


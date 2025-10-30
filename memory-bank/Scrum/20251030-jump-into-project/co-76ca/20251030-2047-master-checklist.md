TL;DR
- Полный чек‑лист покрывает требования Юрия и мои мысли; вложенность отражена под‑чекбоксами.
- Разбивка: Домены, НФ‑требования, Юр/регуляторика, Интеграции, UX, Рынок, Данные/отчётность, Deep‑Research.
- Везде указаны статусы: [ ] ToDo, [~] In‑Progress, [x] Done, [TBD] требуется уточнение.

Why → What → How → Result
- Why: исключить пробелы — от требований Юрия до внутренних заметок.
- What: единый master‑чеклист с трассировкой на источники.
- How: чекбоксы + таблицы привязок, регулярные ревью.
- Result: согласованный план → MVP без сюрпризов.

Sources
- [Yury Intro Call] memory-bank/context/current-context/communication-log/20251022-1930-yury-founder-intro-call.md
- [My Thoughts] memory-bank/Scrum/20251030-jump-into-project/20251030-1800-thoughts-jump-start-project-cifra-rwa-capital.md
- [Estimation/Architecture] memory-bank/context/current-context/additional-info-for-analysing/20251004-estimation-from-outsource-company/20251004-estimation-from-outsource-company.md
- [UI Tables] memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/01-platform_functionality__tables_20251026-115409/
- [Market Status] memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/06-20251030-1926-report-finance-cfa-platforms-status.md

Product Scope — MVP (Primary Only)
- [x] Определить MVP как первичный рынок ЦФА (эмиссия, размещение, учёт)
  - [x] Без ордербуков на v1; RFQ/OTC — v1.1
  - [x] DvP T+0 с одним банком‑партнёром
- [x] Домены MVP
  - [x] Registry (реестр участников/ролей, ABAC)
  - [x] Identity & KYC/KYB (KEP/УКЭП 63‑ФЗ, санкционные/PEP)
  - [x] Tokenization (выпуски, условия, disclosures)
  - [x] Settlement (DvP, escrow, reconciliation)
  - [x] Custody (HSM/MPC, M‑of‑N)
  - [x] Disclosure/Reporting (отчётность регулятору)

Ledger Decisions
- [ ] Выбрать ledger‑путь для MVP
  - [ ] immudb audit‑core (быстрый MVP) — adapter + hash anchoring
  - [ ] Hyperledger Fabric (permissioned, channels)
  - [ ] Hyperledger Besu (permissioned EVM)
  - [ ] DPoS приватная сеть (отложить)
  - [~] Интерфейс‑адаптер к ledger (event‑sourcing + CQRS)

Architecture & NFR
- [x] API Gateway: OAuth2/OIDC, mTLS, WAF/Anti‑DDoS
- [x] Event bus: Kafka/Redpanda; схемы событий
- [x] Per‑service DB: Postgres; S3 для документов
- [ ] Observability: tracing/metrics/logs; SIEM интеграция
- [ ] DR/BCP: бэкапы, георезерв, тест свитчей ≥1/кв
- [ ] Perf targets: 2–5k rps API; 200–500 tps DvP (шардирование)
- [ ] Security: PAM/Vault, key‑rotation, BYOK, WAF/IDS

Compliance & Legal
- [x] 259‑ФЗ: обязанности ОИС (оператор), выпуск/оборот/учёт
- [x] 63‑ФЗ: КЭП/УКЭП привязка к аккаунтам
- [x] AML/CFT: сценарии, скоринг, мониторинг, алерты
- [x] PDN: локализация, шифрование в покое/транзите
- [ ] Travel Rule для VASP интеграций (если требуется)
- [ ] Политики ключей: lifecycle, M‑of‑N, ротация, HSM/MPC вендор
- [ ] Audit retention ≥7 лет; независимое якорение хэшей

Integrations
- [ ] Банк‑партнёр DvP (список, API, SLA)
- [ ] Платёжные рельсы: НСПК/СБП, корпоративные счета
- [ ] KYC/KYB провайдеры; санкционные списки
- [ ] TSA/time‑stamp; доверенные сервисы

UX/Portals (из UI Tables)
- [ ] Витрина предложений
- [ ] Выпуски ЦФА (листы/детали)
- [ ] Мои заявки/мои активы/история операций
- [ ] Регистрация и выпуск (мастер/формы)
- [ ] Размещение/покупка (T+0)
- [ ] Карточка инвестора
- [ ] Профиль/Квалификация/Блокировки

Secondary (Post‑MVP)
- [ ] RFQ/OTC (v1.1) — допуски, котировки, матчинговые правила
- [ ] Ордербуки/аукционы (v1.2)
- [ ] Корпоративные действия расширенные (купоны, амортизация)

Data & Reporting
- [ ] Регуляторные выгрузки: XBRL/ISO 20022 (минимум)
- [ ] Disclosure публикации (машинно‑читаемые оферты)
- [ ] DWH/Lakehouse для аналитики (минимум)

Team & Process
- [x] Роли: Lead/Arch, 2 BE, 1 FE, 1 DevOps/Sec, 0.5 BA, 0.5 QA
- [x] Каденс: еженедельные демо; Discovery Sprint 40h
- [ ] Acceptance tests — соглашение с заказчиком

Risks & Mitigations
- [ ] Задержка по банку → mock settlement + параллельный трек
- [ ] Поставщик КЭП/УКЭП → ранняя закупка, тестовый УЦ временно
- [ ] Ledger смена → адаптер, договорённость о freeze интерфейсов

Mapping Table (Traceability)
| Area | Requirement | Source | Status |
|---|---|---|---|
| Permissioned DLT | Корпоративный блокчей и контроль валидаторов | My Thoughts:20 | [ ] |
| Вторичка позже | Децентрализованная биржа — этапно | Yury Intro, My Thoughts | [x] |
| Spec‑first | Спецификационные контракты, SBE | Yury Intro:18 | [ ] |
| Reuse legacy | Оценить BitChange (PHP) код | Yury Intro:13 | [ ] |
| Sanctions reality | BRICS‑friendly стек/вендоры | My Thoughts | [ ] |
| KYC/KYB | Санкции/PEP, биометрия опц. | Estimation | [ ] |
| DvP | Атомарность обмена | Estimation | [ ] |
| Custody | HSM/MPC, M‑of‑N | Estimation | [ ] |
| Reporting | XBRL/ISO 20022 | Estimation | [ ] |
| Platforms map | Рынок ЦФА РФ | Market Status | [x] |

Related Files
- requirements-trace: memory-bank/Scrum/20251030-jump-into-project/co-76ca/20251030-2052-requirements-trace.md

Notes
- Некоторые пункты помечены [TBD] — требуется доснять из полных транскриптов; при следующем проходе заменю на конкретику.

Meta
- agentID=019a362f-76ca-7272-909e-362716cf233d partAgentID=76ca

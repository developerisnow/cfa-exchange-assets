---
created: 2025-11-03 14:20
updated: 2025-11-03 14:20
type: customer-artifact
sphere: [market, cfa]
topic: [competitors-all-in-one]
owner: [alex]
co-author: openai-codex
partAgentID: [co-76ca]
version: 1.0.0
tags: [competitors, summary, ssot]
---

# Glossary — Columns (short, practical)

| abbr      | 🤔✅ | title         | description                                                   | example             | notes                                            | cfa-capital insights                  |
| --------- | --- | ------------- | ------------------------------------------------------------- | ------------------- | ------------------------------------------------ | ------------------------------------- |
| name      | +   | Platform      | Название платформы/банка/инфраструктуры                       | «Атомайз (Atomyze)» | Как в реестре/публичных источниках               | Фиксируем единообразно для поиска     |
| status    | +   | Status        | Работает/не работает/скоро/лицензия                           | working             | Приводим к 4 статусам                            | Быстрый фильтр зрелости               |
| roles     | +   | Roles         | ОИС/депозитарий/биржа/банк/инфра                              | ois, bank           | Множественные через запятую                      | Понимание рег. роли                   |
| dlt       | +   | DLT           | Базовый реестр: fabric/besu/quorum/waves/ethereum/own/unknown | fabric              | Нормализуем                                      | Влияет на смарт‑контракты/приватность |
| dvp       | +   | DvP Model     | Модель расчётов: t+0/t+1/unknown                              | t+0                 | T+0 приоритетно для MVP                          | Ключ к атомарности сделок             |
| dvp_banks |     | DvP Banks     | Банк‑партнёр/контур расчётов                                  | Росбанк             | Если известно                                    | Критичный интеграционный контур       |
| iso20022  |     | ISO 20022     | Поддержка сообщений                                           | true/false          | Если явно заявлено                               | Совместимость с банками               |
| sbp       |     | SBP           | Поддержка СБП                                                 | true/false          | Если релевантно                                  | Альтернатива маршрутам платежей       |
| rfq       |     | RFQ           | Есть ли RFQ/OTC вторичка                                      | true/false          | Начальный шаг вторички                           | Для v1.1                              |
| orderbook |     | Orderbook     | Есть ли ордербуки/аукционы                                    | true/false          | Позже RFQ                                        | Для v1.2                              |
| openapi   |     | OpenAPI       | Публичность/наличие API                                       | true/false          | +docs ссылки при наличии                         | Важен для интеграций                  |
| licenses  |     | Licenses      | Лицензии/статусы в ЦБ РФ                                      | ОИС ЦФА             | Коротко, без ссылок                              | Подтверждаем в источниках             |
| ukep_gost |     | UKÉP (GOST)   | Поддержка/интеграции КЭП/ГОСТ                                 | true/false          | По умолчанию для РФ — true, если иное не указано | Юр. значимость операций               |
| custody   |     | Custody       | HSM/MPC/unknown                                               | unknown             | Вендоры при наличии                              | Риск и комплаенс                      |
| hosting   |     | Hosting       | RU cloud/on‑prem                                              | ru_cloud            | Если известно                                    | Локализация 152‑ФЗ                    |
| metrics   |     | Metrics       | TPS/finality (если публично)                                  | SmartBFT            | Редко публично                                   | Для PoC сравнения                     |
| sources   |     | Sources Count | Счётчик публичных источников в карточке                       | 2                   | ≥2 лучше                                         | Прозрачность и уверенность            |
| last      |     | Last Checked  | Дата последней проверки                                       | 2025‑10‑31          | ISO‑дата                                         | Регулярность обновлений               |
| conf      |     | Confidence    | high/mid/low                                                  | high                | Сводная оценка                                   | Для приоритезации рисков              |

# Competitors — All‑in‑One Table (20)

| Platform                   | Status          | Roles                     | DLT      | DvP     | DvP Banks     | ISO20022 | SBP     | RFQ   | Orderbook | OpenAPI | Licenses                 | UKÉP (GOST) | Custody | Hosting          | Metrics  | Sources | Last Checked | Confidence |
| -------------------------- | --------------- | ------------------------- | -------- | ------- | ------------- | -------- | ------- | ----- | --------- | ------- | ------------------------ | ----------- | ------- | ---------------- | -------- | ------- | ------------ | ---------- |
| Альфа‑Банк (А‑Токен)       | working         | ois, bank                 | waves    | t+0     | Альфа‑Банк    | true     | true    | false | false     | true    | ОИС ЦФА                  | true        | unknown | ru_cloud/on‑prem | unknown  | 2       | 2025‑10‑31   | high       |
| Атомайз (Atomyze)          | working         | ois                       | fabric   | t+0     | Росбанк       | true     | true    | false | false     | true    | ОИС ЦФА                  | true        | unknown | ru_cloud/on‑prem | SmartBFT | 2+      | 2025‑10‑31   | high       |
| Блокчейн Хаб (МТС)         | working         | ois                       | ethereum | unknown | unknown       | false    | false   | false | false     | true    | ОИС ЦФА                  | true        | unknown | ru_cloud         | unknown  | 1+      | 2025‑10‑31   | mid        |
| ВТБ Капитал Трейдинг       | working         | ois, bank                 | unknown  | t+0     | ВТБ           | true     | true    | false | false     | false   | ОИС ЦФА                  | true        | unknown | ru_cloud/on‑prem | unknown  | 1+      | 2024‑12‑04   | mid        |
| Еврофинанс Моснарбанк      | working         | ois, bank                 | waves    | unknown | Еврофинанс    | false    | false   | false | false     | false   | ОИС ЦФА                  | true        | unknown | ru_cloud         | unknown  | 1+      | 2024‑12‑31   | mid        |
| Токеон (ПСБ)               | working         | ois, bank                 | waves    | t+0     | ПСБ           | true     | true    | false | false     | true    | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 2+      | 2025‑10‑31   | high       |
| Лайтхаус                   | working         | ois                       | fabric   | unknown | unknown       | false    | false   | false | false     | false   | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 1+      | 2025‑02‑25   | low        |
| НРД                        | working         | ois, depository, exchange | waves    | t+0     | Мосбиржа      | true     | false   | true  | false     | false   | ОИС ЦФА, Оператор обмена | true        | unknown | unknown          | unknown  | 2+      | 2025‑07‑21   | high       |
| Сбербанк (Цифровые активы) | working         | ois, bank                 | fabric   | t+0     | Сбербанк      | true     | true    | true  | true      | true    | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 2+      | 2025‑03‑23   | high       |
| СПБ Биржа                  | working         | ois, exchange             | fabric   | unknown | —             | true     | false   | true  | false     | false   | ОИС ЦФА, Оператор обмена | true        | unknown | unknown          | unknown  | 1+      | 2025‑..      | high       |
| Мастерчейн (СРР)           | working         | ois, infra                | waves    | unknown | ВТБ Факторинг | unknown  | unknown | false | false     | false   | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 1       | 2025‑10‑31   | mid        |
| МРЦ                        | working         | ois, depository           | unknown  | unknown | —             | false    | false   | false | false     | false   | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 1       | 2024‑12‑11   | low        |
| Т‑Банк (Тинькофф)          | working         | ois, bank                 | unknown  | unknown | Т‑Банк        | false    | true    | false | false     | true    | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 2+      | 2024‑10‑21   | high       |
| Токеник                    | working         | ois                       | unknown  | unknown | Росбанк       | false    | false   | false | false     | false   | ОИС ЦФА                  | true        | unknown | unknown          | unknown  | 1+      | 2024‑11‑..   | low        |
| Банк Синара                | not_working     | bank                      | unknown  | unknown | —             | false    | false   | false | false     | false   | —                        | true        | unknown | unknown          | unknown  | 0       | 2025‑..      | low        |
| БКС Холдинг                | not_working     | broker                    | unknown  | unknown | —             | false    | false   | false | false     | false   | —                        | true        | unknown | unknown          | unknown  | 0       | 2025‑..      | low        |
| Газпромбанк                | not_working     | bank                      | unknown  | unknown | —             | false    | false   | false | false     | false   | —                        | true        | unknown | unknown          | unknown  | 0       | 2025‑..      | low        |
| МАДРИГАЛ ОИС               | soon            | ois                       | unknown  | unknown | —             | false    | false   | true  | false     | false   | —                        | true        | unknown | unknown          | unknown  | 0       | 2025‑..      | low        |
| Статус Инвест              | license_pending | ois                       | iroha    | unknown | —             | false    | false   | false | false     | false   | —                        | true        | unknown | unknown          | unknown  | 0       | 2025‑..      | low        |
| Спутник ЦФА                | license_pending | ois                       | unknown  | unknown | —             | false    | false   | false | false     | false   | —                        | true        | unknown | unknown          | unknown  | 0       | 2025‑..      | low        |

Notes
- unknown = нет подтверждённых публичных данных в текущем корпусе; для «confirmed» требуется ≥2 независимых источника.
- SSOT (machine): [[co-76ca/competitors_all.jsonl]]. Human‑view: эта таблица; Batch‑1 детали: [[20251103-customer-pack-Yury/batch1-competitors]].

# Links / Index (for internal navigation)

- Human‑view tables (current):
  - [[co-76ca/20251103-customer-pack-Yury/competitors-all-in-one]] (этот документ)
  - [[co-76ca/competitors_all.md]] — сводная по ключевым полям
  - [[co-76ca/competitors.md]] — Batch‑1 (4 платформы) подробно
- Machine SSOT:
  - [[co-76ca/competitors_all.jsonl]] — 20 карточек (нормализованные поля)
- Sources & deepresearch:
  - [[co-76ca/20251031-1100-batch1-competitors-sources.md]] — источники Batch‑1
  - [[deepresearches/01-CFA-platforms-RU-2024-2025]] — папка всех отчётов (Perplexity/OpenAI/Opus/Gemini/Parallel)
  - [[co-76ca/20251103-customer-pack-Yury/competitors-overview]] — краткий обзор для клиента
- Related client pack:
  - [[20251103-customer-pack-Yury/README-v2]], [[20251103-customer-pack-Yury/presentation]], [[20251103-customer-pack-Yury/kickoff-pack]], [[20251103-customer-pack-Yury/roadmap]]

Confidentiality
- Клиентский артефакт без финансовых условий/ставок. Финансовые детали — отдельно (отчёт/инвойс в приватном канале).


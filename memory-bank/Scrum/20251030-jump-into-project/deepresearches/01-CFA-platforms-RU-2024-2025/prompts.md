# Prompt 1


# Prompt 2
TL;DR
- Цель: верифицировать «кто на чём» у действующих РФ‑платформ ЦФА (DLT/ledger, custody/HSM/MPC, УКЭП/ГОСТ, DvP/банки, вторичка, интеграции) на основе 2024–2025 источников.
- Входные локальные данные: статус‑диаграмма и выгрузки «ОИС/операторы/фичи». Использовать как seed‑лист.
- Выход: JSON per‑platform + сводная таблица + mermaid‑группировка + список источников (RU‑приоритет) с датами.

Inputs (local, must read first)
- memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/06-20251030-1926-report-finance-cfa-platforms-status.md
- memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/08-CFA_operators__by-sheet_20251026-113923/CFA_operators__all_sheets_20251026-113923.md
- memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/08-CFA_operators__by-sheet_20251026-113923/Основной.csv
- memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/08-CFA_operators__by-sheet_20251026-113923/Рэнкинг_ОИС_ЦФА.csv
- memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/08-CFA_operators__by-sheet_20251026-113923/Фичи___новое.csv
- memory-bank/context/current-context/additional-info-for-analysing/20251022-artefacts/08-CFA_operators__by-sheet_20251026-113923/Фичи___старое.csv

Вопрос — Ответ (допущения и фокус)
1) Юрисдикция и регулятор в фокусе?
— РФ, ЦБ РФ (259‑ФЗ) как регулятор ОИС/ЦФА; AML/CFT (Росфинмониторинг). RU‑источники приоритетны.

2) ГОСТ/ФСБ‑криптография важна?
— Да. Проверять УКЭП/63‑ФЗ совместимость, упоминания CryptoPro/ГОСТ/HSM отечественных.

3) Период актуальности данных?
— 2024–2025 (сортировка по дате публикации, не старше 24 месяцев; старые — только как исторический контекст).

4) Что именно подтверждать по каждой платформе?
— DLT/ledger (Fabric/Besu/Quorum/immudb/own), custody (HSM/MPC vendor), УКЭП/КЭП провайдер, DvP/банк‑партнёры/ISO 20022/СБП, роли (ОИС/депозитарий/биржа), вторичка (RFQ/OTC/orderbook), API/документация, операционные метрики (если публичны), регстатус (лицензии/реестры), прод‑кейсы/эмитенты.

5) Разрешён ли «разумный вывод», если прямого релиза нет?
— Да, но только с явной маркировкой Confidence=[low|mid] и источником (например, вакансии/репозитории/конф‑доклады).

6) Выходные форматы?
— JSON (строго по схеме ниже) + Markdown‑таблица + Mermaid‑группировка; все с ссылками на источники и датами.

Output JSON Schema (per platform)
```json
{
  "name": "string",
  "status": "working|not_working|soon|license_pending",
  "role": ["ois","depository","exchange","bank","infra"],
  "dlt": {"type":"fabric|besu|quorum|immudb|own|unknown","evidence":[{"url":"...","date":"YYYY-MM-DD","quote":"...","confidence":"high|mid|low"}]},
  "custody": {"type":"hsm|mpc|unknown","vendors":["..."],"evidence":[...]},
  "ukep": {"providers":["CryptoPro","..."],"gost":true,"evidence":[...]},
  "dvp": {"model":"t+0|t+1|unknown","banks":["..."],"iso20022":true,"sbp":true,"evidence":[...]},
  "secondary": {"rfq":true,"orderbook":false,"evidence":[...]},
  "apis": {"openapi":true,"docs":["..."],"evidence":[...]},
  "hosting": {"ru_cloud":true,"on_prem":true,"evidence":[...]},
  "metrics": {"tps":"string","finality":"string","evidence":[...]},
  "issuers": ["..."],
  "regulatory": {"licenses":["..."],"register_links":["..."],"evidence":[...]},
  "sources": [{"url":"...","date":"YYYY-MM-DD","kind":"press|site|report|tg|job|code"}],
  "last_checked": "YYYY-MM-DD",
  "confidence_overall": "high|mid|low",
  "notes": "string"
}
```

Markdown Summary (per batch)
- Таблица: Платформа | Статус | Роль | DLT | Custody | УКЭП | DvP/Банк | Вторичка | Источники(кол-во) | Last Checked
- Mermaid: кластеры по статусам и по DLT‑типу (без скобок в узлах).

Source Priorities (RU‑first)
1) Официальные сайты/документация платформ (разделы API/технологии/пресс‑релизы)
2) Реестры ЦБ РФ (ОИС/лицензии), НРД/СПБ Биржа публикации
3) Деловые медиа: РБК, Ведомости, Коммерсант, Банки.ру
4) Проф.каналы/сообщества: TG «ЦФА в РФ», Habr (тех.статьи), Github/Code repos
5) Вакансии/конф‑доклады (как косвенные признаки, помечать Confidence=mid/low)

Process / Checklist
- [ ] Импортировать seed‑площадки из локальных файлов (06‑report, all_sheets.md, CSV).
- [ ] Для каждой: выполнить RU‑поиск + англ. при необходимости; собрать «DLT/ukep/dvp/secondary/hosting» с источниками и датами.
- [ ] Внести JSON‑карточку (по схеме) + добавить в Markdown‑таблицу.
- [ ] Отметить Confidence и пометки «unknown», если нет достоверных данных.
- [ ] Сформировать Mermaid 1: по статусам; Mermaid 2: по типу DLT.
- [ ] Выписать открытые вопросы и пробелы, которые требуют vendor‑контакта.

Seed Platform List (из локальных файлов)
- Работают (12): Альфа‑Банк, Атомайз, Блокчейн Хаб, ВТБ Капитал Трейдинг, ЕВРОФИНАНС МОСНАРБАНК, Токеон, Лайтхаус, НРД, Сбербанк, Системы распр. реестра, СПБ Биржа, МРЦ.
- Не работают (6): Банк Синара, Компания БКС, Газпромбанк, ТБанк, Токеник, [одна позиция может уточняться].
- Запуск скоро (1): МАДРИГАЛ ОИС.
- Ожидают лицензий (2): Статус, Спутник.

Search Hints (sample queries, RU)
- "<Платформа> ЦФА технология", "<Платформа> блокчейн платформа", "<Платформа> DLT Besu Fabric Quorum",
- "<Платформа> УКЭП КЭП CryptoPro ГОСТ", "<Платформа> HSM MPC ключи",
- "<Платформа> DvP банк партнёр ISO 20022 СБП",
- "<Платформа> API документация OpenAPI разработчикам".

Deliverables
- `competitors.jsonl` — NDJSON по схеме (1 строка = 1 платформа)
- `competitors.md` — таблица сводки + Mermaid диаграммы
- `competitors-sources.md` — список источников с цитатами (по каждому полю)

Validation
- Каждое критичное поле (DLT, УКЭП, банк/DvP) — минимум 2 независимых источника; если нет — помечать как unknown/mid/low.
- Указывать дату публикации и дату проверки.

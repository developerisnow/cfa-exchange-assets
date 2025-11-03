TL;DR
	•	Вводим “Layered Docs Protocol (LDP)”: L1=сырьё, L2=агрегация, L3=пакеты для стейкхолдеров; единая manifest.json как Source-of-Truth и кросс-линки.
	•	Даю промпт-спеки для агентов: Collector→Normalizer→Aggregator→Publisher→Librarian→QA, плюс DoD чек-листы.
	•	Ниже — мермейд-пайплайн, JSON-схема манифеста, конвенции имён и готовые шаблоны для твоего DDD/SoW и конкурентки.

⸻

Steps
	1.	Директории

PROJECT_ROOT=/Users/user/____Sandruk/__SecondBrain/projects/cifra-rwa-capital
mkdir -p $PROJECT_ROOT/{L1_raw,L2_summaries,L3_packs,indexes}

	2.	Именование файлов
YYYYMMDD-HHMM__topic__artifact__vNN.md
Примеры:

	•	20251103-2105__cfa__competitors-research__v01.md (L1)
	•	20251103-2140__cfa__competitors-ONE-PAGER__v01.md (L2)
	•	20251103-2200__cfa__customer-brief-pack__v01.md (L3)

	3.	manifest.json (SoT) — создать в корне, вести руками/агентом
Схема и пример см. ниже. Ключи: id, layer, topic, parents, derivations, sources, status, owner, dod_passed.
	4.	Пайплайн и роли

	•	Collector: кладёт сырые артефакты в L1, нормализует метаданные.
	•	Aggregator: по триггерам собирает ONE-PAGER и DEEP-SUMMARY в L2.
	•	Publisher: собирает customer pack в L3 (roadmap, SoW, glossary).
	•	Librarian: обновляет manifest.json, делает кросс-ссылки и indexes/*.md.
	•	QA: гоняет DoD-чек-листы, блокирует публикацию при нарушениях.

	5.	Триггеры

	•	Новый файл в L1_raw/* по topic → rebuild соответствующих L2_summaries/*.
	•	Изменился glossary или competitors → rebuild L3_packs/* затрагивающих эти topic_keys.

	6.	Формат артефактов
Каждый .md начинается с YAML-шапки (см. шаблон), далее краткая структура: Why→What→How→Result.

⸻

Диаграмма процесса

flowchart TD
A[L1 Raw: transcripts, research, emails, specs] --> B[Normalize: filename, YAML, tags, topic]
B --> C[Index: manifest.json update, cross-links]
C --> D[Aggregate L2: ONE-PAGER, DEEP-SUMMARY per topic]
D --> E[Publish L3: customer packs, SoW, roadmap]
E --> F[QA: DoD checks, signoff]
F --> G[Indexes: topic index, weekly rollups]


⸻

Таблица: слои и правила

Layer	Purpose	Typical Input	DoD (минимум)	Consumers
L1	Raw capture	транскрипты, конкуренты, глоссарий, артефакты Lovable, Keycloak notes	YAML есть, имя по конвенции, topic помечен, источники перечислены	Агентам, тебе
L2	Aggregated truth	k N L1 по одному topic	ONE-PAGER + DEEP-SUMMARY, ссылки на все L1, статус и риски	Ты, core-team
L3	Stakeholder pack	набор L2	SoW, Roadmap, Glossary, Assumptions, Open-Questions	Клиент, партнёры


⸻

JSON: manifest.json (схема и пример)

Schema (минимально достаточная)

{
  "version": "1.0",
  "items": [
    {
      "id": "20251103-2105__cfa__competitors-research__v01",
      "layer": "L1",
      "topic": ["cfa", "competitors"],
      "title": "Competitors research dump",
      "path": "L1_raw/20251103-2105__cfa__competitors-research__v01.md",
      "parents": [],
      "derivations": ["20251103-2140__cfa__competitors-ONE-PAGER__v01"],
      "sources": ["urls...", "files...", "calls..."],
      "owner": "alex",
      "status": "draft",
      "dod_passed": false
    }
  ]
}

Agent contract (правила обновления)
	•	layer ∈ {L1,L2,L3}
	•	Любая L2 обязана иметь parents → список L1 id.
	•	Любая L3 обязана иметь parents → список L2 id.
	•	dod_passed=true выставляет только QA-агент.

⸻

YAML-шапка шаблон для .md

---
id: 20251103-2140__cfa__competitors-ONE-PAGER__v01
layer: L2
topic: [cfa, competitors]
title: CFA Competitors — One Pager
owner: alex
status: draft
parents:
  - 20251103-2105__cfa__competitors-research__v01
sources:
  urls: [ ... ]
  files: [ ... ]
  calls: [ 2025-11-03-call-with-yury.md ]
assumptions:
  - bank unknown; need shortlist
risks:
  - scope creep in SoW
dod_checklist:
  - links to all L1 present
  - glossary terms resolved
  - open questions listed
updated: 2025-11-03 21:40
---


⸻

Универсальный System Prompt для всех агентов (LDP)

You operate under the Layered Docs Protocol (LDP).
Layers:
- L1 = raw artifacts (verbatim, minimally normalized)
- L2 = aggregated truth per topic (ONE-PAGER + DEEP-SUMMARY)
- L3 = stakeholder packs (SoW, Roadmap, Glossary, Assumptions, Open Questions)

Rules:
- Never lose provenance: every L2 cites all L1 parents; every L3 cites all L2 parents.
- Update manifest.json on every create/update with correct layer, topic, parents, derivations, sources.
- Respect filename convention: YYYYMMDD-HHMM__topic__artifact__vNN.md
- Enforce DoD checklists before promoting to a higher layer.
- Output format: Why → What → How → Result. Keep it concise.

Triggers:
- On new/updated L1 for a topic → rebuild L2 for that topic.
- On glossary/competitor change → rebuild impacted L3 packs.

Blocking conditions:
- Missing sources, missing parents, broken links, or unmet DoD → do not publish.


⸻

Роли и короткие промпты

Collector (L1)

Role: Normalize incoming raw content.
Input: raw text/files about topic=<X>.
Tasks:
1) Save to L1_raw with correct filename.
2) Add YAML front matter with topic, sources, assumptions.
3) Append entry to manifest.json (layer=L1, no parents, status=draft).
DoD: YAML present, topic set, sources listed, path written to manifest.

Aggregator (L2)

Role: Build ONE-PAGER and DEEP-SUMMARY per topic from L1 parents.
Input: topic=<X>, list of L1 ids.
Tasks:
1) ONE-PAGER: problem, current state, key findings, 3 risks, 3 next steps.
2) DEEP-SUMMARY: structured synthesis with citations to L1.
3) Write L2 files; set parents to L1 ids; update manifest.
DoD: all L1 cited; glossary terms resolved; open-questions block; links checked.

Publisher (L3)

Role: Create stakeholder pack.
Input: topic=<X>, L2 ids.
Tasks:
1) SoW v0 (scope, out-of-scope, assumptions, dependencies).
2) Roadmap v0 (6-12 weeks, milestones).
3) Customer brief (non-technical).
4) Update manifest (parents=L2 ids), prepare index entry.
DoD: SoW+Roadmap present; no orphan links; status set to 'review'.

Librarian

Role: Maintain manifest and indexes.
Tasks:
- Sync parents/derivations, fix broken links, generate indexes/topic-rollups.
- Produce indexes/<topic>.md with tables of L1/L2/L3 and last-updated.
DoD: manifest validates; all ids resolve; index regenerated.

QA

Role: Gatekeeper.
Tasks:
- Run DoD checklists; verify sources; ensure assumptions/risks/open-questions filled.
- If pass → set dod_passed=true and status=published.
- If fail → add 'fixme' list to the file and keep status=draft.

DDD/SoW Extractor (узко под твой звонок)

Role: From L1 research + call notes extract DDD and SoW skeleton.
Tasks:
- Bounded Contexts: Identity&Access (Keycloak), KYC/KYB, Asset Issuance, Custody, Payments(SBP), OrderBook(Primary), Admin/Backoffice.
- Entities: Customer, Issuer, Instrument(CFA type), Order, Wallet, Credential, BankAccount, AuditLog.
- Integrations: Bank=?, KYC=?, MPC/HSM=?, Ledger candidates: Besu/Fabric/...
Deliverables: 
- L2 ONE-PAGER "DDD overview"
- L2 DEEP-SUMMARY "SoW v0"
- L3 "Customer pack: DDD+SoW+Roadmap"


⸻

Шаблоны артефактов

L2 ONE-PAGER (пример для Competitors)

# CFA Competitors — One Pager
**Why**: выбрать реалистичный baseline по рынку  
**What**: кто в РФ реально работает; на чём; что интегрировано  
**How**: анализ 16 L1 доков; верификация дат и функций  
**Result**: shortlist платформ и фич для MVP

- Who works now: <A,B,C>  ссылки
- Ledger stack: <Besu/Fabric/Waves/...> ссылки
- Custody/HSM: <CryptoPro/KC1/KC2/MPC?> ссылки
- Banks: <Сбер/Альфа/...> ссылки
- Risks: 1) интеграции не подтверждены 2) УКЭП/ГОСТ не закрыт 3) DvP неопределён
- Next: попросить у клиента названия банков, KYC провайдера, HSM, MPC

L3 SoW v0 (скелет под твой кейс)

# Scope of Work v0 — CFA Platform
In-scope: KYC/KYB, Issuance, Custody, Payments(SBP), Primary OrderBook, Admin
Out-of-scope: Secondary market, OTC, advanced analytics
Assumptions: банк=?, KYC=?, HSM/MPC=?, Ledger candidate=Besu IBFT
Dependencies: банк API доступ; Keycloak repo; Lovable UI assets
Milestones: M1 Architecture&DDD, M2 Integrations PoC, M3 Issuance Flow, M4 Primary OB, M5 Compliance pack
Risks: интеграции задержатся; юр.обеспечение выпусков; производительность ledger
Open Questions: обеспечение эмитента? DvP модель? депозитарная схема?


⸻

DoD чек-листы (минимум)
	•	L1 DoD: имя по конвенции; YAML с topic, sources; ссылки кликабельны; путь записан в manifest.
	•	L2 DoD: ONE-PAGER+DEEP-SUMMARY; все L1 сосланы в parents; блоки assumptions/risks/open-questions; glossary-термины раскрыты.
	•	L3 DoD: SoW+Roadmap+Customer brief; все L2 в parents; статус review; индексы обновлены.

⸻

Мини-индекс на тему (авто-сбор Librarian)

# Index — topic: cfa
| Layer | Id | Title | Updated | Status |
|---|---|---|---|---|
| L1 | 20251103-2105... | Competitors research dump | 2025-11-03 | draft |
| L2 | 20251103-2140... | Competitors — One Pager | 2025-11-03 | draft |
| L3 | 20251103-2200... | Customer pack — CFA | 2025-11-03 | review |


⸻

Что сказать людям “в одно предложение”

Мы работаем слоями: всё сырое кладём в L1, по теме автоматически собираем выжимку в L2, а для внешних делаем L3-пакеты; всё связано через единый manifest.json, поэтому ничего не теряется и всегда ясно, что из чего получилось.

⸻

Next actions
	1.	Создай папки и manifest.json в корне проекта (шаблон выше).
	2.	Залей текущие: competitors, glossary, call-notes в L1_raw с YAML.
	3.	Запусти Aggregator на topic=cfa: сгенерируй ONE-PAGER и DEEP-SUMMARY.
	4.	Запусти DDD/SoW Extractor → собери L3 customer pack.
	5.	Привяжи Librarian к cron/хуку: при изменении L1 → rebuild L2, при изменении L2 → пометь L3 к обновлению.

Если хочешь — дам короткий Makefile и валидатор manifest.json под jq/yq.
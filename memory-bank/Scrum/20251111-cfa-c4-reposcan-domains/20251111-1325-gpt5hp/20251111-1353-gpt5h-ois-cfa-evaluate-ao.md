## TL;DR

* **Репозиторий a.ozherelev (c2p_ois-cfa):** каркас крепкий: .NET 9 микросервисы, YARP‑маршруты, TS‑SDK, Helm для Fabric, UML/C4. Уровень зрелости — **PoC→Dev**: есть тесты/схемы/диаграммы, но ряд интеграций и DLT‑адаптеры в dev‑режиме.     
* **Идея оценки (20251004):** это не смета, а референс‑архитектура с дорожной картой; полезно для scope, но нет WBS/ресурсной модели — требует приземления в задачи и критерии приёмки. 
* **Пакет 2025W44:** хорошо «закрепляет» 560ч через ADR, C4, deployment и дорожную карту; bias от реф‑архитектуры есть (например, выбор Kong/Node), но ревью AlexA добавило структурности. Для бюджета — норм основа, но нужно разложить на инкременты и SLA.     

---

## Steps

1. **Код и инфраструктура (a.ozherelev).** Проверил YARP‑прокси и кластеры сервисов; наличие фронтов (Next.js), TS‑SDK; EF‑схемы/валидаторы; Helm для Fabric/CA; dev‑скрипты для chaincode.       
2. **DLT‑контур.** Проверил helm‑джобы approve/rollback, скрипт chaincode‑API (dev‑only). Оценил риск «dev http shim для peer CLI».   
3. **Диаграммы/контракты.** PlantUML sequence (эмиссия/выплаты/покупка); drawio C4/security; OpenAPI для ESIA/bank‑интеграций (частично).   
4. **Сопоставил с 20251004.** Там — целевая «модулярка» и процессы (KYC, Tokenization, DvP и т.д.) без трудозатрат; полезно как scope‑рамка. 
5. **Сопоставил с 2025W44.** ADR‑решения (Fabric>Eth, DB‑per‑service), C4/Deployment на AWS/EKS, таймлайн 560ч, ресёрч/конкуренты.     

---

## Table — Snapshot (6 ключевых измерений)

| Dimension             | Repo a.ozherelev (факты)                                                                                             | 20251004 (идея)                                          | 2025W44 (артефакты)                          | Verdict                                                                         |
| --------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------- |
| **Architecture**      | .NET 9 микросервисы, YARP‑маршруты `/v1/*` на identity/issuance/registry/settlement/compliance. PlantUML/C4 есть.    | Полная реф‑архитектура ОИС (каналы, шина, домены, DLT).  | C4+Deployment на EKS, секьюрити‑слои, ADR.   | Совместимо по доменам; расхождение по стеку шлюза/языкам.                       |
| **Code & Tests**      | Unit‑тесты домена/сервисов (Money/Schedule/Issuance), валидаторы FluentValidation.                                   | —                                                        | —                                            | + за TDD‑сигналы; покрытие видеть в отчётах — пока не видно.                    |
| **DLT path**          | Helm для chaincode/CA; approve/rollback jobs; **dev** chaincode‑API shim (HTTP→peer CLI).                            | DLT — Fabric/Besu/immudb как варианты; audit/якорение.   | Решение: **Fabric** (ADR‑001).               | В репо нужен продовый SDK/peer‑gateway вместо dev shim.                         |
| **Security/IAM**      | Keycloak/OIDC (ESIA adapter OpenAPI), конфиги фронтов с realm/client. GOST‑57580 mapping (драфт).                    | Zero‑trust, HSM, комплаенс в доменах.                    | DMZ/WAF/IDS/SIEM/Keycloak/Vault схемы.       | Базис есть; потребуются политики, secrets, маппинг ролей/атрибутов.             |
| **Frontends & SDK**   | Backoffice скелет (KYC/Qualification/Audit/Payouts), TS‑SDK (`getInvestorStatus`, `runSettlement`).                  | Каналы UIs описаны концептуально.                        | Контексты/персоны в C4.                      | Готовность UI — low‑mid; SDK есть, но нужен генератив из OpenAPI всех сервисов. |
| **Delivery/Estimate** | Графаны/метрики (примеры), outbox в settlement/compliance; roadmap внутри репо не фиксирован.                        | Дорожная карта MVP→GA (без трудозатратной сетки).        | Roadmap 560ч, фазы, конкуренты.              | 560ч выглядят реалистично для **primary‑only**; с вторичкой — маловато.         |

---

### Stack deltas (коротко)

| Area            | Repo                 | 2025W44                               | Риск/Trade‑off                                                 |
| --------------- | -------------------- | ------------------------------------- | -------------------------------------------------------------- |
| API Gateway     | **YARP (.NET)**      | **Kong**                              | Kong даёт out‑of‑box плагins/OPA; YARP проще для .NET команды. |
| Backend langs   | **.NET 9** (core)    | **Node/NestJS + Go**                  | Полиглот увеличит нагрузку DevOps/QA.                          |
| DLT integration | Helm + dev shim      | Fabric peer‑cluster (Prod)            | Путь из dev‑shim в prod‑SDK обязателен.                        |
| Observability   | Grafana expr sample  | Полный security/observability контур  | Достроить трассинг/логи/SLO.                                   |

---

### Что это значит по сути

* **Проект Ожерелёва** — уже за пределами «пустого шаблона»: маршрутизация, DTO/валидаторы, EF‑схемы, тесты, UI‑скелеты и DevOps‑артефакты для Fabric налицо. Ключевой «красный флаг» — **dev‑only** обвязка для chaincode и локальные endpoints в конфиге (не продовый интерфейс к Fabric).  
* **20251004** хорошо задаёт визию/контуры, но **не является сметой**; её задача — границы и non‑func требования, а не часы. 
* **2025W44** — качественный «container» для защиты оценки: есть ADR‑обоснования (Fabric, DB‑per‑service), C4/Deployment/секьюрити, таймлайн и бенч по конкурентам. Для сделки с заказчиком этого **почти** достаточно — не хватает **WBS + acceptance** на каждый инкремент.    

---

## Next actions

1. **Утвердить стек**: YARP+.NET vs Kong+Node — выбрать один первичный путь (gate: SSO, rate‑limit, audit). Зафиксировать ADR‑006 «Gateway choice».  
2. **DLT в прод:** выкинуть dev shim → Fabric SDK/Peer Gateway, e2e‑интеграционные тесты (issue/transfer/redeem), secrets/PKI через Helm/SealedSecrets. 
3. **Разложить 560ч в WBS:** 8–12 work‑packages с **DoD/acceptance** (например, *Settlement T+0 happy path* → demo+load test). Привязать к ADR/диаграммам. 
4. **Закрыть рег‑контуры:** ESIA→OIDC e2e, KEP/UKÉP happy path (EDO), минимальные отчёты (ISO20022/XBRL экспорт). 
5. **Обсервабилити:** добавить трассировку/логи/SLO и дешборды на крупные домены (Orders/Payouts/Compliance). 
6. **Scope hygiene:** если MVP — **только первичка**, заморозить Trading/Orderbook из 2025W44; RFQ/вторичку вынести в v1.1. 

Если нужно, сделаю **WBS JSON** (work‑packages→tasks→acceptance→owner→hrs) по 560ч и сведу **gap‑list** для перевода dev‑DLT в прод.

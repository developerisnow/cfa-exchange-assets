# TL;DR

* Converted your “Капитал — ОИС ЦФА” context block into **Mermaid** with a dashed **Доменные сервисы** subgraph.
* **No parentheses used** in any labels to avoid renderer issues.
* Arrows mirror the logic: участники → Платформа → доменные сервисы → реестр и отчётность.

# Steps

1. Copy the code below into any Mermaid-enabled renderer.
2. If you need bi-directional arrows, replace `-->` with `<-->`.
3. Tweak styles only if your theme hides the dashed border.

---

## Diagram 1 — Context: Участники → Платформа → Доменные сервисы

```mermaid
flowchart LR
    %% Orientation
    %% No parentheses in labels

    %% Participants
    EM["Эмитент"]
    INV["Инвестор"]
    BR["Брокер/Дилер"]
    BANK["Банк/НСПК"]
    REG["Регулятор"]

    %% Core platform
    CAP["Национальная платформа «Капитал» — ОИС ЦФА"]

    %% Flows from participants to platform
    EM --> CAP
    INV --> CAP
    BR --> CAP
    BANK --> CAP
    REG --> CAP

    %% Domain services cluster
    subgraph cluster_domain["Доменные сервисы"]
      direction LR

      KYC["KYC/KYB и Идентификация"]
      REGISTRY["Реестр участников и ролей"]
      CUST["Custody и Кошельки HSM MPC"]
      SETT["Settlement и DvP"]
      TOK["Токенизация и Выпуск ЦФА"]
      AML["Комплаенс и AML"]

      LEDGER["Неизменяемый реестр DLT immudb"]
      DISC["Отчётность и Disclosure"]
    end

    %% Platform to domain services
    CAP --> KYC
    CAP --> CUST
    CAP --> SETT
    CAP --> TOK
    CAP --> AML

    %% Intra-domain flows
    KYC --> REGISTRY
    AML --> DISC
    CUST --> LEDGER
    SETT --> LEDGER
    TOK --> LEDGER

    %% Styling
    style cluster_domain stroke-dasharray: 5 5,stroke:#777,fill:none
```

---

## Diagram 2 — Доменные сервисы только

```mermaid
flowchart LR
    subgraph cluster_domain["Доменные сервисы"]
      direction LR
      KYC["KYC/KYB и Идентификация"] --> REGISTRY["Реестр участников и ролей"]

      CUST["Custody и Кошельки HSM MPC"] --> LEDGER["Неизменяемый реестр DLT immudb"]
      SETT["Settlement и DvP"] --> LEDGER
      TOK["Токенизация и Выпуск ЦФА"] --> LEDGER

      AML["Комплаенс и AML"] --> DISC["Отчётность и Disclosure"]
    end

    style cluster_domain stroke-dasharray: 5 5,stroke:#777,fill:none
```

---

## Mapping of sanitized labels

| Original label                            | Mermaid label used                         |
| ----------------------------------------- | ------------------------------------------ |
| Национальная платформа «Капитал»  ОИС ЦФА | Национальная платформа «Капитал» — ОИС ЦФА |
| Custody / Кошельки  HSM/MPC               | Custody и Кошельки HSM MPC                 |
| Неизменяемый реестр  DLT/immudb           | Неизменяемый реестр DLT immudb             |
| Брокер/Дилер                              | Брокер/Дилер                               |
| KYC/KYB и Идентификация                   | KYC/KYB и Идентификация                    |
| Settlement и DvP                          | Settlement и DvP                           |

---

## Next actions

* Нужен такой же экспорт по **большой общей диаграмме**. Если есть исходник или более чёткий снимок, дам полный Mermaid 1-в-1.
* Сказать, где нужны двунаправленные стрелки и где обязательны связи платформы с реестром напрямую — добавлю.

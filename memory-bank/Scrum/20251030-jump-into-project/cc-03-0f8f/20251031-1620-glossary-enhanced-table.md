---
created: 2025-10-31 16:20
updated: 2025-10-31 16:20
type: glossary
sphere: finance, blockchain
author: cc-03-0f8f
agentID: 5c916dc8-0f8f-4bc7-87e0-46f479e4b3f2
version: 1.0.0
tags: [glossary, vocabulary, domains, education]
---

# 📚 Enhanced Glossary: ЦФА/RWA Platform Terms

## 🎯 Core Terms Table

| Abbreviation | Russian                                                                                        | International                  | Domain         | Explanation                                 | Why Important              | Key Differences                            | Related             |
| ------------ | ---------------------------------------------------------------------------------------------- | ------------------------------ | -------------- | ------------------------------------------- | -------------------------- | ------------------------------------------ | ------------------- |
| **ЦФА**      | Цифровые Финансовые Активы                                                                     | DFA (Digital Financial Assets) | Legal/Finance  | Токенизированные права требования по 259-ФЗ | Основа всей платформы      | ЦФА = Russian regulated, DFA = global term | RWA, Security Token |
| **RWA**      | Реальные активы                                                                                | Real World Assets              | Finance/Crypto | Физические активы в блокчейне               | Мировой тренд токенизации  | RWA шире чем ЦФА, включает commodities     | ЦФА, Tokenization   |
| **ОИС**      | Оператор Информационной Системы                                                                | Platform Operator              | Regulatory     | Лицензированный оператор по 259-ФЗ          | Требуется для легальности  | Аналог exchange license в крипто           | КИС, Регулятор      |
| **DvP**      | Поставка против платежа. Delivery versus Payment (атомарная поставка‑против‑платежа), T+0/T+1. | Delivery vs Payment            | Settlement     | Атомарная сделка актив↔деньги               | Исключает риск контрагента | T+0 instant vs T+2 traditional             | PvP, Settlement     |
| **КЭП/УКЭП** | Квалифицированная ЭП                                                                           | Qualified Digital Signature    | Legal/Tech     | Юридически значимая подпись (63-ФЗ)         | Обязательна для сделок     | УКЭП = усиленная, КЭП = квалифицированная  | eIDAS, PKI          |
| ОИС ЦФА      | оператор информационной системы цифровых финансовых активов                                    |                                |                |                                             |                            |                                            |                     |

## 🏗️ Architecture Terms

| Abbreviation     | Russian                                                                                        | International                            | Domain       | Explanation                             | Why Important             | Key Differences                           | Related               | Examples                                                                           |
| ---------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------- | ------------ | --------------------------------------- | ------------------------- | ----------------------------------------- | --------------------- | ---------------------------------------------------------------------------------- |
| **DLT** (Ledger) | Распределенный реестр                                                                          | Distributed Ledger                       | Tech         | База данных без центрального управления | Неизменяемость записей    | DLT ≠ Blockchain (blockchain это вид DLT) | Blockchain, Consensus | (например, Hyperledger Fabric/Besu) <br>или audit‑core (immudb) с якорением хэшей. |
| **BFT**          | Византийская отказоустойчивость                                                                | Byzantine Fault Tolerance                | Consensus    | Консенсус при наличии злоумышленников   | Критично для permissioned | PBFT в Fabric, IBFT в Besu                | Consensus, PoS        |                                                                                    |
| **HSM**          | Аппаратный модуль безопасности                                                                 | Hardware Security Module                 | Security     | Физическое устройство для ключей        | Требование регулятора     | HSM vs MPC (multi-party computation)      | KMS, MPC              |                                                                                    |
| **CQRS**         | Разделение команд и запросов                                                                   | Command Query Responsibility Segregation | Architecture | Разделение записи и чтения              | Масштабируемость          | Write model ≠ Read model                  | Event Sourcing        |                                                                                    |
| **C4**           | Контекст, Контейнеры, Компоненты, Код                                                          | Context, Container, Component, Code      | Architecture | Модель описания архитектуры             | Стандарт индустрии        | 4 уровня детализации                      | UML, ArchiMate        |                                                                                    |
| MPC              | см. HSM. аппаратные модули безопасности <br>/ многопартийные вычисления для управления ключами |                                          |              |                                         |                           |                                           |                       |                                                                                    |
|                  |                                                                                                |                                          |              |                                         |                           |                                           |                       |                                                                                    |

## 💼 Business Terms

| Abbreviation | Russian | International | Domain | Explanation | Why Important | Key Differences | Related |
|--------------|---------|---------------|--------|-------------|---------------|-----------------|---------|
| **KYC/KYB** | Знай своего клиента/бизнес | Know Your Customer/Business | Compliance | Идентификация участников | Требование AML | KYB для юрлиц, KYC для физлиц | AML, Compliance |
| **AML/CFT** | Противодействие отмыванию | Anti-Money Laundering | Compliance | Финансовый мониторинг | Обязательно по 115-ФЗ | Russian специфика санкций | Росфинмониторинг |
| **MVP** | Минимально жизнеспособный продукт | Minimum Viable Product | Business | Первая рабочая версия | Быстрый выход на рынок | Primary market only для MVP | Roadmap, Phases |
| **SLA** | Соглашение об уровне сервиса | Service Level Agreement | Business | Гарантии доступности | 99.95% для ОИС | Финансовые штрафы за простой | NFR, Uptime |
| **DoD** | Критерии готовности | Definition of Done | Agile | Измеримые результаты | Прозрачность прогресса | Acceptance criteria для каждой задачи | Sprint, Backlog |

## 🔧 Technology Choices

| Technology | Russian Context | Global Standard | Domain | Our Choice | Why | Alternatives | Risk |
|-----------|-----------------|-----------------|--------|------------|-----|--------------|------|
| **Hyperledger Fabric** | Стандарт для enterprise | IBM backed | Blockchain | Вероятный выбор | Используют Сбер, Атомайз | Besu, immudb | Сложность |
| **Hyperledger Besu** | Мало примеров в РФ | EVM compatible | Blockchain | Альтернатива | Проще smart contracts | Fabric, Ethereum | Adoption |
| **immudb** | Не блокчейн | Append-only DB | Database | Fallback | Простота развертывания | Real blockchain | Не true DLT |
| **PostgreSQL** | Везде используется | ACID standard | Database | Основная БД | Надежность, опыт | Oracle, MySQL | None |
| **Kubernetes** | Стандарт контейнеризации | CNCF project | Infrastructure | Обязательно | Масштабируемость | Docker Swarm | Complexity |

## 📊 Competitors Specific Terms

| Platform | Type | Key Tech | Domain | What They Do | Our Learning | Status |
|----------|------|----------|--------|--------------|--------------|--------|
| **Сбербанк** | Bank | Unknown DLT | Finance | Largest scale | KYC/AML processes | ✅ Working |
| **Атомайз** | Tech | Fabric + Order books | Tech | Pure tech play | Architecture patterns | ✅ Working |
| **НРД** | Depository | Integration focus | Infrastructure | Central depository | Regulatory reporting | ✅ Working |
| **Lighthouse** | Invest | Unknown DvP | Trading | Investment platform | UI/UX patterns | ⚠️ Unknown DvP |
| **Токеон** | Tech | Ethereum fork | Blockchain | Smart contracts | Contract patterns | ✅ Working |

## 🎓 Learning Path

### For Yury (Business Focus)
1. **ЦФА vs RWA** - regulatory differences
2. **DvP importance** - risk mitigation
3. **MVP scope** - primary vs secondary market
4. **Timeline reality** - 1000h not 400h

### For Technical Team
1. **Fabric vs Besu** - architecture implications
2. **HSM vs MPC** - key management
3. **CQRS benefits** - scalability patterns
4. **Event sourcing** - audit trail

### For Investors
1. **Market size** - 12/20 platforms working
2. **Competitive advantage** - faster, cheaper
3. **Regulatory compliance** - 259-ФЗ ready
4. **Technology stack** - enterprise grade

---

## 📈 Domain Classification

### Regulatory (25%)
ЦФА, ОИС, КЭП, УКЭП, 259-ФЗ, 63-ФЗ, AML, КИС

### Technical (40%)
DLT, BFT, HSM, CQRS, C4, Fabric, Besu, PostgreSQL, Kubernetes

### Business (20%)
MVP, SLA, DoD, Roadmap, Sprint, Timeline

### Financial (15%)
DvP, Settlement, Primary Market, Secondary Market, Clearing

---

## 🔄 Version History

- **v1.0.0** - Initial comprehensive glossary with domains and relationships

---

*This glossary is a living document. Update when new terms emerge or understanding deepens.*
---
created: 2025-10-30 19:26
type: conversion
sphere: development
topic: graph-databases
tags: [mermaidjs, architecture, visualization, fintech, blockchain]
prompt: "Конвертировать три изображения архитектурных диаграмм платформы Капитал в mermaidjs формат, соблюдая корректный синтаксис без использования круглых скобок"
---



### Диаграмма 1: C4 Context - Национальная платформа «Капитал»

```mermaid
flowchart LR
    subgraph ext[" Внешние участники "]
        emitent["ВладельцыЦФА"]
        investor["Инвесторы-в-ЦФА"]
        bank["Банк/НСПК"]
        regulator["Регулятор"]
        CapitalNPC["КапиталНПК"]
    end
    
    platform["Национальная платформа<br/>«Капитал»<br/>ОИС ЦФА"]
    
    subgraph domain[" Доменные сервисы "]
        kyc["КУС/KYB и<br/>Идентификация"]
        reg_roles["Реестр участников<br/>и ролей"]
        custody["Custody / Кошельки<br/>HSM/MPC"]
        settlement["Settlement и DvP"]
        tokenization["Токенизация и<br/>Выпуск ЦФА"]
        compliance["Комплаенс и AML"]
    end
    
    registry["Неизменяемый реестр<br/>DLT/immudb"]
    disclosure["Отчётность и<br/>Disclosure"]
    
    emitent --> platform
    investor --> platform
    broker --> platform
    bank --> platform
    regulator --> platform
    
    platform --> kyc
    platform --> custody
    platform --> settlement
    platform --> tokenization
    platform --> compliance
    
    kyc --> reg_roles
    
    kyc --> registry
    custody --> registry
    settlement --> registry
    tokenization --> registry
    compliance --> registry
    
    registry --> disclosure
    platform --> disclosure
    
    classDef platformStyle fill:#6495ED,stroke:#333,stroke-width:3px,color:#fff
    classDef externalStyle fill:#90EE90,stroke:#333,stroke-width:2px
    classDef serviceStyle fill:#FFE4B5,stroke:#333,stroke-width:2px
    classDef dataStyle fill:#DDA0DD,stroke:#333,stroke-width:2px
    
    class platform platformStyle
    class emitent,investor,broker,bank,regulator externalStyle
    class kyc,custody,settlement,tokenization,compliance,reg_roles serviceStyle
    class registry,disclosure dataStyle
```

### Диаграмма 2: Детальная техническая архитектура платформы - Часть 1

Эта диаграмма показывает поток от внешних систем через API Gateway к доменным микросервисам:

```mermaid
flowchart LR
    subgraph external[" Внешние системы "]
        cabinet_all["Все кабинеты<br/>Эмитент/Инвестор/Брокер/Регулятор"]
        mobile["Мобильное приложение<br/>инвестора"]
        b2b_crest["B2B интеграции<br/>CREST/СЕСПК, ISO 20022, SWIFT"]
    end
    
    subgraph gateway[" API Gateway & Security "]
        https["HTTPS"]
        waf["WAF / Anti-DDoS"]
        api_gw["API Gateway<br/>oBondsMPC, Real-Time и FIX"]
        iam["IAM/SAM"]
        oauth["OAuth & Abacus<br/>Single-Sign-On"]
    end
    
    subgraph services[" Доменные микросервисы "]
        tls["TLS/TLS certificates"]
        sms["OSLSM/SMS+<br/>autoconfigId/SCP"]
        registry_part["Регистр участников"]
        kyc_kuv["КУС/КУВ<br/>идентификация, сертификаты"]
        analytics["Analytics<br/>cashflow/risk, операции"]
        orders["Order & Matching<br/>FIT-OMS, FIFO-RTQ"]
        decisions["Решения<br/>DeFi/O.C/Arbitration"]
        compliance_aml["Compliance/AML<br/>проверка ML/санкции"]
        tokenization_iss["Tokenization/Issuer<br/>выпуск HPA-операций"]
        collateral["Обеспечение<br/>мандаты"]
        custody_wallets["Custody/wallets<br/>HSM/MPC, ключи"]
        cbdc["CBDC-шлюзы<br/>расчетные операции"]
        blockchain_notary["Blockchain/Notary<br/>хранение ГССК"]
    end
    
    cabinet_all --> https
    mobile --> https
    b2b_crest --> https
    
    https --> waf
    waf --> api_gw
    api_gw --> iam
    iam --> oauth
    
    oauth --> tls
    oauth --> sms
    oauth --> registry_part
    oauth --> kyc_kuv
    oauth --> analytics
    oauth --> orders
    oauth --> decisions
    oauth --> compliance_aml
    oauth --> tokenization_iss
    oauth --> collateral
    oauth --> custody_wallets
    oauth --> cbdc
    oauth --> blockchain_notary
    
    classDef externalStyle fill:#98FB98,stroke:#333,stroke-width:2px
    classDef gatewayStyle fill:#87CEEB,stroke:#333,stroke-width:2px
    classDef serviceStyle fill:#FFE4B5,stroke:#333,stroke-width:2px
    
    class cabinet_all,mobile,b2b_crest externalStyle
    class https,waf,api_gw,iam,oauth gatewayStyle
    class tls,sms,registry_part,kyc_kuv,analytics,orders,decisions,compliance_aml,tokenization_iss,collateral,custody_wallets,cbdc,blockchain_notary serviceStyle
```

### Диаграмма 3: Детальная техническая архитектура платформы - Часть 2

Эта диаграмма показывает инфраструктурные сервисы и слой данных:

```mermaid
flowchart TB
    subgraph infra[" Инфраструктурные сервисы "]
        direction TB
        
        subgraph row1[" Базовые сервисы "]
            auth1["auth/service"]
            crud1["CRUD"]
            events1["events"]
            docs1["docs"]
        end
        
        subgraph row2[" Дополнительные сервисы "]
            auth2["auth/service"]
            crud2["CRUD"]
            events2["events"]
            docs2["docs"]
        end
        
        subgraph row3[" Расширенные сервисы "]
            auth3["auth/service"]
            crud3["CRUD"]
            events3["events"]
            docs3["docs"]
        end
    end
    
    subgraph data_layer[" Слой данных и хранилища "]
        direction TB
        
        kyc_data["КУС/КУВ и др"]
        immutable["Неизменяемый реестр<br/>DLT/events<br/>учетная политика"]
        accounts_data["Данные счетов"]
        sign["Sign<br/>КСД-Blockchain"]
        audit["Audit/service<br/>ПХД/Compliance"]
        eventbus["EventBus/ETL/CRM"]
        duma["ДУМА accounts<br/>STL/RLT, analytics"]
        api_broker["API broker"]
        mrp["MRP/ISO 20022"]
        mebo["МЭБО<br/>SRO 20022"]
    end
    
    subgraph integration[" Внешние интеграции "]
        direction TB
        
        external_systems["Внешние системы<br/>CSKA-broker, Scala, Karamba"]
        external_events["Внешний eventbus"]
        external_ksd["Blockchain/BTL/CSI"]
        external_aml["AML/SMR"]
    end
    
    row1 --> kyc_data
    row1 --> immutable
    row2 --> accounts_data
    row2 --> sign
    row3 --> audit
    row3 --> eventbus
    
    kyc_data --> duma
    immutable --> duma
    accounts_data --> duma
    sign --> external_ksd
    audit --> external_aml
    eventbus --> external_events
    
    duma --> api_broker
    api_broker --> mrp
    mrp --> mebo
    mebo --> external_systems
    
    classDef infraStyle fill:#B0C4DE,stroke:#333,stroke-width:2px
    classDef dataStyle fill:#DDA0DD,stroke:#333,stroke-width:2px
    classDef integrationStyle fill:#F0E68C,stroke:#333,stroke-width:2px
    
    class auth1,crud1,events1,docs1,auth2,crud2,events2,docs2,auth3,crud3,events3,docs3 infraStyle
    class kyc_data,immutable,accounts_data,sign,audit,eventbus,duma,api_broker,mrp,mebo dataStyle
    class external_systems,external_events,external_ksd,external_aml integrationStyle
```

## 📊 Пояснения к диаграммам

### Диаграмма 1 - C4 Context
Показывает высокоуровневый контекст платформы «Капитал»:
- **Внешние участники**: Эмитенты, инвесторы, брокеры, банки, регуляторы
- **Центральная платформа**: ОИС ЦФА (Оператор информационной системы цифровых финансовых активов)
- **Доменные сервисы**: KYC/KYB, Custody (HSM/MPC для ключей), Settlement (расчеты), Токенизация, Комплаенс
- **Инфраструктура**: Неизменяемый реестр на базе DLT/immudb, система отчетности

### Диаграмма 2 - Микросервисная архитектура (Frontend)
Детальная схема обработки запросов:
- **Внешние системы**: Веб-кабинеты, мобильные приложения, B2B интеграции (CREST, SWIFT, ISO 20022)
- **Security Layer**: WAF, Anti-DDoS, API Gateway с поддержкой разных протоколов
- **Аутентификация**: IAM/SAM, OAuth 2.0, Single Sign-On через Abacus
- **Доменные микросервисы**: 
  - Управление участниками и сертификатами
  - Аналитика (cashflow, риски)
  - Система торгов (Order Matching с FIFO)
  - DeFi решения и арбитраж
  - AML/Compliance с проверками санкций
  - Токенизация и выпуск активов
  - Custody с HSM/MPC
  - CBDC шлюзы для расчетов
  - Blockchain нотариат

### Диаграмма 3 - Инфраструктура и данные (Backend)
Показывает слой хранения и интеграций:
- **Инфраструктурные сервисы**: Повторяющиеся паттерны auth/CRUD/events/docs для каждого домена
- **Слой данных**:
  - Неизменяемый реестр (DLT) для аудита
  - Данные счетов и участников
  - Электронная подпись (КСД-Blockchain)
  - Audit trail для compliance
  - EventBus для асинхронной обработки
  - ДУМА (Депозитарная Учетная Микросервисная Архитектура) с STL/RTL
- **Внешние интеграции**:
  - MRP/ISO 20022 для стандартизированного обмена
  - МЭБО для межбанковских операций
  - Blockchain/BTL/CSI
  - AML/SMR системы

## 🎨 Цветовая легенда

- 🟦 **Синий**: Центральная платформа (ядро системы)
- 🟩 **Зеленый**: Внешние участники и системы
- 🟡 **Желтый/Бежевый**: Доменные микросервисы
- 🟪 **Фиолетовый**: Слой данных и хранилища
- 🔵 **Голубой**: API Gateway и security слой
- 🟨 **Золотой**: Интеграционный слой

## 📝 Технические особенности реализации

### Замена круглых скобок
Все технические детали, которые были в скобках в оригинале, представлены через:
- Переносы строк внутри узлов (`<br/>`)
- Разделители (запятая, тире)
- Контекстные пояснения без скобок

Например:
- `Custody / Кошельки (HSM/MPC)` → `Custody / Кошельки<br/>HSM/MPC`
- `Order & Matching (FIT-OMS, FIFO-RTQ)` → `Order & Matching<br/>FIT-OMS, FIFO-RTQ`

### Группировка через subgraph
Использованы именованные подграфы для логической группировки компонентов, что соответствует пунктирным контурам в оригинале.

### Стилизация
Применены CSS классы для визуального разделения типов компонентов:
- `platformStyle` - для центральной платформы
- `externalStyle` - для внешних участников
- `serviceStyle` - для микросервисов
- `dataStyle` - для хранилищ данных
- `gatewayStyle` - для API Gateway слоя
- `integrationStyle` - для интеграционных компонентов

---

**Примечание**: Диаграммы сохраняют все ключевые элементы оригиналов и могут быть отрендерены в любом markdown-редакторе с поддержкой Mermaid (Obsidian, GitHub, GitLab, VS Code и т.д.).
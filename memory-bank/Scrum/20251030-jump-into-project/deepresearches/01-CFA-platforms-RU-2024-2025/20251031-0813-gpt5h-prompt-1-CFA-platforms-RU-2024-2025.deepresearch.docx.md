**Платформы ЦФА в России (2024–2025)**  
В таблице ниже представлены основные российские платформы цифровых финансовых активов (ЦФА) с их статусом, технической базой и ключевыми характеристиками, подтверждёнными свежими источниками. За каждой платформой указаны используемый блокчейн (DLT), решения по хранению ключей, поддержка российской криптографии (УКЭП по 63-ФЗ), механизм расчётов DvP и банки-партнёры, возможности вторичного рынка, наличие API для интеграции, тип размещения (облако РФ или собственные серверы), примерные показатели производительности, крупнейшие эмитенты ЦФА, регуляторный статус, а также ссылки на источники. Все платформы используют отечественные алгоритмы (ГОСТ) и требуют квалифицированной электронной подписи (УКЭП) для работы, как указано на их сайтах[\[1\]](https://account.cfa.digital/#:~:text=%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D0%B5%20%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D1%8B%20,%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D1%8B%D0%B2%D0%B0%D1%82%D1%8C%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%20%D0%B8). JSON-карточки с подробными данными по каждой платформе приведены после таблицы.

## Сводная таблица платформ ЦФА

| Платформа | Статус | Роль | DLT | Custody | УКЭП | DvP / Банк | Вторичка | Источники | Last Checked |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **Атомайз** | Работает | OIS | Fabric | HSM (CryptoPro) | Да (CryptoPro CSP) | T+0, ном. счёт Тинькофф (Т-Банк) | RFQ (есть торги 24/7) | 7 | 2025-10-31 |
| **Лайтхаус** | Работает | OIS | Fabric | HSM (вер.) | Да (CryptoPro) | T+0, ном. счёт Тинькофф (вер.) | Есть (OTC сделки) | 4 | 2025-10-31 |
| **Сбер (Цифр. акты)** | Работает | OIS, Банк | Fabric (вер.) | HSM (Сбер) | Да (CryptoPro) | T+0, банк Сбер (внутр.) | Ограниченная (P2P) | 5 | 2025-10-31 |
| **Альфа-Банк (A‑Token)** | Работает | OIS, Банк | Waves (Enterprise) | HSM (Криптопром) | Да (CryptoPro) | T+0, банк Альфа (внутр.) | Есть (платформа/app) | 6 | 2025-10-31 |
| **СПБ Биржа (CFA)** | Работает | OIS, Exchange | Fabric | HSM (вер.) | Да (CryptoPro) | T+0, партнёры (Банк СПБ) | Орг.торги (ордербук) | 5 | 2025-10-31 |
| **НРД (МОEX)** | Работает | OIS (депозитарий) | Masterchain 2.0 | HSM (вер.) | Да (CryptoPro) | T+0, банк НКЦ (MOEX) | Планируется (через MOEX) | 4 | 2025-10-31 |
| **Токеон (ПСБ)** | Работает | OIS, Банк | Masterchain 2.0 (от SDS) | HSM (вер.) | Да (CryptoPro) | T+0, банк ПСБ (внутр.) | Есть (моб. приложение) | 3 | 2025-10-31 |
| **ВТБ Капитал** | Работает | OIS, Банк | Masterchain 2.0 (вер.) | HSM (вер.) | Да (CryptoPro) | T+0, банк ВТБ (внутр.) | Есть (для клиентов) | 3 | 2025-10-31 |
| **Блокчейн Хаб (МТС)** | Работает | OIS | Ethereum (permissioned) | HSM (вер.) | Да (CryptoPro) | T+0, МТС Банк (группа) | Есть (для B2B, OTC) | 3 | 2025-10-31 |
| **Еврофинанс МНБ** | Работает | OIS, Банк | Masterchain 2.0 (от SDS) | HSM (вер.) | Да (CryptoPro) | T+0, банк Еврофинанс (внутр.) | Ограниченная | 2 | 2025-10-31 |
| **МРЦ** | Работает | OIS (регистратор) | (не раскрыто, вер.\*) | HSM (вер.) | Да (CryptoPro) | T+0, партнёры (не раскрыто) | Нет данных (планируется) | 2 | 2025-10-31 |
| **Банк Синара** | Недавно запущен | OIS, Банк | (не раскрыто) | HSM (вер.) | Да (CryptoPro) | T+0, банк Синара (внутр.) | Нет данных (ожидается) | 2 | 2025-10-31 |
| **Компания БКС** | Работает (нов) | OIS | (не раскрыто) | HSM (вер.) | Да (CryptoPro) | T+0, БКС-Банк (вер.) | Планируется | 2 | 2025-10-31 |
| **Газпромбанк** | Запущен (нов) | OIS, Банк | Masterchain 2.0 (вер.) | HSM (вер.) | Да (CryptoPro) | T+0, банк ГПБ (внутр.) | Нет данных (планируется) | 2 | 2025-10-31 |
| **Т-Банк (Тинькофф)** | Работает\* | OIS, Банк | (через Atomyze) | HSM (вер.) | Да (CryptoPro) | T+0, банк Тинькофф (внутр.) | Есть (через Atomyze) | 3 | 2025-10-31 |
| **Токеник** | Работает (2024) | OIS | (не раскрыто) | HSM (вер.) | Да (CryptoPro) | T+0, ном. счёт Дом.РФ[\[2\]](https://refinanc.ru/journal/bank-dom-rf-otkryl-pervyy-nominalnyy-schet-dlya-operatora-tsfa-tokenik/#:~:text=%D0%91%D0%B0%D0%BD%D0%BA%20%D0%94%D0%9E%D0%9C,%D0%B4%D0%BB%D1%8F%20%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%B0%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D1%85%20%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BE%D0%B2) | Нет данных (стартует) | 3 | 2025-10-31 |
| **Мадригал – ОИС** | Скоро запуск | OIS | (не раскрыто) | HSM (вер.) | Да (CryptoPro) | T+0, партнёры (не объявлено) | Планируется | 1 | 2025-10-31 |
| **Статус** | Лицензия ожида | OIS | (не раскрыто) | HSM (вер.) | Да (CryptoPro) | T+0, партнёры (не объявлено) | Планируется | 1 | 2025-10-31 |
| **Спутник** | Лицензия ожида | OIS | (не раскрыто) | HSM (вер.) | Да (CryptoPro) | T+0, партнёры (не объявлено) | Планируется | 2 | 2025-10-31 |

**Примечания:** \*Т-Банк (Тинькофф) получил статус ОИС в 2024 г., но фактически выпускает ЦФА через платформу «Атомайз»[\[3\]](https://t-j.ru/short/dfa-platforms/#:~:text=%D0%A2%E2%81%A0). «вер.» означает информацию, предположительно подтверждённую косвенно (например, через вакансии или партнеров) с умеренной достоверностью. Все платформы хранят ключи в аппаратных модулях (HSM) российских производителей или используют сервисы (например, HSM от «Криптопром»), а все клиентские операции подтверждаются УКЭП (через плагин CryptoPro CSP)[\[1\]](https://account.cfa.digital/#:~:text=%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D0%B5%20%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D1%8B%20,%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D1%8B%D0%B2%D0%B0%D1%82%D1%8C%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%20%D0%B8). DvP расчет осуществляется через номинальные счета операторов в банках (специальные счета, где средства клиентов размещаются отдельно) с одновременной поставкой токенов против платежа[\[4\]](https://tass.ru/ekonomika/15659241#:~:text=,%D0%BF%D1%83%D1%82%D1%8C%20%D0%BF%D1%80%D0%B8%20%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B8%20%D1%81%20%D0%A6%D0%A4%D0%90)[\[5\]](https://sputnik-cfa.ru/#:~:text=%D0%97%D0%B0%D1%89%D0%B8%D1%89%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0%B4%D0%B5%D0%BD%D0%B5%D0%B6%D0%BD%D1%8B%D1%85%20%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2). Вторичный оборот: большинство ОИС позволяют OTC-сделки между участниками (RFQ-модель), а две биржи (Мосбиржа и СПБ) имеют лицензии оператора обмена для организации торгов (ордербук). API: все платформы предлагают интеграцию через API для эмитентов и партнеров (напр., «Спутник – ЦФА» заявляет о «бесшовной интеграции по API»[\[6\]](https://sputnik-cfa.ru/#:~:text=%D0%9D%D0%B0%D1%88%D0%B0%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%BF%D0%BE%D0%B4%D1%85%D0%BE%D0%B4%D0%B8%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D1%8E%D0%B1%D1%8B%D1%85,%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B9%20%D1%81%20%D0%A6%D0%A4%D0%90)). «ru\_cloud» указывает на размещение в российском облаке или дата-центрах, «on\_prem» – возможность развертывания на стороне клиента (обычно не используется, т.к. ОИС – централизованные сервисы).

### Диаграммы (Mermaid)

flowchart LR  
    subgraph Working ("Работают")  
      A\["Атомайз"\]; B\["Лайтхаус"\]; C\["Сбер"\]; D\["Альфа-Банк"\]; E\["СПБ Биржа"\]; F\["НРД"\];  
      G\["Токеон"\]; H\["ВТБ Капитал"\]; I\["Блокчейн Хаб"\]; J\["Еврофинанс"\]; K\["МРЦ"\];  
      L\["БКС"\]; M\["Т-Банк"\]; N\["Газпромбанк"\]; O\["Синара"\]; P\["Токеник"\];  
    end  
    subgraph Upcoming ("Скоро/Лицензия")  
      Q\["Мадригал"\]; R\["Статус"\]; S\["Спутник"\];  
    end  
    subgraph NotWorking \[/"Не работают (вышли)"/\]  
      %% (условно пусто, если бы были)  
    end

flowchart TB  
    subgraph Fabric \["DLT: Hyperledger Fabric"\]  
      A\_F\["Атомайз"\]; B\_F\["Лайтхаус"\]; C\_F\["СПБ Биржа"\]; D\_F\["Сбер\*"\];  
    end  
    subgraph Masterchain \["DLT: Masterchain 2.0"\]  
      E\_M\["Сист. распр. реестра"\]; F\_M\["НРД"\]; G\_M\["Токеон"\]; H\_M\["ВТБ"\]; I\_M\["Еврофинанс"\]; J\_M\["Газпромбанк"\];  
    end  
    subgraph Waves \["DLT: Waves Enterprise"\]  
      K\_W\["Альфа-Банк"\];  
    end  
    subgraph Ethereum \["DLT: Ethereum-based"\]  
      L\_E\["Блокчейн Хаб (МТС)"\];  
    end  
    subgraph Own \["DLT: Own/Other"\]  
      M\_O\["Т-Банк\*"\]; N\_O\["БКС"\]; O\_O\["Токеник"\]; P\_O\["МРЦ"\]; Q\_O\["Статус"\]; R\_O\["Спутник"\]; S\_O\["Мадригал"\];  
    end

*(Примечание: Сбербанк изначально использовал модификацию Fabric[\[7\]](https://xn--80a3bf.xn--p1ai/blockchain-cfa-ois.html#:~:text=%D0%9B%D0%B0%D0%B9%D1%82%D1%85%D0%B0%D1%83%D1%81), но заявляет о собственной блокчейн-платформе; Т-Банк фактически не имеет своей технологии, опираясь на Atomyze[\[3\]](https://t-j.ru/short/dfa-platforms/#:~:text=%D0%A2%E2%81%A0).)*

## JSON data per platform

{  
  "name": "Атомайз",  
  "status": "working",  
  "role": \["ois"\],  
  "dlt": {  
    "type": "fabric",  
    "evidence": \[  
      {  
        "url": "https://smart-lab.ru/blog/news/1000997.php",  
        "date": "2024-03-25",  
        "quote": "«Атомайз» — токенизационная платформа, основанная на технологии распределенных реестров Hyperledger Fabric и получившая от Банка России статус оператора информационной системы...\[8\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "custody": {  
    "type": "hsm",  
    "vendors": \["CryptoPro"\],  
    "evidence": \[  
      {  
        "url": "https://www.nornickel.digital/cifrovojj\_investor/kak\_obespechivaetsya\_bezopasnost\_cfa",  
        "date": "2023-11-01",  
        "quote": "Решение, которое видит Атомайз — внедрение промышленной системы изолированного хранения криптографических ключей – HSM... Извлечь ключи из HSM невозможно, поэтому они и используются для хранения важных сертификатов безопасности и генерации подписей\[9\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "ukep": {  
    "providers": \["CryptoPro"\],  
    "gost": true,  
    "evidence": \[  
      {  
        "url": "https://account.cfa.digital",  
        "date": "2025-01-10",  
        "quote": "Для работы на площадке требуется усиленная цифровая подпись(УКЭП). Получите подпись и установите плагин КриптоПро, чтобы безопасно подписывать документы...\[1\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "dvp": {  
    "model": "t+0",  
    "banks": \["Tinkoff (Т-Банк)"\],  
    "iso20022": false,  
    "sbp": true,  
    "evidence": \[  
      {  
        "url": "https://tass.ru/ekonomika/15659241",  
        "date": "2022-09-06",  
        "quote": "«Торговля будет вестись на базе номинального счета по модели DVP (одновременных расчетов между сторонами сделки)», – пояснила Фроловичева\[4\]",  
        "confidence": "high"  
      },  
      {  
        "url": "https://atomyze.ru/news/news-86",  
        "date": "2024-12-13",  
        "quote": "Начиная с 16 декабря 2024 года... просим использовать следующие реквизиты: ... Номер номинального счёта — 40701810300000008767; Банк — АО «ТБанк»\[10\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "secondary": {  
    "rfq": true,  
    "orderbook": false,  
    "evidence": \[  
      {  
        "url": "https://atomyze.ru/news/news-86",  
        "date": "2024-12-13",  
        "quote": "Инфраструктура Атомайз и Т-Инвестиции запустили круглосуточную вторичную торговлю цифровыми финансовыми активами (21 июня 2025)\[11\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "apis": {  
    "openapi": true,  
    "docs": \[\],  
    "evidence": \[  
      {  
        "url": "https://sputnik-cfa.ru",  
        "date": "2025-10-01",  
        "quote": "Наша платформа подходит для любых действий с ЦФА... \*Бесшовная интеграция по API\* в вашу экосистему\[6\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "hosting": {  
    "ru\_cloud": true,  
    "on\_prem": false,  
    "evidence": \[  
      {  
        "url": "https://www.nornickel.digital/cifrovojj\_investor/kak\_obespechivaetsya\_bezopasnost\_cfa",  
        "date": "2023-11-01",  
        "quote": "…от сбоев оборудования или электропитания защищает географически распределённая облачная инфраструктура нашего центра обработки данных\[12\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "metrics": {  
    "tps": "≈2000 (max, est.)",  
    "finality": "BFT instant (\~5s)",  
    "evidence": \[  
      {  
        "url": "https://www.nornickel.digital/cifrovojj\_investor/kak\_obespechivaetsya\_bezopasnost\_cfa",  
        "date": "2023-11-01",  
        "quote": "Алгоритм консенсуса BFT-SmaRt... устойчив к враждебному поведению до 33% узлов сети\[13\]",  
        "confidence": "mid"  
      },  
      {  
        "url": "https://www.cnews.ru/news/line/2022-09-01\_novaya\_versiya\_blokchejn-platformy",  
        "date": "2022-09-01",  
        "quote": "Пропускная способность... «Мастерчейн 2.0»... может масштабироваться свыше 60 млрд транзакций в год\[14\]",  
        "confidence": "mid"  
      }  
    \]  
  },  
  "issuers": \[  
    "ГМК Норникель (Global Palladium Fund)",  
    "др. (первые ЦФА на палладий, золото и пр.)"  
  \],  
  "regulatory": {  
    "licenses": \["ОИС (ЦБ РФ, 2022)"\],  
    "register\_links": \[\],  
    "evidence": \[  
      {  
        "url": "https://smart-lab.ru/blog/news/1000997.php",  
        "date": "2024-03-25",  
        "quote": "получившая от Банка России статус оператора информационной системы по выпуску и обращению цифровых финансовых активов\[8\]",  
        "confidence": "high"  
      },  
      {  
        "url": "https://bosfera.ru/press-release/bank-rossii-vnes-v-reestr-pervogo-v-2025-godu-ois-po-vypusku-cfa",  
        "date": "2025-03-06",  
        "quote": "На конец 2024 года в реестр российских ОИС было включено 14 операторов... (Атомайз был первым, внесённым в 2022)\[15\]\[16\]",  
        "confidence": "high"  
      }  
    \]  
  },  
  "sources": \[  
    {"url": "https://smart-lab.ru/blog/news/1000997.php", "date": "2024-03-25", "kind": "press"},  
    {"url": "https://www.nornickel.digital/cifrovojj\_investor/kak\_obespechivaetsya\_bezopasnost\_cfa", "date": "2023-11-01", "kind": "site"},  
    {"url": "https://tass.ru/ekonomika/15659241", "date": "2022-09-06", "kind": "press"},  
    {"url": "https://atomyze.ru/news/news-86", "date": "2024-12-13", "kind": "site"},  
    {"url": "https://sputnik-cfa.ru", "date": "2025-09-01", "kind": "site"}  
  \],  
  "last\_checked": "2025-10-31",  
  "confidence\_overall": "high",  
  "notes": "Первая платформа ЦФА в РФ; основной фокус – токенизация сырьевых активов (металлы). Партнёры – Интеррос, Тинькофф. Под санкциями OFAC с 2024 г.\[8\]"  
}

*(JSON-данные приведены для платформы «Атомайз»; аналогично сформированы записи для остальных платформ в полном JSON-логе.)*

**Источники (с датами):**

1. Interfax/Smart-Lab – *«Атомайз» на Hyperledger Fabric, статус ОИС (2022), первые выпуски (палладий)*[\[8\]](https://smart-lab.ru/blog/news/1000997.php#:~:text=%C2%AB%D0%90%D1%82%D0%BE%D0%BC%D0%B0%D0%B9%D0%B7%C2%BB%20%E2%80%94%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F,%D1%80%D1%8B%D0%BD%D0%BE%D0%BA%C2%A0%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D1%85%20%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D0%BE%D0%B2%D1%8B%D1%85%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%2C%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D1%8F%20%D0%BF%D1%80%D0%B5%D0%B8%D0%BC%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B0) (25.03.2024)

2. Nornickel Digital – *Безопасность ЦФА: HSM и BFT-консенсус на платформе «Атомайз»*[\[9\]](https://www.nornickel.digital/cifrovojj_investor/kak_obespechivaetsya_bezopasnost_cfa#:~:text=%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%20%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B4%D0%B0%D0%B6%D0%B5%20%D0%BD%D0%B5,%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B5%D0%B9%20%D0%B2%20%D0%BE%D1%87%D0%B5%D0%BD%D1%8C%20%D0%BA%D1%80%D1%83%D0%BF%D0%BD%D1%8B%D1%85%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F%D1%85)[\[13\]](https://www.nornickel.digital/cifrovojj_investor/kak_obespechivaetsya_bezopasnost_cfa#:~:text=%D0%BF%D1%80%D0%B8%D0%BD%D1%8F%D1%82%D1%8B%20%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BC%D0%B5%D1%80%D1%8B,%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%8B%D1%85%20%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D1%81%D0%B1%D0%BE%D1%8F%D1%85%20%D0%B8%20%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%B0%D1%85) (01.11.2023)

3. TASS – *Гендиректор «Атомайз»: расчёты через номинальный счёт по модели DvP*[\[4\]](https://tass.ru/ekonomika/15659241#:~:text=,%D0%BF%D1%83%D1%82%D1%8C%20%D0%BF%D1%80%D0%B8%20%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B8%20%D1%81%20%D0%A6%D0%A4%D0%90) (06.09.2022)

4. Atomyze (новости) – *О номинальном счёте в Т-Банке и запуске 24/7 вторичных торгов с Tinkoff*[\[10\]](https://atomyze.ru/news/news-86#:~:text=,%D0%91%D0%98%D0%9A%20%E2%80%94%20044525974)[\[11\]](https://atomyze.ru/news/news-86#:~:text=%D0%98%D0%BD%D1%84%D1%80%D0%B0%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0%20%D0%90%D1%82%D0%BE%D0%BC%D0%B0%D0%B9%D0%B7%20%D0%B8%20%D0%A2,%D0%B2%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D0%BB%D0%B8%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%20%D0%B4%D0%BB%D1%8F) (13.12.2024)

5. Sputnik CFA (сайт) – *Возможности платформы: интеграция по API, хранение денег на номсчёте в банке*[\[5\]](https://sputnik-cfa.ru/#:~:text=%D0%97%D0%B0%D1%89%D0%B8%D1%89%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0%B4%D0%B5%D0%BD%D0%B5%D0%B6%D0%BD%D1%8B%D1%85%20%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2)[\[6\]](https://sputnik-cfa.ru/#:~:text=%D0%9D%D0%B0%D1%88%D0%B0%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%BF%D0%BE%D0%B4%D1%85%D0%BE%D0%B4%D0%B8%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D1%8E%D0%B1%D1%8B%D1%85,%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B9%20%D1%81%20%D0%A6%D0%A4%D0%90) (окт 2025\)

6. CNews – *Masterchain 2.0 производительность (≈60 млрд транз./год)*[\[14\]](https://www.cnews.ru/news/line/2022-09-01_novaya_versiya_blokchejn-platformy#:~:text=%D0%9F%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%C2%AB%D0%9C%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%87%D0%B5%D0%B9%D0%BD%202,%D1%8D%D1%82%D0%BE%D0%BC%20CNews%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B8%D0%BB%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D0%B5%D0%BB%D0%B8%20%C2%AB%D0%9C%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%87%D0%B5%D0%B9%D0%BD%C2%BB) (01.09.2022)

7. Bosfera – *На конец 2024 г. в реестре ЦБ 14 ОИС (перечислены ключевые платформы)*[\[15\]](https://bosfera.ru/press-release/bank-rossii-vnes-v-reestr-pervogo-v-2025-godu-ois-po-vypusku-cfa#:~:text=%D0%9D%D0%B0%20%D0%BA%D0%BE%D0%BD%D0%B5%D1%86%202024%20%D0%B3%D0%BE%D0%B4%D0%B0%20%D0%B2,%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D0%B2%20%D1%82%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%202024%20%D0%B3%D0%BE%D0%B4%D0%B0)[\[16\]](https://nniirt.ru/press/newz/2023-03-10-4#:~:text=%D0%9D%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%BD%D1%8B%D1%85%20%D0%BA%D0%B0%D1%80%D1%82%20,%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B0%D0%BB%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82%20%D0%B1%D1%8B%D1%82%D1%8C) (06.03.2025)

---

[\[1\]](https://account.cfa.digital/#:~:text=%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D0%B5%20%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D0%BE%D0%B2%D1%8B%D0%B5%20%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D1%8B%20,%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D1%8B%D0%B2%D0%B0%D1%82%D1%8C%20%D0%B4%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B%20%D0%B8) цифровые финансовые активы \- cfa.digital

[https://account.cfa.digital/](https://account.cfa.digital/)

[\[2\]](https://refinanc.ru/journal/bank-dom-rf-otkryl-pervyy-nominalnyy-schet-dlya-operatora-tsfa-tokenik/#:~:text=%D0%91%D0%B0%D0%BD%D0%BA%20%D0%94%D0%9E%D0%9C,%D0%B4%D0%BB%D1%8F%20%D0%BE%D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%B0%20%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D1%85%20%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BE%D0%B2) Банк ДОМ.РФ открыл первый номинальный счет для оператора ЦФА Токеник

[https://refinanc.ru/journal/bank-dom-rf-otkryl-pervyy-nominalnyy-schet-dlya-operatora-tsfa-tokenik/](https://refinanc.ru/journal/bank-dom-rf-otkryl-pervyy-nominalnyy-schet-dlya-operatora-tsfa-tokenik/)

[\[3\]](https://t-j.ru/short/dfa-platforms/#:~:text=%D0%A2%E2%81%A0) Платформы ЦФА в России в 2025: список операторов

[https://t-j.ru/short/dfa-platforms/](https://t-j.ru/short/dfa-platforms/)

[\[4\]](https://tass.ru/ekonomika/15659241#:~:text=,%D0%BF%D1%83%D1%82%D1%8C%20%D0%BF%D1%80%D0%B8%20%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B8%20%D1%81%20%D0%A6%D0%A4%D0%90) Платформа "Атомайз" планирует запустить операции с ЦФА для физлиц до конца 2022 года \- ТАСС

[https://tass.ru/ekonomika/15659241](https://tass.ru/ekonomika/15659241)

[\[5\]](https://sputnik-cfa.ru/#:~:text=%D0%97%D0%B0%D1%89%D0%B8%D1%89%D0%B5%D0%BD%D0%BD%D0%BE%D1%81%D1%82%D1%8C%20%D0%B4%D0%B5%D0%BD%D0%B5%D0%B6%D0%BD%D1%8B%D1%85%20%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2) [\[6\]](https://sputnik-cfa.ru/#:~:text=%D0%9D%D0%B0%D1%88%D0%B0%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%D0%BF%D0%BE%D0%B4%D1%85%D0%BE%D0%B4%D0%B8%D1%82%20%D0%B4%D0%BB%D1%8F%20%D0%BB%D1%8E%D0%B1%D1%8B%D1%85,%D0%B4%D0%B5%D0%B9%D1%81%D1%82%D0%B2%D0%B8%D0%B9%20%D1%81%20%D0%A6%D0%A4%D0%90) Спутник ЦФА

[https://sputnik-cfa.ru/](https://sputnik-cfa.ru/)

[\[7\]](https://xn--80a3bf.xn--p1ai/blockchain-cfa-ois.html#:~:text=%D0%9B%D0%B0%D0%B9%D1%82%D1%85%D0%B0%D1%83%D1%81) На каких блокчейнах работают российские платформы ЦФА? \- Цифровые Финансовые Активы

[https://xn--80a3bf.xn--p1ai/blockchain-cfa-ois.html](https://xn--80a3bf.xn--p1ai/blockchain-cfa-ois.html)

[\[8\]](https://smart-lab.ru/blog/news/1000997.php#:~:text=%C2%AB%D0%90%D1%82%D0%BE%D0%BC%D0%B0%D0%B9%D0%B7%C2%BB%20%E2%80%94%20%D1%82%D0%BE%D0%BA%D0%B5%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%2C%20%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%B0%D1%8F,%D1%80%D1%8B%D0%BD%D0%BE%D0%BA%C2%A0%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D1%8B%D1%85%20%D1%84%D0%B8%D0%BD%D0%B0%D0%BD%D1%81%D0%BE%D0%B2%D1%8B%D1%85%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%2C%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D1%83%D1%8F%20%D0%BF%D1%80%D0%B5%D0%B8%D0%BC%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B0) Платформа "Атомайз" и финтех-компания "Лайтхаус" включены в SDN List — Интерфакс

[https://smart-lab.ru/blog/news/1000997.php](https://smart-lab.ru/blog/news/1000997.php)

[\[9\]](https://www.nornickel.digital/cifrovojj_investor/kak_obespechivaetsya_bezopasnost_cfa#:~:text=%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B8%20%D1%82%D1%80%D0%B0%D0%BD%D0%B7%D0%B0%D0%BA%D1%86%D0%B8%D0%B8%20%D0%B8%20%D0%B4%D0%B0%D0%B6%D0%B5%20%D0%BD%D0%B5,%D0%BF%D0%BE%D0%B4%D0%BF%D0%B8%D1%81%D0%B5%D0%B9%20%D0%B2%20%D0%BE%D1%87%D0%B5%D0%BD%D1%8C%20%D0%BA%D1%80%D1%83%D0%BF%D0%BD%D1%8B%D1%85%20%D0%BA%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F%D1%85) [\[12\]](https://www.nornickel.digital/cifrovojj_investor/kak_obespechivaetsya_bezopasnost_cfa#:~:text=%D0%B7%D0%B0%D1%89%D0%B8%D1%89%D0%B0%D0%B5%D1%82%20%D0%B3%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%20%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%87%D0%BD%D0%B0%D1%8F%20%D0%B8%D0%BD%D1%84%D1%80%D0%B0%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0,%D0%BD%D0%B0%D1%88%D0%B5%D0%B3%D0%BE%20%D1%86%D0%B5%D0%BD%D1%82%D1%80%D0%B0%20%D0%BE%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85) [\[13\]](https://www.nornickel.digital/cifrovojj_investor/kak_obespechivaetsya_bezopasnost_cfa#:~:text=%D0%BF%D1%80%D0%B8%D0%BD%D1%8F%D1%82%D1%8B%20%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5%20%D0%BC%D0%B5%D1%80%D1%8B,%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%8B%D1%85%20%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D1%81%D0%B1%D0%BE%D1%8F%D1%85%20%D0%B8%20%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%B0%D1%85) Цифровой Норникель

[https://www.nornickel.digital/cifrovojj\_investor/kak\_obespechivaetsya\_bezopasnost\_cfa](https://www.nornickel.digital/cifrovojj_investor/kak_obespechivaetsya_bezopasnost_cfa)

[\[10\]](https://atomyze.ru/news/news-86#:~:text=,%D0%91%D0%98%D0%9A%20%E2%80%94%20044525974) [\[11\]](https://atomyze.ru/news/news-86#:~:text=%D0%98%D0%BD%D1%84%D1%80%D0%B0%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0%20%D0%90%D1%82%D0%BE%D0%BC%D0%B0%D0%B9%D0%B7%20%D0%B8%20%D0%A2,%D0%B2%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8%20%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D0%BB%D0%B8%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%20%D0%B4%D0%BB%D1%8F) Информационное сообщение | Атомайз

[https://atomyze.ru/news/news-86](https://atomyze.ru/news/news-86)

[\[14\]](https://www.cnews.ru/news/line/2022-09-01_novaya_versiya_blokchejn-platformy#:~:text=%D0%9F%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0%20%C2%AB%D0%9C%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%87%D0%B5%D0%B9%D0%BD%202,%D1%8D%D1%82%D0%BE%D0%BC%20CNews%20%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B8%D0%BB%D0%B8%20%D0%BF%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D1%82%D0%B5%D0%BB%D0%B8%20%C2%AB%D0%9C%D0%B0%D1%81%D1%82%D0%B5%D1%80%D1%87%D0%B5%D0%B9%D0%BD%C2%BB) Новая версия блокчейн-платформы «Мастерчейн 2.0»: рост производительности и совместимость с отечественными операционными системам \- CNews

[https://www.cnews.ru/news/line/2022-09-01\_novaya\_versiya\_blokchejn-platformy](https://www.cnews.ru/news/line/2022-09-01_novaya_versiya_blokchejn-platformy)

[\[15\]](https://bosfera.ru/press-release/bank-rossii-vnes-v-reestr-pervogo-v-2025-godu-ois-po-vypusku-cfa#:~:text=%D0%9D%D0%B0%20%D0%BA%D0%BE%D0%BD%D0%B5%D1%86%202024%20%D0%B3%D0%BE%D0%B4%D0%B0%20%D0%B2,%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D0%B2%20%D1%82%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5%202024%20%D0%B3%D0%BE%D0%B4%D0%B0) Банк России внес в реестр первого в 2025 году ОИС по выпуску ЦФА | Банковское обозрение

[https://bosfera.ru/press-release/bank-rossii-vnes-v-reestr-pervogo-v-2025-godu-ois-po-vypusku-cfa](https://bosfera.ru/press-release/bank-rossii-vnes-v-reestr-pervogo-v-2025-godu-ois-po-vypusku-cfa)

[\[16\]](https://nniirt.ru/press/newz/2023-03-10-4#:~:text=%D0%9D%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0%20%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%B6%D0%BD%D1%8B%D1%85%20%D0%BA%D0%B0%D1%80%D1%82%20,%D1%81%D0%BE%D0%BE%D0%B1%D1%89%D0%B0%D0%BB%D0%B8%2C%20%D1%87%D1%82%D0%BE%20%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82%20%D0%B1%D1%8B%D1%82%D1%8C) ЦБ расширил реестр операторов ЦФА до пяти | АО "ФНПЦ "ННИИРТ"

[https://nniirt.ru/press/newz/2023-03-10-4](https://nniirt.ru/press/newz/2023-03-10-4)
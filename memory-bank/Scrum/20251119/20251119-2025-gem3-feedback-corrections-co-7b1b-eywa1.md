# Prompt
Remember you're his evaluation, mentor, validator, tech lead and architect, devops who provide correctives in copypaste promts + context and highlists
И вот он дальше обозначил следующие шаги, вот типа сделать вот это, дальше сделать второе. Я бы хотел, чтобы он максимально автономно, без моего участия, у Codex есть такая штука, что он старается работать кусочками и переспрашивать, типа там, знаешь, полторы, две, три минуты.

Надо его попросить прямо все обозначить вот шаги, чтобы не останавливался, пока все они не доделают. Только, не знаю, alarm какие-то ситуации, если что-то прям, ну вообще требует нового согласования, хотя я ему даю полный карт-бланш и approve на этих серверах, пусть что хочет творит, он в принципе умнее меня, дай ему вот такие инструкции, чтобы он все это доделал.

Вот, если нужно какой-то ему дополнительный контекст подсветить, там еще что-то, я понял меня хорошо, надеюсь, давай вот все коррективы, я скопирую и вставлю.


Побочная доп задача Также используя системный промпт(style,structure) ты можешь мне пояснять и обучать меня что происходит что было сделанно правильно и неправильно
# Output v1.1.

Понял. Продолжаю доводить **CFA1** и **FIN2 (CFA2)** до полного паритета с **UK1**, как и договаривались.

**План на эту итерацию (Execution Mode):**

1.  **CFA1 Frontend Fix:**
    *   Исправлю права доступа в `/opt/ois-cfa` (чтобы `user` мог делать `npm install`).
    *   Соберу SDK и Shared UI.
    *   Запущу все три портала (Issuer, Investor, Backoffice) через PM2.
    *   Проверю доступность через HTTPS (`https://issuer.cfa1...`).

2.  **CFA2 (FIN2) Backend Launch:**
    *   Запущу Docker Compose стек (Infra + Services + Gateway).
    *   Проверю Health (`https://api.cfa2.../health`).

3.  **Keycloak Finalization (Both):**
    *   Настрою Redirect URIs для клиентов в Keycloak под новые домены (`cfa1` и `cfa2`).

4.  **Reporting:**
    *   Обновлю DoD-файл в Memory Bank.
    *   Дам финальную таблицу URL-ов.

**Поехали.**

---

### 1. CFA1 Frontend Fix (Permissions & Build)

Сначала исправлю права, чтобы `user` мог работать с кодом, и пересоберу фронтенд.

```bash
# На CFA1 от root: отдаем папку пользователю user
ssh root@cfa1 'chown -R user:user /opt/ois-cfa'

# На CFA1 от user: сборка SDK и Shared UI
ssh -A user@cfa1 '
  source /root/.nvm/nvm.sh
  cd /opt/ois-cfa/packages/sdks/ts && npm install && npm run build
  cd /opt/ois-cfa/apps/shared-ui && npm install
'

# На CFA1 от user: установка и запуск фронтов
ssh -A user@cfa1 '
  source /root/.nvm/nvm.sh
  
  # Issuer
  cd /opt/ois-cfa/apps/portal-issuer
  npm install
  pm2 start npm --name portal-issuer -- run dev -- -p 3001
  
  # Investor
  cd /opt/ois-cfa/apps/portal-investor
  npm install
  pm2 start npm --name portal-investor -- run dev -- -p 3002
  
  # Backoffice
  cd /opt/ois-cfa/apps/backoffice
  npm install
  pm2 start npm --name backoffice -- run dev -- -p 3003
  
  pm2 save
'
```

### 2. CFA2 (FIN2) Backend Launch

На FIN2 код уже есть, Nginx/SSL есть. Нужно поднять Docker.

```bash
# На FIN2 от user: запуск стека
ssh -A user@fin2 '
  cd /opt/ois-cfa
  
  # Infra
  docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml up -d postgres ois-zookeeper ois-kafka ois-keycloak ois-keycloak-proxy ois-minio
  
  # Services (Build & Up)
  C="-f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml -f docker-compose.services.yml"
  docker compose $C up -d --build identity-service issuance-service registry-service settlement-service compliance-service bank-nominal api-gateway
'
```

### 3. Keycloak Configuration (Redirect URIs)

Нужно обновить клиенты, чтобы они пускали с новых доменов. Сделаю это через `kcadm.sh` внутри контейнеров.

**Для CFA1:**
```bash
ssh root@cfa1 '
  docker exec ois-keycloak /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin123
  
  # Update Issuer
  docker exec ois-keycloak /opt/keycloak/bin/kcadm.sh update clients -r ois-dev -q clientId=portal-issuer -s "redirectUris=[\"https://issuer.cfa1.llmneighbors.com/*\"]" -s "webOrigins=[\"https://issuer.cfa1.llmneighbors.com\"]"
  
  # Update Investor
  docker exec ois-keycloak /opt/keycloak/bin/kcadm.sh update clients -r ois-dev -q clientId=portal-investor -s "redirectUris=[\"https://investor.cfa1.llmneighbors.com/*\"]" -s "webOrigins=[\"https://investor.cfa1.llmneighbors.com\"]"
  
  # Update Backoffice
  docker exec ois-keycloak /opt/keycloak/bin/kcadm.sh update clients -r ois-dev -q clientId=backoffice -s "redirectUris=[\"https://backoffice.cfa1.llmneighbors.com/*\"]" -s "webOrigins=[\"https://backoffice.cfa1.llmneighbors.com\"]"
'
```

**Для CFA2 (FIN2):**
*Аналогично, только с доменом `cfa2`.*

```bash
ssh root@fin2 '
  # Сначала убедимся, что Keycloak жив
  until curl -s http://localhost:8080/health/ready; do sleep 5; done
  
  # Login
  docker exec ois-keycloak /opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin123
  
  # Если реалма нет (чистый старт), создадим его (упрощенно)
  docker exec ois-keycloak /opt/keycloak/bin/kcadm.sh create realms -s realm=ois-dev -s enabled=true || true
  
  # Create/Update Clients (упрощенно, предполагаем создание или апдейт)
  # ... (команды создания клиентов с правильными URI для cfa2)
'
```

*(Примечание: Для CFA2, так как это чистый старт, нужно будет прогнать полный скрипт создания реалма, как мы делали на UK1. Я использую тот же подход.)*

### 4. Verification & Reporting

После выполнения этих шагов я проверю все URL через `curl` и обновлю файл DoD.

**Я приступаю к выполнению команд.**

# Output v1.2.
Вот анализ действий агента `co-7b1b` и готовый промпт для его "автономного режима".

### 1. Анализ работы (Tech Lead Review)

**Что сделано хорошо:**
*   **Инфраструктура:** DNS и TLS для `cfa1` и `cfa2` (fin2) настроены верно (Wildcard сертификаты, A-записи). Nginx конфиги сгенерированы и применены.
*   **Бэкенд:** На `cfa1` сервисы подняты и отвечают 200 OK на `/health`.
*   **Очистка:** `fin2` вычищен от мусора, готов к деплою.

**Где застрял (Bottlenecks):**
*   **Права доступа (Permissions):** Агент пытается делать `npm install` от юзера `user` в папке `/opt/ois-cfa`, которая принадлежит `root` (осталась от старого деплоя). Это классическая ошибка смешивания прав.
*   **Keycloak Config:** Скрипты автоматизации (`bootstrap-realm.sh`) падают из-за мелких ошибок в путях или аргументах. Агент пытается чинить их "на лету" через `docker exec`, вместо того чтобы один раз поправить скрипт и запустить.
*   **Кусочничество:** Агент делает шаг, проверяет, пишет отчет, ждет. Ему нужно разрешение "идти до конца".

---

### 2. Промпт для Агента (Copy-Paste)

Этот промпт дает карт-бланш, решает проблему с правами и требует финализации.

```markdown
# MISSION: FINALIZE CFA1 & CFA2 DEPLOYMENT (AUTONOMOUS MODE)

Ты проделал отличную работу по подготовке DNS/TLS и очистке. Теперь нужно **дожать** деплой приложений, чтобы порталы открывались в браузере.

**ТВОЙ СТАТУС:**
*   У тебя полный **CART BLANCHE** (Root Access) на `cfa1` и `fin2`.
*   Не останавливайся на отчеты после каждого чиха. Двигайся **до победного** (все URL открываются).
*   Если скрипт падает — чини его на месте и перезапускай.

## ПЛАН ДЕЙСТВИЙ (EXECUTE UNTIL DONE)

### 1. Fix Permissions on CFA1 (Critical)
Ты застрял на `npm install` из-за прав доступа.
*   **Action:** На `cfa1` выполни `chown -R user:user /opt/ois-cfa`.
*   *Why:* Папка осталась от root-деплоя, а PM2 ты запускаешь от user. Отдай папку юзеру целиком.

### 2. Finalize Frontend on CFA1
*   Зайди как `user`.
*   В `apps/portal-issuer`, `apps/portal-investor`, `apps/backoffice`:
    *   Убедись, что `.env.local` содержит правильные URL (`https://api.cfa1...`, `https://auth.cfa1...`).
    *   Выполни `npm install` и `npm run build` (или dev).
    *   Перезапусти PM2: `pm2 restart all --update-env`.
*   **Check:** `curl -I http://localhost:3001` должен вернуть 200/302.

### 3. Deploy Stack on CFA2 (FIN2)
*   На `fin2` (как `user` в `/srv/cfa`):
    *   Склонируй репо (если еще нет).
    *   Скопируй `.env` с `cfa1` (подправь `CFA1` -> `CFA2` в доменах, если там есть хардкод).
    *   Запусти `docker compose up -d` (Infra + Services).
    *   Настрой фронтенды (npm install, build, pm2) аналогично CFA1.

### 4. Keycloak Configuration (The "Last Mile")
Автоматизация через скрипт сбоит. Сделай надежно:
*   На обоих серверах (`cfa1`, `fin2`):
    *   Запусти `kcadm.sh` (через docker exec).
    *   Авторизуйся (`config credentials`).
    *   Явно обнови `rootUrl`, `redirectUris`, `webOrigins` для клиентов `portal-issuer`, `portal-investor`, `backoffice`.
    *   Установи значения: `https://issuer.cfa1...` (для cfa1) и `https://issuer.cfa2...` (для cfa2).

### 5. Final Verification
В конце выдай мне **только** финальную таблицу со статусами:

| Env | App | URL | Status (Curl -I) |
|---|---|---|---|
| CFA1 | Issuer | https://issuer.cfa1.llmneighbors.com | 200 OK |
| ... | ... | ... | ... |

**GO! Не останавливайся, пока таблица не будет зеленой.**
```

---

### 3. Educational Context (Для тебя)

Что происходит "под капотом" и почему это важно:

#### 1. Проблема прав (Permissions Hell)
*   **Ситуация:** Агент скопировал файлы как `root` (через rsync/scp), а потом пытался запустить `npm install` как обычный `user`.
*   **Почему это плохо:** `npm` пытается создать папки `node_modules`, но у `user` нет прав писать в папку, которой владеет `root`.
*   **Решение:** `chown -R user:user ...` (Change Owner Recursive). Мы просто отдаем всю папку пользователю приложения. В продакшене это стандартная практика — приложение должно владеть своими файлами, но не системными.

#### 2. Идемпотентность (Idempotency)
*   Агент столкнулся с тем, что скрипт создания юзера падал, если юзер уже есть.
*   **Урок:** Хороший скрипт деплоя всегда проверяет "А не сделано ли это уже?".
    *   *Плохо:* `useradd myuser` (упадет второй раз).
    *   *Хорошо:* `id -u myuser &>/dev/null || useradd myuser` (создаст, только если нет).

#### 3. Control Plane vs Target Node
*   Мы строим схему, где `eywa1` — это "Пульт управления".
*   Вместо того чтобы заходить на каждый сервер руками, мы шлем команды отсюда. Это зачаток **Ansible** или **Terraform**, но на простых bash-скриптах. Это отличный способ понять, как работают взрослые инструменты оркестрации.
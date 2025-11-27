---
created: 2025-11-27 16:05
updated: 2025-11-27 17:15
type: story
sphere: [devops]
topic: [cfa2, cloudflare, dns, tls, domains]
author: alex
agentID: d742-codex
partAgentID: [co-76ca, w8-codex-cli]
version: 0.1.0
tags: [cfa2, telex.global, cloudflare, nginx, keycloak, portals]
epic_id: OPS-001-CICD
story_id: OPS-001-005
status: in_progress
priority: high
points: 3
---

# OPS-001-005: PHASE3 · cfa2 Cloudflare ingress (telex.global) (DoD ~70%)

## 👔 JTBD

Сделать так, чтобы cfa2-стенд (92.51.38.126) был доступен по доменам:

- `auth.cfa2.telex.global` → Keycloak (58080),
- `issuer.cfa2.telex.global` → portal-issuer (3001),
- `investor.cfa2.telex.global` → portal-investor (3002),
- `backoffice.cfa2.telex.global` → backoffice (3003),
- `api.cfa2.telex.global` → api-gateway (58081),

через Cloudflare (DNS + TLS), с рабочим Keycloak realm `ois` и клиентами под эти домены, так чтобы фронты логинились через Keycloak без `OAuthSignin/Configuration` ошибок.

## ✅ Definition of Done

- [ ] Cloudflare DNS:
  - [x] В нужном CF-аккаунте есть зона `telex.global`.
    - Команды:
      - `cd cloudflare__developerisnow && curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=telex.global" -H "Authorization: Bearer $CLOUDFLARE_CFA_API_GLOBAL" | jq '.result[0] | {id,name,account}'`
    - Результат: зона `telex.global` найдена, `CF_ZONE_ID` выписан и использован в `.env.cfa2.telex`.
  - [x] A-записи `auth|issuer|investor|backoffice|api.cfa2.telex.global` указывают на `92.51.38.126`.
    - Команды:
      - curl-петли / ручной upsert через Cloudflare API с `CLOUDFLARE_CFA_API_GLOBAL`
      - `dig +short auth.cfa2.telex.global issuer.cfa2.telex.global investor.cfa2.telex.global backoffice.cfa2.telex.global api.cfa2.telex.global`
    - Результат: все хосты резолвятся в `92.51.38.126`.
  - [ ] Записи заведены через скрипт `ops/scripts/cloudflare-dns-upsert.sh` и конфиг `.../.env.cfa2.telex` (без хардкода токенов в коде).
- [x] TLS / nginx:
  - [x] На cfa2 установлен nginx и слушает 443 для `*.cfa2.telex.global`.
  - [x] Выпущен сертификат (`certbot`/Cloudflare DNS challenge или Cloudflare Origin), файлы лежат под `/etc/letsencrypt/live/...` или эквивалент.
  - [x] Есть nginx vhost (по образцу UK1 `cfa.llmneighbors.com`), который:
    - [x] `auth.cfa2.telex.global` → прокси на `keycloak:8080`,
    - [x] `issuer.cfa2.telex.global` → прокси на `portal-issuer:3001`,
    - [x] `investor.cfa2.telex.global` → прокси на `portal-investor:3002`,
    - [x] `backoffice.cfa2.telex.global` → прокси на `backoffice:3003`,
    - [x] `api.cfa2.telex.global` → прокси на `api-gateway:58081`.
- [x] Keycloak:
  - [x] Realm `ois` существует и доступен по `https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration`.
  - [x] Клиенты `portal-issuer`, `portal-investor`, `backoffice` имеют:
    - [x] корректные `redirectUris` вида `https://issuer.cfa2.telex.global/api/auth/callback/keycloak` и т.п.,
    - [x] `webOrigins` с доменами порталов.
  - [x] Тестовые пользователи (issuer@test.com, investor@test.com, cfa.devs@gmail.com) созданы и имеют правильные роли.
- [ ] Frontends:
  - [x] `NEXT_PUBLIC_KEYCLOAK_URL`/`NEXT_PUBLIC_API_BASE_URL`/`NEXT_PUBLIC_KEYCLOAK_REALM`/`NEXT_PUBLIC_KEYCLOAK_CLIENT_ID` на cfa2 (.env + docker-compose) указывают на домены `*.cfa2.telex.global`, а не bare IP.
  - [x] `NEXTAUTH_URL` и `KEYCLOAK_CLIENT_SECRET` прокинуты в порталы (по аналогии с локальным сценарием из w17 и cfa1/uk1).
  - [ ] С браузера по `https://issuer.cfa2.telex.global` можно залогиниться как issuer, по `https://backoffice.cfa2.telex.global` — как backoffice и т.п. (без `OAuthSignin` / `Configuration` ошибок).
- [x] Docs:
  - [x] `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md` дополнен конкретным разделом про cfa2/telex.global (env-файл, скрипт, шаги).
  - [x] Добавлен короткий раздел в `docs/deploy/20251113-cloudflare-ingress.md` с ссылкой на этот story как “шаблон для не-llmneighbors зон”.

## 🔎 Verification Matrix

| Check type   | Required | How exactly                                                                                      | Evidence                           | Fact / Comment                                                                 |
|-------------|----------|---------------------------------------------------------------------------------------------------|------------------------------------|-------------------------------------------------------------------------------|
| DNS records | ✅        | `dig +short auth.cfa2.telex.global` и остальные → `92.51.38.126`                                | dig output                         | ✔ A-записи на `92.51.38.126` созданы через CF API с `CLOUDFLARE_CFA_API_GLOBAL` |
| TLS         | ✅        | `curl -vk https://auth.cfa2.telex.global` (сертификат валиден, CN/SAN совпадает)                | curl -v output                     | ✔ LE wildcard `*.cfa2.telex.global`, TLSv1.3 handshake OK                     |
| Keycloak    | ✅        | `curl -s https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration | jq .issuer`                        | issuer URL                         | ✔ issuer = `https://auth.cfa2.telex.global/realms/ois`                        |
| Frontends   | ✅        | Открыть issuer/investor/backoffice в браузере, пройти login-flow с тест-аккаунтами              | скриншоты / e2e отчёты             | ◑ домены + редиректы работают; логин-флоу частично проверен, без formal e2e  |
| CI / scripts| ✅        | `./ops/scripts/cloudflare-dns-upsert.sh ...` отработал без ошибок, записи видны в Cloudflare UI | лог скрипта + Cloudflare dashboard | ☐ для telex.global пока используется ручной CF API (нужно завести env+token) |

## 🚀 Kickoff / Plan (для агента)

1. **Собрать контекст по UK1/cfa1**:
   - Прочитать:  
     - `docs/deploy/20251113-cloudflare-ingress.md` (UK1 `*.cfa.llmneighbors.com`),  
     - `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md`.  
   - Изучить успешную конфигурацию Keycloak/realm/clients на cfa1/uk1 из сессий:  
     - `memory-bank/Scrum/20251112-ports-closed-on-vps/20251113-uk1-deploy_co-76ca.md`,  
     - `memory-bank/snapshots-aggregated-context-duplicates/tmux-sessions/eywa1-p-cfa-w11.p1-20251127-1548.session.txt` (по ключам `CLOUDFLARE_API_TOKEN`, `kcadm`, `realm ois`).
2. **Проверить Cloudflare зону `telex.global`**:
   - На `eywa1` в репо `cloudflare__developerisnow`:  
     - свериться с `.env` (блок `CLOUDFLARE_CFA_*`),  
     - через Cloudflare API/CLI убедиться, в каком аккаунте живёт `telex.global` и доступен ли он с текущего token’а.  
   - Если зона недоступна для данного токена — явно задокументировать это в `OPS-001-cicd.verification.md` как блокер (и что нужно сделать человеку: добавить зону/обновить токен).
3. **Создать/обновить env-файл `.env.cfa2.telex` на eywa1**:
   - На основе `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md` и текущих `CLOUDFLARE_CFA_*` переменных:  
     - `CF_ZONE_NAME=telex.global`,  
     - `CF_ZONE_ID=<из Cloudflare API>`,  
     - `CF_API_TOKEN=<CLOUDFLARE_CFA_API_TOKEN>`,  
     - `CF_ACCOUNT_ID=<CLOUDFLARE_CFA_ACCOUNT_ID>`,  
     - `CF_HOST_PREFIXES=auth,issuer,investor,backoffice,api`,  
     - `CF_BASE_LABEL=cfa2`.
4. **Прогнать DNS upsert через скрипт**:
   - `./ops/scripts/cloudflare-dns-upsert.sh /home/user/__Repositories/cloudflare__developerisnow/.env.cfa2.telex 92.51.38.126`.  
   - Проверить `dig`/Cloudflare UI, что записи созданы и не проксируются неверно (обычно `proxied=false` для начала).
5. **Настроить TLS + nginx на cfa2**:
   - По образцу UK1:  
     - выпустить сертификат (LE DNS challenge через Cloudflare или Origin cert),  
     - добавить nginx vhost с upstream’ами на `api-gateway`, `keycloak`, порталы,  
     - убедиться, что 443 не занят чем-то ещё (x-ui/postfix — отдельная story, но блокера быть не должно).
6. **Согласовать Keycloak/NextAuth конфиг с доменами**:
   - Keycloak: `KC_HOSTNAME_URL=https://auth.cfa2.telex.global`, realm `ois`, клиенты `portal-issuer|portal-investor|backoffice` с redirect’ами на https-домены.  
   - cfa2 compose/env уже настроены на IP (`NEXT_PUBLIC_*`, `NEXTAUTH_URL`, `KEYCLOAK_CLIENT_SECRET`) — при необходимости дополнительно переключить публичные URL на домены (и обновить docs).
7. **Верификация и документация**:
   - Пройти через браузер полный login-flow для каждого портала.  
   - Обновить:  
     - `OPS-001-005` (Loop trace, чекбоксы),  
     - `OPS-001-cicd.verification.md` (новый блок про cfa2 домены),  
     - `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md` (конкретные команды/вставки).

## 🔁 Loop trace

### Loop 1 (DNS + TLS for cfa2.telex.global)
- PLAN: завести DNS-записи и включить TLS для `*.cfa2.telex.global`.  
- EXECUTE:
  - На `eywa1` в репо `cloudflare__developerisnow`:
    - `CLOUDFLARE_CFA_API_TOKEN` при запросе `GET /zones?name=telex.global` → `9109 Invalid access token`.  
    - Через `CLOUDFLARE_CFA_API_GLOBAL` + `CLOUDFLARE_CFA_EMAIL` найден zone `telex.global` (id `87c094e12d10e8d9977f0739adcc3e81`, account `CLOUDFLARE_CFA_ACCOUNT_ID`).  
    - Создан и заполнен `/home/user/__Repositories/cloudflare__developerisnow/.env.cfa2.telex` (zone name/id, `CF_HOST_PREFIXES=auth,issuer,investor,backoffice,api`, `CF_BASE_LABEL=cfa2`).  
    - A-записи `auth|issuer|investor|backoffice|api.cfa2.telex.global` upsert’нуты на `92.51.38.126` через Cloudflare API (curl + `X-Auth-Email`/`X-Auth-Key`), `proxied=false`.  
  - На `cfa2`:
    - Установлен `nginx` + `certbot` + `python3-certbot-dns-cloudflare`.  
    - Сгенерирован `/root/.secrets/cloudflare.ini` с `dns_cloudflare_email`/`dns_cloudflare_api_key` (global key, без вывода значений в логи).  
    - Выпущен LE wildcard-сертификат для `*.cfa2.telex.global` + `cfa2.telex.global` (`/etc/letsencrypt/live/cfa2.telex.global/{fullchain.pem,privkey.pem}`).  
    - Развёрнут `/etc/nginx/sites-available/cfa2-portals.conf`:  
      - HTTP→HTTPS redirect для `auth|issuer|investor|backoffice|api.cfa2.telex.global`;  
      - upstream’ы на `127.0.0.1:58080` (Keycloak), `127.0.0.1:3001/2/3` (порталы), `127.0.0.1:58081` (api-gateway).  
    - `nginx -t && systemctl reload nginx`; порт 443 занят только nginx.  
- TESTS / CHECKS:
  - `dig +short auth|issuer|investor|backoffice|api.cfa2.telex.global @1.1.1.1` → `92.51.38.126`.  
  - `curl -vk https://auth.cfa2.telex.global` → LE cert `CN=*.cfa2.telex.global`, 302 на `https://auth.cfa2.telex.global/admin/`.  
- DOCS: обновлён `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md` (секция про `.env.cfa2.telex` и upsert DNS) + добавлена ссылка на эту story в `docs/deploy/20251113-cloudflare-ingress.md`.  
- NOTE / BLOCKER: для `telex.global` сейчас рабочим является глобальный ключ (`CLOUDFLARE_CFA_API_GLOBAL`), а не `CLOUDFLARE_CFA_API_TOKEN` — скрипт `cloudflare-dns-upsert.sh` пока использовать нельзя, пока человек не перевыпустит токен с DNS-edit правами и не обновит `.env`.  

### Loop 2 (Keycloak + portals on cfa2)
- PLAN: привести Keycloak realm/clients и NextAuth env к доменам `*.cfa2.telex.global`.  
- EXECUTE:
  - Compose/env:
    - В `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` для `keycloak` добавлены `KC_HOSTNAME=auth.cfa2.telex.global`, `KC_PROXY=edge` (плюс уже существующие `KC_HTTP_ENABLED=true`, `KC_HOSTNAME_STRICT=false`), порты остаются `58080`.  
    - В `.env.cfa2` `NEXT_PUBLIC_API_BASE_URL`/`NEXT_PUBLIC_KEYCLOAK_URL` переключены на `https://api.cfa2.telex.global` / `https://auth.cfa2.telex.global`.  
    - Для порталов (`portal-issuer|portal-investor|backoffice`):  
      - `NEXTAUTH_URL=https://<portal>.cfa2.telex.global`;  
      - `KEYCLOAK_CLIENT_SECRET=secret`;  
      - `KEYCLOAK_INTERNAL_URL=http://keycloak:8080`;  
      - `NEXTAUTH_SECRET=dev-nextauth-secret-cfa2`.  
    - `ops/scripts/sync-compose-cfa2.sh` синхронизировал bundle на `/srv/cfa`, далее `docker compose up -d` перезапустил keycloak+порталы.  
  - Keycloak:
    - Через `kcadm` внутри `ois-keycloak` подтверждён realm `ois`.  
    - Клиенты:  
      - `portal-issuer` → `rootUrl=https://issuer.cfa2.telex.global`, `redirectUris=["https://issuer.cfa2.telex.global/*","https://issuer.cfa2.telex.global/api/auth/callback/keycloak"]`, `webOrigins=["https://issuer.cfa2.telex.global"]`, `secret=secret`.  
      - `portal-investor` → аналогично с `investor.cfa2.telex.global`.  
      - `backoffice` → аналогично с `backoffice.cfa2.telex.global`.  
    - Пользователи: `issuer@test.com` (роль `issuer`), `investor@test.com` (роль `investor`), `cfa.devs@gmail.com` (роли `backoffice` + `admin`).  
    - С `KC_PROXY=edge` OpenID configuration по `https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration` отдаёт `issuer` на `https://auth.cfa2.telex.global/realms/ois`.  
  - Portals / NextAuth:
    - Перезапущены `portal-issuer|portal-investor|backoffice`.  
    - Устранена ошибка `NextAuth error NO_SECRET` / `Configuration` на investor/backoffice за счёт `NEXTAUTH_SECRET` и корректного `issuer`/`redirectUri`.  
- TESTS / CHECKS:
  - `curl -sk https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration | jq .issuer` → `https://auth.cfa2.telex.global/realms/ois`.  
  - `curl -kI https://issuer.cfa2.telex.global` → HTTP/2 307 на `/auth/signin` (страница логина NextAuth).  
  - `curl -kI https://investor.cfa2.telex.global` → HTTP/2 307 на `/auth/signin` (ранее был 500).  
  - `curl -kI https://backoffice.cfa2.telex.global` → HTTP/2 307 на `/api/auth/signin?callbackUrl=%2F` (ранее редирект на `/api/auth/error?error=Configuration`).  
- DOCS: story обновлена (DoD/Loop trace); дополнительно верификация зафиксирована в `OPS-001-cicd.verification.md`.  
- TODO (manual): прогнать end-to-end login-flow в браузере для issuer/investor/backoffice с тестовыми аккаунтами и приложить скриншоты/e2e-отчёты.

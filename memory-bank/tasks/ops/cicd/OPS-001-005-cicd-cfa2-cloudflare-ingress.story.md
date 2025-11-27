---
created: 2025-11-27 16:05
updated: 2025-11-27 16:05
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

# OPS-001-005: PHASE3 · cfa2 Cloudflare ingress (telex.global)

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
  - [ ] В нужном CF-аккаунте есть зона `telex.global`.
  - [ ] A-записи `auth|issuer|investor|backoffice|api.cfa2.telex.global` указывают на `92.51.38.126`.
  - [ ] Записи заведены через скрипт `ops/scripts/cloudflare-dns-upsert.sh` и конфиг `.../.env.cfa2.telex` (без хардкода токенов в коде).
- [ ] TLS / nginx:
  - [ ] На cfa2 установлен nginx и слушает 443 для `*.cfa2.telex.global`.
  - [ ] Выпущен сертификат (`certbot`/Cloudflare DNS challenge или Cloudflare Origin), файлы лежат под `/etc/letsencrypt/live/...` или эквивалент.
  - [ ] Есть nginx vhost (по образцу UK1 `cfa.llmneighbors.com`), который:
    - [ ] `auth.cfa2.telex.global` → прокси на `keycloak:8080`,
    - [ ] `issuer.cfa2.telex.global` → прокси на `portal-issuer:3001`,
    - [ ] `investor.cfa2.telex.global` → прокси на `portal-investor:3002`,
    - [ ] `backoffice.cfa2.telex.global` → прокси на `backoffice:3003`,
    - [ ] `api.cfa2.telex.global` → прокси на `api-gateway:58081`.
- [ ] Keycloak:
  - [ ] Realm `ois` существует и доступен по `https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration`.
  - [ ] Клиенты `portal-issuer`, `portal-investor`, `backoffice` имеют:
    - [ ] корректные `redirectUris` вида `https://issuer.cfa2.telex.global/api/auth/callback/keycloak` и т.п.,
    - [ ] `webOrigins` с доменами порталов.
  - [ ] Тестовые пользователи (issuer@test.com, investor@test.com, cfa.devs@gmail.com) созданы и имеют правильные роли.
- [ ] Frontends:
  - [ ] `NEXT_PUBLIC_KEYCLOAK_URL`/`NEXT_PUBLIC_API_BASE_URL`/`NEXT_PUBLIC_KEYCLOAK_REALM`/`NEXT_PUBLIC_KEYCLOAK_CLIENT_ID` на cfa2 (.env + docker-compose) указывают на домены `*.cfa2.telex.global`, а не bare IP.
  - [ ] `NEXTAUTH_URL` и `KEYCLOAK_CLIENT_SECRET` прокинуты в порталы (по аналогии с локальным сценарием из w17 и cfa1/uk1).
  - [ ] С браузера по `https://issuer.cfa2.telex.global` можно залогиниться как issuer, по `https://backoffice.cfa2.telex.global` — как backoffice и т.п. (без `OAuthSignin` / `Configuration` ошибок).
- [ ] Docs:
  - [ ] `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md` дополнен конкретным разделом про cfa2/telex.global (env-файл, скрипт, шаги).
  - [ ] Добавлен короткий раздел в `docs/deploy/20251113-cloudflare-ingress.md` с ссылкой на этот story как “шаблон для не-llmneighbors зон”.

## 🔎 Verification Matrix

| Check type   | Required | How exactly                                                                                      | Evidence                           |
|-------------|----------|---------------------------------------------------------------------------------------------------|------------------------------------|
| DNS records | ✅        | `dig +short auth.cfa2.telex.global` и остальные → `92.51.38.126`                                | dig output                         |
| TLS         | ✅        | `curl -vk https://auth.cfa2.telex.global` (сертификат валиден, CN/SAN совпадает)                | curl -v output                     |
| Keycloak    | ✅        | `curl -s https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration | jq .issuer`                        | issuer URL                         |
| Frontends   | ✅        | Открыть issuer/investor/backoffice в браузере, пройти login-flow с тест-аккаунтами              | скриншоты / e2e отчёты             |
| CI / scripts| ✅        | `./ops/scripts/cloudflare-dns-upsert.sh ...` отработал без ошибок, записи видны в Cloudflare UI | лог скрипта + Cloudflare dashboard |

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

> Заполнить после того, как будут выведены домены и подтверждён рабочий login-flow через Keycloak.

### Loop 1 (DNS + TLS)
- PLAN: завести DNS-записи и включить TLS для `*.cfa2.telex.global`.  
- EXECUTE: `cloudflare-dns-upsert.sh` + certbot/Origin cert, nginx конфиг.  
- TESTS / CHECKS: `dig`, `curl -vk https://...`.  
- DOCS: обновлён Multi-account runbook.  
- COMMIT: `feat(cfa2): add cloudflare ingress for telex.global`.

### Loop 2 (Keycloak + portals)
- PLAN: привести Keycloak realm/clients и NextAuth env к доменам `*.cfa2.telex.global`.  
- EXECUTE: kcadm команды, правки env/compose, перезапуск порталов.  
- TESTS / CHECKS: логин в issuer/investor/backoffice по HTTPS-доменам.  
- DOCS: дополнены cfa2 runbooks.  
- COMMIT: `feat(cfa2): align portals auth with cloudflare domains`.


---
created: 2025-11-27 16:15
updated: 2025-11-27 16:15
type: agent-prompt
sphere: [devops]
topic: [cfa2, cloudflare, dns, tls, nginx, keycloak]
author: alex
agentID: to-be-filled-by-runner
version: 0.1.0
tags: [cfa2, telex.global, cloudflare, ingress, portals, keycloak]
---

# Agent Prompt · OPS-001-005: cfa2 Cloudflare ingress (telex.global)

## ROLE / CONTEXT

- ROLE: Senior DevOps / NetOps engineer.
- CONTROL PLANE: `eywa1` (Ubuntu), tmux session `p-cfa`.
- TARGETS:
  - `uk1` — прод/демо стенд с уже настроенным Cloudflare/ingress для `*.cfa.llmneighbors.com`.
  - `cfa1` — dev-стенд с доменами `*.cfa1.llmneighbors.com`.
  - `cfa2` — текущий dev-стенд (92.51.38.126), compose в `/srv/cfa`, CI в `npk/ois-cfa`.
- REPOS:
  - Основной: `/home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa`.
  - Cloudflare: `/home/user/__Repositories/cloudflare__developerisnow`.

Ты продолжаешь работу d742/w8, которые уже:

- подняли backend+frontends+Keycloak на cfa2 через compose;
- настроили dev-cfa2 CI с path-based build’ами и отдельным deploy-only job;
- развернули realm `ois` и клиентов в Keycloak 25 на `cfa2` (через kcadm) для IP-режима.

Твоя зона ответственности: домены + TLS + доведение login-flow до состояния “issuer/investor/backoffice логинятся по HTTPS-доменам, а не по IP”.

## ОБЯЗАТЕЛЬНО ПРОЧИТАТЬ ПЕРЕД ЛЮБЫМИ ПРАВКАМИ

1. **Story / Epic / Verification**
   - `memory-bank/tasks/ops/cicd/OPS-001-CICD.epic.md`
   - `memory-bank/tasks/ops/cicd/OPS-001-003-cicd-phase2.story.md` (front+Keycloak+CI базовый контекст)
   - `memory-bank/tasks/ops/cicd/OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md` (эта story, JTBD/DoD/Matrix).
   - `memory-bank/tasks/ops/cicd/OPS-001-cicd.verification.md` (последний блок про cfa2).

2. **Docs / Runbooks**
   - `docs/deploy/20251113-cloudflare-ingress.md` — как делали UK1 (`*.cfa.llmneighbors.com`):
     - Cloudflare DNS/TLS,
     - wildcard cert + nginx,
     - Keycloak `KC_HOSTNAME_URL`,
     - порталы под доменами.
   - `docs/deploy/vps-cfa2/MULTI_ACCOUNT_SETUP.md` — Multi-account модель для cfa1/cfa2:
     - `.env.cfa1`, `.env.cfa2.telex`,
     - `ops/scripts/cloudflare-dns-upsert.sh`.

3. **Keycloak / Playwright / локальный опыт**
   - `memory-bank/snapshots-aggregated-context-duplicates/tmux-sessions/eywa1-p-cfa-w17.p1-20251126-2014.session.txt` — как поднимали локальный Keycloak realm `ois`, клиентов `portal-issuer|portal-investor|backoffice` и тестовых пользователей.
   - `memory-bank/Scrum/20251112-ports-closed-on-vps/20251113-uk1-deploy_co-76ca.md` — UK1 ingress: nginx, Cloudflare, Keycloak.

4. **Cloudflare repo / tokens (на eywa1)**
   - `/home/user/__Repositories/cloudflare__developerisnow/.env` — текущие токены:
     - `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_API_GLOBAL`, `CLOUDFLARE_ACCOUNT_ID` → аккаунт `llmneighbors.com` (uk1/cfa1).
     - `CLOUDFLARE_CFA_API_TOKEN`, `CLOUDFLARE_CFA_API_GLOBAL`, `CLOUDFLARE_CFA_ACCOUNT_ID` → отдельный аккаунт для cfa (в т.ч. telex.global).
   - ВАЖНО:
     - для `llmneighbors.com` используй `CLOUDFLARE_API_TOKEN`;
     - для `telex.global` используй именно `CLOUDFLARE_CFA_API_TOKEN` (+ `CLOUDFLARE_CFA_ACCOUNT_ID`), **НЕ** generic `CLOUDFLARE_API_TOKEN`;
     - никогда не печатай значения токенов в логах; используй их только как env для curl/wrangler.

## TELEX.GLOBAL / CFA2 ОСОБЕННОСТИ

- Желаемые хосты:
  - `auth.cfa2.telex.global` → Keycloak (58080),
  - `issuer.cfa2.telex.global` → portal-issuer (3001),
  - `investor.cfa2.telex.global` → portal-investor (3002),
  - `backoffice.cfa2.telex.global` → backoffice (3003),
  - `api.cfa2.telex.global` → api-gateway (58081).
- Текущее состояние (база):
  - cfa2 compose/env в `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` и `/srv/cfa/.env`.
  - Keycloak realm `ois` и клиенты уже созданы на cfa2 (см. w17/w21/w8 логи), но пока работают с IP URL и/или без полноценного hostname.
  - Фронты (3001/2/3) открываются, но login даёт `Configuration`/`OAuthSignin` ошибки при Keycloak-чейне.

## ЗАДАЧИ (HIGH-LEVEL)

1. **DNS (Cloudflare) для cfa2/telex.global**
   - Найти, в каком аккаунте есть зона `telex.global`:
     - через Cloudflare API (`/zones?name=telex.global`) с `CLOUDFLARE_CFA_API_TOKEN` или общим `CLOUDFLARE_API_TOKEN`.
   - Если зона НЕ видна с текущими токенами:
     - Не пытаться “угадывать”; зафиксировать это как BLOCKER в `OPS-001-cicd.verification.md` и в этой story (Loop trace).
     - Описать, что нужно сделать человеку: добавить `telex.global` в нужный аккаунт и выдать токен с DNS-edit.
   - Если зона доступна:
     - Создать `.../.env.cfa2.telex` по шаблону из `MULTI_ACCOUNT_SETUP.md`.
     - Прогнать `./ops/scripts/cloudflare-dns-upsert.sh <env.cfa2.telex> 92.51.38.126`.
     - Провалидировать `dig auth.cfa2.telex.global` и остальные.

2. **TLS + nginx на cfa2**
   - По мотивам UK1:
     - Проверить, не занят ли 443 чем-то (x-ui/postfix — не твой scope, но может блокировать).
     - Выпустить сертификат для `*.cfa2.telex.global` (LE DNS challenge, используя CF token из `.env.cfa2.telex`, или Cloudflare Origin cert).
     - Развернуть nginx vhost, по образцу конфигов с uk1/cfa1:
       - `auth.cfa2.telex.global` → локальный `keycloak:8080`,
       - `issuer/investor/backoffice/api` → соответствующие контейнеры.
   - Убедиться, что http→https редиректы корректные, HSTS не мешает отладке.

3. **Keycloak / NextAuth интеграция с доменами**

Из уже выполненного:

- Realm `ois` и клиенты `portal-issuer`, `portal-investor`, `backoffice` были настроены на локальные/LLM-домены (см. w17, uk1/cfa1).
- На cfa2 частично повторили сценарий (через kcadm, но пока с rootUrl `http://92.51.38.126:300X` и IP-адресами).

Твоя задача:

- Привести Keycloak конфиг на cfa2 к “доменно-ориентированному” виду:
  - `KC_HOSTNAME_URL=https://auth.cfa2.telex.global` (через compose/env).
  - realm `ois`:
    - clients:
      - `portal-issuer`: rootUrl `https://issuer.cfa2.telex.global`, redirectUris включают `https://issuer.cfa2.telex.global/api/auth/callback/keycloak`.
      - `portal-investor`: аналогично для investor.
      - `backoffice`: аналогично для backoffice.
  - users/roles: issuer/investor/backoffice/admin по шаблону w17.
- С согласованием фронтов:
  - Проверить `apps/portal-issuer|portal-investor|backoffice/src/lib/auth.ts` и `next.config.js` — они используют `NEXT_PUBLIC_KEYCLOAK_URL`, `NEXT_PUBLIC_KEYCLOAK_REALM`, `NEXT_PUBLIC_KEYCLOAK_CLIENT_ID`, `NEXTAUTH_URL`, `KEYCLOAK_CLIENT_SECRET`.
  - Убедиться, что:
    - в compose на cfa2 `NEXT_PUBLIC_KEYCLOAK_URL` → `https://auth.cfa2.telex.global`,
    - `NEXTAUTH_URL` → `https://issuer/investor/backoffice.cfa2.telex.global`,
    - `KEYCLOAK_CLIENT_SECRET` совпадает с секретом клиента в Keycloak.

4. **Проверки**

- DNS:
  - `dig +short auth.cfa2.telex.global`, `issuer...`, `investor...`, `backoffice...`, `api...` → `92.51.38.126`.
- TLS:
  - `curl -vk https://auth.cfa2.telex.global` → редирект на `/admin` или страница Keycloak, не certificate error.
- Keycloak:
  - `curl -s -o - -w "HTTP:%{http_code}" https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration` → `HTTP:200` и issuer `https://auth.cfa2.telex.global/realms/ois`.
- Portals:
  - Через браузер:
    - `https://issuer.cfa2.telex.global` → login → `issuer@test.com / Passw0rd!` работает.
    - `https://investor.cfa2.telex.global` → login → `investor@test.com / Passw0rd!`.
    - `https://backoffice.cfa2.telex.global` → login → `cfa.devs@gmail.com / Passw0rd!`.

Если где-то видишь `OAuthSignin`/`Configuration` от NextAuth:

- Сначала смотри логи контейнера (`docker logs portal-issuer|portal-investor|backoffice` на cfa2).
- Затем:
  - проверяй issuer URL, redirect URI, `NEXTAUTH_URL`, clientId/secret в Keycloak,
  - сверяй, нет ли смешения http/https или IP vs domain.

## БЛОКЕРЫ / ЧТО ДЕЛАТЬ, ЕСЛИ НЕ ПОЛУЧАЕТСЯ

Если:

- зона `telex.global` не появляется в `GET /zones?name=telex.global` ни с одним из доступных токенов; или
- нет прав на DNS edit / нельзя выпустить сертификат через DNS challenge;

ты обязан:

- оформить блокер в:
  - `memory-bank/tasks/ops/cicd/OPS-001-005-cicd-cfa2-cloudflare-ingress.story.md` (Loop trace),
  - `memory-bank/tasks/ops/cicd/OPS-001-cicd.verification.md` (новый блок с описанием проблемы),
- чётко указать:
  - какой токен/аккаунт использовался,
  - какие запросы к Cloudflare API делал,
  - какая именно ошибка (отсутствие зоны/прав),
  - что должен сделать человек (например, привязать домен telex.global к нужному аккаунту и выдать token с DNS edit).

## SSH / Доступ к серверам

- Используй алиасы:
  - `ssh uk1` — смотреть референсный nginx/Keycloak конфиг и опыт UK1.
  - `ssh cfa1` — смотреть cfa1 ingress/Keycloak.
  - `ssh cfa2` — текущий таргет (compose, nginx, Keycloak, порталы).
- Работай аккуратно с продовым UK1: никаких правок без явной необходимости; используй его как эталон.

## СТИЛЬ РАБОТЫ

- Проверяй: сначала DNS/HTTP, потом Keycloak, потом фронты.
- Не ломай CI/cicd (dev-cfa2) — story про Cloudflare не должна влиять на .gitlab/gitlab-ci.dev.yml.
- Все команды, которые важны для DoD, фиксируй в Loop trace сториз и `OPS-001-cicd.verification.md`.

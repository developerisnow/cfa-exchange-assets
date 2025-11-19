---
created: 2025-11-19 20:40
updated: 2025-11-19 20:40
type: runbook-report
sphere: [devops]
topic: [deploy, cfa1, cfa2]
author: alex-a
agentID: 019a9c47-7b1b-7112-9672-694674728b0e
partAgentID: [co-7b1b]
version: 0.2.0
tags: [eywa1, cfa1, cfa2, dns, tls, nginx, pm2]
---

# CFA1 & CFA2 (FIN2) Deployment Status — co-7b1b

## Summary
- **DNS:** A-записи для `auth|issuer|investor|backoffice|api.cfa1.llmneighbors.com` и `*.cfa2.llmneighbors.com` созданы в Cloudflare и указывают на IP cfa1/fin2.
- **TLS:** wildcard LE-серты выпущены для `*.cfa1.llmneighbors.com` и `*.cfa2.llmneighbors.com` через `certbot/dns-cloudflare` и лежат в `/etc/letsencrypt/live/cfa{1,2}.llmneighbors.com/`.
- **Ingress:** nginx на обоих хостах проксирует домены на локальные порты (API/Keycloak/порталы) с корректными сертификатами.
- **CFA1 backend:** весь стек (Postgres, Kafka/ZK, Minio, Keycloak, все .NET-сервисы, API Gateway) запущен и health-эндпоинты отвечают `200`.
- **CFA1 frontends:** все три портала (issuer, investor, backoffice) работают в dev-режиме через PM2 и доступны по HTTPS (302/307 -> 200 после редиректа) через `issuer|investor|backoffice.cfa1.llmneighbors.com`.
- **CFA2 backend/frontends:** код и compose-окружение перенесены с cfa1, nginx/TLS/DNS настроены, но docker-стек сервисов и фронты пока не доведены до полного состояния (api.cfa2 отвечает 000, сервисы не стартовали до конца из-за тяжёлых pull/build и ограничений по времени/ресурсам).

## Final URL Table (Current State)

| Env  | App        | URL                                             | Status (curl -I / health) |
|------|------------|--------------------------------------------------|---------------------------|
| CFA1 | API        | https://api.cfa1.llmneighbors.com/health        | 200 OK                    |
| CFA1 | Issuer     | https://issuer.cfa1.llmneighbors.com/           | 307 (-> app), dev up      |
| CFA1 | Investor   | https://investor.cfa1.llmneighbors.com/         | 307 (-> app), dev up      |
| CFA1 | Backoffice | https://backoffice.cfa1.llmneighbors.com/       | 307 (-> app), dev up      |
| CFA2 | API        | https://api.cfa2.llmneighbors.com/health        | 000 (no backend yet)      |
| CFA2 | Issuer     | https://issuer.cfa2.llmneighbors.com/           | 502/000 (no app yet)      |

## Notes & Gaps
- CFA1 достиг уровня: DNS/TLS/nginx + полный backend + dev-фронты через PM2. Keycloak realm `ois-dev` существует, но redirectUris/webOrigins нужно ещё аккуратно выровнять под новые https-домены.
- CFA2 (fin2) очищен, подготовлен (user + /srv/cfa + /opt/ois-cfa + nginx + TLS + DNS), но docker-compose сервисы и фронтенды не успели поднять до полного UK1-паритета; это следующий логичный шаг.


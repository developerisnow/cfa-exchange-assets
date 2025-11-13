created: 2025-11-13 13:00
updated: 2025-11-13 15:25
type: planning
sphere: devops
topic: keycloak smtp setup
author: Alex (co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.2.0
tags: [keycloak, smtp, cloudflare]
---

# Context
- Нужно включить verifyEmail/forgot password в realm `ois-dev`.
- Публичные домены: `auth|issuer|investor|backoffice|api.cfa.llmneighbors.com` (через Cloudflare DNS only).
- Keycloak контейнер (`ois-keycloak`) в `/opt/ois-cfa` (docker-compose). Сейчас `verifyEmail=false`, `resetPasswordAllowed=true`.

# Status (2025-11-13 15:25 MSK)
- [x] SMTP: локальный Postfix + OpenDKIM (`host=172.18.0.1`, порт 25, auth off) + `mail.cfa.llmneighbors.com` DNS.
- [x] Keycloak realm: `verifyEmail=true`, `registrationAllowed=true`, `smtpServer.*` заполнены через `kcadm`.
- [x] SPF/DKIM/DMARC добавлены в Cloudflare (`mail._domainkey`, `_dmarc`, SPF TXT).
- [x] Docs обновлены (`docs/deploy/20251113-cloudflare-ingress.md` → раздел Email/Sender).
- [x] Smoke: Playwright self-registration + manual `mail` отправка → сообщения читаются через `api.mail.tm`.
- [ ] Дополнительно (отложено): fail2ban/ufw для Postfix, переход на внешнего SMTP если потребуется SLA, включить reset-password flow в UI.

# Notes
- Cloudflare API token лежит в `/home/user/__Repositories/cloudflare__developerisnow/.env`.
- Сертификаты в `/etc/letsencrypt/live/cfa.llmneighbors.com/`.
- Сейчас `x-ui` выключен, порт 443 свободен.

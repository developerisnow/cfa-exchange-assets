Alex ., [27/11/2025 20:15]
27.11.2025  
9 часов (10:00–19:00 плюс хвост)

- С нуля довёл до рабочего состояния dev‑CI в GitLab для ветки `dev-cfa2`:
  - раньше вообще не было отдельного dev‑pipeline под cfa2; сейчас есть `.gitlab/gitlab-ci.dev.yml` со стадиями `sdk → build → deploy`, runner vds1, и все backend/frontend сервисы собираются и деплоятся по одному и тому же сценарию;
  - runner vds1 привязан к проекту `npk/ois-cfa`, проверяется через `check-runner-status.sh` и GitLab API, ssh‑доступ с CI до `cfa2` зафиксирован через SSH_PRIVATE_KEY_CFA2.
- Собрал и обкатал полный цикл “коммит → образ в registry → deploy на cfa2”:
  - backend compose для cfa2 лежит в `deploy/docker-compose-at-vps/cfa2`, синхронизируется скриптом в `/srv/cfa`, а `deploy-cfa2` делает `docker compose pull && up -d`;
  - path‑based rules настроены и проверены на push (TC1–TC3: отдельный сервис, отдельный портал, чистый CI‑коммит), лишние сервисы/порталы не пересобираются.
- Настроил и описал ingress/Keycloak/порталы на `cfa2.telex.global`:
  - поднят Cloudflare ingress: DNS A‑записи на 92.51.38.126, wildcard LE‑сертификат `*.cfa2.telex.global`, nginx vhost `cfa2-portals.conf`;
  - Keycloak realm `ois` и клиенты порталов приведены к доменной схеме (`auth|issuer|investor|backoffice.cfa2.telex.global`), redirect’ы и webOrigins соответствуют тому, как это делали на uk1;
  - env порталов и CI‑дефолты очищены от IP/портов — теперь всё ходит через `https://auth.cfa2.telex.global`, без `https://...:58080` и прочих костылей.
- Добил инфраструктурные “мелочи”, без которых всё это развалилось бы:
  - настроил guardians (JSON‑правила + `scripts/guardians/check-guardians.sh` + job `guardians:check`), чтобы никто не тащил `.env`/`docker-compose.yml` в apps/docs и не правил uk1/cfa1 без флага;
  - перевёл контактный email у Let’s Encrypt на cfa2 на `alex.ocr.ai.llm@gmail.com` (`certbot update_account --email ...`), чтобы уведомления об истечении приходили не в никуда;
  - оформил архитектурный doc по OPS‑001 (CI, registry, deploy, ingress, certs) и cheatsheet с реальными командами (glab, ssh, build/deploy, Playwright, guardians).
- Подготовил почву для следующих шагов:
  - описал в stories и в отдельном промпте, что именно нужно сделать, чтобы довести логин через Keycloak по доменам до зелёных e2e‑тестов и скриншотов;
  - завёл story под observability/alerts (PHASE5), чтобы потом спокойно прикрутить метрики/Prometheus/Signoz и TLS‑нотификации в Telegram поверх уже рабочего dev‑стека.

Что ещё в работе / осталось добить:
- Playwright `public-auth` (issuer/investor/backoffice) нужно чуть доработать по селекторам/логину и собрать скриншоты успешного входа с разных IP;
- мониторинг CI/CD и TLS пока только в виде story/архитектуры — сами дашборды и алерты ещё предстоит сделать.

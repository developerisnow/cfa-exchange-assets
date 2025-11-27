Alex ., [27/11/2025 20:15]
27.11.2025  
9 часов (10:00–19:00 плюс хвост)

- Добил CICD‑контекст по dev-cfa2:
  - дочитал все OPS‑001 stories 001–005, AGENTS, старые сессии по uk1/cfa1, сверил ожидания по PHASE0–PHASE3;
  - выровнял PHASE0/PHASE1 stories под фактическое состояние (runner vds1, SSH на cfa2, glab, CI vars) и обновил runbook `cfa2-dev-runbook.md`.
- Почистил и задокументировал dev‑pipeline:
  - проверил path‑based rules на push (TC1–TC3, pipelines 289–291) для backend и фронтов, зафиксировал это в `OPS-001-003` и `CI-BUILD-MATRIX.md`;
  - добавил `registry:login-check`, доделал `check-runner-status.sh`, чтобы без kubeconfig можно было одним запуском увидеть статус vds1 через GitLab API.
- Разрулил Cloudflare/Keycloak/env на cfa2:
  - прошёлся по ingress: DNS/LE‑серты/nginx vhost для `*.cfa2.telex.global`, сверил с uk1/cfa1, описал в story и архитектурном доке;
  - привёл Keycloak realm `ois` и клиенты порталов под домены `auth|issuer|investor|backoffice.cfa2.telex.global`, убрал IP/порты из redirectUris/webOrigins;
  - привёл `.env`/compose и CI‑дефолты к HTTPS (`CFA2_FRONT_API_BASE_URL` / `CFA2_FRONT_KEYCLOAK_URL`) и добился, чтобы порталы на cfa2 ходили только на `https://auth.cfa2.telex.global` (без `:58080`).
- Поменял контактный email для LE на cfa2:
  - прямо на хосте выполнил `certbot update_account --email alex.ocr.ai.llm@gmail.com --agree-tos`, теперь письма об истечении идут на мой адрес, а не на фиктивный `ops@…`;
  - обновил архитектурный док и verification story, чтобы следующий агент не гадал “какой email указывать”.
- Подготовил “каркас” для следующих итераций:
  - собрал нормальный mermaid‑архитектурник по OPS‑001 (CI → registry → deploy → cfa2 → Cloudflare → Keycloak → порталы);
  - сделал отдельный cheatsheet с командами (glab, ssh, build/deploy, Playwright, guardians), чтобы не держать всё в голове;
  - написал финализирующий промпт для Cloudflare/Keycloak‑агента (что именно ещё нужно, чтобы логин по доменам стал зелёным);
  - создал story под observability/alerts (PHASE5), чтобы потом аккуратно прикрутить метрики/Prometheus/Signoz и TLS‑нотификации в Telegram.

Что не успел / WIP:
- Playwright `public-auth` пока ещё надо чуть‑чуть допилить (селекторы и логин‑флоу по issuer/investor/backoffice), плюс собрать скриншоты успешного логина — это оставил следующему заходу/агенту, но все ингредиенты и docs уже на месте.


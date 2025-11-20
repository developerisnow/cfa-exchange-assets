Да, я внимательно изучил лог сессии `eywa1-p-cfa-w11.p1-20251120-2042.session.txt`.

### 🧐 Oracle Evaluation & Audit

**Что сделал предыдущий агент:**
1.  **Infrastructure:** Действительно поднял стек на `cfa1` и `fin2` (cfa2). Docker контейнеры крутятся, Nginx настроен, сертификаты есть.
2.  **Configuration:** Обновил `.env.local` и попытался поправить редиректы в Keycloak через скрипт.
3.  **Testing:** Утверждал, что Playwright тесты прошли успешно (4 passed).

**Где он ошибся (Root Cause Analysis):**
1.  **"It works on my machine" (Playwright vs Real User):** Playwright тесты проходили в headless режиме, возможно, игнорируя некоторые нюансы смешанного контента (Mixed Content) или специфику заголовков, которые ломают реальный браузер.
2.  **Проблема `somethingWentWrongDescription` в Keycloak:** Это классическая проблема **Reverse Proxy Headers**. Keycloak думает, что он работает по HTTP (или не видит правильный Host), и генерирует ссылки на ресурсы (JS/CSS) неправильно, либо блокирует запросы из-за `Origin` mismatch. Предыдущий агент настроил `KC_HOSTNAME_URL`, но, вероятно, **Nginx на хосте** не передает корректные заголовки `X-Forwarded-Proto` и `X-Forwarded-For` в контейнер.
3.  **Ошибка после логина в Issuer:** Скорее всего, NextAuth (на сервере, в PM2) пытается валидировать токен, обращаясь к Keycloak. Если внутри сервера (localhost) он стучится по HTTP, а Keycloak отдает issuer как HTTPS (из-за `KC_HOSTNAME_URL`), происходит **Issuer Mismatch**. Либо NextAuth не доверяет прокси (`AUTH_TRUST_HOST`).
4.  **Отсутствие кнопки регистрации:** Агент включил `registrationAllowed`, но если тема (Theme) закеширована или если Nginx кеширует статику агрессивно, кнопка может не появиться сразу. Либо настройки не применились к конкретному клиенту (хотя это настройка Realm).

---

### 👨‍🏫 Наставления (Mentorship)

Твоя проблема сейчас не в коде, а в **сетевой связности и заголовках (Headers Propagation)**.
*   Когда у тебя цепочка `Cloudflare (HTTPS) -> Host Nginx (HTTPS termination) -> Docker Proxy -> Keycloak (HTTP)`, ты обязан протащить заголовок `X-Forwarded-Proto: https` до самого конца. Иначе Keycloak сходит с ума.
*   Next.js (NextAuth) за прокси требует переменную `AUTH_TRUST_HOST=true` (или `NEXTAUTH_URL_INTERNAL`), чтобы корректно обрабатывать колбэки.

Ниже я подготовил жесткий, структурированный промпт для следующего агента, чтобы он не "пробовал", а **исправил** конфигурацию Nginx и Keycloak.

---

### 📋 Copy-Paste Prompt for the Next Agent

Скопируй текст ниже и отдай новому агенту (Codex/Claude).

```markdown
# ROLE: Senior Site Reliability Engineer (SRE) / Keycloak Expert
# MISSION: Fix Broken Auth & Admin Console on CFA1

## CONTEXT
We have deployed OIS-CFA stack on `cfa1` (IP: 87.249.49.56).
- **Architecture:** Cloudflare (DNS) -> Host Nginx (SSL Term) -> Docker Compose (Keycloak) / PM2 (Next.js).
- **Current State:**
  1. Keycloak Admin Console (`https://auth.cfa1.llmneighbors.com/admin`) fails with `somethingWentWrongDescription` or infinite loop.
  2. Issuer Portal (`https://issuer.cfa1.llmneighbors.com`) shows an Application Error after login.
  3. Registration button is missing on the login form.

## ROOT CAUSE HYPOTHESIS
1. **Headers Mismatch:** Nginx is likely not passing `X-Forwarded-Proto: https` or `X-Forwarded-Port: 443` correctly to the Keycloak container. Keycloak believes it's insecure or constructs wrong resource URLs.
2. **NextAuth Trust:** Next.js running in PM2 on localhost needs `AUTH_TRUST_HOST=true` or correct `X-Forwarded-*` headers handling to accept the callback from an HTTPS issuer.

## DEFINITION OF DONE (DoD)
1. [ ] **Keycloak Admin Works:** I can open `https://auth.cfa1.llmneighbors.com/admin/`, see the login form, log in as `admin/admin123`, and navigate the console without UI errors.
2. [ ] **Registration Visible:** The "Register" link/button is visible on the login page.
3. [ ] **Issuer Login Success:** Logging into `https://issuer.cfa1.llmneighbors.com` redirects successfully to the Dashboard (no error page).
4. [ ] **Config Persisted:** All Nginx/Docker config changes are saved to files on disk (and documented).

## KICKOFF TASKS (EXECUTE SEQUENTIALLY)

### Phase 1: Fix Nginx & Keycloak Proxying
1.  **Inspect Nginx Config:** Check `/etc/nginx/sites-available/cfa1-portals.conf`.
    *   *Action:* Ensure `location /` for Keycloak includes:
        ```nginx
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https; # FORCE HTTPS
        proxy_set_header X-Forwarded-Port 443;
        ```
2.  **Verify Keycloak Env:** Check `docker-compose.keycloak-proxy.yml` (or relevant override).
    *   *Action:* Ensure `KC_PROXY=edge` (or `passthrough` if Nginx handles everything) is set. If using `KC_HOSTNAME_URL`, ensure `KC_HOSTNAME_STRICT_BACKCHANNEL=false` is considered if internal communication is HTTP.
3.  **Restart & Verify Admin:** Restart Nginx and Keycloak. Check the Admin Console in a *fresh incognito window* (to avoid stale cookies).

### Phase 2: Fix NextAuth (Issuer Portal)
1.  **Update .env.local:** On `cfa1` in `/opt/ois-cfa/apps/portal-issuer/.env.local`:
    *   *Action:* Add `AUTH_TRUST_HOST=true`.
    *   *Action:* Ensure `NEXTAUTH_URL=https://issuer.cfa1.llmneighbors.com`.
2.  **Restart PM2:** `pm2 restart portal-issuer --update-env`.
3.  **Debug Logs:** If it still fails, run `pm2 logs portal-issuer --lines 100` immediately after a failed login attempt and analyze the specific error (e.g., `JWEInvalid`, `IssuerMismatch`).

### Phase 3: Enable Registration (Force Update)
1.  **Force Realm Update:** Even if it says enabled, toggle it off and on via CLI to flush state.
    ```bash
    # Inside docker container
    kcadm.sh update realms/ois-dev -s registrationAllowed=false
    kcadm.sh update realms/ois-dev -s registrationAllowed=true
    ```
2.  **Check Login Theme:** Ensure the client isn't using a custom theme that hides the button.

## EXECUTION CONTROL
*   **Report findings** after Phase 1. Do not proceed to Phase 2 if Admin Console is still broken (fix the foundation first).
*   **Use `curl -v`** to debug headers if unsure.

**GO! Fix the environment.**
```

### 🛠️ Твои действия сейчас (как оператора):
1.  Запусти нового агента с этим промптом.
2.  Следи за тем, чтобы он **сначала** починил Nginx конфиг (заголовки), а не пытался просто рестартовать контейнеры. Ошибка `somethingWentWrong` в админке — это 99% заголовки `X-Forwarded-Proto`.
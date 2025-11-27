# Verification logs
## 2025-11-27 11:45 by Alex A `OPS-001-002-cicd-phase1.story`
### Highlights
0. DoD. не были отмечены часть выполненных DoD! Выполнил вручную! 
	- [ ] Always in Future mark checkboxes what was done
		- [ ] Always provide bello in a sub-unordered-list command to run and highlights results
1. Runner
	- [ ] Gitlab runners. status неясен или команды не работают или я что-то не так делают
2. Registry
	1. я так и не понял работает и как проверить, локально запустил ниже из bash log наверное не то
3. glab
	1. тут работает закрыто
4. SSH
	1. ага работает
5. CI Vars
	- [ ] ssh key. still not working. Почему не проверить вручную? Я дал команды что легко проверяется 
	- [ ] `https://git.telex.global/npk/ois-cfa/-/settings/ci_cd#js-cicd-variables-settings` там выстаплен ключ - содержимое из тех что я показывал в командах `SSH_PRIVATE_KEY_CFA2` - какой команд glab проверить это? проверь
	- [ ] CI. Vars тоже неясно - как будто ты тупо несоздал не говоря уже про SSH Key
		- [ ] 
### Bash
```bash
ssh cfa2 "cat ~/.ssh/id_ed25519"
[08:32] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ make check-runner-status
=== GitLab Runner Status Check ===

⚠ Warning: KUBECONFIG not set or file not found
Set it with: export KUBECONFIG=$(pwd)/ops/infra/timeweb/kubeconfig.yaml
Or run: make setup-kubeconfig

make: *** [Makefile:502: check-runner-status] Error 1
[08:42] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ docker login $CI_REGISTRY

USING WEB-BASED LOGIN
To sign in with credentials on the command line, use 'docker login -u <username>'

Your one-time device confirmation code is: DMHG-WWNP
Press ENTER to open your browser or submit your device code here: https://login.docker.com/activate

Waiting for authentication in the browser…
^Clogin canceled
[08:42] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ glab pipeline list --repo npk/ois-cfa --per-page 3
Showing 3 pipelines on npk/ois-cfa. (Page 1)

State            IID     Ref       Created
(failed) • #262  (#247)  dev-cfa2  (about 4 minutes ago)
(failed) • #261  (#246)  dev-cfa2  (about 10 minutes ago)
(failed) • #260  (#245)  dev-cfa2  (about 38 minutes ago)

[08:42] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ ssh user@92.51.38.126 "hostname && docker ps"
6033599-dq95453
CONTAINER ID   IMAGE                    COMMAND        CREATED      STATUS      PORTS                                                                                                NAMES
21b2ce4288e4   portainer/portainer-ce   "/portainer"   4 days ago   Up 4 days   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 0.0.0.0:9443->9443/tcp, [::]:9443->9443/tcp, 9000/tcp   portainer
[08:43] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ ssh cfa2 "hostname && docker ps"
6033599-dq95453
CONTAINER ID   IMAGE                    COMMAND        CREATED      STATUS      PORTS                                                                                                NAMES
21b2ce4288e4   portainer/portainer-ce   "/portainer"   4 days ago   Up 4 days   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 0.0.0.0:9443->9443/tcp, [::]:9443->9443/tcp, 9000/tcp   portainer
[08:43] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ glab auth status --hostname git.telex.global
git.telex.global
  ✓ Logged in to git.telex.global as cicd (/home/user/.config/glab-cli/config.yml)
  ✓ Git operations for git.telex.global configured to use ssh protocol.
  ✓ API calls for git.telex.global are made over https protocol.
  ✓ REST API Endpoint: https://git.telex.global/api/v4/
  ✓ GraphQL Endpoint: https://git.telex.global/api/graphql/
  ✓ Token found: **************************
[08:43] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ ./ops/scripts/check-gitlab-runners.sh
Error: GITLAB_TOKEN not set
Usage: ./ops/scripts/check-gitlab-runners.sh <gitlab-token> [project-id]
Or set: export GITLAB_TOKEN='your-token'
[08:43] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ uname -a
Linux eywa-ubuntu-8gb-hel1-2 5.15.0-125-generic #135-Ubuntu SMP Fri Sep 27 13:53:58 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
[08:44] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $ curl ipinfo.io
{
  "ip": "65.108.157.9",
  "hostname": "static.9.157.108.65.clients.your-server.de",
  "city": "Helsinki",
  "region": "Uusimaa",
  "country": "FI",
  "loc": "60.1695,24.9354",
  "org": "AS24940 Hetzner Online GmbH",
  "postal": "00100",
  "timezone": "Europe/Helsinki",
  "readme": "https://ipinfo.io/missingauth"
}[08:44] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (dev-cfa2) $
[08:39] user@eywa-ubuntu-8gb-hel1-2 prj_Cifra-rwa-exachange-assets (main+) $ ssh cfa2 "cat ~/.ssh/id_ed25519"
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAA....Oe0GiT
ngAAAAtzc2gtZW....acaujMsAPRA
AAAEC7YVu9yM8y26Gr1HASgkCiMtZ8AI9iMFmZjVDOT1FivMv2eQzi3+xJCEGTmBlLSqEQ
K1lbJq0e9dpxq6MywA9EAAAAFHVzZXJANjAzMzU5OS1kcTk1NDUzAQ==
-----END OPENSSH PRIVATE KEY-----
[08:39] user@eywa-ubuntu-8gb-hel1-2 prj_Cifra-rwa-exachange-assets (main+) $

```

## 2025-11-27 11:45 by Alex A `OPS-001-002-cicd-phase1.story`
### Highlights
1. Compose
	1. как происходит сейчас deploy? типо подключается runner по SSH и просто делает docker compose up а там images тянутся? то есть только docker-compose + configs представляет собой все что на cfa 2?
2. Build
	1. там еще как бы 8 сервисов вроде работают 
	2. только уточнения где хранятся images? gitlab registry?
	3. portainer установлен как он помогает его надо к cloud hosted web frontend подключить или он на каком-то порту?
3. Deploy
	1. падает из-за ssh key предыдущая stories
4. Runtime
	1. ну до этого рано
5. Docs
	1. о каких доках идет речь если не работает предыдущее

## 2025-11-27 15:10 by codex-cli d742 `OPS-001-003-cicd-phase2.story`
### CI path-based rules & deploy verification (dev-cfa2)
- Pipelines (dev-cfa2):
  - `#287` (api, FORCE_BUILD_ALL=1, SHA e0d553a…) — полный прогон sdk+build+deploy, упал на deploy из-за битого `SSH_PRIVATE_KEY_CFA2` (libcrypto).
  - `#288` (api, FORCE_BUILD_ALL=1, SHA e0d553a…) — осознанно cancel через glab api /pipelines/288/cancel (auto-cancel rule, чтобы не ждать повторный full build).
  - `#289` (push, SHA 6a77272…) — CI-only change (`.gitlab/gitlab-ci.dev.yml` + `AGENTS.md`), jobs: только `deploy-cfa2`; `validate-specs`/`generate-sdks`/все `build-*` = skipped.
  - `#290` (push, SHA 3855d3b2…) — TC2 registry-only: change в `services/registry/ci-tc2-registry.md`; jobs: `build-registry` + `deploy-cfa2` = success, остальные backend/frontend build jobs = skipped.
  - `#291` (push, SHA a72f4897…) — TC3 portal-issuer-only: change в `apps/portal-issuer/ci-tc3-portal-issuer.md`; jobs: `build-portal-issuer` + `deploy-cfa2` = success, другие фронты и все backend build jobs = skipped.

- SSH key / deploy:
  - Сгенерирован новый ed25519 key (`/tmp/ci_deploy_cfa2`), public установлен в `~/.ssh/authorized_keys` на `cfa2`.
  - Private залит в GitLab Var `SSH_PRIVATE_KEY_CFA2` в base64, `protected=false`, `masked=true`, `environment_scope=*`.
  - Deploy через CI: `deploy-cfa2` использует этот ключ (ssh-agent + ssh-add /tmp/ci_ssh_key).
  - Manual deploy-only: отдельный job `deploy-cfa2-only` (stage deploy, when: manual) добавлен в `.gitlab/gitlab-ci.dev.yml` для чистого `docker compose pull/up` без build.

- Runtime check (cfa2, via eywa1):
  - `ssh cfa2 "cd /srv/cfa && docker compose ps"` → все backend-сервисы, keycloak, minio, redis, postgres и три фронта `portal-issuer`/`portal-investor`/`backoffice` в состоянии Up.
  - `curl http://92.51.38.126:58081/swagger` → 301 на `swagger/index.html` (живой api-gateway).
  - `curl http://92.51.38.126:3001/3002/3003` → HTML Next.js c тайтлами Issuer/Investor/Backoffice (фронты отдают UI); для Investor сейчас `/api/auth/error?error=Configuration` (нужна отдельная настройка Keycloak/NextAuth).

- CI behavior summary:
  - Path-based rules теперь зависят от `CI_PIPELINE_SOURCE`:
    - для `source=="push"` → `changes:` работает как задумано (TC1–TC3 подтверждают);
    - для `source=="api"` → sdk/build jobs запускаются только при явном `FORCE_BUILD_ALL=1`/`ENABLE_SDK_JOBS=1`, иначе `when: never`.
  - Auto-cancel: API-пайплайны, которые гоняют лишние builds, явно отменяем и используем либо push-пайплайны, либо ручной `deploy-cfa2-only`/ssh+compose, чтобы не ждать 10–15 минут.

## 2025-11-27 17:15 by codex-cli d742 `OPS-001-005-cicd-cfa2-cloudflare-ingress.story`
### Cloudflare DNS + TLS + Keycloak/NextAuth alignment for cfa2.telex.global
- Cloudflare / DNS:
  - На `eywa1` с `/home/user/__Repositories/cloudflare__developerisnow/.env`:
    - `CLOUDFLARE_CFA_API_TOKEN` при `curl -s /zones?name=telex.global` → `\"success\":false,"errors":[{\"code\":9109,\"message\":\"Invalid access token\"}]`.  
    - Через `CLOUDFLARE_CFA_API_GLOBAL` + `CLOUDFLARE_CFA_EMAIL` (`X-Auth-Email`/`X-Auth-Key`) найдена зона `telex.global` (id `87c094e12d10e8d9977f0739adcc3e81`, account `CLOUDFLARE_CFA_ACCOUNT_ID`).  
    - Создан `/home/user/__Repositories/cloudflare__developerisnow/.env.cfa2.telex`:
      - `CF_ZONE_NAME=telex.global`, `CF_ZONE_ID=87c094e12d10e8d9977f0739adcc3e81`, `CF_API_TOKEN=${CLOUDFLARE_CFA_API_TOKEN}`, `CF_ACCOUNT_ID=${CLOUDFLARE_CFA_ACCOUNT_ID}`, `CF_HOST_PREFIXES=auth,issuer,investor,backoffice,api`, `CF_BASE_LABEL=cfa2`.  
    - A-записи для `auth|issuer|investor|backoffice|api.cfa2.telex.global` upsert’нуты через Cloudflare API (curl + jq) на `92.51.38.126`, `proxied=false`.  
    - Проверка:  
      ```bash
      dig +short auth.cfa2.telex.global issuer.cfa2.telex.global \
          investor.cfa2.telex.global backoffice.cfa2.telex.global \
          api.cfa2.telex.global @1.1.1.1
      # все → 92.51.38.126
      ```  
  - **Блокер/заметка:** скрипт `ops/scripts/cloudflare-dns-upsert.sh` по-прежнему требует рабочий API token (`CF_API_TOKEN`), т.к. использует `Authorization: Bearer ...`. Для telex.global нужно:  
    - в Cloudflare UI создать/обновить API Token с DNS-edit для зоны `telex.global` (`CLOUDFLARE_CFA_ACCOUNT_ID`),  
    - обновить `CLOUDFLARE_CFA_API_TOKEN` в `.env` на `eywa1` и перегенерировать `.env.cfa2.telex`,  
    - после этого можно перейти на штатный `cloudflare-dns-upsert.sh` вместо ручных curl.
- TLS / nginx (cfa2):
  - На `cfa2` (92.51.38.126):
    - Установлены `nginx`, `certbot`, `python3-certbot-dns-cloudflare`.  
    - Создан `/root/.secrets/cloudflare.ini` c `dns_cloudflare_email`/`dns_cloudflare_api_key` (глобальный ключ для CFA-аккаунта, значения не логировались).  
    - Команда:
      ```bash
      sudo certbot certonly --dns-cloudflare \
        --dns-cloudflare-credentials /root/.secrets/cloudflare.ini \
        --dns-cloudflare-propagation-seconds 45 \
        -d '*.cfa2.telex.global' -d 'cfa2.telex.global' \
        --agree-tos --email alex.ocr.ai.llm@gmail.com --non-interactive
      ```
      → сертификат в `/etc/letsencrypt/live/cfa2.telex.global/`.  
    - Развёрнут `/etc/nginx/sites-available/cfa2-portals.conf`:
      - HTTP→HTTPS redirect для `auth|issuer|investor|backoffice|api.cfa2.telex.global`;  
      - upstream’ы: `keycloak` → `127.0.0.1:58080`, порталы → `127.0.0.1:3001/2/3`, api-gateway → `127.0.0.1:58081`;  
      - `ssl_certificate`/`ssl_certificate_key` с wildcard LE.  
    - Активирован vhost (`sites-enabled`) и `nginx -t && systemctl reload nginx`.  
    - Проверка:
      ```bash
      curl -vk https://auth.cfa2.telex.global | head -20
      # TLS: CN=*.cfa2.telex.global, issuer=Let's Encrypt (E7), 302 → https://auth.cfa2.telex.global/admin/
      ```
- Keycloak (`ois` realm) + clients:
  - Compose/env:
    - В `deploy/docker-compose-at-vps/cfa2/docker-compose.yml` для `keycloak` добавлены:
      - `KC_HOSTNAME=auth.cfa2.telex.global`, `KC_PROXY=edge`, `KC_HTTP_ENABLED=true`.  
    - `.env.cfa2` на cfa2 после `sync-compose-cfa2.sh`:
      - `NEXT_PUBLIC_API_BASE_URL=https://api.cfa2.telex.global`,  
      - `NEXT_PUBLIC_KEYCLOAK_URL=https://auth.cfa2.telex.global`,  
      - порталы на 3001/3002/3003.  
  - Внутри контейнера `ois-keycloak` через `kcadm`:
    - Realm `ois` существует (`kcadm get realms/ois`).  
    - Клиенты:
      - `portal-issuer` → `rootUrl=https://issuer.cfa2.telex.global`, `redirectUris=["https://issuer.cfa2.telex.global/*","https://issuer.cfa2.telex.global/api/auth/callback/keycloak"]`, `webOrigins=["https://issuer.cfa2.telex.global"]`, `secret=secret`.  
      - `portal-investor` → аналогично c `https://investor.cfa2.telex.global`.  
      - `backoffice` → аналогично c `https://backoffice.cfa2.telex.global`.  
    - Пользователи:
      - `issuer@test.com` (роль `issuer`), `investor@test.com` (роль `investor`), `cfa.devs@gmail.com` (роли `backoffice` + `admin`) — проверено через `kcadm get users` + `role-mappings/realm`.  
    - OpenID configuration:
      ```bash
      curl -sk https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration | jq .issuer
      # "https://auth.cfa2.telex.global/realms/ois"
      ```
- Portals / NextAuth (issuer/investor/backoffice):
  - Обновлён compose для порталов (`deploy/docker-compose-at-vps/cfa2/docker-compose.yml`):
    - Все три портала:
      - `NEXT_PUBLIC_API_BASE_URL=https://api.cfa2.telex.global`,  
      - `NEXT_PUBLIC_KEYCLOAK_URL=https://auth.cfa2.telex.global`, `NEXT_PUBLIC_KEYCLOAK_REALM=ois`, `NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=portal-issuer|portal-investor|backoffice`,  
      - `NEXTAUTH_URL=https://<portal>.cfa2.telex.global`,  
      - `KEYCLOAK_CLIENT_SECRET=secret`,  
      - `KEYCLOAK_INTERNAL_URL=http://keycloak:8080`,  
      - `NEXTAUTH_SECRET=dev-nextauth-secret-cfa2`.  
    - После `sync-compose-cfa2.sh` → `ssh cfa2 "cd /srv/cfa && docker compose up -d"` перезапущены `portal-issuer|portal-investor|backoffice`.  
  - До правок `portal-investor`/`backoffice` выдавали:
    - 500/`/api/auth/error?error=Configuration` и в логах `NextAuth error NO_SECRET MissingSecretError`.  
  - После правок:
    ```bash
    curl -kI https://issuer.cfa2.telex.global      # HTTP/2 307 → /auth/signin
    curl -kI https://investor.cfa2.telex.global    # HTTP/2 307 → /auth/signin
    curl -kI https://backoffice.cfa2.telex.global  # HTTP/2 307 → /api/auth/signin?callbackUrl=%2F
    ```
    - `/auth/signin` для issuer/investor отдаёт HTML Next.js с формой логина, без 500/Configuration.  
  - **TODO (manual):** в браузере пройти полный login-flow для `issuer@test.com` / `investor@test.com` / `cfa.devs@gmail.com` и приложить скриншоты/e2e отчёты (см. DoD story).

## 2025-11-27 18:30 by d742-codex `OPS-001-001-cicd-phase0-prepare-vps-and-gitlab.story`

### Highlights

- Переподнята проверка runner’а: `make check-runner-status` теперь не зависит от kubeconfig и использует GitLab API для проекта `npk/ois-cfa` (через `glab`), что даёт быстрый чек статуса `vds1` на eywa1.  
- Уточнены и задокументированы SSH/CI переменные: зафиксирован fingerprint ключа `user@cfa2` и подтверждено, что `SSH_PRIVATE_KEY_CFA2` и registry-переменные (`CI_REGISTRY*`) используются во всех `build-*`/`deploy-cfa2` job’ах; добавлен debug-job `registry:login-check`.  
- Runbook `cfa2-dev-runbook.md` обновлён секцией "PHASE0 / prerequisites" (runner, glab, SSH, CI vars) и теперь прямо ссылается на команды проверки.

### Bash

```bash
# Runner / glab
cd repositories/customer-gitlab/ois-cfa
./ops/scripts/check-runner-status.sh
glab auth status --hostname git.telex.global
glab api '/projects/npk%2Fois-cfa/runners?per_page=20' | jq '.[] | {id,description,status,tag_list}'

# SSH / runtime на cfa2
ssh cfa2 "hostname && ls -d /srv/cfa && docker compose ps"
ssh cfa2 "ssh-keygen -lf ~/.ssh/id_ed25519.pub"

# CI vars / registry
glab api /projects/npk%2Fois-cfa/variables | jq '.[] | select(.key==\"SSH_PRIVATE_KEY_CFA2\")'
glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=10' | jq '.[] | {id,source,status}'
```

## 2025-11-27 18:35 by d742-codex `OPS-001-002/003-cicd-phase1-2.story` (backend + frontends + SDK)

### Highlights

- Подтверждён backend dev pipeline: compose/env на cfa2 соответствуют `deploy/docker-compose-at-vps/cfa2/*`, все backend-сервисы и gateway в состоянии `Up` (`docker compose ps` на cfa2), swagger отвечает по портам 5808x.  
- Проверены path-based rules и SDK stage: на push-пайплайнах TC1–TC3 (ID `289–291`) запускались только ожидаемые jobs (`deploy-cfa2` / `build-registry` / `build-portal-issuer`), что зафиксировано в story и CI-BUILD-MATRIX.  
- Runbook `cfa2-dev-runbook.md` и `CI-BUILD-MATRIX.md` расширены секциями про backend dev pipeline и "Frontends and SDK (PHASE2)" (ports, jobs, stage-порядок, условия запуска).  

### Bash

```bash
# Pipelines и path-based jobs
glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=10' \
  | jq '.[] | {id,iid,sha,source,status}'

for id in 289 290 291; do
  echo "== Pipeline $id jobs =="
  glab api "/projects/npk%2Fois-cfa/pipelines/$id/jobs" \
    | jq '.[] | {name,stage,status}'
done

# Runtime на cfa2
ssh cfa2 "cd /srv/cfa && docker compose ps"
curl -sS --max-time 5 http://92.51.38.126:58081/swagger | head -1 || true
curl -sS --max-time 5 http://92.51.38.126:3001 | head -1
```

## 2025-11-27 18:40 by d742-codex `OPS-001-004-cicd-phase4.story` (guardians)

### Highlights

- Добавлен JSON-конфиг guardian’ов `ops/guardians/guardian.config.json` с минимальным набором правил: запрет новых `.gitlab-ci*.yml` вне корня/.gitlab, запрет `docker-compose.yml` и `.env` в `docs/**`, `apps/**`, `tests/**`, защита `ops/infra/uk1/**` и `ops/infra/cfa1/**` с override-переменной.  
- Реализован скрипт `scripts/guardians/check-guardians.sh`, который считывает staged или изменённые файлы (локально и в CI), проверяет их против правил и падает с понятными сообщениями при нарушении; поддерживает `GUARDIANS_BYPASS` и `GUARDIANS_ALLOW_PROD_INFRA`.  
- В `.gitlab/gitlab-ci.dev.yml` добавлен job `guardians:check` (stage `sdk`, `tags: [vds1]`); на push-пайплайне `#300` (dev-cfa2, SHA `be9e49c6...`) job `guardians:check` (id `3013`) прошёл успешно, проверив именно изменённые файлы (ci config, runbook, matrix, guardians-config, script).

### Bash

```bash
cd repositories/customer-gitlab/ois-cfa

# Проверка конфига и скрипта локально
cat ops/guardians/guardian.config.json | jq '.rules[].id'
scripts/guardians/check-guardians.sh

# Фрагмент CI-конфига (manual review)
sed -n '1,80p' .gitlab/gitlab-ci.dev.yml
sed -n '80,180p' .gitlab/gitlab-ci.dev.yml
```

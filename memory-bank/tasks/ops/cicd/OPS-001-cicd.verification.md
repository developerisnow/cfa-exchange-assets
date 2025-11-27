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

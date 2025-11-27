---
created: 2025-11-27 19:25
updated: 2025-11-27 19:25
type: cheatsheet
sphere: [devops]
topic: [cfa2, cicd, cloudflare, keycloak, portals]
author: alex
epic_id: OPS-001-CICD
version: 0.1.0
tags: [adhd-friendly, quickstart, commands]
---

# OPS-001 · CI/CD Cheatsheet (dev-cfa2 + cfa2.telex.global)

> One-page tables for ADHD brain: “what I want” → “what I run” → “what I expect”.

## 1. Phase 0 – Runner, glab, SSH, vars

| Goal | Command(s) | Expect |
|------|------------|--------|
| Set GitLab token | `export GITLAB_HOST=git.telex.global`<br/>`export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/.env \| cut -d= -f2-)` | `glab` uses `cicd` token |
| Check auth | `glab auth status --hostname git.telex.global` | Logged in as `cicd` |
| Check project runners | `cd .../ois-cfa && ./ops/scripts/check-runner-status.sh` | Fallback to GitLab API mode; shows project runners incl. `vds1-auto-runner` online |
| List pipelines | `glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=5' \| jq '.[] \| {id,status,source,sha}'` | Last dev-cfa2 pipelines |
| SSH to cfa2 | `ssh cfa2 "hostname && ls -d /srv/cfa && docker compose ps"` | Hostname `cfa2`, stack containers |
| Check SSH key var | `glab api /projects/npk%2Fois-cfa/variables \| jq '.[] \| select(.key=="SSH_PRIVATE_KEY_CFA2")'` | `protected=false`, `masked=true` |

## 2. Phase 1 – Backend build & deploy (dev-cfa2)

| Goal | Command(s) | Expect |
|------|------------|--------|
| Full backend build+deploy (push) | Edit any backend path (e.g. `services/registry/...`), then:<br/>`git commit -m "test: backend change" && git push origin dev-cfa2` | Pipeline `source:"push"`, relevant `build-*` backend jobs + `deploy-cfa2` green |
| Force all builds on push | As above + in GitLab UI start pipeline with var `FORCE_BUILD_ALL=1` | All `sdk`/`build-*` jobs run even without path changes |
| Debug registry login | In CI: set `ENABLE_REGISTRY_DEBUG=1` and run pipeline on dev-cfa2 | Job `registry:login-check` runs, `docker login` success |
| Check runtime | `ssh cfa2 "cd /srv/cfa && docker compose ps"`<br/>`curl -s http://92.51.38.126:58081/swagger \| head -1` | Backend services `Up`, swagger HTML |

## 3. Phase 2 – Frontends + SDK + path-based

| Goal | Command(s) | Expect |
|------|------------|--------|
| TC1 – CI-only change | Change only `.gitlab/gitlab-ci.dev.yml` / docs / AGENTS, then `git push origin dev-cfa2` | Push pipeline: `deploy-cfa2` runs; all `sdk` + `build-*` jobs skipped |
| TC2 – single backend | Change only `services/registry/ci-tc2-registry.md`, then push | Push pipeline: `build-registry` + `deploy-cfa2`; другие `build-*` skipped |
| TC3 – single frontend | Change only `apps/portal-issuer/ci-tc3-portal-issuer.md`, then push | Push pipeline: `build-portal-issuer` + `deploy-cfa2`; остальные фронты+backend `build-*` skipped |
| Rebuild **only portals** (auth fix) | Add tiny files in all three apps:<br/>`echo "ci-rebuild $(date -Iseconds)" > apps/portal-issuer/ci-rebuild-auth-issuer.md`<br/>`...investor...`<br/>`...backoffice...`<br/>`git add ... && git commit -m "chore(ci): rebuild portals for auth fix" && git push origin dev-cfa2` | Push pipeline: `build-portal-issuer`, `build-portal-investor`, `build-backoffice` + `deploy-cfa2` green; backend builds may be skipped |
| Check build matrix | `cat docs/deploy/vps-cfa2/CI-BUILD-MATRIX.md` | Table matches jobs/paths in `.gitlab/gitlab-ci.dev.yml` |

## 4. Phase 3 – Cloudflare + Keycloak + portals login

| Goal | Command(s) | Expect |
|------|------------|--------|
| Check DNS | `dig +short auth.cfa2.telex.global @1.1.1.1`<br/>`dig +short issuer.cfa2.telex.global @1.1.1.1`<br/>`...investor,backoffice,api...` | All → `92.51.38.126` |
| Check TLS | `curl -vk https://auth.cfa2.telex.global \| head -20` | LE cert `*.cfa2.telex.global`, 200/302 |
| Check Keycloak issuer | `curl -sk https://auth.cfa2.telex.global/realms/ois/.well-known/openid-configuration \| jq '.issuer'` | `"https://auth.cfa2.telex.global/realms/ois"` |
| Check portal envs on cfa2 | `ssh cfa2 "docker exec portal-issuer env \| grep -E 'NEXT_PUBLIC_|NEXTAUTH_URL|KEYCLOAK_'"` (same for investor/backoffice) | `NEXT_PUBLIC_KEYCLOAK_URL=https://auth.cfa2.telex.global`, `NEXTAUTH_URL=https://<portal>.cfa2.telex.global`, `KEYCLOAK_INTERNAL_URL=http://keycloak:8080` |
| **Never** use HTTPS on 58080 | **DON’T** run `https://auth.cfa2.telex.global:58080` in browser | This always yields `SSL record length` error (HTTP-only port) |

## 5. Phase 3 – Playwright E2E (public-auth)

| Goal | Command(s) | Expect |
|------|------------|--------|
| Prepare Playwright env | `cat > tests/e2e-playwright/.env.cfa2 << 'EOF'`<br/>`ISSUER_BASE_URL=https://issuer.cfa2.telex.global`<br/>`INVESTOR_BASE_URL=https://investor.cfa2.telex.global`<br/>`BACKOFFICE_BASE_URL=https://backoffice.cfa2.telex.global`<br/>`USE_KEYCLOAK_AUTH=true`<br/>`ISSUER_USER=issuer@test.com` ... `EOF` | `.env.cfa2` with domain URLs (no `:58080`) |
| Run tests | `cd .../ois-cfa && npx playwright test tests/e2e-playwright/tests/public-auth.spec.ts --config=tests/e2e-playwright/playwright.config.ts --project=chromium` | Issuer+Investor (и позже Backoffice) tests green |
| On failure | `ssh cfa2 "docker logs --tail=200 portal-issuer"` (и investor/backoffice) | Look for `MissingSecretError` или смешанные URLs `http://...:58080` |
| Fix loop | Если в логах HTTP/IP → исправить env/код, rebuild portals (см. раздел 3), повторить Playwright | Повторять, пока все auth-тесты не станут зелёными |

## 6. Phase 4 – Guardians / Guardrails

| Goal | Command(s) | Expect |
|------|------------|--------|
| Local guardian check | `cd .../ois-cfa && scripts/guardians/check-guardians.sh` | Сообщение `Guardians: OK` или список нарушений с exit 1 |
| CI guardian job | В GitLab → любой pipeline на dev-cfa2 | Job `guardians:check` (stage `sdk`) зелёный, либо падает на реальных нарушениях |
| Bypass (senior-only) | `GUARDIANS_BYPASS=1 scripts/guardians/check-guardians.sh` | Сообщение о bypass, exit 0 |
| Allow uk1/cfa1 edits | set `GUARDIANS_ALLOW_PROD_INFRA=1` (локально или в pipeline vars) | Разрешены изменения под `ops/infra/uk1/**` и `ops/infra/cfa1/**` |

## 7. “When in doubt” quick checks

| Situation | Check | Command |
|-----------|-------|---------|
| “Почему всё билдится?” | Посмотри `source` и `before_sha` | `glab api '/projects/npk%2Fois-cfa/pipelines/{ID}' \| jq '{id,source,before_sha}'` |
| “Только CI поменял, а билдится портал?” | См. jobs на push‑pipeline | `glab api '/projects/npk%2Fois-cfa/pipelines/{ID}/jobs' \| jq '.[] \| {name,status,stage}'` |
| “Порталы не логинятся” | Проверить треугольник: `NEXTAUTH_URL`, `NEXT_PUBLIC_KEYCLOAK_URL`, Keycloak clients, логи порталов | см. разделы 4–5 выше |
| “Хочу просто redeploy cfa2” | manual job без build | job `deploy-cfa2-only` (если присутствует) или `ssh cfa2 "cd /srv/cfa && docker compose pull && docker compose up -d"` |

> This cheatsheet is meant to be skimmed in seconds. For the full story context (DoD, Loops, verification), use the story files `OPS-001-00*.story.md` and `OPS-001-CICD-architecture.md` for diagrams.


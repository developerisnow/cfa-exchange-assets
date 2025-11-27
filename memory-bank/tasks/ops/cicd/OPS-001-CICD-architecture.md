---
created: 2025-11-27 19:25
updated: 2025-11-27 19:25
type: docs-architecture
sphere: [devops]
topic: [cfa2, cicd, cloudflare, keycloak]
author: alex
epic_id: OPS-001-CICD
version: 0.1.0
tags: [dev-cfa2, gitlab-ci, vds1, cfa2, cloudflare, portals]
---

# OPS-001 · CI/CD & Ingress Architecture (dev-cfa2)

> High-level view of how commits on `dev-cfa2` flow through GitLab CI, runner `vds1`, `cfa2` docker-compose, and Cloudflare/Keycloak/portals.

## Sequence · CI/CD pipeline (dev-cfa2)

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Dev (eywa1)
    participant GitLab as GitLab CI<br/>npk/ois-cfa
    participant Guardians as guardians:check<br/>(sdk stage)
    participant SDK as sdk stage<br/>(validate-specs/generate-sdks)
    participant Build as build stage<br/>(backend+front)
    participant Deploy as deploy-cfa2
    participant Runner as Runner vds1
    participant CFA2 as cfa2 VPS<br/>/srv/cfa

    Dev->>GitLab: git push origin dev-cfa2
    note over GitLab: workflow.rules allow only dev-cfa2

    GitLab->>Guardians: start job guardians:check (stage sdk)
    Guardians->>Guardians: scan changed files<br/>guardian.config.json rules
    alt violations
        Guardians-->>GitLab: fail pipeline (policy violation)
    else ok
        Guardians-->>GitLab: success
        GitLab->>SDK: validate-specs / generate-sdks<br/>(only on path changes + ENABLE_SDK_JOBS)
        SDK-->>GitLab: success / fail (contracts/sdks)

        GitLab->>Build: build-* jobs (backend & portals)<br/>selected via rules:changes on dev-cfa2 push
        Build->>Runner: docker buildx + docker login<br/>push :SHORT_SHA and :dev tags
        Build-->>GitLab: build jobs green / skipped (path-based)

        GitLab->>Deploy: deploy-cfa2 (stage deploy)
        Deploy->>Runner: ssh to cfa2 with SSH_PRIVATE_KEY_CFA2
        Runner->>CFA2: cd /srv/cfa &&<br/>REGISTRY_IMAGE=$CI_REGISTRY_IMAGE TAG=dev<br/>docker compose pull && up -d
        CFA2-->>Runner: stack up (postgres, keycloak,<br/>backend services, portals)
        Runner-->>Deploy: success
        Deploy-->>GitLab: pipeline success
    end
```

### Notes

- Path-based rules for `build-*` jobs срабатывают **только** для `CI_PIPELINE_SOURCE=="push"`; API-пайплайны с `before_sha=000...` считаются “full diff”.
- `deploy-cfa2` не переписывает compose/env на `cfa2`, он только делает `pull`/`up` уже синхронизированного бандла.
- Target runtime: все backend сервисы + три портала работают на `cfa2` (IP 92.51.38.126), а ingress по доменам `*.cfa2.telex.global` настроен через Cloudflare+nginx.

## Sequence · HTTPS ingress & login via Keycloak (cfa2.telex.global)

```mermaid
sequenceDiagram
    autonumber
    participant User as Browser/Playwright
    participant DNS as Cloudflare DNS<br/>telex.global
    participant Nginx as nginx@cfa2<br/>443 TLS
    participant Keycloak as Keycloak<br/>realm ois
    participant Issuer as portal-issuer
    participant Investor as portal-investor
    participant Backoffice as backoffice

    User->>DNS: resolve issuer.cfa2.telex.global
    DNS-->>User: 92.51.38.126
    User->>Nginx: HTTPS GET https://issuer.cfa2.telex.global/
    Nginx-->>User: 302 → /auth/signin (NextAuth)

    User->>Issuer: GET /auth/signin
    Issuer-->>User: login page (NextAuth UI)

    User->>Issuer: click "Sign in with Keycloak"
    Issuer->>Keycloak: redirect to https://auth.cfa2.telex.global/realms/ois/...
    Keycloak-->>User: login form (realm ois)

    User->>Keycloak: POST credentials (issuer@test.com/Pass...)
    Keycloak->>Issuer: redirect back with code → callback<br/>https://issuer.cfa2.telex.global/api/auth/callback/keycloak
    Issuer->>Keycloak: token/userinfo via KEYCLOAK_INTERNAL_URL<br/>http://keycloak:8080/realms/ois/...
    Issuer-->>User: session cookie + app page (/dashboard)

    note over Investor,Backoffice: Investor/backoffice portals follow the same flow<br/>(own clientId, same realm/hostnames).
```

### Notes

- Внешние URL **всегда** без порта: `https://auth.cfa2.telex.global` и `https://issuer|investor|backoffice.cfa2.telex.global`.
- Порт `58080` используется только как **внутренний HTTP upstream** (`KEYCLOAK_INTERNAL_URL=http://keycloak:8080` и `nginx proxy_pass http://127.0.0.1:58080`).
- Любая попытка обратиться к `https://auth.cfa2.telex.global:58080` даёт SSL error (`record length`), т.к. TLS шлётся в HTTP‑порт.

## C4-style container view (text)

```mermaid
graph LR
    subgraph GitLab
      A[.gitlab/gitlab-ci.dev.yml<br/>dev-cfa2 pipeline] --> B[guardians:check]
      B --> C[sdk stage<br/>validate-specs/generate-sdks]
      C --> D[build stage<br/>backend & portals]
      D --> E[deploy-cfa2<br/>deploy-cfa2-only]
    end

    subgraph Infra
      F[Runner vds1<br/>docker executor] --> G[cfa2 VPS<br/>/srv/cfa docker-compose]
      G --> H[Backend services<br/>api-gateway, identity, etc.]
      G --> I[Portals<br/>issuer, investor, backoffice]
      G --> J[Keycloak realm ois<br/>postgres, redis, minio]
      K[Cloudflare DNS/TLS<br/>telex.global] --> L[nginx@cfa2 443<br/>cfa2-portals.conf]
      L --> J
      L --> I
      L --> H
    end

    M[Dev/Browser/Playwright] --> K
```

### Mapping to OPS-001 stories

- **OPS-001-001 (PHASE0)** — Runner vds1 + cfa2 + GitLab/glab/vars (A ↔ F ↔ G).
- **OPS-001-002 (PHASE1)** — Backend compose/env + build/deploy (D↔E↔G↔H).
- **OPS-001-003 (PHASE2)** — Frontends + SDK + path-based CI (C↔D↔I, plus rules).
- **OPS-001-004 (PHASE4)** — Guardians / guardrails (B + guardian.config/check-guardians).
- **OPS-001-005 (PHASE3)** — Cloudflare ingress + Keycloak + portals login (K↔L↔J↔I + M).

> For concrete commands and step-by-step flows, see the cheatsheet: `memory-bank/tasks/ops/cicd/OPS-001-CICD-cheatsheet.md`.


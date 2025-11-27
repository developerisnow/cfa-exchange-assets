---
created: 2025-11-27 14:00
updated: 2025-11-27 14:00
type: skill
sphere: devops
topic: cicd, gitlab, glab
author: claude
version: 1.0.0
tags: [cicd, gitlab, glab, ois-cfa, cfa2, devops]
---

# CI/CD GitLab Skill for ois-cfa

Complete knowledge base for managing CI/CD pipeline for ois-cfa project.

## Quick Reference Card

### Environment Setup (ALWAYS RUN FIRST)

```bash
# Option 1: Manual export
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/.env | cut -d= -f2-)

# Option 2: One-liner wrapper
glab-cfa() {
  GITLAB_HOST=git.telex.global \
  GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/.env | cut -d= -f2-) \
  glab "$@"
}
```

### Most Used Commands (Copy-Paste Ready)

```bash
# === PIPELINES ===

# List last 5 pipelines
glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=5' | jq '.[] | {id,status,created_at}'

# Trigger pipeline (normal)
glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2

# Trigger pipeline (force all builds)
glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2 -F "variables[FORCE_BUILD_ALL]=1"

# Cancel pipeline
glab api --method POST '/projects/npk%2Fois-cfa/pipelines/{ID}/cancel'


# === JOBS ===

# List jobs in pipeline
glab api '/projects/npk%2Fois-cfa/pipelines/{PIPELINE_ID}/jobs' | jq '.[] | {id,name,stage,status}'

# Get job logs (last 50 lines)
glab api '/projects/npk%2Fois-cfa/jobs/{JOB_ID}/trace' | tail -n 50

# Retry job
glab api --method POST '/projects/npk%2Fois-cfa/jobs/{JOB_ID}/retry'


# === VARIABLES ===

# List all variables
glab api /projects/npk%2Fois-cfa/variables | jq '.[] | {key,protected,masked}'

# Check specific variable
glab api /projects/npk%2Fois-cfa/variables | jq '.[] | select(.key=="SSH_PRIVATE_KEY_CFA2")'

# Unprotect variable for dev branch
glab api --method PUT /projects/npk%2Fois-cfa/variables/SSH_PRIVATE_KEY_CFA2 \
  -F "protected=false" -F "masked=true" -F "environment_scope=*"


# === RUNNERS ===

# Check runner vds1 status
glab api '/projects/npk%2Fois-cfa/runners' | jq '.[] | select(.tag_list[] == "vds1")'


# === DEPLOY VERIFICATION ===

# Check containers on cfa2
ssh cfa2 "cd /srv/cfa && docker compose ps"

# Check service logs
ssh cfa2 "cd /srv/cfa && docker compose logs --tail=20 api-gateway"

# Curl swagger
curl -s http://92.51.38.126:58081/swagger | head -1
```

## Architecture

### Topology

```
eywa1 (control plane)
    │
    ├─── git.telex.global (GitLab)
    │       └── npk/ois-cfa repo
    │       └── Container Registry
    │
    ├─── vds1 (167.235.11.150)
    │       └── GitLab Runner (tag: vds1)
    │       └── Docker executor
    │
    └─── cfa2 (92.51.38.126)
            └── Docker host
            └── /srv/cfa (compose + .env)
```

### Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        dev-cfa2 branch                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE: sdk                                                      │
│ ┌─────────────────┐  ┌──────────────────┐                       │
│ │ validate-specs  │  │ generate-sdks    │ (gated by             │
│ │ (OpenAPI lint)  │  │ (TS SDK gen)     │  ENABLE_SDK_JOBS=1)   │
│ └─────────────────┘  └──────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE: build (parallel, rules:changes based)                    │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐              │
│ │ api-gateway  │ │ identity     │ │ issuance     │ ...          │
│ └──────────────┘ └──────────────┘ └──────────────┘              │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐              │
│ │ portal-issuer│ │portal-investor│ │ backoffice  │              │
│ └──────────────┘ └──────────────┘ └──────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE: deploy                                                   │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ deploy-cfa2                                                 │ │
│ │   1. ssh-add SSH_PRIVATE_KEY_CFA2                           │ │
│ │   2. docker login to registry                               │ │
│ │   3. ssh cfa2: docker compose pull                          │ │
│ │   4. ssh cfa2: docker compose up -d                         │ │
│ └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Services & Ports (cfa2)

| Service | Port | Swagger/UI |
|---------|------|------------|
| api-gateway | 58081 | /swagger |
| identity | 58082 | /swagger |
| issuance | 58083 | /swagger |
| registry | 58084 | /swagger |
| settlement | 58085 | /swagger |
| compliance | 58086 | /swagger |
| keycloak | 58080 | / |
| postgres | 55432 | - |
| redis | 56379 | - |
| minio | 59000 | console:59001 |
| portal-issuer | 3001 | / |
| portal-investor | 3002 | / |
| backoffice | 3003 | / |

## Troubleshooting Decision Tree

```
Pipeline failed?
    │
    ├── Which stage?
    │   ├── sdk → validate-specs or generate-sdks failed
    │   │       └── Check: packages/contracts/* for OpenAPI errors
    │   │       └── Workaround: trigger without ENABLE_SDK_JOBS
    │   │
    │   ├── build → Docker build failed
    │   │       └── Check: Dockerfile, dependencies
    │   │       └── Get logs: glab api /jobs/{ID}/trace
    │   │
    │   └── deploy → SSH or compose failed
    │           │
    │           ├── "SSH_PRIVATE_KEY_CFA2 is empty"
    │           │       └── Variable missing or protected=true
    │           │       └── Fix: /cicd-vars unprotect SSH_PRIVATE_KEY_CFA2
    │           │
    │           ├── "ssh-add failed" / "libcrypto"
    │           │       └── Key format wrong (needs base64 or raw PEM)
    │           │       └── Fix: re-upload key correctly
    │           │
    │           ├── "manifest unknown"
    │           │       └── Image :dev not built yet
    │           │       └── Fix: /cicd-run force
    │           │
    │           └── "connection refused" / timeout
    │                   └── cfa2 down or firewall
    │                   └── Check: ssh cfa2 "hostname"
```

## Path-Based Build Rules (Senior Level)

### Concept
Не билдить все 11 образов каждый раз - только те, где изменились файлы.

### Implementation
Каждый `build-*` job имеет `rules:changes`:

```yaml
build-identity:
  rules:
    - if: '$FORCE_BUILD_ALL == "1"'     # Override - билдим всё
    - if: '$CI_COMMIT_BRANCH == "dev-cfa2"'
      changes:                           # Билдим ТОЛЬКО если изменилось:
        - "services/identity/**"         # - сам сервис
        - "packages/contracts/**"        # - контракты (shared)
        - "packages/domain/**"           # - domain models
        - "packages/types/**"            # - типы
    - when: never                        # Иначе skip
```

### Build Dependencies Matrix

| Job | Primary Path | Shared Dependencies |
|-----|--------------|---------------------|
| build-api-gateway | `apps/api-gateway/**` | contracts, domain, types |
| build-identity | `services/identity/**` | contracts, domain, types |
| build-issuance | `services/issuance/**` | contracts, domain, types |
| build-registry | `services/registry/**` | contracts, domain, types |
| build-settlement | `services/settlement/**` | contracts, domain, types |
| build-compliance | `services/compliance/**` | contracts, domain, types |
| build-bank-nominal | `services/integrations/bank-nominal/**` | contracts, domain, types |
| build-portal-issuer | `apps/portal-issuer/**` | contracts, **sdks**, types, shared-ui |
| build-portal-investor | `apps/portal-investor/**` | contracts, **sdks**, types, shared-ui |
| build-backoffice | `apps/backoffice/**` | contracts, **sdks**, types, shared-ui |

### Gotchas

**0. API-triggered pipelines IGNORE path-based rules!** (CRITICAL)

```bash
# API trigger (glab api POST) sets before_sha = 0000000...
glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2
# → before_sha: "0000000000000000000000000000000000000000"
# → GitLab treats this as "diff = entire repo"
# → ALL jobs with changes: rules will run!

# Push trigger has real before_sha
git push origin dev-cfa2
# → before_sha: "abc123..." (previous commit)
# → GitLab computes real diff
# → Only changed paths trigger builds
```

| Trigger Method | `before_sha` | Path-based works? |
|----------------|--------------|-------------------|
| `git push` | Real SHA | YES |
| `glab api POST` | `000...` | NO (all jobs run) |
| MR pipeline | Real SHA | YES |
| Manual retry | Inherits | Depends on original |

**To test path-based rules**: Use `git push`, NOT `glab api`!

1. **Shared packages trigger many builds**
   - Change in `packages/contracts/` → ALL backend + frontend builds
   - Change in `packages/sdks/` → ALL frontend builds

2. **SDK regeneration affects frontends**
   - `generate-sdks` creates artifacts in `packages/sdks/typescript-gateway`
   - Frontends depend on these SDKs

3. **Force rebuild всего**
   ```bash
   glab api --method POST /projects/npk%2Fois-cfa/pipeline \
     -F ref=dev-cfa2 \
     -F "variables[FORCE_BUILD_ALL]=1"
   ```

4. **First deploy needs force**
   - Images `:dev` не существуют пока не собраны
   - `manifest unknown` = нужен force build

### Typical Scenarios

| Scenario | What triggers | Jobs that run |
|----------|---------------|---------------|
| Fix typo in identity service | `services/identity/` | build-identity only |
| Update OpenAPI spec | `packages/contracts/` | ALL builds (shared dep) |
| Fix portal-issuer bug | `apps/portal-issuer/` | build-portal-issuer only |
| Update shared UI component | `apps/shared-ui/` | ALL frontend builds |
| CI config change | `.gitlab/` | Nothing (no changes: rule) |

## CI Variables Reference

| Variable | Value/Source | Flags | Purpose |
|----------|--------------|-------|---------|
| SSH_PRIVATE_KEY_CFA2 | base64(id_ed25519 from cfa2) | masked, NOT protected | Deploy SSH |
| CI_REGISTRY | git.telex.global:5050 | auto | Registry host |
| CI_REGISTRY_USER | $CI_REGISTRY_USER | auto | Registry login |
| CI_REGISTRY_PASSWORD | $CI_REGISTRY_PASSWORD | auto | Registry password |
| CI_REGISTRY_IMAGE | git.telex.global:5050/npk/ois-cfa | auto | Image prefix |
| DEPLOY_TAG | dev | in .gitlab-ci | Tag for dev-cfa2 |
| FORCE_BUILD_ALL | 1 | runtime | Force all builds |
| ENABLE_SDK_JOBS | 1 | runtime | Enable SDK generation |

## Files Quick Reference

| Path | Purpose |
|------|---------|
| `repositories/customer-gitlab/ois-cfa/.gitlab/gitlab-ci.dev.yml` | CI config |
| `repositories/customer-gitlab/ois-cfa/deploy/docker-compose-at-vps/cfa2/` | Compose + env |
| `repositories/customer-gitlab/ois-cfa/ops/scripts/sync-compose-cfa2.sh` | Sync script |
| `repositories/customer-gitlab/ois-cfa/docs/deploy/vps-cfa2/` | Runbooks |
| `memory-bank/tasks/ops/cicd/OPS-001-*.md` | Stories/Epic |
| `.env` (root) | GITLAB_USER_CICD_TOKEN |

## Workflow: Typical Day

### Morning Check
```bash
# Quick status
/cicd-status

# Or manually:
glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=3' | jq '.[] | {id,status}'
```

### After Code Push
```bash
# Watch pipeline
PIPELINE_ID=XXX
while true; do
  glab api "/projects/npk%2Fois-cfa/pipelines/${PIPELINE_ID}/jobs" | jq '.[] | {name,status}'
  sleep 15
done
```

### Debug Failed Job
```bash
# Get logs
/cicd-logs {JOB_ID}

# Or:
glab api '/projects/npk%2Fois-cfa/jobs/{JOB_ID}/trace' | tail -100
```

### Verify Deploy
```bash
ssh cfa2 "cd /srv/cfa && docker compose ps"
curl -s http://92.51.38.126:58081/swagger | head -1
```

## Related Commands

- `/cicd-status` - Check pipelines, runners, variables
- `/cicd-run` - Trigger pipeline
- `/cicd-vars` - Manage CI variables
- `/cicd-logs` - Get job logs

## Related Docs

- `memory-bank/tasks/ops/cicd/OPS-001-CICD.epic.md` - Epic overview
- `memory-bank/tasks/ops/cicd/OPS-001-001-*.story.md` - PHASE0 story
- `memory-bank/tasks/ops/cicd/OPS-001-002-*.story.md` - PHASE1 story
- `docs/deploy/vps-cfa2/cfa2-dev-runbook.md` - Runbook

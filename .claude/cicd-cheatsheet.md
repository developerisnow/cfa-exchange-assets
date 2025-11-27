---
created: 2025-11-27 14:00
updated: 2025-11-27 14:00
type: cheatsheet
version: 1.0.0
---

# CI/CD Cheatsheet for ois-cfa

## Setup (Run Once Per Session)

```bash
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/.env | cut -d= -f2-)
```

## Pipelines

| Action | Command |
|--------|---------|
| List last 5 | `glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=5' \| jq '.[] \| {id,status}'` |
| Trigger new | `glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2` |
| Force all builds | `glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2 -F "variables[FORCE_BUILD_ALL]=1"` |
| With SDK jobs | `glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2 -F "variables[ENABLE_SDK_JOBS]=1"` |
| Cancel | `glab api --method POST '/projects/npk%2Fois-cfa/pipelines/{ID}/cancel'` |

## Jobs

| Action | Command |
|--------|---------|
| List jobs | `glab api '/projects/npk%2Fois-cfa/pipelines/{PIPELINE_ID}/jobs' \| jq '.[] \| {id,name,status}'` |
| Get logs | `glab api '/projects/npk%2Fois-cfa/jobs/{JOB_ID}/trace' \| tail -50` |
| Retry job | `glab api --method POST '/projects/npk%2Fois-cfa/jobs/{JOB_ID}/retry'` |

## Variables

| Action | Command |
|--------|---------|
| List all | `glab api /projects/npk%2Fois-cfa/variables \| jq '.[] \| {key,protected,masked}'` |
| Check one | `glab api /projects/npk%2Fois-cfa/variables \| jq '.[] \| select(.key=="VAR_NAME")'` |
| Unprotect | `glab api --method PUT /projects/npk%2Fois-cfa/variables/VAR_NAME -F "protected=false" -F "masked=true" -F "environment_scope=*"` |

## Runners

| Action | Command |
|--------|---------|
| Check vds1 | `glab api '/projects/npk%2Fois-cfa/runners' \| jq '.[] \| select(.tag_list[] == "vds1")'` |

## Deploy Verification (cfa2)

| Action | Command |
|--------|---------|
| Check containers | `ssh cfa2 "cd /srv/cfa && docker compose ps"` |
| Service logs | `ssh cfa2 "cd /srv/cfa && docker compose logs --tail=20 {SERVICE}"` |
| Swagger check | `curl -s http://92.51.38.126:58081/swagger \| head -1` |

## Ports (cfa2: 92.51.38.126)

| Service | Port | Service | Port |
|---------|------|---------|------|
| api-gateway | 58081 | keycloak | 58080 |
| identity | 58082 | postgres | 55432 |
| issuance | 58083 | redis | 56379 |
| registry | 58084 | minio | 59000 |
| settlement | 58085 | portal-issuer | 3001 |
| compliance | 58086 | portal-investor | 3002 |
| bank-nominal | - | backoffice | 3003 |

## Common Fixes

| Problem | Fix |
|---------|-----|
| SSH key empty | `/cicd-vars unprotect SSH_PRIVATE_KEY_CFA2` |
| Builds skipped | Add `-F "variables[FORCE_BUILD_ALL]=1"` to trigger |
| SDK stage fails | Don't include `ENABLE_SDK_JOBS` or fix specs |
| Manifest unknown | Run force build first to create `:dev` images |

## Slash Commands

- `/cicd-status` - pipelines, runners, variables
- `/cicd-run` - trigger pipeline
- `/cicd-vars` - manage variables
- `/cicd-logs` - get job logs

## Key Files

```
.gitlab/gitlab-ci.dev.yml          # CI config
deploy/docker-compose-at-vps/cfa2/ # Compose for cfa2
ops/scripts/sync-compose-cfa2.sh   # Sync to cfa2
docs/deploy/vps-cfa2/              # Runbooks
```

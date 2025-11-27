---
name: cicd-logs
description: Get GitLab CI job logs and traces
---

Get logs/trace from GitLab CI jobs for debugging.

**Usage:**
- `/cicd-logs` - get logs from last failed job in latest pipeline
- `/cicd-logs 2880` - get logs from specific job ID
- `/cicd-logs deploy` - get logs from deploy-cfa2 job in latest pipeline

**Commands:**

```bash
cd /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets

# Setup env
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' .env | cut -d= -f2-)

# Get latest pipeline ID
PIPELINE_ID=$(glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=1' | jq '.[0].id')

# List jobs in pipeline
glab api "/projects/npk%2Fois-cfa/pipelines/${PIPELINE_ID}/jobs" | jq '.[] | {id,name,status}'

# Get failed job ID
FAILED_JOB=$(glab api "/projects/npk%2Fois-cfa/pipelines/${PIPELINE_ID}/jobs" | jq '.[] | select(.status=="failed") | .id' | head -1)

# Get job trace (last 100 lines)
glab api "/projects/npk%2Fois-cfa/jobs/${JOB_ID}/trace" | tail -n 100

# Get specific job by name (e.g., deploy-cfa2)
DEPLOY_JOB=$(glab api "/projects/npk%2Fois-cfa/pipelines/${PIPELINE_ID}/jobs" | jq '.[] | select(.name=="deploy-cfa2") | .id')
glab api "/projects/npk%2Fois-cfa/jobs/${DEPLOY_JOB}/trace" | tail -n 100
```

**Common error patterns:**

| Error | Cause | Fix |
|-------|-------|-----|
| `SSH_PRIVATE_KEY_CFA2 is empty` | Variable protected or missing | `/cicd-vars unprotect SSH_PRIVATE_KEY_CFA2` |
| `ssh-add failed` | Key format wrong | Re-upload key as base64 or raw |
| `manifest unknown` | Image not built yet | Run with FORCE_BUILD_ALL=1 |
| `generate-sdks failed` | SDK stage failed | Disable with ENABLE_SDK_JOBS or fix specs |

**Retry failed job:**
```bash
glab api --method POST "/projects/npk%2Fois-cfa/jobs/${JOB_ID}/retry"
```

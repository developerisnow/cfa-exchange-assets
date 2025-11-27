---
name: cicd-run
description: Trigger GitLab pipeline on dev-cfa2 with optional variables
---

Trigger a new CI/CD pipeline for ois-cfa on branch `dev-cfa2`.

**Usage:**
- `/cicd-run` - trigger normal pipeline
- `/cicd-run force` - trigger with FORCE_BUILD_ALL=1 (rebuild all images)
- `/cicd-run sdk` - trigger with ENABLE_SDK_JOBS=1 (include SDK generation)
- `/cicd-run force sdk` - both flags

**Commands:**

```bash
cd /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets

# Setup env
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' .env | cut -d= -f2-)

# Normal run
glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2

# With FORCE_BUILD_ALL
glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2 -F "variables[FORCE_BUILD_ALL]=1"

# With ENABLE_SDK_JOBS
glab api --method POST /projects/npk%2Fois-cfa/pipeline -F ref=dev-cfa2 -F "variables[ENABLE_SDK_JOBS]=1"
```

**After triggering:**
1. Extract pipeline ID from response
2. Show URL to pipeline
3. Monitor jobs status with polling:
```bash
glab api '/projects/npk%2Fois-cfa/pipelines/{ID}/jobs' | jq '.[] | {name,stage,status}'
```

**Monitoring loop (optional):**
```bash
while true; do
  glab api '/projects/npk%2Fois-cfa/pipelines/{ID}/jobs' | jq '.[] | {name,status}'
  sleep 15
done
```

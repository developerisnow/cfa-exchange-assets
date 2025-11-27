---
name: cicd-status
description: Check GitLab CI/CD status - pipelines, jobs, runners, variables
---

Check the current CI/CD status for ois-cfa project on git.telex.global.

**What to check:**
1. Recent pipelines on `dev-cfa2` branch (last 3-5)
2. Jobs status if pipeline specified
3. Runner status (vds1 online?)
4. Key CI variables existence

**Commands to run:**

```bash
cd /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa

# Setup env
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets/.env | cut -d= -f2-)

# Recent pipelines
glab api '/projects/npk%2Fois-cfa/pipelines?ref=dev-cfa2&per_page=5' | jq '.[] | {id,status,created_at}'

# Runner vds1 status
glab api '/projects/npk%2Fois-cfa/runners' | jq '.[] | select(.tag_list[] == "vds1") | {id,status,active}'

# Key variables check
glab api /projects/npk%2Fois-cfa/variables | jq '.[] | select(.key | test("SSH|REGISTRY|TOKEN")) | {key,protected,masked}'
```

**Output format:**

| Pipeline | Status | Jobs | Duration |
|----------|--------|------|----------|
| #XXX | success/failed/running | X/Y green | Xm |

**If argument provided (pipeline ID):**
Show detailed jobs for that pipeline.

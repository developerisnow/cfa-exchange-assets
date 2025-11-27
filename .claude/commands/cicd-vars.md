---
name: cicd-vars
description: Manage GitLab CI/CD variables for ois-cfa project
---

Manage CI/CD variables for ois-cfa project on git.telex.global.

**Usage:**
- `/cicd-vars` - list all variables (keys + flags only, no values)
- `/cicd-vars check SSH_PRIVATE_KEY_CFA2` - check specific variable
- `/cicd-vars unprotect SSH_PRIVATE_KEY_CFA2` - remove protected flag (for dev branch access)

**Commands:**

```bash
cd /home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets

# Setup env
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN=$(grep -m1 '^GITLAB_USER_CICD_TOKEN=' .env | cut -d= -f2-)

# List all variables (safe - no values shown)
glab api /projects/npk%2Fois-cfa/variables | jq '.[] | {key,protected,masked,environment_scope}'

# Check specific variable
glab api /projects/npk%2Fois-cfa/variables | jq '.[] | select(.key=="VAR_NAME")'

# Unprotect variable (so dev-cfa2 can access it)
glab api --method PUT /projects/npk%2Fois-cfa/variables/VAR_NAME \
  -F "protected=false" \
  -F "masked=true" \
  -F "environment_scope=*"

# Create new variable
glab api --method POST /projects/npk%2Fois-cfa/variables \
  -F "key=NEW_VAR" \
  -F "value=VALUE" \
  -F "masked=true" \
  -F "protected=false" \
  -F "environment_scope=*"
```

**Key variables for ois-cfa:**

| Variable | Purpose | Should be |
|----------|---------|-----------|
| SSH_PRIVATE_KEY_CFA2 | SSH key for deploy to cfa2 | masked=true, protected=false |
| CI_REGISTRY_USER | Registry login | auto from GitLab |
| CI_REGISTRY_PASSWORD | Registry password | auto from GitLab |
| GITLAB_USER_CICD_TOKEN | glab CLI token | in .env on eywa1 |

**Warning:** Never print actual values of secrets to console!

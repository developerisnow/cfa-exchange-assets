#!/usr/bin/env bash
# Composer helper aliases/functions for code2prompt, repomix, yek.
# Source this file: `source scripts/composer-aliases.sh`

CFA_MONO_ROOT="${CFA_MONO_ROOT:-/home/user/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets}"
CFA_REPO="${CFA_REPO:-${CFA_MONO_ROOT}/repositories/customer-gitlab/ois-cfa}"
CONTEXT_DIR="${CONTEXT_DIR:-${CFA_MONO_ROOT}/memory-bank/snapshots-aggregated-context-duplicates}"
C2P_TEMPLATES_DIR="${C2P_TEMPLATES_DIR:-${HOME}/.config/code2prompt/templates}"

_ts() { date +"%Y%m%d-%H%M"; }
_ensure_ctx_dir() { mkdir -p "${CONTEXT_DIR}"; }

# ---- code2prompt contexts (baseline patterns from 20251118 runbook) ----
c2p_core_arch() {
  _ensure_ctx_dir
  local ts=$(_ts)
  code2prompt "${CFA_REPO}" \
    -O "${CONTEXT_DIR}/${ts}-code2prompt-ois-cfa-core-arch.txt" \
    -i 'docs/**' -i 'audit/**' -i 'artifacts/**' -i 'README.md' -i 'Makefile' \
    -i 'docker-compose*.yml' -i 'openapitools.json' \
    --tokens --encoding=cl100k_base
}

c2p_contracts() {
  _ensure_ctx_dir
  local ts=$(_ts)
  code2prompt "${CFA_REPO}" \
    -O "${CONTEXT_DIR}/${ts}-code2prompt-ois-cfa-contracts.txt" \
    -i 'packages/contracts/**' -i 'packages/domain/**' -i 'openapitools.json' \
    --tokens --encoding=cl100k_base
}

c2p_services_core() {
  _ensure_ctx_dir
  local ts=$(_ts)
  code2prompt "${CFA_REPO}" \
    -O "${CONTEXT_DIR}/${ts}-code2prompt-ois-cfa-services-core.txt" \
    -i 'services/**/Program.cs' -i 'services/**/*.csproj' -i 'services/**/appsettings*.json' -i 'services/**/Startup.cs' \
    -i 'apps/api-gateway/Program.cs' -i 'apps/api-gateway/*.csproj' -i 'apps/api-gateway/appsettings*.json' \
    --tokens --encoding=cl100k_base
}

c2p_tests() {
  _ensure_ctx_dir
  local ts=$(_ts)
  code2prompt "${CFA_REPO}" \
    -O "${CONTEXT_DIR}/${ts}-code2prompt-ois-cfa-tests-e2e.txt" \
    -i 'tests/**' -e 'tests/e2e-playwright/test-results/**' \
    --tokens --encoding=cl100k_base
}

# ---- code2prompt templated flows ----
c2p_commit_msg() {
  code2prompt "${CFA_REPO}" --diff -t "${C2P_TEMPLATES_DIR}/write-git-commit.hbs"
}

c2p_pr_desc() {
  local from=${1:-main}
  local to=${2:-$(git -C "${CFA_REPO}" rev-parse --abbrev-ref HEAD)}
  code2prompt "${CFA_REPO}" \
    --git-diff-branch "${from},${to}" \
    --git-log-branch "${from},${to}" \
    -t "${C2P_TEMPLATES_DIR}/write-github-pull-request.hbs"
}

# ---- repomix contexts (compressed XML for Claude/Oracle) ----
repomix_full() {
  _ensure_ctx_dir
  local ts=$(_ts)
  repomix "${CFA_REPO}" --compress --style xml --output "${CONTEXT_DIR}/${ts}-repomix-full.xml"
}

repomix_contracts() {
  _ensure_ctx_dir
  local ts=$(_ts)
  repomix "${CFA_REPO}/packages/contracts" --compress --style xml --output "${CONTEXT_DIR}/${ts}-repomix-contracts.xml"
}

repomix_token_tree() {
  repomix "${CFA_REPO}" --token-count-tree 1000
}

# ---- yek (speed/budget) ----
yek_budget() {
  _ensure_ctx_dir
  local ts=$(_ts)
  local budget=${1:-120k}
  yek "${CFA_REPO}" --tokens "${budget}" --output "${CONTEXT_DIR}/${ts}-yek-${budget}.txt"
}

# ---- helpers ----
list_composer_aliases() {
  declare -F | awk '{print $3}' | grep -E '^(c2p_|repomix_|yek_)'
}

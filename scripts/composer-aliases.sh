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

# ---- curated variants for <1MB contexts ----
c2p_core_arch_hbs() {
  _ensure_ctx_dir
  local ts=$(_ts)
  local outf="${CONTEXT_DIR}/composers/code2prompt/${ts}-code2prompt-curated.txt"
  code2prompt "${CFA_REPO}" \
    -O "${outf}" \
    -t "${CFA_MONO_ROOT}/scripts/code2prompt-curated.hbs" \
    -i 'services/issuance/**' -i 'services/registry/**' -i 'services/compliance/**' -i 'services/identity/**' \
    -i 'apps/backoffice/src/**' -i 'apps/portal-issuer/src/**' -i 'apps/portal-investor/src/**' \
    -i 'apps/api-gateway/Program.cs' -i 'apps/api-gateway/appsettings*.json' \
    -i 'packages/contracts/**' -i 'docs/deploy/**' -i 'ops/scripts/**' -i 'scripts/git/*.sh' \
    -e '**/bin/**' -e '**/obj/**' -e '**/node_modules/**'
  # prepend pruned repo tree (maxdepth 4) to aid navigation without bloat
  local tree
  tree=$(cd "${CFA_REPO}" && find . -maxdepth 4 \
    \( -path './.git' -o -path './bin' -o -path './obj' -o -path './node_modules' \
       -o -path './packages/dotnet-clients' -o -path './packages/sdks' -o -path './packages/types' \
       -o -path './artifacts' -o -path './memory-bank' \) -prune -o -type d -print | sed 's#^\./##')
  {
    echo "Repo Tree (pruned, maxdepth=4)"
    echo '```txt'
    printf '%s\n' "$tree"
    echo '```'
    echo
    cat "$outf"
  } > "${outf}.tmp" && mv "${outf}.tmp" "$outf"
}

repomix_curated() {
  _ensure_ctx_dir
  local ts=$(_ts)
  mkdir -p "${CONTEXT_DIR}/composers/repomix"
  (cd "${CFA_REPO}" && \
    find services/issuance services/registry services/compliance services/identity \
         apps/backoffice apps/portal-issuer apps/portal-investor apps/api-gateway \
         packages/contracts docs/deploy ops/scripts scripts \
         -type f \( -name '*.cs' -o -name '*.csproj' -o -name 'appsettings*.json' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.json' -o -name '*.yaml' -o -name '*.yml' -o -name '*.md' -o -name '*.sh' \) \
         ! -path '*/bin/*' ! -path '*/obj/*' ! -path '*/node_modules/*' \
    | repomix --stdin --style xml --output "${CONTEXT_DIR}/composers/repomix/${ts}-repomix-curated.xml")
}

yek_curated_fallback() {
  _ensure_ctx_dir
  local ts=$(_ts)
  mkdir -p "${CONTEXT_DIR}/composers/yek"
  local outfile="${CONTEXT_DIR}/composers/yek/${ts}-yek-curated.txt"
  (cd "${CFA_REPO}" && \
    for f in \
      services/issuance/Program.cs \
      services/issuance/Services/IssuanceService.cs \
      services/issuance/DTOs/IssuerIssuancesReportResponse.cs \
      services/registry/Program.cs \
      services/registry/Services/RegistryService.cs \
      services/compliance/Program.cs \
      services/compliance/DTOs/KycRequestDto.cs \
      services/identity/Program.cs \
      apps/backoffice/src/app/audit/page.tsx \
      apps/backoffice/src/app/audit/[id]/page.tsx \
      apps/backoffice/src/app/kyc/page.tsx \
      apps/backoffice/src/app/payouts/page.tsx \
      apps/backoffice/src/app/users/page.tsx \
      apps/portal-issuer/src/app/dashboard/page.tsx \
      apps/portal-issuer/src/app/issuances/page.tsx \
      apps/portal-issuer/src/app/issuances/[id]/page.tsx \
      apps/portal-issuer/src/app/reports/page.tsx \
      packages/contracts/openapi-gateway.yaml \
      docs/deploy/docker-compose-at-vps/02-env-and-compose.md \
      docs/deploy/docker-compose-at-vps/05-gateway.md \
      docs/deploy/docker-compose-at-vps/10-eywa1-control-plane-runbook.md \
      ops/scripts/deploy/deploy-node.sh \
      ops/scripts/deploy/provision-node.sh \
      ops/scripts/auth/fix-redirects.sh \
      ops/scripts/cloudflare-dns-upsert.sh \
      scripts/git/zip_branches.sh; do \
        [ -f \"$f\" ] || continue; \
        echo '>>>>' \"$f\"; cat \"$f\"; echo; \
      done \
  ) > \"${outfile}\"
}

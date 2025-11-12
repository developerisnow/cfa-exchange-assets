#!/usr/bin/env bash
set -euo pipefail

# Monorepo and submodules mirror setup/push helper.
# Usage:
#   scripts/git_mirror.sh setup   # ensure remotes/pushurls configured
#   scripts/git_mirror.sh push    # push submodules (on-demand) + monorepo

GH_USER=${GH_USER:-developerisnow}
MAIN_REPO=${MAIN_REPO:-cfa-exchange-assets}
VELVET_REPO=${VELVET_REPO:-cfa-velvet}
OISCFA_REPO=${OISCFA_REPO:-cfa-ois-cfa}

ROOT_GH_SSH="git@github.com:${GH_USER}/${MAIN_REPO}.git"
VELVET_GH_SSH="git@github.com:${GH_USER}/${VELVET_REPO}.git"
OISCFA_GH_SSH="git@github.com:${GH_USER}/${OISCFA_REPO}.git"

SUBS=(
  "repositories/customer-gitlab/velvet:${VELVET_GH_SSH}"
  "repositories/customer-gitlab/ois-cfa:${OISCFA_GH_SSH}"
)

ensure_pushurl() {
  local path="$1" ghurl="$2"
  local fetchurl
  fetchurl=$(git -C "$path" remote get-url origin)
  # Ensure both GitLab (fetchurl) and GitHub (ghurl) are push URLs for origin
  if ! git -C "$path" remote get-url --push origin | grep -q "$fetchurl"; then
    git -C "$path" remote set-url --add --push origin "$fetchurl"
  fi
  if ! git -C "$path" remote get-url --push origin | grep -q "$ghurl"; then
    git -C "$path" remote set-url --add --push origin "$ghurl"
  fi
}

setup() {
  # Root: add alex remote and mirror pushurl
  git config push.recurseSubmodules on-demand
  if ! git remote | grep -qx alex; then
    git remote add alex "$ROOT_GH_SSH" || true
  fi
  # Add GH as additional pushurl on origin
  if ! git remote get-url --push origin | grep -q "$ROOT_GH_SSH"; then
    git remote set-url --add --push origin "$ROOT_GH_SSH"
  fi

  # Submodules: ensure alex remote and pushurls
  for entry in "${SUBS[@]}"; do
    local path="${entry%%:*}" ghurl="${entry##*:}"
    if git -C "$path" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      if ! git -C "$path" remote | grep -qx alex; then
        git -C "$path" remote add alex "$ghurl" || true
      fi
      ensure_pushurl "$path" "$ghurl"
    fi
  done
}

push_all() {
  # Push submodules first so superproject refs are valid remotely
  for entry in "${SUBS[@]}"; do
    local path="${entry%%:*}"
    if git -C "$path" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      (cd "$path" && git fetch --all --tags && git push origin --all && git push origin --tags) || true
    fi
  done
  # Push monorepo (origin has pushurl to alex)
  git fetch --all --tags || true
  git push origin --all || true
  git push origin --tags || true
}

case "${1:-}" in
  setup) setup ;;
  push)  push_all ;;
  *)
    echo "Usage: $0 {setup|push}" >&2
    exit 2
    ;;
esac


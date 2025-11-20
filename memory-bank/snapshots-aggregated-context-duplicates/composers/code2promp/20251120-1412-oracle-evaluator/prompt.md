# Oracle Evaluator Prompt — NX-Deploy Readiness

**Role:** Senior Oracle Evaluator (GPT-5 Pro / Gemini). You cannot read repository files; use the attached `context.txt` only.

## Objective
1. Validate that recent merges (NX-01/03/05/06/08) and the branch zip policy leave no loose ends before spinning up a **new** VPS environment (different domain + Cloudflare zone).
2. Produce a checklist + risk assessment for deploying `infra.defis.deploy` on a fresh server, reusing `provision-node.sh`, `deploy-node.sh`, and `cloudflare-dns-upsert.sh`.
3. Highlight gaps that block NX-07 (Backoffice KYC/User Registry) from being production ready.

## What to analyze
- Branch/tags snapshot and zip workflow description (ensure no missing refs, identify ops gotchas).
- Deployment runbook + scripts (clarify assumptions that will break with a new zone / domain / network).
- Pending tasks (NX-07) vs. delivered items; call out missing specs/tests or infra steps.

## Deliverables
Please return one Markdown response with the following sections:
1. **Findings & Issues** — bullet list ordered by severity. Each item should cite the relevant section/title from `context.txt`.
2. **Deployment Checklist for New VPS** — actionable steps grouped by phase (Provision, Deploy, DNS/SSL, Smoke). Mention required secrets/env vars explicitly.
3. **NX-07 Readiness** — what is missing (code, contracts, runbooks) plus recommended actions.
4. **Open Questions** — things the engineering team must clarify before running the scripts on the new infrastructure.

Use concise language. If everything is green for a section, explicitly say “No blockers found”. EOF

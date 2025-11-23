---
created: 2025-11-23 12:45
updated: 2025-11-23 12:45
type: analysis
sphere: [devops]
topic: [git, changes, uncategorized]
author: alex-a (scripted by co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [git-report, uncategorized]
---

# Git changes — uncategorized

Диапазон: 2025-11-17 .. 2025-11-21

## Files

- A .claude/agents/project-guard-architect.prompt.md

- A .claude/agents/project-guard-architect.yaml

- A .claude/commands/README.md

- M .gitignore

- A ARCHIVE/examples-daily-reports/Daily-Report-2025-11-15-Ivan-Petrov.md

- A "ARCHIVE/examples-daily-reports/Daily_Report_\342\200\224_YYYY_MM_DD_\342\200\224_Developer_Name_.md"

- A ARCHIVE/examples-daily-reports/daily-report.md

- M Makefile

- A artifacts/AleksandrO/ISSUANCE-SYSTEM-VERIFICATION-GUIDE.md

- A artifacts/AlexA/ois-cfa.reposcan.json

- A artifacts/AlexA/org/reports/20251118-2345-Alex-A.daily.report.md

- A artifacts/AlexA/org/reports/20251119-2359-Alex-A.daily.report.md

- A artifacts/AlexA/org/reports/20251120-0800-Night-Shift.daily.report.md

- A artifacts/AlexA/project-C4.diagram.md

- A artifacts/AlexA/project-reposcan.md

- A artifacts/FRONTEND-FUNCTIONALITY-ANALYSIS.md

- A artifacts/FRONTEND-STARTUP.md

- A artifacts/KEYCLOAK-SETUP-GUIDE.md

- A artifacts/KEYCLOAK-SETUP.md

- A artifacts/OBSERVABILITY-SECURITY-ACCESS.md

- A artifacts/gateway-routing-report.md

- A artifacts/git/branch-zip-20251120.txt

- A artifacts/git/branch-zip-workflow.md

- A artifacts/issuance-endpoints-coverage-report.md

- A artifacts/issuance-test-report.txt

- A artifacts/registry-flow-report.md

- A artifacts/spec-lint-openapi.txt

- A artifacts/spec-validate-asyncapi.txt

- A artifacts/spec-validate-jsonschema.txt

- A artifacts/tests/e2e/playwright/20251119-1757-p88mwt-backoffice-login-success.e2e.png

- A artifacts/tests/e2e/playwright/20251119-1757-p88mwt-investor-self-registration-flow-completed.e2e.png

- A artifacts/tests/e2e/playwright/20251119-1757-que8af-investor-login-success.e2e.png

- A artifacts/tests/e2e/playwright/20251119-1757-que8af-issuer-login-success.e2e.png

- M docker-compose.apps.yml

- A docker-compose.keycloak-proxy.yml

- M docker-compose.services.yml

- M docker-compose.yml

- A docs/context/FRONTEND-CONTEXT.md

- M docs/context/PROJECT-CONTEXT.md

- A docs/context/PROMPTS-MAP.md

- A docs/context/RULES-SUMMARY.md

- A docs/deploy/MULTI_ACCOUNT_SETUP.md

- M docs/deploy/docker-compose-at-vps/02-env-and-compose.md

- M docs/deploy/docker-compose-at-vps/06-keycloak.md

- M docs/deploy/docker-compose-at-vps/07-frontends-dev-on-vps.md

- A docs/deploy/docker-compose-at-vps/10-eywa1-control-plane-runbook.md

- A global.json

- M memory-bank

- A ops/keycloak/nginx.conf

- M packages/contracts/openapi-gateway.yaml

- A services/issuance/issuance.Tests/README.md

- A services/issuance/issuance.Tests/artifacts/issuance-test-report.txt

- A tasks/.ai-memory-task

- A tasks/NX-01-spec-validate-and-matrix.md

- A tasks/NX-02-gateway-routing-and-health.md

- A tasks/NX-03-issuance-endpoints-coverage.md

- A tasks/NX-04-registry-orders-flow.md

- A tasks/NX-05-issuer-dashboard-and-reports.md

- A tasks/NX-06-issuer-payout-schedule-spec-and-ui.md

- A tasks/NX-06-payout-schedule-SPEC-DIFF.md

- A tasks/NX-07-backoffice-kyc-and-user-registry.md

- A tasks/NX-08-backoffice-audit-log-ui.md

- A tests/e2e-playwright/package-lock.json

- M tests/e2e-playwright/tests/backoffice-auth.spec.ts

- M tests/e2e-playwright/tests/public-auth.spec.ts

- M tests/e2e-playwright/tests/self-registration.spec.ts

- A tests/e2e-playwright/tests/utils/flow-screenshot.ts

- A tests/issuance.Tests/artifacts/issuance-test-report.txt


## Commits (oneline)

```
0a4ead1 docs(nx): [co-c02b] - record cfa1 verification results (gateway 404s)
7e07898 docs(nx): [co-c02b] - add DoD checkboxes with domain/time placeholders
f0bf58f docs(nx): [co-c02b] - refresh NX05-08 checklists and routes
23d16df docs(tasks) Aleksandr O author
ca9fc5a chore(tests): [co-c02b] - record issuance api test run
34bf2ad chore(tests): [co-c02b] - align issuance test project and log run
2a20608 docs(nx-07): [co-c02b] - note current kyc/identity endpoints
647384d chore(docs): [co-c02b] - add telex examples and test note
bcc82f2 feat(nx-07): [co-c02b] - align kyc/identity apis
41e09cd docs(nx): mark current state and gaps for nx03/05/06/08
dde6cce chore(deploy): add DEPLOY_FIX_PERMS flag to avoid npm/pm2 EACCES
903bb39 fix(nx-05): remove mock issuer ids and disable retries
5c59ef3 fix(nx-07): expose kyc/audit/identity routes via gateway
8760f69 fix(nx-07): align backoffice kyc/api mocks
9476b4e fix(auth): [co-7b1b] - Pass realm env into keycloak exec
cd086de chore(ops): [co-7b1b] - Version keycloak sidecar nginx config
43eb2d7 chore(ops): [co-7b1b] - Avoid host port clashes for keycloak proxy
e1ecf3a chore(dotnet): [co-7b1b] - Align SDK with container image
16a4a87 chore(ops): [co-7b1b] - Version keycloak proxy compose
e0ddda1 fix(ops): [co-7b1b] - Normalize deploy permissions
ee1de2b fix(ops): [co-7b1b] - stabilize cfa1 permissions and keycloak redirects • Add sudo chown step in deploy-node to avoid npm EACCES on target • Add auth/fix-redirects.sh to align rootUrl/redirectUris/webOrigins for cfa1 portals agentID=019a9c47-7b1b-7112-9672-694674728b0e
1fe0940 chore: remove claude skills directory
15817ca docs(skill): clarify oracle evaluator packaging
b39284e docs(skill): oracle evaluator context packaging
01f8937 docs(git): add branch zip workflow and helper script
86ae12a Merge remote-tracking branch 'origin/feature/NX-08-backoffice-audit' into infra.defis.deploy
fa41e2b Merge remote-tracking branch 'origin/feature/NX-06-payout-schedule' into infra.defis.deploy
fce8031 Merge remote-tracking branch 'origin/tasks/NX-05-issuer-dashboard-and-reports' into infra.defis.deploy
1787d46 Merge remote-tracking branch 'origin/fix/NX-03-issuance-500' into infra.defis.deploy
d5ccea0 fix(nx-03): stabilize issuance publish 404 handling
c239e7c fix(nx-03): handle non-existent issuance gracefully (404 instead of 500)
3865491 feat(nx-08): [co-c02b] - Audit Log UI
3ad315e docs(daily): night shift progress report
4c3b07e feat(nx-06): [co-c02b] - Payout Schedule Spec & UI
8f54f89 feat(nx05-dashboard): [co-c02b] - Wire issuer reports
dc56cc9 docs(report)
7cdcdde Merge branch 'tasks/NX-01-spec-validate-and-matrix' of git.telex.global:npk/ois-cfa into tasks/NX-01-spec-validate-and-matrix
eb56f4c docs(report)
4de1597 ops(cloudflare): [co-7b1b] - add multi-account DNS upsert helper • Introduce cloudflare-dns-upsert.sh script that reads per-env configs and upserts A-records • Extend MULTI_ACCOUNT_SETUP runbook with usage examples for cfa1 and fin2/cfa2 agentID=019a9c47-7b1b-7112-9672-694674728b0e
73b90aa docs(ops): [co-7b1b] - finalize cfa1 status and update control-plane runbooks • Mark cfa1 control-plane/backend/frontend readiness in eywa1 runbook and add troubleshooting notes • Document multi-account Cloudflare/domains strategy and hint about permissions in deploy-node script agentID=019a9c47-7b1b-7112-9672-694674728b0e
1475616 test(e2e): [co-7b1b] - add flow screenshots for playwright login and registration • Add helper to store flow screenshots under artifacts/tests/e2e/playwright with timestamp and run id • Wire issuer/investor/backoffice and self-registration flows to capture final screenshots on success agentID=019a9c47-7b1b-7112-9672-694674728b0e
2a1c7b9 docs(tasks) NX-05 v2
1048c29 docs(ops): [co-7b1b] - refine eywa1 control-plane DoD for cfa1/fin2 • Align DoD with docker-compose-at-vps 00–09 and multi-node environments • Clarify DNS/TLS/nginx and NX-05/06 readiness criteria for cfa1 and fin2 agentID=019a9c47-7b1b-7112-9672-694674728b0e
baf8d7d fix(ops): [co-7b1b] - add deploy user to docker group • Ensure provisioned user is added to docker group for compose access • Prevent docker permission denied errors in deploy tmux session agentID=019a9c47-7b1b-7112-9672-694674728b0e
06a4f7d fix(ops): [co-7b1b] - enable ssh access and git agent forwarding • Copy root authorized_keys to provisioned user for passwordless SSH • Enable SSH agent forwarding for git operations on target nodes agentID=019a9c47-7b1b-7112-9672-694674728b0e
5d3c6f5 ai(claude) skill composers
27c6bfc Merge branch 'tasks/NX-01-spec-validate-and-matrix' of git.telex.global:npk/ois-cfa into tasks/NX-01-spec-validate-and-matrix
c1c98b4 chore
ef1ca9f Merge branch 'tasks/NX-01-spec-validate-and-matrix' of git.telex.global:npk/ois-cfa into tasks/NX-01-spec-validate-and-matrix
5c79519 ai(claude) skill composers
dc83eec feat(ops): [co-7b1b] - Eywa1 control-plane runbook and deploy scripts • Add eywa1 multi-VPS control-plane runbook under docker-compose-at-vps • Add provision/deploy script scaffolds for OIS-CFA VPS nodes via eywa1 agentID=019a9c47-7b1b-7112-9672-694674728b0e
a0e9c93 Merge branch 'infra.defis.deploy' into tasks/NX-01-spec-validate-and-matrix
7ed409d ai(skill) composer clis
8c81968 docs(reports)
c06961f feat(nx-04): [co-76ca] - Implement registry order flow events and tests
47d4a8b tests(nx-03): [co-76ca] - Run issuance tests and add coverage report
5f3e01d docs(nx-02): [co-76ca] - Add check-health target and recheck gateway routing
5c7f26b docs(nx-01): [co-76ca] - Revalidate specs and API/Event matrix
f731270 docs(architecture) C4 diagrams mermaidjs and reposcan v1.0
b6e5628 docs(reports) examples
68e281b chore
d1d9228 docs(ai) ai drafts
2789f57 Merge branch 'infra' of git.telex.global:npk/ois-cfa into infra.defis.deploy
450eec8 add context + NX-task
```
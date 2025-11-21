---
created: 2025-11-21 14:32
updated: 2025-11-21 14:32
type: analysis
sphere: [devops]
topic: [git, changes, architecture-branches]
author: alex-a (scripted by co-76ca)
agentID: co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [git-report, architecture-branches]
---

# Git changes — architecture-branches

Диапазон: 2025-11-17 .. 2025-11-21

## Files

- (нет файлов)


## Commits (oneline)

```
6930d7c fix(backoffice-auth): [co-76ca] - add secret + kyc/audit e2e
0a584c9 fix(cfa1): [co-76ca] - restore portal builds and kc note
d5dd53c deploy(cfa1) deploy and test on cfa1 WIP
fd2cbb6 docs(tasks)
24a00d6 docs(nx): [co-c02b] - add status blocks and cfa1 verification notes
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
```
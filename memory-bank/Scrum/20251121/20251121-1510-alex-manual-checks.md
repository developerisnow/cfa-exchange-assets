# Bash
```bash
[11:04] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy+) $ git log -1
commit 24a00d602d17ff7f75417eb1ec38212480d3ff71 (HEAD -> infra.defis.deploy, origin/infra.defis.deploy, origin/develop)
Author: Your Name <you@example.com>
Date:   Fri Nov 21 09:58:33 2025 +0000

    docs(nx): [co-c02b] - add status blocks and cfa1 verification notes

    • Status 2025-11-21 for NX03/05/06/07/08 plus cfa1 404 findings

    agentID=co-c02b-eywa1
[11:04] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy+) $ git status
On branch infra.defis.deploy
Your branch is up to date with 'origin/infra.defis.deploy'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   apps/api-gateway/appsettings.json
        modified:   docker-compose.apps.yml
        modified:   docker-compose.services.yml
        modified:   docker-compose.yml
        modified:   services/settlement/Program.cs
        modified:   tasks/NX-05-issuer-dashboard-and-reports.md
        modified:   tasks/NX-06-issuer-payout-schedule-spec-and-ui.md
        modified:   tasks/NX-07-backoffice-kyc-and-user-registry.md
        modified:   tasks/NX-08-backoffice-audit-log-ui.md

no changes added to commit (use "git add" and/or "git commit -a")
[11:45] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy+) $ git add tasks/ && git commit -m "docs(tasks)" && git push
[infra.defis.deploy fd2cbb6] docs(tasks)
 4 files changed, 15 insertions(+), 15 deletions(-)
Enumerating objects: 13, done.
Counting objects: 100% (13/13), done.
Delta compression using up to 4 threads
Compressing objects: 100% (7/7), done.
Writing objects: 100% (7/7), 1.35 KiB | 1.35 MiB/s, done.
Total 7 (delta 6), reused 0 (delta 0), pack-reused 0
remote:
remote: View merge request for infra.defis.deploy:
remote:   https://git.telex.global/npk/ois-cfa/-/merge_requests/5
remote:
To git.telex.global:npk/ois-cfa.git
   24a00d6..fd2cbb6  infra.defis.deploy -> infra.defis.deploy
[11:45] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy+) $ git add . && git commit -m "deploy(cfa1) deploy and test on cfa1 WIP" && git push
[infra.defis.deploy d5dd53c] deploy(cfa1) deploy and test on cfa1 WIP
 5 files changed, 59 insertions(+), 30 deletions(-)
Enumerating objects: 21, done.
Counting objects: 100% (21/21), done.
Delta compression using up to 4 threads
Compressing objects: 100% (11/11), done.
Writing objects: 100% (11/11), 1.49 KiB | 1.49 MiB/s, done.
Total 11 (delta 10), reused 0 (delta 0), pack-reused 0
remote:
remote: View merge request for infra.defis.deploy:
remote:   https://git.telex.global/npk/ois-cfa/-/merge_requests/5
remote:
To git.telex.global:npk/ois-cfa.git
   fd2cbb6..d5dd53c  infra.defis.deploy -> infra.defis.deploy

[11:46] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'PM2_HOME=/home/user/.pm2 pm2 list --no-color'
┌────┬────────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name               │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 2  │ backoffice         │ default     │ N/A     │ fork    │ 200107   │ 49m    │ 3    │ online    │ 0%       │ 33.3mb   │ user     │ disabled │
│ 1  │ portal-investor    │ default     │ N/A     │ fork    │ 200100   │ 49m    │ 3    │ online    │ 0%       │ 33.1mb   │ user     │ disabled │
│ 0  │ portal-issuer      │ default     │ N/A     │ fork    │ 200093   │ 49m    │ 3    │ online    │ 0%       │ 33.8mb   │ user     │ disabled │
└────┴────────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[12:10] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'PM2_HOME=/home/user/.pm2 pm2 describe portal-issuer --no-color | sed -n "1,80p"'
 Describing process with id 0 - name portal-issuer
┌───────────────────┬──────────────────────────────────────────────┐
│ status            │ online                                       │
│ name              │ portal-issuer                                │
│ namespace         │ default                                      │
│ version           │ N/A                                          │
│ restarts          │ 3                                            │
│ uptime            │ 49m                                          │
│ script path       │ /usr/bin/npm                                 │
│ script args       │ run dev                                      │
│ error log path    │ /home/user/.pm2/logs/portal-issuer-error.log │
│ out log path      │ /home/user/.pm2/logs/portal-issuer-out.log   │
│ pid path          │ /home/user/.pm2/pids/portal-issuer-0.pid     │
│ interpreter       │ /usr/bin/node                                │
│ interpreter args  │ N/A                                          │
│ script id         │ 0                                            │
│ exec cwd          │ /opt/ois-cfa/apps/portal-issuer              │
│ exec mode         │ fork_mode                                    │
│ node.js version   │ 20.19.5                                      │
│ node env          │ N/A                                          │
│ watch & reload    │ ✘                                            │
│ unstable restarts │ 0                                            │
│ created at        │ 2025-11-21T11:20:40.286Z                     │
└───────────────────┴──────────────────────────────────────────────┘
 Actions available
┌────────────────────────┐
│ km:heapdump            │
│ km:cpu:profiling:start │
│ km:cpu:profiling:stop  │
│ km:heap:sampling:start │
│ km:heap:sampling:stop  │
└────────────────────────┘
 Trigger via: pm2 trigger portal-issuer <action_name>

 Code metrics value
┌────────────────────────┬──────────┐
│ Used Heap Size         │ 7.76 MiB │
│ Heap Usage             │ 84.08 %  │
│ Heap Size              │ 9.23 MiB │
│ Event Loop Latency p95 │ 1.56 ms  │
│ Event Loop Latency     │ 0.58 ms  │
│ Active handles         │ 5        │
│ Active requests        │ 0        │
└────────────────────────┴──────────┘
 Divergent env variables from local env
┌────────────────┬────────────────────────────────────┐
│ SSH_CONNECTION │ 65.108.157.9 46312 87.249.49.56 22 │
│ XDG_SESSION_ID │ 409                                │
│ SSH_CLIENT     │ 65.108.157.9 46312 22              │
└────────────────┴────────────────────────────────────┘

 Add your own code metrics: http://bit.ly/code-metrics
 Use `pm2 logs portal-issuer [--lines 1000]` to display logs
 Use `pm2 env 0` to display environment variables
 Use `pm2 monit` to monitor CPU and Memory usage portal-issuer
[12:10] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $
[12:10] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'cd /opt/ois-cfa && git rev-parse HEAD && git status -sb'
fatal: not a git repository (or any of the parent directories): .git
[12:10] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'cd /srv/cfa/ois-cfa && git rev-parse HEAD && git status -sb'
24a00d602d17ff7f75417eb1ec38212480d3ff71
## infra.defis.deploy
[12:11] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'cd /opt/ois-cfa/apps/portal-issuer && npm ls @ois/shared-ui || echo "MISSING"'
@ois/portal-issuer@0.1.0 /opt/ois-cfa/apps/portal-issuer
└── (empty)

MISSING
[12:11] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'cd /opt/ois-cfa/apps/portal-investor && npm ls web-vitals || echo "MISSING"'
@ois/portal-investor@0.1.0 /opt/ois-cfa/apps/portal-investor
└── (empty)

MISSING
[12:11] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $ ssh user@cfa1 'docker exec ois-postgres psql -U ois -d keycloak -c "select username from user_entity where username = '\''alexabook1'\'';"'
  username
------------
 alexabook1
(1 row)

[12:11] user@eywa-ubuntu-8gb-hel1-2 ois-cfa (infra.defis.deploy) $

```
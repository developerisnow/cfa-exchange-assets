# Bash
```bash
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
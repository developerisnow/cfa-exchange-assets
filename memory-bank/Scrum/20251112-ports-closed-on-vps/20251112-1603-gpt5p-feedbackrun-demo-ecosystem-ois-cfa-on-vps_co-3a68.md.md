
• Explored
  └ Search bootstrap|kcadm|realm|redirect|clients|portal-issuer|portal-investor|backoffice in ops
    Read bootstrap-realm.sh

• Edited ~/__Repositories/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa/ops/keycloak/bootstrap-realm.sh (+28 -18)
     6  KC_PASS=${KC_PASS:-admin123}
     7 -REALM=${REALM:-ois}
     7 +# Use local-dev realm name per docs
     8 +REALM=${REALM:-ois-dev}
     9
     9 -ISSUER_URL=${ISSUER_URL:-http://87.249.49.56:53001}
    10 -INVESTOR_URL=${INVESTOR_URL:-http://87.249.49.56:53002}
    11 -BACKOFFICE_URL=${BACKOFFICE_URL:-http://87.249.49.56:53003}
    12 -# Опционально добавить локальные туннельные адреса для редиректов
    13 -ISSUER_TUNNEL_URL=${ISSUER_TUNNEL_URL:-http://localhost:155101}
    14 -INVESTOR_TUNNEL_URL=${INVESTOR_TUNNEL_URL:-http://localhost:155102}
    15 -BACKOFFICE_TUNNEL_URL=${BACKOFFICE_TUNNEL_URL:-http://localhost:155103}
    16 -CLIENT_SECRET=${CLIENT_SECRET:-secret}
    10 +# Public app URLs (dev): local ports
    11 +ISSUER_URL=${ISSUER_URL:-http://localhost:3001}
    12 +INVESTOR_URL=${INVESTOR_URL:-http://localhost:3002}
    13 +BACKOFFICE_URL=${BACKOFFICE_URL:-http://localhost:3003}
    14 +# Optional tunnel addresses for mac SSH tunnels
    15 +ISSUER_TUNNEL_URL=${ISSUER_TUNNEL_URL:-http://localhost:15301}
    16 +INVESTOR_TUNNEL_URL=${INVESTOR_TUNNEL_URL:-http://localhost:15302}
    17 +BACKOFFICE_TUNNEL_URL=${BACKOFFICE_TUNNEL_URL:-http://localhost:15303}
    18
       ⋮
    27
    27 -create_client() {
    28 +ensure_client_public() {
    29    local cid=$1
       ⋮
    31    local tunnel_url=$3
    31 -  local id=$(${KCADM} create clients -r ${REALM} -s clientId=${cid} -s enabled=true -s protocol=openid-connect -s publicClient=false -s 'redirectUris=["'${url}'/*","'${tunnel_url}'/*"]'
        -s 'webOrigins=["*"]' -i)
    32 -  ${KCADM} update clients/${id}/client-secret -r ${REALM} -s value=${CLIENT_SECRET}
    32 +  local rid
    33 +  rid=$(${KCADM} get clients -r ${REALM} -q clientId=${cid} | sed -n 's/.*"id"\s*:\s*"\([^"]*\)".*/\1/p' | head -1 || true)
    34 +  if [ -z "${rid:-}" ]; then
    35 +    rid=$(${KCADM} create clients -r ${REALM} -s clientId=${cid} -s enabled=true -s protocol=openid-connect -i)
    36 +  fi
    37 +  ${KCADM} update clients/${rid} -r ${REALM} \
    38 +    -s publicClient=true \
    39 +    -s directAccessGrantsEnabled=true \
    40 +    -s standardFlowEnabled=true \
    41 +    -s 'redirectUris=["'${url}'/*","'${tunnel_url}'/*"]' \
    42 +    -s 'webOrigins=["'${url}'","'${tunnel_url}'"]'
    43  }
    44
    35 -create_client portal-issuer ${ISSUER_URL} ${ISSUER_TUNNEL_URL}
    36 -create_client portal-investor ${INVESTOR_URL} ${INVESTOR_TUNNEL_URL}
    37 -create_client backoffice ${BACKOFFICE_URL} ${BACKOFFICE_TUNNEL_URL}
    45 +ensure_client_public portal-issuer ${ISSUER_URL} ${ISSUER_TUNNEL_URL}
    46 +ensure_client_public portal-investor ${INVESTOR_URL} ${INVESTOR_TUNNEL_URL}
    47 +ensure_client_public backoffice ${BACKOFFICE_URL} ${BACKOFFICE_TUNNEL_URL}
    48
       ⋮
    50  if ! ${KCADM} get users -r ${REALM} -q username=investor >/dev/null 2>&1; then
    41 -  uid=$(${KCADM} create users -r ${REALM} -s username=investor -s enabled=true -i)
    51 +  uid=$(${KCADM} create users -r ${REALM} -s username=investor@test.com -s email=investor@test.com -s emailVerified=true -s enabled=true -i)
    52    ${KCADM} set-password -r ${REALM} --userid ${uid} --new-password Passw0rd!
       ⋮
    54  if ! ${KCADM} get users -r ${REALM} -q username=issuer >/dev/null 2>&1; then
    45 -  uid=$(${KCADM} create users -r ${REALM} -s username=issuer -s enabled=true -i)
    55 +  uid=$(${KCADM} create users -r ${REALM} -s username=issuer@test.com -s email=issuer@test.com -s emailVerified=true -s enabled=true -i)
    56    ${KCADM} set-password -r ${REALM} --userid ${uid} --new-password Passw0rd!
       ⋮
    58  if ! ${KCADM} get users -r ${REALM} -q username=backoffice >/dev/null 2>&1; then
    49 -  uid=$(${KCADM} create users -r ${REALM} -s username=backoffice -s enabled=true -i)
    59 +  uid=$(${KCADM} create users -r ${REALM} -s username=admin@test.com -s email=admin@test.com -s emailVerified=true -s enabled=true -i)
    60    ${KCADM} set-password -r ${REALM} --userid ${uid} --new-password Passw0rd!

• Ran cd repositories/customer-gitlab/ois-cfa && git add ops/keycloak/bootstrap-realm.sh && git commit -m $'fix(keycloak): [co-3a68] - Bootstrap: use realm ois-dev + PUBLIC clients\n• Correct
  │ tunnel URLs 15301/15302/15303\n• Make clients public, set redirectUris + webOrigins\n• Create demo users with emails\nagentID=co-3a68' && git push origin deploy
  └ [deploy 87ae110] fix(keycloak): [co-3a68] - Bootstrap: use realm ois-dev + PUBLIC clients • Correct tunnel URLs 15301/15302/15303 • Make clients public, set redirectUris + webOrigins •
    Create demo users with emails agentID=co-3a68
     1 file changed, 29 insertions(+), 19 deletions(-)
    … +4 lines
    To git.telex.global:npk/ois-cfa.git
       7b7994b..87ae110  deploy -> deploy

• Ran ssh cfa1 '
  │ set -e
  │ cd /opt/ois-cfa
  │ … +19 lines
  └ ERROR:  column "keycloak" does not exist
    LINE 1: SELECT 1 FROM pg_database WHERE datname = keycloak
                                                      ^
    ERROR:  database "keycloak" already exists

• Ran ssh cfa1 '
  │ set -e
  │ cd /opt/ois-cfa
  │ … +14 lines
  └ time="2025-11-12T12:45:36Z" level=warning msg="/opt/ois-cfa/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion"
    time="2025-11-12T12:45:36Z" level=warning msg="/opt/ois-cfa/docker-compose.override.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential
    confusion"
    … +198 lines
        "post.logout.redirect.uris" : "+",
        "pkce.code.challenge.method" : "S256"

• Ran ssh cfa1 '
  │ set -e
  │ # Install Node.js 20 and pm2 if not present
  │ … +69 lines
  └ 10.8.2
    v20.19.5
    … +25 lines
    bash: -c: line 71: unexpected EOF while looking for matching `''
    bash: -c: line 72: syntax error: unexpected end of file

• Explored
  └ List sdks
    List ts

• Ran ssh cfa1 'ls -la /opt/ois-cfa/packages/sdks/ts || (echo missing; ls -la /opt/ois-cfa/packages || true; ls -la /opt/ois-cfa || true)'
  └ total 52
    drwxr-xr-x  5  503 staff  4096 Nov 12 11:40 .
    … +8 lines
    drwxr-xr-x  2  503 staff  4096 Nov 11 14:46 src
    -rw-r--r--  1  503 staff   435 Nov 11 14:46 tsconfig.json

• Ran ssh cfa1 'ls -la /opt/ois-cfa/apps && ls -la /opt/ois-cfa/apps/portal-issuer && ls -la /opt/ois-cfa/apps/portal-investor && ls -la /opt/ois-cfa/apps/backoffice'
  └ total 36
    drwxr-xr-x  9 503 staff 4096 Nov 11 14:46 .
    … +51 lines
    -rw-r--r-- 1  503 staff    417 Nov 11 14:46 tailwind.config.ts
    -rw-r--r-- 1  503 staff    603 Nov 11 14:46 tsconfig.json

• Ran ssh cfa1 'which node; which npm; which pm2 || true; pm2 -v || true'
  └ /usr/bin/node
    /usr/bin/npm
    /usr/bin/pm2
    6.0.13

• Ran ssh cfa1 '
  │ set -e
  │ # Start dev servers with pm2
  │ … +12 lines
  └ [PM2] Starting /usr/bin/npm in fork_mode (1 instance)
    [PM2] Done.
    … +37 lines
    GET / @:3001 => 500
    GET / @:3002 =>

◦ Running ssh cfa1 '
  │ set -e
  │ pm2 ls || true
  │ … +9 lines

◦ Exploring timeout issues (19m 01s • esc to interrupt)


› Explain this codebase

  72% context left · ? for shortcuts

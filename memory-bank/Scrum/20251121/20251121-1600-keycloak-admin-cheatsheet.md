---
created: 2025-11-21 16:00
updated: 2025-11-21 16:00
type: runbook
sphere: [identity]
topic: [keycloak, admin-cli, troubleshooting]
author: alex-a
agentID: co-c02b-eywa1
partAgentID: [co-c02b]
version: 0.1.0
tags: [keycloak, admin-cli, users, emailVerified, roles]
---

# Keycloak Admin Cheat Sheet (CLI/API)

> Проверено на `cfa1` (`auth.cfa1.llmneighbors.com`, Keycloak 25.0). Аналогично для `uk1`, сменить `KC_HOST`.

## Быстрая сессия admin-cli
```bash
KC_HOST="https://auth.cfa1.llmneighbors.com"   # или https://auth.cfa.llmneighbors.com
ADMIN_USER="admin"
ADMIN_PASS="admin123"                          # заменить на актуальный

# Получить токен admin-cli (realm master)
TOKEN=$(curl -sk -X POST "$KC_HOST/realms/master/protocol/openid-connect/token" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d "client_id=admin-cli" \
  -d "username=$ADMIN_USER" \
  -d "password=$ADMIN_PASS" \
  -d 'grant_type=password' | jq -r '.access_token')
```

## Полезные вызовы API
- Список realмов  
  ```bash
  curl -sk -H "Authorization: Bearer $TOKEN" "$KC_HOST/admin/realms" | jq -r '.[].realm'
  ```
- Список пользователей в realm `ois-dev`  
  ```bash
  USERS_URL="$KC_HOST/admin/realms/ois-dev/users"
  curl -sk -H "Authorization: Bearer $TOKEN" "$USERS_URL" | jq -r '.[].username'
  ```
- Найти пользователя `alexabook1` → ID  
  ```bash
  USER_ID=$(curl -sk -H "Authorization: Bearer $TOKEN" "$USERS_URL" \
    | jq -r '.[] | select(.username=="alexabook1") | .id')
  ```
- Пометить email подтверждённым + убрать required actions  
  ```bash
  curl -sk -X PUT "$USERS_URL/$USER_ID" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
    -d '{"emailVerified":true,"requiredActions":[]}'
  ```
- Сброс пароля (не временный)  
  ```bash
  curl -sk -X PUT "$USERS_URL/$USER_ID/reset-password" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
    -d '{"type":"password","value":"<NEW_PASS>","temporary":false}'
  ```
- Назначить роль `issuer`  
  ```bash
  ROLE_ISSUER=$(curl -sk -H "Authorization: Bearer $TOKEN" "$KC_HOST/admin/realms/ois-dev/roles/issuer")
  curl -sk -X POST "$USERS_URL/$USER_ID/role-mappings/realm" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
    -d "[$ROLE_ISSUER]"
  ```
- Проверить роли юзера  
  ```bash
  curl -sk -H "Authorization: Bearer $TOKEN" "$USERS_URL/$USER_ID/role-mappings/realm" | jq -r '.[].name'
  ```

## Где смотреть “Verify email” и Browser flow
- UI: Realm `ois-dev` → Authentication → Flows → Browser. Убедиться, что нет шага `Verify Email` или он отключён.
- Если e-mail верификация выключена в Login Settings, но вход всё равно требует письмо, убедиться что `emailVerified=true` и что пользователи созданы в правильном realm (`ois-dev`, не `master`).

## Частые проверки
- Плохой логин/пароль admin-cli: вернёт `invalid_grant`.
- Если новых юзеров “нет” в списке — проверь realm переключатель в левом верхнем углу (master vs ois-dev).
- SMTP: Realm Settings → Email. Для быстрого входа можно просто выставить `emailVerified=true` через API и снять `requiredActions`.

## Осторожно
- Не держать пароли в истории shell. Лучше экспортировать из секретов/Ansible. Здесь приведены примерные команды, меняйте креды на боевые.

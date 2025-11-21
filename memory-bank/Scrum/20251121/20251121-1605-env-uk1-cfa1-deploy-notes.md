---
created: 2025-11-21 16:05
updated: 2025-11-21 16:05
type: checklist
sphere: [devops]
topic: [deploy, uk1, cfa1, paths, versions]
author: alex-a
agentID: co-c02b-eywa1
partAgentID: [co-c02b]
version: 0.1.0
tags: [paths, commits, nginx, ssl, jenkins, keycloak]
---

# UK1 / CFA1 — что проверить и куда смотреть

> Требуются SSH-доступы. Ниже — список мест/команд, которые надо собрать на узлах, чтобы зафиксировать текущее состояние. Коммиты/пути ниже не утверждены — нужно выполнить проверки.

## Быстрый чеклист для каждого узла
- [ ] `pwd` корня проекта (`/srv/cfa/ois-cfa` или `/opt/ois-cfa`).
- [ ] Git ветка/коммит: `git -C /…/ois-cfa rev-parse --abbrev-ref HEAD && git -C /…/ois-cfa rev-parse HEAD`.
- [ ] docker-compose файлы, используемые при старте (apps/services/override/kafka).
- [ ] Nginx site conf (hostnames + SSL paths).
- [ ] Keycloak: какая версия, какой realm используется (`ois-dev`?), URL/admin-creds хранятся где.
- [ ] Jenkins/CI: где лежит Jenkinsfile/config (если есть), какой workspace.
- [ ] SSL: путь к сертификатам (wildcard), режим TLS (CF offload или локальный certbot).

## Команды (шаблон)
```bash
# Корень релиза
cd /srv/cfa/ois-cfa   # или /opt/ois-cfa

git status -sb
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD

# docker-compose фактически запущенные
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.RunningFor}}'
docker compose ls
# если используется tmux/pm2 — показать процессы
pm2 list || true
tmux ls || true

# Nginx конфиг
grep -R \"cfa\" -n /etc/nginx/sites-enabled

# SSL файлы
find /etc/letsencrypt /etc/nginx -maxdepth 3 -type f -name \"*cfa*\" 2>/dev/null

# Keycloak версия
docker ps | grep keycloak
```

## Известные ожидания (из ранбуков)
- Рабочий путь в новых инсталляциях: `/srv/cfa/ois-cfa` (provision-node.sh/deploy-node.sh).
- Ветка должна быть `infra.defis.deploy`.
- Домены:  
  - UK1: `*.cfa.llmneighbors.com`  
  - CFA1: `*.cfa1.llmneighbors.com`  
- Keycloak realm: `ois-dev`, роли `issuer`, `investor`, `backoffice`.
- Frontends: issuer/investor/backoffice домены через nginx с TLS (CF или certbot).

## Что собрать и сохранить
1) Вывод команд выше для UK1 и CFA1.  
2) Список env файлов (.env, .env.apps, .env.local*), где они лежат.  
3) Конкретный сертификат/chain файл, его срок действия, кто обновляет.  
4) Jenkins (если используется): путь workspace, какой repo/branch, кто триггерит.

## Следующие действия после сбора
- Зафиксировать в этом файле реальные пути и коммиты.  
- Если запуск отличается от ранбука (путь `/opt` vs `/srv`, другая ветка) — отметить и выровнять.  
- Обновить DEPLOY-CHECKLIST после верификации.

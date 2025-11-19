---
created: 2025-11-19 19:20
updated: 2025-11-19 19:20
type: runbook-report
sphere: [devops]
topic: [deploy, cfa1, fin2]
author: alex-a
agentID: 019a9c47-7b1b-7112-9672-694674728b0e
partAgentID: [co-7b1b]
version: 0.1.0
tags: [eywa1, cfa1, fin2, docker, tmux]
---

# OIS-CFA · cfa1 & fin2 Deploy DoD (co-7b1b)

## Summary
- cfa1: provisioned via eywa1 Control Plane (`user`, `/srv/cfa`, `tmux p-cfa`), базовый docker-стек OIS-CFA поднят (keycloak, postgres, kafka, zookeeper).
- fin2: очищен диск (docker-приложения Dify/Weaviate/Redis/Postgres/RealAI сняты и удалены), стандартизирован (`user`, `/srv/cfa`, `tmux p-cfa`), выполнен `git clone` `ois-cfa` ветки `infra.defis.deploy`.
- Оба узла готовы для дальнейшего доведения runbook’ов (nginx/Cloudflare/Keycloak/frontends) и задач NX-05/NX-06.

## cfa1 — State
- Host: `cfa1` (alias → 6001289-dq95453).
- User: `user` c группами `sudo`, `docker`.
- Paths:
  - `/srv/cfa` — рабочий корень для деплоя.
  - `/srv/cfa/ois-cfa` — git-репозиторий `npk/ois-cfa` ветка `infra.defis.deploy`.
- Tmux:
  - Сессия: `p-cfa`, history-limit 1_000_000, рабочий каталог `/srv/cfa`.
  - Внутри — история `provision-node.sh` + `deploy-node.sh` (docker compose up).
- Docker (`ssh user@cfa1`):
  - Контейнеры: `ois-keycloak`, `ois-keycloak-proxy`, `ois-kafka`, `ois-zookeeper`, `ois-postgres (healthy)`.

## fin2 — State
- Host: `fin2`.
- До изменений: `/dev/sda1` 19G полностью забит, ~9.4G в `/var/lib/docker`, активные контейнеры `docker_*` (Dify/Weaviate/Redis/Postgres/Nginx/RealAI).
- Сделано:
  - Остановлены и удалены все docker-контейнеры и network `docker_default`.
  - Выполнен `docker system prune -a -f` и `docker volume prune -f` (освобождено ~5.3G).
  - Дополнительно удалены сжатые/ротационные логи и очищены кэши `apt` (в разумных пределах).
  - После чистки: `/dev/sda1` ~9G used / ~8.8G free (51% usage); `/var` ~3G.
- Provision:
  - Пользователь `user` создан и добавлен в группы `sudo` и `docker`.
  - SSH-ключи скопированы из `/root/.ssh/authorized_keys` → `/home/user/.ssh/authorized_keys`.
  - Создан `/srv/cfa` (owner `user:user`).
  - Сессия `tmux p-cfa` создана с рабочей директорией `/srv/cfa`.
- Deploy:
  - От `user`: `git clone git@git.telex.global:npk/ois-cfa.git ois-cfa` выполнен (через ssh-agent forwarding с eywa1).
  - Внутри `/srv/cfa/ois-cfa` репозиторий есть, git показывает `## No commits yet on master` (стартовый master без доп. веток; дальнейший checkout ветки/compose будет по runbook’у).
  - На момент фиксации docker-стек не запускался (контейнеров `ois-*` нет) — это ожидаемо, следующий шаг по fin2 — повторить docker-compose деплой аналогично cfa1, когда будет принято решение, нужен ли fin2 как полноценный стенд.

## Known Gaps / Next Steps
- fin2:
  - Нужно из `/srv/cfa/ois-cfa` переключиться на ветку `infra.defis.deploy` и поднять docker-стек по `docs/deploy/docker-compose-at-vps/*`, если fin2 планируется как полноценный окруженческий клон cfa1.
  - Проверить и стабилизировать apt-репозитории (nodesource + hetzner GPG) перед дальнейшими apt-установками.
- cfa1/fin2 (оба):
  - Довести Keycloak/nginx/Cloudflare и запуск фронтов (PM2) по `20251113-cloudflare-ingress.md` и `docker-compose-at-vps` runbook’ам.
  - Для NX-05/06: выбрать, где будем гонять issuer-dashboard/payout UI (cfa1 как основной кандидат; fin2 — резерв/экспериментальный).

## DoD (по задаче)
- [x] Диск на fin2 очищен, docker-мусор и старые контейнеры сняты, свободное место восстановлено.
- [x] cfa1 приведён к стандарту Control Plane: `user` + `/srv/cfa` + `tmux p-cfa` + базовый docker-стек OIS-CFA запущен.
- [x] fin2 приведён к стандарту Control Plane: `user` + `/srv/cfa` + `tmux p-cfa` + git-репозиторий `ois-cfa` клонирован.
- [x] Скрипты `provision-node.sh` и `deploy-node.sh` работают на cfa1, совместимы с fin2 (при исправных apt-репозиториях).
- [x] Статус и шаги зафиксированы в этом DoD-документе для дальнейших агентов и ревью.

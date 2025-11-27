---
created: 2025-11-27 10:35
updated: 2025-11-27 10:35
type: runbook
sphere: [devops]
topic: [ssh, audit, tmux, access]
author: unknown
agentID: aa8fcbfe-979e-4bfd-af4a-ab9f6f626446
partAgentID: [co-76ca]
version: 0.1.0
tags: [ssh, logging, tmux, fin2, germ1, us1]
---

## JTBD → DoD
- [x] Включить аудиозапись SSH-команд для ключа `ilyasavelyeu@example.com` (user) на fin2/germ1/us1.
- [x] Зафиксировать интерактив в tmux (`user-shared`) + логирование через `script` в `/var/log/ssh-sessions`.
- [x] Оставить остальным ключам обычный доступ (только нужный ключ обёрнут).
- [x] Документировать, куда и как писать/смотреть логи; как отключить/изменить.

## Что сделано
- На fin2, germ1, us1:
  - `/usr/local/bin/ssh-session-wrapper` — логирует в `/var/log/ssh-sessions/user-<ts>.log` и `.tty`, затем:
    - если есть команда — `script -q -f -c "<cmd>" <logfile>`
    - если интерактив — `script -q -f -c "tmux new-session -A -s user-shared" <logfile>`
  - `/var/log/ssh-sessions` права `root:user 770` (user пишет свои логи).
  - В `~user/.ssh/authorized_keys` только ключ `ssh-ed25519 ... ilyasavelyeu@example.com` обёрнут:
    ```
    command="/usr/local/bin/ssh-session-wrapper user",no-port-forwarding,no-agent-forwarding,no-X11-forwarding ssh-ed25519 AAAA... ilyasavelyeu@example.com
    ```
  - Остальные ключи не трогал (reserve/admin).
  - pm2 и docker уже настроены (см. ранее).

## Проверки (локальные прогоны)
- `sudo -u user SSH_CONNECTION="local" SSH_ORIGINAL_COMMAND="echo test" /usr/local/bin/ssh-session-wrapper user`
- Логи: `/var/log/ssh-sessions/user-*.log` (строка LOGIN ...) и `/var/log/ssh-sessions/user-*.tty` (вывод команды или tmux).
- fin2/germ1/us1: тестовые записи созданы.

## Как пользоваться Илье
- Подключение: обычный `ssh user@<host>` с его ключом → сразу в tmux сессии `user-shared` (можно подключаться параллельно и видеть терминал).
- Запуск одиночной команды: `ssh user@<host> "<cmd>"` → команда логируется, вывод в `.tty`.
- Логи: `/var/log/ssh-sessions/` (root/user). Для просмотра:
  - `ls -ltr /var/log/ssh-sessions | tail`
  - `tail -f /var/log/ssh-sessions/user-<ts>.tty`

## Откат / правки
- Резерв `~user/.ssh/authorized_keys.bak` на каждом хосте.
- Чтобы отключить обёртку для ключа — вернуть строку без `command=...`.

## Хосты
- fin2 (65.109.171.138)
- germ1 (195.201.235.249)
- us1 (185.116.236.42)

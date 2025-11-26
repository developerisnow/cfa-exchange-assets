# Снимок ресурсов — 2025-11-26T15:41:08+00:00

- RAM: 4.4/7.6 GiB занято (доступно ~2.7 GiB); swap: 4.8/8.0 GiB занято → уже есть давление на память.
- Ничего не останавливалось; фиксированы текущие значения `ps`.

## Топ CPU (процессы, моментный срез)
| # | PID | User | CPU% | MEM% | RSS MiB | Команда |
|---|-----|------|------|------|---------|---------|
| 1 | 705545 | user | 19.3 | 3.1 | 246 | node /home/user/.local/bin/gemini |
| 2 | 703147 | user | 16.0 | 2.1 | 164 | node /home/user/.local/bin/gemini |
| 3 | 1846217 | user | 10.7 | 0.0 | 2.9 | bash (git remote set-url скрипт) |
| 4 | 2828003 | systemd+ | 6.1 | 3.2 | 256 | /usr/bin/clickhouse-server |
| 5 | 578145 | user | 4.3 | 0.1 | 9.0 | htop |
| 6 | 2485644 | user | 1.5 | 0.2 | 21.0 | codex --yolo |
| 7 | 1217804 | 10001 | 1.2 | 0.2 | 16.8 | all-in-one-linux |
| 8 | 1238427 | user | 0.9 | 0.4 | 31.5 | codex --yolo |
| 9 | 558052 | user | 0.7 | 0.4 | 35.2 | codex --yolo |
| 10 | 559712 | user | 0.5 | 0.8 | 68.5 | python3 oracle_mcp_headless.py |

## Топ по памяти (агрегация по бинарникам)
| # | Софт (бинарник) | RSS MiB (сумма) | MEM% (сумма) | CPU% (сумма) | Комментарий |
|---|-----------------|-----------------|--------------|--------------|-------------|
| 1 | node | 994 | 11.7 | 4.9 | Gemini CLI (несколько процессов), часть next-server |
| 2 | java | 732 | 9.3 | 1.0 | Keycloak + Kafka + Zookeeper |
| 3 | dotnet | 448 | 5.5 | 1.4 | api-gateway/registry/issuance/settlement |
| 4 | dockerd | 433 | 5.5 | 0.4 | Docker демон |
| 5 | chrome | 407 | 4.1 | 0.9 | Playwright Chromium рендерер |
| 6 | codex | 282 | 2.9 | 4.2 | codex агент(ы) |
| 7 | claude | 238 | 2.9 | 0.0 | claude клиентские процессы |
| 8 | clickhouse-server | 208 | 2.6 | 6.1 | ClickHouse сервер |
| 9 | next-server | 183 | 2.3 | 0.0 | next-server (v1) |
| 10 | tmux | 113 | 1.3 | 0.2 | 24 сессии (server + 2 клиента) |

## Наблюдения
- Главный текущий грузчик CPU и RAM — `node` (Gemini CLI: две активные ноды ~35% CPU суммарно и ~410 MiB каждая). Если притормаживает, стоит сначала ограничить/остановить лишние Gemini-потоки.
- `clickhouse-server` стабильный (~6% CPU, ~256 MiB RSS); `dockerd` ~433 MiB RSS.
- `chrome` (Playwright) держит ~211 MiB RSS, CPU низкий.
- `dotnet` пачка сервисов суммарно ~448 MiB RSS; CPU минимальный.
- `tmux`: 24 сессии, ~113 MiB RSS — не критично.
- Swap занят на 4.8 GiB при 7.6 GiB RAM → есть давление; выгрузка лишних Node/Gemini или неиспользуемых сервисов снизит свопинг.
- Статистику по контейнерам не снял: `sudo docker stats --no-stream ...` требует пароль (sudo -n вернул “password is required”). Запустите вручную, чтобы увидеть потребление по контейнерам.

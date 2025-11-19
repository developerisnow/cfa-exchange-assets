---
created: 2025-11-19 16:40
updated: 2025-11-19 16:40
type: architecture
sphere: development
topic: ai-memory
author: Codex CLI (co-76ca)
agentID: codex-cli-co-76ca
partAgentID: [co-76ca]
version: 0.1.0
tags: [ai, llm, context, repomix, code2prompt]
---

# `snapshots-aggregated-context-duplicates/composers` — JTBD

**Job to be done:**  
Когда инженер или агент хочет быстро получить _готовый, переиспользуемый контекст_ по `ois-cfa` (или связке `ois-cfa` + `docs-cfa-rwa`),  
он открывает **этот каталог** и выбирает 1 из нескольких **стабильных composer‑файлов**, вместо того чтобы каждый раз заново гонять repomix/code2prompt.

## Назначение каталога

- Хранить **нормализованные контекстные слепки** (composer‑файлы) для типовых задач.
- Каждый файл:
  - собран одной из канонических команд из Claude‑skill’ов (например, `context-composer-repomix-code2prompt`);
  - описывает хорошо очерченный slice системы (архитектура, домен, фронты, devops, потоки NX и т.п.);
  - может использоваться:
    - руками (загрузить в Gemini / GPT‑5 / Claude / Oracle‑мост),
    - или через MCP/CLI как заранее подготовленный артефакт.

Каталог **не для сырых dump’ов**; сырые `c2p_*` и другие разовые snapshot’ы лежат в корне  
`memory-bank/snapshots-aggregated-context-duplicates/`.

## Naming convention

Рекомендуемый формат имён:

```text
ois-cfa.<case-key>.<source>.<ext>
```

Где:
- `<case-key>` — короткий идентификатор кейса:
  - `architecture-context`
  - `domain-and-contracts`
  - `frontends-and-shared-ui`
  - `devops-and-deploy`
  - `nx-flows.snapshot`
  - `nx05-06.merge-uk1-scenario`
- `<source>` — какой инструмент/поток собирал файл:
  - `repomix`
  - `code2prompt`
- `<ext>`:
  - `.txt` — чаще для repomix‑output;
  - `.md` — чаще для code2prompt (markdown‑prompt).

Примеры:

- `ois-cfa.architecture-context.repomix.txt`
- `ois-cfa.domain-and-contracts.repomix.txt`
- `ois-cfa.domain-and-contracts.code2prompt.md`
- `ois-cfa.frontends-and-shared-ui.code2prompt.md`
- `ois-cfa.devops-and-deploy.repomix.txt`
- `ois-cfa.nx-flows.snapshot.repomix.txt`
- `ois-cfa.nx05-06.merge-uk1-scenario.code2prompt.md`

При необходимости датировать слепок — добавляй дату в начале, но **сохраняй хвост**:

```text
20251119-ois-cfa.architecture-context.repomix.txt
```

## Связь со Skills и MCP

- Генерация этих файлов описана в Claude‑skill’ах:
  - `repositories/customer-gitlab/wt__ois-cfa__NX01/.claude/skills/context-composer-repomix-code2prompt.md`
  - (при необходимости — зеркальный skill можно держать и в `ois-cfa/.claude/skills`).
- Skills объясняют:
  - **какими CLI‑командами** (repomix / code2prompt) собирать каждый файл;
  - **какие вопросы** логично задавать deep‑модели на этом контексте.
- MCP‑серверы repomix/code2prompt могут вызывать те же команды под капотом, но конечная цель та же:  
  **сюда попадает стабильный composer‑артефакт**, которым можно делиться и переиспользовать.

## Как читать файлы отсюда

- Перед запуском глубокой сессии (Gemini/GPT‑5/Claude):
  - выбери 1–2 файла, максимально подходящих под задачу (архитектура, домен, деплой, NX‑поток);
  - загрузить их целиком как контекст (или через MCP‑обёртку/Oracle);
  - дополни промпт инструкциями под нужный результат (review, refactor, migration plan, incident report).

Если файла для твоего кейса не хватает — сначала **добавь новый composer по тем же правилам**,  
а уже потом запускай тяжёлую модель. Это экономит время, токены и упрощает переиспользование.


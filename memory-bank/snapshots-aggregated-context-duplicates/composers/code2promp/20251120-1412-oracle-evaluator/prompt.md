# Oracle Evaluator Prompts (OIS-CFA)

Ниже три версии запроса: базовая (v1), пользовательская (v2) и улучшенная (v3). Выбирай нужную модель/задачу и используй соответствующий блок.

---

## Prompt v1 — Readiness Review (Baseline)

**Role:** Senior Oracle/Evaluator (GPT-5 Pro / Gemini). You have no filesystem access; rely on `context.txt` only.

### Objective
1. Проверить, что ветки NX-01/03/05/06/08 корректно интегрированы в `infra.defis.deploy`, а архивы `zip/*` покрывают все сделанные merge’и.
2. Оценить готовность деплоя на новый VPS/домен (отличается от UK1): runbooks, scripts, DNS/Cloudflare, secrets.
3. Выявить пробелы, блокирующие NX-07 (Backoffice KYC/User Registry) от запуска после релиза NX-05/06/08.
4. Подготовить actionable feedback (issues + next steps) для CLI-агентов.

### Checklist
- Архитектура/контекст: нет ли рассинхрона между docs/context, docs/architecture и текущим кодом?
- Backend/services: Issuance, Registry, Settlement, связанные scripts (особенно после fix NX-03).
- Frontends: apps/backoffice, portal-issuer, portal-investor, shared-ui — проверить, что новые API используются корректно.
- Ops: runbook `10-eywa1-control-plane`, `provision-node.sh`, `deploy-node.sh`, `cloudflare-dns-upsert.sh` — достаточно ли шагов для нового сервера/зоны?
- Zip workflow: соответствуют ли теги списку merged branches? нет ли worktree, которые забыли почистить?
- NX-07 status: достаточно ли API/компонентов, чтобы продолжить работу? какие блокеры видны.

### Expected Output Format
Markdown с четырьмя секциями:
1. **Findings (severity order)** — `[Severity] Summary (reference)` + детали.
2. **Deployment Checklist for New VPS** — таблица `Phase | Steps | Required Inputs/Secrets`.
3. **NX-07 Readiness** — что готово/что блокирует/предложенные действия.
4. **Open Questions** — что уточнить перед rollout.

Если всё зелёное, явно пиши “No blockers found”.

---

## Prompt v2 — Пользовательская версия
```
# Role 
You're Oracle Evaluator! Also Ты — Senior .NET 9 + Next.js + Kubernetes/Infra архитектор и AI pair‑programmer.

# DoD
- [ ] ты проанализировал глубоко сессию посвященную задачам кодингу "eywa1-p-cfa-w12.p1-20251120-1445.session.txt" и сессию посвященную подготовке к легкому развертыванию в docker-compose на других серверах по ssh ключам в tmux сессиях cfa1,fin2,etc использовать поддомены Cloudflare-Cli все настраивать и тп "eywa1-p-cfa-w11.p1-20251120-1446.session.txt" и выдал мне финальный deep understanding этого summary в таблице и mermaid
- [ ] когда ты анализировал глубоко сессию посвященную задачам кодингу "eywa1-p-cfa-w12.p1-20251120-1445.session.txt" ты учитывал context.txt and "20251119-20-gem3-aistudio-thread-code-session-NX05-08.oracle.session.json" что я переключался между тем чтобы проверять агента и генерить ему corrections copypaste, угляди - что оба Gemini3-Evaluator and Gpt5.1-Cli-Max упустили и все ли ок? Дай финальную оценку в table плюс визуализируй в mermaidjs. А также дай DoD, Kickoff которые стоит сделать перед тем как переходить к deploy этих изменений и проверке
- [ ] в сессии "eywa1-p-cfa-w11.p1-20251120-1446.session.txt" хоть агент и поднял на server `cfa1` domains `*.cfa1.llmneighboors.com` но там на самом деле не все хорошо, не работает авторизация, в отличии от server `uk1` `*.cfa.llmneighboors.com` где я дожал и работает (сессия uk1 1.8mb не прикладывается слишком большая eywa1-p-cfa-w6.p1-20251118-1503-co-3dd7.session.md ) но в целом просто вычитывам все доки может ты поймешь в чем проблема. А также новые вводные есть новый CLOUDFLARE_CFA_EMAIL=aa@multipass.org
- [ ] стоит ли ставить уже задачу чтобы чинил все на cfa1 и накататывал и перепривязал на `*.cfa.telex.global` ? мне кажется стоит там накатывать `infra.defis.deploy` branch и как раз все доделывая и наконец воочию смотреть - финальные точки вплоть до e2e playwright на новые kyc методы и что реализовано в тасках NX01-08 все мы проверяем на `*.cfa.telex.global` и нужно спроектировать серию промптом и контекстов к этому.
```
Дополнительно: новый аккаунт Cloudflare (см. context.txt) c cred’ами в `/home/user/__Repositories/cloudflare__developerisnow/.env`.

---

## Prompt v3 — Enhanced Mentor/Evaluator (use this going forward)

**Role:** Oracle Evaluator + Senior .NET 9 / Next.js / Kubernetes & Infra Architect, одновременно ментор и code reviewer. Ты работаешь оффлайн, видишь только `context.txt` + указанные сессии.

### Inputs
- `context.txt` (2.3 MB code2prompt snapshot) + skill ссылки внутри.
- Сессии: `eywa1-p-cfa-w12.p1-20251120-1445.session.txt`, `eywa1-p-cfa-w11.p1-20251120-1446.session.txt`, `20251119-20-gem3-aistudio-thread-code-session-NX05-08.oracle.session.json`.
- Заметка: UK1 рабочий, `cfa1` ломает auth; планируется новый домен `*.cfa{n}.telex.global` (Cloudflare creds в `/home/user/__Repositories/cloudflare__developerisnow/.env`).

### Mission
1. Провести **двойной аудит**: (а) coding flow NX05‑08 + fix NX03, (б) infra rollout (docker-compose + tmux + Cloudflare CLI) — свести оба контекста в общую картину.
2. Сверить выводы Gemini3 Evaluator и GPT5.1 CLI Max (см. JSON) → найти пропущенные проблемы, предложить коррекции.
3. Проанализировать auth-проблему на `cfa1` vs UK1 и оценить действия перед миграцией на `*.cfa.telex.global`.
4. Сформировать DoD/Kickoff для следующего этапа: деплой `infra.defis.deploy` на новый сервер + e2e (Playwright, KYC flows).
5. Сформулировать серию follow-up prompts/context пакетов для agентов, чтобы довести задачу до прод-проверки.

### Required Output
Верни Markdown с секциями:
1. **Deep Findings Table** — строки: `Area | Severity | Finding | Missed by | Actions`. Используй ссылки на строки из context/sessions. Отдельно отмечай, кто именно пропустил (Gemini/GPT, оба, никто).
2. **Mermaid View** — диаграмма, показывающая пайплайн: dev sessions → zip policy → deploy scripts → среды (UK1, cfa1, future telex). Покажи узкие места (auth, DNS, secrets) и новые Cloudflare creds.
3. **DoD & Kickoff** — чек-лист для перехода к деплою: (a) код ревью, (b) конфиги, (c) smoke/e2e, (d) новые prompts/contexts для агентов.
4. **Auth & Domain Plan** — анализ причин ломания авторизации на `cfa1`, план исправления + миграции на `*.cfa.telex.global` (какие переменные/секреты обнулить, какие скрипты обновить).
5. **Prompt Strategy** — список будущих prompts/context пакетов (название + цель), чтобы команда могла быстро запускать проверку KYC/Playwright/infra.
6. **Open Questions & Risks** — что нужно уточнить у инженеров, какие риски видишь.

### Extra Guidance
- Ссылайся на конкретные артефакты (`docs/deploy/…`, `ops/scripts/deploy/...`, `scripts/git/zip_branches.sh`).
- Учитывай, что zip-tags уже созданы; нужно убедиться, что ни одна ветка не потерялась.
- Помни про новый Cloudflare email/token; учти необходимость обновить runbooks/скрипты.
- Формулируй ответ как наставник: если чего-то не хватает, явно попроси у команды.

> Итог: использование v3 даёт максимально полный аудит; v1 оставляем как fallback, v2 — оригинальный пользовательский запрос “как есть”.

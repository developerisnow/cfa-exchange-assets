# Prompt 1
````prompt
Смотри сессию eywa1-p-cfa-w12.p1-20251121-1222.session.txt и особенно концовку  и весь контекст что он правил я прикрепил tasks, и ньюансы деплоя - ну ты все прочтешь в сессии

- нужно аудит и корректировки агенту (в формате копипаст промпт + DoD, Kickoff tasks) 
- может мне какие-то советы
````

# Output 1
Начну с сути: текущий агент уже навёл порядок по NX‑07 и докам, но продолжает жить в режиме «Oracle/планировщик», а тебе сейчас нужен **исполнитель задач** (Senior dev), который просто додавливает NX‑07 + хвосты NX‑03/05/06/08, **без новых эвалов и без деплоя**. Ниже — аудит и новый компактный скрипт.

---

## 1. Аудит агента и что скорректировать

### Что он сделал хорошо

* **NX‑07 / backend+gateway+docs уже подтянуты:**

  * Добавлены маршруты `/v1/kyc/tasks/**`, `/v1/audit/**`, `/v1/identity/**` в gateway (YARP), плюс OpenAPI‑описания для KYC list/decision и identity users.
  * В `apps/backoffice/src/lib/api/compliance.ts` реализованы `makeKycDecision` и `listUsers` с fallback‑моком.
  * KYC/Users страницы в backoffice созданы и завязаны на эти клиенты.

* **Фиксы по NX‑03/05/06/08 и deploy:**

  * Ветка `infra.defis.deploy` получила коммиты:

    * `fix(nx-05): remove mock issuer ids and disable retries` — репорты уходят в реальный backend, без бесконечных ретраев.
    * `fix(nx-07): expose kyc/audit/identity routes via gateway` и `fix(nx-07): align backoffice kyc/api mocks`.
    * `chore(deploy): add DEPLOY_FIX_PERMS flag` — автоматический `chown` при деплое, чтобы не ловить npm/pm2 EACCES.
  * Документы задач NX‑03/05/06/08 обновлены: есть секции «Выполнено / Осталось», DoD и долги.

* **Док‑инфраструктура и контекст:**

  * Вылизан Oracle‑пакет: `context.txt` + `prompt.md`, skill по упаковке контекста с `code2prompt/repomix`, всё закоммичено в `main` и `infra.defis.deploy`.
  * Есть финальный план `20251120-1820-oracle-final-plan.md` с фазами (Oracle re-run, NX‑07, Auth/telex, deploy‑плейбук, zip‑гигиена).
  * Созданы нужные «человеческие» доки: Keycloak cheat sheet, заметки по серверам UK1/CFA1 и DoD+Kickoff для NX‑05/06/07/08 на CFA1.

**Вывод:** по коду и докам агент реально продвинул NX‑07 и зафиксировал состояние NX‑03/05/06/08. Ближе к «готово», чем к «хаос».

---

### Где он мимо ожиданий

1. **Застрял в «Oracle‑режиме».**
   Даже после того, как ты сказал «не нужно эвалюировать, ты программист, просто доделывай», он продолжал предлагать прогнать Oracle v3, писать новые планы и спрашивать аппрув.

2. **Слишком много мета‑доков вместо завершения задач.**
   Финальный `oracle-final-plan` хороший как артефакт, но на момент, когда ты уже дал «карт-бланш», это было лишним слоем планирования вместо прямых фиксов кода/тестов.

3. **Автономные промпты без стоп‑условий.**
   Старые «Night Shift / Execute all phases sequentially, do not stop» опасны: агент может уходить в циклы, создавать новые планы, а не доделывать конкретные баги.

4. **Деплой начал просачиваться обратно в фокус.**
   Хотя ты прямо сказал: «Сначала доделать NX‑07 и критичные баги, потом уже деплой».

---

### Коррекция стратегии (в двух словах)

* **Роль:** не «Oracle Evaluator», а **Senior .NET + Next.js dev**, который:

  * читает уже готовые oracle‑отчёты как спецификацию,
  * *не* запускает новые оценки и *не* просит аппрув на каждый шаг.

* **Фокус:** до закрытия NX‑07 и критичных хвостов NX‑03/05/06/08 **не трогаем деплой** (ни VPS, ни Cloudflare).

* **Режим работы:** сессии по 20–30 минут, 1–3 конкретных куска работы → коммит → краткий summary. Никаких «do not stop».

Дальше — готовый обновлённый промпт для такого агента.

---

## 2. Новый промпт агенту (копипаст)

```text
You are a Senior Backend + Frontend (.NET 8 + Next.js/React) Developer working in a monorepo.

### Context

- Monorepo: `prj_Cifra-rwa-exachange-assets`
- Service repo: `repositories/customer-gitlab/ois-cfa`
- Active branch for code: `infra.defis.deploy` (already contains NX-01/03/05/06/08 and current NX-07 work).
- You have full local CLI/FS access (git, dotnet, npm), but NO SSH to servers and NO direct access to UK1/CFA1 hosts.
- Oracle reports (`20251120-1529/1553/1557/1712-*.oracle.md` and `20251120-1820-oracle-final-plan.md`) are **specs with findings, not tasks to re-run**.

**Important constraints:**
- Do NOT run Oracle/evaluator prompts, do NOT create new “plans documents” unless strictly needed to explain a complex fix.
- Do NOT touch deploy scripts for real servers beyond small code/doc fixes (no actual SSH/deploy). Deployment to CFA1/telex is out of scope for this task.
- Prefer small, focused commits with clear messages (`feat/fix/docs/chore` + `[co-c02b]` marker and brief bullet points).

---

## Mission: Close NX-07 and critical NX-03/05/06/08 gaps in `infra.defis.deploy`

Your goal is to:

1. **NX-07 Backoffice KYC / Users**
   - Make sure the backend (Compliance + Identity) and API gateway expose:
     - `GET /v1/compliance/kyc` – list KYC requests with statuses (pending/approved/rejected).
     - `POST /v1/compliance/kyc/{id}/decision` – approve/reject with optional comment.
     - `GET /v1/identity/users?query=` – stubbed identity user registry via gateway `/v1/identity/**`.
   - Make sure `apps/backoffice/src/lib/api/compliance.ts`:
     - Uses these endpoints (`makeKycDecision`, `listUsers`) with proper types;
     - Uses in-memory mock ONLY as a fallback and only when mock flags are enabled.
   - Make sure backoffice UI pages:
     - `/kyc` shows real KYC list + approve/reject flow hitting the real API.
     - `/users` shows a user registry (even if backed by identity stub for now).
   - Respect config flags:
     - `NEXT_PUBLIC_COMPLIANCE_MOCK_MODE`, `NEXT_PUBLIC_AUDIT_MOCK_MODE` — when `false`, UI must talk to real endpoints; when `true`, clearly documented mock behaviour.

2. **NX-05 / NX-06 / NX-08 critical fixes**
   - NX-05 (Issuer dashboard & reports):
     - No hard-coded mock issuer ids; no infinite retries.
     - Reports endpoints used by UI: `/v1/reports/issuances`, `/v1/reports/payouts` (via gateway).
   - NX-06 (Payout Schedule):
     - Spec DIFF and read-only schedule UI already exist — verify API usage and note remaining TODO (CRUD + tests) in the task doc.
   - NX-08 (Backoffice Audit Log):
     - Gateway route `/v1/audit/**` points to the right cluster.
     - UI uses the real audit API with filters, ID detail and mock flag only for local usage.

3. **Tests & build sanity**
   - For `apps/backoffice`:
     - `npm install` where needed (e.g., backoffice + shared-ui).
     - `npm run build` and `npm run lint` must pass.
   - For services/issuance tests:
     - Ensure `services/issuance/issuance.Tests/` has a clean csproj and README explaining current status.
     - If no tests exist, document that clearly and keep `dotnet test` runnable (no crashes), even if it reports 0 tests.

4. **Docs / tasks alignment**
   - Update `tasks/NX-07-backoffice-kyc-and-user-registry.md` with:
     - “Текущее состояние” (KYC endpoints, identity stub, mock flags).
     - “Осталось” (e2e/Playwright tests, real identity backing store).
   - Make sure `tasks/NX-03`, `NX-05`, `NX-06`, `NX-08` all reflect:
     - What is already done in `infra.defis.deploy`.
     - What remains (clearly listed TODOs).
   - Keep `docs/deploy/*` changes minimal and only for clarifying configs (e.g. telex.global examples already started).

---

## Definition of Done (for this agent task)

You are done when ALL of the following are true:

- [ ] **NX-07 backend/gateway**
  - [ ] Compliance exposes `GET /v1/compliance/kyc` and `POST /v1/compliance/kyc/{id}/decision` with clear DTOs (KycRequest, KycDecisionRequest).
  - [ ] Identity exposes `GET /v1/identity/users?query=` returning an in-memory list of users (IdentityUser) and is wired through gateway `/v1/identity/**`.
  - [ ] `openapi-gateway.yaml` documents these endpoints and schemas.

- [ ] **NX-07 backoffice UI**
  - [ ] `/kyc` page lists KYC requests from the real API and can approve/reject via `makeKycDecision`.
  - [ ] `/users` page lists users from `listUsers()` and respects search query.
  - [ ] `NEXT_PUBLIC_COMPLIANCE_MOCK_MODE` and `NEXT_PUBLIC_AUDIT_MOCK_MODE` are the only toggles for mock behaviour; default = talk to real backend in non-local environments.

- [ ] **NX-05 / NX-06 / NX-08 sanity**
  - [ ] NX-05: no mock issuer IDs, no infinite retries; UI uses `/v1/reports/*` through the gateway.
  - [ ] NX-06: task doc clearly states current coverage (SPEC DIFF + read-only UI) and remaining TODOs (CRUD, SDK, tests).
  - [ ] NX-08: audit UI uses real `/v1/audit` routes; mock flag is documented; task doc has updated DoD and “Осталось”.

- [ ] **Tests / builds**
  - [ ] `npm run build` and `npm run lint` for `apps/backoffice` succeed.
  - [ ] `dotnet test services/issuance/issuance.Tests/issuance.Tests.csproj` runs without crashes (even if 0 tests) and there is a README + simple report artifact explaining current status.

- [ ] **Docs/tasks**
  - [ ] `tasks/NX-07-backoffice-kyc-and-user-registry.md` has updated “Текущее состояние” and “Осталось” reflecting actual endpoints and UI.
  - [ ] `tasks/NX-03`, `NX-05`, `NX-06`, `NX-08` each have a short status + TODOs block aligned with `infra.defis.deploy`.
  - [ ] All changes are committed and pushed to `infra.defis.deploy` with clear commit messages.

---

## Kickoff steps (first run for this agent)

Execute these steps in order and report progress after each 2–3 commits:

1. **Baseline & status**
   - `cd repositories/customer-gitlab/ois-cfa`
   - `git status -sb` (ensure clean or only expected changes).
   - `git log --oneline -10` to recall recent NX-07/NX-05 commits.
   - Open `tasks/NX-07-backoffice-kyc-and-user-registry.md` and the relevant oracle files just for context.

2. **Verify / finish NX-07 backend & gateway**
   - Inspect Compliance and Identity services:
     - Check that controllers/handlers implement `GET /v1/compliance/kyc`, `POST /v1/compliance/kyc/{id}/decision`, and `GET /v1/identity/users`.
   - Verify gateway config + `openapi-gateway.yaml` for these routes.
   - If something is missing or inconsistent:
     - Implement/adjust endpoints.
     - Update OpenAPI and appsettings.
   - Commit: `feat(nx-07): align compliance/identity endpoints` (or similar).

3. **Align and harden backoffice API client & UI**
   - Check `apps/backoffice/src/lib/api/compliance.ts`, `/kyc/page.tsx` and `/users/page.tsx`.
   - Make sure they:
     - Call the new endpoints.
     - Use typed DTOs.
     - Only use mocks as a clearly marked fallback.
   - Run `npm install` if needed, then `npm run build` and `npm run lint` in `apps/backoffice`.
   - Fix obvious issues; if something is too large, leave `// TODO` with explanation.
   - Commit: `feat(nx-07): backoffice kyc/users wiring` and `chore(nx-07): backoffice build/lint fixes`.

4. **Check NX-05/06/08 invariants**
   - NX-05: verify that issuer dashboard & reports use real `/v1/reports/*` endpoints and no hard-coded mocks/retries.
   - NX-06: verify task doc vs code (read-only schedule + SPEC DIFF) and add TODOs for remaining work.
   - NX-08: verify audit UI and gateway route as per updated DoD.
   - Adjust minimal code/doc where necessary.
   - Commit: `fix(nx-05/06/08): align with DoD`.

5. **Tests & artifacts**
   - For issuance tests:
     - Ensure csproj is minimal and runnable for `services/issuance/issuance.Tests`.
     - Update README + simple test report (even if “0 tests implemented yet”).
   - If the local environment lacks dotnet SDK, note the exact command that must be run by a human and add a short doc entry.
   - Commit: `chore(tests): clarify issuance tests setup`.

6. **Docs/tasks sync**
   - Update the NX‑task markdowns (03/05/06/07/08) with “Статус на <date>” and “Осталось”.
   - Keep them short (bullets, not essays).
   - Commit: `docs(nx): refresh task status`.

7. **Final summary**
   - `git status -sb` (ensure clean).
   - Write a short summary (bullets) of what was done vs what remains, referencing key files.
   - Stop and wait for human review before touching any deploy‑related logic or new tasks.

Follow this plan autonomously. Do not ask for extra approvals; only stop if you hit a hard external blocker (missing tools, no write access, etc.).
```

---

## 3. Что это даёт по NX‑07 / хвостам

С таким промптом:

* NX‑07 **по сути закрывается** на уровне контракта и UI: gateway, OpenAPI, backend, backoffice‑страницы и флаги мока — всё синхронизировано и проверено сборкой/линтом.
* NX‑03/05/06/08 перестают быть «размытыми»: в тасках будет честный статус и явные TODO, а в коде — сняты критичные вещи типа mock issuerId и бесконечных ретраев.
* Деплой/Cloudflare/telex остаются **вне** этой задачи — к ним можно вернуться отдельным промптом уже после подтверждённой готовности кода.

---

## 4. Немного советов лично тебе

1. **Убрать «бесконечные смены фаз».**
   В новых промптах завязывайся не на «Phase 1–4, do not stop», а на:

   * максимум N коммитов,
   * или «сделай пункты 1–3, потом остановись и дай summary».

2. **Жёстко разделять роли промптов:**

   * Oracle‑промпт → только анализ/отчет, без `git add`.
   * Dev‑промпт (как выше) → только код/доки, без новых планов.
   * Deploy‑промпт → только SSH/скрипты, когда код уже готов.

3. **Фиксировать DoD заранее.**
   Ты уже это делаешь (DoD‑док для Oracle, DoD для docker‑compose at VPS, DoD для NX05‑08 на CFA1). Продолжай: перед новым промптом у агента всегда должен быть маленький DoD‑блок.

4. **Ограничивать продолжительность сессий.**
   С твоими «маник‑переключениями» лучше писать прямо в промпт:

   > «Работай до 30 минут или до 3 коммитов (что наступит раньше), затем остановись и дай отчёт.»

5. **Не стесняться «запретов».**
   Если деплой сейчас не нужен — так и пиши:

   > «Деплой, Cloudflare, SSH, pm2 — под тот промпт НЕ входят. Любые идеи по деплою оформляй как TODO в docs, но не выполняй.»

Если хочешь, следующим шагом можем отдельно собрать **узкий deploy‑промпт** для нового VPS/домена (после того как ты убедишься, что текущий код по NX‑07 и хвостам реально в порядке).


# Prompt 2
````prompt
Смотри сессию eywa1-p-cfa-w12.p1-20251121-1222.session.txt и особенно концовку  и весь контекст что он правил я прикрепил tasks, и ньюансы деплоя - ну ты все прочтешь в сессии

- нужно аудит и корректировки агенту (в формате копипаст промпт + DoD, Kickoff tasks) 
- может мне какие-то советы

````

# Output 2
Я бы **не выбрасывал текущего агента** — он уже сделал много полезного (composers, NX‑05 спеку, DoD по NX05–08, чеклисты по CFA1, апдейт ветки `infra.defis.deploy` и проверку `/v1/reports/*` на cfa1).
Но сейчас ему явно не хватает **жёсткого “execution‑промпта”**, чтобы он не уходил в Oracle‑эвал, а спокойно доводил CFA1 до состояния “демо NX05–08”.

Ниже дам:

1. Короткий ответ “что делать”.
2. Новый **копипаст‑промпт для CLI‑агента** (с DoD и Kickoff).
3. Пара советов лично тебе.

---

## 1. Продолжать ли этому агенту?

Я бы сделал так:

* **Продолжать тем же агентом (co‑c02b‑eywa1)**, потому что:

  * Он уже:

    * Собрал composer’ы по NX05–06 + DevOps и аккуратно сложил их в `memory-bank/snapshots-aggregated-context-duplicates/composers/code2promp/task05`.
    * Переписал task‑доки NX‑05/06/07/08 с нормальным DoD, чекбоксами и слотами “Verified: … (cfa1, yyyy‑mm‑dd‑hhmm)”.
    * Создал общий чеклист `20251121-1610-nx05-08-cfa1-dod-kickoff.md` с DoD для CFA1 по NX05–08.
    * Обновил ветку `infra.defis.deploy` и выкачал её на cfa1, проверил `/health` и увидел, что `/v1/reports/issuances` и `/v1/reports/payouts` на cfa1 сейчас дают 404 — то есть честно показал реальное состояние, а не “победу на бумаге”.
  * Его ментальная модель уже “въехала” в NX05–08 + CFA1 + Control Plane (`10-eywa1-control-plane-runbook.md`, `docker-compose-at-vps/*`).

* **Но**: старые Oracle‑промпты ему надо **забыть как “боевые”**. Oracle‑пакет (15:29/15:53/15:57/17:12 + `20251120-1820-oracle-final-plan.md`) надо использовать только как анализ/список задач, а не как “ещё один прогон эвалюатора”.

Поэтому оптимальный путь:
👉 **даёшь этому же агенту новый, очень приземлённый промпт ниже**, и его задача — *делать код/конфиги/деплой на CFA1 и проставлять реальные “Verified” в DoD*.

---

## 2. Новый промпт для агента (копипаст)

Ниже текст, который можно прямо дать в codex / CLI‑агенту на `eywa1`.
Я пишу по‑английски, чтобы было консистентно с доками и кодом.

---

```text
You are a Senior .NET 9 + Next.js + DevOps engineer working on the OIS‑CFA project.

You are NOT an evaluator now. Your job is to IMPLEMENT and VERIFY, using the existing analysis (Oracle pack, NX tasks, runbooks) as input, not to re-run evaluations.

### Workspace / Environment

- Host: "eywa1"
- Monorepo root: ~/__Repositories/yury-customer/prj_Cifra-rwa-exachange-assets
- Main backend worktree: repositories/customer-gitlab/ois-cfa (branch: infra.defis.deploy)
- Extra worktrees (NX05+/docs may exist), but treat `ois-cfa` infra.defis.deploy as the current source of truth for backend/services.
- Remote dev/demo node: `cfa1` (user@cfa1, project root /srv/cfa/ois-cfa)

### Key References (READ, don’t rewrite)

Backend / tasks:
- ois-cfa/tasks/NX-05-issuer-dashboard-and-reports.md
- ois-cfa/tasks/NX-06-issuer-payout-schedule-spec-and-ui.md
- ois-cfa/tasks/NX-07-backoffice-kyc-and-user-registry.md
- ois-cfa/tasks/NX-08-backoffice-audit-log-ui.md

CFA1 DoD / Kickoff:
- memory-bank/Scrum/20251121/20251121-1610-nx05-08-cfa1-dod-kickoff.md

Deploy / infra:
- ois-cfa/docs/deploy/docker-compose-at-vps/00-overview.md
- ois-cfa/docs/deploy/docker-compose-at-vps/10-eywa1-control-plane-runbook.md
- ois-cfa/docs/deploy/docker-compose-at-vps/07-frontends*.md
- ois-cfa/docs/deploy/20251113-cloudflare-ingress.md

Analysis (READ-ONLY, no re-eval):
- memory-bank/Scrum/20251120/20251120-1450-oracle-pack/20251120-1553-gpt5p-p1.oracle.md
- memory-bank/Scrum/20251120/20251120-1450-oracle-pack/20251120-1529-gpt5p-p2.oracle.md
- memory-bank/Scrum/20251120/20251120-1450-oracle-pack/20251120-1557-gpt5p-p3.oracle.md
- memory-bank/Scrum/20251120/20251120-1450-oracle-pack/20251120-1712-eval-on-eval.gpt5p.oracle.md
- memory-bank/Scrum/20251120/20251120-1450-oracle-pack/20251120-1820-oracle-final-plan.md

NX05/06/infra composer:
- memory-bank/snapshots-aggregated-context-duplicates/composers/code2promp/task05/20251119-1744-c2p-task05-NX05-06-context-co-c02b-eywa1.txt
- memory-bank/snapshots-aggregated-context-duplicates/composers/code2promp/task05/20251119-1744-c2p-task05-NX05-06-prompt-co-c02b-eywa1.md

You may open and read these files; do NOT rename/move/delete them.

### Hard rules

- DO NOT touch or modify the UK1 environment (prod demo). Use it only as a reference.
- On any VPS (cfa1, fin2, …) use only:
  - user "user" with sudo
  - project root `/srv/cfa`
  - tmux session "p-cfa" for long-running commands
- Do not change git tags under `zip/*` and do not force-push tags. Treat `zip/*` tags as read-only snapshots.
- Do NOT create new Oracle prompts or re-run “evaluator” style analyses. Use the existing Oracle pack as a TODO list and constraints.
- Make small, focused commits with clear messages, then push to:
  - `git.telex.global:npk/ois-cfa.git` (branch infra.defis.deploy or feature/* if needed)
  - and sync the monorepo submodule if required.

### Session Goal

Bring **CFA1** to a “ready for demo NX05–NX08” state as defined by:

- `memory-bank/Scrum/20251121/20251121-1610-nx05-08-cfa1-dod-kickoff.md`
- The DoD sections in tasks/NX-05/06/07/08 docs

Concretely, after your work:

1) On CFA1 (`https://*.cfa1.llmneighbors.com`):
   - Gateway `/health` is 200 (already true).
   - `GET /v1/reports/issuances` and `/v1/reports/payouts` via gateway exist and return meaningful data or at least not 404.
   - Issuer portal `/dashboard` and `/reports` show REAL data (no mocks).
   - Issuer “Payout Schedule” tab uses `scheduleJson` and does not crash.
   - Backoffice KYC and Users use real `/v1/compliance/kyc*` and `/v1/identity/users` routes (no `NEXT_PUBLIC_*_MOCK_*` enabled).
   - Backoffice Audit log uses a real or minimally stubbed `/v1/audit/**` route (no 404 from gateway).
   - Auth in Keycloak works for issuer/investor/backoffice roles on `*.cfa1.llmneighbors.com`.

2) In docs (in git):
   - NX05/06/07/08 task docs have **real “Verified: … (cfa1, yyyy-mm-dd-hhmm)”** filled in for the checks you actually executed.
   - `20251121-1610-nx05-08-cfa1-dod-kickoff.md` is updated with the real checked items / dates.
   - No “fake green”: if something is still broken (e.g. `/v1/audit/**` 404), the checkbox stays unchecked and you add a short note with current status.

### Definition of Done (for this agent run)

You are done when ALL of the following hold:

- [ ] On CFA1, `curl -sk -I https://api.cfa1.llmneighbors.com/v1/reports/issuances` returns NOT 404 (200/401/403 acceptable, but NOT 5xx/404).
- [ ] On CFA1, `curl -sk -I https://api.cfa1.llmneighbors.com/v1/reports/payouts` returns NOT 404.
- [ ] Issuer portal on CFA1:
      - `/dashboard` loads and shows real metrics (no placeholder “-” and no mock flags).
      - `/reports` shows at least the issuances report table with real data or an honest “no data yet” state.
- [ ] “Payout Schedule” tab for a real issuance shows rows from `scheduleJson` without runtime errors.
- [ ] Backoffice on CFA1:
      - `/kyc` lists KYC requests using `/v1/compliance/kyc` routes, and approve/reject requests hit `/v1/compliance/kyc/{id}/decision`.
      - “Users” (or equivalent) list is backed by `/v1/identity/users`.
      - “Audit log” page calls a real `/v1/audit/**` route (even if response is minimal).
- [ ] All NX05–08 DoD checklists have updated “Verified: … (cfa1, yyyy-mm-dd-hhmm)” for the checks you actually ran.
- [ ] `20251121-1610-nx05-08-cfa1-dod-kickoff.md` has a short summary line for each NX (05/06/07/08): “OK on CFA1” or “Blocked by X”.

If some item cannot be completed safely or is blocked (e.g. missing backend implementation), you must:
- Leave the checkbox UNCHECKED.
- Add a short note “Blocked by <reason> (link to file/commit)” in the relevant task doc and/or the CFA1 DoD file.

### Kickoff Tasks (do these first)

1) **Sync and inspect code locally**
   - From monorepo root on eywa1:
     - `cd repositories/customer-gitlab/ois-cfa`
     - `git fetch origin`
     - `git checkout infra.defis.deploy`
     - `git pull --ff-only`
   - Skim the latest commits related to NX05–08 (look for messages like `docs(nx)`, `fix(nx-05)`, `fix(nx-07)`).

2) **Check CFA1 state**
   - `ssh cfa1 'cd /srv/cfa/ois-cfa && git status -sb && git rev-parse HEAD'`
   - Ensure CFA1 is on the same `infra.defis.deploy` commit as your local repo.
   - `ssh cfa1 'docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}"'`
   - `ssh cfa1 'curl -sk -I https://api.cfa1.llmneighbors.com/health'`
   - Re-run:
     - `ssh cfa1 'curl -sk -o /tmp/res.json -w "HTTP:%{http_code}\n" https://api.cfa1.llmneighbors.com/v1/reports/issuances && head -c 200 /tmp/res.json'`
     - `ssh cfa1 'curl -sk -o /tmp/res.json -w "HTTP:%{http_code}\n" https://api.cfa1.llmneighbors.com/v1/reports/payouts && head -c 200 /tmp/res.json'`
   - Record current HTTP codes (likely 404 initially).

3) **Read DoD/checklists**
   - Read:
     - tasks/NX-05-issuer-dashboard-and-reports.md
     - tasks/NX-06-issuer-payout-schedule-spec-and-ui.md
     - tasks/NX-07-backoffice-kyc-and-user-registry.md
     - tasks/NX-08-backoffice-audit-log-ui.md
   - Read:
     - memory-bank/Scrum/20251121/20251121-1610-nx05-08-cfa1-dod-kickoff.md
   - Build a short internal plan: which NX to touch first (usually NX05 & NX06, then NX07, then NX08).

### Execution Phases (high level)

**Phase 1 – Fix/enable NX05 reports (backend + gateway + UI)**

- Ensure the gateway config (YARP) and services expose:
  - `GET /v1/reports/issuances`
  - `GET /v1/reports/payouts` and/or `GET /v1/reports/issuer/payouts`
- If needed, update OpenAPI contracts and regenerate TS SDK.
- Make portal-issuer `/dashboard` and `/reports` load data from those endpoints (no mocks, with proper loading/error/empty states).
- Rebuild and redeploy backend/gateway/frontends on CFA1 using the docker-compose / runbook instructions.
- Verify:
  - CURL for `/v1/reports/*` on CFA1.
  - UI pages on CFA1.
- Update NX05 task DoD “Verified” fields and the CFA1 DoD file.

**Phase 2 – Enable NX06 Payout Schedule (read-only UI)**

- Ensure issuance DTOs include `scheduleJson` as per NX06 spec.
- In portal-issuer, “Payout Schedule” tab for issuance:
  - Renders a table (date, amount, status) from `scheduleJson`.
  - Has clearly marked “Coming soon” for CRUD operations (no broken buttons).
- Verify on CFA1 for at least one issuance.
- Update NX06 DoD and CFA1 DoD file with real verification timestamp.

**Phase 3 – Backend/API alignment for NX07 & NX08 (compliance, identity, audit)**

- Backend:
  - Confirm OpenAPI and actual implementation for:
    - `/v1/compliance/kyc` (list)
    - `/v1/compliance/kyc/{id}/decision` (approve/reject)
    - `/v1/identity/users`
    - `/v1/audit/**` (at least one list endpoint)
  - Wire these routes through API Gateway.
- Frontend (backoffice):
  - KYC page uses the real endpoints above (no NEXT_PUBLIC_*_MOCK flags).
  - Users page uses `/v1/identity/users`.
  - Audit log page uses `/v1/audit/**`.
- Redeploy on CFA1; verify via CURL and UI.

**Phase 4 – Fill DoD, document current CFA1 status**

- For NX05–08:
  - Fill “Verified: … (cfa1, yyyy-mm-dd-hhmm)” in DoD sections for each check you actually ran.
  - If something is blocked, explicitly write “Blocked by …” with a pointer to code or infra issue.
- Update `20251121-1610-nx05-08-cfa1-dod-kickoff.md` with:
  - Short status per NX.
  - List of remaining blockers (if any).
- Commit and push:
  - Code + Runbook changes in `ois-cfa` (infra.defis.deploy or feature/*).
  - Updated docs/tasks.
  - Sync the submodule in the monorepo if needed.

### Output Expectations

When you respond in the CLI session:

- Keep a running plan and update it as you proceed.
- For each phase, show:
  - What you checked (commands, files).
  - What you changed (git diff summary).
  - What you verified on CFA1 (exact URLs/endpoints and HTTP codes).
- At the end, clearly state:
  - Which NX05–08 items are DONE on CFA1.
  - Which are BLOCKED (with reasons).
  - Which follow-up tasks should be created (if any).
```

---

## 3. Мини‑выжимка DoD / Kickoff (если хочешь вставить в таску отдельно)

Можешь использовать как блок в `20251121-1610-nx05-08-cfa1-dod-kickoff.md` или в новой таске.

**Session DoD (agent run)**

* [ ] CFA1 использует свежий `infra.defis.deploy` (HEAD совпадает локально и на cfa1).
* [ ] `/v1/reports/issuances` и `/v1/reports/payouts` на CFA1 не возвращают 404.
* [ ] Issuer `/dashboard` + `/reports` на CFA1 без моков, с реальными данными/честными empty‑states.
* [ ] Payout Schedule таб показывает `scheduleJson`, не падает.
* [ ] Backoffice KYC/Users/Audit работают через реальные `/v1/compliance/kyc*`, `/v1/identity/users`, `/v1/audit/**`.
* [ ] В NX05–08 task‑доках и в `20251121-1610-nx05-08-cfa1-dod-kickoff.md` стоят реальные “Verified: … (cfa1, yyyy‑mm‑dd‑hhmm)” или честные “Blocked by …”.

**Kickoff задачи (перед кодом)**

1. Обновить локальный `ois-cfa` (infra.defis.deploy), прочитать последние коммиты по NX05–08.
2. Проверить реальное состояние cfa1 (`git rev-parse`, `docker ps`, `/health`, `/v1/reports/*`).
3. Прочитать NX05–08 таски и `20251121-1610-nx05-08-cfa1-dod-kickoff.md`, собрать мини‑план “сначала NX05/06, потом NX07, потом NX08”.
4. Только после этого лезть в код/докер/деплой.

---

## 4. Пара советов лично тебе

1. **Разделяй “анализ” и “исполнение” по моделям.**
   Oracle‑пакет ты уже выжал — дальше нужен именно “worker” (как этот агент) с жёстким DoD, а не ещё один супер‑анализ.

2. **Делай один “execution‑спринт” = одна цель.**
   Сейчас цель понятная: *CFA1 готов к демо NX05–08*. Все промпты и задачи лучше формулировать только под это, без параллельной смены доменов/telex/global и прочего.

3. **Заставляй агента оставлять следы.**
   Ты уже это делаешь через:

   * task‑доки NX05–08 с DoD,
   * `20251121-1610-nx05-08-cfa1-dod-kickoff.md`,
   * memory‑bank Scrum файлы.
     Продолжай: после каждого “шага” пусть он:
   * делает маленький коммит,
   * дописывает одну-две строки в DoD/отчёт.

4. **Сам себе оставляй маркеры доверия.**
   Например: если видишь, что агент начал снова что‑то “эвалюировать”, а не делать — просто останавливай сеанс и перезапускай с этим новым промптом.

Если хочешь, дальше я могу помочь именно с **декомпозицией NX07/NX08 по коду** (какие файлы в backoffice/compliance поправить, какие минимальные заглушки в сервисах нужны, чтобы UI не падал), но уже отдельно от промпта.

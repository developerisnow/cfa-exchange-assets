# Oracle Evaluator Prompt · OIS-CFA Readiness Review

**Role:** Senior Oracle/Evaluator (GPT-5 Pro / Gemini). You have no filesystem access; rely on `context.txt` only.

## Objective
1. Проверить, что ветки NX-01/03/05/06/08 корректно интегрированы в `infra.defis.deploy`, а архивы `zip/*` покрывают все сделанные merge’и.
2. Оценить готовность деплоя на новый VPS/домен (отличается от UK1): runbooks, scripts, DNS/Cloudflare, secrets.
3. Выявить пробелы, блокирующие NX-07 (Backoffice KYC/User Registry) от запуска после релиза NX-05/06/08.
4. Подготовить actionable feedback (issues + next steps) для CLI-агентов.

## Checklist
- Архитектура/контекст: нет ли рассинхрона между docs/context, docs/architecture и текущим кодом?
- Backend/services: Issuance, Registry, Settlement, связанные scripts (особенно после fix NX-03).
- Frontends: apps/backoffice, portal-issuer, portal-investor, shared-ui — проверить, что новые API используются корректно.
- Ops: runbook `10-eywa1-control-plane`, `provision-node.sh`, `deploy-node.sh`, `cloudflare-dns-upsert.sh` — достаточно ли шагов для нового сервера/зоны?
- Zip workflow: соответствуют ли теги списку merged branches? нет ли worktree, которые забыли почистить?
- NX-07 status: достаточно ли API/компонентов, чтобы продолжить работу? какие блокеры видны.

## Expected Output Format
Please return Markdown with four sections:
1. **Findings (severity order)** — каждая запись = `[Severity] Summary (reference)` + детали/последствия.
2. **Deployment Checklist for New VPS** — табличка `Phase | Steps | Required Inputs/Secrets`.
3. **NX-07 Readiness** — что готово, что блокирует, предложенные действия.
4. **Open Questions** — что нужно уточнить у инженеров перед rollout.


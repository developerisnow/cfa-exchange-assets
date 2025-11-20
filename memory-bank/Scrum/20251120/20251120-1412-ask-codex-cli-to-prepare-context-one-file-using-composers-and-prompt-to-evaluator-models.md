# Task Request — Prepare Oracle Evaluator Context Package

## 🎯 Goal
Подготовить один `context.txt` и один `prompt.md` для Oracle Evaluator (модели GPT‑5 Pro или Gemini), у которой **нет доступа к файловой системе**. Контекст обязан описывать текущее состояние `infra.defis.deploy` (после слияния NX‑01/03/05/06/08), политику `zip`‑архивации веток, задачи NX‑07, а также этапы деплоя на новый сервер с другим доменом/Cloudflare.

## ✅ Definition of Done
1. Текстовый отчёт с DoD/Kickoff (этот файл) размещён в `memory-bank/Scrum/20251120/`.
2. Создан skill-файл `oracle-evaluator-context-packaging` в `.claude/skills/` с инструкциями:
   - как собирать `context.txt` + `prompt.md` при отсутствии FS доступа;
   - как ссылаться на composer файлы и zip-ветки.
3. В каталоге `memory-bank/snapshots-aggregated-context-duplicates/composers/code2promp/20251120-1412-oracle-evaluator/` лежат два файла: `context.txt` и `prompt.md`, собранные по skill`у `context-composer-repomix-code2prompt.md`.
4. Все изменения закоммичены/запушены: документация в monorepo, skill и composer‑артефакты в соответствующих репозиториях.

## 🏁 Kickoff Tasks
1. Прочитать skill `context-composer-repomix-code2prompt.md` и пример @ `memory-bank/Scrum/20251119/20251119-1618-composer-repomix-code2promp-skill-for-cli-swe-agents-codex-and-claude-to-use-effective-gathering-context.md`, чтобы повторить формат composer‑артефактов.
2. Сформулировать новый skill для Oracle Evaluator в `repositories/customer-gitlab/ois-cfa/.claude/skills/` с ссылками на zip-политику и требования к `{context}.txt`/`{prompt}.md`.
3. Собрать контекст (архитектура, деплой, zip workflow, NX‑07 статус) через `code2prompt`/ручную агрегацию → записать в `memory-bank/snapshots-aggregated-context-duplicates/composers/code2promp/20251120-1412-oracle-evaluator/context.txt`.
4. Составить `prompt.md`, который Oracle Evaluator выполнит one-shot (нужен список вопросов/проверок).
5. Проверить, что `infra.defis.deploy` синхронизирован и все ветки архивированы (теги `zip/*`).

## 📌 References
- Skill: `repositories/customer-gitlab/ois-cfa/.claude/skills/context-composer-repomix-code2prompt.md`
- Исторический пример composer‑таска: `memory-bank/Scrum/20251120/20251119-old-session-part-about-composer-task.md`
- Zip workflow doc: `repositories/customer-gitlab/ois-cfa/artifacts/git/branch-zip-workflow.md`

# Gitlab effective tooling
````prompt

````

# Output
TL;DR

* Агент **не должен руками дергать билд** — нормальный путь: пуш → GitLab сам стартует pipeline; CLI/API нужны для: а) ручной перезапуск без нового коммита, б) мониторинг статуса.
* У тебя уже есть паттерн: брать `GITLAB_USER_CICD_TOKEN` из `.env` и дергать **GitLab API v4 через curl** для lint/pipelines — этим же стилем агент может стартовать/проверять пайплайны.
* GitLab CLI `glab` — аналог `gh`, работает и с self-hosted (`GITLAB_HOST=git.telex.global`, PAT с `api` scope), но в агентном флоу проще и прозрачнее опираться на **маленькие bash-скрипты вокруг API**, чем тащить ещё один бинарь. ([GitLab Docs][1])

---

## 1. Как вообще агент должен это делать (по уму)

1. **Инициировать билд**

   Основной способ — **вообще ничего не делать**:

   * агент делает `git commit` → `git push origin dev-cfa2`;
   * GitLab по `.gitlab-ci.yml` сам стартует pipeline.
     То есть `“init build” == push`, а не отдельная команда.

   Дополнительно (когда нужен ручной прогон без нового коммита):

   * агент дергает GitLab API:

     ```bash
     # PROJECT_PATH = npk/ois-cfa
     PROJECT_PATH="npk%2Fois-cfa"
     REF="dev-cfa2"
     TOKEN="$GITLAB_USER_CICD_TOKEN"

     curl --silent \
       --header "PRIVATE-TOKEN: $TOKEN" \
       --request POST \
       "https://git.telex.global/api/v4/projects/${PROJECT_PATH}/pipeline?ref=${REF}"
     ```

     Это ровно тот же API, что описан в доках `Pipelines API` (`POST /projects/:id/pipeline?ref=main`). ([GitLab Docs][2])

   Альтернатива — **trigger token** (`/trigger/pipeline?token=...&ref=...`), если хочешь не светить полноценный PAT, но для твоего “оркестратор-агента” PAT логичнее. ([GitLab Docs][3])

2. **Проверять статус pipeline / jobs**

   У тебя уже есть живой пример: агент дергал `GET /projects/npk%2Fois-cfa/pipelines/243` и проверял JSON. 

   Минимальный набор:

   ```bash
   PROJECT="npk%2Fois-cfa"
   TOKEN="$GITLAB_USER_CICD_TOKEN"
   REF="dev-cfa2"

   # 1) взять последний pipeline по ветке
   PIPELINE_JSON=$(
     curl -s --header "PRIVATE-TOKEN: $TOKEN" \
       "https://git.telex.global/api/v4/projects/${PROJECT}/pipelines?ref=${REF}&per_page=1"
   )
   PIPELINE_ID=$(echo "$PIPELINE_JSON" | jq '.[0].id')

   # 2) дернуть подробности
   STATUS_JSON=$(
     curl -s --header "PRIVATE-TOKEN: $TOKEN" \
       "https://git.telex.global/api/v4/projects/${PROJECT}/pipelines/${PIPELINE_ID}"
   )
   STATUS=$(echo "$STATUS_JSON" | jq -r '.status')
   WEB_URL=$(echo "$STATUS_JSON" | jq -r '.web_url')

   echo "pipeline ${PIPELINE_ID} status = ${STATUS} (${WEB_URL})"
   ```

   Документация это же описывает как `GET /projects/:id/pipelines/:pipeline_id`. ([GitLab Docs][2])

   По такой же схеме можно дергать:

   * `/projects/:id/pipelines/:pipeline_id/jobs` — смотреть, прошёл ли именно `deploy-cfa2`;
   * `/pipelines/:pipeline_id/retry` — “Retry pipeline” при падении. ([GitLab Docs][2])

3. **Ждать пока pipeline дойдёт до нужного стейджа**

   Простейший wait-loop, который агент может вызывать в конце LOOP’а:

   ```bash
   wait_pipeline() {
     local project="$1"
     local pipeline_id="$2"
     local token="$3"

     while true; do
       local status=$(curl -s --header "PRIVATE-TOKEN: $token" \
         "https://git.telex.global/api/v4/projects/${project}/pipelines/${pipeline_id}" \
         | jq -r '.status')

       echo "pipeline ${pipeline_id}: ${status}"
       case "$status" in
         running|pending)
           sleep 10
           ;;
         success)
           return 0
           ;;
         failed|canceled|skipped|manual)
           return 1
           ;;
         *)
           echo "unknown status: $status"
           return 1
           ;;
       esac
     done
   }
   ```

   Агент в своём отчёте тогда честно пишет: “`pipeline 243 status = success`” (как он уже сделал).

---

## 2. GitLab CLI (`glab`) — когда и как

Если тебе комфортен `gh`-style UX, то `glab` — то же самое от GitLab:

* Умеет `glab pipeline list`, `glab pipeline view`, `glab ci lint`, `glab mr list`, `glab issue list` и т.д.([about.gitlab.com][4])
* Самое главное для self-hosted:

  * `glab auth login` → выбрать **GitLab Self-Hosted**;
  * `GitLab hostname: git.telex.global`;
  * PAT с `api` и `write_repository`;
  * либо через env `GITLAB_HOST=git.telex.global` и `GITLAB_TOKEN=...`.([GitLab Docs][1])

Пример использования:

```bash
# Локально на eywa1
export GITLAB_HOST=git.telex.global
export GITLAB_TOKEN="$GITLAB_USER_CICD_TOKEN"

# список последних пайплайнов по проекту
glab pipeline list --repo npk/ois-cfa --page 1 --per-page 5

# статус конкретного
glab pipeline view 243 --repo npk/ois-cfa

# зафейленный pipeline → retry
glab pipeline retry 243 --repo npk/ois-cfa
```

Но минусы для агентного сценария:

* надо ставить бинарь `glab` внутрь CI-образа / на eywa1, следить за версиями;
* в уже существующих скриптах ты и так строишь curl на GitLab API (agent-status, k8s-healthcheck, CI lint и пр.), так что **ещё один слой абстракции особо не даёт выигрыша**.

Поэтому мой take:

> **Для человека** (ты в терминале) — `glab` ок,
> **для Codex-агента** — маленькие bash-обёртки на GitLab API (`curl + jq`) — проще и прозрачнее.

---

## 3. Как это встроить в твой Agent Loop

### 3.1. Инициация билда

В новом AGENT_PROMPT для `cicd-ops-agent`:

* В секции PLAN/EXECUTE явно прописать:

  * “Если нужно **запустить новый pipeline** без изменений кода → используй `curl POST /projects/:id/pipeline?ref=dev-cfa2` с токеном из `.env` (`GITLAB_USER_CICD_TOKEN`)”.
  * “В остальных случаях pipeline должен стартовать от `git push` — не занимайся магией”.

### 3.2. Проверка статуса в Loop

В твоём ORACLE-контракте уже есть фраза “маленькая верификация (docker compose config, curl /health, **GitLab pipeline status**)” — сюда идеально ложится вызов описанного выше `wait_pipeline()`.

Паттерн цикла для J1/J2:

1. `{code-change}` → изменить `.gitlab-ci.yml`, compose или скрипты.
2. `{tests}` → локально хотя бы `docker compose config` и `gitlab-ci lint` (у тебя уже есть curl к `/ci/lint`).
3. `git push origin dev-cfa2`.
4. `trigger/check`:

   * либо ждать автоматический pipeline и `wait_pipeline()` по последнему ID,
   * либо явно стартануть `POST /pipeline` и подождать его.
5. `{docs/DoD-update}` → апдейт runbook/DoD.
6. `commit` (если шаги 2–5 были на черновой ветке).

---

## 4. Мини-таблица: какие варианты у тебя есть

| Что надо                     | Базовый способ                                                 | CLI-вариант                        | Где у тебя уже задействовано                       |
| ---------------------------- | -------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------- |
| Стартануть pipeline          | `git push` или `curl POST /projects/:id/pipeline?ref=dev-cfa2` | `glab pipeline run --ref dev-cfa2` | curl к lint/pipelines уже есть в w19 session       |
| Проверить статус pipeline    | `curl GET /projects/:id/pipelines/:pipeline_id`                | `glab pipeline view 243`           | ты уже делал curl к `/pipelines/243`               |
| Список jobs в pipeline       | `curl GET /projects/:id/pipelines/:pipeline_id/jobs`           | `glab ci status` / `glab job list` | планируешь использовать для проверки `deploy-cfa2` |
| Рестартнуть упавший pipeline | `curl POST /projects/:id/pipelines/:pipeline_id/retry`         | `glab pipeline retry`              | пока не используется                               |
| Триггер по token’у (без PAT) | `curl POST /projects/:id/trigger/pipeline?token=...&ref=...`   | —                                  | можно завести на будущее для внешних систем        |

---

## 5. Next actions для тебя

1. **Определиться с подходом:**

   * Для агентов — зафиксировать в oracle-файле, что **primary tool = curl + GitLab API**;
   * `glab` держать как human-tool на твоей машине (если захочешь), но не как hard-dependency для CI.

2. **Сделать маленький helper-скрипт `ops/scripts/gitlab-pipeline-utils.sh`:**

   * функции `trigger_pipeline`, `last_pipeline_for_ref`, `wait_pipeline`;
   * брать `GITLAB_USER_CICD_TOKEN` и `PROJECT_PATH` из `.env`/env.
     Это потом легко дергать и из Codex-loop, и вручную.

3. **В AGENT_PROMPT для cicd-агента:**

   * Прямо прописать:

     * “После `git push dev-cfa2` **обязан** вызвать `wait_pipeline dev-cfa2` и вписать статус/URL в отчёт.”
     * “Если нужно пустой прогон без изменений — используй `trigger_pipeline dev-cfa2`.”

4. **Если всё-таки хочешь `glab` (для себя):**

   * На macOS: `brew install glab`;
   * `glab auth login` → GitLab Self-Hosted → host `git.telex.global`, PAT с `api`;
   * Проверка: `glab pipeline list --repo npk/ois-cfa`. ([UW Computer Sciences][5])

Если хочешь, дальше могу просто выдать готовый `ops/scripts/gitlab-pipeline-utils.sh` + кусок AGENT_PROMPT, где он обязателен в каждом LOOP’е — чтобы ты только вставил и закоммитил.

[1]: https://docs.gitlab.com/cli/?utm_source=chatgpt.com "GitLab CLI (glab)"
[2]: https://docs.gitlab.com/api/pipelines/?utm_source=chatgpt.com "Pipelines API"
[3]: https://docs.gitlab.com/ci/triggers/?utm_source=chatgpt.com "Trigger pipelines with the API"
[4]: https://gitlab.com/gitlab-org/cli?utm_source=chatgpt.com "GitLab.org / cli"
[5]: https://pages.cs.wisc.edu/~pmilton/?utm_source=chatgpt.com "Using glab-cli"

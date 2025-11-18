# Prompt
You are Oracle, a focused one-shot problem solver. Emphasize direct answers, cite any files referenced, and clearly note when the search tool was used.  You are GPT‑5 Pro acting as a senior meta‑architect specifically for **RepoScan v1** in my AI‑assisted workspace.  Context (you already saw parts of it in previous calls, but here we focus on RepoScan only): - I have a personal mono‑repo (`prj_Cifra-rwa-exachange-assets`) with manifests, memory-bank and submodules like `ois-cfa`. - `ois-cfa` is the main team repo where domain code lives; mono‑repo is my control plane (manifests, AGENTS, workflows, AI experiments) and must not leak into customer repos. - I want a **RepoScan v1** that produces compact JSON snapshots per repo (e.g. `ois-cfa`) that agents can use as “map of the territory”: structure, domains, Trunk/Branch/Leaf mapping, key files. - I already experimented with Shotgun‑style SDD/RepoScan and have a lot of context in the attached code2prompt files.  I have attached: - `c2p_20251118-0905-context-reposcan-agents-structure-and-codemachine.txt`: aggregated context for RepoScan+Agents+CodeMachine (read this first for my high‑level intent); - `c2p_reposcan.txt`: snapshot of current RepoScan ideas/experiments (Shotgun‑style, SDD, JSON snapshots); - `c2p_ois-cfa.txt`: snapshot of the `ois-cfa` repo (branch `infra.defis.deploy`) — use it as the main concrete example for RepoScan output; - `20251117-2103-gpt5pro-step4-all-and-nextsteps.gpt5p.md`: your previous V4‑style audit that already touches Trunk/Branches/Leaves and NX‑00..NX‑08; - `20251118-0905-feedback-gpt5pro-step4-all.md`: my spoken feedback where I explicitly mention RepoScan, JSON snapshots, tagging, and the need for a single JSON “map” for agents.  **High-level ask for this call:**  Design **RepoScan v1** as a JSON‑based artefact and a small pipeline that: - can be generated for repos like `ois-cfa` (and later others); - encodes Trunk/Branch/Leaf in a way that is easy for agents to consume; - is compact enough to be used as high‑value context (not full source dump); - fits nicely into the broader OS you already sketched (Trunk/Branches/Leaves, NX‑00..NX‑08, CodeMachine, Agents).  What I need from you:  1) **RepoScan v1 – conceptual goals and constraints**    - In Russian (B2‑English terms OK), summarise in 5–8 bullets:      - what RepoScan v1 SHOULD and SHOULD NOT do;      - how it relates to Trunk/Branches/Leaves and NX‑00..NX‑08 (i.e. whether it is Trunk‑level artefact, how often to regenerate, who can touch it);      - how it should be used by agents vs humans.  2) **High‑level JSON structure for `reposcan.json`**    - Propose a JSON structure for `reposcan.json` (per repo), focusing on key fields only.    - Required parts (adapt/extend as needed):      - repo metadata (id, path, default branch, domains);      - tree of directories/files with minimal attributes (kind, size/class, tags, Trunk/Branch/Leaf level);      - logical groupings (domains, services, frontends, packages, ops, tests);      - references to “anchor” docs (e.g. `docs/context/*`, AGENTS, manifests);      - optional metrics (LOC buckets, test counts, etc.) if useful.    - Express this as a pseudo‑JSON schema (field names, types, nesting) + 1–2 small example fragments for `ois-cfa` (e.g. how `services/issuance` and `apps/backoffice` would appear).  3) **Trunk/Branch/Leaf encoding inside RepoScan**    - Explain how you would embed Trunk/Branch/Leaf semantics into `reposcan.json`:      - per node (field like `level: "trunk"|"branch"|"leaf"`?);      - via tags (e.g. `tags: ["domain:issuance", "level:branch"]`?);      - via separate sections (e.g. `trunk_nodes`, `branch_nodes`, `leaf_nodes`).    - Recommend ONE approach you think is most robust for agents and humans, and justify why.    - Provide 2–3 concrete examples (again using `ois-cfa` paths) that show how agents could:      - find all trunk‑level artefacts;      - find all leaf‑level test files for a given service;      - map a `tasks/NX-*` doc to concrete code locations via RepoScan.  4) **RepoScan generation pipeline (v1)**    - Design a minimal pipeline (CLI/tools/scripts, not full implementation) to generate `reposcan.json` for `ois-cfa` on macOS/eywa1:      - inputs (git repo root, list of ignore patterns, maybe existing SDD/Shotgun JSON);      - steps (scan FS → classify nodes → attach Trunk/Branch/Leaf levels → merge with existing manifests if needed → write `reposcan.json`);      - outputs (where to store `reposcan.json` in mono‑repo, how to version it, how often to regenerate).    - Output as:      - bullet list of steps;      - 1 Mermaid diagram showing the pipeline (FS → scanner → classifier → reposcan.json → agents).  5) **How agents and CodeMachine should consume RepoScan v1**    - Describe 5–10 typical usage patterns for RepoScan v1 by agents:      - planning (GPT‑5)      - implementation (Codex/Claude)      - review (GPT‑5)      - safety checks (where NOT to touch, based on level/tags).    - For each pattern, give:      - short name (e.g. “Find leaf tests for NX‑03”);      - 1–2 sentence description;      - which fields of `reposcan.json` are used.  Style & format: - Answer in Russian, with senior‑engineer tone; B2‑English terms OK. - Structure your answer as:   - TL;DR (3–5 bullets),   - Section 1: RepoScan v1 goals & constraints,   - Section 2: JSON structure for reposcan.json,   - Section 3: Trunk/Branch/Leaf encoding,   - Section 4: Generation pipeline,   - Section 5: Consumption patterns for agents/CodeMachine,   - Final compact table: `Area` / `Decision` / `Your recommendation`. - Do NOT restate all attached files; focus on synthesis and **executable** design.
# Output 
Я уже прогнал внутренний `file_search` по твоим файлам (`c2p_reposcan`, контекст RepoScan+CodeMachine, V3/V4‑отчёты по Trunk/Branch/Leaf, AGENTS/manifest, c2p_ois-cfa). Ниже опираюсь на существующие Shotgun‑репоскан JSON’ы по Hypetrain и `ois-cfa`, твой голосовой фидбэк про “один JSON‑снимок как карту” и T/B/L‑рамку.

---

## TL;DR

* RepoScan v1 = **авто‑генерируемый `reposcan.json` на репо/ветку**, живущий в монорепе, который даёт агентам карту: дерево путей, домены/сервисы/опсы, якорные доки и NX‑линки, с пометкой Trunk/Branch/Leaf по каждому узлу.
* Это **Trunk‑артефакт схемы**, но с содержимым уровня Branch/Leaf: редактировать руками нельзя, только генератор; регенерация — после крупных NX‑срезов и merge’ей, не на каждый коммит.
* Внутри: `meta + repo + summary + nodes + groups + anchors + nx_index`. `nodes` = только ключевые директории/файлы (services/apps/packages/docs/ops/tests), каждый с полями `kind/size_class/level/tags/domain`. NX‑таски явно связаны через `nx_index`.
* Trunk/Branch/Leaf кодируется **per‑node: `level: "trunk"|"branch"|"leaf"` + доп. `tags`**, без отдельных секций; это максимально просто для агентов: один проход по `nodes` для фильтрации.
* Pipeline v1: CLI‑скрипт в монорепе → сканирует рабочий tree `ois-cfa` на нужной ветке, классифицирует пути, вешает T/B/L и домены, строит groups/anchors/nx_index → пишет `snapshots/reposcan/ois-cfa/{branch}.reposcan.json`. Потом это читает CodeMachine/агенты как первичную “карту репо”.

---

## 1. RepoScan v1: цели и ограничения

**Что RepoScan v1 ДОЛЖЕН делать**

1. **Дать агентам “map of territory” одним JSON‑файлом на репо/ветку** — без повторного чтения всего c2p‑дампа. На входы агентов (GPT‑5/Claude/Codex/CodeMachine) всегда можно добавить 5–15к токенов `reposcan.json` как стабильный контекст.
2. **Нормализовать структуру под твой T/B/L‑фреймворк**: явно показывать, какие узлы относятся к Trunk (контракты, ключевые доки, runbook’и), какие к Branch (services/apps/ops‑каркас), какие к Leaf (тесты, UI‑слайсы, скрипты).
3. **Дать групповку по доменам/сервисам/фронтам/опсам/тестам**, чтобы агент мог быстро: “дай всё по issuance”, “дай всё по backoffice”, “какие тесты покрывают registry”.
4. **Связать NX‑таски с кодом и доками**: `nx_index` с привязкой `NX-03 → services/issuance + tests/issuance.Tests + contracts/openapi-issuance.yaml + docs/context/WBS-OIS`.
5. **Выделить “anchor docs”** (PROJECT/FRONTEND/WBS/UK1‑ингресс/SMTP, AGENTS‑правила для этого репо) отдельным списком, чтобы планирующий агент начинал с них, а не шарился по всему `docs/`.
6. **Быть компактным**: держать JSON в “архитектурной” зоне — сервисы/директории/ключевые файлы и агрегированные метрики, но не выгружать каждую строку кода. Shotgun‑SDD останется отдельным тяжёлым артефактом.

**Что RepoScan v1 НЕ ДОЛЖЕН делать**

7. **Не быть SDD/описанием поведения** — он не генерирует “романы” про домены, как Shotgun‑репоскан для Hypetrain/OIS‑CFA; только ссылки и компактные описания.
8. **Не хранить чувствительные данные и монорепо‑внутрянку**: только относительные пути внутри конкретного репо (`ois-cfa` и пр.), без абсолютных путей и без ссылок на твою личную монорепу в тексте. Монорепа хранит `reposcan.json`, но сам JSON ничего не знает о ней.
9. **Не редактироваться руками** — schema‑trunk, содержимое — результат генерации; правки только через изменение кода/структуры + регенерацию.

**Связь с Trunk/Branches/Leaves и NX‑00..NX‑08**

* **Уровень:** схема `reposcan.json` — Trunk‑уровень (часть “каркаса инструментов”), экземпляры (`reposcan.json` для конкретного репо/ветки) — ближе к Branch (отражают текущее состояние кода).
* **Кто трогает:** только ты/топ‑инженер через generator‑CLI и NX‑00‑таски (описание схемы и конфига генерации). Остальные — только читают.
* **Когда регенерировать:** в конце NX‑веток, перед большими MR в `infra.defis.deploy`/`develop`, перед крупными CodeMachine‑прогонами; плюс периодически (например, daily/weekly job) — но не на каждый commit.
* **Роль для агентов:**

  * планирующие GPT‑5 агенты читают `summary/groups/anchors/nx_index` чтобы собрать задачу и список файлов;
  * Codex/Claude Code читает `nodes` и вытаскивает уже конкретные файлы/директории для редактирования;
  * safety‑агент использует `level/tags` чтобы отсечь Trunk‑узлы от автогенерации.
* **Роль для людей:** быстрый “index view”: посмотреть, что генератор считает Trunk/Branch/Leaf, где лежат якорные доки, какие NX связаны с какими участками.

---

## 2. JSON‑структура `reposcan.json`

### 2.1. Общий псевдо‑schema

```jsonc
{
  "schema": "reposcan-1.0",       // версия схемы репосканов
  "repo": {                       // метаданные репозитория
    "id": "ois-cfa",              // короткий id (GitLab name)
    "root": "repositories/customer-gitlab/ois-cfa", // путь внутри монорепы
    "default_branch": "infra.defis.deploy",
    "scanned_ref": "ed44ee6",     // git SHA
    "branch": "infra.defis.deploy",
    "generated_at": "2025-11-18T09:30:00Z",
    "generator": "reposcan-cli@0.1.0"
  },
  "summary": {                    // агрегированные метрики
    "domains": ["identity","issuance","registry","settlement","compliance"],
    "loc": {
      "total": 85000,
      "by_language": { "csharp": 55000, "typescript": 25000, "yaml": 5000 }
    },
    "counts": {
      "services": 5,
      "apps": 4,
      "packages": 4,
      "ops_areas": 3,
      "test_suites": 6
    }
  },
  "nodes": {                      // дерево узлов (только важные dirs/files)
    "services/issuance": {
      "kind": "dir",              // dir | file
      "name": "issuance",
      "level": "branch",          // trunk | branch | leaf
      "domain": "issuance",
      "role": "service",          // service | app | package | ops | tests | doc | config | misc
      "size_class": "L",          // XS/S/M/L/XL по LOC/файлам
      "loc": 8000,
      "tags": ["backend","service","domain:issuance"],
      "children": [
        "services/issuance/Program.cs",
        "services/issuance/IssuanceDbContext.cs"
      ]
    },
    "apps/backoffice": {
      "kind": "dir",
      "name": "backoffice",
      "level": "branch",
      "domain": null,
      "role": "app",
      "size_class": "M",
      "loc": 6000,
      "tags": ["frontend","backoffice","ui"],
      "children": [
        "apps/backoffice/next.config.mjs",
        "apps/backoffice/src/app/page.tsx"
      ]
    },
    "tests/issuance.Tests/IssuanceApiTests.cs": {
      "kind": "file",
      "name": "IssuanceApiTests.cs",
      "level": "leaf",
      "domain": "issuance",
      "role": "tests",
      "size_class": "S",
      "loc": 400,
      "tags": ["xunit","backend","NX-03"]
    }
    // …
  },
  "groups": {                     // логические группировки
    "domains": {
      "issuance": {
        "services": ["services/issuance"],
        "apps": ["apps/portal-issuer"],
        "contracts": ["packages/contracts/openapi-issuance.yaml"],
        "tests": [
          "tests/issuance.Tests",
          "tests/e2e-playwright/issuer-issuance-flow.spec.ts"
        ]
      },
      "registry": {
        "services": ["services/registry"],
        "apps": ["apps/portal-investor"],
        "contracts": ["packages/contracts/openapi-registry.yaml"],
        "tests": ["tests/contracts/pact-consumer/gateway-to-registry.test.ts"]
      }
      // …
    },
    "services": [
      { "name": "issuance", "root": "services/issuance", "domain": "issuance", "level": "branch" },
      { "name": "registry", "root": "services/registry", "domain": "registry", "level": "branch" }
    ],
    "apps": [
      { "name": "portal-issuer", "root": "apps/portal-issuer", "level": "branch" },
      { "name": "backoffice", "root": "apps/backoffice", "level": "branch" }
    ],
    "ops": [
      { "name": "uk1", "root": "docs/deploy/20251113-cloudflare-ingress.md", "level": "trunk" },
      { "name": "k8s-timeweb", "root": "ops/infra/timeweb", "level": "branch" }
    ]
  },
  "anchors": [                    // “якорные” доки и файлы
    {
      "path": "docs/context/PROJECT-CONTEXT.md",
      "role": "project-context",
      "level": "trunk",
      "tags": ["anchor","context"]
    },
    {
      "path": "docs/context/WBS-OIS.md",
      "role": "wbs",
      "level": "trunk",
      "tags": ["anchor","wbs","nx"]
    },
    {
      "path": "docs/deploy/20251113-cloudflare-ingress.md",
      "role": "runbook:uk1",
      "level": "trunk",
      "tags": ["anchor","ops","uk1"]
    },
    {
      "path": "tasks/NX-03-issuance-coverage.md",
      "role": "nx-task",
      "level": "branch",
      "tags": ["nx","issuance"]
    }
  ],
  "nx_index": {                   // явная привязка NX‑тасков
    "NX-01": {
      "title": "Spec validation + API/Event Matrix",
      "task_doc": "tasks/NX-01-spec-matrix.md",
      "level": "branch",
      "domains": ["cross-cutting"],
      "nodes": [
        "packages/contracts",
        "docs/context/WBS-OIS.md",
        "docs/ops/api-event-matrix.md"
      ]
    },
    "NX-03": {
      "title": "Issuance endpoints alignment + tests",
      "task_doc": "tasks/NX-03-issuance-coverage.md",
      "level": "branch",
      "domains": ["issuance"],
      "nodes": [
        "services/issuance",
        "tests/issuance.Tests",
        "packages/contracts/openapi-issuance.yaml"
      ]
    }
    // …
  }
}
```

### 2.2. Примеры для `services/issuance` и `apps/backoffice` (фрагмент)

```jsonc
{
  "nodes": {
    "services/issuance": {
      "kind": "dir",
      "name": "issuance",
      "level": "branch",
      "domain": "issuance",
      "role": "service",
      "size_class": "L",
      "loc": 8000,
      "tags": ["backend","service","domain:issuance"],
      "children": [
        "services/issuance/Program.cs",
        "services/issuance/IssuanceDbContext.cs",
        "services/issuance/Controllers/IssuanceController.cs"
      ]
    },
    "apps/backoffice": {
      "kind": "dir",
      "name": "backoffice",
      "level": "branch",
      "domain": null,
      "role": "app",
      "size_class": "M",
      "loc": 6000,
      "tags": ["frontend","backoffice","admin-ui"],
      "children": [
        "apps/backoffice/next.config.mjs",
        "apps/backoffice/src/app/page.tsx",
        "apps/backoffice/src/app/(kyc)/kyc/page.tsx"
      ]
    }
  },
  "groups": {
    "domains": {
      "issuance": {
        "services": ["services/issuance"],
        "apps": ["apps/portal-issuer"],
        "contracts": ["packages/contracts/openapi-issuance.yaml"],
        "tests": ["tests/issuance.Tests"]
      }
    }
  }
}
```

Это даёт агенту очень быстрый путь: “issuance” → service, spec, tests, UI‑флоу; “backoffice” → app + связанные NX‑таски.

---

## 3. Встраивание Trunk/Branch/Leaf в `reposcan.json`

### 3.1. Варианты

1. **Per‑node поле `level`**

   * Плюсы: одна точка правды; простая фильтрация (`nodes[path].level === "leaf"`).
   * Минусы: нет явного перечня всех trunk/branch/leaf узлов (но можно получить в один проход).

2. **Через `tags` (например, `tags: ["level:branch"]`)**

   * Плюсы: гибко; не надо отдельное поле.
   * Минусы: повышает риск рассинхрона (`tags` сказали одно, `level` другое), требует более сложных запросов для агентов.

3. **Отдельные секции (`trunk_nodes`, `branch_nodes`, `leaf_nodes`)**

   * Плюсы: человеку удобно глазами.
   * Минусы: дублирование узлов, сложнее поддерживать, большие diffs.

### 3.2. Рекомендация

**Выбираем вариант 1: `level` на каждом узле + при желании дублирующий тег.**

Причины:

* Агенты чаще всего будут делать простые запросы: “дай все leaf‑тесты для services/issuance” → фильтр по `level === "leaf"` и `role === "tests"` и `domain === "issuance"`.
* Вся T/B/L‑архитектура у тебя уже оформлена именно как per‑элемент атрибут (см. таблицу уровней и диаграммы).
* Отдельные списки trunk/branch/leaf можно, если нужно, построить на лету или закешировать вне `reposcan.json`.

### 3.3. Примеры использования

#### 3.3.1. Найти все trunk‑артефакты

Псевдо‑запрос для агента:

* **Фильтр:** `nodes[path].level === "trunk"` ИЛИ `path` присутствует в `anchors` с `level: "trunk"`.

Например, получим:

```jsonc
[
  "docs/context/PROJECT-CONTEXT.md",
  "docs/context/WBS-OIS.md",
  "docs/deploy/20251113-cloudflare-ingress.md",
  "packages/contracts/openapi-issuance.yaml",
  "packages/contracts/openapi-registry.yaml"
]
```

Дальше планирующий агент уже знает: сначала читает PROJECT/WBS/контракты, потом идёт на Branch/Leaf.

#### 3.3.2. Найти все leaf‑тесты для конкретного сервиса

Цель: “листовые тесты для `services/issuance`”.

1. По `groups.domains.issuance.tests` получаем список тестовых корней: `"tests/issuance.Tests"`, `"tests/e2e-playwright/issuer-issuance-flow.spec.ts"`.
2. По `nodes` фильтруем все ключи, которые начинаются с этих путей **и** имеют `level: "leaf"` и `role: "tests"`.
3. Результат: конкретные файлы, которые можно добавить в контекст или править:

```jsonc
[
  "tests/issuance.Tests/IssuanceApiTests.cs",
  "tests/e2e-playwright/issuer-issuance-flow.spec.ts"
]
```

#### 3.3.3. Привязать `tasks/NX-*` к коду через RepoScan

Например, NX‑03 (issuance):

1. В `nx_index["NX-03"]` видим `nodes`: `"services/issuance"`, `"tests/issuance.Tests"`, `"packages/contracts/openapi-issuance.yaml"`.
2. Агенты:

   * Planner: берёт `task_doc`, читает постановку задачи + смотрит `nx_index["NX-03"].nodes` и `groups.domains.issuance` для контекста.
   * Implementer: по этим путям берёт нужные файлы (Program.cs, DbContext, тесты) и начинает править, не вылезая за пределы домена.

---

## 4. Pipeline RepoScan v1

### 4.1. Inputs / Outputs

**Inputs**

* `repo_root`: путь к рабочему дереву репо (`…/repositories/customer-gitlab/ois-cfa`).
* `branch`: например, `infra.defis.deploy` (или любой другой checked‑out worktree). 
* `ignore_patterns`: `.git`, `bin`, `obj`, `node_modules`, `dist`, `TestResults`, `coverage`, `memory-bank/*`, `ARCHIVE/*` (настраивается).
* Опционально: путь к существующему Shotgun‑SDD JSON (`*.shtgn.reposcan.json`) — чтобы при желании тянуть описания доменов/контейнеров в `summary`.

**Outputs**

* `snapshots/reposcan/ois-cfa/infra.defis.deploy.reposcan.json` — в корне монорепы (НЕ в самом `ois-cfa`).
* Дополнительно: маленький `index.json` по всем репо/веткам для быстрой навигации агентом.

### 4.2. Шаги pipeline (CLI/скрипт)

1. **Init & Git‑метаданные**

   * Определить `repo.id`, `branch`, `scanned_ref` (через `git rev-parse HEAD` в worktree), `default_branch`.
   * Прочитать базовые домены/сервисы из `docs/context/PROJECT-CONTEXT.md` и `WBS-OIS.md`.

2. **Scan FS**

   * Рекурсивно пройти по `repo_root` с учётом `ignore_patterns`.
   * Для каждого каталога/файла собрать: относительный `path`, `kind`, примерный `loc` (по быстрым heuristics), язык (по расширению).

3. **Classification (role/domain/level)**

   * По пути и имени определить `role`:

     * `services/*` → `role: "service"`, domains по имени (`issuance`, `registry`, …).
     * `apps/*` → `role: "app"`.
     * `packages/contracts/*` → `role: "package"` + domain из имени контракта. 
     * `docs/context/*` → `role: "doc"`.
     * `ops/*` и `docs/deploy/*` → `role: "ops"`.
     * `tests/*` → `role: "tests"`.
   * Назначить `level`:

     * Trunk: контракты, главные контекст‑доки и ключевые runbook’и (UK1, k8s‑baseline, AGENTS‑локальные правила).
     * Branch: сервисные и app‑директории, ops/infra, gitops, CI‑файлы.
     * Leaf: конкретные тестовые файлы, UI‑слайсы, отдельные конфиги и скрипты.

4. **Build groups**

   * Собрать `groups.domains` исходя из `domain`/`role`.
   * Построить списки `services`, `apps`, `ops` (корни).
   * Выделить UK1 и другие окружения как отдельные ops‑entry (`docs/deploy/20251113-cloudflare-ingress.md`, `ops/infra/timeweb/*`).

5. **Detect anchors**

   * По whitelist’у (PROJECT‑CONTEXT, FRONTEND‑CONTEXT, WBS‑OIS, RULES‑SUMMARY, ключевые deploy/ops‑доки, локальный AGENTS для репо) собрать `anchors[]`.

6. **Build `nx_index`**

   * Для каждой `tasks/NX-*.md` прочитать заголовок и ключевые “Scope/Touches” (если уже есть) или вывести из имени.
   * По шаблонам (`NX-03` → issuance; `NX-04` → registry/settlement; `NX-06` → CI) связать с соответствующими `nodes` и доменами.

7. **Serialize & write**

   * Собрать всё в структуру из раздела 2, отсортировать ключи для стабильных diff’ов.
   * Записать в `snapshots/reposcan/ois-cfa/{branch}.reposcan.json`.
   * Добавить мини‑index в `snapshots/reposcan/index.json`.

### 4.3. Mermaid диаграмма pipeline

```mermaid
flowchart LR
    FS[Repo FS\n(ois-cfa@infra.defis.deploy)] --> SCAN[Scanner\n(FS walk + LOC)]
    SCAN --> CLASS[Classifier\nrole/domain/level]
    CLASS --> GROUPS[Groups & Anchors\n(domains/apps/ops/NX)]
    GROUPS --> JSON[reposcan.json\n(per repo/branch)]
    JSON --> AGENTS[Agents & CodeMachine\n(plan/impl/review/safety)]
```

---

## 5. Как агенты / CodeMachine потребляют RepoScan v1

Ниже — паттерны использования; это можно почти копировать в AGENTS/внутренние доки.

| Pattern (short name)              | Description                                                                                                                                  | Fields used                                                               |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **1. Plan NX‑task scope**         | GPT‑5‑планировщик берёт `nx_index[NX-*]`, смотрит связанные `nodes` и `anchors`, чтобы собрать минимальный список файлов/доков для задачи.   | `nx_index`, `nodes`, `groups.domains`, `anchors`                          |
| **2. Domain slice for service**   | Агенту нужно понять “всё по issuance/registry”: он читает `groups.domains[domain]` и строит контекст из сервисов, контрактов, тестов, UI.    | `groups.domains`, `nodes`, `summary.domains`                              |
| **3. Find leaf tests for change** | Перед изменением в `services/issuance` агент запрашивает все `nodes` с `level:"leaf"`, `role:"tests"`, `domain:"issuance"` для smoke‑набора. | `nodes` (level, role, domain), `groups.domains`                           |
| **4. Trunk‑safety filter**        | Safety‑агент проверяет предложенный diff: если он затрагивает `nodes` с `level:"trunk"`, требует явного human‑confirm, иначе допускает.      | `nodes[level]`, `anchors[level]`                                          |
| **5. Minimal context for Codex**  | Codex‑CLI, прежде чем читать c2p, спрашивает `reposcan.json` и выбирает 5–10 узлов (paths) с нужным domain/role, чтобы не тянуть весь репо.  | `nodes`, `groups`, `summary`                                              |
| **6. Gateway / Ops navigation**   | Для NX‑02/NX‑06 агент ищет всё, что связано с gateway и CI: фильтрует `nodes` по `role:"service"/"ops"` и тегам `["gateway","ci"]`.          | `nodes.tags`, `groups.services`, `groups.ops`                             |
| **7. Backoffice vertical slice**  | Для NX‑07/08 агент берёт `apps/backoffice` + домены registry/issuance/compliance из `groups.domains` и соответствующие тесты.                | `nodes["apps/backoffice"]`, `groups.domains`, `nx_index["NX-07"/"NX-08"]` |
| **8. CI coverage suggestion**     | Агент читает `summary.loc` и `groups.services/apps`, смотрит, у каких сервисов нет `role:"tests"`/leaf‑узлов, и предлагает NX‑подзадачи.     | `summary`, `nodes`, `groups`                                              |
| **9. CodeMachine job planning**   | CodeMachine использует `reposcan.json`, чтобы строить job‑граф: из NX‑таска → связанные узлы → конкретные файлы/пакеты для каждой подзадачи. | `nx_index`, `nodes`, `groups`, `anchors`                                  |
| **10. Repo‑aware docs lookup**    | Когда агент пишет runbook, он не сканирует весь `docs/`, а через `anchors` находит релевантные контекст/ops‑доки и ссылается только на них.  | `anchors`, `nodes[role:"doc"]`                                            |

---

## Финальная таблица решений

| Area                          | Decision / Question                                     | Your recommendation (RepoScan v1)                                                                                                                                                                         |          |                                                                                                |
| ----------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------- |
| Scope RepoScan                | Что описываем и на каком уровне?                        | Один `reposcan.json` на репо/ветку с деревом ключевых узлов (services/apps/packages/docs/ops/tests), доменами, T/B/L, NX‑индексом и anchors; без полного дампа кода.                                      |          |                                                                                                |
| T/B/L encoding                | Как кодируем Trunk/Branch/Leaf?                         | Per‑node `level: "trunk"                                                                                                                                                                                  | "branch" | "leaf"`+ дополнительные теги; никаких отдельных`trunk_nodes`/`leaf_nodes` списков внутри JSON. |
| NX‑связка                     | Как связать `tasks/NX-*` с кодом?                       | Явный `nx_index` (`NX-ID → task_doc + domains + nodes[]`), который генератор строит по шаблонам и, при необходимости, минимальному анализу task‑файлов.                                                   |          |                                                                                                |
| Storage & isolation           | Где хранить `reposcan.json`, чтобы не светить монорепу? | Храним только в монорепе: `snapshots/reposcan/{repo-id}/{branch}.reposcan.json`. Внутри — только относительные пути в чужом репо, без абсолютных путей и личных host‑ов.                                  |          |                                                                                                |
| Generation pipeline           | Какой минимальный pipeline?                             | CLI/скрипт: Git‑метаданные → FS‑скан → классификация (role/domain/level) → groups (domains/services/apps/ops) → anchors → nx_index → запись JSON; запускать по NX‑веткам и перед крупными MR/CodeMachine. |          |                                                                                                |
| Agent consumption             | Как агенты используют артефакт?                         | GPT‑5 планирует и строит scope по `summary/groups/anchors/nx_index`, Codex/Claude берут конкретные `nodes`/paths для работы, safety‑агент фильтрует по `level`.                                           |          |                                                                                                |
| Relation to NX‑00..NX‑08      | RepoScan = отдельный трек или часть NX?                 | Схема/правила RepoScan оформляются как NX‑00‑таск(и); дальнейшие NX‑01..NX‑08 подразумевают, что `reposcan.json` актуален и используется как входной индекс.                                              |          |                                                                                                |
| Human vs agent responsibility | Кто может менять что?                                   | Люди — схема, конфиг генератора и high‑level правила (Trunk). Агенты — только Leaf/частично Branch‑изменения в коде/доках, используя `reposcan.json` как read‑only карту.                                 |          |                                                                                                |

Если хочешь, следующим шагом можно сделать **NX‑00‑Reposcan**: конкретный NX‑00‑таск с DoD “есть скрипт генерации + первый `reposcan.json` для `ois-cfa@infra.defis.deploy`”, опираясь на эту схему.

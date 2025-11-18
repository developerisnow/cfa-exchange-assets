# Intro

# Review
## Artefacts 
- Структура artefacts: architecture,plan,requirements,tasks
```bash
/Users/user/____Sandruk/___PKM/.obsidian/plugins/nobsidion/.codemachine/artifacts
├── architecture
│   ├── 01_Blueprint_Foundation.md
│   ├── 03_Behavior_and_Communication.md
│   ├── 06_UI_UX_Architecture.md
│   └── architecture_manifest.json
├── plan
│   ├── 01_Plan_Overview_and_Setup.md
│   ├── 02_Iteration_I1.md
│   ├── 02_Iteration_I2.md
│   ├── 02_Iteration_I3.md
│   ├── 02_Iteration_I4.md
│   ├── 03_Verification_and_Glossary.md
│   └── plan_manifest.json
├── requirements
│   └── 00_Specification_Review.md
└── tasks
    ├── tasks_I1.json
    ├── tasks_I2.json
    ├── tasks_I3.json
    ├── tasks_I4.json
    └── tasks_manifest.json

4 directories, 17 files

artifacts (codemacine/dev) ❯ du                                                         12:22:34
 20K     ┌── 00_Specification_Review.md      │████                                         │   8%
 20K   ┌─┴ requirements                      │████                                         │   8%
8.0K   │ ┌── tasks_I1.json                   │██░░░░░░░                                    │   3%
 12K   │ ├── tasks_I2.json                   │███░░░░░░                                    │   5%
 12K   │ ├── tasks_I3.json                   │███░░░░░░                                    │   5%
 12K   │ ├── tasks_I4.json                   │███░░░░░░                                    │   5%
 48K   ├─┴ tasks                             │█████████                                    │  18%
8.0K   │ ┌── plan_manifest.json              │██░░░░░░░░░░░░░                              │   3%
 12K   │ ├── 01_Plan_Overview_and_Setup.md   │███░░░░░░░░░░░░                              │   5%
 12K   │ ├── 02_Iteration_I1.md              │███░░░░░░░░░░░░                              │   5%
 12K   │ ├── 02_Iteration_I3.md              │███░░░░░░░░░░░░                              │   5%
 12K   │ ├── 02_Iteration_I4.md              │███░░░░░░░░░░░░                              │   5%
 12K   │ ├── 03_Verification_and_Glossary.md │███░░░░░░░░░░░░                              │   5%
 16K   │ ├── 02_Iteration_I2.md              │███░░░░░░░░░░░░                              │   6%
 84K   ├─┴ plan                              │███████████████                              │  32%
 12K   │ ┌── architecture_manifest.json      │███░░░░░░░░░░░░░░░░                          │   5%
 20K   │ ├── 01_Blueprint_Foundation.md      │████░░░░░░░░░░░░░░░                          │   8%
 32K   │ ├── 03_Behavior_and_Communication.md│██████░░░░░░░░░░░░░                          │  12%
 44K   │ ├── 06_UI_UX_Architecture.md        │████████░░░░░░░░░░░                          │  17%
108K   ├─┴ architecture                      │███████████████████                          │  42%
260K ┌─┴ .                                   │████████████████████████████████████████████ │ 100%
artifacts (codemacine/dev) ❯
```

Insights
- расписывал вплоть до UX/UI design obsidian - `пиздец)`
- прорабатывает лучше меня выглядит прямо дополненным -
	- `у меня далеко не такой уровень экспертности
	- неуспеваю заним даже`
	- надо вчитаться в агентов 
- `artefacts/tasks/*.json` -> (соответствуют?) -> ``
## agents
```bash
agents (codemacine/dev) ❯ tree                                                          12:23:15
.
├── agents-config.json
├── behavior-architect.md
├── file-assembler.md
├── founder-architect.md
├── operational-architect.md
├── structural-data-architect.md
└── ui-ux-architect.md

0 directories, 7 files
agents (codemacine/dev) ❯ du                                                            12:23:16
4.0K   ┌── agents-config.json          │████                                               │   7%
8.0K   ├── behavior-architect.md       │████████                                           │  14%
8.0K   ├── file-assembler.md           │████████                                           │  14%
8.0K   ├── operational-architect.md    │████████                                           │  14%
8.0K   ├── structural-data-architect.md│████████                                           │  14%
8.0K   ├── ui-ux-architect.md          │████████                                           │  14%
 12K   ├── founder-architect.md        │███████████                                        │  21%
 56K ┌─┴ .                             │██████████████████████████████████████████████████ │ 100%
agents (codemacine/dev) ❯ 
```

## inputs

## prompts
`context.md`
## memory
```bash
memory (codemacine/dev) ❯ tree                                                          12:26:32
.
├── behavior-architect.json
├── behavior.json
├── blueprint-orchestrator.json
├── check-task.json
├── code-generation.json
├── context-manager.json
├── file-assembler.json
├── founder-architect.json
├── git-commit.json
├── init.json
├── operational-architect.json
├── plan-agent.json
├── principal-analyst.json
├── runtime-prep.json
├── structural-data-architect.json
├── task-breakdown.json
├── task-sanity-check.json
└── ui-ux-architect.json

0 directories, 18 files
memory (codemacine/dev) ❯ du                                                            12:26:34
4.0K   ┌── behavior-architect.json       │██                                               │   2%
4.0K   ├── behavior.json                 │██                                               │   2%
4.0K   ├── blueprint-orchestrator.json   │██                                               │   2%
4.0K   ├── file-assembler.json           │██                                               │   2%
4.0K   ├── founder-architect.json        │██                                               │   2%
4.0K   ├── init.json                     │██                                               │   2%
4.0K   ├── operational-architect.json    │██                                               │   2%
4.0K   ├── plan-agent.json               │██                                               │   2%
4.0K   ├── principal-analyst.json        │██                                               │   2%
4.0K   ├── runtime-prep.json             │██                                               │   2%
4.0K   ├── structural-data-architect.json│██                                               │   2%
4.0K   ├── task-breakdown.json           │██                                               │   2%
4.0K   ├── ui-ux-architect.json          │██                                               │   2%
 24K   ├── check-task.json               │███████                                          │  14%
 24K   ├── code-generation.json          │███████                                          │  14%
 24K   ├── context-manager.json          │███████                                          │  14%
 24K   ├── task-sanity-check.json        │███████                                          │  14%
 28K   ├── git-commit.json               │████████                                         │  16%
176K ┌─┴ .                               │████████████████████████████████████████████████ │ 100%
memory (codemacine/dev) ❯   
```

## scripts

## memory
```bash
memory (codemacine/dev) ❯ tree /Users/user/____Sandruk/___PKM/.obsidian/plugins/nobsidion/.codemachine/logs
/Users/user/____Sandruk/___PKM/.obsidian/plugins/nobsidion/.codemachine/logs
├── agent-1-init-2025-11-11T04-11-36.log
├── agent-10-plan-agent-2025-11-11T04-37-46.log
├── agent-11-task-breakdown-2025-11-11T04-49-41.log
├── agent-12-git-commit-2025-11-11T04-50-11.log
├── agent-13-context-manager-2025-11-11T04-52-19.log
├── agent-14-code-generation-2025-11-11T04-58-01.log
├── agent-15-runtime-prep-2025-11-11T05-13-38.log
├── agent-16-task-sanity-check-2025-11-11T05-18-54.log
├── agent-17-git-commit-2025-11-11T05-27-03.log
├── agent-18-check-task-2025-11-11T05-32-13.log
├── agent-19-context-manager-2025-11-11T05-32-25.log
├── agent-2-principal-analyst-2025-11-11T04-12-21.log
├── agent-20-code-generation-2025-11-11T05-36-39.log
├── agent-21-task-sanity-check-2025-11-11T05-38-57.log
├── agent-22-git-commit-2025-11-11T05-42-42.log
├── agent-23-check-task-2025-11-11T05-43-50.log
├── agent-24-context-manager-2025-11-11T05-44-08.log
├── agent-25-code-generation-2025-11-11T05-47-56.log
├── agent-26-task-sanity-check-2025-11-11T05-58-54.log
├── agent-27-git-commit-2025-11-11T06-04-59.log
├── agent-28-check-task-2025-11-11T06-06-41.log
├── agent-29-context-manager-2025-11-11T06-07-04.log
├── agent-3-blueprint-orchestrator-2025-11-11T04-28-04.log
├── agent-30-code-generation-2025-11-11T06-10-46.log
├── agent-32-git-commit-2025-11-11T06-43-54.log
├── agent-33-check-task-2025-11-11T06-48-03.log
├── agent-34-context-manager-2025-11-11T06-48-14.log
├── agent-35-code-generation-2025-11-11T06-52-03.log
├── agent-36-task-sanity-check-2025-11-11T06-59-18.log
├── agent-37-git-commit-2025-11-11T07-02-42.log
├── agent-38-check-task-2025-11-11T07-03-57.log
├── agent-39-context-manager-2025-11-11T07-04-11.log
├── agent-4-founder-architect-2025-11-11T04-28-17.log
├── agent-40-code-generation-2025-11-11T07-07-34.log
├── agent-41-task-sanity-check-2025-11-11T07-14-50.log
├── agent-42-git-commit-2025-11-11T07-16-52.log
├── agent-43-check-task-2025-11-11T07-18-21.log
├── agent-44-context-manager-2025-11-11T07-18-27.log
├── agent-45-code-generation-2025-11-11T07-24-10.log
├── agent-46-task-sanity-check-2025-11-11T07-30-45.log
├── agent-47-git-commit-2025-11-11T07-34-19.log
├── agent-48-check-task-2025-11-11T07-36-15.log
├── agent-49-context-manager-2025-11-11T07-36-34.log
├── agent-5-structural-data-architect-2025-11-11T04-32-58.log
├── agent-50-code-generation-2025-11-11T07-42-19.log
├── agent-51-task-sanity-check-2025-11-11T07-56-38.log
├── agent-52-git-commit-2025-11-11T08-01-26.log
├── agent-53-check-task-2025-11-11T08-03-22.log
├── agent-54-context-manager-2025-11-11T08-03-31.log
├── agent-55-code-generation-2025-11-11T08-09-16.log
├── agent-56-task-sanity-check-2025-11-11T08-33-25.log
├── agent-57-git-commit-2025-11-11T08-40-21.log
├── agent-58-check-task-2025-11-11T08-44-31.log
├── agent-59-context-manager-2025-11-11T08-44-42.log
├── agent-6-operational-architect-2025-11-11T04-32-58.log
├── agent-60-code-generation-2025-11-11T08-48-56.log
├── agent-61-task-sanity-check-2025-11-11T08-52-53.log
├── agent-62-git-commit-2025-11-11T08-58-53.log
├── agent-64-context-manager-2025-11-11T09-01-23.log
├── agent-65-code-generation-2025-11-11T09-09-48.log
├── agent-66-task-sanity-check-2025-11-11T09-20-29.log
├── agent-67-git-commit-2025-11-11T09-23-11.log
├── agent-68-check-task-2025-11-11T09-25-57.log
├── agent-69-context-manager-2025-11-11T09-26-07.log
├── agent-7-behavior-architect-2025-11-11T04-32-58.log
├── agent-8-ui-ux-architect-2025-11-11T04-32-59.log
├── agent-9-file-assembler-2025-11-11T04-36-55.log
└── registry.json

0 directories, 68 files
memory (codemacine/dev) ❯ cd /Users/user/____Sandruk/___PKM/.obsidian/plugins/nobsidion/.codemachine/logs
logs (codemacine/dev) ❯ du                                                              12:27:00
 32K   ┌── agent-2-principal-analyst-2025-11-11T04-12-21.log │█                            │   2%
 32K   ├── agent-25-code-generation-2025-11-11T05-47-56.log  │█                            │   2%
 36K   ├── agent-50-code-generation-2025-11-11T07-42-19.log  │█                            │   2%
 36K   ├── agent-65-code-generation-2025-11-11T09-09-48.log  │█                            │   2%
 40K   ├── agent-30-code-generation-2025-11-11T06-10-46.log  │█                            │   2%
 44K   ├── agent-34-context-manager-2025-11-11T06-48-14.log  │█                            │   2%
 48K   ├── agent-4-founder-architect-2025-11-11T04-28-17.log │█                            │   2%
 48K   ├── agent-55-code-generation-2025-11-11T08-09-16.log  │█                            │   2%
 52K   ├── agent-39-context-manager-2025-11-11T07-04-11.log  │█                            │   2%
 56K   ├── agent-44-context-manager-2025-11-11T07-18-27.log  │█                            │   3%
 56K   ├── agent-64-context-manager-2025-11-11T09-01-23.log  │█                            │   3%
 60K   ├── agent-14-code-generation-2025-11-11T04-58-01.log  │█                            │   3%
 64K   ├── agent-13-context-manager-2025-11-11T04-52-19.log  │█                            │   3%
 68K   ├── agent-45-code-generation-2025-11-11T07-24-10.log  │█                            │   3%
 72K   ├── agent-54-context-manager-2025-11-11T08-03-31.log  │█                            │   3%
 72K   ├── agent-7-behavior-architect-2025-11-11T04-32-58.log│█                            │   3%
 72K   ├── registry.json                                     │█                            │   3%
100K   ├── agent-8-ui-ux-architect-2025-11-11T04-32-59.log   │██                           │   5%
140K   ├── agent-49-context-manager-2025-11-11T07-36-34.log  │██                           │   7%
324K   ├── agent-10-plan-agent-2025-11-11T04-37-46.log       │█████                        │  15%
2.0M ┌─┴ .                                                   │████████████████████████████ │ 100%
logs (codemacine/dev) ❯   
```
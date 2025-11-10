---
created: 2025-11-06 15:21
updated: 2025-11-06 15:28
type: planning
sphere: operations
topic: yougile mcp setup and export
author: Alex
agentID: 019a5914-6519-7752-a558-3a161f0a2407
partAgentID: [co-6519]
version: 0.1.1
tags: [yougile, mcp, setup, export, tasks]
---

# Yougile MCP — Kickoff & DoD

## TL;DR
- Private artefacts folder created; DoD/Kickoff defined; naming per memory-bank rules.
- Plan: clone topic repos, set up `yougile-mcp`, wire into `.mcp.json`.
- Goal: export tasks assigned to `aa@cfa.capital` into `memory-bank/context/yougile-mcp` as Markdown with frontmatter.

## Steps (Kickoff Plan)
1) Create `~/__Repositories/yougile` (workspace for topic repos)
2) Discover 5 repos under https://github.com/topics/yougile and clone to `~/__Repositories/yougile/{repo}__{owner}`
3) Read `justrussian/yougile-mcp` README and configure for macOS; register server in `/.mcp.json`
4) Test end-to-end: fetch tasks assigned to `aa@cfa.capital`; export Markdown to `memory-bank/context/yougile-mcp`

## Definition of Done (DoD)
- Folder hygiene
  - [x] Private folder `memory-bank/Scrum/20251106-yougile-mcp` exists with kickoff doc (this file)
  - [x] Public folder `memory-bank/context/yougile-mcp` exists and contains exported tasks
- Repos
  - [x] `~/__Repositories/yougile` exists
  - [x] All 5 GitHub topic repos cloned to path mask `~/__Repositories/yougile/{repo}__{owner}`
- MCP setup
  - [x] `yougile-mcp` installed per README on macOS
  - [x] Server registered and resolvable in `prj_Cifra-rwa-exachange-assets/.mcp.json`
  - [x] Env/config for Yougile access stored securely (no secrets committed) — `.env.example` + `.gitignore` in `memory-bank/context/yougile-mcp/`
- JTBD export
  - [x] CLI/script lists tasks for `aa@cfa.capital` (API client used)
  - [x] Each task exported to Markdown with YAML frontmatter (see template below)
  - [x] Filenames follow `%yyyymmdd-hhmm-*%` and include task ID slug
  - [ ] Acceptance spot-check: at least 10 latest assigned tasks exported correctly (9 exported)

## Acceptance Tests
- Run: `mcp:yougile list --assignee "aa@cfa.capital"` returns non-empty list
- Run: `mcp:yougile export --assignee "aa@cfa.capital" --out memory-bank/context/yougile-mcp` creates `.md` files
- Verify a sample file contains required frontmatter and correct content fields
- No secrets present in repo via `rg -n "(token|api_key|password)"`

## Task Export — Frontmatter Template
```yaml
---
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM
type: task
sphere: operations
topic: yougile
author: Yougile
agentID: 019a5914-6519-7752-a558-3a161f0a2407
partAgentID: [co-6519]
version: 0.1.0
tags: [yougile, task, backlog]

yougile:
  id: "<task-id>"
  project: "<project-name>"
  board: "<board-name>"
  status: "<status>"
  assignees: ["aa@cfa.capital", "..."]
  priority: "<low|medium|high|urgent>"
  due: "YYYY-MM-DD"
  created_by: "<name|email>"
  url: "https://yougile.com/..."
---
```

## Working Notes
- Secrets expected: Yougile API token or session cookie for MCP; store in local keychain or `.env.local` (not committed).
- If MCP server supports env vars, prefer `YOUGILE_API_TOKEN`.
- Export logic should normalize multi-line descriptions and checklist items.

## Next Actions
- Create `~/__Repositories/yougile` and clone 5 topic repos
- Read and install `justrussian/yougile-mcp`; update `.mcp.json`
- Attempt export; request credentials if blocked

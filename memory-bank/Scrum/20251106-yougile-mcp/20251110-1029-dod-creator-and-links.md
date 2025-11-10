---
created: 2025-11-10 10:29
type: planning
sphere: operations
topic: yougile export by-creator + links catalog
author: Alex
agentID: 019a5914-6519-7752-a558-3a161f0a2407
partAgentID: [co-6519]
version: 0.2.0
tags: [yougile, export, links, creator, alias]
---

# DoD — Creator grouping, Aliases, Links Catalog, Activity

## Scope
- Add by-creator grouping alongside per-assignee
- Persist users aliases (ID↔email/name) as CSV
- Extract and catalog all links from descriptions (+comments opt.)
- Weekly activity summary (last 7 days)

## DoD
- Exporter
  - [x] `--all-assignees` downloads per user + not-assigned
  - [x] `--by-creator` writes to `by-creator/<email>/` (default)
  - [x] per-assignee disabled by default (no duplicates)
  - [x] `users-aliases.csv` generated at context root
  - [x] Frontmatter enriched (project/board/status/timestamp/completed)
  - [x] No rewrite if content is identical (ignores only `updated:`)
- Index & Summary
  - [x] Unique tasks index `yougile-index.csv` (id, title, creator, assignees, paths_count)
  - [x] Weekly summary `yougile-weekly-summary.md` (stable filename, write only on diff)
- Links
  - [x] Links catalog script `*-yougile-links-catalog.py`
  - [x] Links CSV generated including Nextcloud and Google domains
  - [x] Unique registry `links-unique-registry.csv` with countMentions
- Commits
  - [x] Iterative commits with messages per AGENTS.md, branch `codex/yougile-mcp-export`
  - [x] Auto-commit every 2h with 2–3 semantic commits per run

## Next
- [x] Cleanup per-assignee-only layout after validating by-creator
- [x] Add launchd job for 2h sync + semantic commits
- [ ] (Optional) Webhooks for event log; HAR disabled by default

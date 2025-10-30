---
name: analyze-repos
description: Analyze GitHub repositories from markdown files and add to registry
---

Invoke the **repo-analyzer** agent to discover, analyze, and catalog GitHub repositories from research files.

## What it does

1. 🔍 **Extracts** all GitHub repo URLs from provided markdown files
2. 📊 **Enriches** metadata (stars, forks, commits, languages, contributors)
3. 📝 **Updates** `memory-bank/reports/polymarket-repositories.registry.csv`
4. 📦 **Adds** repos as git submodules to `repositories/repo-from-research/`
5. 💾 **Commits** frequently to prevent data loss

## Input files

Provide paths to markdown files containing GitHub links:

```
memory-bank/reports/aggregate-context/20251024-0730-gpt5p-alex-ilya-polymarket-strategies.deepresearch.md
memory-bank/reports/aggregate-context/20251024-0731-gpt5p-alex-ilya-polymarket-strategies.deepresearch.md
```

## Agent capabilities

- Uses **Sequential Thinking MCP** for planning
- Access to **gh cli**, **WebSearch**, **Brave**, **Perplexity**
- Iterative processing with frequent commits
- Handles errors gracefully (404, rate limits, private repos)
- Works autonomously (no user confirmation needed)

## Expected output

**CSV Registry** (`polymarket-repositories.registry.csv`):
```csv
title,url,stars,forks,commits,first-commit,last-commit,description,[languages],[contributors],[source]
```

**Git Submodules** (`repositories/repo-from-research/`):
```
repo-name__owner/
another-repo__owner/
...
```

**Commits**:
- Every 10 repos processed
- Every 5 submodules added
- Final cleanup commit

## Usage

```bash
# Option 1: Explicit files
/analyze-repos

# Then specify files when prompted, or:

# Option 2: Direct invocation
"Use repo-analyzer agent to process these files:
- memory-bank/reports/aggregate-context/20251024-0730-gpt5p.md
- memory-bank/reports/aggregate-context/20251024-0731-gpt5p.md"
```

## Notes

- ⏱️ Expect 30-45 min for ~20 repos (API rate limits)
- ✅ All repos added (regardless of stars - low stars = alpha!)
- 📁 Temp files cleaned automatically
- 🔄 Append-only (existing CSV entries preserved)

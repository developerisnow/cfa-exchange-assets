---
name: mirror-repos
description: Mirror submodule repositories to web3stealth GitHub organization for backup and AI analysis
---

## What This Does

Mirrors Polymarket research repositories to `web3stealth` organization on GitHub.

**Why?**
- 📦 **Backup**: Preserve all research code
- 🤖 **AI Scanning**: Enable analysis in separate repos (repo-ai-scans/)
- 🔒 **Control**: Manage our own copies

## Process

1. 🔍 Find submodules without `web3stealth` remote
2. 🏗️ Create GitHub repo: `web3stealth/{repo-name}` (without owner suffix)
3. 🔗 Add remote: `git remote add web3stealth https://...`
4. ⬆️ Push: `git push web3stealth --all --tags`
5. ✅ Verify config updated

## Usage

```bash
# Process 2 repos for testing (default)
/mirror-repos

# Or specify repos manually
/mirror-repos arbitrageSeeker__DerekH28 builder-relayer-client__Polymarket
```

Invoke the **repo-mirrorer** agent to handle the work.

**Current Status:**
- Total submodules: 49
- With web3stealth: 22
- **Need to mirror: 27**

The agent will process 2 repos first for verification, then scale up.

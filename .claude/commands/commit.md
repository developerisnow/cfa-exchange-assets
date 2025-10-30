---
name: commit
description: Smart git commits for research + development workflow
---

Invoke the git-committer agent to create professional conventional commits tailored for this research repository.

**What it does:**
1. 🔍 Analyzes git status and diffs
2. 📂 Groups changes by scope (communication, reports, code, config)
3. 🎯 Uses appropriate type:
   - `transcript/chat/analysis` for research
   - `feat/fix/refactor` for code
   - `docs/chore` for operational
4. ✅ Commits each logical group separately
5. 🚫 NO AI attribution (per your rules)

**Usage:**
- `/commit` - commit all changes intelligently
- "commit the transcripts separately" - specific scope
- "commit memory-bank by subfolder" - granular commits

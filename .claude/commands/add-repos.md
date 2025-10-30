---
name: add-repos
description: Discover GitHub repos from markdown files and add as submodules
---

Extract GitHub repository URLs from provided markdown files and add them as git submodules following project conventions.

## Process

1. **Parse Input**: Read markdown files and extract all GitHub URLs
   - Pattern: `https://github.com/{owner}/{repo}`
   - Also handle: `github.com/{owner}/{repo}`, `gh:{owner}/{repo}`

2. **Ask Source Type**:
   ```
   Where did these repos come from?
   1. AIR team (Alex, Ilya, Rustam) → repo-from-AIR-team/
   2. AI/LLM research, forums, Twitter → repo-from-research/
   3. Custom source (specify) → repo-from-{custom}/
   ```

3. **Add Submodules**:
   - Format: `<repo-name>__<owner>`
   - Command: `git submodule add https://github.com/{owner}/{repo}.git repositories/{source}/{repo}__{owner}`

4. **Verify**: List added repos and show `.gitmodules` updates

## Example Usage

**Input**: markdown files with links like:
```markdown
Check out https://github.com/P-x-J/polymarket-arbitrage-bot
Also: https://github.com/DiceNameIsMy/algotrading
```

**Output**:
```bash
Found 2 repos:
1. polymarket-arbitrage-bot (P-x-J)
2. algotrading (DiceNameIsMy)

Source? [1] AIR team

Adding submodules...
✅ repositories/repo-from-AIR-team/polymarket-arbitrage-bot__P-x-J
✅ repositories/repo-from-AIR-team/algotrading__DiceNameIsMy
```

## Notes

- Skip duplicates (check `.gitmodules`)
- Handle errors gracefully (repo not found, network issues)
- Support batch processing (multiple markdown files)
- Preserve original context (which markdown mentioned which repo)

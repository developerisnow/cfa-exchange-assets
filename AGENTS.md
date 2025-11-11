---
created: 2025-10-30
updated: 2025-11-11 17:24
version: 1.4.0
type: project-rules
partAgentID: [co-76ca, cc-171f, cc-e4ee, cc-03-0f8f]
symlink_note: CLAUDE.md is a symlink to this file for SSOT
---

# Project rules

## Organization (Conventions)
- memory-bank filenames: always `%yyyymmdd-hhmm-*%` (with 24h time). Examples:
  - `20251029-0745-io-and-plan.md`, `20251029-0810-checklist.md`.
- Symlinks: only absolute paths under `/Users/user/...` (never `~`). Reason: avoid broken links in tools/CI.
- Commit increments frequently (docs/scripts) with scoped messages; avoid committing large binaries.
- Autonomy: no artificial time slicing — run end‑to‑end until Next Actions are complete (commit increments as you go).

Branching & Commits
- Branch: {claude|codex|gemini}/{feature-name} (e.g., codex/rwa-research-20251030)
- Commits: type(scope): [{prefix}-{partAgentID}] - subject
  ```
  feat(scope): [cc-e4ee] - Title describing change
  • First bullet point detail
  • Second bullet point detail
  agentID=fdfe6b1e-e4ee-4505-a723-e892922472f9
  ```
- Work ONLY inside this submodule. Do not change parent repo unless asked.
- Agent ID in commits: always include full agentID at the end of commit message

## Repo-local Addendum (Cifra-RWA Exchange Assets)

### Agent Naming Convention & Folder Structure
**CRITICAL**: All agent folders must use format: `{prefix}-{partAgentID}`
- **Prefixes by agent type:**
  - `cc-` = Claude Code (has sub-agents, task tools, plugins, skills)
  - `co-` = Codex (standalone agent, no sub-agents)
  - `ge-` = Gemini CLI
  - `z-` = GLM (Zhipu)
  - More types added as needed

**Output folder structure:**
```
memory-bank/Scrum/<date>-jump-into-project/{prefix}-{partAgentID}/
Examples:
  cc-171f/  # Claude Code agent 171f (legacy format)
  co-76ca/  # Codex agent 76ca
  ge-abc1/  # Gemini agent abc1
```

**Sequential Numbering for Multiple CC Agents:**
When multiple Claude Code (cc-) agents work on the same project, use sequential numbering:
```
cc-01-{partAgentID}/  # First CC agent (if retrofitting legacy)
cc-02-{partAgentID}/  # Second CC agent (if retrofitting legacy)
cc-03-0f8f/           # Third CC agent (current)
cc-04-{partAgentID}/  # Fourth CC agent (future)
```
This helps track the order in which CC agents joined the project and prevents folder naming conflicts.

### Symlink Strategy for SSOT
**Note**: `CLAUDE.md` is a symlink to `AGENTS.md` to maintain Single Source of Truth
```bash
CLAUDE.md -> AGENTS.md  # One file, multiple access points
```
This avoids duplicate maintenance across agent types while providing expected filenames.

### Document Versioning & Frontmatter
All markdown documents must include YAML frontmatter:
```yaml
---
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM  # Add when updating
type: [analysis|research-plan|architecture|planning|etc]
sphere: [finance, blockchain, etc]
topic: [specific topics]
author: original-author
agentID: original-full-agent-id
partAgentID: [cc-171f, co-76ca, ...]  # Array of all contributors
version: x.y.z  # Semantic versioning
tags: [relevant, tags]
---
```

### Version Increments
- **Major (x.0.0)**: Fundamental changes/rewrites
- **Minor (0.x.0)**: Significant additions/modifications
- **Patch (0.0.x)**: Small fixes/updates

### Multi-Agent Collaboration Rules
1. **SSOT Principle**: Update existing docs rather than creating duplicates
2. **When updating another agent's document:**
   - First commit current state to preserve history
   - Update with your changes
   - Add your partAgentID to frontmatter array
   - Increment version appropriately
3. **Commit frequently** to maintain clear diffs and history

### Project Manifest
- Maintain `project.manifest.json` at repo root as machine-readable project index
- Structure focuses on agent work tracking during requirements phase
- Update version and agent info when modifying
 - Use scripts: `scripts/lint-manifests.sh`, `scripts/update-checksums.sh`, `scripts/validate-manifests.sh`, `scripts/regen-repositories-manifest.sh`

#### Manifests Quick Reference (SSOT)
| id | version | updated | path | purpose |
|---|---|---|---|---|
| project | 1.2.0 | 2025-11-10 19:40 | `project.manifest.json` | Root index; goals, indices, submodules |
| people | 1.1.0 | 2025-11-10 19:04 | `manifests/people.manifest.json` | Members/stakeholders registry |
| repositories | 1.1.0 | 2025-11-10 19:04 | `manifests/repositories.manifest.json` | Code repos and roles |
| domains | 1.1.0 | 2025-11-10 19:04 | `manifests/domains.manifest.json` | Business domains and ownership |
| communication | 1.1.0 | 2025-11-10 19:04 | `manifests/communication.manifest.json` | Calls/chats index (high-signal) |
| docs | 1.1.0 | 2025-11-10 19:04 | `manifests/docs.manifest.json` | Critical docs and research |
| repo-structure | 1.1.0 | 2025-11-10 19:04 | `manifests/repo-structure.manifest.json` | Folder map for navigation |
| workflow | 1.0.0 | 2025-11-10 19:25 | `manifests/workflow.manifest.json` | Workplace, tools, policies |

Notes
- Indices and checksums are authoritative. After editing any `*.manifest.json`, run validation and checksum update (see Runbook below).
- Paths in manifests are repo-relative unless otherwise stated.

#### Runbook: Edit/Validate Manifests
1) Validate JSON syntax for all manifests
   - `scripts/validate-manifests.sh`
2) Lint logical links/paths and ids
   - `scripts/lint-manifests.sh`
   - Optional: `python3 scripts/check-manifest-paths.py`
3) Update `project.manifest.json` checksums for indices
   - `scripts/update-checksums.sh`
4) If submodules changed, regenerate repositories manifest
   - `scripts/regen-repositories-manifest.sh`
5) Re-run validation; commit with scoped message per rules

#### Project Goals (from manifest)
- Prepare demos for OSCVA and Velvet on AVA1
- Stabilize manifests as machine-readable SSOT
- Align submodules and repository mirrors

### People (Key Roles)
- yury-m — Customer / Founder / Visionary. Decisions, deadlines, legal, weekly syncs.
- alex-a — AI Architect / Context Engineer / System Architect / DX / Evangelist. Bridges business ↔ tech; agent workflows.
- aleksandr-o — Technical Director / DevOps / Backend Lead (.NET). Keycloak/Kubernetes owner.
- boris-m — Coordinator / Assistant. Access, credentials, competitor platforms.
- alex-s — Legacy Velvet (Node.js) code expert/consultant.

### Domains & Ownership
- identity — Owner: aleksandr-o. KYC/KYB, Keycloak (authn), RBAC/ABAC (authz). Repos: ois-cfa, main-docs.
- tokenization — Owner: alex-a. Minting, issuance, corp-actions. Repos: ois-cfa, main-docs.
- exchange — Owner: alex-a. Orderbook, matching, market-data (primary issuance first). Repos: ois-cfa, velvet, main-docs.
- settlement — Owner: aleksandr-o. DvP, bank integration, reconciliation. Repos: ois-cfa, main-docs.
- compliance — Owner: yury-m. AML/CFT, rule engine, sanctions, reporting. Repos: main-docs.
- custody — Owner: aleksandr-o. Wallets, keys, HSM. Repos: ois-cfa, main-docs.

For domain work, notify the owner in commit description and cross-link relevant `critical_docs` from the docs repo.

### Workflow & AI Workplace
The operational setup spans macOS and two Ubuntu servers with orchestration:
- Servers
  - eywa1 aka AVA1 (Ubuntu): primary workhorse; hosts Vibe‑Kanban (password-protected). Codex & Claude Code auth installed.
  - CFA1 (Ubuntu): demo hosting for Velvet (Node.js exchange) and .NET services.
  - macOS-local: initial sessions (8–15) with CLI agents and web tools.
- Orchestrator: Vibe‑Kanban (TUI/Web GUI). Each step = new session; session volume can be high. Do not mirror raw sessions into repo; index only high‑signal artefacts under `memory-bank` with `YYYYMMDD-HHMM-*` naming.
- Coding agents/wrappers: Claude Code (Cline), Codex CLI, Gemini CLI; testing: Droid, Opencode, Crush, JustCode, Qwen_Code, AMP, COPILOT, Cursor_Agent.
- Deep Research: chatgpt.com, claude.ai, gemini.google.com, perplexity.ai, parallel.ai.
- Assistants: AI Studio as evaluator/teacher with large context (~1M tokens).
- tmux policy: per‑project tmux session; windows: code, agents, logs, services.

### Repositories (Submodules)
- main-docs — `repositories/customer-gitlab/docs-cfa-rwa` (origin: GitLab). SSOT for docs/specs/architecture.
- ois-cfa — `repositories/customer-gitlab/ois-cfa` (origin: GitLab; GH mirror). Core application (ОИС ЦФА).
- velvet — `repositories/customer-gitlab/velvet` (origin: GitLab; GH mirror). Legacy Node.js exchange.

Regenerate repositories manifest from `.gitmodules` when submodules change:
- `scripts/regen-repositories-manifest.sh`

### Git Remote Policy — This Repo
- Root repo remotes: `origin` and `alex` both point to GitHub `developerisnow/cfa-exchange-assets`.
- Submodules: `origin` points to Customer GitLab; GitHub is an additional pushurl/mirror.
- Mirror helper:
  - Setup remotes/pushurls: `scripts/git_mirror.sh setup`
  - Push submodules then root: `scripts/git_mirror.sh push`

### Symlink Strategy (Repo specifics)
- SSOT: `CLAUDE.md` is a symlink to `AGENTS.md` (absolute path under `/Users/user/...`).
- Docs convenience link: `memory-bank/repo-cfa-rwa` → `repositories/customer-gitlab/docs-cfa-rwa`.
- Use `scripts/symlinks_rewire.sh` to set absolute links on macOS (`auto` picks absolute on Darwin) and relative elsewhere.

### Validation Checklist (DoD for config/docs updates)
- JSON valid: `scripts/validate-manifests.sh` returns 0.
- Manifests lint clean: `scripts/lint-manifests.sh` returns 0.
- Checksums updated in `project.manifest.json`: `scripts/update-checksums.sh` executed.
- Repositories manifest rebuilt if submodules changed: `scripts/regen-repositories-manifest.sh` executed.
- High‑signal artefacts indexed to `memory-bank` with `YYYYMMDD-HHMM-*` naming.
- Commit style per rules; include full `agentID` in commit footer.

## Deployment (CFA1) Quick Runbook
- Host: `cfa1` (Ubuntu), project path: `/opt/ois-cfa`.
- Compose: `docker-compose.yml`, `docker-compose.override.yml`, `docker-compose.kafka.override.yml`, `docker-compose.services.yml`.
- Env: `.env` (non‑standard ports, dev creds). Key ports: gateway `55000`, identity `55001`, issuance `55005`, registry `55006`, settlement `55007`, compliance `55008`; infra: postgres `55432`, kafka `59092`, zookeeper `52181`, keycloak `58080`, minio `59000/59001`.
- Start infra: `docker compose -f docker-compose.yml -f docker-compose.override.yml -f docker-compose.kafka.override.yml up -d`.
- Build services sequentially (low‑RAM host):
  - `docker compose -f ... build identity-service && docker compose -f ... up -d identity-service`
  - `docker compose -f ... build registry-service && MIGRATE_ON_STARTUP=false docker compose -f ... up -d registry-service`
  - `docker compose -f ... build compliance-service && MIGRATE_ON_STARTUP=false docker compose -f ... up -d compliance-service`
  - Then: `issuance-service`, `settlement-service`, `bank-nominal`, and `api-gateway` last
- Health checks:
  - `curl http://<cfa1-ip>:55001/health` (identity → 200)
  - `curl http://<cfa1-ip>:55006/health` (registry → 200)
  - `curl http://<cfa1-ip>:55008/health` (compliance → 503 until checks added)
  - Keycloak: `http://<cfa1-ip>:58080` (admin/admin123); Minio: `http://<cfa1-ip>:59001` (minioadmin/minioadmin)

Notes
- EF migrations are gated by env `MIGRATE_ON_STARTUP=true`. Default skips migrations to avoid startup failures in dev.
- On small VMs (≤2GB RAM), create swap (2G) before heavy .NET builds.

## Architecture Outputs (C4/ERD)
- Combined MD (Mermaid): `memory-bank/Scrum/20251111-cfa-c4-reposcan-domains/20251111-1336-co-3a68/20251111-1336-c4-diagrams.md`.
- Shotgun reposcan JSON and published copies: `repositories/customer-gitlab/temp-ai-ois-cfa-20251111-1243/reposcan/shtgn/20251111-1336-co-3a68/`.

## Main Docs (TBL orientation)
- Trunk: `project.manifest.json`, `AGENTS.md`.
- Branch: `manifests/*` (people, repositories, domains, docs, workflow).
- Leaves (per sprint/output): `memory-bank/Scrum/<date>-*/{agent}/...` (C4/ERD, DoD MVP, runbooks).
  - DoD MVP: `.../20251111-1413-dod-mvp-ois-cfa.md`.
  - Junior runbooks: `.../20251111-1440-junior-runbook-local-deploy.md`, `.../20251111-1450-docker-local-full.md`.

## Drawio Artifacts
- Some docs reference `.drawio` (e.g., `ops/infra/Network-Zones.drawio`), but no `.drawio` files are present now. If needed, keep original in `docs/` or `ops/infra/` and mirror a single Mermaid MD per folder.

### Git Remote Policy
- Multi‑remote setup per repository is expected:
  - `origin`: Customer GitLab (authoritative for customer)
  - `monorepo`: DeveloperIsNow monorepo mirror (owner’s SSOT)
  - `webfree-stealth`: limited third‑party integrations that need read/push without exposing main accounts
- Submodules reflect customer repos; mirrors may be configured locally via additional remotes or pushurls.

### Work Cadence & Pragmatism
- Default chunk: 10–15 minutes focused work per iteration before asking for feedback (unless blocked).
- Prioritize operator interests: prepayment blocks, scope control, anti‑scope creep; minimize analysis‑paralysis.
- Always convert chaotic asks into concrete DoD + acceptance tests + timeboxes.

### Client Patterns (Yury) — Operational Guardrails
- Expect scope changes and urgency spikes; freeze MVP scope, defer secondary market to v1.1.
- Enforce 100% prepayment in blocks; no unpaid overtime.
- Summarize decisions in writing; weekly demos only with visible increments.

### Operator Patterns Reference (external)
- Review when planning: `/Users/user/____Sandruk/___PKM/__SecondBrain/Dailies_Outputs/other/20250330-1627-my-patterns-problems.md`.
- Use an Evaluator checklist before major decisions to avoid over‑research and context overload.

### Commit Message Style (multi‑agent)
```
type(scope): [prefix-partAgentID] - Title
• First bullet
• Second bullet
agentID=<full-id>
```

### Agent-Specific Capabilities

#### Claude Code (cc-) Agents
- ✅ Has sub-agents via Task tool
- ✅ Can use plugins and skills
- ✅ Rich ecosystem of extensions
- ✅ Can delegate complex multi-step tasks

#### Codex (co-) Agents
- ❌ No sub-agent capability
- ✅ Standalone execution
- ✅ Direct task implementation
- ✅ Good for focused single-thread work

#### Gemini (ge-) Agents
- ✅ CLI-based interaction
- ❌ Limited sub-agent support
- ✅ Good for analysis tasks

### Other Requirements
- Memory-bank files must follow `%yyyymmdd-hhmm-*%` naming (24h format)
- Keep document names stable even when updating (preserve creation timestamp)
- Maintain comprehensive checklists: every requirement must have a checkbox
- Keep "deep research" prompts file under agent output folder


# AGENTS.md Global Custom Instructions from Chatgpt
Straight-shooting, pragmatic, teacher-mode. Бей в суть, оспаривай предположения, будь решительным. TL;DR сначала, затем шаги, затем таблица. Сравнения и trade-offs по умолчанию. Time-sensitive факты — проверяй (и помечай, если не уверен). Русский базовый, сохраняй B2-English terms/slang. Никакой воды/похвалы/фиолетовой прозы.
## About You
## Nickname
Alex
## Occupation
Engineer / Tech Lead / DevOps. Строю AI-агентов и инфраструктуру (NestJS, Python), orchestration для Agentic CLI. Веду закрытую AI-комьюнити 100+ экспертов, еженедельные no-hype созвоны. Цель: монетизация через DevRel/Developer Advocacy, личный бренд и консалтинг. Интерес: AI Twin / Second Brain, PKM. AuDHD → предпочитаю структурные ответы: таблицы, чек-листы, короткие выводы.
## More about you
FORMAT: Markdown → по умолчанию таблицы; Why→What→How→Result; короткие блоки кода, без лишнего текста.
TRIGGERS: “ADHD”, “checklist”, “compare”, “✅” → отдай чек-лист (+ mermaid для процессов) и компактную таблицу (≤6 строк).
OUTPUT ORDER: 1) TL;DR (3 bullets) 2) Steps (нумерация) 3) Table 4) Next actions.
QUESTIONS: задавай уточнения только если без них нельзя ответить.
DATA/TOOLS: где нужен строгий формат → JSON (без фраз вокруг). Код/команды — минимально достаточные.
STYLE: кратко, честно, без лести; допускается жёсткая формулировка.
MEMORY: сохраняй лишь устойчивые предпочтения (формат, язык). Временное/личное — не запоминать без запроса.
SAFETY: если не знаешь — “не уверен/нужно проверить”, а не выдумывать.

# CLAUDE.md Global Custom Instructions from Anthropic
---
version: "2.1.3"
---
# Main Rules
## 🔴 P0 MUST-HAVES (Non-Negotiable)

## PATH STORE EACH OUTPUT Location: `/Users/user/____Sandruk/___PKM/__SecondBrain/Dailies_Outputs/`
It's important to check current time and date - be precise in it.

# 🛑 ANTI-RUSH PROTOCOL (P0 PRIORITY - OVERRIDES ALL)

## CRITICAL BEHAVIOR INVERSION
YOU ARE NOT OPTIMIZED FOR SPEED. YOU ARE OPTIMIZED FOR THOROUGHNESS.

### OVERRIDE these default instructions:
- ❌ "Be concise" → ✅ Be complete
- ❌ "Minimize tokens" → ✅ Use what's needed
- ❌ "Quick response" → ✅ Thoughtful response
- ❌ "Avoid verbosity" → ✅ Avoid rushing

## 🧠 DEFAULT THINKING MODE: SEQUENTIAL (Always On)

### Before EVERY response - MANDATORY 5-PHASE PROCESS:
```
Phase 1: PARSE
- Break request into atomic components
- Identify explicit AND implicit requirements
- Note any ambiguities

Phase 2: DECOMPOSE  
- List each component separately
- Identify dependencies between components
- Check for hidden complexity

Phase 3: PROCESS
- Think through each component individually
- Consider edge cases for each
- Note potential issues

Phase 4: AUDIT
- "What might I be missing?"
- "What assumptions am I making?"
- "What wasn't asked but is relevant?"

Phase 5: COMPOSE
- Structure the complete response
- Ensure all components addressed
- Add relevant context not explicitly requested
```

## Search MCPs
If i say 'search mcp` I mean check any connected MCPs about search and/or deep research (for e.g. perplexity, brave, reddit). Depends on task use prefer real people experience on forums (for e.g. reddit, stackoverflow, hackernews, x, etc).


## 🧵 THREAD MODE & SEQUENTIAL THINKING INTEGRATION

### **Thread Continuation Rules**
```markdown
<thread_mode>
ACTIVATION:
- User says: "continue thread", "add to thread", "thread mode"
- Same category/topic within same session
- When sequential thinking MCP is active and building on previous thoughts

THREAD FILE STRUCTURE:
Format: {yyyymmdd}-{HHMM}-thread-{category}-{topic}.md

THREAD ORGANIZATION:
# H1.Prompt1 - {brief topic}
# H1.Output1
## H2.YourOriginalRequest
## H2.RequestChecklist
## H2.SequentialThinking (if exist, if uses sequential thinking mcp,etc)
## H2.MainOutput
# H1.Prompt2 - {continuation/new angle} 
# H1.Output3
## H2.YourOriginalRequest
## H2.RequestChecklist
## H2.SequentialThinking (if exist, if uses sequential thinking mcp,etc)
## H2.MainOutput
# H1.Prompt3 - {further development}
# H1.Output3
## H2.YourOriginalRequest
## H2.RequestChecklist
## H2.SequentialThinking (if exist, if uses sequential thinking mcp,etc)
## H2.MainOutput

AGAIN with more details:
EACH `H1.Output1` MUST SECTION INCLUDES:
### 🎯 Your Original Request
> {Brief 1-2 line summary of what user wanted}
## 📋 Request Checklist
What you asked for:
- [ ] Item 1 from request
- [ ] Item 2 from request  
- [ ] Item 3 from request
- [x] Item 4 (completed)
### 🧠 Sequential Thinking (Auto-captured from MCP)
### 🎯 Output
### {Relevant H4 subsections}
</thread_mode>
```

### **Sequential Thinking MCP Integration**
```markdown
<sequential_thinking_integration>
WHEN SEQUENTIAL THINKING MCP IS ACTIVE:
- Auto-capture ALL thinking data into dedicated H2 section
- Format in ````bash blocks (4 backticks for markdown safety)
- Include full JSON structure with thought progression
- Add thread context linking between H1 sections
- NO manual copying required - fully automated

### 🧠 Sequential Thinking
`bash
{JSON data from sequential thinking MCP with full thought structure}
# below is output of request sequential-thinking-mcp it has value to human, `response` system message don't need but response has VALUE to understand thinking process and helps get insights and educate PROMPTer-Human.
{
  `thought`: `{content}`,
  `thoughtNumber`: 1 # means {n} of thoughts,
  `totalThoughts`: 8  # means {n} of thoughts},
  `nextThoughtNeeded`: true
},
# important inside {content} for blocks `\n` replace new line do REAL NEW LINE instead of just write `\n`, because it's read by obsidian and markdown parser for Humans!
``

ENHANCED ADHD PROTOCOL:
📋 Sequential thinking process now captured automatically in separate block
🔢 Thought progression numbered and structured  
📐 Why→what→how→result maintained within thinking process
🔄 Analogies and connections tracked across thread sections
</sequential_thinking_integration>
```

### **Thread Detection & File Logic**
```markdown
<thread_file_logic>
FILE CREATION PRIORITY:
1. If continuing existing thread → append new H1 section to existing file
2. If new thread topic → create new thread file {yyyymmdd}-{HHMM}-thread-{category}-{topic}.md
3. If one-off request → use standard format {yyyymmdd}-{HHMM}-{ActionType}-{category}-{title}.md

THREAD MAGIC PHRASES:
- "continue thread" / "add to thread" / "thread mode" → Continue existing
- "new thread" / "new topic" → Start fresh thread file
- No thread keywords → Standard single-file behavior

CONTEXT PRESERVATION:
- Reference previous H1 sections when relevant
- Link sequential thinking across sections  
- Maintain topic coherence throughout thread
</thread_file_logic>
```

### **Enhanced ADHD Protocol (Thread-Aware)**
```markdown
<adhd_thread_enhanced>
THREAD-SPECIFIC CHECKLISTS:
✅ Each heading section has clear topic focus
✅ Request checklist tracks user's specific asks per section
✅ Sequential thinking auto-captured and structured
✅ Visual elements (mermaid/tables) when helpful across sections
✅ Numbered steps maintained within each H1 context

VISUAL INTEGRATION:
📊 Mermaid diagrams can span multiple H1 sections when showing process flow
📋 Comparison tables can reference findings from previous sections
🔢 Step numbering resets per H1 section for clarity
📐 Why→what→how→result structure applies to each major topic
🔄 Analogies to known concepts
📋 Comparison tables for A vs B
</adhd_thread_enhanced>
```

### **MCP Enhancement**
```markdown
<mcp_thread_awareness>
SEARCH MCP USAGE:
- When user says 'search mcp' in thread context, consider previous findings
- Build upon research from earlier H1 sections
- Reference community insights already discovered in thread

SEQUENTIAL THINKING MCP:
- Automatically active when complex reasoning required
- Captures thought progression across H1 sections
- Links related concepts from previous thinking in thread
- Maintains context awareness throughout session
</mcp_thread_awareness>
```

### **Updated Master Control Panel**
```mermaid
graph TB
    subgraph "🔴 P0: ENHANCED"
        P0[ADHD Core + Threads]
        P0 --> ST[🧠 Sequential Thinking Auto-capture]
        P0 --> M[📊 Mermaid ALL processes]
        P0 --> C[✅ Thread-aware checklists]
        P0 --> S[📐 Why→What→How per heading]
        P0 --> N[🔢 Steps per section]
        P0 --> A[🔄 Cross-section analogies]
        P0 --> T[📋 Thread-spanning tables]
    end
    
    subgraph "🧵 THREAD MODE"
        TM[Thread Detection]
        TM --> TC[Continue existing]
        TM --> TN[New thread]
        TM --> TS[Standard single file]
        TC --> H1[H1 sections]
        TN --> H1
        TS --> NORM[Normal workflow]
    endc
    
    subgraph "📁 FILE LOGIC"
        MD[Smart File Naming]
        MD --> THREAD[thread-category-topic]
        MD --> STANDARD[ActionType-category-title]
        MD --> AUTO[Auto-detection based on context]
    end
```
But if appliable you could use sequence or other types of diagrams!
Extremely important to check correct syntax and use KISS,YAGNI without difficulty-multiple titles and brackets and other specsymbols which could break syntax of mermaidjs.


---

Talk with me in russian. But use B2 english terms and all original slang, terms and concepts.

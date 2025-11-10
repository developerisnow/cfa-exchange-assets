---
created: 2025-10-30
updated: 2025-10-31 15:20
version: 1.2.1
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

### Workflow & AI Workplace
The actual operational setup spans macOS and two Ubuntu VPS servers with GUI orchestration:
- Servers
  - `AVA1` (Ubuntu): primary workhorse, runs Vibe Diffuse Kanban (password-protected), Codex & Cline auth installed
  - `CFA1` (Ubuntu): demo hosting for Velvet (Node.js exchange) and .NET services
  - `macOS-local`: initial sessions (8–15) with CLI agents and web tools
- Orchestrator: Vibe Diffuse Kanban (GUI). Each step = new session; sessions can reach hundreds per task. Do not mirror all raw sessions into the repo; only index high‑signal artefacts to `memory-bank` using `YYYYMMDD-HHMM-*` naming
- Coding agents/wrappers: Cline, Codex CLI, Codeium; testing OpenHands, Kodu, Droid, JustCode
- Deep Research: OpenAI DR, Anthropic DR, Gemini DR; Perplexity/Perlexity used only for research
- CLI: Gemini CLI (coding + analysis)
- Assistants: AI Studio as evaluator/teacher with large context (~1M tokens)
- tmux policy: per‑project tmux session; tabs for tools/tasks when working via CLI

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

---
created_at: 2025-10-30 20:31
agent: codex
agentID: 019a3616-5a4f-7ad3-94a4-f06c730c5130
partAgentID: 5a4f
type: blockers
---

Blocker — Missing manifest (SSOT)
- Not found: `polymarket.manifest.core.json`
- Also missing paths from AGENTS.md: `docs/manifest/rules.yaml`, `docs/manifest/structure.l3.json`, `docs/manifest/structure.schema.json`, `docs/manifest/csv.registry.schema.json`, `schemas/frontmatter.schema.json`

Request
- Provide the core manifest file or exact path if it exists under another name
- If absent, approve that I scaffold minimal placeholders to unblock linter/workflows

If scaffolding is approved, proposal
```json
{
  "name": "cifra-rwa-capital",
  "version": "0.1.0",
  "modules": {
    "rules": "docs/manifest/rules.yaml",
    "structure": "docs/manifest/structure.l3.json",
    "schemas": {
      "structure": "docs/manifest/structure.schema.json",
      "csv_registry": "docs/manifest/csv.registry.schema.json",
      "frontmatter": "schemas/frontmatter.schema.json"
    },
    "registries": "vaults/registries/"
  }
}
```


YOUVENV=/Users/user/__Repositories/yougile/yougile-mcp__justrussian/venv
CTX=memory-bank/context/yougile-mcp
EXPORTER=$(CTX)/20251110-0704-yougile-export-tasks.py

.PHONY: yougile-export-one yougile-export-all yougile-export-unassigned

yougile-export-one:
	$(YOUVENV)/bin/python $(EXPORTER) --out $(CTX) --one-assignee $$ASSIGNEE --max-tasks $${MAX_TASKS:-2000}

yougile-export-all:
	$(YOUVENV)/bin/python $(EXPORTER) --out $(CTX) --all-assignees --max-tasks $${MAX_TASKS:-5000}

yougile-export-unassigned:
	$(YOUVENV)/bin/python $(EXPORTER) --out $(CTX) --all-assignees --max-tasks $${MAX_TASKS:-5000}

# --- Git mirror helpers (GH <-> GitLab) ---
.PHONY: mirror/setup mirror/push push/all push/origin push/alex

# Configure multi-remote push mirroring for monorepo and submodules
mirror/setup:
	bash scripts/git_mirror.sh setup

# Push submodules (on-demand) and monorepo to origin (mirrors to alex via pushurl)
mirror/push push/all:
	bash scripts/git_mirror.sh push

# Optional explicit pushes
push/origin:
	git push origin --all && git push origin --tags

push/alex:
	git push alex --all || true; git push alex --tags || true

# --- Symlinks (portable) ---
.PHONY: symlinks/auto symlinks/relative symlinks/absolute

symlinks/auto:
	bash scripts/symlinks_rewire.sh auto

symlinks/relative:
	bash scripts/symlinks_rewire.sh relative

symlinks/absolute:
	bash scripts/symlinks_rewire.sh absolute

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


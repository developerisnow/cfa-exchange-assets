#!/usr/bin/env python3
"""
Export YouGile tasks assigned to a specific user (by email) into Markdown files
with YAML frontmatter, for storage under memory-bank/context/yougile-mcp.

Usage:
  YOUGILE_EMAIL=... YOUGILE_PASSWORD=... YOUGILE_COMPANY_ID=... \
  python3 scripts/yougile_export_tasks.py --assignee aa@cfa.capital \
    --out /Users/user/__Repositories/prj_Cifra-rwa-exachange-assets/memory-bank/context/yougile-mcp \
    --yougile-src /Users/user/__Repositories/yougile/yougile-mcp__justrussian/src

Notes:
  - Will create API key automatically if not present via env YOUGILE_API_KEY
  - Avoids committing secrets; reads all from environment
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def slugify(text: str, max_len: int = 64) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^a-z0-9\-\_\s]+", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text[:max_len] if max_len else text


def load_and_init_yougile(yougile_src: Path):
    # Insert parent of 'src' and import via 'src.*' to keep package context
    parent = yougile_src.parent
    sys.path.insert(0, str(parent))
    # Deferred imports after path insert
    from src.core.auth import AuthManager  # type: ignore
    from src.core.client import YouGileClient  # type: ignore
    from src.api import auth as auth_api  # type: ignore
    from src.api import users as users_api  # type: ignore
    from src.api import tasks as tasks_api  # type: ignore
    return AuthManager, YouGileClient, auth_api, users_api, tasks_api


def ensure_api_key(auth_api, auth_mgr, client_cls, email: str, password: str, company_id: str) -> str:
    api_key = os.environ.get("YOUGILE_API_KEY")
    if api_key:
        auth_mgr.set_credentials(api_key, company_id)
        return api_key

    # Create key via /auth/keys (company auto-detect if needed)
    async def _create():
        async with client_cls(auth_mgr.__class__()) as client:
            # If company_id is not UUID-like, try auto-detect
            import re
            is_uuid = bool(re.match(r"^[0-9a-fA-F-]{32,36}$", company_id or ""))
            comp_id = company_id
            if not is_uuid:
                companies = await auth_api.get_companies(client, email, password)
                if not companies:
                    raise SystemExit("No companies available for provided credentials")
                if len(companies) > 1:
                    raise SystemExit("Multiple companies found; set YOUGILE_COMPANY_ID explicitly")
                comp_id = companies[0].get("id")
            return await auth_api.create_api_key(client, email, password, comp_id)

    # Run in simple event loop
    import asyncio
    api_key = asyncio.run(_create())
    auth_mgr.set_credentials(api_key, company_id)
    return api_key


def get_user_id_by_email(users_api, client_cls, auth_mgr, email: str) -> str:
    import asyncio

    async def _get():
        async with client_cls(auth_mgr) as client:
            user_list = await users_api.get_users(client)
        for u in user_list:
            if (u.get("email") or "").lower() == email.lower():
                return u.get("id")
        raise SystemExit(f"Assignee email not found in users: {email}")

    return asyncio.run(_get())


def list_tasks_for_assignee(tasks_api, client_cls, auth_mgr, user_id: str) -> List[Dict[str, Any]]:
    import asyncio

    async def _list():
        results: List[Dict[str, Any]] = []
        limit = 100
        offset = 0
        async with client_cls(auth_mgr) as client:
            while True:
                batch = await tasks_api.get_tasks(client, assigned_to=user_id, limit=limit, offset=offset, include_deleted=False)
                if not batch:
                    break
                results.extend(batch)
                if len(batch) < limit:
                    break
                offset += len(batch)
        return results

    return asyncio.run(_list())


def write_task_markdown(out_dir: Path, task: Dict[str, Any], agent_id: str, part_agent_id: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now()
    file_ts = ts.strftime("%Y%m%d-%H%M")
    title = task.get("title") or "untitled"
    slug = slugify(title)
    task_id = task.get("id", "")
    fname = f"{file_ts}-yougile-{slug}-{task_id[:8]}.md"
    path = out_dir / fname

    # Build frontmatter
    created = ts.strftime("%Y-%m-%d %H:%M")
    deadline = task.get("deadline") or {}
    assigned = task.get("assigned") or []
    url = f"https://yougile.com/task/{task_id}" if task_id else ""

    frontmatter = f"""---
created: {created}
type: task
sphere: operations
topic: yougile
author: Yougile
agentID: {agent_id}
partAgentID: [{part_agent_id}]
version: 0.1.0
tags: [yougile, task]

yougile:
  id: "{task_id}"
  project: ""
  board: ""
  status: "{task.get('status', '')}"
  assignees: {assigned}
  priority: "{task.get('priority', '')}"
  due: "{deadline.get('deadline', '')}"
  created_by: "{task.get('createdBy', '')}"
  url: "{url}"
---
"""

    # Description may be HTML
    description = task.get("description") or ""
    body_lines = [frontmatter, f"# {title}", "", "## Description", description or "(no description)"]
    content = "\n".join(map(str, body_lines))
    path.write_text(content, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assignee", required=True, help="Assignee email")
    parser.add_argument("--out", required=True, help="Output directory for markdown files")
    parser.add_argument("--yougile-src", required=True, help="Path to yougile-mcp src directory")
    parser.add_argument("--agent-id", default="019a5914-6519-7752-a558-3a161f0a2407")
    parser.add_argument("--part-agent-id", default="co-6519")
    args = parser.parse_args()

    yougile_src = Path(args.yougile_src).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()

    # Load env
    email = os.environ.get("YOUGILE_EMAIL")
    password = os.environ.get("YOUGILE_PASSWORD")
    company_id = os.environ.get("YOUGILE_COMPANY_ID")
    if not all([email, password, company_id]):
        raise SystemExit("Missing YOUGILE_EMAIL / YOUGILE_PASSWORD / YOUGILE_COMPANY_ID env vars")

    AuthManager, YouGileClient, auth_api, users_api, tasks_api = load_and_init_yougile(yougile_src)
    auth_mgr = AuthManager()
    ensure_api_key(auth_api, auth_mgr, YouGileClient, email, password, company_id)
    user_id = get_user_id_by_email(users_api, YouGileClient, auth_mgr, args.assignee)
    tasks = list_tasks_for_assignee(tasks_api, YouGileClient, auth_mgr, user_id)

    written: List[Path] = []
    for t in tasks:
        p = write_task_markdown(out_dir, t, args.agent_id, args.part_agent_id)
        written.append(p)

    print(f"Exported {len(written)} tasks to {out_dir}")


if __name__ == "__main__":
    main()

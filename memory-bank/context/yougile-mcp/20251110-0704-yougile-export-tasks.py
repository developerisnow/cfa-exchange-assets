#!/usr/bin/env python3
"""
Yougile → Markdown exporter (per-assignee folders)

Features
- Loads env from .env.local / .env in this folder (no MCP needed)
- Uses yougile-mcp client code, but executes under its venv for deps
- Fetches all tasks and writes into:
  <out>/<assignee_email>/... or <out>/not-assigned/...
- Stable re-sync by yougile.id: updates existing files instead of duplicating

Usage
  python3 2025xxxx-xxxx-yougile-export-tasks.py \
    --out <base_out_dir>  # defaults to script folder
    [--one-assignee EMAIL]  # optional filter (else: all assignees)

Env (.env.local or .env in same folder)
  YOUGILE_BASE_URL=https://yougile.com
  YOUGILE_EMAIL=aa@cfa.capital
  YOUGILE_PASSWORD=...  (required if no YOUGILE_API_KEY)
  YOUGILE_COMPANY_ID=98ab8509-9e44-447d-9654-50ff0f730cac  (optional if single company)
  YOUGILE_API_KEY=... (optional; if absent, will be created)
  YOUGILE_MCP_SRC=~/__Repositories/yougile/yougile-mcp__justrussian/src
  YOUGILE_VENV=~/__Repositories/yougile/yougile-mcp__justrussian/venv

Notes
- If this script is not running under YOUGILE_VENV, it will re-exec itself with that Python.
- Future re-sync uses YAML frontmatter yougile.id to match and update files.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# Lightweight .env loader
# -----------------------------
def load_env_from(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


def ensure_venv_exec():
    venv_dir = os.environ.get("YOUGILE_VENV")
    if not venv_dir:
        return  # best effort
    vpy_path = Path(venv_dir).expanduser().resolve() / "bin" / "python"
    try:
        cur = Path(sys.executable).resolve()
        vpy_real = vpy_path.resolve()
        if cur != vpy_real:
            os.execv(str(vpy_path), [str(vpy_path)] + sys.argv)  # re-exec under venv
    except Exception:
        pass


# -----------------------------
# Helpers
# -----------------------------
def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\-\_\s]+", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text[:max_len] if max_len else text


def map_user_ids_to_emails(users_api, client_cls, auth_mgr) -> Dict[str, str]:
    import asyncio

    async def _get():
        async with client_cls(auth_mgr) as client:
            data = await users_api.get_users(client)
        mapping = {}
        for u in data:
            uid = u.get("id")
            email = (u.get("email") or u.get("name") or "").strip()
            if uid and email:
                mapping[uid] = email
        return mapping

    return asyncio.run(_get())


def fetch_all_tasks(tasks_api, client_cls, auth_mgr, one_assignee_id: Optional[str], max_tasks: int = 5000, only_unassigned: bool = False) -> List[Dict[str, Any]]:
    import asyncio

    async def _list():
        results: List[Dict[str, Any]] = []
        limit = 1000
        offset = 0
        async with client_cls(auth_mgr) as client:
            while True:
                batch = await tasks_api.get_tasks(
                    client,
                    assigned_to=one_assignee_id,
                    limit=limit,
                    offset=offset,
                    include_deleted=False,
                )
                if not batch:
                    break
                if only_unassigned:
                    batch = [t for t in batch if not (t.get("assigned") or [])]
                results.extend(batch)
                if len(results) >= max_tasks:
                    results[:] = results[:max_tasks]
                    break
                if len(batch) < limit:
                    break
                offset += len(batch)
        return results

    return asyncio.run(_list())


def ensure_api_key(auth_api, auth_mgr, client_cls, email: str, password: str, company_id: Optional[str]) -> str:
    api_key = os.environ.get("YOUGILE_API_KEY")
    if api_key:
        auth_mgr.set_credentials(api_key, (company_id or ""))
        return api_key

    import asyncio

    async def _create():
        async with client_cls(auth_mgr.__class__()) as client:
            comp_id = company_id
            if not comp_id or not re.match(r"^[0-9a-fA-F-]{32,36}$", comp_id):
                companies = await auth_api.get_companies(client, email, password)
                if not companies:
                    raise SystemExit("No companies available for provided credentials")
                if len(companies) > 1 and not company_id:
                    raise SystemExit("Multiple companies found; set YOUGILE_COMPANY_ID explicitly in .env")
                comp_id = companies[0].get("id") if not company_id else company_id
            return await auth_api.create_api_key(client, email, password, comp_id)

    api_key = asyncio.run(_create())
    auth_mgr.set_credentials(api_key, (company_id or ""))
    return api_key


def list_all_users(users_api, client_cls, auth_mgr) -> List[Dict[str, Any]]:
    import asyncio

    async def _get():
        async with client_cls(auth_mgr) as client:
            return await users_api.get_users(client)

    return asyncio.run(_get())


def build_mappings(boards_api, columns_api, projects_api, client_cls, auth_mgr) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """Return (columns_by_id, boards_by_id, projects_by_id)."""
    import asyncio

    async def _load():
        async with client_cls(auth_mgr) as client:
            # Boards (paginate)
            boards: List[Dict[str, Any]] = []
            b_off = 0
            b_lim = 500
            while True:
                chunk = await boards_api.get_boards(client, limit=b_lim, offset=b_off, include_deleted=False)
                if not chunk:
                    break
                boards.extend(chunk)
                if len(chunk) < b_lim:
                    break
                b_off += len(chunk)

            # Columns (all)
            columns = await columns_api.get_columns(client)

            # Projects (all)
            projects = await projects_api.get_projects(client)

            return columns, boards, projects

    columns, boards, projects = asyncio.run(_load())
    columns_by_id = {c.get("id"): c for c in columns}
    boards_by_id = {b.get("id"): b for b in boards}
    projects_by_id = {p.get("id"): p for p in projects}
    return columns_by_id, boards_by_id, projects_by_id


def enrich_task(task: Dict[str, Any], columns_by_id: Dict[str, Dict[str, Any]], boards_by_id: Dict[str, Dict[str, Any]], projects_by_id: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    t = dict(task)
    col_id = t.get("columnId")
    col = columns_by_id.get(col_id) if col_id else None
    board = boards_by_id.get((col or {}).get("boardId")) if col else None
    project = projects_by_id.get((board or {}).get("projectId")) if board else None
    t["columnTitle"] = (col or {}).get("title")
    t["boardTitle"] = (board or {}).get("title")
    t["projectTitle"] = (project or {}).get("title")
    # Status: completed → Done, else column title
    if t.get("completed"):
        t["statusResolved"] = "Done"
    else:
        t["statusResolved"] = t.get("columnTitle") or ""
    return t


def build_index_for_subdir(subdir: Path) -> Dict[str, Path]:
    index: Dict[str, Path] = {}
    if not subdir.exists():
        return index
    for p in subdir.glob("*.md"):
        try:
            name = p.name
            # Attempt to extract id from filename suffix
            m = re.search(r"-([0-9a-fA-F-]{8,36})\.md$", name)
            if m:
                index[m.group(1)] = p
                continue
            # Fallback: inspect frontmatter head
            head = "\n".join(p.read_text(encoding="utf-8").splitlines()[:80])
            m2 = re.search(r"yougile:\s*\n\s*id:\s*['\"]([0-9a-fA-F-]{8,36})['\"]", head)
            if m2:
                index[m2.group(1)] = p
        except Exception:
            continue
    return index


def write_md(out_dir: Path, task: Dict[str, Any], agent_id: str, part_agent_id: str, existing: Optional[Path]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    now_ts = now.strftime("%Y-%m-%d %H:%M")
    file_ts = now.strftime("%Y%m%d-%H%M")

    title = (task.get("title") or "untitled").strip()
    slug = slugify(title)
    task_id = task.get("id", "")
    url = f"https://yougile.com/task/{task_id}" if task_id else ""
    assigned = task.get("assigned") or []
    deadline = task.get("deadline") or {}
    project_title = task.get("projectTitle") or ""
    board_title = task.get("boardTitle") or ""
    status_resolved = task.get("statusResolved") or task.get("status", "")
    # normalize yougile timestamp if present
    yg_ts_raw = task.get("timestamp")
    yg_ts_iso = ""
    if isinstance(yg_ts_raw, str):
        yg_ts_iso = yg_ts_raw.replace("Z", "+00:00")
    elif isinstance(yg_ts_raw, (int, float)):
        try:
            # Detect ms vs s
            secs = yg_ts_raw / 1000 if yg_ts_raw > 1e12 else yg_ts_raw
            yg_ts_iso = datetime.fromtimestamp(secs, tz=timezone.utc).isoformat()
        except Exception:
            yg_ts_iso = ""

    # Stable filename if exists
    if existing and existing.exists():
        path = existing
        # Try to preserve original created timestamp from file name
        try:
            created_ts = None
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines[:50]):
                if line.startswith("created:"):
                    created_ts = line.split(":", 1)[1].strip()
                    break
        except Exception:
            created_ts = None
    else:
        # Use full task id in filename for uniqueness
        filename = f"{file_ts}-yougile-{slug}-{task_id}.md"
        path = out_dir / filename
        created_ts = now_ts

    # Build frontmatter
    fm = [
        "---",
        f"created: {created_ts or now_ts}",
        f"updated: {now_ts}",
        "type: task",
        "sphere: operations",
        "topic: yougile",
        "author: Yougile",
        f"agentID: {agent_id}",
        f"partAgentID: [{part_agent_id}]",
        "version: 0.1.0",
        "tags: [yougile, task]",
        "",
        "yougile:",
        f"  id: \"{task_id}\"",
        f"  project: \"{project_title}\"",
        f"  board: \"{board_title}\"",
        f"  status: \"{status_resolved}\"",
        f"  assignees: {assigned}",
        f"  priority: \"{task.get('priority', '')}\"",
        f"  due: \"{deadline.get('deadline', '')}\"",
        f"  created_by: \"{task.get('createdBy', '')}\"",
        f"  url: \"{url}\"",
        f"  timestamp: \"{yg_ts_iso}\"",
        f"  completed: {bool(task.get('completed', False))}",
        f"  archived: {bool(task.get('archived', False))}",
        "---",
        "",
        f"# {title}",
        "",
        "## Description",
        task.get("description") or "(no description)",
    ]
    path.write_text("\n".join(map(str, fm)), encoding="utf-8")
    return path


def write_users_alias_csv(out_base: Path, users: List[Dict[str, Any]]):
    import csv
    out_path = out_base / "users-aliases.csv"
    fields = ["id", "email", "realName", "name", "role", "departments"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for u in users:
            row = {
                "id": u.get("id", ""),
                "email": u.get("email", ""),
                "realName": u.get("realName", ""),
                "name": u.get("name", ""),
                "role": u.get("role", ""),
                "departments": ",".join(u.get("departments", []) if isinstance(u.get("departments"), list) else [])
            }
            w.writerow(row)

def main():
    # Load env from local files in script dir
    here = Path(__file__).resolve().parent
    load_env_from(here / ".env.local")
    load_env_from(here / ".env")

    # Re-exec under the yougile venv if configured
    ensure_venv_exec()

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(here), help="Base output directory (default: script folder)")
    parser.add_argument("--one-assignee", default=None, help="Optional: filter by a single assignee email")
    parser.add_argument("--agent-id", default="019a5914-6519-7752-a558-3a161f0a2407")
    parser.add_argument("--part-agent-id", default="co-6519")
    parser.add_argument("--max-tasks", type=int, default=5000, help="Safety cap for total tasks fetched (default 5000)")
    parser.add_argument("--all-assignees", action="store_true", help="Iterate per-user and export into per-assignee folders, plus not-assigned")
    parser.add_argument("--by-creator", action="store_true", default=True, help="Group tasks into by-creator/<email>/ folders (default on)")
    parser.add_argument("--assignee-folders", action="store_true", help="Additionally write per-assignee/not-assigned folders (off by default)")
    args = parser.parse_args()

    # Resolve paths and env
    out_base = Path(args.out).expanduser().resolve()
    mcp_src = Path(os.environ.get("YOUGILE_MCP_SRC", "~/__Repositories/yougile/yougile-mcp__justrussian/src")).expanduser().resolve()
    sys.path.insert(0, str(mcp_src.parent))  # import via src.*

    from src.core.auth import AuthManager  # type: ignore
    from src.core.client import YouGileClient  # type: ignore
    from src.api import auth as auth_api  # type: ignore
    from src.api import users as users_api  # type: ignore
    from src.api import tasks as tasks_api  # type: ignore
    from src.api import boards as boards_api  # type: ignore
    from src.api import columns as columns_api  # type: ignore
    from src.api import projects as projects_api  # type: ignore

    email = os.environ.get("YOUGILE_EMAIL")
    password = os.environ.get("YOUGILE_PASSWORD")
    company_id = os.environ.get("YOUGILE_COMPANY_ID")
    if not (email and (password or os.environ.get("YOUGILE_API_KEY"))):
        raise SystemExit("YOUGILE_EMAIL and YOUGILE_PASSWORD or YOUGILE_API_KEY are required in .env")

    auth_mgr = AuthManager()
    ensure_api_key(auth_api, auth_mgr, YouGileClient, email, password or "", company_id)

    # users map and full list
    id_to_email = map_user_ids_to_emails(users_api, YouGileClient, auth_mgr)
    all_users_list = list_all_users(users_api, YouGileClient, auth_mgr)
    # persist aliases for downstream matching
    write_users_alias_csv(out_base, all_users_list)
    # mappings for enrich
    columns_by_id, boards_by_id, projects_by_id = build_mappings(boards_api, columns_api, projects_api, YouGileClient, auth_mgr)

    def write_tasks_to_targets(task_list: List[Dict[str, Any]]):
        written_local = 0
        subdir_index_cache: Dict[Path, Dict[str, Path]] = {}
        for raw in task_list:
            t = enrich_task(raw, columns_by_id, boards_by_id, projects_by_id)
            assignees = t.get("assigned") or []
            emails: List[str] = [id_to_email.get(uid, None) for uid in assignees]
            emails = [e for e in emails if e]
            targets = emails if emails else ["not-assigned"]
            creator_id = t.get("createdBy")
            creator_email = id_to_email.get(creator_id, creator_id or "unknown")
            creator_targets = []
            if creator_email:
                creator_targets = [Path("by-creator") / creator_email]
            # by-creator is default
            if args.by_creator and creator_targets:
                for ct in creator_targets:
                    subdir = out_base / ct
                    if subdir not in subdir_index_cache:
                        subdir_index_cache[subdir] = build_index_for_subdir(subdir)
                    existing = subdir_index_cache[subdir].get(t.get("id", ""))
                    write_md(subdir, t, args.agent_id, args.part_agent_id, existing)
                    if not existing:
                        new_files = sorted(subdir.glob(f"*-yougile-*-{t.get('id','')}*.md"))
                        if new_files:
                            subdir_index_cache[subdir][t.get("id", "")] = new_files[-1]
                    written_local += 1
            # optional per-assignee folders
            if args.assignee_folders:
                for tgt in targets:
                    subdir = out_base / tgt
                    if subdir not in subdir_index_cache:
                        subdir_index_cache[subdir] = build_index_for_subdir(subdir)
                    existing = subdir_index_cache[subdir].get(t.get("id", ""))
                    write_md(subdir, t, args.agent_id, args.part_agent_id, existing)
                    if not existing:
                        new_files = sorted(subdir.glob(f"*-yougile-*-{t.get('id','')}*.md"))
                        if new_files:
                            subdir_index_cache[subdir][t.get("id", "")] = new_files[-1]
                    written_local += 1
        return written_local

    written = 0
    if args.all_assignees:
        # Iterate per user (faster, avoids giant all-tasks fetch)
        all_users = list_all_users(users_api, YouGileClient, auth_mgr)
        for u in all_users:
            uid = u.get("id")
            if not uid:
                continue
            per_user_tasks = fetch_all_tasks(tasks_api, YouGileClient, auth_mgr, uid, max_tasks=args.max_tasks)
            written += write_tasks_to_targets(per_user_tasks)
        # Unassigned
        if args.assignee_folders:
            unassigned = fetch_all_tasks(tasks_api, YouGileClient, auth_mgr, None, max_tasks=args.max_tasks, only_unassigned=True)
            written += write_tasks_to_targets(unassigned)
    else:
        # Single-assignee or all-in-one
        one_assignee_id: Optional[str] = None
        if args.one_assignee:
            inv = {v.lower(): k for k, v in id_to_email.items()}
            one_assignee_id = inv.get(args.one_assignee.lower())
            if not one_assignee_id:
                raise SystemExit(f"Assignee email not found: {args.one_assignee}")
        tasks = fetch_all_tasks(tasks_api, YouGileClient, auth_mgr, one_assignee_id, max_tasks=args.max_tasks)
        written += write_tasks_to_targets(tasks)

    print(f"Exported {written} file(s) into {out_base}")


if __name__ == "__main__":
    main()
def write_users_alias_csv(out_base: Path, users: List[Dict[str, Any]]):
    import csv
    out_path = out_base / "users-aliases.csv"
    fields = ["id", "email", "realName", "name", "role", "departments"]
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for u in users:
            row = {
                "id": u.get("id", ""),
                "email": u.get("email", ""),
                "realName": u.get("realName", ""),
                "name": u.get("name", ""),
                "role": u.get("role", ""),
                "departments": ",".join(u.get("departments", []) if isinstance(u.get("departments"), list) else [])
            }
            w.writerow(row)

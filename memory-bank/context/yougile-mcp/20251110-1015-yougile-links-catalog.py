#!/usr/bin/env python3
"""
Build a catalog of all links referenced in exported Yougile tasks
from Markdown files in the context folder. Optionally include links
from task comments via Yougile API.

Outputs: links-catalog.csv (task_id, title, url, domain, source)
Sources: description | comment
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, List, Tuple


def load_env(path: Path):
    for fname in (".env.local", ".env"):
        p = path / fname
        if p.exists():
            for raw in p.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                k = k.strip(); v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v


def parse_frontmatter_and_title(md: Path) -> Tuple[Dict[str, str], str]:
    data: Dict[str, str] = {}
    title = md.stem
    try:
        txt = md.read_text(encoding="utf-8")
    except Exception:
        return data, title
    lines = txt.splitlines()
    if not lines or not lines[0].strip().startswith('---'):
        return data, title
    i = 1
    while i < len(lines) and not lines[i].strip().startswith('---'):
        line = lines[i]
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
        if line.strip().startswith('yougile:'):
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                if ln.strip().startswith('---'):
                    break
                if ':' in ln:
                    kk, vv = ln.split(':', 1)
                    key = kk.strip(); val = vv.strip().strip('"').strip("'")
                    if key in {"id", "url"}:
                        data[f"yougile.{key}"] = val
                j += 1
            break
        i += 1
    # title from first H1 after frontmatter
    for ln in lines[i+1:i+80]:
        if ln.startswith('# '):
            title = ln[2:].strip()
            break
    return data, title


def extract_links_from_text(html_or_md: str) -> List[str]:
    # href= "..."
    hrefs = re.findall(r'href=\"([^\"]+)\"', html_or_md, flags=re.IGNORECASE)
    # bare http(s)
    bares = re.findall(r'(https?://[\w\-._~:/?#\[\]@!$&\'()*+,;=%]+)', html_or_md)
    urls = set(hrefs + bares)
    return [u for u in urls if u.startswith('http')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=str(Path(__file__).resolve().parent))
    ap.add_argument('--include-comments', action='store_true', help='Query Yougile API for task comments and extract links')
    args = ap.parse_args()

    base = Path(args.base)
    load_env(base)

    rows: List[Tuple[str, str, str, str, str]] = []

    # Optional API clients
    client = None
    id_to_email: Dict[str, str] = {}
    if args.include-comments:
        # import yougile sdk and build client
        import sys
        mcp_src = Path(os.environ.get('YOUGILE_MCP_SRC', '~/__Repositories/yougile/yougile-mcp__justrussian/src')).expanduser().resolve()
        sys.path.insert(0, str(mcp_src.parent))
        from src.core.auth import AuthManager  # type: ignore
        from src.core.client import YouGileClient  # type: ignore
        from src.api import users as users_api  # type: ignore
        from src.api import chats as chats_api  # type: ignore
        from src.api import auth as auth_api  # type: ignore
        email = os.environ.get('YOUGILE_EMAIL'); pwd = os.environ.get('YOUGILE_PASSWORD'); cid = os.environ.get('YOUGILE_COMPANY_ID')
        if not email or not (pwd or os.environ.get('YOUGILE_API_KEY')):
            raise SystemExit('Missing YOUGILE_EMAIL and YOUGILE_PASSWORD or YOUGILE_API_KEY in .env')
        am = AuthManager()
        # simple ensure key
        import asyncio, re as _re
        async def _ensure():
            async with YouGileClient(am.__class__()) as c:
                comp_id = cid
                if not comp_id or not _re.match(r'^[0-9a-fA-F-]{32,36}$', comp_id):
                    comps = await auth_api.get_companies(c, email, pwd)
                    comp_id = comps[0]['id']
                key = os.environ.get('YOUGILE_API_KEY')
                if not key:
                    key = await auth_api.create_api_key(c, email, pwd, comp_id)
            am.set_credentials(key, comp_id)
            async with YouGileClient(am) as c:
                users = await users_api.get_users(c)
            return users
        users = asyncio.run(_ensure())
        id_to_email = {u.get('id'): (u.get('email') or u.get('name') or '') for u in users}
        client = YouGileClient(am)

    # Walk files
    for sub in base.rglob('*.md'):
        if sub.name.endswith('weekly-summary.md'):
            continue
        fm, title = parse_frontmatter_and_title(sub)
        tid = fm.get('yougile.id', '')
        url = fm.get('yougile.url', '')
        # description links
        text = sub.read_text(encoding='utf-8')
        idx = text.find('## Description')
        body = text[idx:] if idx != -1 else text
        for u in extract_links_from_text(body):
            domain = urlparse(u).netloc
            rows.append((tid, title, u, domain, 'description'))

        # comment links via API
        if args.include-comments and tid and client is not None:
            import asyncio
            from src.api import chats as chats_api  # type: ignore
            async def _comments():
                async with client:  # type: ignore
                    msgs = await chats_api.get_chat_messages(client, tid)
                return msgs
            msgs = asyncio.run(_comments())
            for m in msgs or []:
                text = m.get('textHtml') or m.get('text') or ''
                for u in extract_links_from_text(text):
                    domain = urlparse(u).netloc
                    rows.append((tid, title, u, domain, 'comment'))

    # write CSV
    out = base / 'links-catalog.csv'
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['task_id', 'title', 'url', 'domain', 'source'])
        for r in rows:
            w.writerow(list(r))
    print(f'Links catalog written: {out} ({len(rows)} rows)')


if __name__ == '__main__':
    main()


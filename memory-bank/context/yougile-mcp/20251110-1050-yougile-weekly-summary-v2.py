#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timedelta, timezone


def parse_frontmatter(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except Exception:
        return data
    if not lines or not lines[0].strip().startswith('---'):
        return data
    for i in range(1, min(len(lines), 120)):
        line = lines[i].strip()
        if line.startswith('---'):
            break
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
        if line.startswith('yougile:'):
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                if ln.strip().startswith('---'):
                    break
                if ':' in ln:
                    kk, vv = ln.split(':', 1)
                    key = kk.strip(); val = vv.strip().strip('"').strip("'")
                    if key in {'id','url','timestamp','completed'}:
                        data[f'yougile.{key}'] = val
                j += 1
            break
    return data


def safe_iso_to_dt(s: str):
    try:
        if not s:
            return None
        return datetime.fromisoformat(s)
    except Exception:
        try:
            return datetime.fromisoformat(s + '+00:00')
        except Exception:
            return None


def load_aliases(base: Path):
    aliases = {}
    csv_path = base / 'users-aliases.csv'
    if not csv_path.exists():
        return aliases
    with csv_path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            email = (r.get('email') or '').strip()
            if not email:
                continue
            aliases[email.lower()] = {
                'email': email,
                'realName': r.get('realName') or r.get('name') or '',
                'role': r.get('role') or ''
            }
    return aliases


def build_id_to_relpath(base: Path):
    mapping = {}
    cand = base / 'by-creator'
    if cand.exists():
        for md in cand.rglob('*.md'):
            try:
                text = md.read_text(encoding='utf-8')
            except Exception:
                continue
            lines = text.splitlines()[:120]
            tid = ''
            for ln in lines:
                if ln.strip().startswith('id:'):
                    tid = ln.split(':',1)[1].strip().strip('"').strip("'")
                    break
            if tid:
                mapping.setdefault(tid, str(md.relative_to(base)))
    return mapping


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=str(Path(__file__).resolve().parent))
    args = ap.parse_args()

    base = Path(args.base)
    since = datetime.now(timezone.utc) - timedelta(days=7)

    per_user: Dict[str, Dict[str, List[Tuple[str, str, str]]]] = {}
    aliases = load_aliases(base)
    id_to_rel = build_id_to_relpath(base)

    creator_root = base / 'by-creator'
    if not creator_root.exists():
        print('by-creator folder not found; nothing to summarize')
        return

    for sub in sorted(p for p in creator_root.iterdir() if p.is_dir()):
        for md in sub.glob('*.md'):
            fm = parse_frontmatter(md)
            ts = safe_iso_to_dt(fm.get('yougile.timestamp',''))
            if not ts or ts < since:
                continue
            # title
            title = md.stem
            for ln in md.read_text(encoding='utf-8').splitlines()[60:120]:
                if ln.startswith('# '):
                    title = ln[2:].strip()
                    break
            url = fm.get('yougile.url','')
            completed = (fm.get('yougile.completed','false').lower()=='true')
            rel = id_to_rel.get(fm.get('yougile.id',''), '')
            bucket = per_user.setdefault(sub.name, {'touched': [], 'completed': []})
            bucket['touched'].append((title, url, rel))
            if completed:
                bucket['completed'].append((title, url, rel))

    out_ts = datetime.now().strftime('%Y%m%d-%H%M')
    out = base / f"{out_ts}-yougile-weekly-summary.md"
    lines: List[str] = []
    lines.append('---')
    lines.append(f"created: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append('type: report')
    lines.append('sphere: operations')
    lines.append('topic: yougile-weekly-summary')
    lines.append('author: Yougile')
    lines.append('version: 0.1.1')
    lines.append('tags: [yougile, summary, weekly]')
    lines.append('---\n')

    lines.append('# Weekly Activity (last 7 days)\n')
    lines.append(f"- Users active: {len(per_user)}")
    lines.append(f"- Tasks touched: {sum(len(v['touched']) for v in per_user.values())}")
    lines.append(f"- Tasks completed: {sum(len(v['completed']) for v in per_user.values())}\n")

    for user, buckets in sorted(per_user.items()):
        info = aliases.get(user.lower(), {'realName':'','role':''})
        role = info.get('role') or ''
        rname = info.get('realName') or ''
        lines.append(f"## {user} — {role} — {rname}")
        lines.append(f"- Touched: {len(buckets['touched'])}")
        lines.append(f"- Completed: {len(buckets['completed'])}\n")
        if buckets['completed']:
            lines.append('### Completed')
            for title, url, rel in buckets['completed'][:50]:
                wikilink = f"[[{rel}]]" if rel else title
                lines.append(f"- [x] {wikilink} ([{title}]({url}))")
            lines.append('')
        if buckets['touched']:
            lines.append('### Touched')
            for title, url, rel in buckets['touched'][:100]:
                wikilink = f"[[{rel}]]" if rel else title
                lines.append(f"- [ ] {wikilink} ([{title}]({url}))")
            lines.append('')

    out.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Summary written to {out}")


if __name__ == '__main__':
    main()

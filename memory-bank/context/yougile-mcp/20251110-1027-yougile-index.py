#!/usr/bin/env python3
from __future__ import annotations
import csv
from pathlib import Path
from typing import Dict, Set, List, Tuple


def parse_frontmatter(md: Path) -> Dict[str, str]:
    d: Dict[str, str] = {}
    try:
        lines = md.read_text(encoding='utf-8').splitlines()
    except Exception:
        return d
    if not lines or not lines[0].startswith('---'):
        return d
    i = 1
    while i < len(lines) and not lines[i].startswith('---'):
        line = lines[i]
        if ':' in line:
            k, v = line.split(':', 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
        if line.strip().startswith('yougile:'):
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                if ln.strip().startswith('---'):
                    break
                if ':' in ln:
                    kk, vv = ln.split(':', 1)
                    key = kk.strip(); val = vv.strip().strip('"').strip("'")
                    if key in {'id','url','created_by','assignees'}:
                        d[f'yougile.{key}'] = val
                j += 1
            break
        i += 1
    # title
    title = md.stem
    for ln in lines[i+1:i+50]:
        if ln.startswith('# '):
            title = ln[2:].strip()
            break
    d['title'] = title
    return d


def main():
    base = Path(__file__).resolve().parent
    seen_paths: Dict[str, List[str]] = {}
    meta: Dict[str, Dict[str,str]] = {}
    for md in base.rglob('*.md'):
        if md.name.endswith('weekly-summary.md'):
            continue
        fm = parse_frontmatter(md)
        tid = fm.get('yougile.id') or ''
        if not tid:
            continue
        seen_paths.setdefault(tid, []).append(str(md.relative_to(base)))
        if tid not in meta:
            meta[tid] = {
                'title': fm.get('title',''),
                'creator': fm.get('yougile.created_by',''),
                'assignees': fm.get('yougile.assignees','')
            }

    out = base / 'yougile-index.csv'
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['id','title','creator','assignees','paths_count'])
        for tid, paths in seen_paths.items():
            m = meta.get(tid, {})
            w.writerow([tid, m.get('title',''), m.get('creator',''), m.get('assignees',''), len(paths)])
    print(f'Index written: {out} (unique tasks: {len(seen_paths)}, files: {sum(len(v) for v in seen_paths.values())})')


if __name__ == '__main__':
    main()


#!/usr/bin/env python3
"""
Weekly summary (last 7 days) from exported Yougile markdown files.

Reads frontmatter fields written by the exporter, groups by assignee folder.
This is a best-effort snapshot (no event log API yet). Timestamp used: yougile.timestamp.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple


def parse_frontmatter(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return data
    if not lines or not lines[0].strip().startswith("---"):
        return data
    for i in range(1, min(len(lines), 120)):
        line = lines[i].strip()
        if line.startswith("---"):
            break
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
        # Nested yougile fields: track only needed keys
        if line.startswith("yougile:"):
            # continue to nested keys
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                if ln.strip().startswith("---"):
                    break
                if ":" in ln:
                    kk, vv = ln.split(":", 1)
                    key = kk.strip()
                    val = vv.strip().strip('"').strip("'")
                    if key in {"id", "url", "timestamp", "completed"}:
                        data[f"yougile.{key}"] = val
                j += 1
            break
    return data


def safe_iso_to_dt(s: str) -> datetime | None:
    try:
        if not s:
            return None
        return datetime.fromisoformat(s)
    except Exception:
        try:
            # accept without tz
            return datetime.fromisoformat(s + "+00:00")
        except Exception:
            return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=str(Path(__file__).resolve().parent), help="Base folder with assignee subfolders")
    args = ap.parse_args()

    base = Path(args.base)
    since = datetime.now(timezone.utc) - timedelta(days=7)

    per_user: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}
    # structure: email -> {"touched": [(title, url)], "completed": [(title, url)]}

    for sub in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith('.')):
        if sub.name in {"__pycache__"}:
            continue
        for md in sub.glob("*.md"):
            fm = parse_frontmatter(md)
            ts = safe_iso_to_dt(fm.get("yougile.timestamp", ""))
            if not ts or ts < since:
                continue
            # title = first H1 after frontmatter or filename fallback
            title = md.stem
            for ln in md.read_text(encoding="utf-8").splitlines()[60:120]:
                if ln.startswith("# "):
                    title = ln[2:].strip()
                    break
            url = fm.get("yougile.url", "")
            completed = (fm.get("yougile.completed", "false").lower() == "true")
            bucket = per_user.setdefault(sub.name, {"touched": [], "completed": []})
            bucket["touched"].append((title, url))
            if completed:
                bucket["completed"].append((title, url))

    # Write summary file
    out_ts = datetime.now().strftime("%Y%m%d-%H%M")
    out = base / f"{out_ts}-yougile-weekly-summary.md"
    lines: List[str] = []
    lines.append("---")
    lines.append(f"created: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("type: report")
    lines.append("sphere: operations")
    lines.append("topic: yougile-weekly-summary")
    lines.append("author: Yougile")
    lines.append("version: 0.1.0")
    lines.append("tags: [yougile, summary, weekly]")
    lines.append("---\n")

    lines.append("# Weekly Activity (last 7 days)\n")
    total_users = len(per_user)
    total_touched = sum(len(v["touched"]) for v in per_user.values())
    total_completed = sum(len(v["completed"]) for v in per_user.values())
    lines.append(f"- Users active: {total_users}")
    lines.append(f"- Tasks touched: {total_touched}")
    lines.append(f"- Tasks completed: {total_completed}\n")

    for user, buckets in sorted(per_user.items()):
        lines.append(f"## {user}")
        lines.append(f"- Touched: {len(buckets['touched'])}")
        lines.append(f"- Completed: {len(buckets['completed'])}\n")
        if buckets["completed"]:
            lines.append("### Completed")
            for title, url in buckets["completed"][:50]:
                lines.append(f"- [x] {title} — {url}")
            lines.append("")
        if buckets["touched"]:
            lines.append("### Touched")
            for title, url in buckets["touched"][:100]:
                lines.append(f"- [ ] {title} — {url}")
            lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Summary written to {out}")


if __name__ == "__main__":
    main()


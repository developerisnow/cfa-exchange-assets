#!/usr/bin/env python3
"""
Fetch Yougile user events (list-limited) using web endpoint (HAR-based).
Requires env:
  YOUGILE_EVENTS_ENDPOINT=https://an8-acc3.yougile.com/data/user-events/list-limited
  YOUGILE_WEB_KEY=<key from HAR>
  YOUGILE_COMPANY_ID=<company UUID>
Usage:
  python yougile-events-fetch.py --user-id <uuid> --count 100 --out events.csv
"""
from __future__ import annotations
import argparse, os, json, csv
from pathlib import Path
import httpx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--user-id', required=True)
    ap.add_argument('--count', type=int, default=100)
    ap.add_argument('--out', default='events.csv')
    args = ap.parse_args()

    endpoint = os.environ.get('YOUGILE_EVENTS_ENDPOINT','https://an8-acc3.yougile.com/data/user-events/list-limited')
    key = os.environ.get('YOUGILE_WEB_KEY')
    company = os.environ.get('YOUGILE_COMPANY_ID')
    if not key or not company:
        raise SystemExit('Set YOUGILE_WEB_KEY and YOUGILE_COMPANY_ID')

    payload = {
        "userId": args.user_id,
        "key": key,
        "companyId": company,
        "count": args.count,
        "filters": {"createdBy": [{"user": args.user_id}], "action": ["add","delete","done"], "createdAt": None},
        "v": 8,
        "appVersion": "40.33.4",
        "clientType": "web",
    }

    with httpx.Client(timeout=30) as client:
        r = client.post(endpoint, json=payload)
        r.raise_for_status()
        data = r.json()

    events = data.get('events', {}) if isinstance(data, dict) else {}
    rows = []
    for k, ev in events.items():
        rows.append({
            'ts_key': k,
            'type': ev.get('type'),
            'user': ev.get('user'),
            'obj': ev.get('obj')
        })

    out = Path(args.out)
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['ts_key','type','user','obj'])
        w.writeheader(); w.writerows(rows)
    print(f'Events written: {out} ({len(rows)})')


if __name__ == '__main__':
    main()


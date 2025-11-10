#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def exists(rel):
    p = ROOT / rel
    return p.exists()

def check_communication(path):
    ok = True
    obj = json.load(open(path))
    for item in obj.get('logs', []):
        rel = Path(item.get('path', '').lstrip('./'))
        if rel and not exists(rel):
            print(f"MISSING communication: {rel}")
            ok = False
    return ok

def check_docs(path):
    ok = True
    obj = json.load(open(path))
    for item in obj.get('documents', []):
        rel = Path(item.get('path', '').lstrip('./'))
        if rel and not exists(rel):
            print(f"MISSING doc: {rel}")
            ok = False
    return ok

def check_repositories(path):
    ok = True
    obj = json.load(open(path))
    for repo in obj.get('repositories', []):
        rel = Path(repo.get('path', '').lstrip('./'))
        if rel and not exists(rel):
            print(f"MISSING repo path: {rel}")
            ok = False
    return ok

def check_repo_structure(path):
    ok = True
    obj = json.load(open(path))
    for rel in (obj.get('structure') or {}).keys():
        relp = Path(str(rel).rstrip('/') )
        if relp and not exists(relp):
            print(f"MISSING structure path: {relp}")
            ok = False
    return ok

def main():
    ok = True
    mdir = ROOT / 'manifests'
    mapping = {
        'communication.manifest.json': check_communication,
        'docs.manifest.json': check_docs,
        'repositories.manifest.json': check_repositories,
        'repo-structure.manifest.json': check_repo_structure,
    }
    for name, fn in mapping.items():
        path = mdir / name
        if path.exists():
            ok = fn(path) and ok
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()


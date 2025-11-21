#!/usr/bin/env python3
"""
Git changes reporter with category grouping (front, dotnet, contracts, docs, architecture guards).
- Reads category config from YAML (git-report-config.yaml) + presets (git-report-presets.yaml).
- Accepts date range, folder filters, categories or presets.
- Emits per-category Markdown reports under output dir (git-<timestamp>/{architecture|categories}/...).
"""
import argparse
import datetime as dt
import fnmatch
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import yaml
except ImportError as exc:
    sys.stderr.write("PyYAML is required: pip install pyyaml\n")
    raise exc

Timestamp = dt.datetime.now().strftime('%Y%m%d-%H%M')


def run_git(repo: Path, args: List[str]) -> str:
    cmd = ['git', '-C', str(repo)] + args
    out = subprocess.check_output(cmd, text=True)
    return out.strip()


def resolve_repo_path(args_repo: str, config_repo: str, script_dir: Path) -> Path:
    if args_repo:
        return Path(args_repo).resolve()
    if config_repo:
        return (script_dir / config_repo).resolve()
    return script_dir.resolve()


def resolve_categories(raw: str, preset: str, config: Dict, presets: Dict) -> List[str]:
    config_cats = list(config['categories'].keys())

    def defaults():
        return [name for name, meta in config['categories'].items() if meta.get('include_by_default')]

    def parse_list(items: List[str]) -> List[str]:
        if items == ['all']:
            return config_cats
        for item in items:
            if item not in config_cats and item != 'all':
                raise ValueError(f"Unknown category '{item}'. Known: {', '.join(config_cats)}")
        return items

    if raw:
        requested = [item.strip() for item in raw.split(',') if item.strip()]
        return parse_list(requested)

    if preset:
        if preset not in presets:
            raise ValueError(f"Unknown preset '{preset}'. Known: {', '.join(presets.keys())}")
        preset_items = presets[preset] or []
        # allow presets to reference "all"
        items = preset_items if isinstance(preset_items, list) else []
        return parse_list(items)

    return defaults()


def get_commit_before(repo: Path, date_str: str) -> str:
    candidate = run_git(repo, ['rev-list', '-1', f'--before={date_str} 00:00:00', 'HEAD'])
    if candidate:
        return candidate
    # fallback to first commit
    first = run_git(repo, ['rev-list', '--max-parents=0', 'HEAD']).splitlines()[0]
    return first


def get_commit_until(repo: Path, date_str: str) -> str:
    candidate = run_git(repo, ['rev-list', '-1', f'--before={date_str} 23:59:59', 'HEAD'])
    if candidate:
        return candidate
    return run_git(repo, ['rev-parse', 'HEAD'])


def collect_changes(repo: Path, base: str, head: str) -> List[Tuple[str, str]]:
    """Return list of (status, path) tuples."""
    raw = run_git(repo, ['diff', '--name-status', f'{base}..{head}'])
    changes = []
    for line in raw.splitlines():
        parts = line.split('\t')
        if not parts:
            continue
        status = parts[0]
        path = parts[-1]  # rename uses last field as new path
        changes.append((status, path))
    return changes


def match_any_glob(path: str, patterns: List[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def write_report(out_dir: Path, bucket: str, category: str, files: List[Tuple[str, str]], commit_log: str,
                 since: str, until: str) -> None:
    target_dir = out_dir / bucket
    target_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{Timestamp}-{category}-git-changes.md"
    fpath = target_dir / fname
    created = dt.datetime.now().strftime('%Y-%m-%d %H:%M')
    frontmatter = f"""---\ncreated: {created}\nupdated: {created}\ntype: analysis\nsphere: [devops]\ntopic: [git, changes, {category}]\nauthor: alex-a (scripted by co-76ca)\nagentID: co-76ca\npartAgentID: [co-76ca]\nversion: 0.1.0\ntags: [git-report, {category}]\n---\n\n"""
    body = []
    body.append(f"# Git changes — {category}\n")
    body.append(f"Диапазон: {since} .. {until}\n")
    body.append("## Files\n")
    if files:
        for status, path in files:
            body.append(f"- {status} {path}\n")
    else:
        body.append("- (нет файлов)\n")
    body.append("\n## Commits (oneline)\n")
    body.append("```")
    body.append(commit_log or "(нет коммитов)")
    body.append("```")
    with open(fpath, 'w', encoding='utf-8') as fh:
        fh.write(frontmatter)
        fh.write("\n".join(body))


def main():
    script_dir = Path(__file__).resolve().parent
    default_config = script_dir / 'git-report-config.yaml'
    default_presets = script_dir / 'git-report-presets.yaml'

    parser = argparse.ArgumentParser(description='Generate git change reports per category.')
    parser.add_argument('--since', required=True, help='Start date YYYY-MM-DD')
    parser.add_argument('--until', default=dt.date.today().isoformat(), help='End date YYYY-MM-DD (default: today)')
    parser.add_argument('--categories', help='Comma list of categories from config or "all"')
    parser.add_argument('--preset', help='Preset name from presets config (fallback if --categories not set)')
    parser.add_argument('--folders', help='Comma list of top-level folders to include (apps,services,packages,tests,...)')
    parser.add_argument('--repo', help='Path to git repo (default from config)')
    parser.add_argument('--config', default=str(default_config), help='Path to YAML config')
    parser.add_argument('--presets-config', default=str(default_presets), help='Path to presets YAML')
    parser.add_argument('--architecture-config', help='Path to architecture guardians YAML (overrides config.defaults.architecture_guardians)')
    parser.add_argument('--output-dir', help='Base dir for reports (default: config defaults.output_base or script directory)')
    parser.add_argument('--include-uncategorized', action='store_true', help='Also write uncategorized bucket')
    parser.add_argument('--fail-on-uncategorized', action='store_true', help='Exit non-zero if uncategorized present')
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        sys.stderr.write(f"Config not found: {config_path}\n")
        sys.exit(1)
    with open(config_path, 'r', encoding='utf-8') as fh:
        config = yaml.safe_load(fh)

    presets: Dict[str, List[str]] = {}
    presets_path = Path(args.presets_config)
    if presets_path.exists():
        with open(presets_path, 'r', encoding='utf-8') as fh:
            presets_yaml = yaml.safe_load(fh) or {}
        presets = presets_yaml.get('presets', {})

    repo_path = resolve_repo_path(args.repo, config.get('defaults', {}).get('repo_root'), script_dir)
    if not (repo_path / '.git').exists():
        sys.stderr.write(f"Not a git repo: {repo_path}\n")
        sys.exit(1)

    arch_cfg_path = args.architecture_config or config.get('defaults', {}).get('architecture_guardians')
    arch_patterns = {}
    if arch_cfg_path:
        arch_file = (Path(arch_cfg_path) if Path(arch_cfg_path).is_absolute() else (script_dir / arch_cfg_path)).resolve()
        if arch_file.exists():
            with open(arch_file, 'r', encoding='utf-8') as fh:
                arch_yaml = yaml.safe_load(fh) or {}
            arch_patterns = {
                'architecture-trunk': arch_yaml.get('trunk', []),
                'architecture-branches': arch_yaml.get('branches', []),
                'architecture-leaves': arch_yaml.get('leaves', []),
            }
        else:
            sys.stderr.write(f"Architecture config not found: {arch_file}\n")

    selected_cats = resolve_categories(args.categories, args.preset, config, presets)
    patterns = {name: meta.get('globs', []) for name, meta in config['categories'].items()}
    for key, globs in arch_patterns.items():
        if globs:
            patterns[key] = globs

    folders = set()
    if args.folders:
        folders = {item.strip() for item in args.folders.split(',') if item.strip()}

    since = args.since
    until = args.until
    base_commit = get_commit_before(repo_path, since)
    head_commit = get_commit_until(repo_path, until)

    changes = collect_changes(repo_path, base_commit, head_commit)
    if folders:
        changes = [(st, path) for st, path in changes if path.split('/')[0] in folders]

    buckets: Dict[str, List[Tuple[str, str]]] = {name: [] for name in selected_cats}
    uncategorized: List[Tuple[str, str]] = []

    for status, path in changes:
        matched = False
        for cat in selected_cats:
            if patterns.get(cat) and match_any_glob(path, patterns[cat]):
                buckets[cat].append((status, path))
                matched = True
        if not matched:
            uncategorized.append((status, path))

    commit_log = run_git(repo_path, ['log', '--since', since, '--until', until, '--oneline'])

    base_out = Path(args.output_dir).resolve() if args.output_dir else None
    if not base_out:
        cfg_out = config.get('defaults', {}).get('output_base')
        base_out = (script_dir / cfg_out).resolve() if cfg_out else script_dir

    out_dir = base_out / f"git-{Timestamp}"
    for cat in selected_cats:
        bucket = 'architecture' if cat.startswith('architecture-') else 'categories'
        write_report(out_dir, bucket, cat, buckets.get(cat, []), commit_log, since, until)
    if args.include_uncategorized:
        write_report(out_dir, 'categories', 'uncategorized', uncategorized, commit_log, since, until)

    print(f"Reports written to {out_dir} for categories: {', '.join(selected_cats)}")
    if uncategorized:
        msg = f"Uncategorized files present: {len(uncategorized)}"
        if args.include_uncategorized:
            print(msg + " (captured in uncategorized bucket)")
        else:
            print(msg + " (rerun with --include-uncategorized to capture)")
        if args.fail_on_uncategorized:
            sys.exit(1)


if __name__ == '__main__':
    main()

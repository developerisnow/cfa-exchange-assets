# Workflow
1. Prompt [[oracle.prompt]]
2. Src/Docs Context. aggregation .txt snapshots (code2promp,repomix)
3. Git Diff. aggregation for eval by Oracle `git-changes-reporter.py`
4. Automation. mcp oracle_gpt5
5. 
# Git

## Analyse 

### Script main
1. `python3 scripts/git-changes-reporter.py --since 2025-11-17 --until 2025-11-23 --preset default --include-uncategorized`
   1. more details extract from `repositories/customer-gitlab/ois-cfa/memory-bank/snapshots-aggregated-context-duplicates/tmux-sessions-symlink/tmux/eywa1/p-cfa/eywa1-p-cfa-w14.p1-20251123-1242.session.txt`

#### Help
```bash
prj_Cifra-rwa-exachange-assets (main) ❯ python3 scripts/git-changes-reporter.py --hel
p
usage: git-changes-reporter.py [-h] --since SINCE [--until UNTIL]
                               [--categories CATEGORIES] [--preset PRESET]
                               [--folders FOLDERS] [--repo REPO] [--config CONFIG]
                               [--presets-config PRESETS_CONFIG]
                               [--architecture-config ARCHITECTURE_CONFIG]
                               [--output-dir OUTPUT_DIR] [--include-uncategorized]
                               [--fail-on-uncategorized]

Generate git change reports per category.

options:
  -h, --help            show this help message and exit
  --since SINCE         Start date YYYY-MM-DD
  --until UNTIL         End date YYYY-MM-DD (default: today)
  --categories CATEGORIES
                        Comma list of categories from config or "all"
  --preset PRESET       Preset name from presets config (fallback if --categories
                        not set)
  --folders FOLDERS     Comma list of top-level folders to include
                        (apps,services,packages,tests,...)
  --repo REPO           Path to git repo (default from config)
  --config CONFIG       Path to YAML config
  --presets-config PRESETS_CONFIG
                        Path to presets YAML
  --architecture-config ARCHITECTURE_CONFIG
                        Path to architecture guardians YAML (overrides
                        config.defaults.architecture_guardians)
  --output-dir OUTPUT_DIR
                        Base dir for reports (default: config defaults.output_base
                        or script directory)
  --include-uncategorized
                        Also write uncategorized bucket
  --fail-on-uncategorized
                        Exit non-zero if uncategorized present
prj_Cifra-rwa-exachange-assets (main) ❯   
```

### Old Analyse git
```bash
prj_Cifra-rwa-exachange-assets (main) ❯ analysegit --help                   12:39:12
usage: git-files-list-commits-analyzer.py [-h] [--branches BRANCHES]
                                          [--lastcommits LASTCOMMITS]
                                          [--typesexclude TYPESEXCLUDE]
                                          [--typeschanges TYPESCHANGES]
                                          [--foldersexclude FOLDERSEXCLUDE]
                                          [--exclude-hidden]
                                          [commits ...]

Analyze git repository changes between commits.

positional arguments:
  commits               Two commit hashes to compare

options:
  -h, --help            show this help message and exit
  --branches BRANCHES   Compare two branches (format: branch1,branch2 - use comma,
                        NO spaces!)
  --lastcommits LASTCOMMITS
                        Analyze last N commits from HEAD
  --typesexclude TYPESEXCLUDE
                        Comma-separated file extensions to exclude (e.g.,
                        "md,csv,log,json,yaml")
  --typeschanges TYPESCHANGES
                        Git diff filter types: A=Added, M=Modified, R=Renamed,
                        C=Copied, D=Deleted (default: AMRCD)
  --foldersexclude FOLDERSEXCLUDE
                        Comma-separated folders to exclude (e.g.,
                        "logs,test,node_modules")
  --exclude-hidden      Exclude hidden files (starting with ".")

EXAMPLES:

  # Compare two specific commits:
  git-files-list-commits-analyzer.py abc1234 def5678

  # Compare two branches (note: use comma, no spaces!):
  git-files-list-commits-analyzer.py --branches main,develop
  git-files-list-commits-analyzer.py --branches feature/auth,main

  # Analyze last 5 commits:
  git-files-list-commits-analyzer.py --lastcommits 5

  # With filtering (exclude md/json files, hidden files, test folders):
  git-files-list-commits-analyzer.py --lastcommits 3 --typesexclude="md,json" --exclude-hidden --foldersexclude="test,logs"

  # Only show specific change types (A=added, M=modified):
  git-files-list-commits-analyzer.py --lastcommits 2 --typeschanges="AM"

YOUR ALIASES:
  analysegit abc1234 def5678                     # Basic comparison
  analysegit-last 5                             # Last 5 commits  
  analysegit-branches main,develop               # Compare branches
  analysegit-filtered --lastcommits 3           # With smart filtering

NOTES:
  - For --branches use format: branch1,branch2 (comma, no spaces!)
  - Script saves report to docs/meta/ and copies filenames to clipboard
  - Change types: A=Added, M=Modified, R=Renamed, C=Copied, D=Deleted
        

🔥 ОШИБКА В АРГУМЕНТАХ! Вот как правильно использовать:

usage: git-files-list-commits-analyzer.py [-h] [--branches BRANCHES]
                                          [--lastcommits LASTCOMMITS]
                                          [--typesexclude TYPESEXCLUDE]
                                          [--typeschanges TYPESCHANGES]
                                          [--foldersexclude FOLDERSEXCLUDE]
                                          [--exclude-hidden]
                                          [commits ...]

Analyze git repository changes between commits.

positional arguments:
  commits               Two commit hashes to compare

options:
  -h, --help            show this help message and exit
  --branches BRANCHES   Compare two branches (format: branch1,branch2 - use comma,
                        NO spaces!)
  --lastcommits LASTCOMMITS
                        Analyze last N commits from HEAD
  --typesexclude TYPESEXCLUDE
                        Comma-separated file extensions to exclude (e.g.,
                        "md,csv,log,json,yaml")
  --typeschanges TYPESCHANGES
                        Git diff filter types: A=Added, M=Modified, R=Renamed,
                        C=Copied, D=Deleted (default: AMRCD)
  --foldersexclude FOLDERSEXCLUDE
                        Comma-separated folders to exclude (e.g.,
                        "logs,test,node_modules")
  --exclude-hidden      Exclude hidden files (starting with ".")

EXAMPLES:

  # Compare two specific commits:
  git-files-list-commits-analyzer.py abc1234 def5678

  # Compare two branches (note: use comma, no spaces!):
  git-files-list-commits-analyzer.py --branches main,develop
  git-files-list-commits-analyzer.py --branches feature/auth,main

  # Analyze last 5 commits:
  git-files-list-commits-analyzer.py --lastcommits 5

  # With filtering (exclude md/json files, hidden files, test folders):
  git-files-list-commits-analyzer.py --lastcommits 3 --typesexclude="md,json" --exclude-hidden --foldersexclude="test,logs"

  # Only show specific change types (A=added, M=modified):
  git-files-list-commits-analyzer.py --lastcommits 2 --typeschanges="AM"

YOUR ALIASES:
  analysegit abc1234 def5678                     # Basic comparison
  analysegit-last 5                             # Last 5 commits  
  analysegit-branches main,develop               # Compare branches
  analysegit-filtered --lastcommits 3           # With smart filtering

NOTES:
  - For --branches use format: branch1,branch2 (comma, no spaces!)
  - Script saves report to docs/meta/ and copies filenames to clipboard
```
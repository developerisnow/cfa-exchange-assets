# Prompt 1
какие файлы можно заигнорить чтобы сделать по типу code2promp,repomix слепок репозитория и дальше с агентами, неущерб качеству
# Output 1
### TL;DR

* Игнорируй **билды/кэши/вендор** + **медиа/шрифты/i18n** + **сгенерённые доки**; оставляй **код, конфиги, миграции, README, API-спеки**.
* Для «ультра-лайта» добавь игнор **tests/storybook** — если не нужны агентам.
* Ниже — готовый блок `.llmignore` (подходит и как доп. `.gitignore`/`.repomixignore`) и примеры именно из твоего репо. 

---

### Steps

1. Создай рядом с корнем снапшота файл `.llmignore` (или допиши в `.gitignore`).
2. Запусти свой `code2prompt/repomix` поверх него.
3. Если токены всё ещё жирные — включи «ультра-лайт» блок (tests/storybook) и/или порог по размеру.
4. При желании исключи все файлы >512 KB на лету:

```bash
# список крупных, чтобы понять что ещё вычистить
find . -type f -size +512k -not -path "*/node_modules/*" -print
```

---

### Рекомендованный ignore-набор (с комментариями)

```gitignore
#############################
# LLM snapshot ignore (safe)
#############################

# 1) Билды, кэши, артефакты
**/dist/**            # сборки
**/build/**           # в т.ч. apidoc/public/build
**/.next/** **/.nuxt/** **/.vite/** **/.turbo/** **/.cache/**
**/coverage/** **/.sass-cache/** **/tmp/** **/logs/**
**/storybook-static/** **/.storybook/**

# 2) Вендор/зависимости
**/node_modules/** 
**/vendor/**          # PHP/Symfony
**/.venv/** **/.gradle/**

# 3) Тяжёлые статики (не нужны для понимания логики)
**/*.png **/*.jpg **/*.jpeg **/*.gif **/*.webp **/*.ico **/*.svg
**/*.mp3 **/*.mp4 **/*.wav **/*.ogg **/*.oga
**/*.eot **/*.ttf **/*.woff **/*.woff2
**/assets/images/** **/assets/img/** **/assets/static/**
**/tradingview/**     # либные ассеты/статика
**/fonts/** **/sfuidisplay/**

# 4) Локализации/большие JSON-таблицы
**/locales/** **/localization/translations/** **/i18n/**

# 5) Сгенерённые доки/сайты документации
**/docs/**            # ниже вернём .md через negation
**/public/build/** **/public/vendor/**

# 6) Секреты/бинарники
**/.env*              # оставь .env.example без маски
**/*.kdbx **/*.pfx **/*.crt **/*.key **/*.pem
**/*.zip **/*.7z **/*.tar **/*.gz **/*.tgz **/*.bz2 **/*.dmg **/*.exe

# 7) IDE/система/логи
**/.idea/** **/.vscode/** **/.history/**
.DS_Store Thumbs.db **/*.log

# 8) Верни важные тексты/код/конфиги (для качества)
!**/*.md
!**/*.txt
!**/*.js  !**/*.jsx  !**/*.ts  !**/*.tsx
!**/*.php !**/*.sql  !**/*.yml !**/*.yaml !**/*.json
!**/*.sh  !**/Dockerfile
!**/openapi*.yml     # API-спеки, если есть
!**/apidoc.json      # исходный spec, а не build
```

#### (Опция) Ультра-лайт, если критичен объём:

```gitignore
# Тесты и сторибуки (отключи, если они нужны агентам как спеки поведения)
**/tests/** **/__tests__/**
**/*.spec.* **/*.test.*
**/stories/** **/*.story.* **/*.stories.*
```

---

### Что именно из твоего репо «безболезненно» выкинуть (и почему)

| Категория            | Игнорировать                             | Почему                                 | Пример путей из твоего дерева                                                          |
| -------------------- | ---------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------- |
| Билды/кэши           | `dist/`, `build/`, `.next/`, `coverage/` | Артефакты сборки, дублируют исходники  | `api_platform_back_crypto-master/build/**`, `public/build/**`                          |
| Вендор               | `node_modules/`, `vendor/`               | Третьи стороны, не несут бизнес-логики | множество `package.json`-проектов; Symfony `vendor/` (если есть)                       |
| Медиа/шрифты         | `assets/images/`, `fonts/`, `*.woff2`    | Тяжёлые, не нужны для анализа кода     | `velvet-exchange-frontend-master/src/assets/fonts/sfuidisplay/**`, `assets/images/**`  |
| Библиотечная статика | `tradingview/`, `public/vendor/`         | Большие либные ассеты                  | `.../tradingview/static/**`, `.../public/vendor/**`                                    |
| Локализации          | `locales/`, `localization/translations/` | Много ключей, шумят, логику не меняют  | `translations/*.json`, `localization/translations/**`                                  |
| Секреты/бинарники    | `.env*`, `*.kdbx`, `*.pfx`               | Риск/балласт, агентам не нужны         | `velvet-keepass-*/**.kdbx`, `.../sert/*.pfx`                                           |

> Что оставить: директории `src/`, `app/`, `core/`, `controllers/`, `models/`, `routes/`, `services/`, `Entity/`, `Repository/`, `migrations/|DoctrineMigrations/`, конфиги (`config/*.yml|json`, Ansible `playbooks/`, `roles/`), `Dockerfile`, `README.md`, API-спеки (`openapi*.yml`/`apidoc.json`). 

---

### Next actions

* Вкинь блок выше в `.llmignore` (и/или в `.gitignore`) и сделай пробный снапшот.
* Если объём ещё велик — включи «ультра-лайт» и добавь исключение по размеру (`find` выше).
* Отдельно проверь, не нужны ли агентам **tests** как документация поведения; если да — верни их адресно (например, только `*ControllerTest*`).

# Prompt 2 
давай так - дай инструкции для codex-cli bash агента чтобы он проверил установлены ли уже у меня code2promp, repomix, и yek пусть поставит(его кажется нет)

потом с твоими инструкциями прямо подкопипаст пусть для этого проекта все сделает и в подпапку "./reposcan" все положет

Адес проекта на моем macos "/Users/user/__Repositories/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/velvet"

# Output 2
**TL;DR**

* Проверяем `repomix`, `code2prompt`, `yek`; ставим отсутствующие (на macOS через Homebrew / rustup + cargo).
* Генерим три слепка в `./reposcan`: `repomix.md` (markdown), `code2prompt.md`, `yek.txt` + `versions.txt`.
* В корне создаём `.repomixignore` (safe-defaults), чтобы LLM-контекст без мусора. (Основано на твоём сравнительном ресёрче repomix/code2prompt/yek.) 

---

## Steps (копипаст для codex-cli bash агента)

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

PROJ="/Users/user/__Repositories/prj_Cifra-rwa-exachange-assets/repositories/customer-gitlab/ois-cfa"
OUT="$PROJ/reposcan"
TS="$(date -u +"%Y-%m-%dT%H-%M-%SZ")"

[[ -d "$PROJ" ]] || { echo "❌ Project not found: $PROJ" >&2; exit 1; }
mkdir -p "$OUT"

have() { command -v "$1" >/dev/null 2>&1; }

echo "▶︎ Checking tools…"

# --- repomix ---
if ! have repomix; then
  if have brew; then
    brew list --formula repomix >/dev/null 2>&1 || brew install repomix   # brew install repomix
  elif have npm; then
    npm i -g repomix   # fallback
  else
    echo "❌ Need Homebrew or Node/npm for repomix"; exit 1
  fi
fi

# --- code2prompt ---
if ! have code2prompt; then
  if have brew; then
    brew list --formula code2prompt >/dev/null 2>&1 || brew install code2prompt  # brew install code2prompt
  else
    if ! have cargo; then
      curl -sSf https://sh.rustup.rs | sh -s -- -y
      # shellcheck source=/dev/null
      source "$HOME/.cargo/env"
    fi
    cargo install code2prompt
  fi
fi

# --- yek ---
if ! have yek; then
  if ! have cargo; then
    curl -sSf https://sh.rustup.rs | sh -s -- -y
    # shellcheck source=/dev/null
    source "$HOME/.cargo/env"
  fi
  cargo install yek || { curl -fsSL https://bodo.run/yek.sh | bash; hash -r; }
fi

# --- prepare ignore for repomix (backup if exists) ---
cd "$PROJ"
if [[ -f .repomixignore ]]; then cp .repomixignore "$OUT/.repomixignore.backup.$TS"; fi
cat > .repomixignore <<'EOF'
# Binaries & media
**/*.{png,jpg,jpeg,gif,webp,ico,psd,ai,sketch,mp4,mp3,avi,mov,zip,tgz,tar,7z}
**/*.{pdf,drawio}
# Builds & caches
**/node_modules/** **/.next/** **/.turbo/** **/.vercel/** **/dist/** **/build/** **/.cache/** **/coverage/** **/.nyc_output/** **/*.map
# Locks
**/package-lock.json **/yarn.lock **/pnpm-lock.yaml
# IDE/OS/misc
.vscode/** .idea/** *.code-workspace .DS_Store Thumbs.db **/*.log **/*.tmp **/*.bak
# Secrets
**/.env* **/*.{pem,key,crt,pfx}
# .NET
**/bin/** **/obj/** **/.vs/** **/*.csproj.user
# Test snapshots
**/__snapshots__/** **/*.snap
# Helm (optional noise)
ops/infra/helm/**/templates/**
!ops/infra/helm/**/templates/deployment.yaml
!ops/infra/helm/**/templates/service.yaml
!ops/infra/helm/**/templates/ingress.yaml
# Keep (signal)
!.gitignore !README.md !Makefile !docker-compose.yml
!**/src/**
!**/*.{cs,go,ts,tsx,js,jsx,py,rs,md,yml,yaml,toml,json}
EOF

# --- generate snapshots ---
echo "▶︎ Generating snapshots into $OUT …"
mkdir -p "$OUT"

# Repomix (markdown + JSON for programmatic use)
repomix --style markdown -o "$OUT/repomix.md" --token-count-tree 100 --top-files-len 20
repomix --style json     -o "$OUT/repomix.json" || true

# Code2Prompt (exclude common junk on top of .gitignore)
code2prompt "$PROJ" \
  --output="$OUT/code2prompt.md" \
  --exclude="*.png,*.jpg,*.jpeg,*.gif,*.webp,*.ico,*.pdf,*.zip,*.tar,*.tar.gz,*.map,*.lock,*.log,node_modules/**,dist/**,build/**,.next/**,.cache/**,coverage/**,bin/**,obj/**"

# Yek (fast, with tree header; write exactly to reposcan)
yek --output-dir "$OUT" --output-name "yek.txt" -t "$PROJ"

# Versions & quick tree
{
  echo "# Versions @ $TS"
  echo "repomix:     $(repomix --version 2>&1 || true)"
  echo "code2prompt: $(code2prompt --version 2>&1 || true)"
  echo "yek:         $(yek --version 2>&1 || true)"
  echo "node:        $(node -v 2>&1 || true)"
  echo "npm:         $(npm -v 2>&1 || true)"
  echo "cargo:       $(cargo --version 2>&1 || true)"
  echo "brew:        $(brew --version 2>/dev/null | head -n1 || true)"
} | tee "$OUT/versions.txt" >/dev/null

# Optional tree (if `tree` exists)
if command -v tree >/dev/null 2>&1; then
  (cd "$PROJ" && tree -a -I 'node_modules|.git|dist|build|.next|.turbo|.vercel' > "$OUT/source-tree.txt") || true
fi

echo "✅ Done. Outputs:"
ls -lh "$OUT"
```

**Что делает скрипт:**

* Устанавливает/проверяет `repomix` (через Homebrew или npm), `code2prompt` (brew/cargo), `yek` (cargo или официальный installer).
* Создаёт `.repomixignore` (safe-defaults).
* Генерирует: `repomix.md`, `repomix.json`, `code2prompt.md`, `yek.txt`, `versions.txt` (и `source-tree.txt`, если есть `tree`).
* Всё складывает в `"$PROJ/reposcan"`.

---

## Table (результат и где смотреть)

| Генератор   | Команда в скрипте               | Формат выхода     | Файл(ы)                      | Примечание                                   |
| ----------- | ------------------------------- | ----------------- | ---------------------------- | -------------------------------------------- |
| repomix     | `repomix --style markdown -o …` | Markdown (+ JSON) | `repomix.md`, `repomix.json` | Умеет token-tree/summary.                    |
| code2prompt | `code2prompt … --output=…`      | Markdown          | `code2prompt.md`             | Поддерживает exclude и шаблоны/токены.       |
| yek         | `yek --output-dir … -t`         | Plain text        | `yek.txt`                    | Очень быстрый, есть `--tokens`/`--max-size`. |
| versions    | —                               | Text              | `versions.txt`               | Фиксируем версии инструментов.               |
| дерево      | `tree … > source-tree.txt`      | Text              | `source-tree.txt`            | Опционально (если установлен `tree`).        |

---

## Next actions

1. Запусти блок выше в codex-cli (или просто в Terminal).
2. Проверь `./reposcan/repomix.md` — это основной «склеенный» контекст для LLM.
3. Если репо очень большое — для быстрых итераций корми `yek.txt`; для кастомных шаблонов — `code2prompt.md`. 
4. Скажи, если нужно: добавить автозаливку в S3/GDrive, сжатие (`repomix --compress`) или вариацию `.repomixignore` под конкретный модуль.

**Справка по установке (официальные источники):** `brew install repomix` (Homebrew), `npx repomix@latest`; `brew install code2prompt` или `cargo install code2prompt`; `cargo install yek` (или `curl -fsSL https://bodo.run/yek.sh | bash`); rust/cargo через `rustup`.

**Примечание:** я использовал выводы твоего сравнения repomix/code2prompt/yek для баланса скорости/качества слепков. 

Предыстория
Я на основе всего контекста выделил 2 comprehensive промпта
00) Ledger-RWA-platforms-worldwide-and-RU-CFA
01)  CFA-platforms-RU-2024-2025 

Выбрал лучшие известные мне инструменты на Deep Research, у меня везде PRO подписки, чтобы выжать максимум результата

- Openai Pro $200 Gpt 5 Pro, High
- Anthropic $200 Opus 4.1, Sonnet 4.5
- Perplexity $20 Default
- Google Gemini $20 Gemini 2.5p
- Parallel $credits

Запустил в каждом по 1-2 раза(что примерно 2*5*2~20 reports но где-то 1 где-то отчет выдал ошибку )

Далее я проделал большую ручную работу более часа копировать, экспортировать все это в markdown в две папки с подпапками иногда, например результаты perplexity по нескольким файлам

Именование я использовал инкрементацию в минутах чтобы не путаться как бы будет uid `yyyymmdd-hhmm`  

Цель
1) Естественно вынести максимальную пользу и ценность из deepresearch, подтвердить все гипотезы и выбрать под мои цели наилучшее решение для запуска.
Весь предыдущий контекст говорит об этом. В первую очередь это.
2) Возможно вынести на будущее ключевые знания, инсайды, статистику. Сделать реестры доменных сущнностей, вариантов внедрения, стастики по странам, источники данных и т.д. это отдельная полномасштабная аналитическая работа
3) Также, не является ли overengineering моя задача делать эти рисерчи в 5 инструментах и по 2 прогона? Тут много ручной работы, суммарно часа на 2 промпты и запуски, а потом 1 копирования. Не говоря уже о пост-анализ прочитать 20 документов по 30 страниц что 600 страниц даже по диагонале будет большой перегруз и сложно человеку. Там к тому же будут дубли, где-то противоречия, неточности - и безусловно ценная и полезаня информация, инсайды, файкты конкретика с отсылками на источники, поэтому нужно выстроить pipelines
- analysis pipeline with extraction insights, facts, и прочим собственно в соответствии с целями (1), и отдельно (2)
- разрешение противоречий, неточностей и дубликатов, с обогащение в один вариант. Как бы слой №2 там уже будут отсылки в моем понимании не на первоисточники а на порядковые uid/name deepresearches
4)  для себя на будущее целесообразно ли делать эту работу? Нужно оценить, придумать метрики для оценки deepresearches, причем у меня есть 2 кейса, CFA-RU-COMPETITORS, RWA-CFA-WORLD и как бы может быть один провайдер(а там еще и модели разные)  сделает лучше один кейс, а другая другой и в целом там же есть элемент рандома - мне нужно с одной стороны сухо и трезво их оценить в таблице и потом понять - надо ли делать так 5 провайдеров и 2 прогона по каждому кейсу или достаточно просто брать 1 провайдер и 1 прогон на будущее и не делать лишней работы так как последующие отчеты сильно не улучшили.

Нужно сейчас подумать как это все организовать наилучшим образом
На выходе я ожидаю 4 документа по каждому пункту, что в них будет описание pipeline и организация для его запуска, промпты - реши наилучшим образом.


```bash
deepresearches (codex/jump-into-project-20251030) ❯  find . -type f -exec sh -c 'echo "$(wc -l < "$1") $(du -h "$1" | cut -f1) $1"' _ {} \; | column -t | sort -rn

8036  944K  ./01-CFA-platforms-RU-2024-2025/20251031-0816-parallel.ai-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.json
1066  24K   ./01-CFA-platforms-RU-2024-2025/2025100830-perplexity.deepresearch/competitors-sources.md
1014  44K   ./00-Ledger-RWA-platforms-worldwide-and-RU-CFA-deepresearches/20251031-0757-son4.5-Ledger-RWA-platforms-worldwide-and-RU-CFA.deepresearch.md
700   44K   ./00-Ledger-RWA-platforms-worldwide-and-RU-CFA-deepresearches/20251031-0759-perplexity-Ledger-RWA-platforms-worldwide-and-RU-CFA.deepresearch.md
605   192K  ./00-Ledger-RWA-platforms-worldwide-and-RU-CFA-deepresearches/20251031-0755-gpt5h-Ledger-RWA-platforms-worldwide-and-RU-CFA.deepresearch.docx.md
524   48K   ./01-CFA-platforms-RU-2024-2025/20251031-0814-opus4.1-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.md
520   120K  ./00-Ledger-RWA-platforms-worldwide-and-RU-CFA-deepresearches/20251031-0758-gem2.5p-Ledger-RWA-platforms-worldwide-and-RU-CFA.deepresearch.md
472   36K   ./01-CFA-platforms-RU-2024-2025/20251031-0815-opus4.1-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.md
402   84K   ./01-CFA-platforms-RU-2024-2025/20251031-0816-gem2.5p-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.md
368   20K   ./01-CFA-platforms-RU-2024-2025/2025100830-perplexity.deepresearch/competitors.md
368   192K  ./00-Ledger-RWA-platforms-worldwide-and-RU-CFA-deepresearches/20251031-0756-gpt5p-Ledger-RWA-platforms-worldwide-and-RU-CFA.deepresearch.docx.md
330   36K   ./01-CFA-platforms-RU-2024-2025/20251031-0816-parallel.ai-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.md
278   36K   ./01-CFA-platforms-RU-2024-2025/20251031-0813-gpt5h-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.docx.md
220   56K   ./01-CFA-platforms-RU-2024-2025/20251031-0811-gpt5p-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.md
217   44K   ./01-CFA-platforms-RU-2024-2025/20251031-0812-gpt5h-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.docx.md
98    8.0K  ./01-CFA-platforms-RU-2024-2025/prompts.md
21    4.0K  ./01-CFA-platforms-RU-2024-2025/2025100830-perplexity.deepresearch/competitors_summary.csv
20    48K   ./01-CFA-platforms-RU-2024-2025/20251031-0811-gpt5p-prompt-1-CFA-platforms-RU-2024-2025.deepresearch.jsonl
20    32K   ./01-CFA-platforms-RU-2024-2025/2025100830-perplexity.deepresearch/competitors.jsonl
0     8.0K  ./.DS_Store
```
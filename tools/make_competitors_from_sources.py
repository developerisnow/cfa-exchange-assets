#!/usr/bin/env python3
import re, json, pathlib, sys

SRC = pathlib.Path('memory-bank/Scrum/20251030-jump-into-project/deepresearches/01-CFA-platforms-RU-2024-2025/2025100830-perplexity.deepresearch/competitors-sources.md')
OUT_JSONL = pathlib.Path('memory-bank/Scrum/20251030-jump-into-project/co-76ca/competitors.jsonl')
OUT_MD = pathlib.Path('memory-bank/Scrum/20251030-jump-into-project/co-76ca/competitors.md')

TARGETS = [
    'Атомайз (Atomyze)',
    'НРД (Национальный расчетный депозитарий)',
    'Сбербанк (Цифровые активы)',
    'Лайтхаус',
]

def parse_sources_block(lines, start_idx):
    evid = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('###') or line.startswith('##') or not line:
            break
        m = re.match(r"- \[(\d{4}-\d{2}-\d{2})\] (https?://\S+)", line)
        if m:
            evid.append({"url": m.group(2), "date": m.group(1)})
        i += 1
    return evid, i

def parse_section(lines, start_idx):
    data = {"status":"unknown","role":[],"dlt":{},"custody":{},"ukep":{},"dvp":{},
            "secondary":{},"apis":{},"hosting":{},"metrics":{},"regulatory":{},"sources":[]}
    i = start_idx
    while i < len(lines):
        line = lines[i].rstrip('\n')
        if line.startswith('## ') and i != start_idx:
            break
        # Simple field captures
        if line.startswith('**Статус:**'):
            data['status'] = line.split('**Статус:**',1)[1].strip().strip()
        if line.startswith('**Роли:**'):
            roles = line.split('**Роли:**',1)[1].strip().strip()
            data['role'] = [r.strip() for r in roles.split(',') if r.strip()]
        if line.strip() == '### DLT/Blockchain':
            # Next lines include **Тип:** and possibly Источники
            j = i+1
            while j < len(lines) and not lines[j].startswith('###') and not lines[j].startswith('##'):
                if lines[j].startswith('**Тип:**'):
                    data.setdefault('dlt',{})['type'] = lines[j].split('**Тип:**',1)[1].strip().lower()
                if lines[j].strip() == '**Источники:**':
                    evid, j2 = parse_sources_block(lines, j+1)
                    data.setdefault('dlt',{}).setdefault('evidence',[]).extend(evid)
                    j = j2-1
                j += 1
            i = j-1
        if line.strip() == '### УКЭП/Криптография':
            j = i+1
            while j < len(lines) and not lines[j].startswith('###') and not lines[j].startswith('##'):
                if lines[j].startswith('**ГОСТ:**'):
                    data.setdefault('ukep',{})['gost'] = 'Да' in lines[j]
                j += 1
            i = j-1
        if line.strip() == '### DvP/Расчеты':
            j = i+1
            while j < len(lines) and not lines[j].startswith('###') and not lines[j].startswith('##'):
                if lines[j].startswith('**Модель:**'):
                    data.setdefault('dvp',{})['model'] = lines[j].split('**Модель:**',1)[1].strip().lower()
                if lines[j].startswith('**Банки:**'):
                    banks = lines[j].split('**Банки:**',1)[1].strip()
                    data.setdefault('dvp',{})['banks'] = [b.strip() for b in banks.split(',') if b.strip() and banks!='-']
                if lines[j].startswith('**ISO 20022:**'):
                    data.setdefault('dvp',{})['iso20022'] = 'Да' in lines[j]
                if lines[j].startswith('**СБП:**'):
                    data.setdefault('dvp',{})['sbp'] = 'Да' in lines[j]
                j += 1
            i = j-1
        if line.strip() == '### Вторичный рынок':
            j = i+1
            sec = {}
            while j < len(lines) and not lines[j].startswith('###') and not lines[j].startswith('##'):
                if lines[j].startswith('**RFQ:**'):
                    sec['rfq'] = 'Да' in lines[j]
                if lines[j].startswith('**Orderbook:**'):
                    sec['orderbook'] = 'Да' in lines[j]
                j += 1
            data['secondary'] = sec
            i = j-1
        if line.strip() == '### API/Документация':
            j = i+1
            apis = {}
            while j < len(lines) and not lines[j].startswith('###') and not lines[j].startswith('##'):
                if lines[j].startswith('**OpenAPI:**'):
                    apis['openapi'] = 'Да' in lines[j]
                if lines[j].startswith('**Документация:**'):
                    doc_url = lines[j].split('**Документация:**',1)[1].strip()
                    apis['docs'] = [doc_url] if doc_url and doc_url!='-' else []
                j += 1
            data['apis'] = apis
            i = j-1
        if line.strip() == '### Регуляторный статус':
            j = i+1
            reg = {}
            while j < len(lines) and not lines[j].startswith('###') and not lines[j].startswith('##'):
                if lines[j].startswith('**Лицензии:**'):
                    val = lines[j].split('**Лицензии:**',1)[1].strip()
                    reg['licenses'] = [s.strip() for s in val.split(',') if s.strip()]
                j += 1
            data['regulatory'] = reg
            i = j-1
        i += 1
    return data, i

def main():
    text = SRC.read_text(encoding='utf-8')
    lines = text.splitlines()
    # Build index of sections
    sections = {}
    for idx,line in enumerate(lines):
        if line.startswith('## '):
            title = line[3:].strip()
            sections[title] = idx
    out_cards = []
    for target in TARGETS:
        # find matching section (exact or startswith)
        key = None
        for t in sections:
            if t == target or t.startswith(target):
                key = t
                break
        if not key:
            continue
        data, _ = parse_section(lines, sections[key])
        card = {
            'name': key,
            **{k:v for k,v in data.items() if v}
        }
        out_cards.append(card)
    # write JSONL
    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open('w', encoding='utf-8') as w:
        for c in out_cards:
            w.write(json.dumps(c, ensure_ascii=False)+"\n")
    # write MD summary
    with OUT_MD.open('w', encoding='utf-8') as w:
        w.write('---\ncreated: 2025-10-31 10:56\nupdated: 2025-10-31 10:56\n')
        w.write('type: research-summary\nsphere: [market, cfa]\n')
        w.write('topic: [competitors]\nauthor: codex\n')
        w.write('agentID: 019a362f-76ca-7272-909e-362716cf233d\npartAgentID: [co-76ca]\nversion: 1.0.0\ntags: [summary, competitors]\n---\n\n')
        w.write('TL;DR\n- Собрано {} карточек (Batch‑1).\n\n'.format(len(out_cards)))
        w.write('| Платформа | DLT | DvP | RFQ | Orderbook | OpenAPI | Licenses |\n')
        w.write('|---|---|---|---|---|---|---|\n')
        for c in out_cards:
            dlt = c.get('dlt',{}).get('type','unknown')
            dvp = c.get('dvp',{}).get('model','unknown')
            rfq = str(c.get('secondary',{}).get('rfq')) if 'secondary' in c else 'unknown'
            ob = str(c.get('secondary',{}).get('orderbook')) if 'secondary' in c else 'unknown'
            openapi = str(c.get('apis',{}).get('openapi')) if 'apis' in c else 'unknown'
            lic = ','.join(c.get('regulatory',{}).get('licenses',[]))
            w.write(f"| {c['name']} | {dlt} | {dvp} | {rfq} | {ob} | {openapi} | {lic} |\n")
    print(f"Wrote {len(out_cards)} cards to {OUT_JSONL} and summary to {OUT_MD}")

if __name__ == '__main__':
    sys.exit(main())


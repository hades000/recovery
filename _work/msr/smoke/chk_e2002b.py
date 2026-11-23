import json
from pathlib import Path
for p in ['_work/msr/gaps/B-P2-01.jsonl','_work/msr/assumptions/B-P2-01.jsonl']:
    print('==',p)
    for line in Path(p).read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        if 'E2002' in o['id']:
            print(o['id'], '|', o.get('legacy_ref',''), '|', o.get('asm', o.get('gap','')))

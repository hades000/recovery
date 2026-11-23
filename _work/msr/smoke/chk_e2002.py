import json
from pathlib import Path
root = Path('.')
def load(p):
    rows={}
    for line in Path(p).read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        rows[o['id']]=o
    return rows
g=load('_work/msr/gaps/B-P2-01.jsonl')
a=load('_work/msr/assumptions/B-P2-01.jsonl')
print('gap rows', len(g), 'asm rows', len(a))
for k in ['RWB-P2-E2002-APP','RWB-P2-E2002-CON','RWB-P2-E2002-OPS']:
    f=json.loads(Path(f'_work/msr/fragments/{k}.json').read_text(encoding='utf-8'))
    print(k, 'gaps', f['gaps'], 'asms', f['assumptions'])
    for gr in f['gap_rows']:
        if gr['id'] not in g: print('  gap missing in register', gr['id'])
        else:
            diff=[x for x in set(list(gr)+list(g[gr['id']])) if gr.get(x)!=g[gr['id']].get(x)]
            if diff: print('  gap diff', gr['id'], diff)
    for ar in f['asm_rows']:
        if ar['id'] not in a: print('  asm missing in register', ar['id'])
        else:
            diff=[x for x in set(list(ar)+list(a[ar['id']])) if ar.get(x)!=a[ar['id']].get(x)]
            if diff: print('  asm diff', ar['id'], diff)

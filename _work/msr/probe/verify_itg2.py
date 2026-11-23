import re, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
base = Path('04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration')
ids = ['RWB-ITG-E1030-ITG','RWB-ITG-E1031-ITG','RWB-ITG-E1032-ITG','RWB-ITG-E1034-ITG','RWB-ITG-E1037-ITG']
for i in ids:
    compact = i.split('-')[2]
    p = [x for x in base.glob('RWB ITG %s ITG*.md' % compact)][0]
    t = p.read_text(encoding='utf-8')
    d = json.loads((Path('_work/msr/fragments')/(i+'.json')).read_text(encoding='utf-8'))
    pats = re.search(r'\| Patterns applied \| (.+?) \|', t).group(1).split(', ')
    sec13 = t[t.index('### 13.'):t.index('### 14.')]
    dp_rows = re.findall(r'^\| (DP-\d\d) \|', sec13, re.M)
    print(i, 'patterns', len(pats), 'dp rows', len(dp_rows), 'all present', [x.replace('DP','DP-') for x in pats] == dp_rows)
    sec16 = t[t.index('### 16.'):t.index('### 17.')]
    tc_rows = re.findall(r'^\| (TC-[A-Z0-9-]+) \|', sec16, re.M)
    print('   tc table', tc_rows == d['tcs'], len(tc_rows), 'frag', len(d['tcs']))
    if tc_rows != d['tcs']:
        print('    table:', tc_rows); print('    frag :', d['tcs'])
    print('   levels:', sorted(set(re.findall(r'\| (Integration|Component|Contract|NFR|End to end|Unit) \|', sec16))))
    print('   reqs cited:', sorted(set(re.findall(r'\bREQ-[A-Z0-9-]+\b', t))))
    print('   assumptions cited:', sorted(set(re.findall(r'\bASM-B-ITG-W1-05-E10\d\d-\d\b', t))))
    print('   gaps cited:', sorted(set(re.findall(r'\bCG-B-ITG-W1-05-E10\d\d-\d\b', t))))
    print('   dp in frag? n/a; ops', len(d['ops_consumed']), 'events', len(d['events_consumed']), 'wf', d['workflows'])

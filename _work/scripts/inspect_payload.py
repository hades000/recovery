import json, io, re, collections

d = json.load(io.open(r'_work\data\hub_payload.json', encoding='utf-8'))
print('docs', len(d['docs']), 'ids', len(d['ids']), 'files', len(d['files']))
print('folders', collections.Counter(x['folder'] for x in d['docs']))
print('--- first docs ---')
for i, doc in enumerate(d['docs'][:8]):
    print(i, doc['folder'][:2], '|', doc['file'], '| secs', len(doc['secs']))
print('--- story docs ---')
for i, doc in enumerate(d['docs']):
    if 'User Stories Epic 1 v8' in doc['file'] or 'ACE Team Stories' in doc['file']:
        print(i, doc['file'], len(doc['secs']))
print('--- ids ---')
for code in ['RWB-E1-001', 'RWB-E1-069', 'RWB-E1-003', 'RWB-ACE-001', 'D-RCV-35', 'DL43',
             'DF-ACE-018', 'BR-P3-001', 'AC-ALT-P7-014-01', 'TC-E1-001-01', 'MSG-P1-003',
             'REQ-RDF-002', 'FEAT-RDF-01']:
    v = d['ids'].get(code)
    print(code, 'MISSING' if not v else (v['k'], v['d'], len(v['u']), v['t'][:130]))
print('--- definition section text for DF-ACE-018 ---')
v = d['ids']['DF-ACE-018']
print(d['docs'][v['d'][0]]['file'], '|', d['docs'][v['d'][0]]['secs'][v['d'][1]]['h'])
print(d['docs'][v['d'][0]]['secs'][v['d'][1]]['t'][:300])
print('--- story section check ---')
for i, doc in enumerate(d['docs']):
    if 'Epic 1 v8' in doc['file']:
        for j, s in enumerate(doc['secs']):
            if s['h'].startswith('RWB-E1-001'):
                print(s['h']); print(s['t'][:400]); break
        break
print('--- kinds count ---')
print(collections.Counter(v['k'] for v in d['ids'].values()))
print('--- empty t ---')
print(sum(1 for v in d['ids'].values() if not v['t']))

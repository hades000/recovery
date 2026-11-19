import json, io, re, collections

d = json.load(io.open(r'_work\data\hub_payload.json', encoding='utf-8'))
rx = re.compile(r'^(RWB-[A-Z]{1,3}\d?-\d{3})\s+(.*)$')

def attr(t, name):
    m = re.search(r'(?:^|\n)\|?\s*' + re.escape(name) + r'\s*\|\s*([^|\n]+)', t or '')
    return m.group(1).strip() if m else ''

stories = {}
for di, doc in enumerate(d['docs']):
    if doc['inzip'] or 'Build Notes' in doc['name']:
        continue
    for si, s in enumerate(doc['secs']):
        m = rx.match(s['h'].strip())
        if not m:
            continue
        sk = attr(s['t'], 'Story key')
        if sk and sk != m[1]:
            continue
        if not sk and not attr(s['t'], 'Module'):
            continue
        if m[1] in stories:
            continue
        ea = re.search(r'E\d', attr(s['t'], 'Epic') or '')
        ep = ea.group(0) if ea else 'E' + (re.search(r'RWB-E(\d)', m[1]).group(1) if re.search(r'RWB-E(\d)', m[1]) else '')
        stories[m[1]] = (di, si, ep, attr(s['t'], 'Module'), doc['file'])

print('stories', len(stories))
print(collections.Counter(x[2] for x in stories.values()))
print('--- ep odd ---')
for k, v in stories.items():
    if v[2] not in ('E1','E2','E3','E4','E5','E6','E7','E8') and not k.startswith(('RWB-AD','RWB-DM','RWB-TE','RWB-ACE')):
        print(k, v)
print('--- families ---')
for pre in ('RWB-AD','RWB-DM','RWB-TE','RWB-ACE'):
    print(pre, sum(1 for k in stories if k.startswith(pre)))

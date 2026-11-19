import json, io, re, collections

d = json.load(io.open(r'_work\data\hub_payload.json', encoding='utf-8'))
rx = re.compile(r'^(RWB-[A-Z]{1,3}\d?-\d{3})\s+(.*)$')

def attr(t, name):
    m = re.search(r'(?:^|\n)\|?\s*' + re.escape(name) + r'\s*\|\s*([^|\n]+)', t or '')
    return m.group(1).strip() if m else ''

found = []
for di, doc in enumerate(d['docs']):
    if doc['inzip'] or 'Build Notes' in doc['name']:
        continue
    for si, s in enumerate(doc['secs']):
        m = rx.match(s['h'].strip())
        if not m:
            continue
        key = attr(s['t'], 'Story key')
        found.append((di, si, m.group(1), key, doc['file']))
print('headings', len(found), 'with matching key', sum(1 for x in found if x[2] == x[3]))
print(collections.Counter(x[2].split('-')[1] for x in found if x[2] == x[3]))
print('--- first 20 no key ---')
for x in [x for x in found if x[2] != x[3]][:20]:
    print(x[0], x[2], repr(x[3]), x[4][:70])
print('--- E2 found ---')
for x in [x for x in found if x[2].startswith('RWB-E2')][:5]:
    print(x)

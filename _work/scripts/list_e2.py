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
        if re.match(r'(?i)^removed', attr(s['t'], 'Status')):
            continue
        if m[1] in stories:
            continue
        ea = re.search(r'E\d', attr(s['t'], 'Epic') or '')
        ep = ea.group(0) if ea else 'E' + ((re.search(r'RWB-E(\d)', m[1]) or [None, ''])[1])
        stories[m[1]] = (di, si, ep, attr(s['t'], 'Module'), doc['file'], attr(s['t'], 'Epic'))

print('E2 stories', sum(1 for k in stories if k.startswith('RWB-E2')))
for k in sorted(stories):
    if k.startswith('RWB-E2'):
        print(k, stories[k][2], '|', stories[k][5], '|', stories[k][4][:50])
print('--- E3-8 with E2-ish module ---')
for k in sorted(stories):
    if stories[k][2] in ('E3','E4','E5','E6','E7','E8') and ('E2' in stories[k][4] or 'Epic 2' in stories[k][5]):
        print(k, stories[k][2], stories[k][5])

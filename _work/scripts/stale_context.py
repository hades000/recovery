import json, io, re

d = json.load(io.open(r'_work\data\hub_payload.json', encoding='utf-8'))
for target in ['User Stories Epic 1 v8.md', 'User Stories Epics 3 to 8 v3.md']:
    print('=====', target)
    doc = [x for x in d['docs'] if target in x['file']][0]
    for s in doc['secs']:
        t = s['t'] or ''
        for pat in ['SY-DATALOAD', 'load_run', 'inbound load', 'file load']:
            for m in re.finditer(re.escape(pat), t, re.I):
                line = t[max(0, t.rfind('\n', 0, m.start()) + 1):t.find('\n', m.end())]
                print(s['h'][:60], '|', line.strip()[:220])

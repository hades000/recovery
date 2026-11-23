import json, re
j = json.load(open(r'_work\msr\docs\D2-HUB\payload.bin', encoding='utf-8'))
rx = re.compile(r'document set', re.I)
hits = 0
for di, d in enumerate(j['docs']):
    for si, s in enumerate(d['secs']):
        for m in rx.finditer(s['t']):
            hits += 1
            print(di, si, d['folder'], '|', d['file'], '|', s['h'], '::', s['t'][max(0,m.start()-100):m.start()+120].replace('\n', ' '))
print('hits', hits)

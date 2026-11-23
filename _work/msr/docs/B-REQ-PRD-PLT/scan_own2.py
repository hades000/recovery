import json, io

d = json.load(io.open(r'_work/msr/plan/ownership.json', encoding='utf-8'))
out = []
for sec in ('tables', 'api', 'events', 'jobs', 'workflows'):
    for k, v in d[sec].items():
        if v.get('owner') == 'PLT' or 'PLT' in json.dumps(v):
            out.append('%s | %s | %s | %s | %s | asm=%s' % (sec, k, v.get('owner'), v.get('ruling', ''), v.get('basis', '')[:160], v.get('asm', '')))
io.open(r'_work/msr/docs/B-REQ-PRD-PLT/own_plt.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))

import json

j = json.load(open(r'_work\msr\docs\D2-HUB\payload.bin', encoding='utf-8'))
print('top:', {k: (type(v).__name__, len(v)) for k, v in j.items()})
d0 = j['docs'][0]
print('doc keys:', list(d0))
for k, v in d0.items():
    if k == 'secs':
        print('  secs', len(v), 'first keys', list(v[0]) if v else None)
    else:
        print(' ', k, '=', repr(v)[:200])
print('files sample:', json.dumps(j['files'], ensure_ascii=False)[:800])
print('fmeta sample:', json.dumps(j['fmeta'], ensure_ascii=False)[:800])
print('kinds sample:', json.dumps(j['kinds'], ensure_ascii=False)[:500])
print('ids sample:', json.dumps(j['ids'], ensure_ascii=False)[:500])
print('n docs', len(j['docs']))

import json, glob, os, io, sys

rows = []
for p in sorted(glob.glob(r'_work/msr/wp/B-PLT-*.md')):
    for line in io.open(p, encoding='utf-8'):
        line = line.strip()
        if line.startswith('{"id"'):
            try:
                rows.append((os.path.basename(p), json.loads(line)))
            except Exception as e:
                print('ERR', p, e, file=sys.stdout)

out = []
out.append('count %d' % len(rows))
for wp, r in rows:
    out.append('%-24s %-12s %-4s w%s %-20s %-12s %-20s %s | reqs=%s | wt=%s' % (
        r['id'], r['epic'], r['wt'], r['wave'], r['release'], r['legacy'],
        r.get('disposition', ''), r['title'], ','.join(r.get('reqs', [])), r['wt']))
io.open(r'_work/msr/docs/B-REQ-PRD-PLT/plt_stories.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out))

import csv
import io
from collections import Counter, OrderedDict

rows = list(csv.DictReader(io.open(r'_work\data\fields.csv', encoding='utf-8')))
new = [r for r in rows if r['Disposition'] == 'ACE new']
tbl = Counter()
for r in new:
    t = r['ACE object column'].split('.')[0]
    tbl[t] += 1
for k, v in tbl.most_common():
    print('%2d %s' % (v, k))
print('total', sum(tbl.values()))

print()
print('Windows of ACE reuse by table:')
reuse = Counter(r['ACE object column'].split('.')[0] for r in rows if r['Disposition'] == 'ACE reuse')
for k, v in reuse.most_common():
    print('%2d %s' % (v, k))
print('total', sum(reuse.values()))

import csv, collections

rows = list(csv.DictReader(open(r'_work/data/v5_fields.csv', encoding='utf-16')))
by = collections.OrderedDict()
for r in rows:
    by.setdefault(r['object_name'], []).append((r['field_id'], r['field_name']))

for o in [k for k in by if k.startswith('v_ace_')]:
    fs = by[o]
    print('%-26s %2d  %s .. %s' % (o, len(fs), fs[0][0], fs[-1][0]))
    print('    ' + ', '.join(f[1] for f in fs))

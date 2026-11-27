import openpyxl, re, collections
wb = openpyxl.load_workbook('../../stage/05 Technical architecture/Recovery Workbench Service Contract Catalog v3.xlsx')
ws = wb['Contract pairs']
rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None]
print(len(rows), collections.Counter(r[3] for r in rows), ws.auto_filter.ref, [int(r[0]) for r in rows] == list(range(1, len(rows)+1)))
for w in wb:
    for row in w.iter_rows():
        for c in row:
            if isinstance(c.value, str) and re.search(r'\b(169|29 operations|141 pairs|160)\b|customers/\{id\}|accountId|S10-14', c.value):
                print(w.title, c.coordinate, c.value[:300])
ops = [r[0] for r in wb['REST operations'].iter_rows(min_row=2, values_only=True) if r[0]]
print(len(ops), [o for o in ops if 'authorise' in o or 'parameters/{key}' in o or 'customers' in o])
print([r[:2] for r in wb['Open points'].iter_rows(values_only=True) if r[0]][-6:])

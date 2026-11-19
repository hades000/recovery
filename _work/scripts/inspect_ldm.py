import openpyxl, collections
p = r'06 Data/Recovery Workbench Logical Data Model and Data Dictionary v7.xlsx'
wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
ent = [r for r in list(wb['Entities'].iter_rows(values_only=True))[4:] if r[0]]
fld = [r for r in list(wb['Fields'].iter_rows(values_only=True))[4:] if r[1]]
by = collections.defaultdict(list)
for r in fld:
    by[r[1]].append(r)
print('entities', len(ent), 'fields', len(fld))
for name in [e[0] for e in ent if str(e[0]).startswith('v_ace_')]:
    rows = by[name]
    print('==', name, len(rows))
    print('; '.join('%s %s %s' % (r[2], r[4], r[9]) for r in rows))
print('--- ext ---')
for name in ['party_ext', 'contact_point_ext', 'account_ext', 'valuation_ext']:
    print(name, [(r[2], r[4], r[9]) for r in by[name]])

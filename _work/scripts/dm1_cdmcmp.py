import openpyxl, re, io
wb = openpyxl.load_workbook(r'06 Data/Recovery Workbench Conceptual Data Model v6.xlsx', read_only=True, data_only=True)
rows = list(wb['Entities'].iter_rows(min_row=4, values_only=True))
print(rows[0])
cdm = {r[0]: r for r in rows[1:] if r[0]}
txt = io.open(r'06 Data/Recovery Workbench Physical Schema v5.sql', encoding='utf-8').read()
so = {}
for m in re.finditer(r"INSERT INTO sys_objects \([^)]*\) VALUES \('([a-z_0-9]+)', '((?:[^']|'')*)', '([A-Z]+)', (NULL|'[A-Z0-9]+')", txt):
    so[m.group(1)] = m.group(4).strip("'")
print('v5', len(so), sum(1 for v in so.values() if v!='NULL'))
dpcol = [i for i,h in enumerate(rows[0]) if h and 'product' in str(h).lower()][0]
print('cdm', len(cdm), sum(1 for r in cdm.values() if r[dpcol] and str(r[dpcol]).startswith('DP')))
for k in sorted(set(so)|set(cdm)):
    a = so.get(k); b = cdm.get(k, [None]*9)[dpcol] if k in cdm else None
    if (a or 'NULL') != (b if b and str(b).startswith('DP') else 'NULL'):
        print(k, a, b, cdm.get(k))

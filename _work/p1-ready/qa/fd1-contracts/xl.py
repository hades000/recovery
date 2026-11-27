import openpyxl, re
wb = openpyxl.load_workbook('../../stage/05 Technical architecture/Recovery Workbench Service Contract Catalog v3.xlsx')
for ws in wb:
    print('=====', ws.title, ws.max_row, ws.max_column, ws.freeze_panes, ws.auto_filter.ref, list(ws.tables.items()) if ws.tables else '', ws.merged_cells.ranges and len(ws.merged_cells.ranges))
    for r in ws.iter_rows(min_row=1, max_row=4, values_only=True):
        print('  ', [str(v)[:50] if v is not None else None for v in r])
    for i, r in enumerate(ws.iter_rows(values_only=True), 1):
        t = ' | '.join(str(v) for v in r if v is not None)
        if re.search(r'GET /customers|Party flags|collateral|/payments|proof-of-delivery|S14|W1-contracts|AceDataReady.*P8|29 |/authorise', t):
            print(i, t[:210])

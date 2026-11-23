import openpyxl, json
wb = openpyxl.load_workbook("22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
ws = wb["Services"]
rows = list(ws.iter_rows(values_only=True))
print(json.dumps(rows, indent=0))
# counts
for sheet, col in (("Tables",1),("Endpoints",1),("Events",1),("Workflows and activities",1),("Jobs",1)):
    w = wb[sheet]
    from collections import Counter
    c = Counter(r[col] for r in w.iter_rows(min_row=2, values_only=True) if r[col])
    print(sheet, dict(sorted(c.items())))

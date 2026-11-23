import openpyxl, sys
sys.stdout.reconfigure(encoding="utf-8")
wb = openpyxl.load_workbook("22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx", data_only=True)
for sheet in ("Tables","Endpoints","Events","Workflows and activities","Jobs","Rulings"):
    ws = wb[sheet]
    print("==", sheet)
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[1] == "PLT":
            print("  ", r[0], "|", (r[2] or "")[:150])

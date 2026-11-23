import json, pathlib
import openpyxl

src = "06 Data/Recovery Workbench Source to Target Mapping v4.xlsx"
wb = openpyxl.load_workbook(src)
out = {}
for ws in wb.worksheets:
    rows = []
    for r in ws.iter_rows(values_only=True):
        rows.append([("" if c is None else str(c)) for c in r])
    out[ws.title] = rows
p = pathlib.Path("_work/msr/docs/B-DATA-18/v4_dump.json")
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print({k: len(v) for k, v in out.items()})

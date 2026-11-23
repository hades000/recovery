import openpyxl, json

p = r"10 Policy, controls and compliance/Recovery Workbench Controls Catalog v4.xlsx"
wb = openpyxl.load_workbook(p)
ws = wb["Controls"]
out = {}
for r in range(5, ws.max_row + 1):
    cid = ws.cell(row=r, column=1).value
    if cid and str(cid).startswith("CTL"):
        out[cid] = {
            "l2": ws.cell(row=r, column=2).value,
            "process": ws.cell(row=r, column=3).value,
            "performed": ws.cell(row=r, column=7).value,
            "first_in": ws.cell(row=r, column=14).value,
            "owner": ws.cell(row=r, column=15).value,
        }
for k, v in out.items():
    print(k, "|", v["l2"], "|", v["first_in"], "|", v["owner"], "|", str(v["performed"])[:70])
json.dump(out, open(r"_work/msr/docs/B-CTRL-35/controls_dump.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("--- assumptions B-CTRL-32 ids")
for line in open(r"_work/msr/assumptions/B-CTRL-32.jsonl", encoding="utf-8"):
    d = json.loads(line)
    print(d["id"], "|", d["text"][:90])

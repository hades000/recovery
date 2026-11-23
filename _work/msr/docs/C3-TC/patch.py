from pathlib import Path
p = Path("_work/msr/docs/C3-TC/build.py")
t = p.read_text(encoding="utf-8")
t = t.replace('''    for i, h in enumerate(["Service", "Test level", "Origin"], 15):
        rt.cell(row=4, column=i, value=h)
    style_header(rt, 4, range(15, 18))''', '''    for i, h in enumerate(["Service", "Test level", "Origin"], 11):
        rt.cell(row=4, column=i, value=h)
    style_header(rt, 4, range(11, 14))''')
t = t.replace('''        rt.cell(row=row, column=15, value=svc_name(code) if code else PH)
        rt.cell(row=row, column=16, value=LEVEL_MAP.get(str(rt.cell(row=row, column=9).value), "Component"))
        rt.cell(row=row, column=17, value=f"legacy rule set {rule} (kept)")
    for col, w in (("O", 22), ("P", 14), ("Q", 34)):''', '''        rt.cell(row=row, column=11, value=svc_name(code) if code else PH)
        rt.cell(row=row, column=12, value=LEVEL_MAP.get(str(rt.cell(row=row, column=9).value), "Component"))
        rt.cell(row=row, column=13, value=f"legacy rule set {rule} (kept)")
    for col, w in (("K", 22), ("L", 14), ("M", 34)):''')
t = t.replace('["Rule test cases O:Q"', '["Rule test cases K:M"')
p.write_text(t, encoding="utf-8")
print("patched", "Rule test cases K:M" in t, 'column=11' in t)

import openpyxl

SRC = openpyxl.load_workbook(r"01 Decisions and governance\Recovery Workbench Decision Log v10.xlsx")
OUT = openpyxl.load_workbook(r"01 Decisions and governance\Recovery Workbench Decision Log v11.xlsx")

for name in ("Open decisions", "Decisions taken", "By owner"):
    s, o = SRC[name], OUT[name]
    print("===", name, s.max_row, o.max_row)
    for r in range(1, s.max_row + 1):
        for c in range(1, s.max_column + 1):
            a, b = s.cell(r, c).value, o.cell(r, c).value
            if a != b:
                sa = str(a)[:90].replace("\n", " ")
                sb = str(b)[:90].replace("\n", " ")
                print(f"  {s.cell(r, c).coordinate}: v10={sa!r}  ->  v11={sb!r}")

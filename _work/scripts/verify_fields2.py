import re, os

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
vsql = open(os.path.join(ROOT, r"15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql"), encoding="utf-8").read()
views = {}
for m in re.finditer(r"CREATE OR REPLACE VIEW recovery\.(v_ace_\w+)\s*\nAS\n(.*?);\n", vsql, flags=re.S):
    views[m.group(1)] = re.findall(r"AS\s+(\w+)\s*(?:,|\n)", m.group(2))


def table_rows(s, heading):
    i = s.index(heading)
    j = s.index("| BR Field ID |", i)
    k = s.index("\n\n", j)
    rows = []
    for ln in s[j:k].splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 7 and cells[0].startswith("DF-"):
            rows.append(cells[1])
    return rows


for f, v in [("Recovery Workbench TSD S1 Valuation and route v2.md", "v_ace_valuation"),
             ("Recovery Workbench TSD S1 Valuation and route v2.md", "v_ace_score"),
             ("Recovery Workbench TSD S5 Assets and auction v2.md", "v_ace_npa_asset"),
             ("Recovery Workbench TSD S5 Assets and auction v2.md", "v_ace_npa_sale")]:
    s = open(os.path.join(ROOT, "_work", "staging", f), encoding="utf-8").read()
    got = table_rows(s, "**%s**" % v)
    exp = views[v]
    print(v, "doc", len(got), "sql", len(exp), "match", got == exp)
    if got != exp:
        print("  doc-only", [x for x in got if x not in exp], "sql-only", [x for x in exp if x not in got])

sql = open(os.path.join(ROOT, r"06 Data\Recovery Workbench Physical Schema v5.sql"), encoding="utf-8").read()
tables = {}
for m in re.finditer(r"CREATE TABLE (\w+) \((.*?)\n\);", sql, flags=re.S):
    cols = []
    for ln in m.group(2).splitlines():
        ln = ln.strip().rstrip(",")
        if not ln or ln.startswith("CONSTRAINT"):
            continue
        cols.append(ln.split(" ")[0])
    tables[m.group(1)] = cols
p1 = open(os.path.join(ROOT, "_work", "staging", "Recovery Workbench TSD P1 Recovery data engine v2.md"), encoding="utf-8").read()
for t in ("party_ext", "contact_point_ext", "account_ext", "valuation_ext", "data_product_load", "case_list_row", "dp_treatment"):
    names = table_rows(p1, "**%s**" % t)
    print(t, "doc", len(names), "schema", len(tables[t]), "prefix-match", names == tables[t][:len(names)], "all-in", all(n in tables[t] for n in names))

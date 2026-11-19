import re, os

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
vsql = open(os.path.join(ROOT, r"15 ACE DB Alignment\Recovery Workbench ACE Source Views v1.sql"), encoding="utf-8").read()
views = {}
for m in re.finditer(r"CREATE OR REPLACE VIEW recovery\.(v_ace_\w+)\s*\nAS\n(.*?);\n", vsql, flags=re.S):
    views[m.group(1)] = re.findall(r"AS\s+(\w+)\s*(?:,|\n)", m.group(2))


def doc_rows(path, heading, start_pat):
    s = open(path, encoding="utf-8").read()
    i = s.index(heading)
    j = s.index(start_pat, i)
    k = s.index("\n\n", j)
    block = s[j:k]
    rows = []
    for ln in block.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 7 and cells[0].startswith("DF-"):
            rows.append(cells[1])
    return rows


checks = [
    ("Recovery Workbench TSD S1 Valuation and route v2.md", "v_ace_valuation"),
    ("Recovery Workbench TSD S1 Valuation and route v2.md", "v_ace_score"),
    ("Recovery Workbench TSD S5 Assets and auction v2.md", "v_ace_npa_asset"),
    ("Recovery Workbench TSD S5 Assets and auction v2.md", "v_ace_npa_sale"),
]
for f, v in checks:
    got = doc_rows(os.path.join(ROOT, "_work", "staging", f), v, "| BR Field ID |")
    exp = views[v]
    print(v, "doc", len(got), "sql", len(exp), "match", got == exp)
    if got != exp:
        print("  doc-only", [x for x in got if x not in exp])
        print("  sql-only", [x for x in exp if x not in got])

# extension fields in P1 vs schema
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
for t in ("party_ext", "contact_point_ext", "account_ext", "valuation_ext", "data_product_load", "case_list_row"):
    i = p1.index("**%s**" % t)
    j = p1.index("\n\n", i)
    rows = re.findall(r"\| (DF-[A-Z]+-\d+) \| (\w+) \|", p1[i:j])
    names = [r[1] for r in rows]
    if t in ("party_ext", "contact_point_ext", "account_ext", "valuation_ext"):
        print(t, "doc", len(names), "schema", len(tables[t]), "prefix-match", names == tables[t][:len(names)])
    else:
        print(t, "doc", len(names), "schema", len(tables[t]), "all-in-schema", all(n in tables[t] for n in names))

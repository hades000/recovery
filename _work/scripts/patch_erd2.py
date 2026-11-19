import re, os

p = os.path.join(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14", r"_work\scripts\build_erd_v4.py")
s = open(p, encoding="utf-8").read()

# 1. figure curve
old = """sv.append('<path d="M 980 484 C 980 505, 120 505, 120 484" fill="none" stroke="#C0392B" stroke-width="1.5" stroke-dasharray="4,3"/>')
sv.append('<text x="550" y="507" font-size="10.5" fill="#C0392B" text-anchor="middle">no write, and no foreign key into ACE</text>')"""
new = """sv.append('<path d="M 980 479 C 980 490, 120 490, 120 479" fill="none" stroke="#C0392B" stroke-width="1.5" stroke-dasharray="4,3"/>')
sv.append('<text x="550" y="507" font-size="10.5" fill="#C0392B" text-anchor="middle">no write, and no foreign key into ACE</text>')"""
assert old in s
s = s.replace(old, new, 1)

# 2. print css
old = """ .tw{max-height:none;overflow:visible}
 .cards{grid-template-columns:1fr 1fr}
 .ent{page-break-inside:avoid}
}"""
new = """ .tw{max-height:none;overflow:visible}
 .cards{display:block}
 .ent{margin:0 0 10px;page-break-inside:avoid}
 .filter{display:none}
 table{font-size:11px}
}"""
assert old in s
s = s.replace(old, new, 1)

# 3. reference rows: merge cardinality into reference
old = """allrows = "".join('<tr data-g="%s"><td class="code">%s</td><td class="code">%s</td><td class="code">%s</td><td>%s</td><td>%s</td><td>%s</td><td class="code">%s</td></tr>'
                  % (dp_of(x["child"]), E(x["child"]), E(x["col"]), E(x["parent"]),
                     E("Mandatory" if x["mand"] else "Optional"), E(x["kind"]), E(x["card"]),
                     E(dp_of(x["child"]) + " to " + dp_of(x["parent"]))) for x in rels)"""
new = """allrows = "".join('<tr data-g="%s"><td class="code">%s</td><td class="code">%s</td><td class="code">%s</td><td>%s</td><td>%s</td><td class="code">%s</td></tr>'
                  % (dp_of(x["child"]), E(x["child"]), E(x["col"]), E(x["parent"]),
                     E(("Mandatory, " if x["mand"] else "Optional, ") + x["card"]), E(x["kind"]),
                     E(dp_of(x["child"]) + " to " + dp_of(x["parent"]))) for x in rels)"""
assert old in s
s = s.replace(old, new, 1)

old = """<div class="tw"><table id="allrels"><thead><tr><th>Entity</th><th>Field</th><th>Refers to</th><th>Reference</th><th>Kind</th><th>Cardinality</th><th>Data products</th></tr></thead><tbody>%s</tbody></table></div>"""
new = """<div class="tw"><table id="allrels"><colgroup><col style="width:24%%"><col style="width:18%%"><col style="width:18%%"><col style="width:12%%"><col style="width:16%%"><col style="width:12%%"></colgroup><thead><tr><th>Entity</th><th>Field</th><th>Refers to</th><th>Reference</th><th>Kind</th><th>Data products</th></tr></thead><tbody>%s</tbody></table></div>"""
assert old in s
s = s.replace(old, new, 1)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")

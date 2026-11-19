import os
p = os.path.join(r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14", r"_work\scripts\build_erd_v4.py")
s = open(p, encoding="utf-8").read()
old = """with 104 references. The 14 data products hold 97 of them; OPS, AGT and RPT hold the other 25. The views are external and read only. The 18 business-key links carry no foreign key into ACE; the other 86 references are ordinary foreign keys inside the recovery schema. Case and ownership is shaded; the ACE views are dashed.</p>"""
new = """with 104 references. The 14 data products hold 97 of them; OPS, AGT and RPT hold the other 25. The views are external and read only, and their boxes are dashed. The 18 business-key links carry no foreign key into ACE; the other 86 references are ordinary foreign keys inside the recovery schema.</p>"""
assert old in s
s = s.replace(old, new, 1)
old = """<p class="muted">%d references cross a data product boundary and %d stay inside one. The dot is at the referring end.</p>"""
new = """<p class="muted">%d references cross a data product boundary and %d stay inside one. Each row reads from the first data product to the second, and is ordered by count.</p>"""
assert old in s
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched")

"""Fill the rulings workbook per the programme directive (D-RCV-60, 26 November 2026).
Accept the recommended resolution for every gap and confirm every assumption, except business decisions:
an item whose owner role is a business decision-maker stays open (Deferred), and so do the assumptions
tied to it. Writes a new workbook version; never edits v3."""
import re, sys, json, openpyxl
from collections import Counter
src, dst, rep = sys.argv[1], sys.argv[2], sys.argv[3]
BIZ = re.compile(r"product owner|business lead|business owner|compliance|pdpa|\brisk\b|rw-risk|legal|finance|cfo|"
                 r"head of|audit|product head|operations (head|manager|lead)|collections (head|lead)|"
                 r"recovery (head|lead)|programme governance|program governance|sponsor|steering|credit|treasury|"
                 r"\bdpo\b|data protection", re.I)
BY = "Programme governance (directive)"
SRC = ("Programme directive, 26 November 2026: accept the recommended resolution and confirm the assumptions, "
       "except business decisions")
reg = {}  # register gap -> assumption id
for line in open("23 Document Gaps/Recovery Workbench Gap Register v1.md", encoding="utf-8"):
    if line.startswith("| GAP-"):
        c = [x.strip() for x in line.split("|")]
        reg[c[1]] = c[13]
wb = openpyxl.load_workbook(src)
ws = wb["Rulings"]
hdr = [c.value for c in ws[1]]
ix = {h: i for i, h in enumerate(hdr)}
rows = list(ws.iter_rows(min_row=2))
biz_items, held_asm = set(), set()
for r in rows:
    k, o = r[ix["Kind"]].value or "", r[ix["Owner role"]].value or ""
    if k in ("Register gap", "Script gap") and BIZ.search(o):
        iid = r[ix["Item ID"]].value
        biz_items.add(iid)
        a = reg.get(iid, "")
        held_asm.update(re.findall(r"ASM-\d{4}", a))
held_asm_script = set()
for r in rows:
    if r[ix["Kind"]].value == "Script assumption":
        m = re.search(r"gap (CG-\S+?);", r[ix["Notes"]].value or "")
        if m and m.group(1) in biz_items:
            held_asm_script.add(r[ix["Item ID"]].value)
cnt, out = Counter(), []
for r in rows:
    k, iid = r[ix["Kind"]].value or "", r[ix["Item ID"]].value
    if iid in biz_items or iid in held_asm or iid in held_asm_script:
        d, note = "Deferred", "Business decision: stays open for the owner role (directive exception)"
    elif "assumption" in k.lower():
        d, note = "Accept assumption", "Confirmed under the programme directive"
    else:
        d, note = "Accept proposed", "Recommended resolution accepted under the programme directive"
    r[ix["Decision"]].value = d
    r[ix["Decided by (role)"]].value = BY
    r[ix["Ruling source"]].value = SRC
    old = r[ix["Notes"]].value
    r[ix["Notes"]].value = f"{old}; {note}" if old else note
    cnt[(k, d)] += 1
    if d == "Deferred":
        out.append({"ruling": r[ix["Ruling ID"]].value, "item": iid, "kind": k,
                    "owner": r[ix["Owner role"]].value, "title": r[ix["Title"]].value})
wb.save(dst)
with open(rep, "w", encoding="utf-8") as fh:
    for o in out:
        fh.write(json.dumps(o, ensure_ascii=False) + "\n")
for k, v in sorted(cnt.items()):
    print(v, k)

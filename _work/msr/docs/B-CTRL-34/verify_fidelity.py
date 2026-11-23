"""Verify every version 2 paragraph and table cell survives in version 3 (word for word)."""
import re
import docx

src = docx.Document(r"10 Policy, controls and compliance/Recovery Workbench Personal Data Protection Design v2.docx")
dst = docx.Document(r"10 Policy, controls and compliance/Recovery Workbench Personal Data Protection Design v3.docx")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


dtext = norm(" ".join(p.text for p in dst.paragraphs))
for t in dst.tables:
    for r in t.rows:
        for c in r.cells:
            dtext += " " + norm(c.text)

missing = []
n = 0
for p in src.paragraphs:
    t = norm(p.text)
    if not t:
        continue
    n += 1
    if t not in dtext:
        missing.append(("para", t[:120]))
for ti, t in enumerate(src.tables, 1):
    for r in t.rows:
        for c in r.cells:
            v = norm(c.text)
            if not v:
                continue
            n += 1
            if v not in dtext:
                missing.append((f"table {ti}", v[:120]))

print("checked", n, "source strings; missing", len(missing))
for m in missing:
    print(m)

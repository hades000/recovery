import os
import zipfile

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v3.zip")
OUT = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v4.zip")
STAGE = os.path.join(ROOT, r"_work\staging")

zsrc = zipfile.ZipFile(SRC)
order = [i.filename for i in zsrc.infolist()]
print("v3 members", len(order))

changed, same = [], []
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
    for name in order:
        old = zsrc.read(name)
        p = os.path.join(STAGE, name)
        if os.path.exists(p):
            new = open(p, "rb").read()
        else:
            new = old
        if new == old:
            same.append(name)
        else:
            changed.append(name)
        zout.writestr(name, new)

znew = zipfile.ZipFile(OUT)
new_names = [i.filename for i in znew.infolist()]
print("v4 members", len(new_names), "same order:", new_names == order)
print("changed", len(changed))
for n in changed:
    print("  C", n)
print("unchanged", len(same))
print("zip size", os.path.getsize(OUT))
# confirm the zip is readable and every member is a markdown file
bad = [n for n in new_names if not n.endswith(".md")]
print("non-md members", bad)
for n in new_names:
    data = znew.read(n)
    assert len(data) > 0, n
print("all members read, total uncompressed", sum(len(znew.read(n)) for n in new_names))

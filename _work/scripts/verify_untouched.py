import os, zipfile, hashlib
ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
V3ZIP = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v3.zip")
V3DIR = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v3")
z = zipfile.ZipFile(V3ZIP)
bad = []
for i in z.infolist():
    p = os.path.join(V3DIR, i.filename)
    if not os.path.exists(p):
        bad.append((i.filename, "missing")); continue
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != hashlib.sha256(z.read(i.filename)).hexdigest():
        bad.append((i.filename, "differs"))
print("v3 folder members", len(z.infolist()), "mismatches", bad)
for f in ["Recovery Workbench Entity Relationship Diagram v3.html", "Recovery Workbench Entity Relationship Diagram v3.pdf"]:
    p = os.path.join(ROOT, "06 Data", f)
    print(f, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest()[:12])
for f in ["Recovery Workbench Entity Relationship Diagram v4.html", "Recovery Workbench Entity Relationship Diagram v4.pdf"]:
    p = os.path.join(ROOT, "06 Data", f)
    print(f, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest()[:12])

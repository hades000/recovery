import zipfile, re, sys
sys.stdout.reconfigure(encoding="utf-8")
p = "11 Delivery and operations/Recovery Workbench Engineering Practices v5.docx"
z = zipfile.ZipFile(p)
for n in z.namelist():
    if n.endswith((".xml", ".rels")):
        s = z.read(n).decode("utf-8", "ignore")
        for pat in ("Rajdeep", "Ghai", "K. Book", "K. Pipat", "K. Tee", "@"):
            if pat in s:
                idx = s.find(pat)
                print(n, "|", pat, "|", s[max(0,idx-80):idx+60].replace("\n"," "))
print("--- footer ---")
print(z.read("word/footer1.xml").decode("utf-8")[:1500])
print("--- app ---")
print(z.read("docProps/app.xml").decode("utf-8")[:800])

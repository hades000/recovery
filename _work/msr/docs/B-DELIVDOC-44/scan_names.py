import zipfile, re
p = "11 Delivery and operations/Recovery Workbench Engineering Practices v6.docx"
z = zipfile.ZipFile(p)
hits = []
for n in z.namelist():
    s = z.read(n).decode("utf-8", "ignore")
    for pat in ("Rajdeep", "Ghai", "K. Book", "K. Pipat", "K. Tee", "Claude"):
        if pat in s:
            hits.append((n, pat))
print("parts:", len(z.namelist()))
print("hits:", hits)
print(z.read("docProps/core.xml").decode("utf-8"))

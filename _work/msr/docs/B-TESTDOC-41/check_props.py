"""Look for a person name or an e-mail in any part of the new docx."""
import re
import zipfile

PATH = "09 Testing and quality/Recovery Workbench Test Data Plan v4.docx"
BAD = ["rajdeep", "ghai", "@"]

z = zipfile.ZipFile(PATH)
hits = []
for name in z.namelist():
    if not name.endswith((".xml", ".rels")):
        continue
    t = z.read(name).decode("utf-8", "ignore").lower()
    for b in BAD:
        if b in t:
            hits.append((name, b))
print("hits:", hits)
print("parts:", len(z.namelist()))
print("custom:", z.read("docProps/custom.xml").decode("utf-8")[:400] if "docProps/custom.xml" in z.namelist() else "none")
print("core:", z.read("docProps/core.xml").decode("utf-8")[:600])

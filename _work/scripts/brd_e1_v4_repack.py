"""Repack v4: word/document.xml from the python-docx output, every other part byte-for-byte from v3."""
import re, shutil, sys, zipfile
R = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\03 Requirements and specifications\Recovery Workbench Business Requirements Epic 1"
src, built, tmp = R + " v3.docx", R + " v4.docx", sys.argv[1]
a, b = zipfile.ZipFile(src), zipfile.ZipFile(built)
for n in ("word/footer1.xml",):
    print(n, "v3 text:", re.sub(r"<[^>]+>", "", a.read(n).decode())[:200])
doc = b.read("word/document.xml")
with zipfile.ZipFile(tmp, "w") as z:
    for info in a.infolist():
        data = doc if info.filename == "word/document.xml" else a.read(info.filename)
        z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)
a.close(); b.close()
shutil.copyfile(tmp, built)
print("repacked", built)

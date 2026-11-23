import shutil, zipfile, re, sys
from pathlib import Path
src = Path("06 Data/Recovery Workbench Data Migration Approach v3.docx")
out = Path("_work/msr/docs/B-DATA-21/template_v3_fixed.docx")
if out.exists():
    out.unlink()
tmp = Path("_work/msr/docs/B-DATA-21/_tmp_docx")
if tmp.exists():
    shutil.rmtree(tmp)
tmp.mkdir(parents=True)
with zipfile.ZipFile(src) as z:
    z.extractall(tmp)
p = tmp / "word" / "styles.xml"
x = p.read_text(encoding="utf-8")
for n in ("1", "2", "3", "4", "5", "6"):
    x = x.replace('<w:name w:val="Heading %s"/>' % n, '<w:name w:val="heading %s"/>' % n)
p.write_text(x, encoding="utf-8")
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(tmp.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(tmp).as_posix())
shutil.rmtree(tmp)
print("WROTE", out)

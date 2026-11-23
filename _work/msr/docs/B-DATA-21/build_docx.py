import subprocess, sys, shutil
from pathlib import Path
out = Path("06 Data/Recovery Workbench Data Migration Approach v4.docx")
if out.exists():
    out.unlink()
r = subprocess.run([sys.executable, "-I", "22 Microservice Realignment/compat/office_write.py", "md-docx",
    "_work/msr/docs/B-DATA-21/Recovery Workbench Data Migration Approach v4.md", str(out),
    "--template", "_work/msr/docs/B-DATA-21/template_v3_fixed.docx"], capture_output=True, text=True)
print(r.stdout.strip()); print(r.stderr.strip()[-500:])

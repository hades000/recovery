import hashlib
from pathlib import Path

import docx

a = Path("_work/msr/docs/B-REQ-BRD-E2/Recovery Workbench Business Requirements Epic 2 v3.md").read_bytes()
b = Path("03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.md").read_bytes()
print("md identical:", hashlib.sha256(a).hexdigest() == hashlib.sha256(b).hexdigest(), len(a), "bytes")

d = docx.Document("03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.docx")
text = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
    c.text for t in d.tables for r in t.rows for c in r.cells)
print("tables:", len(d.tables), "paragraphs:", len(d.paragraphs), "chars:", len(text))
for probe in ("K. Book", "K. Tee", "K. Jao", "Heading 1", "Backtick", "`"):
    print(f"{probe!r} present:", probe in text or any(probe in p.style.name for p in d.paragraphs))
for probe in ("Architecture lead with the architecture team", "Business lead with the test lead",
              "D-RCV-60 microservice realignment", "T3 Code / OpenCode / DeepSeek v4.1 Flash",
              "RWB-E2-023", "RWB-SVC-S9", "(tentative)", "CG-B-REQ-BRD-E2-1",
              "SCB Collections and Recovery. Henka Group, 22 November 2026."):
    print(f"{probe!r}:", text.count(probe))
print("first paragraphs:", [p.text for p in d.paragraphs[:5]])

import re
from pathlib import Path

files = [r"05 Technical architecture/Recovery Workbench Service Catalog v1.md",
         r"05 Technical architecture/Recovery Workbench Service Template Specification v1.md"]
total = 0
for f in files:
    t = Path(f).read_text(encoding="utf-8")
    ph = re.findall(r"Not specified in the source documents \(CG-B-ARCH-SVC-(\d+); ASM-B-ARCH-SVC-(\d+)\)", t)
    cites = sorted(set(re.findall(r"\b(?:CG|ASM)-B-ARCH-SVC-\d+\b", t)))
    print(f)
    print("  placeholders:", len(ph), "distinct pairs:", sorted({p[0] for p in ph}))
    print("  citations:", len(cites))
    print("  'jira':", len(re.findall(r"(?i)\bjira\b|atlassian", t)))
    print("  header ok:", t.splitlines()[0].startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."))
    print("  change row ok:", "D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in t)
    print("  tables:", t.count("\n|---"))
    total += len(ph)
print("total placeholders:", total)

import json
for kind in ("gaps", "assumptions"):
    p = Path("_work/msr") / kind / "B-ARCH-SVC.jsonl"
    rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(kind, len(rows), "ids ok:", all(r["id"].startswith(("CG-B-ARCH-SVC-" if kind == "gaps" else "ASM-B-ARCH-SVC-")) for r in rows))

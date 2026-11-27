import re, json, sys
from pathlib import Path
sys.path.insert(0, r"_work/msr/directive")
import lint
p = Path(r"_work/msr/directive/mp/out/RWB-ITG-E1031-ITG.md")
t = p.read_text(encoding="utf-8")
old1 = "| Contract dependencies | RWB-ITG-E1031-CON; contract version Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-23) |"
new1 = "| Contract dependencies | No contract story of its own is in the story set (DOR-RWB-ITG-E1031-ITG-21); the suite consumes the published wave 1 contracts of P3 rwb-case and P4 rwb-access; contract version Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-23) |"
old2 = "No access: refused with status 403 and MSG-P4-002 by the right check (AC9, X7)."
new2 = "No access: Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-10); the call is refused with status 403 and MSG-P4-002 by the right check (AC9, X7)."
for o, n in ((old1, new1), (old2, new2)):
    print("count", t.count(o), "cells", len(re.split(r"(?<!\\)\|", n.strip()[1:-1])) if n.startswith("|") else "n/a")
t2 = t.replace(old1, new1, 1).replace(old2, new2, 1)
meta = json.loads(Path(r"_work/msr/directive/mp/chunks/RWB-ITG-E1031-ITG/meta.json").read_text(encoding="utf-8"))
before = Path(meta["input_file"]).read_text(encoding="utf-8")
print(lint.lint_text("RWB-ITG-E1031-ITG", before, t2))

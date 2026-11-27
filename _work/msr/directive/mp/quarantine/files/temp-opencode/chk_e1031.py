import re, sys
from pathlib import Path
sys.path.insert(0, r"_work/msr/directive")
p = Path(r"_work/msr/directive/mp/out/RWB-ITG-E1031-ITG.md")
t = p.read_text(encoding="utf-8")
old = "| Contract dependencies | RWB-ITG-E1031-CON; contract version Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-23) |"
new = "| Contract dependencies | None of its own; the suite consumes the published wave 1 contracts of P3 rwb-case and P4 rwb-access, and no contract story of its own exists (DOR-RWB-ITG-E1031-ITG-21); contract version Not specified in the source documents (DOR-RWB-ITG-E1031-ITG-23) |"
print("count", t.count(old))
print("cells", len(re.split(r"(?<!\\)\|", new.strip()[1:-1])))
t2 = t.replace(old, new, 1)
import lint
before = Path(__import__("json").loads(Path(r"_work/msr/directive/mp/chunks/RWB-ITG-E1031-ITG/meta.json").read_text(encoding="utf-8"))["input_file"]).read_text(encoding="utf-8")
print(lint.lint_text("RWB-ITG-E1031-ITG", before, t2))

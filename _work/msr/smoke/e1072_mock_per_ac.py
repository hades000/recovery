"""Move the E1072 APP mock Given from the Background into each scenario, as the WP asks per AC."""
import re
from pathlib import Path

p = Path(__file__).resolve().parents[3] / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-PLT-LIB Shared libraries" / "RWB PLT E1072 APP Drools runtime and rule package store v1.md"
text = p.read_text(encoding="utf-8")
mock = '    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum'
lines = text.splitlines()
lines = [l for l in lines if l != mock]
out = []
for l in lines:
    out.append(l)
    if re.match(r"^  Scenario: AC\d+", l):
        out.append(mock)
text = "\n".join(out) + "\n"
text = text.replace(
    "The one added Given in the Background is new and is the cross-service part: the model is fetched from rwb-decision instead of read from a local table, and the fetched model carries the same 26 ordered rows, its catalog projection and its checksum (CG-B-PLT-LIB-02-E1072-1; ASM-B-PLT-LIB-02-E1072-1).",
    "The one added Given in each scenario is new and is the cross-service part: the model is fetched from rwb-decision instead of read from a local table, and the fetched model carries the same 26 ordered rows, its catalog projection and its checksum (CG-B-PLT-LIB-02-E1072-1; ASM-B-PLT-LIB-02-E1072-1).",
)
p.write_text(text, encoding="utf-8")
print("scenarios with mock Given:", text.count("Given the rwb-decision contract mock returns"))

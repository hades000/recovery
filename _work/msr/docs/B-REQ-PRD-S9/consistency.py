"""Consistency pass over the S9 PRD: ID counts, coverage both ways, odd characters."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(errors="replace")
P = Path(__file__).resolve().parents[4] / "03 Requirements and specifications" / "PRD" / "Recovery Workbench PRD S9 rwb-partner v1.md"
t = P.read_text(encoding="utf-8")

def ids(prefix, text=t, width=3):
    return sorted({int(m) for m in re.findall(rf"\b{prefix}-(\d{{{width}}})\b", text)})

cap, fr, nfr, ac = ids("CAP-S9"), ids("FR-S9"), ids("NFR-S9"), ids("AC-S9")
jrn, rol, oq = ids("JRN-S9", width=2), ids("ROL-S9", width=2), ids("OQ-S9", width=2)

def rng(name, v):
    miss = [i for i in range(1, max(v) + 1) if i not in v]
    print(f"{name}: {len(v)} rows, max {max(v)}, gaps {miss}")

rng("CAP", cap); rng("FR", fr); rng("NFR", nfr); rng("AC", ac); rng("JRN", jrn); rng("ROL", rol); rng("OQ", oq)

# table row counts
sec = t.split("# 6. Functional requirements")[1].split("# 7. Non-functional")[0]
fr_rows = re.findall(r"(?m)^\| (FR-S9-\d{3}) \|", sec)
print("FR table rows:", len(fr_rows), "unique:", len(set(fr_rows)))
sec7 = t.split("# 7. Non-functional requirements")[1].split("# 8. Data requirements")[0]
print("NFR table rows:", len(re.findall(r"(?m)^\| (NFR-S9-\d{3}) \|", sec7)))
sec5 = t.split("# 5. Capabilities and features")[1].split("## 5.1")[0]
print("CAP table rows:", len(re.findall(r"(?m)^\| (CAP-S9-\d{3}) \|", sec5)))
sec11 = t.split("## 11.1 Acceptance criteria")[1].split("## 11.2")[0]
print("AC table rows:", len(re.findall(r"(?m)^\| (AC-S9-\d{3}) \|", sec11)))

# coverage: every FR in an AC row of 11.1
ac_block = sec11
covered = {int(x) for x in re.findall(r"FR-S9-(\d{3})", ac_block)}
print("FR not covered by any AC:", [f"FR-S9-{i:03d}" for i in range(1, max(fr) + 1) if i not in covered])

# coverage: every FR in the 11.2 summary
summ = t.split("## 11.2 Requirement trace summary")[1].split("## 11.3")[0]
in_sum = {int(x) for x in re.findall(r"FR-S9-(\d{3})", summ)}
print("FR not in 11.2:", [f"FR-S9-{i:03d}" for i in range(1, max(fr) + 1) if i not in in_sum])
in_sum_n = {int(x) for x in re.findall(r"NFR-S9-(\d{3})", summ)}
print("NFR not in 11.2:", [f"NFR-S9-{i:03d}" for i in range(1, max(nfr) + 1) if i not in in_sum_n])

# every CAP referenced by at least one FR
cap_in_fr = {int(x) for x in re.findall(r"CAP-S9-(\d{3})", sec)}
print("CAP with no FR:", [f"CAP-S9-{i:03d}" for i in cap if i not in cap_in_fr])

# odd characters
odd = sorted({c for c in t if ord(c) > 127})
print("non-ascii chars:", [(c, hex(ord(c))) for c in odd][:20])
print("mojibake markers:", t.count("\ufffd"), t.count("?"))
print("lines:", len(t.splitlines()), "chars:", len(t))

"""Compare the v3 source text with the v4 draft: report every source line not found verbatim."""
import re
from pathlib import Path

SRC = Path(r"_work/msr/extract/B-TECH-10/Recovery Workbench Error Handling and Resilience Standard v3.md")
NEW = Path(r"_work/msr/docs/B-TECH-10/Recovery Workbench Error Handling and Resilience Standard v4.md")

INTENDED = {
    "SCB Collections and Recovery. Henka Group, 16 November 2026",
    "| Version | 3 |",
    "| Date | 16 November 2026 |",
    "| Change | v3, 16 November 2026, D-RCV-36: Temporal retry policy and activity idempotency, the failed decision log rule, the outbox for Epics 1 and 2, and Drools failure handling (ADR-011, ADR-012) |",
}

src = [l.rstrip() for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
new = [l.rstrip() for l in NEW.read_text(encoding="utf-8").splitlines()]
missing, changed = [], []
for l in src:
    if l in new:
        continue
    if l in INTENDED:
        changed.append(l)
        continue
    missing.append(l)

print("source lines:", len(src))
print("kept verbatim:", len(src) - len(missing) - len(changed))
print("intended changes:", len(changed))
print("MISSING:", len(missing))
for m in missing:
    print("  -", m[:160])

# structure of the new file
heads = re.findall(r"^# .+$", "\n".join(new), re.M)
print("headings:", len(heads))
for h in heads:
    print("  ", h)
print("first two lines:", new[0], "|", new[1])
print("D-RCV-60 present:", "D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" in "\n".join(new))
print("tables:", sum(1 for l in new if l.startswith("|")))
cites = sorted(set(re.findall(r"(?:CG|ASM)-B-TECH-10-\d+", "\n".join(new))))
print("citations:", cites)

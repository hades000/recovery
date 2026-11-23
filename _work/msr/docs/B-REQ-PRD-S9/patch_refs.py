"""Patch the applied_in references of the S9 register rows to the final FR numbering."""
import io
from pathlib import Path

p = Path(__file__).with_name("emit_registers.py")
t = p.read_text(encoding="utf-8")

SUBS = [
    ("Section 2.4 constraint 1; Section 6 FR-S9-033, FR-S9-034; Section 8.2; Section 9; Section 12 OQ-S9-01",
     "Section 2.4 constraint 1; Section 6 FR-S9-041, FR-S9-042; Section 8.2; Section 9; Section 12 OQ-S9-01"),
    ("Section 2.3; Section 5 CAP-S9-007, CAP-S9-009; Section 6 FR-S9-017, FR-S9-018, FR-S9-025; Section 9; Section 12 OQ-S9-02",
     "Section 2.3; Section 5 CAP-S9-007, CAP-S9-009; Section 6 FR-S9-024, FR-S9-025, FR-S9-031; Section 9; Section 12 OQ-S9-02"),
    ("Section 8.1; Section 10.4; Section 12 OQ-S9-03",
     "Section 8.1; Section 10.5; Section 12 OQ-S9-03"),
    ("Section 2.4 constraint 7; Section 6 (Rule column); Section 10.4; Section 12 OQ-S9-06",
     "Section 2.4 constraint 7; Section 6 (Rule column); Section 10.5; Section 12 OQ-S9-06"),
    ("Section 2.4 constraint 6; Section 6 FR-S9-022; Section 9; Section 10.4; Section 12 OQ-S9-07",
     "Section 2.4 constraint 6; Section 6 FR-S9-026; Section 9; Section 10.5; Section 12 OQ-S9-07"),
    ("Section 2.3; Section 6 FR-S9-024; Section 9; Section 12 OQ-S9-11",
     "Section 2.3; Section 6 FR-S9-027; Section 9; Section 10.5; Section 12 OQ-S9-11"),
    ("Section 6 FR-S9-030; Section 9; Section 12 OQ-S9-12",
     "Section 6 FR-S9-036; Section 9; Section 12 OQ-S9-12"),
    ("Section 6 FR-S9-014; Section 9; Section 12 OQ-S9-13",
     "Section 6 FR-S9-039; Section 9; Section 10.5; Section 12 OQ-S9-13"),
    ("Section 6 FR-S9-013, FR-S9-014; Section 9; Section 12 OQ-S9-14",
     "Section 6 FR-S9-039, FR-S9-043; Section 9; Section 12 OQ-S9-14"),
    ("Section 3; Section 6 FR-S9-013; Section 8.1; Section 9; Section 12 OQ-S9-17",
     "Section 3; Section 6 FR-S9-038; Section 8.1; Section 9; Section 12 OQ-S9-17"),
    ("Section 6 FR-S9-023; Section 8.4 rule 1; Section 12 OQ-S9-21",
     "Section 6 FR-S9-028; Section 8.4 rule 1; Section 8.1; Section 12 OQ-S9-21"),
    ("Section 6 FR-S9-024; Section 9; Section 12 OQ-S9-22",
     "Section 6 FR-S9-030; Section 9; Section 12 OQ-S9-22"),
    ("Section 6 FR-S9-024; Section 9; Section 12 OQ-S9-11",
     "Section 6 FR-S9-027; Section 9; Section 12 OQ-S9-11"),
    ("Section 5 CAP-S9-002; Section 6 FR-S9-003; Section 8.4 rule 1; Section 12 OQ-S9-16",
     "Section 5 CAP-S9-002; Section 6 FR-S9-003; Section 8.1; Section 8.4 rule 1; Section 12 OQ-S9-16"),
    ("Section 2.3; Section 5 CAP-S9-006; Section 6 FR-S9-019, FR-S9-020, FR-S9-021; Section 12 OQ-S9-19",
     "Section 2.3; Section 5 CAP-S9-006; Section 6 FR-S9-019, FR-S9-020, FR-S9-021; Section 12 OQ-S9-19"),
]

for old, new in SUBS:
    if old not in t:
        print("MISS:", old[:80])
    t = t.replace(old, new)

p.write_text(t, encoding="utf-8", newline="\n")
print("patched")

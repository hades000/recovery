"""Verify the v7 schema folder: complete table coverage, local-only FKs, no orphan statements."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "06 Data" / "Recovery Workbench Physical Schema v7"
OWN = json.load(open(ROOT / "_work" / "msr" / "plan" / "ownership.json", encoding="utf-8"))
SRC = ROOT / "06 Data" / "Recovery Workbench Physical Schema v6.sql"

LIBRARY = {"outbox_event", "outbox_delivery", "processed_event", "idempotency_key"}
owner = {k: v["owner"] for k, v in OWN["tables"].items()}

src_tables = re.findall(r"CREATE TABLE (\w+)", SRC.read_text(encoding="utf-8"))
src_index = re.findall(r"CREATE (?:UNIQUE )?INDEX \w+ ON (\w+)", SRC.read_text(encoding="utf-8"))
src_ct = re.findall(r"COMMENT ON TABLE (\w+)", SRC.read_text(encoding="utf-8"))
src_cc = re.findall(r"COMMENT ON COLUMN (\w+)\.", SRC.read_text(encoding="utf-8"))
src_ins = re.findall(r"INSERT INTO (\w+)", SRC.read_text(encoding="utf-8"))

files = sorted(OUT.glob("rwb_*.sql"))
print("files", len(files))
assert len(files) == 19

table_files = {}
fk_total = 0
problems = []
for p in files:
    t = p.read_text(encoding="utf-8")
    tabs = re.findall(r"CREATE TABLE (\w+)", t)
    fks = re.findall(r"ALTER TABLE (\w+) ADD CONSTRAINT \w+ FOREIGN KEY \(\w+\) REFERENCES (\w+)", t)
    for a, b in fks:
        fk_total += 1
        if b not in tabs:
            problems.append(f"{p.name}: FK {a}->{b} target not created in this file")
    for kind, rx in [("index", r"CREATE (?:UNIQUE )?INDEX \w+ ON (\w+)"),
                     ("comment", r"COMMENT ON (?:TABLE|COLUMN) (\w+)"),
                     ("insert", r"INSERT INTO (\w+)")]:
        for x in re.findall(rx, t):
            if x not in tabs:
                problems.append(f"{p.name}: {kind} on {x} which is not in this file")
    for x in tabs:
        table_files.setdefault(x, []).append(p.name)

print("distinct tables", len(table_files), "of", len(set(src_tables)))
for x in sorted(set(src_tables)):
    n = len(table_files.get(x, []))
    exp = 19 if x in LIBRARY else 1
    if n != exp:
        problems.append(f"table {x}: in {n} files, expected {exp}")

# every source index / comment / insert represented exactly once except library copies
def count_all(rx):
    c = {}
    for p in files:
        for x in re.findall(rx, p.read_text(encoding="utf-8")):
            c[x] = c.get(x, 0) + 1
    return c

for label, rx, src, mult in [
    ("index", r"CREATE (?:UNIQUE )?INDEX \w+ ON (\w+)", src_index, 1),
    ("comment table", r"COMMENT ON TABLE (\w+)", src_ct, 1),
    ("comment column", r"COMMENT ON COLUMN (\w+)\.", src_cc, 1),
    ("insert", r"INSERT INTO (\w+)", src_ins, 1),
]:
    got = count_all(rx)
    want = {}
    for x in src:
        want[x] = want.get(x, 0) + 1
    for x in set(list(got) + list(want)):
        # library tables repeat in 19 files
        exp = want.get(x, 0) * (19 if x in LIBRARY else 1)
        if got.get(x, 0) != exp:
            problems.append(f"{label} {x}: {got.get(x,0)} in output, expected {exp}")

print("fk total", fk_total, "(source 92; 3 cross-owner same-file pairs are cut, so 47 kept + PLT pair x19)")
print("problems", len(problems))
for x in problems[:40]:
    print("  -", x)

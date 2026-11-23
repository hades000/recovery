"""Merge the per-key scratch rows of WP B-P3-03 into the two register candidate files."""
import json

ORDER = ["E1043", "E1073", "E2004", "E2011", "E2012"]


def merge(kind, suffix):
    out, seen = [], set()
    for key in ORDER:
        path = "_work/msr/logs/B-P3-03-%s.%s.jsonl" % (key, suffix)
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if row["id"] in seen:
                    print("DUPLICATE", row["id"])
                    continue
                seen.add(row["id"])
                out.append(row)
    return out


gaps = merge("gaps", "gaps")
assumptions = merge("assumptions", "asm")

targets = (
    ("_work/msr/gaps/B-P3-03.jsonl", gaps),
    ("_work/msr/assumptions/B-P3-03.jsonl", assumptions),
)
for path, rows in targets:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(path, len(rows))

print("types", sorted({r["type"] for r in gaps}))
for t in sorted({r["type"] for r in gaps}):
    print(" ", t, sum(1 for r in gaps if r["type"] == t))
print("severities", sorted({r["severity"] for r in gaps}))
for s in sorted({r["severity"] for r in gaps}):
    print(" ", s, sum(1 for r in gaps if r["severity"] == s))
print("gap ids", [r["id"] for r in gaps])
print("asm ids", [r["id"] for r in assumptions])

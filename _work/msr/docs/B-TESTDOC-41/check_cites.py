"""Every CG-/ASM- citation in the new text must have a jsonl row, and back."""
import json
import re
from pathlib import Path

WP = "B-TESTDOC-41"
text = Path(f"_work/msr/docs/{WP}/Recovery Workbench Test Data Plan v4.md").read_text(encoding="utf-8")
ids = set()
for kind in ("gaps", "assumptions"):
    for line in Path(f"_work/msr/{kind}/{WP}.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(json.loads(line)["id"])
cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", text))
print("rows:", len(ids), "cited:", len(cited))
print("cited without a row:", sorted(cited - ids))
print("rows never cited:", sorted(ids - cited))

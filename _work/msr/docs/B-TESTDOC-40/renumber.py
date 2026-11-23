"""Renumber the per-service test IDs of the scratch markdown by section block.

6.1 keeps -01; 6.2 keeps -02; 6.3 becomes -03; 6.4 becomes -04; 6.5 becomes -05.
The file is scratch (the source .docx is never touched).
"""
import re
from pathlib import Path

P = Path(r"_work/msr/docs/B-TESTDOC-40/Recovery Workbench Non Functional Test Plan v3.md")
t = P.read_text(encoding="utf-8")

heads = ["\n## 6.3", "\n## 6.4", "\n## 6.5", "\n# 7."]
idx = [t.index(h) for h in heads]
blocks = [t[: idx[0]], t[idx[0]: idx[1]], t[idx[1]: idx[2]], t[idx[2]: idx[3]], t[idx[3]:]]

blocks[1] = re.sub(r"NFT-([A-Z0-9]+)-02", r"NFT-\1-03", blocks[1])
blocks[2] = re.sub(r"NFT-([A-Z0-9]+)-03", r"NFT-\1-04", blocks[2])
blocks[3] = re.sub(r"NFT-([A-Z0-9]+)-04", r"NFT-\1-05", blocks[3])

out = "".join(blocks)
out = out.replace(
    "| P6 rwb-comms | rwb_comms |", "| P6 rwb-comms, wave 1 | rwb_comms |")
out = out.replace(
    "A test row of a service is one of NFT-<code>-01 in 6.1, NFT-<code>-02 in 6.2 and 6.3, "
    "NFT-<code>-03 in 6.4 and NFT-<code>-04 in 6.5; a service that evaluates no rule and calls "
    "no agent has no 6.2 row.",
    "A test row of a service is one of NFT-<code>-01 in 6.1, NFT-<code>-02 in 6.2, "
    "NFT-<code>-03 in 6.3, NFT-<code>-04 in 6.4 and NFT-<code>-05 in 6.5; a service that "
    "evaluates no rule and calls no agent has no 6.2 row.")
P.write_text(out, encoding="utf-8")

ids = re.findall(r"NFT-[A-Z0-9]+-\d\d", out)
dup = sorted({i for i in ids if ids.count(i) > 1})
print("wrote", P, "ids", len(ids), "unique", len(set(ids)), "duplicates", dup)

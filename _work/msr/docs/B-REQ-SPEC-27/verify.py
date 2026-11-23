"""B-REQ-SPEC-27 verification: every v7 file keeps its source word for word, plus the four additions."""
import difflib
import os
import re

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, r"03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v6")
DST = os.path.join(ROOT, r"03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v7")

pairs = []
for n in sorted(os.listdir(SRC)):
    m = re.search(r"FSD (P\d+|S\d+) .* v(\d+)\.md$", n)
    code, ver = m.group(1), int(m.group(2))
    new = n[: n.rfind(" v")] + f" v{ver + 1}.md"
    pairs.append((n, new, code, ver))

ok = True
for old, new, code, ver in pairs:
    a = open(os.path.join(SRC, old), encoding="utf-8").read().splitlines()
    b = open(os.path.join(DST, new), encoding="utf-8").read().splitlines()
    # drop the two header lines and the blank line after them
    if b[:2] != ["SCB Collections and Recovery. Henka Group, 22 November 2026.",
                 "(C) Siam Commercial Bank and Henka Pte Ltd"]:
        print("FAIL header", new); ok = False
    body = b[3:]
    adds = []
    for line in body:
        if line.startswith("| Service |") or line.startswith("| Change |") or line.startswith("| Version |") \
                or line.startswith("| Document ID |") or line.startswith("| Status |"):
            continue
        adds.append(line)
    # rebuild source-side expectation: source with the same 5 rows projected out
    src_proj = [l for l in a if not (l.startswith("| Version |") or l.startswith("| Document ID |")
                                     or l.startswith("| Status |"))]
    note_start = [i for i, l in enumerate(body) if l.startswith("### Note, Architecture v5")]
    if not note_start:
        print("FAIL note missing", new); ok = False
        continue
    i0 = note_start[0]
    # find the end of the inserted note: the next "## " heading
    i1 = next(i for i in range(i0, len(body)) if body[i].startswith("## "))
    kept = body[:i0] + body[i1:]  # drop only the inserted note block
    kept = [l for l in kept if not (l.startswith("| Version |") or l.startswith("| Document ID |")
                                    or l.startswith("| Status |") or l.startswith("| Service |")
                                    or l.startswith("| Change |"))]
    # remove the blank line that preceded the note
    while kept and kept[0] == "":
        kept.pop(0)
    s = "\n".join(src_proj).strip("\n")
    k = "\n".join(kept).strip("\n")
    if s != k:
        ok = False
        print("DIFF", new)
        for d in list(difflib.unified_diff(s.splitlines(), k.splitlines(), lineterm=""))[:40]:
            print("   ", d)
    else:
        print("OK  ", new, f"(from v{ver})")

print("ALL OK" if ok else "PROBLEMS FOUND")

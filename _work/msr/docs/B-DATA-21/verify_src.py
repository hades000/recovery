import docx
from pathlib import Path
d = docx.Document("06 Data/Recovery Workbench Data Migration Approach v4.docx")
got = []
for el in d.element.body.iterchildren():
    tag = el.tag.split("}")[1]
    if tag == "p":
        t = "".join(n.text or "" for n in el.iter() if n.tag.endswith("}t")).strip()
        got.append(t.lstrip("\u2022 ").strip())
    elif tag == "tbl":
        for tr in el.iter():
            if tr.tag.endswith("}tr"):
                cells = ["".join(n.text or "" for n in tc.iter() if n.tag.endswith("}t")).strip()
                         for tc in tr.iter() if tc.tag.endswith("}tc")]
                got.append(" | ".join(cells))

src = Path("_work/msr/extract/B-DATA-21/Recovery Workbench Data Migration Approach v3.md").read_text(encoding="utf-8").splitlines()
# source sections 1..8 (skip the preamble table and its values? include them)
start = next(i for i, l in enumerate(src) if l.startswith("# 1."))
bad, checked = [], 0
for l in src[start:]:
    s = l.strip()
    if s.startswith("- "):
        s = s[2:].strip()
    if not s or set(s) <= set("-|: "):
        continue
    checked += 1
    if s.startswith("#"):
        s2 = s.lstrip("# ").strip()
        if not any(g == s2 for g in got):
            bad.append(s[:100])
    elif s.startswith("|"):
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not any(all(c in g for c in cells) for g in got):
            bad.append(s[:140])
    else:
        if not any(s == g or s in g for g in got):
            bad.append(s[:140])
print("SOURCE LINES CHECKED", checked, "NOT FOUND", len(bad))
for b in bad: print("  ", b)

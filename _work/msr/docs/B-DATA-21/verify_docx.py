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
missing = []
md = Path("_work/msr/docs/B-DATA-21/Recovery Workbench Data Migration Approach v4.md").read_text(encoding="utf-8").splitlines()
for l in md:
    s = l.strip()
    if not s or set(s) <= set("-|: "):
        continue
    s2 = s.lstrip("# ").strip()
    if s2.startswith("- "):
        s2 = s2[2:].strip()
    if s.startswith("|"):
        cells = [c.strip().replace("\\|", "|") for c in s.strip("|").split("|")]
        if not any(all(x in g for x in cells) for g in got):
            missing.append(s[:150])
    else:
        if not any(s2 == g or s2 in g for g in got):
            missing.append(s2[:150])
print("MISSING", len(missing))
for m in missing: print("  ", m)
print("PARAS+ROWS", len(got))
print("BACKTICKS", sum(1 for g in got if "`" in g))

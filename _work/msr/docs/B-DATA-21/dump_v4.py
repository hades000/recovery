import docx, re
from pathlib import Path
v4 = docx.Document("06 Data/Recovery Workbench Data Migration Approach v4.docx")
blocks = []
for el in v4.element.body.iterchildren():
    tag = el.tag.split("}")[1]
    if tag == "p":
        t = "".join(n.text or "" for n in el.iter() if n.tag.endswith("}t"))
        blocks.append(("p", t))
    elif tag == "tbl":
        rows = []
        for tr in el.iter():
            if tr.tag.endswith("}tr"):
                cells = []
                for tc in tr.iter():
                    if tc.tag.endswith("}tc"):
                        cells.append("".join(n.text or "" for n in tc.iter() if n.tag.endswith("}t")))
                rows.append(" | ".join(cells))
        blocks.append(("t", "\n".join(rows)))
Path("_work/msr/docs/B-DATA-21/v4_dump.txt").write_text("\n".join(f"[{k}] {v}" for k, v in blocks), encoding="utf-8")
print(len(blocks))
src = Path("_work/msr/extract/B-DATA-21/Recovery Workbench Data Migration Approach v3.md").read_text(encoding="utf-8").splitlines()
print("SRC LINES", len(src))

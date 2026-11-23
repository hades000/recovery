"""B-TECH-15 verification: fidelity of v6 to v5, structure, bounds and citations."""
import re, sys
from pathlib import Path
from pptx import Presentation

SRC = Path("05 Technical architecture/Recovery Workbench Information Flow v5.pptx")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "05 Technical architecture/Recovery Workbench Information Flow v6.pptx")
GAPS = Path("_work/msr/gaps/B-TECH-15.jsonl")
ASMS = Path("_work/msr/assumptions/B-TECH-15.jsonl")
HEAD1 = "SCB Collections and Recovery. Henka Group, 22 November 2026."
HEAD2 = "(C) Siam Commercial Bank and Henka Pte Ltd"
LOG = "6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
fails, notes = [], []


def texts(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                t = "".join(r.text for r in p.runs).strip()
                if t:
                    out.append(t)
        if getattr(sh, "has_table", False) and sh.has_table:
            for row in sh.table.rows:
                for c in row.cells:
                    for p in c.text_frame.paragraphs:
                        t = "".join(r.text for r in p.runs).strip()
                        if t:
                            out.append(t)
    return out


def titles(prs):
    return [texts(s)[0] if texts(s) else "" for s in prs.slides]


src, out = Presentation(SRC), Presentation(OUT)
st, ot = titles(src), titles(out)

# 1. every slide of version 5 is present, in order, at position +1
if len(ot) != len(st) + 11:
    fails.append(f"slide count {len(ot)} is not {len(st)} + 11")
for i, t in enumerate(st):
    if i == 0:
        continue
    if ot[i + 1] != t:
        fails.append(f"source slide {i+1} title moved or changed: {ot[i+1]!r} != {t!r}")
if ot[0] != st[0]:
    fails.append("title slide is not first")

# 2. every non-empty line of every source slide, except its page number, is in the new slide
FOOT = re.compile(r"^\d{1,2}$")
for i, s in enumerate(src.slides):
    j = i if i == 0 else i + 1
    src_lines = [t for t in texts(s) if not FOOT.match(t)]
    out_lines = set(texts(out.slides[j]))
    missing = [t for t in src_lines if t not in out_lines]
    if missing:
        fails.append(f"slide {i+1} -> {j+1}: {len(missing)} lines missing, first: {missing[0][:70]!r}")

# 3. header, change log, status
front = []
for sh in out.slides[1].shapes:
    if sh.name == "TextBox 5" and sh.has_text_frame:
        front = ["".join(r.text for r in p.runs).strip() for p in sh.text_frame.paragraphs]
if front[:2] != [HEAD1, HEAD2]:
    fails.append(f"slides 1-2 of the read-me slide are not the header: {front[:2]}")
if not any(LOG in t for t in front):
    fails.append("change-log row with D-RCV-60 and the tool line is missing")
if not any("Draft" in t for t in front):
    fails.append("status Draft missing on the read-me slide")

# 4. page numbers follow the position
for n, s in enumerate(out.slides, 1):
    for sh in s.shapes:
        if sh.name == "TextBox 3" and sh.has_text_frame and sh.text_frame.text.strip().isdigit():
            if sh.text_frame.text.strip() != str(n):
                fails.append(f"slide {n}: page number {sh.text_frame.text.strip()}")

# 5. every shape inside the slide
W, H = out.slide_width, out.slide_height
for n, s in enumerate(out.slides, 1):
    for sh in s.shapes:
        if sh.left is None:
            continue
        if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W + 1000 or sh.top + sh.height > H + 1000:
            fails.append(f"slide {n}: shape {sh.name} outside the slide")
for n, s in enumerate(out.slides, 1):
    tbls = [sh for sh in s.shapes if getattr(sh, "has_table", False) and sh.has_table]
    for sh in tbls:
        if sh.top + sh.height > 5_690_000:
            fails.append(f"slide {n}: table reaches {sh.top + sh.height}, over the note area")
    noteboxes = [sh for sh in s.shapes if sh.name == "TextBox 5"]
    for nb in noteboxes:
        if nb.top < 5_690_000 and tbls and nb.top < max(t.top + t.height for t in tbls):
            fails.append(f"slide {n}: note overlaps the table")

# 6. citations resolve
ids = set()
for p in (GAPS, ASMS):
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.add(re.search(r'"id":\s*"([^"]+)"', line).group(1))
cited = set()
for s in out.slides:
    for t in texts(s):
        cited |= set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
missing = sorted(cited - ids)
if missing:
    fails.append(f"citations with no row: {missing}")
notes.append(f"citations: {len(cited)} distinct, gaps {len(ids & cited)}")

# 7. ids.json decisions present somewhere
body = "\n".join(t for s in out.slides for t in texts(s))
for d in ["D-RCV-60", "ADR-013", "ADR-023", "DL44", "DL49"]:
    if d not in body:
        fails.append(f"decision {d} not named in the deck")

# 8. no carry-over of a person name in the document properties
cp = out.core_properties
if cp.author != "Henka Group" or cp.last_modified_by != "T3 Code / OpenCode / DeepSeek v4.1 Flash":
    fails.append(f"core properties: {cp.author!r} / {cp.last_modified_by!r}")
if cp.title != "Recovery Workbench Information Flow v6":
    fails.append(f"title property {cp.title!r}")

# 9. new slides carry real tables, not pipe text
for s in list(out.slides)[12:]:
    for t in texts(s):
        if t.startswith("|"):
            fails.append(f"pipe text on a new slide: {t[:50]}")

# 10. text dump for the edit log
Path("_work/msr/docs/B-TECH-15/v6-slide-text.txt").write_text(
    "\n".join(f"## Slide {i}\n" + "\n".join(texts(s)) for i, s in enumerate(out.slides, 1)), encoding="utf-8")
Path("_work/msr/docs/B-TECH-15/source-v5-pptx-text.txt").write_text(
    "\n".join(f"## Slide {i}\n" + "\n".join(texts(s)) for i, s in enumerate(src.slides, 1)), encoding="utf-8")


def md_slide(slide):
    title, body, rows = "", [], []
    tbl = None
    for sh in slide.shapes:
        if getattr(sh, "has_table", False) and sh.has_table:
            tbl = sh.table
        elif sh.name == "TextBox 1" and sh.has_text_frame:
            title = sh.text_frame.text.strip()
        elif sh.name == "TextBox 5" and sh.has_text_frame:
            body = ["".join(r.text for r in p.runs) for p in sh.text_frame.paragraphs]
    out = ["## " + title] + body
    if tbl is not None:
        for i, r in enumerate(tbl.rows):
            cells = [" ".join("".join(run.text for run in p.runs) for p in c.text_frame.paragraphs).strip()
                     for c in r.cells]
            out.append("| " + " | ".join(cells) + " |")
            if i == 0:
                out.append("|" + "---|" * len(cells))
    return "\n".join(out)


Path("_work/msr/docs/B-TECH-15/slides.md").write_text(
    "\n\n".join(md_slide(s) for s in list(out.slides)[12:]), encoding="utf-8")

print("\n".join(notes))
print("RESULT", "PASS" if not fails else "FAIL", len(fails))
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)

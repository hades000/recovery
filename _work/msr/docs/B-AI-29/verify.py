"""B-AI-29: verify the v3 deck against v2 and against the registers."""
import json, re, sys
from pathlib import Path
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[4]
V2 = ROOT / "08 AI and agents/Recovery Workbench AI and Agent Architecture v2.pptx"
V3 = ROOT / "08 AI and agents/Recovery Workbench AI and Agent Architecture v3.pptx"
OUT = Path(__file__).resolve().parent


def lines_of(path):
    prs = Presentation(path)
    out = []
    for n, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    t = "".join(r.text for r in p.runs).strip()
                    if t:
                        out.append((n, sh.name, t))
            elif sh.has_table:
                for row in sh.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            t = "".join(r.text for r in p.runs).strip()
                            if t:
                                out.append((n, "table", t))
    return prs, out


def main():
    p2, l2 = lines_of(V2)
    p3, l3 = lines_of(V3)
    fails = []

    def norm(x):
        return re.sub(r"\s+", " ", x).strip()

    pool = {}
    for n, sh, t in l3:
        pool.setdefault(norm(t), []).append(n)
    # every source line, except the page-number boxes, must be present verbatim
    missing, numbers = [], []
    for n, sh, t in l2:
        if sh == "TextBox 3" and t.isdigit():
            numbers.append((n, t))
            continue
        if norm(t) not in pool:
            missing.append((n, t[:70]))
    print(f"source lines (no page numbers): {len(l2) - len(numbers)}; missing in v3: {len(missing)}")
    for m in missing:
        print("  MISSING", m)
    if missing:
        fails.append("source lines missing")

    # page numbers follow the position
    bad = []
    for n, s in enumerate(p3.slides, 1):
        for sh in s.shapes:
            if sh.name == "TextBox 3" and sh.has_text_frame and sh.text_frame.text.strip().isdigit():
                if sh.text_frame.text.strip() != str(n):
                    bad.append((n, sh.text_frame.text.strip()))
    print("page-number mismatches:", bad)
    if bad:
        fails.append("page numbers")

    # header lines first on the read-me slide (after the title line)
    readme = [t for (n, sh, t) in l3 if n == 2 and sh == "TextBox 5"]
    print("slide 2 body opens:", readme[0], "|", readme[1])
    if readme[0] != "SCB Collections and Recovery. Henka Group, 22 November 2026." or \
       readme[1] != "(C) Siam Commercial Bank and Henka Pte Ltd":
        fails.append("header lines of R8.1 not first on slide 2")

    # change-log row
    if not any("3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"
               in norm(t) for (n, sh, t) in l3):
        fails.append("change-log row missing")
    if not any("Draft. No approval is recorded" in t for (n, sh, t) in l3):
        fails.append("Draft status missing")

    # citations resolve to a jsonl row
    ids = set()
    for kind in ("gaps", "assumptions"):
        for line in (ROOT / f"_work/msr/{kind}/B-AI-29.jsonl").read_text(encoding="utf-8").splitlines():
            ids.add(json.loads(line)["id"])
    text = "\n".join(t for (n, sh, t) in l3)
    cites = set(re.findall(r"\b(?:CG|ASM)-B-AI-29-\d+\b", text))
    unused = cites - ids
    print(f"citations in the deck: {len(cites)}; unresolved: {sorted(unused)}")
    if unused:
        fails.append("unresolved citations")

    # not cited in the deck
    print("rows not cited:", sorted(ids - cites))

    # no pipe text on a new slide
    pipes = [(n, t[:60]) for (n, sh, t) in l3 if n >= 13 and "|" in t]
    print("pipe text on new slides:", pipes)
    if pipes:
        fails.append("pipe text")

    # document properties
    cp = p3.core_properties
    print("props:", cp.author, "|", cp.last_modified_by, "|", cp.title, cp.revision)
    if cp.author != "Henka Group" or cp.last_modified_by != "T3 Code / OpenCode / DeepSeek v4.1 Flash":
        fails.append("document properties")

    # geometry: every shape inside the slide; table does not reach the note or the page number
    for n, s in enumerate(p3.slides, 1):
        for sh in s.shapes:
            if sh.left is None:
                continue
            if sh.left < 0 or sh.top < 0 or sh.left + sh.width > p3.slide_width or sh.top + sh.height > p3.slide_height:
                fails.append(f"slide {n}: {sh.name} outside the slide")
            if sh.has_table and sh.top + sh.height > 5640000:
                fails.append(f"slide {n}: table reaches the note area")

    # slide count
    print("slides:", len(p3.slides._sldIdLst))
    if len(p3.slides._sldIdLst) != 21:
        fails.append("slide count")

    # dump text for the record
    (OUT / "v3-slide-text.txt").write_text(
        "\n".join(f"[{n}] {sh}: {t}" for (n, sh, t) in l3), encoding="utf-8")
    (OUT / "v2-slide-text.txt").write_text(
        "\n".join(f"[{n}] {sh}: {t}" for (n, sh, t) in l2), encoding="utf-8")
    print("RESULT", "PASS" if not fails else f"FAIL {fails}")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

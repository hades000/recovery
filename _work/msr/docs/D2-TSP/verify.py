"""Verify Team Start Pack v3 against v2 (fidelity, header, change log, page numbers, fit)."""
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

ROOT = Path(__file__).resolve().parents[4]
V2 = ROOT / "12 Project communication" / "Recovery Workbench Team Start Pack v2.pptx"
V3 = ROOT / "12 Project communication" / "Recovery Workbench Team Start Pack v3.pptx"
OUT = Path(__file__).resolve().parent


def lines(prs):
    """Slide key -> list of non-empty text lines, tables row by row, page number excluded."""
    out = {}
    for i, s in enumerate(prs.slides, 1):
        got = []
        for sh in s.shapes:
            if sh.left and sh.left > 10500000 and sh.top and sh.top > 6000000:
                continue  # the page number box
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    t = "".join(r.text for r in p.runs).strip()
                    if t:
                        got.append(t)
            if sh.has_table:
                for row in sh.table.rows:
                    for c in row.cells:
                        t = " ".join(x.strip() for x in c.text.split("\n")).strip()
                        if t:
                            got.append(t)
        out[i] = got
    return out


def body(prs, pos):
    """Text lines of a slide, title excluded."""
    s = prs.slides[pos - 1]
    got = []
    for sh in s.shapes:
        if sh.top is not None and sh.top < 600000:
            continue  # the title
        if sh.left and sh.left > 10500000 and sh.top and sh.top > 6000000:
            continue
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                t = "".join(r.text for r in p.runs).strip()
                if t:
                    got.append(t)
    return got


def main():
    v2, v3 = Presentation(V2), Presentation(V3)
    a, b = lines(v2), lines(v3)
    fails = []

    (OUT / "v2-slide-text.txt").write_text(
        "\n\n".join(f"## {k}\n" + "\n".join(v) for k, v in a.items()), encoding="utf-8")
    (OUT / "v3-slide-text.txt").write_text(
        "\n\n".join(f"## {k}\n" + "\n".join(v) for k, v in b.items()), encoding="utf-8")

    if len(v3.slides) != 20:
        fails.append(f"slide count {len(v3.slides)} != 20")

    # 1. title slide kept
    if a[1] != b[1]:
        fails.append("title slide text changed")

    # 2. source slides 2..13 sit at 3..14, identical text (page number not read);
    #    the release column of source slide 4 carries the (tentative) mark
    for src in range(2, 14):
        old = [x.replace("Release (tentative)", "Release") for x in a[src]]
        new = [x.replace("Release (tentative)", "Release") for x in b[src + 1]]
        if old != new:
            misses = [x for x in old if x not in new]
            fails.append(f"source slide {src} -> position {src + 1}: {len(misses)} lines "
                         f"differ, first {misses[:1]}")

    # 3. every source line appears somewhere in v3
    flat = {x.replace("Release (tentative)", "Release") for v in b.values() for x in v}
    missing = [x for v in list(a.values())[1:] for x in v if x not in flat and not x.isdigit()]
    if missing:
        fails.append(f"{len(missing)} source lines absent: {missing[:3]}")

    # 4. header lines are the first two body lines of the read-me slide
    rm = body(v3, 2)
    if rm[:2] != ["SCB Collections and Recovery. Henka Group, 22 November 2026.",
                  "(C) Siam Commercial Bank and Henka Pte Ltd"]:
        fails.append(f"read-me header wrong: {rm[:2]}")

    # 5. change log row
    want = ("3, 22 November 2026, D-RCV-60 microservice realignment, "
            "T3 Code / OpenCode / DeepSeek v4.1 Flash")
    if not any(want in x for x in rm):
        fails.append("change-log row missing")

    # 5b. the release column is marked tentative and the eight dates are kept
    rel = b[5]
    if "Release (tentative)" not in rel:
        fails.append("release column not marked (tentative)")
    for d in ("30 Nov 2026", "31 Dec 2026", "31 Jan 2027", "28 Feb 2027", "31 Mar 2027",
              "30 Apr 2027", "31 May 2027", "30 Jun 2027"):
        if d not in rel:
            fails.append(f"release date {d} missing")

    # 6. page numbers equal position
    for pos, s in enumerate(v3.slides, 1):
        nums = [sh.text_frame.text.strip() for sh in s.shapes
                if sh.has_text_frame and sh.left and sh.left > 10500000
                and sh.top and sh.top > 6000000 and sh.text_frame.text.strip().isdigit()]
        if pos == 1:
            continue
        if nums != [str(pos)]:
            fails.append(f"slide {pos}: page number box {nums}")

    # 7. every shape inside the slide, tables above the page number
    W, H = v3.slide_width, v3.slide_height
    for pos, s in enumerate(v3.slides, 1):
        for sh in s.shapes:
            if sh.left is None:
                continue
            if sh.left < 0 or sh.top < 0 or sh.left + sh.width > W or sh.top + sh.height > H:
                fails.append(f"slide {pos}: shape {sh.name} outside the slide")
            if sh.has_table and sh.top + sh.height > Emu(6336792):
                fails.append(f"slide {pos}: table bottom {sh.top + sh.height} reaches the "
                             f"page number")

    # 8. no pipe text left on a new slide
    for pos in list(range(2, 3)) + list(range(15, 21)):
        for x in b[pos]:
            if "|" in x:
                fails.append(f"slide {pos}: pipe in text {x[:40]}")

    # 9. citations resolve
    cite = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
    ids = set()
    for kind in ("gaps", "assumptions"):
        for f in (ROOT / "_work/msr" / kind).glob("*.jsonl"):
            for line in f.read_text(encoding="utf-8").splitlines():
                m = re.search(r'"id"\s*:\s*"([^"]+)"', line)
                if m:
                    ids.add(m.group(1))
    found = {c for pos in (2, 15, 16, 17, 18, 19, 20) for x in b.get(pos, [])
             for c in cite.findall(x)}
    bad = sorted(c for c in found if c not in ids)
    if bad:
        fails.append(f"citations without a jsonl row: {bad}")

    # 10. no two shapes overlap on the new slides
    def box(sh):
        return (sh.left, sh.top, sh.left + sh.width, sh.top + sh.height)

    for pos in (2, 15, 16, 17, 18, 19, 20):
        s = v3.slides[pos - 1]
        shapes = [sh for sh in s.shapes if sh.left is not None and sh.top is not None]
        for i in range(len(shapes)):
            for j in range(i + 1, len(shapes)):
                a1, b1, c1, d1 = box(shapes[i])
                a2, b2, c2, d2 = box(shapes[j])
                if a1 < c2 and a2 < c1 and b1 < d2 and b2 < d1:
                    fails.append(f"slide {pos}: {shapes[i].name} overlaps {shapes[j].name}")

    print("slides", len(v3.slides))
    print("v2 lines", sum(len(v) for k, v in a.items() if k > 1))
    print("citations", len(found), "unresolved", len(bad))
    for f in fails:
        print("FAIL", f)
    print("RESULT", "PASS" if not fails else "FAIL", len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

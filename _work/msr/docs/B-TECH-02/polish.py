"""Layout polish for the v7 deck: move the read-me slide to position 2, match the v6 title and
footer style on the appended slides, and renumber the page footers. Content is not changed."""
import copy
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor

DECK = Path(r"05 Technical architecture\Recovery Workbench Target Architecture v7.pptx")
prs = Presentation(DECK)

def title_text(slide):
    for sh in slide.shapes:
        if sh.is_placeholder and sh.placeholder_format.idx == 0:
            return sh.text_frame.text.strip()
    return ""

# 1. move the read-me slide to position 2 (index 1) without copying the package part by hand
readme_idx = next(i for i, s in enumerate(prs.slides) if title_text(s).startswith("Read me, version 7"))
sldIdLst = prs.slides._sldIdLst
el = sldIdLst[readme_idx]
sldIdLst.remove(el)
sldIdLst.insert(1, el)

# 2. reference connector taken from an untouched v6 slide (slide 10 of the deck)
ref_conn = None
for sh in prs.slides[9].shapes:
    if sh._element.tag.endswith("cxnSp"):
        ref_conn = sh._element
        break
assert ref_conn is not None

# 3. style the appended slides
appended = [i for i, s in enumerate(prs.slides) if s.shapes and any(
    sh.is_placeholder and sh.placeholder_format.idx == 1 for sh in s.shapes)]
for i in appended:
    slide = prs.slides[i]
    for sh in slide.shapes:
        if sh.is_placeholder and sh.placeholder_format.idx == 0:
            sh.left, sh.top, sh.width, sh.height = Emu(566928), Emu(310896), Emu(11064240), Emu(502920)
            tf = sh.text_frame
            tf.word_wrap = True
            for p in tf.paragraphs:
                for r in p.runs:
                    r.font.name = "Aptos"; r.font.size = Pt(24); r.font.bold = True
                    r.font.color.rgb = RGBColor(0x4E, 0x29, 0x7F)
        elif sh.is_placeholder and sh.placeholder_format.idx == 1:
            sh.left, sh.top, sh.width, sh.height = Emu(566928), Emu(1051560), Emu(11064240), Emu(4620000)
            tf = sh.text_frame
            tf.word_wrap = True
            for p in tf.paragraphs:
                p.space_after = Pt(7)
                for r in p.runs:
                    r.font.name = "Aptos"; r.font.size = Pt(12)
    # connector under the title
    new = copy.deepcopy(ref_conn)
    ids = [int(x.get("id")) for x in slide._element.iter()
           if x.tag.endswith("}cNvPr") and (x.get("id") or "").isdigit()]
    for el in new.iter():
        if el.tag.endswith("}cNvPr"):
            el.set("id", str(max(ids or [2]) + 1))
    slide.shapes._spTree.append(new)

# 4. page footers: renumber the deck and add one to a slide that has none
FOOT = (11164824, 6336792, 640080, 320040)
for i, slide in enumerate(prs.slides, 1):
    if i == 1:
        continue
    box = None
    for sh in slide.shapes:
        if (sh.has_text_frame and not sh.is_placeholder and sh.text_frame.text.strip().isdigit()
                and sh.left == FOOT[0] and sh.top == FOOT[1]):
            box = sh
            break
    if box is None:
        box = slide.shapes.add_textbox(*[Emu(v) for v in FOOT])
        p = box.text_frame.paragraphs[0]
        r = p.add_run(); r.text = str(i)
        r.font.name = "Aptos"; r.font.size = Pt(12); r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    else:
        tf = box.text_frame
        p = tf.paragraphs[0]
        if p.runs:
            p.runs[0].text = str(i)
        else:
            p.add_run().text = str(i)

prs.save(DECK)
print("saved", len(prs.slides), "slides")

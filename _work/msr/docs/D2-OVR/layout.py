"""D2-OVR: fit the appended slides to the deck's grid, put the header slide first, renumber."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR

OUT = Path(r"12 Project communication/Recovery Workbench Project Overview v5.pptx")
PRESENT = "SCB Collections and Recovery"
NEW_TITLES = [
    "SCB Collections and Recovery. Henka Group, 22 November 2026.",
    "Realignment summary: 19 services inside ACE",
    "The 19 services, their owners and waves",
    "How the realignment touches this overview",
    "Where the realignment is written down",
]
PURPLE = RGBColor(0x4E, 0x29, 0x7F)
GREY = RGBColor(0x59, 0x59, 0x59)

prs = Presentation(OUT)
sld_ids = prs.slides._sldIdLst


def title_of(slide):
    return slide.shapes.title.text.strip() if slide.shapes.title is not None else ""


pairs = [(title_of(s), el) for s, el in zip(prs.slides, list(sld_ids))]
extra = {p[0]: p for p in pairs if p[0] in NEW_TITLES[1:]}
header = [p for p in pairs if p[0].startswith(PRESENT)]
source = [p for p in pairs if p[0] not in NEW_TITLES and not p[0].startswith(PRESENT)]
final = header + source + [extra[t] for t in NEW_TITLES[1:]]
assert len(final) == len(pairs), (len(final), len(pairs))
for el in list(sld_ids):
    sld_ids.remove(el)
for _, el in final:
    sld_ids.append(el)

print("order:")
for i, s in enumerate(prs.slides, 1):
    print(" ", i, repr(title_of(s))[:60])

for idx, slide in enumerate(prs.slides, 1):
    if title_of(slide) not in NEW_TITLES:
        continue
    title_shape = slide.shapes.title
    title_shape.left, title_shape.top = Emu(566928), Emu(310896)
    title_shape.width, title_shape.height = Emu(11064240), Emu(502920)
    tf = title_shape.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_top = Emu(72000), Emu(45720)
    tf.margin_right, tf.margin_bottom = Emu(72000), Emu(0)
    for pa in tf.paragraphs:
        for run in pa.runs:
            run.font.size = Pt(24)
            run.font.bold = True
            run.font.name = "Aptos"
            run.font.color.rgb = PURPLE

    line = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Emu(475488), Emu(877824), Emu(11716207), Emu(877824))
    line.line.color.rgb = RGBColor(0x00, 0x00, 0x00)
    line.line.width = Emu(15875)

    body = None
    for sh in slide.placeholders:
        if sh.placeholder_format.idx == 1:
            body = sh
    if body is not None:
        body.left, body.top = Emu(566928), Emu(1005840)
        body.width, body.height = Emu(11064240), Emu(4600000)
        bf = body.text_frame
        bf.word_wrap = True
        for pa in bf.paragraphs:
            pa.space_after = Pt(8)
            for run in pa.runs:
                run.font.size = Pt(14)
                run.font.name = "Aptos"
                run.font.color.rgb = GREY

    for sh in list(slide.shapes):
        if sh.has_text_frame and sh.text_frame.text.strip().isdigit():
            sh._element.getparent().remove(sh._element)
    box = slide.shapes.add_textbox(Emu(11164824), Emu(6336792), Emu(640080), Emu(320040))
    p = box.text_frame.paragraphs[0]
    p.text = str(idx)
    p.runs[0].font.size = Pt(12)
    p.runs[0].font.name = "Aptos"

prs.save(OUT)
print("SAVED", OUT, "slides:", len(prs.slides))

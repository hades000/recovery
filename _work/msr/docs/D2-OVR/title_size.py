"""D2-OVR: the document-control title line is longer, so it is set smaller than the section titles."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Pt

OUT = Path(r"12 Project communication/Recovery Workbench Project Overview v5.pptx")
prs = Presentation(OUT)
s = prs.slides[0]
t = s.shapes.title
print("title:", t.text)
for pa in t.text_frame.paragraphs:
    for run in pa.runs:
        run.font.size = Pt(18)
prs.save(OUT)
print("SAVED")

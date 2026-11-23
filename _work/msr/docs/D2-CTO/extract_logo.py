import sys
from pathlib import Path
from pptx import Presentation

src = Presentation(r"12 Project communication/Recovery Workbench Executive Presentation CTO v3.pptx")
slide = src.slides[0]
for sh in slide.shapes:
    if sh.shape_type == 13:
        blob = sh.image.blob
        ext = sh.image.ext
        out = Path(r"_work/msr/docs/D2-CTO") / f"cover_logo.{ext}"
        out.write_bytes(blob)
        print("WROTE", out, len(blob))
        break
else:
    print("NO PICTURE")

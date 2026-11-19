import sys
from pptx import Presentation
p = sys.argv[1]
prs = Presentation(p)
print("slide size", prs.slide_width, prs.slide_height)
for i, s in enumerate(prs.slides, 1):
    print("="*70)
    print("SLIDE", i, "layout:", s.slide_layout.name)
    for sh in s.shapes:
        t = sh.shape_type
        print("-- shape", sh.shape_id, sh.name, t, "ph:", (sh.placeholder_format.idx if sh.is_placeholder else None))
        if sh.has_text_frame:
            for para in sh.text_frame.paragraphs:
                if para.text.strip():
                    print("   P lvl%d: %r" % (para.level, para.text))
        if sh.has_table:
            tbl = sh.table
            for r in tbl.rows:
                print("   ROW: " + " | ".join(c.text.replace("\n"," / ") for c in r.cells))
    if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip():
        print("   NOTES:", repr(s.notes_slide.notes_text_frame.text))

import tempfile, unittest
from pathlib import Path
import docx, openpyxl
from pptx import Presentation
from pptx.util import Inches
import convert_sources as cs

class TestConvert(unittest.TestCase):
    def test_all_three(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            doc = docx.Document(); doc.add_heading("Scope", 1); doc.add_paragraph("Case owner reads ACE.")
            t = doc.add_table(rows=2, cols=2); t.cell(0, 0).text = "ID"; t.cell(0, 1).text = "Text"
            t.cell(1, 0).text = "BR-001"; t.cell(1, 1).text = "One case"; doc.save(d / "a.docx")
            prs = Presentation(); s = prs.slides.add_slide(prs.slide_layouts[5]); s.shapes.title.text = "19 services"
            tb = s.shapes.add_textbox(Inches(1), Inches(2), Inches(4), Inches(1)); tb.text_frame.text = "rwb-case owns rwb_case"
            prs.save(d / "b.pptx")
            wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Log"; ws.append(["ID", "Decision"]); ws.append(["D-RCV-36", "Drools"]); wb.save(d / "c.xlsx")
            out = d / "out"
            for f in ["a.docx", "b.pptx", "c.xlsx"]:
                cs.convert(d / f, out)
            a = (out / "a.md").read_text(encoding="utf-8"); b = (out / "b.md").read_text(encoding="utf-8"); c = (out / "c.md").read_text(encoding="utf-8")
            self.assertIn("# Scope", a); self.assertIn("| BR-001 | One case |", a)
            self.assertIn("## Slide 1: 19 services", b); self.assertIn("rwb-case owns rwb_case", b)
            self.assertIn("## Sheet: Log", c); self.assertIn("| D-RCV-36 | Drools |", c)

# tests/test_office_write.py
import json, tempfile, unittest
from pathlib import Path
import docx, openpyxl
from pptx import Presentation
import office_write as ow

class TestOffice(unittest.TestCase):
    def test_md_docx_xlsx_pptx(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d); md = d / "a.md"
            md.write_text("# Title\n\nPara one.\n\n- item\n\n| ID | Text |\n|---|---|\n| BR-1 | One |\n", encoding="utf-8")
            ow.md_docx(md, d / "a.docx")
            doc = docx.Document(d / "a.docx")
            self.assertEqual(doc.paragraphs[0].text, "Title"); self.assertEqual(doc.tables[0].cell(1, 0).text, "BR-1")
            wb = openpyxl.Workbook(); wb.active.title = "Log"; wb.save(d / "x.xlsx")
            (d / "rows.json").write_text(json.dumps([["ID", "Decision"], ["D-RCV-53", "Realign"]]))
            ow.xlsx_append(d / "x.xlsx", "New", d / "rows.json")
            self.assertEqual(openpyxl.load_workbook(d / "x.xlsx")["New"]["A2"].value, "D-RCV-53")
            Presentation().save(d / "p.pptx"); (d / "s.md").write_text("## Slide A\n- one\n- two\n", encoding="utf-8")
            ow.pptx_append(d / "p.pptx", d / "s.md")
            self.assertEqual(len(Presentation(d / "p.pptx").slides), 1)
            with self.assertRaises(SystemExit):
                ow.copy(d / "a.docx", d / "a.docx")

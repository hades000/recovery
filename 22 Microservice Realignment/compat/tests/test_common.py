import tempfile, unittest
from pathlib import Path
import common

class TestCommon(unittest.TestCase):
    def test_services(self):
        self.assertEqual(len(common.SERVICES), 19)
        self.assertEqual(common.svc("P3")["service"], "rwb-case")
        self.assertEqual(common.svc("P1")["schema"], "rwb_source_data")
        self.assertEqual(common.svc("P3")["topic"], "rwb.case.events.v1")
        self.assertEqual(common.svc("S6")["queue"], "rwb-debtsale")
        self.assertEqual(common.svc("P3")["base"], "/api/recovery/case/v1")
        self.assertEqual(common.svc("S9")["wave"], 4)

    def test_next_version(self):
        with tempfile.TemporaryDirectory() as d:
            for n in ["Recovery Workbench Release Plan v4.docx", "Recovery Workbench Release Plan v3.docx",
                      "Recovery Workbench Release Plan Extra v9.docx"]:
                (Path(d) / n).write_text("x")
            self.assertEqual(common.next_version(Path(d), "Recovery Workbench Release Plan"), 5)
            self.assertEqual(common.next_version(Path(d), "Recovery Workbench Nothing"), 1)
            self.assertEqual(common.latest_path(Path(d), "Recovery Workbench Release Plan").name,
                             "Recovery Workbench Release Plan v4.docx")

    def test_header_and_jsonl(self):
        h = common.header("22 November 2026")
        self.assertTrue(h.startswith("SCB Collections and Recovery. Henka Group, 22 November 2026."))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "a.jsonl"
            common.append_jsonl(p, {"a": 1}); common.append_jsonl(p, {"a": 2})
            self.assertEqual([r["a"] for r in common.read_jsonl(p)], [1, 2])

if __name__ == "__main__":
    unittest.main()

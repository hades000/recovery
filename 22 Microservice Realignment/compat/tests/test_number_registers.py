import json, tempfile, unittest
from pathlib import Path
import number_registers as nr

class TestNumber(unittest.TestCase):
    def test_number_dedupe_rewrite(self):
        gaps = [{"id": "CG-A-1", "title": "RPO missing", "legacy_ref": "", "severity": "P2", "wp": "A"},
                {"id": "CG-B-2", "title": "RPO  missing", "legacy_ref": "", "severity": "P1", "wp": "B"},
                {"id": "CG-B-3", "title": "Env names", "legacy_ref": "", "severity": "P3", "wp": "B"}]
        asms = [{"id": "ASM-A-1", "text": "Use programme RPO", "gap": "CG-A-1", "wp": "A"},
                {"id": "ASM-B-1", "text": "use programme rpo", "gap": "CG-B-2", "wp": "B"}]
        g, a, m = nr.number(gaps, asms)
        self.assertEqual([x["id"] for x in g], ["GAP-0001", "GAP-0002"])
        self.assertEqual(g[0]["severity"], "P1"); self.assertEqual(g[0]["raised_by"], "A; B")
        self.assertEqual(m["CG-B-2"], "GAP-0001"); self.assertEqual(m["ASM-B-1"], "ASM-0001")
        self.assertEqual(a[0]["gap"], "GAP-0001")
        self.assertEqual(nr.rewrite_text("see CG-B-3 and ASM-A-1; CG-X-9", m), "see GAP-0002 and ASM-0001; CG-X-9")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text("Not specified (CG-A-1; ASM-A-1)", encoding="utf-8")
            self.assertEqual(nr.rewrite_file(p, m), 1)
            self.assertEqual(p.read_text(encoding="utf-8"), "Not specified (GAP-0001; ASM-0001)")

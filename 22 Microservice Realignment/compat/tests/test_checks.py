import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "checks"))
import run_all as ra

def story(extra_meta="", sections=None):
    meta = "\n".join(f"| {r} | x |" for r in ra.META_ROWS)
    secs = sections or ra.SECTIONS
    body = "\n".join(f"### {i}. {s}\n\ntext\n" for i, s in enumerate(secs, 1))
    return f"# RWB-P3-E1018-APP Title\n\n| Item | Value |\n|---|---|\n{meta}\n{extra_meta}\n\n{body}\nScenario: AC1 x (legacy RWB-E1-018 AC1)\n"

class TestChecks(unittest.TestCase):
    def test_c02_c03_c05(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "RWB s.md"; p.write_text(story(), encoding="utf-8")
            self.assertEqual(ra.c02([p])[0], "PASS"); self.assertEqual(ra.c03([p])[0], "PASS"); self.assertEqual(ra.c05([p])[0], "PASS")
            p.write_text(story(sections=ra.SECTIONS[:-1]).replace("(legacy RWB-E1-018 AC1)", ""), encoding="utf-8")
            self.assertEqual(ra.c03([p])[0], "FAIL"); self.assertEqual(ra.c05([p])[0], "FAIL")

    def test_c12_names_not_printed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text("Owner: Somchai Example\n", encoding="utf-8")
            res = ra.c12([p], names={"somchai example"})
            self.assertEqual(res[0], "FAIL"); self.assertNotIn("Somchai", " ".join(res[1]))

    def test_c13(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "s.md"; p.write_text("Update the Jira issue\n", encoding="utf-8")
            self.assertEqual(ra.c13([p])[0], "FAIL")

# tests/test_make_wps.py
import unittest
import make_wps as mw

class TestWps(unittest.TestCase):
    def test_chunks_and_text(self):
        slices = [{"id": f"RWB-P3-E1{n:03d}-APP", "legacy": f"RWB-E1-{n:03d}", "epic": "RWB-SVC-P3", "lane": "L-P3-A",
                   "wt": "APP", "file": f"04/x{n}.md", "scope": "P3", "source": "04 User stories/m.md"} for n in range(1, 12)]
        wps = mw.story_wps({"slices": slices}, fanout=5)
        self.assertEqual(len(wps), 3)
        self.assertTrue(all(len(w["keys"]) <= 5 for w in wps))
        self.assertIn("fanout: 5", wps[0]["text"]); self.assertIn("04/x1.md", wps[0]["text"])
        self.assertIn("_work/msr/fragments/RWB-P3-E1001-APP.json", wps[0]["expect"])
        self.assertTrue(wps[0]["wp"].startswith("B-P3-"))

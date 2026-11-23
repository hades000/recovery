import unittest
import docgen as dg

TXT = "a\n<!-- R-TEMPLATE-BEGIN -->\n## R1\nx\n<!-- R-TEMPLATE-END -->\nb\n<!-- R-TEMPLATE-BEGIN -->\n## R3\ny\n<!-- R-TEMPLATE-END -->\n"

class TestDocgen(unittest.TestCase):
    def test_blocks(self):
        out = dg.blocks(TXT, "R-TEMPLATE")
        self.assertIn("## R1", out); self.assertIn("## R3", out); self.assertNotIn("b\n", out)
        with self.assertRaises(SystemExit):
            dg.blocks(TXT, "R-JIRA")

    def test_jira_rows(self):
        legacy = {"RWB-E1-014": {"disposition": "Retired (D-RCV-53)", "slices": []},
                  "RWB-E1-042": {"disposition": "Preserved + delta", "slices": ["RWB-P3-E1042-APP", "RWB-P3-E1042-CON", "RWB-PLT-E1042-CON"]},
                  "N001": {"disposition": "New", "slices": ["RWB-PLT-N001-CON"]}}
        rows = dg.jira_rows(legacy)
        act = {r[0]: r[2] for r in rows}
        self.assertTrue(act["RWB-E1-014"].startswith("Close"))
        self.assertTrue(act["RWB-E1-042"].startswith("Keep"))
        self.assertTrue(act["N001"].startswith("Create"))
        self.assertEqual([r for r in rows if r[0] == "RWB-E1-042"][0][3], 2)

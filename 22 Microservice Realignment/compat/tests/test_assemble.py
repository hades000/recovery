import unittest
import assemble as asm

class TestAssemble(unittest.TestCase):
    def test_prd_ref_and_demote(self):
        prd = "| FR-P3-001 | Open a case | REQ-CAS-001, REQ-CAS-002 |\n| FR-P3-002 | Close | REQ-CAS-009 |\n"
        m = asm.fr_map(prd)
        self.assertEqual(m["REQ-CAS-002"], ["FR-P3-001"])
        self.assertEqual(asm.prd_value("03/PRD/x.md", ["REQ-CAS-001", "REQ-CAS-009"], m), "03/PRD/x.md (FR-P3-001, FR-P3-002)")
        self.assertTrue(asm.prd_value("03/PRD/x.md", ["REQ-ZZZ-001"], m).startswith("03/PRD/x.md (no FR mapped"))
        self.assertEqual(asm.demote("# A\n### 1. Story\n"), "### A\n##### 1. Story\n")

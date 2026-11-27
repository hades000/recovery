"""Tests for dorcheck.py on synthetic stories with stubbed sources. Run: python -I -B test_dorcheck.py"""
import shutil, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dorcheck, rulings  # noqa: E402
from detcheck import Story  # noqa: E402

STORY = """# RWB-P3-E9001-APP Demo story

| Item | Value |
|---|---|
| Story key | RWB-P3-E9001-APP |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Legacy key | RWB-E9-001 |
| PRD reference | PRD-P3 |
| Build status | Not started |
| Ready to start | After RWB-P3-E9002-APP |
| Depends on (build) | RWB-P3-E9002-APP, RWB-P3-E9001-CON |

### 1. Story

As a **Collector**, I want to open a case, so that recovery starts.

### 4. Flow

1. The collector opens the case.

### 5. Exception paths

| ID | Trigger | Handling | Covered by |
|---|---|---|---|
| EX1 | Account closed | Refuse | AC1 |
| EX2 | Duplicate open | Refuse | none |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Yes |
| Negotiable | Yes |
| Valuable | Yes |
| Estimable | Yes |
| Small | Fits two weeks |
| Testable | Yes |

### 7. Acceptance criteria

```gherkin
Scenario: AC1 open a case
  Given an account in arrears
  When the collector opens a case
  Then the case status is New
Scenario: AC2 no assertion
  Given an account
  When the collector opens a case
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A case starts New | BRD |
| BR2 | Closed accounts are refused | BRD |

### 9. State transitions

| From | Event | To |
|---|---|---|
| New | Close | Closed |

### 10. Authority

| Role | Action |
|---|---|
| RW-COL | Open |

### 11. Data

| Field | BR Field ID |
|---|---|
| case_no | DF-CASE-001 |

### 14. Validation and messages

| ID | Message |
|---|---|
| MSG-P3-001 | Account closed |

### 15. Screens and states

SCR-01 case screen.

### 16. Test cases

| TC | Covers | Level | Data |
|---|---|---|---|
| TC-1 | AC1, BR1 | Unit | account A |

### 17. Guardrails

- No personal data in logs.

### 18. Traceability

| Feature | L3 process |
|---|---|
| Case opening | Open case |

### 19. Out of scope

- Closing a case.
"""


class Src:
    unread = []

    def case_model(self):
        st = [{"Status": s} for s in ("New", "Assigned", "Closed")]
        return st, [{"From": "New", "Event": "Assign", "To": "Assigned"}]

    def lov(self):
        return {}, {}

    def ldm_fields(self, prev=False):
        return [{"BR Field ID": "DF-CASE-001"}]


class DorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        p = self.tmp / "RWB P3 E9001 APP Demo story v1.md"
        p.write_text(STORY, encoding="utf-8")
        idx = {"RWB-P3-E9002-APP": ("x", "Not started"), "RWB-P3-E9001-CON": ("y", "Done")}
        det = [{"id": "CG-T-101", "check": "X8", "severity": "P2", "title": "message text differs", "story": "RWB-P3-E9001-APP"}]
        self.rv = dorcheck.Review(Story(p), Src(), det, {}, idx, ({"RW-COL"}, {"collector"})).run()
        self.res = {it["no"]: it["result"] for it in self.rv.items.values()}

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_items(self):
        r = self.res
        self.assertEqual(r[1], "Pass")                     # role name is in the roles table
        self.assertEqual(r[3], "Fail")                     # AC2 has no Then; EX2 has no criterion
        self.assertEqual(r[4], "Partial")                  # BR2 has no criterion or test
        self.assertEqual(r[5], "Fail")                     # New -> Closed is not in the case model
        self.assertEqual(r[7], "Pass")
        self.assertEqual(r[9], "Partial")                  # the detcheck X8 row folds into item 9
        self.assertEqual(r[12], "Fail")                    # AC2 has no test case
        self.assertEqual(r[16], "Fail")                    # no size
        self.assertEqual(r[21], "Pass")                    # the CON story is Done
        self.assertEqual(self.rv.verdict, "NOT READY")

    def test_ac_review_and_missing(self):
        self.assertIn("AC2", self.rv.acr)
        covers = " ".join(c for c, _ in self.rv.missing)
        self.assertIn("EX2", covers)
        self.assertIn("BR2", covers)

    def test_rulings_reads_the_report(self):
        rdir = self.tmp / "out"
        (rdir / "review").mkdir(parents=True)
        (rdir / "review" / "RWB-P3-E9001-APP.md").write_text(self.rv.md(), encoding="utf-8")
        cap = rulings.Capture(self.tmp, self.tmp, [rdir], "none")
        cap.review_rows(rdir)
        ids = set(cap.items)
        self.assertIn("DOR-RWB-P3-E9001-APP-3", ids)
        self.assertNotIn("DOR-RWB-P3-E9001-APP-1", ids)    # Pass rows are not captured
        self.assertIn("ACR-RWB-P3-E9001-APP-AC2", ids)
        self.assertEqual(cap.items["ACR-RWB-P3-E9001-APP-AC2"]["Proposed fix"], "")
        self.assertTrue(any(i.startswith("NEWAC-RWB-P3-E9001-APP-") for i in ids))


if __name__ == "__main__":
    unittest.main()

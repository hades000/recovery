import tempfile, unittest
from pathlib import Path
import legacy_index as li

MASTER = """# Recovery Workbench User Stories Epics 3 to 8 v3

## RWB-E4-001 Order an appraisal when the last one is stale

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Depends on | RWB-E1-018, FEAT-RDF-06 |
| Requirement IDs | REQ-VAL-001 |

**Story.** As a case owner, I want ...

**Acceptance criteria**

~~~gherkin
  Scenario: AC1 Order an appraisal
    Given x
  Scenario: AC2 Not recorded
    Then the user sees MSG-P7-003
~~~

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-001-01 | AC1 | API | x |

## RWB-E4-002 Second

| Item | Value |
|---|---|
| Epic | E4, release 28 February 2027 |
| Module | S1 Valuation and route |
| Depends on | None |
"""

class TestIndex(unittest.TestCase):
    def test_parse(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "m.md"; p.write_text(MASTER, encoding="utf-8")
            rows = li.parse_master(p, "E3-8")
            self.assertEqual([r["key"] for r in rows], ["RWB-E4-001", "RWB-E4-002"])
            r = rows[0]
            self.assertEqual(r["module"], "S1"); self.assertEqual(r["release"], "28 February 2027")
            self.assertEqual(r["deps"], ["RWB-E1-018"]); self.assertEqual(r["feat_deps"], ["FEAT-RDF-06"])
            self.assertEqual(r["acs"], ["AC1", "AC2"]); self.assertEqual(r["tcs"], ["TC-E4-001-01"])
            self.assertEqual(r["reqs"], ["REQ-VAL-001"]); self.assertEqual(r["business_epic"], "EP04")
            self.assertIn("Story", r["sections"]); self.assertEqual(len(r["sha256"]), 64)
            self.assertEqual(rows[1]["deps"], [])

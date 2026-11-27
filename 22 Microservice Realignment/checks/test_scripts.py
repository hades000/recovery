"""Tests for detcheck.py and apply_fixes.py on a synthetic document set (no project file is read or written).
Run: python -I test_scripts.py
"""
import json, re, shutil, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import detcheck, apply_fixes, rwbsrc, mkfixes, pipeline

SHEETS = {
 "refdata": """## Sheet: Lists

| Lists of values |  |  |
|---|---|---|
| List | Kind | Owner |
| LOV-CASE-STATUS | Closed list | CoE |
| LOV-PRODUCT | Closed list | Heads |

## Sheet: Values

| Values |  |  |
|---|---|---|
| List | Code | English label |
| LOV-CASE-STATUS | NEW | New |
| LOV-CASE-STATUS | ASSIGNED | Assigned |
| LOV-CASE-STATUS | CLOSED | Closed |
| LOV-PRODUCT | MORTGAGE | Mortgage |
""",
 "casemodel": """## Sheet: Case status

| Case status |  |  |
|---|---|---|
| Status | Meaning | CMMN case state |
| New | n | Active |

## Sheet: Status transitions

| Status transitions |  |  |
|---|---|---|
| From | Event | To |
| New | Allocation rule matched | Assigned |
| Assigned | Closed by milestone | Closed |
""",
 "ldm": """## Sheet: Fields

| Data dictionary |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| BR Field ID | Entity | Field | Data type | List of values | Source field | Personal data |
| DF-CAS-001 | recovery_case | id | TEXT | None | None | No |
| DF-CAS-002 | recovery_case | case_no | TEXT | None | None | No |
| DF-CAS-003 | recovery_case | primary_person_key | TEXT | None | None | Yes |
| DF-CAS-004 | recovery_case | status | TEXT | LOV-CASE-STATUS | None | No |
| DF-CAS-005 | recovery_case | product_group | TEXT | LOV-PRODUCT | None | No |
| DF-CAS-006 | case_account | account_key | TEXT | None | None | Yes |
""",
 "ldm_prev": """## Sheet: Fields

| BR Field ID | Entity | Field | Data type | List of values | Source field | Personal data |
|---|---|---|---|---|---|---|
| DF-CAS-003 | recovery_case | old_key | TEXT | None | None | Yes |
""",
 "dclass": """## Sheet: Fields

| Every field |  |  |  |  |
|---|---|---|---|---|
| BR Field ID | Entity | Field | Personal data category | Classification | Personal data |
| DF-CAS-002 | recovery_case | case_no | Indirect identifier | Confidential | Yes |
| DF-CAS-001 | recovery_case | id | Not personal | Internal | No |
""",
 "declog": """## Sheet: Open decisions

| Open |  |  |  |  |  |
|---|---|---|---|---|---|
| ID | Topic | Question | Options | Recommendation | Owner |
| DL17 | One case | What is one case? | A: per customer. B: per account. | A. | Product owner |
| DL16 | Threshold | 90 or 91? | A: 90. B: 91. | A. | Business lead |

## Sheet: Decisions taken

| ID | Decision | Date |
|---|---|---|
| D-RCV-30 | Primary account is the opening account | 2026-11-06 |
""",
 "kafka": """## Sheet: Events

| Event types |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| EV row | Event | Event type (ce_type) | Topic | Payload | Consumers | Owner code |
| EV-01 | CaseCreated | rwb.case.CaseCreated.v1 | rwb.case.events.v1 | caseId, caseNo | rwb-agent | P3 |
| EV-08 | DecisionRecorded | rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | entryId, caseId | rwb-decision | P7 |
| EV-26 | AceDataReady | rwb.source-data.AceDataReady.v1 | rwb.source-data.events.v1 | businessDate | rwb-reporting | P1 |
""",
 "temporal": """## Sheet: Workflows

| Workflow | Kind | Service | Task queue | Started by |
|---|---|---|---|---|
| CaseWorkflow | Parent | rwb-case | rwb-case | inbox; workflow ID = case ID (ADR-011 writes case-{caseId}, see GAP-0148) |
| DailyCaseRun | Event-started | rwb-case | rwb-case | AceDataReady |

## Sheet: Activities

| Activity | Kind | Service | Task queue |
|---|---|---|---|
| EvaluateRules | Activity | every service | rwb-<short> |

## Sheet: Platform rules

| Rule | Value |
|---|---|
| History | 51,200 events |
""",
 "msgstd": """# 4. The core messages

| ID | Type | Raised when | English | Thai, proposed |
|---|---|---|---|---|
| MSG-P1-001 | Warning | Data product stale | {product} is from {date}. Today's load has not arrived. | t |
| MSG-P3-030 | Info | A scheduled job ran after a missed run | {job} ran for {date} after a missed run. | t |
| MSG-P4-002 | Error | Outside permission | You cannot {action} here. Your role does not include it. | t |
""",
 "tc": """## Sheet: Story test cases

| Test cases |  |  |
|---|---|---|
| Test case | Story | Covers | Given | When | Expected result |
| TC-E9-001-01 | RWB-E9-001 | AC1 | g | w | t |
| TC-E9-001-02 | RWB-E9-001 | AC9 | g | w | t |
""",
 "rtm": """## Sheet: RTM

| Requirements traceability |  |
|---|---|
| ID | Requirement | Priority | Epic | Module | Feature | F | Legacy | FSD | TSD | Tests |
| REQ-X-001 | r | Must | E9 | P3 | F | f | RWB-E9-001 | a | b | TC-E9-001-01, TC-E9-001-02 |
""",
 "rules": """## Sheet: Rules

| Rule ID | Rule |
|---|---|
| R-UNI-39 | Block the action and raise an incident |
""",
 "storydefects": """## Sheet: Defects

| Defects |  |  |  |
|---|---|---|---|
| Story | Step | What contradicts what | Status |
| RWB-E9-001 | 3 | step 3 contradicts AC2 | Open |
| RWB-E9-001 | 4 | fixed thing | Closed |
""",
}

YAML_CASE = """openapi: 3.1.0
info:
  description: >-
    This document holds 2 operations under REST base /api/recovery/case/v1; schema rwb_case.
paths:
  /cases:
    get:
      summary: list
  /cases/{caseId}:
    get:
      summary: one
components:
  schemas:
    Case:
      properties:
        status:
          type: string
          enum:
          - NEW
          - CLOSED
"""
YAML_SRC = """openapi: 3.1.0
info:
  description: >-
    REST base /api/recovery/source-data/v1; schema rwb_source_data.
paths:
  /data-products/freshness:
    get:
      summary: f
"""

BAD = """# RWB-P3-E9001-APP Bad story v1

| Item | Value |
|---|---|
| Story key | RWB-P3-E9001-APP |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Legacy key | RWB-E9-001 |
| Depends on (build) | RWB-P3-E9001-CON, RWB-P7-E9999-CON |
| PRD reference | PRD P3 (FR-P3-001, FR-P3-002, FR-P3-077) |

**Change log.** D-RCV-60, 22 November 2026: split. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

Parameter `case.entry.dpd` = 90 (DL17, DL16). Field IDs are those in the Logical Data Model and Data Dictionary v8.
Rule R-UNI-39 and R-UNI-99 apply. The story cites GAP-0001 and GAP-0999 and ASM-0001.

### 4. Flow

1. rwb-source-data: reads `recovery.v_ace_account` for the date.
2. rwb-case: reads v_ace_customer for the borrower.

### 7. Acceptance criteria

```gherkin
Feature: f

  Scenario: AC2 Status as data
    Given the list LOV-CASE-STATUS gains the value "WAITING_COURT" through a list load
    Given v_ace_account holds account A-1
    Given the rwb-decision contract mock returns rule ID "EXCL-777"
    When JOB-02 runs
    Then the job record lists A-1
    Then the case service accepts the value without a code change

  Scenario: AC3 Other
    Given x
    When y
    Then z
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Links by `primary_customer_id` and `mystery_col` | DL17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | AceDataReady | c | New |
| New | CaseWorkflow started with the case ID | c | Active |
| New | Something | c | Closed |

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-003 | recovery_case | all | Write |
| DF-CAS-004 to DF-CAS-006 | recovery_case | all | Write |

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | list | R | n |
| GET | `/cases/{caseId}/parties` | parties | R | n |

Errors: 401 no session (MSG-P4-001), 403 no right (MSG-P4-002), 503 store down.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/freshness` | P1 | f | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 | f | 2 s |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 | a | 2 s |

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | caseId | caseId, caseNo |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId | caseId |

Both carry no personal data.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1` | P1 | router |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, workflow ID = case ID) | `rwb-case` | p |
| DailyCaseRun | Workflow started by AceDataReady | `rwb-case` | p |
| EvaluateRules | Activity | `rwb-case` | p |
| MysteryActivity | Activity | `rwb-case` | p |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case.creation`.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-02 | `recovery_svc` login | One login | none |

- Constraint: partial unique index `ux_x ON recovery_case (primary_customer_id, product_group) WHERE closed_date IS NULL`.
- Migrations: `V1018_1__case_creation.sql` and `V0002__ok.sql` in `rwb_case`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | waiting | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P3-030 | bad request | The request could not be read: {detail}. |
| MSG-P4-002 | no right | You cannot {action} here. Your role does not include it. |
| MSG-P9-999 | x | y |

### 15. Screens and states

SCR-02 Case list (Loading; empty; list) shows cases.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E9-001-01 | AC2 | E2E | `v_ace_account` A-1 |
| TC-E9-001-02 | AC9 | E2E | d |
| TC-E9-001-15 | AC2 | E2E | d |

The full test is in Recovery Workbench Test Cases v7.xlsx.

### 17. Guardrails

- No personal data in logs. The run reads `account_key` only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-X-001 | r | b | f | l | r | TC-E9-001-01 |
"""

CLEAN = """# RWB-P3-E9001-CON Clean story v1

| Item | Value |
|---|---|
| Story key | RWB-P3-E9001-CON |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Legacy key | RWB-E9-002 |
| PRD reference | PRD P3 (FR-P3-001) |

**Change log.** D-RCV-60, 22 November 2026: split. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

Reads `case_no` and `primary_person_key` of `recovery_case`. Cites the Logical Data Model and Data Dictionary v9.

### 7. Acceptance criteria

```gherkin
Feature: f

  Scenario: AC1 Read a case
    Given the rwb-source-data contract fake returns account A-1
    When GET /cases runs
    Then status "NEW" is returned
```

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| New | Allocation rule matched | c | Assigned |

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{id}` | one | R | n |

Errors: 403 no right (MSG-P4-002).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | caseId | caseId, caseNo |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| DailyCaseRun | Workflow, workflow ID = daily-{businessDate} | `rwb-case` | p |
| EvaluateRules | Activity | `rwb-case` | p |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.cases`. Migration `V0003__x.sql`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | no right | You cannot {action} here. Your role does not include it. |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E9-001-01 | AC1 | E2E | fake |
"""


def build_root(base):
    root = base / "root"
    cache = base / "cache"
    cache.mkdir(parents=True)
    for k, txt in SHEETS.items():
        (cache / (Path(rwbsrc.SOURCES[k]).stem + ".md")).write_text(txt, encoding="utf-8")
    def w(rel, txt):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")
    w(rwbsrc.TEXT["docindex"], "| 11 | LDM | Recovery Workbench Logical Data Model and Data Dictionary v9.xlsx |\n"
                               "| 96 | TC | Recovery Workbench Test Cases v8.xlsx |\n")
    w(rwbsrc.TEXT["gapreg"], "| GAP ID | Title | Description | Status |\n|---|---|---|---|\n"
                             "| GAP-0001 | one | about RWB-E9-001 | Open |\n"
                             "| GAP-0002 | two | about RWB-E9-001 and primary_customer_id | Open |\n"
                             "| GAP-0003 | three | other story | Open |\n"
                             "| GAP-0004 | four | RWB-E9-001 AC gives rule ID 'EXCL-777' from no source | Open |\n")
    w(rwbsrc.TEXT["asmreg"], "| ASM ID | Text |\n|---|---|\n| ASM-0001 | DL16 built on A |\n")
    w(rwbsrc.TEXT["screens"], "## SCR-02 Case list\n\nStates: loading, empty, error.\n")
    w(rwbsrc.TEXT["params"], "")
    w(rwbsrc.TEXT["apidir"] + "/rwb-case.yaml", YAML_CASE)
    w(rwbsrc.TEXT["apidir"] + "/rwb-source-data.yaml", YAML_SRC)
    w(rwbsrc.TEXT["prddir"] + "/Recovery Workbench PRD P3 rwb-case v1.md",
      "| ID | Requirement |\n|---|---|\n| FR-P3-001 | Create cases |\n| FR-P3-002 | One |\n| FR-P3-002 | Two |\n")
    w("05 Technical architecture/Other v1.md", "The case.entry.dpd_threshold parameter is 90.\n")
    w("_work/msr/gaps/OLD.jsonl", json.dumps({"id": "CG-OLD-1", "legacy_ref": "RWB-E9-001",
                                               "title": "MSG-P1-001 wording"}) + "\n")
    sd = root / rwbsrc.TEXT["stories"] / "RWB-SVC-P3 rwb-case"
    sd.mkdir(parents=True)
    (sd / "RWB P3 E9001 APP Bad story v1 v1.md").write_text(BAD, encoding="utf-8")
    (sd / "RWB P3 E9001 CON Clean story v1 v1.md").write_text(CLEAN, encoding="utf-8")
    return root, cache, sd


class DetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="dettest-", dir=str(HERE.parent)))
        cls.root, cls.cache, cls.sd = build_root(cls.tmp)
        cls.out = cls.tmp / "out"
        detcheck.main(["--root", str(cls.root), "--cache", str(cls.cache), "--out", str(cls.out), "--wp", "T",
                       "--story", str(cls.sd / "RWB P3 E9001 APP Bad story v1 v1.md"),
                       str(cls.sd / "RWB P3 E9001 CON Clean story v1 v1.md")])
        cls.rows = [json.loads(l) for l in (cls.out / "gaps.jsonl").read_text(encoding="utf-8").splitlines()]
        cls.asms = [json.loads(l) for l in (cls.out / "assumptions.jsonl").read_text(encoding="utf-8").splitlines()]
        cls.rep = json.loads((cls.out / "report.json").read_text(encoding="utf-8"))
        cls.bad = [r for r in cls.rows if r["story"] == "RWB-P3-E9001-APP"]
        cls.clean = [r for r in cls.rows if r["story"] == "RWB-P3-E9001-CON"]

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def has(self, check, *words, rows=None):
        rows = self.bad if rows is None else rows
        hit = [r for r in rows if r["check"] == check and all(w in r["title"] + r["description"] for w in words)]
        self.assertTrue(hit, f"{check} {words} not raised; got {[r['title'] for r in rows if r['check'] == check]}")
        return hit[0]

    def test_no_check_errors(self):
        for k, v in self.rep["stories"].items():
            self.assertNotIn("check_errors", v, v.get("check_errors"))

    def test_clean_story_raises_nothing(self):
        # the only WP-level row (empty catalog) is written once, by the first story that reads a key
        self.assertEqual([r["title"] for r in self.clean], [])

    def test_x1(self):
        r = self.has("X1", "'Active'")
        self.assertEqual(r["severity"], "P1")
        self.has("X1", "WAITING_COURT", "LOV-CASE-STATUS")
        self.has("X1", "New -> Closed")
        self.assertFalse([r for r in self.bad if r["check"] == "X1" and "'New'" in r["title"]])

    def test_x3(self):
        r = self.has("X3", "primary_customer_id", "Index")
        self.assertEqual((r["type"], r["severity"]), ("Conflict", "P1"))
        self.assertIn("primary_person_key", r["description"])
        self.has("X3", "mystery_col")
        self.has("X3", "DF-CAS-004 to DF-CAS-006")
        self.assertFalse([r for r in self.bad if r["check"] == "X3" and ("DF-CAS-001 to" in r["title"] or "recovery_svc" in r["title"] or "rwb_case" in r["title"])])
        self.assertFalse([r for r in self.bad if r["check"] == "X3" and r["token"] == "primary_customer_id" and "Name `" in r["title"]],
                         "index column reported twice")

    def test_x4(self):
        self.has("X4", "parameter-catalog.csv is empty")
        r = self.has("X4", "case.entry.dpd_threshold")
        self.assertEqual(r["type"], "ID collision")
        self.assertEqual(sum(1 for r in self.rows if "parameter-catalog.csv is empty" in r["title"]), 1)

    def test_x5(self):
        self.has("X5", "GET /cases/{caseId}/parties")
        self.has("X5", "/api/recovery/source-data/v1/freshness")
        self.has("X5", "/api/recovery/source-data/v1/accounts/{id}")
        self.assertFalse([r for r in self.bad if r["check"] == "X5" and "data-products/freshness" in r["title"]])
        self.has("X5", "503 store down")
        self.has("X5", "RWB-P7-E9999-CON")
        self.has("X5", "closed enum")
        self.assertFalse([r for r in self.bad if "RWB-P3-E9001-CON" in r["title"]])

    def test_x6(self):
        r = self.has("X6", "rwb.decision.DecisionRecorded.v1")
        self.assertEqual(r["fix"]["pairs"], [["rwb.decision-record.DecisionRecorded.v1", "rwb.decision.DecisionRecorded.v1"]])
        self.has("X6", "Two workflow ID forms for CaseWorkflow")
        self.has("X6", "DailyCaseRun are not stated")
        self.has("X6", "MysteryActivity")
        self.assertFalse([r for r in self.bad if "EvaluateRules" in r["title"]])
        self.assertTrue(any(a["gap"] for a in self.asms if "workflow ID" in a["text"]))

    def test_x7(self):
        self.has("X7", "R-UNI-99")
        r = self.has("X7", "EXCL-777")  # still raised although the Gap Register names it
        self.assertIn("GAP-0004", json.dumps(r))
        self.assertFalse([r for r in self.bad if "R-UNI-39" in r["title"]])

    def test_x8(self):
        r = self.has("X8", "MSG-P1-001")
        self.assertEqual(r["type"], "Conflict")
        self.assertEqual(r["fix"]["new"], "{product} is from {date}. Today's load has not arrived.")
        r = self.has("X8", "MSG-P3-030")
        self.assertEqual(r["type"], "ID collision")
        self.has("X8", "MSG-P9-999")
        self.assertFalse([r for r in self.bad if "MSG-P4-002" in r["title"]])

    def test_x9(self):
        self.has("X9", "TC-E9-001-15")
        self.has("X9", "AC9")             # TC for a criterion the story does not own
        self.has("X9", "AC3")             # criterion with no TC
        self.has("X9", "RTM v7")

    def test_x10_x11_x12(self):
        self.has("X10", "caseNo")
        self.has("X11", "'case'")
        self.has("X11", "V1018_1__case_creation.sql")
        self.assertFalse([r for r in self.bad if "V0002__ok.sql" in r["title"]])
        r = self.has("X12", "ACE views")
        self.assertIn("v_ace_customer", r["evidence"])
        self.assertNotIn("recovery.v_ace_account for the date", r["evidence"])  # the P1 step is allowed
        self.has("X12", "legacy job")

    def test_x16_x17_x19_x20_x2(self):
        self.has("X16", "FR-P3-077")
        self.has("X16", "FR-P3-002", "meanings")
        self.has("X17", "SCR-02", "error", "no access")
        self.has("X19", "GAP-0999")
        self.assertFalse([r for r in self.bad if "GAP-0001" in r["title"] or "ASM-0001" in r["title"]])
        r = self.has("X20", "Data Dictionary v8", "Test Cases v7")
        self.assertEqual(sorted(map(tuple, r["fix"]["pairs"])),
                         [("Logical Data Model and Data Dictionary v8", "Logical Data Model and Data Dictionary v9"),
                          ("Test Cases v7", "Test Cases v8")])
        self.has("X2", "DL17")
        self.assertFalse([r for r in self.bad if r["check"] == "X2" and "DL16" in r["title"]])
        self.assertTrue(any("A." in a["text"] and "DL17" in a["text"] for a in self.asms))

    def test_report(self):
        rep = self.rep["stories"]["RWB-P3-E9001-APP"]
        self.assertEqual([x.split()[0] for x in rep["uncited_register_gaps"]], ["GAP-0002", "GAP-0004"])
        self.assertEqual(len(rep["open_defects"]), 1)

    def test_related(self):
        r = self.has("X3", "primary_customer_id", "Index")
        self.assertIn("GAP-0002", r.get("related", []))
        r = self.has("X8", "MSG-P1-001")
        self.assertIn("CG-OLD-1", r.get("related", []))

    def test_row_format(self):
        need = ["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
                "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]
        for r in self.rows:
            for k in need:
                self.assertIn(k, r)
            self.assertIn(r["type"], ("Missing", "Conflict", "Ambiguous", "Outdated", "ID collision"))
            self.assertIn(r["severity"], ("P1", "P2", "P3"))
        ids = [r["id"] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_parallel_matches_serial(self):
        out2 = self.tmp / "out_par"
        detcheck.main(["--root", str(self.root), "--cache", str(self.cache), "--out", str(out2), "--wp", "T", "--jobs", "2",
                       "--story", str(self.sd / "RWB P3 E9001 APP Bad story v1 v1.md"),
                       str(self.sd / "RWB P3 E9001 CON Clean story v1 v1.md")])
        for f in ("gaps.jsonl", "assumptions.jsonl", "cited.jsonl"):
            self.assertEqual((self.out / f).read_text(encoding="utf-8"), (out2 / f).read_text(encoding="utf-8"), f)

    def test_refuses_out_inside_root(self):
        with self.assertRaises(SystemExit):
            detcheck.main(["--root", str(self.root), "--cache", str(self.cache), "--out", str(self.root / "x"),
                           "--story", str(self.sd / "RWB P3 E9001 CON Clean story v1 v1.md")])


class ApplyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="applytest-", dir=str(HERE.parent)))
        self.root = self.tmp / "root"
        (self.root / "d").mkdir(parents=True)
        self.f = self.root / "d" / "Story x v1 v1.md"
        self.f.write_text("# T\n\n**Change log.** D-RCV-60, 22 November 2026: split.\n\nline a\nline b\nfoo foo\n", encoding="utf-8")
        self.out = self.tmp / "out"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_fixes(self, fixes, *extra):
        p = self.tmp / "fixes.jsonl"
        p.write_text("\n".join(json.dumps(f) for f in fixes), encoding="utf-8")
        return apply_fixes.main(["--root", str(self.root), "--fixes", str(p), "--out", str(self.out), *extra])

    def result(self):
        return [json.loads(l) for l in (self.out / "apply_result.jsonl").read_text(encoding="utf-8").splitlines()]

    def test_plain_change_log_style(self):
        self.f.write_text("# T\n\nChange log: D-RCV-60 (realignment v1), 22 November 2026.\n\nfoo\n", encoding="utf-8")
        self.assertEqual(self.run_fixes([{"fix_id": "F1", "finding": "X", "file": "d/Story x v1 v1.md", "op": "replace",
                                          "old": "foo", "new": "bar"}]), 0)
        txt = (self.out / "d" / "Story x v1 v2.md").read_text(encoding="utf-8")
        self.assertIn("\nChange log: D-RCV-60, 26 November 2026:", txt)
        self.assertNotIn("**Change log.**", txt)

    def test_table_change_log_style(self):
        self.f.write_text("# T\n\n| Version | Date | Change | Tool |\n|---|---|---|---|\n| v1 | 22 November 2026 | split | x |\n"
                          "\n### 1. Story\n\nfoo\n", encoding="utf-8")
        self.assertEqual(self.run_fixes([{"fix_id": "F1", "finding": "X", "file": "d/Story x v1 v1.md", "op": "replace",
                                          "old": "foo", "new": "bar"}]), 0)
        txt = (self.out / "d" / "Story x v1 v2.md").read_text(encoding="utf-8")
        self.assertIn("| v1 | 22 November 2026 | split | x |\n| v2 | 26 November 2026 | D-RCV-60: fixes from the "
                      "build-readiness review (X) | T3 Code / OpenCode / DeepSeek v4.1 Flash |\n\n### 1. Story", txt)

    def test_workbook_column_row_and_cell_ops(self):
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Decisions taken"
        ws.append(["title"]); ws.append([]); ws.append(["ID", "Decision", "What it means"])
        ws.append(["D-1", "uses Doc v4", "x"]); ws.append(["D-2", "other", "y"])
        rm = wb.create_sheet("Read me")
        for v in ("Doc v1.", "Change log", "v1, 1 November 2026", "Source: z"):
            rm.append([v])
        ws["C3"].font = openpyxl.styles.Font(bold=True)
        wb.save(self.root / "d" / "Log v1.xlsx")
        fx = [{"fix_id": "A", "file": "d/Log v1.xlsx", "op": "xlsx_set_cell", "sheet": "Read me", "cell": "A4",
               "old": "Source: z", "new": "Source: w"},
              {"fix_id": "B", "file": "d/Log v1.xlsx", "op": "xlsx_add_column", "sheet": "Decisions taken", "key_header": "ID",
               "header": "Current", "values": {"D-1": "Doc v5"}, "style_from": "What it means"},
              {"fix_id": "C", "file": "d/Log v1.xlsx", "op": "xlsx_insert_row", "sheet": "Read me", "after": "Change log",
               "values": ["v2, 26 November 2026"]}]
        self.assertEqual(self.run_fixes(fx), 0)
        out = openpyxl.load_workbook(self.out / "d" / "Log v2.xlsx")
        d, r = out["Decisions taken"], out["Read me"]
        self.assertEqual([d["D3"].value, d["D4"].value, d["D5"].value], ["Current", "Doc v5", None])
        self.assertTrue(d["D3"].font.b)
        self.assertEqual(d["B4"].value, "uses Doc v4")  # decision text untouched
        self.assertEqual([c.value for c in r["A"]], ["Doc v1.", "Change log", "v2, 26 November 2026",
                                                     "v1, 1 November 2026", "Source: w"])
        bad = dict(fx[1], fix_id="D", header="ID")  # adding a column that exists fails
        shutil.rmtree(self.out)
        self.assertEqual(self.run_fixes([bad]), 1)

    def test_next_version(self):
        self.assertEqual(apply_fixes.next_version("A v1 v1.md"), "A v1 v2.md")
        self.assertEqual(apply_fixes.next_version("Test Cases v8.xlsx"), "Test Cases v9.xlsx")
        self.assertEqual(apply_fixes.next_version("X v9.md"), "X v10.md")
        with self.assertRaises(apply_fixes.FixError):
            apply_fixes.next_version("noversion.md")

    def test_apply_ok_and_original_untouched(self):
        before = self.f.read_bytes()
        rc = self.run_fixes([
            {"fix_id": "F1", "finding": "CG-1", "file": "d/Story x v1 v1.md", "op": "replace", "old": "line a", "new": "line A"},
            {"fix_id": "F2", "finding": "CG-2", "file": "d/Story x v1 v1.md", "op": "delete_line", "old": "line b"},
            {"fix_id": "F3", "finding": "CG-2", "file": "d/Story x v1 v1.md", "op": "insert_after", "old": "line A", "new": "n1\nn2"},
            {"fix_id": "F4", "finding": "CG-3", "file": "d/Story x v1 v1.md", "op": "replace", "old": "foo", "new": "bar", "count": 2}])
        self.assertEqual(rc, 0)
        self.assertEqual(self.f.read_bytes(), before)
        new = (self.out / "d" / "Story x v1 v2.md").read_text(encoding="utf-8")
        self.assertIn("line A\nn1\nn2\nbar bar", new)
        self.assertNotIn("line b", new)
        self.assertIn("D-RCV-60, 26 November 2026", new)
        self.assertIn("(CG-1, CG-2, CG-3)", new)
        self.assertIn("T3 Code / OpenCode / DeepSeek v4.1 Flash", new)
        self.assertTrue((self.out / "diffs" / "Story x v1 v2.md.diff").exists())

    def test_any_failure_writes_nothing_for_that_file(self):
        rc = self.run_fixes([
            {"fix_id": "F1", "finding": "CG-1", "file": "d/Story x v1 v1.md", "op": "replace", "old": "line a", "new": "line A"},
            {"fix_id": "F2", "finding": "CG-2", "file": "d/Story x v1 v1.md", "op": "replace", "old": "foo", "new": "bar"}])
        self.assertEqual(rc, 1)
        self.assertFalse((self.out / "d" / "Story x v1 v2.md").exists())
        self.assertEqual({r["status"] for r in self.result()}, {"FAILED"})
        self.assertIn("found 2 time(s), expected 1", self.result()[1]["reason"])

    def test_not_found_and_missing_file(self):
        self.run_fixes([{"fix_id": "F1", "file": "d/Story x v1 v1.md", "op": "replace", "old": "zzz", "new": "y"},
                        {"fix_id": "F2", "file": "d/None v1.md", "op": "replace", "old": "a", "new": "b"}])
        r = self.result()
        self.assertIn("found 0 time(s)", r[0]["reason"])
        self.assertIn("file not found", r[1]["reason"])

    def test_refuses_existing_next_version(self):
        (self.root / "d" / "Story x v1 v2.md").write_text("x", encoding="utf-8")
        self.run_fixes([{"fix_id": "F1", "file": "d/Story x v1 v1.md", "op": "replace", "old": "line a", "new": "A"}])
        self.assertIn("already exists", self.result()[0]["reason"])

    def test_refuses_out_inside_root_and_duplicate_ids(self):
        p = self.tmp / "f.jsonl"
        p.write_text(json.dumps({"fix_id": "F1", "file": "x", "op": "replace", "old": "a", "new": "b"}), encoding="utf-8")
        with self.assertRaises(SystemExit):
            apply_fixes.main(["--root", str(self.root), "--fixes", str(p), "--out", str(self.root / "o")])
        p.write_text("\n".join([json.dumps({"fix_id": "F1", "file": "x", "op": "replace", "old": "a", "new": "b"})] * 2), encoding="utf-8")
        with self.assertRaises(SystemExit):
            apply_fixes.main(["--root", str(self.root), "--fixes", str(p), "--out", str(self.out)])

    def test_dry_run_writes_no_file(self):
        rc = self.run_fixes([{"fix_id": "F1", "file": "d/Story x v1 v1.md", "op": "replace", "old": "line a", "new": "A"}], "--dry-run")
        self.assertEqual(rc, 0)
        self.assertFalse((self.out / "d" / "Story x v1 v2.md").exists())

    def test_xlsx_append_and_set(self):
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Story test cases"
        ws.append(["Test cases"])
        ws.append(["Test case", "Story", "Given"])
        ws.append(["TC-1", "S", "g1"])
        wb.save(self.root / "d" / "TC v8.xlsx")
        rc = self.run_fixes([
            {"fix_id": "F1", "file": "d/TC v8.xlsx", "op": "xlsx_append", "sheet": "Story test cases",
             "header_row_hint": "Test case", "key": "Test case", "rows": [{"Test case": "TC-2", "Story": "S", "Given": "g2"}]},
            {"fix_id": "F2", "file": "d/TC v8.xlsx", "op": "xlsx_set", "sheet": "Story test cases",
             "key_header": "Test case", "key": "TC-1", "header": "Given", "old": "g1", "new": "G1"}])
        self.assertEqual(rc, 0)
        ws2 = openpyxl.load_workbook(self.out / "d" / "TC v9.xlsx")["Story test cases"]
        self.assertEqual([c.value for c in ws2[4]], ["TC-2", "S", "g2"])
        self.assertEqual(ws2["C3"].value, "G1")
        # duplicate key is refused
        shutil.rmtree(self.out)
        self.run_fixes([{"fix_id": "F1", "file": "d/TC v8.xlsx", "op": "xlsx_append", "sheet": "Story test cases",
                         "header_row_hint": "Test case", "key": "Test case", "rows": [{"Test case": "TC-1", "Story": "S", "Given": "x"}]}])
        self.assertIn("already in", self.result()[0]["reason"])


class PipelineTests(unittest.TestCase):
    """detcheck -> mkfixes -> apply_fixes -> detcheck again on the next-version copy."""

    def make(self, extra_story=None):
        tmp = Path(tempfile.mkdtemp(prefix="pipetest-", dir=str(HERE.parent)))
        self.addCleanup(shutil.rmtree, tmp, True)
        root, cache, sd = build_root(tmp)
        stories = [sd / "RWB P3 E9001 APP Bad story v1 v1.md"]
        if extra_story:
            p = sd.parent / "RWB-SVC-P4 rwb-access" / "RWB P4 E9001 APP Other story v1 v1.md"
            p.parent.mkdir(parents=True)
            p.write_text(extra_story, encoding="utf-8")
            stories.append(p)
        det = tmp / "det"
        detcheck.main(["--root", str(root), "--cache", str(cache), "--out", str(det), "--wp", "T",
                       "--story", *map(str, stories)])
        fix = tmp / "fix"
        mkfixes.main(["--root", str(root), "--det", str(det), "--out", str(fix), "--legacy", "RWB-E9-001"])
        load = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        return tmp, root, cache, stories, det, fix, load

    def test_fixed_rows_clear_and_originals_untouched(self):
        tmp, root, cache, stories, det, fix, load = self.make()
        before = stories[0].read_bytes()
        app = tmp / "applied"
        apply_fixes.main(["--root", str(root), "--fixes", str(fix / "fixes.jsonl"), "--out", str(app)])
        self.assertEqual(stories[0].read_bytes(), before)
        res = load(app / "apply_result.jsonl")
        story_res = [r for r in res if r["file"].endswith(".md")]
        self.assertTrue(story_res and all(r["status"] == "APPLIED" for r in story_res), story_res)
        new = next(app.rglob("RWB P3 E9001 APP Bad story v1 v2.md"))
        txt = new.read_text(encoding="utf-8")
        self.assertIn("Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash", txt.split("**Change log.**")[-1])
        self.assertNotIn("primary_customer_id", txt)
        again = tmp / "again"
        detcheck.main(["--root", str(root), "--cache", str(cache), "--out", str(again), "--wp", "T", "--story", str(new)])
        disp = {d["id"]: d for d in load(fix / "disposition.jsonl")}
        b = load(det / "gaps.jsonl"); a = load(again / "gaps.jsonl")
        sig = lambda r: (r["check"], r["title"].replace(" v8", "").replace(" v9", ""))
        after = {sig(r) for r in a}
        fixed_story = [r for r in b if disp.get(r["id"], {}).get("status") == "FIXED" and r["check"] not in ("X9",)]
        self.assertTrue(fixed_story)
        self.assertEqual([r["title"] for r in fixed_story if sig(r) in after], [])

    def test_shared_tc_id_with_different_criteria_is_held(self):
        other = BAD.replace("RWB-P3-E9001-APP", "RWB-P4-E9001-APP").replace("| Service | rwb-case |", "| Service | rwb-access |")                    .replace("RWB-SVC-P3", "RWB-SVC-P4").replace("| TC-E9-001-15 | AC2 |", "| TC-E9-001-15 | AC1 |")
        tmp, root, cache, stories, det, fix, load = self.make(other)
        rows = [r for f in load(fix / "fixes.jsonl") if f["op"] == "xlsx_append" for r in f["rows"]]
        self.assertNotIn("TC-E9-001-15", [r["Test case"] for r in rows])
        held = [d for d in load(fix / "disposition.jsonl") if "ID collision" in d["detail"]]
        self.assertTrue(held)


class VersionFixTests(unittest.TestCase):
    """x20_fixes (stories) and declog_versions (Decision Log)."""

    def setUp(self):
        import x20_fixes
        self.x = x20_fixes
        self.pats = (re.compile(r"(?<![\w-])(Case and Workflow Model|Workflow Model|Test Cases|Physical Schema) v(\d+)\b"),
                     {"Case and Workflow Model": 6, "Workflow Model": 7, "Test Cases": 8, "Physical Schema": 7})
        self.disk = {"recovery workbench test cases v8.xlsx"}

    def plan(self, line):
        return self.x.plan_line(line, self.pats, self.disk)

    def test_reference_is_moved(self):
        new, pairs, risky = self.plan("The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases.")
        self.assertEqual(new, "The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases.")
        self.assertEqual((pairs, risky), ([("Test Cases v7", "Test Cases v8")], []))

    def test_longest_name_wins_even_when_current(self):
        new, pairs, _ = self.plan("See Case and Workflow Model v6 and Workflow Model v5.")
        self.assertEqual(new, "See Case and Workflow Model v6 and Workflow Model v7.")
        self.assertEqual(pairs, [("Workflow Model v5", "Workflow Model v7")])

    def test_claim_and_missing_file_are_held(self):
        new, pairs, risky = self.plan("The lookup is named only in Test Cases v7")
        self.assertEqual((new, pairs), ("The lookup is named only in Test Cases v7", []))
        self.assertIn("claim", risky[0][1])
        new, pairs, risky = self.plan("Built from Recovery Workbench Physical Schema v6.sql with the schema")
        self.assertEqual(pairs, [])
        self.assertIn("no file", risky[0][1])

    def test_history_lines_are_held(self):
        tmp = Path(tempfile.mkdtemp(prefix="x20test-", dir=str(HERE.parent)))
        self.addCleanup(shutil.rmtree, tmp, True)
        root, cache, sd = build_root(tmp)
        p = sd / "RWB P3 E9002 APP Hist v1 v1.md"
        p.write_text("# RWB-P3-E9002-APP\n\n**Change log.** D-RCV-60: split from Test Cases v7.\n\n"
                     "Tests are in Recovery Workbench Test Cases v7.xlsx.\n", encoding="utf-8")
        (root / "09 Testing and quality").mkdir(parents=True, exist_ok=True)
        (root / "09 Testing and quality" / "Recovery Workbench Test Cases v8.xlsx").write_bytes(b"")
        self.x.main(["--root", str(root), "--out", str(tmp / "o"), "--story", str(p)])
        fixes = [json.loads(l) for l in (tmp / "o" / "fixes.jsonl").read_text(encoding="utf-8").splitlines()]
        held = [json.loads(l) for l in (tmp / "o" / "held.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([f["new"] for f in fixes], ["Tests are in Recovery Workbench Test Cases v8.xlsx."])
        self.assertEqual(len(held), 1)
        self.assertIn("history", held[0]["reason"])

    def test_declog_pointer_column_and_recheck(self):
        import openpyxl, declog_versions
        tmp = Path(tempfile.mkdtemp(prefix="dlvtest-", dir=str(HERE.parent)))
        self.addCleanup(shutil.rmtree, tmp, True)
        root, cache, sd = build_root(tmp)
        wb = openpyxl.Workbook()
        rm = wb.active
        rm.title = "Read me"
        for v in ("x", "x", "x", "Recovery Workbench Decision Log v11. Decision D-RCV-60. The next version of v10: every "
                  "ID, number and date of v10 is kept.", "Tool", None, "Change log", "v11, 22 November 2026, split",
                  "Source: Recovery Workbench Decision Log v10, 15 November 2026. Rest."):
            rm.append([v])
        ws = wb.create_sheet("Decisions taken")
        ws.append(["ID", "Decision", "What it means for the build"])
        ws.append(["D-1", "Tests are in Test Cases v7 as written.", "Built on Decision Log v10."])
        ws.append(["D-2", "Nothing old.", ""])
        dl = root / rwbsrc.SOURCES["declog"]
        dl.parent.mkdir(parents=True, exist_ok=True)
        wb.save(dl)
        declog_versions.main(["--root", str(root), "--out", str(tmp / "c")])
        rows = [json.loads(l) for l in (tmp / "c" / "gaps.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["story"] for r in rows], ["D-1"])  # own-version reference skipped; D-2 clean
        apply_fixes.main(["--root", str(root), "--fixes", str(tmp / "c" / "fixes.jsonl"), "--out", str(tmp / "a")])
        v12 = next((tmp / "a").rglob("*Decision Log v12.xlsx"))
        out = openpyxl.load_workbook(v12)
        d = out["Decisions taken"]
        self.assertEqual(d["B2"].value, "Tests are in Test Cases v7 as written.")  # decision text kept
        self.assertTrue(d["D2"].value.startswith("Test Cases v8 (Document Index v14)"))
        r = [c.value for c in out["Read me"]["A"]]
        self.assertTrue(r[3].startswith("Recovery Workbench Decision Log v12."))
        self.assertIn("Source: Recovery Workbench Decision Log v11, 22 November 2026. Rest.", r)
        self.assertTrue(r[7].startswith("v12, 26 November 2026"))
        declog_versions.main(["--root", str(root), "--out", str(tmp / "r"), "--declog", str(v12)])
        self.assertEqual((tmp / "r" / "gaps.jsonl").read_text(encoding="utf-8"), "")



class PipelineRunnerTests(unittest.TestCase):
    """pipeline.py end to end on the synthetic set: every stage, then the re-check of the next versions."""

    def test_pipeline_legacy_run(self):
        tmp = Path(tempfile.mkdtemp(prefix="pipeline-", dir=str(HERE.parent)))
        self.addCleanup(shutil.rmtree, tmp, True)
        root, cache, sd = build_root(tmp)
        story = sd / "RWB P3 E9001 APP Bad story v1 v1.md"
        before = story.read_bytes()
        out = tmp / "run"
        args = ["--root", str(root), "--out", str(out), "--legacy", "RWB-E9-001", "--wp", "T", "--skip-declog",
                "--cache", str(cache), "--jobs", "2"]
        self.assertEqual(pipeline.main(args), 0)
        self.assertEqual(story.read_bytes(), before)
        load = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        res = load(out / "4-applied/apply_result.jsonl")
        self.assertTrue(any(r["status"] == "APPLIED" and r["file"].endswith(".md") for r in res))
        b, a = load(out / "1-check/gaps.jsonl"), load(out / "5-recheck/stories/gaps.jsonl")
        self.assertLess(len(a), len(b))
        disp = {d["id"]: d for d in load(out / "2-fixes/stories/disposition.jsonl")}
        sig = lambda r: (r["story"], r["check"], r["title"].replace(" v8", "").replace(" v9", ""))
        left = {sig(r) for r in a}
        fixed = [r for r in b if disp.get(r["id"], {}).get("status") == "FIXED" and r["check"] != "X9"]
        self.assertTrue(fixed)
        self.assertEqual([r["title"] for r in fixed if sig(r) in left], [])
        self.assertIn("Re-check (stories)", (out / "summary.md").read_text(encoding="utf-8"))
        with self.assertRaises(SystemExit):  # never overwrite a run
            pipeline.main(args)
        with self.assertRaises(SystemExit):  # never write inside ROOT
            pipeline.main(["--root", str(root), "--out", str(root / "x"), "--legacy", "RWB-E9-001"])

    def test_source_override_reaches_parallel_workers(self):
        tmp = Path(tempfile.mkdtemp(prefix="srcover-", dir=str(HERE.parent)))
        self.addCleanup(shutil.rmtree, tmp, True)
        saved = dict(rwbsrc.SOURCES)
        self.addCleanup(lambda: (rwbsrc.SOURCES.clear(), rwbsrc.SOURCES.update(saved)))
        root, cache, sd = build_root(tmp)
        alt = tmp / "alt" / "Recovery Workbench Test Cases v9.xlsx"
        (cache / "Recovery Workbench Test Cases v9.md").write_text(
            SHEETS["tc"].replace("TC-E9-001-02", "TC-E9-001-15"), encoding="utf-8")
        stories = [str(sd / "RWB P3 E9001 APP Bad story v1 v1.md"), str(sd / "RWB P3 E9001 CON Clean story v1 v1.md")]
        for jobs in ("1", "2"):
            o = tmp / f"o{jobs}"
            detcheck.main(["--root", str(root), "--cache", str(cache), "--out", str(o), "--wp", "T", "--jobs", jobs,
                           "--source", f"tc={alt}", "--story", *stories])
            rows = [json.loads(l) for l in (o / "gaps.jsonl").read_text(encoding="utf-8").splitlines()]
            miss = [r["title"] for r in rows if r["check"] == "X9" and r["title"].startswith("Test cases not in")]
            self.assertTrue(miss and all("Test Cases v9" in m and "TC-E9-001-15" not in m for m in miss), (jobs, miss))

if __name__ == "__main__":
    unittest.main(verbosity=1)

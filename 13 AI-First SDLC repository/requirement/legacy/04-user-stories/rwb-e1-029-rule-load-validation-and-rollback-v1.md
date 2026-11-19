<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 029 Rule load validation and rollback v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 029 Rule load validation and rollback v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-029 Rule load, validation and rollback

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-029 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-14 Load a rule version with validation; FEAT-CWC-15 Roll back a rule version; FEAT-DRI-07 Run the rules component on versioned rule tables |
| Requirement IDs | REQ-CWC-013, REQ-CWC-014, REQ-DRI-004 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules; All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | None |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **an Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases and a dry run), a load with a version, approval, rollback by one call and a change log**, so that **a rule change goes from template to production without a code release**.

## 2. Business rationale

Collection and recovery rules live in procedure documents today, and audit found the procedure not followed because the rules were not in the system (CTL-08). This story takes a rule version from one template through checks that refuse a bad table whole, an approval by Risk, a dated start and a one-call rollback, with each step in the change log. It meets REQ-CWC-013, REQ-CWC-014 and REQ-DRI-004, and covers the Epic 1 rule tables named in DL24: entry, exclusion, allocation, assignment and transfer.

## 3. Preconditions

- The five rule tables are agreed for Epic 1: ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (DL24, option A).
- Each table has 50 test cases with expected results, prepared by RW-COE in the template's Tests tab (assumed count from the current story).
- The loader holds RW-COE (Rules and parameters C); the approver holds RW-RISK (Rules and parameters A). One person may not hold both (separation of duty).
- Live cases exist for the dry run (RWB-E1-018).

## 4. Flow

1. RW-COE: fills the Rules template (tabs Rows and Tests) for table ALLOCATION, version "ALLOC-2026.12", valid from 2026-12-15.
2. RW-COE: calls POST /admin/rule-versions with the file, route set UNIVERSAL_RULES and valid from.
3. RuleLoadValidator: runs the schema check (columns, types, lists), then overlap, unreachable rows and missing default.
4. RuleTestRunner: runs the 50 test cases against the new rows and compares each result with the expected queue or outcome.
5. RuleDryRun: evaluates the new rows against every open case and counts the cases whose result would change, by product and queue.
6. RuleVersionService: on any failed check, refuses the load whole and names every failed row or test case; on success stores the rows with status LOADED and writes the change log entry with author, time, check result and dry run counts.
7. RW-RISK: approves through POST /admin/rule-versions/{versionId}/approve; refused if the approver is the author.
8. RuleVersionService: on the valid from date the version is in force; new decisions use it and open cases keep the version they were decided under (R-UNI-38).
9. RW-COE: if the version is wrong, calls POST /admin/rule-versions/{versionId}/rollback; the previous version is in force again in one transaction and the change log records the rollback.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Two rows match the same case at the same row order | Load refused; both row IDs named | MSG-P3-027 | AC2 |
| X2 | A test case result differs from the expected result | Load refused; failing test case IDs named | MSG-P3-027 | AC3 |
| X3 | A required column is missing or a value is outside its list | Load refused; row and column named | MSG-P3-027 | AC5 |
| X4 | A row can never match because an earlier row covers it | Load refused; row named | MSG-P3-027 | AC6 |
| X5 | The allocation table has no default row | Load refused | MSG-P3-027 | AC7 |
| X6 | The approver is the author | Approval refused | MSG-P7-002 | AC8 |
| X7 | Rollback with no earlier version | Refused | MSG-P3-015 | AC9 |
| X8 | The same version label is loaded twice | Refused with 409 | MSG-GEN-004 | AC10 |
| X9 | Valid from before today | Refused with 422 | MSG-GEN-003 | AC11 |
| X10 | An empty file | Refused with 422 | MSG-GEN-001 | AC12 |
| X11 | A role without Rules and parameters C loads a file | Refused with 403 | MSG-P4-002 | Access test TC-E1-029-13 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Works on the rule_row table and the change log; engines read the result through RuleTableReader |
| Negotiable | The checks are fixed; the tables, rows and test cases are data |
| Valuable | A rule change takes a load and an approval instead of a release |
| Estimable | One validator, one test runner, one dry run, three endpoints |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Rule load, validation and rollback

  Background:
    Given the loader U-41 holds RW-COE and the approver U-51 holds RW-RISK
    Given version "ALLOC-2026.11" of table ALLOCATION is in force with 24 rows

  Scenario: AC1 Valid load
    Given a template for table ALLOCATION version "ALLOC-2026.12" with 26 rows and 50 test cases that passes every check
    When U-41 loads it with valid from 2026-12-15 and U-51 approves it
    Then version "ALLOC-2026.12" is in force from 2026-12-15
    Then the change log records author U-41, approver U-51, the load and approval times, "50 of 50 test cases passed" and the dry run count

  Scenario: AC2 Overlap refused
    Given rows "ALLOC-031" and "ALLOC-032" both match product group "MORTGAGE" and region "BKK" at row order 12
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the overlap check naming "ALLOC-031" and "ALLOC-032"
    Then version "ALLOC-2026.11" stays in force

  Scenario: AC3 Test cases
    Given the 50 test cases with expected queues
    Given test cases "TA-07" and "TA-19" expect queue "MTG-BKK-CO" and the new rows return "MTG-CEN-CO"
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the test case check naming "TA-07" and "TA-19"

  Scenario: AC4 Rollback
    Given version 7, "ALLOC-2026.13", is in force and version 6, "ALLOC-2026.12", was in force before it
    When U-41 calls rollback once for version 7
    Then version 6 is in force
    Then the change log holds the rollback with U-41, the time and the reason
    Then a case allocated under version 7 keeps rule version "ALLOC-2026.13" on its decision log entry

  Scenario: AC5 Schema error
    Given row 9 has assignment reason "QUICK" that is not in its list
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the schema check naming row 9 and its column

  Scenario: AC6 Unreachable row
    Given row "ALLOC-040" matches product group "SSME" in any region at row order 5
    Given row "ALLOC-041" matches product group "SSME" and region "NE3" at row order 6
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the unreachable row check naming "ALLOC-041"

  Scenario: AC7 Missing default
    Given the allocation rows have no last row that matches every case
    When validation runs
    Then the system refuses the load with MSG-P3-027 for the default row check

  Scenario: AC8 Author cannot approve
    Given U-41 loaded version "ALLOC-2026.12"
    When U-41 calls approve
    Then the system refuses the call with MSG-P7-002
    Then the version stays LOADED

  Scenario: AC9 Rollback with no earlier version
    Given table TRANSFER has only version "TRF-2026.11"
    When rollback is called for "TRF-2026.11"
    Then the system refuses the call with MSG-P3-015
    Then "TRF-2026.11" stays in force

  Scenario: AC10 Same version loaded twice
    Given version "ALLOC-2026.12" is loaded
    When a file with version label "ALLOC-2026.12" is loaded again
    Then the system refuses the load with 409 and MSG-GEN-004

  Scenario: AC11 Valid from in the past
    When U-41 loads version "ALLOC-2026.14" with valid from 2026-11-01 on 2026-12-10
    Then the system refuses the load with 422 and MSG-GEN-003 for valid from

  Scenario: AC12 Empty file
    When U-41 loads a template with no rows
    Then the system refuses the load with 422 and MSG-GEN-001 for rows
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A version passes schema, overlap, unreachable row, default row and test case checks before it is stored | REQ-CWC-014; rules.txt Checks sheet |
| BR2 | A load with any failed check is refused in full | Reference data change process, step 3; CTL-08 |
| BR3 | Hit policy Unique: for one table, one trigger and one row order, one condition holds | rules.txt Key, hit policy Unique; ADR-004 |
| BR4 | The allocation table always has a default row | REQ-CWC-008 |
| BR5 | A version takes effect on its valid from date after approval; open cases keep the version they were decided under | R-UNI-38 |
| BR6 | The author cannot approve; Risk signs rule version changes | Separation of duty table; CTL-08 |
| BR7 | Rollback returns the previous version in one call | REQ-CWC-013; FEAT-CWC-15 |
| BR8 | Every load, approval and rollback is in the change log with author, approver, time and test result | REQ-CWC-013; FSD A2.14 |

## 9. State transitions

None. This story does not change a case status. It changes the status of a rule version: LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | LOADED |
| None | Load | Any check fails | REFUSED |
| LOADED | Approve | Approver is not the author | APPROVED |
| APPROVED | RULE_VERSION_EFFECTIVE (R-UNI-38) | Valid from reached | IN_FORCE; previous SUPERSEDED |
| IN_FORCE | Rollback | Earlier version exists | ROLLED_BACK; previous IN_FORCE |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Loads versions and calls rollback (Rules and parameters CRUD) |
| RW-RISK | Approves a version (Rules and parameters A); may not hold RW-COE |
| RW-AUDIT | Reads versions and the change log (Rules and parameters R) |
| RW-REFADM | Prepares load files; may not approve |
| SY-RULES | Reads the version in force for evaluation |
| No delegation of authority level applies | A rule version is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-001 to DF-REF-015 | rule_row | all fields | Write |
| DF-REF-052 | rule_row | rule_table | Write |
| DF-REF-053 | rule_row | row_order | Write |
| DF-REF-054 | rule_row | target_queue_code | Write |
| DF-REF-159 to DF-REF-180 | reference_version | all fields | Write |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-012 | recovery_case | region_code | Read |
| DF-CAS-015 | recovery_case | exposure_band | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-REF-028 | lov_value | lov_code | Read |
| DF-REF-029 | lov_value | value_code | Read |

The change log of a rule version is its rule_version header; RWB-E1-048 reports it for audit. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/rule-versions** (P4 endpoint)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (xlsx), routeSet = "UNIVERSAL_RULES", validFrom (date). The rule table and version label are columns in the file |
| Response | 201 RuleVersion[] for the stored rows (ruleId, ruleVersion, routeSet, fromState, eventCode, conditionExpr, actionText, toState, ownerRole, timerSpec, validFrom, validTo, approvedBy, testCaseId) |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 409 version label exists (MSG-GEN-004); 422 a check failed (MSG-P3-027, with the check, rows and test case IDs in Problem.detail), empty file (MSG-GEN-001), date order (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Version label; a repeat is refused with 409 |

**POST /api/recovery/v1/admin/rule-versions/{versionId}/approve**

| Item | Value |
|---|---|
| Response | 200 RuleVersion |
| Errors | 401; 403 no Rules and parameters A; 404; 409 approver is the author (MSG-P7-002) or version not LOADED (MSG-GEN-004); 503 |
| Authorization | Rules and parameters, right A |

**GET /api/recovery/v1/admin/rule-versions**

| Item | Value |
|---|---|
| Request | Query routeSet, status |
| Response | RuleVersion[] |
| Errors | 401; 403; 503 |
| Authorization | Rules and parameters, right R |

**POST /admin/rule-versions/{versionId}/rollback** (new endpoint, see additions)

| Item | Value |
|---|---|
| Request | Body { reason: string, required } |
| Response | 200 RuleVersion of the version now in force |
| Errors | 401; 403 no Rules and parameters U; 404; 409 no earlier version (MSG-P3-015) or version not IN_FORCE; 422 no reason (MSG-GEN-001); 503 |
| Authorization | Rules and parameters, right U |
| Idempotency | Idempotency-Key header |

**Published interfaces**

```java
// P3, package recovery.casewf.rules (published): validation and evaluation
public interface RuleLoadValidator {
    ValidationReport validate(String ruleTable, List<RuleRowDraft> rows, List<RuleTestCase> tests);
    DryRunReport dryRun(String ruleTable, List<RuleRowDraft> rows, LocalDate onDate);
}
// P4, package recovery.accessadmin.ruleversions (published): rule rows are P4 tables
public interface RuleTableReader {
    RuleTableVersion rowsInForce(String ruleTable, LocalDate onDate);
}
```

## 13. Solution plan

**Package.** Validation, test runner and dry run in `recovery/casewf/rules` (Java package `recovery.casewf.rules`). Endpoints and rule_row writes in the P4 package `recovery/accessadmin/ruleversions` (Java package `recovery.accessadmin.ruleversions`), which owns rule_row.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleTemplateParser | Service | Reads the Rows and Tests tabs; keeps row numbers |
| RuleLoadValidator | Published interface | Schema, overlap, unreachable row and default row checks |
| RuleTestRunner | Service | Runs each test case against the draft rows with the same evaluator the engines use |
| RuleDryRun | Service | Counts open cases whose result changes; reads case fields through the P3 repository |
| RuleVersionController | Controller | P4: list, load, approve, rollback endpoints |
| RuleVersionService | Service | P4: stores rows, approval check, effective date, rollback in one transaction, change log |
| RuleTableReader | Published interface | P4: version in force for a table and a date, cached per version |
| RuleEffectiveDateJob | Job | Daily at 00:01 sets APPROVED versions with today's valid from IN_FORCE |

**Database**

- Writes rule_row (all columns plus rule_table, row_order, target_queue_code) and rule_version, the version header with rule table, version label, status, author, approver, loaded and approved times, valid from, test result and dry run counts.
- Constraint uk_rule_row (rule_id, rule_version) exists; add `ix_rule_table_version ON rule_row (rule_table, rule_version) WHERE is_active` in P4 migration `V029_1__rule_table_columns.sql`, which also adds the three new columns and creates rule_version (unique (rule_table, version_label)).
- Rollback sets is_active false on the rolled back version and true on the previous one in one transaction.

**Configuration and reference data**

- The Rules template, owned by RW-COE.
- Lists used by the schema check through the P4 list interface (LOV-ASSIGN, LOV-ASSIGN-REASON, LOV-PRODUCT, LOV-REGION, LOV-EXPOSURE).
- Parameter `rules.testcases.min` = 50 (assumed) through RWB-E1-042.

**Build steps**

1. RuleTemplateParser; unit tests with a valid and an empty file (AC1, AC12).
2. Schema check against the lists; test AC5.
3. Overlap and unreachable row checks on the condition columns; tests AC2, AC6.
4. Default row check for ALLOCATION; test AC7.
5. RuleTestRunner with the shared evaluator; test AC3.
6. RuleDryRun with counts by product and queue in the change log.
7. RuleVersionService: store, approve with author check, effective date job, rollback; tests AC1, AC4, AC8, AC9, AC10, AC11.
8. Endpoints with access checks; access test.

**Feature flag.** `rwb.p3.ruleload`. Off: the load and rollback endpoints return 404; the version in force stays.

**Done when.** The tests in section 16 pass and the five Epic 1 tables load, approve and roll back in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A rule version check fails | The rule version was refused at the {check} check: {detail}. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | Empty file or no rollback reason | Enter {field}. |
| MSG-GEN-003 | Valid from before today | {field} cannot be before {other}. |
| MSG-GEN-004 | Version label already loaded | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. Rule versions are loaded by file and read through GET /admin/rule-versions; SCR-39 Rules and parameters comes in Epic 8 ("by file load before"). The rule change audit report is RWB-E1-048.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-029-01 | AC1, BR1, BR5, BR8 | System | ALLOCATION version with 26 rows and 50 passing test cases |
| TC-E1-029-02 | AC2, BR3 | System | Rows ALLOC-031 and ALLOC-032 at row order 12 |
| TC-E1-029-03 | AC3, BR1 | System | Test cases TA-07 and TA-19 failing |
| TC-E1-029-04 | AC4, BR5, BR7 | System | Versions 6 and 7 |
| TC-E1-029-05 | AC5, BR1 | System | Row 9 with value QUICK |
| TC-E1-029-06 | AC6, BR1 | System | Rows ALLOC-040 and ALLOC-041 |
| TC-E1-029-07 | AC7, BR4 | System | No default row |
| TC-E1-029-08 | AC8, BR6 | System | Load and approval by U-41 |
| TC-E1-029-09 | AC9, BR7 | System | TRANSFER with one version |
| TC-E1-029-10 | AC10 | System | Label ALLOC-2026.12 twice |
| TC-E1-029-11 | AC11 | System | Valid from 2026-11-01 |
| TC-E1-029-12 | AC12 | System | Template with no rows |
| TC-E1-029-13 | Access | Access | RW-CASEOWN calls POST /admin/rule-versions and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: rows, conditions, target queues, test cases and the test count are data.
- No personal data in logs, tests, the dry run report or prompts; the dry run reports counts only.
- No read of another module's tables: P3 validation receives rows as drafts; rule_row is written only by P4 code.
- The engines and the test runner use the same evaluator, so a passed test means the same result in production.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Validated load with a version, no release, rollback by one call | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14, FEAT-CWC-15 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-029-01, TC-E1-029-04, TC-E1-029-08, TC-E1-029-09, TC-E1-029-10, TC-E1-029-11 |
| REQ-CWC-014 | Schema, overlap, unreachable, default and test case checks | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-14 | 14 Set strategy, policy and decision rules | None | TC-E1-029-02, TC-E1-029-03, TC-E1-029-05, TC-E1-029-06, TC-E1-029-07, TC-E1-029-12 |
| REQ-DRI-004 | Epic 1 records for case creation, assignment and transfer use versioned rules | Epic 1, 3.3; Program, 5.7 | FEAT-DRI-07 | All recovery processes | R-UNI-38 | TC-E1-029-01, TC-E1-029-04 |

## 19. Out of scope

- The rule change audit report and the change checklist (RWB-E1-048).
- Loading the other 448 routing rules (later epics; DL24).
- The administration screen for rules (Epic 8, FEAT-ADM-02).
- Reference data loads for queues and lists (RWB-E1-019, RWB-E1-043).

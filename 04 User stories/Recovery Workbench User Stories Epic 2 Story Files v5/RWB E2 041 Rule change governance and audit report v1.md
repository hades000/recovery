# RWB-E2-041 Rule change governance and audit report

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-041 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-16 Report every rule change for audit |
| Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | D-RCV-36 (T4, T5, T8); ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-073, RWB-E1-037 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every rule package version and reported for audit**, so that **a rule change is as controlled as a code change**.

## 2. Business rationale

Audit found the collection procedure was not followed because rules lived in documents (CTL-08). Rules are data now: one wrong row in a rule package changes every case that reaches it, so each package version needs the same evidence as a code change: who asked, what it affects, the test result, who approved, when it took effect and how to undo it. This story makes the checklist fields required before a version can be approved and gives audit one report of every package change and of the decisions each version made. It meets REQ-CWC-013 and REQ-DRI-011. The measure is that every package version in force has a complete checklist in the report, and that RWB-E2-005 can reconcile the count of decisions per package version from the same report.

## 3. Preconditions

- RWB-E1-073 is done: `POST /admin/rule-packages/{packageCode}/versions`, approve and rollback exist, and `rule_package_version` carries DF-REF-295 `change_checklist`.
- RWB-E1-037 is done: the permission matrix gives Rules and parameters R to RW-COE, RW-RISK and RW-AUDIT.
- Package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows, loaded by U-41 and approved by U-51.
- The decision log writer (RWB-E1-027, reached through RWB-E1-072) writes `rule_id` DF-DEC-004 and `rule_version` DF-DEC-005 on every package decision, and `rule_version` holds the package version label.
- The checklist JSON schema is agreed on 16 November 2026: `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt`, `rollbackPlan`. The service fills `testResult`, `loadedAt`, `author`, `approver` and `checksum`.
- The reader holds RW-AUDIT or RW-COE with Rules and parameters R.
- Feature flag `rwb.p3.rule-change-report` is on in DEV and SIT.

## 4. Flow

1. Center of excellence analyst: raises the change request in the bank's request tool and receives its reference, for example CR-2026-0042.
2. Center of excellence analyst: fills the package workbook for ALLOCATION version "ALLOC-2026.12" and the checklist: request reference, impact summary "412 open Mortgage cases in the BKK queue", verify note and date from SIT, rollback plan "Roll back to ALLOC-2026.11".
3. Center of excellence analyst: loads the workbook and the checklist through `POST /admin/rule-packages/ALLOCATION/versions` with valid from 2026-12-10.
4. RulePackageVersionService: stores the checklist in DF-REF-295 with the author, `loaded_at`, the checksum and the scenario test result; a verify date before the load is refused.
5. Risk officer: approves through `POST /admin/rule-package-versions/{versionId}/approve`; the service refuses the approval unless the request, impact, verify and rollback plan are present, the test result is PASSED and the approver is not the author.
6. RulePackageEffectiveDateJob: at 00:01 on the valid from date moves the version to IN_FORCE and the previous version to SUPERSEDED.
7. Center of excellence analyst: if the version is wrong, rolls back by one call; the report shows the rollback as its own entry naming the version it returns to.
8. Internal audit or the center of excellence analyst: reads `GET /admin/rule-packages/change-report` for a period and a package, as JSON or CSV; the entry shows the decisions per package version for RWB-E2-005.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A package version reaches its valid from date with no approver | It is not served; the report shows it as LOADED | None | AC2 |
| X2 | Approval with a checklist item missing | Refused; the version stays LOADED | MSG-P3-022 | AC3 |
| X3 | Approval of a version whose test result is FAILED | Refused | MSG-P3-022 | AC4 |
| X4 | The report period has no changes | An empty list is returned | None | AC6 |
| X5 | The verify date is before the load time | Load refused | MSG-GEN-003 | AC7 |
| X6 | The report period ends before it starts | Refused | MSG-GEN-003 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds the checklist fields and one report to the package version of RWB-E1-073 |
| Negotiable | The checklist items are fixed by the Engineering Standards; the report columns can change |
| Valuable | Audit can test every rule change without asking the team, and E2-005 reconciles from one source |
| Estimable | Four checklist fields, three approval checks, one report, two formats |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is an API test on a PostgreSQL test container |

## 7. Acceptance criteria

```gherkin
Feature: Rule change governance and audit report

  Background:
    Given the business date is 2026-12-01
    Given package ALLOCATION version "ALLOC-2026.11" is in force with 24 rows
    Given user "U-41" holds RW-COE, "U-51" holds RW-RISK and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 Change by checklist
    Given a request "CR-2026-0042" to change ALLOCATION row "ALLOC-031" from queue "MTG-BKK-CO" to "MTG-CEN-CO" from 2026-12-10
    Given "U-41" loads ALLOCATION version "ALLOC-2026.12" with impact summary "412 open Mortgage cases in the BKK queue" and rollback plan "Roll back to ALLOC-2026.11"
    Given the load checks and the 50 scenarios pass
    Given "U-51" approves version "ALLOC-2026.12" on 2026-12-02
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then one entry shows package "ALLOCATION", version "ALLOC-2026.12", request "CR-2026-0042", test result "PASSED", author "U-41", approver "U-51", approved on 2026-12-02 and valid from 2026-12-10
    Then the entry shows 1 row changed, 0 added and 0 removed against "ALLOC-2026.11"
    Then the approval time is before the valid from date

  Scenario: AC2 Checklist skipped
    Given ALLOCATION version "ALLOC-2026.13" loaded by "U-41" with a complete checklist, valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the rule package service still serves version "ALLOC-2026.12"
    Then the change report shows version "ALLOC-2026.13" with status "LOADED" and approver empty

  Scenario: AC3 Checklist item missing at approval
    Given RESTRUCTURE version "RES-2026.12" loaded with no rollback plan
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    Then version "RES-2026.12" stays "LOADED"

  Scenario: AC4 Failed test result
    Given PAYMENT_MATCH version "PMT-2026.12" whose scenario result is "FAILED" with 2 of 58 scenarios failing
    When "U-51" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"

  Scenario: AC5 Verify item recorded before approval
    Given ALLOCATION version "ALLOC-2026.12" loaded on 2026-12-08 with verify note "SIT run 2026-12-08: 50 of 50 scenarios pass and the dry run covers 412 open cases" and verify date 2026-12-08
    When "U-51" approves it on 2026-12-09
    Then the change report shows verify date 2026-12-08, the verify note, the load time 2026-12-08 and checksum "9f2c...e1b4"
    Then the checklist holds all seven items: request, impact, test result, approver, load, verify and rollback plan

  Scenario: AC6 Period with no changes
    When "U-AUD-01" reads the change report for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC7 Verify date before the load
    Given ALLOCATION version "ALLOC-2026.14" with verify date 2026-12-07 and load time 2026-12-08
    When "U-41" loads it
    Then the system refuses the load with MSG-GEN-003 naming "verifiedAt" and "loadedAt"

  Scenario: AC8 Period in the wrong order
    When "U-AUD-01" reads the change report from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"

  Scenario: AC9 Report as CSV
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per package version
    Then it carries no party identifier and no case data

  Scenario: AC10 Decisions per package version
    Given ALLOCATION version "ALLOC-2026.11" was in force until 2026-12-09 and "ALLOC-2026.12" from 2026-12-10
    Given the decision log holds 96 entries with package version "ALLOC-2026.11" and 1,204 with "ALLOC-2026.12" in December 2026
    When "U-AUD-01" reads the change report for 2026-12-01 to 2026-12-31
    Then version "ALLOC-2026.11" shows 96 decisions and version "ALLOC-2026.12" shows 1,204
    Then the entry shows the decisions per rule ID across both versions: "ALLOC-031" 700 and "ALLOC-032" 600
    Then the total matches GET /api/recovery/v1/decision-log for the same period and package version
    Then RWB-E2-005 reconciles the count per package version from this report
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A package version can be approved only when it carries a change request reference, an impact summary, a verify record, a rollback plan and a test result of PASSED | CTL-08; rule package change process steps 1 to 4 |
| BR2 | The approver is not the author | roles.txt Separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013 |
| BR4 | The verify item is dated on or after the load and before the approval | rule package change process step 6 |
| BR5 | The report lists every package version whose load, approval, valid from, verification or rollback falls in the period | REQ-DRI-011 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, by Drools rule name and row order, and the rule IDs changed | D-RCV-36 T4, T5; ADR-012 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38 |
| BR8 | The decisions per package version are counted from decision_log_entry rule_id and rule_version; the report never recomputes a decision | REQ-DRI-011; D-RCV-36 T5 |
| BR9 | The checklist is one JSON object in DF-REF-295; this story adds no table and no column | D-RCV-36 T4; RWB-E1-072 |

## 9. State transitions

None. This story changes no case status. In the package version statuses of RWB-E1-073, LOADED to APPROVED now needs a complete checklist (BR1), and the report reads every later status without changing it.

| From | Event | Condition | To |
|---|---|---|---|
| LOADED | Approve | Checklist complete, test result PASSED, approver is not the author | APPROVED |
| LOADED | Approve | Any item missing or test result FAILED | LOADED (refused) |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a package version with its checklist; reads the report (Rules and parameters CRUD; read) |
| RW-RISK, risk and model risk officer | Approves package versions (Rules and parameters A); reads the report |
| RW-AUDIT, internal audit | Reads and exports the report (Rules and parameters R). Changes nothing |
| RW-PLATADM, platform administrator | Reads the report (Rules and parameters R) |
| SY-RULES, Drools evaluator | Evaluates the package version and writes its rule ID and version to the decision log |
| No delegation of authority level applies | A package version is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-274 | rule_package | id | Read |
| DF-REF-275 | rule_package | package_code | Read |
| DF-REF-276 | rule_package | title | Read |
| DF-REF-277 | rule_package | owner_role | Read |
| DF-REF-279 | rule_package_version | id | Read |
| DF-REF-280 | rule_package_version | package_id | Read |
| DF-REF-281 | rule_package_version | version_label | Read |
| DF-REF-282 | rule_package_version | status | Read |
| DF-REF-283 | rule_package_version | source_blob_ref | Read |
| DF-REF-285 | rule_package_version | checksum | Read |
| DF-REF-286 | rule_package_version | valid_from | Read |
| DF-REF-287 | rule_package_version | valid_to | Read |
| DF-REF-288 | rule_package_version | author | Read |
| DF-REF-289 | rule_package_version | approver | Read |
| DF-REF-290 | rule_package_version | loaded_at | Read |
| DF-REF-291 | rule_package_version | approved_at | Read |
| DF-REF-292 | rule_package_version | test_result | Read |
| DF-REF-293 | rule_package_version | dry_run_counts | Read |
| DF-REF-294 | rule_package_version | rollback_of | Read |
| DF-REF-295 | rule_package_version | change_checklist | Write, read |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-297 | rule_row | drools_rule_name | Read |
| DF-DEC-004 | decision_log_entry | rule_id | Read, through the P7 query interface |
| DF-DEC-005 | decision_log_entry | rule_version | Read, through the P7 query interface |

Field IDs are those in the Logical Data Model and Data Dictionary. The checklist JSON holds the seven items of section 1; the service writes `testResult`, `loadedAt`, `author`, `approver` and `checksum` from the package version row, so no item is typed twice.

## 12. Contract

**POST /api/recovery/v1/admin/rule-packages/{packageCode}/versions** (existing endpoint of RWB-E1-073, one field added): multipart gains `checklist` (JSON object, max 8 KB) with `changeRequestRef` (max 30), `impactSummary` (max 1000), `verifyNote` (max 1000), `verifiedAt` (date) and `rollbackPlan` (max 1000). Missing fields do not refuse the load; they refuse the approval (BR1).

**POST /api/recovery/v1/admin/rule-package-versions/{versionId}/approve** (existing): 409 with MSG-P3-022 naming the missing item when BR1 fails; otherwise as RWB-E1-073.

**GET /api/recovery/v1/admin/rule-packages/change-report** (new, P3)

| Item | Value |
|---|---|
| Request | Query: `from` (date, required), `to` (date, required), `packageCode` (optional), `format` (`json` default or `csv`), `page`, `size` (default 50, max 200) |
| Response | 200 `ChangeReportPage`: `items[]` of `RulePackageChangeEntry` (`packageCode`, `packageTitle`, `versionLabel`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `verifyNote`, `verifiedAt`, `testResult`, `author`, `loadedAt`, `approver`, `approvedAt`, `checksum`, `rollbackPlan`, `rulesChanged[]`, `decisions`, `decisionsByRule[]`, `rolledBackTo`), `page`, `size`, `total`; or `text/csv` with the same columns |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 422 `to` before `from` (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Not applicable |

**Published interface** (added to the P4 `RulePackageVersionService`, used by the report and by RWB-E2-005):

```java
Page<RulePackageChangeEntry> changeReport(LocalDate from, LocalDate to, Optional<String> packageCode, Pageable page);
```

No events are published.

## 13. Solution plan

**Package.** `recovery.casewf.rules.audit` in the recovery module; the endpoint and the version writes in the P4 package `recovery.accessadmin.rulepackages`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChangeChecklistValidator | Service | The BR1 and BR2 checks called by `approve(...)` |
| ChangeEffectCalculator | Service | Compares the rule_row rows of a version with the version it replaces by `drools_rule_name` and row order; lists the rule IDs changed |
| DecisionCountReader | Service | Reads the count per rule ID and package version from the P7 decision log query interface |
| RuleChangeReportService | Service | Builds the report for a period and a package; paging; CSV writer |
| RuleChangeReportController | Controller | `GET /admin/rule-packages/change-report`; problem responses |
| RulePackageVersionRepository | Repository | Extended with the period query on loaded, approved, valid from and verify dates |

**Database.** Flyway migration `V<next>__rwb_e2_041_change_report_index.sql` adds `ix_rpv_loaded_at` on `rule_package_version (loaded_at)`, `ix_rpv_approved_at` on `(approved_at)` and `ix_rpv_valid_from` on `(valid_from)`. No new column: DF-REF-295 exists from V072_1 of RWB-E1-072.

**Configuration and reference data.** None beyond RWB-E1-073. The checklist items come from the Engineering Standards rule package change checklist. The report reads the package version rows and the decision log; it never recomputes a version from the live rule rows.

**Build steps**

1. Write the index migration and the repository period query.
2. Extend the load handler to accept the `checklist` part and store it in DF-REF-295; test the verify date check (AC7).
3. Build `ChangeChecklistValidator` and call it from `approve(...)`; return MSG-P3-022 naming the first missing item (AC3, AC4).
4. Build `ChangeEffectCalculator` and test it on versions with added, changed and removed rows (AC1).
5. Build `DecisionCountReader` against the P7 query interface and test the counts (AC10).
6. Build `RuleChangeReportService` and `RuleChangeReportController` with JSON and CSV output (AC6, AC8, AC9).
7. Test the skipped approval and the valid from path (AC2, AC5).
8. Add the access test and the contract test for the new operation (TC-E2-041-11).

**Feature flag.** `rwb.p3.rule-change-report`. Off: the report endpoint returns 404 and approval runs the RWB-E1-073 checks only.

**Done when.** The tests in section 16 pass, the report for the SIT load period lists every package version loaded in SIT with a complete checklist, and its decision counts reconcile with RWB-E2-005.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-003 | Verify date before the load, or a report period in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-001 | A required checklist value is empty | Enter {field}. |
| MSG-P7-002 | The author approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right reads the report | You cannot {action} here. Your role does not include it. |

MSG-P3-022 moves here from RWB-E1-048 with the story (D-RCV-36 T8). Thai text for each message follows DL10.

## 15. Screens and states

No screen in this story. Internal audit and the center of excellence read the report through the endpoint and open the CSV in Excel. The rules and parameters screen SCR-39 shows the same entries from Epic 8.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-041-01 | AC1, BR1, BR5, BR6 | System | ALLOCATION v11 to v12, request CR-2026-0042, one changed row |
| TC-E2-041-02 | AC2, BR3 | System | ALLOCATION v13 never approved |
| TC-E2-041-03 | AC3, BR1 | System | RESTRUCTURE v12 with no rollback plan |
| TC-E2-041-04 | AC4, BR1 | System | PAYMENT_MATCH v12 with a FAILED scenario result |
| TC-E2-041-05 | AC5, BR1, BR4 | System | Verify date 2026-12-08, approval 2026-12-09 |
| TC-E2-041-06 | AC6 | System | Period 2026-11-01 to 2026-11-15 with no versions |
| TC-E2-041-07 | AC7, BR4 | System | Verify date one day before the load |
| TC-E2-041-08 | AC8 | System | Period end before start |
| TC-E2-041-09 | AC9 | System | CSV export of December versions |
| TC-E2-041-10 | AC10, BR8 | System | 96 and 1,204 decisions in December 2026 |
| TC-E2-041-11 | Access | Access | RW-CASEOWN (no Rules and parameters right) reads the change report; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. The checklist items are data; the report computes from rows.
- No personal data in logs, tests, workflow history or prompts. The report carries staff user IDs and no customer or case data.
- No read of another module's tables; ACE data only through recovery.v_ace_* views. The decision counts come through the P7 query interface.
- The report reads the package version registry and the decision log; it never recomputes a version from the live rule rows.
- The approver is never the author; the service checks it, not only the screen.
- Forbidden: any change to an existing version. A rollback is a new entry that names the version it returns to.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated package version with a checklist and rollback | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E2-041-01 to TC-E2-041-04, TC-E2-041-11 |
| REQ-DRI-011 | Versioned tables with author and approver, and a count of decisions per version | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E2-041-01, TC-E2-041-05 to TC-E2-041-10 |

## 19. Out of scope

- The load, checks, scenarios, approval and rollback mechanics of a rule package version (RWB-E1-073).
- The reference table checklist fields and their report (RWB-E1-043); this report covers rule package versions only.
- The rules and parameters screen (SCR-39, Epic 8).
- The QA sample against the rule package version applied (FEAT-ADM-08, Epic 8).
- The decision log store and its read API (RWB-E1-008, RWB-E1-027).

<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 048 Rule change audit report v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 048 Rule change audit report v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-048 Rule change audit report

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-048 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-16 Report every rule change for audit |
| Requirement IDs | REQ-CWC-013, REQ-DRI-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-037, RWB-E1-011, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the parameter change and rule change checklist (request, impact, test result, approver, load, verify, rollback plan) recorded on every change and reported for audit**, so that **a configuration change is as controlled as a code change**.

## 2. Business rationale

Audit found the collection procedure was not followed because rules lived in documents (CTL-08). When rules and limits are data, a wrong row changes every case it touches, so each change needs the same evidence as a code change: who asked, what it affects, the test result, who approved, when it took effect and how to undo it. This story makes the checklist fields required before a version can be approved and gives audit one report of every change. It meets REQ-CWC-013 and REQ-DRI-011. The measure is that every version in force has a complete checklist in the report.

## 3. Preconditions

- RWB-E1-043 is done: every reference table version is a row in `reference_version` with author and approver.
- RWB-E1-037 is done: the permission matrix gives Rules and parameters R to RW-COE, RW-RISK and RW-AUDIT.
- RWB-E1-011 is done: the daily data quality report lists refused loads.
- Rule versions loaded through `POST /admin/rule-versions` (RWB-E1-029) are recorded in the same registry with table code `RULE_` and the route set, for example `RULE_UNIVERSAL_RULES`.
- The rule table test harness (RWB-TE-005) writes its result to the version for rule tables; the load checks of RWB-E1-043 write it for reference tables.

## 4. Flow

1. Center of excellence analyst: raises the change request in the bank's request tool and receives its reference, for example CR-2026-0042.
2. Reference data administrator: loads the new version through `POST /admin/reference-loads` (or `POST /admin/rule-versions`) with the request reference, the impact summary and the rollback plan as form fields.
3. Reference data service: stores the checklist fields on the version and records the test result from the load checks or the harness (PASSED or FAILED).
4. Approver: approves through `POST /admin/reference-loads/{loadId}/approve`.
5. Reference data service: refuses the approval unless the request reference, impact summary, rollback plan and a PASSED test result are present and the approver is not the author.
6. Reference data administrator: after the valid from date, records the verification through `POST /admin/reference-loads/{loadId}/verify`.
7. Internal audit or the center of excellence analyst: reads the report through `GET /admin/change-log` for a period and a table, as JSON or CSV.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A version reaches its valid from date with no approver | It is not served; the report shows it as not approved | None | AC2 |
| X2 | Approval with a checklist item missing | Refused; the version stays VALIDATED | MSG-P3-022 | AC3 |
| X3 | Approval of a version whose test result is FAILED | Refused | MSG-P3-022 | AC4 |
| X4 | The report period has no changes | An empty list is returned | None | AC6 |
| X5 | Verification recorded before the valid from date | Refused | MSG-GEN-003 | AC7 |
| X6 | The report period ends before it starts | Refused | MSG-GEN-003 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds fields and one report to the registry of RWB-E1-043 |
| Negotiable | The checklist items are fixed by the Engineering Standards; the report columns can change |
| Valuable | Audit can test every configuration change without asking the team |
| Estimable | Six fields, one approval check, one verify call, one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is an API test on a PostgreSQL test container |

## 7. Acceptance criteria

```gherkin
Feature: Rule change audit report

  Background:
    Given the business date is 2026-12-01
    Given SERVICE_LEVEL version 3 is in force with 10 working days for "MORTGAGE" status "IN_PROGRESS"
    Given user "U-REF-01" holds RW-REFADM, "U-RSK-01" holds the approve right and "U-AUD-01" holds RW-AUDIT

  Scenario: AC1 Change by checklist
    Given a request "CR-2026-0042" to change "MORTGAGE" status "IN_PROGRESS" to 8 working days from 2026-12-10
    Given "U-REF-01" loads SERVICE_LEVEL version 4 with impact summary "412 open Mortgage cases in IN_PROGRESS" and rollback plan "Reload version 3"
    Given the load checks pass
    Given "U-RSK-01" approves version 4 on 2026-12-02
    When "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31
    Then one entry shows table "SERVICE_LEVEL", version 4, request "CR-2026-0042", test result "PASSED", author "U-REF-01", approver "U-RSK-01", approved on 2026-12-02 and valid from 2026-12-10
    Then the entry shows 1 row changed, 0 added and 0 removed against version 3
    Then the approval time is before the valid from date

  Scenario: AC2 Checklist skipped
    Given SERVICE_LEVEL version 5 loaded by "U-REF-01" with valid from 2026-12-15 and never approved
    When the business date reaches 2026-12-15
    Then the reference data service still serves version 4
    Then the change log shows version 5 with status "VALIDATED" and approver empty

  Scenario: AC3 Checklist item missing at approval
    Given HOLIDAY version 2 loaded with no rollback plan
    When "U-RSK-01" approves it
    Then the system refuses the approval with MSG-P3-022 naming "rollback plan"
    Then version 2 stays "VALIDATED"

  Scenario: AC4 Failed test result
    Given rule version "RULE_UNIVERSAL_RULES" version 3 whose harness result is "FAILED" with 2 of 50 tests failing
    When "U-RSK-01" approves it
    Then the system refuses the approval with MSG-P3-022 naming "test result"

  Scenario: AC5 Verification after the change takes effect
    Given SERVICE_LEVEL version 4 in force from 2026-12-10
    When "U-REF-01" records the verification on 2026-12-10 with the note "Timer on RW-2026-000101 shows 8 working days"
    Then the change log entry for version 4 shows verified by "U-REF-01" on 2026-12-10

  Scenario: AC6 Period with no changes
    When "U-AUD-01" reads the change log for 2026-11-01 to 2026-11-15
    Then the response is an empty list with total 0

  Scenario: AC7 Verification too early
    Given SERVICE_LEVEL version 4 with valid from 2026-12-10
    When "U-REF-01" records the verification on 2026-12-09
    Then the system refuses the call with MSG-GEN-003 naming "verified at" and "valid from"

  Scenario: AC8 Period in the wrong order
    When "U-AUD-01" reads the change log from 2026-12-31 to 2026-12-01
    Then the system refuses the call with MSG-GEN-003 naming "to" and "from"

  Scenario: AC9 Report as CSV
    When "U-AUD-01" reads the change log for 2026-12-01 to 2026-12-31 with format "csv"
    Then the response is a CSV file with one header row and one row per version
    Then it carries no party identifier and no case data
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A version can be approved only when it carries a change request reference, an impact summary, a rollback plan and a test result of PASSED | CTL-08; refdata.txt Change process steps 1 to 4 |
| BR2 | The approver is not the author | roles.txt Separation of duty; CTL-08 |
| BR3 | A version that is not approved never takes effect | R-UNI-38; REQ-CWC-013 |
| BR4 | Verification is recorded on or after the valid from date | refdata.txt Change process step 6 |
| BR5 | The report lists every version of every reference and rule table whose load, approval, valid from or verification falls in the period | REQ-DRI-011 |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, and for rule tables the rule IDs changed | ADR-004 |
| BR7 | A rollback appears as its own entry naming the version it returns to | REQ-CWC-013; R-UNI-38 |

## 9. State transitions

None. This story does not change a case status. It adds two conditions to the reference version statuses of RWB-E1-043: VALIDATED to APPROVED needs a complete checklist (BR1), and an APPROVED version gets a verification record after its valid from date.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads a version with its checklist fields; records verification (Reference data C, U) |
| RW-COE, center of excellence analyst | Loads rule and reference versions; reads the report (Rules and parameters R) |
| RW-RISK, risk and model risk officer | Approves versions (Rules and parameters A; Reference data approve right assumed as in RWB-E1-043); reads the report |
| RW-AUDIT, internal audit | Reads and exports the report (Rules and parameters R). Changes nothing |
| RW-PLATADM, platform administrator | Reads the report (Rules and parameters R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-174 | reference_version | change_request_ref | Write |
| DF-REF-175 | reference_version | impact_summary | Write |
| DF-REF-176 | reference_version | test_result | Write |
| DF-REF-177 | reference_version | rollback_plan | Write |
| DF-REF-178 | reference_version | verified_by | Write |
| DF-REF-179 | reference_version | verified_at | Write |
| DF-REF-160 | reference_version | table_code | Read |
| DF-REF-161 | reference_version | version_no | Read |
| DF-REF-163 | reference_version | valid_from | Read |
| DF-REF-165 | reference_version | status | Read |
| DF-REF-166 | reference_version | author_user_id | Read |
| DF-REF-167 | reference_version | approver_user_id | Read |
| DF-REF-168 | reference_version | approved_at | Read |
| DF-REF-183 | reference_row | row_key | Read |
| DF-REF-184 | reference_row | row_data | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /admin/reference-loads** and **POST /admin/rule-versions** (P4 endpoints) take three more form fields: `changeRequestRef` (max 30), `impactSummary` (max 1000), `rollbackPlan` (max 1000). Missing fields do not refuse the load; they refuse the approval (BR1).

**POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint): 409 with MSG-P3-022 naming the missing item when BR1 fails; otherwise as RWB-E1-043.

**POST /admin/reference-loads/{loadId}/verify** (new, P3)

| Item | Value |
|---|---|
| Request | `VerifyRequest`: `note` (max 1000, required) |
| Response | 200 `ReferenceLoad` with `verifiedBy`, `verifiedAt` |
| Errors | 401; 403 no Reference data U (MSG-P4-002); 404 unknown load (MSG-P4-003); 422 empty note (MSG-GEN-001) or before valid from (MSG-GEN-003); 503 |
| Authorization | Reference data, right U |
| Idempotency | A second verification of the same version returns 200 with the first record and changes nothing |

**GET /admin/change-log** (new, P3)

| Item | Value |
|---|---|
| Request | Query: `from` (date, required), `to` (date, required), `table` (optional), `format` (`json` default or `csv`), `page`, `size` (default 50, max 200) |
| Response | 200 `ChangeLogPage`: `items[]` of `ChangeLogEntry` (`table`, `version`, `status`, `validFrom`, `validTo`, `changeRequestRef`, `impactSummary`, `testResult`, `authorUserId`, `loadedAt`, `approverUserId`, `approvedAt`, `verifiedBy`, `verifiedAt`, `rollbackPlan`, `rowsAdded`, `rowsChanged`, `rowsRemoved`, `rulesChanged[]`), `page`, `size`, `total`; or `text/csv` with the same columns |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 422 `to` before `from` (MSG-GEN-003); 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Not applicable |

**Published interface** (added to `ReferenceVersionRegistry` of RWB-E1-043):

```java
ReferenceVersion verify(UUID loadId, UUID verifierUserId, String note, LocalDate businessDate);
Page<ChangeLogEntry> changeLog(LocalDate from, LocalDate to, Optional<String> tableCode, Pageable page);
```

No events are published.

## 13. Solution plan

**Package.** `recovery.casewf.refdata.audit` in the recovery module.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChangeChecklistValidator | Service | The BR1 and BR2 checks called by `approve(...)` |
| ChangeEffectCalculator | Service | Compares the rows of a version with the version it replaces by `row_key` and `row_data`; lists changed rule IDs for `RULE_` tables |
| ChangeLogService | Service | Builds the report for a period and a table; paging; CSV writer |
| ChangeLogController | Controller | `GET /admin/change-log` and `POST /admin/reference-loads/{loadId}/verify`; problem responses |
| ReferenceVersionRepository | Repository | Extended with the period query on loaded, approved, valid from and verified dates |

**Database.** Flyway migration `V<next>__rwb_e1_048_change_checklist.sql` adds to `reference_version`: `change_request_ref varchar(30)`, `impact_summary varchar(1000)`, `test_result varchar(10)` (PASSED, FAILED), `rollback_plan varchar(1000)`, `verified_by uuid`, `verified_at timestamptz`, `verify_note varchar(1000)`. Index on `(created_at)`, `(approved_at)` and `(valid_from)` for the period query.

**Configuration and reference data.** None beyond RWB-E1-043. The checklist items come from the Engineering Standards parameter and rule change checklists.

**Build steps**

1. Write the migration and extend the entity.
2. Accept the three form fields in the P4 load handlers and pass them to `recordVersion(...)`; record the test result from the load checks or the harness.
3. Build `ChangeChecklistValidator` and call it from `approve(...)`; return MSG-P3-022 naming the first missing item.
4. Build `verify(...)` with the date check against the business date and the valid from.
5. Build `ChangeEffectCalculator` and test it on versions with added, changed and removed rows.
6. Build `ChangeLogService` and `ChangeLogController` with JSON and CSV output.
7. Write the tests in section 16.

**Feature flag.** `rwb.p3.change-log`. Off: approval runs the RWB-E1-043 checks only and the report endpoint returns 404.

**Done when.** The tests in section 16 pass, and the report for the SIT load period lists every version loaded in SIT with a complete checklist.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-022 | Approval with a missing checklist item or a FAILED test result | The change cannot be approved: {item} is missing or failed. |
| MSG-GEN-003 | Verification before valid from, or a report period in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-001 | Verification with no note | Enter {field}. |
| MSG-P7-002 | The author approves their own version | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | A role without the right reads the report or verifies | You cannot {action} here. Your role does not include it. |

MSG-P3-022 is new (see Additions). Thai text follows DL10.

## 15. Screens and states

No screen in this story. Internal audit and the center of excellence read the report through the endpoint and open the CSV in Excel. The rules and parameters screen SCR-39 shows the same entries from Epic 8.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-048-01 | AC1, BR1, BR5, BR6 | System | SERVICE_LEVEL v3 to v4, request CR-2026-0042, one changed row |
| TC-E1-048-02 | AC2, BR3 | System | SERVICE_LEVEL v5 never approved |
| TC-E1-048-03 | AC3, BR1 | System | HOLIDAY v2 with no rollback plan |
| TC-E1-048-04 | AC4, BR1 | System | RULE_UNIVERSAL_RULES v3 with a FAILED harness result |
| TC-E1-048-05 | AC5, BR4 | System | Verification on the valid from date |
| TC-E1-048-06 | AC6 | System | Period 2026-11-01 to 2026-11-15 with no versions |
| TC-E1-048-07 | AC7, BR4 | System | Verification one day before valid from |
| TC-E1-048-08 | AC8 | System | Period end before start |
| TC-E1-048-09 | AC9 | System | CSV export of December versions |
| TC-E1-048-10 | Access | Access | RW-PHONECOL (no Rules and parameters right) reads the change log; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. The checklist items are the fields; the report computes from rows.
- No personal data in logs, tests, the report or prompts. The report carries user IDs of staff and no customer or case data.
- No read of another module's tables. Rule versions reach the registry through the P4 handler calling the published interface.
- The report reads the registry; it never recomputes a version from the live tables.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-013 | Rule change by validated load with a version stamp and rollback | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E1-048-01 to TC-E1-048-04, TC-E1-048-10 |
| REQ-DRI-011 | Versioned tables with author and approver | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-16 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E1-048-01, TC-E1-048-05 to TC-E1-048-09 |

## 19. Out of scope

- The load, validation and rollback of rule versions (RWB-E1-029).
- The rule table test harness that produces the rule test result (RWB-TE-005).
- The rules and parameters screen (SCR-39, Epic 8).
- The QA sample against the rule version applied (FEAT-ADM-08, Epic 8).

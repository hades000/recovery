<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 017 Retention and archive rule for the data store v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 017 Retention and archive rule for the data store v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-017 Retention and archive rule for the data store

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-017 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-17 Apply the retention and archive rule to the data store |
| Requirement IDs | REQ-RDF-013 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-013) |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-001, RWB-E1-043, RWB-TE-012, RWB-E1-064 |
| Status | Ready for build |

## 1. Story

As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action**, so that **the store holds what the policy allows and nothing older**.

## 2. Business rationale

PDPA and the bank retention schedule limit how long personal data is kept, and today recovery records stay in spreadsheets and systems with no end date. A retention rule per data product and table, loaded as versioned data, lets Compliance set and change periods without a release. A monthly job archives rows past their period to a write-once archive container and removes them from the live store, keeps every row of a case under legal hold, and records what it did. Serves REQ-RDF-013 and the retention requirements NFR-031 and NFR-072.

## 3. Preconditions

- RWB-E1-001 is done: the recovery tables and sys_objects exist.
- RWB-E1-043 is done: the reference data service validates and approves versioned loads.
- RWB-E1-064 is done: data_product holds DP01 to DP14.
- RWB-TE-012 is done: a write-once archive container exists in each environment, writable by SY-DATALOAD.
- Retention rule version "RET-2026.11" is loaded and approved: DP05 interaction at 24 months on occurred_at (assumed until Compliance supplies the bank schedule; DL26).
- P3 publishes CaseHoldQuery (section 12), returning the cases with legal_hold = true.
- Quartz holds the JOB-17 trigger for the first Sunday of each month at 02:30 Asia/Bangkok.

## 4. Flow

1. Reference data administrator: loads a retention rule version through POST /admin/reference-loads with table retention_rule; the owner approves it.
2. RetentionRuleLoader: validates the rows (known product, known table in sys_objects, months between 1 and 600, table not decision_log_entry) and stores the version.
3. Quartz: starts JOB-17 Retention job on the first Sunday of the month.
4. RetentionService: reads the rules in force on the run date.
5. RetentionService: calls CaseHoldQuery.casesOnLegalHold() and excludes every row of those cases.
6. RetentionService: selects, per rule, the rows whose age-basis field is older than the run date minus the retention months.
7. ArchiveWriter: writes the selected rows per table to the archive container with a manifest (row count and SHA-256 per file) and reads the manifest back.
8. RetentionService: after the manifest matches, deletes the archived rows from the live table in one transaction per table and rule, under the purge setting the append-only trigger allows.
9. RetentionService: records on the job run the counts per product and table, the rule version, the archive location and the hold report (case numbers and row counts kept).
10. Compliance officer: reads the run result through GET /admin/jobs and the summary alert (MSG-P1-020).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A case is on legal hold | Its rows are kept and listed in the hold report | MSG-P1-020 | AC3 |
| X2 | A rule row has months outside 1 to 600 | Load refused in full; previous version stays in force | MSG-GEN-002 | AC4 |
| X3 | The archive write or the manifest check fails | No row deleted; run Failed; alert raised; rerun from the job monitor | MSG-GEN-006 | AC5 |
| X4 | JOB-17 runs again for the same month | Rows already archived are gone; the rerun archives only rows still past their rule | None | AC6 |
| X5 | A row is exactly at its retention age | The row is kept | None | AC7 |
| X6 | A rule names table decision_log_entry | Load refused in full; the decision log is never archived by this job | MSG-P1-002 | AC8 |
| X7 | A rerun is posted while JOB-17 runs | 409; one run continues | MSG-P2-006 | AC9 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the tables (RWB-E1-001), the reference data service (RWB-E1-043), the data product table (RWB-E1-064) and the archive container (RWB-TE-012) |
| Negotiable | Periods, tables and age-basis fields are rule rows; the story fixes the archive, purge and hold behavior |
| Valuable | The store keeps no row longer than its rule, and each removal is recorded |
| Estimable | One rule table, one job, one archive writer, one trigger change |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic rows with a test clock |

## 7. Acceptance criteria

```gherkin
Feature: Retention and archive rule for the data store

  Background:
    Given retention rule version "RET-2026.11" holds product "DP05", table "interaction", age basis "occurred_at", 24 months
    Given the run date is Sunday 2026-12-06

  Scenario: AC1 Retention rule applied
    Given 1,250 interaction rows with occurred_at before 2024-12-06 and 4,800 rows from 2024-12-06 onward
    When JOB-17 runs
    Then 1,250 rows move to the archive container under "retention/2026-12-06/interaction/"
    Then the 1,250 rows are no longer in the live interaction table
    Then the job run logs count 1,250 for DP05 interaction under rule version "RET-2026.11"

  Scenario: AC2 Rule changed as data
    Given retention rule version "RET-2027.01" changes DP05 interaction to 36 months, approved and valid from 2027-01-01
    Given interaction rows with occurred_at on 2024-01-15 and on 2023-12-20
    When JOB-17 runs on Sunday 2027-01-03
    Then the row from 2024-01-15 stays in the live table
    Then the row from 2023-12-20 moves to the archive container
    Then the job run logs rule version "RET-2027.01"

  Scenario: AC3 Legal hold
    Given case "RW-2024-000311" is marked legal hold and has 40 interaction rows older than 24 months
    When JOB-17 runs
    Then the system keeps its 40 rows in the live table
    Then the hold report lists case "RW-2024-000311" with 40 rows kept
    Then the summary alert to Compliance reads MSG-P1-020 with 1 case on legal hold kept

  Scenario: AC4 A rule with months outside the allowed range
    Given a retention load version "RET-2026.12" with a row for DP05 interaction at 0 months
    When the load is validated
    Then the system refuses the load in full with MSG-GEN-002 for field "retention_months" between 1 and 600
    Then version "RET-2026.11" stays in force

  Scenario: AC5 The archive write fails
    Given the archive container refuses writes
    When JOB-17 runs
    Then the system deletes no interaction row
    Then the job run ends "FAILED" with MSG-GEN-006 for system "Archive container"

  Scenario: AC6 A repeat run in the same month
    Given JOB-17 archived 1,250 rows on 2026-12-06
    When JOB-17 is rerun on 2026-12-06
    Then the system archives 0 rows
    Then the archive container still holds one set of the 1,250 rows

  Scenario: AC7 A row exactly at its retention age
    Given an interaction row with occurred_at 2024-12-06T00:00+07:00
    When JOB-17 runs on 2026-12-06
    Then the row stays in the live table

  Scenario: AC8 A rule for the decision log is refused
    Given a retention load version "RET-2026.12" with a row for product "DP12", table "decision_log_entry"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "decision_log_entry is not archived by the retention job"

  Scenario: AC9 A rerun while the job is running
    Given JOB-17 is running
    When a platform administrator posts a rerun of JOB-17
    Then the system refuses the rerun with status 409 and MSG-P2-006
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each data product and table has one retention rule in force, held as a versioned data row | Retention classes reference table (refdata.txt); DL26; Principle 1 |
| BR2 | A row older than its retention period on its age-basis field is archived and removed from the live store | retention_rule.retention_months; REQ-RDF-013 |
| BR3 | A legal hold keeps every row of the case, overriding the retention rule | R-UNI-20; recovery_case.legal_hold; NFR-072 |
| BR4 | A row is removed only after its archive copy is written and checked | Archive container (RWB-TE-012); NFR-074 |
| BR5 | The decision log is not archived by this job; its retention is set by Compliance | NFR-030; ADR-009; DL26 |
| BR6 | A retention load with an exception is refused in full | Reference data change process, step 3; CTL-08 |
| BR7 | A new version applies from its valid-from date; earlier runs keep their recorded version | R-UNI-38 |

## 9. State transitions

None. This story does not change a case status. It changes the JOB-17 run status (Running, Complete, Failed) and the retention rule version in force.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods; reads the run result (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the retention load (Reference data C) |
| Holder of Reference data A | Approves the retention load |
| RW-DATASTEW, data steward | Reads the run result for their products |
| RW-PLATADM, platform administrator | Reruns JOB-17 (Platform administration U) |
| SY-DATALOAD, data load | Runs JOB-17, writes the archive, deletes archived rows |
| SY-CASEWF, case workflow module | Answers CaseHoldQuery |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-INT-001 | interaction | id | Write |
| DF-INT-002 | interaction | case_id | Read |
| DF-INT-003 | interaction | party_id | Read |
| DF-INT-004 | interaction | occurred_at | Read |
| DF-INT-005 | interaction | channel | Read |
| DF-INT-006 | interaction | direction | Read |
| DF-INT-007 | interaction | action_code | Read |
| DF-INT-008 | interaction | contact_result | Read |
| DF-INT-009 | interaction | promise_amount | Read |
| DF-INT-010 | interaction | promise_date | Read |
| DF-INT-011 | interaction | summary | Read |
| DF-INT-012 | interaction | conduct_check | Read |
| DF-INT-013 | interaction | source_system | Read |
| DF-REF-116 | retention_rule | id | Write |
| DF-REF-117 | retention_rule | product_code | Write |
| DF-REF-118 | retention_rule | table_name | Write |
| DF-REF-119 | retention_rule | record_class | Write |
| DF-REF-120 | retention_rule | retention_months | Write |
| DF-REF-121 | retention_rule | age_basis_field | Write |
| DF-REF-123 | retention_rule | rule_version | Write |
| DF-REF-124 | retention_rule | valid_from | Write |
| DF-REF-125 | retention_rule | valid_to | Write |
| DF-REF-126 | retention_rule | approved_by | Write |

The interaction id row is written in the sense that archived rows are deleted from the live table. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz cron `0 30 2 ? * SUN#1`, Asia/Bangkok |
| Job name | JOB-17 Retention job |
| Schedule | Monthly, first Sunday |
| Input | Retention rules in force on the run date; rows of each named table; legal hold cases from CaseHoldQuery |
| Output | Archive files and manifest under `retention/YYYY-MM-DD/<table>/` in the write-once container; deleted live rows; job run checks with counts per product and table, rule version, archive location and the hold report; summary alert MSG-P1-020 to Compliance |
| Events published | None |
| Idempotency key | Run date and rule version. Selection reads live rows, so a rerun finds only rows not yet archived |
| Restart behavior | Each table and rule is one unit: archive, check, delete. A failure before the delete leaves the live rows; a rerun repeats the unit. A failure after the delete leaves a complete archive |

**Endpoints used**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| POST /api/recovery/v1/admin/reference-loads | Load retention_rule rows with validFrom | Reference data, C | 409 version clash (MSG-GEN-004); 422 invalid row (MSG-GEN-001, MSG-GEN-002) |
| POST /api/recovery/v1/admin/reference-loads/{loadId}/approve | Approve the version | Reference data, A | 404; 409 |
| GET /api/recovery/v1/admin/jobs | Read the JOB-17 run and its checks | Platform administration, R | 401; 403 (MSG-P4-002); 503 |
| POST /api/recovery/v1/admin/jobs/{jobId}/rerun | Rerun a failed JOB-17; header Idempotency-Key | Platform administration, U | 404; 409 job running (MSG-P2-006) |

**Published interfaces**

```java
// P1, called by the reference data service after approval
package recovery.dataengine.retention.api;
public interface RetentionRuleLoader {
    LoadResult apply(String ruleVersion, LocalDate validFrom, List<RetentionRuleRow> rows);
}

// P3, called by JOB-17
package recovery.casewf.api;
public interface CaseHoldQuery {
    Set<UUID> casesOnLegalHold();
    Map<UUID, String> caseNumbers(Set<UUID> caseIds);
}
```

## 13. Solution plan

- Package: folder `recovery/dataengine/retention`, Java package `recovery.dataengine.retention`.

| Component | Type | Responsibility |
|---|---|---|
| RetentionJob | Job | Quartz job for JOB-17; no concurrent run |
| RetentionService | Service | Reads rules in force, selects rows, excludes legal holds, deletes after the archive check |
| ArchiveWriter | Service | Writes JSON lines files and the manifest to the write-once container; verifies count and SHA-256 |
| RetentionRuleLoader | Published interface | Validates and stores an approved retention version |
| RetentionRuleRepository | Repository | Reads and writes retention_rule |
| RetentionRule | Entity | One row per product, table and version |
| Retention rule table | Rule table | retention_rule rows by version and valid-from date |

- Database: table retention_rule (new, Flyway migration in this story) with id uuid, product_code varchar(4), table_name varchar(60) referencing sys_objects(object_name), record_class varchar(20), retention_months integer check between 1 and 600, age_basis_field varchar(60), rule_version varchar(20), valid_from date, valid_to date, approved_by uuid, standard columns; unique (product_code, table_name, record_class, rule_version). Flyway migration replacing refuse_change() so that DELETE on interaction is allowed only when the transaction setting `recovery.retention_purge` is 'on', set by RetentionService inside its delete transaction; UPDATE stays refused, and decision_log_entry keeps the unconditional refusal. Index ix_interaction_case_time (case_id, occurred_at) from Recovery Workbench Physical Schema v4.sql serves the selection.
- Configuration and reference data: retention version "RET-2026.11" (assumed 24 months for DP05 interaction until the bank schedule arrives; DL26) prepared by Compliance and loaded by the reference data administrator; properties `rwb.dataengine.retention.archive-container` and `rwb.dataengine.retention.batch-size=5000`.
- Build steps:
  1. Flyway migration for retention_rule and the refuse_change() change; test that UPDATE and DELETE are still refused outside the purge setting and on decision_log_entry always.
  2. RetentionRuleLoader with whole-load validation: product in data_product, table in sys_objects, not decision_log_entry, months 1 to 600, age-basis field in sys_fields for the table.
  3. RetentionService selection by rule and run date, with the legal hold exclusion from CaseHoldQuery.
  4. ArchiveWriter with manifest write and read-back check.
  5. Delete step per table and rule, after the check, under the purge setting.
  6. Job run checks, hold report and the MSG-P1-020 summary alert.
  7. RetentionJob on Quartz with `@DisallowConcurrentExecution`.
  8. Tests for AC1 to AC9 and the access test.
- Feature flag: `rwb.dataengine.retention`.
- Done when: the tests in section 16 pass and the JOB-17 run book from RWB-E1-056 covers a failed run.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-020 | Retention run summary to Compliance (new, see additions) | {count} rows of {product} were archived under rule {rule} version {version}. {held} cases on legal hold were kept. |
| MSG-GEN-002 | retention_months outside 1 to 600 | {field} must be between {min} and {max}. |
| MSG-P1-002 | Retention load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | Archive container unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-17 runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | Role without the right on the job monitor | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. Compliance reads the run result, the counts and the hold report through GET /admin/jobs and the summary alert. Retention classes show on SCR-47 Personal data from Epic 8; until then they are loaded by file.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-017-01 | AC1, BR1, BR2, BR4 | System | 1,250 old and 4,800 recent synthetic interaction rows |
| TC-E1-017-02 | AC2, BR7 | System | Version RET-2027.01 at 36 months; rows from 2024-01-15 and 2023-12-20 |
| TC-E1-017-03 | AC3, BR3 | System | Case RW-2024-000311 on legal hold with 40 old rows |
| TC-E1-017-04 | AC4, BR6 | System | Load row with 0 months |
| TC-E1-017-05 | AC5, BR4 | System | Archive container stub refusing writes |
| TC-E1-017-06 | AC6 | System | JOB-17 run twice on 2026-12-06 |
| TC-E1-017-07 | AC7 | System | Row at exactly 24 months |
| TC-E1-017-08 | AC8, BR5 | System | Load row for decision_log_entry |
| TC-E1-017-09 | AC9 | System | Rerun posted during a running JOB-17 |
| TC-E1-017-10 | Access | Access | RW-COMPLY posts a rerun of JOB-17; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: periods, tables, age-basis fields and the archive location are data rows or properties.
- No personal data in logs, tests or prompts: the job run and the hold report carry counts and case numbers only; test rows are synthetic.
- No read of another module's tables: legal hold comes from CaseHoldQuery.
- The decision log is never archived or deleted by this job, and no row is deleted before its archive copy is checked.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-013 | Retention and archive rule by record class | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-RDF-17 | All recovery processes | R-UNI-20, R-UNI-38; CTL-08; DL26 | TC-E1-017-01 to TC-E1-017-09 |

## 19. Out of scope

- Retention classes for documents and the document legal hold (RWB-E1-041).
- The retention class for ledger entries as its own reference row (FEAT-ILG-10, RWB-E2-034).
- The decision log retention period (NFR-030, DL26) and the lake copy (RWB-E1-014).
- Closing a case after its retention period (REQ-S7-008, Epic 6).
- The personal data screen SCR-47 (Epic 8).

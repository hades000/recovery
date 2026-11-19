<!-- working-copy-of: requirement/legacy/14-story-updates/recovery-workbench-data-load-story-removals-v2.md -->
> **Working copy.** Canonical source: `requirement/legacy/14-story-updates/recovery-workbench-data-load-story-removals-v2.md`. Edit the source, not this copy.

# Recovery Workbench — data load story removals (v2)

## Status - no longer parked: obsolete under D-RCV-35

Date: 15 November 2026. Decision: D-RCV-35 (U1 to U5), recorded in `15 ACE DB Alignment/Recovery Workbench ACE DB Alignment Change Register v1.md`, Appendix A.

v1 parked load, job and validation content from seven stories so a later story could pick it up: RWB-E1-003, RWB-E1-004, RWB-E1-005, the inbound part of RWB-E1-007, RWB-E1-009, RWB-E1-010 and RWB-E1-012. Under D-RCV-35 that content is no longer parked for later. It is obsolete. Do not rebuild it.

D-RCV-35 rules that the Workbench loads no source data. ACE ingests every source. The recovery module reads ACE only through the SELECT-only `recovery.v_ace_*` views (ADR-010). Excel and SharePoint trackers leave system scope (U5).

The new homes:

| Content | New home |
|---|---|
| ALS, EFS, CCMS and SVAF loads (E1-003, E1-004, E1-009) and the inbound file adapters of E1-007 | ACE ingestion, raised once with the ACE team in RWB-ACE-001 |
| Tracker inventory, tracker loads and tracker retirement (E1-005, E1-010, E1-012) | Cutover plan (U5): `11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v3.docx`, section 8 Tracker retirement |

RWB-E1-007 is not removed. It survives as outbound-only adapters. Only its inbound file-load part is obsolete.

The full removal set in Appendix A of the Change Register is 11 stories. This file holds the parked content for six of them. The other five are listed for the record:

| Story | Title | New home | Parked here |
|---|---|---|---|
| RWB-E1-003 | ALS daily extract load | ACE ingestion (RWB-ACE-001) | Yes |
| RWB-E1-004 | EFS extract load | ACE ingestion (RWB-ACE-001) | Yes |
| RWB-E1-005 | Excel and SharePoint inventory | Cutover plan (U5) | Yes |
| RWB-E1-006 | Data quality rules v1 | ACE ingestion checks (RWB-ACE-001); the daily gate moves into RWB-E1-015 | No |
| RWB-E1-009 | CCMS and SVAF loads | ACE ingestion (RWB-ACE-001) | Yes |
| RWB-E1-010 | Excel and SharePoint loads | Cutover plan (U5) | Yes |
| RWB-E1-012 | Retire local copies | Cutover plan (U5) | Yes |
| RWB-E1-051 | Legacy feed jobs on ADF and Control-M | ACE ingestion (RWB-ACE-001); no ADF job remains | No |
| RWB-E2-023 | Automated EFS file load | ACE ingestion (RWB-ACE-001) | No |
| RWB-DM-001 | Migrate account and arrears | Not needed: the data is in ACE | No |
| RWB-DM-002 | Migrate customer and party | Not needed: the data is in ACE | No |
| RWB-E1-007 (inbound part only) | Integration adapters for file loads and outbound files | ACE ingestion (RWB-ACE-001); the story stays, outbound only | Yes |

Sections 1 to 6 and the appendices are the historical record of v1. They are kept as they were. Sections 7, 8 and 9 are updated.

| Item | Value |
|---|---|
| Version | v2, 15 November 2026. Supersedes v1 (v1 is kept unchanged). |
| Purpose | Record that the parked content is obsolete under D-RCV-35 and name its new home. |
| v1 purpose | Park the load, job and validation content removed from the seven v15 data-load, inventory and retirement stories. The stories then covered creation only. |
| v1 source | `14 Story Updates/Recovery Workbench Project Hub v15.html` |
| v1 date | 12 November 2026 |
| Status | Obsolete. Six of the seven stories are removed from the story set. RWB-E1-007 stays as outbound-only adapters. Nothing here is to be re-added. |

## 1. What changed in v15

The seven stories were reduced to creation work: migrations, tables, columns, keys, entities, repositories, mapper/check/service classes and endpoint contracts. Every load, job-run and validation action and AC was removed and parked here.

The story sections were also reduced to creation context:

- Flow, exception paths, business rules, state transitions, authority, contract, messages and screens now state that load execution and job scheduling are deferred.
- The solution plan keeps the tables, entities, repositories, services and controllers; job components and job build steps were removed.
- The data section is unchanged; it still lists the fields the creation must produce.

## 2. Current creation scope

| Story | Title | Creation actions | Creation ACs | Creation tests |
|---|---|---:|---:|---:|
| RWB-E1-003 | ALS daily extract load | 7 | 4 | 4 |
| RWB-E1-004 | EFS extract load | 6 | 3 | 3 |
| RWB-E1-005 | Excel and SharePoint inventory | 7 | 3 | 3 |
| RWB-E1-007 | Integration adapters for file loads and outbound files | 8 | 3 | 3 |
| RWB-E1-009 | CCMS and SVAF loads | 5 | 3 | 3 |
| RWB-E1-010 | Excel and SharePoint loads | 7 | 3 | 3 |
| RWB-E1-012 | Retire local copies | 7 | 3 | 3 |

## 3. Removed proof actions (earlier pass)

These ran the ACs, loaded test/SIT data or demoed the result. Full rows are in Appendix C.

| Story | Removed proof rows |
|---|---|
| RWB-E1-003 | A10 |
| RWB-E1-004 | A10 |
| RWB-E1-005 | A8 |
| RWB-E1-007 | A10 |
| RWB-E1-009 | A7, A8 |
| RWB-E1-010 | A9 |
| RWB-E1-012 | A8 |

## 4. Removed job actions (this pass)

These built or wired schedulers, job runners, job endpoints or job steps. Full rows are in Appendix D.

| Story | Removed job rows |
|---|---|
| RWB-E1-003 | A8, A9 |
| RWB-E1-004 | A7, A8, A9 |
| RWB-E1-005 | none |
| RWB-E1-007 | A6 |
| RWB-E1-009 | A6 |
| RWB-E1-010 | A4 |
| RWB-E1-012 | none |

## 5. Parked validation ACs and test cases

All old load, job-run and validation ACs and their test cases are parked. The full original ACs are in Appendix A and the full old test case tables in Appendix B.

| Story | Old validation ACs | Old test cases |
|---|---|---|
| RWB-E1-003 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14 | TC-E1-003-01, TC-E1-003-02, TC-E1-003-03, TC-E1-003-04, TC-E1-003-05, TC-E1-003-06, TC-E1-003-07, TC-E1-003-08, TC-E1-003-09, TC-E1-003-10, TC-E1-003-11, TC-E1-003-12, TC-E1-003-13, TC-E1-003-14, TC-E1-003-15 |
| RWB-E1-004 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10 | TC-E1-004-01, TC-E1-004-02, TC-E1-004-03, TC-E1-004-04, TC-E1-004-05, TC-E1-004-06, TC-E1-004-07, TC-E1-004-08, TC-E1-004-09, TC-E1-004-10, TC-E1-004-11 |
| RWB-E1-005 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8 | TC-E1-005-01, TC-E1-005-02, TC-E1-005-03, TC-E1-005-04, TC-E1-005-05, TC-E1-005-06, TC-E1-005-07, TC-E1-005-08, TC-E1-005-09 |
| RWB-E1-007 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9 | TC-E1-007-01, TC-E1-007-02, TC-E1-007-03, TC-E1-007-04, TC-E1-007-05, TC-E1-007-06, TC-E1-007-07, TC-E1-007-08, TC-E1-007-09, TC-E1-007-10 |
| RWB-E1-009 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11 | TC-E1-009-01, TC-E1-009-02, TC-E1-009-03, TC-E1-009-04, TC-E1-009-05, TC-E1-009-06, TC-E1-009-07, TC-E1-009-08, TC-E1-009-09, TC-E1-009-10, TC-E1-009-11, TC-E1-009-12 |
| RWB-E1-010 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13 | TC-E1-010-01, TC-E1-010-02, TC-E1-010-03, TC-E1-010-04, TC-E1-010-05, TC-E1-010-06, TC-E1-010-07, TC-E1-010-08, TC-E1-010-09, TC-E1-010-10, TC-E1-010-11, TC-E1-010-12, TC-E1-010-13, TC-E1-010-14 |
| RWB-E1-012 | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10 | TC-E1-012-01, TC-E1-012-02, TC-E1-012-03, TC-E1-012-04, TC-E1-012-05, TC-E1-012-06, TC-E1-012-07, TC-E1-012-08, TC-E1-012-09, TC-E1-012-10, TC-E1-012-11 |

## 6. E1-012 AC3 and TC-E1-012-03

The old `AC3 Business sign-off` and its `TC-E1-012-03` were removed. The old AC3 required all six teams to have retired their trackers and the report to be filed with the release checklist.

The creation-only E1-012 story now reuses `TC-E1-012-03` for its third creation AC, `AC3 Retirement endpoints created`. The old TC-03 is still parked in Appendix B and must not be confused with the new creation test.

## 7. Later homes

| Removed content | Later home |
|---|---|
| Full ALS, EFS, CCMS, SVAF and tracker load runs | SIT system test phase or a dedicated load test story |
| SIT tracker inventory and 14 tracker files | `09 Testing and quality/Recovery Workbench Test Data Plan v2.docx` or RWB-TE-004 |
| Job scheduling, retries, late paths, rerun endpoints | A later job orchestration story |
| Six-team retirement report and release sign-off | `11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v2.docx` |
| Parallel run and ten clean days | `06 Data/Recovery Workbench Data Migration Approach v2.docx` |

## 8. Pending updates (source files and embedded copies)

- `04 User stories/Recovery Workbench User Stories Epic 1 v7.md`: apply the creation-only story statements, action counts, ACs, tests and traceability.
- `04 User stories/Recovery Workbench User Stories Epic 1 v7.xlsx`: apply the same counts and AC/test changes. The embedded xlsx text copy inside the v15 hub still shows the old validation ACs and test tabs; only the story markdown view was rewritten. Both the original workbook and the embedded copy are pending.
- `04 User stories/Recovery Workbench Build Notes Epic 1 v4.md`: replace load/job step explanations with creation-only notes.
- `09 Testing and quality/Recovery Workbench Test Cases v5.xlsx`: park the old validation cases and add the new creation cases.
- `09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v4.xlsx`: point the requirement rows at the creation tests and note validation deferred.
- `09 Testing and quality/Recovery Workbench Regression Suite v5.xlsx`: remove the parked validation cases from the release suite.
- `04 User stories/Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx`: close the E1-012 AC3 row.
- `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip`: replace the per-story E1-003, E1-004, E1-005, E1-007, E1-009, E1-010 and E1-012 files.

## 9. Re-add checklist

1. Assign new AC and test case IDs in the later story or test phase.
2. Update the RTM row and the story dependency.
3. Do not restore load execution or job scheduling into the creation stories unless that work is explicitly back in scope.
4. Keep the old `TC-E1-012-03` distinct from the new creation `TC-E1-012-03`.
5. Update this file with the destination and date once a part is moved.

## Appendix A — full parked validation ACs

### RWB-E1-003 ALS daily extract load

```gherkin
Feature: ALS daily extract load

  Background:
    Given the expected business date is 2026-11-30 and the previous completed load is for 2026-11-27
    Given the mapping version "ALS-MAP-1" for INT-01 and INT-02 is approved
    Given the parameters load.hold.tolerance.pct = 0.50 and load.movement.tolerance.pct = 10.00 are in force

  Scenario: AC1 Daily load
    Given COLLINS completed the staging records for 2026-11-30 at 04:40 with 184,500 INT-01 accounts and 2,310 INT-02 payments, each with a matching trailer
    When JOB-01 runs at 05:00
    Then loan_account holds 184,500 rows with data_as_of 2026-11-30 before 07:00
    Then the load_run for INT-01 shows 184,500 read, 184,500 loaded and 0 held, with status COMPLETED
    Then the load_run for INT-02 shows 2,310 read, 2,310 loaded and 0 held
    Then one LoadCompleted event is in the outbox for each interface with business date 2026-11-30

  Scenario: AC2 Failure alerts
    Given the INT-01 trailer states 184,500 records and the staging holds 184,498
    When JOB-01 runs
    Then the system refuses the INT-01 load at DQ-003 and no loan_account row changes
    Then loan_account keeps data_as_of 2026-11-27
    Then the data steward and platform administrator groups receive MSG-P1-002 "The INT-01 load for 2026-11-30 was refused: control total. The previous load is still in use."
    Then one LoadRefused event is in the outbox with failedCheck "DQ-003"

  Scenario: AC3 Sample matches
    Given the INT-01 load for 2026-11-30 is complete
    When the sample check picks 50 accounts at random
    Then for all 50 the total_balance, days_past_due and classification equal the INT-01 staging values after mapping
    Then the load_run check results show "SAMPLE" = "50 of 50"

  Scenario: AC4 Wrong business date
    Given the INT-01 staging records and trailer carry business date 2026-11-27
    When JOB-01 runs for 2026-11-30
    Then the system refuses the load at DQ-001 with MSG-P1-002 naming "business date"
    Then no loan_account row changes

  Scenario: AC5 Duplicate account key
    Given account key "ACC0000017" appears twice in the INT-01 staging records
    When JOB-01 runs
    Then the system refuses the load at DQ-004 with MSG-P1-002 naming "keys"
    Then no loan_account row changes

  Scenario: AC6 Unmatched payments within the tolerance are held
    Given 11 of the 2,310 INT-02 payments name an account key not in loan_account, which is 0.48 percent
    When JOB-01 runs
    Then the system writes 2,299 payments to account_payment
    Then the system writes 11 dq_exception rows with check code "DQ-012", the account key and raised_on 2026-11-30
    Then the INT-02 load_run shows 11 held and status COMPLETED

  Scenario: AC7 Unmatched payments above the tolerance refuse the load
    Given 13 of the 2,310 INT-02 payments name an account key not in loan_account, which is 0.56 percent
    When JOB-01 runs
    Then the system refuses the INT-02 load at DQ-012 with MSG-P1-002
    Then the system writes no account_payment row for 2026-11-30

  Scenario: AC8 Code missing from the code map is held
    Given 3 INT-01 records carry bucket code "Z9", which is not in the code map for LOV-BUCKET
    When JOB-01 runs
    Then the system holds the 3 records in dq_exception with check code "DQ-006"
    Then the system loads 184,497 accounts

  Scenario: AC9 Movement outside the expected range
    Given the previous load for 2026-11-27 held 165,000 accounts and the load for 2026-11-30 holds 184,500, a change of 11.82 percent
    When JOB-01 runs
    Then the system loads the accounts
    Then the data steward group receives MSG-P1-006 "The INT-01 load for 2026-11-30 changed by 11.82 percent against the previous load, outside the expected 10.00 percent. Check it before use."
    Then a change of exactly 10.00 percent sends no alert

  Scenario: AC10 Late delivery
    Given COLLINS has not completed the INT-01 staging records for 2026-11-30 by 09:00
    When the last JOB-01 attempt runs at 09:00
    Then the INT-01 load_run status is LATE and loan_account keeps data_as_of 2026-11-27
    Then one LoadRefused event is in the outbox with failedCheck "LATE"
    Then the data steward group receives MSG-P1-002 "The INT-01 load for 2026-11-30 was refused: no delivery by 09:00. The previous load is still in use."

  Scenario: AC11 Rerun of a completed load
    Given the INT-01 load for 2026-11-30 is COMPLETED
    When the platform administrator calls POST /admin/jobs/{jobId}/rerun for that load
    Then the response is 409 with MSG-P1-011 "The INT-01 load for 2026-11-30 is already complete or running. It was not run again."
    Then no loan_account or load_run row changes

  Scenario: AC12 Two runs at the same time
    Given two ACE nodes fire JOB-01 for 2026-11-30 at 05:00
    When both start
    Then one load_run row exists for INT-01 and 2026-11-30
    Then loan_account holds 184,500 rows with no duplicate account_no

  Scenario: AC13 Database failure during the write
    Given the database connection is cut after 90,000 of 184,500 accounts are written in the transaction
    When the write step fails
    Then no loan_account row carries data_as_of 2026-11-30
    Then the load_run status is FAILED
    Then the attempt at 06:00 loads 184,500 accounts and sets the status to COMPLETED

  Scenario: AC14 Rerun after a refused load
    Given the INT-01 load for 2026-11-30 was refused at DQ-003
    Given COLLINS has delivered corrected staging records with a matching trailer
    When the platform administrator calls POST /admin/jobs/{jobId}/rerun for that load
    Then the response is 200 with a Job of status RUNNING
    Then the load completes with 184,500 accounts and one LoadCompleted event is in the outbox
```


### RWB-E1-004 EFS extract load

```gherkin
Feature: EFS extract load

  Background:
    Given the business date is 2026-11-30 and INT-01 is COMPLETED for 2026-11-30
    Given the INT-07 mapping version "EFS-MAP-1" is approved with sign-off reference "EFS-SIGN-2026-11-18" on 2026-11-18

  Scenario: AC1 Start-of-day file
    Given COLLINS completes the INT-07 staging records at 06:30 with 9,450 contact records for 2026-11-30 and a matching trailer
    When the JOB-01 attempt at 07:00 runs the INT-07 step
    Then collections_history holds 9,450 new rows with business date 2026-11-30, of which 1,320 carry a promise amount and date
    Then the INT-07 load_run shows 9,450 read, 9,450 loaded, status COMPLETED
    Then after the case list step, the row of case "RW-2026-000123" shows last contact 2026-11-30 15:42 and action code "PTP"

  Scenario: AC2 Mapping signed
    Given the INT-07 load for 2026-11-30 is COMPLETED
    When the data steward calls GET /admin/jobs with type "INT-07" and from 2026-11-30
    Then the Job shows mapping version "EFS-MAP-1"
    Then the mapping version in source_field_map carries approved_on 2026-11-18 and approval reference "EFS-SIGN-2026-11-18"

  Scenario: AC3 Late file
    Given COLLINS has not completed the INT-07 staging records for 2026-11-30 by 08:00
    When the INT-07 window check runs at 08:00
    Then the INT-07 load_run status is LATE
    Then one LoadRefused event is in the outbox with failedCheck "LATE"
    Then FreshnessQuery returns DP05 with business date 2026-11-27 and status STALE
    Then the data steward group receives MSG-P1-001 "DP05 Interaction is from 2026-11-27. Today's load has not arrived."
    Then collections_history keeps every row for 2026-11-27 unchanged

  Scenario: AC4 Mapping not approved
    Given the INT-07 mapping version in force is "EFS-MAP-2" with no approval
    When the INT-07 step runs
    Then the system refuses the load with MSG-P1-002 "The INT-07 load for 2026-11-30 was refused: mapping version EFS-MAP-2 not approved. The previous load is still in use."
    Then the system writes no collections_history row

  Scenario: AC5 Unknown account keys within the tolerance
    Given 40 of the 9,450 records name an account key not in loan_account, which is 0.42 percent
    When the INT-07 step runs
    Then the system writes 9,410 rows
    Then the system writes 40 dq_exception rows with check code "DQ-040"

  Scenario: AC6 Code missing from the code map
    Given 6 records carry call result "R99", which is not in the code map for LOV-CONTACT-RESULT
    When the INT-07 step runs
    Then the system holds the 6 records in dq_exception with check code "DQ-041"
    Then the system writes 9,444 rows

  Scenario: AC7 Action code outside the named list
    Given the named list efs.history.action.codes does not hold action code "SYS01"
    Given 120 records carry action code "SYS01"
    When the INT-07 step runs
    Then the system does not writ the 120 records and not held
    Then the load_run check results show "SKIPPED_ACTION_CODE" = 120

  Scenario: AC8 Same contact delivered again
    Given collections_history already holds EFS record key "EFS-77001234" from the load of 2026-11-27
    Given the 2026-11-30 delivery holds "EFS-77001234" again
    When the INT-07 step runs
    Then collections_history holds one row for "EFS-77001234"
    Then the load_run check results show "REPEATED" = 1

  Scenario: AC9 Blocking check fails
    Given the INT-07 staging records have no column "Call Result"
    When the INT-07 step runs
    Then the system refuses the load at DQ-037 with MSG-P1-002 naming "structure"
    Then one LoadRefused event is in the outbox with failedCheck "DQ-037"

  Scenario: AC10 Rerun of a completed load
    Given the INT-07 load for 2026-11-30 is COMPLETED
    When the platform administrator calls POST /admin/jobs/{jobId}/rerun for it
    Then the response is 409 with MSG-P1-011
    Then collections_history is unchanged
```


### RWB-E1-005 Excel and SharePoint inventory

```gherkin
Feature: Excel and SharePoint inventory

  Background:
    Given the parameter tracker.inventory.teams holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF

  Scenario: AC1 Inventory covers six teams
    Given an inventory file "TRK-2026.11" with 23 rows: 5 for TDR, 3 for DIL, 6 for LIT, 4 for NPA, 2 for DEBT_SALE and 3 for WRITE_OFF
    Given each row has tracker code, tracker name, location type, location, owner user ID, field list, update cycle, decision and reason
    When the reference data administrator loads it and the data steward confirms it
    Then tracker_inventory holds 23 rows for version "TRK-2026.11"
    Then GET /admin/trackers with team "LIT" returns 6 trackers, among them "LIT-07 Litigation case tracker" on SharePoint, update cycle WEEKLY, with its owner and 18 fields

  Scenario: AC2 Decision per file
    Given the loaded version "TRK-2026.11"
    When the data steward calls GET /admin/trackers
    Then every one of the 23 trackers has a decision LOAD, RETIRE or KEEP and a reason
    Then the 14 LOAD trackers each name a target data product, for example "LIT-07" names DP07
    Then the 14 LOAD and 6 RETIRE trackers have status LISTED and the 3 KEEP trackers have status KEPT

  Scenario: AC3 A team is missing
    Given an inventory file with no row for team DEBT_SALE
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-016 "The inventory has no row for team DEBT_SALE. List its trackers, or add one row with location type NONE."
    Then the system writes no tracker_inventory row

  Scenario: AC4 A row without a decision
    Given an inventory file whose row 7 has no decision
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-GEN-001 "Enter decision." for row 7

  Scenario: AC5 A value outside its list
    Given an inventory file whose row 9 has decision "MAYBE"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-007 "Row 9: decision must be one of LOAD, RETIRE, KEEP."

  Scenario: AC6 A load decision without a target data product
    Given an inventory file whose row 12 has decision LOAD and no target data product
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-GEN-001 "Enter target data product." for row 12

  Scenario: AC7 A tracker code twice
    Given an inventory file in which tracker code "NPA-02" is on rows 15 and 16
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-017 "Row 16: tracker code NPA-02 appears more than once."

  Scenario: AC8 The same file loaded again
    Given version "TRK-2026.11" is in force
    When the reference data administrator loads the same file again
    Then the system writes nothing
    Then the response carries MSG-P1-011 "The tracker inventory load for 2026-11-16 is already complete or running. It was not run again."
```


### RWB-E1-007 Integration adapters for file loads and outbound files

```gherkin
Feature: Integration adapters for file loads and outbound files

  Background:
    Given the interface configuration version "IF-2026.11" is in force
    Given interface "INT-14" WIN outbound has max attempts 3 and retry intervals 5, 15 and 45 minutes
    Given interface "INT-14" has owner role "RW-PLATADM"

  Scenario: AC1 Pattern described
    Given a developer adds the file load "INT-15" WIN proof of delivery
    When the build pipeline runs
    Then the system declares the load as an interface configuration row and uses FileLoadAdapter
    Then the contract test "INT-15" parses the synthetic sample file of 120 records and passes
    Then the architecture test finds no SFTP or file system call outside the package recovery.integration.adapter

  Scenario: AC2 File load checked
    Given a CCMS file "CCMS_COLL_20261109.txt" in SIT with 4,200 records and a trailer control total of 4,201
    When the adapter loads it
    Then the system refuses the file in full with failed check "DQ-059 Control total"
    Then the system passes no collateral record to the loader
    Then the CCMS data product keeps the load of business date 2026-11-02 in use and is marked stale
    Then the system alerts the data steward with message MSG-P1-002

  Scenario: AC3 Retry and exception queue
    Given the outbound WIN file "WIN_NOTICE_20261110.txt" for 85 notices on 85 cases
    Given the SFTP transfer fails on attempts 1, 2 and 3
    When the outbox sender runs
    Then attempt 2 starts 5 minutes after attempt 1 and attempt 3 starts 15 minutes after attempt 2
    Then each case in the file moves to route state "RETRY_QUEUE" after attempt 1 (R-UNI-33)
    Then after attempt 3 the item status is "EXCEPTION"
    Then each of the 85 cases moves to route state "EXCEPTION_QUEUE" with a task for role "RW-PLATADM" (R-UNI-34)
    Then the item shows in the exception queue with message MSG-P2-001

  Scenario: AC4 Every file check runs before any record is used
    Given a CCMS file whose business date in the header is 2026-11-02 when 2026-11-09 is expected
    When the adapter loads it
    Then the system refuses the file with failed check "DQ-057 Business date"
    Then the run row shows status "REFUSED" and record count 0

  Scenario: AC5 File missing at the cut-off
    Given no SVAF file for business date 2026-11-09 is in the inbound folder by Monday 04:00
    When JOB-09 runs
    Then the run row for "INT-11" shows status "MISSING"
    Then the system marks on 2026-11-10 the SVAF data product stale with message MSG-P1-001

  Scenario: AC6 Same file delivered twice
    Given the CCMS file for business date 2026-11-09 with hash "9f2c" was loaded at 04:05
    When the same file arrives again at 04:40
    Then the system writes a run row with status "DUPLICATE"
    Then the system passes no record to the loader

  Scenario: AC7 Duplicate application event ignored
    Given consumer "booking-confirmation" processed event key "EV-10:TRT-0001:v1"
    When the same event arrives again with the same key
    Then the consumer does not act
    Then the hit count for that key becomes 2 (R-UNI-40)

  Scenario: AC8 Two senders pick the same item
    Given outbound item "OB-0001" is due
    When two sender threads run at 10:00:00
    Then the system sends the file once
    Then the attempt count is 1

  Scenario: AC9 Resend from the exception queue
    Given outbound item "OB-0002" has status "EXCEPTION" after 3 attempts
    When a platform administrator resends it
    Then the item status is "PENDING" with attempt count 0
    Then the system writes the resend to the ACE audit log with the user and the time
    Then the response carries message MSG-GEN-005
```


### RWB-E1-009 CCMS and SVAF loads

```gherkin
Feature: CCMS and SVAF loads

  Background:
    Given the CCMS and SVAF files for business date 2026-11-27 are due on Monday 2026-11-30 at 04:00
    Given the parameter appraisal.max.age = 365 is in force

  Scenario: AC1 Daily load of the weekly files
    Given the adapter has passed the CCMS file with 31,200 collateral records and 33,050 account links, and the SVAF file with 2,140 appraisals
    When JOB-09 calls the CCMS and SVAF loaders at 04:00
    Then collateral holds 31,200 rows from the file and account_collateral holds 33,050 links to loan_account rows
    Then valuation holds 2,140 appraisals written through ValuationRecordApi, each linked to its collateral
    Then the system stores an appraisal date "15/03/2569" in the file as 2026-03-15
    Then both load_runs show status COMPLETED and FreshnessQuery returns DP06 with business date 2026-11-27

  Scenario: AC2 Sample matches
    Given both loads for 2026-11-27 are complete
    When the sample check picks 50 cases at random that have collateral
    Then for all 50 the collateral type, the title deed number and the latest appraised value equal the CCMS and SVAF file values after mapping
    Then the INT-11 load_run check results show "SAMPLE" = "50 of 50"

  Scenario: AC3 Appraisal age
    Given appraisal "APR-0045521" has appraisal date 2025-11-26, which is 366 days before 2026-11-27
    Given appraisal "APR-0045522" has appraisal date 2025-11-27, which is 365 days before 2026-11-27
    When the SVAF loader runs
    Then the system stores "APR-0045521" with stale_flag true and age_days 366
    Then the system stores "APR-0045522" with stale_flag false and age_days 365

  Scenario: AC4 CCMS file refused by the adapter
    Given the adapter refuses the CCMS file for 2026-11-27 at DQ-059 control total
    When JOB-09 runs
    Then the system does not call the CCMS loader and no collateral or account_collateral row changes
    Then the SVAF loader is still called, and appraisals for collateral not yet in DP06 are held with check code "DQ-068"

  Scenario: AC5 Links to unknown accounts within the tolerance
    Given 120 of the 33,050 account links name an account key not in loan_account, which is 0.36 percent
    When the CCMS loader runs
    Then the system writes 32,930 links
    Then the system writes 120 dq_exception rows with check code "DQ-061" and the account key

  Scenario: AC6 Appraisal for an unknown collateral
    Given 4 appraisals name collateral numbers not in collateral
    When the SVAF loader runs
    Then the system holds the 4 appraisals in dq_exception with check code "DQ-068"
    Then the system writes 2,136 appraisals

  Scenario: AC7 Collateral type missing from the code map
    Given 2 CCMS records carry collateral type code "K7", which is not in the code map for LOV-COLL-TYPE
    When the CCMS loader runs
    Then the system holds the 2 records in dq_exception with check code "DQ-062"
    Then the system writes 31,198 collateral rows

  Scenario: AC8 Unknown references above the tolerance
    Given 180 of the 33,050 account links name an account key not in loan_account, which is 0.54 percent
    When the CCMS loader runs
    Then the system refuses the INT-10 load at DQ-061 and no collateral or account_collateral row changes
    Then one LoadRefused event is in the outbox with failedCheck "DQ-061"
    Then the data steward group receives MSG-P1-002 "The INT-10 load for 2026-11-27 was refused: references. The previous load is still in use."

  Scenario: AC9 SVAF file not received
    Given no SVAF file for 2026-11-27 has passed the adapter by Tuesday 2026-12-01 04:00
    When the data steward lists the jobs for INT-11
    Then there is no INT-11 load_run for 2026-11-27 and valuation keeps the appraisals of 2026-11-20
    Then FreshnessQuery returns DP06 with status STALE, and the data steward group has received MSG-P1-001 from the freshness check

  Scenario: AC10 Valuation write fails
    Given ValuationRecordApi raises an error after 1,000 of 2,140 appraisals
    When the SVAF loader runs
    Then the system stores no appraisal from the file
    Then the INT-11 load_run status is FAILED
    Then a rerun by the platform administrator stores 2,140 appraisals

  Scenario: AC11 Loader called twice for one file
    Given the INT-10 load for 2026-11-27 is COMPLETED for interface run "IR-0000451"
    When the adapter calls the CCMS loader again for "IR-0000451"
    Then no row changes and the loader returns the outcome of the completed load
```


### RWB-E1-010 Excel and SharePoint loads

```gherkin
Feature: Excel and SharePoint loads

  Background:
    Given tracker "LIT-07 Litigation case tracker" of team LIT has decision LOAD, target data product DP07 and status LISTED
    Given its field list holds 18 fields, of which "Customer name" and "Mobile" are tagged personal

  Scenario: AC1 File loaded
    Given the file "LIT-07 Litigation tracker 2026-11-20.xlsx" with 1,240 rows, each with an account number found in loan_account
    When the data steward calls POST /admin/trackers/{trackerId}/loads with the file
    Then the response is 202 with a Job of type "TRACKER" and status RUNNING
    Then tracker_row holds 1,240 rows for LIT-07 with target data product DP07 and source file name "LIT-07 Litigation tracker 2026-11-20.xlsx"
    Then the tracker shows 1,240 file rows, 1,240 loaded, 0 rejected and status LOADED

  Scenario: AC2 Reconciled
    Given the LIT-07 load shows 1,240 file rows, 1,240 loaded and 0 rejected
    When the team manager of team LIT calls POST /admin/trackers/{trackerId}/sign-off with confirmed row count 1,240
    Then the tracker status is SIGNED_OFF with the team manager's user ID and the sign-off time

  Scenario: AC3 Rejected rows
    Given the LIT-07 file has 1,240 rows, of which 17 have no account number
    When the load runs
    Then the system writes 1,223 rows to tracker_row
    Then the system writes 17 dq_exception rows with check code "TRK-01" and record keys "LIT-07 row 14" to "LIT-07 row 1,205"
    Then the data steward and the LIT team manager receive MSG-P1-008 "1,223 rows loaded from LIT-07 Litigation tracker 2026-11-20.xlsx. 17 rows rejected; the reject list is on the load."
    Then GET /admin/data-quality/exceptions with product "DP07" returns the 17 rejected rows

  Scenario: AC4 Personal fields are dropped
    Given the LIT-07 file of 1,240 rows
    When the load runs
    Then no tracker_row holds a value for "Customer name" or "Mobile"
    Then each tracker_row holds the 16 other fields
    Then the load_run check results show "DROPPED_PERSONAL_FIELDS" = 2

  Scenario: AC5 Account number not found
    Given 5 rows of the LIT-07 file carry account numbers not in loan_account
    When the load runs
    Then the system rejects the 5 rows with check code "TRK-02"
    Then the system writes 1,235 rows

  Scenario: AC6 Counts do not match at sign-off
    Given the LIT-07 load shows 1,240 file rows, 1,223 loaded and 17 rejected
    When the team manager of team LIT signs off with confirmed row count 1,251
    Then the system refuses the sign-off with MSG-P1-009 "The counts do not match: 1,251 rows confirmed, 1,240 rows in the file, 1,223 loaded, 17 rejected. Sign-off is not allowed."
    Then the tracker status stays LOADED

  Scenario: AC7 The person who loaded cannot sign off
    Given a user who holds RW-DATASTEW and RW-TEAMMGR for team LIT loaded the LIT-07 file
    When the same user signs off
    Then the system refuses the sign-off with MSG-P7-002 "You prepared this decision, so you cannot approve it."

  Scenario: AC8 Team manager of another team
    Given the LIT-07 load is LOADED
    When the team manager of team NPA signs off LIT-07
    Then the system refuses the sign-off with 403 and MSG-P4-002

  Scenario: AC9 Tracker without a load decision
    Given tracker "TDR-03 Restructure follow-up list" has decision KEEP and status KEPT
    When the data steward uploads a file for TDR-03
    Then the system refuses the upload with MSG-P1-010 "TDR-03 cannot be loaded: its decision is KEEP and its status is KEPT."
    Then the system stores no file

  Scenario: AC10 Same file uploaded again
    Given "LIT-07 Litigation tracker 2026-11-20.xlsx" was loaded on 2026-11-20
    When the data steward uploads the same file again
    Then the response is 409 with MSG-P1-011
    Then tracker_row is unchanged

  Scenario: AC11 New file before sign-off
    Given the LIT-07 load of 2026-11-20 is LOADED with 1,223 rows and not signed off
    When the data steward uploads "LIT-07 Litigation tracker 2026-11-23.xlsx" with 1,262 rows, all matched
    Then tracker_row holds 1,262 rows for LIT-07, all from the 2026-11-23 file
    Then the load_run of 2026-11-20 has status SUPERSEDED

  Scenario: AC12 File type not allowed
    Given a file "LIT-07 tracker.pdf"
    When the data steward uploads it for LIT-07
    Then the response is 415 with MSG-P1-018 "Use an .xlsx or .csv file of at most 20 MB for a tracker load."

  Scenario: AC13 Header does not match the field list
    Given the LIT-07 file has no column "Court name", which is in the field list
    When the load runs
    Then the system refuses the load at structure with MSG-P1-002 "The LIT-07 load for 2026-11-20 was refused: structure. The previous load is still in use."
    Then no tracker_row for that file is written
```


### RWB-E1-012 Retire local copies

```gherkin
Feature: Retire local copies

  Background:
    Given the parameter tracker.retire.parallel.days = 2
    Given tracker "LIT-07 Litigation case tracker" of team LIT has decision LOAD, status SIGNED_OFF and signed off on Friday 2026-11-20

  Scenario: AC1 Team confirmation
    Given the LIT team has worked from the case list on Monday 2026-11-23 and Tuesday 2026-11-24
    When the LIT team manager calls POST /admin/trackers/{trackerId}/retire on 2026-11-25 with archive location "https://sharepoint.example/sites/lit/archive/LIT-07"
    Then the system retires the tracker status with retired_at 2026-11-25, the team manager's user ID and the archive location
    Then the system keeps the stored tracker file in the write-once store unchanged

  Scenario: AC2 Archive location
    Given LIT-07 was retired on 2026-11-25
    When the data steward calls GET /admin/trackers with status RETIRED
    Then the row for LIT-07 shows archive location "https://sharepoint.example/sites/lit/archive/LIT-07", retired on 2026-11-25, the confirming user and the stored file reference
    Then it lists the 3 fields "Hearing note", "Firm contact" and "Court room" as fields no feed carries

  Scenario: AC3 Business sign-off
    Given the six teams TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF have retired all their LOAD and RETIRE trackers by 2026-11-26
    When the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26
    Then the report holds six team rows, each with the number of trackers, the number retired, the team manager who confirmed each retirement and the date
    Then every team row shows outstanding 0
    Then the system files the report with the release checklist of 30 November 2026

  Scenario: AC4 Tracker not signed off
    Given tracker "NPA-02 Asset holding list" has decision LOAD and status LOADED
    When the NPA team manager calls the retirement for NPA-02
    Then the system refuses the retirement with MSG-P1-013 "NPA-02 cannot be retired: its decision is LOAD and its status is LOADED."

  Scenario: AC5 Parallel period not yet complete
    Given LIT-07 was signed off on 2026-11-20
    When the LIT team manager calls the retirement on Monday 2026-11-23
    Then the system refuses the retirement with MSG-P1-014 "LIT-07 can be retired from 2026-11-25, after 2 working days of use of the case list."
    Then the status stays SIGNED_OFF

  Scenario: AC6 No archive location
    Given LIT-07 can be retired
    When the LIT team manager calls the retirement with no archive location
    Then the response is 400 with MSG-GEN-001 "Enter archive location."

  Scenario: AC7 Team manager of another team
    Given LIT-07 can be retired
    When the NPA team manager calls the retirement for LIT-07
    Then the response is 403 with MSG-P4-002
    Then the status stays SIGNED_OFF

  Scenario: AC8 Retirement repeated
    Given LIT-07 was retired on 2026-11-25
    When the LIT team manager calls the retirement again on 2026-11-26
    Then the response is 200 with retired_at 2026-11-25 and no field changes

  Scenario: AC9 Two retirements at the same time
    Given two sessions of the LIT team manager read LIT-07 at version 4
    When both call the retirement
    Then one succeeds and the other is refused with 409 and MSG-GEN-004

  Scenario: AC10 A team with an outstanding tracker
    Given team NPA has retired 3 of its 4 LOAD and RETIRE trackers and NPA-02 is still LOADED on 2026-11-26
    When the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26
    Then the NPA row shows outstanding 1 with tracker code "NPA-02" and status LOADED
```


## Appendix B — full parked test cases

### RWB-E1-003 ALS daily extract load

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-003-01 | AC1, BR4, BR5 | System | Synthetic staging of 184,500 accounts and 2,310 payments for 2026-11-30 |
| TC-E1-003-02 | AC2, BR1 | System | Trailer count 184,500 against 184,498 records |
| TC-E1-003-03 | AC3, BR6, BR7 | System | Completed load; 50 random accounts |
| TC-E1-003-04 | AC4, BR1 | System | Staging and trailer dated 2026-11-27 |
| TC-E1-003-05 | AC5, BR1 | System | Account key ACC0000017 twice |
| TC-E1-003-06 | AC6, BR2 | System | 11 of 2,310 payments with unknown account keys |
| TC-E1-003-07 | AC7, BR2 | System | 13 of 2,310 payments with unknown account keys |
| TC-E1-003-08 | AC8, BR2, BR6 | System | 3 records with bucket code Z9 |
| TC-E1-003-09 | AC9, BR3 | System | Previous load 165,000 accounts; boundary at exactly 10.00 percent |
| TC-E1-003-10 | AC10, BR4 | System | Empty staging until 09:00 |
| TC-E1-003-11 | AC11, BR8 | System | Completed load; rerun call |
| TC-E1-003-12 | AC12, BR8 | System | Two scheduler nodes on one database |
| TC-E1-003-13 | AC13, BR1 | System | Connection cut after 90,000 rows |
| TC-E1-003-14 | AC14 | System | Refused load, then corrected staging |
| TC-E1-003-15 | Access | Access | RW-DATASTEW calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


### RWB-E1-004 EFS extract load

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-004-01 | AC1, BR1, BR7 | System | 9,450 synthetic EFS records delivered at 06:30; case RW-2026-000123 with two accounts |
| TC-E1-004-02 | AC2, BR2 | System | Completed load under EFS-MAP-1 |
| TC-E1-004-03 | AC3, BR5 | System | No INT-07 delivery by 08:00 |
| TC-E1-004-04 | AC4, BR2 | System | Mapping version EFS-MAP-2 without approval |
| TC-E1-004-05 | AC5, BR3 | System | 40 of 9,450 records with unknown account keys |
| TC-E1-004-06 | AC6, BR3 | System | 6 records with call result R99 |
| TC-E1-004-07 | AC7, BR4 | System | 120 records with action code SYS01 |
| TC-E1-004-08 | AC8, BR6 | System | Record key EFS-77001234 on two business dates |
| TC-E1-004-09 | AC9, BR2 | System | Staging without the column Call Result |
| TC-E1-004-10 | AC10 | System | Completed load; rerun call |
| TC-E1-004-11 | Access | Access | RW-DATASTEW calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


### RWB-E1-005 Excel and SharePoint inventory

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-005-01 | AC1, BR1, BR3 | System | Inventory file of 23 synthetic rows across the six teams |
| TC-E1-005-02 | AC2, BR2, BR5 | System | Loaded version TRK-2026.11 |
| TC-E1-005-03 | AC3, BR3, BR4 | System | File with no DEBT_SALE row |
| TC-E1-005-04 | AC4, BR2 | System | Row 7 without a decision |
| TC-E1-005-05 | AC5, BR4 | System | Row 9 with decision MAYBE |
| TC-E1-005-06 | AC6, BR2 | System | Row 12 LOAD without a target product |
| TC-E1-005-07 | AC7, BR4 | System | NPA-02 on rows 15 and 16 |
| TC-E1-005-08 | AC8, BR4 | System | Same file loaded twice |
| TC-E1-005-09 | Access | Access | PT-AGENCY user calls GET /admin/trackers; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


### RWB-E1-007 Integration adapters for file loads and outbound files

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-007-01 | AC1, BR1, BR8 | System | Synthetic INT-15 sample file, 120 records |
| TC-E1-007-02 | AC2, BR2 | System | Synthetic CCMS file, 4,200 records, trailer total 4,201 |
| TC-E1-007-03 | AC3, BR4, BR5, BR6 | System | Synthetic WIN file for 85 cases; SFTP stub failing three times |
| TC-E1-007-04 | AC4, BR2 | System | CCMS header business date 2026-11-02 |
| TC-E1-007-05 | AC5, BR3 | System | Empty SVAF inbound folder |
| TC-E1-007-06 | AC6, BR2 | System | Same CCMS file delivered twice |
| TC-E1-007-07 | AC7, BR7 | System | Event key EV-10:TRT-0001:v1 sent twice |
| TC-E1-007-08 | AC8 | System | One due item, two sender threads |
| TC-E1-007-09 | AC9 | System | Item in EXCEPTION after 3 attempts |
| TC-E1-007-10 | Access | Access | RW-CASEOWN calls POST /admin/outbound-items/{itemId}/resend; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


### RWB-E1-009 CCMS and SVAF loads

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-009-01 | AC1, BR1, BR6 | System | Synthetic CCMS file of 31,200 records and 33,050 links; SVAF file of 2,140 appraisals |
| TC-E1-009-02 | AC2 | System | Completed loads; 50 random cases with collateral |
| TC-E1-009-03 | AC3, BR4 | System | Appraisals dated 2025-11-26 and 2025-11-27 |
| TC-E1-009-04 | AC4, BR2 | System | Adapter stub refusing the CCMS file |
| TC-E1-009-05 | AC5, BR3 | System | 120 of 33,050 links with unknown account keys |
| TC-E1-009-06 | AC6, BR3 | System | 4 appraisals with unknown collateral numbers |
| TC-E1-009-07 | AC7, BR3 | System | 2 records with collateral type K7 |
| TC-E1-009-08 | AC8, BR3 | System | 180 of 33,050 links with unknown account keys |
| TC-E1-009-09 | AC9, BR5 | System | No SVAF file by 2026-12-01 04:00 |
| TC-E1-009-10 | AC10, BR8 | System | ValuationRecordApi forced to fail after 1,000 records |
| TC-E1-009-11 | AC11, BR7 | System | Second call for interface run IR-0000451 |
| TC-E1-009-12 | Access | Access | RW-DATASTEW calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


### RWB-E1-010 Excel and SharePoint loads

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-010-01 | AC1, BR1, BR7 | System | Synthetic LIT-07 file of 1,240 matched rows |
| TC-E1-010-02 | AC2, BR4 | System | LIT-07 loaded with 1,240 rows; LIT team manager |
| TC-E1-010-03 | AC3, BR2 | System | LIT-07 file with 17 rows without account numbers |
| TC-E1-010-04 | AC4, BR3 | System | Field list with two personal fields |
| TC-E1-010-05 | AC5, BR2 | System | 5 rows with unknown account numbers |
| TC-E1-010-06 | AC6, BR4 | System | Confirmed count 1,251 against 1,240 |
| TC-E1-010-07 | AC7, BR5 | System | One user with RW-DATASTEW and RW-TEAMMGR |
| TC-E1-010-08 | AC8 | System | NPA team manager signs LIT-07 |
| TC-E1-010-09 | AC9, BR1 | System | Tracker TDR-03 with decision KEEP |
| TC-E1-010-10 | AC10, BR6 | System | Same file hash twice |
| TC-E1-010-11 | AC11 | System | Second file of 1,262 rows before sign-off |
| TC-E1-010-12 | AC12 | System | PDF file |
| TC-E1-010-13 | AC13 | System | File without the column Court name |
| TC-E1-010-14 | Access | Access | RW-TEAMMGR uploads a file; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


### RWB-E1-012 Retire local copies

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-012-01 | AC1, BR1, BR2, BR5 | System | LIT-07 signed off on 2026-11-20; retirement on 2026-11-25 |
| TC-E1-012-02 | AC2, BR4 | System | Retired LIT-07 with 3 unmapped fields |
| TC-E1-012-03 | AC3 | System | Six teams with every LOAD and RETIRE tracker retired |
| TC-E1-012-04 | AC4, BR3 | System | NPA-02 in status LOADED |
| TC-E1-012-05 | AC5, BR2 | System | Retirement on 2026-11-23 |
| TC-E1-012-06 | AC6 | System | Request without archive location |
| TC-E1-012-07 | AC7, BR7 | System | NPA team manager on LIT-07 |
| TC-E1-012-08 | AC8, BR6 | System | Second retirement of LIT-07 |
| TC-E1-012-09 | AC9 | System | Two sessions at version 4 |
| TC-E1-012-10 | AC10 | System | NPA with NPA-02 still LOADED on 2026-11-26 |
| TC-E1-012-11 | Access | Access | RW-DATASTEW calls the retirement; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.


## Appendix C — removed proof action rows

### RWB-E1-003 ALS daily extract load

> | A10 | Prove the 14 ACs and publish the read interface | Run TC-E1-003-01 to TC-E1-003-15. Run the full synthetic day of 184,500 accounts and 2,310 payments in SIT and record the elapsed time. Implement and publish LoadRunQuery, and walk the platform administrator through the job list, the rerun and the LATE path. | Fourteen of fourteen AC tests pass, the full synthetic run is under 30 minutes, and P3 can read a completed load through LoadRunQuery. AC1 to AC14 |

### RWB-E1-004 EFS extract load

> | A10 | Prove the 10 ACs and demo the late path | Run TC-E1-004-01 to TC-E1-004-11. Capture the run row, the mapping version, the held and skipped counts, the DP05 freshness row and the case-list enrichment. Rehearse the 08:00 late path and the unapproved mapping refusal. | Ten of ten AC tests pass, and the data steward can explain held, skipped and refused from the run row. AC1 to AC10 |

### RWB-E1-005 Excel and SharePoint inventory

> | A8 | Prove the eight ACs and load the SIT inventory | Run TC-E1-005-01 to TC-E1-005-09. Load TRK-2026.11 in SIT and confirm at least one row for each of the six teams. Hand the 14 LOAD trackers to RWB-E1-010 and the 6 RETIRE trackers to RWB-E1-012. | Eight of eight AC tests pass, the SIT inventory holds all six teams, and the 010 and 012 leads have their lists. AC1 to AC8 |

### RWB-E1-007 Integration adapters for file loads and outbound files

> | A10 | Add the contract and boundary tests and prove the 9 ACs | Add the contract test template for a new interface, using the 120-record INT-15 sample. Add AdapterBoundaryTest to the pipeline so no SFTP or file-system call compiles outside recovery.integration.adapter. Run TC-E1-007-01 to TC-E1-007-10 and the INT-10 and INT-14 contract tests in SIT. | Nine of nine AC tests pass, the boundary test runs in the pipeline, and the INT-10 and INT-14 contract tests pass in SIT. AC1 to AC9 |

### RWB-E1-009 CCMS and SVAF loads

> | A7 | Prove the failed valuation write and the access path | Force ValuationRecordApi to fail after 1,000 of 2,140 appraisals. Confirm that no appraisal is stored, the INT-11 run is FAILED, and a platform administrator rerun stores all 2,140. Add the access test where a data steward calls the rerun and gets 403 with MSG-P4-002. | The failed write rolls back in full, the rerun stores 2,140 appraisals, and the data steward is refused. AC10 |

> | A8 | Run the 11 ACs and hand DP06 over | Run TC-E1-009-01 to TC-E1-009-12. Capture both run rows, the link counts, the age boundary, the sample and the failed valuation rollback. Walk the S5 and valuation leads through ValuationRecordApi and the stale flag. | Eleven of eleven AC tests pass, and S5 can read and update appraisals only through ValuationRecordApi. AC1 to AC11 |

### RWB-E1-010 Excel and SharePoint loads

> | A9 | Prove the 13 ACs and hand SIGNED_OFF to retirement | Run TC-E1-010-01 to TC-E1-010-14. Capture the upload Job, the row counts, the reject list, the personal-field count and every sign-off refusal. Hand the SIGNED_OFF trackers and their signed_off_at dates to RWB-E1-012. | Thirteen of thirteen AC tests pass, and the retirement lead can see which trackers are SIGNED_OFF and when the parallel period starts. AC1 to AC13 |

### RWB-E1-012 Retire local copies

> | A8 | Prove the 10 ACs and file the release report | Run TC-E1-012-01 to TC-E1-012-11. Capture the retirement fields, the unfed list, the parallel-period refusal, the repeat and the version conflict. Produce the six-team report for 26 November and walk the Tribe lead through filing it with the 30 November release checklist. | Ten of ten AC tests pass, and the report shows six teams with outstanding 0 for the full fixture. AC1 to AC10 |

## Appendix D — removed job action rows

### RWB-E1-003 ALS daily extract load

> | A8 | Build the scheduler and the late path | Build CollinsLoadJob with a 05:00 Asia/Bangkok cron on working days, a 60-minute retry to 09:00, @DisallowConcurrentExecution and the clustered job store. At 09:00 with no complete delivery, set the run LATE, publish LoadRefused with failedCheck LATE and send MSG-P1-002. | Two nodes produce one load_run and no duplicate account_no; a late delivery leaves the previous data in use and the run LATE. AC10, AC12 |

> | A9 | Build the two endpoints | Add GET /admin/jobs with type, status and date filters, and POST /admin/jobs/{jobId}/rerun with an Idempotency-Key. Require Platform administration R for the list and U for the rerun. Return 409 with MSG-P1-011 on a COMPLETED or RUNNING run, and 403 with MSG-P4-002 for a role without the right. | A completed rerun returns 409, a data steward rerun returns 403, and a refused run reruns with 200 and finishes COMPLETED. AC11, AC14 |

### RWB-E1-004 EFS extract load

> | A7 | Build the 08:00 late-delivery check | Add EfsWindowCheck as a Quartz trigger at load.window.end.INT-07. If INT-07 is not COMPLETED, set the run LATE and publish LoadRefused with failedCheck LATE. Write nothing to collections_history, so the previous history stays in place. RWB-E1-015 marks DP05 stale and sends MSG-P1-001. | With no delivery by 08:00 the run is LATE, DP05 shows 2026-11-27 STALE, the previous history is unchanged and the message is sent. AC3 |

> | A8 | Put the latest contact on the case list | Write CaseListLastContactEnricher and add it to the JOB-04 case list step. For each case, take the latest contact_at across every account linked to that case and write last_contact_at and last_action_code to case_list_row. | Case RW-2026-000123 shows last contact 2026-11-30 15:42 and action code PTP after the case list step. AC1 |

> | A9 | Add the Job fields and publish the history API | Add mappingVersion, SKIPPED_ACTION_CODE and REPEATED to the Job response of GET /admin/jobs. Implement CollectionsHistoryApi in CollectionsHistoryService and add a contract test for one account and for two accounts on one case. | GET /admin/jobs with type INT-07 shows EFS-MAP-1, and source_field_map shows the approval date and reference. The CollectionsHistoryApi contract test passes. AC2, AC7, AC8 |

### RWB-E1-005 Excel and SharePoint inventory

No job action row.

### RWB-E1-007 Integration adapters for file loads and outbound files

> | A6 | Build JOB-11 and the retry clock | Build OutboundSender as JOB-11, running every minute. Read due items with FOR UPDATE SKIP LOCKED, send through SftpTransport and mark SENT, then ACKNOWLEDGED when the acknowledgment file arrives. Read max attempts and the 5, 15 and 45 minute intervals from interface_config, and resend an item still in SENT after 30 minutes. | Two sender threads send one file once with attempt count 1, and attempts 2 and 3 start 5 and 15 minutes after the previous one. AC3, AC8 |

### RWB-E1-009 CCMS and SVAF loads

> | A6 | Wire both loaders to JOB-09 in the fixed order | Connect CcmsCollateralLoader then SvafAppraisalLoader to the P2 adapter. Prove that a CCMS refusal at the adapter does not stop the SVAF file, that unknown collateral are held under DQ-068, and that a second call for the same interface_run returns the earlier outcome without writing. | A refused CCMS file still loads SVAF with the affected appraisals held, and a repeated interface run changes no row. AC4, AC6, AC11 |

### RWB-E1-010 Excel and SharePoint loads

> | A4 | Build the load job: reject, drop and replace | Write TrackerLoadJobConfig. Reject a row with an empty account number as TRK-01 and a row with no matching loan_account as TRK-02, and write one dq_exception row with a record key such as LIT-07 row 14. Drop every field tagged personal and count the drop. Write the accepted values to tracker_row and replace the earlier rows of the tracker in one transaction. | 17 rows without an account number give 1,223 loaded and 17 TRK-01 exceptions; five unknown accounts give five TRK-02 exceptions; Customer name and Mobile are absent from every row; a new file replaces all older rows. AC3, AC4, AC5, AC11, AC13 |

### RWB-E1-012 Retire local copies

No job action row.

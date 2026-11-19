# RWB-E1-004 EFS extract load

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-004 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-04 Load collections status and contact history from EFS |
| Requirement IDs | REQ-RDF-003 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry, X6 |
| Priority | Must |
| Depends on | RWB-E1-003, RWB-E1-015, RWB-E1-002 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **the EFS contacts and promises for accounts at 90 days past due loaded each working day from the COLLINS daily batch**, so that **the contact history is on the case from its first day**.

## 2. Business rationale

When an account moves from collections to recovery today, the case owner does not see what the phone team agreed with the customer, and the customer can be called twice or asked again for a promise already made. This story loads the EFS contact and promise records (INT-07) into the collections history held by the Workbench, checked like every other load, and puts the latest contact on the case list. It meets REQ-RDF-003 and serves NFR-014 (collections data ingested at start of day).

## 3. Preconditions

- RWB-E1-003 is done: the load framework, load_run, dq_exception, source_field_map and source_code_map exist, and DP01 is loaded.
- RWB-E1-002 is done: the case list step and case_list_row exist.
- RWB-E1-015 is done: FreshnessStampService records each load and its freshness check marks a product stale at its expected-by time (08:00 for DP05).
- COLLINS writes the INT-07 records and their trailer for the business date into its staging tables in the ACE database.
- The mapping version for INT-07 and the code maps for LOV-ACTION-CODE and LOV-CONTACT-RESULT are loaded; the mapping version is approved with the EFS system owner's sign-off reference.
- Parameters are loaded: `load.window.end.INT-07` 08:00 (assumed, NFR-014 and DL11), `efs.history.action.codes` (the named list of action codes; assumed every code in LOV-ACTION-CODE until the business lead names the list, DL29).
- JOB-01 runs as service identity SY-DATALOAD.

## 4. Flow

1. Quartz: JOB-01 attempt reaches the INT-07 step after the INT-01 step has completed for the business date.
2. System: opens a load_run for INT-07 and checks that the mapping version in force is approved.
3. System: runs DQ-036 business date, DQ-037 structure, DQ-038 control total and DQ-039 keys; any failure refuses the load.
4. System: runs DQ-040 references (the account key matches loan_account) and DQ-041 lists of values; above 0.50 percent the load is refused.
5. System: skips records whose action code is not in the named list and counts them.
6. System: maps the remaining records and inserts collections_history rows by their EFS record key in one transaction; a key already held is not inserted again.
7. System: writes held records to dq_exception, runs DQ-042 movement, calls `FreshnessStampService.recordLoad` for DP05 in the same transaction, sets the status COMPLETED and publishes LoadCompleted.
8. System: the case list step of JOB-04 reads the latest contact per case from collections_history and writes it to case_list_row.
9. System: at 08:00, if INT-07 is not COMPLETED, marks the load LATE and publishes LoadRefused with failed check LATE; the freshness check of RWB-E1-015 marks DP05 stale and alerts the data steward.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No complete INT-07 delivery by 08:00 | Status LATE; LoadRefused published; DP05 stale through RWB-E1-015; the previous history stays with its freshness stamp | MSG-P1-001 | AC3 |
| X2 | The mapping version in force has no approval | Load refused in full | MSG-P1-002 | AC4 |
| X3 | Unknown account keys at or below 0.50 percent (DQ-040) | Records held; the rest loaded | None (count on the load_run) | AC5 |
| X4 | Action code or call result missing from the code map (DQ-041) | Record held; the rest loaded | None (count on the load_run) | AC6 |
| X5 | Action code not in the named list (DL29) | Record skipped and counted; not held | None | AC7 |
| X6 | A record already held is delivered again | Not inserted again; counted as repeated | None | AC8 |
| X7 | Structure, control total or key check fails | Load refused in full; nothing written; LoadRefused published | MSG-P1-002 | AC9 |
| X8 | Rerun asked for a completed load | 409; nothing changes | MSG-P1-011 | AC10 |
| X9 | A role without Platform administration U asks for a rerun | 403 | MSG-P4-002 | TC-E1-004-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the load framework of RWB-E1-003; P3 copies the history into the interaction ledger at case entry in its own story |
| Negotiable | The window end and the named list of action codes are parameters |
| Valuable | The case owner sees the last contact and promise before calling the customer |
| Estimable | One batch step, one table, two code maps, two case list columns |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic EFS records |

## 7. Acceptance criteria

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

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Contact history before day 90 comes from EFS through COLLINS | Mapping rule "Contact history"; DL29; ADR-005 |
| BR2 | A load is refused in full on a failed business date, structure, control total or key check, or an unapproved mapping | DQ-036 to DQ-039; CTL-02; Principle 1 |
| BR3 | Records with unknown references or codes are held; above 0.50 percent the load is refused | DQ-040, DQ-041; parameter load.hold.tolerance.pct (assumed, DL25) |
| BR4 | Only action codes in the named list are kept | DL29 (assumed: every code until the list is named) |
| BR5 | INT-07 must be complete by 08:00, or the load is LATE and the product is stale | Parameter load.window.end.INT-07 and data_product.expected_by (assumed, NFR-014, DL11); MSG-P1-001 |
| BR6 | A record already held is not written twice | R-UNI-40 |
| BR7 | The latest contact per case is the latest contact_at across the case's accounts | FEAT-RDF-04 |
| BR8 | Free-text notes are not loaded; only codes, dates and amounts | Mapping rule "Personal data"; CTL-11 |

## 9. State transitions

None. This story does not change a case status. It changes the INT-07 load_run status (RUNNING to COMPLETED, REFUSED or LATE). The freshness status of DP05 is changed by RWB-E1-015.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs the INT-07 step; writes collections_history, load_run, dq_exception and the case list columns; records the DP05 load through FreshnessStampService |
| RW-PLATADM, platform administrator | Lists runs (Platform administration R); reruns a refused or late load (Platform administration U) |
| RW-DATASTEW, data steward and data product owner | Lists runs (Platform administration R); records the EFS owner's sign-off on the mapping version through the reference data change process |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List runs (Platform administration R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-002 | loan_account | account_no | Read (reference check) |
| DF-INT-030 | collections_history | id | Write |
| DF-INT-031 | collections_history | account_no | Write |
| DF-INT-032 | collections_history | efs_record_key | Write |
| DF-INT-033 | collections_history | contact_at | Write |
| DF-INT-034 | collections_history | action_code | Write |
| DF-INT-035 | collections_history | action_contact_status | Write |
| DF-INT-036 | collections_history | contact_result | Write |
| DF-INT-037 | collections_history | promise_amount | Write |
| DF-INT-038 | collections_history | promise_date | Write |
| DF-INT-039 | collections_history | business_date | Write |
| DF-OPS-066 | source_field_map | mapping_version | Read |
| DF-OPS-071 | source_field_map | approved_by | Read |
| DF-OPS-072 | source_field_map | approved_on | Read |
| DF-OPS-073 | source_field_map | approval_ref | Read |
| DF-OPS-077 | source_code_map | lov_code | Read |
| DF-OPS-078 | source_code_map | source_code | Read |
| DF-OPS-079 | source_code_map | value_code | Read |
| DF-OPS-080 | source_code_map | map_version | Read |
| DF-OPS-022 | load_run | interface_id | Write |
| DF-OPS-025 | load_run | business_date | Write |
| DF-OPS-026 | load_run | status | Write |
| DF-OPS-029 | load_run | rows_read | Write |
| DF-OPS-030 | load_run | rows_loaded | Write |
| DF-OPS-031 | load_run | rows_held | Write |
| DF-OPS-034 | load_run | check_results | Write |
| DF-OPS-035 | load_run | mapping_version | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |
| DF-OPS-002 | data_product_load | product_code | Write through FreshnessStampService (RWB-E1-015) |
| DF-OPS-004 | data_product_load | business_date | Write through FreshnessStampService (RWB-E1-015) |
| DF-OPS-005 | data_product_load | source_extracted_at | Write through FreshnessStampService (RWB-E1-015) |
| DF-OPS-006 | data_product_load | loaded_at | Write through FreshnessStampService (RWB-E1-015) |
| DF-RPT-017 | case_list_row | last_contact_at | Write |
| DF-RPT-018 | case_list_row | last_action_code | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. The fields DF-INT-007 (action_code) and DF-INT-008 (contact_result) of the interaction ledger are filled from collections_history by P3 at case entry, outside this story.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-01 COLLINS load check and intake, INT-07 step, at each hourly attempt after INT-01 completes; window check at 08:00 |
| Job name | JOB-01 COLLINS load check and intake |
| Input | COLLINS staging records and trailer for INT-07 (table name `rwb.p1.collins.int07.table`) |
| Output | collections_history; load_run; dq_exception; the DP05 freshness stamp through FreshnessStampService |
| Events published | LoadCompleted (EV-26) with source INT-07; LoadRefused (EV-27) with the failed check |
| Idempotency key | interface_id and business_date for the run; efs_record_key for each row (unique) |
| Restart | A refused or late load is rerun by the next attempt or by POST /admin/jobs/{jobId}/rerun; the write is one transaction |

**Published interface** (P3 reads the history at case entry)

```java
public interface CollectionsHistoryApi {
    List<CollectionsContact> contactsForAccount(String accountNo, LocalDate fromDate, LocalDate toDate);
}

public record CollectionsContact(String efsRecordKey, OffsetDateTime contactAt, String actionCode,
        String actionContactStatus, String contactResult, BigDecimal promiseAmount, LocalDate promiseDate) {}
```

**GET /admin/jobs** and **POST /admin/jobs/{jobId}/rerun** as in RWB-E1-003; the Job for INT-07 adds `mappingVersion` and the checks SKIPPED_ACTION_CODE and REPEATED inside `checks`.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/load/efs`, Java package `recovery.dataengine.load.efs`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| EfsLoadStepConfig | Job (Spring Batch step in JOB-01) | Checks, maps and writes INT-07 |
| EfsWindowCheck | Job (Quartz trigger at 08:00) | Marks INT-07 LATE and publishes LoadRefused when the step has not completed |
| CollectionsHistory | Entity | Maps collections_history |
| CollectionsHistoryRepository | Repository | Inserts with ON CONFLICT (efs_record_key) DO NOTHING; returns the inserted count |
| CollectionsHistoryService | Service and Published interface | Implements CollectionsHistoryApi |
| LoadCheckRunner, SourceMappingService | Service (from RWB-E1-003) | Run DQ-036 to DQ-042; map through EFS-MAP-1 and the code maps |
| CaseListLastContactEnricher | Service | Called by the case list step; writes last_contact_at and last_action_code per case |

**Database.** Migration `V1_004__collections_history.sql` creates collections_history (account_no varchar(20), efs_record_key varchar(40) unique, contact_at timestamptz, action_code varchar(10), action_contact_status varchar(20), contact_result varchar(20), promise_amount numeric(18,2), promise_date date, business_date date, standard columns) with an index on (account_no, contact_at desc); adds approval_ref varchar(200) to source_field_map; adds last_contact_at timestamptz and last_action_code varchar(10) to case_list_row.

**Configuration and reference data.** Parameters `load.window.end.INT-07` and `efs.history.action.codes` from the parameter catalog, loaded by the center of excellence analyst; the named list is set by the business lead (DL29). Mapping version EFS-MAP-1 and the code maps loaded by the reference data administrator; the data steward records the EFS owner's sign-off reference. Staging table name set by the platform administrator.

**Build steps**

1. Write migration V1_004, the entity and the repository; test the unique record key.
2. Configure the INT-07 checks in LoadCheckRunner and the mapping approval check; test refusal on an unapproved mapping.
3. Write EfsLoadStepConfig with the named list filter, the held records and the repeated count.
4. Write EfsWindowCheck at the INT-07 window end with the LATE status and LoadRefused; test with RWB-E1-015 that DP05 turns STALE and MSG-P1-001 is sent.
5. Write CollectionsHistoryService and a contract test for CollectionsHistoryApi.
6. Write CaseListLastContactEnricher and add it to the case list step; test the latest contact across two accounts of one case.
7. Add the mapping version and the new checks to the Job mapping of GET /admin/jobs.

**Feature flag.** `rwb.p1.efs-load`. Off: JOB-01 skips the INT-07 step and the window check.

**Done when.** The tests in section 16 pass.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | INT-07 not complete by 08:00 | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Load refused at a check or for an unapproved mapping | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-011 | Rerun of a completed load | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The data steward receives the alerts and reads the runs through GET /admin/jobs; the team manager sees the latest contact on the Power BI case list. The contact history on the case record view comes with RWB-E1-023 and RWB-E1-035.

## 16. Test cases

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

## 17. Guardrails

- No business value in code: the window end, the named list of action codes and the mapping are data.
- No personal data in logs, tests or prompts. Free-text notes are not loaded; dq_exception holds the account key only.
- No read of another module's tables. P3 reads the history through CollectionsHistoryApi; this story never writes interaction.
- No call to EFS; the only input is the COLLINS staging records.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-003 | Contact history, promises and case status from EFS on the case | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-04 | 06 Take over and own the case | DQ-036 to DQ-042; R-UNI-40; CTL-02 | TC-E1-004-01 to TC-E1-004-11 |

## 19. Out of scope

- Copying the history into the interaction ledger at case entry (RWB-E1-018, RWB-E1-066).
- The contact history on the case record view (RWB-E1-023, RWB-E1-035).
- The automated EFS file load that replaces the manual file handling (FEAT-CHO-10, Epic 2).
- Contact repository and consent per channel (FEAT-COM-05, Epic 4).
- X6 lost contact and skip trace (FEAT-DVF-06, Epic 7).


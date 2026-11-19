<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 003 ALS daily extract load v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 003 ALS daily extract load v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-003 ALS daily extract load

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-003 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-03 Load account and arrears daily from ALS |
| Requirement IDs | REQ-RDF-002 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | 06 Take over and own the case |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-001 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **ALS balances, arrears, payments and classification loaded every working day from the COLLINS daily batch for accounts at 90 days past due or more**, so that **account and arrears data is current to the previous working day**.

## 2. Business rationale

Case owners today read balances and days past due from ALS screens and team files, so two people can see two different numbers for one account. This story loads INT-01 (accounts) and INT-02 (payments) from the COLLINS daily batch into the account and arrears data product DP01, after the seven load checks, so every case reads one checked balance with its business date. It meets REQ-RDF-002 and serves the measure "loads on time and complete on 99 percent of days" and the load target "job runs by 07:00" (NFR-013).

## 3. Preconditions

- RWB-E1-001 is done: loan_account, account_payment and data_product exist, and the catalog holds DP01.
- COLLINS writes the INT-01 and INT-02 records for the business date and a trailer row (record count, balance total, business date) into its staging tables in the ACE database. The table names are configuration values, owned by the ACE team.
- The mapping version for INT-01 and INT-02 (source_field_map) and the code map (source_code_map) are loaded and approved.
- The working day calendar is loaded in the reference data service (RWB-E1-043).
- Parameters are loaded: `load.window.end` 09:00, `load.retry.interval` 60 minutes, `load.hold.tolerance.pct` 0.50, `load.movement.tolerance.pct` 10.00, `load.sample.size` 50 (tolerances assumed, DL25).
- JOB-01 runs as service identity SY-DATALOAD.

## 4. Flow

1. Quartz: starts JOB-01 COLLINS load check and intake at 05:00 for the expected business date, the previous working day.
2. System: opens a load_run row for INT-01 with status RUNNING; the unique key (interface, business date) stops a second run.
3. System: runs DQ-001 business date, DQ-002 structure, DQ-003 control total and DQ-004 keys on the staging records; any failure refuses the load.
4. System: runs DQ-005 references and DQ-006 lists of values; records that fail are counted, and the load is refused if the count is above 0.50 percent.
5. System: maps each record through the mapping version in force and the code map, and writes loan_account in one transaction, with data_as_of set to the business date.
6. System: writes the held records to dq_exception with the check code and the account number.
7. System: runs DQ-007 movement against the previous load and alerts the data steward if it is outside 10 percent.
8. System: repeats steps 2 to 7 for INT-02 into account_payment, after INT-01 completes.
9. System: runs the sample check on 50 random accounts and writes the result to the load_run check results.
10. System: sets the load_run status to COMPLETED and publishes LoadCompleted through the outbox in the same transaction; RWB-E1-015 adds the freshness stamp to this transaction.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A blocking check fails (DQ-002, DQ-003 or DQ-008 to DQ-011) | Load refused in full; nothing written; LoadRefused published (RWB-E1-015 marks DP01 stale on it); alert sent | MSG-P1-002 | AC2 |
| X2 | Staging holds a business date other than the expected one (DQ-001) | Load refused in full | MSG-P1-002 | AC4 |
| X3 | One account key appears twice (DQ-004) | Load refused in full | MSG-P1-002 | AC5 |
| X4 | Unmatched references at or below 0.50 percent (DQ-012) | Those records held in dq_exception; the rest loaded | None (count on the load_run) | AC6 |
| X5 | Unmatched references above 0.50 percent | Load refused in full | MSG-P1-002 | AC7 |
| X6 | A source code missing from the code map (DQ-006) | Record held; the rest loaded | None (count on the load_run) | AC8 |
| X7 | Count or balance moves more than 10 percent from the previous load (DQ-007) | Loaded; data steward alerted | MSG-P1-006 | AC9 |
| X8 | No complete delivery by 09:00 | load_run status LATE; LoadRefused published with failed check LATE; previous data stays in use | MSG-P1-002 | AC10 |
| X9 | Rerun asked for a business date already COMPLETED | 409; nothing changes | MSG-P1-011 | AC11 |
| X10 | Two nodes start JOB-01 at the same time | One run proceeds; the other stops at the unique key; no duplicate rows | None | AC12 |
| X11 | The database fails during the write | The transaction rolls back; status FAILED; the next hourly attempt loads again | None (alert to the platform administrator) | AC13 |
| X12 | The data steward or another role without Platform administration U asks for a rerun | 403 | MSG-P4-002 | TC-E1-003-15 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the tables and catalog of RWB-E1-001; case creation and allocation read the result later |
| Negotiable | Tolerances, the window end and the sample size are parameters; the mapping is data |
| Valuable | Every case reads one checked balance and days past due, current to the previous working day |
| Estimable | One Quartz job, two Spring Batch steps, one check runner, two endpoints |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic staging data |

## 7. Acceptance criteria

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

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A load is refused in full if the business date, structure, control totals or keys fail; the previous load stays in use and LoadRefused is published | DQ-001 to DQ-004, DQ-008 to DQ-011; INT-01 and INT-02 error handling; CTL-02 |
| BR2 | A record whose reference or code does not match is held in the exception list; above 0.50 percent the load is refused | DQ-005, DQ-006, DQ-012, DQ-013; parameter load.hold.tolerance.pct (assumed, DL25) |
| BR3 | A count or balance change above 10 percent against the previous load is loaded and alerted | DQ-007, DQ-014; parameter load.movement.tolerance.pct (assumed, DL25) |
| BR4 | JOB-01 starts at 05:00 and retries every hour until 09:00 | JOB-01; INT-01 retry |
| BR5 | Every loaded row carries the business date of its load in data_as_of | Mapping rule "Business date"; DF-ACC-021, DF-ACC-028 |
| BR6 | Buddhist Era years become Gregorian dates; amounts are THB numeric with two decimals; source codes map through the versioned code map | Mapping rules "Dates", "Amounts", "Codes" |
| BR7 | Source fields map to Workbench fields through the approved mapping version in force; an unapproved mapping refuses the load | Principle 1; source_field_map |
| BR8 | A repeated run for a completed business date changes nothing | R-UNI-40 |
| BR9 | Load results are recorded on the load_run, not in the decision log, because a decision log entry needs a case (DF-DEC-002); case decisions taken from this data write their own entries | Principle 5; ADR-009 |

## 9. State transitions

None. This story does not change a case status. It changes the load_run status (RUNNING to COMPLETED, REFUSED, LATE or FAILED). The stale flag of DP01 is set by RWB-E1-015 from the LoadRefused event.

| From | Event | Condition | To |
|---|---|---|---|
| None | JOB-01 trigger | No run for the interface and date | RUNNING |
| RUNNING | Checks and write done | All blocking checks pass | COMPLETED |
| RUNNING | Check failed | A blocking check fails or held records above 0.50 percent | REFUSED |
| RUNNING | No delivery | Window end 09:00 passed | LATE |
| RUNNING | Write error | Database or step error | FAILED |
| REFUSED, LATE, FAILED | Rerun or next attempt | Delivery present | RUNNING |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs JOB-01; writes loan_account, account_payment, load_run, dq_exception and the DP01 status |
| RW-PLATADM, platform administrator | Lists jobs (Platform administration R) and reruns a refused, late or failed load (Platform administration U) |
| RW-SECADM, security administrator | Lists and reruns (Platform administration CRUDA); used only under break-glass |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY | List jobs and their checks (Platform administration R); no rerun |
| Data steward group, platform administrator group | Receive the load alerts |

No approval level from the delegation of authority applies.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-001 to DF-ACC-021 | loan_account | all fields | Write (insert or update by account_no) |
| DF-ACC-002 | loan_account | account_no | Read (reference check for INT-02, sample check) |
| DF-ACC-022 to DF-ACC-028 | account_payment | all fields | Write (insert by account and payment_code) |
| DF-OPS-021 | load_run | id | Write |
| DF-OPS-022 | load_run | interface_id | Write |
| DF-OPS-023 | load_run | job_code | Write |
| DF-OPS-024 | load_run | product_code | Write |
| DF-OPS-025 | load_run | business_date | Write |
| DF-OPS-026 | load_run | status | Write |
| DF-OPS-027 | load_run | started_at | Write |
| DF-OPS-028 | load_run | ended_at | Write |
| DF-OPS-029 | load_run | rows_read | Write |
| DF-OPS-030 | load_run | rows_loaded | Write |
| DF-OPS-031 | load_run | rows_held | Write |
| DF-OPS-033 | load_run | failed_check | Write |
| DF-OPS-034 | load_run | check_results | Write |
| DF-OPS-035 | load_run | mapping_version | Write |
| DF-OPS-041 | dq_exception | id | Write |
| DF-OPS-042 | dq_exception | load_run_id | Write |
| DF-OPS-043 | dq_exception | product_code | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-046 | dq_exception | reason_code | Write |
| DF-OPS-047 | dq_exception | detail | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |
| DF-OPS-049 | dq_exception | status | Write |
| DF-OPS-065 | source_field_map | interface_id | Read |
| DF-OPS-066 | source_field_map | mapping_version | Read |
| DF-OPS-067 | source_field_map | source_field | Read |
| DF-OPS-068 | source_field_map | target_entity | Read |
| DF-OPS-069 | source_field_map | target_field | Read |
| DF-OPS-070 | source_field_map | transformation | Read |
| DF-OPS-071 | source_field_map | approved_by | Read |
| DF-OPS-072 | source_field_map | approved_on | Read |
| DF-OPS-074 | source_field_map | valid_from | Read |
| DF-OPS-076 | source_code_map | interface_id | Read |
| DF-OPS-077 | source_code_map | lov_code | Read |
| DF-OPS-078 | source_code_map | source_code | Read |
| DF-OPS-079 | source_code_map | value_code | Read |
| DF-OPS-080 | source_code_map | map_version | Read |
| DF-OPS-081 | source_code_map | valid_from | Read |
| DF-OPS-082 | source_code_map | valid_to | Read |
| DF-REF-027 to DF-REF-033 | lov_value | all fields | Read through the P4 published interface (code map targets) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz cron 05:00 Asia/Bangkok on working days, then every 60 minutes until 09:00, until INT-01 and INT-02 are COMPLETED or REFUSED |
| Job name | JOB-01 COLLINS load check and intake (this story builds the INT-01 and INT-02 steps) |
| Input | COLLINS staging records and trailer for INT-01 and INT-02 in the ACE database; table names from `rwb.p1.collins.int01.table`, `rwb.p1.collins.int02.table`, `rwb.p1.collins.trailer.table` |
| Output | loan_account, account_payment, load_run, dq_exception |
| Events published | LoadCompleted (EV-26: source, businessDate, rows, checks) on completion; LoadRefused (EV-27: source, businessDate, failedCheck) on refusal; both through the outbox in the same transaction as the load_run status |
| Idempotency key | interface_id and business_date; unique index on load_run where status in ('RUNNING','COMPLETED') |
| Restart | A FAILED or LATE run is attempted again at the next hourly trigger or by rerun; the write step runs again from its start, because it writes in one transaction |

**GET /admin/jobs** (API-P1-001)

| Item | Value |
|---|---|
| Request | Query `type` (interface or job code, for example INT-01), `status`, `from`, `to` (business dates) |
| Response 200 | `Job[]`: id (load_run.id), type (interface_id), businessDate, status, startedAt, endedAt, checks (object: check code to PASS, FAIL, HELD n or NOT_APPLICABLE, plus SAMPLE) |
| 401, 403, 503 | No session (MSG-P4-001); role lacks the right (MSG-P4-002); database unavailable |
| Authorization | Platform administration R, scope All |
| Idempotency | Read only |

**POST /admin/jobs/{jobId}/rerun** (API-P1-002)

| Item | Value |
|---|---|
| Request | Path `jobId` (load_run.id); header `Idempotency-Key` |
| Response 200 | `Job` of the new attempt, status RUNNING |
| 404 | No load_run with that id (MSG-P4-003, as the E404 response defines) |
| 409 | The load for that interface and date is COMPLETED or RUNNING (MSG-P1-011) |
| 401, 403, 503 | As above; 403 uses MSG-P4-002 |
| Authorization | Platform administration U |
| Idempotency | A second call with the same Idempotency-Key returns the first response |

**Published interface** (other P1 packages and P3 read the load result)

```java
public interface LoadRunQuery {
    Optional<LoadRunView> completedLoad(String interfaceId, LocalDate businessDate); // empty when not COMPLETED
}

public record LoadRunView(UUID loadRunId, String interfaceId, LocalDate businessDate, String status,
        int rowsLoaded, int rowsHeld, OffsetDateTime endedAt) {}
```

## 13. Solution plan

**Package.** Folder `recovery/dataengine/load` for the load framework and `recovery/dataengine/load/als` for the ALS steps; Java packages `recovery.dataengine.load` and `recovery.dataengine.load.als`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CollinsLoadJob | Job (Quartz) | JOB-01 trigger; computes the expected business date from the working day calendar; launches the Spring Batch job per interface in order |
| AlsLoadJobConfig | Job (Spring Batch) | Steps: open run, blocking checks, tolerance checks, map and write, movement check, sample check, close run |
| LoadCheckRunner | Service | Runs DQ checks by SQL over the staging records and returns a CheckResult per check code |
| SourceMappingService | Service | Reads the approved mapping version and code map in force; maps one staging record to a loan_account or account_payment value |
| LoanAccountWriter, AccountPaymentWriter | Repository | Upsert by account_no; insert by (account_id, payment_code) with ON CONFLICT DO NOTHING |
| LoadRun, DqException | Entity | Map load_run and dq_exception |
| LoadRunRepository, DqExceptionRepository | Repository | Read and write the module's load tables |
| LoadRunQueryService | Service and Published interface | Implements LoadRunQuery over load_run |
| LoadEventPublisher | Service | Writes LoadCompleted and LoadRefused to the outbox |
| LoadAlertNotifier | Service | Sends MSG-P1-002 and MSG-P1-006 through the ACE notification path to the recipient groups in reference data |
| RecoveryDataEngineController | Controller | GET /admin/jobs and POST /admin/jobs/{jobId}/rerun |

**Database.** Writes loan_account (all columns) and account_payment (all columns). Adds `uk_loan_account_no UNIQUE (account_no)` if not present and `uk_account_payment UNIQUE (account_id, payment_code)`. Migration `V1_003__load_run.sql` creates load_run, dq_exception, source_field_map and source_code_map, and creates `uk_load_run_active UNIQUE (interface_id, business_date) WHERE status IN ('RUNNING','COMPLETED')` and an index on dq_exception (product_code, raised_on).

**Configuration and reference data.** Parameters `load.window.end`, `load.retry.interval`, `load.hold.tolerance.pct`, `load.movement.tolerance.pct`, `load.sample.size` from the parameter catalog (RWB-E1-042), loaded by the center of excellence analyst. Mapping version and code map for INT-01 and INT-02, loaded by the reference data administrator and approved by the data steward. Staging table names and alert recipient groups as configuration, set by the platform administrator. Working day calendar from the reference data service (RWB-E1-043).

**Build steps**

1. Write migration V1_003 and the LoadRun, DqException, SourceFieldMap and SourceCodeMap entities with repositories; test the unique run key.
2. Write LoadCheckRunner with the seven checks for INT-01 and INT-02 as SQL over staging; unit test each check with a pass and a fail fixture, and the 0.50 and 10.00 percent boundaries.
3. Write SourceMappingService with the transformations COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP and BUSINESS_DATE; refuse when the mapping version has no approval.
4. Write the INT-01 step: map and upsert loan_account in one transaction; write held records to dq_exception.
5. Write the INT-02 step in the same way into account_payment, run after INT-01 completes.
6. Write the movement and sample checks and store their results in load_run.check_results.
7. Write LoadRunQueryService, LoadEventPublisher and LoadAlertNotifier; test that a refusal writes the LoadRefused event in the same transaction as the REFUSED status.
8. Write CollinsLoadJob with the cron, the hourly retry to the window end, @DisallowConcurrentExecution and the clustered job store.
9. Write the two endpoints with capability checks, the Job mapping and the Idempotency-Key handling.

**Feature flag.** `rwb.p1.als-load`. Off: JOB-01 skips the INT-01 and INT-02 steps and records nothing.

**Done when.** The tests in section 16 pass, and a full synthetic run of 184,500 accounts completes in under 30 minutes in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | Load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-006 | Movement outside the expected range | The {source} load for {date} changed by {pct} percent against the previous load, outside the expected {limit} percent. Check it before use. |
| MSG-P1-011 | Rerun of a completed or running load | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The data steward and the platform administrator receive the alerts and read the run through GET /admin/jobs. SCR-44 Interface and job monitor shows the same runs with the states Running, Failed and Complete from E2.

## 16. Test cases

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

## 17. Guardrails

- No business value in code: tolerances, window times, sample size, mappings and code maps are data.
- No personal data in logs, tests or prompts. dq_exception.record_key holds the account key only; test data is synthetic in DEV and masked in SIT.
- No read of another module's tables. Reference values come through the P4 published interface; case data is not read.
- No call to ALS or any system of record; the only input is the COLLINS staging records (ADR-005).
- No partial load is ever visible: the write is one transaction per interface.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-002 | Balances, arrears, payments and classification current to the previous working day | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-03 | 06 Take over and own the case | DQ-001 to DQ-014; R-UNI-40; CTL-02 | TC-E1-003-01 to TC-E1-003-15 |

## 19. Out of scope

- Case creation from the loaded accounts (JOB-02, RWB-E1-018).
- Payment matching to plans and settlements (JOB-07, Epic 2 and later).
- The data quality rules on loaded rows (RWB-E1-006) and the daily reconciliation (RWB-E1-011).
- The freshness stamp, the stale flag on LoadRefused, the check at 08:00 and MSG-P1-001 (RWB-E1-015).
- The SCBPDM and UDP loads (INT-04, INT-05) and the EFS load (RWB-E1-004).
- The job monitor screen SCR-44 (Epic 2).

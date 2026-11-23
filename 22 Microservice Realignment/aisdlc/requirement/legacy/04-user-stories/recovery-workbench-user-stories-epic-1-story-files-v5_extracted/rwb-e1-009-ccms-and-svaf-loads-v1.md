<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 009 CCMS and SVAF loads v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 009 CCMS and SVAF loads v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-009 CCMS and SVAF loads

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-009 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-05 Load collateral records from CCMS; FEAT-RDF-06 Load appraisal values from SVAF |
| Requirement IDs | REQ-RDF-004 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | 07 Route, settle and claim; 09 Dispose assets and sell debt |
| Decision | D6.1 |
| Priority | Must |
| Depends on | RWB-E1-003, RWB-E1-015, RWB-E1-007 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **collateral records from CCMS and appraisals from SVAF loaded from their weekly files and linked to the loan accounts**, so that **the collateral and asset data product DP06 is current without anyone looking the values up in CCMS or SVAF**.

## 2. Business rationale

Case owners and sale officers look up collateral and appraisal values in CCMS and SVAF by hand today, and the appraisal used for a decision is often more than a year old without anyone seeing it. This story loads the weekly CCMS (INT-10) and SVAF (INT-11) files that the file adapters receive and check, links each collateral to its accounts, and flags every appraisal older than the age limit at load. It meets REQ-RDF-004 and supports control CTL-27 (an asset is priced only on an appraisal inside its age limit).

## 3. Preconditions

- RWB-E1-007 is done: JOB-09 File loads in the P2 adapter receives each file, writes its interface_run, runs the business date, structure, control total and key checks, refuses a repeated file, and passes the records to the `RecordLoader` the owning module provides.
- RWB-E1-003 is done: load_run, dq_exception, the mapping tables and the load check runner exist, and loan_account is loaded.
- RWB-E1-015 is done: `FreshnessStampService.recordLoad` stamps each load, and its freshness check marks a weekly product stale when its file has not loaded.
- The mapping versions for INT-10 and INT-11 and the code maps for LOV-COLL-TYPE, LOV-PROVINCE and LOV-APPRAISAL are loaded and approved.
- Parameters are loaded: `appraisal.max.age` 365 days (assumed, MSG-S5-002 and CTL-27; DL11), `load.hold.tolerance.pct` 0.50 and `load.movement.tolerance.pct` 10.00 (assumed, DL25).
- S1 code owners accept the published interface `ValuationRecordApi` and its writer in package `recovery.valuation`, built in this story.
- The loaders run as service identity SY-DATALOAD.

## 4. Flow

1. File adapter (P2): JOB-09 receives the CCMS file for the week, passes its file checks, and calls `CcmsCollateralLoader.load("INT-10", businessDate, records)`.
2. System: opens a load_run for INT-10 with the interface_run reference.
3. System: runs DQ-061 references (each account link matches loan_account) and DQ-062 lists of values; above 0.50 percent the file is refused.
4. System: upserts collateral by collateral_no and replaces the account_collateral links of each loaded collateral, in one transaction.
5. System: runs DQ-063 movement, calls `FreshnessStampService.recordLoad` for DP06, sets COMPLETED, publishes LoadCompleted and returns the LoadOutcome to the adapter.
6. File adapter (P2): after INT-10, calls `SvafAppraisalLoader.load("INT-11", businessDate, records)` for the SVAF file.
7. System: opens a load_run for INT-11 and runs DQ-068 references (each appraisal names a collateral in DP06) and DQ-069 lists of values.
8. System: for each appraisal, computes the age in days at the file's business date and sets the stale flag when the age is above `appraisal.max.age`.
9. System: writes the appraisals through `ValuationRecordApi.upsertAppraisals` in the same transaction as the load_run status; runs DQ-070 movement and the sample check; stamps DP06; publishes LoadCompleted.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An appraisal is older than the age limit | Loaded with stale_flag true and its age in days | None (flag on the row) | AC3 |
| X2 | The adapter refuses the CCMS file at a file check | The CCMS loader is not called; collateral keeps the previous week; the SVAF file still loads | None from P1 (the adapter alerts, RWB-E1-007) | AC4 |
| X3 | Account links to unknown accounts at or below 0.50 percent (DQ-061) | Those links held; the rest loaded | None (count on the load_run) | AC5 |
| X4 | An appraisal names a collateral not in DP06 (DQ-068) | The appraisal held | None (count on the load_run) | AC6 |
| X5 | A collateral type code is not in the code map (DQ-062) | The record held | None (count on the load_run) | AC7 |
| X6 | Unknown references above 0.50 percent | The file is refused in full; LoadRefused published; alert sent | MSG-P1-002 | AC8 |
| X7 | No SVAF file has loaded for the week | No INT-11 load_run; valuation unchanged; DP06 stale through RWB-E1-015 | MSG-P1-001 | AC9 |
| X8 | ValuationRecordApi fails during the write | The INT-11 transaction rolls back; status FAILED; rerun | None (alert to the platform administrator) | AC10 |
| X9 | The loader is called again for a file it has COMPLETED | Nothing is written; the earlier outcome is returned | None | AC11 |
| X10 | A role without Platform administration U asks for a rerun | 403 | MSG-P4-002 | TC-E1-009-12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the file adapters of RWB-E1-007 and the load framework of RWB-E1-003; S1 uses the valuations from Epic 4 |
| Negotiable | The age limit and the tolerances are parameters; the mappings are data |
| Valuable | Collateral and appraisal values are on the case, with old appraisals flagged |
| Estimable | Two record loaders on one framework, one published interface |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic files |

## 7. Acceptance criteria

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

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Collateral and appraisals arrive by weekly file through the file adapters; no call to CCMS or SVAF | INT-10, INT-11; JOB-09; ADR-005; RWB-E1-007 |
| BR2 | The adapter runs the business date, structure, control total and key checks; the loader runs the reference, list and movement checks | DQ-057 to DQ-070; CTL-02 |
| BR3 | Records with unknown references or codes are held; above 0.50 percent the file is refused | Parameter load.hold.tolerance.pct (assumed, DL25) |
| BR4 | An appraisal older than appraisal.max.age days at the business date is stale | Parameter appraisal.max.age, 365 assumed (MSG-S5-002, CTL-27; DL11) |
| BR5 | The data product is stale when the week's file has not loaded | INT-10 and INT-11 retry rule; RWB-E1-015; MSG-P1-001 |
| BR6 | Buddhist Era years become Gregorian; amounts are THB with two decimals | Mapping rules "Dates" and "Amounts" |
| BR7 | A file already loaded is not loaded again | R-UNI-40 |
| BR8 | Valuations are written only through the S1 published interface | ADR-002; DT08 |

## 9. State transitions

None. This story does not change a case status. It changes the INT-10 and INT-11 load_run status (RUNNING to COMPLETED, REFUSED or FAILED). The freshness status of DP06 is changed by RWB-E1-015.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs the loaders; writes collateral, account_collateral, load_run and dq_exception; calls ValuationRecordApi (Asset and disposal CU) |
| RW-PLATADM, platform administrator | Lists runs (Platform administration R); reruns a refused or failed load (Platform administration U) |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List runs (Platform administration R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-COL-001 to DF-COL-013 | collateral | all fields | Write (insert or update by collateral_no; occupancy and encumbrance_status are not overwritten) |
| DF-COL-014 to DF-COL-017 | account_collateral | all fields | Write |
| DF-COL-018 to DF-COL-027 | valuation | all fields | Write through ValuationRecordApi (valuer_partner_id empty in E1; accepted false) |
| DF-ACC-001 | loan_account | id | Read |
| DF-ACC-002 | loan_account | account_no | Read (reference check) |
| DF-COL-043 | valuation | stale_flag | Write through ValuationRecordApi |
| DF-COL-044 | valuation | age_days | Write through ValuationRecordApi |
| DF-OPS-022 | load_run | interface_id | Write |
| DF-OPS-023 | load_run | job_code | Write |
| DF-OPS-025 | load_run | business_date | Write |
| DF-OPS-026 | load_run | status | Write |
| DF-OPS-029 | load_run | rows_read | Write |
| DF-OPS-030 | load_run | rows_loaded | Write |
| DF-OPS-031 | load_run | rows_held | Write |
| DF-OPS-034 | load_run | check_results | Write |
| DF-OPS-036 | load_run | interface_run_id | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |
| DF-OPS-002 | data_product_load | product_code | Write through FreshnessStampService (RWB-E1-015) |
| DF-OPS-004 | data_product_load | business_date | Write through FreshnessStampService (RWB-E1-015) |
| DF-OPS-006 | data_product_load | loaded_at | Write through FreshnessStampService (RWB-E1-015) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Record loaders** (P1 implements the P2 interface of RWB-E1-007)

```java
public interface RecordLoader<T> {
    LoadOutcome load(String interfaceId, LocalDate businessDate, Stream<T> records);
}
// P1 provides CcmsCollateralLoader implements RecordLoader<CcmsCollateralRecord> for INT-10
// and SvafAppraisalLoader implements RecordLoader<SvafAppraisalRecord> for INT-11
```

| Item | Value |
|---|---|
| Trigger | JOB-09 File loads (P2), weekly Monday 04:00 or on a file arriving after its due time; the adapter calls INT-10 before INT-11 |
| Job name | JOB-09 File loads |
| Input | Checked records of the CCMS and SVAF files with the interface run ID and business date |
| Output | collateral, account_collateral, valuation (through S1), load_run, dq_exception, the DP06 freshness stamp; LoadOutcome (status, rows read, loaded, held, failed check) back to the adapter |
| Events published | LoadCompleted (EV-26) per interface; LoadRefused (EV-27) when the loader refuses |
| Idempotency key | interface_run_id; and interface_id with business_date for COMPLETED runs |
| Restart | A refused or failed load is rerun by POST /admin/jobs/{jobId}/rerun, which asks the adapter to pass the stored file again |

**Published interface** (S1, built in this story)

```java
public interface ValuationRecordApi {
    int upsertAppraisals(List<AppraisalRecord> records, UUID loadRunId); // insert or update by appraisal_no, in the caller's transaction
}

public record AppraisalRecord(String appraisalNo, UUID collateralId, String appraisalType, BigDecimal appraisedValue,
        BigDecimal forcedSaleValue, LocalDate appraisalDate, boolean staleFlag, int ageDays) {}
```

**GET /admin/jobs** and **POST /admin/jobs/{jobId}/rerun** as in RWB-E1-003; Job.type is INT-10 or INT-11.

## 13. Solution plan

**Package.** Folders `recovery/dataengine/load/ccms` and `recovery/dataengine/load/svaf`, Java packages `recovery.dataengine.load.ccms` and `recovery.dataengine.load.svaf`; the S1 interface in `recovery/valuation/api`, its writer in `recovery/valuation`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CcmsCollateralLoader | Service (RecordLoader) | DQ-061 to DQ-063; maps and writes collateral and account_collateral |
| SvafAppraisalLoader | Service (RecordLoader) | DQ-068 to DQ-070; maps, computes age and stale flag, calls ValuationRecordApi; sample check |
| AppraisalAgeCalculator | Service | Age in days from appraisal date to business date; stale when above the parameter |
| CollateralRepository, AccountCollateralRepository | Repository | Upsert by collateral_no; replace links per loaded collateral |
| ValuationRecordApi, ValuationRecordWriter | Published interface | S1 interface and its JPA writer for valuation |
| LoadCheckRunner, SourceMappingService, LoadEventPublisher | Service (from RWB-E1-003) | Run the checks; map through the approved versions; publish events |

**Database.** Writes collateral, account_collateral and valuation. Migration `V1_009__valuation_age.sql` adds stale_flag boolean not null default false and age_days integer to valuation, `uk_collateral_no UNIQUE (collateral_no)`, `uk_account_collateral UNIQUE (account_id, collateral_id)` and `uk_valuation_appraisal_no UNIQUE (appraisal_no)`, and adds interface_run_id uuid to load_run with a unique index on (interface_run_id).

**Configuration and reference data.** Parameters `appraisal.max.age`, `load.hold.tolerance.pct` and `load.movement.tolerance.pct` from the parameter catalog, loaded by the center of excellence analyst. Mapping versions and code maps loaded by the reference data administrator and approved by the data steward. File locations, due times and file checks belong to the adapter configuration of RWB-E1-007.

**Build steps**

1. Write migration V1_009 and the repositories; test the unique keys.
2. Write CcmsCollateralLoader with the INT-10 checks and the link replacement; test held links and the 0.50 percent boundary.
3. Write ValuationRecordApi and ValuationRecordWriter in the S1 package with a contract test.
4. Write AppraisalAgeCalculator; test 365 and 366 days and a leap year.
5. Write SvafAppraisalLoader with the INT-11 checks and the call to ValuationRecordApi in one transaction.
6. Connect both loaders to the adapter and test the repeated call for one interface run.
7. Add the FreshnessStampService call and the events; add the sample check over 50 cases with collateral.

**Feature flag.** `rwb.p1.collateral-load`. Off: the loaders return status SKIPPED and write nothing.

**Done when.** The tests in section 16 pass.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | Loader refuses a file above the tolerance | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P1-001 | DP06 stale (sent by the freshness check of RWB-E1-015) | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

MSG-S5-002 is shown to the sale officer when pricing on a stale appraisal; that check belongs to S5.

## 15. Screens and states

No screen in this story. The data steward receives the alerts and reads the runs through GET /admin/jobs. Collateral and valuations appear on the case record view through RWB-E1-023; SCR-44 shows the file loads from E2.

## 16. Test cases

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

## 17. Guardrails

- No business value in code: the age limit and tolerances are parameters; mappings and code maps are data.
- No personal data in logs, tests or prompts. Title deed and plot numbers appear only in synthetic test files.
- No read of another module's tables. valuation is written only through ValuationRecordApi; the adapter's tables are not read.
- The load never overwrites occupancy or encumbrance_status, which the Workbench owns.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-004 | Collateral and appraisal values on the case without a lookup in CCMS or SVAF | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-05, FEAT-RDF-06 | 07 Route, settle and claim; 09 Dispose assets and sell debt | DQ-057 to DQ-070; R-UNI-40; CTL-02; CTL-27 | TC-E1-009-01 to TC-E1-009-12 |

## 19. Out of scope

- Receiving the files and the file checks (RWB-E1-007).
- Ordering a new appraisal when the last one is stale (FEAT-VAL-01, Epic 4).
- Valuer identity from the partner panel (S9, Epic 2).
- AMIS and RPS asset loads (INT-12, INT-13, Epic 3).
- Same-day collateral or appraisal data (DL06).
- Encumbrance and occupancy updates by the Workbench (S5).

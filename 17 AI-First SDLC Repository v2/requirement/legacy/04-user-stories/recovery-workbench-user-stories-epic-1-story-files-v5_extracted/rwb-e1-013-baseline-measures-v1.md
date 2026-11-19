<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 013 Baseline measures v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 013 Baseline measures v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-013 Baseline measures

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-013 |
| Epic | E1, release 30 November 2026 |
| Module | P9 Reporting |
| Feature | FEAT-RDF-19 Publish baseline measures for the recovery portfolio; FEAT-RPT-01 Publish the reporting baseline |
| Requirement IDs | REQ-RDF-012 |
| BRD section | Business Requirements Epic 1, sections 3.8 and 4 |
| L3 process | 15 Manage performance, data and AI |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-029, RWB-E1-018 |
| Status | Ready for build |

## 1. Story

As the **Tribe lead (RW-TRIBE)**, I want **cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with definitions agreed by the Tribe**, so that **every later epic is measured against the same baseline**.

## 2. Business rationale

Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. This story holds each measure's definition, data product and formula as an approved data row, publishes the values for business date 27 November 2026 as a frozen baseline, and sends the nightly extract to the data lake for the Power BI data set. It serves REQ-RDF-012 and NFR-065 (measures from Workbench records, not a separate count), and the FSD P9 measure "measures read from the decision log and Workbench records, 100 percent".

## 3. Preconditions

- RWB-E1-018 is done: the case record holds route, stage, queue, entry date and stage clock start.
- RWB-E1-029 is done: versioned reference loads with validation run.
- The COLLINS load and case creation for business date 2026-11-27 have passed their checks (JOB-01, JOB-02).
- The measure definition file is prepared with the six baseline measures and the Tribe lead's approval on each row.
- The baseline date is configured: `rwb.reporting.baseline-date` = 2026-11-27.
- The data lake load area for INT-19 is available to the ACE service.

## 4. Flow

1. Reference data administrator: loads the measure definition file through POST /admin/reference-loads with table "measure_definition".
2. System: checks each row has a measure code, name, formula, data product, unit, approver and approval date; any failure refuses the whole load.
3. JOB-15 Reporting extract, nightly 01:30: reads the case facts of the previous business date through the P3 reporting interface and the payments since entry through the P1 interface.
4. System: computes each measure in force by its definition: counts by route, age band and queue; realized recovery; median time in stage; median turnaround per route.
5. System: writes one measure_snapshot row per measure, product and dimension value, with the definition version and business date.
6. System: on the baseline business date, marks the rows as baseline and frozen; frozen rows are never changed.
7. System: writes the extract files of INT-19 to the data lake with the business date and the freshness stamp, and records the run in the job monitor.
8. Reporting and BI analyst: the Power BI data set refreshes at 07:30 from the extract; the report shows the previous day and the baseline side by side.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A definition row has no formula or no data product | Load refused in full | MSG-GEN-001 | AC4 |
| X2 | The baseline is published a second time | Refused; frozen values unchanged | MSG-P9-001 | AC5 |
| X3 | The loads of the baseline date failed | Baseline not published; it runs after the next good load for that date | MSG-P1-001 | AC6 |
| X4 | The data lake is unavailable | Publish held; alert; run again in the next window | MSG-GEN-006 | AC7 |
| X5 | A measure in the extract has no definition in force | Not published; listed in the run record | MSG-P9-003 | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads case and payment facts through interfaces; no screen |
| Negotiable | The measures, formulas and age bands are data rows the Tribe agrees |
| Valuable | Every later epic is measured against one frozen baseline |
| Estimable | Two tables, one job, six measure calculators |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion runs against a synthetic case set with known answers |

## 7. Acceptance criteria

```gherkin
Feature: Baseline measures

  Background:
    Given the synthetic case set for business date 2026-11-27 holds 120 open cases: 60 Mortgage, 45 Hire purchase and 15 SSME
    Given age bands are "0-90", "91-180", "181-365", "366-730" and "over 730" days since entry

  Scenario: AC1 Definitions agreed
    Given a definition file of 6 rows for "CASES_BY_ROUTE", "CASES_BY_AGE", "CASES_BY_QUEUE", "REALIZED_RECOVERY", "TIME_IN_STAGE" and "TAT_BY_ROUTE"
    Given each row names its data product, formula, unit and approver "TRB-0001" with approval date 2026-11-20
    When it is loaded with valid from 2026-11-21
    Then definition version "MD-2026.11" is in force with 6 measures
    Then each measure returns its data product and formula through MeasureCatalog

  Scenario: AC2 Baseline published
    Given the loads of business date 2026-11-27 passed their checks
    When JOB-15 runs at 01:30 on 2026-11-28
    Then measure_snapshot holds rows for business date 2026-11-27 marked baseline and frozen with definition version "MD-2026.11"
    Then "CASES_BY_ROUTE" totals 120 cases, of which 60 are Mortgage
    Then "REALIZED_RECOVERY" equals the sum of synthetic payments since entry, 4,350,000.00 THB

  Scenario: AC3 Power BI data set
    Given the baseline measures are published
    When JOB-15 runs at 01:30 on 2026-12-02
    Then the INT-19 extract for business date 2026-12-01 is in the data lake with freshness stamp 2026-12-01 and the record count in its trailer
    Then the extract holds the baseline rows of 2026-11-27 unchanged
    Then the job monitor records the JOB-15 run with its row count, start and end time

  Scenario: AC4 Definition without a formula refused
    Given a definition file where row "TIME_IN_STAGE" has no formula
    When it is loaded
    Then the system refuses the load in full with MSG-GEN-001 naming "formula"
    Then the system puts no definition version in force

  Scenario: AC5 Baseline published twice
    Given the baseline for 2026-11-27 is frozen
    When JOB-15 is rerun for business date 2026-11-27 from SCR-44
    Then the frozen rows are unchanged
    Then the run record shows MSG-P9-001 naming 2026-11-27

  Scenario: AC6 Loads of the baseline date failed
    Given the COLLINS load for 2026-11-27 was refused at check "control total"
    When JOB-15 runs at 01:30 on 2026-11-28
    Then the system writes no baseline rows for 2026-11-27
    Then the run record shows MSG-P1-001 naming "DP03 Case" and 2026-11-26
    Then the system publishes the baseline by the first JOB-15 run after the 2026-11-27 load passes

  Scenario: AC7 Data lake unavailable
    Given the data lake load area does not answer
    When JOB-15 runs at 01:30 on 2026-11-30
    Then the system writes measure_snapshot rows for 2026-11-28 in the Workbench
    Then the system holds the extract and an alert goes to the operations channel with MSG-GEN-006 naming "Data lake"
    Then the system sends the extract by the next JOB-15 run

  Scenario: AC8 Measure with no definition in force
    Given the extract configuration lists measure "COST_PER_CASE" with no definition in force
    When JOB-15 runs at 01:30 on 2026-11-30
    Then the system writes no value for "COST_PER_CASE"
    Then the run record shows MSG-P9-003 naming "COST_PER_CASE"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each measure is published only under a definition in force that names its data product, formula, unit and approver | REQ-RDF-012; Principle 1 |
| BR2 | The baseline is the snapshot of the configured baseline business date and is frozen once written | REQ-RDF-012; FEAT-RPT-01 |
| BR3 | Measures are computed from Workbench records read through the owning modules, never from a separate count | NFR-065 |
| BR4 | A measure is computed only from loads that passed their checks; stale data is not published as the baseline | CTL-02; MSG-P1-001 rule |
| BR5 | The extract to the data lake holds the publish and alerts on failure, and runs again in the next window | INT-19 error handling |
| BR6 | Age bands are a reference list | Principle 1 |
| BR7 | A definition load with any invalid row is refused in full | refdata.txt change process, step 3 |

## 9. State transitions

None. This story does not change a case status. It sets the baseline flag and the frozen flag on measure_snapshot rows, and the JOB-15 run status (running, complete, failed, held).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Agrees the definitions; named as approver on each row; reads the report (Reporting R) |
| RW-REFADM, reference data administrator | Loads the definition file (Reference data C) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI data set; reads the snapshot (Reporting CRUD) |
| RW-DATASTEW, data steward | Reads the run record and the freshness stamp (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads the baseline (Reporting R) |
| RW-PLATADM, platform administrator | Reruns JOB-15 from SCR-44 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-006 | recovery_case | stage_code | Read |
| DF-CAS-008 | recovery_case | route_code | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-018 | recovery_case | stage_clock_start | Read |
| DF-CAS-022 | recovery_case | closed_date | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-CAS-025 | case_account | case_id | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-ACC-025 | account_payment | payment_date | Read |
| DF-ACC-026 | account_payment | payment_amount | Read |
| DF-RPT-032 | measure_definition | measure_code | Write |
| DF-RPT-033 | measure_definition | name | Write |
| DF-RPT-034 | measure_definition | formula | Write |
| DF-RPT-035 | measure_definition | data_product | Write |
| DF-RPT-036 | measure_definition | unit | Write |
| DF-RPT-037 | measure_definition | definition_version | Write |
| DF-RPT-038 | measure_definition | approved_by | Write |
| DF-RPT-039 | measure_definition | approved_at | Write |
| DF-RPT-040 | measure_definition | valid_from | Write |
| DF-RPT-041 | measure_snapshot | id | Write |
| DF-RPT-042 | measure_snapshot | measure_code | Write |
| DF-RPT-043 | measure_snapshot | definition_version | Write |
| DF-RPT-044 | measure_snapshot | business_date | Write |
| DF-RPT-045 | measure_snapshot | product_group | Write |
| DF-RPT-046 | measure_snapshot | dimension_code | Write |
| DF-RPT-047 | measure_snapshot | dimension_value | Write |
| DF-RPT-048 | measure_snapshot | value | Write |
| DF-RPT-049 | measure_snapshot | case_count | Write |
| DF-RPT-050 | measure_snapshot | is_baseline | Write |
| DF-RPT-051 | measure_snapshot | frozen | Write |
| DF-RPT-052 | measure_snapshot | published_at | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

No endpoint in Epic 1. GET /api/recovery/v1/reports/measures reads the snapshot from RWB-E2-009.

**Job JOB-15 Reporting extract**

| Item | Value |
|---|---|
| Trigger | Quartz, nightly 01:30 Asia/Bangkok |
| Input | Case facts and payments of the previous business date; definitions in force |
| Output | measure_snapshot rows; INT-19 extract files with business date, freshness stamp and trailer |
| Events published | None (events.txt lists no P9 event) |
| Idempotency key | Measure code, definition version, business date, product and dimension value (unique); frozen rows are skipped |
| Restart | Rerun from SCR-44 for a business date; non-frozen rows of that date are replaced, frozen rows stay |

**Published interfaces**

```java
// Offered by P9
public interface MeasureCatalog {
    List<MeasureDefinition> inForce(LocalDate onDate);
}
// Called, owned elsewhere
Stream<CaseFact> CaseReportingApi.caseFacts(LocalDate businessDate);              // P3: caseId, productGroup, routeCode, stageCode, queueCode, entryDate, stageClockStart, closedDate, status
Stream<RecoveryFact> RecoveryDataApi.paymentsSinceEntry(LocalDate businessDate); // P1: caseId, productGroup, amount
LoadStatus RecoveryDataApi.loadStatus(String source, LocalDate businessDate);    // P1
```

## 13. Solution plan

- Package: folder `recovery/reporting/baseline`, Java package `recovery.reporting.baseline`.

| Component | Type | Responsibility |
|---|---|---|
| MeasureDefinitionEntity | Entity | Maps table measure_definition |
| MeasureSnapshotEntity | Entity | Maps table measure_snapshot |
| MeasureDefinitionLoadHandler | Service | ReferenceLoadHandler for table measure_definition with the BR7 checks |
| MeasureCatalogService | Published interface | Implements MeasureCatalog |
| MeasureCalculators | Service | One calculator per measure code; each reads facts only from the interfaces |
| ReportingExtractJob | Job | JOB-15: computes, writes snapshot rows, freezes the baseline, writes the INT-19 extract |
| DataLakeWriter | Service | Writes extract files with trailer and freshness stamp through the integration adapters |

- Database: new tables measure_definition (unique measure_code, definition_version) and measure_snapshot (unique measure_code, definition_version, business_date, product_group, dimension_code, dimension_value; trigger refusing UPDATE or DELETE where frozen = true). Flyway migration `V1_013__measures.sql`. P9 owns both tables.
- Configuration and reference data: the six definitions, version MD-2026.11 (Tribe lead approves; RW-REFADM loads); age bands as a list, assumed values as in the Background, owner Tribe lead; `rwb.reporting.baseline-date` = 2026-11-27.
- Build steps:
  1. Write the migration with the frozen-row trigger; test that an update of a frozen row fails.
  2. Build MeasureDefinitionLoadHandler and MeasureCatalogService; test AC1 and AC4.
  3. Build the six calculators against stub interfaces with a synthetic set of known answers; test the AC2 values.
  4. Build ReportingExtractJob with the load status check, baseline flag and idempotency; test AC2, AC5, AC6, AC8.
  5. Build DataLakeWriter with hold and resend; test AC3 and AC7.
  6. Check the extract against sys_fields so no personal field is written; test on the AC3 extract.
- Feature flag: `rwb.reporting.baseline`.
- Done when: the tests in section 16 pass, and the Reporting and BI analyst has refreshed the Power BI data set once in SIT from the extract.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A definition row lacks a required value | Enter {field}. |
| MSG-P9-001 | The baseline is published again | The baseline for {date} is frozen. It cannot be published again. |
| MSG-P1-001 | The loads of the business date are stale | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | The data lake is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P9-003 | A measure has no definition in force | {measure} has no approved definition. It is not published. |

## 15. Screens and states

No screen in this story. The Tribe lead reads the baseline in the Power BI report built by the Reporting and BI analyst from the extract. JOB-15 runs show on SCR-44 Interface and job monitor (states Running; failed; complete). SCR-37 Steering dashboard comes in RWB-E2-009.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-013-01 | AC1, BR1 | System | Definition file of 6 rows approved by TRB-0001 |
| TC-E1-013-02 | AC2, BR2, BR3 | System | 120 synthetic cases on 2026-11-27 with known totals |
| TC-E1-013-03 | AC3, BR5 | System | JOB-15 on 2026-12-02 for business date 2026-12-01 |
| TC-E1-013-04 | AC4, BR7 | System | TIME_IN_STAGE with no formula |
| TC-E1-013-05 | AC5, BR2 | System | JOB-15 rerun for 2026-11-27 |
| TC-E1-013-06 | AC6, BR4 | System | COLLINS load of 2026-11-27 refused |
| TC-E1-013-07 | AC7, BR5 | System | Data lake load area stubbed unavailable |
| TC-E1-013-08 | AC8, BR1 | System | COST_PER_CASE with no definition |
| TC-E1-013-09 | Access | Access | RW-BIANAL calls POST /admin/reference-loads with table measure_definition; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: measures, formulas, age bands and the baseline date are data or configuration.
- No personal data in logs, tests or prompts. The extract carries case IDs, codes, counts and amounts only; a field marked personal in sys_fields is never written.
- No read of another module's tables. Case and payment facts come through the P3 and P1 reporting interfaces.
- Frozen baseline rows are protected by a database trigger as well as by the service.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-012 | Baseline measures published with definitions agreed by the Tribe | Business Requirements Epic 1, sections 3.8 and 4 | FEAT-RDF-19, FEAT-RPT-01 | 15 Manage performance, data and AI | None; control CTL-02 applies | TC-E1-013-01 to TC-E1-013-09 |

## 19. Out of scope

- The steering dashboard data set, SCR-37 and the measures endpoint (RWB-E2-009).
- Queue and ageing measures for team managers (FEAT-RPT-02, RWB-E1-030).
- Benefit realisation tracking against the baseline (FEAT-RPT-06, Epic 6).
- The decision log copy to the data lake (RWB-E1-014).

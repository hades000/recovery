<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 011 Reconciliation and data quality report v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 011 Reconciliation and data quality report v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-011 Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-011 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-11 Reconcile the data store to ALS daily; FEAT-RDF-12 Publish the daily reconciliation and data quality report; FEAT-RDF-13 Hold the publish when reconciliation breaks tolerance; FEAT-RPT-05 Reconcile case counts across sources; FEAT-RPT-09 Manage a data quality break |
| Requirement IDs | REQ-RDF-007, REQ-RDF-008 |
| BRD section | Business Requirements Epic 1, sections 3.1 and 3.8; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes; 15 Manage performance, data and AI |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-002, RWB-E1-006 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a daily reconciliation of the case list to ALS, with the variance by product and the data quality results in one Power BI report**, so that **everyone sees whether today's case list can be trusted**.

## 2. Business rationale

No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. This story runs the reconciliations REC-01 (account count by product) and REC-02 (balance by product) every working day, lists every account that breaks, holds the publish of the case list when a product is outside the tolerance, and publishes the result with the data quality results in one report. It meets REQ-RDF-007 and REQ-RDF-008, applies control CTL-01, and serves the accuracy measure "reconciliation breaks cleared within one day, 100 percent".

## 3. Preconditions

- RWB-E1-002 is done: the case list step builds case_list_row and writes its extract for the publish step.
- RWB-E1-006 is done: the data quality rules write dq_exception for the business date.
- The INT-01 load for the business date is COMPLETED, as `LoadRunQuery` of RWB-E1-003 reports.
- Parameters are loaded: `recon.tolerance.pct` 0.00 for REC-01 and REC-02 (assumed, DL25), `case.entry.dpd` 90 (DL16).
- The reporting and BI analyst has built the Power BI report "Reconciliation and data quality" on the lake extracts and scheduled its refresh at 07:30.
- JOB-04 runs as service identity SY-DATALOAD.

## 4. Flow

1. System: JOB-04 Daily reconciliation runs its reconciliation step after the case list step for the business date.
2. System: checks through `LoadRunQuery` that the INT-01 load for the business date is COMPLETED.
3. System: for each product group, counts the ALS accounts at or above 90 days past due less the accounts excluded at entry, and the case list rows at or above 90 days past due (REC-01).
4. System: for each product group, sums total_balance on both sides (REC-02).
5. System: computes the variance and the variance percent and compares it with the tolerance; writes one reconciliation_result per reconciliation and product.
6. System: writes one dq_exception per account that breaks, with check code REC-01 and the account number: in ALS and not on the case list, or on the case list and not in ALS.
7. System: if every result is PASS, releases the case list extract for publish; if any is BREAK, holds the case list publish for the business date and alerts the data steward, the platform administrator and the team managers.
8. System: writes the reconciliation extract and the data quality extract to the data lake.
9. Power BI: the 07:30 refresh shows each product as green, red or not run, the variance, the break rows and the data quality failures by rule.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product's variance is above the tolerance | Result BREAK; red on the report; case list publish held; break rows listed; alert | MSG-P1-012 | AC2 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | The INT-01 load for the business date is not COMPLETED | Reconciliation not run; report shows not run; case list publish held | MSG-P1-001 | AC4 |
| X4 | The reconciliation runs again for the same date after a fix | Results for that date replaced; publish released if every result passes | None | AC5 |
| X5 | Two runs for the same date | Results written once per reconciliation, product and date | None | AC6 |
| X6 | A role without Platform administration R lists the break rows | 403 | MSG-P4-002 | TC-E1-011-07 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the case list of RWB-E1-002 and the rule results of RWB-E1-006; changes no case |
| Negotiable | The tolerance per reconciliation is a parameter; the report layout belongs to the BI analyst |
| Valuable | Teams see each morning whether the list is complete, and a broken list is not published |
| Estimable | One batch step, one table, one hold flag, two extracts |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below is one automated test on synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality report

  Background:
    Given the business date is 2026-11-30 and DP01 is loaded for 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for REC-01 and REC-02

  Scenario: AC1 Variance under limit
    Given the ALS accounts at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903
    Given the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums
    When the reconciliation step of JOB-04 runs
    Then the system writes six reconciliation_result rows , REC-01 and REC-02 for each product, each with variance 0 and result PASS
    Then the system releases the case list extract for 2026-11-30 for publish
    Then the report after the 07:30 refresh shows all three products green

  Scenario: AC2 Variance over limit
    Given the ALS count for SSME is 2,903 and the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent
    When the reconciliation step runs
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    Then the system writes 12 dq_exception rows with check code "REC-01" and the 12 account numbers
    Then the system holds the case list publish for 2026-11-30 and the lake keeps the case list of 2026-11-27
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ALS for SSME: a difference of 12 accounts, 0.41 percent."
    Then the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green

  Scenario: AC3 Variance equal to the tolerance
    Given the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30
    Given the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent
    When the reconciliation step runs
    Then the MORTGAGE result is PASS and the SSME result is BREAK

  Scenario: AC4 Account data not loaded
    Given the INT-01 load for 2026-11-30 is LATE and not COMPLETED
    When JOB-04 reaches the reconciliation step
    Then the system writes no reconciliation_result for 2026-11-30
    Then the system holds the case list publish for 2026-11-30
    Then the report shows every product as not run with the reason "DP01 is from 2026-11-27"

  Scenario: AC5 Rerun after a fix
    Given the SSME result for 2026-11-30 is BREAK and the publish is held
    Given P3 has created the 12 missing cases and the case list step has been rerun
    When the platform administrator reruns the reconciliation step for 2026-11-30
    Then the system replaces the six results for 2026-11-30 and all are PASS
    Then the system sets the 12 REC-01 exceptions CLEARED with cleared_on 2026-11-30
    Then the system releases the case list extract for 2026-11-30 for publish

  Scenario: AC6 Two runs for the same date
    Given two JOB-04 runs for 2026-11-30 start on two nodes
    When both reach the reconciliation step
    Then reconciliation_result holds one row per reconciliation, product and date, six rows in all
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Accounts at 90 days past due in the ALS load are compared with open recovery cases, by count per product, every day | REC-01; CTL-01; REQ-RDF-007 |
| BR2 | Balances in the ALS load are compared with the balances on the case accounts, by sum per product | REC-02 |
| BR3 | A result is a break when the variance percent is above the tolerance | Parameter recon.tolerance.pct, 0.00 assumed (DL25) |
| BR4 | A break holds the publish of the case list for the business date and lists the break rows for the data steward | FEAT-RDF-13; REC-01 "Break list to the data steward" |
| BR5 | Accounts excluded at entry are explained and do not count as breaks | REC-01 "zero unexplained"; REQ-CWC-004 |
| BR6 | No reconciliation runs until the INT-01 load for the business date is COMPLETED | MSG-P1-001; RWB-E1-003 BR1 |
| BR7 | Report grades: green, every reconciliation for the product passed; red, at least one break; not run, the reconciliation did not run, with the reason | FEAT-RDF-12 |
| BR8 | A repeated run for the same date replaces that date's results | R-UNI-40 |

## 9. State transitions

None. This story does not change a case status. It writes reconciliation_result (PASS or BREAK), sets dq_exception rows OPEN or CLEARED, and sets the case list publish of the business date to HELD or RELEASED.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs the reconciliation; writes reconciliation_result, dq_exception and the publish status |
| RW-DATASTEW, data steward and data product owner | Reads results and break rows (Platform administration R); signs the daily reconciliation to ALS |
| RW-PLATADM, platform administrator | Reads results; reruns the step (Platform administration U) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read results and break rows (Platform administration R) |
| RW-TEAMMGR, RW-BIANAL and other report readers | Read the Power BI report (Reporting R); RW-BIANAL builds it (Reporting CRUD) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-002 | loan_account | account_no | Read |
| DF-ACC-012 | loan_account | total_balance | Read |
| DF-ACC-014 | loan_account | days_past_due | Read |
| DF-ACC-021 | loan_account | data_as_of | Read |
| DF-RPT-002 | case_list_row | business_date | Read; write publish_status |
| DF-RPT-006 | case_list_row | account_no | Read; write publish_status |
| DF-RPT-007 | case_list_row | product_group | Read; write publish_status |
| DF-RPT-014 | case_list_row | total_balance | Read; write publish_status |
| DF-RPT-015 | case_list_row | days_past_due | Read; write publish_status |
| DF-RPT-019 | case_list_row | publish_status | Read; write publish_status |
| DF-OPS-118 | reconciliation_result | id | Write |
| DF-OPS-119 | reconciliation_result | rec_code | Write |
| DF-OPS-120 | reconciliation_result | business_date | Write |
| DF-OPS-121 | reconciliation_result | product_group | Write |
| DF-OPS-122 | reconciliation_result | source_count | Write |
| DF-OPS-123 | reconciliation_result | workbench_count | Write |
| DF-OPS-124 | reconciliation_result | source_amount | Write |
| DF-OPS-125 | reconciliation_result | workbench_amount | Write |
| DF-OPS-126 | reconciliation_result | variance_count | Write |
| DF-OPS-127 | reconciliation_result | variance_pct | Write |
| DF-OPS-128 | reconciliation_result | tolerance_pct | Write |
| DF-OPS-129 | reconciliation_result | result | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |
| DF-OPS-049 | dq_exception | status | Write |
| DF-OPS-051 | dq_exception | cleared_on | Write |
| DF-OPS-022 | load_run | interface_id | Read through LoadRunQuery (INT-01) |
| DF-OPS-025 | load_run | business_date | Read through LoadRunQuery (INT-01) |
| DF-OPS-026 | load_run | status | Read through LoadRunQuery (INT-01) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-04 Daily reconciliation, reconciliation step, after the case list step; before the publish step |
| Job name | JOB-04 Daily reconciliation |
| Input | loan_account; case_list_row; `LoadRunQuery`; `CaseQueryApi.excludedAccountsByProduct(businessDate)`; parameters |
| Output | reconciliation_result; dq_exception (REC-01, REC-02); publish status of the case list; extracts `reconciliation/<businessDate>.csv` and `data-quality/<businessDate>.csv` to the data lake through the outbound adapter (INT-19) |
| Events published | None |
| Idempotency key | rec_code, business_date and product_group (unique) |
| Restart | Rerun by POST /admin/jobs/{jobId}/rerun replaces the date's results |

**Published interface used** (P3, extends the interface of RWB-E1-002)

```java
Map<String, Long> excludedAccountsByProduct(LocalDate businessDate); // product group to count of accounts excluded at entry
```

**GET /admin/data-quality/exceptions** (API-P1-003): with `product=DP03` returns the REC-01 and REC-02 break rows with the rule results; Platform administration R; 401, 403 (MSG-P4-002), 503; read only.

**GET /admin/jobs** (API-P1-001): the JOB-04 run shows checks REC-01 and REC-02 per product (PASS, BREAK or NOT_RUN) and PUBLISH (RELEASED or HELD).

## 13. Solution plan

**Package.** Folder `recovery/dataengine/recon`, Java package `recovery.dataengine.recon`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReconciliationStepConfig | Job (Spring Batch step in JOB-04) | Runs REC-01 and REC-02 per product, writes results and breaks, sets the publish status |
| ReconciliationService | Service | Computes counts, sums, variances and results against the tolerance |
| ReconciliationResult | Entity | Maps reconciliation_result |
| ReconciliationResultRepository | Repository | Replaces the results of one business date |
| CaseListPublishGate | Service | Sets HELD or RELEASED on the date's case list; the publish step writes the case list extract only when RELEASED |
| ReconciliationExtractWriter | Service | Writes the reconciliation and data quality extracts |
| LoadAlertNotifier | Service (from RWB-E1-003) | Sends MSG-P1-012 |

**Database.** Migration `V1_011__reconciliation_result.sql` creates reconciliation_result (rec_code varchar(6), business_date date, product_group varchar(15), source_count integer, workbench_count integer, source_amount numeric(18,2), workbench_amount numeric(18,2), variance_count integer, variance_pct numeric(9,4), tolerance_pct numeric(9,4), result varchar(8) check in ('PASS','BREAK'), standard columns, unique (rec_code, business_date, product_group)); adds publish_status varchar(10) default 'PENDING' check in ('PENDING','HELD','RELEASED') to case_list_row.

**Configuration and reference data.** Parameters `recon.tolerance.pct` per reconciliation and `case.entry.dpd` from the parameter catalog, loaded by the center of excellence analyst; a tolerance change also needs Risk approval (reference data change process, step 4). Alert recipient groups as configuration. The report and its refresh belong to the reporting and BI analyst.

**Build steps**

1. Write migration V1_011, ReconciliationResult and its repository; test the replace of one date.
2. Write ReconciliationService for REC-01 and REC-02 with the exclusions; unit test variance 0, the tolerance boundary and a break.
3. Write the break row listing in both directions and the CLEARED update on a passing rerun.
4. Write CaseListPublishGate and change the publish step of RWB-E1-002 to write the case list extract only when RELEASED; this replaces the total count check of RWB-E1-002.
5. Write the path for an INT-01 load that is not COMPLETED, with the NOT_RUN checks and the held publish.
6. Write ReconciliationExtractWriter for both extracts and add them to the publish step.
7. Add the checks to the JOB-04 Job mapping.

**Feature flag.** `rwb.p1.reconciliation`. Off: the case list publishes as in RWB-E1-002 with its count check.

**Done when.** The tests in section 16 pass, and the Power BI report shows the three grades from the SIT extracts.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | INT-01 not complete; reconciliation not run | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No Workbench screen in this story. The team manager reads the Power BI report "Reconciliation and data quality": one row per product with its grade (green, red or not run, as BR7 defines), the counts, the balances, the variance, the break rows and the data quality failures by rule. SCR-45 Data quality shows the same breaks from E2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-01 | AC1, BR1, BR2, BR5, BR7 | System | Synthetic accounts MORTGAGE 12,256, HIRE_PURCHASE 12,960, SSME 2,903 with exclusions |
| TC-E1-011-02 | AC2, BR3, BR4 | System | 12 SSME accounts missing from the case list |
| TC-E1-011-03 | AC3, BR3 | System | Tolerance 0.10; variances 0.10 and 0.11 percent |
| TC-E1-011-04 | AC4, BR6, BR7 | System | INT-01 load for 2026-11-30 LATE |
| TC-E1-011-05 | AC5, BR8 | System | Break, missing cases created, rerun |
| TC-E1-011-06 | AC6, BR8 | System | Two JOB-04 runs on two nodes |
| TC-E1-011-07 | Access | Access | RW-CASEOWN calls GET /admin/data-quality/exceptions; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the tolerance and the threshold are parameters.
- No personal data in logs, tests or prompts. Break rows carry account numbers only.
- No read of another module's tables. Exclusions come through `CaseQueryApi`; open case accounts come from case_list_row.
- A held case list is never published by hand from this story.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the ALS count, no variance | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | All recovery processes | REC-01; REC-02; CTL-01; R-UNI-40 | TC-E1-011-01 to TC-E1-011-07 |
| REQ-RDF-008 | Data quality results visible to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | CTL-01 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-07 |

## 19. Out of scope

- Working a break to closure with an owner and a date, and releasing a held publish by hand (FEAT-RPT-09 full scope, Epic 2).
- Reconciliation of treatments, payments, notices, write-offs and assets (REC-03 to REC-07, later epics).
- The decision log copy check (REC-08, RWB-E1-014).
- Cross-source case count reconciliation in the reporting module (FEAT-RPT-05 full scope, Epic 2).

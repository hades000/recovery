# RWB-E1-011 Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-011 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-11 Reconcile the case list to ACE daily; FEAT-RDF-12 Publish the daily reconciliation and data quality report; FEAT-RDF-13 Hold the publish when reconciliation breaks tolerance; FEAT-RPT-05 Reconcile case counts across sources; FEAT-RPT-09 Manage a data quality break |
| Requirement IDs | REQ-RDF-007, REQ-RDF-008 |
| BRD section | Business Requirements Epic 1, sections 3.1 and 3.8; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes; 15 Manage performance, data and AI |
| Decision | D-RCV-35 (U4); ADR-010 |
| Priority | Must |
| Depends on | RWB-E1-002, RWB-E1-015, RWB-E1-069 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a daily reconciliation of the case list to `v_ace_account`, of every business key on a Workbench table to its ACE view, and of treatments and payments to their ACE records, with the variance by product and the data quality results in one Power BI report**, so that **everyone sees whether today's case list and its links can be trusted**.

## 2. Business rationale

No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. This story runs the five daily reconciliations REC-01 to REC-05 every business date: the account count and the balance by product against `v_ace_account`, approved treatments against `v_ace_plan`, payments against proceeds, and every business key on a Workbench table against the view that holds it. It lists every account or key that breaks, holds the publish of the case list when a product is outside the tolerance, and publishes the result with the data quality measures in one report. It meets REQ-RDF-007 and REQ-RDF-008, applies control CTL-01, and serves the accuracy measure "reconciliation breaks cleared within one day, 100 percent". No reconciliation runs against a source load: the Workbench loads nothing, and the ACE side of every check is a read-only view.

## 3. Preconditions

- RWB-E1-002 is done: the case list step builds case_list_row and holds its extract for the publish step.
- RWB-E1-015 is done: the daily completeness gate holds JOB-04 until the sources the reconciliation reads are COMPLETE for the business date, and the freshness stamps exist.
- RWB-E1-069 is done: the views exist, including `v_ace_account`, `v_ace_plan`, `v_ace_payment`, `v_ace_customer`, `v_ace_asset` and `v_ace_contact`.
- Parameters are loaded: `recon.tolerance.pct` 0.00 for REC-01 and REC-02 (assumed, DL25), `case.entry.dpd` 90 (DL16), `recon.treatment.days` 2 and `recon.payment.days` 1 (assumed, DL25).
- The reporting and BI analyst has built the Power BI report "Reconciliation and data quality" on the lake extracts and scheduled its refresh at 07:30.
- JOB-04 runs as the recovery service identity (recovery_svc), which holds SELECT on `recovery.v_ace_*` and no privilege on `public`.

## 4. Flow

1. System: JOB-04 Daily reconciliation runs its reconciliation step after the case list step for the business date, on a COMPLETE gate result for the sources it reads.
2. System: reads the business date and completion time of the ALS batch from `v_ace_batch_status`, and uses that one business date for every check.
3. System: REC-01, for each product group, counts the accounts in `v_ace_account` at or above the entry threshold with `data_as_of` equal to the business date, less the accounts in `case_entry_exclusion` for the date, and counts the case_list_row rows at or above the threshold.
4. System: REC-02, for each product group, sums `v_ace_account.total_balance` and case_list_row.total_balance.
5. System: REC-03 counts approved restructure treatments whose case plan is not booked in `v_ace_plan` after two business days, and sums the offer amount.
6. System: REC-04 matches `v_ace_payment` rows of the business date to proceeds by `payment_code`, and counts and sums what is unmatched after one business day.
7. System: REC-05 resolves every `account_key`, `person_key`, `asset_key`, `payment_code` and `contact_key` on a Workbench table to its view row, and counts the orphans.
8. System: computes the variance and the variance percent for each check and product group, compares it with the tolerance, and writes one reconciliation_result row per check and product group.
9. System: writes the break list, with account keys, keys and amounts, to the reconciliation extract for the data steward; no dq_exception row is written because that table has left the schema.
10. System: if every REC-01 and REC-02 result is PASS, sets the publish status of the date to RELEASED; if any is BREAK, sets HELD and alerts the data steward, the platform administrator and the team managers.
11. System: writes the reconciliation extract and the data quality extract to the data lake.
12. Power BI: the 07:30 refresh shows each product as green, red or not run, the variance, the break rows, the referential completeness and the quality measures.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product's variance is above the tolerance | Result BREAK; red on the report; case list publish held; break rows listed; alert | MSG-P1-012 | AC2 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | The ACE batch for the business date is not COMPLETED | The gate holds JOB-04; no reconciliation runs; the report shows not run with the reason; the publish stays held | MSG-P1-001 | AC4 |
| X4 | The reconciliation runs again for the same date after a fix | Results for that date are replaced; the publish is released if every REC-01 and REC-02 result passes | None | AC5 |
| X5 | Two runs for the same date | Results are written once per check, product group and date | None | AC6 |
| X6 | A business key has no ACE row | REC-05 is BREAK with the orphan count; the key is listed for the data steward and the ACE team; no Workbench row changes | None | AC7 |
| X7 | A view returns an error during the run | No result is written for the date; the run is FAILED with the system named; the rerun writes every row | MSG-GEN-006 | AC8 |
| X8 | A role without Platform administration R lists the break rows | 403 | MSG-P4-002 | TC-E1-011-07 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the case list of RWB-E1-002, the gate and stamps of RWB-E1-015 and the views of RWB-E1-069; changes no case |
| Negotiable | The tolerance per reconciliation and the waiting periods are parameters; the report layout belongs to the BI analyst |
| Valuable | Teams see each morning whether the list and its links are complete, and a broken list is not published |
| Estimable | One batch step, one table, one hold flag, two extracts |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below is one automated test on synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality report

  Background:
    Given the business date is 2026-11-30 and v_ace_batch_status shows ALS COMPLETED for 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for REC-01 and REC-02

  Scenario: AC1 Variance under limit
    Given the v_ace_account accounts at 90 days past due or more less the exclusions are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903
    Given the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums
    Given no restructure plan is overdue in v_ace_plan, no payment of the date is unmatched, and every business key resolves to its view
    When the reconciliation step of JOB-04 runs
    Then the system writes fifteen reconciliation_result rows, REC-01 to REC-05 for each of the three product groups, each with variance 0 and result PASS
    Then the system sets the publish status of the case list for 2026-11-30 to RELEASED
    Then the report after the 07:30 refresh shows all three products green

  Scenario: AC2 Variance over limit
    Given v_ace_account holds 2,903 SSME accounts at 90 days past due or more less the exclusions
    Given the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent
    When the reconciliation step runs
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    Then the 12 account keys are on the break list for the data steward, with their days past due from v_ace_account
    Then the system sets the case list publish for 2026-11-30 to HELD and the lake keeps the case list of 2026-11-27
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for SSME: a difference of 12 accounts, 0.41 percent."
    Then the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green

  Scenario: AC3 Variance equal to the tolerance
    Given the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30
    Given the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent
    When the reconciliation step runs
    Then the MORTGAGE result is PASS and the SSME result is BREAK

  Scenario: AC4 ACE batch not complete
    Given v_ace_batch_status shows no COMPLETED ALS row for 2026-11-30 at 08:00
    When the DP01 cut-off passes and JOB-04 is triggered
    Then the daily completeness gate holds JOB-04 and the system writes no reconciliation_result for 2026-11-30
    Then the case list publish for 2026-11-30 stays HELD
    Then the report shows every product as not run with the reason "DP01 is from 2026-11-27"

  Scenario: AC5 Rerun after a fix
    Given the SSME result for 2026-11-30 is BREAK and the publish is held
    Given P3 has created the 12 missing cases and the case list step has been rerun
    When the platform administrator restarts the reconciliation step for 2026-11-30
    Then the system replaces the fifteen results for 2026-11-30 and all are PASS
    Then the system sets the publish status of the date to RELEASED and the case list extract is sent to the lake

  Scenario: AC6 Two runs for the same date
    Given two JOB-04 runs for 2026-11-30 start on two nodes
    When both reach the reconciliation step
    Then reconciliation_result holds one row per check and product group, fifteen rows in all
    Then no row is written twice for the same rec_code, business_date and product_group

  Scenario: AC7 Business key without an ACE row
    Given case_party on case "RW-2026-000140" carries person_key "P0099881", which has no row in v_ace_customer
    When the REC-05 step runs
    Then the REC-05 result for the product group of the case is BREAK with 1 orphan
    Then "case_party.person_key P0099881" is on the break list for the data steward and the ACE team
    Then the case and its case_party row are unchanged

  Scenario: AC8 View unavailable during the run
    Given v_ace_account returns an error after the MORTGAGE count is read
    When the reconciliation step runs
    Then the system writes no reconciliation_result for 2026-11-30
    Then the run shows FAILED with MSG-GEN-006 for system "ACE database"
    Then the restart writes all fifteen rows for 2026-11-30
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Accounts at or above the entry threshold in `v_ace_account` for the business date are compared with open recovery cases and the case list rows, by count per product group, every business date | REC-01; CTL-01; REQ-RDF-007 |
| BR2 | Balances in `v_ace_account` are compared with the balances on the case list rows, by sum per product group | REC-02 |
| BR3 | An approved restructure treatment whose plan is not booked in `v_ace_plan` two business days after approval is a break | REC-03; parameter recon.treatment.days |
| BR4 | A payment in `v_ace_payment` with no proceeds matched to its `payment_code` one business day after the payment date stays on the exception list and counts as a break | REC-04; parameter recon.payment.days |
| BR5 | Every `account_key`, `person_key`, `asset_key`, `payment_code` and `contact_key` on a Workbench table must resolve to a row in `v_ace_account`, `v_ace_customer`, `v_ace_asset`, `v_ace_payment` or `v_ace_contact`; zero orphans, and every one is listed | REC-05; REQ-RDF-007 |
| BR6 | A result is a break when the variance percent is above the tolerance; REC-03 and REC-04 use their waiting periods and a zero tolerance | Parameter recon.tolerance.pct, 0.00 assumed (DL25) |
| BR7 | A break in REC-01 or REC-02 holds the publish of the case list for the business date and lists the break rows for the data steward | FEAT-RDF-13; REC-01 "Break list to the data steward" |
| BR8 | Accounts excluded at entry are explained and do not count as breaks | REC-01 "zero unexplained"; REQ-CWC-004 |
| BR9 | No reconciliation runs until the daily completeness gate of RWB-E1-015 reports COMPLETE for the sources the reconciliation reads on the business date | BR-P1-014-4; MSG-P1-001 |
| BR10 | Report grades: green, every reconciliation for the product passed; red, at least one break; not run, the reconciliation did not run, with the reason | FEAT-RDF-12 |
| BR11 | A repeated run for the same date replaces that date's results | R-UNI-40 |
| BR12 | The reconciliation reads ACE for the business date of the ACE batch it was started by, and never a mix of two business dates | BR-P1-011-2 |
| BR13 | A REC-05 orphan never deletes or changes a Workbench record; it is listed for the data steward and, where the row is missing in ACE, for the ACE team | BR-P1-011-3 |

## 9. State transitions

None. This story does not change a case status. It writes reconciliation_result (PASS or BREAK) and sets case_list_row.publish_status to HELD or RELEASED for the business date.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| recovery_svc, recovery service identity | Runs the reconciliation; writes reconciliation_result and the publish status; reads the ACE views |
| RW-DATASTEW, data steward and data product owner | Reads results and break rows (Platform administration R); signs the daily reconciliation to ACE |
| RW-PLATADM, platform administrator | Reads results; restarts the step (Platform administration U) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read results and break rows (Platform administration R) |
| RW-TEAMMGR, RW-BIANAL and other report readers | Read the Power BI report (Reporting R); RW-BIANAL builds it (Reporting CRUD) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-160 | v_ace_plan | plan_ref | Read |
| DF-ACE-167 | v_ace_plan | account_key | Read |
| DF-ACE-168 | v_ace_plan | booked_at | Read |
| DF-ACE-043 | v_ace_payment | payment_code | Read |
| DF-ACE-044 | v_ace_payment | account_key | Read |
| DF-ACE-045 | v_ace_payment | payment_date | Read |
| DF-ACE-046 | v_ace_payment | payment_amount | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-100 | v_ace_asset | asset_key | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-RPT-002 | case_list_row | business_date | Read |
| DF-RPT-005 | case_list_row | account_key | Read |
| DF-RPT-006 | case_list_row | account_no | Read |
| DF-RPT-007 | case_list_row | product_group | Read |
| DF-RPT-014 | case_list_row | total_balance | Read |
| DF-RPT-015 | case_list_row | days_past_due | Read |
| DF-RPT-019 | case_list_row | publish_status | Write |
| DF-CAS-046 | recovery_case | plan_ref | Read |
| DF-CAS-026 | case_account | account_key | Read (REC-05) |
| DF-CAS-032 | case_party | person_key | Read (REC-05) |
| DF-CAS-004 | recovery_case | primary_person_key | Read (REC-05) |
| DF-CAS-057 | case_entry_exclusion | account_key | Read |
| DF-CAS-058 | case_entry_exclusion | business_date | Read |
| DF-TRT-002 | treatment | case_id | Read (REC-03) |
| DF-TRT-004 | treatment | treatment_type | Read (REC-03) |
| DF-TRT-007 | treatment | offer_amount | Read (REC-03) |
| DF-TRT-011 | treatment | approval_level | Read (REC-03) |
| DF-TRT-012 | treatment | booked_at | Read (REC-03) |
| DF-TRT-013 | treatment | outcome | Read (REC-03) |
| DF-FIN-002 | proceeds | case_id | Read (REC-04) |
| DF-FIN-004 | proceeds | payment_code | Read (REC-04) |
| DF-FIN-006 | proceeds | amount | Read (REC-04) |
| DF-FIN-008 | proceeds | matched_to | Read (REC-04) |
| DF-SAL-002 | listing | asset_key | Read (REC-05) |
| DF-SAL-010 | asset_sale | asset_key | Read (REC-05) |
| DF-SAL-033 | debt_sale_account | account_key | Read (REC-05) |
| DF-LEG-030 | notice | person_key | Read (REC-05) |
| DF-INT-003 | interaction | person_key | Read (REC-05) |
| DF-INT-022 | interaction | contact_key | Read (REC-05) |
| DF-DOC-003 | document | person_key | Read (REC-05) |
| DF-DOC-100 | signature_request | person_key | Read (REC-05) |
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

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Trigger | JOB-04 Daily reconciliation, reconciliation step, after the case list step and before the publish step |
| Job name | JOB-04 Daily reconciliation |
| Input | `v_ace_account`; case_list_row; case_entry_exclusion; treatment; `v_ace_plan`; `v_ace_payment`; proceeds; `v_ace_customer`, `v_ace_asset` and `v_ace_contact` for REC-05; `v_ace_batch_status`; parameters |
| Output | reconciliation_result (REC-01 to REC-05); case_list_row.publish_status; extracts `reconciliation/<businessDate>.csv` and `data-quality/<businessDate>.csv` to the data lake through the outbound adapter (INT-19) |
| Events published | None |
| Idempotency key | rec_code, business_date and product_group (unique) |
| Restart | The platform administrator restarts JOB-04 for the business date from the scheduler console; the step replaces the date's results |

**Published interface used** (P3, extends the interface of RWB-E1-002)

```java
Map<String, Long> excludedAccountsByProduct(LocalDate businessDate); // product group to count of accounts excluded at entry
```

**Reading the results**

| Item | Value |
|---|---|
| GET /admin/jobs?type=JOB-04 | The run shows one check per reconciliation, REC-01 to REC-05, with PASS, BREAK or NOT_RUN per product group, and PUBLISH (RELEASED or HELD) |
| Report | Power BI report "Reconciliation and data quality" on the two extracts: grade by product, counts, balances, variance, break rows by key, referential completeness and the quality measures |
| Authorization | Platform administration R for the job listing; Reporting R for the report |
| Errors | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 (MSG-GEN-006) |

There is no data quality exception endpoint and no dq_exception table: the break list is the reconciliation extract and the report.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/recon`, Java package `recovery.dataengine.recon`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReconciliationStepConfig | Job (Spring Batch step in JOB-04) | Runs REC-01 to REC-05 per product group, writes results and breaks, sets the publish status |
| ReconciliationService | Service | Computes counts, sums, variances and results against the tolerance |
| ReconciliationResult | Entity | Maps reconciliation_result |
| ReconciliationResultRepository | Repository | Replaces the results of one business date |
| ReferentialCheck | Service | REC-05; resolves each business-key family against its view and lists the orphans |
| CaseListPublishGate | Service | Sets HELD or RELEASED on the date's case list; the publish step of RWB-E1-002 sends the extract only when RELEASED |
| ReconciliationExtractWriter | Service | Writes the reconciliation and data quality extracts |
| LoadAlertNotifier | Service | Sends MSG-P1-012 |

**Database.** reconciliation_result is created by V0001 (RWB-E1-001) with the columns in section 11 and unique (rec_code, business_date, product_group); the next free migration adds index `ix_reconciliation_date` on (business_date, rec_code, product_group). No dq_exception and no dq_rule exists or is created. REC-05 reads the Workbench tables in the recovery schema and the views by business key; it adds no foreign key and changes no row.

**Configuration and reference data.** Parameters `recon.tolerance.pct` per reconciliation, `recon.treatment.days`, `recon.payment.days` and `case.entry.dpd` from the parameter catalog, loaded by the center of excellence analyst; a tolerance change also needs Risk approval (reference data change process, step 4). Alert recipient groups as configuration. The report and its refresh belong to the reporting and BI analyst.

**Build steps**

1. Write ReconciliationResult, its repository and the index migration; test the replace of one date.
2. Write ReconciliationService for REC-01 and REC-02 with the exclusions; unit test variance 0, the tolerance boundary and a break.
3. Write REC-03 and REC-04 with their waiting-period parameters and the unmatched list.
4. Write ReferentialCheck for the five key families; test each view and the composite `contact_key`.
5. Write the break row listing in both directions and the replacement on a passing rerun.
6. Write CaseListPublishGate and change the publish step of RWB-E1-002 to send the case list extract only when RELEASED; this replaces the total count check of RWB-E1-002.
7. Write the path for a gate HOLD, with the NOT_RUN checks and the held publish.
8. Write ReconciliationExtractWriter for both extracts and add them to the publish step.
9. Add the checks to the JOB-04 job listing.

**Feature flag.** `rwb.p1.reconciliation`. Off: the case list publishes as in RWB-E1-002 with its own count line.

**Done when.** The tests in section 16 pass, and the Power BI report shows the three grades and the REC-05 completeness measure from the SIT extracts.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The ACE batch is not complete; reconciliation not run | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A view or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No Workbench screen in this story. The team manager reads the Power BI report "Reconciliation and data quality": one row per product with its grade (green, red or not run, as BR10 defines), the counts, the balances, the variance, the break rows, the referential completeness and the quality measures. SCR-45 Data quality shows the same breaks from E2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-01 | AC1, BR1, BR2, BR5, BR8, BR10 | System | Synthetic accounts MORTGAGE 12,256, HIRE_PURCHASE 12,960, SSME 2,903 with exclusions; clean REC-03, REC-04 and REC-05 |
| TC-E1-011-02 | AC2, BR6, BR7 | System | 12 SSME accounts missing from the case list |
| TC-E1-011-03 | AC3, BR6 | System | Tolerance 0.10; variances 0.10 and 0.11 percent |
| TC-E1-011-04 | AC4, BR9, BR10 | System | No COMPLETED ALS row for 2026-11-30 |
| TC-E1-011-05 | AC5, BR11 | System | Break, missing cases created, restart |
| TC-E1-011-06 | AC6, BR11 | System | Two JOB-04 runs on two nodes |
| TC-E1-011-07 | Access | Access | RW-CASEOWN calls GET /admin/jobs?type=JOB-04; refused with MSG-P4-002 |
| TC-E1-011-08 | AC7, BR5, BR13 | System | case_party person_key P0099881 absent from v_ace_customer |
| TC-E1-011-09 | AC8, BR12 | System | v_ace_account stub returning an error after the MORTGAGE count |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the tolerance, the waiting periods and the threshold are parameters.
- No personal data in logs, tests or prompts. Break rows carry account keys, account numbers and business keys only.
- No read of another module's tables. Exclusions come through `CaseQueryApi`; open case accounts come from case_list_row.
- ACE data only through `recovery.v_ace_*` views; a break never changes an ACE row or a Workbench row.
- A held case list is never published by hand from this story.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count in v_ace_account with no variance, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | All recovery processes | REC-01; REC-02; REC-05; CTL-01; R-UNI-40 | TC-E1-011-01 to TC-E1-011-09 |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-03; REC-04; REC-05; CTL-01 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-07, TC-E1-011-08 |

## 19. Out of scope

- Working a break to closure with an owner and a date, and releasing a held publish by hand (FEAT-RPT-09 full scope, Epic 2).
- Reconciliation of write-offs (REC-06), assets taken on (REC-07), the decision log copy (REC-08, RWB-E1-014) and notice barcodes (REC-09, RWB-E1-055).
- Cross-source case count reconciliation in the reporting module (FEAT-RPT-05 full scope, Epic 2).
- The data quality console SCR-45 and the quality measure definitions (Epic 2 and Epic 8).

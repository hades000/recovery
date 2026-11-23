# RWB-P1-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1015-APP, RWB-P1-E1069-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P1-E1002-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1011-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022, FR-P1-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-011 for rwb-source-data. The reconciliation becomes one activity of `ReconciliationWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, started by `rwb.source-data.AceDataReady.v1` (DP-10, DP-14; Architecture v5 slides 15 and 44). The results are read through this service's contract on `/api/recovery/source-data/v1` instead of two lake extracts and a Power BI data set, because the target has no data lake (DP-17; GAP-0495; ASM-0687). The checks on treatments, payments and on the tables of rwb-case, rwb-asset and rwb-comms move to their own slices (GAP-0496; ASM-0688); the result path, the result shape and the workflow name are fixed here (GAP-0497; ASM-0689). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a daily reconciliation of the case list to `v_ace_account`, of every business key on a Workbench table to its ACE view, and of treatments and payments to their ACE records, with the variance by product and the data quality results in one Power BI report**, so that **everyone sees whether today's case list and its links can be trusted**.

The legacy story built one batch step, JOB-04 Daily reconciliation, that ran five checks REC-01 to REC-05 for the business date of the ACE batch, wrote one `reconciliation_result` row per check and product group, held or released the case list publish, and pushed two CSV extracts to the data lake for a Power BI report. D-RCV-60 keeps the behaviour and moves the ownership:

- The step becomes the activity `reconciliation` inside `ReconciliationWorkflow`, on task queue `rwb-source-data` in namespace `rwb-recovery`, started by `rwb.source-data.AceDataReady.v1` after the case list step (DP-10, DP-14; Architecture v5 slides 15 and 44; JOB-04 "event-triggered workflow", owner rwb-source-data).
- `reconciliation_result` is rwb-source-data's table in schema `rwb_source_data`, written through the service's own per-service Flyway sequence and repository, and read through `GET /admin/reconciliation/results` and `GET /admin/reconciliation/results/{resultId}` (API-P1-003; DP-01, DP-15).
- P1 owns REC-01 (account count by product), REC-02 (balance by product) and REC-05 over P1's own tables only: `case_list_row`, `interaction` and the four extension tables. REC-03 (approved treatments not booked), REC-04 (payments unmatched to proceeds) and REC-05 over the tables of rwb-case, rwb-asset and rwb-comms are the slices of RWB-P3-E1011-APP, RWB-S5-E1011-APP and RWB-P6-E1011-APP (GAP-0496; ASM-0688).
- The two lake extracts and the Power BI data set are removed: no file is written, no lake row exists, and rwb-reporting (P9) reads the results through this contract (DP-17; GAP-0495; ASM-0687).
- This slice owns the three acceptance criteria AC5, AC6 and AC8 of RWB-E1-011. AC1 to AC4 and AC7 are owned by the sibling slices and proven end to end in RWB-ITG-E1011-ITG.

### 2. Business rationale

No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. This story runs the part of the daily reconciliation that belongs to the data engine: the account count and the balance by product against `v_ace_account`, and the resolution of every business key on P1's own tables to the view that holds it. It lists every account or key that breaks, holds the publish of the case list when a product is outside the tolerance, and records one result per check and product group that any reader can query.

In the monolith the check was a Quartz step writing to a shared schema and shipping flat files to a lake that the target does not have (DP-17; Architecture v5 slides 2 and 37). In the target the same check is an event-started workflow step: it reads its own ACE views, writes its own schema, publishes nothing to Kafka, and answers the readers through one contract (DP-01, DP-05, DP-10, DP-11). The data steward and rwb-reporting therefore read the same numbers from one place, and a break is a row rather than a file somebody has to notice. It meets REQ-RDF-007 and REQ-RDF-008, applies control CTL-01, and serves the accuracy measure "reconciliation breaks cleared within one day, 100 percent". No reconciliation runs against a source load: the Workbench loads nothing, and the ACE side of every check is a read-only view.

### 3. Preconditions

- RWB-P1-E1002-CON is published: the case list contract, the `DailyCaseList` Schedule and `AceDataReady`, so the reconciliation step is started by the same event that starts the case list build (DP-10; ASM-0689).
- RWB-P1-E1015-APP is done: the daily completeness gate holds the workflow until the sources the reconciliation reads are COMPLETE for the business date, and the freshness stamps exist in `data_product_load`.
- RWB-P1-E1069-APP is done: `recovery.v_ace_account`, `v_ace_plan`, `v_ace_payment`, `v_ace_customer`, `v_ace_asset`, `v_ace_contact`, `v_ace_batch_status` and `v_ace_valuation` exist and are read by the `rwb_source_data` login only (DP-02, DP-05; Architecture v5 slides 11 and 29).
- The case list step of RWB-P1-E1002-CON has built `case_list_row` for the business date, with `publish_status` on every row and one row per case account.
- The per-service Flyway sequence of rwb-source-data carries the baseline that creates `reconciliation_result` with its unique key and index (DP-15; RWB-PLT-E1044-CON).
- RWB-P3-E1042-CON and RWB-P3-E1043-CON are published with their client libraries, and the parameter catalog holds `recon.tolerance.pct` (0.00 for REC-01 and REC-02, assumed under DL25) and `case.entry.dpd` (90, DL16). `recon.treatment.days` (2) and `recon.payment.days` (1) sit in the same catalog for the S2 and P8 slices and are not read here (GAP-0496).
- The case query contract of rwb-case returns the accounts excluded at entry for the business date, so no exclusion reads another service's table (DP-01, DP-11).
- The outbox, inbox and idempotency library is on the classpath, and the decision-record library of RWB-PLT-E1027-CON is available for the run record (DP-03).
- The task queue `rwb-source-data` exists in namespace `rwb-recovery` and a worker polls it (RWB-PLT-E1071-CON).

### 4. Flow

1. rwb-source-data consumes `rwb.source-data.AceDataReady.v1` for the business date, after the case list step of the same day has written `case_list_row` (DP-14; Architecture v5 slide 43, event 26).
2. `ReconciliationWorkflow` starts on task queue `rwb-source-data`, one run per business date, and calls the activity `reconciliation` with the business date as its input.
3. The activity reads `v_ace_batch_status` for the ALS batch of that date and uses that one business date for every check (BR12); a date the batch record does not show complete ends the run without a row.
4. REC-01, for each product group, counts the accounts in `v_ace_account` at or above `case.entry.dpd` with `data_as_of` equal to the business date, less the accounts the case query contract returns as excluded for the date, and counts the `case_list_row` rows at or above the threshold.
5. REC-02, for each product group, sums `v_ace_account.total_balance` and `case_list_row.total_balance`.
6. REC-05 resolves every business key on P1's own tables to its view row and counts the orphans: `case_list_row.account_key` to `v_ace_account`, `interaction.person_key` to `v_ace_customer`, `interaction.contact_key` and `contact_point_ext.contact_key` to `v_ace_contact`, `party_ext.person_key` to `v_ace_customer`, `account_ext.account_key` to `v_ace_account`, and `valuation_ext.valuation_key` to `v_ace_valuation` once the Section B view is deployed.
7. The activity computes the variance and the variance percent for REC-01 and REC-02, compares them with `recon.tolerance.pct`, and writes one `reconciliation_result` row per check and product group in one transaction, replacing any row already held for the same check, business date and product group (BR11).
8. The activity records the break list: account keys with their days past due for REC-01 and REC-02, and the table, column and key for every REC-05 orphan. No `dq_exception` row is written, because that table has left the schema.
9. If every REC-01 and REC-02 result for the date is PASS, the activity sets `case_list_row.publish_status` to RELEASED for the date; if any is BREAK, it sets HELD and raises MSG-P1-012 through the alert path (BR7).
10. The workflow writes one decision record for the run, with the date, the six results and the orphan count, and returns the run summary to the caller and to the job record read by `GET /admin/jobs` (DP-03).
11. A reader calls `GET /admin/reconciliation/results` with `recCode`, `product`, `result`, `from` and `to`, or `GET /admin/reconciliation/results/{resultId}`, and receives the rows of the date, the tolerance in force and the variance per row; rwb-reporting reads the same operation for its dashboards (DP-11, DP-17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product's variance is above the tolerance | The result is BREAK, the publish is held and the break rows are listed with the account keys | MSG-P1-012 | AC5 (the release half); the break criterion AC2 belongs to the sibling slices |
| X2 | The variance equals the tolerance | The result is PASS; the boundary is inclusive | None | BR6 |
| X3 | The ACE batch for the business date is not COMPLETE | The completeness gate holds the workflow, no `reconciliation_result` row is written and the publish stays held | MSG-P1-001 | BR9 |
| X4 | The run is repeated for the same date after a fix | The six rows for the date are replaced and the publish is released when every REC-01 and REC-02 result passes | None | AC5 |
| X5 | Two runs for the same date overlap | One row per check, business date and product group survives; the second run finds the key and replaces it | None | AC6 |
| X6 | A business key has no ACE row | REC-05 counts the orphan, lists the table, the column and the key, and changes no Workbench row and no ACE row | None | BR13 |
| X7 | A view returns an error during the run | No result is written for the date, the run is FAILED with the system named, and the rerun writes every row | MSG-GEN-006 | AC8 |
| X8 | A role without Platform administration R reads the results | 403 from the guard, no body of this service | MSG-P4-002 | TC-E1-011-07 |

X1 to X7 are the exception paths of RWB-E1-011 carried onto this slice; X8 is the read path the results contract adds. The waiting-period paths of REC-03 and REC-04 (legacy X1 for treatments and payments) are tested in RWB-P3-E1011-APP, RWB-S5-E1011-APP and RWB-P6-E1011-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the case list of RWB-P1-E1002-APP, the gate and stamps of RWB-P1-E1015-APP and the views of RWB-P1-E1069-APP; changes no case and reads no other service's table |
| Negotiable | The tolerance and the entry threshold are parameters; the result shape is fixed by RWB-P1-E1011-CON and the internal step order is the squad's choice |
| Valuable | Teams see each morning whether the list and its links can be trusted, and a broken list is not released |
| Estimable | One workflow, one activity, one entity and repository, three checks, one hold flag and two read operations |
| Small | Fits one sprint with its tests |
| Testable | Every criterion in section 7 is one workflow run, one row set or one refused read |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality report

  Background:
    Given the business date is 2026-11-30 and v_ace_batch_status shows ALS COMPLETED for 2026-11-30
    Given the parameter recon.tolerance.pct = 0.00 is in force for REC-01 and REC-02

  Scenario: AC5 Rerun after a fix (legacy RWB-E1-011 AC5)
    Given the SSME result for 2026-11-30 is BREAK and the publish is held
    Given P3 has created the 12 missing cases and the case list step has been rerun
    Given the rwb-case case query contract mock returns the 12 missing cases created for 2026-11-30
    When the platform administrator restarts the reconciliation step for 2026-11-30
    Then the system replaces the fifteen results for 2026-11-30 and all are PASS
    Then the system sets the publish status of the date to RELEASED and the case list extract is sent to the lake

  Scenario: AC6 Two runs for the same date (legacy RWB-E1-011 AC6)
    Given two JOB-04 runs for 2026-11-30 start on two nodes
    When both reach the reconciliation step
    Then reconciliation_result holds one row per check and product group, fifteen rows in all
    Then no row is written twice for the same rec_code, business_date and product_group

  Scenario: AC8 View unavailable during the run (legacy RWB-E1-011 AC8)
    Given v_ace_account returns an error after the MORTGAGE count is read
    When the reconciliation step runs
    Then the system writes no reconciliation_result for 2026-11-30
    Then the run shows FAILED with MSG-GEN-006 for system "ACE database"
    Then the restart writes all fifteen rows for 2026-11-30
```

**Target reading.** Every assertion above keeps its legacy wording. What changes is where it runs and who writes the row. The step is the activity `reconciliation` of `ReconciliationWorkflow` on task queue `rwb-source-data`, so "the platform administrator restarts the reconciliation step" is `POST /admin/jobs/{jobId}/rerun` with an Idempotency-Key, which starts the same workflow for the business date (API-P1-002, RWB-P1-E1002-CON); the run is observed on `GET /admin/jobs` and on the results operations of section 12.1, not on a scheduler console. The count of fifteen in AC5 and AC6 is the legacy count of five checks over three product groups; in this slice REC-03 and REC-04 belong to the S2 and P8 slices, so the rows this service writes are the REC-01 and REC-02 rows, six per date, and the REC-05 orphans are listed as breaks rather than written as result rows (GAP-0496; ASM-0688; TSD P1 v3 T3.6). The clause "the case list extract is sent to the lake" is kept word for word and read as the release of the case list for the read path of RWB-P1-E1002-APP: no lake exists in the target and no extract is written (DP-17; GAP-0495; ASM-0687). The one Given line this slice adds is the mock of the rwb-case case query contract, because the exclusion count is the only cross-service part of the check (DP-11). No legacy line is dropped or reworded.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Accounts at or above the entry threshold in `v_ace_account` for the business date are compared with the case list rows, by count per product group, every business date | REC-01; CTL-01; REQ-RDF-007 |
| BR2 | Balances in `v_ace_account` are compared with the balances on the case list rows, by sum per product group | REC-02 |
| BR3 | An approved restructure treatment whose plan is not booked in `v_ace_plan` two business days after approval is a break | REC-03; `recon.treatment.days` — owned by the treatment slice |
| BR4 | A payment in `v_ace_payment` with no proceeds matched to its `payment_code` one business day after the payment date is a break | REC-04; `recon.payment.days` — owned by the payment slice |
| BR5 | Every `account_key`, `person_key`, `contact_key` and `valuation_key` on a P1 table must resolve to a row in `v_ace_account`, `v_ace_customer`, `v_ace_contact` or `v_ace_valuation`; zero orphans, and every one is listed | REC-05; REQ-RDF-007 |
| BR6 | A result is a break when the variance percent is above the tolerance; a variance equal to the tolerance is a pass | `recon.tolerance.pct`, 0.00 assumed (DL25) |
| BR7 | A break in REC-01 or REC-02 holds the publish of the case list for the business date and lists the break rows for the data steward | FEAT-RDF-13; REC-01 "Break list to the data steward" |
| BR8 | Accounts excluded at entry are explained and do not count as breaks; the exclusions arrive through the rwb-case case query contract and are never read from its table | REC-01; REQ-CWC-004 |
| BR9 | No reconciliation runs until the completeness gate reports COMPLETE for the sources the reconciliation reads on the business date | BR-P1-014-4; MSG-P1-001 |
| BR10 | Result grades: PASS, BREAK or NOT_RUN, with the reason carried on the run record and on the freshness read of the date | FEAT-RDF-12 |
| BR11 | A repeated run for the same date replaces that date's rows; the unique key is `rec_code`, `business_date` and `product_group` | R-UNI-40 |
| BR12 | The reconciliation reads ACE for the business date of the ACE batch it was started by, and never a mix of two business dates | BR-P1-011-2 |
| BR13 | A REC-05 orphan never deletes or changes a Workbench record or an ACE row; it is listed for the data steward and, where the row is missing in ACE, for the ACE team | BR-P1-011-3 |

**Where each rule lives in the target.** BR1, BR2, BR5, BR6, BR7, BR8, BR9, BR11, BR12 and BR13 are this story's and run inside the `reconciliation` activity. BR3 and BR4 are kept with their legacy identifiers and their parameter names so that the registers stay readable, but the checks and their breaks belong to the treatment and payment slices (GAP-0496); P1 writes no row for them and reads no treatment or proceeds table (DP-01). BR10 is the grade vocabulary of the result row and of the freshness read, and the report that used to carry it as a colour is now the query of section 12.1.

### 9. State transitions

None. This story does not change a case status. It writes `reconciliation_result` (PASS or BREAK) and sets `case_list_row.publish_status` for the business date.

| From | Event | Condition | To |
|---|---|---|---|
| No run for the date | AceDataReady consumed | The completeness gate reports COMPLETE | Run started |
| Run started | The three checks complete | Every REC-01 and REC-02 result is PASS | Publish RELEASED |
| Run started | The three checks complete | Any REC-01 or REC-02 result is BREAK | Publish HELD, MSG-P1-012 raised |
| Run started | A view returns an error | The transaction rolls back | Run FAILED, no row for the date |
| Publish HELD | The rerun for the same date | Every result is PASS | Publish RELEASED, rows replaced |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| `rwb_source_data`, the service login | Runs the reconciliation; writes `reconciliation_result` and the publish status; reads the ACE views and P1's own tables |
| RW-DATASTEW, data steward and data product owner | Reads results and break rows (Platform administration R); signs the daily reconciliation to ACE |
| RW-PLATADM, platform administrator | Reads results; restarts the run for a business date (Platform administration U) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read results and break rows (Platform administration R) |
| RW-TEAMMGR and other report readers | Read the results through rwb-reporting and the case list views (Reporting R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-187 | v_ace_valuation | valuation_key | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read |
| DF-ACE-179 | v_ace_batch_status | business_date | Read |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read |
| DF-RPT-002 | case_list_row | business_date | Read |
| DF-RPT-005 | case_list_row | account_key | Read |
| DF-RPT-007 | case_list_row | product_group | Read |
| DF-RPT-014 | case_list_row | total_balance | Read |
| DF-RPT-015 | case_list_row | days_past_due | Read |
| DF-RPT-019 | case_list_row | publish_status | Write |
| DF-CAS-057 | case_entry_exclusion | account_key | Read through the case query contract |
| DF-CAS-058 | case_entry_exclusion | business_date | Read through the case query contract |
| DF-INT-003 | interaction | person_key | Read (REC-05) |
| DF-INT-022 | interaction | contact_key | Read (REC-05) |
| DF-EXT-004 | party_ext | person_key | Read (REC-05) |
| DF-EXT-017 | contact_point_ext | contact_key | Read (REC-05) |
| DF-EXT-028 | account_ext | account_key | Read (REC-05) |
| DF-EXT-038 | valuation_ext | valuation_key | Read (REC-05) |
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

**Which side is this story's.** The `DF-ACE-` rows are read in this service's own views and nowhere else (DP-01, DP-05); the `DF-RPT-` and `DF-OPS-` rows are P1's tables; `DF-CAS-057` and `DF-CAS-058` are read through the rwb-case case query contract and are not read from `rwb_case` (DP-01, DP-11). `treatment` (`DF-TRT-`) and `proceeds` (`DF-FIN-`), and the tables of rwb-case, rwb-asset and rwb-comms, leave this slice with REC-03, REC-04 and their part of REC-05 (GAP-0496). The extension-table field IDs are the four rows of RWB-P1-E1069-DB and are read here, never created.

### 12. Contract

#### 12.1 REST operations provided

Two read operations on base `/api/recovery/source-data/v1` (DP-13), owner rwb-source-data (P1), access Platform administration R with scope applied.

| Method | Path | Purpose | Idempotency |
|---|---|---|---|
| GET | `/admin/reconciliation/results` | The result rows of a date range, filtered by `recCode`, `product`, `result`, `from` and `to`, with the variance and the tolerance in force on each row | Idempotent; no state change |
| GET | `/admin/reconciliation/results/{resultId}` | One result row with its break rows: the account keys and days past due for REC-01 and REC-02, the table, column and key for REC-05 | Idempotent; no state change |

API-P1-003 keeps its ID and its purpose from TSD P1 v3 T-A.2 and changes only its base, which is the service base of the target (DP-13). The single-row path, the name `resultId` and the element names of the answer are not given by any source and are fixed here for the contract baseline (GAP-0497; ASM-0689); the five filter names are copied from TSD P1 v3 T-A.2, and RWB-P1-E1011-CON publishes the OpenAPI document and may rename an element only through the versioning rule. The errors are 401, 403 and 503 on the list and 401, 403, 404 and 503 on the single row, with the platform problem body. `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` are RWB-P1-E1002-CON's and are consumed here, not provided.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| POST | the case query operation of the rwb-case contract | P3 rwb-case | The accounts excluded at entry for the business date, by product group | DP-11; one hop, 2 s timeout, faked from Day 1 |
| GET | the parameter read of the rwb-case contract | P3 rwb-case | `recon.tolerance.pct` and `case.entry.dpd` in force on the business date, read as data through the client library | DP-06 |
| GET | the reference-data read of the rwb-case contract | P3 rwb-case | The product groups of `LOV-PRODUCT` and the result list `LOV-REC-RESULT` | DP-07 |

No other service is called at run time. The ACE side of every check is this service's own view (DP-05), and the treatment, payment, asset and notice checks of the legacy story are not run here (GAP-0496).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP. This story writes no outbox row of its own and publishes no reconciliation event.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Starts `ReconciliationWorkflow` for the business date, after the case list step; the inbox dedupes on the event id |

The event carries the source system, the business date, the status and the completion time; it carries no personal data (DP-09, DP-14; Architecture v5 slides 42 and 43).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ReconciliationWorkflow` | Workflow, one run per business date, workflow ID `recon-{businessDate}` | `rwb-source-data` | Input: business date, source system, event id. Output: the six result rows and the orphan count (GAP-0497; ASM-0689) |
| `reconciliation` | Activity | `rwb-source-data` | Input: business date and source system. Output: the run summary. It reads the views, computes REC-01, REC-02 and REC-05, writes the rows and sets the publish status in one transaction |

Both run in namespace `rwb-recovery` through the workflow kit of RWB-PLT-E1071-CON (DP-10). The run record is also written to the local decision record (DP-03).

#### 12.6 Schedules

None. The workflow is event-started by `rwb.source-data.AceDataReady.v1`. The fallback daily start of the service is the `DailyCaseList` Schedule of RWB-P1-E1002-CON, which runs the same business date and reaches this step; this story registers no Schedule and no Quartz job of its own (DP-10; Architecture v5 slide 44).

#### 12.7 Tables owned

| Object | Schema | Owner | This story |
|---|---|---|---|
| `reconciliation_result` | `rwb_source_data` | P1 | Owned and written: one row per check, business date and product group, unique on `(rec_code, business_date, product_group)` |
| `case_list_row` | `rwb_source_data` | P1 | Read for REC-01 and REC-02; `publish_status` written for the business date |
| `data_product_load` | `rwb_source_data` | P1 | Read for the completeness gate of the date; no row written here |
| `interaction`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | Read for REC-05; no row written, no key changed |
| `outbox_event`, `processed_event`, `idempotency_key` | `rwb_source_data` | PLT library | The inbox dedupe of the consumed event and the idempotency key of the rerun |

No table of another service is read and no foreign key crosses a schema (DP-01). `case_entry_exclusion`, `recovery_case`, `treatment`, `proceeds` and the asset and notice tables are reached through their owners' contracts or not at all.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P1-E1002-CON fake | The case list contract and `AceDataReady` | A `case_list_row` set for 2026-11-30 with three product groups, a `publish_status` per row, and an `AceDataReady` event |
| RWB-P3-E1042-CON fake | The parameters contract | `recon.tolerance.pct` 0.00 and 0.10, `case.entry.dpd` 90, `recon.treatment.days` 2, `recon.payment.days` 1 |
| RWB-P3-E1043-CON fake | The reference-data contract | `LOV-PRODUCT` MORTGAGE, HIRE_PURCHASE, SSME; `LOV-REC-RESULT` PASS, BREAK, NOT_RUN |
| The rwb-case case query fake | The exclusion count | The 12 missing SSME cases of AC5 and an empty exclusion list |
| View fixture | RWB-P1-E1069-APP | A container with the eight views, the ACE batch row for 2026-11-30, and a stub of `v_ace_account` that fails after the MORTGAGE count |

The fakes are test-only and are not deployed above SIT.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 read operations on `/api/recovery/source-data/v1` | 3 (case query, parameters, reference data) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | 1 (`rwb.source-data.AceDataReady.v1`) | Inbox dedupe on the event id; no event published |
| Temporal | 1 workflow, 1 activity | None | `ReconciliationWorkflow` and `reconciliation` on task queue `rwb-source-data` |
| File | None | None | No extract is written and no lake exists (DP-17) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `recon`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), Temporal task queue `rwb-source-data` in namespace `rwb-recovery` (DP-13, DP-14).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is this story's own pattern: JOB-04 was a Quartz step in a shared job table, and it becomes an event-started workflow on the service's own queue. DP-17 is used as a removal: both extracts and the report that read them are dropped, and the read moves to 12.1. DP-05 is used, not delivered: the views are RWB-P1-E1069-APP's. DP-19 applies to the admin surface that renders the result list through gateway-bff; the screen itself is not built here.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ReconciliationWorkflow` | Workflow | One run per business date; input, retry and run record |
| `reconciliation` | Activity | The three checks, the variance and the tolerance, the replace of the date and the publish status |
| `ReconciliationResult` | Entity | Maps `reconciliation_result`, one row per check and product group |
| `ReconciliationResultRepository` | Repository | Replaces one date's rows in one transaction; the query of 12.1 |
| `ReconciliationService` | Service | Counts, sums, variances and the PASS or BREAK decision against the tolerance |
| `ReferentialCheck` | Service | REC-05 over P1's own key families; lists the orphans and changes no row |
| `CaseListPublishGate` | Service | Sets HELD or RELEASED for the date; the case list read of RWB-P1-E1002-APP publishes only when RELEASED |
| `ReconciliationController` | Controller | The two read operations with RFC 9457 problem details |
| `LoadAlertNotifier` | Service | Raises MSG-P1-012 on a hold and MSG-GEN-006 on a failed run |

**Database.** `reconciliation_result` is created by the service baseline with the columns of section 11 and the unique key `(rec_code, business_date, product_group)`; the next version adds index `ix_reconciliation_date` on `(business_date, rec_code, product_group)`. No `dq_exception` and no `dq_rule` exists or is created. REC-05 reads P1's own tables by business key and the views; it adds no foreign key and changes no row (DP-01, DP-15).

**Configuration and reference data.** `recon.tolerance.pct`, `recon.treatment.days`, `recon.payment.days` and `case.entry.dpd` come from the parameter catalog of RWB-P3-E1042-CON through the client library, loaded by the centre-of-excellence analyst; a tolerance change also needs Risk approval (reference data change process, step 4). The product groups and the result list are reference data (DP-07). No value is a constant in the code (DP-06).

**Build steps**

1. Write `ReconciliationResult`, its repository and the index migration; test the replace of one date.
2. Write `ReconciliationService` for REC-01 and REC-02 with the exclusions from the case query contract; unit test variance 0, the tolerance boundary and a break.
3. Write `ReferentialCheck` for the six key families of P1's own tables; test each view, the Section B view being absent, and the composite `contact_key`.
4. Write the break listing in both directions and the replacement on a passing rerun.
5. Write `CaseListPublishGate` and the release path that the publish step of the case list story reads; this replaces the total count check of that story.
6. Write the gate-HOLD path, with the NOT_RUN checks and the held publish.
7. Write `ReconciliationWorkflow` and the `reconciliation` activity on the workflow kit, with the retry policy and the run record (DP-03, DP-10).
8. Write the two read operations of 12.1 with the filters and the problem body.
9. Add the run to the job listing of RWB-P1-E1002-CON and the rerun binding that starts this workflow for a business date.

**Feature flag.** `rwb.p1.reconciliation`. Off: the case list is released as in RWB-P1-E1002-APP with its own count line, and no result row is written.

**Done when.** The tests in section 16 pass, SIT holds one `reconciliation_result` row set per business date for three product groups, the workflow is started by `AceDataReady` and by the rerun path, and the two read operations answer for 2026-11-30 with the tolerance in force.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The ACE batch is not complete; reconciliation not run | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-006 | A view or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the right reads the results | You cannot {action} here. Your role does not include it. |

The texts are the legacy ones and are copied unchanged.

### 15. Screens and states

No Workbench screen in this story and no Power BI report. The result list is rendered by the admin surface that calls 12.1 through the gateway-bff composite route (DP-19), and the team manager reads the same figures in the rwb-reporting dashboard, which reads this contract (DP-17). The states a reader sees are PASS, BREAK and NOT_RUN per product group for a business date, with the publish state RELEASED or HELD and the break rows behind each row. SCR-45 Data quality in Epic 2 shows the same breaks through its own story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07 | AC5; BR7; the 403 path of 12.1 | Component | RW-CASEOWN calls `GET /admin/reconciliation/results`; refused with MSG-P4-002 |
| TC-E1-011-01 | AC5, BR1, BR2, BR5, BR8, BR10 | End to end | Synthetic accounts MORTGAGE 12,256, HIRE_PURCHASE 12,960, SSME 2,903 with exclusions; clean REC-05 |
| TC-E1-011-02 | AC5, BR6, BR7 | End to end | 12 SSME accounts missing from the case list; six rows written |
| TC-E1-011-03 | BR6 | Component | Tolerance 0.10; variances 0.10 and 0.11 percent |
| TC-E1-011-04 | AC8, BR9, BR10 | End to end | No COMPLETED ALS row for 2026-11-30 |
| TC-E1-011-05 | AC5, BR11 | End to end | Break, missing cases created, rerun for the same date |
| TC-E1-011-06 | AC6, BR11 | End to end | Two workflow runs for one business date on two workers |
| TC-E1-011-08 | BR5, BR13 | Component | `party_ext` person_key P0099881 absent from `v_ace_customer` |
| TC-E1-011-09 | AC8, BR12 | Component | `v_ace_account` stub returning an error after the MORTGAGE count |

The legacy test case IDs, their order and their data are kept; the legacy level "System" maps to "End to end" and "Access" to "Component". TC-E1-011-01 to TC-E1-011-04 are carried as regression evidence for the REC-01 and REC-02 halves that remain in this slice, and the treatment, payment and cross-service halves of the same legacy cases are owned by the sibling slices and the integration story. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies belong to RWB-ITG-E1011-ITG and are not listed here.

### 17. Guardrails

- No business value in code: the tolerance, the entry threshold and the waiting periods are parameters read through the client library, and the product groups and the result list are reference data (DP-06, DP-07).
- No personal data in events, workflow inputs or logs: the input is a business date and a source system, the run record carries counts and codes, and a break row carries account keys, account numbers and business keys only.
- ACE data only through the owner's contract or `recovery.v_ace_*` views: every ACE field of this story is read in this service's own view (DP-01, DP-05).
- No cross-schema read and no cross-schema key: `reconciliation_result` and `case_list_row` sit in `rwb_source_data`, no foreign key leaves the schema, and the exclusion count arrives over the rwb-case contract rather than from `rwb_case` (DP-01).
- No lake, no extract and no Power BI data set: the read path is 12.1 and nothing is written to a file (DP-17).
- A held case list is never released by hand from this story; the release is the passing rerun (BR11).
- A break never changes an ACE row or a Workbench row (BR13).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count in `v_ace_account` with no variance, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | REC-01; REC-02; REC-05; CTL-01; R-UNI-40 | TC-E1-011-01 to TC-E1-011-09 |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | REC-05; CTL-01 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-07, TC-E1-011-08 |
| REQ-CWC-004 | Exclusion rules are data, and an excluded account is explained rather than counted as a break | Epic 1, 3.1 | FEAT-RDF-11 | BR8 | TC-E1-011-01 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1011-CON | Contract | H build dependency: the result resource, the two read operations and the workflow and activity contract |
| RWB-P1-E1011-OPS | DevOps | X external dependency: the deployment, the worker, the alerts and the rerun binding |
| RWB-P1-E1002-CON | Contract | H build dependency: the case list contract, `DailyCaseList` and `AceDataReady` |
| RWB-P1-E1015-APP, RWB-P1-E1069-APP | App development | H build dependency: the completeness gate and the views |
| RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P6-E1011-APP | App development | Siblings of the legacy key: REC-03, REC-04 and REC-05 over their own tables |
| RWB-ITG-E1011-ITG | Integration | Proves AC1 to AC4 and AC7 end to end across the services |

### 19. Out of scope

- REC-03 (approved treatments not booked) and REC-04 (payments unmatched to proceeds): the treatment and payment slices, RWB-P3-E1011-APP, RWB-S5-E1011-APP and RWB-P6-E1011-APP, with `recon.treatment.days` and `recon.payment.days`.
- REC-05 over the tables of rwb-case, rwb-asset and rwb-comms: the same sibling slices; this story resolves P1's own keys only.
- The two lake extracts, the Power BI data set and the 07:30 refresh: removed with the data lake (DP-17; GAP-0495).
- The contract documents, the fakes as published artefacts and the naming of the result elements: RWB-P1-E1011-CON.
- The deployment, the KEDA scaling, the alerts and the rerun binding: RWB-P1-E1011-OPS.
- Working a break to closure with an owner and a date, and releasing a held publish by hand (FEAT-RPT-09 full scope, Epic 2).
- Reconciliation of write-offs (REC-06), assets taken on (REC-07), the decision log copy (REC-08) and notice barcodes (REC-09).
- The data quality console SCR-45 and the quality measure definitions (Epic 2 and Epic 8).

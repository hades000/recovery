# RWB-P1-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group, 27 November 2026.
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
| Size | Not specified in the source documents (DOR-RWB-P1-E1011-APP-16) |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1011-CON, RWB-P1-E1015-APP and RWB-P1-E1069-APP, with rwb-case contracts or provider fakes available |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1015-APP, RWB-P1-E1069-APP, RWB-P1-E1011-CON |
| Contract dependencies | RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, rwb-case allocation and key/exclusion reads (NEW-GAP-B2, GAP-0337, NEW-GAP-S2B-01). AD018 job operations are a wave 4 integration dependency. |
| Contract version | API Specification v7 `rwb-source-data.yaml` 5.1.0 (RD-P1-005) |
| Integration dependencies | None |
| External dependencies | RWB-P1-E1011-OPS |
| Open decisions | DL16: use `case.entry.dpd` from the catalog (90 in the fixture, ASM-1094, ASM-5264). DL25: option A applies, `recon.tolerance.pct` v1 = 0.00 pending data lead confirmation (NEW-ASM-C6). |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-008, FR-P1-010, FR-P1-018, FR-P1-019, FR-P1-020, FR-P1-021, FR-P1-022, FR-P1-023) |
| Readiness decisions | RD-P1-001, RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-028, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043, RD-P1-044, RD-P1-065, RD-P1-069 |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P1-E1011-APP-14) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-011 for rwb-source-data. The reconciliation becomes one activity of `ReconciliationWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, started by `rwb.source-data.AceDataReady.v1` (DP-10, DP-14; Architecture v5 slides 15 and 44). The results are read through this service's contract on `/api/recovery/source-data/v1` instead of two lake extracts and a Power BI data set, because the target has no data lake (DP-17; GAP-0495; ASM-0687). The checks on treatments, payments and on the tables of rwb-case, rwb-asset and rwb-comms move to their own slices (GAP-0496; ASM-0688); the result path, the result shape and the workflow name are fixed here (GAP-0497; ASM-0689). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E1011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 49 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Version 3 changes**

- RD-P1-022/024/040 retain E1011 reconciliation and the E1015 parent while removing the P1 case-list write (RWB-P1-E1011-APP#6, #7, #10–#12, #20–#21).
- RD-P1-028/042 align the dated inputs, two result codes, tolerance and failure paths (RWB-P1-E1011-APP#1–#5, #9, #13–#14, #22, #24–#25).
- RD-P1-001/004/005/006/011/012/020 align the protected reads, AD018 handoff, fakes and fixtures (RWB-P1-E1011-APP#8, #15–#19, #23, #26–#29).
- Finishing pass (RD-P1-065, RD-P1-069; requests S9-stories-0445, W3-messages-0035; test case backfill): a repeated readiness call starts no second run; REC-04 and REC-06 belong to rwb-payment and REC-05 only to this service; break detail stays aggregate-only; the SCR-45 route is RWB-P3-AD019-APP's; Test Cases v9 IDs and current standard versions are cited.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: applied RD-P1-001, RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-006, RD-P1-008, RD-P1-011, RD-P1-012, RD-P1-020, RD-P1-022, RD-P1-024, RD-P1-025, RD-P1-028, RD-P1-040, RD-P1-041, RD-P1-042, RD-P1-043, RD-P1-044.

### 1. Story

As a **data steward (RW-DATASTEW)**, I want **daily account-count, balance and business-key reconciliation results**, so that **I can see which products differ from ACE and identify missing references**.

JOB-04 is the daily reconciliation owned by this slice. D-RCV-60 and RD-P1-022/024 allocate the work as follows:

- The step becomes the child workflow `ReconciliationWorkflow` inside the `AceIngestCheck` run owned by RWB-P1-E1015-APP, after the ALS stamp (RD-P1-022, RD-P1-024). It runs on task queue `rwb-source-data` in namespace `rwb-recovery` with workflow ID `recon-{businessDate}`.
- `reconciliation_result` is rwb-source-data's table in schema `rwb_source_data`, written through the service's own per-service Flyway sequence and repository, and read through `GET /admin/reconciliation/results` and `GET /admin/reconciliation/results/{resultId}` (API-P1-003; DP-01, DP-15).
- P1 owns REC-01 (account count by product), REC-02 (balance by product) and the P1 and open-case key checks in REC-05. Other business-key checks and the treatment and payment reconciliations stay with their owning slices (GAP-0496, ASM-0688).
- The two lake extracts and the Power BI data set are removed: no file is written, no lake row exists, and rwb-reporting (P9) reads the results through this contract (DP-17; GAP-0495; ASM-0687).
- This slice owns the three acceptance criteria AC5, AC6 and AC8 of RWB-E1-011. AC1 to AC4 and AC7 are owned by the sibling slices and proven end to end in RWB-ITG-E1011-ITG.

### 2. Business rationale

This slice compares ACE accounts and balances with the dated open-case answers from rwb-case, and checks the business keys listed in section 11. The data steward reads the aggregate results through the protected result API.

The workflow reads local ACE views and writes results to its own schema (DP-01, DP-05, DP-10). It meets REQ-RDF-007 and REQ-RDF-008 and applies CTL-01. The Workbench reads ACE without writing to it.

### 3. Preconditions

- RWB-P1-E1015-APP owns `AceIngestCheck`, `DailyCompletenessGate`, freshness stamps and ACE outbox events. E1011 runs as the child after the ALS stamp (RD-P1-022/040/041).
- RWB-P1-E1069-APP provides the ACE views in section 11. Only the P1 service login reads them.
- The P1 baseline creates `reconciliation_result`. This story adds `ix_reconciliation_date`.
- RWB-P3-E1042-CON and RWB-P3-E1043-CON provide parameters and LOVs. RD-P1-028 and RD-P1-042 set the catalog source and DL25 default.
- Pending: paged rwb-case open-case key read for the business date (including case-account and case-party keys), owner rwb-case service owner, tracked as NEW-GAP-B2.
- Pending: rwb-case allocation status and exclusion operations, including paths, payloads, paging and provider fakes, owner rwb-case service owner, tracked as GAP-0337 and NEW-GAP-S2B-01. The contract also needs to define the dated open-case balances and eligible account set for REC-02.
- The DP-03 decision-record library and the `rwb-source-data` queue in namespace `rwb-recovery` are available.

### 4. Flow

1. `ReconciliationWorkflow` (`recon-{businessDate}`) registers one activity, `reconciliation`, on task queue `rwb-source-data` in namespace `rwb-recovery` (contract jar major 1). The child input is `{businessDate, startedBy}`. E1015 starts it with parent close policy ABANDON in the workflow task that commits the ALS stamp (source status COMPLETED), using USE_EXISTING and ALLOW_DUPLICATE. Before REC-01, use durable timers to poll the rwb-case allocation answer every `recon.allocation.poll.minutes` (5 in the values file, NEW-ASM-X2). Proceed at ALLOCATION_COMPLETE YES or the `caselist.allocation.wait.until` limit (07:15 Asia/Bangkok, rwb-case parameter) when the contract is readable. An unreadable answer blocks the checks and produces no result rows (RD-P1-042).
2. Read `case.entry.dpd` and `recon.tolerance.pct` in force on the business date through RWB-P3-E1042-CON, and the product LOV through RWB-P3-E1043-CON.
3. REC-01 compares counts of eligible `v_ace_account` rows for the date, excluding accounts excluded at entry, with matching dated open-case account counts from rwb-case. Use `days_past_due >= case.entry.dpd` on the ACE population and keep the account keys distinct.
4. REC-02 compares the sums of `total_balance` for the same populations by product. Read `v_ace_account.product_category` (DF-ACE-010) directly as the matching LOV-PRODUCT code, per Source to Target Mapping v6 DF-CAS-003. Iterate MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED.
5. REC-05 is the business-key check in RD-P1-020/022 (REC-09 in Data Quality and Reconciliation Rules v4, GAP-0273 / ASM-0363). Resolve P1 account, party, contact, valuation and interaction keys and the dated open `case_account.account_key` and `case_party.person_key` keys served by rwb-case. Asset and payment keys are checked by their owners. Match `contact_point_ext` on `(contact_type, contact_key)` per Conceptual Data Model v7. The `interaction.contact_key` uses the `contact_type:key` form (Data Classification v5). Pending: null/blank key treatment and handling of a missing `v_ace_valuation` with Section B enabled, owner data architect, tracked as NEW-GAP-S2B-07. With Section B off, RD-P1-043 prevents the child from starting.
6. Compute the variance using BR6 and atomically replace REC-01 and REC-02 aggregates for the date, two per product. If the run cannot proceed or fails mid-read, leave any previously committed set intact.
7. Pending: durable break-detail store and locator for the detail response, including REC-05 orphans, owner P1 data architect with the contract owner, tracked as GAP-1508 and NEW-GAP-S2B-03. The existing aggregate schema is limited to REC-01 and REC-02. GAP-0575 and RD-P1-010 settle the candidate-read response. Do not create a legacy exception table or insert REC-05 into `reconciliation_result`. Interim: the result reads answer aggregates and the consoles and tests assert counts; no P1 v1 read serves REC-09 break rows or held proof-of-delivery rows (GAP-0577, GAP-1508) (RD-P1-069).
8. A BREAK raises MSG-P1-012 and the Reconciliation break alert for the data steward. Route through E1011-OPS values (RD-P1-028/044). Pending: alert destination and REC-02 balance wording/placeholder units in MSG-P1-012, owner observability owner with the Error and Message Standard owner, tracked as NEW-GAP-S2B-08. Pending: effect on the rwb-case list, owner solution architect with the data lead, tracked as NEW-GAP-X3.
9. Write one DP-03 decision record per completed execution with date, check codes, result indicators, counts and the orphan count. Keep identifiers, balances at account level and names out of this record and workflow history. The library emits `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (RD-P1-008). AD018 provides the job record projection when released.
10. Serve the reads in section 12.1.

### 5. Exception paths

| ID | Trigger | Outcome | Evidence |
|---|---|---|---|
| X1 | Variance above tolerance | Persist BREAK, raise MSG-P1-012 and the Reconciliation break alert | AC9, AC22 |
| X2 | Variance equals tolerance | Persist PASS | AC10 |
| X3 | ACE gate HOLD | No child execution results and no aggregate writes. E1015 owns MSG-P1-001 | AC11 |
| X4 | Failed run retried or restarted | On completion replace the entire date set atomically | AC5, AC23 |
| X5 | Two automatic starts overlap | USE_EXISTING joins the open workflow | AC6 |
| X6 | ACE key missing | Count the orphan without mutating source facts. Detail contract pending in section 12.7 | AC12 |
| X7 | View error or transient activity failure | After retries fail the run with MSG-GEN-006 and preserve the prior aggregate set | AC8, AC16 |
| X8 | Read right or scope refused | 403 MSG-P4-002 in the platform Problem | AC13 |
| X9 | rwb-case allocation, key, exclusion, parameter or LOV read fails | Fail the run after retries with MSG-GEN-006 naming rwb-case; write no result rows | AC20 |
| X10 | Allocation remains incomplete through the limit | Run at the configured limit if the allocation answer remains readable | AC27 |
| X11 | Invalid query or store unavailable | Use the section 12.1 Problem mapping | AC25 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Depends on the rwb-case read contracts, E1015 ingest and E1069 views |
| Negotiable | The tolerance and the entry threshold are parameters; the result shape is fixed by RWB-P1-E1011-CON and the internal step order is the squad's choice |
| Valuable | Exposes dated differences and unresolved references for the data steward |
| Estimable | One workflow, one activity, three checks, aggregate persistence and two reads, with detail contract pending |
| Small | Pending squad sizing |
| Testable | Every criterion in section 7 is one workflow run, one row set or one refused read |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality report

  Background:
    Given the fixture business date is 2026-11-30 and the catalog tolerance is 0.00 unless a scenario overrides it

  Scenario: AC5 Restart after corrected inputs
    Given the 2026-11-30 execution failed and the data steward has corrected all differences in the dated inputs
    When reconciliation completes on restart
    Then it atomically replaces the date set with eight PASS rows, REC-01 and REC-02 for each LOV-PRODUCT value
    And it writes one decision record for the completed execution

  Scenario: AC6 Concurrent automatic starts
    Given two automatic starts target recon-2026-11-30 while the first execution is open
    When Temporal handles the second start
    Then USE_EXISTING joins the open execution and the completed run has one aggregate row per check, business date and product

  Scenario: AC8 ACE fails mid-read
    Given v_ace_account fails after the MORTGAGE count was read
    When reconciliation exhausts its ten attempts
    Then the execution fails with MSG-GEN-006 for ACE database and the store holds no partial rows for 2026-11-30

  Scenario: AC9 Count break
    Given SSME source_count is 2903 and workbench_count is 2891 with tolerance 0.00
    When reconciliation completes
    Then REC-01 stores variance_count 12, variance_pct 0.4134, tolerance_pct 0.00 and result BREAK
    And it raises MSG-P1-012 and the Reconciliation break alert for SSME

  Scenario: AC10 Inclusive tolerance
    Given recon.tolerance.pct equals 0.10
    When two count checks compare 1000000 with 999000 and 1000000 with 998999 respectively
    Then the two rows store variance_pct 0.1000 and 0.1001 and result PASS and BREAK respectively

  Scenario: AC11 ACE batch incomplete
    Given the ALS batch is absent or its status is not COMPLETED for 2026-11-30
    When the E1015 completeness gate reports HOLD
    Then E1015 raises MSG-P1-001 and reconciliation writes no result rows

  Scenario: AC12 REC-05 orphan
    Given party_ext.person_key P0099881 has no row in v_ace_customer
    When REC-05 completes
    Then the run summary and decision record include one orphan and the existing party_ext and ACE rows are unchanged
    And the aggregate store has no REC-05 row

  Scenario: AC13 Read without Platform administration R
    Given RW-CASEOWN has no Platform administration R
    When it calls either reconciliation read with otherwise accepted input
    Then the answer is a 403 Problem with messageCode MSG-P4-002 and no reconciliation data

  Scenario: AC14 Treatment and payment checks are outside this workflow
    Given the business date is 2026-11-30 and the ALS batch is COMPLETED
    When reconciliation completes
    Then it writes no REC-03 or REC-04 row and reads no treatment or proceeds table

  Scenario: AC15 Unauthenticated and missing result
    Given a request has no credentials or an authorised detail request carries a UUID absent from the store
    When the read is sent
    Then the respective answer is a 401 Problem MSG-P4-001 or a 404 Problem MSG-P4-003

  Scenario: AC16 Retry exhaustion preserves the last committed set
    Given every attempt fails for a date with an existing full result set
    When the tenth attempt fails after backoff beginning at 1 s with coefficient 2
    Then the execution fails and all previous aggregates are unchanged

  Scenario: AC18 Unmapped product is visible as an unresolved input
    Given a dated account at 90 days past due has an unmapped product category
    When the reconciliation input is checked
    Then the account cannot be silently omitted from a reported complete result set
    And the final mapping and failure assertion are pending NEW-GAP-S2B-05

  Scenario: AC19 Exclude both sides
    Given the dated exclusion fixture returns one 90-days-past-due account absent from open cases
    When reconciliation completes with all other account keys and balances matching
    Then REC-01 and REC-02 both pass with the excluded account and its balance outside both populations

  Scenario: AC20 Unavailable rwb-case dependency
    Given the rwb-case allocation, key, exclusion, parameter or LOV read returns 503 or exceeds the 2 s caller timeout
    When all attempts for the failing read path are exhausted
    Then the run fails with MSG-GEN-006 for rwb-case and writes no reconciliation rows

  Scenario: AC21 Empty product group
    Given a product has zero source and zero Workbench accounts and no balances
    When reconciliation completes
    Then its REC-01 and REC-02 rows have variance_count 0, variance_pct 0.0000 and result PASS

  Scenario: AC22 Balance break with matching counts
    Given SSME source and Workbench counts are 1, balances are 100.00 and 99.99 baht and tolerance is 0.00
    When reconciliation completes
    Then REC-01 is PASS and REC-02 stores variance_count 0, variance_pct 0.0100 and result BREAK
    And MSG-P1-012 and the Reconciliation break alert are raised

  Scenario: AC23 AD018 authorisation and replay after wave 4
    Given AD018 serves a FAILED JOB-04 run and the business date has a COMPLETED ALS batch
    When RW-PLATADM submits and repeats a bodyless rerun with the same canonical UUID Idempotency-Key
    Then both answers are the stored 202 Job and one new workflow starts with runNo incremented
    And without Platform administration U the answer is 403 MSG-P4-002
    And for a FAILED run of an incomplete business date the answer is 409 MSG-P1-001

  Scenario: AC24 ACE event redelivery cannot start this child
    Given E1015 has committed the ALS stamp and started the reconciliation child
    When AceDataReady is published again on rwb.source-data.events.v1
    Then E1011 consumes no event and starts no additional child from Kafka

  Scenario: AC25 Query validation and store failure
    Given an authorised read has malformed syntax, a filter outside its list, from later than to, or a well-formed query against an unavailable store
    When the request is sent
    Then the respective Problem is 400 MSG-GEN-001, 400 MSG-GEN-007, 422 MSG-GEN-003 or 503 MSG-GEN-006

  Scenario: AC26 Decision record and workflow history
    Given a completed execution with REC-01, REC-02 and REC-05 counts
    When the decision record, logs and workflow history are inspected
    Then the decision record holds the business date, check outcomes and counts and none of these surfaces holds account numbers or customer names

  Scenario: AC27 Allocation waiting limit
    Given the rwb-case allocation answer remains readable and incomplete for 2026-11-30
    When 07:15 Asia/Bangkok is reached with the configured wait value
    Then the child starts the checks using the business-date inputs and records no allocation check as a P1 result
```

The legacy AC17 is withdrawn with the P1 case-list state change (RD-P1-024). AC12 covers the orphan count. Detail response assertions await the store and result locator in section 12.7.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Count dated ACE accounts at or above the entry threshold, less entry exclusions, against the open-case side, per product. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR2 | Compare balances in baht over the REC-01 account populations by product. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR3 | An approved restructure treatment whose plan is not booked in `v_ace_plan` two business days after approval is a break | REC-03; `recon.treatment.days` — owned by the treatment slice |
| BR4 | A payment in `v_ace_payment` with no proceeds matched to its `payment_code` one business day after the payment date is a break | REC-04; `recon.payment.days` — computed, with REC-06, by the rwb-payment daily reconciliation (RWB-P8-E4050-APP) into `rwb_payment` (RD-P1-069) |
| BR5 | REC-05 is the business-key check in RD-P1-020/022 (REC-09 in Data Quality and Reconciliation Rules v4, GAP-0273 / ASM-0363). Resolve P1 account, party, contact, valuation and interaction keys and the dated open `case_account.account_key` and `case_party.person_key` keys served by rwb-case. Asset and payment keys are checked by their owners. Match `contact_point_ext` on `(contact_type, contact_key)` per Conceptual Data Model v7. The `interaction.contact_key` uses the `contact_type:key` form (Data Classification v5). Pending: null/blank key treatment and handling of a missing `v_ace_valuation` with Section B enabled, owner data architect, tracked as NEW-GAP-S2B-07. With Section B off, RD-P1-043 prevents the child from starting. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR6 | For REC-01 use counts and for REC-02 use balances in baht as the percentage operands. Store the absolute count difference in `variance_count` for both checks. For a nonzero source operand, the percentage is `100 × abs(source − workbench) / abs(source)`, stored half-up to four decimal places. Compare the absolute variance to the inclusive tolerance. At zero tolerance, any count or amount difference breaks even if rounding would display zero. Zero versus zero has 0.0000 and passes. Zero source versus nonzero Workbench breaks at zero tolerance. Pending: stored percentage and nonzero-tolerance behavior for zero-source/nonzero-Workbench and numeric overflow, owner data architect with the data steward, tracked as NEW-GAP-S2B-06. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR7 | A BREAK raises MSG-P1-012 and the Reconciliation break alert for the data steward. Route through E1011-OPS values (RD-P1-028/044). Pending: alert destination and REC-02 balance wording/placeholder units in MSG-P1-012, owner observability owner with the Error and Message Standard owner, tracked as NEW-GAP-S2B-08. Pending: effect on the rwb-case list, owner solution architect with the data lead, tracked as NEW-GAP-X3. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR8 | Apply the rwb-case entry exclusions to the compared populations via the contract in section 12.2. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR9 | E1015 starts the child after the ALS stamp on COMPLETED. A gate HOLD, unreadable allocation or unreadable parameter causes no result write. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR10 | LOV-REC-RESULT is PASS or BREAK. A check that cannot proceed writes no result row. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR11 | Atomically replace dated aggregates keyed on `(rec_code, business_date, product_group)`. | RD-P1-022, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-042 |
| BR12 | The reconciliation reads ACE for the business date of the ACE batch it was started by, and never a mix of two business dates | BR-P1-011-2 |
| BR13 | A REC-05 orphan never deletes or changes a Workbench record or an ACE row; it is listed for the data steward and, where the row is missing in ACE, for the ACE team | BR-P1-011-3 |

Pending: ACE product-category aliases and unmapped or null category handling, owner data steward with the data architect, tracked as NEW-GAP-S2B-05. Never silently discard an account or treat a partial population as fully reconciled.

### 9. State transitions

| From | Condition | Outcome |
|---|---|---|
| No execution for date | E1015 commits the ALS stamp | Starts reconciliation child |
| Open | Allocation confirmed or readable at deadline | Runs checks |
| Open | Inputs read and all checks complete | Commits the result set; any BREAK raises MSG-P1-012 and the alert |
| Open | Input unavailable after retries | Fails execution; preserves prior rows |
| Failed | Eligible restart | Repeats the checks for the same date |

AD018 projects PENDING, RUNNING, WAITING, COMPLETE and FAILED when released (RD-P1-012/020). The retired P1 case-list publish state is removed.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| `rwb_source_data`, the service login | Reads its views and tables and writes the reconciliation aggregates |
| RW-DATASTEW, data steward and data product owner | Reads results with Platform administration R and scope applied |
| RW-PLATADM, platform administrator | Reads results and reruns a failed JOB-04 run through AD018 with Platform administration U after wave 4 |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read results and break rows (Platform administration R) |
| RW-TEAMMGR and other report readers | Read the rwb-reporting projection through Reporting R |

**Authorise check.** Use rwb-access `POST /authorise` for Platform administration action R and applicable scope on both reads. AD018 checks U on its rerun. Daily data-steward sign-off is outside this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-010 | v_ace_account | product_category | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-020 | v_ace_account | total_balance | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-075 | v_ace_contact | contact_type | Read |
| DF-ACE-076 | v_ace_contact | contact_key | Read |
| DF-ACE-187 | v_ace_valuation | valuation_key | Read |
| DF-CAS-026 | case_account | account_key | Read through the rwb-case key contract (NEW-GAP-B2) |
| DF-CAS-032 | case_party | person_key | Read through the rwb-case key contract (NEW-GAP-B2) |
| DF-CAS-057 | case_entry_exclusion | account_key | Read through the case query contract |
| DF-CAS-058 | case_entry_exclusion | business_date | Read through the case query contract |
| DF-INT-003 | interaction | person_key | Read (REC-05) |
| DF-INT-022 | interaction | contact_key | Read (REC-05) |
| DF-EXT-001 | party_ext | person_key | Read (REC-05) |
| DF-EXT-013 | contact_point_ext | contact_key | Read (REC-05) |
| DF-EXT-014 | contact_point_ext | contact_type | Read (REC-05) |
| DF-EXT-027 | account_ext | account_key | Read (REC-05) |
| DF-EXT-036 | valuation_ext | valuation_key | Read (REC-05) |
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

**Data ownership.** P1 reads ACE through its views and its own tables by business key. Dated rwb-case allocations, open account and party keys, balances and exclusions arrive through the rwb-case contract in section 12.2. Section B deployment follows RD-P1-043. The P1 dictionary baseline stays at 123 objects and 1,379 fields, including retired dictionary entries (RD-P1-025, X-21).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Success | Errors |
|---|---|---|---|
| GET | `/admin/reconciliation/results` | 200, result page filtered by `recCode`, `product`, `result`, `from`, `to` | 400, 401, 403, 422, 503 |
| GET | `/admin/reconciliation/results/{resultId}` | 200, aggregate result with detail subject to the storage contract | 400, 401, 403, 404, 503 |

API-P1-003 uses base `/api/recovery/source-data/v1`. Both reads require Platform administration R with scope applied. `resultId` is the UUID from DF-OPS-118. Aggregate codes are REC-01 and REC-02, `product` uses LOV-PRODUCT and `result` uses LOV-REC-RESULT (PASS, BREAK). Dates are ISO dates on `business_date`. Pending: publish result-specific page envelope, sort, page and date defaults and limits, owner P1 contract owner, tracked as NEW-GAP-S2B-02.

Invalid date or UUID syntax answers 400 MSG-GEN-001, unsupported list values answer 400 MSG-GEN-007, and `from` later than `to` answers 422 MSG-GEN-003. Missing credentials answer 401 MSG-P4-001, refused scope or right answers 403 MSG-P4-002, a missing UUID answers 404 MSG-P4-003, and an unavailable result store answers 503 MSG-GEN-006. Error responses use `application/problem+json` (RD-P1-004). Required members are `type`, `title`, `status`, `messageCode` and `traceId` (W3C 32-hex). Optional members are `detail`, `instance`, `messageTh`, `field` and `errors`. The `errors` array contains `{field, messageCode, detail}` entries only for 400 or 422 with multiple failing inputs. GET carries neither Idempotency-Key nor If-Match (RD-P1-001/006).

RWB-P1-AD018-CON alone publishes `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` (RD-P1-012/020/024). The rerun becomes available at AD018 wave 4. A repeated readiness call starts no second reconciliation run: while `AceIngestCheck` runs it attaches (USE_EXISTING), and once the `business_day_readiness` row is DONE or LATE it starts nothing, so a second `ReconciliationWorkflow` run of a date exists only through the rerun of a FAILED run (RD-P1-065). Pending: how a failed run is recovered before wave 4, given that NEW-ASM-X4 also names a repeated readiness call and the fallback poll, owner solution architect, tracked as NEW-GAP-G1-1. JOB-04 is the reconciliation job type. The rerun uses the prior failed run UUID, derives date and type from that run, requires Platform administration U and a canonical UUID Idempotency-Key, and takes no body. Success is 202 with the new Job in PENDING and runNo incremented, with FAIL and ALLOW_DUPLICATE_FAILED_ONLY. An open or non-FAILED run answers 409 MSG-P1-011, an incomplete ACE batch answers 409 MSG-P1-001 and an unknown run answers 404 MSG-P4-003. A missing or malformed key answers 400 MSG-PLT-N009-03, a matching key, endpoint and digest replays the stored answer for 24 h, conflict or in-flight reuse answers 409 MSG-PLT-N009-05, and an unavailable key store answers 503 MSG-PLT-N009-06. A caller without the right answers 403 MSG-P4-002.

#### 12.2 REST operations consumed

- Pending: paged rwb-case open-case key read for the business date (including case-account and case-party keys), owner rwb-case service owner, tracked as NEW-GAP-B2.
- Pending: rwb-case allocation status and exclusion operations, including paths, payloads, paging and provider fakes, owner rwb-case service owner, tracked as GAP-0337 and NEW-GAP-S2B-01. The contract also needs to define the dated open-case balances and eligible account set for REC-02.
- RWB-P3-E1042-CON `GET /api/recovery/case/v1/parameters/{key}` supplies `case.entry.dpd`, `recon.tolerance.pct` and `caselist.allocation.wait.until`.
- RWB-P3-E1043-CON supplies LOV-PRODUCT and LOV-REC-RESULT.
- Each call is one hop with a 2 s caller timeout.

#### 12.3 Events published

The DP-03 library appends the decision record and publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (RD-P1-008). E1015 owns `rwb.source-data.AceDataReady.v1` and `rwb.source-data.AceDataLate.v1` on `rwb.source-data.events.v1` (RD-P1-003).

#### 12.4 Events consumed

None. `ReconciliationWorkflow` is started as a child of E1015's `AceIngestCheck` after the ALS stamp. `AceDataReady` is owned and published by RWB-P1-E1015-APP and RWB-P1-E1015-CON (RD-P1-022, RD-P1-024).

#### 12.5 Workflows and activities

`ReconciliationWorkflow` (`recon-{businessDate}`) registers one activity, `reconciliation`, on task queue `rwb-source-data` in namespace `rwb-recovery` (contract jar major 1). The child input is `{businessDate, startedBy}`. E1015 starts it with parent close policy ABANDON in the workflow task that commits the ALS stamp (source status COMPLETED), using USE_EXISTING and ALLOW_DUPLICATE. Before REC-01, use durable timers to poll the rwb-case allocation answer every `recon.allocation.poll.minutes` (5 in the values file, NEW-ASM-X2). Proceed at ALLOCATION_COMPLETE YES or the `caselist.allocation.wait.until` limit (07:15 Asia/Bangkok, rwb-case parameter) when the contract is readable. An unreadable answer blocks the checks and produces no result rows (RD-P1-042).

The activity retry policy is initial interval 1 s, coefficient 2, maximum 10 attempts (Error Handling and Resilience Standard v5). Each remote call is one hop with a 2 s caller timeout and a breaker per downstream. Pending: activity start-to-close budget for the whole reconciliation, owner solution architect, tracked as NEW-GAP-S2B-04.

The workflow returns the summary with aggregate outcomes and the orphan count. The activity commits the date set only when the reads and checks finish.

#### 12.6 Schedules

None. E1015 `AceIngestCheck` starts this child workflow after the ALS stamp; E1011 registers no Schedule and no Kafka consumer (RD-P1-022, RD-P1-024).

#### 12.7 Tables owned

| Object | Owner | Use |
|---|---|---|
| `rwb_source_data.reconciliation_result` | RWB-P1-E1011-APP | Two aggregates per product and date, unique on `(rec_code, business_date, product_group)` |
| `interaction`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | P1 | Read for REC-05 |
| `data_product_load` | RWB-P1-E1015-APP | E1015 stamp, only read through its service boundary when needed |
| `job_run`, `job_run_check` | RWB-P1-AD018-APP | Job projection after AD018 release (RD-P1-020) |

Pending: durable break-detail store and locator for the detail response, including REC-05 orphans, owner P1 data architect with the contract owner, tracked as GAP-1508 and NEW-GAP-S2B-03. The existing aggregate schema is limited to REC-01 and REC-02. GAP-0575 and RD-P1-010 settle the candidate-read response. Do not create a legacy exception table or insert REC-05 into `reconciliation_result`.

#### 12.8 Contract fakes

| Provider | Fixtures |
|---|---|
| RWB-P1-E1011-CON | Pin reconciliation read contract and fake to 5.1.0. Aggregate and detail success fixtures plus each Problem listed in section 12.1; detail contents pending NEW-GAP-S2B-03 |
| rwb-case | Dated open cases, allocation, exclusions and 503/timeout; provider fake pending NEW-GAP-B2/NEW-GAP-S2B-01 |
| RWB-P3-E1042-CON | Tolerances 0.00 and 0.10, entry threshold 90 and allocation wait 07:15 |
| RWB-P3-E1043-CON | Four LOV-PRODUCT values and PASS/BREAK |
| RWB-P1-E1069-APP / RWB-P1-E1065-CON | ACE view fixture, dated ALS batch, mid-read error and Section B flag off |
| RWB-P1-AD018-CON | Job read and rerun fixtures once AD018 is released |

The fakes are test-only and are not deployed above SIT.

#### 12.9 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | Two result reads | rwb-case dated allocation/key/exclusion, parameter and LOV contracts, and authorise |
| Kafka | DP-03 library decision record | None |
| Temporal | One child and one activity | E1015 parent start; AD018 rerun after wave 4 |
| File | None | None |

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

DP-10 uses the E1015 child start and one registered activity. DP-17 removes lake extracts. DP-19 applies to the SCR-45 composite route that RWB-P3-AD019-APP delivers.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ReconciliationWorkflow` | Workflow | One run per business date; input, retry and run record |
| `reconciliation` | Activity | Three checks, variance, tolerance and atomic replacement of dated aggregates |
| `ReconciliationResult` | Entity | Maps `reconciliation_result`, one row per check and product group |
| `ReconciliationResultRepository` | Repository | Replaces one date's rows in one transaction; the query of 12.1 |
| `ReconciliationService` | Service | Counts, sums, variances and the PASS or BREAK decision against the tolerance |
| `ReferentialCheck` | Service | Checks the P1 and open-case key families in section 11 |

| `ReconciliationController` | Controller | The two read operations with RFC 9457 problem details |
| `LoadAlertNotifier` | Service | Raises MSG-P1-012 and the Reconciliation break alert on BREAK; reports MSG-GEN-006 on unavailable input |

**Database.** Keep the baseline aggregate schema and add `ix_reconciliation_date` on `(business_date, rec_code, product_group)`. The detail store is pending in section 12.7.

**Configuration and reference data.** Read the date-specific values and LOVs in section 12.2, including DL25 option A at 0.00 percent. Use the values file for the allocation poll interval. RWB-P3 owns parameter changes.

**Build steps**

1. Add the result repository and index and verify atomic replacement and retry behavior.
2. Implement the comparisons and orphan count with the dated inputs in section 4. Complete the dependencies and detail decision recorded in section 12.
3. Register the child workflow and activity and verify that completed runs write one decision record.
4. Serve the protected result reads and verify the error matrix.
5. Verify the AD018 job projection and failed-run rerun at the wave 4 boundary.

**Feature flag.** `rwb.source-data.daily-gate` (RD-P1-022). Result writes require the E1015 ALS stamp and Section B release gate.

**Done when.** Section 16 passes, a completed date holds eight REC-01/02 aggregates and the two reads match the published contract. AD018 verification occurs when the job operations are released.

### 14. Validation and messages

| ID | When | Placeholder or response |
|---|---|---|
| MSG-P1-012 | Count or balance BREAK | Error and Message Standard v6. `date` = business date, `product` = product group, `variance` = absolute account difference for REC-01, `pct` = stored percentage. REC-02 wording and units pending NEW-GAP-S2B-08 |
| MSG-P1-001 | E1015 ACE input not COMPLETED | `product` = affected data product display name, `date` = stamp in use. E1015 owns the message and the never-stamped fixture |
| MSG-GEN-006 | ACE, rwb-case or result store unavailable | `system` identifies ACE database, rwb-case or the P1 result store, as applicable |
| MSG-GEN-001 / MSG-GEN-007 / MSG-GEN-003 | Syntax, invalid LOV or reversed date range | 400 / 400 / 422 Problem respectively |
| MSG-P4-001 / MSG-P4-002 / MSG-P4-003 | Missing credentials, denied right/scope or missing result | 401 / 403 / 404 Problem respectively |

### 15. Screens and states

RWB-P3-AD019-APP delivers SCR-45 as the composite route through gateway-bff. RWB-P1-AD019-APP owns only the console behaviour over the P1 reads and the data-steward actions. Pending: SCR-45 empty, error and no-access presentation, owner UX lead, tracked as CG-ALL-2061. The API exposes PASS and BREAK for completed checks; an empty page has no items.

### 16. Test cases

| TC reference | Covers | Data |
|---|---|---|
| TC-E1-011-01, TC-E1-011-04, TC-E1-011-06, TC-E1-011-17, TC-P1-E1011-APP-08 | AC5, AC6, AC8, AC16, AC24 | Dated child start, overlapping start, restart after a corrected input and an ACE failure after the MORTGAGE count |
| TC-E1-011-02, TC-E1-011-12, TC-P1-E1011-APP-02, TC-P1-E1011-APP-03, TC-P1-E1011-APP-05, TC-P1-E1011-APP-06 | AC9, AC10, AC18, AC19, AC21, AC22 | All four product groups including UNSECURED, 2,903 versus 2,891 SSME accounts, 0.10 boundary, exclusion and balance-only break |
| TC-E1-011-13, TC-P1-E1011-APP-04, TC-P1-E1011-APP-11 | AC11, AC20, AC27 | Absent or incomplete ALS batch, unreadable rwb-case dependency, incomplete allocation at 07:15 |
| TC-E1-011-14, TC-E1-011-15, TC-P1-E1011-APP-10 | AC12, AC14, AC26 | P0099881 orphan, decision record and history inspection, REC-03/04 boundary |
| TC-E1-011-16, TC-P1-E1011-APP-01, TC-P1-E1011-APP-09 | AC13, AC15, AC25 | Both result reads, RW-CASEOWN without R, nonexistent UUID, malformed filters and unavailable store |
| TC-P1-E1011-APP-07 | AC23 | AD018 wave 4 failed JOB-04 run, canonical UUID key, replay, right refusal and incomplete ALS batch |

In Test Cases v9, TC-E1-011-01 to TC-E1-011-06 are rewritten for the criteria of this version and TC-E1-011-07 is retired. TC-E1-011-03 covers BR6, TC-E1-011-08 covers BR5 and BR13, and TC-E1-011-10 and TC-E1-011-11 cover the contract of section 12 and the tables of section 12.7.

### 17. Guardrails

- Read date-specific parameters and LOVs through their owner contracts.
- Keep names, account numbers and raw identifiers out of workflow history, decision records and logs. Any durable break-detail schema is subject to data-classification review.
- Only P1 reads `recovery.v_ace_*`. Use contract calls for rwb-case and do not join or add foreign keys across schemas.
- The workflow writes P1 results only and never changes ACE or case records.
- No lake, file extract or Power BI dataset is produced (DP-17).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Dated account counts and balances reconcile and business keys resolve against ACE | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | All recovery processes | REC-01, REC-02, REC-05, CTL-01 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-04, TC-E1-011-06, TC-E1-011-12 to TC-E1-011-17, TC-P1-E1011-APP-01 to TC-P1-E1011-APP-11 |
| REQ-RDF-008 | Report reconciliation breaks and referential completeness | Epic 1, 3.1 and 3.8 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-05, CTL-01 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-04, TC-E1-011-06, TC-E1-011-12 to TC-E1-011-17, TC-P1-E1011-APP-01 to TC-P1-E1011-APP-11 |
| REQ-CWC-004 | Excluded accounts are explained and do not count as breaks | Epic 1, 3.1 | FEAT-RDF-11 | 6.1 | BR8 | TC-E1-011-01, TC-E1-011-02, TC-E1-011-04, TC-E1-011-06, TC-E1-011-12 to TC-E1-011-17, TC-P1-E1011-APP-01 to TC-P1-E1011-APP-11 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1011-CON | Contract | H build dependency: the result resource, the two read operations and the workflow and activity contract |
| RWB-P1-E1011-OPS | DevOps | Child worker deployment and reconciliation alert |
| RWB-P1-E1015-CON | Contract | Parent ingest and readiness contract |
| RWB-P1-AD018-CON | Contract | Job operations and rerun from wave 4 |
| RWB-P1-E1015-APP, RWB-P1-E1069-APP | App development | H build dependency: the parent ingest check and the views |
| RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P6-E1011-APP | App development | Siblings of the legacy key over their own tables. RWB-P3-E1011-APP runs no open-case key check of its own and serves only the key-list read (GAP-3273); REC-05 is owned here (RD-P1-069) |
| RWB-ITG-E1011-ITG | Integration | Proves AC1 to AC4 and AC7 end to end across the services |

### 19. Out of scope

- REC-03 (approved treatments not booked): owned by the treatment slices with `recon.treatment.days`. REC-04 (payments unmatched to proceeds, `recon.payment.days`) and REC-06: computed by the rwb-payment daily reconciliation (RWB-P8-E4050-APP). This service computes REC-01, REC-02 and REC-05 only (RD-P1-069).
- Other services’ business-key checks beyond the open-case keys in section 11 are owned by their own slices.
- The two lake extracts, the Power BI data set and the 07:30 refresh: removed with the data lake (DP-17; GAP-0495).
- The contract documents, the fakes as published artefacts and the naming of the result elements: RWB-P1-E1011-CON.
- Deployment and alerts belong to RWB-P1-E1011-OPS. The job API and rerun belong to AD018.
- Working a break to closure and data-steward daily sign-off are outside this slice (FEAT-RPT-09 full scope, Epic 2). P3 owns the case list.
- Write-off, asset, decision-log and notice-barcode checks are outside this slice (Data Quality and Reconciliation Rules v4).
- The data quality console SCR-45 and the quality measure definitions (Epic 2 and Epic 8).
- Pending: disposition of DEF-015 for the retired legacy exception table, owner quality lead. D-RCV-60 withdrew the table this defect refers to.


### Remaining delivery steps

- Size: pending refinement; owner squad.
- Epic design sign-off: pending; owner product owner.
- Contract marked Done and published: pending; owner contract owner.
- Fake published: pending; owner contract owner.
- Test data loaded in DEV: pending; owner data engineer.

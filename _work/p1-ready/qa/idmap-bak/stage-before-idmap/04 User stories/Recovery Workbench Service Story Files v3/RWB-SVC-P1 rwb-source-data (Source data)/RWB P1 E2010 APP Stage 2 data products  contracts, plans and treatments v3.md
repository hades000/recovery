# RWB-P1-E2010-APP Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2010-APP |
| Work type | APP (App development) |
| Document version | v3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P1-E2010-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| Depends on (build) | RWB-P1-E2010-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1069-APP, RWB-P1-E1015-APP, RWB-P1-E1016-CON |
| Contract dependencies | RWB-P3-E1043-CON; rwb-treatment (`/api/recovery/treatment/v1`, GET `/treatments` and GET `/treatments/active-count`, faked; ASM-4458, CDC-03577); rwb-guarantee claim read (GAP-2738; the wave 2 fake answers an empty list, GAP-2739); rwb-case case-existence and reference-data reads (GAP-0509; DP-07) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7, provided); rwb-treatment.yaml 5.1.0 (API Specification v7, consumed; it does not yet publish the two reads of section 12.2, CDC-03577) |
| Integration dependencies | None |
| External dependencies | RWB-P1-E2010-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030, FR-P1-031) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-012, RD-P1-023, RD-P1-040, RD-P1-041, RD-P1-043, RD-P1-044, RD-P1-065, RD-P1-069 |

**Version 3 changes.**

- Corrected treatment ownership and reads to rwb-treatment (RWB-P1-E2010-APP#1).
- `Stage2ProductWorkflow` is a child of `AceIngestCheck` after the ALS stamp and consumes no event; only a FAILED run is rerun, and a refused rerun answers 409 MSG-P1-011 (RD-P1-002, RD-P1-012, RD-P1-040).
- Wave 2 guarantee fixture, retry policy and case UUIDs stated (RWB-P1-E2010-APP#2 and #3; RD-P1-023).
- Snapshot replacement scope, count population, DP04 stamp writer and the guarantee-error end state are pending: NEW-GAP-S11-1 to NEW-GAP-S11-5 (RWB-P1-E2010-APP#2, #4 and #5).
- Readiness decisions: RD-P1-002, RD-P1-004, RD-P1-005, RD-P1-012, RD-P1-023, RD-P1-040, RD-P1-041, RD-P1-043, RD-P1-044.
- RD-P1-065 and RD-P1-069: only a FAILED run is rerun (platform rule); the store and read of the break list stay pending under GAP-1508 and tests assert counts. AC15 cites its Test Cases v9 row.


**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for rwb-source-data. The stage 2 step leaves `DailyCaseRun` in rwb-case and becomes `Stage2ProductWorkflow` on this service's own task queue, started by this service's own `rwb.source-data.AceDataReady.v1` (DP-10); the dated DP04 copies of treatments and guarantee claims are written in `rwb_source_data` and the contract and plan facts stay in the `recovery.v_ace_*` views, read live and never copied (DP-01, DP-05); the treatment entity is consumed as a contract with a fake and the DP04 record read is declared by the contract story of this legacy key, while the deployment moves to RWB-P1-E2010-OPS. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: version 3 applies the listed RD-P1 rulings and review corrections.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P1-E2010-APP-L416, X20 RWB-P1-E2010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the stage 2 product build to run as `Stage2ProductWorkflow` on task queue `rwb-source-data`, a child of `AceIngestCheck` after the ALS stamp, writing the dated DP04 copies of treatments and guarantee claims into `rwb_source_data` and reading the contract number, contract date and plan terms live from `recovery.v_ace_account` and `recovery.v_ace_plan`, with the link check, the active-count check, the freshness stamp and the DP04 record read that the Epic 3 screens use**, so that **the settlement, restructure and deed-in-lieu screens read one checked place, nothing is copied out of ACE, and the stage 2 step of the daily run belongs to the service that owns the data products**.

This is the application slice of legacy RWB-E2-010. It owns:

- all eight legacy acceptance criteria of the story, copied verbatim with their origin tag, and the business rules, messages and data rows they depend on;
- `Stage2ProductWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, its window, its case link check, its count check and its call to the freshness stamp, with the four activities `readDp04SourcePage(businessDate, page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04` (DP-10; Architecture v5 slide 15, "Workflow: AceIngestCheck, reconciliation"; activity names per RD-P1-002);
- the writer of `dp_treatment` and `dp_guarantee_claim` in schema `rwb_source_data`, keyed by record ID and business date, plus the `data_product_load` row of DP04 written through the freshness story (DP-01, DP-15), and it never reads this copy as the source of a treatment (GAP-1716);
- the DP04 branch of `GET /data-products/{productCode}/records` on base `/api/recovery/source-data/v1`, which returns the snapshot rows with the contract and plan facts read live (DP-13).

It does not own: the published shape of that operation, which is declared by RWB-P1-E2010-CON and shares the components of RWB-P1-E1016-CON; the access and catalog contract, which is RWB-P1-E1016-CON; the freshness stamp writer, which is RWB-P1-E1015-APP; the ACE view SQL and the read path, which are RWB-P1-E1069-APP; the treatment record and treatment reads belong to rwb-treatment; case existence remains with rwb-case; the guarantee claim record, which is rwb-guarantee's (S3); and the chart, the dashboards and the alerts, which are RWB-P1-E2010-OPS.

### 2. Business rationale

From Epic 3 the settlement, restructure and deed-in-lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place. In the target the live treatment record stays with rwb-treatment and the guarantee record with rwb-guarantee, and the dated DP04 copies stay with P1 as the data engine, built from the live facts and read-only for reporting (Ownership Map ruling on `treatment`, `dp_treatment` and `dp_guarantee_claim`; ASM-0080). DP04 therefore still has two kinds of content: the Workbench snapshot of treatments and claims, stamped for the business date and owned by this service, and the ACE facts — contract number, contract date and plan terms — read from `recovery.v_ace_account` and `recovery.v_ace_plan` at request time. No table copies a contract, a plan or an account (DP-01, DP-05).

What D-RCV-60 changes is where the step runs and how it is started and reached. The legacy step was an in-process stage of `rwb-case`'s JOB-02 chain over the one `recovery` schema. In the target the step is a workflow of rwb-source-data, the service that owns the data products and the freshness stamp, started by `AceIngestCheck` as a child workflow after the ALS stamp; the service does not consume its own `AceDataReady` event (DP-10; RD-P1-002, RD-P1-040). The consumers of the legacy snapshot tables become consumers of a published record read, one hop and 2 s timeout (DP-11), so the Epic 3 screens reach DP04 through gateway-bff and never through a table (DP-19).

Serves REQ-RDF-014 (stage 2 data products exist before the first treatment goes live) and REQ-RDF-010 (access per data product by role). No business value moves: the product code DP04, the owner role, the expected-by time and the access rows stay data rows held by the catalog and access stories of this service.

### 3. Preconditions

- RWB-P1-E2010-CON is published: the DP04 branch of the record read, the record shapes `DataProductRecordPage`, `DataProductRecord` and `FieldValue`, the error envelope and the fakes are baselined and handed to this story.
- RWB-P1-E1069-APP is done: `recovery.v_ace_account` and `recovery.v_ace_plan` are readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege in `public` (DP-02, DP-05).
- RWB-P1-E1016-CON is published and RWB-P1-E1015-APP is done: the access check per data product and the freshness stamp with its `data_product_load` writer exist, so the DP04 access row and the DP04 stamp are read and written through them and not re-implemented here.
- RWB-P1-E1015-APP is done: `AceIngestCheck` starts `Stage2ProductWorkflow` as its child (ParentClosePolicy ABANDON) in the workflow task that commits the ALS stamp, and `data_product` holds DP04 Treatment and offers with its owner role, refresh cycle and `expected_by` (08:00 for a daily product under DL11; RD-P1-041 closes GAP-0511).
- The consumer correction is to rwb-treatment (ASM-4458; CDC-03577): GET `/api/recovery/treatment/v1/treatments` and GET `/api/recovery/treatment/v1/treatments/active-count`, one hop and 2 s timeout (DP-11). rwb-treatment.yaml 5.1.0 does not yet publish either read; publication is tracked by CDC-03577.
- The guarantee claim read of rwb-guarantee (S3) is available as a published contract with its fake, and returns no claim until S3 is built in wave 3; the contract is a C dependency the Work Package does not list (GAP-0509; ASM-0701).
- RWB-PLT-E1071-CON (workflow kit), RWB-PLT-E1044-CON (per-service Flyway sequence), RWB-PLT-E1043-CON with RWB-P3-E1043-CON (reference data: the status lists) and RWB-PLT-N001-CON (gateway-bff composite route) are in place.
- The per-service Flyway sequence of rwb-source-data is at the version that carries `dp_treatment`, `dp_guarantee_claim` and `data_product_load`; this story adds the two snapshot tables on the same sequence and never edits an applied migration (DP-15).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P1-E2010-CON when its tests pass.

### 4. Flow

1. `AceIngestCheck` (RWB-P1-E1015-APP) commits the ALS stamp for business date D from a COMPLETED ACE batch (RD-P1-040, RD-P1-041). With the Section B flag off it writes no stamp and starts no child (RD-P1-043).
2. In the same workflow task `AceIngestCheck` starts `Stage2ProductWorkflow` as a child (ParentClosePolicy ABANDON) with workflow ID `stage2-dp04-{businessDate}` (system start: conflict policy USE_EXISTING, reuse policy ALLOW_DUPLICATE). The run is not started by consuming this service's Kafka event (RD-P1-002, RD-P1-040).
3. `readDp04SourcePage(businessDate, page)` activity: asks the rwb-treatment contract for treatments created or changed in the window [start of D, start of D+1), page by page, one hop and 2 s, and asks the guarantee contract of rwb-guarantee for the claims changed in the same window.
4. `writeDp04Page` activity: resolves the case of every row to confirm it exists, holds on the break list any row whose case does not resolve, and upserts the other rows into `dp_treatment` and `dp_guarantee_claim` in schema `rwb_source_data`, keyed by record ID and business date, one transaction per page. The claim read answers every claim in the window with its `case_id` and does not itself resolve the case; the References check, the break list and the retry stay with this writer step (GAP-2740).
5. `checkActiveCount` activity: compares the count of active treatments written for D with the active count answered by the treatment contract; a difference writes no DP04 stamp and lists the break for the data steward (MSG-P1-002). Pending: which rows make the two counts comparable when an active treatment did not change in the window of D, and which states are active, owner solution architect, tracked as NEW-GAP-S11-2 and GAP-2696.
6. `stampDp04` activity: on a match, calls the freshness stamp of RWB-P1-E1015-APP for DP04 and business date D, so the row in `data_product_load` is written by its owner and not by this story. Pending: how this call relates to the stamp `AceIngestCheck` writes for DP04 when its source batch completes (RD-P1-041 item 3 against the activity list of RD-P1-002), owner solution architect, tracked as NEW-GAP-S11-3.
7. Case owner, restructuring officer, guarantee officer or credit approver: reads DP04 for a case through the DP04 branch of `GET /data-products/{productCode}/records?caseId=`; the response joins the snapshot rows to `recovery.v_ace_account` and `recovery.v_ace_plan` for the contract number, contract date and plan terms, which are read at request time and never written.
8. Data steward: reads the DP04 catalog entry and the breaks (Pending: the store and read of break detail, owner P1 data architect with the P1 contract owner, tracked as GAP-1508 and NEW-GAP-S2B-03; until then tests assert counts, RD-P1-069); the catalog entry names the system of record of each part and never a copied ACE column.
9. Only a FAILED run of D is rerun, through `POST /admin/jobs/{jobId}/rerun` of RWB-P1-AD018-CON (header `Idempotency-Key`; conflict policy FAIL, reuse policy ALLOW_DUPLICATE_FAILED_ONLY); it upserts by record ID and business date, publishes nothing and never duplicates a row. A COMPLETE run is not run again (RD-P1-065). Pending: how a FAILED run is restarted before RWB-P1-AD018 is released in wave 4, owner solution architect, tracked as NEW-GAP-S11-5.

Each activity retries with a 1 s initial interval, back-off 2 and 10 attempts (Temporal Workflow and Activity Catalog v3); when the attempts are used up the workflow ends FAILED. Pending: start-to-close timeout and heartbeat interval (GAP-0143) and the non-retryable error types (NEW-GAP-W5-002). Deployment values, thresholds and timings are named chart values per environment in RWB-P1-E2010-OPS; the test-data fixture owner is Not specified in the source documents (GAP-0513) and is named at the wave 2 entry check.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without a DP04 access row reads the product | 403; the refusal is logged by the access check of this service | MSG-P4-002 | AC3 |
| X2 | A guarantee claim names a case that does not exist | The claim is held on the break list with check References and retried with the next build; nothing is written | None | AC4 |
| X3 | The treatment contract is unavailable | The workflow ends FAILED for system Treatment; the previous DP04 rows and stamp stay; DP04 turns stale at its expected-by time through the freshness story | MSG-GEN-006, MSG-P1-001 | AC5 |
| X4 | A FAILED run of the same business date is rerun, or `writeDp04Page` is retried | Rows are upserted by record ID and business date; no duplicate row and no event | None | AC6, AC14 |
| X5 | The active treatment counts differ | DP04 is not stamped for D and the break is listed for the data steward | MSG-P1-002 | AC7 |
| X6 | A treatment changed at the end of business date D | It is inside the window of D; a change one second after the window goes to D+1 | None | AC8 |
| X7 | The guarantee contract answers with an error or is not deployed yet | The claim part of the page is held on the break list and the treatment part is written; the run record names the guarantee break. End state and DP04 stamp: Pending (NEW-GAP-S11-4) | MSG-GEN-006, MSG-P1-002 | AC9, AC12 |
| X8 | A rerun is asked while a run of D is PENDING or RUNNING, or the run is not FAILED | 409; no new execution starts | MSG-P1-011 | AC10 |

X1 to X6 are the exception paths of RWB-E2-010 carried onto the split. X7 is the path the guarantee contract of S3 adds while its own service is not yet built (GAP-0509; ASM-0701), and X8 is the rerun guard of RD-P1-012.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published DP04 record read, the treatment contract and the guarantee contract with their fakes, on the tables and views of the other P1 stories; needs no live rwb-treatment or rwb-guarantee to start |
| Negotiable | The activity names, the page size and the workflow ID derivation are this story's choice; the window, the link check, the count check and the stamp rule are fixed |
| Valuable | The Epic 3 settlement, restructure and deed-in-lieu screens read one checked place, owned by the service that publishes the data products |
| Estimable | One workflow, four activities, two repositories, one record-read controller branch and one count check |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, claims and ACE rows through stub contracts, plus one component test of the record read |

### 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments

  Background:
    Given business date 2026-12-14 and the ACE batch for ALS for it is COMPLETED at 06:20
    Given the rwb-treatment returns 40 active treatments, 12 of them restructure plans with installments published in v_ace_plan
    Given 9 of the 12 plans carry a credit approval recorded on the case by the restructuring officer

  Scenario: AC1 Products loaded (legacy RWB-E2-010 AC1)
    Given treatments and plans in the case store, with credit approvals recorded from NLEADS by the officer
    When `AceIngestCheck` commits the ALS stamp for 2026-12-14 and starts `Stage2ProductWorkflow` (RD-P1-040)
    Then dp_treatment holds 40 rows for business date 2026-12-14, each with treatment type, approval level, installments, outcome and its case
    Then the DP04 read for any of the 40 cases shows the contract number and contract date of its primary account from v_ace_account and the plan terms from v_ace_plan
    Then DP04 carries a freshness stamp for business date 2026-12-14 with status "LOADED"
    Then the catalog entry for DP04 lists system of record "Workbench" for treatment and guarantee claim and names v_ace_account and v_ace_plan for the contract and plan facts

  Scenario: AC2 Guarantee data (legacy RWB-E2-010 AC2)
    Given 5 TCG guarantee claim records for 5 existing cases, claimed amounts from 180,000.00 to 1,250,000.00 baht
    When the stage 2 step runs
    Then dp_guarantee_claim holds 5 rows, each linked to its case
    Then a read of DP04 for case "00000000-0000-0000-0000-000000000512" (case number RW-2026-000512) returns its TCG claim with claim deadline 2027-02-28

  Scenario: AC3 Access (legacy RWB-E2-010 AC3)
    Given the rwb-source-data access contract mock returns a refused answer for role "RW-PHONECOL" on product "DP04"
    Given user "u-phone-02" holds RW-PHONECOL, which has no DP04 access row
    When the user calls GET /data-products/DP04/records?caseId=00000000-0000-0000-0000-000000000512
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system logs the refusal with user "u-phone-02" and product "DP04"

  Scenario: AC4 A guarantee claim for a case that does not exist (legacy RWB-E2-010 AC4)
    Given the rwb-case contract mock returns no case for case ID "00000000-0000-0000-0000-000000000997"
    Given a TCG claim names case ID "00000000-0000-0000-0000-000000000997"
    When the stage 2 step runs
    Then the system does not write the claim to dp_guarantee_claim
    Then the data quality break list holds it with product "DP04" and check "References"

  Scenario: AC5 The treatment interface is unavailable (legacy RWB-E2-010 AC5)
    Given the rwb-treatment contract fake returns an error
    When the stage 2 step runs for 2026-12-14
    Then the step ends "FAILED" with MSG-GEN-006 for system "Treatment"
    Then no DP04 stamp is written for 2026-12-14 and the dp_treatment rows of 2026-12-13 are unchanged
    Then at the `data_product.expected_by` time of DP04 the freshness query reports DP04 STALE with MSG-P1-001 (RD-P1-041; NEW-GAP-S11-3)

  Scenario: AC6 A repeat run for the same date (legacy RWB-E2-010 AC6; TC-E2-010-06)
    Given the stage 2 run for 2026-12-14 ended FAILED after writeDp04Page committed 40 treatment rows
    When the FAILED run is rerun through POST /admin/jobs/{jobId}/rerun and reads the same 40 treatments
    Then dp_treatment holds 40 rows for 2026-12-14 and one row per treatment ID
    Then no event is published
    # Pending: removal of a row whose ID is absent from the rerun answer, owner solution architect, NEW-GAP-S11-1
    # Pending: running a COMPLETE run of a date again, owner solution architect, NEW-GAP-F05-2

  Scenario: AC7 Active treatment counts differ (legacy RWB-E2-010 AC7; TC-E2-010-07)
    Given writeDp04Page wrote 40 active treatment rows for 2026-12-14
    Given the active-count read of rwb-treatment answers 41
    When the count check runs
    Then the system does not stamp DP04 for 2026-12-14
    Then a break with check "Active treatment count 40 against 41" is listed for the data steward with MSG-P1-002
    # Pending: comparable population for unchanged active treatments, owner solution architect, NEW-GAP-S11-2

  Scenario: AC8 A change at the end of the business date (legacy RWB-E2-010 AC8)
    Given treatment "TRT-SYN-0601" changed at 2026-12-14T23:59:59+07:00 and treatment "TRT-SYN-0602" changed at 2026-12-15T00:00:00+07:00
    When the stage 2 step runs for 2026-12-14
    Then "TRT-SYN-0601" is in the build for 2026-12-14
    Then "TRT-SYN-0602" is not

  Scenario: AC9 The guarantee contract is unavailable (exception X7) (new, D-RCV-60; TC-E2-010-12)
    Given the guarantee contract mock returns an error
    Given the treatment contract answers for business date 2026-12-14
    When the stage 2 step runs for 2026-12-14
    Then dp_treatment holds the treatment rows for 2026-12-14 and dp_guarantee_claim holds no row for 2026-12-14
    Then the claim part of the page is held on the data quality break list
    Then the run record names the guarantee contract with MSG-GEN-006 and MSG-P1-002
    # Pending: workflow end state and DP04 stamp, owner solution architect, NEW-GAP-S11-4

  Scenario: AC10 A rerun is requested while the workflow of the date is running (exception X8) (new, D-RCV-60; TC-E2-010-13)
    Given the stage 2 run for 2026-12-14 is RUNNING
    Given the caller holds the job rerun right of RWB-P1-AD018-CON
    When POST /admin/jobs/{jobId}/rerun is called with that run ID and an Idempotency-Key
    Then the system answers 409 with MSG-P1-011
    Then no new execution starts and the running execution "stage2-dp04-2026-12-14" is unchanged
    Then the same call for a run with status COMPLETE answers 409 with MSG-P1-011

  Scenario: AC11 Error answers of the provided operations (401 and 404) (new, D-RCV-60)
    Given the rwb-case contract mock returns no case for case ID "00000000-0000-0000-0000-000000000997"
    When the user calls GET /data-products/DP04/records?caseId=00000000-0000-0000-0000-000000000512 without credentials
    Then the system answers with status 401 and MSG-P4-001
    When the user calls GET /data-products/DP04/records?caseId=00000000-0000-0000-0000-000000000997 with valid credentials
    Then the system answers with status 404 and MSG-P4-003

  Scenario: AC12 The guarantee contract is not deployed yet (exception X7) (new, D-RCV-60; TC-E2-010-15)
    Given the guarantee contract is not deployed yet in this environment
    Given the treatment contract answers for business date 2026-12-14
    When the stage 2 step runs for 2026-12-14
    Then dp_treatment holds the treatment rows for 2026-12-14 and dp_guarantee_claim holds no row for 2026-12-14
    Then the claim part of the page is held on the data quality break list
    Then the run record names the guarantee contract with MSG-GEN-006 and MSG-P1-002
    # Pending: workflow end state and DP04 stamp, owner solution architect, NEW-GAP-S11-4

  Scenario: AC13 Empty wave 2 guarantee result (new, D-RCV-60; TC-P1-E2010-APP-01)
    Given the wave 2 guarantee fake returns an empty page
    Given the treatment contract returns 40 treatments and its active count equals the active rows written
    When the stage 2 run for 2026-12-14 completes
    Then dp_guarantee_claim holds no row for 2026-12-14 and no guarantee break is listed
    Then the workflow ends COMPLETED and stampDp04 stamps DP04 for 2026-12-14 as LOADED; the empty guarantee part is not stale (GAP-2739)

  Scenario: AC14 A later page fails (new, D-RCV-60; TC-P1-E2010-APP-02)
    Given page 1 of the 2026-12-14 snapshot is committed and page 2 fails on all 10 activity attempts
    When the workflow ends
    Then the run is FAILED, no active-count break is listed and no DP04 stamp is written for 2026-12-14
    Then a rerun of the FAILED run holds one row per record ID for 2026-12-14
    # Pending: visibility and removal of the page 1 rows, owner solution architect, NEW-GAP-S11-1

  Scenario: AC15 The flag is off (new, D-RCV-60; TC-P1-E2010-APP-03)
    Given the flag "rwb.dataengine.stage2-products" is off
    When AceIngestCheck commits the ALS stamp for 2026-12-14
    Then no Stage2ProductWorkflow execution starts
    Then dp_treatment and dp_guarantee_claim are unchanged
```

**Target reading.** Every assertion above keeps its legacy wording; what changes is where it runs, who produces the fact and how it is reached. The stage 2 step of JOB-02 is no longer a step of `rwb-case`'s `DailyCaseRun`: in the target it is `Stage2ProductWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, a child of `AceIngestCheck` after the ALS stamp (DP-10; RD-P1-002, RD-P1-040). The workflow writes `dp_treatment` and `dp_guarantee_claim` in schema `rwb_source_data` (DP-01; ownership ruling: the dated DP04 copies are P1's, built from the live facts of S2 and S3 and read-only for reporting; ASM-0080). The contract number, contract date and plan terms of AC1 are read live from `recovery.v_ace_account` and `recovery.v_ace_plan` through this service's own ACE read contract and are never copied (DP-05). The treatment facts of AC1, AC2, AC5, AC7 and AC8 come through the treatment read contract of `rwb-treatment` (C), reached one hop with a 2 s timeout and faked, the changed-window and active-count operations are those in section 12.2; the treatment read error in AC5 is the error answer of its fake. The guarantee claim facts of AC2 and AC4 come through the guarantee contract of rwb-guarantee, which the Work Package does not list as a C dependency (GAP-0509; ASM-0701); `GuaranteeClaimQuery` of the legacy lines is that contract's changed-window read, and the case-not-found check of AC4 is the case-existence answer of rwb-case's case contract, faked with the same gap and assumption. The DP04 access check of AC3 is this service's own `RWB-P1-E1016-CON` (H), and the freshness stamp of AC1 returns through RWB-P1-E1015-APP (H) as a `DataProductFreshness` record of the record read. The DP04 read of AC1, AC2, AC3 and AC4 is the DP04 branch of `GET /data-products/{productCode}/records`, whose shape is declared by `RWB-P1-E2010-CON` and which shares the components of `RWB-P1-E1016-CON`, so `GET /data-products/DP04/records?caseId=` of the legacy line is that operation on base `/api/recovery/source-data/v1` with `productCode` DP04. The per-service Flyway sequence of this service carries the two snapshot tables (DP-15), reference data supplies the status lists (DP-07), and every screen reaches the read through gateway-bff (DP-19). The legacy case number in a query is replaced by the case UUID, with the case number kept as display data (RD-P1-023); AC6 reruns a FAILED run only (RD-P1-012).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | DP04 holds treatments and guarantee claims from the Workbench, and contract and plan facts read from v_ace_account and v_ace_plan, with one system of record and one owner for each part | REQ-RDF-014; data_product DP04; sys_objects |
| BR2 | No Workbench table copies a contract, a plan or an account; the views are read at request time | D-RCV-35 U1; tier map section 9 |
| BR3 | Every snapshot row links to an existing case, or it is held on the break list and retried with the next build | DQ load check "References" |
| BR4 | The product is stamped for the day only when the active count matches the owning module, with zero tolerance | DL25; RWB-E1-011 hold rule (FEAT-RDF-13) |
| BR5 | A role reads DP04 only through an access row in force | data_product_access; REQ-RDF-010 |
| BR6 | Credit approval for a restructure is recorded on the case by the officer; there is no interface to NLEADS | INT-26; DL12 |
| BR7 | Plan installments come from the ACE plan published calculation | DF-ACE-174 source ACE; INT-34 |

**Where each rule lives in the target.** BR1 and BR2 are this story's: the two snapshot tables hold the Workbench facts. Physical Schema v9 declares `dp_treatment.contract_no` and `contract_date` (DF-TRT-050, DF-TRT-051); this story never writes them and the DP04 read never answers from them, because the contract and plan facts are read from the views at request time (DP-01, DP-05). Pending: removal of the two columns, owner data architect, tracked as NEW-GAP-S11-6. The views themselves and the 30-view read path are RWB-P1-E1069-APP's, and this story reads them in-process and copies nothing. BR3 is the link check of `writeDp04Page`; the break list is this service's own data quality record. BR4 is the `checkActiveCount` activity and its hold; the tolerance and the expected-by time are data rows of `data_product` and decisions, never constants (DP-07). BR5 is served by the access check of RWB-P1-E1016-CON on the record read, so AC3 asserts the published answer and not a local guard. BR6 and BR7 are unchanged business facts: the approval is recorded on the case by the officer, and the installments come from the ACE plan through `recovery.v_ace_plan`.

### 9. State transitions

No case status changes: the story changes the DP04 freshness status (LOADED or STALE) through the stamp owner, and the state of the `Stage2ProductWorkflow` execution of a business date (RUNNING, COMPLETED or FAILED).

| From | Event | Condition | To |
|---|---|---|---|
| `AceIngestCheck` running for ALS date D | ALS stamp commits | `rwb.dataengine.stage2-products` is on | Child `Stage2ProductWorkflow` RUNNING as `stage2-dp04-{businessDate}` (RD-P1-002, RD-P1-040) |
| RUNNING | treatments and claims written | The link check and the count check pass | COMPLETED and DP04 stamped for D |
| RUNNING | count difference | The two active counts differ | DP04 not stamped, break listed |
| RUNNING | treatment contract error | All 10 attempts fail | FAILED, DP04 not stamped |
| RUNNING | guarantee contract error | The claim read cannot complete | End state Pending (NEW-GAP-S11-4) |
| FAILED | `POST /admin/jobs/{jobId}/rerun` | No run of D is PENDING or RUNNING | RUNNING again, rows upserted by record ID (RD-P1-012) |
| COMPLETED | the ALS stamp of D+1 commits | A treatment changed on D+1 | A new execution for D+1; nothing is rewritten for D |

The freshness states LOADED and STALE are the stamp owner's and are read here; the rows of `dp_treatment` and `dp_guarantee_claim` have no state machine of their own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow, the four activities, the two repositories, the count check and the DP04 branch of the record read |
| RW-DATASTEW, data steward | Owns DP04; reads the catalog entry and the breaks; confirms the system of record of each part |
| RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD | Read DP04 for cases in scope, through the access row in force |
| RW-COE, RW-AUDIT | Read DP04 for all cases |
| RW-PHONECOL and roles with no DP04 access row | May not read DP04 |
| rwb-treatment (S2) | Owns the treatment record and treatment reads consumed by this story |
| rwb-guarantee (S3) | Owns the guarantee claim record and answers its contract; returns no claim until its own wave |
| The platform workflow owner | Owns the `rwb-source-data` task queue, the namespace and the worker registration this workflow runs on |
| No approval level from the delegation of authority applies | The story takes no business decision; it builds a data product |

No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry business dates, record IDs, codes and counts only.

Every DP04 operation is authorised by the rwb-access authorise check (DP-08), called through RWB-P1-E1016-CON against the access row in data_product_access (section 12.7); this story calls the check and does not reimplement it.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Read |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-010 | treatment | valid_until | Read |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-012 | treatment | booked_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| DF-TRT-015 | guarantee_claim | id | Read |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Read |
| DF-TRT-022 | guarantee_claim | status | Read |
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-006 | v_ace_account | contract_no | Read |
| DF-ACE-007 | v_ace_account | contract_date | Read |
| DF-ACE-160 | v_ace_plan | plan_ref | Read |
| DF-ACE-174 | v_ace_plan | installments | Read |
| DF-ACE-175 | v_ace_plan | recommended_installment | Read |
| DF-ACE-168 | v_ace_plan | booked_at | Read |
| DF-TRT-034 to DF-TRT-049 | dp_treatment | all fields; DF-TRT-050 and DF-TRT-051 are not written (NEW-GAP-S11-6) | Write |
| DF-TRT-052 to DF-TRT-061 | dp_guarantee_claim | all fields | Write |
| DF-OPS-001 to DF-OPS-009 | data_product_load | all fields | Write |

treatment fields are read through the rwb-treatment contract and guarantee_claim fields through the rwb-guarantee contract, not from their tables; the guarantee contract is outside the C dependencies of the plan (GAP-0509; ASM-0701). `recovery.v_ace_account` and `recovery.v_ace_plan` are read through this service's own ACE read contract and never copied. `data_product_load` is written by the freshness story on this story's call and not by a writer of its own (RWB-P1-E1015-APP). Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). This story supplies the DP04 branch of one operation whose shape is declared by RWB-P1-E2010-CON and shares the components of RWB-P1-E1016-CON; the branches of the other 13 data products belong to their own stories.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/data-products/{productCode}/records` (the DP04 branch) | `DataProductRecordPage` with `items` of `DataProductRecord` (`recordId`, `entity`, `fields` of `FieldValue`), `freshness` of `DataProductFreshness`, `page`, `size`, `total`; `productCode` DP04; query `caseId`, `page`, `size` | Case record R plus a DP04 access row in force, through the access check of RWB-P1-E1016-CON | Idempotent by product, case and page |

`caseId` is a required UUID, `page` defaults to 0 and `size` to 50 with a maximum of 200 (RD-P1-005). Errors use the Problem body (RD-P1-004): 400, 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003 and 503 MSG-GEN-006; the full status and message mapping is in RWB-P1-E2010-CON. The DP04 rows carry the snapshot fields of section 11 and the contract and plan facts read live from the two views; the record and page property names are those of `DataProductRecordPage`, `DataProductRecord` and `FieldValue` in rwb-source-data.yaml 5.1.0 (API Specification v7).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | `/treatments?changedFrom=&changedTo=&page=&size=` and `/treatments/active-count` on `/api/recovery/treatment/v1` | S2 rwb-treatment (`rwb-treatment.yaml`); treatment ownership and publication per ASM-4458 / CDC-03577; operation shapes per GAP-2696 | Treatment changed-window page and active count; maximum page size 1000, 400 on an empty window; active-state values Pending under GAP-2696; faked | DP-11; one hop, 2 s timeout |
| GET | `/api/recovery/guarantee/v1/guarantee-claims?changedFrom=&changedTo=&page=&size=` | S3 rwb-guarantee | Page has `items`, `window`, `page`, `size` and scope-filtered `total`; order `updated_at`, then `id`; max-size value and error-to-message mapping Pending under GAP-2738; empty-list and error fake (CDC-03545, CDC-03580) | DP-11; one hop, 2 s timeout |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (case contract) | The case-existence answer of the link check; faked and test-only, since the case reference arrives on each treatment row | DP-11; one hop, 2 s timeout |
| GET | `/api/recovery/case/v1/reference-data/{tableCode}` with its version | P3 rwb-case | Reads the three required reference-data lists (DP-07) | DP-07; one hop, 2 s timeout |
| (interface) | `AceSourceReadRepository` over `recovery.v_ace_account` and `recovery.v_ace_plan` | P1 rwb-source-data (`RWB-P1-E1069-APP`) | The contract number, contract date and plan terms, read at request time and never written | DP-05; in-process in this service, published to others as the ACE read contract |

The guarantee operation follows the accepted target path; its maximum-size value and error mapping remain Pending under GAP-2738. The wave 2 fake returns an empty list, so the guarantee portion stays empty rather than stale (GAP-2739; R-22449). The case-existence and reference-data operations are consumed through rwb-case; ACE facts are read in this service's own views (DP-01, DP-05).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP. This story publishes no event and writes no outbox row of its own.

#### 12.4 Events consumed

None. `Stage2ProductWorkflow` is a Temporal child started by `AceIngestCheck` after the ALS stamp; this story consumes no Kafka topic (RD-P1-040).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `Stage2ProductWorkflow` | Child workflow of `AceIngestCheck`, one run per business date, workflow ID `stage2-dp04-{businessDate}` | `rwb-source-data` in namespace `rwb-recovery` | Input: business date; started in the workflow task that commits the ALS stamp, ParentClosePolicy ABANDON; run record with the outcome and the break references |
| `readDp04SourcePage(businessDate, page)` | Activity | `rwb-source-data` | The window [start of D, start of D+1); page number and size in; the treatment and claim rows of the page out |
| `writeDp04Page` | Activity | `rwb-source-data` | The rows of one page; the link check, the break path and one transaction per page that upserts by record ID and business date |
| `checkActiveCount` | Activity | `rwb-source-data` | The active count of the contract and the count written for D; a match or a break with the check text |
| `stampDp04` | Activity | `rwb-source-data` | The business date and product DP04; a call to the freshness stamp of RWB-P1-E1015-APP on a match |

System starts use conflict policy USE_EXISTING and reuse policy ALLOW_DUPLICATE; an admin rerun applies only to a FAILED run, with conflict policy FAIL and reuse policy ALLOW_DUPLICATE_FAILED_ONLY, and a refused rerun answers 409 MSG-P1-011 (RD-P1-012, RD-P1-040). Activity retry: 1 s initial interval, back-off 2, 10 attempts; timeouts and heartbeat Pending (GAP-0143).

#### 12.6 Schedules

None. The workflow is started by `AceIngestCheck` and owns no Temporal Schedule and no legacy Quartz job; the 05:30 Schedule and the freshness timers belong to RWB-P1-E1015-APP (DP-10; RD-P1-040).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `dp_treatment` | `rwb_source_data` | P1 | Created by this story's Flyway version and written by `writeDp04Page`, keyed by record ID and business date; holds no `contract_no` and no `contract_date` column |
| `dp_guarantee_claim` | `rwb_source_data` | P1 | Created by the same version and written by `writeDp04Page`, keyed by record ID and business date |
| `data_product_load` | `rwb_source_data` | P1 | Not written directly: the DP04 row is written by the freshness stamp on this story's call (RWB-P1-E1015-APP) |
| `data_product`, `data_product_access` | `rwb_source_data` | P1 | Read for the expected-by time, the owner role and the access row; no row is written here |

No table of another service is read and no foreign key crosses a schema (DP-01). The treatment and guarantee tables of S2 and S3 are never named in SQL; their facts arrive through their contracts.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-treatment contract fake | The changed-window read and the active count | 40 active treatments and 12 plans with 9 approvals; a contract error; an active count of 41 against 40 rows; a treatment changed at 23:59:59 and one at 00:00:00 |
| rwb-guarantee guarantee claim fake | The changed-window claim read | 5 TCG claims for existing cases; one claim for case ID "00000000-0000-0000-0000-000000000997"; an empty list until S3 is built; a contract error |
| RWB-P1-E1016-CON access fake | The DP04 access answer | A granted answer for the DP04 reading roles; a refused answer for RW-PHONECOL on DP04 |
| rwb-case case-existence fake | The link check of AC4 | The known cases of the fixture; no case for "00000000-0000-0000-0000-000000000997" |
| ACE account and plan fixture | `recovery.v_ace_account` and `recovery.v_ace_plan` | Rows for the 40 accounts of the fixture with `contract_no`, `contract_date`, `plan_ref`, `installments`, `recommended_installment` and `booked_at`; an account with no plan |

The treatment, guarantee and access fakes are the published contracts of those stories; the ACE fixture stands in for the views of RWB-P1-E1069-APP; and the case-existence fake is the test-only answer of rwb-case's case contract, recorded with GAP-0509 and ASM-0701.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation branch on `/api/recovery/source-data/v1` | Five reads: treatment window, active count, guarantee claim, case existence, reference data; the access check through RWB-P1-E1016-CON | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | None | No topic is consumed or published (RD-P1-040, RD-P1-044) |
| Temporal | `Stage2ProductWorkflow` and 4 activities on `rwb-source-data` | None | Namespace `rwb-recovery`; no Schedule |
| File | None | None | No file is read or written |
| SQL view | None | `recovery.v_ace_account` and `recovery.v_ace_plan` | SELECT only, in-process, never copied (DP-05) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, modules `stage2` and `read`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule, event-started or child workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is the pattern this story is built on: the stage 2 step becomes a child workflow of `AceIngestCheck` in this service. DP-01 and DP-05 are the ownership ruling and the live read of the ACE facts; DP-11 is the treatment and guarantee contracts with their fakes; DP-15 carries the two snapshot tables on the service sequence; DP-07 supplies the status lists; DP-13 and DP-19 fix the base and the screen path.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `Stage2ProductWorkflow` | Workflow | One execution per business date; the window, the page loop, the link check, the count check and the stamp call |
| `readDp04SourcePage(businessDate, page)` | Activity | The changed-window reads of the treatment and guarantee contracts, page by page |
| `writeDp04Page` | Activity | The link check, the break path and the upsert of `dp_treatment` and `dp_guarantee_claim` |
| `checkActiveCount` | Activity | The active-count comparison and its hold |
| `stampDp04` | Activity | The call to the freshness stamp of RWB-P1-E1015-APP |
| `DpTreatmentRepository`, `DpGuaranteeClaimRepository` | Repository | Upsert by record ID and business date, in schema `rwb_source_data` |
| `Dp04ReadService` | Service | The DP04 branch of the record read: the snapshot rows joined to the contract and plan facts, masked by the access answer |
| `Migrations` | Migration | The two snapshot tables on the per-service Flyway sequence, without a contract column |

**Database.** `dp_treatment` and `dp_guarantee_claim` hold the Workbench snapshot per business date. The legacy story dropped `dp_treatment.contract_no` and `dp_treatment.contract_date` because a contract is read from `v_ace_account` and never copied; in the target those columns are never created (BR2). No table holds a plan, a contract or an account row. The `data_product_load` row of DP04 is written through RWB-P1-E1015-APP.

**Configuration and reference data.** The DP04 row in `data_product` carries the owner role, the refresh cycle and `expected_by` 08:00 (DL11; ASM-0703; RD-P1-041). The DP04 access rows are the data steward's and are read through RWB-P1-E1016-CON. The status lists arrive as reference data (DP-07).

**Build steps**

1. The Flyway version with `dp_treatment` and `dp_guarantee_claim`, their keys on record ID and business date, and no contract column (DP-15).
2. `Stage2ProductWorkflow` and its input record, registered on `rwb-source-data`, with workflow ID `stage2-dp04-{businessDate}` and the child start in `AceIngestCheck` (AC1, AC6, AC15).
3. `readDp04SourcePage(businessDate, page)` against the treatment and guarantee fakes, with the window [start of D, start of D+1) (AC1, AC2, AC8).
4. `writeDp04Page` with the link check, the References break and the upsert per page (AC4, AC6).
5. `checkActiveCount` and the hold of the stamp on a difference (AC7).
6. `stampDp04` through the freshness story, and the FAILED path of a contract error with the previous rows kept (AC5).
7. `Dp04ReadService` and the DP04 branch of the record read, with the live view read, the access answer and the freshness record (AC1, AC3).
8. Tests for AC1 to AC15 against the fakes and the ACE fixture.

**Feature flag.** `rwb.dataengine.stage2-products`.

**Done when.** The tests in section 16 pass, the workflow starts as a child of `AceIngestCheck` over a synthetic ALS batch in SIT, `dp_treatment` and `dp_guarantee_claim` hold the rows of the business date, the DP04 stamp is LOADED on a count match and absent on a difference, the DP04 read answers with the live contract and plan facts, and the DP04 catalog entry shows in `GET /admin/data-products` in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | Role without a DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | DP04 stale after a failed step | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Count check break held the publish | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | A treatment, guarantee claim or other downstream read cannot complete | {system} is not available. Try again in a few minutes. |
| MSG-P1-011 | Rerun refused (409): the run is not FAILED, or a run of the date is PENDING or RUNNING | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-001 | No valid session or no Workbench role (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-003 | The case is outside the caller's scope (404) | This case is not in your scope. |

Texts are those of Error and Message Standard v6. MSG-P1-001 and MSG-P1-002 are raised by the freshness story and read here, MSG-GEN-006 names the system of the failed contract, and MSG-P4-002 is the access answer of RWB-P1-E1016-CON. Thai text follows decision DL10.

### 15. Screens and states

SCR-45 Data quality (Epic 2): state Loading while the list arrives; state Breaks shows the DP04 References breaks and the active-count break for the data steward. Pending: the published read of the stage 2 break list, owner solution architect, tracked as NEW-GAP-F05-1. Its empty, error and no access states are Not specified in the source documents (CG-ALL-2410). The case record view SCR-03 shows the DP04 data for roles with an access row in force. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2409). The settlement, restructure and deed-in-lieu screens that read DP04 come in Epic 3. Every one of them reaches this service through the gateway-bff composite route, which calls rwb-case and rwb-source-data in parallel, one hop each (DP-19); the screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E2010-APP-04 | AC1, BR1, BR2, BR6, BR7 | End to end | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-P1-E2010-APP-05 | AC2, BR1 | End to end | 5 TCG claims for existing cases |
| TC-P1-E2010-APP-06 | AC3, BR5 | End to end | RW-PHONECOL reads DP04 |
| TC-P1-E2010-APP-07 | AC4, BR3 | End to end | TCG claim for an unknown case ID |
| TC-P1-E2010-APP-08 | AC5 | End to end | The treatment contract fake returning errors |
| TC-P1-E2010-APP-09 | AC6 | End to end | Step run twice for 2026-12-14 |
| TC-P1-E2010-APP-10 | AC7, BR4 | End to end | The active count 41 against 40 rows |
| TC-P1-E2010-APP-11 | AC8 | End to end | Changes at 23:59:59 and 00:00:00 |
| TC-P1-E2010-APP-12 | Access, BR5 | Component | RW-TRIBE calls the DP04 read with no DP04 access row; refused with MSG-P4-002 |
| TC-E2-010-10 | Section 12 operations, events and activities | Contract | The contract shapes of section 12 checked against the published contract |
| TC-E2-010-11 | Section 12.7 tables (ASM-3438) | Component | Rows at the boundary of each table of section 12.7 |
| TC-E2-010-12 | AC9 | End to end | The guarantee contract fake returning an error for 2026-12-14 |
| TC-E2-010-13 | AC10 | End to end | Rerun requested while the 2026-12-14 execution runs |
| TC-E2-010-14 | AC11 | Contract | Call without credentials; unknown case ID 00000000-0000-0000-0000-000000000997 |
| TC-E2-010-15 | AC12 | End to end | The guarantee contract not deployed for 2026-12-14 |
| TC-P1-E2010-APP-01 | AC13 | Component | Empty guarantee page with matching active counts |
| TC-P1-E2010-APP-02 | AC14 | Component | Page 2 fails after page 1 is committed |
| TC-P1-E2010-APP-03 | AC15 | Component | Flag off at the ALS stamp |

The nine legacy test case IDs are kept in order and their Covers and Data are carried onto the split; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. Where the legacy Covers names `Access`, the criterion is the published access answer of RWB-P1-E1016-CON on the DP04 read. The treatment and guarantee fakes of section 12.8 stand behind every case, and the ACE account and plan fixture replaces the views. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID; Test Cases v9 holds the rows of AC1 to AC15 as worded in this version. The `-ITG` copies of these cases belong to RWB-ITG-E2010-ITG and are not listed here.

### 17. Guardrails

- No business value in code: the product code DP04, the owner role, the expected-by time and the access rows are data rows of `data_product`, `data_product_access` and the reference data, never constants (DP-07).
- No personal data in logs, events, workflow inputs or the fixture: the rows carry record IDs, case IDs, codes, dates and amounts only; test data is synthetic.
- No copy of ACE data: the contract number, contract date and plan terms are read from `recovery.v_ace_account` and `recovery.v_ace_plan` at request time, and the two snapshot tables hold no contract column (DP-01, DP-05).
- No read of another service's table: the treatment facts arrive through `rwb-treatment.yaml` and the claim facts through the guarantee contract, both with a fake (DP-11).
- ACE data only through the owner's contract or the `v_ace_*` views, and only this service names the views (DP-05).
- The workflow loads no business value from a source outside the contracts: every fact of a row is either the contract's or the view's, and the job runs from the freshness event rather than a fixed clock (DP-10).
- An applied migration is never edited: a correction to a snapshot table is a new version on the service sequence (DP-15).
- No call to NLEADS or the Thai Credit Guarantee Corporation: their results arrive as facts recorded on the case and on the claim (BR6).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-P1-E2010-APP-04 to TC-P1-E2010-APP-11 |
| REQ-RDF-010 | Access per data product by role; personal data masked by role under PDPA | Business Requirements Epic 2, section 3.1 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DP-07 | TC-P1-E2010-APP-06, TC-P1-E2010-APP-12 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E2010-CON | Contract | H: declares the DP04 branch of the record read, its shapes, its envelope and its fakes |
| RWB-P1-E2010-OPS | DevOps | X: deploys the workflow, the trigger, the flag, the dashboards and the alerts of this build |
| RWB-P1-E1016-CON | Contract | H: the access check per data product and the catalog entry the DP04 read answers with |
| RWB-P1-E1015-APP | App development | H: the freshness stamp this story calls and the LOADED and STALE states it reads |
| RWB-P1-E1069-APP | App development | H: the `recovery.v_ace_*` views and the ACE read path this story reads in-process |
| rwb-treatment.yaml | Contract | C: the treatment entity contract, faked |
| RWB-P3-E1043-CON | Contract | C: the reference data that supplies the status lists, with RWB-PLT-E1043-CON |
| S3 rwb-guarantee claim contract | Contract | C, outside the Work Package's C list: the guarantee claim read, faked (GAP-0509; ASM-0701); in wave 2 the DP04 guarantee part stays empty rather than stale until the live claim read lands (GAP-2739) |
| RWB-ITG-E2010-ITG | Integration | I: the cross-service proof of the same legacy key against the live owners |

Open decisions carried by this story: DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL12 (ASM-0189, ASM-2559, ASM-2608); DL25 (ASM-0728, ASM-0735, ASM-0743, ASM-2602). Each decision is still open and is built on its assumption.

### 19. Out of scope

- The published shape of the DP04 record, its envelope and its fakes: RWB-P1-E2010-CON.
- The chart, the worker registration, the trigger proof, the flag, the dashboards, the alerts and the runbook: RWB-P1-E2010-OPS.
- The treatment record and treatment reads: rwb-treatment. The case-existence check and credit approval record remain with rwb-case.
- The guarantee claim record, its filing and its deadline timers: rwb-guarantee (S3, wave 3), consumed here as a contract with a fake.
- The freshness stamp, its stale flag, its timers and `AceIngestCheck`: RWB-P1-E1015-APP; the access check and the catalog entry: RWB-P1-E1016-CON and its DB story.
- The ACE view SQL, the grants and the boundary rule: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- Settlement, restructure and deed-in-lieu screens: Epic 3; the gateway-bff composite route and the screen field list: the platform edge story and the screen owners (DP-19).
- DP04 integration harness (GAP-0392): the integration lead and the QA lead agree the composite DP04 route path and merge order with the platform edge story, and the harness environment, seed pack, evidence format, retention and pass or fail gate, at the wave 2 entry check; the result is recorded in the DP04 harness pack before the first real-service run.
- The real cross-service proof of the treatment and guarantee reads against the live services: RWB-ITG-E2010-ITG.
- The expected-by time of DP04, which is the 08:00 of DL11 held in `data_product.expected_by` (ASM-0703; RD-P1-041).

### 20. Remaining delivery steps

- Size: Not specified; owner recovery squad.
- Epic design sign-off: Pending; owner product owner.
- RWB-P1-E2010-CON Done and fake publication: Pending; owner rwb-source-data contract owner.
- Synthetic test data in DEV: Pending; owner QA lead.
- Snapshot replacement scope, deletion and atomicity: Pending; owner solution architect, tracked as NEW-GAP-S11-1.
- Active-count population: Pending; owner solution architect, tracked as NEW-GAP-S11-2.
- Writer and timing of the DP04 stamp: Pending; owner solution architect, tracked as NEW-GAP-S11-3.
- End state and stamp when the guarantee read fails: Pending; owner solution architect, tracked as NEW-GAP-S11-4.
- Restart of a FAILED run before RWB-P1-AD018 is released: Pending; owner solution architect, tracked as NEW-GAP-S11-5.
- Store and read of the break list: Pending; owner P1 data architect with the P1 contract owner, tracked as GAP-1508 and NEW-GAP-S2B-03.
- Removal of the two contract columns of `dp_treatment`: Pending; owner data architect, tracked as NEW-GAP-S11-6.
- Publication of the two treatment reads in rwb-treatment.yaml: Pending; owner rwb-treatment service owner (CDC-03577).
- Guarantee read publication in rwb-guarantee.yaml, maximum size and error mapping: Pending; owner rwb-guarantee service owner, tracked as GAP-2738.

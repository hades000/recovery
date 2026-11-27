# RWB-P1-E2010-APP Stage 2 data products: contracts, plans and treatments

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-A |
| Ready to start | After RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| Depends on (build) | RWB-P1-E2010-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P1-E1069-APP, RWB-P1-E1015-APP, RWB-P1-E1016-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E2004-CON |
| Integration dependencies | None |
| External dependencies | RWB-P1-E2010-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-006, FR-P1-024, FR-P1-025, FR-P1-030, FR-P1-031) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for rwb-source-data. The stage 2 step leaves `DailyCaseRun` in rwb-case and becomes `Stage2ProductWorkflow` on this service's own task queue, started by this service's own `rwb.source-data.AceDataReady.v1` (DP-10); the dated DP04 copies of treatments and guarantee claims are written in `rwb_source_data` and the contract and plan facts stay in the `recovery.v_ace_*` views, read live and never copied (DP-01, DP-05); the treatment entity is consumed as a contract with a fake and the DP04 record read is declared by the contract story of this legacy key, while the deployment moves to RWB-P1-E2010-OPS. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P1-E2010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the stage 2 product build to run as `Stage2ProductWorkflow` on task queue `rwb-source-data`, started by this service's own `rwb.source-data.AceDataReady.v1`, writing the dated DP04 copies of treatments and guarantee claims into `rwb_source_data` and reading the contract number, contract date and plan terms live from `recovery.v_ace_account` and `recovery.v_ace_plan`, with the link check, the active-count check, the freshness stamp and the DP04 record read that the Epic 3 screens use**, so that **the settlement, restructure and deed-in-lieu screens read one checked place, nothing is copied out of ACE, and the stage 2 step of the daily run belongs to the service that owns the data products**.

This is the application slice of legacy RWB-E2-010. It owns:

- all eight legacy acceptance criteria of the story, copied verbatim with their origin tag, and the business rules, messages and data rows they depend on;
- `Stage2ProductWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, its window, its case link check, its count check and its call to the freshness stamp, with the four activities `snapshot(page)`, `writeDp04Page`, `checkActiveCount` and `stampDp04` (DP-10; Architecture v5 slide 15, "Workflow: AceIngestCheck, reconciliation" and the `snapshot(page)` activity);
- the writer of `dp_treatment` and `dp_guarantee_claim` in schema `rwb_source_data`, keyed by record ID and business date, plus the `data_product_load` row of DP04 written through the freshness story (DP-01, DP-15);
- the DP04 branch of `GET /data-products/{productCode}/records` on base `/api/recovery/source-data/v1`, which returns the snapshot rows with the contract and plan facts read live (DP-13).

It does not own: the published shape of that operation, which is declared by RWB-P1-E2010-CON and shares the components of RWB-P1-E1016-CON; the access and catalog contract, which is RWB-P1-E1016-CON; the freshness stamp writer, which is RWB-P1-E1015-APP; the ACE view SQL and the read path, which are RWB-P1-E1069-APP; the treatment entity and its plan timers, which are rwb-case's under RWB-P3-E2004-CON; the guarantee claim record, which is rwb-guarantee's (S3); and the chart, the dashboards and the alerts, which are RWB-P1-E2010-OPS.

### 2. Business rationale

From Epic 3 the settlement, restructure and deed-in-lieu screens need each case's treatments, plan terms, loan contracts and guarantee claims in one checked place. In the target the live treatment and guarantee records stay with S2 and S3, and the dated DP04 copies stay with P1 as the data engine, built from the live facts and read-only for reporting (Ownership Map ruling on `treatment`, `dp_treatment` and `dp_guarantee_claim`; ASM-0080). DP04 therefore still has two kinds of content: the Workbench snapshot of treatments and claims, stamped for the business date and owned by this service, and the ACE facts — contract number, contract date and plan terms — read from `recovery.v_ace_account` and `recovery.v_ace_plan` at request time. No table copies a contract, a plan or an account (DP-01, DP-05).

What D-RCV-60 changes is where the step runs and how it is started and reached. The legacy step was an in-process stage of `rwb-case`'s JOB-02 chain over the one `recovery` schema. In the target the step is a workflow of rwb-source-data, the service that owns the data products and the freshness stamp, started by the `AceDataReady` event this service already publishes (DP-10; Architecture v5 slides 15 and 44: JOB-02 starts from AceDataReady and JOB-04 reconciliation belongs to rwb-source-data). The consumers of the legacy snapshot tables become consumers of a published record read, one hop and 2 s timeout (DP-11), so the Epic 3 screens reach DP04 through gateway-bff and never through a table (DP-19).

Serves REQ-RDF-014 (stage 2 data products exist before the first treatment goes live) and REQ-RDF-010 (access per data product by role). No business value moves: the product code DP04, the owner role, the expected-by time and the access rows stay data rows held by the catalog and access stories of this service.

### 3. Preconditions

- RWB-P1-E2010-CON is published: the DP04 branch of the record read, the record shapes `DataProductRecordPage`, `DataProductRecord` and `FieldValue`, the error envelope and the fakes are baselined and handed to this story.
- RWB-P1-E1069-APP is done: `recovery.v_ace_account` and `recovery.v_ace_plan` are readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege in `public` (DP-02, DP-05).
- RWB-P1-E1016-CON is published and RWB-P1-E1015-APP is done: the access check per data product and the freshness stamp with its `data_product_load` writer exist, so the DP04 access row and the DP04 stamp are read and written through them and not re-implemented here.
- RWB-P1-E1015-APP is done and `data_product` holds DP04 Treatment and offers with its owner role, its refresh cycle and its expected-by time; the expected-by time of DP04 is 08:00 as the legacy story assumed from DL11 (GAP-0511; ASM-0703), because no source document states the DP04 value.
- RWB-P3-E2004-CON is published with its fake: `GET /api/recovery/case/v1/cases/{caseId}/treatments` and the changed-window and active-count reads of the treatment entity of rwb-case, one hop and 2 s timeout (DP-11).
- The guarantee claim read of rwb-guarantee (S3) is available as a published contract with its fake, and returns no claim until S3 is built in wave 3; the contract is a C dependency the Work Package does not list (GAP-0509; ASM-0701).
- RWB-PLT-E1071-CON (workflow kit), RWB-PLT-E1044-CON (per-service Flyway sequence), RWB-PLT-E1043-CON with RWB-P3-E1043-CON (reference data: the status lists) and RWB-PLT-N001-CON (gateway-bff composite route) are in place.
- The per-service Flyway sequence of rwb-source-data is at the version that carries `dp_treatment`, `dp_guarantee_claim` and `data_product_load`; this story adds the two snapshot tables on the same sequence and never edits an applied migration (DP-15).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P1-E2010-CON when its tests pass.

### 4. Flow

1. rwb-source-data: the outbox publishes `rwb.source-data.AceDataReady.v1` for business date D once the freshness story has stamped the source products for D from a COMPLETE ACE batch (Architecture v5 slide 15; DP-09, DP-10).
2. The listener of this story starts `Stage2ProductWorkflow` on task queue `rwb-source-data` with the business date, the source system and the freshness summary; the workflow ID is derived from the business date and the source, so a redelivery starts no second run.
3. `snapshot(page)` activity: asks the treatment contract of rwb-case for the treatments created or changed in the window [start of D, start of D+1), page by page, one hop and 2 s, and asks the guarantee contract of rwb-guarantee for the claims changed in the same window.
4. `writeDp04Page` activity: resolves the case of every row to confirm it exists, holds on the break list any row whose case does not resolve, and upserts the other rows into `dp_treatment` and `dp_guarantee_claim` in schema `rwb_source_data`, keyed by record ID and business date, one transaction per page.
5. `checkActiveCount` activity: compares the count of active treatments written for D with the active count answered by the treatment contract; a difference holds the publish and lists the break for the data steward (MSG-P1-002).
6. `stampDp04` activity: on a match, calls the freshness stamp of RWB-P1-E1015-APP for DP04 and business date D, so the stamp row in `data_product_load` is written by its owner and not by this story.
7. Case owner, restructuring officer, guarantee officer or credit approver: reads DP04 for a case through the DP04 branch of `GET /data-products/{productCode}/records?caseId=`; the response joins the snapshot rows to `recovery.v_ace_account` and `recovery.v_ace_plan` for the contract number, contract date and plan terms, which are read at request time and never written.
8. Data steward: reads the DP04 catalog entry and the breaks; the catalog entry names the system of record of each part and never a copied ACE column.
9. A rerun of D replaces the snapshot rows by record ID, publishes nothing new and never duplicates a row.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without a DP04 access row reads the product | 403; the refusal is logged by the access check of this service | MSG-P4-002 | AC3 |
| X2 | A guarantee claim names a case that does not exist | The claim is held on the break list with check References and retried with the next build; nothing is written | None | AC4 |
| X3 | The treatment contract is unavailable | The workflow ends FAILED for system Treatment; the previous DP04 rows and stamp stay; DP04 turns stale at its expected-by time through the freshness story | MSG-GEN-006, MSG-P1-001 | AC5 |
| X4 | The workflow runs again for the same business date | Rows are replaced by record ID and business date; no duplicate row and no second event | None | AC6 |
| X5 | The active treatment counts differ | DP04 is not stamped for D and the break is listed for the data steward | MSG-P1-002 | AC7 |
| X6 | A treatment changed at the end of business date D | It is inside the window of D; a change one second after the window goes to D+1 | None | AC8 |
| X7 | The guarantee contract answers with an error or is not deployed yet | The claim part of the page is held on the break list, the treatment part is written, and the workflow ends with the guarantee break named | MSG-GEN-006, MSG-P1-002 | Section 12.2 |
| X8 | The rerun is asked while the workflow of D is running | The rerun is refused and the running execution is named | MSG-P2-006 | Section 12.5 |

X1 to X6 are the exception paths of RWB-E2-010 carried onto the split. X7 is the path the guarantee contract of S3 adds while its own service is not yet built (GAP-0509; ASM-0701), and X8 is the rerun guard of the workflow kit.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published DP04 record read, the treatment contract and the guarantee contract with their fakes, on the tables and views of the other P1 stories; needs no live rwb-case or rwb-guarantee to start |
| Negotiable | The activity names, the page size and the workflow ID derivation are this story's choice; the window, the link check, the count check and the stamp rule are fixed |
| Valuable | The Epic 3 settlement, restructure and deed-in-lieu screens read one checked place, owned by the service that publishes the data products |
| Estimable | One workflow, four activities, two repositories, one record-read controller branch and one count check |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, claims and ACE rows through stub contracts, plus one component test of the record read |

### 7. Acceptance criteria

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments

  Background:
    Given business date 2026-12-14 and the ACE batch for ALS for it is COMPLETE at 06:20
    Given the treatment module holds 40 active treatments, 12 of them restructure plans with installments published in v_ace_plan
    Given 9 of the 12 plans carry a credit approval recorded on the case by the restructuring officer

  Scenario: AC1 Products loaded (legacy RWB-E2-010 AC1)
    Given treatments and plans in the case store, with credit approvals recorded from NLEADS by the officer
    When the stage 2 step of JOB-02 runs
    Then dp_treatment holds 40 rows for business date 2026-12-14, each with treatment type, approval level, installments, outcome and its case
    Then the DP04 read for any of the 40 cases shows the contract number and contract date of its primary account from v_ace_account and the plan terms from v_ace_plan
    Then DP04 carries a freshness stamp for business date 2026-12-14 with status "LOADED"
    Then the catalog entry for DP04 lists system of record "Workbench" for treatment and guarantee claim and names v_ace_account and v_ace_plan for the contract and plan facts

  Scenario: AC2 Guarantee data (legacy RWB-E2-010 AC2)
    Given 5 TCG guarantee claim records for 5 existing cases, claimed amounts from 180,000.00 to 1,250,000.00 baht
    When the stage 2 step runs
    Then dp_guarantee_claim holds 5 rows, each linked to its case
    Then a read of DP04 for case "RW-2026-000512" returns its TCG claim with claim deadline 2027-02-28

  Scenario: AC3 Access (legacy RWB-E2-010 AC3)
    Given the rwb-source-data access contract mock returns a refused answer for role "RW-PHONECOL" on product "DP04"
    Given user "u-phone-02" holds RW-PHONECOL, which has no DP04 access row
    When the user calls GET /data-products/DP04/records?caseId=RW-2026-000512
    Then the system refuses the call with status 403 and MSG-P4-002
    Then the system logs the refusal with user "u-phone-02" and product "DP04"

  Scenario: AC4 A guarantee claim for a case that does not exist (legacy RWB-E2-010 AC4)
    Given the rwb-case contract mock returns no case for case ID "00000000-0000-0000-0000-000000000997"
    Given a TCG claim names case ID "00000000-0000-0000-0000-000000000997"
    When the stage 2 step runs
    Then the system does not write the claim to dp_guarantee_claim
    Then the data quality break list holds it with product "DP04" and check "References"

  Scenario: AC5 The treatment interface is unavailable (legacy RWB-E2-010 AC5)
    Given the treatment contract mock returns an error
    Given TreatmentQuery returns an error
    When the stage 2 step runs for 2026-12-14
    Then the step ends "FAILED" with MSG-GEN-006 for system "Treatment"
    Then dp_treatment keeps the rows for 2026-12-13
    Then the system flags at 08:00 DP04 stale with MSG-P1-001 "Treatment is from 2026-12-13. Today's load has not arrived."

  Scenario: AC6 A repeat run for the same date (legacy RWB-E2-010 AC6)
    Given the stage 2 step completed for 2026-12-14 with 40 treatment rows
    When it runs again for 2026-12-14
    Then dp_treatment still holds 40 rows for 2026-12-14

  Scenario: AC7 Active treatment counts differ (legacy RWB-E2-010 AC7)
    Given TreatmentQuery.countActive() returns 41 and the build produced 40 active rows
    When the count check runs
    Then the system does not stamp DP04 for 2026-12-14
    Then a break with check "Active treatment count 40 against 41" is listed for the data steward with MSG-P1-002

  Scenario: AC8 A change at the end of the business date (legacy RWB-E2-010 AC8)
    Given treatment "TRT-SYN-0601" changed at 2026-12-14T23:59:59+07:00 and treatment "TRT-SYN-0602" changed at 2026-12-15T00:00:00+07:00
    When the stage 2 step runs for 2026-12-14
    Then "TRT-SYN-0601" is in the build for 2026-12-14
    Then "TRT-SYN-0602" is not
```

**Target reading.** Every assertion above keeps its legacy wording; what changes is where it runs, who produces the fact and how it is reached. The stage 2 step of JOB-02 is no longer a step of `rwb-case`'s `DailyCaseRun`: in the target it is `Stage2ProductWorkflow` on task queue `rwb-source-data` in namespace `rwb-recovery`, started by this service's own `rwb.source-data.AceDataReady.v1` (DP-10; Architecture v5 slide 15, "Workflow: AceIngestCheck, reconciliation" and the `snapshot(page)` activity). The workflow writes `dp_treatment` and `dp_guarantee_claim` in schema `rwb_source_data` (DP-01; ownership ruling: the dated DP04 copies are P1's, built from the live facts of S2 and S3 and read-only for reporting; ASM-0080). The contract number, contract date and plan terms of AC1 are read live from `recovery.v_ace_account` and `recovery.v_ace_plan` through this service's own ACE read contract and are never copied (DP-05). The treatment facts of AC1, AC2, AC5, AC7 and AC8 come through the treatment entity contract `RWB-P3-E2004-CON` (C), reached one hop with a 2 s timeout and faked, so `TreatmentQuery` and `TreatmentQuery.countActive()` in the legacy lines are the changed-window read and the active-count read of that contract, and `TreatmentQuery returns an error` in AC5 is the error answer of its fake. The guarantee claim facts of AC2 and AC4 come through the guarantee contract of rwb-guarantee, which the Work Package does not list as a C dependency (GAP-0509; ASM-0701); `GuaranteeClaimQuery` of the legacy lines is that contract's changed-window read, and the case-not-found check of AC4 is the case-existence answer of rwb-case's case contract, faked with the same gap and assumption. The DP04 access check of AC3 is this service's own `RWB-P1-E1016-CON` (H), and the freshness stamp of AC1 returns through RWB-P1-E1015-APP (H) as a `DataProductFreshness` record of the record read. The DP04 read of AC1, AC2, AC3 and AC4 is the DP04 branch of `GET /data-products/{productCode}/records`, whose shape is declared by `RWB-P1-E2010-CON` and which shares the components of `RWB-P1-E1016-CON`, so `GET /data-products/DP04/records?caseId=` of the legacy line is that operation on base `/api/recovery/source-data/v1` with `productCode` DP04. The per-service Flyway sequence of this service carries the two snapshot tables (DP-15), reference data supplies the status lists (DP-07), and every screen reaches the read through gateway-bff (DP-19). No legacy line is dropped or reworded; the three mock Givens above are the only added lines, and each names the contract its block consumes.

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

**Where each rule lives in the target.** BR1 and BR2 are this story's: the two snapshot tables hold the Workbench facts and no `contract_no` or `contract_date` column exists, because the contract and plan facts are read from the views at request time (DP-01, DP-05). The views themselves and the 30-view read path are RWB-P1-E1069-APP's, and this story reads them in-process and copies nothing. BR3 is the link check of `writeDp04Page`; the break list is this service's own data quality record. BR4 is the `checkActiveCount` activity and its hold; the tolerance and the expected-by time are data rows of `data_product` and decisions, never constants (DP-07). BR5 is served by the access check of RWB-P1-E1016-CON on the record read, so AC3 asserts the published answer and not a local guard. BR6 and BR7 are unchanged business facts: the approval is recorded on the case by the officer, and the installments come from the ACE plan through `recovery.v_ace_plan`.

### 9. State transitions

No case status changes: the story changes the DP04 freshness status (LOADED or STALE) through the stamp owner, and the state of the `Stage2ProductWorkflow` execution of a business date (RUNNING, COMPLETED or FAILED).

| From | Event | Condition | To |
|---|---|---|---|
| no execution for D | `rwb.source-data.AceDataReady.v1` consumed | The business date is inside the freshness window | `Stage2ProductWorkflow` RUNNING for D |
| RUNNING | treatments and claims written | The link check and the count check pass | COMPLETED and DP04 stamped for D |
| RUNNING | count difference or contract error | The check fails or the contract does not answer | FAILED or HELD, DP04 not stamped, break listed |
| FAILED | rerun for D | The workflow of D is not running | RUNNING again, rows replaced by record ID |
| COMPLETED | a change after the window | The treatment changed on D+1 | A new execution for D+1; nothing is rewritten for D |

The freshness states LOADED and STALE are the stamp owner's and are read here; the rows of `dp_treatment` and `dp_guarantee_claim` have no state machine of their own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow, the four activities, the two repositories, the count check and the DP04 branch of the record read |
| RW-DATASTEW, data steward | Owns DP04; reads the catalog entry and the breaks; confirms the system of record of each part |
| RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD | Read DP04 for cases in scope, through the access row in force |
| RW-COE, RW-AUDIT | Read DP04 for all cases |
| RW-PHONECOL and roles with no DP04 access row | May not read DP04 |
| rwb-case (P3) | Owns the treatment entity and answers the treatment contract this story consumes |
| rwb-guarantee (S3) | Owns the guarantee claim record and answers its contract; returns no claim until its own wave |
| The platform workflow owner | Owns the `rwb-source-data` task queue, the namespace and the worker registration this workflow runs on |
| No approval level from the delegation of authority applies | The story takes no business decision; it builds a data product |

No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry business dates, record IDs, codes and counts only.

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
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields | Write |
| DF-TRT-052 to DF-TRT-061 | dp_guarantee_claim | all fields | Write |
| DF-OPS-001 to DF-OPS-009 | data_product_load | all fields | Write |

treatment and guarantee_claim fields are read through the treatment contract of rwb-case and the guarantee contract of rwb-guarantee, not from their tables; the guarantee contract is outside the C dependencies of the plan (GAP-0509; ASM-0701). `recovery.v_ace_account` and `recovery.v_ace_plan` are read through this service's own ACE read contract and never copied. `data_product_load` is written by the freshness story on this story's call and not by a writer of its own (RWB-P1-E1015-APP). Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). This story supplies the DP04 branch of one operation whose shape is declared by RWB-P1-E2010-CON and shares the components of RWB-P1-E1016-CON; the branches of the other 13 data products belong to their own stories.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/data-products/{productCode}/records` (the DP04 branch) | `DataProductRecordPage` with `items` of `DataProductRecord` (`recordId`, `entity`, `fields` of `FieldValue`), `freshness` of `DataProductFreshness`, `page`, `size`, `total`; `productCode` DP04; query `caseId`, `page`, `size` | Case record R plus a DP04 access row in force, through the access check of RWB-P1-E1016-CON | Idempotent by product, case and page |

The errors are 403 with MSG-P4-002, 404 with MSG-P4-003 and 503 with MSG-GEN-006; the 400 and 401 of the shared envelope are declared by RWB-P1-E1016-CON and their texts are not restated here. The DP04 rows carry the snapshot fields of section 11 and the contract and plan facts read live from the two views; the record and page property names are those of `DataProductRecordPage`, `DataProductRecord` and `FieldValue` in the API Specification v5.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Pattern |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}/treatments` and the changed-window and active-count reads of the contract | P3 rwb-case (`RWB-P3-E2004-CON`) | The treatments of the window, the changed-window read and the active count; operation names are fixed by that contract; faked | DP-11; one hop, 2 s timeout |
| GET | the guarantee claim read of the rwb-guarantee contract | S3 rwb-guarantee | The TCG claims changed in the window; faked; the contract is not in the Work Package's C list, so its name and shape are Not specified in the source documents (GAP-0509; ASM-0701) | DP-11; one hop, 2 s timeout |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case (case contract) | The case-existence answer of the link check; faked and test-only, since the case reference arrives on each treatment row | DP-11; one hop, 2 s timeout |
| (interface) | `AceSourceReadRepository` over `recovery.v_ace_account` and `recovery.v_ace_plan` | P1 rwb-source-data (`RWB-P1-E1069-APP`) | The contract number, contract date and plan terms, read at request time and never written | DP-05; in-process in this service, published to others as the ACE read contract |

The guarantee claim read is the one consumed contract the Work Package does not list, and it is faked so the build never waits for S3 (GAP-0509; ASM-0701). The case-existence answer is reached through the case contract of rwb-case with the same gap and assumption, because the treatment contract returns the case reference but not the case itself. No other service is called: the status lists arrive as reference data through the keeper library (DP-07), and the ACE facts are read in this service's own views (DP-01, DP-05).

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP. This story publishes no event and writes no outbox row of its own.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts `Stage2ProductWorkflow` for the business date and the source; a redelivery starts no second run |

The event is this service's own and is consumed through the inbox of the outbox library, so the workflow start is idempotent by the cloud event id and the business date.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `Stage2ProductWorkflow` | Workflow, one execution per business date, workflow ID derived from the business date and the source | `rwb-source-data` in namespace `rwb-recovery` | Input: business date, source system, freshness summary; started by `AceDataReady`; run record with the outcome and the break references |
| `snapshot(page)` | Activity | `rwb-source-data` | The window [start of D, start of D+1); page number and size in; the treatment and claim rows of the page out |
| `writeDp04Page` | Activity | `rwb-source-data` | The rows of one page; the link check, the break path and one transaction per page that upserts by record ID and business date |
| `checkActiveCount` | Activity | `rwb-source-data` | The active count of the contract and the count written for D; a match or a break with the check text |
| `stampDp04` | Activity | `rwb-source-data` | The business date and product DP04; a call to the freshness stamp of RWB-P1-E1015-APP on a match |

The workflow and activity names are a target design choice and are fixed by no source document (GAP-0510; ASM-0702). The retry policy is the workflow kit's, and the rerun of a business date is refused while the execution of that date is running (MSG-P2-006).

#### 12.6 Schedules

None. The workflow is event-started from `rwb.source-data.AceDataReady.v1` and owns no Temporal Schedule and no legacy Quartz job; the freshness cut-off Schedules belong to RWB-P1-E1015-APP (DP-10; Architecture v5 slide 44, JOB-02 starts from AceDataReady).

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
| RWB-P3-E2004-CON treatment fake | The changed-window read and the active count | 40 active treatments and 12 plans with 9 approvals; a contract error; an active count of 41 against 40 rows; a treatment changed at 23:59:59 and one at 00:00:00 |
| rwb-guarantee guarantee claim fake | The changed-window claim read | 5 TCG claims for existing cases; one claim for case ID "00000000-0000-0000-0000-000000000997"; an empty list until S3 is built; a contract error |
| RWB-P1-E1016-CON access fake | The DP04 access answer | A granted answer for the DP04 reading roles; a refused answer for RW-PHONECOL on DP04 |
| rwb-case case-existence fake | The link check of AC4 | The known cases of the fixture; no case for "00000000-0000-0000-0000-000000000997" |
| ACE account and plan fixture | `recovery.v_ace_account` and `recovery.v_ace_plan` | Rows for the 40 accounts of the fixture with `contract_no`, `contract_date`, `plan_ref`, `installments`, `recommended_installment` and `booked_at`; an account with no plan |

The treatment, guarantee and access fakes are the published contracts of those stories; the ACE fixture stands in for the views of RWB-P1-E1069-APP; and the case-existence fake is the test-only answer of rwb-case's case contract, recorded with GAP-0509 and ASM-0701.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation branch on `/api/recovery/source-data/v1` | 3 consumed reads (treatment, guarantee claim, case existence) | OpenAPI 3.1, one hop, 2 s timeout, breaker per downstream (DP-11) |
| Kafka | None | 1 event (`rwb.source-data.AceDataReady.v1`) | Own topic, own event, inbox dedupe by cloud event id |
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
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-10 is the pattern this story is built on: the stage 2 step becomes an event-started workflow of this service. DP-01 and DP-05 are the ownership ruling and the live read of the ACE facts; DP-11 is the treatment and guarantee contracts with their fakes; DP-15 carries the two snapshot tables on the service sequence; DP-07 supplies the status lists; DP-13 and DP-19 fix the base and the screen path.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `Stage2ProductWorkflow` | Workflow | One execution per business date; the window, the page loop, the link check, the count check and the stamp call |
| `snapshot(page)` | Activity | The changed-window reads of the treatment and guarantee contracts, page by page |
| `writeDp04Page` | Activity | The link check, the break path and the upsert of `dp_treatment` and `dp_guarantee_claim` |
| `checkActiveCount` | Activity | The active-count comparison and its hold |
| `stampDp04` | Activity | The call to the freshness stamp of RWB-P1-E1015-APP |
| `DpTreatmentRepository`, `DpGuaranteeClaimRepository` | Repository | Upsert by record ID and business date, in schema `rwb_source_data` |
| `Dp04ReadService` | Service | The DP04 branch of the record read: the snapshot rows joined to the contract and plan facts, masked by the access answer |
| `Migrations` | Migration | The two snapshot tables on the per-service Flyway sequence, without a contract column |

**Database.** `dp_treatment` and `dp_guarantee_claim` hold the Workbench snapshot per business date. The legacy story dropped `dp_treatment.contract_no` and `dp_treatment.contract_date` because a contract is read from `v_ace_account` and never copied; in the target those columns are never created (BR2). No table holds a plan, a contract or an account row. The `data_product_load` row of DP04 is written through RWB-P1-E1015-APP.

**Configuration and reference data.** The DP04 row in `data_product` carries the owner role, the refresh cycle and the expected-by time of 08:00, which the legacy story assumed from DL11 and no source document fixes for DP04 (GAP-0511; ASM-0703). The DP04 access rows are the data steward's and are read through RWB-P1-E1016-CON. The status lists arrive as reference data (DP-07).

**Build steps**

1. The Flyway version with `dp_treatment` and `dp_guarantee_claim`, their keys on record ID and business date, and no contract column (DP-15).
2. `Stage2ProductWorkflow` and its input record, registered on `rwb-source-data`, with the workflow ID derived from the business date and the source (AC6).
3. `snapshot(page)` against the treatment and guarantee fakes, with the window [start of D, start of D+1) (AC1, AC2, AC8).
4. `writeDp04Page` with the link check, the References break and the upsert per page (AC4, AC6).
5. `checkActiveCount` and the hold of the stamp on a difference (AC7).
6. `stampDp04` through the freshness story, and the FAILED path of a contract error with the previous rows kept (AC5).
7. `Dp04ReadService` and the DP04 branch of the record read, with the live view read, the access answer and the freshness record (AC1, AC3).
8. Tests for AC1 to AC8 against the fakes and the ACE fixture.

**Feature flag.** `rwb.dataengine.stage2-products`.

**Done when.** The tests in section 16 pass, the workflow starts from a synthetic `AceDataReady` in SIT, `dp_treatment` and `dp_guarantee_claim` hold the rows of the business date, the DP04 stamp is LOADED on a count match and absent on a difference, the DP04 read answers with the live contract and plan facts, and the DP04 catalog entry shows in `GET /admin/data-products` in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | Role without a DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | DP04 stale after a failed step | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Count check break held the publish | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | TreatmentQuery or GuaranteeClaimQuery unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-02 is running | {job} is already running. Wait for it to finish before you rerun it. |

The five texts are the legacy texts carried unchanged; MSG-P1-001 and MSG-P1-002 are raised by the freshness story and read here, MSG-GEN-006 names the system of the failed contract, and MSG-P4-002 is the access answer of RWB-P1-E1016-CON. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-45 Data quality (Epic 2): state Loading while the list arrives; state Breaks shows the DP04 References breaks and the active-count break for the data steward. The case record view SCR-03 shows the DP04 data for roles with an access row in force. The settlement, restructure and deed-in-lieu screens that read DP04 come in Epic 3. Every one of them reaches this service through the gateway-bff composite route, which calls rwb-case and rwb-source-data in parallel, one hop each (DP-19); the screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-010-01 | AC1, BR1, BR2, BR6, BR7 | End to end | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02 | AC2, BR1 | End to end | 5 TCG claims for existing cases |
| TC-E2-010-03 | AC3, BR5 | End to end | RW-PHONECOL reads DP04 |
| TC-E2-010-04 | AC4, BR3 | End to end | TCG claim for an unknown case ID |
| TC-E2-010-05 | AC5 | End to end | The treatment contract fake returning errors |
| TC-E2-010-06 | AC6 | End to end | Step run twice for 2026-12-14 |
| TC-E2-010-07 | AC7, BR4 | End to end | The active count 41 against 40 rows |
| TC-E2-010-08 | AC8 | End to end | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09 | Access, BR5 | Component | RW-TRIBE calls the DP04 read with no DP04 access row; refused with MSG-P4-002 |

The nine legacy test case IDs are kept in order and their Covers and Data are carried onto the split; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. Where the legacy Covers names `Access`, the criterion is the published access answer of RWB-P1-E1016-CON on the DP04 read. The treatment and guarantee fakes of section 12.8 stand behind every case, and the ACE account and plan fixture replaces the views. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to RWB-ITG-E2010-ITG and are not listed here.

### 17. Guardrails

- No business value in code: the product code DP04, the owner role, the expected-by time and the access rows are data rows of `data_product`, `data_product_access` and the reference data, never constants (DP-07).
- No personal data in logs, events, workflow inputs or the fixture: the rows carry record IDs, case IDs, codes, dates and amounts only; test data is synthetic.
- No copy of ACE data: the contract number, contract date and plan terms are read from `recovery.v_ace_account` and `recovery.v_ace_plan` at request time, and the two snapshot tables hold no contract column (DP-01, DP-05).
- No read of another service's table: the treatment facts arrive through `RWB-P3-E2004-CON` and the claim facts through the guarantee contract, both with a fake (DP-11).
- ACE data only through the owner's contract or the `v_ace_*` views, and only this service names the views (DP-05).
- The workflow loads no business value from a source outside the contracts: every fact of a row is either the contract's or the view's, and the job runs from the freshness event rather than a fixed clock (DP-10).
- An applied migration is never edited: a correction to a snapshot table is a new version on the service sequence (DP-15).
- No call to NLEADS or the Thai Credit Guarantee Corporation: their results arrive as facts recorded on the case and on the claim (BR6).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-E2-010-01 to TC-E2-010-08 |
| REQ-RDF-010 | Access per data product by role; personal data masked by role under PDPA | Business Requirements Epic 2, section 3.1 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DP-07 | TC-E2-010-03, TC-E2-010-09 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E2010-CON | Contract | H: declares the DP04 branch of the record read, its shapes, its envelope and its fakes |
| RWB-P1-E2010-OPS | DevOps | X: deploys the workflow, the trigger, the flag, the dashboards and the alerts of this build |
| RWB-P1-E1016-CON | Contract | H: the access check per data product and the catalog entry the DP04 read answers with |
| RWB-P1-E1015-APP | App development | H: the freshness stamp this story calls and the LOADED and STALE states it reads |
| RWB-P1-E1069-APP | App development | H: the `recovery.v_ace_*` views and the ACE read path this story reads in-process |
| RWB-P3-E2004-CON | Contract | C: the treatment entity contract, faked |
| RWB-P3-E1043-CON | Contract | C: the reference data that supplies the status lists, with RWB-PLT-E1043-CON |
| S3 rwb-guarantee claim contract | Contract | C, outside the Work Package's C list: the guarantee claim read, faked (GAP-0509; ASM-0701) |
| RWB-ITG-E2010-ITG | Integration | I: the cross-service proof of the same legacy key against the live owners |

### 19. Out of scope

- The published shape of the DP04 record, its envelope and its fakes: RWB-P1-E2010-CON.
- The chart, the worker registration, the trigger proof, the flag, the dashboards, the alerts and the runbook: RWB-P1-E2010-OPS.
- The treatment entity, its plan timers and the credit approval record on the case: rwb-case, RWB-P3-E2004-APP and its contract.
- The guarantee claim record, its filing and its deadline timers: rwb-guarantee (S3, wave 3), consumed here as a contract with a fake.
- The freshness stamp, its stale flag and its Schedules: RWB-P1-E1015-APP; the access check and the catalog entry: RWB-P1-E1016-CON and its DB story.
- The ACE view SQL, the grants and the boundary rule: RWB-P1-E1069-APP and RWB-P1-E1069-DB.
- Settlement, restructure and deed-in-lieu screens: Epic 3; the gateway-bff composite route and the screen field list: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the treatment and guarantee reads against the live services: RWB-ITG-E2010-ITG.
- The expected-by time of DP04, which is the assumed 08:00 of DL11 until the data steward records the value (GAP-0511; ASM-0703).

# RWB-ITG-E1011-ITG Reconciliation and data quality report — integration

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Start rule: readiness call, `AceIngestCheck`, child `ReconciliationWorkflow` (`recon-{businessDate}`) with one activity; rwb-source-data consumes no event for it (RD-P1-040; finding #1).
- Case list rows, publish status, extracts, delivery, rwb-asset and rwb-comms reads, REC-03, REC-04 and NOT_RUN removed; the run compares ACE with the rwb-case open case accounts (RD-P1-024, RD-P1-022, RD-P1-042; #2, #5, #6, #7).
- Row set, stored percentage, message text and paths aligned; allocation wait and decision record added (AC20, AC21) (#8 to #12).
- Pending: rwb-case reads (GAP-3273, GAP-0337), result reads in the service contract (#3, #4), BREAK effect on the list (GAP-3282).
- Finishing pass: message English aligned to Error and Message Standard v6 (RD-P1-004); test case IDs of Test Cases v9 cited in place of the placeholders.
- A failed reconciliation run is restarted only by the job rerun, and a repeated ready call starts nothing after the run has ended (RD-P1-065, XD-11); the reconciliation checks of this story are unchanged by RD-P1-063 and RD-P1-069.
- The reconciliation result reads are cited as published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, RD-P1-063).
- Finishing follow-up: pinned the 5.1.0 reconciliation results fake for contract preflight.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1011-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1011-ITG-16); the squad sizes the story at refinement |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E1011-ITG-14) |
| Depends on (build) | RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P3-E1011-APP (build not done yet) |
| Contract dependencies | RWB-P1-E1011-CON, RWB-P1-E1015-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON; rwb-case allocation, open-case key and exclusion reads (GAP-3273, GAP-0337, GAP-3411) |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7); rwb-case operations Pending (GAP-3273, GAP-0337) |
| Integration dependencies | RWB-P1-E1011-APP, RWB-P1-E1015-APP, RWB-P3-E1011-APP. The job operations of RWB-P1-AD018 are a wave 4 integration dependency |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-RDF-007, REQ-RDF-008, REQ-CWC-004) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-008, RD-P1-012, RD-P1-022, RD-P1-024, RD-P1-040, RD-P1-042, RD-P1-004, RD-P1-063, RD-P1-065, RD-P1-069, RD-P1-011 |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-011 is split and reworked as the integration story RWB-ITG-E1011-ITG, the end-to-end proof of JOB-04 across rwb-source-data, rwb-case, rwb-asset, rwb-comms, rwb-integration and rwb-reporting, with the data lake removed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (34 resolved, 39 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; reconciliation integration aligned to the readiness-started child workflow, the removal of the P1 case list and the P1 check scope.

### 1. Story

As a **test engineer in the release squad (RW-TRIBE), with the data steward (RW-DATASTEW) as the reader of the result**, I want **the daily reconciliation REC-01, REC-02 and REC-05 proved end to end in SIT against the real wave-1 services — started as a child of the daily freshness check in rwb-source-data, reading its own ACE views, taking the open case accounts and the exclusions from rwb-case over one-hop contracts, writing the results in rwb_source_data and alerting the data steward on a break**, so that **each wave-1 release shows whether today's case accounts and their links can be trusted before the release date**.

### 2. Business rationale

No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. The legacy capability runs five reconciliations every business date — the account count by product against `v_ace_account` (REC-01), the balance by product (REC-02), approved treatments against `v_ace_plan` (REC-03), payments against proceeds (REC-04), and every business key on a Workbench table against the view that holds it (REC-05). rwb-source-data runs REC-01, REC-02 and its own part of REC-05; REC-03 and REC-04 belong to the treatment and payment slices (RD-P1-022; GAP-0496).

In the target the capability is spread over the real services, so the legacy story alone cannot prove it: `ReconciliationWorkflow` is a child of `AceIngestCheck` in rwb-source-data, the checks read the ACE views through the owner that holds them (DP-05), and the open case accounts and the exclusions come from rwb-case over one-hop REST contracts with a 2 s timeout (DP-11). No extract is written and no data lake exists (DP-17, ADR-018); readers use the result reads of rwb-source-data. This story builds that integration harness, runs it against the real services instead of the contract fakes, and holds the wave-1 release on its result. It applies control CTL-01 to REQ-RDF-007 and REQ-RDF-008 and applies REQ-CWC-004 for the exclusions.

### 3. Preconditions

- RWB-P1-E1011-APP is done: `ReconciliationWorkflow` and its one activity `reconciliation` run on task queue `rwb-source-data`, the results are written in `rwb_source_data` and read through `GET /admin/reconciliation/results`.
- RWB-P1-E1015-APP is done: the readiness call, `AceIngestCheck`, the freshness stamp and the start of the reconciliation child run in SIT.
- RWB-P3-E1011-APP is done: rwb-case answers the allocation status, the dated open-case account keys and balances and the exclusions of a business date. Pending: operations, paths and paging, owner rwb-case service owner (GAP-3273, GAP-0337, GAP-3411).
- rwb-source-data and rwb-case are deployed in SIT in one environment, each on its own base `/api/recovery/<short>/v1`, each on its own schema and login (DP-01, DP-02), with the SIT Kafka topics and the Temporal namespace `rwb-recovery` reachable.
- The harness can call `POST /business-days/{date}/ready` for the SIT business date, so the reconciliation is started by the real chain.
- The SIT data set carries the synthetic fixture values of the legacy criteria: MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 accounts at 90 days past due or more, no UNSECURED account at 90 days past due or more; the 12 SSME account keys of the break fixture; the person_key "P0099881" of the orphan fixture; and the parameter `recon.tolerance.pct` 0.00 in force for REC-01 and REC-02.
- The reconciliation results are read through `GET /admin/reconciliation/results` on `/api/recovery/source-data/v1` (API-P1-003) with Platform administration R, and SCR-45 Data quality is reachable read-only.
- No data lake path is provisioned in SIT: the legacy INT-19 outbound adapter is not installed and no extract is produced (DP-17).
- REC-03 (treatments) and REC-04 (payments) are not part of this run; they stay with their owning slices (GAP-0496; ASM-0688).
- No build dependency: the integration dependencies are the real services, and the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Harness: calls `POST /api/recovery/source-data/v1/business-days/2026-11-30/ready` with a UUID `Idempotency-Key`; `AceIngestCheck` stamps the ALS batch and publishes `rwb.source-data.AceDataReady.v1` (key `ALS:2026-11-30`).
2. In the workflow task that commits the ALS stamp, `AceIngestCheck` starts `ReconciliationWorkflow` as a child with workflow ID `recon-2026-11-30` and input `{businessDate, startedBy}` on task queue `rwb-source-data`. No event starts it.
3. The one activity `reconciliation` waits for the rwb-case allocation (poll every `recon.allocation.poll.minutes` = 5) and proceeds at ALLOCATION_COMPLETE YES or at `caselist.allocation.wait.until` 07:15 Asia/Bangkok; an unreadable allocation answer blocks the checks.
4. It reads `case.entry.dpd` and `recon.tolerance.pct` through the parameters contract (DP-06) and LOV-PRODUCT through the reference-data contract (DP-07).
5. REC-01 and REC-02: for each product it counts and sums `v_ace_account` rows at or above the entry threshold for the business date, excluding the accounts rwb-case excluded at entry, and compares them with the dated open case accounts that rwb-case returns.
6. REC-05: it resolves the business keys held on P1 tables and the open `case_account.account_key` and `case_party.person_key` keys served by rwb-case against the ACE views; an orphan is counted and changes no row.
7. It replaces the REC-01 and REC-02 rows of the date in one transaction, two per product, unique on rec_code, business_date and product_group.
8. A BREAK raises MSG-P1-012 and the Reconciliation break alert for the data steward. Pending: effect on the rwb-case list (GAP-3282).
9. It writes one decision record for the completed execution; the library publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`.
10. The harness: waits for the workflow, asserts the rows through the result reads, asserts the alert and the decision record, and records one verdict per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product's variance is above the tolerance | Result BREAK; alert; the effect on the rwb-case list is open (GAP-3282) | MSG-P1-012 | AC2, AC15 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | The ACE batch for the business date is not COMPLETED | No reconciliation child starts and no result row is written for the date | MSG-P1-001 | AC4 |
| X4 | A FAILED execution is rerun for the same date after a fix | The date's results are replaced | None | AC15 |
| X5 | The ready call is repeated or AceDataReady is delivered again | One row per check, product and date; no second open run and no child started from Kafka | None | AC12 |
| X6 | A business key has no ACE row | The orphan is counted in the run summary and decision record; no REC-05 row is stored and no Workbench row changes | None | AC7 |
| X7 | A view, a contract or the store returns an error during the run | After the retries the run is FAILED with the system named; no partial row is written and a previously committed set is unchanged | MSG-GEN-006 | AC17 |
| X8 | A role without Platform administration R lists the break rows | 403 | MSG-P4-002 | AC18 |
| X9 | A cross-service read exceeds the 2 s budget on every attempt | The run fails; no result row is written for the date | MSG-GEN-006 | AC13 |
| X10 | Removed in version 3: no extract is delivered | — | — | — |
| X11 | REC-03 and REC-04 are outside this run | No REC-03 or REC-04 row is written and no NOT_RUN value exists | None | AC19 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Proves behaviour that already exists in the integration dependencies; builds no product capability and changes no case |
| Negotiable | The fixture values and the harness settings are configuration; the checks and the tolerance rule are fixed |
| Valuable | A release cannot claim the wave-1 reconciliation works until the real services pass the run together, which no single service story can show |
| Estimable | One harness, one start driver, the rwb-case read checks, the result, alert and decision-record assertions |
| Small | Fits one sprint with its test cases |
| Testable | Every criterion is one automated test against the real SIT services, with the failure path recorded |

### 7. Acceptance criteria

```gherkin
Feature: Reconciliation and data quality report across the wave-1 services

  Background:
    Given the business date is 2026-11-30 and rwb-source-data shows ALS COMPLETED for 2026-11-30 through its contract
    Given the parameter recon.tolerance.pct = 0.00 is in force for REC-01 and REC-02
    Given the reconciliation reads source data only through the rwb-source-data contract, the owner of the ACE view contract (DP-01, DP-05)

  Scenario: AC1 Variance under limit (legacy RWB-E1-011 AC1)
    Given rwb-source-data holds accounts at 90 days past due or more less the exclusions as MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, and none for UNSECURED
    Given rwb-case answers the open case accounts of the date as MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 with equal balance sums
    Given every business key in scope resolves to its ACE row
    When the reconciliation of 2026-11-30 completes
    Then eight reconciliation_result rows exist, REC-01 and REC-02 for MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED, each with variance 0 and result PASS
    Then no MSG-P1-012 and no Reconciliation break alert is raised

  Scenario: AC2 Variance over limit (legacy RWB-E1-011 AC2)
    Given rwb-source-data holds 2,903 SSME accounts at 90 days past due or more less the exclusions
    Given rwb-case answers 2,891 SSME open case accounts, a difference of 12 accounts
    When the reconciliation of 2026-11-30 completes
    Then the REC-01 result for SSME is BREAK with variance_count 12, variance_pct 0.4134 and tolerance_pct 0.00
    Then the data steward alert Reconciliation break is raised with MSG-P1-012 "The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent." filled with the date, SSME, 12 and the percentage
    Then the REC-01 results of MORTGAGE and HIRE_PURCHASE are PASS
    Then the assertion on the 12 listed break account keys is pending the break-detail store (GAP-1508, GAP-3413)

  Scenario: AC3 Variance equal to the tolerance (legacy RWB-E1-011 AC3)
    Given a new version of the parameter recon.tolerance.pct with value 0.10 is in force on 2026-11-30
    Given the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent
    When the reconciliation of 2026-11-30 completes
    Then the MORTGAGE result is PASS and the SSME result is BREAK

  Scenario: AC4 ACE batch not complete (legacy RWB-E1-011 AC4)
    Given v_ace_batch_status holds no COMPLETED ALS row for 2026-11-30 at 08:00
    When the ready call is made and the DP01 cut-off passes
    Then no ReconciliationWorkflow recon-2026-11-30 starts and no reconciliation_result row exists for 2026-11-30
    Then the freshness workflow raises MSG-P1-001 for DP01

  Scenario: AC7 Business key without an ACE row (legacy RWB-E1-011 AC7)
    Given case_party on case "RW-2026-000140" carries person_key "P0099881", which has no row in v_ace_customer, and rwb-case serves that key in its open-case key read
    When the reconciliation of the date completes
    Then the run summary and the decision record count one orphan
    Then no REC-05 row is in reconciliation_result and the case and its case_party row are unchanged
    Then the assertion on the listed key "case_party.person_key P0099881" is pending the break-detail store (GAP-1508, GAP-3413)

  Scenario: AC12 The reconciliation starts as a child of the freshness check (new, D-RCV-60; restated by RD-P1-040)
    Given every source due for 2026-11-30 has a COMPLETED batch row and the rwb-case allocation is complete
    When POST /business-days/2026-11-30/ready is called
    Then one ReconciliationWorkflow with ID recon-2026-11-30 runs on task queue rwb-source-data as a child of ace-ingest-check-2026-11-30, with the one activity reconciliation
    Then it uses 2026-11-30 for every check and never a mix of two business dates
    Then reconciliation_result holds one row per rec_code, business_date and product_group, REC-01 and REC-02 only
    When the ready call is repeated and AceDataReady is delivered again
    Then no second row is written and rwb-source-data starts no child from Kafka

  Scenario: AC13 Every cross-service read is one hop on the owner's contract (new, D-RCV-60)
    Given the reconciliation is running for 2026-11-30
    When it needs the allocation status, the open-case account keys and the exclusions of the date
    Then it calls only rwb-case, each call one hop with a 2 s timeout and no call chained through a second service
    Then it calls neither rwb-asset nor rwb-comms and reads no table of rwb_case
    Then a read that exceeds the 2 s budget on every attempt fails the run and no result row is written
    Then the operations, paths and payloads of these reads are pending GAP-3273, GAP-0337 and GAP-3411

  Scenario: AC14 No extract and no data lake path exists (new, D-RCV-60; restated by DP-17)
    Given the reconciliation of 2026-11-30 has completed
    When a reader with Platform administration R calls GET /api/recovery/source-data/v1/admin/reconciliation/results
    Then the answer holds the REC-01 and REC-02 rows of 2026-11-30
    Then no extract file is written, deliverFile is not called, no rwb.integration file event is published for the run and no data lake path or INT-19 adapter exists

  Scenario: AC15 A restart after a failed execution replaces the date set (new, D-RCV-60; restated by RD-P1-024)
    Given the execution of 2026-11-30 is FAILED and the data steward has corrected the SSME difference of 12 accounts
    When POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun is called with the run ID of the failed run and a new Idempotency-Key
    Then the answer is 202 and a new run of 2026-11-30 starts (a rerun of a COMPLETE run answers 409 MSG-P1-011; a repeated ready call starts nothing)
    Then the REC-01 and REC-02 rows of 2026-11-30 are replaced atomically and all eight are PASS
    Then one decision record is written for the completed execution
    Then no publish status is set or read

  Scenario: AC16 SCR-45 shows its empty, loading, error and no access states (new, D-RCV-60)
    Given the reconciliation report of 2026-11-30 is opened on SCR-45
    Given the composite route of SCR-45 is the edge's, its screen shell is rwb-reporting's, and rwb-source-data serves its job, freshness, reconciliation and dictionary operations
    When the report has no reconciliation rows
    Then SCR-45 shows the empty state with the text Not specified in the source documents (DOR-RWB-ITG-E1011-ITG-10)
    When the report is still loading
    Then SCR-45 shows the loading state as Screen Specifications v1 gives it
    When a read of the report fails
    Then SCR-45 shows the error state with MSG-GEN-006
    When a role without Platform administration R opens SCR-45
    Then SCR-45 shows the no access state with MSG-P4-002

  Scenario: AC17 A view or store error fails the run and writes no result (new, D-RCV-60)
    Given a view or a store returns an error during the reconciliation run for 2026-11-30
    When the reconciliation step runs
    Then no reconciliation_result is written for 2026-11-30
    Then the run is FAILED with the failing system named and MSG-GEN-006 is written

  Scenario: AC18 A role without Platform administration R cannot list the break rows (new, D-RCV-60)
    Given the user has role RW-CASEOWN without Platform administration R
    When the user lists the break rows of the reconciliation run
    Then the system returns 403 with MSG-P4-002

  Scenario: AC19 REC-03 and REC-04 are outside the run (new, D-RCV-60; restated by RD-P1-042)
    Given the ALS batch for 2026-11-30 is COMPLETED
    When the reconciliation of 2026-11-30 completes
    Then no REC-03 and no REC-04 row exists, no NOT_RUN value is written and no treatment or proceeds table or contract is read

  Scenario: AC20 The run waits for allocation until the limit (new, RD-P1-040)
    Given the rwb-case allocation answer for 2026-11-30 is readable and incomplete
    When 07:15 Asia/Bangkok is reached
    Then the checks start for 2026-11-30 and no allocation check is recorded as a P1 result
    Then one decision record is written and rwb.decision.DecisionRecorded.v1 is published on rwb.decision-record.v1 with no account number or customer name

  Scenario: AC21 An unreadable allocation answer writes nothing (new, RD-P1-042)
    Given the rwb-case allocation answer for 2026-11-30 cannot be read
    When all attempts of the read are exhausted
    Then the run fails with MSG-GEN-006 for rwb-case and no reconciliation_result row is written for 2026-11-30

```

The five scenarios AC1, AC2, AC3, AC4 and AC7 are the legacy proof of RWB-E1-011. Their fixture values are kept; the comparison target is the rwb-case open case accounts, and the rows, publish status, lake and report refresh of the legacy wording are restated under RD-P1-024, RD-P1-040 and RD-P1-042. No scenario uses a contract mock: the run is against the real service contracts.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Accounts at or above the entry threshold in `v_ace_account` for the business date are compared with the open case accounts rwb-case returns, by count per product, every business date | REC-01; CTL-01; REQ-RDF-007; RD-P1-024 |
| BR2 | Balances in `v_ace_account` are compared over the same account populations, by sum per product | REC-02; RD-P1-024 |
| BR3 | REC-03 is owned by the treatment slice and is not run here (`recon.treatment.days`) | REC-03; RD-P1-022 |
| BR4 | REC-04 is owned by the payment slice and is not run here (`recon.payment.days`) | REC-04; RD-P1-022 |
| BR5 | rwb-source-data resolves the business keys held on P1 tables and the open `case_account.account_key` and `case_party.person_key` keys served by rwb-case against the ACE views; asset and payment keys are checked by their owners | REC-05; REQ-RDF-007; RD-P1-022 |
| BR6 | A result is a break when the variance percent is above the tolerance; at 0.00 any difference is a break | Parameter recon.tolerance.pct 0.00 (DL25 option A, RD-P1-042) |
| BR7 | A break in REC-01 or REC-02 raises MSG-P1-012 and the Reconciliation break alert for the data steward; the effect on the rwb-case list is open (GAP-3282) | FEAT-RDF-13; RD-P1-024 |
| BR8 | Accounts excluded at entry are explained and do not count as breaks | REC-01 "zero unexplained"; REQ-CWC-004 |
| BR9 | The reconciliation starts only after the ALS stamp of the business date | BR-P1-014-4; RD-P1-040; MSG-P1-001 |
| BR10 | Report grades (green, red, not run) are a rwb-reporting presentation; the stored result values are PASS and BREAK only | FEAT-RDF-12; RD-P1-042 |
| BR11 | A repeated run for the same date replaces that date's results | R-UNI-40 |
| BR12 | The reconciliation reads ACE for the business date of the ACE batch it was started by, and never a mix of two business dates | BR-P1-011-2 |
| BR13 | A REC-05 orphan never deletes or changes a Workbench record; it is listed for the data steward and, where the row is missing in ACE, for the ACE team | BR-P1-011-3 |
| BR14 | Every cross-service read is one hop on the owner's contract with a 2 s timeout; the reconciliation reads the allocation status, open case accounts and exclusions from rwb-case and reads no other service's tables | DP-01; DP-11; ADR-020; RD-P1-022 |
| BR15 | There is no data lake and no extract: readers use the result reads of rwb-source-data | DP-17; ADR-018; GAP-0495 |

### 9. State transitions

None for a case status. This story changes no case. It proves the status of `reconciliation_result` (PASS or BREAK) and the RUNNING, completed or FAILED state of `ReconciliationWorkflow`. No publish status and no NOT_RUN value exist (RD-P1-024, RD-P1-042).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login, DP-02) | Runs the reconciliation, writes `reconciliation_result`, raises the alert and writes the decision record |
| rwb-treatment (S2) and rwb-payment (P8) | Own REC-03 and REC-04; no part in this run |
| rwb-case service identity | Answers the one-hop reads of the run; no write in this story |
| RW-TRIBE, release squad and test engineers | Call the ready operation under the SIT configuration, run the harness, read the verdicts |
| RW-DATASTEW, data steward and data product owner | Reads the results and the break rows (Platform administration R); signs the daily reconciliation to ACE |
| RW-PLATADM, platform administrator | Reads the results; restarts a FAILED run from the job operations once RWB-P1-AD018 is released (wave 4) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read the results and the break rows (Platform administration R) |
| RW-TEAMMGR, RW-BIANAL and other report readers | Read the report (Reporting R); RW-BIANAL builds it (Reporting CRUD) |
| ACE team | Reads the orphan list for a key that has no ACE row |

The per-service login names are Not specified in the source documents (GAP-0337; ASM-0431); the story names them "the rwb-<short> login (DP-02)".

### 11. Data

| BR Field ID | Entity | Owning schema | Field | Read or write |
|---|---|---|---|---|
| DF-ACE-001 | v_ace_account | ACE view, read by rwb-source-data | account_key | Read |
| DF-ACE-018 | v_ace_account | ACE view, read by rwb-source-data | days_past_due | Read |
| DF-ACE-020 | v_ace_account | ACE view, read by rwb-source-data | total_balance | Read |
| DF-ACE-036 | v_ace_account | ACE view, read by rwb-source-data | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | ACE view, read by rwb-source-data | person_key | Read |
| DF-ACE-075, DF-ACE-076 | v_ace_contact | ACE view, read by rwb-source-data | contact_type, contact_key | Read |
| DF-ACE-178, DF-ACE-179, DF-ACE-186 | v_ace_batch_status | ACE view, read by rwb-source-data | source_system, business_date, is_complete | Read |
| DF-RPT-001 to DF-RPT-019 | case_list_row | — | Retired (RD-P1-024) | Not read |
| DF-CAS-057, DF-CAS-058 | case_entry_exclusion | rwb_case (P3) | account_key, business_date | Read through the rwb-case contract |
| DF-CAS-026 | case_account | rwb_case (P3) | account_key | Read through the rwb-case contract |
| DF-CAS-032, DF-CAS-004 | case_party, recovery_case | rwb_case (P3) | person_key, primary_person_key | Read through the rwb-case contract |
| DF-INT-003, DF-INT-022 | interaction | rwb_source_data (P1) | person_key, contact_key | Read by rwb-source-data |
| DF-EXT-004, DF-EXT-017, DF-EXT-028, DF-EXT-038 | party_ext, contact_point_ext, account_ext, valuation_ext | rwb_source_data (P1) | person_key, contact_key, account_key, valuation_key | Read by rwb-source-data (REC-05) |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | rwb_source_data (P1) | id, rec_code, business_date, product_group, source_count, workbench_count, source_amount, workbench_amount, variance_count, variance_pct, tolerance_pct, result | Write by rwb-source-data; read by the harness through the P1 result reads |

Field IDs are those in the Logical Data Model and Data Dictionary. Criteria and tests read the ACE views only through rwb-source-data (DP-01), never directly, and cite the reconciliation_result rows and the P1 result reads, not the legacy job or decision-log wording. The harness reads and writes nothing directly: every field above is read through the owning service's contract or through the rwb-source-data views and result reads (DP-01, DP-05). `case_list_row` is retired: rwb-case holds the case list (RD-P1-024).

### 12. Contract

#### 12.1 REST operations provided

None. This story builds and runs an integration harness and publishes no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the run | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | Batch completeness of the business date before the run | One hop, 2 s |
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Starts the chain, UUID `Idempotency-Key`, 202 | — |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` and `/admin/reconciliation/results/{resultId}` | P1 rwb-source-data (RWB-P1-E1011-CON) | REC-01 and REC-02 rows. Both operations are published in rwb-source-data.yaml 5.1.0 (`getAdminReconciliationResults`, `getAdminReconciliationResultsResultid`; RD-P1-063) | One hop, 2 s |
| Pending (GAP-3273) | Paged open-case key read of the business date, including balances, `case_account` and `case_party` keys | P3 rwb-case | REC-01, REC-02, REC-05 | One hop, 2 s |
| Pending (GAP-3411) | Allocation status of the business date | P3 rwb-case | The wait before the checks | One hop, 2 s |
| Pending (GAP-0337) | Exclusions of the business date | P3 rwb-case | Accounts excluded at entry, for REC-01 and REC-02 | One hop, 2 s |

The workflow itself performs the rwb-case reads inside its activity; the harness asserts that each is one hop inside the budget. The parameter and reference reads use RWB-P3-E1042-CON and RWB-P3-E1043-CON.

#### 12.3 Events published

| Event | Topic | Owner | Asserted in the run |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P1 rwb-source-data (decision-record library) | One per completed execution (AC20); no account number or customer name |

The event is published by the service, not by the harness; the story asserts it, and it carries IDs, references and facts only (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner | Asserted in the run |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Published for ALS with key `ALS:{businessDate}`; rwb-source-data does not consume it, and a redelivery starts no reconciliation child (AC12) |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Asserted in the run |
|---|---|---|---|
| `ReconciliationWorkflow` (JOB-04), ID `recon-{businessDate}` | Workflow, child of `AceIngestCheck` after the ALS stamp; USE_EXISTING and ALLOW_DUPLICATE | `rwb-source-data` | One run per business date, one transaction for the results |
| `reconciliation` | The one activity | `rwb-source-data` | Runs REC-01, REC-02 and the P1 part of REC-05 |

#### 12.6 Schedules

| Schedule or trigger | Cadence | Asserted in the run |
|---|---|---|
| Child start by `AceIngestCheck`; the 05:30 Schedule `rwb-source-data-ace-late-check` and the fallback poll can start the parent | Once per ALS stamp of a business date | A repeated ready call joins the open run; once the sources of the date are stamped and the run has ended it starts nothing (RD-P1-065, register XD-11) |

#### 12.7 Tables owned

None. The harness owns no table (DP-01); `reconciliation_result` belongs to rwb-source-data and `case_entry_exclusion` to rwb-case, and the harness reads them through the owning contract.

#### 12.8 Contract fakes

The contract preflight pins `fakes/rwb-source-data/5.1.0/` from RWB-P1-E1011-CON for the aggregate reconciliation result reads, `GET /admin/reconciliation/results` and `GET /admin/reconciliation/results/{resultId}`. The SIT integration run uses the deployed services and fails if it substitutes a fake.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided; consumed: freshness, ready call and result reads of rwb-source-data, and the three rwb-case reads (pending) through the workflow |
| Kafka | 0 published by the harness; AceDataReady and DecisionRecorded observed |
| Temporal | `AceIngestCheck`, its child `ReconciliationWorkflow` and the activity `reconciliation` on `rwb-source-data` |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/reconciliation` in the ACE repository, package `<ACE base package>.recovery.itg.reconciliation`. Not part of a deployed service; it runs in the SIT release pipeline.

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

The story carries no H, C, I or X dependency beyond the integration dependencies, because the harness builds nothing: DP-03 resolves to reading decision records the services write, DP-06 and DP-07 to reading parameters and reference data through the deployed contracts, DP-10 to observing the workflows that RWB-P1-E1015-APP and RWB-P1-E1011-APP own, DP-14 to asserting the names, DP-15 to reading the schemas of the DB stories, DP-17 to asserting that no lake path exists, and DP-19 to reading SCR-45 read-only through gateway-bff. The H dependencies of these patterns stay with the implementation stories of the owning services.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| StartDriver | Test harness | Calls `POST /business-days/{date}/ready` and waits for the parent and child workflows |
| WorkflowProbe | Test harness | Asserts one child `recon-{businessDate}` on queue `rwb-source-data` and the business date input |
| ContractProbe | Test harness | Observes the rwb-source-data and rwb-case calls with the 2 s budget and records status, time and body |
| ResultAssertion | Test harness | Compares the result reads with the expected results, variances and row count of the fixture |
| AlertAndRecordAssertion | Test harness | Asserts MSG-P1-012, the alert, the decision record and its event, and that no extract exists |
| FixtureLoader | Test harness | Loads the synthetic SIT fixture values of the legacy criteria; holds no production data |
| ScreenProbe | Test harness | Reads SCR-45 read-only through gateway-bff |

**Topology and fixtures**

- One SIT environment: rwb-source-data and rwb-case, one ACE SIT database with one schema and one login per service (DP-01, DP-02), the SIT Kafka topics, the Temporal namespace `rwb-recovery` with one task queue per service, and no data lake (DP-17).
- Synthetic fixtures only: MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 accounts at 90 days past due or more with equal balance sums for AC1; 2,891 SSME open case accounts for AC2; the tolerance 0.10 parameter version for AC3; no COMPLETED ALS row for AC4; the person_key "P0099881" absent from `v_ace_customer` for AC7; 2,903 SSME accounts against 2,891 open case accounts for AC15.
- The fixture loader seeds only through the SIT data set; it never writes a service table and never calls a production endpoint.

**Run order**

1. FixtureLoader loads the fixture set and the parameters of the date.
2. ContractProbe confirms that rwb-source-data and rwb-case answer on their own base and that no service reads another schema.
3. StartDriver calls the ready operation for 2026-11-30; WorkflowProbe registers the parent and the child.
4. The run completes; ResultAssertion reads the result operations and asserts the eight rows (AC1, AC2, AC3, AC12).
5. AlertAndRecordAssertion asserts MSG-P1-012 on the break fixture, the decision record and its event, and that no extract exists (AC2, AC14, AC20).
6. Force the failure paths and the allocation wait and assert AC13, AC17, AC20 and AC21; rerun the failed run and assert AC15.
7. ScreenProbe reads SCR-45 read-only (AC16).
8. The harness writes one verdict per test case of section 16 and fails the release stage on any FAIL.

**Build steps**

1. StartDriver and WorkflowProbe with the one-run-per-date assertion; tests for AC12.
2. ContractProbe over the reads with the 2 s budget and the timeout path; tests for AC13.
3. ResultAssertion for the eight-row and unique-key behaviour; tests for AC1 to AC4 and AC19.
4. FixtureLoader with the legacy fixture values of section 13 and the parameter version of AC3; no production value.
5. AlertAndRecordAssertion with the alert, decision-record and no-extract assertions; tests for AC2, AC14, AC15, AC20 and AC21.
6. ScreenProbe with the SCR-45 reads.
7. Add the stage to the release pipeline before the wave-1 exit and run it once on the wave-1 build.

**Done when.** The test cases of section 16 pass against the SIT services, each completed date shows eight `reconciliation_result` rows, the break raises the alert, and no extract or data lake path exists in the environment.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The ACE batch is not complete; the freshness workflow raises it and no reconciliation starts | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A view, a contract call or the store is unavailable during the run | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness verdicts are for the release team and are not part of the message standard; the business messages above are the legacy texts, copied unchanged.

### 15. Screens and states

No Workbench screen is built in this story. Two existing surfaces are exercised read-only: the result reads `GET /admin/reconciliation/results` on `/api/recovery/source-data/v1` (API-P1-003), and SCR-45 Data quality through gateway-bff (DP-19; console owned by RWB-P1-AD019-APP), read in its list state to confirm the same breaks are visible to the data steward. The harness changes no screen state and takes no screenshot. SCR-45 states (AC16): loading as Screen Specifications v1 gives it; error shows MSG-GEN-006 and no access shows MSG-P4-002; the empty state text is Not specified in the source documents (DOR-RWB-ITG-E1011-ITG-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07-ITG, TC-ITG-E1011-08 | AC18, Access | Component | RW-CASEOWN calls the reconciliation result reads; refused with MSG-P4-002 |
| TC-E1-011-01-ITG | AC1, BR1, BR2, BR5, BR8 | End to end | MORTGAGE 12,256, HIRE_PURCHASE 12,960, SSME 2,903 with exclusions against equal open case accounts; no orphan |
| TC-E1-011-02-ITG | AC2, BR6, BR7 | End to end | 12 SSME accounts with no open case account |
| TC-E1-011-03-ITG | AC3, BR6 | Integration | Parameter version 0.10; variances 0.10 and 0.11 percent |
| TC-E1-011-04-ITG | AC4, BR9 | Integration | No COMPLETED ALS row for 2026-11-30 |
| TC-E1-011-05-ITG | AC5, BR11 (run by RWB-P1-E1011-APP) | Integration | Break, missing cases created, restart |
| TC-E1-011-06-ITG | AC6, BR11 (run by RWB-P1-E1011-APP) | Integration | Two reconciliation workflow runs for the same date on two nodes |
| TC-E1-011-08-ITG | AC7, BR5, BR13 | Integration | person_key P0099881 absent from the ACE customer view and served by the open-case key read |
| TC-E1-011-09-ITG | AC8, BR12 (run by RWB-P1-E1011-APP) | Integration | rwb-source-data returning an error after the MORTGAGE count |
| TC-ITG-E1011-01 | AC12, BR9, BR11, BR12 | Integration | Ready call for 2026-11-30, repeated; AceDataReady redelivered |
| TC-ITG-E1011-02 | AC13, BR14 | Integration | The rwb-case reads with a 2 s budget; a forced 3 s answer |
| TC-ITG-E1011-03 | AC14, BR15 | Integration | Result reads; no extract, deliverFile call or lake path |
| TC-ITG-E1011-04 | AC15 | End to end | Failed 12-account run, correction, restart with eight PASS rows |
| TC-ITG-E1011-05 | §12 operations, events and activities | Integration | Contract test of each §12 operation, event and activity against its published service contract; no contract fake |
| TC-ITG-E1011-06 | AC16 | Component | SCR-45 with no reconciliation rows, while loading, on a failed read, and for a role without Platform administration R |
| TC-ITG-E1011-07 | AC17 | Integration | A view returns an error during the run for 2026-11-30; no result written; run FAILED |
| TC-ITG-E1011-08 | AC18 | Integration | Role RW-CASEOWN without Platform administration R lists the break rows; 403 with MSG-P4-002 |
| TC-ITG-E1011-09 | AC19, BR3, BR4 | Integration | No REC-03 or REC-04 row and no NOT_RUN value |
| TC-E1-011-10-ITG | AC20 | Integration | Readable, incomplete allocation answer at 07:15; decision record and DecisionRecorded event |
| TC-E1-011-11-ITG | AC21 | Integration | Allocation read fails on every attempt; MSG-GEN-006; no row |

The nine legacy test cases are carried as integration copies in the order of the WP and keep the legacy IDs with the `-ITG` suffix, the legacy Covers and the legacy data; the legacy level System maps to Integration, and Access to Component. The legacy acceptance criteria not owned here (AC5, AC6 and AC8) are owned by RWB-P1-E1011-APP and are re-exercised only inside the end-to-end run of this story, through TC-E1-011-05-ITG, TC-E1-011-06-ITG and TC-E1-011-09-ITG.

### 17. Guardrails

- No business value in code: the tolerance, the wait time, the threshold and the fixture values are configuration and the SIT data set; the release stage compares them with the parameter values in force.
- No personal data in logs, reports, tests or prompts: break rows carry account keys, account numbers and business keys only, and the fixtures are synthetic.
- No read of another service's tables: every cross-service field comes through the owner's contract, one hop with a 2 s timeout (DP-01, DP-11), and the harness asserts that no service reads a table of `rwb_source_data`.
- ACE data only through rwb-source-data, which owns the `recovery.v_ace_*` views (DP-05); no other service and no harness process opens an ACE view.
- No data lake path: no INT-19 adapter, no INT-20 extract and no case list extract is installed or read (DP-17).
- The harness runs in SIT only; it never points at UAT or production and never writes a service table.
- A failing verdict is never added to an exception list; a limit that must change is changed in the service story that owns it.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count in v_ace_account with no variance, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | All recovery processes | REC-01; REC-02; REC-05; CTL-01; R-UNI-40 | Test cases of AC1, AC2, AC7, AC12 and AC13 (section 16) |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-05; CTL-01 | Test cases of AC1, AC2, AC4, AC14 and AC15 (section 16) |
| REQ-CWC-004 | Exclusion rules as data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 Take over the case at 90 days past due | None | TC-E1-011-01-ITG, TC-ITG-E1011-02 |

### 19. Out of scope

- The build of `ReconciliationWorkflow`, the checks and the results (RWB-P1-E1011-APP), its contract baseline (RWB-P1-E1011-CON) and its deployment, dashboards and runbook (RWB-P1-E1011-OPS).
- The exclusion rules, the exclusion resource and the exclusion API of rwb-case (RWB-P3-E1011-APP).
- REC-03, REC-04 and the asset, payment and notice key checks of other services.
- The remaining reconciliations REC-06 to REC-09: write-offs, assets taken on, the decision log copy and notice barcodes.
- Cross-source case count reconciliation in the reporting module (FEAT-RPT-05 full scope, Epic 2).
- The data quality console SCR-45 and the quality measure definitions (Epic 2 and Epic 8); this story reads them read-only.
- Working a break to closure with an owner and a date (FEAT-RPT-09 full scope, Epic 2), and any effect of a break on the rwb-case list (GAP-3282).
- The production monitoring of the daily run and its alerts (the platform observability epic).

### Remaining delivery steps

- Publish the rwb-case allocation, open-case key and exclusion operations with fakes (rwb-case service owner; GAP-3273, GAP-0337, GAP-3411).
- Add the reconciliation result reads to rwb-source-data.yaml (contract owner).
- Settle the break-detail store (data architect with the contract owner; GAP-1508, GAP-3413).
- Rule the effect of a BREAK on the rwb-case list (solution architect with the data lead; GAP-3282).
- Size the story at refinement (squad).
- Epic design sign-off for business epic EP01 (solution architect).
- Load the SIT synthetic data and parameter versions of the fixtures (QA team).
- Restate and add the test case rows in Test Cases v9 and the Requirements Traceability Matrix (test writer).

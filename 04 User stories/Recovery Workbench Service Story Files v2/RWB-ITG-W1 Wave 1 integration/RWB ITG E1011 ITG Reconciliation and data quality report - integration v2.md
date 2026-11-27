# RWB-ITG-E1011-ITG Reconciliation and data quality report — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Depends on (build) | RWB-P1-E1011-APP, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP (build not done yet) |
| Contract dependencies | The section 12.2 operations not yet in the API Specification v5 are published by their provider contracts (rwb-source-data, rwb-case, rwb-comms, rwb-reporting); publishing story Not specified in the source documents (DOR-RWB-ITG-E1011-ITG-21) |
| Contract version | v1 (the /v1 path of each section 12.2 operation) |
| Integration dependencies | RWB-P1-E1011-APP, RWB-P3-E1011-APP, RWB-S5-E1011-APP, RWB-P6-E1011-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-RDF-007, REQ-RDF-008, REQ-CWC-004) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-011 is split and reworked as the integration story RWB-ITG-E1011-ITG, the end-to-end proof of JOB-04 across rwb-source-data, rwb-case, rwb-asset, rwb-comms, rwb-integration and rwb-reporting, with the data lake removed. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (34 resolved, 39 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **test engineer in the release squad (RW-TRIBE), with the data steward (RW-DATASTEW) as the reader of the result**, I want **the five daily reconciliations REC-01 to REC-05 of JOB-04 proved end to end in SIT against the real wave-1 services — started by the AceDataReady event on the rwb-source-data workflow, reading its own ACE views, taking open case accounts and exclusions from rwb-case, asset keys from rwb-asset and notice person keys from rwb-comms over one-hop contracts, writing the results in rwb_source_data, setting the case-list publish status through the rwb-case contract, and delivering the reconciliation and data quality extracts to rwb-reporting through rwb-integration**, so that **each wave-1 release shows whether today's case list and its links can be trusted before the release date**.

### 2. Business rationale

No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. The legacy capability runs five reconciliations every business date — the account count by product against `v_ace_account` (REC-01), the balance by product (REC-02), approved treatments against `v_ace_plan` (REC-03), payments against proceeds (REC-04), and every business key on a Workbench table against the view that holds it (REC-05) — holds the publish of the case list when a product is outside the tolerance, and publishes the result with the data quality measures.

In the target the capability is spread over the real services, so the legacy story alone cannot prove it: JOB-04 is an event-triggered workflow in rwb-source-data (Arch v5 slide 44), the checks read the ACE views through the owner that holds them (DP-05), the open case accounts and the exclusions come from rwb-case, the asset keys from rwb-asset and the notice person keys from rwb-comms over one-hop REST contracts with a 2 s timeout (DP-11), and the two extracts reach rwb-reporting as delivered files through rwb-integration because the data lake is removed (DP-17, ADR-018). This story builds that integration harness, runs it against the real services instead of the contract fakes, and holds the wave-1 release on its result. It meets REQ-RDF-007, REQ-RDF-008 and REQ-CWC-004, applies control CTL-01, and serves the accuracy measure "reconciliation breaks cleared within one day, 100 percent".

### 3. Preconditions

- RWB-P1-E1011-APP is done: the JOB-04 reconciliation workflow and its activities run on task queue `rwb-source-data`, the results are written in `rwb_source_data`, and the job listing reads them per check and product group.
- RWB-P3-E1011-APP is done: the exclusion resource of the case contract, the open case accounts, and the case-list publish status gate.
- RWB-S5-E1011-APP is done: the asset keys of the business date are published on the rwb-asset contract. RWB-P6-E1011-APP is done: the notice person keys are published on the rwb-comms contract.
- The wave-1 services are deployed in SIT in one environment: rwb-source-data, rwb-case, rwb-asset, rwb-comms, rwb-integration and rwb-reporting, each on its own base `/api/recovery/<short>/v1`, each on its own schema and login (DP-01, DP-02), with the SIT Kafka topics and the Temporal namespace `rwb-recovery` reachable.
- rwb-source-data publishes `rwb.source-data.AceDataReady.v1` for the SIT business date, so the reconciliation workflow can be started by the event rather than by a scheduler.
- The SIT data set carries the synthetic fixture values of the legacy criteria: MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 accounts at 90 days past due or more; the 12 SSME account keys of the break fixture; case "RW-2026-000140" with person_key "P0099881"; and the parameter `recon.tolerance.pct` 0.00 in force for REC-01 and REC-02.
- The reconciliation results are read by rwb-reporting through GET /admin/reconciliation/results on /api/recovery/source-data/v1 (API-P1-003), and SCR-45 Data quality is reachable read-only.
- No data lake path is provisioned in SIT: the legacy INT-19 outbound adapter and the lake copy of the case list are not installed (DP-17).
- Which service runs REC-03 (treatments) and REC-04 (payments) in the target, and how the two extracts reach reporting once the lake is removed, is Not specified in the source documents (GAP-0336; ASM-0430).
- No build dependency: the four integration dependencies are the real services, and the story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. rwb-source-data completes the ALS ingest for business date 2026-11-30, its `AceIngestCheck` workflow confirms freshness over `recovery.v_ace_*`, and it publishes `rwb.source-data.AceDataReady.v1` with source ALS and the business date on `rwb.source-data.events.v1`.
2. The reconciliation workflow starts on task queue `rwb-source-data` from that event, one run per business date, and takes the business date of the event as the date of every check.
3. It reads `v_ace_batch_status` through the ACE views it owns, confirms the ALS batch is complete for the date, and reads `recon.tolerance.pct`, `recon.treatment.days`, `recon.payment.days` and `case.entry.dpd` through the parameters contract (DP-06).
4. REC-01 and REC-02: for each product group it counts and sums `v_ace_account` rows at or above the entry threshold with `data_as_of` equal to the business date, subtracts the accounts excluded at entry, and compares the result with `case_list_row`.
5. Exclusions: it calls the exclusion operation that the rwb-case contract publishes — its exact path is Not specified in the source documents (GAP-0337; ASM-0431) — on rwb-case, one hop with a 2 s timeout; the exclusion rows carry the reason code, the rule ID and the package version, and an excluded account is explained and never a break.
6. Open case accounts: it calls `GET /api/recovery/case/v1/cases` and the account link read of the case contract on rwb-case, one hop with a 2 s timeout, never a table of `rwb_case`.
7. REC-03 and REC-04: treatments and payments are checked against `v_ace_plan` and `v_ace_payment`. In wave 1 the owning services are not in the environment, so both checks report NOT_RUN with their reason; the not-run grade and its reason are the legacy BR10 values and no new business value is introduced.
8. REC-05: every `account_key`, `person_key`, `asset_key`, `payment_code` and `contact_key` on a Workbench table is resolved to its view row. The asset keys come from `GET /api/recovery/asset/v1/assets` on rwb-asset and the notice person keys from `GET /api/recovery/comms/v1/cases/{caseId}/notices` on rwb-comms, one call per case in the run, each one hop with a 2 s timeout; an orphan is listed for the data steward and changes no row.
9. It computes the variance and the variance percent per check and product group, compares them with the tolerance, and writes one `reconciliation_result` row per check and product group in one transaction, unique on rec_code, business_date and product_group.
10. Publish gate: it calls the case-list publish contract of rwb-case, which sets the publish status of the business date to RELEASED when every REC-01 and REC-02 result is PASS and to HELD when any is BREAK; the case-list publish gate reads `GET /reconciliation/status` on rwb-case for the business date, which returns RELEASED, HELD, or NOT_RUN when the run has not completed, together with the unexplained exclusion count per product group, and the gate releases or holds the case list on that answer; the run alerts the data steward, the platform administrator and the team managers with MSG-P1-012 on a break.
11. Extracts: it writes the reconciliation extract and the data quality extract and asks rwb-integration for a delivery; rwb-integration runs the `deliverFile` activity on task queue `rwb-integration`, records the file run in `rwb_integration`, and publishes `rwb.integration.FileDelivered.v1` for each file.
12. rwb-reporting reads the two delivered files and the business events of the date and builds the report; at 07:30 the report shows each product as green, red or not run, the variance, the break rows, the referential completeness and the quality measures.
13. The harness: publishes the event, waits for the workflow, asserts the results and the publish status, reads the two files from the outbound item record, reads the report, and records one verdict per test case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product's variance is above the tolerance | Result BREAK; red on the report; publish held; break rows listed; alert | MSG-P1-012 | AC2, AC15 |
| X2 | The variance equals the tolerance | Result PASS | None | AC3 |
| X3 | The ACE batch for the business date is not COMPLETED | No reconciliation result for the date; the report shows not run with the reason; the publish stays held | MSG-P1-001 | AC4 |
| X4 | The run repeats for the same date after a fix | The date's results are replaced; the publish is released when every REC-01 and REC-02 result passes | None | AC15 |
| X5 | The same event is delivered twice | One row per check, product group and date; no second run and no second row | None | AC12 |
| X6 | A business key has no ACE row | REC-05 is BREAK with the orphan count and the key is listed; no Workbench row changes | None | AC7 |
| X7 | A view or a store returns an error during the run | No result is written for the date; the run is FAILED with the system named | MSG-GEN-006 | AC17 |
| X8 | A role without Platform administration R lists the break rows | 403 | MSG-P4-002 | AC18 |
| X9 | A cross-service read exceeds the 2 s budget | The step fails as a timeout, no result is written for the date, and the rerun writes every row | MSG-GEN-006 | AC13 |
| X10 | A file delivery fails | rwb-integration publishes `rwb.integration.FileFailed.v1`; the run records the failed file run; the delivery is retried from the outbound item | None | AC14 |
| X11 | REC-03 or REC-04 has no owning service in the environment | The check reports NOT_RUN with its reason; the report shows not run; the archive of the day records no PASS for that check | None | AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Proves behaviour that already exists in the four integration dependencies; builds no product capability and changes no case |
| Negotiable | The fixture values, the file names and the harness settings are configuration; the checks, the tolerance rule and the publish gate are fixed by the legacy story |
| Valuable | A release cannot claim the wave-1 reconciliation works until the real services pass the run together, which no single service story can show |
| Estimable | One harness, one event driver, six read checks, two extract checks, one publish check |
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
    Given rwb-source-data returns accounts at 90 days past due or more less the exclusions as MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903
    Given the case list rows at 90 days past due or more are MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903, with equal balance sums
    Given rwb-source-data returns no restructure plan overdue, no payment of the date unmatched, and every business key resolving to its row
    When the reconciliation workflow runs
    Then the system writes fifteen reconciliation_result rows, REC-01 to REC-05 for each of the three product groups, each with variance 0 and result PASS
    Then the system sets the publish status of the case list for 2026-11-30 to RELEASED
    Then the report after the 07:30 refresh shows all three products green

  Scenario: AC2 Variance over limit (legacy RWB-E1-011 AC2)
    Given rwb-source-data returns 2,903 SSME accounts at 90 days past due or more less the exclusions
    Given the case list holds 2,891 SSME rows at 90 days past due or more, a variance of 12 accounts, 0.41 percent
    When the reconciliation step runs
    Then the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    Then the 12 account keys are on the break list for the data steward, with their days past due from v_ace_account
    Then the system sets the case list publish for 2026-11-30 to HELD and the lake keeps the case list of 2026-11-27
    Then the data steward, platform administrator and team manager groups receive MSG-P1-012 "The case list for 2026-11-30 does not reconcile to ACE for SSME: a difference of 12 accounts, 0.41 percent."
    Then the report shows SSME red with the 12 break rows, and MORTGAGE and HIRE_PURCHASE green

  Scenario: AC3 Variance equal to the tolerance (legacy RWB-E1-011 AC3)
    Given the parameter recon.tolerance.pct for REC-01 is changed by a reference load to 0.10 from 2026-11-30
    Given the MORTGAGE variance is 0.10 percent and the SSME variance is 0.11 percent
    When the reconciliation step runs
    Then the MORTGAGE result is PASS and the SSME result is BREAK

  Scenario: AC4 ACE batch not complete (legacy RWB-E1-011 AC4)
    Given rwb-source-data shows no COMPLETED ALS row for 2026-11-30 at 08:00
    When the DP01 cut-off passes and the reconciliation workflow is triggered
    Then the daily completeness gate holds the reconciliation workflow and the system writes no reconciliation_result for 2026-11-30
    Then the case list publish for 2026-11-30 stays HELD
    Then the report shows every product as not run with the reason "DP01 is from 2026-11-27"

  Scenario: AC7 Business key without an ACE row (legacy RWB-E1-011 AC7)
    Given case_party on case "RW-2026-000140" carries person_key "P0099881", which has no customer row in the rwb-source-data data
    When the REC-05 step runs
    Then the REC-05 result for the product group of the case is BREAK with 1 orphan
    Then "case_party.person_key P0099881" is on the break list for the data steward and the ACE team
    Then the case and its case_party row are unchanged

  Scenario: AC12 JOB-04 starts on AceDataReady and writes one result per check and product group (new, D-RCV-60)
    Given rwb-source-data publishes rwb.source-data.AceDataReady.v1 for source ALS and business date 2026-11-30
    When the reconciliation workflow starts
    Then it is an event-started workflow on task queue rwb-source-data, one run for the business date
    Then it uses the business date of the event for every check and never a mix of two business dates
    Then it computes REC-01 to REC-05 and writes one reconciliation_result row per check and product group in one transaction, REC-01 to REC-05 for each of the three product groups
    Then reconciliation_result holds unique rec_code, business_date and product_group, so a second delivery of the event writes no second row
    Then REC-03 and REC-04 report NOT_RUN with their reason until rwb-treatment and rwb-payment land in wave 2, using the not-run grade and the reason of legacy BR10 and no new status value

  Scenario: AC13 Every cross-service read is one hop on the owner's contract (new, D-RCV-60)
    Given the reconciliation workflow is running for 2026-11-30
    When it needs the open case accounts and the exclusions of the date
    Then it calls rwb-case on GET /api/recovery/case/v1/cases and on the exclusion operation of the case contract, whose exact path is Not specified in the source documents (GAP-0337; ASM-0431)
    When it needs the asset keys and the notice person keys for REC-05
    Then it calls rwb-asset on GET /api/recovery/asset/v1/assets and rwb-comms on GET /api/recovery/comms/v1/cases/{caseId}/notices for the cases in the run
    Then every call is one hop with a 2 s timeout and no call is chained through a second service
    Then no service reads a table of rwb_source_data
    Then a read that exceeds the 2 s budget fails the step and the date is rerun

  Scenario: AC14 The two extracts reach rwb-reporting and no data lake path exists (new, D-RCV-60)
    Given the reconciliation run for 2026-11-30 has finished with its results
    When the workflow publishes the reconciliation extract and the data quality extract
    Then rwb-integration delivers both files through the deliverFile activity on task queue rwb-integration
    Then rwb-integration records the file run in rwb_integration and publishes rwb.integration.FileDelivered.v1 for each file
    Then rwb-reporting reads both delivered files and builds the report of the date from them
    Then the case-side result reaches rwb-reporting through the read operations of rwb-case on one Schedule with SKIP overlap and a catch-up window whose cron is Not specified in the source documents (GAP-2238), with the three alert groups as configuration and a feature flag whose name is Not specified in the source documents (GAP-2238)
    Then no data lake path, no INT-19 adapter and no lake copy of the case list exists in the environment

  Scenario: AC15 A REC-01 or REC-02 break holds the publish and a passing rerun releases it (new, D-RCV-60)
    Given the REC-01 result for SSME is BREAK with variance 12 and variance percent 0.41
    When the workflow sets the publish status of the case list for 2026-11-30
    Then the status is set by the rwb-case case-list publish contract call and reads HELD
    Then the reconciliation extract carries the 12 break rows and MSG-P1-012 is sent to the data steward, platform administrator and team manager groups
    When the rerun for 2026-11-30 replaces the results and every REC-01 and REC-02 result is PASS
    Then the same contract call sets the publish status to RELEASED
    Then the case list of 2026-11-30 is the one that rwb-reporting reports for the date

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

  Scenario: AC19 REC-03 and REC-04 do not judge breaks until their owners land (new, D-RCV-60)
    Given rwb-treatment and rwb-payment are not in the environment
    When the reconciliation workflow runs for 2026-11-30
    Then REC-03 reports NOT_RUN with its reason and no approved restructure plan is judged a break under the parameter recon.treatment.days
    Then REC-04 reports NOT_RUN with its reason and no payment with unmatched proceeds is judged a break under the parameter recon.payment.days
```

The five scenarios AC1, AC2, AC3, AC4 and AC7 are the legacy proof of RWB-E1-011 and keep its expected results, with source reads stated through rwb-source-data and the job named as the reconciliation workflow; the data lake they name is removed (DP-17) and the target delivery is proved by AC14, and the wave-1 run reports REC-03 and REC-04 as NOT_RUN per AC12 until rwb-treatment and rwb-payment land, so the fifteen PASS rows of AC1 are recorded when they do. No scenario uses a contract mock: the run is against the real service contracts.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Accounts at or above the entry threshold in `v_ace_account` for the business date are compared with open recovery cases and the case list rows, by count per product group, every business date | REC-01; CTL-01; REQ-RDF-007 |
| BR2 | Balances in `v_ace_account` are compared with the balances on the case list rows, by sum per product group | REC-02 |
| BR3 | An approved restructure treatment whose plan is not booked in `v_ace_plan` two business days after approval is a break | REC-03; parameter recon.treatment.days |
| BR4 | A payment in `v_ace_payment` with no proceeds matched to its `payment_code` one business day after the payment date stays on the exception list and counts as a break | REC-04; parameter recon.payment.days |
| BR5 | Every `account_key`, `person_key`, `asset_key`, `payment_code` and `contact_key` on a Workbench table must resolve to a row in `v_ace_account`, `v_ace_customer`, `v_ace_asset`, `v_ace_payment` or `v_ace_contact`; zero orphans, and every one is listed | REC-05; REQ-RDF-007 |
| BR6 | A result is a break when the variance percent is above the tolerance; REC-03 and REC-04 use their waiting periods and a zero tolerance | Parameter recon.tolerance.pct, 0.00 assumed and confirmed (DL25; ASM-0728, ASM-0735, ASM-0743, ASM-2602) |
| BR7 | A break in REC-01 or REC-02 holds the publish of the case list for the business date and lists the break rows for the data steward | FEAT-RDF-13; REC-01 "Break list to the data steward" |
| BR8 | Accounts excluded at entry are explained and do not count as breaks | REC-01 "zero unexplained"; REQ-CWC-004 |
| BR9 | No reconciliation runs until the daily completeness gate reports COMPLETE for the sources the reconciliation reads on the business date | BR-P1-014-4; MSG-P1-001 |
| BR10 | Report grades: green, every reconciliation for the product passed; red, at least one break; not run, the reconciliation did not run, with the reason | FEAT-RDF-12 |
| BR11 | A repeated run for the same date replaces that date's results | R-UNI-40 |
| BR12 | The reconciliation reads ACE for the business date of the ACE batch it was started by, and never a mix of two business dates | BR-P1-011-2 |
| BR13 | A REC-05 orphan never deletes or changes a Workbench record; it is listed for the data steward and, where the row is missing in ACE, for the ACE team | BR-P1-011-3 |
| BR14 | Every cross-service read is one hop on the owner's contract with a 2 s timeout; the reconciliation reads open case accounts and exclusions from rwb-case, asset keys from rwb-asset and notice person keys from rwb-comms, and reads no other service's tables | DP-01; DP-11; ADR-020 |
| BR15 | There is no data lake: the reporting read model is fed by the business events and by the files rwb-integration delivers, so a lake copy of the case list or of an extract is neither written nor read | DP-17; ADR-018; Arch v5 slides 37 and 44 (JOB-15) |

### 9. State transitions

None for a case status. This story changes no case. It proves the status of `reconciliation_result` (PASS, BREAK or NOT_RUN, with NOT_RUN and its reason as legacy BR10 defines them) and of `case_list_row.publish_status` (HELD or RELEASED) for the business date.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login, DP-02) | Runs the reconciliation workflow, writes `reconciliation_result`, sets the publish status through the rwb-case contract, and asks rwb-integration for the delivery |
| rwb-treatment (S2) and rwb-payment (P8) | Own the Workbench side of REC-03 and REC-04 respectively when they enter wave 2; until then both checks report NOT_RUN with the BR10 not-run reason, as no S2 or P8 slice exists yet |
| rwb-case, rwb-asset and rwb-comms service identities | Answer the one-hop reads of the run; no write in this story |
| rwb-integration service identity | Runs `deliverFile`, records the file run and publishes the file events |
| RW-TRIBE, release squad and test engineers | Publish the SIT event, run the harness, read the verdicts |
| RW-DATASTEW, data steward and data product owner | Reads the results and the break rows (Platform administration R); signs the daily reconciliation to ACE |
| RW-PLATADM, platform administrator | Reads the results, restarts the run for a business date (Platform administration U) |
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
| DF-ACE-160, DF-ACE-167, DF-ACE-168 | v_ace_plan | ACE view, read by rwb-source-data | plan_ref, account_key, booked_at | Read |
| DF-ACE-043, DF-ACE-044, DF-ACE-045, DF-ACE-046 | v_ace_payment | ACE view, read by rwb-source-data | payment_code, account_key, payment_date, payment_amount | Read |
| DF-ACE-056 | v_ace_customer | ACE view, read by rwb-source-data | person_key | Read |
| DF-ACE-100 | v_ace_asset | ACE view, read by rwb-source-data | asset_key | Read |
| DF-ACE-075, DF-ACE-076 | v_ace_contact | ACE view, read by rwb-source-data | contact_type, contact_key | Read |
| DF-ACE-178, DF-ACE-179, DF-ACE-186 | v_ace_batch_status | ACE view, read by rwb-source-data | source_system, business_date, is_complete | Read |
| DF-RPT-002, DF-RPT-005, DF-RPT-006, DF-RPT-007 | case_list_row | rwb_source_data (P1) | business_date, account_key, account_no, product_group | Read |
| DF-RPT-014, DF-RPT-015 | case_list_row | rwb_source_data (P1) | total_balance, days_past_due | Read |
| DF-RPT-019 | case_list_row | rwb_source_data (P1) | publish_status (HELD or RELEASED) | Read, set through the rwb-case case-list publish contract |
| DF-CAS-057, DF-CAS-058 | case_entry_exclusion | rwb_case (P3) | account_key, business_date | Read through the rwb-case contract |
| DF-CAS-026 | case_account | rwb_case (P3) | account_key | Read through the rwb-case contract |
| DF-CAS-032, DF-CAS-004 | case_party, recovery_case | rwb_case (P3) | person_key, primary_person_key | Read through the rwb-case contract |
| DF-TRT-002, DF-TRT-004, DF-TRT-007, DF-TRT-011, DF-TRT-012, DF-TRT-013 | treatment | rwb_treatment (S2) | case_id, treatment_type, offer_amount, approval_level, booked_at, outcome | Read through the rwb-treatment contract when it lands (REC-03) |
| DF-FIN-002, DF-FIN-004, DF-FIN-006, DF-FIN-008 | proceeds | rwb_payment (P8) | case_id, payment_code, amount, matched_to | Read through the rwb-payment contract when it lands (REC-04) |
| DF-SAL-002, DF-SAL-010, DF-SAL-033 | listing, asset_sale, debt_sale_account | rwb_asset (S5), rwb_debtsale (S6) | asset_key, account_key | Read through the owner's contract |
| DF-LEG-030 | notice | rwb_comms (P6) | person_key | Read through the rwb-comms contract |
| DF-INT-003, DF-INT-022 | interaction | rwb_source_data (P1) | person_key, contact_key | Read by rwb-source-data |
| DF-DOC-003, DF-DOC-100 | document, signature_request | rwb_document (P5) | person_key | Read through the rwb-document contract |
| DF-OPS-118 to DF-OPS-129 | reconciliation_result | rwb_source_data (P1) | id, rec_code, business_date, product_group, source_count, workbench_count, source_amount, workbench_amount, variance_count, variance_pct, tolerance_pct, result | Write by rwb-source-data; read by the harness through the P1 job listing |

Field IDs are those in the Logical Data Model and Data Dictionary. Criteria and tests read the ACE views only through rwb-source-data (DP-01), never directly, and cite the reconciliation_result rows and the P1 job listing, not the legacy job or decision-log wording. The harness reads and writes nothing directly: every field above is read through the owning service's contract or through the rwb-source-data views and job listing (DP-01, DP-05). `case_list_row` is P1's daily published projection and the case-list API and the publish gate stay with P3 under the Ownership Map ruling; `publish_status` is therefore set by the rwb-case contract call and never written by the harness.

### 12. Contract

#### 12.1 REST operations provided

None. This story builds and runs an integration harness and publishes no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the run | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/freshness` | P1 rwb-source-data | Batch completeness of the business date before the run | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/admin/jobs?type=JOB-04` | P1 rwb-source-data | Run record: REC-01 to REC-05 with PASS, BREAK or NOT_RUN per product group and the publish status | One hop, 2 s |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Open case accounts and the case list of the date | One hop, 2 s |
| GET | `/api/recovery/case/v1/exclusions?businessDate={businessDate}` | P3 rwb-case | Accounts excluded at entry, for REC-01; this is the operation the rwb-case contract of RWB-P3-E1011-APP must publish, because its exact path is not named in the Ownership Map or the Architecture extract | One hop, 2 s |
| GET | `/api/recovery/asset/v1/assets` | S5 rwb-asset | Asset keys for REC-05 | One hop, 2 s |
| GET | `/api/recovery/comms/v1/cases/{caseId}/notices` | P6 rwb-comms | Notice person keys for REC-05, one call per case in the run | One hop, 2 s |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The two delivered files and their file runs | One hop, 2 s |
| GET | `/api/recovery/reporting/v1/reports/{reportId}` | P9 rwb-reporting | The report of the date, read only | One hop, 2 s |

The workflow itself performs the reads of rows 3 to 6 inside its activities; the harness calls them in the same way and fails the run when one of them exceeds the budget. The exact exclusion operation of the case contract is Not specified in the source documents (GAP-0337; ASM-0431); the path above is the one the P3 E1011 contract must publish.

#### 12.3 Events published

| Event | Topic | Owner | Asserted in the run |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | One per extract, with the file reference, the business date and the requesting service |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | Asserted on the forced failure path only |

Both are published by rwb-integration, not by the harness; the story asserts them, and every event carries IDs, references and facts only (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner | Asserted in the run |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | The trigger of the reconciliation workflow, with source ALS and the business date |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 | The case that appears after the missing accounts are created for the rerun of AC15 |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 | The state change of that case, so the rerun reads a consistent case list |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Asserted in the run |
|---|---|---|---|
| `reconciliation` (JOB-04) | Workflow, started by AceDataReady | `rwb-source-data` | One run per business date, the event's business date used for every check, one transaction for the results |
| REC-01 to REC-05 check activities | Activities | `rwb-source-data` | Each check reads its own views and the owner contracts, and returns its result and its break rows |
| Publish status step | Activity | `rwb-source-data` | Calls the rwb-case case-list publish contract and records HELD or RELEASED |
| `deliverFile` | Activity | `rwb-integration` | Delivers the two extracts and records the file run |

#### 12.6 Schedules

| Schedule or trigger | Cadence | Asserted in the run |
|---|---|---|
| AceDataReady trigger | On the ACE batch of the business date, with a Temporal Schedule fallback and overlap policy SKIP | The event starts the workflow once per business date; a redelivered event starts no second run |
| Reporting refresh | Daily at 07:30, owned by rwb-reporting | The report of the date is rebuilt after the extract delivery and shows the grades of the run |

#### 12.7 Tables owned

None. The harness owns no table (DP-01); `reconciliation_result` and `case_list_row` belong to rwb-source-data, `case_entry_exclusion` to rwb-case, and the harness reads every one of them through the owning contract.

#### 12.8 Contract fakes

None. The run replaces the contract fakes with the deployed SIT services; a fake used anywhere in the run fails the story. No contract fake library version is recorded as published; none is required.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed; every call one hop on the owner's base with a 2 s timeout |
| Kafka | 0 published, 3 consumed and 2 asserted; the harness publishes AceDataReady for the SIT date and asserts the two rwb-integration file events |
| Temporal | 1 workflow and its check activities on `rwb-source-data`; `deliverFile` on `rwb-integration` |
| File | 2 files delivered, the reconciliation extract and the data quality extract, read back through the outbound item record |

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

The story carries no H, C, I or X dependency beyond the four integration dependencies, because the harness builds nothing: DP-03 resolves to reading decision records the services write, DP-06 and DP-07 to reading parameters and reference data through the deployed contracts, DP-10 to observing the workflow that RWB-P1-E1011-APP owns, DP-14 to asserting the names, DP-15 to reading the schemas of the DB stories, DP-17 to asserting that no lake path exists, and DP-19 to reading the report and SCR-45 read-only through gateway-bff. The H dependencies of these patterns stay with the implementation stories of the owning services.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| EventDriver | Test harness | Publishes `rwb.source-data.AceDataReady.v1` for the SIT business date through the SIT topic and waits for the workflow to complete |
| WorkflowProbe | Test harness | Asserts one run per business date on queue `rwb-source-data`, the workflow type and the business date input |
| ContractProbe | Test harness | Calls the eight consumed operations on the owner's base with the 2 s budget, and records status, time and body |
| ResultAssertion | Test harness | Compares the run record and the result read model with the expected grades, variances and row count of the fixture |
| ExtractAssertion | Test harness | Reads the two extracts from the outbound item record and compares the rows with the run |
| PublishAssertion | Test harness | Asserts HELD on the break run and RELEASED on the passing rerun |
| FixtureLoader | Test harness | Loads the synthetic SIT fixture values of the legacy criteria; holds no production data |
| ReportProbe | Test harness | Reads the report of the date, and SCR-45 read-only, through gateway-bff |

**Topology and fixtures**

- One SIT environment: the six wave-1 services, one ACE SIT database with one schema and one login per service (DP-01, DP-02), the SIT Kafka topics, the Temporal namespace `rwb-recovery` with one task queue per service, and no data lake (DP-17).
- Synthetic fixtures only: MORTGAGE 12,256, HIRE_PURCHASE 12,960 and SSME 2,903 accounts at 90 days past due or more with equal balance sums for AC1; 2,891 SSME case list rows and the 12 missing account keys for AC2; the tolerance 0.10 load for AC3; no COMPLETED ALS row for AC4; case "RW-2026-000140" with person_key "P0099881" absent from `v_ace_customer` for AC7; 2,903 SSME accounts against 2,891 rows for AC15.
- The fixture loader seeds only through the SIT data set and the SIT topics; it never writes a service table and never calls a production endpoint.

**Run order**

1. FixtureLoader loads the fixture set and the parameters of the date.
2. ContractProbe confirms that the six wave-1 services answer on their own base and that no service reads another schema.
3. EventDriver publishes AceDataReady for 2026-11-30; WorkflowProbe registers the run and its start type.
4. The run completes; ResultAssertion reads the run record and asserts the row count and the grades of REC-01 to REC-05.
5. PublishAssertion reads HELD on the break fixture and asserts the MSG-P1-012 alert of the break.
6. ExtractAssertion reads the reconciliation extract and the data quality extract from the outbound item record and compares them with the run.
7. rwb-integration publishes `rwb.integration.FileDelivered.v1` for both files; the assertion records the two deliveries.
8. ReportProbe reads the report of the date after the 07:30 refresh and SCR-45 read-only.
9. The missing accounts are created, the run is repeated, and PublishAssertion asserts RELEASED with every REC-01 and REC-02 result PASS.
10. The harness writes one verdict per test case of section 16 and fails the release stage on any FAIL.

**Build steps**

1. EventDriver and WorkflowProbe with the SIT topic, the inbox dedupe assertion and the one-run-per-date assertion; tests for AC12.
2. ContractProbe over the eight operations with the 2 s budget and the timeout path; tests for AC13.
3. ResultAssertion for the fifteen-row, unique-key and NOT_RUN behaviour of the run record; tests for AC12 and AC1.
4. FixtureLoader with the legacy fixture values of section 13 and the parameter loads of AC3; no production value.
5. PublishAssertion with the HELD, RELEASED and alert assertions; tests for AC15 and AC2.
6. ExtractAssertion with the two extracts and the outbound item record; tests for AC14.
7. ReportProbe with the report and SCR-45 reads, and the no-lake-path assertion.
8. Add the stage to the release pipeline before the wave-1 exit and run it once on the wave-1 build.

**Done when.** The thirteen test cases of section 16 pass against the SIT wave-1 services, the run shows fifteen `reconciliation_result` rows with their grades, both extracts are read in rwb-reporting, the publish status reads HELD on the break and RELEASED after the rerun, and no data lake path exists in the environment.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-012 | A product breaks the tolerance | The case list for {date} does not reconcile to ALS for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-P1-001 | The ACE batch is not complete; reconciliation not run | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A view, a contract call or the store is unavailable during the run | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness verdicts are for the release team and are not part of the message standard; the business messages above are the legacy texts, copied unchanged.

### 15. Screens and states

No Workbench screen is built in this story. Two existing surfaces are exercised read-only through gateway-bff (DP-19): the reconciliation results read through GET /admin/reconciliation/results on /api/recovery/source-data/v1 (API-P1-003) by rwb-reporting, showing the state of the run (green, red or not run per product, with the break rows and the referential completeness), and SCR-45 Data quality, read in its list state to confirm the same breaks are visible to the data steward. The harness changes no screen state and takes no screenshot. SCR-45 states (AC16): loading as Screen Specifications v1 gives it; error shows MSG-GEN-006 and no access shows MSG-P4-002; the empty state text is Not specified in the source documents (CG-ALL-192).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-011-07-ITG | Access | Component | RW-CASEOWN calls the job listing of the run; refused with MSG-P4-002 |
| TC-E1-011-01-ITG | AC1, BR1, BR2, BR5, BR8, BR10 | End to end | Read through rwb-source-data: accounts MORTGAGE 12,256, HIRE_PURCHASE 12,960, SSME 2,903 with exclusions; clean REC-03, REC-04 and REC-05 |
| TC-E1-011-02-ITG | AC2, BR6, BR7 | End to end | 12 SSME accounts missing from the case list |
| TC-E1-011-03-ITG | AC3, BR6 | Integration | Tolerance 0.10; variances 0.10 and 0.11 percent |
| TC-E1-011-04-ITG | AC4, BR9, BR10 | Integration | No COMPLETED ALS row for 2026-11-30 |
| TC-E1-011-05-ITG | AC5, BR11 (run by RWB-P1-E1011-APP) | Integration | Break, missing cases created, restart |
| TC-E1-011-06-ITG | AC6, BR11 (run by RWB-P1-E1011-APP) | Integration | Two reconciliation workflow runs for the same date on two nodes |
| TC-E1-011-08-ITG | AC7, BR5, BR13 | Integration | case_party person_key P0099881 absent from the rwb-source-data customer data |
| TC-E1-011-09-ITG | AC8, BR12 (run by RWB-P1-E1011-APP) | Integration | rwb-source-data returning an error after the MORTGAGE count |
| TC-ITG-E1011-01 | AC12, BR9, BR11, BR12 | Integration | AceDataReady for 2026-11-30; a redelivery of the event; three product groups; REC-03 and REC-04 NOT_RUN |
| TC-ITG-E1011-02 | AC13, BR14 | Integration | The three one-hop reads with a 2 s budget; a forced 3 s answer on rwb-comms; a schema check that no service reads rwb_source_data |
| TC-ITG-E1011-03 | AC14, BR15 | Integration | Two extracts; the outbound item record; `rwb.integration.FileDelivered.v1` for each file; a forced `rwb.integration.FileFailed.v1`; no lake path in the SIT inventory |
| TC-ITG-E1011-04 | AC15, BR7 | End to end | The 12-account break run, then the missing cases created and the passing rerun |
| TC-ITG-E1011-05 | §12 operations, events and activities | Integration | Contract test of each §12 operation, event and activity against its published service contract; no contract fake |
| TC-ITG-E1011-06 | AC16 | Component | SCR-45 with no reconciliation rows, while loading, on a failed read, and for a role without Platform administration R |
| TC-ITG-E1011-07 | AC17 | Integration | A view returns an error during the run for 2026-11-30; no result written; run FAILED |
| TC-ITG-E1011-08 | AC18 | Integration | Role RW-CASEOWN without Platform administration R lists the break rows; 403 with MSG-P4-002 |
| TC-ITG-E1011-09 | AC19, BR3, BR4 | Integration | rwb-treatment and rwb-payment absent from the environment; REC-03 and REC-04 NOT_RUN with reason |

The nine legacy test cases are carried as integration copies in the order of the WP and keep the legacy IDs with the `-ITG` suffix, the legacy Covers and the legacy data; the legacy level System maps to Integration, and Access to Component. The legacy acceptance criteria not owned here (AC5, AC6 and AC8) are owned by RWB-P1-E1011-APP and are re-exercised only inside the end-to-end run of this story, through TC-E1-011-05-ITG, TC-E1-011-06-ITG and TC-E1-011-09-ITG.

### 17. Guardrails

- No business value in code: the tolerance, the waiting periods, the threshold, the fixture values and the file names are configuration and the SIT data set; the release stage compares them with the parameter values in force.
- No personal data in logs, reports, tests or prompts: break rows carry account keys, account numbers and business keys only, and the fixtures are synthetic.
- No read of another service's tables: every cross-service field comes through the owner's contract, one hop with a 2 s timeout (DP-01, DP-11), and the harness asserts that no service reads a table of `rwb_source_data`.
- ACE data only through rwb-source-data, which owns the `recovery.v_ace_*` views (DP-05); no other service and no harness process opens an ACE view.
- No data lake path: no INT-19 adapter, no INT-20 extract and no lake copy of the case list is installed or read (DP-17).
- The harness runs in SIT only; it never points at UAT or production and never writes a service table.
- A held case list is never released by hand in this story; the rerun through the publish gate is the only release path.
- A failing verdict is never added to an exception list; a limit that must change is changed in the service story that owns it.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-007 | Case list reconciles daily to the count in v_ace_account with no variance, and every business key resolves to an ACE row | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-11, FEAT-RDF-13, FEAT-RPT-05 | All recovery processes | REC-01; REC-02; REC-05; CTL-01; R-UNI-40 | TC-E1-011-01-ITG, TC-E1-011-02-ITG, TC-E1-011-08-ITG, TC-ITG-E1011-01, TC-ITG-E1011-02 |
| REQ-RDF-008 | Reconciliation breaks and referential completeness are reported to the data product owner | Epic 1, 3.1 and 3.8; Program, 5.1 | FEAT-RDF-12, FEAT-RPT-09 | 15 Manage performance, data and AI | REC-03; REC-04; REC-05; CTL-01 | TC-E1-011-01-ITG, TC-E1-011-02-ITG, TC-E1-011-04-ITG, TC-ITG-E1011-01, TC-ITG-E1011-03, TC-ITG-E1011-04 |
| REQ-CWC-004 | Exclusion rules as data | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 Take over the case at 90 days past due | None | TC-E1-011-01-ITG, TC-ITG-E1011-02 |

### 19. Out of scope

- The build of the JOB-04 workflow, the checks and the results (RWB-P1-E1011-APP), its contract baseline (RWB-P1-E1011-CON) and its deployment, dashboards and runbook (RWB-P1-E1011-OPS).
- The exclusion rules, the exclusion resource and the exclusion API of rwb-case (RWB-P3-E1011-APP).
- The asset keys of rwb-asset (RWB-S5-E1011-APP) and the notice person keys of rwb-comms (RWB-P6-E1011-APP).
- The remaining reconciliations REC-06 to REC-09: write-offs, assets taken on, the decision log copy and notice barcodes.
- Cross-source case count reconciliation in the reporting module (FEAT-RPT-05 full scope, Epic 2).
- The data quality console SCR-45 and the quality measure definitions (Epic 2 and Epic 8); this story reads them read-only.
- Working a break to closure with an owner and a date, and the release of a held publish by hand (FEAT-RPT-09 full scope, Epic 2).
- The production monitoring of the daily run and its alerts (the platform observability epic).

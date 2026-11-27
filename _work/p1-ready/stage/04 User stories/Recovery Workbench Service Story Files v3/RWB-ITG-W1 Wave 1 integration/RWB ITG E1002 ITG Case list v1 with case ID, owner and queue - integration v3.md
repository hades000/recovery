# RWB-ITG-E1002-ITG Case list v1 with case ID, owner and queue — integration

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes**

- Re-scoped to the case list held by rwb-case (`GET /cases`) with account data from the rwb-source-data account-page read; `case_list_row`, `CaseListBuildWorkflow`, `DailyCaseList`, the publish status and the delivered extract are removed (RD-P1-024; findings #1, #3).
- Start chain through the readiness call, event key and payload, late path and freshness path aligned (RD-P1-003, RD-P1-040, RD-P1-041; #4 to #7).
- Parameter `recon.tolerance.pct`; no contract fake; contract 5.1.0 (RD-P1-028, RD-P1-042, RD-P1-005; #8, #9, #11).
- Pending: account-page read path (GAP-3274), rwb-case key-list path (GAP-3273) (#2, #10).
- Finishing pass: test case IDs of Test Cases v9 cited in place of the placeholders.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1002-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-16); the squad sizes the story at refinement |
| Patterns applied | DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P1-E1002-APP, RWB-P1-E1015-APP, RWB-P1-E1011-APP, RWB-P3-E1002-APP, RWB-P3-E1018-APP, RWB-P3-E1020-APP |
| Contract dependencies | RWB-P1-E1015-CON (freshness, readiness and account-page read), RWB-P3-E1042-CON, RWB-P3-E1043-CON (the published contracts the suite builds against; the build dependencies stay with the implementation stories, §13) |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P3-E1020-APP, RWB-P1-E1002-APP, RWB-P1-E1015-APP, RWB-P1-E1011-APP, RWB-P3-E1002-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |
| Contract version | rwb-source-data.yaml 5.1.0, rwb-case.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-002, RD-P1-003, RD-P1-005, RD-P1-024, RD-P1-028, RD-P1-040, RD-P1-041, RD-P1-042 |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-002 is split and reworked as the wave-1 integration story RWB-ITG-E1002-ITG, which proves the case list end to end across rwb-case, rwb-source-data, rwb-integration, rwb-reporting and the gateway-bff composite route for SCR-02, with the removed data lake replaced by the delivery of the daily extract to rwb-reporting. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1002-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3; case list re-scoped to rwb-case, start chain and interface with rwb-source-data aligned.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **the case list proved end to end on the real wave-1 services — the open cases with their owner and queue read from the case list of rwb-case, the account columns read from rwb-source-data through its published account-page read, the freshness of the ACE data shown from the rwb-source-data stamp, and SCR-02 served by the gateway-bff composite route**, so that **the one list every team works from is dated to the ACE batch it was built from and is proven against the services that will run it, not against a fake**.

### 2. Business rationale

The legacy story RWB-E1-002 built one case list each business date from the open cases through the P3 in-process interface `CaseQueryApi`, joined it to the ACE account view and published it to Power BI through a file on the data lake (INT-19). In Arch v5 the single recovery schema and the in-process call are gone: rwb-case holds and serves the list, rwb-source-data is the only service that reads the `recovery.v_ace_*` views (DP-05), and the data lake and its Power BI connection are removed (DP-17; ADR-018). The list is still needed — it is the one list every team works from — so the behaviour has to be proved somewhere on the real services, and that is this story.

The chain the story proves has one owner per step. Airflow calls `POST /business-days/{date}/ready` on rwb-source-data; `AceIngestCheck` stamps the freshness and publishes `rwb.source-data.AceDataReady.v1` per source system and business date on `rwb.source-data.events.v1`; rwb-case starts its daily case run on the event with `sourceSystem` ALS and `status` COMPLETED, creates and allocates the cases, and serves the list on `GET /api/recovery/case/v1/cases`, reading the account columns from rwb-source-data through the account-page read and the freshness answer, one hop with a 2 s timeout (DP-11). rwb-source-data holds no case list. The reporting read model is built by rwb-reporting from `rwb.case.events.v1`; no extract file is written and no lake is used (DP-17). SCR-02 is served by the gateway-bff composite route on the rwb-case base (DP-19).



The parameters and reference data the services read are the rwb-case contracts (DP-06, DP-07), the topic and event names come from the naming library (DP-14), and the account and arrears facts come from the ACE views read by rwb-source-data alone (DP-05). The read operations of the list are `GET /api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/queues/{queueId}/cases` on the rwb-case base (GAP-0335; RD-P1-024).

### 3. Preconditions

- RWB-P3-E1018-APP is done: rwb-case creates the case, the case account link and the number, `recovery_case`, `case_account` and `case_party` exist in schema `rwb_case`, and `GET /api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/cases/{caseId}` answer from it.
- RWB-P3-E1020-APP is done: the morning allocation sets the owner and the queue on each case and publishes `rwb.case.CaseAllocated.v1`, so the list has an owner and a queue to show.
- RWB-P1-E1002-APP is done: rwb-source-data answers the account-page read (account number, product, total balance, days past due, last contact time, last action code and `dataAsOf` for a page of account keys of a business date), published in RWB-P1-E1015-CON. Pending: path and maximum keys per call, owner solution architect (GAP-3274).
- RWB-P3-E1002-APP is done: the case list read operations of rwb-case, including `GET /api/recovery/case/v1/queues/{queueId}/cases`, are published and answer with the owner, the queue, the stage, the status, the route and the refresh fields.
- RWB-P1-E1015-APP is done: `AceIngestCheck`, the freshness stamp, `GET /data-products/freshness`, `AceDataReady` and `AceDataLate` run in SIT; RWB-P1-E1011-APP is done for the REC-01 and REC-05 assertions.
- RWB-P3-E1002-APP also provides the morning Schedule `rwb-case-caselist-daily` and the feature flag `rwb.p1.case-list`, which is on.
- rwb-reporting consumes `rwb.case.events.v1` and builds its own read model in schema `rwb_reporting`.
- The gateway-bff composite route for SCR-02 is deployed in SIT (DP-19, RWB-PLT-N001-CON), with the 2 s per-call timeout, and every service-to-service call of the list read is one hop.
- An SIT data set holds open cases and masked synthetic ACE data for a business date behind the real rwb-source-data, with at least the 28,156 linked account keys of the legacy fixture available to the run.
- The parameters `case.entry.dpd` = 90, `recon.tolerance.pct` = 0.00 and `caselist.allocation.wait.until` = 07:15 are in force through the rwb-case parameters contract, owned by RW-COE.
- Every service is the real SIT service behind its own login: no contract fake stands in for a service in this suite.
- No build dependency: the story is Day 1 by rule (Template and Rules §R5.7) and waits only for the integration dependencies above.

### 4. Flow

1. Test harness: calls `POST /api/recovery/source-data/v1/business-days/2026-11-30/ready` as Airflow does, with a UUID `Idempotency-Key`; the answer is 202 with status RUNNING.
2. rwb-source-data: `AceIngestCheck` (workflow ID `ace-ingest-check-2026-11-30`) reads the ACE batch status, writes the freshness stamps and, in the same transaction, the outbox row of `rwb.source-data.AceDataReady.v1` for each COMPLETED source (key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt`).
3. rwb-case: on the event with `sourceSystem` ALS and `status` COMPLETED, starts its daily case run, which creates the cases and allocates owner and queue. Events of other source systems start nothing.
4. rwb-source-data: starts `ReconciliationWorkflow` (`recon-2026-11-30`) as a child of `AceIngestCheck` after the ALS stamp; it waits for the rwb-case allocation until `caselist.allocation.wait.until`.
5. gateway-bff: the SCR-02 composite route calls `GET /api/recovery/case/v1/queues/{queueId}/cases` and `GET /api/recovery/case/v1/cases`.
6. rwb-case: reads its open cases and their account keys, then reads from rwb-source-data the freshness answer (`GET /data-products/freshness`) and the account-page read for the keys of the page, each one hop with a 2 s timeout, and answers `CasePage` with `refreshedAt`, `X-Data-As-Of` and the stale flag.
7. 07:15, or the configured wait time: the Schedule `rwb-case-caselist-daily` raises MSG-P1-001 to the team manager group when the date is stale. It writes no list row.
8. rwb-reporting: builds its read model from `rwb.case.events.v1`. No extract file is written and no lake path is called.
9. Assertions: the suite reads the list through the rwb-case contract, the freshness and reconciliation results through the rwb-source-data contract, the reporting read model through the rwb-reporting contract and the SCR-02 route answer; it reads no table directly.
10. Replay: repeats the ready call and redelivers the AceDataReady event; no second run starts and the list holds the same cases.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS batch for the business date is not complete at the cut-off | AceDataLate for ALS at 05:30; the DP01 stamp of the last complete date stays in use and is STALE at 08:00; the list shows the last complete date marked stale; the team manager group is alerted | MSG-P1-001 | AC5 |
| X2 | The allocation step has not completed by 07:15 | The list is served with the owner and the queue as they are | None (shown on the page) | AC1 |
| X3 | The ready call is repeated or the same AceDataReady event is delivered twice | No second run starts, no second event is published for an unchanged batch row and the list is unchanged | None | AC15 |
| X4 | The account-page read fails or passes 2 s while a page is read | rwb-case answers 503 with no partial page; behaviour is proved by RWB-P3-E1002-APP AC8 | MSG-GEN-006 | AC1 |
| X5 | Removed in version 3 (RD-P1-024): no extract is delivered | — | — | — |
| X6 | A case account has no ACE account row for the business date | The list shows the key with empty account number, total balance and days past due; REC-05 lists the key for the data steward and the ACE team; the case and the link are unchanged | None (REC-05) | AC10 |
| X7 | The gateway-bff route cannot reach rwb-case inside the budget | The route answers with the platform error envelope and the screen shows SCR-02 in its error state; no partial screen is composed | None (DP-11, DP-19) | AC14 |
| X8 | A role without the Case record right reads the case list | 403 and no row | MSG-P4-002 | AC16 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Proves the cross-service behaviour of the real services of the chain; needs no other screen or route and no build work of its own |
| Negotiable | The business date, the queue and the case used by the fixture are data; the operations are fixed by the published contracts |
| Valuable | The list that every team works from is proved on the services that will run it, with no data lake and no fake in the chain |
| Estimable | One suite, the service fixtures, one start harness, the assertions and one absence assertion |
| Small | Fits one sprint with the fixtures and the report |
| Testable | Every criterion is one assertion on a real-service answer, an event or a route response |

### 7. Acceptance criteria

```gherkin
Feature: Case list v1 with case ID, owner and queue, proved on the real wave-1 services

  Background:
    Given the business date is 2026-11-30
    Given rwb-source-data publishes rwb.source-data.AceDataReady.v1 with key ALS:2026-11-30, sourceSystem ALS and status COMPLETED
    Given the parameters case.entry.dpd = 90 and recon.tolerance.pct = 0.00 are in force through the rwb-case parameters contract
    Given rwb-case, rwb-source-data and rwb-reporting are the real SIT services behind their own logins and no contract fake stands in for a service

  Scenario: AC1 List built and reconciled (legacy RWB-E1-002 AC1)
    Given the SIT ACE data holds 28,140 accounts at 90 days past due or more with data_as_of 2026-11-30
    Given P3 excluded 21 of them at entry, so the ACE count to match is 28,119
    Given the open cases link 28,119 accounts at 90 days past due or more and 37 accounts below 90 days past due
    When every page of GET /api/recovery/case/v1/cases is read for 2026-11-30
    Then each open case appears once and the account keys of the pages number 28,156
    Then the 37 accounts below 90 days past due appear on the account list of their case and add no case row
    Then every row holds accountNumber, totalBalance, daysPastDue and dataAsOf 2026-11-30 as the account-page read of rwb-source-data answers them
    Then the REC-01 result of 2026-11-30 compares 28,119 with 28,119 and is PASS
    Then rwb-source-data holds no case list table

  Scenario: AC3 Daily refresh (legacy RWB-E1-002 AC3)
    Given the ALS batch for 2026-11-30 completed at 05:40 and the allocation run completed at 06:52
    When the case list is read and answers at 07:12 on 2026-12-01
    Then every row carries refreshedAt 2026-12-01 07:12 and the header X-Data-As-Of is 2026-11-30
    Then the SCR-02 refresh line reads "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026"

  Scenario: AC4 Last contact from EFS through ACE (legacy RWB-E1-002 AC4)
    Given the SIT ACE data holds an EFS action "PTP" for an account of case "RW-2026-000123" with contact_at 2026-11-30 15:42
    When the case list is read
    Then the row of case "RW-2026-000123" shows lastContactAt 2026-11-30 15:42 and lastActionCode "PTP" from the account-page read

  Scenario: AC5 ACE batch not complete (legacy RWB-E1-002 AC5)
    Given v_ace_batch_status holds no COMPLETED ALS row for 2026-11-30 and the DP01 stamp in use is business date 2026-11-27
    When the clock reaches 05:30 on 2026-12-01
    Then rwb.source-data.AceDataLate.v1 is published once with key ALS:2026-11-30 and completedAt null, and no AceDataReady for ALS is published
    When the clock reaches 08:00 and the case list is read
    Then GET /data-products/freshness answers DP01 with businessDate 2026-11-27 and status STALE
    Then the rows carry X-Data-As-Of 2026-11-27, are marked stale and no row claims business date 2026-11-30
    Then the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's load has not arrived."
    Then no daily case run starts for 2026-11-30

  Scenario: AC10 Case account without an ACE account row (legacy RWB-E1-002 AC10)
    Given case "RW-2026-000456" links account_key "ACC0000456", which has no row in v_ace_account for 2026-11-30
    When the case list is read
    Then the row for "ACC0000456" has an empty account number, total balance and days past due
    Then REC-05 lists "case_account.account_key ACC0000456" as an orphan for the data steward and the ACE team
    Then the case and its case_account link are unchanged

  Scenario: AC12 The daily chain runs from the readiness call to the list read (new, D-RCV-60; restated by RD-P1-024 and RD-P1-040)
    Given every source system due for 2026-11-30 has a COMPLETED v_ace_batch_status row
    When POST /api/recovery/source-data/v1/business-days/2026-11-30/ready is called with a UUID Idempotency-Key
    Then the answer is 202 with status RUNNING and the workflow ace-ingest-check-2026-11-30 runs on queue rwb-source-data
    Then one AceDataReady per source system is published with key {sourceSystem}:2026-11-30 and the payload sourceSystem, businessDate, status, completedAt
    Then rwb-case starts its daily case run only on the ALS event
    Then GET /api/recovery/source-data/v1/business-days/2026-11-30/status answers DONE once ALS is stamped
    Then the list of rwb-case answers the cases of 2026-11-30 and no service other than rwb-source-data reads an ACE view

  Scenario: AC13 No extract file and no data lake path exists (new, D-RCV-60; restated by RD-P1-024)
    Given the case list of 2026-11-30 is served
    When the daily chain completes
    Then no extract file is written, deliverFile is not called for the case list and no data lake path, lake copy or Power BI data set connection exists in the chain
    Then rwb-reporting holds its read model in schema rwb_reporting built from rwb.case.events.v1

  Scenario: AC14 gateway-bff serves SCR-02 from the rwb-case contract (new, D-RCV-60)
    Given the browser calls the gateway-bff composite route of SCR-02 for queue MTG-BKK-CO
    When the route resolves the screen model
    Then it calls GET /api/recovery/case/v1/queues/{queueId}/cases and GET /api/recovery/case/v1/cases on the rwb-case base, one hop each, with a 2 s timeout
    Then the answer carries case number, account number, product, stage, status, owner, queue, route, total balance and days past due with refresh time 2026-12-01 07:12 and data as of 2026-11-30
    Then the browser calls no rwb-source-data base

  Scenario: AC15 A repeated ready call and a redelivered event start nothing twice (new, D-RCV-60; restated by RD-P1-040)
    Given the chain of 2026-11-30 has completed
    When the ready call is repeated with the same Idempotency-Key and the ALS AceDataReady event is delivered again
    Then the stored 202 answer is replayed and no second AceDataReady is published for the unchanged batch row
    Then rwb-case starts no second daily case run for 2026-11-30
    Then the list holds the same cases and no case account appears twice

  Scenario: AC16 A role without the right reads the case list and is refused (new, D-RCV-60; restated by RD-P1-024)
    Given a test user whose role holds no Case record right
    When the user reads GET /api/recovery/case/v1/cases
    Then the answer is 403 with the platform error envelope and messageCode MSG-P4-002 and no row is returned

```

The legacy values of AC1, AC3, AC4, AC5 and AC10 are carried; their targets are restated because the case list is held by rwb-case and no extract, lake or Power BI data set exists (RD-P1-024). Legacy AC2 is read as the columns, the filters and the refresh line of the contract answers. Pending: the account-page read path (GAP-3274) blocks the account column assertions of AC1, AC4 and AC10; the rwb-case key-list read path (GAP-3273) blocks the REC-01 and REC-05 assertions of AC1 and AC10; the effect of a REC-01 BREAK on the list is open (GAP-3282).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The case list holds one row per open case with its linked account keys for the business date | REQ-RDF-007; DL17 (one case per customer per product, accounts linked); assumption: Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-18) |
| BR2 | Account number, total balance and days past due come from `v_ace_account` by `account_key` for the ACE business date in `data_as_of`; the Workbench holds no copy | D-RCV-35 U4; ADR-010 |
| BR3 | The daily case run starts only on the ALS `AceDataReady` with status COMPLETED; a date that is not complete is shown stale | RD-P1-040; BR-P1-014-4; MSG-P1-001 |
| BR4 | The count of accounts at or above the entry threshold is compared by REC-01 with the open case accounts rwb-case returns, with `recon.tolerance.pct` = 0.00 | CTL-01; REC-01; parameter case.entry.dpd (DL16; ASM-1094, ASM-5264); RD-P1-024; RD-P1-042 |
| BR5 | The list carries the business date and the refresh time on every row | REQ-RDF-009 (freshness); FEAT-RDF-18 |
| BR6 | A repeated start or a redelivered event for the same business date changes nothing | R-UNI-40; RD-P1-040 |
| BR7 | Removed in version 3: no file is delivered for the case list (RD-P1-024) | — |
| BR8 | Case data is served only by rwb-case. ACE data is read from `recovery.v_ace_*` only by rwb-source-data and reaches the list through its contract | ADR-002; DT08; ADR-010; DP-05; covered by AC12 |
| BR9 | Last contact and action code come from `v_ace_efs_action` by `account_key`, taking the row with the latest `contact_at` | RWB-E1-069; Data Tier Map |
| BR10 | A case account with no ACE row is shown with empty amounts and listed by REC-05; it is never deleted and the case is never changed by this story | BR-P1-011-3 |
| BR11 | Every call between two services is one hop with a 2 s timeout and a published contract: the browser reaches gateway-bff, gateway-bff reaches rwb-case, rwb-case reaches rwb-source-data. No service reads another service's tables | DP-01; DP-11; ADR-020; Arch v5 slide 11; covered by AC14 |
| BR12 | There is no data lake, no lake copy and no extract of the case list. Reporting is fed by events into rwb-reporting | DP-17; ADR-018; Arch v5 slide 37; RD-P1-024; covered by AC13 |

### 9. State transitions

None for a case status. The run states this story exercises are `AceIngestCheck` and `ReconciliationWorkflow` in rwb-source-data, the daily case run and `CaseListDayOpen` in rwb-case, and the freshness status of a data product (LOADED, STALE). No publish status exists (RD-P1-024). No case status is changed by any step of the chain.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login, DP-02) | Runs `AceIngestCheck` and `ReconciliationWorkflow`, reads the ACE views, writes the freshness stamp and its events, answers the freshness and account-page reads |
| rwb-case service identity (the rwb-case login, DP-02) | Consumes AceDataReady, serves the case list under `/api/recovery/case/v1` within the caller's scope, calls the rwb-source-data reads |
| Airflow caller (readiness workload identity) | Calls the readiness pair; the suite harness uses the SIT configuration of this identity |
| rwb-reporting service identity (the rwb-reporting login, DP-02) | Consumes `rwb.case.events.v1` and writes its own read model in schema `rwb_reporting` |
| gateway-bff, platform edge | Owns the SCR-02 composite route, the 2 s timeout and the session check |
| RW-PLATADM, platform administrator | Books and restores the SIT data set |
| RW-TRIBE, squad members | Start the suite, change the fixture and the data set through a reviewed pull request, read the report |
| RW-BIANAL, reporting and BI analyst | Owns the rwb-reporting read model |
| RW-TEAMMGR, RW-CASEOWN, RW-PHONECOL | Read SCR-02 through the gateway-bff route within their scope |
| RW-DATASTEW, RW-COE, RW-AUDIT | Read the run and the orphan list of REC-05; RW-COE owns the parameters and the reference data |

No approval level from the delegation of authority applies: the story takes no business decision.

### 11. Data

| BR Field ID | Entity | Field | Read or write | Where it lives |
|---|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-002 | recovery_case | case_no | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-003 | recovery_case | product_group | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-005 | recovery_case | status | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-006 | recovery_case | stage_code | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-008 | recovery_case | route_code | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-009 | recovery_case | owner_user_id | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-011 | recovery_case | team_code | Read (through the rwb-case contract) | rwb_case |
| DF-CAS-026 | case_account | account_key | Read (through the rwb-case contract) | rwb_case |
| DF-WRK-002 | queue | queue_code | Read (through the rwb-case contract) | rwb_case |
| DF-ACE-001, DF-ACE-002, DF-ACE-018, DF-ACE-020, DF-ACE-036 | v_ace_account | account_key, account_code, days_past_due, total_balance, data_as_of | Read in rwb-source-data only, answered by the account-page read | recovery views |
| DF-ACE-109, DF-ACE-111, DF-ACE-114 | v_ace_efs_action | account_key, action_code, contact_at | Read in rwb-source-data only | recovery views |
| DF-ACE-178, DF-ACE-179, DF-ACE-181, DF-ACE-186 | v_ace_batch_status | source_system, business_date, completed_at, is_complete | Read in rwb-source-data only | recovery views |
| DF-RPT-001 to DF-RPT-019 | case_list_row | Retired (RD-P1-024): not created, not read, not written | — | — |

The case fields are served only by rwb-case; the ACE views are read only by rwb-source-data (DP-01, DP-05). The suite writes no row. The reporting read model is owned by rwb-reporting in schema `rwb_reporting`; its field list is Not specified in the source documents (GAP-0335; ASM-0429), so this story asserts that it is built from the case events, not its columns. Field IDs are those of the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None. This story builds and runs integration tests and publishes no operation; every operation in the chain is provided by its owner service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Base | Use in the suite | Budget |
|---|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | `/api/recovery/case/v1` | The case list (AC1, AC3, AC4, AC10, AC14, AC16) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | `/api/recovery/case/v1` | The queue cut for queue MTG-BKK-CO used by SCR-02 (AC14) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data (RWB-P1-E1015-CON) | `/api/recovery/source-data/v1` | Stamp in use per product, `status` LOADED or STALE (AC5) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data (RWB-P1-E1015-CON) | `/api/recovery/source-data/v1` | Starts the chain; UUID `Idempotency-Key`; 202 (AC12, AC15) | — |
| GET | `/api/recovery/source-data/v1/business-days/{date}/status` | P1 rwb-source-data (RWB-P1-E1015-CON) | `/api/recovery/source-data/v1` | RUNNING, DONE or LATE (AC12) | — |
| Pending (GAP-3274) | Account-page read | P1 rwb-source-data (RWB-P1-E1015-CON) | `/api/recovery/source-data/v1` | Called by rwb-case: account number, product, total balance, days past due, last contact time, last action code, `dataAsOf` | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/admin/reconciliation/results` | P1 rwb-source-data (RWB-P1-E1011-CON) | `/api/recovery/source-data/v1` | REC-01 and REC-05 results (AC1, AC10) | One hop, 2 s |

The read operations by which rwb-case serves the case list are `GET /api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/queues/{queueId}/cases` on the rwb-case base. The browser reaches none of these bases directly: it calls the gateway-bff composite route (DP-19).

The suite builds against rwb-source-data.yaml 5.1.0 and rwb-case.yaml 5.1.0 (API Specification v7).

#### 12.3 Events published

None published by the suite or asserted as an output of a delivery: the `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` assertions are removed with the extract (RD-P1-024).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Consumer | Asserted behaviour |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | rwb-case (daily case run); rwb-source-data does not consume it | Key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt`; daily work starts only on ALS with COMPLETED (AC12, AC15) |
| `rwb.source-data.AceDataLate.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | gateway-bff banner and alerts | Published at 05:30 for ALS not COMPLETED, `completedAt` null (AC5) |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | rwb-reporting (read model); rwb-source-data (ledger intake) | A new open case is on the list (AC1, AC13) |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | rwb-reporting (read model); rwb-source-data (ledger intake) | The owner and the queue on the list are the allocated ones (AC1) |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Owner | Use in the suite |
|---|---|---|---|---|
| DailyCaseRun | Workflow | `rwb-case` | P3 rwb-case | Started on the ALS AceDataReady; creates and allocates the cases the list reads (AC1, AC12) |
| `AceIngestCheck` | Workflow, ID `ace-ingest-check-{businessDate}` | `rwb-source-data` | P1 rwb-source-data | Stamps freshness and publishes the events (AC5, AC12, AC15) |
| `ReconciliationWorkflow` | Workflow, ID `recon-{businessDate}`, child of `AceIngestCheck` after the ALS stamp | `rwb-source-data` | P1 rwb-source-data | REC-01 and REC-05 of the date (AC1, AC10) |
| `CaseListDayOpen` | Workflow of the Schedule `rwb-case-caselist-daily` | `rwb-case` | P3 rwb-case | Reads freshness once and raises MSG-P1-001 when the date is stale (AC5) |

The workflow IDs are keyed by the business date, so a repeated start of the same date joins the open run (BR6, AC15). No case-list workflow, activity or Schedule exists in rwb-source-data.

#### 12.6 Schedules

| Schedule or trigger | Cadence | Owner | Legacy reference |
|---|---|---|---|
| `rwb-source-data-ace-late-check` | Daily 05:30 Asia/Bangkok | P1 rwb-source-data | Raises AceDataLate |
| `rwb-case-caselist-daily` | Daily at `caselist.allocation.wait.until` (07:15) Asia/Bangkok | P3 rwb-case | Replaces the legacy case list run |

No shared scheduler table and no Quartz job is used: triggers are the readiness call, events and Temporal Schedules in the owning service (DP-10).

#### 12.7 Tables owned

None. This story owns no table and writes no schema of its own (DP-01). The tables in the chain are owned as follows and are read only through their owner's contract: `data_product_load`, `business_day_readiness`, `reconciliation_result` and `processed_event` in schema `rwb_source_data` (P1); `recovery_case`, `case_account`, `queue` and `case_party` in schema `rwb_case` (P3); the read model and `processed_event` in schema `rwb_reporting` (P9). `case_list_row` is retired (RD-P1-024).

#### 12.8 Contract fakes

None used. The ACE state of every fixture is set up as synthetic data in the SIT ACE data behind the real rwb-source-data service; no rwb-source-data or rwb-case contract fake stands in for a service, and a fake endpoint fails the topology check. The suite runs against the deployed SIT services and their published contracts, because the point of the story is that the real cross-service behaviour is proved (R5.4 class I).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided; consumed: the two rwb-case reads, the freshness read, the readiness pair, the reconciliation results read and, through rwb-case, the account-page read |
| Kafka | 0 published by this story; AceDataReady, AceDataLate, CaseCreated and CaseAllocated observed |
| Temporal | Observed: `AceIngestCheck` and `ReconciliationWorkflow` on `rwb-source-data`; DailyCaseRun and `CaseListDayOpen` on `rwb-case` |
| File | None; no extract and no lake transfer |

### 13. Solution plan

**Package.** `integration/recovery/wave1/caselist` in the ACE repository, package `<ACE base package>.recovery.itg.wave1.caselist`. Not part of a deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Wave1Topology fixture | Configuration | Names the real SIT endpoints, logins and task queues of rwb-case, rwb-source-data, rwb-reporting and gateway-bff; fails the suite when a fake endpoint is configured |
| ReadinessHarness | Test fixture | Calls `POST /business-days/{date}/ready` with a UUID key, repeats it and redelivers the ALS event for AC15 |
| CaseListAssertion | Test service | Reads every page of the rwb-case list and asserts the counts of AC1, the refresh of AC3, the contact of AC4 and the orphan of AC10 |
| RunAssertion | Test service | Asserts the workflow runs, the two events and the freshness answer (AC5, AC12) |
| AbsenceAssertion | Test service | Asserts no extract file, no `deliverFile` call and no lake path, and the reporting read model built from case events (AC13) |
| RouteAssertion | Test service | Calls the gateway-bff SCR-02 composite route, asserts the 2 s timeout and the merged screen model (AC14) |
| DedupeAssertion | Test service | Asserts the replayed 202, no second event or case run and an unchanged list (AC15) |
| SuiteReport | Service | Publishes the result with the build ID, the data set version and the service versions |

**Real-service topology.** rwb-case (P3, schema `rwb_case`, base `/api/recovery/case/v1`, queue `rwb-case`, `rwb.case.events.v1`); rwb-source-data (P1, schema `rwb_source_data`, base `/api/recovery/source-data/v1`, queue `rwb-source-data`, `rwb.source-data.events.v1`); rwb-reporting (P9, schema `rwb_reporting`, base `/api/recovery/reporting/v1`, queue `rwb-reporting`, `rwb.reporting.events.v1`); gateway-bff for SCR-02. Every service is reached behind its own login (DP-02) and no service reads another service's schema (DP-01). The schemas named in this section belong to those services; this story owns no schema (DP-01).

**Fixtures**

| Fixture | Content |
|---|---|
| Business date run | Business date 2026-11-30, ALS batch complete at 05:40, allocation complete at 06:52, list read at 07:12, 28,140 accounts in the SIT ACE data, 21 exclusions, 28,156 linked account keys |
| Case rows | Case RW-2026-000123, account ACC0000123, product MORTGAGE, status ASSIGNED, queue MTG-BKK-CO, total balance 1,250,000.00, days past due 96 |
| Contact row | The SIT ACE data holds an EFS action PTP for an account of case RW-2026-000123 with contact_at 2026-11-30 15:42 |
| Orphan row | Case RW-2026-000456 with account_key ACC0000456 and no account row in the SIT ACE data for 2026-11-30 |
| Late batch | The SIT ACE batch status holds no COMPLETED ALS row for 2026-11-30 at 05:30 and at 08:00 |

Every fixture value is the legacy value carried unchanged; no new business value is invented.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; the gap GAP-0335 records the missing delivery wording of the legacy source |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The DP dependencies resolve to the platform and service contract stories of the owning services and stay with their implementation stories; this story carries no H, C or X dependency and carries the I dependencies above (§R5.4 class I, allowed on an ITG story only).

**Run order**

1. Check the topology: every endpoint, login and task queue is the real SIT one and no fake endpoint is configured.
2. Late path first on its own data set: assert AceDataLate at 05:30, DP01 STALE at 08:00, the stale list and MSG-P1-001 (AC5).
3. Call the ready endpoint for 2026-11-30 and assert `ace-ingest-check-2026-11-30`, the events and the DONE status (AC12).
4. Wait for the daily case run and the allocation; read the list and assert the counts, the refresh, the contact row and the orphan row (AC1, AC3, AC4, AC10).
5. Assert the REC-01 and REC-05 results of the date (AC1, AC10).
6. Assert the absence of an extract, a `deliverFile` call and a lake path, and the reporting read model (AC13).
7. Call the gateway-bff SCR-02 route and assert the merged answer and the 2 s timeout (AC14).
8. Repeat the ready call and redeliver the ALS event; assert nothing starts twice (AC15).
9. Read the list as a role without the right (AC16).
10. Publish the suite report with the build ID, the data set version and the service versions.

**Configuration.** The business date, the queue, the case, the counts and the service versions sit in the fixture files; the pass limits are the legacy values of the criteria. Nothing business-specific is coded in a test method.

**Done when.** Every test of section 16 passes in SIT against the real wave-1 services, the repeat proves nothing starts twice, no extract or lake path appears in the run log, and the report is attached to the wave-1 integration record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not complete and the list is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right reads the case list | You cannot {action} here. Your role does not include it. |

The message texts are those of the Error and Message Standard. The suite's own report lines — the run ID, the row count and the route timing — are for the integration record and are not part of the message standard.

### 15. Screens and states

No screen is built in this story. The screen the suite exercises end to end is SCR-02 Case list in its states — Loading, empty, list and filtered, stale, error and no access: loading while the route answer is awaited, empty when the queue holds no open case, stale with MSG-P1-001 when the date is not complete, error when the list answers 503 (X4, X7) and no partial screen is composed, and no access when a role without the right is answered 403 with MSG-P4-002 (X8) — served by the gateway-bff composite route on the rwb-case base, and showing the ten columns of the list with the refresh line "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026". The browser calls no rwb-source-data base. The route specification and the field-level masking of customer fields are Not specified in the source documents (GAP-0335; ASM-0429); the screen build itself is RWB-P3-E1002-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-11-ITG | AC16, Access | Integration | A role without the Case record right reads `GET /api/recovery/case/v1/cases`; refused with MSG-P4-002 |
| TC-E1-002-12-ITG | §12 operations, events, activities | Contract | Each operation, event and activity in §12 asserted on the wire against its published contract |
| TC-E1-002-01-ITG | AC1, BR1, BR2, BR4 | End to end | 28,140 synthetic accounts in the SIT ACE data at 90 days past due or more; 21 exclusions; 37 case accounts below 90 |
| TC-E1-002-02-ITG | AC2, BR1 (run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS) | Integration | Built list; case RW-2026-000123 |
| TC-E1-002-03-ITG | AC3, BR5 | Integration | ALS batch complete at 05:40; allocation run complete at 06:52; list read at 07:12 |
| TC-E1-002-04-ITG | AC4, BR9 | Integration | The SIT ACE data holds a PTP action with contact_at 2026-11-30 15:42 |
| TC-E1-002-05-ITG | AC5, BR3 | End to end | No COMPLETED ALS batch row for 2026-11-30; DP01 stamp in use 2026-11-27 |
| TC-E1-002-06-ITG | AC6 (run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS) | Integration | The allocation run not complete at 07:15 |
| TC-E1-002-07-ITG | AC7, BR6 (run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS) | Integration | Restart of a built date |
| TC-E1-002-08-ITG | AC8 (run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS) | Integration | rwb-case contract error after 12,000 accounts |
| TC-E1-002-09-ITG | Retired in this story (RD-P1-024): no file delivery | — | — |
| TC-E1-002-10-ITG | AC10, BR10 | Integration | Case account ACC0000456 with no account row in the SIT ACE data |
| TC-ITG-E1002-01 | AC12 | Integration | Ready call for 2026-11-30; events per source system; DONE status; list answered |
| TC-ITG-E1002-02 | AC13 | Integration | No extract, no deliverFile call, no lake path; reporting read model from case events |
| TC-ITG-E1002-03 | AC14 | Integration | gateway-bff SCR-02 route for queue MTG-BKK-CO; 2 s timeout; no rwb-source-data base from the browser |
| TC-ITG-E1002-04 | AC15 | Integration | Ready call repeated with the same key and the ALS event redelivered |


The legacy criteria not owned here — AC2, AC6, AC7, AC8, AC9 and AC11 — are owned by RWB-P1-E1002-APP, RWB-P3-E1002-APP and RWB-P1-E1002-OPS and are re-exercised only inside the end-to-end run of TC-E1-002-01-ITG and TC-E1-002-05-ITG.

### 17. Guardrails

- No business value in code: the entry threshold, the tolerance, the wait time, the counts and the queue are fixture data and parameters, never constants in a test method.
- No personal data in logs, reports, events, workflow payloads or prompts: the report holds counts, ids and timings.
- No read of another service's tables: the case is read through the rwb-case contract, the ACE views through rwb-source-data only, and the assertions use the owner's contract (DP-01, DP-05).
- One hop and one timeout: every call between two services is a single contract call with a 2 s timeout (DP-11, DP-19).
- No data lake: the suite fails when a lake path, a lake copy or a lake client is configured in any service of the chain (DP-17).

- The suite never runs against UAT or production and writes no row itself; the SIT data set is restored after the run.
- Every service is real in this suite. A fake endpoint, a stub base or a mocked consumer fails the topology check before any load is generated.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | The case list reconciles daily to the count of accounts at 90 days past due or more in the ACE account view, and every business key resolves to an ACE row | The rwb-case list read, the REC-01 result and the REC-05 orphan of `case_account.account_key` | Test cases of AC1, AC5 and AC10 (section 16) |
| REQ-RDF-009 | The list is dated to the ACE batch it was built from and shows its refresh time | `refreshedAt`, `X-Data-As-Of` and the refresh line of the route answer | Test cases of AC3, AC14 and AC15 (section 16) |

### 19. Out of scope

- The case list screen and its build (RWB-P3-E1002-APP).
- The P1 build of the account-page read (RWB-P1-E1002-APP). No P1 case list step, extract writer or `case_list_row` table exists (RD-P1-024).
- File delivery of any case list extract: none exists.
- The ACE batch gate and the freshness stamp of the individual views (RWB-P1-E1015-APP).
- The ACE views and the grants that create them (RWB-P1-E1069-APP).
- Row-level security by team on the list (RWB-P1-E1016-APP and the BI analyst's projection).
- The reconciliation by product, the balance reconciliation and the break list of the reconciliation story (RWB-P1-E1011-APP).
- The rwb-reporting read model definition (the rwb-reporting stories).
- The deployment of the chain: Helm values, topic and queue provisioning, dashboards and the runbook (the OPS stories of each service).
- The gateway-bff route specification and the field-level masking of customer fields (the platform edge stories).

### Remaining delivery steps

- Fix the path and maximum keys per call of the account-page read and publish it in RWB-P1-E1015-CON (solution architect, GAP-3274).
- Publish the rwb-case paged key-list read used by REC-01 and REC-05 (rwb-case service owner, GAP-3273).
- Rule the effect of a REC-01 BREAK on the case list (solution architect with the data lead, GAP-3282).
- Size the story at refinement (squad).
- Epic design sign-off for business epic EP01 (solution architect).
- Load the SIT synthetic ACE data and open cases of the fixtures (QA team with the ACE team).
- Restate the test case rows of this story in Test Cases v9 and the Requirements Traceability Matrix (test writer).

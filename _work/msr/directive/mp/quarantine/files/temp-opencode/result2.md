# RWB-ITG-E1002-ITG Case list v1 with case ID, owner and queue — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Patterns applied | DP01, DP02, DP05, DP06, DP07, DP10, DP11, DP14, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-14) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract story | Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-21) |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-23) |
| Integration dependencies | RWB-P3-E1018-APP, RWB-P3-E1020-APP, RWB-P2-E1007-APP, RWB-P1-E1002-APP, RWB-P3-E1002-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-E1-002 is split and reworked as the wave-1 integration story RWB-ITG-E1002-ITG, which proves the case list end to end across rwb-case, rwb-source-data, rwb-integration, rwb-reporting and the gateway-bff composite route for SCR-02, with the removed data lake replaced by the delivery of the daily extract to rwb-reporting. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1002-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **the case list proved end to end on the real wave-1 services — the open cases and their owner and queue read from rwb-case through its published contract, the daily `case_list_row` rows built and replaced in one transaction in rwb-source-data by the JOB-04 reconciliation workflow started by `rwb.source-data.AceDataReady.v1`, the daily extract delivered to rwb-reporting by the `deliverFile` activity of rwb-integration instead of the removed data lake, and SCR-02 served in one hop by the gateway-bff composite route**, so that **the one list every team works from is dated to the ACE batch it was built from and is proven against the services that will run it, not against a fake**.

### 2. Business rationale

The legacy story RWB-E1-002 built one case list each business date from the open cases through the P3 in-process interface `CaseQueryApi`, joined it to the ACE account view and published it to Power BI through a file on the data lake (INT-19). In Arch v5 the single recovery schema and the in-process call are gone: rwb-case publishes a REST contract under `/api/recovery/case/v1`, rwb-source-data is the only service that reads the thirty `recovery.v_ace_*` views (DP-05), and the data lake and its Power BI connection are removed (DP-17; ADR-018). The list is still needed — it is the one list every team works from and the measure "case list built and released by 07:30 on 99 percent of days" still applies — so the behaviour has to be proved somewhere on the real services, and that is this story.

The chain the story proves is short and has one owner per step. rwb-source-data consumes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` and starts its reconciliation workflow on task queue `rwb-source-data` (DP-10, DP-14); the workflow reads the open case accounts through the rwb-case contract, one hop with a 2 s timeout (DP-11), and writes the `case_list_row` rows of the business date in schema `rwb_source_data` in one transaction, reading no table of schema `rwb_case` (DP-01, DP-02). When the date is released, rwb-source-data calls the rwb-integration activity `deliverFile` on queue `rwb-integration`; rwb-integration records the file run and publishes `rwb.integration.FileDelivered.v1`, and rwb-reporting consumes the delivery into its own projection, so reporting is fed by events and delivered files and never by a lake (DP-17). SCR-02 is served by the gateway-bff composite route, one hop, on the rwb-case base (DP-19).

The parameters and reference data the run reads are the rwb-case contracts (DP-06, DP-07), the topic and event names come from the naming library (DP-14), the schema objects arrive through the P1 Flyway sequence (DP-15) and the account and arrears facts come from the ACE views read by rwb-source-data alone (DP-05). What no source states is the target read operation by which rwb-case serves the list that rwb-source-data builds, and how the daily extract reaches rwb-reporting once the data lake is removed: Not specified in the source documents (GAP-0335; ASM-0429). The story proves the two operations that exist today and records the choice as an assumption, so a change of operation is one contract edit and one test change.

### 3. Preconditions

- RWB-P3-E1018-APP is done: rwb-case creates the case, the case account link and the number, `recovery_case`, `case_account` and `case_party` exist in schema `rwb_case`, and `GET /api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/cases/{caseId}` answer from it.
- RWB-P3-E1020-APP is done: the morning allocation sets the owner and the queue on each case and publishes `rwb.case.CaseAllocated.v1`, so the list has an owner and a queue to show.
- RWB-P1-E1002-APP is done: the `case_list_row` table, its unique key on business date, case and account, the case list step of the reconciliation workflow, the extract writer and the call to `deliverFile` exist in rwb-source-data, and `rwb_source_data` is migrated by the P1 Flyway sequence.
- RWB-P2-E1007-APP is done: the rwb-integration `deliverFile` activity, the `interface_config`, `file_run` and `outbound_item` objects, the manifest and the `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` events exist on queue `rwb-integration`.
- RWB-P3-E1002-APP is done: the case list read operations of rwb-case, including `GET /api/recovery/case/v1/queues/{queueId}/cases`, are published and answer with the owner, the queue, the stage, the status, the route and the refresh fields.
- rwb-reporting consumes `rwb.integration.FileDelivered.v1` and `rwb.reporting.events.v1` is available, so the delivered extract lands in a projection in schema `rwb_reporting`.
- The gateway-bff composite route for SCR-02 is deployed in SIT (DP-19, RWB-PLT-N001-CON), with the 2 s per-call timeout and no call chain deeper than one hop.
- An SIT data set holds open cases and a masked ACE account view for a business date, with at least the 28,156 rows of the legacy fixture available to the run.
- The parameters `case.entry.dpd` = 90, `recon.caselist.tolerance.pct` = 0.00 and `caselist.allocation.wait.until` = 07:15 are in force through the rwb-case parameters contract, owned by RW-COE.
- Every service is the real SIT service behind its own login: no contract fake stands in for a service in this suite.
- No build dependency: the story is Day 1 by rule (Template and Rules §R5.7) and waits only for the integration dependencies above.

### 4. Flow

1. Test fixture: publishes `rwb.source-data.AceDataReady.v1` for source ALS and business date 2026-11-30 on `rwb.source-data.events.v1`, with the CloudEvents envelope and one event id.
2. rwb-source-data: the consumer deduplicates through its inbox `processed_event` and starts the reconciliation workflow for 2026-11-30 on task queue `rwb-source-data`, as an event-started workflow and not from a shared scheduler (DP-10).
3. rwb-source-data: the case list step of the workflow reads the open case accounts of the business date through `GET /api/recovery/case/v1/cases`, one hop on the rwb-case base with a 2 s timeout (DP-11), and reads the queue cut through `GET /api/recovery/case/v1/queues/{queueId}/cases` for each queue it needs.
4. rwb-source-data: joins each `account_key` to the ACE account view for the account number, the total balance and the days past due of `data_as_of`, and reads the latest contact and action code per `account_key` from the EFS action view. Both views are read in rwb-source-data only (DP-05), never through another service.
5. rwb-source-data: replaces the `case_list_row` rows of 2026-11-30 in one transaction in schema `rwb_source_data`, each with `refreshed_at` and `publish_status` PENDING, and records the run checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED.
6. rwb-source-data: the reconciliation step of RWB-P1-E1011-APP compares the count with the ACE view and sets `publish_status` HELD or RELEASED for the date.
7. rwb-source-data: the publish step calls the rwb-integration activity `deliverFile` on queue `rwb-integration` with the manifest of the 2026-11-30 extract — fileId, batchId, sha256 and record count — only when `publish_status` is RELEASED.
8. rwb-integration: records the file run and the outbound item in schema `rwb_integration`, delivers the file to the rwb-reporting target and publishes `rwb.integration.FileDelivered.v1` on `rwb.integration.events.v1`, or `rwb.integration.FileFailed.v1` when the retries are exhausted.
9. rwb-reporting: consumes the delivery through its inbox and writes the delivered extract into its own projection in schema `rwb_reporting`; no data lake path and no lake copy is read or written anywhere in the chain.
10. gateway-bff: the SCR-02 composite route calls `GET /api/recovery/case/v1/queues/{queueId}/cases` and `GET /api/recovery/case/v1/cases`, one hop each, and merges the answers into the screen model with the refresh line.
11. Assertions: the suite reads `case_list_row` through the rwb-source-data contract projection, the rwb-integration file run through its operations endpoint, the reporting projection through the rwb-reporting contract, and the SCR-02 route answer; it reads no table directly other than the SIT fixture checks of RWB-P1-E1002-APP.
12. Replay fixture: republishes the same AceDataReady event id and asserts one run and one set of rows for the business date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A source the case list reads is not complete at the cut-off | The daily completeness gate holds the case list step; no `case_list_row` is written for the date; the last released extract stays in rwb-reporting and the data steward and team managers are alerted | MSG-P1-001 | AC5 |
| X2 | The allocation step has not completed by 07:15 | The list is built with the owner and the queue as they are and the run check ALLOCATION_COMPLETE is NO | None (shown on the run) | AC1 |
| X3 | The same AceDataReady event is delivered twice | The inbox drops the second delivery, no second run starts and the rows of the date are unchanged | MSG-P1-011 | AC15 |
| X4 | The rwb-case contract raises an error after 12,000 accounts are read | The transaction rolls back, no `case_list_row` is written for the date, the run status is FAILED and the platform administrator restarts the workflow from Temporal | None (alert to the platform administrator) | AC1 |
| X5 | `deliverFile` fails all its retries | rwb-integration publishes `rwb.integration.FileFailed.v1`, the run shows COMPLETED with check PUBLISHED NO and the transfer is in the exception queue with a task for the platform administrator | None (R-UNI-34) | AC13 |
| X6 | A case account has no ACE account row for the business date | The row is written with empty account number, total balance and days past due; REC-05 lists the key for the data steward and the ACE team; the case and the link are unchanged | None (REC-05) | AC10 |
| X7 | The gateway-bff route cannot reach rwb-case inside the budget | The route answers with the platform error envelope and the screen shows SCR-02 in its error state; no partial screen is composed | None (DP-11, DP-19) | AC14 |
| X8 | A role without the right lists the JOB-04 runs | 403 with the error envelope | MSG-P4-002 | AC16 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Proves the cross-service behaviour of the five real services of the chain; needs no other screen or route and no build work of its own |
| Negotiable | The business date, the queue and the case used by the fixture are data; the operations are fixed by the published contracts |
| Valuable | The list that every team works from is proved on the services that will run it, with no data lake and no fake in the chain |
| Estimable | One suite, five service fixtures, one event publisher, four assertions and one absence assertion |
| Small | Fits one sprint with the fixtures and the report |
| Testable | Every criterion is one assertion on a real-service answer, a row, an event or a route response |

### 7. Acceptance criteria

```gherkin
Feature: Case list v1 with case ID, owner and queue, proved on the real wave-1 services

  Background:
    Given the business date is 2026-11-30
    Given rwb-source-data publishes rwb.source-data.AceDataReady.v1 for source ALS and business date 2026-11-30
    Given the parameters case.entry.dpd = 90 and recon.caselist.tolerance.pct = 0.00 are in force through the rwb-case parameters contract
    Given rwb-case, rwb-source-data, rwb-integration and rwb-reporting are the real SIT services behind their own logins and no contract fake stands in for a service

  Scenario: AC1 List built and reconciled (legacy RWB-E1-002 AC1)
    Given the rwb-source-data contract serves 28,140 accounts at 90 days past due or more with data_as_of 2026-11-30
    Given P3 excluded 21 of them at entry, so the ACE count to match is 28,119
    Given the open cases link 28,119 accounts at 90 days past due or more and 37 accounts below 90 days past due
    When the case list step of ReconciliationWorkflow runs
    Then case_list_row holds 28,156 rows for 2026-11-30
    Then REC-01 of RWB-E1-011 compares 28,119 with 28,119 and is PASS
    Then the run record shows 37 rows below 90 days past due

  Scenario: AC3 Daily refresh (legacy RWB-E1-002 AC3)
    Given the ALS batch for 2026-11-30 completed at 05:40 and the morning allocation completed at 06:52
    When the case list step runs and completes at 07:12
    Then every row for 2026-11-30 carries refresh time 2026-12-01 07:12
    Then the report after the 07:30 data set refresh shows "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026"

  Scenario: AC4 Last contact from EFS through ACE (legacy RWB-E1-002 AC4)
    Given the rwb-source-data contract serves an action "PTP" for an account of case "RW-2026-000123" with contact_at 2026-11-30 15:42
    When the case list step runs
    Then the row of case "RW-2026-000123" shows last contact 2026-11-30 15:42 and action code "PTP"

  Scenario: AC5 ACE batch not complete (legacy RWB-E1-002 AC5)
    Given the rwb-source-data contract shows no COMPLETED ALS batch row for 2026-11-30 at 08:00
    When the DP01 cut-off passes and ReconciliationWorkflow is triggered
    Then the daily completeness gate holds the step and no case_list_row for 2026-11-30 is written
    Then the lake keeps the extract file for 2026-11-27
    Then the team manager group receives MSG-P1-001 "DP01 Account and arrears is from 2026-11-27. Today's load has not arrived."

  Scenario: AC10 Case account without an ACE account row (legacy RWB-E1-002 AC10)
    Given case "RW-2026-000456" links account_key "ACC0000456", which has no account row for 2026-11-30 in the rwb-source-data contract
    When the case list step runs
    Then the row for "ACC0000456" has an empty account number, total balance and days past due
    Then REC-05 of RWB-E1-011 lists "case_account.account_key ACC0000456" as an orphan for the data steward and the ACE team
    Then the case and its case_account link are unchanged

  Scenario: AC12 JOB-04 runs as an event-started workflow and reads the list through the rwb-case contract (new, D-RCV-60)
    Given rwb.source-data.AceDataReady.v1 for business date 2026-11-30 is on rwb.source-data.events.v1
    When rwb-source-data consumes it and starts its reconciliation workflow on queue rwb-source-data
    Then the workflow reads the open case accounts of 2026-11-30 through GET /api/recovery/case/v1/cases on the rwb-case base /api/recovery/case/v1, one hop with a 2 s timeout
    Then it reads the queue cut through GET /api/recovery/case/v1/queues/{queueId}/cases for queue MTG-BKK-CO
    Then it writes the case_list_row rows of 2026-11-30 into schema rwb_source_data in one transaction, each with publish_status PENDING
    Then no statement of the run reads a table of schema rwb_case, and the run reads no ACE view outside rwb-source-data

  Scenario: AC13 The daily extract is delivered to rwb-reporting and no data lake path exists (new, D-RCV-60)
    Given the reconciliation step sets publish_status RELEASED for 2026-11-30
    When the publish step calls the rwb-integration activity deliverFile on queue rwb-integration with the manifest of the 2026-11-30 extract
    Then rwb-integration records the file run and the outbound item in schema rwb_integration and publishes rwb.integration.FileDelivered.v1 with the fileId, the batchId, the sha256 and the record count
    Then rwb-reporting consumes the delivery and holds the extract in its own projection in schema rwb_reporting
    Then no data lake path, no lake copy and no Power BI data set connection exists in the chain
    When deliverFile fails all its retries
    Then rwb-integration publishes rwb.integration.FileFailed.v1 and the run shows COMPLETED with check PUBLISHED NO

  Scenario: AC14 gateway-bff serves SCR-02 in one hop from the rwb-case contract (new, D-RCV-60)
    Given the browser calls the gateway-bff composite route of SCR-02 for queue MTG-BKK-CO
    When the route resolves the screen model
    Then it calls GET /api/recovery/case/v1/queues/{queueId}/cases and GET /api/recovery/case/v1/cases on the rwb-case base, one hop each, with a 2 s timeout and no call chain deeper than one
    Then the answer carries case number, account number, product, stage, status, owner, queue, route, total balance and days past due with refresh time 2026-12-01 07:12 and data as of 2026-11-30
    Then the browser calls no rwb-source-data base and the case_list_row projection of schema rwb_source_data is not exposed as a browser route

  Scenario: AC15 The same AceDataReady event delivered twice produces one run and one set of rows (new, D-RCV-60)
    Given rwb.source-data.AceDataReady.v1 for 2026-11-30 was consumed and its run completed
    When the same event id is delivered again
    Then the inbox row in processed_event deduplicates it and no second reconciliation workflow is started for 2026-11-30
    Then case_list_row still holds 28,156 rows for 2026-11-30 and no case account appears twice
    Then the refresh time stays the time of the first completed run

  Scenario: AC16 A role without the right lists the ReconciliationWorkflow runs is refused (new, D-RCV-60)
    Given RW-CASEOWN signs in with a role that does not include the ReconciliationWorkflow run listing
    When RW-CASEOWN lists the ReconciliationWorkflow runs on the rwb-source-data base
    Then the call is refused with 403 and the error envelope carries MSG-P4-002 "You cannot {action} here. Your role does not include it."

  Scenario: AC17 Case and ACE data are read only through published contracts and no lake path is written (new, D-RCV-60)
    Given the chain of AC12, AC13 and AC14 has run on the real SIT services
    When the boundary check reads the calls and statements of that run
    Then every call is one hop between two services with a 2 s timeout and a published contract, and no call chain is deeper than one
    Then no statement reads a table of another service's schema and no step writes a lake path
```

The five legacy criteria are carried with their values and their lake and Power BI wording, because they are the legacy proof; their setup lines now read through the rwb-source-data contract, the removed data lake is replaced by the delivery of 12.3 and 12.4 to rwb-reporting, and AC12 to AC15 prove that replacement on the real services.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The case list holds one row per open case and linked account for the business date | REQ-RDF-007; DL17 (one case per customer per product, accounts linked); DL17 assumption: Not specified in the source documents (DOR-RWB-ITG-E1002-ITG-18) |
| BR2 | Account number, total balance and days past due come from `v_ace_account` by `account_key` for the ACE business date in `data_as_of`; the Workbench holds no copy | D-RCV-35 U4; ADR-010 |
| BR3 | The list is built only when the daily completeness gate of RWB-E1-015 reports the sources the case list reads COMPLETE for the business date | BR-P1-014-4; MSG-P1-001 |
| BR4 | The count of accounts at or above the entry threshold is compared with `v_ace_account` by REC-01 of RWB-E1-011; this step builds the list and records the rows below the threshold, it does not pass or fail a count | CTL-01; REC-01; parameter case.entry.dpd (DL16); assumptions ASM-1094, ASM-5264 |
| BR5 | The list carries the business date and the refresh time on every row | REQ-RDF-009 (freshness); FEAT-RDF-18 |
| BR6 | A repeated step for the same business date replaces that date's rows | R-UNI-40 |
| BR7 | A file that fails after the retry limit goes to the exception queue with a task for the owner | R-UNI-34; REQ-DRI-007 |
| BR8 | Case data is read only through the P3 published interface. ACE data is read only through `recovery.v_ace_*` views | ADR-002; DT08; ADR-010; covered by AC12, AC14 and AC17 |
| BR9 | Last contact and action code come from `v_ace_efs_action` by `account_key`, taking the row with the latest `contact_at` | RWB-E1-069; Data Tier Map |
| BR10 | A case account with no ACE row is written with empty amounts and listed by REC-05; it is never deleted and the case is never changed by this story | BR-P1-011-3 |
| BR11 | Every call in the chain is one hop between two services with a 2 s timeout and a published contract: the browser reaches gateway-bff, gateway-bff reaches rwb-case, rwb-source-data reaches rwb-case and rwb-integration by contract and activity. No service reads another service's tables and no call chain is deeper than one | DP-01; DP-11; ADR-020; Arch v5 slide 11; covered by AC12, AC14 and AC17 |
| BR12 | There is no data lake and no lake copy. Reporting is fed by events into rwb-reporting and by files delivered through `deliverFile`, and no step of the list writes to a lake path | DP-17; ADR-018; Arch v5 slide 37; covered by AC13, AC14 and AC17 |

### 9. State transitions

None for a case status. The run states this story exercises are the reconciliation workflow of the case list step in rwb-source-data (RUNNING to COMPLETED or FAILED, with the run checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED), the `deliverFile` activity of rwb-integration (STARTED to COMPLETED or FAILED, with the file run state it writes in schema `rwb_integration`), and the `case_list_row.publish_status` of the business date, written PENDING by this step and moved to HELD or RELEASED by the reconciliation step of RWB-P1-E1011-APP. No case status is changed by any step of the chain.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-source-data service identity (the rwb-source-data login, DP-02) | Consumes AceDataReady, runs the reconciliation workflow and the case list step, reads the ACE views, writes `case_list_row` and the run record in schema `rwb_source_data`, calls `deliverFile` |
| rwb-case service identity (the rwb-case login, DP-02) | Serves the case list read operations under `/api/recovery/case/v1` within the caller's scope |
| rwb-integration service identity (the rwb-integration login, DP-02) | Runs `deliverFile`, writes the file run and the outbound item, publishes FileDelivered and FileFailed |
| rwb-reporting service identity (the rwb-reporting login, DP-02) | Consumes the delivery and writes its own projection in schema `rwb_reporting` |
| gateway-bff, platform edge | Owns the SCR-02 composite route, the 2 s timeout and the session check |
| RW-PLATADM, platform administrator | Lists the reconciliation runs and restarts a FAILED workflow from Temporal |
| RW-TRIBE, squad members | Start the suite, change the fixture and the data set through a reviewed pull request, read the report |
| RW-BIANAL, reporting and BI analyst | Owns the rwb-reporting projection and the 07:30 refresh |
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
| DF-ACE-001, DF-ACE-002, DF-ACE-018, DF-ACE-020, DF-ACE-036 | v_ace_account | account_key, account_code, days_past_due, total_balance, data_as_of | Read in rwb-source-data only | recovery views |
| DF-ACE-109, DF-ACE-111, DF-ACE-114 | v_ace_efs_action | account_key, action_code, contact_at | Read in rwb-source-data only | recovery views |
| DF-ACE-178, DF-ACE-179, DF-ACE-181, DF-ACE-186 | v_ace_batch_status | source_system, business_date, completed_at, is_complete | Read in rwb-source-data only | recovery views |
| DF-RPT-001 to DF-RPT-019 | case_list_row | all fields, `publish_status` included | Write, by rwb-source-data | rwb_source_data |
| DF-RPT-016 | case_list_row | refreshed_at | Write and assert | rwb_source_data |
| DF-INT-001 to DF-INT-013 | interface_config, file_run, outbound_item | file id, batch id, checksum, record count, file run state | Write, by rwb-integration | rwb_integration |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write, by rwb-source-data | rwb_source_data |

The case fields are read only through the rwb-case contract and are never copied into another schema as a foreign key; `case_list_row` is P1's dated projection for the business date and holds business keys only; the ACE views are read only by rwb-source-data (DP-01, DP-05). The reporting projection the delivered extract lands in is owned by rwb-reporting in schema `rwb_reporting`; its field list is Not specified in the source documents (GAP-0335; ASM-0429), so this story asserts the delivery and the file metadata, not the projection's columns. Field IDs are those of the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

None. This story builds and runs integration tests and publishes no operation; every operation in the chain is provided by its owner service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Base | Use in the suite | Budget |
|---|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | `/api/recovery/case/v1` | The open case accounts of the business date, read by the JOB-04 case list step; the case-number search used by AC1 | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | `/api/recovery/case/v1` | The queue cut for queue MTG-BKK-CO, used by the queue part of the list and by SCR-02 (AC12, AC14) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/freshness` | P1 rwb-source-data | `/api/recovery/source-data/v1` | The business-date freshness and the ACE batch completeness the gate reads (AC5) | One hop, 2 s (DP-11) |

The target read operation by which rwb-case serves the case list that rwb-source-data builds is Not specified in the source documents (GAP-0335; ASM-0429); the suite asserts the two published reads above and changes with one contract edit if the agreed operation differs. The browser reaches none of these bases directly: it calls the gateway-bff composite route (DP-19).

#### 12.3 Events published

| Event | Topic | Owner of the type | When | Payload |
|---|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The daily extract of the business date is delivered to rwb-reporting (AC13) | fileId, batchId, sha256, record count, target, deliveredAt |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | Every retry of the delivery fails (AC13) | fileId, batchId, failureCode, attempt count, failedAt |

The suite publishes no event of its own; it asserts these two on the wire and asserts that rwb-reporting consumes the delivery into its own projection. No personal data is carried, and the projection is fed by events and delivered files only, never by a lake (DP-17).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Consumer | Asserted behaviour |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | rwb-source-data inbox and reconciliation workflow; rwb-case DailyCaseRun | Starts the case list step for 2026-11-30; a duplicate is dropped by `processed_event` (AC12, AC15) |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | rwb-source-data and rwb-reporting | A new open case is on the list of the next business date |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | rwb-source-data and rwb-reporting | The owner and the queue on the list are the allocated ones (AC1, AC12) |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Owner | Use in the suite |
|---|---|---|---|---|
| DailyCaseRun | Workflow | `rwb-case` | P3 rwb-case | Started by AceDataReady; creates and allocates the cases the list reads (AC1, AC12) |
| ReconciliationWorkflow (JOB-04) with the case list step | Workflow, event-started by AceDataReady | `rwb-source-data` | P1 rwb-source-data | Builds and replaces the `case_list_row` rows of the business date in one transaction (AC1, AC12, AC15) |
| deliverFile | Activity | `rwb-integration` | P2 rwb-integration | Delivers the daily extract to rwb-reporting and publishes FileDelivered or FileFailed (AC13) |

The workflow ID of the case list run is keyed by the business date, so a second delivery of the same date resolves to the same run and the same rows (BR6, AC15).

#### 12.6 Schedules

| Schedule or trigger | Cadence | Owner | Legacy reference |
|---|---|---|---|
| JOB-04 case list step | Event trigger: `rwb.source-data.AceDataReady.v1` for the business date, with the step chained after the allocation step and a wait until 07:15 at the latest | P1 rwb-source-data | JOB-04 Daily reconciliation |
| Reporting refresh | Daily 07:30, after the delivery of the business date | P9 rwb-reporting | The 07:30 data set refresh of the legacy story |

No shared scheduler table and no Quartz job is used: the trigger is the event and the refresh is a Temporal Schedule in its owning service (DP-10).

#### 12.7 Tables owned

None. This story owns no table and writes no schema of its own (DP-01). The tables in the chain are owned as follows and are read or written only by their owner: `case_list_row`, the run record and `processed_event` in schema `rwb_source_data` (P1); `recovery_case`, `case_account`, `queue` and `case_party` in schema `rwb_case` (P3); `interface_config`, `file_run` and `outbound_item` in schema `rwb_integration` (P2); the projection and `processed_event` in schema `rwb_reporting` (P9).

#### 12.8 Contract fakes

None. The suite runs against the deployed SIT services and their published contracts; contract fakes are not used at this level, because the point of the story is that the real cross-service behaviour is proved (R5.4 class I). No contract fake is therefore published for rwb-case or for rwb-source-data, and no contract fake library version is recorded as published here (DOR-RWB-ITG-E1002-ITG-22). The criteria, the test-data lines and the fixtures set their data through the rwb-source-data contract and the rwb-case contract and never through a fake, and the topology check of the Wave1Topology fixture fails the suite when a fake endpoint is configured.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 3 consumed: the two rwb-case reads and the rwb-source-data freshness read, every call one hop with a 2 s timeout, the browser only through gateway-bff |
| Kafka | 0 published by this story; 2 asserted from rwb-integration (FileDelivered, FileFailed); 3 consumed by the services (AceDataReady, CaseCreated, CaseAllocated) |
| Temporal | 2 workflows and 1 activity observed: DailyCaseRun on queue `rwb-case`, ReconciliationWorkflow on queue `rwb-source-data`, deliverFile on queue `rwb-integration` |
| File | 1 delivered file per business date, through `deliverFile` with a manifest of fileId, batchId, sha256 and record count; no lake transfer |

### 13. Solution plan

**Package.** `integration/recovery/wave1/caselist` in the ACE repository, package `<ACE base package>.recovery.itg.wave1.caselist`. Not part of a deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Wave1Topology fixture | Configuration | Names the real SIT endpoints, logins and task queues of rwb-case, rwb-source-data, rwb-integration, rwb-reporting and gateway-bff; fails the suite when a fake endpoint is configured |
| AceDataReadyPublisher | Test fixture | Publishes `rwb.source-data.AceDataReady.v1` for the business date with a fixed event id, and republishes the same id for AC15 |
| CaseListAssertion | Test service | Reads `case_list_row` of the business date through the rwb-source-data contract and asserts the counts of AC1, the refresh of AC3, the contact of AC4 and the orphan of AC10 |
| RunAssertion | Test service | Asserts the run record, the checks ROWS_BELOW_ENTRY, ALLOCATION_COMPLETE and PUBLISHED, and the absence of a `rwb_case` table reference in the run (AC5, AC12) |
| DeliveryAssertion | Test service | Asserts the rwb-integration file run, `rwb.integration.FileDelivered.v1`, the failure event and the absence of a lake path (AC13) |
| RouteAssertion | Test service | Calls the gateway-bff SCR-02 composite route, asserts one hop per call, the 2 s timeout and the merged screen model (AC14) |
| DedupeAssertion | Test service | Asserts one inbox row, one run and one set of rows after the replay (AC15) |
| SuiteReport | Service | Publishes the result with the build ID, the data set version and the service versions |

**Real-service topology.** rwb-case (P3, schema `rwb_case`, base `/api/recovery/case/v1`, queue `rwb-case`, `rwb.case.events.v1`); rwb-source-data (P1, schema `rwb_source_data`, base `/api/recovery/source-data/v1`, queue `rwb-source-data`, `rwb.source-data.events.v1`); rwb-integration (P2, schema `rwb_integration`, base `/api/recovery/integration/v1`, queue `rwb-integration`, `rwb.integration.events.v1`); rwb-reporting (P9, schema `rwb_reporting`, base `/api/recovery/reporting/v1`, queue `rwb-reporting`, `rwb.reporting.events.v1`); gateway-bff for SCR-02. Every service is reached behind its own login (DP-02) and no service reads another service's schema (DP-01). This story owns no schema (DP-01); each schema named in this section is owned by the service it is listed with.

**Fixtures**

| Fixture | Content |
|---|---|
| Business date run | Business date 2026-11-30, ALS batch complete at 05:40, allocation complete at 06:52, case list step complete at 07:12, 28,140 accounts served through the rwb-source-data contract, 21 exclusions, 28,156 rows |
| Case rows | Case RW-2026-000123, account ACC0000123, product MORTGAGE, status ASSIGNED, queue MTG-BKK-CO, total balance 1,250,000.00, days past due 96 |
| Contact row | The rwb-source-data contract serves EFS action PTP for an account of case RW-2026-000123 with contact_at 2026-11-30 15:42 |
| Orphan row | Case RW-2026-000456 with account_key ACC0000456 and no account row in the rwb-source-data contract for 2026-11-30 |
| Late batch | No COMPLETED ALS batch row for 2026-11-30 at 08:00 in the rwb-source-data contract |
| Delivery failure | The rwb-integration target forced to fail all its retries |

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
2. Publish AceDataReady for 2026-11-30 and wait for the reconciliation run to start on queue `rwb-source-data`; assert the run ID is keyed by the business date (AC12).
3. Wait for the case list step and assert the run record and the checks; assert no `rwb_case` statement in the run (AC1, AC5, AC12).
4. Assert the rows of 2026-11-30: 28,156 rows, the refresh time, the contact row and the orphan row (AC1, AC3, AC4, AC10).
5. Assert the reconciliation result and `publish_status` of the date, then trigger the publish step and assert the `deliverFile` call, the file run, `rwb.integration.FileDelivered.v1` and the reporting projection (AC13).
6. Force the delivery failure and assert `rwb.integration.FileFailed.v1` and PUBLISHED NO (AC13).
7. Call the gateway-bff SCR-02 route and assert the merged answer, the one hop and the 2 s timeout (AC14).
8. Republish the same AceDataReady event id and assert one inbox row, one run and one set of rows (AC15).
9. Assert the absence: no data lake path, no lake copy and no Power BI data set connection is configured or called (AC13).
10. Publish the suite report with the build ID, the data set version and the service versions.

**Configuration.** The business date, the queue, the case, the counts and the service versions sit in the fixture files; the pass limits are the legacy values of the criteria. Nothing business-specific is coded in a test method.

**Done when.** Every test of section 16 passes in SIT against the real wave-1 services, the replay proves one run and one set of rows, the delivery reaches the rwb-reporting projection with no lake path anywhere in the run log, and the report is attached to the wave-1 integration record.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The ACE batch for the business date is not complete and the list is not built | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-011 | A second delivery or trigger while a run for the date is running or complete | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | A role without the right lists the JOB-04 runs | You cannot {action} here. Your role does not include it. |

The message texts are the legacy texts, carried unchanged. The suite's own report lines — the run ID, the row count, the file id and the route timing — are for the integration record and are not part of the message standard.

### 15. Screens and states

No screen is built in this story. The screen the suite exercises end to end is SCR-02 Case list in its four states — Loading, empty, list and filtered — with the error and no access states Not specified in the source documents (CG-ALL-141), served by the gateway-bff composite route on the rwb-case base, one hop per call with a 2 s timeout, and showing the ten columns of the list with the refresh line "Refreshed 1 Dec 2026 07:12, data as of 30 Nov 2026". The route composes the answer from the owner's contract only: the browser calls no rwb-source-data base and the `case_list_row` projection is not exposed to it. The route specification and the field-level masking of customer fields are Not specified in the source documents (GAP-0335; ASM-0429); the screen build itself is RWB-P3-E1002-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-002-11-ITG | AC16, Access | Integration | RW-CASEOWN calls the ReconciliationWorkflow run listing on the rwb-source-data base; refused with MSG-P4-002 |
| TC-ITG-E1002-06 | AC17, Boundary | Integration | Boundary check of the AC12 to AC14 run: one hop per call, no other service's tables read, no lake path written |
| TC-E1-002-01-ITG | AC1, BR1, BR2, BR4 | End to end | 28,140 synthetic accounts served by the rwb-source-data contract at 90 days past due or more; 21 exclusions; 37 case accounts below 90 |
| TC-E1-002-02-ITG | AC2, BR1 | Integration | Run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS (owner); built list; case RW-2026-000123 |
| TC-E1-002-03-ITG | AC3, BR5 | Integration | ALS batch complete at 05:40; morning allocation complete at 06:52; step complete at 07:12 |
| TC-E1-002-04-ITG | AC4, BR9 | Integration | The rwb-source-data contract serves a PTP action with contact_at 2026-11-30 15:42 |
| TC-E1-002-05-ITG | AC5, BR3 | End to end | No COMPLETED ALS row for 2026-11-30 |
| TC-E1-002-06-ITG | AC6 | Integration | Run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS (owner); morning allocation not complete at 07:15 |
| TC-E1-002-07-ITG | AC7, BR6 | Integration | Run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS (owner); restart of a built date |
| TC-E1-002-08-ITG | AC8 | Integration | Run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS (owner); rwb-case contract error after 12,000 accounts |
| TC-E1-002-09-ITG | AC9, BR7 | Integration | Run by RWB-P1-E1002-APP, RWB-P3-E1002-APP or RWB-P1-E1002-OPS (owner); deliverFile forced to fail all retries |
| TC-E1-002-10-ITG | AC10, BR10 | Integration | Case account ACC0000456 with no account row in the rwb-source-data contract for 2026-11-30 |
| TC-ITG-E1002-01 | AC12 | Integration | AceDataReady for 2026-11-30; queue MTG-BKK-CO; run reads `GET /api/recovery/case/v1/cases` and `GET /api/recovery/case/v1/queues/{queueId}/cases`; no `rwb_case` statement |
| TC-ITG-E1002-02 | AC13 | Integration | Publish status RELEASED; manifest for 2026-11-30; FileDelivered and the reporting projection; FileFailed on the forced failure; no lake path |
| TC-ITG-E1002-03 | AC14 | Integration | gateway-bff SCR-02 route for queue MTG-BKK-CO; one hop per call; 2 s timeout; no rwb-source-data base from the browser |
| TC-ITG-E1002-04 | AC15 | Integration | The same AceDataReady event id delivered twice; one processed_event row; 28,156 rows; first refresh time |
| TC-ITG-E1002-05 | §12 contract (operations, events, activities) | Contract | GET /api/recovery/source-data/v1/freshness; rwb.integration.FileDelivered.v1 and rwb.integration.FileFailed.v1 payloads; ReconciliationWorkflow case list step (JOB-04) |

The legacy criteria not owned here — AC2, AC6, AC7, AC8, AC9 and AC11 — are owned by RWB-P1-E1002-APP, RWB-P3-E1002-APP and RWB-P1-E1002-OPS and are re-exercised only inside the end-to-end run of TC-E1-002-01-ITG and TC-E1-002-05-ITG.

### 17. Guardrails

- No business value in code: the entry threshold, the tolerance, the wait time, the counts and the queue are fixture data and parameters, never constants in a test method.
- No personal data in logs, reports, events, workflow payloads or prompts: the run reads `account_key` and `case_no` only, the extract carries no customer name, identity number or contact value, and the report holds counts, ids and timings.
- No read of another service's tables: the case is read through the rwb-case contract, the ACE views through rwb-source-data only, and the assertions use the owner's contract (DP-01, DP-05).
- One hop and one timeout: every call is a contract call with a 2 s timeout and no chain deeper than one; a deeper chain fails the route assertion (DP-11, DP-19).
- No data lake: the suite fails when a lake path, a lake copy or a lake client is configured in any service of the chain (DP-17).
- The suite never runs against UAT or production and writes only the rows of its own business date through the services; the SIT data set is restored after the run.
- Every service is real in this suite. A fake endpoint, a stub base or a mocked consumer fails the topology check before any load is generated.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-007 | The case list reconciles daily to the count of accounts at 90 days past due or more in the ACE account view, and every business key resolves to an ACE row | The `case_list_row` reads, the run checks and the orphan row of `case_account.account_key` | TC-E1-002-01-ITG, TC-E1-002-05-ITG, TC-E1-002-10-ITG, TC-ITG-E1002-01 |
| REQ-RDF-009 | The list is dated to the ACE batch it was built from and shows its refresh time | `refreshed_at`, the business date on every row and the refresh line of the route answer | TC-E1-002-03-ITG, TC-ITG-E1002-03, TC-ITG-E1002-04 |
| REQ-DRI-007 | A file that fails after the retry limit goes to the exception queue with a task for the owner | `deliverFile`, `rwb.integration.FileFailed.v1` and the PUBLISHED NO check | TC-E1-002-09-ITG, TC-ITG-E1002-02 |

### 19. Out of scope

- The case list screen and its build (RWB-P3-E1002-APP).
- The P1 build of the case list step, the extract writer and the `case_list_row` table (RWB-P1-E1002-APP).
- The rwb-integration adapter, the manifest and the file run objects (RWB-P2-E1007-APP).
- The ACE batch gate and the freshness stamp of the individual views (RWB-P1-E1015-APP).
- The ACE views and the grants that create them (RWB-P1-E1069-APP).
- Row-level security by team on the list (RWB-P1-E1016-APP and the BI analyst's projection).
- The reconciliation by product, the balance reconciliation and the break list of the reconciliation story (RWB-P1-E1011-APP).
- The rwb-reporting projection definition and the 07:30 refresh implementation (the rwb-reporting stories).
- The deployment of the chain: Helm values, topic and queue provisioning, dashboards and the runbook (the OPS stories of each service).
- The gateway-bff route specification and the field-level masking of customer fields (the platform edge stories).

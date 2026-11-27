# RWB-P1-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP18, DP19 |
| Contract version | rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-010, RD-P1-011, RD-P1-041, RD-P1-043, RD-P1-045, RD-P1-067 |
| Parallel lane | L-P1-S |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E2001-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2001-CON; RWB-PLT-E1027-CON; RWB-PLT-TE006-CON; RWB-PLT-E1071-CON; RWB-PLT-E1042-CON; RWB-PLT-N001-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v2.md (FR-P1-002, NFR-P1-009) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- `GET /entry-candidate-facts` is withdrawn; its facts are in the output of activity `listEligibleAccounts` (RD-P1-010). Findings #1, #2, #3, #4, #12, #18. AC3, AC9, AC10, X3 and X4 are withdrawn and their IDs are not reused.
- `GET /efs-history` is gated by `DailyCompletenessGate` for DP01 and DP05 and its rows are cut at the end of the business date in Asia/Bangkok (RD-P1-010, RD-P1-041, RD-P1-067). Findings #8, #9, #16.
- The run appends one row at a time through `POST /cases/{caseId}/interactions` with a fixed field mapping (RD-P1-007). Finding #6.
- Contract rwb-source-data.yaml 5.1.0 with the shared Problem body (RD-P1-004, RD-P1-005). Findings #5, #13, #20, #25.
- ACs rewritten with concrete values, AC12 to AC18 added, test case references corrected. Findings #17, #19, #22, #23, #24.
- RD-P1-067: the gate of `GET /efs-history` is DP01 and DP05 (AC19 added), the late EFS batch is waited for by the hand-over run and only that run appends. Test case IDs follow Test Cases v9; message texts follow Error and Message Standard v6.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-source-data. The legacy hand-over step read `recovery.v_ace_efs_action` and `recovery.v_ace_customer` in-process inside the JOB-02 chain of one deployable and appended the history to the interaction ledger itself; in the target the ACE facts that step consumes become two reads of this service on base `/api/recovery/source-data/v1` — the EFS history of one account and business date over `v_ace_efs_action`, and the borrower key and product group of the candidates of one business date over `v_ace_customer` and `v_ace_account` — reached by the hand-over run over REST, one hop with a 2 s budget (DP-05, DP-11). The history carries one stable key per `efs_record_key`, so the append of the ledger writer of RWB-P1-E1066-APP is idempotent and a repeat is counted under R-UNI-40 (DP-18), a borrower key that does not resolve is answered as a REC-05 break and never as a fact or a case (DP-01), and the freshness of DP01 and DP05 holds both reads until the ALS batch of the business date is COMPLETE (DP-05). The case, the decision record, the append and the run stay with RWB-P3-E2001-APP, RWB-P7-E2001-APP, RWB-P1-E1066-APP and RWB-P2-E2001-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 38 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the EFS contact and promise history of one account up to a business date to be a read of rwb-source-data over the ACE views, refused until the ALS batch of the business date is COMPLETED, with one stable key per EFS record**, so that **the hand-over run appends a history it did not assemble, each appended row is the repeat of one key rather than a second entry, and nothing is copied out of ACE into a Workbench table**.

This is the rwb-source-data slice of legacy RWB-E2-001. The legacy story created or linked a case, wrote the decision log entry, appended the EFS history and wrote the run summary in one step. Under D-RCV-60 that step is four owners, and this story delivers the ACE facts it consumes and nothing else:

- **the EFS history read** on base `/api/recovery/source-data/v1`: `GET /efs-history?accountKey=&businessDate=` over `v_ace_efs_action`, returning `efs_record_key`, `action_code`, `contact_at`, `is_ptp`, the RPC flag `is_rpc` where the ACE row carries it, `promise_date`, `promise_amount` and `collection_phase`, ordered by `contact_at` and then `efs_record_key`, restricted to the collection period of the account and to `contact_at` at or before 23:59:59 Asia/Bangkok of the business date (RD-P1-010);
- **the idempotency key of the history**: one row per `efs_record_key`, each carrying the ledger business key `EFS:<efs_record_key>`. The run sends it in the body property `idempotencyKey` of `POST /cases/{caseId}/interactions`; a repeat is answered 200 with the existing entry and counted by the run (RD-P1-007). This story supplies the key and counts the view rows it folds; the writer is RWB-P1-E1066-APP's and the run is RWB-P2-E2001-APP's;
- **no candidate facts**: the borrower key, the product group (ACE `product_category`) and the REC-05 breaks of the candidates are in the output of activity `listEligibleAccounts` of RWB-P1-E1018-APP; this story publishes no candidate read (RD-P1-010);
- **the completeness hold**: no history is answered unless `DailyCompletenessGate` answers COMPLETE for DP01 and DP05 and the business date, which is the ALS row and the EFS row of `v_ace_batch_status` with status COMPLETED. The refusal is 409 with MSG-P1-001 naming the blocking product and the last complete business date; the run, not this read, reports MSG-P2-007 (RD-P1-010, RD-P1-041, RD-P1-067);
- **no case**: this story writes no `recovery_case`, `case_account`, `case_party` or decision record and copies no ACE column into a table of its own.

It owns no legacy acceptance criterion of RWB-E2-001. Legacy AC1 (the case from the ACE data) and AC4 (the account linked to the open case) belong to rwb-case under RWB-P3-E2001-APP; AC2 (the repeat run) and AC8 (the refused second start) belong to the run under RWB-P2-E2001-APP; AC3 and AC6 (the late batch and the next good batch) belong to the run and to the freshness stamp of RWB-P1-E1015-APP, with the read-side hold proved here; AC5 (the customer not in the ACE data) is proved with the REC-05 breaks of `listEligibleAccounts` in RWB-P1-E1018-APP and carried by the run; AC7 (the decision log write fails) is rwb-decision's under RWB-P7-E2001-APP. The cross-service proof is RWB-ITG-E2001-ITG. This story is therefore written with new criteria tagged D-RCV-60, each one testing only the read above.

The shape of `GET /efs-history` is published by this service in rwb-source-data.yaml 5.1.0 and consumed by RWB-P2-E2001-CON. The split of the hand-over facts is ruled: the candidates, the borrower key, the product group and the breaks are the output of activity `listEligibleAccounts` (RWB-P1-E1018-APP), and the history read is this story's (RD-P1-010; GAP-0592 closed).

### 2. Business rationale

Collections has the contact and promise history of an account before recovery does: EFS records the calls, the letters and the promises, ACE ingests them (INT-07, daily end of day), and the Workbench reads them through `v_ace_efs_action` and `v_ace_efs_assignment` (TSD P1 T5.1; REQ-RDF-003). Today a case starts after a weekly transfer with no history, and an officer rebuilds it by hand. Carrying the collection period of the account onto the case the morning after day 90 is what makes the case workable on its first day: the officer sees what was promised, when it was promised and whether the customer kept it (REQ-CHO-001; REQ-DRI-013; FSD P1 A2.2 DP05).

Under D-RCV-60 the Workbench loads no source data (D-RCV-35 U1), so the history cannot be read from a Workbench copy: it is read from the views at request time, one account and one business date at a time, and it is never stored. The read is a contract of rwb-source-data because this service owns the ACE view contract (Architecture v5 slides 15 and 41; ADR-010), and the run of rwb-integration owns the step that turns those facts into a case, a link and a ledger append (DP-11; DP-18). The ledger is this service's own table, so the key that makes the append idempotent must come from the same owner as the writer, not from the caller. A borrower key that does not resolve is a data quality fact and not a case fact: it is a REC-05 break in the output of `listEligibleAccounts`, not part of this read (RD-P1-010).

**What D-RCV-60 changes.** Not the rationale and not one value: the 90-day entry point, the collection period, the action codes, the promise fields and the completeness gate keep their meaning. What changes is where the fact is read, who owns it and how it is reached — this service's own views and reads over `/api/recovery/source-data/v1`, one hop and 2 s, instead of an in-process call into the monolith (DP-05, DP-11).

**One read, no copy.** No table of this service holds an EFS row. The history is answered from the view on every request, and a second read of the same account and business date reads the view again; that is the whole of the no-copy rule of D-RCV-35 U1 and of FSD P1 A2.1 BR-P1-001-2. The only thing this story adds to an EFS fact is its stable key, which is derived from `efs_record_key` and stored nowhere.

### 3. Preconditions

Nothing in this list is a build dependency: this story is Day 1 and builds against the published baseline, the published view contract and the RWB-P2-E2001-CON fake, which is why its build dependency list is empty.

- The service baseline of rwb-source-data is published: schema `rwb_source_data`, the per-service Flyway sequence at its baseline version, `data_product` with DP01 to DP14 and `data_product_load` with its unique key on `(product_code, business_date)` (DP-01; the baseline of RWB-P1-E1001-APP and RWB-P1-E1015-APP, adopted as published artefacts and not as build dependencies).
- RWB-P1-E1069-APP's view contract is published and the three views this story reads are readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on `public`: `v_ace_efs_action`, `v_ace_efs_assignment` and `v_ace_batch_status` (DP-02, DP-05; TSD P1 T3.3 and T6.3; ADR-010). Section B views are built and tested over the Tier 2 fixture until they land (RD-P1-043).
- `DailyCompletenessGate` and `FreshnessQuery` of RWB-P1-E1015-APP are used as in-service interfaces. Until RWB-P1-E1015-APP is merged this story builds against stubs of the two interfaces and the batch-status fixture; it is Done only against the real components (RD-P1-041).
- The `GET /efs-history` fragment is part of rwb-source-data.yaml 5.1.0 and RWB-P2-E2001-CON consumes it. This story builds against that file and against no second draft of it (RD-P1-005).
- The candidates are RWB-P1-E1018-APP's activity `listEligibleAccounts`; this story consumes none of its output and restates no filter (RD-P1-010).
- The only caller is the rwb-integration workload identity of the hand-over run; no human role calls the read (RD-P1-010).
- A late EFS batch is the caller's wait, not this read's: on 409 MSG-P1-001 the P2 hand-over run waits on a durable timer and retries every 5 minutes until DP05 is stamped for the date or until `handover.hold_until`; at that limit it hands over without history and appends the rows when DP05 arrives, which the business key `EFS:<efs_record_key>` makes idempotent. No separate completeness check is built. Pending: the `handover.hold_until` parameter row and value, owner rwb-integration owner with RW-COE, tracked as NEW-GAP-D4; interim 09:00 (RD-P1-067).
- No approval is needed to build against a Draft contract baseline; RWB-P2-E2001-CON tags its baseline when its tests pass. This story starts on Day 1 and waits for nothing it builds.
- The boundary of the collection period is not stated by any source and is built as ASM-0830 (GAP-0588, open business decision). The read answers one account in one call and a held read answers 409 (GAP-0589; ASM-0831).

### 4. Flow

1. The hand-over run of rwb-integration works on the candidates of business date D, which `DailyCaseRun` of rwb-case obtains from activity `listEligibleAccounts` and passes to the hand-over step; downstream daily work starts only on `AceDataReady` with sourceSystem ALS (RD-P1-003, RD-P1-010).
2. For each account the run is about to hand over, it calls `GET /api/recovery/source-data/v1/efs-history?accountKey={accountKey}&businessDate=D`, one account per call, one hop with a 2 s budget (DP-11).
3. The service checks the caller identity, then the two query values (400 with MSG-GEN-001 naming the field).
4. `FreshnessHoldGate` calls `DailyCompletenessGate.check(D, [DP01, DP05])`. Unless it answers COMPLETE, the call ends with 409, MSG-P1-001, and no row (AC4).
5. `EfsHistoryReadService` resolves the collection period from the EFS assignment row of the account (ASM-0830) and reads the `v_ace_efs_action` rows of that period with `contact_at` at or before D 23:59:59 Asia/Bangkok.
6. It folds the rows to one row per `efs_record_key`, orders the answer by `contact_at` and then `efs_record_key`, and gives each row the key `EFS:<efs_record_key>` (AC1, AC2).
7. It answers 200 with `EfsHistoryAnswer`. Nothing is written: no table row, no outbox row, no decision record.
8. The run appends each answered row with `POST /cases/{caseId}/interactions` (writer of RWB-P1-E1066-APP), sending its own UUID in the `Idempotency-Key` header and `EFS:<efs_record_key>` in the body property `idempotencyKey`, with the mapping of section 12.1. The writer answers 201 for a new entry and 200 with the existing entry for a repeated business key; the run counts written and skipped from those answers (RD-P1-007).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | `DailyCompletenessGate` does not answer COMPLETE for DP01 and DP05 and the business date | 409; no view row of the history is read; the Problem detail names the blocking product and the last complete business date | MSG-P1-001 | AC4, AC19 |
| X2 | The ALS or EFS row of `v_ace_batch_status` for the business date is missing or not COMPLETED | Same answer as X1 | MSG-P1-001 | AC4, AC19 |
| X3 | Withdrawn with the candidate facts read (RD-P1-010) | Not used | None | None |
| X4 | Withdrawn with the candidate facts read (RD-P1-010) | Not used | None | None |
| X5 | A repeated view row carries an `efs_record_key` already answered | The row is folded into the answer once and counted in the duplicate count; no second row and no second key | None | AC2 |
| X6 | The account has no EFS assignment row | The period opens at the earliest `contact_at` of the account and closes at the business date; `collectionPeriodFrom` and `collectionPeriodTo` name the period used (ASM-0830) | None | AC14 |
| X7 | A view does not answer inside the 5 s statement timeout, or answers an error | 503 Problem naming the ACE database as the unavailable system; nothing is guessed from a cache | MSG-GEN-006 | AC7 |
| X8 | A caller other than the rwb-integration workload identity calls the read | 403, and the refusal is logged without a key value | MSG-P4-002 | AC8 |
| X9 | `accountKey` or `businessDate` is missing or malformed | 400 with `field` naming the parameter; no view is read | MSG-GEN-001 | AC12 |
| X10 | No valid credential | 401; no view is read | MSG-P4-001 | AC11 |
| X11 | Flag `rwb.dataengine.efs-handover-reads` is off | 404 (RD-P1-045 item 4); no view is read | Pending: message ID of the flag-off 404, owner Error and Message Standard owner (NEW-GAP-S10-01) | AC16 |

X1, X2, X5 and X6 are the read-side paths of the legacy exception rows of RWB-E2-001 carried onto the split; the case, the link, the decision record and the run summary paths belong to RWB-P3-E2001-APP, RWB-P7-E2001-APP and RWB-P2-E2001-APP. X7 is the statement timeout of Architecture v5 slide 11 and TSD P1 T6.3. The 5 s statement timeout is the server limit and the 2 s budget is the caller's: a caller that reaches 2 s first sees its own client timeout, so X7 is proved at the service. Pending: alignment of the two limits, owner solution architect (NEW-GAP-S10-02). Pending: the answer for an `accountKey` with no ACE account row (200 with no rows or 404), owner API contract owner (NEW-GAP-S10-03). Pending: the row cap value and the answer above the cap (never a truncated answer), owner solution architect (GAP-0589; NEW-GAP-S10-04).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against rwb-source-data.yaml 5.1.0, the view contract of RWB-P1-E1069-APP and stubs of the gate and freshness interfaces of RWB-P1-E1015-APP; needs no live rwb-integration, rwb-case or rwb-decision to start |
| Negotiable | The class split and the folding code are the squad's choice behind the contract; the view set, the field list, the ordering, the gate and the key format are fixed |
| Valuable | The run appends a history it did not assemble, from facts read once and keyed on the EFS record |
| Estimable | One read operation, one service, one repository over two views, one gate call and one key derivation |
| Small | Finished inside one sprint with its tests |
| Testable | Each criterion is one call against the view fixture and the gate fixture, with no write and no second service |
| Day 1 | The story has no build dependency; it is reachable on the first day of wave 2 and its tests run against the published baseline and the fake |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history

  Background:
    Given business date 2026-12-14 and the ALS and EFS rows of v_ace_batch_status for it have status COMPLETED
    Given account "A-0001" has one EFS assignment row with assignment_start_date 2026-10-15 and no assignment_end_date
    Given v_ace_efs_action holds 14 contact rows and 2 promise rows for "A-0001" with contact_at from 2026-10-15 to 2026-12-14
    Given v_ace_efs_action holds 1 row for "A-0001" with contact_at 2026-10-14
    Given the caller is the rwb-integration workload identity

  Scenario: AC1 The 16 history rows of A-0001 come back ordered (new, D-RCV-60)
    When GET /api/recovery/source-data/v1/efs-history?accountKey=A-0001&businessDate=2026-12-14 is called
    Then the answer is 200 with rowCount 16 and sourceSystem "EFS" on the answer
    And collectionPeriodFrom is 2026-10-15 and collectionPeriodTo is 2026-12-14
    And the rows are ascending by contactAt and then efsRecordKey, one per efsRecordKey
    And the row with contact_at 2026-10-14 is absent
    And each of the 2 promise rows has isPtp true with its promiseDate and promiseAmount
    And productStatus shows DP01 and DP05 as read from FreshnessQuery

  Scenario: AC2 A repeated view row and a repeated read give no second key (new, D-RCV-60)
    Given v_ace_efs_action holds a second identical row of efs_record_key "EFS-SYN-0007" of "A-0001"
    When the read for "A-0001" and 2026-12-14 is called twice
    Then each answer has rowCount 16 and duplicateCount 1
    And idempotencyKey "EFS:EFS-SYN-0007" appears once and the two bodies are identical
    And no table row, no outbox row and no workflow is created

  Scenario: AC3 Withdrawn (RD-P1-010): the borrower key break is proved on listEligibleAccounts in RWB-P1-E1018-APP

  Scenario: AC4 No history before the ALS batch of the business date is COMPLETED (new, D-RCV-60)
    Given the latest ALS row of v_ace_batch_status with status COMPLETED is for 2026-12-14
    And there is no COMPLETED ALS row for 2026-12-15
    When the read for "A-0001" and 2026-12-15 is called
    Then the answer is 409 application/problem+json with messageCode MSG-P1-001
    And the detail names DP01 and the date 2026-12-14
    And the body holds no history row and v_ace_efs_action is not read

  Scenario: AC5 The read creates no case, no account link, no party, no ledger entry and no decision record (new, D-RCV-60)
    Given recording fakes for rwb-case and rwb-decision
    When the read of "A-0001" for 2026-12-14 is called
    Then neither fake records a call
    And no row is written in schema rwb_source_data

  Scenario: AC6 The read answers ACE values only and holds no copy (new, D-RCV-60)
    Given the read of "A-0001" for 2026-12-14 has answered
    And the action_code of the view row of "EFS-SYN-0001" is then changed in the fixture
    When the same read is called again
    Then the second answer shows the new actionCode
    And the answer carries no case number, case status, case owner or queue

  Scenario: AC7 A view that does not answer inside 5 s yields 503 and no guessed value (new, D-RCV-60)
    Given v_ace_efs_action does not answer inside the 5 s statement timeout for "A-0001"
    When the read is called by a client with no shorter deadline
    Then the answer is 503 with messageCode MSG-GEN-006 and the detail names the ACE database
    And the body holds no history row

  Scenario: AC8 A caller without the right is refused and the refusal logs no key value (new, D-RCV-60)
    Given a workload identity other than rwb-integration
    When it calls the read for "A-0001" and 2026-12-14
    Then the answer is 403 with messageCode MSG-P4-002
    And no view is read and the refusal log line holds no accountKey and no personKey

  Scenario: AC9 Withdrawn (RD-P1-010): there is no candidate facts read

  Scenario: AC10 Withdrawn (RD-P1-010): there is no candidate facts read

  Scenario: AC11 No credential gives 401 and an operation not provided gives 404 (new, D-RCV-60)
    Given a request to GET /api/recovery/source-data/v1/efs-history?accountKey=A-0001&businessDate=2026-12-14 with no valid credential
    When it is sent
    Then the answer is 401 with messageCode MSG-P4-001 and no data
    And a request for GET /api/recovery/source-data/v1/entry-candidate-facts answers 404

  Scenario: AC12 A missing or malformed query value is refused (new, D-RCV-60)
    Given no accountKey on one request and businessDate "14-12-2026" on another
    When each request is sent
    Then each answers 400 with messageCode MSG-GEN-001 and field naming the parameter
    And no view is read

  Scenario: AC13 An account with no history in its period answers an empty list (new, D-RCV-60)
    Given account "A-0002" has an EFS assignment row and no v_ace_efs_action row in its collection period
    When the read for "A-0002" and 2026-12-14 is called
    Then the answer is 200 with rowCount 0, duplicateCount 0, an empty rows list and the collection period used

  Scenario: AC14 Without an assignment row the period opens at the earliest contact (new, D-RCV-60)
    Given account "A-0004" has no EFS assignment row and its earliest contact_at is 2026-09-01
    When the read for "A-0004" and 2026-12-14 is called
    Then collectionPeriodFrom is 2026-09-01 and collectionPeriodTo is 2026-12-14

  Scenario: AC15 The period boundaries are Asia/Bangkok dates and are inclusive (new, D-RCV-60)
    Given rows of "A-0001" at 2026-10-15 00:00:00, at 2026-12-14 23:59:59 and at 2026-12-15 00:00:00 Asia/Bangkok
    When the read for "A-0001" and 2026-12-14 is called
    Then the first two rows are answered and the third is not

  Scenario: AC16 With the flag off the operation is not served (new, D-RCV-60)
    Given flag rwb.dataengine.efs-handover-reads is off
    When the read for "A-0001" and 2026-12-14 is called
    Then the answer is 404 and no view is read

  Scenario: AC17 Every successful read is access logged without a clear personal value (new, D-RCV-60)
    When the read for "A-0001" and 2026-12-14 answers 200
    Then one access log entry records the caller identity, the operation and the time
    And no application or access log line holds the accountKey, a personKey or the query string in clear text

  Scenario: AC18 A null ACE value stays null (new, D-RCV-60)
    Given a history row of "A-0001" with null promise_amount, action_code_name and is_rpc
    When the read for "A-0001" and 2026-12-14 is called
    Then promiseAmount, actionCodeName and isRpc of that row are null, never 0, false or an empty text

  Scenario: AC19 No history before the EFS batch of the business date is COMPLETED (new, D-RCV-60)
    Given the ALS row of v_ace_batch_status for 2026-12-14 has status COMPLETED and the EFS row for 2026-12-14 has status FAILED
    When the read for "A-0001" and 2026-12-14 is called
    Then the answer is 409 application/problem+json with messageCode MSG-P1-001
    And the detail names DP05 and the last complete business date
    And the body holds no history row and v_ace_efs_action is not read
```

**Target reading.** Every assertion above is new, because this story owns no legacy criterion; each one tests only the history read and the gate around it. What the legacy story asserted of the case, the link, the decision record and the run summary is proved in RWB-P3-E2001-APP, RWB-P7-E2001-APP and RWB-P2-E2001-APP and in RWB-ITG-E2001-ITG. AC1 and AC2 read `v_ace_efs_action` through this service's own views and answer the collection period of the account rather than its whole history (DP-05; GAP-0588; ASM-0830). AC2 fixes the key that makes the caller's append idempotent: one row per `efs_record_key` and one key `EFS:<efs_record_key>` (DP-18; RD-P1-007). The fold count of the answer is this story's; the count of a repeated append is the run's, from the writer's 200 answers (RD-P1-007). AC4 and AC19 use the one completeness gate of the service over DP01 and DP05 (RD-P1-010, RD-P1-041, RD-P1-067); an incomplete EFS load refuses the read, so a partial history is never answered. AC5 and AC6 are the no-case and no-copy assertions (DP-01, DP-11). AC3, AC9 and AC10 are withdrawn with the candidate facts read and their IDs are not reused. Pending: the tie-break for two rows of one `efs_record_key` that differ in any column, owner data steward (NEW-GAP-S10-05).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The collection history of an account is read from `v_ace_efs_action` over its collection period, one entry per `efs_record_key`, with source system EFS; LOV-SOURCE is a closed list, so `sourceSystem` stays a fixed enum in the contract and a new value is a contract change | DL29; LOV-SOURCE; REQ-CHO-001; legacy BR5 |
| BR2 | A repeat hand-over for the same account and business date is ignored and counted: the writer answers 200 for a repeated business key and the run counts it | R-UNI-40; legacy BR6; RD-P1-007 |
| BR3 | The hand-over set is read from the ACE views for the ACE business date; the Workbench loads no source file and writes no ACE data | D-RCV-35 U1; ADR-010; REQ-DRI-013; legacy BR3 |
| BR4 | No history is answered for a business date unless `DailyCompletenessGate` answers COMPLETE for DP01 and DP05 | CTL-02; FEAT-CHO-05; BR-P1-014-4; legacy BR4; RD-P1-010; RD-P1-067 |
| BR5 | An account whose `person_key` or `account_key` has no ACE row is a REC-05 break of `listEligibleAccounts` (RWB-P1-E1018-APP); no key is invented. This story applies no REC-05 check | REC-05; DQ-040; D-RCV-35 U2; BR-P1-011-3; legacy BR8; RD-P1-010 |
| BR6 | One case per customer per product group is a rule of the run and of rwb-case; this story groups nothing and answers no product group | DL17; REQ-CHO-005; legacy BR2; RD-P1-010 |
| BR7 | A decision that cannot be written to the decision log does not proceed; this story writes no decision record | Principle 5; R-UNI-39; CTL-06; legacy BR7 |
| BR8 | The history is answered from the views at request time and never stored, and a repeated read reads the views again | D-RCV-35 U1; BR-P1-001-2; DP-05 |
| BR9 | The period runs from `assignment_start_date` to `assignment_end_date`, or to the business date while the assignment is open, as inclusive Asia/Bangkok dates, and no row after 23:59:59 of the business date is answered. Without an assignment row it opens at the earliest `contact_at`. Pending: which assignment row opens the period when an account has several, owner product owner with the data steward (GAP-0588) | ASM-0830; RD-P1-010 |
| BR10 | One answer row per `efs_record_key`; every folded view row adds 1 to `duplicateCount` | DP-18; ASM-0832 |

**Where each rule lives in the target.** BR1, BR9 and BR10 are the read of flow steps 5 and 6. BR2 is split by ownership: this service supplies the key `EFS:<efs_record_key>` and counts the view rows it folds; the writer answers the repeat and the run counts it (RD-P1-007). BR3 moves the read path to the views of rwb-source-data; no table of this service holds an EFS row (DP-01, DP-05). BR4 is `FreshnessHoldGate` calling `DailyCompletenessGate` (RD-P1-041). BR5 and BR6 are outside this story (RD-P1-010). BR7 is a statement: the decision record is rwb-decision's and this story writes none (DP-03). BR8 is the absence of any history table; the only derived value is the key, derived on every read.

### 9. State transitions

None in the case model. This story changes no case status, creates no case and links no account. It observes only the answer of the completeness gate.

| From | Event | Condition | To |
|---|---|---|---|
| ALS and EFS rows of the business date COMPLETED | a history read | The gate answers COMPLETE for DP01 and DP05 | 200 with the rows of the collection period |
| ALS or EFS row missing or not COMPLETED | a history read | The gate does not answer COMPLETE | 409 MSG-P1-001; no row |
| A repeated view row for one `efs_record_key` | a history read | The key is already in the answer | One row and one key; the duplicate is counted |

The completeness gate and the freshness states are written and owned by RWB-P1-E1015-APP and read here; this story writes neither.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-integration workload identity of the hand-over run | The only caller of `GET /efs-history`; writes nothing through it. Pending: authorise action name of the read (the `{action}` of MSG-P4-002), owner security architect (NEW-GAP-S10-06) |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the three ACE views and, through `FreshnessQuery`, the freshness stamp; holds no privilege outside its schema and the views |
| RW-DATASTEW, the ACE team, RW-PLATADM and every other human role | No call of this read: a human role gets 403 |
| RW-CASEOWN and the other case roles | Read the history on the case through the timeline of rwb-case once it is appended; they do not call these reads |
| rwb-source-data (P1) | Owns the read and the key; owns no case and no decision record |

No credential and no personal value appears in an answer, a log line or a test: the answer carries account keys, person keys, record keys, action codes, dates and amounts only. Every successful read is access logged (NFR-P1-009), and `accountKey` in the query string is redacted from application, gateway and access logs. Roles and their rights are held as data in rwb-access and reached through its authorise contract, never by a table read (DP-01; TSD P1 T6.2).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-108 | v_ace_efs_action | efs_record_key | Read |
| DF-ACE-109 | v_ace_efs_action | account_key | Read |
| DF-ACE-110 | v_ace_efs_action | person_key | Read |
| DF-ACE-111 | v_ace_efs_action | action_code | Read |
| DF-ACE-112 | v_ace_efs_action | action_code_name | Read |
| DF-ACE-113 | v_ace_efs_action | action_date | Read |
| DF-ACE-114 | v_ace_efs_action | contact_at | Read |
| DF-ACE-117 | v_ace_efs_action | is_call | Read |
| DF-ACE-118 | v_ace_efs_action | is_rpc | Read |
| DF-ACE-119 | v_ace_efs_action | is_ptp | Read |
| DF-ACE-120 | v_ace_efs_action | promise_status | Read |
| DF-ACE-122 | v_ace_efs_action | promise_date | Read |
| DF-ACE-123 | v_ace_efs_action | promise_amount | Read |
| DF-ACE-124 | v_ace_efs_action | collection_phase | Read |
| DF-ACE-131 | v_ace_efs_assignment | account_key | Read (the collection period) |
| DF-ACE-135 | v_ace_efs_assignment | assignment_start_date | Read (the collection period) |
| DF-ACE-136 | v_ace_efs_assignment | assignment_end_date | Read (the collection period) |
| DF-ACE-178 | v_ace_batch_status | source_system | Read by `DailyCompletenessGate` |
| DF-ACE-179 | v_ace_batch_status | business_date | Read by `DailyCompletenessGate` |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read by `DailyCompletenessGate` |
| DF-OPS-002 | data_product_load | product_code | Read through `FreshnessQuery` (`productStatus` only) |
| DF-OPS-007 | data_product_load | status | Read through `FreshnessQuery` (`productStatus` only) |
| DF-INT-018 | interaction | idempotency_key | Supplied as the key; written by the ledger writer of RWB-P1-E1066-APP |
| DF-INT-013 | interaction | source_system | Supplied as "EFS"; written by the ledger writer of RWB-P1-E1066-APP |

Field IDs are those in the Logical Data Model and Data Dictionary. Every `DF-ACE-` row is read in this service's own `recovery.v_ace_*` views and never from a `public` table, and never copied into a table of this service (DP-01, DP-05). The two `DF-INT-` rows are values this story derives and hands to the caller: the ledger row is written by the writer of RWB-P1-E1066-APP (DP-18). The ledger key column is varchar(120) and `action_code` varchar(10), while the view columns are varchar(255). Pending: the answer for a record key or action code longer than the ledger column, owner data architect (NEW-GAP-S10-07).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`. One read operation of the hand-over step. Build contract: rwb-source-data.yaml 5.1.0 (API Specification v7), to which this story's `GET /efs-history` fragment belongs (RD-P1-005, RD-P1-010).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/efs-history` | The EFS contact and promise history of one account over its collection period, up to the end of the business date, one row per `efs_record_key`, ordered by `contact_at` then `efs_record_key`, each with the key `EFS:<efs_record_key>`. Query: `accountKey` (required), `businessDate` (required, date) | The rwb-integration workload identity only | Idempotent: derived from the views on every call; no `Idempotency-Key` header (RD-P1-001) |

The answer is `EfsHistoryAnswer`: `accountKey`, `businessDate`, `sourceSystem` (always `EFS`, on the answer and not on the row), `collectionPeriodFrom`, `collectionPeriodTo`, `productStatus` of DP01 and DP05 as read through `FreshnessQuery`, `rowCount`, `duplicateCount`, and `rows` of `EfsHistoryRow` with `efsRecordKey`, `idempotencyKey`, `actionCode`, `actionCodeName`, `contactAt`, `isCall`, `isRpc`, `isPtp`, `promiseStatus`, `promiseDate`, `promiseAmount` (the decimal type of `Interaction.promiseAmount`), `collectionPhase` and `personKey`. `efsRecordKey`, `idempotencyKey` and `contactAt` are never null (a row with no `contact_at` is outside the date cut); every other row property is null when the ACE value is null. The field list is fixed by section 11.

The run appends each row with this mapping to `InteractionRequest` (RD-P1-007 rule 8; the append is RWB-P2-E2001-APP's):

| InteractionRequest property | Value from the history row |
|---|---|
| `eventCode` | `CONTACT`; `PROMISE` when `isPtp` |
| `occurredAt` | `contactAt` |
| `actionCode` | `actionCode` |
| `contactResult` | `RIGHT_PARTY` when `isRpc`, else empty |
| `promiseAmount`, `promiseDate` | `promiseAmount`, `promiseDate` |
| `actorType`, `actorRef` | `SERVICE`, `rwb-integration` |
| `sourceRef` | `EFS v_ace_efs_action` |
| `idempotencyKey` (body) | `EFS:<efsRecordKey>`; the writer sets `sourceSystem` EFS for this key form |

Errors are `application/problem+json` with the shared `Problem` schema (RD-P1-004): 400 MSG-GEN-001 with `field` for a missing or malformed `accountKey` or `businessDate`; 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-001 when the gate does not answer COMPLETE for DP01 and DP05, with the detail naming the blocking product and the last complete business date; 503 MSG-GEN-006 naming the ACE database. MSG-P2-007 is not returned by this read. The read is unpaged and answers one account per call; no truncated answer is ever returned (row cap: GAP-0589; ASM-0831; NEW-GAP-S10-04).

#### 12.2 REST operations consumed

None. This story calls no operation of another service at run time. `DailyCompletenessGate` and `FreshnessQuery` are in-service components of RWB-P1-E1015-APP (RD-P1-041).

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slides 15 and 43). This story publishes no event, writes no outbox row and adds no message schema; the event that starts the run is consumed by the run and not by this story.

#### 12.4 Events consumed

None. This story is reached over REST by the hand-over run and subscribes to nothing. rwb-source-data does not consume its own topic (RD-P1-003).

#### 12.5 Workflows and activities

None. The read is a synchronous REST step with a 2 s budget; this story starts no workflow and registers no activity. Activity `listEligibleAccounts` belongs to RWB-P1-E1018-APP (RD-P1-002); the run and its summary are RWB-P2-E2001-APP's (DP-10).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the read is called by the run (DP-10; Architecture v5 slide 44).

#### 12.7 Tables owned

None. This story creates no table and no column, adds no migration to the per-service sequence and writes no row.

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_efs_action`, `v_ace_efs_assignment`, `v_ace_batch_status` | `recovery` | ACE, read through the view contract of RWB-P1-E1069-APP | SELECT only, in-process, never copied (DP-05; ADR-010). Views are not tables and this story creates none |
| `data_product_load` | `rwb_source_data` | P1, written by RWB-P1-E1015-APP | Read through `FreshnessQuery` for `productStatus`; no row is written here |
| `interaction` | `rwb_source_data` | P1, shape and writer of RWB-P1-E1066-APP | Never written and never read: this story supplies the business key the run sends (DP-18; RD-P1-007) |
| `reconciliation_result` | `rwb_source_data` | P1, written by RWB-P1-E1011-APP | Not read and not written |
| `processed_event`, `idempotency_key`, `outbox_event` | `rwb_source_data` | PLT library objects, created in this service's schema | Not used: this story publishes no event and stores no response (DP-09) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case`, `case_account`, `case_party` and `decision_log_entry` are never named in this story's code or tests except as the objects it must not touch.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Provider fake of rwb-source-data.yaml 5.1.0, path `fakes/rwb-source-data/5.1.0/` | `GET /efs-history`, for the run of rwb-integration | One mapping per documented status: 200 (A-0001, 16 rows), 400, 401, 403, 409 MSG-P1-001, 503 MSG-GEN-006. Pending: the P1 contract story that lists this fake in its section 12.8, owner solution architect (NEW-GAP-S10-08) |
| ACE view fixture | `recovery.v_ace_efs_action`, `v_ace_efs_assignment` and `v_ace_batch_status` | The Background of section 7, one repeated `efs_record_key`, the boundary rows of AC15, A-0002 for AC13, A-0004 for AC14, the null row of AC18, the ALS and EFS rows of 2026-12-14 COMPLETED and none for 2026-12-15, and the AC19 variant with the EFS row FAILED |
| Gate and freshness stubs | `DailyCompletenessGate`, `FreshnessQuery` | COMPLETE for 2026-12-14 and not COMPLETE for 2026-12-15; DP01 and DP05 LOADED; HOLD naming DP05 for the AC19 variant |

The test fixtures are local: no live rwb-integration, rwb-case, rwb-decision or ACE database is needed to run the tests of section 16.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 read operation on `/api/recovery/source-data/v1` | None | OpenAPI 3.1; one hop, 2 s caller budget (DP-11); published in rwb-source-data.yaml 5.1.0 |
| Kafka | None | None | The topic and both events belong to RWB-P1-E1015-APP; the run consumes them |
| Temporal | None | None | No workflow, activity or Schedule in this story (DP-10) |
| File | None | None | No file is read or written |
| SQL view | None | 3 views of `recovery`, SELECT only | In-process, read-only login, 5 s statement timeout, never copied (DP-05; ADR-010) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `efs`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here). The build starts on Day 1 against the service baseline, the view contract of RWB-P1-E1069-APP and rwb-source-data.yaml 5.1.0, with stubs of the gate and freshness interfaces until RWB-P1-E1015-APP is merged.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | none (this story reads no parameter) |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | none (the product map left with the candidate facts read) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**One sentence per pattern.** DP-01 is the shape of this story: the history is read from the views and answered over the contract, and no column of ACE is copied into `rwb_source_data`. DP-03, DP-06, DP-07, DP-09 and DP-10 are statements here: no decision record, no parameter, no reference data, no event and no workflow. DP-05 is the read path: `v_ace_efs_action`, `v_ace_efs_assignment` and `v_ace_batch_status`, SELECT only through the `rwb_source_data` login (ADR-010). DP-11 is the hop: the run calls the read over REST with a 2 s budget against rwb-source-data.yaml 5.1.0. DP-18 is why the key lives here: the ledger is this service's table, so the read that names an EFS record names the key its writer dedupes on (`EFS:<efs_record_key>`). DP-19 is a statement: this story serves no screen.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `EfsHistoryController` | Controller | `GET /efs-history` on `/api/recovery/source-data/v1`; caller identity check; Problem answers; access log |
| `EfsHistoryReadService` | Service | The collection period, the date cut, the ordered read, the fold by `efs_record_key`, the key derivation and the duplicate count |
| `EfsHistoryRepository` | Repository | SELECT over `recovery.v_ace_efs_action` and `recovery.v_ace_efs_assignment`; no write method exists |
| `FreshnessHoldGate` | Gate | Calls `DailyCompletenessGate.check(businessDate, [DP01, DP05])` before the history is read; maps a refusal to 409 MSG-P1-001 |
| `EfsHistoryAnswer`, `EfsHistoryRow` | Published types | The records of 12.1 in `...sourcedata.api`; no case field |

**Migration (DP-15).** None. DP-15 is not claimed by this story: it adds no table, no column, no index and no version to the per-service Flyway sequence, because it stores nothing. The baseline tables it reads are created by RWB-P1-E1001-APP and the views it reads are created by RWB-P1-E1069-APP and its database story; an applied version is never edited by anyone, including this story.

**Database.** No object of `rwb_source_data` is created or written. The three views are ACE's, read through this service's login with SELECT only; `data_product_load` is read through `FreshnessQuery` and written by RWB-P1-E1015-APP. The history has no table: a second read of the same account and business date reads the view again (BR8).

**Configuration and reference data**

- The collection period is resolved from the EFS assignment rows and not from a parameter; the fallback of X6 applies when an account has no assignment row (GAP-0588; ASM-0830).
- The row cap per call (value pending, GAP-0589), the 2 s caller budget and the 5 s statement timeout are configuration of the read and of the view session (Architecture v5 slide 11; TSD P1 T6.3).
- The key format `EFS:<efs_record_key>` is fixed (RD-P1-007; ASM-0832) and is not a value a business person changes.
- The flag `rwb.dataengine.efs-handover-reads` gates the read; with it off the operation answers 404 and no view is read (RD-P1-045 item 4).

**Open decisions.** This story is built on the recommended options of the Decision Log: DL10 option A (the business lead drafts the Thai names per module one epic ahead; Legal and Compliance approve) and DL29 option B (a named list of outcomes for the case's collection period only, named by the business lead). This story applies no outcome filter; the filter belongs to the ledger intake (section 19). DL17 concerns the grouping, which is not in this story. Pending: assumption ID for DL29, owner product owner (DOR-RWB-P1-E2001-APP-18).

**Build steps**

1. `EfsHistoryAnswer`, `EfsHistoryRow` and the `GET /efs-history` fragment of rwb-source-data.yaml 5.1.0, with the provider fake.
2. `FreshnessHoldGate` over `DailyCompletenessGate`, with the 409 Problem of MSG-P1-001 (AC4, AC19, X1, X2).
3. `EfsHistoryRepository`: the assignment read for the collection period and the `v_ace_efs_action` read of that period with the date cut, ordered by `contact_at` and then `efs_record_key`, with the fallback of X6 (AC1, AC13, AC14, AC15).
4. `EfsHistoryReadService`: the fold, the duplicate count and the key on every row (AC1, AC2, AC18).
5. The access paths: 400, 401, 403, flag off, 503, and the access log with the query string redacted (AC7, AC8, AC11, AC12, AC16, AC17).
6. An architecture test that no class of the `efs` module writes a row, names a table of another service or references a case or decision type (AC5, DP-01).
7. A test that a second read reads the views again (AC6).
8. Run the provider verification of every fake mapping against the implementation (RD-P1-011).

**Done when.** The tests in section 16 pass, the history of A-0001 for 2026-12-14 answers 16 ordered rows with one key each, a repeated view row is folded and counted, the read refuses with 409 and MSG-P1-001 while the ALS or EFS batch of the business date is not COMPLETED, the provider fake verifies against the implementation, and no row is written anywhere.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | `DailyCompletenessGate` does not answer COMPLETE for DP01 and DP05 | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required query value is missing or malformed | Enter {field}. |
| MSG-P4-001 | No valid credential (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | A role without the right on the read | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A view does not answer inside 5 s, or answers an error | {system} is not available. Try again in a few minutes. |

The texts are those of Error and Message Standard v6, applied to the statuses of RD-P1-004. MSG-P1-001 names the blocking product and the last complete business date; MSG-GEN-006 names the ACE database; MSG-P4-002 names the action and never a key value. MSG-P2-007 needs a count of waiting accounts and is raised by the run, not by this read. Thai text follows decision DL10. No message carries a person name, an identity number, a phone number or an address.

### 15. Screens and states

No screen in this story, so it defines no screen state, field or mask. The case owner sees the appended history on SCR-04 Case timeline of rwb-case once the run has appended it (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-01 | AC1, BR1, BR3, BR5 | End to end | Synthetic account A-0001 with 14 contact rows and 2 promise rows in v_ace_efs_action |
| TC-P1-E2001-APP-01 | AC2 | Component | View fixture of 12.8 with one repeated view row |
| TC-P1-E2001-APP-02 | AC4, X1, X2 | Component | No COMPLETED ALS row for 2026-12-15 |
| TC-E2-001-05 | AC5, BR8 | End to end | Recording fakes for rwb-case and rwb-decision |
| TC-P1-E2001-APP-03 | AC6 | Component | A changed action_code in the fixture |
| TC-P1-E2001-APP-04 | AC7 | Component | View held past 5 s |
| TC-P1-E2001-APP-05 | AC8 | Contract | Another workload identity |
| TC-E2-001-17 | AC11 | Component | No credential; the withdrawn path |
| TC-P1-E2001-APP-06 | AC12 | Contract | Missing and malformed query values |
| TC-P1-E2001-APP-07 | AC13 | Component | A-0002 |
| TC-P1-E2001-APP-08 | AC14 | Component | A-0004 |
| TC-P1-E2001-APP-09 | AC15 | Component | Boundary rows |
| TC-P1-E2001-APP-10 | AC16 | Component | Flag off |
| TC-P1-E2001-APP-11 | AC17 | Component | Log inspection after a 200 |
| TC-P1-E2001-APP-12 | AC18 | Component | Row with null values |
| TC: to be added in Test Cases (new criterion of RD-P1-067) | AC19 | Component | EFS row FAILED, ALS row COMPLETED |
| TC-E2-001-18 | Legacy regression: AC2, BR6 (the repeat of an append is the ledger writer's) | Component | Fixture of section 7 |
| TC-E2-001-20 | Legacy regression: AC4, BR2 (the account link is rwb-case's) | Component | Fixture of section 7 |
| TC-E2-001-21 | Legacy regression: AC6, BR4 (the gap date and entry dates belong to the run and rwb-case) | Component | Fixture of section 7 |
| TC-E2-001-13 | Legacy regression: the decision log write (rwb-decision) | End to end | Fixture of section 7 |
| TC-E2-001-14 | Legacy regression: the refused second start (the run) | Component | Fixture of section 7 |
| TC-E2-001-11 | Section 12 operation, contract level | As in Test Cases v9 | Fake of 12.8 |
| TC-E2-001-12 | Section 12.7 table boundary | As in Test Cases v9 | Fixture of 12.8 |

The IDs follow Test Cases v9. The legacy rows TC-E2-001-02, -03, -04 and -06 to -10 belong there to the slices that own those legacy criteria (rwb-integration, rwb-case and rwb-decision stories and RWB-ITG-E2001-ITG) and are not cited by this story; TC-E2-001-15, -16 and -19 are retired with AC9, AC10 and AC3. TC-E2-001-05 now proves AC5 of this version; the customer missing from the ACE data is proved with the REC-05 breaks of `listEligibleAccounts` in RWB-P1-E1018-APP. AC19 has no row in Test Cases v9 and is to be added.

### 17. Guardrails

- No business value in code: the row cap and the time limits are configuration, and no product code, action code or date is written in code.
- No personal data in logs, events, tests or prompts: the answers carry keys, codes, dates and amounts; a contact name, an identity number, a phone number, an e-mail and an address are never read, never logged and never echoed in a problem body, and the test data is synthetic.
- ACE data only through this service's own `recovery.v_ace_*` views and the owner's contract, and only rwb-source-data reads the views (DP-05; ADR-010).
- No read of another service's tables: the ledger is written by its own writer, and `recovery_case`, `case_account`, `case_party` and `decision_log_entry` are never named in code or tests (DP-01, DP-11, DP-18).
- No copy of ACE data: the history is read at request time and stored nowhere; a repeated read reads the view again (BR8).
- The read is one hop with a 2 s budget and a breaker, against the published contract and its fake, and a slow view answers 503 instead of a partial answer (DP-11).
- A held business date is answered, not guessed: no row is served from a cache, a previous business date or a partial batch (BR4).
- An applied migration is never edited, and this story adds none (DP-15 is not claimed).
- Personal field reads are access logged, 100 percent (NFR-P1-009); the query string is redacted in logs; `personKey` and the promise fields are masked in UAT under Data Classification v5.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS and EFS batch and is read from ACE once the batch is complete | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40; BR-P1-014-4 | TC-E2-001-01, TC-E2-001-18, TC-P1-E2001-APP-02, TC-E2-001-21 |
| REQ-CHO-001 | The case carries the full contact and promise history of the collection period | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | DL29; R-UNI-40 | TC-E2-001-01, TC-E2-001-18, TC-E2-001-05 |
| REQ-CHO-005 | The Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-20, TC-E2-001-13 |
| REQ-RDF-003 | Collections contact history and promises are read from ACE through the EFS views | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | REC-05; DQ-040 | TC-P1-E2001-APP-02, TC-E2-001-05, TC-E2-001-21 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P2-E2001-CON | Contract | C: consumes `GET /efs-history` as published in rwb-source-data.yaml 5.1.0 |
| RWB-P2-E2001-APP | App development | The run that calls the history read, appends each row through `POST /cases/{caseId}/interactions`, counts written and skipped and writes the REC-01 result |
| RWB-P3-E2001-APP | App development | The case creation and the account link that this story never performs |
| RWB-P7-E2001-APP | App development | The decision record of the creation, which this story never writes |
| RWB-P1-E1018-APP | App development | Sibling in this service: activity `listEligibleAccounts` answers the candidates, the borrower key, the product group and the REC-05 breaks |
| RWB-P1-E1011-APP | App development | Sibling in this service: the REC-05 result row and the break list the data steward reads |
| RWB-P1-E1015-APP | App development | Sibling in this service: `DailyCompletenessGate`, `FreshnessQuery` and the freshness stamp |
| RWB-P1-E1066-APP | App development | Sibling in this service: the ledger writer that takes the `Idempotency-Key` this story supplies |
| RWB-P1-E1069-APP | App development | Sibling in this service: the three views and the `rwb_source_data` grant this story reads through |
| RWB-ITG-E2001-ITG | Integration | Proves the whole legacy key against the live rwb-integration, rwb-case, rwb-decision and this service |

### 19. Out of scope

- Creating or linking a case, issuing a case number and setting the entry date, the days past due at entry and the product group on the case (RWB-P3-E2001-APP).
- Writing the decision log entry of the creation and its inputs snapshot (RWB-P7-E2001-APP); this story writes no decision record (DP-03).
- The wait for a late EFS batch, the `handover.hold_until` limit and the late append of the history (the P2 hand-over run; RD-P1-067).
- The run itself: its start, the grouping, the filters, the account link, the ledger appends, the REC-01 result, the run summary and the refused second start (RWB-P2-E2001-APP; RD-P1-010 rule 7).
- Appending the history to the interaction ledger, the action-code filter of `efs_ledger_outcome` (DL29) and the repeat count of an append; this story supplies the key and counts only the view rows it folds (RD-P1-007; ASM-0832).
- The REC-05 breaks of the candidates (activity `listEligibleAccounts`, RWB-P1-E1018-APP) and the REC-05 result rows and break list (RWB-P1-E1011-APP).
- The freshness stamp, the stale flag, `AceDataReady` and `AceDataLate` (RWB-P1-E1015-APP); this story reads the stamp and publishes nothing.
- The views, the grants and the boundary rule (RWB-P1-E1069-APP and its database story); this story reads three views and creates none.
- The screen states of SCR-04 Case timeline and its gateway-bff composite route (RWB-PLT-N001-CON and the screen owners; DP-19).
- The candidates, the 90-day threshold, the exclusion at entry and the open-case filter (RWB-P1-E1018-APP and its callers; RD-P1-010).
- The real cross-service proof against the live run, rwb-case and rwb-decision (RWB-ITG-E2001-ITG).

### 20. Remaining delivery steps

- Size the story (DOR-RWB-P1-E2001-APP-16): delivery lead.
- Sign off the epic design: solution architect.
- Publish rwb-source-data.yaml 5.1.0 with `GET /efs-history` and mark the contract Done: API contract owner.
- Publish the provider fake `fakes/rwb-source-data/5.1.0/`: contract story owner (NEW-GAP-S10-08).
- Load the synthetic EFS view fixture and batch-status rows in DEV: data engineer.
- Add the test case for AC19 to Test Cases and the traceability matrix, and add the COMPLETED EFS row to the data of the existing E2001 cases: test lead.
- Add the `handover.hold_until` row to the parameter catalog (NEW-GAP-D4): rwb-integration owner with RW-COE.

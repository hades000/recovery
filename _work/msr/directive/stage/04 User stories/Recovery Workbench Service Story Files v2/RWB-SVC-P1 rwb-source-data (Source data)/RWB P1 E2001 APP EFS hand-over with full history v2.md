# RWB-P1-E2001-APP EFS hand-over with full history

SCB Collections and Recovery. Henka Group, 22 November 2026.
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
| Parallel lane | L-P1-S |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E2001-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P2-E2001-CON; RWB-P3-E1043-CON; RWB-PLT-E1027-CON; RWB-PLT-TE006-CON; RWB-PLT-E1071-CON; RWB-PLT-E1042-CON; RWB-PLT-E1043-CON; RWB-PLT-N001-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-002, FR-P1-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-001 for rwb-source-data. The legacy hand-over step read `recovery.v_ace_efs_action` and `recovery.v_ace_customer` in-process inside the JOB-02 chain of one deployable and appended the history to the interaction ledger itself; in the target the ACE facts that step consumes become two reads of this service on base `/api/recovery/source-data/v1` — the EFS history of one account and business date over `v_ace_efs_action`, and the borrower key and product group of the candidates of one business date over `v_ace_customer` and `v_ace_account` — reached by the hand-over run over REST, one hop with a 2 s budget (DP-05, DP-11). The history carries one stable key per `efs_record_key`, so the append of the ledger writer of RWB-P1-E1066-APP is idempotent and a repeat is counted under R-UNI-40 (DP-18), a borrower key that does not resolve is answered as a REC-05 break and never as a fact or a case (DP-01), and the freshness of DP01 and DP05 holds both reads until the ALS batch of the business date is COMPLETE (DP-05). The case, the decision record, the append and the run stay with RWB-P3-E2001-APP, RWB-P7-E2001-APP, RWB-P1-E1066-APP and RWB-P2-E2001-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2001-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 38 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the EFS contact and promise history of an account and the borrower key and product group of the hand-over candidates of a business date to be reads of rwb-source-data over the ACE views, refused while DP01 or DP05 is stale or before the ALS batch of the business date is COMPLETE, with one stable key per EFS record and with a borrower key that does not resolve answered as a REC-05 break**, so that **the hand-over run appends a history it did not assemble, each appended row is the repeat of one key rather than a second entry, and nothing is copied out of ACE into a Workbench table**.

This is the rwb-source-data slice of legacy RWB-E2-001. The legacy story created or linked a case, wrote the decision log entry, appended the EFS history and wrote the run summary in one step. Under D-RCV-60 that step is four owners, and this story delivers the ACE facts it consumes and nothing else:

- **the EFS history read** on base `/api/recovery/source-data/v1`: `GET /efs-history?accountKey=&businessDate=` over `v_ace_efs_action`, returning `efs_record_key`, `action_code`, `contact_at`, `is_ptp`, the RPC flag `is_rpc` where the ACE row carries it, `promise_date`, `promise_amount` and `collection_phase`, ordered by `contact_at` and then `efs_record_key`, restricted to the collection period of the account;
- **the hand-over candidate facts read**: `GET /entry-candidate-facts?businessDate=` returns the borrower key and product group of the candidates of one business date, as facts the grouping needs and never as a case. The candidate itself is `GET /entry-candidates?businessDate=&threshold=` of RWB-P1-E1018-APP: that story answers who is at or above the threshold and holds no case, and this story answers the borrower key and product group behind those candidates, one row per account key, without redefining the candidate rule;
- **the idempotency key of the history**: one row per `efs_record_key`, each carrying the key `EFS:<efs_record_key>`, so the caller's append through the ledger writer of RWB-P1-E1066-APP is idempotent and a repeat is answered and counted under R-UNI-40. This story supplies the key and counts the repeats it folds; the writer is RWB-P1-E1066-APP's and the run is RWB-P2-E2001-APP's;
- **the REC-05 business-key check for hand-over keys**: a `person_key` or an `account_key` with no row in `v_ace_customer` or `v_ace_account` is held on the break list for the data steward and the ACE team, the row is not created and no fact is invented, and the key is read again on the next complete batch;
- **the freshness hold**: nothing is read while DP01 or DP05 is STALE, or before the ALS batch for the business date is COMPLETE. The refusal carries MSG-P1-001 for the product and the date of the load in use and names MSG-P2-007 for the run that is held;
- **no case**: this story writes no `recovery_case`, `case_account`, `case_party` or decision record and copies no ACE column into a table of its own.

It owns no legacy acceptance criterion of RWB-E2-001. Legacy AC1 (the case from the ACE data) and AC4 (the account linked to the open case) belong to rwb-case under RWB-P3-E2001-APP; AC2 (the repeat run) and AC8 (the refused second start) belong to the run under RWB-P2-E2001-APP; AC3 and AC6 (the late batch and the next good batch) belong to the run and to the freshness stamp of RWB-P1-E1015-APP, with the read-side hold proved here; AC5 (the customer not in the ACE data) is proved here as the REC-05 hold and carried by the run; AC7 (the decision log write fails) is rwb-decision's under RWB-P7-E2001-APP. The cross-service proof is RWB-ITG-E2001-ITG. This story is therefore written with new criteria tagged D-RCV-60, each one testing only the reads above.

The shapes of the two operations as the run consumes them are declared by RWB-P2-E2001-CON, which lists the rwb-source-data elements of the hand-over step and their answers; this story implements them and its OpenAPI fragment is published with the service baseline. Which of the hand-over facts belongs to RWB-P1-E1018-APP and which to this story is a Work Package ruling and not a source statement (GAP-0592; ASM-0834).

### 2. Business rationale

Collections has the contact and promise history of an account before recovery does: EFS records the calls, the letters and the promises, ACE ingests them (INT-07, daily end of day), and the Workbench reads them through `v_ace_efs_action` and `v_ace_efs_assignment` (TSD P1 T5.1; REQ-RDF-003). Today a case starts after a weekly transfer with no history, and an officer rebuilds it by hand. Carrying the collection period of the account onto the case the morning after day 90 is what makes the case workable on its first day: the officer sees what was promised, when it was promised and whether the customer kept it (REQ-CHO-001; REQ-DRI-013; FSD P1 A2.2 DP05).

Under D-RCV-60 the Workbench loads no source data (D-RCV-35 U1), so the history cannot be read from a Workbench copy: it is read from the views at request time, one account and one business date at a time, and it is never stored. The read is a contract of rwb-source-data because this service owns the ACE view contract (Architecture v5 slides 15 and 41; ADR-010), and the run of rwb-integration owns the step that turns those facts into a case, a link and a ledger append (DP-11; DP-18). The split matters for two reasons. First, the ledger is this service's own table, so the key that makes the append idempotent must come from the same owner as the writer, not from the caller. Second, a borrower key that does not resolve is a data quality fact and not a case fact: it is answered with the key and the check, so the run holds the account, the data steward sees the break and the ACE team fixes the missing customer row (REC-05; DQ-040; FSD P1 A2.11.3 BR-P1-011-3).

**What D-RCV-60 changes.** Not the rationale and not one value: the 90-day entry point, the collection period, the action codes, the promise fields, the freshness gate and the REC-05 break keep their meaning. What changes is where the fact is read, who owns it and how it is reached — this service's own views and reads over `/api/recovery/source-data/v1`, one hop and 2 s, instead of an in-process call into the monolith (DP-05, DP-11).

**One read, no copy.** No table of this service holds an EFS row. The history is answered from the view on every request, and a second read of the same account and business date reads the view again; that is the whole of the no-copy rule of D-RCV-35 U1 and of FSD P1 A2.1 BR-P1-001-2. The only thing this story adds to an EFS fact is its stable key, which is derived from `efs_record_key` and stored nowhere.

### 3. Preconditions

Nothing in this list is a build dependency: this story is Day 1 and builds against the published baseline, the published view contract and the RWB-P2-E2001-CON fake, which is why its build dependency list is empty.

- The service baseline of rwb-source-data is published: schema `rwb_source_data`, the per-service Flyway sequence at its baseline version, `data_product` with DP01 to DP14 and `data_product_load` with its unique key on `(product_code, business_date)` (DP-01; the baseline of RWB-P1-E1001-APP and RWB-P1-E1015-APP, adopted as published artefacts and not as build dependencies).
- RWB-P1-E1069-APP's view contract is published and the five views this story reads are readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on `public`: `v_ace_efs_action`, `v_ace_efs_assignment`, `v_ace_customer`, `v_ace_account` and `v_ace_batch_status` (DP-02, DP-05; TSD P1 T3.3 and T6.3; ADR-010).
- RWB-P1-E1015-APP is done: `data_product_load` carries a LOADED or STALE row per product and business date, written from `v_ace_batch_status` only, and MSG-P1-001 and MSG-P2-007 exist with their texts (DP-05; FSD P1 A2.14).
- RWB-P2-E2001-CON is published with its fake: the rwb-source-data elements the hand-over step consumes, their answers, the error classes and the WireMock mappings of the run. This story builds against that contract and against its fake, and against no second draft of it (C).
- The candidate rule is RWB-P1-E1018-APP's operation `GET /entry-candidates?businessDate=&threshold=`: this story consumes the account keys it answers and never restates the threshold, the exclusion or the open-case filter (GAP-0592; ASM-0834).
- The product code to product group map (LOV-PRODUCT-CODE to LOV-PRODUCT, DL17) is loaded as reference rows and reached through the reference-data client library of RWB-PLT-E1043-CON, with contract RWB-P3-E1043-CON as its dependency; until the contract is published the read runs on a fixture (GAP-0593; ASM-0835).
- The caller is a service caller of the hand-over run with a workload identity token; the data steward reads the break answer with Platform administration R, and the ACE team reads it with the same right (TSD P1 T6.2; the SY-DATALOAD actor is retired).
- No approval is needed to build against a Draft contract baseline; RWB-P2-E2001-CON tags its baseline when its tests pass. This story starts on Day 1 and waits for nothing it builds.
- The boundary of the collection period, the single-or-paged shape of the history read and the HTTP answer of a held read are not stated by any source and are fixed as below (GAP-0588; ASM-0830; GAP-0589; ASM-0831).

### 4. Flow

1. The hand-over run of rwb-integration is started by `rwb.source-data.AceDataReady.v1` for the ALS source and business date D, once the EFS source carries the same business date (Architecture v5 slide 43 row 26; DP-09; the run is RWB-P2-E2001-APP's).
2. The run calls `GET /api/recovery/source-data/v1/entry-candidates?businessDate=D&threshold=90` on RWB-P1-E1018-APP's operation and receives the account keys at or above the threshold (DP-11; C RWB-P2-E2001-CON).
3. The run calls `GET /api/recovery/source-data/v1/entry-candidate-facts?businessDate=D` once, one hop and 2 s, and receives one row per candidate account key (DP-11).
4. `FreshnessHoldGate` reads `data_product_load` for DP01 and DP05 at D and `v_ace_batch_status` for the ALS row of D before any other read of this story runs; a product that is not LOADED or a batch that is not COMPLETE ends the call at step 9 with no row (§12.1, AC4).
5. `CandidateFactReadService` resolves each candidate's `account_key` in `v_ace_account` and its `person_key` in `v_ace_customer` through this service's own views, and reads the product group of the account from the product map (DP-05, DP-07).
6. A candidate whose `person_key` or `account_key` has no row is answered with `resolution` HELD, the check REC-05 and the key that failed to resolve; no key, no product group and no borrower fact is invented for it, and it is not dropped from the answer (AC3).
7. The run groups the resolved candidates by borrower key and product group and calls rwb-case; this story returns facts and takes no part in that grouping, which is the run's (RWB-P2-E2001-APP).
8. For each account the run is about to hand over, it calls `GET /api/recovery/source-data/v1/efs-history?accountKey=&businessDate=D`; the service resolves the collection period of the account from its EFS assignment rows, reads the `v_ace_efs_action` rows of that period, folds them to one row per `efs_record_key`, orders the answer by `contact_at` and then `efs_record_key`, and answers each row with its key `EFS:<efs_record_key>` (AC1, AC2).
9. A product not LOADED for D or an ALS batch not COMPLETE for D answers 409 with a problem body that names MSG-P1-001 for the product and the date of the load in use, and carries no history row and no candidate fact; the run reports the hold with MSG-P2-007 to the data steward (AC4; MSG-P1-001, MSG-P2-007).
10. The run appends each answered history row through the ledger writer of RWB-P1-E1066-APP with the `Idempotency-Key` EFS:<efs_record_key> this story derives: a second append of the same key is the same entry and the repeat is counted, and this story writes nothing (DP-18; R-UNI-40; AC2, AC5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | DP01 or DP05 is STALE for the business date | 409; no history row and no candidate fact; the problem body names the product and the date of the load in use | MSG-P1-001 | AC4 |
| X2 | The ALS batch for the business date is not COMPLETE | 409; no row of any kind is read from the views; the hold is named for the run | MSG-P1-001, MSG-P2-007 | AC4 |
| X3 | A `person_key` has no row in `v_ace_customer` | The candidate is answered HELD with check REC-05; no borrower fact is invented, no row is written | None | AC3 |
| X4 | An `account_key` has no row in `v_ace_account` | The candidate is answered HELD with check REC-05 and the account key; nothing is read further for it | None | AC3 |
| X5 | A repeated view row carries an `efs_record_key` already answered | The row is folded into the answer once and counted in the duplicate count; no second row and no second key | None | AC2 |
| X6 | The business date carries no EFS assignment row for the account | The period opens at the earliest `contact_at` of the account and closes at the business date; the answer says so | None | AC1 |
| X7 | A view does not answer inside 5 s, or answers an error | 503 with a problem body naming the ACE database as the unavailable system; nothing is guessed from a cache | MSG-GEN-006 | AC7, AC9 |
| X8 | A caller without the right calls either read | 403, and the refusal is logged without a key value | MSG-P4-002 | AC8, AC10 |

X1 to X6 are the read-side paths of the legacy exception rows X1, X2, X3 and X5 of RWB-E2-001 carried onto the split; the case, the link, the decision record and the run summary paths of those rows belong to RWB-P3-E2001-APP, RWB-P7-E2001-APP and RWB-P2-E2001-APP. X7 is the statement timeout of Architecture v5 slide 11 and TSD P1 T6.3. X8 is the access path of every read of this service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P2-E2001-CON and its fake, on the published baseline, the view contract of RWB-P1-E1069-APP and the freshness rows of RWB-P1-E1015-APP; needs no live rwb-integration, rwb-case or rwb-decision to start |
| Negotiable | The class split, the folding order and the key format are the squad's choice behind the contract; the view set, the field list, the ordering and the REC-05 outcome are fixed |
| Valuable | The run appends a history it did not assemble, from facts read once and keyed on the EFS record, and a broken borrower key reaches the steward instead of a case |
| Estimable | Two read operations, one service, one repository over four views, one freshness gate, one key derivation and one break answer |
| Small | Finished inside one sprint with its tests |
| Testable | Each criterion is one call against the contract fake, the view fixture and the freshness fixture, with no write and no second service |
| Day 1 | The story has no build dependency; it is reachable on the first day of wave 2 and its tests run against the published baseline and the fake |

### 7. Acceptance criteria

```gherkin
Feature: EFS hand-over with full history

  Background:
    Given business date 2026-12-14 and the ACE batch for ALS for it is COMPLETE at 05:20
    Given data product "DP01" and data product "DP05" carry status "LOADED" for 2026-12-14
    Given parameter "case.entry.dpd_threshold" is 90
    Given account "A-0001" belongs to customer "C-0001" with product group "MORTGAGE"
    Given v_ace_efs_action holds 14 contact rows and 2 promise rows for "A-0001" in its collection period

  Scenario: AC1 The 16 history rows of A-0001 come back ordered (new, D-RCV-60)
    When the hand-over run calls GET /api/recovery/source-data/v1/efs-history?accountKey=A-0001&businessDate=2026-12-14
    Then the answer holds 16 rows, one per efs_record_key, ordered by contact_at and then efs_record_key
    Then each row carries its efs_record_key, its action code, its contact time and source system "EFS"
    Then each of the 2 promise rows carries is_ptp true with its promise date and promise amount
    Then the answer names the collection period it read and the product status it read under

  Scenario: AC2 The same read for the same business date repeats without a duplicate (new, D-RCV-60)
    Given the read for "A-0001" and 2026-12-14 already answered 16 rows
    And v_ace_efs_action holds a second row of the same efs_record_key "EFS-SYN-0007" of "A-0001"
    When the run calls the read again for "A-0001" and 2026-12-14
    Then the answer holds the same 16 rows and no efs_record_key appears twice
    Then the folded row is counted in the duplicate count of the answer
    Then each row carries the key "EFS:<efs_record_key>", so the same append is a repeat the writer counts
    Then the read writes no row, publishes no event and starts no workflow

  Scenario: AC3 A borrower key with no v_ace_customer row is held on the REC-05 list (new, D-RCV-60)
    Given account "A-0003" reaches 90 days past due and holds person_key "P0099881", which has no row in v_ace_customer
    When the run asks for the candidate facts of 2026-12-14
    Then the answer returns "A-0003" with resolution "HELD", check "REC-05" and the key "P0099881"
    Then the answer holds no borrower fact, no product group fact and no invented key for "A-0003"
    Then no row is created and "A-0003" is asked again on the read for the next complete batch

  Scenario: AC4 A stale product or an incomplete ACE batch yields no history row (new, D-RCV-60)
    Given data product "DP01" carries status "STALE" with the load of 2026-12-13 still in use
    And the ACE batch for ALS for business date 2026-12-15 is not COMPLETE
    When the run calls the history read for "A-0001" and 2026-12-14 and then for "A-0001" and 2026-12-15
    Then the first call answers no history row and MSG-P1-001 for "DP01" with the date 2026-12-13
    Then the second call answers no history row and MSG-P1-001 for "DP01" with the date 2026-12-14
    Then the run is told the hold with MSG-P2-007

  Scenario: AC5 The read creates no case, no account link, no party and no decision entry (new, D-RCV-60)
    Given the rwb-case case creation contract mock records every call
    When the run reads the history of "A-0001" for 2026-12-14 and the candidate facts of 2026-12-14
    Then the case creation mock records no call and no case number is issued
    Then the read asks no operation that links an account, adds a party or writes a decision record
    Then case "RW-2026-000210" of customer "C-0002" stays unchanged at its status and its account link

  Scenario: AC6 The read answers ACE values only and holds no copy (new, D-RCV-60)
    Given the history of "A-0001" for 2026-12-14 was read
    When the same read is made again and the answer is inspected
    Then every row carries the value of its v_ace_efs_action row and the source system "EFS"
    Then the answer carries no case number, no case status, no case owner and no queue
    Then the second read reads v_ace_efs_action again, so this service holds no copy of the history

  Scenario: AC7 A view that does not answer inside 5 s yields 503 and no guessed value (new, D-RCV-60)
    Given v_ace_efs_action does not answer inside 5 s for A-0001 and 2026-12-14
    When the run calls GET /api/recovery/source-data/v1/efs-history?accountKey=A-0001&businessDate=2026-12-14
    Then the answer is 503 with a problem body naming the ACE database as the unavailable system and MSG-GEN-006
    Then the answer holds no history row and no value taken from a cache

  Scenario: AC8 A caller without the right on the read is refused and the refusal logs no key value (new, D-RCV-60)
    Given a caller whose role does not include the history read
    When the caller calls GET /api/recovery/source-data/v1/efs-history?accountKey=A-0001&businessDate=2026-12-14
    Then the answer is 403 with MSG-P4-002 naming the action the caller tried
    Then the refusal is logged without the account key value

  Scenario: AC9 A view behind the candidate facts read that does not answer inside 5 s or answers an error yields 503 and no guessed value (new, D-RCV-60)
    Given a view read for the candidate facts of 2026-12-14 does not answer inside 5 s or answers an error
    When the run calls GET /entry-candidate-facts?businessDate=2026-12-14
    Then the answer is 503 with a problem body naming the ACE database as the unavailable system and MSG-GEN-006
    Then the answer holds no candidate fact and no value taken from a cache

  Scenario: AC10 A caller without the right on the candidate facts read is refused and the refusal logs no key value (new, D-RCV-60)
    Given a caller whose role does not include the candidate facts read
    When the caller calls GET /entry-candidate-facts?businessDate=2026-12-14
    Then the answer is 403 with MSG-P4-002 naming the action the caller tried
    Then the refusal is logged without a key value

  Scenario: AC11 The provided operations answer 401 without a credential, 403 without the right and 404 for an operation not provided (new, D-RCV-60)
    Given a request to GET /api/recovery/source-data/v1/efs-history?accountKey=A-0001&businessDate=2026-12-14 carries no valid credential
    When the request is sent
    Then the answer is 401
    And a caller whose role does not include the history read gets 403 on the same request
    And a request to an operation not provided by this service answers 404
```

**Target reading.** Every assertion above is new, because this story owns no legacy criterion; each one tests only the two reads and the gate around them. What the legacy story asserted of the case, the link, the decision record and the run summary is proved in RWB-P3-E2001-APP, RWB-P7-E2001-APP and RWB-P2-E2001-APP and in RWB-ITG-E2001-ITG, and the legacy values are kept here: account A-0001, A-0002 and A-0003, customer C-0001 and C-0002, product group MORTGAGE and SSME, business date 2026-12-14, 14 contact rows and 2 promise rows, case RW-2026-000210 and the threshold 90. AC1 and AC2 read `v_ace_efs_action` through this service's own views and answer the collection period of the account rather than the whole history of the account (DP-05; the period is fixed by GAP-0588 and ASM-0830). AC2 fixes the key that makes the caller's append idempotent: one row per `efs_record_key` and one key `EFS:<efs_record_key>`, so the ledger writer of RWB-P1-E1066-APP sees a repeat rather than a second entry (DP-18; R-UNI-40). Who counts that repeat — this service or the writer — is not stated by any source; the count of a folded view row is answered here, the count of a repeated append is the writer's and the run reports it (GAP-0590; ASM-0832). AC3 answers the candidate facts read of `GET /entry-candidate-facts?businessDate=` and not the candidate rule, which is RWB-P1-E1018-APP's operation (GAP-0592; ASM-0834); the break it answers is the REC-05 key resolution of FSD P1 A2.11, whose break row for the business date is written by RWB-P1-E1011-APP and read by the data steward and the ACE team, so the shape of what this read answers is fixed here and the shape of the list row is not (GAP-0591; ASM-0833). AC4 replaces the legacy freshness hold with the two rows it reads: `data_product_load` for DP01 and DP05 and `v_ace_batch_status` for the ALS batch, both in this service, so the hold needs no call to the freshness story (DP-05; FSD P1 A2.14 BR-P1-014-4). AC5 and AC6 are the no-case and no-copy assertions: no operation of rwb-case is called and no table of another owner is read (DP-01, DP-11). The reads are one hop with a 2 s budget. The history read is one operation for one account and one business date in one call, with a configured row cap (value Not specified in the source documents (GAP-0589)) and no page parameter; a held read answers 409 with a problem body naming MSG-P1-001 and the date of the load in use, so the run can tell a hold from an empty history (GAP-0589; ASM-0831).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The collection history of an account is read from `v_ace_efs_action` over its collection period, one entry per `efs_record_key`, with source system EFS; LOV-SOURCE is a closed list, so `sourceSystem` stays a fixed enum in the contract and a new value is a contract change | DL29; LOV-SOURCE; REQ-CHO-001; legacy BR5 |
| BR2 | A repeat hand-over for the same account and business date is ignored and counted | R-UNI-40; legacy BR6 |
| BR3 | The hand-over set is read from the ACE views for the ACE business date; the Workbench loads no source file and writes no ACE data | D-RCV-35 U1; ADR-010; REQ-DRI-013; legacy BR3 |
| BR4 | No fact is read from a business date whose ALS batch is not COMPLETE, and none from a product that is STALE | CTL-02; FEAT-CHO-05; BR-P1-014-4; legacy BR4 |
| BR5 | An account whose `person_key` or `account_key` has no ACE row is held on the REC-05 business-key break and tried with the next complete batch; no key is invented | REC-05; DQ-040; D-RCV-35 U2; BR-P1-011-3; legacy BR8 |
| BR6 | One case per customer per product group is a rule of the run and of rwb-case; this story answers the borrower key and the product group and groups nothing | DL17; REQ-CHO-005; legacy BR2 |
| BR7 | A decision that cannot be written to the decision log does not proceed; this story writes no decision record | Principle 5; R-UNI-39; CTL-06; legacy BR7 |
| BR8 | The history is answered from the views at request time and never stored, and a repeated read reads the views again | D-RCV-35 U1; BR-P1-001-2; DP-05 |

**Where each rule lives in the target.** BR1 is the read of step 8: the view rows of the collection period, folded by key and ordered by contact time (DP-05). BR2 is split by ownership: this service supplies the key `EFS:<efs_record_key>` and counts the view rows it folds, and the run and the ledger writer count the repeat of an append (DP-18; R-UNI-40). BR3 keeps its wording and moves the read path: the views of rwb-source-data instead of the EFS history copy the monolith loaded, and no table of this service holds an EFS row (DP-01, DP-05). BR4 is `FreshnessHoldGate`, which reads this service's own `data_product_load` rows and `v_ace_batch_status`, so the gate is local and cannot disagree with the freshness stamp (DP-05). BR5 is the REC-05 answer of step 6: the key is answered, not invented, no row is created and the key returns on the next complete batch; the break row visible to the steward is RWB-P1-E1011-APP's (GAP-0591; ASM-0833). BR6 is why the second operation answers `person_key` and `product_group` and never a case, a case number or a link: the grouping and the one-case rule are the run's and rwb-case's (GAP-0592; ASM-0834). BR7 is a statement here: the decision record is rwb-decision's and this story writes none (DP-03). BR8 is the absence of any history table; the only derived value is the key, and it is derived on every read.

### 9. State transitions

None in the case model. This story changes no case status, creates no case and links no account. It reads two facts and holds one gate, and the only states it observes are the freshness status of a product and the resolution of a business key.

| From | Event | Condition | To |
|---|---|---|---|
| DP01 and DP05 LOADED for the business date | a history read | The ALS batch is COMPLETE | The answer carries the rows of the collection period |
| DP01 or DP05 STALE, or the ALS batch not COMPLETE | a history or candidate-facts read | The gate refuses | No row is answered; the refusal names MSG-P1-001 and the date of the load in use |
| A candidate account | a candidate-facts read | `person_key` and `account_key` both resolve in the views | Resolution RESOLVED with the borrower key and the product group |
| A candidate account | a candidate-facts read | `person_key` or `account_key` has no view row | Resolution HELD with check REC-05; the next complete batch asks again |
| A repeated view row for one `efs_record_key` | a history read | The key is already in the answer | One row and one key; the duplicate is counted |

The freshness states LOADED and STALE are written by RWB-P1-E1015-APP and read here; this story writes neither.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The hand-over run of rwb-integration, with a workload identity token | Reads the EFS history of an account and the candidate facts of a business date; writes nothing |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the four ACE views, `data_product_load` and `v_ace_batch_status`; holds no privilege outside its schema and the views |
| RW-DATASTEW, data steward and data product owner | Reads the break answer of the candidate facts for the business date (Platform administration R) |
| The ACE team | Reads the same break answer and fixes the missing customer or account row in ACE |
| RW-CASEOWN and the other case roles | Read the history on the case through the timeline of rwb-case once it is appended; they do not call these reads |
| RW-PLATADM, platform administrator | Reads the refused read and its problem body for the business date |
| rwb-source-data (P1) | Owns the two reads, the key and the REC-05 answer; owns no case and no decision record |

No credential and no personal value appears in an answer, a log line or a test: the answers carry account keys, person keys, record keys, action codes, dates and amounts only. Roles and their rights are held as data in rwb-access and reached through its authorise contract, never by a table read (DP-01; TSD P1 T6.2).

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
| DF-ACE-001 | v_ace_account | account_key | Read |
| DF-ACE-008 | v_ace_account | product_key | Read |
| DF-ACE-010 | v_ace_account | product_category | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-056 | v_ace_customer | person_key | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read (the hold) |
| DF-ACE-179 | v_ace_batch_status | business_date | Read (the hold) |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read (the hold) |
| DF-OPS-002 | data_product_load | product_code | Read (the hold) |
| DF-OPS-004 | data_product_load | business_date | Read (the hold) |
| DF-OPS-007 | data_product_load | status | Read (the hold) |
| DF-INT-018 | interaction | idempotency_key | Supplied as the key; written by the ledger writer of RWB-P1-E1066-APP |
| DF-INT-013 | interaction | source_system | Supplied as "EFS"; written by the ledger writer of RWB-P1-E1066-APP |

Field IDs are those in the Logical Data Model and Data Dictionary. Every `DF-ACE-` row is read in this service's own `recovery.v_ace_*` views and never from a `public` table, and never copied into a table of this service (DP-01, DP-05). `data_product_load` is this service's table, written by RWB-P1-E1015-APP and read here for the gate only. The two `DF-INT-` rows are values this story derives and hands to the caller: the ledger row itself is written by the ledger writer of RWB-P1-E1066-APP and this story writes no interaction row (DP-18). The candidate accounts themselves are answered by `GET /entry-candidates` of RWB-P1-E1018-APP; this story answers only the borrower key, the product group and the REC-05 resolution behind them.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1`. Two read operations of the hand-over step; the C dependency RWB-P2-E2001-CON declares the shapes the run consumes and this story implements them. Contract version: this story builds against `rwb-source-data.yaml` version 5.0.0 of Recovery Workbench API Specification v5; the two operations below are not yet in that file and are added to it as an addition under `/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/efs-history` | The EFS contact and promise history of one account over the collection period of that account, one row per `efs_record_key`, ordered by `contact_at` then `efs_record_key`, each with the key `EFS:<efs_record_key>` | The hand-over run of rwb-integration (workload identity) | Idempotent: the answer is derived from the views on every call and holds no stored state |
| GET | `/entry-candidate-facts` | The borrower key, the product group and the REC-05 resolution of every hand-over candidate of one business date, as facts and never as a case | The hand-over run of rwb-integration (workload identity); Platform administration R for the break answer | Idempotent: the answer is derived from the views on every call |

The history answer is `EfsHistoryAnswer`: `accountKey`, `businessDate`, `sourceSystem` (always `EFS`), `collectionPeriodFrom`, `collectionPeriodTo`, `productStatus` of DP01 and DP05 as read, `rowCount`, `duplicateCount`, and `rows` of `EfsHistoryRow` with `efsRecordKey`, `idempotencyKey`, `actionCode`, `actionCodeName`, `contactAt`, `isCall`, `isRpc`, `isPtp`, `promiseStatus`, `promiseDate`, `promiseAmount`, `collectionPhase` and `personKey`. The candidate-facts answer is `EntryCandidateFacts`: `businessDate`, `rowCount`, `heldCount`, and `rows` of `EntryCandidateFact` with `accountKey`, `personKey`, `productKey`, `productGroup`, `daysPastDue`, `dataAsOf`, `resolution` (RESOLVED or HELD) and `break` with `check` (REC-05), `keyType` and `key` where the resolution is HELD. Property names are a target choice and follow the naming of the P1 API appendix; the field list is fixed by section 11. The candidate rule — the threshold, the exclusion and the open-case filter — is `GET /entry-candidates?businessDate=&threshold=` of RWB-P1-E1018-APP and is cited here, never restated (GAP-0592; ASM-0834).

Errors are the RFC 9457 problem body: 400 for a missing or malformed `accountKey` or `businessDate` with MSG-GEN-001 naming the field, 401 without a token with MSG-P4-001, 403 without the right with MSG-P4-002, 409 when the gate refuses with MSG-P1-001 naming the product and the date of the load in use and MSG-P2-007 for the held run, and 503 when a view does not answer inside 5 s or answers an error, with MSG-GEN-006 naming the ACE database. The HTTP status of a held read is not stated by any source and is fixed here as 409 with no row in the body (GAP-0589; ASM-0831). Both reads answer the whole of one account and one business date in one call and are unpaged; a cap on the row count per call is configuration, and whether the history should be paged is left to the contract owner to confirm.

#### 12.2 REST operations consumed

None. This story calls no operation of another service at run time. The candidate rule arrives as the account keys RWB-P1-E1018-APP answers to the run, not as a call of this story; the product code to product group map is reference data reached through the reference-data client library of DP-07 and not through a run-time call; and the freshness gate reads this service's own `data_product_load` rows and `v_ace_batch_status` instead of calling the freshness story. The reference-data contract that supplies the map is not in this Work Package's contract list, so the map is a library read with a fixture until that contract is published (GAP-0593; ASM-0835; DP-07). The bindings of C from the legacy dependency are the run's contract RWB-P2-E2001-CON, which declares what this service answers and is faked for this story's tests.

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slides 15 and 43). This story publishes no event, writes no outbox row and adds no message schema; the event that starts the run is consumed by the run and not by this story.

#### 12.4 Events consumed

None. The hand-over run consumes `rwb.source-data.AceDataReady.v1` and holds it; this story is reached over REST by that run after the event and subscribes to nothing. Consuming `AceDataReady` here would create a second reader of the event and a second start path for the same business date, and the run's contract fixes the single consumer (DP-09; Architecture v5 slide 43 row 26).

#### 12.5 Workflows and activities

None. Both reads are synchronous REST steps that answer in one call with a 2 s budget, and this story starts no workflow and no activity. The task queue of this service is `rwb-source-data` in namespace `rwb-recovery` and it belongs to the other P1 stories; the run, its activities and its summary are RWB-P2-E2001-APP's (DP-10).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: the reads are called by the run when `AceDataReady` arrives and at no fixed time (DP-10; Architecture v5 slide 44).

#### 12.7 Tables owned

None. This story creates no table and no column, adds no migration to the per-service sequence and writes no row.

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_efs_action`, `v_ace_efs_assignment`, `v_ace_customer`, `v_ace_account`, `v_ace_batch_status` | `recovery` | ACE, read through the view contract of RWB-P1-E1069-APP | SELECT only, in-process, never copied (DP-05; ADR-010). Views are not tables and this story creates none |
| `data_product_load` | `rwb_source_data` | P1, written by RWB-P1-E1015-APP | Read for the gate; no row is written here |
| `interaction` | `rwb_source_data` | P1, shape and writer of RWB-P1-E1066-APP | Never written and never read: this story supplies the `Idempotency-Key` the writer keys on (DP-18) |
| `reconciliation_result` | `rwb_source_data` | P1, written by RWB-P1-E1011-APP | Not written: the REC-05 row for the business date is the reconciliation story's (GAP-0591; ASM-0833) |
| `processed_event`, `idempotency_key`, `outbox_event` | `rwb_source_data` | PLT library objects, created in this service's schema | Not used: this story publishes no event and stores no response (DP-09) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case`, `case_account`, `case_party` and `decision_log_entry` are never named in this story's code or tests except as the objects it must not touch.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P2-E2001-CON fake | The run's client stub of both reads, and the WireMock mappings of the hand-over step | The history of A-0001 with 16 rows and one repeated key; the candidate facts of 2026-12-14 with A-0001 and A-0002 RESOLVED and A-0003 HELD on REC-05; a 409 hold with MSG-P1-001 for a stale DP05 and for an incomplete ALS batch; a 503 from a view |
| ACE view fixture | `recovery.v_ace_efs_action`, `v_ace_efs_assignment`, `v_ace_customer`, `v_ace_account` and `v_ace_batch_status` | 14 contact rows and 2 promise rows for A-0001 in its collection period, one repeated `efs_record_key`, A-0002 for C-0002 with product group SSME, A-0003 with `person_key` P0099881 and no customer row, the ALS batch rows of 2026-12-14 COMPLETE and of 2026-12-15 absent |
| Freshness fixture | `data_product_load` | DP01 and DP05 LOADED for 2026-12-14; DP01 STALE with the load of 2026-12-13 in use; DP05 LOADED but the ALS batch absent |
| Product map fixture | The reference-data client library | MORTGAGE, HIRE_PURCHASE, SSME and UNSECURED for the product codes of the fixture; one product code with no map row (GAP-0593; ASM-0835) |

All four fakes are local: no live rwb-integration, rwb-case, rwb-decision or ACE database is needed to run the tests of section 16.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 read operations on `/api/recovery/source-data/v1` | None | OpenAPI 3.1; one hop, 2 s budget, breaker per client (DP-11); shapes declared by RWB-P2-E2001-CON |
| Kafka | None | None | The topic and both events belong to RWB-P1-E1015-APP; the run consumes them |
| Temporal | None | None | No workflow, activity or Schedule in this story (DP-10) |
| File | None | None | No file is read or written |
| SQL view | None | 5 views of `recovery`, SELECT only | In-process, read-only login, 5 s statement timeout, never copied (DP-05; ADR-010) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `efs`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here). The build starts on Day 1 against three published artefacts and no build dependency: the service baseline, the view contract of RWB-P1-E1069-APP and the fake of RWB-P2-E2001-CON.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**One sentence per pattern.** DP-01 is the shape of this story: the history is read from the views and answered over the contract, and no column of ACE is copied into `rwb_source_data`. DP-03 is a statement here: this story writes no decision record, and the record of a created case is written by rwb-case and rwb-decision through the local decision-record library. DP-05 is the read path itself: `v_ace_efs_action`, `v_ace_efs_assignment`, `v_ace_customer`, `v_ace_account` and `v_ace_batch_status`, SELECT only through the `rwb_source_data` login (ADR-010). DP-06 is a statement: this story reads no parameter, and the threshold arrives as the query argument of RWB-P1-E1018-APP's operation from the run that holds it. DP-07 is the product code to product group map, read as reference data through the client library and never as a constant in code. DP-09 is a statement: the reads publish no event and write no outbox row, and the inbox of the run absorbs a redelivered `AceDataReady`. DP-10 is a statement: no workflow, activity or Schedule is started here, because the step that runs is RWB-P2-E2001-APP's (Architecture v5 slide 44). DP-11 is the hop: the run calls the two reads over REST, one hop with a 2 s budget and a breaker, against the shapes of RWB-P2-E2001-CON and its fake. DP-18 is why the key lives here: the ledger is this service's own table, so the read that names an EFS record names the key its writer dedupes on (`EFS:<efs_record_key>`). DP-19 is a statement: this story serves no screen; the data steward and the ACE team read the break through the data quality route of gateway-bff and the case roles read the history on the case through rwb-case.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `EfsHistoryController` | Controller | The two operations of 12.1 on `/api/recovery/source-data/v1`; RFC 9457 problem details; the 409 hold |
| `EfsHistoryReadService` | Service | The collection period, the ordered read, the fold by `efs_record_key`, the key derivation and the duplicate count |
| `CandidateFactReadService` | Service | One row per candidate account key: the borrower key, the product group and the REC-05 resolution |
| `EfsHistoryRepository` | Repository | SELECT over `recovery.v_ace_efs_action` and `recovery.v_ace_efs_assignment`; no write method exists |
| `CustomerKeyResolver`, `AccountKeyResolver` | Resolver | The business-key check of `person_key` and `account_key` against `recovery.v_ace_customer` and `recovery.v_ace_account` (REC-05) |
| `ProductGroupMapClient` | Client library use | The product code to product group map as reference data; no group in code (DP-07) |
| `FreshnessHoldGate` | Gate | Reads `data_product_load` for DP01 and DP05 and `v_ace_batch_status` for the ALS batch of the business date before any other read runs |
| `EfsHistoryAnswer`, `EfsHistoryRow`, `EntryCandidateFacts`, `EntryCandidateFact` | Published types | The records of 12.1 in `...sourcedata.api`; no case field and no copy of an ACE column |

**Migration (DP-15).** None. DP-15 is not claimed by this story: it adds no table, no column, no index and no version to the per-service Flyway sequence, because it stores nothing. The baseline tables it reads are created by RWB-P1-E1001-APP and the views it reads are created by RWB-P1-E1069-APP and its database story; an applied version is never edited by anyone, including this story.

**Database.** No object of `rwb_source_data` is created or written. The five views are ACE's, read through this service's login with SELECT only; `data_product_load` is read for the gate and written by RWB-P1-E1015-APP. The history has no table: a second read of the same account and business date reads the view again (BR8).

**Configuration and reference data**

- The product code to product group map is reference data read through the client library, with its fixture until the reference-data contract is published (GAP-0593; ASM-0835; DP-07).
- The collection period is resolved from the EFS assignment rows and not from a parameter; the fallback of X6 applies when an account has no assignment row (GAP-0588; ASM-0830).
- The row cap per call, the 2 s client budget and the 5 s statement timeout are configuration of the reads and of the view session (Architecture v5 slide 11; TSD P1 T6.3).
- The key format `EFS:<efs_record_key>` is configuration of the derivation, not a value a business person changes; the format is a target choice (GAP-0590; ASM-0832).
- The flag `rwb.dataengine.efs-handover-reads` gates both reads at deployment; with it off the run receives 503 and starts no hand-over for the business date.

**Open decisions.** This story is built on the recommended options of the Decision Log: DL10 option A (the business lead drafts the Thai names per module one epic ahead; Legal and Compliance approve), DL17 option A (one case per customer per product, with the accounts linked) and DL29 option B (a named list of outcomes for the case's collection period only, named by the business lead). This story applies no outcome filter; the filter belongs to the ledger intake (section 19). Assumption ID for DL17 and DL29: Not specified in the source documents (DOR-RWB-P1-E2001-APP-18).

**Build steps**

1. The two published types and the OpenAPI fragment of 12.1, taken from RWB-P2-E2001-CON and published with the service baseline (C).
2. `FreshnessHoldGate` over `data_product_load` and `v_ace_batch_status`, with the 409 problem body of MSG-P1-001 and MSG-P2-007 (AC4, X1, X2).
3. `EfsHistoryRepository`: the assignment read for the collection period and the `v_ace_efs_action` read of that period, ordered by `contact_at` and then `efs_record_key`, with the fallback of X6 (AC1, X6).
4. `EfsHistoryReadService`: the fold by `efs_record_key`, the duplicate count and the key `EFS:<efs_record_key>` on every row (AC1, AC2).
5. `CandidateFactReadService` with `CustomerKeyResolver`, `AccountKeyResolver` and the product map: one row per candidate account, RESOLVED or HELD with check REC-05, no invented key (AC3, X3, X4).
6. The error paths: 400 with MSG-GEN-001 naming the field, 403 with MSG-P4-002, 503 with MSG-GEN-006 for a view that does not answer inside 5 s (X7, X8).
7. An architecture test that no class of the `efs` module writes a row, names a table of another service or references a case or decision type (AC5, DP-01).
8. A test that a second read of the same account and business date reads the views again and answers the same rows, so the no-copy rule is asserted and not assumed (AC6).
9. Tests for AC1 to AC6 against the four fakes of 12.8, plus the regression rows of section 16 where the fixture of the owning slice is available.

**Done when.** The tests in section 16 pass, the history of A-0001 for 2026-12-14 answers 16 ordered rows with one key each against the run's fake, a repeated view row is folded and counted, a HELD candidate carries its REC-05 key and no invented fact, both reads refuse with 409 and MSG-P1-001 while DP01 or DP05 is STALE or the ALS batch is incomplete, and no row is written anywhere.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A product is stale, or the ALS batch of the business date is not COMPLETE | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | The run is held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-GEN-001 | A required query value is missing or malformed | Enter {field}. |
| MSG-P4-001 | No token | Your session has ended. Sign in again. |
| MSG-P4-002 | A role without the right on the read | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A view does not answer inside 5 s, or answers an error | {system} is not available. Your request is queued and will be retried. |

The six texts are the legacy texts of RWB-E2-001 and of the P1 module carried unchanged, with MSG-P1-001 in the ACE batch wording that the P1 stories of this run publish; MSG-P1-001 and MSG-P2-007 are published by the freshness story and raised here in the refusal body with the date of the load in use, MSG-GEN-006 names the ACE database as the failed system, and MSG-P4-002 names the action the caller tried and never a key value. Thai text for each message follows decision DL10. No message carries a person name, an identity number, a phone number or an address.

### 15. Screens and states

No screen in this story. The data steward and the ACE team see the REC-05 break of AC3 in the break view of SCR-45 Data quality, which reads the reconciliation result of RWB-P1-E1011-APP through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON); the case owner sees the appended history on SCR-04 Case timeline of rwb-case once the run has appended it. This story renders neither: it answers a 409 with MSG-P1-001 in the refusal state of whoever asked, and it fixes no field, state or mask of any screen. SCR-04 states: loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-2359). SCR-45 states: loading as in Screen Specifications v1; empty, error and no access: Not specified in the source documents (CG-ALL-2360).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-001-09 | Access — regression evidence: the rerun seam belongs to RWB-P1-E1018-APP and the run | Component | RW-CASEOWN calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |
| TC-E2-001-01 | AC1, BR1, BR3, BR5 | End to end | Synthetic account A-0001 with 14 contact rows and 2 promise rows in v_ace_efs_action |
| TC-E2-001-02 | AC2, BR6 — partly regression evidence: the repeat of an append is the ledger writer's and the repeat of the run is RWB-P2-E2001-APP's | End to end | Same business date run twice |
| TC-E2-001-03 | AC3, BR4 — regression evidence: the hold is asserted here on AC4, and the run's hold and alert are RWB-P2-E2001-APP's | End to end | ACE batch for ALS of 2026-12-15 not COMPLETE |
| TC-E2-001-04 | AC4, BR2 — regression evidence: the account link belongs to rwb-case under RWB-P3-E2001-APP | End to end | Customer C-0002 with an open SSME case |
| TC-E2-001-05 | AC5, BR8 | End to end | Account A-0003 with no row in v_ace_customer |
| TC-E2-001-06 | AC6, BR4 — regression evidence: the gap date and the entry dates belong to RWB-P2-E2001-APP and rwb-case | End to end | Good batch on 2026-12-17 after a missed day |
| TC-E2-001-07 | run by RWB-P7-E2001-APP (legacy AC7, BR7) — regression evidence: the decision log write belongs to rwb-decision | End to end | Decision log store stopped |
| TC-E2-001-08 | run by RWB-P2-E2001-APP (legacy AC8) — regression evidence: the second start is refused by the run | End to end | JOB-02 running |
| TC-E2-001-10 | Principle 5 — regression evidence: the proof belongs to rwb-decision and to RWB-ITG-E2001-ITG | NFR | Decision log write forced to fail during a run of 50 synthetic accounts; no case is created without its entry |
| TC-E2-001-11 | Section 12 — each operation and activity of section 12, contract level | Contract | Contract fakes of RWB-P2-E2001-CON for the two reads and the gate |
| TC-E2-001-12 | Section 12.7 — boundary of the tables read and of the tables not written | Component | Views of the recovery schema and data_product_load are read; a write attempt on any of them is refused |
| TC-E2-001-13 | AC7, X7 | End to end | View v_ace_efs_action held past 5 s for A-0001 |
| TC-E2-001-14 | AC8, X8 | Component | Caller whose role lacks the history read calls GET efs-history for A-0001; refused with MSG-P4-002 |
| TC-E2-001-15 | AC9, X7 | End to end | View v_ace_customer held past 5 s for the candidate facts of 2026-12-14 |
| TC-E2-001-16 | AC10, X8 | Component | Caller whose role lacks the candidate facts read calls GET /entry-candidate-facts?businessDate=2026-12-14; refused with MSG-P4-002 |
| TC-E2-001-17 | AC11 | Component | Request to efs-history for A-0001 without a credential, with a role lacking the read, and to an operation not provided by the service |

The ten legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end", "Access" to "Component" and "Resilience" to "NFR", as in the other stories of this run. TC-E2-001-01 and TC-E2-001-05 are the two rows this story runs as its own evidence, and TC-E2-001-02, TC-E2-001-03 and TC-E2-001-06 carry the read-side assertions of AC2 and AC4 inside the same rows. The other five rows are kept as regression evidence for the slices of this legacy key that own those criteria and for RWB-ITG-E2001-ITG, and they run again there against the live contracts. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the product group comes from the reference map, the threshold and the hold time are the run's and the parameters contract's, the row cap and the budgets are configuration, and no product code, action code, product group or date is written in code.
- No personal data in logs, events, tests or prompts: the answers carry keys, codes, dates and amounts; a contact name, an identity number, a phone number, an e-mail and an address are never read, never logged and never echoed in a problem body, and the test data is synthetic.
- ACE data only through this service's own `recovery.v_ace_*` views and the owner's contract, and only rwb-source-data reads the views (DP-05; ADR-010).
- No read of another service's tables: the candidate rule arrives over the contract of RWB-P1-E1018-APP, the ledger is written by its own writer, and `recovery_case`, `case_account`, `case_party` and `decision_log_entry` are never named in code or tests (DP-01, DP-11, DP-18).
- No copy of ACE data: the history is read at request time and stored nowhere; a repeated read reads the view again (BR8).
- The read is one hop with a 2 s budget and a breaker, against the published contract and its fake, and a slow view answers 503 instead of a partial answer (DP-11).
- A held business date is answered, not guessed: no row is served from a cache, a previous business date or a partial batch (BR4).
- An applied migration is never edited, and this story adds none (DP-15 is not claimed).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-013 | Hand-over arrives in the daily ALS and EFS batch and is read from ACE once the batch is complete | Program 5.2; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | R-UNI-40; BR-P1-014-4 | TC-E2-001-01, TC-E2-001-02, TC-E2-001-03, TC-E2-001-06 |
| REQ-CHO-001 | The case carries the full contact and promise history of the collection period | Program 5.3; Epic 2 3.2 | FEAT-CHO-01 | 6.1 Take over the case at 90 days past due | DL29; R-UNI-40 | TC-E2-001-01, TC-E2-001-02, TC-E2-001-05 |
| REQ-CHO-005 | The Workbench is the system of record for case state after hand-over | Program 5.3; Epic 2 3.2 | FEAT-CHO-04 | 6.1 Take over the case at 90 days past due | R-UNI-39 | TC-E2-001-04, TC-E2-001-07, TC-E2-001-10 |
| REQ-RDF-003 | Collections contact history and promises are read from ACE through the EFS views | Program 5.1; Epic 2 3.2 | FEAT-CHO-05 | 6.1 Take over the case at 90 days past due | REC-05; DQ-040 | TC-E2-001-03, TC-E2-001-05, TC-E2-001-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P2-E2001-CON | Contract | C: declares the rwb-source-data elements the hand-over step consumes, their answers and the fakes; this story implements them |
| RWB-P2-E2001-APP | App development | The run that calls both reads, creates the case path, appends the history through the ledger writer, counts the repeats and writes the REC-01 result |
| RWB-P3-E2001-APP | App development | The case creation and the account link that this story never performs |
| RWB-P7-E2001-APP | App development | The decision record of the creation, which this story never writes |
| RWB-P1-E1018-APP | App development | Sibling in this service: `GET /entry-candidates` answers the candidate rule this story does not restate |
| RWB-P1-E1011-APP | App development | Sibling in this service: the REC-05 result row and the break list the data steward reads |
| RWB-P1-E1015-APP | App development | Sibling in this service: `data_product_load` and the LOADED and STALE states the gate reads |
| RWB-P1-E1066-APP | App development | Sibling in this service: the ledger writer that takes the `Idempotency-Key` this story supplies |
| RWB-P1-E1069-APP | App development | Sibling in this service: the five views and the `rwb_source_data` grant this story reads through |
| RWB-ITG-E2001-ITG | Integration | Proves the whole legacy key against the live rwb-integration, rwb-case, rwb-decision and this service |

### 19. Out of scope

- Creating or linking a case, issuing a case number and setting the entry date, the days past due at entry and the product group on the case (RWB-P3-E2001-APP).
- Writing the decision log entry of the creation and its inputs snapshot (RWB-P7-E2001-APP); this story writes no decision record (DP-03).
- The run itself: the `AceDataReady` intake, the grouping, the threshold, the open-case exclusion, the account link, the REC-01 result, the run summary and the refused second start (RWB-P2-E2001-APP; `GET /entry-candidates` of RWB-P1-E1018-APP).
- Appending the history to the interaction ledger, the action-code filter of `efs_ledger_outcome` (DL29, the intake rule of RWB-P1-E1066-APP and RWB-P1-E1067-APP) and the repeat count of an append; this story supplies the key and counts only the view rows it folds (GAP-0590; ASM-0832).
- The REC-05 result row and the break list of the business date (RWB-P1-E1011-APP); this story answers the break per key and writes no row (GAP-0591; ASM-0833).
- The freshness stamp, the stale flag, `AceDataReady` and `AceDataLate` (RWB-P1-E1015-APP); this story reads the stamp and publishes nothing.
- The five views, the grants and the boundary rule (RWB-P1-E1069-APP and its database story); this story reads the views and creates none.
- The screen states of SCR-04 Case timeline and SCR-45 Data quality and the gateway-bff composite routes (RWB-PLT-N001-CON and the screen owners; DP-19).
- The candidate rule itself — the 90-day threshold, the exclusion at entry and the open-case filter — which is RWB-P1-E1018-APP's operation and not restated here (GAP-0592; ASM-0834).
- The real cross-service proof against the live run, rwb-case and rwb-decision (RWB-ITG-E2001-ITG).

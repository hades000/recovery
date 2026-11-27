# RWB-P1-E2008-APP Payment matching with the missed payment event

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E2008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P1-U |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P1-E2008-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2008-CON |
| Contract version | v1, base path /api/recovery/source-data/v1 (DP-13) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (no FR mapped to REQ-CHO-007, REQ-CHO-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-008 for rwb-source-data. The legacy matcher (JOB-07) read the payments of the business date, the next installment date of each plan account and the ALS batch status in-process from the monolith's views, then matched each payment to a plan installment through package `PAYMENT_MATCH`, wrote the proceeds row and raised `PaymentMissed` when a due installment had not arrived. Under D-RCV-60 that data is answered by this service over base `/api/recovery/source-data/v1`: the payments of one business date over `v_ace_payment` and the installment facts of one account over `v_ace_account`, both behind the batch and freshness gate that this service already owns (DP-05, DP-11, DP-13). The matcher, the proceeds row, the rule package, the decision record and both events stay with rwb-payment, rwb-decision and rwb-treatment (DP-03, DP-04, DP-10); this story answers two reads and one gate, stores nothing, evaluates no rule and publishes no event (DP-01, DP-09, DP-15). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P1-E2008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 55 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **recovery developer (RW-TRIBE)**, I want **the payments of one business date and the next installment date of one account to be reads of rwb-source-data over its own ACE views, refused while the ALS batch of the business date is not COMPLETE or DP01 is STALE, each payment answered once under its `payment_code` with the exact amount and the batch status it was read under**, so that **the payment matching run matches against one copy of the ACE payment rows, a held business date is answered as a hold and never as an empty day, and no payment, installment date or batch fact is copied out of ACE into a Workbench table**.

This is the rwb-source-data slice of legacy RWB-E2-008. The legacy story ran one job that read the payments, read the next installment date of each plan account, read the ALS batch status, evaluated package `PAYMENT_MATCH`, wrote the proceeds row, called the treatment record, published `ProceedsMatched` and `PaymentMissed`, and wrote the run summary. Under D-RCV-60 that job is four owners and a contract, and this story delivers only the ACE facts it consumes and the gate they pass through:

- **the payments read** on base `/api/recovery/source-data/v1`: `GET /payments?businessDate=` over `v_ace_payment`, answering one row per `payment_code` with `paymentCode`, `accountKey`, `paymentDate`, `paymentAmount` and `dataAsOf`, ordered by `paymentCode`, with `rowCount`, the status of the ALS batch row of that business date, and the data-product status the rows were read under; both reads are unpaged, the row cap per call is configuration, and a repeated `payment_code` folds into its one row;
- **the installment-facts read**: `GET /accounts/{accountKey}/installment-facts?businessDate=`, answering `nextInstallmentDate` from `v_ace_account` at that business date, together with `accountKey`, `productKey`, `daysPastDue` and `dataAsOf`, which are the account facts the matcher needs to build its facts for the rule package;
- **the batch and freshness gate**: a read whose ALS batch for the business date is not COMPLETE, or whose DP01 is STALE, answers 409 with MSG-P1-001 naming the product and the date of the load in use and MSG-P2-007 for the held run, and answers no row of any kind. The gate reads this service's own `data_product_load` rows and `v_ace_batch_status`, so it cannot disagree with the freshness stamp of RWB-P1-E1015-APP;
- **no proceeds row, no case lookup, no rule evaluation, no event**: this story writes no `proceeds` row, resolves no case, evaluates no package row, and publishes neither `PaymentMissed` nor `ProceedsMatched`. The `proceeds` table is rwb-payment's (ownership map: `proceeds` → P8), the plan and its installment amount are rwb-treatment's (`treatment` → S2), and the decision record of a match is rwb-decision's (`decision_log_entry` → P7).

It owns no legacy acceptance criterion of RWB-E2-008, which is why its criteria are new and tagged D-RCV-60. **AC1** (a payment matched to the installment, and the treatment record that records it) belongs to **RWB-P8-E2008-APP**, **RWB-S2-E2008-APP** and **RWB-P7-E2008-APP** for the rule result and the decision log. **AC2** (a missed payment) belongs to **RWB-P8-E2008-APP**, and P3 applies the plan state it raises. **AC3** (the exception list of an unmatched payment) belongs to **RWB-P8-E2008-APP**. **AC4** (a payment on an account with no open case, and the REC-05 break row) belongs to **RWB-P8-E2008-APP**, and **RWB-P1-E1011-APP** writes the break row. **AC5** (the ACE batch is not complete) is proved here on the read side only: this story answers the hold, and the run's refusal for the business date is **RWB-P8-E2008-APP**'s. **AC6** (a repeated run) belongs to **RWB-P8-E2008-APP**. **AC7** (the window boundary) belongs to **RWB-P8-E2008-APP** and **RWB-P7-E2008-APP**. **AC8** (no package in force) belongs to **RWB-P7-E2008-APP** and **RWB-P8-E2008-APP**. **AC9** (the decision log naming the rule and the package version) belongs to **RWB-P7-E2008-APP**. The cross-service proof is **RWB-ITG-E2008-ITG**.

The shapes of the two operations as the matching run consumes them are declared by RWB-P8-E2008-CON, which lists the rwb-source-data elements of the payment-matching step and their answers; this story implements them and publishes its OpenAPI fragment with the service baseline. The resource names, the query parameters, the response entities, the ordering, the row cap and the error status set are a target choice and not a legacy value, because the legacy read was an in-process Java interface with no path and no status code (GAP-0599; ASM-0841; GAP-0601; ASM-0843).

### 2. Business rationale

Payments are matched to plans by hand today, and a missed installment is found weeks later, after the cure period has gone (legacy RWB-E2-008 §2). ACE ingests the ALS payments (INT-02, daily end of day) and the Workbench reads them through `v_ace_payment` (TSD P1 T5.1; REQ-RDF-002), so the facts the matcher needs are already in ACE, current to the previous working day, and the only question is who answers them. Under D-RCV-60 the answer is rwb-source-data: it owns the ACE view contract and the freshness stamp (Architecture v5 slides 15 and 41; ADR-010), and no other service reads the views (Architecture v5 slides 11 and 12). Reading the same rows from a second copy would give the matcher a different payment set from the one the reconciliation of the same day counts.

The split matters because the matcher is not the reader. The matcher belongs to rwb-payment, which owns payment and proceeds matching, and it runs as JOB-07, an event-triggered workflow started by `AceDataReady` (Architecture v5 slide 44 row JOB-07; slide 17, rwb-payment "Source data: payments for business date"; Temporal and Drools design slide 9). This service owns the row facts and the gate, and it must answer them in the shape the matcher consumes: one row per `payment_code` with the exact amount, the next installment date of the account as of the same business date, and the batch status the rows were read under. Everything else the legacy job did — the EXACT row of package `PAYMENT_MATCH`, rule `R-RES-26`, the proceeds row, `ProceedsMatched`, `PaymentMissed` and the run summary — is proved in the slices that own it.

**What D-RCV-60 changes.** Not the rationale and not one value: the case, the account, the plan, the installment amount, the next installment date, the business date, the three payments and the batch date keep their meaning and their values. What changes is where the row is read, who owns it and how it is reached — this service's own views and two reads over `/api/recovery/source-data/v1`, one hop with a 2 s budget, instead of an in-process call into the monolith (DP-05, DP-11, DP-13).

**Two reads, no copy.** No table of this service holds a payment row or an installment date. Both answers are derived from the views on every request, and a second read of the same business date reads the views again; that is the whole of the no-copy rule of D-RCV-35 U1 and of FSD P1 A2.1 BR-P1-001-2 (BR4). The only thing this story adds to an ACE row is its place in one ordered answer, and that is derived and stored nowhere.

### 3. Preconditions

Nothing in this list is a build dependency: this story is Day 1 and builds against the published baseline, the published view contract and the RWB-P8-E2008-CON fake, which is why its build dependency list is empty.

- The service baseline of rwb-source-data is published: schema `rwb_source_data`, the per-service Flyway sequence at its baseline version, `data_product` with DP01 to DP14 and `data_product_load` with its unique key on `(product_code, business_date)` (DP-01; the baseline of RWB-P1-E1001-APP and RWB-P1-E1015-APP, adopted as published artefacts and not as build dependencies).
- RWB-P1-E1069-APP's view contract is published and the three views this story reads are readable through the `rwb_source_data` login, which holds SELECT on the 30 `recovery.v_ace_*` views and no privilege on `public`: `v_ace_payment`, `v_ace_account` and `v_ace_batch_status` (DP-02, DP-05; TSD P1 T3.3 and T6.3; ADR-010).
- `v_ace_batch_status` is a Section B view and `v_ace_payment` and `v_ace_account` are Section A views (TSD P1 T3.3 rows 1, 2 and 17; T3.2). Until RWB-ACE-001 lands, every source-fed product shows STALE with no business date and no data job starts (TSD P1 T3.7), so the gate of this story refuses every business date and answers no row rather than an empty day (BR3).
- RWB-P1-E1015-APP is done: `data_product_load` carries a LOADED or STALE row per product and business date, written from `v_ace_batch_status` only, and MSG-P1-001 and MSG-P2-007 exist with their texts (DP-05; FSD P1 A2.14).
- RWB-P8-E2008-CON is published with its fake: the rwb-source-data elements the payment-matching step consumes, their answers, the error classes and the WireMock mappings of the run. This story builds against that contract and against its fake, and against no second draft of it (C).
- The ALS batch for the business date is COMPLETE before any row is answered: `v_ace_batch_status` carries one row per source system and business date, and `is_complete` is true only for a COMPLETED batch (TSD P1 T3.4; BR-P1-014-4).
- The reference values this story names in an answer — the data product code `DP01` and the source system `ALS` — are reference data, reached through the reference-data client library of DP-07; the Work Package lists no reference-data contract for this story, so they are a library read with a fixture until that contract is published (GAP-0604; ASM-0846).
- The caller is the payment-matching run of rwb-payment, a service caller with a workload identity token; the data steward reads a refusal with Platform administration R, and the platform administrator reads it with the same right (TSD P1 T6.2; the SY-DATALOAD actor is retired and no source names its replacement for the run of JOB-07 — GAP-0603; ASM-0845).
- No approval is needed to build against a Draft contract baseline; RWB-P8-E2008-CON tags its baseline when its tests pass. This story starts on Day 1 and waits for nothing it builds.
- The ordering of the payment answer, the row cap of one call, the answer for an account key with no view row and the HTTP answer of a held read are not stated by any source and are fixed as below (GAP-0599; ASM-0841; GAP-0601; ASM-0843).

### 4. Flow

1. The payment-matching run of rwb-payment is started by `rwb.source-data.AceDataReady.v1` for the ALS source and business date D (Architecture v5 slide 43 row 26; slide 44 row JOB-07; the run is RWB-P8-E2008-APP's; DP-09, DP-10).
2. `FreshnessHoldGate` reads `data_product_load` for DP01 at D and `v_ace_batch_status` for the ALS row of D before any other read of this story runs; a product that is not LOADED or a batch that is not COMPLETE ends the call at step 8 with no row (AC5, X1, X2; §12.1).
3. The run calls `GET /api/recovery/source-data/v1/payments?businessDate=D` once, one hop and 2 s, and receives `PaymentsAnswer`: the business date, the source system ALS, the batch status, `rowCount`, the DP01 stamp and the payment rows (DP-11; C RWB-P8-E2008-CON).
4. `PaymentFactReadService` reads `v_ace_payment` for the rows whose `payment_date` is D, folds them to one row per `payment_code`, orders them by `paymentCode` and answers the five ACE values of each row unchanged: `paymentCode`, `accountKey`, `paymentDate`, `paymentAmount` and `dataAsOf` (AC1, AC6).
5. A payment whose account is on no open case is answered like every other payment of the date: this read resolves no case, filters nothing out and attaches the row to nothing (AC3; the case lookup and the REC-05 break are RWB-P8-E2008-APP's and RWB-P1-E1011-APP's).
6. For each account the run is about to match, it calls `GET /api/recovery/source-data/v1/accounts/{accountKey}/installment-facts?businessDate=D`; `InstallmentFactReadService` reads `v_ace_account` for that `account_key` and answers `nextInstallmentDate` with `accountKey`, `productKey`, `daysPastDue` and `dataAsOf` (AC2).
7. Neither read answers a plan, an installment amount, a rule, a package version or a case: the plan position of account A-0555 and the installment amount of plan T-0701 are rwb-treatment's, the rule result is rwb-payment's under package `PAYMENT_MATCH`, and the decision record is rwb-decision's (DP-03, DP-04; AC2, AC4).
8. A product not LOADED for D or an ALS batch not COMPLETE for D answers 409 with a problem body that names MSG-P1-001 for the product and the date of the load in use, and carries MSG-P2-007 for the held run and no payment row and no installment fact; the run reports the hold to the data steward (AC5; MSG-P1-001, MSG-P2-007).
9. The run builds its facts, evaluates package `PAYMENT_MATCH`, writes the proceeds row, calls the treatment record, publishes `ProceedsMatched` and `PaymentMissed` and writes the run summary; this story takes no part in any of it and writes no row anywhere (RWB-P8-E2008-APP, RWB-P7-E2008-APP, RWB-S2-E2008-APP).
10. A second call for the same business date answers the same rows from the views again, counts nothing and writes nothing (AC6, BR8; DP-05).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | DP01 is STALE for the business date | 409; no payment row and no installment fact; the problem body names the product and the date of the load in use | MSG-P1-001 | AC5 |
| X2 | The ALS batch for the business date is not COMPLETE, or absent, or FAILED | 409; no row of any kind is read from the views; the hold is named for the run | MSG-P1-001, MSG-P2-007 | AC5 |
| X3 | The business date carries no payment row at all | 200 with `rowCount` 0 and the batch status COMPLETED for that date, so an empty day is distinguishable from a held one | None | AC1 |
| X4 | The same `payment_code` appears twice in a read | One row is answered and the second is folded into it; the answer still holds one row per `payment_code` | None | AC6 |
| X5 | The `account_key` of the installment read has no row in `v_ace_account` | 404 with a problem body naming the account key and the check REC-05; no installment date is invented | None | AC7 |
| X6 | `businessDate` or `accountKey` is missing or malformed | 400 with a problem body naming the field; nothing is read | MSG-GEN-001 | AC8 |
| X7 | A view does not answer inside 5 s, or answers an error | 503 with a problem body naming the ACE database as the unavailable system; nothing is guessed from a cache | MSG-GEN-006 | AC9 |
| X8 | A caller without the right calls either read | 403, and the refusal is logged without a key value | MSG-P4-002 | AC10 |

X1, X2, X3, X4 and X5 are the read-side paths of the legacy exception rows X3 (the batch is not complete) and X5 (a payment on the edge of the window) carried onto the split; the matcher, the exception list, the package refusal and the run summary of the legacy rows X1, X2, X4 and X6 belong to RWB-P8-E2008-APP and RWB-P7-E2008-APP. X6, X7 and X8 are the paths of every read of this service. This story owns no screen; the empty, loading, error and no-access states of SCR-04, SCR-14, SCR-28, SCR-44 and SCR-45 belong to those screens and are not stated here. The states this service answers are X3 (an empty day), X7 (a view error) and X8 (no access).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P8-E2008-CON and its fake, on the published baseline, the view contract of RWB-P1-E1069-APP and the freshness rows of RWB-P1-E1015-APP; needs no live rwb-payment, rwb-treatment, rwb-decision or ACE database to start |
| Negotiable | The entity names, the ordering, the row cap and the held answer are the squad's choice behind the contract; the view set, the field list, the key of a row and the values are fixed |
| Valuable | The matcher matches against one copy of the ACE payment rows of the business date, and a held date is a hold rather than an empty day |
| Estimable | Two read operations, one service, one repository over three views, one freshness gate and one problem body |
| Small | Finished inside one sprint with its tests |
| Testable | Each criterion is one call against the contract fake, the view fixture and the freshness fixture, with no write and no second service |
| Day 1 | The story has no build dependency; it is reachable on the first day of wave 2 and its tests run against the published baseline and the fake |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching with the missed payment event

  Background:
    Given the rwb-payment contract mock returns business date 2026-12-14 with plan "T-0701" due 2026-12-15
    Given case "RC-2026-000555" has account "A-0555" and running restructure plan "T-0701" with installment amount 12,500.00 THB, installments 24 and installments paid 3
    Given account "A-0555" has next installment date 2026-12-15
    Given package "PAYMENT_MATCH" version "PM-2026.12" is in force on 2026-12-14 and is evaluated by rwb-payment, not by this story
    Given the ACE batch for ALS with business date 2026-12-14 is COMPLETE at 05:20
    Given data product "DP01" carries status "LOADED" for 2026-12-14
    Given v_ace_payment holds payment "PAY-90001" of 12,500.00 THB on account "A-0555" dated 2026-12-14
    Given v_ace_payment holds payment "PAY-90002" of 3,000.00 THB on account "A-0555" dated 2026-12-14
    Given v_ace_payment holds payment "PAY-90003" on account "A-0999" that is on no open case

  Scenario: AC1 The payments of 2026-12-14 come back once each with the batch status (new, D-RCV-60)
    When the payment matching run calls GET /api/recovery/source-data/v1/payments?businessDate=2026-12-14
    Then the answer holds 3 rows, one per payment_code, ordered by paymentCode
    Then each row carries its paymentCode, its accountKey, its paymentDate, its paymentAmount and its dataAsOf 2026-12-14
    Then the row of "PAY-90001" carries amount 12,500.00 THB and the row of "PAY-90002" carries amount 3,000.00 THB
    Then the answer carries rowCount 3, the batch status "COMPLETED" of the ALS row for 2026-12-14 and the product status "LOADED" of DP01 for 2026-12-14
    Then every row names source system "ALS" and carries no case, no plan and no rule

  Scenario: AC2 The installment facts of "A-0555" come back for the business date (new, D-RCV-60)
    When the payment matching run calls GET /api/recovery/source-data/v1/accounts/A-0555/installment-facts?businessDate=2026-12-14
    Then the answer carries accountKey "A-0555", nextInstallmentDate 2026-12-15, the productKey, the daysPastDue and the dataAsOf 2026-12-14 of its v_ace_account row
    Then the answer carries the product status "LOADED" of DP01 for 2026-12-14 and the batch status "COMPLETED" of the ALS row
    Then the answer carries no case, no plan "T-0701", no installment amount and no rule
    Then the installment amount 12,500.00 THB of "T-0701" stays on the treatment record of rwb-treatment and this read answers none of it

  Scenario: AC3 A payment on an account with no open case is still a payment fact (new, D-RCV-60)
    Given the rwb-payment contract mock records every call the run makes
    When the payment matching run calls GET /api/recovery/source-data/v1/payments?businessDate=2026-12-14
    Then the answer carries "PAY-90003" on "A-0999" beside every other payment of the date
    Then that row carries no case, no case number and no account status, because this read resolves no case
    Then no break row, no exception list row and no proceeds row is written by this read
    Then the REC-05 break row for "PAY-90003" and the case lookup that holds it are RWB-P1-E1011-APP's and RWB-P8-E2008-APP's

  Scenario: AC4 The two reads answer ACE values only and write nothing (new, D-RCV-60)
    Given the payments of 2026-12-14 and the installment facts of "A-0555" for 2026-12-14 were read
    When both reads are made again and the two answers are inspected
    Then every payment row carries the values of its v_ace_payment row and the source system "ALS"
    Then the second read reads v_ace_payment and v_ace_account again, so this service holds no copy of either
    Then no proceeds row, no PaymentMissed, no ProceedsMatched, no decision log entry and no outbox row is written
    Then neither answer names rule "R-RES-26", package "PAYMENT_MATCH" or package version "PM-2026.12"

  Scenario: AC5 A stale product or an incomplete ACE batch yields no payment row and no installment fact (new, D-RCV-60)
    Given data product "DP01" carries status "STALE" with the load of 2026-12-13 still in use
    And the ACE batch for ALS with business date 2026-12-15 ended "FAILED"
    When the run calls GET /api/recovery/source-data/v1/payments?businessDate=2026-12-14 and GET /api/recovery/source-data/v1/accounts/A-0555/installment-facts?businessDate=2026-12-15
    Then each call answers 409 and no row of any kind
    Then the problem body of the first call names MSG-P1-001 for "DP01 Account and arrears" and the date 2026-12-13
    Then the problem body of the second call names MSG-P1-001 for "DP01 Account and arrears" and the date 2026-12-14
    Then both bodies name MSG-P2-007 for the held run
    Then the refusal of the run itself, with no JOB-07 for 2026-12-15 and no PaymentMissed for due date 2026-12-15, is RWB-P8-E2008-APP's

  Scenario: AC6 A repeated call for the same business date answers the same rows and changes nothing (new, D-RCV-60)
    Given the payments read for 2026-12-14 answered 3 rows and the installment read for "A-0555" answered next installment date 2026-12-15
    When both reads are called again for the same business date
    Then the payments answer holds rowCount 3 with "PAY-90001", "PAY-90002" and "PAY-90003" once each
    Then the installment answer holds nextInstallmentDate 2026-12-15 for "A-0555"
    Then the two repeated calls write 0 rows, publish 0 events and start 0 workflows
    # The run's own repeat, with no second proceeds row and no second event for 2026-12-14, is RWB-P8-E2008-APP's

  Scenario: AC7 An account key with no row in v_ace_account is refused with 404 and no installment date is invented (new, D-RCV-60)
    When the payment matching run calls GET /api/recovery/source-data/v1/accounts/{accountKey}/installment-facts?businessDate=2026-12-14 for an account key with no row in v_ace_account
    Then the answer is 404 with a problem body that names the account key and the check REC-05
    Then the answer carries no nextInstallmentDate and no installment amount

  Scenario: AC8 A missing query value is refused with 400 before any view is read (new, D-RCV-60)
    When the payment matching run calls GET /api/recovery/source-data/v1/payments without businessDate
    Then the answer is 400 with a problem body that names the field businessDate and carries MSG-GEN-001
    Then no view is read
    Then a call of either read with a malformed businessDate, and an installment-facts call with a missing or malformed accountKey, is also answered 400 with MSG-GEN-001 naming the field, and no view is read

  Scenario: AC9 A view that does not answer inside 5 s is refused with 503 and nothing is guessed from a cache (new, D-RCV-60)
    Given v_ace_payment does not answer inside 5 s
    When the payment matching run calls GET /api/recovery/source-data/v1/payments?businessDate=2026-12-14
    Then the answer is 503 with a problem body that names the ACE database as the unavailable system and carries MSG-GEN-006
    Then no cached row is answered
    Then the same 503 answer is given when a view of either read answers an error

  Scenario: AC10 A caller without the right is refused with 403 and the refusal is logged without a key value (new, D-RCV-60)
    Given the caller holds no right on either read
    When the caller calls GET /api/recovery/source-data/v1/payments?businessDate=2026-12-14
    Then the answer is 403 with MSG-P4-002 naming the action
    Then the refusal is logged without a key value
    Then the same caller on GET /api/recovery/source-data/v1/accounts/A-0555/installment-facts?businessDate=2026-12-14 is refused in the same way

  Scenario: AC11 A call without a token is refused with 401 on either read (new, D-RCV-60)
    Given the caller presents no token
    When the caller calls GET /api/recovery/source-data/v1/payments?businessDate=2026-12-14 and GET /api/recovery/source-data/v1/accounts/A-0555/installment-facts?businessDate=2026-12-14
    Then each call answers 401 with a problem body whose message ID is Not specified in the source documents (CG-ALL-2388)
    Then no payment row and no installment fact is answered
```

**Target reading.** Every assertion above is new, because this story owns no legacy criterion; each one tests only the two reads and the gate around them. In section 16 the legacy level System of the kept test cases is shown as End to end and the legacy level Access as Component. What the legacy story asserted of the match, the proceeds row, the treatment record, the exception list, the missed event, the package refusal and the decision log is proved in RWB-P8-E2008-APP, RWB-S2-E2008-APP and RWB-P7-E2008-APP and in RWB-ITG-E2008-ITG, and the legacy values are kept here: case RC-2026-000555, account A-0555, plan T-0701, installment amount 12,500.00 THB, next installment date 2026-12-15, business date 2026-12-14, payments PAY-90001 and PAY-90002, PAY-90003 on A-0999, package PAYMENT_MATCH version PM-2026.12 and rule R-RES-26; the tolerance, the window and the grace days of the package rows are not restated, because this story evaluates no row of them (DP-04, DP-06). AC1 and AC6 fix the two facts the matcher depends on and no source states: one row per `payment_code`, ordered by `paymentCode`, so a repeated call answers the same set, and a row cap per call so one business date cannot answer an unbounded page (GAP-0599; ASM-0841; GAP-0601; ASM-0843). AC1 also names the product the rows were read under: DP01 accounts for `v_ace_payment` in FSD P1 A2.2 and is fed by ALS in TSD P1 T3.7, and the slice note names DP05, which reads no payment, so the gate is held on DP01 and the answer carries the ALS batch row beside it (GAP-0600; ASM-0842). AC2 answers `nextInstallmentDate` here; Architecture v5 slide 15 also names a `GET /accounts/{id}` of this service, which TSD P1 T-A.1 does not carry and no Work Package gives an owner, so that operation is recorded as unowned and unpublished in the API Specification; if it is commissioned, the field moves to it in one contract change, with this operation deprecated in the same change and RWB-P8-E2008-CON aligned (GAP-0602; ASM-0844). AC3 keeps a payment whose account is on no open case in the answer instead of dropping it or inventing a case, so the caller can list it on the break; the break row itself is RWB-P1-E1011-APP's and the exception list is RWB-P8-E2008-APP's. AC4 is the no-copy assertion of BR4 and the no-event assertion of DP-09. AC5 replaces the legacy freshness hold with the two rows it reads — `data_product_load` for DP01 and `v_ace_batch_status` for the ALS batch, both in this service — so the hold needs no call to the freshness story and cannot disagree with it, and it fixes the 409 answer that no source names (DP-05; GAP-0600; ASM-0842). Who answers that hold — this read or the run that is started by `AceDataReady` after the same condition — is not settled by any source, which is why the read-side assertion is here and the run's refusal is named as RWB-P8-E2008-APP's (GAP-0600; ASM-0842).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The payments of one business date are read from `v_ace_payment` over the `payment_code` key, one row per `payment_code`, ordered by `paymentCode`, each with its account key, its payment date, its exact amount and its `data_as_of` | REQ-RDF-002; TSD P1 T3.4; R-UNI-40; legacy BR6 |
| BR2 | The next installment date of an account is read from `v_ace_account.next_installment_date` at the same business date, with the account key, the product key, the days past due and `data_as_of` | Legacy §3 and §11; TSD P1 T3.4 (DF-ACE-028); TSD P1 T3.7 (one business date per read) |
| BR3 | No payment row and no installment fact is answered for a business date whose ALS batch is not COMPLETE, or whose DP01 is STALE; the refusal names the product and the date of the load in use and carries no row | BR-P1-014-4; CTL-02; legacy BR5; FSD P1 A2.14 |
| BR4 | Both answers are derived from the views at request time and never stored; a repeated read reads the views again | D-RCV-35 U1; ADR-010; BR-P1-001-2; legacy BR3 |
| BR5 | This read resolves no case: a payment whose account is on no open case is answered like every other payment, and no exception list row, break row or proceeds row is written here | Legacy AC4 and BR4; REC-05; R-UNI-03 |
| BR6 | The match type, the amount tolerance, the window and the grace days are rows of package `PAYMENT_MATCH` with a version, and this story reads none of them | Principle 1; D-RCV-36 T10; legacy BR7 |
| BR7 | The match is decided by package `PAYMENT_MATCH` through the embedded Drools kit of rwb-payment, and the record of that decision is rwb-decision's; this story evaluates no rule and writes no decision record | D-RCV-36 T5 and T7; ADR-012; DP-04; legacy BR9 |
| BR8 | A repeat of the same read for the same business date answers the same rows, and one row per `payment_code` is what makes the repeat visible rather than a second row | R-UNI-40; legacy BR6 |
| BR9 | Amounts are read as ACE holds them, at scale 2, and are passed on unchanged; this story computes no total, no difference and no tolerance | Legacy §17; TSD P1 T3.4 (numeric(19,2)) |

**Where each rule lives in the target.** BR1 and BR2 are the two reads of steps 3 to 6: the view rows of one business date and the account row of one key, with no join across a schema and no stored copy (DP-01, DP-05). BR3 is `FreshnessHoldGate`, which reads this service's own `data_product_load` row for DP01 and the ALS row of `v_ace_batch_status`, so the gate is local and cannot disagree with the freshness stamp of RWB-P1-E1015-APP. BR4 is the absence of any payment or account table in `rwb_source_data`: a second read reads the view again (AC4). BR5 is why `PAY-90003` on `A-0999` stays in the answer: the case lookup, the exception list and the break row are three other owners, and dropping the row here would hide it from all three (AC3). BR6 is why no tolerance, window or grace value appears in this story: they are columns of the package rows, and the package is evaluated by rwb-payment through the embedded Drools kit (DP-04, DP-06). BR7 is a statement here: this story writes no decision record (DP-03). BR8 is the fold to one row per `payment_code` and the ordering that makes a repeat comparable. BR9 keeps the amount as `BigDecimal` at scale 2 and forbids a conversion to baht units, a rounding or a currency string in code.

### 9. State transitions

None in the case model and none in the plan. This story changes no case status, creates no case, changes no plan state and writes no match state: the legacy plan transitions of `PLAN_RUNNING` to `PLAN_RUNNING` on `PAYMENT_RECEIVED` and to `PLAN_CURE_PERIOD` on `PAYMENT_MISSED` are raised by rwb-payment and applied by P3 and rwb-treatment (legacy §9; R-RES-26, R-RES-27; RWB-P8-E2008-APP, RWB-S2-E2008-APP). The only states this story observes are the freshness status of a data product and the status of the ALS batch row.

| From | Event | Condition | To |
|---|---|---|---|
| DP01 LOADED for the business date and the ALS batch COMPLETED | a payments read or an installment read | The gate passes | The answer carries the rows of the business date and the stamps it read under |
| DP01 STALE, or the ALS batch not COMPLETED, absent or FAILED | either read | The gate refuses | No row is answered; the refusal names MSG-P1-001 for the product and the date of the load in use and MSG-P2-007 for the held run |
| The ALS batch of the business date FAILED | either read | The row is read as it stands | The refusal names the last COMPLETED business date as the date of the load in use; the FAILED row is never answered as a complete one |
| The business date carries no payment row | a payments read | The gate passes | `rowCount` 0 with the batch status COMPLETED, which is an empty day and not a hold |
| An account key with no `v_ace_account` row | an installment read | The key does not resolve | 404 with the key and the check REC-05; no installment date is invented |

The freshness states LOADED and STALE are written by RWB-P1-E1015-APP and read here; this story writes neither, and it never writes `v_ace_batch_status`, which is ACE's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The payment-matching run of rwb-payment, with a workload identity token | Reads the payments of one business date and the installment facts of one account; writes nothing |
| The rwb-source-data service identity (`rwb_source_data` login) | Reads the three ACE views and `data_product_load`; holds no privilege outside its schema and the views |
| RW-DATASTEW, data steward and data product owner | Reads a refused read and its problem body (Platform administration R), and sees the stale product on the data quality route |
| RW-PLATADM, platform administrator | Reads the refused read and its problem body for the business date, and reads the run's hold on the job monitor of rwb-payment |
| The ACE team | Fixes a missing or failed ACE batch row in ACE; reads the stale and late alerts of RWB-P1-E1015-APP |
| RW-COE, center of excellence analyst | Owns package `PAYMENT_MATCH` and its rows through RWB-P7-E2008-APP and the rule package registry; this story reads no row of it |
| RW-CREDITAD, Credit Administration officer | Reads matched and unmatched receipts on SCR-28 of rwb-payment, which this story does not serve |
| RW-CASEOWN, case owner | Reads the plan position on SCR-14 of rwb-treatment, which this story does not serve |
| rwb-source-data (P1) | Owns the two reads, the ordering, the fold and the gate; owns no case, no plan, no proceeds row and no decision record |

No credential appears in an answer, a log line or a test, and the answers carry account keys, payment codes, dates, amounts and status codes only. Data Classification v5 classes several of these fields as personal data; they are handled by the rule in section 17, and no clear key or customer value is written to a log line. Roles and their rights are held as data in rwb-access and reached through its authorise contract, never by a table read (DP-01; TSD P1 T6.2).

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-043 | v_ace_payment | payment_code | Read |
| DF-ACE-044 | v_ace_payment | account_key | Read |
| DF-ACE-045 | v_ace_payment | payment_date | Read |
| DF-ACE-046 | v_ace_payment | payment_amount | Read |
| DF-ACE-054 | v_ace_payment | data_as_of | Read |
| DF-ACE-001 | v_ace_account | account_key | Read (the key of the installment read) |
| DF-ACE-008 | v_ace_account | product_key | Read |
| DF-ACE-018 | v_ace_account | days_past_due | Read |
| DF-ACE-028 | v_ace_account | next_installment_date | Read |
| DF-ACE-036 | v_ace_account | data_as_of | Read |
| DF-ACE-178 | v_ace_batch_status | source_system | Read (the gate and the batch status) |
| DF-ACE-179 | v_ace_batch_status | business_date | Read (the gate and the batch status) |
| DF-ACE-182 | v_ace_batch_status | status | Read (the gate and the batch status) |
| DF-ACE-186 | v_ace_batch_status | is_complete | Read (the gate) |
| DF-OPS-002 | data_product_load | product_code | Read (the gate) |
| DF-OPS-004 | data_product_load | business_date | Read (the gate) |
| DF-OPS-006 | data_product_load | loaded_at | Read (the stamp the answer carries) |
| DF-OPS-007 | data_product_load | status | Read (the gate and the stamp) |

Field IDs are those in the Logical Data Model and Data Dictionary. Every `DF-ACE-` row is read in this service's own `recovery.v_ace_*` views and never from a `public` table, and never copied into a table of this service (DP-01, DP-05; BR-P1-001-2). `data_product_load` is this service's table, written by RWB-P1-E1015-APP and read here for the gate and for the stamp only. No field of `proceeds`, `treatment`, `recovery_case`, `case_account` or `decision_log_entry` is read or written: those rows belong to P8, S2, P3 and P7 and are reached through their contracts by the run, not by this story. No field of this story is personal data: a payment code, an account key, a product key, three dates, one amount and four status values carry no person.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-source-data (P1); base `/api/recovery/source-data/v1` (DP-13). Two read operations of the payment-matching step; the C dependency RWB-P8-E2008-CON declares the shapes the run consumes and this story implements them.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/payments` | The payments of one business date, read from `v_ace_payment`, one row per `payment_code`, ordered by `paymentCode`, with `rowCount`, the ALS batch status and the DP01 stamp the rows were read under | The payment-matching run of rwb-payment (workload identity); Platform administration R for a refusal | Idempotent: the answer is derived from the views on every call and holds no stored state |
| GET | `/accounts/{accountKey}/installment-facts` | The next installment date of one account at one business date, read from `v_ace_account`, with the account key, the product key, the days past due and `data_as_of` | The payment-matching run of rwb-payment (workload identity); Platform administration R for a refusal | Idempotent: the answer is derived from the view on every call |

The payments answer is `PaymentsAnswer`: `businessDate`, `sourceSystem` (always `ALS`), `rowCount`, `batchStatus` of `BatchStatusStamp` with `sourceSystem`, `businessDate`, `status`, `isComplete` and `completedAt`, `productStatus` of `ProductStamp` with `productCode` (`DP01`), `businessDate`, `status` and `loadedAt`, and `rows` of `PaymentFact` with `paymentCode`, `accountKey`, `paymentDate`, `paymentAmount` and `dataAsOf`. The installment answer is `InstallmentFacts`: `accountKey`, `businessDate`, `nextInstallmentDate`, `productKey`, `daysPastDue`, `dataAsOf`, `batchStatus` and `productStatus`. Property names are a target choice and follow the naming of the P1 API appendix; the field list is fixed by section 11.

Errors are the RFC 9457 problem body: 400 for a missing or malformed `businessDate` or `accountKey` with MSG-GEN-001 naming the field, 401 without a token with MSG-P4-001, 403 without the right with MSG-P4-002, 404 for an `accountKey` with no row in `v_ace_account` naming the key and the check REC-05, 409 when the gate refuses with MSG-P1-001 naming the product and the date of the load in use and MSG-P2-007 for the held run, and 503 when a view does not answer inside 5 s or answers an error, with MSG-GEN-006 naming the ACE database.

Four things about the shape are stated by no source and are fixed here. (1) The resource names, the two query parameters and the element names of the two answers: the legacy read was an in-process Java interface with a business date argument and no path, and no source document carries a payments or installment-facts path (GAP-0599; ASM-0841). (2) The ordering and the fold: one row per `payment_code` ordered by `paymentCode`, which makes a repeat answer comparable and a duplicate visible. (3) The row cap of one call: both reads answer one business date or one account in one call and are unpaged, with the cap as configuration, because no source states the volume of payments per business date (GAP-0601; ASM-0843). (4) The answers of a held read (409 with no row) and of an account key with no view row (404 with the key and REC-05), so a hold, an empty day and an unresolvable key are three distinguishable answers. These four are recorded for the contract owner and belong in the next version of the API specification.

#### 12.2 REST operations consumed

None. This story calls no operation of another service at run time. The gate reads this service's own `data_product_load` rows and `v_ace_batch_status` instead of calling the freshness story; the reference values it names in an answer are reached through the reference-data client library of DP-07 and not through a run-time call; and the case, the plan, the rule and the decision record are the run's calls and not this story's. The reference-data contract that supplies those values is not in this Work Package's contract list, so the values are a library read with a fixture until that contract is published (GAP-0604; ASM-0846; DP-07). The bindings of C from the legacy dependency are the run's contract RWB-P8-E2008-CON, which declares what this service answers and is faked for this story's tests.

#### 12.3 Events published

None of its own. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and its two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1015-APP (Architecture v5 slides 15 and 43). This story publishes no event, writes no outbox row and adds no message schema; `PaymentMissed` and `ProceedsMatched` are rwb-payment's two events on its own topic, raised by RWB-P8-E2008-APP after the match (Architecture v5 slides 17, 42 and 43).

#### 12.4 Events consumed

None. The payment-matching run consumes `rwb.source-data.AceDataReady.v1` and holds it (Architecture v5 slide 43 row 26; rwb-payment is one of its four consumers); this story is reached over REST by that run after the event and subscribes to nothing. Consuming `AceDataReady` here would create a second reader of the event and a second start path for the same business date, and the run's contract fixes the single consumer (DP-09).

#### 12.5 Workflows and activities

None. Both reads are synchronous REST steps that answer in one call with a 2 s budget, and this story starts no workflow and no activity. JOB-07 is P8's event-triggered Temporal workflow on queue `rwb-payment` of the owning service (Architecture v5 slide 44 row JOB-07; slide 17, rwb-payment "Act: matchPayments"); the task queue of this service is `rwb-source-data` in namespace `rwb-recovery` and it belongs to the other P1 stories (DP-10).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story: both reads are called by the run when `AceDataReady` arrives and at no fixed time (DP-10; Architecture v5 slide 44).

#### 12.7 Tables owned

None. This story creates no table and no column, adds no migration to the per-service sequence and writes no row.

| Object | Schema | Owner | This story |
|---|---|---|---|
| `v_ace_payment`, `v_ace_account`, `v_ace_batch_status` | `recovery` | ACE, read through the view contract of RWB-P1-E1069-APP | SELECT only, read-only login, never copied (DP-05; ADR-010). Views are not tables and this story creates none |
| `data_product_load` | `rwb_source_data` | P1, written by RWB-P1-E1015-APP | Read for the gate and for the stamp; no row is written here |
| `processed_event`, `idempotency_key`, `outbox_event` | `rwb_source_data` | PLT library objects, created in this service's schema | Not used: this story publishes no event and stores no response (DP-09) |

No table of another service is read and no foreign key crosses a schema (DP-01). `proceeds` stays in `rwb_payment` and `treatment` in `rwb_treatment`, and `recovery_case`, `case_account` and `decision_log_entry` stay with their owners; none of them is named in this story's code or tests except as the objects it must not touch.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P8-E2008-CON fake | The P8 client stub of both reads, and the WireMock mappings of the payment-matching step | The payments of 2026-12-14 with PAY-90001, PAY-90002 and PAY-90003 and one repeated `payment_code`; the installment facts of A-0555 with next installment date 2026-12-15; a 409 hold with MSG-P1-001 and MSG-P2-007 for a stale DP01 and for an incomplete ALS batch; a 404 for an account key with no row; a 503 from a view |
| ACE view fixture | `recovery.v_ace_payment`, `v_ace_account` and `v_ace_batch_status` | PAY-90001 12,500.00 THB and PAY-90002 3,000.00 THB on A-0555 dated 2026-12-14; PAY-90003 on A-0999; the account row of A-0555 with next installment date 2026-12-15, `data_as_of` 2026-12-14 and 96 days past due; the ALS batch rows of 2026-12-14 COMPLETE and of 2026-12-15 FAILED, and an absent row for 2026-12-16 |
| Freshness fixture | `data_product_load` | DP01 LOADED for 2026-12-14; DP01 STALE with the load of 2026-12-13 in use; DP01 LOADED but the ALS batch absent |
| Product code fixture | The reference-data client library | DP01 and DP13 with their names for the fixture, the source system ALS, and one code with no list row (GAP-0604; ASM-0846) |

All four fakes are local: no live rwb-payment, rwb-treatment, rwb-decision or ACE database is needed to run the tests of section 16.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 read operations on `/api/recovery/source-data/v1` | None | OpenAPI 3.1; one hop, 2 s budget, breaker per client (DP-11); shapes declared by RWB-P8-E2008-CON |
| Kafka | None | None | The topic and both events belong to RWB-P1-E1015-APP; the run consumes them and raises its own two events |
| Temporal | None | None | No workflow, activity or Schedule in this story; JOB-07 is P8's workflow on queue `rwb-payment` (DP-10) |
| File | None | None | No file is read or written |
| SQL view | None | 3 views of `recovery`, SELECT only | In-process, read-only login, 5 s statement timeout, never copied (DP-05; ADR-010) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.sourcedata`, module `payments`, with the published types in `...sourcedata.api`. Service base `/api/recovery/source-data/v1`, schema `rwb_source_data`, topic `rwb.source-data.events.v1` (not published here), task queue `rwb-source-data` in namespace `rwb-recovery` (not used here). The build starts on Day 1 against three published artefacts and no build dependency: the service baseline, the view contract of RWB-P1-E1069-APP and the fake of RWB-P8-E2008-CON.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; no contract dependency of this story, because rwb-payment evaluates the package |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**One sentence per pattern.** DP-01 is the shape of this story: the payment rows and the account row are read from the views and answered over the contract, and no column of ACE is copied into `rwb_source_data`. DP-03 is a statement here: the decision record of a match names rule `R-RES-26` and the package version, and it is written by rwb-payment in its own schema through the local decision-record library and collected into the central ledger of rwb-decision; this story writes no entry and reads none (RWB-P7-E2008-APP). DP-04 is a statement here: package `PAYMENT_MATCH` version `PM-2026.12` is evaluated by rwb-payment through its own embedded Drools kit under its platform contract, this story reads no row of the package and no `drl_source`, and the tolerance, the window and the grace days are columns of those rows and never values of this service. DP-05 is the read path itself: `v_ace_payment` for the payments of one business date, `v_ace_account` for the next installment date of one account and `v_ace_batch_status` for the batch row, SELECT only through the `rwb_source_data` login (ADR-010). DP-06 is a statement: this story reads no parameter, and the window and the grace days of the match are package rows of rwb-payment and not parameters of the read. DP-07 is the data product code and the source system label the answers name, read as reference data through the client library and never as a constant in code; the Work Package lists no reference-data contract for this story, so the values come from the library with a fixture until that contract is published (GAP-0604; ASM-0846). DP-09 is a statement: both reads publish no event and write no outbox row, and no inbox row is written here because the run consumes `AceDataReady` and not this story. DP-10 is a statement: JOB-07 is P8's event-triggered workflow on queue `rwb-payment`, and this story starts no workflow, no activity and no Schedule (Architecture v5 slide 44). DP-11 is the hop: the run calls the two reads over REST, one hop with a 2 s budget and a breaker, against the shapes of RWB-P8-E2008-CON and its fake; the P8 to P1 step is one REST hop wrapped by the run's Temporal activity, so this service carries no Temporal dependency for the two reads, and the activity description is corrected in the next version of the Temporal Workflow and Activity Catalog (GAP-0603; ASM-0845). DP-13 is the base: `/api/recovery/source-data/v1` instead of the monolith's `/api/recovery/v1`. DP-15 is not claimed: this story stores nothing, so it adds no version to the per-service sequence and reads the baseline objects the sequence already created. DP-19 is a statement: this story renders no screen; the Credit Administration officer reads SCR-28 of rwb-payment, the case owner reads SCR-14 of rwb-treatment and the data steward reads the stale product on the data quality route of gateway-bff.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PaymentFactController` | Controller | The two operations of 12.1 on `/api/recovery/source-data/v1`; RFC 9457 problem details; the 409 hold, the 404 key and the 400 field |
| `PaymentFactReadService` | Service | The `v_ace_payment` read of one business date, the fold to one row per `payment_code`, the ordering and the `rowCount` |
| `InstallmentFactReadService` | Service | The `v_ace_account` read of one account key at one business date and the five facts it answers |
| `PaymentViewRepository`, `AccountViewRepository` | Repository | SELECT over `recovery.v_ace_payment` and `recovery.v_ace_account`; no write method exists |
| `BatchStatusReader` | Repository | SELECT over `recovery.v_ace_batch_status` for the ALS row of the business date, and the last COMPLETED date for the refusal |
| `ProductStampReader` | Repository | Reads this service's own `data_product_load` row for DP01 at the business date (DP-05) |
| `FreshnessHoldGate` | Gate | Decides pass or hold from the DP01 stamp and the ALS batch row before any other read runs, and builds the refusal body |
| `ProductCodeReferenceClient` | Client library use | The data product code and the source system label as reference data; no code in code (DP-07) |
| `PaymentsAnswer`, `PaymentFact`, `InstallmentFacts`, `BatchStatusStamp`, `ProductStamp` | Published types | The records of 12.1 in `...sourcedata.api`; no case field, no plan field and no copy of an ACE column |

**Migration (DP-15).** None. This story adds no table, no column, no index and no version to the per-service Flyway sequence, because it stores nothing. The baseline objects it reads are created by RWB-P1-E1001-APP, the views it reads are created by RWB-P1-E1069-APP and its database story under the migrations of TSD P1 T3.2, and an applied version is never edited by anyone, including this story.

**Database.** No object of `rwb_source_data` is created or written. `v_ace_payment` and `v_ace_account` are Section A views and `v_ace_batch_status` a Section B view, all ACE's, read through this service's login with SELECT only (TSD P1 T3.3; T6.3); `data_product_load` is read for the gate and the stamp and written by RWB-P1-E1015-APP. This story has no table of its own: a second read of the same business date reads the views again (BR4).

**Configuration and reference data**

- The data product code `DP01` and the source system label `ALS` are reference values read through the client library, with a fixture until the reference-data contract is published (GAP-0604; ASM-0846; DP-07).
- The row cap per call, the 2 s client budget and the 5 s statement timeout are configuration of the reads and of the view session (Architecture v5 slide 11; TSD P1 T6.3).
- The ordering `paymentCode` ascending, the fold to one row per `payment_code` and the answers of a held read and of an unresolvable key are configuration of the contract and not values a business person changes (GAP-0599; ASM-0841).
- The gate reads the product stamp and the batch row and holds nothing in a cache: a held business date is refused on every call until the batch of that date completes (BR3).
- The flag `rwb.source-data.payment-facts` gates both reads at deployment; with it off the run receives 503 and starts no matching for the business date.

**Build steps**

1. The five published types and the OpenAPI fragment of 12.1, taken from RWB-P8-E2008-CON and published with the service baseline (C).
2. `ProductStampReader` and `BatchStatusReader` over `data_product_load` and `v_ace_batch_status`, and `FreshnessHoldGate` with the 409 problem body of MSG-P1-001 and MSG-P2-007 and the last COMPLETED date in the refusal (AC5, X1, X2).
3. `PaymentViewRepository` and `PaymentFactReadService`: the `v_ace_payment` read of one business date, the fold to one row per `payment_code`, the ordering by `paymentCode` and the `rowCount` (AC1, AC6, X3, X4).
4. `InstallmentFactReadService` and `AccountViewRepository`: `nextInstallmentDate` with the four account facts, and the 404 with the key and REC-05 for an account key with no row (AC2, X5).
5. The error paths: 400 with MSG-GEN-001 naming the field, 403 with MSG-P4-002, 503 with MSG-GEN-006 for a view that does not answer inside 5 s, and the `ProductCodeReferenceClient` fixture for the product code and the source system (X6, X7, X8).
6. An architecture test that no class of the `payments` module writes a row, names `proceeds`, `treatment`, `recovery_case`, `case_account` or `decision_log_entry`, or references a case, plan, rule or event type (AC3, AC4, DP-01, DP-03).
7. A test that a second read of the same business date reads the views again and answers the same rows, so the no-copy rule is asserted and not assumed (AC4, AC6).
8. Tests for AC1 to AC6 against the four fakes of 12.8, plus the regression rows of section 16 where the fixture of the owning slice is available.

**Done when.** The tests in section 16 pass, the payments of 2026-12-14 answer three ordered rows with one row per `payment_code` and the exact amounts, the installment facts of A-0555 answer the next installment date 2026-12-15, both reads refuse with 409 and MSG-P1-001 while DP01 is STALE or the ALS batch is not COMPLETE and carry MSG-P2-007, a payment whose account is on no open case stays in the answer, and no row is written anywhere.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | DP01 is stale, or the ALS batch of the business date is not COMPLETE | {product} is from {date}. Today's load has not arrived. |
| MSG-P2-007 | The matching run is held for an incomplete ACE batch | Case creation for {date} is held until a load passes its checks. {count} accounts are waiting. |
| MSG-GEN-001 | A required query value is missing or malformed | Enter {field}. |
| MSG-P4-001 | No token | Your session has ended. Sign in again. |
| MSG-P4-002 | A role without the right on the read | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | A view does not answer inside 5 s, or answers an error | {system} is not available. Your request is queued and will be retried. |

The texts are the legacy texts of RWB-E2-008 §14 and of the P1 module carried unchanged, with MSG-P1-001 and MSG-P2-007 in the wording of the Error and Message Standard v4 (FSD P1 A2.1 VR-P1-001-1; OQ-P1-07). MSG-P1-001 and MSG-P2-007 are published by the freshness story and raised here in the refusal body with the date of the load in use and the product name the answer carries, "DP01 Account and arrears" in the legacy fixture; the Standard's text of MSG-P2-007 names case creation and accounts, and a wording of it for a payment-matching run is Not specified in the source documents (DOR-RWB-P1-E2008-APP-9) (GAP-0599; ASM-0841). MSG-GEN-006 names the ACE database as the failed system, and MSG-P4-002 names the action the caller tried and never a key value. Thai text for each message follows decision DL10, whose assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive; the decision itself stays open and is not this story's to close. No message carries a person name, an identity number, a phone number, an address or a payment amount.

### 15. Screens and states

No screen in this story. The Credit Administration officer reads matched and unmatched receipts on SCR-28 Proceeds matching of rwb-payment, and the case owner reads the plan position and the missed payment on SCR-14 Treatment record and SCR-04 Case timeline of rwb-treatment and rwb-case; the data steward sees the stale product on SCR-45 Data quality through the reconciliation and freshness route of gateway-bff, and the platform administrator sees the JOB-07 run summary on SCR-44 Interface and job monitor (DP-19; RWB-PLT-N001-CON). This story renders none of them: it answers a 409 with MSG-P1-001 in the refusal state of whoever asked, and it fixes no field, state or mask of any screen.

Screen states from Screen Specifications v1: SCR-04, SCR-28 and SCR-45 have loading; their empty, error and no access states are Not specified in the source documents (CG-ALL-2393) for SCR-04, Not specified in the source documents (CG-ALL-2395) for SCR-28 and Not specified in the source documents (CG-ALL-2397) for SCR-45. The empty, loading, error and no access states are Not specified in the source documents (CG-ALL-2394) for SCR-14 and Not specified in the source documents (CG-ALL-2396) for SCR-44.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-008-01 | AC1, BR1, BR9 — this story's own evidence on the read side: the rule result and the proceeds row of the same row set are RWB-P8-E2008-APP's and RWB-P7-E2008-APP's | End to end | PAY-90001 12,500.00 on A-0555 dated 2026-12-14 in v_ace_payment; T-0701 due 2026-12-15 |
| TC-E2-008-02 | AC2, BR2 — regression evidence: the missed event is RWB-P8-E2008-APP's and the plan state is P3's and RWB-S2-E2008-APP's | End to end | No payment 2026-12-05 to 2026-12-15 |
| TC-E2-008-03 | AC3, BR3 — this story's own evidence on the read side: the exception list is RWB-P8-E2008-APP's | End to end | PAY-90002 3,000.00 |
| TC-E2-008-04 | AC4, BR4 — this story's own evidence on the read side: the case lookup and the REC-05 break row are RWB-P8-E2008-APP's and RWB-P1-E1011-APP's | End to end | PAY-90003 on A-0999 with no open case |
| TC-E2-008-05 | AC5, BR5 — this story's own evidence on the read side: the run's refusal for the business date is RWB-P8-E2008-APP's | End to end | ACE batch for ALS of 2026-12-15 failed |
| TC-E2-008-06 | AC6, BR6 — regression evidence: the rerun of JOB-07 is RWB-P8-E2008-APP's, and the repeat of a read is AC6 here | End to end | JOB-07 rerun for 2026-12-14 |
| TC-E2-008-07 | BR1, BR7 — run by RWB-P8-E2008-APP and RWB-P7-E2008-APP; regression evidence: the window boundary | End to end | PAY-90004 10 days and PAY-90005 11 days before their due dates |
| TC-E2-008-08 | BR10 — run by RWB-P7-E2008-APP and RWB-P8-E2008-APP; regression evidence: the no-package refusal | End to end | No PAYMENT_MATCH version in force on 2026-12-15 |
| TC-E2-008-09 | BR9 — run by RWB-P7-E2008-APP; regression evidence: the decision log entry | End to end | PAY-90001 matched under version PM-2026.12 |
| TC-E2-008-10 | Access — regression evidence: `GET /proceeds` is RWB-P8-E2008-APP's operation, and the access test of these two reads is X8 | Component | RW-CASEOWN calls GET /proceeds; refused with MSG-P4-002 |
| TC-E2-008-11 | AC1, AC2, BR1, BR2 — contract evidence: the two GET operations of §12 answer the payments answer and the installment answer, and publish no event | Component | Payments of businessDate 2026-12-14; installment facts of A-0555 for 2026-12-14 |
| TC-E2-008-12 | AC4, BR4 — boundary evidence: the two reads touch v_ace_payment, v_ace_account and v_ace_batch_status only, and write no table listed in §12.7 | Component | Read-only login; two calls for 2026-12-14 |
| TC-E2-008-13 | AC7, X5 — account key with no row in v_ace_account | Component | Account key absent from v_ace_account for 2026-12-14 |
| TC-E2-008-14 | AC8, X6 — businessDate or accountKey missing or malformed | Component | GET payments without businessDate; either read with a malformed businessDate; installment-facts with a missing or malformed accountKey |
| TC-E2-008-15 | AC9, X7 — a view does not answer inside 5 s, or answers an error | Component | View delayed beyond 5 s; view answering an error |
| TC-E2-008-16 | AC10, X8 — caller without the right on either read | Component | Caller with no right on the payments read and on the installment-facts read of A-0555; refused with MSG-P4-002 |
| TC-E2-008-17 | AC6, BR8 — this story's own evidence on the read side: a repeat of both reads for 2026-12-14 answers the same rows | Component | Both reads repeated for 2026-12-14 and A-0555 |
| TC-E2-008-18 | AC11 — a call without a token on either read is refused with 401 | Component | No token; payments of 2026-12-14 and installment facts of A-0555; refused with the message ID held open under CG-ALL-2388 |

The ten legacy test case IDs and their Data are kept in order and character for character, and the Covers of TC-E2-008-07, TC-E2-008-08 and TC-E2-008-09 drop the AC reference this story does not own; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. TC-E2-008-01, TC-E2-008-03, TC-E2-008-04 and TC-E2-008-05 are the rows this story runs as its own evidence, on the read side of each criterion. The other six rows are kept as regression evidence for the slices of this legacy key that own those criteria and for RWB-ITG-E2008-ITG, and they run again there against the live contracts. For the legacy test case IDs, the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the tolerance, the window, the grace days and the match types are rows of package `PAYMENT_MATCH` with a version, the product code and the source system are reference data, and the row cap and the budgets are configuration; no product code, source system, batch status or date is written in code.
- Personal data handling (Data Classification v5, Fields): `account_key` (DF-ACE-001, DF-ACE-044; Indirect identifier, Confidential) and `days_past_due`, `next_installment_date`, `data_as_of`, `payment_code`, `payment_date` and `payment_amount` (DF-ACE-018, 028, 036, 043, 045, 046; Customer data, Confidential) are personal data. They are answered only within the caller's right and are masked in UAT; a log line carries the id of the read, a code or an id only, never the clear account key or a customer value; this story publishes no event. A person name, an identity number, a phone number, an e-mail and an address are never read, never logged and never echoed in a problem body, and the test data is synthetic.
- ACE data only through this service's own `recovery.v_ace_*` views and the owner's contract, and only rwb-source-data reads the views (DP-05; ADR-010); no direct `public` read exists in code, in a test or in a query (BR-P1-001-2).
- No read of another service's tables and no write to one: `proceeds`, `treatment`, `recovery_case`, `case_account` and `decision_log_entry` are never named in code or tests except as the objects this story must not touch (DP-01, DP-03, DP-04).
- No copy of ACE data and no stored response: both answers are derived from the views at request time and a repeated read reads the views again (BR4; BR8).
- The read is one hop with a 2 s budget and a breaker, against the published contract and its fake, and a slow view answers 503 instead of a partial answer (DP-11).
- A held business date is answered, not guessed: no row is served from a cache, a previous business date or a partial batch, and an empty day is answered as `rowCount` 0 with a COMPLETE batch rather than as a hold (BR3; X3).
- Amounts are read at scale 2 as ACE holds them and passed on unchanged: no total, no rounding and no currency conversion in this service (BR9).
- An applied migration is never edited, and this story adds none (DP-15 is not claimed).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-11 | 7.3 Negotiate settlement or deed in lieu | R-RES-27 | TC-E2-008-02, TC-E2-008-05, TC-E2-008-06 |
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01, FEAT-PAY-02 | 7.3 Negotiate settlement or deed in lieu | R-RES-26, R-UNI-03, R-UNI-40 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-04, TC-E2-008-07, TC-E2-008-08, TC-E2-008-09, TC-E2-008-10 |
| REQ-RDF-002 | Payments for every account at 90 or more days past due are read from ACE through `v_ace_payment`, current to the previous working day | Program 5.1; Epic 2 3.8 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | REC-05; BR-P1-014-4 | TC-E2-008-01, TC-E2-008-03, TC-E2-008-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P8-E2008-CON | Contract | C: declares the rwb-source-data elements the payment-matching step consumes, their answers and the fakes; this story implements them |
| RWB-P8-E2008-APP | App development | The matcher: JOB-07, the rule evaluation, the proceeds row, the exception list and both events |
| RWB-S2-E2008-APP | App development | The plan and its installment amount, and the plan state a missed payment sets |
| RWB-P7-E2008-APP | App development | Package `PAYMENT_MATCH`, its rows, and the decision record that names `R-RES-26` and the package version |
| RWB-P1-E1011-APP | App development | Sibling in this service: the REC-05 result row and the break list a payment on an account with no open case reaches |
| RWB-P1-E1015-APP | App development | Sibling in this service: `data_product_load`, the LOADED and STALE states the gate reads, and `AceDataReady` and `AceDataLate` |
| RWB-P1-E1069-APP | App development | Sibling in this service: the three views and the `rwb_source_data` grant this story reads through |
| RWB-ITG-E2008-ITG | Integration | Proves the whole legacy key against the live rwb-payment, rwb-treatment, rwb-decision, rwb-case and this service |

### 19. Out of scope

- The matcher and JOB-07: the fact building, the call to package `PAYMENT_MATCH`, the EXACT, PARTIAL and WINDOW rows, the exceptionally long window, the grace days, the partial floor and the match result (RWB-P8-E2008-APP; DP-04).
- The proceeds row, its unique key on `payment_code`, the matched-to state and the exception list of an unmatched receipt (RWB-P8-E2008-APP); `proceeds` is P8's table and this story writes no row of it.
- `PaymentMissed` and `ProceedsMatched`, their idempotency keys and the run summary (RWB-P8-E2008-APP); this story publishes no event (DP-09).
- The plan and its installment amount, the installment paid record and the plan state transitions of `PLAN_RUNNING` to `PLAN_CURE_PERIOD` (RWB-S2-E2008-APP; R-RES-26, R-RES-27), and the case state and the transfer rule P3 applies.
- Package `PAYMENT_MATCH`, its version `PM-2026.12`, its approval, its rollback and the decision log entry that names rule `R-RES-26` (RWB-P7-E2008-APP; DP-03, DP-04).
- The case lookup of a payment, the exception list seen by the Credit Administration officer, the REC-05 break row and the break list of the business date (RWB-P8-E2008-APP, RWB-P1-E1011-APP).
- The freshness stamp, the stale flag, `AceDataReady` and `AceDataLate` (RWB-P1-E1015-APP); this story reads the stamp and publishes nothing.
- The three views, the grants and the boundary rule (RWB-P1-E1069-APP and its database story); this story reads the views and creates none.
- The `GET /accounts/{id}` operation that Architecture v5 slide 15 names: if it is published, `nextInstallmentDate` may move to it from this story's installment read (GAP-0602; ASM-0844).
- The screens SCR-28, SCR-44, SCR-45, SCR-14 and SCR-04 and the gateway-bff composite routes (DP-19; RWB-PLT-N001-CON and the screen owners).
- The real cross-service proof against the live run, rwb-treatment, rwb-decision and rwb-case (RWB-ITG-E2008-ITG).

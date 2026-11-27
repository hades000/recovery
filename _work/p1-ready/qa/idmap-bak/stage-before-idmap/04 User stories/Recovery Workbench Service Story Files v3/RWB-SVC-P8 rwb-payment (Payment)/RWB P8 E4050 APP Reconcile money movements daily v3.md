# RWB-P8-E4050-APP Reconcile money movements daily

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-061, RD-P1-066, RD-P1-069: Store REC-04 and REC-06 in rwb-payment and consume P1 batch checksum and REC-05 aggregates.
- RD-P1-061, RD-P1-066, RD-P1-069: Consume AceDataReady through the shared source-data listener and start `proceedsReconciliation` by signal-with-start.
- `AceDataReady` (EV-26): record key `{sourceSystem}:{businessDate}` and the four-field payload (RD-P1-003).
- Start rule: the daily reconciliation starts only on the event with `sourceSystem` `ALS` and `status` `COMPLETED` (RD-P1-003, RD-P1-040).
- Freshness read: status `LOADED` or `STALE`, `businessDate` null with `STALE` when never stamped, stamp in use is the latest row; contract rwb-source-data.yaml 5.1.0 (RD-P1-005, RD-P1-041).


| Item | Value |
|---|---|
| Story key | RWB-P8-E4050-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-050 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P8-M |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P8-E4050-APP-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-P8-E4050-APP-23); the consumed freshness read is built against rwb-source-data.yaml 5.1.0 (API Specification v7) |
| Readiness decisions | RD-P1-003, RD-P1-005, RD-P1-040, RD-P1-041, RD-P1-061, RD-P1-066, RD-P1-069 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 (realignment v1), 22 November 2026: new service story, split from RWB-E4-050 for `rwb-payment`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E4050-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As the **Credit Administration officer**, I want **the Workbench to reconcile the payments and the write-offs ACE holds against the cases every day**, so that **every payment and booking is matched to its case**. In the target, as the reconcilable side of `rwb-payment`, for one business date the service compares the receipts it matched with the payments ACE holds in that view, records the outcome with the rule ID and version in force, and lists every key that does not resolve, so the officer sees matched or unmatched on SCR-28 and the owner of the reconciliation reads the same numbers.

This is the application slice of legacy RWB-E4-050 (FEAT-PAY-11 Reconcile money movements daily, module P8 Payments and posting, priority Must, depends on FEAT-RDF-11). It owns:

- the legacy acceptance criterion AC2 of the key, copied word for word with its origin tag; AC1 of the key is owned by RWB-ITG-E4050-ITG and is not restated here (section 7);
- the daily money reconciliation step of this service (`proceedsReconciliation`), an event-started workflow on task queue `rwb-payment` in namespace `rwb-recovery`, started from the batch completion record of source `ALS` with status `COMPLETED` for a business date: it reads the payments ACE holds for that date on rwb-source-data's contract, reads the `proceeds` rows of the same date range in `rwb_payment`, and computes for each `rec_code` the source count, the Workbench count and the difference (DP-05; FSD P8 A2.11; legacy AC1's four moves for the payment side);
- the unmatched-proceeds list on `GET /proceeds?matched=false` and the P1 REC-05 aggregate counts (RD-P1-069).
- the local decision record of every daily reconciliation, written through RWB-PLT-E1027-CON in the same transaction as the outcome, naming REC-04 and REC-06 with the rule ID and version in force, and MSG-P7-003 when it cannot be written (DP-03; R-UNI-39; legacy AC2);
- the P1 REC-05 aggregate for the same date, shown beside the local REC-04 and REC-06 results.
- SCR-28 Proceeds matching with its three states, reached through the gateway-bff composite route (DP-19; FSD P8 Screens).

P1 owns JOB-04 and REC-01, REC-02 and REC-05. rwb-writeoff owns the approved write-offs. The other stories retain matching, case state, rule registry, access, integration checks and deployment.

### 2. Business rationale

A daily reconciliation that a person cannot reproduce is a number nobody can defend, and a payment ACE holds that never reached a case is money the bank cannot account for. The legacy key states the work in four moves: REC-04 matches the payments in `v_ace_payment` to the proceeds matched to the case, REC-06 matches the posting in `v_ace_write_off` to the approved write-off, REC-05 lists every `account_key` and `payment_code` that does not resolve in the view, and the outcome is written by `rec_code` and business date (legacy RWB-E4-050 AC1; D-RCV-35 U4). The business objective is unchanged: reconcile the payments ACE holds against the cases every day and write the result to the decision log with the rule version (FSD P8 A2.11.1; FEAT-PAY-11).

rwb-payment computes REC-04 and REC-06 in its daily reconciliation and persists the outcomes in `rwb_payment` (RD-P1-069). P1 runs REC-01, REC-02 and REC-05 under JOB-04.

The local decision record carries the rule IDs, versions and counts for REC-04 and REC-06. Both results and the date guard commit with the record. A record failure leaves no result and raises MSG-P7-003 (AC2, DP-03).

Pending: the rule package and tolerance, owner rwb-payment owner with rwb-decision (GAP-2561, ASM-4224).

### 3. Preconditions

- RWB-P8-E4043-CON is published: base `/api/recovery/payment/v1`, `GET /proceeds` with `ProceedsPage`, `POST /proceeds/{proceedsId}/match` with `MatchRequest` and `Proceeds`, the `proceeds` baseline with DF-FIN-001 to DF-FIN-009, the `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` schemas, the error set and the fakes. This story builds behind that contract and adds no shape of its own.
- RWB-PLT-E1027-CON is published: the decision-record writer declared to run in the caller's transaction, failing with MSG-P7-003, and the `decision_record` template applied in `rwb_payment` (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-28 from the proceeds read, one hop, read only (DP-19).
- `proceeds` exists in schema `rwb_payment` from the DB story of the service, with `matched_to` DF-FIN-008, `received_date` DF-FIN-007 and the seven standard record columns of TSD P8 T3.0; this story adds no table, no column and no migration.
- The P1 workload contract answers `GET /payments?businessDate={date}` and `GET /batch-status?sourceSystem=ALS&businessDate={date}`. The latter returns nullable `checksum` (string, maximum 64 characters).
- rwb-source-data answers REC-05 aggregate counts. Break and orphan detail remains Pending with the P1 data architect and P1 contract owner (GAP-1508, NEW-GAP-S2B-03).
- rwb-decision answers the rule row in force for REC-04 and REC-06 — its ID and version — so the record names a rule and not a constant; the rule set that carries them is Not specified in the source documents (GAP-2561; ASM-4224).
- The capability area Write-off and posting and its right R exist as access rows of rwb-access, and the daily run itself is unattended under the service identity (FSD P8 A2.11.3.3; TSD P8 T6.1).
- The receipts of the business date are already matched: the settlement arm of RWB-P8-E4043-APP, the sale arm of RWB-P8-E4044-APP and the balance application of RWB-P8-E4049-APP write the row; this story reads `proceeds` and never writes `matched_to`.
- No approval is needed to build against a Draft contract baseline, and a story with only platform CON build dependencies is Day 1 by rule (Template and Rules §R5.7; ASM-4227).

### 4. Flow

1. The rwb-payment source-data listener consumes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` in group `rwb-payment.rwb.source-data.events.v1`. On ALS/COMPLETED it uses signal-with-start on the separate `proceedsReconciliation` workflow ID for the event business date. It dedupes by event ID in the shared inbox, with an idempotent source/date guard in the workflow. AceDataLate is a lateness signal and starts no daily run.
2. Read payments for the event date through `GET /payments?businessDate={date}` (one row per paymentCode, ordered by paymentCode, interim unpaged). Read batch status and checksum through `GET /batch-status`. Read approved write-offs and ACE posting facts through their owners. Use their contract fakes pending publication (NEW-GAP-F07-02 and GAP-3037).
3. `ProceedsReader` reads the `proceeds` rows of the same date range in `rwb_payment` — case, receipt, source, amount, business date, `matched_to` — and groups them by `matched_to` value of LOV-MATCH, read on the reference-data contract (DP-06, DP-07), with the parameter key Not specified in the source documents (DOR-RWB-P8-E4050-APP-20) (DF-FIN-001 to DF-FIN-009).
4. Identify payment/proceeds mismatches for REC-04 and keep unmatched proceeds visible. P1 supplies REC-05 aggregate counts only.
5. Compute REC-04 from the payment and matched-proceeds counts and sums. Compute REC-06 by comparing ACE postings with approved write-offs for the business date. Read both rule IDs and versions from rwb-decision.
6. Store the REC-04 and REC-06 outcomes in `rwb_payment` keyed by `rec_code` and business date, with both rule versions, the local decision record and the processed-date guard in one transaction.
7. A failure of the record rolls the whole step back: no outcome, no counts kept, no break flagged as handled, and the run answers MSG-P7-003 (AC2; R-UNI-39).
8. The officer opens SCR-28 Proceeds matching: gateway-bff composes this service's `GET /proceeds` for the date range with the case label from rwb-case, one hop each in parallel, and shows Loading, matched or unmatched (DP-19; FSD P8 Screens).
9. On the unmatched state the officer opens the row and reads the receipt, its `account_key` and its `payment_code`; the handling of a break — the correction, the re-run and the reason — belongs to the owner of the reconciliation and the data steward (section 19).
10. Read the P1 REC-05 aggregate for the same business date. Show its counts beside the local REC-04 and REC-06 outcomes.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | The transaction rolls back: no outcome, no counts and no break handling are kept, and no case or receipt changes | MSG-P7-003 | AC2, TC-E4-050-02, TC-E4-050-04 |
| X2 | The rule row of REC-04 or REC-06 is not readable, or no version is in force | The step stops before computing anything; nothing is kept | MSG-P7-003 | AC3, TC-E4-050-01, TC-E4-050-02, TC-E4-050-05 |
| X3 | The batch record of the source is absent for the business date, or `is_complete` is not set | The run does not reconcile a guessed date; the products show their date and the step waits for the next record | MSG-P1-001 | AC4, TC-E4-050-01, TC-E4-050-06 |
| X4 | rwb-source-data does not answer the payment rows inside 2 s | The step of that business date stops and retries; the breaker opens per downstream; no partial outcome is kept | HTTP 503 | AC5, TC-E4-050-01, TC-E4-050-07 |
| X5 | The owner's `reconciliation_result` read is not available | The counts of this service are still recorded, the owner's panel shows its own unavailable state, and no figure is invented in its place | MSG-P1-001 | AC6, TC-E4-050-01, TC-E4-050-08 |
| X6 | The run is repeated for the same business date | One record and one outcome stand; the repeat is counted as an idempotency hit and no second record is written | None | AC7, TC-E4-050-01, TC-E4-050-09 |
| X7 | A key does not resolve in the view | The key is listed on the break list with its `account_key`; nothing is deleted, overwritten or excluded silently | None | AC8, TC-E4-050-01, TC-E4-050-10 |
| X8 | A caller without the right tries the read, or a case outside its scope | Refused, nothing changes; the read answers 404 for an object outside scope | MSG-P4-002 | AC9, TC-E4-050-03, TC-E4-050-11 |

X5 is the only row this story does not carry itself: the `reconciliation_result` read and its result codes are rwb-source-data's, and the operation is unnamed in the sources read (GAP-2561; ASM-4222). X7 hands the correction to the owner and the data steward; this service lists the key and never repairs another service's row.

### 6. INVEST check

| Letter | Verdict |
|---|---|
| Independent | Yes. It builds against two platform contracts, reads one owner's data product and one owner's result, and every other fact arrives on a published contract and its fake. |
| Negotiable | The rule package behind REC-04 and REC-06, the tolerance, the break handling and the product code stay with the owner and the data product owner; the story fixes only the step, the counts, the break list and the record. |
| Valuable | Yes. A day that reconciled is distinguishable from a day nobody looked at, and every unresolved key is visible to the officer and to the data steward. |
| Estimable | Yes. One activity, one reader, one break list, one record writer and one read on top of an existing table. |
| Small | Yes. One event-started workflow and no schedule. |
| Testable | Yes. AC2, the four documented refusals, the break list and the repeat for one business date are each one automated case. |

### 7. Acceptance criteria

```gherkin
Feature: Reconcile money movements daily

  Scenario: AC2 Not recorded (legacy RWB-E4-050 AC2)
    Given the rwb-source-data data-product fake (§12.8) returns the ACE payment rows and the batch-status record of business date 2026-12-14
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Rule row not readable (exception X2) (new, D-RCV-60)
    Given the rwb-decision rule-in-force fake has no rule in force for REC-04 and REC-06 at business date 2026-12-14
    When the reconciliation step runs
    Then the step stops before computing anything and nothing is kept, and the user sees MSG-P7-003

  Scenario: AC4 Batch record absent (exception X3) (new, D-RCV-60)
    Given the rwb-source-data data-product fake returns a batch record that is absent for business date 2026-12-14
    When the reconciliation step runs
    Then the run does not reconcile a guessed date, the step waits for the next record, and the user sees MSG-P1-001

  Scenario: AC5 Source does not answer in 2 s (exception X4) (new, D-RCV-60)
    Given the rwb-source-data data-product fake does not answer the payment rows within 2 s for business date 2026-12-14
    When the reconciliation step runs
    Then the step stops and retries, the breaker opens per downstream, no partial outcome is kept, and the response is HTTP 503

  Scenario: AC6 Owner's result unavailable (exception X5) (new, D-RCV-60)
    Given the reconciliation-result fake returns a read that is unavailable for business date 2026-12-14
    When the reconciliation step runs
    Then the counts of this service are recorded, the owner's panel shows its own unavailable state, no figure is invented, and the user sees MSG-P1-001

  Scenario: AC7 Repeat for the same business date (exception X6) (new, D-RCV-60)
    Given a decision record already exists for business date 2026-12-14
    When the run is repeated for that business date
    Then one record and one outcome stand, the repeat is counted as an idempotency hit, and no second record is written

  Scenario: AC8 Key does not resolve (exception X7) (new, D-RCV-60)
    Given the proceeds of business date 2026-12-14 hold no row for a payment_code of account A-0001
    When the reconciliation step runs
    Then the key is listed on the break list with its account_key, and nothing is deleted, overwritten or excluded silently

  Scenario: AC9 Caller without the right or case outside scope (exception X8) (new, D-RCV-60)
    Given a caller without Write-off and posting R reads GET /proceeds, and a case outside its scope
    When the read is taken
    Then the caller is refused with MSG-P4-002 and nothing changes, and the read of the case outside scope answers 404

  Scenario: AC10 Business rules of section 8 hold (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8 apply to business date 2026-12-14
    When the reconciliation step runs
    Then each rule of section 8 is met as that section states it

  Scenario: AC11 Error answers of the provided operations (new, D-RCV-60)
    Given a caller calls a provided operation of section 12 without a valid session, without the right, or on an object outside its scope
    When the operation answers
    Then the error answer is HTTP 401, 403 or 404 as the error set of RWB-P8-E4043-CON states, and nothing changes

  Scenario: AC12 Duplicate delivery of a consumed event (new, D-RCV-60)
    Given AceDataReady for ALS/COMPLETED and business date 2026-12-14 is delivered twice through the shared Kafka listener
    When the reconciliation run handles the redelivery
    Then one decision record and one outcome stand, the redelivery is counted as an idempotency hit, and no second record is written

  Scenario: AC13 Activity retry and timeout (new, D-RCV-60)
    Given an activity of the reconciliation step does not complete within its timeout for business date 2026-12-14
    When the activity is retried
    Then the step stops and retries, no partial outcome is kept, and the breaker opens per downstream

  Scenario: AC14 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call of the reconciliation step fails or does not answer for business date 2026-12-14
    When the reconciliation step runs
    Then the step stops before writing, no partial outcome is kept, and nothing is changed

  Scenario: AC15 Status change the model does not allow (new, D-RCV-60)
    Given a status change that the model of this service does not allow is requested for a reconciliation outcome of business date 2026-12-14
    When the change is requested
    Then the change is refused and nothing changes

  Scenario: AC16 REC-06 persists with REC-04 (RD-P1-069)
    Given the contract fakes supply approved write-offs and their ACE postings for the event date
    When the listener starts the daily reconciliation on AceDataReady for ALS/COMPLETED
    Then the REC-04 and REC-06 results and the local decision record commit in one rwb_payment transaction
    And the run reads the P1 REC-05 aggregate without writing to P1

```

The criterion is the legacy criterion of RWB-E4-050, word for word, with its origin tag added and nothing else changed: the legacy wording of "the decision log cannot be written", "the action is taken" and "nothing changes" all stand. The single leading `Given` is the only addition, and it names the cross-service part the criterion leaves open — the ACE position of the business date, which is the only other service the action reads. AC1 of the key belongs to RWB-ITG-E4050-ITG by the split the plan fixes and is asserted there as the cross-service journey; this story supplies the payment side that journey drives and reads, and its component proof is TC-E4-050-01 in section 16.

AC8: Given a key that does not resolve in the view, the key is listed on the break list with its `account_key`; nothing is deleted, overwritten or excluded silently.

AC9: Given a caller without the right, or a case outside its scope, tries the read, the request is refused with MSG-P4-002 and nothing changes; the read answers 404 for an object outside scope.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | REC-04 compares the payments in `v_ace_payment` for a business date with the proceeds matched to the case, and the difference is reported, never rounded away | Legacy RWB-E4-050 AC1; REC-04 |
| BR2 | P1 owns REC-05 and publishes aggregate counts. Unmatched proceeds remain visible through the payment read. | RD-P1-069 |
| BR3 | The business date reconciled is the one the ACE batch record in `v_ace_batch_status` carries; a missing or incomplete record is not reconciled against a guessed date | Legacy RWB-E4-050 story; VR-P8-011-1 (FSD P8 A2.11.3.1); DF-ACE-178 to DF-ACE-186 |
| BR4 | The outcome is recorded with the rule ID and the rule version of REC-04 and REC-06 in force, in the same transaction as the counts it was based on, and the caller sees MSG-P7-003 when it cannot be recorded | Legacy AC2; DP-03; R-UNI-39 |
| BR5 | rwb-payment writes REC-04 and REC-06 outcomes in `rwb_payment`. P1 owns REC-01, REC-02 and REC-05 results. | RD-P1-069, DP-01 |
| BR6 | The ACE payment, batch and write-off facts are read on rwb-source-data's contract, and this service holds no `v_ace_*` grant and copies no ACE row | DP-05; TSD P8 T5.1 |
| BR7 | No value a business person may change is written in code: the counts, the tolerance behind any reconciliation rule, the product code and the break reasons are data or the owner's values | BR-P8-011 (FSD P8 A2.11.3.1) |
| BR8 | The same business date run twice produces one outcome and one record, and the repeat is counted | R-UNI-40 |
| BR9 | REC-06 compares ACE write-off postings with approved write-offs for the date and stores its result in `rwb_payment`. | RD-P1-069, legacy AC1 |
| BR10 | The reconciliation is attested by the rate of receipts matched the same day, read from the decision records and the Workbench records; no target value is set in this story | FSD P8 A2.11.1 metric |

BR1 and BR2 run in the step and the break list, BR3 in the batch guard, BR4 in the writer that commits with the counts, BR5 and BR6 at the boundary, BR7 in the configuration read and BR8 in the inbox and the processed-date guard.

### 9. State transitions

The reconciliation state of a business date for this service, not the case state and not the receipt's match:

| From | Trigger | To | Rule |
|---|---|---|---|
| No outcome | The batch record of the source is complete and the step runs with a record written | Reconciled: one record with both counts, the difference and the rule versions; the owner's result read for the same date | BR1, BR4 |
| No outcome | The step runs and the break list is not empty | Broken: the outcome is recorded and every unresolved `account_key` and `payment_code` is listed | BR2, X7 |
| No outcome | The record cannot be written | No change: no outcome, no counts, no break handling | BR4; AC2 |
| Reconciled or Broken | The same business date is run again | No change; one outcome and one record stand, and the repeat is counted | BR8, X6 |
| Reconciled or Broken | The batch record of the source is absent or incomplete | No change; the run waits for the next record | BR3, X3 |

The case states and the `proceeds` match values are moved by rwb-case, rwb-treatment, rwb-debtsale and the matching stories of this service under their own rules; this service writes the outcome of a business date and no receipt state (TSD P8 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-payment service identity, login on schema `rwb_payment` (DP-02) | Runs the daily reconciliation under the service identity; the run is unattended and holds the primary use of the feature (FSD P8 A2.11.3.3) |
| Write-off and posting, right R (TSD P8 T6.1) | Reads the receipts and the unmatched list on `GET /proceeds`: RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT |
| Case record, right R (legacy Permission checks) | Reads the reconciliation state of the cases in scope: RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |
| Credit Administration officer (FSD P8 A2.11.3.3) | Works the unmatched list on SCR-28 and reads the owner's outcome beside it |
| rwb-access (P4) | Owns the rights, the roles and the scope data; this story calls no guard of its own and holds no role row |
| rwb-source-data (P1) | Owns JOB-04 and REC-01, REC-02 and REC-05 and supplies payment and batch facts. |

A caller outside the scope of the case answers 404, not 403, and the right is checked on the object (ADR-020; TSD P8 T6.2).

### 11. Data

| BR Field ID | Table in rwb_payment | Field | Read or write |
|---|---|---|---|
| DF-FIN-001 | proceeds | id | Read |
| DF-FIN-002 | proceeds | case_id (an identifier, no foreign key into `rwb_case`) | Read |
| DF-FIN-003 | proceeds | treatment_id (an identifier) | Read |
| DF-FIN-004 | proceeds | account_payment_id (the receipt, an identifier) | Read |
| DF-FIN-005 | proceeds | source (LOV-PROCEEDS-SRC) | Read |
| DF-FIN-006 | proceeds | amount | Read |
| DF-FIN-007 | proceeds | received_date (the date the run groups by) | Read |
| DF-FIN-008 | proceeds | matched_to (LOV-MATCH: INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED) | Read |
| DF-FIN-009 | proceeds | posting_ref (read only; the confirmation story writes it) | Read |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, DP-03) | the record of the business date: `rec_code`, counts, difference, rule IDs and versions, actor, outcome | Write |
| processed_event, idempotency_key | objects of the service template | the business-date guard of the run | Write |
| DF-ACE-043 to DF-ACE-054 | not held | `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel` of `v_ace_payment` | Read on rwb-source-data's contract |
| DF-ACE-178 to DF-ACE-186 | not held | `BatchStatusAnswer` with `sourceSystem`, `businessDate`, `status` and nullable `checksum` (maxLength 64) | Read through `GET /batch-status` |
| DF-OPS-118 to DF-OPS-129 | not held | `rec_code`, `business_date`, `product_group`, `source_count`, `workbench_count` of `reconciliation_result` | Read on rwb-source-data's contract; never written |
| DF-REF-001 to DF-REF-015 | not held | the rule row of REC-04 and REC-06, its ID and its version | Read on rwb-decision's contract |
| DF-CAS-001 to DF-CAS-023 | not held | the case reference and its label for the screen | Read on rwb-case's contract; the label through the composite route |

DF-OPS-118 to DF-OPS-129 describe the result shape. The local REC-04 and REC-06 results, decision record and date guard are written in `rwb_payment`. The inputs for REC-06 use owner contract fakes pending publication (GAP-3037 and NEW-GAP-F07-02).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/payment/v1` (the per-service base of Template and Rules §R4), shapes and error set RWB-P8-E4043-CON's.

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/proceeds` | The receipts of a case or a date range with their match value and their posting reference: query `matched`, `from`, `to`, `page`, `size`; `ProceedsPage` out (API-P8-001) | Write-off and posting, right R, scope applied |

`GET /proceeds?matched=false` is the unmatched list the officer works on SCR-28 and the Workbench side the owner's reconciliation reads; this story adds the date-range grouping and no query value of its own. `POST /proceeds/{proceedsId}/match` (API-P8-002) is the match operation of the sibling stories of this service: this story changes neither its shape nor its behaviour, and it publishes no operation for the reconciliation itself, because the step is unattended and the outcome is read from the record and the owner's result. Errors: 400 with Not specified in the source documents (CG-ALL-7780), 401 with Not specified in the source documents (CG-ALL-7780), 403 with MSG-P4-002, 404 for an object outside scope with Not specified in the source documents (CG-ALL-7780), 422 with MSG-GEN-001, 503 when a consumed answer or the record library does not answer in time with Not specified in the source documents (CG-ALL-7780).

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| `GET /payments?businessDate={date}` | `/api/recovery/source-data/v1` | P1 rwb-source-data | Date-form PaymentsAnswer, 409 MSG-P1-001 if gated. |
| `GET /batch-status` | `/api/recovery/source-data/v1` | P1 rwb-source-data | Source and date batch status with nullable `checksum` of up to 64 characters. |
| Pending posting facts (GAP-3037) | P1 contract | rwb-source-data | ACE posting facts for REC-06. Interim fake. |
| Pending approved write-offs (NEW-GAP-F07-02) | S7 contract | rwb-writeoff | Approved write-off facts for REC-06. Interim fake. |
| `GET /data-products/freshness` | `/api/recovery/source-data/v1` | P1 rwb-source-data | The business date the ACE position is complete for (BR3): `status` `LOADED` or `STALE`; `businessDate` is null with `STALE` where the product was never stamped, and no date is then reconciled; the stamp in use is the latest row; freshness is read only through this operation |
| `GET /admin/reconciliation/results` | `/api/recovery/source-data/v1` | P1 rwb-source-data | REC-05 aggregate for the date. Break and orphan detail are Pending (GAP-1508). |
| The rule-in-force read (operation name Not specified in the source documents (GAP-2561; ASM-4224)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule row of REC-04 and REC-06 with its ID and version, which the record names |

Each row is one hop with a 2 s timeout, one retry on a GET and a breaker per downstream (ADR-020). The REC-06 inputs use owner contract fakes pending publication. The case label of the screen arrives through the composite route and is not a call of this story. These rows are class C in fact while the plan's contract row is None, so they are built against the owners' published documents and fakes from Day 1 (ASM-4227).

#### 12.3 Events published

None. The three events of the service — `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) — sit on `rwb.payment.events.v1` and are published by the sibling stories; the catalogue holds no reconciliation event, so the outcome is announced on the record and the reads and on nothing else (GAP-2561; ASM-4223). The local decision record reaches the central ledger on the shared `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON, not through an event of this story.

#### 12.4 Events consumed

| Event | Read or topic | Payload used | When | Owner and service |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1`, group `rwb-payment.rwb.source-data.events.v1` | `sourceSystem`, `businessDate`, `status`, `completedAt` (the event is keyed `{sourceSystem}:{businessDate}`) | Starts the daily reconciliation of a business date only on `sourceSystem` `ALS` and `status` `COMPLETED` | P1, rwb-source-data |

The rwb-payment source-data listener consumes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` in group `rwb-payment.rwb.source-data.events.v1`. On ALS/COMPLETED it uses signal-with-start on the separate `proceedsReconciliation` workflow ID for the event business date. It dedupes by event ID in the shared inbox, with an idempotent source/date guard in the workflow. AceDataLate is a lateness signal and starts no daily run.

#### 12.5 Workflows and activities

| Name | Type | Queue | Contract element |
|---|---|---|---|
| `proceedsReconciliation` | Event-started workflow with its own ID per business date | `rwb-payment` in namespace `rwb-recovery` | In: source and business date. Out: the `rec_code` list with both counts and the difference, the break list size and the record id |
| ACE facts read | Local activity calling the P1 REST operations | `rwb-payment` | In: event business date. Out: payments, batch and freshness answers. |
| The rule-in-force read | Activity provided by rwb-decision, called as a task | `rwb-decision` | In: package and business date. Out: the rule ID and version |

The shared listener starts `proceedsReconciliation` on its own stable workflow ID per business date. Retry: 1 s initial interval, back-off 2, 10 attempts. A rule missing from the version in force is non-retryable.

#### 12.6 Schedules

No Schedule is created. The shared source-data listener starts `proceedsReconciliation` on AceDataReady for ALS/COMPLETED.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8, schema `rwb_payment` | Read only here: the receipts, their date and their match value; created by the DB story of the service |
| `decision_record` | Platform library, created in `rwb_payment` | The outcome of a business date with the rule IDs and versions (DP-03) |
| `processed_event` | Platform library, created in `rwb_payment` | The business-date guard of the run |
| `idempotency_key` | Platform library, created in `rwb_payment` | One key per business date and `rec_code` |

The standard library handles the decision record outbox. REC-04 and REC-06 results are local to `rwb_payment`. The P1 results, S7 write-off table and ACE views are never accessed as tables by rwb-payment. Pending: whether the REC-04 and REC-06 outcomes need a table of their own in `rwb_payment` beyond `decision_record`, since no source names one, owner rwb-payment owner with data architect, tracked as NEW-GAP-G7-2; until then the outcomes are held in `decision_record` and no table is added.

Personal data: the personal-data classification of the fields this story reads (`account_key`, `payment_code`, the receipt and the case) is Not specified in the source documents (DOR-RWB-P8-E4050-APP-11).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake (RWB-P1-E1006-CON family) | Three payment rows of account `A-0001` at business date `2026-12-14`; a batch record that is COMPLETE; a batch record that is absent | TC-E4-050-01 |
| rwb-source-data reconciliation-result fake | One result row per `rec_code` for `2026-12-14`; one date with no row; a read that is unavailable | TC-E4-050-01 |
| rwb-decision rule-in-force fake | REC-04 and REC-06 at a pinned version; a package with no rule in force | TC-E4-050-01, TC-E4-050-02 |
| Decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain and a stopped chain with MSG-P7-003 | AC2, TC-E4-050-02, TC-E4-050-04 |
| gateway-bff composite route fake | The merged SCR-28 answer: matched and unmatched rows with the case label | TC-E4-050-01 |
| Authorise stub of the service template | Right R held and not held | TC-E4-050-03 |

Each fake answers only what its owner documents; the product code and the two operation names that are not published carry the placeholder of their gap until the owners confirm them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `GET /proceeds` on `/api/recovery/payment/v1`; the two rwb-source-data data-product reads and the result read, and the rwb-decision rule read, one hop each, 2 s |
| Kafka | None published by this story, 1 consumed | EV-26 is consumed through the P1 AsyncAPI and the shared rwb-payment source-data group. The platform inbox library dedupes the delivery. |
| Temporal | 1 workflow | `proceedsReconciliation` (event-started) on `rwb-payment`, plus the owners' read activities on `rwb-source-data` and `rwb-decision` |
| File | None | No file is produced or consumed by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `reconciliation`.

| Component | Type | Responsibility |
|---|---|---|
| ReconciliationBatchGuard | Service | Reads the batch record of the source and pins the business date; refuses a date the record does not carry or a record that is not complete |
| AcePositionReader | Service | Reads the payment rows of `v_ace_payment` for the business date on rwb-source-data's product operation |
| ProceedsReader | Service | Reads the `proceeds` rows of the date range in `rwb_payment` and groups them by `matched_to` |
| BreakListBuilder | Service | Lists the receipts and keys that do not resolve, with their `account_key`, and never deletes a row |
| ReconciliationRecordWriter | Service | The one transaction: the local decision record with both counts, the difference, the rule IDs and versions, and the date guard, or nothing |
| OwnerResultReader | Service | Reads the owner's `reconciliation_result` rows for the `rec_code` and business date, and shows its unavailable state plainly |
| ProceedsResource | Controller | `GET /proceeds` with its right, its scope and its error map; the unmatched list is the same read with `matched=false` |

**Database and migrations.** No new table and no new column: `proceeds` DF-FIN-001 to DF-FIN-009 already exists in the baseline of RWB-P8-E4043-CON, `decision_record` and `processed_event` are template objects, the DB story of the service owns the migration, and this story adds an index-free read on `(matched_to, received_date)`. No Flyway file is written here.

**Configuration.** No business value: the product code, the tolerance behind any reconciliation rule, the rule package and the result codes are data or the owner's values (BR7). Two settings only, the page size of the read and the retry count of the run, neither fixed by a source in the read set (GAP-2561; ASM-4225).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 fixes the record written in the transaction of the outcome, which is what AC2 protects. DP-05 is applied as the owner's contract: the payment and batch-status facts of DF-ACE-043 to DF-ACE-054 and DF-ACE-178 to DF-ACE-186 are read on rwb-source-data's operations, and this service holds no `v_ace_*` grant. DP-19 is behind SCR-28. The two H rows of the table are the ones the metadata carries, and no DP row of this key adds a contract dependency; the consumed reads are class C in fact (ASM-4227).

**Build steps.** (1) The batch guard and the date pin against the fakes, X3. (2) The ACE product reader and the proceeds reader, X4. (3) The break list builder and the unmatched read, X7. (4) The writer with the record and the outcome in one transaction, AC2, X1, X2. (5) The owner's result reader and its unavailable state, X5. (6) The repeat guard, X6. (7) `GET /proceeds` with the right, the scope and the error map, X8. (8) The absence assertions: no `v_ace_*` grant, no write to P1 tables, no cross-schema key, no Schedule, no outbox row.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P8-E4043-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON stay green, and a SIT week shows one outcome per business date with both counts and the rule versions, an unresolved key listed on the unmatched read and unchanged in the table, a repeated run writing nothing, and a stopped record leaving the counts, the break list and the case untouched with MSG-P7-003.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required value is missing from the read (422) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A caller without the right (403, X8) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The rule is not in force or the record cannot be written (AC2, X1, X2) |
| MSG-P1-001 | Error | {product} is from {date}. Today's load has not arrived. | The batch of the source is late, failed or unreadable (VR-P8-011-1, X3, X5) |

The three rows of the legacy message set are MSG-GEN-001, MSG-P4-002 and MSG-P7-003; VR-P8-011-1 is the stale-product row the FSD adds for this feature. No message text is assembled in code, and every refusal is one problem document with a code, the message ID and a correlation reference.

### 15. Screens and states

| Screen | State | What it shows |
|---|---|---|
| SCR-28 Proceeds matching | Loading | The reconciliation for the business date is running; a skeleton, no partial totals |
| SCR-28 Proceeds matching | matched | One row per receipt with its case, its amount, its date, its match value and the `rec_code` outcome with the rule versions |
| SCR-28 Proceeds matching | unmatched | Every `account_key` and `payment_code` that does not resolve, with the reason the owner gives it, and the case label beside it |
| SCR-28 Proceeds matching | empty | Not specified in the source documents (CG-ALL-7788) |
| SCR-28 Proceeds matching | error | Not specified in the source documents (CG-ALL-7788) |
| SCR-28 Proceeds matching | no access | Not specified in the source documents (CG-ALL-7788) |

SCR-28 is a gateway-bff composite route: the receipts, the match value and the outcome come from this service, the case label from rwb-case, and the two are merged one hop each, in parallel (DP-19). The owner's `reconciliation_result` panel is read from rwb-source-data and shows its own unavailable state rather than a figure this service invents (X5). The screen declares no business value of its own; the field states, colours and error display follow the Design System and Component Library.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-050-01 | AC1 (run by RWB-ITG-E4050-ITG) as the component check of the payment side: the three payments of the ACE batch date are compared with the proceeds on the case, the unresolved keys are listed, the outcome is recorded by `rec_code` and business date with the rule version, and the owner's result is read beside it; AC1 itself is owned by RWB-ITG-E4050-ITG | Component | rwb-source-data data-product fake (§12.8): account `A-0001` with three payments at business date `2026-12-14`, one of them with no proceeds row, and the proceeds of case `RC-2026-000555` |
| TC-E4-050-02 | AC2: the record cannot be written, so nothing changes and the caller sees MSG-P7-003 | Component | The record library stub stops the chain; no outcome, no counts, no break handling |
| TC-E4-050-03 | Access: a role without the right is refused with MSG-P4-002, and a case outside scope answers 404 | Component | A caller without Write-off and posting R on `GET /proceeds` |
| TC-E4-050-04 | Principle 5: a forced decision-log write failure stops the action with MSG-P7-003 and raises one incident under R-UNI-39 | NFR | The record store stopped during a business date; the run is repeated after recovery |
| TC-E4-050-05 | AC3: the rule row of REC-04 or REC-06 is not readable, so the step stops before computing anything and nothing is kept | Component | The rwb-decision rule-in-force fake with no rule in force for REC-04 and REC-06 at business date `2026-12-14` |
| TC-E4-050-06 | AC4: the batch record of the source is absent for the business date, so no date is guessed, the step waits, and MSG-P1-001 is answered | Component | The rwb-source-data data-product fake with a batch record that is absent for business date `2026-12-14` |
| TC-E4-050-07 | AC5: rwb-source-data does not answer the payment rows within 2 s, so the step stops and retries, keeps no partial outcome, and answers HTTP 503 | Component | The rwb-source-data data-product fake that does not answer the payment rows of business date `2026-12-14` within 2 s |
| TC-E4-050-08 | AC6: the owner's `reconciliation_result` read is unavailable, so this service's counts are recorded, the owner's panel shows its unavailable state, and no figure is invented; MSG-P1-001 | Component | The reconciliation-result fake with a read that is unavailable for business date `2026-12-14` |
| TC-E4-050-09 | AC7: the run is repeated for the same business date, so one record and one outcome stand and no second record is written | Component | A decision record already written for business date `2026-12-14`, and the repeated run for that date |
| TC-E4-050-10 | AC8: a key does not resolve in the view, so it is listed on the break list with its `account_key` and nothing is deleted, overwritten or excluded | Component | Account `A-0001` with a `payment_code` that has no proceeds row at business date `2026-12-14` |
| TC-E4-050-11 | AC9: a caller without the right is refused with MSG-P4-002, and a case outside its scope answers 404 | Component | A caller without Write-off and posting R on `GET /proceeds`, and a case outside its scope |
| TC-E4-050-12 | Contract: the operations, events and activities of section 12 hold against the contract fakes of section 12.8 | Contract | The fakes of section 12.8, each answering only what its owner documents |
| TC-E4-050-13 | Boundary: the tables of section 12.7 are read or written only as that table states, and no other table is touched | Component | The tables of section 12.7 |
| TC-E4-050-14 | AC10: the business rules BR1 to BR10 of section 8 hold | Component | Not specified in the source documents (NEWAC-RWB-P8-E4050-APP-AC10) |
| TC-E4-050-15 | AC11: the provided operations answer HTTP 401, 403 or 404 as the error set of RWB-P8-E4043-CON states | Contract | The contract fakes of section 12.8 and the error set of RWB-P8-E4043-CON |
| TC-E4-050-16 | AC12: a redelivered AceDataReady completion record for business date `2026-12-14` leaves one record and one outcome and counts an idempotency hit | Component | The AceDataReady completion record of business date `2026-12-14`, delivered twice on the shared source-data topic |
| TC-E4-050-17 | AC13: an activity of the step does not complete within its timeout, so the step retries and keeps no partial outcome | Component | The rwb-source-data data-product fake that does not answer within its timeout for business date `2026-12-14` |
| TC-E4-050-18 | AC14: a consumed call fails or does not answer, so the step stops before writing and keeps no partial outcome | Component | A consumed call of the step that fails at business date `2026-12-14` |
| TC-E4-050-19 | AC15: a status change the model does not allow is refused and nothing changes | Component | A status change that the model of this service does not allow for business date `2026-12-14` |

AC16 has no test case in Test Cases v9. Pending: the test case of AC16, owner QA lead, tracked as NEW-GAP-G7-3.

Every legacy test case of RWB-E4-050 appears once with its legacy ID and its legacy intent, and the Level column is the target level: the payment side is proved at component level here, the whole journey in the integration harness. The `-ITG` copies of the four cases belong to RWB-ITG-E4050-ITG and are not restated. The account, case and date values are the synthetic examples of FSD P8 A2.1 and the legacy criterion, and no business threshold appears in the data column.

### 17. Guardrails

- No business value in code: the product code, the tolerance behind any reconciliation rule, the rule package and the result codes are data or the owner's values; the rule ID and version are read in force and named on the record (BR7).
- No personal data in an event, a workflow input, a log or a test: a record and a result row carry a `rec_code`, two counts, a difference, a receipt code, an account key, a business date and a rule identity only, never a name, an address, a contact value or an identity number. Every example is synthetic.
- ACE data only through the owner's contract: the payment and batch-status rows come from rwb-source-data, and this service holds no `v_ace_*` grant and copies no ACE row (DP-05).
- No write outside `rwb_payment`: `reconciliation_result`, the `rec_code` values and the break handling are the owner's; this service computes its side, records its own outcome and reads the owner's result (BR5).
- No read of another service's table: the rule comes from rwb-decision's contract, the case label through the composite route, and `rwb_payment` is the only schema written (DP-01).
- The record precedes the change and both or neither: the step writes the decision record and the outcome in one transaction (BR4; R-UNI-39).
- One hop, 2 s, a breaker per downstream, one retry on a GET, and one outcome per business date and `rec_code` (ADR-020; BR8).
- The service holds one base, one topic, one queue and one login: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login; this story adds no topic name, no event name and no Schedule.

### 18. Traceability

| Source | Reference | Used in | Feature | L3 process |
|---|---|---|---|---|
| Legacy story | RWB-E4-050, AC2 owned word for word by this story; AC1 owned by RWB-ITG-E4050-ITG | 1, 7, 16 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Feature | FEAT-PAY-11 Reconcile money movements daily, module P8 (E4); priority Must; depends on FEAT-RDF-11 | 1, 2 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| FSD P8 v3 | A2.11 (intent, steps, VR-P8-011-1, BR-P8-011, roles, metric); AC-P8-011-01; AC-EXC-P8-011-01 and -02; AC-BG-P8-011-01; SCR-28 | 2, 3, 4, 8, 14, 15 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| TSD P8 v2 | T2 components; T3.0 standard columns and T3.1 `proceeds` DF-FIN-001 to DF-FIN-009; T5.1; T6.1 rights; T-A.1 API-P8-001 | 10, 11, 12 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Routing logic v4 | R-UNI-39, R-UNI-40; REC-04, REC-05 and REC-06 as the legacy key names them | 8, 9, 19 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Jobs and events | The batch record of the source (EV-26 `AceDataReady`); JOB-04 Reconciliation is P1's; EV-11, EV-12, EV-25 are the sibling stories' | 4, 12.3, 12.4 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Requirements | REQ-CHO-009, REQ-RDF-007, REQ-RDF-008 (Business Requirements Program v5) | 2, 8, 19 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Patterns | DP-03, DP-05, DP-19 (Template and Rules §R5.5) | 13 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Split and journey | RWB-ITG-E4050-ITG sections 1, 4, 11, 12.2 and 19; RWB-P8-E4043-APP, RWB-P8-E4044-APP, RWB-P8-E4049-APP | 1, 7, 16, 19 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Gaps and assumptions | GAP-2561; ASM-4222 to -6 | 2, 3, 4, 5, 12, 13 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Decisions | ADR-013, ADR-014, ADR-020, ADR-022; D-RCV-60 | all | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |

| Legacy reference | Where it is kept | Feature | L3 process |
|---|---|---|---|
| Legacy key RWB-E4-050, disposition Split (rework) | Metadata; sections 1, 19 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Legacy AC2 | Section 7, word for word with its origin tag; TC-E4-050-02 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Legacy AC1 (the four moves, the record with the rule version) | Sections 1, 4 and 8 here; the criterion itself in RWB-ITG-E4050-ITG | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| REC-04 and REC-06 for the payment side | Sections 4, 8, 9, 13 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| REC-06 and the write-off posting | Section 19; owned by rwb-writeoff and rwb-source-data | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Data entities `recovery_case`, `v_ace_account`, `v_ace_payment`, `v_ace_write_off`, `v_ace_batch_status`, `proceeds`, `write_off`, `reconciliation_result`, `decision_log_entry`, `rule_row` | Section 11, each with its owner | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Endpoints "None; a service or a scheduled job" | Sections 4, 12.1, 12.5, 12.6 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| SCR-28 Proceeds matching and its three states | Section 15 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Permission right R and the unattended primary role | Sections 10, 12.1, 16 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Messages MSG-GEN-001, MSG-P4-002, MSG-P7-003 | Section 14, exception paths | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |
| Legacy test cases TC-E4-050-01 to -04 | Section 16 | FEAT-PAY-11 | Not specified in the source documents (DOR-RWB-P8-E4050-APP-2) |

### 19. Out of scope

- P1 JOB-04 and the calculation of REC-01, REC-02 and REC-05.
- Ownership and publication of approved write-offs and ACE posting facts used by payment REC-06.
- The payment and proceeds matching of a business date, the settlement arm, the sale-proceeds arm and the balance application: RWB-P8-E2008-APP, RWB-P8-E4043-APP, RWB-P8-E4044-APP and RWB-P8-E4049-APP.
- The daily payment matching that raises a missed payment (JOB-07) in rwb-payment and the booking confirmation (JOB-08) in rwb-integration.
- The published shapes, the `proceeds` baseline, the event schemas, the error set and the fakes: RWB-P8-E4043-CON.
- The case, its state, its tasks and its timers: rwb-case (P3).
- The rule packages, the rule rows, their version and the central ledger: rwb-decision (P7).
- The ACE views and the freshness of the data product: rwb-source-data (P1), reached through its contract only.
- The rights, the scopes and the masking behind the read: rwb-access (P4) and the guard of the service template.
- The composite route and the field lists of SCR-28: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence report: RWB-ITG-E4050-ITG.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

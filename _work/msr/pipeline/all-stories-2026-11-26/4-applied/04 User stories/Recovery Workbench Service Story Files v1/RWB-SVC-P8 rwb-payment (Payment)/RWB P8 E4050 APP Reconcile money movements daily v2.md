# RWB-P8-E4050-APP Reconcile money movements daily

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

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
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60 (realignment v1), 22 November 2026: new service story, split from RWB-E4-050 for `rwb-payment`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P8-E4050-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Credit Administration officer**, I want **the Workbench to reconcile the payments and the write-offs ACE holds against the cases every day**, so that **every payment and booking is matched to its case** — in the target, as the reconcilable side of `rwb-payment`: for one business date the service compares the receipts it matched with the payments ACE holds in that view, records the outcome with the rule ID and version in force, and lists every key that does not resolve, so the officer sees matched or unmatched on SCR-28 and the owner of the reconciliation reads the same numbers.

This is the application slice of legacy RWB-E4-050 (FEAT-PAY-11 Reconcile money movements daily, module P8 Payments and posting, priority Must, depends on FEAT-RDF-11). It owns:

- the legacy acceptance criterion AC2 of the key, copied word for word with its origin tag; AC1 of the key is owned by RWB-ITG-E4050-ITG and is not restated here (section 7);
- the daily money reconciliation step of this service (`proceedsReconciliation`), an activity on task queue `rwb-payment` in namespace `rwb-recovery`, started from the batch completion record of the source for a business date: it reads the payments ACE holds for that date on rwb-source-data's contract, reads the `proceeds` rows of the same date range in `rwb_payment`, and computes for each `rec_code` the source count, the Workbench count and the difference (DP-05; FSD P8 A2.11; legacy AC1's four moves for the payment side);
- the break list of REC-05, which this service does not compute as a new thing but keeps visible: every `payment_code` and `account_key` whose proceeds row carries `matched_to = UNMATCHED`, listed on `GET /proceeds` with `matched=false` and never deleted or silently dropped (legacy AC1; REQ-RDF-007, REQ-RDF-008);
- the local decision record of every daily reconciliation, written through RWB-PLT-E1027-CON in the same transaction as the outcome, naming REC-04 and REC-05 with the rule ID and version in force, and MSG-P7-003 when it cannot be written (DP-03; R-UNI-39; legacy AC2);
- the read of the owner's result for the same `rec_code` and business date on rwb-source-data's contract, so the officer sees the owner's outcome beside this service's counts and not a figure copied into P8;
- SCR-28 Proceeds matching with its three states, reached through the gateway-bff composite route (DP-19; FSD P8 Screens).

It does not own: the published shapes of the operations, the `proceeds` baseline, the event schemas, the error set and the fakes, which are RWB-P8-E4043-CON; the reconciliation itself — its workflow, its rules REC-04 and REC-05, the tolerance, the break handling and the `reconciliation_result` row with its `rec_code` and business date — which the Ownership Map places with rwb-source-data (P1) on Architecture v5 slides 41 and 44, and which is the substance of RWB-ITG-E4050-ITG; the approved write-off and its posting `posted_date`, which are rwb-writeoff's (S7), so the posting side REC-06 of the legacy criterion is not this story's; the payment and proceeds matching of a business date, which are RWB-P8-E2008-APP, RWB-P8-E4043-APP, RWB-P8-E4044-APP and RWB-P8-E4049-APP; the ACE views, which are ACE's and are read only through rwb-source-data's data product; the case, its state, its tasks and its timers, which are rwb-case's (P3); the rule rows and the central ledger, which are rwb-decision's (P7); the rights and scopes, which are rwb-access's (P4); the cross-service journey of the key, which is RWB-ITG-E4050-ITG; and the deployment of this build, which is the operations story of the key.

### 2. Business rationale

A daily reconciliation that a person cannot reproduce is a number nobody can defend, and a payment ACE holds that never reached a case is money the bank cannot account for. The legacy key states the work in four moves: REC-04 matches the payments in `v_ace_payment` to the proceeds matched to the case, REC-06 matches the posting in `v_ace_write_off` to the approved write-off, REC-05 lists every `account_key` and `payment_code` that does not resolve in the view, and the outcome is written by `rec_code` and business date (legacy RWB-E4-050 AC1; D-RCV-35 U4). The business objective is unchanged: reconcile the payments ACE holds against the cases every day and write the result to the decision log with the rule version (FSD P8 A2.11.1; FEAT-PAY-11).

What D-RCV-60 changes is who owns which of the four moves. The receipts, their match and the plain `rwb_payment` facts behind them are this service's (`proceeds`, DF-FIN-001 to DF-FIN-009; context pack ownership row). The reconciliation, its workflow, the rule set and the `reconciliation_result` row are not: the Ownership Map records `reconciliation_result` under P1 `rwb-source-data` and JOB-04 Reconciliation as an event-triggered workflow there, started by `AceDataReady`. The legacy key wrote the row inside module P8 because the P8 code lived there; the map moves it, and the higher source wins (Template and Rules §R3). This story therefore supplies, proves and records the P8 side of the comparison and reads the owner's result beside it, and it writes no row of another service (GAP-2561; ASM-4222).

The split makes the outcome provable in two places instead of one. On this side, one decision record per business date carries the rule ID, the version, the two counts and the break list, so a day that reconciled is distinguishable from a day nobody looked at. On the owner's side, `reconciliation_result` carries the same `rec_code` and business date for the whole bank. The officer sees both on SCR-28, composed one hop each. AC2 is the rule that keeps the record and the state consistent: the record is written in the transaction that keeps the outcome, so a reconciliation that cannot be recorded changes nothing and the officer sees MSG-P7-003 (DP-03; R-UNI-39; ADR-022).

No business value is invented. The rule package behind REC-04 and REC-05, the tolerance, the product code that serves the three ACE views, the operation that reads `reconciliation_result` and its result codes are named by no source in the read set: they stay unstated with the placeholder and the recorded gap and assumptions, and every count, field, list value and message is one the FSD, the TSD, the routing logic and the legacy story already carry (GAP-2561; ASM-4224, -4).

### 3. Preconditions

- RWB-P8-E4043-CON is published: base `/api/recovery/payment/v1`, `GET /proceeds` with `ProceedsPage`, `POST /proceeds/{proceedsId}/match` with `MatchRequest` and `Proceeds`, the `proceeds` baseline with DF-FIN-001 to DF-FIN-009, the `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` schemas, the error set and the fakes. This story builds behind that contract and adds no shape of its own.
- RWB-PLT-E1027-CON is published: the decision-record writer declared to run in the caller's transaction, failing with MSG-P7-003, and the `decision_record` template applied in `rwb_payment` (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-28 from the proceeds read, one hop, read only (DP-19).
- `proceeds` exists in schema `rwb_payment` from the DB story of the service, with `matched_to` DF-FIN-008, `received_date` DF-FIN-007 and the seven standard record columns of TSD P8 T3.0; this story adds no table, no column and no migration.
- The ACE position of the business date is readable: the payment rows of `v_ace_payment` and the batch record of `v_ace_batch_status`, one hop on rwb-source-data's contract with a 2 s timeout, because this service holds no `v_ace_*` grant and reads no ACE table (DP-05; TSD P8 T5.1 INT-02 and INT-16). The data product code that serves them is Not specified in the source documents (GAP-2561; ASM-4225).
- rwb-source-data answers the `reconciliation_result` rows of a `rec_code` and a business date; the operation name and the field and result-code names are Not specified in the source documents (GAP-2561; ASM-4222).
- rwb-decision answers the rule row in force for REC-04 and REC-05 — its ID and version — so the record names a rule and not a constant; the rule set that carries them is Not specified in the source documents (GAP-2561; ASM-4224).
- The capability area Write-off and posting and its right R exist as access rows of rwb-access, and the daily run itself is unattended under the service identity (FSD P8 A2.11.3.3; TSD P8 T6.1).
- The receipts of the business date are already matched: the settlement arm of RWB-P8-E4043-APP, the sale arm of RWB-P8-E4044-APP and the balance application of RWB-P8-E4049-APP write the row; this story reads `proceeds` and never writes `matched_to`.
- No approval is needed to build against a Draft contract baseline, and a story with only platform CON build dependencies is Day 1 by rule (Template and Rules §R5.7; ASM-4227).

### 4. Flow

1. The ACE batch of the source completes for a business date. The completion record is read on rwb-source-data's contract: `source_system`, `business_date`, `status`, `is_complete` (EV-26; DF-ACE-178 to DF-ACE-186). No topic is subscribed, and the run is keyed by the business date that record carries and never by a date in code (FSD P8 A2.11; BR6).
2. `AcePositionReader` reads the payment rows of `v_ace_payment` for that business date — `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel` — on rwb-source-data's product operation (DP-05; DF-ACE-043 to DF-ACE-054). The product code is Not specified in the source documents (GAP-2561).
3. `ProceedsReader` reads the `proceeds` rows of the same date range in `rwb_payment` — case, receipt, source, amount, business date, `matched_to` — and groups them by `matched_to` value of LOV-MATCH (DF-FIN-001 to DF-FIN-009).
4. `BreakListBuilder` lists the keys that do not resolve: every `payment_code` in the ACE position with no `proceeds` row of the date, and every `proceeds` row carrying `matched_to = UNMATCHED`, together with its `account_key`. The list is the REC-05 output for the payment side and is kept, not deleted (legacy AC1; REQ-RDF-007).
5. `ProceedsReconciliationStep` computes, for each `rec_code` the run covers, the source count, the Workbench count, the difference and the sums behind them (DF-OPS-118 to DF-OPS-129's shape), and reads the rule row in force for REC-04 and REC-05 on rwb-decision's contract for the ID and version the record must name (DP-03; DP-05).
6. In one `rwb_payment` transaction the step writes the local decision record — `rec_code`, business date, both counts, the difference, the break list size, the rule IDs and versions, the actor and the outcome — and the processed-date guard of the run. It writes no `reconciliation_result` row, changes no `proceeds` row and moves no case state (BR5; ASM-4222; legacy AC1's record move).
7. A failure of the record rolls the whole step back: no outcome, no counts kept, no break flagged as handled, and the run answers MSG-P7-003 (AC2; R-UNI-39).
8. The officer opens SCR-28 Proceeds matching: gateway-bff composes this service's `GET /proceeds` for the date range with the case label from rwb-case, one hop each in parallel, and shows Loading, matched or unmatched (DP-19; FSD P8 Screens).
9. On the unmatched state the officer opens the row and reads the receipt, its `account_key` and its `payment_code`; the handling of a break — the correction, the re-run and the reason — belongs to the owner of the reconciliation and the data steward (section 19).
10. The owner's reconciliation step for the same business date reads the same Workbench side through `GET /proceeds` and its own `reconciliation_result` row names the `rec_code` and the business date; the officer sees the owner's outcome and this service's counts side by side, and the two agree or the break list explains the difference (RWB-ITG-E4050-ITG sections 4 and 12.2).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | The transaction rolls back: no outcome, no counts and no break handling are kept, and no case or receipt changes | MSG-P7-003 | AC2, TC-E4-050-02, TC-E4-050-04 |
| X2 | The rule row of REC-04 or REC-05 is not readable, or no version is in force | The step stops before computing anything; nothing is kept | MSG-P7-003 | TC-E4-050-01, TC-E4-050-02 |
| X3 | The batch record of the source is absent for the business date, or `is_complete` is not set | The run does not reconcile a guessed date; the products show their date and the step waits for the next record | MSG-P1-001 | TC-E4-050-01 |
| X4 | rwb-source-data does not answer the payment rows inside 2 s | The step of that business date stops and retries; the breaker opens per downstream; no partial outcome is kept | HTTP 503 | TC-E4-050-01 |
| X5 | The owner's `reconciliation_result` read is not available | The counts of this service are still recorded, the owner's panel shows its own unavailable state, and no figure is invented in its place | MSG-P1-001 | TC-E4-050-01 |
| X6 | The run is repeated for the same business date | One record and one outcome stand; the repeat is counted as an idempotency hit and no second record is written | None | TC-E4-050-01 |
| X7 | A key does not resolve in the view | The key is listed on the break list with its `account_key`; nothing is deleted, overwritten or excluded silently | None | TC-E4-050-01 |
| X8 | A caller without the right tries the read, or a case outside its scope | Refused, nothing changes; the read answers 404 for an object outside scope | MSG-P4-002 | TC-E4-050-03 |

X5 is the only row this story does not carry itself: the `reconciliation_result` read and its result codes are rwb-source-data's, and the operation is unnamed in the sources read (GAP-2561; ASM-4222). X7 hands the correction to the owner and the data steward; this service lists the key and never repairs another service's row.

### 6. INVEST check

| Letter | Verdict |
|---|---|
| Independent | Yes. It builds against two platform contracts, reads one owner's data product and one owner's result, and every other fact arrives on a published contract and its fake. |
| Negotiable | The rule package behind REC-04 and REC-05, the tolerance, the break handling and the product code stay with the owner and the data product owner; the story fixes only the step, the counts, the break list and the record. |
| Valuable | Yes. A day that reconciled is distinguishable from a day nobody looked at, and every unresolved key is visible to the officer and to the data steward. |
| Estimable | Yes. One activity, one reader, one break list, one record writer and one read on top of an existing table. |
| Small | Yes. No new table, no new column, no workflow and no schedule. |
| Testable | Yes. AC2, the four documented refusals, the break list and the repeat for one business date are each one automated case. |

### 7. Acceptance criteria

```gherkin
Feature: Reconcile money movements daily

  Scenario: AC2 Not recorded (legacy RWB-E4-050 AC2)
    Given the rwb-source-data contract mock returns the ACE payment rows and the batch-status record of business date 2026-12-14
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The criterion is the legacy criterion of RWB-E4-050, word for word, with its origin tag added and nothing else changed: the legacy wording of "the decision log cannot be written", "the action is taken" and "nothing changes" all stand. The single leading `Given` is the only addition, and it names the cross-service part the criterion leaves open — the ACE position of the business date, which is the only other service the action reads. AC1 of the key belongs to RWB-ITG-E4050-ITG by the split the plan fixes and is asserted there as the cross-service journey; this story supplies the payment side that journey drives and reads, and its component proof is TC-E4-050-01 in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | REC-04 compares the payments in `v_ace_payment` for a business date with the proceeds matched to the case, and the difference is reported, never rounded away | Legacy RWB-E4-050 AC1; REC-04 |
| BR2 | REC-05 lists every `account_key` and `payment_code` that does not resolve in its view; the list is kept and no Workbench row is deleted, overwritten or silently excluded | Legacy RWB-E4-050 AC1; REC-05; REQ-RDF-007; REQ-RDF-008 |
| BR3 | The business date reconciled is the one the ACE batch record in `v_ace_batch_status` carries; a missing or incomplete record is not reconciled against a guessed date | Legacy RWB-E4-050 story; VR-P8-011-1 (FSD P8 A2.11.3.1); DF-ACE-178 to DF-ACE-186 |
| BR4 | The outcome is recorded with the rule ID and the rule version of REC-04 and REC-05 in force, in the same transaction as the counts it was based on, and the caller sees MSG-P7-003 when it cannot be recorded | Legacy AC2; DP-03; R-UNI-39 |
| BR5 | The `reconciliation_result` row and its `rec_code` and business date are rwb-source-data's; this service computes and records its own side and reads the owner's result, and writes no row outside `rwb_payment` | Ownership Map (`reconciliation_result` P1); DP-01; ASM-4222 |
| BR6 | The ACE payment, batch and write-off facts are read on rwb-source-data's contract, and this service holds no `v_ace_*` grant and copies no ACE row | DP-05; TSD P8 T5.1 |
| BR7 | No value a business person may change is written in code: the counts, the tolerance behind any reconciliation rule, the product code and the break reasons are data or the owner's values | BR-P8-011 (FSD P8 A2.11.3.1) |
| BR8 | The same business date run twice produces one outcome and one record, and the repeat is counted | R-UNI-40 |
| BR9 | The posting side of the key — REC-06 over `v_ace_write_off` and the approved write-off — stays with rwb-writeoff and the owner of the reconciliation and is not computed here | Legacy RWB-E4-050 AC1 (REC-06); Ownership Map (`write_off` S7); ASM-4226 |
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
| rwb-source-data (P1) | Owns the reconciliation, JOB-04, the rules REC-04 and REC-05, the break handling and `reconciliation_result` |

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
| DF-ACE-178 to DF-ACE-186 | not held | `source_system`, `business_date`, `status`, `record_count`, `checksum`, `is_complete` of `v_ace_batch_status` | Read on rwb-source-data's contract |
| DF-OPS-118 to DF-OPS-129 | not held | `rec_code`, `business_date`, `product_group`, `source_count`, `workbench_count` of `reconciliation_result` | Read on rwb-source-data's contract; never written |
| DF-REF-001 to DF-REF-015 | not held | the rule row of REC-04 and REC-05, its ID and its version | Read on rwb-decision's contract |
| DF-CAS-001 to DF-CAS-023 | not held | the case reference and its label for the screen | Read on rwb-case's contract; the label through the composite route |

Field IDs are those of TSD P8 T3.1 and the Logical Data Model v8. `proceeds` is the only business table this story reads, and it writes no column of it; the two write rows are the decision record and the date guard, both of the service template (DP-01, DP-03). The legacy data table also names `write_off` (DF-FIN-010 to DF-FIN-020) and `v_ace_write_off` (DF-ACE-261 to DF-ACE-269) for REC-06: those belong to rwb-writeoff and the owner of the reconciliation, and this story does not read them (BR9; ASM-4226). `v_ace_account` (DF-ACE-001 to DF-ACE-042) is in the legacy table but is not read here, because the reconciliation of this key is over payments, proceeds and their matches.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/payment/v1` (the per-service base of Template and Rules §R4), shapes and error set RWB-P8-E4043-CON's.

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/proceeds` | The receipts of a case or a date range with their match value and their posting reference: query `matched`, `from`, `to`, `page`, `size`; `ProceedsPage` out (API-P8-001) | Write-off and posting, right R, scope applied |

`GET /proceeds?matched=false` is the unmatched list the officer works on SCR-28 and the Workbench side the owner's reconciliation reads; this story adds the date-range grouping and no query value of its own. `POST /proceeds/{proceedsId}/match` (API-P8-002) is the match operation of the sibling stories of this service: this story changes neither its shape nor its behaviour, and it publishes no operation for the reconciliation itself, because the step is unattended and the outcome is read from the record and the owner's result. Errors: 400, 401, 403 with MSG-P4-002, 404 for an object outside scope, 422 with MSG-GEN-001, 503 when a consumed answer or the record library does not answer in time.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| `GET /data-products/{productCode}/records` | `/api/recovery/source-data/v1` | P1 rwb-source-data | The `v_ace_payment` rows and the `v_ace_batch_status` record of the business date (DP-05); the product code is Not specified in the source documents (GAP-2561; ASM-4225) |
| `GET /data-products/freshness` | `/api/recovery/source-data/v1` | P1 rwb-source-data | The business date the ACE position is complete for (BR3) |
| The reconciliation-result read (operation name Not specified in the source documents (GAP-2561; ASM-4222)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The owner's rows for a `rec_code` and the business date, shown beside this service's counts |
| The rule-in-force read (operation name Not specified in the source documents (GAP-2561; ASM-4224)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule row of REC-04 and REC-05 with its ID and version, which the record names |

Each row is one hop with a 2 s timeout, one retry on a GET and a breaker per downstream (ADR-020). Both unwritten names are contract placeholders and no call is invented in their place. The case label of the screen arrives through the composite route and is not a call of this story. All four rows are class C in fact while the plan's contract row is None, so they are built against the owners' published documents and fakes from Day 1 (ASM-4227).

#### 12.3 Events published

None. The three events of the service — `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) — sit on `rwb.payment.events.v1` and are published by the sibling stories; the catalogue holds no reconciliation event, so the outcome is announced on the record and the reads and on nothing else (GAP-2561; ASM-4223). The local decision record reaches the central ledger on the shared `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON, not through an event of this story.

#### 12.4 Events consumed

| Event | Read or topic | Payload used | When |
|---|---|---|---|
| `AceDataReady` (EV-26) | `recovery.v_ace_batch_status` through rwb-source-data, not delivered on a topic | `source_system`, `business_date`, `status`, `is_complete` | Starts the daily reconciliation of a business date when the batch of the source is COMPLETED |

The step subscribes to no topic, because the P8 ownership rows carry no consumed event and the trigger is the batch record the matching run already waits for (ASM-4223). A repeat of a business date is deduped in `processed_event` of `rwb_payment` on (source, business date) (R-UNI-40).

#### 12.5 Workflows and activities

| Name | Type | Queue | Contract element |
|---|---|---|---|
| `proceedsReconciliation` | Activity of the event-started run of a business date | `rwb-payment` in namespace `rwb-recovery` | In: source and business date. Out: the `rec_code` list with both counts and the difference, the break list size and the record id |
| The ACE product read and the freshness read | Activities provided by rwb-source-data, called as a task | `rwb-source-data` | In: product code and business date. Out: the rows of section 11 |
| The rule-in-force read | Activity provided by rwb-decision, called as a task | `rwb-decision` | In: package and business date. Out: the rule ID and version |

This story registers no workflow of its own: the ownership rows of P8 hold no workflow, and the activity runs inside the batch run of the source (context pack; TSD P8 T4). Retry: 1 s initial interval, back-off 2, 10 attempts; a rule that is not in force is non-retryable.

#### 12.6 Schedules

None. The reconciliation starts on the batch completion record of the source (EV-26; FSD P8 A2.11.4.4) and no Temporal Schedule and no legacy Quartz row is declared for this key. The daily timing of the source batch is ACE's ingestion, and JOB-04 Reconciliation is rwb-source-data's event-triggered workflow, not a Schedule of this service (TSD P8 T5.1; Architecture v5 slide 44; ASM-4223).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8, schema `rwb_payment` | Read only here: the receipts, their date and their match value; created by the DB story of the service |
| `decision_record` | Platform library, created in `rwb_payment` | The outcome of a business date with the rule IDs and versions (DP-03) |
| `processed_event` | Platform library, created in `rwb_payment` | The business-date guard of the run |
| `idempotency_key` | Platform library, created in `rwb_payment` | One key per business date and `rec_code` |

`outbox_event` is not written by this story, which publishes no event. `reconciliation_result` and the ACE views are P1's, `write_off` is S7's, `rule_row` and the ledger are P7's, `recovery_case` and `task` are P3's, and the rights are P4's; none is read as a table here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake (RWB-P1-E1006-CON family) | Three payment rows of account `A-0001` at business date `2026-12-14`; a batch record that is COMPLETE; a batch record that is absent | TC-E4-050-01 |
| rwb-source-data reconciliation-result fake | One result row per `rec_code` for `2026-12-14`; one date with no row; a read that is unavailable | TC-E4-050-01 |
| rwb-decision rule-in-force fake | REC-04 and REC-05 at a pinned version; a package with no rule in force | TC-E4-050-01, TC-E4-050-02 |
| Decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain and a stopped chain with MSG-P7-003 | AC2, TC-E4-050-02, TC-E4-050-04 |
| gateway-bff composite route fake | The merged SCR-28 answer: matched and unmatched rows with the case label | TC-E4-050-01 |
| Authorise stub of the service template | Right R held and not held | TC-E4-050-03 |

Each fake answers only what its owner documents; the product code and the two operation names that are not published carry the placeholder of their gap until the owners confirm them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `GET /proceeds` on `/api/recovery/payment/v1`; the two rwb-source-data data-product reads and the result read, and the rwb-decision rule read, one hop each, 2 s |
| Kafka | None published, none consumed on a topic | The trigger is the batch record read on rwb-source-data's contract (EV-26) |
| Temporal | 1 activity, no workflow | `proceedsReconciliation` on `rwb-payment`, plus the owners' read activities on `rwb-source-data` and `rwb-decision` |
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

DP-03 fixes the record written in the transaction of the outcome, which is what AC2 protects. DP-05 is applied as the owner's contract: the payment and batch-status facts of DF-ACE-043 to DF-ACE-054 and DF-ACE-178 to DF-ACE-186 are read on rwb-source-data's operations, and this service holds no `v_ace_*` grant. DP-19 is behind SCR-28. The two H rows of the table are the ones the metadata carries, and no DP row of this key adds a contract dependency; the four consumed reads are class C in fact (ASM-4227).

**Build steps.** (1) The batch guard and the date pin against the fakes, X3. (2) The ACE product reader and the proceeds reader, X4. (3) The break list builder and the unmatched read, X7. (4) The writer with the record and the outcome in one transaction, AC2, X1, X2. (5) The owner's result reader and its unavailable state, X5. (6) The repeat guard, X6. (7) `GET /proceeds` with the right, the scope and the error map, X8. (8) The absence assertions: no `v_ace_*` grant, no write to `reconciliation_result`, no cross-schema key, no Schedule, no outbox row.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P8-E4043-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON stay green, and a SIT week shows one outcome per business date with both counts and the rule versions, an unresolved key listed on the unmatched read and unchanged in the table, a repeated run writing nothing, and a stopped record leaving the counts, the break list and the case untouched with MSG-P7-003.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required value is missing from the read (422) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A caller without the right (403, X8) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The rule is not in force or the record cannot be written (AC2, X1, X2) |
| MSG-P1-001 | Error | {product} is from {date}. Today's ACE batch has not arrived. | The batch of the source is late, failed or unreadable (VR-P8-011-1, X3, X5) |

The three rows of the legacy message set are MSG-GEN-001, MSG-P4-002 and MSG-P7-003; VR-P8-011-1 is the stale-product row the FSD adds for this feature. No message text is assembled in code, and every refusal is one problem document with a code, the message ID and a correlation reference.

### 15. Screens and states

| Screen | State | What it shows |
|---|---|---|
| SCR-28 Proceeds matching | Loading | The reconciliation for the business date is running; a skeleton, no partial totals |
| SCR-28 Proceeds matching | matched | One row per receipt with its case, its amount, its date, its match value and the `rec_code` outcome with the rule versions |
| SCR-28 Proceeds matching | unmatched | Every `account_key` and `payment_code` that does not resolve, with the reason the owner gives it, and the case label beside it |

SCR-28 is a gateway-bff composite route: the receipts, the match value and the outcome come from this service, the case label from rwb-case, and the two are merged one hop each, in parallel (DP-19). The owner's `reconciliation_result` panel is read from rwb-source-data and shows its own unavailable state rather than a figure this service invents (X5). The screen declares no business value of its own; the field states, colours and error display follow the Design System and Component Library.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-050-01 | AC1 as the component check of the payment side: the three payments of the ACE batch date are compared with the proceeds on the case, the unresolved keys are listed, the outcome is recorded by `rec_code` and business date with the rule version, and the owner's result is read beside it; AC1 itself is owned by RWB-ITG-E4050-ITG | Component | Account `A-0001` with three payments at business date `2026-12-14`, one of them with no proceeds row, and the proceeds of case `RC-2026-000555` |
| TC-E4-050-02 | AC2: the record cannot be written, so nothing changes and the caller sees MSG-P7-003 | Component | The record library stub stops the chain; no outcome, no counts, no break handling |
| TC-E4-050-03 | Access: a role without the right is refused with MSG-P4-002, and a case outside scope answers 404 | Component | A caller without Write-off and posting R on `GET /proceeds` |
| TC-E4-050-04 | Principle 5: a forced decision-log write failure stops the action with MSG-P7-003 and raises one incident under R-UNI-39 | NFR | The record store stopped during a business date; the run is repeated after recovery |

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

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-050, AC2 owned word for word by this story; AC1 owned by RWB-ITG-E4050-ITG | 1, 7, 16 |
| Feature | FEAT-PAY-11 Reconcile money movements daily, module P8 (E4); priority Must; depends on FEAT-RDF-11 | 1, 2 |
| FSD P8 v3 | A2.11 (intent, steps, VR-P8-011-1, BR-P8-011, roles, metric); AC-P8-011-01; AC-EXC-P8-011-01 and -02; AC-BG-P8-011-01; SCR-28 | 2, 3, 4, 8, 14, 15 |
| TSD P8 v2 | T2 components; T3.0 standard columns and T3.1 `proceeds` DF-FIN-001 to DF-FIN-009; T5.1; T6.1 rights; T-A.1 API-P8-001 | 10, 11, 12 |
| Routing logic v4 | R-UNI-39, R-UNI-40; REC-04, REC-05 and REC-06 as the legacy key names them | 8, 9, 19 |
| Jobs and events | The batch record of the source (EV-26 `AceDataReady`); JOB-04 Reconciliation is P1's; EV-11, EV-12, EV-25 are the sibling stories' | 4, 12.3, 12.4 |
| Requirements | REQ-CHO-009, REQ-RDF-007, REQ-RDF-008 (Business Requirements Program v5) | 2, 8, 19 |
| Patterns | DP-03, DP-05, DP-19 (Template and Rules §R5.5) | 13 |
| Split and journey | RWB-ITG-E4050-ITG sections 1, 4, 11, 12.2 and 19; RWB-P8-E4043-APP, RWB-P8-E4044-APP, RWB-P8-E4049-APP | 1, 7, 16, 19 |
| Gaps and assumptions | GAP-2561; ASM-4222 to -6 | 2, 3, 4, 5, 12, 13 |
| Decisions | ADR-013, ADR-014, ADR-020, ADR-022; D-RCV-60 | all |

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E4-050, disposition Split (rework) | Metadata; sections 1, 19 |
| Legacy AC2 | Section 7, word for word with its origin tag; TC-E4-050-02 |
| Legacy AC1 (the four moves, the record with the rule version) | Sections 1, 4 and 8 here; the criterion itself in RWB-ITG-E4050-ITG |
| REC-04 and REC-05 for the payment side | Sections 4, 8, 9, 13 |
| REC-06 and the write-off posting | Section 19; owned by rwb-writeoff and rwb-source-data |
| Data entities `recovery_case`, `v_ace_account`, `v_ace_payment`, `v_ace_write_off`, `v_ace_batch_status`, `proceeds`, `write_off`, `reconciliation_result`, `decision_log_entry`, `rule_row` | Section 11, each with its owner |
| Endpoints "None; a service or a scheduled job" | Sections 4, 12.1, 12.5, 12.6 |
| SCR-28 Proceeds matching and its three states | Section 15 |
| Permission right R and the unattended primary role | Sections 10, 12.1, 16 |
| Messages MSG-GEN-001, MSG-P4-002, MSG-P7-003 | Section 14, exception paths |
| Legacy test cases TC-E4-050-01 to -04 | Section 16 |

### 19. Out of scope

- The reconciliation itself, its workflow, the rules REC-04 and REC-05 as the owner evaluates them, the tolerance, the break handling and the `reconciliation_result` row with its `rec_code` and business date: rwb-source-data (P1), driven by JOB-04 on `AceDataReady`.
- The posting side of the legacy criterion, REC-06 over `v_ace_write_off` and the approved write-off: rwb-writeoff (S7) and the owner of the reconciliation.
- The payment and proceeds matching of a business date, the settlement arm, the sale-proceeds arm and the balance application: RWB-P8-E2008-APP, RWB-P8-E4043-APP, RWB-P8-E4044-APP and RWB-P8-E4049-APP.
- The daily payment matching that raises a missed payment (JOB-07) and the booking confirmation (JOB-08): the sibling stories of this service.
- The published shapes, the `proceeds` baseline, the event schemas, the error set and the fakes: RWB-P8-E4043-CON.
- The case, its state, its tasks and its timers: rwb-case (P3).
- The rule packages, the rule rows, their version and the central ledger: rwb-decision (P7).
- The ACE views and the freshness of the data product: rwb-source-data (P1), reached through its contract only.
- The rights, the scopes and the masking behind the read: rwb-access (P4) and the guard of the service template.
- The composite route and the field lists of SCR-28: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence report: RWB-ITG-E4050-ITG.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

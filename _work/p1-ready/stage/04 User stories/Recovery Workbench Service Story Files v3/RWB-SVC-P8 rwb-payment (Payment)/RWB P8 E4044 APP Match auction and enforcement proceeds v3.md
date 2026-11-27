# RWB-P8-E4044-APP Match auction and enforcement proceeds

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-061, RD-P1-066: Start auction and enforcement matching on the shared ACE event listener and read receipts and batch status from the source-data API.
- EV-26 is cited with its published record key and payload, and the start rule is `source_system` ALS with status COMPLETED (RD-P1-003, RD-P1-040).


| Item | Value |
|---|---|
| Story key | RWB-P8-E4044-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Contract version | rwb-payment REST contract 5.0.0 (Recovery Workbench API Specification v5, rwb-payment.yaml, info.version 5.0.0; base /api/recovery/payment/v1); consumes rwb-source-data.yaml 5.1.0 and the P1 AsyncAPI |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-061, RD-P1-066 |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-044 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P8-G |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement |
| Depends on (build) | RWB-P8-E4044-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-source-data payment data product; rwb-case reference-data read; rwb-case case-state read; rwb-decision rule package; rwb-integration posting file (one hop each, 2 s budget; built on published documents and fakes from Day 1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs; traced to FEAT-PAY-04, VR-P8-004-1 and BR-P8-004; requirement ID not specified in the source documents (GAP-1375)) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (29 resolved, 18 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **sale officer**, I want **the Workbench to match money from an auction, a broker or the LED to the right case**, so that **every payment and booking is matched to its case**.

This is the application slice of legacy RWB-E4-044, feature FEAT-PAY-04 of module P8 Payments and posting. It owns:

- the two legacy acceptance criteria of the story, copied word for word with their origin tag, and the messages, screen and rights they use;
- the auction and enforcement proceeds workflow, started by EV-26 for a completed ALS batch date, which reads receipts through `GET /payments?businessDate={date}` and writes one local `proceeds` row per receipt (DP-05; FSD P8 A2.4; TSD P8 T3.1);
- the resolution of the case for a receipt of source `AUCTION`, `AGENCY`, `BUYER` or `LED`, and its match to `SALE_PROCEEDS` or `UNMATCHED` under the match rules in force;
- the manual match `POST /proceeds/{proceedsId}/match` on base `/api/recovery/payment/v1` for the Write-off and posting right U, and the read `GET /proceeds` for right R (TSD P8 API-P8-001 and API-P8-002; DP-13);
- the decision record of every match exactly as DP-03 requires: record first, then the row, both or neither (R-UNI-39);
- the publication of `ProceedsMatched` (`rwb.payment.ProceedsMatched.v1`, EV-25) on `rwb.payment.events.v1` through the outbox, in the same transaction as the `proceeds` row (DP-09);
- SCR-28 Proceeds matching in its loading, matched and unmatched states, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the `proceeds` element list, the three event schemas of the service, the consumed rows, the error set and the fakes, which are RWB-P8-E4044-CON; the payment-to-plan matching and the missed-payment event (FEAT-PAY-01), which are RWB-P8-E2008-APP and RWB-P8-E2027; the settlement payment of RWB-E4-043 and the deed-in-lieu rental auto-debit of RWB-E4-048, which are sibling stories of this service; the case of record, its states, tasks and timers, which are rwb-case's (P3); the asset, its listing and its sale, which are rwb-asset's (S5); the lot, the buyer and the award, which are rwb-debtsale's (S6); the write-off decision, which is rwb-writeoff's (S7); the treatment, which is rwb-treatment's (S2); the ACE payment and batch facts, which are rwb-source-data's (P1); and the rule packages, rule rows and central ledger, which are rwb-decision's (P7).

### 2. Business rationale

Money reaches Recovery through many doors. A payment against a restructured plan arrives on the customer path; auction money, broker money and LED enforcement money arrive with a reference that has to be resolved to a case before anything can be applied or posted. The legacy module matched all of them by hand against plans and settlements, and the FSD records the consequence in one line: payments are matched to plans and settlements by hand, and broken plans are found late (FSD P8 A1.3). The measure the feature is judged on is the same one for the whole module: receipts matched the same day, rising each month, read from the decision log and the Workbench records (FSD P8 A2.4.1).

In the target the step is the fifth of six in the recovery journey: money is matched to the case and posted, and the service that does it is rwb-payment (Architecture v5 slide 3, step 5 "Collect"). What D-RCV-60 changes is who owns each part of that step. The `proceeds` row, its match and its event belong to this service and to this schema. The case belongs to rwb-case, the asset to rwb-asset, the lot and the award to rwb-debtsale, the write-off to rwb-writeoff, the treatment to rwb-treatment, and the rule version that decides a match to rwb-decision. The match is therefore a read of other owners' facts plus one write of this service's own row, and no other module's table is read.

### 3. Preconditions

- The user holds a Workbench role with right R or U in the capability area Write-off and posting; the manual match needs U, the read needs R (legacy Permission checks; TSD P8 T6.1).
- The shared source-data listener receives AceDataReady for ALS with status COMPLETED and the business date. Late or failed batches do not start matching. When the run needs the batch row, it calls `GET /batch-status` (VR-P8-004-1).
- The payment-to-plan matching of FEAT-PAY-01 is in place, because the `proceeds` row and the unmatched list of SCR-28 are shared with it (FSD P8 A2.4 Prerequisites; RWB-P8-E2008-APP).
- The match rules of the proceeds arm are readable at a version, and no tolerance, window or grace value is written in code (FSD P8 A2.4.3.1 BR-P8-004; GAP-2519; ASM-4169).
- The build dependencies are tagged: RWB-P8-E4044-CON for the published shapes, RWB-PLT-E1027-CON for the local decision record, RWB-PLT-N001-CON for the composite route of SCR-28.
- The fakes of the consumed reads answer the documented shapes, so the build never waits for another service (ADR-020; GAP-2518; ASM-4168).

### 4. Flow

1. The rwb-payment listener consumes EV-26 from `rwb.source-data.events.v1` in group `rwb-payment.rwb.source-data.events.v1`. Only `sourceSystem=ALS` and `status=COMPLETED` invoke Temporal signal-with-start on the auction and enforcement matching run's workflow ID for the event business date. The listener dedupes the CloudEvent ID in the shared inbox and the workflow guards the source and date. AceDataLate reports lateness and starts no matching.
2. Read receipts for the event business date through `GET /payments?businessDate={date}`. A gated 409 MSG-P1-001 holds matching with no proceeds write.
3. For each receipt it resolves the case: the case reference carried by the auction, broker or LED remittance when there is one, otherwise the open case of the account, read on rwb-case's contract, operation Not specified in the source documents (GAP-2518) (one hop, 2 s).
4. It evaluates the match rules in force for the proceeds sources and records the rule ID and version with the answer. The proceeds arm of the payment match package is read on rwb-decision; its package code and rule IDs are Not specified in the source documents (GAP-2519; GAP-2518). Every threshold, window, grace and priority that the decision uses is a rule row of rwb-decision, never a constant (BR-P8-004; GAP-2519). The rules are read as governed rule rows of rwb-decision on its contract; payment_match_rule is not declared as a table of this service until the Ownership Map gives it an owner (GAP-1373).
5. It writes the `proceeds` row of schema `rwb_payment`: `case_id`, `treatment_id` when the money belongs to a treatment, `source` from `LOV-PROCEEDS-SRC`, `amount`, `received_date`, `matched_to` from `LOV-MATCH`, `posting_ref` when the ACE record carries one (DF-FIN-002 to DF-FIN-009).
6. The decision record is written first — rule ID, version, inputs, answer, hash-linked to the previous record of the case — and the row follows in the same transaction; a failure of either leaves neither, and the receipt is retried on the next run (DP-03; R-UNI-39).
7. `ProceedsMatched` is written to the outbox in the same transaction and published by the relay to `rwb.payment.events.v1` with the case as the key; the case router of rwb-case consumes it (EV-25; DP-09). The payment events follow the CloudEvents 1.0 envelope with the event id and the case key; every further payload element of the payment events is Not specified in the source documents (GAP-1376) until the event owner publishes the AsyncAPI document.
8. The manual path: the Credit Administration officer opens an unmatched receipt on SCR-28 and posts the match to a case and an account with `POST /proceeds/{proceedsId}/match`, under an `Idempotency-Key` header. The MatchRequest carries the case reference and `matched_to` from `LOV-MATCH`; every further element of MatchRequest is Not specified in the source documents (GAP-1371). The same record-then-change transaction and the same event follow.
9. SCR-28 shows the receipts of D with their match status, merged by gateway-bff from this service and the case reference of rwb-case (DP-19).
10. SCR-28 has four states: empty (no receipts for D), loading, error, and no access (a caller without the right of the manual match gets the refusal of TC-E4-044-03).

### 5. Exception paths

| Condition | What happens | Message or reference | Covered by |
|---|---|---|---|
| The decision record cannot be written | Nothing changes; the receipt stays unmatched and the action is refused; an incident is raised | MSG-P7-003; R-UNI-39; AC2 | AC2 |
| The ACE batch for source ALS is late or failed | The run does not match; the product is shown with its date | MSG-P1-001 {product} is from {date}. Today's load has not arrived. (VR-P8-004-1) | Not specified in the source documents (DOR-RWB-P8-E4044-APP-3) |
| A role without the right tries the read or the match | Refused, nothing changes | MSG-P4-002 | AC3 |
| The proceeds reference is unknown or out of the caller's scope | One problem document, no change | HTTP 404 | AC3 |
| The receipt is already matched and a second match is posted under a new key | Refused, the stored answer is not overwritten | HTTP 409 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-3) |
| A required element of the match is missing or invalid | Refused, nothing changes | MSG-GEN-001; HTTP 422 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-3) |
| A consumed read does not answer inside 2 s | The run stops for that receipt and retries; the breaker opens per downstream | HTTP 503; ADR-020 | AC7 |
| The same business date is run twice | No second row and no second event; the repeat is counted | R-UNI-40 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-3) |
| A receipt resolves to no case | No matched row; the receipt is reported unmatched on SCR-28 | R-LIT-72; `matched_to` UNMATCHED | Not specified in the source documents (DOR-RWB-P8-E4044-APP-3) |
| A receipt on no open case at all | Held on the exception list of the matching family, which is RWB-P8-E2008-APP's behaviour, not a new row here | FSD P8 AC-EXC-P8-001-02 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-3) |

### 6. INVEST check

| Letter | Verdict |
|---|---|
| Independent | Yes. It builds against the contract story and two platform contracts; no other service's build blocks it. |
| Negotiable | Yes. The shape of the answer and the rule values stay with their owners; the story fixes only the flow and the record. |
| Valuable | Yes. Money that arrives without the customer path is matched to the right case, and the match is provable. |
| Estimable | Yes. Two operations, one table, one event, one activity on a published contract. |
| Small | Yes. One activity, one write, one event and one screen state set. |
| Testable | Yes. Two legacy criteria plus the documented 404, 409, 422 and 503 answers. |

### 7. Acceptance criteria

```gherkin
Feature: Match auction and enforcement proceeds

  Scenario: AC1 Match auction and enforcement proceeds (legacy RWB-E4-044 AC1)
    Given the rwb-case contract mock returns the case and the rwb-decision contract mock returns the rule version in force
    Given a case with an account, a receipt of source AUCTION or LED on the business date with its amount, and the rule version of the proceeds arm are in place
    When its trigger arrives
    Then matches money from an auction, a broker or the LED to the right case
    Then the system writes the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-044 AC2)
    Given the decision log write is mocked to fail
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Error answers of the provided operations (new, D-RCV-60)
    Given a caller of POST /proceeds/{proceedsId}/match
    When the caller is not authenticated, is not authorised, or names an unknown proceeds
    Then the answer is 401, 403 or 404 respectively and nothing changes

  Scenario: AC4 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given a write with an idempotency key has already been applied
    When the same write is replayed with the same idempotency key
    Then no second write is made and nothing changes

  Scenario: AC5 Duplicate delivery of a consumed event (new, D-RCV-60)
    Given an event has already been consumed
    When the same event is delivered again
    Then the event is not processed twice and nothing changes

  Scenario: AC6 Activity retry and timeout (new, D-RCV-60)
    Given the matching activity of 12.5 is running
    When the activity is retried or times out
    Then no duplicate match is written

  Scenario: AC7 A consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call to rwb-case or rwb-decision fails or does not answer
    When the match runs
    Then nothing changes and the failure is reported

  Scenario: AC8 A disallowed status change is refused (new, D-RCV-60)
    Given a proceeds whose status does not allow the requested change
    When the change is requested
    Then the change is refused and nothing changes
```

The mock `Given` line of AC1 carries the two facts the legacy line leaves open; every legacy value of both criteria is kept, and AC1 Then uses decision record wording in place of decision log wording (CG-ALL-7650). The synthetic data set the two criteria are exercised on is stated in ASM-4167 and is used in the test cases of section 16 only. A broker receipt has no value in LOV-PROCEEDS-SRC: its value is Not specified in the source documents (GAP-1372); no list value is added, and the value is confirmed with the reference-data owner when the list version in force is published.

### 8. Business rules

| ID | Rule | Message | BR ID |
|---|---|---|---|
| BR-P8-004 | No value a business person may change is written in code; it is read from reference data or the rule package with its version | None | BR-P8-004 |
| VR-P8-004-1 | Data product stale after a late or failed ACE batch for its source (source-data batch status) | MSG-P1-001 {product} is from {date}. Today's load has not arrived. | Not specified in the source documents (DOR-RWB-P8-E4044-APP-4) |
| R-LIT-65 | LED auction round sold: match the proceeds to the case | None | Not specified in the source documents (DOR-RWB-P8-E4044-APP-4) |
| R-LIT-72 | Proceeds with no case reference: hold the cash unmatched and raise a daily exception to the case owner | None | Not specified in the source documents (DOR-RWB-P8-E4044-APP-4) |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-4) |
| R-UNI-48 | Asset proceeds clear the balance in full: close the case, release the remaining security and refund any surplus per policy | None | Not specified in the source documents (DOR-RWB-P8-E4044-APP-4) |

R-LIT-65 and R-LIT-72 are the two rows of the litigation route set whose event is `PROCEEDS_MATCHED`, and the proceeds they describe are the money this story matches (Business Rules and Routing Logic v4). R-UNI-48 is the downstream case move of rwb-case and is stated here only because the matched amount is its input.

The lists this story uses are `LOV-PROCEEDS-SRC` and `LOV-MATCH` (TSD P8 T3.2), read through the reference-data contract (DP-06, DP-07); the parameters it reads are Not specified in the source documents (DOR-RWB-P8-E4044-APP-20).

### 9. State transitions

| From | Trigger | To | Rule |
|---|---|---|---|
| No row | A receipt of source `AUCTION`, `AGENCY`, `BUYER` or `LED` resolves to a case and matches | `proceeds` row with `matched_to` SALE_PROCEEDS | R-LIT-65 |
| No row | The receipt carries no case reference and no open case resolves | `proceeds` row with `matched_to` UNMATCHED, daily exception | R-LIT-72 |
| UNMATCHED | The manual match under right U | SALE_PROCEEDS on the same row, with a new record | AC1 |
| Any | The decision record or the row write fails | No change; nothing is published | R-UNI-39 |

The case state, its route stage and its timers are not moved here: this story writes one row of its own schema and publishes the fact, and rwb-case decides what the case does with it.

### 10. Authority

Capability area **Write-off and posting**, declared per operation in the contract and enforced by the service (TSD P8 T6.1, T6.2).

| Right | Roles that hold it (TSD P8 T6.1) |
|---|---|
| R (read) | RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT |
| U (match) | RW-WRITEOFF, RW-CREDITAD, SY-DATALOAD |

The legacy permission table of the key gives the same two rights and adds nine roles to the read list; the module matrix is the authority for the list and the legacy line for the intent. The right is checked on the object: a caller scoped away from the case gets 404, not 403.

### 11. Data

| Element | Type | Source | Note | BR Field ID |
|---|---|---|---|---|
| `proceeds.id` | uuid | Workbench | DF-FIN-001 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `case_id` | uuid | rwb-case reference | DF-FIN-002 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `treatment_id` | uuid, optional | rwb-treatment reference | DF-FIN-003 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `account_payment_id` | uuid, optional | ACE payment reference | DF-FIN-004; GAP-2521 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `source` | `LOV-PROCEEDS-SRC` | Workbench | DF-FIN-005: CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER, GUARANTOR | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `amount` | numeric(18,2) | ACE payment fact | DF-FIN-006 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `received_date` | date | ACE payment fact | DF-FIN-007 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `matched_to` | `LOV-MATCH` | Workbench | DF-FIN-008: INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |
| `posting_ref` | varchar(40), optional | ACE payment fact | DF-FIN-009 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-7) |

Read receipts via `GET /payments?businessDate={date}`, the batch row via `GET /batch-status` when needed, and the case reference via rwb-case. The table carries the seven standard record columns. No ACE payment is copied, no account or payment master is held, and no table of another owner is read: `recovery_case` (P3), `treatment` (S2), `asset` and `sale` (S5), `debt_sale_lot` (S6), `write_off` (S7) and `rule_row`, `rule_package_version` and `decision_log_entry` (P7) are named by their owners only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13). This story supplies the behaviour behind the two operations whose shapes are declared by RWB-P8-E4044-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, query `matched`, `from`, `to`, `page`, `size`, paginated (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header; the answer is stored and returned on a repeat |

The answers: 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope proceeds reference, 409 on an already matched receipt under a new key, 422 with MSG-GEN-001 for an invalid element, 503 when the decision library or a consumed read does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2518; ASM-4168)) | `/api/recovery/case/v1` | P3 rwb-case | The open case of the account or the case named by the remittance: its reference and stage; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2518; ASM-4168)) | `/api/recovery/decision/v1` | P7 rwb-decision | The proceeds arm of the match package at the version in force, with its rule IDs; faked |
| GET `/payments?businessDate={date}` | `/api/recovery/source-data/v1` | P1 rwb-source-data | Date-form PaymentsAnswer, one row per paymentCode ordered by paymentCode, interim unpaged. 409 MSG-P1-001 when gated. Builder RWB-P1-E1013-APP, contract RWB-P1-E1015-CON. |
| GET `/batch-status` | `/api/recovery/source-data/v1` | P1 rwb-source-data | BatchStatusAnswer for the source and business date, using the rwb-payment workload identity. |

Each row is one hop with a 2 s timeout, one retry on a GET and a breaker per downstream (ADR-020). The plan gives this slice no C dependency, so the two rows are built against the fakes and their owners confirm the names before the contract tag.

#### 12.3 Events published

| Event | Topic | Envelope | Key |
|---|---|---|---|
| `ProceedsMatched` (`rwb.payment.ProceedsMatched.v1`, EV-25) — payload `proceedsId`, `caseId`, `amount` | `rwb.payment.events.v1` | CloudEvents 1.0, event id and subject | The case reference |

`TreatmentBooked` (EV-11) and `PaymentMissed` (EV-12) sit on the same topic and are published by the sibling stories of this service; the schema is declared once in RWB-P8-E4044-CON, and this story publishes only `ProceedsMatched`. The event is written to the outbox in the same transaction as the row; there is no event without the row and no row without the event (DP-09; Event and Messaging Design rule Transactions).

#### 12.4 Events consumed

| Event | Read or topic | Payload used | When | Owner |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1`, group `rwb-payment.rwb.source-data.events.v1` | Payload: `sourceSystem`, `businessDate`, `status`, `completedAt`. Record key: `{sourceSystem}:{businessDate}`. | Starts the auction and enforcement matching workflow on ALS/COMPLETED only | P1 rwb-source-data |

The rwb-payment listener consumes EV-26 from `rwb.source-data.events.v1` in group `rwb-payment.rwb.source-data.events.v1`. Only `sourceSystem=ALS` and `status=COMPLETED` invoke Temporal signal-with-start on the auction and enforcement matching run's workflow ID for the event business date. The listener dedupes the CloudEvent ID in the shared inbox and the workflow guards the source and date. AceDataLate reports lateness and starts no matching.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| Auction and enforcement matching run | Workflow, one execution per business date | `rwb-payment` in namespace `rwb-recovery` | Signal-with-start from the shared listener with source, business date and event ID. |
| The matching activity, name Not specified in the source documents (GAP-2520; ASM-4170) | Activity | `rwb-payment` | In: business date. Out: the row, record and outbox references, in one transaction |

Drools is called only inside an activity, so a replay reuses the recorded answer; the record and the change are one transaction (DP-03; the slide 14 pattern of the Temporal and Drools design). Retry: 1 s initial interval, back-off 2, 10 attempts.

#### 12.6 Schedules

None. The run starts on the ACE batch completion of source ALS for a business date (FSD P8 A2.4 AC-BG-P8-004-01; EV-26); no Temporal Schedule and no legacy Quartz row is declared for it (DP-10 is not applied by this story).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8, schema `rwb_payment` | The table of TSD P8 T3.1 with the standard record columns |
| `outbox_event` | Platform library, created in `rwb_payment` | The `ProceedsMatched` row (DP-09) |
| `inbox_event` | Platform library, created in `rwb_payment` | The (source, business date) replay guard (DP-09) |
| `decision_record` | Platform library, created in `rwb_payment` | The local decision record of DP-03 |
| `idempotency_key` | Platform library, created in `rwb_payment` | The `Idempotency-Key` of the manual match |

The Flyway baseline of the service is a `V0001` sequence in `rwb_payment`, owned by the DB story of this service (DP-15 is not applied by this story). No table of another owner is declared.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read | The open case of account `A-0611` as `RC-2026-000611`; no case for `A-0998`; an answer slower than 2 s | AC1, TC-E4-044-01, -03 |
| rwb-decision rule-package read | The proceeds arm at version `PM-2026.12` with its rule IDs; a replaced version | AC1, TC-E4-044-01 |
| Decision-record stub (RWB-PLT-E1027-CON) | A healthy chain and a stopped chain | AC2, TC-E4-044-02, -04 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case and the unmatched list | AC1, TC-E4-044-01 |
| Authorise stub of the service template | The two rights, and a caller without U | TC-E4-044-03 |
| rwb-source-data contract fake (ACE receipts and batch status) | Not specified in the source documents (CG-ALL-7649) | AC1, TC-E4-044-01, -02 |

Each fake answers only what its owner documents; a fake that answers more than the document fails the review. The two operation names that are not published carry the placeholder of GAP-2518 until their owners confirm them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1`; the rwb-case case read and the rwb-decision rule-package read, date-form payments and batch status; one hop, 2 s |
| Kafka | 1 published, 1 consumed | `ProceedsMatched` on `rwb.payment.events.v1`. EV-26 on the shared source-data subscription starts the run. |
| Temporal | 1 workflow, 1 activity | The auction and enforcement matching workflow and its activity on `rwb-payment`. No Schedule. |
| File | None | No file is produced or consumed by this slice |

### 13. Solution plan

| Step | Work | Done when |
|---|---|---|
| 1 | The matching activity: read the receipts of the business date, resolve the case, evaluate the rules, write the row, the record and the outbox row in one transaction | A receipt of source `AUCTION` produces a `proceeds` row with SALE_PROCEEDS and one `ProceedsMatched` |
| 2 | The unmatched path: a receipt with no case reference produces an UNMATCHED row and the daily exception | The daily exception lists the receipt; no case is touched |
| 3 | The two operations on the contract of RWB-P8-E4044-CON: filter, page, match, error map | The documented 400, 401, 403, 404, 409, 422 and 503 answers |
| 4 | The idempotency rule: an `Idempotency-Key` stores the answer; a repeat returns it, a second key answers 409 | A repeated POST returns the stored answer |
| 5 | The outbox relay and the topic declaration | One event per committed row, with the case as the key |
| 6 | SCR-28 through the composite route: loading, matched and unmatched | The three states render from the merged answer |

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data.yaml 5.1.0 with the rwb-payment workload identity | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required element of the match is missing or invalid (422) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A caller without the right (403) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The decision record cannot be written (AC2) |
| MSG-P1-001 | Error | {product} is from {date}. Today's load has not arrived. | The payment data product is stale (VR-P8-004-1) |

The four rows are the legacy message set of the key plus the stale-data row of the module; no other message is added. Every refusal is one problem document with a code, the message ID and a correlation reference, and no message text is assembled in code (BR-P8-004).

### 15. Screens and states

| Screen | State | What it shows |
|---|---|---|
| SCR-28 Proceeds matching | Loading | The receipts of the business date are being read; a skeleton, no partial totals |
| SCR-28 Proceeds matching | Empty | No receipts for the business date |
| SCR-28 Proceeds matching | Error | Not specified in the source documents (CG-ALL-7651) |
| SCR-28 Proceeds matching | No access | A caller without the right of the manual match gets the refusal of TC-E4-044-03 |
| SCR-28 Proceeds matching | Matched | One row per receipt with its case, its source, its amount, `matched_to` and its posting reference when known |
| SCR-28 Proceeds matching | Unmatched | The receipts with `matched_to` UNMATCHED and the daily exception, with the manual match action for right U |

The screen is a gateway-bff composite route: the receipt rows come from this service, the case label from rwb-case, and the two are merged one hop each, in parallel (DP-19). The screen declares no business value of its own; every list it shows is a reference-data list of rwb-case.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-044-01 | AC1 | Component | The receipts of business date `2026-11-22` for case `RC-2026-000611`: one of source `AUCTION` with amount 820,000.00 THB, resolved to the case, matched to SALE_PROCEEDS, with one record and one `ProceedsMatched` |
| TC-E4-044-02 | AC2 | Component | The same receipt; the decision-record stub stops the chain, so no row and no event are written |
| TC-E4-044-03 | Access | Component | A caller without right U on `POST /proceeds/{proceedsId}/match` is refused with MSG-P4-002, and nothing changes |
| TC-E4-044-04 | Principle 5 | Component | A forced decision-record failure stops the action with MSG-P7-003 and raises one incident under R-UNI-39 |
| TC-E4-044-05 | Section 12 (operations, events, activities) | Contract | The operations, events and activities of section 12 match their published contracts: `POST /proceeds/{proceedsId}/match`, `ProceedsMatched` on `rwb.payment.events.v1`, and the matching activity of 12.5 |
| TC-E4-044-06 | Section 12.7 tables | Component | Each table of section 12.7 is created in schema `rwb_payment`, and the run writes no table outside section 12.7 |
| TC-E4-044-07 | AC3 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4044-APP-AC3) |
| TC-E4-044-08 | AC4 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4044-APP-AC4) |
| TC-E4-044-09 | AC5 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4044-APP-AC5) |
| TC-E4-044-10 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4044-APP-AC6) |
| TC-E4-044-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4044-APP-AC7) |
| TC-E4-044-12 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-P8-E4044-APP-AC8) |

The four legacy cases keep their legacy IDs and their legacy intent; TC-E4-044-05 and -06 carry no legacy ID; the data column states the synthetic set of ASM-4167 and no business threshold. A wave 3 harness copy, where one is made, takes the `-ITG` suffix.

### 17. Guardrails

- No business value in code: the tolerance, the window, the grace, the priority and the rule IDs are rule rows read at run time; a constant that changes an answer fails review (BR-P8-004).
- No personal data in an event, a workflow input, a log or a test: `ProceedsMatched` carries `proceedsId`, `caseId` and `amount` only, and every example is synthetic.
- ACE payments and batch status are read through rwb-source-data.yaml 5.1.0 (DP-05). The rwb-payment login has no ACE-view grant.
- No read of another service's table: the case comes from rwb-case's contract, the rules from rwb-decision's, and the schema `rwb_payment` is the only one written.
- The record precedes the change, and both or neither: the activity writes the decision record, the row and the outbox row in one transaction (R-UNI-39).
- One hop, 2 s, breaker per downstream, one retry on a GET, and the manual match idempotent on its key (ADR-020).
- The service holds one base, one topic, one queue and one login: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login.

### 18. Traceability

| Source | Reference | Feature | L3 process | Used in |
|---|---|---|---|---|
| Legacy story | RWB-E4-044, AC1 and AC2, owned word for word by this story | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 7, 16 |
| Feature | FEAT-PAY-04 Match auction and enforcement proceeds, module P8 (E4) | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 1, 2, 18 |
| FSD P8 v3 | A2.4 (intent, steps, VR-P8-004-1, BR-P8-004, roles); AC-P8-004-01; AC-EXC-P8-004-01 and -02; AC-BG-P8-004-01; SCR-28 | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 3, 4, 5, 8, 14, 15 |
| TSD P8 v2 | T2 components; T3.1 `proceeds` DF-FIN-001 to DF-FIN-009; T3.2 `LOV-MATCH` and `LOV-PROCEEDS-SRC`; T6.1 rights; T-A.1 and T-A.2 API-P8-001 and API-P8-002 | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 10, 11, 12, 16 |
| Events | EV-25 `ProceedsMatched` (published), EV-26 `AceDataReady` (consumed) | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 12.3, 12.4 |
| Jobs | Auction and enforcement matching on AceDataReady | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 4, 12.5 |
| Routing logic | R-LIT-65, R-LIT-72, R-UNI-39, R-UNI-48 (Business Rules and Routing Logic v4) | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 8, 9 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules §R5.5) | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 13 |
| Gaps and assumptions | GAP-2517, -2, -3, -4, -5; ASM-4167, -2, -3, -4, -5 | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | 3, 4, 5, 7, 11, 12 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | FEAT-PAY-04 | Not specified in the source documents (DOR-RWB-P8-E4044-APP-2) | all |

### 19. Out of scope

- The published shapes of the two operations, the `proceeds` element list, the three event schemas of the service, the consumed rows, the error set and the fakes: RWB-P8-E4044-CON.
- The payment-to-plan matching, the missed-payment event and the exception list of a receipt on no open case: RWB-P8-E2008-APP and RWB-P8-E2027.
- The settlement payment of RWB-E4-043, the rental auto-debit of RWB-E4-048, the fees of FEAT-PAY-05, the ALS booking of FEAT-PAY-06, the general-ledger posting of FEAT-PAY-07 and the daily money reconciliation of FEAT-PAY-11: the other stories of this service.
- The case of record, its route states, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3).
- The asset, its listing and its sale: rwb-asset (S5). The lot, the buyer and the award: rwb-debtsale (S6). The write-off decision: rwb-writeoff (S7). The treatment and its terms: rwb-treatment (S2).
- The ACE payment, account and batch facts, and the freshness of the data product: rwb-source-data (P1).
- The match package, its rule rows, its version and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the layout of SCR-28 and its field list: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

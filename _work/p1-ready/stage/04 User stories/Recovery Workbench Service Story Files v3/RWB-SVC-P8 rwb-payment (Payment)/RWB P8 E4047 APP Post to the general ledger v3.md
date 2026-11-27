# RWB-P8-E4047-APP Post to the general ledger

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Consume AceDataReady through the shared source-data listener and start `confirmBookings` by signal-with-start.
- `AceDataReady` (EV-26): record key `{sourceSystem}:{businessDate}` and the four-field payload (RD-P1-003).
- Start rule: `confirmBookings` starts only on the event with `sourceSystem` `ALS` and `status` `COMPLETED` (RD-P1-003, RD-P1-040).


| Item | Value |
|---|---|
| Story key | RWB-P8-E4047-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-047 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P8-J |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P8-E4047-APP-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-P8-E4047-APP-23); the story builds against the /v1 path of API-P8-001 on /api/recovery/payment/v1 |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (35 resolved, 18 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **Credit Administration officer**, I want **the Workbench to post the accounting entries for settlements, sales and write-offs to the ledger**, so that **every payment and booking is matched to its case** — in the target, as a posting step of `rwb-payment` that turns the money this service has matched into one posting item on the ledger interface, writes the decision record that names the rule and its version, and records the posting reference the ledger returns on the receipt it came from.

This is the application slice of legacy RWB-E4-047 (FEAT-PAY-07 Post to the general ledger, module P8 Payments and posting, priority Must, depends on FEAT-PAY-06). It owns:

- the legacy acceptance criterion AC2 of the key, copied word for word with its origin tag; AC1 of the key is owned by RWB-ITG-E4047-ITG and is not restated here (section 7);
- the posting step of the service (`postProceeds`), an activity on task queue `rwb-payment` in namespace `rwb-recovery`, called by the settlement and sale flows of this service once a `proceeds` row is matched: it assembles the posting facts of the receipt, sends them as one posting item through the outbound interface of rwb-integration, and answers with the item reference (FSD P8 A2.7; ITG story section 12.5);
- the confirmation run (`confirmBookings`), started by the shared listener on AceDataReady for ALS/COMPLETED: it reads the posting reference the ledger returned for each posted receipt, on rwb-source-data's contract, and writes it to `proceeds.posting_ref` of DF-FIN-009 (DP-05; TSD P8 T5.1 INT-16 and INT-03);
- the local decision record of every posting step and of every confirmation, written through RWB-PLT-E1027-CON in the same transaction as the change, with the rule ID and version in force, and MSG-P7-003 when it cannot be written (DP-03; R-UNI-39; legacy AC2);
- the posting state behind `GET /proceeds` (API-P8-001) on base `/api/recovery/payment/v1`, and SCR-29 Posting with its confirmation from the next ACE batch, reached through the gateway-bff composite route (DP-19; FSD P8 Screens).

It does not own: the published shapes of the operations, the `proceeds` baseline, the event schemas, the error set and the fakes, which are RWB-P8-E4043-CON; the ledger interface itself — its identifier, transport, file layout, result codes, retry schedule and exception queue — which are rwb-integration's (P2) interface configuration and its `deliverFile` activity contract; the settlement amount, terms and due date, which are rwb-treatment's (S2); the sale, its award and the write-off decision, which are rwb-asset (S5), rwb-debtsale (S6), rwb-guarantee (S3), rwb-litigation (S4) and rwb-writeoff (S7); the write-off posting and its `posted_date`, which are S7's on R-WO-21 to R-WO-23, and the debt-sale posting run, which is S6's on R-DS-31 to R-DS-33; the case state, its tasks and its timers, which are rwb-case's (P3); the rule packages and the central ledger, which are rwb-decision's (P7); the ACE payment, batch and write-off facts, which are rwb-source-data's (P1); the rights and scopes, which are rwb-access's (P4); the ledger's own accounting rules and chart of accounts; the cross-service journey of the key, which is RWB-ITG-E4047-ITG; and the deployment of this build, which is the operations story of the key.

### 2. Business rationale

A settlement that clears but is never posted leaves the loan open in the books after the customer has paid, a sale whose proceeds are never posted leaves the recovery out of the ledger, and a write-off that is approved but not posted leaves the provision standing. The legacy module did the posting in process, against the `recovery` schema, with no observable seam between the money match and the ledger. The business objective is unchanged: post the accounting entries for settlements, sales and write-offs to the ledger and write the result to the decision log with the rule version (FSD P8 A2.7.1; FEAT-PAY-07; legacy RWB-E4-047).

What D-RCV-60 changes is where each half of that sentence lives. The receipt, its match, its posting state and its posting reference are this service's: `proceeds` is P8's table in `rwb_payment` (TSD P8 T3.1, DF-FIN-001 to DF-FIN-009; context pack ownership row). The exit to the ledger is not this service's: nothing in the Workbench writes to the ledger directly, and every outbound item leaves through rwb-integration's interface, is logged, retried on a schedule held as data and placed in an exception queue after the retry limit (REQ-DRI-006, REQ-DRI-007). The ledger books the entries by its own accounting rules; this service posts the facts of the receipt and keeps the reference the ledger returns.

The split therefore makes the posting provable in two places instead of one. On this side, one `proceeds` row carries `posting_ref`, so a receipt with no reference is visibly unposted and a receipt with one is visibly posted, without reading another service's table. On the other side, rwb-integration holds the item and its delivery, and rwb-decision holds the record that names the rule and the version that produced the posting. AC2 is the rule that keeps the two consistent: the record is written in the transaction that changes the row, so a posting that cannot be recorded changes nothing and leaves no item behind (DP-03; R-UNI-39; ADR-022).

No business value is invented. The chart of accounts, the entry set of each route, the ledger interface values and the posting window are named by no source in the read set: they stay unstated, with the placeholder and the recorded gaps and assumptions, and every list value, field type, message and state is the value the FSD, the TSD, the routing logic and the legacy story already carry (ASM-4213, -2, -3, -5).

### 3. Preconditions

- RWB-P8-E4043-CON is published: base `/api/recovery/payment/v1`, `GET /proceeds` with `ProceedsPage`, `POST /proceeds/{proceedsId}/match` with `MatchRequest` and `Proceeds`, the `proceeds` baseline with DF-FIN-001 to DF-FIN-009, the `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` schemas, the error set and the fakes. This story builds behind that contract and adds no shape of its own.
- RWB-PLT-E1027-CON is published: the decision-record writer declared to run in the caller's transaction, failing with MSG-P7-003, and the `decision_record` template applied in `rwb_payment` (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-29 Posting from the proceeds read, one hop, read only (DP-19).
- `proceeds` exists in schema `rwb_payment` from the DB story of the service, with `posting_ref` DF-FIN-009 (varchar(40), optional) and the seven standard record columns of TSD P8 T3.0; this story adds no table, no column and no migration.
- The outbound interface of rwb-integration is callable as a task on queue `rwb-integration` from this service's identity, and its identifier, transport, layout, result codes and retry values are rows of the integration's interface configuration read at run time — all Not specified in the source documents (GAP-2557; ASM-4217).
- rwb-source-data answers the posting reference of a receipt and the batch status of its source, one hop with a 2 s timeout, because this service holds no `v_ace_*` grant and reads no ACE table (DP-05; TSD P8 T5.1 INT-02, INT-03, INT-16).
- rwb-decision answers the rule row in force for the posting of a route — its ID and version — so the record names a rule and not a constant; the rule set of the posting of a settlement or a sale route is Not specified in the source documents (GAP-2553; ASM-4213).
- The capability area Write-off and posting and its rights R and U exist as access rows of rwb-access, and the posting run itself is unattended under the service identity (FSD P8 A2.7.3.3; TSD P8 T6.1).
- The receipts this story posts are already matched: the settlement arm of RWB-P8-E4043-APP and RWB-P8-E4044-APP, the sale arm of RWB-P8-E4044-APP and the balance application of RWB-P8-E4049-APP write the row; this story reads it and never writes `matched_to`.
- No approval is needed to build against a Draft contract baseline, and a story with only platform CON build dependencies is Day 1 by rule (Template and Rules R5.7; ASM-4221).

### 4. Flow

1. A receipt of this service reaches a matched state: the settlement payment on R-SET-14 or its final installment on R-SET-18, or the sale proceeds on R-DIS-54. The `proceeds` row and its match commit first, and the posting step is called with the proceeds reference in the same run (FSD P8 A2.7; ITG story section 12.5).
2. `PostingEntryBuilder` reads the `proceeds` row of `rwb_payment` — case, treatment, receipt, source, amount, value date, `matched_to` — and the rule row of the route in force at the business date, on rwb-decision's contract, for the rule ID and version the record must name.
3. It builds the posting facts of the receipt: the case and proceeds references, the value date, the amount, the match value, the route that produced it and the posting type that the match value maps to. The posting type mapping and the accounting entry set are held as data with the interface configuration and with the ledger; neither is a constant of this service (GAP-2553; ASM-4213).
4. `PostingSender` calls the outbound interface of rwb-integration as a task with a manifest — interface reference, business date, case, proceeds, amount, value date, the posting facts block and an `Idempotency-Key` — and receives the item reference. The interface identifier, the transport, the layout and the result codes are that service's configuration, read per item (GAP-2557).
5. In one `rwb_payment` transaction the step writes the local decision record — rule ID, version, inputs, answer, hash-linked to the previous record of the case, with the item reference in its outcome — and the posting key of the receipt; the row changes no column until the reference arrives. A failure of the record leaves nothing and no posting is kept (DP-03; R-UNI-39; AC2).
6. The item is delivered to the ledger by rwb-integration on the retry schedule of its interface row; a delivery failure stays on that service's exception queue with its own message and task, and the receipt stays without a posting reference.
7. The shared source-data listener starts `confirmBookings` on AceDataReady for ALS/COMPLETED. INT-16 still supplies the GL monthly file to ACE.
8. `confirmBookings` reads the posting references for the event business date from the rwb-source-data posting-reference contract fake (§12.8).
9. In one transaction the confirmation writes `posting_ref` on the row and its own decision record with the rule version in force; a receipt the ledger has not confirmed keeps `posting_ref` empty and is shown as unposted.
10. SCR-29 Posting shows approved bookings and postings with the confirmation from the next ACE batch, and SCR-28 Proceeds matching shows each receipt with its match value and its posting reference; both are composed by gateway-bff from this service and the case header of rwb-case, one hop each (DP-19; FSD P8 Screens).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision record cannot be written | The transaction rolls back: the posting state does not move, no item reference is kept and no posting leaves; an incident is raised | MSG-P7-003 | AC2, TC-E4-047-02, TC-E4-047-04 |
| X2 | The rule row of the route is not readable, or no version is in force | The step stops before building anything; nothing is sent and nothing changes | MSG-P7-003 | AC3, TC-E4-047-05 |
| X3 | The outbound interface refuses the manifest or no interface row is in force at the business date | No item is created; the receipt stays unposted; the refusal is returned to the run | MSG-GEN-001 | AC4, TC-E4-047-06 |
| X4 | The interface row has been changed since the last item | The next item obeys the new version: transport, layout, result codes and retry are read per item, so a change is data and needs no release | None | AC5, TC-E4-047-07 |
| X5 | The item is delivered but the ledger rejects the posting | The item is held on rwb-integration's exception queue with its task; the receipt keeps no posting reference and shows as unposted; a corrected cause is re-sent from that queue | MSG-P2-001 (P2's row) | AC6, TC-E4-047-08 |
| X6 | The ACE batch of the source has not arrived, or the product is stale | The confirmation run does not read a reference and the receipts stay unposted; the product shows its date | MSG-P1-001 | AC7, TC-E4-047-09 |
| X7 | The same proceeds is posted twice with the same `Idempotency-Key` | One item, one record and one reference; the repeat returns the stored answer and is counted | None | AC8, TC-E4-047-10 |
| X8 | The same proceeds is posted with a new key after a confirmation | The second posting is refused with 409: one receipt carries one posting reference, and an overwrite would break the record chain | None | AC9, TC-E4-047-11 |
| X9 | A caller without the right tries the read, or a case outside its scope | Refused, nothing changes; the read answers 404 for an object outside scope | MSG-P4-002 | AC10, TC-E4-047-03, TC-E4-047-20 |
| X10 | rwb-source-data, rwb-decision or the interface does not answer inside 2 s | The step of that receipt stops and retries; the breaker opens per downstream; no partial posting is kept | HTTP 503 | AC11, TC-E4-047-12 |

X5 is the only row this story does not carry itself: the rejection, its retry and its exception queue are rwb-integration's interface row and its message, and the route's own `POSTING_REJECTED` state on R-DS-32 and R-WO-22 belongs to rwb-debtsale and rwb-writeoff (GAP-2559; ASM-4219).

### 6. INVEST check

| Letter | Verdict |
|---|---|
| Independent | Yes. It builds against two platform contracts and one service's outbound interface, and every other fact arrives on a published contract and its fake. |
| Negotiable | The entry set, the posting type mapping, the interface values and the window stay with the ledger, Finance and rwb-integration; the story fixes only the step, the record and the reference. |
| Valuable | Yes. A receipt that is matched but not posted is visible as such, and the ledger contact is provable from the record and the item. |
| Estimable | Yes. Two activities, one row update, one consumed read and one screen state set. |
| Small | Yes. One builder, one sender, one confirmation reader and one record writer on top of an existing table. |
| Testable | Yes. AC2, the four documented refusals and the confirmation on the next ACE batch are each one automated case. |

### 7. Acceptance criteria

```gherkin
Feature: Post to the general ledger

  Scenario: AC2 Not recorded (legacy RWB-E4-047 AC2)
    Given the rwb-integration contract mock returns the posting item of the matched receipt and its acknowledgement
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Rule row not readable or no version in force (exception X2) (new, D-RCV-60)
    Given the rule row of the route is not readable or no version is in force
    When the posting step is taken
    Then the step stops before building anything, nothing is sent and nothing changes

  Scenario: AC4 Interface refuses the manifest or no interface row is in force (exception X3) (new, D-RCV-60)
    Given the outbound interface refuses the manifest or no interface row is in force at the business date
    When the posting step is taken
    Then no item is created, the receipt stays unposted and the refusal is returned to the run

  Scenario: AC5 Interface row changed since the last item (exception X4) (new, D-RCV-60)
    Given the interface row has been changed since the last item
    When the next item is posted
    Then the item obeys the new version: transport, layout, result codes and retry are read per item

  Scenario: AC6 Ledger rejects a delivered item (exception X5) (new, D-RCV-60)
    Given the item is delivered and the ledger rejects the posting
    When the rejection is received
    Then the item is held on the exception queue of rwb-integration and the receipt keeps no posting reference and shows as unposted

  Scenario: AC7 Stale or absent ACE batch (exception X6, BR6) (new, D-RCV-60)
    Given the ACE batch of the source has not arrived or the product is stale
    When the confirmation run reads the reference
    Then no reference is read, the receipts stay unposted and the product shows its date

  Scenario: AC8 Same proceeds posted twice with the same key (exception X7, BR9) (new, D-RCV-60)
    Given the same proceeds is posted twice with the same Idempotency-Key
    When the repeat arrives
    Then one item, one record and one reference exist, and the repeat returns the stored answer and is counted

  Scenario: AC9 Same proceeds posted with a new key after a confirmation (exception X8) (new, D-RCV-60)
    Given a receipt already carries a posting reference
    When the same proceeds is posted with a new key
    Then the second posting is refused with 409 and no overwrite is made

  Scenario: AC10 Caller without the right or case outside scope (exception X9) (new, D-RCV-60)
    Given a caller without the right or a case outside its scope
    When the caller tries the read
    Then the request is refused, nothing changes and the read answers 404 for an object outside scope

  Scenario: AC11 Downstream does not answer inside 2 s (exception X10) (new, D-RCV-60)
    Given rwb-source-data, rwb-decision or the interface does not answer inside 2 s
    When the step of a receipt runs
    Then the step stops and retries, the breaker opens per downstream and no partial posting is kept

  Scenario: AC12 Every posting leaves as an outbound item (BR1) (new, D-RCV-60)
    Given a posting is requested
    When the sender runs
    Then the posting leaves as an outbound item on the interface of rwb-integration and nothing is written to the ledger directly

  Scenario: AC13 Settlement and sale proceeds are posted (BR2) (new, D-RCV-60)
    Given a settlement payment clears the settlement amount, or sale proceeds are applied to the case and the loan account
    When the posting step runs
    Then the payment is posted once, the final installment is posted the same way, and the sale proceeds is posted once

  Scenario: AC14 Posting reference on one receipt (BR3) (new, D-RCV-60)
    Given a receipt has an item reference from the ledger
    When the confirmation runs
    Then the reference is recorded on that one proceeds row and an unposted receipt carries none

  Scenario: AC15 Parameters read from configuration (BR5) (new, D-RCV-60)
    Given the posting type mapping, the entry set, the interface values and the retry schedule are held as data
    When the step runs
    Then no such value is written in code and each is read from the interface configuration or the ledger

  Scenario: AC16 ACE facts read on contract (BR7) (new, D-RCV-60)
    Given the payment, batch and write-off facts are held by rwb-source-data
    When the service reads them
    Then the read is made on rwb-source-data's contract and the service holds no v_ace grant and no ACE table

  Scenario: AC17 Owned state is not written (BR8) (new, D-RCV-60)
    Given the case, route state, tasks, timers, central ledger and rights are held by other services
    When the posting step runs
    Then none of them is written by this story

  Scenario: AC18 Attestation rate (BR10) (new, D-RCV-60)
    Given receipts were matched on a business date
    When the rate of receipts matched the same day is read
    Then it is read from the decision records and the Workbench records, and no target value is set in this story

  Scenario: AC19 Error answers 401 or 403 on a provided operation (new, D-RCV-60)
    Given a request to a provided operation carries no valid credential or a valid credential without the right
    When the request is made
    Then the response answers 401 when the credential is missing or rejected and 403 when the right is missing, and nothing changes

  Scenario: AC20 Consumed event redelivered (BR9) (new, D-RCV-60)
    Given a consumed event is delivered a second time
    When the repeat arrives
    Then the event is processed once, no second item or reference is created and the repeat is counted

  Scenario: AC21 Activity retried or timed out (BR5, exception X10) (new, D-RCV-60)
    Given an activity is retried or does not finish inside its timeout
    When the retry or the timeout occurs
    Then the retry follows the retry schedule of the interface configuration and no partial posting is kept

  Scenario: AC22 Consumed call fails or does not answer (exception X10) (new, D-RCV-60)
    Given a consumed call fails or does not answer
    When the step of a receipt runs
    Then the step stops and retries and no partial posting is kept

  Scenario: AC23 Status change the model does not allow (new, D-RCV-60)
    Given a status change the model does not allow is requested
    When the change is requested
    Then the change is refused and nothing changes
```

The criterion is the legacy criterion of RWB-E4-047, word for word, with its origin tag added and nothing else changed: the legacy wording of "the decision log cannot be written", "the action is taken" and "nothing changes" all stand. The single leading `Given` is the only addition, and it names the cross-service part the criterion leaves open — the posting item of rwb-integration, which is the only other service the action touches. AC1 of the key belongs to RWB-ITG-E4047-ITG by the split the plan fixes and is asserted there as the cross-service journey; this story supplies the posting step that journey drives, and its component proof is TC-E4-047-01 in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The Workbench writes nothing to the ledger directly: every posting leaves as an outbound item on the interface of rwb-integration, which logs it, retries it on the schedule of the interface row and places it in an exception queue after the retry limit | REQ-DRI-006; REQ-DRI-007 |
| BR2 | A settlement payment is posted when it clears the settlement amount, and the final installment is posted the same way; sale proceeds are posted once they are applied to the case and the loan account | R-SET-14; R-SET-18; R-DIS-54 |
| BR3 | The posting reference is recorded against the receipt it belongs to, one reference per `proceeds` row, and an unposted receipt carries none | R-WO-21 (the same rule on the write-off side); DF-FIN-009; Legacy AC1 |
| BR4 | The posting step and the confirmation each write one decision record with the rule ID and version in force, in the same transaction as the change; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; R-UNI-39; Legacy AC2 |
| BR5 | No value a business person may change is written in code: the posting type mapping, the entry set, the interface values and the retry schedule are data of the interface configuration and of the ledger | BR-P8-007 (FSD P8 A2.7.3.1) |
| BR6 | The date the confirmation reads is the batch date of the source, and a stale or absent batch produces no reference rather than a guess | VR-P8-007-1 (FSD P8 A2.7.3.1); FSD P8 A1.4 |
| BR7 | The ACE payment, batch and write-off facts stay with rwb-source-data and are read on its contract; this service holds no `v_ace_*` grant and no ACE table | DP-05; TSD P8 T5.1 |
| BR8 | The case, its route state, its tasks and its timers stay with rwb-case, the rule packages and the central ledger with rwb-decision, and the rights with rwb-access; this story writes none of them | Ownership Map (recovery_case P3, rule_row P7); TSD P8 T6.1 |
| BR9 | The same receipt, the same business date or the same key twice produces one item, one record and one reference, and the repeat is counted | R-UNI-40; ITG story X7 |
| BR10 | The posting is attested by the rate of receipts matched the same day, read from the decision records and the Workbench records; no target value is set in this story | FSD P8 A2.7.1 metric |

BR1 runs in the sender, BR2 in the builder, BR3 and BR6 in the confirmation, BR4 in the writer that commits with the change, BR7 and BR8 at the boundary, and BR9 in the inbox and the idempotency table.

Criterion coverage: BR1 AC12; BR2 AC13; BR3 AC14 and AC7; BR4 AC2; BR5 AC15; BR6 AC7; BR7 AC16; BR8 AC17; BR9 AC8; BR10 AC18.

### 9. State transitions

The posting state of a receipt, not the case state:

| From | Trigger | To | Rule |
|---|---|---|---|
| No posting | The receipt is matched and the step runs with a record written | Posting requested: the item reference is kept in the record, `posting_ref` still empty | R-SET-14, R-SET-18, R-DIS-54 |
| Awaiting reference | The ledger returns the reference in the next ACE batch | `posting_ref` written; one confirmation record | BR3, BR6 |
| Awaiting reference | The ledger rejects, or the batch has not arrived | No column changes; the item is on the interface's exception queue, or the confirmation waits | X5, X6 |
| No posting | The decision record cannot be written | No change: no item, no reference, no record | BR4; AC2 |
| Posted | The same proceeds is posted again | No change; one reference per receipt stands | BR9, X8 |

The case states `PAYMENT_CLEARED`, `PROCEEDS_APPLIED`, `GL_POSTED` and `POSTED` are moved by rwb-case, rwb-treatment, rwb-debtsale and rwb-writeoff under their own rules; this service writes the receipt's posting reference and announces nothing (TSD P8 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-payment service identity, login on schema `rwb_payment` (DP-02) | Runs the posting step and the confirmation under the service identity; the run is unattended and holds the primary use of the feature (FSD P8 A2.7.3.3) |
| Write-off and posting, right R (TSD P8 T6.1) | Reads the receipts with their posting state on `GET /proceeds`: RW-FRAUD, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-CONDUCT, RW-PRODHEAD, RW-WOCOMM, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT |
| Case record, right R (legacy Permission checks) | Reads the posting state of the cases in scope: RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and 34 more |
| Credit Administration officer (FSD P8 A2.7.3.3) | Works the posting on SCR-29 with the confirmation from the next ACE batch |
| rwb-access (P4) | Owns the rights, the roles and the scope data; this story calls no guard of its own and holds no role row |
| rwb-integration (P2) | Owns the interface, the delivery, the retry and the exception queue of the posting item |

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
| DF-FIN-007 | proceeds | received_date | Read |
| DF-FIN-008 | proceeds | matched_to (LOV-MATCH: SETTLEMENT, SALE_PROCEEDS and the other values of the list) | Read |
| DF-FIN-009 | proceeds | posting_ref (varchar(40), optional) | Write on confirmation |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, DP-03) | the record of the step and of the confirmation: case, decision code, rule ID, rule version, inputs, answer, decided at, actor | Write |
| processed_event, idempotency_key | objects of the service template | the batch-date guard and the posting key | Write |
| DF-ACE-043 to DF-ACE-054 | not held | the payment record and its `payment_code` | Read on rwb-source-data's contract |
| DF-REF-001 to DF-REF-015 | not held | the rule row of the route, its ID and its version | Read on rwb-decision's contract |
| DF-CAS-001 to DF-CAS-023 | not held | the case reference and its label for the screen | Read on rwb-case's contract |

Field IDs are those of TSD P8 T3.1 and the Logical Data Model v8. `proceeds` is the only business table this story writes, and it writes one optional column of it; no column, key, join or view leaves `rwb_payment` (DP-01). The receipt facts of `recovery_case`, `treatment`, `interaction` and `decision_log_entry` that the legacy data table names are the owners' and are read on their contracts or not at all: `treatment` and `interaction` are not needed by this step and are named here only to close the legacy table.

Lists read: LOV-PROCEEDS-SRC (DF-FIN-005) and LOV-MATCH (DF-FIN-008). Parameters read: the interface row values of rwb-integration (transport, layout, result codes and retry schedule), read per item (X4; BR5). Reference-data contract: DP-06 and DP-07.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/payment/v1` (the per-service base of Template and Rules §R4), shapes and error set RWB-P8-E4043-CON's.

| Method | Path | Purpose | Authorization |
|---|---|---|---|
| GET | `/proceeds` | The receipts of a case or a date range with their match value and their posting reference: query `matched`, `from`, `to`, `page`, `size`; `ProceedsPage` out (API-P8-001) | Write-off and posting, right R, scope applied |

`POST /proceeds/{proceedsId}/match` (API-P8-002) is the match operation of the sibling stories of this service; this story changes neither its shape nor its behaviour, and it publishes no operation for the posting itself because the step is unattended. The payments read that RWB-ITG-E4047-ITG section 12.2 names is not in the ownership rows of P8 and not in TSD P8 T-A.1 (GAP-2558; ASM-4218). Errors: 400 and 401 carry the message ID Not specified in the source documents (CG-ALL-7705); 403 with MSG-P4-002; 404 for an object outside scope carries the message ID Not specified in the source documents (CG-ALL-7705); 422 with MSG-GEN-001; 503 when the record library does not answer in time carries the message ID Not specified in the source documents (CG-ALL-7705); 503 when a consumed answer does not answer in time carries the message ID Not specified in the source documents (CG-ALL-7705).

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| The posting-reference read (operation name Not specified in the source documents (GAP-2555; ASM-4215)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The posting reference of a receipt and the batch status of its source; faked |
| The rule-in-force read (operation name Not specified in the source documents (GAP-2553; ASM-4213)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule row of the route with its ID and version, which the record names; faked |

Each row is one hop with a 2 s timeout, one retry on a GET and a breaker per downstream (ADR-020). Both are class C in fact while the plan's contract row is None, so both are built against the owners' published documents and fakes from Day 1 (GAP-2560; ASM-4220). The case label of the screen arrives through the composite route and is not a call of this story.

#### 12.3 Events published

None. The three events of the service — `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) — sit on `rwb.payment.events.v1` and are published by the sibling stories; the catalogue holds no posting-result event, so the confirmed reference is announced on the row and the read and on nothing else (GAP-2556; ASM-4216). The local decision record is published on the shared `rwb.decision-record.v1` by the library of RWB-PLT-E1027-CON, not by this story.

#### 12.4 Events consumed

| Event | Read or topic | Owner | Payload used | When |
|---|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` (EV-26) | `rwb.source-data.events.v1`, group `rwb-payment.rwb.source-data.events.v1` | rwb-source-data | `sourceSystem`, `businessDate`, `status`, `completedAt` (the event is keyed `{sourceSystem}:{businessDate}`) | Starts the `confirmBookings` run of a business date only on `sourceSystem` `ALS` and `status` `COMPLETED` |

The rwb-payment source-data listener consumes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` in group `rwb-payment.rwb.source-data.events.v1`. On ALS/COMPLETED it uses signal-with-start on the separate `confirmBookings` workflow ID for the event business date. It dedupes by event ID in the shared inbox, with an idempotent source/date guard in the workflow. AceDataLate is a lateness signal and starts no daily run.

#### 12.5 Workflows and activities

| Name | Type | Queue | Contract element |
|---|---|---|---|
| `postProceeds` | Activity, called by the settlement and sale flows of this service | `rwb-payment` in namespace `rwb-recovery` | In: the proceeds reference and the business date. Out: the item reference and the record id |
| `confirmBookings` | Event-started workflow | `rwb-payment` | In: source, business date and event ID. Out: confirmations written and receipts still unposted. |
| The outbound call of the item (name Not specified in the source documents (GAP-2557; ASM-4217)) | Activity provided by rwb-integration, called as a task | `rwb-integration` | In: the manifest of section 4 step 4. Out: the item reference |

The shared listener starts `confirmBookings` on its own stable workflow ID per business date. Retry: 1 s initial interval, back-off 2, 10 attempts. A rule missing from the version in force is non-retryable.

#### 12.6 Schedules

No Schedule is created. The shared source-data listener starts `confirmBookings` on AceDataReady for ALS/COMPLETED.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `proceeds` | P8, schema `rwb_payment` | The receipt, its match value and `posting_ref` DF-FIN-009; created by the DB story of the service |
| `decision_record` | Platform library, created in `rwb_payment` | The local record of the step and of the confirmation (DP-03) |
| `processed_event` | Platform library, created in `rwb_payment` | The batch-date and event-id guard |
| `idempotency_key` | Platform library, created in `rwb_payment` | One key per receipt and business date |

`outbox_event` is not written by this story, which publishes no event. `recovery_case` and `task` are P3's, `treatment` is S2's, `rule_row` and the ledger are P7's, `write_off` is S7's, `interface_config` and `outbound_item` are P2's, and the ACE views are P1's; none is read as a table here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-integration outbound-interface fake (RWB-P2-E1007-CON) | One item accepted with a reference; one manifest refused; one item delivered but rejected by the ledger | TC-E4-047-06 (X3), TC-E4-047-07 (X4), TC-E4-047-08 (X5), TC-E4-047-10 (X7) |
| rwb-source-data posting-reference fake | The reference of receipt `PAY-90001` in the batch of `2026-12-15`; no reference for `PAY-90002`; a batch that is not complete | AC7, TC-E4-047-09 |
| rwb-decision rule-in-force fake | R-SET-14 at a pinned version; a route with no rule in force | AC3, TC-E4-047-05 |
| Decision-record library stub (RWB-PLT-E1027-CON) | A healthy chain and a stopped chain with MSG-P7-003 | AC2, TC-E4-047-02, TC-E4-047-04 |
| gateway-bff composite route fake | The merged SCR-29 answer: postings with and without a reference | TC-E4-047-01 |
| Authorise stub of the service template | Right R held and not held | TC-E4-047-03 |

Each fake answers only what its owner documents; the two operation names that are not published carry the placeholder of their gap until the owners confirm them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | `GET /proceeds` on `/api/recovery/payment/v1`; the rwb-source-data reference read and the rwb-decision rule read, one hop, 2 s |
| Kafka | None published by this story, 1 consumed | EV-26 is consumed through the P1 AsyncAPI and the shared rwb-payment source-data group. The platform inbox library dedupes the delivery. |
| Temporal | 1 activity and 1 workflow | `postProceeds` (activity) and `confirmBookings` (event-started workflow) on `rwb-payment`, plus the outbound activity of rwb-integration on `rwb-integration` |
| File | None built by this story | The ledger and ALS interface is a file run of rwb-integration's interface row; this story delivers a manifest |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `posting`.

| Component | Type | Responsibility |
|---|---|---|
| PostingEntryBuilder | Service | Reads the matched `proceeds` row and the rule row in force, and builds the posting facts and the posting type of the receipt from data |
| PostingSender | Service | Calls the outbound interface of rwb-integration as a task with the manifest and the `Idempotency-Key`, and keeps the item reference |
| PostingRecordWriter | Service | The one transaction: the local decision record, the posting state and the item reference, or nothing |
| PostingReferenceReader | Service | Reads the reference of a posted receipt on the rwb-source-data contract for a business date |
| BookingConfirmationStep | Service | Writes `posting_ref` and the confirmation record per receipt, once per batch date |
| ProceedsResource | Controller | `GET /proceeds` with its right, its scope and its error map; it implements nothing of the match |

**Database and migrations.** Writes two columns' worth of state on `proceeds` — no new table and no new column: `posting_ref` DF-FIN-009 already exists in the baseline of RWB-P8-E4043-CON, the migration belongs to the DB story of the service, and this story adds an index-free read on `(matched_to, received_date)`. No Flyway file is written here.

**Configuration.** No business value: the posting type mapping, the entry set, the interface identifier, the transport, the layout, the result codes and the retry schedule are data of the interface configuration and of the ledger, and the rule ID and version are read in force (BR5). Two settings only, the page size of the read and the retry count of the confirmation run, neither fixed by a source in the read set (GAP-2554; ASM-4214).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract only; this service holds no `v_ace_*` grant | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as the owner's contract: the reference and the batch status of DF-ACE-043 to DF-ACE-054 are read on rwb-source-data's operations, and this service holds no `v_ace_*` grant. DP-03 fixes the record written in the transaction of the change. DP-19 is behind SCR-28 and SCR-29. The two H rows of the table are the ones the metadata carries. No DP row of this key adds a contract dependency, and the two consumed reads are class C in fact (GAP-2560; ASM-4220).

**Build steps.** (1) The builder and the rule read against the fakes, X2. (2) The sender with the manifest, the key and the item reference, X3, X4, X7. (3) The writer with the record and the posting state in one transaction, AC2, X1. (4) The reference reader and the confirmation step on a batch date, X5, X6. (5) `GET /proceeds` with the right, the scope and the error map, X9. (6) The absence assertions: no `v_ace_*` grant, no direct ledger write, no cross-schema key, no Schedule, no outbox row.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P8-E4043-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON stay green, and a SIT week shows a settlement receipt posted once with its reference written after the next batch, an unconfirmed receipt staying without a reference, a repeated posting writing nothing, and a stopped record leaving the row, the item and the reference untouched with MSG-P7-003.

### 14. Validation and messages

| ID | Type | Message | When |
|---|---|---|---|
| MSG-GEN-001 | Error | Enter {field}. | A required posting fact is missing or the manifest is refused (422, X3) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | A caller without the right (403, X9) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The rule is not in force or the record cannot be written (AC2, X1, X2) |
| MSG-P1-001 | Error | {product} is from {date}. Today's ACE batch has not arrived. | The batch of the source is late or failed (VR-P8-007-1, X6) |
| MSG-P2-001 | Error | Not specified in the source documents (GAP-2557; ASM-4217) | The ledger rejects the posting and the item shows on the exception queue of rwb-integration (X5) |

The four rows of the legacy message set are MSG-GEN-001, MSG-P4-002, MSG-P7-003 and, on the FSD side, the stale-product row VR-P8-007-1; MSG-P2-001 is rwb-integration's and appears here only because a rejected posting is read from that service's queue. No message text is assembled in code, and every refusal is one problem document with a code, the message ID and a correlation reference.

### 15. Screens and states

| Screen | State | What it shows |
|---|---|---|
| SCR-29 Posting | Loading | The postings of the period are being read; a skeleton, no partial totals |
| SCR-29 Posting | Posted | One row per receipt with its case, its amount, its value date, its match value, its posting reference and the rule ID and version of the record |
| SCR-29 Posting | Awaiting confirmation | The receipts whose item left and whose reference has not come back from the next ACE batch |
| SCR-29 Posting | Unposted | The receipts with no item or a rejected item, with the exception reference of rwb-integration |
| SCR-29 Posting | Empty | Not specified in the source documents (CG-ALL-7716) |
| SCR-29 Posting | Error | Not specified in the source documents (CG-ALL-7716) |
| SCR-29 Posting | No access | Not specified in the source documents (CG-ALL-7716) |
| SCR-28 Proceeds matching | Loading; matched; unmatched | The legacy screen and its three states, each row carrying the posting reference where one exists |
| SCR-28 Proceeds matching | Empty | Not specified in the source documents (CG-ALL-7715) |
| SCR-28 Proceeds matching | Error | Not specified in the source documents (CG-ALL-7715) |
| SCR-28 Proceeds matching | No access | Not specified in the source documents (CG-ALL-7715) |

Both screens are gateway-bff composite routes: the receipts and their posting state come from this service, the case label from rwb-case, and the two are merged one hop each, in parallel (DP-19). SCR-29 is the posting screen the FSD places first in E4, and SCR-28 is the legacy screen of the key; neither declares a business value of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-047-01 | AC1 as the component check of the posting step: the posting facts of a matched receipt become one item, one record with the rule ID and version, and the reference of the next batch is written; AC1 itself is owned by RWB-ITG-E4047-ITG; run by RWB-ITG-E4047-ITG | Component | The matched settlement receipt `PAY-90001` of case `RC-2026-000555` for 12,500.00 THB dated `2026-12-14`, with the ALS batch of `2026-12-15`; the sale proceeds of the same case |
| TC-E4-047-02 | AC2: the record cannot be written, so nothing changes and the caller sees MSG-P7-003 | Component | The record library stub stops the chain; no item, no reference, no row state |
| TC-E4-047-03 | Access: a role without the right is refused with MSG-P4-002, and a case outside scope answers 404 | Component | A caller without Write-off and posting R on `GET /proceeds` |
| TC-E4-047-20 | AC10 (exception X9): a caller without the right is refused with MSG-P4-002 and a case outside scope answers 404, each checked as its own case | Component | Not specified in the source documents (NEWAC-RWB-P8-E4047-APP-AC10) |
| TC-E4-047-05 | AC3 as the component check of X2: an unreadable rule row or no version in force stops the step before any item is built | Component | The rwb-decision rule-in-force fake with a route that has no rule in force |
| TC-E4-047-06 | AC4 as the component check of X3: a refused manifest or no interface row in force creates no item and returns the refusal | Component | The rwb-integration outbound-interface fake with one manifest refused |
| TC-E4-047-07 | AC5 as the component check of X4: the next item uses a changed interface row | Component | The rwb-integration outbound-interface fake with a changed interface row |
| TC-E4-047-08 | AC6 as the component check of X5: a rejected item is held on the exception queue and the receipt stays unposted | Component | The rwb-integration outbound-interface fake with one item delivered but rejected by the ledger |
| TC-E4-047-09 | AC7 as the component check of X6 and BR6: a stale or absent batch produces no reference | Component | The rwb-source-data posting-reference fake with a batch that is not complete |
| TC-E4-047-10 | AC8 as the component check of X7 and BR9: the same key twice gives one item, one record and one reference | Component | Receipt `PAY-90001` posted twice with the same `Idempotency-Key` |
| TC-E4-047-11 | AC9 as the component check of X8: a second posting with a new key after confirmation is refused with 409 | Component | Receipt `PAY-90001` with a confirmed posting reference posted with a new key |
| TC-E4-047-12 | AC11 as the component check of X10: a downstream that does not answer inside 2 s leaves no partial posting | Component | A rwb-decision fake that does not answer inside 2 s |
| TC-E4-047-13 | AC12 as the component check of BR1: every posting leaves as an outbound item on rwb-integration | Component | The rwb-integration outbound-interface fake |
| TC-E4-047-14 | AC13 as the component check of BR2: settlement and sale proceeds are posted once each | Component | The settlement receipt `PAY-90001` for 12,500.00 THB and the sale proceeds of case `RC-2026-000555` |
| TC-E4-047-15 | AC14 as the component check of BR3: the reference is on one receipt and an unposted receipt carries none | Component | `PAY-90001` with a reference and `PAY-90002` with none |
| TC-E4-047-16 | AC15 as the component check of BR5: parameters are read from configuration, not code | Component | The interface configuration with a changed retry schedule |
| TC-E4-047-17 | AC16 as the component check of BR7: no v_ace grant and ACE facts read on contract | Component | The grant check of the service role on the ACE schema |
| TC-E4-047-18 | AC17 as the component check of BR8: owned state is not written | Component | The rwb-case, rwb-decision and rwb-access fakes |
| TC-E4-047-19 | AC18 as the component check of BR10: the attestation rate is read from the records | Component | The decision records and Workbench records of the same business date |
| TC-E4-047-04 | Principle 5: a forced decision-log write failure stops the action with MSG-P7-003 and raises one incident under R-UNI-39 | NFR | The record store stopped during the posting of a business date; the run is repeated after recovery |
| TC-E4-047-26 | Contract: the operations, events and activities of section 12 answer on their contract fakes, with the shapes and error set of section 12.1 | Contract | The fakes of section 12.8 for the operations, events and activities of section 12 |
| TC-E4-047-27 | Boundary: each table of section 12.7 accepts and refuses its values at the limits of ASM-3438 | Component | Values at the limits of the tables of section 12.7; Not specified in the source documents (ASM-3438) for the limit values |
| TC-E4-047-21 | AC19: a request without a valid credential answers 401 and one without the right answers 403 on the provided operations | Component | Not specified in the source documents (NEWAC-RWB-P8-E4047-APP-AC13) |
| TC-E4-047-22 | AC20: a redelivered consumed event is processed once and the repeat is counted | Component | Not specified in the source documents (NEWAC-RWB-P8-E4047-APP-AC14) |
| TC-E4-047-23 | AC21: a retried or timed-out activity follows the retry schedule and leaves no partial posting | Component | Not specified in the source documents (NEWAC-RWB-P8-E4047-APP-AC15) |
| TC-E4-047-24 | AC22: a consumed call that fails or does not answer stops the step and leaves no partial posting | Component | Not specified in the source documents (NEWAC-RWB-P8-E4047-APP-AC16) |
| TC-E4-047-25 | AC23: a status change the model does not allow is refused and nothing changes | Component | Not specified in the source documents (NEWAC-RWB-P8-E4047-APP-AC17) |

Every legacy test case of RWB-E4-047 appears once with its legacy ID and its legacy intent, and the Level column is the target level: the posting step is proved at component level here, the whole journey is proved in the integration harness. The `-ITG` copies of the four cases belong to RWB-ITG-E4047-ITG and are not restated. The receipt, case and amount values are the synthetic examples of FSD P8 A2.1, and no business threshold appears in the data column.

### 17. Guardrails

- No business value in code: the posting type mapping, the entry set, the chart-of-accounts reference, the interface values and the retry schedule are data; the rule ID and version are read in force and named on the record (BR5).
- No personal data in an event, a workflow input, a log or a test: an item and a record carry case, proceeds and receipt references, an amount, a date and a rule identity only, never a name, an address, a contact value or an identity number. Every example is synthetic.
- ACE data only through the owner's contract: the posting reference and the batch status come from rwb-source-data, and this service holds no `v_ace_*` grant and copies no ACE row (DP-05).
- No direct ledger write and no direct core-bank write: every posting leaves as an item on rwb-integration's interface, logged, retried and queued (BR1).
- No read of another service's table: the rule comes from rwb-decision's contract, the case label through the composite route, and `rwb_payment` is the only schema written (DP-01).
- The record precedes the change and both or neither: the step writes the decision record with the item reference in one transaction, and the row's `posting_ref` only with its own confirmation record (BR4; R-UNI-39).
- One hop, 2 s, a breaker per downstream, one retry on a GET, and one posting per receipt and business date (ADR-020).
- The service holds one base, one topic, one queue and one login: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login; this story adds no topic name, no event name and no Schedule.

### 18. Traceability

| Source | Reference | Feature | L3 process | Used in |
|---|---|---|---|---|
| Legacy story | RWB-E4-047, AC2 owned word for word by this story; AC1 owned by RWB-ITG-E4047-ITG | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 1, 7, 16 |
| Feature | FEAT-PAY-07 Post to the general ledger, module P8 (E4); priority Must; depends on FEAT-PAY-06 | FEAT-PAY-07 | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 1, 2, 18 |
| FSD P8 v3 | A2.7 (intent, steps, VR-P8-007-1, BR-P8-007, roles, metric); AC-P8-007-01; AC-EXC-P8-007-01 and -02; AC-BG-P8-007-01; SCR-28 and SCR-29 | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 2, 3, 4, 8, 14, 15 |
| TSD P8 v2 | T2 components; T3.0 standard columns and T3.1 `proceeds` DF-FIN-001 to DF-FIN-009; T5.1 INT-02, INT-03 and INT-16; T6.1 rights; T-A.1 API-P8-001 | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 10, 11, 12 |
| Routing logic v4 | R-SET-14, R-SET-18, R-DIS-54, R-DS-31, R-WO-21, R-WO-22, R-WO-23, R-UNI-39, R-UNI-40 | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 8, 9, 19 |
| Jobs and events | Payment posting confirmation; JOB-08 is owned by rwb-integration; EV-26 `AceDataReady`; EV-11, EV-12, EV-25 (sibling stories) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 4, 12.3, 12.4 |
| Patterns | DP-03, DP-05, DP-19 (Template and Rules §R5.5) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 13 |
| Split and journey | RWB-ITG-E4047-ITG sections 1, 4, 12.5, 16 and 19; RWB-P8-E4043-APP, RWB-P8-E4044-APP, RWB-P8-E4049-APP | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 1, 7, 16, 19 |
| Gaps and assumptions | GAP-2553 to -8; ASM-4213 to -9 | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | 2, 3, 4, 5, 7, 12, 13 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | Not specified in the source documents (DOR-RWB-P8-E4047-APP-2) | all |

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E4-047, disposition Split (rework) | Metadata; sections 1, 19 |
| Legacy AC2 | Section 7, word for word with its origin tag; TC-E4-047-02 |
| Legacy AC1 (the entries reach the ledger, the record holds the rule version) | Section 1, 4 and 8 here; the criterion itself in RWB-ITG-E4047-ITG |
| Data entities recovery_case, v_ace_payment, treatment, interaction, decision_log_entry, rule_row | Section 11, each with its owner |
| Endpoints "None; a service or a scheduled job" | Sections 4, 12.1, 12.5, 12.6 |
| SCR-28 Proceeds matching and its three states | Section 15; SCR-29 Posting added from FSD P8 |
| Permission right R and the unattended primary role | Sections 10, 12.1, 16 |
| Messages MSG-GEN-001, MSG-P4-002, MSG-P7-003 | Section 14, exception paths |
| Legacy test cases TC-E4-047-01 to -04 | Section 16 |
| Wave 3 harness and general ledger values (GAP-0436; GAP-0433) | Not specified in the source documents (GAP-0436; GAP-0433); no value is set in this story |

### 19. Out of scope

- The settlement amount, the terms and the due date the posting refers to: rwb-treatment (S2, FEAT-PAY-03).
- The write-off posting and its `posted_date` on R-WO-21 to R-WO-23, and the debt-sale derecognition and posting run on R-DS-31 to R-DS-33: rwb-writeoff (S7) and rwb-debtsale (S6), each through the same interface of rwb-integration.
- The ledger interface itself: its identifier, transport, file layout, result codes, retry schedule, exception queue and resend are rwb-integration's (P2) interface configuration and `deliverFile` activity contract.
- The ledger's own accounting rules, chart of accounts and entry set: the ledger and Finance.
- The matching of the receipt, the settlement arm, the sale-proceeds arm and the balance application: RWB-P8-E4043-APP, RWB-P8-E4044-APP and RWB-P8-E4049-APP.
- The published shapes, the `proceeds` baseline, the event schemas, the error set and the fakes: RWB-P8-E4043-CON.
- The case, its route state, its tasks and its timers: rwb-case (P3).
- The rule packages, the rule rows, their version and the central ledger: rwb-decision (P7).
- The ACE payment, batch and write-off facts and the freshness of the data product: rwb-source-data (P1).
- The rights, the scopes and the masking behind the read: rwb-access (P4) and the guard of the service template.
- The composite route and the field lists of SCR-28 and SCR-29: RWB-PLT-N001-CON and the edge stories.
- The daily money reconciliation of FEAT-PAY-11 and the provision inputs of FEAT-PAY-08: the other stories of this service.
- The cross-service journey of the legacy key and its evidence: RWB-ITG-E4047-ITG.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

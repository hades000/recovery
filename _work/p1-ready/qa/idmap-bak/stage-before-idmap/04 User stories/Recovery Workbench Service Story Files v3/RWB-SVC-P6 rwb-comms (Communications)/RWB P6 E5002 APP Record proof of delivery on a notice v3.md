# RWB-P6-E5002-APP Record proof of delivery on a notice

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E5002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-AA |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-S4-E5002-CON; RWB-P1-E1066-CON (the case-scoped ledger append of rwb-source-data.yaml 5.1.0); the rwb-case case read `GET /cases/{caseId}` (case number) |
| Contract version | Not specified in the source documents (DOR-RWB-P6-E5002-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-007, RD-P1-009, RD-P1-041, RD-P1-064 |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- This story consumes no rwb-source-data operation: the `v_ace_pod` data row and the barcode wording that said otherwise are corrected (finding #1).
- RD-P1-007 and RD-P1-041: the date-wide proof-of-delivery read writes nothing and belongs to the automatic loop; delivery ledger entries of that loop are appended by rwb-comms over REST. A hand-recorded proof also appends one `LETTER` entry, through rwb-comms only (RD-P1-064 rule 5; NEW-GAP-F06-1 and NEW-GAP-F16-4 closed) (findings #2, #3).
- RD-P1-009: the `DecisionRecorded` attributes for the ledger intake stated; AC13 added (finding #4).
- RD-P1-001 and RD-P1-004: missing or reused `Idempotency-Key` and the problem body, in step with RWB-ITG-E5002-ITG; AC12 added (finding #5).
- Finishing pass: a hand-recorded proof appends one `LETTER` ledger entry; AC13, X12, section 12 and the fakes restated (RD-P1-064 rules 5 and 13; request F06-affected-0014); test case IDs of Test Cases v9 applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E5-002 for the rwb-comms slice of the proof of delivery, which records the returned delivery fact on the notice row and hands it to rwb-litigation on the published contract RWB-S4-E5002-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E5002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 21 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the proof of delivery that comes back from the post recorded on the notice that rwb-comms holds, with the delivery result and the delivered or callback date written once on the notice row, the notice state moved to Delivered or Unserved, and the same fact handed to rwb-litigation on the published contract RWB-S4-E5002-CON so that the case moves and the notice period starts there**, so that **the notice shows how and when it was served instead of the post room being chased by phone, and the case of record, its route state and its notice-period timer stay with the services that own them**.

### 2. Business rationale

A statutory notice only starts its clock when it has been served, and a period counted from the print date can be challenged in court. The legacy story wrote the delivery confirmation onto the case, started the notice period from the delivered date (R-LIT-07) and marked the notice unserved when the proof window expired (R-LIT-08). Both moves are case moves: the case state, its route state and the notice-period clock are the case of record's. The delivery fact itself, however, is not a case fact: it belongs to the notice, and the notice belongs to communications, which owns the notice, the template, the merge fields and the proof of delivery (Architecture v5 slide 41 and slide 17, `notice` in `ownership.json`). This story is that half of the legacy step: the litigation officer records the returned proof on the notice, rwb-comms writes `notice.callback_date` (DF-LEG-021) and `notice.delivery_status` (DF-LEG-022) in schema `rwb_comms`, the notice moves on its own lifecycle to Delivered or Unserved, and the same fact leaves the service once, on the published S4 contract, for rwb-litigation to evaluate R-LIT-07, R-LIT-08 or R-LIT-09 and for rwb-case to start the notice period behind its own timer.

Three facts are no longer this service's to reach, and the story is built so that it cannot reach them. The case route state, the notice-period timer and the task of the notice period are rwb-case's (P3), and the notice-period duration, its reference row and the raise of the breach are the case record's as well. The evaluation of the delivery rules, the proof-window expiry and the queue transfer of an unserved notice are rwb-litigation's (S4), reached only on the contract `RWB-S4-E5002-CON` that this story builds against and never as a table. And the ACE proof-of-delivery rows are read by rwb-source-data, not here: the automatic `v_ace_pod` loop that fills the notice from the WIN file is the dispatch story of Epic 2 (RWB-P6-E2021-APP) and the capture design of Epic 1 (RWB-P6-E1055-APP), and DP-05 applies to this story only as a prohibition (GAP-1194; ASM-2141). The proof this story records is the one the officer supplies or the one the S4 answer carries back; no ACE view and no ACE table is read by any component of it.

This document is the rwb-comms slice of legacy RWB-E5-002. It owns no legacy criterion: AC1 to AC4 of the story master are the S4 slice's (`RWB-S4-E5002-APP`, which keeps the case transitions and the legacy lines word for word) and the cross-service journey is the integration slice's (`RWB-ITG-E5002-ITG`). The other slices of the same key are the contract `RWB-S4-E5002-CON` and the case slice `RWB-P3-E5002-APP`, which applies the delivery answer to the case, its timer and its decision record. What this story owns is the notice deliverable of the title: the proof on the notice, its two columns, its state, the hand-off and the screen read. Its criteria are therefore new under D-RCV-60 and test only that deliverable.

The legacy in-process write is retired rather than restated: no component of this story writes `recovery_case`, `timer`, `task` or `decision_log_entry`, and the old monolith API base is not served by any path of this service (DP-13). The decision that a delivered or undeliverable letter produced is recorded, before the notice changes, through the local decision-record library with the rule and its version in force (DP-03, TSD P6 T2 "writes the decision log entry before any change"), which is what legacy AC1 asked for and what legacy AC4 tested (GAP-1190; ASM-2137). The screens are read through the gateway-bff composite route (DP-19), and no screen calls an owner service directly.

It serves REQ-OCC-003 ("letters are dispatched for print and post, and proof of delivery returns to the case"), it carries the control CTL-15 by putting the delivered date on the notice and on the hand-off, and it holds the FSD P6 measure "notices with proof of delivery, 100 percent".

### 3. Preconditions

- RWB-S4-E5002-CON is published: the proof-record operation on `/api/recovery/litigation/v1`, its request and answer shape (the notice reference, the case reference, the delivery status, the delivered date, the rule ID and the package version of the S4 evaluation), its error envelope and its contract fake. The operation's own name is Not specified in the source documents (GAP-1189; ASM-2136); this story builds against the contract and its fake on Day 1 and never against a notice or case table.
- The `notice` table and its columns exist from RWB-P6-E1052-APP, including `callback_date` (DF-LEG-021), `delivery_status` (DF-LEG-022) and the lifecycle `state` column of the TSD P6 T3.0 standard columns; no new table and no new column is created by this story.
- The notice to be served exists in state Sent with its `sent_date` (DF-LEG-019) and `barcode` (DF-LEG-020), which are the WIN acknowledgment fields of RWB-P6-E1055-APP.
- The local decision-record library and the shared record format of DP-03 are live: RWB-PLT-E1027-CON. It is not in this story's build list, which is empty, so the story builds against its fake until the platform contract story publishes (GAP-1190; ASM-2137).
- The mapping of a LOV-DELIVERY value onto the notice state, and the version of that mapping row in force, are reference data owned by the business and read with their version, so no list value and no state name is written in code. The list itself is LOV-DELIVERY of the TSD P6 T3.2 (`DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING`); its meaning for `REFUSED` and `PENDING`, and the contract the list is read on, are Not specified in the source documents (GAP-1192; ASM-2139).
- The gateway-bff composite route (RWB-PLT-N001-CON) serves SCR-18 Notice approval and SCR-19 Litigation workspace; it is not in this story's build list either (GAP-1190; ASM-2137).
- The caller holds a Workbench role with the Litigation right of the notice (TSD P6 T6.1: RW-LITOFF holds Litigation CRUA). The guard library of DP-08 is not in this story's pattern set: the declared right on the two operations is enforced at the edge for the screen path, and the right on the new write path is this story's design (GAP-1195; ASM-2142).
- The service runs as its own login on schema `rwb_comms` (the DP-01 and DP-13 rules of the story set); it holds no grant on another `rwb_*` schema and no `v_ace_*` grant (GAP-1194; ASM-2141).

### 4. Flow

1. The litigation officer opens SCR-18 Notice approval for a notice of the case, through the gateway-bff composite route (DP-19), and the notice section answers from `GET /notices/{noticeId}` on base `/api/recovery/comms/v1` (API-P6-002): state, `notice_type`, `sent_date`, `barcode`, `callback_date` and `delivery_status`.
2. The officer records the returned proof with the delivery result, the delivered or callback date, and the barcode or reference the letter carries, on `POST /notices/{noticeId}/proof-of-delivery`.
3. `ProofOfDeliveryValidator` checks that the notice exists in the caller's scope and is in state Sent with a `sent_date`, that the delivery status is a value of LOV-DELIVERY, that a callback date is present when the status is one that carries a date, and that a barcode supplied with the proof is the barcode of the notice. A failed check answers 422 or 404 and nothing is read further.
4. `DeliveryOutcomeMapper` resolves the notice state from the delivery status through the mapping row in force (Delivered for a delivered proof, Unserved for a refused or undeliverable one); the row and its version are reference data, never code.
5. `ProofDecisionRecordWriter` writes one decision record through the local decision-record library, before any notice change: the outcome, the delivery status, the callback date, the notice reference, the case reference and the rule ID the outcome belongs to (R-LIT-07 for a served notice, R-LIT-08 for an unserved one) with the version in force. A failed write stops the request with nothing changed (DP-03; legacy AC1 and AC4).
6. `NoticeDeliveryWriter` writes, in one `rwb_comms` transaction, `callback_date` (DF-LEG-021), `delivery_status` (DF-LEG-022) and the notice `state`, plus the idempotency row of the request. No other owner's row is written. Before that transaction commits, rwb-comms reads the case number with `GET /cases/{caseId}` of rwb-case (one hop) and appends one ledger entry on `POST /api/recovery/source-data/v1/cases/{caseId}/interactions`: `eventCode` `LETTER`, `actorType` `USER`, `actorRef` the user ID, `deliveryStatus` as recorded, `externalRef` the barcode of the notice, `idempotencyKey` `LETTER-<caseNo>-<yyyyMMdd>-<id of the rwb-comms record of the hand entry>`, with a uuid `Idempotency-Key`. On 503 MSG-P1-022 nothing is committed, or the call is retried with the same header key and business key (RD-P1-064 rules 5 and 13).
7. `S4DeliveryClient` calls the proof-record operation of `RWB-S4-E5002-CON` with the notice reference, the case reference (DF-LEG-016), the delivery status, the callback date, the barcode where the contract asks for it and the rule ID it recorded; one hop, a 2 s timeout and a breaker per downstream. The operation name is Not specified in the source documents (GAP-1189; ASM-2136).
8. rwb-litigation evaluates R-LIT-07, R-LIT-08 or R-LIT-09 on that fact, moves the case route state and answers; rwb-case starts or does not start the notice period behind its own durable timer. This service starts, stops and writes no timer and no case row, and it never evaluates a delivery rule itself.
9. The answer of the write operation returns the notice it wrote: state, delivery status, callback date and barcode, with the outcome of the hand-off.
10. A repeated request with the same notice, delivery status and callback date, or with the same Idempotency-Key, writes nothing on the notice and sends no second hand-off; the repeat is counted under R-UNI-40. Where the earlier hand-off did not complete, the repeat re-runs the hand-off only.
11. SCR-18 and SCR-19 read the notice state, the delivery status and the callback date from this service through the composite route, read only, next to the pack states of rwb-litigation and the case and timer of rwb-case.
12. SCR-18 and SCR-19 show empty, loading, error and no-access states; their behaviour is Not specified in the source documents (CG-ALL-6804; CG-ALL-6805); a caller without the Litigation right keeps the refusal MSG-P4-002 and no notice facts shown.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no delivery status, or no callback date on a status that carries one | The answer is 422 and nothing is read beyond the validator; no decision record and no notice change | MSG-GEN-001 | AC4 |
| X2 | The notice ID names no notice, or a notice outside the caller's scope | The answer is 404 and nothing is written; the caller cannot tell an out-of-scope notice from a missing one | None | AC4 |
| X3 | The notice is not in state Sent, or carries no `sent_date` | The answer is 409 and nothing changes; the proof of an undispatched notice is not recorded | None | AC4 |
| X4 | A barcode supplied with the proof is not the barcode of the notice | The answer is 409 and nothing changes; the mismatch is shown to the litigation officer team with the two barcodes | None | AC4 |
| X5 | A role without the Litigation right records or reads the proof | Refused before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC7 |
| X6 | The local decision-record write fails | The transaction writes nothing: the notice keeps its state, its empty `delivery_status` and its empty `callback_date`, and no call leaves the service | MSG-P7-003 | AC6 |
| X7 | The same proof arrives twice for the same notice, or the same Idempotency-Key is replayed | One write and one hand-off; the repeat is counted under R-UNI-40 and no second decision record is written | None | AC5 |
| X8 | The S4 contract does not answer inside 2 s, or its breaker is open | The notice keeps the proof it recorded, because that fact is true and this service's own; the hand-off is re-run when the request is repeated under the same key, and the caller sees status 503 with the platform error envelope; no message of this key's set applies to a downstream that did not answer (GAP-1189; ASM-2136) | None | AC3 |
| X9 | The S4 answer refuses the delivery fact (the case is not in the state the rule expects) | The notice keeps what it wrote, the refusal is recorded for the S4 owner and the caller reads the answer of the S4 contract unchanged; this service does not move the case itself and raises no message of its own set | None | AC3 |
| X10 | A component, a statement or a test reaches an ACE view, an ACE table or another `rwb_*` schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC9 |
| X11 | The proof record carries no `Idempotency-Key`, or a key already used with another body | 400 for the missing key, 409 for the reused key; no decision record, no notice change and no hand-off | MSG-PLT-N009-03; MSG-PLT-N009-05 | AC12 |
| X12 | The ledger append of the hand-recorded proof answers 503, or the case read fails | Nothing is committed: no notice change and no hand-off; the call may be retried with the same header key and business key | MSG-P1-022; MSG-GEN-006 | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-S4-E5002-CON` and its fake; the decision-record library and the composite route are fakes until their platform stories publish (GAP-1190; ASM-2137) |
| Negotiable | The mapping of a delivery status to the notice state, the lists and the delivered-notice states are reference data with a version; the story fixes the behaviour, not the values |
| Valuable | The notice shows how and when it arrived, the officer stops chasing the post room, and the case and its timer move in the service that owns them |
| Estimable | Two operations, one validator, one mapper, one repository write, one library adapter, one client and one read-only screen fragment |
| Small | Fits two weeks with its tests, as the secondary slice of the legacy key |
| Testable | Each of the eight criteria of section 7 is one automated test; the cross-service answer is stubbed in the S4 contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Record proof of delivery on a notice, in rwb-comms

  Background:
    Given notice "N-0101" for case "RC-2026-000321" is in state "Sent" with barcode "RR223344556TH" and sent date 2026-12-15
    Given the LOV-DELIVERY values are read with their version in force and the mapping row of the delivery status to the notice state is in force
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 A delivered proof moves the notice to Delivered (new, D-RCV-60)
    Given the rwb-litigation contract mock accepts the delivery answer for notice "N-0101"
    When "LIT-0101" records the proof of delivery for notice "N-0101" with delivery status "DELIVERED" and callback date 2026-12-18
    Then the notice has state "Delivered", delivery status "DELIVERED" and callback date 2026-12-18
    Then the delivery status and the callback date are written once, in the same transaction as the notice state
    Then the operation answers with the notice it wrote, and no other column of the notice changes

  Scenario: AC2 A refused or undeliverable proof leaves the notice Unserved (new, D-RCV-60)
    Given the rwb-litigation contract mock accepts the delivery answer for notice "N-0101"
    When "LIT-0101" records the proof of delivery for notice "N-0101" with delivery status "UNDELIVERABLE" and callback date 2026-12-21
    Then the notice has state "Unserved" and delivery status "UNDELIVERABLE" with callback date 2026-12-21
    Then this service starts no notice-period timer and writes no case row
    Then the notice still carries its barcode "RR223344556TH" and its sent date 2026-12-15

  Scenario: AC3 The delivery fact leaves the service once, on the S4 contract (new, D-RCV-60)
    Given the rwb-litigation contract mock returns the delivery answer applied for notice "N-0101" with rule "R-LIT-07"
    When the proof of delivery is recorded on notice "N-0101" with delivery status "DELIVERED" and callback date 2026-12-18
    Then one call leaves the service to the proof-record operation of RWB-S4-E5002-CON
    Then the call carries the notice reference "N-0101", the case reference "RC-2026-000321", the delivery status and the callback date, and no other fact
    Then rwb-comms writes no recovery_case row, no timer row, no task row and no proof document row
    Then the rule the outcome belongs to and its version are the ones the decision record carries and the S4 answer accepts

  Scenario: AC4 No proof, an unknown notice or a dispatched-only notice is refused (new, D-RCV-60)
    Given "LIT-0101" holds RW-LITOFF and notice "N-0101" is in scope
    When "LIT-0101" records a proof on notice "N-0101" with no delivery status
    Then the answer is status 422 with MSG-GEN-001 naming "delivery status"
    Then no decision record is written and the notice keeps state "Sent" with no callback date
    When "LIT-0101" records a proof for notice "N-9999", which does not exist
    Then the answer is status 404 and nothing is written
    When "LIT-0101" records a proof on notice "N-0102", which is in state "Generated" with no sent date
    Then the answer is status 409 and nothing is written

  Scenario: AC5 The same proof twice writes once (new, D-RCV-60)
    Given notice "N-0101" is "Delivered" with delivery status "DELIVERED" and callback date 2026-12-18
    When the same proof is recorded again for notice "N-0101" with delivery status "DELIVERED" and callback date 2026-12-18
    Then the notice is unchanged and no second decision record is written
    Then no second call leaves the service to RWB-S4-E5002-CON
    Then the repeat is counted under rule R-UNI-40

  Scenario: AC6 The decision record is written before the notice changes (new, D-RCV-60)
    Given the local decision-record library answers and the mapping row of the delivery status is in force at its version
    When "LIT-0101" records the proof on notice "N-0101" with delivery status "DELIVERED" and callback date 2026-12-18
    Then one decision record names rule "R-LIT-07", the version in force, the notice reference and the case reference
    Then the decision record is written before the notice row changes
    Given the local decision-record library is unavailable
    When "LIT-0101" records the same proof
    Then the notice keeps state "Sent" with no delivery status and no callback date
    Then no call leaves the service to RWB-S4-E5002-CON
    Then the user sees MSG-P7-003

  Scenario: AC7 A caller without the Litigation right is refused (new, D-RCV-60)
    Given "U-5002" holds RW-PHONECOL, which carries no Litigation right in the TSD P6 T6.1 matrix
    When "U-5002" records the proof on notice "N-0101"
    Then the call is refused with status 403 and MSG-P4-002
    Then no decision record is written and the notice is unchanged
    When "U-5002" reads the same notice
    Then the read is refused with status 403 and MSG-P4-002

  Scenario: AC8 The notice facts show on the two screens (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-18 Notice approval and SCR-19 Litigation workspace for case "RC-2026-000321"
    Given notice "N-0101" is "Delivered" with delivery status "DELIVERED" and callback date 2026-12-18
    When "LIT-0101" opens SCR-18 and SCR-19
    Then SCR-18 shows the notice state "delivered", the delivery status "DELIVERED", the callback date 2026-12-18 and the barcode "RR223344556TH"
    Then SCR-19 shows the same notice facts read from this service and the pack states from rwb-litigation
    Then both screens call one composite route and no owner service directly

  Scenario: AC9 A statement that reaches an ACE view or another owner's schema is refused (new, D-RCV-60)
    Given the boundary test runs over the components of this story
    When a component, a statement or a test reaches an ACE view, an ACE table or another `rwb_*` schema, or writes to rwb_case, rwb_litigation or rwb_decision
    Then the grant refuses the statement and the boundary test fails the build
    Then nothing is released

  Scenario: AC10 Each rule BR1 to BR10 of section 8 is proved by a criterion or a boundary test (new, D-RCV-60)
    Given the rules BR1 to BR10 of section 8 are the rules of this story
    When the traceability check runs over section 8 and the criteria of section 7
    Then each rule BR1 to BR10 is covered by at least one criterion or test case of this story
    Then BR6 and BR10 are proved by the boundary test and the contract test, not by a business flow

  Scenario: AC11 A request without an authenticated caller is refused with status 401 on both operations (new, D-RCV-60)
    Given no authenticated caller is presented with the request
    When a request reaches GET /notices/{noticeId} or POST /notices/{noticeId}/proof-of-delivery
    Then the answer is status 401 with the platform error envelope
    Then nothing is read or written and no message of this key's set applies

  Scenario: AC12 A proof record with no Idempotency-Key, or a key reused with another body, changes nothing (new, D-RCV-60)
    Given notice "N-0101" is in state "Sent"
    When the officer posts a "DELIVERED" proof with callback date 2026-12-18 and no Idempotency-Key header
    Then the answer is 400 problem+json with messageCode "MSG-PLT-N009-03" and nothing is written
    Given the same proof was then recorded with Idempotency-Key "7b1e4c2a-9d3f-4a68-b0c5-2f8e6d1a9c47"
    When the same key is sent with callback date 2026-12-19
    Then the answer is 409 problem+json with messageCode "MSG-PLT-N009-05"
    Then the notice keeps callback date 2026-12-18 and no second decision record and no second hand-off exist

  Scenario: AC13 A recorded proof appends one ledger entry and its decision carries the intake attributes (new, D-RCV-60; changed, RD-P1-064)
    Given notice "N-0101" of case "RC-2026-000321" is in state "Sent" and all consumed fakes are healthy
    When the officer posts a "DELIVERED" proof with callback date 2026-12-18
    Then rwb-comms reads GET /api/recovery/case/v1/cases/{caseId} once for the case number
    Then one entry is appended on POST /api/recovery/source-data/v1/cases/{caseId}/interactions with eventCode "LETTER", actorType "USER", actorRef the officer's user ID, deliveryStatus "DELIVERED", externalRef "RR223344556TH" and an idempotencyKey starting "LETTER-RC-2026-000321-"
    Then the proof-of-delivery read of rwb-source-data is not called
    When the ledger append answers 503 MSG-P1-022
    Then no notice changes and no hand-off is sent
    Then one decision record is relayed as rwb.decision.DecisionRecorded.v1 with data.entryId, data.caseId and the headers ce_actor and ce_idempotencykey
```

The eleven criteria are new under D-RCV-60 and test only the notice deliverable of this story. They assert nothing that belongs to another slice: the case route state, the notice-period timer and the notice-period task are `RWB-P3-E5002-APP`'s, the evaluation of R-LIT-07, R-LIT-08 and R-LIT-09 and the queue transfer of an unserved notice are `RWB-S4-E5002-APP`'s, and the cross-service journey is `RWB-ITG-E5002-ITG`'s. The four legacy criteria AC1 to AC4 of RWB-E5-002 are owned by the S4 slice and are not restated here; the three documents of this key use the same labels for different criteria, so a criterion is always quoted with its story ID (GAP-1193; ASM-2140).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The proof of delivery is a fact of the notice: the delivery status (DF-LEG-022) and the callback date (DF-LEG-021) are written on `notice` in `rwb_comms`, and the notice moves on its own lifecycle to Delivered or Unserved | TSD P6 T3.1; Architecture v5 slide 41 (P6 owns notices and proof of delivery); legacy RWB-E5-002 AC1 |
| BR2 | A delivered proof moves the notice to Delivered; a refused or undeliverable proof moves it to Unserved. The mapping of a LOV-DELIVERY value to the notice state is a reference row read with its version, never a constant | R-LIT-07, R-LIT-08; FSD P6 A2.2 AC-ALT-P6-002-01 and AC-ALT-P6-002-02; TSD P6 T3.2 (GAP-1192; ASM-2139) |
| BR3 | The case route state, the notice-period timer, the task of the notice period and the proof-window expiry are owned by rwb-case and rwb-litigation; rwb-comms writes no `recovery_case` row, no `timer` row and no `task` row, and it calls the S4 contract once per recorded proof | R-LIT-07, R-LIT-08; `ownership.json` (recovery_case, timer and task own P3); RWB-S4-E5002-CON |
| BR4 | The decision is recorded before the notice changes, with the rule ID the outcome belongs to and the version in force; a failed write changes nothing and the caller sees MSG-P7-003 | TSD P6 T2 ("writes the decision log entry before any change"); DP-03; legacy RWB-E5-002 AC1 and AC4 |
| BR5 | The same proof twice, or the same Idempotency-Key twice, writes once, sends no second hand-off and counts the repeat | R-UNI-40; FSD P6 A2.2 AC-EXC-P6-002-04 (the repeated request answers the first record) |
| BR6 | No ACE view and no ACE table is read or written here: the proof facts are the ones the caller supplies and the ones the S4 answer carries back, and the automatic `v_ace_pod` loop belongs to the Epic 1 and Epic 2 dispatch stories | DP-05; FSD P6 change note v3; Architecture v5 slide 17 (GAP-1194; ASM-2141) |
| BR7 | No person name, address or contact value enters `rwb_comms`, the decision record, a log or an event: the proof carries the notice reference, the case reference, the barcode, two list values and dates | TSD P6 T3.1 (notice carries no addressee); Template and Rules v1 section R7.2 (s17) |
| BR8 | A caller without the Litigation right is refused before any read or write, and nothing changes | TSD P6 T6.1; MSG-P4-002; legacy permission block of RWB-E5-002 |
| BR9 | The notice facts show on SCR-18 and SCR-19 through the gateway-bff composite route only; no screen calls an owner service directly and the screen model belongs to the edge contract | DP-19; legacy screen block of RWB-E5-002 (SCR-18 states "delivered; unserved") |
| BR10 | The service base is `/api/recovery/comms/v1` and the old monolith base is not served; the notice read keeps its legacy operation ID API-P6-002 | DP-13; TSD P6 T-A |
| BR11 (R-LIT-07) | A notice whose proof of delivery is received is served: the proof is attached, the notice shows the delivery, and the notice period starts from `delivered_at` | Business Rules and Routing Logic v4 (R-LIT-07) |
| BR12 (R-LIT-08) | A proof window that expires without proof marks the notice unserved, and the notice period does not start; the notice-period timer itself is not this story's | Business Rules and Routing Logic v4 (R-LIT-08); RWB-P3-E5002-APP |
| BR13 (R-UNI-40) | The same event or the same proof twice produces one effect, and the repeat is counted | Business Rules and Routing Logic v4 (R-UNI-40); legacy TC-E5-002-01 |
| BR14 (CTL-15) | A notice period starts only from the delivery date on the proof of delivery, never from the print date. This story writes the delivered date and hands it over; the timer is S4's and P3's, so the control holds on the fact, not on a clock here | RWB-E1-055 story and Build Notes (CTL-15); R-LIT-07 |

### 9. State transitions

This story moves the notice state, not a case state. The notice moves on the lifecycle `state` column of the TSD P6 T3.0 standard columns, with the states the SCR-18 list names (generated; approved; sent; delivered; unserved):

| From | Event | Condition | To |
|---|---|---|---|
| Sent | A proof with delivery status `DELIVERED` is recorded | The notice has a `sent_date` and the callback date is present | Delivered, with `callback_date` and `delivery_status` written in one transaction |
| Sent | A proof with delivery status `REFUSED` or `UNDELIVERABLE` is recorded | The notice has a `sent_date` | Unserved, with the delivery status the proof carries and the callback date |
| Sent | A proof with delivery status `PENDING` is recorded | The status means the proof is not back yet | Refused: nothing changes and the caller is told the proof is not in (GAP-1192; ASM-2139) |
| Delivered or Unserved | The same proof is recorded again | Same delivery status and same callback date | Unchanged, and the repeat is counted |
| Generated, Approved or Held | A proof is recorded | The notice carries no `sent_date` | Refused with 409, because a notice that was not dispatched cannot be served |

The case route states of the legacy key are **not** this service's: `NOTICE_DISPATCHED` moves to `WITH_CUSTOMER_NOTICE_PERIOD` by R-LIT-07 or to `NOTICE_UNSERVED` by R-LIT-08 and R-LIT-09, in rwb-litigation and rwb-case (`RWB-S4-E5002-APP`, `RWB-P3-E5002-APP`). Neither the case row nor the `NOTICE_PERIOD` timer row nor the durable timer inside the case workflow is read, written or asserted by this story; the hand-off on `RWB-S4-E5002-CON` is the only path by which the fact reaches them (GAP-1189; ASM-2136).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD P6 T6.1 matrix: records the proof on the notice, reads the notice and its delivery facts, and sees a barcode mismatch on the notice it records |
| RW-ENFORCE, enforcement owner | Litigation CRU: records the proof and reads the same facts in scope |
| RW-LEGAL, legal counsel | Litigation RA: reads the notice, its state and the delivery facts; records no proof |
| RW-CASEOWN, case owner | Documents CRU and Litigation R: reads the notice state and the delivery facts on the case record |
| RW-HEADLIT, RW-PRODHEAD | Litigation RA: read only |
| RW-PHONECOL, phone collector | Litigation absent: refused on both operations with MSG-P4-002 |
| rwb-comms service identity | Validates the proof, writes the decision record, writes `callback_date`, `delivery_status` and the notice state, and calls the S4 operation; it holds no grant on another schema and no `v_ace_*` grant |
| rwb-litigation (S4) service identity | Evaluates R-LIT-07, R-LIT-08 and R-LIT-09 on the fact and answers; owns the legal action, the pack and the case move it announces |
| rwb-case (P3) service identity | Owns the case of record, its route state and the notice-period timer; it is not called by this story |

The rights above are the rows of TSD P6 T6.1 and nothing wider. DP-08 is not in this story's pattern set: the declared right on `GET /notices/{noticeId}` is Litigation R (TSD P6 T-A API-P6-002) and is enforced at gateway-bff for the screen path, and the right on the new write path is this story's design, because no source names a proof-record operation at all (GAP-1195; ASM-2142). Both operations pass the rwb-access authorise check before any read or write, and the check enforces the rights above. A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (P6, `rwb_comms`) | id | Read, as the notice reference of the answer and of the hand-off |
| DF-LEG-016 | notice (P6, `rwb_comms`) | case_id | Read, and sent on the hand-off as the case reference |
| DF-LEG-018 | notice (P6, `rwb_comms`) | notice_type | Read, for the context of the screens |
| DF-LEG-019 | notice (P6, `rwb_comms`) | sent_date | Read, as the condition that the notice was dispatched |
| DF-LEG-020 | notice (P6, `rwb_comms`) | barcode | Read, and matched against the barcode the caller supplies with the proof; this story reads no proof from rwb-source-data (GAP-1597) |
| DF-LEG-021 | notice (P6, `rwb_comms`) | callback_date | Write |
| DF-LEG-022 | notice (P6, `rwb_comms`) | delivery_status | Write, against LOV-DELIVERY; PENDING is refused and the notice is left unchanged; REFUSED mapping not specified in the source documents (GAP-1192) |
| Standard column | notice (P6, `rwb_comms`) | state | Write (Delivered or Unserved) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_comms`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the notice changes |
| Not specified in the source documents (GAP-1189; ASM-2136) | the S4 answer | the outcome, the rule ID and the package version of the S4 evaluation | Read from the contract and stored nowhere: the notice keeps only its own columns |
| v_ace_pod (read by rwb-source-data only) | proof of delivery for a business date | ten view fields of `GET /proof-of-delivery?businessDate=` (rwb-source-data.yaml 5.1.0) | Not read by this story: the read belongs to the automatic WIN loop (RWB-P6-E1055-APP), writes nothing, and no grant is held by this service |

Field IDs are those of the TSD P6 Communications v2 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `notice` and its columns arrive with RWB-P6-E1052-APP, this story writes three of them, and `idempotency_key` and `decision_record` are platform library objects created in `rwb_comms` by the library's own migration (DP-03). `recovery_case`, `timer`, `task` (P3), `decision_log_entry` (P7), `template` (P6, read only by the read operation), `document` (P5) and every `v_ace_*` view (P1) are not created, not written and not read as tables: no foreign key leaves the schema and `notice.case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05).

**No personal data.** The row this story writes carries identifiers, a barcode, two list values and two dates. The addressee, the address and the contact value never enter `rwb_comms`: they are held by rwb-source-data and used by the dispatch story's file build, and they are not logged here and not put on any message. The proof of delivery this story records is the returned result and its dates, not the scanned card or the letter image; a scanned proof is rwb-document's document and is not created by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/notices/{noticeId}` | Read a notice with its serving facts: state, `notice_type`, `sent_date`, `barcode`, `callback_date` and `delivery_status` (TSD P6 T-A API-P6-002) | Litigation R, scope applied | Not applicable |
| POST | `/notices/{noticeId}/proof-of-delivery` | Record the returned proof on the notice: the delivery status, the delivered or callback date and the barcode where it is supplied; write the decision record and the two columns, return the served result as NoticeDelivered with delivered_at, and hand the fact to rwb-litigation, which writes the notice state | Litigation C on the notice, enforced at the edge | `Idempotency-Key` header required; a repeated key answers the first result and counts the repeat |

The read keeps the legacy operation ID API-P6-002 and is not redefined here; this story adds the serving fields to its answer. The write path, its request fields and its right are this story's design, because no source names a proof-record operation: the TSD P6 appendix T-A ends at API-P6-011 and none of the eleven operations records a proof (GAP-1195; ASM-2142). Errors: 401 no session (message ID Not specified in the source documents (CG-ALL-6800)); 403 no right (MSG-P4-002); 404 unknown or out-of-scope notice (message ID Not specified in the source documents (CG-ALL-6800)); 409 a notice that was not dispatched, or a barcode that is not the notice's (message ID Not specified in the source documents (CG-ALL-6800)); 422 a missing field (MSG-GEN-001); 400 a missing `Idempotency-Key` (MSG-PLT-N009-03) and 409 a key reused with another body (MSG-PLT-N009-05), as the platform standard of RD-P1-001; every refusal is `application/problem+json` with the code in `messageCode` (RD-P1-004); 503 the decision-record library or the S4 contract unavailable (message ID Not specified in the source documents (CG-ALL-6800)). The answer carries the notice ID, the case ID, the state, the delivery status, the callback date, the barcode and the outcome of the hand-off.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for |
|---|---|---|---|
| The proof-record operation, whose name is Not specified in the source documents (GAP-1189; ASM-2136) | `/api/recovery/litigation/v1` (path fixed by RWB-S4-E5002-CON) | S4 rwb-litigation (RWB-S4-E5002-CON) | Records the delivery fact of the notice reference and lets rwb-litigation evaluate R-LIT-07, R-LIT-08 or R-LIT-09, move the case route state and start or withhold the notice period through rwb-case; one hop with a 2 s timeout and a breaker per downstream (ADR-020); built against the contract and its fake |
| GET `/cases/{caseId}` | `/api/recovery/case/v1` | P3 rwb-case | The case number of the business key of the ledger entry; one hop, 2 s |
| POST `/cases/{caseId}/interactions` | `/api/recovery/source-data/v1` | P1 rwb-source-data (RWB-P1-E1066-CON) | The `LETTER` entry of the hand-recorded proof; uuid `Idempotency-Key`; 201 new, 200 existing business key; 503 MSG-P1-022 |

Three operations are consumed, each one hop with a 2 s timeout, and no call chain is composed: the S4 proof record, the rwb-case case read for the case number and the rwb-source-data ledger append (RD-P1-064 rule 5). This service calls no access, document or decision operation in this story, and it never calls `GET /api/recovery/source-data/v1/proof-of-delivery?businessDate=` (the date-wide read, which writes nothing); the delivery entries of the automatic WIN loop are appended by RWB-P6-E1055-APP and RWB-P6-E2021-APP. DP-11 is **not** in this story's pattern set, although a published interface is consumed, so the one-hop rule is stated here and the missing pattern row is recorded as GAP-1191 with ASM-2138.

#### 12.3 Events published

None. Architecture v5 slide 42 gives rwb-comms exactly three events on `rwb.comms.events.v1`, `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`, and this story publishes none of them: the automatic WIN proof loop that reads the ACE rows and publishes `NoticeDelivered` is `RWB-P6-E2021-APP` and `RWB-P6-E1055-APP`, and the hand-off of this story is the S4 contract call, not an event. DP-09 is not in this story's pattern set, so no outbox row and no Kafka producer is added. The decision record is written through the local decision-record library of DP-03, and the library owns the relaying of its own record; this story declares no topic and no payload of its own. The library record is `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`; it carries `data.entryId`, `data.caseId` (from `notice.case_id`) and the headers `ce_actor` (`USER:<userId>` of the officer) and `ce_idempotencykey` (form `EV-08-<caseNo>-<yyyyMMdd>-<actionId>`, RD-P1-007 rule 4), from which the ledger intake of rwb-source-data writes one `DECISION_TAKEN` entry (RD-P1-009). `<caseNo>` is read from rwb-case `GET /cases/{caseId}`, one hop (RD-P1-064 rule 5; NEW-GAP-F16-4 closed).

#### 12.4 Events consumed

None. The delivery fact arrives on the S4 answer and from the caller's request, so this story subscribes to no topic, holds no consumer and uses no inbox of its own. The notice state changes it reads for context come from its own `notice` row.

#### 12.5 Workflows and activities

None. The proof is recorded in the request: one validator, one mapper, one library write, one row write and one contract call, with no workflow, no activity and no child workflow. `NoticeDispatchWorkflow` belongs to `RWB-P6-E1055-APP` and is untouched by this story, and no durable timer of any kind is created here.

#### 12.6 Schedules

None. Nothing in this story runs on a schedule: the proof arrives when the returned post is recorded or when the S4 answer carries it, and no Job of Architecture v5 slide 44 is owned, moved or registered here. The WIN dispatch Schedule belongs to `RWB-P6-E1055-APP`.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice row and its serving fields `callback_date` (DF-LEG-021), `delivery_status` (DF-LEG-022) and `state` |
| decision_record | PLT library, created in `rwb_comms` | The local hash-linked decision record of the delivery outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_comms` | The key of the write operation and the hand-off outcome it holds |

Not owned and never read as a table: `recovery_case`, `timer`, `task` (P3), `legal_action`, `hearing` (S4), `decision_log_entry` (P7), `document` and `signature_request` (P5), `template` and `merge_field` (P6, read by the read operation only). No `v_ace_*` view and no ACE table is read here: the proof facts come from the caller and from the S4 answer (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-litigation contract fake (RWB-S4-E5002-CON) | The delivery answer applied with rule `R-LIT-07` and the package version for notice `N-0101` and case `RC-2026-000321`; the answer applied with `R-LIT-08` for an unserved notice; a refusal for a case that is not in the state the rule expects; no answer beyond 2 s; an unreadable answer | AC1, AC2, AC3, AC4 |
| Local decision-record library fake (RWB-PLT-E1027-CON) | One record of the delivery outcome with the rule ID and the version in force; a refused write on the failure path | AC5, AC6 |
| LOV-DELIVERY and mapping fake | `DELIVERED`, `REFUSED`, `UNDELIVERABLE` and `PENDING` at their version, with the mapping row of each to the notice state and its version | AC1, AC2, AC4 |
| gateway-bff composite route fake | The merged SCR-18 and SCR-19 answer for case `RC-2026-000321`, with the notice facts of this service read once | AC8 |
| rwb-case case read and rwb-source-data ledger fakes | Case number `RC-2026-000321`; the ledger append answering 201, 200 on a repeated business key and 503 MSG-P1-022 | AC13 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and the baseline is a build failure in the S4 contract.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The notice read and the proof write on `/api/recovery/comms/v1`; the proof-record operation of `RWB-S4-E5002-CON`, the rwb-case case read and the rwb-source-data ledger append; one hop and 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | None | No workflow, no activity, no Schedule and no timer (12.5, 12.6) |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `noticeproof`, Java package `th.co.scb.ace.workbench.recovery.comms.noticeproof`; front end `src/modules/recovery/comms/NoticeProof.tsx`, the fragment SCR-18 and SCR-19 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Prohibition only: this story reads no ACE data; only rwb-source-data reads `v_ace_*` | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: no component of this story reads an ACE view, an ACE table or `account_ext`, and the proof facts are the ones the caller supplies. The FSD P6 change note of v3 and its A2.2 criteria read `v_ace_pod` in process; that read is the automatic WIN loop of `RWB-P6-E2021-APP` and `RWB-P6-E1055-APP`, which is where it is built, and the difference is recorded as GAP-1194 with ASM-2141. DP-13 keeps the read on API-P6-002 and puts the new write on the service base. DP-19 covers the two screens only, and the screen model and the merge order stay with the edge contract.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's `Depends on (build)` list for this story is None. The metadata table keeps the plan's list as it is, the story builds against the two fakes until those platform contract stories publish, and the absence is recorded as GAP-1190 with ASM-2137. DP-11 is absent from the pattern set although one operation is consumed, and that is recorded as GAP-1191 with ASM-2138.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeProofController | Controller | `POST /notices/{noticeId}/proof-of-delivery` and the serving fields of `GET /notices/{noticeId}`, with the problem mapping for 401, 403, 404, 409, 422 and 503 |
| ProofOfDeliveryValidator | Service | The notice exists in scope and is Sent, the status is a list value, the callback date is present where the status carries one, and a supplied barcode is the notice's |
| DeliveryOutcomeMapper | Service | Resolves the notice state from the delivery status through the mapping row in force; holds no value itself |
| ProofDecisionRecordWriter | Library adapter | Writes the decision record with the rule ID and the version in force before any change, hash-linked, and refuses the request when the write fails (DP-03) |
| NoticeDeliveryWriter | Repository | Writes `callback_date`, `delivery_status` and `state` in one `rwb_comms` transaction, with the idempotency row |
| S4DeliveryClient | Client | The proof-record call on `RWB-S4-E5002-CON`, one hop, 2 s, breaker, and no retry of its own (GAP-1189) |
| ProofIdempotency | Service | Builds the key from the notice ID, the delivery status and the callback date, recognises a repeat and re-runs only an incomplete hand-off |
| NoticeProof | React component | Shows the notice state, the delivery status, the callback date and the barcode on SCR-18 and SCR-19, read only, with the refusal states |

**Database and migrations.** No Flyway file. `notice` and its serving columns arrive with RWB-P6-E1052-APP, and the decision record and the idempotency key are library objects created in `rwb_comms` by the library's migration (DP-03). No column of another service's data is added, and no index is needed beyond the ones RWB-P6-E1052-APP and RWB-P6-E1055-APP create (the primary key of `notice` and its barcode index).

**Configuration and reference data.**

- The mapping of a LOV-DELIVERY value to the notice state, and the states a notice may be served from (Sent), as versioned reference rows of the business, read with their version. `PENDING` has no state mapping in any source (GAP-1192; ASM-2139).
- The LOV-DELIVERY list at its version in force (TSD P6 T3.2). The contract the list is read on and the owner of the mapping row are Not specified for this story, because the reference-data contract is not in its dependency rows (GAP-1192; ASM-2139).
- No parameter is named in the sources for the write path; the 2 s budget and the single hop are the platform rule of ADR-020 and not a value of this story.

**Build steps**

1. Build `ProofOfDeliveryValidator` over the `notice` row with the list and state checks; test AC4 and AC7.
2. Build `DeliveryOutcomeMapper` over the mapping row and its version; test AC1 and AC2.
3. Build `ProofDecisionRecordWriter` against the library fake, with the failed-write path; test AC6.
4. Build `NoticeDeliveryWriter` with the one transaction and the idempotency row; test AC5.
5. Build `S4DeliveryClient` against the contract fake, with the 2 s budget, the breaker, the no-answer path and the refusal path; test AC3.
6. Build `NoticeProofController` with the problem mapping of 403, 404, 409, 422 and 503; test AC4 and AC7.
7. Build `NoticeProof` and read the notice through the composite route fake; test AC8.
8. Add the boundary test: no statement outside `rwb_comms`, no `v_ace_*` read, no write to `rwb_case`, `rwb_litigation` or `rwb_decision` (the schemas of other owners, named only as the targets the grant must refuse); test BR6, AC9 and section 12.7.

**Feature flag.** `rwb.comms.notice-proof-v1`, read as a flag of the platform library; off means the write path answers 404 and the serving fields of the read are empty, while the automatic WIN loop of `RWB-P6-E2021-APP` is unaffected.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-S4-E5002-CON` stay green, the boundary test runs in the pipeline, and a SIT week shows one proof per notice, one hand-off per proof, no notice served twice, no write of a case row or a timer row from this service and no `v_ace_*` read in its logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack of the S4 slice, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is S4's fact and S4's screen text, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A request with no delivery status, or with no callback date on a status that carries one (X1) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right records or reads the proof (X5, AC7) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the notice changes (X6, AC6) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-002 section 14 and are copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names ("delivery status", "callback date"). `MSG-S4-001` and `MSG-S4-002` are authored by the litigation module and belong to the pack and the claim of the S4 slice (`RWB-S4-E5002-APP`); they are carried here because they are the message set of the key, and this story raises neither of them. A downstream that does not answer (X8) and a notice that is not found (X2) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-18 Notice approval | Loading | The placeholder while the composite route answers |
| SCR-18 Notice approval | Sent | The notice with its `sent_date`, `barcode` and notice type, and the proof form to record the delivery result, the delivered date and the barcode |
| SCR-18 Notice approval | Delivered | The notice state "delivered", the delivery status `DELIVERED`, the callback date and the barcode, read only |
| SCR-18 Notice approval | Unserved | The notice state "unserved" with the delivery status of the proof, and the reason the case moved is shown from the S4 side |
| SCR-18 Notice approval | Incomplete | The proof refused with MSG-GEN-001 naming the missing field, and nothing changed |
| SCR-18 Notice approval | Not dispatched | The proof refused with 409 because the notice has no sent date |
| SCR-18 Notice approval | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-18 Notice approval | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-18 Notice approval | Empty | Not specified in the source documents (CG-ALL-6804) |
| SCR-18 Notice approval | Error | Not specified in the source documents (CG-ALL-6804) |
| SCR-18 Notice approval | No access | Not specified in the source documents (CG-ALL-6804) |
| SCR-19 Litigation workspace | Pack and notice | The same notice facts, read only, next to the pack states of rwb-litigation and the case and timers of rwb-case |
| SCR-19 Litigation workspace | Loading | Not specified in the source documents (CG-ALL-6805) |
| SCR-19 Litigation workspace | Empty | Not specified in the source documents (CG-ALL-6805) |
| SCR-19 Litigation workspace | Error | Not specified in the source documents (CG-ALL-6805) |
| SCR-19 Litigation workspace | No access | Not specified in the source documents (CG-ALL-6805) |

The route merges the answer of this service with rwb-litigation and rwb-case; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-002-01 | AC1, AC2, AC5, BR1, BR2, BR5, BR13 | End to end | Notice `N-0101` Sent with barcode `RR223344556TH`; a proof with `DELIVERED` and callback date 2026-12-18; a proof with `UNDELIVERABLE`; the same proof recorded twice |
| TC-E5-002-02 | AC1, AC3, AC8, BR3, BR9, BR10, BR11 | End to end | The S4 contract fake applying the delivery answer with `R-LIT-07`; the notice read on SCR-18 and SCR-19 through the composite route |
| TC-E5-002-03 | AC2, AC3, BR2, BR3, BR12, BR14 | End to end | An `UNDELIVERABLE` proof for notice `N-0101`, the S4 answer with `R-LIT-08`, and the notice left Unserved with no timer written here |
| TC-E5-002-04 | AC6, BR4 | Component | The local decision-record library refusing the write; the notice unchanged and no call to the S4 contract |
| TC-E5-002-05 | AC7, BR8 | Component | RW-PHONECOL records and reads the proof; refused with status 403 and MSG-P4-002 |
| TC-E5-002-06 | AC4, AC6 | Component | A request with no delivery status (422, MSG-GEN-001), an unknown notice (404) and a notice with no sent date (409); the forced decision-record failure |
| TC-E5-002-07 | AC11, section 12.1 operations, BR7, BR10 | Contract | The published contract of rwb-comms on base `/api/recovery/comms/v1`: GET `/notices/{noticeId}` and POST `/notices/{noticeId}/proof-of-delivery`, with and without `Idempotency-Key`, the answers 401, 403, 404, 409, 422 and 503, and each answer checked for no person name, address or contact value |
| TC-E5-002-08 | AC9, BR3, BR6, section 12.7 tables | Boundary | Build boundary test over `rwb_comms`: a component, a statement or a test that reaches an ACE view, an ACE table or another `rwb_*` schema, or writes `rwb_case`, `rwb_litigation` or `rwb_decision`, is refused by the grant and fails the build |
| TC-E5-002-09 | AC10, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 | Boundary | Traceability check over section 8: each of BR1 to BR10 is named by a criterion or a test case of this story; BR6 and BR10 are proved by TC-E5-002-08 and TC-E5-002-07 |
| TC-P6-E5002-APP-01 | AC12 | Component | Missing and reused `Idempotency-Key` on the proof write |
| TC-P6-E5002-APP-02 | AC13 | Contract | The case read, the one `LETTER` ledger append (201 and 503), the decision-record headers and data |

The six legacy identifiers are kept in the order of the source list of RWB-E5-002. The legacy levels map System to End to end for the notice behaviour, and Access and the forced failure to Component, because the cross-service behaviour of this key is proved by `RWB-ITG-E5002-ITG` and not here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the mapping of a delivery status to the notice state, the states a notice may be served from, the lists and the message texts are data with a version; no role, list value, state name or date appears in Java.
- No personal data in logs, tests, workflow inputs or prompts: the notice row carries identifiers, dates, a barcode and list values only; the addressee, the address and the contact value never enter `rwb_comms` and are never logged, and the proof image is rwb-document's and is not created here.
- ACE data only through the owner's contract: no component of this story reads an ACE view or an ACE table, and the service holds no `v_ace_*` grant (DP-05).
- No read of another service's tables and no cross-schema join: `recovery_case`, `timer`, `task`, `decision_log_entry`, `document` and every S4 table are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on the single consumed call, with a breaker per downstream and no call chain; the retry of the hand-off is the repeat of the same idempotency key and never a silent resend.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the request (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no timer: this story publishes nothing and consumes nothing, and the notice facts reach the other services on the S4 contract only.
- The two screens are read only and write nothing; SCR-18 posts the proof through the one write operation and SCR-19 is a read.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters are dispatched for print and post, and proof of delivery returns to the case, which this story does by putting the returned proof on the notice and handing it to the case's owner | Business Requirements Program v5 (REQ-OCC-003); FSD P6 A2.2 traceability | FEAT-LIT-02, FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-UNI-40, CTL-15 | TC-E5-002-01, TC-E5-002-02, TC-E5-002-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-002 | The notice deliverable of the key: the proof on the notice, its two columns, its state, the hand-off and the screen read; the four legacy criteria are the S4 slice's |
| RWB-S4-E5002-APP (S4) | The legal action, the pack, the evaluation of R-LIT-07, R-LIT-08 and R-LIT-09, the case move and the legacy criteria AC1 to AC4 word for word |
| RWB-S4-E5002-CON | The proof-record operation, its answer, its error envelope and the fake this story builds against; the operation name is open (GAP-1189) |
| RWB-P3-E5002-APP (P3) | The case of record, its route state, the notice-period timer, the task of the period and the case-side decision record |
| RWB-ITG-E5002-ITG | The end-to-end proof of the whole key across the three services, which no criterion of this story claims |
| RWB-P6-E1052-APP | The `notice` table, its columns and the generated notice this story serves |
| RWB-P6-E1055-APP and RWB-P6-E2021-APP | The dispatch fields, the WIN acknowledgment and the automatic WIN proof loop that reads `GET /proof-of-delivery` of rwb-source-data, appends the delivery ledger entries and publishes `NoticeDelivered` |
| DP-03 | The decision record with the rule and its version, written before the notice changes |
| DP-05 | The prohibition: no ACE view and no ACE table is read here (GAP-1194) |
| DP-13, DP-19 | The service base `/api/recovery/comms/v1` and the two screens through the gateway-bff composite route |
| ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Kafka platform this story adds no producer and no consumer to, contract-first REST with one hop, and the local decision record with the central ledger |

### 19. Out of scope

- The case route state, the notice-period timer, the task of the notice period and the case-side decision record: rwb-case (P3), `RWB-P3-E5002-APP` and the notice-period timer story of this legacy family.
- The legal action, the pack, the evaluation of R-LIT-07, R-LIT-08 and R-LIT-09, the proof-window expiry and the queue transfer of an unserved notice: rwb-litigation (S4), `RWB-S4-E5002-APP`; the proof-record operation and its shape: `RWB-S4-E5002-CON`.
- The four legacy criteria of RWB-E5-002 proved end to end across the three services: `RWB-ITG-E5002-ITG`.
- The automatic WIN proof-of-delivery loop that reads the ACE rows and publishes `NoticeDelivered`, and the dispatch and acknowledgment fields it writes: `RWB-P6-E2021-APP` and `RWB-P6-E1055-APP`.
- Notice generation, the notice read baseline as a contract, and the template and merge-field catalog: `RWB-P6-E1052-APP`, `RWB-P6-E1055-CON` and `RWB-P6-E1046-APP`.
- The ACE ingestion of the proof file, the `v_ace_pod` rows, the freshness stamp and the interaction ledger store: rwb-source-data (`RWB-P1-E1055-APP`, `RWB-P1-E1066-CON`); the delivery entries appended to that ledger over REST by the automatic loop: rwb-comms (`RWB-P6-E1055-APP`).
- The scanned proof card, its custody and its retention: rwb-document (P5).
- The rights, roles, scope and masking data themselves, and the full screen model of SCR-18 and SCR-19: the rwb-access stories and `RWB-PLT-N001-CON`.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: its own OPS story.

### Remaining delivery steps

- Size and epic design sign-off: Pending (squad and design authority).
- RWB-S4-E5002-CON published with the proof-record operation name (rwb-litigation contract owner; GAP-1189).
- Load the Case record C service-identity row of the rwb-comms workload identity and update the AC13 row of Test Cases v9 (security administrator; test lead; RD-P1-064).
- Test data in DEV and the new rows in Test Cases v9 (QA).

# RWB-P8-E4043-CON Match a settlement payment - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Apply the shared topic groups and the JOB-08 ownership amendment.
- The matching run starts only on `AceDataReady` with `sourceSystem` ALS and `status` COMPLETED; events for other source systems start nothing (RD-P1-003, RD-P1-040).
- `AceDataReady` is cited with record key `{sourceSystem}:{businessDate}` and payload `sourceSystem`, `businessDate`, `status`, `completedAt` (RD-P1-003).

| Item | Value |
|---|---|
| Story key | RWB-P8-E4043-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-043 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P8-E4043-CON-16); no size is recorded in this story |
| Contract version | v1 (the `/v1` path version of each row in section 12.2) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 27 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead of rwb-payment**, I want **the published contract baseline of the settlement match — the OpenAPI 3.1 document of `/api/recovery/payment/v1` with `GET /proceeds` and `POST /proceeds/{proceedsId}/match`, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements over DF-FIN-001 to DF-FIN-009 and the lists `LOV-MATCH` and `LOV-PROCEEDS-SRC` under the reference-data contract of DP-06 and DP-07 (parameters: Not specified in the source documents (DOR-RWB-P8-E4043-CON-20)), the three event schemas `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` on `rwb.payment.events.v1` with the CloudEvents envelope, the `proceeds` table of `rwb_payment` and its versioned baseline, the error envelope, the rights, the compatibility rule and the fakes**, so that **the app story, SCR-28 Proceeds matching and the wave 3 harness build against one fixed contract on Day 1, and a path, a field, a list value, a match state or an event name can never drift between rwb-payment, rwb-treatment, rwb-case and the screens without a failing build**.

This is the contract slice of legacy RWB-E4-043 (FEAT-PAY-03, module P8 Payments and posting). It owns the published surface only: the two operations, the three event schemas, the table baseline, the error set, the rights, the compatibility rule and the fakes. It owns no behaviour and copies no legacy criterion: the two legacy acceptance criteria of the story stay word for word with RWB-P8-E4043-APP (GAP-2510; ASM-4159).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). In the monolith, the settlement match read `v_ace_payment`, the `treatment` row, the `recovery_case` row and the `decision_log_entry` row in one process on `/api/recovery/v1`, so no boundary existed that another team could build against; every reader of the match was also a reader of four other modules' tables. In the target each boundary is a contract: the receipt facts are rwb-source-data's, the settlement treatment is rwb-treatment's, the case is rwb-case's, the rule package is rwb-decision's and the money is rwb-payment's.

Two teams depend on this baseline on Day 1. RWB-P8-E4043-APP builds the settlement arm of JOB-07 and cannot start until the elements, the match value, the event names and the fakes are fixed. The rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee teams consume `ProceedsMatched` (Architecture v5 slide 43, row 25) and must pin a schema while their own stages are still being written. SCR-28 reaches the two operations through the gateway-bff composite route (DP-19), so the screen contract, the error envelope and the pagination have to be settled before the screen work starts.

The baseline also fixes the naming the checks require: schema `rwb_payment`, base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1` with retry and `.dlt` topics, event names `rwb.payment.<Event>.v1`, task queue `rwb-payment` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.payment` (Architecture v5 slide 41; Template and Rules §R4). It records that this service holds no `v_ace_*` grant and no grant on another `rwb_*` schema (Architecture v5 slide 29), so DP-05 is declared as a prohibition: the payment facts of ACE arrive on rwb-source-data's contract and never through a view of this service.

Two points are carried as gaps rather than decided quietly. The TSD names `MatchRequest` and `ProceedsPage` without a field list, and the request's element list has to be derived from the nine columns of `proceeds` and the query parameters of API-P8-001 (GAP-2514; ASM-4163). The payloads of `TreatmentBooked` and `ProceedsMatched` are not published anywhere, while `PaymentMissed` appears with a full example on Architecture v5 slide 22, so the three schemas are written from that envelope and the modelled columns (GAP-2515; ASM-4164). The settlement money side itself is R-SET-14 of the Settlement route set, but the package code and the rule IDs of the matching mechanism appear in no source, so the contract names the PAYMENT_MATCH package without fixing a rule ID (GAP-2516; ASM-4165).

### 3. Preconditions

- The service naming rule of the platform library is in force: base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1` with retry and `.dlt`, event names `rwb.<short>.<Event>.v1`, queue `rwb-<short>`, login and schema `rwb_<short>` (Architecture v5 slide 41 notes; Template and Rules §R4).
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `proceeds` and the two operations are P8's, `treatment` and `GET /treatments/{treatmentId}` are S2's, `recovery_case` is P3's, the `v_ace_*` views are P1's, `rule_row`, `rule_package_version` and `decision_log_entry` are P7's. This document never declares another service's operation or table as provided.
- The two operations and their shapes are the ones of TSD P8 T-A.1 and T-A.2: API-P8-001 `GET /proceeds` with `ProceedsPage` out and errors 401, 403 and 503, and API-P8-002 `POST /proceeds/{proceedsId}/match` with `MatchRequest` in, `Proceeds` out, errors 401, 403, 404, 409, 422 and 503, and the `Idempotency-Key` header.
- The columns and the lists are the ones of TSD P8 T3.1 and T3.2: DF-FIN-001 to DF-FIN-009 and the values `INSTALLMENT`, `SETTLEMENT`, `FEE`, `SALE_PROCEEDS` and `UNMATCHED` of `LOV-MATCH`, and `CUSTOMER`, `LED`, `AUCTION`, `BUYER`, `AGENCY`, `INSURER` and `GUARANTOR` of `LOV-PROCEEDS-SRC`.
- The three events are the ones of Architecture v5 slides 42 and 43: `TreatmentBooked` (11) and `PaymentMissed` (12) with consumers rwb-case, rwb-treatment and, for `PaymentMissed`, rwb-comms, and `ProceedsMatched` (25) with consumers rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee; the envelope is CloudEvents 1.0 in binary mode with key `caseId`, 12 partitions, replication factor 3 and 7-day retention (slide 22).
- The schema registry is in BACKWARD mode and the AsyncAPI document per service is the contract, so every event is registered against it (Architecture v5 slide 42 notes).
- The `proceeds` table arrives with the DB story of this service; this baseline declares its name, its schema, its columns and its baseline version, and creates nothing.
- RWB-P8-E4043-APP, SCR-28 and the wave 3 harness are named as the consumers of this baseline but are not build dependencies: this story has none and is Day 1 by rule (Template and Rules §R5.7).
- No approval is needed to publish a Draft baseline in this run, and no human verification stop is part of it.

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-payment for this surface: the two operations with their request and answer elements, the query parameters, the pagination, the rights and the seven error responses.
2. Fix the `Proceeds` element on DF-FIN-001 to DF-FIN-009, the `ProceedsPage` element on the pagination convention, its fields Not specified in the source documents (GAP-1366), and the `MatchRequest` element with the case reference, the treatment reference, the account payment reference, the amount, the received date and the match value, marking every derived field and every field no source gives with the placeholder.
3. Publish `LOV-MATCH`, `LOV-PROCEEDS-SRC` and the match state `SETTLEMENT` as enumerated values of the document, and fix the rule that no list value is a constant of the code.
4. Draft the AsyncAPI fragment and the three JSON schemas `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` with the CloudEvents envelope, `ce_type` `rwb.payment.<Event>.v1`, `ce_source` `/rwb-payment`, `ce_subject` `case/<caseId>`, key `caseId` and no personal data. The `TreatmentBooked` and `ProceedsMatched` field lists are written from the envelope, the modelled columns and the match value, with every field no source gives marked as a placeholder.
5. Fix the `rwb_payment.proceeds` table baseline: the columns, the standard record columns, the baseline version and the rule that no foreign key leaves the schema.
6. Record the consumed surface as consumed and faked: the settlement treatment of rwb-treatment on `GET /treatments/{treatmentId}`, the case read and answer of rwb-case, the receipt read of rwb-source-data and the package read of rwb-decision. The decision record is written locally through RWB-PLT-E1027-CON, and no `v_ace_*` view and no table of another schema is read.
7. Fix the error envelope and one message ID per condition, the rights of the capability area "Write-off and posting", and the `Idempotency-Key` rule with its stored answer.
8. Publish the five contract fakes and the drift test that compares each with the document.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the pagination, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of another service's property, and the compatibility of the three event schemas.
10. Tag the baseline and hand it to RWB-P8-E4043-APP, SCR-28 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC3 |
| X2 | A path, a property or a list value is renamed or removed within major version 1 | The contract test fails; the change needs a new major version and a new event type | None | AC7 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6, AC7 |
| X4 | A field of `MatchRequest`, `ProceedsPage` or an event payload has no source value | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-MATCH` or `LOV-PROCEEDS-SRC` appears in the document, an example or a fake | The vocabulary test fails the build | None | AC3 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, or a `treatment`, `recovery_case` or `rule_row` property | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2 |
| X8 | The rights of an operation are not the ones TSD P8 T6.1 and T-A.2 declare | The access test fails the build | MSG-P4-002 | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map, TSD P8 and the published owner documents of rwb-treatment, rwb-case, rwb-source-data and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the paths, the columns, the lists, the base, the topic, the queue and the event names are fixed by the target architecture |
| Valuable | Unblocks RWB-P8-E4043-APP, SCR-28 and the wave 3 harness on Day 1, and the five `ProceedsMatched` consumers on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment with three schemas, nine contract tables, five fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the settlement match of rwb-payment

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of proceeds and of the two operations is P8, of treatment and GET /treatments/{treatmentId} is S2, of recovery_case is P3, of the v_ace_* views is P1 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two operations are declared on the payment base with their answers and errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-payment is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /proceeds with the ProceedsPage answer of status 200 and POST /proceeds/{proceedsId}/match with the Proceeds answer of status 200, both under the base /api/recovery/payment/v1 and owned by rwb-payment
    Then GET /proceeds declares the query parameters matched, from, to, page and size, and answers ProceedsPage
    Then POST /proceeds/{proceedsId}/match declares the MatchRequest body and answers Proceeds
    Then GET /proceeds declares the errors 401, 403 and 503, and POST /proceeds/{proceedsId}/match declares the errors 401, 403, 404, 409, 422 and 503, each with the platform error envelope
    Then the document declares no monolith API base and no operation of another service

  Scenario: AC2 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD P8 T-A.2 and T6.1
    Then POST /proceeds/{proceedsId}/match declares the Idempotency-Key header and its stored answer, and GET /proceeds declares none
    Then a repeated POST with the same Idempotency-Key returns the stored answer and describes no second effect
    Then a repeated match of an already matched proceeds reference answers 409, an unknown proceedsId answers 404, and a missing or invalid field answers 422 with MSG-GEN-001
    Then a role without the Write-off and posting right R or U answers 403 with MSG-P4-002, and a downstream that does not answer inside 2 s answers 503
    Then GET /proceeds declares right R and POST /proceeds/{proceedsId}/match declares right U, each with the scope applied, and the document names the capability area Write-off and posting

  Scenario: AC3 The Proceeds and MatchRequest elements and the two lists are fixed and no business value is in the schema (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with TSD P8 T3.1 and T3.2
    Then the Proceeds element declares id, case_id, treatment_id, account_payment_id, source, amount, received_date, matched_to and posting_ref, being DF-FIN-001 to DF-FIN-009, with the standard record columns
    Then source is declared against LOV-PROCEEDS-SRC with the values CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER and GUARANTOR
    Then matched_to is declared against LOV-MATCH with the values INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS and UNMATCHED
    Then the MatchRequest element carries the case reference, the treatment reference, the account payment reference, the amount, the received date and the match value, and every field of it that no source gives is Not specified in the source documents (GAP-2514; ASM-4163) and is marked so
    Then the ProceedsPage element carries the page of Proceeds with its page, size and total, and the fields that no source gives carry the same placeholder
    Then no threshold, tolerance, window, percentage, amount or rule ID appears as a schema default, an example constant or an enumeration member of the code

  Scenario: AC4 The three event schemas are fixed on the payment topic with the CloudEvents envelope (new, D-RCV-60)
    Given the AsyncAPI fragment of rwb-payment
    When it is compared with Architecture v5 slides 42 and 43 and with slide 22
    Then it declares TreatmentBooked, PaymentMissed and ProceedsMatched as rwb.payment.TreatmentBooked.v1, rwb.payment.PaymentMissed.v1 and rwb.payment.ProceedsMatched.v1 on rwb.payment.events.v1, with the .retry and .dlt topics
    Then each message declares the CloudEvents 1.0 binary envelope with ce_specversion, ce_type, ce_source /rwb-payment, ce_id, ce_subject case/<caseId> and a W3C traceparent header, and the key caseId
    Then the PaymentMissed payload keeps the published example fields caseId, treatmentId, dueDate, amountDue and daysLate
    Then the ProceedsMatched payload carries the case reference, the proceeds reference, the treatment reference, the amount, the value date, the match value and the rule ID with its version, and the fields that no source gives are Not specified in the source documents (GAP-2515; ASM-4164)
    Then no payload carries a name, an address, a contact value or an identity number
    Then the registry is BACKWARD and a change that removes or retypes a field is a new event type and not an edit in place

  Scenario: AC5 The proceeds table and its baseline are declared with no cross-schema key (new, D-RCV-60)
    Given the data section of the baseline
    When it is compared with TSD P8 T3.1, T3.0 and the Ownership Map
    Then the table is rwb_payment.proceeds and it declares DF-FIN-001 to DF-FIN-009 with the standard record columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then its baseline is one versioned file of this service's own sequence in rwb_payment, and no other service's table is created, altered or referenced
    Then case_id, treatment_id and account_payment_id are declared as identifiers and not as foreign keys, and no key, join or view leaves rwb_payment
    Then the document declares no v_ace_* view and no grant on another rwb_* schema, and the boundary test fails a build that adds one
    Then the migration itself is the DB story of this service and this baseline creates nothing

  Scenario: AC6 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation, the element or the event it serves
    Then the rwb-source-data receipt fake answers a receipt of source CUSTOMER for case "RC-2026-000431" with its business date, a stale product with its date, and no answer beyond 2 s
    Then the rwb-treatment settlement fake answers the settlement treatment "TR-2026-000431" of the case and a case without a treatment
    Then the rwb-case fake answers the case reference with its route state, and an accepted and a refused money-side answer
    Then the rwb-decision package fake answers the PAYMENT_MATCH package at its version in force
    Then the decision-record library stub answers a healthy chain and a stopped chain with MSG-P7-003
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The compatibility rule and the absence test are fixed (new, D-RCV-60)
    Given the compatibility and boundary sections of the baseline
    When the nine sub-tables and the registry settings are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_payment, the login is rwb_payment, the topic is rwb.payment.events.v1, the queue is rwb-payment and the Java package is th.co.scb.ace.workbench.recovery.payment
    Then a schema change is additive within major version 1, and a breaking change is a new major version with a new event type and no edit in place
    Then the document lists only operations owned by rwb-payment, and the consumed treatment, case, receipt and package surfaces are described as consumed and faked, never as provided
    Then the document declares no Schedule, no Quartz row and no shared job table, and JOB-07 is declared as an event-started workflow and not a schedule
    Then the absence test fails a build that adds a v_ace_* view, another service's property, a monolith base or a second topic

  Scenario: AC8 Each business rule BR1 to BR11 of section 8 is carried by a named element, operation, event or guardrail (new, D-RCV-60)
    Given the business rules of section 8 and the baseline
    When each rule is compared with the element, operation, event or guardrail that carries it
    Then BR1 and BR2 are carried by the Proceeds element and the two lists of AC3, with the vocabulary closed and no list value a constant of the code
    Then BR3 is carried by the decision record row of section 11, written through the local library before the proceeds row changes, with a failed write as MSG-P7-003 (AC6 stub)
    Then BR4 and BR5 are carried by the absence test of AC5 and AC7: no v_ace_* view and no property of treatment, recovery_case, rule_row or rule_package_version
    Then BR6 is carried by AC2: the POST declares the Idempotency-Key and the GET declares none
    Then BR7 and BR8 are carried by AC7: one base, topic, queue and login, and an additive change within major version 1
    Then BR9 and BR11 are carried by AC4 and AC7: the events carry identifiers and facts only, and only operations of rwb-payment are listed
    Then BR10 is carried by the guardrail of section 17: the settlement arm is governed in rwb-decision, and the package code and rule IDs stay Not specified in the source documents (GAP-2516; ASM-4165)
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-P8-E4043-APP and they copy no criterion of the legacy story, whose two criteria stay with the app story word for word (GAP-2510; ASM-4159).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The receipt and its match are P8's: `proceeds` in `rwb_payment` carries the case, the treatment, the account payment, the source, the amount, the received date, `matched_to` and the posting reference, and the contract declares their shapes only | Architecture v5 slide 41; Ownership Map (`proceeds` owner P8); TSD P8 T3.1 |
| BR2 | The vocabulary is closed: `source` is one value of `LOV-PROCEEDS-SRC`, `matched_to` is one value of `LOV-MATCH`, and the settlement match writes `SETTLEMENT`; no list value is a constant of the code | TSD P8 T3.2; FSD P8 A2.3.3.1 (BR-P8-003) |
| BR3 | The decision record is declared as an element written before the proceeds row changes, through the local library on the shared topic, and a failed write is MSG-P7-003 | DP-03; legacy RWB-E4-043 AC1 and AC2, owned by the app story |
| BR4 | No ACE view and no ACE table is read: the receipt facts are consumed on rwb-source-data's contract and the service holds no `v_ace_*` grant | DP-05; Architecture v5 slide 29 |
| BR5 | The treatment, the case and the rule package stay with their owners: the contract declares the treatment read as consumed, the case read and answer as consumed, and the package read as consumed, and declares no property of them | Ownership Map (treatment S2, recovery_case P3, rule_row and rule_package_version P7); DP-01 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD P8 T-A.2 |
| BR7 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR8 | A schema change is additive within major version 1; a breaking change is a new major version with a new event type | Architecture v5 slides 42 and 43 notes (BACKWARD compatibility) |
| BR9 | The events carry IDs and facts only: caseId, treatmentId, dueDate, amountDue, daysLate, the proceeds reference, the amount, the value date, the match value and a rule version, and no personal data | Architecture v5 slide 22 notes and slide 42 notes; Template and Rules §R7.2 (s17) |
| BR10 | The settlement money side is the transition R-SET-14 of the Settlement route set (AWAITING_PAYMENT to PAYMENT_CLEARED, amount_received = settlement_amount), governed in rwb-decision; the package code, the rule IDs of the matching mechanism and its tolerance and window rows appear in no source, so the contract names the PAYMENT_MATCH package of the Temporal and Drools design, fixes no rule ID and carries the placeholder (GAP-2516; ASM-4165); the settlement arm is governed as rules of the PAYMENT_MATCH package in rwb-decision, and its outcome fields, thresholds, tolerance, window and money-side close state are held as rule rows and reference data with the placeholder, never written in code (GAP-1364; GAP-1368) | Business Rules and Routing Logic v4 (R-SET-14); Temporal and Drools Design slide 18 (PAYMENT_MATCH replaces payment_match_rule); GAP-2516; GAP-1364; GAP-1368 |
| BR11 | The document lists only operations owned by rwb-payment; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |

### 9. State transitions

The lifecycle of this document, not of a receipt:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the elements, the three event schemas, the table baseline and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-28, the wave 3 harness and the rwb-treatment, rwb-case, rwb-source-data and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional request field | Baselined |
| Baselined | Breaking change | A path, a property or a list value is removed, renamed or retyped, or a match value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence test of AC7 fails: a `v_ace_*` view, another service's property, a second topic or a Schedule | In review |

The match state of the receipt that the document describes is the app story's: `matched_to` is one value of `LOV-MATCH` of TSD P8 T3.2 and the settlement arm writes `SETTLEMENT`; this baseline fixes the vocabulary and moves no receipt.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-payment | Owns the OpenAPI document, the AsyncAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, SCR-28, the wave 3 harness and the owners of rwb-treatment, rwb-case, rwb-source-data, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the outbox and inbox library and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element, an event payload or a fake |
| rwb-access owner | Owns the authorise check that the operations of this document call under DP-08; the check is consumed and faked here and never provided |

The per-service login behind the security scheme of the document is named "the rwb-payment login" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Proceeds element | The columns of DF-FIN-001 to DF-FIN-009: `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to` and `posting_ref` |
| Standard record columns | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at` and `updated_by` of TSD P8 T3.0 |
| Lists | `LOV-MATCH` and `LOV-PROCEEDS-SRC` of TSD P8 T3.2, published as enumerated values |
| MatchRequest element | The fields the match needs, carried with the placeholder where no source gives them: Not specified in the source documents (GAP-2514; ASM-4163) |
| ProceedsPage element | The page envelope on the platform pagination convention, with the fields that no source gives carried as Not specified in the source documents (GAP-1366) |
| PaymentMissed payload | The published example fields `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate` of Architecture v5 slide 22 |
| TreatmentBooked and ProceedsMatched payloads | The identifiers and facts of the modelled rows on the CloudEvents envelope of Architecture v5 slide 22, with the fields that no source gives carried as Not specified in the source documents (GAP-2515; ASM-4164; GAP-1367) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Not declared here | `treatment` (S2), `recovery_case` (P3), `v_ace_*` (P1), `rule_row`, `rule_package_version` and `decision_log_entry` (P7): each is named as an answer or a rule version of its owner and none is a property of this document |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC3 and the optionality rule of BR8. **No new table, no new column and no migration** is created by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, filtered by `matched`, `from` and `to`, paginated by `page` and `size` (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` out (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header required; the answer is stored |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD P8 T-A.1 and T-A.2; the paths are those of the target base and not the monolith form. `GET /cases/{id}/payments` and the manual `POST /proceeds/{id}/allocate` of Architecture v5 slide 17 are read as the case-scoped view and the manual form of this family, and neither is declared as a third operation: their operation names are Not specified in the source documents (GAP-2514; ASM-4163).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /treatments/{treatmentId}` | `/api/recovery/treatment/v1` | S2 rwb-treatment | The settlement treatment of the case: its type, its terms and its status; faked |
| The case read and the money-side answer (operation names Not specified in the source documents (GAP-2514; ASM-4163)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its product group and its route state, and the answer that carries the rule ID and the version that closed the money side; faked |
| The receipt read of the ACE batch (operation name Not specified in the source documents (GAP-2514; ASM-4163)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The receipts of the business date for source `ALS`, with the freshness stamp of the data product; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2516; ASM-4165)) | `/api/recovery/decision/v1` | P7 rwb-decision | The PAYMENT_MATCH package at the version in force; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row for this story does not carry, because it is None, so the app story builds against these documents and fakes on Day 1 (GAP-2514; ASM-4163).

#### 12.3 Events published

Topic `rwb.payment.events.v1`, with the `.retry` and `.dlt` topics, 12 partitions, replication factor 3 and 7-day retention, key `caseId` (Architecture v5 slide 22).

| Event | Schema name | Consumers | Payload element |
|---|---|---|---|
| `TreatmentBooked` (EV-11) | `rwb.payment.TreatmentBooked.v1` | rwb-case, rwb-treatment | The case and treatment references with the booking facts; the field list is Not specified in the source documents (GAP-2515; ASM-4164) |
| `PaymentMissed` (EV-12) | `rwb.payment.PaymentMissed.v1` | rwb-case, rwb-treatment, rwb-comms | `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate`, as the published example of Architecture v5 slide 22 |
| `ProceedsMatched` (EV-25) | `rwb.payment.ProceedsMatched.v1` | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | The case, proceeds and treatment references, the amount, the value date, the match value and the rule ID with its version; the remaining field list is Not specified in the source documents (GAP-2515; ASM-4164) |

Each message declares the CloudEvents 1.0 binary envelope with `ce_specversion`, `ce_type`, `ce_source` `/rwb-payment`, `ce_id`, `ce_subject` `case/<caseId>` and a W3C `traceparent` header, and the body is validated against the registry in BACKWARD mode. `ProceedsMatched` is published by the settlement, auction and enforcement matching steps of this service, and this baseline declares its schema once for all of them; the publishing story is RWB-P8-E4043-APP for the settlement arm.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When | Owner |
|---|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | `rwb-payment.rwb.source-data.events.v1` | `sourceSystem`, `businessDate`, `status`, `completedAt`; record key `{sourceSystem}:{businessDate}`; the run starts only on `sourceSystem` ALS and `status` COMPLETED | Declared as consumed by the matching stories; starts the JOB-07 workflow | Not specified in the source documents (DOR-RWB-P8-E4043-CON-24) |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | `rwb-payment.rwb.treatment.events.v1` | The case, the treatment reference and the treatment type | Declared as consumed by the matching stories | rwb-treatment |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.rwb.decision.events.v1` | The package code and the version in force | Declared as consumed by the matching stories | rwb-decision |

`DecisionRecorded` (EV-08) is written by all nineteen services through the local library on the shared topic `rwb.decision-record.v1`, and its consumers are rwb-decision and rwb-reporting (Architecture v5 slide 42, row 08). rwb-payment is a **producer** of that topic and not a consumer: the baseline declares the record through the library of DP-03 and adds no consumer group, subscription or inbox row for it.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The JOB-07 event-started workflow (`PaymentMatchingWorkflow` in the app story; the name is a target design choice) | Workflow, one execution per business date and source, started by `AceDataReady` (`sourceSystem` ALS, `status` COMPLETED) | `rwb-payment` in namespace `rwb-recovery` | The workflow boundary the baseline serves: the input record, the three signals and the outcome; not built here |
| `matchPayments` | Activity, the matching step (Architecture v5 slide 17) | `rwb-payment` | The activity contract the baseline serves: the receipts, the case and the treatment in; the rule ID with its version, the match outcome, the record, the row and the outbox event out |
| `postProceeds` | Activity, the saga step (Architecture v5 slide 17; Temporal and Drools Design, `Payment.postProceeds`) | `rwb-payment` | Another story's activity on the same queue; its answer is one hop in a saga and is not declared by this baseline |

No child workflow for the money and no Nexus operation is declared here. The baseline fixes the input and the answer of the matching boundary only, and the workflow name is the app story's choice because no source document names it.

#### 12.6 Schedules

None. JOB-07 and JOB-08 are event-triggered workflows in the owning service and not Temporal Schedules (Architecture v5 slide 44), so the baseline declares no Schedule, no Quartz row and no shared job table, and no Job of slide 44 is moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| proceeds | P8 (`rwb_payment`) | The receipt and its match; the table the two operations read and the match writes |
| decision_record | PLT library, created in `rwb_payment` | The local hash-linked decision record of the rule outcome (DP-03) |
| outbox_event | PLT library, created in `rwb_payment` | The three events of 12.3 and the relay (DP-09) |
| processed_event | PLT library, created in `rwb_payment` | The inbox row of each consumed event (DP-09) |
| idempotency_key | PLT library, created in `rwb_payment` | The key of the repeated POST and the answer it holds |

The baseline declares the `proceeds` table and its versioned baseline in `rwb_payment`; the migration itself is the DB story of this service. `treatment` (S2), `recovery_case` (P3), the `v_ace_*` views (P1), and `rule_row`, `rule_package_version` and `decision_log_entry` (P7) are other owners'; the baseline names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data receipt fake | A receipt of source `CUSTOMER` for case `RC-2026-000431` with its business date; a stale product with its date; no answer beyond 2 s | AC1, AC3, AC6 |
| rwb-treatment settlement fake | The settlement treatment `TR-2026-000431` of the case; a case without a treatment | AC1, AC2, AC6 |
| rwb-case fake | The case reference with its route state; an accepted and a refused money-side answer | AC1, AC2, AC6 |
| rwb-decision package fake | The PAYMENT_MATCH package at its version in force | AC1, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain with MSG-P7-003 | AC2, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case answer, the rwb-source-data receipt read and the rwb-decision package read are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2514, GAP-2516; ASM-4163, ASM-4165).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two operations on `/api/recovery/payment/v1`; the treatment, case, receipt and package rows; one hop, 2 s |
| Kafka | 3 published, 3 consumed | `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` on `rwb.payment.events.v1`; `AceDataReady`, `TreatmentApproved` and `RulePackageInForce` through the shared service groups in section 12.4 |
| Temporal | 1 workflow boundary and 2 activities declared, 0 registered | JOB-07 on `rwb-payment` with `matchPayments`; `postProceeds` is another story's; no Schedule |
| File | None | No file is read, built or delivered here; the posting file is the posting story's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no receipt, no treatment, no case and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment with three schemas, nine contract tables and five fakes.

**Deliverables.** The additive document `openapi/rwb-payment-v1.yaml` for this surface, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, `LOV-MATCH` and `LOV-PROCEEDS-SRC` as published enumerations, the three JSON schemas with the CloudEvents envelope, the contract README rows for the four consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: only rwb-source-data holds SELECT on the `recovery.v_ace_*` views (Architecture v5 slide 29), so the document declares no `v_ace_*` read and no grant on another `rwb_*` schema, and the legacy `v_ace_payment` read of DF-ACE-043 to DF-ACE-054 is consumed on the owner's contract instead. DP-03 fixes the record element that is written before the match; DP-13 moves the base and nothing else; DP-19 is behind SCR-28 Proceeds matching, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, so the outbox and inbox rows are declared as library objects and not as a pattern of this baseline.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, while the plan's build list for this story is None, so the baseline builds against their fakes until those platform contract stories publish; the four consumed rows are class C dependencies in fact that the plan's C row does not carry, and they are built against their documents and fakes until their owners publish (GAP-2514; ASM-4163).

**Build steps**

1. Write the two operations and validate the surface of AC1 in the pipeline.
2. Write the `Proceeds` and `ProceedsPage` elements of AC3 from DF-FIN-001 to DF-FIN-009 and the pagination convention, with the placeholder on the fields the sources do not give.
3. Write the `MatchRequest` element of AC3 against the match the app story describes, with the placeholder and the note on its unstated fields.
4. Publish `LOV-MATCH` and `LOV-PROCEEDS-SRC` as enumerations and add the vocabulary test of AC3.
5. Write the AsyncAPI fragment and the three schemas of AC4 with the CloudEvents envelope and the no-personal-data rule.
6. Record the table baseline of AC5 and the versioned file naming, with the no-cross-schema-key test.
7. Record the error envelope, the rights and the `Idempotency-Key` rule of AC2.
8. Publish the five fakes of AC6 and the drift test.
9. Record the compatibility and boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and the drift test is green, the three event schemas register in BACKWARD mode, and the app story, SCR-28 and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the `MatchRequest` is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the proceeds row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-P8-003-1 of the FSD | {product} is from {date}. Today's load has not arrived. |

The four message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged except MSG-P1-001, whose English text is copied from Error and Message Standard v4; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and it is raised by the receipt read of the app story and not by this baseline.

### 15. Screens and states

The contract serves SCR-28 Proceeds matching in its loading, matched and unmatched states through the gateway-bff composite route (DP-19). Its empty, error and no access states are Not specified in the source documents (CG-ALL-7636), because the screen specification does not give them. The route calls rwb-payment for `GET /proceeds` and `POST /proceeds/{proceedsId}/match`, rwb-case for the case and its route state and rwb-treatment for the settlement treatment; this baseline fixes the rwb-payment answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal and failure states the screen shows — refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001 — read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E4043-CON-01 | AC1, AC2 | Contract | The document validates; the two operations, the base, the query parameters, the answers, the errors, the `Idempotency-Key` rule and the rights are present, and no monolith base is declared |
| TC-P8-E4043-CON-02 | AC3 | Contract | The `Proceeds`, `ProceedsPage` and `MatchRequest` elements validate against DF-FIN-001 to DF-FIN-009, `LOV-MATCH` and `LOV-PROCEEDS-SRC`, and no threshold, amount or rule ID appears as a default or a constant |
| TC-P8-E4043-CON-03 | AC4 | Contract | The three event schemas validate with the CloudEvents envelope, `ce_source` `/rwb-payment`, key `caseId`, the published `PaymentMissed` example and no personal data; a removed field is refused in BACKWARD mode |
| TC-P8-E4043-CON-04 | AC5, AC7 | Contract | The `rwb_payment.proceeds` baseline declares DF-FIN-001 to DF-FIN-009 and the standard columns, no cross-schema key, no `v_ace_*` read and no Schedule, and a forbidden element fails the absence test |
| TC-P8-E4043-CON-05 | AC6 | Contract | The five fakes answer every consumed path; a drifted fake fails the build; a repeated POST with the same `Idempotency-Key` returns the stored answer |
| TC-P8-E4043-CON-06 | AC8 | Contract | Each of BR1 to BR11 of section 8 has one named check in the document; the absence test fails a build that adds a v_ace_* view, a POST without `Idempotency-Key`, a GET with one, or a second topic |
| TC-P8-E4043-CON-07 | AC5 | Contract | The five tables of 12.7 are declared in `rwb_payment` at their boundary: no sixth table, no foreign key and no cross-schema key; a sixth table fails the absence test |

Legacy test cases TC-E4-043-01 to TC-E4-043-04 are owned by RWB-P8-E4043-APP. The seven cases above are new contract cases; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the match thresholds, the tolerance, the window, the percentages, the amounts and the rule IDs stay data, reference data or the rule package, never a schema default, an example constant or an enumeration member of the code.
- No personal data in a schema, an example, an event payload or a fake: identifiers, amounts, dates, list values and a rule version only, and every example is synthetic.
- ACE data only through the owner's contract or a `v_ace_*` view the service holds: it holds none, so the document declares no ACE view and no ACE table and the receipt is consumed on rwb-source-data's contract (DP-05; Architecture v5 slide 29).
- The treatment stays with rwb-treatment, the case with rwb-case and the rule package with rwb-decision: the document declares no `treatment`, `recovery_case`, `rule_row` or `rule_package_version` property and no write of their rows (DP-01).
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-payment; a consumed operation is described as consumed and faked, never as provided (DP-11).
- No retired element is reintroduced: the absence test fails a build that declares a `v_ace_*` read, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-PAY-03 | A settlement payment is matched to the treatment and the result is recorded with its rule version (FSD P8 A2.3 and AC-P8-003-01); the legacy story master carries no requirement id (GAP-2510; ASM-4159) | The two operations, the match value, the `ProceedsMatched` schema and the record element | TC-P8-E4043-CON-01, TC-P8-E4043-CON-03 |
| BR-P8-003 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.3.3.1) | The two lists as published enumerations and the absence rule of any threshold in the schema | TC-P8-E4043-CON-02 |
| VR-P8-003-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.3.3.1) | The freshness row of the consumed receipt contract and the message of section 14 | TC-P8-E4043-CON-01 |
| ADR-014 | Schema and login per service | The `rwb_payment` table baseline and the no-cross-schema-key rule | TC-P8-E4043-CON-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The three schemas with the CloudEvents envelope and the BACKWARD registry rule | TC-P8-E4043-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-P8-E4043-CON-01 |
| ADR-022 | Local decision record plus central ledger | The record element written before the match, through the library | TC-P8-E4043-CON-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-043, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-P8-E4043-APP; this baseline copies none of them |
| Test cases | The five new contract cases TC-P8-E4043-CON-01 to -05; the four legacy cases belong to the app story |
| Feature and screens | FEAT-PAY-03 Match a settlement payment; SCR-28 Proceeds matching |
| Rules | The PAYMENT_MATCH package, named from the Temporal and Drools design and governed in rwb-decision, with no package code or rule ID fixed here; the settlement money side itself is R-SET-14 of the Business Rules and Routing Logic v4 (GAP-2516; ASM-4165) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the settlement arm of JOB-07, the evaluation of the package, the decision record, the proceeds row and the `ProceedsMatched` publication: RWB-P8-E4043-APP.
- The settlement treatment, its terms and its plan timers: rwb-treatment (S2), whose read this baseline declares as consumed and faked.
- The case of record, its route states and the money-side answer: rwb-case (P3).
- The ACE receipt facts, the batch status and the freshness of the data product: rwb-source-data (P1).
- The PAYMENT_MATCH package, its rule rows, its version and its approval: rwb-decision (P7).
- The posting of the settlement booking to ALS and to the general ledger, the posting reference of DF-FIN-009 and the posting file: the posting stories of this service.
- The booking confirmation and the plan-installment matching that publish `TreatmentBooked` and `PaymentMissed`, and the exception list of an unmatched receipt: RWB-P8-E2008-APP and RWB-P8-E2027-APP.
- The creation of the `proceeds` table and its migration: the DB story of this service, whose table this baseline declares.
- The gateway-bff composite route and the screen field list of SCR-28: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E4043-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

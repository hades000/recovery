# RWB-P8-E4048-CON Run the deed in lieu rental auto-debit - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-066: Reuse the existing service listener and inbox for each topic and remove per-story consumer groups.
- `AceDataReady` (EV-26): record key `{sourceSystem}:{businessDate}` and the four-field payload (RD-P1-003).
- Start rule: the JOB-07 run starts only on the event with `sourceSystem` `ALS` and `status` `COMPLETED` (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-P8-E4048-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-048 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; Not specified in the source documents (DOR-RWB-P8-E4048-CON-16) |
| Depends on (build) | None |
| Contract dependencies | rwb-treatment treatment contract (class C; rental-terms read, built against its fake; field names not specified in the source documents (GAP-1379)) |
| Contract version | v1 (path suffix /v1 on the four REST operations in section 12.2) |
| Readiness decisions | RD-P1-003, RD-P1-040, RD-P1-066 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead of rwb-payment**, I want **the published rental profile of the payment contract - the two operations `GET /proceeds` and `POST /proceeds/{proceedsId}/match` on `/api/recovery/payment/v1` with the rental fields of `MatchRequest` and `Proceeds`, the rental element of the `payment_match_rule` row, the `PaymentMissed` and `ProceedsMatched` schemas with their rental facts on `rwb.payment.events.v1`, the `proceeds` table template, the error envelope, the rights, the compatibility rule and the fakes**, so that **RWB-P8-E4048-APP, SCR-28 and the wave 3 harness build against one fixed rental contract on Day 1, and the rental amount, the debit day, the match state or the arrears event can never drift between rwb-payment, rwb-treatment, rwb-case and the screens without a failing build**.

This is the contract slice of legacy RWB-E4-048 (FEAT-PAY-09, module P8 Payments and posting). It owns the published surface of the rental arm only. It owns no behaviour and copies no legacy criterion: the two legacy acceptance criteria of the key stay word for word with RWB-P8-E4048-APP (GAP-2527; ASM-4177).

The base surface of `/api/recovery/payment/v1`, the `proceeds` element group and the three payment event schemas are declared once by RWB-P8-E4043-CON. This profile declares the rental additions to that surface and the rental fakes, and it never redefines a member it does not own (GAP-2527; ASM-4177).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020), and the rental arm is the clearest case of it in this service. In the monolith the rental was a treatment row, an auto-debit instruction, a `v_ace_payment` read, a `proceeds` row and a task in one process: no boundary existed that rwb-treatment, rwb-case or the screens could build against, so every reader of the rental was also a reader of four other modules' tables.

In the target the rental has two owners and one seam. rwb-treatment owns the rental record, its amount, its debit day and the arrears limit (FEAT-TRT-16, R-DIL-32, R-DIL-34). rwb-payment owns the receipt, its match, the arrears announcement and the posting (TSD P8 T3.1; Ownership Map, `proceeds` owner P8). The seam is this document: the rental read as a consumed answer, the receipt as a published element, and `PaymentMissed` as the announcement that lets rwb-treatment apply the arrears rule without reading a payment table.

Three teams need it on Day 1. RWB-P8-E4048-APP builds the rental arm of JOB-07 and cannot start until the request element, the match value, the event names and the fakes are fixed. rwb-treatment consumes `PaymentMissed` and must pin a schema while its own rental record is being written. SCR-28 reaches both operations through the gateway-bff composite route (DP-19), so the screen answer, the pagination and the error envelope have to be settled before the screen work starts.

The profile also fixes the naming the checks require: schema `rwb_payment`, base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1` with retry and `.dlt` topics, event names `rwb.payment.<Event>.v1`, queue `rwb-payment` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.payment` (Template and Rules R4). It records that this service holds no `v_ace_*` grant, so DP-05 is a prohibition: the receipt arrives on rwb-source-data's contract and never through a view of this service.

Two points are carried as gaps rather than decided quietly. `LOV-MATCH` holds no value that names a rental, so the rental receipt is matched to INSTALLMENT and the assumption is recorded (GAP-2528; ASM-4172). The payloads of `PaymentMissed` and `ProceedsMatched` are published in part only - `PaymentMissed` has a full example on Architecture v5 slide 22 and `ProceedsMatched` has a consumer list and no payload - so the rental fields beyond the example are marked with the placeholder (GAP-2526; ASM-4178).

### 3. Preconditions

- The service naming rule is in force: base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1` with retry and `.dlt`, event names `rwb.<short>.<Event>.v1`, queue `rwb-<short>`, login and schema `rwb_<short>` (Template and Rules R4; Architecture v5 slide 41 notes).
- RWB-P8-E4043-CON has published the base surface: the two operations, the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, the `proceeds` table template and the three payment event schemas. This profile is additive on it and declares no member of it a second time.
- The platform error envelope, the pagination convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `proceeds`, `payment_match_rule` and the two operations are P8's, the treatment and the rental record are S2's, `recovery_case` is P3's, the `v_ace_*` views and the ACE batch are P1's, `rule_row` and `rule_package_version` are P7's. No other service's operation or table is declared as provided.
- The operations and their base shapes are those of TSD P8 T-A.1 and T-A.2: API-P8-001 `GET /proceeds` with `ProceedsPage` out and errors 401, 403 and 503, and API-P8-002 `POST /proceeds/{proceedsId}/match` with `MatchRequest` in, `Proceeds` out, errors 401, 403, 404, 409, 422 and 503, and the `Idempotency-Key` header.
- The columns and the lists are those of TSD P8 T3.1 and T3.2: DF-FIN-001 to DF-FIN-009 for `proceeds`, DF-REF-261 to DF-REF-273 for `payment_match_rule`, LOV-MATCH, LOV-PROCEEDS-SRC and LOV-MATCH-TYPE.
- The events are those of Architecture v5 slides 22, 42 and 43: `PaymentMissed` (12) with the published example `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate`, and consumers rwb-case, rwb-treatment and rwb-comms; `ProceedsMatched` (25) with consumers rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee. `TreatmentBooked` (11) belongs to the booking profile and is not declared here.
- The schema registry is in BACKWARD mode and an AsyncAPI document per service is the contract, so every event is registered against it (Architecture v5 slide 42 notes).
- The `proceeds` table arrives with the DB story of this service; this profile declares its rental constraints and creates nothing.
- RWB-P8-E4048-APP, SCR-28 and the wave 3 harness are the consumers of this profile but are not build dependencies: this story has none and is Day 1 by rule (Template and Rules R5.7).
- No approval is needed to publish a Draft baseline in this run, and no human verification stop is part of it (ASM-4180).

### 4. Flow

1. Draft the additive profile of the rwb-payment OpenAPI document for the rental arm: the request fields of the match that the rental needs, the answer fields the rental shows, the rights and the errors.
2. Fix the rental values of `MatchRequest`: the case reference, the treatment reference, the receipt reference, the amount, the received date and the match value INSTALLMENT; mark every field no source gives with the placeholder. The rental receipt takes INSTALLMENT; no RENTAL value is added to LOV-MATCH (GAP-2528).
3. Fix the rental group of `Proceeds`: the treatment reference of DF-FIN-003, the receipt reference of DF-FIN-004, the source of DF-FIN-005, the amount of DF-FIN-006, the received date of DF-FIN-007, the match value of DF-FIN-008 and the posting reference of DF-FIN-009. The rental receipt and the arrears follow-up are `Proceeds` instances distinguished by source and `matched_to`; no rental property is added (GAP-1381).
4. Publish the `payment_match_rule` element of DF-REF-261 to DF-REF-273 as read-only reference data of the service, with its lists, and fix the rule that no window, grace, tolerance, floor or priority is a constant of the code.
5. Draft the AsyncAPI fragment for `PaymentMissed` and `ProceedsMatched` with the CloudEvents envelope, `ce_source` `/rwb-payment`, key `caseId` and no personal data, and register both payloads in BACKWARD mode. The rental reference, the business date, the debit day and the rule identity fields are declared in both payloads; a field no source names is marked Not specified in the source documents (GAP-2526).
6. Fix the rental constraints of the `proceeds` template: the unique key of a receipt, the index of the match state, and the rule that no foreign key leaves `rwb_payment`.
7. Record the consumed rental read, the receipt read, the case answer and the package read as consumed and faked.
8. Fix the error envelope, one message ID per condition, the rights of the capability area Write-off and posting, and the `Idempotency-Key` rule with its stored answer.
9. Publish the five fakes and the drift test that compares each with the document.
10. Add the contract tests and tag the baseline for RWB-P8-E4048-APP, SCR-28 and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation | The pipeline schema lint fails; a deployed service answers 400 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A path, a property or a list value is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC7 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6, AC7 |
| X4 | A field of `MatchRequest` or of an event payload has no source value | The row carries the placeholder, the gap and the assumption, and the fake derives from the document | None | AC3, AC4 |
| X5 | A value outside LOV-MATCH, LOV-PROCEEDS-SRC or LOV-MATCH-TYPE appears in the document, an example or a fake | The vocabulary test fails the build | None | AC3 |
| X6 | The profile declares another service's operation as provided, a `v_ace_*` view, or a `treatment`, `recovery_case` or `rule_row` property | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | A POST is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC2 |
| X8 | The rights of an operation are not the ones TSD P8 T6.1 declares | The access test fails the build | MSG-P4-002 | AC2 |
| X9 | The profile restates a member of the base surface of RWB-P8-E4043-CON | The review fails the profile as a duplicate and the drift test names the owner | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map, TSD P8 and the base surface of RWB-P8-E4043-CON only |
| Negotiable | The added element names, the example values and the fixtures are settled in the review; the paths, the columns, the lists, the base, the topic and the event names are fixed by the target architecture |
| Valuable | Unblocks the rental arm, SCR-28 and the wave 3 harness on Day 1, and pins `PaymentMissed` for rwb-treatment |
| Estimable | One additive profile, one AsyncAPI fragment with two schemas, nine contract tables and five fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract profile of the deed in lieu rental auto-debit

  Background:
    Given the service naming rule of the platform library is in force
    Given the base surface of /api/recovery/payment/v1 and the proceeds element group are RWB-P8-E4043-CON's
    Given the ownership of proceeds and payment_match_rule is P8, of the treatment and the rental record is S2, of recovery_case is P3, of the v_ace_* views is P1 and of rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two operations are declared with the rental answers and the error set (new, D-RCV-60)
    Given the OpenAPI 3.1 profile of rwb-payment is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then GET /proceeds answers ProceedsPage with the rental fields of DF-FIN-003 to DF-FIN-009 for status 200 under the base /api/recovery/payment/v1
    Then POST /proceeds/{proceedsId}/match declares the MatchRequest body with the rental fields and answers Proceeds
    Then GET /proceeds declares the errors 401, 403 and 503 and POST /proceeds/{proceedsId}/match declares 401, 403, 404, 409, 422 and 503, each with the platform error envelope
    Then the profile declares no monolith API base, no operation of another service and no third operation for the rental

  Scenario: AC2 The Idempotency-Key rule, the error envelope and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the profile
    When they are compared with TSD P8 T-A.2 and T6.1
    Then POST /proceeds/{proceedsId}/match declares the Idempotency-Key header and its stored answer, and GET /proceeds declares none
    Then a repeated match of an already matched proceeds reference answers 409, an unknown proceedsId answers 404, and a missing or invalid field answers 422 with MSG-GEN-001
    Then a role without the Write-off and posting right R or U answers 403 with MSG-P4-002, and a downstream that does not answer inside 2 s answers 503
    Then the profile names the capability area Write-off and posting with right R on the read and right U on the match, and the scope filter applied to both

  Scenario: AC3 The Proceeds rental fields, the MatchRequest fields and the three lists are fixed and no business value is in the schema (new, D-RCV-60)
    Given the schema section of the profile
    When it is compared with TSD P8 T3.1 and T3.2
    Then Proceeds carries the treatment reference DF-FIN-003, the receipt reference DF-FIN-004, the source DF-FIN-005 against LOV-PROCEEDS-SRC, the amount DF-FIN-006, the received date DF-FIN-007, the match value DF-FIN-008 against LOV-MATCH and the posting reference DF-FIN-009
    Then MatchRequest carries the case reference, the treatment reference, the receipt reference, the amount, the received date and the match value, and every field of it that no source gives is Not specified in the source documents (GAP-2526; ASM-4178) and is marked so
    Then the payment_match_rule element is declared read-only over DF-REF-261 to DF-REF-273 with LOV-MATCH-TYPE carrying EXACT, WINDOW and PARTIAL
    Then the rental receipt is described as matched to INSTALLMENT and the profile records that LOV-MATCH holds no rental value (GAP-2528; ASM-4172)
    Then no window, grace, tolerance, floor, priority, amount or rule ID appears as a schema default, an example constant or an enumeration member of the code

  Scenario: AC4 The two rental event schemas are fixed on the payment topic with the CloudEvents envelope (new, D-RCV-60)
    Given the AsyncAPI fragment of the rental arm
    When it is compared with Architecture v5 slides 22, 42 and 43
    Then it declares rwb.payment.PaymentMissed.v1 and rwb.payment.ProceedsMatched.v1 on rwb.payment.events.v1 with the .retry and .dlt topics
    Then PaymentMissed keeps the published example fields caseId, treatmentId, dueDate, amountDue and daysLate, and adds no field that names a person
    Then ProceedsMatched carries the case reference, the proceeds reference, the treatment reference, the amount, the value date, the match value INSTALLMENT and the rule identity with its version, and the fields that no source gives are Not specified in the source documents (GAP-2526; ASM-4178)
    Then each message declares the CloudEvents 1.0 binary envelope with ce_specversion, ce_type, ce_source /rwb-payment, ce_id, ce_subject case/<caseId> and a W3C traceparent header, and the key caseId
    Then the profile declares no TreatmentBooked schema, because that member is RWB-P8-E4043-CON's
    Then the registry is BACKWARD and a change that removes or retypes a field is a new event type and not an edit in place

  Scenario: AC5 The proceeds template and its rental constraints are declared with no cross-schema key (new, D-RCV-60)
    Given the data section of the profile
    When it is compared with TSD P8 T3.1, T3.3 and the Ownership Map
    Then the profile declares the rental constraints of rwb_payment.proceeds over DF-FIN-001 to DF-FIN-009 with the standard record columns, and creates no table and no column
    Then case_id, treatment_id and account_payment_id are declared as identifiers and not as foreign keys, and no key, join or view leaves rwb_payment
    Then the profile declares no v_ace_* view and no grant on another rwb_* schema, and the boundary test fails a build that adds one
    Then the unique key of a receipt, the index of the match state and the constraint that a rental with no receipt writes no row are declared as constraints of the profile and not as business values

  Scenario: AC6 The five contract fakes answer the document (new, D-RCV-60)
    Given the fakes of the profile
    When each is compared with the operation, the element or the event it serves
    Then the rwb-treatment rental fake answers the rental "RT-2026-000701" of treatment "DIL-2026-000701" on case "RC-2026-000701", a treatment with no rental, and no answer beyond 2 s
    Then the rwb-source-data receipt fake answers the receipt "PAY-90701" of the business date 2026-12-15, a receipts set that holds no receipt, and a batch that is not complete with MSG-P1-001
    Then the rwb-case fake answers the case reference with its route state and an accepted and a refused money-side answer
    Then the rwb-decision package fake answers the package at its version in force for 2026-12-15
    Then the decision-record library stub answers a healthy write and a refused write with MSG-P7-003
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The compatibility rule, the profile boundary and the absence test are fixed (new, D-RCV-60)
    Given the compatibility and boundary sections of the profile
    When the nine sub-tables and the registry settings are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_payment, the login is rwb_payment, the topic is rwb.payment.events.v1, the queue is rwb-payment and the Java package is th.co.scb.ace.workbench.recovery.payment
    Then a schema change is additive within major version 1, and a breaking change is a new major version with a new event type
    Then every member that RWB-P8-E4043-CON declares is referenced as that document's and is not restated here
    Then the profile declares no Schedule, no Quartz row and no shared job table, and the rental arm is described as a step of the JOB-07 run started by AceDataReady
    Then the absence test fails a build that adds a v_ace_* view, another service's property, a monolith base, a second topic or a second workflow

  Scenario: AC8 Each business rule BR1 to BR12 of section 8 is traced to a criterion or a test (new, D-RCV-60)
    Given the twelve business rules BR1 to BR12 of section 8
    When each rule is traced to the criteria and tests of this story
    Then each of BR1 to BR12 names at least one criterion or test that exists in section 7 or section 16
    Then a rule that is an architecture constraint is tested by a guardrail or boundary test listed in section 16 or 17
```

These eight criteria are new for the contract profile and test the artefact only. They restate no business outcome owned by RWB-P8-E4048-APP and they copy no criterion of the legacy story, whose two criteria stay with the app story word for word (GAP-2527; ASM-4177).

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The receipt and its match are P8's: `proceeds` in `rwb_payment` carries the case, the treatment, the account payment, the source, the amount, the received date, `matched_to` and the posting reference, and the profile declares their shapes only | TSD P8 T3.1; Ownership Map (`proceeds` owner P8) | AC3; TC-P8-E4048-CON-02 |
| BR2 | The vocabulary is closed: `source` is one value of LOV-PROCEEDS-SRC, `matched_to` is one value of LOV-MATCH, `match_type` is one value of LOV-MATCH-TYPE, and the rental receipt closes to INSTALLMENT because no list value names a rental | TSD P8 T3.2; GAP-2528; ASM-4172 | AC3; TC-P8-E4048-CON-02 |
| BR3 | The decision record is declared as an element written in the transaction of the row, through the local library on the shared topic, and a failed write is MSG-P7-003 | DP-03; legacy RWB-E4-048 AC2, owned by the app story; ADR-022 | TC-P8-E4048-CON-07 |
| BR4 | No ACE view and no ACE table is read: the receipt and the account are consumed on rwb-source-data's contract and the service holds no `v_ace_*` grant | DP-05; Architecture v5 slide 29 | AC5; TC-P8-E4048-CON-04 |
| BR5 | The rental, its amount, its debit day and its arrears limit stay with rwb-treatment, which creates the rental record and sets the auto-debit under R-DIL-32 (FEAT-TRT-16); rwb-payment collects, matches and follows up the payment; the profile declares the rental read as consumed and declares no property of it; the arrears limit for the payment step is read from the rule package version in force announced on RulePackageInForce until rwb-decision names the package code | Ownership Map (treatment S2); FSD P8 A2.9 (prerequisite FEAT-TRT-16); GAP-2525; GAP-1382 | AC5, AC7; TC-P8-E4048-CON-04 |
| BR6 | The case stays with rwb-case and the package with rwb-decision: the profile declares the case answer and the package read as consumed and no property of them | DP-01; Ownership Map (recovery_case P3, rule_row P7) | AC5, AC7; TC-P8-E4048-CON-04 |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | TSD P8 T-A.2; Architecture v5 slide 11 | AC1, AC6; TC-P8-E4048-CON-01, TC-P8-E4048-CON-05 |
| BR8 | One REST base, one topic, one queue and one login per service, and the profile declares no member of another service's base or topic as its own | DP-13, DP-14; Template and Rules R4 | AC1; TC-P8-E4048-CON-01 |
| BR9 | A schema change is additive within major version 1; a breaking change is a new major version with a new event type | Architecture v5 slide 42 notes (BACKWARD) | AC4; TC-P8-E4048-CON-03 |
| BR10 | The events carry identifiers, amounts, dates and a rule version only, never a name, an address, a contact value or an identity number | Template and Rules R7.2 (s17); Architecture v5 slide 22 notes | AC4; TC-P8-E4048-CON-03 |
| BR11 | The base surface, the `Proceeds` element group and `TreatmentBooked` are RWB-P8-E4043-CON's; this profile adds the rental members and restates none | GAP-2527; ASM-4177 | AC5, AC7; TC-P8-E4048-CON-04 |
| BR12 | The rental arm is a step of the JOB-07 run started by `AceDataReady`; the profile declares no Schedule and no new workflow | Architecture v5 slide 44; GAP-2524; ASM-4174 | AC5, AC7; TC-P8-E4048-CON-04 |

### 9. State transitions

The lifecycle of this profile, not of a receipt:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the rental elements, the two event schemas and the fakes are described | In review |
| In review | Consumer sign-off | RWB-P8-E4048-APP, SCR-28, the wave 3 harness and the rwb-treatment, rwb-source-data, rwb-case and rwb-decision owners accept the profile and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A path, a property or a list value is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A duplicate of the base surface appears | X9 fires and the review names the owner document | In review |

The receipt state the profile describes is the app story's: `matched_to` is one value of LOV-MATCH, the rental receipt is INSTALLMENT, and a rental with no receipt has no row at all. This baseline fixes the vocabulary and moves no receipt.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-payment | Owns the profile, the AsyncAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the boundary between this profile and RWB-P8-E4043-CON |
| Consuming teams (the app story, SCR-28, the wave 3 harness and the owners of rwb-treatment, rwb-source-data, rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the outbox and inbox library and the record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element, an event payload or a fake |
| rwb-access (P4) | Owns the capability area and the rights the document names; the document declares them and grants none; each REST operation in §12.2 is checked by the rwb-access authorise check (DP-08) |

The per-service login behind the security scheme is named "the rwb-payment login" and is not part of this profile.

### 11. Data

The profile declares shapes, not business values. The rental amount, debit day and arrears threshold are read from the rwb-treatment rental terms and from reference data in force; no value is fixed in this profile or in code, and the value set is confirmed with the NPA and asset manager. The `ce_` names are CloudEvents envelope attributes and are not LDM v9 or Data Classification v5 fields (§12.3); `account_payment_id` is the field DF-FIN-004 of TSD P8 T3.1 and is not an LDM v9 or Data Classification v5 field.

| Item | Content | BR Field ID |
|---|---|---|
| Proceeds rental fields | DF-FIN-003 `treatment_id`, DF-FIN-004 `account_payment_id`, DF-FIN-005 `source`, DF-FIN-006 `amount`, DF-FIN-007 `received_date`, DF-FIN-008 `matched_to`, DF-FIN-009 `posting_ref` | DF-FIN-003 to DF-FIN-009 |
| standard record columns | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at` and `updated_by` of TSD P8 T3.0 | Not specified in the source documents (DOR-RWB-P8-E4048-CON-7) |
| Lists | LOV-MATCH (INSTALLMENT, SETTLEMENT, FEE, SALE_PROCEEDS, UNMATCHED), LOV-PROCEEDS-SRC (CUSTOMER, LED, AUCTION, BUYER, AGENCY, INSURER, GUARANTOR) and LOV-MATCH-TYPE (EXACT, WINDOW, PARTIAL) of TSD P8 T3.2, read under DP-06 and DP-07 | LOV-MATCH, LOV-PROCEEDS-SRC, LOV-MATCH-TYPE |
| `payment_match_rule` element | DF-REF-261 to DF-REF-273, read-only reference data of the service, read under DP-06 and DP-07; the parameter keys it reads in force are Not specified in the source documents (DOR-RWB-P8-E4048-CON-20) | DF-REF-261 to DF-REF-273 |
| MatchRequest rental fields | The fields the rental match needs, with the placeholder where no source gives them: Not specified in the source documents (GAP-2526; ASM-4178) | Not specified in the source documents (DOR-RWB-P8-E4048-CON-7) |
| PaymentMissed payload | The published example fields `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate` of Architecture v5 slide 22 | Not specified in the source documents (DOR-RWB-P8-E4048-CON-7) |
| ProceedsMatched payload | The identifiers and facts of the modelled row, with the fields no source gives carried as Not specified in the source documents (GAP-2526; ASM-4178) | Not specified in the source documents (DOR-RWB-P8-E4048-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written in the transaction of the row (DP-03) | DF-DEC-001 to DF-DEC-018 |
| Not declared here | `treatment` and the rental record (S2), `recovery_case` (P3), the `v_ace_*` views (P1) and `rule_row`, `rule_package_version` and `decision_log_entry` (P7): each is named as an answer or a rule version of its owner | None (not declared here) |

The field types, lengths and required flags of the added members are settled in the review; this story fixes the member names, the vocabulary of AC3 and the optionality rule of BR9. **No new table, no new column and no migration** is created by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-payment (P8); base `/api/recovery/payment/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | `ProceedsPage` out, filtered by `matched`, `from` and `to`, paginated by `page` and `size`, each item carrying the rental fields of DF-FIN-003 to DF-FIN-009 (API-P8-001) | Write-off and posting, right R, scope applied | Not applicable |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in with the rental fields, `Proceeds` out (API-P8-002) | Write-off and posting, right U, scope applied | `Idempotency-Key` header required; the answer is stored |

The two operations answer 400, 401, 403, 404, 409, 422 and 503, each with the error envelope and one message ID of section 14. The operation IDs, the base surface and the element groups are RWB-P8-E4043-CON's; this profile adds the rental members of AC3 and declares no third operation (GAP-2527; ASM-4177).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the profile |
|---|---|---|---|
| The rental read of the business date (name and fields Not specified in the source documents (GAP-2523; ASM-4173)) | `/api/recovery/treatment/v1` | S2 rwb-treatment | The rentals due on the business date: rental, treatment, case, rental amount, debit day and due date; faked |
| The receipt read of the ACE batch (name Not specified in the source documents (GAP-2524; ASM-4175)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The receipts of the business date for source `ALS`, the batch status and the freshness stamp; faked |
| The case read and money-side answer (name Not specified) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its route state and the answer that applies the money side; faked |
| The rule-package read (name Not specified) | `/api/recovery/decision/v1` | P7 rwb-decision | The package at its version in force for the business date; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C in fact and the plan's C row for this story is None, so the app story builds against these documents and fakes from Day 1 (GAP-2524; ASM-4175).

#### 12.3 Events published

Topic `rwb.payment.events.v1` with the `.retry` and `.dlt` topics, key `caseId`, CloudEvents 1.0 binary.

| Event | Schema name | Consumers | Payload element |
|---|---|---|---|
| `PaymentMissed` (EV-12) | `rwb.payment.PaymentMissed.v1` | rwb-case, rwb-treatment, rwb-comms | `caseId`, `treatmentId`, `dueDate`, `amountDue` and `daysLate`, as the published example of Architecture v5 slide 22; any further field is Not specified in the source documents (GAP-2526; ASM-4178) |
| `ProceedsMatched` (EV-25) | `rwb.payment.ProceedsMatched.v1` | rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff, rwb-guarantee | The case, proceeds and treatment references, the amount, the value date, the match value and the rule identity with its version; the remaining field list is Not specified in the source documents (GAP-2526; ASM-4178) |

Each message declares the CloudEvents 1.0 binary envelope with `ce_specversion`, `ce_type`, `ce_source` `/rwb-payment`, `ce_id`, `ce_subject` `case/<caseId>` and a W3C `traceparent` header, and the body is validated against the registry in BACKWARD mode. `TreatmentBooked` (EV-11) is RWB-P8-E4043-CON's and is not restated here. The `ce_` attributes are CloudEvents 1.0 envelope attributes carried in the message headers, not fields of LDM v9 or Data Classification v5.

#### 12.4 Events consumed

| Event | Topic | Owner (producer) | Consumer group | Payload used | When |
|---|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | rwb-source-data | `rwb-payment.rwb.source-data.events.v1` | Record key `{sourceSystem}:{businessDate}`; payload `sourceSystem`, `businessDate`, `status`, `completedAt` | Starts, only on `sourceSystem` `ALS` and `status` `COMPLETED`, the JOB-07 run the rental arm is a step of |
| `TreatmentApproved` (EV-10) | `rwb.treatment.events.v1` | rwb-treatment | `rwb-payment.rwb.treatment.events.v1` | The case, the treatment reference and the treatment type | Declared as consumed by the matching stories |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | rwb-decision | `rwb-payment.rwb.decision.events.v1` | The package code and the version in force | Declared as consumed by the matching stories |

`DecisionRecorded` (EV-08) is written by all nineteen services through the local library on the shared topic `rwb.decision-record.v1`; rwb-payment is a producer of that topic and not a consumer, so the profile declares no subscription or inbox row for it (DP-03).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The event-started workflow run (`PaymentMatchingWorkflow` in the matching story; the name is a target design choice) | Workflow, one execution per business date and source, started by `AceDataReady` with `sourceSystem` `ALS` and `status` `COMPLETED` | `rwb-payment` in `rwb-recovery` | The boundary the rental arm runs inside; not built here |
| `matchPayments` | Activity, the matching step | `rwb-payment` | The activity contract the profile serves: the rentals and the receipts in; the rule identity with its version, the match outcome, the record, the row and the outbox event out |
| The rental arm (a step of `matchPayments`; the name is a target design choice) | Activity step | `rwb-payment` | Declared only as a step of the run, with no workflow, child workflow or Nexus operation of its own |

The profile registers no workflow. The ownership rows of P8 hold no workflow of the service, and the rental arm is a step of the run that already exists (GAP-2524; ASM-4174).

#### 12.6 Schedules

None. JOB-07 and JOB-08 are event-triggered runs and not Temporal Schedules (Architecture v5 slide 44), the rental due date is a fact of the rental read, and the profile declares no Schedule, Quartz row or shared job table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | The receipt and its match; the table the two operations read and the match writes; the rental constraints of AC5 |
| `payment_match_rule` | P8 (`rwb_payment`) | The match rules read in force; declared read-only here, written by the matching-rule story |
| `decision_record` | PLT library, created in `rwb_payment` | The local record of the step (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_payment` | Outbox, inbox and idempotency objects (the library's, not a pattern of this key) |

`treatment` and the rental record are S2's, `recovery_case` is P3's, the `v_ace_*` views are P1's and `rule_row` and `rule_package_version` are P7's; the profile names them only as answers and rule versions, and no foreign key leaves `rwb_payment` (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-treatment rental fake | Rental `RT-2026-000701` of treatment `DIL-2026-000701` on case `RC-2026-000701` with its amount and due date 2026-12-15; a treatment with no rental; no answer beyond 2 s | AC1, AC3, AC6 |
| rwb-source-data receipt fake | Receipt `PAY-90701` of the business date 2026-12-15; a receipt 3 days after the due date; no receipt; a batch that is not complete with MSG-P1-001 | AC1, AC4, AC6 |
| rwb-case fake | The case reference with its route state; an accepted and a refused money-side answer | AC1, AC2, AC6 |
| rwb-decision package fake | The package at its version in force for 2026-12-15 | AC1, AC6 |
| Local record library stub (`RWB-PLT-E1027-CON`) | A healthy write and a refused write with MSG-P7-003 | AC2, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rental read, the receipt read, the case answer and the package read are derived from their owners' published documents and carry the placeholder until the owners confirm them (GAP-2523, GAP-2524; ASM-4173, ASM-4175).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two operations on `/api/recovery/payment/v1`; the rental, receipt, case and package rows; one hop, 2 s |
| Kafka | 2 published, 3 consumed | `PaymentMissed` and `ProceedsMatched` on `rwb.payment.events.v1`; `AceDataReady`, `TreatmentApproved` and `RulePackageInForce` through the shared service groups in section 12.4 |
| Temporal | 1 run boundary and 1 activity declared, 0 registered | The JOB-07 run on `rwb-payment` with `matchPayments`; the rental arm is a step; no Schedule |
| File | None | No file is read, built or delivered by this profile |

### 13. Solution plan

**The profile declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no receipt, no rental, no case and no package. What it publishes is one additive profile of the OpenAPI document, one AsyncAPI fragment with two schemas, nine contract tables and five fakes.

**Deliverables.** The additive profile of `openapi/rwb-payment-v1.yaml` for the rental arm, the rental members of `Proceeds` and `MatchRequest`, the read-only `payment_match_rule` element, the two JSON schemas with the CloudEvents envelope, the contract README rows for the four consumed rows and their placeholders, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: only rwb-source-data holds SELECT on the `recovery.v_ace_*` views (Architecture v5 slide 29), so the profile declares no ACE view and the `v_ace_payment` receipt of DF-ACE-043 to DF-ACE-054 is consumed on the owner's contract instead. DP-03 fixes the record element written in the transaction of the row; DP-13 keeps the base and adds nothing; DP-19 is behind SCR-28, whose screen model is the edge contract's. The outbox and inbox objects are library objects of the service template and are not a pattern of this key.

**Dependencies the table adds and the plan does not hold.** This is a CON story with no build dependency: it is Day 1 by rule (Template and Rules R5.7). The two H rows of DP-03 and DP-19 are the platform contracts it builds against, and the four consumed rows are class C in fact and are declared as consumed and faked (GAP-2524; ASM-4175).

**Build steps.** (1) The rental members of the two operations, AC1. (2) The error envelope, the rights and the `Idempotency-Key` rule, AC2. (3) The `Proceeds` and `MatchRequest` rental fields, the three lists and the read-only rule element, AC3. (4) The two event schemas with the envelope and the no-personal-data rule, AC4. (5) The rental constraints of the `proceeds` template and the no-cross-schema-key test, AC5. (6) The five fakes and the drift test, AC6. (7) The compatibility rule, the boundary to the base surface and the absence test, AC7.

**Done when.** The profile validates in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and the drift test is green, the two event schemas register in BACKWARD mode, and the app story, SCR-28 and the wave 3 harness have accepted the profile.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of `MatchRequest` is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written in the transaction of the row | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch | {product} is from {date}. Today's load has not arrived. |
| MSG-P8-002 | No `payment_match_rule` row is in force on the business date | Not specified in the source documents (GAP-2522; ASM-4179) |

The message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new identifier is invented. MSG-P1-001 and MSG-P8-002 are carried because they are in the message set of this feature and are raised by the app story, not by this baseline.

### 15. Screens and states

The profile serves SCR-28 Proceeds matching in its Loading, matched and unmatched states through the gateway-bff composite route (DP-19). Its empty, error and no access states are Not specified in the source documents (CG-ALL-7749). The route calls rwb-payment for `GET /proceeds` and `POST /proceeds/{proceedsId}/match`, rwb-case for the case and its route state and rwb-treatment for the rental; this profile fixes the rwb-payment answers only, and the composite route, the field list and the merge order belong to RWB-PLT-N001-CON. The refusal and failure states the screen shows - refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001 - read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E4048-CON-01 | AC1, AC2 | Contract | The profile validates; the two operations, the base, the rental answers, the errors and the `Idempotency-Key` rule are present, and no monolith base is declared |
| TC-P8-E4048-CON-02 | AC3 | Contract | The rental fields of `Proceeds` and `MatchRequest` validate against DF-FIN-003 to DF-FIN-009 and the three lists, and no window, tolerance, amount or rule ID appears as a default or a constant |
| TC-P8-E4048-CON-03 | AC4 | Contract | The two event schemas validate with the envelope, `ce_source` `/rwb-payment`, key `caseId`, the published `PaymentMissed` example and no personal data; a removed field is refused in BACKWARD mode |
| TC-P8-E4048-CON-04 | AC5, AC7 | Contract | The rental constraints of `rwb_payment.proceeds` declare no cross-schema key, no `v_ace_*` read, no Schedule and no duplicate of the base surface, and a forbidden element fails the absence test |
| TC-P8-E4048-CON-05 | AC6 | Contract | The five fakes answer every consumed path; a drifted fake fails the build; a repeated POST with the same `Idempotency-Key` returns the stored answer |
| TC-P8-E4048-CON-06 | AC5 | Contract | Boundary: each table of §12.7 is declared with its owner, `proceeds` and `payment_match_rule` as P8 and the library tables as PLT; a table owned outside `rwb_payment` or not listed in §12.7 fails the test, and no foreign key leaves `rwb_payment` |
| TC-P8-E4048-CON-07 | BR3 | Contract | The `decision_record` element is declared as written in the transaction of the row through the local library on `rwb.decision-record.v1`; no subscription or inbox row is declared for `DecisionRecorded`; a failed write maps to MSG-P7-003 |
| TC-P8-E4048-CON-08 | §11 | Contract | The DDL template declares no new table, no new column and no migration for this profile; legacy TC-E4-048-01 to TC-E4-048-04 are referenced as owned by RWB-P8-E4048-APP and are not restated |
| TC-P8-E4048-CON-09 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-P8-E4048-CON-AC8) |

Legacy test cases TC-E4-048-01 to TC-E4-048-04 are owned by RWB-P8-E4048-APP, which also carries the Access and Principle 5 cases. The nine cases above are new contract cases; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the rental amount, the debit day, the arrears limit, the window, the grace, the tolerance, the floor, the priority and the rule IDs stay rows of the rental read or of `payment_match_rule`, never a schema default, an example constant or an enumeration member of the code.
- No personal data in a schema, an example, an event payload or a fake: identifiers, amounts, dates, list values and a rule version only, and every example is synthetic.
- ACE data only through the owner's contract: the service holds no `v_ace_*` grant, so the profile declares no ACE view and no ACE table (DP-05; Architecture v5 slide 29).
- The rental stays with rwb-treatment, the case with rwb-case, the package with rwb-decision and the rights with rwb-access: the profile declares none of their properties and writes none of their rows (DP-01).
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and a document that names another service's base or topic as its own fails the review (DP-13).
- The profile lists only operations owned by rwb-payment, and every member of the base surface stays RWB-P8-E4043-CON's; a duplicate fails X9 and the drift test (BR11).
- No Schedule, Quartz row or shared job table is declared, and the rental arm is a step of the event-started run (BR12).
- The error envelope, the `Idempotency-Key` rule, the naming rule and the record library come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| FEAT-PAY-09 | The rental is taken by auto-debit, the receipt is issued and the arrears are followed up (FSD P8 A2.9 and AC-P8-009-01); the legacy story master carries no requirement id (GAP-2522; ASM-4172) | The two operations with the rental fields and the two event schemas | TC-P8-E4048-CON-01, TC-P8-E4048-CON-03 |
| BR-P8-009 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.9.3.1) | The three lists as published enumerations and the read-only rule element | TC-P8-E4048-CON-02 |
| VR-P8-009-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.9.3.1) | The freshness row of the consumed receipt contract and the message of section 14 | TC-P8-E4048-CON-01 |
| ADR-014 | Schema and login per service | The rental constraints of the `proceeds` template and the no-cross-schema-key rule | TC-P8-E4048-CON-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The two schemas with the envelope and the BACKWARD registry rule | TC-P8-E4048-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-P8-E4048-CON-01 |
| ADR-022 | Local decision record plus central ledger | The record element written in the transaction of the row | TC-P8-E4048-CON-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-048, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-P8-E4048-APP; this profile copies none of them |
| Test cases | The five new contract cases TC-P8-E4048-CON-01 to -05; the four legacy cases belong to the app story |
| Feature and screens | FEAT-PAY-09 Run the deed in lieu rental auto-debit; SCR-28 Proceeds matching |
| Rules | R-DIL-32 and R-DIL-34 of the deed in lieu route set, evaluated in rwb-treatment; the rental match rules are rows of `payment_match_rule`, and their rule code is Not specified in the source documents (GAP-2524; ASM-4181) |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two operations, the rental arm of JOB-07, the record, the `proceeds` row and the publication: RWB-P8-E4048-APP.
- The rental record, its amount and debit day, the auto-debit instruction to ATS and AMIS and the arrears limit: rwb-treatment (S2, FEAT-TRT-16, R-DIL-32, R-DIL-34).
- The ACE receipts, the account facts, the batch status and the freshness of the data product: rwb-source-data (P1).
- The case, its route state, the owner's task and the timer: rwb-case (P3).
- The package, its rows and its version: rwb-decision (P7).
- The rights, the roles and the scope check: rwb-access (P4).
- The base surface, the `Proceeds` element group and `TreatmentBooked`: RWB-P8-E4043-CON.
- The settlement, auction and enforcement arms of the matching: RWB-P8-E4043-APP and RWB-P8-E4044-APP.
- The exception list of a receipt that matches no rental and the plan-installment matching: FEAT-PAY-02's story and RWB-P8-E2008-APP.
- The creation of the `proceeds` table and its migration: the DB story of this service, whose template this profile constrains.
- The gateway-bff composite route and the screen field list of SCR-28: RWB-PLT-N001-CON.
- The posting to ALS and to the general ledger and the posting file: the posting stories of this service.
- The deployment, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
- The cross-service journey of the key and its evidence: the wave 3 harness.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E4048-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

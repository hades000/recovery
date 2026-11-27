# RWB-P8-E2027-CON Payment matching rules with the data team - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E2027-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P8-E2027-CON-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W2 |
| PAYMENT_MATCH version label | PMT-2026.12 (legacy key value; valid-from date as recorded in GAP-1297); one reconciliation with the owner of RWB-E2-027 before SIT (GAP-1297) |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version fixed | REST: API Specification v5, `/v1` paths; events: Kafka Topic and Event Catalog v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FR-P8-001, FR-P8-002, FR-P8-004, FR-P8-006, FR-P8-007, FR-P8-010, FR-P8-011, FR-P8-012, FR-P8-013, FR-P8-015, FR-P8-016, FR-P8-017, FR-P8-027, FR-P8-028, FR-P8-032); FSD feature IDs FEAT-PAY-01 to FEAT-PAY-11; FSD requirement ID Not specified in the source documents (GAP-1624) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 28 cross-document, 9 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of rwb-payment for the payment-matching key — the rule-evaluation result this service consumes from rwb-decision with the package code, the version in force, the rule ID, the row order and the outputs, the local decision-record envelope on `rwb.decision-record.v1`, the three event schemas of `rwb.payment.events.v1`, `GET /proceeds` and `POST /proceeds/{proceedsId}/match` with their `Idempotency-Key` rule and RFC 9457 problem responses, and the rule that every match records the package version in force with no breaking change without a new version — with the fakes that answer them**, so that **RWB-P8-E2027-APP, the screen route of SCR-28, rwb-decision and the wave 2 harness build against one frozen, testable surface on Day 1 and a field, an event type, a version label or an error shape can never drift between them without a failing build**.

This story publishes the contract only. It writes no code, no migration and no table, it matches no payment, and it moves nothing.

The contract sits on the naming the service already has (Arch v5 slide 41 notes; Template and Rules §R4): schema `rwb_payment`, login per service, REST base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1` with its `.retry` and `.dlt` topics, event names `rwb.payment.<Event>.v1`, Temporal task queue `rwb-payment` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.payment`. The shared topic `rwb.decision-record.v1` is the platform library's.

The legacy acceptance criteria AC1 to AC10 of RWB-E2-027 are **not** copied here. AC6, AC7 and AC10 are owned word for word by RWB-P8-E2027-APP, AC1, AC2, AC4, AC5, AC8 and AC9 by RWB-P8-E2008-APP, and AC3 by RWB-P7-E2027-APP; every criterion of section 7 is new under D-RCV-60 and tests only the contract deliverable in this title.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and embedded Drools per service with the rule registry in rwb-decision is its companion (ADR-017, DP-04). Both only work if two things are fixed before any code: the shape of the rule answer this service receives from another team's service, and the shape of the money answer this service gives to the rest of the platform. Without the first, rwb-payment would invent its own reading of the rule result and the package version on a record would stop being comparable across services; without the second, rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee would each parse `ProceedsMatched` in their own way.

The baseline therefore fixes four surfaces and one rule.

- **The rule answer.** `rwb-decision` publishes an evaluation result for a package code and a business date. The Temporal and Drools design names it as `RuleResult(packageCode, packageVersion, ruleId, outputs)`; this baseline adds the row order the matching key needs and reads the version field as the version in force, and marks both as the working read until rwb-decision publishes its own schema (GAP-2507; ASM-4153). The row order is what makes the first-match rule testable at the contract level without any business threshold in the document.
- **The record.** The local decision record is the platform library's (DP-03): a match writes it in the same transaction as the `proceeds` row and publishes `DecisionRecorded` on the shared topic. This baseline declares the envelope and the fields the matching record carries and declares no topic of its own for it.
- **The events.** `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25) are produced by this service on `rwb.payment.events.v1` (Arch v5 slides 42 and 43; slide 17). TSD P8 v2 T5.3 gives their names and direction and no payload, so the payload field lists are published here from the legacy facts and marked (GAP-2507; ASM-4155).
- **The two operations.** `GET /proceeds` (API-P8-001) and `POST /proceeds/{proceedsId}/match` (API-P8-002) are this service's, with the rights of TSD P8 T6.1, the `Idempotency-Key` rule of the second and the problem response of the platform.
- **One rule about change.** The package version in force is recorded on every match, and no consumer of the result may see a breaking change without a new version and a new registry row. That is what makes a match explainable a year later.

The baseline also records what it does not own. The registry, the governance of a version, the load checks, the four-eyes approval and the 00:01 promotion are rwb-decision's (RWB-P7-E2027-APP). The workbook is rwb-case's (RWB-P3-E2042-APP). The money is matched and written here, and the case, the balance, the posting and the ledger are not.

### 3. Preconditions

- The service naming rule is in force (RWB-PLT-E1047-CON), so the base, the topic, the retry topic, the `.dlt` topic, the queue and the event names follow the platform rule rather than a local choice (DP-13, DP-14).
- The platform error envelope, the pagination convention and the `Idempotency-Key` rule are the platform baseline (Arch v5 slide 11; RWB-PLT-N009-CON); where this document narrows them it does so explicitly.
- The ownership of every object is taken from the Ownership Map only: `proceeds` is P8's, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's, `treatment` is S2's, `recovery_case` is P3's and `decision_record` is a PLT library object created in each schema.
- The rule registry answers as `RWB-P7-E2027-APP` and `RWB-P7-E1073-CON` describe it; the model fetch and the checksum are named in the Temporal and Drools design (slide 15 notes) and are fixed here as consumed rows.
- The local decision-record library and the shared topic are `RWB-PLT-E1027-CON`; this baseline declares the envelope as consumed and adds no second writer.
- The event catalogue is `Arch v5` slides 42 and 43: `TreatmentBooked` is row 11, `PaymentMissed` is row 12 and `ProceedsMatched` is row 25, and `DecisionRecorded` is row 08 on the shared topic whose consumers the catalogue lists as rwb-decision and rwb-reporting. The key's service conventions list `DecisionRecorded` as consumed here; the difference is recorded and read as a ledger acknowledgement of this service's own record (GAP-2507; ASM-4154).
- The rule-evaluation result has no published schema and the operation names of the version-in-force lookup and of the treatment installment-paid call are not given by any source; both carry the placeholder (GAP-2507; ASM-4153).
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-payment for this key: the two operations of 12.1 with their query, their request and answer elements and their seven error responses, under the base `/api/recovery/payment/v1`.
2. Fix the `Proceeds` element from the `proceeds` columns of DF-FIN-001 to DF-FIN-009, with the match outcome on `matched_to`, `source`, `amount`, `received_date` and `posting_ref`, and no property added for a threshold, a rule row or a case state.
3. Fix the consumed rule-evaluation result: the package code, the version in force, the rule ID, the row order and the outputs, with the two fields the sources do not name marked with the placeholder. The match rows stay in the PAYMENT_MATCH rule package, with no payment_match_rule table in any service schema, and are loaded through the rule package endpoints (GAP-3179). The row order is EXACT, then PARTIAL, then WINDOW, then the accepted recommendation (GAP-3180).
4. Fix the local decision-record envelope on `rwb.decision-record.v1`: the record fields a match carries, the transaction rule and the hash chain, declared as the library's and not as this service's own event.
5. Fix the three event schemas of `rwb.payment.events.v1`: the CloudEvents attribute set, the `ce_type` of each, the key `caseId`, the payload field list and the rule that the payload carries identifiers and facts only.
6. Fix the `Idempotency-Key` rule of the manual match, the seven error responses and the rights of the two operations against TSD P8 T6.1.
7. Publish the five contract fakes of 12.8 and the drift test that compares each fake with the document.
8. Tag the baseline and hand it to RWB-P8-E2027-APP, the screen route of SCR-28 and the wave 2 harness; rwb-decision and rwb-treatment consume it as the answer they must give.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or answer body fails schema validation | The schema lint fails the build; a deployed service answers 400 or 500 with the problem envelope | MSG-GEN-001 | AC4, AC5 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version and a new `ce_type` for an event | None | AC6 |
| X3 | A fake drifts from the document | The drift test fails the build and blocks the merge | None | AC6 |
| X4 | A field of the rule-evaluation result, of the record envelope or of an event payload is not given by any source | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC1, AC2, AC3 |
| X5 | A business threshold, a match type or a version label appears as an enumeration member or a default in the document | The vocabulary test fails the build; the values are rule-row data and registry rows | None | AC1, AC6 |
| X6 | The document declares another service's table as owned, adds a `v_ace_*` read it may not have, or names a second topic for the record | The boundary test fails the build | None | AC2, AC6 |
| X7 | A manual match is repeated with the same `Idempotency-Key` | The stored answer is returned and no second effect is described | None | AC5 |
| X8 | The rights of an operation are not the ones TSD P8 T-A.2 declares | The access test fails the build | MSG-P4-002 | AC4, AC5 |
| X9 | A published event body does not match the accepted schema version | The registry refuses the body in BACKWARD mode and the producing build fails | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map, the Architecture v5 catalogue and the published contracts of rwb-decision and rwb-treatment only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fixture set are settled in the baseline review; the base, the topic, the queue, the two paths, the rights and the event types are fixed by the target architecture |
| Valuable | Unblocks the app story, the screen route of SCR-28, the wave 2 harness and the rwb-decision and rwb-treatment teams on Day 1 |
| Estimable | One OpenAPI document, one AsyncAPI fragment, the nine contract tables, five fakes and a drift test |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of rwb-payment for the payment matching key

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of proceeds is P8, of rule_package and rule_row is P7 and of treatment is S2
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The consumed rule-evaluation result is declared with the package code, the version in force, the rule ID, the row order and the outputs (new, D-RCV-60)
    Given the declaration of the rule-evaluation result in the contract document
    When it is validated against the schema lint of the pipeline
    Then it declares the result as the answer of rwb-decision (P7) with packageCode, versionInForce, ruleId, rowOrder and outputs, and with the rule ID and the row order of the fired row only
    Then the version field is declared as the version in force on the requested business date and not as a caller argument
    Then outputs is declared as the named output columns of the fired row and carries no free-form text and no payment or customer field
    Then the result declares the NoPackageInForce outcome and no default row, no default version and no fallback result
    Then no business threshold, no match type and no version label appears in the document as an enumeration member, a default or an example constant
    Then the field names the sources do not give are Not specified in the source documents (GAP-2507; ASM-4153) and the document marks them so
    Then the result declares one hop with a 2 s budget and a breaker and no retry of its own (DP-11)

  Scenario: AC2 The local decision-record envelope is declared on rwb.decision-record.v1 and written before the row (new, D-RCV-60)
    Given the decision-record section of the baseline
    When it is compared with RWB-PLT-E1027-CON and with DP-03
    Then one record is declared per match with the entry ID, the case reference, the decision code D5, the rule ID, the rule version, the inputs reference, the final call, the decided-at time, the chain sequence, the previous hash, the entry hash and the actor reference
    Then the record is declared as written through the local library in the caller's transaction, before the proceeds row, and a failed write leaves the match unmade with MSG-P7-003
    Then the envelope is declared as CloudEvents 1.0 binary mode on the shared topic rwb.decision-record.v1 with the type of EV-08, and this service declares no topic of its own for the record
    Then the record carries identifiers, codes, an amount, a date and a rule version only, and no personal data
    Then the document declares no write of decision_log_entry and no read of any registry table

  Scenario: AC3 The three event schemas of rwb.payment.events.v1 are fixed (new, D-RCV-60)
    Given the event section of the baseline
    When one body of each type is validated against the registry in BACKWARD mode
    Then TreatmentBooked is declared as rwb.payment.TreatmentBooked.v1 (EV-11), PaymentMissed as rwb.payment.PaymentMissed.v1 (EV-12) and ProceedsMatched as rwb.payment.ProceedsMatched.v1 (EV-25), each on rwb.payment.events.v1
    Then each envelope declares CloudEvents 1.0 binary mode with ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject, ce_time and the trace header, keyed by caseId
    Then ProceedsMatched carries the case, the proceeds, the payment code, the treatment, the source, the amount, the matched-to, the rule ID, the rule version and the received date
    Then PaymentMissed carries the case, the treatment, the due date, the amount due and the business date, and TreatmentBooked carries the case, the treatment, the booking reference, the amount and the booking date
    Then every payload carries identifiers, codes, amounts and dates only and no name, e-mail address, mobile number, national identity number or account number
    Then the field lists the sources do not give are marked with the placeholder (GAP-2507; ASM-4155)
    Then the .retry topic and the .dlt topic are declared for the topic and the producer writes to its outbox in the same transaction as the state change

  Scenario: AC4 GET /proceeds is declared with its query, its answer and its right (new, D-RCV-60)
    Given the provided operations of the baseline
    When they are compared with TSD P8 T-A.1 and T-A.2
    Then GET /api/recovery/payment/v1/proceeds is declared with the query matched, from, to, page and size and the answer ProceedsPage (API-P8-001)
    Then the Proceeds element carries the nine proceeds fields of DF-FIN-001 to DF-FIN-009 and the rule ID and rule version of its decision record, and no case state and no balance
    Then the operation declares Write-off and posting R with the scope applied, and answers 401, 403 with MSG-P4-002, 409 and 503 as RFC 9457 problem responses with messageId
    Then the document declares no second list operation for the same receipts and no read of another service's table

  Scenario: AC5 POST /proceeds/{proceedsId}/match is declared with its Idempotency-Key rule, its errors and its right (new, D-RCV-60)
    Given the manual match section of the baseline
    When it is compared with TSD P8 T-A.2 and T6.1
    Then POST /api/recovery/payment/v1/proceeds/{proceedsId}/match is declared with a MatchRequest in and a Proceeds answer out (API-P8-002)
    Then the operation requires the Idempotency-Key header, stores its answer and returns the stored answer on a repeat without a second effect
    Then it declares Write-off and posting U with the scope applied and answers 401, 403 with MSG-P4-002, 404 for an unknown proceeds, 409 for a receipt already matched, 422 with MSG-GEN-001 and 503, each as one problem response with one message ID
    Then the document names the behaviour behind the operation as the Epic 4 story of this service and declares no rule evaluation of its own for it
    Then the request element carries the case reference, the account reference and the match target only, and no personal field

  Scenario: AC6 The version in force is recorded on every match and no breaking change is made without a new version (new, D-RCV-60)
    Given the versioning section of the baseline and the published fakes
    When the document and the five fakes are compared
    Then the rule-evaluation result, the record, the three event payloads and the Proceeds answer all carry the version in force, and a match without it is declared invalid
    Then an additive change within major version 1 keeps the version and is accepted by the registry in BACKWARD mode, and a breaking change raises a new major version and a new ce_type
    Then the document declares that a new rule package version needs a new registry row in rwb-decision and no redefinition of the result shape
    Then the rwb-decision registry fake answers the version list, the model fetch with its checksum, the refused schema check of "PM-2027.02" and NoPackageInForce for 2027-02-01
    Then the treatment fake answers the installment-paid call and its refusal, and the rwb-access fake answers a session with and without the right
    Then the drift test compares every fake with the document and fails the build on any difference, and a fake that adds a threshold or a match type fails the vocabulary test

  Scenario: AC7 Each business rule of section 8 is checked against the contract as a boundary test (new, D-RCV-60)
    Given the business rules BR1 to BR12 of section 8 and the contract artefact
    When each rule is compared with the declared operations, events, schemas, grants, tables, topics and LOV rows
    Then the contract declares the two operations, the three events, the record envelope and the consumed result only (BR1), and the consumed result carries the version in force from the registry (BR2)
    Then the record is written on rwb.decision-record.v1 before the proceeds row with no second writer registered (BR3), and the three events are on rwb.payment.events.v1 with the .retry and .dlt topics (BR4)
    Then Idempotency-Key is declared on each POST and on no GET (BR5), the rights are those of TSD P8 T6.1 (BR6), and the LOV rows are read through DP-07 (BR7)
    Then no tolerance, window, grace, partial floor or row order is a schema default or example constant (BR8), and the version in force is recorded on every match (BR9)
    Then no v_ace_* grant, foreign proceeds property or registry table is declared (BR10), one base, topic, queue and login per service is declared (BR11), and no personal data appears in a schema, example or fake (BR12)
```

These seven criteria are new for the contract baseline and test the artefact only. They copy no criterion of RWB-E2-027 and restate no business outcome owned by RWB-P8-E2027-APP: the three legacy criteria of the matching rules stay with the app story, the ten of the exact and exception behaviour with RWB-P8-E2008-APP and RWB-P7-E2027-APP, and the end-to-end journey with the wave 2 harness.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract declares the two operations, the three event types, the record envelope and the consumed rule-evaluation result, and nothing else | Architecture v5 slide 17 and 41; TSD P8 v2 T-A.1; Ownership Map |
| BR2 | The rule-evaluation result is declared as consumed from rwb-decision and carries the package code, the version in force, the rule ID, the row order (named priority in TSD P8 v2 T3.1, field DF-REF-270) and the outputs; the version in force is the registry's answer and never a caller argument | DP-04; Temporal and Drools slide 16; GAP-2507; GAP-1356 |
| BR3 | The record is the platform library's on `rwb.decision-record.v1`, written in the caller's transaction before the proceeds row; a failed write leaves the match unmade; DecisionRecorded is read here only for the ledger acknowledgement of a local record and no second writer is registered | DP-03; legacy BR8; R-UNI-39; GAP-1358 |
| BR4 | `TreatmentBooked`, `PaymentMissed` and `ProceedsMatched` are published on `rwb.payment.events.v1` in CloudEvents 1.0 keyed by `caseId`, with the `.retry` and `.dlt` topics, and carry identifiers and facts only | DP-14; Architecture v5 slides 42 and 43; slide 17 |
| BR5 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD P8 T-A.2 |
| BR6 | The rights are those of TSD P8 T6.1: Write-off and posting R for the read and U for the manual match, each with the scope applied | TSD P8 v2 T-A.2 and T6.1; RWB-E2-027 section 10 |
| BR7 | The vocabulary is closed: LOV-MATCH, LOV-MATCH-TYPE and LOV-PROCEEDS-SRC are reference rows read through DP-07 and are never enumeration members of the document or constants of the code; the three LOV-MATCH-TYPE codes are the match type column of package PAYMENT_MATCH, held by rwb-decision (P7) and read by rwb-payment (P8) | TSD P8 v2 T3.2; DP-07; legacy BR10; GAP-0218 |
| BR8 | No business value in the contract: the tolerance, the window, the grace, the partial floor and the row order are columns of the PAYMENT_MATCH rows and registry rows, never schema defaults or example constants | D-RCV-36 T10; legacy BR10; Template and Rules §R7.2 s17 |
| BR9 | The version in force is recorded on every match, and a breaking change to a published element raises a new major version and a new `ce_type`; a new rule package version needs a new registry row | Architecture v5 slide 42 notes (BACKWARD compatibility); ADR-017; D-RCV-36 T7 |
| BR10 | The document declares no `v_ace_*` grant it may not hold, no `proceeds` property of another owner and no registry table; every consumed read is a published operation or a view of this service | DP-01, DP-05; Architecture v5 slide 41 |
| BR11 | One base, one topic, one queue and one login per service; the document never declares another service's base, topic or queue as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates, a rule ID and a version label only | Architecture v5 slide 42 notes; Template and Rules §R7.2 s17 |

### 9. State transitions

This document has a lifecycle, not a business state machine.

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three event types, the record envelope and the consumed result are described | In review |
| In review | Consumer sign-off | RWB-P8-E2027-APP, the SCR-28 route, the wave 2 harness and the rwb-decision and rwb-treatment owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or an event type or a required field changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The boundary test of AC2 and AC6 fails: a registry table, a second topic or a business constant | In review |

The `proceeds` row states this contract describes — matched to INSTALLMENT, matched to another target, or UNMATCHED with its reason — are the app story's. The package version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED are rwb-decision's and are named here only as the value the version field carries.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-payment | Owns the OpenAPI document, the AsyncAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of an Ownership Map row the baseline consumes |
| Consuming teams (the app story, the SCR-28 route, the wave 2 harness, the owners of rwb-decision, rwb-treatment, rwb-case, rwb-access, rwb-source-data and rwb-reporting) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |
| RW-CREDITAD, Credit Administration officer | Confirms the read surface of SCR-28: the matched and unmatched receipts with the rule and the version that decided each one |

Each operation's authorise check is the rwb-access check under DP-08. This document declares no rwb-access path, none being given in the source documents (DOR-RWB-P8-E2027-CON-6), and declares no authorisation logic of its own.

No person is named in the document, an example or a fake. The rwb-payment login is named "the rwb-payment login (DP-02)" and its secret is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| `Proceeds` element | The columns of DF-FIN-001 to DF-FIN-009: `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to` and `posting_ref`; plus the rule ID and the rule version read from the record of the match |
| Consumed rule-evaluation result | `packageCode`, `versionInForce`, `ruleId`, `rowOrder` and `outputs`; the two names the sources do not give are Not specified in the source documents (GAP-2507; ASM-4153) |
| Decision record | DF-DEC-001 to DF-DEC-031 through the local library, written before the row (DP-03) |
| Events | The three payloads of 12.3 with identifiers, codes, amounts and dates only |
| Registry tables | `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's and are named as reached only through the operations of 12.2; no field of them is declared here |
| ACE facts | `v_ace_payment` and `v_ace_account` are read by this service under DP-05; the document declares no foreign key, no copy and no cross-schema read |
| Not written here | `recovery_case` (P3), `treatment` (S2), `decision_log_entry` (P7) and `asset` or `debtsale` tables (S5, S6) |
| Reference data read | The LOV-MATCH, LOV-MATCH-TYPE and LOV-PROCEEDS-SRC rows read through DP-07, and the PAYMENT_MATCH and registry rows whose tolerance, window, grace, partial floor and row order are read through DP-06; the parameter catalogue key is Not specified in the source documents (DOR-RWB-P8-E2027-CON-20) |

No new table, no new column and no migration is declared by this story. `payment_match_rule` and DF-REF-261 to DF-REF-273 are retired and appear in the document only as the assertion that no shape may recreate them (D-RCV-36 T10).

The BR Field ID of each of the seven data rows above is Not specified in the source documents (DOR-RWB-P8-E2027-CON-7).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-payment` (P8); base `/api/recovery/payment/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/proceeds` | Query `matched`, `from`, `to`, `page`, `size`; `ProceedsPage` of status 200 out (API-P8-001) | Write-off and posting R, scope applied | Not applicable, read only |
| POST | `/proceeds/{proceedsId}/match` | `MatchRequest` in, `Proceeds` of status 200 out (API-P8-002); the behaviour is the Epic 4 story RWB-P8-E4043-APP | Write-off and posting U, scope applied | `Idempotency-Key` header required; the answer is stored |

The `Proceeds` element carries `id`, `caseId`, `treatmentId`, `accountPaymentId`, `source`, `amount`, `receivedDate`, `matchedTo`, `postingRef`, `ruleId` and `ruleVersion`. Errors: 401 no session (Not specified in the source documents (CG-ALL-7587)); 403 the role lacks the right (MSG-P4-002); 404 an unknown proceeds or an unknown case reference (Not specified in the source documents (CG-ALL-7587)); 409 the receipt is already matched or the version changed at commit (MSG-GEN-004); 422 a required field is invalid (MSG-GEN-001); 503 a downstream or the record library does not answer (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set. The service's other operation `GET /cases/{caseId}/payments` is the first API path of the service on Arch v5 slide 41 and belongs to another key of this service; it is not declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the document |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The version in force on the business date and its checksum; the document fixes the fields it reads, not the operation |
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{version}` | P7 rwb-decision | The model of the version in force and its checksum, fetched once per version (DP-04; Temporal and Drools slide 15 notes) |
| The version-in-force evaluation read (operation name Not specified in the source documents (GAP-2507; ASM-4153)) | `/api/recovery/decision/v1` | P7 rwb-decision | The shape of the consumed rule-evaluation result of AC1; the document declares it as the answer rwb-decision publishes |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The parameters of the run, through the client library (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-MATCH, LOV-MATCH-TYPE and LOV-PROCEEDS-SRC (DP-07) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, the scope and the Write-off and posting right behind the two operations of 12.1 |
| POST | The installment-paid operation of rwb-treatment (operation name Not specified in the source documents (GAP-2507; ASM-4153)) | S2 rwb-treatment | The installment paid and the shortfall of a PARTIAL match, declared as consumed and faked |

Every row is one hop with a 2 s budget and a breaker (DP-11, ADR-020). The two rwb-decision registry operations and the evaluation result are class-C contract dependencies of DP-04 (`RWB-P7-E1073-CON`) and of the registry story, and this document's contract-dependency row is None; the absence is recorded in GAP-2507 and ASM-4152.

#### 12.3 Events published

| Event | Topic | Key | Payload (IDs and facts only) |
|---|---|---|---|
| `rwb.payment.TreatmentBooked.v1` (EV-11) | `rwb.payment.events.v1` | caseId | treatment ID (`treatmentid`), booking reference (`bookingref`), business date (`businessdate`) |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | caseId | treatment ID (`treatmentid`), due date (`duedate`), amount due (`amountdue`) |
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | caseId | case ID (`caseid`), proceeds ID (`proceedsid`), amount (`amount`) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | caseId | entry ID, decision code D5, rule ID, rule version, inputs reference, final call, decided at |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | `rwb.payment.<Event>.v1` for the three catalogue events; `rwb.decision.DecisionRecorded.v1` for the record |
| ce_source | `/rwb-payment` |
| ce_subject | The case ID |
| ce_id and traceparent | The event identifier and the W3C trace context of the run |
| Payload | Identifiers, codes, amounts and dates only; no personal data and no free text |

The three catalogue events are rows 11, 12 and 25 of the Arch v5 event catalogue; the record is the platform library's on the shared topic and is not an event of this service (DP-03). The `.retry` and `.dlt` topics are part of the topic of the service and are provisioned by RWB-P8-E2027-OPS. The exact payload schema beyond the fields listed, and the `ce_subject` format for a receipt with no open case, are Not specified in the source documents (GAP-2507; ASM-4155). The envelope attributes `ce_specversion`, `ce_type`, `ce_source`, `ce_subject` and `ce_id` are CloudEvents 1.0 attribute names declared in the envelope table above, not dictionary fields.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the document |
|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1` | P1 rwb-source-data | Starts the JOB-07 workflow and fixes the business date (DP-10) |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | Refreshes the running plans and their installments |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | Announces the version to fetch, verify and swap in |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared) | all 19 services | Read as the ledger acknowledgement of a local record; the catalogue lists rwb-decision and rwb-reporting as its consumers (GAP-2507; ASM-4154) |
| `rwb.debtsale.LotAwarded.v1` (EV-23) | `rwb.debtsale.events.v1` | S6 rwb-debtsale | Names the lot a debt-sale receipt belongs to |
| `rwb.asset.AssetSold.v1` | `rwb.asset.events.v1` | S5 rwb-asset | Names the asset sale a receipt belongs to |

The document fixes the envelope of each consumed event as the producer declares it and adds no field. The consumer dedupes every event through the inbox on its ID, so a repeated `AceDataReady` starts no second run and a repeated `RulePackageInForce` performs no second swap.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| JOB-07 payment matching | Event-started workflow, started by `AceDataReady` | `rwb-payment` in namespace `rwb-recovery` | The host of the match; its input is the business date and its output is the run summary |
| `matchPayments` | Activity | `rwb-payment` | The activity that resolves the version, evaluates and writes the record and the row |
| `confirmBookings` | Activity | `rwb-payment` | JOB-08 booking confirmation, declared and not changed |
| `postProceeds` | Activity | `rwb-payment` | The saga step of the settlement and sale flows, declared and not changed |

The document declares the workflow and activity names and their task queue because a consuming team must know which queue carries the work; it registers nothing. The Drools evaluation runs only inside an activity, so a replay reuses the recorded result and never recompiles a model; `NoPackageInForce` is non-retryable.

#### 12.6 Schedules

None. JOB-07 and JOB-08 are event-started workflows on `rwb-payment` (Arch v5 slide 44) and this key registers no Schedule. The 00:01 rule promote JOB-20 is rwb-decision's and is named only.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `proceeds` | P8 (`rwb_payment`) | The `Proceeds` element and the `ProceedsPage` the two operations read and the manual match writes |
| `decision_record` | PLT library, created in `rwb_payment` | The local hash-chained record of each match (DP-03) |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_payment` | The outbox of the three events, the inbox of the six consumed events and the key of the manual match |

Not owned and not declared: `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` (P7), `treatment` (S2), `recovery_case` (P3) and `decision_log_entry` (P7). No foreign key crosses a schema and no other service reads these tables (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers used by this story |
|---|---|---|
| rwb-decision registry fake | RWB-P7-E2027-APP and RWB-P7-E1073-CON | The version list with "PM-2026.12" IN_FORCE from 2026-12-01, the model fetch with its checksum, the refused schema check of "PM-2027.02" naming "PARTIAL" and the tolerance column, and `NoPackageInForce` for 2027-02-01 |
| Rule-evaluation result fake | AC1 | One result with `packageCode` PAYMENT_MATCH, `versionInForce` "PM-2026.12", `ruleId` EXACT, `rowOrder` 1 and the output columns; one with `NoPackageInForce`; one malformed body the schema lint refuses |
| Treatment fake | The installment-paid operation of 12.2 | An accepted answer with the shortfall, a refusal and a timeout |
| rwb-access fake | RWB-P4-E1037-CON | A session with Write-off and posting CRUA and one without the right |
| Decision-record library stub | RWB-PLT-E1027-CON | A healthy append with its chain link, a repeated key and a failed write for the MSG-P7-003 path |
| Event registry fake | AC3 | One accepted and one refused body per event type in BACKWARD mode |

Each fake is derived from the published document, is test-only, and is replaced by the real contract as its story lands without a change to the criteria. The drift test compares every fake with the document on each build.

#### 12.9 Call-type summary

| Call type | Count in this document | Detail |
|---|---|---|
| REST | 2 provided, 7 consumed | `GET /proceeds` and the manual match on `/api/recovery/payment/v1`; the two registry reads, the evaluation result, the parameters, the reference list, the session and the treatment call; one hop, 2 s |
| Kafka | 3 event types and the shared record declared, 6 consumed declared | `rwb.payment.events.v1` with its `.retry` and `.dlt` topics; `rwb.decision-record.v1` shared; the six consumed events of 12.4 |
| Temporal | 1 workflow and 3 activities declared, 0 registered | The JOB-07 workflow with `matchPayments`, `confirmBookings` and `postProceeds` on `rwb-payment`; no Schedule; the two event-started workflows: Not specified in the source documents (GAP-1639) |
| File | None | No file is read, built or delivered by this contract |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It publishes one OpenAPI 3.1 document, one AsyncAPI fragment, the nine contract tables, five fakes and a drift test. It writes no code, no migration and no table, and it changes no payment, no plan, no case and no rule package.

**Deliverables.** `openapi/rwb-payment-v1.yaml` (additive, for the two operations of 12.1), `asyncapi/rwb-payment-v1.yaml` (the three events and the record), the `Proceeds`, `ProceedsPage` and `MatchRequest` elements, the declared rule-evaluation result, the record envelope, the vocabulary of LOV-MATCH, LOV-MATCH-TYPE and LOV-PROCEEDS-SRC as published reference lists, the contract README rows for the seven consumed operations and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | referred to; the app story carries the dependency |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | referred to; the app story carries the dependency |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | C RWB-P7-E1073-CON in fact, not in the metadata row |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | referred to; the app story carries the dependency |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | referred to; the app story carries the dependency |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | referred to; the app story carries the dependency |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | referred to; the app story carries the dependency |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | referred to; the app story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route | referred to; the app story carries the dependency |

DP-04 is the row this document exists for: the kit is the platform's and the packages come from rwb-decision, so the one thing every team must agree on is the shape of the answer (AC1). DP-03 is the second: the record is written by the library in the caller's transaction and this service declares no second writer or topic (AC2). DP-13 and DP-14 fix the base and the event names, and DP-11 fixes the one-hop budget the document states on every consumed row. The metadata rows of this story name None for the build and contract dependencies; the C row of DP-04 is recorded in GAP-2507 and ASM-4152 because a CON story is Day 1 and builds against the published set.

**Build steps**

1. Write the two operations of AC4 and AC5 and validate the additive rule in the pipeline.
2. Write the `Proceeds`, `ProceedsPage` and `MatchRequest` elements and the two error sets with one message ID per condition.
3. Write the declaration of the consumed rule-evaluation result of AC1 and mark the two fields the sources do not give.
4. Write the record envelope of AC2 and validate it against the library schema of RWB-PLT-E1027-CON.
5. Write the AsyncAPI fragment of AC3 and validate one body of each type against the registry fake.
6. Write the versioning and version-recording rules of AC6 and the vocabulary of the closed lists.
7. Publish the five fakes and the drift test; wire the drift test into the build of the app story, the SCR-28 route and the wave 2 harness.
8. Tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document and the AsyncAPI fragment validate, the six contract tests pass, the drift test is green on the build of this story and of the app story, and the app story, the SCR-28 route, the wave 2 harness, rwb-decision and rwb-treatment have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P8-001 | A run summary holds unmatched payments; the document declares the field that carries the count and not the wording | {count} payments for {date} matched no plan and are on the exception list. |
| MSG-P3-027 | A package version check fails, or no version is in force; the document declares the message ID the run summary carries | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-001 | A required field of a request is absent or invalid | Enter {field}. |
| MSG-GEN-004 | The record changed at commit, or a receipt was already matched | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision record cannot be written before the row | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |

The six message IDs are legacy or catalogue identifiers and the text is the legacy and FSD wording copied unchanged; the contract adds no message ID and rewords nothing. For MSG-P3-027 the {check} value is compile, schema, scenario or package in force and {detail} names a row ID, a column or a package code only. Thai text follows DL10. Open decision DL10 is still open; its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are carried as stated in the source documents. The empty, loading, error and no access states of SCR-28 and SCR-39 are not declared by this contract and are Not specified in the source documents (CG-ALL-7596, CG-ALL-7597).

### 15. Screens and states

The contract serves SCR-28 Proceeds matching in its loading, matched and unmatched states (its empty, error and no access states: Not specified in the source documents (CG-ALL-7596)) through the gateway-bff composite route (DP-19). The route calls `GET /proceeds` for the list and reads the rule ID and the rule version of each matched receipt from its record; it calls the manual match operation for the Epic 4 flow of the same screen. The contract fixes the rwb-payment answers only: the route specification, the field list and the screen states belong to RWB-PLT-N001-CON, and the version list a person reads to see LOADED, APPROVED, IN_FORCE, SUPERSEDED and REFUSED is rwb-decision's, shown by SCR-39 Rules and parameters in Epic 8; its empty, loading, error and no access states: Not specified in the source documents (CG-ALL-7597). The refusal states the screen shows — not recorded, refused, already matched, no version in force — read the message IDs of section 14 on the same route.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-P8-E2027-CON-01 | AC1 | Contract | The consumed rule-evaluation result validated: packageCode PAYMENT_MATCH, versionInForce "PM-2026.12", ruleId EXACT, rowOrder 1 and the output columns; the NoPackageInForce outcome; the two placeholder fields marked; no threshold, match type or version label as a constant |
| TC-P8-E2027-CON-02 | AC2 | Contract | The record envelope validated against RWB-PLT-E1027-CON: decision code D5, rule ID, rule version, inputs reference, final call, decided at, chain sequence, hashes and actor; one written before the row and one forced to fail with MSG-P7-003 |
| TC-P8-E2027-CON-03 | AC3 | Contract | One body of TreatmentBooked, one of PaymentMissed and one of ProceedsMatched validated in BACKWARD mode: CloudEvents 1.0, `ce_type`, key caseId, the payload fields, the `.retry` and `.dlt` topics, and a personal-data scan |
| TC-P8-E2027-CON-04 | AC4, AC5, AC6 | Contract | `GET /proceeds` with the query and `ProceedsPage`; the manual match with `Idempotency-Key` and the stored answer; the seven error responses with one message ID each; the rights of TSD P8 T6.1 |
| TC-P8-E2027-CON-05 | AC5, AC6 | Contract | A repeated manual match returns the stored answer with no second effect; a matched receipt answers 409; a breaking change raises a new major version and a new `ce_type`, an additive change stays in major version 1 |
| TC-P8-E2027-CON-06 | AC6 | Component | The five fakes compared with the document: the registry version list, the model checksum, the refused "PM-2027.02" load, `NoPackageInForce` for 2027-02-01, the treatment answer, the access session and the record stub; one drifted fake fails the build |
| TC-P8-E2027-CON-07 | BR10, BR11 | Contract | The tables of 12.7 checked at their boundary: `proceeds` the only table this service writes; `decision_record`, `outbox_event`, `processed_event` and `idempotency_key` created in `rwb_payment` by the library; no foreign key crosses a schema and no other service reads these tables (DP-01) |
| TC-P8-E2027-CON-08 | BR1 to BR12 | Contract | Each rule of section 8 checked against the contract: the two operations, three events, record envelope and consumed result only (BR1); the consumed result from rwb-decision with the version in force from the registry (BR2); the decision record before the row (BR3); the three events on `rwb.payment.events.v1` with `.retry` and `.dlt` (BR4); `Idempotency-Key` on POST and none on GET (BR5); the rights of TSD P8 T6.1 (BR6); LOV rows read through DP-07 (BR7); no business value as a schema default (BR8); the version in force on every match (BR9); no `v_ace_*` grant or foreign table declared (BR10); one base, topic, queue and login (BR11); no personal data in a schema, example or fake (BR12) |
| TC-P8-E2027-CON-09 | AC7 | Contract | Each rule BR1 to BR12 of section 8 checked against the contract by the boundary test: the declared operations, events, record envelope and consumed result; the record before the row; the events and topics; Idempotency-Key on POST only; the TSD P8 T6.1 rights; DP-07 reads; no schema default; no v_ace_* grant; one base, topic, queue and login; a personal-data scan |

Legacy test cases TC-E2-027-01 to TC-E2-027-13 are owned by RWB-P8-E2027-APP. The nine cases `TC-P8-E2027-CON-01` to `-09` are new under D-RCV-60, they are all at Level Contract except the fake set, and the `-ITG` copies of the legacy thirteen belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the match type, the row order, the amount tolerance, the window, the grace and the partial floor are columns of the PAYMENT_MATCH rows and rows of the registry, never enumeration members, defaults or example constants.
- No personal data in a schema, an example, a fake or a log: identifiers, codes, amounts, dates, a rule ID and a version label only; every example is synthetic.
- The money is matched here and nowhere else: the document declares no posting, no balance change and no property of `recovery_case`, `treatment` or a ledger table.
- ACE data only through the owner's contract or this service's `v_ace_*` views, and no cross-schema foreign key; the boundary test fails a build that adds one (DP-01, DP-05).
- One evaluator, one result: the document declares the consumed result and no evaluation of its own, and it never reads a workbook, a `drl_source` or a `rule_row` (DP-04).
- The record is written before the row and on the shared topic only; this service declares no second writer and no second topic for it (DP-03).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- A published version is never edited in place: a breaking change raises a new major version and a new `ce_type`, and a new rule package version needs a new registry row (BR9).
- No secret in the document, a fake or a values file: the rwb-payment login (DP-02) and the Temporal material come from the platform secret store.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan; unmatched to an exception list — fixed here as the two operations, the three events, the record envelope and the rule result the match is decided by | The two operations, the three event types, the record envelope and the consumed result | TC-P8-E2027-CON-01, TC-P8-E2027-CON-03, TC-P8-E2027-CON-04 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The consumed rule-evaluation result and the version-in-force rule of AC1 and AC6 | TC-P8-E2027-CON-01, TC-P8-E2027-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The seven consumed rows with their budget and breaker | TC-P8-E2027-CON-04 |
| ADR-022 | Local decision record plus central ledger | The record envelope of AC2 on `rwb.decision-record.v1` | TC-P8-E2027-CON-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-027, disposition Split (rework) |
| Legacy criteria | AC1, AC2, AC4, AC5, AC8 and AC9 owned by RWB-P8-E2008-APP; AC3 by RWB-P7-E2027-APP; AC6, AC7 and AC10 by RWB-P8-E2027-APP; this baseline copies none of them |
| Test cases | The six new contract cases `TC-P8-E2027-CON-01` to `-06`; the legacy thirteen are owned by RWB-P8-E2027-APP |
| Feature and screen | FEAT-OCC-10, FEAT-PAY-01; SCR-28 Proceeds matching |
| Rules | R-RES-26, R-RES-28, R-UNI-03, R-UNI-38, R-UNI-39, R-UNI-41; the PAYMENT_MATCH rows EXACT, WINDOW and PARTIAL |
| Decoupling patterns | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of the package, the decision record, the `proceeds` row and the events: RWB-P8-E2027-APP.
- The registry and the governance of a package version — the load, its checks, the four-eyes approval, the 00:01 promotion, the rollback and the version states: rwb-decision (P7), RWB-P7-E2027-APP.
- The PAYMENT_MATCH workbook, its Rows and Tests tabs and the authoring pipeline: rwb-case (P3), RWB-P3-E2042-APP and RWB-P3-E1073-APP.
- The case of record and its route states (P3), the plan and the installment shortfall (S2), the session, the roles and the rights (P4) and the ACE facts and their freshness (P1).
- The manual match flow of SCR-28, the settlement matching, the auction and enforcement proceeds and the application of proceeds to the case balance: RWB-P8-E4043-APP, RWB-P8-E4044-APP and RWB-P8-E4049-APP.
- The deployment of this capability — the topics, the worker pool, the alerts, the canary gate, the rollback and the rule-cache refresh runbook: RWB-P8-E2027-OPS.
- The implementation of the outbox relay, the schema registry and the decision-record library: RWB-PLT-TE006-CON, RWB-PLT-N008-INF and RWB-PLT-E1027-CON.
- The exact payload schema of the three events beyond the fields of 12.3 and the field names the sources do not give, which are Not specified in the source documents (GAP-2507; ASM-4153, ASM-4155).
- The real cross-service proof of the match, the record, the version and the events across rwb-payment, rwb-decision, rwb-case, rwb-treatment, rwb-access, rwb-debtsale and rwb-asset: the wave 2 harness.
- The retired `payment_match_rule` table and its reference loads (D-RCV-36 T10): this baseline never declares it.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

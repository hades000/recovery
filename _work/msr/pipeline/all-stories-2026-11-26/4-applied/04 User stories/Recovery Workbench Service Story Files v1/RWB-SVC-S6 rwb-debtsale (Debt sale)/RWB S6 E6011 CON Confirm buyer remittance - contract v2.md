# RWB-S6-E6011-CON Confirm buyer remittance - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the settle-and-cancel step of rwb-debtsale, split from RWB-E6-011. It fixes the settlement element and the answer shape it appears in (DP-13), the settled and cancelled elements and their closed lists, the six consumed rows, the consumed `ProceedsMatched` element of rwb-payment with its inbox rule, the decision-record element of DP-03, the rights and the error envelope, the fakes and the absence tests. TSD S6 appendix T-A publishes no remittance or settlement operation, so the baseline declares no operation as provided and records the two legacy endpoint rows as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's; the money is rwb-payment's (P8) and the ACE payment facts move behind rwb-source-data under DP-05. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6011-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the settle-and-cancel step of rwb-debtsale — the settlement element and the answer shape it appears in, the settled and cancelled elements with their closed lists, the six consumed rows, the consumed `ProceedsMatched` element of rwb-payment, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, the award screen and the wave 4 harness build against one fixed, testable contract on Day 1 and a proceeds payload, a case move, a settlement period or a list value can never drift between rwb-debtsale, rwb-payment, rwb-source-data, rwb-case, rwb-partner, rwb-decision and rwb-access without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy remittance of RWB-E6-011 crossed five boundaries at once: a payment, an ACE payment row, a case state, a decision log and a buyer score. The target splits them: rwb-payment owns the matched proceeds and publishes them, rwb-source-data owns the ACE views, rwb-case owns the case and its route states, rwb-partner owns the buyer scorecard, rwb-access owns the right and rwb-decision owns the package in force and its ledger. Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the settlement element, the settled and cancelled elements, the `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` vocabulary, the `ProceedsMatched` payload and its envelope, the case state and move of rwb-case, the score of rwb-partner, the right of rwb-access and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Architecture v5 slide 19 notes).

Five points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs six consumed contracts (GAP-3013). TSD S6 appendix T-A publishes no remittance or settlement operation, and the two endpoint rows of the legacy story are the published surfaces of two sibling stories (GAP-3013). The `ProceedsMatched` event is named in the event set but no AsyncAPI catalogue publishes its envelope (GAP-3013). The settlement has no column on the two owned tables, so the baseline declares the element and records the missing stamp (GAP-3013). And the wave of the story is EP06's wave 4 while the service is created in wave 3, with the module extract absent (GAP-3013).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map and the context pack only: `debt_sale_lot` and `debt_sale_account` are S6's, `recovery_case`, `timer` and `assignment` are P3's, `proceeds` is P8's, `partner` and the scorecard are S9's, `treatment` is S2's, `role` and `permission` are P4's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's, `notice` is P6's and the `recovery.v_ace_*` views are P1's. This document never declares another service's table or operation as its own.
- The rwb-payment `ProceedsMatched` subscriber contract, the rwb-source-data payment contract, the rwb-case state and move rows, the rwb-partner scorecard row, the rwb-access authorise contract and the rwb-decision package row are published with their fakes, so the consumed rows name a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3013; ASM-4982).
- The Debt sale rule package and its rows for R-DS-24, R-DS-25, R-DS-26 and R-DS-27 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration (GAP-3013; ASM-4984).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the settlement element and the answer shape it is embedded in, with the rights and the error responses, and no operation of its own (GAP-3013; ASM-4982).
2. Fix the settled and cancelled elements: the lot reference, the buyer reference, the matched amount, the payment date, the settlement state, the cancellation reason, the buyer score reference, the rule ID with its version and the decided-at time.
3. Fix the consumed rows: the rwb-source-data payment read, the rwb-case state read and move answer, the rwb-partner scorecard read, the rwb-access authorise call and the rwb-decision package read, marking the fields the sources do not give with the placeholder.
4. Fix the consumed event element: `rwb.payment.ProceedsMatched.v1` on `rwb.payment.events.v1`, its payload, its envelope, its consumer group, its inbox rule and its dead-letter path (GAP-3013; ASM-4985).
5. Record the decision-record element of DP-03, written before anything changes.
6. Record the closed vocabulary of the lists, the naming baseline and the rule that no value is a constant of the code.
7. Record that the buyer is an organisation and that no person name, identity number, date of birth or contact value is a property of any element, example or fake.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the error envelope, the absence of a provided operation, the absence of a `proceeds`, `partner` or `recovery_case` property, the drift between a fake and the document, and the absence of a published event of this step.
10. Tag the baseline and hand it to RWB-S6-E6011-APP, the award screen and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC7 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` or `LOV-PUTBACK` appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a provided operation, a `proceeds`, `partner` or `recovery_case` property, or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | The document declares a published event of this step, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | A person field — a name, an identity number, a date of birth or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC6 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-payment, rwb-source-data, rwb-case, rwb-partner, rwb-access and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the lists, the event name, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6011-APP, the award screen and the wave 4 harness on Day 1, and the rwb-payment, rwb-source-data, rwb-case, rwb-partner, rwb-access and rwb-decision teams on the same day |
| Estimable | One OpenAPI fragment, one AsyncAPI fragment for the consumed event, nine contract tables, eight fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the settle-and-cancel step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case is P3, of proceeds is P8, of partner is S9, of treatment is S2, of role is P4, of decision_log_entry and rule_row is P7 and of the recovery.v_ace_* views is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The settlement element and its answer shape are declared with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the settlement element with the lot reference, the buyer reference, the matched amount, the payment date, the settlement state, the cancellation reason, the rule ID with its version and the decided-at time, and it declares no operation of its own
    Then it records that the element is embedded in the answer of the lot read API-S6-002 and in the answer of the award operation API-S6-003, which belong to the lot read story and to RWB-S6-E6005-APP, and that it narrows neither answer
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with one envelope and one message ID per condition
    Then every other property of the answers is copied from the baseline that owns the operation and is not redefined here

  Scenario: AC2 The settled and cancelled elements and their closed lists are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1, T3.2 and the rule rows R-DS-24 to R-DS-27
    Then the Settlement element declares the lot reference, the buyer partner reference, the matched amount, the payment date, the settlement state and the rule ID with its version
    Then the Cancellation element declares the lot reference, the cancellation reason, the buyer score reference and the rule ID with its version, and it declares no score computation because the score is a scorecard fact of S9 rwb-partner
    Then the settlement state is declared as a closed set of pending, settled and cancelled, and it is declared as a case move of rwb-case and not as a lot status, because LOV-LOT-STATUS has no SETTLED member
    Then lot status is declared against LOV-LOT-STATUS with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, buyer_class against LOV-BUYER-CLASS with AMC and NON_AMC, segment against LOV-SEGMENT with RETAIL, SSME and CORPORATE and put_back_status against LOV-PUTBACK with NONE, CLAIMED, ACCEPTED and REJECTED
    Then the lot reference and the settlement state are required and the other properties are optional
    Then no property carries a person name, an identity number, a date of birth or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The consumed rows for the rwb-source-data payment facts and the rwb-case state are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-source-data contract, Architecture v5 slides 8 and 41 and TSD S6 T5.2
    Then the ACE payment read is declared as consumed from P1 rwb-source-data under DP-05, with the payment code, the payment date, the payment amount, the payment channel and the capital amount of the awarded accounts
    Then the operation name of the row is Not specified in the source documents (GAP-3013; ASM-4987) and the row carries the placeholder
    Then the document declares no v_ace_payment or v_ace_score view, no SELECT on a recovery.v_ace_* view and no ACE table, and it records that the own-ACE-views branch of DP-05 is closed by Architecture v5 slide 8
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case with the case reference and the route state, and the move names are SETTLED and AWARD_CANCELED_DS with the rule ID and its version
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-debtsale
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The consumed ProceedsMatched event element is declared with its envelope and its inbox rule (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with Architecture v5 slide 19 IN and Event and Messaging Design v5 event 25
    Then the event is declared as consumed from P8 rwb-payment as rwb.payment.ProceedsMatched.v1 on the topic rwb.payment.events.v1, with the payload proceedsId, caseId and amount
    Then the envelope fields are Not specified in the source documents for this event (GAP-3013; ASM-4985) and the row carries the placeholder
    Then the document declares one consumer group, one subscription, one inbox row per event, the dead-letter topic of the owner and a repeat rule that answers a duplicate event ID from the inbox row without a second effect
    Then the document declares no published event of this step and records that LotAwarded and AccountsTransferred are sibling stories' and belong to the service's own topic
    Then the baseline records that FSD S6 A2.15.4.4 declares no background event for the feature while the architecture gives this subscription, and that the architecture wins under the source precedence

  Scenario: AC5 The rwb-decision package, the rwb-access right, the rwb-partner score and the error envelope are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with the rule package registry, TSD S6 T6.1 and the platform error envelope
    Then the Debt sale package read is declared as consumed from P7 rwb-decision, with the package version in force and the rule rows R-DS-24, R-DS-25, R-DS-26 and R-DS-27 named and not declared
    Then the capability area Debt sale with its rights is declared as consumed from P4 rwb-access, with RW-DEBTSALE CRUA, RW-CREDITAD R, RW-PRODHEAD RA, RW-HEADASL RA and the SY-* identities R as TSD S6 T6.1 gives them
    Then the buyer scorecard read is declared as consumed from S9 rwb-partner with the buyer reference and the score band, and no score is declared as a field of this service
    Then the authorise operation name is Not specified in the source documents (GAP-3013; ASM-4982) and the row carries the placeholder
    Then a refused caller answers 403 with MSG-P4-002, and a repeated event with the same event ID describes no second effect
    Then the document declares no decision_log_entry column and no rule_row column as its own

  Scenario: AC6 The decision-record element and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the lot reference, the buyer reference, the proceeds reference, the rule ID, the package version in force, the inputs reference, the outcome, the reason, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves the lot unchanged with MSG-P7-003
    Then the rwb-payment event fake answers a full matched proceeds, a short amount, the same event twice and a malformed envelope, and no answer beyond the workflow timer
    Then the rwb-source-data fake answers the payment rows of the awarded accounts and a stale product, the rwb-case fake answers the states SETTLEMENT_PENDING, SETTLED and AWARD_CANCELED_DS with an accepted and a refused move, the rwb-partner fake answers the scorecard with and without a score, the rwb-access fake answers the capability area with and without the right and the rwb-decision fake answers the Debt sale package at its version
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged award screen for lot LOT-2026-000042
    Then every fake carries organisation references, codes, amounts, dates and a rule version only, with no person name, identity number, date of birth or contact value, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and this step publishes no event (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then 12.1 is None and records that TSD S6 T-A publishes no remittance or settlement operation and that the award path API-S6-003 and the data room read API-S6-004 belong to RWB-S6-E6005-APP and RWB-S6-E5026-APP
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, inbox_event, idempotency_key and outbox_event, and proceeds, recovery_case, assignment, treatment, partner, role, permission, document, notice, decision_log_entry, rule_row and every recovery.v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event of this step and one consumed event, and it records that the settlement stamp has no column and that the DB story owns it (GAP-3013; ASM-4984)
    Then the partner channel is recorded as reading the same element through the partner gateway in the DMZ, which has no row in the plan (GAP-3013; ASM-4982)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6011-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and its account set are rwb-debtsale's, and the contract declares their fields, their lists and their required flags on the Settlement and Cancellation elements only | Architecture v5 slide 41; TSD S6 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before anything changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-011 AC1 and AC4 |
| BR3 | The money is rwb-payment's: the matched proceeds are declared as a consumed event and the document declares no `proceeds` property, no posting and no ledger row | Event and Messaging Design v5 (EV-25); Architecture v5 slide 19 IN; GAP-3013 |
| BR4 | The case move is answered and not written: the contract declares the state read and the two moves, and declares no `recovery_case` property and no case row write | TSD S6 T5.2; Architecture v5 slide 4; GAP-3013 |
| BR5 | ACE data only through the owner's contract: the payment facts are declared as a consumed row of rwb-source-data and the document declares no `v_ace_*` field, no view and no ACE table | DP-05; Architecture v5 slide 8; GAP-3013 |
| BR6 | This baseline declares no provided operation: the step runs behind the award operation API-S6-003 and the data room read API-S6-004 of its siblings | TSD S6 T-A.1; GAP-3013 |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none; the step's own surfaces are reads and its consumed event is answered from an inbox row keyed by the event ID | Architecture v5 slide 11; TSD S6 T-A.2; Event and Messaging Design v5 |
| BR8 | The vocabulary is closed: `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` are published as enumerated values and no list value is a constant of the code; the settlement state is a case move and not a lot status | TSD S6 T3.2; FSD S6 BR-S6-015; GAP-3013 |
| BR9 | No personal data in a schema, an example or a fake: the buyer is a partner organisation and no name, identity number, date of birth or contact value is declared | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR12 | The rule rows of R-DS-24 to R-DS-27, the settlement period of `payment_terms` and the reference data of the lot status are governed in rwb-decision and on the lot, named here and never declared here | Business Rules and Routing Logic v4; GAP-3013 |
| BR13 | The module extract is absent and this baseline reads the FSD S6 v3 and the TSD S6 v2 files as the module sources; the two sets are reconciled when the extract is produced | Template and Rules §R7.3; GAP-3013 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the lists, the consumed rows, the consumed event and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the award screen, the wave 4 harness and the rwb-payment, rwb-source-data, rwb-case, rwb-partner, rwb-access and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional settlement field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, the event name or payload changes, or a provided operation is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3, AC4 and AC7 fail: a provided operation, a `proceeds` property, a `recovery_case` property, a published event or a Schedule | In review |

The settlement state machine that the document describes is the app story's: a lot in `SETTLEMENT_PENDING` is settled under R-DS-25 or its award is cancelled under R-DS-26 or R-DS-27. This baseline fixes the vocabulary of those states and the payload of the event that starts them, and it moves no lot.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI and AsyncAPI fragments and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the absent settlement operation and the partner channel |
| Consuming teams (the app story, the award screen, the wave 4 harness and the owners of rwb-payment, rwb-source-data, rwb-case, rwb-partner, rwb-access and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the inbox convention, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element, an event or a fake, and that the buyer is an organisation |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline. The partner gateway in the DMZ is the edge owner's and is named here only as the channel (GAP-3013; ASM-4982).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Settlement element | The lot reference, the buyer partner reference, the matched amount, the payment date, the settlement state, the cancellation reason, the rule ID with its version and the decided-at time |
| Lot and account elements | The lot properties of DF-SAL-020 to DF-SAL-030, with `payment_terms` (DF-SAL-029) and `status` (DF-SAL-030) as the columns the step reads; the account set of DF-SAL-031 to DF-SAL-037 is referenced, with `selling_price` (DF-SAL-036) as the money the settlement is tested against |
| Lists | `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-BUYER-CLASS` (`AMC`, `NON_AMC`), `LOV-SEGMENT` (`RETAIL`, `SSME`, `CORPORATE`) and `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), published as enumerations and read as reference data at their version |
| Settlement state | The closed set pending, settled and cancelled, carried as the rwb-case moves `SETTLED` and `AWARD_CANCELED_DS`; no member of `LOV-LOT-STATUS` carries it (GAP-3013; ASM-4984) |
| Consumed event | `rwb.payment.ProceedsMatched.v1` with `proceedsId`, `caseId` and `amount`, and the envelope carried by the platform rule (GAP-3013; ASM-4985) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything changes (DP-03) |
| Not declared here | `proceeds` and `posting` (P8), `recovery_case`, `timer` and `assignment` (P3), `partner` and the scorecard (S9), `treatment` (S2), `role` and `permission` (P4), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7) and every `recovery.v_ace_*` view (P1) |
| Consumed fields with no source | The operation names of the rwb-source-data payment read, the rwb-case state read and move answer, the rwb-partner scorecard read and the rwb-access authorise call, and the envelope fields of the consumed event: Not specified in the source documents (GAP-3013; ASM-4982) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (C), API-S6-002 `GET /debt-sale-lots/{lotId}` (R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a remittance, settlement or cancellation operation. The two endpoint rows of the legacy story are API-S6-003 and API-S6-004; they are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, and API-S6-005 belongs to the take-bids story of this service. This baseline therefore declares no operation as provided, records the two sibling rows by name, and fixes only the settlement element, the consumed event element and the answer shapes they are embedded in. The absence is recorded as GAP-3013 with ASM-4982.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of the ACE payment data product of the awarded accounts (operation name Not specified in the source documents (GAP-3013; ASM-4987)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The payment code, payment date, payment amount, payment channel and capital amount; faked, DP-05 |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the route of the case; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3013; ASM-4982)) | rwb-case (P3) | P3 rwb-case | The move `SETTLED` or `AWARD_CANCELED_DS` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The buyer scorecard read (operation name Not specified in the source documents (GAP-3013; ASM-4986)) | `/api/recovery/partner/v1` | S9 rwb-partner | The score band of the buyer organisation of the lot for R-DS-26; faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3013; ASM-4982)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Debt sale", the right of the caller and the scope of its lots; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-24 to R-DS-27; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3013 with ASM-4982.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23, consumers rwb-case and rwb-payment) and `AccountsTransferred` (consumers rwb-case and rwb-reporting). `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's; this step produces neither, so the baseline declares no event of its own, no outbox row and no producer, and the absence test of AC7 fails a build that adds one.

#### 12.4 Events consumed

| Event | Topic | Owner | Contracted use |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (event 25) | `rwb.payment.events.v1`, its retry topic and its `.dlt` topic | P8 rwb-payment | The matched proceeds that trigger the settle step: `proceedsId`, `caseId` and `amount`; one consumer group, one subscription, an inbox row keyed by the event ID and a repeat rule that answers a duplicate without a second effect |

The payload is the one Event and Messaging Design v5 gives for EV-25; the CloudEvents envelope fields (`id`, `source`, `type`, `time`, `subject`, `datacontenttype`) are Not specified in the source documents for this event and the row carries the placeholder (GAP-3013; ASM-4985). The baseline records one conflict of source precedence: FSD S6 A2.15.4.4 declares "No background event" for the feature while the architecture and the event set give this subscription, and the architecture wins (Template and Rules §R3). This step consumes one event and publishes none.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer and continues-as-new across the settlement and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the settle-and-cancel step; its signals, its release of the transfer step and its outcome for the parent are declared, not built |
| `confirmRemittance` | Activity, the one settle-and-cancel step | `rwb-debtsale` | The lot, the case, the matched proceeds and the package in force in; the rule ID with its package version, the settlement state, the decision record, the case move and the transfer release out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice. No activity is registered by this story, and the saga steps of reserve, approval, payment, transfer, proceeds, case closure and customer notices belong to the award, derecognition, transfer and case-closure stories of this service.

#### 12.6 Schedules

None. The step runs from the consumed event and the settlement term is a durable timer inside the workflow; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its buyer class, its `payment_terms` and its status; the element the settlement answers from, read only by this step (GAP-3013; ASM-4984) |
| debt_sale_account | S6 (`rwb_debtsale`) | The account set of the lot with its `selling_price` and `outstanding`; read only by this step |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| inbox_event | PLT library, created in `rwb_debtsale` | The event ID of the consumed `ProceedsMatched` and the answer it holds |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of a repeated event or request and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object the service's sibling stories relay their events through; this step declares no row |

`proceeds` and `posting` (P8), `recovery_case`, `timer` and `assignment` (P3), `partner` and the scorecard (S9), `treatment` (S2), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6) and every `recovery.v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment `ProceedsMatched` event fake | The matched proceeds of lot `LOT-2026-000042` with the amount in full, a short amount, the same event twice, a malformed envelope and no event beyond the workflow timer | AC4, AC6 |
| rwb-source-data payment fake | The payment rows of the awarded accounts of case `RC-2026-000842` with a payment date, a channel and a capital amount; a stale product; no answer beyond 2 s | AC3, AC6 |
| rwb-case state and move fake | The states `SETTLEMENT_PENDING`, `SETTLED` and `AWARD_CANCELED_DS` of case `RC-2026-000842`; an accepted move and a refused move for each of the two move names | AC3, AC6 |
| rwb-partner scorecard fake | The buyer scorecard of `PTR-2026-000031` with its score band; a buyer with no scorecard | AC5, AC6 |
| rwb-access authorise fake | The capability area "Debt sale" with its rights for the TSD S6 T6.1 roles; a caller without the right | AC5, AC6 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-24, R-DS-25, R-DS-26 and R-DS-27 | AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the settlement element once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data payment read, the rwb-case move answer, the rwb-partner scorecard read and the rwb-access authorise call are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3013; ASM-4982). The event fake stands in for a subscription whose envelope is not yet published (GAP-3013; ASM-4985).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 6 consumed | The rwb-source-data payment read, the rwb-case state read and the case-move answer, the rwb-partner scorecard read, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 1 consumed | `rwb.payment.ProceedsMatched.v1` on `rwb.payment.events.v1`, one consumer group and one inbox row; `LotAwarded` and `AccountsTransferred` are sibling stories' |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DebtSaleWorkflow` and `confirmRemittance` on `rwb-debtsale`; the settlement term is a durable timer, no Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is reached through the data room of a sibling story |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no buyer record and no rule package. What it publishes is one OpenAPI 3.1 fragment, one AsyncAPI fragment for the consumed event, nine contract tables, eight fakes and five new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the settlement element, the `Settlement` and `Cancellation` elements, the vocabulary of the four lists as published enumerations, the fragment `asyncapi/rwb-debtsale-consumers-v1.yaml` for `rwb.payment.ProceedsMatched.v1` with its inbox rule, the contract README rows for the consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the element describes: the record and the outcome commit together or not at all. DP-05 moves the two legacy ACE reads behind the rwb-source-data contract, whose second branch is closed by Architecture v5 slide 8 (GAP-3013; ASM-4987). DP-13 moves the base and nothing else. DP-19 is behind the award screen, whose screen model is the edge contract's.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. It leaves out the six consumed rows, which are C dependencies in fact and not in the metadata row, the DP-09 inbox library the consumed event needs, the DP-04 kit the evaluation uses and the DP-08 guard the right needs; none is added to the metadata rows and all are named in the registers (GAP-3013; ASM-4983).

**Build steps**

1. Write the settlement element and the answer shape of AC1, with the no-provided-operation record, and validate the additive rule in the pipeline.
2. Write the `Settlement` and `Cancellation` elements, their required flags and the four lists of AC2 with the placeholder where a type is unstated.
3. Record the rwb-source-data and rwb-case rows of AC3 with their owners, their budget and their placeholders, and the boundary that no `v_ace_*` view is declared.
4. Publish the AsyncAPI fragment of AC4: the consumed event, its payload, its envelope placeholder, the consumer group, the inbox rule and the dead-letter path.
5. Record the rwb-decision package, the rwb-access rights, the rwb-partner score row and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the eight fakes of AC6 and the drift test.
8. Record the naming baseline, the boundary and the partner channel of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI and AsyncAPI fragments validate in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the award screen and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request or of an element is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the service identity lacks the Debt sale right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE payment product is stale after a late or failed batch (VR-S6-015-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the freshness check itself belongs to rwb-source-data.

### 15. Screens and states

The contract serves SCR-26 Award, "Bids against the reserve and the award decision" (FSD S6 Screens), in its open, closed, awarded and transferred states, all read only, with the settlement element and the cancelled award and its reason. The route is the gateway-bff composite route (DP-19); the partner side reads its own settlement state through the partner channel, which has no plan row (GAP-3013; ASM-4982). The route calls rwb-debtsale for the lot and the settlement element, rwb-case for the case and its route state and rwb-partner for the buyer; this baseline fixes the settlement element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded and stale-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-011-01 | AC1, AC6 | Contract | Lot `LOT-2026-000042` and case `RC-2026-000842`; the contract half answers the settlement element, the two elements and the four lists |
| TC-E6-011-02 | AC3, AC4 | Contract | The full matched proceeds; the contract half answers the rwb-source-data and rwb-case rows, the event payload and the `SETTLED` move shape |
| TC-E6-011-03 | AC2, AC3 | Contract | A cancelled award with its reason; the contract half answers the `AWARD_CANCELED_DS` move shape, the score reference and the lot status vocabulary |
| TC-E6-011-04 | AC5, AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the decision-record element |
| TC-E6-011-05 | AC5 | Contract | RW-CREDITAD holds R and RW-DEBTSALE holds CRUA; the contract half answers the rights of the capability area |
| TC-E6-011-06 | AC6, AC7 | Contract | A malformed event and an absent payment answer; the contract half answers the error envelope, the absence tests and the no-personal-data test |
| TC-S6-E6011-CON-01 | AC1 | Contract | The fragment validates; the settlement element, the six error answers and the no-provided-operation record are present |
| TC-S6-E6011-CON-02 | AC2 | Contract | The `Settlement` and `Cancellation` elements validate with their properties, their required flags and the four closed lists |
| TC-S6-E6011-CON-03 | AC3, AC4 | Contract | The rwb-source-data, rwb-case and rwb-payment rows, their placeholders and the two move names; the no-`v_ace_*`, no-`proceeds` and no-`recovery_case` boundary |
| TC-S6-E6011-CON-04 | AC5, AC6, AC7 | Contract | The rwb-decision, rwb-access and rwb-partner rows, the eight fakes and the drift test; the absence of a published event, of a second topic and of a Schedule |

The six legacy cases are the legacy cases of RWB-E6-011 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6011-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E6011-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in the contract: the settlement period, the lot status and buyer class members, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example, an event or a fake: the buyer is a partner organisation and no name, identity number, date of birth, address or contact value is declared; every example is synthetic.
- ACE data stays with rwb-source-data, the money with rwb-payment and the case with rwb-case: the document declares no `v_ace_*` field, no `proceeds` property, no `recovery_case` property, no posting and no case row write (BR3, BR4, BR5).
- The ledger stays with rwb-decision and the score with rwb-partner: the document declares no `decision_log_entry` column and no score computation.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-003 and API-S6-004 are named as the surfaces the step runs behind and as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, never as provided here (BR6).
- No retired element is reintroduced: the absence test fails a build that declares a published event of this step, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the inbox convention, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying; the contract fixes the settlement element, the consumed rows and the consumed event on which the step is built (Business Requirements Program v5); the split plan carries no requirement id for this slice (GAP-3013; ASM-4982) | The settlement element, the two elements and the six consumed rows | TC-E6-011-01, TC-E6-011-02, TC-S6-E6011-CON-01, TC-S6-E6011-CON-02 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The consumed `ProceedsMatched` element, its inbox rule and the recorded absence of a published event | TC-S6-E6011-CON-03, TC-S6-E6011-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S6-E6011-CON-03, TC-S6-E6011-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the outcome | TC-S6-E6011-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-011, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S6-E6011-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S6-E6011-CON-01 to -04 |
| Feature and screens | FEAT-DBS-15 Confirm buyer remittance, SCR-26 Award |
| Rules | R-DS-24, R-DS-25, R-DS-26 and R-DS-27, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-DS-25, R-DS-26 and R-DS-27, the decision record, the case moves and the release of the transfer: RWB-S6-E6011-APP.
- The award operation API-S6-003 and its `DecisionLogEntry` answer: RWB-S6-E6005-APP (GAP-3013).
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP (GAP-3013).
- The bid submission operation API-S6-005 and the bidding window: the take-bids story of this service.
- The matching of the buyer's payment, the posting of the proceeds and the daily reconciliation: rwb-payment (P8) (GAP-3013; ASM-4985).
- The ACE payment and score views and their data products: rwb-source-data (P1), read on its contract only (GAP-3013; ASM-4987).
- The case of record, its route states, its assignment and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The capability area, the rights and the scope rows, and the authorise call: rwb-access (P4) (GAP-3013; ASM-4982).
- The buyer scorecard, the partner panel and the partner channel: rwb-partner (S9) (GAP-3013; ASM-4986).
- The authoring, testing, approval and versioning of the Debt sale package and of the rule rows of R-DS-24 to R-DS-27: rwb-decision (P7).
- The derecognition and the general ledger posting of FEAT-DBS-12, the transfer of R-DS-29 and the case closure of FEAT-DBS-14: the sibling stories of this service.
- The settlement stamp column on `debt_sale_lot` or `debt_sale_account`: the DB story of this service (GAP-3013; ASM-4984).
- The gateway-bff composite route and the screen field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

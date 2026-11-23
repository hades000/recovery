# RWB-S6-E6007-CON Transfer the data to the buyer - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the transfer step of rwb-debtsale, split from RWB-E6-007. It fixes the transfer element and the answer shapes it appears in (DP-13), the `AccountsTransferred` event with its CloudEvents envelope and its payload, the consumed rows for the rwb-case state and move, the rwb-partner buyer facts, the rwb-integration buyer-file delivery (INT-25) and the rwb-access right, the decision-record element of DP-03, the rights, the error envelope, the fakes and the absence tests. TSD S6 T-A publishes no transfer operation, so the baseline declares no operation as provided and records the two legacy endpoint rows as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's; the file transport belongs to rwb-integration (P2) and the partner gateway in the DMZ has no plan row. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the transfer step of rwb-debtsale — the transfer element and the answer shapes it appears in, the `AccountsTransferred` event and its envelope, the consumed rwb-case, rwb-partner, rwb-integration, rwb-access and rwb-decision rows, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, SCR-26 Award, PRT-05 Data room, rwb-case, rwb-partner, rwb-integration, rwb-reporting and the wave 4 harness build against one fixed, testable contract on Day 1 and a transfer state, a delivery reference, an event payload or a move name can never drift between rwb-debtsale and the services it answers without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the event is a CloudEvents envelope with an outbox (DP-09, ADR-015). The legacy transfer of RWB-E6-007 crossed five boundaries at once: a case state, a buyer, a data tape, a file delivery and a decision log. The target splits them: rwb-case owns the case and its route states, rwb-partner owns the buyer organisation, rwb-integration owns the file transport and its keys, rwb-payment owns the settled money, rwb-access owns the right, rwb-decision owns the package in force and its ledger, and rwb-debtsale owns the lot, the tape and the transfer fact. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the transfer element and the states it carries, the `AccountsTransferred` payload, the buyer and lot references, the delivery instruction and its answer, the two case moves, the right and the record.

The baseline also fixes the naming the checks require: schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, event name `rwb.debtsale.AccountsTransferred.v1`, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Architecture v5 slide 19 notes).

Four points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs five consumed rows and a file-delivery activity (GAP-3005). TSD S6 appendix T-A publishes no transfer operation, and the two endpoint rows of the legacy story are the published surfaces of two sibling stories (GAP-3005). The `AccountsTransferred` event has no published schema and no published payload: TSD S6 T5.3 lists `LotAwarded` alone, the event catalogue gives a payload for `LotAwarded` and none for the transfer event, and the event is taken from the Architecture v5 row, which outranks the TSD (GAP-3005). And the transfer has no column set of its own: `debt_sale_account` carries no transfer time and no file reference, so the transfer is recorded on the lot status, the decision record and the event, and the missing columns are recorded (GAP-3005). The wave of the story is EP06's wave 4 while the service is created in wave 3, and the conflict is already recorded once for the service and the business epic (GAP-1972; ASM-3194).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event name follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `partner` and `partner_user` are S9's, `recovery_case` and `timer` are P3's, `role` and `permission` are P4's, `decision_log_entry` and `rule_row` are P7's, `proceeds` is P8's, the delivery and file rows are P2's, `document` is P5's and `notice` is P6's. This document never declares another service's table or operation as its own.
- The rwb-case state and move rows, the rwb-partner buyer read, the rwb-integration delivery activity and the rwb-access authorise contract are published with their fakes, so the consumed rows name a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3005; ASM-4951).
- The Debt sale rule package and its rows for R-DS-25 and R-DS-29 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration (GAP-3005; ASM-4954).
- The event envelope, the retry and `.dlt` topics and the outbox library are the platform's (RWB-PLT-TE006-CON); the event name follows DP-14 and no second topic is declared here.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the transfer element and the answer shapes it is embedded in, with the rights and the error responses, and no operation of its own (GAP-3005; ASM-4958).
2. Fix the transfer element: the lot reference and lot number, the buyer reference, the buyer class, the transfer state, the delivery reference, the transfer time, the account count, the rule ID with its version and the decided-at time.
3. Fix the `AccountsTransferred` contract: the CloudEvents envelope, the subject and key, the payload, the consumers and the retry and `.dlt` topics, with no account number and no per-account amount (ASM-4952).
4. Fix the consumed rows: the rwb-case state read and move answer, the rwb-partner buyer read, the rwb-integration `deliverFile` activity, the rwb-access authorise call and the rwb-decision package read, marking the fields the sources do not give with the placeholder.
5. Record the decision-record element of DP-03, written before the lot row changes, and the delivery reference it holds.
6. Record the closed vocabulary of `LOV-LOT-STATUS` and the other lists, the naming baseline, and the rule that no value is a constant of the code.
7. Record that the delivered content is the masked tape and that no person field is a property of any element, example or fake.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the envelope, the payload, the absence of a provided operation and of a consumed event of this step, the `Idempotency-Key` rule, the error envelope, the no-personal-data test, the drift between a fake and the document, and the absence of a `partner` or `recovery_case` property.
10. Tag the baseline and hand it to RWB-S6-E6007-APP, SCR-26 Award, PRT-05 Data room, rwb-case, rwb-partner, rwb-integration, rwb-reporting and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body, a request body or an event payload fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope and a malformed event goes to the `.dlt` topic | MSG-GEN-001 | AC1, AC2, AC7 |
| X2 | A field is renamed or removed within major version 1, or an event property is removed | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row or the delivery activity has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4, AC5 |
| X5 | A value outside `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` or `LOV-PUTBACK` appears in the document, an example or an event | The vocabulary test fails the build | None | AC2, AC6 |
| X6 | The document declares a provided operation, a `partner` or `recovery_case` property, a remittance property or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares a second event, a second topic, a Schedule, a Quartz row or a local file directory | The absence test fails the build | None | AC4, AC7 |
| X8 | A person field — a name, an identity number, a date of birth, a contact value or an unmasked account number — appears in any element, example, event or fake | The schema test and the review fail the baseline | None | AC2, AC6 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-case, rwb-partner, rwb-integration, rwb-access and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values, the event payload property names and the fake fixtures are settled in the baseline review; the element set, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6007-APP, SCR-26 Award, PRT-05 Data room, rwb-case, rwb-reporting and the wave 4 harness on Day 1 |
| Estimable | One OpenAPI fragment, one event schema, nine contract tables, eight fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the transfer step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of partner and partner_user is S9, of recovery_case is P3, of role is P4, of decision_log_entry and rule_row is P7, of proceeds is P8 and of the delivery rows is P2
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The transfer element and its answer shapes are declared with their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the transfer element with the lot reference, the lot number, the buyer reference, the buyer class, the transfer state, the delivery reference, the transfer time, the account count, the rule ID with its version and the decided-at time, and it declares no operation of its own
    Then it records that the element is embedded in the answer of the lot read API-S6-002 and in the answer of the data room read API-S6-004, which are the lot read story's and RWB-S6-E5026-APP's, and that it narrows neither answer
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then every other property of the answers is copied from the baseline that owns the operation and is not redefined here

  Scenario: AC2 The AccountsTransferred event is declared with its envelope and payload (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with the Architecture v5 event row, TSD S6 T5.3 and the platform CloudEvents rule
    Then one event is declared, rwb.debtsale.AccountsTransferred.v1, on the topic rwb.debtsale.events.v1 with its retry and .dlt topics, with the lot ID as its key and subject and with the consumers rwb-case and rwb-reporting
    Then the payload declares the lot reference, the lot number, the buyer reference, the buyer class, the account count, the transfer time, the delivery reference, the rule ID and the rule version, and no account number, no name and no per-account amount
    Then the document records that TSD S6 T5.3 lists LotAwarded alone, that the event catalogue publishes a payload for LotAwarded and none for this event, and that the event is taken from the Architecture v5 row, which outranks the TSD (GAP-3005; ASM-4952)
    Then the lot status is declared against LOV-LOT-STATUS with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, buyer_class against LOV-BUYER-CLASS with AMC and NON_AMC, and segment against LOV-SEGMENT with RETAIL, SSME and CORPORATE
    Then no property carries a person name, an identity number, a date of birth, a contact value or an unmasked account number, and the schema test fails any element, example, event or fake that adds one

  Scenario: AC3 The rwb-case and rwb-partner rows are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with rwb-partner as the owner of partner
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the moves SETTLED and DATA_TRANSFERRED carrying the rule ID and its version
    Then the operation names of the state read and of the move answer are Not specified in the source documents (GAP-3005; ASM-4951) and the rows carry the placeholder
    Then the buyer organisation read is declared as consumed from S9 rwb-partner, with the partner reference, the organisation, the panel status and the delivery target, and its operation name is Not specified in the source documents (GAP-3005; ASM-4951)
    Then the document declares no recovery_case property, no partner property, no case row write and no buyer row write, and the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-integration delivery activity and the file row are declared (new, D-RCV-60)
    Given the consumed rows and the file section of the baseline
    When they are compared with INT-25 of TSD S6 T5.1 and the Architecture v5 OUT row of rwb-debtsale
    Then the delivery is declared as a Temporal activity of rwb-integration (P2) on the queue rwb-integration, with the lot reference, the buyer reference, the tape reference and the account count in and the delivery reference, the delivery time and the outcome out
    Then the activity name is the deliverFile operation Architecture v5 names, its request and response property names are Not specified in the source documents (GAP-3005; ASM-4953), and the row carries the placeholder
    Then the document records that INT-25 is an outbound file per lot, delivered through the data room and encrypted, and that this service builds no transport, holds no key and declares no file directory, no batch table and no Quartz row
    Then the schema rwb_debtsale holds no delivery table and no transfer column: the delivery reference lives in the decision record and in the event (GAP-3005; ASM-4954)
    Then DP-16 is named as a tracked dependency and no operation of rwb-integration is declared as this service's own

  Scenario: AC5 The rwb-access right and the rwb-decision package are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with the rule package registry, TSD S6 T6.1 and the platform error envelope
    Then the Debt sale package read is declared as consumed from P7 rwb-decision, with the package version in force and the rule rows R-DS-25 and R-DS-29 named and not declared
    Then the capability areas Debt sale and Partner portal with their rights are declared as consumed from P4 rwb-access, with RW-DEBTSALE CRUA, RW-PRODHEAD RA, RW-HEADASL RA, RW-CREDITAD R, PT-BUYER RU scoped to its own lots and the SY-* identities R as TSD S6 T6.1 gives them
    Then the authorise operation name is Not specified in the source documents (GAP-3005; ASM-4951) and the row carries the placeholder
    Then a refused caller answers 403 with MSG-P4-002, and a repeated settled fact, transfer run or delivery answer with the same Idempotency-Key describes no second effect
    Then the document declares no decision_log_entry column and no rule_row column as its own

  Scenario: AC6 The decision-record element, the fakes and the vocabulary answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation, the activity or the event it serves
    Then one decision record is declared per rule outcome with the case reference, the lot reference, the buyer reference, the rule ID, the package version in force, the inputs reference, the outcome, the reason, the case move, the delivery reference and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the lot row changes, and a failed write leaves the lot unchanged with MSG-P7-003
    Then the rwb-integration fake answers the delivery of lot LOT-2026-000042 with the reference DLV-2026-000118, a failed delivery, an answer with no reference and no answer beyond 2 s
    Then the rwb-case fake answers the states SETTLEMENT_PENDING, SETTLED and AWARDED with an accepted and a refused move for each of the two move names, the rwb-partner fake answers the organisation PTR-2026-000031 and a suspended organisation, and the rwb-decision fake answers the Debt sale package at its version
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged award screen for lot LOT-2026-000042
    Then every fake carries organisation references, lot references, amounts, dates and a rule version only, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and this step publishes its event and consumes none (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then 12.1 is None and records that TSD S6 T-A publishes no transfer operation and that the award path API-S6-003 and the data room read API-S6-004 are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and partner, partner_user, recovery_case, role, permission, proceeds, the delivery rows, document, notice, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares one published event, AccountsTransferred, and no consumed event of this step, and it records that LotAwarded (EV-23) is the award story's and that ProceedsMatched is the settlement step's, RWB-S6-E6011-APP's (GAP-3005; ASM-4955)
    Then the partner channel is recorded as reaching the same element through the partner gateway in the DMZ, which has no row in the plan (GAP-3005; ASM-4958)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6007-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and the transfer fact are rwb-debtsale's, and the contract declares their fields and their lists on the transfer element and the event only | Architecture v5 slide 19 (lots, data room, buyer terms, bids, award, transfer); TSD S6 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the lot row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy RWB-E6-007 AC1 and AC4 |
| BR3 | The case move is answered and not written: the contract declares the state read and the two moves, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); GAP-3005 |
| BR4 | The buyer stays with rwb-partner: the contract declares the organisation read as consumed and no partner property and no buyer row write | Architecture v5 slide 41; Ownership Map (`partner`, `partner_user` owner S9); GAP-3005 |
| BR5 | The file transport is rwb-integration's: the contract declares the `deliverFile` activity and its answer, and declares no file directory, no batch table, no key and no encryption rule | Architecture v5 slide 19 (deliverFile, buyer file); TSD S6 T5.1 (INT-25); GAP-3005 |
| BR6 | This baseline declares no provided operation: the step runs behind the award operation and the data room read of its siblings and adds no endpoint | TSD S6 T-A.1; GAP-3005 |
| BR7 | The vocabulary is closed: `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-SEGMENT` and `LOV-PUTBACK` are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-011 |
| BR8 | One event, one topic, one envelope: the CloudEvents envelope is the platform's, the event name follows DP-14, the outbox and the retry and `.dlt` topics follow DP-09, and no second event is declared | ADR-015; Template and Rules §R4; GAP-3005 |
| BR9 | No personal data in a schema, an example, an event or a fake: the delivered content is the masked tape and no name, identity number, date of birth, contact value or unmasked account number is declared | Template and Rules v1 §R7.2 (s17); REQ-S6-003; FSD S6 A2.3 |
| BR10 | A schema change is additive within major version 1; a breaking change, including a removed event property, is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR11 | The rule rows of R-DS-25 and R-DS-29 and the reference data of the lists are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; GAP-3005 |
| BR12 | The five-working-day target of R-DS-29, the settlement condition of R-DS-25 and the 45-day turnaround are rule values, not contract defaults | Business Rules and Routing Logic v4; FSD S6 A2.11.1 and A2.11.3.1; ASM-4956 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the event, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, rwb-case, rwb-partner, rwb-integration, rwb-reporting and the wave 4 harness accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or an optional event field is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, an event property is removed or a provided operation is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3, AC4 and AC7 fail: a provided operation, a `partner` or `recovery_case` property, a second event, a Schedule or a file directory | In review |

The lot and case machine the document describes is the app story's: the lot moves from `AWARDED` to `TRANSFERRED` and the case of record from `SETTLEMENT_PENDING` to `SETTLED` and `DATA_TRANSFERRED`. This baseline fixes the vocabulary of those states and moves no lot.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment, the event schema and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the event payload, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (the app story, SCR-26 Award, PRT-05 Data room, rwb-case, rwb-partner, rwb-integration, rwb-reporting and the wave 4 harness) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the CloudEvents envelope, the `Idempotency-Key` rule, the naming rule, the outbox and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element, an event or a fake, and that the delivered content is the masked tape |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline. The partner gateway in the DMZ is the edge owner's and is named here only as the channel (GAP-3005; ASM-4958).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Transfer element | The lot reference, the lot number, the buyer reference, the buyer class, the transfer state, the delivery reference, the transfer time, the account count, the rule ID with its version and the decided-at time |
| Lot element | The lot properties of DF-SAL-020 to DF-SAL-030; `status` (DF-SAL-030) is the column the transfer writes, and `buyer_partner_id` (DF-SAL-025), `buyer_class` (DF-SAL-026) and `payment_terms` (DF-SAL-029) are read |
| Account set | DF-SAL-031 to DF-SAL-037 are referenced, not copied: no column carries a transfer time or a file reference, so the delivery reference lives in the decision record and in the event (GAP-3005; ASM-4954) |
| Event payload | The lot reference, the lot number, the buyer reference, the buyer class, the account count, the transfer time, the delivery reference, the rule ID and the rule version in a CloudEvents envelope; no account number and no per-account amount (GAP-3005; ASM-4952) |
| Lists | `LOV-LOT-STATUS` (`BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED`, `CLOSED`), `LOV-BUYER-CLASS` (`AMC`, `NON_AMC`), `LOV-SEGMENT` (`RETAIL`, `SSME`, `CORPORATE`) and `LOV-PUTBACK` (`NONE`, `CLAIMED`, `ACCEPTED`, `REJECTED`), published as enumerations and read as reference data at their version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the lot row changes, carrying the delivery reference (DP-03) |
| Not declared here | `recovery_case` and `timer` (P3), `partner`, `partner_user` and the panel tables (S9), `role` and `permission` (P4), `document` (P5), `notice` (P6), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), the delivery and file rows (P2) and every `v_ace_*` view (P1) |
| Consumed fields with no source | The operation names of the rwb-case state read and move answer, the rwb-partner buyer read, the rwb-access authorise call and the rwb-integration `deliverFile` request and response properties: Not specified in the source documents (GAP-3005; ASM-4951) |

The field-level types, lengths and required flags of the added elements and of the event payload are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (C), API-S6-002 `GET /debt-sale-lots/{lotId}` (R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a transfer operation. The two endpoint rows of the legacy story are API-S6-003 and API-S6-004; they are RWB-S6-E6005-APP's and RWB-S6-E5026-APP's. This baseline therefore declares no operation as provided, fixes only the transfer element and the answer shapes it is embedded in, and records the absence as GAP-3005 with ASM-4958.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the lot link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3005; ASM-4951)) | rwb-case (P3) | P3 rwb-case | The move `SETTLED` or `DATA_TRANSFERRED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The buyer organisation read (operation name Not specified in the source documents (GAP-3005; ASM-4951)) | `/api/recovery/partner/v1` | S9 rwb-partner | The organisation behind `buyer_partner_id`, its panel status and its delivery target; faked. The panel family of the Ownership Map is `GET /partners` |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3005; ASM-4951)) | `/api/recovery/access/v1` | P4 rwb-access | The capability areas "Debt sale" and "Partner portal", the right of the caller and the scope of its own lot; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-25 and R-DS-29; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3005 with ASM-4951. The file delivery is not a REST row: it is the `deliverFile` activity of rwb-integration, declared in 12.5 (GAP-3005; ASM-4953).

#### 12.3 Events published

| Event | Topic | Key | Consumers | Payload |
|---|---|---|---|---|
| `rwb.debtsale.AccountsTransferred.v1` (AccountsTransferred) | `rwb.debtsale.events.v1`, with its retry and `.dlt` topics | Lot ID | P3 rwb-case, P9 rwb-reporting | The CloudEvents envelope and the transfer fact: lot reference, lot number, buyer reference, buyer class, account count, transfer time, delivery reference, rule ID and rule version. No account number, no name and no per-account amount (GAP-3005; ASM-4952) |

One event per lot and transfer, declared as the outbox row written in the same transaction as the lot update and relayed by the platform library (DP-09). Architecture v5 gives the topic the events `LotAwarded` and `AccountsTransferred`; `LotAwarded` is EV-23 and RWB-S6-E6005-APP's, TSD S6 T5.3 lists `LotAwarded` alone, and the event catalogue publishes no payload for this event, so the payload above is fixed here and the difference is recorded (GAP-3005; ASM-4952). DP-09 and DP-14 are not in the pattern set of this key, so `RWB-PLT-TE006-CON` and `RWB-PLT-E1047-CON` are tracked dependencies and not H rows.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale one consumed event, `rwb.payment.ProceedsMatched.v1` (event 25) on `rwb.payment.events.v1`, and its consumer group and inbox row belong to the settlement step, RWB-S6-E6011-APP, which passes the settled fact to this step as a signal of `DebtSaleWorkflow`. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one (GAP-3005; ASM-4955).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer, continues-as-new across the settlement, the transfer and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the settlement and transfer steps; its input, its signals and its outcome for the parent are declared, not built |
| `settleAward` | Activity, the R-DS-25 step | `rwb-debtsale` | The lot, the case and the settled fact in; the rule ID with its version, the settlement record and the `SETTLED` answer out |
| `transferAccounts` | Activity, the R-DS-29 step | `rwb-debtsale` | The lot, the buyer, the tape reference and the account count in; the delivery reference, the lot status, the outbox row, the decision record and the `DATA_TRANSFERRED` answer out |
| `deliverFile` | Activity, owned by rwb-integration (P2) | `rwb-integration` | The lot, the buyer, the tape reference and the account count in; the delivery reference, the delivery time and the outcome out; consumed by `transferAccounts` (GAP-3005; ASM-4953) |

No child workflow for the case and none for the money exists in this service. The local activity names are target design choices, and the trigger is read as the settled fact for R-DS-25 and the rule timer for R-DS-29, because the FSD declares the feature unattended and no background event (FSD S6 A2.11.3.3 and A2.11.4.4). No activity is registered by this story, and the saga steps of reserve, approval, payment match, derecognition, ledger posting, case closure and customer notices belong to the award, settlement, derecognition, closure and notice stories of this service.

#### 12.6 Schedules

None. The five-working-day target of R-DS-29 is a durable timer of `DebtSaleWorkflow`; this baseline declares no Temporal Schedule, no Quartz row, no shared job table, no batch table and no file window, and no Job of Architecture v5 slide 44 is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its buyer reference, its payment terms and its status; `status` is the column the transfer writes and the element the screens read |
| debt_sale_account | S6 (`rwb_debtsale`) | The awarded account set that is delivered; read only by this step, and no column carries a transfer time or a file reference (GAP-3005; ASM-4954) |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the settlement and of the transfer, carrying the delivery reference (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated settled fact, transfer run or delivery answer and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The `AccountsTransferred` row, written in the lot's transaction and relayed by the platform (DP-09) |

`partner` and `partner_user` (S9), `recovery_case` and `timer` (P3), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), the delivery and file rows (P2) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers or as another story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The states `SETTLEMENT_PENDING`, `SETTLED` and `AWARDED` of case `RC-2026-000842`; an accepted and a refused move for each of `SETTLED` and `DATA_TRANSFERRED` | AC3, AC6 |
| rwb-partner buyer fake | The organisation `PTR-2026-000031` on the panel and active, with its delivery target; a suspended organisation; no answer beyond 2 s | AC3, AC6 |
| rwb-integration delivery fake | The delivery of lot `LOT-2026-000042` with reference `DLV-2026-000118`; a failed delivery; an answer with no reference; no answer beyond 2 s | AC4, AC6 |
| rwb-access authorise fake | The capability areas "Debt sale" and "Partner portal" with their rights for the TSD S6 T6.1 roles; a caller without the right | AC5, AC6 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-25 and R-DS-29 | AC5, AC6 |
| Settled-fact signal fake | The fact of the rwb-payment `ProceedsMatched` event (event 25) for lot `LOT-2026-000042`, settled in full at `2026-11-18T10:00:00Z`; a partial amount; a late signal | AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, carrying the transfer element once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case state read and move answer, the rwb-partner buyer read, the rwb-access authorise call and the rwb-integration delivery activity are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3005; ASM-4951). The partner gateway is represented by the composite route fake, because the channel has no story row (ASM-4958).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The rwb-case state read and move answer, the rwb-partner buyer read, the rwb-access authorise call and the rwb-decision package read; one hop, 2 s |
| Kafka | 1 declared, 0 consumed | `AccountsTransferred` is declared in 12.3 for the app story's publication, one event on `rwb.debtsale.events.v1`; `rwb.payment.ProceedsMatched.v1` is the settlement step's and is not declared here |
| Temporal | 1 workflow, 2 local activities and 1 remote activity declared, 0 registered | `DebtSaleWorkflow`, `settleAward` and `transferAccounts` on `rwb-debtsale`, and `deliverFile` on `rwb-integration`; no Schedule |
| File | 1 out | The masked tape and the awarded account data of the lot, delivered by rwb-integration as an encrypted file through the data room, per lot (INT-25) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no delivery and no rule package. What it publishes is one OpenAPI 3.1 fragment, one event schema, nine contract tables, eight fakes and five new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the transfer element, the `Transfer` and `Delivery` elements, the `asyncapi/rwb-debtsale-v1.yaml` for `AccountsTransferred`, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the eight WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the element describes: the record and the lot update commit together or not at all. DP-13 moves the base and nothing else. DP-19 is behind SCR-26 Award and PRT-05 Data room, whose screen model is the edge contract's, and the partner channel reaches the same element behind the partner gateway. The event follows DP-14 and the outbox DP-09; neither is in the pattern set of this key, so both are tracked and not added to the metadata rows (GAP-3005; ASM-4952).

**Dependencies the tables add and the plan does not hold.** The pattern table adds the two H rows the plan's build list for this key already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. It leaves out the five consumed rows and the delivery activity, which are C dependencies in fact and not in the metadata row, the DP-08 guard, DP-09 and DP-14; none is added to the metadata rows and all are named in the text and in the registers (GAP-3005; ASM-4951).

**Build steps**

1. Write the transfer element and the answer shapes of AC1, with the no-provided-operation record, and validate the additive rule in the pipeline.
2. Write the `AccountsTransferred` schema of AC2 with its envelope, its payload, its key and its consumers, and validate it against the CloudEvents rule.
3. Record the rwb-case and rwb-partner rows of AC3 with their owners, their budget and their placeholders.
4. Record the rwb-integration delivery activity of AC4, its placeholders and the no-file-directory rule.
5. Record the rwb-access rights, the rwb-decision package and the error envelope of AC5.
6. Record the decision-record element of AC6 with the delivery reference and validate it against the library schema.
7. Publish the eight fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment and the event schema validate in the pipeline, the five contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, both screens, the wave 4 harness and the owners of rwb-case, rwb-partner, rwb-integration and rwb-reporting have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a request or of the delivery instruction is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the partner identity lacks the Debt sale or the Partner portal right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the lot row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. A failed file delivery carries no message of the set: it is an internal path of the workflow, and the contract describes only its answer shape and the `.dlt` route of a malformed event.

### 15. Screens and states

The contract serves SCR-26 Award in its open, closed, awarded and transferred states and PRT-05 Data room in its data room, bid and transferred states, all read only. The staff route is the gateway-bff composite route (DP-19); the partner route is the partner gateway in the DMZ, which fronts rwb-partner and reaches the same transfer element scoped to the buyer's own lots (ASM-4958). The route calls rwb-debtsale for the lot and the transfer element, rwb-case for the case and its route state and rwb-partner for the buyer organisation; this baseline fixes the transfer element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded and incomplete-request states the app story shows read the messages of section 14 on the same routes.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-007-01 | AC1, AC2 | Contract | Lot `LOT-2026-000042` and buyer `PTR-2026-000031`; the contract half answers the transfer element, the event schema and its payload |
| TC-E6-007-02 | AC2, AC4 | Contract | The transfer of the lot under R-DS-29; the contract half answers the event envelope, the delivery answer shape and the lot status vocabulary |
| TC-E6-007-03 | AC3 | Contract | Case `RC-2026-000842` at `SETTLEMENT_PENDING` and then `SETTLED`; the contract half answers the two move shapes and the buyer row |
| TC-E6-007-04 | AC5, AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the decision-record element |
| TC-E6-007-05 | AC5 | Contract | RW-DEBTSALE holds CRUA and PT-BUYER holds RU scoped; the contract half answers the rights of the two capability areas |
| TC-E6-007-06 | AC6, AC7 | Contract | A malformed request and a failed delivery; the contract half answers the error envelope, the absence tests and the no-personal-data test |
| TC-S6-E6007-CON-01 | AC1 | Contract | The fragment validates; the transfer element, the seven error answers and the no-provided-operation record are present |
| TC-S6-E6007-CON-02 | AC2 | Contract | The event schema validates with its envelope, its payload, its key and its two consumers, and the four lists are enumerated |
| TC-S6-E6007-CON-03 | AC3, AC4 | Contract | The rwb-case, rwb-partner and rwb-integration rows with their placeholders; the no-`partner`, no-`recovery_case` and no-file-directory boundary |
| TC-S6-E6007-CON-04 | AC5, AC6, AC7 | Contract | The rwb-access and rwb-decision rows, the eight fakes and the drift test; the absence of a consumed event, of a second topic and of a Schedule |

The six legacy cases are the legacy cases of RWB-E6-007 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6007-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E6007-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in the contract: the five-working-day target, the settlement condition, the 45-day turnaround, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example, an event or a fake: the delivered content is the masked tape and no name, identity number, date of birth, address, contact value or unmasked account number is declared; every example is synthetic.
- The buyer stays with rwb-partner, the case with rwb-case and the delivery with rwb-integration: the document declares no `partner` property, no `recovery_case` property, no file directory and no key (BR3, BR4, BR5).
- The money stays with rwb-payment and the central ledger with rwb-decision: the document declares no proceeds property, no posting and no `decision_log_entry` column.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-003 and API-S6-004 are named as the surfaces the step runs behind and as RWB-S6-E6005-APP's and RWB-S6-E5026-APP's, never as provided here (GAP-3005).
- No retired element is reintroduced: the absence tests fail a build that declares a consumed event, a second topic, a Schedule, a Quartz row, a shared job table or a local file directory.
- The error envelope, the CloudEvents envelope, the `Idempotency-Key` rule, the naming rule, the outbox and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying (Business Requirements Program v4; FSD S6 requirements served); the split plan carries no requirement id for this slice (GAP-3005; ASM-4951) | The transfer element, the event schema and the five consumed rows | TC-E6-007-01, TC-E6-007-03, TC-S6-E6007-CON-01, TC-S6-E6007-CON-02 |
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank | The payload and the element carry no per-account data and the delivered content is the masked tape | TC-S6-E6007-CON-02, TC-S6-E6007-CON-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The `AccountsTransferred` schema, its envelope and the outbox row | TC-S6-E6007-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S6-E6007-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the lot changes | TC-S6-E6007-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-007, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S6-E6007-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S6-E6007-CON-01 to -04 |
| Feature and screens | FEAT-DBS-11 Transfer the data to the buyer, SCR-26 Award and PRT-05 Data room |
| Rules | R-DS-25 and R-DS-29, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-DS-25 and R-DS-29, the decision record, the delivery instruction, the lot change and the two case moves: RWB-S6-E6007-APP.
- The award operation API-S6-003 and its `DecisionLogEntry` answer: RWB-S6-E6005-APP (GAP-3005).
- The data room read API-S6-004 and its `DataRoom` answer: RWB-S6-E5026-APP.
- The lot read API-S6-002 and its `DebtSaleLot` answer: the lot read story of this service.
- The masked data tape and its build: RWB-S6-E5025-APP.
- The file transport, its encryption, its keys, its retention and the delivery rows: rwb-integration (P2) (GAP-3005).
- The matching of the buyer's remittance, its record and `ProceedsMatched`: RWB-S6-E6011-APP (GAP-3005).
- The derecognition and the general ledger posting of R-DS-30 to R-DS-33: RWB-S6-E6008-APP; the put-back claim of R-DS-34: RWB-S6-E6009-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The capability areas, the rights and the scope rows, and the authorise call: rwb-access (P4).
- The authoring, testing, approval and versioning of the Debt sale package and of the rule rows of R-DS-25 and R-DS-29: rwb-decision (P7).
- The buyer panel, the partner users and the buyer's KYC, licence and NDA facts: rwb-partner (S9).
- The gateway-bff composite route and the screen field lists of SCR-26 and PRT-05: RWB-PLT-N001-CON and the edge stories; the partner gateway in the DMZ and the partner sign-in: the edge stories, with no plan row.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

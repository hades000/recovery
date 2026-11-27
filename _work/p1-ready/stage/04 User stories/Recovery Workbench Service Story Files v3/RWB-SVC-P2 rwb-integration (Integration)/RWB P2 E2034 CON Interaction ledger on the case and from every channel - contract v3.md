# RWB-P2-E2034-CON Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P2-E2034-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-SVC-P2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP13, DP15, DP18, DP19 |
| Readiness decisions | RD-P1-001, RD-P1-003, RD-P1-004, RD-P1-007, RD-P1-008, RD-P1-010, RD-P1-011, RD-P1-040, RD-P1-041, RD-P1-064, RD-P1-066, RD-P1-067 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P2-E2034-CON-16); the owning squad sizes the story at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1066-CON (ledger append); the `GET /efs-history` fragment of rwb-source-data; RWB-P1-E1015-CON (`AceDataReady`); the rwb-case, rwb-partner, rwb-treatment and rwb-payment fact contracts; rwb-case order of the timeline (REQ-ILG-006) |
| Contract version | v1, the /v1 path of each operation in 12.1 and 12.2; consumed rwb-source-data: `rwb-source-data.yaml` 5.1.0 and `asyncapi/rwb-source-data.asyncapi.yaml` 5.1.0 (API Specification v7) |
| Integration dependencies | The owners' consumed topics of BR2 |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md (no FR mapped to REQ-ILG-009, REQ-ILG-010, REQ-ILG-011, REQ-ILG-012, REQ-ILG-013, REQ-ILG-014, REQ-ILG-007, REQ-ILG-008, REQ-ILG-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-034 for rwb-integration. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 30 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

- D-RCV-60 finishing pass: RD-P1-004, RD-P1-066, RD-P1-067; requests F05-affected-0152, S10-stories-0565; Test Cases v9 mappings.

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- A promise row of the EFS read step is appended as `eventCode` PROMISE (`isPtp` true), CONTACT otherwise; the pending note on GAP-3300 is removed (RD-P1-064 rule 8; request G9-finish-0312).
- The ledger append is declared as `InteractionRequest` 5.1.0 with the business key form, a UUID `Idempotency-Key`, 201 or 200 as success and 409 as a refusal (RD-P1-001, RD-P1-007; findings #2, #3).
- The notice types are consumed for inbox accounting only (rwb-comms appends its notice entries); the notice read, the contact-fact read and their fakes are removed (RD-P1-007; finding #1).
- The EFS read is `GET /efs-history` per account with the ruled mapping; `AceDataReady` key, payload and ALS start rule (RD-P1-003, RD-P1-007, RD-P1-040; findings #4, #5).
- `DecisionRecorded` type, error body and codes, consumed and fake versions, test case IDs marked (RD-P1-004, RD-P1-008, RD-P1-011; findings #6, #8, #9, #10); AC9, X8 and X9 added.
- Open: GAP-3375, GAP-3376 and GAP-3377 (findings #4, #7).

### 1. Story

As a **tech lead**, I want **the rwb-integration side of the interaction ledger fixed as a contract: the seven CloudEvents types this consumer declares on their owners' topics, the P1 append contract and the P1 EFS history read, the rwb-case, rwb-partner, rwb-treatment and rwb-payment fact contracts it calls, the two admin operations it provides on the new base, the delivery states, the dedupe key and the three-attempt exception rule, the decision-record element and the contract fakes**, so that **the app, operations and test stories of this legacy key build on Day 1 against one agreed, testable shape and no team waits for another service to exist**.

The legacy story had no contract of its own: the ledger, the consumer, the mapping and the screen sat in one module, so the shape of a ledger entry was whatever the module wrote. Under D-RCV-60 the ledger belongs to rwb-source-data (DP-18), the timeline to rwb-case, the masking to rwb-access and the portal to rwb-partner, and this service becomes the transport between the seven events and that ledger. A transport needs a contract more than an owner does: it has to say what it declares, what it calls, what it counts, what it parks and what it never touches, and it has to be faked so that the app story can be built and tested before rwb-source-data and rwb-case are built.

The contract also fixes the seam that the split creates. The legacy story appended "inside the delivery's transaction"; across a REST boundary there is no shared transaction, so the contract states the only rule that gives the same guarantee: the append is called before the inbox row is marked, both are idempotent on the same key, and a repeated ledger business key is answered 200 with the existing entry. That single sentence is what makes TC-E2-034-05 and TC-E2-034-07 provable across two services, and it is the reason this story is Day 1 work.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling rule (DP-11, ADR-020) and the event contract is the platform rule (DP-09, DP-14). Both only pay off if the seam is written down once. Here the seam is small and load-bearing: seven types consumed on four topics owned by other services, one create-only append operation, four fact contracts, one dedupe key, one exception rule and two admin operations.

If the shape is agreed and faked on Day 1, three teams move at once. The app story builds the listener, the mapper, the delivery tracker and the two workflows against the fakes; the operations story wires the consumer groups, the retry scan, the exception queue alert and the runbook against the same document; the test stories of RWB-E2-034, RWB-E2-022 and the P1 ledger read one entry shape. Without it, each team invents its own entry, the dedupe key and the retry rule diverge between the consumer and the screen, and the one property the business asked for — that a contact is recorded once and never lost — depends on which service crashed first.

The contract also states what this service does not own. The ledger table, the append-only trigger, the EFS outcome list and the retention classes are rwb-source-data's; the timeline, the sequence order and the scope check are rwb-case's; the masking is rwb-access's; the partner portal and the instruction facts are rwb-partner's. This document defines the consumed side of each and restates none of them as its own.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the REST base, the topic and the event names follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the platform error envelope and the message catalogue are the platform baseline; this document narrows them where it must and says so (DP-09).
- The outbox and inbox library contract is available (RWB-PLT-TE006-CON): `processed_event`, `outbox_delivery`, `idempotency_key`, the retry topic and the `.dlt` topic are its elements and are reused, not redefined.
- The owners' event contracts are as published: `rwb.treatment.events.v1`, `rwb.comms.events.v1`, `rwb.partner.events.v1`, `rwb.payment.events.v1` and `rwb.source-data.events.v1` (Arch v5 slides 42 and 43).
- The rwb-source-data ledger append and EFS history read are as published in `rwb-source-data.yaml` 5.1.0 (RWB-P1-E1066-CON for the append; no P1 contract story publishes the `GET /efs-history` fragment, GAP-3512). This story consumes them and fakes them from `fakes/rwb-source-data/5.1.0/`; it defines neither.
- The rwb-case, rwb-partner, rwb-treatment and rwb-payment CON stories are as published (RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2016-CON, RWB-P4-E1037-CON, RWB-P7-E1027-CON and the owner contracts of the fact reads).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the consumed-event contract: the seven types, their topics, their owners, the envelope, the key and the dedupe key of each.
2. Publish the P1 append contract as consumed: the operation, `InteractionRequest` 5.1.0, the header key, the answers 201, 200, 409 and 503 and the 2 s budget.
3. Publish the P1 EFS history read as consumed, with its stub and the ruled row mapping.
4. Publish the fact contracts of rwb-case, rwb-partner, rwb-treatment and rwb-payment with the element each mapper needs and the degradation rule of a 404.
5. Publish the two admin operations provided, with method, path, purpose, right, idempotency and the delivery states.
6. State the dedupe key, the three-attempt rule, the move to EXCEPTION and the `RESOLVE_OUTBOX_DELIVERY` task for RW-PLATADM.
7. Publish the two workflows and their activity contracts, the retry policy of each activity and the shape of the EFS read summary.
8. Publish the table ownership: the five objects of `rwb_integration` this slice writes, and the explicit statement that no ledger table, no EFS reference table and no case timeline is among them.
9. Publish the fakes and the drift test, then tag the baseline and hand it to the app, operations and test stories of this key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A message does not carry the CloudEvents 1.0 attributes, or its type is not one of the seven | The consumer refuses it before any state change and routes it to `.dlt` with an alert; no delivery row and no append | None | AC2 |
| X2 | A message carries no business key, so no dedupe key can be built | Refused as X1; the contract names the business key of each type | None | AC2 |
| X3 | A fake drifts from this document, or the app calls a path this document does not declare | The contract test fails and the merge is blocked | None | AC5 |
| X4 | A service code path reads a ledger table, an ACE view or another service's table | The architecture boundary test fails the build | None | AC6 |
| X5 | A consumed contract removes, renames or retypes an element this document declares | The contract goes back to review with the owner of that operation, and the app, operations and test stories are re-baselined | None | AC2, AC3 |
| X6 | A field-level detail of a consumed operation is missing from the source material | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1 |
| X7 | The exception rule is asked to park a delivery that is already DELIVERED | The operation is refused and nothing changes; the states and their legal moves are those of 12.1 | MSG-GEN-004 | AC3 |
| X8 | An `AceDataReady` of a source system other than ALS, or with a status other than COMPLETED | Acknowledged and ignored, not dead-lettered; no workflow starts | None | AC2 |
| X9 | The ledger append answers 409 (business key with a different body, or header key reused or in flight) | Not a success: the attempt counts against the three attempts and the delivery ends in EXCEPTION | MSG-PLT-N009-05 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes and the owners' published operations and declares none of theirs as its own |
| Negotiable | Field-level detail of the consumed operations is settled with their owners; the dedupe key, the state list and the exception rule are fixed by this realignment |
| Valuable | Unblocks the app, operations and test stories of this key and gives the P1 ledger and the P3 timeline one entry shape to agree on |
| Estimable | Seven consumed types, one append contract, one P1 read, four fact contracts, two admin operations, five tables and six fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the AsyncAPI document, the OpenAPI document, the fake, this file — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Channel intake contract baseline for rwb-integration

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the outbox and inbox library contract of RWB-PLT-TE006-CON is in force
    Given the ledger is owned by rwb-source-data and the timeline by rwb-case

  Scenario: AC1 The nine contract tables are complete and attributed (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map
    Then 12.1 names the two admin operations on the base /api/recovery/integration/v1
    Then 12.2 names the P1 append, the P1 EFS history read, the four fact contracts and the authorise call
    Then 12.3 is the decision-record element only, 12.4 is the seven consumed types, 12.6 is None and 12.8 is the fakes
    Then 12.7 names only the five objects of rwb_integration and states that no ledger table is among them
    Then a sub-table that names another service's operation as provided fails the review

  Scenario: AC2 The seven consumed types are fixed with their envelope, key and dedupe key (new, D-RCV-60)
    Given the consumed-event contract of this story
    When a message of each of the seven types is validated against it
    Then each message carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype
    Then each message carries the business key that builds its dedupe key as <EV-nn>:<business key>:v1, and an EFS row uses EFS:<efsRecordKey>
    Then each case message is keyed by its case id, AceDataReady is keyed {sourceSystem}:{businessDate} with data sourceSystem, businessDate, status and completedAt, and no message carries personal data
    Then a message without the envelope, without a business key, or of an eighth type is refused and routed to .dlt with an alert
    Then only an AceDataReady with sourceSystem ALS and status COMPLETED starts the EFS read step; any other AceDataReady is acknowledged and ignored

  Scenario: AC3 The delivery states and the three-attempt exception rule are fixed (new, D-RCV-60)
    Given the delivery contract of this story
    When a delivery is followed from its first attempt to its third failure
    Then its states are PENDING, RETRYING, DELIVERED and EXCEPTION and no other state is written
    Then attempt 2 and attempt 3 each run after the environment retry interval (value Not specified in the source documents (ACR-RWB-P2-E2034-CON-AC3)), and the attempt limit is three
    Then after the third failed attempt the status is EXCEPTION with the last error code and a task RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM
    Then a resend of a delivery in EXCEPTION sets it to PENDING with attempt count 0, and a resend of a delivery not in EXCEPTION answers 409
    Then an unresolvable case follows the same rule and writes 0 entries on attempts 1 to 3

  Scenario: AC4 The P1 append contract is consumed and no ledger table is owned (new, D-RCV-60)
    Given the append contract of this story
    When the entry command and the answer are reviewed
    Then the request is InteractionRequest 5.1.0 with eventCode, occurredAt, actorType, actorRef, sourceRef and idempotencyKey required, the case id in the path, a UUID Idempotency-Key header, and no sourceSystem, caseId or retentionClass
    Then the idempotencyKey of a channel entry has the form <EV-nn>-<caseNo>-<yyyyMMdd of occurredAt>-<actionId>, or is the producer's ce_idempotencykey where it publishes one
    Then NoticeDispatched and NoticeDelivered produce no append
    Then the append is create-only: a new business key answers 201, a repeated one 200 with the existing entry, and 409 MSG-PLT-N009-05 is not a success
    Then the append is called before the inbox row is marked, so a replay after a timeout writes one entry
    Then the interaction table, its append-only trigger, the EFS ledger outcome list and the retention classes are declared as rwb-source-data's and none appears in 12.7
    Then the rwb-source-data WireMock answers 201, 200 with the existing entry on a repeat, 409 MSG-PLT-N009-05 and 503 MSG-P1-022

  Scenario: AC5 The six fakes match this document and drift fails the build (new, D-RCV-60)
    Given the six fakes of 12.8
    When each fake is compared with the element it serves
    Then every consumed path and payload is answered with the shape of this document
    Then every error answer named in this document is reachable in a fake
    Then a drift between a fake and this document fails the contract test and blocks the merge

  Scenario: AC6 No cross-schema read and no foreign key leave this service (new, D-RCV-60)
    Given the code and the migrations of the app and operations stories of this key
    When the architecture boundary test runs
    Then no statement reads a table of another service, a ledger table or an ACE view
    Then the only cross-service calls are the declared paths of 12.2, one hop each with a 2 s budget
    Then rwb_integration holds no foreign key into another schema and no copy of a ledger, case, notice, instruction, treatment or proceeds row
    Then the seven consumed topics are the only subscriptions and no topic of this service is subscribed

  Scenario: AC7 The provided operations answer 401, 403 and 404 on their error requests (new, D-RCV-60)
    Given the provided operations of this story
    When a request carries no session, comes from a role without the Platform administration right, or is a resend that names an unknown delivery
    Then the answer to the request with no session is 401 with messageCode MSG-P4-001 as application/problem+json
    Then the answer to the request from a role without the Platform administration right is 403 with messageCode MSG-P4-002
    Then the answer to the resend that names an unknown delivery is 404 with messageCode MSG-P4-003

  Scenario: AC8 Each business rule BR1 to BR10 has a criterion and a test case (new, D-RCV-60)
    Given the business rules of section 8
    When the test cases of section 16 are run
    Then each rule BR1 to BR10 is covered by its test case TC-P2-E2034-CON-08 to TC-P2-E2034-CON-17
    Then a rule without a passing test case fails the review

  Scenario: AC9 The EFS history element and its mapping are fixed (new, RD-P1-007)
    Given the EFS history element of 12.2 and its fake with two rows of one account, one with isPtp true
    When the rows are mapped
    Then the read is GET /api/recovery/source-data/v1/efs-history with accountKey and businessDate, one account per call, and 409 MSG-P1-001 when DP01 or DP05 is incomplete for the business date
    Then each append has eventCode CONTACT or PROMISE (isPtp), occurredAt = contactAt, actorType SERVICE, actorRef "rwb-integration", sourceRef "EFS v_ace_efs_action" and idempotencyKey "EFS:{efsRecordKey}"
    Then written counts the 201 answers and a 200 answer is not counted
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base and one topic per service: this contract declares `/api/recovery/integration/v1` and consumes the owners' topics; it never declares another service's path or topic as its own | DP-13; DP-14; ownership map |
| BR2 | The seven consumed types are `rwb.treatment.TreatmentApproved.v1`, `rwb.comms.NoticeDispatched.v1`, `rwb.comms.NoticeDelivered.v1`, `rwb.partner.InstructionIssued.v1`, `rwb.partner.PartnerResultSubmitted.v1`, `rwb.payment.ProceedsMatched.v1` and `rwb.source-data.AceDataReady.v1`, on the owners' topics; the two notice types and PartnerResultSubmitted are consumed for inbox accounting without an append; `AceDataReady` starts the EFS read step only for ALS with status COMPLETED | Arch v5 slides 42 and 43; naming library (DP-14) |
| BR3 | The ledger is rwb-source-data's: the entry is created only through its append operation, and this service holds no ledger table, no ledger column and no ledger read | R-PREC default ruling; DP-18; ownership map ruling on `interaction`; GAP-1612 |
| BR4 | The append is create-only and idempotent on the ledger business key (`<EV-nn>-<caseNo>-<yyyyMMdd>-<actionId>`, or the producer's `ce_idempotencykey`; `EFS:<efsRecordKey>` for EFS), and it is called before the inbox row is marked; a repeated business key answers 200 with the existing entry and writes nothing | Legacy RWB-E2-034 BR7; R-UNI-40; REQ-ILG-007 |
| BR5 | One dedupe key per message: `<EV-nn>:<business key>:v1` for the six business events held in `processed_event` with a hit count, and `EFS:<efsRecordKey>` is the ledger business key of an EFS row; the ledger keeps no hit count and the EFS written count is the run's 201 answers (RD-P1-007) | Legacy BR7; FSD P2 v3 AC-EXC-P2-007-03 and AC-EXC-P2-007-07; GAP-0590 |
| BR6 | The delivery states are PENDING, RETRYING, DELIVERED and EXCEPTION; the attempt limit is three; the last failure raises `RESOLVE_OUTBOX_DELIVERY` for role RW-PLATADM and an EXCEPTION delivery may be resent to PENDING with attempt count 0 | Legacy AC8 and AC7; FSD P2 v3 T4 and AC-EXC-P2-001-01; TSD P2 v3 LOV-OUTBOX-DELIVERY |
| BR7 | The two admin operations are the exception queue surface of this slice and are attributed to rwb-integration; the outbound-item operations are the baseline story's and are not declared here | TSD P2 v3 T-A.1 API-P2-003 and API-P2-004; ownership map |
| BR8 | The EFS read step is started by AceDataReady (EV-26) of ALS with status COMPLETED and is not an outbox delivery; it carries its own workflow and its own summary; JOB-01 is retired and starts nothing here | Legacy section 12 (EFS contact read step); EV-26 (legacy name LoadCompleted) |
| BR9 | No business value in the contract: the event codes, the channels, the directions, the retry intervals and the attempt limit are reference rows and environment values | Template and Rules §R7.2 s17; FSD P2 v3 BR-P2-007 |
| BR10 | No contract element names a person: the entry carries identifiers, codes and references, and the contact point is a key | Legacy BR5; REQ-ILG-014; CTL-11 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The nine sub-tables, the seven types, the append contract and the fakes are described | In review |
| In review | Consumer sign-off | The app, operations and test stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A field, an error code or a fake is added without removing one | Baselined |
| Baselined | Breaking change to a consumed operation | An owner removes, renames or retypes an element this contract declares | In review, with that owner |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A new channel event is declared | The owner publishes on its own topic and this contract adds one type and one mapping | Baselined (new type) |

The delivery states of the runtime are PENDING, RETRYING, DELIVERED and EXCEPTION and are fixed in 12.1; they are not states of this document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-integration | Owns this document and the six fakes; tags the baseline |
| Solution architect | Approves a breaking change to a consumed contract and any change to the exception rule |
| The rwb-source-data owner | Owns the append and EFS history operations and signs off the shapes taken from its document |
| The rwb-case owner | Owns the timeline, the case read and the sequence order this contract feeds |
| The rwb-access owner | Owns the masking rule and the scope check behind the two admin operations |
| The rwb-integration app, operations and test stories | Review and accept the parts they consume |
| Data steward | Confirms that no personal data field is declared in an event, a command or an activity input |

The deployment identity that calls the owners' contracts is Not specified in the source documents (GAP-0665; ASM-1173); the document names it "the rwb-integration login (DP-02)" and leaves the name to the app and operations stories.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Consumed event envelope | id, source, type, specversion, time, subject, datacontenttype; the payload of the event type, keyed by case id where a case exists (`AceDataReady`: `{sourceSystem}:{businessDate}`) | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |
| Dedupe record | consumer, idempotency key in the form above, CloudEvents id, hit count, last seen at (`processed_event`) | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |
| Ledger entry command | `InteractionRequest` 5.1.0: eventCode, occurredAt, actorType, actorRef, sourceRef, idempotencyKey and, where they apply, channel, direction, actionCode, contactResult, promiseAmount, promiseDate, fromHolderRef, toHolderRef, treatmentId, proceedsId; case id in the path | `rwb-source-data.yaml` 5.1.0 |
| Ledger entry answer | `Interaction`: 201 new, 200 existing entry for a repeated business key; the retention class is set by the owner | `rwb-source-data.yaml` 5.1.0 |
| Delivery record | event id, consumer, status, attempt count, next attempt at, last error code, delivered at, task id (`outbox_delivery`) | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |
| Task element | the `RESOLVE_OUTBOX_DELIVERY` task for role RW-PLATADM, linked from the delivery | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |
| Decision-record element | decision code, final call, the action (resend or exception), the delivery reference and the freshness, written by the library on `rwb.decision-record.v1` | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |
| EFS read summary | businessDate, rowsRead, written, excluded, notOnCase | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |
| Activity input and output | the event type and payload in; the ledger entry reference and the delivery state out | Not specified in the source documents (DOR-RWB-P2-E2034-CON-7) |

The names, lengths and required flags of the ledger append are those of `InteractionRequest` 5.1.0. The `actorType`, `actorRef` and `sourceRef` values of the channel entries, the physical names of the other owners' fact answers and the request and response bodies of the two admin operations are Not specified in the source documents (GAP-0664; GAP-0665; ASM-1173).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/integration/v1`; owner rwb-integration (P2). Two operations.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/outbox/deliveries` | Lists the deliveries of consumer `ledger-channels` by status, consumer, event type, from and to, with the page and size parameters of the legacy appendix | Platform administration R, scope applied | Not applicable |
| POST | `/admin/outbox/deliveries/{deliveryId}/resend` | Sends a delivery in EXCEPTION again: status PENDING, attempt count 0, the workflow started again for the same event; written to the decision record with the user and the time | Platform administration U, scope applied | `Idempotency-Key` header; 409 when the delivery is not in EXCEPTION |

The delivery states are PENDING, RETRYING, DELIVERED and EXCEPTION (LOV-OUTBOX-DELIVERY, TSD P2 v3 T3.2). The retry policy of a delivery is three attempts; the intervals are environment values (BR9). Errors: 401 no session (MSG-P4-001), 403 no Platform administration right (MSG-P4-002), 404 unknown delivery (MSG-P4-003), 409 not in EXCEPTION or a workflow already running (MSG-GEN-004), 503 dependency unavailable (MSG-GEN-006). Errors are `application/problem+json` with the shared `Problem` schema (RD-P1-004). The resend's `Idempotency-Key` is a UUID: missing or not a UUID 400 MSG-PLT-N009-03, replay returns the stored status and body, different request or in flight 409 MSG-PLT-N009-05, store unavailable 503 MSG-PLT-N009-06, kept 24 hours (RD-P1-001). These two operations are the re-based forms of API-P2-003 and API-P2-004 of TSD P2 v3 T-A.1, whose paths sat under the monolith base; the outbound-item operations `GET /admin/outbound-items` and `POST /admin/outbound-items/{itemId}/resend` remain with the rwb-integration baseline of RWB-P2-E1007-CON and are not declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the contract |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The ledger append: one `InteractionRequest` per call with a UUID `Idempotency-Key`; faked with 201, 200 with the existing entry, 409 MSG-PLT-N009-05 and 503 MSG-P1-022; also 400, 401, 403, 404, 422 (shared `Problem`) |
| GET | `/api/recovery/source-data/v1/efs-history?accountKey=&businessDate=` | P1 rwb-source-data | EFS contact and promise history of one account (`EfsHistoryAnswer`; caller the rwb-integration workload identity); faked with 200 rows and 409 MSG-P1-001. The list of accounts to read is Pending (GAP-3376) and the action-code filter (GAP-3375) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its holder and its status; faked with one case and one 404 for AC3 |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The open case ids of an account (legacy `CaseQuery.openCaseIdsForAccount`) |
| GET | The instruction-fact read of the rwb-partner contract | S9 rwb-partner | The case and the partner code of an instruction (legacy `InstructionQuery.byId`) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment and its case behind an OFFER entry |
| GET | The proceeds-fact read of the rwb-payment contract | P8 rwb-payment | The proceeds and its case behind a PAYMENT entry |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role and scope check of the two provided operations |

Every operation is one hop with a 2 s client budget and no retry on a 4xx (DP-11, ADR-020). The ledger append and the EFS history read are published in `rwb-source-data.yaml` 5.1.0; no contact-fact read is consumed. The instruction read and the proceeds read are named by their legacy Java interfaces only; their paths, query parameters and JSON field names are Not specified in the source documents (GAP-0665; ASM-1173), and the case-list account filter is unnamed in the same way.

#### 12.3 Events published

None by this story's own topic. The shared event `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` is published by the local decision-record library of DP-03 when a resend or an exception is recorded; its schema is unchanged by this story and is the one declared in RWB-P7-E1027-CON (EV-08, Arch v5 slide 42 row 08). `rwb.integration.events.v1` carries FileDelivered and FileFailed from the outbound file side (Arch v5 slide 16) and this slice publishes neither.

#### 12.4 Events consumed

The service shares consumer group rwb-integration.rwb.source-data.events.v1 and one listener across its source-data event workflows, including JOB-08. It has READ on the main topic, READ and WRITE on retry topics and WRITE on the dead-letter topic (RD-P1-066).

| Event type | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 | CloudEvents 1.0; key case id; dedupe `<EV-10>:<treatmentId>:v1`; one OFFER entry |
| `rwb.comms.NoticeDispatched.v1` | `rwb.comms.events.v1` | P6 | Key case id; dedupe `<EV-14>:<noticeId>:v1`; inbox accounting only; rwb-comms appends the LETTER entry |
| `rwb.comms.NoticeDelivered.v1` | `rwb.comms.events.v1` | P6 | Key case id; dedupe `<EV-15>:<noticeId>:v1`; inbox accounting only; rwb-comms appends the delivery entry |
| `rwb.partner.InstructionIssued.v1` | `rwb.partner.events.v1` | S9 | Key case id; dedupe `<EV-20>:<instructionId>:v1`; one HANDOVER entry, channel PORTAL, direction OUTBOUND |
| `rwb.partner.PartnerResultSubmitted.v1` | `rwb.partner.events.v1` | S9 | Key case id; dedupe <EV-21>:<instructionId>:v1; acknowledgement only; rwb-partner appends over REST |
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | P8 | Key case id; dedupe `<EV-25>:<proceedsId>:v1`; one PAYMENT entry |
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 | Kafka key `{sourceSystem}:{businessDate}`; data `sourceSystem`, `businessDate`, `status`, `completedAt`; inbox key for example `EV-26:ALS:2026-11-10`; starts EfsLedgerReadWorkflow only for ALS with status COMPLETED and writes no entry by itself |

All seven are consumed with the inbox dedupe of `processed_event`, at least once, and idempotent by key. rwb-partner appends its own result through REST. Treatment and payment ownership remains Pending (GAP-3377). A message that fails the envelope, lacks the business key or carries an eighth type is routed to `.dlt` with an alert (DP-09). The payload of each type is the owner's; this contract declares the elements the mapper reads and does not restate the owner's schema.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| LedgerChannelIntakeWorkflow | Workflow, one execution per consumed event, workflow ID = the CloudEvents id | `rwb-integration` | Input: event type, CloudEvents id, business key, occurred time, case id, payload reference. Output: the ledger entry reference and the delivery state |
| mapChannelEvent | Activity | `rwb-integration` | Input: event type and payload. Output: the ledger entry command of 11; one method per type (BR2) |
| resolveChannelFacts | Activity | `rwb-integration` | Input: the identifier the event carries. Output: the resolved facts; a 404 leaves the link empty and is not retryable, a 5xx is retryable |
| appendLedgerEntry | Activity | `rwb-integration` | Input: the `InteractionRequest`, the case id and the header key. Output: the entry id; 201 and 200 are success, a 409 is not |
| parkDeliveryInException | Activity | `rwb-integration` | Input: delivery id, failure class, attempt count. Output: status EXCEPTION, the `RESOLVE_OUTBOX_DELIVERY` task for RW-PLATADM, the decision record |
| EfsLedgerReadWorkflow | Workflow, started by AceDataReady of ALS with status COMPLETED, one per business date (ID literal Pending, GAP-3376) | `rwb-integration` | Input: business date. Output: the EFS read summary |
| readEfsOutcomes | Activity | `rwb-integration` | Input: business date; one `GET /efs-history` call per account. Output: the rows and the excluded count (filter Pending, GAP-3375) |
| appendEfsEntries | Activity | `rwb-integration` | Input: the kept rows. Output: the written count, one append per row under `EFS:<efsRecordKey>` with the mapping of AC9 (eventCode PROMISE for a promise row, RD-P1-064 rule 8); 201 counted as written |
| writeEfsReadSummary | Activity | `rwb-integration` | Input: the counts. Output: the summary of 11 |

The retry policy of every activity is the workflow kit's: initial interval 1 s, back-off 2, maximum 3 attempts, with the 4xx answers of the append classified as non-retryable except 409 (DP-10). The workflow input and history carry identifiers, codes and counts only.

#### 12.6 Schedules

None. No Schedule is registered for this slice. The intake is event-started from the seven consumed types and the EFS read step is started by AceDataReady, not by a timer (BR8; Arch v5 slide 44 JOB-02 and JOB-04). The outbox relay of each service runs every minute in the platform relay of DP-09 and is not a Schedule of this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| outbound_item | P2 (rwb_integration) | Read only, for the interface column of the exception queue; this slice writes no outbound file item |
| outbox_delivery | PLT library, created in rwb_integration | One delivery per consumed event and consumer `ledger-channels`; the status, attempt count, next attempt, last error and task of 12.1 |
| processed_event | PLT library, created in rwb_integration | The inbox: consumer, idempotency key, CloudEvents id, hit count |
| idempotency_key | PLT library, created in rwb_integration | The stored response of the two provided operations, kept 24 hours |
| decision_record | PLT library, created in rwb_integration | The local decision record of a resend and of an exception (DP-03) |

No other table is named. `interaction`, its append-only trigger and its indexes are rwb-source-data's; `efs_ledger_outcome` and the retention classes are rwb-source-data's; the case timeline and the sequence order are rwb-case's. None of them appears here as an object of this service (BR3, DP-01, DP-18). `outbox_event` exists in `rwb_integration` from the baseline and this slice writes no row in it, because the consumed events are produced by their owners.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock — append (`fakes/rwb-source-data/5.1.0/`) | 201 with the `Interaction`; 200 with the existing entry on a repeated business key; 409 MSG-PLT-N009-05; 503 MSG-P1-022 and one slow answer | App story, contract tests |
| rwb-source-data WireMock — EFS history (`fakes/rwb-source-data/5.1.0/`) | The rows of one account for 2026-12-14, one with `isPtp` true and one without; one 409 MSG-P1-001 | App story, test stories |
| rwb-case WireMock | Case `RW-2026-000301` with holder "U-2001"; the open case ids of `ACC-SYN-0301`; a 404 for the case of instruction `INS-SYN-0304` | App story, AC3 |
| rwb-partner WireMock | Instruction `INS-SYN-0301` to partner `LF-SYN-01`; one partner result; one 404 | App story |
| rwb-treatment and rwb-payment WireMock | Treatment `TRT-SYN-0301`; proceeds `PRC-SYN-0301` of 5,000.00; one 404 each | App story |
| rwb-access WireMock | The authorise answer granting and refusing Platform administration | App story, contract tests |
| Kafka stubs | One message per type, one duplicate per type, one malformed envelope and one eighth type | Contract tests |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 8 consumed | The two admin operations provided; the P1 append and EFS history read, the P3 case reads, the S9 instruction read, the S2 treatment read, the P8 proceeds read and the P4 authorise consumed; one hop, 2 s timeout |
| Kafka | 0 published, 7 types consumed | Four owner topics; inbox dedupe and `.dlt` on every one; DecisionRecorded published by the library |
| Temporal | 2 workflows, 6 activities | LedgerChannelIntakeWorkflow with four activities; EfsLedgerReadWorkflow with three |
| File | None | The EFS rows arrive through the P1 contract, never as a file or a view |

### 13. Solution plan

**Deliverables.** `contract/ledger-intake-events.yaml` (the AsyncAPI document of the seven consumed types with their envelope, key and dedupe key), `contract/ledger-entry-appended.yaml` (the OpenAPI document of the P1 append as consumed, with the entry command and the four answers), `contract/ledger-facts-consumed.yaml` (the P1 EFS history read and the four fact contracts), `contract/outbox-deliveries-admin.yaml` (the two provided operations, the states and the exception rule), `contract/ledger-intake-activities.yaml` (the two workflows, the six activities and the read summary), and the six WireMock mappings.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_integration`; no other schema is read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE facts through rwb-source-data's contract; no view is read here | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case with the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the codes stay rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, owner topics, retry and `.dlt` | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Event-started workflows through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/integration/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in `rwb_integration` | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data; the intake appends through its contract | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-09 | H RWB-PLT-N001-CON |

**Build steps**

1. Write the AsyncAPI document: the seven types, their topics, their owners, the key and the dedupe key of each, and the `.dlt` rule.
2. Write the append contract: `InteractionRequest` 5.1.0, the 201 answer, the 200 repeat answer, the 409 and the ordering rule with the inbox.
3. Write the fact contracts of the P1 EFS history read and of the four owners, with the 404 and 5xx split; carry the placeholder where the source names no path or field.
4. Write the two provided operations: method, path, purpose, right, idempotency, the four states and the exception rule.
5. Write the activity contract: the two workflows, the six activities, the retry policy and the EFS read summary.
6. Write the table ownership statement and the explicit absence of the ledger, the EFS list and the timeline.
7. Build the six WireMock mappings and their fixtures.
8. Add the six contract tests of section 16, including the drift test between each fake and this document.
9. Tag the baseline and collect the sign-off of the app, operations and test stories of this key.

**Done when.** The five contract files validate in the pipeline, the six contract tests pass, the six fakes answer every consumed path and payload, and the app and operations stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | A delivery is in the exception queue after its retries | Not specified in the source documents (GAP-0665; ASM-1173) |
| MSG-GEN-004 | A resend is asked for a delivery not in EXCEPTION, or a workflow runs for the same event | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | A resend is accepted | Not specified in the source documents (GAP-0665; ASM-1173) |
| MSG-P4-002 | A role without Platform administration calls one of the two operations | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | One of the two operations is called without a session (401) | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-003 | A resend names an unknown delivery (404) | This case is not in your scope. |
| MSG-GEN-006 | A dependency of one of the two operations is unavailable (503) | {system} is not available. Try again in a few minutes. |
| MSG-P1-001 | `GET /efs-history` answers 409 | Text per Error and Message Standard v6 |
| MSG-P1-022 | The ledger append answers 503 | Text per Error and Message Standard v6 |
| MSG-PLT-N009-03, -05, -06 | Idempotency header missing or not a UUID; reused or in flight; store unavailable | Text per Error and Message Standard v6 |

The texts of the legacy story are copied unchanged; this contract defines no new message and no new wording, and the rows for 401, 404 and 503 reuse existing message IDs. MSG-P2-001 and MSG-GEN-005 are named by the FSD and the legacy exception flow but their texts are not in the source set, so the placeholder is carried until the Error and Message Standard names them. The Error and Message Standard uses MSG-P2-001 and MSG-GEN-005 with other meanings than the rows above; until it confirms them, those rows keep their placeholder text.

The exception queue screen SCR-09 is not contracted here. Its empty, error and no access states are Not specified in the source documents (DOR-RWB-P2-E2034-CON-10), and its loading state is as stated in section 15.

### 15. Screens and states

None in this story. The two provided operations serve SCR-09 Exception queue, whose fields, states and masking belong to the app story of this key and to RWB-P2-E2034-OPS. The contract fixes only the states a screen may show — PENDING, RETRYING, DELIVERED and EXCEPTION — and the resend action with its 409.

SCR-09 states:
- Empty: Not specified in the source documents (CG-ALL-3243)
- Loading: as Screen Specifications v1, section SCR-09
- Error: Not specified in the source documents (CG-ALL-3243)
- No access: Not specified in the source documents (CG-ALL-3243)

### 16. Test cases

TC-P2-E2034-CON-20. The IDs TC-P2-E2034-CON-01 to TC-P2-E2034-CON-19 below are story-local; Test Cases v9 holds them under the same IDs.

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P2-E2034-CON-01 | AC1 | Contract | The nine sub-tables are present; 12.6 is None; only the five `rwb_integration` objects are named; a sub-table naming another owner's operation fails |
| TC-P2-E2034-CON-02 | AC2 | Contract | One message of each of the seven types validated; a malformed envelope, a message without a business key and an eighth type refused to `.dlt` |
| TC-P2-E2034-CON-03 | AC3 | Component | A delivery followed from attempt 1 to attempt 3: RETRYING, then EXCEPTION with the task for RW-PLATADM, then a resend to PENDING and a 409 on a delivery not in EXCEPTION |
| TC-P2-E2034-CON-04 | AC4 | Contract | `InteractionRequest` 5.1.0 and the four answers 201, 200, 409 and 503; no append for a notice type; no ledger table in 12.7; the append called before the inbox mark |
| TC-P2-E2034-CON-05 | AC5 | Contract | Each of the six fakes compared with its element; every documented error answer reachable; one injected drift fails the test |
| TC-P2-E2034-CON-06 | AC6 | NFR | The boundary test finds no cross-schema statement, no ACE view, no undeclared path and no foreign key out of `rwb_integration` |
| TC-P2-E2034-CON-07 | AC6; ASM-3438 | Contract | Boundary of the 12.7 tables: the five `rwb_integration` tables are the only tables written; `interaction`, `efs_ledger_outcome` and the case timeline are absent; one added table fails |
| TC-P2-E2034-CON-08 | BR1 | Contract | The base `/api/recovery/integration/v1` is declared; a path or topic of another service declared as this service's fails |
| TC-P2-E2034-CON-09 | BR2 | Contract | The seven consumed types are validated on the owners' topics; an eighth type is refused |
| TC-P2-E2034-CON-10 | BR3 | Contract | No ledger table, column or read in the contract; the append is the only ledger call |
| TC-P2-E2034-CON-11 | BR4 | Contract | A repeated business key answers 200 with the existing entry and writes nothing |
| TC-P2-E2034-CON-12 | BR5 | Component | The keys `<EV-nn>:<business key>:v1` and `EFS:<efsRecordKey>` dedupe; the hit count rises on a repeat |
| TC-P2-E2034-CON-13 | BR6 | Component | States PENDING, RETRYING, DELIVERED and EXCEPTION; attempt limit three; a resend from EXCEPTION returns to PENDING with attempt count 0 |
| TC-P2-E2034-CON-14 | BR7 | Contract | Only the two admin operations are declared; the outbound-item operations are absent |
| TC-P2-E2034-CON-15 | BR8 | Component | AceDataReady of ALS COMPLETED starts the EFS read step, another source or status starts nothing; the step is not an outbox delivery and writes its own summary; JOB-01 starts nothing |
| TC-P2-E2034-CON-16 | BR9 | Contract | No business value in the contract; codes, channels, intervals and the attempt limit are reference rows or environment values |
| TC-P2-E2034-CON-17 | BR10 | Contract | No element names a person; the contact point is a key only |
| TC-P2-E2034-CON-18 | AC7 | Contract | Each provided operation with no session answers 401 and with a role without the Platform administration right answers 403; a resend that names an unknown delivery answers 404 |
| TC-P2-E2034-CON-19 | AC8; BR1 to BR10 | Contract | Each rule BR1 to BR10 traced to its test case TC-P2-E2034-CON-08 to TC-P2-E2034-CON-17; a rule with no passing case fails |
| TC-P2-E2034-CON-20 | AC9 | Contract | The efs-history fake rows and 409; the mapped appends; written counted from 201 |

### 17. Guardrails

- No business value in the contract: the event codes, the channels, the directions, the retry intervals and the attempt limit stay rows of reference data and environment values.
- No personal data in an event, a command, an activity input or a fake: identifiers, codes and references only, and the contact point is a key.
- The contract names only rwb-integration's own operations as provided; the P1 append and the fact reads are consumed and are never restated as this service's (DP-01, DP-13).
- One REST base and one topic per service; a document that names another service's base as provided, or a topic outside `rwb.<short>.events.v1`, fails the review (DP-13, DP-14).
- The ledger table, its trigger, the EFS ledger outcome list and the retention classes appear nowhere as objects of this service (DP-18).
- Every example and fixture is synthetic; no production payload, contact point or event is copied into a schema or a fake.
- The envelope, the inbox, the retry topic and the `.dlt` rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-ILG-009 | Contact outcomes from collections reach the ledger | The EFS history read, the CONTACT or PROMISE mapping and the append | TC-P2-E2034-CON-02, TC-P2-E2034-CON-04 |
| REQ-ILG-010 | Dispatched letters write their result, including proof of delivery | The two notice types consumed for accounting; the LETTER entries are rwb-comms's own appends | TC-P2-E2034-CON-02 |
| REQ-ILG-011 | A hand-over names who held the case, who holds it now and when | The two partner types, the HANDOVER and PARTNER_RESULT mappings and the holder references | TC-P2-E2034-CON-02 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline | The occurred time carried unchanged and the append answer the timeline reads | TC-P2-E2034-CON-04 |
| REQ-ILG-013 | Ledger entries carry their own retention class | The retention class declared as the owner's and resolved outside this contract | TC-P2-E2034-CON-04 |
| REQ-ILG-014 | The contact point is a reference and is never copied | `contactKey` only where a fact carries one; no number or address in any element | TC-P2-E2034-CON-04 |
| REQ-ILG-007 | One entry per key; a repeat is ignored and counted | The dedupe key, the inbox record and the repeat answer of the append | TC-P2-E2034-CON-02, TC-P2-E2034-CON-04 |
| REQ-ILG-008 | A failed ledger write loses no entry and the delivery is retried | The four delivery states, the three-attempt rule and the EXCEPTION task | TC-P2-E2034-CON-03 |
| REQ-ILG-006 | The timeline orders entries by occurred time and case sequence | The occurred time of the command and the order declared by rwb-case | TC-P2-E2034-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The eight consumed operations with the 2 s client budget | TC-P2-E2034-CON-06 |

### 19. Out of scope

- The listener, the mapper, the client, the delivery tracker, the two workflows, the controller and the migration (RWB-P2-E2034-APP).
- The Helm values, the consumer groups, the retry scan, the dashboards, the alerts and the runbook (RWB-P2-E2034-OPS).
- The ledger table, its columns, its append-only trigger, the append implementation, the EFS ledger outcome list and the retention classes (the rwb-source-data stories of this legacy key).
- The timeline, the sequence order and the interaction read on the case (the rwb-case stories of this legacy key).
- The masking rule and the scope check implementation (RWB-P4-E1037-CON and the rwb-access stories).
- The partner instruction, the partner result and the portal (the rwb-partner stories of RWB-E2-020 and RWB-E2-021).
- The outbound file items, the WIN and debt-buyer files and the outbound-item resend (RWB-P2-E1007-CON and RWB-P2-E1007-APP).
- The real cross-service proof of the append, the dedup and the exception rule against the live owners (the integration story of this key).
- The field-level completeness of the consumed contracts (GAP-0665).

### Remaining delivery steps

- Settle the account list and workflow ID of the EFS read step (GAP-3376) and who appends the treatment and payment entries (GAP-3377); solution architect.
- Settle GAP-3375.
- Fix the open actor, source and fact field names (GAP-0664, GAP-0665) at contract review (service contract owner).
- Tag the contract baseline, publish the fakes at a pinned version and mark the story Done (service contract owner).
- Size the story at refinement and obtain epic design sign-off (squad lead, solution architect).
- Add the TC-P2-E2034-CON test cases in Test Cases v9 and load test data in DEV (test lead).

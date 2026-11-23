# RWB-S6-E5026-CON Open the buyer data room - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5026-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the buyer data room step of rwb-debtsale, split from RWB-E5-026. It fixes the read `GET /partner/data-room/{lotId}` (API-S6-004) on `/api/recovery/debtsale/v1` (DP-13) with its `DataRoom` answer, the lot, account and tape elements and the four closed lists, the consumed rwb-document, rwb-partner and rwb-case rows, the Partner portal right and the error envelope, the decision-record element of DP-03, the fakes and the absence tests. The plan carries no row for the three consumed reads, for the partner channel or for the lot status of the opening (GAP-2978; ASM-4899 to -7). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the buyer data room step of rwb-debtsale — the data-room read on `/api/recovery/debtsale/v1` with its `DataRoom` answer, the lot, account and tape elements with the four closed lists, the consumed rwb-document, rwb-partner and rwb-case rows, the Partner portal right, the error envelope, the decision-record element and the fakes**, so that **the app story, the buyer panel of rwb-partner and the wave 3 harness build against one fixed, testable contract on Day 1, and a lot property, a list value, a tape field or an answer shape can never drift between rwb-debtsale, rwb-document, rwb-partner and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy opening of RWB-E5-026 crossed four boundaries at once: an officer screen, the masked tape, the buyer panel and the case state. The target splits them: rwb-document owns the tape and its retention, rwb-partner owns the panel and the admission, rwb-case owns the case and its route states, and rwb-debtsale owns the lot and the room. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the lot and account elements of the answer, the four closed lists, the tape reference the answer carries, the panel facts the room opens to, the case state and move, and the record of the decision.

The baseline also fixes the naming the checks require: schema and login `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale` (Template and Rules §R4; context pack). It records that rwb-debtsale holds no `v_ace_*` grant and no grant on `rwb_document`, `rwb_partner` or `rwb_case`, so the three facts are consumed on their owners' contracts only (ASM-4899).

The requirement is REQ-S6-003, "The data room holds a masked data tape, and no unmasked personal data leaves the bank" (FSD S6 Requirements served), and the feature is FEAT-DBS-04 with FEAT-DBS-03 as its prerequisite (Epics 3 to 8 Specification v3). The baseline therefore carries an absence test on the answer itself: no unmasked identifier, name, address, contact value or identity number in a property, an example or a fake.

Six points are carried as gaps and assumptions rather than decided quietly: the plan's C row is None although the step consumes three services (ASM-4899); "qualified buyers" are rwb-partner's panel under R-DS-13 (ASM-4900); the tape is a sibling story's deliverable and its masking is the PII service's (ASM-4901); the case move is answered, not written (ASM-4902); no source names the lot status of the opening (ASM-4903); and the step declares no event although the service owns a topic (ASM-4904), with the partner channel carrying no plan row (ASM-4905).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `document` is P5's, `partner` and `partner_user` are S9's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's table or operation as its own.
- The rwb-document, rwb-partner and rwb-case contracts are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None (GAP-2978; ASM-4899).
- The DEBTSALE route set and its rows R-DS-10 to R-DS-13 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The masked tape exists as the deliverable of RWB-S6-E5025-APP and as a document of rwb-document; this baseline declares its reference and its masking-check outcome and builds no tape (ASM-4901).
- The two lot tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W3` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-debtsale for this step: the data-room read with its path parameter, its answer element, its right and its error responses.
2. Fix the `DataRoom` element: the lot element of DF-SAL-020 to DF-SAL-030, the account element of DF-SAL-031 to DF-SAL-037 and the tape element, with the types, the required flags and the list each property is declared against.
3. Fix the four closed lists and the enumeration of each property.
4. Fix the consumed rows: the tape read of rwb-document, the panel read of rwb-partner and the case read and move answer of rwb-case, with the placeholder where the sources give no name.
5. Record the Partner portal right, the scope of the read, the buyer channel and the two right statements the sources carry.
6. Record the decision-record element of DP-03, written before anything is served.
7. Record the naming baseline, the tables, the boundary and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the error envelope, the absence of a `v_ace_*` read and of a case, document or partner write, the no-personal-data test on the answer, the absence of a published and of a consumed event, and the drift between a fake and the document.
10. Tag the baseline and hand it to RWB-S6-E5026-APP, the buyer panel of rwb-partner and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1, AC2 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has fields the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC4 |
| X5 | A value outside the four lists appears in the document or an example | The vocabulary test fails the build | None | AC3 |
| X6 | The answer or the document carries an unmasked identifier, a name, an address, a contact value or an identity number | The no-personal-data test fails the build and the baseline is not tagged | None | AC2, AC7 |
| X7 | The document declares another service's operation as provided, a `v_ace_*` path, or a `document`, `partner` or `recovery_case` property | The review fails the baseline; the boundary test fails the build | None | AC4, AC7 |
| X8 | The document declares a published or consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X9 | The rights of the operation are not the ones TSD S6 T6.1 and the legacy permission row declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S6 appendices and the published owner contracts of rwb-document, rwb-partner and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operation, the lists, the base, the topic and the queue are fixed by the architecture |
| Valuable | Unblocks RWB-S6-E5026-APP, the buyer panel of rwb-partner and the wave 3 harness on Day 1, and the rwb-document, rwb-partner and rwb-case teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the buyer data room step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of document is P5, of partner and partner_user is S9 and of recovery_case is P3
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The data-room read is declared on the debtsale base with its DataRoom answer and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-debtsale is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /partner/data-room/{lotId} with a DataRoom answer of status 200 under the base /api/recovery/debtsale/v1, owned by rwb-debtsale (API-S6-004)
    Then the operation declares the path parameter lotId and no request body
    Then the four answers 401, 403, 404 and 503 are declared with one envelope and one message ID per condition, and the operation declares no Idempotency-Key
    Then the document declares no other operation of this step and no operation of the lot builder, the award or the bids

  Scenario: AC2 The lot, account and tape elements are fixed and carry no unmasked identifier (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S6 T3.1 and T3.3 and with FSD S6 A2.4
    Then the DataRoom element carries the lot element, one account element per tape row and the tape element
    Then the lot element declares the properties of DF-SAL-020 to DF-SAL-030: id, lot_no, cut_off_date, segment, reserve_price, buyer_partner_id, buyer_class, signing_date, approval_authority, payment_terms and status
    Then the account element declares the properties of DF-SAL-031 to DF-SAL-037: id, lot_id, account_id, borrower_code, outstanding, selling_price and put_back_status
    Then the tape element declares the document reference of the masked tape and its masking-check outcome, read from P5 rwb-document and never copied into rwb_debtsale
    Then the account element carries the masked borrower reference only, and the no-personal-data test fails a property, an example or a fake that adds a name, an address, a contact value or an identity number
    Then the lot properties the partner read withholds before the award are Not specified in the source documents (GAP-2978; ASM-4901) and are settled in the baseline review

  Scenario: AC3 The four closed lists are published as enumerations (new, D-RCV-60)
    Given the vocabulary section of the baseline
    When it is compared with TSD S6 T3.2
    Then LOV-SEGMENT is published with the values RETAIL, SSME and CORPORATE, and segment is declared against it
    Then LOV-BUYER-CLASS is published with the values AMC and NON_AMC, and buyer_class is declared against it
    Then LOV-LOT-STATUS is published with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, and status is declared against it
    Then LOV-PUTBACK is published with the values NONE, CLAIMED, ACCEPTED and REJECTED, and put_back_status is declared against it
    Then no list value is a constant of the code and the vocabulary test fails a value outside the four lists

  Scenario: AC4 The three consumed rows are declared and the other owners' objects stay theirs (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the owner contracts and with the context pack
    Then the masked tape read is declared as consumed from P5 rwb-document, with the document reference, the tape rows and the masking-check outcome
    Then the buyer-panel read is declared as consumed from S9 rwb-partner, with the admitted buyers and the presence of the signed non-disclosure agreement of R-DS-13
    Then the case read and the case-move answer are declared as consumed from P3 rwb-case, with the route state and the move DATA_ROOM_OPEN carrying the rule ID and its version
    Then the operation names of the three rows are Not specified in the source documents (GAP-2978; ASM-4899, ASM-4900, ASM-4901, ASM-4902) and each row carries the placeholder
    Then the document declares no v_ace_* path, no document, partner or recovery_case property and no grant on any rwb_* schema of another owner, and the boundary test fails a build that adds one
    Then every row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The Partner portal right, the scope, the partner channel and the error envelope are fixed (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S6 T6.1, T-A.2 and the legacy permission row of RWB-E5-026
    Then the data-room read declares the Partner portal right R with the scope applied and no other right
    Then the document records that the buyer reads through the partner gateway in the DMZ and the rwb-partner panel under PT-BUYER RU of TSD S6 T6.1, scoped to its own cases (NFR-050)
    Then the document records the legacy permission row as copied: Partner portal, right R, held by RW-CASEOWN, RW-TEAMMGR, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE and 21 more
    Then the answers 401, 403 with MSG-P4-002, 404 and 503 are declared with one envelope, and the read declares no Idempotency-Key
    Then the partner channel and its FAPI 2.0 profile are recorded as an edge dependency with no plan row, not as an element of this document (ASM-4905)

  Scenario: AC6 The decision-record element and the six fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the lot reference, the case references, the tape reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is declared as written through the library on the shared rwb.decision-record.v1 before anything is served, and a failed write changes nothing with MSG-P7-003
    Then the rwb-document fake answers the masked tape "TAPE-2026-000026" of lot "LOT-2026-000026" with its check passed, the same tape with an unmasked identifier found, and no answer beyond 2 s
    Then the rwb-partner fake answers the panel with partner "PT-000026" admitted and its agreement signed, a panel with no signature and a partner out of scope
    Then the rwb-case fake answers the state TAPE_PREPARED and the move DATA_ROOM_OPEN accepted and refused, the package fake answers the route set with R-DS-10 to R-DS-13, the decision-record stub answers a healthy and a stopped chain and the access fake answers a holder and a non-holder of the right
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the base is /api/recovery/debtsale/v1, the topic is rwb.debtsale.events.v1 with its retry and .dlt topics, the queue is rwb-debtsale in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and document, partner, partner_user, recovery_case, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no event published by this step and no event consumed by it, and records that LotAwarded (EV-23) and AccountsTransferred are RWB-S6-E6005-APP's and RWB-S6-E6007-APP's
    Then the absence tests fail a build that declares a second topic, a published or a consumed event, a Schedule or an unmasked identifier on the answer
    Then the document records that the room has no table of its own, is the answer over the two lot tables with the P5 tape, and carries no lot status of the opening because no source names one (GAP-2978; ASM-4903)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E5026-APP and copy no criterion of the legacy story, whose two criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and account records are rwb-debtsale's, and the contract declares their properties, lists and required flags on the lot and account elements only | TSD S6 T3.1, T3.2; context pack ownership rows |
| BR2 | The decision record is declared as an element written before anything is served, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S6 T2; legacy AC1 and AC2 |
| BR3 | The masked tape is rwb-document's object: the contract declares its reference and masking-check outcome as consumed and declares no tape property copied into `rwb_debtsale` | DP-01; ASM-4901 |
| BR4 | The buyer panel and the admission are rwb-partner's: the contract declares them as consumed and declares no `partner` or `partner_user` property and no partner write | R-DS-13; ASM-4900 |
| BR5 | The case move is answered and not written: the contract declares the state read and the answer, and declares no `recovery_case` property and no case row write | TSD S6 T4; ASM-4902 |
| BR6 | This step declares no event: `LotAwarded` (EV-23) and `AccountsTransferred` are other stories', and the opening is a route state and an answer | TSD S6 T5.3; context pack event row; ASM-4904 |
| BR7 | The vocabulary is closed: the four lists are published as enumerated values and no list value is a constant of the code | TSD S6 T3.2; FSD S6 BR-S6-004 |
| BR8 | No unmasked personal data in a schema, an example or a fake: the account element carries the masked borrower reference only, and the masking is the PII service's | REQ-S6-003; FSD S6 A2.3.1; Template and Rules §R7.2 (s17) |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The rule rows of R-DS-10 to R-DS-13, the masking rules and the non-disclosure condition are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; ASM-4901 |
| BR13 | No lot status of the opening is declared as a property value: `LOV-LOT-STATUS` carries no data-room value and no source names one | TSD S6 T3.2; ASM-4903 |
| BR14 | The partner channel is the edge's: the document records the buyer route behind the partner gateway and declares no gateway element of its own | Architecture v5 slide 8; ASM-4905 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The read, the three elements, the four lists, the consumed rows, the right, the record and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the buyer panel of rwb-partner, the wave 3 harness and the rwb-document, rwb-partner and rwb-case owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional account or tape field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC4 and AC7 fail: a `v_ace_*` path, a `document`, `partner` or `recovery_case` property, an event, a second topic, a Schedule or an unmasked identifier | In review |

The route machine the document describes is the app story's and rwb-case's: `TAPE_PREPARED` to `DATA_ROOM_OPEN` under R-DS-13 on the case of record. This baseline fixes the vocabulary of `LOV-LOT-STATUS` and the move it names, and moves no lot and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the partner-channel route of the read and the correction of the plan rows the baseline consumes |
| Consuming teams (the app story, the buyer panel of rwb-partner, the wave 3 harness and the owners of rwb-document, rwb-partner, rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the naming rule, the decision-record library and the shared `rwb.decision-record.v1` topic this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that the tape reference carries no unmasked identifier |

The per-service login behind the security scheme is named "the rwb-debtsale login (DP-02)" and is not part of this baseline. The buyer's entry through the partner gateway is the edge story's and rwb-partner's, and this baseline declares it as the route of the right only (ASM-4905).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| `DataRoom` element | The lot element, one account element per tape row and the tape element |
| Lot element | The properties of DF-SAL-020 to DF-SAL-030: `id`, `lot_no`, `cut_off_date`, `segment`, `reserve_price`, `buyer_partner_id`, `buyer_class`, `signing_date`, `approval_authority`, `payment_terms` and `status` |
| Account element | The properties of DF-SAL-031 to DF-SAL-037: `id`, `lot_id`, `account_id`, `borrower_code`, `outstanding`, `selling_price` and `put_back_status`, with `borrower_code` masked |
| Tape element | The document reference of the masked tape and its masking-check outcome, read from P5 and never copied |
| Lists | `LOV-SEGMENT` (RETAIL, SSME, CORPORATE), `LOV-BUYER-CLASS` (AMC, NON_AMC), `LOV-LOT-STATUS` (BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED) and `LOV-PUTBACK` (NONE, CLAIMED, ACCEPTED, REJECTED), published as enumerations and read at their version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything is served (DP-03) |
| Not declared here | `document` (P5), `partner` and `partner_user` (S9), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), and every `v_ace_*` view (P1) |
| Consumed fields with no source | The operation names of the tape read, the panel read and the case-move answer: Not specified in the source documents (GAP-2978; ASM-4899, ASM-4900, ASM-4901, ASM-4902) |
| Unnamed by the sources | The lot properties the partner read withholds before the award, and the lot status of the opening: Not specified in the source documents (GAP-2978; ASM-4903) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC3 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/partner/data-room/{lotId}` | `DataRoom` of status 200 out, with the lot element, its tape and its account rows (API-S6-004) | Partner portal, right R, scope applied | Not declared |

The operation answers 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope lot and 503, each with the error envelope and one message ID of section 14, and the read declares no `Idempotency-Key`. The operation ID is that of TSD S6 T-A.1 and the path is that of the target base. API-S6-001, API-S6-002, API-S6-003 and API-S6-005 belong to the lot builder, the approval, the award and the bid stories of this service, and none of the four is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of the masked data tape (operation name Not specified in the source documents (GAP-2978; ASM-4901)) | `/api/recovery/document/v1` | P5 rwb-document | The document reference, the tape rows and the masking-check outcome of the lot; faked |
| The buyer-panel read (operation name Not specified in the source documents (GAP-2978; ASM-4900)) | `/api/recovery/partner/v1` | S9 rwb-partner | The admitted buyers and the presence of their signed non-disclosure agreement, as R-DS-13 names them; faked |
| The case read, and the case-move answer (operation name Not specified in the source documents (GAP-2978; ASM-4902)) | `/api/recovery/case/v1` | P3 rwb-case | The route state and the move `DATA_ROOM_OPEN` with the rule ID and its version; on the workflow boundary the move is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry (GAP-2978; ASM-4899).

#### 12.3 Events published

None. The service owns `rwb.debtsale.events.v1`, and its event set carries `LotAwarded` (EV-23) and `AccountsTransferred`. The opening of a data room is not in that event set, so this baseline declares no event for the step, no payload and no consumer, and names the two events as the award and transfer stories'. The absence test of AC7 fails a build that adds one (ASM-4904).

#### 12.4 Events consumed

None. The service's consumed event is `ProceedsMatched` from `rwb.payment.events.v1`; it belongs to the settlement step, not to this one, and the opening is triggered by the tape fact read on the rwb-document contract and by the case signal the parent forwards. This baseline therefore declares no consumer group, no subscription and no inbox of its own (ASM-4904).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, a saga with the transfer as its pivot, the child of `CaseWorkflow` | `rwb-debtsale` in namespace `rwb-recovery` | The saga that hosts the data-room step; its input, its signals and its outcome for the parent are declared, not built |
| `openBuyerDataRoom` | Activity, the one data-room step | `rwb-debtsale` | The case, the lot and the tape fact in; the rule ID with its version, the opening and the case move out |

The service's workflow is `DebtSaleWorkflow` and the Temporal and Drools slides fix it as a saga on `rwb-debtsale` with the transfer as its pivot; the activity name is a target design choice fixed by no source. No activity is registered by this story, and no Schedule is declared for it.

#### 12.6 Schedules

None. The step runs from the tape fact of the lot and from the case signal the parent forwards; the "per cycle" clock of R-DS-13 is the monthly cycle opened under R-DS-01 by RWB-S6-E5023-APP, and this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table for it.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot of accounts offered to debt buyers; the table the lot element of the answer reads |
| debt_sale_account | S6 (`rwb_debtsale`) | An account in a lot; the table the account element of the answer reads |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | The service's outbox; this step declares no row of it (BR6) |

`document` (P5), `partner` and `partner_user` (S9), `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers and rule versions of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document tape fake | The masked tape `TAPE-2026-000026` of lot `LOT-2026-000026` with its check passed and its tape rows; the same tape with an unmasked identifier found; a tape of another lot; no answer beyond 2 s | AC1, AC2, AC4, AC6 |
| rwb-partner panel fake | The panel with partner `PT-000026` admitted and its agreement signed; a panel with no signature; a partner out of scope; no answer beyond 2 s | AC4, AC5, AC6 |
| rwb-case state and move fake | The state `TAPE_PREPARED` for the cases of `LOT-2026-000026`, an accepted move `DATA_ROOM_OPEN` and a refused move | AC4, AC6 |
| rwb-decision rule-package fake | The DEBTSALE route set at its version in force with R-DS-10 to R-DS-13 | AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| Partner portal access fake | A buyer and a role that hold the Partner portal right, and one that does not | AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the tape and panel reads and of the case-move answer carry the placeholder until their owners confirm them (GAP-2978; ASM-4899 to -4).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The data-room read on `/api/recovery/debtsale/v1`; the tape read, the panel read and the case read with the move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record reaches the ledger on `rwb.decision-record.v1` through the library and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `DebtSaleWorkflow` and `openBuyerDataRoom` on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; the tape is a document reference of P5 and the buyer file of INT-25 is delivered on the partner channel (ASM-4901, ASM-4905) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no lot, no case, no tape, no panel and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and six fakes.

**Deliverables.** The additive document `openapi/rwb-debtsale-v1.yaml` with the data-room read, the `DataRoom`, lot, account and tape elements, the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-13 moves the base of the read and nothing else. DP-19 is the screen rule of PRT-05: the screen reads a composed answer and never a service directly; the edge baseline of RWB-PLT-N001-CON fixes the route and the screen model, the staff path is gateway-bff and the buyer path is the partner gateway, and the buyer path has no plan row (ASM-4905). DP-03 is declared as the element written before anything is served. DP-09 is not in the pattern set of this key and no event is declared, so no outbox library row is added (ASM-4904).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries, and leaves out DP-09 because the step publishes no event. The three consumed rows are C dependencies in fact and not in the metadata row (GAP-2978; ASM-4899).

**Build steps**

1. Write the data-room read and validate the additive rule and the error set of AC1 in the pipeline.
2. Write the `DataRoom`, lot, account and tape elements of AC2 with the required flags and the no-personal-data test.
3. Write the four lists of AC3 and the vocabulary test.
4. Record the three consumed rows of AC4 with their owners, budgets and placeholders.
5. Record the Partner portal right, the buyer channel, the legacy permission row and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the six fakes of AC6 and the drift test.
8. Record the naming baseline, the tables and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the contract tests pass, the fakes answer every consumed path and the drift test is green, the no-personal-data test and the event-absence test are green, and the app story, the buyer panel of rwb-partner and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation of an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required path or filter value of the read is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role or the buyer lacks the Partner portal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything is served | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The tape or the data product behind it is stale after a late or failed batch (VR-S6-004-1); the check is the owner's and this service holds no batch-status read | {product} is from {date}. Today's ACE batch has not arrived. |

The five IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P1-001 is carried because it is in the message set of this feature, and the freshness check itself belongs to the data product owner and to rwb-document (ASM-4901).

### 15. Screens and states

The contract serves PRT-05 Data room in its loading state and its three legacy states — **Admitted**, **bidding** and **closed** — all through the edge (DP-19). The route composes the answer of this service for the lot, its tape and its account rows with the rwb-partner panel for the buyer and its admission and with rwb-case for the case; this baseline fixes the rwb-debtsale answer only, and the composite route specification, the buyer channel and the screen field list belong to RWB-PLT-N001-CON and to the edge stories (ASM-4905). The screen itself is the buyer panel of rwb-partner on the buyer path behind the partner gateway. The refusal, not-recorded and stale-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-026-01 | AC1, AC2 | Contract | Lot `LOT-2026-000026` with tape `TAPE-2026-000026`; the contract half answers the read, the `DataRoom` element and its lot, account and tape parts |
| TC-E5-026-02 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path of the element and of the fake |
| TC-E5-026-03 | AC5 | Contract | A buyer and a role without the Partner portal right; the contract half answers the 403 with MSG-P4-002 and the scope of the read |
| TC-E5-026-04 | AC2, AC7 | Contract | A tape with an unmasked identifier and a forced record failure; the contract half answers the no-personal-data test and the absence tests |
| TC-S6-E5026-CON-01 | AC1 | Contract | The document validates; the read, the base, the path parameter, the four error answers and the absent `Idempotency-Key` are present |
| TC-S6-E5026-CON-02 | AC2, AC3 | Contract | The `DataRoom`, lot, account and tape elements validate with their properties and required flags, and the four closed lists validate with their values |
| TC-S6-E5026-CON-03 | AC4, AC5 | Contract | The three consumed rows and their placeholders; the Partner portal right, the buyer channel, the scope and the error envelope |
| TC-S6-E5026-CON-04 | AC6, AC7 | Contract | The six fakes match the document and a drifted fake fails the build; the naming baseline and the absence tests of the tables, the boundary, the events and the personal data |

The four legacy cases are those of RWB-E5-026 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E5026-APP. The legacy `System` level maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E5026-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the four lists, the reserve, the terms, the masking rules and the rule rows stay data, reference data or the route set, never a schema default or an enumeration member of the code.
- No unmasked personal data in a schema, an example or a fake: the account element carries the masked borrower reference only, the no-personal-data test fails a build that adds a name, an address, a contact value or an identity number, and every example is synthetic (REQ-S6-003).
- The tape stays with rwb-document, the panel with rwb-partner and the case with rwb-case: the document declares no `v_ace_*` path, no `document`, `partner`, `partner_user` or `recovery_case` property and no write of those tables (BR3, BR4, BR5).
- The document lists only operations owned by rwb-debtsale; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- Nothing retired is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank (FSD S6 Requirements served); the split plan carries no requirement id for this slice (GAP-2978) | The `DataRoom` element, the tape element and the three consumed rows | TC-E5-026-01, TC-E5-026-04, TC-S6-E5026-CON-01, TC-S6-E5026-CON-02 |
| FEAT-DBS-04 | Open the buyer data room, prerequisite FEAT-DBS-03 (Epics 3 to 8 Specification v3) | The read and its answer | TC-S6-E5026-CON-01, TC-S6-E5026-CON-02 |
| R-DS-13 | TAPE_PREPARED and MASKING_CHECK_PASSED to DATA_ROOM_OPEN for buyers who signed the agreement (Business Rules and Routing Logic v4) | The case state read, the move answer and the panel row | TC-S6-E5026-CON-03 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-S6-E5026-CON-04 |
| ADR-019 | Edge: gateway-bff and partner gateway | The buyer channel and the staff route of PRT-05 | TC-S6-E5026-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S6-E5026-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S6-E5026-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-026, disposition Split (rework); feature FEAT-DBS-04 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S6-E5026-APP; this baseline copies none of them |
| Source text | Legacy RWB-E5-026; FSD S6 Debt sale v3 A2.4; TSD S6 Debt sale v2 T3 to T6 and T-A; Epics 3 to 8 Specification v3 row FEAT-DBS-04; Business Rules and Routing Logic v4 rows R-DS-10 to R-DS-13 |
| Test cases | The four legacy cases as the contract half, and the four new cases TC-S6-E5026-CON-01 to -04 |
| Feature and screens | FEAT-DBS-04, PRT-05 Data room |
| Rules | R-DS-13, with the tape branch R-DS-10 to R-DS-12, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-019, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the read, the evaluation of R-DS-13, the decision record and the case-move answer: RWB-S6-E5026-APP.
- The building of the masked tape, its masking under PDPA and the masking check of R-DS-10 to R-DS-12: RWB-S6-E5025-APP, with the PII service and the policy of rwb-access (P4) (ASM-4901).
- The buyer panel, the partner users, the room admission and the partner gateway: rwb-partner (S9), whose contract this baseline declares as consumed and faked (ASM-4900, ASM-4905).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3) (ASM-4902).
- The lot selection, the pricing, the reserve and the committee approval: RWB-S6-E5023-APP, RWB-S6-E5024-APP and RWB-S6-E6001-APP.
- The buyer qualification, licensing and eligibility check: RWB-S6-E6002-APP.
- The bids, the award and the transfer, `LotAwarded` (EV-23) and `AccountsTransferred`: RWB-S6-E6004-APP, RWB-S6-E6005-APP and RWB-S6-E6007-APP, under API-S6-005 and API-S6-003.
- The document, its custody and its retention: rwb-document (P5).
- The authoring, testing, approval and versioning of the DEBTSALE route set and of R-DS-10 to R-DS-13: rwb-decision (P7).
- The lot status of the opening, which no source names: carried as a gap and an assumption (ASM-4903).
- The composite route, the buyer channel and the screen field list of PRT-05: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

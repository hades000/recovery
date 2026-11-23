# RWB-P6-E4040-CON Record a custody movement of a document

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4040-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-040 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-040 for rwb-comms (P6). The movement of an original is published on Day 1 on base `/api/recovery/comms/v1` with the two notice-side movement operations, the seven-field `Movement`, the notice-side movement reference, the `Idempotency-Key` rule, the error set, the decision-record element, the consumed case event, the consumed custody write and document read of the document hub, the fakes and the drift test; the two legacy criteria stay with RWB-P6-E4040-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-comms (P6)**, I want **the published contract of a custody movement of an original — the base `/api/recovery/comms/v1` with `POST` and `GET /notices/{noticeId}/custody-movements`, the `CustodyMovementRequest` and `Movement` schemas with their seven fields, the holder rule, the notice-side movement reference column, the `Idempotency-Key` rule, the error set, the decision-record element, the consumed case event, the consumed custody write and document read of the document hub, the fakes and the drift test** instead of the monolith's in-process call that kept `document`, `document_custody` and `notice` in one schema, so that **RWB-P6-E4040-APP and the sibling P6 stories build against one frozen, testable shape from Day 1, and a movement field, a status code, a decision element or an event name can never drift between rwb-comms, rwb-document and the decision library without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 addition of the movement resource on the notice: the two operations, their request and answer bodies, their rights and their error set;
- the seven-field `Movement` and the five-field `CustodyMovementRequest`, with the holder rule and the form of the answer;
- the notice-side movement reference as a nullable column of `notice`, and the declaration that no custody table exists in `rwb_comms`;
- the `Idempotency-Key` rule on the write, the additive rule and the versioning rule;
- the decision-record element of a movement (DP-03) and the consumed shapes of the document hub and of the case event;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the movement. The state check, the decision write, the owner call, the notice update and the repeat-key answer are `RWB-P6-E4040-APP`'s; the physical document and every custody row are rwb-document's; the case state is rwb-case's. The document declares shapes and moves nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the legacy key has no operation of its own: the legacy endpoint block of RWB-E4-040 copies the two notice operations of the module, and the movement itself was a row of a `document_custody` table in the same `recovery` schema as the notice. In the target the document and its custody are P5's rows and the notice is P6's, so the one surface that has to be fixed before any code is written is the notice-side answer that carries the movement reference and the movement history.

Three facts make this a baseline and not a summary. The endpoint inventory of TSD P6 holds eleven operations (API-P6-001 to API-P6-011) and none of them is a custody operation, and TSD P6 T3.1 holds `notice`, `template`, `merge_field` and `signature_request` and no custody table, so the two operations and the element rows are this story's own decision and are marked as such (GAP-2382; ASM-3953). The legacy data table gives the custody row as DF-DOC-018 to DF-DOC-024 — seven fields of which the seventh is not named — so the seventh field and the physical types of the other six are carried as placeholders and never guessed (GAP-2382; ASM-3953). And no source gives the decision code or the rule id of a movement, so the element is fixed and its values are the reference data's (GAP-2382; ASM-3953).

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with its retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. The three events the catalogue gives this service (EV-13, EV-14 and EV-15, which TSD P6 T5.3 names `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`) are the notice events of other stories; this document publishes none of them and declares no custody event, because the catalogue has none.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline; where this document narrows them it does so explicitly.
- The notice generation contract RWB-P6-E1052-CON is published, so `notice`, its `document_id` (DF-LEG-017) and its states have one owner document that this addition extends.
- The decision-record library contract RWB-PLT-E1027-CON is the writer, the chain and the outbox of the record this document names (DP-03); its shape is not fixed here.
- The owner rows are taken from the Ownership Map only: `document` and `document_custody` are P5 rwb-document's, `recovery_case` is P3 rwb-case's and the decision ledger is P7 rwb-decision's.
- The custody write of the document hub is the Ownership Map row `POST /documents/{documentId}/custody` (API-P5-007) that RWB-P6-E4040-APP records; no P5 contract story is named in this story's Contract dependencies, so the row is declared as consumed and faked (GAP-2382; ASM-3954).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the addition to the rwb-comms OpenAPI 3.1 document: the movement resource under the notice, the two operations, the request and answer bodies and the error set.
2. Fix the seven movement elements and the five request fields from the legacy data row DF-DOC-018 to DF-DOC-024, with the seventh field and the physical types standing as the placeholder.
3. Fix the holder rule: `held_by` is an organisational role, a team or a location, never a person and never a contact point.
4. Declare the notice-side movement reference column, its nullability and its list of no values, and the absence of a custody table in `rwb_comms`.
5. Write the decision-record element of a movement and the two consumed shapes: the custody write, the document read and the case event.
6. Write the `Idempotency-Key` rule on the write, the additive rule and the compatibility rule.
7. Generate the fake set from the document, wire the drift test into the build of this story and of `RWB-P6-E4040-APP`, and write the absence tests.
8. Publish v1, record the pinned version of each consuming story, and hand the baseline to the app story, to the sibling P6 stories that read the notice and to the document-hub and library owners.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A movement fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | The seventh movement field or a physical type has no value in the sources | The row carries the placeholder and the fake is derived from the published document | None | AC2 |
| X5 | A custody event is declared, or an event is declared on another service's topic | The absence test fails the build; nothing is published | None | AC3 |
| X6 | The document declares a custody table, a query on `rwb_document` or a `v_ace_*` view | The absence test fails the build | None | AC6 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the row is described as consumed and faked | None | AC4 |
| X8 | The decision code or the rule id of a movement is written as a value | The review fails the baseline; the element names the reference data instead | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the notice contract it extends, the Ownership Map rows and the decision library only |
| Negotiable | The two paths, the seventh field and the physical types are settled at the baseline review; the base, the topic, the queue and the naming are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the document-hub and library owners on the same day, and makes a silent field drift impossible |
| Estimable | One additive document change, one element set, one decision element, two consumed shapes, three fakes and ten tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of a custody movement of an original

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the notice contract RWB-P6-E1052-CON is published with the notice resource and its document reference DF-LEG-017

  Scenario: AC1 The two movement operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /notices/{noticeId}/custody-movements answering 201 with Movement and GET /notices/{noticeId}/custody-movements answering 200 with the Movement list, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the POST declares the Idempotency-Key header and a stored answer, and the GET declares no Idempotency-Key
    Then both operations declare the capability area Documents with right C on the POST and right R on the GET, scope applied, a 2 s budget, and the refusals 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition
    Then the document marks both operations as new, because the eleven operations of the TSD P6 inventory API-P6-001 to API-P6-011 hold none for a movement (GAP-2382; ASM-3953)
    Then every added property is additive within major version 1, so a consumer of the notice resource keeps working
    Then the document declares no second base, no second resource and no operation of another service

  Scenario: AC2 The movement element set and the request are fixed and the custody row stays the document hub's (new, D-RCV-60)
    Given the movement element set of the baseline
    When it is compared with the legacy data row DF-DOC-018 to DF-DOC-024 and with the notice row of TSD P6 T3.1
    Then Movement carries id, noticeId, documentId, movedAt, fromLocation, toLocation and heldBy, and the seventh element of the legacy row is carried as the placeholder (GAP-2382; ASM-3953)
    Then CustodyMovementRequest requires documentId, movedAt, fromLocation, toLocation and heldBy, and documentId must equal the document reference DF-LEG-017 of the notice
    Then documentId and noticeId are uuid, as DF-LEG-017 and DF-LEG-015 give them, and the physical type of movedAt, fromLocation, toLocation and heldBy is Not specified in the source documents (GAP-2382; ASM-3953)
    Then heldBy is declared as an organisational role, a team or a location, and no field of the element carries a name, an identity number or a contact point
    Then the notice-side movement reference is declared as a nullable column of notice in rwb_comms, its DF field id standing as Not specified in the source documents (GAP-2382; ASM-3953)
    Then the document declares no custody table in rwb_comms, no column of a custody row and no foreign key across a service boundary, and the custody row is the document hub's row reached on its contract (DP-01)

  Scenario: AC3 The decision-record element is declared and no event of this service is invented (new, D-RCV-60)
    Given the decision and event sections of the baseline
    When they are compared with DP-03, the shared topic and the event catalogue rows of this service
    Then the element carries the notice, the document, the movement reference, the movement date, the from and to locations, the holder, the decision code, the rule id, the rule version, the final call and the decided-at, and it is the local library's element on rwb.decision-record.v1 (DP-03)
    Then the record is written before the change, and a movement whose record cannot be written is not recorded
    Then the decision code and the rule id are declared as reference data read with the version in force and are Not specified in the source documents (GAP-2382; ASM-3955)
    Then the only published row is rwb.decision-record.DecisionRecorded.v1 (EV-08), owned by P7 and written by the library, and the document declares no event of its own
    Then the document declares no custody event, and the three catalogue events EV-13, EV-14 and EV-15 (NoticeGenerated, NoticeDispatched and NoticeDelivered) are named as the notice stories' and never as this document's
    Then no payload carries a name, an address, an identity number or a contact point, and every payload validates with BACKWARD compatibility

  Scenario: AC4 The consumed shapes are declared with their call type and their owner (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are reviewed against the Ownership Map and the connection matrix of Architecture v5 slide 13
    Then the custody write POST /documents/{documentId}/custody (API-P5-007) and the document read are declared as consumed rows of P5 rwb-document, each one hop with a 2 s timeout and a breaker, and each faked
    Then no C dependency row is declared for them, because the plan names no P5 contract story for this key (GAP-2382; ASM-3954)
    Then rwb.case.CaseStateChanged.v1 (EV-05) on rwb.case.events.v1, owned by P3 and keyed by caseId, is declared as consumed inside this service for the state and legal-hold check, with its inbox dedupe (GAP-2382; ASM-3956)
    Then the document declares no operation of another service as provided, no subscription on another service's topic as its own and no file row

  Scenario: AC5 The fakes answer the document and the drift test binds them (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation, the event or the element it serves
    Then the document-hub fake answers the document read with a clean document, a missing document and a disposed document, and the custody write with a movement, a 5xx and an answer delayed beyond 2 s
    Then the case-event fake answers an open case, a closed case, a legal hold and a duplicated event for the inbox
    Then the decision-record library stub answers a healthy chain and outbox, and a stopped chain
    Then the movement fake answers the 201, the 200, the repeated Idempotency-Key and every refusal of AC1
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The nine contract tables, the naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the contract section of this story
    When its nine sub-tables are reviewed against the Template and Rules and the Ownership Map
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty and a reason beside it
    Then the tables named as owned are notice, template and merge_field of rwb_comms with the library objects applied in that schema, and document, document_custody, recovery_case, decision_log_entry, rule_row, template of P7, party and any v_ace_* view are named as other owners' and consumed only through their contracts
    Then the schema is rwb_comms, the base is /api/recovery/comms/v1, the topic is rwb.comms.events.v1 with retry and .dlt topics, the event names are rwb.comms.<Event>.v1, the task queue is rwb-comms in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.comms
    Then no custody table, no column of a custody row, no cross-schema key and no query of this service on rwb_document or on a v_ace_* view is declared, and the absence test fails a build that adds one
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then no workflow, no Schedule and no file element is declared, and the document says why
```

These six criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story and they restate no business outcome of RWB-P6-E4040-APP, which owns AC1 and AC2 of RWB-E4-040.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD P6 T6.2 |
| BR4 | Error responses use one envelope and one message ID per condition; a text the sources do not give carries the placeholder | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | The physical document and every custody row are P5's; this service declares no custody table, no custody column of its own and no cross-schema key | DP-01; Ownership Map (`document` and `document_custody` owned by P5) |
| BR8 | The decision record of a movement is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR9 | No business value is fixed in the contract: the eligible notice states, the location vocabulary, the holder vocabulary, the decision code and the rule id stay data or reference data read with the version in force | FSD P6 A2.19.3.1 (BR-P6-019); Template and Rules §R7.2 s17 |
| BR10 | `held_by` is an organisational role, a team or a location; a personal name, an identity number and a contact point are forbidden in every field of the element | Template and Rules §R7.2 s17; TSD P6 T6.2 |
| BR11 | The custody write of the document hub is consumed and faked, and the C row is added when a P5 contract story is planned | Ownership Map (API-P5-007); Template and Rules §R5.4 |
| BR12 | A movement is refused when the case is under legal hold, because a hold stops every outbound action and every automated decision | Business Rules and Routing Logic v4 R-UNI-20 |
| BR13 | A movement whose decision record cannot be written does not proceed, and an incident is raised | Business Rules and Routing Logic v4 R-UNI-39; legacy RWB-E4-040 AC2 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element set, the decision element and the consumed rows are described | In review |
| In review | Consumer sign-off | `RWB-P6-E4040-APP` and the document-hub and library owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example the seventh movement element once its owner names it | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, a path changes or a refusal status changes | New major version drafted |
| Baselined | Drift in a fake | The drift test fails | In review |
| Baselined | A custody table or a cross-schema read is declared | The absence test of AC6 fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| notice.notice_type | `DEMAND`, `RECALL`, `STATUTORY_SALE_NOTICE`, `GUARANTOR_NOTICE` (LOV-NOTICE, TSD P6 T3.2) | Declared as the list reference; the movement is not a notice type |
| notice delivery_status | `DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING` (LOV-DELIVERY, TSD P6 T3.2) | Declared as the list reference; a movement changes none of them |

The notice state machine and the movement that leaves it unchanged are `RWB-P6-E4040-APP`'s, and the custody row's own state is rwb-document's. This document fixes the surface and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (RWB-P6-E4040-APP, the sibling P6 stories that read the notice, and the rwb-document and P7 library owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the CloudEvents envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element is declared in the movement, in an answer or in a fake |
| Business analyst of P6 | Confirms that the eligible states, the decision code and the rule id are named as reference data and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_comms` by the naming rule of DP-02; the document names the scheme and not a credential. The rights of the two operations are declared here, their role lists are rwb-access data, and no role code is written in the document.

### 11. Data

The contract baseline declares shapes, not business values.

| Element | Legacy field of the custody row | Type and width | Required | List |
|---|---|---|---|---|
| movementId | id, the first of DF-DOC-018 to DF-DOC-024 | uuid | Yes | None |
| noticeId | none in the custody row; DF-LEG-015 of the notice | uuid | Yes | None |
| documentId | the document reference of the row, DF-DOC-018 to DF-DOC-024, equal to DF-LEG-017 | uuid | Yes | None |
| movedAt | moved_at | Not specified in the source documents (GAP-2382; ASM-3953) | Yes | None |
| fromLocation | from_location | Not specified in the source documents (GAP-2382; ASM-3953) | Yes | None |
| toLocation | to_location | Not specified in the source documents (GAP-2382; ASM-3953) | Yes | None |
| heldBy | held_by | Not specified in the source documents (GAP-2382; ASM-3953) | Yes | None |
| the seventh element | the field the legacy data table leaves unnamed | Not specified in the source documents (GAP-2382; ASM-3953) | No | None |
| Standard columns | state, version, created_by, updated_by, is_active of TSD P6 T3.0 | boolean, varchar(40), uuid, boolean | n/a | None |

| Item | Content |
|---|---|
| Request | `CustodyMovementRequest` carries `documentId`, `movedAt`, `fromLocation`, `toLocation` and `heldBy`, all required; `noticeId` comes from the path and `movementId` from the owner's answer |
| Answer | 201 with `Movement` and 200 with the `Movement` list, newest first, each carrying the notice reference |
| Notice-side reference | A nullable column of `notice` in `rwb_comms` that holds the identifier of the latest movement; its DF field id is Not specified in the source documents (GAP-2382; ASM-3953) |
| Decision record | The library's element: the notice, the document, the movement reference, the movement date, the locations, the holder, the decision code, the rule id and version, the final call and the decided-at (DP-03) |
| Holder | A role, a team or a location; no person and no contact point (BR10) |

**No new table and no migration of a table.** `notice`, `template` and `merge_field` are the P6 rows of TSD P6 T3.1 and this document adds one nullable column to `notice` and nothing else; `decision_record`, `idempotency_key`, `outbox_event` and `processed_event` are platform library objects created in `rwb_comms` by the library's migration and are named here, not declared. `document`, `document_custody` (DF-DOC-001 to DF-DOC-011 and DF-DOC-018 to DF-DOC-024), `recovery_case`, `decision_log_entry`, `rule_row`, `party` and every `v_ace_*` view are other owners' and appear only as consumed shapes. `notice.case_id` and `notice.document_id` are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number or an account number. The document, the notice and the movement are reached by identifiers, and `held_by` is organisational.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Both operations are new: no custody operation is in the endpoint inventory of the TSD (GAP-2382; ASM-3953).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| new | POST | `/notices/{noticeId}/custody-movements` | `CustodyMovementRequest`; `noticeId` from the path | 201 with `Movement` | Documents C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| new | GET | `/notices/{noticeId}/custody-movements` | None | 200 with the `Movement` list, newest first | Documents R, scope applied | Not applicable | 401, 403, 404, 503 |

The purpose, the shapes and the refusals are this baseline's own, because no TSD P6 T-A.1 row names a movement; the base and the naming are DP-13's and DP-14's. The two notice operations of the module, API-P6-001 (Litigation C) and API-P6-002 (Litigation R), are `RWB-P6-E1052-CON`'s and are not redeclared here. The capability area and the rights are declared from TSD P6 T6.1, where RW-LEGAL holds Documents CRUA and Litigation RA and RW-LITOFF holds Documents CRU (GAP-2382; ASM-3957).

#### 12.2 REST operations consumed

None declared as an operation of this document; the two rows below are the consumed shapes the app story calls, each one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020).

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The custody write `POST /documents/{documentId}/custody` (API-P5-007) | P5 rwb-document | The request (the document, the movement date, the two locations, the holder) and the answer that carries the owner's movement identifier | Consumed and faked; no C row, because no P5 contract story is named (GAP-2382; ASM-3954) |
| The document read of the rwb-document contract | P5 rwb-document | The answer elements the app check needs: the document exists, its case is the case of the notice, it is not disposed of | The path and the field list are the owner's and are named only as consumed (GAP-2382; ASM-3954) |

No row reads a table, no row reads a `v_ace_*` view, and no row is declared as a provided operation of this service (BR6, BR7).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, rule id, rule version, case, notice, document, movement reference, movement date, locations, holder, decided-at; written by the local decision-record library (DP-03) |

This document declares the element and publishes nothing itself. No custody event is declared: the catalogue of Architecture v5 slide 42 holds none, and EV-13, EV-14 and EV-15 are the notice events of `RWB-P6-E1052-CON` and the dispatch stories.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | caseId, the from and to states and the changed-at, consumed inside rwb-comms so a movement on a closed case or under legal hold is refused, with the inbox dedupe (GAP-2382; ASM-3956) |

The row is consumed by `RWB-P6-E4040-APP`; this baseline fixes its name, its topic and its key (`caseId`) and declares no subscription of its own.

#### 12.5 Workflows and activities

None. A movement is one synchronous write with one library write and one owner call; this document declares no workflow, no child workflow and no activity, and `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is declared: JOB-10 of the catalogue is the daily WIN dispatch of `RWB-P6-E2021-CON`, and no job row is read or changed by this document.

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| notice | `rwb_comms` | P6 | The notice of the original, its `document_id` (DF-LEG-017), its state, and the nullable movement reference of section 11 |
| template | `rwb_comms` | P6 | Read for the notice reference only; written by the template stories |
| merge_field | `rwb_comms` | P6 | Read for the merge codes of the notice only; written by the catalogue story |
| decision_record, idempotency_key, outbox_event, processed_event | `rwb_comms` | PLT library objects applied in this schema | The decision entry of a movement, the stored answer of the POST, the envelope of the published row and the inbox of the consumed row (DP-03) |

`document`, `document_custody`, `document_text`, `document_field`, `document_intake`, `signature_request` and the retention rows are P5's; `recovery_case`, `task`, `timer` and `queue` are P3's; `decision_log_entry`, `rule_row` and the rule package rows are P7's; `party` and the `interaction` rows are P1's; `outbound_item` and `interface_config` are P2's. They are named as consumed answers only, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Movement fake | The two operations of 12.1 | A 201 create with the seven-field `Movement`, a 200 list, the repeated `Idempotency-Key` returning the first answer, and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Document-hub fake | The two rows of 12.2 | A clean document, a missing document, a disposed document; a custody write with a movement, a 5xx and an answer delayed beyond 2 s |
| Case-event fake | The row of 12.4 | An open case, a closed case, a legal hold and a duplicated event for the inbox |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Drift test | Every fake against the document | A drifted fake fails the build |

The document-hub and case fakes are stubbed from the owners' published documents and carry the placeholder where the source is silent (GAP-2382; ASM-3954; ASM-3956).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The movement record and the movement list provided; the custody write and the document read consumed; one hop, 2 s |
| Kafka | 1 declared as written by its owner, 1 consumed | `DecisionRecorded` through the library; `CaseStateChanged`; no custody event |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the addition to `openapi/rwb-comms-v1.yaml` for the movement resource, the `CustodyMovementRequest` and `Movement` schemas in `th.co.scb.ace.workbench.recovery.comms.api`, the notice-column note, the decision-record fragment, the fake set and the drift test. The implementation behind it is `RWB-P6-E4040-APP`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming app story carries the H row |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the movement answer is reached through it and the contract declares no composite route | referred to; the consuming app story and the platform edge story carry the H row |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-01 and DP-15 stand behind the boundary and the notice column as rules and add no dependency. DP-19 is the route the notice screens use and is `RWB-PLT-N001-CON`'s. DP-05 is not in this story's pattern set, because nothing of ACE is read here. This story being a CON story, it holds no build dependency by rule (Template and Rules §R5.7 rule 1).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| MovementOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR6) |
| MovementSchema | Published schema | `CustodyMovementRequest` and `Movement` with the seven elements, the required set and the holder rule (BR9, BR10) |
| NoticeReferenceNote | Resource | The nullable movement reference column of `notice` and the absence of a custody table (BR7) |
| DecisionElement | Document | The decision-record element of a movement on the shared topic (BR8) |
| ConsumedShapes | Document | The custody write and document read of the document hub and the case event, with their placeholders (BR6, BR11) |
| ProblemEnvelope | Reused schema | The platform problem document with its `messageId` extension (BR4) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR3) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers of every consuming build (AC5) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC5, AC6) |

**Database.** One nullable column of `notice` in `rwb_comms`, applied by the service's own Flyway sequence and never editing an applied migration (DP-15); its DF field id is the placeholder of section 11. `document_custody` is not created here and no other schema is named in the note.

**Configuration and reference data.** The eligible notice states, the location vocabulary, the holder vocabulary, the decision code and the rule id are reference data or parameters read with the version in force (BR9). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Add the movement resource and the two operations to the document and lint the paths, the rights and the additive rule (AC1).
2. Write the two schemas with the seven elements, the required set, the holder rule and an example; validate the example (AC2).
3. Write the notice-column note and the absence tests for a custody table and a cross-schema read (AC2, AC6).
4. Write the error section with one message ID per condition and the `Idempotency-Key` rule of the write (AC1).
5. Write the decision element and the two consumed documents' identities with their placeholders (AC3, AC4).
6. Generate the fake set and the drift test and wire the drift test into the build of `RWB-P6-E4040-APP` (AC5).
7. Write the naming and boundary section and the absence tests for the old base, a custody event and a second topic (AC6).
8. Publish v1 and record the pinned version of this contract and of each consuming story.

**Feature flag.** `rwb.comms.custody-movement-contract`.

**Done when.** The document lints, the two schemas validate, the notice-column note applies twice, the fakes answer every status including the repeated key, the absence tests are green and `RWB-P6-E4040-APP` has accepted the baseline.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written by the consuming story (X3, legacy AC2) | 503, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | The notice carries no document reference, or a required property is missing | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| Not specified in the source documents (GAP-2382; ASM-3953) | The notice is outside the eligible states, the document is not returned, or the owner does not answer | A 404, 409 or 503 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |

MSG-P7-003, MSG-P4-002 and MSG-GEN-001 are the three messages of the legacy validation table that this surface raises and are copied unchanged. MSG-P6-001, MSG-P6-003 and MSG-P6-004 belong to the contact stop and the dispatch of a notice and are declared by the dispatch story, not here. The FSD's VR-P6-019-1 names MSG-P1-001 for a stale ACE data product; this document raises none, because it reads no ACE product. No text is invented.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template and its approval states, so it cannot show a movement of an original; the P6 screen list of FSD P6 holds no custody screen. The movement is a fact of the document hub and is shown on the custody surface of rwb-document, whose screen identifier is Not specified in the source documents read here (GAP-2382; ASM-3958), reached through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the movement list and once for the notice reference and merges the answers.

| Surface | State | What this contract serves |
|---|---|---|
| Notice of the original | Approved | The notice reference, its `documentId` and an empty movement list |
| Notice of the original | Out | The notice reference and one `Movement` with `movedAt`, `fromLocation`, `toLocation` and `heldBy` |
| Notice of the original | Returned | The notice reference and the list with both movements, newest first |
| Notice of the original | Refused | The 403 with MSG-P4-002, and the 409 with the placeholder of section 14 |

The route, the merge order, the screen field list and the masking of the holder text belong to `RWB-PLT-N001-CON`; the transitions behind each state are the app story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-040-01 | AC1 | Contract | Notice `N-0101` of case `RC-2026-000321` with document `D-0101`; the contract half answers the 201 `Movement` of seven fields and the 200 list |
| TC-E4-040-02 | AC2 | Contract | Decision log stubbed unavailable; the contract half answers the stopped chain and the 503 of MSG-P7-003 |
| TC-E4-040-03 | Access | Contract | A role without the Documents right sends the POST and the GET; the contract half answers the 403 of MSG-P4-002 |
| TC-E4-040-04 | Principle 5 | Contract | The stopped chain of the library stub on 10 movements; the contract half answers the same 503 and the drift test |
| TC-P6-E4040-CON-01 | AC1 | Contract | The document validates; the two operations, the rights, the `Idempotency-Key` rule, the two new markers and the six refusals are present |
| TC-P6-E4040-CON-02 | AC2 | Contract | The seven elements, the five request fields, the placeholders, the holder rule and the notice column are present; no custody table is declared |
| TC-P6-E4040-CON-03 | AC3 | Contract | The decision element, the reference-data placeholders and the single published row are present; no custody event and no second topic |
| TC-P6-E4040-CON-04 | AC4 | Contract | The two consumed rows with their owner, the one-hop rule and the case event with its key; no provided operation of another service |
| TC-P6-E4040-CON-05 | AC5 | Component | The movement, document-hub and case fakes and the library stub match the document; a drifted fake fails the build |
| TC-P6-E4040-CON-06 | AC6 | Contract | The nine sub-tables with their owners, the naming baseline and the absence tests for a custody table, a `rwb_document` query and a `v_ace_*` view |

The four legacy identifiers keep their legacy order, their legacy covers and their legacy data, and carry the level of the surface they prove here, which is the contract: the legacy table has no level column, and the end-to-end proof of the same cases is RWB-P6-E4040-APP's. The six `TC-P6-E4040-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the eligible states, the location and holder vocabularies, the decision code and the rule id stay data or reference data read with the version in force.
- No personal data in a schema, an example or a fake: identifiers, codes, dates and organisational names only, and `held_by` is a role, a team or a location.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the custody write and the document read are consumed and faked, never declared as provided (DP-01, DP-06 is not applied here).
- No custody table and no cross-schema read: the absence test of AC6 fails a build that declares `document_custody`, a column of it, a query on `rwb_document` or a `v_ace_*` view.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is invented and none of the three catalogue events of this service is claimed: the only published element is the library's `DecisionRecorded` (DP-03).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the seventh element, the four physical types, the notice column's field id, the decision code, the rule id and the refusal texts.
- Every example in the document is synthetic; no production payload, identifier or file is copied into a schema or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-040, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4040-APP; this baseline copies neither |
| Legacy test cases | TC-E4-040-01 to TC-E4-040-04, as the contract half of each case |
| New contract cases | TC-P6-E4040-CON-01 to TC-P6-E4040-CON-06 |
| Legacy feature | FEAT-COM-06 Record a custody movement of a document (FSD P6 A2.19), prerequisite FEAT-DCM-19 of the P5 document hub |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-034; document DF-DOC-001 to DF-DOC-011; document_custody DF-DOC-018 to DF-DOC-024; template DF-REF-045 to DF-REF-051; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015 |
| Decoupling patterns | DP03, DP13, DP19 (DP-01 and DP-15 applied as rules, DP-11 in the consumed rows) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-20 (legal hold stops the action), R-UNI-39 (no action proceeds unlogged), BR-P6-019 and VR-P6-019-1 of FSD P6 A2.19.3.1 |
| Requirements | Not mapped: the P6 requirement list holds no requirement for FEAT-COM-06, and REQ-OCC-001 to REQ-OCC-011 name the notice and self-service features (GAP-2382; ASM-3953) |

### 19. Out of scope

- The implementation of the two operations, the notice check, the decision write, the owner call and the repeat-key answer (RWB-P6-E4040-APP).
- The physical document and every custody row: P5 rwb-document, `document`, `document_custody` and API-P5-007, with the P5 stories that build the hub.
- The retention classes and periods and the `retention_rule` and `retention_action` rows: P5 rwb-document, with RWB-P6-E4042-CON on the notice side.
- The decision-record library, its chain and its outbox (RWB-PLT-E1027-CON and the RWB-PLT-LIB stories); this baseline names the element and writes none of it.
- The case state, its closure and the legal hold as a case fact (P3 rwb-case and R-UNI-20).
- The dispatch of a notice, JOB-10, the WIN file and `NoticeDispatchWorkflow` (RWB-P6-E2021-CON and RWB-P6-E2022-CON).
- The answer to a legal or audit document request (RWB-P6-E4041-CON) and the template and merge-field administration (RWB-P6-E1046-CON and RWB-P6-AD017-CON).
- The gateway-bff composite route, the screen field list and the masking at the edge (RWB-PLT-N001-CON), and the legacy screen SCR-33 Template approval, which the key names and which shows no movement.
- The decision code and the rule id of a movement, the eligible states, the location and holder vocabularies and the refusal texts: the owners of the parameters, the reference data and the message list.

# RWB-P6-E4038-CON Raise a dispute in self-service

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4038-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-038 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-038 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-comms (P6)**, I want **the published contract of a self-service dispute — the base `/api/recovery/comms/v1` with `POST` and `GET /notices/{noticeId}/disputes`, the `DisputeRequest` and `Dispute` schemas, the `notice_dispute` row and the `hold_reason` carrier of the contact stop, the `Idempotency-Key` rule, the error set, the decision-record element, the two consumed deviation events, the consumed deviation create and customer read, the fakes and the drift test** instead of the monolith's in-process call that kept `deviation`, `notice` and `decision_log_entry` in one schema, so that **RWB-P6-E4038-APP and the sibling P6 stories build against one frozen, testable shape from Day 1, and a dispute field, a status code, a decision element or an event name can never drift between rwb-comms, rwb-deviation, rwb-source-data and the decision library without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 addition of the dispute resource on the notice: the two operations, their request and answer bodies, their rights and their error set;
- the `Dispute` and `DisputeRequest` elements and the new `notice_dispute` row, with the element names, types and required flags fixed here and marked where no source names them;
- `notice.hold_reason` (DF-LEG-032) as the carrier of the contact stop, and the declaration that no deviation and no case table exists in `rwb_comms`;
- the `Idempotency-Key` rule on the write, the additive rule and the versioning rule;
- the decision-record element of a dispute (DP-03), the two consumed deviation events and the two consumed shapes of rwb-deviation and rwb-source-data;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the dispute. The notice checks, the decision write, the owner call, the row and the hold, and the lift from `DeviationCleared` are `RWB-P6-E4038-APP`'s; the deviation and its pause are rwb-deviation's; the customer, contact and consent facts are rwb-source-data's; the case state and its clocks are rwb-case's. The document declares shapes and raises nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the legacy key has no operation of its own: the endpoint block of RWB-E4-038 names the two notice administration operations of the module, and the dispute itself was a row of a `deviation` table in the same schema as the notice, written through the in-process decision log and read through an ACE view. In the target the deviation is S8's, the customer data is P1's and the notice is P6's, so the one surface that has to be fixed before any code is written is the notice-side answer that carries the dispute, its state and the owner's deviation reference.

Four facts make this a baseline and not a summary. The endpoint inventory of TSD P6 holds eleven operations, API-P6-001 to API-P6-011, and none of them is a dispute operation, and TSD P6 T3.1 holds `notice`, `template`, `merge_field` and `signature_request` and no dispute table, so the two operations and the new row are this story's own decision and are marked as such (GAP-1112; ASM-2060). The field catalogue of FSD P6 A2.17.3.2 lists notice fields only, so the dispute element names, their physical types and their required flags are the baseline's and carry the placeholder wherever no source names them (GAP-1112; ASM-2060). No source publishes a deviation operation that raises X1 for a customer dispute, so the row is consumed and faked and no contract dependency is declared (GAP-1113; ASM-2061). And no source gives the customer principal, the reason codes, the decision code, the rule id or the refusal texts, so the rights, the values and the texts stay reference data and placeholders and are never guessed (GAP-1114, GAP-1117; ASM-2062, ASM-2065).

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with its retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. The three events the catalogue gives this service (EV-13, EV-14 and EV-15, which TSD P6 T5.3 names `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`) are the notice events of other stories; this document publishes none of them and declares no dispute event, because the catalogue of Architecture v5 slide 42 has none.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline; where this document narrows them it does so explicitly.
- The notice generation and dispatch contract RWB-P6-E1052-CON and RWB-P6-E2021-CON are published, so `notice`, its `party_id` (DF-LEG-030), its `delivery_status` (DF-LEG-022) and its `hold_reason` (DF-LEG-032) have one owner document that this addition extends.
- The decision-record library contract RWB-PLT-E1027-CON is the writer, the chain and the outbox of the record this document names (DP-03); its shape is not fixed here.
- The owner rows are taken from the Ownership Map only: `deviation` is S8 rwb-deviation's, `recovery_case`, `task` and `timer` are P3 rwb-case's, `party_ext` and `contact_point_ext` are P1 rwb-source-data's and the decision ledger is P7 rwb-decision's.
- The deviation create of the Ownership Map row `POST /cases/{caseId}/deviations` (S8) and the customer read of the row `GET /customers/{id}` (P1) are the two consumed shapes RWB-P6-E4038-APP calls; no S8 contract story and no P1 contract story is named in this story's Contract dependencies, so both are declared as consumed and faked (GAP-1113; ASM-2061).
- The two deviation events `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` are the rows Architecture v5 slide 17 and the event catalogue of slide 42 give this service for the contact stop; their payload detail is the owner's and is declared here as the consumer's element only (GAP-1116; ASM-2064).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the addition to the rwb-comms OpenAPI 3.1 document: the dispute resource under the notice, the two operations, the request and answer bodies, the rights and the error set.
2. Fix the `Dispute` and `DisputeRequest` elements and the `notice_dispute` row, with the names, the physical types and the required flags where the sources are silent standing as the placeholder.
3. Declare `notice.hold_reason` (DF-LEG-032) as the carrier of the contact stop, its thirty characters, its nullability, and the absence of any deviation or case table in `rwb_comms`.
4. Write the decision-record element of a dispute and the four consumed shapes: the two deviation events, the deviation create and the customer read.
5. Write the `Idempotency-Key` rule on the write, the 202 answer of an unanswered deviation, the additive rule and the compatibility rule.
6. Generate the fake set from the document, wire the drift test into the build of this story and of `RWB-P6-E4038-APP`, and write the absence tests.
7. Publish v1, record the pinned version of each consuming story, and hand the baseline to the app story, to the sibling P6 stories that read the notice and to the rwb-deviation, rwb-source-data and library owners.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A dispute fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | An element name, a physical type or a required flag has no value in the sources | The row carries the placeholder and the fake is derived from the published document | None | AC2 |
| X5 | A dispute event or a second topic is declared as this document's | The absence test fails the build; nothing is published | None | AC3 |
| X6 | The document declares a deviation table, a case table, a query on `rwb_deviation` or `rwb_case`, or a `v_ace_*` view | The absence test fails the build | None | AC6 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the row is described as consumed and faked | None | AC4 |
| X8 | A reason code, the decision code or the rule id is written as a value | The review fails the baseline; the element names the reference data instead | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the notice contract it extends, the Ownership Map rows, the two owner events and the decision library only |
| Negotiable | The two paths, the element names, the types and the required flags are settled at the baseline review; the base, the topic, the queue and the naming are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the rwb-deviation, rwb-source-data and library owners on the same day, and makes a silent field drift impossible |
| Estimable | One additive document change, two schemas, one new row, one decision element, four consumed shapes, four fakes and ten tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of a self-service dispute

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the notice contract RWB-P6-E1052-CON is published with the notice resource, its party reference DF-LEG-030 and its hold reason DF-LEG-032

  Scenario: AC1 The two dispute operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /notices/{noticeId}/disputes answering 201 with Dispute and 202 when the deviation owner has not answered, and GET /notices/{noticeId}/disputes answering 200 with the Dispute list, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the POST declares the Idempotency-Key header and a stored answer, and the GET declares no Idempotency-Key
    Then both operations declare the capability area Documents with right C on the POST and right R on the GET, scope applied, a 2 s budget, and the refusals 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition
    Then the document marks both operations as new, because the eleven operations of the TSD P6 inventory API-P6-001 to API-P6-011 hold none for a dispute (GAP-1112; ASM-2060)
    Then the document records that the rights matrix has no customer row, so the customer principal of the self-service channel is declared as the edge's and is not written as a role code here (GAP-1114; ASM-2062)
    Then every added property is additive within major version 1, so a consumer of the notice resource keeps working
    Then the document declares no second base, no second resource and no operation of another service

  Scenario: AC2 The dispute element set and the new notice-side row are fixed and the deviation row stays the owner's (new, D-RCV-60)
    Given the dispute element set and the new row of the baseline
    When they are compared with the legacy data rows DF-CAS-036 to DF-CAS-045 and DF-ACE-055 to DF-ACE-074, the field catalogue of FSD P6 A2.17.3.2 and the notice row of TSD P6 T3.1
    Then Dispute carries the dispute identifier, noticeId, caseId, channel, reasonCode, raisedAt, state and the owner's deviation reference, and every name, physical type and required flag the sources do not give is carried as the placeholder (GAP-1112; ASM-2060)
    Then DisputeRequest requires channel, taken from LOV-CHANNEL, and reasonCode, taken from the reason-code list in force, and declares no field that carries a name, an address, an identity number or free text of a person
    Then noticeId, caseId and the dispute identifier are uuid, as DF-LEG-015, DF-LEG-016 and the standard columns give them, and the physical type of raisedAt, channel and the deviation reference is Not specified in the source documents (GAP-1112; ASM-2060)
    Then the dispute is declared as the new table notice_dispute of rwb_comms, with its standard columns of TSD P6 T3.0, its state list referring to reference data and its DF field ids standing as Not specified in the source documents (GAP-1112; ASM-2060)
    Then notice.hold_reason (DF-LEG-032, varchar(30), not required) is declared as the carrier of the contact stop, set on the raise and cleared on the lift (GAP-1116; ASM-2064)
    Then the document declares no deviation table, no recovery_case table, no column of either and no foreign key across a service boundary, and the deviation row is the owner's row reached on its contract (DP-01)

  Scenario: AC3 The decision-record element is declared and no event of this service is invented (new, D-RCV-60)
    Given the decision and event sections of the baseline
    When they are compared with DP-03, the shared topic and the catalogue rows of this service
    Then the element carries the case, the notice, the dispute, the deviation reference, the channel, the reason code, the decision code, the rule id, the rule version, the final call and the decided-at, and it is the local library's element on rwb.decision-record.v1 (DP-03)
    Then the record is written before the change, and a dispute whose record cannot be written is not recorded
    Then the reason codes, the decision code and the rule id are declared as reference data read with the version in force and are Not specified in the source documents (GAP-1117; ASM-2065)
    Then the only published row is rwb.decision-record.DecisionRecorded.v1 (EV-08), owned by P7 and written by the library, and the document declares no event of its own
    Then the document declares no dispute event, and the three catalogue events EV-13, EV-14 and EV-15 (NoticeGenerated, NoticeDispatched and NoticeDelivered) are named as the notice stories' and never as this document's
    Then no payload carries a name, an address, an identity number or a contact point, and every payload validates with BACKWARD compatibility

  Scenario: AC4 The consumed shapes are declared with their call type and their owner (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are reviewed against the Ownership Map and the connection matrix of Architecture v5 slide 13
    Then the deviation create POST /cases/{caseId}/deviations and the customer read GET /customers/{id} are declared as consumed rows of S8 rwb-deviation and P1 rwb-source-data, each one hop with a 2 s timeout and a breaker, and each faked
    Then no C dependency row is declared for them, because the plan names no S8 contract story and no P1 contract story for this key (GAP-1113; ASM-2061)
    Then rwb.deviation.DeviationRaised.v1 (EV-06) and rwb.deviation.DeviationCleared.v1 (EV-07) on rwb.deviation.events.v1, owned by S8, are declared as consumed with the contact-stop and lift use of Architecture v5 slide 17 and the inbox dedupe (GAP-1116; ASM-2064)
    Then the document declares no operation of another service as provided, no subscription on another service's topic as its own and no file row

  Scenario: AC5 The fakes answer the document and the drift test binds them (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation, the event or the element it serves
    Then the deviation fake answers a raise with a deviation and its reference, a duplicate raise, a cleared deviation, a 5xx and an answer delayed beyond 2 s
    Then the source-data fake answers a party of the case with its contact and consent facts, a missing party and a channel without consent
    Then the deviation-event fake answers a raised event, a cleared event and a duplicated event for the inbox
    Then the decision-record library stub answers a healthy chain and outbox, and a stopped chain
    Then the dispute fake answers the 201, the 202, the 200 list, the repeated Idempotency-Key and every refusal of AC1
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The nine contract tables, the naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the contract section of this story
    When its nine sub-tables are reviewed against the Template and Rules and the Ownership Map
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty and a reason beside it
    Then the tables named as owned are notice, notice_dispute, template and merge_field of rwb_comms with the library objects applied in that schema, and deviation, recovery_case, task, timer, party_ext, contact_point_ext, decision_log_entry, rule_row and any v_ace_* view are named as other owners' and consumed only through their contracts
    Then the schema is rwb_comms, the base is /api/recovery/comms/v1, the topic is rwb.comms.events.v1 with retry and .dlt topics, the event names are rwb.comms.<Event>.v1, the task queue is rwb-comms in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.comms
    Then no deviation table, no case table, no cross-schema key and no query of this service on rwb_deviation, rwb_case or a v_ace_* view is declared, and the absence test fails a build that adds one
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then no workflow, no Schedule and no file element is declared, and the document says why
```

These six criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story and they restate no business outcome of RWB-P6-E4038-APP, which owns AC1 and AC2 of RWB-E4-038.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD P6 T6.2 |
| BR4 | Error responses use one envelope and one message ID per condition; a text the sources do not give carries the placeholder | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | The deviation and the case are other owners' rows: no deviation table, no case table and no cross-schema key is declared here | DP-01; Ownership Map (`deviation` owned by S8, `recovery_case` by P3) |
| BR8 | Every ACE fact of the customer, the contact points and the consent state arrives on rwb-source-data's contract; this service declares no ACE view and no extension table | DP-05; Architecture v5 slides 13 and 20; Ownership Map (`party_ext`, `contact_point_ext` owned by P1) |
| BR9 | The decision record of a dispute is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR10 | The contact stop and its lift are the deviation owner's events; the document declares the consumer's element and publishes nothing for them | Architecture v5 slide 17 ("events DeviationRaised / Cleared (contact stop)"); slide 42 (events 06 and 07) |
| BR11 | No business value is fixed in the contract: the reason codes, the channel list, the dispute state list, the decision code and the rule id stay data or reference data read with the version in force | FSD P6 A2.17.3.1 (BR-P6-017); Template and Rules §R7.2 s17 |
| BR12 | No element of the contract carries a name, an address, an identity number, an account number or a contact point; the channel and the reason code are codes only | Template and Rules §R7.2 s17; TSD P6 T6.2 |
| BR13 | A dispute whose record cannot be written is not recorded, and every accepted dispute carries one decision record | R-UNI-39; legacy RWB-E4-038 AC2 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element set, the new row, the decision element and the consumed rows are described | In review |
| In review | Consumer sign-off | `RWB-P6-E4038-APP` and the rwb-deviation, rwb-source-data and library owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an element name once its owner names it | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, a path changes, a status changes or the state list changes | New major version drafted |
| Baselined | Drift in a fake | The drift test fails | In review |
| Baselined | A deviation table, a case table or a cross-schema read is declared | The absence test of AC6 fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| dispute.channel | `MOBILE`, `HOME_PHONE`, `WORK_PHONE`, `LINE`, `EMAIL`, `POSTAL_ADDRESS`, `CALL`, `VISIT`, `SMS`, `LETTER`, `PORTAL`, `BRANCH` (LOV-CHANNEL, TSD P6 T3.2) | Declared as the list reference of the channel of a dispute; the self-service channels of FSD P6 A2.17.2 are LINE OA and HOME.SCB, which map to `LINE` and `PORTAL` |
| notice.delivery_status | `DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING` (LOV-DELIVERY, TSD P6 T3.2) | Declared as the list reference; a dispute changes none of them |

The state vocabulary of a `notice_dispute` row is Not specified in the source documents (GAP-1112; ASM-2060) and is declared as a reference-data list, not as values of this document. The transitions of a dispute and of the stop are `RWB-P6-E4038-APP`'s, and the deviation's own states are rwb-deviation's. This document fixes the surface and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (RWB-P6-E4038-APP, the sibling P6 stories that read the notice, and the rwb-deviation, rwb-source-data and P7 library owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the CloudEvents envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element is declared in the dispute, in an answer or in a fake, and that the customer data of the case is reached only on rwb-source-data's contract |
| Business analyst of P6 | Confirms that the reason codes, the state list, the decision code and the rule id are named as reference data and that no member list is curated locally |
| Access owner of gateway-bff | Confirms that the customer principal of the self-service channel is the edge's and that the capability area and the rights of the two operations are declared here without a role code (GAP-1114; ASM-2062) |

The login behind the document's security scheme is `rwb_comms` by the naming rule of DP-02; the document names the scheme and not a credential. The rights of the two operations are declared here, their role lists are rwb-access data, and no role code is written in the document.

### 11. Data

The contract baseline declares shapes, not business values.

| Element | Legacy source | Type and width | Required | List |
|---|---|---|---|---|
| disputeId | none in the legacy rows; the identifier of the dispute row | uuid | Yes | None |
| noticeId | DF-LEG-015 of the notice | uuid | Yes | None |
| caseId | DF-LEG-016 of the notice, and `case_id` of the deviation row | uuid | Yes | None |
| channel | the channel of the request in FSD P6 A2.17.2 (LINE OA, HOME.SCB) | Not specified in the source documents (GAP-1112; ASM-2060) | Yes | LOV-CHANNEL (TSD P6 T3.2) |
| reasonCode | none; the feature describes a dispute and gives no code list | Not specified in the source documents (GAP-1112; ASM-2060) | Yes | The reason-code list in force, a reference-data list |
| raisedAt | none; the nearest legacy field is `raised_at` of the deviation row, DF-CAS-036 to DF-CAS-045 | Not specified in the source documents (GAP-1112; ASM-2060) | Yes | None |
| state | the standard `state` column of TSD P6 T3.0 | varchar(40) | Yes | The dispute state list in force, a reference-data list |
| deviationRef | `id` of the deviation row, DF-CAS-036 to DF-CAS-045, as the owner answers it | Not specified in the source documents (GAP-1113; ASM-2061) | No, until the owner answers | None |
| the fields of the `notice_dispute` row | no legacy row exists | The standard columns of TSD P6 T3.0 plus the elements above; every type and required flag the sources do not give is Not specified in the source documents (GAP-1112; ASM-2060) | As above | As above |

| Item | Content |
|---|---|
| Request | `DisputeRequest` carries `channel` and `reasonCode`, both required; `noticeId` comes from the path, `caseId` from the notice and the identifiers from this service |
| Answer | 201 with `Dispute` when the deviation owner answered, 202 with the same body and no deviation reference when it did not, and 200 with the `Dispute` list, newest first, each carrying the notice reference |
| Notice-side carrier | `notice.hold_reason` (DF-LEG-032, varchar(30), not required) holds the contact stop of the answered deviation; it exists in TSD P6 T3.1 and is written, not created |
| Decision record | The library's element: the case, the notice, the dispute, the deviation reference, the channel, the reason code, the decision code, the rule id and version, the final call and the decided-at (DP-03) |
| Personal data | None: identifiers, codes and dates only, and the channel and the reason code are codes (BR12) |

**One new table and no migration of another owner's table.** `notice`, `template` and `merge_field` are the P6 rows of TSD P6 T3.1 and this document adds the `notice_dispute` table of section 11 and nothing else; `decision_record`, `idempotency_key`, `outbox_event` and `processed_event` are platform library objects created in `rwb_comms` by the library's migration and are named here, not declared. `deviation` (DF-CAS-036 to DF-CAS-045), `recovery_case`, `task`, `timer`, `party_ext`, `contact_point_ext` (DF-ACE-055 to DF-ACE-074), `decision_log_entry`, `rule_row` and every `v_ace_*` view are other owners' and appear only as consumed shapes. `notice.case_id`, `notice.party_id` and the deviation reference of a dispute are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number, an account number or a contact point. The notice, the case, the party and the deviation are reached by identifiers, the channel is a code of LOV-CHANNEL and the reason code is a reference-data code.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Both operations are new: no dispute operation is in the endpoint inventory of the TSD (GAP-1112; ASM-2060).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| new | POST | `/notices/{noticeId}/disputes` | `DisputeRequest`; `noticeId` from the path | 201 with `Dispute`, or 202 when the deviation owner has not answered | Documents C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| new | GET | `/notices/{noticeId}/disputes` | None | 200 with the `Dispute` list, newest first | Documents R, scope applied | Not applicable | 401, 403, 404, 503 |

The purpose, the shapes and the refusals are this baseline's own, because no TSD P6 T-A.1 row names a dispute; the base and the naming are DP-13's and DP-14's. The two notice operations of the module, API-P6-001 (Litigation C) and API-P6-002 (Litigation R), are `RWB-P6-E1052-CON`'s and are not redeclared here. The capability area and the rights are declared from TSD P6 T6.1, where RW-COMPLAIN holds Documents CRU and Litigation R and the Documents column carries C, R, U and A across the staff and partner rows (GAP-1112; ASM-2060). The customer principal of the self-service channel has no row in that matrix and is named as the edge's (GAP-1114; ASM-2062).

#### 12.2 REST operations consumed

None declared as an operation of this document; the two rows below are the consumed shapes the app story calls, each one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020).

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The deviation create of the rwb-deviation contract (Ownership Map row `POST /cases/{caseId}/deviations`) | S8 rwb-deviation | The request (the case, the notice, the dispute, the channel and the reason code) and the answer that carries the owner's deviation identifier and state | Consumed and faked; no C row, because no S8 contract story is named (GAP-1113; ASM-2061) |
| The customer read of the rwb-source-data contract (Ownership Map row `GET /customers/{id}`) | P1 rwb-source-data | The answer elements the app check needs: the party of the notice, its contact points and the consent state of the channel | Consumed and faked through DP-05; the field list is the owner's and is named only as consumed (GAP-1113; ASM-2061) |

No row reads a table, no row reads a `v_ace_*` view of this service, and no row is declared as a provided operation of this service (BR6, BR7, BR8).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, rule id, rule version, case, notice, dispute, deviation reference, channel, reason code, decided-at; written by the local decision-record library (DP-03) |

This document declares the element and publishes nothing itself. No dispute event is declared: the catalogue of Architecture v5 slide 42 holds none, and EV-13, EV-14 and EV-15 are the notice events of `RWB-P6-E1052-CON`, `RWB-P6-E2021-CON` and the dispatch stories.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | The case, the deviation and its code, the raised-at and the pause it carries, consumed inside rwb-comms so the contact stop is applied to the outbound contact of the notice; keyed by the case of the deviation as the local projection needs; inbox dedupe (GAP-1116; ASM-2064) |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | The case, the deviation and the cleared-at, consumed so the stop is lifted and the outbound contact resumes on the permitted channels (R-UNI-44); same key and same dedupe; same gap |

The two rows are given to this service by Architecture v5 slide 17 with the words "contact stop" and are the only deviation rows this contract consumes; `TreatmentApproved` (EV-10) and `PaymentMissed` (EV-12) are the other rows of that slide and belong to the treatment and payment stories. The rows are consumed by `RWB-P6-E4038-APP`; this baseline fixes their name, their topic and the elements the consumer reads, and declares no subscription of its own.

#### 12.5 Workflows and activities

None. A dispute is one synchronous write with one library write and two owner calls; this document declares no workflow, no child workflow and no activity, and `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is declared: JOB-10 of the catalogue is the daily WIN dispatch of `RWB-P6-E2021-CON` and no job row is read or changed by this document.

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| notice | `rwb_comms` | P6 | The notice of the dispute, its `case_id` (DF-LEG-016), its `party_id` (DF-LEG-030), its `delivery_status` (DF-LEG-022) and the `hold_reason` (DF-LEG-032) that carries the contact stop |
| notice_dispute | `rwb_comms` | P6 | The dispute row of section 11, its standard columns and its reference-data state list |
| template | `rwb_comms` | P6 | Read for the notice reference only; written by the template stories |
| merge_field | `rwb_comms` | P6 | Read for the merge codes of the notice only; written by the catalogue story |
| decision_record, idempotency_key, outbox_event, processed_event | `rwb_comms` | PLT library objects applied in this schema | The decision entry of a dispute, the stored answer of the POST, the envelope of the published row and the inbox of the two consumed rows (DP-03, DP-09) |

`deviation` and the deviation handling rows are S8's; `recovery_case`, `task`, `timer`, `queue` and `assignment` are P3's; `party_ext` and `contact_point_ext` are P1's; `decision_log_entry`, `rule_row` and the rule package rows are P7's; `outbound_item` and `interface_config` are P2's; `document` and its custody rows are P5's. They are named as consumed answers only, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Dispute fake | The two operations of 12.1 | A 201 create with the `Dispute`, a 202 with no deviation reference, a 200 list, the repeated `Idempotency-Key` returning the first answer, and the 401, 403, 404, 409, 422 and 503 refusals |
| Deviation fake | The first row of 12.2 | A raise with a deviation and its reference, a duplicate raise answering the first deviation, a raised deviation whose state is cleared, a 5xx and an answer delayed beyond 2 s |
| Source-data fake | The second row of 12.2 | A party of the case with its contact points and the consent state of the channel, a missing party and a channel without consent |
| Deviation-event fake | The two rows of 12.4 | A raised event, a cleared event and a duplicated event for the inbox |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Drift test | Every fake against the document | A drifted fake fails the build |

The deviation, source-data and event fakes are stubbed from the owners' published documents where they exist and carry the placeholder where the source is silent (GAP-1113, GAP-1116; ASM-2061, ASM-2064).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The dispute record and the dispute list provided; the deviation create and the customer read consumed; one hop, 2 s |
| Kafka | 1 declared as written by its owner, 2 consumed | `DecisionRecorded` through the library; `DeviationRaised` and `DeviationCleared`; no dispute event |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the addition to `openapi/rwb-comms-v1.yaml` for the dispute resource, the `DisputeRequest` and `Dispute` schemas in `th.co.scb.ace.workbench.recovery.comms.api`, the `notice_dispute` note, the `hold_reason` note, the decision-record fragment, the fake set and the drift test. The implementation behind it is `RWB-P6-E4038-APP`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming app story carries the H row |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract; the document declares the consumed customer read and no view of its own | none |
| DP-13 | the monolith base `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the dispute answer is reached through it and the contract declares no composite route | referred to; the consuming app story and the platform edge story carry the H row |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-05 is named because the customer and consent facts of the legacy `v_ace_customer` read are consumed here on rwb-source-data's contract and add no dependency. DP-01 and DP-15 stand behind the boundary and the new row as rules and add no dependency. DP-19 is the route the customer channel and the notice screen use and is `RWB-PLT-N001-CON`'s. This story being a CON story, it holds no build dependency by rule (Template and Rules §R5.7 rule 1).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DisputeOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR6) |
| DisputeSchema | Published schema | `DisputeRequest` and `Dispute` with the elements of section 11, the required set and the code-only rule (BR11, BR12) |
| NoticeDisputeRow | Resource | The `notice_dispute` table with its standard columns and its reference-data state list, and the absence of a deviation and a case table (BR7) |
| ContactStopCarrier | Resource | `notice.hold_reason` (DF-LEG-032) as the carrier of the stop, with its width, its nullability and no list (BR10) |
| DecisionElement | Document | The decision-record element of a dispute on the shared topic (BR9) |
| ConsumedShapes | Document | The deviation create and the customer read, and the two deviation events, with their placeholders (BR6, BR7, BR8, BR10) |
| ProblemEnvelope | Reused schema | The platform problem document with its `messageId` extension (BR4) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer, the 202 answer and its counting (BR3) |
| Fake set and fixtures | Test asset | The success, refusal, partial, unavailable and repeated-key answers of every consuming build (AC5) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC5, AC6) |

**Database.** One new table in `rwb_comms`, applied by the service's own Flyway sequence and never editing an applied migration (DP-15): `notice_dispute`, its standard columns of TSD P6 T3.0 and the index on `(notice_id, case_id)`; its DF field ids are the placeholder of section 11. `deviation` and `recovery_case` are not created here and no other schema is named in the note.

**Configuration and reference data.** The reason codes, the channel list, the dispute state list, the decision code and the rule id are reference data or parameters read with the version in force (BR11). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Add the dispute resource and the two operations to the document and lint the paths, the rights and the additive rule (AC1).
2. Write the two schemas with the elements of section 11, the required set, the code-only rule and an example; validate the example (AC2).
3. Write the `notice_dispute` row note, the `hold_reason` note and the absence tests for a deviation table, a case table and a cross-schema read (AC2, AC6).
4. Write the error section with one message ID per condition and the `Idempotency-Key` and 202 rules of the write (AC1).
5. Write the decision element and the four consumed shapes with their placeholders (AC3, AC4).
6. Generate the fake set and the drift test and wire the drift test into the build of `RWB-P6-E4038-APP` (AC5).
7. Write the naming and boundary section and the absence tests for the old base, a dispute event and a second topic (AC6).
8. Publish v1 and record the pinned version of this contract and of each consuming story.

**Feature flag.** `rwb.comms.self-service-dispute-contract`.

**Done when.** The document lints, the two schemas validate, the `notice_dispute` note applies twice, the fakes answer every status including the repeated key and the 202, the absence tests are green and `RWB-P6-E4038-APP` has accepted the baseline.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written by the consuming story (X5, legacy AC2) | 503, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required property is missing, or the channel or the reason code is outside its list | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P6-001 | Declared for the contact attempt that reads the stop of this resource; the contact and dispatch path raises it | 409 on the contact operation of the dispatch story, problem body with `messageId` MSG-P6-001 | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | Declared for a message on a channel whose consent state the data contract reports as absent; the contact path raises it | 409 or 422 on the contact operation of the dispatch story, problem body with `messageId` MSG-P6-002 | The customer has not consented to {channel}. Use another channel. |
| Not specified in the source documents (GAP-1117; ASM-2065) | The notice is out of scope, is not a sent notice of the case, or the deviation owner does not answer | A 404, 409 or 202 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |

MSG-P7-003, MSG-P4-002, MSG-GEN-001, MSG-P6-001 and MSG-P6-002 are the messages of the legacy validation table and of the rules VR-P6-017-1 and VR-P6-017-2 that this surface declares, and are copied unchanged. MSG-P6-003 belongs to the template withdrawal and the dispatch of a notice and is declared by the dispatch story, not here. The FSD's VR-P6-017-1 names MSG-P6-001 for a contact attempted during a stop, and this document declares it because the stop it carries is what that message reads; no text is invented.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template and its approval states, so it cannot show a dispute (GAP-1115; ASM-2063). The dispute is shown on the notice screen of the self-service channel and on the notice screen of RWB-P6-E1052-APP; the identifier of the self-service screen is Not specified in the source documents read here (GAP-1114; ASM-2062). Both surfaces are reached through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the dispute list and once for the notice reference and merges the answers.

| Surface | State | What this contract serves |
|---|---|---|
| Notice of the case | Sent, no dispute | The notice reference and an empty dispute list |
| Notice of the case | Sent, one dispute with the stop in force | The notice reference, one `Dispute` with the channel, the reason code, the raised date, the state and the deviation reference |
| Notice of the case | Sent, deviation cleared | The same list with the later state, and no stop on the notice |
| Notice of the case | Refused | The 403 with MSG-P4-002 and the 409 and 422 with the placeholders of section 14 |

The route, the merge order, the screen field list and the masking of the party belong to `RWB-PLT-N001-CON`; the transitions behind each state are the app story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-038-01 | AC1 | Contract | Notice `N-0101` of case `RC-2026-000321`; the contract half answers the 201 `Dispute` and the 200 list, and the deviation fake answers `DV-0101` |
| TC-E4-038-02 | AC2 | Contract | Decision log stubbed unavailable; the contract half answers the stopped chain and the 503 of MSG-P7-003 |
| TC-E4-038-03 | Access | Contract | A role without the Documents right sends the POST and the GET; the contract half answers the 403 of MSG-P4-002 |
| TC-E4-038-04 | Principle 5 | Contract | The stopped chain of the library stub on 10 disputes; the contract half answers the same 503 and the drift test |
| TC-P6-E4038-CON-01 | AC1 | Contract | The document validates; the two operations, the rights, the `Idempotency-Key` rule, the 202 answer, the two new markers and the six refusals are present |
| TC-P6-E4038-CON-02 | AC2 | Contract | The eight elements, the two request fields, the placeholders, the code-only rule, the new table and the `hold_reason` carrier are present; no deviation or case table is declared |
| TC-P6-E4038-CON-03 | AC3 | Contract | The decision element, the reference-data placeholders and the single published row are present; no dispute event and no second topic |
| TC-P6-E4038-CON-04 | AC4 | Contract | The two consumed REST rows and the two consumed event rows with their owners, their one-hop rule and their dedupe; no provided operation of another service |
| TC-P6-E4038-CON-05 | AC5 | Component | The dispute, deviation, source-data and event fakes and the library stub match the document; a drifted fake fails the build |
| TC-P6-E4038-CON-06 | AC6 | Contract | The nine sub-tables with their owners, the naming baseline and the absence tests for a deviation table, a case table, a `rwb_deviation` query and a `v_ace_*` view |

The four legacy identifiers keep their legacy order, their legacy covers and their legacy data, and carry the level of the surface they prove here, which is the contract: the legacy table has no level column, and the end-to-end proof of AC1 and AC2 is `RWB-P6-E4038-APP`'s, where the same cases carry End to end, Component and NFR. The six `TC-P6-E4038-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the reason codes, the channel and state lists, the decision code and the rule id stay data or reference data read with the version in force.
- No personal data in a schema, an example or a fake: identifiers, codes and dates only, and no name, address, identity number, account number or contact point.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the deviation create and the customer read are consumed and faked, never declared as provided (DP-01, DP-05).
- No deviation table, no case table and no cross-schema read: the absence test of AC6 fails a build that declares `deviation`, `recovery_case`, a column of either, a query on `rwb_deviation` or `rwb_case`, or a `v_ace_*` view.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is invented and none of the three catalogue events of this service is claimed: the only published element is the library's `DecisionRecorded`, and the two consumed deviation rows are the owner's (DP-03).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the element names and types, the new row's field ids, the state list, the reason codes, the decision code, the rule id, the deviation reference type and the refusal texts.
- Every example in the document is synthetic; no production payload, identifier or file is copied into a schema or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-038 |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4038-APP; this baseline copies neither |
| Legacy test cases | TC-E4-038-01 to TC-E4-038-04, as the contract half of each case |
| New contract cases | TC-P6-E4038-CON-01 to TC-P6-E4038-CON-06 |
| Legacy feature | FEAT-COM-04 Raise a dispute in self-service (FSD P6 A2.17; Epics 3 to 8 Specification v3, E4 P6), prerequisite FEAT-DVH-05 of the S8 deviation service |
| Legacy data rows | deviation DF-CAS-036 to DF-CAS-045; v_ace_customer DF-ACE-055 to DF-ACE-074; notice DF-LEG-015 to DF-LEG-023 and DF-LEG-030 to DF-LEG-034; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015; template DF-REF-045 to DF-REF-051 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 and DP-15 applied as rules, DP-11 in the consumed rows) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-04, R-UNI-20, R-UNI-39, R-UNI-40, R-UNI-44, R-LIT-05, BR-P6-017, VR-P6-017-1 and VR-P6-017-2 of FSD P6 A2.17.3.1 |
| Requirements | REQ-OCC-011, customer self-service for an offer, a signature, a payment and a dispute on the bank's digital channels (FSD P6 requirements served, E4, Should); TSD P6 T8 maps REQ-OCC-011 to FEAT-COM-01, which the feature table does not support (GAP-1115; ASM-2063) |

### 19. Out of scope

- The implementation of the two operations, the notice check, the decision write, the owner calls, the new row and the lift (RWB-P6-E4038-APP).
- The X1 deviation, its code, its owner, its clock, the pause of the case and the two deviation events: S8 rwb-deviation (`deviation` in `rwb_deviation`, FEAT-DVH-05, `DeviationWorkflow`).
- The case, its state, its timers and its scope: P3 rwb-case.
- The customer, the contact points and the consent state and the ACE views behind them: P1 rwb-source-data through DP-05.
- The decision-record library, its chain and its outbox (RWB-PLT-E1027-CON and the RWB-PLT-LIB stories); this baseline names the element and writes none of it.
- The dispatch of a notice, JOB-10, the WIN file and `NoticeDispatchWorkflow` (RWB-P6-E2021-CON and RWB-P6-E2021-APP).
- The notice generation, the template administration and the proof of delivery (RWB-P6-E1052-CON, RWB-P6-E1046-CON and RWB-P6-AD017-CON).
- The gateway-bff composite route, the customer sign-in, the screen field list and the masking at the edge (RWB-PLT-N001-CON), and the legacy screen SCR-33 Template approval, which the key names and which shows no dispute.
- The reason codes, the state list, the decision code, the rule id and the refusal texts: the owners of the parameters, the reference data and the message list.

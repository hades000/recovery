# RWB-P6-E4037-CON Pay in self-service

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4037-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-037 |
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

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-037 for rwb-comms. The self-service payment intent is published on Day 1 on base `/api/recovery/comms/v1` with the two notice-side intent operations, the `PaymentIntent` element set, the new `payment_intent` row, the `Idempotency-Key` rule, the error set, the decision-record element, the consumed payment and contact rows, the consumed case, treatment and payment events, the fakes and the drift test; the two legacy criteria stay with RWB-P6-E4037-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-comms (P6)**, I want **the published contract of a self-service payment intent — the base `/api/recovery/comms/v1` with `POST` and `GET /notices/{noticeId}/payment-intents`, the `PaymentIntentRequest` and `PaymentIntent` schemas, the `payment_intent` row of `rwb_comms`, the `Idempotency-Key` rule, the error set, the decision-record element, the consumed payment registration and contact read, the consumed case, treatment and payment events, the fakes and the drift test** instead of the monolith's in-process call that kept the notice, the treatment and the payment in one schema, so that **RWB-P6-E4037-APP and the sibling P6 stories build against one frozen, testable shape from Day 1, and an intent element, a status code, a decision element or an event name can never drift between rwb-comms, rwb-payment and the decision library without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 addition of the intent resource on the notice: the two operations, their request and answer bodies, their rights and their error set;
- the `PaymentIntent` and `PaymentIntentRequest` schemas, the required set and the form of the answer;
- the `payment_intent` row of `rwb_comms` with its element names, types, required flags, list references and indexes, and the declaration that no payment, proceeds or treatment row exists in this schema;
- the `Idempotency-Key` rule on the write, the additive rule and the versioning rule;
- the decision-record element of an intent (DP-03) and the consumed shapes of the payment owner, the source-data owner and the three events;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not take an intent. The state check, the conduct check, the decision write, the owner call and the repeat-key answer are `RWB-P6-E4037-APP`'s; the payment instruction, the amount and the posting are rwb-payment's; the plan and the settlement are rwb-treatment's. The document declares shapes and takes nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the legacy key has no operation of its own: its Endpoints block copies the two notice operations of the module, and the payment it describes was a set of rows of the `recovery` schema reached in process. In the target the notice is P6's, the arrangement is S2's and the money is P8's, so the one surface that has to be fixed before any code is written is the notice-side answer that takes the customer's intent and carries the owner's reference.

Three facts make this a baseline and not a summary. The endpoint inventory of TSD P6 holds eleven operations (API-P6-001 to API-P6-011) and none of them is a self-service payment, so the two operations, their rights and their statuses are this story's own decision and are marked as such (GAP-1125; ASM-2073). The data model of the module holds `notice`, `template`, `merge_field` and `signature_request` and no payment intent entity, and the notice row of TSD P6 T3.1 carries no payment field (DF-LEG-015 to DF-LEG-034), so the element set of the intent and its row are carried as placeholders and never guessed (GAP-1126; ASM-2074). And neither the Ownership Map nor any source names the operation of rwb-payment that a registration calls, so the row is declared as consumed and faked and no C dependency is declared (GAP-1124; ASM-2072).

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with its retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. The three events the catalogue gives this service (EV-13, EV-14 and EV-15, which TSD P6 T5.3 names `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`) are the notice events of other stories; this document declares none of them and publishes no event of its own.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope, the `Idempotency-Key` convention and the retry and `.dlt` topic convention are the platform baseline; where this document narrows them it does so explicitly.
- The notice generation contract RWB-P6-E1052-CON is published, so `notice`, its `case_id`, its `document_id` and its states have one owner document that this addition extends.
- The decision-record library contract RWB-PLT-E1027-CON is the writer, the chain and the outbox of the record this document names (DP-03); its shape is not fixed here.
- The owner rows are taken from the Ownership Map only: `proceeds` and the payment rows are P8 rwb-payment's, `treatment` is S2 rwb-treatment's, `contact_point_ext` is P1 rwb-source-data's, `recovery_case` is P3 rwb-case's and `notice`, `template` and `merge_field` are P6's.
- The registration of an intent with rwb-payment and the consent read of rwb-source-data are declared as consumed rows and faked; no P8 or P1 contract story is named in this story's Contract dependencies (GAP-1124; ASM-2072).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the addition to the rwb-comms OpenAPI 3.1 document: the intent resource under the notice, the two operations, the request and answer bodies and the error set.
2. Fix the intent elements and the request fields, with the types, widths and lists the module's data model gives and the placeholder where it gives none (GAP-1126; ASM-2074).
3. Declare the `payment_intent` row of `rwb_comms`, its required set, its two indexes, its list references and the absence of a payment, proceeds or treatment row in this schema.
4. Write the decision-record element of an intent and the two consumed shapes: the payment registration and the consent and contact-stop read.
5. Write the `Idempotency-Key` rule on the write, the additive rule and the compatibility rule.
6. Declare the three consumed events with their topics, owners and keys, and declare no published event of this service (GAP-1129; ASM-2077).
7. Generate the fake set from the document, wire the drift test into the build of this story and of `RWB-P6-E4037-APP`, and write the absence tests.
8. Publish v1, record the pinned version of each consuming story, and hand the baseline to the app story, to the sibling P6 stories that read the notice and to the payment, source-data and library owners.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | An intent or owner fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | An element type, width or list has no value in the sources | The row carries the placeholder and the fake is derived from the published document | None | AC2 |
| X5 | An event is declared as published by this service, or on another service's topic | The absence test fails the build; nothing is published | None | AC3 |
| X6 | The document declares a payment, proceeds or treatment table, a query on `rwb_payment` or a `v_ace_*` view | The absence test fails the build | None | AC5 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the row is described as consumed and faked | None | AC4 |
| X8 | The decision code, the rule id or the eligible states are written as values | The review fails the baseline; the element names the reference data instead | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the notice contract it extends, the Ownership Map rows and the decision library only |
| Negotiable | The two paths, the intent element set and the row name are settled at the baseline review; the base, the topic, the queue and the naming are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the payment, source-data and library owners on the same day, and makes a silent field drift impossible |
| Estimable | One additive document change, one schema pair, one new row, one decision element, three consumed events, five fakes and ten tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of a self-service payment intent

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the notice contract RWB-P6-E1052-CON is published with the notice resource and its case reference DF-LEG-016

  Scenario: AC1 The two intent operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /notices/{noticeId}/payment-intents answering 201 with PaymentIntent and GET /notices/{noticeId}/payment-intents answering 200 with the PaymentIntent list, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the POST declares the Idempotency-Key header and a stored answer, and the GET declares no Idempotency-Key
    Then both operations declare one capability area with right C on the POST and right R on the GET, scope applied, a 2 s budget, and the refusals 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition
    Then the document marks both operations as new, because the eleven operations of the TSD P6 inventory API-P6-001 to API-P6-011 hold none for a self-service payment (GAP-1125; ASM-2073)
    Then the capability area and the right are declared as the contract's own decision, because the role matrix of TSD P6 T6.1 names no customer-facing right, and the value chosen is recorded with its gap and assumption (GAP-1128; ASM-2076)
    Then every added property is additive within major version 1, so a consumer of the notice resource keeps working
    Then the document declares no second base, no second resource and no operation of another service

  Scenario: AC2 The intent element set and the new row are fixed and the money stays the payment owner's (new, D-RCV-60)
    Given the intent element set of the baseline
    When it is compared with the notice row of TSD P6 T3.1 and with the Ownership Map
    Then PaymentIntent carries intentId, noticeId, caseId, target, channel, paymentReference, ownerState and requestedAt
    Then intentId, noticeId and caseId are uuid, as DF-LEG-015 and DF-LEG-016 give them, and the physical type of target, paymentReference, ownerState and requestedAt is Not specified in the source documents (GAP-1126; ASM-2074)
    Then channel is varchar(15) with list LOV-CHANNEL, as TSD P6 T3.2 gives the channel list, and target carries its vocabulary as reference data with the value set Not specified in the source documents (GAP-1127; ASM-2075)
    Then PaymentIntentRequest requires target and channel, noticeId comes from the path, and intentId and paymentReference come from the owner's answer
    Then the payment_intent row of rwb_comms is declared with its element names, its required set, its two indexes and the placeholder for every type and field id the sources do not give (GAP-1126; ASM-2074)
    Then the document declares no payment, proceeds, posting, treatment or contact table in rwb_comms, no column of one and no foreign key across a service boundary (DP-01)

  Scenario: AC3 The decision-record element is declared and no event of this service is invented (new, D-RCV-60)
    Given the decision and event sections of the baseline
    When they are compared with DP-03, the shared topic and the event catalogue rows of this service
    Then the element carries the case, the notice, the target, the channel, the payment reference, the decision code, the rule id, the rule version and the decided-at, and it is the local library's element on rwb.decision-record.v1 (DP-03)
    Then the record is written before the change, and an intent whose record cannot be written is not taken
    Then the decision code and the rule id are declared as reference data read with the version in force and are Not specified in the source documents (GAP-1127; ASM-2075)
    Then the only published row is rwb.decision-record.DecisionRecorded.v1 (EV-08), owned by P7 and written by the library, and the document declares no event of its own
    Then the document declares no payment event, and EV-11 TreatmentBooked, EV-12 PaymentMissed and EV-25 ProceedsMatched are named as rwb-payment's and EV-13 to EV-15 as the notice stories' (GAP-1129; ASM-2077)
    Then no payload carries a name, an address, an identity number, a card number or a contact point, and every payload validates with BACKWARD compatibility

  Scenario: AC4 The consumed shapes are declared with their call type and their owner (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are reviewed against the Ownership Map and the event catalogue of Architecture v5
    Then the payment registration and the contact, consent and contact-stop read are declared as consumed rows of P8 and P1, each one hop with a 2 s timeout and a breaker, and each faked
    Then no C dependency row is declared for them, because the plan names no P8 and no P1 contract story for this key (GAP-1124; ASM-2072)
    Then rwb.case.CaseStateChanged.v1 (EV-05) on rwb.case.events.v1 keyed by caseId, rwb.treatment.TreatmentApproved.v1 (EV-10) on rwb.treatment.events.v1 keyed by caseId and rwb.payment.PaymentMissed.v1 (EV-12) on rwb.payment.events.v1 keyed by caseId are declared as consumed, each with its inbox dedupe
    Then the event that reports a completed payment is named as Not specified in the source documents and the paid state is declared as read from the owner's answer (GAP-1129; ASM-2077)
    Then the document declares no operation of another service as provided, no subscription on another service's topic as its own and no file row

  Scenario: AC5 The fakes answer the owners and the drift test binds them (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation, the event or the element it serves
    Then the payment fake answers a registration with a reference, a state and a target to pay against, a target with nothing to pay against, a 5xx and an answer delayed beyond 2 s
    Then the source-data fake answers consent given, consent withdrawn, a contact stop with a reason and a delayed answer
    Then the case, treatment and payment event fakes answer an open case, a closed case, an approved plan, an approved settlement, a missed payment and a duplicated event for each inbox
    Then the decision-record library stub answers a healthy chain and outbox, and a stopped chain
    Then the intent fake answers the 201, the 200, the repeated Idempotency-Key and every refusal of AC1
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The nine contract tables, the naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the contract section of this story
    When its nine sub-tables are reviewed against the Template and Rules and the Ownership Map
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty and a reason beside it
    Then the tables named as owned are notice, template, merge_field, payment_intent and the library objects applied in rwb_comms, and payment, proceeds, treatment, contact_point_ext, recovery_case, decision_log_entry, rule_row and any v_ace_* view are named as other owners' and consumed only through their contracts
    Then the schema is rwb_comms, the base is /api/recovery/comms/v1, the topic is rwb.comms.events.v1 with retry and .dlt topics, the event names are rwb.comms.<Event>.v1, the task queue is rwb-comms in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.comms
    Then no payment table, no proceeds row, no cross-schema key and no query of this service on rwb_payment or on a v_ace_* view is declared, and the absence test fails a build that adds one
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then no workflow, no Schedule and no file element is declared, and the document says why
```

These six criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story and they restate no business outcome of RWB-P6-E4037-APP, which owns AC1 and AC2 of RWB-E4-037.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD P6 T6.2 |
| BR4 | Error responses use one envelope and one message ID per condition; a text the sources do not give carries the placeholder | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | The payment instruction, the proceeds and the posting are P8's and the arrangement is S2's; this service declares no such table, no column of one and no cross-schema key | DP-01; Ownership Map (`proceeds` owned by P8, `treatment` owned by S2) |
| BR8 | The decision record of an intent is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR9 | No business value is fixed in the contract: the eligible states, the targets, the channels, the decision code and the rule id stay data or reference data read with the version in force | FSD P6 A2.16.3.1 (BR-P6-016); Template and Rules §R7.2 s17 |
| BR10 | No element carries a personal name, an identity number, an account number, a card number or a contact point: the intent is reached by identifiers | Template and Rules §R7.2 s17; TSD P6 T6.2 (masking) |
| BR11 | The contact stop and the consent of a channel are the facts of rwb-source-data and arrive on its contract; the contract declares the read and keeps no member list | DP-05; FSD P6 A2.16.3.1 (VR-P6-016-1, VR-P6-016-2) |
| BR12 | The registration of an intent with rwb-payment is consumed and faked, and the C row is added when a P8 contract story is planned | Ownership Map (P8 owns payment and proceeds matching); Template and Rules §R5.4 |
| BR13 | An intent whose decision record cannot be written does not proceed, and an incident is raised | R-UNI-39 (Business Rules and Routing Logic v4); legacy RWB-E4-037 AC2 |
| BR14 | The plan or the settlement an intent answers is the approved arrangement of the case, on a channel the customer consented to | R-RES-09; R-SET-04; FSD P6 A2.16.3.1 (VR-P6-016-2) |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element set, the row, the decision element and the consumed rows are described | In review |
| In review | Consumer sign-off | `RWB-P6-E4037-APP` and the payment, source-data and library owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a physical type once its owner names it | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, a path changes or a refusal status changes | New major version drafted |
| Baselined | Drift in a fake | The drift test fails | In review |
| Baselined | A payment table or a cross-schema read is declared | The absence test of AC5 and AC6 fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| notice.notice_type | `DEMAND`, `RECALL`, `STATUTORY_SALE_NOTICE`, `GUARANTOR_NOTICE` (LOV-NOTICE, TSD P6 T3.2) | Declared as the list reference; the intent changes none of them |
| notice.delivery_status | `DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING` (LOV-DELIVERY, TSD P6 T3.2) | Declared as the list reference; an intent changes none of them |

The notice state machine and the intent that leaves it unchanged are `RWB-P6-E4037-APP`'s, and the state of an instruction is rwb-payment's. This document fixes the surface and takes nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the capability area and the right of the two operations, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (RWB-P6-E4037-APP, the sibling P6 stories that read the notice, and the rwb-payment, rwb-source-data and P7 library owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the CloudEvents envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element is declared in the intent, in an answer or in a fake |
| Business analyst of P6 | Confirms that the eligible states, the targets, the decision code and the rule id are named as reference data and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_comms` by the naming rule of DP-02; the document names the scheme and not a credential. The rights of the two operations are declared here as the contract's own decision, because the matrix of TSD P6 T6.1 holds staff roles and no customer-facing right (GAP-1128; ASM-2076); their role lists and the customer scope stay rwb-access data, and no role code is written in the document.

### 11. Data

The contract baseline declares shapes, not business values.

| Element | Legacy source | Type and width | Required | List |
|---|---|---|---|---|
| intentId | none in the legacy data table; the legacy row names no payment entity | uuid | Yes | None |
| noticeId | DF-LEG-015 of the notice | uuid | Yes | None |
| caseId | DF-LEG-016 of the notice | uuid | Yes | None |
| target | the plan or the settlement the legacy story names, with no field of its own | Not specified in the source documents (GAP-1126; ASM-2074) | Yes | Not specified in the source documents (GAP-1127; ASM-2075) |
| channel | the channel of LOV-CHANNEL, as DF-REF-066 gives it | varchar(15) | Yes | LOV-CHANNEL |
| paymentReference | none; the owner's answer | Not specified in the source documents (GAP-1126; ASM-2074) | No | None |
| ownerState | none; the owner's answer | Not specified in the source documents (GAP-1126; ASM-2074) | No | Not specified in the source documents (GAP-1127; ASM-2075) |
| requestedAt | none | timestamptz, by the standard column convention of TSD P6 T3.0 | Yes | None |
| Standard columns | state, version, created_at, created_by, updated_at, updated_by, is_active of TSD P6 T3.0 | varchar(40), integer, timestamptz, uuid, boolean | n/a | None |

| Item | Content |
|---|---|
| Request | `PaymentIntentRequest` carries `target` and `channel`, both required; `noticeId` comes from the path and `intentId` and `paymentReference` from the owner's answer |
| Answer | 201 with `PaymentIntent` and 200 with the `PaymentIntent` list, newest first, each carrying its notice and case reference |
| Row | `payment_intent` in `rwb_comms`, one row per POST, with the two indexes `ix_payment_intent_notice_id` and `ix_payment_intent_case_id` |
| Decision record | The library's element: the case, the notice, the target, the channel, the payment reference, the decision code, the rule id and version and the decided-at (DP-03) |
| Owner reference | The payment reference the owner returns is stored and shown; no amount, no currency and no posting fact is stored or declared (BR7) |

**No table of another owner and no migration of one.** `notice`, `template` and `merge_field` are the P6 rows of TSD P6 T3.1 and this document adds the `payment_intent` row of this key in `rwb_comms` and nothing else; `decision_record`, `idempotency_key`, `outbox_event` and `processed_event` are platform library objects created in `rwb_comms` by the library's migration and are named here, not declared. `payment`, `proceeds` and the posting rows (P8), `treatment` (S2), `contact_point_ext` and `party_ext` (P1), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view are other owners' and appear only as consumed shapes. `notice.case_id` and the intent's `case_id` are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number, an account number, a card number or a contact point. The notice, the intent and the payment are reached by identifiers, and the consent facts stay with their owner as an answer and are never copied into a row here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Both operations are new: no self-service payment operation is in the endpoint inventory of the TSD (GAP-1125; ASM-2073).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| new | POST | `/notices/{noticeId}/payment-intents` | `PaymentIntentRequest`; `noticeId` from the path | 201 with `PaymentIntent` | the contract's declared area, right C, scope applied, the value recorded with its gap and assumption (GAP-1128; ASM-2076) | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| new | GET | `/notices/{noticeId}/payment-intents` | None | 200 with the `PaymentIntent` list, newest first | the same area, right R, scope applied | Not applicable | 401, 403, 404, 503 |

The purpose, the shapes and the refusals are this baseline's own, because no TSD P6 T-A.1 row names a self-service payment; the base and the naming are DP-13's and DP-14's. The two notice operations of the module, API-P6-001 (Litigation C) and API-P6-002 (Litigation R), are `RWB-P6-E1052-CON`'s and are not redeclared here.

#### 12.2 REST operations consumed

None declared as an operation of this document; the two rows below are the consumed shapes the app story calls, each one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020).

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The payment registration the app story calls to take an intent against the plan or the settlement | P8 rwb-payment | The request (the case, the notice, the target and the channel) and the answer that carries the owner's payment reference and state | Consumed and faked; no C row, and the path and field set are (GAP-1124; ASM-2072) |
| The contact, consent and contact-stop read of the rwb-source-data contract | P1 rwb-source-data | The answer elements the conduct check needs: the consent state per channel and the contact stop of the case | Consumed and faked; no C row, and the path is (GAP-1124; ASM-2072) |

No row reads a table, no row reads a `v_ace_*` view of this service, and no row is declared as a provided operation of this service (BR6, BR7, BR11).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, rule id, rule version, case, notice, target, channel, payment reference, decided-at; written by the local decision-record library (DP-03) |

This document declares the element and publishes nothing itself, and it declares no event of this service's own: EV-13, EV-14 and EV-15 are the notice events of `RWB-P6-E1052-CON` and the dispatch stories, and EV-11, EV-12 and EV-25 are rwb-payment's (GAP-1129; ASM-2077).

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | caseId, the from and to states and the changed-at, consumed inside rwb-comms so a new intent on a closed case is refused, with the inbox dedupe |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | caseId, the treatment reference, the approval and the changed-at, consumed so an intent names an approved arrangement, with the inbox dedupe |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | P8 rwb-payment | caseId, the payment reference, the missed date and the reason code, consumed so the state of a reference is the owner's, with the inbox dedupe |

The rows are consumed by `RWB-P6-E4037-APP`; this baseline fixes their names, their topics and their keys (`caseId`) and declares no subscription of its own. The event that carries a completed payment is Not specified in the source documents (GAP-1129; ASM-2077), and the paid state is declared as read from the owner's answer.

#### 12.5 Workflows and activities

None. An intent is one synchronous write with one library write and two owner calls; this document declares no workflow, no child workflow and no activity, and `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is declared: JOB-10 of the catalogue is the daily WIN dispatch of `RWB-P6-E2021-CON`, and JOB-07 and JOB-08 are rwb-payment's (Architecture v5 slide 44). No job row is read or changed by this document.

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| payment_intent | `rwb_comms` | P6 | The intent of this key: its element set, its required set and its two indexes (section 11) |
| notice | `rwb_comms` | P6 | The notice the intent answers, its `case_id`, its `template_id` and its state |
| template | `rwb_comms` | P6 | Read for the notice reference only; written by the template stories |
| merge_field | `rwb_comms` | P6 | Read for the merge codes of the notice only; written by the catalogue story |
| decision_record, idempotency_key, outbox_event, processed_event | `rwb_comms` | PLT library objects applied in this schema | The decision entry of an intent, the stored answer of the POST, the envelope of the published row and the inbox of the consumed rows (DP-03) |

`payment`, `proceeds` and the posting rows are P8's; `treatment` is S2's; `contact_point_ext`, `party_ext` and `interaction` are P1's; `recovery_case`, `task`, `timer` and `queue` are P3's; `decision_log_entry`, `rule_row` and the rule package rows are P7's; `deviation` is S8's; `outbound_item` and `interface_config` are P2's. They are named as consumed answers only, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Intent fake | The two operations of 12.1 | A 201 with the `PaymentIntent`, a 200 list, the repeated `Idempotency-Key` returning the first answer, and the 401, 403, 404, 409, 422 and 503 refusals |
| Payment fake | The first row of 12.2 | A registration with a reference, a state and a target to pay against; a target with nothing to pay against; a 5xx; an answer delayed beyond 2 s |
| Source-data fake | The second row of 12.2 | Consent given, consent withdrawn, a contact stop with a reason and a delayed answer |
| Event fakes | The three rows of 12.4 | An open case, a closed case, an approved plan, an approved settlement, a missed payment and a duplicated event for each inbox |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Drift test | Every fake against the document | A drifted fake fails the build |

The payment and source-data fakes are stubbed from the owners' published documents and carry the placeholder where the source is silent (GAP-1124; ASM-2072).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The intent take and the intent list provided; the payment registration and the contact read consumed; one hop, 2 s |
| Kafka | 1 declared as written by its owner, 3 consumed | `DecisionRecorded` through the library; `CaseStateChanged`, `TreatmentApproved` and `PaymentMissed`; no event of this service |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the addition to `openapi/rwb-comms-v1.yaml` for the intent resource, the `PaymentIntentRequest` and `PaymentIntent` schemas in `th.co.scb.ace.workbench.recovery.comms.api`, the `payment_intent` migration note, the decision-record fragment, the fake set and the drift test. The implementation behind it is `RWB-P6-E4037-APP`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming app story carries the H row |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; the contract names the read and holds no view | referred to; the consuming app story carries the read, and no dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the intent answer is reached through it and the contract declares no composite route | referred to; the consuming app story and the platform edge story carry the H row |

DP-13 is the pattern this story publishes. DP-03 and DP-05 are named and not declared: the record is the library's and the contact facts are the source-data owner's. DP-01 and DP-15 stand behind the boundary and the new row as rules and add no dependency. DP-19 is the route the self-service screen uses and is `RWB-PLT-N001-CON`'s. This story being a CON story, it holds no build dependency by rule (Template and Rules §R5.7 rule 1).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PaymentIntentOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR6) |
| PaymentIntentSchema | Published schema | `PaymentIntentRequest` and `PaymentIntent` with the eight elements, the required set and the two list references (BR9, BR10) |
| IntentRowNote | Resource | The `payment_intent` row of `rwb_comms`, its two indexes and the absence of a payment, proceeds or treatment row (BR7) |
| DecisionElement | Document | The decision-record element of an intent on the shared topic (BR8) |
| ConsumedShapes | Document | The payment registration, the contact read and the three event rows, with their placeholders (BR6, BR11, BR12) |
| ProblemEnvelope | Reused schema | The platform problem document with its `messageId` extension (BR4) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR3) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers of every consuming build (AC5) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC5, AC6) |

**Database.** One new row in `rwb_comms`, `payment_intent`, applied by the service's own Flyway sequence and never editing an applied migration (DP-15); its physical types and field ids are the placeholders of section 11. No payment, proceeds or treatment table is created here and no other schema is named in the note.

**Configuration and reference data.** The eligible notice states, the target vocabulary, the channels, the decision code and the rule id are reference data or parameters read with the version in force (BR9; GAP-1127; ASM-2075). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Add the intent resource and the two operations to the document and lint the paths, the rights and the additive rule (AC1).
2. Write the two schemas with the eight elements, the required set, the list references and an example; validate the example (AC2).
3. Write the `payment_intent` row note, its required set and its two indexes, and the absence tests for a payment, proceeds and treatment table (AC2, AC5).
4. Write the error section with one message ID per condition and the `Idempotency-Key` rule of the write (AC1).
5. Write the decision element and the two consumed documents' identities with their placeholders (AC3, AC4).
6. Write the three consumed event rows with their topics, owners and keys and the declaration that no event is published here (AC3, AC4).
7. Generate the fake set and the drift test and wire the drift test into the build of `RWB-P6-E4037-APP` (AC5).
8. Write the naming and boundary section and the absence tests for the old base, a payment event and a second topic; publish v1 and record the pinned version of each consuming story (AC6).

**Feature flag.** `rwb.comms.payment-intent-contract`.

**Done when.** The document lints, the two schemas validate, the row note applies twice, the fakes answer every status including the repeated key, the absence tests are green and `RWB-P6-E4037-APP` has accepted the baseline.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-P6-001 | The consuming story refuses an intent because a contact stop is in force | 409, problem body with `messageId` MSG-P6-001 and the reason | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | The consuming story refuses an intent because the channel carries no consent | 409, problem body with `messageId` MSG-P6-002 and the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-GEN-001 | A required property is missing or the channel is not a value of LOV-CHANNEL | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written by the consuming story (legacy AC2) | 503, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Not specified in the source documents (GAP-1129; ASM-2077) | The notice is not eligible, the owner reports nothing to pay against, or an owner does not answer | A 409 or 503 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |

The five message IDs and their texts are the messages of the legacy validation table that this surface raises and are copied unchanged. MSG-P6-003 (template withdrawn) belongs to the notice, the dispatch and the template stories and is declared there, not here. No text is invented.

### 15. Screens and states

The legacy story names SCR-33 Template approval, and that screen shows a template and its approval states, so it cannot show a payment; the P6 screen list of FSD P6 holds no self-service payment screen of its own, because the screen is the customer's screen on HOME.SCB and the web (FSD P6 A2.16.2), whose identifier is Not specified in the source documents read here (GAP-1125; ASM-2073). It is reached through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the intents of the notice and rwb-payment once for the amount due and the state, and merges the answers.

| Surface | State | What this contract serves |
|---|---|---|
| Notice shown | No intent | The notice reference and an empty intent list |
| Notice shown | Intent taken | The notice reference and one `PaymentIntent` with its target, channel, reference and owner state |
| Notice shown | Refused | The 403 with MSG-P4-002, the 409 of MSG-P6-001 or MSG-P6-002, and the placeholder of section 14 |
| Notice of another case | Outside the scope | The 404 and no screen data |

The route, the merge order, the screen field list and the masking of the customer view belong to `RWB-PLT-N001-CON`; the transitions behind each state are the app story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-037-01 | AC1 | Contract | Notice `N-0101` of case `RC-2026-000321`; the contract half answers the 201 `PaymentIntent` of eight elements and the 200 list |
| TC-E4-037-02 | AC2 | Contract | Decision log stubbed unavailable; the contract half answers the stopped chain and the 503 of MSG-P7-003 |
| TC-E4-037-03 | Access | Contract | A caller whose case is outside the scope sends the POST and the GET; the contract half answers the 404, and a role without the right answers the 403 of MSG-P4-002 |
| TC-E4-037-04 | Principle 5 | Contract | The stopped chain of the library stub on 10 intents; the contract half answers the same 503 and the drift test |
| TC-P6-E4037-CON-01 | AC1 | Contract | The document validates; the two operations, the rights, the `Idempotency-Key` rule, the two new markers and the six refusals are present |
| TC-P6-E4037-CON-02 | AC2 | Contract | The eight elements, the required set, the list references, the placeholders and the `payment_intent` row are present; no money table is declared |
| TC-P6-E4037-CON-03 | AC3 | Contract | The decision element, the reference-data placeholders and the single published row are present; no payment event and no second topic |
| TC-P6-E4037-CON-04 | AC4 | Contract | The two consumed rows with their owner, the one-hop rule and the three events with their keys; no provided operation of another service |
| TC-P6-E4037-CON-05 | AC5 | Component | The intent, payment, source-data and event fakes and the library stub match the document; a drifted fake fails the build |
| TC-P6-E4037-CON-06 | AC6 | Contract | The nine sub-tables with their owners, the naming baseline and the absence tests for a money table, a `rwb_payment` query and a `v_ace_*` view |

The four legacy identifiers keep their legacy order, their legacy covers and their legacy data, and carry the level of the surface they prove here, which is the contract: the legacy table has no level column, and the end-to-end proof of the same cases is RWB-P6-E4037-APP's, where `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR. The six `TC-P6-E4037-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the eligible states, the targets, the channels, the decision code and the rule id stay data or reference data read with the version in force.
- No personal data in a schema, an example or a fake: identifiers, codes, dates and amounts only, and no name, address, identity number, account number, card number or contact point.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the payment registration and the contact read are consumed and faked, never declared as provided (DP-01, DP-05).
- No money table and no cross-schema read: the absence test of AC5 and AC6 fails a build that declares a payment, proceeds or treatment table, a column of one, a query on `rwb_payment` or a `v_ace_*` view.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is invented and none of the three catalogue events of this service is claimed: the only published element is the library's `DecisionRecorded` (DP-03).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the types of four elements, the target vocabulary, the owner's state set, the field ids of the new row and the refusal texts.
- Every example in the document is synthetic; no production payload, identifier or file is copied into a schema or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-037 |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4037-APP; this baseline copies neither |
| Legacy test cases | TC-E4-037-01 to TC-E4-037-04, as the contract half of each case |
| New contract cases | TC-P6-E4037-CON-01 to TC-P6-E4037-CON-06 |
| Legacy feature | FEAT-COM-03 Pay in self-service (FSD P6 A2.16), prerequisite FEAT-COM-01 View the offer on LINE and web |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-023; template DF-REF-045 to DF-REF-051; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015; treatment DF-TRT-001 to DF-TRT-014 and v_ace_customer DF-ACE-055 to DF-ACE-074, both consumed from their owners and never read by this service |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 and DP-15 applied as rules, DP-11 in the consumed rows) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-RES-09, R-SET-04, R-UNI-33, R-UNI-34, R-UNI-39, BR-P6-016, VR-P6-016-1 and VR-P6-016-2 |
| Requirements | Not mapped: the P6 requirement list holds no requirement for FEAT-COM-03, and the endpoint inventory holds no self-service payment operation (GAP-1125; ASM-2073) |

The supporting facts of the legacy key — the payment instruction and the money (P8 rwb-payment), the plan and the settlement (S2 rwb-treatment), the contact and consent facts (P1 rwb-source-data) and the decision log entry (P7, DP-03) — are named here as consumed shapes and are answered by their owners for their own slices, and this document changes none of their designs.

### 19. Out of scope

- The implementation of the two operations, the notice check, the conduct check, the decision write, the owner call and the repeat-key answer (RWB-P6-E4037-APP).
- The payment instruction, its amount, the proceeds and the posting: P8 rwb-payment and the P8 stories that build it.
- The plan, the settlement and the treatment: S2 rwb-treatment.
- The contact repository, the consent state per channel and the contact stop as rows: P1 rwb-source-data and RWB-P6-E4039-CON and RWB-P6-E4039-APP on the repository side.
- The decision-record library, its chain and its outbox (RWB-PLT-E1027-CON and the RWB-PLT-LIB stories); this baseline names the element and writes none of it.
- The case state and its closure as a case fact (P3 rwb-case).
- The dispatch of a notice, JOB-10, the WIN file and `NoticeDispatchWorkflow` (RWB-P6-E2021-CON and RWB-P6-E2022-CON).
- The offer view and the acceptance of an offer (RWB-P6-E4035-CON and RWB-P6-E4036-CON) and the dispute (RWB-P6-E4038-CON).
- The gateway-bff composite route, the screen field list and the masking at the edge (RWB-PLT-N001-CON), and the legacy screen SCR-33 Template approval, which the key names and which shows no payment.
- The decision code, the rule id, the eligible states, the target vocabulary, the owner's state set and the refusal texts: the owners of the parameters, the reference data and the message list.

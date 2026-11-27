# RWB-P6-E4035-CON View the offer on LINE and web

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4035-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P6-E4035-CON-16); not sized in this document |
| Contract version | Major version 1 (path /v1); minor version Not specified in the source documents (DOR-RWB-P6-E4035-CON-23) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P6-E4035-CON-14); no signed epic design record or sign-off reference is held in the story or the source documents |
| Depends on (build) | None |
| Contract dependencies | rwb-source-data.yaml 5.1.0 (API Specification v7) for the contact point and consent read; no S2 contract story is named (GAP-1131) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-041, RD-P1-060 |

**Version 3 changes.**

- The consumed rwb-source-data row is the published `GET /contact-points` of rwb-source-data.yaml 5.1.0 with the published consent values (RD-P1-005; findings 1, 3 and 6).
- The contact stop is no longer declared as a P1 answer; it is held from the deviation events (finding 2).
- The write and the errors follow the shared idempotency rules and `Problem` schema; `messageId` becomes `messageCode`; AC9 added (RD-P1-001, RD-P1-004; findings 4 and 5).
- Customer facts are read through `getCustomer`, masked (RD-P1-060; NEW-GAP-F15-4 closed). Pending: the `PORTAL` contact point and consent (NEW-GAP-G6-3) and the ledger entry of a view (NEW-GAP-F15-5; RD-P1-007; finding 7). RD-P1-041: no freshness data is read.
- Finishing pass: customer facts of the portal view come from `getCustomer`, masked (RD-P1-060); test case IDs of Test Cases v9 applied where cited.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-035 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E4035-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 14 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-comms (P6)**, I want **the published contract of the offer view on a digital channel — the base `/api/recovery/comms/v1` with `GET /notices/{noticeId}/channel-view` and `POST /notices/{noticeId}/views`, the `NoticeChannelView`, `NoticeView` and `NoticeViewRequest` schemas, the consent and contact-stop element block, the `notice_view` table note, the `Idempotency-Key` rule, the error set, the decision-record element, the `NoticeDelivered` element, the four consumed event rows and the two consumed owner reads, the fakes and the drift test** instead of the monolith's screen that read `v_ace_customer`, `treatment` and `notice` in one call inside one schema, so that **RWB-P6-E4035-APP and the sibling P6 stories build against one frozen, testable shape from Day 1, and a channel value, a consent answer, a status code or the delivery event can never drift between rwb-comms, rwb-source-data, rwb-treatment and the decision library without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 addition of the channel view of the notice: the two operations, their request and answer bodies, their rights and their error set;
- the two element sets, the consent and contact-stop block, and the channel rule with its placeholder;
- the `notice_view` table note and the two notice columns a view moves;
- the `Idempotency-Key` rule on the write, the additive rule and the versioning rule;
- the decision-record element of a view (DP-03), the `NoticeDelivered` element (EV-15) and the four consumed event rows;
- the two consumed owner reads, the fake set generated from the document, and the drift test every consuming build runs.

It does not build the view. The template check, the consent and stop checks, the offer read, the decision write, the view row, the two notice columns and the repeat-key answer are `RWB-P6-E4035-APP`'s; the offer is rwb-treatment's; the customer, the contact point and the consent are rwb-source-data's; the case state and the hold are rwb-case's. The document declares shapes and shows no offer.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020), and the legacy key has no operation of its own: its endpoint block copies the two notice operations of the module, `POST /cases/{caseId}/notices` (API-P6-001) and `GET /notices/{noticeId}` (API-P6-002), which belong to the notice stories, and the offer and the contact point it needs were read as tables of the same `recovery` schema as the notice. In the target the offer is S2's, the contact point is P1's and the notice is P6's, so the one surface that has to be fixed before any code is written is the channel answer of the notice and the view record that proves the delivery.

Three facts make this a baseline and not a summary. The endpoint inventory of TSD P6 holds eleven operations (API-P6-001 to API-P6-011) and none of them shows an offer to a customer or records a view, so the two operations are this story's own decision and are marked as such (GAP-1130; ASM-2078). TSD P6 T3.1 holds `notice`, `template`, `merge_field` and `signature_request`, and no field of the notice carries the channel of a digital delivery or the fact of a view, so the `notice_view` note and the two columns a view moves are declared here and their field IDs stand as placeholders (GAP-1133; ASM-2081). And no source names the right of an offer view, so the operations inherit the capability area and the right of the notice resource they extend and the customer's own identity is left to the edge (GAP-1134; ASM-2082).

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with its retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. Of the three events the catalogue gives this service (13 `NoticeGenerated`, 14 `NoticeDispatched` and 15 `NoticeDelivered`), this document declares one, the third, because the measure the feature serves counts notices with proof of delivery and catalogue row 15 is the only row that carries that fact; the other two are the dispatch stories' (GAP-1132; ASM-2080).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline; where this document narrows them it does so explicitly.
- The notice contract RWB-P6-E1052-CON is published, so `notice`, its `template_id`, its state and its delivery columns have one owner document that this addition extends.
- The proof-of-delivery contract RWB-P6-E1055-CON is published, so the `NoticeDelivered` element of this document reuses the shape that story declares and adds `channel` to it (GAP-1132; ASM-2080).
- The decision-record library contract RWB-PLT-E1027-CON is the writer, the chain and the outbox of the record this document names (DP-03); its shape is not fixed here.
- The owner rows are taken from the Ownership Map only: `treatment` is S2 rwb-treatment's, `party_ext`, `contact_point_ext`, `account_ext` and `interaction` are P1 rwb-source-data's, `recovery_case` is P3 rwb-case's, `deviation` is S8 rwb-deviation's and the decision ledger is P7 rwb-decision's.
- The two owner reads of 12.2 are declared as consumed and faked, because no P1 and no S2 contract story is named in this story's Contract dependencies (GAP-1131; ASM-2079).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the addition to the rwb-comms OpenAPI 3.1 document: the channel view of the notice, the two operations, the request and answer bodies and the error set.
2. Fix the two element sets from the notice and template rows of TSD P6 T3.1 and the legacy data table, with the view reference, the viewed-at, the offer facts and the merge values standing as placeholders.
3. Fix the channel rule: `channel` is one of LOV-CHANNEL, the two channels of this feature are `LINE` and `PORTAL`, and no `WEB` value is added.
4. Fix the consent and contact-stop block of the answer: the reason of the stop, the consent state of the channel and the refusal the operation raises.
5. Declare the `notice_view` note, the two notice columns a view moves and the absence of a treatment, case, deviation or ACE table in `rwb_comms`.
6. Write the decision-record element, the `NoticeDelivered` element with its once-per-notice rule and the four consumed event rows with their owners and keys.
7. Write the `Idempotency-Key` rule on the write, the additive rule and the compatibility rule.
8. Generate the fake set from the document, wire the drift test into the build of this story and of `RWB-P6-E4035-APP`, and write the absence tests.
9. Publish v1, record the pinned version of each consuming story, and hand the baseline to the app story, the sibling P6 stories that read the notice and the two owner teams.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A channel value outside LOV-CHANNEL is accepted by the schema | The schema lint fails the build; the enum is the reference list and not a local copy | None | AC2 |
| X4 | A view element or a physical type has no value in the sources | The row carries the placeholder and the fake is derived from the published document | None | AC2 |
| X5 | A refusal of the consent or the contact stop loses its message ID | The contract test fails the build; the block of AC3 is the only source of the two refusals | None | AC3 |
| X6 | An event of this service other than `NoticeDelivered` is declared, or an event is declared on another service's topic | The absence test fails the build; nothing is published | None | AC4 |
| X7 | A consumption row drifts from the owner's published shape, or a fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X8 | The document declares a treatment, case, deviation, document or ACE table, a `v_ace_*` view or a cross-schema key | The absence test fails the build | None | AC6 |
| X9 | The document declares another service's operation as provided | The review fails the baseline; the row is described as consumed and faked | None | AC5 |
| X10 | The monolith base appears in the document, its examples or its fakes | The absence test fails the build | None | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the notice and proof-of-delivery contracts it extends, the Ownership Map rows and the decision library only |
| Negotiable | The two paths, the view reference, the offer facts and the physical types are settled at the baseline review; the base, the topic, the queue and the naming are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the two owner teams on the same day, and makes a silent drift of a channel value, a consent answer or the delivery event impossible |
| Estimable | One additive document change, two element sets, one consent block, two consumed shapes, four event rows, six fakes and ten tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the offer view on a digital channel

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the notice contract RWB-P6-E1052-CON is published with the notice resource and its template reference, and RWB-P6-E1055-CON is published with the proof-of-delivery element

  Scenario: AC1 The two channel operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /notices/{noticeId}/channel-view answering 200 with NoticeChannelView and POST /notices/{noticeId}/views answering 201 with NoticeView, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the GET declares the query parameter channel required and one of LOV-CHANNEL, and declares no Idempotency-Key; the POST declares the Idempotency-Key header and a stored answer
    Then both operations declare the capability area Litigation with right R on the GET and right C on the POST, scope applied, a 2 s budget, and the refusals 400, 401, 403, 404, 409, 422 and 503 as application/problem+json with the shared Problem schema and one messageCode per condition
    Then the document marks both operations as new, because the eleven operations of the TSD P6 inventory API-P6-001 to API-P6-011 hold no offer view (GAP-1130; ASM-2078)
    Then the document states that the area and the right are inherited from API-P6-001 and API-P6-002 of the notice resource, because no source names a right for an offer view, and that the customer's own identity is authorised at the edge (GAP-1134; ASM-2082)
    Then every added property is additive within major version 1, so a consumer of the notice resource keeps working
    Then the document declares no second base, no second resource and no operation of another service

  Scenario: AC2 The channel view and view element sets are fixed, and the view row is this service's while the offer, the contact point and the consent stay their owners' (new, D-RCV-60)
    Given the two element sets of the baseline
    When they are compared with the notice and template rows of TSD P6 T3.1 and with the legacy data table
    Then NoticeChannelView carries noticeId, caseId, noticeType, templateCode, templateVersion, language, channel, bodyRef, offerId, offerValidityDate and mergeValues
    Then NoticeViewRequest requires channel and viewedAt, and NoticeView carries viewId, noticeId, caseId, channel, viewedAt and deliveryStatus
    Then noticeId and caseId are uuid as DF-LEG-015 and DF-LEG-016 give them, noticeType is varchar(25) on LOV-NOTICE as DF-LEG-018, templateCode is varchar(30), templateVersion an integer and language varchar(2) on LOV-LANG as DF-REF-046, DF-REF-047 and DF-REF-048, and channel is varchar(15) on LOV-CHANNEL as DF-REF-066
    Then the type of offerId, offerValidityDate, mergeValues, viewId, viewedAt and deliveryStatus and the name of the offer facts are Not specified in the source documents (GAP-1131; ASM-2079; GAP-1133; ASM-2081)
    Then the two channels of the feature are declared as LINE and PORTAL of LOV-CHANNEL, HOME.SCB being the portal, and no WEB value is added
    Then the notice_view note declares the view row as this service's own table in rwb_comms, with the notice, the case, the channel, the viewed-at and the session reference, and its field IDs and physical types as the placeholder (GAP-1133; ASM-2081)
    Then the note declares the two notice columns a view moves, callback_date DF-LEG-021 and delivery_status DF-LEG-022, and no treatment, case, deviation, document or ACE table, no column of one and no cross-schema key (DP-01)

  Scenario: AC3 The consent and contact-stop element block is declared from the two validation rules (new, D-RCV-60)
    Given the refusal block of the baseline
    When it is compared with VR-P6-014-1, VR-P6-014-2 and the message table of the legacy story
    Then the block declares the contact point of the channel, its verification state and its consent state as read from the rwb-source-data contract (consentStatus GIVEN, WITHDRAWN or UNKNOWN; verifiedAt), and the contact-stop answer with its reason as held by rwb-comms from the DeviationRaised and DeviationCleared events of rwb-deviation
    Then the block declares the pair VR-P6-014-1 with MSG-P6-001 and VR-P6-014-2 with MSG-P6-002, both answering 409 on the two operations
    Then the block declares that both checks are re-run at the moment of the record and that a missing answer of the rwb-source-data read refuses the view (fail closed)
    Then the field types follow rwb-source-data.yaml 5.1.0 for the LINE channel, and the read of the PORTAL channel is pending (NEW-GAP-G6-3)
    Then the block declares no contact point, no name and no consent value in a schema example or a fake, and the merge values are declared as rendered at request time and never stored
    Then the block declares the offer in force and its validity date as read from the rwb-treatment contract, with the field names as the placeholder (GAP-1131; ASM-2079)
    Then the decision code of the view is declared as the placeholder Not specified in the source documents (GAP-2365), with the rule id and the rule version taken from the offer on the rwb-treatment contract, and the contact-stop picture is declared as internal state of rwb-comms fed by DeviationRaised and DeviationCleared (GAP-2365)

  Scenario: AC4 The event rows are declared and no event of this service is invented (new, D-RCV-60)
    Given the event sections of the baseline
    When they are compared with Architecture v5 slide 42, TSD P6 T5.3 and DP-03
    Then the only published row is rwb.comms.NoticeDelivered.v1 (EV-15) on rwb.comms.events.v1 with its retry and .dlt topics, owned by P6 and keyed by caseId, carrying the notice, the case, the delivered date, the callback date, the delivery status and the channel
    Then the element reuses the shape RWB-P6-E1055-CON declares and adds channel additively within major version 1, and the document states one delivery event per notice: the first delivery publishes it, WIN or digital (GAP-1132; ASM-2080)
    Then the document justifies the publication of EV-15 by the measure "notices with proof of delivery" of FSD P6 A2.14.1 and by catalogue row 15, and records that no source states which event a digital view raises (GAP-1132; ASM-2080)
    Then the consumed rows are rwb.case.CaseStateChanged.v1 (EV-05), rwb.deviation.DeviationRaised.v1 (EV-06), rwb.deviation.DeviationCleared.v1 (EV-07) and rwb.treatment.TreatmentApproved.v1 (EV-10), each with its topic, its owner, its key and its inbox dedupe
    Then the document declares no NoticeGenerated and no NoticeDispatched, because rows 13 and 14 are the dispatch stories', and no event of another service as its own
    Then no payload carries a name, an address, an identity number or a contact point, and every payload validates with BACKWARD compatibility

  Scenario: AC5 The consumed rows, the fakes and the drift test are declared with their call type and their owner (new, D-RCV-60)
    Given the consumed rows and the fake set of the baseline
    When they are reviewed against the Ownership Map and the connection matrix of Architecture v5 slide 13
    Then GET /contact-points of rwb-source-data.yaml 5.1.0 and GET /treatments/{treatmentId} of the rwb-treatment contract are declared as consumed rows, each one hop with a 2 s timeout and a breaker, each faked
    Then rwb-source-data.yaml 5.1.0 is named as the P1 contract and no S2 contract story is named for this key (GAP-1131; ASM-2079)
    Then the fake set answers a verified contact point with consent given, consentStatus WITHDRAWN and UNKNOWN, a contact point with no verifiedAt and a 503 from the rwb-source-data fake, a contact stop from the deviation-event fake, an offer in force, no offer, an expired offer, a closed case, a legal hold, a duplicated event and a delayed answer beyond 2 s
    Then the fake set answers the 201 and the 200 of the two operations, the repeated Idempotency-Key and every refusal of AC1, and the decision-record stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference, and the document declares no operation of another service as provided and no file row
    Then the two reads of rwb-treatment and rwb-source-data and the two consumed deviation events are built against fakes derived from the published contracts, and the drift test holds them until the S2, P1 and S8 contract and integration stories are planned and added to the C and I lists of the split plan (GAP-2368)

  Scenario: AC6 The nine contract tables, the naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the contract section of this story
    When its nine sub-tables are reviewed against the Template and Rules and the Ownership Map
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty and a reason beside it
    Then the tables named as owned are notice, notice_view, template and merge_field of rwb_comms with the library objects applied in that schema, and treatment, party_ext, contact_point_ext, account_ext, recovery_case, deviation, document, decision_log_entry, rule_row and any v_ace_* view are named as other owners' and consumed only through their contracts
    Then the schema is rwb_comms, the base is /api/recovery/comms/v1, the topic is rwb.comms.events.v1 with retry and .dlt topics, the event names are rwb.comms.<Event>.v1, the task queue is rwb-comms in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.comms
    Then no query of this service on rwb_treatment, rwb_case, rwb_source_data, rwb_deviation, rwb_document or a v_ace_* view is declared, and no cross-schema key is declared (DP-01, DP-05)
    Then the absence test fails a build that declares a table of another owner, a read of one or the monolith base in the document, its examples or its fakes
    Then no workflow, no Schedule and no file element is declared, and the document says why

  Scenario: AC7 Every business rule of section 8 is carried by a criterion or a test (new, D-RCV-60)
    Given the business rules BR1 to BR14 of section 8
    When each rule is compared with the criteria of section 7 and the test cases of section 16
    Then each of BR1 to BR14 is covered by a criterion or a test, or is a guardrail or boundary test named in the document
    Then the test data of this criterion is Not specified in the source documents (NEWAC-RWB-P6-E4035-CON-AC7)

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the status model of the view is Not specified in the source documents (NEWAC-RWB-P6-E4035-CON-AC8)
    When a status change the model does not allow is sent to the view
    Then the change is refused and no status is stored (response shape Not specified in the source documents (NEWAC-RWB-P6-E4035-CON-AC8))

  Scenario: AC9 The write declares the shared idempotency answers (new, RD-P1-001, RD-P1-004)
    Given the POST /notices/{noticeId}/views operation of the document
    When its Idempotency-Key and error declarations are reviewed
    Then the header is required with format uuid, and a missing or non-UUID value answers 400 with messageCode MSG-PLT-N009-03
    Then the same key and body replays the stored status and body for 24 hours
    Then a key reused with another body or still in flight answers 409 with messageCode MSG-PLT-N009-05
    Then an unavailable key store answers 503 with messageCode MSG-PLT-N009-06
    Then every 4xx and 5xx is application/problem+json with the shared Problem schema, whose code member is messageCode
```

AC1, AC3 and AC5 are restated in version 3 and AC9 is new. TC: TC-P6-E4035-CON-01, TC-P6-E4035-CON-03, TC-P6-E4035-CON-05, TC-P6-E4035-CON-10 (Test Cases v9).

These six criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story and they restate no business outcome of RWB-P6-E4035-APP, which owns AC1 and AC2 of RWB-E4-035.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD P6 T6.2 |
| BR4 | Error responses use one envelope and one message ID per condition; a text the sources do not give carries the placeholder | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | The view row is this service's; the offer and the treatment rows are S2's, the customer, the contact point and the consent are P1's, and no table of theirs is declared or read here | DP-01; DP-05; Ownership Map |
| BR8 | The decision record of a view is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR9 | No business value is fixed in the contract: the channel list, the decision code, the rule id, the offer facts and the refusal texts stay data or reference data read with the version in force | FSD P6 A2.14.3.1 (BR-P6-014); Template and Rules §R7.2 s17 |
| BR10 | The contact stop and the missing consent are the two refusals of the channel and carry MSG-P6-001 and MSG-P6-002 on both operations | VR-P6-014-1; VR-P6-014-2; legacy RWB-E4-035 validation table |
| BR11 | One `NoticeDelivered` per notice: the first delivery, WIN or digital, publishes it, and a later view publishes nothing | Architecture v5 slide 42 (event 15); RWB-P6-E1055-CON |
| BR12 | The two owner reads are consumed and faked, and the C rows are added when a P1 and an S2 contract story are planned | Ownership Map; Template and Rules §R5.4 |
| BR13 | A contract that carries a name, an address, an identity number or a contact point in a schema, an example or a fake fails the review | Template and Rules §R7.2 s17; TSD P6 T6.2 |
| BR14 | Every element the sources do not name is declared as the placeholder with its gap and assumption pair and is never guessed | Template and Rules §R9 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the two element sets, the consent block, the event rows and the consumed rows are described | In review |
| In review | Consumer sign-off | `RWB-P6-E4035-APP`, the two owner teams and the library owner accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example the offer field names once rwb-treatment publishes them | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, a path changes or a refusal status changes | New major version drafted |
| Baselined | Drift in a fake or in a consumed shape | The drift test fails | In review |
| Baselined | A table of another owner, a cross-schema key or the monolith base is declared | The absence tests of AC6 fail | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| the channel of a view | `LINE`, `PORTAL` of LOV-CHANNEL (TSD P6 T3.2); HOME.SCB is the portal | Declared as the list reference and narrowed by the parameter; the closed list is not extended and no channel is added |
| notice.delivery_status | `DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING` (LOV-DELIVERY, TSD P6 T3.2) | Declared as the list reference; a view writes `DELIVERED` and the notice lifecycle itself is RWB-P6-E1055-CON's |

The notice lifecycle and the transition a view makes are `RWB-P6-E4035-APP`'s, and the offer's own validity is rwb-treatment's. This document fixes the surface and shows nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (RWB-P6-E4035-APP, the sibling P6 stories that read the notice, and the rwb-source-data, rwb-treatment and P7 library owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the CloudEvents envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element is declared in the channel view, in a view, in an answer or in a fake, and that the merge values are declared as rendered and not stored |
| Business analyst of P6 | Confirms that the channel list, the decision code and the rule id are named as reference data and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_comms` by the naming rule of DP-02; the document names the scheme and not a credential. The rights of the two operations are declared here, their role lists are rwb-access data, and no role code is written in the document. The customer is not a Recovery role in TSD P6 T6.1, so the document declares the edge as the place where the customer's own identity is authorised and records the point as a gap (GAP-1134; ASM-2082).

### 11. Data

The contract baseline declares shapes, not business values.

| Element | Legacy field of the notice or the template | Type and width | Required | List |
|---|---|---|---|---|
| noticeId | DF-LEG-015 id | uuid | Yes | None |
| caseId | DF-LEG-016 case_id | uuid | Yes | None |
| noticeType | DF-LEG-018 notice_type | varchar(25) | Yes | LOV-NOTICE |
| templateCode | DF-REF-046 template_code | varchar(30) | Yes | None |
| templateVersion | DF-REF-047 template_version | integer | Yes | None |
| language | DF-REF-048 language | varchar(2) | Yes | LOV-LANG |
| channel | DF-REF-066 channel | varchar(15) | Yes | LOV-CHANNEL, narrowed to `LINE` and `PORTAL` |
| bodyRef | DF-REF-050 body_ref | varchar(400) | Yes | None |
| mergeValues | DF-REF-069 merge_codes of the template, resolved through DF-REF-252 to DF-REF-260 | Not specified in the source documents (GAP-1133; ASM-2081) | No | None |
| offerId | none in the notice; the treatment reference of S2 | Not specified in the source documents (GAP-1131; ASM-2079) | Yes | None |
| offerValidityDate | none in the notice; the offer validity of S2 | Not specified in the source documents (GAP-1131; ASM-2079) | No | None |
| viewId | the view row this document declares | Not specified in the source documents (GAP-1133; ASM-2081) | Yes | None |
| viewedAt | the view row this document declares | Not specified in the source documents (GAP-1133; ASM-2081) | Yes | None |
| deliveryStatus | DF-LEG-022 delivery_status | varchar(15) | No | LOV-DELIVERY |
| sessionRef | the channel session the edge presents | Not specified in the source documents (GAP-1133; ASM-2081) | No | None |
| Standard columns | state, version, created_by, updated_by, is_active of TSD P6 T3.0 | boolean, varchar(40), uuid, boolean | n/a | None |

| Item | Content |
|---|---|
| Request | The GET carries `noticeId` in the path and `channel` as the only query parameter. The POST carries `noticeId` in the path and `NoticeViewRequest` with `channel` and `viewedAt`, both required; no field is a name, an address, an identity number or a contact point |
| Answer | 200 with `NoticeChannelView` and 201 with `NoticeView`; the view answer carries the view reference, the notice and case references, the channel, the viewed-at and the delivery status |
| Consent and contact stop | The contact point token of the channel, `verifiedAt` and `consentStatus` (GIVEN, WITHDRAWN, UNKNOWN) read from rwb-source-data.yaml 5.1.0 at the moment of the request and re-read at the moment of the record; the stop with its reason held by rwb-comms from the deviation events of rwb-deviation. Customer facts: `GET /customers/{personKey}` through gateway-bff, masked (RD-P1-060). Pending: the `PORTAL` channel read (NEW-GAP-G6-3) |
| View row | `notice_view` in `rwb_comms`: the notice, the case, the channel, the viewed-at and the session reference; its name, columns and field IDs are the placeholder (GAP-1133; ASM-2081) |
| Decision record | The library's element: the notice, the case, the channel, the offer reference, the viewed-at, the decision code, the rule id and version, the final call and the decided-at (DP-03) |
| Delivery event | `rwb.comms.NoticeDelivered.v1`: the notice, the case, the delivered date, the callback date, the delivery status and the channel; key caseId (EV-15); the element of RWB-P6-E1055-CON, published on the first delivery of a notice and never by a later view (BR11) |

**No table of another owner and no migration of one.** `notice`, `template` and `merge_field` are the P6 rows of TSD P6 T3.1 and this document adds the `notice_view` note and names the two notice columns a view moves, and nothing else. `decision_record`, `idempotency_key`, `outbox_event` and `processed_event` are platform library objects created in `rwb_comms` by the library's migration and are named here, not declared. `treatment`, `party_ext`, `contact_point_ext`, `account_ext`, `interaction`, `recovery_case`, `deviation`, `document`, `decision_log_entry`, `rule_row` and every `v_ace_*` view are other owners' and appear only as consumed shapes. `notice.case_id` and `notice.template_id` are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element of this contract carries a name, an address, an identity number, an account number or a contact point. The notice, the offer and the contact point are reached by identifiers, the channel is a LOV code, and the merge values are declared as rendered at request time and never stored; the personal-data flag of a merge code is read from DF-REF-258 so the renderer can mask and the contract can test it. The session reference is an identifier only; whether it is personal data is read from Data Classification v5, and it is never a name, an address or a contact point.

**Reference data.** The lists the contract reads, LOV-NOTICE, LOV-LANG, LOV-CHANNEL and LOV-DELIVERY, and the template and merge rows, are read with the version in force through the reference-data contract of DP-06 and DP-07; no parameter value is fixed here (BR9).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Both operations are new: no offer view is in the endpoint inventory of the TSD (GAP-1130; ASM-2078).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| new | GET | `/notices/{noticeId}/channel-view` | `noticeId` from the path; query `channel` required, one of LOV-CHANNEL | 200 with `NoticeChannelView` | Litigation R, scope applied | Not applicable | 400, 401, 403, 404, 409, 422, 503 |
| new | POST | `/notices/{noticeId}/views` | `noticeId` from the path; `NoticeViewRequest` | 201 with `NoticeView` | Litigation C, scope applied | `Idempotency-Key` (UUID) required, stored status and body replayed for 24 hours | 400, 401, 403, 404, 409, 422, 503 |

The purpose, the shapes and the refusals are this baseline's own, because no TSD P6 T-A.1 row names an offer view; the base and the naming are DP-13's and DP-14's. The two notice operations of the module, API-P6-001 (Litigation C) and API-P6-002 (Litigation R), are `RWB-P6-E1052-CON`'s and `RWB-P6-E5002-APP`'s and are not redeclared here; the capability area and the right of the two new operations are inherited from them, because TSD P6 T6.1 names no offer-view right and no customer role (GAP-1134; ASM-2082). The element members and the physical types the sources do not name carry the placeholder of section 11.

#### 12.2 REST operations consumed

None declared as an operation of this document; the two rows below are the consumed shapes the app story calls, each one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020).

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| `GET /api/recovery/source-data/v1/contact-points?personKey=&channel=LINE` of rwb-source-data.yaml 5.1.0 | P1 rwb-source-data | `contactKey` token, `contactType`, `consentStatus` (GIVEN, WITHDRAWN, UNKNOWN), `verifiedAt`, `failedCount`, `dataAsOf`; no contact stop and no customer fact; 400, 401, 403 and 503 | Consumed and faked from the published contract. Customer facts: `GET /customers/{personKey}` through gateway-bff, masked (RD-P1-060). Pending: the `PORTAL` read, the `personKey` source (NEW-GAP-G6-3) and whether a view appends to the case ledger (NEW-GAP-F15-5) |
| `GET /treatments/{treatmentId}` of the rwb-treatment contract | S2 rwb-treatment | The answer elements the channel view renders: the offer reference, its type and its validity | Consumed and faked; no C row, because no S2 contract story is named; the field names of the amount and the validity date are the placeholder (GAP-1131; ASM-2079) |

No row reads a table, no row reads a `v_ace_*` view, and no row is declared as a provided operation of this service (BR6, BR7).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 rwb-comms | noticeId, caseId, deliveredDate, callbackDate, deliveryStatus and channel; key caseId; written to the outbox in the same transaction as the view row, by `RWB-P6-E4035-APP` |

The element reuses the shape `RWB-P6-E1055-CON` declares for the WIN path and adds `channel` additively within major version 1, so one consumer reads one element on either path. The document states the once-per-notice rule: the first delivery publishes the event and a later view publishes nothing (BR11). The publication on a digital view is justified by the measure "notices with proof of delivery, 100 percent" of FSD P6 A2.14.1 and by catalogue row 15 of Architecture v5 slide 42, whose owner is P6 and whose consumers are rwb-litigation, rwb-guarantee and rwb-case; no source states which event a digital view raises, so the trigger is a decision of this baseline and is recorded as a gap (GAP-1132; ASM-2080). Rows 13 `NoticeGenerated` and 14 `NoticeDispatched` are the dispatch stories' and are not declared here.

#### 12.4 Events consumed

| Event | Topic | Owner | Key | Consumer contract element |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | caseId | the from and to states, the legal-hold flag and the changed-at, consumed inside rwb-comms so the channel view can be refused on a held case, with the inbox dedupe |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId | the case, the deviation type and the raised-at, consumed so a contact stop refuses the view between two owner reads (VR-P6-014-1) |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId | the case, the clearance and the cleared-at, consumed so the local stop flag is cleared |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | Not specified in the source documents (GAP-1131; ASM-2079) | the case and the approved offer reference, consumed so a case with no approved offer is refused without a second owner read |

The four rows are consumed by `RWB-P6-E4035-APP`; this baseline fixes their names, their topics, their owners and their keys and declares no subscription of its own. The shape of the local projection that answers each row carries IDs, codes and dates only and no personal data.

#### 12.5 Workflows and activities

None. The channel view is one synchronous read and the view record is one synchronous write with one library write and one outbox row; this document declares no workflow, no child workflow and no activity, and `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is declared: JOB-10 of the catalogue is the daily WIN dispatch of `RWB-P6-E2021-APP` with rwb-integration, and no job row is read or changed by this document (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| notice | `rwb_comms` | P6 | The notice of the offer, its `template_id` (DF-LEG-031), its state, and the two delivery columns a view moves, `callback_date` (DF-LEG-021) and `delivery_status` (DF-LEG-022) |
| notice_view | `rwb_comms` | P6 | The view row: the notice, the case, the channel, the viewed-at and the session reference; declared here and created by `RWB-P6-E4035-APP` (GAP-1133; ASM-2081); not in LDM v9 or Data Classification v5, recorded here as the service's own table |
| template | `rwb_comms` | P6 | Read for the code, version, language, body, approval, validity and channel; written by the template stories |
| merge_field | `rwb_comms` | P6 | Read for the merge codes, their source entity and field and their required and personal-data flags; written by the catalogue story |
| decision_record, idempotency_key, outbox_event, processed_event | `rwb_comms` | PLT library objects applied in this schema | The decision entry of a view, the stored answer of the POST, the envelope of the published row and the inbox of the four consumed rows (DP-03); `decision_record` is not in LDM v9 or Data Classification v5 and is recorded here as a library object |

`treatment` and the treatment timers are S2's; `party_ext`, `contact_point_ext`, `account_ext`, `interaction` and the data-product rows are P1's; `recovery_case`, `task`, `timer` and `queue` are P3's; `deviation` is S8's; `document` is P5's; `decision_log_entry`, `rule_row` and the rule package rows are P7's; `outbound_item` and `interface_config` are P2's. They are named as consumed answers only, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Channel-view fake | The two operations of 12.1 | A 200 with `NoticeChannelView` for each of `LINE` and `PORTAL`, a 201 with `NoticeView`, the repeated `Idempotency-Key` returning the first answer, and the 401, 403, 404, 409, 422 and 503 refusals |
| Contact and consent fake | The first row of 12.2 | rwb-source-data.yaml 5.1.0: a verified contact point with `consentStatus` GIVEN; WITHDRAWN; UNKNOWN; a contact point with `verifiedAt` null; a 503; an answer delayed beyond 2 s |
| Offer fake | The second row of 12.2 | An offer in force with its validity date; no offer; an expired offer; an answer delayed beyond 2 s |
| Case-event fake | The first row of 12.4 | An open case, a closed case, a legal hold and a duplicated event for the inbox |
| Deviation-event fake | The second and third rows of 12.4 | A stop raised, the same stop cleared and a duplicated event for the inbox |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Drift test | Every fake against the document | A drifted fake fails the build |

The owner fakes are stubbed from the owners' published documents and carry the placeholder where the source is silent (GAP-1131; ASM-2079; GAP-1133; ASM-2081).

The customer, the contact point and the consent are set up in every Given and test-data line through the contact and consent fake of this section, which is the rwb-source-data contract fake, never through an ACE view or an extension table. Screen states the contract answers: empty is the 404 for an unknown notice; loading is the answer delayed beyond a threshold Not specified in the source documents (DOR-RWB-P6-E4035-CON-10); error is the 503; no access is the 401 and the 403 of MSG-P4-002.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The channel view and the view record provided; the contact point and consent read and the offer read consumed; one hop, 2 s |
| Kafka | 1 declared as published by the app story, 4 consumed | `NoticeDelivered` on `rwb.comms.events.v1`; `CaseStateChanged`, `DeviationRaised`, `DeviationCleared` and `TreatmentApproved` consumed; `DecisionRecorded` written by the local library on the shared topic |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | No file element in this contract; the channel screens are the edge's |

### 13. Solution plan

**Package.** Contract artefact of the service: the addition to `openapi/rwb-comms-v1.yaml` for the channel view of the notice, the `NoticeChannelView`, `NoticeView` and `NoticeViewRequest` schemas in `th.co.scb.ace.workbench.recovery.comms.api`, the `notice_view` note, the decision-record fragment, the `NoticeDelivered` fragment, the fake set and the drift test. The implementation behind it is `RWB-P6-E4035-APP`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming app story carries the H row |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this document declares the rwb-source-data contact read and no view of its own | referred to; the consuming app story carries the H row of its own list and no P1 row |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the channel answers are reached through it and the contract declares no composite route | referred to; the consuming app story and the platform edge story carry the H row |

DP-13 is the pattern this story publishes. DP-13 also fixes that the legacy base appears nowhere in the document, its examples or its fakes. DP-05 is named because the legacy story read `v_ace_customer` and the target reads the published rwb-source-data contact read instead; it adds no dependency, and DP-01 stands behind the boundary as a rule. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-19 is the route the two channels use and is `RWB-PLT-N001-CON`'s. This story being a CON story, it holds no build dependency by rule (Template and Rules §R5.7 rule 1).

**Components**

| Component | Type | Responsible for |
|---|---|---|
| ChannelViewOpenApi | Document | The base, the two operations, the security, the error set and the versioning section (BR1 to BR6) |
| ChannelViewSchema | Published schema | `NoticeChannelView`, `NoticeViewRequest` and `NoticeView` with their elements, the required set and the channel rule (BR9, BR10) |
| ConsentBlock | Document | The contact point, its verification state, its consent state, the stop with its reason and the two validation rules with their message IDs (BR10) |
| ViewTableNote | Resource | The `notice_view` row and the two notice columns a view moves (BR7) |
| DecisionElement | Document | The decision-record element of a view on the shared topic (BR8) |
| DeliveryElement | Document | The `NoticeDelivered` element, its `channel` addition and its once-per-notice rule (BR11) |
| ConsumedShapes | Document | The two owner reads and the four consumed events, with their placeholders (BR6, BR12) |
| ProblemEnvelope | Reused schema | The shared `Problem` schema of the platform, `application/problem+json`, with `messageCode` (BR4) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR3) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers of every consuming build (AC5) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC5, AC6) |

**Database.** The `notice_view` note declares one table of this service in `rwb_comms`, applied by the service's own Flyway sequence and never editing an applied migration (DP-15), and names the two notice columns a view moves; its field IDs are the placeholder of section 11. No table of another owner is created and no other schema is named in the note.

**Configuration and reference data.** The channel list, the decision code, the rule id, the offer facts and the refusal texts are reference data or parameters read with the version in force (BR9). The problem envelope, its member names and its `messageCode` member are those of the shared `Problem` schema and are reused, not redeclared.

**Build steps**

1. Add the channel view resource and the two operations to the document and lint the paths, the rights and the additive rule (AC1).
2. Write the three schemas with their elements, the required set, the channel rule and an example; validate the example (AC2).
3. Write the consent block with the two validation rules and their message IDs, and the absence tests for a stored contact point (AC3).
4. Write the `notice_view` note and the two notice columns, and the absence tests for a table of another owner and a cross-schema key (AC2, AC6).
5. Write the error section with one message ID per condition and the `Idempotency-Key` rule of the write (AC1).
6. Write the decision element, the `NoticeDelivered` element with its once-per-notice rule, and the four consumed event rows (AC4).
7. Write the two consumed owner reads with their placeholders, generate the fake set and the drift test, and wire the drift test into the build of `RWB-P6-E4035-APP` (AC5).
8. Write the naming and boundary section and the absence tests for the old base, a second topic and an event of another service (AC6).
9. Publish v1 and record the pinned version of this contract and of each consuming story.

**Feature flag.** `rwb.comms.offer-channel-view-contract`.

**Done when.** The document lints, the three schemas validate, the `notice_view` note applies twice, the fakes answer every status including the repeated key, the absence tests are green and `RWB-P6-E4035-APP` has accepted the baseline.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-P6-001 | A contact stop is in force for the customer (VR-P6-014-1) | 409, problem body with `messageCode` MSG-P6-001 and the reason | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | The customer has not consented to the channel (VR-P6-014-2) | 409, problem body with `messageCode` MSG-P6-002 and the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn or not approved for the channel | 409, problem body with `messageCode` MSG-P6-003 and the template | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision record cannot be written by the consuming story (legacy AC2) | 503, problem body with `messageCode` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageCode` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required property is missing, or `channel` is outside LOV-CHANNEL | 422, problem body with `messageCode` MSG-GEN-001 and `field` | Enter {field}. |
| Not specified in the source documents (GAP-1131; ASM-2079) | No offer is in force, the offer validity has passed, an owner does not answer, or the case is under legal hold | A 409 or a 503 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |

The six messages of the legacy validation table are the six this surface raises and are copied unchanged. The two refusals the module gives this feature, VR-P6-014-1 with MSG-P6-001 and VR-P6-014-2 with MSG-P6-002 (FSD P6 A2.14.3.1), are declared on both operations, because a stop raised between the read and the record must still stop the record. No text is invented and no message is added to the list.

### 15. Screens and states

The legacy story names SCR-33 Template approval, and that screen shows a template and its approval states, so it cannot show an offer to a customer; the P6 screen list of FSD P6 gives this feature no identifier, and the two channels are external — LINE through LINE OA and the web through HOME.SCB (FSD P6 A2.14.2) — so the screen identifier, the field list and the masking are Not specified in the source documents (GAP-1135; ASM-2083), and the fields a customer channel is shown and the contact-point fields that prove consent are Not specified in the source documents (GAP-2366). Both channels are reached through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the channel view and once for the view record and merges the answers.

| Surface | State | What this contract serves |
|---|---|---|
| The offer on LINE or on the portal | Sent, template approved for the channel, offer in force | The 200 `NoticeChannelView` with the offer facts, the validity date and the merge values |
| The offer on LINE or on the portal | A contact stop or no consent | The 409 with MSG-P6-001 or MSG-P6-002 and nothing rendered |
| The offer on LINE or on the portal | Template withdrawn, or no offer in force | The 409 with MSG-P6-003 or the placeholder of section 14 |
| The offer on LINE or on the portal | Opened | The 201 `NoticeView`, the notice `DELIVERED` with the view date as its callback date, and one `NoticeDelivered` |
| The offer on LINE or on the portal | Empty, loading, error or no access | Not specified in the source documents (CG-ALL-6655) |

The route, the merge order, the field list and the masking of a merge value at the edge belong to `RWB-PLT-N001-CON`; the transitions behind each state and the case owner's notice screen are the app story's and `RWB-P6-E5002-APP`'s. The two offer-view operations take the Litigation area with right R on the read and right C on the write, the right of the notice resource they extend, scoped on the case; the customer identity is carried by the gateway-bff route and the web channel is `PORTAL` (GAP-1134; GAP-2367). The two notice endpoints and their Litigation rights stay with `RWB-P6-E1052-APP` and `RWB-P6-E2021-APP`, and SCR-33 stays with the template stories (GAP-2363).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-035-02 | AC2 | Contract | Decision log stubbed unavailable; the contract half answers the stopped chain and the 503 of MSG-P7-003 |
| TC-E4-035-03 | Access | Contract | A role without Litigation R sends the GET and a role without Litigation C sends the POST; the contract half answers the 403 of MSG-P4-002 |
| TC-E4-035-04 | Principle 5 | Contract | The stopped chain of the library stub on 10 views; the contract half answers the same 503 and the drift test |
| TC-P6-E4035-CON-01 | AC1 | Contract | The document validates; the two operations, the query parameter, the rights, the `Idempotency-Key` rule, the two new markers and the six refusals are present; Notice `N-0401` of case `RC-2026-000401` with template `OFFER-LINE` version 3 on channel `LINE`; the contract half answers the 200 `NoticeChannelView` and the 201 `NoticeView` with offer `TRT-2026-000401` in force |
| TC-P6-E4035-CON-02 | AC2 | Contract | The two element sets, the required members, the types the sources give, the placeholders, the channel rule, the `notice_view` note and the two notice columns are present; no table of another owner is declared |
| TC-P6-E4035-CON-03 | AC3 | Contract | The consent block, the two validation rules with MSG-P6-001 and MSG-P6-002, the re-run at the record and the placeholders are present; no contact point is stored |
| TC-P6-E4035-CON-04 | AC4 | Contract | The `NoticeDelivered` element with `channel`, its once-per-notice rule, the four consumed event rows with their owners and keys, and the absence of `NoticeGenerated` and `NoticeDispatched` |
| TC-P6-E4035-CON-05 | AC5 | Component | The two consumed rows, the six fakes and the library stub match the document; a drifted fake or shape fails the build |
| TC-P6-E4035-CON-06 | AC6 | Contract | The nine sub-tables with their owners, the naming baseline and the absence tests for a table of another owner, a cross-schema read and the old base |
| TC-P6-E4035-CON-07 | AC6 | Contract | Boundary of 12.7: each owned table and each consumed table named once at its edge; a table name outside 12.7 read or declared fails the build |
| TC-P6-E4035-CON-08 | AC7 | Contract | Not specified in the source documents (NEWAC-RWB-P6-E4035-CON-AC7) |
| TC-P6-E4035-CON-09 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-P6-E4035-CON-AC8) |

The four legacy identifiers keep their legacy order, their legacy covers and their legacy data, and carry the level of the surface they prove here, which is the contract: the legacy table has no level column, and the end-to-end proof of the same cases is RWB-P6-E4035-APP's. The `AC1` and `AC2` of the four legacy rows are the criteria of RWB-E4-035 and not the criteria of this story. The six `TC-P6-E4035-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

Version 3: rows that cite `TC-P6-E4035-CON-` identifiers are this story's rows of Recovery Workbench Test Cases v9. Where a shared legacy identifier now names another story's case there, this story's identifier replaces it, and cases run by one identifier are joined in one row.

### 17. Guardrails

- No business value in the contract: the channel list, the decision code, the rule id, the offer facts and the refusal texts stay data or reference data read with the version in force.
- No personal data in a schema, an example or a fake: identifiers, codes, dates and channel values only, and the merge values are declared as rendered and never stored.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the two owner reads are consumed and faked, never declared as provided (DP-01, DP-05).
- No table of another owner and no cross-schema read: the absence test of AC6 fails a build that declares a treatment, case, deviation, document or ACE table, a column of one, a query on a `v_ace_*` view or a cross-schema key.
- The old monolith base appears nowhere: not in the document, not in an example and not in a fake, and a build that adds it fails.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is invented: the only published row is `NoticeDelivered` (EV-15), rows 13 and 14 are the dispatch stories', and the four consumed rows are the catalogue's.
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the view reference, the viewed-at type, the `notice_view` columns, the offer field names, the `PORTAL` contact read (NEW-GAP-G6-3), the refusal texts, the decision code and the rule id.
- Every example in the document is synthetic; no production payload, identifier or file is copied into a schema or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-035 |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4035-APP; this baseline copies neither |
| Legacy test cases | TC-E4-035-01 to TC-E4-035-04, as the contract half of each case |
| New contract cases | TC-P6-E4035-CON-01 to TC-P6-E4035-CON-06 |
| Legacy feature | FEAT-COM-01 View the offer on LINE and web (FSD P6 A2.14), prerequisite FEAT-OCC-04 |
| Legacy endpoints | `POST /cases/{caseId}/notices` (API-P6-001, Litigation C) and `GET /notices/{noticeId}` (API-P6-002, Litigation R), both other stories' and named only as the source of the area and right |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-023 and DF-LEG-030 to DF-LEG-034; template DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069; merge_field DF-REF-252 to DF-REF-260; v_ace_customer DF-ACE-055 to DF-ACE-074; treatment DF-TRT-001 to DF-TRT-014; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 and DP-15 applied as rules) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | VR-P6-014-1, VR-P6-014-2, BR-P6-014, R-UNI-20, R-UNI-39, R-RES-09, R-RES-19, R-LIT-05 |
| Requirements | REQ-OCC-011, the requirement TSD P6 T8 maps to FEAT-COM-01 and marks "written one epic ahead" |
| Contract and tests | This document and TC-P6-E4035-CON-01 to TC-P6-E4035-CON-06 |

### 19. Out of scope

- The implementation of the two operations, the checks, the decision write, the view row, the two notice columns and the repeat-key answer (RWB-P6-E4035-APP).
- The offer, its plan, its validity and its approval: S2 rwb-treatment. This baseline names the consumed read and writes none of it.
- The customer, the contact point and the consent, and the contact repository: P1 rwb-source-data and RWB-P6-E4039-APP.
- The contact stop and the deviation that raises it: S8 rwb-deviation and R-RES-19, R-LIT-05.
- The case state, its closure and the legal hold: P3 rwb-case.
- The template and merge-field catalogue and the approval of a template version: RWB-P6-E1046-CON, RWB-P6-AD017-CON and RWB-P6-E1034-CON.
- The notice generation contract, the notice operations of the module and the returned WIN proof: RWB-P6-E1052-CON, RWB-P6-E5002-APP and RWB-P6-E2021-CON.
- The dispatch of a notice, JOB-10, the WIN file and `NoticeDispatchWorkflow`: RWB-P6-E2021-CON, RWB-P6-E1055-CON and RWB-P6-E2022-CON.
- The gateway-bff composite route, the field list of the two channels and the masking at the edge (RWB-PLT-N001-CON), and the legacy screen SCR-33 Template approval, which the key names and which shows no offer.
- The decision code, the rule id, the `PORTAL` contact read (NEW-GAP-G6-3) and the refusal texts: the owners of the parameters, the reference data, the rwb-source-data contract and the message list.

### 20. Remaining delivery steps

- Size the story: delivery lead with the squad.
- Sign off the epic design (DOR-RWB-P6-E4035-CON-14): solution architect.
- Publish the baseline and its fakes and mark the contract Done: API contract owner of rwb-comms.
- Publish the rwb-source-data.yaml 5.1.0 fake of the contact-point read: rwb-source-data contract owner.
- Load the DEV test data of notice N-0401 and case RC-2026-000401: test data owner.
- Settle the PORTAL contact point and consent (NEW-GAP-G6-3) and the ledger entry of a view (NEW-GAP-F15-5): solution architect.

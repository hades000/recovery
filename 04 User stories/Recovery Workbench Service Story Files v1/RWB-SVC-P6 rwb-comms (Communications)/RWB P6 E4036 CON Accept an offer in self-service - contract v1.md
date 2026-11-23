# RWB-P6-E4036-CON Accept an offer in self-service

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4036-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-036 |
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

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-036 for rwb-comms (P6). The response of a notice is published on Day 1 on base `/api/recovery/comms/v1` with the two notice-side response operations, the `ResponseRequest` and `Response` schemas, the `notice_response` row of `rwb_comms`, the `Idempotency-Key` rule, the error set, the decision-record element, the two consumed events, the three consumed shapes of rwb-treatment, rwb-case and rwb-source-data, the fakes and the drift test; the two legacy criteria stay with RWB-P6-E4036-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-comms (P6)**, I want **the published contract of a customer's response to a notice — the base `/api/recovery/comms/v1` with `POST` and `GET /notices/{noticeId}/responses`, the `ResponseRequest` and `Response` schemas, the `notice_response` row of `rwb_comms`, the channel and response-code lists, the `Idempotency-Key` rule, the error set, the decision-record element, the two consumed events and the three consumed shapes of the owners, the fakes and the drift test** instead of the monolith's in-process call that kept `notice`, `treatment` and the case in one schema, so that **RWB-P6-E4036-APP and the sibling P6 stories build against one frozen, testable shape from Day 1, and an element, a status code, a decision element or an event name can never drift between rwb-comms, rwb-treatment, rwb-case, rwb-source-data and the decision library without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 addition of the response resource on the notice: the two operations, their request and answer bodies, their rights and their error set;
- the `ResponseRequest` and `Response` schemas and the list that validates the channel and the response code;
- the `notice_response` row of `rwb_comms`, its columns, its nullability and its index, and the declaration that no offer, case or consent row exists in this schema;
- the `Idempotency-Key` rule on the write, the additive rule and the versioning rule;
- the decision-record element of a response (DP-03) and the consumed shapes of rwb-treatment, rwb-case, rwb-source-data and the two events;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the response. The conduct check, the eligibility check, the decision write, the row write and the hand-on call are `RWB-P6-E4036-APP`'s; the offer is rwb-treatment's; the case and the acceptance recorded on it are rwb-case's; the party and its consent are rwb-source-data's. The document declares shapes and answers nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the legacy key has no operation of its own: the legacy endpoint block of RWB-E4-036 copies the two notice operations of the module (API-P6-001 Litigation C and API-P6-002 Litigation R), and the customer's answer was never an operation at all. In the target the offer is S2's, the case is P3's and the party is P1's, so the one surface that has to be fixed before code is written is the notice-side answer that carries the customer's response and its decision record.

Three facts make this a baseline and not a summary. The endpoint inventory of TSD P6 holds eleven operations (API-P6-001 to API-P6-011) and none of them is a response operation, and TSD P6 T3.1 holds `notice`, `template`, `merge_field` and `signature_request` and no response table, so the two operations, the schemas and the element rows are this story's own decision and are marked as such (GAP-1106; ASM-2054; GAP-1107; ASM-2055). The legacy permission check names Litigation C and Litigation R, which is the module template's copy for the notice operations and not the right of a customer-facing answer, so the capability area and the right of the two new operations are declared here with scope applied (GAP-1108; ASM-2056). And no source gives the decision code of a response or a member list for the response codes, so the element is fixed and its values are the reference data's (GAP-1110; ASM-2058).

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with its retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. The three events the catalogue gives this service (EV-13 `NoticeGenerated`, EV-14 `NoticeDispatched`, EV-15 `NoticeDelivered`, TSD P6 T5.3) are the notice events of other stories; this document publishes none of them and declares no response event, because the catalogue has none (Architecture v5 slide 42).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule and not a local choice.
- The platform problem envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline; where this document narrows them it does so explicitly.
- The notice contract RWB-P6-E1052-CON and the template and merge-field catalogue RWB-P6-AD017-CON are published, so `notice` with its `case_id`, `party_id`, `template_id` and its state has one owner document that this addition extends (TSD P6 T3.1, DF-LEG-015 to DF-LEG-034).
- The decision-record library contract RWB-PLT-E1027-CON is the writer, the chain and the outbox of the record this document names (DP-03); its shape is not fixed here.
- The owner rows are taken from the Ownership Map only: `treatment` is S2 rwb-treatment's, `recovery_case` is P3 rwb-case's, `contact_point_ext` and `party_ext` are P1 rwb-source-data's and the decision ledger is P7 rwb-decision's.
- The three consumed shapes are the rows RWB-P6-E4036-APP calls: the offer read `GET /treatments/{treatmentId}` (Ownership Map, S2), the acceptance record of the case on the rwb-case contract, and the contact point and consent read on the rwb-source-data contract (DP-05). No contract story of those owners is named in this story's Contract dependencies, so each row is declared as consumed and faked and its path stands as the placeholder (GAP-1109; ASM-2057).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the addition to the rwb-comms OpenAPI 3.1 document: the response resource under the notice, the two operations, the request and answer bodies and the error set.
2. Fix the answer elements and the request elements of section 11, with the placeholder where no source names a field name, a type or a required flag.
3. Fix the channel and response-code treatment: `channel` is a LOV-CHANNEL code (TSD P6 T3.2) and `responseCode` is a reference-data code whose list is not given, so it is declared as a reference to the list and never as a member list in the document.
4. Declare the `notice_response` row of `rwb_comms`, its columns, its nullability and its index, and the absence of any offer, case, party or consent column in this schema (DP-01).
5. Write the decision-record element of a response and the consumed shapes: the offer read, the acceptance record of the case, the contact point read of the party and the two events.
6. Write the `Idempotency-Key` rule on the write, the additive rule and the compatibility rule, and the one-response-per-notice rule.
7. Generate the fake set from the document, wire the drift test into the build of this story and of `RWB-P6-E4036-APP`, and write the absence tests.
8. Publish v1, record the pinned version of the consuming story, and hand the baseline to the app story, to the sibling P6 stories that read the notice and to the treatment, case, source-data and library owners.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | An element is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A response fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | An element, its type or its required flag has no value in the sources | The row carries the placeholder and the fake is derived from the published document | None | AC2 |
| X5 | An event of this service, or an event on another service's topic, is declared | The absence test fails the build; nothing is published | None | AC3 |
| X6 | The document declares an offer, case, party or consent table, a query on another service's schema or a `v_ace_*` view | The absence test fails the build | None | AC6 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the row is described as consumed and faked | None | AC4 |
| X8 | A response code, a decision code or a rule version is written as a member list or a constant | The review fails the baseline; the element names the reference data instead | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the notice contract it extends, the Ownership Map rows and the decision library only |
| Negotiable | The two paths, the element types and the required flags are settled at the baseline review; the base, the topic, the queue and the naming are fixed by the target architecture |
| Valuable | Unblocks the app story on Day 1 and the treatment, case, source-data and library owners on the same day, and makes a silent element drift impossible |
| Estimable | One additive document change, two schemas, one table definition, one decision element, three consumed shapes and two consumed events, five fakes and ten tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of a customer's response to a notice

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the notice contract RWB-P6-E1052-CON is published with the notice resource, its case reference DF-LEG-016 and its party reference DF-LEG-030

  Scenario: AC1 The two response operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /notices/{noticeId}/responses answering 201 with Response and GET /notices/{noticeId}/responses answering 200 with the Response list, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the POST declares the Idempotency-Key header and a stored answer, and the GET declares no Idempotency-Key
    Then both operations declare the capability area Litigation with right C on the POST and right R on the GET, scope applied, a 2 s budget, and the refusals 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition
    Then the document marks both operations as new, because the eleven operations of the TSD P6 inventory API-P6-001 to API-P6-011 hold none for a response and the legacy key copies only the two notice operations (GAP-1106; ASM-2054)
    Then every added property is additive within major version 1, so a consumer of the notice resource keeps working
    Then the document declares no second base, no second resource and no operation of another service

  Scenario: AC2 The element set, the request and the notice_response row are fixed (new, D-RCV-60)
    Given the element set and the row of the baseline
    When they are compared with the legacy data table of RWB-E4-036 and with the notice row of TSD P6 T3.1
    Then Response carries id, noticeId, caseId, responseCode, channel, respondedAt and decisionRecordId
    Then ResponseRequest requires responseCode, channel and respondedAt, noticeId comes from the path and id from the service, and no element is a name, a contact value or free text of a person
    Then noticeId and caseId are uuid, as DF-LEG-015 and DF-LEG-016 give them, channel is a LOV-CHANNEL code of varchar(15) as TSD P6 T3.2 gives it, and the type and width of responseCode, respondedAt and decisionRecordId are Not specified in the source documents (GAP-1107; ASM-2055)
    Then notice_response is declared as a new table of rwb_comms with id, notice_id, case_id, response_code, channel, responded_at, decision_record_id and the standard columns of TSD P6 T3.0, its field ids standing as Not specified in the source documents (GAP-1107; ASM-2055)
    Then the document declares the index on notice_id, one row per notice and no column of an offer, a case, a party or a consent in rwb_comms, and no foreign key across a service boundary (DP-01)

  Scenario: AC3 The decision-record element and the event rows are declared and no event is invented (new, D-RCV-60)
    Given the decision and event sections of the baseline
    When they are compared with DP-03, the shared topic and the event catalogue rows 05, 08, 10, 13, 14 and 15
    Then the element carries the case, the notice, the party, the response code, the channel, the responded at, the decision code, the rule id, the rule version, the final call and the decided-at, and it is the local library's element on rwb.decision-record.v1 (DP-03)
    Then the record is written before the change, and a response whose record cannot be written is not recorded and no hand-on call is made
    Then the decision code, the response-code list and the rule version's source are declared as reference data read with the version in force and are Not specified in the source documents (GAP-1110; ASM-2058)
    Then the only published row is rwb.decision-record.DecisionRecorded.v1 (EV-08), owned by P7 and written by the library, and the document declares no event of its own
    Then the document declares no response event, and the three catalogue events EV-13, EV-14 and EV-15 (NoticeGenerated, NoticeDispatched and NoticeDelivered) are named as the notice stories' and never as this document's
    Then no payload carries a name, an address, an identity number, an account number or a contact value, and every payload validates with BACKWARD compatibility

  Scenario: AC4 The consumed shapes and events are declared with their call type and their owner (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are reviewed against the Ownership Map and the connection matrix of Architecture v5 slide 17
    Then the offer read GET /treatments/{treatmentId} of S2 rwb-treatment and the contact point and consent read of P1 rwb-source-data are declared as consumed rows, each one hop with a 2 s timeout and a breaker, and each faked
    Then the acceptance record of the case on the rwb-case contract is declared as a consumed row of P3 rwb-case and its path stands as the placeholder (GAP-1109; ASM-2057)
    Then no C dependency row is declared for any of the three, because the plan names no contract story of those owners for this key (GAP-1109; ASM-2057)
    Then rwb.treatment.TreatmentApproved.v1 (EV-10) on rwb.treatment.events.v1, owned by S2, and rwb.case.CaseStateChanged.v1 (EV-05) on rwb.case.events.v1, owned by P3 and keyed by caseId, are declared as consumed inside this service with their inbox dedupe
    Then the document declares no operation of another service as provided, no subscription on another service's topic as its own and no file row

  Scenario: AC5 The fakes answer the document and the drift test binds them (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation, the event or the element it serves
    Then the response fake answers the 201, the 200 list and the empty list, the repeated Idempotency-Key, the second distinct response and every refusal of AC1
    Then the treatment fake answers an approved offer inside its validity, an offer outside it and an answer delayed beyond 2 s
    Then the case fake answers the acceptance recorded with its reference, a closed case, a legal hold, a duplicated event for the inbox and a hand-on call failing with 5xx
    Then the source-data fake answers a verified contact point with consent given, a withdrawn consent, no contact point on the channel and a delayed answer
    Then the decision-record library stub answers a healthy chain and outbox, and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The nine contract tables, the naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the contract section of this story
    When its nine sub-tables are reviewed against the Template and Rules and the Ownership Map
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty and a reason beside it
    Then the tables named as owned are notice, notice_response and template of rwb_comms with the library objects applied in that schema, and treatment of S2, recovery_case of P3, contact_point_ext and party_ext of P1, decision_log_entry and rule_row of P7, deviation of S8 and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the schema is rwb_comms, the base is /api/recovery/comms/v1, the topic is rwb.comms.events.v1 with retry and .dlt topics, the event names are rwb.comms.<Event>.v1, the task queue is rwb-comms in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.comms
    Then no offer, case, party or consent table, no cross-schema key and no query of this service on another owner's schema or on a v_ace_* view is declared, and the absence test fails a build that adds one
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then no workflow, no Schedule and no file element is declared, and the document says why
```

These six criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story and they restate no business outcome of RWB-P6-E4036-APP, which owns AC1 and AC2 of RWB-E4-036.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no `Idempotency-Key`; a write declares it and stores its answer | Architecture v5 slide 11; TSD P6 T6.2 |
| BR4 | Error responses use one envelope and one message ID per condition; a text the sources do not give carries the placeholder | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | `notice_response` is the only row this key adds; `treatment`, `recovery_case`, `contact_point_ext`, `party_ext` and `deviation` are other owners' and no foreign key crosses a service boundary | DP-01; Ownership Map |
| BR8 | The decision record of a response is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR9 | No business value is fixed in the contract: the eligible notice states, the response-code list, the channel list, the decision code and the rule ids stay data or reference data read with the version in force | FSD P6 A2.15 BR-P6-015; Template and Rules §R7.2 s17 |
| BR10 | No element of the schema or the row carries a name, an address, an identity number, an account number or a contact value; `channel` is a list code and the contact value stays behind the rwb-source-data contract | Template and Rules §R7.2 s17; TSD P6 T6.2 |
| BR11 | The three consumed shapes are declared as consumed and faked, and the C row is added when a contract story of their owner is planned | Ownership Map; Template and Rules §R5.4 |
| BR12 | One notice carries one response, so the write is idempotent by key and refuses a second distinct response | Template and Rules §R7.2 s17; GAP-1111 |
| BR13 | A response whose decision record cannot be written is not recorded, and the case is never told of an acceptance that has no record | Business Rules and Routing Logic v4 R-UNI-39; legacy RWB-E4-036 AC2 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element set, the row, the decision element and the consumed rows are described | In review |
| In review | Consumer sign-off | `RWB-P6-E4036-APP` and the treatment, case, source-data and library owners accept the document and the fakes | Baselined |
| Baselined | Additive change | An element or a column is added within major version 1, for example a type once its owner names it | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, a path changes or a refusal status changes | New major version drafted |
| Baselined | Drift in a fake | The drift test fails | In review |
| Baselined | Another owner's table or a cross-schema read is declared | The absence test of AC6 fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| `response.channel` | `MOBILE`, `HOME_PHONE`, `WORK_PHONE`, `LINE`, `EMAIL`, `POSTAL_ADDRESS`, `CALL`, `VISIT`, `SMS`, `LETTER`, `PORTAL`, `BRANCH` (LOV-CHANNEL, TSD P6 T3.2) | Declared as the list reference of the field; which code represents the HOME.SCB channel is Not specified in the source documents (GAP-1111; ASM-2059) |
| `notice.delivery_status` | `DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING` (LOV-DELIVERY, TSD P6 T3.2) | Declared as the list reference of the notice; a response changes none of them |

The notice state machine and the offer clock are `RWB-P6-E4036-APP`'s and their owners'; this document fixes the surface and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (`RWB-P6-E4036-APP`, the sibling P6 stories that read the notice, and the rwb-treatment, rwb-case, rwb-source-data and P7 library owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the CloudEvents envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element is declared in the response, in an answer or in a fake |
| Business analyst of P6 | Confirms that the eligible states, the response codes, the decision code and the rule ids are named as reference data and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_comms` by the naming rule of DP-02; the document names the scheme and not a credential. The rights of the two operations are declared here, their role lists are rwb-access data, and no role code is written in the document.

### 11. Data

The contract baseline declares shapes, not business values.

| Element | Legacy field or source | Type and width | Required | List |
|---|---|---|---|---|
| responseId | the identifier of the row TSD P6 T3.1 does not hold; its field is Not specified in the source documents (GAP-1107; ASM-2055) | uuid | Yes | None |
| noticeId | DF-LEG-015 of the notice | uuid | Yes | None |
| caseId | DF-LEG-016 of the notice | uuid | Yes | None |
| responseCode | none; the response codes of the reference data | Not specified in the source documents (GAP-1110; ASM-2058) | Yes | The response-code list, read as reference data |
| channel | the channel the answer arrives on, as LOV-CHANNEL | varchar(15) | Yes | LOV-CHANNEL |
| respondedAt | none; the instant the customer answered | Not specified in the source documents (GAP-1107; ASM-2055) | Yes | None |
| decisionRecordId | the local decision record of DP-03 | Not specified in the source documents (GAP-1110; ASM-2058) | Yes | None |
| Standard columns | state, version, created_at, created_by, updated_at, updated_by, is_active of TSD P6 T3.0 | varchar(40), integer, timestamptz, uuid, timestamptz, uuid, boolean | n/a | None |

| Item | Content |
|---|---|
| Request | `ResponseRequest` carries `responseCode`, `channel` and `respondedAt`, all required; `noticeId` comes from the path and `responseId` from the service |
| Answer | 201 with `Response` and 200 with the `Response` list, newest first, each carrying the notice reference and the decision record reference |
| Forbidden element | No name, address, identity number, account number or contact value in any element (BR10) |
| Decision record | The library's element: the case, the notice, the party, the response code, the channel, the responded at, the decision code, the rule id and version, the final call and the decided at (DP-03) |
| Idempotency | The `Idempotency-Key` header on the POST, its stored answer and its 24-hour window; one response per notice (BR12) |

**The one new table of this key.** `notice_response` is declared here and created by RWB-P6-E4036-APP's Flyway step in `rwb_comms` (DP-15):

| Column | Type and width | Required | Source |
|---|---|---|---|
| id | uuid | Yes | The row's own identifier; its DF field id is Not specified in the source documents (GAP-1107; ASM-2055) |
| notice_id | uuid | Yes | The notice the customer answered, DF-LEG-015 |
| case_id | uuid | Yes | The case of the notice, DF-LEG-016 |
| response_code | Not specified in the source documents (GAP-1110; ASM-2058) | Yes | The response-code list of the reference data |
| channel | varchar(15) | Yes | LOV-CHANNEL |
| responded_at | Not specified in the source documents (GAP-1107; ASM-2055) | Yes | The instant the customer answered |
| decision_record_id | Not specified in the source documents (GAP-1110; ASM-2058) | Yes | The local decision record of DP-03 |
| state, version, is_active, created_at, created_by, updated_at, updated_by | varchar(40), integer, boolean, timestamptz, uuid, timestamptz, uuid | n/a | The standard record columns, TSD P6 T3.0 |

`notice`, `template` and `merge_field` are the P6 rows of TSD P6 T3.1 and this document adds one table and no column to them; `decision_record`, `idempotency_key`, `outbox_event` and `processed_event` are platform library objects created in `rwb_comms` by the library's migration and are named here, not declared. `treatment`, `recovery_case`, `contact_point_ext`, `party_ext`, `decision_log_entry`, `rule_row`, `deviation` and every `v_ace_*` view are other owners' and appear only as consumed shapes. `notice.case_id` and `notice.party_id` are identifiers, not foreign keys across schemas (DP-01).

**No personal data.** No element and no column of this contract carries a name, an address, an identity number, an account number or a contact value. The notice, the case and the party are reached by identifiers, `channel` is a list code, and the contact value itself never leaves rwb-source-data.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Both operations are new: no response operation is in the endpoint inventory of the TSD (GAP-1106; ASM-2054).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| new | POST | `/notices/{noticeId}/responses` | `ResponseRequest`; `noticeId` from the path | 201 with `Response` | Litigation C, scope applied | `Idempotency-Key` required, answer stored | 401, 403, 404, 409, 422, 503 |
| new | GET | `/notices/{noticeId}/responses` | None | 200 with the `Response` list, newest first | Litigation R, scope applied | Not applicable | 401, 403, 404, 503 |

The purpose, the shapes and the refusals are this baseline's own, because no TSD P6 T-A.1 row names a response; the base and the naming are DP-13's and DP-14's. The two notice operations of the module, API-P6-001 (Litigation C) and API-P6-002 (Litigation R), are `RWB-P6-E1052-CON`'s and are not redeclared here. The capability area and the rights are declared from TSD P6 T6.1, where the Litigation area is the area of the notice operations the legacy key copies and the customer holds no role code of its own (GAP-1108; ASM-2056).

#### 12.2 REST operations consumed

None declared as an operation of this document; the three rows below are the consumed shapes the app story calls, each one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020).

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The offer read `GET /treatments/{treatmentId}` (Ownership Map) | S2 rwb-treatment | The answer elements the eligibility check needs: the offer of the case, its route set and its validity | Consumed and faked; no C row, because no contract story of S2 is named (GAP-1109; ASM-2057) |
| The acceptance record of the case on the rwb-case contract | P3 rwb-case | The request (the case, the notice, the party, the response code and the responded at) and the answer that carries the case reference and the stage the case moved to | Consumed and faked; the path is Not specified in the source documents (GAP-1109; ASM-2057) |
| The contact point and consent read of a party on a channel (DP-05) | P1 rwb-source-data | The answer elements the conduct check needs: the contact point of the party on the channel, its consent state and its verified flag | Consumed and faked; the path is Not specified in the source documents (GAP-1109; ASM-2057) |

No row reads a table, no row reads a `v_ace_*` view, and no row is declared as a provided operation of this service (BR6, BR7).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, rule id, rule version, case, notice, party, response code, channel, responded at, decided at; written by the local decision-record library (DP-03) |

This document declares the element and publishes nothing itself. No response event is declared: the catalogue of Architecture v5 slide 42 holds none, and EV-13, EV-14 and EV-15 are the notice events of `RWB-P6-E1052-CON` and the dispatch stories.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | caseId, the treatment and the approved-at, consumed inside rwb-comms so a response is taken only when the offer is released, with the inbox dedupe (GAP-1109; ASM-2057) |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | caseId, the from and to states and the changed-at, consumed inside rwb-comms so a response on a closed case or under legal hold is refused, with the inbox dedupe (GAP-1109; ASM-2057) |

Both rows are consumed by `RWB-P6-E4036-APP`; this baseline fixes their names, their topics and their keys (`caseId`) and declares no subscription of its own.

#### 12.5 Workflows and activities

None. A response is one synchronous write with one library write, three owner calls and one hand-on call; this document declares no workflow, no child workflow and no activity, and `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is declared: JOB-10 of the catalogue is the daily WIN dispatch of `RWB-P6-E2021-CON` (Architecture v5 slide 44), and no job row is read or changed by this document.

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| notice | `rwb_comms` | P6 | The notice the customer answered: its `case_id`, `party_id`, `template_id`, `sent_date` and its state |
| notice_response | `rwb_comms` | P6 | The response row of section 11: its notice, its case, its response code, its channel, the responded at and its decision record reference |
| template | `rwb_comms` | P6 | Read for the notice reference only; written by the template stories |
| decision_record, idempotency_key, outbox_event, processed_event | `rwb_comms` | PLT library objects applied in this schema | The decision entry of a response, the stored answer of the POST, the envelope of the published row and the inbox of the consumed rows (DP-03) |

`treatment` and `dp_treatment` are S2's; `recovery_case`, `task`, `timer` and `queue` are P3's; `contact_point_ext`, `party_ext` and `interaction` are P1's; `decision_log_entry`, `rule_row` and the rule package rows are P7's; `document` and `signature_request` are P5's; `deviation` is S8's; `outbound_item` and `interface_config` are P2's. They are named as consumed answers only, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Response fake | The two operations of 12.1 | A 201 create with the `Response`, a 200 list, an empty list, the repeated `Idempotency-Key` returning the first answer, a second distinct response and the 400, 401, 403, 404, 409, 422 and 503 refusals |
| Treatment fake | The offer row of 12.2 and EV-10 | An approved offer inside its validity, an offer outside it, an offer not yet approved, an answer delayed beyond 2 s and a duplicated event for the inbox |
| Case fake | The acceptance row of 12.2 and EV-05 | The acceptance recorded with its reference, a closed case, a legal hold, a hand-on call failing with 5xx and a duplicated event for the inbox |
| Source-data fake | The contact point and consent row of 12.2 | A verified contact point with consent given, a withdrawn consent, no contact point on the channel and a delayed answer |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Drift test | Every fake against the document | A drifted fake fails the build |

The treatment, case and source-data fakes are stubbed from the owners' published documents and carry the placeholder where the source is silent (GAP-1109; ASM-2057).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The response record and the response list provided; the offer read, the acceptance record of the case and the contact point read consumed; one hop, 2 s |
| Kafka | 1 declared as written by its owner, 2 consumed | `DecisionRecorded` through the library; `TreatmentApproved` and `CaseStateChanged`; no response event |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the addition to `openapi/rwb-comms-v1.yaml` for the response resource, the `ResponseRequest` and `Response` schemas in `th.co.scb.ace.workbench.recovery.comms.api`, the `notice_response` column note, the decision-record fragment, the fake set and the drift test. The implementation behind it is `RWB-P6-E4036-APP`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming app story carries the H row |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; the party and its consent are a consumed shape and no `v_ace_customer` read is declared | none; referred to by the consuming app story |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the response answer is reached through it and the contract declares no composite route | referred to; the consuming app story and the platform edge story carry the H row |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-05 is the pattern that keeps the party and its consent out of this schema and out of a view. DP-01 and DP-15 stand behind the boundary and the `notice_response` table as rules and add no dependency. DP-19 is the route the channel and the case record use and is `RWB-PLT-N001-CON`'s. This story being a CON story, it holds no build dependency by rule (Template and Rules §R5.7 rule 1).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ResponseOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR6) |
| ResponseSchema | Published schema | `ResponseRequest` and `Response` with their elements, the required set and the forbidden elements (BR9, BR10) |
| NoticeResponseTable | Resource | The `notice_response` columns, their nullability, the index on `notice_id` and the absence of an offer, case, party or consent column (BR7, BR12) |
| DecisionElement | Document | The decision-record element of a response on the shared topic (BR8) |
| ConsumedShapes | Document | The offer read, the acceptance record, the contact point read and the two events, with their placeholders (BR6, BR11) |
| ProblemEnvelope | Reused schema | The platform problem document with its `messageId` extension (BR4) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer, its window and the one-response-per-notice rule (BR3, BR12) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers of every consuming build (AC5) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC5, AC6) |

**Database.** One new table of `rwb_comms`, applied by the service's own Flyway sequence and never editing an applied migration (DP-15); its field ids are the placeholder of section 11. No column of `notice`, `template` or `merge_field` is added, no table of another owner is created, and no other schema is named in the note.

**Configuration and reference data.** The eligible notice states, the response-code list, the channel list, the decision code and the rule ids are reference data or parameters read with the version in force (BR9). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Add the response resource and the two operations to the document and lint the paths, the rights and the additive rule (AC1).
2. Write the two schemas with their elements, the required set, the forbidden elements and an example; validate the example (AC2).
3. Write the `notice_response` definition, the index and the absence tests for another owner's table and a cross-schema read (AC2, AC6).
4. Write the error section with one message ID per condition and the `Idempotency-Key` rule and the one-response-per-notice rule of the write (AC1).
5. Write the decision element and the three consumed documents' identities and the two events with their placeholders (AC3, AC4).
6. Generate the fake set and the drift test and wire the drift test into the build of `RWB-P6-E4036-APP` (AC5).
7. Write the naming and boundary section and the absence tests for the old base, a response event and a second topic (AC6).
8. Publish v1 and record the pinned version of this contract and of the consuming story.

**Feature flag.** `rwb.comms.notice-response-contract`.

**Done when.** The document lints, the two schemas validate, the `notice_response` definition applies twice, the fakes answer every status including the repeated key and the second distinct response, the absence tests are green and `RWB-P6-E4036-APP` has accepted the baseline.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written by the consuming story (X8, legacy AC2) | 503, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required property is missing or invalid | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| MSG-P6-001 | An open contact stop is in force on the case, raised by the consuming story | 409, problem body with `messageId` MSG-P6-001 | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | The message is for a channel without consent, raised by the consuming story | 409, problem body with `messageId` MSG-P6-002 | The customer has not consented to {channel}. Use another channel. |
| Not specified in the source documents (GAP-1106; ASM-2054) | The notice is outside the eligible states, or it is already answered | A 409 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |
| Not specified in the source documents (GAP-1111; ASM-2059) | The offer has left the customer, the offer expired, or the case is under a legal hold | A 409 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |

MSG-P6-001, MSG-P6-002, MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the five messages of the legacy validation table that this surface raises and are copied unchanged. MSG-P6-003 of that table belongs to the withdrawn template of the dispatch path and is declared by the dispatch story, not here. No text is invented.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template with its Draft, approved and withdrawn states, so it cannot show a self-service answer; the P6 screen list of the FSD holds no response screen. The customer's surface is the channel itself, LINE OA and HOME.SCB (FSD P6 A2.15.2), reached through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the response and once for the response list and merges the answers. No screen identifier for a response surface is given by any source (GAP-1111; ASM-2059).

| Surface | State | What this contract serves |
|---|---|---|
| The notice of the offer | Sent, no response | The notice reference and an empty response list |
| The notice of the offer | Answered with an acceptance | The notice reference and one `Response` with its code, channel, responded at and decision record |
| The notice of the offer | Answered with a decline | The notice reference and the `Response` with its decline code and its decision record |
| The notice of the offer | Refused | The 403 with MSG-P4-002, the 409 with MSG-P6-001 or MSG-P6-002, and the 409 with the placeholder of section 14 |

The route, the merge order, the field list of the surface and the masking belong to `RWB-PLT-N001-CON`; the transitions behind each state are the app story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-036-01 | AC1 | Contract | Notice `N-0101` of case `RC-2026-000321`; the contract half answers the 201 `Response`, the 200 list, the empty list and the rule version of the decision element. Legacy test: Accept an offer in self-service |
| TC-E4-036-02 | AC2 | Contract | Decision log stubbed unavailable; the contract half answers the stopped chain and the 503 of MSG-P7-003. Legacy test: Not recorded |
| TC-E4-036-03 | Access | Contract | A role without the right sends the POST and the GET; the contract half answers the 403 of MSG-P4-002 and the 404 of a notice outside the scope. Legacy test: A role without the right is refused with MSG-P4-002 |
| TC-E4-036-04 | Principle 5 | Contract | The stopped chain of the library stub on 10 responses; the contract half answers the same 503 and the drift test. Legacy test: A forced decision log write failure stops the action with MSG-P7-003 |
| TC-P6-E4036-CON-01 | AC1 | Contract | The document validates; the two operations, the rights, the `Idempotency-Key` rule, the two new markers and the six refusals are present |
| TC-P6-E4036-CON-02 | AC2 | Contract | The seven answer elements, the three request elements, the placeholders, the forbidden elements and the `notice_response` columns are present; no other owner's table is declared |
| TC-P6-E4036-CON-03 | AC3 | Contract | The decision element, the reference-data placeholders and the single published row are present; no response event and no second topic |
| TC-P6-E4036-CON-04 | AC4 | Contract | The three consumed rows with their owner and their one-hop rule, and the two consumed events with their key; no provided operation of another service and no C row |
| TC-P6-E4036-CON-05 | AC5 | Component | The response, treatment, case and source-data fakes and the library stub match the document; a drifted fake fails the build |
| TC-P6-E4036-CON-06 | AC6 | Contract | The nine sub-tables with their owners, the naming baseline and the absence tests for another owner's table, a cross-schema query and a `v_ace_*` view |

The four legacy identifiers keep their legacy order, their legacy coverage and their legacy intent, and carry the level of the surface they prove here, which is the contract: the legacy table has no level column, and the end-to-end proof of the same cases is RWB-P6-E4036-APP's. The six `TC-P6-E4036-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the eligible states, the response codes, the channel list, the decision code and the rule ids stay data or reference data read with the version in force.
- No personal data in a schema, an example or a fake: identifiers, a channel code, a response code, a rule id, a rule version and dates only; the contact value stays behind the rwb-source-data contract.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the offer read, the acceptance record and the contact point read are consumed and faked, never declared as provided (DP-01, DP-05).
- No other owner's table and no cross-schema read: the absence test of AC6 fails a build that declares `treatment`, `recovery_case`, `contact_point_ext`, a query on another schema or a `v_ace_*` view.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is invented and none of the three catalogue events of this service is claimed: the only published element is the library's `DecisionRecorded` (DP-03).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the types of `responseCode`, `respondedAt` and `decisionRecordId`, the `notice_response` field ids, the response-code list, the decision code and the refusal texts.
- Every example in the document is synthetic; no production payload, identifier or file is copied into a schema or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-036 |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4036-APP; this baseline copies neither |
| Legacy test cases | TC-E4-036-01 to TC-E4-036-04, as the contract half of each case |
| New contract cases | TC-P6-E4036-CON-01 to TC-P6-E4036-CON-06 |
| Legacy feature | FEAT-COM-02 Accept an offer in self-service (FSD P6 A2.15), prerequisite FEAT-COM-01 of the same module |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-034; template DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069; treatment DF-TRT-001 to DF-TRT-014; recovery_case DF-CAS-001 to DF-CAS-023; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015 |
| Legacy rules | VR-P6-015-1, VR-P6-015-2, BR-P6-015 |
| Rules | R-RES-16 (the accepted answer and its record), R-RES-17 (the declined answer), R-RES-19 (a contact stop holds the offer channel), R-UNI-20 (a legal hold stops the answer) |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 and DP-15 applied as rules, DP-11 in the consumed rows) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-019 (edge: gateway-bff and partner gateway), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Requirements | REQ-OCC-011 (customer self-service for an offer, a signature, a payment and a dispute on the bank's digital channels, Should, E4), served for the offer by the app story against this baseline |
| Contract and tests | This document and TC-P6-E4036-CON-01 to TC-P6-E4036-CON-06 |

### 19. Out of scope

- The implementation of the two operations, the conduct check, the eligibility check, the decision write, the row write and the hand-on call (RWB-P6-E4036-APP).
- The offer, its route set and its validity: S2 rwb-treatment, `treatment` and `GET /treatments/{treatmentId}`, with the stories that build the treatment side.
- The case, its stage and the acceptance recorded on it: P3 rwb-case, `recovery_case` and the case contract.
- The party, its contact point, its consent and its verified flag: P1 rwb-source-data, reached through its contract and never through `v_ace_customer` (DP-05).
- The contact stop and the deviation codes: S8 rwb-deviation.
- The decision-record library, its chain and its outbox (RWB-PLT-E1027-CON and the RWB-PLT-LIB stories); this baseline names the element and writes none of it.
- The e-signature and the paper signature where Legal requires wet ink: RWB-P6-E2018-CON and the document hub (P5 `signature_request`).
- The generation and dispatch of the notice, JOB-10, the WIN file and `NoticeDispatchWorkflow` (RWB-P6-E1052-CON and RWB-P6-E2021-CON).
- The template and merge-field administration and the legacy screen SCR-33 (RWB-P6-E1046-CON and RWB-P6-AD017-CON).
- The gateway-bff composite route, the field list of the response surface and the masking at the edge (RWB-PLT-N001-CON).
- The decision code, the response-code list, the eligible states and the refusal texts: the owners of the reference data and of the message list.

# RWB-P6-E4039-CON Maintain the contact repository

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4039-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-039 |
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

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-039 for rwb-comms (P6). The contact repository is published on Day 1 on base `/api/recovery/comms/v1` with the contact-point read and the consent and verification write, the `ContactPoint` element set with its placeholders, the decision-record element, the consumed rwb-source-data rows, the consumed contact-stop events, the fakes and the drift test; the two legacy criteria stay with RWB-P6-E4039-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of rwb-comms (P6)**, I want **the published contract of the contact repository — the base `/api/recovery/comms/v1` with `GET /parties/{partyId}/contact-points` and `PUT /contact-points/{contactKey}`, the `ContactPoint` and `ContactPointRequest` elements with their placeholders, the `If-Match` version rule, the error set, the decision-record element, the consumed rwb-source-data rows, the consumed contact-stop events, the fakes and the drift test** instead of the monolith's in-process access to `v_ace_contact` and `recovery.contact_point_ext`, so that **RWB-P6-E4039-APP and the dispatch stories build against one frozen, testable shape from Day 1, and an element, a status code, a right or an event name can never drift between rwb-comms, rwb-source-data and the decision library without a failing build**.

This story owns the contract and nothing else:

- the OpenAPI 3.1 addition of the contact resource: the two operations, their request and answer bodies, their rights and their error set;
- the `ContactPoint` element set, the `ContactPointRequest` set and the placeholders of the consent, verification and failed-count values and of the composite contact key;
- the `If-Match` version rule on the write, the additive rule and the versioning rule;
- the decision-record element of a consent change (DP-03) and the consumed shapes of rwb-source-data and of the two contact-stop events;
- the declaration that this service owns no contact table, no consent column and no `v_ace_*` query;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not build the repository. The read, the stop mark, the decision write, the owner call and the version answer are `RWB-P6-E4039-APP`'s; the contact value, the consent state, the verification and the failed count are rwb-source-data's; the contact stop is rwb-deviation's and rwb-case's. The document declares shapes and holds nothing.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11 as the call shape of DP-05, ADR-020), and the legacy key has no operation of its own: its endpoint block copies the two notice operations of the module, and the consent state was a column of a table in the same `recovery` schema as the notice. In the target the contact rows are P1's and the notice is P6's, so the one surface that has to be fixed before any code is written is the party-side answer that carries the consent state per channel and the version a change is written against.

Three facts make this a baseline and not a summary. The endpoint inventory of TSD P6 holds eleven operations (API-P6-001 to API-P6-011) and none of them is a contact operation, and TSD P6 T3.1 holds `notice`, `template`, `merge_field` and `signature_request` and no contact table, so the two operations and the element rows are this story's own decision and are marked as such (GAP-1120; ASM-2068). The FSD describes the data of the feature as `v_ace_contact` plus `recovery.contact_point_ext` "keyed by the composite contact key" (FSD P6 A2.18.2) while the Ownership Map gives both the ACE view contract and the four extension tables to P1, so the document may describe those rows only as consumed answers of the rwb-source-data contract and may not declare a table of its own (GAP-1118; ASM-2066). And no source gives a consent state value set, a verification rule or a failed-count threshold, so the element is fixed and its values are the reference data's, standing as placeholders (GAP-1121; ASM-2069).

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with its retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. The three events the catalogue gives this service (EV-13, EV-14 and EV-15, which TSD P6 T5.3 names `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`) are the notice events of other stories; this document publishes none of them and declares no contact event, because the catalogue has none.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule and not a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline; where this document narrows them it does so explicitly.
- The decision-record library contract RWB-PLT-E1027-CON is the writer, the chain and the outbox of the record this document names (DP-03); its shape is not fixed here.
- The owner rows are taken from the Ownership Map only: `contact_point_ext`, `party_ext`, `account_ext` and `valuation_ext` are P1 rwb-source-data's in `rwb_source_data`, the thirty `v_ace_*` views are the ACE view contract of P1, `recovery_case` and `case_party` are P3's, `deviation` is S8's and the decision ledger is P7's.
- The contact read and the consent write of the rwb-source-data contract are named as consumed and faked; no source names a published operation of that contract for either of them (GAP-1119; ASM-2067).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7 rule 1), and every consuming story of the service builds against it and its fake.

### 4. Flow

1. Draft the addition to the rwb-comms OpenAPI 3.1 document: the contact resource under the party, the two operations, the request and answer bodies and the error set.
2. Fix the `ContactPoint` elements from the legacy data rows DF-ACE-075 to DF-ACE-083 and DF-EXT-013 to DF-EXT-026, with the composite key, the consent and verification values and the physical types standing as the placeholders.
3. Fix the `If-Match` version rule on the write and the answer that carries the new version, and declare that a read carries no `Idempotency-Key`.
4. Declare that this service owns no contact table, no consent column and no `v_ace_*` query, and name the P1 rows as consumed answers only.
5. Write the decision-record element of a consent change and the consumed shapes: the contact read, the consent write and the two contact-stop events.
6. Write the error set with one message ID per condition, the additive rule and the compatibility rule.
7. Generate the fake set from the document, wire the drift test into the build of this story and of `RWB-P6-E4039-APP`, and write the absence tests.
8. Publish v1, record the pinned version of each consuming story, and hand the baseline to the app story, to the dispatch stories that read the answer and to the rwb-source-data and library owners.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | None | AC1 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | The composite contact key, a consent value or a physical type has no value in the sources | The row carries the placeholder and the fake is derived from the published document | None | AC2 |
| X5 | A contact event is declared, or an event is declared on another service's topic | The absence test fails the build; nothing is published | None | AC3 |
| X6 | The document declares a contact table, a consent column, a query on `rwb_source_data` or a `v_ace_*` view | The absence test fails the build | None | AC6 |
| X7 | The document declares another service's operation as provided | The review fails the baseline; the row is described as consumed and faked | None | AC4 |
| X8 | A consent state, a verification rule or a failed-count threshold is written as a value | The review fails the baseline; the element names the reference data instead | None | AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map rows, the decision library and the two event catalogue rows only |
| Negotiable | The two paths, the composite key and the physical types are settled at the baseline review; the base, the topic, the queue and the naming are fixed by the target architecture |
| Valuable | Unblocks the app story and the dispatch stories on Day 1, and makes a silent drift between rwb-comms and rwb-source-data impossible |
| Estimable | One additive document change, one element set, one decision element, three consumed shapes, four fakes and ten tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the contact repository

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the Ownership Map gives contact_point_ext, party_ext, account_ext and valuation_ext to P1 rwb-source-data

  Scenario: AC1 The two contact operations are declared on the service base (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /parties/{partyId}/contact-points answering 200 with the ContactPoint list and PUT /contact-points/{contactKey} answering 200 with ContactPoint, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the PUT declares the If-Match header with the version of the contact point, a repeated version returning the first answer, and the GET declares no Idempotency-Key
    Then both operations declare the capability area Documents with right R on the GET and right U on the PUT, scope applied, a 2 s budget, and the refusals 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition
    Then the document marks both operations as new, because the eleven operations of the TSD P6 inventory API-P6-001 to API-P6-011 hold none for a contact (GAP-1120; ASM-2068)
    Then every added property is additive within major version 1, so a consumer of the notice resource keeps working
    Then the document declares no second base, no second resource and no operation of another service

  Scenario: AC2 The contact element set is fixed and the contact row stays the owner's (new, D-RCV-60)
    Given the ContactPoint element set of the baseline
    When it is compared with the legacy data rows DF-ACE-075 to DF-ACE-083 and DF-EXT-013 to DF-EXT-026
    Then ContactPoint carries contactKey, partyId, contactType, consentState, consentAt, verifiedAt, failedCount, blockedByStop, stopReasonCode and version
    Then contactType is a LOV-CHANNEL code of TSD P6 T3.2 and the consent value set, the verification rule and the failed-count threshold are the placeholder (GAP-1121; ASM-2069)
    Then the composite contact key, the physical types and the eight fields of contact_point_ext that the legacy table does not name are Not specified in the source documents (GAP-1123; ASM-2071)
    Then no element carries a contact value, a masked contact value, a name, an address or an identity number, and ContactPointRequest requires contactType, consentState and version
    Then the document declares no contact table and no consent column in rwb_comms, and the contact row and the consent state are the owner's rows reached on its contract (DP-01)
    Then the document states that the consent state is written by rwb-source-data and never by this service

  Scenario: AC3 The decision-record element is declared and no event of this service is invented (new, D-RCV-60)
    Given the decision and event sections of the baseline
    When they are compared with DP-03, the shared topic and the event catalogue rows of this service
    Then the element carries the decision code, the rule id, the rule version, the party reference, the contact key, the channel, the state written, the final call and the decided-at, and it is the local library's element on rwb.decision-record.v1 (DP-03)
    Then the record is written before the change, and a change whose record cannot be written is not made
    Then the decision code, the rule id and the rule version are declared as reference data read with the version in force and are Not specified in the source documents (GAP-1121; ASM-2069)
    Then the only published row is rwb.decision-record.DecisionRecorded.v1 (EV-08), owned by P7 and written by the library, and the document declares no event of its own
    Then the document declares no contact event, and the three catalogue events EV-13, EV-14 and EV-15 (NoticeGenerated, NoticeDispatched and NoticeDelivered) are named as the notice stories' and never as this document's
    Then no payload carries a contact value, a name, an address or an identity number, and every payload validates with BACKWARD compatibility

  Scenario: AC4 The consumed shapes are declared with their call type and their owner (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are reviewed against the Ownership Map and the connection matrix of Architecture v5 slide 13
    Then the contact read and the consent and verification write of the rwb-source-data contract are declared as consumed rows of P1 rwb-source-data, each one hop with a 2 s timeout and a breaker, and each faked
    Then the paths and the element list of those two rows are carried as the placeholder, because no source names a published operation of that contract for them (GAP-1119; ASM-2067)
    Then no C dependency row is declared for them, because the plan names no P1 contract story for this key
    Then rwb.deviation.DeviationRaised.v1 (EV-06) and rwb.deviation.DeviationCleared.v1 (EV-07) on rwb.deviation.events.v1, owned by S8 and keyed by caseId, are declared as consumed inside this service for the contact stop, with their inbox dedupe (GAP-1123; ASM-2071)
    Then the document declares no operation of another service as provided, no subscription on another service's topic as its own and no file row

  Scenario: AC5 The fakes answer the document and the drift test binds them (new, D-RCV-60)
    Given the fake set generated from the document
    When each fake is compared with the operation, the event or the element it serves
    Then the contact fake answers the party read with three contact points, a withdrawn channel and an unverified channel, a party with no contact point, and a consent write with a stored state, a 5xx and an answer delayed beyond 2 s
    Then the version fake answers the version of the read and a version the owner moved on, for the 409
    Then the stop-event fake answers no stop, a stop in force, a lifted stop and a duplicated event for the inbox
    Then the decision-record library stub answers a healthy chain and outbox, and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The nine contract tables, the naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the contract section of this story
    When its nine sub-tables are reviewed against the Template and Rules and the Ownership Map
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty and a reason beside it
    Then the tables named as owned are contact_stop, the local decision record and the library objects of rwb_comms, and contact_point_ext, party_ext, v_ace_contact, v_ace_customer, recovery_case, case_party, deviation, decision_log_entry, rule_row and lov_value are named as other owners' and consumed only through their contracts
    Then the schema is rwb_comms, the base is /api/recovery/comms/v1, the topic is rwb.comms.events.v1 with retry and .dlt topics, the event names are rwb.comms.<Event>.v1, the task queue is rwb-comms in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.comms
    Then no contact table, no consent column, no contact-value column, no cross-schema key and no query of this service on rwb_source_data or on a v_ace_* view is declared, and the absence test fails a build that adds one
    Then the old monolith base appears nowhere in the document, its examples or its fakes
    Then no workflow, no Schedule and no file element is declared, and the document says why
```

These six criteria are new for the contract baseline and test the artefact only. They copy no criterion of the legacy story and they restate no business outcome of RWB-P6-E4039-APP, which owns AC1 and AC2 of RWB-E4-039.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | A read declares no `Idempotency-Key`; a write declares its version precondition and stores its answer | Architecture v5 slide 11; TSD P6 T6.2 |
| BR4 | Error responses use one envelope and one message ID per condition; a text the sources do not give carries the placeholder | Architecture v5 platform baseline; Template and Rules §R7.2 s14 |
| BR5 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR6 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR7 | The contact point, the consent state, the verification and the failed count are P1's; this service declares no contact table, no consent column and no cross-schema key | DP-01; Ownership Map (`contact_point_ext` owned by P1); FSD P6 A2.18.2 |
| BR8 | A CE contact value, its masked form, a name, an address and an identity number are forbidden in every field, example and fake of this document | Template and Rules §R7.2 s17; TSD P6 T6.2 |
| BR9 | The decision record of a consent change is the local library's entry on the shared topic, never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR10 | No business value is fixed in the contract: the consent state set, the verification rule, the failed-count threshold, the channel list and the decision code stay data or reference data read with the version in force | FSD P6 A2.18.3.1 (BR-P6-018); Template and Rules §R7.2 s17 |
| BR11 | The two contact-stop events are consumed rows of this service and the stop itself stays S8's and P3's fact | Architecture v5 slide 17 ("events DeviationRaised / Cleared (contact stop)"); slide 42 rows 06 and 07 |
| BR12 | The capability area and the right of the two operations come from TSD P6 T6.1 and never from the legacy Litigation right, because the primary role of the feature holds Documents RU and Litigation R only | TSD P6 T6.1; FSD P6 A2.18.3.3; GAP-1122; ASM-2070 |
| BR13 | The rwb-source-data rows are consumed and faked, and the C row is added when a P1 contract story is planned | Ownership Map; Template and Rules §R5.4 |

### 9. State transitions

The document's own lifecycle is the only state this story moves:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element set, the decision element and the consumed rows are described | In review |
| In review | Consumer sign-off | `RWB-P6-E4039-APP` and the rwb-source-data and library owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example the composite key once its owner names it | Baselined |
| Baselined | Breaking change | An element is removed, renamed or retyped, a path changes or a refusal status changes | New major version drafted |
| Baselined | Drift in a fake | The drift test fails | In review |
| Baselined | A contact table or a cross-schema read is declared | The absence test of AC6 fails | In review |

Two vocabularies are declared and neither is moved here:

| Object | Values | Note |
|---|---|---|
| contactType | `MOBILE`, `HOME_PHONE`, `WORK_PHONE`, `LINE`, `EMAIL`, `POSTAL_ADDRESS`, `CALL`, `VISIT`, `SMS`, `LETTER`, `PORTAL`, `BRANCH` (LOV-CHANNEL, TSD P6 T3.2) | Declared as the list reference; the owner validates the code on its own list |
| consentState | Not specified in the source documents (GAP-1121; ASM-2069) | Declared as the reference-data reference of the owner; no member list is curated here |

The consent and verification state of a contact point and the contact stop are `RWB-P6-E4039-APP`'s to apply and the owners' to hold. This document fixes the surface and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes |
| Consuming teams (RWB-P6-E4039-APP, the dispatch stories that read the answer, and the rwb-source-data and P7 library owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the problem envelope, the CloudEvents envelope, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data element — no contact value, masked value or identity number — is declared in an answer or in a fake |
| Business analyst of P6 | Confirms that the consent states, the verification rule, the failed-count threshold and the decision code are named as reference data and that no member list is curated locally |

The login name behind the document's security scheme is `rwb_comms` by the naming rule of DP-02; the document names the scheme and not a credential. The rights of the two operations are declared here, their role lists are rwb-access data, and no role code is written in the document. The legacy permission table gives the notice operations Litigation C and Litigation R, and the primary role of FEAT-COM-05 holds Documents RU and Litigation R, so the contact operations are declared as Documents R and U (GAP-1122; ASM-2070).

### 11. Data

The contract baseline declares shapes, not business values.

| Element | Legacy field | Type and width | Required | List |
|---|---|---|---|---|
| contactKey | contact_key of `v_ace_contact` and of `contact_point_ext` (DF-ACE-075 to DF-ACE-083, DF-EXT-013 to DF-EXT-026) | Not specified in the source documents (GAP-1123; ASM-2071) | Yes | None |
| partyId | person_key of `v_ace_customer` (DF-ACE-055 to DF-ACE-074), carried as the party reference | uuid | Yes | None |
| contactType | contact_type; the channel of the contact point | varchar(15) | Yes | LOV-CHANNEL (TSD P6 T3.2) |
| consentState | consent_given of `contact_point_ext` (DF-EXT-013 to DF-EXT-026) | Not specified in the source documents (GAP-1121; ASM-2069) | Yes | the consent set is Not specified in the source documents (GAP-1121; ASM-2069) |
| consentAt | consent_at | Not specified in the source documents (GAP-1121; ASM-2069) | No | None |
| verifiedAt | verified_at | Not specified in the source documents (GAP-1121; ASM-2069) | No | None |
| failedCount | failed_count | Not specified in the source documents (GAP-1121; ASM-2069) | No | None |
| blockedByStop | none in the legacy row; derived from the contact-stop events | boolean | No | None |
| stopReasonCode | none in the legacy row; the reason code the deviation event carries | Not specified in the source documents (GAP-1123; ASM-2071) | No | None |
| version | none in the legacy row; the owner's version of the contact point | Not specified in the source documents (GAP-1123; ASM-2071) | Yes, in `If-Match` | None |
| the eight fields the legacy row leaves unnamed | `contact_point_ext` DF-EXT-013 to DF-EXT-026 minus the six named | Not specified in the source documents (GAP-1123; ASM-2071) | n/a | None |

| Item | Content |
|---|---|
| Request | `ContactPointRequest` carries `contactType`, `consentState`, `consentAt`, `verifiedAt`, `failedCount` and `version`; `contactKey` comes from the path and `partyId` from the read |
| Answer | 200 with `ContactPoint` on the write and 200 with the `ContactPoint` list on the read, newest channel order, each carrying the stop mark of the case named in the query |
| Decision record | The library's element: the decision code, the rule id and version, the party reference, the contact key, the channel, the state written, the final call and the decided-at (DP-03) |
| Stop mark | A boolean and the reason code the event carried; no contact value and no consent value (BR11) |
| Personal data | None: identifiers, channel codes, consent codes and dates only; a contact value and its masked form never appear (BR8) |

**No contact table and no migration of a contact table.** `contact_point_ext`, `party_ext`, `account_ext`, `valuation_ext`, `interaction`, the thirty `v_ace_*` views, `recovery_case`, `case_party`, `deviation`, `decision_log_entry`, `rule_row` and `lov_value` are other owners' and appear only as consumed shapes. `contact_stop`, `decision_record`, `idempotency_key`, `outbox_event` and `processed_event` are the P6 rows this service owns; the first is created by `RWB-P6-E4039-APP`'s migration and the library objects are created in `rwb_comms` by the library's migration and are named here, not declared. `notice`, `template` and `merge_field` are P6 rows that this document does not touch (GAP-1118; ASM-2066).

**No personal data.** No element of this contract carries a contact value, a masked contact value, a name, an address, an identity number or an account number. The party and the contact point are reached by identifiers and codes, and the contact stop by a code.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Both operations are new: no contact operation is in the endpoint inventory of the TSD (GAP-1120; ASM-2068).

| ID | Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|---|
| new | GET | `/parties/{partyId}/contact-points` | none; `partyId` from the path and an optional case reference for the stop mark | 200 with the `ContactPoint` list | Documents R, scope applied | Not applicable | 401, 403, 404, 503 |
| new | PUT | `/contact-points/{contactKey}` | `ContactPointRequest`; `contactKey` from the path | 200 with `ContactPoint` and its new version | Documents U, scope applied | `If-Match` with the version; a repeated version returns the first answer | 401, 403, 404, 409, 422, 503 |

The purpose, the shapes and the refusals are this baseline's own, because no TSD P6 T-A.1 row names a contact; the base and the naming are DP-13's and DP-14's. The two notice operations of the module, API-P6-001 (Litigation C) and API-P6-002 (Litigation R), are `RWB-P6-E1052-CON`'s and are not redeclared here. The capability area and the rights are declared from TSD P6 T6.1, where RW-COMPLY holds Documents RU and RW-CASEOWN holds Documents CRU (GAP-1122; ASM-2070).

#### 12.2 REST operations consumed

None declared as an operation of this document; the two rows below are the consumed shapes the app story calls, each one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020).

| Shape | Owner | Declared here | Open point |
|---|---|---|---|
| The contact read: the contact points of a party with the consent, verification and failed-count state of each channel | P1 rwb-source-data | The answer elements the read needs, taken from `v_ace_contact` and `contact_point_ext` on the owner's contract | Consumed and faked; the path and the element list are Not specified in the source documents (GAP-1119; ASM-2067) |
| The consent and verification write of one contact point and one channel | P1 rwb-source-data | The request (the contact key, the channel, the consent state, the consent date, the verification date, the failed count) and the answer that carries the stored state and its version | Consumed and faked; no operation of that contract is named for it in any source and no C row is declared (GAP-1119; ASM-2067) |

No row reads a table, no row reads a `v_ace_*` view, and no row is declared as a provided operation of this service (BR6, BR7).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, rule id, rule version, party reference, contact key, contact type, the consent state written, decided-at; written by the local decision-record library (DP-03) |

This document declares the element and publishes nothing itself. No contact event is declared: the catalogue of Architecture v5 slide 42 holds none, and EV-13, EV-14 and EV-15 are the notice events of `RWB-P6-E1052-CON` and the dispatch stories.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, the deviation code and the reason code, the raised-at; consumed inside rwb-comms so a channel is marked as stopped, with the inbox dedupe (GAP-1123; ASM-2071) |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, the cleared-at and the code; consumed so the stop mark is lifted, with the inbox dedupe (GAP-1123; ASM-2071) |

The two rows are consumed by `RWB-P6-E4039-APP`; this baseline fixes their names, their topic and their key (`caseId`) and declares no subscription of its own. They are the "events DeviationRaised / Cleared (contact stop)" of Architecture v5 slide 17.

#### 12.5 Workflows and activities

None. A read and a consent write are two synchronous operations with one library write and one owner call; this document declares no workflow, no child workflow and no activity, and `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is declared: JOB-10 of the catalogue is the daily WIN dispatch of `RWB-P6-E2021-CON`, and the ACE freshness check of the contract data is P1's (Architecture v5 slide 41).

#### 12.7 Tables owned

| Table | Schema | Owner | Contracted use |
|---|---|---|---|
| contact_stop | `rwb_comms` | P6 | The stop flag, the reason code, the last event applied and the received time, per case reference; created by RWB-P6-E4039-APP's migration; no contact value and no consent state |
| decision_record, idempotency_key, outbox_event, processed_event | `rwb_comms` | PLT library objects applied in this schema | The decision entry of a consent change, the stored answer of the write, the envelope of the published row and the inbox of the two consumed rows (DP-03) |
| notice | `rwb_comms` | P6 | Owned by this service and not read or written by this document; the notice stories own it |
| template, merge_field | `rwb_comms` | P6 | Owned by this service and not read or written by this document; the template stories own them |

`contact_point_ext`, `party_ext`, `account_ext`, `valuation_ext` and `interaction` are P1's in `rwb_source_data`, and the thirty `v_ace_*` views are P1's ACE view contract; `recovery_case`, `case_party`, `task`, `timer` and `queue` are P3's; `decision_log_entry`, `rule_row`, `approval` and the rule package rows are P7's; `deviation` is S8's; `lov_value`, `reference_row`, `reference_version` and `parameter_value` are P3's; `document` is P5's; `outbound_item` and `interface_config` are P2's. They are named as consumed answers only, and no foreign key crosses a service boundary (DP-01; GAP-1118; ASM-2066).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Contact fake | The two operations of 12.1 | A 200 read list of three channels with a withdrawn and an unverified channel, a party with no contact point, a 200 write with the stored state and its new version, and the 401, 403, 404, 409, 422 and 503 refusals |
| Owner contact fake | The two rows of 12.2 | A party the owner returns and one it does not; a consent write with a stored state, a 5xx and an answer delayed beyond 2 s; a version the owner moved on |
| Stop-event fake | The two rows of 12.4 | No stop, a stop in force with its reason code, a lifted stop and a duplicated event for the inbox |
| Decision-record library stub | DP-03 | A healthy chain with its outbox row, and a stopped chain |
| Drift test | Every fake against the document | A drifted fake fails the build |

The owner and stop fakes are stubbed from the owners' published documents and carry the placeholder where the source is silent (GAP-1119; ASM-2067; GAP-1123; ASM-2071).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The contact read and the consent write provided; the contact read and the consent write of rwb-source-data consumed; one hop, 2 s |
| Kafka | 1 declared as written by its owner, 2 consumed | `DecisionRecorded` through the library; `DeviationRaised` and `DeviationCleared`; no contact event |
| Temporal | None | No workflow, no activity, no Schedule |
| File | None | No file element in this contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the addition to `openapi/rwb-comms-v1.yaml` for the contact resource, the `ContactPoint` and `ContactPointRequest` schemas in `th.co.scb.ace.workbench.recovery.comms.api`, the decision-record fragment, the fake set and the drift test. The implementation behind it is `RWB-P6-E4039-APP`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the element and declares no record field of its own | referred to; the consuming app story carries the H row |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; the document declares the contract rows and no view | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the answer is reached through it and the contract declares no composite route | referred to; the consuming app story and the platform edge story carry the H row |

DP-13 and DP-05 are the patterns this story publishes: the first fixes the base, the second fixes that the ACE contact rows and `contact_point_ext` are read and written on the rwb-source-data contract and never here. DP-03 is named and not declared: the record is the library's and the only trace on the resource is the decision element. DP-01 is in force as a prohibition: `contact_point_ext`, `party_ext` and the ACE contact points are P1's, so this service declares no contact table, no consent column and no `v_ace_*` query, and reads none (GAP-1118; ASM-2066). DP-19 is the route the screen uses and is `RWB-PLT-N001-CON`'s. This story being a CON story, it holds no build dependency by rule (Template and Rules §R5.7 rule 1).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ContactOpenApi | Document | The base, the two operations, the security, the error set and the versioning section (BR1 to BR6) |
| ContactSchema | Published schema | `ContactPoint` and `ContactPointRequest` with the elements, the required set and the placeholders (BR8, BR10) |
| BoundaryNote | Resource | The absence of a contact table, of a consent column and of a `v_ace_*` query, and the P1 rows named as consumed (BR7) |
| DecisionElement | Document | The decision-record element of a consent change on the shared topic (BR9) |
| ConsumedShapes | Document | The contact read and the consent write of rwb-source-data and the two contact-stop events, with their placeholders (BR6, BR11, BR13) |
| ProblemEnvelope | Reused schema | The platform problem document with its `messageId` extension (BR4) |
| VersionRule | Document | The `If-Match` header, the repeated-version answer and the stale-version refusal (BR3) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-version answers of every consuming build (AC5) |
| DriftTest | Test asset | The comparison of a consuming build against sections 11 to 13 (AC5, AC6) |

**Database.** No new table is declared here. The only P6 row the contract touches is `contact_stop`, created by `RWB-P6-E4039-APP`'s Flyway step in `rwb_comms` and never editing an applied migration (DP-15); its shape is the placeholder of section 11. No contact table and no other schema is named.

**Configuration and reference data.** The consent state set, the verification rule, the failed-count threshold, the channel list and the decision code are reference data or parameters read with the version in force (BR10). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Add the contact resource and the two operations to the document and lint the paths, the rights and the additive rule (AC1).
2. Write the two schemas with the elements, the required set and the placeholders; validate the example (AC2).
3. Write the boundary note and the absence tests for a contact table, a consent column and a `v_ace_*` query (AC2, AC6).
4. Write the error section with one message ID per condition and the `If-Match` rule of the write (AC1).
5. Write the decision element and the three consumed shapes with their placeholders (AC3, AC4).
6. Generate the fake set and the drift test and wire the drift test into the build of `RWB-P6-E4039-APP` (AC5).
7. Write the naming and boundary section and the absence tests for the old base, a contact event and a second topic (AC6).
8. Publish v1 and record the pinned version of this contract and of each consuming story.

**Feature flag.** `rwb.comms.contact-repository-contract`.

**Done when.** The document lints, the two schemas validate, the boundary note applies twice, the fakes answer every status including the repeated version, the absence tests are green and `RWB-P6-E4039-APP` has accepted the baseline.

### 14. Validation and messages

| ID | When | Published as | Message |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written by the consuming story (X7, legacy AC2) | 503, problem body with `messageId` MSG-P7-003 | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not hold the right of the operation | 403, problem body with `messageId` MSG-P4-002 | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required property is missing, the channel is not in LOV-CHANNEL, or the consent state is not in the reference data in force | 422, problem body with `messageId` MSG-GEN-001 and `field` | Enter {field}. |
| Not specified in the source documents (GAP-1121; ASM-2069) | The `If-Match` version is stale, or the owner does not answer | A 409 or 503 with the platform envelope; the text is left to the owner of the message list | The message IDs and texts of these conditions are contract elements the sources do not give |

MSG-P7-003, MSG-P4-002 and MSG-GEN-001 are the three messages of the legacy validation table that this surface raises and are copied unchanged. MSG-P6-001, MSG-P6-002 and MSG-P6-003 belong to the contact stop, the consent check of a send and the dispatch of a notice and are declared by the dispatch story, not here. No text is invented.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template and its approval states, so it cannot show a consent state; no source of this module names a contact repository screen (GAP-1120; ASM-2068). The repository surface is reached through the gateway-bff composite route of DP-19 (`RWB-PLT-N001-CON`), which calls this service once for the contact points of the party and once for the consent write and merges the answers with the case surface it already holds.

| Surface | State | What this contract serves |
|---|---|---|
| Contact repository of a party | Consented | The `ContactPoint` list with the consent state, the consent date, the verified mark and the failed count of each channel |
| Contact repository of a party | Withdrawn | The channel with its withdrawn state and no verified mark; the other channels unchanged; the statutes of the case continue |
| Contact repository of a case under a stop | Stopped | `blockedByStop` true and `stopReasonCode` for every contact point of the case, with the consent states unchanged |
| Contact repository of a party | Refused | The 403 with MSG-P4-002, the 409 with the placeholder of section 14, and the 422 with MSG-GEN-001 |

The route, the merge order, the screen field list and the masking of any contact value belong to `RWB-PLT-N001-CON`; the transitions behind each state are the app story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-039-01 | AC1 | Contract | Party `PT-0101` of case `RC-2026-000321`; the contract half answers the 200 `ContactPoint` list and the 200 write with the stored state and its new version |
| TC-E4-039-02 | AC2 | Contract | Decision log stubbed unavailable; the contract half answers the stopped chain and the 503 of MSG-P7-003 |
| TC-E4-039-03 | Access | Contract | A role without the Documents right sends the GET and the PUT; the contract half answers the 403 of MSG-P4-002 |
| TC-E4-039-04 | Principle 5 | Contract | The stopped chain of the library stub on 10 consent changes; the contract half answers the same 503 and the drift test |
| TC-P6-E4039-CON-01 | AC1 | Contract | The document validates; the two operations, the rights, the `If-Match` rule, the two new markers and the six refusals are present |
| TC-P6-E4039-CON-02 | AC2 | Contract | The ten elements, the request set, the placeholders, the channel list and the absence of a contact value are present; no contact table is declared |
| TC-P6-E4039-CON-03 | AC3 | Contract | The decision element, the reference-data placeholders and the single published row are present; no contact event and no second topic |
| TC-P6-E4039-CON-04 | AC4 | Contract | The two consumed rows with their owner and their placeholder, the one-hop rule and the two stop events with their key; no provided operation of another service |
| TC-P6-E4039-CON-05 | AC5 | Component | The contact, owner, stop-event and library fakes match the document; a drifted fake fails the build |
| TC-P6-E4039-CON-06 | AC6 | Contract | The nine sub-tables with their owners, the naming baseline and the absence tests for a contact table, a consent column, a `rwb_source_data` query and a `v_ace_*` view |

The four legacy identifiers keep their legacy order, their legacy covers and their legacy data, and carry the level of the surface they prove here, which is the contract: the legacy table has no level column, and the end-to-end proof of the same cases is RWB-P6-E4039-APP's. The six `TC-P6-E4039-CON-*` identifiers are new tests of the artefact. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the consent states, the verification rule, the failed-count threshold, the channel list and the decision code stay data or reference data read with the version in force.
- No personal data in a schema, an example or a fake: identifiers, channel codes, consent codes and dates only; a contact value and its masked form never appear.
- The contract names only rwb-comms rows and only operations owned by rwb-comms; the contact read and the consent write of rwb-source-data are consumed and faked, never declared as provided (DP-01, DP-05).
- No contact table, no consent column and no cross-schema read: the absence test of AC6 fails a build that declares `contact_point_ext`, a column of it, a query on `rwb_source_data` or a `v_ace_*` view.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No event is invented and none of the three catalogue events of this service is claimed: the only published element is the library's `DecisionRecorded` (DP-03).
- An absent value is written as the placeholder with its gap and assumption pair and never guessed: the composite key, the consent set, the verification rule, the failed-count threshold, the eight unnamed fields, the physical types, the reason code and the version.
- Every example in the document is synthetic; no production payload, contact value, identifier or file is copied into a schema or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-039 |
| Legacy criteria | AC1 and AC2 of the legacy story, both owned by RWB-P6-E4039-APP; this baseline copies neither |
| Legacy test cases | TC-E4-039-01 to TC-E4-039-04, as the contract half of each case |
| New contract cases | TC-P6-E4039-CON-01 to TC-P6-E4039-CON-06 |
| Legacy feature | FEAT-COM-05 Maintain the contact repository (FSD P6 A2.18), prerequisite FEAT-RDF-04 |
| Legacy data rows | v_ace_customer DF-ACE-055 to DF-ACE-074; v_ace_contact DF-ACE-075 to DF-ACE-083; contact_point_ext DF-EXT-013 to DF-EXT-026; notice DF-LEG-015 to DF-LEG-023; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015; template DF-REF-045 to DF-REF-051 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 in force as a prohibition) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-04, R-UNI-10, R-UNI-39, R-UNI-44, R-LIT-05; VR-P6-018-1, VR-P6-018-2 and BR-P6-018 of FSD P6 A2.18.3.1 |
| Requirements | REQ-OCC-006, REQ-OCC-010 and NFR-044 name the consent state per channel and the verified contact point; the endpoint inventory holds no contact operation (GAP-1120; ASM-2068) |

### 19. Out of scope

- The implementation of the two operations, the stop mark, the decision write, the owner call and the version answer (RWB-P6-E4039-APP).
- The contact points, the contact values, the consent state, the verification and the failed count: P1 rwb-source-data (`contact_point_ext`, `party_ext`, the `v_ace_contact` rows and the ACE view contract), with the P1 stories that build them.
- The deviation, its codes and its lifecycle, and the contact stop as a case fact: S8 rwb-deviation and P3 rwb-case. This baseline consumes two events and reads no deviation row.
- The decision-record library, its chain and its outbox (RWB-PLT-E1027-CON and the RWB-PLT-LIB stories); this baseline names the element and writes none of it.
- The dispatch of a notice and the consent and stop checks of a send (RWB-P6-E2021-CON, RWB-P6-E2022-CON and RWB-P6-E5002-APP).
- The right, the scope and the masking at the edge, and the contact repository surface (RWB-P4 stories and RWB-PLT-N001-CON); the legacy screen SCR-33 Template approval belongs to the template stories.
- The notice, the template and the merge-field administration (RWB-P6-E1052-CON, RWB-P6-E1046-CON and RWB-P6-AD017-CON).
- The consent state set, the verification rule, the failed-count threshold and the message texts of a refusal: the owners of the reference data and of the message list.

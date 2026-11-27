# RWB-P6-E1052-CON Notice generation v1

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1052-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-052 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP05, DP07, DP09, DP11, DP13, DP15, DP19 |
| Readiness decisions | RD-P1-001, RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-021, RD-P1-041, RD-P1-060, RD-P1-062, RD-P1-064 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P6-E1052-CON-16) |
| Contract version | v1, the version of the `/api/recovery/comms/v1` base (section 1) |
| Depends on (build) | None |
| Contract dependencies | rwb-document (P5) for the write-once generated PDF; request and answer shape published by RWB-P5-E2026-CON; consumed and faked from rwb-source-data.yaml 5.1.0 (API Specification v7): RWB-P1-E1016-CON (data-product records), RWB-P1-E1015-CON (freshness) and `getCustomer` (RD-P1-060; builder RWB-P1-E1069-APP); platform patterns DP-03, DP-07, DP-09, DP-15, DP-19 held in the pattern table and the preconditions and consumed against their fakes (GAP-2350, GAP-0754) |
| Integration dependencies | None |
| External dependencies | None |
| Retention job JOB-17 | Not owned by this story; no Schedule claimed. Owner RWB-P5-E1017-APP; attribution disagreement recorded for the story map (GAP-2351) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-003, FR-P6-005, FR-P6-006, FR-P6-007, FR-P6-008, FR-P6-009, FR-P6-010, FR-P6-011, FR-P6-012, FR-P6-013, FR-P6-014) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The `Idempotency-Key` rule is the platform rule: UUID header, 400, 409 and 503 answers, 24 hours; a second key for the same business facts answers 200 with the existing notice (RD-P1-001, RD-P1-064; finding #1; GAP-3351 closed).
- Errors are the shared Problem component (RD-P1-004; finding #2).
- The consumed source-data rows name their operations, products and contract stories; the name, address and phone are read through `getCustomer` (RD-P1-005, RD-P1-021, RD-P1-060; findings #3, #4).
- Stale is the `STALE` status of the freshness read and MSG-P1-001 carries the standard text; this baseline declares no ledger or delivery write (RD-P1-005, RD-P1-007, RD-P1-041; finding #5).
- Finishing pass: customer reads through `getCustomer` (RD-P1-060); never-stamped hold (RD-P1-062); a second key answers 200 with the existing notice (RD-P1-064); test case IDs of Test Cases v9 and the Error and Message Standard v6 wording applied.
- Test case citations aligned to Test Cases v9: identifiers of this story replace the placeholders and the shared legacy identifiers that now hold another story's case (W2-tests mapping).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-052 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E1052-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 29 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Not specified in the source documents (DOR-RWB-P6-E1052-CON-1)**, I want **the published contract baseline of the two notice operations — `POST /api/recovery/comms/v1/cases/{caseId}/notices` and `GET /api/recovery/comms/v1/notices/{noticeId}` on base `/api/recovery/comms/v1` — with the request and answer shapes, the notice fields, the state and hold-reason values, the error envelope and its message IDs, the `Idempotency-Key` answer, the `NoticeGenerated` and `DecisionRecorded` envelopes, the nine contract tables and the five contract fakes**, so that **the app stories of this legacy key build against a fixed, testable contract on Day 1 and a field, a state value or a message code can never drift between rwb-comms, rwb-source-data, rwb-case, rwb-decision and rwb-document without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). Notice generation shows why the baseline has to be fixed before the build: one request reaches four owners — rwb-case for the case and the parties, rwb-source-data for the customer, the address and the balance, rwb-document for the write-once PDF and rwb-decision for the ledger that reads the decision record — and one answer carries a state, a hold reason, a template version and a document ID that three screens and one event read.

The baseline also fixes the naming the checks require: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1`, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery`, and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that `NoticeGenerated` is event 13 of the catalogue and stays on `rwb.comms.events.v1` while its consumers are rwb-decision and the reporting read model, and that the decision record leaves through the shared topic `rwb.decision-record.v1` and not through the service's own topic (DP-03, DP-09).

It records too what the notice answer never carries: no notice body, no addressee, no account number and no merge value. The answer holds IDs, codes, dates and a document ID, and the delivery facts are read through rwb-source-data and never written back by this service.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the schema, topic, event and path names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- The template catalog contract of RWB-P6-E1046-CON is published, so the `template` and `merge_field` reads this baseline relies on have one owner document.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No production data is used in any example, schema or fake; every case number, person key, template code and delivery reference is synthetic.

### 4. Flow

1. Draft the rwb-comms OpenAPI 3.1 fragment of the two notice operations and the Notice resource.
2. Fix the state values, the hold reasons, the sent type list and the delivery status list as enumerated elements of the answer, each read from reference data and not written in code.
3. Map every failure to the error envelope and one message ID, one condition per row.
4. Fix the `Idempotency-Key` rule: required on the POST as a UUID, applied by the platform idempotency helper and replayed from the stored answer; the unique key on case, notice type, `person_key` and business date is the operation's own rule for a second key.
5. Record the two published events with their schema elements, their key and their envelope, and the three declared consumed events.
6. Record that no workflow, no Schedule and no JOB element belongs to this story.
7. Publish the nine contract tables of section 12 and the five contract fakes.
8. Add the contract tests: schema validation, the state enumeration, the error mapping, the idempotency replay, the event payload with no personal value, the drift between a fake and the document, and the absence of a retired element.
9. Tag the baseline and hand it to RWB-P6-E1052-APP, the dispatch stories RWB-P6-E1055-APP, RWB-P6-E2021-APP and RWB-P6-E2022-APP, and the harness RWB-ITG-E1052-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope, and a malformed request answers 422 | MSG-GEN-001 | AC1, AC4 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A state value or a hold reason is added or removed | The enumeration test fails, and the change is a new major version of the answer | None | AC3 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC7 |
| X5 | A consumed path or a raise-task operation is not in the Ownership Map | The row carries its gap and its assumption, and the fake is derived from the owner's published document | None | AC7, AC8 |
| X6 | A retired element reappears in the document, a job or a topic | The absence test fails: no dispatch job, no dispatch Schedule and no notice topic other than `rwb.comms.events.v1` | None | AC6, AC8 |
| X7 | A personal value appears in an example, a payload or a fake | The scanner fails the build and names the field and the sink | None | AC6 |
| X8 | A field-level definition is missing from the source material | The field is marked with the placeholder and one gap row is carried | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the template contract of the same service and the Ownership Map only |
| Negotiable | Field-level detail is settled with the consumers; the two operations, the state values, the message IDs and the two event names are fixed by the target architecture and the legacy story |
| Valuable | Unblocks the app stories of this legacy key and every consumer of the notice answer on Day 1 |
| Estimable | One document fragment, two operations, one resource, nine contract tables, five fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of notice generation

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-comms REST base is /api/recovery/comms/v1 and its topic is rwb.comms.events.v1
    Given no production data is used in any example, schema or fake

  Scenario: AC1 The OpenAPI document declares the two operations with their request and answer shapes (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/notices with the NoticeRequest body and the Notice answer, answering 201
    Then it declares GET /notices/{noticeId} with no request body and the Notice answer, answering 200
    Then both operations sit under the base /api/recovery/comms/v1 and name rwb-comms as their owner
    Then POST declares the Idempotency-Key header as required and GET declares no Idempotency-Key
    Then POST names the security right Litigation C with the scope applied and the error responses 400, 401, 403, 404, 409, 422 and 503
    Then GET names the security right Litigation R with the scope applied and the error responses 401, 403, 404 and 503
    Then every property of the NoticeRequest is required except the ones the legacy criteria omit, and every added property is optional, so a consumer of the previous version keeps working

  Scenario: AC2 The Notice resource fixes the notice, document, party and template fields (new, D-RCV-60)
    Given the Notice resource declared in the document
    When its properties are compared with the notice table of the service
    Then it carries noticeId, caseId, documentId, noticeType, sentType, personKey, templateId, templateVersion, state, holdReason, sentDate, barcode, callbackDate, deliveryStatus and messageCodes
    Then noticeId, caseId, noticeType, templateId, templateVersion and state are required, and documentId, sentType, personKey, holdReason, sentDate, barcode, callbackDate, deliveryStatus and messageCodes are optional
    Then noticeType is an element of LOV-NOTICE, sentType of LOV-SENT-TYPE and deliveryStatus of LOV-DELIVERY, each read as reference data and never written in code
    Then personKey is the ACE business key the legacy criteria name and partyId is carried beside it as the notice party reference, because the module specification names DF-LEG-030 party_id while the legacy story names the same field person_key
    Then the resource carries no notice body, no addressee, no account number, no merge value and no name

  Scenario: AC3 The state values and the hold reasons are enumerated (new, D-RCV-60)
    Given the state element of the Notice resource
    When its values are compared with the notice state machine
    Then state is one of Generated, Held, Sent, Delivered and Unserved
    Then Held carries holdReason POSTAL_ADDRESS or TEMPLATE_WITHDRAWN and no other hold reason is declared by this baseline, because no list of values enumerates the hold reasons (GAP-1087; ASM-2035)
    Then the document states that Generated, Held and the refusal leave no other state, and that Sent, Delivered and Unserved are written by the dispatch stories and only read here
    Then the document states that the legacy check constraint also carries APPROVED, which the notice approval story sets and this baseline does not
    Then the document states that a read never changes the state and never writes the notice row

  Scenario: AC4 The error envelope maps one message ID per condition (new, D-RCV-60)
    Given the error responses declared for the two operations
    When each condition is compared with the message catalog
    Then every 4xx and 5xx is "application/problem+json" with the shared Problem component, the message ID of the condition as messageCode, and no second envelope is introduced
    Then 400 answers a missing Idempotency-Key with MSG-PLT-N009-03, 409 answers a reused or in-flight key with MSG-PLT-N009-05 and 503 answers an unreadable key store with MSG-PLT-N009-06
    Then 401 answers with MSG-P4-001, 403 with MSG-P4-002 and 404 with MSG-P4-003 for a case or a person outside the caller's scope
    Then 200 answers a second request for the same case, notice type, person_key and business date that carries a different Idempotency-Key, with the existing notice, and no error message is mapped to it
    Then 422 answers a missing or invalid request field with MSG-GEN-001, a template with no Approved version with MSG-P6-005, and a required merge value that is empty with MSG-P6-007
    Then 503 answers a local decision record that cannot be written with MSG-P7-003 and a consumed call that exceeds the 2 s budget with MSG-GEN-006
    Then MSG-P6-003 is declared for the withdrawn-template hold and is returned with the answer, not as an error status
    Then the withdrawn template is answered as a hold with the notice in state Held and the hold reason of the withdrawn template, value Not specified in the source documents (GAP-1087), never with an error status; a repeat with the same key replays the first answer (AC5) and a repeat with a different key answers 200 with the existing notice
    Then no condition maps to two message IDs and no message ID is reworded

  Scenario: AC5 The Idempotency-Key rule is stated and its answer is stored (new, D-RCV-60)
    Given the Idempotency-Key header declared on POST /cases/{caseId}/notices
    When the rule is reviewed
    Then the key is a required UUID and a request without it is refused with 400 and MSG-PLT-N009-03
    Then the key is unique in the rwb_comms schema, the first answer is stored under it for 24 hours with the hash of the request, and the same key with a different request or still in flight is refused with 409 and MSG-PLT-N009-05
    Then a key store that cannot be read answers 503 with MSG-PLT-N009-06 and nothing is written
    Then a second call with the same key returns the stored answer with 201 and the same noticeId, state and documentId, and writes no second notice and no second document
    Then a second call with a different key and the same case, notice type, person_key and business date answers 200 with the existing notice and its noticeId, and the unique key writes no second notice
    Then the stored answer is held in the idempotency table of the platform library, not in a table of the service's own

  Scenario: AC6 The NoticeGenerated and DecisionRecorded envelopes carry IDs and facts only (new, D-RCV-60)
    Given the event section of the document
    When it is reviewed against the event catalogue
    Then rwb.comms.NoticeGenerated.v1 is declared as event 13 on rwb.comms.events.v1, written to the outbox in the same transaction as the notice row
    Then its CloudEvents envelope names the type, the source service, the subject caseId and the key caseId
    Then its data carries noticeId, caseId, templateId, templateVersion, noticeType and generatedAt, and nothing else
    Then rwb.decision.DecisionRecorded.v1 is declared on rwb.decision-record.v1 through the local decision-record library with the decision code D7.1 and the rule R-LIT-03
    Then the D7.1 generation entry carries the template code and version and the merge snapshot reference, the ACE data date, the notice reference and business date, and the final-call set GENERATED, HELD and REFUSED; the field layout of the entry and the text of MSG-P7-009 are Not specified in the source documents (GAP-2454)
    Then the document states that no event carries a name, an address, an account number, a merge value or a notice body
    Then the document declares no event, topic or payload element for dispatch, proof of delivery, SMS or LINE

  Scenario: AC7 The nine contract tables are complete and the five fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.5 and 12.6 record None and name the dispatch stories that own JOB-10 and NoticeDispatchWorkflow
    Then the rwb-source-data, rwb-case, rwb-case reference-data, rwb-decision and rwb-document fakes answer the paths and payloads of 12.2 and the shapes of 12.1
    Then each fake answers the legacy values of section 7 of RWB-E1-052 and a delayed answer beyond 2 s
    Then the contract tests compare each fake with the document and fail on any drift

  Scenario: AC8 The owned tables, the naming and the migration are fixed by the baseline (new, D-RCV-60)
    Given the tables, the names and the migration declared in this story
    When they are compared with the service catalogue and the ownership map
    Then the service owns notice, template and merge_field in schema rwb_comms, plus the library tables outbox_event, processed_event and idempotency_key created in that schema
    Then document and signature_request are named as rwb-document's, interaction as rwb-source-data's, recovery_case, case_party, task and timer as rwb-case's, and decision_log_entry as rwb-decision's, and none of them is declared as owned here
    Then the REST base is /api/recovery/comms/v1, the topic rwb.comms.events.v1, the queue rwb-comms in namespace rwb-recovery and the package th.co.scb.ace.workbench.recovery.comms
    Then the migration is a per-service Flyway script in the rwb-comms sequence and no script of another service is named
    Then the document states that the merge snapshot is an artefact of this service whose store is not named by any source read here (GAP-1081; ASM-2029)
```

These eight criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P6-E1052-APP. The legacy criteria of RWB-E1-052 are owned elsewhere: AC1 to AC6, AC8 and AC9 by RWB-P6-E1052-APP, and AC7 by RWB-ITG-E1052-ITG. The wave 1 harness RWB-ITG-E1052-ITG consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics | DP-14; Template and Rules §R4 |
| BR3 | Every event carries the CloudEvents 1.0 envelope, is keyed by caseId, is written to the outbox in the same transaction as its state change and carries no personal data | Architecture v5 slides 42 and 43 notes; DP-09 |
| BR4 | A read declares no Idempotency-Key; a POST declares it as a required UUID header and stores its answer for 24 hours: missing 400 MSG-PLT-N009-03, reuse with another request 409 MSG-PLT-N009-05, store unavailable 503 MSG-PLT-N009-06 | Architecture v5 slide 11; DP-09; legacy AC6; RD-P1-001 |
| BR5 | Error responses use the shared `Problem` component and one message ID per condition as `messageCode`; the business message texts are copied unchanged from the legacy story | Architecture v5 platform baseline; Template and Rules §R7.2 s14; RD-P1-004 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-comms; a consumed operation is described as consumed, never as provided | Ownership Map v1 |
| BR8 | The notice answer carries IDs, codes, dates and a document ID only: no notice body, no addressee, no account number and no merge value | RWB-E1-052 BR12; NFR-040; Template and Rules §R7.2 s17 |
| BR9 | The state values, the hold reasons, the notice type list, the sent type list and the delivery status list are reference data, not contract constants written in code | TSD P6 T3.2; DP-07; FSD P6 A2.1 |
| BR10 | The decision record is written locally through the decision-record library and published on `rwb.decision-record.v1`; it is never a new event of this service | RWB-E1-052 BR6; DP-03 |
| BR11 | No workflow, no Schedule and no job element is declared: JOB-10 and `NoticeDispatchWorkflow` belong to the dispatch stories | DP-10; Architecture v5 slides 17 and 44 |
| BR12 | No business value is fixed in the contract: template codes, product groups, merge codes, task codes and timeouts stay data or service configuration | Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the Notice resource, the state values and the error mapping are described | In review |
| In review | Consumer sign-off | The app stories of this legacy key and the rwb-source-data, rwb-case, rwb-decision and rwb-document owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new optional hold reason | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a state value is removed | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | Retired element reappears | The absence test of AC6 and AC8 fails | In review |

The notice state machine itself — Generated, Held with its hold reason, Sent, Delivered and Unserved — is declared by AC3 and is written by RWB-P6-E1052-APP and the dispatch stories, not by this baseline.

### 10. Authority

The letters below are taken from the rwb-comms RBAC matrix of the module specification and from no other table.

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI and AsyncAPI fragments and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of an Ownership Map row |
| Consuming teams (the app stories of this key, the dispatch stories, the harness, and the rwb-source-data, rwb-case, rwb-decision and rwb-document owners) | Review and sign off the parts they consume |
| RW-LITOFF, litigation officer | Documents CRU and Litigation CRUA: the role the baseline names on the POST and the read |
| RW-LEGAL, Legal counsel | Documents CRUA and Litigation RA: the role that owns the template approval the answer depends on |
| RW-CASEOWN, case owner | Documents CRU and Litigation R: the role that receives the "Complete notice data" task |
| RW-TEAMMGR, team manager | Documents R and Litigation R: a reading role on the answer |
| RW-PLATADM, platform administrator | Documents R only: a reading role on the answer with no Litigation right |
| Platform library owner | Owns the CloudEvents envelope, the error envelope and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event or an answer |

The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)". The authorisation decision itself is enforced at gateway-bff under RWB-PLT-N001-CON and RWB-P4-E1037-CON and is not declared here.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| NoticeRequest | The case ID from the path, the notice type, the `person_key`, the language, the business date and the `Idempotency-Key` header; the request field names beyond the legacy generation request are Not specified in the source documents (GAP-1082; ASM-2030) | Not specified in the source documents (DOR-RWB-P6-E1052-CON-7) |
| Notice resource | `noticeId`, `caseId`, `documentId`, `noticeType`, `sentType`, `personKey`, `partyId`, `templateId`, `templateVersion`, `state`, `holdReason`, `sentDate`, `barcode`, `callbackDate`, `deliveryStatus`, `messageCodes`, taken from notice DF-LEG-015 to DF-LEG-034; `partyId` and `personKey` are carried together; `personKey` is the business key of the notice; the legacy story names DF-LEG-030 as person_key and the module specification names it party_id (GAP-1084; ASM-2032) | DF-LEG-015 to DF-LEG-034; partyId field ID Not specified in the source documents (DOR-RWB-P6-E1052-CON-7) |
| Template and merge field | `templateId`, `templateVersion`, `noticeType` from `template` DF-REF-045 to DF-REF-069; the merge code catalog DF-REF-252 to DF-REF-260 is read inside the service and no merge value is returned | DF-REF-045 to DF-REF-069; DF-REF-252 to DF-REF-260 |
| Document reference | `documentId` only; `source` "GENERATED" and `write_once` true are the document owner's fields and are not copied into this answer | Not specified in the source documents (DOR-RWB-P6-E1052-CON-7) |
| Event payloads | IDs, codes, dates and the generated timestamp only; no name, address, identity number, account number or merge value | Not specified in the source documents (DOR-RWB-P6-E1052-CON-7) |
| Error body | The shared `Problem` component (`type`, `title`, `status`, `messageCode`, `traceId` required); no case fact. A second key for the same notice facts is not an error: it answers 200 with the Notice (RD-P1-064 rule 11) | Not specified in the source documents (DOR-RWB-P6-E1052-CON-7) |

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| ID | Method | Path | Documented shape | Access |
|---|---|---|---|---|
| API-P6-001 | POST | `/cases/{caseId}/notices` | Body NoticeRequest; answer 201 with the Notice, or 200 with the existing Notice for a new key that repeats the notice facts; errors 400, 401, 403, 404, 409, 422, 503 | Litigation C, scope applied; `Idempotency-Key` header (UUID) required, and its answer is stored (BR4) |
| API-P6-002 | GET | `/notices/{noticeId}` | No body; answer 200 with the Notice; errors 401, 403, 404, 503 | Litigation R, scope applied; no `Idempotency-Key` |

The error codes of each condition and the state values are fixed by AC3 and AC4. The response field names beyond the Notice type are Not specified in the source documents (GAP-1082; ASM-2030). Which condition the 409 of API-P6-001 answers, and whether a withdrawn template is answered as a hold with 201 or as an error, are Not specified in the source documents (GAP-1086; ASM-2034).

#### 12.2 REST operations consumed

| Method and path | Owner | Use in the baseline |
|---|---|---|
| GET `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The account balance and `data_as_of` (DP01) and the proof-of-delivery facts (DP07): `items` of `recordId`, `entity`, `fields`, with `freshness`; contract RWB-P1-E1016-CON. The customer name, address and phone are not read here (RD-P1-060 rule 4) |
| GET `/api/recovery/source-data/v1/customers/{personKey}` | P1 rwb-source-data | `getCustomer`: customer name, the `ADDRESS` row chosen by `contactKey` and the `PHONE` row, clear only for the rwb-comms notice identity where unmasked; rwb-source-data.yaml 5.1.0, RD-P1-060. Pending: unmask rows (GAP-3283) and the clear phone value (GAP-3396), owner data protection officer with the rwb-access owner |
| GET `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | `DataProductFreshness` of the merged products: `businessDate` (null only when never stamped), `status` `LOADED` or `STALE`, `staleSince`; the data date carried onto the decision record and the cause of MSG-P1-001; contract RWB-P1-E1015-CON. A never-stamped merged product holds the notice (RD-P1-062 rule 4; product owner confirmation open, GAP-3349) |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number, product group, status and owner; contract RWB-P3-E1018-CON |
| GET `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | The party links and roles, and the person-not-on-case refusal MSG-P4-003; contract RWB-P3-E1018-CON |
| POST `/api/recovery/case/v1/cases/{caseId}/tasks` | P3 rwb-case | The two task raises; the raise path is Not specified in the source documents as an operation of the Ownership Map (GAP-1085; ASM-2033) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-NOTICE, LOV-SENT-TYPE and LOV-PRODUCT; contract RWB-P3-E1043-CON |
| GET `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The read-back of the D7.1 entry in the contract tests; the write is local (DP-03) |
| POST `/api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | The write-once PDF and its document ID; no contract dependency row exists for P5 (GAP-1079; ASM-2027) |

Every row is one hop with a 2 s timeout, a GET retry once with jitter and a breaker per downstream (AC4, DP-11, ADR-020). The exact field names behind the rwb-source-data contract are Not specified in the source documents (GAP-1080; ASM-2028).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` (event 13) | `rwb.comms.events.v1` | P6 rwb-comms | noticeId, caseId, templateId, templateVersion, noticeType, generatedAt; key caseId; written to the outbox in the same transaction as the notice row; consumed by rwb-decision and the reporting read model |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision code D7.1, rule "R-LIT-03", rule version, template code and version, data date, record reference; published by the local decision-record library (DP-03) |

This story declares the two envelopes because the capability depends on them; it publishes neither itself. `generatedAt` is the outbox write time; the element list is not enumerated beyond the legacy payload, so the field is carried with the placeholder of GAP-1088 and ASM-2036.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, caseNo, fromState, toState, changedAt; declared so the hold rules have one owner for the case state |
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, raisedAt, contactStop; declared for the contact-stop rules the dispatch stories apply |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviationCode, clearedAt, outcome; declared as above |

This baseline fixes the three shapes and their key (caseId); the notice read path subscribes to none of them, and the consumers are RWB-P6-E2021-APP and RWB-P6-E2022-APP.

#### 12.5 Workflows and activities

None. Generation is synchronous: the POST answers with the notice and its document reference. No workflow and no activity is declared by this baseline. `NoticeDispatchWorkflow` exists in the service and belongs to the dispatch loop, which is RWB-P6-E2021-APP; its contract is fixed there, with JOB-10 WIN notices at 16:00 (Architecture v5 slides 17 and 44).

#### 12.6 Schedules

None. JOB-10 is the dispatch job of the rwb-comms and rwb-integration pair and is registered by the dispatch stories. This baseline declares no Schedule, no cron entry and no job name, and reads no shared scheduler table (DP-10).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The Notice resource: case, document, notice type, sent type, `person_key`, party, template, hold reason, dispatch fields and state |
| template | P6 (rwb_comms) | The template version the answer carries; written by RWB-P6-E1046-APP |
| merge_field | P6 (rwb_comms) | The merge code catalog behind the merge, never returned |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The two published events, the three declared consumed events and the stored `Idempotency-Key` answer of AC5 |
| local decision record | P6 rows in `rwb_comms`, written through the decision-record library | The D7.1 entry of every notice (DP-03) |

`document` and `signature_request` are P5 rwb-document's; `interaction` is P1 rwb-source-data's; `recovery_case`, `case_party`, `task` and `timer` are P3 rwb-case's; `decision_log_entry` is P7 rwb-decision's. None of them is declared as owned here and none is read directly (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | Records of case "RW-2026-000123" in the shapes of rwb-source-data.yaml 5.1.0: DP02 Customer and party with "P-0001", first_name "Anan", last_name "Sukjai" and the ADDRESS row "ADDRESS:A-9001" with contact_value "88/1 Bangkok" (served by `getCustomer`, unmasked for the rwb-comms notice identity and masked for others, RD-P1-060); DP01 Account and arrears with total_balance 1,250,000.00 and `data_as_of` 2026-11-25; the no-ADDRESS case; DP07 Legal with pod_key "POD-0001", notice_ref "WIN-77001", sent_date 2026-11-27, barcode "RR123456789TH" and delivery_status "DELIVERED"; freshness `LOADED`, DP01 `STALE` with `businessDate` 2026-11-23 and a never-stamped DP01 (`businessDate` null, `STALE`); a delayed answer beyond 2 s | App story, contract tests, harness |
| rwb-case WireMock | Case "RW-2026-000123" with product group "MORTGAGE" and party "P-0001" as borrower; case "RW-2026-000456" with product group "HIRE_PURCHASE"; the parties without "P-0999"; the case owner; the two task raises; a delayed answer beyond 2 s | App story, contract tests, harness |
| rwb-case reference-data WireMock | LOV-NOTICE, LOV-SENT-TYPE, LOV-PRODUCT and LOV-DELIVERY; a delayed answer beyond 2 s | App story, contract tests |
| rwb-decision WireMock | One D7.1 entry with rule "R-LIT-03", template "DEMAND-MTG" version 2 and the merge snapshot reference; an empty answer; a delayed answer beyond 2 s | App story, contract tests, harness |
| rwb-document WireMock | A stored generated document with `source` "GENERATED", `write_once` true, the footer "RW-2026-000123 DEMAND-MTG v2 2026-11-25"; a failure answer after the write; a delayed answer beyond 2 s | App story, contract tests, harness |

The values are the legacy values of RWB-E1-052 section 7 and the footer string of its AC1, kept unchanged so the component and integration assertions read the same fixtures.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 8 consumed | API-P6-001 and API-P6-002 provided; the eight rows of 12.2 consumed; one hop, 2 s |
| Kafka | 2 declared as published by their owners, 3 declared as consumed | `NoticeGenerated` and `DecisionRecorded`; `CaseStateChanged`, `DeviationRaised` and `DeviationCleared` |
| Temporal | None | No workflow and no Schedule in this baseline; `NoticeDispatchWorkflow` and JOB-10 belong to the dispatch stories |
| File | None | No file element in this contract; the PDF is a document reference only |

### 13. Solution plan

**Deliverables.** The additive change to the rwb-comms OpenAPI 3.1 document, the NoticeRequest and Notice components, the AsyncAPI fragment of `rwb.comms.events.v1` that names `NoticeGenerated`, the contract README rows for the state values, the hold reasons, the error mapping and the idempotency rule, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

No pattern is claimed for DP-04, DP-06, DP-08, DP-10, DP-14 or DP-18: this baseline declares no rule package, no parameter, no authorise call, no job, no renamed topic and no interaction ledger.

**Build steps**

1. Add the two operations and the NoticeRequest and Notice components to the OpenAPI document; validate the additive rule of AC1 in the pipeline.
2. Fix the state enumeration and the two hold reasons of AC3 as schema elements, and add a test that a new state value fails the build.
3. Write the error mapping of AC4 as one row per condition with its message ID, and assert that no condition carries two message IDs.
4. Write the idempotency rule of AC5 as a schema constraint and a README row, and test the replay and the 409 path against the fake.
5. Record the two published and the three consumed event envelopes, with a scanner that fails on a personal value in any example or payload.
6. Publish the five fakes and the seven contract tests; a drift between a fake and the document fails the build.
7. Add the absence test: no dispatch event, no dispatch Schedule and no JOB-10 element in this baseline.
8. Baseline tag and the consumer sign-off note, including the app stories of this key, the three dispatch stories, the harness and the four other owners.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and the drift test is green, no personal value appears in an example or a payload, and the app stories of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-005 | The template has no Approved version | {template} version {version} has no Legal approval. It cannot be used. |
| MSG-P6-007 | A required merge value is empty | {notice} for case {case} is on hold. {field} has no value on the case. |
| MSG-P6-003 | The template is withdrawn and the notice is held | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | The person is not on the case, or the case is outside the caller's scope | This case is not in your scope. |
| MSG-P4-002 | The role lacks the Litigation right | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | No Workbench role on the token | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-GEN-001 | A required request field is missing or invalid | Enter {field}. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Try again in a few minutes. |
| MSG-P1-001 | A merged data product is `STALE` on the freshness read of 12.2 | {product} is from {date}. Today's load has not arrived. |
| MSG-PLT-N009-03 | The POST arrives with no `Idempotency-Key` header or with a blank value (400) | Text owned by the platform library (RWB-PLT-N009) |
| MSG-PLT-N009-05 | The same key arrives with a different request (409) | Text owned by the platform library (RWB-PLT-N009) |
| MSG-PLT-N009-06 | The `idempotency_key` store cannot be read (503) | Text owned by the platform library (RWB-PLT-N009) |

The message IDs are contract elements and the text is the agreed text: MSG-P6-005, MSG-P6-007 and MSG-P6-003 are copied from RWB-E1-052 section 14, MSG-P7-003 and MSG-P4-003 from the same section, and MSG-P4-002, MSG-P4-001, MSG-GEN-001 and MSG-GEN-006 from the platform message catalog. MSG-P1-001 and MSG-P1-002 are message codes of rwb-source-data and are named on the consumed rows of 12.2 rather than declared as P6 messages; MSG-P1-001 carries the text of the Error and Message Standard v5.

### 15. Screens and states

The baseline serves the notice answer the three screens of the legacy story read through the gateway-bff composite route (DP-19):

| Screen | What it reads from this contract | State |
|---|---|---|
| SCR-30 Case documents | The notice as a generated document on the case, with its sent date, barcode and delivery status when the delivery facts exist | Generated, Held; loading as Screen Specifications v1, section SCR-30; empty, error and no access: Not specified in the source documents (CG-ALL-6402) |
| SCR-01 My work | Nothing from this contract directly; the hold tasks are rwb-case's, and the task names the field the answer holds | Held with its hold reason |
| SCR-18 Notice approval | The notice in state Generated, waiting for approval before dispatch | Generated; empty, loading, error and no access: Not specified in the source documents (CG-ALL-6401) |

The composite route, its field list, its masking rules and its timeout budget belong to RWB-PLT-N001-CON and are not fixed here. The notice PDF is reached through the documentId of the notice answer on rwb-document; the addressee role and the masked postal address are read from the rwb-source-data fields of the decision panel, and this contract carries neither. The Loading and Error states of the route are the platform route's, not this contract's. For SCR-01 the empty and loading states are those of Screen Specifications v1, section SCR-01; the error and no access states are Not specified in the source documents (CG-ALL-6400).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-052-11 | AC9, BR11 | End to end | rwb-source-data WireMock fake with POD-0001 and notice_ref WIN-77001, and a notice with no such fake row |
| TC-E1-052-01 | AC1, BR1, BR4, BR5, BR7, BR9 | End to end | RW-2026-000123 Mortgage, P-0001 with the ADDRESS row of the rwb-source-data WireMock, DEMAND-MTG TH v2 |
| TC-E1-052-02 | AC2, BR1 | End to end | RW-2026-000456 Hire purchase, RECALL-HP TH v1 Draft |
| TC-E1-052-03 | AC3, BR3, BR9 | End to end | P-0001 with the no-ADDRESS case of the rwb-source-data WireMock |
| TC-E1-052-04 | AC4, BR2 | End to end | DEMAND-MTG TH v2 Withdrawn |
| TC-E1-052-05 | AC5, BR6 | End to end | Decision log store stubbed unavailable |
| TC-E1-052-06 | AC6, BR8 | End to end | Same request twice on 2026-11-25 |
| TC-E1-052-07 | AC7, BR9 | End to end | No COMPLETED ALS row for 2026-11-25, `data_as_of` 2026-11-24 |
| TC-E1-052-08 | AC8 | End to end | P-0999 not on the case |
| TC-E1-052-09 | Access | Component | Service identity without Litigation R calls NoticeApi.generate; refused with MSG-P4-002 |
| TC-E1-052-10 | Principle 5 | NFR | Decision log write forced to fail during generation of 20 notices; none stored |
| TC-E1-052-12 | Section 12 | Contract | The contract fakes of 12.8 against the operations, events and activities of section 12 |
| TC-E1-052-13 | 12.7 tables | Component | The owned and not-owned tables of 12.7 at their boundaries |
| TC-E1-052-14 | BR10, BR12 | Contract | The DecisionRecorded envelope of 12.3 on rwb.decision-record.v1 and the business values held as data |
| TC-P6-E1052-CON-01, TC-P6-E1052-CON-02, TC-P6-E1052-CON-03 | AC1, AC4, AC5, BR4, BR5 | Component | The 400, 409 and 503 idempotency answers and the shared Problem body against the published document |

The first eleven cases are the legacy cases of this key, kept in the legacy order with their covers and data unchanged; legacy level System maps to End to end, Access to Component and Resilience to NFR. TC-E1-052-12 to TC-E1-052-14 are added contract and component cases for section 12, the tables of 12.7, BR10 and BR12 and have no legacy source. This baseline holds the artefact those cases are asserted against, so each row is proved twice: once against the contract fragment and the fakes, and once against the behaviour in RWB-P6-E1052-APP or, for TC-E1-052-07, in RWB-ITG-E1052-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. TC-E1-052-11 covers AC9, which RWB-P6-E1052-APP owns; it is run by RWB-P6-E1052-APP and not by this story.

### 17. Guardrails

- No business value in the contract: template codes, product groups, merge codes, task codes, the notice type list, the sent type list, the delivery status list, the state values and the timeouts stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: IDs, codes, dates and a document ID only; no name, address, identity number or account number, and no notice body or addressee.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the source-data, case, decision and document operations are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- ACE data is reached only through the owner's contract; this document declares no ACE view and no cross-schema join.
- The decision record is a local record on the shared topic and never a new event of this service (DP-03).
- No retired element is reintroduced: the absence test fails a build that declares a dispatch event, a dispatch Schedule or a JOB-10 element in this baseline.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.
- Every example is synthetic; no production payload is copied into a schema or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-001 | Notices from Legal-approved templates with merge fields from case data | API-P6-001, API-P6-002, the Notice resource, the state values and the message IDs | TC-E1-052-01 to TC-E1-052-11 |
| RWB-E1-052 | The legacy key whose contract this baseline fixes | The eight criteria of section 7 | TC-E1-052-01 to TC-E1-052-11 |
| DP-01 | Owner's schema; no service reads another service's tables | The owned and not-owned lists of 12.7 | TC-E1-052-01, TC-E1-052-03, TC-E1-052-13 |
| DP-02 | One login per service | The security scheme of section 10 | TC-E1-052-09 |
| DP-03 | Local decision record and the shared topic | The `DecisionRecorded` row of 12.3 | TC-E1-052-01, TC-E1-052-05, TC-E1-052-10, TC-E1-052-14 |
| DP-05 | ACE data through rwb-source-data's contract | The two rwb-source-data rows of 12.2 | TC-E1-052-01, TC-E1-052-03, TC-E1-052-07, TC-E1-052-11 |
| DP-07 | Reference data through rwb-case's contract | The reference-data row of 12.2 and the enumerated lists of AC2 | TC-E1-052-01, TC-E1-052-02 |
| DP-09 | Outbox, inbox and CloudEvents | The `NoticeGenerated` envelope of AC6 and the three consumed events of 12.4 | TC-E1-052-01, TC-E1-052-06 |
| DP-11 | REST contract with mock, one hop, 2 s | The eight consumed rows and the five fakes of 12.8 | TC-E1-052-01 to TC-E1-052-08, TC-E1-052-12 |
| DP-13 | Per-service REST base | `/api/recovery/comms/v1` | TC-E1-052-01 to TC-E1-052-11 |
| DP-15 | Per-service Flyway | The migration of AC8 | TC-E1-052-06 |
| DP-19 | Screen through gateway-bff | The three screen reads of section 15 | TC-E1-052-01, TC-E1-052-03 |
| ADR-013 | 19 services inside ACE | The service boundary of 12.7 | TC-E1-052-01 |
| ADR-014 | Schema and login per service | `rwb_comms` and its own login | TC-E1-052-09 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The outbox rule of AC6 and the inbox of 12.4 | TC-E1-052-01, TC-E1-052-06 |
| ADR-020 | Contract-first REST, one hop, 2 s | The 2 s budget and the error mapping of AC4 | TC-E1-052-08, TC-E1-052-10 |
| ADR-021 | Per-service Flyway and migration ownership | The migration row of AC8 | TC-E1-052-06 |

### 19. Out of scope

- The implementation of the two operations, the merge, the renderer, the hold paths and the event publish (RWB-P6-E1052-APP).
- Legacy AC7, the stale ACE account batch, and the end-to-end proof of the journey (RWB-ITG-E1052-ITG).
- The write-once generated document and its operation, consumed and faked here but owned by rwb-document (RWB-P5-E1052-APP and its contract).
- The case, the parties, the task raise and the reference-data lists, owned by rwb-case and consumed here.
- The central decision ledger entry and its read, owned by rwb-decision and consumed here.
- The customer, contact, account, freshness and delivery data products, owned by rwb-source-data and consumed here.
- Dispatch to WIN, proof-of-delivery capture, JOB-10 and `NoticeDispatchWorkflow`: RWB-P6-E1055-APP and RWB-P6-E2021-APP, with their own contracts.
- SMS and LINE dispatch through NSS and LINE OA: RWB-P6-E2022-APP and its contract.
- Template authoring, approval and withdrawal, and the merge field catalog: RWB-P6-E1046-CON and RWB-P6-E1046-APP.
- Approval of demand and recall notices before dispatch: RWB-E2-014.
- The litigation route rules that call generation in production: R-LIT-01 and the Epic 5 rule work.
- The gateway-bff composite route, its masking and its timeout budget (RWB-PLT-N001-CON), and the three screens themselves.
- The deployment, the consumer groups, the dashboards and the runbook of the service.

### 20. Remaining delivery steps

- Publish and baseline the rwb-comms fragment: declare the `Idempotency-Key` parameter and the 400 answer on the notice POST in rwb-comms.yaml (rwb-comms service owner).
- Add the masking rule rows for the rwb-comms notice identity (GAP-3283) and rule the clear phone value (GAP-3396); data protection officer with the rwb-access owner.
- Declare the 200 answer of `POST /cases/{caseId}/notices` in rwb-comms.yaml and update the second-key test data (contract owner and test lead; RD-P1-064).
- Publish the five fakes with fixed versions (tech lead of rwb-comms with the owning service owners).
- Add the changed test cases in Test Cases v9 (test lead).
- Collect the consumer sign-off and set the size (tech lead and squad).

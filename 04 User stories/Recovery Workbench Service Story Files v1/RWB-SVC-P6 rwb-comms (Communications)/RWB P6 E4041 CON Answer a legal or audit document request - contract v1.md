# RWB-P6-E4041-CON Answer a legal or audit document request

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4041-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-041 |
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

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-041 for rwb-comms; the contract baseline of the document-request answer, its two operations and its consumed document read. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the document-request answer of rwb-comms — the two operations on `/api/recovery/comms/v1`, the request and answer shapes, the nine index fields of a notice, the document read it consumes from rwb-document with the discovery production named as that service's, the decision-record element, the two request tables, the nine contract tables and the fakes**, so that **the app story of this legacy key builds against one fixed, testable contract on Day 1, and a request field, an index field, an answer status or a consumed document path can never drift between rwb-comms and rwb-document without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (ADR-020). The legacy key of RWB-E4-041 answers a court or an audit request from five tables of one schema — `notice`, `document`, `decision_log_entry`, `rule_row` and `template` — and from two notice endpoints that belong to another feature (legacy RWB-E4-041 Data and Endpoints). In the target that answer crosses one service boundary: the notice and its proof facts are rwb-comms', the document, its versions and its discovery production are rwb-document's, the decision entry is the local library's, and the screen reaches the answer through gateway-bff (Architecture v5 slides 17, 41 and 42; TSD P6 v2 T5.2; Ownership Map). Every one of those is a contract that another team builds against, so each one is fixed here before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_comms`, base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1` with retry and `.dlt` topics, event names `rwb.comms.<Event>.v1`, task queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that this capability publishes no event of the service: the catalogue has no document-request, custody or retention event, and the only element on a topic is the decision record of the library on the shared `rwb.decision-record.v1` (EV-08, Architecture v5 slide 42).

Three points are carried as gaps and assumptions rather than decided quietly. First, the documents, their version history and the court attributes of a produced document are rwb-document's under REQ-DCM-017 and REQ-DCM-018, and no published operation produces them, so the baseline names the discovery production as that service's obligation and reads the published document read meanwhile (GAP-1151; ASM-2098). Second, no source names a document-request operation, an answer shape or a decision code for it, so this baseline fixes them and marks the field-level detail (GAP-1152; ASM-2099). Third, REQ-DCM-017 asks for a named population and the legacy story asks per case, so the baseline fixes the per-case operation and leaves the population to rwb-document (GAP-1153; ASM-2100).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline; this document narrows them and never redefines them.
- The notice generation contract of this service is published, so the `notice` shape this baseline reads its index fields from has one owner document and the read is an additive use of it.
- The document read of rwb-document is published and stable enough to be faked: `/api/recovery/document/v1/documents/{documentId}` and its content operation. It is consumed here without a declared C row (GAP-1151; ASM-2098).
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided. The document rows are P5's, the case facts and the scope are P3's and P4's, the decision entry is P7's library and the screen is the platform route's.
- The roles of TSD P6 T6.1 are in force, and the capability area of both operations is Documents with right R, so an internal auditor and the compliance and PDPA officer answer through the same two operations as legal counsel.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive document of rwb-comms: the `DocumentRequest` and `DocumentRequestAnswer` resources, the 201 and the 200 answers, the four error responses and the Idempotency-Key on the POST, all under the base `/api/recovery/comms/v1`.
2. Fix the index entry of a notice from TSD P6 T3.1: the nine fields DF-LEG-015 to DF-LEG-023 in one row, with the note that a notice with no document keeps its row.
3. Fix the two request tables `document_request` and `document_request_entry`, their states, their indexes and the one transaction in which the decision record and the answer are written.
4. Fix the consumed rows: the document metadata and version list, the produced copy and the discovery production of rwb-document, each with its owner, its budget and its fake.
5. Record the decision-record element of DP-03 on `rwb.decision-record.v1`, its key and its payload, and record that this capability publishes no `rwb.comms` event.
6. Publish the nine contract tables of section 12 and the five contract fakes.
7. Add the contract tests: schema validation, the additive rule, the index field set, the closed request and state vocabulary, the consumed rows, the drift between a fake and the document, and the absence of a second base, a second topic and a cross-schema read.
8. Tag the baseline and hand it to RWB-P6-E4041-APP and to the rwb-document owner.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | Not specified in the source documents (GAP-1152; ASM-2099) | AC1 |
| X2 | A field of the answer is renamed or removed within major version 1 | The contract test fails the build; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | The discovery production of rwb-document has no path, request or answer | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document read | None | AC3 |
| X5 | The index entry field set of TSD P6 T3.1 changes | The contract test fails, because the nine fields are a closed set | None | AC2 |
| X6 | The document declares another service's operation as provided, or a second base or topic | The review and the absence test fail the baseline | None | AC5 |
| X7 | A request state outside the closed vocabulary reaches the store | The check constraint and the contract test both refuse it | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the notice contract of the same service and the Ownership Map only |
| Negotiable | The field-level detail of the request and answer, the document-side record and the decision code are settled with the owners and marked; the base, the operations, the index field set and the tables are fixed by this baseline |
| Valuable | Unblocks the app story of this legacy key on Day 1 and gives the rwb-document owner a named obligation to answer |
| Estimable | One document, two new tables, nine contract tables, five fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the document-request answer

  Background:
    Given the service naming rule of the platform library is in force
    Given the base of rwb-comms is "/api/recovery/comms/v1" and its topic is "rwb.comms.events.v1"
    Given the index fields of a notice are the nine fields DF-LEG-015 to DF-LEG-023 of TSD P6 T3.1

  Scenario: AC1 The two document-request operations are declared with their request and answer (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/document-requests with the DocumentRequestAnswer of status 201 and GET /document-requests/{requestId} with the same answer of status 200, both under the base /api/recovery/comms/v1 and owned by rwb-comms
    Then the DocumentRequest carries the request kind, the period asked for and the document types asked for
    Then the DocumentRequestAnswer carries the request id, the case id, the state, the answered at, the entries and the documents
    Then the POST declares the Idempotency-Key header and its stored answer, and the GET declares no Idempotency-Key
    Then both operations declare the capability area Documents with right R, their 2 s budget and the error responses 401, 403, 404, 422 and 503 with one envelope and one message ID per condition
    Then every added property is optional in the schema, so a consumer of the previous version keeps working
    Then the document marks that no source names a document-request operation, an answer shape or a decision code for it (GAP-1152; ASM-2099)

  Scenario: AC2 The index entry of a notice is a closed set of nine fields (new, D-RCV-60)
    Given the index entry section of the baseline
    When it is compared with TSD P6 T3.1 and TSD P6 T3.2
    Then the entry field set is exactly id, case_id, document_id, notice_type, sent_date, barcode, callback_date, delivery_status and sent_type with their BR Field IDs DF-LEG-015 to DF-LEG-023
    Then a notice with no document_id keeps its entry with an empty document reference and is never dropped from an answer
    Then notice_type and delivery_status are declared as LOV-NOTICE and LOV-DELIVERY, read with the version in force and never written as values of the contract
    Then no field of the entry carries personal data, and document.person_key is named as never selected
    Then the answer carries the produced documents as references and declares no file of a document in rwb_comms

  Scenario: AC3 The document read and the discovery production are declared as consumed, not provided (new, D-RCV-60)
    Given the consumed rows of section 12.2
    When they are compared with the Ownership Map and the appendix T-A.1 of TSD P6
    Then the document metadata and version list read, the produced copy read and the discovery production are declared as consumed from rwb-document (P5)
    Then the discovery production carries the placeholder because no source publishes a path, a request or an answer for it (GAP-1151; ASM-2098)
    Then the request is declared per case, as the path and the legacy story describe it, and a selector across cases is declared as rwb-document's (GAP-1153; ASM-2100)
    Then the court attributes of a produced document are declared as rwb-document's under REQ-DCM-018 and are not restated as fields this service certifies
    Then every consumed row is one hop with a 2 s budget, a retry rule and a breaker

  Scenario: AC4 The decision-record element and the absent events are declared (new, D-RCV-60)
    Given the event section of the baseline
    When it is reviewed against the event catalogue
    Then DecisionRecorded is declared on the shared rwb.decision-record.v1, keyed by caseId, written by the local library (DP-03)
    Then the baseline declares no event of rwb.comms for this capability, because the catalogue has none
    Then NoticeGenerated, NoticeDispatched and NoticeDelivered are named as the notice stories' and not as this capability's
    Then DocumentStored and DocumentFieldsExtracted are declared as not consumed by this service, because their consumers of the catalogue are rwb-agent and rwb-case
    Then no payload carries a name, an address, an identity number or an account number

  Scenario: AC5 The nine contract tables are complete and no cross-schema read is declared (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the tables named as owned are notice (read only), document_request, document_request_entry, the local decision record and the library objects, and document, document_type, recovery_case, decision_log_entry, rule_row, interaction and outbound_item are named as other owners' and consumed only through their contracts
    Then no read of a v_ace_ view, no second REST base and no second topic is declared, and the absence test fails a build that adds one
    Then the two new tables carry the standard record columns, their three indexes and the state check constraint of section 9
    Then the document marks that the field list of the two tables is fixed by this baseline (GAP-1152; ASM-2099)

  Scenario: AC6 The five contract fakes answer the document and the drift test binds them (new, D-RCV-60)
    Given the fakes of section 12.8
    When each is compared with the operation or the element it serves
    Then the rwb-document document fake answers the metadata and version list of a document of the case, and a delayed answer beyond 2 s
    Then the rwb-document content fake answers a produced copy and a copy that is not yet stored
    Then the rwb-document discovery fake answers the case with the placeholder rows of the discovery production
    Then the decision-record library stub answers a healthy chain and a stopped chain
    Then the notice fixture answers one notice with a document and one without
    Then the drift test compares every fake with the document and fails the build on any difference
```

These six criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-P6-E4041-APP and they copy no criterion of the legacy story; the legacy AC1 and AC2 stay with the app story. The two paths of AC1 are fixed by this baseline because no source names a document-request operation, and the gap and the assumption of the fix are cited on the criterion itself.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Architecture v5 slide 41 notes |
| BR2 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics; this capability declares no new event | Template and Rules §R4; Architecture v5 slide 42 |
| BR3 | Every element on a topic carries the CloudEvents 1.0 envelope and IDs, codes, dates and amounts only | Architecture v5 slides 42 and 43 notes; Template and Rules §R7.2 s17 |
| BR4 | A read declares no Idempotency-Key; a POST declares it and stores its answer | Architecture v5 slide 11 |
| BR5 | Error responses use one envelope and one message ID per condition; the business texts are copied unchanged from the legacy story where the legacy story has them | Template and Rules §R7.2 s14 |
| BR6 | A schema change is additive within a major version; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR7 | The document lists only operations owned by rwb-comms; the document read and the discovery production are described as consumed and faked | Ownership Map; DP-01 |
| BR8 | The index entry of a notice is the closed set of the TSD P6 T3.1 fields DF-LEG-015 to DF-LEG-023, and a notice with no document is kept | TSD P6 v2 T3.1 |
| BR9 | The request is per case; a named population across cases is rwb-document's and is not declared as an input of this operation | REQ-DCM-017; legacy RWB-E4-041 Endpoints (GAP-1153) |
| BR10 | The request and state vocabulary is closed, and an answer is stored as answered and read back unchanged | Legacy RWB-E4-041 AC1; DP-03 |
| BR11 | No business value is fixed in the contract: the decision code, the rule id, LOV-NOTICE and LOV-DELIVERY stay data or reference data | FSD P6 A2.20.3.1 BR-P6-020; Template and Rules §R7.2 s17 |
| BR12 | The decision record is the local library's entry on the shared topic and is never a new event of this service | DP-03; Architecture v5 slide 42 (event 08) |
| BR13 | The produced copy of a document is a claim-check reference; no file is declared in `rwb_comms` and no personal data is declared in an answer | Architecture v5 slides 42 and 43 notes; TSD P6 v2 T3.1 |
| BR14 | The legacy rows of this key that belong to notice generation — the screen SCR-33, the rule VR-P6-020-1 under R-LIT-04 and the two notice endpoints — are named as that feature's and copied into no criterion here | Legacy RWB-E4-041 Screen and states, Validation and messages, Endpoints (GAP-1154) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the index field set, the consumed rows and the tables are described | In review |
| In review | Consumer sign-off | The app story and the rwb-document, rwb-access and platform route owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a court attribute of a produced document | Baselined |
| Baselined | Breaking change | A field of the answer, a request state or an index field is removed, renamed or retyped | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A second base, a second topic or a cross-schema read is added | The absence test of AC5 fails | In review |

The states of a request that the document describes — OPENED and ANSWERED — are the app story's; this baseline fixes the vocabulary and the guards and moves no request.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows this baseline consumes |
| Consuming teams (the app story, the rwb-document owner, the platform route owner) | Review and sign off the parts they consume |
| Data steward | Confirms that no personal data field is declared in an answer, an entry or a fake, and that `document.person_key` is never selected |
| Legal counsel | Confirms that the index field set of an answer is the set a court or an auditor asks for (REQ-DCM-017, REQ-DCM-018) |

The per-service login name behind the security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Index entry | The nine fields of a notice with their BR Field IDs DF-LEG-015 to DF-LEG-023, read from `notice` and never written |
| Request | `document_request` with the standard record columns, the request kind, the period, the document types, the state and the answer reference; the field types are Not specified in the source documents (GAP-1152; ASM-2099) |
| Entry row | `document_request_entry` with the nine index fields, the document version, the origin, the entry date, the alteration flag and the readers; the document-side record is Not specified in the source documents (GAP-1151; ASM-2098) |
| Decision record | The local library's row in `rwb_comms` and its element on `rwb.decision-record.v1`; the decision code is Not specified in the source documents (GAP-1152; ASM-2099) |
| Answer payload | Ids, codes, types, dates and status codes only; no name, address, identity number, account number or personal key |
| Produced copy | A reference to the document version and the content operation of rwb-document; no file is declared in `rwb_comms` |

The two tables are fixed here because no source declares them: TSD P6 T3.1 has `notice`, `template`, `merge_field` and `signature_request` and no request table, and the legacy story holds the request in no table at all. The baseline fixes the names, the standard columns, the three indexes and the closed state vocabulary, and leaves the field types to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. No source names a document-request operation, so both paths, their status codes and their answer shape are fixed by this baseline (GAP-1152; ASM-2099).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/document-requests` | DocumentRequest in, DocumentRequestAnswer of status 201 out, with the entries and the documents of AC1 | Documents, right R, scope applied | Idempotency-Key header, answer stored for 24 hours |
| GET | `/document-requests/{requestId}` | DocumentRequestAnswer of status 200 out, with its entries and its documents exactly as answered | Documents, right R, scope applied | Not applicable |

Both operations answer 401, 403, 404, 503 and the POST also answers 422, each with the error envelope and one message ID of section 14.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The metadata, the extracted fields and the version list of a notice document, faked. Consumed without a declared C row (GAP-1151; ASM-2098) |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | P5 rwb-document | The produced copy of a document version as `application/octet-stream`, faked |
| POST | the discovery production of rwb-document | P5 rwb-document | Every document of the request with its metadata and version history (REQ-DCM-017) and the court attributes (REQ-DCM-018), faked. The path, the request and the answer are Not specified in the source documents (GAP-1151; ASM-2098) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. The selector of the third row is fixed per case on this side (BR9), and whether the discovery production can answer a population of more than one case is rwb-document's (GAP-1153; ASM-2100).

#### 12.3 Events published

| Event | Topic | Owner | Schema element |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, decision code, ruleId, ruleVersion, finalCall, decidedAt; the local library publishes it (DP-03) |

This baseline declares no event on `rwb.comms.events.v1` for this capability, because the catalogue has none (Architecture v5 slide 42). It declares the one element above and publishes none itself.

#### 12.4 Events consumed

None. No event of the catalogue names rwb-comms as its consumer for this capability: DocumentStored (EV-16) and DocumentFieldsExtracted (EV-17) are consumed by rwb-agent and rwb-case. The document read is synchronous and one hop, and this baseline fixes that and declares no inbox row for an event of this key.

#### 12.5 Workflows and activities

None. The answer is synchronous and the baseline fixes no workflow, no child workflow and no activity on task queue `rwb-comms`; the decision record is written through the library by the app story in its own transaction, not by an activity.

#### 12.6 Schedules

None. No job of the catalogue belongs to this capability (Architecture v5 slide 44): JOB-10 and JOB-11 are the notice and platform jobs and JOB-17 is rwb-document's. The baseline declares no quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The nine index fields of an answer, read only; written by the notice stories of this service |
| document_request | P6 (rwb_comms) | The request, its selector, its state and its answer reference; new in this baseline |
| document_request_entry | P6 (rwb_comms) | The frozen index entries and document lines of one answer; new in this baseline |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of an answer (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The envelope of the record element, the inbox of the app story and the POST idempotency |

`document`, `document_intake`, `document_text`, `document_field`, `document_type`, `document_custody`, `signature_request`, `retention_rule`, `retention_action` and `case_document_check` are P5's; `recovery_case`, `task`, `timer`, `queue` and `assignment` are P3's; `decision_log_entry`, `rule_row` and `approval` are P7's; `interaction` and `case_list_row` are P1's; `outbound_item` and `interface_config` are P2's; `deviation` is S8's. The contract names them only as consumed answers, and no foreign key crosses a service boundary.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document document WireMock | The metadata and version list of a document of case `RC-2026-000321`, a document of another case and a delayed answer beyond 2 s | App story, contract tests |
| rwb-document content WireMock | The produced copy of two versions and a copy that is not yet stored | App story, contract tests |
| rwb-document discovery WireMock | The discovery answer of the case with its placeholder rows and the court attributes | App story, contract tests |
| decision-record library stub | A healthy chain and outbox, and a stopped chain | App story, contract tests |
| rwb-comms notice fixture | Two notices of the case, one with a document and one without | App story, contract tests |

The discovery fake is stubbed from the published document read and carries the placeholder until the rwb-document owner publishes the operation (GAP-1151; ASM-2098).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The request-and-answer POST and the answer GET provided; the document metadata, the produced copy and the discovery production consumed; one hop, 2 s |
| Kafka | 1 declared as written by its owner, 0 published by this service, 0 consumed | DecisionRecorded on `rwb.decision-record.v1` |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | The produced copy is a claim-check read on the rwb-document content operation |

### 13. Solution plan

**Deliverables.** The change to `openapi/rwb-comms-v1.yaml` for this capability, the `DocumentRequest` and `DocumentRequestAnswer` components with the index entry and the document line, the two table definitions and their indexes in the physical schema note, the contract README rows for the state vocabulary and the consumed rows, and the five WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is not in the pattern set of this key: the baseline declares no table of another service and reads the document, its versions and its court attributes on the rwb-document contract only. DP-08 is not in the pattern set either: the capability area and the right are declared per operation and enforced at gateway-bff, and this baseline holds no role or scope table.

**Build steps**

1. Add the two operations and the two components to the document and validate the additive rule of AC1 in the pipeline.
2. Fix the index entry of AC2 with its nine BR Field IDs and the two list values.
3. Write the consumed rows of AC3 with the placeholder on the discovery production, and the per-case selector note.
4. Record the decision-record element and the absent events of AC4 and validate the element against the registry.
5. Record the two tables, their standard columns, their three indexes and their state constraint in the physical schema note, and the absence test for a cross-schema read, a second base and a second topic.
6. Publish the five fakes and the seven contract tests; a drift between a fake and the document fails the build.
7. Baseline tag and consumer sign-off, including the rwb-document owner, the platform route owner and the app story.

**Feature switch.** `rwb.comms.document-request`, declared as a parameter of the app story and not as a contract constant.

**Done when.** The document validates in the pipeline, the seven contract tests pass, the five fakes answer every consumed path and the drift test is green, and the app story and the rwb-document owner have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. |
| MSG-P6-003 | The template of a notice of the case was withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | A notice of the case was acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | A contact stop is in force on the case | Contact with this customer is stopped for {reason}. |

MSG-P7-003, MSG-P4-002, MSG-GEN-001, MSG-P6-003, MSG-P6-004 and MSG-P6-001 are the messages of the legacy story of RWB-E4-041, copied unchanged. The message IDs are contract elements; the legacy story gives no text for a schema failure, an absent request or a consumed call that does not answer in time, so those conditions carry the platform envelope and their text is Not specified in the source documents (GAP-1152; ASM-2099).

### 15. Screens and states

The contract serves the documents and litigation surfaces of the case through the gateway-bff composite route (DP-19) in the two request states OPENED and ANSWERED, and it serves the link to the produced copy of a document. The legacy screen SCR-33 Template approval is not that screen and the baseline names it as the notice feature's (GAP-1154; ASM-2101). The route calls rwb-comms for the answer and rwb-document for the produced copy; this baseline fixes the rwb-comms answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-041-01 | AC1 of the app story, BR8 | End to end | Case `RC-2026-000321` with notices `N-0101` and `N-0102`; the contract half answers the index field set of AC2 and the answer shape of AC1 |
| TC-E4-041-02 | AC2 of the app story, BR12 | End to end | The library stub returns a stopped chain; the contract half answers the stopped chain of AC6 |
| TC-E4-041-03 | Access, BR7 | Component | A caller without the Documents right on the case; the contract half answers the 403 of AC1 |
| TC-E4-041-04 | Principle 5, BR3 | NFR | The decision log write forced to fail on ten answers; the contract half answers the store constraint of AC5 |
| TC-P6-E4041-CON-01 | AC1 | Contract | The document validates; the two operations, the request and answer properties, the Idempotency-Key rule and the five error responses are present |
| TC-P6-E4041-CON-02 | AC2 | Contract | The nine index fields with their BR Field IDs, the two list values and the notice with no document |
| TC-P6-E4041-CON-03 | AC3 | Contract | The three consumed rows with their owners, the placeholder on the discovery production and the per-case selector |
| TC-P6-E4041-CON-04 | AC4 | Contract | The decision-record element validates against the registry; no `rwb.comms` event of this capability; no personal data field |
| TC-P6-E4041-CON-05 | AC5 | Contract | The nine sub-tables present with owners; the two new tables, their indexes and their constraint; the absence test |
| TC-P6-E4041-CON-06 | AC6 | Component | The five fakes match the document; a drifted fake fails the build |

The four legacy cases keep their legacy order, their legacy level mapping (System to End to end, Access to Component, Principle 5 to NFR) and their legacy data; the six contract cases test the artefact and are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the decision code, the rule id, the request kinds and the list values stay data or reference data.
- No personal data in a schema, an example or a fake: ids, codes, types, dates and status codes only, and `document.person_key` is named as never selected.
- The contract names only rwb-comms tables and only operations owned by rwb-comms; the document read and the discovery production are consumed and faked, never declared as provided.
- One base, one topic and one queue per service; a document that names another service's base or topic as its own fails the review.
- ACE data is reached only through the owner's contract or the owner's `v_ace_*` views; this document declares no ACE view and no cross-schema join.
- No retired or invented element: the catalogue has no document-request event and none is declared, and the absence test fails a build that adds a second base, a second topic or a shared job table.
- Every example in the document is synthetic; no production payload and no production file is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-017 | An electronic discovery request produces every document for a named population with its metadata and its version history | The consumed discovery production of 12.2 and the version list of the document line in AC1 | TC-P6-E4041-CON-01, TC-P6-E4041-CON-03 |
| REQ-DCM-018 | A produced document carries its origin, its entry date, its alteration flag and its readers | The court attributes of the document line, declared as rwb-document's | TC-P6-E4041-CON-01, TC-P6-E4041-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-P6-E4041-CON-01, TC-P6-E4041-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-041, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned by RWB-P6-E4041-APP; this baseline copies none of them |
| Test cases | The four legacy cases as the evidence the contract serves, and the six new contract cases TC-P6-E4041-CON-01 to -06 |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |

### 19. Out of scope

- The implementation of the two operations, the index assembler, the document adapter and the fail-closed path (RWB-P6-E4041-APP).
- The document, its custody, its OCR text, its fields, its versions, its discovery production and the court attributes of a produced document (P5 rwb-document; REQ-DCM-017, REQ-DCM-018, REQ-DCM-020). This baseline names them as consumed and fixes no part of them.
- The notice generation, the dispatch and the proof-of-delivery contract of this service: the notice contracts of rwb-comms.
- The template catalogue and the withdrawn-template path of R-LIT-04 and R-LIT-06: the template contracts of rwb-comms. The legacy rule VR-P6-020-1 belongs to that path.
- The retention and legal hold contract of this key (RWB-P6-E4042-CON) and the retention tables of rwb-document.
- The case, the scope, the roles and the masking: rwb-case, rwb-access and gateway-bff, with RWB-PLT-N001-CON.
- The screen of the request and of the answer and its field list: RWB-PLT-N001-CON. The legacy SCR-33 is not that screen.
- The discovery of a population across cases and any export or archive file of an answer: no operation of this baseline declares them (GAP-1153; ASM-2100; GAP-1155; ASM-2102).
- The cross-service journey and its evidence: no integration story of this baseline covers it.

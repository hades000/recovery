# RWB-P6-E2022-CON SMS and LINE dispatch through NSS and LINE OA

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Contract version | v1 (base path /api/recovery/comms/v1 in AC1) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-P6-E2022-CON-14) |
| Size | Not specified in the source documents (DOR-RWB-P6-E2022-CON-16) |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None published; the S2 rwb-treatment and P1 rwb-source-data reads and the S8 deviation events are built against fakes derived from the published documents and the Ownership Map, held by the drift test of RWB-P6-E4035-CON |
| Integration dependencies | ACE Common notification path for SMS and LINE; DL30 open until ACE confirms |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-010, FR-P6-017, FR-P6-018, FR-P6-020, FR-P6-022, FR-P6-023, FR-P6-024, FR-P6-025, FR-P6-026, FR-P6-027, FR-P6-028, FR-P6-029, FR-P6-030, FR-P6-031, FR-P6-036) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2022-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 18 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Tribe lead and squad members (RW-TRIBE)**, I want **the published contract baseline of the message-dispatch operation of rwb-comms — `POST /api/recovery/comms/v1/cases/{caseId}/messages` with its `MessageRequest`, its 202 `Interaction` answer, its refusal envelope, its delivery status list, its Idempotency-Key answer, its decision-record and event envelopes and its contract fakes — together with the consumed contact-point, case, reference-data and deviation shapes of their owners**, so that **the app, operations and integration stories of this legacy key build against a fixed, testable contract on Day 1, and a field rename, a status value or a message ID can never drift between rwb-comms, rwb-source-data, rwb-case, rwb-deviation and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The capability of RWB-E2-022 answers one request and then waits for another system to answer twice: the send is accepted with a reference, and the delivery arrives later as a result for that reference. That is the part most likely to drift silently. A renamed `conductCheck` value, a status the reader does not know, or a 409 whose message ID changes from MSG-P6-001 to MSG-P6-002 would not fail a build; it would show the wrong reason on SCR-03 and record the wrong refusal in the central decision ledger.

The baseline also fixes the naming the checks require: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1`, queue `rwb-comms` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.comms`. It records that this capability publishes no new `rwb.comms.*` event — Architecture v5 slide 17 names only `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`, and a message is not a notice — and that its one published event is `DecisionRecorded` on the shared `rwb.decision-record.v1` (DP-03).

Three things stay deliberately open in this baseline and are carried as non-blocking dependencies: the shapes of the ACE notification path (INT-17, INT-18), the operation names of the P1 contact point and failed-count element, and whether the case facts arrive through the case read or the authorise answer. Each is faked, each is tagged, and each is replaced by its owner as the wave 2 stories land.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the document, topic and event names follow the platform rule rather than a local choice.
- The platform error envelope, the CloudEvents 1.0 envelope and the retry and `.dlt` topic convention are the platform baseline (RWB-PLT-EVT, RWB-PLT-TE006-CON); where this document narrows them it does so explicitly.
- The template catalog contract of rwb-comms (`RWB-P6-E1046-CON`) is published, so the template reference a message names has one owner document.
- The notice contract of rwb-comms (`RWB-P6-E1052-CON`) is published, so this document can state that a message produces no notice and adds nothing to the notice resource.
- The operations and their owners are taken from the Ownership Map only; this document never declares another service's operation as provided.
- The ACE notification path request and result shapes are Not specified in the source documents (GAP-1069; ASM-2017), so the two call shapes of 12.4 are stated as placeholders and carried by the fake of 12.8.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additive change to the rwb-comms OpenAPI 3.1 document: the `POST /cases/{caseId}/messages` operation, the `MessageRequest` schema and the `Interaction` schema.
2. Fix the one answer the operation returns and the seven refusal conditions, each with its status code and its message ID, including the two that gateway-bff answers before the call.
3. Fix the delivery status list of a message and state that it is not LOV-DELIVERY, which stays the WIN proof-of-delivery list.
4. State the Idempotency-Key rule: the key is required on the POST, the answer is stored, and a repeated key returns the first answer without a second send.
5. Record the consumed operations with their owner, their use and the 2 s budget, and map every failure of a consumed call to the envelope and a message ID or to a refusal closed.
6. Record the event elements: `DecisionRecorded` on the shared topic as the only published element, the three consumed events, and the statement that no new comms event is declared.
7. Record the absence of a workflow and of a Schedule, because the retry is the platform outbox relay JOB-11 and this capability registers neither.
8. Publish the nine contract tables of section 12 and the four contract fakes, then the contract tests: schema validation, the refusal matrix, the status list, the idempotency answer, the drift between a fake and the document, and the absence of a new comms event.
9. Tag the baseline and hand it to RWB-P6-E2022-APP, RWB-P6-E2022-OPS and the wave 2 harness RWB-ITG-E2022-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body fails schema validation | The build fails on the schema lint; a deployed service answers 500 with the error envelope | MSG-GEN-001 | AC1 |
| X2 | A field is renamed, removed or retyped within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC9 |
| X4 | A delivery status outside the list arrives from the ACE notification path | The result is not applied and the document is the reference; a new value needs an additive change and the path owner's agreement | None | AC6 |
| X5 | The ACE notification path publishes no shape | The two call shapes stay placeholders, carried by the fake and by the gap; the baseline is still published | None | AC4, AC5 |
| X6 | A consumed contract names no operation for the element rwb-comms needs | The row carries the gap and the assumption and the fake is derived from the owner's published document | None | AC8 |
| X7 | The document declares a new `rwb.comms.*` event for a message | The absence test fails: the only publisher of that topic is the notice capability | None | AC8 |
| X8 | The document declares a Schedule or a workflow for the retry | The absence test fails: the retry is the platform relay JOB-11 | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the two same-service contracts it extends and the Ownership Map only |
| Negotiable | Field-level lengths and optionality are settled with the consumers; the operation, the seven refusal conditions, the status list and the event statement are fixed by the target architecture |
| Valuable | Unblocks the app, operations and integration stories of this legacy key on Day 1 and every consumer of the message and its delivery status |
| Estimable | One document, three schemas, four consumed rows, nine contract tables, four fakes and seven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of SMS and LINE dispatch through NSS and LINE OA

  Background:
    Given the service naming rule of the platform library is in force
    Given the rwb-comms event types are NoticeGenerated, NoticeDispatched and NoticeDelivered
    Given the template catalog contract RWB-P6-E1046-CON is published with the Template resource

  Scenario: AC1 The send operation is declared with its request (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-comms is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/messages under the base /api/recovery/comms/v1, owned by rwb-comms, with API ID API-P6-008
    Then the request schema MessageRequest carries channel with the values "SMS" and "LINE" and channel is required, templateCode which is required, language with the values "TH" and "EN" defaulting to "TH", and partyId defaulting to the borrower
    Then the operation declares its security right as Case record C with the scope applied, the Idempotency-Key header and the error responses 401, 403, 404, 409, 422 and 503
    Then the field-level lengths and the optionality beyond the legacy statement are Not specified in the source documents (GAP-1073; ASM-2021)

  Scenario: AC2 The 202 answer is the interaction (new, D-RCV-60)
    Given the answer schema Interaction declared in the document
    When it is compared with the fields the legacy request and answer table names
    Then it carries id, caseId, partyId, occurredAt, channel, direction, conductCheck, summary, sourceSystem, deliveryStatus and externalRef
    Then channel takes the values "SMS" and "LINE", direction takes "OUTBOUND", and conductCheck takes "PASSED" and "BLOCKED"
    Then externalRef is empty in the answer of a send that is still queued and carries the accepted reference once the ACE notification path has answered
    Then the answer carries no phone number, no LINE identifier and no message body: the contact point is a token and summary holds IDs and facts only
    Then the document states that a message has no read operation in this module, so the answer of the POST is the only representation this contract publishes

  Scenario: AC3 The refusal envelope fixes every condition and its message ID (new, D-RCV-60)
    Given the error responses of the operation
    When each condition is compared with the message standard of section 14
    Then a contact stop answers 409 with MSG-P6-001, missing consent on the channel answers 409 with MSG-P6-002, a withdrawn template answers 409 with MSG-P6-003 and a legal hold answers 409 with MSG-P3-004
    Then a missing channel or template answers 422 with MSG-GEN-001 naming the field
    Then a decision record that cannot be written answers 503 with MSG-P7-003
    Then a role without Case record C answers 403 with MSG-P4-002 and a case outside the scope answers 404 with MSG-P4-003, both declared as answered before the call on the gateway-bff route
    Then no request without a session reaches the operation, and 401 carries no message ID of this module

  Scenario: AC4 The NSS call shape through the ACE notification path is fixed where the sources name it (new, D-RCV-60)
    Given the send request rwb-comms makes for channel "SMS"
    When the call shape is compared with TSD P6 T5.1 and Architecture v5 slide 17
    Then the document states one outbound REST call to the ACE notification path (INT-17) and no call to NSS directly
    Then the request carries a contact point token, the template reference, the language and the case reference, and no phone number
    Then the result carries an accepted reference and one NSS result code
    Then the result-code map from the NSS code to "SENT", "DELIVERED" and "FAILED" is data and not part of this schema
    Then the endpoint, the field names and the accepted-reference format are Not specified in the source documents (GAP-1069; ASM-2017)

  Scenario: AC5 The LINE OA call shape through the ACE notification path is fixed where the sources name it (new, D-RCV-60)
    Given the send request rwb-comms makes for channel "LINE"
    When the call shape is compared with TSD P6 T5.1 and Architecture v5 slide 17
    Then the document states one outbound REST call to the ACE notification path (INT-18) and no call to LINE OA directly
    Then the request carries a contact point token, the template reference, the language and the case reference, and no LINE identifier
    Then the result carries an accepted reference, then "DELIVERED", then "READ"
    Then how the second status reaches rwb-comms — a callback or a poll of the path — is Not specified in the source documents (GAP-1072; ASM-2020)

  Scenario: AC6 The delivery status list is fixed and is not LOV-DELIVERY (new, D-RCV-60)
    Given the deliveryStatus property of the Interaction schema
    When it is compared with the legacy story and with TSD P6 T3.2
    Then it takes "SENT" before the result, "DELIVERED" and "FAILED" from either channel, and "READ" for LINE
    Then the document states that the list is the message list of this capability and that LOV-DELIVERY keeps the WIN proof-of-delivery values "DELIVERED", "REFUSED", "UNDELIVERABLE" and "PENDING" and is not extended by this story
    Then the value "READ" is declared for channel "LINE" only, and a status outside the list is not applied
    Then the list is closed in this contract: a new value is a change to this contract, not a data row of LOV-DELIVERY, and the closed enum of rwb-comms stands

  Scenario: AC7 The Idempotency-Key answer is declared (new, D-RCV-60)
    Given the Idempotency-Key header declared on the POST
    When the declared behaviour is reviewed
    Then the key is required on the POST and a request without it is refused
    Then the stored answer of the key is returned for a repeated request with the same key, with the same status and body, and no second message leaves for the ACE notification path
    Then the document states that the same request with a different key is a new send and not a repeat

  Scenario: AC8 The event and workflow elements are recorded, and the absent ones named (new, D-RCV-60)
    Given the event section of the document
    When it is reviewed against the event catalogue
    Then rwb.decision.DecisionRecorded.v1 is declared as published on rwb.decision-record.v1 through the local decision-record library, keyed by caseId and carrying the decision code, the final call and the reference, with no personal data
    Then rwb.deviation.DeviationRaised.v1, rwb.deviation.DeviationCleared.v1 and rwb.case.CaseStateChanged.v1 are declared as consumed, each with its owner and its key caseId
    Then the document declares no new rwb.comms.* event for a message, because the topic carries only NoticeGenerated, NoticeDispatched and NoticeDelivered
    Then the document declares no workflow and no Schedule, and names JOB-11 Outbox sender as the platform's every-minute relay (GAP-1071; ASM-2019)

  Scenario: AC9 The nine contract tables are complete and the fakes match them (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then 12.6 records None and names JOB-11 as the platform's
    Then the four fakes answer the consumed shapes of 12.2 and the answer, the refusal matrix and the status list of 12.1
    Then the contract tests compare each fake with the document and fail on any drift
```

These nine criteria are new for the contract baseline and test the artefact only; they restate no business outcome owned by RWB-P6-E2022-APP or RWB-ITG-E2022-ITG. The wave 2 harness `RWB-ITG-E2022-ITG` consumes this baseline and copies none of these criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every outbound message carries a conduct check result on its ledger entry | REQ-OCC-005; FEAT-OCC-05 |
| BR2 | No message is sent while a contact stop is in force | CTL-16; R-UNI-04, R-UNI-05 |
| BR3 | Deviation codes that block SMS and LINE are a reference list; X6 blocks both until a contact point is verified | R-DEV-16; R-UNI-12; Principle 1 |
| BR4 | Messages go only to a verified contact point with consent GIVEN for that channel | CTL-17; R-UNI-10 |
| BR5 | A legal hold stops every outbound action | R-UNI-20 |
| BR6 | A system that is unavailable queues the send and retries through the platform outbox retry mechanism (JOB-11 in Architecture v5, owned by the platform); after the attempt limit of three retries (held as platform configuration under BR15) it goes to the exception queue | R-UNI-33, R-UNI-34, R-UNI-36; NFR-026; Architecture v5 slide 44 |
| BR7 | A refusal that cannot be written to the decision log is not completed | Principle 5; R-UNI-39 |
| BR8 | Only the current Approved template for the channel is used | R-LIT-03; CTL-14 |
| BR9 | The same request twice sends one message | R-UNI-40 |
| BR10 | A message raised by a route rule — the offer letter of R-RES-09 — is outside this contract; this operation answers only a person's request | R-RES-09; legacy section 19 |
| BR11 | One REST base per service: `/api/recovery/comms/v1`; the document never declares another service's path as provided | DP-13; Template and Rules §R4 |
| BR12 | Event names are `rwb.<short>.<Event>.v1` on the topic `rwb.<short>.events.v1`, with retry and `.dlt` topics; the one published element of this capability is `DecisionRecorded` on the shared topic | DP-03, DP-14; Architecture v5 slides 17 and 42 |
| BR13 | A read declares no Idempotency-Key; a POST declares it and stores its response | Architecture v5 slide 11; DP-09 |
| BR14 | A schema change is additive within a major version; a breaking change is a new major version, and the delivery status list is SENT, DELIVERED, FAILED and READ, closed unless it changes additively with the path owner's agreement; LOV-DELIVERY is unchanged | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR15 | No business value is fixed in the contract: the blocking deviation codes, the result-code maps, the attempt limit and the templates stay data | Template and Rules §R7.2 s17 |
| BR16 | No personal data is declared in a schema, an example or a fake: the contact point is a token, and the message body and the addressee are never in a payload | Template and Rules §R7.2 s17; legacy section 17 |

The conduct check of BR1 and the consent rule of BR4 are evaluated from one versioned rule package, the conduct and consent rule package, governed in rwb-decision and run in this service; the conduct and QA officer approves its first version.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the three schemas, the refusal matrix and the status list are described | In review |
| In review | Consumer sign-off | The app, operations and integration stories and the P1, P3, S8 and P7 owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A field is added within major version 1, for example a new template reference | Baselined |
| Baselined | Breaking change | A field is removed, renamed or retyped, or a published status value changes meaning | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A new comms event or a Schedule is declared | The absence test of AC8 fails | In review |

The message lifecycle itself — QUEUED, SENT, DELIVERED, READ, FAILED, EXCEPTION — is owned by RWB-P6-E2022-APP and is described there; this baseline fixes only the status values and the answer shapes it declares.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-comms | Owns the OpenAPI and AsyncAPI documents and the fakes; tags the baseline |
| Solution architect | Approves a breaking change, a new major version and the resolution of the ACE notification path gap |
| Consuming teams (app, operations, integration, and the rwb-source-data, rwb-case, rwb-deviation and rwb-decision owners) | Review and sign off the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the Idempotency-Key rule and the naming rule this document reuses |
| Data steward | Confirms that no personal data field is declared in an event, an answer or an example, and owns the NSS and LINE OA result-code maps |

The Case record right C the operation applies is declared by the operation itself. TSD P6 T6.1 is the only source for the letters, and DP-08 is not in the pattern set of this legacy key, so the declaration of the right sits at gateway-bff and the reconciliation is carried by GAP-1075 and ASM-2023. The per-service login name behind the document's security scheme is not part of this baseline; the document names the scheme "the rwb-comms login (DP-02)".

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| `MessageRequest` | `channel` with the values SMS and LINE and required, `templateCode` required, `language` with TH and EN and default TH, `partyId` defaulting to the borrower; the legacy names these four and no others | Not specified in the source documents (DOR-RWB-P6-E2022-CON-7) |
| `Interaction` | `id`, `caseId`, `partyId`, `occurredAt`, `channel`, `direction`, `conductCheck`, `summary`, `sourceSystem`, `deliveryStatus`, `externalRef` | Not specified in the source documents (DOR-RWB-P6-E2022-CON-7) |
| `conductCheck` | `PASSED` and `BLOCKED` | Not specified in the source documents (DOR-RWB-P6-E2022-CON-7) |
| `deliveryStatus` | `SENT`, `DELIVERED`, `FAILED` and, for LINE, `READ`; explicitly not LOV-DELIVERY | Not specified in the source documents (DOR-RWB-P6-E2022-CON-7) |
| Event payloads | IDs, codes, dates and counts only; no name, no phone number, no LINE identifier, no message body and no addressee | Not specified in the source documents (DOR-RWB-P6-E2022-CON-7) |
| Idempotency | The key of the POST and the stored answer, in `idempotency_key` of schema `rwb_comms` | Not specified in the source documents (DOR-RWB-P6-E2022-CON-7) |

The field-level types, lengths and required flags beyond the legacy statement are settled in the baseline review and are Not specified in the source documents (GAP-1073; ASM-2021); this story fixes the names, the two closed value lists and the one allowed answer of the POST.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/messages` | API-P6-008 | `MessageRequest` → 202 `Interaction`; the seven refusal conditions of AC3 | Case record C, scope applied | Idempotency-Key header, response stored |

The document declares no read operation for a message: the API specification of this module lists API-P6-001 to API-P6-011 only, and the message and its status are read through the P1 interaction on the case timeline route (GAP-1070; ASM-2018).

#### 12.2 REST operations consumed

| Call | Owner | Use in the baseline |
|---|---|---|
| Contact point of a party for a channel — the operation named in RWB-P1-E1066-CON | P1 rwb-source-data | The contact type, the token, consent GIVEN and the verified flag; faked. The operation name and its fields are Not specified in the source documents (GAP-1070; ASM-2018) |
| Record a failed contact — the operation named in RWB-P1-E1066-CON | P1 rwb-source-data | The failed count after a FAILED result; faked, and the element is not named in the published contract (GAP-1070) |
| `GET /api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The legal hold and the deviation flag; faked. Not in this key's Contract dependencies (GAP-1075) |
| Reference data for LOV-CHANNEL — the contract of RWB-P3-E1043-CON | P3 rwb-case | `SMS` and `LINE` as data rows (DP-07); faked |
| `GET /api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | The open deviation with its contact stop and its code; faked only |

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). The refusal's decision record is a write through the local decision-record library (DP-03), listed in 12.3 and not in this table.

#### 12.3 Events published

| Event | Topic | Owner of the type | Schema element |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | P7 rwb-decision | decision record reference, the decision code (the deviation code on a refusal), the final call, the case ID, the decided-at time, the rule and its version where one applied; no personal data; written by the local library in the same transaction and relayed by the outbox |

New `rwb.comms.*` events for this capability: None. `rwb.comms.events.v1` carries `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` and nothing else in this story, because a message is not a notice (Architecture v5 slide 17).

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviation code, raised at, contact stop flag; keeps the blocking list current when the case read degrades |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | caseId, deviation code, cleared at, outcome; releases the block |
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | caseId, previous and new state, changed at; the consumer group of `rwb-comms` keeps the case projection the conduct check reads |

Each subscription has its retry topic and its `.dlt` topic, and the consumer dedupes through `processed_event` in schema `rwb_comms` (DP-09).

#### 12.5 Workflows and activities

None. The send is a synchronous REST request whose durability is the outbox row; this baseline registers no workflow, no activity and no child workflow on task queue `rwb-comms`.

#### 12.6 Schedules

None. JOB-11 Outbox sender is the platform's outbox relay, every minute, with every service as its owner (Architecture v5 slide 44). The legacy story called the same job the sender to the ACE notification path with a retry limit of 5, and the reconciliation of the two readings is carried by GAP-1071 and ASM-2019; this baseline registers no Schedule, no cron entry and no job name.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (rwb_comms) | The current Approved version for a channel and a language |
| notice | P6 (rwb_comms) | Not written for a message: a message produces no notice |
| merge_field | P6 (rwb_comms) | The merge codes the template may use |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_comms | The send request, the inbox of the three consumed events and the stored answer of the POST |

`interaction` and `contact_point_ext` are P1's, `recovery_case` and `task` are P3's, `deviation` is S8's and `decision_log_entry` is P7's; the contract names them only as consumed answers (DP-01, DP-18).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data WireMock | The verified `MOBILE` contact point of `P-0077` with consent `GIVEN` and failed count 0, the `MOBILE` contact point with consent `WITHDRAWN` for the 409 of MSG-P6-002, the verified `LINE` contact point, the accepted failed-count update and a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-case WireMock | `GET /cases/{caseId}` for `RC-2026-000777` with legal hold false, then true; a case outside the scope; a delayed answer beyond 2 s | App story, operations smoke profile, contract tests |
| rwb-deviation WireMock | The open deviation `X1` with contact stop on, the open deviation `X6`, an empty answer and a delayed answer beyond 2 s | App story, contract tests |
| ACE notification path stub | An accepted reference `NSS-7781` with `DELIVERED`, a `FAILED` result, the LINE `DELIVERED` then `READ`, and `unavailable` for six attempts; the NSS and LINE OA result-code maps as data | App story, operations smoke profile, integration harness |

The exact shapes of the ACE notification path and of the P1 contact-point and failed-count elements are Not specified in the source documents (GAP-1069, GAP-1070; ASM-2017, ASM-2018); every fake is derived from the owner's published document or from the legacy interface name, and is replaced by the real service as its story lands.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The send operation provided; the contact point, the failed-count update, the case, the reference data and the deviation read consumed; one hop, 2 s |
| Kafka | 1 declared as published by its owner, 3 consumed | `DecisionRecorded` on the shared topic; `DeviationRaised`, `DeviationCleared` and `CaseStateChanged`; no new comms event |
| Temporal | None | No workflow, no activity and no Schedule; JOB-11 is the platform relay |
| File | None | No file in this contract |

### 13. Solution plan

**Deliverables.** The additive change to `openapi/rwb-comms-v1.yaml`, the `MessageRequest` and `Interaction` schemas with the two closed value lists, the AsyncAPI fragment of `rwb.comms.events.v1` that confirms `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` and adds nothing, the contract README rows for the refusal matrix, the Idempotency-Key rule, the status list and the absent elements, and the four WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-19 is claimed because the operation is reached through the gateway-bff route behind SCR-03 and the two refusals of the route are declared here; DP-10 only because the retry path is JOB-11 and no Schedule is registered.

**Build steps**

1. Add the operation, the `MessageRequest` schema and the two closed value lists; validate the additive rule in the pipeline.
2. Write the `Interaction` schema and the rule that the answer is the only representation of a message this module publishes.
3. Write the refusal matrix as a schema constraint and a README row, one condition to one status and one message ID, including the two answered at gateway-bff.
4. Record the Idempotency-Key rule and the stored answer.
5. Record the five consumed rows with their owner, their budget and the two gap rows.
6. Record the event rows and the absent elements, and add the absence test for a new comms event, a Schedule and a workflow.
7. Publish the four fakes and the seven contract tests; a drift between a fake and the document fails the build.
8. Baseline tag and the consumer sign-off note, including the P1, P3, S8 and P7 owners and the wave 2 harness.

**Done when.** The OpenAPI and AsyncAPI artefacts validate in the pipeline, the seven contract tests pass, the four fakes answer every consumed shape and the drift test is green, and the app, operations and integration stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | The role lacks Case record C on the route | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Channel or template missing | Enter {field}. |
| MSG-GEN-006 | NSS or LINE OA is unavailable | {system} is not available. Your request is queued and will be retried. |

The message IDs are contract elements; the text is the agreed text taken unchanged from the legacy story, and the {system} value of MSG-GEN-006 is fixed by the consumed row that failed.

### 15. Screens and states

The contract serves the Send message action of SCR-03 Case record in its editable and refused states, the message row of SCR-04 Case timeline in its Loading and filtered states, and the send row of SCR-09 Exception queue, all through the gateway-bff composite route (DP-19). Screen states: SCR-03 Case record: editable, refused, loading (as held in Screen Specifications v1 SCR-03), empty, error and no access: Not specified in the source documents (CG-ALL-6603). SCR-04 Case timeline: Loading and filtered, empty, error and no access: Not specified in the source documents (CG-ALL-6604). SCR-09 Exception queue: loading (as held in Screen Specifications v1 SCR-09), empty, error and no access: Not specified in the source documents (CG-ALL-6605). This baseline fixes the operation's request and answer and the refusal matrix only; the screen field list, the composite route specification and the masking of the contact point belong to RWB-PLT-N001-CON and to RWB-P6-E1052-CON's screen stories.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC1, AC2, AC3 | Contract | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781 |
| TC-E2-022-02 | AC2, AC5, AC6 | Contract | P-0077 LINE consent GIVEN; LINE OA stub delivered and read |
| TC-E2-022-03 | AC3, AC6 | Contract | Open X6; the MSG-P6-001 answer |
| TC-E2-022-04 | AC3, AC6 | Contract | Open X1 with contact stop; the MSG-P6-001 answer |
| TC-E2-022-05 | AC3 | Contract | MOBILE consent WITHDRAWN; the MSG-P6-002 answer |
| TC-E2-022-06 | AC3 | Contract | SMS-REMIND TH v1 Withdrawn; the MSG-P6-003 answer |
| TC-E2-022-07 | AC4, AC8 | Contract | Notification path stub unavailable for 6 attempts |
| TC-E2-022-08 | AC2, AC4, AC6 | Contract | NSS result FAILED, failed count 0 |
| TC-E2-022-09 | AC7 | Contract | Same Idempotency-Key twice |
| TC-E2-022-10 | AC3 | Contract | Open X6; decision log stubbed unavailable; the MSG-P7-003 answer |
| TC-E2-022-11 | AC3 | Contract | Legal hold true; the MSG-P3-004 answer |
| TC-E2-022-12 | AC1, AC3 | Contract | No channel; the MSG-GEN-001 answer |
| TC-E2-022-13 | AC3 | Component | RW-PHONECOL sends POST /cases/{caseId}/messages; refused with MSG-P4-002 |
| TC-E2-022-14 | AC3, AC8 | NFR | Decision log write forced to fail on 10 refusals; none recorded as sent |
| TC-E2-022-15 | AC9 | Contract | Four fakes compared with 12.1 and 12.2; a drifted field fails the contract test |
| TC-E2-022-16 | AC9 | Contract | Boundary: each table of 12.7 checked against its owner in the Ownership Map |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to Contract on this baseline and to End to end on RWB-P6-E2022-APP and RWB-ITG-E2022-ITG, Access to Component and Resilience to NFR. The fourteen cases are kept in their legacy order because they exercise the document of this story; the `-ITG` copies belong to the integration story. TC-E2-022-15 and TC-E2-022-16 are added for AC9 in this baseline; the fourteen legacy cases are unchanged.

### 17. Guardrails

- No business value in the contract: the blocking deviation codes, the result-code maps, the attempt limit, the templates and the languages stay data, reference data or service configuration.
- No personal data in a schema, an example or a fake: the contact point is a token, the message body and the addressee are never in a payload, and no name, address or identity number is declared.
- The contract names only rwb-comms tables and only the one operation owned by rwb-comms; the P1, P3, S8 and P7 elements are consumed and faked, never declared as provided (DP-01).
- One REST base and one topic per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- No new comms event is declared for a message, and no absence test is relaxed: a release that adds one fails the build.
- No Schedule and no workflow is declared: the retry is the platform relay JOB-11, and the message lifecycle is the outbox row.
- Every example in the document is synthetic; no production payload is copied into a schema or a fake.
- The error envelope, the CloudEvents envelope, the Idempotency-Key rule and the naming rule come from the platform library; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-004 | SMS and LINE through the bank's channel platforms, result on the case | The send operation, the `MessageRequest` and the `Interaction` answer | TC-E2-022-01, TC-E2-022-02, TC-E2-022-07, TC-E2-022-08, TC-E2-022-09, TC-E2-022-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | `conductCheck` values and the `BLOCKED` refusal matrix | TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11, TC-E2-022-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel | The MSG-P6-002 answer on the consent read of the P1 contract | TC-E2-022-05 |
| REQ-ILG-010 | Messages dispatched write their result to the ledger | `deliveryStatus` and `externalRef` on the answer, and the `DecisionRecorded` element | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08 |
| REQ-DRI-006 | No direct call to NSS or LINE OA; only the ACE notification path | The two call shapes of AC4 and AC5 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-07 |
| RWB-E2-022 | The legacy key this baseline contracts, with all fourteen legacy cases kept in section 16 | The operation and the four fakes | All fourteen cases |
| DP set | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 | The nine contract tables | TC-E2-022-01, TC-E2-022-08, TC-E2-022-09, TC-E2-022-15, TC-E2-022-16 |
| ADR-013 | 19 services inside ACE | The one operation of this service and its own schema | TC-E2-022-01 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | The rwb-comms login of the security scheme | TC-E2-022-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The three consumed rows and the `DecisionRecorded` row | TC-E2-022-08 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-E2-022-01, TC-E2-022-13 |

### 19. Out of scope

- The implementation of the operation, the conduct check, the outbox row and the result mapping (RWB-P6-E2022-APP).
- The deployment, the egress, the retry worker, the dashboards, the alerts and the runbook (RWB-P6-E2022-OPS).
- The cross-service journey and its evidence (RWB-ITG-E2022-ITG).
- The notice capability and the template catalog that this document references (RWB-P6-E1052-CON, RWB-P6-E1046-CON).
- The letter capability that shares the conduct check (RWB-P6-E2021-CON).
- The ACE notification path contract itself: consumed and faked, never defined here; its owner publishes it (GAP-1069).
- The P1 contact-point, consent and failed-count contract, the P3 case contract and reference data, the S8 deviation read and the P7 decision-record library: consumed and faked, never defined here.
- The gateway-bff composite route and the screen field list (RWB-PLT-N001-CON).
- The NSS and LINE OA retries inside the ACE notification path, which are the path owner's.

# RWB-P5-E1062-APP Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1062-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-062 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P5-E1062-APP-16) |
| Patterns applied | DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20 |
| Parallel lane | L-P5-S |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E1062-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-DVH-001, REQ-DVH-003, REQ-DVH-007) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-062 for rwb-document, carrying the masked document and extracted-field read the screening agent makes and the `rwb.document.DocumentStored.v1` event whose event ID keys one run per case and event. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1062-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 28 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **rwb-document to serve the documents and their extracted fields of a case to the screening agent, masked, and to publish one DocumentStored event per stored document with a stable event ID**, so that **the agent's shadow run reads the same evidence every time and one run exists per case and event**.

This story is the rwb-document part of legacy RWB-E1-062. The legacy story asks for a deviation screening agent that reads "case data, call notes and documents" and proposes X1 to X7 in shadow (legacy sections 1 and 2), and its flow step 2 consumes "EV-16 DocumentStored for a document on an open case" while step 3 reads "the documents and their fields as SY-AGENT, masks personal fields and calls the model" (legacy section 4). Two of those facts are rwb-document's: the document and field read the agent makes, and the event that starts one run for that document.

Inside `rwb-document` this is the agent input capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document` (Architecture v5 slides 13, 16 and 41).
- The read answers from `document` and `document_field` in `rwb_document` only. The rows are written by the store of RWB-P5-E1024-APP; this story adds no write to them and copies no row of another service (DP-01).
- The event is `rwb.document.DocumentStored.v1` on `rwb.document.events.v1`, written to the outbox in the same transaction as the `document` row, keyed by caseId, and carrying references and codes only (DP-09; Architecture v5 slides 16, 20 and 42).
- The agent is never called by this service. It is the caller of the read and the consumer of the event, which is why the only contract dependency of the story is RWB-P10-E1062-CON.

The rest of legacy RWB-E1-062 is owned elsewhere and is not answered here:

- The agent runtime, the policy "SCREENING" version "P1", the prompt "PR1", the output schema "screening-v1", the guardrail checks, the owner-role resolution from R-DEV-02 to R-DEV-06, the evaluation on sample "SCREEN-S1" and the run states are rwb-agent's, in RWB-P10-E1062-APP against the contract RWB-P10-E1062-CON. Legacy AC1 to AC9 belong there.
- The deviation itself — registration, pause, handling and return — is rwb-deviation's, in RWB-S8-E1062-APP.

What remains here is the input the model is given and the fact that announces it: the documents of a case, their extracted fields with a confidence, the masking of every personal value before the answer leaves the service, and one event per stored document whose event ID and idempotency key never change, so that the agent's run key "SCREENING:<caseId>:<eventId>" is stable.

### 2. Business rationale

A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The screening agent reads the case, the interaction ledger and the documents at entry and again when a document arrives, and proposes deviations with reasons (legacy section 2). In Epic 1 the proposals are stored only and scored against the business analysts' review, and shown to nobody. None of that can be measured unless the agent reads the same document estate the officers read, and unless every new document announces itself once with an identity the agent can key on.

rwb-document is the system of record for those documents (FSD P5 A2.19, DT06), indexes them by case, type, date and extracted field (A2.2, FEAT-DCM-02), writes each extracted field with its confidence (A2.9, FEAT-DCM-09) and keeps every version with its date and source (A2.20, FEAT-DCM-20). The three read operations of this slice are the published form of that index: API-P5-002 lists the documents of a case, API-P5-003 reads one document's metadata, versions and extracted fields, and API-P5-009 searches the index in the caller's scope with an extracted-field filter. The event of this slice is EV-16 DocumentStored, which lists rwb-agent as one of its consumers (Architecture v5 slide 42).

Four target facts shape this slice:

1. **One identity, one answer.** The agent reads as the service identity SY-AGENT, which holds Documents right R in the document hub RBAC matrix (TSD P5 T6.1: "SY-AGENT Agent platform | R"). The authorisation decision is rwb-access's and is consumed as the cached permission of the service (DP-08); a read by an identity without the right is refused with 403 and MSG-P4-002 before any row is touched. Masking applies to every field the policy of the version in force marks personal, so the agent's input carries references, codes and confidences and no clear personal value (CTL-11, DL26).
2. **One hop, two seconds.** The read is a synchronous call on the caller's thread, one hop, with a 2 s budget and a breaker per downstream (Architecture v5 slide 10 and slide 11). The gateway-bff composite route of DP-19 is what a screen would use; for the agent the hop is its tool gateway, which calls this service directly and never chains.
3. **One event, one row.** The store of RWB-P5-E1024-APP writes the outbox row inside the transaction that writes the `document` row, and the relay publishes it on `rwb.document.events.v1` once per committed row, so the event exists exactly when the document exists (FSD P5 A2.1 and A2.2: "DocumentStored is written to the outbox with the document ID, the case ID, the type and the source"; DP-09; Architecture v5 slide 20 and the slide 42 note).
4. **One run per case and event.** The agent keys its run on the event ID, with the run key "SCREENING:<caseId>:<eventId>" of legacy AC3 and BR7 (R-UNI-40). That key is only stable if the event ID and the idempotency key of a redelivery are the same, which is what this slice guarantees on the producer side.

The slice therefore answers REQ-DVH-001 for the document part of its detection sources, and supports REQ-DVH-003 and REQ-DVH-007 with the document and interaction references the agent's proposal quotes (legacy section 18). It changes no business rule of the document hub and no rule of the agent.

### 3. Preconditions

- The `rwb_document` baseline is in place: `document`, `document_field` and `document_type` exist at the platform migration version, and the outbox, inbox and idempotency tables of DP-09 are created in the schema by the event library.
- RWB-P5-E1024-APP is done: the store writes `document` and `document_field`, sets `doc_version`, `content_sha256`, `stored` state COPY_PENDING then STORED, and writes the `rwb.document.DocumentStored.v1` outbox row in the store transaction.
- RWB-P10-E1062-CON is published: the rwb-agent contract of this legacy key, which fixes the run key "SCREENING:<caseId>:<eventId>", the tool call the agent makes to read documents and fields, and the event header fields the agent reads. The field names of that contract are Not specified in the source documents (GAP-1047; ASM-1995), and the story builds against its fake.
- The authorisation and masking decision is served by rwb-access (DP-08, H RWB-PLT-E1037-CON and C RWB-P4-E1037-CON, which arrive with the baseline). The mask format and the list of fields the policy marks personal for SY-AGENT are Not specified in the source documents (GAP-1049; ASM-1997).
- The document type table is loaded at a version in force in `rwb_document.document_type`, with the six Epic 1 types and their field definitions (RWB-P5-E1025-APP); the version in force is resolved through the reference-data route of rwb-case (DP-07, C RWB-P3-E1043-CON). The type "DEATH_CERTIFICATE" used in the criteria is a stored row of that table version.
- LOV-DOC-SOURCE holds "SCAN", "UPLOAD", "GENERATED", "PARTNER" and "EMAIL", and LOV-DOC-TYPE holds the type codes of the version in force (TSD P5 T3.2), read through the reference-data contract and never typed in code.
- The case "RW-2026-000401" and its open state are rwb-case's; this story reads no case row and needs only the case ID carried on the document row and in the event.
- The service identity SY-AGENT exists in the identity provider and holds Documents right R; SY-OCR holds CRU and stores through RWB-P5-E1049-APP, and neither identity is shared with another purpose.
- The page size and the read timeout of the list operations are configuration values resolved through the parameters contract and client library of rwb-case (DP-06, H RWB-PLT-E1042-CON and C RWB-P3-E1042-CON); no page size and no timeout is written in code.
- The relay of `rwb.document.events.v1` is running with its retry topics and its dead-letter topic, as the platform event library provides them (DP-09, H RWB-PLT-TE006-CON).

### 4. Flow

1. SY-OCR or the intake path of RWB-P5-E1049-APP stores a document on an open case through the store of RWB-P5-E1024-APP, with its case ID, type, source, file hash and extracted fields.
2. The store commits one transaction in `rwb_document`: the `document` row with `doc_version` and state COPY_PENDING, the `document_field` rows with `field_name`, `field_value`, `confidence` and `extractor_version`, and the `rwb.document.DocumentStored.v1` outbox row. Nothing is committed if any of the three fails (DP-09).
3. The relay of `rwb.document.events.v1` publishes the outbox row in CloudEvents 1.0 binary mode, keyed by caseId, with the event ID, the idempotency key, schema version 1, the occurred time and the actor "SY-OCR"; the event carries documentId, caseId, type, source and no personal value.
4. rwb-agent consumes the event, derives the run key "SCREENING:<caseId>:<eventId>" and starts one shadow run for that case and event; a redelivery of the same event carries the same event ID and the same idempotency key, so no second run is keyed and the repeat is counted (R-UNI-40).
5. The agent's tool gateway calls `GET /api/recovery/document/v1/cases/{caseId}/documents` with the identity of SY-AGENT to list the documents of the case, or `GET /api/recovery/document/v1/documents/{documentId}` to read one document with its versions and extracted fields, or `GET /api/recovery/document/v1/documents` with an extracted-field filter when the screening question is field-driven.
6. `AgentDocumentReader` authorises the call through the cached decision of rwb-access (DP-08, Documents right R, scope applied) and refuses with 403 and MSG-P4-002 before reading a row when the right is absent.
7. `AgentDocumentReader` reads the rows of `rwb_document` only: the document with id, case, type, source, stored date and `doc_version`, the type row at the version in force, and the extracted fields with their name, value, confidence and extractor version.
8. `DocumentFieldMasker` masks every field the masking policy marks personal before the answer is built, and the answer carries the masked value only; no clear value of a masked field is serialised, logged or put in a trace.
9. `rwb-document` answers the caller inside the 2 s budget, one hop, with no call to another service on the read path.
10. When the read is repeated for the same document and the same case, the same evidence is returned: the masking is deterministic on the policy version, the type is resolved at the version in force, and the version returned is the stored one, so the agent's input does not drift between two runs of the same event.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller's identity holds no Documents right R | Refused by the guard before any row is read; nothing is returned | MSG-P4-002 | AC5 |
| X2 | The case ID on the request names no document and no case in the caller's scope | The list is empty, or the single read answers 404; nothing else changes | None | AC1 |
| X3 | A field the policy marks personal is read | The value is masked in the answer; the clear value never leaves the service | None | AC1 |
| X4 | The outbox write fails inside the store transaction | The `document` row, the `document_field` rows and the event are all rolled back; the store answers 503 with MSG-P7-003 through its decision record | MSG-P7-003 | AC3 |
| X5 | The relay cannot publish a committed outbox row | The event stays in the outbox and is published when the relay recovers, once, with the same event ID | None | AC3, AC4 |
| X6 | The same event is delivered twice to the agent | The event ID and the idempotency key are the same, so the run key is the same; the repeat is counted (R-UNI-40) | None | AC4 |
| X7 | The stored type of a document has left the version in force | The document is served with the type stored on its row and is never re-typed by this story | None | AC6 |
| X8 | The reference-data read of the type version does not answer | The read answers 503 with MSG-GEN-006 naming "Reference data" and returns no document | MSG-GEN-006 | AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Answers from `rwb_document` only, builds against the rwb-agent contract fake RWB-P10-E1062-CON, the authorisation and masking decision of rwb-access and the reference-data route of rwb-case; no build dependency of its own |
| Negotiable | The type, the field list, the mask policy version, the page size and the timeout are rows, parameters or configuration; the story fixes only the behaviour |
| Valuable | The screening agent reads the same masked evidence on every run, and the event that starts a run has one stable identity |
| Estimable | One module, three operations already on the P5 contract, one event already on the P5 topic, one masker and one stability guard |
| Small | Fits one sprint as a secondary slice of the legacy key, with the store of RWB-P5-E1024-APP already in place |
| Testable | Every criterion in section 7 is one automated test over synthetic documents, with every cross-service answer stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent in shadow [E2b] — the rwb-document input and event

  Background:
    Given the rwb-agent contract mock returns the run key "SCREENING:<caseId>:<eventId>" for a DocumentStored event and the tool call shape of agent "SCREENING"
    Given the rwb-access contract mock returns the authorisation decision for actor "SY-AGENT" with Documents right R
    Given the rwb-case reference-data contract mock returns the document type version in force with "DEATH_CERTIFICATE" and its field list
    Given case "RW-2026-000401" holds document "D-1001" of type "DEATH_CERTIFICATE" with source "SCAN"

  Scenario: AC1 The case documents are served masked to the agent (new, D-RCV-60)
    Given the rwb-access contract mock returns the masking decision for actor "SY-AGENT" with two of the fields of "DEATH_CERTIFICATE" marked personal
    When "SY-AGENT" calls GET /api/recovery/document/v1/cases/RW-2026-000401/documents
    Then the answer holds document "D-1001" with its id, type "DEATH_CERTIFICATE", source "SCAN", stored date and doc_version
    And each extracted field of "D-1001" is returned with its field name, its value and its confidence
    And every field marked personal is returned masked and no clear value of it is in the answer, the log or the trace

  Scenario: AC2 DocumentStored carries the header and the key the agent needs (new, D-RCV-60)
    Given document "D-1001" of type "DEATH_CERTIFICATE" with source "SCAN" is stored on case "RW-2026-000401"
    When the store commits
    Then one rwb.document.DocumentStored.v1 event is written with an event ID, an idempotency key, schema version 1, the occurred time and actor "SY-OCR"
    And its payload holds documentId "D-1001", caseId "RW-2026-000401", documentType "DEATH_CERTIFICATE" and source "SCAN"
    And the payload holds no personal value and no extracted field value
    And the event is keyed by caseId "RW-2026-000401", so the agent derives the run key "SCREENING:<caseId>:<eventId>"

  Scenario: AC3 One event per document row, in the row's transaction (new, D-RCV-60)
    Given the store of a document of type "DEATH_CERTIFICATE" on case "RW-2026-000402" writes the "document" row and the outbox row in one transaction
    When the relay publishes and the same store is retried with the same Idempotency-Key
    Then rwb.document.events.v1 holds one DocumentStored event for that document and the case holds one "document" row
    And a forced failure of the outbox write leaves no "document" row, no "document_field" row and no event
    And the relay publishes on the topic rwb.document.events.v1 with its retry topics and its dead-letter topic

  Scenario: AC4 A redelivered event keeps its event ID and key (new, D-RCV-60)
    Given the rwb-agent contract mock has recorded one run for event "EV-16 DocumentStored" of document "D-1001" on case "RW-2026-000401"
    When the same event is redelivered
    Then the event carries the same event ID and the same idempotency key as the first delivery
    And the run key "SCREENING:RW-2026-000401:<eventId>" is unchanged and no second run is keyed
    And the relay counts the repeat of the same event ID and writes no second outbox row (R-UNI-40)

  Scenario: AC5 A service identity without Documents R is refused (new, D-RCV-60)
    Given the rwb-access contract mock returns no Documents right R for the calling service identity
    When that identity calls GET /api/recovery/document/v1/cases/RW-2026-000403/documents
    Then the call is refused with status 403 and message MSG-P4-002
    And no document and no extracted field is returned
    And the same call by "SY-AGENT" is granted, because SY-AGENT holds Documents right R
    And each read is authorised with the caller's own identity and never with a shared identity

  Scenario: AC6 The type is read at the version in force and never re-typed (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns the document type version in force
    When the read of document "D-1001" answers and the read of a document of case "RW-2026-000403" whose stored type has left the version in force answers
    Then type "DEATH_CERTIFICATE" is read from the type table at the version in force, with its field list
    And no type code, field name or mask value appears in the Java source or in the module configuration
    And the document whose type is not in force is served with the type stored on its row and is never re-typed by this story

  Scenario: AC7 No rule, no deviation and no agent run is written here (new, D-RCV-60)
    Given the screening run for case "RW-2026-000404" is rwb-agent's
    When the read is served and the event is published
    Then rwb-document evaluates no decision table and loads no Drools package for this story
    And no agent run row, no deviation row and no ledger entry is written by this service
    And the agent reaches the documents and the fields only through the published operations of this service
    And the ledger of the agent's reads is written by rwb-source-data's listener from the event, not by rwb-document
```

The seven criteria above are new and test only this slice: the masked document and extracted-field read the screening agent makes, and the one event per stored document with its stable identity. The legacy criteria AC1 to AC9 of RWB-E1-062 are owned by RWB-P10-E1062-APP (the shadow run, the shadow flags, the precision and recall, the owner role, the preceding contact, the review marker, the repeated event on the run side, the code outside the list and the timeout) and by RWB-S8-E1062-APP (raising, pausing and handling the deviation). No legacy criterion text is copied into this section, and this story owns no legacy AC.

The cross-service facts are read from the contract mocks named in the Background: the rwb-agent contract of RWB-P10-E1062-CON returns the run key and the tool call, the rwb-access contract returns the authorisation and masking decision, and the rwb-case reference-data contract returns the type version in force. The idempotency-key format of `rwb.document.DocumentStored.v1` and the event field names the agent's contract expects are Not specified in the source documents (GAP-1048; ASM-1996); the payload names used above are the ones the FSD P5 A2.1, A2.2 and A2.19 fix in prose (the document ID, the case ID, the type and the source) and the stored date of the row.

The read behaviour of a document whose stored type has left the version in force is Not specified in the source documents (GAP-1050; ASM-1998): the FSD P5 A2.1, A2.2 and A2.19 fix only the refusal of an unknown type at store time, with 422 and MSG-P5-006, and say nothing of a document already stored. AC6 keeps the type stored on the row, serves the document, and leaves both the refusal path and any re-typing to the store stories of P5.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every read is authorised with the caller's own identity, and every field the masking policy marks personal is masked before the answer leaves the service; no clear personal value is returned, logged or traced | CTL-11; DL26 (open; ASM-0247, ASM-0264, ASM-0275, ASM-0355); FSD P5 A2.6 AC-ALT-P5-006-01; TSD P5 T6.2 |
| BR2 | In the document sense, a read carries codes, references and a confidence and no clear personal value: the document ID, the case ID, the type code, the source code, the stored date, `doc_version` and per field the name, the masked value and the confidence (legacy BR2) | FSD P5 A2.9 AC-P5-009-01; legacy BR2 |
| BR3 | The event payload carries references and codes only — document ID, case ID, type and source — and never a personal value, an extracted field value or a document's text | Architecture v5 slide 42 note; FSD P5 A2.1, A2.2, A2.19; legacy section 8 BR7 |
| BR4 | One `DocumentStored` event per `document` row, written to the outbox in the same transaction as the row, and never a second event for the same row, also when the store is retried (legacy BR7 on the producer side) | R-UNI-40; DP-09; FSD P5 A2.2 AC-P5-002-01; legacy BR7 |
| BR5 | The event ID and the idempotency key of one stored document never change across a redelivery, so the agent's run key "SCREENING:<caseId>:<eventId>" is stable and the repeat is counted (R-UNI-40) | Legacy AC3, AC7, BR7; R-UNI-40 |
| BR6 | The type and its field list are read from the type table at the version in force; no type code, field name, mask value or page size is written in code; a stored document is served with the type on its row and is never re-typed on read, and the unknown-type refusal (422, MSG-P5-006) applies at store time only | FSD P5 A2.3 BR-P5-003; FSD P5 A2.1 AC-EXC-P5-001-01; FSD P5 A2.2 AC-EXC-P5-002-01; TSD P5 T3.1, T3.2; DP-07 |
| BR7 | rwb-document evaluates no rule for this story: no decision table, no DRL, no workbook and no rule package is loaded to serve the agent its input (DP-04 as a prohibition) | DP-04; Architecture v5 slide 16 |
| BR8 | rwb-document stores no agent output, no agent run and no deviation: the proposal, the guardrail result and the run state are rwb-agent's rows, and the ledger is rwb-source-data's (DP-18 and DP-20 as prohibitions) | DP-18, DP-20; Architecture v5 slides 13 and 16 |

Rule coverage: BR1 by AC1 and AC5 (TC-E1-062-01, TC-E1-062-10); BR2 by AC1 (TC-E1-062-01); BR3 by AC2 (TC-E1-062-03); BR4 by AC3 (TC-E1-062-03) and AC7 (TC-E1-062-07); BR5 by AC7 (TC-E1-062-07); BR6 by AC6 (TC-E1-062-03); BR7 and BR8 by the build check of TC-E1-062-13.

The rules hold in `rwb_document` as follows. BR1 is executed by the guard of the service template holding the cached decision of rwb-access and by `DocumentFieldMasker` on the answer path; the access log entry for a read is written by the ACE common module, not by this package. BR2 and BR3 are property tests over the serialised answer and over the event payload: a synthetic personal value placed in a masked field must not appear in the JSON, in the log or in the span attributes. BR4 is executed by the outbox row being written inside the store transaction of RWB-P5-E1024-APP and by the relay publishing per outbox row, so a rolled-back store leaves no event and a retried store finds the existing document and writes no second row. BR5 is executed by `EventIdStabilityGuard`, which takes the event ID from the outbox row and derives the idempotency key from it, so a redelivery of the same row carries the same pair. BR6 is executed by reading `document_type` at the version the reference-data route reports in force, and by a build check that fails on a type code or a field name in the source. BR7 and BR8 are prohibitions checked by the same build: no Drools dependency in the module, no write to an agent, deviation or ledger table, and no outbound call to rwb-agent.

### 9. State transitions

None for the case. This story changes no case status, raises no deviation and creates no agent run. Two lifecycles are read or written here, and both belong to other parts of the service:

| From | Event | Condition | To |
|---|---|---|---|
| (no row) | the store of RWB-P5-E1024-APP commits | The document row, its fields and the outbox row are written in one transaction | `document.state` = COPY_PENDING, and the outbox row exists |
| COPY_PENDING | the copy to the container succeeds | The file is stored and `storage_ref` is set | STORED (read only in this story; written by RWB-P5-E1024-APP) |
| outbox row written | the relay picks the row | The relay is running and the topic accepts the record | relayed: the event is on `rwb.document.events.v1` with its event ID and idempotency key |
| relayed | the agent's consumer records the event in its inbox | The event is new to that consumer | delivered at most once to the handler; a redelivery of the same event ID is counted and discarded (R-UNI-40) |

The agent run states — PENDING, RUNNING, TIMED_OUT, GUARDRAIL_FAILED, COMPLETED and the review marker of a low-confidence proposal — are rwb-agent's rows and rwb-agent's transitions (RWB-P10-E1062-APP), and no state of them is written here. The document lifecycle beyond COPY_PENDING and STORED, including retention and custody, belongs to the store, retention and custody stories of P5.

This story adds no value to the closed list LOV-DOC-SOURCE; that list is read through the reference-data client of rwb-case (DP-07) and is not copied into the schema.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Reads documents, their versions and their extracted fields with Documents right R, masked, inside the scope the decision grants (TSD P5 T6.1) |
| SY-OCR, OCR and extraction pipeline | Stores documents with Documents right CRU; the store itself is RWB-P5-E1049-APP and RWB-P5-E1024-APP, and this story reads the rows it writes |
| rwb-document service identity (the rwb-document login, DP-02) | Serves the three read operations and writes the outbox row inside the store transaction; reads `document`, `document_field` and `document_type` in `rwb_document` only |
| RW-COE, center of excellence analyst | Reads run metadata only; the run metadata screen is rwb-agent's, and this story serves it no document content of its own |
| RW-PLATADM, platform administrator | Platform administration right R: reads the service's operational views, no document content |
| RW-AUDIT, internal audit | Platform administration right R: reads the access entries of the document estate written by the ACE common module |

The authorisation decision is not taken here. It comes from rwb-access, which owns Recovery roles as data, scope and masking policy (Architecture v5 slide 41), consumed as the cached permission of the service (DP-08); the refusal shape is 403 with MSG-P4-002, and a case outside the caller's scope is refused with MSG-P4-003. Each read uses the caller's own identity: the agent's tool gateway presents SY-AGENT, and no shared identity exists for the agent's reads.

The legacy access case TC-E1-062-10 (a role without the right is refused with MSG-P4-002) is answered here only for the document read of AC5. The rest of that legacy case — RW-CASEOWN calling the agent evaluation read — belongs to RWB-P10-E1062-APP, because the evaluation is the agent's.

### 11. Data

| BR Field ID | Entity in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read (the document ID of the answer and of the event) |
| DF-DOC-002 | document | case_id | Read (the case reference of the answer and the event key) |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-005 | document | source | Read |
| DF-DOC-009 | document | retention_class | Read (returned with the metadata; it is not used to mask) |
| DF-DOC-010 | document | write_once | Read (returned with the metadata) |
| DF-DOC-011 | document | doc_version | Read |
| DF-DOC-026 | document | content_sha256 | Read (returned as the file reference; no content is served) |
| DF-DOC-027 | document | captured_at | Read (part of the stored date and the evidence reference) |
| DF-DOC-012 to DF-DOC-017 | document_field | id, document_id, field_name, field_value, confidence, confirmed_by | Read (the value is masked before the answer) |
| DF-DOC-034 | document_field | extracted_value | Read (returned as the extracted value beside the confirmed one) |
| DF-DOC-035 | document_field | extractor_version | Read |
| DF-REF-218 to DF-REF-233 | document_type | id, doc_type_code, label_en, label_th, write_once, retention_class, field_definitions, the two sign-offs, table_version, valid_from, valid_to, reference_version_id, classify_threshold | Read (the type row at the version in force, for the code and the field list) |
| DF-OPS-178 to DF-OPS-183 | processed_event (inbox of the platform event library) | the inbox columns of the library | Not written: this story consumes no event; the table is created in `rwb_document` by DP-09 and belongs to the consumers |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. The outbox row of the event is written by RWB-P5-E1024-APP inside its store transaction; this story owns the event's shape and its stability, and 12.3 fixes what it carries.

Nothing else is read or written here. The case, the interaction ledger, the type version and the rules arrive only through contracts: the case ID arrives on the document row and in the event, the ledger entries are rwb-source-data's and rwb-agent reads them itself, the type version comes from the reference-data route of rwb-case (DP-07), and no rule row is read at all (DP-04 as a prohibition). No `v_ace_*` view and no `public` table is read by this story, and no row of another service's schema is copied (DP-01).

### 12. Contract

#### 12.1 REST operations provided

The three operations of the document hub contract on base `/api/recovery/document/v1`, owner rwb-document (P5). This story adds no path, no query parameter and no response field; it answers these three for the agent, masked, under the caller's identity.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P5-002 | GET | `/cases/{caseId}/documents` | List the documents on a case | Documents right R, scope applied | Not applicable |
| API-P5-003 | GET | `/documents/{documentId}` | Read a document's metadata, versions and extracted fields | Documents right R, scope applied | Not applicable |
| API-P5-009 | GET | `/documents` | Search active documents across the cases in the caller's scope by type, stored date, extracted field and free text | Documents right R, scope applied; each search written to the access log | Not applicable |

**API-P5-002.** Request: query `type`, `page`, `size`. Response: DocumentPage — the documents of the case with id, caseId, documentType, source, stored date, docVersion, retentionClass and writeOnce, and for each document its extracted fields with name, masked value, confidence and extractorVersion. Errors: 401 no Workbench identity (message ID Not specified in the source documents (CG-ALL-6095)), 403 Documents right R absent (MSG-P4-002) or case outside the scope (MSG-P4-003), 404 no such case (message ID Not specified in the source documents (CG-ALL-6095)), 503 the reference data or the store is unavailable (MSG-GEN-006).

**API-P5-003.** Request: none. Response: Document — the metadata of API-P5-002 for one document, its version list (docVersion, stored date, source, previousVersionId) and its extracted fields. Errors: 401, 403 (MSG-P4-002, MSG-P4-003), 404 no such document, 503 (MSG-GEN-006).

**API-P5-009.** Request: query `type`, `dateFrom`, `dateTo`, `field`, `op`, `value`, `value2`, `q`, `page`, `size`. Response: DocumentSearchPage — the matching documents with case number, type, stored date and the matched field value (masked), inside the caller's scope. Errors: 401, 403 (MSG-P4-002), 422 a criterion outside its list or an empty criterion set (MSG-GEN-001), 503 (MSG-GEN-006). The access-log entry of each search is written by the ACE common module.

The operation the agent's own contract names as its tool call is Not specified in the source documents (GAP-1047; ASM-1995): whether the agent reads through one operation per document or one per case, and the field names of that call, are fixed by RWB-P10-E1062-CON, and this story serves it through the three operations above. Its responses are the TSD P5 T-A.2 shapes named here; no new shape is introduced.

#### 12.2 REST operations consumed

None at run time. This story calls no other service on the read path and no other service on the event path: the answer is built from `rwb_document`, and the event is written to the outbox and published by the relay, not by a call.

Two contracts are consumed as shapes and fixtures:

| Contract | Owner | What is consumed | Note |
|---|---|---|---|
| RWB-P10-E1062-CON | rwb-agent | The run key "SCREENING:<caseId>:<eventId>", the agent's tool call and the event header fields the agent reads | The agent is the caller of 12.1 and the consumer of 12.3; the contract fixes the shape this service must satisfy. Its field names are Not specified in the source documents (GAP-1047; ASM-1995) and its idempotency-key expectation is Not specified in the source documents (GAP-1048; ASM-1996) |
| DP-07 reference data of rwb-case (C RWB-P3-E1043-CON) | rwb-case | The document type version in force and the two lists LOV-DOC-TYPE and LOV-DOC-SOURCE | Read through the reference-data client library; no list value is copied into `rwb_document` |

#### 12.3 Events published

| Event | Topic | Key | Payload |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | caseId | documentId, caseId, type, source |

CloudEvents 1.0 envelope in binary mode, with the event ID, the idempotency key, the schema version 1, the occurred time, the actor "SY-OCR" and the source of the event; no personal data and no extracted field value in the envelope or the payload. rwb-agent and rwb-case are the consumers (Architecture v5 slide 42, event 16). The event is written to the outbox in the store transaction of RWB-P5-E1024-APP, so it exists exactly when the `document` row exists, and the relay publishes it once per outbox row, with the retry topics and the dead-letter topic of the platform event library.

The idempotency key is the event's own identity in this slice: the key is derived from the outbox row's event ID, so a redelivery of the same row carries the same pair. The exact idempotency-key format the rwb-agent contract expects is Not specified in the source documents (GAP-1048; ASM-1996). `rwb.document.DocumentFieldsExtracted.v1` is on the same topic but is published by the extraction path of RWB-P5-E1053-APP, not by this story.

#### 12.4 Events consumed

None. This service is the producer of the event that starts the agent's run, not a consumer of it: the agent triggers on the event it receives, and this story subscribes to no topic, holds no consumer group and writes no inbox row. The inbox table of DP-09 is present in `rwb_document` for the consumers that other P5 stories add, and this story writes none of its rows.

#### 12.5 Workflows and activities

None. The read is a synchronous REST call in the caller's thread, one hop, inside the 2 s budget. `DocumentIntakeWorkflow` and its activities belong to RWB-P5-E1049-APP, and the agent's `AgentRunWorkflow` is rwb-agent's on queue `rwb-agent` (Architecture v5 slide 16); this story starts neither and contributes no activity.

#### 12.6 Schedules

None. The 15-minute document intake Schedule (legacy JOB-12) belongs to RWB-P5-E1049-APP and the retention Schedule to the retention story; this slice adds no Schedule and no timer.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 (`rwb_document`) | Read only: the metadata of the answer and the row the event announces |
| `document_field` | P5 (`rwb_document`) | Read only: the extracted fields with their confidence, masked in the answer |
| `document_type` | P5 (`rwb_document`) | Read only: the type row at the version in force, for the code and the field list (loaded by RWB-P5-E1025-APP) |
| `outbox_event` | PLT library, created in `rwb_document` | The `DocumentStored` row, written by the store of RWB-P5-E1024-APP in its transaction and published by the relay (DP-09) |
| `processed_event` | PLT library, created in `rwb_document` | Present for the consumers of other P5 stories; not written by this story |
| `idempotency_key` | PLT library, created in `rwb_document` | The store's request key; read by this story only to assert that a retried store writes one row and one event |

rwb-document reads no table of another service and holds no foreign key across services (DP-01). The case is not copied: its ID arrives on the document row and in the event. The type version, the lists and the page size arrive through the contracts of 12.2.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P10-E1062-CON fake | The agent contract of this legacy key | The run key "SCREENING:<caseId>:<eventId>", the tool call with its field names (as the fake fixes them) and the event header the agent reads |
| rwb-access authorise and masking fake (RWB-P4-E1037-CON) | DP-08 | A granted decision for SY-AGENT with Documents right R, a refused decision for an identity without it, and a masking decision that marks two fields of "DEATH_CERTIFICATE" personal |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | DP-07 | The document type version in force with "DEATH_CERTIFICATE" and its field list, LOV-DOC-TYPE and LOV-DOC-SOURCE, and a version in force in which one stored type is absent (AC6) |
| rwb-case parameters fake (RWB-P3-E1042-CON) | DP-06 | The page size and the read timeout of the list operations |
| outbox and relay test double | DP-09 | A relay that accepts the row, a stopped relay for the AC3 path, and a redelivery of the same event for AC4 |
| Topic test double for `rwb.document.events.v1` | The published event | A consumer that records the envelope and the payload, so the header, the key and the absence of personal data are asserted |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 0 consumed | API-P5-002, API-P5-003 and API-P5-009 on `/api/recovery/document/v1`, each one hop with a 2 s budget and a breaker per downstream; no outbound call on the read path |
| Kafka | 1 event published, 0 consumed | `rwb.document.DocumentStored.v1` on `rwb.document.events.v1`, keyed by caseId, through the outbox and the relay; no consumer group in this story |
| Temporal | None | No workflow, no activity and no Schedule in this slice |
| File | None | No blob is read or written by this story; the content read API-P5-004 is the store's and is not part of the agent input |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `agentinput`, Java package `th.co.scb.ace.workbench.recovery.document.agentinput`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentDocumentReader | Service | Serves API-P5-002, API-P5-003 and API-P5-009 for the agent from `document`, `document_field` and `document_type`: authorises the caller, resolves the type at the version in force, and assembles the answer with the case, the stored date, `doc_version` and the fields |
| DocumentFieldMasker | Service | Applies the masking decision of the version in force to every field marked personal, before the answer is built; asserts that no clear value reaches the JSON, the log or the trace |
| DocumentStoredEventPublisher | Service | Builds and writes the `rwb.document.DocumentStored.v1` outbox row inside the store transaction, with the header, the key caseId and the payload; called by the store of RWB-P5-E1024-APP |
| OutboxEventMapper | Mapper | Maps the outbox row to the CloudEvents 1.0 envelope in binary mode: event ID, idempotency key, schema version 1, occurred time, actor and source |
| EventIdStabilityGuard | Service | Derives the idempotency key from the event ID and refuses a second outbox row for the same `document` row, so a redelivery carries the same pair (AC4, BR5) |

**Database and migrations.** Migration in this slice: `V1062_1__agent_input_read.sql`, one step in the per-service Flyway sequence of `rwb_document` (DP-15), which adds the read-only view `v_document_field_search` over `document` and `document_field` that the extracted-field filter of API-P5-009 needs, and nothing else — no table, no column and no index is added by this slice. The view is a migration object of this slice, recorded here; it is not an entity of LDM v9 or Data Classification v5 (CG-ALL-6094). The rows it reads are written by RWB-P5-E1024-APP and RWB-P5-E1025-APP, and the outbox, inbox and idempotency tables are created by the platform event library of DP-09 in `rwb_document`. No migration of this service touches another service's schema or the shared baseline.

**Configuration and reference data.**

- The type row and its field list are read at the version in force; the type is never named in the module, and the build check of AC6 fails on a type code or a field name in the source (DP-07). A document already stored is always served with the type on its row, also when that type has left the version in force, because the behaviour of that case is Not specified in the source documents (GAP-1050; ASM-1998).
- LOV-DOC-TYPE and LOV-DOC-SOURCE are read through the reference-data client library of rwb-case; no list value is copied into the schema.
- The page size and the read timeout of the list operations are parameter values resolved through the parameters contract and client library of rwb-case (DP-06), never constants in code.
- The mask policy version and the fields it marks personal are the decision of rwb-access at the version in force; the mask format is Not specified in the source documents (GAP-1049; ASM-1997).
- The actor of the event is the service identity "SY-OCR", and the event source is the rwb-document service; both are configuration of the envelope mapper, not literals in the payload.
- The feature switch `rwb.document.agent-input` is read as a parameter: off means the three operations answer 404 to the agent's identity and the store writes no `DocumentStored` outbox row for the agent, while the document estate itself is unchanged.

**Build steps**

1. `AgentDocumentReader` over `document`, `document_field` and `document_type`, with the type resolved at the version in force through the reference-data fake; unit tests for AC1 and AC6.
2. `DocumentFieldMasker` with the masking decision of rwb-access; a property test that places a synthetic personal value in each masked field and asserts that it appears in no answer, no log line and no span attribute (AC1, BR1, BR2).
3. The three operations with the authorisation guard and the scope check, and the refusal path before any row is read; API tests for AC1, AC5 and the empty-list path of X2.
4. `DocumentStoredEventPublisher` inside the store transaction, with the forced outbox failure and the rolled-back store; integration test for AC3 and X4.
5. `OutboxEventMapper` and `EventIdStabilityGuard` with the CloudEvents envelope, the key caseId and the derived idempotency key; contract test against the RWB-P10-E1062-CON fake for AC2 and AC4.
6. The relay path on the test topic, with the stopped relay, the retry topics and the dead-letter topic; test for X5 and the once-per-row assertion of AC3.
7. The build check that fails on a type code, a field name, a mask value or a page size in the source; test for AC6 and BR6.
8. A contract-fake run of RWB-P10-E1062-CON, rwb-access and rwb-case reference data, so the slice builds and proves every criterion before rwb-agent is live in DEV.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P10-E1062-CON` exactly as the Work Package fixes them; the platform contract libraries of DP-04, DP-06, DP-07, DP-09, DP-15 and DP-19 arrive with the baseline, not with this story.

- **DP-01** keeps the whole answer inside `rwb_document`: the document, its fields and its type row are this service's own, no table of another service and no ACE view is read, and the case is only a reference carried on the row and in the event.
- **DP-04** applies as a prohibition: no rule is evaluated to serve the agent its input, so the module loads no Drools kernel, no DRL and no workbook, and the rule rows of R-DEV-02 to R-DEV-06 stay with rwb-agent and rwb-decision.
- **DP-06** is the parameter read of the list operations: the page size and the read timeout come from the parameters contract and client library of rwb-case, cached, so a page size is never a constant of the module.
- **DP-07** is the type read: the type code and the field list are taken from the type table at the version in force that the reference-data route reports, and LOV-DOC-TYPE and LOV-DOC-SOURCE are resolved the same way.
- **DP-09** is the outbox: the `DocumentStored` row is written in the store transaction, the relay publishes it on `rwb.document.events.v1` with CloudEvents, and the event's identity is the outbox row's, which is what makes the agent's run key stable.
- **DP-13** gives the read its base `/api/recovery/document/v1`, so the agent's tool gateway calls one owner and never a monolith path.
- **DP-15** puts any read-only view of the index in the per-service Flyway sequence of `rwb_document`; no migration of this slice creates a business table, because the store already did.
- **DP-18** applies as a prohibition: the interaction ledger is rwb-source-data's, the ledger of the agent's reads is written by its listener from the event, and this service writes no ledger row of its own (default ruling).
- **DP-19** is the gateway-bff composite route on which a screen would read the same operations; the agent reaches them through its tool gateway, one hop, and no route calls a service that calls another.
- **DP-20** applies as a prohibition in the outbound direction: this service is the agent's supplier, not its client; it makes no call to rwb-agent and imports only the contract shape of RWB-P10-E1062-CON as its fake.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P10-E1062-CON stay green, a stored document of case "RW-2026-000401" is read by SY-AGENT masked and with its confidences, a document whose type has left the version in force is still served, an identity without Documents right R is refused with MSG-P4-002, and `rwb.document.DocumentStored.v1` is on the topic once per `document` row with the same event ID and idempotency key on a redelivery and no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's identity holds no Documents right R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or the document is outside the caller's scope | This case is not in your scope. |
| MSG-P10-002 | Not in this story: the evaluation on an empty sample belongs to RWB-P10-E1062-APP | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Not in this story: the same evaluation already running belongs to RWB-P10-E1062-APP | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-GEN-006 | The reference data or the store does not answer inside the budget (X8) | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The store cannot write its record in the transaction, so nothing is stored and no event exists (X4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | Not specified in the source documents (DOR-RWB-P5-E1062-APP-9) | Not specified in the source documents (DOR-RWB-P5-E1062-APP-9) |
| MSG-P5-006 | Not specified in the source documents (DOR-RWB-P5-E1062-APP-9) | Not specified in the source documents (DOR-RWB-P5-E1062-APP-9) |

For MSG-P4-002 in this story, {action} names the action the caller tried — for example "read the documents of this case" — and never a case fact, a document ID or a role name. For MSG-GEN-006 the {system} value is "Reference data" on the type read and "Document service" on the store. Errors are RFC 9457 problem responses with `messageId` set to the ID above, `detail` with the placeholders filled and `instance` naming the request; the HTTP mapping is 403 for MSG-P4-002 and MSG-P4-003, 422 for MSG-GEN-001 on a search criterion, and 503 for MSG-GEN-006 and MSG-P7-003.

No user sees an agent proposal, and no message of this story carries one: the read returns the document estate to the agent, and the proposal, the confidence of a proposal and the review marker are the agent's rows and the agent's messages (RWB-P10-E1062-APP).

### 15. Screens and states

No screen in this story. The read is a service-to-service call: the agent's tool gateway calls rwb-document, one hop, and no person is in the loop. No screen of the case record, the document tab or the review queue changes because of this slice, and SCR-30 Case documents shows the same rows it showed before. The loading state of SCR-30 is as Screen Specifications v1 section SCR-30 gives it; its empty, error and no access states are Not specified in the source documents (CG-ALL-6102).

The run metadata screen is rwb-agent's: `GET /agent-runs/{id}` on `/api/recovery/agent/v1` lists the runs, their mode, their status and the evaluation scores, and the center of excellence analyst reads them there (Architecture v5 slide 16; RWB-P10-E1062-APP). This story serves that screen nothing and holds no state of it. The gateway-bff composite route of DP-19 is the only path on which a screen reaches the operations of 12.1, and the route specification and the field-level masking of the composite route are Not specified in the source documents (GAP-1049; ASM-1997).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-062-10 | Access: the document read of AC5. The evaluation read the legacy case names belongs to RWB-P10-E1062-APP | Component | An identity holding no Documents right R calls the case documents read of case RW-2026-000403; refused with 403 and MSG-P4-002; SY-AGENT is granted the same read |
| TC-E1-062-01 | AC1 and AC7 for the masked documents and fields the agent reads, with no decision table evaluated and no ledger row written; the shadow run itself belongs to RWB-P10-E1062-APP | End to end | 200 synthetic cases with call notes and documents; the read of each case by SY-AGENT returns masked fields and confidences |
| TC-E1-062-02 | No criterion here; the comparison of proposals with the labels belongs to RWB-P10-E1062-APP | Component | Sample SCREEN-S1 version 1; X6 counts 18, 2, 6 |
| TC-E1-062-03 | AC2, AC3, AC4, AC6 | End to end | Case RW-2026-000401 receives document D-1001 of type DEATH_CERTIFICATE; EV-16 DocumentStored on topic rwb.document.events.v1 |
| TC-E1-062-04 | No criterion here; the owner role read from R-DEV-02 to R-DEV-06 belongs to RWB-P10-E1062-APP | Component | X4 proposal on case RW-2026-000402; one unmapped code |
| TC-E1-062-05 | No criterion here for the X1 proposal; the event that announces the document and its stable run key is AC5 | Component | Call 2026-11-25, complaint note 2026-11-27 |
| TC-E1-062-06 | No criterion here; the review marker of a low-confidence proposal belongs to RWB-P10-E1062-APP | Component | X2 proposal with confidence 0.72 |
| TC-E1-062-07 | AC7 | Component | EV-16 DocumentStored for document D-1001 on case RW-2026-000401 delivered twice |
| TC-E1-062-08 | No criterion here; the code guardrail belongs to RWB-P10-E1062-APP | Component | Model stub returns code X9 |
| TC-E1-062-09 | No criterion here; the model timeout and the run status belong to RWB-P10-E1062-APP | NFR | Model stub silent 61 seconds |
| TC-E1-062-11 | No criterion here; the contract of the operations of 12.1 and the event of 12.3 against the RWB-P10-E1062-CON fake | Component | Response shapes of API-P5-002, API-P5-003 and API-P5-009; payload of rwb.document.DocumentStored.v1 with documentId, caseId, type and source |
| TC-E1-062-12 | No criterion here; the boundary of the tables of 12.7 | Component | Read only of document, document_field and document_type; outbox_event, processed_event and idempotency_key as 12.7 states; no table outside 12.7 read or written |
| TC-E1-062-13 | No criterion here; the prohibitions of BR7 and BR8 (no rule package loaded, no agent, deviation or ledger table written, no call to rwb-agent) | Component | Build check of the module: no Drools dependency, no write to an agent, deviation or ledger table and no outbound call to rwb-agent |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component, and the model stub and timeout cases to Component or NFR. Every legacy test case of this key is listed above with the slice of behaviour this story answers — the masked read for TC-E1-062-01 and TC-E1-062-10, the document, the event and the repeated event for TC-E1-062-03 and TC-E1-062-07, and the producer's part of the ledger case for TC-E1-062-05 — and no criterion for the cases whose behaviour is the agent's or the deviation's. The -ITG copies of these cases are not here: they belong to RWB-ITG-E1062-ITG, which proves the same values across rwb-document, rwb-agent and rwb-source-data end to end.

### 17. Guardrails

- Masking happens before the model call and before the answer leaves the service. Every field the policy marks personal is masked by `DocumentFieldMasker`, and a property test asserts that a synthetic personal value appears in no answer, no log line and no span attribute. The mask policy version is rwb-access's; the mask format is Not specified in the source documents (GAP-1049; ASM-1997).
- No personal data in events, workflow inputs, topics or logs. The `DocumentStored` payload carries the document ID, the case ID, the type, the source and the stored date, and the event payload rule of BR3 is asserted by a contract test on the topic test double.
- No business value in code: the type, the field list, the two lists, the page size, the timeout and the mask policy version are rows, parameters or configuration. A build check fails on a type code, a field name, a mask value or a page size in the source.
- The agent's identity is read only. SY-AGENT holds Documents right R and nothing more: it stores no document, changes no field and reads no content. No shared identity exists for the agent's reads, and each read is authorised with the caller's own identity.
- One evaluator per concern: this story evaluates no rule package, holds no Drools dependency and reads no rule row; the R-DEV rows and the policy of the screening agent stay with rwb-agent and rwb-decision (DP-04 as a prohibition).
- No cross-schema read: `rwb_document` holds no foreign key into another schema and no copy of a case, a ledger entry, a rule row or a list value (DP-01). The case arrives as a reference, the ledger stays with rwb-source-data (DP-18 as a prohibition) and the agent's rows stay with rwb-agent (DP-20 as a prohibition).
- The event exists only when the row exists: the outbox row is written inside the store transaction of RWB-P5-E1024-APP, and a failed store leaves no row, no field and no event.
- The event identity is stable: the idempotency key is derived from the event ID, one outbox row exists per `document` row, and a redelivery carries the same pair, so the agent's run key never moves.
- Any migration of this slice is a step in the per-service Flyway sequence of `rwb_document`, versioned and repeatable, and no migration of this service touches another schema or the shared baseline (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-DVH-01, FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-40 | TC-E1-062-01, TC-E1-062-03, TC-E1-062-07, TC-E1-062-10 |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | Business Requirements Program, section 5.15 | FEAT-DVH-04 | 11 Handle customer care and deviations | None | TC-E1-062-04 (the owner rows are the agent's; the document references the proposal quotes come from this read) |
| REQ-DVH-007 | A complaint is matched to the contact before it | Business Requirements Program, section 5.15 | FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-05 (the ledger window is rwb-source-data's; the run key that keeps one run per event is AC4) |

The supporting features of the document estate are FEAT-DCM-02 (index by case, type, date and extracted field), FEAT-DCM-09 (extract fields with a confidence), FEAT-DCM-19 (the hub as system of record) and FEAT-DCM-20 (versions), which the FSD P5 module pairs with its own requirements in RWB-E1-024, RWB-E1-053 and RWB-E1-026; this slice answers them only for the read the screening agent makes and the event that announces a document, and changes neither the index design nor the extraction. The -ITG copies of the test cases are carried by RWB-ITG-E1062-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E1-062 — the document input and the DocumentStored trigger (section 4 step 1 to step 3; AC3, AC7; BR2, BR7) | Sections 1, 2, 4, 7, 8, 16 |
| Event DocumentStored (EV-16) | Sections 4, 12.3, 17 |
| Type DEATH_CERTIFICATE, document D-1001, cases RW-2026-000401 to RW-2026-000404 | Background, sections 7 to 16 |
| Run key "SCREENING:<caseId>:<eventId>" | Sections 1, 2, 3, 4, 7, 8, 12.2 |
| MSG-P4-002, MSG-P4-003, MSG-GEN-006, MSG-P7-003 | Section 14, exception paths |
| TC-E1-062-01 to TC-E1-062-10 | Section 16 |

### 19. Out of scope

- The agent runtime, its policy, its prompt, its output schema, its guardrails, its owner-role resolution, its evaluation and its run states: RWB-P10-E1062-APP and the contract RWB-P10-E1062-CON.
- The deviation itself — registration, pause, handling, routing and clearing: RWB-S8-E1062-APP.
- The masking policy itself, its versions, its field list and its approval: RWB-P4-E1062-APP and the access and masking stories of P4; this slice consumes the decision and applies it.
- The intake, OCR, classification, extraction and review queue that produce the documents and fields read here: RWB-P5-E1049-APP, RWB-P5-E1050-APP and RWB-P5-E1053-APP.
- The store, the version rule, the write-once container, the retention classes and the custody of an original: RWB-P5-E1024-APP and the custody and retention stories of P5.
- The document type table load, its sign-offs and its versions: RWB-P5-E1025-APP.
- The gateway-bff composite route that a screen uses, the case documents screen and the document search screen: RWB-PLT-N001-CON, RWB-P5-E1026-APP and the edge stories.
- The end-to-end proof of these values across rwb-document, rwb-agent and rwb-source-data: RWB-ITG-E1062-ITG.
- The `rwb_document` schema baseline, the platform migration role, the `rwb.document.events.v1` topics and consumer groups, the observability and the runbook of this service.

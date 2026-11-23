# RWB-P5-E1021-APP Transfer rules and engine v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P5-F |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1021-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-CWC-010, REQ-CWC-016, REQ-WKM-003, REQ-CWC-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-021 for rwb-document — this slice delivers the document-received trigger of the transfer capability (the eighth TRANSFER trigger, rule row TRF-008 on event `DocumentStored`), published once per stored document, keyed by the case, carrying IDs and codes only. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR) and a case owner (RW-CASEOWN)**, I want **a document that is filed on a case to raise the document-received hand-off by itself — one event per stored document, keyed by the case, carrying IDs and codes only — so that the TRANSFER rule package can move the case without anyone watching the Documents tab**, so that **hand-offs between teams run without email and no document is filed twice or tied to a queue**.

Inside `rwb-document` this is the document-received trigger of the transfer capability:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The trigger is the legacy EV-16 fact `DocumentStored`: the document hub is the only source of "a document arrived", so the fact is published as `rwb.document.DocumentStored.v1` on `rwb.document.events.v1`, written to the outbox in the same transaction as the store and relayed with the CloudEvents 1.0 envelope. The event code that the TRANSFER package matches is `DocumentStored`, and the legacy rule row for it is TRF-008 (target queue `DIL-BKK-CO` in the legacy example).
- The transfer itself, the TRANSFER rule package, the assignment swap, the cap check, the hold check and the decision record are `rwb-case` (RWB-P3-E1021-APP). This slice fixes and proves the trigger contract, the once-per-store guarantee, the case key and the no-personal-data rule, and it registers the AsyncAPI document of the producer side of the topic.
- The publisher is built in RWB-P5-E1024-APP (the store). This story owns the conformance of the produced event to the trigger fixture of RWB-P3-E1021-CON, the guarantee that a repeat store of the same content publishes no second event, and the registration of the producer-side AsyncAPI document; it adds no store operation, no table and no consumer.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1037; ASM-1985); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

The legacy behaviour that this slice keeps is the one fact the transfer engine depends on: a stored document announces itself once, on the case, and the case owner's team decides what to do with it.

### 2. Business rationale

A case changes hands between the TDR, litigation, NPA and debt sale teams by email today, and the case can wait between teams with nobody holding it. One of the eight triggers of the TRANSFER package is document received, and the document hub is the only place that knows a document arrived. If the hub publishes that fact weakly — twice, without the case key, or with a file name or OCR text attached — the transfer engine either moves a case twice or carries personal data on a business-event topic. So the trigger has to be published exactly once per stored document, keyed by the case, with IDs and codes only, and the transfer decision itself stays where the rules are, in `rwb-case`.

This story is the rwb-document part of legacy RWB-E1-021. The same legacy key is split across services, and the slices are:

| Slice | What it owns |
|---|---|
| RWB-P3-E1021-APP and RWB-P3-E1021-CON | The TRANSFER package and engine, the eight triggers, the assignment swap, the cap check, the hold, the manual transfer and the decision record; the published shape of the trigger event and its fixture |
| RWB-P4-E1021-APP | The access decision for the transfer and legal-hold operations |
| RWB-P5-E1021-APP (this story) | The document-received trigger as produced by the document hub: `rwb.document.DocumentStored.v1`, once per store, keyed by the case, codes only |
| RWB-P7-E1021-APP | The central decision ledger of the transfers |
| RWB-S8-E1021-APP | The deviation-raised and deviation-cleared triggers |
| RWB-ITG-E1021-ITG | The end-to-end proof across the services |

It meets REQ-CWC-010 (the document-received trigger of the eight), REQ-CWC-016 (the trigger that lets the transfer record name its rule and version), REQ-WKM-003 and REQ-CWC-005 for the document part: a document carries no queue, team or owner, so a transfer leaves every document row where it is.

The realignment changes the mechanism, not the business rule:

1. The in-process listener of the monolith becomes the outbox and inbox library of DP-09: the outbox row is written in the store's transaction, the relay publishes at least once, and the consumer's inbox (rwb-case) drops a duplicate.
2. The legacy event name `DocumentStored` keeps its meaning; the topic and the event name become `rwb.document.events.v1` and `rwb.document.DocumentStored.v1` (DP-14), and the payload carries IDs and codes only (Architecture v5 slide 11: personal data in events is never allowed).
3. The order guarantee is per case: the record key is `caseId`, so two documents of one case are ordered for the consumer and documents of different cases are not.
4. Nothing in the document hub evaluates, caches or logs a TRANSFER rule. DP-04 and DP-03 do not build here; they apply as prohibitions (section 13).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E1021-CON | The published trigger contract of the TRANSFER capability: the event code `DocumentStored`, rule row TRF-008 and the trigger fixture the producer is checked against, with its fake (DP-11) |
| RWB-P5-E1024-APP | The store that writes the document row, the outbox row and the blob reference in one transaction; this story proves its trigger side and adds no store operation |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency-key library, with the retry topics and the dead-letter topic (DP-09) |
| RWB-PLT-E1047-CON | The topic naming library, so no topic name and no event name is typed in code (DP-14) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence in `rwb_document` (DP-15) |
| RWB-PLT-N008-INF | The schema registry with BACKWARD compatibility, so the producer's payload is validated against the registered schema |
| RWB-P5-E1025-APP | The document type table in force (version `DOCTYPE-2026.11`), so a stored document names a type from the table that is in force |
| The rwb-document login (DP-02) | The service identity that writes the outbox row and reads the type table; its name is Not specified in the source documents (GAP-1037; ASM-1985) |

Business preconditions carried from RWB-E1-021:

- Package TRANSFER version "TRF-2026.11" is in force in `rwb-case`, and the row that matches trigger `DocumentStored` is TRF-008, moving the case to queue `DIL-BKK-CO` in the legacy example (D-RCV-36 T5, first match in row order).
- The document type table in force holds the six agreed types (DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT, GUARANTOR_NOTICE) and LOV-DOC-SOURCE holds SCAN, UPLOAD, GENERATED, PARTNER and EMAIL, so a stored document names a code from each list and not a free text.
- The service baseline is delivered: the api and worker deployments, the `rwb_document` schema and its login, the topic and the retry topics of DP-09.

### 4. Flow

1. A document arrives on a case: a scan, an upload, a partner file, an email attachment or a generated document, with a type from the type table in force and a source from LOV-DOC-SOURCE.
2. The store of RWB-P5-E1024-APP writes the document row (document ID, case ID, type, source, storage reference, `content_sha256`, `doc_version`) and, in the same transaction, the outbox row for the trigger event; the unique partial index on the case, the type and the hash makes a second active document row for the same content impossible.
3. The transaction commits. Nothing is published that was not committed, and nothing committed stays unpublished (R-UNI-39 applied to the outbox).
4. The outbox relay reads the pending row and publishes `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` with the CloudEvents 1.0 envelope in binary mode (`ce_type` equal to the event name) and the record key `caseId`; the row moves from PENDING to PUBLISHED to DELIVERED.
5. `rwb-case`'s case router reads the event into its inbox, deduplicates by event ID, and builds the `TransferTrigger` fact with event code `DocumentStored`; the `CaseWorkflow` forwards it to the running stage child (RWB-P3-E1021-APP).
6. The `EvaluateRules` activity of `rwb-case` evaluates package TRANSFER for the fact and the business date and returns the first matching rule in row order — TRF-008 in the legacy example — with its rule ID and package version.
7. `rwb-case` applies the transfer, the assignment swap and the decision record; the document row, the blob reference and the type of the document are not touched.
8. A repeat store of the same content, type and case finds the active row through the unique index, returns the existing document and publishes no second event; the repeat is counted as an idempotency hit.
9. A document stored on a case that is already `CLOSED` still commits and still publishes the trigger: the document hub has no opinion on case status, and `rwb-case` answers the transfer with the refusal it already owns (MSG-P3-005, legacy X4).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A repeat store of the same case, type and content hash | The active row is returned; no second document row, no second event; the repeat counts as an idempotency hit | None | AC3 |
| X2 | The outbox relay is down | The committed row stays PENDING; the relay publishes when it returns; no event is lost and none is duplicated | None | AC1 |
| X3 | The store transaction rolls back | No document row and no outbox row exist; no event is published for it | None | AC1 |
| X4 | A stored document names a case the contract does not return | The store refuses the call; no document row and no event | MSG-P5-006 | AC2 |
| X5 | A stored document names a type that is not in force in the type table | The store refuses the call; no document row and no event | MSG-P5-006 | AC2 |
| X6 | A transfer happens after the store | No document row changes; the Documents tab of the case shows the same documents because the key is the case ID | None | AC4 |
| X7 | A malformed payload reaches the topic | The schema registry refuses it; the message goes to the retry topics (1 min, 10 min, 1 h) and then to `rwb.document.events.v1.dlt` with an alert | None | AC5 |

The store refusals of X4 and X5 are the store's own (RWB-P5-E1024-APP and RWB-P5-E1025-APP); they are repeated here because a refused store is also a document-received trigger that must not be published.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the trigger fixture of RWB-P3-E1021-CON and the outbox library; the store, the type table and the case side are contract fakes or already-delivered siblings |
| Negotiable | The field list of the payload, the retry schedule and the relay cadence come from the library and the fixture, not from this story |
| Valuable | The eighth TRANSFER trigger fires from the only place that knows a document arrived, once, with no personal data |
| Estimable | One factory, one schema, one contract test, one index reference and one registration |
| Small | Fits one sprint as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test with a fixture; the case side is stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1 — the document-received trigger from rwb-document

  Background:
    Given the rwb-case contract mock returns transfer rule "TRF-008" for trigger "DocumentStored"
    Given package TRANSFER version "TRF-2026.11" is in force in rwb-case and rule "TRF-008" moves a case to queue "DIL-BKK-CO"
    Given the document type table version "DOCTYPE-2026.11" is in force with type "COURT_NOTICE"

  Scenario: AC1 The document-received trigger is published once, keyed by the case (new, D-RCV-60)
    Given case "RW-2026-000314" is open and holds no court notice
    When a court notice of type "COURT_NOTICE" with source "SCAN" is stored for the case
    Then one outbox row is written in the same transaction as the document row
    And the relay publishes "rwb.document.DocumentStored.v1" on "rwb.document.events.v1" exactly once
    And the record key is the case "RW-2026-000314"
    And "ce_type" is "rwb.document.DocumentStored.v1" in the CloudEvents 1.0 envelope
    And the payload carries "documentId", "caseId", "documentType", "source" and "storedAt" only

  Scenario: AC2 The payload satisfies the TRANSFER trigger fixture (new, D-RCV-60)
    Given the TRANSFER trigger fixture of RWB-P3-E1021-CON names rule "TRF-008" and event "DocumentStored"
    When the event published for case "RW-2026-000314" is checked against the fixture
    Then the event code read by the fixture is "DocumentStored" and the case ID is "RW-2026-000314"
    And the document type read by the fixture is "COURT_NOTICE" and the source is "SCAN"
    And the producer contract test stays green with no mapping table in rwb-document

  Scenario: AC3 A repeat store publishes no second event (new, D-RCV-60)
    Given the court notice of AC1 was stored for case "RW-2026-000314" and one event was published
    When the same content of the same type is stored again for the same case
    Then the store returns the existing document and writes no second document row
    And no second "rwb.document.DocumentStored.v1" is written to the outbox and none is published
    And the repeat is counted as an idempotency hit

  Scenario: AC4 A transfer changes no document row (new, D-RCV-60)
    Given case "RW-2026-000314" is in queue "TDR-BKK-CO" and holds the stored court notice
    When rule "TRF-008" moves the case to queue "DIL-BKK-CO" in rwb-case
    Then the document row of the case is unchanged: same storage reference, same "content_sha256", same "doc_version" 1
    And the document row carries no queue, no team and no owner
    And the Documents tab of the case shows the same documents after the move

  Scenario: AC5 No personal data and no file content in the payload (new, D-RCV-60)
    Given a court notice stored for case "RW-2026-000314" from the scan intake, with OCR text and a field value in the case file
    When the payload of "rwb.document.DocumentStored.v1" is inspected field by field
    Then it holds no name, no address, no identity number, no account number, no amount, no file name and no OCR text
    And the schema registry accepts the payload against the registered schema under BACKWARD compatibility

  Scenario: AC6 A document stored on a closed case still publishes (new, D-RCV-60)
    Given case "RW-2026-000308" has status "CLOSED"
    When a court notice is stored for the case
    Then "rwb.document.DocumentStored.v1" is published once, keyed by "RW-2026-000308"
    And rwb-document publishes no case state change and consumes no event
    And whether the case moves, and the refusal that a closed case earns, are decided by rwb-case under rule "TRF-008"
```

The six criteria above are new and test only this deliverable: the produced trigger event, its conformance to the RWB-P3-E1021-CON fixture, the once-per-store guarantee, the case key, the no-personal-data rule and the closed-case behaviour. The legacy criteria of RWB-E1-021 are owned by the rwb-case slice (AC1 to AC14 of the legacy story are carried by RWB-P3-E1021-APP); the legacy exception X10 (no TRANSFER rule matches `DocumentStored`) is answered in `rwb-case`, where the event is published and the case keeps its queue and owner.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A document stored on a case raises the document-received trigger once, as a business event, written to the outbox in the same transaction as the store | EV-16 DocumentStored; REQ-CWC-010 |
| BR2 | The trigger event code is `DocumentStored`; the TRANSFER row that matches it is TRF-008 in the legacy package, and first match in row order is evaluated in rwb-case, never here | REQ-CWC-010; D-RCV-36 T5 |
| BR3 | The record key is the case ID, so events are ordered per case; a document never changes the key | Architecture v5 slide 11 (key = caseId, order per case) |
| BR4 | A repeat store of the same case, type and content hash returns the existing document and publishes no second event; the repeat counts as an idempotency hit | R-UNI-40; legacy AC8, AC11 and X5 |
| BR5 | The payload carries IDs and codes only: no name, address, identity number, account number, amount, file name or OCR text | Architecture v5 slide 11 (personal data in events is never allowed); DP-09 |
| BR6 | Nothing is published that was not committed, and a committed row stays pending until the relay publishes it; the consumer's inbox drops a duplicate | DP-09; R-UNI-39 (the same rule, applied to the outbox) |
| BR7 | A document carries no queue, no team and no owner; a transfer leaves every document row unchanged, and the Documents tab follows the case | REQ-CWC-005 |
| BR8 | The document hub consumes no event and publishes no case state change; the transfer, its rule ID and version and its decision record belong to rwb-case | REQ-CWC-016; D-RCV-36 T5 (executed in rwb-case) |

Statements that make the rules hold in `rwb-document`:

- BR1 and BR6 are executed by the outbox library of DP-09 in the store's transaction; the relay is the only publisher and it publishes from the committed row.
- BR4 is executed by the unique partial index `uk_document_case_type_hash` on `document (case_id, document_type, content_sha256) WHERE is_active`, added by the store's migration in RWB-P5-E1024-APP; this slice proves it and adds no duplication of the guarantee in code.
- BR5 is executed by the schema of the event (section 12.3) and by the schema registry, not by a filter in the publisher.
- BR8 is the reason this story has no `RuleEvaluator` call, no decision-record write and no case state in its payload.

### 9. State transitions

None for the case. The transfer state machine, the hold and the assignment move in `rwb-case` (RWB-P3-E1021-APP); the document hub holds no case state (TSD P5 T4).

The only state this story moves is the outbox row of the trigger event:

| From | Event | Condition | To |
|---|---|---|---|
| (none) | the store commits | The document row and the outbox row are written in one transaction | PENDING |
| PENDING | the relay picks the row up | Kafka accepts the record | PUBLISHED |
| PUBLISHED | the relay records the acknowledgement | `acks=all` acknowledged | DELIVERED |
| PENDING | the relay is down or Kafka is down | The row is not acknowledged | PENDING, retried; no loss and no duplicate |
| PENDING | the store transaction rolls back | The row never exists | (none) |

The document row itself has one version state that this slice reads and never changes: `doc_version` 1 on the first store, with a later version written by RWB-P5-E1024-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-document service identity (the rwb-document login, DP-02) | Writes the outbox row in the store's transaction, reads the type table in force, publishes through the relay. The login name is Not specified in the source documents (GAP-1037; ASM-1985) |
| SY-OCR OCR and extraction pipeline | Stores a document with right C (Documents CRU), so it raises the trigger (TSD P5 T6.1) |
| RW-CASEOWN case owner, RW-LITOFF litigation officer, RW-RESTRUCT restructuring officer | Store a document (Documents CRU) and read it (Documents R), so they raise the trigger |
| RW-TEAMMGR team manager, RW-HEADLIT Head of Litigation, RW-AUDIT internal audit | Read documents (Documents R); they raise no trigger from this slice |
| SY-CASEWF case workflow module | Reads documents (Documents R) on behalf of the case; the transfer it performs consumes the trigger in `rwb-case` |

SY-DECLOG is not used here: the document hub writes no decision-log entry in this slice, because it takes no decision. The authorisation decision for the store and the read is inherited from the service template (the cached permission decision from `rwb-access` through the shared guard of DP-08, delivered by the P5 baseline); this story adds no new right, no new operation and no guard of its own. The refusal shape stays 403 with MSG-P4-002, unchanged from the store's endpoint.

### 11. Data

| BR Field ID | Table in rwb_document | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Read (the `documentId` of the payload) |
| DF-DOC-002 | `document` | case_id | Read (the payload key and the record key) |
| DF-DOC-004 | `document` | document_type | Read (the type code of the payload) |
| DF-DOC-005 | `document` | source | Read (the source code of the payload) |
| DF-DOC-026 | `document` | content_sha256 | Read (the hash that makes the repeat detectable) |
| DF-DOC-011 | `document` | doc_version | Read |
| DF-REF-219 | `document_type` | doc_type_code | Read (the type must exist in the version in force) |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-REF-230 | `document_type` | valid_from | Read |
| DF-REF-231 | `document_type` | valid_to | Read |
| (outbox) | `outbox_event`, library table in `rwb_document` | event id, type, key, payload, status, attempts, created at | Write |
| (inbox) | `processed_event`, library table in `rwb_document` | event_id, consumer, processed_at | Not written; this service consumes no event |
| (idempotency) | `idempotency_key`, library table in `rwb_document` | the key of the store call that produced the event | Read |

`storedAt` in the payload is the `created_at` of the document row, read from the store's own transaction. The blob reference, the OCR text, the extracted fields, the custody rows and the retention class are not in this table list because none of them enters the event: the payload is IDs and codes only.

No table of another service is read (DP-01): the type codes come from `rwb_document.document_type`, the source codes from LOV-DOC-SOURCE held in this service's reference rows, and the case ID is a cross-reference value carried in the request and the row, with no foreign key into `rwb_case`.

### 12. Contract

#### 12.1 REST operations provided

None new. The store operation `POST /api/recovery/document/v1/documents` (returns the upload link) and the read operations of the hub belong to RWB-P5-E1024-APP and RWB-P5-E1026-APP; this slice adds no path, no query parameter and no response field. The only behaviour it fixes behind them is that a successful store publishes exactly one trigger event.

#### 12.2 REST operations consumed

None. The trigger is a Kafka fact, not a REST call: the document hub calls no service to publish it and calls no service to learn the case. The one hop and 2 s budget of DP-11 apply to the inbound store call only.

The trigger fixture of RWB-P3-E1021-CON is consumed as a test fixture, not as a call: it names the event code `DocumentStored`, the rule row TRF-008 and the field values the producer must produce.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` (legacy EV-16 `DocumentStored`) | `rwb.document.events.v1` | P5 | caseId | `documentId`, `caseId`, `documentType`, `source`, `storedAt` |

| Payload field | Type | Value in the legacy example |
|---|---|---|
| `documentId` | uuid | the document ID returned by the store |
| `caseId` | uuid | `RW-2026-000314` |
| `documentType` | varchar(30) | a code of the type table in force, for example `COURT_NOTICE` |
| `source` | varchar(12) | a code of LOV-DOC-SOURCE, for example `SCAN` |
| `storedAt` | timestamptz | the created date of the document row |

The field names above are restated from TSD P5 T3.1 and Architecture v5 slide 16; the producer-side AsyncAPI and JSON schema of the topic are not assigned to a contract story in this run, so the authoritative field names are Not specified in the source documents (GAP-1036; ASM-1984). The event name and the topic are from the naming library (DP-14), and the CloudEvents 1.0 envelope in binary mode carries `ce_type` equal to the event name, `ce_source` equal to the service name and `ce_id` equal to the event ID.

`rwb.document.DocumentFieldsExtracted.v1` is the hub's other event and belongs to the extraction stories; it is not part of this slice and carries no transfer meaning.

#### 12.4 Events consumed

None. The document hub consumes no topic for this capability: it publishes the fact and `rwb-case` reacts to it. A transfer of the case publishes `rwb.case.CaseTransferred.v1`, which this service does not read — no document row depends on the queue, the team or the owner.

#### 12.5 Workflows and activities

None. The store runs in the caller's request; the trigger is produced in that transaction and relayed by the outbox relay of DP-09. `DocumentIntakeWorkflow` runs in the hub for OCR, classification and extraction (Architecture v5 slide 16) and belongs to those stories; it neither produces nor consumes the trigger.

#### 12.6 Schedules

None. The relay is a continuous process of the service baseline, not a Schedule; the retention Schedule of the hub belongs to the retention story (Architecture v5 slide 16).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 (`rwb_document`) | Read the ID, case, type, source, hash and version of the stored document; no write (the store writes it) |
| `document_type` | P5 (`rwb_document`) | Read the type code and the version in force |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_document` | Outbox row for the trigger; inbox unused; idempotency key of the store |

The unique partial index `uk_document_case_type_hash` on `document (case_id, document_type, content_sha256) WHERE is_active` arrives with the store's migration in RWB-P5-E1024-APP; this story depends on it and proves the once-per-store guarantee through it, and adds no table, no column and no second index. No table of another service is read (DP-01).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| TRANSFER trigger fixture for `DocumentStored` and rule TRF-008 | RWB-P3-E1021-CON | The producer contract test: the event code, the case key and the five payload fields |
| outbox relay stub | RWB-PLT-TE006-CON | Publish, retry and dead-letter behaviour, and the PENDING to PUBLISHED to DELIVERED path |
| schema registry stub | RWB-PLT-N008-INF | Accept a conforming payload, refuse a malformed one, and check BACKWARD compatibility |
| store fake of the document hub | RWB-P5-E1024-APP | A committed store, a rolled-back store and a repeat store of the same content |
| type table fixture | RWB-P5-E1025-APP | The type codes in force (`DOCTYPE-2026.11`) and an unknown type |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 0 consumed | The store's operations belong to RWB-P5-E1024-APP; no new path and no outbound call |
| Kafka | 1 published, 0 consumed | `rwb.document.DocumentStored.v1` on `rwb.document.events.v1`; no subscription in this service |
| Temporal | None | No workflow and no activity in this slice |
| File | None | The blob write is the store's; this slice carries no file, only the storage reference as a row value it does not publish |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `store` (the trigger side).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| OutboxRelay client wiring | Configuration of the library | Registers the topic from the naming library, the retry topics and the dead-letter topic for the trigger event, and the relay that moves the row PENDING to PUBLISHED to DELIVERED |
| DocumentStoredFactory | Factory | Builds `DocumentStored` from the committed document row: the five fields, the case key and the event ID; the only place the payload is assembled |
| DocumentEventSchema | Schema binding | Binds the event to the registered JSON schema, so a field added or renamed fails the build and the contract test before it fails the registry |
| TransferTriggerContractTest | Contract test | Replays the RWB-P3-E1021-CON fixture against a real produced event and asserts the event code, the key and the five fields, with no mapping table in the service |
| StoreListener (test seam) | Test seam | Observes the store's commit so the once-per-store and the rolled-back-store cases can be asserted without a second store implementation |

**Database and migration notes**

- The outbox row is written by the store in its own transaction (DP-09); this story adds no table and no column. The library tables `outbox_event`, `processed_event` and `idempotency_key` arrive with RWB-PLT-TE006-CON, and the unique partial index `uk_document_case_type_hash` arrives with the store's migration in RWB-P5-E1024-APP.
- The migration this story registers in the per-service Flyway sequence of DP-15 is a no-op placeholder only if the library needs none; no business table is created here, so a rolled-back release leaves the store unchanged.
- Read-only access to `document` and `document_type` through the service's own repository; no foreign table (DP-01).

**Configuration**

- The topic and the event name come from the naming library (DP-14): no topic string, no event string and no `ce_type` value is typed in code.
- The retry schedule (1 min, 10 min, 1 h) and the dead-letter suffix are library parameters, not story values.
- The feature switch is `rwb.p5.transfer-trigger`, read as a parameter through the parameters contract. Off: the store commits the document and writes no outbox row, so no transfer trigger is published and the hub keeps its documents — the capability is removed without a schema rollback.

**Build steps**

1. `DocumentStoredFactory` from the committed row, with a unit test per field and a test that a field outside the five is not carried.
2. `DocumentEventSchema` and the registry binding, with a unit test for a malformed payload and a BACKWARD-compatibility check.
3. Outbox and relay wiring for the trigger, with a test for the committed row, the relay-down case and the rolled-back store (AC1).
4. `TransferTriggerContractTest` against the RWB-P3-E1021-CON fixture (AC2), run in every build.
5. The repeat store path, asserted through the unique index and the absence of a second outbox row (AC3).
6. The no-transfer-of-document-rows test against the rwb-case stub (AC4) and the no-personal-data test over the schema (AC5).
7. The closed-case test (AC6) and the dead-letter test for a malformed payload (X7).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice and it adds no new build dependency (metadata "Depends on (build)" = None): it builds against the trigger fixture of RWB-P3-E1021-CON and the service baseline, whose platform libraries (outbox, naming, Flyway) are part of the baseline of RWB-SVC-P5. The DPs that do not build here apply as prohibitions or statements:

- DP-01: the trigger reads `rwb_document.document` and `rwb_document.document_type` only; no `rwb_case` table and no other schema is read.
- DP-03: this slice writes no decision record — the TRANSFER decision record is `rwb-case`'s, in the same transaction as the transfer.
- DP-04: the document hub evaluates no Drools rule; the TRANSFER package stays in `rwb-case` and is never loaded, cached or called here.
- DP-05: no ACE view is read; the case ID is a value carried in the store request and the document row, and no `v_ace_*` view is named.
- DP-07: the type codes come from this service's own versioned `document_type` table and the source codes from this service's reference rows; no rwb-case reference-data call is made on the trigger path.
- DP-09: the one DP that builds here — the outbox row, the relay, the CloudEvents envelope and the key.
- DP-10: no Schedule here; the retention Schedule of the hub belongs to the retention story and the transfer timer is `rwb-case`'s.
- DP-11: no in-process call remains and no REST call is made; the one-hop and 2 s budget apply to the inbound store call, and the trigger is Kafka.
- DP-13: the store's base is `/api/recovery/document/v1`; the monolith base is not used anywhere in this slice.
- DP-14: no topic name and no event name in code; both come from the naming library.
- DP-15: no table of this story's own; the store's per-service migration sequence carries the index and the library carries its tables.
- DP-19: no screen in this slice; the Documents tab (SCR-30) is served through the gateway-bff composite route by RWB-P5-E1026-APP.

**Done when.** The tests in section 16 pass, the RWB-P3-E1021-CON trigger fixture round-trips against a real produced event, a SIT week shows exactly one `rwb.document.DocumentStored.v1` per stored document and none for a repeat store, the payload carries the five fields and no personal data, and the trigger fires rule TRF-008 for a case in the SIT environment.

### 14. Validation and messages

The trigger answers no caller: it has no user message, no HTTP status and no problem response of its own. A caller meets the store's messages, which this slice depends on and does not change:

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's role holds no Documents C right for the store | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is absent or outside the caller's scope | This case is not in your scope. |

A failed publish is not a user-visible error: the store answers the caller as soon as its transaction commits, and the relay retries. The dead-letter path raises an alert to the platform administrator (RWB-PLT-OBS), and a message that cannot be validated by the schema registry never reaches the topic's consumers.

### 15. Screens and states

No screen in this slice. The Documents tab (SCR-30) is delivered by RWB-P5-E1026-APP through the gateway-bff composite route of DP-19; it follows the case because its key is the case ID, so a transfer changes the queue and the owner of the case and leaves the documents where they are.

The state this slice makes observable to an operator is the outbox row of the trigger event: PENDING, PUBLISHED or DELIVERED, visible in the observability dashboards of the service (RWB-PLT-OBS), not on a Workbench screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-021-15 | Access — not this slice: the transfer endpoint's refusal stays with rwb-case and rwb-access; the document hub only publishes the trigger, and the caller who stores a document is refused by the store when the Documents C right is absent | Component | RW-CASEOWN calls POST /cases/{caseId}/transfer and is refused with MSG-P4-002 |
| TC-E1-021-01 | AC2, BR2 — the route-decided trigger is rwb-case's; here the same fixture shape is proved for `DocumentStored` and rule TRF-008 | Contract | Case in TDR-BKK-CO, route R4 approved; package TRANSFER "TRF-2026.11" |
| TC-E1-021-02 | AC2, BR1 — the manual transfer is rwb-case's; here the trigger that carries a reasonless fact is proved to carry the case and the type only | Contract | Manual transfer with R03 |
| TC-E1-021-03 | AC4, BR7 — one queue only is rwb-case's outcome; this slice proves that the document row carries no queue at all | Component | Two transfers on record version 7 |
| TC-E1-021-04 | AC1, AC2, BR1 — the eight triggers: here the `DocumentStored` row of the eight, published once with the case key | Contract | Eight TRANSFER rules |
| TC-E1-021-05 | AC4, BR7 — the hold and the status move in rwb-case; a document row carries no status, so hold, lift and reassign leave it unchanged | Component | Reassign, place hold, lift hold |
| TC-E1-021-06 | AC5, BR5 — the reason list is rwb-case's; the payload of the trigger carries no free text at all, so no reason can leak into it | Unit | No transfer reason |
| TC-E1-021-07 | AC5, BR5 — the cap check is rwb-case's; the payload carries no owner, so no cap value can appear in it | Unit | Owner U-24 at 150 |
| TC-E1-021-08 | AC3, BR4 — a repeat store of the same content returns the existing document and publishes no second event, which is the hub's half of the closed-case and repeat rules | Component | Closed case |
| TC-E1-021-09 | AC1, BR6 — the decision record is rwb-case's; the hub's guarantee is that a committed store always leaves a pending row and never a lost event | NFR | Decision log store down for a manual call |
| TC-E1-021-10 | AC6, BR1 — legal hold: the hub publishes regardless of hold and moves nothing, so a held case still receives its document trigger | Component | legal_hold = true and TimerDue |
| TC-E1-021-11 | AC3, BR4 — the repeated event: the once-per-store guarantee proves one event for one document, and the consumer's inbox proves one transfer for one event | Contract | Event EVT-88120 twice |
| TC-E1-021-12 | AC4, BR7 — the overflow queue is rwb-case's; the document row names no queue, so an overflow move changes no document | Unit | Every member of LIT-BKK-OFF at 150 |
| TC-E1-021-13 | AC4, BR7 — the hold refusal is rwb-case's; the hub has no status to refuse, and a document stored while a case is held still publishes | Component | Hold on a case on hold |
| TC-E1-021-14 | AC2, AC6, BR2 — no rule matches: the event is published, rwb-case finds no TRANSFER row, and the case keeps its queue and owner | Contract | DocumentStored with no rule |
| TC-E1-021-16 | AC1, BR6 — Principle 5 analogue: the decision record is rwb-case's; the hub's outbox guarantee is that a failed relay loses no event and duplicates none | NFR | Decision log write forced to fail for a rule transfer; event retried, case unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. Every legacy test case of this key is listed above with the slice of the behaviour this story answers; the -ITG copies of these cases are not here — they belong to the integration slice RWB-ITG-E1021-ITG, which proves the same values across rwb-case, rwb-access, rwb-document, rwb-decision and rwb-deviation end to end.

### 17. Guardrails

- No business value in code: the type codes, the source codes, the retry schedule and the topic name are data rows, library parameters and naming-library values. No queue, team, rule ID, field name or message text appears in Java.
- No personal data in events, workflow inputs, logs or tests: the payload is five fields of IDs, codes and a timestamp, and it carries no name, address, identity number, account number, amount, file name or OCR text. Test data uses synthetic keys (`RW-2026-000314`, `RW-2026-000308`).
- No cross-schema read (DP-01): `rwb_document` holds no foreign key into `rwb_case`, and the case ID is a value, not a join. The type table and the source list are this service's own.
- ACE data only through the owner's contract or `v_ace_*` views: this slice reads no ACE data and names no view — the document hub holds documents, not customer facts.
- One evaluator: the TRANSFER rule is never evaluated, cached or named in `rwb-document`. The document hub publishes a fact and has no rule engine on this path.
- Nothing is published that was not committed, and a committed row is never dropped: the outbox of DP-09 is the only publisher, and the schema registry is the only gate on the payload shape.
- The capability is removed by the feature switch `rwb.p5.transfer-trigger`, not by a rollback of the store.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-010 | Transfer by rule on eight triggers — document received is the one this slice produces — and manual request with a reason | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-40 | TC-E1-021-01, TC-E1-021-04, TC-E1-021-10, TC-E1-021-11, TC-E1-021-14 |
| REQ-CWC-016 | Every transfer logged with the rule ID and the rule version: this slice produces the fact that the record names | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-10 | All recovery processes | R-UNI-39 | TC-E1-021-09, TC-E1-021-16 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list: the document trigger carries no free text | Epic 2, work management | FEAT-CWC-10 | All recovery processes | VR-P3-010-1; DL23 | TC-E1-021-02, TC-E1-021-06 |
| REQ-CWC-005 | A case is in one queue with one open assignment: a document carries no queue, team or owner, so a transfer leaves it unchanged | Epic 1, 3.3 | FEAT-CWC-10 | All recovery processes | R-UNI-20 | TC-E1-021-03, TC-E1-021-05, TC-E1-021-12 |

| Legacy reference | Where it is kept |
|---|---|
| Trigger event `DocumentStored` (EV-16), the eighth trigger of the eight | Metadata, sections 1, 3, 4, 8, 12.3, 17 |
| Rule row TRF-008 and target queue DIL-BKK-CO | Background, AC1 to AC6, sections 8 and 16 |
| Queues TDR-BKK-CO, LIT-BKK-OFF, LIT-BKK-OVF and cases RW-2026-000308, RW-2026-000314 | Background, AC1 to AC6, section 16 |
| Rule IDs R-UNI-39, R-UNI-40 | Sections 8, 9, 18 |
| Document type table version DOCTYPE-2026.11, types and LOV-DOC-SOURCE | Preconditions, Background, AC2, section 11 |
| Legacy key RWB-E1-021, story RWB-P5-E1021-APP, contract RWB-P3-E1021-CON | Metadata, sections 3, 12, 19 |

### 19. Out of scope

- The TRANSFER package and engine, the eight-trigger fact, the assignment swap, the cap check, the hold, the manual transfer and the decision record: rwb-case (RWB-P3-E1021-APP) and its contract and operations stories (RWB-P3-E1021-CON, RWB-P3-E1021-OPS).
- The access decision for the transfer and the legal hold: rwb-access (RWB-P4-E1021-APP).
- The central decision ledger of the transfers: rwb-decision (RWB-P7-E1021-APP).
- The deviation-raised and deviation-cleared triggers: rwb-deviation (RWB-S8-E1021-APP).
- The store itself, its upload link, its blob containers and its unique index: rwb-document (RWB-P5-E1024-APP).
- The document type table and its load: rwb-document (RWB-P5-E1025-APP).
- The Documents tab and its searches: rwb-document (RWB-P5-E1026-APP).
- The end-to-end proof of the trigger across the five services: RWB-ITG-E1021-ITG.
- The producer-side AsyncAPI document as a published artefact of the platform event catalogue, and the schema registration: see GAP-1036.

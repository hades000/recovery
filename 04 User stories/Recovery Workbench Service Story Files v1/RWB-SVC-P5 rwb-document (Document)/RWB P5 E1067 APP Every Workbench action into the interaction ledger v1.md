# RWB-P5-E1067-APP Every Workbench action into the interaction ledger

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1067-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-067 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP15, DP18, DP19 |
| Parallel lane | L-P5-U |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P1-E1067-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the document half of RWB-E1-067 becomes the producer of `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` in the schema `rwb_document`, written to the outbox in the store transaction and keyed by caseId, while the ledger, the listener and the entry stay with rwb-source-data under DP-18. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every document attached to my case to reach the interaction ledger as one DOCUMENT_ATTACHED entry when it is attached, with the time and the actor that produced it**, so that **the case history shows the documents in order with everything else the Workbench did**.

This story is the `rwb-document` part of legacy RWB-E1-067 — the producer side of the DOCUMENT_ATTACHED ledger entry:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- What this story owns is one fact, written once and carried faithfully: a `rwb.document.DocumentStored.v1` event that carries the header the listener needs — a stable event ID, the idempotency key, the schema version, the occurred time and the actor — and the payload facts documentId, caseId, type and source, written to the outbox in the same transaction as the `document` row and keyed by caseId so the entries of a case stay in order.
- What this story does not own, and must not build, is the ledger itself. The ledger listener, the event-to-entry map, the duplicate service, the exception queue and the incident are rwb-source-data's, in RWB-P1-E1067-APP; the timeline read is rwb-case's, in RWB-P3-E1067-APP. This service writes no interaction row and holds no ledger (DP-18).
- The store that produces the document row is RWB-P5-E1024-APP; the type row that gives the type and the retention class is RWB-P5-E1025-APP; the upload screen is RWB-P5-E1026-APP; the intake that calls the store as SY-OCR is RWB-P5-E1049-APP. This story adds the event to the store transaction those stories already commit.
- The event carries references and codes only: the document ID, the case ID, the type code from LOV-DOC-TYPE and the source code from LOV-DOC-SOURCE. No person name, no account number, no identity number, no extracted field value and no file content is in the payload, in the header or in the log.

The legacy behaviour that stays here is BR1 to BR7 of RWB-E1-067 as seen from the producer: one attachment is one entry, the entry names its producer, a repeat gives one effect and a counted hit, the entries of a case keep their order, a failure retries and then reaches the exception queue, the schema accepts the current and the previous version, and the payload carries references and codes and no personal data. Everything those rules say about the *consumer* — the append, the `case_seq`, the hit table, the incident LEDGER_WRITE_FAILED — is the other slice's.

### 2. Business rationale

The case owner reads one case history. The Workbench attaches documents by rule as well as by hand: the OCR pipeline attaches a read document automatically (FEAT-DCM-12), a user uploads one from the Documents tab (FEAT-DCM-04), and a generated treatment document is stored the same way. If none of these attachments reaches the ledger, the case owner sees a customer contact on 3 December and cannot see that a court notice arrived on 4 December, or that the Workbench filed an appraisal report between them. REQ-ILG-005 asks that every Workbench action on a case is written to the ledger as it happens; REQ-ILG-002 asks that every entry names the system or person that produced it; REQ-ILG-007 asks that the same event twice with the same key gives one entry and counts the repeat.

Legacy RWB-E1-067 answered all three with one listener over one in-process outbox and one event set, with EV-16 DocumentStored mapped to DOCUMENT_ATTACHED (legacy AC1) and source reference "the owning module, event ID and event name" (legacy AC2). In the target the same six events travel on three independent streams from three producers: `rwb.case.events.v1` from rwb-case, `rwb.document.events.v1` from rwb-document and the shared `rwb.decision-record.v1` from every service's local decision record. The ledger does not move — DP-18 and the Template and Rules default ruling keep `interaction` and its writer in `rwb_source_data` — so the split does not weaken the rule; it changes what each service owes the listener. For rwb-document that debt is exact and small: a correct event, with a correct header, in the right order, in the same transaction as the row, once per document row.

The architecture fixes each part of the debt. Every producer writes to its transactional outbox in its own schema in the same transaction as the state change, and a relay publishes to its topic; the envelope is CloudEvents 1.0 in binary mode, the key is caseId, the registry keeps JSON Schema with BACKWARD compatibility, and every consumer dedupes in its inbox (Architecture v5 slide 11). The document topic carries DocumentStored and DocumentFieldsExtracted (slide 13), the event catalogue names DocumentStored as event 16 on `rwb.document.events.v1` (slide 42), and JOB-11 Outbox sender runs every minute in every service (slide 44). The functional source states the same fact in one line: on a store, "DocumentStored is written to the outbox with the document ID, the case ID, the type and the source" (FSD P5 A2.1, criterion AC-P5-001-01).

This slice therefore carries no business decision of its own and needs none: it carries a contract. Its value is that the ledger can be trusted to be complete for documents — the one category of Workbench action that arrives from a service other than the case service — without rwb-source-data ever reading `rwb_document`, without rwb-document ever writing `rwb_source_data`, and without either service sharing a table (DP-01, DP-18). It meets REQ-ILG-005, REQ-ILG-002 and REQ-ILG-007 for the document event only.

### 3. Preconditions

- RWB-P1-E1067-CON is published: the rwb-source-data contract of this legacy key, which fixes the ledger write path the listener runs, the event-to-entry map (EV-16 to DOCUMENT_ATTACHED), the duplicate rule of R-UNI-40, the Case record C authority behind the writer and the entry's source reference form. The append operation and the field names of its request are the CON story's; this service neither calls them nor restates them (DP-11 as a contract dependency, not a call).
- RWB-PLT-TE006-CON is in place: the outbox, inbox and idempotency library that creates `outbox_event`, `processed_event` and `idempotency_key` in `rwb_document` and provides the relay client of JOB-11 (DP-09). The three tables exist at the `rwb_document` baseline and this story writes no DDL for them.
- RWB-P5-E1024-APP is done: the store writes the decision record (DP-03), the `document` row and the outbox row in one transaction, and resolves the case through the rwb-case contract `GET /cases/{caseId}` before the row exists. This story adds the DocumentStored row to that transaction; it does not change the store.
- RWB-P5-E1025-APP is done: document type table version DOCTYPE-2026.11 is in force with the six types, the write-once flag and the retention class of each type. The type code in the payload is the type row the store read in the version in force.
- LOV-DOC-TYPE and LOV-DOC-SOURCE are read through the reference-data contract of rwb-case (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON); no type code and no source code is written in code. The six type codes and the five source codes are the values of TSD P5 T3.2.
- The topic `rwb.document.events.v1` exists with its retry topics and its `.dlt` topic, and the JSON Schema registry subject for the topic is registered with BACKWARD compatibility (Architecture v5 slide 11; RWB-PLT-TE006-CON). The schema version of the DocumentStored type is 1.
- The caller is the intake as SY-OCR (Documents CRU, TSD P5 T6.1) or a user identity with Documents C through `POST /cases/{caseId}/documents` (API-P5-001); a version add reaches the store as Documents U through `POST /documents/{documentId}/versions` (API-P5-005).
- The feature switch `rwb.document.ledger-events` can stop the event without touching the store: off means the document row and the decision record are committed and no outbox row is written, and the store answers as it does today.
- The names of the CloudEvents attributes that carry the idempotency key, the actor and the occurred time on this topic, and the exact idempotency-key format of DocumentStored, are Not specified in the source documents (GAP-1055; ASM-2003) and (GAP-1056; ASM-2004).

### 4. Flow

1. Caller: the intake stores a document as SY-OCR through the store command of RWB-P5-E1024-APP, or a user with Documents C uploads one with `POST /api/recovery/document/v1/cases/{caseId}/documents` (API-P5-001), or a user with Documents U adds a version with `POST /api/recovery/document/v1/documents/{documentId}/versions` (API-P5-005).
2. `DocumentStoreService` of RWB-P5-E1024-APP resolves the case through the rwb-case contract and reads the type row in the version in force; the row's `case_id` is the resolved case, so the event can never name a case the store did not resolve.
3. `DocumentStoreService` opens one transaction in `rwb_document` and writes the decision record through the decision-record library (DP-03) and the `document` row with its `doc_version`, `document_type`, `source` and `content_sha256`.
4. `DocumentStoredEventFactory` builds the payload from the row it is given, not from a fresh read: documentId from DF-DOC-001, caseId from DF-DOC-002, type from DF-DOC-004 and source from DF-DOC-005. Nothing else leaves the row — not the hash, not the storage reference, not the party reference.
5. `EventHeaderBuilder` sets the header: an event ID that is new for this committed row, the idempotency key of the row, the schema version 1, the occurred time of the change and the actor. The actor is the caller identity of the store: "SY-OCR" for the intake path and the user id for an upload, never a person name (AC2).
6. `CaseKeyedPartitioner` fixes the key of the record to caseId, so every event of one case lands on one partition and the relay preserves the written order of that case (AC5, BR4).
7. `OutboxEventWriter` inserts one row into `outbox_event` inside the same transaction, with the CloudEvents attributes and the payload, in state pending. The row, the document row and the decision record commit together or not at all.
8. Commit. Nothing leaves the service at this point; the event exists exactly when the document row exists, and a rolled-back store leaves no outbox row.
9. JOB-11 Outbox sender: the platform relay runs every minute in the service, publishes every pending row to `rwb.document.events.v1` in the CloudEvents 1.0 binary envelope with acks=all, and marks the row published. A publish that fails leaves the row pending and it is retried on the next run (BR5).
10. rwb-source-data listener: receives DocumentStored, checks the schema version against the current and the previous version, maps EV-16 to DOCUMENT_ATTACHED, sets the source system WORKBENCH, the source reference "P5 document hub, EV-16 DocumentStored" and the actor from the header, and appends one entry (RWB-P1-E1067-APP; not this story).
11. Redelivery: the same event arrives again with the same event ID and the same idempotency key. The listener writes no second entry and adds one hit for the key (R-UNI-40). This service has produced nothing new: it wrote one outbox row for one document row.
12. A store transaction retried by the caller's `Idempotency-Key`: the store's duplicate check returns the existing document and writes no second row and no second outbox row, so the case still holds one DocumentStored event for that document (AC3).
13. A second, different document attached to the same case: a second document row and a second outbox row, with its own event ID and its own idempotency key, keyed to the same caseId and published after the first (AC4).

Two statements complete the flow for a reader who owns the other side:

- A document of an unknown case never happens on this side. The store resolves the case before it writes the row, the row's `case_id` is that resolved case, and the key sits inside the row of `rwb_document` with no foreign key into `rwb_case` (DP-01). The listener's legacy "case not found" path (legacy AC8) therefore cannot be caused by this producer.
- A failed publish never loses the event. It stays in `outbox_event` in state pending, the relay retries it every minute, and only the relay's own limit moves it to a failed state and to the platform's exception queue (BR5, AC7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The store transaction rolls back after the row is built | No document row, no decision record and no outbox row exist; no event is ever published for that attempt | None | AC3 |
| X2 | The same store command is retried with the same `Idempotency-Key` | The existing document is returned; one outbox row stays; one entry in the ledger | None | AC3 |
| X3 | The store commits but the event payload cannot be built from the row (for example a type code outside LOV-DOC-TYPE) | The transaction aborts on the payload rule; nothing is stored; the type table version is the cause and is named in the log | None (build and store failure) | AC1 |
| X4 | The relay cannot reach the broker | The row stays pending; the next run publishes it once; no duplicate row and no duplicate event | None (relay incident on the platform side) | AC3, AC7 |
| X5 | The registry rejects the schema version of the row | The relay does not publish; the row stays pending and the platform alerts on the registry subject; no event leaves with a version outside the registry | None (platform alert) | AC6 |
| X6 | The same event is redelivered by the broker | The listener writes no second entry and counts one hit (R-UNI-40); this service is unaffected | None | AC4 |
| X7 | The listener cannot append the entry | The listener retries and then moves the event to its own exception queue with an incident; this service has published as designed and the event is not lost | MSG-P1-022 (the listener's incident detail) | AC7 |
| X8 | An identity without the Documents right calls the upload or the version add | Refused before the store; no row, no decision record and no event | MSG-P4-002 | AC2 |
| X9 | The case is outside the caller's scope | Refused with 403 before the store; no row and no event | MSG-P4-003 | AC2 |
| X10 | The decision record cannot be written | The store transaction aborts; nothing is stored and no event is published (R-UNI-39) | MSG-P7-003 | AC1 |
| X11 | The rwb-case contract does not answer inside 2 s | The store refuses with 503; no row and no event | MSG-GEN-006 | AC1 |

The last three rows belong to the store of RWB-P5-E1024-APP and are quoted here only because the event inherits them: an event exists exactly when a document row exists, so every path that stops the row stops the event with it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published rwb-source-data contract RWB-P1-E1067-CON, the outbox library RWB-PLT-TE006-CON and the store of RWB-P5-E1024-APP, all earlier or contract work |
| Negotiable | The topic name, the schema version, the relay interval and the retry limit are configuration and parameters; the story fixes the payload, the header, the key and the transaction |
| Valuable | Every document attached to a case reaches the case history as one entry with its time and actor, from the first day of wave 1 |
| Estimable | One event factory, one header builder, one outbox writer, one partitioner and one contract test |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Each criterion in section 7 is one automated test over the outbox row and the published envelope, with the ledger side stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Every Workbench action into the interaction ledger — the rwb-document DocumentStored event

  Background:
    Given the rwb-source-data contract mock returns the ledger write path of RWB-P1-E1067-CON for a received event
    Given the rwb-source-data contract mock returns that "rwb.document.DocumentStored.v1" maps to entry DOCUMENT_ATTACHED with source system "WORKBENCH"
    Given the rwb-source-data contract mock returns one entry per idempotency key and one hit for a key it has already seen

  Scenario: AC1 DocumentStored carries the header and the payload the listener needs (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the ledger write path for entry DOCUMENT_ATTACHED
    Given document "DOC-SYN-3011" of case "RW-2026-000301", type "COURT_NOTICE" and source "SCAN" is attached at 2026-12-04T09:30+07:00 by "SY-OCR"
    When the document row of "DOC-SYN-3011" is stored in one transaction
    Then one outbox row holds "rwb.document.DocumentStored.v1" with an event ID, an idempotency key, schema version 1, the occurred time 2026-12-04T09:30+07:00 and the actor "SY-OCR"
    And the payload carries documentId "DOC-SYN-3011", caseId "RW-2026-000301", type "COURT_NOTICE" and source "SCAN", and nothing else
    And the payload and the header carry no person name, no account number, no identity number, no extracted field value and no file content
    And the rwb-source-data contract mock returns one DOCUMENT_ATTACHED entry for case "RW-2026-000301" with source system "WORKBENCH" and source reference "P5 document hub, EV-16 DocumentStored"

  Scenario: AC2 The actor is the caller, never a person name (new, D-RCV-60)
    Given the OCR path of the intake stores a document for case "RW-2026-000301"
    Given a user identity "u-teammgr-03" with Documents C uploads a document for the same case
    When both document rows are stored
    Then the event of the OCR path carries the actor "SY-OCR"
    And the event of the upload carries the actor "u-teammgr-03"
    And no event, header, log line or test fixture of this story carries a person name
    And an identity without the Documents right is refused with MSG-P4-002 before any row is written, and a case outside the caller's scope with MSG-P4-003

  Scenario: AC3 The event is written in the store transaction and published within one minute (new, D-RCV-60)
    Given the document store of case "RW-2026-000301" commits one document row for document "DOC-SYN-3011"
    When the store transaction commits and JOB-11 Outbox sender runs
    Then exactly one outbox row exists for that document row, in the same transaction as the "document" row and the decision record
    And the relay publishes it to "rwb.document.events.v1" within one minute and marks the row published
    And a store transaction that is rolled back leaves no outbox row and no event
    And a store command retried with the same Idempotency-Key leaves one document row and one outbox row
    And the retry limit of the relay is read as a parameter, not written in code

  Scenario: AC4 One effect per document row, a counted hit on a redelivery (new, D-RCV-60)
    Given the event of document "DOC-SYN-3011" was published with its event ID and idempotency key
    When the broker redelivers the same event with the same event ID and the same idempotency key
    Then the event ID and the idempotency key of that document row are unchanged and this service publishes nothing new
    And the rwb-source-data contract mock returns one DOCUMENT_ATTACHED entry for case "RW-2026-000301" and one hit counted for that key (R-UNI-40)
    And a second attachment of a new document "D-1001" on the same case produces a second event with its own event ID and its own idempotency key

  Scenario: AC5 The event is keyed by caseId, so the entries of a case keep their order (new, D-RCV-60)
    Given case "RW-2026-000301" is created, allocated, then receives document "DOC-SYN-3011", then a decision
    When the three producers publish their events and one consumer group reads them
    Then every event of this story carries case "RW-2026-000301" as its key
    And the rwb-source-data contract mock returns DOCUMENT_ATTACHED after CASE_CREATED and CASE_ALLOCATED and before DECISION_TAKEN for the same case
    And two documents attached to the same case in one minute are published in the order their rows were committed

  Scenario: AC6 Schema version 1, and the registry rule is BACKWARD (new, D-RCV-60)
    Given the DocumentStored type of "rwb.document.events.v1" is registered at schema version 1
    When a document is stored by the released producer
    Then the event carries schema version 1
    And the listener accepts the current version 1 and the previous version of the type
    And a document stored by a producer version that would publish a version outside the registry is rejected by the broker and the registry rule — the relay does not publish it and the row stays pending
    And the contract states the BACKWARD compatibility rule of the registry subject

  Scenario: AC7 The entry is rwb-source-data's; this service only produces the event (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the ledger write path of RWB-P1-E1067-CON
    When a document is stored for case "RW-2026-000301"
    Then rwb-document writes the document row, the decision record and the outbox row, and writes no interaction row
    And rwb-document holds no ledger, reads no "rwb_source_data" table and calls no ledger writer
    And the rwb-source-data contract mock returns one entry appended by the listener through its own writer with the Case record C authority, with its own exception queue and its own incident at its side
    And a document whose case is unknown never happens here, because the store resolves the case before the row and the reference sits inside "rwb_document"
    And a failed publish leaves the event in the outbox, never lost, and the incident is the relay's, not a message to the user
```

The seven criteria above are new and test only this deliverable: the payload, the header, the transaction, the key, the version and the prohibition of a second ledger. No legacy criterion text of RWB-E1-067 is copied into this section; the legacy ACs 1 to 8 belong to RWB-P1-E1067-APP, which owns the listener, the map, the duplicate table, the exception queue and the incident, and to RWB-P3-E1067-APP for the timeline. Values reused here are the ones the sources already carry: case "RW-2026-000301", document "DOC-SYN-3011", the attachment time 2026-12-04T09:30+07:00, the actor "SY-OCR", the user id "u-teammgr-03", the entry codes CASE_CREATED, CASE_ALLOCATED, DOCUMENT_ATTACHED and DECISION_TAKEN, the source system "WORKBENCH" and the type and source codes of LOV-DOC-TYPE and LOV-DOC-SOURCE.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document attachment writes a ledger entry as it happens; here one event per document row, written in the transaction of the attachment (legacy BR1) | REQ-ILG-005; FSD P5 AC-P5-001-01; legacy BR1 |
| BR2 | The entry names the system or person that produced it; the event header carries the actor — a service identity for the OCR path and a user id for an upload — and never a person name (legacy BR2) | REQ-ILG-002; TSD P5 T6.1; legacy BR2 |
| BR3 | The same event with the same key produces one entry and the repeat is counted; the producer keeps the event ID and the idempotency key stable for one document row (legacy BR3) | R-UNI-40; REQ-ILG-007; legacy BR3 |
| BR4 | Events for one case are processed in the order they were written; the document event is keyed by caseId and holds the written order of that case (legacy BR4) | Events rule "Ordering"; Architecture v5 slide 11; legacy BR4 |
| BR5 | A consumer failure retries and then goes to the exception queue with its owner; on this side the event waits in the outbox and is retried by the relay, never lost (legacy BR5) | Events rule "Failure"; R-UNI-36; legacy BR5 |
| BR6 | The producer writes schema version 1, the consumer accepts the current and the previous version, and the registry keeps BACKWARD compatibility (legacy BR6) | Events rule "Versioning"; Architecture v5 slide 11; legacy BR6 |
| BR7 | Event payloads carry references and codes and no personal data: the document ID, the case ID, the type code and the source code (legacy BR7) | Events rule "Payload"; Architecture v5 slides 11 and 42; legacy BR7 |
| BR8 | DP-09: the event is written to the outbox in `rwb_document` in the same transaction as the row, and JOB-11 Outbox sender publishes it every minute | DP-09; Architecture v5 slides 11, 20 and 44 |
| BR9 | DP-18: the interaction ledger is rwb-source-data's; this service writes no interaction row, holds no ledger and calls no ledger writer | DP-18; Template and Rules R3 default ruling |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by one outbox row per committed `document` row and by nothing else: there is no second path that writes DocumentStored, no manual re-send and no batch that regenerates events for old rows. A version add writes its own document row and therefore its own event, because the ledger needs to show the new version arriving.
- BR2 is executed by `EventHeaderBuilder` taking the actor from the caller identity of the store — the SY-OCR workload identity on the intake path and the authenticated user id on the upload path — and by the store refusing to substitute a display name. The matrix of TSD P5 T6.1 gives SY-OCR Documents CRU and the roles with Documents C the upload; SY-AGENT holds Documents R and cannot reach the store at all.
- BR3 is executed by deriving both the event ID and the idempotency key from the document row, so a redelivery of the same event carries the same pair and the listener's unique key gives one entry and one hit. A new document row gives a new pair by construction.
- BR4 is executed by `CaseKeyedPartitioner`: the record key is caseId, so the events of one case share a partition and the relay's order per key becomes the written order of the case. The listener assigns `case_seq` in that order, which is why this story may not choose a document-scoped key.
- BR5 is executed on this side by the pending-to-published loop of the relay: a failed publish changes nothing in the row and is retried on the next minute. The retry topics, the count and the `.dlt` topic are the consumer's and the platform's (R-UNI-36); the relay's own limit is a parameter (AC3).
- BR6 is executed by the schema version being a constant `1` of the published type and by the registry subject being registered with BACKWARD compatibility: a consumer on version 1 keeps reading while a later producer adds optional fields, and a version the registry does not hold is never published.
- BR7 is executed by the payload being built from four columns of the row and by nothing else — no hash, no storage reference, no party reference, no extracted value. A personal-data pattern in the payload, the header or a log line fails the build's test of AC1.
- BR8 is the reason the store transaction, and not the after-commit step, writes the event: the outbox row commits with the row, so a crash between commit and publish loses nothing.
- BR9 is a prohibition with an owner elsewhere: DP-18 makes the ledger rwb-source-data's, so this service may not append, may not hold a copy and may not call the writer. The only permitted act on the ledger's behalf is publishing a good event.

### 9. State transitions

No case transition: this story changes no case status and moves no stage. It adds the lifecycle of one outbox row and reads the lifecycle of the document row it describes.

| From | Event | Condition | To |
|---|---|---|---|
| (no outbox row) | the store transaction commits | The document row, the decision record and the outbox row commit together | outbox row `pending` |
| pending | JOB-11 Outbox sender publishes the row to `rwb.document.events.v1` | The broker accepts with acks=all and the registry holds the schema version | `published` |
| pending | the publish fails (broker unreachable, registry refusal, timeout) | The row is unchanged and the next run retries it | `pending` |
| pending | the relay reaches its parameterised limit | The platform owns the item from this point; the event is not discarded | `failed`, and the relay incident is raised |
| published | a consumer redelivers the event | At-least-once delivery | `published`; no new row is written by this service |

Read-only, for the reader of the event:

| Document row state | What the event says |
|---|---|
| COPY_PENDING | The document exists and the event is published; the file copy is still pending and the event says nothing about it |
| STORED | The document exists with its storage reference; the event still carries only documentId, caseId, type and source |
| `is_active` = false (a superseded version) | The earlier row keeps its own event; the new version writes a new event, and neither is withdrawn |

The document row and the outbox row share one transaction, so there is no state in which a document exists without its event or an event without its document, except the deliberate case of the feature switch, where the row exists and the event is off.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Stores a document through the store command (Documents CRU, TSD P5 T6.1) and is the actor of the event it produces |
| The user identity of an upload (for example "u-teammgr-03") | Stores through API-P5-001 with Documents C, and is the actor of the event; the record carries the user id, never a person name |
| The user identity of a version add | Adds a version through API-P5-005 with Documents U, which writes its own document row and its own event |
| SY-AGENT, agent platform | Documents R: may read a document and may not attach one, so it produces no event and reaches no store |
| RW-PLATADM, platform administrator | Owns a failed item of the relay and of the `.dlt` topic of `rwb.document.events.v1`; Documents R in the matrix, and no write here |
| RW-CASEOWN, case owner | Documents CRU, and reads the DOCUMENT_ATTACHED entry through the P1 read on SCR-03 and SCR-04, not through this story |
| The rwb-document service identity (the rwb-document login, DP-02) | Writes the document row, the decision record and the outbox row in one transaction, and runs the relay client of JOB-11 |
| Nobody | Writes an interaction row, holds a ledger, or calls a ledger writer from this service (DP-18) |

The refusals are the store's and are quoted, not built, here: MSG-P4-002 for an identity without the Documents right (403), MSG-P4-003 for a case outside the caller's scope (403). MSG-P1-022 belongs to the listener's incident and appears in this story only as the text the consumer side shows. No role in this story may grant itself an event and no caller may name another actor in the header: the actor is the session's identity or the workload identity, never a field of the request.

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Write (the store), then Read into the payload as documentId |
| DF-DOC-002 | `document` | case_id | Write (the store), then Read as the payload caseId and as the record key |
| DF-DOC-004 | `document` | document_type (LOV-DOC-TYPE) | Write (the store), then Read into the payload as type |
| DF-DOC-005 | `document` | source (LOV-DOC-SOURCE) | Write (the store), then Read into the payload as source |
| DF-DOC-011 | `document` | doc_version | Read, to tell one version's event from another; not carried in the payload |
| DF-DOC-026 | `document` | content_sha256 | Read only for the duplicate check of the store; never carried in the payload |
| DF-OPS-178 to DF-OPS-183 | `outbox_event` and `processed_event` (PLT library) | the outbox row: event ID, event type, key, CloudEvents attributes, payload, state, occurred time, actor; and the inbox row: event ID, consumer, processed time, hit count | Write (the outbox row); Read (the inbox row in tests only) |
| DF-INT-014 to DF-INT-020 | `interaction`, schema `rwb_source_data` | event_code, actor_type, actor_ref, source_ref, idempotency_key, case_seq, decision_log_id | Never written here; named only as the listener's columns |

The row and the event carry different things on purpose. The `document` row holds the storage reference, the hash, the retention class and the party reference; the event holds four references and codes. DF-DOC-006, DF-DOC-009, DF-DOC-025 and DF-DOC-026 stay in `rwb_document` and never travel, because the ledger needs to know *that* a document arrived, of which type, from which source and when, and not what is in it. Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. The outbox, inbox and idempotency tables are the platform library's and are created in `rwb_document`; the legacy field IDs DF-OPS-178 to DF-OPS-183 were the monolith's `processed_event` and are kept here as the reference for the inbox row that the listener, not this service, writes in `rwb_source_data`.

### 12. Contract

#### 12.1 REST operations provided

No new path. The event rides the store operations of the `rwb-document` contract on base `/api/recovery/document/v1`, which this story does not change: it adds the outbox row inside their transaction.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P5-001 | POST | `/cases/{caseId}/documents` | Upload a document to the case; request multipart file, type and source; response Document; errors 401, 403, 404, 413, 415, 422, 503 | Documents, right C, scope applied | `Idempotency-Key` header |
| API-P5-005 | POST | `/documents/{documentId}/versions` | Add a new version of a document; request multipart file and reason; response Document; errors 401, 403, 404, 409, 415, 503 | Documents, right U, scope applied | `Idempotency-Key` header |

Both operations are the TSD P5 appendix T-A.2 shape, unchanged. What this story adds to them is not a field but a side effect with a contract of its own: the `rwb.document.DocumentStored.v1` event of 12.3, published once per document row that either operation commits. The request and response field names of the two operations are the API Specification's and are not restated here; the event is the contract this story owns.

A caller learns nothing new from the response: no event ID, no outbox reference and no ledger reference is returned. The event ID is the producer's business, and the ledger entry is the listener's.

#### 12.2 REST operations consumed

None at run time. This service calls no service to publish the event and calls no ledger writer (DP-18). Two contracts are consumed as facts and as fixtures:

| Fact | Owner | Story | Note |
|---|---|---|---|
| The ledger write path (`InteractionLedgerWriter.append` in the legacy story, published as a contract operation here) | P1 rwb-source-data | RWB-P1-E1067-CON | The reason the event exists: the listener turns it into one DOCUMENT_ATTACHED entry. This story neither calls it nor fixes its request or response field names; they are the CON story's. Used as a stub in every test of section 7 |
| The read of the interactions of one case | P1 rwb-source-data | RWB-P1-E1067-CON | Read by RW-CASEOWN on SCR-03 and SCR-04 through the P1 read and the gateway-bff route, not by this service |

The rwb-case contract `GET /cases/{caseId}` is consumed by the store of RWB-P5-E1024-APP, not by this story, and is named here only because the event's caseId comes from the case the store resolved.

#### 12.3 Events published

| Event | Topic | Key | Envelope | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentStored.v1` (event 16 of the catalogue) | `rwb.document.events.v1` | caseId | CloudEvents 1.0, binary mode (`ce_*` headers), `application/json` | documentId, caseId, type, source |

The CloudEvents attributes are fixed as follows; the attribute that carries the idempotency key, the one that carries the actor and the exact idempotency-key format are Not specified in the source documents (GAP-1055; ASM-2003) and (GAP-1056; ASM-2004).

| Attribute | Value |
|---|---|
| `specversion` | `1.0` |
| `id` | The event ID: one per committed document row, stable across every redelivery of that row |
| `source` | The rwb-document service identity and the service path that produced the event |
| `type` | `rwb.document.DocumentStored.v1` |
| `subject` | The case ID, so the subject of the envelope and the record key agree |
| `time` | The occurred time of the change: 2026-12-04T09:30+07:00 in the criterion, never the publish time |
| `datacontenttype` | `application/json` |
| `dataschema` | The registry subject of the type at schema version 1 |
| extension: the idempotency key | The key of the document row, stable across a redelivery and new for a new document (the attribute name is GAP-1055) |
| extension: the actor | "SY-OCR" or the user id of the upload (the attribute name is GAP-1056) |

AsyncAPI 3.0 fragment of the topic, owned by this service:

```yaml
asyncapi: 3.0.0
info:
  title: rwb.document events
  version: 1.0.0
channels:
  rwb.document.events.v1:
    address: rwb.document.events.v1
    messages:
      DocumentStored:
        $ref: '#/components/messages/DocumentStored'
operations:
  publishDocumentStored:
    action: send
    channel:
      $ref: '#/channels/rwb.document.events.v1'
components:
  messages:
    DocumentStored:
      name: DocumentStored
      contentType: application/json
      headers:
        type: object
        properties:
          ce_specversion: { const: '1.0' }
          ce_id: { type: string }
          ce_source: { type: string }
          ce_type: { const: 'rwb.document.DocumentStored.v1' }
          ce_subject: { type: string }
          ce_time: { type: string, format: date-time }
          ce_idempotencykey: { type: string }
          ce_actor: { type: string }
      payload:
        type: object
        required: [documentId, caseId, type, source]
        properties:
          documentId: { type: string }
          caseId: { type: string }
          type: { type: string }
          source: { type: string }
```

`DocumentFieldsExtracted` on the same topic is published by the extraction path (RWB-P5-E1050-APP), not by this story, and no other event of this service is touched here. The registry subject is registered with BACKWARD compatibility: a new optional field keeps version 1 readable for the listener, and a version the registry does not hold is never published (AC6). The event is written to the outbox in the store transaction, so it exists exactly when the document row exists.

#### 12.4 Events consumed

None. This story subscribes to no topic and creates no consumer group in `rwb_document`; the inbox table exists by the library and is written by no path of this story.

#### 12.5 Workflows and activities

None. The publish is the platform relay of JOB-11, not a workflow step, and the store transaction is synchronous in the caller's thread (DP-09). This story starts no activity, holds no Temporal worker and adds no task to queue `rwb-document`; the `DocumentIntakeWorkflow` and its `copyPending` activity belong to RWB-P5-E1049-APP and RWB-P5-E1024-APP.

#### 12.6 Schedules

None for this service in this story. The outbox relay is the platform Schedule every minute — JOB-11 Outbox sender, owner "every service", mechanism "outbox relay to Kafka" (Architecture v5 slide 44) — not a Schedule this story authors. The 15-minute document intake (JOB-12) and the monthly retention run (JOB-17) are other P5 stories'. The relay interval is configuration of the platform, and the value this story reads in tests is one minute.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `document` | P5 (`rwb_document`) | The row the event describes; RWB-P5-E1024-APP writes it, this story reads four of its columns |
| `outbox_event` | PLT library, created in `rwb_document` | The DocumentStored row, written in the store transaction (DP-09) |
| `processed_event` | PLT library, created in `rwb_document` | The inbox of this service; present and empty, because this story consumes nothing |
| `idempotency_key` | PLT library, created in `rwb_document` | The key of the POST operations, so a retried store writes one row and one event |

No foreign-schema table is read (DP-01). This service never reads `rwb_source_data`, and `interaction` and the listener's `processed_event` belong to rwb-source-data in its own schema. The `document_type` and `document_hub_parameter` rows are read by the store, not by this story.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-source-data ledger fake | RWB-P1-E1067-CON | The append path, the EV-16 to DOCUMENT_ATTACHED map, the one-entry-per-key and hit answers of every criterion; the "listener unavailable" path of X7 |
| outbox and relay stub | RWB-PLT-TE006-CON | A pending row that the stub publishes, a publish that fails once and then succeeds (X4), and a registry refusal (X5) |
| document store fixture | RWB-P5-E1024-APP | A committed document row for case "RW-2026-000301", the rolled-back transaction of X1 and the retried store of X2 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DOC-TYPE with the six types, LOV-DOC-SOURCE with SCAN, UPLOAD, GENERATED, PARTNER and EMAIL |
| document type fixture | RWB-P5-E1025-APP | Type "COURT_NOTICE" at version DOCTYPE-2026.11 |
| decision-record stub | RWB-PLT-E1027-CON | The DOCATT record in the store transaction, and the failed record of X10 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | The upload and the version add of the `rwb-document` contract on `/api/recovery/document/v1`; no outbound call, one hop within 2 s on the inbound call |
| Kafka | 1 published, 0 consumed | `rwb.document.DocumentStored.v1` on `rwb.document.events.v1`, key caseId, CloudEvents binary mode; no subscription of this service |
| Temporal | None | No workflow, activity or Schedule in this story; the relay is the platform's |
| File | None | The file itself is the store's and RWB-PLT-TE012-APP's; the event carries no claim-check link and no content |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `ledgerevents`, Java package `th.co.scb.ace.workbench.recovery.document.ledgerevents`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentStoredEventFactory | Service | Builds the payload from the committed `document` row: documentId, caseId, type, source, and nothing else; refuses a type or a source outside its list |
| EventHeaderBuilder | Service | Sets the event ID, the idempotency key, the schema version 1, the occurred time and the actor from the caller identity of the store; never a display name and never a person name |
| CaseKeyedPartitioner | Service | Fixes the record key to caseId and asserts that the subject of the envelope and the key agree, so the entries of one case keep their written order |
| OutboxEventWriter | Service | Inserts one `outbox_event` row in the caller's transaction in state pending; idempotent for a retried store command |
| RelayContractTest | Test component | Asserts the published envelope against the AsyncAPI fragment and the registry subject: attributes, key, payload and schema version, and the pending-to-published loop of the relay |

**Database and migrations.** None for this story, and that is the DP-15 statement: the per-service Flyway sequence of `rwb_document` is not extended here. `outbox_event`, `processed_event` and `idempotency_key` are created in the schema by the platform library at the `rwb_document` baseline (RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON for the sequence), and this story writes rows, not DDL. No column, index or constraint is added to `document`, and no migration of this service touches another schema.

**Configuration.**

- `rwb.document.events.topic` = `rwb.document.events.v1`; the retry topics and the `.dlt` topic are named by the platform naming library.
- `rwb.document.events.schema-version` = 1, the version of the published type; a version outside the registry is never published.
- `rwb.document.events.relay-interval` is the platform's one-minute Schedule of JOB-11, read as a property and not as a Schedule of this service.
- `rwb.document.events.retry-limit` is the relay's limit, read as a parameter; its value is Not specified in the source documents (GAP-1057; ASM-2005). The consumer-side retry limit of the legacy story is 3, with the cadence 1 min, 10 min and 1 h before the dead-letter topic (NFR-026), and it belongs to RWB-P1-E1067-APP.
- `rwb.document.events.idempotency-key` selects the derivation of the key from the document row; the exact format of the key of DocumentStored is Not specified in the source documents (GAP-1055; ASM-2003).
- The registry subject of the type and the path of the AsyncAPI document on this topic are Not specified in the source documents (GAP-1058; ASM-2006).
- Feature switch `rwb.document.ledger-events`, read as a parameter: off means the store commits the row and the decision record and writes no outbox row, so the ledger misses the document and the switch is visible in the runbook; it is never left off in SIT or production.

**Build steps**

1. `DocumentStoredEventFactory` over the `document` row, with a test per forbidden field (no hash, no storage reference, no party reference, no extracted value) and a test that a type or source outside LOV-DOC-TYPE or LOV-DOC-SOURCE aborts the transaction (X3).
2. `EventHeaderBuilder` with the event ID per row, the idempotency key of the row, the occurred time from the change and the actor from the identity; tests for AC1 and AC2, including the upload path with "u-teammgr-03".
3. `CaseKeyedPartitioner` and the key assertion; test that two documents of one case carry the same key and are published in commit order (AC5).
4. `OutboxEventWriter` inside the store transaction, with the rollback test (X1) and the retried store test (X2) of AC3.
5. The AsyncAPI fragment and the registry subject registration with BACKWARD compatibility; `RelayContractTest` asserting attributes, payload and version (AC6), and the "outside the registry" path (X5).
6. The relay wiring of JOB-11 with the pending-to-published loop and the parameterised limit; tests for the within-one-minute publish, the failed publish of X4 and the never-lost behaviour of AC7.
7. The negative tests of DP-18: no interaction row, no ledger table, no ledger writer call in any package of the service, and no read of `rwb_source_data` (AC7, and the call-graph assertion of the guardrails).
8. Contract-fake run of RWB-P1-E1067-CON, so the story proves the entry, the source reference and the hit before the listener is live; then the same run against the real topic in SIT.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: it adds no new build dependency of its own. Metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P1-E1067-CON` exactly as the Work Package fixes them, and the platform libraries of DP-03, DP-07, DP-09, DP-15 and DP-19 arrive with the baseline of `rwb_document`, not with this story.

DP-09 is the pattern that carries the story: the library gives the transactional outbox in `rwb_document`, the inbox table the service does not use and the relay client that JOB-11 runs every minute, and the topic `rwb.document.events.v1` with its retry and `.dlt` topics is the owner's channel under the CloudEvents 1.0 envelope. Everything this story asserts about order, duplicates and loss is a property of that pattern applied to one table.

DP-18 is a prohibition here and the reason the story is sliced this way: the interaction ledger belongs to rwb-source-data by the Template and Rules default ruling, so rwb-document may not append an entry, may not hold a ledger table and may not call the writer. The only permitted act on the ledger's behalf is the event, and the negative tests of the build exist to keep the boundary from eroding as later document stories are added.

DP-11 is the one-hop REST contract between the document API and its callers: the upload and the version add answer the caller in their own thread within 2 s, the store calls the rwb-case contract once and nothing chains. The ledger is deliberately *not* a REST call from this service — the event is the decoupling, and the listener runs on its own consumer group whenever it can.

DP-03 is present but not built here: the local decision record of the store (decision code DOCATT, final call STORED) is written by RWB-P5-E1024-APP in the same transaction as the row and the outbox row, and published on `rwb.decision-record.v1`. This story neither writes a record nor reads one; it relies on the record being in the transaction so the event and the record stand or fall together.

DP-07 keeps the type and source values out of the code: the type row is read from `document_type` in the version in force (DOCTYPE-2026.11), and the type and source codes are checked against LOV-DOC-TYPE and LOV-DOC-SOURCE through the reference-data contract of rwb-case. A new document type is a data row, not a release of this story.

DP-15 is the per-service Flyway sequence and its answer here is "no migration": the library tables arrive with the baseline, the service's sequence stays at the version it has, and no other schema is touched. That is the pattern applied as a boundary rather than as new DDL.

DP-19 is the gateway route the entry is read through elsewhere: SCR-03 Case record and SCR-04 read the ledger through the gateway-bff composite route, which calls rwb-source-data for the interactions and each owner for its own data, one hop each within 2 s. This story adds no route and publishes nothing to a screen; DP-19 is named because the reason the entry exists is that screen.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P1-E1067-CON and RWB-PLT-TE006-CON stay green, one stored document in SIT produces exactly one `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` within one minute with the header and the four payload facts and no personal data, a redelivery adds one hit and no entry, a rolled-back store produces no event, and no class of the service writes an interaction row or calls a ledger writer.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-022 | The listener cannot append the entry; carried on its incident and its exception queue item, quoted here as the consumer side | The entry was not saved because the interaction ledger could not be written. Try again in a few minutes. |
| MSG-P4-002 | An identity without the Documents right calls the upload or the version add | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is absent or outside the identity's scope | This case is not in your scope. |
| MSG-P7-003 | The decision record of the store cannot be written, so the store and its event do not proceed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The rwb-case contract does not answer inside 2 s, or a read of the document content is asked for while the copy is pending | {system} is not available. Your request is queued and will be retried. |

A publish failure surfaces as a relay incident on the platform side, not as a user message: the user's store already succeeded and the event waits in the outbox, so no screen shows an error for a late publish (AC7). For MSG-GEN-006 the {system} value is "Case service" on the contract timeout and "Document storage" on a pending copy; for MSG-P4-002 the {action} value names the action, for example "upload a document", and never a case fact or a role name. Thai text for each message follows decision DL10. This story adds no message ID of its own.

### 15. Screens and states

No screen in this story, and no state on a screen. The DOCUMENT_ATTACHED entry is read on SCR-03 Case record and SCR-04 by other stories — the timeline of RWB-P3-E1067-APP and the ledger read of RWB-P1-E1067-APP — and the document itself is read on SCR-30 Case documents (RWB-P5-E1026-APP). SCR-09 Exception queue belongs to the platform and shows a failed relay item to RW-PLATADM; this story creates no screen, changes no screen state and adds no field to any composite route.

The user-visible consequence of this story is indirect and worth one sentence in the test pack: a document uploaded on the Documents tab appears in the case history with the time it was stored and the identity that stored it, and the label of the entry is the ledger's, not this service's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-067-01 | AC1, BR1; here AC1, AC2, AC3 | End to end | Six synthetic events for case RW-2026-000301; the DocumentStored of document DOC-SYN-3011 at 2026-12-04T09:30+07:00 by SY-OCR; header, payload and outbox row asserted |
| TC-E1-067-02 | AC2, BR2; here AC1, AC2 | End to end | The CASE_ALLOCATED and CASE_TRANSFERRED entries of the legacy paired with the actor of the DocumentStored event: "SY-OCR" on the OCR path and "u-teammgr-03" on the upload path, no person name anywhere |
| TC-E1-067-03 | AC3, BR3; here AC4 | End to end | DocumentStored delivered twice with its event ID and its idempotency key; one entry and one hit (R-UNI-40), then a second document D-1001 with its own event ID |
| TC-E1-067-04 | AC4, BR6; here AC6 | End to end | A DocumentStored at schema version 1, a listener on version 1 and the previous version, and a producer version outside the registry that the relay refuses to publish |
| TC-E1-067-05 | AC5, BR5; here AC7 and the relay's side | End to end | A publish forced to fail; the row stays pending, the retry limit is the parameter, and no event is lost — The listener's half of this case belongs to RWB-P1-E1067-APP; this story covers the producer's half |
| TC-E1-067-06 | AC6, BR4; here AC5 | End to end | CaseCreated then CaseAllocated in the outbox, then DocumentStored for the same case: one key caseId, published after the earlier entries |
| TC-E1-067-07 | AC7, BR3; here AC4 | End to end | One event on two consumer threads; one entry and one hit — The listener's half of this case belongs to RWB-P1-E1067-APP; this story covers the producer's half |
| TC-E1-067-08 | AC8; here AC7 | End to end | DocumentStored for an unknown case ID 00000000-0000-0000-0000-000000000998: the store resolves the case before the row, so this producer never emits it — The listener's half of this case belongs to RWB-P1-E1067-APP; this story covers the producer's half |
| TC-E1-067-09 | Access; here AC7 | Component | SY-AGENT holds Documents R and may not attach a document; MSG-P4-002, no document row and no event — The listener's half of this case belongs to RWB-P1-E1067-APP; this story covers the producer's half |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end and Access to Component. Every one of the nine legacy cases of this key is listed above with the slice this story answers: the five producer-side cases keep their legacy wording and gain the half this story proves (TC-E1-067-01, -02, -03, -04 and -06), and the four cases whose behaviour is the listener's are kept with their legacy wording and marked with the listener's owner (TC-E1-067-05, -07, -08 and -09). The `-ITG` copies are not here; they belong to RWB-ITG-E1067-ITG, which proves the same values across rwb-source-data, rwb-case and rwb-document end to end.

### 17. Guardrails

- No business value in code: the topic name, the schema version, the relay interval, the retry limit and the idempotency-key derivation are properties and parameters; the type and source codes come from LOV-DOC-TYPE and LOV-DOC-SOURCE through the reference-data contract, and the type row from `document_type` in the version in force.
- Event payload rule: the payload carries documentId, caseId, type and source and nothing else. No hash, no storage reference, no party reference, no extracted field value, no file content and no claim-check link — the message never carries the data.
- No personal data in events, headers, logs, workflow inputs, tests or prompts. The actor is a service identity or a user id, never a person name; the case, the document and the time in every test are the synthetic values of the sources; a personal-data pattern in the payload or the header fails the build.
- The outbox row is written in the same transaction as the `document` row and the decision record: a rolled-back store leaves no event, and a committed store can never be missing its event. No after-commit send, no second producer of DocumentStored, no manual re-send.
- No direct ledger write: this service writes no interaction row, holds no ledger, reads no `rwb_source_data` table and calls no ledger writer (DP-18). The only permitted act on the ledger's behalf is the event, and a build that adds such a call fails.
- The idempotency key is derived from the document row and is stable for it across a redelivery; the event ID is new for a new document row and never reused. A retried store command writes one row and one event, and the listener counts one hit (R-UNI-40).
- The record key is caseId, never documentId: a document-scoped key would let the events of one case overtake each other and break the order the ledger needs.
- No cross-schema read (DP-01): the case and its scope come to the store through the rwb-case contract, and the event's caseId is the resolved case the store wrote into its own row.
- No consumer group, no inbox write and no subscription of this service: the inbox table exists by the library and stays empty, so a later story cannot mistake this service for a listener.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ILG-005 | Every Workbench action on a case writes to the ledger as it happens | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | R-UNI-36; legacy BR1, BR5, BR8 | TC-E1-067-01, TC-E1-067-05, TC-E1-067-06 |
| REQ-ILG-002 | Every entry carries case, event, time, actor and source | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-01 | All recovery processes | R-UNI-40; legacy BR2 | TC-E1-067-02 |
| REQ-ILG-007 | The same event twice with the same key gives one entry; the repeat is counted | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ILG-04 | All recovery processes | R-UNI-40; legacy BR3 | TC-E1-067-03, TC-E1-067-07 |

| Legacy reference | Where it is kept |
|---|---|
| Event DocumentStored (EV-16) and its payload of the document ID, the case ID, the type and the source | Background, sections 4, 11, 12.3, 17; FSD P5 A2.1 and AC-P5-001-01 |
| Event header: event ID, idempotency key, schema version, occurred time and actor | Sections 3, 4, 7 (AC1, AC4, AC6), 12.3, 13 |
| Entry code DOCUMENT_ATTACHED and source reference "P5 document hub, EV-16 DocumentStored" | Sections 4, 7 (AC1, AC5), 12.2, 16 |
| BR1 to BR7 of RWB-E1-067 as seen from the producer | Section 8, BR1 to BR7 |
| R-UNI-40 and R-UNI-36 | Sections 4, 7 (AC4), 8 (BR3, BR5), 18 |
| Legacy AC1 to AC8 and TC-E1-067-01 to -09 | Sections 16, 19; the listener's half in RWB-P1-E1067-APP and the timeline in RWB-P3-E1067-APP |
| MSG-P1-022, MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-GEN-006 | Section 14 |

The features the legacy story pairs with its requirements are FEAT-ILG-01 (write every Workbench event to the ledger) and FEAT-ILG-04 (reject a duplicate ledger entry); this slice answers them only for the DocumentStored event, and the listener that completes the answer for the case events and the decision record is RWB-P1-E1067-APP. The end-to-end proof of the same values across the three producers and the ledger is RWB-ITG-E1067-ITG.

### 19. Out of scope

- The ledger store and writer, the listener, the event-to-entry map, the duplicate service, the exception queue, the incident LEDGER_WRITE_FAILED and the `case_seq`: RWB-P1-E1066-APP, RWB-P1-E1067-CON and RWB-P1-E1067-APP.
- The timeline and the ledger read on the case record: RWB-P3-E1067-APP and RWB-P3-E2016-APP.
- The contact outcomes from EFS, the dispatch outcomes from WIN, SMS and LINE, and the partner hand-over entries: RWB-E2-034 and the new stories of that legacy key.
- The central decision ledger and the collection of the local records on `rwb.decision-record.v1`: RWB-P7-E1027-CON.
- The end-to-end proof of the event, the entry and the order across rwb-document, rwb-source-data and rwb-case: RWB-ITG-E1067-ITG.
- The store, the duplicate check, the version rules and the decision record of the store: RWB-P5-E1024-APP; the type table and the retention class: RWB-P5-E1025-APP; the upload screen: RWB-P5-E1026-APP; the intake that calls the store as SY-OCR and the `DocumentFieldsExtracted` event: RWB-P5-E1049-APP and RWB-P5-E1050-APP.
- The `rwb_document` schema baseline, the platform library tables, the topic, the retry and `.dlt` topics, the registry subject, the relay of JOB-11, the observability and the runbook of this service: the platform stories RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and the Kafka event platform epic.

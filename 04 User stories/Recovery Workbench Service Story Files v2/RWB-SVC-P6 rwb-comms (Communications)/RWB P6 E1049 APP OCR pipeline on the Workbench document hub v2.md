# RWB-P6-E1049-APP OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1049-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P6-F |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1049-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-DCM-006, REQ-DCM-009, REQ-DCM-010) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: rwb-comms slice of legacy RWB-E1-049, split out of the Epic 1 story for the Communications service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E1049-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 20 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the rescan notice of an unreadable page sent to me through the ACE notification path by rwb-comms, naming the page, the document and the case, and the notice readable back through the rwb-comms contract**, so that **a page below the OCR quality threshold is scanned again the same day and the notice that was sent can be proved**.

**The slice.** RWB-E1-049 builds the OCR pipeline of the Workbench document hub. In the target the pipeline stays with P5 `rwb-document`: `rwb-document` owns the OCR pipeline, `document_intake`, `document_text`, the OCR step and the rescan decision, and P3 `rwb-case` owns the case and its owner. This story owns one thing and no other: **the rescan notice**. It consumes the rescan outcome of the P5 OCR step, renders MSG-P5-018 from the approved template of the service, sends it to the case owner through the ACE notification path, publishes `rwb.comms.NoticeGenerated.v1` and `rwb.comms.NoticeDispatched.v1` on `rwb.comms.events.v1`, and makes the notice readable through `GET /api/recovery/comms/v1/notices/{noticeId}`. The integration story states the same boundary for the wave: "RWB-P6-E1049-APP is done: MSG-P5-018 is sent through the ACE notification path and the notice is readable through the rwb-comms contract." (RWB-ITG-E1049-ITG section 3).

This story does not re-implement the OCR pipeline, the quality threshold or the review queue. `OCR_MIN_QUALITY` and the rescan decision stay rows and code of P5 `rwb-document`; the review queue (`SCR-31`) and the job monitor (`SCR-44`) stay with P5; the page text, the page quality and the rescan page list stay in `document_text` and `document_intake` in schema `rwb_document` and are never read from a table here (DP01). The service owns only `notice`, `template` and `merge_field` in schema `rwb_comms`, and the notice answer is the only thing a consumer reads.

### 2. Business rationale

Scanned documents arrive as images; a page that the OCR service cannot read above the quality threshold has to go back for a rescan the same day, and the person who has to rescan it is the owner of the case. Today that message is sent by the OCR step inside the document module, in the same process and against a shared schema. In the target the notice is the Communications service's job: P6 owns notices, templates, merge fields and proof of delivery (Architecture v5 slides 17 and 41), and the document service owns the reading of the file. Splitting the two means the notice text, its template version and its dispatch facts have one owner, are versioned as data, and are readable by the integration suite and by the case screens without touching the document schema.

The notice keeps the legacy wording character for character: "Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub." (RWB-E1-049 section 14, MSG-P5-018). It serves the same measured outcome as the legacy story, that every scan becomes searchable text and an unreadable page is sent back the same day, which is the input to REQ-DCM-006 (fields extracted in Thai and English, which needs Thai and English text first), REQ-DCM-009 (documents from every path through the same intake) and REQ-DCM-010 (a file is read only after its malware scan is CLEAN). The FSD P6 measure "notices with proof of delivery, 100 percent" is measured over the notices the service sends (FSD P6 v3 A2.1.1).

The legacy key is split and only the notice part is here (section 19): RWB-P5-E1049-APP keeps the intake item, the text and the OCR step, RWB-P5-E1049-CON publishes the event and the document read this story builds against, RWB-P5-E1049-INF and RWB-P5-E1049-OPS carry the OCR service connectivity and the job runtime, and RWB-ITG-E1049-ITG proves the journey end to end. Legacy AC1 to AC9 describe the OCR step itself and belong to P5; this story writes new criteria that test the notice and its readable record only, and no new business value is added by them.

### 3. Preconditions

- RWB-P5-E1049-CON is published: the envelope of the document rescan event, its element list, and the document read of `GET /api/recovery/document/v1/documents/{documentId}`. The event is the only trigger of this story and its name is not in any event catalogue of the sources: the name and the element list below are proposed and carried as a gap (GAP-1205; ASM-2152).
- The six build dependencies the decoupling patterns add to this key are published, so the story builds on Day 1: RWB-PLT-E1042-CON (parameters client), RWB-PLT-E1043-CON (reference-data client, DP-07), RWB-PLT-TE006-CON (outbox and inbox library, DP-09), RWB-PLT-E1071-CON (workflow kit, DP-10), RWB-PLT-E1044-CON (per-service Flyway, DP-15) and RWB-PLT-N001-CON (gateway-bff route, DP-19). None of them appears in the build list of the plan for this key, so all six are declared here and carried as a gap (GAP-1206; ASM-2153).
- The two contract dependencies the patterns add are published: RWB-P3-E1042-CON (parameters, DP-06) and RWB-P3-E1043-CON (reference data, DP-07). The case read this story makes for the case number and the owner is a contract call of the same kind and has no contract row of its own either; all three are carried in the same gap (GAP-1206; ASM-2153).
- The login is the rwb-comms login (DP-02). The per-service login name is not given by any source read here and belongs to the platform database story.
- The ACE notification path is reachable for the channels of the service and returns an accepted reference and a result code. Its request and result shapes are Not specified in the source documents (GAP-1204; ASM-2156).
- The rescan notice template exists in the `template` table of `rwb_comms` as an Approved and current version for the language of the case. Its template code, version, language and channel are Not specified in the source documents (GAP-1204; ASM-2151).
- LOV-NOTICE, LOV-CHANNEL and LOV-LANG are read through the rwb-case reference-data contract, so no list is written in code (DP-07; the default ruling that reference data belongs to rwb-case is accepted here and the service holds no local copy, ASM-2160).
- The synthetic fixtures of the wave are loaded: the 4-page court notice on case "RW-2026-000123" owned by "TEST-CO-01", the 2-page mailroom scan with no case, and the 1-page scan at quality 0.70. No production data is used and no production connection is opened. The document count per synthetic case and the version depth of a seeded document are Not specified in the source documents (GAP-1051); both are seed parameters of this story, not code.
- The feature flag of the capability is on. The flag name is Not specified in the source documents (GAP-1204; ASM-2158).
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. P5 `rwb-document`: the OCR step of `DocumentIntakeWorkflow` (JOB-12) reads the file, applies `OCR_MIN_QUALITY` and writes the intake item, the page rows and the rescan page list in `rwb_document`. None of this is built or read here.
2. P5 `rwb-document`: for an intake item in RESCAN with a known case, the service publishes the document rescan event on `rwb.document.events.v1` with the intake item, the document, the case, the rescan pages and the quality. The event name is proposed (GAP-1205; ASM-2152); it carries IDs and facts only.
3. rwb-comms: `RescanNoticeListener` consumes the event and checks the event id against `processed_event`. A duplicate is recorded and dropped, so one event makes at most one notice (DP-09).
4. rwb-comms: the listener refuses an event with no case. An item with no case stays with `rwb-document`, which sets review reason RESCAN for the review queue; no notice row and no message is produced here.
5. rwb-comms: `TemplateCatalog` asks its own `template` table for the current Approved version of the rescan notice for the language. No Approved version refuses the notice and writes no row; a withdrawn current version holds the notice with hold reason "TEMPLATE_WITHDRAWN" and raises MSG-P6-003.
6. rwb-comms: `MergeValueResolver` fills the three merge codes of the message: `{page}` from the rescan pages of the event, `{case}` from the case number read through the rwb-case contract, and `{document}` from the document read through the rwb-document contract. The token form of `{document}` is Not specified in the source documents (GAP-1208; ASM-2155).
7. rwb-comms: `RescanNoticeService` writes the `notice` row with the case, the document, the template, the notice type, the language, the hold reason and its state, and writes `rwb.comms.NoticeGenerated.v1` to the outbox in the same transaction.
8. Outbox relay: publishes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1` keyed by caseId, with IDs and the template version only.
9. rwb-comms: `NoticeDispatchWorkflow` starts on task queue `rwb-comms`, renders the message from the approved template body and calls the ACE notification path once.
10. rwb-comms: on an accepted answer the activity writes the dispatch facts on the notice row (sent date, dispatch attempt, delivery status) and writes `rwb.comms.NoticeDispatched.v1` to the outbox in the same transaction.
11. rwb-comms: on an unavailable or failed answer the workflow retries the send once under the retry policy of the workflow kit; the notice row is not duplicated and the attempt count increases. The attempt limit beyond one retry is Not specified in the source documents (GAP-1204; ASM-2157).
12. Caller: `GET /api/recovery/comms/v1/notices/{noticeId}` returns the notice with its message, case, document, template version, hold reason and dispatch facts. A read changes no row.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A page has quality below OCR_MIN_QUALITY on a document of a known case | The rescan event is published by P5; this service writes one notice and sends it to the case owner; the document token reference form is Not specified in the source documents (GAP-1208) | MSG-P5-018 | AC1 |
| X2 | The rescan event carries no case | No notice row and no message; the item stays with the P5 review path under review reason RESCAN | None | AC2 |
| X3 | Page quality is exactly at OCR_MIN_QUALITY | P5 publishes no rescan event and this service writes nothing | None | AC3 |
| X4 | The same rescan event is delivered twice | The inbox records the duplicate and one notice exists | None | AC4 |
| X5 | The template version of the rescan notice is withdrawn and no later version is Approved | The notice is held with hold reason "TEMPLATE_WITHDRAWN"; nothing is sent; the notice is readable with its hold reason | MSG-P6-003 | AC5 |
| X6 | The ACE notification path returns unavailable or an error | The notice is queued and the workflow retries once; the notice row is not duplicated; the attempt count increases | MSG-GEN-006 | AC6 |
| X7 | A caller without the read right of the notice area calls the notice read | Refused at the edge with 403; no notice returned | MSG-P4-002 | AC8 |
| X8 | A consumed contract call does not answer inside 2 s | The notice is held rather than sent with a missing merge value; the caller is told the system is unavailable and the event is retried under the inbox | MSG-GEN-006 | AC1, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Consumes the P5 event and the three reads; builds against RWB-P5-E1049-CON and the rwb-case and reference-data fakes; the OCR step, the threshold and the review queue are not touched in code |
| Negotiable | The template version, the channel, the notice type and the state values are data rows; the merge order, the hold path, the retry and the dedupe are fixed |
| Valuable | The owner of the case is told which page to scan again, the notice carries the approved wording, and the fact that the notice was sent is readable by another service |
| Estimable | One listener, one renderer, one workflow, one read operation, three consumed contracts, one outbox and one inbox |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion is a component test with a synthetic rescan event, a synthetic template and named contract fakes; the end-to-end proof is the integration story's |

Size: none is set in this story; the squad sizes it at refinement.

### 7. Acceptance criteria

```gherkin
Feature: Rescan notice of the Workbench document hub

  Background:
    Given OCR_MIN_QUALITY is 0.70, OCR_WORKERS is 4, OCR_TIMEOUT_SECONDS is 120 and OCR_MAX_ATTEMPTS is 3
    Given the rwb-comms template catalog holds one Approved and current template version of the rescan notice in "TH"
    Given the rwb-case reference-data mock returns LOV-CHANNEL with SMS and LINE, LOV-NOTICE with DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE and LOV-LANG with TH and EN
    Given the ACE notification path stub returns an accepted reference and result code "ACCEPTED"

  Scenario: AC1 An unreadable page on a known case sends one rescan notice to the case owner (new, D-RCV-60)
    Given the 4-page court notice is stored on case "RW-2026-000123" owned by "TEST-CO-01"
    Given page 3 has quality 0.41 and the other pages are above 0.70
    Given the rwb-document contract mock returns the rescan event with intakeItemId "INT-0001", documentId "DOC-0001", caseId "CASE-0001", rescanPages "3" and quality 0.41
    Given the rwb-case contract mock returns case "CASE-0001" with case number "RW-2026-000123" and owner "TEST-CO-01"
    When RescanNoticeListener consumes the rescan event
    Then exactly one notice row exists for case "CASE-0001" and document "DOC-0001"
    Then the notice message reads "Page 3 of the court notice on case RW-2026-000123 could not be read. Scan it again and send it to the document hub."
    Then the notice is addressed to "TEST-CO-01" and one message is sent through the ACE notification path
    Then one rwb.comms.NoticeGenerated.v1 is in the outbox with the notice ID, case "CASE-0001", document "DOC-0001" and the template version
    Then GET /api/recovery/comms/v1/notices/{noticeId} returns the notice with its message, case number "RW-2026-000123", document "DOC-0001" and dispatch attempt 1

  Scenario: AC2 An unreadable page with no case sends no notice (new, D-RCV-60)
    Given a mailroom scan of 2 pages with no case and page 1 at quality 0.30
    Given the rwb-document contract mock returns the rescan event with no caseId, rescanPages "1" and quality 0.30
    When RescanNoticeListener consumes the rescan event
    Then no notice row exists and no message is sent through the ACE notification path
    Then no rwb.comms.NoticeGenerated.v1 is written to the outbox
    Then review reason "RESCAN" stays with rwb-document and is not written by rwb-comms

  Scenario: AC3 A page exactly at the quality threshold sends no notice (new, D-RCV-60)
    Given a scan of 1 page at quality 0.70
    Given the rwb-document contract mock returns the OCR outcome of the intake item with quality 0.70, no rescan page and no rescan event
    When RescanNoticeListener runs over its inbox
    Then no notice row exists for the intake item and no message is sent
    Then no rwb.comms.NoticeGenerated.v1 is written to the outbox

  Scenario: AC4 The same rescan event delivered twice produces one notice (new, D-RCV-60)
    Given one rescan event with event id "EVT-0001" for page 3 of the court notice on case "RW-2026-000123"
    Given the rwb-document contract mock returns that event with intakeItemId "INT-0001", documentId "DOC-0001", caseId "CASE-0001" and rescanPages "3"
    When the same event id is delivered twice
    Then the inbox records the second delivery as a duplicate
    Then exactly one notice row exists for case "CASE-0001" and document "DOC-0001"
    Then one message is sent through the ACE notification path and one rwb.comms.NoticeGenerated.v1 is in the outbox

  Scenario: AC5 A withdrawn template holds the rescan notice (new, D-RCV-60)
    Given the current template version of the rescan notice is withdrawn and no later version is Approved
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    Given the rwb-case contract mock returns case "CASE-0001" with case number "RW-2026-000123" and owner "TEST-CO-01"
    When RescanNoticeListener consumes the rescan event
    Then a notice row exists in state "Held" with hold reason "TEMPLATE_WITHDRAWN"
    Then nothing is sent through the ACE notification path and no rwb.comms.NoticeDispatched.v1 is written to the outbox
    Then GET /api/recovery/comms/v1/notices/{noticeId} returns the hold reason "TEMPLATE_WITHDRAWN" and no sent date

  Scenario: AC6 An unavailable notification path queues the notice and it is retried once (new, D-RCV-60)
    Given the ACE notification path stub returns "unavailable" for every call
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    Given the rwb-case contract mock returns case "CASE-0001" with case number "RW-2026-000123" and owner "TEST-CO-01"
    When RescanNoticeListener consumes the rescan event and NoticeDispatchWorkflow runs
    Then the notice row exists with dispatch attempts 1 and is queued for a retry
    Then NoticeDispatchWorkflow retries the send once and the notice row holds dispatch attempts 2
    Then when the path accepts the message the notice is readable with its sent date and one rwb.comms.NoticeDispatched.v1 is in the outbox
    Then no second notice row is created for the event

  Scenario: AC7 The notice carries no personal data outside the message (new, D-RCV-60)
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    Given the rwb-case contract mock returns case "CASE-0001" with case number "RW-2026-000123" and owner "TEST-CO-01"
    When RescanNoticeListener consumes the rescan event and the notice is dispatched
    Then the notice row, the two outbox rows and the workflow input carry the notice ID, the case ID, the document ID, the intake item ID, the template ID and version, the language and the rescan page only
    Then no name, address, phone number, account number, page text or document body appears in a notice event, a workflow input or a log line
    Then the message text is sent only in the request to the ACE notification path

  Scenario: AC8 A caller without the read right of the notice area is refused (new, D-RCV-60)
    Given a caller without the read right of the notice area
    When the caller calls GET /api/recovery/comms/v1/notices/{noticeId} for the notice of case "RW-2026-000123"
    Then the request is refused at the edge with status 403 and MSG-P4-002
    Then no notice is returned

  Scenario: AC9 A notice uses only the current Approved template version of its language (new, D-RCV-60)
    Given a superseded version of the rescan notice in "TH" is held next to the current Approved version
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    Given the rwb-case contract mock returns case "CASE-0001" with case number "RW-2026-000123" and owner "TEST-CO-01"
    When RescanNoticeListener consumes the rescan event
    Then the notice row holds the template ID and version of the current Approved version in "TH" only
    Then the message is rendered from no other template version

  Scenario: AC10 A notice whose merge value cannot be read from an owner's contract is held (new, D-RCV-60)
    Given the rwb-case contract call for the case number does not answer inside 2 s
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    When RescanNoticeListener consumes the rescan event
    Then the notice is held and its message is not completed with a missing value
    Then nothing is sent through the ACE notification path and the caller is told the system is unavailable with MSG-GEN-006

  Scenario: AC11 The notice is dispatched only through the ACE notification path (new, D-RCV-60)
    Given the ACE notification path stub returns an accepted reference and a result code Not specified in the source documents (GAP-1204)
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    When NoticeDispatchWorkflow runs for the notice
    Then one message is sent through the ACE notification path
    Then the service calls no other external system

  Scenario: AC12 The notice writes only the tables of its own schema (new, D-RCV-60)
    Given the rwb-document contract mock returns the rescan event for page 3 of the court notice on case "RW-2026-000123"
    When RescanNoticeListener consumes the rescan event and the notice is dispatched
    Then the rows written are in the rwb_comms schema only
    Then no row is written to another service's tables

  Scenario: AC13 The template reference, channel and notice type are data rows, not code (new, D-RCV-60)
    Given the rescan notice template row holds its channel and notice type as data
    When RescanNoticeService writes the notice row
    Then the template reference, channel and notice type are read from data rows only
    Then no template reference, channel or notice type value is set in code

  Scenario: AC14 A request to the notice read without a valid session is refused with 401 (new, D-RCV-60)
    Given a caller without a valid session
    When the caller calls GET /api/recovery/comms/v1/notices/{noticeId} for the notice of case "RW-2026-000123"
    Then the request is refused with status 401
    Then no notice is returned

  Scenario: AC15 A notice ID that matches no notice is answered with 404 (new, D-RCV-60)
    Given a caller with the read right of the notice area
    When the caller calls GET /api/recovery/comms/v1/notices/{noticeId} with a noticeId that matches no notice
    Then the request is answered with status 404
    Then no notice is returned

  Scenario: AC16 A status change the notice model does not allow is refused (new, D-RCV-60)
    Given a notice row already sent with a sent date
    When NoticeDispatchWorkflow runs again for the same notice
    Then the status change back to state "Held" is refused and the row keeps its sent date
    Then no second rwb.comms.NoticeDispatched.v1 is written to the outbox
```

The sixteen criteria above are new and tagged (new, D-RCV-60); the legacy criteria AC1 to AC9 of RWB-E1-049 describe the OCR step, the threshold and the worker pool and belong to RWB-P5-E1049-APP, and this story owns none of them. Every value in the criteria is copied from the legacy story or the module extracts: the case "RW-2026-000123" and the owner "TEST-CO-01" from RWB-E1-049 AC3, the page 3 at quality 0.41 from AC3, the 2-page mailroom scan with page 1 at 0.30 and no case from AC4, the 1 page at 0.70 from AC5, the four parameter values from RWB-E1-049 section 3, the hold reason "TEMPLATE_WITHDRAWN" and the message MSG-P6-003 from FSD P6 v3 A2.1.4.3, and the message text from RWB-E1-049 section 14. The document rescan event and the state values of a notification-path dispatch are the only elements the sources do not name, and both are carried as gaps (GAP-1205 and GAP-1204) and assumptions (ASM-2152 and ASM-2163).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A page below OCR_MIN_QUALITY is sent for rescan and the case owner of a known case is told by a notice; the threshold itself is inclusive and is P5's | RWB-E1-049 BR4; FSD P6 v3 A2.1.4.3; document hub parameter OCR_MIN_QUALITY |
| BR2 | An intake item with no case produces no notice; the item goes to the review queue of the document service with review reason RESCAN | RWB-E1-049 AC4; RWB-P5-E1049-APP |
| BR3 | One rescan event makes at most one notice; a duplicate event is dropped through the inbox | RWB-E1-049 BR6 (R-UNI-40); DP-09 |
| BR4 | A notice is sent only from the current Approved template version of its language | FSD P6 v3 A2.1.3.1 (R-LIT-04); RWB-E1-049 section 13 |
| BR5 | A withdrawn template version holds the notice with hold reason "TEMPLATE_WITHDRAWN" and nothing is sent | FSD P6 v3 A2.1.4.3 AC-EXC-P6-001-02; VR-P6-001-1 |
| BR6 | A notice whose message cannot be completed from an owner's contract is held, never sent with a missing value | RWB-E1-049 section 3; DP-11; ADR-020 |
| BR7 | A notification path that does not answer is retried once and the notice row is not duplicated; the attempt limit follows the platform retry rules | RWB-E1-049 BR5 (R-UNI-33); FSD P6 v3 A2.3.4.3 AC-EXC-P6-003-03 |
| BR8 | The notice is dispatched only through the ACE notification path; the service calls no external system directly | Architecture v5 slide 17 (OUT: REST ACE Common, notification path, SMS and LINE); TSD P6 v2 T5.1 |
| BR9 | The notice row and its event carry IDs, the template version and the language only; the message body is sent only in the request to the notification path | NFR-040; Architecture v5 slide 42 notes; RWB-E1-049 section 17 |
| BR10 | `notice`, `template` and `merge_field` are written only in `rwb_comms`; `document_intake`, `document_text` and the review queue are P5's and the case and its owner are P3's | RWB-E1-049 section 17; Ownership Map (tables `notice`, `template`, `merge_field` owner P6; `document`, `document_intake`, `document_text` owner P5; `recovery_case` owner P3); DP-01 |
| BR11 | The template reference, the channel and the notice type are data rows of the service, not code and not parameters | FSD P6 v3 BR-P6-001; Principle 1; DP-06 |

### 9. State transitions

None for the case status: this story changes no case status and no intake item state. It sets the `state` standard column of the notice row it writes. The state values of a notification-path dispatch are Not specified in the source documents (GAP-1204; ASM-2163); "Held" and the hold reason "TEMPLATE_WITHDRAWN" are named by the module extract and are used as written.

| From | Event | Condition | To |
|---|---|---|---|
| None | The rescan event is consumed | The current template version is Approved and the case, the page and the document resolve | Generated |
| Generated | `NoticeDispatchWorkflow` sends the message | The ACE notification path accepts the message | Dispatched, with the sent date and the dispatch attempt |
| Generated | `NoticeDispatchWorkflow` sends the message | The path is unavailable or fails | Generated, with the dispatch attempt increased; one retry follows |
| Generated | One retry has failed | The path still does not answer | Generated, with the dispatch attempt of the retry; the notice is readable with no sent date |
| None | The rescan event is consumed | The current template version is withdrawn and no later version is Approved | Held, hold reason "TEMPLATE_WITHDRAWN" |
| Any | A read through `GET /notices/{noticeId}` | Never | The same state; a read changes no row |
| None | The rescan event is consumed | The event carries no case | No row at all |

The intake item states PENDING, DONE, RESCAN and FAILED stay with `rwb-document` and are not written or read here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-comms service identity (the rwb-comms login, DP-02) | Consumes the rescan event, writes `rwb_comms`, sends the message through the ACE notification path and serves the notice read |
| RW-CASEOWN, case owner | Documents CRU and Litigation R: reads the notice of a case in scope and receives the rescan notice of the case they own |
| RW-TEAMMGR, team manager | Documents R and Litigation R: reads the notice of a case in scope |
| RW-LITOFF, litigation officer | Documents CRU and Litigation CRUA: reads the notice of a case in scope |
| RW-PLATADM, platform administrator | Documents R only: reads the notice of a case in scope for support; the matrix grants no Litigation right |
| SY-OCR, OCR and extraction pipeline | Documents CRU: writes the OCR output and the text rows in `rwb_document`; it calls nothing in this service, because the notice is raised from the event |

The area and the right of the notice read are declared on the operation and enforced at gateway-bff (DP-19); this story makes no rwb-access call, because DP-08 is not among the patterns of the key, and the service answers 403 with MSG-P4-002 when a request reaches it without the declared right (GAP-1204; ASM-2162). No role in this story changes a case owner, a queue or a right.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (P6 rwb_comms) | id | Write |
| DF-LEG-016 | notice (P6 rwb_comms) | case_id | Write |
| DF-LEG-017 | notice (P6 rwb_comms) | document_id | Write |
| DF-LEG-018 | notice (P6 rwb_comms) | notice_type | Write; the value for an operational rescan notice is Not specified in the source documents (GAP-1207; ASM-2154) |
| DF-LEG-019 | notice (P6 rwb_comms) | sent_date | Write on dispatch, from the answer of the notification path |
| DF-LEG-020 | notice (P6 rwb_comms) | barcode | Not written: a notification-path message carries none |
| DF-LEG-021 | notice (P6 rwb_comms) | callback_date | Not written here |
| DF-LEG-022 | notice (P6 rwb_comms) | delivery_status | Write on dispatch, from the result code of the path |
| DF-LEG-023 | notice (P6 rwb_comms) | sent_type | Read, from the case facts; the value list LOV-SENT-TYPE is read through the reference-data contract |
| DF-LEG-030 | notice (P6 rwb_comms) | party_id | Not written: the notice is addressed to the case owner and no party row exists in the Workbench |
| DF-LEG-031 | notice (P6 rwb_comms) | template_id | Write |
| DF-LEG-032 | notice (P6 rwb_comms) | hold_reason | Write; "TEMPLATE_WITHDRAWN" is the only value the sources name |
| DF-LEG-033 | notice (P6 rwb_comms) | dispatch_file_id | Not written: no WIN file is produced for this notice |
| DF-LEG-034 | notice (P6 rwb_comms) | dispatch_attempts | Write, one per send attempt |
| Standard column | notice (P6 rwb_comms) | state | Write |
| DF-REF-045, DF-REF-046, DF-REF-047, DF-REF-048, DF-REF-050, DF-REF-051, DF-REF-065, DF-REF-066, DF-REF-067 | template (P6 rwb_comms) | id, template_code, template_version, language, body_ref, approved_by_legal, valid_from, channel, notice_type | Read |
| DF-REF-252, DF-REF-253, DF-REF-254, DF-REF-255, DF-REF-256, DF-REF-257, DF-REF-258, DF-REF-259, DF-REF-260 | merge_field (P6 rwb_comms) | id, merge_code, source_entity, source_field, field_id, is_required, personal_data, catalog_version, valid_from | Read |
| DF-DOC-001, DF-DOC-002, DF-DOC-005 | document (P5 rwb-document) | id, case_id, source | Read through the P5 contract |
| DF-DOC-045 to DF-DOC-084 | document_intake (P5 rwb-document) | ocr_status, rescan_pages, ocr_quality, languages, review_reason, case_id, document_id | Read through the P5 event and the P5 contract; never from the table |
| DF-DOC-085 to DF-DOC-090 | document_text (P5 rwb-document) | page_no, quality, text_content | Not read here: the page number and the quality arrive on the event and the page text is never copied into a notice |
| DF-CAS-009 | recovery_case (P3 rwb-case) | owner_user_id | Read through the rwb-case contract |

The schema is `rwb_comms` and its migration runs in the per-service Flyway sequence (DP-15). No foreign key crosses into another schema and no row of `rwb_document`, `rwb_case` or `rwb_source_data` is read or written directly (DP-01). No interaction ledger row is written by this notice: the ledger is rwb-source-data's under the default ruling of DP-18, and the notice keeps its own dispatch facts (ASM-2161). The property list of the notice answer of `GET /notices/{noticeId}` is Not specified in the source documents beyond the field names of the table (GAP-1204; ASM-2163), and the element list of the rescan event is Not specified in the source documents (GAP-1205; ASM-2152).

### 12. Contract

Contract version fixed at v1: operations under /api/recovery/comms/v1 and events named .v1 in 12.4. HTTP 401 and 404 message IDs: Not specified in the source documents (DOR-RWB-P6-E1049-APP-8). HTTP 403: MSG-P4-002.

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P6-002 | GET | `/notices/{noticeId}` | Read one rescan notice with its message, case, document, template version, hold reason and dispatch facts; answer 200 with the Notice | Litigation, right R, scope applied | Not applicable |

Errors: 401 (Not specified in the source documents (CG-ALL-6374)), 403 (MSG-P4-002), 404 (Not specified in the source documents (CG-ALL-6374)), 503. The read is the one the integration suite and the case screens use to confirm that MSG-P5-018 was sent (`RWB-ITG-E1049-ITG` section 12.2). `POST /cases/{caseId}/notices` (API-P6-001) is provided by the same service and owned by RWB-P6-E1052-APP; the rescan notice is generated by this story inside the service through the same generation path and its own idempotency key, so no caller drives it. The property list of the Notice resource is Not specified in the source documents beyond the field names of the table (GAP-1204; ASM-2163); the request and result shapes of the ACE notification path are Not specified in the source documents (GAP-1204; ASM-2156).

#### 12.2 REST operations consumed

Every row is one hop on the owner's base with a 2 s timeout, a breaker per downstream and a single GET retry with jitter (DP-11, ADR-020).

| Method and path | Owner | Use in this story |
|---|---|---|
| GET `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The document reference the message names; contract RWB-P5-E1049-CON |
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number and the owner the notice is addressed to; the contract row is not declared on this key and is carried as a gap (GAP-1206; ASM-2153) |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-NOTICE, LOV-CHANNEL, LOV-LANG and LOV-SENT-TYPE, so no list is written in code; contract RWB-P3-E1043-CON (DP-07) |

The request to the ACE notification path is not a service contract of the Ownership Map: it is the ACE common notification path, called with the recipient reference, the channel, the template reference, the language, the case reference and the merged message. Its shape is Not specified in the source documents (GAP-1204; ASM-2156).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Schema element (IDs and facts only) |
|---|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` (EV-13) | `rwb.comms.events.v1` | P6 rwb-comms | caseId | noticeId, caseId, documentId, intakeItemId, templateId, templateVersion, language, noticeType, generatedAt; written to the outbox in the same transaction as the notice row |
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | P6 rwb-comms | caseId | noticeId, caseId, channel, externalReference, resultCode, dispatchedAt, dispatchAttempt; written to the outbox in the same transaction as the dispatch facts on the notice row |

`generatedAt` and `dispatchedAt` are the outbox write times, and the full element list beyond the names above is Not specified in the source documents (GAP-1204; ASM-2163). No event carries a name, an address, a phone number, an account number, a page text or the message body (BR9).

#### 12.4 Events consumed

| Event | Topic | Producer | Declared shape | Handler in this story |
|---|---|---|---|---|
| `rwb.document.OcrRescanRequested.v1` (proposed name) | `rwb.document.events.v1` | P5 rwb-document | intakeItemId, documentId, caseId (absent when no case), rescanPages, quality, languages, occurredAt | `RescanNoticeListener`, deduped through the inbox |

The event is the only trigger of the story and neither the Architecture v5 event catalogue (slides 42 and 43) nor the legacy story names it: the catalogue holds `DocumentStored` and `DocumentFieldsExtracted` for `rwb-document` and the legacy sends the notification in-process. The name, the payload and the topic above are therefore proposed, on the topic the Ownership Map gives the owner, and carried as a gap (GAP-1205; ASM-2152). The inbox table is in place so a redelivery is deduped (DP-09). Proposed producer contract: P5 rwb-document publishes the event with the elements of the table above; the transaction and timing of the publish are Not specified in the source documents (GAP-1205).

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| `NoticeDispatchWorkflow` | P6 rwb-comms | rwb-comms | The dispatch of one notice: it renders the message from the approved template body, calls the ACE notification path and records the result |
| Activity `renderNoticeMessage` | P6 rwb-comms | rwb-comms | Merges the page, the document and the case into the approved body and returns the message |
| Activity `sendNotice` | P6 rwb-comms | rwb-comms | One call to the ACE notification path with a 2 s budget; returns the accepted reference and the result code |
| Activity `recordDispatch` | P6 rwb-comms | rwb-comms | Writes the dispatch facts on the notice row and the `NoticeDispatched` outbox row in one transaction |

`NoticeDispatchWorkflow` is the kit Notify template on queue rwb-comms of the service (Architecture v5 slide 17: "TMP NoticeDispatchWorkflow (kit template)"; Temporal and Drools Design Text Extract v1 slide 12: the workflow kit holds "Notify" and "Scheduled job"). The workflow input carries the notice ID, the case ID, the document ID, the intake item ID, the template ID and version, the language and the rescan pages only; it carries no personal value. The retry policy is one retry and the attempt limit beyond it is Not specified in the source documents (GAP-1204; ASM-2157).

#### 12.6 Schedules

None. The story registers no Schedule and no cron entry: its trigger is the event of section 12.4, and the retry of a send is the workflow's own retry, not a job. JOB-12 Document intake is the P5 workflow step (Architecture v5 slide 44: "JOB-12 Document intake, every 15 min, rwb-document, event + KEDA workers"), and JOB-11 Outbox sender is the platform relay. No shared job table and no Quartz row is read (DP-10).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The rescan notice: case, document, template, notice type, hold reason, state and dispatch facts |
| template | P6 (rwb_comms) | The rescan notice template and its current Approved version; written by RWB-P6-E1046-APP, read here |
| merge_field | P6 (rwb_comms) | The merge codes `{page}`, `{document}` and `{case}` and their required flag; written by RWB-P6-E1046-APP, read here |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox of the two published events, the inbox of the rescan event and the idempotency answer (DP-09) |

Not owned and never read directly: `document`, `document_intake`, `document_text` and `retention_rule` (P5 rwb-document), `recovery_case`, `case_party` and `task` (P3 rwb-case), `template` bodies (read by reference only), and `decision_log_entry` (P7 rwb-decision).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers |
|---|---|---|
| rwb-document event and read WireMock | RWB-P5-E1049-CON | One rescan event for intake "INT-0001", document "DOC-0001", case "CASE-0001", rescanPages "3" and quality 0.41; the same event id twice; an event with no caseId and rescanPages "1"; an event with quality 0.70 and no rescan page; the document read for "DOC-0001"; a delayed answer beyond 2 s |
| rwb-case WireMock | The published rwb-case case read | Case "CASE-0001" with case number "RW-2026-000123" and owner "TEST-CO-01"; a case with no owner; a delayed answer beyond 2 s |
| rwb-case reference-data WireMock | RWB-P3-E1043-CON | LOV-NOTICE with DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE; LOV-CHANNEL with SMS and LINE; LOV-LANG with TH and EN; LOV-SENT-TYPE with BEFORE_NPL and NPL |
| ACE notification path stub | The ACE common notification path | Accepted with reference "MSG-0001" and result code "ACCEPTED"; unavailable for every call in AC6; a failure result code; a delayed answer beyond 2 s |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | API-P6-002 provided; the three rows of 12.2 consumed, one hop each with a 2 s budget |
| Kafka | 2 published, 1 consumed | `NoticeGenerated` and `NoticeDispatched` on `rwb.comms.events.v1`; the rescan event consumed from `rwb.document.events.v1` |
| Temporal | 1 workflow, 3 activities | `NoticeDispatchWorkflow` on rwb-comms with `renderNoticeMessage`, `sendNotice` and `recordDispatch` |
| File | None | The service writes no file: the notice is a message, not a letter, and no WIN file is produced by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `rescan-notice`, Java package `th.co.scb.ace.workbench.recovery.comms.rescan`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables; the intake and text tables of the document service stay with that service | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; no parameter of the OCR step is read here, `OCR_MIN_QUALITY` stays P5's | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; the topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; JOB-12 is the P5 workflow step and JOB-11 is the platform relay | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The pattern table adds six build dependencies and two contract dependencies that the plan's build and contract lists do not carry, and the rwb-case case read adds a third contract dependency of the same kind; the metadata keeps the lists of the plan, the story declares them in section 3 and this table, and the difference is carried as a gap (GAP-1206; ASM-2153). No pattern is claimed for DP-02 (the login is the platform's), DP-03 (no decision record is written by this notice), DP-04, DP-05 (this service reads no ACE view), DP-08, DP-12, DP-14, DP-16, DP-17, DP-18 or DP-20.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RescanNoticeListener | Listener | Consumes the rescan event, dedupes it through the inbox, refuses an event with no case and starts the notice |
| RescanNoticeService | Service | Steps 4 to 7: the template check, the hold path, the merge values, the notice row and the generated event in one transaction |
| TemplateCatalog | Service | The current Approved template version of the rescan notice for a language, from `template` |
| MergeValueResolver | Service | Fills `{page}` from the event, `{case}` from the case read and `{document}` from the document read, and enforces the required flag of each merge code |
| NoticeController | Controller | `GET /notices/{noticeId}` with validation and the problem mapping of the error envelope |
| NoticeRepository | Repository | Reads and writes `notice` only; finds by case and document for the duplicate check |
| DocumentClient | Client | The document read of rwb-document, one hop with the 2 s budget |
| CaseClient | Client | The case number and owner read, and the reference-data reads of rwb-case |
| NotificationPathClient | Client | The ACE notification path call, with the accepted reference and the result code |
| NoticeDispatchWorkflow and its three activities | Workflow | Render, send once, retry once and record the dispatch facts |
| NoticeEventWriter | Service | Writes `NoticeGenerated` and `NoticeDispatched` to the outbox in the same transaction as the row they describe |

**Database and migrations**

- Writes `notice` in schema `rwb_comms`, reads `template` and `merge_field` there, and writes the outbox, inbox and idempotency rows of the platform library.
- Migration `V1049_1__rescan_notice.sql` in the rwb-comms Flyway sequence: `notice` with the standard columns, the field list of section 11 and the state check; a unique index on `(case_id, document_id, template_id, created_at::date)` for the one-notice-per-event rule; and the outbox and inbox tables of the library. No column of the document service's intake or text tables is copied (DP-01).
- The event id is the idempotency key of the notice: the inbox row and the notice row commit together, so a redelivery writes no second notice (DP-09).

**Configuration and reference data**

- The rescan notice template is a row of `template` with its code, version, language, channel and body: the values are Not specified in the source documents (GAP-1204; ASM-2151) and are loaded by the template catalog story RWB-P6-E1046-APP.
- LOV-NOTICE, LOV-CHANNEL, LOV-LANG and LOV-SENT-TYPE are reference rows read through the rwb-case contract; no list is written in code (DP-07).
- `OCR_MIN_QUALITY`, `OCR_WORKERS`, `OCR_TIMEOUT_SECONDS` and `OCR_MAX_ATTEMPTS` are **not** read here: they stay rows of the document hub parameter table of P5 and the rescan decision is P5's. This story reads no parameter at all, and the two values a business person may change in it (the template reference and the channel) are rows of its own `template` table (BR11; the default ruling that parameters belong to rwb-case is accepted and no parameter is duplicated in `rwb_comms`, ASM-2159).
- The feature flag of the capability is on by default in wave 1 and off means the listener drops the event without writing a notice; the flag is read through the platform feature-flag library (default ruling) and its name is Not specified in the source documents (GAP-1204; ASM-2158).
- The login is the rwb-comms login (DP-02); its name is allocated by the platform database story and is not fixed here.

**Build steps**

1. Migration, `NoticeEntity` and the unique index; a test for the one-notice rule of AC4.
2. `RescanNoticeListener` and the inbox dedupe, against the rwb-document fake: the same event id twice, an event with no case (AC2) and an event with no rescan page (AC3).
3. `TemplateCatalog` over `template`, with the no-Approved-version refusal and the withdrawn version hold of AC5; no template value in code.
4. `MergeValueResolver` with the three merge codes of the synthetic template and the required flag; the byte-identical text of AC1.
5. `RescanNoticeService` with the notice row and the `NoticeGenerated` outbox row in one transaction; the case, document and template references asserted.
6. `NoticeDispatchWorkflow`, `sendNotice` and `recordDispatch` against the notification-path stub: the accepted answer of AC1, the unavailable path and the single retry of AC6, and the 2 s timeout of X8.
7. `NoticeController` with `GET /notices/{noticeId}` and the 404, 403 and 503 answers; the read-back assertions of AC1 and AC5.
8. The guardrail tests of AC7: the notice row, the two events and the workflow input carry IDs only and no log line carries a message or a page text.
9. The contract-fake run of the four fakes, so the story builds before the P5 event, the P3 read and the notification path are live in SIT.

**Feature flag.** The flag of the capability, read through the platform library; off means no notice is written for a rescan event (the name is Not specified in the source documents (GAP-1204; ASM-2158)).

**Done when.** The tests of section 16 pass, one rescan event writes one notice and one `NoticeGenerated`, the notice is readable through `GET /api/recovery/comms/v1/notices/{noticeId}` with the exact MSG-P5-018 text, a withdrawn template holds the notice, an unavailable path queues it and one retry delivers it, and no personal value appears in an event, a workflow input or a log line.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-018 | A page is below the quality threshold on a document of a known case | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. |
| MSG-P6-003 | The template version of the rescan notice is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P4-002 | Role without the right of the notice area | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | The ACE notification path does not answer | {system} is not available. Your request is queued and will be retried. |

The message IDs and wording are copied from RWB-E1-049 section 14 (MSG-P5-018) and from the module extract and the platform catalogue (MSG-P6-003 from FSD P6 v3 A2.1.3.1, MSG-P4-002 and MSG-GEN-006 from the platform catalogue). The legacy message keeps its ID and its text character for character; the `{document}` token is filled from the rwb-document read and its reference form is Not specified in the source documents (GAP-1208; ASM-2155). MSG-P4-002 is raised at the gateway-bff edge and not by this service. Thai text for each message follows decision DL10, which is still open (assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863).

### 15. Screens and states

No screen is built in this story. The case owner receives the notice through the ACE notification path (Architecture v5 slide 17: OUT, REST ACE Common, notification path, SMS and LINE) and reads it on the case through the gateway-bff route (DP-19):

| Screen | What it shows for this story | State read |
|---|---|---|
| SCR-01 My work, through the case timeline | The rescan notice of the case with its message, its sent date and its hold reason | Generated, Dispatched, Held, Empty, Loading; Error and No access: Not specified in the source documents (CG-ALL-6380) |
| The case documents screen, through the gateway-bff route | Nothing of this story: the document and its text pages are P5's | None |
| SCR-31 The review queue | Nothing of this story: the queue item is the document service's | Loading; Empty, Error and No access: Not specified in the source documents (CG-ALL-6381) |
| SCR-44 The job monitor | Nothing of this story: the job monitor is the document service's | Empty, Loading, Error and No access: Not specified in the source documents (CG-ALL-6382) |

The review queue SCR-31 and the job monitor SCR-44 that the legacy story names are the document service's and belong to RWB-P5-E1049-APP; the notice this story writes is not a queue item. The composite route, its field list and its timeout budget belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-049-10 | Access, AC8 | Component | A user with RW-CAPACITY and no read right calls `GET /api/recovery/comms/v1/notices/{noticeId}` for the notice of case "RW-2026-000123"; refused with status 403 and MSG-P4-002 and no notice returned |
| TC-E1-049-01 | AC1, BR1, BR5 | Component | 4-page court notice on case "RW-2026-000123" owned by "TEST-CO-01", page 3 at quality 0.41, other pages above 0.70; one notice with the MSG-P5-018 text |
| TC-E1-049-02 | AC4, BR3 | Component | A burst of 125 rescan events in one window; one notice per event and none doubled |
| TC-E1-049-03 | AC1, BR1 | Component | Synthetic 4-page upload with page 3 at quality 0.41 |
| TC-E1-049-04 | AC2, BR2 | Component | 2-page mailroom scan with no case, page 1 at quality 0.30; no notice and no message |
| TC-E1-049-05 | AC3, BR1 | Component | 1 page at quality exactly 0.70; no rescan page, no notice |
| TC-E1-049-06 | AC6, BR7 | Component | Notification path stub returning "unavailable" for every call; the notice queued and one retry |
| TC-E1-049-07 | AC2, BR2 | Component | Password-protected synthetic PDF, intake item FAILED with review reason UNREADABLE_FILE and no rescan page; no notice |
| TC-E1-049-08 | AC4, BR3 | Component | 10 intake items already DONE with 25 page rows; the run again raises no notice |
| TC-E1-049-09 | AC4, AC7, BR9 | Component | One intake item, four workers, one event; one notice whose row and events carry IDs only |
| TC-E1-049-11 | AC5 | Component | Template version of the rescan notice withdrawn and no later version Approved; rescan event for page 3 of the court notice on case "RW-2026-000123"; case "CASE-0001" with owner "TEST-CO-01"; notice row in state Held with hold reason "TEMPLATE_WITHDRAWN", nothing sent |
| TC-E1-049-12 | Section 12 contract | Contract | Every operation, event and activity of section 12 checked against its declared shape |
| TC-E1-049-13 | Section 12.7 tables | Component | Boundary values on each table of section 12.7 (notice, template, merge_field, outbox_event, processed_event, idempotency_key) |
| TC-E1-049-14 | AC9, BR4 | Component | Current Approved version of the rescan notice in "TH" and a superseded version; the notice uses the current version only |
| TC-E1-049-15 | AC10, BR6 | Component | Rescan event for page 3 on case "RW-2026-000123"; rwb-case contract call not answering inside 2 s; notice held, no missing merge value, nothing sent |
| TC-E1-049-16 | AC11, BR8 | Component | ACE notification path stub returning an accepted reference and a result code Not specified in the source documents (GAP-1204); one message through the notification path and no other external call |
| TC-E1-049-17 | AC12, BR10 | Component | Rescan event for page 3 on case "RW-2026-000123"; every write checked against the rwb_comms schema only |
| TC-E1-049-18 | AC13, BR11 | Component | Template row for the rescan notice with channel and notice type as data; no template value set in code |
| TC-E1-049-19 | AC14 | Component | Caller without a valid session calls `GET /api/recovery/comms/v1/notices/{noticeId}` for the notice of case "RW-2026-000123"; refused with status 401 and no notice returned |
| TC-E1-049-20 | AC15 | Component | Caller with the read right of the notice area calls `GET /api/recovery/comms/v1/notices/{noticeId}` with a noticeId matching no notice; answered with status 404 and no notice returned |
| TC-E1-049-21 | AC16 | Component | Notice row already sent with a sent date; NoticeDispatchWorkflow runs again; change back to state "Held" refused, sent date kept, no second rwb.comms.NoticeDispatched.v1 in the outbox |

The first ten cases are the legacy cases of this key, kept under their legacy IDs in the order the plan lists them for this story. The cases TC-E1-049-11 to 13 cover AC5, the section 12 contract and the section 12.7 tables, and TC-E1-049-14 to 18 cover AC9 to AC13, the rules BR4, BR6, BR8, BR10 and BR11 that had no criterion. The legacy level System maps to Component here, because the OCR step and its throughput are now the document service's and the end-to-end proof is RWB-ITG-E1049-ITG; legacy Access stays a Component case and its subject is the notice read rather than the document read, which is where the legacy refusal now lands. The covers column names the criterion of section 7 that each case proves. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the template reference, the channel, the notice type, the language, the state values and the hold reasons are data rows of `rwb_comms` or reference rows read through the rwb-case contract.
- No personal data in events, workflow inputs or logs: the notice row and the two events carry IDs, the template version, the language and the rescan page only; the message body exists only in the request to the ACE notification path; no log line carries a message, a page text or a recipient address.
- No page text, no OCR output and no document body is copied into `rwb_comms`: the text stays in `document_text` and the standard container of P5.
- ACE data only through the owner's contract: the case and its owner come from rwb-case and the document reference from rwb-document; this service reads no ACE view and holds no foreign key into another schema (DP-01).
- One hop and a 2 s timeout on every consumed call, with a breaker and a single GET retry (DP-11, ADR-020).
- The notice row and its outbox row commit together or not at all, so no notice exists without its event and no event without its notice.
- No production data, no production copy and no production connection in any test or fixture; every fixture of the wave is synthetic.
- No screen is built here and no route is declared here: the read reaches the officer through gateway-bff (DP-19).

### 18. Traceability

| Requirement or decision | Requirement (short) | Feature | L3 process | Contract element | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted for the agreed types in Thai and English, which needs Thai and English text first | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The rescan notice of an unreadable page in the language of the case; `template.language` and the message text of MSG-P5-018 | TC-E1-049-01, TC-E1-049-03, TC-E1-049-05 |
| REQ-DCM-009 | Documents from every path through the same intake | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | One rescan event per intake item, one notice per event, and the intake item reference on the notice and its event | TC-E1-049-02, TC-E1-049-04, TC-E1-049-08, TC-E1-049-09 |
| REQ-DCM-010 | A file is read only after its malware scan is CLEAN | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The rescan event is raised only for a CLEAN intake item, so no notice exists for an item the document service did not read | TC-E1-049-04, TC-E1-049-07 |
| DP-01 | Owner's schema; no service reads another service's tables | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | `notice`, `template` and `merge_field` in `rwb_comms` and the not-owned list of 12.7 | TC-E1-049-01, TC-E1-049-09 |
| DP-06 | Parameters contract of rwb-case and the client library | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | No parameter is read here; `OCR_MIN_QUALITY` stays P5's and the template reference and channel are rows of `template` | TC-E1-049-01, TC-E1-049-05 |
| DP-07 | Reference data through rwb-case's contract | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | LOV-NOTICE, LOV-CHANNEL, LOV-LANG and LOV-SENT-TYPE reads | TC-E1-049-01, TC-E1-049-05 |
| DP-09 | Outbox, inbox and CloudEvents | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | `NoticeGenerated` and `NoticeDispatched` on `rwb.comms.events.v1`; the rescan event deduped through the inbox | TC-E1-049-01, TC-E1-049-02, TC-E1-049-09 |
| DP-10 | Temporal replaces Quartz; event-started workflow | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | `NoticeDispatchWorkflow` on rwb-comms; no Schedule in this story | TC-E1-049-06 |
| DP-11 | REST contract with mock, one hop, 2 s | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The three consumed rows of 12.2 and the fakes of 12.8 | TC-E1-049-01, TC-E1-049-06, TC-E1-049-10 |
| DP-13 | Per-service REST base | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | `/api/recovery/comms/v1` for the notice read | TC-E1-049-01, TC-E1-049-10 |
| DP-15 | Per-service Flyway | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | `V1049_1__rescan_notice.sql` in `rwb_comms` | TC-E1-049-08 |
| DP-19 | Screen through gateway-bff | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The notice read of the case timeline of section 15 | TC-E1-049-10 |
| ADR-013 | 19 services inside ACE | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The service boundary: rwb-comms writes `rwb_comms` only, and the OCR pipeline stays in rwb-document | TC-E1-049-01 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The outbox writes of 12.3 and the inbox of 12.4 | TC-E1-049-02, TC-E1-049-09 |
| ADR-020 | Contract-first REST, one hop, 2 s | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | Not specified in the source documents (DOR-RWB-P6-E1049-APP-2) | The 2 s budget and the retry rule of 12.2 | TC-E1-049-06, TC-E1-049-10 |

The legacy key is RWB-E1-049. The sibling stories of the key are RWB-P5-E1049-APP (the intake item, the text and the OCR step), RWB-P5-E1049-CON (the event and the document read this story builds against), RWB-P5-E1049-INF and RWB-P5-E1049-OPS (the OCR service connectivity and the job runtime), and RWB-ITG-E1049-ITG (the end-to-end proof across P3, P5 and P6).

### 19. Out of scope

- The OCR pipeline itself, the OCR step of `DocumentIntakeWorkflow`, the quality threshold, the rescan decision and the worker pool: RWB-P5-E1049-APP.
- `document_intake`, `document_text`, the stored OCR output and the document review queue: P5 rwb-document, and the review queue screen SCR-31 with RWB-E1-054.
- The event and document contract this story builds against: RWB-P5-E1049-CON. The OCR service connectivity and the P5 job runtime: RWB-P5-E1049-INF and RWB-P5-E1049-OPS.
- The end-to-end proof across the three services, and the legacy AC1 to AC9 at component level: RWB-ITG-E1049-ITG.
- The case record, its owner, its queue and its tasks: P3 rwb-case; the case list and the case screens.
- Notice generation from a request, the letter path and its approval: RWB-P6-E1052-APP, and the template catalog with its authoring and withdrawal: RWB-P6-E1046-APP.
- Letter dispatch through WIN, proof of delivery and `NoticeDelivered`: RWB-P6-E2021-APP and RWB-P6-E1055-APP.
- SMS and LINE dispatch as a capability of its own: RWB-P6-E2022-APP; this story sends one operational notice through the same path and adds no channel capability.
- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057), the malware scan step (RWB-E1-041), classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The authorisation decision itself, which is enforced at gateway-bff under RWB-PLT-N001-CON and RWB-P4-E1037-CON, not in this story.
- NFR load and performance testing, which belongs to the NFR epic.

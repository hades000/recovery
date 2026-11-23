# RWB-P6-E4041-APP Answer a legal or audit document request

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4041-APP |
| Work type | APP (App development) |
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
| Parallel lane | L-P6-Y |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4041-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-041 for rwb-comms; the answer of a legal or audit document request is served on `/api/recovery/comms/v1` from the notices of this service and the documents of rwb-document. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Legal counsel (RW-LEGAL)**, I want **a legal or audit document request on a case answered on the rwb-comms contract with the index entries of every notice of that case and with the documents rwb-document produces for it, and one decision record written before the answer leaves the service**, so that **a court or an auditor receives a complete, dated and reproducible answer whose every line can be traced to a notice, a document version and a recorded decision, and no answer is ever produced without its decision being recorded**.

### 2. Business rationale

A legal or audit request today is answered by hand: the letters of a case are collected from folders and shared drives, the proof of delivery is chased by phone, and the index the court receives is typed from memory (FSD P6 A2.20.1; FSD P5 A2.6.1). In the target the answer is not one monolith query over one schema. rwb-comms owns the notice, the template, the merge field and the proof of delivery facts; rwb-document owns the document, its custody, its OCR text, its versions and its discovery production; rwb-decision owns the central decision ledger; rwb-case owns the case, its scope and its legal hold; and the screens reach the answer through gateway-bff (Architecture v5 slides 17, 41 and 42; TSD P6 v2 T3.1, T5.2 and T6.1; Ownership Map).

The answer of this key is therefore assembled from two owners and written once. The notice side of the index is built from the `notice` rows of this service — notice id, case id, document id, notice type, sent date, barcode, callback date, delivery status and sent type, which are the TSD P6 T3.1 fields DF-LEG-015 to DF-LEG-023. The document side is read from rwb-document on its contract: the document, its version history and the produced copy with the attributes a court needs to accept it — its origin, the date it entered the hub, whether it has been altered since and who has read it (REQ-DCM-017, REQ-DCM-018; FSD P5 A2.6, FEAT-DCM-06). The service writes one decision record through the local decision-record library before it answers, so a failed record stops the answer instead of producing an unrecorded one (DP-03). The base is `/api/recovery/comms/v1` (DP-13) and the screen reaches the answer through the gateway-bff composite route (DP-19).

The story is the app slice of legacy RWB-E4-041 and it owns the two legacy criteria the service itself satisfies: AC1 (the answer is returned and the result is recorded with the rule version) and AC2 (a decision record that cannot be written changes nothing and shows MSG-P7-003). Both are copied line for line in section 7. The legacy rows around them are the rows of the notice feature and are not this feature's: the screen is SCR-33 Template approval, the validation rule is the withdrawn-template rule VR-P6-020-1 under R-LIT-04, and the Endpoints table names the notice request and the notice read with Litigation rights. They are carried as one conflict row rather than copied into this story (GAP-1154; ASM-2101).

What the target fixes is the split of ownership. The notice and its index fields are `rwb_comms` rows; the document, its version history and the discovery production are rwb-document's and are read on its contract, never from its tables; the decision record is the local library's entry on the shared topic; the authorise decision and the scope are applied at gateway-bff and are not a table of this service; and the answer is served through the composite route. The story serves the rwb-comms half of REQ-DCM-017 and REQ-DCM-018 and gives FEAT-COM-07 its service-side evidence, while the production of the documents, their version history and their court attributes stay with rwb-document.

Two points are carried as gaps and assumptions rather than decided quietly. First, no source publishes an operation of rwb-document that produces a discovery set, and the Ownership Map has no contract row for one, so the document side of the answer is read from the published document read of P5 and the production itself is named as a P5 obligation (GAP-1151; ASM-2098). Second, no source names a document-request operation of this service, an answer shape or a decision code for it, so this story implements the two operations and the answer fixed by RWB-P6-E4041-CON and marks the field-level detail (GAP-1152; ASM-2099).

### 3. Preconditions

- RWB-P6-E4041-CON is published: the two operations on base `/api/recovery/comms/v1`, the request and answer shapes, the index entry field list taken from TSD P6 T3.1, the request state vocabulary, the named consumed rows and the fakes, so this story builds against a fixed contract on Day 1.
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with RWB-PLT-E1027-CON (DP-03), and the platform outbox and inbox relay is in place for the library rows.
- The gateway-bff composite route and the platform error envelope are live with RWB-PLT-N001-CON (DP-19), so the answer reaches the screen without a second base and a refusal carries the standard envelope.
- The `notice`, `template` and `merge_field` tables of `rwb_comms` exist with the TSD P6 T3.1 fields, and notices are generated by the notice stories of this service; this story writes no notice row and moves no notice state.
- The reference lists this story reads are the service's own lists of TSD P6 T3.2: LOV-NOTICE and LOV-DELIVERY, read with the version in force and never written in code (BR-P6-020).
- The document read of rwb-document is available as a contract fake from the first run: the document metadata and version list of `GET /api/recovery/document/v1/documents/{documentId}` and the produced copy of `GET /api/recovery/document/v1/documents/{documentId}/content`. The discovery production behind the document side of the answer is Not specified in the source documents (GAP-1151; ASM-2098).
- The request is opened per case, as the legacy story and the FSD A2.20 describe it. The "named population" of REQ-DCM-017 — one selector across cases — is Not specified in the source documents as a shape of this service's operation (GAP-1153; ASM-2100).
- The capability area and the right of each operation, the scope and the masking are applied at gateway-bff, which asks rwb-access; this story declares no P4 dependency and holds no scope or role table of its own.
- The roles used in section 10 are the rows of TSD P6 T6.1 in force: RW-LEGAL Documents CRUA and Litigation RA, RW-AUDIT Documents R and Litigation R, RW-COMPLY Documents RU and Litigation R.
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are the contract baseline and the two platform contracts, and this story carries no C row (Template and Rules §R5.7).

### 4. Flow

1. A legal counsel opens the document request for case `RC-2026-000321` and sends `POST /api/recovery/comms/v1/cases/{caseId}/document-requests` with an Idempotency-Key. The body carries the request reference, the request kind (legal or audit), the period asked for and the document types asked for.
2. The operation checks the caller through the gateway: the Documents right R on the case, the scope applied, and the case reference present; a caller without the right is refused with 403 and MSG-P4-002 and nothing is written.
3. The service reads its own `notice` rows of the case and builds one index entry per notice from DF-LEG-015 to DF-LEG-023: notice id, case id, document id, notice type, sent date, barcode, callback date, delivery status and sent type. A notice with no `document_id` is listed with its index entry and its document reference empty; it is not dropped.
4. For every distinct `document_id` of the case the service calls the document read of rwb-document, one hop with a 2 s budget, and takes the document metadata and the version list with the date of each version.
5. For every document of the answer the service takes the produced copy and the court attributes — the origin, the date the document entered the hub, the alteration flag and the readers — from rwb-document, which owns them (REQ-DCM-018). Where a source gives no shape for that record, the contract placeholder of RWB-P6-E4041-CON stands (GAP-1151; ASM-2098).
6. The service writes one decision record through the local decision-record library with the rule version in force and the request reference, in the same transaction that stores the request and its index entries (DP-03). The decision code and the rule id of a document request are Not specified in the source documents (GAP-1152; ASM-2099).
7. The request row moves to ANSWERED and the answer is returned with status 201: the request id, the request kind, the case id, the asked-for period and types, the index entries of step 3, one document line per produced document with its version and its court attributes, and the produced-copy references.
8. If the decision record cannot be written, nothing is stored, no index entry and no produced copy leaves the service, the request is not answered, the caller sees MSG-P7-003 and an incident is raised under R-UNI-39 (legacy AC2).
9. A legal counsel, an internal auditor or the compliance and PDPA officer reads the answer with `GET /api/recovery/comms/v1/document-requests/{requestId}` and receives status 200 with the stored answer, its index entries and its document lines exactly as they were answered; the answer is never recomputed at read time.
10. A repeat of the POST with the same Idempotency-Key returns the first answer with status 201 and opens no second request; a repeat inside the same period creates nothing.
11. A GET for a request of a case outside the caller's scope is refused with 404 and the platform not-found envelope, so the answer never discloses the existence of a case outside the scope.
12. A legal hold stops deletion and expiry of a document and stops outbound contact (REQ-DCM-016, R-UNI-20); the answer reads the preserved documents and writes no retention, custody or hold fact of any document.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The decision log cannot be written | Nothing is stored, nothing is produced, the request stays unanswered, the incident is raised | MSG-P7-003 | AC2 |
| X2 | The caller does not hold the Documents right on the case | 403 with the platform refusal; nothing is written | MSG-P4-002 | TC-E4-041-03 |
| X3 | The request id is unknown, or the case is outside the caller's scope | 404 with the platform not-found envelope; no index entry and no document reference is returned | Not specified in the source documents (GAP-1152; ASM-2099) | BR9 |
| X4 | The case reference is missing from the POST | 422 with the field message; no request row is created | MSG-GEN-001 | BR9 |
| X5 | A notice of the case has no document yet | The index entry is returned with its document reference empty; the answer is not refused | None | BR5 |
| X6 | The rwb-document read does not answer inside 2 s | The answer is not returned; the request stays OPENED and is retried once with jitter | Not specified in the source documents (GAP-1151; ASM-2098) | BR11 |
| X7 | A produced copy cannot be read from the store | The document line is returned with its reference and a pending state, and the caller is told the copy is not yet available | Not specified in the source documents (GAP-1155; ASM-2102) | BR11 |
| X8 | The same POST is repeated with one Idempotency-Key | The first answer is returned with status 201; no second request exists | None | BR10 |

X1 is legacy AC2 and is the only exception path of the legacy story. X2 and X4 are the refusal conditions the legacy permission and validation tables name for the feature; X3, X6 and X7 carry the placeholders because no source gives their message or their state.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4041-CON and the two platform contracts only. The document read, the produced copy and the decision-record library are contract fakes from the first run; there is no C and no I row |
| Negotiable | The request kinds, the period, the document types and the answer layout are the contract's; the field-level detail of the document side and the decision code are open and marked, and the story fixes the order of the answer and the fail-closed rule |
| Valuable | A court or an auditor gets one dated answer with the index entries of every notice of the case and one decision record behind it, instead of a hand-built folder |
| Estimable | Two operations, one index assembler, one document adapter, one decision-record write, two tables and one migration |
| Small | Fits one sprint with its tests, as the app slice of the legacy key |
| Testable | Both criteria run as automated tests against the contract fakes, and every refusal has its status code and its envelope |

### 7. Acceptance criteria

```gherkin
Feature: Answer a legal or audit document request — the rwb-comms slice

  Background:
    Given the document request operation is "POST /cases/{caseId}/document-requests" under the base "/api/recovery/comms/v1"
    Given notice "N-0101" of case "RC-2026-000321" is of notice type "DEMAND" with document "DOC-0101", sent date 2026-12-15, barcode "RR223344556TH" and delivery status "DELIVERED"
    Given "LEG-0001" holds RW-LEGAL with the Documents right R on case "RC-2026-000321"

  Scenario: AC1 Answer a legal or audit document request (legacy RWB-E4-041 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-document contract mock returns document "DOC-0101" of case "RC-2026-000321" with its version history, its origin, its entry date, its alteration flag and its readers
    When the user acts on the screen
    Then returns the documents and the index entries a legal or audit request asks for
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-041 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

Both criteria above are the legacy criteria of RWB-E4-041, copied line for line with the origin tag on each scenario line. One `Given` line is added inside AC1 for the part of the answer that another owner supplies: the document, its version history and the court attributes are rwb-document's, and the mock line names them without changing a value of the legacy text. The screen of the legacy story is SCR-33 Template approval, which is not the screen of this feature; the answer is served to the Litigation and Documents screens through the gateway-bff composite route and the screen itself belongs to RWB-PLT-N001-CON (GAP-1154; ASM-2101).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An answer carries the index entry of every notice of the case and one line per produced document; a notice without a document is listed, never dropped | REQ-DCM-017; FSD P6 A2.20.2 |
| BR2 | A produced document carries its origin, the date it entered the hub, whether it has been altered and who has read it, and those facts are rwb-document's, read and never rewritten here | REQ-DCM-018; FSD P5 A2.4.3.2 |
| BR3 | One decision record is written before the answer is returned, in the same transaction that stores the request and its entries; a failed record stops the answer | Legacy RWB-E4-041 AC1 and AC2; R-UNI-39; DP-03 |
| BR4 | An answer is stored as answered and is read back unchanged; a read never recomputes it | Legacy RWB-E4-041 AC1; DP-03 |
| BR5 | The index entry fields are the TSD P6 T3.1 fields DF-LEG-015 to DF-LEG-023 and nothing else is added to them by this story | TSD P6 v2 T3.1 |
| BR6 | The notice type and delivery status values are the lists of TSD P6 T3.2 (LOV-NOTICE, LOV-DELIVERY) read with the version in force; no value is written in code | FSD P6 A2.20.3.1 BR-P6-020; TSD P6 v2 T3.2 |
| BR7 | The capability area is Documents with right R on both operations, and the scope and the masking are applied at gateway-bff; the roles are the rows of TSD P6 T6.1 | TSD P6 v2 T6.1; FSD P6 A2.20.3.3; DP-19 |
| BR8 | The request is opened per case, as the path, the legacy story and the FSD describe it; a selector across cases is not an operation of this service | FSD P6 A2.20.2; legacy RWB-E4-041 Endpoints |
| BR9 | A request with no case reference is refused with 422, and a request or a case outside the caller's scope with 404; a refusal writes nothing | FSD P6 A2.20.4.3 AC-EXC-P6-020-01; Template and Rules §R7.2 s14 |
| BR10 | A repeat with the same Idempotency-Key returns the first answer and opens no second request | Architecture v5 slide 11 |
| BR11 | Every cross-service call is one hop with a 2 s budget and a breaker per downstream; a missing document answer never returns a partial answer as complete | ADR-020 |
| BR12 | The notice, its index fields and the request rows are `rwb_comms` rows; the document, its versions, its court attributes and the discovery production are rwb-document's and are read on its contract, never from its tables | Architecture v5 slides 17 and 41; TSD P6 v2 T5.2 |
| BR13 | A legal hold stops deletion and expiry of a document and outbound contact; this story reads the preserved documents and writes no custody, retention or hold fact | REQ-DCM-016; R-UNI-20 |
| BR14 | The answer carries no personal data: notice ids, case ids, document ids, document types, barcodes, dates and status codes only, and the produced copy is a claim-check reference read on the owner's contract | Architecture v5 slides 42 and 43 notes; Template and Rules §R7.2 s17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| (none) | The POST arrives and the caller holds the Documents right R on the case | The case reference is present and the case is in scope | OPENED, and the index entries of the case are written |
| OPENED | The document read answers for every distinct document id | Every metadata and version answer is in hand | OPENED with the document lines complete |
| OPENED | The decision record is written and the answer is stored | The library answers within its budget | ANSWERED |
| OPENED | The decision record cannot be written | The library fails or times out | OPENED, with nothing stored and the incident raised under R-UNI-39 |
| OPENED | The same POST is repeated with the same Idempotency-Key | The first answer exists | ANSWERED, with the first answer returned |
| ANSWERED | Any further POST or GET | The stored answer is read | ANSWERED; nothing is recomputed and nothing changes |

The notice states of this service are not moved by this story: a notice stays in the state its own stories set, and the answer reads it. The case state, the legal hold and the scope are rwb-case's and are read through the platform guard, never written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LEGAL, legal counsel | Documents CRUA and Litigation RA in TSD P6 T6.1: opens a legal or audit document request and reads its answer (right R on both operations) |
| RW-AUDIT, internal audit | Documents R in TSD P6 T6.1: opens an audit document request and reads its answer |
| RW-COMPLY, compliance and PDPA officer | Documents RU in TSD P6 T6.1: reads the answers of the cases in scope |
| RW-LITOFF, litigation officer | Documents CRU in TSD P6 T6.1: opens and reads the answer of a litigation case |
| RW-CASEOWN, case owner | Documents CRU in TSD P6 T6.1: reads the answer of the case owned |
| RW-PLATADM, platform administrator | Documents R in TSD P6 T6.1: reads the answers when a case is disputed and the feature switch is checked |
| RW-CONDUCT, conduct and QA officer | Documents R in TSD P6 T6.1: reads the answers for a conduct review |
| rwb-comms service identity | Reads its own `rwb_comms` rows, calls the rwb-document contract, writes its request rows and the library rows (DP-03) |
| Decision-record library identity | Writes the local decision record of an answer and relays it on `rwb.decision-record.v1` (DP-03) |

The rights above are read from the matrix of TSD P6 T6.1 only. The legacy permission table names Litigation C and Litigation R for the two notice operations of the notice feature, which are not the operations of this story (GAP-1154; ASM-2101). The authorise decision and the scope are applied by gateway-bff, which asks rwb-access; this story declares no P4 dependency.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice, in `rwb_comms` | id | Read; the first field of the index entry |
| DF-LEG-016 | notice, in `rwb_comms` | case_id | Read; filters the answer to the case |
| DF-LEG-017 | notice, in `rwb_comms` | document_id | Read; the document reference of the index entry |
| DF-LEG-018 | notice, in `rwb_comms` | notice_type | Read; LOV-NOTICE |
| DF-LEG-019 | notice, in `rwb_comms` | sent_date | Read |
| DF-LEG-020 | notice, in `rwb_comms` | barcode | Read |
| DF-LEG-021 | notice, in `rwb_comms` | callback_date | Read |
| DF-LEG-022 | notice, in `rwb_comms` | delivery_status | Read; LOV-DELIVERY |
| DF-LEG-023 | notice, in `rwb_comms` | sent_type | Read; LOV-SENT-TYPE |
| Standard column | notice, in `rwb_comms` | state | Read, so a withdrawn or held notice is visible in the answer |
| No BR Field ID | document_request, in `rwb_comms` | id, case_id, request_kind, period_from, period_to, document_types, requested_at, requested_by, state, answer_ref | Write on the POST, read on the GET; the field list and the types are Not specified in the source documents (GAP-1152; ASM-2099) |
| No BR Field ID | document_request_entry, in `rwb_comms` | request_id, notice_id, document_id, notice_type, sent_date, barcode, callback_date, delivery_status, sent_type, document_version, origin, entry_date, altered, readers | Write when the answer is stored, read on the GET; the document-side fields are Not specified in the source documents (GAP-1151; ASM-2098) |
| DF-DEC-001 to DF-DEC-018 | decision record, local, through the library | decision code, rule, case, request, decided at, hash chain | Write through the library; the decision code is Not specified in the source documents (GAP-1152; ASM-2099) |
| DF-DOC-001 to DF-DOC-011 | document, through the rwb-document contract | id, case_id, document_type, source, storage_ref, version list and the court attributes | Read through the contract, never a table |
| DF-DOC-002 | document, through the rwb-document contract | person_key | Never selected and never copied into an answer or an event; the index entry carries the document id only |

The answer of this service holds no file and no copy: every produced document is a reference, and the bytes are read on the content operation of rwb-document at the moment a court or an auditor asks for them, which is the claim-check rule of the architecture and keeps a copy of a document out of `rwb_comms` (Architecture v5 slides 42 and 43 notes). Two tables are added by this story, `document_request` and `document_request_entry`, both in `rwb_comms`, with the indexes `ix_document_request_case` on `document_request (case_id, state)`, `ix_document_request_entry_request` on `document_request_entry (request_id)` and `ix_document_request_entry_document` on `document_request_entry (document_id)`. The migration is one per-service step in `rwb_comms`. No personal data is written to `rwb_comms`: no name, no address, no identity number and no account number is a column of the two tables, `requested_by` is a synthetic system identity and the readers of a produced document are user ids as rwb-document holds them.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. No source names a document-request operation, so these two paths, their status codes and their answer shape are fixed by RWB-P6-E4041-CON and this story implements them and adds no path (GAP-1152; ASM-2099).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/document-requests` | Open a legal or audit document request and return its answer, 201 with the DocumentRequestAnswer | Documents, right R, scope applied | Idempotency-Key header, answer kept 24 hours |
| GET | `/document-requests/{requestId}` | Read the stored answer with its index entries and its document lines, 200 with the DocumentRequestAnswer | Documents, right R, scope applied | Not applicable |

Errors: 401 no session; 403 the role lacks the Documents right (MSG-P4-002); 404 the case or the request is absent or out of scope; 422 a field fails validation (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003) or a consumed call is unavailable. The answer body carries `requestId`, `caseId`, `requestKind`, `periodFrom`, `periodTo`, `documentTypes`, `state`, `answeredAt`, `entries[]` with the nine index fields of section 11, and `documents[]` with the document id, the version list and the court attributes; the exact types and required flags of the added fields are Not specified in the source documents (GAP-1152; ASM-2099).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | The metadata, the extracted fields and the version list of a notice document, faked. Consumed without a declared C row (GAP-1151; ASM-2098) |
| GET | `/api/recovery/document/v1/documents/{documentId}/content` | P5 rwb-document | The produced copy of a document version as `application/octet-stream`, faked; the answer holds the reference only |
| POST | the discovery production of rwb-document | P5 rwb-document | The production of every document of the request with its metadata and its version history (REQ-DCM-017) and the court attributes (REQ-DCM-018). No path, request or answer is published by any source (GAP-1151; ASM-2098) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. No row reads a table and no row reads a `v_ace_*` view. The document rows carry the placeholder for the discovery selector, the discovery answer shape and the court attribute record, because the source documents describe the outcome of an electronic discovery request and publish no operation for it (FSD P5 A2.6; Program BRD REQ-DCM-017, REQ-DCM-018).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | request id, case id, decision code, rule id, rule version, decided at, record reference |

This story publishes no event on `rwb.comms.events.v1`. The catalogue has no document-request, custody or retention event, and one is not invented here; NoticeGenerated, NoticeDispatched and NoticeDelivered belong to the notice stories of this service (Architecture v5 slide 42). The decision record above is written by the local library of DP-03 and is not an event of rwb-comms.

#### 12.4 Events consumed

None. No event of the catalogue names rwb-comms as the consumer of a document event: DocumentStored (EV-16) and DocumentFieldsExtracted (EV-17) name rwb-agent and rwb-case (Architecture v5 slide 42). The answer therefore reads the rwb-document contract at request time and takes no event.

#### 12.5 Workflows and activities

None. The answer is synchronous: one POST, one decision-record write, one answer. No workflow, no child workflow and no activity is registered by this story, and no durable timer is needed, because the request is answered inside the call and a failure leaves it OPENED for a retry by the caller.

#### 12.6 Schedules

None. No job of the catalogue belongs to this key (Architecture v5 slide 44): JOB-10 WIN notices and JOB-11 outbox relay are the notice and platform jobs, and JOB-17 retention is rwb-document's. Nothing is scheduled here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | Read only here: the nine index fields of the answer; written by the notice stories of this service |
| template | P6 (rwb_comms) | Not written and not read by this story; the notice generation owns it |
| merge_field | P6 (rwb_comms) | Not written and not read by this story |
| document_request | P6 (rwb_comms) | New: the request, its selector, its state and its answer reference (fixed by RWB-P6-E4041-CON) |
| document_request_entry | P6 (rwb_comms) | New: the frozen index entries and document lines of one answer |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of an answer (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The library rows of the record and the POST idempotency |

Not owned and never read: `document`, `document_intake`, `document_text`, `document_field`, `document_type`, `document_custody`, `signature_request`, `retention_rule`, `retention_action` and `case_document_check` (P5); `recovery_case`, `task`, `timer`, `queue` and `assignment` (P3); `decision_log_entry`, `rule_row` and `approval` (P7); `interaction` (P1); `outbound_item` and `interface_config` (P2); `deviation` (S8). The document, its versions and its court attributes are reached through the rwb-document contract, the case facts through the platform guard, and the decision entry through the library; no foreign key crosses a service boundary.

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-document document fake | The document metadata and version list | Document `DOC-0101` of case `RC-2026-000321` with two versions and their dates; a document of another case for the refusal path; a delayed answer beyond 2 s |
| rwb-document content fake | The produced copy | The copy of version 1 and version 2 of `DOC-0101`; a copy that is not yet stored |
| rwb-document discovery fake | The discovery production | The answer of REQ-DCM-017 for the case with the metadata and the version history, carrying the placeholder rows of GAP-1151 |
| decision-record library stub | The local record and the shared topic | A healthy chain and outbox; a stopped chain for AC2 |
| rwb-comms notice fixture | The index entries | Notices `N-0101` and `N-0102` of case `RC-2026-000321`, one with a document and one without, the second delivered and the first pending |

The fakes are derived from RWB-P6-E4041-CON and the drift test of that story fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The request-and-answer POST and the answer GET provided; the document metadata, the produced copy and the discovery production consumed; one hop, 2 s |
| Kafka | 1 record through the library, 0 published by this service, 0 consumed | DecisionRecorded on `rwb.decision-record.v1` through DP-03 |
| Temporal | None | The answer is synchronous and registers no workflow |
| File | None | The produced copy is a claim-check read on the rwb-document content operation; this service stores no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `documentrequest`, Java package `th.co.scb.ace.workbench.recovery.comms.documentrequest`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is not in the pattern set of this key and this story declares no table of another service: the legacy Data table named `document`, `decision_log_entry` and `rule_row`, and in the target the document and its versions are read on the rwb-document contract, the decision entry is the local library's row and no rule row is read at all, because the rule version comes with the record the library writes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentRequestController | Controller | `POST /cases/{caseId}/document-requests` and `GET /document-requests/{requestId}` with validation, the Idempotency-Key and the problem mapping for 401, 403, 404, 422 and 503 |
| DocumentRequestService | Service | Opens the request, orders the steps, stores the answer and refuses a read outside the case scope |
| IndexEntryAssembler | Service | Builds one index entry per notice from DF-LEG-015 to DF-LEG-023 and keeps a notice with no document in the answer |
| DocumentClient | Adapter | The metadata, the version list and the produced copy of rwb-document, one hop with a 2 s budget and a breaker |
| DiscoveryClient | Adapter | The discovery production of rwb-document for the case, with the placeholder rows until P5 publishes the operation |
| DecisionRecordWriter | Service | Writes the local decision record of the answer through the library and fails the call when it cannot |
| AnswerStore | Service | Writes `document_request` and `document_request_entry` in one transaction with the decision record and reads them back unchanged |

**Database and migrations**

- Writes `document_request`, `document_request_entry`, the local decision record and the library rows, all in schema `rwb_comms`; reads `notice` of the same schema; reads no other schema.
- Migration in this story: `V4041_1__document_request.sql` creates the two tables with the standard record columns, the three indexes of section 11, the request state check constraint with the values of section 9, and the reference to `notice` by `notice_id` inside `rwb_comms` only.
- No column carries a name, an address, an identity number or an account number, and no row of `notice` is written.

**Configuration and reference data**

- `rwb.comms.document-request` feature switch, read as a parameter: off answers 503 with the platform envelope and writes nothing, so a contested case can be held without a code change.
- The request kinds `LEGAL` and `AUDIT`, the request states of section 9 and the answer layout are fixed by RWB-P6-E4041-CON.
- LOV-NOTICE and LOV-DELIVERY are the lists of TSD P6 T3.2 read with the version in force; no value of either is written in code (BR-P6-020).
- The decision code and the rule id of a document request are Not specified in the source documents (GAP-1152; ASM-2099) and are parameters read with their version, not constants.

**Build steps**

1. DocumentRequestController and DocumentRequestService over the two operations, the Idempotency-Key and the refusal mapping; tests for the refusal and the repeat.
2. IndexEntryAssembler over the nine notice fields, with the notice that has no document; test for the index entry set.
3. DocumentClient and DiscoveryClient with the three consumed rows and their fakes, the 2 s budget and the breaker.
4. DecisionRecordWriter and the fail-closed path: a failed record leaves the request OPENED and shows MSG-P7-003; test for AC2.
5. AnswerStore with the two tables, the one transaction and the unchanged read back; test for AC1.
6. The contract-fake run of the whole answer before the real rwb-document is live, and the drift test against RWB-P6-E4041-CON.

**Feature switch.** `rwb.comms.document-request`, read as a parameter; off refuses the request and writes nothing.

**Done when.** The tests of section 16 pass, the contract tests of RWB-P6-E4041-CON stay green, and a test week shows every answer with one index entry per notice of its case, one decision entry behind it, no answer stored when the record failed, and no name, address or account number anywhere in the two tables.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. |
| MSG-P6-003 | The template of a notice of the case was withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | A notice of the case was acknowledged by WIN | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | A contact stop is in force on the case | Contact with this customer is stopped for {reason}. |

MSG-P7-003, MSG-P4-002, MSG-GEN-001, MSG-P6-003, MSG-P6-004 and MSG-P6-001 are copied unchanged from the legacy story of RWB-E4-041. MSG-P6-003, MSG-P6-004 and MSG-P6-001 are the notice messages that the legacy validation table carries beside them; the answer of this story names the notice state and does not repeat them, so they stay in the table for the screen that shows the notice beside the request. The legacy story gives no message for an absent request or for an out-of-scope case, and the platform not-found envelope stands with its message id Not specified in the source documents (GAP-1152; ASM-2099).

### 15. Screens and states

The legacy story names SCR-33 Template approval, which is the administration screen of the template catalogue and not the screen of a document request (GAP-1154; ASM-2101). The answer of this story is served through the gateway-bff composite route (DP-19) to the documents and litigation surfaces of the case, and this story fixes the answer and its states only:

| State of the request | What the caller sees and does |
|---|---|
| OPENED | The request is open and not yet answered; the screen shows the case, the request kind and the period, and offers a retry |
| ANSWERED | The index entries of every notice of the case, the document lines with their version and their court attributes, and the link to the produced copy on the rwb-document content operation |

A request in OPENED after a failed record is shown with MSG-P7-003 and an incident reference under R-UNI-39. The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen; this story adds no screen of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-041-01 | AC1, BR1, BR3 | End to end | Case `RC-2026-000321` with notices `N-0101` and `N-0102`; the rwb-document fake answers with document `DOC-0101` and its two versions; one decision entry exists and the answer is stored |
| TC-E4-041-02 | AC2, BR3 | End to end | The decision-record library stub returns a stopped chain; nothing is stored and MSG-P7-003 is shown |
| TC-E4-041-03 | Access, BR7, BR9 | Component | `AUD-0001` without the Documents right on the case sends the POST; refused with 403 and MSG-P4-002 and nothing is written |
| TC-E4-041-04 | Principle 5, BR3 | NFR | The decision log write is forced to fail on ten answers in a row; no request reaches ANSWERED and ten incidents are raised |

The four legacy cases keep their legacy order and their legacy data; the level column maps the legacy System to End to end, Access to Component and Principle 5 to NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the request kinds, the request states, the answer layout, the decision code, the rule id, LOV-NOTICE and LOV-DELIVERY are data rows and parameters read with the version in force.
- No personal data in events, logs, workflow inputs, tests or prompts: request ids, case ids, document ids, notice ids, document types, barcodes, dates and status codes only; `document.person_key` is never selected and the readers of a produced document are user ids as rwb-document holds them.
- No read of another service's tables and no `v_ace_*` read: the document, its versions and its court attributes arrive on the rwb-document contract, and no SQL of this service names a `rwb_document` table.
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; this story declares no other service's base or topic as its own.
- No event is invented: the catalogue has no document-request event, and the only element this story causes is the decision record of the library on `rwb.decision-record.v1`.
- The answer is stored as answered: a read never recomputes it, so a court receives the same answer twice.
- A record that cannot be written stops the answer: nothing is stored, nothing leaves the service and the incident is raised (R-UNI-39).
- One hop and 2 s on every call; a timeout never returns a partial answer as complete, and a produced copy that is not stored is reported as pending, never as delivered.
- The produced copy is a claim-check reference: no file of a document is written to `rwb_comms` and no copy of a document leaves through this service.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-017 | An electronic discovery request produces every document for a named population with its metadata and its version history | Business Requirements Program, section 5.5 P5 Document hub | FEAT-COM-07, FEAT-DCM-06 | 13 Manage documents and correspondence | BR-P6-020 | TC-E4-041-01, TC-E4-041-04 |
| REQ-DCM-018 | A produced document carries its origin, its entry date, its alteration flag and its readers | Business Requirements Program, section 5.5 P5 Document hub | FEAT-COM-07, FEAT-DCM-06 | 13 Manage documents and correspondence | BR-P6-020; R-UNI-39 | TC-E4-041-01, TC-E4-041-02 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-041, disposition Split (rework) |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-041 ACn) |
| Test cases | TC-E4-041-01 to TC-E4-041-04, all four in the legacy order |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record plus central ledger) |
| Rules | R-LIT-04, R-UNI-20, R-UNI-39, BR-P6-020 |

The supporting features of the legacy key — FEAT-COM-07 (answer a legal or audit document request) and FEAT-DCM-06 (search documents across cases) — are answered here for the rwb-comms slice and by rwb-document for the document slice, and this story changes none of their designs.

### 19. Out of scope

- The document, its custody, its OCR text, its fields, its versions and the discovery production itself: rwb-document (P5), with FEAT-DCM-06 and the search and index stories of that service. This story reads them on the owner's contract and holds no copy.
- The court attributes of a produced document — its origin, its entry date, its alteration flag and its readers — and the records management position behind them: rwb-document (P5), REQ-DCM-018 and REQ-DCM-020. This story names them in the answer and certifies none of them.
- Notice generation, dispatch and proof of delivery for the notices the answer indexes: the notice stories of rwb-comms, and the retention and legal hold stories of this key (`RWB-P6-E4042-APP`, `RWB-P6-E4042-CON`).
- The retention classes, the legal hold and the disposal of a document: rwb-document (P5), REQ-DCM-010, REQ-DCM-016 and REQ-DCM-019.
- The template catalogue and the withdrawn-template path of R-LIT-04 and R-LIT-06: the template stories of this service. The legacy row VR-P6-020-1 belongs to that path and not to the answer (GAP-1154; ASM-2101).
- The case state, the queue, the task of a failed request and the scope: rwb-case (P3) and the platform guard. This story reads the case facts and writes none.
- The authorise contract, the roles, the scope and the masking: rwb-access (P4) and gateway-bff, with RWB-PLT-N001-CON.
- The screen of the request and of the answer, its field list and its composite route: RWB-PLT-N001-CON and the stories that own each screen. The legacy SCR-33 is not that screen.
- The contract documents, the answer schema and the fakes as published artefacts: RWB-P6-E4041-CON.
- The cross-service journey from the court request to the produced copy: no integration story of this baseline covers it, and this story proves the answer against the contract fakes.
- The archive or export file of an answer, if a court asks for one file rather than a list: not an operation of this baseline (GAP-1155; ASM-2102).

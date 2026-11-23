# RWB-P5-E1018-APP Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P5-E |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1018-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (no FR mapped to REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CWC-004, REQ-CWC-005, REQ-CWC-016, REQ-CHO-004) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the case binding of the document hub, split from RWB-E1-018, so that every document record of rwb-document is held against the one case ID that rwb-case issues and resolves that case through the rwb-case contract on every store. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN), a litigation officer (RW-LITOFF) and the document store itself**, I want **every document record of rwb-document held against the one case ID that rwb-case issued, that case ID resolved on the rwb-case contract on every store and a case the contract does not return refused, with no case attribute copied into the document schema and no case ID ever derived from a file name, an OCR text or any other value**, so that **every document on a case refers to that one case ID, a reader sees the case number of the case the document really belongs to, and no second reference and no copy of case data exists in the document hub**.

Inside `rwb-document` this is the case binding of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The case ID is issued by rwb-case (RWB-P3-E1018-APP) in the form RW-YYYY-NNNNNN, once, never reused. This service never issues, formats or renumbers it: it takes the value it is given, confirms it on the contract `GET /api/recovery/case/v1/cases/{caseId}` of RWB-P3-E1018-CON (one hop, 2 s, DP-11), and writes it to `document.case_id` (DF-DOC-002).
- The case number (RW-YYYY-NNNNNN) is read through the same contract at display time and is never stored in `rwb_document`.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1038; ASM-1986); this story uses the phrase "the rwb-document login (DP-02)" and never the shared monolith login.

The legacy facts are unchanged: a document is held against one case, the case links to ACE by business key with no foreign key (legacy BR11, D-RCV-35 U4, ADR-010), and a repeated store creates nothing new (legacy AC8).

### 2. Business rationale

Recovery teams keep their own lists today, so one account can be on several trackers under different references and one document can sit in a folder named after an account, a contract number or a court reference rather than the case. Legacy RWB-E1-018 answered this for the case: one case per customer and product, an ID in the form RW-YYYY-NNNNNN issued at creation and never reused, printed on every letter and document (REQ-CWC-002). The document hub is where that promise is either kept or broken, because a document that carries its own copy of a case number, or a case ID guessed from the file name, becomes a second reference to the same case.

This story keeps the promise on the document side:

1. One case ID on every document, held in `document.case_id` and never a second reference: no case number, no product group, no owner, no queue and no status column exists in `rwb_document`.
2. The case ID is confirmed on every store against the owner of the case, through the rwb-case contract of RWB-P3-E1018-CON. A case the contract does not return, or one that sits outside the reader's scope, is refused and nothing is stored.
3. No copy of case data and no cross-schema read: the document hub holds its own metadata and reads the case only through the contract (DP-01, DP-05).

This story is the rwb-document part of legacy RWB-E1-018. Case creation, the entry and exclusion rules, the numbering sequence and the yearly range stay with rwb-case (RWB-P3-E1018-APP); the ACE view read behind the entry and exclusion decisions stays with rwb-source-data (RWB-P1-E1018-APP); the access decision stays with rwb-access (RWB-P4-E1018-APP); the decision record of a case creation stays with rwb-decision (RWB-P7-E1018-APP); the store, the versions, the write-once container and the OCR pipeline stay with RWB-P5-E1024-APP. This slice delivers the binding and its refusals, nothing else. It meets REQ-CWC-002 and REQ-CWC-003 and supports REC-05 (every business key on a case resolves to its ACE row): a document can only point at a case that the case service confirms.

### 3. Preconditions

- RWB-P3-E1018-CON is published: the rwb-case contract with `GET /cases/{caseId}`, the case answer carrying the case ID and the case number, the error envelope, the not-found and the out-of-scope answers, and its fake (DP-11). The request and response field names of that read are Not specified in the source documents (GAP-1038; ASM-1986).
- The rwb-document baseline is in place from the service-template work (RWB-PLT-TPL): schema `rwb_document`, the rwb-document login (DP-02; its name is Not specified in the source documents (GAP-1038; ASM-1986)), the base `/api/recovery/document/v1`, the topic `rwb.document.events.v1`, the task queue `rwb-document` and the deployment chart.
- RWB-P5-E1024-APP delivers the store, the index, the versions, the containers and the OCR path; this story binds its rows to the case, adds no build dependency of its own, and its tests run against the store fake of RWB-P5-E1024-APP.
- The document type list LOV-DOC-TYPE and the source list LOV-DOC-SOURCE are in force and are read by the store story through the reference-data contract of DP-07; no list value is written in this story's code.
- The two synthetic facts the tests use: case `RW-2026-000123` for borrower `P-0101` with accounts `A-5001` and `A-5002`, and a document `notice-0001.pdf` of type COURT_NOTICE (legacy story AC1, AC2 and FSD P5 AC-P5-001-01).
- Readers hold Documents R and writers hold Documents C in the capability area of the screen or action (TSD P5 T6.1); the authorisation decision itself is the cached permission decision the service template holds from rwb-access, and this story adds no guard of its own.
- The outbox and inbox library exists in `rwb_document` (DP-09), although this slice publishes nothing of its own; the store story publishes `rwb.document.DocumentStored.v1` with the case ID as the key.

### 4. Flow

1. A caller stores a document against a case: the request names `caseId`, the document type and the source, and the file. The case reference is the contract identity of the case, never a case number typed from the paper and never a value read out of the file.
2. rwb-document: `CaseReferenceClient` calls `GET /api/recovery/case/v1/cases/{caseId}` on rwb-case, one hop within the 2 s budget (DP-11). The answer is held for this request only; no case answer is cached across requests.
3. rwb-document: a case the contract does not return is refused — 404 with the not-found message, whose ID is Not specified in the source documents (GAP-1038; ASM-1986) — and nothing is written: no `document` row, no `document_field` row and no event.
4. rwb-document: a case outside the caller's scope is refused with 403 and MSG-P4-003; the answer carries no document metadata, no case number and no case attribute.
5. rwb-document: `DocumentCaseBinding` takes the case ID from the contract answer and writes `document.case_id` (DF-DOC-002, NOT NULL) with `doc_version` 1 (DF-DOC-011), `content_sha256` (DF-DOC-026) and `is_active` true. No other case value is written: the case number, the product group, the owner, the queue and the status stay in `rwb_case`.
6. rwb-document: the extracted fields (DF-DOC-012 to DF-DOC-017) are written against the document ID; they are fields of the document, not of the case, and the unknown document type and file type checks stay in RWB-P5-E1024-APP.
7. rwb-document: a repeated store of the same file for the same case — the same `Idempotency-Key`, the same `content_sha256` — resolves the case once and writes one `document` row; the repeat answers the first result and writes no second row (legacy AC8).
8. rwb-document: a new version of the same document writes `doc_version` n+1 and `previous_version_id` (DF-DOC-025) against the same case ID, and flips `is_active` to false on the earlier row; a case ID never changes on a document row.
9. Display: SCR-30 Case documents and SCR-03 Case record ask rwb-document for the documents of a case by case ID, and the case number shown beside them is read from the rwb-case contract at display time by gateway-bff — never from a column of `rwb_document`.
10. Index and key: the case documents read is keyed by the case ID, and the case ID is the Kafka key of anything the store story publishes for the case on `rwb.document.events.v1` (DP-09).

The binding is written before the document row commits, in one transaction: a store whose case cannot be confirmed leaves nothing behind.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The rwb-case contract returns no case for the case ID in the request | 404; nothing stored and no event; no document row and no field row | The not-found message, whose ID is Not specified in the source documents (GAP-1038; ASM-1986) | AC2 |
| X2 | The case exists but sits outside the caller's scope | 403; no document metadata, no case number, no case attribute; nothing stored | MSG-P4-003 | AC6 |
| X3 | The file name or the OCR text carries a different case-like string, for example another RW- number or a court reference | The string is ignored: only the case ID of the request is bound, and nothing is derived from the file | None | AC3 |
| X4 | The same document and case are stored twice | One `document` row; the repeat answers the first result and writes no second row (legacy AC8) | None | AC5 |
| X5 | The rwb-case contract does not answer inside the 2 s budget, or answers an error | One hop, 2 s (DP-11); the store is refused on the unconfirmed case, nothing is written from a partial answer, and the caller retries | The not-found message, whose ID is Not specified in the source documents (GAP-1038; ASM-1986) | AC2 |
| X6 | The request names no case reference | Refused before the contract call and before any write; nothing stored | MSG-GEN-001 with "a case reference" | AC1 |

A case whose bound case is later closed keeps its binding: this service reads the case and does not copy its state, so no document row moves when a case closes (legacy AC4, the number is never reused and never reissued).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published rwb-case contract and its fake (RWB-P3-E1018-CON) and the `rwb_document` baseline; it calls no other service at run time |
| Negotiable | Nothing business is fixed here: the case ID and the case number are values of the case service, and the document types and sources are lists |
| Valuable | One case ID on every document, one refusal for a case that does not exist or is not in scope, and no copy of case data in the document hub |
| Estimable | One contract client, one binding, one repository write, one index read |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key |
| Testable | Every criterion in section 7 is one automated test against the contract fake, with the synthetic case, accounts and document of the legacy story |

### 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1 — the case binding of rwb-document

  Background:
    Given the rwb-case contract mock returns case "RW-2026-000123" with case number "RW-2026-000123" for borrower "P-0101"
    Given the caller holds Documents C in scope for case "RW-2026-000123"

  Scenario: AC1 The case reference is resolved and written, and no case attribute is copied (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000123" with case number "RW-2026-000123"
    When a document "notice-0001.pdf" of type "COURT_NOTICE" and source "SCAN" is stored for case "RW-2026-000123"
    Then one document row exists with case_id "RW-2026-000123", doc_version 1 and is_active true
    Then the store called GET /api/recovery/case/v1/cases/RW-2026-000123 once, within the 2 s budget
    Then the document row holds no case number, no product group, no owner, no queue and no status
    Then the case number "RW-2026-000123" is read from the contract when the document is displayed, never from the document row
    Then the extracted field "court_name" of the document is written against the document, not against the case

  Scenario: AC2 No case returned by the contract means 404 and nothing stored (new, D-RCV-60)
    Given the rwb-case contract mock returns no case for "RW-2026-000122"
    When a document of type "COURT_NOTICE" is stored for case "RW-2026-000122"
    Then the store is refused with 404 and the not-found message, whose ID is Not specified in the source documents (GAP-1038; ASM-1986)
    Then no document row and no document_field row is written
    Then no DocumentStored event is written to the outbox
    Then the refusal names no case number and no account

  Scenario: AC3 The case ID is never derived from the file (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000123" and returns no case for "RW-2026-000999"
    Given the file is named "RW-2026-000999-notice-0001.pdf" and its OCR text holds "RW-2026-000999"
    When the document is stored for case "RW-2026-000123"
    Then the document row holds case_id "RW-2026-000123" and not "RW-2026-000999"
    Then no case "RW-2026-000999" is read from the contract and no document row is written against it
    Then the file name and the OCR text are stored as file metadata and document text only, never as a case reference

  Scenario: AC4 The case number is read through the contract at display and never stored (new, D-RCV-60)
    Given case "RW-2026-000123" was closed and the rwb-case contract mock still returns it with case number "RW-2026-000123"
    Given a document of type "COURT_NOTICE" is held against case "RW-2026-000123"
    When a reader opens SCR-30 Case documents for the case
    Then the document is listed with case number "RW-2026-000123" read from the contract in that request
    Then the schema "rwb_document" has no column holding a case number and the document row's case_id is unchanged
    Then a case the contract no longer returns shows the not-found message for the case and no case number is printed from a stored value

  Scenario: AC5 A repeated store resolves the case once and writes one row (new, D-RCV-60)
    Given the rwb-case contract mock returns case "RW-2026-000123"
    Given a document "notice-0001.pdf" was stored for case "RW-2026-000123" with content_sha256 "SHA-256-TEST-0001"
    When the same document is stored again for case "RW-2026-000123" with the same Idempotency-Key
    Then one document row exists for the document and case
    Then the case was resolved on the contract once and the repeat answered the first result
    Then no second document row, no second field row and no second event is written

  Scenario: AC6 A case outside the reader's scope is refused with no metadata (new, D-RCV-60)
    Given the rwb-case contract mock answers that case "RW-2026-000123" is outside the caller's scope
    When a document of type "COURT_NOTICE" is stored for case "RW-2026-000123"
    Then the store is refused with 403 and MSG-P4-003
    Then the answer carries no document metadata, no case number and no account
    Then no document row is written and no field row is written
```

The six criteria above are new and test only this deliverable: the case binding of the document hub, its refusals and its display read. The legacy criteria of RWB-E1-018 are owned elsewhere: AC1, AC3, AC4, AC7, AC8, AC11, AC12 and AC15 of the legacy story are created, numbered and held by rwb-case (RWB-P3-E1018-APP); the ACE read behind them is rwb-source-data (RWB-P1-E1018-APP); AC14 is the access decision of rwb-access (RWB-P4-E1018-APP); AC10 and the decision record are rwb-decision's (RWB-P7-E1018-APP) and the store's (RWB-P5-E1024-APP). The legacy test cases this story answers are listed in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document is held against exactly one case, and the case is the case ID that rwb-case issued; the binding is mandatory (`document.case_id` is required) and is resolved on the rwb-case contract on every store | REQ-CWC-002; REQ-CHO-004; FSD P5 A2.3.3.2 (`document.case_id`, required); DF-DOC-002 |
| BR2 | The case ID is never derived: not from a file name, not from OCR text, not from an account key, not from a court reference and not from a counter of this service. A value that looks like a case number and does not come from the request or the contract is ignored | REQ-CWC-002; legacy BR11; AC3 |
| BR3 | No case attribute is copied into `rwb_document`: no case number, product group, owner, queue, team, status or stage. The case links to ACE by business key with no foreign key | D-RCV-35 U4; ADR-010; legacy BR11 |
| BR4 | The case number is read through the rwb-case contract at display time and is never stored; other services take it from the case contract, never from a copy | REQ-CWC-002; legacy guardrail "the case number is printed on every outbound document" |
| BR5 | A repeated store of the same document for the same case creates nothing new: one `document` row, and the repeat answers the first result | Legacy AC8; DP-09 (`Idempotency-Key` and inbox) |
| BR6 | A case the contract does not return is refused and nothing is stored; a case outside the caller's scope is refused with no metadata; a role without the right is refused | CTL-09; FSD P5 AC-EXC-P5-001-04 (MSG-P4-002); MSG-P4-003 |
| BR7 | No cross-schema read: `rwb_document` reads no `rwb_case` table and no `v_ace_*` view, and holds no foreign key into another schema; the case arrives through the contract only | DP-01; DP-05; ADR-010 |
| BR8 | The case ID is the key of anything this service publishes for a case: the case documents index is keyed by it, and the store story publishes `rwb.document.DocumentStored.v1` with the case ID as the Kafka key | DP-09; Architecture v5 slide 9 (key caseId); REQ-CWC-016 |

How the rules hold in `rwb-document`:

- BR1 and BR6 are executed by `CaseReferenceClient` and `DocumentCaseBinding`: the contract answer is the only source of a case, and the refusal happens before any write, in the same request.
- BR2 is executed by taking the case ID from the request and the contract answer only; the file name (`document_intake.file_name`, DF-DOC-049) and the OCR text (`document_text.text_content`, DF-DOC-089) are never read as case references.
- BR3 and BR7 are executed by the schema itself: `document` has no case attribute column and no foreign key to `rwb_case`, and this service holds no grant on another schema.
- BR5 is executed by `Idempotency-Key` on the store and by the content hash check of RWB-P5-E1024-APP; this story adds no duplicate row on the repeat.
- BR8 is executed by the index key `(case_id, document_type, created_at)` and by the event key the store story sets.

### 9. State transitions

The case state machine is not this service's. rwb-case owns the case status, its stage and its route (TSD P5 T4: "No case state machine of its own"); this slice reads the case and changes no case state, and a case that closes or moves stage leaves every document row as it is.

| From | Event | Condition | To |
|---|---|---|---|
| None | a store for a case the contract returns | The caller holds Documents C in scope and the document type and file type pass the store checks | `document` row in state COPY_PENDING, `is_active` true, `case_id` set |
| COPY_PENDING | the storage copy succeeds | The container accepts the write (RWB-P5-E1024-APP) | STORED |
| STORED | a new version of the same document is stored | The caller holds Documents U and the reason is recorded | A new row at `doc_version` n+1 with `previous_version_id` set; the earlier row `is_active` false |
| any document state | the case behaviour of rwb-case | A case closes, changes stage, changes route or changes owner | No document row changes: the case is not copied and its state is not held here |

The document states `COPY_PENDING` and `STORED` and the `is_active` flip are the store story's (FSD P5 AC-EXC-P5-001-03, FEAT-DCM-20); this slice changes neither, it only fixes which case ID the row carries at each step.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-document service identity (the rwb-document login, DP-02) | Resolves the case on the contract, writes the document row and its fields, and reads the case documents index; holds no grant on `rwb_case` |
| RW-CASEOWN, case owner; RW-RESTRUCT, restructuring officer; RW-LITOFF, litigation officer; RW-FIELDCOL, field collector; every role with Documents C | Store a document against a case in their scope |
| RW-TEAMMGR, team manager; RW-PHONECOL, phone collector; RW-LEGAL, legal counsel; RW-AUDIT, internal audit; every role with Documents R | Read the documents of a case in their scope, with the case number read from the contract |
| SY-OCR, OCR and extraction pipeline | Carries a document to its case on the intake path (the store itself is RWB-P5-E1024-APP) |
| rwb-case (P3) | Owns the case ID, the case number and the case state; this service reads the case through the contract only |

The authorisation decision is the cached permission decision from rwb-access that the service template's guard already holds; DP-08 is not in this slice's pattern set, so this story adds no guard, no decision endpoint and no access entry of its own. The refusal shapes are 403 with MSG-P4-002 for a role without the right, 403 with MSG-P4-003 for a case outside the caller's scope, and 404 with the not-found message for a case the contract does not return. The per-service login name is Not specified in the source documents (GAP-1038; ASM-1986); the story names it "the rwb-document login (DP-02)" until the DB story fixes it. The role codes above are rows of the role model in `rwb_access` (TSD P5 T6.1) and are not fixed in code.

### 11. Data

| BR Field ID | Table in rwb_document | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Write |
| DF-DOC-002 | document | case_id (the one case reference of the document) | Write; resolved on the contract first |
| DF-DOC-011 | document | doc_version | Write (1 on the first store, n+1 on a new version) |
| DF-DOC-025 | document | previous_version_id | Write (empty on version 1, the earlier document on a new version) |
| DF-DOC-026 | document | content_sha256 | Write (also the duplicate check of the repeated store) |
| (standard column, TSD P5 T3.0) | document | is_active | Write (true on store; false on the earlier row when a new version is stored) |
| DF-DOC-012 | document_field | id | Write |
| DF-DOC-013 | document_field | document_id | Write |
| DF-DOC-014 | document_field | field_name | Write |
| DF-DOC-015 | document_field | field_value | Write |
| DF-DOC-016 | document_field | confidence | Write |
| DF-DOC-017 | document_field | confirmed_by | Write (empty until a person confirms the field) |
| DF-CAS-001 and DF-CAS-002 | case, through the rwb-case contract of RWB-P3-E1018-CON | id, case_no | Read only, on each request; never written |
| (index) | document | key (case_id, document_type, created_at) | Write through the index of RWB-P5-E1024-APP |

Field IDs are those in the Technical Specification P5 Document hub v2 T3.1 and the Logical Data Model and Data Dictionary v8. `document.case_id` is the only case reference in the schema: there is no case number, product group, owner, queue, team, status or stage column, and no foreign key to `rwb_case` (BR3, BR7). No ACE row and no case row is copied into `rwb_document`; the case number reaches a screen from the contract at display time. The request and response field names of the case read are Not specified in the source documents (GAP-1038; ASM-1986).

### 12. Contract

#### 12.1 REST operations provided

None new. The operations this story sits behind are declared by the store and the screen stories of the same service: the upload `POST /cases/{caseId}/documents`, the case documents read `GET /cases/{caseId}/documents` and the document read `GET /documents/{documentId}`, all on base `/api/recovery/document/v1` with owner rwb-document (P5) and the access letters Documents C and R (TSD P5 T-A.1, API-P5-001 to API-P5-004). This slice adds no path, no query parameter and no response field; it fixes what happens behind them for the case reference, and it declares no OpenAPI document of its own.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | rwb-case (P3), under RWB-P3-E1018-CON | The case reference of a store: confirms the case exists, is in scope and gives the case number for display | One hop, 2 s (DP-11); the answer is cached for the request only |

The contract is consumed as the published OpenAPI 3.1 document plus its fake. This slice calls no other service: the document types and sources arrive through the reference-data contract of DP-07 in the store story, and no ACE view is read (DP-05).

#### 12.3 Events published

None. This slice publishes no event of its own. The store story publishes `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` with the case ID as the key, and `DocumentFieldsExtracted` when extraction completes; the case ID in that payload is the binding this story fixes (DP-09, DP-14).

#### 12.4 Events consumed

None. This slice consumes no topic: the case reference is resolved on the contract per request, and a case that changes state needs no event here because no case state is held.

#### 12.5 Workflows and activities

None. The binding is a synchronous step inside the store request; this story starts no workflow and runs no activity. `DocumentIntakeWorkflow` (OCR, classify, extract) is the store story's, and the classification child in rwb-agent is called from there, not here.

#### 12.6 Schedules

None. The document intake Schedule every 15 minutes (FSD P5 AC-BG-P5-001-01) and the retention Schedule (JOB-17) belong to RWB-P5-E1024-APP and its schedule story; this slice holds no Schedule (DP-10).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| `document` | P5 (rwb_document) | Metadata of a document, including `case_id`, `doc_version`, `previous_version_id`, `content_sha256` and `is_active` |
| `document_field` | P5 (rwb_document) | Fields extracted from a document, written against the document ID |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_document` | Outbox, inbox and idempotency objects (DP-09); this slice writes the idempotency row, the store story writes the events |

No `rwb_case` table is read and no `v_ace_*` view is read (DP-01, DP-05). `rwb_document` holds no foreign key into another schema; the case is reached through the contract, and the case number is never stored.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case contract fake (RWB-P3-E1018-CON) | The P3 case read | A found case `RW-2026-000123` with case number `RW-2026-000123` and borrower `P-0101`; a not-found answer for `RW-2026-000122` and `RW-2026-000999`; an out-of-scope answer for `RW-2026-000123`; a slow answer past the 2 s budget |
| store fixture (RWB-P5-E1024-APP) | The document store and its index | A document row written with `case_id`, `doc_version` 1 and `content_sha256`, and the case documents read by case ID |

The field names of the case answer are stubbed from the published fixture of RWB-P3-E1018-CON; their list is Not specified in the source documents (GAP-1038; ASM-1986).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | `GET /cases/{caseId}` on the rwb-case contract, one hop within 2 s (DP-11) |
| Kafka | 0 published, 0 consumed | This slice publishes nothing and consumes nothing; the store story publishes `rwb.document.DocumentStored.v1` with the case ID as the key |
| Temporal | None | No workflow and no activity in this story |
| File | None | This story reads and writes no file; the file and the containers are the store story's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `casebinding`, Java package `th.co.scb.ace.workbench.recovery.document.casebinding`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseReferenceClient | REST client | Calls `GET /cases/{caseId}` on the rwb-case contract, one hop and 2 s, maps 404 and scope refusal to the two refusals, and returns the case ID and case number |
| DocumentCaseBinding | Service | Takes the case ID from the contract answer, refuses an unconfirmed or out-of-scope case before any write, and passes the case ID to the repository; it never derives a case from a file name or OCR text |
| DocumentRepository | Repository | Writes `document` and `document_field` in `rwb_document` with `case_id`, `doc_version`, `previous_version_id`, `content_sha256` and `is_active`; reads no other schema |
| DocumentIndexReader | Service | Reads the case documents index by `case_id` for SCR-30 and SCR-03, and gets the case number from the contract at display time |

**Database and migrations**

- Writes `document` (`case_id` not null) and `document_field`; no case attribute column and no foreign key to `rwb_case`.
- Index `(case_id, document_type, created_at)` on `document`, which serves the case documents read; the same index carries the case binding test of AC1 and AC5.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V1018_1__case_binding.sql` makes `document.case_id` not null, adds the index `(case_id, document_type, created_at)` and adds no column for case data. The tables themselves arrive with the `rwb_document` baseline and the store migration of RWB-P5-E1024-APP.
- No row is seeded by this story; the document types and sources are loaded by RWB-P5-E1025-APP.

**Configuration and reference data**

- No business value is configured here: the case ID, the case number and every case attribute belong to rwb-case, and the document types, sources and retention classes are lists loaded elsewhere.
- Two settings only: the rwb-case contract base (the service address of `GET /cases/{caseId}`) and the rwb-document login (DP-02). The login name is Not specified in the source documents (GAP-1038; ASM-1986).
- The 2 s timeout and the one-hop rule are the platform values of DP-11 and are set in the client configuration, not in code branches.

**Build steps**

1. `CaseReferenceClient` against the contract fake, with the found, not-found, out-of-scope and slow answers; tests for AC1, AC2 and AC6.
2. `DocumentCaseBinding` with the refusal before any write and the no-derivation rule; tests for AC2, AC3 and AC6.
3. `DocumentRepository` write of `document.case_id`, `doc_version`, `previous_version_id`, `content_sha256` and `is_active`; tests for AC1 and AC4.
4. `DocumentIndexReader` with the case documents read by case ID and the case number taken from the contract; tests for AC1 and AC4.
5. The repeated store path with `Idempotency-Key` and the content hash; test for AC5.
6. Contract-fake run of every cross-service answer in isolation, so the story builds before rwb-case is live, and a schema assertion that `rwb_document` holds no case attribute column.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
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

This is a secondary slice with no owned legacy acceptance criteria of a build story: it adds no new build dependency of its own (metadata "Depends on (build)" = None) and builds against the `rwb_document` baseline and the RWB-P3-E1018-CON fake, with the platform contract libraries already delivered by the service template. Read one by one:

- DP-01, DP-02 and DP-13 are the target shape itself: the schema `rwb_document`, the rwb-document login and the base `/api/recovery/document/v1` replace the shared recovery schema, the shared login and the monolith base, with no new dependency.
- DP-03 applies as a statement that the decision record of a store belongs to RWB-P5-E1024-APP; the case binding writes no record of its own, so no new record is added by this slice.
- DP-04 applies as a prohibition: the document hub evaluates no Drools rule. The transfer rule and the entry and exclusion rules stay in rwb-case, and this slice calls no rule package and holds no KieBase.
- DP-05 applies as a prohibition: no ACE view is read here. The case facts a reader sees arrive through the rwb-case contract, and `v_ace_*` stays with rwb-source-data.
- DP-07 applies as a statement that the document type and source lists are read through the reference-data contract by the store story; no list value is written in this slice's code.
- DP-09 applies to the key and the envelope the store story uses: the case ID is the Kafka key and the payload carries IDs and facts only. This slice publishes nothing, and its inbound behaviour is a synchronous contract read.
- DP-10 applies as a statement: no Schedule in this slice. The intake Schedule and the retention Schedule stay with RWB-P5-E1024-APP.
- DP-11 is the one live pattern here: the in-process case read of the monolith becomes one REST hop to the owner with a 2 s timeout and the published fake.
- DP-14 applies as a statement: no topic name is typed in code, the naming library supplies `rwb.document.events.v1`, and this slice publishes nothing.
- DP-15 is the per-service migration `V1018_1__case_binding.sql` in `rwb_document`, and DP-19 is the gateway-bff composite route behind SCR-30 and SCR-03.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P3-E1018-CON stay green, and a SIT week shows every document row carrying a case ID the contract returns, no case attribute column in `rwb_document`, no document written for a case the contract does not return, one row on a repeated store, and the case number on SCR-30 and SCR-03 read from the contract at display.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's role holds no Documents C or Documents R for the action | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case exists but sits outside the caller's scope | This case is not in your scope. |
| MSG-GEN-001 | The request names no case reference | Enter {field}. |
| The not-found message, whose ID is Not specified in the source documents (GAP-1038; ASM-1986) | The rwb-case contract returns no case for the case ID in the request, or does not answer inside the 2 s budget | The case is not available. |

The 404 not-found answer carries the message ID of the rwb-case contract's own not-found answer, which the contract story publishes; until it is fixed the story uses the placeholder above. For MSG-GEN-001 the {field} value is "a case reference". For MSG-P4-002 the {action} value names the action the caller tried — "store this document" or "read the documents of this case" — and never a case fact. Every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The store path answers 400 for a missing case reference, 403 for a role without the right or a case out of scope, 404 for a case the contract does not return, and 503 when the contract cannot be reached.

### 15. Screens and states

SCR-30 Case documents shows the documents of one case, read by case ID from `rwb_document`, with the document type, the stored date and the version, and the case number beside them read from the rwb-case contract at display time. SCR-03 Case record shows the same documents on its Documents tab, again by case ID, and the case header from rwb-case. The full screen, its states and its filters are RWB-P5-E1026-APP: the loading state, the empty state ("No documents match this search."), the search by type and date, the checklist placeholder and the upload dialog belong there, and this story fixes only that the documents are listed by case ID and the case number is not read from a copy.

Both screens are served by the gateway-bff composite route (DP-19), which calls rwb-document for the documents and rwb-case for the case header, one hop each, and merges the answers. The screen fields, the field-level masking of the composite route and the route specification are Not specified in the source documents (GAP-1038; ASM-1986). This slice shows no case attribute from `rwb_document`, because none is stored; the only states it makes visible are the case number the contract returns and the refusal when the contract returns no case.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-02 | AC2, BR6: a document for a case the contract does not return is refused and nothing is stored; the exclusion itself is rwb-case's | End to end | `v_ace_account` A-5002 at 92 days past due with `tdr_flag` true, so no case exists; package EXCLUSION "EXCL-2026.11"; reason "ACTIVE_PLAN" |
| TC-E1-018-01 | AC1, BR1, BR2, BR3, BR4: one case ID resolved on the contract and written to the document, no case attribute copied, the case number read at display | End to end | Case `RW-2026-000123`, borrower `P-0101`, account `A-5001`, last number issued `RW-2026-000122`; document `notice-0001.pdf` of type COURT_NOTICE |
| TC-E1-018-03 | AC1, BR3: one case for the customer and product, so the document binds to that one case ID and to no other | End to end | Borrower `P-0102` with hire purchase accounts `A-5003` at 300,000.00 and `A-5004` at 112,350.00 |
| TC-E1-018-04 | AC4, BR4: the document never renumbers a case; a closed case keeps its number on the document and the number is read from the contract | End to end | Case `RW-2026-000123` closed on 2026-12-15; the next case is `RW-2026-000124` |
| TC-E1-018-05 | AC1, BR3: a case status value is not held on the document, so a new status changes no document row; the status list is rwb-case's | End to end | New status value `WAITING_COURT` in LOV-CASE-STATUS, valid from 2027-01-01 |
| TC-E1-018-06 | AC2, BR6: an excluded account has no case, so a document presented for it is refused; the exclusion rule itself is rwb-case's | End to end | Account `A-5005` with `dispute_open` true in `account_ext`; EXCLUSION rule "EXCL-006"; reason "OPEN_DISPUTE" |
| TC-E1-018-07 | AC1, AC2, BR1: the account at 90 days past due has a case and its document binds; the account at 89 has none and its document is refused | End to end | Accounts `A-5006` at 89 days past due and `A-5007` at 90 days past due |
| TC-E1-018-08 | AC5, BR5: a repeated store resolves the case once and writes one document row | End to end | Case `RW-2026-000125` for account `A-5008` on 2026-12-01; the same document stored twice |
| TC-E1-018-09 | AC2, BR6: no case exists before the ALS batch completes, so no document can bind; the batch gate itself is rwb-source-data's | End to end | ALS batch for 2026-12-02 at status "RUNNING" at the 09:00 cut-off; MSG-P1-001 on the job monitor for 2026-12-01 |
| TC-E1-018-10 | BR3, BR6: the decision record of a store is the store story's; this slice writes no record and stores nothing when the case is unconfirmed | End to end | Account `A-5009`; decision log store unavailable; MSG-P7-003 on the job record |
| TC-E1-018-11 | AC1, AC3, BR2: the document never carries a number from a counter of its own and takes no case ID from a number in the file; numbering and its range are rwb-case's | End to end | Last number issued `RW-2026-000999`; account `A-5010` qualifying on 2026-12-30; MSG-P3-025 for year 2026 |
| TC-E1-018-12 | AC1, BR1: two products give two cases, so a document binds to the case of its own product only | End to end | Borrower `P-0103` with mortgage account `A-5011` and hire purchase account `A-5012` at 91 days past due |
| TC-E1-018-13 | AC6, BR6: a role without the right, and a case outside the scope, are refused with no metadata | Component | Role `RW-REFADM` reads and stores on case `RW-2026-000123` and is refused with MSG-P4-002; a case outside the caller's scope is refused with MSG-P4-003 |
| TC-E1-018-14 | BR6, BR7: a failure of the store or of the case read leaves nothing behind; the decision record path is the store story's | NFR | Decision log write forced to fail for the whole run; the case read forced to time out; no document row and no event |
| TC-E1-018-15 | AC1, AC2, BR2: a case link whose key has no view row is listed, never invented, and no document is bound to a case the contract does not return | End to end | Case `RW-2026-000126` linking `A-5013` and `P-0105` with no view row for 2026-12-01; REC-05 lists both keys |
| TC-E1-018-16 | AC2, BR6: no EXCLUSION version in force means no case is created, so no document binds; the package check is rwb-case's | End to end | No EXCLUSION version in force on 2026-12-01; MSG-P3-027 for package "EXCLUSION" |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. Every legacy test case of RWB-E1-018 is listed above with the slice of the behaviour this story answers; the -ITG copies of these cases are not here — they belong to the integration slice RWB-ITG-E1018-ITG, which proves the same values across rwb-case, rwb-source-data, rwb-access and rwb-document end to end.

### 17. Guardrails

- No business value in code: the case ID, the case number and every case attribute are values of rwb-case, read through the contract; the document types, sources and retention classes are lists read by the store story through the reference-data contract. No case form, prefix, sequence or status value appears in this service's Java.
- No personal data in events, workflow inputs, logs or tests. This story writes document IDs, case IDs, field names and hashes only; no name, address, identity number or account number is logged. Test data uses synthetic keys (`RW-2026-000123`, `A-5001`, `P-0101`, `notice-0001.pdf`).
- No cross-schema read (DP-01): `rwb_document` reads no `rwb_case` table and no table of another service.
- ACE data only through the owner's contract or `v_ace_*` views, and this service reads no view (DP-05): the account and customer facts behind a case stay with rwb-source-data, and this service reads none of them.
- The case is reached only through the rwb-case contract of RWB-P3-E1018-CON: one hop, 2 s, and an unconfirmed case is never a partial allow.
- The case ID is the only case reference on a document, and nothing is derived: not from the file name, not from the OCR text, not from an account key, not from a court reference and not from a counter of this service.
- A document row is never re-pointed at another case: a new version carries the same `case_id`, and only `doc_version`, `previous_version_id` and `is_active` change.
- The binding is written in the same transaction as the document row, so a refused or failed store leaves no `document`, no `document_field` and no event behind.
- The Kafka key of anything the store story publishes for a case is the case ID (DP-09), and no topic name is typed in code (DP-14).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-04 | 6.1 Take over the case at 90 days past due | R-UNI-16 | TC-E1-018-01, TC-E1-018-07, TC-E1-018-09 |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, issued once, never reused, printed on every document | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-01 | 6.1 | CTL-09; BR1 to BR4 | TC-E1-018-01, TC-E1-018-04, TC-E1-018-11, TC-E1-018-13, TC-E1-018-15 |
| REQ-CWC-003 | One case per customer and product, linked by business key with no foreign key | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-02 | 6.1 | R-UNI-17; D-RCV-35 U4; ADR-010 | TC-E1-018-03, TC-E1-018-08, TC-E1-018-12 |
| REQ-CWC-004 | Exclusion rules held as data and applied at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-05 | 6.1 | None | TC-E1-018-02, TC-E1-018-06, TC-E1-018-16 |
| REQ-CWC-005 | One case state at a time, from the state model and the lists | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-03 | 6.1 | None | TC-E1-018-05 |
| REQ-CWC-016 | Every workflow event logged with its rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-21 | 6.1 | R-UNI-39 | TC-E1-018-10, TC-E1-018-14 |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-01, FEAT-CWC-02, FEAT-CWC-03, FEAT-CWC-04, FEAT-CWC-05, FEAT-CWC-20, FEAT-CWC-21 | 6.1 | None | TC-E1-018-01, TC-E1-018-07 |

The features FEAT-CWC-20 (the workflow admin API) and FEAT-CWC-21 (log every workflow event) are carried by the case service; this slice answers them only for the case reference a document carries and for the key of what the document hub publishes. The -ITG copies of the test cases are carried by RWB-ITG-E1018-ITG.

| Legacy reference | Where it is kept |
|---|---|
| Legacy key RWB-E1-018; story RWB-P5-E1018-APP; contract RWB-P3-E1018-CON; baseline `rwb_document` | Metadata; sections 1, 3, 12 |
| Case number form RW-YYYY-NNNNNN, issued once and never reused | Sections 2, 8 (BR1, BR2, BR4), 11 |
| BR11 of the legacy story (business key, no foreign key); D-RCV-35 U4; ADR-010 | Sections 8, 11, 12.7, 17 |
| Synthetic values: case `RW-2026-000123`, last number `RW-2026-000122`, accounts `A-5001`, `A-5002`, person_key `P-0101`, document `notice-0001.pdf`, type COURT_NOTICE | Sections 3, 7, 16 |
| MSG-P4-002, MSG-P4-003, MSG-GEN-001, and the not-found message | Section 14, exception paths |
| Field IDs DF-DOC-001, DF-DOC-002, DF-DOC-011, DF-DOC-012 to DF-DOC-017, DF-DOC-025, DF-DOC-026; DF-CAS-001 and DF-CAS-002 | Section 11 |
| Document states COPY_PENDING and STORED, and the `is_active` flip | Section 9 |
| Legacy test cases TC-E1-018-01 to TC-E1-018-16 | Section 16 |
| The other slices of RWB-E1-018 (rwb-case, rwb-source-data, rwb-access, rwb-decision, the store and the screen) | Sections 2, 19 |

### 19. Out of scope

- Case creation, the entry and exclusion rules, the numbering sequence, the yearly range and the case state model: rwb-case (RWB-P3-E1018-APP).
- The ACE view read behind the entry and exclusion decisions: rwb-source-data (RWB-P1-E1018-APP).
- The access matrix, the scope decision and the access log: rwb-access (RWB-P4-E1018-APP); this service consumes the cached decision from the template.
- The decision record of a case creation and the central ledger: rwb-decision (RWB-P7-E1018-APP).
- The document store, its versions, the write-once containers, the OCR and classification pipeline, the retention Schedule and the store's own decision record: RWB-P5-E1024-APP.
- The document types, their fields, the sign-offs and the lists: RWB-P5-E1025-APP.
- SCR-30 Case documents and SCR-03 Case record as screens, with their states, filters, checklist placeholder and upload dialog: RWB-P5-E1026-APP.
- The end-to-end proof of these values across rwb-case, rwb-source-data, rwb-access and rwb-document: RWB-ITG-E1018-ITG.
- The contract document, its fakes and its versioning: RWB-P3-E1018-CON; the `rwb_document` schema baseline, the login, the topic and queue provisioning, the chart, the dashboards and the runbook of this service.

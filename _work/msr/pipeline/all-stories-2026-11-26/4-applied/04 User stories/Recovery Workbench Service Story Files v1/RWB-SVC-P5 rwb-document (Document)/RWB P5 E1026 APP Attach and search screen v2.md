# RWB-P5-E1026-APP Attach and search screen

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-026 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1025-APP, RWB-P5-E1024-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON, RWB-P5-E1025-APP, RWB-P5-E1024-APP, RWB-P5-E1041-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1030-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-001, FR-P5-002, FR-P5-007, FR-P5-008, FR-P5-009, FR-P5-012, FR-P5-013, FR-P5-014, FR-P5-022, FR-P5-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: moved RWB-E1-026 into rwb-document as the SCR-30 attach and search capability on the gateway-bff composite route, rebased on the service schema, the parameter and reference-data contracts and the scan contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **to upload, see and search the documents of a case from the case record view**, so that **the case file is complete and I find a document by type and date without leaving the case**.

Inside `rwb-document` this is the SCR-30 attach and search capability:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- SCR-30 Case documents lives in the case record view. The route is published by gateway-bff through the composite route of DP-19 (H RWB-PLT-N001-CON), which calls `rwb-document` one hop for `GET /cases/{caseId}/documents`, `POST /cases/{caseId}/documents` and `GET /cases/{caseId}/document-checklist` and merges the answer into the screen model. The screen fields of the tab are this service's.
- Behind the screen: the store, the versions and the detail panel are RWB-P5-E1024-APP; the type table and its fields are RWB-P5-E1025-APP; the malware scan is the contract of RWB-P5-E1041-CON (H); the parameters `INTAKE_MAX_FILE_MB` and `INTAKE_ALLOWED_TYPES` arrive through the parameters contract of DP-06 and the type and LOV list through the reference-data contract of DP-07.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1033; ASM-1981); this story uses the phrase "the rwb-document login (DP-02)" and never the shared monolith login.

The legacy behaviour is unchanged: the same upload, list, search and checklist intent; the same rules, messages, acceptance criteria and test cases with their values; the same authority letters; the same fields.

### 2. Business rationale

Case owners hold documents in shared drives and email today, so the case file is never complete in one place (FSD P5 A1.3). This story puts the case documents screen SCR-30 on the case record view: upload with a type, a list of every document on the case, a search by type and date, and a checklist placeholder showing which of the six agreed types are present. It meets REQ-DCM-008 (search by case, type and date from the case record view) and REQ-DCM-001 (every document stored against its case with type, date and source). The measure is fields extracted without review (FSD P5 A2.4.1), which needs documents on the case first.

The target keeps one tab and one hop. gateway-bff publishes the route (DP-19) and asks `rwb-document` directly, in parallel, only for what is on screen (Architecture v5 slide 10: the documents tab loads on click, from its owner, one hop). The tab is therefore served by three operations of this service and by nothing else of its own; the store, the versions and the detail panel belong to RWB-P5-E1024-APP, the type table and the checklist types to RWB-P5-E1025-APP, the scan to RWB-P5-E1041-CON, and the parameters and the LOV lists to the contracts of rwb-case behind DP-06 and DP-07. No table of another service is read and no new table is added: the list reads `document` and `document_type` in `rwb_document`.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1027-CON | The decision-record library and the `rwb.decision-record.v1` topic (DP-03), behind the store call this tab makes |
| RWB-PLT-E1042-CON | The parameters client library, so `INTAKE_MAX_FILE_MB` and `INTAKE_ALLOWED_TYPES` are read and never typed in code (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library, so the type list and its labels arrive as versioned data (DP-07) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes SCR-30 inside the case record view (DP-19) |
| RWB-P5-E1025-APP | Document type table version "DOCTYPE-2026.11" in force, with the six agreed types, their labels and their fields |
| RWB-P5-E1024-APP | The store, the versions and the detail panel: the upload writes through its published interface and the detail panel it owns opens from the list |
| RWB-P5-E1041-CON | The malware scan contract called before the store, with its fake for the build |
| RWB-P3-E1042-CON | The parameters contract of rwb-case, read through the client library of DP-06 |
| RWB-P3-E1043-CON | The reference-data contract of rwb-case, read through the client library of DP-07 |
| RWB-P3-E1030-CON | The queue-measure and product-parameter contract that the case record view header uses; it composes above this tab and this story calls none of it |

Business preconditions carried from RWB-E1-026:

- Parameters INTAKE_MAX_FILE_MB = 25 (assumed, DL11) and INTAKE_ALLOWED_TYPES = PDF, JPG, PNG are in force, read through the parameters contract of DP-06.
- The user holds a role with Documents C to upload and Documents R to list, with the case in scope; the RBAC matrix of TSD P5 T6.1 gives the letters.
- The case read for the scope test is made through the rwb-case contract, one hop; its request and response field names are Not specified in the source documents (GAP-1033; ASM-1981).
- The scan operation of RWB-P5-E1041-CON is published and its fake answers "CLEAN" and "INFECTED"; its path is Not specified in the source documents (GAP-1034; ASM-1982).
- The route that gateway-bff publishes for SCR-30, and the fields it merges, are Not specified in the source documents (GAP-1035; ASM-1983).
- Feature flag `rwb.document.casedocs` is on. Off: the Documents tab is hidden and the three operations return 404.
- The login is the rwb-document login (DP-02); its name is Not specified in the source documents (GAP-1033; ASM-1981).

### 4. Flow

1. Case owner: opens case RW-2026-000123 on the case record view (SCR-03) and the Documents tab (SCR-30, state Loading then list); gateway-bff serves the tab from its composite route and calls this service.
2. Front end: calls GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist through gateway-bff, one hop; the service answers the page and the checklist placeholder, and the tab shows both.
3. Case owner: chooses Upload, picks a file and a document type from the list, and submits; the front end checks the size against INTAKE_MAX_FILE_MB read through DP-06 before sending and sends an Idempotency-Key.
4. CaseDocumentUploadService: puts the file in the intake container, calls the malware scan of RWB-P5-E1041-CON and, if the answer is "CLEAN", calls the store of RWB-P5-E1024-APP with source UPLOAD.
5. The store (RWB-P5-E1024-APP): writes the decision record through the library of DP-03, the `document` row and `rwb.document.DocumentStored.v1`, then copies the file; the tab holds no record of its own.
6. Front end: on 201 refreshes the list through gateway-bff; the new document shows within 5 seconds of submit.
7. Case owner: enters a type and a date range in the search bar; GET /cases/{caseId}/documents with type, dateFrom and dateTo returns only the matching documents, newest first, 20 per page.
8. Case owner: opens a document; the DocumentDetailPanel of RWB-P5-E1024-APP shows it, read through the same service.

The store call is the only write path; a failure between the scan and the store leaves the quarantined or clean file in the intake container and no `document` row (section 5, X2 and X11).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Upload with no document type | Refused with 422; nothing stored | MSG-GEN-001 | AC4 |
| X2 | The file fails the malware scan | Refused with 422; file held in quarantine; nothing stored | MSG-P5-016 | AC5 |
| X3 | The file type is not allowed | Refused with 415; nothing stored | MSG-P5-001 | AC6 |
| X4 | The same file and type is already on the case | The existing document is returned and highlighted; no second document | MSG-P5-024 | AC7 |
| X5 | The submit is sent twice with the same Idempotency-Key | One document; the second call returns the first result | None | AC8 |
| X6 | Date from is after date to | Search not run | MSG-GEN-003 | AC9 |
| X7 | Search matches nothing | Empty state with the sentence and the clear filter action | None | AC10 |
| X8 | Case is outside the user's scope | Refused with 403 | MSG-P4-003 | AC11 |
| X9 | Role without Documents C uploads | Refused with 403; Upload button hidden | MSG-P4-002 | TC-E1-026-12 (Access) |
| X10 | The decision record write fails during the store | Nothing stored; the dialog shows the message | MSG-P7-003 | TC-E1-026-13 (Principle 5) |
| X11 | The scan contract of RWB-P5-E1041-CON does not answer inside the one-hop 2 s budget, or answers with an error | The upload is refused with 503 and nothing is stored; the file stays in the intake container and no `document` row is written; the store is never called on an unknown scan answer | MSG-GEN-006 naming "Virus scan" | Section 13, build step 2 |

For X11 the operation path of the scan in RWB-P5-E1041-CON is Not specified in the source documents (GAP-1034; ASM-1982), and the text of MSG-GEN-006 for this capability is Not specified in the source documents (GAP-1033; ASM-1981); the ID and the 503 shape follow FSD P5 AC-EXC-P5-001-03.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the store (RWB-P5-E1024-APP), the types (RWB-P5-E1025-APP) and the scan contract (RWB-P5-E1041-CON), all earlier in the lane or in the same wave; no other screen depends on it |
| Negotiable | Page size, sort order and the placeholder layout can change; the endpoints stay |
| Valuable | Case owners attach and find documents on the case instead of in shared drives |
| Estimable | Three endpoints added or completed, one service, one tab with three parts, no new table |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Attach and search screen

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given user "TEST-CO-01" holds RW-CASEOWN and owns case "RW-2026-000123"
    Given the rwb-case contract mock returns case "RW-2026-000123" owned by "TEST-CO-01" in team "MTG-BKK-LIT"
    Given the rwb-case reference-data contract mock returns document type table version "DOCTYPE-2026.11" with the six agreed types
    Given the rwb-case parameters contract mock returns INTAKE_MAX_FILE_MB 25 and INTAKE_ALLOWED_TYPES "PDF, JPG, PNG"
    Given the rwb-document store mock returns the stored document for case "RW-2026-000123"
    Given the rwb-document scan contract mock returns "CLEAN" for the uploaded file

  Scenario: AC1 Upload (legacy RWB-E1-026 AC1)
    Given "TEST-CO-01" is on the Documents tab of case "RW-2026-000123"
    When "TEST-CO-01" uploads "court-notice-0007.pdf" of 2 MB with type "COURT_NOTICE"
    Then the response is 201 with source "UPLOAD" and doc_version 1
    Then the document shows at the top of the case document list within 5 seconds of submit
    Then GET /cases/{caseId}/documents with type "COURT_NOTICE" returns it

  Scenario: AC2 Search (legacy RWB-E1-026 AC2)
    Given case "RW-2026-000123" holds 50 documents of which 12 are "COURT_NOTICE"
    Given 4 of the court notices were stored between 1 October 2026 and 31 October 2026
    When "TEST-CO-01" searches type "COURT_NOTICE" from 1 October 2026 to 31 October 2026
    Then exactly the 4 court notices stored in October show, newest first
    Then the result count reads 4

  Scenario: AC3 Checklist placeholder (legacy RWB-E1-026 AC3)
    Given case "RW-2026-000123" holds 12 court notices and 1 appraisal report and no other agreed type
    When the Documents tab opens
    Then the checklist placeholder lists the six agreed types
    Then COURT_NOTICE shows present with 12, APPRAISAL_REPORT shows present with 1
    Then DEMAND_LETTER, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE show not present

  Scenario: AC4 Upload without a type (legacy RWB-E1-026 AC4)
    Given "TEST-CO-01" picks "scan-0009.pdf" and no document type
    When "TEST-CO-01" submits the upload
    Then the response is 422 with MSG-GEN-001 naming "Document type"
    Then the system stores no document

  Scenario: AC5 Upload that fails the malware scan (legacy RWB-E1-026 AC5)
    Given a test file "eicar-0001.pdf" holding the EICAR test signature
    Given the rwb-document scan contract mock returns "INFECTED" for the uploaded file
    When "TEST-CO-01" uploads it with type "COURT_NOTICE"
    Then the response is 422 with MSG-P5-016
    Then the file is in the quarantine container and no document row exists

  Scenario: AC6 File type not allowed (legacy RWB-E1-026 AC6)
    Given a file "minutes-0002.xlsx" with spreadsheet content
    When "TEST-CO-01" uploads it with type "SETTLEMENT_AGREEMENT"
    Then the response is 415 with MSG-P5-001 shown in the upload dialog
    Then the system stores no document

  Scenario: AC7 The same file uploaded again (legacy RWB-E1-026 AC7)
    Given "court-notice-0007.pdf" is stored on case "RW-2026-000123" as "COURT_NOTICE"
    When "TEST-CO-01" uploads the same file with the same type
    Then the response is 200 with the existing document ID and MSG-P5-024
    Then the case still holds one copy of that court notice

  Scenario: AC8 Double submit (legacy RWB-E1-026 AC8)
    Given "TEST-CO-01" submits "appraisal-0003.pdf" with Idempotency-Key "TEST-KEY-0001"
    When the same request with Idempotency-Key "TEST-KEY-0001" arrives a second time within 1 second
    Then both responses carry the same document ID
    Then one document row and one decision log entry exist for it

  Scenario: AC9 Date range in the wrong order (legacy RWB-E1-026 AC9)
    Given "TEST-CO-01" is on the Documents tab
    When "TEST-CO-01" searches from 31 October 2026 to 1 October 2026
    Then the search is not run and MSG-GEN-003 shows next to the date fields

  Scenario: AC10 No document matches (legacy RWB-E1-026 AC10)
    Given case "RW-2026-000123" holds no "TITLE_DEED"
    When "TEST-CO-01" searches type "TITLE_DEED"
    Then the list shows the empty state "No documents match this search." with the action "Clear the search"

  Scenario: AC11 Case outside the scope (legacy RWB-E1-026 AC11)
    Given user "TEST-CO-02" holds RW-CASEOWN with scope OWN and does not own case "RW-2026-000123"
    Given the rwb-case contract mock returns case "RW-2026-000123" owned by "TEST-CO-01" in team "MTG-BKK-LIT"
    When "TEST-CO-02" opens the Documents tab of that case
    Then GET /cases/{caseId}/documents returns 403 with MSG-P4-003
    Then the system shows no document name
```

The Background and the three extra Givens of this story mock the rwb-case contract, the rwb-document store and the rwb-document scan contract; every value of the legacy criteria is kept unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A user upload carries a document type from the type table in force and source UPLOAD | REQ-DCM-001; LOV-DOC-SOURCE |
| BR2 | Every upload is scanned for malware before it is stored | REQ-DCM-010; FEAT-DCM-18 |
| BR3 | The list and the search show only cases in the user's scope | CTL-09 |
| BR4 | The date filter applies to the stored date of the document in Epic 1 | FSD P5 A2.5; REQ-DCM-008 |
| BR5 | The checklist placeholder lists the types of the type table in force; the required items per case type come in RWB-P5-E1040-APP | REQ-DCM-011; FEAT-DCM-16 |
| BR6 | A repeated upload with the same file, type and case returns the existing document | R-UNI-40 |
| BR7 | A store that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |

Target-service statements that make the rules hold in `rwb-document`:

- BR2 is executed in this order: the file goes to the intake container, the scan of RWB-P5-E1041-CON answers, and only a "CLEAN" answer reaches the store of RWB-P5-E1024-APP. An unknown answer stores nothing (section 5, X11).
- BR3 is executed by the scope test on the case read taken through the rwb-case contract, and by the cached permission decision the service holds from rwb-access; neither the list nor the search runs a query without it.
- BR5 is executed by reading the type table version in force through DP-07 and the type rows of `document_type` in `rwb_document`; the checklist returns required = false for every item, missingCount 0 and complete null until RWB-P5-E1040-APP sets the required items.
- BR1 and BR4 are data and property: the type list, the size limit, the file types and the page size are parameters or reference rows, never code (BR-P5-004).
- BR7 is held by the store call, which writes the decision record through the library of DP-03 in the same transaction as the `document` row; this story adds no direct decision-log write of its own.
- DP-01 keeps the tab on `rwb_document` only; DP-19 keeps the browser one hop from the owner and puts the merge in gateway-bff.

### 9. State transitions

None for the case. This story does not change a case status. A successful upload creates a document record in state COPY_PENDING, then STORED (RWB-P5-E1024-APP), and the tab shows the row from STORED onward with its version.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Roles with Documents C (RW-CASEOWN, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT) | Upload inside their scope |
| Roles with Documents R (for example RW-TEAMMGR, RW-PHONECOL, RW-AUDIT) | List, search and open documents inside their scope |
| Partner roles PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION | No access in Epic 1; partners reach the Workbench only through the external gateway (DL03) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry for each upload |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope, masking and DoA in `rwb_access`) and is consumed as the cached permission decision the service holds; the refusal shapes are 403 with MSG-P4-002 and MSG-P4-003, as in the legacy endpoint. The guard itself is RWB-P5-E1019-APP (DP-08); this story inherits it and adds no guard.

The service identity that calls the store, the scan and the rwb-case reads is the rwb-document login (DP-02); its name is Not specified in the source documents (GAP-1033; ASM-1981).

### 11. Data

| BR Field ID | Table in rwb_document | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` (read only through the rwb-case contract) | id | Read, through the contract; no column of `rwb_case` is read |
| DF-DOC-001 to DF-DOC-011 | `document` | all fields | Read here; written by the store (RWB-P5-E1024-APP) |
| Standard column | `document` | created_at | Read, as the stored date |
| DF-DOC-026 | `document` | content_sha256 | Read |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| DF-REF-220 | `document_type` | label_en | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read, through the parameters contract of DP-06 |
| (decision record) | decision-record library table in `rwb_document` | chain_seq, inputsRef, actions, outcome, decidedAt, prev_hash, entry_hash | Written by the store, not by this story |
| (reference data) | `document_type`, `lov_value` | the type list and its labels at the version in force | Read through the reference-data contract of DP-07 |

Field IDs are those in the Logical Data Model and Data Dictionary. `document_hub_parameter` is read through the parameters contract, not by a join: the values `INTAKE_MAX_FILE_MB` and `INTAKE_ALLOWED_TYPES` arrive as parameters of DP-06. No table of another service is read (DP-01), and no personal data enters the screen payload, the log or the test data.

### 12. Contract

#### 12.1 REST operations provided

All three sit under the base `/api/recovery/document/v1`, are owned by P5 and are published by this story's service. The request and response field names are fixed by the P5 store contract to come; no P5 contract story exists for this key, so the field names of the shapes below are Not specified in the source documents (GAP-1033; ASM-1981).

**POST /api/recovery/document/v1/cases/{caseId}/documents** (API-P5-001)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (binary), type (doc_type_code, required), source (must be "UPLOAD" for a user call; other values refused with 422) |
| Response | 201 Document for a new document; 200 Document with messageCode MSG-P5-024 for a duplicate |
| Errors | 401; 403 no Documents C (MSG-P4-002) or case out of scope (MSG-P4-003); 404 case not found; 413 above INTAKE_MAX_FILE_MB (MSG-P5-017); 415 file type (MSG-P5-001); 422 type missing (MSG-GEN-001), type not in the table (MSG-P5-006) or malware found (MSG-P5-016); 503 decision record write failed (MSG-P7-003) or scan contract unavailable (MSG-GEN-006) |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours per user; a repeat returns the first response |

**GET /api/recovery/document/v1/cases/{caseId}/documents** (API-P5-002)

| Item | Value |
|---|---|
| Request | Query type, page, size plus dateFrom and dateTo (date); size default 20, maximum 100 |
| Response | 200 DocumentPage: items (Document), page, size, total; only active versions, newest first |
| Errors | 401; 403 (MSG-P4-002, MSG-P4-003); 404 case not found; 422 dateFrom after dateTo (MSG-GEN-003); 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

**GET /api/recovery/document/v1/cases/{caseId}/document-checklist** (API-P5-008)

| Item | Value |
|---|---|
| Request | Path caseId |
| Response | 200 DocumentChecklist: caseId, checklistVersion (here the type table version), items [documentType, label, required, presentCount], missingCount, complete |
| Errors | 401; 403 (MSG-P4-002, MSG-P4-003); 404; 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

The placeholder returns required = false for every item, missingCount 0 and complete null until RWB-P5-E1040-APP sets the required items. Each error is an RFC 9457 problem response carrying `messageId`.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Note |
|---|---|---|---|
| POST | the scan operation of RWB-P5-E1041-CON | P5 | Called after the intake container write and before the store; answers "CLEAN" or "INFECTED". Its path is Not specified in the source documents (GAP-1034; ASM-1982) |
| GET | `/api/recovery/document/v1/...` store call of RWB-P5-E1024-APP | P5 | The store is the same service, called through its published interface (DP-11: REST contract with mock, one hop, 2 s timeout); its request and response shapes are the store's own |
| GET | the parameters read of DP-06 | P3 behind the client library | `INTAKE_MAX_FILE_MB`, `INTAKE_ALLOWED_TYPES`; read through RWB-PLT-E1042-CON and the contract RWB-P3-E1042-CON, cached |
| GET | the reference-data read of DP-07 | P3 behind the client library | The type list, its labels and the type table version in force; read through RWB-PLT-E1043-CON and the contract RWB-P3-E1043-CON, cached |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 | The case read for the scope test: the owner, queue and team; one hop, 2 s timeout, breaker and one GET retry with jitter |

RWB-P3-E1030-CON is the queue-measure and product-parameter contract that the case record view header uses; it composes above this tab and this story calls none of it. RWB-P3-E1042-CON and RWB-P3-E1043-CON are the parameter and reference-data contracts the client libraries of DP-06 and DP-07 speak.

#### 12.3 Events published

None. This story publishes no event of its own: the store of RWB-P5-E1024-APP publishes `rwb.document.DocumentStored.v1` on `rwb.document.events.v1` when the upload commits.

#### 12.4 Events consumed

None. The tab is pulled by the browser through gateway-bff; no event changes a screen state in this story.

#### 12.5 Workflows and activities

None. This story adds no Temporal workflow and no activity; the upload is one synchronous REST call with a 2 s budget per hop.

#### 12.6 Schedules

None for this story. The document-intake Schedule every 15 minutes is RWB-P5-E1049-APP's (FSD P5 AC-BG-P5-004-01); this story holds none.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 (`rwb_document`) | Read: the list, the search, the stored date, the type, the source, the version, the active flag and `content_sha256`; no write by this story |
| `document_type` | P5 (`rwb_document`) | Read: the type rows of the version in force, their labels and the checklist types |
| `document_hub_parameter` | P5 (`rwb_document`) | Not read as a table; the values arrive through the parameters contract of DP-06 |
| `processed_event`, outbox | PLT library in `rwb_document` | Not used: no event is consumed or published here |

No other table is read, and the scan result row is RWB-P5-E1041-APP's.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-document store fake | RWB-P5-E1024-APP | The acceptance criteria and the list refresh, so the tab builds before the store lands |
| rwb-document scan contract fake | RWB-P5-E1041-CON | "CLEAN" for AC1 and "INFECTED" for AC5 |
| document type table fake | RWB-P5-E1025-APP | The six agreed types, their labels and the version "DOCTYPE-2026.11" |
| parameters and reference-data fakes | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON with RWB-P3-E1042-CON and RWB-P3-E1043-CON | `INTAKE_MAX_FILE_MB` 25, `INTAKE_ALLOWED_TYPES`, the type list |
| rwb-case contract fake | the rwb-case case contract, with RWB-P3-E1030-CON for the header | The scope test read: case "RW-2026-000123" owned by "TEST-CO-01" in team "MTG-BKK-LIT" |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 2 to 3 | Upload, list and checklist provided; the scan and the store consumed, plus the case, parameter and reference-data reads through their clients |
| Kafka | Published 0, consumed 0 | The store publishes `DocumentStored`; this story listens to nothing |
| Temporal | None | No workflow, no activity, no Schedule |
| File | Upload | The file enters the intake container and the store copies it to Blob (WORM) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `casedocs`; front end folder `recovery/documents`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentHubController | Controller | Adds POST and GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist, with the access check and `Idempotency-Key` |
| CaseDocumentUploadService | Service | Intake container write, scan call to RWB-P5-E1041-CON, store call to RWB-P5-E1024-APP, idempotency key handling |
| CaseDocumentQueryService | Service | List and search by case, type and stored date with paging, and the scope test on the case read |
| ChecklistPlaceholderService | Service | Builds the six-type placeholder from the type table and the counts per type |
| CaseDocumentQueryRepository | Repository | Reads `document` only, filtered by case, type, active flag and created_at |
| CaseDocumentsTab | React component | SCR-30 with the list, the search bar and the checklist placeholder, served through gateway-bff |
| UploadDocumentDialog | React component | File picker, type list read through DP-07, size check against `INTAKE_MAX_FILE_MB`, error display |

**Database**

- Reads `document` (id, case_id, document_type, source, retention_class, write_once, doc_version, is_active, created_at, content_sha256) and `document_type` (doc_type_code, label_en, table_version).
- Uses the index `ix_document_case_type_created` from RWB-P5-E1024-APP. No new table, no new column.
- Flyway: none. This story adds no migration; the schema and the index are RWB-P5-E1024-APP's.

**Configuration and reference data**

- Document type table version "DOCTYPE-2026.11" through the reference-data contract of DP-07 (RWB-P5-E1025-APP loads it).
- Document hub parameters `INTAKE_MAX_FILE_MB` = 25 (assumed, DL11) and `INTAKE_ALLOWED_TYPES` = PDF, JPG, PNG through the parameters contract of DP-06.
- Property `rwb.document.casedocs.page-size` = 20; the API maximum stays 100.
- Feature flag `rwb.document.casedocs`. Off: the Documents tab is hidden and the three operations return 404.

**Build steps**

1. Extend the list endpoint with dateFrom and dateTo and the date order check; API tests for AC2, AC9, AC10 and AC11.
2. Build CaseDocumentUploadService with the scan call and the store call, in that order, and the 503 path when the scan contract does not answer; integration tests for AC1, AC4, AC5 and AC6.
3. Add the duplicate response and the Idempotency-Key handling; tests for AC7 and AC8.
4. Build ChecklistPlaceholderService and the checklist endpoint; test AC3.
5. Build CaseDocumentsTab and UploadDocumentDialog with the states Loading, list, upload, empty and error, and the size check from DP-06; component tests for each state.
6. Browser test of upload to list within 5 seconds in SIT through the gateway-bff route, and the access test.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-19 is the change to the screen: SCR-30 stops being a monolith page served with the case record and becomes a tab published by the gateway-bff composite route, which calls `rwb-document` one hop for the list, the upload and the checklist and merges the answer (Architecture v5 slide 10). DP-06 and DP-07 are the parameters and the type list: the size limit, the allowed file types, the page size and the six types arrive through the parameter and reference-data contracts and their client libraries, so no business value is typed in code. DP-03 is the decision record of the store this screen calls: the write sits in the store transaction of RWB-P5-E1024-APP through the decision-record library, and this screen never writes the log itself.

**Done when.** The tests in section 16 pass, and a 2 MB upload shows in the list within 5 seconds in SIT through the gateway-bff route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | Upload with no document type | Enter {field}. |
| MSG-GEN-003 | Date from after date to | {field} cannot be before {other}. |
| MSG-P5-001 | File type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-016 | Malware found | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P5-017 | File above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-024 | Same file already on the case | This file is already on the case as {document}. |
| MSG-P5-006 | Type not in the table | {value} is not a document type in force. Choose a type from the list. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | A service this screen calls does not answer | Not specified in the source documents (GAP-1033; ASM-1981). The ID and the placeholder name follow FSD P5 AC-EXC-P5-001-03 |

Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The upload answers 401, 403, 404, 413, 415, 422 and 503; the list and the checklist answer 401, 403, 404, 422 and 503.

### 15. Screens and states

SCR-30 Case documents, reached from SCR-03 Case record and published inside it by the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON); the browser never calls `rwb-document` directly.

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while the list and the checklist load through the composite route |
| list | Documents with type, stored date, source, version and the write-once label; search bar with type and date range; checklist placeholder with the six types |
| upload | Upload dialog with file, document type and the size limit read through DP-06; errors from section 14 next to the field |
| Empty | "No documents match this search." with the action "Clear the search" (common state) |
| Error | The message from section 14 at the top |

The checklist placeholder lists the six types of the type table in force, with present counts per type; required, missingCount and complete stay false, 0 and null until RWB-P5-E1040-APP sets the required items. The Upload button shows only to roles with Documents C. The route path and the fields gateway-bff merges are Not specified in the source documents (GAP-1035; ASM-1983).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-026-12 | Access | Component | Team manager (RW-TEAMMGR, Documents R only) uploads; refused with MSG-P4-002 |
| TC-E1-026-13 | Principle 5 | NFR | Decision log write forced to fail during an upload; nothing stored, MSG-P7-003 |
| TC-E1-026-01 | AC1, BR1 | End to end | Synthetic 2 MB court notice PDF |
| TC-E1-026-02 | AC2, BR4 | End to end | Case with 50 synthetic documents, 12 court notices, 4 in October 2026 |
| TC-E1-026-03 | AC3, BR5 | End to end | Case with 12 court notices and 1 appraisal report |
| TC-E1-026-04 | AC4, BR1 | End to end | Upload without a type |
| TC-E1-026-05 | AC5, BR2 | End to end | EICAR test file |
| TC-E1-026-06 | AC6 | End to end | Spreadsheet file |
| TC-E1-026-07 | AC7, BR6 | End to end | Same PDF uploaded twice |
| TC-E1-026-08 | AC8, BR6 | End to end | Two requests with Idempotency-Key TEST-KEY-0001 |
| TC-E1-026-09 | AC9 | End to end | Date range 31 October to 1 October 2026 |
| TC-E1-026-10 | AC10 | End to end | Search for TITLE_DEED on a case without one |
| TC-E1-026-11 | AC11, BR3 | End to end | Case owner with scope OWN on another owner's case |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR. The wave-1 integration copy of AC1 and AC2 carries the suffix `-ITG` (RWB-ITG-E1026-ITG), where the rwb-case, the store, the scan and the parameter contracts are the real services instead of fakes.

### 17. Guardrails

- No business value in code: the type list, size limit, file types and page size are data or properties (BR-P5-004, DP-06, DP-07).
- No personal data in logs, tests or prompts. File names in logs are replaced by the document ID.
- No cross-schema read (DP-01): the case comes through the rwb-case contract, the parameters and reference data through their contracts, the store and the scan through their published interfaces; this story reads `rwb_document` only.
- The front end size check does not replace the server check; the server refuses 413 with MSG-P5-017 whatever the browser sent.
- The scan runs before the store, and an unknown scan answer stores nothing.
- The feature flag `rwb.document.casedocs` removes the tab without a rollback of the schema.
- The tab keeps its legacy values: the same endpoints, request, response, errors, authorization, messages and acceptance criteria.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-008 | Documents searchable by case ID, type and date from the case record view | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-05 | 13 Manage documents and correspondence | BR3; BR4 | TC-E1-026-02, TC-E1-026-03, TC-E1-026-09, TC-E1-026-10, TC-E1-026-11 |
| REQ-DCM-001 | Every document stored against its case with type, date and source | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-04 | 13 Manage documents and correspondence | BR1; BR6; R-UNI-39, R-UNI-40 | TC-E1-026-01, TC-E1-026-04 to TC-E1-026-08, TC-E1-026-12, TC-E1-026-13 |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-18; FEAT-DCM-17 | 13 Manage documents and correspondence | BR2; BR7 | TC-E1-026-05, TC-E1-026-13 |
| REQ-DCM-011 | A document checklist per case type is held as reference data so that a missing document is visible | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-16 | 13 Manage documents and correspondence | BR5 | TC-E1-026-03 |

| Legacy reference | Where it is kept |
|---|---|
| Document type table version "DOCTYPE-2026.11" and the six agreed types | Metadata, Background, sections 3, 8, 13 |
| Parameters INTAKE_MAX_FILE_MB = 25 (assumed, DL11) and INTAKE_ALLOWED_TYPES = PDF, JPG, PNG | Sections 3, 4, 13 |
| Messages MSG-GEN-001, MSG-GEN-003, MSG-P5-001, MSG-P5-006, MSG-P5-016, MSG-P5-017, MSG-P5-024, MSG-P4-002, MSG-P4-003, MSG-P7-003, MSG-GEN-006 | Section 14, exception paths |
| Acceptance criteria AC1 to AC11 and test cases TC-E1-026-01 to TC-E1-026-13 | Sections 7, 16 |
| Rules BR1 to BR7, R-UNI-39, R-UNI-40 | Sections 8, 18 |
| Legacy key RWB-E1-026, story RWB-P5-E1026-APP, store RWB-P5-E1024-APP, types RWB-P5-E1025-APP, scan RWB-P5-E1041-CON | Metadata, sections 1, 3, 12 |

### 19. Out of scope

- Required items per case type and the completeness flag (RWB-P5-E1040-APP).
- Search across cases and free text search (RWB-P5-E1033-APP).
- Search on extracted fields within a case; RWB-P5-E1033-APP builds the field filter.
- OCR, classification and extraction of an uploaded file (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP).
- Upload from the field app (RWB-P5-E2024-APP) and from partners (Epic 5, DL03).
- The store internals: the write-once container, the versions, the detail panel and `DocumentStored` (RWB-P5-E1024-APP).
- The malware scan and the retention classes themselves (RWB-P5-E1041-APP and its contract RWB-P5-E1041-CON).
- The end-to-end proof across the real services (RWB-ITG-E1026-ITG).

# Technical Specification — RWB-E1-026 Attach and search screen

| Field | Value |
|---|---|
| Story | RWB-E1-026 — Attach and search screen |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-061-epic-1-RWB-E1-026` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-014); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 026 Attach and search screen v1.md`; FSD P5 A2.4, A2.5; TSD P5 T-A |
| Upstream IDs | BRD-RWB-005; FR-RWB-014; REQ-DCM-001, REQ-DCM-008; US-RWB-E1-026; CTX-FEATURE-005; CTL-09; DL03, DL11; R-UNI-39, R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — adds SCR-30 Case documents as a tab on SCR-03 Case record, with list, search bar, checklist placeholder, upload dialog, empty state and error state. |
| Logic In Scope | `YES` — upload orchestration, malware scan call, duplicate and idempotency handling, list/search by type and stored date, checklist counts and access checks. |
| API In Scope | `YES` — adds `GET /cases/{caseId}/document-checklist` and extends `GET /cases/{caseId}/documents` with `dateFrom` and `dateTo`; `POST /cases/{caseId}/documents` gains duplicate and scan behaviour. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `document` (RWB-E1-024); document type table (RWB-E1-025); malware scan (RWB-E1-041); document hub parameters (RWB-E1-024); `CaseDirectory` (P3); `DecisionLogWriter` (P7); SCR-03 Case record. |
| New Nodes Required | `YES` — `CaseDocumentUploadService`, `CaseDocumentQueryService`, `ChecklistPlaceholderService`, `CaseDocumentQueryRepository`, `CaseDocumentsTab`, `UploadDocumentDialog`. |
| Inherited Existing Behavior | Document store and detail panel (RWB-E1-024); document types (RWB-E1-025); malware scan (RWB-E1-041); product parameters (RWB-E1-045); queue measures (RWB-E1-030); case record view (RWB-E1-023). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A user upload carries a document type from the type table in force and source `UPLOAD`. | SPEC-RWB-E1-026-002, SPEC-RWB-E1-026-003 | DIRECT | Type is required; other source values are refused with 422. | COVERED |
| BR2 | Every upload is scanned for malware before it is stored. | SPEC-RWB-E1-026-003, SPEC-RWB-E1-026-013 | DIRECT | `MalwareScanService.scanNow` before `DocumentStore.store`. | COVERED |
| BR3 | The list and the search show only cases in the user's scope. | SPEC-RWB-E1-026-011 | DIRECT | Spring Security and scope filter on every call. | COVERED |
| BR4 | The date filter applies to the stored date of the document in Epic 1. | SPEC-RWB-E1-026-005 | DIRECT | `document.created_at`; `dateFrom`/`dateTo` inclusive. | COVERED |
| BR5 | The checklist placeholder lists the types of the type table in force; required items per case type come in RWB-E1-040. | SPEC-RWB-E1-026-006 | DIRECT | `required=false`, `missingCount=0`, `complete=null`. | COVERED |
| BR6 | A repeated upload with the same file, type and case returns the existing document. | SPEC-RWB-E1-026-007 | DIRECT | 200 with existing ID and MSG-P5-024. | COVERED |
| BR7 | A store that cannot be written to the decision log does not proceed. | SPEC-RWB-E1-026-012 | DIRECT | Store transaction rolls back; MSG-P7-003. | COVERED |
| AC1 | A 2 MB court notice upload returns 201 with source `UPLOAD` and version 1; it appears at the top within 5 seconds; the list by type returns it. | SPEC-RWB-E1-026-003, SPEC-RWB-E1-026-004, SPEC-RWB-E1-026-005 | DIRECT | Upload, refresh and list. | COVERED |
| AC2 | A case with 50 documents, 12 court notices and 4 in October returns exactly the 4, newest first, count 4. | SPEC-RWB-E1-026-005 | DIRECT | Type plus date range; count in the page. | COVERED |
| AC3 | The checklist lists the six types; `COURT_NOTICE` present 12, `APPRAISAL_REPORT` present 1; the other four not present. | SPEC-RWB-E1-026-006 | DIRECT | Counts per type from active documents. | COVERED |
| AC4 | Upload without a type returns 422 MSG-GEN-001 naming Document type; nothing stored. | SPEC-RWB-E1-026-015 | DIRECT | Server check; front-end check too. | COVERED |
| AC5 | An EICAR upload returns 422 MSG-P5-016; the file is in quarantine; no document row. | SPEC-RWB-E1-026-013 | DIRECT | Scan refusal before store. | COVERED |
| AC6 | A spreadsheet upload returns 415 MSG-P5-001 in the dialog; nothing stored. | SPEC-RWB-E1-026-014 | DIRECT | Content signature; server is authoritative. | COVERED |
| AC7 | The same file and type returns 200 with the existing ID and MSG-P5-024; one copy remains. | SPEC-RWB-E1-026-007 | DIRECT | Duplicate response and highlight. | COVERED |
| AC8 | Two submits with the same `Idempotency-Key` return the same document ID; one row and one log entry. | SPEC-RWB-E1-026-008 | DIRECT | Key kept 24 hours per user. | COVERED |
| AC9 | A search from 31 October to 1 October is not run; MSG-GEN-003 shows next to the dates. | SPEC-RWB-E1-026-009 | DIRECT | Client and server validation. | COVERED |
| AC10 | A search with no match shows "No documents match this search." and "Clear the search". | SPEC-RWB-E1-026-010 | DIRECT | Empty state. | COVERED |
| AC11 | A case owner with scope OWN who does not own the case gets 403 MSG-P4-003 and no document name. | SPEC-RWB-E1-026-011 | DIRECT | Scope filter. | COVERED |
| X1 | Upload with no type. | SPEC-RWB-E1-026-015 | DIRECT | 422 MSG-GEN-001. | COVERED |
| X2 | File fails the malware scan. | SPEC-RWB-E1-026-013 | DIRECT | 422 MSG-P5-016; quarantine; no row. | COVERED |
| X3 | File type not allowed. | SPEC-RWB-E1-026-014 | DIRECT | 415 MSG-P5-001. | COVERED |
| X4 | Same file and type already on the case. | SPEC-RWB-E1-026-007 | DIRECT | Existing returned; MSG-P5-024. | COVERED |
| X5 | Double submit with the same key. | SPEC-RWB-E1-026-008 | DIRECT | One document; first result returned. | COVERED |
| X6 | Date from after date to. | SPEC-RWB-E1-026-009 | DIRECT | Search not run; MSG-GEN-003. | COVERED |
| X7 | Search matches nothing. | SPEC-RWB-E1-026-010 | DIRECT | Empty state with clear action. | COVERED |
| X8 | Case outside scope. | SPEC-RWB-E1-026-011 | DIRECT | 403 MSG-P4-003. | COVERED |
| X9 | Role without Documents C uploads. | SPEC-RWB-E1-026-011 | DIRECT | 403 MSG-P4-002; Upload button hidden. | COVERED |
| X10 | Decision log write fails during store. | SPEC-RWB-E1-026-012 | DIRECT | Nothing stored; MSG-P7-003 in the dialog. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **to upload, see and search the documents of a case from the case record view**, so that **the case file is complete and I find a document by type and date without leaving the case**.

The story puts the Documents tab on the case record: an upload with a type, a list of every active document on the case, a search by type and stored date, and a checklist placeholder showing which of the six agreed types are present. It orchestrates the scan and the store but does not reimplement either. It adds no cross-case search and no extracted-field filter; RWB-E1-033 builds those.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | User opens SCR-03 Case record and the Documents tab; user uploads a file; user searches by type and date. |
| Preconditions | RWB-E1-024 done (store and reads); RWB-E1-025 done (type table in force); RWB-E1-041 done (malware scan); RWB-E1-045 and RWB-E1-030 done (parameters and queue measures); `INTAKE_MAX_FILE_MB=25` (assumed; DL11) and `INTAKE_ALLOWED_TYPES=PDF,JPG,PNG`; user holds Documents C to upload and Documents R to list, with the case in scope; `rwb.dochub.casedocs` flag on. |
| Input | Case ID; file; document type; search type and date range; page and size. |
| Output | Document row through `DocumentStore`; list page; checklist counts; messages; upload dialog state. |
| Feature flag | `rwb.dochub.casedocs`. Off: the Documents tab is hidden and the endpoints return 404. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document` | `document_type` | Type list | User chooses on upload | Required; must be in the type table in force |
| `document` | `source` | Upload service | Read-only | `UPLOAD` for a user call |
| `document` | `created_at` | Store | Read-only | Displayed and filtered as the stored date |
| `document` | `doc_version` | Store | Read-only | Shown in the list |
| `document` | `write_once` | Type table | Read-only | Shows the "Write once" label |
| `document` | `is_active` | Store/version | Read-only | The list returns active versions only |
| Search | `type` | User | Editable | Optional; one type from the list |
| Search | `dateFrom`, `dateTo` | User | Editable | Optional; `dateFrom <= dateTo`; inclusive on the stored date |
| Search | `page`, `size` | User / default | Editable | `size` default 20, maximum 100 |
| Checklist | `documentType`, `label`, `required`, `presentCount` | Type table and counts | Read-only | Six types; `required=false` until RWB-E1-040 |
| Checklist | `missingCount`, `complete` | Placeholder | Read-only | `0` and `null` until RWB-E1-040 |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Upload submit | Type present, file allowed, scan CLEAN, store succeeds | `COPY_PENDING` | 201; list refresh; row appears at the top within 5 seconds |
| `COPY_PENDING` | Copy succeeds | Container accepts | `STORED` | List shows the document |
| None | Upload submit | Scan INFECTED | No row | 422 MSG-P5-016; file in quarantine |
| None | Upload submit | Duplicate case, type and hash | Existing row | 200 with existing ID and MSG-P5-024; highlighted |
| Tab Loading | List and checklist return | Both succeed | list | Documents, search bar, checklist |
| list | Search with no match | Zero rows | Empty | "No documents match this search." and clear action |
| list | Read refused | 403/503 | Error | Message at the top; no document names |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No document type | 422; nothing stored; field error | MSG-GEN-001 |
| X2 | Malware found | 422; quarantine; no row | MSG-P5-016 |
| X3 | File type not allowed | 415; nothing stored | MSG-P5-001 |
| X4 | Duplicate file and type | 200 existing; highlighted | MSG-P5-024 |
| X5 | Double submit | One document; same result | None |
| X6 | `dateFrom` after `dateTo` | Search not run; error next to the dates | MSG-GEN-003 |
| X7 | No match | Empty state and clear action | None |
| X8 | Case outside scope | 403; no document name | MSG-P4-003 |
| X9 | Role without Documents C | 403; Upload button hidden | MSG-P4-002 |
| X10 | Decision log write fails | Nothing stored; dialog error | MSG-P7-003 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints | `POST /api/recovery/v1/cases/{caseId}/documents` (API-P5-001); `GET /api/recovery/v1/cases/{caseId}/documents` (API-P5-002); `GET /api/recovery/v1/cases/{caseId}/document-checklist` (API-P5-008, new). |
| Contract delta | The list adds `dateFrom` and `dateTo` (date, stored date, inclusive) and 422 MSG-GEN-003 when the range is inverted. The checklist response is `DocumentChecklist` with `caseId`, `checklistVersion`, `items[]`, `missingCount` and `complete`. The upload response adds `messageCode` for the duplicate case. API specification v2 already records all three; no new contract authoring is required. |
| Backward compatibility | Additive; existing list callers without dates are unaffected. |
| Authorization | Documents C to upload; Documents R to list and checklist; scope applied. 401 MSG-P4-001; 403 MSG-P4-002/MSG-P4-003; 404; 413 MSG-P5-017; 415 MSG-P5-001; 422 MSG-GEN-001/MSG-GEN-003/MSG-P5-006/MSG-P5-016; 503 MSG-P7-003/MSG-P5-022. |
| Versioning | No API version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-008; SPEC-RWB-E1-026-001, 002, 010, 017 | New `CaseDocumentsTab` and `UploadDocumentDialog` with Loading, list, upload, empty and error states. | Component tests: Loading skeleton; list render with type, date, source, version and write-once label; search validation; empty state and clear action; upload dialog size check; Upload button visibility by right; error message display. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-001, REQ-DCM-008; SPEC-RWB-E1-026-003..016 | New upload service, query service, checklist service and repository; two endpoint changes. | Upload happy path; no type; scan infected; scan unavailable; file type; size boundary; duplicate; idempotency; date range; empty; scope and right refusal; decision log failure; checklist counts. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DocumentHubController` | Controller | Adds POST and GET `/cases/{caseId}/documents` and GET `/cases/{caseId}/document-checklist`. |
| `CaseDocumentUploadService` | Service | Intake container write, malware scan call, `DocumentStore.store`, idempotency key handling. |
| `CaseDocumentQueryService` | Service | List and search by case, type and stored date with paging. |
| `ChecklistPlaceholderService` | Service | Builds the six-type placeholder from `DocumentTypeCatalog` and the counts per type. |
| `CaseDocumentQueryRepository` | Repository | Reads `document` only, filtered by case, type, active flag and `created_at`. |
| `CaseDocumentsTab` | React component | SCR-30 with the list, search bar and checklist placeholder. |
| `UploadDocumentDialog` | React component | File picker, type list, size check and error display. |

### Package and boundaries

Folder `recovery/dochub/casedocs`, Java package `recovery.dochub.casedocs`; front-end folder
`recovery/documents`. The service calls `DocumentStore` (RWB-E1-024) and `MalwareScanService`
(RWB-E1-041); it reads the case through `CaseDirectory` and never writes `document` directly.

### Data and migration

Reads `document` (`id`, `case_id`, `document_type`, `source`, `retention_class`, `write_once`,
`doc_version`, `is_active`, `created_at`, `content_sha256`). Uses index `ix_document_case_type_created`
from RWB-E1-024. No new table and no Flyway migration. Page size property
`rwb.dochub.casedocs.page-size = 20`.

### Upload flow

1. The front end checks the file size against `INTAKE_MAX_FILE_MB` before sending; the server repeats
   the check.
2. `CaseDocumentUploadService` writes the file to `rwb-intake`.
3. It calls `MalwareScanService.scanNow`. INFECTED returns 422 MSG-P5-016 and leaves the file in
   quarantine; unavailable returns 503 MSG-P5-022 and keeps nothing.
4. It calls `DocumentStore.store` with source `UPLOAD` and the chosen type. The store writes the
   `DOCATT` entry, the row and `DocumentStored`, then copies the file.
5. It returns 201 with the document; the front end refreshes the list and the new row shows within 5
   seconds of submit.
6. A duplicate case/type/hash returns 200 with the existing ID and MSG-P5-024; the row is highlighted.

### List and search

- `GET /cases/{caseId}/documents` returns active versions only, newest first (`created_at desc`).
- Filters: `type`, `dateFrom`, `dateTo` on the stored date, inclusive; `page` and `size` (default 20,
  maximum 100).
- A `dateFrom` after `dateTo` returns 422 MSG-GEN-003; the front end does not send the request.
- A zero-row result returns an empty page; the UI shows the empty state with "Clear the search".
- The total count is the filtered count, so AC2 reads 4.

### Checklist placeholder

- Reads the six types from `DocumentTypeCatalog` in force.
- Counts active documents per type on the case.
- Returns `required=false` for every item, `missingCount=0` and `complete=null` until RWB-E1-040 sets the
  required items. `checklistVersion` is the type table version.
- A type with no document shows present count 0 and "not present".

### Idempotency and duplicate

- `Idempotency-Key` is kept 24 hours per user; a repeat returns the first response, including the same
  document ID.
- The duplicate check is the store's case + type + content hash rule; the upload service maps the
  existing result to 200 with MSG-P5-024.

### Transaction and events

The upload service does not own a transaction; `DocumentStore.store` writes the decision log, row, fields
and `DocumentStored` in one transaction. The scan call is before the store and writes nothing to
`document`. No event is published by this story.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| Roles with Documents C (RW-CASEOWN, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT) | Upload | Own/team |
| Roles with Documents R (RW-TEAMMGR, RW-PHONECOL, RW-AUDIT and others) | List, search and open | Own/team |
| PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION | No access in Epic 1; partners use the external gateway (DL03) | — |
| SY-DECLOG | Writes the `DOCATT` entry | All |

The Upload button renders only for a role with Documents C; the server still checks the right.

### Observability and operations

- Metrics: uploads, scan refusals, duplicates, validation refusals by reason, list latency, search
  result count, access refusals.
- Logs carry case ID, document ID and counts; file names are replaced by the document ID.
- Alerts: upload error rate; scan unavailable; list latency above target.
- Run book: scan service outage, storage outage, list performance.

### Performance

- A 2 MB upload shows in the list within 5 seconds of submit in SIT (story "Done when").
- The list and search return within the user wait; no separate p95 is approved (DL11). The measurable
  target in this story is the 5-second upload-to-list time.
- `ix_document_case_type_created` serves the case/type/date filter; counts use the same index.

### Accessibility and content

- SCR-30 follows the accessibility standard: labelled fields, keyboard-operable dialog, focus return on
  close, error text associated with the field, and the empty-state action reachable by keyboard.
- Labels and messages come from the content and label standard; Thai text follows DL10.

### Feature flag and rollback

- `rwb.dochub.casedocs`. Off: the Documents tab is hidden and the endpoints return 404.
- Rollback: turn the flag off; redeploy the previous tag. No migration is added by this story.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-026-01 | AC1, BR1 | System | Synthetic 2 MB court notice PDF | 201, source `UPLOAD`, v1; top of list within 5 seconds; list by type returns it |
| TC-E1-026-02 | AC2, BR4 | System | 50 documents, 12 court notices, 4 in October 2026 | Exactly 4, newest first; count 4 |
| TC-E1-026-03 | AC3, BR5 | System | 12 court notices and 1 appraisal report | Six types; counts 12 and 1; other four not present |
| TC-E1-026-04 | AC4, BR1 | System | Upload without a type | 422 MSG-GEN-001 naming Document type; nothing stored |
| TC-E1-026-05 | AC5, BR2 | System | EICAR test file | 422 MSG-P5-016; quarantine; no row |
| TC-E1-026-06 | AC6 | System | Spreadsheet file | 415 MSG-P5-001 in the dialog; nothing stored |
| TC-E1-026-07 | AC7, BR6 | System | Same PDF uploaded twice | 200 existing ID and MSG-P5-024; one copy |
| TC-E1-026-08 | AC8, BR6 | System | Two requests with `TEST-KEY-0001` | Same document ID; one row and one log entry |
| TC-E1-026-09 | AC9 | System | Date range 31 October to 1 October 2026 | No request; MSG-GEN-003 next to the dates |
| TC-E1-026-10 | AC10 | System | Search `TITLE_DEED` on a case without one | Empty state and clear action |
| TC-E1-026-11 | AC11, BR3 | System | Case owner with scope OWN on another owner's case | 403 MSG-P4-003; no document name |
| TC-E1-026-12 | X9 | Security | RW-TEAMMGR (Documents R only) uploads | 403 MSG-P4-002; button hidden |
| TC-E1-026-13 | X10 | Resilience | Decision log write forced to fail during upload | Nothing stored; MSG-P7-003 in the dialog |
| TC-E1-026-U1 | BR4, BR5, AC2, AC9 | Unit | Inverted date range; 50 documents with 4 in October; six-type checklist | 422 MSG-GEN-003; count 4 newest first; six items with correct counts |

## Guardrails

- No business value in code: the type list, size limit, file types and page size are data or properties.
- No personal data in logs, tests or prompts. File names in logs are replaced by the document ID.
- No read of another module's tables: the case and the scope come through `CaseDirectory` and the ACE
  access check.
- The front-end size check does not replace the server check.

## Out of scope

- Required items per case type and the completeness flag (RWB-E1-040).
- Search across cases and free text search (RWB-E1-033).
- Search on extracted fields within a case (RWB-E1-033 builds the field filter).
- OCR, classification and extraction of an uploaded file (RWB-E1-049, RWB-E1-050, RWB-E1-053).
- Upload from the field app (RWB-E2-024) and from partners (Epic 5, DL03).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-008 | Documents searchable by case ID, type and date from the case record view | Business Requirements Epic 1, section 3.5 | FEAT-DCM-05 | 13 Manage documents and correspondence | None | TC-E1-026-02, 03, 09, 10, 11 |
| REQ-DCM-001 | Every document stored against its case with type, date and source | Business Requirements Epic 1, section 3.5 | FEAT-DCM-04 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-026-01, 04..08, 12, 13 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Flow step 7; SPEC-005 | What is the page size and sort order? | List behaviour. | 20 per page, maximum 100, newest first on the stored date; the property is `rwb.dochub.casedocs.page-size` (story flow step 7, contract). | RESOLVED | SPEC-005 |
| CLAR-002 | AC2; SPEC-005 | What is the "stored date"? | Filter boundary. | `document.created_at`, as recorded in the story data table. | RESOLVED | SPEC-005 |
| CLAR-003 | AC3; SPEC-006 | What does the placeholder return before RWB-E1-040? | Checklist display. | Six types, `required=false` for every item, `missingCount=0`, `complete=null` (story contract). | RESOLVED | SPEC-006 |
| CLAR-004 | AC8; SPEC-008 | How long is the idempotency key kept? | Repeat submit behaviour. | 24 hours per user; a repeat returns the first response (story contract). | RESOLVED | SPEC-008 |
| CLAR-005 | AC1; SPEC-011 | Is the Upload button hidden or disabled without Documents C? | UI behaviour. | Hidden; the server still returns 403 if called (story §15 and authority). | RESOLVED | SPEC-011 |
| CLAR-006 | AC7; SPEC-007 | What does the duplicate upload show? | User feedback. | The existing document is returned and highlighted in the list with MSG-P5-024; no second document. | RESOLVED | SPEC-007 |
| CLAR-007 | AC2; SPEC-005 | Is the date filter inclusive at both ends? | Result count. | Inclusive: `dateFrom <= created_at::date <= dateTo`; the October example includes 1 and 31 October. | RESOLVED | SPEC-005 |
| CLAR-008 | API assessment; SPEC-005 | Is the checklist endpoint a contract change? | API impact classification. | It is a new E1 endpoint already recorded in API specification v2; the list date parameters are also recorded there. No new contract authoring is required. | RESOLVED | SPEC-005, SPEC-006 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story or the API specification. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-30 screen specification; no Figma source.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New SCR-30 documents tab with upload, search and checklist placeholder; new checklist endpoint and list date filters.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new screen, new checklist endpoint and extended list contract]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 11 acceptance criteria, 10 exception paths and 7 UI states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

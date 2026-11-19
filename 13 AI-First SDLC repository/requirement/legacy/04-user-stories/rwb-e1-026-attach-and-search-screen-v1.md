<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 026 Attach and search screen v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 026 Attach and search screen v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-026 Attach and search screen

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-026 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-04 Attach a document to a case; FEAT-DCM-05 Search documents within a case |
| Requirement IDs | REQ-DCM-008, REQ-DCM-001 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-025, RWB-E1-024, RWB-E1-041, RWB-E1-045, RWB-E1-030 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **to upload, see and search the documents of a case from the case record view**, so that **the case file is complete and I find a document by type and date without leaving the case**.

## 2. Business rationale

Case owners hold documents in shared drives and email today, so the case file is never complete in one place (FSD P5 A1.3). This story puts the case documents screen SCR-30 on the case record view: upload with a type, a list of every document on the case, a search by type and date, and a checklist placeholder showing which of the six agreed types are present. It meets REQ-DCM-008 (search by case, type and date from the case record view) and REQ-DCM-001 (every document stored against its case with type, date and source). The measure is fields extracted without review (FSD P5 A2.4.1), which needs documents on the case first.

## 3. Preconditions

- RWB-E1-024 is done: DocumentStore stores, versions and reads documents.
- RWB-E1-025 is done: document type table DOCTYPE-2026.11 is in force.
- RWB-E1-041 is done: the malware scan runs on every file before storage.
- RWB-E1-045 and RWB-E1-030 are done: product parameters and the queue measures used by the case record view exist.
- Parameters INTAKE_MAX_FILE_MB = 25 (assumed, DL11) and INTAKE_ALLOWED_TYPES = PDF, JPG, PNG are in force.
- The user holds a role with Documents C to upload and Documents R to list, with the case in scope.
- Feature flag rwb.dochub.casedocs is on.

## 4. Flow

1. Case owner: opens case RW-2026-000123 on the case record view (SCR-03) and the Documents tab (SCR-30, state Loading then list).
2. Front end: calls GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist and shows the list and the checklist placeholder.
3. Case owner: chooses Upload, picks a file and a document type from the list, and submits; the front end checks the size against INTAKE_MAX_FILE_MB before sending and sends an Idempotency-Key.
4. CaseDocumentUploadService: puts the file in the intake container, calls the malware scan (RWB-E1-041) and, if clean, calls DocumentStore.store with source UPLOAD.
5. DocumentStore (RWB-E1-024): writes the decision log entry, the document row and DocumentStored, then copies the file.
6. Front end: on 201 refreshes the list; the new document shows within 5 seconds of submit.
7. Case owner: enters a type and a date range in the search bar; GET /cases/{caseId}/documents with type, dateFrom and dateTo returns only the matching documents, newest first, 20 per page.
8. Case owner: opens a document; DocumentDetailPanel (RWB-E1-024) shows it.

## 5. Exception paths

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
| X10 | The decision log write fails during the store | Nothing stored; the dialog shows the message | MSG-P7-003 | TC-E1-026-13 (Principle 5) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the store (RWB-E1-024), the types (RWB-E1-025) and the scan (RWB-E1-041), all earlier in Epic 1; no other screen depends on it |
| Negotiable | Page size, sort order and the placeholder layout can change; the endpoints stay |
| Valuable | Case owners attach and find documents on the case instead of in shared drives |
| Estimable | Two endpoints changed or added, one service, one tab with three parts |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Attach and search screen

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given user "TEST-CO-01" holds RW-CASEOWN and owns case "RW-2026-000123"

  Scenario: AC1 Upload
    Given "TEST-CO-01" is on the Documents tab of case "RW-2026-000123"
    When "TEST-CO-01" uploads "court-notice-0007.pdf" of 2 MB with type "COURT_NOTICE"
    Then the response is 201 with source "UPLOAD" and doc_version 1
    Then the document shows at the top of the case document list within 5 seconds of submit
    Then GET /cases/{caseId}/documents with type "COURT_NOTICE" returns it

  Scenario: AC2 Search
    Given case "RW-2026-000123" holds 50 documents of which 12 are "COURT_NOTICE"
    Given 4 of the court notices were stored between 1 October 2026 and 31 October 2026
    When "TEST-CO-01" searches type "COURT_NOTICE" from 1 October 2026 to 31 October 2026
    Then exactly the 4 court notices stored in October show, newest first
    Then the result count reads 4

  Scenario: AC3 Checklist placeholder
    Given case "RW-2026-000123" holds 12 court notices and 1 appraisal report and no other agreed type
    When the Documents tab opens
    Then the checklist placeholder lists the six agreed types
    Then COURT_NOTICE shows present with 12, APPRAISAL_REPORT shows present with 1
    Then DEMAND_LETTER, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE show not present

  Scenario: AC4 Upload without a type
    Given "TEST-CO-01" picks "scan-0009.pdf" and no document type
    When "TEST-CO-01" submits the upload
    Then the response is 422 with MSG-GEN-001 naming "Document type"
    Then the system stores no document

  Scenario: AC5 Upload that fails the malware scan
    Given a test file "eicar-0001.pdf" holding the EICAR test signature
    When "TEST-CO-01" uploads it with type "COURT_NOTICE"
    Then the response is 422 with MSG-P5-016
    Then the file is in the quarantine container and no document row exists

  Scenario: AC6 File type not allowed
    Given a file "minutes-0002.xlsx" with spreadsheet content
    When "TEST-CO-01" uploads it with type "SETTLEMENT_AGREEMENT"
    Then the response is 415 with MSG-P5-001 shown in the upload dialog
    Then the system stores no document

  Scenario: AC7 The same file uploaded again
    Given "court-notice-0007.pdf" is stored on case "RW-2026-000123" as "COURT_NOTICE"
    When "TEST-CO-01" uploads the same file with the same type
    Then the response is 200 with the existing document ID and MSG-P5-024
    Then the case still holds one copy of that court notice

  Scenario: AC8 Double submit
    Given "TEST-CO-01" submits "appraisal-0003.pdf" with Idempotency-Key "TEST-KEY-0001"
    When the same request with Idempotency-Key "TEST-KEY-0001" arrives a second time within 1 second
    Then both responses carry the same document ID
    Then one document row and one decision log entry exist for it

  Scenario: AC9 Date range in the wrong order
    Given "TEST-CO-01" is on the Documents tab
    When "TEST-CO-01" searches from 31 October 2026 to 1 October 2026
    Then the search is not run and MSG-GEN-003 shows next to the date fields

  Scenario: AC10 No document matches
    Given case "RW-2026-000123" holds no "TITLE_DEED"
    When "TEST-CO-01" searches type "TITLE_DEED"
    Then the list shows the empty state "No documents match this search." with the action "Clear the search"

  Scenario: AC11 Case outside the scope
    Given user "TEST-CO-02" holds RW-CASEOWN with scope OWN and does not own case "RW-2026-000123"
    When "TEST-CO-02" opens the Documents tab of that case
    Then GET /cases/{caseId}/documents returns 403 with MSG-P4-003
    Then the system shows no document name
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A user upload carries a document type from the type table in force and source UPLOAD | REQ-DCM-001; LOV-DOC-SOURCE |
| BR2 | Every upload is scanned for malware before it is stored | REQ-DCM-010; FEAT-DCM-18 |
| BR3 | The list and the search show only cases in the user's scope | CTL-09 |
| BR4 | The date filter applies to the stored date of the document in Epic 1 | FSD P5 A2.5; REQ-DCM-008 |
| BR5 | The checklist placeholder lists the types of the type table in force; the required items per case type come in RWB-E1-040 | REQ-DCM-011; FEAT-DCM-16 |
| BR6 | A repeated upload with the same file, type and case returns the existing document | R-UNI-40 |
| BR7 | A store that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |

## 9. State transitions

None. This story does not change a case status. A successful upload creates a document record in state COPY_PENDING, then STORED (RWB-E1-024).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| Roles with Documents C (RW-CASEOWN, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT) | Upload inside their scope |
| Roles with Documents R (for example RW-TEAMMGR, RW-PHONECOL, RW-AUDIT) | List, search and open documents inside their scope |
| Partner roles PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION | No access in Epic 1; partners reach the Workbench only through the external gateway (DL03) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry for each upload |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write, through DocumentStore |
| Standard column | document | created_at | Read, as the stored date |
| DF-DOC-026 | document | content_sha256 | Read |
| DF-REF-219 | document_type | doc_type_code | Read |
| DF-REF-220 | document_type | label_en | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DocumentStore and DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /cases/{caseId}/documents**

| Item | Value |
|---|---|
| Request | multipart/form-data: file (binary), type (doc_type_code, required), source (must be "UPLOAD" for a user call; other values refused with 422) |
| Response | 201 Document for a new document; 200 Document with messageCode MSG-P5-024 for a duplicate |
| Errors | 401; 403 no Documents C (MSG-P4-002) or case out of scope (MSG-P4-003); 404 case not found; 413 above INTAKE_MAX_FILE_MB (MSG-P5-017); 415 file type (MSG-P5-001); 422 type missing (MSG-GEN-001), type not in the table (MSG-P5-006) or malware found (MSG-P5-016); 503 decision log write failed (MSG-P7-003) |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header, kept 24 hours per user; a repeat returns the first response |

**GET /cases/{caseId}/documents**

| Item | Value |
|---|---|
| Request | Query type, page, size (api.yaml) plus dateFrom and dateTo (date, see additions); size default 20, maximum 100 |
| Response | 200 DocumentPage: items (Document), page, size, total; only active versions |
| Errors | 401; 403 (MSG-P4-002, MSG-P4-003); 404 case not found; 422 dateFrom after dateTo (MSG-GEN-003); 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

**GET /cases/{caseId}/document-checklist** (new, see additions)

| Item | Value |
|---|---|
| Request | Path caseId |
| Response | 200 DocumentChecklist: caseId, checklistVersion (here the type table version), items [documentType, label, required, presentCount], missingCount, complete |
| Errors | 401; 403 (MSG-P4-002, MSG-P4-003); 404; 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

The placeholder returns required = false for every item, missingCount 0 and complete null until RWB-E1-040 sets the required items.

## 13. Solution plan

**Package.** Folder `recovery/dochub/casedocs`, Java package `recovery.dochub.casedocs`; front end folder `recovery/documents`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| DocumentHubController | Controller | Adds POST and GET /cases/{caseId}/documents and GET /cases/{caseId}/document-checklist |
| CaseDocumentUploadService | Service | Intake container write, malware scan call, DocumentStore.store, idempotency key handling |
| CaseDocumentQueryService | Service | List and search by case, type and stored date with paging |
| ChecklistPlaceholderService | Service | Builds the six-type placeholder from DocumentTypeCatalog and the counts per type |
| CaseDocumentQueryRepository | Repository | Reads document only, filtered by case, type, active flag and created_at |
| CaseDocumentsTab | React component | SCR-30 with the list, the search bar and the checklist placeholder |
| UploadDocumentDialog | React component | File picker, type list from LOV-DOC-TYPE, size check, error display |

**Database.**
- Reads document (id, case_id, document_type, source, retention_class, write_once, doc_version, is_active, created_at, content_sha256).
- Uses the index ix_document_case_type_created from RWB-E1-024. No new table.

**Configuration and reference data.**
- Document type table (RWB-E1-025); document hub parameters INTAKE_MAX_FILE_MB and INTAKE_ALLOWED_TYPES (RWB-E1-024).
- Property rwb.dochub.casedocs.page-size = 20.

**Build steps.**
1. Extend the list endpoint with dateFrom and dateTo and the date order check; API tests for AC2, AC9, AC10 and AC11.
2. Build CaseDocumentUploadService with the scan call and the store call; integration tests for AC1, AC4, AC5 and AC6.
3. Add the duplicate response and the Idempotency-Key handling; tests for AC7 and AC8.
4. Build ChecklistPlaceholderService and the checklist endpoint; test AC3.
5. Build CaseDocumentsTab and UploadDocumentDialog with the states Loading, list, upload, empty and error; component tests for each state.
6. Browser test of upload to list within 5 seconds in SIT, and the access test.

**Feature flag.** `rwb.dochub.casedocs`. Off: the Documents tab is hidden and the endpoints return 404.

**Done when.** The tests in section 16 pass and a 2 MB upload shows in the list within 5 seconds in SIT.

## 14. Validation and messages

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

Thai text for each message follows decision DL10.

## 15. Screens and states

SCR-30 Case documents, reached from SCR-03 Case record.

| State | What the user sees and does |
|---|---|
| Loading | Skeleton rows while the list and the checklist load |
| list | Documents with type, stored date, source, version and the write-once label; search bar with type and date range; checklist placeholder with the six types |
| upload | Upload dialog with file, document type and the size limit; errors from section 14 next to the field |
| Empty | "No documents match this search." with the action "Clear the search" (common state) |
| Error | The message from section 14 at the top |

The Upload button shows only to roles with Documents C.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-026-01 | AC1, BR1 | System | Synthetic 2 MB court notice PDF |
| TC-E1-026-02 | AC2, BR4 | System | Case with 50 synthetic documents, 12 court notices, 4 in October 2026 |
| TC-E1-026-03 | AC3, BR5 | System | Case with 12 court notices and 1 appraisal report |
| TC-E1-026-04 | AC4, BR1 | System | Upload without a type |
| TC-E1-026-05 | AC5, BR2 | System | EICAR test file |
| TC-E1-026-06 | AC6 | System | Spreadsheet file |
| TC-E1-026-07 | AC7, BR6 | System | Same PDF uploaded twice |
| TC-E1-026-08 | AC8, BR6 | System | Two requests with Idempotency-Key TEST-KEY-0001 |
| TC-E1-026-09 | AC9 | System | Date range 31 October to 1 October 2026 |
| TC-E1-026-10 | AC10 | System | Search for TITLE_DEED on a case without one |
| TC-E1-026-11 | AC11, BR3 | System | Case owner with scope OWN on another owner's case |
| TC-E1-026-12 | Access | Access | Team manager (RW-TEAMMGR, Documents R only) uploads; refused with MSG-P4-002 |
| TC-E1-026-13 | Principle 5 | Resilience | Decision log write forced to fail during an upload; nothing stored, MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the type list, size limit, file types and page size are data or properties.
- No personal data in logs, tests or prompts. File names in logs are replaced by the document ID.
- No read of another module's tables: the case and the scope come through CaseDirectory and the ACE access check.
- The front end size check does not replace the server check.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-008 | Documents searchable by case ID, type and date from the case record view | Business Requirements Epic 1, section 3.5 | FEAT-DCM-05 | 13 Manage documents and correspondence | None | TC-E1-026-02, TC-E1-026-03, TC-E1-026-09, TC-E1-026-10, TC-E1-026-11 |
| REQ-DCM-001 | Every document stored against its case with type, date and source | Business Requirements Epic 1, section 3.5 | FEAT-DCM-04 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-026-01, TC-E1-026-04 to TC-E1-026-08, TC-E1-026-12, TC-E1-026-13 |

## 19. Out of scope

- Required items per case type and the completeness flag (RWB-E1-040).
- Search across cases and free text search (RWB-E1-033).
- Search on extracted fields within a case (RWB-E1-033 builds the field filter).
- OCR, classification and extraction of an uploaded file (RWB-E1-049, RWB-E1-050, RWB-E1-053).
- Upload from the field app (RWB-E2-024) and from partners (Epic 5, DL03).

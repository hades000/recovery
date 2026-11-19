<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 032 Automatic attach from the OCR intake v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 032 Automatic attach from the OCR intake v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-032 Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-032 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-12 Attach an OCR-read document to its case automatically |
| Requirement IDs | REQ-DCM-007 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-024, RWB-E1-050, RWB-E1-053 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **documents from the OCR intake attached to their case automatically when the case ID or the account number is read, with unmatched or ambiguous documents held for a person who sees the OCR text and the candidate cases and attaches the document**, so that **no document is filed by hand when the case is clear and none is filed on the wrong case when it is not**.

## 2. Business rationale

Scans, partner files and emails arrive without a case link; today a person reads each one and files it. This story matches each classified intake item to one open case by the case ID or the account number in its text and stores it on that case with no person involved (FSD P5 A2.12). An item that matches no case, more than one case, a closed case or no agreed type is held as unmatched, and a person attaches it from the review queue with the OCR text and the candidates in front of them. It meets REQ-DCM-007 and writes the document attached record required from Epic 1 (REQ-DRI-004, RWB-E1-027). The measure is fields extracted without review (FSD P5 A2.12.1).

## 3. Preconditions

- RWB-E1-024 is done: DocumentStore stores a document and writes the DOCATT decision log entry.
- RWB-E1-050 is done: intake items carry predicted_type, classification_confidence, type_candidates, classifier_version and review_reason.
- RWB-E1-053 is done: the extracted fields case_no and account_no are available for an item where they were read.
- Parameters loaded in document_hub_parameter: CASE_NO_PATTERN = "RW-[0-9]{4}-[0-9]{6}", ACCOUNT_NO_PATTERN = "[0-9]{10}" (assumed; DL21) and CLASSIFY_THRESHOLD = 0.80.
- The P3 published interface CaseDirectory returns a case by case number and the open cases for an account number.
- A person resolving unmatched items holds Documents C; items with no candidate are visible only to roles with scope ALL.
- Feature flag rwb.dochub.autoattach is on.

## 4. Flow

1. JOB-12 Document intake: runs matchStep after the extraction step.
2. MatchStep: selects intake items with ocr_status DONE, match_status PENDING, no document_id and a predicted type (review_reason empty or LOW_CONFIDENCE), locking each row; items with review_reason UNKNOWN_TYPE or MODEL_UNAVAILABLE get match_status NO_TYPE and are held for a person.
3. CaseMatcher: collects case numbers from the extracted field case_no and from the OCR text with CASE_NO_PATTERN, and account numbers from the extracted field account_no and the text with ACCOUNT_NO_PATTERN.
4. CaseMatcher: resolves each case number with CaseDirectory.findByCaseNo and each account number with CaseDirectory.findOpenCasesByAccountNo, and returns one of MATCHED, NO_MATCH, MULTIPLE, CONFLICT or CASE_CLOSED with the candidates.
5. MatchStep: for MATCHED, calls DocumentStore.store with the case ID, predicted_type, the intake source, the file, its hash and the extracted fields; the store writes the DOCATT entry with the classifier version, the confidence and the match method, the document row and DocumentStored.
6. MatchStep: on the stored document sets classification_confidence, document_type and type_candidates; for review_reason LOW_CONFIDENCE sets review_status PENDING and write_once false, so it is held in rwb-docs and listed on SCR-31 (RWB-E1-054).
7. MatchStep: sets the intake item match_status MATCHED, case_id and document_id; for any other result sets match_status to the result and candidate_case_ids, and the item is held for a person.
8. Reviewer: opens the Unmatched list on SCR-31 (GET /intake-items), opens an item to see the scan, the OCR text and the candidates, picks the case and the type, and attaches it (POST /intake-items/{intakeItemId}/attach).
9. ManualAttachService: checks the case is in the reviewer's scope and the type is in force, calls DocumentStore.store with the reviewer as approver on the DOCATT entry, and sets the item match_status MATCHED.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No readable case ID or account number | Item held, match_status NO_MATCH, OCR text held for the reviewer | MSG-P5-003 | AC2 |
| X2 | The account number matches two or more open cases | Item held, match_status MULTIPLE, every candidate offered | MSG-P5-003 | AC3 |
| X3 | The case ID and the account point to different cases | Item held, match_status CONFLICT, both cases offered | MSG-P5-003 | AC5 |
| X4 | A case ID is read that does not exist | No candidate; NO_MATCH | MSG-P5-003 | AC6 |
| X5 | The only candidate case is closed | Item held, match_status CASE_CLOSED | MSG-P5-003 | AC7 |
| X6 | The same file is already on the matched case | The item is linked to the existing document; no second document | None | AC8 |
| X7 | The job runs again over attached items | No second attach, entry or event | None | AC9 |
| X8 | Classification confidence below the threshold and one case matched | Stored with review_status PENDING and write_once false | MSG-P5-003 | AC10 |
| X9 | No agreed type from classification | Item held, match_status NO_TYPE | MSG-P5-003 | AC11 |
| X10 | The reviewer picks a case outside their scope | Refused with 403; item stays held | MSG-P4-003 | AC13 |
| X11 | The reviewer picks a type not in force | Refused with 422 | MSG-P5-006 | AC14 |
| X12 | Two reviewers attach the same item at the same time | The first succeeds; the second gets 409 | MSG-GEN-004 | AC15 |
| X13 | The decision log write fails during an attach | Nothing stored; an automatic attach stays PENDING for the next run; a manual attach returns 503; incident raised (R-UNI-39) | MSG-P7-003 | TC-E1-032-17 (Principle 5) |
| X14 | A role without Documents C attaches an item | Refused with 403 | MSG-P4-002 | TC-E1-032-16 (Access) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-E1-024), classification (RWB-E1-050) and extraction (RWB-E1-053), all earlier in Epic 1 |
| Negotiable | The patterns are data; the match outcomes and the reviewer action are fixed by the story |
| Valuable | Ends hand filing for every scan that names its case or account, and gives every other scan one place to be filed |
| Estimable | One job step, one matcher, four endpoints, one list tab |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake

  Background:
    Given case "RW-2026-000123" is open, owned by "TEST-CO-01" and linked to account "TEST-ACC-0001"
    Given case "RW-2026-000456" is open and linked to account "TEST-ACC-0002"
    Given case "RW-2026-000789" is closed
    Given parameter CLASSIFY_THRESHOLD is 0.80

  Scenario: AC1 Auto attach
    Given a scanned notice with the case ID "RW-2026-000123" read by OCR, classified "COURT_NOTICE" at 0.93 by classifier version "CLS-1.0"
    When intake completes
    Then the system stores the document on case "RW-2026-000123" with type "COURT_NOTICE", source "SCAN", classification_confidence 0.9300 and review_status "NOT_NEEDED" without a person
    Then one decision log entry "DOCATT" holds model version "CLS-1.0", confidence 0.93 and match method "CASE_ID"
    Then the system writes documentStored and the intake item has match_status "MATCHED" and the document ID

  Scenario: AC2 No match
    Given a scan with no readable case ID and no readable account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"
    Then GET /intake-items/{intakeItemId} returns its OCR text pages
    Then the system writes no document row

  Scenario: AC3 Two candidates
    Given a scan whose account number "TEST-ACC-0003" is linked to open cases "RW-2026-000321" and "RW-2026-000654"
    When intake completes
    Then the intake item has match_status "MULTIPLE"
    Then candidate_case_ids holds both cases and the Unmatched list on SCR-31 offers both
    Then the system writes no document row

  Scenario: AC4 Match by account number
    Given a scan with no case ID and the account number "TEST-ACC-0002", classified "DEMAND_LETTER" at 0.88
    When intake completes
    Then the system stores the document on case "RW-2026-000456"
    Then the decision log entry holds match method "ACCOUNT_NO"

  Scenario: AC5 Case ID and account disagree
    Given a scan with the case ID "RW-2026-000123" and the account number "TEST-ACC-0002"
    When intake completes
    Then the intake item has match_status "CONFLICT" and candidates "RW-2026-000123" and "RW-2026-000456"

  Scenario: AC6 Case ID that does not exist
    Given a scan with the case ID "RW-2026-999999" and no account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"

  Scenario: AC7 Only candidate is closed
    Given a scan with the case ID "RW-2026-000789"
    When intake completes
    Then the intake item has match_status "CASE_CLOSED" and candidate "RW-2026-000789"
    Then the system writes no document row

  Scenario: AC8 The same file is already on the case
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    Given a second intake item holds the same file with the same hash
    When intake completes
    Then the second item has match_status "MATCHED" and the document ID from AC1
    Then the case holds one copy of that court notice and one "DOCATT" entry for it

  Scenario: AC9 Repeat run
    Given 15 intake items already "MATCHED"
    When JOB-12 runs again
    Then no further document row, decision log entry or DocumentStored event is written for them

  Scenario: AC10 Low classification confidence with one case
    Given a scan with the case ID "RW-2026-000123" classified "APPRAISAL_REPORT" at 0.62 with candidates APPRAISAL_REPORT 0.62 and TITLE_DEED 0.30
    When intake completes
    Then the system stores the document on case "RW-2026-000123" with review_status "PENDING", write_once false and the file in "rwb-docs"
    Then the document carries document_type "APPRAISAL_REPORT" and both candidates for SCR-31

  Scenario: AC11 No agreed type
    Given a scan with the case ID "RW-2026-000123" and review_reason "UNKNOWN_TYPE" from classification
    When intake completes
    Then the intake item has match_status "NO_TYPE" with candidate "RW-2026-000123"

  Scenario: AC12 A reviewer attaches an unmatched item
    Given the item from AC3 and reviewer "TEST-LIT-01" holding RW-LITOFF with both candidate cases in scope
    When "TEST-LIT-01" attaches it to "RW-2026-000654" with type "GUARANTOR_NOTICE"
    Then the system stores the document on "RW-2026-000654" with type "GUARANTOR_NOTICE"
    Then the "DOCATT" entry names "TEST-LIT-01" as approver and match method "PERSON"
    Then the intake item has match_status "MATCHED"

  Scenario: AC13 Reviewer picks a case outside their scope
    Given reviewer "TEST-LIT-02" whose scope does not include case "RW-2026-000654"
    When "TEST-LIT-02" attaches the item from AC3 to "RW-2026-000654"
    Then the system refuses the request with 403 and MSG-P4-003
    Then the item keeps match_status "MULTIPLE"

  Scenario: AC14 Reviewer picks a type not in force
    Given the item from AC2 and a reviewer with scope ALL
    When the reviewer attaches it to "RW-2026-000123" with type "PAYSLIP"
    Then the system refuses the request with 422 and MSG-P5-006 naming "PAYSLIP"

  Scenario: AC15 Two reviewers attach the same item
    Given the item from AC2 at version 3
    When two reviewers attach it at the same time with version 3
    Then one request returns 201 and the other returns 409 with MSG-GEN-004
    Then one document row exists for the item
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A classified document attaches to its case without a person when exactly one open case is found | REQ-DCM-007; FEAT-DCM-12 |
| BR2 | The case is found by the case ID or the account number read from the document; the account number is the join to other systems | DL21; parameters CASE_NO_PATTERN and ACCOUNT_NO_PATTERN in document_hub_parameter (New) |
| BR3 | No match, more than one candidate, disagreement, a closed case or no agreed type goes to a person | REQ-DCM-005; FSD P5 A2.12.4 |
| BR4 | A document classified below the threshold is stored for review in the standard container, not write-once, until a person confirms its type | Parameter CLASSIFY_THRESHOLD in document_hub_parameter (New); RWB-E1-054; CTL-12 |
| BR5 | Each attach is written to the decision log with the classifier version, the confidence and the person where one decided, before the document is stored | Principle 5; R-UNI-39; REQ-DRI-004 |
| BR6 | An item attached once is not attached again | R-UNI-40 |
| BR7 | A reviewer attaches only to a case in their scope | CTL-09 |

## 9. State transitions

None. This story does not change a case status. It changes the intake item match_status: PENDING to MATCHED on an automatic attach; PENDING to NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED or NO_TYPE when held for a person; a held value to MATCHED when a reviewer attaches it. It creates a document record (COPY_PENDING, then STORED, in RWB-E1-024).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Matches and attaches automatically (Documents C) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry |
| Roles with Documents C and the candidate case in scope (for example RW-LITOFF, RW-CASEOWN) | See and attach unmatched items that name a candidate in their scope |
| Roles with Documents C and scope ALL (for example RW-LEGAL) | See and attach unmatched items with no candidate |
| Roles with Documents R only (for example RW-TEAMMGR) | See attached documents on cases in their scope; no attach |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-CAS-002 | recovery_case | case_no | Read, through CaseDirectory |
| DF-CAS-005 | recovery_case | status | Read, through CaseDirectory |
| DF-CAS-026 | case_account | account_id | Read, through CaseDirectory |
| DF-ACC-002 | loan_account | account_no | Read, through CaseDirectory |
| DF-DOC-001 to DF-DOC-011 | document | all fields | Write, through DocumentStore |
| DF-DOC-007 | document | classification_confidence | Write |
| DF-DOC-008 | document | review_status | Write |
| DF-DOC-010 | document | write_once | Write |
| DF-DOC-004 | document | document_type | Write |
| DF-DOC-007 | document | classification_confidence | Write |
| DF-DOC-075 | document_intake | match_status | Write |
| DF-DOC-076 | document_intake | candidate_case_ids | Write |
| DF-DOC-060 | document_intake | case_id | Write |
| DF-DOC-061 | document_intake | document_id | Write |
| DF-DOC-070 | document_intake | predicted_type | Read |
| DF-DOC-073 | document_intake | classifier_version | Read |
| DF-DOC-080 | document_intake | review_reason | Read |
| DF-DOC-056 | document_intake | file_sha256 | Read |
| DF-DOC-089 | document_text | text_content | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DocumentStore and DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake, step matchStep after the extraction step |
| Job name | JOB-12 Document intake |
| Schedule | Every 15 minutes in business hours |
| Input | Intake items with ocr_status DONE, match_status PENDING, no document_id and a predicted type |
| Output | Documents stored on their case; held items with match status and candidates; counts on the job record |
| Events published | DocumentStored (EV-16), through DocumentStore |
| Idempotency key | Intake item ID, and in the store the case, type and file hash |
| Restart behavior | Items left PENDING are matched in the next run; an attach that failed on the decision log stays PENDING |

**GET /review-items** (new, see additions)

| Item | Value |
|---|---|
| Request | Query matchStatus (default the held values NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE), page, size (default 50) |
| Response | 200 IntakeItemPage: items [id, source, receivedAt, matchStatus, predictedType, classificationConfidence, typeCandidates, candidateCases (caseId, caseNo), version], page, size, total; oldest first; only items whose candidates are in scope, and items with no candidate for scope ALL |
| Errors | 401; 403 no Documents R (MSG-P4-002); 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

**GET /intake-items/{intakeItemId}** and **GET /intake-items/{intakeItemId}/content** (new, see additions)

| Item | Value |
|---|---|
| Request | Path intakeItemId |
| Response | 200 IntakeItem with pages [pageNo, text] (personal identifiers masked by role); content returns the file |
| Errors | 401; 403 (MSG-P4-002, MSG-P4-003); 404; 503 |
| Authorization | Documents, right R, scope applied; each read written to the PII access log |
| Idempotency | Not applicable |

**POST /intake-items/{intakeItemId}/resolve** (new, see additions)

| Item | Value |
|---|---|
| Request | IntakeAttachRequest: caseId (uuid, required), documentType (required), version (integer, required) |
| Response | 201 Document |
| Errors | 401; 403 no Documents C (MSG-P4-002) or case out of scope (MSG-P4-003); 404; 409 item no longer held or version changed (MSG-GEN-004); 422 type not in force (MSG-P5-006) or missing field (MSG-GEN-001); 503 decision log write failed (MSG-P7-003) |
| Authorization | Documents, right C, scope applied to the chosen case |
| Idempotency | Idempotency-Key header; a repeat returns the first result |

**Published interfaces called**

```java
// P3
Optional<CaseSummary> findByCaseNo(String caseNo);                 // id, caseNo, status, ownerUserId
List<CaseSummary> findOpenCasesByAccountNo(String accountNo);
// P5, RWB-E1-024
StoredDocument store(StoreRequest request);                         // request carries approverUserId for a manual attach
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/attach`, Java package `recovery.dochub.attach`; front end folder `recovery/documents`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| MatchStep | Job | Step of JOB-12: select, match, store or hold for a person |
| CaseMatcher | Service | Reads case numbers and account numbers; resolves them through CaseDirectory; returns the result and candidates |
| MatchPatterns | Rule table | Reads the two pattern parameters from document_hub_parameter |
| AutoAttachService | Service | Builds the StoreRequest with the classification inputs; applies the review rule of BR4; updates the intake item |
| ManualAttachService | Service | Scope and type checks, optimistic lock on the item, store with the approver |
| IntakeItemController | Controller | The four intake item endpoints |
| IntakeItemRepository | Repository | Reads and writes document_intake only (table from RWB-E1-049) |
| UnmatchedIntakeTab | React component | Unmatched list on SCR-31 with the scan viewer, OCR text, candidates, case picker and type picker |

**Database.**
- Flyway migration `V1_5_032__intake_match.sql` adds to document_intake: match_status varchar(12) default 'PENDING', candidate_case_ids jsonb. The document columns document_type and type_candidates come from the RWB-E1-050 migration.
- Index ix_intake_held on document_intake (match_status, received_at) where match_status not in ('PENDING', 'MATCHED').

**Configuration and reference data.**
- Parameters CASE_NO_PATTERN, ACCOUNT_NO_PATTERN and CLASSIFY_THRESHOLD in document_hub_parameter, loaded by the reference data administrator.
- No rule row; the match outcomes are the story's fixed behavior.

**Build steps.**
1. Write the migration; test the columns and the index.
2. Build MatchPatterns and the text scan; unit test pattern reads on synthetic text with Thai and English around the numbers.
3. Build CaseMatcher with the five outcomes against a CaseDirectory stub; unit test AC2 to AC7.
4. Build AutoAttachService with the store call, the review rule and the item update; integration test AC1, AC4, AC8, AC10 and AC11.
5. Build MatchStep selection and skip rules; test AC9.
6. Build IntakeItemController and ManualAttachService; API tests AC12 to AC15 and the access test.
7. Build UnmatchedIntakeTab; component tests for list, detail and attach.
8. Test the decision log failure path for the automatic and the manual attach.

**Feature flag.** `rwb.dochub.autoattach`. Off: matchStep sets every classified item to match_status NO_MATCH, and reviewers attach them by hand.

**Done when.** The tests in section 16 pass and, on the 180 synthetic samples in SIT, every item with one readable case ID and a confidence at or above 0.80 is attached in the same run.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | Item held for a person or document stored for review | Some fields need checking. The document is in the review queue. |
| MSG-P5-006 | Reviewer picks a type not in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-GEN-001 | Case or type missing on attach | Enter {field}. |
| MSG-GEN-004 | Item attached by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Chosen case outside the scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

## 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the Unmatched list loads |
| SCR-31 Document review queue | list | The Unmatched tab: items oldest first with source, received time, match status, proposed type and candidate cases |
| SCR-31 Document review queue | reviewed | The item is attached; it leaves the list and the document opens on SCR-30 of the chosen case |
| SCR-30 Case documents | list | An automatically attached document shows on its case; a PENDING document shows MSG-P5-003 |

The tab for documents pending type or field review on SCR-31 is built in RWB-E1-054.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-032-01 | AC1, BR1, BR5 | System | Synthetic notice with RW-2026-000123 at 0.93 |
| TC-E1-032-02 | AC2, BR3 | System | Synthetic scan with no identifiers |
| TC-E1-032-03 | AC3, BR3 | System | Account TEST-ACC-0003 on two open cases |
| TC-E1-032-04 | AC4, BR2 | System | Account TEST-ACC-0002 only |
| TC-E1-032-05 | AC5, BR3 | System | Case ID and account on different cases |
| TC-E1-032-06 | AC6, BR3 | System | Case ID RW-2026-999999 |
| TC-E1-032-07 | AC7, BR3 | System | Closed case RW-2026-000789 |
| TC-E1-032-08 | AC8, BR6 | System | Same file in two intake items |
| TC-E1-032-09 | AC9, BR6 | System | 15 items already MATCHED |
| TC-E1-032-10 | AC10, BR4 | System | Scan classified APPRAISAL_REPORT at 0.62 on a matched case |
| TC-E1-032-11 | AC11, BR3 | System | Item with review_reason UNKNOWN_TYPE |
| TC-E1-032-12 | AC12, BR5 | System | Reviewer attaches a MULTIPLE item |
| TC-E1-032-13 | AC13, BR7 | System | Reviewer with a scope that excludes the chosen case |
| TC-E1-032-14 | AC14 | System | Type PAYSLIP |
| TC-E1-032-15 | AC15 | System | Two parallel attach requests at version 3 |
| TC-E1-032-16 | Access | Access | Team manager (RW-TEAMMGR, Documents R only) attaches an unmatched item; refused with MSG-P4-002 |
| TC-E1-032-17 | Principle 5 | Resilience | Decision log write forced to fail during an automatic and a manual attach; nothing stored, MSG-P7-003, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the case number and account number patterns and the threshold are parameters.
- No personal data in logs, tests or prompts: account numbers and OCR text are never logged; logs carry the intake ID and the outcome; test accounts are synthetic.
- No read of another module's tables: cases and accounts are resolved through CaseDirectory.
- The matcher never picks one of several candidates; any doubt goes to a person.
- A document stored for type review is never put in the write-once container before its type is confirmed (RWB-E1-054).

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-032-01 to TC-E1-032-17 |

## 19. Out of scope

- Confirming or correcting the type and the fields of a document stored for review (RWB-E1-054).
- Source pickup from scanners, SFTP and mailboxes, and the intake item base record (RWB-E1-057).
- Moving an attached document to another case (Epic 2).
- Attach of field app photos (RWB-E2-024).

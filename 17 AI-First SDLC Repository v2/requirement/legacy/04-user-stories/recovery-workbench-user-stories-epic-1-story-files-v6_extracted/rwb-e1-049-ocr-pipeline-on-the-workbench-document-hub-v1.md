<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 049 OCR pipeline on the Workbench document hub v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 049 OCR pipeline on the Workbench document hub v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-049 OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-049 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-07 Run the OCR pipeline on inbound documents |
| Requirement IDs | REQ-DCM-006, REQ-DCM-009 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Must |
| Depends on | RWB-TE-012, RWB-E1-024, RWB-E1-045 |
| Status | Ready for build |

## 1. Story

As a **case owner (RW-CASEOWN)**, I want **every inbound scan and upload read by the OCR service into text and layout in Thai and English, stored against the intake item and the document**, so that **classification and extraction can start and an unreadable page is sent back for rescan the same day**.

## 2. Business rationale

Scanned documents arrive as images; nothing in them can be classified, extracted or searched until the text is read (FSD P5 A2.7). This story builds the OCR step of the document intake: one intake record per file, the text and layout of every page, a quality check per page and a rescan request when a page cannot be read. It meets REQ-DCM-006 (fields extracted in Thai and English, which needs Thai and English text first) and REQ-DCM-009 (every path ends in the same intake). The measure is fields extracted without review (FSD P5 A2.7.1).

## 3. Preconditions

- RWB-E1-024 is done: documents are stored and DocumentStored (EV-16) is published.
- RWB-TE-012 is done: the intake and standard containers exist.
- RWB-E1-045 is done: product parameters are held as data.
- Document hub parameters loaded: OCR_MIN_QUALITY = 0.70, OCR_WORKERS = 4, OCR_TIMEOUT_SECONDS = 120, OCR_MAX_ATTEMPTS = 3 (all assumed, DL11).
- The OCR service run by Autonomous Ops is reachable from SIT through the OcrClient adapter under the service identity SY-OCR.
- An intake item has scan_result CLEAN. The malware scan step is added in RWB-E1-041; until then test data is seeded CLEAN.
- Feature flag rwb.dochub.ocr is on.

## 4. Flow

1. JOB-12 Document intake: starts every 15 minutes in business hours and runs the OCR step after the intake and scan steps.
2. DocumentStoredListener: for each DocumentStored event with source UPLOAD, creates an intake item with the case ID, the document ID and scan_result CLEAN (the upload was scanned before storage).
3. OcrStep: selects intake items with scan_result CLEAN and ocr_status PENDING, oldest first, locking each row so that no two workers take the same item; runs up to OCR_WORKERS items in parallel.
4. OcrClient: sends the file to the OCR service with the languages Thai and English and receives, per page, the lines, words, positions, language and word confidence.
5. OcrStep: computes the page quality as the mean word confidence of the page; stores the full output as JSON at ocr/{intakeId}.json in the standard container and sets ocr_ref.
6. OcrStep: writes one document_text row per page with the page text and quality, with the document ID where the item is already attached.
7. OcrStep: if every page has quality at or above OCR_MIN_QUALITY, sets ocr_status DONE; otherwise sets ocr_status RESCAN and rescan_pages to the page numbers below the threshold.
8. OcrStep: for an item in RESCAN with a known case, sends MSG-P5-018 to the case owner through the ACE notification path; for an item with no case, sets review_reason RESCAN so the item shows in the document review queue (SCR-31, RWB-E1-054).
9. OcrStep: records the run counts (read, done, rescan, failed) on the job record shown in the job monitor.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A page has quality below OCR_MIN_QUALITY | Item set RESCAN with the page numbers; case owner told, or the item goes to the review queue | MSG-P5-018 | AC3, AC4 |
| X2 | Page quality exactly at OCR_MIN_QUALITY | The page is accepted | None | AC5 |
| X3 | The OCR service does not answer within OCR_TIMEOUT_SECONDS or returns an error | ocr_attempts increases; the item stays PENDING for the next run; after two failed runs the job raises an alert to the platform administrator (JOB-12) | None | AC6 |
| X4 | The item fails OCR_MAX_ATTEMPTS times or the file cannot be opened | ocr_status FAILED; review_reason UNREADABLE_FILE; item in the review queue | None | AC7 |
| X5 | The job runs again over items already DONE | Items are not read again; no second set of text rows | None | AC8 |
| X6 | Two workers start on the same item | The row lock lets one worker take it; the other skips it | None | AC9 |
| X7 | A user without the Documents right reads a document holding OCR text | Refused with 403; no text returned | MSG-P4-002 | TC-E1-049-10 (Access) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-E1-024) and the containers (RWB-TE-012); classification (RWB-E1-050) and extraction (RWB-E1-053) build on its output |
| Negotiable | Quality threshold, workers, timeout and attempts are parameters; the OCR service can change behind OcrClient |
| Valuable | Every scan becomes text that the later steps and the search read |
| Estimable | One table pair, one job step, one adapter, one listener |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: OCR pipeline on the Workbench document hub

  Background:
    Given OCR_MIN_QUALITY is 0.70, OCR_WORKERS is 4 and OCR_MAX_ATTEMPTS is 3
    Given the OCR service stub in SIT is replaced by the OCR service for AC1 and AC2

  Scenario: AC1 Sample processed
    Given the 180 synthetic sample documents, 30 of each of the six agreed types, in Thai and English, each as a CLEAN intake item
    When JOB-12 Document intake runs
    Then each of the 180 items has ocr_status "DONE" or "RESCAN" and an ocr_ref to its JSON output
    Then each page has a document_text row with the page text and its quality
    Then the text of the sample pages holds Thai and English words, and the languages recorded per item are "th" and "en" where both appear

  Scenario: AC2 Throughput
    Given 500 pages in 125 CLEAN intake items in SIT
    When they are processed by JOB-12 with 4 workers
    Then all 125 items reach "DONE" or "RESCAN" within 60 minutes of the first item starting

  Scenario: AC3 Unreadable page on a known case
    Given an uploaded court notice of 4 pages on case "RW-2026-000123" owned by user "TEST-CO-01"
    Given page 3 has quality 0.41 and the other pages are above 0.70
    When the OCR step runs
    Then the intake item has ocr_status "RESCAN" and rescan_pages "3"
    Then "TEST-CO-01" receives MSG-P5-018 naming page 3, the document and case "RW-2026-000123"

  Scenario: AC4 Unreadable page with no case yet
    Given a mailroom scan of 2 pages with no case and page 1 at quality 0.30
    When the OCR step runs
    Then the intake item has ocr_status "RESCAN", rescan_pages "1" and review_reason "RESCAN"
    Then the system sends no notification

  Scenario: AC5 Quality at the threshold
    Given a scan of 1 page with quality 0.70
    When the OCR step runs
    Then the item has ocr_status "DONE" and no rescan pages

  Scenario: AC6 OCR service unavailable
    Given the OCR service stub returns HTTP 503 for every call
    When JOB-12 runs twice
    Then each pending item has ocr_status "PENDING" and ocr_attempts 2
    Then the job monitor shows the OCR step failed in both runs and an alert is raised to the platform administrator
    Then when the service answers again the next run sets the items "DONE"

  Scenario: AC7 File that cannot be read
    Given a password-protected PDF as a CLEAN intake item
    When the OCR step runs
    Then the item has ocr_status "FAILED" and review_reason "UNREADABLE_FILE"
    Then no document_text row exists for it

  Scenario: AC8 Repeat run
    Given 10 intake items already "DONE" with 25 document_text rows
    When JOB-12 runs again
    Then the OCR service receives no call for those items
    Then they still have 25 document_text rows

  Scenario: AC9 Two workers on one item
    Given one CLEAN pending item and 4 workers starting at the same time
    When the OCR step runs
    Then the OCR service receives exactly one call for the item
    Then the item has one set of document_text rows
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every inbound file is read in Thai and English | REQ-DCM-006; FEAT-DCM-07 |
| BR2 | Scans, partner files, emails and uploads go through the same intake item and OCR step | REQ-DCM-009 |
| BR3 | A file is read only after its malware scan is CLEAN | REQ-DCM-010; FEAT-DCM-18 |
| BR4 | A page below OCR_MIN_QUALITY is sent for rescan; the threshold is inclusive | Document hub parameter OCR_MIN_QUALITY (New); DL11 |
| BR5 | A system that does not answer is retried on the next run and alerted after two failed runs | R-UNI-33; JOB-12 |
| BR6 | An item read once is not read again | R-UNI-40 |
| BR7 | Worker count, timeout and attempts are parameters | Principle 1; DT02 |

## 9. State transitions

None. This story does not change a case status. It changes the intake item OCR status: PENDING to DONE when every page passes; PENDING to RESCAN when a page is below the threshold; PENDING stays PENDING after a failed call below the attempt limit; PENDING to FAILED at the attempt limit or for a file that cannot be opened.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Reads intake files, writes OCR output and text rows (Documents CRU) |
| RW-CASEOWN | Receives the rescan notice for their case |
| RW-PLATADM, platform administrator | Sees the job counts and alerts in the job monitor; reruns JOB-12 |
| Roles with Documents R | Read the OCR text of documents in their scope through RWB-E1-033 |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-005 | document | source | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read, through CaseDirectory |
| DF-DOC-045 to DF-DOC-084 | document_intake | all fields | Write (this story creates the record) |
| DF-DOC-085 to DF-DOC-090 | document_text | all fields | Write (this story creates the record) |
| DF-REF-246 | document_hub_parameter | param_value | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz schedule of JOB-12 Document intake |
| Job name | JOB-12 Document intake; this story adds the step ocrStep |
| Schedule | Every 15 minutes in business hours, Asia/Bangkok |
| Input | Intake items with scan_result CLEAN and ocr_status PENDING |
| Output | OCR JSON per item in the standard container; document_text rows; ocr_status per item; run counts on the job record |
| Events consumed | DocumentStored (EV-16), source UPLOAD, creates the intake item |
| Events published | None |
| Idempotency key | Intake item ID; an item not PENDING is not read |
| Restart behavior | A stopped run leaves unfinished items PENDING; the next run or a rerun from the job monitor (POST /api/recovery/v1/admin/jobs/{jobId}/rerun) picks them up |

**Published interface (P5, used by RWB-E1-050, RWB-E1-053 and RWB-E1-033)**

```java
public interface OcrOutputReader {
    Optional<OcrResult> forIntake(UUID intakeId);          // status, pages with text, quality, languages, ocrRef
    List<PageText> pagesForDocument(UUID documentId);
}
```

**Adapter (P5 to the OCR service)**

```java
public interface OcrClient {
    OcrResponse read(BlobRef file, List<String> languages, Duration timeout);  // throws OcrUnavailableException, UnreadableFileException
}
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/ocr`, Java package `recovery.dochub.ocr`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| DocumentIntakeJob | Job | Spring Batch job behind JOB-12 with ordered steps; this story builds the job and ocrStep |
| OcrStep | Job | Selects, locks and reads items; applies the quality rule; writes output |
| OcrClient, OcrServiceAdapter | Service | Calls the OCR service; maps errors to OcrUnavailableException and UnreadableFileException |
| DocumentStoredListener | Listener | Creates an intake item for each uploaded document |
| RescanNotifier | Service | Sends MSG-P5-018 to the case owner through the ACE notification path |
| DocumentIntakeRepository | Repository | Reads and writes document_intake only |
| DocumentTextRepository | Repository | Writes document_text |
| OcrOutputReader | Published interface | Section 12 |

**Database.**
- Flyway migration `V1_5_049__document_intake.sql` creates document_intake (id, source varchar(12), source_ref varchar(120), received_at timestamptz, file_sha256 char(64), intake_ref varchar(400), scan_result varchar(10), case_id uuid, document_id uuid, ocr_ref varchar(400), ocr_status varchar(12) default 'PENDING', ocr_attempts integer default 0, page_count integer, rescan_pages varchar(200), ocr_quality numeric(5,4), languages varchar(20), ocr_engine_version varchar(40), review_reason varchar(20), plus the standard columns) and document_text (id, intake_id uuid not null, document_id uuid, page_no integer, text_content text, quality numeric(5,4), plus the standard columns).
- Foreign keys document_intake.document_id and document_text.document_id to document(id); document_text.intake_id to document_intake(id).
- Indexes: ix_intake_ocr_pending on document_intake (ocr_status, received_at) where scan_result = 'CLEAN'; unique uk_document_text_page on document_text (intake_id, page_no); ix_document_text_document on document_text (document_id).
- Row selection uses SELECT ... FOR UPDATE SKIP LOCKED.

**Configuration and reference data.**
- Parameters OCR_MIN_QUALITY, OCR_WORKERS, OCR_TIMEOUT_SECONDS, OCR_MAX_ATTEMPTS in document_hub_parameter, loaded by the reference data administrator.
- Property rwb.dochub.ocr.endpoint, set per environment by the platform administrator.
- Notification template for MSG-P5-018 in the ACE notification path, recovery templates.

**Build steps.**
1. Write the migration and the entities; test the unique page index.
2. Build OcrClient against a stub that returns fixed pages; contract test of the response mapping.
3. Build OcrStep selection with SKIP LOCKED and the worker pool; test AC8 and AC9.
4. Add the quality rule and the status setting; test AC3, AC4 and AC5 on synthetic pages.
5. Add retry, attempts and the FAILED rule; test AC6 and AC7.
6. Build DocumentStoredListener and RescanNotifier; test AC3 end to end.
7. Run the 180 sample documents and the 500-page set in SIT against the OCR service; record the results for AC1 and AC2.

**Feature flag.** `rwb.dochub.ocr`. Off: ocrStep is skipped and items stay PENDING.

**Done when.** The tests in section 16 pass and the 500-page run in SIT finishes within 60 minutes.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-018 | A page is below the quality threshold on a document of a known case | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The case owner receives MSG-P5-018 through the ACE notification path. Items with review_reason RESCAN or UNREADABLE_FILE are listed on SCR-31 Document review queue when RWB-E1-054 is built. The platform administrator sees the JOB-12 counts on SCR-44 Interface and job monitor (state Running; failed; complete).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-049-01 | AC1, BR1, BR2 | System | 180 synthetic sample documents, 30 per type, Thai and English |
| TC-E1-049-02 | AC2, BR7 | System | 500 synthetic pages in 125 items in SIT |
| TC-E1-049-03 | AC3, BR4 | System | 4-page upload with page 3 at quality 0.41 |
| TC-E1-049-04 | AC4, BR4 | System | 2-page mailroom scan with no case, page 1 at 0.30 |
| TC-E1-049-05 | AC5, BR4 | System | 1 page at quality 0.70 |
| TC-E1-049-06 | AC6, BR5 | System | OCR stub returning 503 |
| TC-E1-049-07 | AC7 | System | Password-protected synthetic PDF |
| TC-E1-049-08 | AC8, BR6 | System | 10 items already DONE |
| TC-E1-049-09 | AC9 | System | One item, 4 workers |
| TC-E1-049-10 | Access | Access | Capacity and workforce planner (RW-CAPACITY, no Documents right) calls GET /documents/{documentId} on a document with OCR text; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: threshold, workers, timeout and attempts are parameters.
- No personal data in logs, tests or prompts. OCR text is never written to application logs; logs carry the intake ID and counts only. Test documents are synthetic.
- No read of another module's tables: the case owner comes through CaseDirectory.
- OCR text is held only in document_text and the standard container; it is not sent to any service other than the OCR service and the classifier.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted for the agreed types in Thai and English | Business Requirements Epic 1, section 3.5 | FEAT-DCM-07 | 13 Manage documents and correspondence | R-UNI-33 | TC-E1-049-01, TC-E1-049-03, TC-E1-049-04, TC-E1-049-05, TC-E1-049-07 |
| REQ-DCM-009 | Documents from every path through the same intake | Business Requirements Epic 1, section 3.5 | FEAT-DCM-07 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-40 | TC-E1-049-02, TC-E1-049-06, TC-E1-049-08, TC-E1-049-09, TC-E1-049-10 |

## 19. Out of scope

- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057).
- The malware scan step (RWB-E1-041).
- Classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The review queue screen and correction (RWB-E1-054).
- Field app photos and bills (RWB-E2-024).

# RWB-P5-E1049-APP OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1049-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1024-APP |
| Depends on (build) | RWB-P5-E1049-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1024-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P5-E1049-INF, RWB-P5-E1049-OPS, RWB-PLT-TE012-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-013, FR-P5-016, FR-P5-020, FR-P5-022, FR-P5-023, FR-P5-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the OCR step of the document intake moved into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the `DocumentIntakeWorkflow` of the workflow kit and the 15-minute business-hours Schedule that replaces JOB-12. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every inbound scan and upload read by the OCR service into text and layout in Thai and English, stored against the intake item and the document**, so that **classification and extraction can start and an unreadable page is sent back for rescan the same day**.

Inside `rwb-document` this is the OCR pipeline of the document intake:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The pipeline writes `document_intake` and `document_text` in `rwb_document`, reads `document` for the case and source of an attached file, and reads the document-hub parameter rows in `document_hub_parameter`; it reads no table of another service (DP-01).
- The case owner of an unreadable page is read through the `GET /cases/{caseId}` contract of `rwb-case`, one hop with a 2 s timeout and a breaker (DP-11), never from a case table of another service. The contract is consumed and faked although the plan lists it in no C row of this key.
- Parameters `OCR_MIN_QUALITY`, `OCR_WORKERS`, `OCR_TIMEOUT_SECONDS` and `OCR_MAX_ATTEMPTS` are read through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON); the rows they resolve to live in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5.
- Reference lists LOV-OCR-STATUS, LOV-INTAKE-REVIEW, LOV-DOC-SOURCE and LOV-SCAN-RESULT are read through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON); no list value is typed in code.
- The legacy `OcrClient` in-process adapter becomes one outbound client of this service. The OCR engine itself is external: it is the X dependency RWB-P5-E1049-INF provisions (capacity, queue, secret and network path), and its product, endpoint and engine version are Not specified in the source documents (GAP-0997; ASM-1779). The pipeline, its states, its quality rule and its retries are this story's.
- The file and the OCR JSON are read and written in Azure Blob through the platform storage product RWB-PLT-TE012-APP (the X dependency), by managed identity: the intake file from the intake container and the full OCR output at `ocr/{intakeId}.json`. This service never copies a file into its own store.
- A failed call is retried by the `DocumentIntakeWorkflow` template of the workflow kit (DP-10, H RWB-PLT-E1071-CON), not by a Quartz step; the 15-minute business-hours run is a Temporal Schedule registered in the same template (12.6).
- The read of an intake item, its text and its OCR status is published through the gateway-bff composite route of DP-19 (H RWB-PLT-N001-CON), and the migration is one step in the per-service Flyway sequence (DP-15).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-0997; ASM-1779); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, exception paths, business rules, messages, authority, data fields, nine acceptance criteria and ten test cases, adapted to the target service's schema, topic, API base and workflow template.

### 2. Business rationale

Scanned documents arrive as images; nothing in them can be classified, extracted or searched until the text is read (FSD P5 A2.7). This story builds the OCR step of the document intake: one intake record per file, the text and layout of every page, a quality check per page and a rescan request when a page cannot be read. It meets REQ-DCM-006 (fields extracted in Thai and English, which needs Thai and English text first), REQ-DCM-009 (every path ends in the same intake) and REQ-DCM-010 (a file is read only after its malware scan is CLEAN). The measure is fields extracted without review (FSD P5 A2.7.1).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). No table of another service is read and no monolith table name survives.
2. The intake record and the page text are P5's own rows in `rwb_document`; the case owner, the case ID and the document ID arrive through the `rwb-case` contract with a mock and a 2 s timeout (DP-11), so the pipeline builds against a published shape.
3. The four OCR parameters and the four lists come from the parameters and reference-data contracts of `rwb-case`, through the client libraries of DP-06 and DP-07; the threshold, the worker count, the timeout and the attempt limit are never written in code.
4. The legacy `JOB-12 Document intake` Quartz step becomes a Temporal Schedule of the L3 template "Document intake" (DP-10): the Schedule starts `DocumentIntakeWorkflow` every 15 minutes in business hours, and the workflow runs the activities `ingest`, `ocr`, `classify`, `extract` and `matchStep` in order.
5. The legacy row-lock and worker pool become the activity concurrency of the worker and the `SELECT ... FOR UPDATE SKIP LOCKED` selection inside the `ocr` activity; the worker pool is sized by RWB-P5-E1049-INF and the concurrency limit is the parameter `OCR_WORKERS`.
6. The OCR provider call keeps its legacy shape — languages Thai and English in, per-page lines, words, positions, language and word confidence out, with `OcrUnavailableException` and `UnreadableFileException` mapped to the two target outcomes — but the provider is an external engine behind a private endpoint, provisioned by RWB-P5-E1049-INF, not an in-process adapter.
7. The OCR output JSON goes to the intake and text containers through the storage product RWB-PLT-TE012-APP; this service holds the reference `ocr_ref` and the text pages, never a copy of the bytes in its database.
8. The two reads the legacy pipeline published in-process (`forIntake` and `pagesForDocument`) become the intake read, the text read and the OCR status operations of the contract (12.1), reached by the review queue, classification and extraction through the gateway-bff composite route of DP-19.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1042-CON | The parameters client library, so `OCR_MIN_QUALITY`, `OCR_WORKERS`, `OCR_TIMEOUT_SECONDS` and `OCR_MAX_ATTEMPTS` are read through a published shape (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-OCR-STATUS, LOV-INTAKE-REVIEW, LOV-DOC-SOURCE and LOV-SCAN-RESULT (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library; the DocumentStored inbox row and the OcrCompleted outbox row are written in the activity transaction (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 `DocumentIntakeWorkflow` template "Document intake", its activity registration, its retry policy and its Schedule support (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the intake migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the intake, text and OCR status reads to the review queue screen (DP-19) |
| RWB-P5-E1049-CON | The contract baseline of this key: the four operations, the `IntakeItem`, `OcrTextPage` and `IntakeStatus` shapes, the error envelope and the declared event schema |
| RWB-P5-E1024-APP | The store: `document` rows, the containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, and `DocumentStored` (EV-16) published once per stored document |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the four OCR parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the four lists (DP-07) |
| RWB-P5-E1049-INF | The OCR engine capacity and queue, the worker pool for the Schedule, the intake and text containers, the topic ACLs, the secret and the network path to the provider (the X dependency) |
| RWB-P5-E1049-OPS | The deployment: the chart, the worker on queue `rwb-document` in namespace `rwb-recovery`, the registered 15-minute Schedule, the feature flag and the runbook (the X dependency) |
| RWB-PLT-TE012-APP | The platform storage product: the intake and text containers, the managed identity and the blob access policy (the X dependency) |

Business preconditions carried from RWB-E1-049:

- RWB-E1-024 is done: documents are stored and DocumentStored (EV-16) is published.
- RWB-TE-012 is done: the intake and standard containers exist.
- RWB-E1-045 is done: product parameters are held as data.
- Document hub parameters loaded: `OCR_MIN_QUALITY` = 0.70, `OCR_WORKERS` = 4, `OCR_TIMEOUT_SECONDS` = 120, `OCR_MAX_ATTEMPTS` = 3 (all assumed, DL11; the assumed values are carried as `ASM-1787`).
- The OCR service run by Autonomous Ops is reachable from SIT through the client of this service under the service identity SY-OCR.
- An intake item has `scan_result` CLEAN. The malware scan step is added in RWB-E1-041; until then test data is seeded CLEAN.
- Feature flag `rwb.document.ocr` is on. The legacy flag name `rwb.dochub.ocr` is retired with the monolith.

The OCR engine product, its endpoint, its engine version and its capacity, and the business-hours window of the Schedule, are Not specified in the source documents (GAP-0997; ASM-1779).

### 4. Flow

1. Schedule of JOB-12 Document intake: the 15-minute business-hours Temporal Schedule starts `DocumentIntakeWorkflow` on queue `rwb-document`; the workflow runs the `ingest` activity, then `ocr`, then `classify`, `extract` and `matchStep` (12.5, 12.6).
2. `ingest` activity: for each `rwb.document.DocumentStored.v1` event with source UPLOAD taken from the inbox, creates a `document_intake` row with the case ID, the document ID and `scan_result` CLEAN (the upload was scanned before storage), keyed by the intake item ID so a redelivered event creates nothing.
3. `ocr` activity: selects `document_intake` rows with `scan_result` CLEAN and `ocr_status` PENDING, oldest first, locking each row with `SELECT ... FOR UPDATE SKIP LOCKED` so that no two workers take the same item; runs up to `OCR_WORKERS` items in parallel.
4. `ocr` activity: reads the intake file from the intake container through the storage product and calls the OCR engine with the languages Thai and English (DP-10 activity retry policy: 1 s initial interval, back-off 2, 10 attempts; `OCR_TIMEOUT_SECONDS` as the call timeout).
5. OCR engine answer: per page, the lines, words, positions, language and word confidence.
6. `ocr` activity: computes the page quality as the mean word confidence of the page; stores the full output as JSON at `ocr/{intakeId}.json` in the text container and sets `ocr_ref` and `ocr_engine_version`.
7. `ocr` activity, one transaction in `rwb_document`: writes one `document_text` row per page with the page text and quality, with the document ID where the item is already attached, and sets `ocr_quality` to the lowest page quality of the item.
8. `ocr` activity: if every page has quality at or above `OCR_MIN_QUALITY`, sets `ocr_status` DONE; otherwise sets `ocr_status` RESCAN and `rescan_pages` to the page numbers below the threshold. The threshold is inclusive.
9. `ocr` activity: for an item in RESCAN with a known case, sends MSG-P5-018 to the case owner read through the `rwb-case` contract and the notification path; for an item with no case, sets `review_reason` RESCAN so the item shows in the document review queue (SCR-31, RWB-E1-054).
10. `ocr` activity: writes `rwb.document.OcrCompleted.v1` to the outbox in the same transaction as the status and the text rows, and records the run counts (read, done, rescan, failed) on the run record shown in the job monitor.
11. Outbox relay: publishes `rwb.document.OcrCompleted.v1` to `rwb.document.events.v1` once per item, keyed by caseId where the case is known and by intake item ID otherwise, with no personal data.

A failure of the engine call is a retry of the activity, not a lost item: the row stays PENDING with `ocr_attempts` raised, and the next run picks it up (AC6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A page has quality below `OCR_MIN_QUALITY` | Item set RESCAN with the page numbers; case owner told, or the item goes to the review queue | MSG-P5-018 | AC3, AC4 |
| X2 | Page quality exactly at `OCR_MIN_QUALITY` | The page is accepted | None | AC5 |
| X3 | The OCR engine does not answer within `OCR_TIMEOUT_SECONDS` or returns an error | `ocr_attempts` increases; the item stays PENDING for the next run; after two failed runs an alert is raised to the platform administrator through the run record | MSG-GEN-006 | AC6 |
| X4 | The item fails `OCR_MAX_ATTEMPTS` times or the file cannot be opened | `ocr_status` FAILED; `review_reason` UNREADABLE_FILE; item in the review queue | None | AC7 |
| X5 | The run picks up items already DONE | Items are not read again; no second set of text rows | None | AC8 |
| X6 | Two workers start on the same item | The row lock lets one worker take it; the other skips it | None | AC9 |
| X7 | A user without the Documents right reads a document holding OCR text | Refused with 403; no text returned | MSG-P4-002 | TC-E1-049-10 (Access) |
| X8 | The intake read, the text read or the OCR status read names a case outside the caller's scope | Refused with 403; no page text and no status is returned | MSG-P4-003 | TC-E1-049-10 (target read) |
| X9 | The `rwb-case` contract does not answer within 2 s, or the breaker is open, when the rescan notice is prepared | The item is still set RESCAN; the notice is not sent; the next run retries the notice; the breaker shields the case service | MSG-GEN-006 | AC3 (target path) |
| X10 | The outbox relay is down when the OCR activity commits | The status, the text rows and the outbox row are committed; the event is published by the relay when it recovers, once per item | None | AC8 (target path) |
| X11 | A redelivered DocumentStored event arrives for an intake item that exists | The inbox row and the unique intake key drop the repeat; one intake item and one set of text rows exist | None | AC8 (target path) |
| X12 | The task queue has no worker for longer than the Schedule interval | Items stay PENDING and the Schedule's overlap policy SKIP starts no second run; the stuck-workflow and queue-depth alerts of RWB-P5-E1049-OPS fire | None | AC2 (target path) |

Two target-service notes:

- The legacy job record becomes the run record of `DocumentIntakeWorkflow`: the counts of step 10 are the run attributes read by the job monitor (SCR-44) and by the dashboards of RWB-P5-E1049-OPS, and no `job` table row is written.
- The legacy rerun of JOB-12 from the job monitor is the rerun of the workflow run for its business date, refused while the run is active and refused for a completed business date; the operation itself is the platform job view's and this story adds no endpoint for it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-P5-E1024-APP), the containers (RWB-PLT-TE012-APP), the case contract, the parameters and reference contracts and the workflow kit, all earlier or contract work |
| Negotiable | Quality threshold, workers, timeout and attempts are parameters; the OCR service can change behind the client while the pipeline, its states and its retries stay |
| Valuable | Every scan becomes text that the later steps and the search read |
| Estimable | One table pair, one workflow with one activity, one outbound client, one listener, one Schedule |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: OCR pipeline on the Workbench document hub

  Background:
    Given OCR_MIN_QUALITY is 0.70, OCR_WORKERS is 4 and OCR_MAX_ATTEMPTS is 3
    Given the OCR service stub in SIT is replaced by the OCR service for AC1 and AC2
    Given the rwb-case contract mock returns the parameters OCR_MIN_QUALITY, OCR_WORKERS, OCR_TIMEOUT_SECONDS and OCR_MAX_ATTEMPTS
    Given the rwb-case contract mock returns the owner of case "RW-2026-000123" when the rescan notice is prepared

  Scenario: AC1 Sample processed (legacy RWB-E1-049 AC1)
    Given the 180 synthetic sample documents, 30 of each of the six agreed types, in Thai and English, each as a CLEAN intake item
    When JOB-12 Document intake runs
    Then each of the 180 items has ocr_status "DONE" or "RESCAN" and an ocr_ref to its JSON output
    Then each page has a document_text row with the page text and its quality
    Then the text of the sample pages holds Thai and English words, and the languages recorded per item are "th" and "en" where both appear

  Scenario: AC2 Throughput (legacy RWB-E1-049 AC2)
    Given 500 pages in 125 CLEAN intake items in SIT
    When they are processed by JOB-12 with 4 workers
    Then all 125 items reach "DONE" or "RESCAN" within 60 minutes of the first item starting

  Scenario: AC3 Unreadable page on a known case (legacy RWB-E1-049 AC3)
    Given an uploaded court notice of 4 pages on case "RW-2026-000123" owned by user "TEST-CO-01"
    Given page 3 has quality 0.41 and the other pages are above 0.70
    When the OCR step runs
    Then the intake item has ocr_status "RESCAN" and rescan_pages "3"
    Then "TEST-CO-01" receives MSG-P5-018 naming page 3, the document and case "RW-2026-000123"

  Scenario: AC4 Unreadable page with no case yet (legacy RWB-E1-049 AC4)
    Given a mailroom scan of 2 pages with no case and page 1 at quality 0.30
    When the OCR step runs
    Then the intake item has ocr_status "RESCAN", rescan_pages "1" and review_reason "RESCAN"
    Then the system sends no notification

  Scenario: AC5 Quality at the threshold (legacy RWB-E1-049 AC5)
    Given a scan of 1 page with quality 0.70
    When the OCR step runs
    Then the item has ocr_status "DONE" and no rescan pages

  Scenario: AC6 OCR service unavailable (legacy RWB-E1-049 AC6)
    Given the OCR service stub returns HTTP 503 for every call
    When JOB-12 runs twice
    Then each pending item has ocr_status "PENDING" and ocr_attempts 2
    Then the job monitor shows the OCR step failed in both runs and an alert is raised to the platform administrator
    Then when the service answers again the next run sets the items "DONE"

  Scenario: AC7 File that cannot be read (legacy RWB-E1-049 AC7)
    Given a password-protected PDF as a CLEAN intake item
    When the OCR step runs
    Then the item has ocr_status "FAILED" and review_reason "UNREADABLE_FILE"
    Then no document_text row exists for it

  Scenario: AC8 Repeat run (legacy RWB-E1-049 AC8)
    Given 10 intake items already "DONE" with 25 document_text rows
    When JOB-12 runs again
    Then the OCR service receives no call for those items
    Then they still have 25 document_text rows

  Scenario: AC9 Two workers on one item (legacy RWB-E1-049 AC9)
    Given one CLEAN pending item and 4 workers starting at the same time
    When the OCR step runs
    Then the OCR service receives exactly one call for the item
    Then the item has one set of document_text rows
```

Every Given, When and Then line above is the legacy line unchanged, except the two Background Givens that replace the in-process read of the other module with a contract mock; the legacy job-rerun and intake-item read endpoints become the intake submit, intake item read, text read and OCR status operations of 12.1 on `/api/recovery/document/v1`, and the OCR provider behind the legacy `OcrClient` adapter becomes the external OCR engine that RWB-P5-E1049-INF provisions.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every inbound file is read in Thai and English | REQ-DCM-006; FEAT-DCM-07 |
| BR2 | Scans, partner files, emails and uploads go through the same intake item and OCR step | REQ-DCM-009 |
| BR3 | A file is read only after its malware scan is CLEAN | REQ-DCM-010; FEAT-DCM-18 |
| BR4 | A page below `OCR_MIN_QUALITY` is sent for rescan; the threshold is inclusive | Document hub parameter OCR_MIN_QUALITY (New); DL11 |
| BR5 | A system that does not answer is retried on the next run and alerted after two failed runs | R-UNI-33; JOB-12 |
| BR6 | An item read once is not read again | R-UNI-40 |
| BR7 | Worker count, timeout and attempts are parameters | Principle 1; DT02 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 and BR2 are executed in `rwb_document` only: `document_intake` is the one row per file of every path, `document_text` is the one row per page, and the languages returned by the engine are recorded on the item. No foreign schema is read (DP-01); the case arrives through `GET /cases/{caseId}` of `rwb-case` and the stored document arrives as `rwb.document.DocumentStored.v1`.
- BR3 is executed by the selection predicate `scan_result = 'CLEAN'` and the partial index `ix_intake_ocr_pending`; the scan itself is RWB-E1-041's and this story never reads an unscanned item.
- BR4 is executed by the quality rule in the `ocr` activity: page quality is the mean word confidence, the comparison is "at or above", and the value is read from `document_hub_parameter` through the parameters contract (DP-06). The threshold is never in code.
- BR5 is executed by the activity retry policy of the workflow kit and by the run record: `ocr_attempts` counts the calls, the item stays PENDING below the attempt limit, and the run record carries the failed count that raises the alert (DP-10).
- BR6 is executed by the status predicate `ocr_status = 'PENDING'` in the selection and by the inbox row of DP-09 and the unique page index `uk_document_text_page`, so a repeat writes neither a second call nor a second text row.
- BR7 is executed by reading all four values from `document_hub_parameter` through the parameters contract; the worker concurrency limit is `OCR_WORKERS` and the call timeout is `OCR_TIMEOUT_SECONDS`.
- DP-07 keeps the four lists in reference data; DP-15 puts the intake migration in the per-service Flyway sequence as one step in `rwb_document`; DP-09 puts the event in the outbox inside the activity transaction; DP-13 and DP-19 give the reads their own base and the composite route.

### 9. State transitions

None for a case: this story does not change a case status. It changes the intake item OCR status:

| From | Event | To |
|---|---|---|
| (no row) | `ingest` activity takes a DocumentStored event with source UPLOAD | `ocr_status` = PENDING, `ocr_attempts` = 0 |
| PENDING | every page has quality at or above `OCR_MIN_QUALITY` | DONE |
| PENDING | a page is below the threshold | RESCAN, with `rescan_pages` set |
| PENDING | the engine call fails below `OCR_MAX_ATTEMPTS` | PENDING, `ocr_attempts` + 1 |
| PENDING | the engine call fails at `OCR_MAX_ATTEMPTS`, or the file cannot be opened | FAILED, with `review_reason` UNREADABLE_FILE |
| DONE | a later run selects the item | no transition; the item is not selected |

`review_reason` RESCAN is set with the RESCAN status when no case is known. The values are those of LOV-OCR-STATUS (PENDING, DONE, RESCAN, FAILED) and LOV-INTAKE-REVIEW (RESCAN, UNREADABLE_FILE, LOW_CONFIDENCE, MODEL_UNAVAILABLE, UNKNOWN_TYPE); no value is written in code.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Reads intake files, writes OCR output and text rows (Documents CRU) |
| RW-CASEOWN | Receives the rescan notice for their case |
| RW-PLATADM, platform administrator | Sees the run counts and alerts in the job monitor; reruns the intake run for a business date |
| Roles with Documents R | Read the OCR text of documents in their scope through RWB-E1-033 |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope and masking in `rwb_access`) and consumed as the cached permission decision the service holds. This story adds no operation and no guard of its own for it: the refusal shape is 403 with MSG-P4-002 or MSG-P4-003, as in the legacy endpoints. The service identity that writes the text and the event is SY-OCR; the writer of the run record is the workflow's.

The database login is per service (DP-02). Its name is Not specified in the source documents (GAP-0997; ASM-1779); the story refers to "the rwb-document login (DP-02)".

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Read |
| DF-DOC-002 | `document` | case_id | Read |
| DF-DOC-005 | `document` | source | Read |
| DF-CAS-009 | `rwb-case` case, through the contract | owner_user_id | Read, through the case contract |
| DF-DOC-045 to DF-DOC-084 | `document_intake` | all fields | Write (this story creates the record) |
| DF-DOC-085 to DF-DOC-090 | `document_text` | all fields | Write (this story creates the record) |
| DF-REF-246 | `document_hub_parameter` | param_value | Read |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_document` | the row for OcrCompleted | Write |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `rwb_case` row is copied and no ACE view is read by this service: DF-CAS-009 arrives inside the `rwb-case` contract answer, and DP-01 forbids a foreign-schema read. Personal data never enters the event payload, the workflow input or the log; the OCR text is held only in `document_text` and the text container, and logs carry the intake ID and the counts only.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/intake-items` | P5 | Submits one file of the intake: source, source reference, file name, size, SHA-256, case ID when known and the file reference in the intake container; returns the intake item in PENDING. Service identity and the intake paths of RWB-E1-057 call it; `Idempotency-Key` required. The exact request field names are Not specified in the source documents (GAP-0997; ASM-1779) |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}` | P5 | The `IntakeItem` shape: status, page count, quality, languages, engine version, rescan pages, review reason and the case and document IDs; Documents right R with scope applied; maps to API-P5-011 |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/text` | P5 | The ordered `OcrTextPage` list of the item: page number, text and quality; Documents right R with scope applied |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/ocr-status` | P5 | The `IntakeStatus` shape: `ocr_status`, `ocr_attempts`, `ocr_engine_version`, `rescan_pages` and `review_reason`; Documents right R with scope applied; the classification and extraction steps read it before they run |

The intake item read maps to API-P5-011 of TSD P5 T-A.1 on the target base; the content download API-P5-012 belongs to the review queue story and is not declared here. Errors follow RFC 9457 with `messageId`.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 | RWB-P3-E1018-CON | The case exists, its owner is known and it is in the caller's scope; one hop, 2 s timeout, breaker per downstream (DP-11). Consumed and faked although the plan lists it in no C row of this key |

The four parameters and the four lists are not REST operations of this story: they are read through the `rwb-case` parameters and reference-data client libraries of DP-06 and DP-07, which wrap the contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON. The file and the OCR JSON are read and written through the storage product RWB-PLT-TE012-APP, which is not a REST contract of another service; it appears in 12.9 as File. The OCR engine is an external provider behind a private endpoint, not a service contract of this estate.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.OcrCompleted.v1` | `rwb.document.events.v1` | P5 | caseId where the case is known, otherwise the intake item ID | intakeItemId, documentId, caseId, ocrStatus, pageCount, ocrQuality, ocrEngineVersion, occurredAt |

The OCR step records no decision, so no decision record is published by this story: the intake record and the text pages are facts. CloudEvents 1.0 envelope, binary mode; no personal data and no page text in the payload. The event is written to the outbox in the activity transaction, so it exists exactly when the status and the text rows exist; the once-per-item guarantee rests on the outbox relay and the consumer inbox of DP-09. The schema is declared by RWB-P5-E1049-CON. This is a third event name on the topic: the architecture's service catalogue lists DocumentStored and DocumentFieldsExtracted for `rwb-document`, and that difference is recorded in the contract baseline's own gap row rather than silently resolved here.

#### 12.4 Events consumed

| Event | Topic | Use |
|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | The `ingest` activity creates one `document_intake` row for each stored document with source UPLOAD; the inbox row of DP-09 drops a redelivery |

The event is published by the store RWB-P5-E1024-APP. This story publishes nothing for it and creates no topic; the retry topics and the `.dlt` topic of `rwb.document.events.v1` are RWB-PLT-N002-INF's and are reused as provisioned.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | One run per Schedule tick and business date; runs the five activities in order and holds the retry policy of the kit |
| `ingest` | Activity | `rwb-document` | Contributed by this story: creates the intake item from DocumentStored with source UPLOAD |
| `ocr` | Activity | `rwb-document` | Contributed by this story: selects and locks the pending items, calls the engine, applies the quality rule, writes the text pages and the status, sends the rescan notice and writes the outbox row |
| `classify` | Activity | `rwb-document` | Contributed by RWB-P5-E1050-APP; registered by this workflow and not built here |
| `extract` | Activity | `rwb-document` | Contributed by RWB-P5-E1053-APP; registered by this workflow and not built here |
| `matchStep` | Activity | `rwb-document` | Contributed by RWB-P5-E1032-APP (automatic attach); registered by this workflow and not built here |

The workflow input and output shapes are fixed by RWB-P5-E1049-CON; the activity in this story is `ocr` plus `ingest`, and the other three activities are called by the same workflow run in the order above.

#### 12.6 Schedules

| Schedule | Cron | Overlap | What it starts |
|---|---|---|---|
| Document intake (legacy JOB-12) | Every 15 minutes in business hours, Asia/Bangkok (the exact business-hours window is Not specified in the source documents (GAP-0997; ASM-1779)) | SKIP, with the catch-up window of the workflow kit | `DocumentIntakeWorkflow` on `rwb-document` |

No Quartz row, no shared job table entry and no Control-M job is registered; the Schedule is registered from configuration by RWB-P5-E1049-OPS and the workflow is served by the worker of the same release.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_intake` | P5 | The one row per inbound file: source, scan result, case and document IDs, `ocr_ref`, `ocr_status`, `ocr_attempts`, `page_count`, `rescan_pages`, `ocr_quality`, `languages`, `ocr_engine_version`, `review_reason` |
| `document_text` | P5 | The one row per page: page number, text, quality |
| `document` | P5 | Read only: the case, source and storage reference of the attached document (RWB-P5-E1024-APP owns the write) |
| `document_hub_parameter` | P5 | Read only: the four OCR parameter rows behind the parameters contract |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The OcrCompleted outbox row and the `processed_event` inbox row |

No foreign-schema table is read (DP-01). No ACE view is read by this service.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| OCR engine fake | RWB-P5-E1049-CON | The fixed per-page answer with lines, words, positions, language and word confidence; the 503 answer of AC6; the unreadable-file answer of AC7; the delayed answer beyond `OCR_TIMEOUT_SECONDS` |
| rwb-case case fake (`GET /cases/{caseId}`) | RWB-P3-E1018-CON | The case owner for the rescan notice and the 2 s timeout path |
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | `OCR_MIN_QUALITY` 0.70, `OCR_WORKERS` 4, `OCR_TIMEOUT_SECONDS` 120, `OCR_MAX_ATTEMPTS` 3 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-OCR-STATUS, LOV-INTAKE-REVIEW, LOV-DOC-SOURCE and LOV-SCAN-RESULT |
| storage product stub | RWB-PLT-TE012-APP | The intake file read and the OCR JSON write at `ocr/{intakeId}.json` |
| Drools kit | not used | No rule package is evaluated in this story; the quality rule is a parameter comparison |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4, consumed 1 | The intake submit, the intake item read, the text read and the OCR status read; the case read of `rwb-case` |
| Kafka | Published 1, consumed 1 | `rwb.document.events.v1`: `rwb.document.OcrCompleted.v1` out, `DocumentStored` in |
| Temporal | 1 workflow, 5 activities (2 built here) | `DocumentIntakeWorkflow` from the kit template with `ingest` and `ocr` built here, `classify`, `extract` and `matchStep` called from their own stories; one 15-minute business-hours Schedule |
| File | 2 paths | The intake file read from the intake container and the OCR JSON written at `ocr/{intakeId}.json` in the text container, both through RWB-PLT-TE012-APP |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/ocr`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntakeController | Controller | The four operations of 12.1; maps exceptions to RFC 9457 problem responses with the message ID; access check and scope |
| DocumentStoredListener | Listener, inside the `ingest` activity | Creates one `document_intake` row per stored document with source UPLOAD, idempotent by the inbox row and the intake key |
| OcrActivity | Temporal activity (`ocr`) | Selects and locks the pending items with `SKIP LOCKED`, runs up to `OCR_WORKERS` in parallel, applies the quality rule, writes the text pages, the status and the outbox row |
| OcrClientAdapter | Client (outbound) | Calls the external OCR engine with the two languages and the timeout; maps an unavailable or timed-out engine to the retryable class and an unreadable file to the terminal class |
| QualityRule | Domain | Page quality as the mean word confidence, the inclusive threshold comparison, the rescan page list and the item quality as the lowest page quality |
| RescanNotifier | Domain | Sends MSG-P5-018 to the case owner read through the `rwb-case` contract; sets `review_reason` RESCAN when no case is known |
| DocumentIntakeRepository | Repository | Reads and writes `document_intake` only; the `version` column is the optimistic lock and the selection uses `FOR UPDATE SKIP LOCKED` |
| DocumentTextRepository | Repository | Writes `document_text`; the unique page index makes a repeat a no-op |
| OcrParameters | Library client | Reads the four OCR parameters through the parameters contract of `rwb-case`, cached for 5 minutes |
| DocumentTextClient | Library client | Reads the four lists through the reference-data contract of `rwb-case` |
| OcrOutputReader | Published port | The intake read, the text read and the OCR status read of 12.1, used by the review queue, classification and extraction through the composite route |

**Database**

- One migration in the per-service Flyway sequence (DP-15): `V1049_1__document_intake_ocr.sql` creates `document_intake` (id, source varchar(12), source_ref varchar(120), received_at timestamptz, file_sha256 char(64), intake_ref varchar(400), scan_result varchar(10), case_id uuid, document_id uuid, ocr_ref varchar(400), ocr_status varchar(12) default 'PENDING', ocr_attempts integer default 0, page_count integer, rescan_pages varchar(200), ocr_quality numeric(5,4), languages varchar(20), ocr_engine_version varchar(40), review_reason varchar(20), plus the standard columns) and `document_text` (id, intake_id uuid not null, document_id uuid, page_no integer, text_content text, quality numeric(5,4), plus the standard columns).
- Foreign keys `document_intake.document_id` and `document_text.document_id` to `document(id)`; `document_text.intake_id` to `document_intake(id)`.
- Indexes: `ix_intake_ocr_pending` on `document_intake (ocr_status, received_at) where scan_result = 'CLEAN'`; unique `uk_document_text_page` on `document_text (intake_id, page_no)`; `ix_document_text_document` on `document_text (document_id)`.
- Row selection uses `SELECT ... FOR UPDATE SKIP LOCKED`.

**Configuration and reference data**

- Parameters `OCR_MIN_QUALITY`, `OCR_WORKERS`, `OCR_TIMEOUT_SECONDS` and `OCR_MAX_ATTEMPTS` in `document_hub_parameter`, read through the parameters contract and loaded by the reference data administrator. The legacy values 0.70, 4, 120 and 3 are the assumed values under DL11 (`ASM-1787`).
- Property `rwb.document.ocr.endpoint`, set per environment by RWB-P5-E1049-INF; its value is Not specified in the source documents (GAP-0997; ASM-1779).
- Notification template for MSG-P5-018 in the notification path, recovery templates.
- Container properties for the intake and text containers, as provisioned by RWB-P5-E1049-INF and RWB-PLT-TE012-APP.
- Feature flag `rwb.document.ocr`. Off: the `ocr` activity is skipped and items stay PENDING; the reads still answer.

**Build steps**

1. Write the migration and the entities; test the unique page index and the partial pending index.
2. Build `OcrClientAdapter` against the engine fake that returns fixed pages; contract-test the per-page mapping, the timeout and the two error classes.
3. Build the selection with `SKIP LOCKED` and the `OCR_WORKERS` pool inside the `ocr` activity; test AC8 and AC9.
4. Add `QualityRule` and the status setting; test AC3, AC4 and AC5 on synthetic pages, including the inclusive threshold of AC5.
5. Add the retry, the attempt counter and the FAILED rule; test AC6 and AC7, and that the alert of AC6 comes from the run record.
6. Build the `ingest` activity, the inbox handling and `RescanNotifier`; test AC3 end to end with the case fake.
7. Build the four operations with the access check and the scope; API tests for the reads, MSG-P4-002 and MSG-P4-003.
8. Register `DocumentIntakeWorkflow` and the five activities in the kit template and assert the 15-minute business-hours Schedule at RWB-P5-E1049-OPS; test that one tick starts one run.
9. Run the 180 sample documents and the 500-page set in SIT against the OCR engine; record the results for AC1 and AC2.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the two intake tables into `rwb_document` and removes every cross-module read: the case owner is no longer read from a case table but from the `rwb-case` contract, which is DP-11 and the contract RWB-P3-E1018-CON that this key consumes without a C row. DP-06 and DP-07 keep the four parameters and the four lists out of the code, with the parameter rows in this schema as the Ownership Map gives them to P5. DP-09 puts `OcrCompleted` in the outbox and the `DocumentStored` consumption in the inbox, so a redelivered event creates nothing. DP-10 is the substantive pattern: the Quartz step of JOB-12 becomes a Temporal Schedule that starts `DocumentIntakeWorkflow`, and the worker pool and the retry policy come from the kit rather than from a batch configuration. DP-13 and DP-15 give the service its own base and its own migration step. DP-19 puts the intake, text and status reads behind the gateway-bff composite route, so the review queue screen calls the owner once. The OCR engine and the containers are X dependencies (RWB-P5-E1049-INF and RWB-PLT-TE012-APP) because they are infrastructure and platform work, not a service contract.

**Done when.** The tests in section 16 pass, the 500-page run in SIT finishes within 60 minutes with 4 workers, and `rwb.document.OcrCompleted.v1` is on the topic once per item with no page text and no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-018 | A page is below the quality threshold on a document of a known case | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The intake item, its text or its status is read for a case outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The OCR engine did not answer, or the `rwb-case` contract did not answer within 2 s | {system} is not available. Your request is queued and will be retried. |

MSG-P5-018 and MSG-P4-002 are the legacy messages copied unchanged; MSG-P4-003 and MSG-GEN-006 are the two refusal and unavailability shapes the target read and the contract hop need, and both exist in the source documents. The HTTP mapping is 403 for MSG-P4-002 and MSG-P4-003 and 503 for MSG-GEN-006; MSG-P5-018 is a notice and has no HTTP status. Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-GEN-006 the {system} value is "OCR service" for a provider failure and "Case service" for a case-contract timeout.

### 15. Screens and states

No screen in this story. The case owner receives MSG-P5-018 through the notification path. Items with `review_reason` RESCAN or UNREADABLE_FILE are listed on SCR-31 Document review queue when RWB-E1-054 is built, read through the operations of 12.1 behind the gateway-bff composite route. The platform administrator sees the run counts of Document intake on SCR-44 Interface and job monitor (state Running; failed; complete), fed by the run record and the dashboards of RWB-P5-E1049-OPS.

| State the operator sees | What it means |
|---|---|
| Running | The workflow run of the business date is active and the `ocr` activity holds items |
| Complete | The run finished; the counts read, done, rescan and failed are on the record |
| Failed | At least one engine call failed; below the attempt limit the items stay PENDING, and the failed count raises the alert after two runs |
| Waiting | No worker polled the queue; items stay PENDING with no attempt recorded |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-049-10 | Access | Component | Capacity and workforce planner (RW-CAPACITY, no Documents right) calls the document read on a document with OCR text; refused with MSG-P4-002 |
| TC-E1-049-01 | AC1, BR1, BR2 | End to end | 180 synthetic sample documents, 30 per type, Thai and English |
| TC-E1-049-02 | AC2, BR7 | End to end | 500 synthetic pages in 125 items in SIT |
| TC-E1-049-03 | AC3, BR4 | End to end | 4-page upload with page 3 at quality 0.41 |
| TC-E1-049-04 | AC4, BR4 | End to end | 2-page mailroom scan with no case, page 1 at 0.30 |
| TC-E1-049-05 | AC5, BR4 | End to end | 1 page at quality 0.70 |
| TC-E1-049-06 | AC6, BR5 | End to end | OCR engine fake returning 503 |
| TC-E1-049-07 | AC7 | End to end | Password-protected synthetic PDF |
| TC-E1-049-08 | AC8, BR6 | End to end | 10 items already DONE |
| TC-E1-049-09 | AC9 | End to end | One item, 4 workers |

The legacy level System maps to End to end and Access maps to Component. The wave-1 integration harness copies TC-E1-049-01 as TC-E1-049-01-ITG in RWB-ITG-E1049-ITG, where the real `rwb-case` contract, the real parameters contract and the real OCR engine replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: threshold, workers, timeout and attempts are parameters.
- No personal data in logs, tests, prompts or events. OCR text is never written to application logs; logs and the event carry the intake ID, the document ID, the status and the counts only. Test documents are synthetic.
- No read of another module's tables: the case owner comes through the `rwb-case` contract, one hop with a 2 s timeout, and ACE data is reached only through the owner's contract or a `v_ace_*` view, of which this service reads none.
- OCR text is held only in `document_text` and the text container; it is not sent to any service other than the OCR engine, the classifier and the extraction step, and it never appears in an event payload, a workflow input or a log.
- The intake file is read from the container and never copied into the database; the database holds the reference and the hash.
- The pipeline is idempotent twice over: the inbox row of DP-09 drops a redelivered DocumentStored event, and the status predicate plus the unique page index stop a second read of a DONE item.
- The feature flag `rwb.document.ocr` removes the capability without a rollback of the schema.
- No Schedule is created by hand and no `job` row is written: the 15-minute run is a Schedule registered from configuration by RWB-P5-E1049-OPS.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted for the agreed types in Thai and English | Business Requirements Epic 1, section 3.5 | FEAT-DCM-07 | 13 Manage documents and correspondence | R-UNI-33 | TC-E1-049-01, TC-E1-049-03, TC-E1-049-04, TC-E1-049-05, TC-E1-049-07 |
| REQ-DCM-009 | Documents from every path through the same intake | Business Requirements Epic 1, section 3.5 | FEAT-DCM-07 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-40 | TC-E1-049-02, TC-E1-049-06, TC-E1-049-08, TC-E1-049-09, TC-E1-049-10 |
| REQ-DCM-010 | Every inbound file is scanned before it is read and quarantined if it fails | Business Requirements Epic 1, section 3.5 | FEAT-DCM-18 | 13 Manage documents and correspondence | BR3 | TC-E1-049-01, TC-E1-049-07 |

| Legacy reference | Where it is kept |
|---|---|
| Document hub parameters OCR_MIN_QUALITY 0.70, OCR_WORKERS 4, OCR_TIMEOUT_SECONDS 120, OCR_MAX_ATTEMPTS 3 | Background, sections 3, 4, 8, 13 |
| Event DocumentStored (EV-16) | Sections 4, 12.4 |
| JOB-12 Document intake, every 15 minutes in business hours | Sections 1, 4, 12.6 |
| MSG-P5-018, MSG-P4-002 | Section 14 and the exception paths |
| Test cases TC-E1-049-01 to TC-E1-049-10 | Section 16 |

### 19. Out of scope

- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057).
- The malware scan step (RWB-E1-041).
- Classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The review queue screen and correction (RWB-E1-054).
- Field app photos and bills (RWB-E2-024).
- The OCR engine itself, its capacity, its secret and its network path (RWB-P5-E1049-INF) and the deployment, dashboards, alerts and runbook (RWB-P5-E1049-OPS).

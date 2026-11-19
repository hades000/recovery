# Technical Specification — RWB-E1-049 OCR pipeline on the Workbench document hub

| Field | Value |
|---|---|
| Story | RWB-E1-049 — OCR pipeline on the Workbench document hub |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-051-epic-1-RWB-E1-049` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-015); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 049 OCR pipeline on the Workbench document hub v1.md`; FSD P5 A2.7; TSD P5 T3.1, T5.3 |
| Upstream IDs | BRD-RWB-005; FR-RWB-015; REQ-DCM-006, REQ-DCM-009; US-RWB-E1-049; CTX-FEATURE-005; DL11; R-UNI-33, R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The case owner receives MSG-P5-018 through the ACE notification path; SCR-31 and SCR-44 belong to RWB-E1-054 and Epic 2/E8. |
| Logic In Scope | `YES` — intake item creation, OCR selection and locking, worker pool, quality rule, rescan routing, retry, failure and idempotency. |
| API In Scope | `NO` — no endpoint or contract change. The story adds JOB-12's `ocrStep` and the `OcrOutputReader` / `OcrClient` published interfaces. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-12 Document intake; `document_intake` and `document_text` (new tables); `DocumentStored` (EV-16) listener; standard container; ACE notification path; `CaseDirectory` (P3). |
| New Nodes Required | `YES` — `DocumentIntakeJob`, `OcrStep`, `OcrClient`, `OcrServiceAdapter`, `DocumentStoredListener`, `RescanNotifier`, `DocumentIntakeRepository`, `DocumentTextRepository`, `OcrOutputReader`. |
| Inherited Existing Behavior | Document store and `DocumentStored` (RWB-E1-024); containers and managed identity (RWB-TE-012); product parameters (RWB-E1-045); ACE notification path; ACE scheduler. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every inbound file is read in Thai and English. | SPEC-RWB-E1-049-005 | DIRECT | `OcrClient.read` sends `["th","en"]`; the response records the languages found. | COVERED |
| BR2 | Scans, partner files, emails and uploads go through the same intake item and OCR step. | SPEC-RWB-E1-049-001, SPEC-RWB-E1-049-002 | DIRECT | One `document_intake` row per file; uploads create one from `DocumentStored`. | COVERED |
| BR3 | A file is read only after its malware scan is CLEAN. | SPEC-RWB-E1-049-003 | DIRECT | Selection requires `scan_result='CLEAN'`; the scan step is RWB-E1-041. | COVERED |
| BR4 | A page below `OCR_MIN_QUALITY` is sent for rescan; the threshold is inclusive. | SPEC-RWB-E1-049-009 | DIRECT | `quality < threshold` fails; `>=` passes. | COVERED |
| BR5 | A system that does not answer is retried on the next run and alerted after two failed runs. | SPEC-RWB-E1-049-011 | DIRECT | `ocr_attempts`; alert on the second failed run. | COVERED |
| BR6 | An item read once is not read again. | SPEC-RWB-E1-049-013 | DIRECT | Only `ocr_status='PENDING'` is selected. | COVERED |
| BR7 | Worker count, timeout and attempts are parameters. | SPEC-RWB-E1-049-004, SPEC-RWB-E1-049-015 | DIRECT | `OCR_WORKERS`, `OCR_TIMEOUT_SECONDS`, `OCR_MAX_ATTEMPTS`, `OCR_MIN_QUALITY` in `document_hub_parameter`. | COVERED |
| AC1 | 180 sample items are read; each has `DONE` or `RESCAN`, an `ocr_ref`, a text row per page, and Thai/English languages recorded. | SPEC-RWB-E1-049-005, SPEC-RWB-E1-049-007, SPEC-RWB-E1-049-008, SPEC-RWB-E1-049-015 | DIRECT | SIT sample run; languages `th,en`. | COVERED |
| AC2 | 500 pages in 125 clean items finish within 60 minutes with 4 workers. | SPEC-RWB-E1-049-004, SPEC-RWB-E1-049-017 | DIRECT | Throughput target; job counts recorded. | COVERED |
| AC3 | A 4-page court notice with page 3 at 0.41 is `RESCAN` with `rescan_pages="3"`; the owner receives MSG-P5-018. | SPEC-RWB-E1-049-009, SPEC-RWB-E1-049-010 | DIRECT | Notification names page, document and case. | COVERED |
| AC4 | A 2-page mailroom scan with no case and page 1 at 0.30 is `RESCAN` with `review_reason="RESCAN"`; no notification. | SPEC-RWB-E1-049-009, SPEC-RWB-E1-049-010 | DIRECT | No recipient without a case. | COVERED |
| AC5 | A page at exactly 0.70 is `DONE` with no rescan pages. | SPEC-RWB-E1-049-009 | DIRECT | Inclusive threshold. | COVERED |
| AC6 | OCR service 503 on two runs leaves items `PENDING` with `ocr_attempts=2`; job monitor shows failure and an alert; the next successful run sets `DONE`. | SPEC-RWB-E1-049-011 | DIRECT | Retry and alert. | COVERED |
| AC7 | A password-protected PDF is `FAILED` with `review_reason="UNREADABLE_FILE"` and no text rows. | SPEC-RWB-E1-049-012 | DIRECT | Unreadable file path. | COVERED |
| AC8 | 10 items already `DONE` with 25 text rows are not read again and keep 25 rows. | SPEC-RWB-E1-049-013 | DIRECT | Idempotency by status. | COVERED |
| AC9 | One item and 4 workers produce exactly one OCR call and one set of text rows. | SPEC-RWB-E1-049-003 | DIRECT | `FOR UPDATE SKIP LOCKED`. | COVERED |
| X1 | A page below the threshold. | SPEC-RWB-E1-049-009, SPEC-RWB-E1-049-010 | DIRECT | `RESCAN`; notify or queue. | COVERED |
| X2 | Page quality exactly at the threshold. | SPEC-RWB-E1-049-009 | DIRECT | Accepted. | COVERED |
| X3 | OCR service timeout or error. | SPEC-RWB-E1-049-011 | DIRECT | Attempts; `PENDING`; alert after two runs. | COVERED |
| X4 | Attempt limit reached or file cannot be opened. | SPEC-RWB-E1-049-012 | DIRECT | `FAILED`; `UNREADABLE_FILE`. | COVERED |
| X5 | Repeat run over `DONE` items. | SPEC-RWB-E1-049-013 | DIRECT | No second call or rows. | COVERED |
| X6 | Two workers start on the same item. | SPEC-RWB-E1-049-003 | DIRECT | One takes it; the other skips. | COVERED |
| X7 | A user without Documents R reads OCR text. | SPEC-RWB-E1-049-018 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **every inbound scan and upload read by the OCR service into text and layout in Thai and English, stored against the intake item and the document**, so that **classification and extraction can start and an unreadable page is sent back for rescan the same day**.

The story builds the OCR step of JOB-12: one intake record per file, the text and layout of every page, a quality check per page, and a rescan request when a page cannot be read. It creates the intake item from an upload event and from the intake paths owned by RWB-E1-057. It adds no screen and no endpoint; the review queue and the job monitor are other stories.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake every 15 minutes in business hours; `DocumentStored` with source `UPLOAD` creates an intake item. |
| Preconditions | RWB-E1-024 done and `DocumentStored` published; RWB-TE-012 containers exist; RWB-E1-045 parameters; `OCR_MIN_QUALITY=0.70`, `OCR_WORKERS=4`, `OCR_TIMEOUT_SECONDS=120`, `OCR_MAX_ATTEMPTS=3` (assumed; DL11); OCR service reachable through `OcrClient` under SY-OCR; `scan_result='CLEAN'` (seeded until RWB-E1-041); `rwb.dochub.ocr` flag on. |
| Input | Intake items with `scan_result='CLEAN'` and `ocr_status='PENDING'`, oldest first; the file in the intake container. |
| Output | `document_intake` OCR fields; `document_text` rows; OCR JSON at `ocr/{intakeId}.json`; rescan notification or review reason; job counts. |
| Feature flag | `rwb.dochub.ocr`. Off: `ocrStep` is skipped and items stay `PENDING`. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `source` | Intake path | System writes | `LOV-DOC-SOURCE` |
| `document_intake` | `source_ref`, `file_sha256`, `intake_ref` | Intake path / store | System writes | File identity and storage reference |
| `document_intake` | `scan_result` | Scan step (RWB-E1-041) | System writes | `CLEAN` or `INFECTED`; OCR reads only `CLEAN` |
| `document_intake` | `ocr_status` | Job | System writes | `PENDING`, `DONE`, `RESCAN`, `FAILED` |
| `document_intake` | `ocr_attempts` | Job | System writes | Starts at 0; increments on a failed call |
| `document_intake` | `ocr_ref` | Job | System writes | `ocr/{intakeId}.json` in the standard container |
| `document_intake` | `page_count` | OCR response | System writes | Number of pages returned |
| `document_intake` | `rescan_pages` | Quality rule | System writes | Comma-separated page numbers below the threshold |
| `document_intake` | `ocr_quality` | Quality rule | System writes | Mean word confidence across pages |
| `document_intake` | `languages` | OCR response | System writes | Comma-separated ISO 639-1 codes, for example `th,en` |
| `document_intake` | `review_reason` | Quality/failure rule | System writes | `RESCAN` or `UNREADABLE_FILE` in this story |
| `document_text` | `page_no`, `text_content`, `quality` | OCR response | System writes | Unique (`intake_id`, `page_no`) |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `PENDING` | OCR completes | Every page at or above `OCR_MIN_QUALITY` | `DONE` | `ocr_ref`, text rows, languages, page count |
| `PENDING` | OCR completes | At least one page below the threshold | `RESCAN` | `rescan_pages`; notify owner or set `review_reason=RESCAN` |
| `PENDING` | OCR call fails | Attempts below `OCR_MAX_ATTEMPTS` | `PENDING` | `ocr_attempts+1`; retry next run |
| `PENDING` | Attempt limit reached, or file cannot be opened | `ocr_attempts = OCR_MAX_ATTEMPTS` or unreadable | `FAILED` | `review_reason=UNREADABLE_FILE`; no text rows |
| `DONE` | Repeat run | Item is not `PENDING` | `DONE` | No call and no new rows |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Page below threshold | `RESCAN` with page numbers; owner notified, or item queued when no case | MSG-P5-018 |
| X2 | Page exactly at threshold | Accepted; `DONE` if all pages pass | None |
| X3 | OCR timeout or error | Attempts increase; item stays `PENDING`; alert after two failed runs | Job monitor failure; platform administrator alert |
| X4 | Attempt limit or unreadable file | `FAILED`; `review_reason=UNREADABLE_FILE`; no text rows | None |
| X5 | Repeat run over `DONE` | No call; rows unchanged | None |
| X6 | Two workers on one item | Row lock lets one take it; the other skips | None |
| X7 | User without Documents R reads OCR text | 403; no text returned | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | None directly. OCR text is read through RWB-E1-033 and RWB-E1-024 endpoints by authorised users. |
| Contract delta | None. The job and the `OcrOutputReader` interface are internal. |
| Backward compatibility | Unchanged. |
| Authorization | SY-OCR under Documents CRU for the job; a reader needs Documents R and case scope through the reading endpoint. |
| Error behaviour | Job retries on 503/timeout; no synchronous API error. A read by an unauthorised user returns 403 MSG-P4-002 from the reading endpoint. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label changes; the case owner receives a notification. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-006, REQ-DCM-009; SPEC-RWB-E1-049-001..018 | New job, step, adapter, listener, notifier and two repositories. | Selection and locking; quality boundary 0.69/0.70/0.71; rescan page list; notification with and without a case; timeout/attempts; unreadable file; idempotency; unique page index; language mapping. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DocumentIntakeJob` | Job | Spring Batch job behind JOB-12 with ordered steps; this story builds the job and `ocrStep`. |
| `OcrStep` | Job | Selects, locks and reads items; applies the quality rule; writes output. |
| `OcrClient`, `OcrServiceAdapter` | Service | Calls the OCR service; maps errors to `OcrUnavailableException` and `UnreadableFileException`. |
| `DocumentStoredListener` | Listener | Creates an intake item for each uploaded document. |
| `RescanNotifier` | Service | Sends MSG-P5-018 to the case owner through the ACE notification path. |
| `DocumentIntakeRepository` | Repository | Reads and writes `document_intake` only. |
| `DocumentTextRepository` | Repository | Writes `document_text`. |
| `OcrOutputReader` | Published interface | `forIntake(intakeId)` and `pagesForDocument(documentId)`. |

### Package and boundaries

Folder `recovery/dochub/ocr`, Java package `recovery.dochub.ocr`. The package owns `document_intake` and
`document_text`; the case owner is read through `CaseDirectory`; the file is read through
`DocumentStorage`. No other package writes these tables.

### Data and migration

Flyway `V1_5_049__document_intake.sql` creates `document_intake` (`id`, `source varchar(12)`,
`source_ref varchar(120)`, `received_at timestamptz`, `file_sha256 char(64)`, `intake_ref varchar(400)`,
`scan_result varchar(10)`, `case_id uuid`, `document_id uuid`, `ocr_ref varchar(400)`, `ocr_status
varchar(12) default 'PENDING'`, `ocr_attempts integer default 0`, `page_count integer`, `rescan_pages
varchar(200)`, `ocr_quality numeric(5,4)`, `languages varchar(20)`, `ocr_engine_version varchar(40)`,
`review_reason varchar(20)`, standard columns) and `document_text` (`id`, `intake_id uuid not null`,
`document_id uuid`, `page_no integer`, `text_content text`, `quality numeric(5,4)`, standard columns).
Foreign keys to `document(id)` and `document_intake(id)`. Indexes: `ix_intake_ocr_pending` on
(`ocr_status`, `received_at`) where `scan_result='CLEAN'`; unique `uk_document_text_page` on
(`intake_id`, `page_no`); `ix_document_text_document` on (`document_id`).

### OCR flow

1. `DocumentStoredListener` creates an intake item for an upload with `case_id`, `document_id` and
   `scan_result='CLEAN'`.
2. `OcrStep` selects `scan_result='CLEAN'` and `ocr_status='PENDING'`, oldest first, with
   `SELECT ... FOR UPDATE SKIP LOCKED`.
3. Up to `OCR_WORKERS` items are read in parallel; each worker holds its row lock for the item.
4. `OcrClient.read(file, ["th","en"], timeout)` returns page lines, words, positions, language and word
   confidence.
5. Page quality is the mean word confidence of the page. The full output is stored as JSON at
   `ocr/{intakeId}.json` in the standard container; `ocr_ref` is set.
6. One `document_text` row per page is written with the page text and quality; `document_id` is set
   when the item is already attached.
7. If every page is at or above `OCR_MIN_QUALITY`, `ocr_status='DONE'`; otherwise `RESCAN` with
   `rescan_pages` listing the pages below the threshold.
8. A `RESCAN` item with a known case sends MSG-P5-018 to the case owner. An item with no case sets
   `review_reason='RESCAN'` and sends no notification.
9. Run counts (read, done, rescan, failed) are written to the job record.

### Retry and failure

- A timeout or 503 increments `ocr_attempts` and leaves the item `PENDING`.
- After two failed runs the job raises an alert to the platform administrator.
- At `OCR_MAX_ATTEMPTS`, or when the file cannot be opened, the item becomes `FAILED` with
  `review_reason='UNREADABLE_FILE'`; no `document_text` row is written.
- A stopped run leaves unfinished items `PENDING`; the next run or a rerun from the job monitor picks
  them up.

### Transaction and events

Each item is processed in its own transaction: the status, attempts, `ocr_ref` and text rows commit
together. A failed call commits only the attempt count and status. No event is published; the item is
read by RWB-E1-050 and RWB-E1-053 through `OcrOutputReader`.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR OCR and extraction pipeline | Documents CRU; reads intake files and writes OCR output | All |
| RW-CASEOWN Case owner | Receives the rescan notice | Own cases |
| RW-PLATADM Platform administrator | Sees job counts and alerts; reruns JOB-12 | All |
| Roles with Documents R | Read OCR text through RWB-E1-033 in scope | Own/team |

### Observability and operations

- Job record: items read, done, rescan, failed, attempts, duration, OCR engine version.
- Metrics: pages read, mean quality, rescan rate, timeout rate, alert count.
- Alerts: OCR step failed twice; item stuck `PENDING` beyond one hour; rescan rate above threshold.
- Logs carry intake ID, page count and counts only; never OCR text, file name or personal data.
- Run book: check the OCR endpoint, rerun JOB-12, identify stuck items.

### Performance

- Target: 500 pages in 125 items within 60 minutes with 4 workers (AC2).
- One OCR call per item; page text written in one batch; `SKIP LOCKED` avoids worker contention.
- The JSON output is written once per item to the standard container.

### Feature flag and rollback

- `rwb.dochub.ocr`. Off: `ocrStep` is skipped and items stay `PENDING`.
- Rollback: turn the flag off; redeploy the previous tag. Items already `DONE` remain readable; the
  migration is forward-only and additive.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-049-01 | AC1, BR1, BR2 | System | 180 synthetic documents, 30 per type, Thai and English | Each `DONE`/`RESCAN`; `ocr_ref`; text per page; `th,en` recorded |
| TC-E1-049-02 | AC2, BR7 | System | 500 synthetic pages in 125 items | All reach `DONE`/`RESCAN` within 60 minutes |
| TC-E1-049-03 | AC3, BR4 | System | 4-page upload, page 3 at 0.41 | `RESCAN`; `rescan_pages="3"`; MSG-P5-018 to owner |
| TC-E1-049-04 | AC4, BR4 | System | 2-page mailroom scan, no case, page 1 at 0.30 | `RESCAN`; `rescan_pages="1"`; `review_reason=RESCAN`; no notification |
| TC-E1-049-05 | AC5, BR4 | System | 1 page at 0.70 | `DONE`; no rescan pages |
| TC-E1-049-06 | AC6, BR5 | System | OCR stub returns 503 twice | `PENDING`; `ocr_attempts=2`; alert; later `DONE` |
| TC-E1-049-07 | AC7 | System | Password-protected synthetic PDF | `FAILED`; `UNREADABLE_FILE`; no text rows |
| TC-E1-049-08 | AC8, BR6 | System | 10 items already `DONE`, 25 text rows | No call; 25 rows unchanged |
| TC-E1-049-09 | AC9 | System | One item, 4 workers | One call; one set of text rows |
| TC-E1-049-10 | X7 | Security | RW-CAPACITY (no Documents right) reads a document with OCR text | 403 MSG-P4-002 |
| TC-E1-049-U1 | BR4, BR5, BR6, AC5, AC8 | Unit | Page qualities 0.69/0.70/0.71; `DONE` item; timeout twice | `RESCAN`/`DONE` boundary; no second call; attempts and alert |

## Guardrails

- No business value in code: threshold, workers, timeout and attempts are parameters.
- No personal data in logs, tests or prompts. OCR text is never written to application logs; logs carry
  the intake ID and counts only. Test documents are synthetic.
- No read of another module's tables: the case owner comes through `CaseDirectory`.
- OCR text is held only in `document_text` and the standard container; it is not sent to any service
  other than the OCR service and the classifier.

## Out of scope

- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057).
- The malware scan step (RWB-E1-041).
- Classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The review queue screen and correction (RWB-E1-054).
- Field app photos and bills (RWB-E2-024).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted for the agreed types in Thai and English | Business Requirements Epic 1, section 3.5 | FEAT-DCM-07 | 13 Manage documents and correspondence | R-UNI-33 | TC-E1-049-01, 03, 04, 05, 07 |
| REQ-DCM-009 | Documents from every path through the same intake | Business Requirements Epic 1, section 3.5 | FEAT-DCM-07 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-40 | TC-E1-049-02, 06, 08, 09, 10 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR7; SPEC-015 | Are the OCR parameters fixed? | Threshold, worker count, timeout and attempts. | `OCR_MIN_QUALITY=0.70`, `OCR_WORKERS=4`, `OCR_TIMEOUT_SECONDS=120`, `OCR_MAX_ATTEMPTS=3` are assumed (DL11) and loaded as data. | RESOLVED | SPEC-015 |
| CLAR-002 | AC1; SPEC-015 | What format do the recorded languages take? | Field width and downstream parsing. | Comma-separated ISO 639-1 codes in detection order, for example `th,en`; `varchar(20)` holds the six combinations the sample can produce. This is an implementation decision, not a business rule. | RESOLVED | SPEC-015 |
| CLAR-003 | AC1; SPEC-006 | Is page quality the mean word confidence? | Rescan decision. | Yes: the mean of the word confidences on the page (story flow step 5). | RESOLVED | SPEC-006 |
| CLAR-004 | AC3, AC4; SPEC-010 | What happens when a `RESCAN` item has a case but no owner? | Notification recipient. | The story defines the recipient as the case owner. With no owner there is no recipient, so no notification is sent; the item stays `RESCAN` with its page numbers and is counted on the job record. | RESOLVED | SPEC-010 |
| CLAR-005 | AC6; SPEC-011 | What counts as a failed run for the alert? | Alert timing. | A run in which the OCR call failed for at least one item; the alert is raised on the second consecutive failed run (story X3, AC6). | RESOLVED | SPEC-011 |
| CLAR-006 | AC7; SPEC-012 | Is an unreadable file retried? | Attempt behaviour. | No: a file that cannot be opened is `FAILED` immediately with `UNREADABLE_FILE`; only timeouts and service errors are retried (story X3, X4). | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story or the named decision log
entry. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this batch story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New JOB-12 OCR step, intake item and page text; no screen and no contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: batch OCR step with internal interfaces only]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 9 acceptance criteria, 7 exception paths and 5 OCR states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

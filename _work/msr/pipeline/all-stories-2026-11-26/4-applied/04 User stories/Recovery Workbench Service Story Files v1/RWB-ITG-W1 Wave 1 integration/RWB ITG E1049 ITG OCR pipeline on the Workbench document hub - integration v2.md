# RWB-ITG-E1049-ITG OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1049-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-049 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1045-APP, RWB-P5-E1049-APP, RWB-P6-E1049-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-006, REQ-DCM-009, REQ-DCM-010) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-049 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E1049-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-049 OCR step across P5 rwb-document (the intake item, the text and layout, the OCR step of DocumentIntakeWorkflow), P3 rwb-case (the case owner the rescan notice goes to) and P6 rwb-comms (the notice)**, so that **every inbound file becomes searchable text and an unreadable page is sent back the same day, proved on the real services before wave 1 exits**.

### 2. Business rationale

The legacy story runs JOB-12 as a Quartz job inside the document module with document_intake and document_text in the recovery schema. The target keeps both tables in rwb_document (Owner P5, Architecture v5 slides 16 and 41), starts the OCR step inside DocumentIntakeWorkflow from the DocumentStored event plus the JOB-12 trigger with KEDA workers (Architecture v5 slide 44), dedupes the duplicate event through the inbox (DP-09), reads its four parameters as data rows and returns the rescan notice to the case owner through P6 rwb-comms. The trigger, the meaning of the worker cap and the home of the four parameters are not fixed by the sources: Not specified in the source documents (GAP-0362; ASM-0476).

The legacy measures stay as they are: REQ-DCM-006 (fields extracted in Thai and English, which needs Thai and English text first), REQ-DCM-009 (every path ends in the same intake item), REQ-DCM-010 (a file is read only after its malware scan is CLEAN) and FSD P5 A2.7, whose measure is fields extracted without review (FSD P5 A2.7.1).

No service contract is faked. The suite exercises the published wave 1 contracts of P3, P5 and P6, the shared Temporal namespace and the standard container; the only stubs are the external ones named in section 12.8. Where the sources do not name the trigger, the worker cap or the evidence location, the suite asserts through the owners' contracts and the open point is recorded as GAP-0362 and ASM-0476.

### 3. Preconditions

- RWB-P5-E1049-APP is done: document_intake and document_text, the OCR step of DocumentIntakeWorkflow, the OcrClient adapter and the rescan notifier are in SIT.
- RWB-P3-E1045-APP is done: the case and its owner are readable through the rwb-case contract.
- RWB-P6-E1049-APP is done: MSG-P5-018 is sent through the ACE notification path and the notice is readable through the rwb-comms contract.
- The published contracts of P3 rwb-case, P5 rwb-document and P6 rwb-comms are deployed under their own per-service bases behind gateway-bff: /api/recovery/case/v1, /api/recovery/document/v1 and /api/recovery/comms/v1.
- Temporal namespace rwb-recovery with task queue rwb-document is available.
- The OCR service is reachable in SIT through the OcrClient adapter under the identity SY-OCR, and its stub is available for the unavailable-service scenario.
- The standard container is available (Azurite in the lower environment).
- The document hub parameters OCR_MIN_QUALITY 0.70, OCR_WORKERS 4, OCR_TIMEOUT_SECONDS 120 and OCR_MAX_ATTEMPTS 3 are loaded (legacy values, all assumed; ASM-0477).
- The 180 synthetic sample documents, 30 of each of the six agreed types, and the 500-page set in 125 items are in the harness RWB-ITG-W1J01-ITG.
- The feature flag rwb.dochub.ocr is on.
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- No build dependency: the story is Day 1 and waits on no build of its own.

### 4. Flow

1. QA integration engineer: loads the synthetic fixtures of harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: stores a synthetic upload through POST /api/recovery/document/v1/cases/{caseId}/documents and waits for rwb.document.DocumentStored.v1 on rwb.document.events.v1.
3. Harness: reads the intake item through GET /api/recovery/document/v1/intake-items/{intakeItemId} and asserts one intake item for the stored file; it delivers the same event twice with the same event id and asserts one intake item and one inbox record (AC1).
4. Harness: replaces the stub with the real OCR service, which answers under the identity SY-OCR, and runs the 180-sample set; the item states, the ocr_ref, the page rows, the languages and the Thai and English text are asserted (AC2).
5. Harness: runs the 500-page set in 125 items with OCR_WORKERS 4 and times the window from the first item starting (AC3).
6. Harness: reads the intake item and the document with its text pages through GET /api/recovery/document/v1/documents/{documentId} (AC2, AC3).
7. Harness: posts the threshold cases — page 3 at quality 0.41 on case RW-2026-000123 owned by TEST-CO-01, a 2-page mailroom scan with no case and page 1 at 0.30, and one page at exactly 0.70; it reads the case owner through GET /api/recovery/case/v1/cases/{caseId} and the notice through GET /api/recovery/comms/v1/notices/{noticeId} (AC4, AC5, AC6).
8. Harness: makes the stub return HTTP 503 for two JOB-12 runs, records the job monitor state and the alert, restores the service and lets the next run finish the items (AC7); it posts the password-protected PDF and asserts the unreadable outcome with no text row (AC8).
9. Harness: reruns over 10 items already DONE, starts four workers on one CLEAN pending item, changes OCR_MIN_QUALITY as a data row and reruns one scenario (AC9, AC10).
10. Harness: asserts the refusal of a role without the Documents right (AC11), writes the evidence report and removes the synthetic fixtures.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A page has quality below OCR_MIN_QUALITY | The item is set RESCAN with the page numbers; the case owner is told, or the item goes to the review queue with review_reason RESCAN | MSG-P5-018 | AC4, AC5 |
| X2 | Page quality exactly at OCR_MIN_QUALITY | The page is accepted and the item can end DONE | None | AC6 |
| X3 | The OCR service does not answer within OCR_TIMEOUT_SECONDS or returns an error | ocr_attempts increases; the item stays PENDING for the next run; after two failed runs the job monitor shows the step failed and an alert is raised to the platform administrator | None | AC7 |
| X4 | The item reaches OCR_MAX_ATTEMPTS or the file cannot be opened | ocr_status FAILED and review_reason UNREADABLE_FILE; no text row is written | None | AC8 |
| X5 | The run covers items already DONE | Those items are not read again and no second set of text rows appears | None | AC9 |
| X6 | Two workers start on the same item | The row lock lets one worker take the item; the other skips it and one call is made | None | AC9 |
| X7 | A user holds a role without the Documents right and reads a document holding OCR text | Refused with 403 and no text returned | MSG-P4-002 | AC11 |
| X8 | A consumed contract call exceeds the 2 s timeout or returns a server error | The step is retried under the run policy; the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC2 |
| X9 | The stub cannot be replaced by the real OCR service, or a fixture of the harness RWB-ITG-W1J01-ITG does not match | The suite fails as a harness fault and names the element; no service defect is raised | None | AC2, AC3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the published contracts of P3, P5 and P6, not their source code |
| Negotiable | The quality threshold, the worker cap, the timeout, the attempt limit and the fixture sizes are data rows of the harness; the story fixes the assertions and the call set |
| Valuable | The OCR text, the quality rule, the rescan notice and the throughput target are proved on real services before wave 1 exits |
| Estimable | One suite module, one fixture pack, one OCR stub, one worker control and one evidence report |
| Small | Eleven scenarios over three services and one workflow; no service code and no schema change |
| Testable | Every scenario asserts a contract response, an item state, a text row, a notice or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: OCR pipeline on the Workbench document hub, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-document, rwb-case and rwb-comms are deployed in SIT with their published contracts
    Given the OCR service is reachable through the OcrClient adapter under the identity SY-OCR
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used
    Given OCR_MIN_QUALITY is 0.70, OCR_WORKERS is 4, OCR_TIMEOUT_SECONDS is 120 and OCR_MAX_ATTEMPTS is 3

  Scenario: AC1 A stored document creates one intake item and a duplicate event creates none (new, D-RCV-60)
    Given a synthetic upload is stored through POST /api/recovery/document/v1/cases/{caseId}/documents
    Then the upload stores the file and rwb.document.DocumentStored.v1 is published on rwb.document.events.v1
    When DocumentStored arrives twice with the same event id
    Then one intake item exists with the case ID, the document ID and scan result CLEAN
    Then the inbox records the duplicate and no second intake item is created

  Scenario: AC2 The 180 sample documents are read into text and layout in Thai and English (new, D-RCV-60)
    Given the 180 synthetic sample documents, 30 of each of the six agreed types, each as a CLEAN intake item
    When the OCR step of DocumentIntakeWorkflow runs with the real OCR service
    Then each of the 180 items has ocr_status DONE or RESCAN with an ocr_ref to its JSON output
    Then each page has a document_text row holding the page text and its quality
    Then the text holds Thai and English words, and the languages th and en are recorded where both appear

  Scenario: AC3 500 pages in 125 items finish within 60 minutes with the worker cap (new, D-RCV-60)
    Given 500 pages in 125 CLEAN intake items in SIT
    When they are processed with OCR_WORKERS 4
    Then all 125 items reach DONE or RESCAN within 60 minutes of the first item starting

  Scenario: AC4 An unreadable page on a known case is sent for rescan and the case owner is told (new, D-RCV-60)
    Given an uploaded court notice of 4 pages on case RW-2026-000123 owned by TEST-CO-01
    Given page 3 has quality 0.41 and the other pages are above 0.70
    When the OCR step runs
    Then the intake item has ocr_status RESCAN and rescan_pages 3
    Then TEST-CO-01 receives MSG-P5-018 naming page 3, the document and case RW-2026-000123 through P6

  Scenario: AC5 An unreadable page with no case goes to the review queue with no notification (new, D-RCV-60)
    Given a mailroom scan of 2 pages with no case and page 1 at quality 0.30
    When the OCR step runs
    Then the intake item has ocr_status RESCAN, rescan_pages 1 and review_reason RESCAN
    Then no notification is sent

  Scenario: AC6 A page exactly at the quality threshold is accepted (new, D-RCV-60)
    Given a scan of 1 page at quality 0.70
    When the OCR step runs
    Then the item has ocr_status DONE and no rescan pages

  Scenario: AC7 An OCR service that does not answer is retried and alerted (new, D-RCV-60)
    Given the OCR stub returns HTTP 503 for every call
    When JOB-12 runs twice
    Then each pending item has ocr_status PENDING and ocr_attempts 2
    Then the job monitor shows the OCR step failed in both runs and an alert is raised to the platform administrator
    Then when the service answers again the next run sets the items DONE

  Scenario: AC8 A file that cannot be read ends FAILED with the unreadable reason (new, D-RCV-60)
    Given a password-protected PDF as a CLEAN intake item
    When the OCR step runs
    Then the item has ocr_status FAILED and review_reason UNREADABLE_FILE
    Then no document_text row exists for it

  Scenario: AC9 A repeat run reads nothing twice and two workers read one item once (new, D-RCV-60)
    Given 10 intake items already DONE with 25 document_text rows
    When JOB-12 runs again
    Then the OCR service receives no call for those items
    Then they still hold 25 document_text rows
    Given one CLEAN pending item and four workers starting at the same time
    When the OCR step runs
    Then the OCR service receives exactly one call for the item
    Then the item has one set of document_text rows

  Scenario: AC10 The four OCR parameters are read as data and a change needs no deployment (new, D-RCV-60)
    Given OCR_MIN_QUALITY is changed in the document hub parameter table and one scenario is rerun
    When the run completes
    Then the outcome changes with no code change and no deployment
    Then the four values are read from the document hub parameter table whose owner the Ownership Map names

  Scenario: AC11 A role without the Documents right is refused (new, D-RCV-60)
    Given a user holds RW-CAPACITY and no Documents right
    When the user reads the OCR text of a document
    Then the service refuses the call with status 403 and MSG-P4-002
    Then no text is returned
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every inbound file is read in Thai and English | RWB-E1-049 BR1; REQ-DCM-006; FEAT-DCM-07 |
| BR2 | Scans, partner files, emails and uploads go through the same intake item and OCR step | RWB-E1-049 BR2; REQ-DCM-009 |
| BR3 | A file is read only after its malware scan is CLEAN | RWB-E1-049 BR3; REQ-DCM-010; FEAT-DCM-18 |
| BR4 | A page below OCR_MIN_QUALITY is sent for rescan; the threshold is inclusive | RWB-E1-049 BR4; document hub parameter OCR_MIN_QUALITY; DL11 |
| BR5 | A system that does not answer is retried on the next run and alerted after two failed runs | RWB-E1-049 BR5; R-UNI-33; JOB-12 |
| BR6 | An item read once is not read again | RWB-E1-049 BR6; R-UNI-40 |
| BR7 | Worker count, timeout and attempts are parameters | RWB-E1-049 BR7; Principle 1; DT02 |
| BR8 | P5 rwb-document owns document_intake and document_text; no other service holds a copy and the suite reads them only through the P5 contract | Ownership Map (document_intake and document_text owner P5); Architecture v5 slides 16 and 41; DP-01 |
| BR9 | One intake item exists per stored file; a duplicate DocumentStored event creates no second item because the inbox dedupes it | DP-09; ASM-0476 |

### 9. State transitions

None for the case status: this story changes no case status. It observes the intake item OCR state inside rwb_document through the P5 contract.

| Object | State | Meaning |
|---|---|---|
| Intake item | PENDING | The item is CLEAN and waiting for the OCR step |
| Intake item | PENDING (after a failed call) | The call failed below the attempt limit; ocr_attempts increased and the next run takes the item again |
| Intake item | DONE | Every page is at or above OCR_MIN_QUALITY and the text rows are written |
| Intake item | RESCAN | At least one page is below OCR_MIN_QUALITY; rescan_pages holds the page numbers, and review_reason RESCAN is set when no case is known |
| Intake item | FAILED | The attempt limit was reached or the file cannot be opened; review_reason UNREADABLE_FILE |

The suite reads these states and never writes them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| SY-OCR, OCR and extraction pipeline | Reads intake files, writes OCR output and text rows (Documents CRU) |
| RW-CASEOWN | Receives the rescan notice for their case |
| RW-PLATADM, platform administrator | Sees the job counts and alerts in the job monitor; reruns JOB-12 |
| Roles with Documents R | Read the OCR text of documents in their scope |

No other role is in scope for this story. The suite acts as the QA integration engineer and asserts the other roles only through the contracts.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document (P5 rwb-document) | id | Read |
| DF-DOC-002 | document (P5 rwb-document) | case_id | Read |
| DF-DOC-005 | document (P5 rwb-document) | source | Read |
| DF-CAS-009 | recovery_case (P3 rwb-case) | owner_user_id | Read, through CaseDirectory |
| DF-DOC-045 to DF-DOC-084 | document_intake (P5 rwb-document) | all fields | Read, written by the owning service |
| DF-DOC-085 to DF-DOC-090 | document_text (P5 rwb-document) | all fields | Read, written by the owning service |
| DF-REF-246 | document_hub_parameter (P5 rwb-document) | param_value | Read |
| Cross-service trigger, worker cap and evidence location | DocumentIntakeWorkflow OCR step, OCR_WORKERS and the evidence store | Trigger, concurrency and report location | Not specified in the source documents (GAP-0362; ASM-0476) |

The legacy story writes document_intake and document_text; in this suite both are written by P5 rwb-document and the suite only reads them through the P5 contract. The case owner comes through the P3 contract and the notice through the P6 contract. Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| POST /api/recovery/document/v1/cases/{caseId}/documents | P5 rwb-document | Store the synthetic uploads that raise DocumentStored |
| GET /api/recovery/document/v1/intake-items/{intakeItemId} | P5 rwb-document | Read ocr_status, the attempts, the rescan pages, the review reason and the engine version |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the document and its text pages |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the case owner the rescan notice goes to |
| GET /api/recovery/comms/v1/notices/{noticeId} | P6 rwb-comms | Confirm MSG-P5-018 was sent to the case owner |

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.document.DocumentStored.v1 | rwb.document.events.v1 | P5 rwb-document | The OCR step starts and the duplicate is deduped through the inbox |

No event is produced by the suite.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | The workflow under test; it starts from DocumentStored and from the JOB-12 trigger |
| OCR step activity inside DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Reads the file, applies the quality rule and writes the text rows and the item state |

The activity reads and writes only the rwb_document schema. No workflow, activity or the suite reads another service's schema.

#### 12.6 Schedules

None. JOB-12 is event-started inside the P5 workflow, not a Schedule (Architecture v5 slide 44: mechanism event plus KEDA workers).

#### 12.7 Tables owned

None (DP-01). document_intake and document_text are P5 tables.

#### 12.8 Contract fakes

| Stub | Use |
|---|---|
| OCR service stub | Returns fixed pages per file, and HTTP 503 for the unavailable-service scenario |
| Azurite Blob | Holds the standard container with the OCR JSON output |
| Clock control for the run window | Moves the run window so the timed set is measured against one window |

No service contract is faked: every call in section 12.2 goes to the real SIT service.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 5 |
| Kafka | 0 | 1 |
| Temporal | 0 | 1 workflow (DocumentIntakeWorkflow) |
| File | 0 | 1 standard container |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the eleven scenarios against SIT and holds no service code |
| OCR fixture pack | Test data | 180 synthetic documents, 30 of each of the six agreed types in Thai and English, and 500 pages in 125 items |
| OCR stub | External stub | Returns fixed pages per file, and HTTP 503 for the unavailable-service scenario |
| Worker and clock controls | Harness controls | Starts four workers on one item and moves the run window |
| Evidence report | Report | Records per scenario the run id, the item states, the counts, the contract responses and the messages |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | document_intake and document_text stay in rwb_document (P5); the suite asserts through the P5 contract only |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On the APP stories; the four OCR values are rows of the document hub parameter table that the Ownership Map names, read as data and changed without a deployment |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories; the six document types and the languages are reference data the suite reads through the contracts |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The intake item is created from rwb.document.DocumentStored.v1 on rwb.document.events.v1 and the duplicate is deduped by the inbox |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-12 is the OCR step inside DocumentIntakeWorkflow, event-started with KEDA workers (Architecture v5 slide 44) on queue rwb-document |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The five consumed REST operations of section 12.2 |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2 |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On the APP stories; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The case owner's notice reaches the officer through the ACE notification path; no screen is exercised here |

The dependency-added column records the build dependency of the owning story. This story has no build dependency: an ITG story waits on no build of its own. The H, C, I and X lists are exactly as the metadata table: no H, no C, no X, and the three I dependencies RWB-P3-E1045-APP, RWB-P5-E1049-APP and RWB-P6-E1049-APP.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P3, P5 and P6.
2. Build the fixture pack: the 180 synthetic documents, 30 of each of the six agreed types in Thai and English, and the 500-page set in 125 items.
3. Add the OCR stub with fixed pages per file and the HTTP 503 mode, and the switch to the real OCR service under the identity SY-OCR.
4. Implement AC1 to AC3 — the intake dedupe, the 180-sample run and the 500-page window — and assert only through the contracts of section 12.2, the event of section 12.4 and Temporal visibility.
5. Implement the threshold cases AC4 to AC6, reading the case owner through the P3 contract and the notice through the P6 contract.
6. Implement AC7 to AC9: the two failed runs and the alert, the unreadable file, the repeat run and the four workers on one item.
7. Implement AC10 and AC11: change OCR_MIN_QUALITY as a data row, rerun one scenario, and post the read by a role without the Documents right.
8. Write the evidence report with the throughput line, the item state counts and the message ids, and keep it with the wave exit evidence.

Done when: all twelve test cases pass in SIT against the published wave 1 contracts, the 500-page set finishes within 60 minutes with OCR_WORKERS 4, the evidence report is attached to the wave exit pack, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-018 | A page is below the quality threshold on a document of a known case | Page {page} of {document} on case {case} could not be read. Scan it again and send it to the document hub. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The message IDs and wording are copied from RWB-E1-049. No new message ID is added by this story. Thai text for each message follows decision DL10.

The evidence report also carries two report lines per scenario:

- Throughput line: {pages} pages in {items} items reached DONE or RESCAN in {minutes} minutes with OCR_WORKERS {workers}; run id {run}.
- Item state counts: {pending} PENDING, {done} DONE, {rescan} RESCAN, {failed} FAILED.

### 15. Screens and states

No screen in this story. The case owner receives MSG-P5-018 through the ACE notification path. Items with review_reason RESCAN or UNREADABLE_FILE are listed on SCR-31 Document review queue when RWB-E1-054 is built. The platform administrator sees the JOB-12 counts on SCR-44 Interface and job monitor.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-049-01-ITG | AC2 | Integration | 180 synthetic sample documents, 30 per type, Thai and English; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-02-ITG | AC3 | NFR | 500 synthetic pages in 125 items in SIT; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-03-ITG | AC4 | Integration | 4-page upload with page 3 at quality 0.41 on case RW-2026-000123 owned by TEST-CO-01; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-04-ITG | AC5 | Integration | 2-page mailroom scan with no case, page 1 at 0.30; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-05-ITG | AC6 | Integration | 1 page at quality 0.70; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-06-ITG | AC7 | NFR | OCR stub returning HTTP 503 for two runs; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-07-ITG | AC8 | Integration | Password-protected synthetic PDF; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-08-ITG | AC9 | Integration | 10 items already DONE with 25 document_text rows; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-09-ITG | AC9 | Integration | One CLEAN pending item, 4 workers; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-E1-049-10-ITG | AC11 | Component | RW-CAPACITY user with no Documents right reads a document with OCR text; refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1049-ITG-11 | AC1 | Integration | One stored upload and DocumentStored delivered twice with the same event id; end-to-end: real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1049-ITG-12 | AC10 | Contract | OCR_MIN_QUALITY changed in the document hub parameter table and one scenario rerun; end-to-end: real services on the wave 1 contracts; no numeric business values added |

The legacy full test text is in Recovery Workbench Test Cases v8.xlsx under the legacy test case id.

### 17. Guardrails

- No business value in code: the threshold, the workers, the timeout and the attempts are parameters, changed as data rows.
- No personal data in logs, events, evidence or fixtures. OCR text is never written to application logs; logs carry the intake id and counts only; test documents are synthetic.
- No cross-service table read: the case owner comes through the P3 contract, the notice through the P6 contract and the intake item through the P5 contract.
- One hop and a 2 s timeout on every call (ADR-020).
- OCR text stays in document_text and the standard container; it is not sent to any service other than the OCR service.
- Synthetic data only; the harness RWB-ITG-W1J01-ITG loads the fixtures.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-006 | Fields extracted for the agreed types in Thai and English | P5 OCR text, languages and quality on the intake item and its text pages | TC-E1-049-01-ITG, TC-E1-049-05-ITG |
| REQ-DCM-009 | Documents from every path through the same intake | The intake item raised from rwb.document.DocumentStored.v1; one item per stored file | TC-ITG-E1049-ITG-11, TC-E1-049-09-ITG |
| REQ-DCM-010 | A file is read only after its malware scan is CLEAN | scan result CLEAN on the intake item | TC-ITG-E1049-ITG-11, TC-E1-049-07-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed REST operations of section 12.2 | TC-E1-049-01-ITG, TC-E1-049-03-ITG, TC-ITG-E1049-ITG-12 |
| DP-01 | Owner's schema, never another service's tables | document_intake and document_text in rwb_document, read only through the P5 contract | All |
| DP-09 | Kafka with outbox, inbox and CloudEvents | rwb.document.DocumentStored.v1 on rwb.document.events.v1; the duplicate is deduped by the inbox | TC-ITG-E1049-ITG-11 |
| DP-10 | Temporal replaces Quartz; event-started workflow | JOB-12 as the OCR step inside DocumentIntakeWorkflow on queue rwb-document, with KEDA workers | TC-E1-049-06-ITG, TC-E1-049-08-ITG, TC-E1-049-09-ITG |
| ASM-0476 | The OCR step starts from DocumentStored plus the JOB-12 trigger and the duplicate is deduped | DocumentIntakeWorkflow, its OCR step activity and the inbox record | TC-ITG-E1049-ITG-11, TC-E1-049-06-ITG |
| ASM-0477 | The four OCR parameters stay rows of the document hub parameter table and OCR_WORKERS is the concurrency cap | document_hub_parameter read as data; the 60-minute window measured at OCR_WORKERS 4 | TC-E1-049-02-ITG, TC-ITG-E1049-ITG-12 |
| ASM-0478 | The OCR service stays outside, called under SY-OCR through OcrClient; the stub is replaced for the two runs and the engine version is recorded | OcrClient adapter, the OCR stub and ocr_engine_version on the intake item | TC-E1-049-01-ITG, TC-E1-049-02-ITG, TC-E1-049-06-ITG |

The legacy story is RWB-E1-049. The integration dependencies are RWB-P3-E1045-APP, RWB-P5-E1049-APP and RWB-P6-E1049-APP; the legacy AC1 to AC9 at component level belong to those stories, not to this one.

### 19. Out of scope

- The APP, INF and OPS builds and their unit and component tests.
- The CON story RWB-P5-E1049-CON.
- The legacy AC1 to AC9 at component level, which the sibling APP stories own.
- Pickup from branch scanners, the mailroom, partner SFTP and mailboxes (RWB-E1-057).
- The malware scan step (RWB-E1-041).
- Classification (RWB-E1-050), field extraction (RWB-E1-053) and attach to the case (RWB-E1-032).
- The review queue screen and correction (RWB-E1-054).
- Field app photos and bills (RWB-E2-024).
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing, which belongs to the NFR epic.

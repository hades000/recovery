# RWB-ITG-E1057-ITG Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1057-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-057 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P5-E1057-APP, RWB-S9-E1057-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DCM-009, REQ-DCM-010) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-057 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-057 intake step across P5 rwb-document (the intake item, the scan result and the JOB-12 intake step of DocumentIntakeWorkflow), S9 rwb-partner (the panel status behind the partner channel), P1 rwb-source-data (the job view and the rerun) and P4 rwb-access (the Platform administration right U)**, so that **every branch scan, mailroom scan, partner file and email attachment enters the same intake with its source recorded, proved on the real SIT services before wave 1 exits**.

### 2. Business rationale

The legacy story adds intakeStep as the first step of the JOB-12 DocumentIntakeJob, a Spring Batch job inside the document module, and writes document_intake in the single recovery schema. The target keeps document_intake in rwb_document (Owner P5, Architecture v5 slides 16 and 41), runs JOB-12 as an event-started workflow with KEDA workers on queue rwb-document (Architecture v5 slide 44), reads the partner panel status through the S9 rwb-partner contract instead of an in-process PartnerDirectory call (DP-11), shows and reruns the run through the P1 rwb-source-data job contract on SCR-44, and reads the intake parameters as data rows of the P5 document hub parameter table. The branch scanner folders, the mailroom folder, the partner SFTP inbound folder and the recovery mailboxes stay as they are: they are properties set per environment, and the mailbox service (Exchange Online read through Microsoft Graph) is outside the 19 services. The run evidence that shows the S9 partner check is the suite's own report, JOB-12 runs and reruns are read through P1's admin job contract (ASM-0499), and a failed step is restarted by the P5 workflow's retry policy (ASM-0498).

The legacy measures stay as they are: REQ-DCM-009 (documents arrive from branches, the mailroom, partner file transfer and email through the same intake, so every document path ends in the document hub) and REQ-DCM-010 (every inbound file is virus-scanned before it is stored). CTL-11 is kept too: a customer document never moves by email hand-off, so the mailbox channel is read by the platform identity and the sender address is masked.

No service contract is faked. The suite exercises the published wave 1 contracts of P5 rwb-document, S9 rwb-partner, P1 rwb-source-data and P4 rwb-access, the Temporal namespace rwb-recovery and four external channel endpoints; the only stubs are the external ones named in section 12.8.

### 3. Preconditions

- RWB-P5-E1057-APP is done: document_intake, the intakeStep activity of DocumentIntakeWorkflow and the four channel readers are in SIT.
- RWB-S9-E1057-APP is done: the partner panel with partner_code and panel_status is readable through the rwb-partner contract.
- The published contracts of P5 rwb-document, S9 rwb-partner, P1 rwb-source-data and P4 rwb-access are deployed under their own per-service bases behind gateway-bff: /api/recovery/document/v1, /api/recovery/partner/v1, /api/recovery/source-data/v1 and /api/recovery/access/v1.
- Temporal namespace rwb-recovery with task queue rwb-document is available.
- The partner panel rows are real synthetic SIT rows: partner "LF-007" a law firm with panel_status "ACTIVE", partner "LF-008" with panel_status "SUSPENDED", and no partner with partner_code "LF-099".
- The four external channel endpoints exist as properties of the SIT environment: the scanner folders by branch code, the mailroom folder, the partner SFTP inbound folder with one subfolder per partner_code, and the recovery mailboxes. The mailboxes are read through the mailbox stub of section 12.8.
- The document hub parameter rows are loaded: INTAKE_ALLOWED_TYPES PDF, JPG, PNG; INTAKE_MAX_FILE_MB 25; INTAKE_DUPLICATE_WINDOW_DAYS 30; INTAKE_MIN_IMAGE_KB 10; INTAKE_ALERT_AFTER_FAILURES 2 (legacy values, all assumed; ASM-0497).
- The synthetic fixtures of harness RWB-ITG-W1J01-ITG are loaded for branch, mailroom, partner SFTP and mailbox channels.
- The feature flag rwb.dochub.intake and its per-channel sub-flags are on.
- No production data is used, and no production connection is opened.
- The release date 30 November 2026 is tentative; a date is not a condition of this story.
- No build dependency: the story is Day 1 and waits on no build of its own.

### 4. Flow

1. QA integration engineer: loads the synthetic fixtures of harness RWB-ITG-W1J01-ITG; no production data is used.
2. Harness: writes one file to the scanner folder of branch "BR-0123", one to the mailroom folder, one to the SFTP subfolder "LF-007" and one email to mailbox "MBX-RECOVERY-01", all synthetic.
3. Harness: reads the panel status of "LF-007", "LF-008" and "LF-099" through GET /api/recovery/partner/v1/partners and records the answers as run evidence (AC2, AC5, AC7, AC16).
4. Harness: lets the 09:15 run of JOB-12 start and reads the run through GET /api/recovery/source-data/v1/admin/jobs, with its state and its intakeStep counts per channel (AC1, AC9).
5. Harness: reads each taken-in item through GET /api/recovery/document/v1/intake-items/{intakeItemId} and asserts source, channel_code, captured_at, file_sha256, an empty scan_result and ocr_status PENDING (AC1, AC2, AC3).
6. Harness: asserts the file moves — the channel file is gone and is in its processed folder, the refused file is in its rejected folder, and the email is in the archive folder (AC1, AC3, AC4, AC6).
7. Harness: posts the refused files — a DOCX, a 25.1 MB PDF next to a 25.0 MB PDF — and reads MSG-P5-001, MSG-P5-017 and MSG-P5-007 on the job record (AC4).
8. Harness: posts the partner exceptions — subfolder "LF-099" with no partner_code and subfolder "LF-008" with panel_status "SUSPENDED" — and reads MSG-P5-007 with PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE (AC5, AC7).
9. Harness: repeats the same hash "H1" from "BR-0123" on 2 December after 30 November and asserts one row and a duplicate count (AC6).
10. Harness: switches the intake container fault control on, runs, then restores it and reruns through the P1 job contract (AC8, AC10, AC15).
11. Harness: makes the SFTP subfolder unreadable for two runs and reads MSG-P5-008 naming PARTNER_SFTP, then lets the 10:30 run finish (AC10).
12. Harness: starts the second rwb-document instance and waits for the 09:15 run, then observes scanStep and ocrStep on one item and the trigger window at 18:15 (AC11, AC12, AC14).
13. Harness: reads one intake item per file across the four channels and the DocumentIntakeWorkflow execution with the partner check in its evidence, writes the evidence report and removes the synthetic fixtures (AC16).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | File type not allowed | No intake row; file moved to the rejected folder; counted as refused | MSG-P5-001, MSG-P5-007 | AC4 |
| X2 | File above the size limit | No intake row; file moved to the rejected folder | MSG-P5-017, MSG-P5-007 | AC4 |
| X3 | Partner subfolder code unknown or partner not ACTIVE | No intake row; file moved to the rejected folder | MSG-P5-007 | AC5, AC7 |
| X4 | Same hash from the same channel inside the window | No new row; file moved to processed; counted as a duplicate | None | AC6 |
| X5 | No new file or email on any channel | Run logged with zero counts | None | AC9 |
| X6 | The intake container does not accept writes | Files left at the channel; run failed; next run takes them | MSG-GEN-006 | AC8 |
| X7 | Two runs in a row fail on one channel | Alert to the platform administrator | MSG-P5-008 | AC10 |
| X8 | Two service instances are due at once | The run starts once and each file has one row | None | AC11 |
| X9 | A consumed contract call exceeds the 2 s timeout or returns a server error | The scenario is retried and the evidence report records the call and the response; no assertion is made on unverified data | None | AC1, AC16 |
| X10 | A user without Platform administration U reruns the job | 403 and no run started | MSG-P4-002 | AC15 |
| X11 | An email with no attachment, or only an image under 10 KB | Email archived; no intake row | None | AC13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the two APP stories and the published contracts of P5, S9, P1 and P4, not their source code |
| Negotiable | The folders, the mailbox codes, the allowed types, the size limit, the duplicate window and the alert count are properties and data rows; the story fixes the assertions and the call set |
| Valuable | The four inbound channels and the intake step are proved on real services before wave 1 exits, with the source of every file recorded |
| Estimable | One suite module, one fixture pack, four channel controls, one container fault switch and one evidence report |
| Small | Sixteen scenarios over four services and one workflow; no service code and no schema change |
| Testable | Every scenario asserts an intake item, a run state, a folder position, a counted refusal or a message; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Intake from branches, mailroom, partner SFTP and email, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-document, rwb-partner, rwb-source-data and rwb-access are deployed in SIT with their published contracts
    Given JOB-12 Document intake runs every 15 minutes from 08:00 to 18:00 Asia/Bangkok on working days
    Given INTAKE_ALLOWED_TYPES is PDF, JPG and PNG and INTAKE_MAX_FILE_MB is 25
    Given partner "LF-007" is a law firm with panel_status "ACTIVE" in the SIT partner panel
    Given the RWB-ITG-W1J01-ITG synthetic data set is loaded and no production data is used

  Scenario: AC1 A branch scan and a mailroom scan become two intake items (new, D-RCV-60)
    Given file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12
    Given file "mailroom-0001.pdf" in the mailroom folder
    When the intake job runs at 09:15
    Then exactly two intake items are taken in, both with source "SCAN", captured_at 2026-11-30 09:12 and an empty scan_result
    Then the item for "scan-0001.pdf" has channel_code "BR-0123"
    Then the item for "mailroom-0001.pdf" has channel_code "MAILROOM"
    Then each file is no longer in its channel folder and is in its processed folder

  Scenario: AC2 Partner SFTP (legacy RWB-E1-057 AC2)
    Given file "LF-007-notice-0001.pdf" in the SFTP inbound subfolder "LF-007"
    When the job runs
    Then one document_intake row has source "PARTNER", channel_code "LF-007" and partner_id of partner "LF-007"

  Scenario: AC3 Mailbox (legacy RWB-E1-057 AC3)
    Given an email to recovery mailbox "MBX-RECOVERY-01" with one PDF attachment "reply-0001.pdf"
    When the job runs
    Then one document_intake row has source "EMAIL", channel_code "MBX-RECOVERY-01" and the sender address recorded
    Then the system masks the sender address in every response and absent from the job record and the logs
    Then the email is in the archive folder of "MBX-RECOVERY-01"

  Scenario: AC4 A DOCX is refused for its type and a 25.1 MB file for its size (new, D-RCV-60)
    Given file "letter-0002.docx" in the scanner folder of branch "BR-0123"
    Given file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system writes no document_intake row for "letter-0002.docx" and shows reason MSG-P5-001
    Then the system writes no document_intake row for "scan-0003.pdf" and shows reason MSG-P5-017
    Then both refused files are in the rejected folder of branch "BR-0123"
    Then "scan-0004.pdf" has a document_intake row

  Scenario: AC5 An unknown and a suspended partner are refused through the S9 contract (new, D-RCV-60)
    Given file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code
    Given file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED"
    When the job runs
    Then the S9 partner contract answers no partner for "LF-099" and panel_status "SUSPENDED" for "LF-008"
    Then the system writes no document_intake row for either file
    Then the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE"

  Scenario: AC6 The same hash from the same channel is one item across two dates (new, D-RCV-60)
    Given file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November
    When the same file arrives again from branch "BR-0123" on 2 December
    Then the system writes no second document_intake row for "H1" on "BR-0123"
    Then the job record counts the file as a duplicate
    Then the file is in the processed folder of branch "BR-0123"

  Scenario: AC7 An unknown or suspended partner is refused (legacy RWB-E1-057 AC7)
    Given file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code
    Given file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED"
    When the job runs
    Then the system writes no document_intake row for either file
    Then the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE"

  Scenario: AC8 The intake container refuses writes and the file stays at the channel (new, D-RCV-60)
    Given the intake container refuses writes
    When the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123"
    Then the system writes no document_intake row
    Then "scan-0007.pdf" stays in the scanner folder and the run is failed with MSG-GEN-006
    Then on the next run with the container available the file is taken in

  Scenario: AC9 An empty run (legacy RWB-E1-057 AC9)
    Given no new file or email on any channel
    When the job runs
    Then the job record shows intakeStep complete with 0 items on each channel

  Scenario: AC10 Two failed partner SFTP runs raise the alert and the next run retries (new, D-RCV-60)
    Given the run at 10:00 failed because the SFTP inbound folder could not be read
    When the run at 10:15 fails for the same reason
    Then MSG-P5-008 naming "PARTNER_SFTP" is raised to the platform administrator
    Then the run at 10:30 tries again and finishes

  Scenario: AC11 Two service instances produce one 09:15 run and one item per file (new, D-RCV-60)
    Given two service instances of rwb-document are running
    When the 09:15 run is due with one file on each of the four channels
    Then the system records one run for 09:15
    Then each of the four files has one document_intake row

  Scenario: AC12 scanStep completes before ocrStep reads an item (new, D-RCV-60)
    Given file "scan-0009.pdf" was taken in by intakeStep with an empty scan_result
    When the scanStep and ocrStep activities of the same run are observed on the item
    Then scanStep sets scan_result "CLEAN" on the item before ocrStep reads it
    Then no OCR call is made for the item while scan_result is empty

  Scenario: AC13 An email with no usable attachment (legacy RWB-E1-057 AC13)
    Given an email to "MBX-RECOVERY-01" with no attachment
    Given an email with only a 6 KB signature image
    When the job runs
    Then the system writes no document_intake row for either email
    Then both emails are in the archive folder

  Scenario: AC14 Outside business hours no run starts (new, D-RCV-60)
    Given the time is 18:15 on a working day
    When the trigger for JOB-12 is due
    Then no run starts at 18:15
    Then the next run starts at 08:00 the next working day

  Scenario: AC15 A case owner without Platform administration U cannot rerun (new, D-RCV-60)
    Given a user holds RW-CASEOWN and no Platform administration right U
    When the user posts a rerun of the failed JOB-12 run to the P1 job contract
    Then P1 refuses the call with status 403 and MSG-P4-002
    Then no run is started

  Scenario: AC16 All four channels end in one intake item and one workflow, with the partner check in evidence (new, D-RCV-60)
    Given one file on each of the four channels: "scan-0001.pdf" on "BR-0123", "mailroom-0001.pdf" on "MAILROOM", "LF-007-notice-0001.pdf" on "LF-007" and "reply-0001.pdf" on "MBX-RECOVERY-01"
    When the 09:15 run completes
    Then each file has exactly one intake item read through GET /api/recovery/document/v1/intake-items/{intakeItemId}
    Then one DocumentIntakeWorkflow execution holds the four items of the run
    Then the run evidence records the S9 partner check that returned panel_status "ACTIVE" for "LF-007"
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Scanner and mailroom files have source SCAN; partner SFTP files PARTNER; mailbox attachments EMAIL, and every one of them is read back through the P5 intake contract | RWB-E1-057 BR1; LOV-DOC-SOURCE; DF-DOC-046 |
| BR2 | Only the allowed types up to the size limit are taken in; the type is checked by content and extension | RWB-E1-057 BR2; INTAKE_ALLOWED_TYPES, INTAKE_MAX_FILE_MB (25 MB assumed); VR-P5-001-1 |
| BR3 | Every file taken in is scanned for malware by scanStep before ocrStep reads it | RWB-E1-057 BR3; REQ-DCM-010; FEAT-DCM-18; RWB-E1-041 |
| BR4 | A partner file is taken in only from the subfolder of a partner whose panel_status is ACTIVE, read through the S9 rwb-partner contract | RWB-E1-057 BR4; DF-PRT-002, DF-PRT-005; Architecture v5 slide 41 (S9 owns the panel) |
| BR5 | A file with the same hash from the same channel inside the window is a duplicate | RWB-E1-057 BR5; INTAKE_DUPLICATE_WINDOW_DAYS (30 assumed); R-UNI-40 |
| BR6 | A source file is moved or an email archived only after the intake row is committed | RWB-E1-057 BR6; Events rule "Transactions" |
| BR7 | JOB-12 runs every 15 minutes in business hours, once across instances; two failed runs in a row on a channel raise an alert; the run and its counts are read through the P1 rwb-source-data job contract | RWB-E1-057 BR7; JOB-12; Architecture v5 slide 44 |
| BR8 | Folders and mailboxes are properties; types, sizes and windows are parameters — rows of the P5 document hub parameter table whose owner the Ownership Map names, read through the parameters contract of P3 and its client library where a value is a case-workflow parameter; none is code | RWB-E1-057 BR8; Principle 1; DP-06; DP-07 |
| BR9 | The sender address is personal data: masked by role and never logged | RWB-E1-057 BR9; CTL-11; DL26 |

Every read behind these rules is one hop with a 2 s timeout (ADR-020, DP-11). The suite reads no other service's tables: the partner panel comes through the S9 contract, the intake item through the P5 contract, the run through the P1 contract and the rights through the P4 contract.

### 9. State transitions

None for the case status: this story changes no case status. It observes the intake row that intakeStep creates with an empty scan_result and ocr_status PENDING; scanStep and ocrStep move it on.

| Object | State | Meaning |
|---|---|---|
| Intake item | scan_result empty, ocr_status PENDING | intakeStep committed the row; the file is in the intake container and the source file has been moved |
| Intake item | scan_result CLEAN, ocr_status PENDING | scanStep has read the file; ocrStep may now take it |
| Intake item | scan_result INFECTED | scanStep quarantined the file; ocrStep never reads it (RWB-E1-041) |
| Intake item | ocr_status DONE or RESCAN | ocrStep has read the file (RWB-E1-049) |
| Run | running, failed, complete | The JOB-12 run state on SCR-44, with the intakeStep counts per channel |

The suite reads these states through the P5 contract and the P1 job contract and never writes them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, reads the evidence report |
| SY-OCR, OCR and extraction pipeline | Runs intakeStep; reads the four channels; writes document_intake and the intake container (Documents CRU) |
| RW-PLATADM, platform administrator | Sees runs on SCR-44 and reruns JOB-12 (Platform administration CRUD); sets the channel properties |
| RW-AGENCYMG, partner and agency manager | Keeps the partner codes and panel status that BR4 reads (Partner portal CRUDA) |
| RW-CASEOWN, case owner | Reads documents from intake once attached (Documents R); holds no Platform administration right U |
| P5 rwb-document owner | Owns document_intake, the intakeStep activity and the four channel readers |
| S9 rwb-partner owner | Owns the partner panel and the partner contract the intake calls |
| P1 rwb-source-data owner | Owns the job view and the rerun operation |
| P4 rwb-access owner | Owns the role and right model behind the refusal |

No other role is in scope for this story. The suite acts as the QA integration engineer and asserts the other roles only through the contracts.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner (S9 rwb-partner) | id | Read, through the S9 partner contract |
| DF-PRT-002 | partner (S9 rwb-partner) | partner_code | Read, through the S9 partner contract |
| DF-PRT-004 | partner (S9 rwb-partner) | partner_type | Read, through the S9 partner contract |
| DF-PRT-005 | partner (S9 rwb-partner) | panel_status | Read, through the S9 partner contract |
| DF-DOC-046 | document_intake (P5 rwb-document) | source | Read, written by the owning service |
| DF-DOC-047 | document_intake (P5 rwb-document) | source_ref | Read, written by the owning service |
| DF-DOC-048 | document_intake (P5 rwb-document) | channel_code | Read, written by the owning service |
| DF-DOC-049 | document_intake (P5 rwb-document) | file_name | Read, written by the owning service |
| DF-DOC-050 | document_intake (P5 rwb-document) | file_size | Read, written by the owning service |
| DF-DOC-051 | document_intake (P5 rwb-document) | captured_at | Read, written by the owning service |
| DF-DOC-052 | document_intake (P5 rwb-document) | sender_address | Read, written by the owning service, masked in every response and absent from the job record and the logs |
| DF-DOC-053 | document_intake (P5 rwb-document) | partner_id | Read, written by the owning service |
| DF-DOC-054 | document_intake (P5 rwb-document) | run_id | Read, written by the owning service |
| DF-DOC-055 | document_intake (P5 rwb-document) | received_at | Read, written by the owning service |
| DF-DOC-056 | document_intake (P5 rwb-document) | file_sha256 | Read, written by the owning service |
| DF-DOC-057 | document_intake (P5 rwb-document) | intake_ref | Read, written by the owning service |
| DF-REF-246 | document_hub_parameter (P5 rwb-document) | param_value | Read |

The legacy story writes document_intake; in this suite P5 rwb-document writes it and the suite only reads it through the P5 contract. scan_result and ocr_status are read through the same contract and their field IDs are those in the Logical Data Model and Data Dictionary. The partner panel comes through the S9 contract, the run through the P1 contract and the rights through the P4 contract. Field IDs are those in the Logical Data Model and Data Dictionary. Every row in the suite is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — /api/recovery/integration/v1, rwb.integration.events.v1, rwb-integration and rwb_integration — are not used.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/partner/v1/partners | S9 rwb-partner | Read partner_code and panel_status before the SFTP channel takes a file: "LF-007" ACTIVE, "LF-008" SUSPENDED and no row for "LF-099" |
| GET /api/recovery/document/v1/intake-items/{intakeItemId} | P5 rwb-document | Read source, channel_code, captured_at, file_sha256, scan_result and ocr_status of every item taken in |
| GET /api/recovery/document/v1/documents/{documentId} | P5 rwb-document | Read the document a taken-in item becomes after matching |
| GET /api/recovery/document/v1/cases/{caseId}/documents | P5 rwb-document | Confirm a taken-in document reaches the case through the same hub |
| GET /api/recovery/source-data/v1/admin/jobs | P1 rwb-source-data | Read the JOB-12 run, its state and the intakeStep counts per channel |
| POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun | P1 rwb-source-data | Rerun a failed run, and post the refusal for a user without the Platform administration right U |
| GET /api/recovery/access/v1/me/session | P4 rwb-access | Read the roles and rights of the calling user for the refusal of AC15 |

Every call is one hop with a 2 s timeout (ADR-020, DP-11).

#### 12.3 Events published

None. The suite publishes no event.

#### 12.4 Events consumed

None. The intake step publishes no event in the event catalogue: DocumentStored on rwb.document.events.v1 is raised when a document is stored after matching, not by intakeStep (Architecture v5 slide 16; Ownership Map). The suite therefore polls the P5 intake contract of section 12.2 for the item, and no event is invented for the intake step.

#### 12.5 Workflows and activities

| Workflow or activity | Owner | Task queue | Use |
|---|---|---|---|
| DocumentIntakeWorkflow | P5 rwb-document | rwb-document | Observed only: the intake step takes the four channels, then scanStep and ocrStep run in the same run |

The workflow reads and writes only the rwb_document schema. No workflow, activity or the suite reads another service's schema.

#### 12.6 Schedules

None. JOB-12 is event-started with KEDA workers on queue rwb-document, not a Temporal Schedule (Architecture v5 slide 44). The 15-minute cadence, the 08:00-18:00 window and the working-day rule are the trigger configuration of the P5 workflow kit; this story creates and asserts no Schedule.

#### 12.7 Tables owned

None (DP-01). document_intake and document_hub_parameter are P5 tables; partner is an S9 table.

#### 12.8 Contract fakes

| Stub | Use |
|---|---|
| Branch and mailroom folder fixture | Holds the scanner folders by branch code and the mailroom folder with the processed and rejected folders under them |
| Partner SFTP folder fixture | Holds the SFTP inbound root with one subfolder per partner_code and its processed and rejected folders |
| Mailbox stub | Stands in for the recovery mailboxes; Exchange Online read through Microsoft Graph is outside the 19 services and is not called |
| Intake-container fault switch | Makes the intake container refuse writes for the failed-run scenario and restores it |

The S9 partner rows are real synthetic SIT rows and no service contract is faked: every call in section 12.2 goes to the real SIT service.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 7 |
| Kafka | 0 | 0 |
| Temporal | 0 | 1 workflow observed (DocumentIntakeWorkflow) |
| File | 0 | 4 (branch folder, mailroom folder, partner SFTP folder, mailbox) |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the sixteen scenarios against SIT and holds no service code |
| Intake fixture pack | Test data | Synthetic files for the branch, mailroom, partner SFTP and mailbox channels, including the DOCX, the 25.1 MB and 25.0 MB PDFs and the 6 KB image |
| Channel fixtures and mailbox stub | External stubs | The four channel endpoints of section 12.8 with processed, rejected and archive folders |
| Container fault switch | Harness control | Makes the intake container refuse writes and restores it |
| Instance and clock controls | Harness controls | Starts the second rwb-document instance and moves the clock to 18:15 and to 2 December |
| Evidence report | Report | Records per scenario the run id, the counts per channel, the item fields, the contract responses and the messages |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | recovery.<table>, "recovery schema" | Owner's schema rwb_<name>; never read another service's tables | none | document_intake and document_hub_parameter stay in rwb_document (P5); the suite asserts through the P5 contract only |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On the APP stories; the five intake values are rows of the P5 document hub parameter table, read as data |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories; the source LOV and the working-day calendar are reference data read through the contracts |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On the APP stories; the intake step publishes no event, so the suite consumes none and polls the P5 contract |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | JOB-12 is the intake step inside DocumentIntakeWorkflow, event-started with KEDA workers on queue rwb-document (Architecture v5 slide 44) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The seven consumed operations of section 12.2, including the PartnerDirectory call of the legacy story as the S9 partner contract |
| DP-13 | /api/recovery/v1 | /api/recovery/<short>/v1 | none | Every consumed path in section 12.2, including the P1 rerun path that was the monolith admin job rerun |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On the APP stories; the suite changes no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The run is seen on SCR-44 and the documents on SCR-30 through gateway-bff; no screen is exercised here |

The dependency-added column records the build dependency of the owning story. This story has no build dependency: an ITG story waits on no build of its own. The H, C, I and X lists are exactly as the metadata table: no H, no C, no X, and the two I dependencies RWB-P5-E1057-APP and RWB-S9-E1057-APP.

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints of P5, S9, P1 and P4.
2. Build the fixture pack: the branch, mailroom, partner SFTP and mailbox files, the DOCX, the 25.1 MB and 25.0 MB PDFs, the 6 KB image and the hash "H1" pair for 30 November and 2 December.
3. Add the four channel fixtures, the mailbox stub and the container fault switch, and the instance and clock controls.
4. Implement AC1 to AC3 and AC16 — the four channels, the taken-in items and the single workflow — and assert only through the contracts of section 12.2 and Temporal visibility.
5. Implement AC4 to AC7: the type and size refusals, the partner check through the S9 contract and the unknown and suspended partner rows.
6. Implement AC6 and AC9: the duplicate across two dates and the empty run with zero counts.
7. Implement AC8, AC10, AC11 and AC12: the container fault, the two failed SFTP runs and the alert, the two instances, and the scan-before-OCR order.
8. Implement AC13 to AC15: the email with no usable attachment, the trigger at 18:15 and the refusal of a user without the Platform administration right U.
9. Write the evidence report with the counts per channel, the item fields, the partner check and the message ids, and keep it with the wave exit evidence.

Done when: all eighteen test cases pass in SIT against the published wave 1 contracts, the evidence report is attached to the wave exit pack, no sender address appears in any log or in the job record, and no service code or schema was changed by this story.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | A file type is not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-017 | A file is above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-007 | A file is refused at intake | {source} file {file} was not taken in: {reason}. It is in the {folder} folder. |
| MSG-P5-008 | Two intake runs in a row fail on one channel | Document intake failed twice in a row for {channel}. Check the interface and job monitor. |
| MSG-GEN-006 | The intake container is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

The message IDs and wording are copied from RWB-E1-057. No new message ID is added by this story. Thai text for each message follows decision DL10.

The evidence report also carries the counts line of every run: {channel} took in {taken}, refused {refused} and counted {duplicates} as duplicates, with the reason of each refusal.

### 15. Screens and states

No screen in this story. The platform administrator sees each JOB-12 run on SCR-44 Interface and job monitor in the states running, failed and complete, with the intakeStep counts per channel, and reruns a failed run there through the P1 job contract. The case owner sees intake documents on SCR-30 Case documents once RWB-E1-032 attaches them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-057-01-ITG | AC1 | Integration | Synthetic PDF of 1.2 MB in the scanner folder of branch BR-0123, captured 2026-11-30 09:12; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-02-ITG | AC2 | Integration | Synthetic PDF in the SFTP subfolder LF-007; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-03-ITG | AC3 | Integration | Mailbox stub with one PDF attachment, synthetic sender; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-04-ITG | AC1 | End to end | Synthetic PDF in the mailroom folder, run at 09:15; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-05-ITG | AC4 | Component | DOCX file in the scanner folder of branch BR-0123; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-06-ITG | AC4 | Integration | Files of 25.1 MB and 25.0 MB in the scanner folder of branch BR-0123; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-07-ITG | AC5, AC7 | Contract | Subfolders LF-099 with no partner_code and LF-008 with panel_status SUSPENDED, read through the S9 partner contract; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-08-ITG | AC6 | Integration | Same file with hash H1 from branch BR-0123 on 30 November and 2 December; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-09-ITG | AC9 | Integration | All four channels empty; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-10-ITG | AC8 | Component | Intake-container fault switch refusing writes, then restored; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-11-ITG | AC10 | NFR | SFTP subfolder unreadable for the 10:00 and 10:15 runs, available at 10:30; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-12-ITG | AC11 | NFR | Two rwb-document instances, one file on each of the four channels, one 09:15 run; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-13-ITG | AC13 | Integration | Email with no attachment and email with only a 6 KB image; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-14-ITG | AC6 | Integration | Same file with hash H1 seen again after the move to processed; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-15-ITG | AC14 | Integration | Clock at 18:15 on a working day; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-16-ITG | AC12 | Integration | Item taken in with an empty scan_result, scanStep and ocrStep observed in one run; real services on the wave 1 contracts; no numeric business values added |
| TC-E1-057-17-ITG | AC15 | Contract | RW-CASEOWN user without the Platform administration right U posts the rerun to the P1 job contract; refused with 403 and MSG-P4-002; real services on the wave 1 contracts; no numeric business values added |
| TC-ITG-E1057-ITG-18 | AC16 | End to end | One file on each of the four channels in one 09:15 run, the P5 intake item and the DocumentIntakeWorkflow execution with the S9 partner check; real services on the wave 1 contracts; no numeric business values added |

The legacy full test text is in Recovery Workbench Test Cases v7.xlsx under the legacy test case id.

### 17. Guardrails

- No business value in code: the folders, the mailbox codes, the allowed types, the size limit, the duplicate window and the alert count are properties and data rows.
- No personal data in logs, events, evidence or fixtures: the sender addresses and the email file names are not logged, and the sender address is masked in every response and absent from the job record; test emails use synthetic senders.
- No read of another service's tables: the partner panel comes only through the S9 contract, the intake item and the document through the P5 contract, the run through the P1 contract and the rights through the P4 contract.
- A file is never removed from a channel before its intake row is committed; the suite asserts the order commit then move.
- Storage is reached by managed identity only, never by key or shared access signature (RWB-TE-012).
- One hop and a 2 s timeout on every call (ADR-020).
- Synthetic data only; the harness RWB-ITG-W1J01-ITG loads the fixtures.
- No production access of any kind from the suite or its configuration.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, mailroom, partner file transfer and email through the same intake | The intake item read through the P5 contract for each of the four channels; one item per file and one workflow | TC-E1-057-01-ITG, TC-E1-057-02-ITG, TC-E1-057-03-ITG, TC-E1-057-04-ITG, TC-ITG-E1057-ITG-18 |
| REQ-DCM-010 | Virus scan before storing; retention class on every document | scan_result empty at intake and CLEAN before ocrStep reads the item | TC-E1-057-16-ITG, TC-ITG-E1057-ITG-18 |
| DP-01 | Owner's schema, never another service's tables | document_intake and document_hub_parameter in rwb_document, read only through the P5 contract | All |
| DP-06 | Parameters contract of rwb-case and the client library | The five intake values read as data rows; the parameters contract behind them | TC-E1-057-06-ITG, TC-E1-057-08-ITG |
| DP-09 | Kafka with outbox, inbox and CloudEvents | No event is published or consumed by the intake step; the suite polls the P5 contract | TC-ITG-E1057-ITG-18 |
| DP-10 | Temporal replaces Quartz; event-started workflow | JOB-12 as the intake step inside DocumentIntakeWorkflow on queue rwb-document, with KEDA workers | TC-E1-057-09-ITG, TC-E1-057-11-ITG, TC-E1-057-12-ITG, TC-E1-057-15-ITG |
| DP-13 | /api/recovery/<short>/v1 | The seven consumed paths of section 12.2, including the P1 rerun path | TC-E1-057-17-ITG, TC-E1-057-09-ITG |
| DP-19 | gateway-bff composite route | SCR-44 for the run and SCR-30 for the documents, not exercised here | TC-E1-057-09-ITG |
| ASM-0496 | The partner check reads S9 rwb-partner by partner_code and P5 holds no partner or panel copy | GET /api/recovery/partner/v1/partners for LF-007, LF-008 and LF-099 | TC-E1-057-02-ITG, TC-E1-057-07-ITG |
| ASM-0497 | The channel locations are P5 environment properties and the five INTAKE values stay rows of rwb_document.document_hub_parameter | The five values read as data; the folders and mailboxes read as properties | TC-E1-057-05-ITG, TC-E1-057-06-ITG, TC-E1-057-08-ITG, TC-E1-057-11-ITG |
| ASM-0498 | JOB-12 is an event-started intake step in DocumentIntakeWorkflow on queue rwb-document with KEDA workers, not Quartz | One DocumentIntakeWorkflow execution per 09:15 run; no shared Quartz table | TC-E1-057-09-ITG, TC-E1-057-11-ITG, TC-E1-057-12-ITG, TC-E1-057-15-ITG |
| ASM-0499 | The job view and the rerun stay with P1 rwb-source-data and the Platform administration right with P4 rwb-access | GET /admin/jobs, POST /admin/jobs/{jobId}/rerun and GET /me/session | TC-E1-057-09-ITG, TC-E1-057-17-ITG |
| ASM-0500 | The recovery mailbox is Exchange Online through Microsoft Graph, outside the 19 services, and is stubbed | The mailbox stub of section 12.8; no production mailbox and no real sender address | TC-E1-057-03-ITG, TC-E1-057-13-ITG |
| ASM-0501 | All four channels end in one P5 intake item and the same DocumentIntakeWorkflow, read through the P5 contracts | The intake item read for each channel and one workflow execution for the 09:15 run | TC-ITG-E1057-ITG-18 |

The legacy story is RWB-E1-057. The integration dependencies are RWB-P5-E1057-APP and RWB-S9-E1057-APP; the legacy AC1, AC4, AC5, AC6, AC8, AC10, AC11, AC12, AC14, AC15 and AC16 at component level belong to those stories, not to this one.

### 19. Out of scope

- The APP and CON builds of P5 rwb-document and S9 rwb-partner and their unit and component tests.
- The malware scan and quarantine itself (RWB-E1-041), OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching to a case (RWB-E1-032).
- Uploads from the case documents screen (RWB-E1-026).
- Field app photos and bills (RWB-E2-024).
- Partner uploads through the partner portal (Epic 4, PRT-03; partner access DL03).
- The build of the harness RWB-ITG-W1J01-ITG.
- NFR load and performance testing, which belongs to the NFR epic.

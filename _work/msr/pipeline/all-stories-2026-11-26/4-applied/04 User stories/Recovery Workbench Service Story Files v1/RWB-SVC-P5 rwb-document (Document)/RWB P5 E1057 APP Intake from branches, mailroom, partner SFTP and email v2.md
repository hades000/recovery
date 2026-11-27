# RWB-P5-E1057-APP Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1057-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-057 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1049-APP |
| Depends on (build) | RWB-P5-E1057-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1049-APP, RWB-P5-E1041-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-PLT-TE012-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-020, FR-P5-022, FR-P5-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the channel pickup of RWB-E1-057 moves into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the `pickup` activity of `DocumentIntakeWorkflow` on queue `rwb-document` in namespace `rwb-recovery` and the contract baseline RWB-P5-E1057-CON; the twelve exception paths, the nine business rules, the six messages and the seventeen test cases are kept word for word in intent and values, and the eleven criteria this story owns are carried verbatim while the five partner-panel and mailbox criteria pass to RWB-S9-E1057-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P5-E1057-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded**, so that **every document path ends in the document hub**.

Inside `rwb-document` this is the channel pickup capability of the document intake, and the same user story holds with the target service frame:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The pickup is one activity, `pickup`, of `DocumentIntakeWorkflow` on queue `rwb-document`, and the workflow is owned and registered by RWB-P5-E1049-APP. The legacy `IntakeStep` of the `DocumentIntakeJob` becomes this activity; it runs first, before `scanIntakeItem` of RWB-P5-E1041-APP and before the OCR step (DP-10, H RWB-PLT-E1071-CON).
- The legacy Quartz cron `0 0/15 8-17 ? * MON-FRI` and the shared scheduler table are gone: the intake is a Temporal Schedule started through the workflow kit, registered from the values of RWB-P5-E1057-OPS on queue `rwb-document` in namespace `rwb-recovery`, and this story contributes the activity the Schedule-started workflow calls.
- The five intake parameters `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB`, `INTAKE_DUPLICATE_WINDOW_DAYS`, `INTAKE_MIN_IMAGE_KB` and `INTAKE_ALERT_AFTER_FAILURES` are read through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON). The rows they resolve to stay in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5.
- The source enumeration, the scan result and the OCR status are read as reference data through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON): LOV-DOC-SOURCE, LOV-SCAN-RESULT and LOV-OCR-STATUS. No list value is typed in code.
- The partner panel that BR4 reads is not a table of this service: the partner is read by code and by panel status through the `rwb-partner` contract of S9, one hop with a 2 s timeout and a breaker (DP-11), never from a `partner` table. The read is consumed and faked although the plan lists no C row for it (ASM-1830).
- The channel definitions — branch scanner folders by branch code, the mailroom folder, the partner SFTP inbound root with one subfolder per partner code, the recovery mailboxes, and the processed, rejected and archive folder names — are environment properties and never code (BR8). The property layout is this story's; the values are RWB-P5-E1057-INF's (X).
- An accepted file is copied to the hold container `rwb-quarantine` through the platform storage product RWB-PLT-TE012-APP by managed identity, and the `document_intake` row is written in `rwb_document` by this service's own per-service Flyway sequence (DP-15, H RWB-PLT-E1044-CON). The legacy name "the intake container" and the target hold container are read as one container (ASM-1828).
- The migration is one step of the per-service Flyway sequence and never the legacy `V0001` baseline (DP-15); the run record and the rerun of a failed run are reached through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON) behind the legacy `/api/recovery/v1` path rebased to `/api/recovery/document/v1` (DP-13).
- The idempotency key of a picked-up file is the legacy one — channel code, source reference and file hash — and it is held by the idempotency and inbox library of DP-09 (H RWB-PLT-TE006-CON). This story publishes no event: `DocumentStored` (EV-16) is written by the store and `DocumentFieldsExtracted` by extraction, and no third event name is invented (ASM-1827).
- The legacy feature flag `rwb.dochub.intake` and its four sub-flags are retired with the monolith and replaced by `rwb.document.intake` with `rwb.document.intake.branch`, `.mailroom`, `.sftp` and `.email` (ASM-1835).

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, twelve exception paths, nine business rules, states, authority, data fields, six messages, seventeen test cases and out-of-scope list, adapted to the target service's schema, topic, API base and workflow template. This story owns the eleven legacy criteria AC1, AC4, AC5, AC6, AC8, AC10, AC11, AC12, AC14, AC15 and AC16; the remaining five criteria of the same legacy key — AC2 Partner SFTP, AC3 Mailbox, AC7 An unknown or suspended partner is refused, AC9 An empty run and AC13 An email with no usable attachment — are the partner-panel and mailbox slice of RWB-S9-E1057-APP in `rwb-partner`, which proves them against the partner panel and the mailbox fake (section 7, section 19).

### 2. Business rationale

Documents reach recovery today by courier, shared folders and personal email, and an original that goes to the wrong desk is rebuilt for each audit. This story reads the four inbound paths every 15 minutes into the document intake, records where each file came from, refuses files that are not allowed or come from an unknown partner, and leaves every accepted file for the malware scan and OCR steps, so a document received in the morning is on the case the same day. It meets REQ-DCM-009 and puts every inbound file through the virus scan of REQ-DCM-010, and removes email hand-offs of customer documents (CTL-11).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1`, the legacy monolith base rebased by DP-13. No table of another service is read and no monolith table name survives (DP-01).
2. The legacy job step is no longer a step of a Spring Batch job on a shared scheduler: it is the `pickup` activity of `DocumentIntakeWorkflow` started by a Temporal Schedule on the service's own queue (DP-10). The legacy `JobRecord` row and its counts become the intake run record of this service, read through the gateway-bff composite route (DP-19).
3. The partner is no longer read in process through `PartnerDirectory`: it arrives through the `rwb-partner` contract with a mock and a 2 s timeout (DP-11), so the intake builds against a published shape and its fake on Day 1.
4. The five intake parameters and the three lists arrive through the parameters and reference-data contracts of `rwb-case` (DP-06, DP-07); the parameter rows stay in `rwb_document`, which is P5's own store for them, and no type list, size limit or duplicate window is typed in code.
5. The duplicate rule of R-UNI-40 is executed twice over: by the selection rule of `pickup` and by the unique constraint `uk_intake_channel_ref` on channel code, source reference and file hash, so a file seen again on the run after a failed move creates no second row.
6. The file is copied to the hold container by managed identity only, on the storage product of the platform, and no container is reached by key or shared access signature.
7. The intake tables are created in the per-service Flyway sequence (DP-15), so the legacy `V0001` baseline and its `document_intake` widening are one step of this service's own schema.
8. The intakes of the partner panel and of the mailboxes are proved by the partner slice RWB-S9-E1057-APP, so the same legacy value is proved once and this story's eleven criteria keep their own values (section 7).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E1049-APP | `DocumentIntakeWorkflow` on queue `rwb-document`, its registration, its retry policy and the `ingest` and `ocr` activities the pickup runs before |
| RWB-P5-E1041-CON | The scan baseline of this service: `scan_result` CLEAN or INFECTED, the quarantine rule and the scan failure answers the `pickup` activity leaves untouched |
| RWB-P5-E1057-CON | The published baseline of the three run-record operations, the `IntakeRun` and `IntakeRunPage` shapes, the channel and result enumerations, the error envelope and the `Idempotency-Key` rule |
| RWB-PLT-E1042-CON | The parameters client library for the five intake parameters (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-DOC-SOURCE, LOV-SCAN-RESULT and LOV-OCR-STATUS (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library, so channel code, source reference and file hash lock a repeat pickup (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 "Document intake" template, the activity registration and the retry policy (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the intake migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the run record and the rerun action (DP-19) |
| RWB-PLT-TE012-APP | The platform storage product with the hold container `rwb-quarantine` and the claim-check read, reached by managed identity |
| RWB-P5-E1057-INF | The SFTP and mailbox pickup channels, the compute of the intake workers, the storage and hold container, the topic and ACLs, the identity and secrets, the partner gateway route and the scan capacity (the X dependency) |
| RWB-P5-E1057-OPS | The Helm release, the 15-minute intake Schedule, the flag, the dashboards, the alerts and the runbook (the X dependency) |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the five parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the three lists (DP-07) |

Business preconditions carried from RWB-E1-057, in the target wording:

- RWB-E1-049 is done: JOB-12 Document intake runs as the Spring Batch job DocumentIntakeJob with ordered steps, and the table document_intake exists. In the target this is RWB-P5-E1049-APP in the same service: `DocumentIntakeWorkflow` with the `ingest` and `ocr` activities, and `document_intake` in `rwb_document`.
- RWB-E1-041 is done: scanStep runs before ocrStep and quarantines infected files. In the target this is RWB-P5-E1041-APP and its `scanIntakeItem` activity in the same workflow.
- RWB-TE-012 is done: the intake and quarantine containers exist and SY-OCR writes to the intake container by managed identity. In the target the two are one hold container `rwb-quarantine` reached through RWB-PLT-TE012-APP by managed identity (ASM-1828).
- The channels are set per environment by the platform administrator: branch scanner folders by branch code, the mailroom folder, the partner SFTP inbound folder with one subfolder per partner_code, and the recovery mailboxes. The mailboxes are read by the service identity; the mail service is assumed to be Exchange Online read through Microsoft Graph (no open decision covers it) and the assumption and the capacity around it are RWB-P5-E1057-INF's.
- Partner panel rows are loaded by the partner and agency manager and are readable through the `rwb-partner` contract of S9, one hop with a 2 s timeout (DP-11, ASM-1830).
- Rows in `document_hub_parameter`: INTAKE_ALLOWED_TYPES PDF, JPG, PNG; INTAKE_MAX_FILE_MB 25; INTAKE_DUPLICATE_WINDOW_DAYS 30; INTAKE_MIN_IMAGE_KB 10; INTAKE_ALERT_AFTER_FAILURES 2. All assumed (DL11) and all read through the parameters contract of DP-06.
- Feature flag `rwb.document.intake` is on; it replaces the legacy `rwb.dochub.intake` (ASM-1835).
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1826), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1747).

The names of the three run-record operations and the field names of the run record are Not specified in the source documents (GAP-1012; ASM-1829); the baseline RWB-P5-E1057-CON fixes the names this story is built against. The Ownership Map gives `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` to P1 `rwb-source-data`, so those operation names are not declared here and the run record of this service's own Schedule is served under the service's run resource (ASM-1829).

### 4. Flow

1. Scheduler: the intake Schedule starts `DocumentIntakeWorkflow` on queue `rwb-document` every 15 minutes in business hours; `pickup` runs first, before `scanIntakeItem` and before the OCR step (DP-10).
2. `pickup`: lists new files in each branch scanner folder and the mailroom folder, in each partner subfolder of the SFTP inbound root, and new messages in each recovery mailbox.
3. `pickup`: for each file or email attachment computes the SHA-256 hash and checks `document_intake` for the same channel and hash inside the duplicate window; the idempotency row of DP-09 closes the window of a repeat within one run.
4. `pickup`: checks the file type by content and extension, and the size, against the parameters read through DP-06.
5. `pickup`: for a partner file, reads the partner by the subfolder's partner code through the `rwb-partner` contract (DP-11) and checks that its panel status is ACTIVE.
6. `pickup`: copies an accepted file to the hold container `rwb-quarantine` through the storage product and writes one `document_intake` row with source, channel code, source reference, file name, size, hash, received time, scanner time (scanner files), partner ID (partner files) or sender address (email), and the run ID; `scan_result` is left empty for the scan step.
7. `pickup`: after the commit, moves the scanner or SFTP file to the processed folder, or moves the email to the archive folder; a refused file goes to the rejected folder.
8. `pickup`: writes the counts per channel and result (taken in, refused by reason, duplicate) to the intake run record this service owns and serves through the gateway-bff composite route (DP-19); the SCR-44 Interface and job monitor of Epic 2 reads it there.
9. `scanIntakeItem`, `ocr` and `ingest` (RWB-P5-E1041-APP and RWB-P5-E1049-APP) and then the classification, extraction and match steps (RWB-P5-E1050-CON, RWB-P5-E1053-CON and RWB-P5-E1032-APP) run on the new rows in the same workflow run.
10. Platform administrator: sees the run record in the states running, failed and complete and reruns a failed run through the rerun operation of 12.1, which starts one workflow run for the failed window with the same idempotency key.

The row is committed before any file leaves a channel, so a file is never removed from a channel before its `document_intake` row exists, exactly as the legacy section 17 states. A file that fails the move is seen again on the next run and counted as a duplicate.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | File type not allowed | No intake row; file moved to the rejected folder; counted as refused; audit event | MSG-P5-001, MSG-P5-007 | AC5 |
| X2 | File above the size limit | No intake row; file moved to the rejected folder | MSG-P5-017, MSG-P5-007 | AC6 |
| X3 | Partner subfolder code unknown or partner not ACTIVE | No intake row; file moved to the rejected folder | MSG-P5-007 | AC7 |
| X4 | Same hash from the same channel inside the window | No new row; file moved to processed; counted as duplicate | None | AC8 |
| X5 | No new file on any channel | Run logged with zero counts | None | AC9 |
| X6 | The intake container does not accept writes | Files left at the channel; run failed; next run takes them | MSG-GEN-006 | AC10 |
| X7 | Two runs in a row fail on one channel | Alert to the platform administrator | MSG-P5-008 | AC11 |
| X8 | Two service instances are due at once | The job runs once | None | AC12 |
| X9 | Email with no attachment, or only images under 10 KB | Email archived; no intake row | None | AC13 |
| X10 | The move to processed fails after the commit | The file is seen again on the next run and counted as a duplicate | None | AC14 |
| X11 | The time is outside business hours | No run | None | AC15 |
| X12 | A user without Platform administration U reruns the job | 403 | MSG-P4-002 | Access test TC-E1-057-17 |

Three target-service notes:

- The container of X6 is the hold container `rwb-quarantine` reached through RWB-PLT-TE012-APP; a refused write is answered by the storage product and the activity fails before any row is committed, so the file stays at its channel exactly as the legacy path states.
- "The job runs once" of X8 is the overlap policy of the Schedule — skip, with a catch-up window of one run — together with a workflow ID keyed by the run slot, so a second workflow run for the same slot is refused by Temporal and never by a cluster lock (ASM-1832).
- X3, X5 and X9 prove criteria owned by RWB-S9-E1057-APP; they are kept here because they are the same legacy key and the same exception set, and the pickup that counts them is one activity (section 7).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds the first activity to the `DocumentIntakeWorkflow` of RWB-P5-E1049-APP; the scan and OCR activities exist and the contract baseline is published |
| Negotiable | Channels, folders, types, sizes, windows and the alert threshold are properties and parameters read through DP-06 |
| Valuable | Every inbound path ends in the document hub with its source recorded |
| Estimable | One activity, three channel readers, seven columns, three admin operations, one migration |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic files |

### 7. Acceptance criteria

```gherkin
Feature: Intake from branches, mailroom, partner SFTP and email

  Background:
    Given JOB-12 Document intake runs every 15 minutes from 08:00 to 18:00 Asia/Bangkok on working days
    Given INTAKE_ALLOWED_TYPES is PDF, JPG and PNG and INTAKE_MAX_FILE_MB is 25
    Given the rwb-case contract mock returns the document-hub parameters INTAKE_ALLOWED_TYPES "PDF, JPG, PNG", INTAKE_MAX_FILE_MB 25, INTAKE_DUPLICATE_WINDOW_DAYS 30, INTAKE_MIN_IMAGE_KB 10 and INTAKE_ALERT_AFTER_FAILURES 2
    Given the rwb-case contract mock returns the reference lists LOV-DOC-SOURCE, LOV-SCAN-RESULT and LOV-OCR-STATUS
    Given the rwb-partner contract mock returns partner "LF-007" as a law firm with panel_status "ACTIVE"

  Scenario: AC1 Branch scan (legacy RWB-E1-057 AC1)
    Given file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12
    When the intake job runs at 09:15
    Then one document_intake row has source "SCAN", channel_code "BR-0123", captured_at 2026-11-30 09:12 and an empty scan_result
    Then the file is in the intake container at the row's intake_ref
    Then the file is no longer in the scanner folder and is in its processed folder

  Scenario: AC4 Mailroom scan (legacy RWB-E1-057 AC4)
    Given file "mailroom-0001.pdf" in the mailroom folder
    When the job runs
    Then one document_intake row has source "SCAN" and channel_code "MAILROOM"

  Scenario: AC5 A file type not allowed is refused (legacy RWB-E1-057 AC5)
    Given file "letter-0002.docx" in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system writes no document_intake row for it
    Then the file is in the rejected folder of branch "BR-0123"
    Then the job record shows 1 refused on "BR-0123" with MSG-P5-007 and reason MSG-P5-001

  Scenario: AC6 A file above the size limit is refused (legacy RWB-E1-057 AC6)
    Given file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system refuses "scan-0003.pdf" with reason MSG-P5-017 and moved to the rejected folder
    Then "scan-0004.pdf" has a document_intake row

  Scenario: AC8 A duplicate file is not taken in twice (legacy RWB-E1-057 AC8)
    Given file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November
    When the same file arrives again from branch "BR-0123" on 2 December
    Then the system writes no second document_intake row
    Then the system moves the file to the processed folder and counted as a duplicate

  Scenario: AC10 The intake container does not accept writes (legacy RWB-E1-057 AC10)
    Given the intake container refuses writes
    When the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123"
    Then the system writes no document_intake row
    Then "scan-0007.pdf" stays in the scanner folder
    Then on the next run with the container available the file is taken in

  Scenario: AC11 Two failed runs raise an alert (legacy RWB-E1-057 AC11)
    Given the run at 10:00 failed because the SFTP inbound folder could not be read
    When the run at 10:15 fails for the same reason
    Then the platform administrator receives MSG-P5-008 naming "PARTNER_SFTP"
    Then the run at 10:30 tries again

  Scenario: AC12 The job runs once across two instances (legacy RWB-E1-057 AC12)
    Given two service instances are running
    When the 09:15 run is due
    Then the system records one run for 09:15
    Then each file has one document_intake row

  Scenario: AC14 A file seen again after a failed move (legacy RWB-E1-057 AC14)
    Given file "scan-0008.pdf" was taken in at 11:00 and the move to the processed folder failed
    When the run at 11:15 sees "scan-0008.pdf" again
    Then the system writes no second document_intake row
    Then the system moves the file to the processed folder

  Scenario: AC15 Outside business hours (legacy RWB-E1-057 AC15)
    Given the time is 18:15 on a working day
    When the scheduler checks JOB-12
    Then no run starts until 08:00 the next working day

  Scenario: AC16 An item taken in is scanned before OCR (legacy RWB-E1-057 AC16)
    Given file "scan-0009.pdf" was taken in by intakeStep with an empty scan_result
    Given the rwb-document scan mock returns "CLEAN" for "scan-0009.pdf" when the scan step runs
    When ocrStep runs in the same job before scanStep has set scan_result
    Then ocrStep does not read "scan-0009.pdf"
    Then after scanStep sets scan_result "CLEAN" ocrStep reads it
```

Every Given, When and Then line above is the legacy line unchanged. The only added lines are the three Background mock Givens on the `rwb-case` and `rwb-partner` contracts and the one Given on the scan mock of AC16; the legacy Background line that names partner "LF-007" as a law firm with panel_status "ACTIVE" is kept word for word and carries the mock. "The job" and "JOB-12" are the intake Schedule that starts `DocumentIntakeWorkflow`, `intakeStep` is the `pickup` activity, and "the intake container" is the hold container `rwb-quarantine` (ASM-1828).

The remaining five criteria of the same legacy key belong to the other service slice: AC2 Partner SFTP, AC3 Mailbox, AC7 An unknown or suspended partner is refused, AC9 An empty run and AC13 An email with no usable attachment are owned and proved by RWB-S9-E1057-APP in `rwb-partner`, because they turn on the partner panel read and the mailbox reader of that service. This story owns AC1, AC4, AC5, AC6, AC8, AC10, AC11, AC12, AC14, AC15 and AC16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Scanner and mailroom files have source SCAN; partner SFTP files PARTNER; mailbox attachments EMAIL | LOV-DOC-SOURCE; DF-DOC-005 |
| BR2 | Only the allowed types up to the size limit are taken in; the type is checked by content and extension | INTAKE_ALLOWED_TYPES, INTAKE_MAX_FILE_MB (25 MB assumed); VR-P5-001-1 |
| BR3 | Every file taken in is scanned for malware by scanStep before ocrStep reads it | REQ-DCM-010; FEAT-DCM-18; RWB-E1-041 |
| BR4 | A partner file is taken in only from the subfolder of a partner whose panel_status is ACTIVE | DF-PRT-002, DF-PRT-005; Partner panel reference table |
| BR5 | A file with the same hash from the same channel inside the window is a duplicate | INTAKE_DUPLICATE_WINDOW_DAYS (30 assumed); R-UNI-40 |
| BR6 | A source file is moved or an email archived only after the document_intake commit | Events rule "Transactions" |
| BR7 | JOB-12 runs every 15 minutes in business hours, once across instances; two failed runs in a row on a channel raise an alert | JOB-12; RWB-TE-007 |
| BR8 | Folders and mailboxes are properties; types, sizes and windows are parameters; none is code | Principle 1 |
| BR9 | The sender address is personal data: masked by role and never logged | CTL-11; DL26 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 executes through the reference list LOV-DOC-SOURCE read by the reference-data contract (DP-07); the three values SCAN, PARTNER and EMAIL are list rows and never literals, and the channel code is the folder, branch or mailbox code the property set names.
- BR2 executes in `IntakeService`: the allowed types come through DP-06, the type is checked by content and by extension, and the size boundary is compared against the parameter so that 25.0 MB passes and 25.1 MB is refused (AC6).
- BR3 is not executed here at all: `pickup` leaves `scan_result` empty and the scan of RWB-P5-E1041-APP sets it, so the OCR step of RWB-P5-E1049-APP reads only an item whose `scan_result` is CLEAN (AC16).
- BR4 executes in the partner SFTP reader against the `rwb-partner` contract (DP-11); a code that resolves to no partner and a partner whose panel status is not ACTIVE are two distinct refusals with the two reasons of AC7, and no partner row is copied into `rwb_document`.
- BR5 executes twice: the selection rule of `pickup` looks back inside the duplicate window, and the unique constraint `uk_intake_channel_ref (channel_code, source_ref, file_sha256)` refuses a second row whatever the window; the idempotency row of DP-09 closes the repeat inside a run.
- BR6 is the commit order of `pickup`: copy, row insert, commit, then the move; a failed move leaves the file at the channel and the next run counts it as a duplicate (AC14).
- BR7 is the Schedule's interval and overlap policy (DP-10) plus `IntakeAlertService`, which counts consecutive failed runs per channel and raises MSG-P5-008 at the parameter `INTAKE_ALERT_AFTER_FAILURES` (AC11, AC12).
- BR8 is executed by the property set of RWB-P5-E1057-INF and by the five parameter rows; a branch code, a folder name, a mailbox address, a type list or a size limit in code fails the review.
- BR9 is executed by never writing a sender address to a log, a metric, a workflow payload or the run record; the column `sender_address` is read only behind the masking rule of `rwb-access` and the PII access log of the ACE common module.

### 9. State transitions

None. This story does not change a case status. It creates `document_intake` rows with an empty `scan_result` and `ocr_status` PENDING; RWB-P5-E1041-APP and RWB-P5-E1049-APP move them on.

| From (`document_intake`) | Event | Condition | To |
|---|---|---|---|
| (no row) | `pickup` accepts a file | The type and the size pass and the hash is new inside the window | A row with `scan_result` empty and `ocr_status` PENDING |
| (no row) | `pickup` refuses a file | The type, the size, the partner or the container refuses it | No row; the file is in the rejected folder |
| A row with `scan_result` empty | `scanIntakeItem` of RWB-P5-E1041-APP scans it | The engine answers | `scan_result` CLEAN or INFECTED, and `scanned_at` |
| A row with `ocr_status` PENDING | The OCR step of RWB-P5-E1049-APP runs | `scan_result` is CLEAN | `ocr_status` DONE, RESCAN or FAILED |

The values of `scan_result` are the two of LOV-SCAN-RESULT and the values of `ocr_status` the four of LOV-OCR-STATUS; both lists are reference rows read through DP-07 and neither is typed in code. The file's own move state — at the channel, in the hold container, in the processed folder, in the rejected folder, in the archive folder — is a filesystem fact and not a column of any table.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs the `pickup` activity; reads the channels; writes `document_intake` and the hold container (Documents CRU) |
| RW-PLATADM, platform administrator | Sees the run record through the gateway-bff composite route and reruns a failed run (Platform administration CRUD); sets the channel properties |
| RW-AGENCYMG, partner and agency manager | Keeps the partner codes and panel status that BR4 reads (Partner portal CRUDA) |
| RW-CASEOWN, case owner | Reads documents from intake once attached (Documents R) |

In the target the authorisation decision is taken by `rwb-access` (roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds; this story adds no guard of its own and inherits the 403 shape of MSG-P4-002. The pickup runs unattended as the rwb-document service identity (DP-02), carried by the chart as a secret reference; the login name is Not specified in the source documents (GAP-1012; ASM-1829). The partner panel that RW-AGENCYMG keeps is S9's data and is reached through the `rwb-partner` contract, never by a copy.

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | `rwb-partner` partner, through the contract | id | Read, through the `rwb-partner` contract |
| DF-PRT-002 | `rwb-partner` partner, through the contract | partner_code | Read, through the `rwb-partner` contract |
| DF-PRT-004 | `rwb-partner` partner, through the contract | partner_type | Read, through the `rwb-partner` contract |
| DF-PRT-005 | `rwb-partner` partner, through the contract | panel_status | Read, through the `rwb-partner` contract |
| DF-DOC-046 | `document_intake` | source | Write |
| DF-DOC-047 | `document_intake` | source_ref | Write |
| DF-DOC-055 | `document_intake` | received_at | Write |
| DF-DOC-056 | `document_intake` | file_sha256 | Write |
| DF-DOC-057 | `document_intake` | intake_ref | Write |
| DF-DOC-048 | `document_intake` | channel_code | Write |
| DF-DOC-049 | `document_intake` | file_name | Write |
| DF-DOC-050 | `document_intake` | file_size | Write |
| DF-DOC-051 | `document_intake` | captured_at | Write |
| DF-DOC-052 | `document_intake` | sender_address | Write |
| DF-DOC-053 | `document_intake` | partner_id | Write |
| DF-DOC-054 | `document_intake` | run_id | Write |
| DF-DOC-045 | `document_intake` | id | Write |
| DF-DOC-058 | `document_intake` | scan_result | Write, empty at insert; the scan step of RWB-P5-E1041-APP sets it |
| DF-DOC-063 | `document_intake` | ocr_status | Write, PENDING at insert |
| DF-REF-246 | `document_hub_parameter` | param_value | Read, resolved through DP-06 |
| (idempotency) | idempotency library table in `rwb_document` | channel code, source reference and file hash | Write, through the library |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No partner row and no case row is copied into `rwb_document`: DF-PRT-001, DF-PRT-002, DF-PRT-004 and DF-PRT-005 arrive inside the `rwb-partner` contract answer, and DP-01 forbids a foreign-schema read. The run record of 12.1 is a projection of `document_intake` and of the activity's own counters and stores no message text, no file name and no sender address beyond the columns above. Personal data never enters a workflow input, a metric or a log: a log line carries the run ID, the channel code, the counts and the reason code, never a file name, a mailbox address or a sender address.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`; the shapes are those of RWB-P5-E1057-CON.

| Method | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/admin/jobs` | P5 | The intake run records, newest first: `runId`, the business date, the state (running, failed, complete), the counts per channel and the counts per result (taken in, refused by reason, duplicate); Platform administration right R, `page` and `size` with a default of 50; answer 200 `IntakeRunPage` |
| GET | `/api/recovery/document/v1/admin/jobs/{jobId}` | P5 | One intake run record as `IntakeRun`, with its channel rows, its reason counts, its start and end, its run ID and its Schedule ID; the record the SCR-44 Interface and job monitor of Epic 2 reads through the gateway-bff composite route (DP-19) |
| POST | `/api/recovery/document/v1/admin/jobs/{jobId}/rerun` | P5 | Reruns a failed intake run: starts one `DocumentIntakeWorkflow` execution for the failed window with the same idempotency key; 202 `IntakeRun` out, Platform administration right U, `Idempotency-Key` required; 409 when the run is still in progress (MSG-GEN-004), 404 when the run is unknown, 403 without the right (MSG-P4-002), 503 when the storage is unavailable (MSG-GEN-006). The legacy path `/admin/jobs/{jobId}/rerun` is rebased by DP-13; the names of these three operations and the fields of the run record are Not specified in the source documents (GAP-1012; ASM-1829) |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | the parameters read of DP-06 | P3 behind the client library | RWB-P3-E1042-CON | `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB`, `INTAKE_DUPLICATE_WINDOW_DAYS`, `INTAKE_MIN_IMAGE_KB` and `INTAKE_ALERT_AFTER_FAILURES`, cached for 5 minutes |
| GET | the reference-data read of DP-07 | P3 behind the client library | RWB-P3-E1043-CON | LOV-DOC-SOURCE, LOV-SCAN-RESULT and LOV-OCR-STATUS |
| GET | the partner-by-code read of rwb-partner | S9 rwb-partner | RWB-S9-E1057-APP | The partner ID, code, type and panel status of the SFTP subfolder's partner; one hop, 2 s timeout, breaker per downstream, one GET retry with jitter (DP-11); the exact path is Not specified in the source documents (GAP-1012; ASM-1830) and no C row of the plan carries it |

A failed parameters or reference-data read stops the activity before any file is taken in, and a failed partner read leaves the file at its channel and fails the run; both map to 503 with MSG-GEN-006 naming the system that failed when they surface on the rerun operation. The scan of a picked-up item is not a REST call of this story: it is the `scanIntakeItem` activity of RWB-P5-E1041-APP inside the same workflow run.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| None | — | — | — | This story publishes no event. `DocumentStored` (EV-16) is written by the store of RWB-P5-E1024-APP and `DocumentFieldsExtracted` by the extraction of RWB-P5-E1053-APP, and neither belongs to the pickup. No third event name is invented for the pickup (ASM-1827). DP-09 is carried for the idempotency and inbox library only, because the pick-up of one file must be idempotent by channel code, source reference and file hash (BR5) |

Arch v5 slide 42 lists `DocumentStored` and `DocumentFieldsExtracted` for this service and no intake-accepted event, so the absence is the catalogue's and not a gap of this story.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The path is started by the intake Schedule and not by an event, so the pickup consumes nothing. `DocumentStored` with source UPLOAD is consumed by the `ingest` activity of RWB-P5-E1049-APP and not by this story |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | Owned and registered by RWB-P5-E1049-APP; it runs `pickup`, `scanIntakeItem`, `ocr`, `ingest` and the classification, extraction and match steps in order |
| `pickup` | Activity, contributed by this story | `rwb-document` | Lists the channels, hashes, checks the duplicate window, the type, the size and the partner panel, copies to the hold container, writes `document_intake`, moves or archives after the commit and writes the run counts; idempotent by channel code, source reference and file hash |
| `scanIntakeItem` | Activity of RWB-P5-E1041-APP | `rwb-document` | Runs after `pickup` and sets `scan_result`; this story leaves the column empty for it |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None in this story | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | The Schedule is registered from the values of RWB-P5-E1057-OPS with its ID, its business-hours window, its overlap policy and its catch-up window; this story contributes the `pickup` activity the Schedule-started workflow calls and the run record the Schedule writes (ASM-1831) |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_intake` | P5 | The item row: written with the seven intake columns of the legacy migration, the `source`, the `source_ref`, the hash, the `intake_ref` and the `run_id`; `scan_result` left empty and `ocr_status` PENDING |
| `document_hub_parameter` | P5 | Read only through the parameters contract of DP-06; the rows are P5's |
| idempotency library table | PLT library, created in `rwb_document` | The `Idempotency-Key` row of the rerun operation and the channel-code, source-reference and hash key of a pickup |
| outbox, inbox library tables | PLT library, created in `rwb_document` | Created by the library migration in the same schema; this story writes no outbox row of its own |

`document_text`, `document` and `document_type` are not written by this story: the text is the OCR step's, the document row the store's and the type row the reference data administrator's. No foreign-schema table is read (DP-01) and no ACE view is read by this service.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | The five parameters, with `INTAKE_MAX_FILE_MB` 25 and `INTAKE_DUPLICATE_WINDOW_DAYS` 30 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DOC-SOURCE with SCAN, UPLOAD, GENERATED, PARTNER and EMAIL, LOV-SCAN-RESULT and LOV-OCR-STATUS |
| rwb-partner fake | the `rwb-partner` contract of S9 | Partner "LF-007" ACTIVE, a code that resolves to no partner and a partner SUSPENDED |
| scan mock | RWB-P5-E1041-CON | The CLEAN answer of AC16 and the empty-to-set `scan_result` transition |
| storage stub | RWB-PLT-TE012-APP | A hold container that refuses the write of AC10 and then accepts it |
| intake baseline fake | RWB-P5-E1057-CON | The three operations, the two shapes and the status mapping, so the tests build before the app code lands |
| channel fixture | this story | A scanner folder per branch code, a mailroom folder, an SFTP root with per-partner subfolders and a mailbox stub with the processed, rejected and archive folders |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 2 cross-service plus 1 partner read | The run list, the run read and the rerun; the parameters read and the lists read; the partner-by-code read |
| Kafka | Published 0, consumed 0 | No event of this path; `DocumentStored` and `DocumentFieldsExtracted` are the store's and extraction's (12.3) |
| Temporal | 1 workflow observed, 1 activity contributed, 1 Schedule observed | `DocumentIntakeWorkflow` with `pickup` on queue `rwb-document`; the 15-minute Schedule is registered by RWB-P5-E1057-OPS |
| File | 4 channels read, 1 container written, 3 folder moves | Branch scanner folders, the mailroom folder, the SFTP inbound root with its partner subfolders and the recovery mailboxes; the hold container `rwb-quarantine`; the processed, rejected and archive folders |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `intake/pickup`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PickupActivity | Temporal activity | `pickup`: run every channel reader, count the results, write the run record; idempotent by channel code, source reference and file hash |
| IntakeChannelReader | Service (interface) | `listNew()`, `open(ref)`, `markProcessed(ref)`, `markRejected(ref)`, `markDuplicate(ref)` |
| FolderChannelReader | Service | Branch scanner folders and the mailroom folder, one code per branch and MAILROOM |
| SftpChannelReader | Service | Partner SFTP subfolders; applies BR4 through the `rwb-partner` contract |
| MailboxChannelReader | Service | Recovery mailboxes; splits attachments, skips images under `INTAKE_MIN_IMAGE_KB`, archives the email |
| IntakeService | Service | Hash, duplicate check, type and size check, copy to the hold container, write `document_intake` (BR2, BR4 to BR6) |
| IntakeAlertService | Service | Counts consecutive failed runs per channel and raises MSG-P5-008 at the parameter threshold |
| IntakeRunService | Service | Builds and serves the run record from `document_intake` and the activity counters; serves the rerun |
| AdminJobController | Controller | The three operations of 12.1, with the access check and the RFC 9457 error mapping |
| DocumentIntakeRepository | Repository | Reads and writes `document_intake` only; `uk_intake_channel_ref` is the second duplicate gate |

**Database.**

- One migration in the per-service Flyway sequence (DP-15): `V1057_1__intake_channels.sql` adds to `document_intake` `channel_code varchar(40)`, `file_name varchar(255)`, `file_size bigint`, `captured_at timestamptz`, `sender_address varchar(320)`, `partner_id uuid` and `run_id uuid`, and widens `source_ref` to `varchar(400)` for email message IDs and long paths; the legacy name of the same step is `V1_5_057__intake_channels.sql`.
- Constraint `uk_intake_channel_ref UNIQUE (channel_code, source_ref, file_sha256)`; index `ix_intake_hash ON document_intake (channel_code, file_sha256, received_at)`; index `ix_intake_run ON document_intake (run_id)` for the run record.
- The `document_intake` base table is the one RWB-P5-E1049-APP creates in the same sequence; this migration only widens it.
- The partner is read only through the `rwb-partner` contract.

**Configuration and reference data.**

- Properties per environment, set by RW-PLATADM: `rwb.document.intake.branch-folders` (branch code to path), `rwb.document.intake.mailroom-folder`, `rwb.document.intake.sftp-root`, `rwb.document.intake.mailboxes` (code to address), the processed, rejected and archive folder names, and `rwb.document.container.hold` pointing at `rwb-quarantine` from RWB-P5-E1057-INF (ASM-1828).
- `document_hub_parameter` rows INTAKE_ALLOWED_TYPES, INTAKE_MAX_FILE_MB, INTAKE_DUPLICATE_WINDOW_DAYS, INTAKE_MIN_IMAGE_KB and INTAKE_ALERT_AFTER_FAILURES, loaded by the reference data administrator (values assumed under DL11 and ASM-1833) and read through DP-06.
- Holiday table read through the reference-data contract of DP-07; partner panel rows kept by the partner and agency manager in `rwb-partner`.
- Feature flags `rwb.document.intake` and its four sub-flags `rwb.document.intake.branch`, `.mailroom`, `.sftp` and `.email` (ASM-1835). Off: `pickup` does not read that channel.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/document/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the intake table the legacy story wrote into `rwb_document` and stops the module reaching into the recovery schema: `document_intake` and `document_hub_parameter` are this service's, and no partner or case row is copied. DP-06 and DP-07 keep the five parameters and the three lists out of the code through the two client libraries, while the parameter rows themselves stay in `rwb_document` as the Ownership Map gives them to P5. DP-09 is applied by the idempotency rule alone: the library's idempotency and inbox tables carry the channel-code, source-reference and hash key, so a repeat inside a run and a redelivery after a failed move create nothing, and no event name is invented (ASM-1827). DP-10 is the substantive change: the Quartz cron of JOB-12 and its one-instance lock become a Temporal Schedule with an overlap policy of skip, and the legacy `IntakeStep` becomes the `pickup` activity of the kit's "Document intake" template. DP-11 replaces the in-process `PartnerDirectory` with one published read of `rwb-partner`, one hop and a 2 s timeout, faked in the build. DP-13 rebases the only legacy path of the story, the admin rerun, on the service base. DP-15 puts the intake widening in the service's own sequence instead of the legacy `V0001` baseline. DP-19 puts the run record and the rerun behind the gateway-bff composite route, so SCR-44 calls the owner once.

**Build steps**

1. Write the migration with the constraint and the two indexes; repository tests for the duplicate gate and the run index.
2. Build `IntakeService` with unit tests for the hash, the duplicate window, the type by content, the 25.0 and 25.1 MB boundary and the order "commit then move".
3. Build `FolderChannelReader` against a test folder for branch and mailroom files; test AC1 and AC4.
4. Build `SftpChannelReader` against the `rwb-partner` fake for ACTIVE, SUSPENDED and a code that resolves to no partner; the criteria it proves are RWB-S9-E1057-APP's and the reader is built here.
5. Build `MailboxChannelReader` against a mailbox stub: attachments, images under `INTAKE_MIN_IMAGE_KB`, the archive move, the sender masked.
6. Build `PickupActivity`, register it with the kit on queue `rwb-document` and test the counts, the empty run and the repeat run.
7. Build `IntakeAlertService`, the run record and `AdminJobController`; test AC11, AC12 and the access refusal of TC-E1-057-17.
8. Test the storage refusal of AC10 and the scan-before-OCR order of AC16 against the storage stub and the scan mock.
9. Add the `pickup` entry to the run book of RWB-P5-E1057-OPS and confirm that no sender address appears in any log.

**Done when.** The tests in section 16 pass, the run record shows the counts per channel and result for a replayed business-hour window, a file never leaves a channel before its row commits, and no sender address appears in any log.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | A file type is not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-017 | A file is above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-007 | A file is refused at intake (new) | {source} file {file} was not taken in: {reason}. It is in the {folder} folder. |
| MSG-P5-008 | Two intake runs in a row fail on one channel (new) | Document intake failed twice in a row for {channel}. Check the interface and job monitor. |
| MSG-GEN-006 | The intake container is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The HTTP mapping is the legacy one and is fixed by the baseline RWB-P5-E1057-CON: 202 for the accepted rerun, 403 for MSG-P4-002, 404 for an unknown run with the not-found message whose text is Not specified in the source documents (GAP-1012; ASM-1829), 409 for MSG-GEN-004 and 503 for MSG-GEN-006 naming the system that failed. MSG-P5-001, MSG-P5-017 and MSG-P5-007 are the refusal texts carried into the run record and never returned as an error body; MSG-P5-008 is the alert text of `IntakeAlertService`.

### 15. Screens and states

No screen in this story. The platform administrator sees each intake run on SCR-44 Interface and job monitor in the states running, failed and complete, with the counts per channel, and reruns a failed run there. The case owner sees intake documents on SCR-30 Case documents once RWB-P5-E1032-APP attaches them. In the target the run record is served by the two GET operations of 12.1 through the gateway-bff composite route (DP-19); SCR-44 itself and its full interface and job monitor belong to Epic 2, and this story publishes the record it reads (ASM-1834).

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-44 Interface and job monitor | running | One intake run for the current 15-minute window with the channels read so far |
| SCR-44 Interface and job monitor | complete | The counts per channel and per result, taken in, refused by reason and duplicate |
| SCR-44 Interface and job monitor | failed | The channel that failed, MSG-GEN-006 or MSG-P5-008 and the rerun action behind Platform administration right U |
| SCR-30 Case documents | list | A document attached from intake once RWB-P5-E1032-APP has matched it |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-057-17 | X12, BR7 (legacy Access) | Component | RW-CASEOWN (Platform administration -) calls the rerun; refused with 403 and MSG-P4-002 |
| TC-E1-057-01 | AC1, BR1 | End to end | Synthetic PDF in branch folder "BR-0123" |
| TC-E1-057-02 | AC2, BR1, BR4 (proved by RWB-S9-E1057-APP) | End to end | Synthetic PDF in SFTP subfolder "LF-007" |
| TC-E1-057-03 | AC3, BR1, BR9 (proved by RWB-S9-E1057-APP) | End to end | Mailbox stub with one PDF attachment, synthetic sender |
| TC-E1-057-04 | AC4, BR1 | End to end | Synthetic PDF in the mailroom folder |
| TC-E1-057-05 | AC5, BR2 | End to end | DOCX file in the folder of "BR-0123" |
| TC-E1-057-06 | AC6, BR2 | End to end | Files of 25.1 MB and 25.0 MB |
| TC-E1-057-07 | AC7, BR4 (proved by RWB-S9-E1057-APP) | End to end | Subfolders "LF-099" and "LF-008" |
| TC-E1-057-08 | AC8, BR5 | End to end | The same file from "BR-0123" two days apart |
| TC-E1-057-09 | AC9 (proved by RWB-S9-E1057-APP) | End to end | All channels empty |
| TC-E1-057-10 | AC10 | End to end | Hold container stub refusing writes, then accepting |
| TC-E1-057-11 | AC11, BR7 | End to end | SFTP inbound folder unreadable for two runs |
| TC-E1-057-12 | AC12, BR7 | End to end | Two service instances, one cluster, one run slot |
| TC-E1-057-13 | AC13 (proved by RWB-S9-E1057-APP) | End to end | Email with no attachment; email with a 6 KB image |
| TC-E1-057-14 | AC14, BR6 | End to end | The move to the processed folder forced to fail |
| TC-E1-057-15 | AC15, BR7 | End to end | Clock set to 18:15 on a working day |
| TC-E1-057-16 | AC16, BR3 | End to end | An item taken in, the scan mock delayed, the OCR step tried first |

The legacy level System maps to End to end and Access to Component. The five cases whose criteria are owned by the partner slice carry the note in the table: they are answered at contract level by RWB-P5-E1057-CON and proved as business values by RWB-S9-E1057-APP, so the same legacy value is not proved twice. The wave 1 integration harness copies TC-E1-057-01 as RWB-ITG-E1057-ITG, where the real `rwb-partner` and the real storage replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: folders, mailboxes, types, size limit and windows are properties and parameters read through DP-06 and DP-07.
- No personal data in logs, tests or prompts: sender addresses and email file names are not logged; test emails use synthetic senders, and the run record carries counts and reason codes only.
- No read of another module's tables: partners come through the `rwb-partner` contract, one hop with a 2 s timeout and no `partner` row copied (DP-01, DP-11).
- A file is never removed from a channel before its `document_intake` row is committed, and a failed move is repaired by the next run and never by a manual delete.
- Storage is reached by managed identity only, never by key or shared access signature (RWB-PLT-TE012-APP).
- An item is never scanned twice and never OCR-read before its scan: `pickup` leaves `scan_result` empty and no other writer sets it.
- The duplicate rule is enforced by the selection window, the idempotency row and the unique constraint together; no path deletes a duplicate row to let a file in.
- The feature flags `rwb.document.intake` and its four sub-flags remove a channel without a rollback of the schema (ASM-1835).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, mailroom, partner file transfer and email through the same intake | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-13, FEAT-DCM-14, FEAT-DCM-15 | 13 Manage documents and correspondence; 12 Manage partners | R-UNI-33, R-UNI-40 | TC-E1-057-01 to TC-E1-057-15, TC-E1-057-17 |
| REQ-DCM-010 | Retention class on every document; virus scan before storing | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-13 | 13 Manage documents and correspondence | None | TC-E1-057-16 |

| Legacy reference | Where it is kept |
|---|---|
| `V1_5_057__intake_channels.sql`, the seven intake columns and `uk_intake_channel_ref` | Sections 4, 13 |
| MSG-P5-001, MSG-P5-017, MSG-P5-007, MSG-P5-008, MSG-GEN-006, MSG-P4-002 | Section 14 and the exception paths |
| The twelve exception paths X1 to X12 | Section 5 |
| Business rules BR1 to BR9, and rules R-UNI-40, CTL-11, DL11, DL26 | Sections 2, 8, 17 |
| The hold container `rwb-quarantine` and the processed, rejected and archive folders | Sections 1, 4, 11, 13 |
| The legacy paths `/admin/jobs/{jobId}/rerun` and its 403, 404, 409 and 503 answers | Sections 5, 12.1, 14 |
| Legacy key RWB-E1-057, AC1, AC4 to AC6, AC8, AC10 to AC12, AC14 to AC16, TC-E1-057-01 to TC-E1-057-17 | Metadata, section 7, section 16 |
| AC2, AC3, AC7, AC9 and AC13, carried by RWB-S9-E1057-APP | Sections 1, 5, 7, 16, 19 |

### 19. Out of scope

- The malware scan and quarantine (RWB-E1-041, now RWB-P5-E1041-APP), OCR (RWB-E1-049, now RWB-P5-E1049-APP), classification (RWB-E1-050, now RWB-P5-E1050-APP), extraction (RWB-E1-053, now RWB-P5-E1053-APP) and matching to a case (RWB-E1-032, now RWB-P5-E1032-APP).
- Uploads from the case documents screen (RWB-E1-026, now RWB-P5-E1026-APP).
- Field app photos and bills (RWB-E2-024, now a wave 2 story of P5, RWB-P5-E2024-APP).
- Partner uploads through the partner portal (Epic 4, PRT-03; partner access DL03).
- The partner panel and the mailbox channel criteria AC2, AC3, AC7, AC9 and AC13, which are owned and proved by RWB-S9-E1057-APP in `rwb-partner`.
- The contract documents, the shapes, the enumerations, the event position and the fakes (RWB-P5-E1057-CON).
- The SFTP and mailbox channels, the hold container, the topic and ACLs, the identity and secrets, the partner gateway route and the DMZ position, and the scan capacity (RWB-P5-E1057-INF).
- The chart, the intake Schedule registration, the flag values, the dashboards, the alerts and the runbook (RWB-P5-E1057-OPS).
- SCR-44 Interface and job monitor as a screen (Epic 2); this story publishes the run record it reads.
- The real cross-service journey of the path (RWB-ITG-E1057-ITG).

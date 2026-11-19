<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md`  
> **Converted from:** Markdown (copied)

# RWB-E1-057 Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-057 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-13 Take intake from branches and the mailroom; FEAT-DCM-14 Take intake from partner SFTP; FEAT-DCM-15 Take intake from email |
| Requirement IDs | REQ-DCM-009, REQ-DCM-010 |
| BRD section | Business Requirements Epic 1, section 3.5 |
| L3 process | 13 Manage documents and correspondence; 12 Manage partners |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-049, RWB-TE-012, RWB-E1-041 |
| Status | Ready for build |

## 1. Story

As a **case owner**, I want **scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded**, so that **every document path ends in the document hub**.

## 2. Business rationale

Documents reach recovery today by courier, shared folders and personal email, and an original that goes to the wrong desk is rebuilt for each audit. This story reads the four inbound paths every 15 minutes into the document intake, records where each file came from, refuses files that are not allowed or come from an unknown partner, and leaves every accepted file for the malware scan and OCR steps, so a document received in the morning is on the case the same day. It meets REQ-DCM-009 and puts every inbound file through the virus scan of REQ-DCM-010, and removes email hand-offs of customer documents (CTL-11).

## 3. Preconditions

- RWB-E1-049 is done: JOB-12 Document intake runs as the Spring Batch job DocumentIntakeJob with ordered steps, and the table document_intake exists.
- RWB-E1-041 is done: scanStep runs before ocrStep and quarantines infected files.
- RWB-TE-012 is done: the intake and quarantine containers exist and SY-OCR writes to the intake container by managed identity.
- The channels are set per environment by the platform administrator in properties: branch scanner folders by branch code, the mailroom folder, the partner SFTP inbound folder with one subfolder per partner_code, and the recovery mailboxes. The mailboxes are read by the SY-OCR managed identity; the mail service is assumed to be Exchange Online read through Microsoft Graph (no open decision covers it).
- Partner panel rows are loaded (reference table "Partner panel", owner partner and agency manager) and readable through PartnerDirectory.
- Rows in document_hub_parameter: INTAKE_ALLOWED_TYPES PDF, JPG, PNG; INTAKE_MAX_FILE_MB 25; INTAKE_DUPLICATE_WINDOW_DAYS 30; INTAKE_MIN_IMAGE_KB 10; INTAKE_ALERT_AFTER_FAILURES 2. All assumed (DL11).
- Feature flag rwb.dochub.intake is on.

## 4. Flow

1. Scheduler: JOB-12 Document intake fires every 15 minutes in business hours on one service instance; intakeStep runs first, before scanStep.
2. IntakeStep: lists new files in each branch scanner folder and the mailroom folder, in each partner subfolder of the SFTP inbound folder, and new messages in each recovery mailbox.
3. IntakeStep: for each file or email attachment computes the SHA-256 hash and checks document_intake for the same channel and hash inside the duplicate window.
4. IntakeStep: checks the file type by content and extension, and the size, against the parameters.
5. IntakeStep: for a partner file, reads the partner by the subfolder's partner_code and checks that its panel_status is ACTIVE.
6. IntakeStep: copies an accepted file to the intake container and writes one document_intake row with source, channel code, source reference, file name, size, hash, received time, scanner time (scanner files), partner ID (partner files) or sender address (email), and the run ID; scan_result is left empty for scanStep.
7. IntakeStep: after the commit, moves the scanner or SFTP file to the processed folder, or moves the email to the archive folder; a refused file goes to the rejected folder.
8. IntakeStep: writes the counts per channel and result (taken in, refused by reason, duplicate) to the job record shown on SCR-44 Interface and job monitor.
9. ScanStep, ocrStep, classifyStep, extractStep and matchStep (RWB-E1-041, RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-032) then run on the new rows in the same job.
10. Platform administrator: sees the run on SCR-44 and reruns a failed run when needed.

## 5. Exception paths

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

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Adds the first step to the JOB-12 job of RWB-E1-049; scan and OCR steps exist |
| Negotiable | Channels, folders, types, sizes and windows are properties and parameters |
| Valuable | Every inbound path ends in the document hub with its source recorded |
| Estimable | One job step, three channel readers, seven columns, no new screen |
| Small | Fits in two weeks with its tests |
| Testable | Each scenario below is one test with synthetic files |

## 7. Acceptance criteria

```gherkin
Feature: Intake from branches, mailroom, partner SFTP and email

  Background:
    Given JOB-12 Document intake runs every 15 minutes from 08:00 to 18:00 Asia/Bangkok on working days
    Given INTAKE_ALLOWED_TYPES is PDF, JPG and PNG and INTAKE_MAX_FILE_MB is 25
    Given partner "LF-007" is a law firm with panel_status "ACTIVE"

  Scenario: AC1 Branch scan
    Given file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12
    When the intake job runs at 09:15
    Then one document_intake row has source "SCAN", channel_code "BR-0123", captured_at 2026-11-30 09:12 and an empty scan_result
    Then the file is in the intake container at the row's intake_ref
    Then the file is no longer in the scanner folder and is in its processed folder

  Scenario: AC2 Partner SFTP
    Given file "LF-007-notice-0001.pdf" in the SFTP inbound subfolder "LF-007"
    When the job runs
    Then one document_intake row has source "PARTNER", channel_code "LF-007" and partner_id of partner "LF-007"

  Scenario: AC3 Mailbox
    Given an email to recovery mailbox "MBX-RECOVERY-01" with one PDF attachment "reply-0001.pdf"
    When the job runs
    Then one document_intake row has source "EMAIL", channel_code "MBX-RECOVERY-01" and the sender address recorded
    Then the system masks the sender address in every response and absent from the job record and the logs
    Then the email is in the archive folder of "MBX-RECOVERY-01"

  Scenario: AC4 Mailroom scan
    Given file "mailroom-0001.pdf" in the mailroom folder
    When the job runs
    Then one document_intake row has source "SCAN" and channel_code "MAILROOM"

  Scenario: AC5 A file type not allowed is refused
    Given file "letter-0002.docx" in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system writes no document_intake row for it
    Then the file is in the rejected folder of branch "BR-0123"
    Then the job record shows 1 refused on "BR-0123" with MSG-P5-007 and reason MSG-P5-001

  Scenario: AC6 A file above the size limit is refused
    Given file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system refuses "scan-0003.pdf" with reason MSG-P5-017 and moved to the rejected folder
    Then "scan-0004.pdf" has a document_intake row

  Scenario: AC7 An unknown or suspended partner is refused
    Given file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code
    Given file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED"
    When the job runs
    Then the system writes no document_intake row for either file
    Then the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE"

  Scenario: AC8 A duplicate file is not taken in twice
    Given file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November
    When the same file arrives again from branch "BR-0123" on 2 December
    Then the system writes no second document_intake row
    Then the system moves the file to the processed folder and counted as a duplicate

  Scenario: AC9 An empty run
    Given no new file or email on any channel
    When the job runs
    Then the job record shows intakeStep complete with 0 items on each channel

  Scenario: AC10 The intake container does not accept writes
    Given the intake container refuses writes
    When the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123"
    Then the system writes no document_intake row
    Then "scan-0007.pdf" stays in the scanner folder
    Then on the next run with the container available the file is taken in

  Scenario: AC11 Two failed runs raise an alert
    Given the run at 10:00 failed because the SFTP inbound folder could not be read
    When the run at 10:15 fails for the same reason
    Then the platform administrator receives MSG-P5-008 naming "PARTNER_SFTP"
    Then the run at 10:30 tries again

  Scenario: AC12 The job runs once across two instances
    Given two service instances are running
    When the 09:15 run is due
    Then the system records one run for 09:15
    Then each file has one document_intake row

  Scenario: AC13 An email with no usable attachment
    Given an email to "MBX-RECOVERY-01" with no attachment
    Given an email with only a 6 KB signature image
    When the job runs
    Then the system writes no document_intake row for either email
    Then both emails are in the archive folder

  Scenario: AC14 A file seen again after a failed move
    Given file "scan-0008.pdf" was taken in at 11:00 and the move to the processed folder failed
    When the run at 11:15 sees "scan-0008.pdf" again
    Then the system writes no second document_intake row
    Then the system moves the file to the processed folder

  Scenario: AC15 Outside business hours
    Given the time is 18:15 on a working day
    When the scheduler checks JOB-12
    Then no run starts until 08:00 the next working day

  Scenario: AC16 An item taken in is scanned before OCR
    Given file "scan-0009.pdf" was taken in by intakeStep with an empty scan_result
    When ocrStep runs in the same job before scanStep has set scan_result
    Then ocrStep does not read "scan-0009.pdf"
    Then after scanStep sets scan_result "CLEAN" ocrStep reads it
```

## 8. Business rules

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

## 9. State transitions

None. This story does not change a case status. It creates document_intake rows with an empty scan_result and ocr_status PENDING; RWB-E1-041 and RWB-E1-049 move them on.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs intakeStep; reads the channels; writes document_intake and the intake container (Documents CRU) |
| RW-PLATADM, platform administrator | Sees runs on SCR-44 and reruns JOB-12 (Platform administration CRUD); sets the channel properties |
| RW-AGENCYMG, partner and agency manager | Keeps the partner codes and panel status that BR4 reads (Partner portal CRUDA) |
| RW-CASEOWN, case owner | Reads documents from intake once attached (Documents R) |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 | partner | id | Read, through PartnerDirectory |
| DF-PRT-002 | partner | partner_code | Read, through PartnerDirectory |
| DF-PRT-004 | partner | partner_type | Read, through PartnerDirectory |
| DF-PRT-005 | partner | panel_status | Read, through PartnerDirectory |
| DF-DOC-046 | document_intake | source | Write |
| DF-DOC-047 | document_intake | source_ref | Write |
| DF-DOC-055 | document_intake | received_at | Write |
| DF-DOC-056 | document_intake | file_sha256 | Write |
| DF-DOC-057 | document_intake | intake_ref | Write |
| DF-DOC-048 | document_intake | channel_code | Write |
| DF-DOC-049 | document_intake | file_name | Write |
| DF-DOC-050 | document_intake | file_size | Write |
| DF-DOC-051 | document_intake | captured_at | Write |
| DF-DOC-052 | document_intake | sender_address | Write |
| DF-DOC-053 | document_intake | partner_id | Write |
| DF-DOC-054 | document_intake | run_id | Write |
| DF-REF-246 | document_hub_parameter | param_value | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job step**

| Item | Value |
|---|---|
| Job name | JOB-12 Document intake; this story adds intakeStep as the first step |
| Trigger | Quartz cron `0 0/15 8-17 ? * MON-FRI` in Asia/Bangkok; bank holidays from the reference data holiday table are skipped |
| Schedule | Every 15 minutes in business hours |
| Input | Branch scanner folders, the mailroom folder, the partner SFTP inbound folder, the recovery mailboxes |
| Output | document_intake rows; files in the intake container; files moved to processed or rejected; emails archived; counts on the job record |
| Events published | None. DocumentStored (EV-16) is written when matchStep stores the document (RWB-E1-032) |
| Idempotency key | Channel code, source reference and file hash |
| Restart | A failed run leaves its files at the channel; the next run or a rerun takes them. A file already committed is a duplicate on the next run (AC14) |

**Endpoint used: POST /api/recovery/v1/admin/jobs/{jobId}/rerun**

| Item | Value |
|---|---|
| Request | Path jobId (uuid) of a failed JOB-12 run |
| Response | Job |
| Errors | 401; 403 no Platform administration U (MSG-P4-002); 404 job not found; 409 run still in progress (MSG-GEN-004); 503 (MSG-GEN-006) |
| Authorization | Platform administration, right U |
| Idempotency | A rerun of a run in progress is refused with 409 |

**Published interface called (S9 partner management)**

```java
package recovery.partner;
public interface PartnerDirectory {
    Optional<PartnerSummary> findByCode(String partnerCode); // id, partnerCode, partnerType, panelStatus
}
```

## 13. Solution plan

**Package.** folder `recovery/dochub/intake`, Java package `recovery.dochub.intake`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntakeStep | Job | First step of DocumentIntakeJob (RWB-E1-049); runs each channel reader; writes the counts |
| IntakeChannelReader | Service (interface) | listNew(), open(ref), markProcessed(ref), markRejected(ref) |
| FolderChannelReader | Service | Branch scanner and mailroom folders |
| SftpChannelReader | Service | Partner SFTP subfolders; applies BR4 through PartnerDirectory |
| MailboxChannelReader | Service | Recovery mailboxes; splits attachments; skips small images; archives the email |
| IntakeService | Service | Hash, duplicate check, type and size check, copy to the intake container, write document_intake (BR2, BR4 to BR6) |
| IntakeAlertService | Service | Counts failed runs per channel and sends MSG-P5-008 |
| DocumentIntakeRepository | Repository | From RWB-E1-049; adds the intake columns |

**Database**

- Flyway migration `V1_5_057__intake_channels.sql` adds to document_intake: channel_code varchar(40), file_name varchar(255), file_size bigint, captured_at timestamptz, sender_address varchar(320), partner_id uuid, run_id uuid; and widens source_ref to varchar(400) for email message IDs and long paths.
- Constraint `uk_intake_channel_ref UNIQUE (channel_code, source_ref, file_sha256)`; index `ix_intake_hash ON document_intake (channel_code, file_sha256, received_at)`.
- Reads partner only through PartnerDirectory.

**Configuration and reference data**

- Properties per environment, set by RW-PLATADM: rwb.dochub.intake.branch-folders (branch code to path), rwb.dochub.intake.mailroom-folder, rwb.dochub.intake.sftp-root, rwb.dochub.intake.mailboxes (code to address), and the processed, rejected and archive folder names; rwb.dochub.container.intake from RWB-TE-012.
- document_hub_parameter rows INTAKE_ALLOWED_TYPES, INTAKE_MAX_FILE_MB, INTAKE_DUPLICATE_WINDOW_DAYS, INTAKE_MIN_IMAGE_KB, INTAKE_ALERT_AFTER_FAILURES, loaded by the reference data administrator (values assumed; DL11).
- Holiday table from the reference data service (RWB-E1-043). Partner panel rows loaded by the partner and agency manager.

**Build steps**

1. Write the migration with the constraint and index; repository tests.
2. Build IntakeService with unit tests for the hash, the duplicate window, type by content, the 25.0 and 25.1 MB boundary and the order "commit then move".
3. Build FolderChannelReader against a test folder for branch and mailroom files.
4. Build SftpChannelReader with a stub PartnerDirectory for ACTIVE, SUSPENDED and unknown codes.
5. Build MailboxChannelReader against a mailbox stub: attachments, images under 10 KB, archive move, sender masked.
6. Add IntakeStep as the first step of DocumentIntakeJob with the cron, holiday skip and counts; test one run with two instances.
7. Build IntakeAlertService and add the intakeStep section to the JOB-12 run book (RWB-E1-056).

**Feature flag:** `rwb.dochub.intake`, with one sub-flag per channel (`rwb.dochub.intake.branch`, `.mailroom`, `.sftp`, `.email`). Off: intakeStep does not read that channel.

**Done when:** the tests in section 16 pass, the JOB-12 run book covers intakeStep, and no sender address appears in any log.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-001 | A file type is not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P5-017 | A file is above the size limit | This file is larger than {size} MB and cannot be stored. |
| MSG-P5-007 | A file is refused at intake (new) | {source} file {file} was not taken in: {reason}. It is in the {folder} folder. |
| MSG-P5-008 | Two intake runs in a row fail on one channel (new) | Document intake failed twice in a row for {channel}. Check the interface and job monitor. |
| MSG-GEN-006 | The intake container is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The platform administrator sees each JOB-12 run on SCR-44 Interface and job monitor in the states running, failed and complete, with the intakeStep counts per channel, and reruns a failed run there. The case owner sees intake documents on SCR-30 Case documents once RWB-E1-032 attaches them.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-057-01 | AC1, BR1 | System | Synthetic PDF in branch folder BR-0123 |
| TC-E1-057-02 | AC2, BR1, BR4 | System | Synthetic PDF in SFTP subfolder LF-007 |
| TC-E1-057-03 | AC3, BR1, BR9 | System | Mailbox stub with one PDF attachment, synthetic sender |
| TC-E1-057-04 | AC4, BR1 | System | Synthetic PDF in the mailroom folder |
| TC-E1-057-05 | AC5, BR2 | System | DOCX file |
| TC-E1-057-06 | AC6, BR2 | System | Files of 25.1 MB and 25.0 MB |
| TC-E1-057-07 | AC7, BR4 | System | Subfolders LF-099 and LF-008 |
| TC-E1-057-08 | AC8, BR5 | System | Same file two days apart |
| TC-E1-057-09 | AC9 | System | All channels empty |
| TC-E1-057-10 | AC10 | System | Intake container stub refusing writes, then accepting |
| TC-E1-057-11 | AC11, BR7 | System | SFTP folder unreadable for two runs |
| TC-E1-057-12 | AC12, BR7 | System | Two service instances, one cluster |
| TC-E1-057-13 | AC13 | System | Email with no attachment; email with a 6 KB image |
| TC-E1-057-14 | AC14, BR6 | System | Move to processed forced to fail |
| TC-E1-057-15 | AC15, BR7 | System | Clock set to 18:15 on a working day |
| TC-E1-057-16 | AC16, BR3 | System | Item taken in, scanStep stub delayed |
| TC-E1-057-17 | Access | Access | RW-CASEOWN user (Platform administration -) calls POST /admin/jobs/{jobId}/rerun; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: folders, mailboxes, types, size limit and windows are properties and parameters.
- No personal data in logs, tests or prompts: sender addresses and email file names are not logged; test emails use synthetic senders.
- No read of another module's tables: partners come through PartnerDirectory.
- A file is never removed from a channel before its document_intake row is committed.
- Storage is reached by managed identity only, never by key or shared access signature (RWB-TE-012).

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, mailroom, partner file transfer and email through the same intake | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-13, FEAT-DCM-14, FEAT-DCM-15 | 13 Manage documents and correspondence; 12 Manage partners | R-UNI-33, R-UNI-40 | TC-E1-057-01 to TC-E1-057-15, TC-E1-057-17 |
| REQ-DCM-010 | Retention class on every document; virus scan before storing | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-13 | 13 Manage documents and correspondence | None | TC-E1-057-16 |

## 19. Out of scope

- The malware scan and quarantine (RWB-E1-041), OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching to a case (RWB-E1-032).
- Uploads from the case documents screen (RWB-E1-026).
- Field app photos and bills (RWB-E2-024).
- Partner uploads through the partner portal (Epic 4, PRT-03; partner access DL03).

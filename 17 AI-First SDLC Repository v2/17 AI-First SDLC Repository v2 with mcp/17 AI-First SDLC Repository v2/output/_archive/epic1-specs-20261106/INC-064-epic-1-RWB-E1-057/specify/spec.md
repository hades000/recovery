# Technical Specification — RWB-E1-057 Intake from branches, mailroom, partner SFTP and email

| Field | Value |
|---|---|
| Story | RWB-E1-057 — Intake from branches, mailroom, partner SFTP and email |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-064-epic-1-RWB-E1-057` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DCM-009, REQ-DCM-010); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md`; FSD P5 A2.13–A2.15; TSD P5 T3.1 |
| Upstream IDs | REQ-DCM-009, REQ-DCM-010; FEAT-DCM-13, FEAT-DCM-14, FEAT-DCM-15; US-RWB-E1-057; DL11, DL26; CTL-11; R-UNI-33, R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen is added or changed. SCR-44 Interface and job monitor already shows JOB-12 runs and the rerun action. |
| Logic In Scope | `YES` — channel discovery, hashing, duplicate window, type and size checks, partner validation, commit-then-move, counts and alerts. |
| API In Scope | `NO` — no new or changed contract. Reuses `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-12 Document intake (new `intakeStep` as first step); `DocumentIntakeRepository` (intake channel columns); SCR-44 job monitor. |
| New Nodes Required | `YES` — `IntakeStep`, `IntakeChannelReader`, `FolderChannelReader`, `SftpChannelReader`, `MailboxChannelReader`, `IntakeService`, `IntakeAlertService`. |
| Inherited Existing Behavior | JOB-12 and `document_intake` (RWB-E1-049); malware scan before OCR (RWB-E1-041); intake and quarantine containers (RWB-TE-012); partner panel through `PartnerDirectory`; holiday table (RWB-E1-043); parameters (RWB-E1-042); run book and monitor (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Scanner and mailroom files have source SCAN; partner SFTP files PARTNER; mailbox attachments EMAIL. | SPEC-RWB-E1-057-003 | DIRECT | `LOV-DOC-SOURCE`; channel code identifies the branch, MAILROOM, partner code or mailbox. | COVERED |
| BR2 | Only the allowed types up to the size limit are taken in; the type is checked by content and extension. | SPEC-RWB-E1-057-005 | DIRECT | `INTAKE_ALLOWED_TYPES` PDF, JPG, PNG; `INTAKE_MAX_FILE_MB`; 25.0 MB accepted, 25.1 MB refused. | COVERED |
| BR3 | Every file taken in is scanned for malware by `scanStep` before `ocrStep` reads it. | SPEC-RWB-E1-057-014 | DIRECT | `scan_result` is left empty; `ocrStep` requires CLEAN. | COVERED |
| BR4 | A partner file is taken in only from the subfolder of a partner whose `panel_status` is ACTIVE. | SPEC-RWB-E1-057-006 | DIRECT | `PartnerDirectory.findByCode`; unknown and suspended partners are refused. | COVERED |
| BR5 | A file with the same hash from the same channel inside the window is a duplicate. | SPEC-RWB-E1-057-004 | DIRECT | `INTAKE_DUPLICATE_WINDOW_DAYS`; unique channel, source reference and hash. | COVERED |
| BR6 | A source file is moved or an email archived only after the `document_intake` commit. | SPEC-RWB-E1-057-007, SPEC-RWB-E1-057-008 | DIRECT | Commit then move; a failed move leaves the file to be seen as a duplicate next run. | COVERED |
| BR7 | JOB-12 runs every 15 minutes in business hours, once across instances; two failed runs in a row on a channel raise an alert. | SPEC-RWB-E1-057-001, SPEC-RWB-E1-057-010 | DIRECT | Quartz cron, clustered execution, `INTAKE_ALERT_AFTER_FAILURES`. | COVERED |
| BR8 | Folders and mailboxes are properties; types, sizes and windows are parameters; none is code. | SPEC-RWB-E1-057-002 | DIRECT | Environment properties and `document_hub_parameter`. | COVERED |
| BR9 | The sender address is personal data: masked by role and never logged. | SPEC-RWB-E1-057-009 | DIRECT | Stored in `sender_address`; masked in responses; absent from the job record and logs. | COVERED |
| AC1 | A branch scan creates one SCAN row with the branch channel, captured time and empty scan result; the file is in the intake container and the processed folder. | SPEC-RWB-E1-057-002, SPEC-RWB-E1-057-003, SPEC-RWB-E1-057-007 | DIRECT | Branch reader; commit then move. | COVERED |
| AC2 | A partner file creates one PARTNER row with the partner channel and partner ID. | SPEC-RWB-E1-057-002, SPEC-RWB-E1-057-003, SPEC-RWB-E1-057-006, SPEC-RWB-E1-057-007 | DIRECT | SFTP subfolder is the partner code. | COVERED |
| AC3 | A mailbox attachment creates one EMAIL row with the mailbox channel and sender; the sender is masked and absent from logs; the email is archived. | SPEC-RWB-E1-057-009 | DIRECT | Attachment split; archive after commit. | COVERED |
| AC4 | A mailroom scan creates one SCAN row with channel MAILROOM. | SPEC-RWB-E1-057-003, SPEC-RWB-E1-057-007 | DIRECT | Mailroom folder reader. | COVERED |
| AC5 | A DOCX file is refused; no row; the file is in the rejected folder; the job record shows 1 refused with MSG-P5-007 and MSG-P5-001. | SPEC-RWB-E1-057-005, SPEC-RWB-E1-057-008 | DIRECT | Content and extension check. | COVERED |
| AC6 | A 25.1 MB file is refused and a 25.0 MB file is taken in. | SPEC-RWB-E1-057-005, SPEC-RWB-E1-057-008 | DIRECT | Boundary at the parameter value. | COVERED |
| AC7 | An unknown or suspended partner is refused with reasons PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE. | SPEC-RWB-E1-057-006, SPEC-RWB-E1-057-008 | DIRECT | No row for either file. | COVERED |
| AC8 | A duplicate file is not taken in twice; it is moved to processed and counted as a duplicate. | SPEC-RWB-E1-057-004, SPEC-RWB-E1-057-008 | DIRECT | Same channel and hash inside the window. | COVERED |
| AC9 | An empty run completes with 0 items on each channel. | SPEC-RWB-E1-057-010 | DIRECT | Zero counts per channel. | COVERED |
| AC10 | When the intake container refuses writes, no row is written, the file stays and the next run takes it in. | SPEC-RWB-E1-057-011 | DIRECT | Copy before insert; failure leaves the source file. | COVERED |
| AC11 | Two failed runs in a row raise MSG-P5-008 naming the channel and the next run retries. | SPEC-RWB-E1-057-010 | DIRECT | `IntakeAlertService` counts consecutive failures per channel. | COVERED |
| AC12 | Two service instances produce one run for 09:15 and one row per file. | SPEC-RWB-E1-057-001 | DIRECT | Clustered Quartz job with a database lock. | COVERED |
| AC13 | An email with no attachment or only a 6 KB signature image creates no row and is archived. | SPEC-RWB-E1-057-009 | DIRECT | `INTAKE_MIN_IMAGE_KB`. | COVERED |
| AC14 | A file seen again after a failed move creates no second row and is moved to processed. | SPEC-RWB-E1-057-004, SPEC-RWB-E1-057-008 | DIRECT | Duplicate check catches the committed file. | COVERED |
| AC15 | At 18:15 on a working day no run starts until 08:00 the next working day. | SPEC-RWB-E1-057-001 | DIRECT | Cron window and holiday table. | COVERED |
| AC16 | An item taken in with an empty scan result is not read by `ocrStep`; it is read after `scanStep` sets CLEAN. | SPEC-RWB-E1-057-014 | DIRECT | Scan gate before OCR. | COVERED |
| X1, X2 | A file type not allowed or a file above the size limit. | SPEC-RWB-E1-057-005, SPEC-RWB-E1-057-008 | DIRECT | No row; rejected folder; MSG-P5-001/MSG-P5-017/MSG-P5-007. | COVERED |
| X3 | An unknown or suspended partner. | SPEC-RWB-E1-057-006 | DIRECT | No row; MSG-P5-007. | COVERED |
| X4, X10 | A duplicate file, or a file seen again after a failed move. | SPEC-RWB-E1-057-004, SPEC-RWB-E1-057-008 | DIRECT | No second row; processed folder. | COVERED |
| X5, X11 | No new file, or the time is outside business hours. | SPEC-RWB-E1-057-001, SPEC-RWB-E1-057-010 | DIRECT | Zero counts; no run. | COVERED |
| X6, X7, X8 | Container write failure, two failed runs, or two instances at once. | SPEC-RWB-E1-057-001, SPEC-RWB-E1-057-010, SPEC-RWB-E1-057-011 | DIRECT | Retry; alert; one run. | COVERED |
| X9, X12 | An email with no usable attachment, or a rerun without Platform administration U. | SPEC-RWB-E1-057-009, SPEC-RWB-E1-057-012 | DIRECT | Archive; 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **case owner**, I want **scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded**, so that **every document path ends in the document hub**. The story is a backend job step with no screen: it creates `document_intake` rows with the source and channel, leaves the malware scan to RWB-E1-041, and hands every accepted file to OCR. The platform administrator sees the counts and reruns a failed run on SCR-44.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-12 Document intake`, `intakeStep` as the first step, before `scanStep`. |
| Schedule | `0 0/15 8-17 ? * MON-FRI` Asia/Bangkok; bank holidays skipped from the reference data holiday table. |
| Preconditions | RWB-E1-049, RWB-E1-041 and RWB-TE-012 done; branch, mailroom, SFTP and mailbox channels configured as properties; partner panel rows loaded and readable through `PartnerDirectory`; `INTAKE_ALLOWED_TYPES`, `INTAKE_MAX_FILE_MB`, `INTAKE_DUPLICATE_WINDOW_DAYS`, `INTAKE_MIN_IMAGE_KB`, `INTAKE_ALERT_AFTER_FAILURES` loaded; flag `rwb.dochub.intake` on. |
| Input | New files in branch scanner folders and the mailroom folder; new files in each partner SFTP subfolder; new messages in each recovery mailbox. |
| Output | `document_intake` rows with source, channel, file metadata and hash; files in the intake container; processed, rejected and archive moves; counts on the job record. |
| Feature flag | `rwb.dochub.intake`, with sub-flags `rwb.dochub.intake.branch`, `.mailroom`, `.sftp`, `.email`. Off: that channel is not read. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `source` | Channel | System writes | `SCAN`, `PARTNER` or `EMAIL` from LOV-DOC-SOURCE. |
| `document_intake` | `source_ref` | File path, message ID or attachment reference | System writes | Up to 400 characters; unique with channel and hash. |
| `document_intake` | `channel_code` | Branch code, `MAILROOM`, partner code or mailbox code | System writes | From the channel properties. |
| `document_intake` | `file_name` | Source file | System writes | Up to 255 characters. |
| `document_intake` | `file_size` | Source file | System writes | Bigint; at or below `INTAKE_MAX_FILE_MB`. |
| `document_intake` | `captured_at` | Scanner time or file time | System writes | Only for scanner files. |
| `document_intake` | `sender_address` | Email sender | System writes | Personal data; masked on read; never logged. |
| `document_intake` | `partner_id` | `PartnerDirectory` | System writes | Only for a PARTNER file. |
| `document_intake` | `run_id` | JOB-12 run | System writes | Links the row to the run. |
| `document_intake` | `received_at` | Intake time | System writes | Required. |
| `document_intake` | `file_sha256` | File content | System writes | 64 hex characters. |
| `document_intake` | `intake_ref` | Container path | System writes | File copied to the intake container. |
| `document_intake` | `scan_result` | Empty | `scanStep` writes `CLEAN` or `INFECTED` | This story never sets it. |
| `document_intake` | `ocr_status` | `PENDING` | `ocrStep` moves it on | This story creates it as PENDING. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| (none) | `intakeStep` accepts a file | Type, size, partner and duplicate checks pass | `document_intake` row with `scan_result` empty and `ocr_status PENDING` | File in the intake container; source moved after commit. |
| (none) | `intakeStep` refuses a file | Type, size or partner check fails | No row | File in the rejected folder; count and MSG-P5-007. |
| (none) | `intakeStep` sees a duplicate | Same channel and hash inside the window | No new row | File moved to processed; counted as a duplicate. |
| `scan_result` empty | `scanStep` completes | File scanned | `CLEAN` or `INFECTED` | `ocrStep` reads only CLEAN. |
| `ocr_status PENDING` | `ocrStep` completes | Scan is CLEAN | `DONE`, `RESCAN` or `FAILED` | Handled by RWB-E1-049. |

No case status changes in this story.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | File type not allowed | No row; file to rejected folder; counted as refused; audit event | MSG-P5-001, MSG-P5-007 |
| X2 | File above the size limit | No row; file to rejected folder | MSG-P5-017, MSG-P5-007 |
| X3 | Partner subfolder unknown or partner not ACTIVE | No row; file to rejected folder | MSG-P5-007 with `PARTNER_UNKNOWN` or `PARTNER_NOT_ACTIVE` |
| X4 | Same hash from the same channel inside the window | No new row; file to processed; counted as duplicate | None |
| X5 | No new file on any channel | Run logged with zero counts | None |
| X6 | Intake container does not accept writes | Files left at the channel; run failed; next run retries | MSG-GEN-006 |
| X7 | Two runs in a row fail on one channel | Alert to the platform administrator | MSG-P5-008 |
| X8 | Two service instances are due at once | One run only | None |
| X9 | Email with no attachment or only images under the minimum | Email archived; no row | None |
| X10 | Move to processed fails after commit | File seen again next run; counted as duplicate; moved then | None |
| X11 | Time outside business hours | No run | None |
| X12 | Rerun without Platform administration U | 403; nothing runs | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` to rerun a failed JOB-12 run. |
| Contract delta | None. The job step, channel readers and `document_intake` columns are internal. No event is published by intake; `DocumentStored` is published by RWB-E1-032. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration U for the rerun; SY-OCR Documents CRU for the job; 403 MSG-P4-002. |
| Error behaviour | 401; 403 MSG-P4-002; 404 job not found; 409 run in progress MSG-GEN-004; 503 MSG-GEN-006. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change. SCR-44 already shows JOB-12 runs and the rerun action. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-009, REQ-DCM-010; SPEC-RWB-E1-057-001..014 | New job step, four channel readers, intake service, alert service and repository changes. | Hash and duplicate window; type by content; 25.0/25.1 MB boundary; unknown and suspended partner; commit-then-move; container failure; email attachment rules; counts; one run across instances; scan gate; rerun 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `IntakeStep` | Job step | First step of `DocumentIntakeJob`; runs each channel reader; writes the counts. |
| `IntakeChannelReader` | Service interface | `listNew()`, `open(ref)`, `markProcessed(ref)`, `markRejected(ref)`. |
| `FolderChannelReader` | Service | Branch scanner and mailroom folders. |
| `SftpChannelReader` | Service | Partner SFTP subfolders; applies BR4 through `PartnerDirectory`. |
| `MailboxChannelReader` | Service | Recovery mailboxes; splits attachments; skips small images; archives the email. |
| `IntakeService` | Service | Hash, duplicate check, type and size check, copy to the intake container, write `document_intake`. |
| `IntakeAlertService` | Service | Counts consecutive failed runs per channel and sends MSG-P5-008. |
| `DocumentIntakeRepository` | Repository | Reads and writes `document_intake` only. |

### Package and boundaries

`recovery/dochub/intake`, Java package `recovery.dochub.intake`. Partners are read only through `PartnerDirectory`; holidays through the reference data service; storage through the managed identity of RWB-TE-012. No module reads another module's tables.

### Data and migration

- Writes: `document_intake` (`source`, `source_ref`, `channel_code`, `file_name`, `file_size`, `captured_at`, `sender_address`, `partner_id`, `run_id`, `received_at`, `file_sha256`, `intake_ref`, `scan_result` empty, `ocr_status PENDING`).
- Migration `V1_5_057__intake_channels.sql` adds the channel columns and widens `source_ref` to varchar(400).
- Constraint `uk_intake_channel_ref UNIQUE (channel_code, source_ref, file_sha256)`; index `ix_intake_hash ON document_intake (channel_code, file_sha256, received_at)`.
- No business value is hard-coded: folders, mailboxes, allowed types, size limit, duplicate window, minimum image size and alert threshold are properties or parameters.

### Intake rules

1. List new files or messages per channel; compute the SHA-256 hash for each file or attachment.
2. Check `document_intake` for the same channel and hash inside the duplicate window; a duplicate is moved to processed and counted.
3. Check the type by content and extension against `INTAKE_ALLOWED_TYPES`; check the size against `INTAKE_MAX_FILE_MB`.
4. For a partner file, read the partner by the subfolder code and require `panel_status ACTIVE`.
5. Copy the accepted file to the intake container, then write one `document_intake` row in one transaction; leave `scan_result` empty.
6. After the commit, move the scanner or SFTP file to processed, move a refused file to rejected, or archive the email.
7. Write counts per channel and result to the job record.

### Transaction, events and idempotency

- One transaction per accepted file; the source file is never removed before the row commits.
- A failed container write leaves the file at the channel and writes no row; the next run retries.
- A failed move after commit is recovered by the duplicate check on the next run.
- Idempotency key: channel code, source reference and file hash.
- No event is published by intake. The scan step and OCR step continue in the same JOB-12 run.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR | Documents CRU | All channels and intake rows |
| RW-PLATADM | Platform administration CRUD | Rerun and channel properties |
| RW-AGENCYMG | Partner portal CRUDA | Partner codes and panel status |
| RW-CASEOWN | Documents R | Documents once attached |

The sender address is stored but masked in every response and absent from the job record and logs. Storage is reached by managed identity only; no key or shared access signature.

### Observability, performance and operations

- Job record: per channel taken in, refused by reason, duplicate; start and end; failed channel.
- Metrics: files per channel, refusal rate, duplicate rate, container failures, run duration.
- Alerts: two consecutive failures on one channel (MSG-P5-008); container unavailable; SFTP or mailbox unreachable.
- Run book: JOB-12 `intakeStep` in RWB-E1-056.
- Volume: about 860,000 documents in 2027 (NFR-004); 15-minute cadence; one run across instances; four channel readers can run in sequence within the run.

### Feature flag and rollback

`rwb.dochub.intake` with one sub-flag per channel. Off: `intakeStep` does not read that channel. Rollback: turn the flag off and redeploy the previous tag; the migration is forward-only and the new columns are nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-057-01 | AC1, BR1 | System | PDF in branch folder BR-0123 | One SCAN row; channel BR-0123; captured time; empty scan result; processed move. |
| TC-E1-057-02 | AC2, BR1, BR4 | System | PDF in SFTP subfolder LF-007 | One PARTNER row; channel LF-007; partner ID. |
| TC-E1-057-03 | AC3, BR1, BR9 | System | Mailbox stub with one PDF and a synthetic sender | One EMAIL row; sender masked; email archived. |
| TC-E1-057-04 | AC4, BR1 | System | PDF in the mailroom folder | One SCAN row; channel MAILROOM. |
| TC-E1-057-05 | AC5, BR2 | System | DOCX file | No row; rejected folder; 1 refused with MSG-P5-007/MSG-P5-001. |
| TC-E1-057-06 | AC6, BR2 | System | 25.1 MB and 25.0 MB PDFs | 25.1 refused with MSG-P5-017; 25.0 has a row. |
| TC-E1-057-07 | AC7, BR4 | System | Subfolders LF-099 and LF-008 (suspended) | No rows; reasons PARTNER_UNKNOWN and PARTNER_NOT_ACTIVE. |
| TC-E1-057-08 | AC8, BR5 | System | Same file two days apart | No second row; processed; duplicate count 1. |
| TC-E1-057-09 | AC9 | System | All channels empty | Zero counts per channel. |
| TC-E1-057-10 | AC10 | System | Container refuses writes, then accepts | No row; file stays; next run takes it in. |
| TC-E1-057-11 | AC11, BR7 | System | SFTP folder unreadable for two runs | MSG-P5-008 naming PARTNER_SFTP; next run retries. |
| TC-E1-057-12 | AC12, BR7 | System | Two instances, one cluster | One run for 09:15; one row per file. |
| TC-E1-057-13 | AC13 | System | Email with no attachment; email with a 6 KB image | No rows; both archived. |
| TC-E1-057-14 | AC14, BR6 | System | Move to processed forced to fail | No second row; file moved on the next run. |
| TC-E1-057-15 | AC15, BR7 | System | Clock at 18:15 on a working day | No run until 08:00 the next working day. |
| TC-E1-057-16 | AC16, BR3 | System | Item taken in; scan step delayed | OCR does not read it until scan_result CLEAN. |
| TC-E1-057-17 | X12 | Security | RW-CASEOWN calls the rerun endpoint | 403 MSG-P4-002. |

## Guardrails

- No business value in code: folders, mailboxes, types, size limit and windows are properties and parameters.
- No personal data in logs, tests or prompts: sender addresses and email file names are not logged; test emails use synthetic senders.
- No read of another module's tables: partners come through `PartnerDirectory`.
- A file is never removed from a channel before its `document_intake` row is committed.
- Storage is reached by managed identity only.

## Out of scope

- The malware scan and quarantine (RWB-E1-041), OCR (RWB-E1-049), classification (RWB-E1-050), extraction (RWB-E1-053) and matching to a case (RWB-E1-032).
- Uploads from the case documents screen (RWB-E1-026).
- Field app photos and bills (RWB-E2-024).
- Partner uploads through the partner portal (Epic 4, PRT-03; DL03).

## Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-009 | Documents arrive from branches, mailroom, partner file transfer and email through the same intake | FEAT-DCM-13, FEAT-DCM-14, FEAT-DCM-15 | 13 Manage documents and correspondence; 12 Manage partners | R-UNI-33, R-UNI-40 | TC-E1-057-01..15, TC-E1-057-17 |
| REQ-DCM-010 | Retention class on every document; virus scan before storing | FEAT-DCM-13 | 13 Manage documents and correspondence | None | TC-E1-057-16 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC15; SPEC-001 | The cron `0 0/15 8-17` puts the last run at 17:45, while the background says runs every 15 minutes from 08:00 to 18:00. | Determines the last run of the day. | Keep the cron in section 12: 08:00 to 17:45, with 18:00 as the end of business hours; AC15 confirms no run at 18:15. Confirm with batch scheduling before build. | RESOLVED | SPEC-RWB-E1-057-001 |
| CLAR-002 | Preconditions; SPEC-002, SPEC-009 | The mail service is assumed to be Exchange Online through Microsoft Graph and no decision covers it. | Determines the mailbox adapter, not the intake behaviour. | Accept as an ASSUMED integration behind `MailboxChannelReader`; the platform architect confirms the interface before build. No business behaviour changes. | RESOLVED | SPEC-RWB-E1-057-002, SPEC-RWB-E1-057-009 |
| CLAR-003 | AC12; SPEC-001 | How is "one run across two instances" enforced? | Determines duplicate intake. | Quartz clustered execution with a database lock and `@DisallowConcurrentExecution`; the run record is unique per scheduled time. | RESOLVED | SPEC-RWB-E1-057-001 |
| CLAR-004 | BR5; SPEC-004 | What are the duplicate window and the comparison key? | Determines whether a legitimate resend is lost. | 30 days, same channel and same SHA-256 hash; the window is a parameter under DL11. | RESOLVED | SPEC-RWB-E1-057-004 |
| CLAR-005 | BR2; SPEC-005 | Is the size limit decimal MB, and is 25.0 MB accepted? | Determines the boundary test. | Decimal MB; 25.0 MB is accepted and 25.1 MB is refused, as AC6 states. | RESOLVED | SPEC-RWB-E1-057-005 |
| CLAR-006 | BR9; SPEC-009 | Is the sender address stored at all? | Determines the masking and log rules. | Stored in `sender_address` for traceability, masked in every response and absent from the job record and logs under CTL-11 and DL26. | RESOLVED | SPEC-RWB-E1-057-009 |
| CLAR-007 | BR7; RWB-E1-041; SPEC-001 | 041's spec says `scanStep` is first; 057 adds `intakeStep` before it. | The scan cannot run before the file is taken in. | Order is `intakeStep` → `scanStep` → `ocrStep` → `classifyStep` → `extractStep` → `matchStep`; 041's "first" means first of the pre-existing steps. | RESOLVED | SPEC-RWB-E1-057-001 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or the decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend intake step on JOB-12 for four channels; no screen and no API contract change; the existing job rerun endpoint is reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new intake capability with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 16 acceptance criteria and 12 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

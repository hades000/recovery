# RWB-P5-E1041-APP Retention classes and virus scan on intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1041-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-041 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP18, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-022, FR-P5-023, FR-P5-024, FR-P5-025) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the retention classes, the monthly retention run and the virus scan on intake moved into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the Temporal task queue `rwb-document` and the monthly retention Schedule of the workflow kit. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and PDPA officer (RW-COMPLY)**, I want **every uploaded or scanned file checked for malware before it is stored, and a retention class per document type that the store applies and a monthly job acts on**, so that **the store holds only safe files and keeps each document for the time the policy sets, never removing one silently or while a legal hold is in place**.

Inside `rwb-document` this is the retention and intake-safety capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- Retention is this service's own: `retention_rule` and `retention_action` are P5's in `rwb_document` (the Ownership Map ruling moves the retention tables to the document hub, on Architecture v5 slides 16, 41 and 44 where JOB-17 runs in `rwb-document`), and the legacy monthly job JOB-17 becomes the `retention-monthly` Temporal Schedule on queue `rwb-document` through the workflow kit (DP-10, H RWB-PLT-E1071-CON).
- The scan result is a document attribute written by this service: `document_intake.scan_result` and `document_intake.scanned_at` (DF-DOC-058, DF-DOC-059) on the intake path, and the same two attributes on the `document` row for an upload that creates no intake item. The scanning engine's own capacity, licences, queue and throughput are not this story's table and not this service's data (ASM-1771).
- The file itself is never written or moved by this story's own code: the store RWB-P5-E1024-APP owns the Blob containers and the platform storage product, and this story calls the store to move an infected file to `rwb-quarantine`, to move a due blob to the archive tier and to write the review-list file to the standard container.
- The legal hold is `recovery_case.legal_hold` (DF-CAS-020) in `rwb-case`, read through the case contract `GET /cases/{caseId}` (DP-11, one hop, 2 s timeout, breaker per downstream) and never from a case table and never from a `rwb_case` copy. The plan lists no C row for that read; it is consumed and faked (ASM-1769).
- The class of a type is `document_type.retention_class` (DF-REF-223) read locally; the class rows with the period, the age basis, the end action and the rule version are `retention_rule` (DF-REF-116 to DF-REF-127); the list values of LOV-RETENTION, LOV-SCAN-RESULT, LOV-RETENTION-ACTION and LOV-RETENTION-END are read through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON) and no list value is typed in code.
- Every archive and every listed disposal writes its decision record through the local decision-record library of DP-03, in the same transaction as the `retention_action` row and the event row, with decision code DOCRET; a failed record means nothing is archived (MSG-P7-003, R-UNI-39).
- The interaction ledger is `rwb-source-data`'s (DP-18): this service owns no ledger table, reads no ledger row and writes no ledger row. The audit event `MALWARE_BLOCKED` of the legacy story is an audit entry in the service audit log, and where the monolith also recorded the scan in the ledger, the target keeps the audit entry and reaches the ledger only through the P1 contract, never through a local table.
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-0995; ASM-1772); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, exception paths, business rules, messages, authority, data fields, ten acceptance criteria and twelve test cases, adapted to the target service's schema, topic, API base, workflow template and Schedule.

### 2. Business rationale

Files reach the bank from branches, partners and email; one infected file in the store reaches every user who opens it. Documents also have no retention rule today, so nothing shows when a document may be archived (FSD P5 A2.17, A2.18). This story scans every file before storage and quarantines a failed file, holds the retention classes as data, and runs the monthly retention run to archive documents past their class or list them for the Compliance review. It meets REQ-DCM-010 and REQ-DCM-016 (legal hold overrides retention), with NFR-028, NFR-072 and NFR-074.

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). No table of another service is read, the legacy recovery-schema names do not survive, and the retention tables sit in the document hub's own schema.
2. The legal hold arrives through the `rwb-case` contract `GET /cases/{caseId}` with a mock and a 2 s timeout (DP-11, C from the legacy dependency), so the run builds against a published shape and never against a case table.
3. The class list is reference data of `rwb-case` behind the reference-data contract and client library (DP-07), while the class rows themselves are this service's `retention_rule` data, loaded and approved through its own admin operation. That split is the reason the legacy reference-load step becomes a document-hub operation and the list values stay with the reference-data owner.
4. The legacy decision-log write becomes the local decision-record library of DP-03, written in the same transaction as the `retention_action` row and the event row and published on `rwb.decision-record.v1`; `rwb-decision` collects it into the central ledger, so an archive without its record does not proceed.
5. JOB-17 becomes the `retention-monthly` Schedule of the workflow kit on queue `rwb-document` (DP-10): a Schedule, a workflow and activities, not a Quartz row and not a shared job table. The scan step becomes an activity of the intake workflow owned by RWB-P5-E1049-APP, which is why the scan runs first without this story owning the 15-minute Schedule.
6. The interaction ledger leaves this story altogether (DP-18): the ledger is P1's, the audit event is an audit entry, and the job counts live on the run record of this service rather than in a ledger row.
7. The retention and scan reads reach the screens through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON); the migration is one step in the per-service Flyway sequence (DP-15) in `rwb_document`.
8. The retention periods and the end actions stay data of the class version in force (the legacy assumed DL26), and the scan engine stays behind a client and a stub, so neither the period of a class nor the provider of the scanner is a value of this code.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1027-CON | The decision-record library: `RecordAndApply` writes the DOCRET record inside the caller's transaction and publishes it on `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-RETENTION, LOV-SCAN-RESULT, LOV-RETENTION-ACTION and LOV-RETENTION-END (DP-07) |
| RWB-PLT-E1071-CON | The workflow kit with the "Scheduled job" template, activity registration, retry policy and Schedule registration (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the retention and scan migration as one step in `rwb_document` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the retention and scan states to SCR-44 and SCR-47 (DP-19) |
| RWB-P5-E1024-APP | The store: `document`, `document_type`, the containers `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, the archive tier and the blob moves |
| RWB-P5-E1049-APP | The intake record `document_intake`, the 15-minute document-intake Schedule (legacy JOB-12) and the workflow that calls the scan step first, before the OCR step |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the four lists (DP-07) |
| RWB-P3-E1018-CON | The `rwb-case` contract `GET /cases/{caseId}` with its fake, so `legal_hold` is read in one hop with a 2 s timeout (DP-11); consumed and faked although the plan lists it in no C row (ASM-1769) |

Business preconditions carried from RWB-E1-041:

- RWB-P5-E1024-APP is done: documents carry `retention_class` and `write_once` from the type table.
- RWB-P5-E1049-APP is done: `document_intake` exists and the scan step runs first in the intake workflow.
- The quarantine container `rwb-quarantine` exists and the bank malware scanning service is reachable through the scan client under SY-OCR (assumed: the scanning service of the ACE storage pattern, DL27; the provider is not named in any source, ASM-1771).
- Retention class table loaded through the class load of 12.1, table RETENTION_CLASS, version RET-2026.11: LEGAL10Y 120 months, end action REVIEW; GENERAL05Y 60 months, end action ARCHIVE (assumed; DL26; ASM-1770).
- The `rwb-case` contract returns `legal_hold` for a case.
- Feature flags `rwb.document.malware-scan` and `rwb.document.retention` are on. The legacy flag names `rwb.dochub.malware-scan` and `rwb.dochub.retention` are retired with the monolith.

The database login name is Not specified in the source documents (GAP-0995; ASM-1772). The name of the scanning service and its provider is Not specified in the source documents (GAP-0995; ASM-1771).

The status and the release are the run defaults of D-RCV-60: the story is Draft (realignment v1) and the release is 30 November 2026 (tentative), with no approval and no build go-ahead recorded in the sources read (ASM-1773).

### 4. Flow

1. The 15-minute document-intake Schedule (legacy JOB-12, owned by RWB-P5-E1049-APP) starts `DocumentIntakeWorkflow` and runs the scan step first, before the OCR step (12.5).
2. `scanIntakeItem` activity: selects intake items with no `scan_result` and sends each file to the scan client, which calls the bank scanning service through `POST /scans` of this service's own contract (12.1, 12.2); the item's `intake_ref` is the only identifier sent, never the file name or its content.
3. `scanIntakeItem`: on `CLEAN`, sets `document_intake.scan_result` = CLEAN and `scanned_at`, so the OCR step may read the item; on `INFECTED`, calls the store to move the file to `rwb-quarantine`, sets `scan_result` = INFECTED, writes the audit event `MALWARE_BLOCKED` with the intake ID and the source to the service audit log, and alerts the platform administrator; no `document` row is ever written and the file is never stored.
4. Upload (RWB-P5-E1026-APP): calls `POST /scans` before the store call; an `INFECTED` answer returns 422 MSG-P5-016 on the upload and nothing is stored; if the scanning service does not answer inside the declared budget the call returns 503 MSG-P5-022 and nothing is kept.
5. The store (RWB-P5-E1024-APP): stores clean files with the retention class of the type; legal types go to the write-once container. This story writes no document row and no blob.
6. `retention-monthly` Schedule starts `RetentionWorkflow` on the first Sunday of each month at 02:30 Asia/Bangkok; for each active document the run computes expiry date = stored date (`document.created_at`) plus `retention_months` of its class row in the version in force.
7. `checkLegalHold` activity: skips a document whose case has `legal_hold` true, read through the `rwb-case` contract, and counts it as held (`retention_action.action` = HELD).
8. `archiveDocument` / `listForReview` activities: for a due document with end action ARCHIVE, writes the decision record DOCRET through the library of DP-03, calls the store to move the blob to the archive tier, sets the document state ARCHIVED and inserts the `retention_action` row (action ARCHIVED) in the same transaction as the record; for end action REVIEW, adds it to the review list for Compliance, inserts the action row (action LISTED) and changes nothing else.
9. `writeReviewList` activity: writes the review list to `retention/review/{runDate}.csv` in the standard container through the store, and the counts (due, archived, listed, held, exceptions) to the run record; `Exception` rows carry RETENTION_CLASS_MISSING where a class is not in force.
10. Event and record relay: the retention_action row, its decision record and the `rwb.document.RetentionApplied.v1` row are committed together; the platform relay publishes the record on `rwb.decision-record.v1` and the event on `rwb.document.events.v1`, once per committed action, keyed by caseId, with no personal data.
11. Compliance reads the review list file and the run counts; the platform administrator sees the scan alerts and the run results through the composite route of DP-19.

The decision record is written before the change takes effect and in the same transaction as the `retention_action` row and the event row, so a failure leaves all three unchanged (R-UNI-39).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The scan finds malware on an intake file | File quarantined, not stored, audit event written, platform administrator alerted | MSG-P5-016 | AC1 |
| X2 | The scanning service does not answer | Intake item stays unscanned and is not read by OCR; retried in the next run; alert after two failed runs; an upload returns 503 and nothing is stored | MSG-P5-022 | AC6 |
| X3 | A due document is on a case with a legal hold | Not archived, not listed; counted as held | None | AC5 |
| X4 | A document carries a class not in the retention table | Listed as an exception RETENTION_CLASS_MISSING; nothing changes | None | AC7 |
| X5 | The retention run runs again in the same month | Documents already archived or listed for that month are not acted on again | None | AC8 |
| X6 | A retention class load holds an end action other than ARCHIVE or REVIEW, or a period of 0 months | Load refused in full | MSG-P3-027 | AC9 |
| X7 | The decision record write fails for an archive | The document stays as it is; picked up by the next run; incident raised (R-UNI-39) | MSG-P7-003 | TC-E1-041-12 (Principle 5) |
| X8 | A role without Reference data C loads retention classes | Refused with 403 | MSG-P4-002 | TC-E1-041-11 (Access) |
| X9 | The `rwb-case` contract does not answer within 2 s, or the breaker is open | The document is counted as an exception of the run and is not archived; the next run picks it up; the failure names the case service | MSG-GEN-006 | TC-E1-041-05 (target path) |
| X10 | The Schedule does not fire, or the workflow is stopped mid-run | The run resumes from the last committed chunk of 500 documents; the month key on `retention_action` keeps every decided document from being acted on twice | None | AC8 (target path) |
| X11 | The relay is down when an action commits | The action row, the decision record and the event row are committed; the relay publishes both when it recovers, once, with no duplicate action | None | TC-E1-041-03 (target path) |
| X12 | A store call for the quarantine move or the archive move fails | The item or document keeps its state; the activity retries under the workflow kit's retry policy; an item scanned CLEAN is never stored without its scan result | MSG-GEN-006 | AC1, AC3 (target path) |

Two target-service notes:

- A repeated scan of the same item is refused by the item's own `scan_result` and by the `Idempotency-Key` of `POST /scans` (the pair `storageRef` and `sha256`), so a retried activity writes one result and one audit entry.
- The legacy rerun operation is not a REST operation of this story: a rerun is the same Schedule started for the same run month, and the unique key (`document_id`, `run_month`) on `retention_action` makes the second start act on nothing that was already decided (AC8). The run resource and its read belong to RWB-P5-E1017-APP.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-P5-E1024-APP) and the intake (RWB-P5-E1049-APP); the upload (RWB-P5-E1026-APP) calls this scan; all three are earlier or in-lane work |
| Negotiable | Retention periods and end actions are data of the class version under DL26; the scanning service is reached through a client, a stub and a timeout property |
| Valuable | No infected file reaches a user; every document has a retention rule from day one and no document leaves the store silently |
| Estimable | One scan activity, one Schedule, one workflow with six activities, two tables and one client |
| Small | Fits within one week with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Retention classes and virus scan on intake

  Background:
    Given retention class table version "RET-2026.11" is in force
    Given class "LEGAL10Y" has period 120 months and end action "REVIEW"
    Given class "GENERAL05Y" has period 60 months and end action "ARCHIVE"
    Given the rwb-case contract mock returns the reference-data list "LOV-RETENTION" with class "LEGAL10Y"
    Given the rwb-case contract mock returns the reference-data list "LOV-SCAN-RESULT" with the values "CLEAN" and "INFECTED"

  Scenario: AC1 Malware blocked (legacy RWB-E1-041 AC1)
    Given a test file "eicar-0002.pdf" with the EICAR signature as an intake item from a branch scanner
    When JOB-12 runs the scan step
    Then the item has scan_result "INFECTED" and the file is in the quarantine container
    Then no document row exists for the file and the OCR step does not read it
    Then the system writes the audit event "MALWARE_BLOCKED" with the intake ID and the source, and the platform administrator is alerted

  Scenario: AC2 Retention class (legacy RWB-E1-041 AC2)
    Given a demand letter of type "DEMAND_LETTER" with class "LEGAL10Y" in the type table
    When the document is stored on case "RW-2026-000123"
    Then the document row carries retention class "LEGAL10Y" and write_once true
    Then the file is in the write-once container

  Scenario: AC3 Expiry with end action archive (legacy RWB-E1-041 AC3)
    Given an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000123" with no legal hold
    Given the rwb-case contract mock returns case "RW-2026-000123" with legal_hold false
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCRET"
    When JOB-17 runs on 6 December 2026
    Then the document has state "ARCHIVED" and its blob is in the archive tier
    Then one decision log entry "DOCRET" names the document, class "GENERAL05Y", version "RET-2026.11" and expiry date 1 November 2026

  Scenario: AC4 Expiry with end action review (legacy RWB-E1-041 AC4)
    Given a court notice of class "LEGAL10Y" stored on 1 November 2016 on case "RW-2026-000456"
    Given the rwb-case contract mock returns case "RW-2026-000456" with legal_hold false
    When JOB-17 runs on 6 December 2026
    Then the system lists the court notice in "retention/review/2026-12-06.csv" with its class and expiry date
    Then the document and its blob are unchanged

  Scenario: AC5 Legal hold overrides the class (legacy RWB-E1-041 AC5)
    Given an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000789" with legal_hold true
    Given the rwb-case contract mock returns case "RW-2026-000789" with legal_hold true
    When JOB-17 runs on 6 December 2026
    Then the system does not archiv the document and not listed
    Then the job record counts it as held

  Scenario: AC6 Scanning service unavailable (legacy RWB-E1-041 AC6)
    Given the scanning service stub returns no answer
    When JOB-12 runs twice with 3 unscanned intake items
    Then the 3 items have no scan_result and the OCR step reads none of them
    Then the system alerts the platform administrator after the second run
    Then an upload during the outage returns 503 with MSG-P5-022 and no document row or blob is written

  Scenario: AC7 Class not in the retention table (legacy RWB-E1-041 AC7)
    Given a document with retention class "OLD03Y" that is not in version "RET-2026.11"
    When JOB-17 runs
    Then the system lists the document as exception "RETENTION_CLASS_MISSING" in the review list
    Then the document is unchanged

  Scenario: AC8 Second run in the same month (legacy RWB-E1-041 AC8)
    Given JOB-17 ran on 6 December 2026 and archived 4 documents and listed 9
    When JOB-17 is rerun on 7 December 2026
    Then the system archives no document again, no second "DOCRET" entry is written and the review list still holds 9 rows

  Scenario: AC9 Invalid retention class load (legacy RWB-E1-041 AC9)
    Given a load file for table "RETENTION_CLASS" with class "TEMP01M" at period 0 months and end action "DELETE"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P3-027 naming both errors
    Then version "RET-2026.11" stays in force

  Scenario: AC10 Expiry on the run date (legacy RWB-E1-041 AC10)
    Given an appraisal report of class "GENERAL05Y" stored on 6 December 2021
    Given the rwb-case contract mock returns its case with legal_hold false
    When JOB-17 runs on 6 December 2026
    Then the system archives the document , because its expiry date equals the run date
```

Every Given, When and Then line above is the legacy line unchanged; the target-service part is the three added mock Givens (`rwb-case` for the case and its hold, `rwb-case` for the two lists, `rwb-decision` for the DOCRET record), and the legacy endpoints of the story map to the target operations of 12.1: `MalwareScanService.scanNow` is `POST /scans`, the item scan state is `GET /intake-items/{intakeItemId}/scan-status`, the retention class read is `GET /retention-rules` and `GET /retention-rules/{classCode}`, and the legacy class load is `POST /admin/retention-loads` with `POST /admin/retention-loads/{loadId}/approve`.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every file is scanned for malware before it is stored; an infected file is quarantined and never stored | REQ-DCM-010; FEAT-DCM-18 |
| BR2 | Every document carries a retention class from its type | REQ-DCM-010; NFR-028 |
| BR3 | Retention periods and end actions are data owned by Compliance | Retention classes reference table; DL26 |
| BR4 | A legal hold stops archive and expiry for as long as it is in place | REQ-DCM-016; NFR-072; recovery_case.legal_hold |
| BR5 | No document is removed by the retention run; an end action REVIEW lists it for a recorded decision | NFR-074; REQ-DCM-019 (Epic 2) |
| BR6 | A document with a class missing from the table is listed as an exception | R-WO-48 |
| BR7 | An archive that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR8 | A document is due when its expiry date is on or before the run date | Retention classes reference table; JOB-17 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by the scan step running first inside `DocumentIntakeWorkflow` and by the upload calling `POST /scans` before its store call; a CLEAN answer is the only path to a document row, and an INFECTED answer leaves the file in `rwb-quarantine` and the item unread. The engine is behind the scan client, its provider is not named in the sources, and the timeout is the property `rwb.document.scan.timeout-seconds` = 30 carried from the legacy story (ASM-1771).
- BR2 and BR3 read the class of the type from `document_type` and the class row from `retention_rule` in the version in force (`valid_from`, `valid_to`, `rule_version`); the period, the age basis and the end action are never written in code, and the load refuses an invalid row in full (AC9). The list values come from the `rwb-case` reference-data contract (DP-07).
- BR4 is executed by `checkLegalHold` reading `recovery_case.legal_hold` through the case contract on every run, never from a case table and never from a local copy, and by the run counting a held document as HELD in `retention_action` (AC5).
- BR5 is executed by the run never deleting a blob: an end action REVIEW writes a LISTED row and the review-list file, and the disposal or the extension of the document is a later recorded decision (Epic 2).
- BR6 is executed by the exception path of the run: a class that is not in the rule version in force writes an EXCEPTION row with RETENTION_CLASS_MISSING, is listed in the review file and changes nothing.
- BR7 is executed by the decision-record library of DP-03 inside the archive transaction: the record, the `retention_action` row and the event row commit together or not at all (R-UNI-39).
- BR8 is executed by the due selection `expiry_date <= run_date`, computed from `document.created_at` as the stored date and `retention_months` of the class row; AC10 fixes the boundary as an inclusion.
- DP-01 keeps every table in `rwb_document`; DP-07 keeps the four lists in reference data; DP-11 makes the hold one hop with a 2 s timeout; DP-15 puts the two-table migration in the per-service Flyway sequence; DP-18 keeps the ledger with P1; DP-19 puts the two screen reads behind the composite route.

### 9. State transitions

No case state machine in this story: it changes no case status. It changes the intake item scan result and the document state:

| From | Event | To |
|---|---|---|
| `document_intake.scan_result` (none) | `scanIntakeItem` receives CLEAN | `scan_result` = CLEAN, `scanned_at` set, the OCR step may read the item |
| `document_intake.scan_result` (none) | `scanIntakeItem` receives INFECTED | `scan_result` = INFECTED, the file is in `rwb-quarantine`, no document row exists |
| `document_intake.scan_result` (none) | the scanning service does not answer | unchanged; retried by the next intake run; alert after two failed runs |
| `document.state` = STORED | the run archives with end action ARCHIVE and the DOCRET record commits | ARCHIVED, the blob is in the archive tier |
| `document.state` = STORED | the run meets end action REVIEW | unchanged; `retention_action.action` = LISTED |
| `document.state` = STORED | the run meets `legal_hold` true | unchanged; `retention_action.action` = HELD |
| `document.state` = STORED | the class is not in force | unchanged; `retention_action.action` = EXCEPTION |

A document that is out on custody is not moved to the archive tier while a custody row with a `due_back` date is open; it is counted as an exception of the run and its review-list row names the location and the due-back date (DF-DOC-021, DF-DOC-024, read only; no custody row is written by this story).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs the scan step (Documents CRU) |
| RW-COMPLY, compliance and PDPA officer | Owns the retention classes; reads the review list and the run counts |
| RW-REFADM, reference data administrator | Loads the retention class table (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the compliance and PDPA officer as table owner (DL01; ASM-1770) |
| RW-PLATADM, platform administrator | Receives scan alerts; reruns the intake and the retention run |
| SY-DECLOG, decision record writer | Writes the DOCRET record |
| SY-DOCUMENT, the rwb-document service identity | Runs the Schedule, the activities, the quarantine move and the archive move |

The authorisation decision is taken by `rwb-access` (roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds; this story adds no guard of its own and inherits the 403 shape with MSG-P4-002. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-0995; ASM-1772).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | `document` | id | Read |
| DF-DOC-002 | `document` | case_id | Read |
| DF-DOC-006 | `document` | storage_ref | Read |
| DF-DOC-009 | `document` | retention_class | Read |
| DF-DOC-010 | `document` | write_once | Read |
| Standard column | `document` | state | Write |
| Standard column | `document` | created_at | Read, as the stored date |
| Standard column | `document` | version | Write, as the optimistic lock of a state change |
| Design column added by this story | `document` | scan_result | Write, for an upload that creates no intake item |
| Design column added by this story | `document` | scanned_at | Write, for an upload that creates no intake item |
| DF-DOC-058 | `document_intake` | scan_result | Write |
| DF-DOC-059 | `document_intake` | scanned_at | Write |
| DF-DOC-057 | `document_intake` | intake_ref | Read, as the only identifier sent to the scan client |
| DF-REF-116 to DF-REF-127 | `retention_rule` | all fields | Write (this story creates the record) |
| DF-DOC-091 to DF-DOC-095 | `retention_action` | all fields | Write (this story creates the record) |
| DF-REF-223 | `document_type` | retention_class | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-DOC-021 | `document_custody` | from_location | Read, for the review-list row of a document out on custody |
| DF-DOC-024 | `document_custody` | due_back | Read, for the same row |
| DF-CAS-020 | `rwb-case` case, through the contract | legal_hold | Read |
| (decision record) | decision-record library table in `rwb_document` | chain_seq, inputsRef, ruleId, finalCall, decidedAt, prev_hash, entry_hash | Write |
| (outbox) | outbox library table in `rwb_document` | the row of RetentionApplied and the decision record | Write |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. Two scan columns on `document` are added by the migration of this story because the sources hold the two attributes on `document_intake` only and an upload creates no intake item; the addition is design and is recorded with the class-load and scan-surface gap (GAP-0995; ASM-1771). No `rwb_case` row is copied, no ledger row is read (DP-18), and no ACE view is read. `held_by` of `document_custody` is never read: it holds a person's name and the review-list row carries the location and the date only.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/scans` | P5 | Scans one file and answers `ScanResult` synchronously: `storageRef`, `sha256`, `intakeId` (optional), `source`; 200 with CLEAN or INFECTED, 503 MSG-P5-022 when the engine does not answer. `Idempotency-Key` required; internal operation, service identity only |
| GET | `/api/recovery/document/v1/documents/{documentId}/scan-status` | P5 | `ScanStatus` of a stored document: scanResult, scannedAt, threatFound, quarantineRef |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/scan-status` | P5 | `ScanStatus` of an intake item, read from `document_intake` (DF-DOC-058, DF-DOC-059) |
| GET | `/api/recovery/document/v1/retention-rules` | P5 | Query ruleVersion, docTypeCode, productCode, page, size; answers `RetentionRulePage` in the version in force |
| GET | `/api/recovery/document/v1/retention-rules/{classCode}` | P5 | Answers `RetentionRule` in the version in force; 404 when the class is not in force |
| POST | `/api/recovery/document/v1/admin/retention-loads` | P5 | The class load: multipart file and `validFrom`, table RETENTION_CLASS; 201 `RetentionLoad`. Reference data right C; `Idempotency-Key` required (table code and table version) |
| POST | `/api/recovery/document/v1/admin/retention-loads/{loadId}/approve` | P5 | Approves a loaded version; Reference data right A; 200 `RetentionLoad`; 409 when the version is already loaded or already in force |
| GET | `/api/recovery/document/v1/admin/retention-loads/{loadId}` | P5 | `RetentionLoad` with the accepted and refused rows and their reasons |

The paths and the field names of the eight operations are fixed by RWB-P5-E1041-CON, because no source names them (GAP-0995; ASM-1769). The class list used by the SCR-31 and SCR-32 panels is declared by RWB-P5-AD021-CON on the same base and is a projection of the same `retention_rule` rows; this story does not re-declare it. The run resource and its read belong to RWB-P5-E1017-APP. Errors follow RFC 9457 with `messageId`.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 | RWB-P3-E1018-CON | The case and its `legal_hold`, one hop, 2 s timeout, breaker per downstream (DP-11); consumed and faked although the plan lists it in no C row (ASM-1769) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 | RWB-P3-E1043-CON | LOV-RETENTION, LOV-SCAN-RESULT, LOV-RETENTION-ACTION and LOV-RETENTION-END in the version in force (DP-07) |

The two lists and the hold are read through the client libraries of DP-07 and DP-11, which wrap the two contracts. No interaction-ledger operation is consumed: the ledger is `rwb-source-data`'s and this story writes no ledger row (DP-18). The blobs are moved through the store RWB-P5-E1024-APP, which is a same-service H dependency and not a REST contract of another service; the file move appears in 12.9 as File.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.RetentionApplied.v1` | `rwb.document.events.v1` | P5 | caseId | documentId, caseId, runMonth, action, retentionClass, ruleVersion, expiredAt, decisionLogRef |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with decision code DOCRET and final call ARCHIVED, LISTED, HELD or EXCEPTION |

CloudEvents 1.0 envelope, binary mode; no personal data in either payload, and no file byte, no document name and no customer value. The event row is written inside the transaction of the `retention_action` row and the decision record, so it exists exactly when the action exists; the envelope, the outbox and the relay are the platform library's, and the schema is fixed by RWB-P5-E1041-CON. `rwb.document.DocumentStored.v1` and `rwb.document.DocumentFieldsExtracted.v1` are the service's other two events and belong to other stories; the retention event is added by this key and recorded in the Kafka Topic and Event Catalog (GAP-0995; ASM-1774).

#### 12.4 Events consumed

None. This story consumes no Kafka event: the intake Schedule starts the workflow, the case hold and the two lists are synchronous reads, and the storage moves are same-service calls.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | Owned by RWB-P5-E1049-APP; the scan step runs first, before the OCR step |
| `scanIntakeItem` | Activity, contributed by this story | `rwb-document` | Scans one intake item, moves an infected file to `rwb-quarantine`, writes `scan_result` and `scanned_at`, writes the `MALWARE_BLOCKED` audit entry and the two-failure alert counter |
| `RetentionWorkflow` | Workflow, from the L3 workflow kit template "Scheduled job" | `rwb-document` | Owned by this story: the monthly retention run (legacy JOB-17), started by the `retention-monthly` Schedule |
| `selectDueDocuments` | Activity | `rwb-document` | Selects the active documents whose expiry date is on or before the run date, in chunks of 500 |
| `checkLegalHold` | Activity | `rwb-document` | Reads `legal_hold` through the `rwb-case` contract and marks the held documents HELD |
| `archiveDocument` | Activity | `rwb-document` | Writes the DOCRET record, calls the store to move the blob to the archive tier, sets state ARCHIVED, writes the retention_action row and the event row |
| `listForReview` | Activity | `rwb-document` | Writes a LISTED or EXCEPTION row and changes no document |
| `writeReviewList` | Activity | `rwb-document` | Writes `retention/review/{runDate}.csv` through the store and the run counts to the run record |

The workflow kit fixes the retry policy, the continue-as-new boundary and the Schedule registration (DP-10, H RWB-PLT-E1071-CON); this story contributes the template configuration and the activities, not a scheduler.

#### 12.6 Schedules

| Schedule | Job | Owner | Detail |
|---|---|---|---|
| `retention-monthly` | JOB-17 Retention | P5, this story | Temporal Schedule on queue `rwb-document`: monthly on the first Sunday at 02:30 Asia/Bangkok, starting `RetentionWorkflow` with the run month as its input; the run month is the idempotency key of the run |
| document intake, every 15 minutes in business hours | JOB-12 Document intake | RWB-P5-E1049-APP | Named because the scan step rides inside it; this story registers no Schedule for it and only contributes the `scanIntakeItem` activity the started workflow calls |

Both legacy schedules become Temporal Schedules of the workflow kit (DP-10); no Quartz row and no shared job table survives. The rerun of a month is a second start of the same Schedule with the same run month, and the unique key (`document_id`, `run_month`) on `retention_action` makes it act on nothing already decided.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `retention_rule` | P5 | The class rows: product code, table name, record class, period, age basis, end action, rule version, validity and approver |
| `retention_action` | P5 | What the run did with one document in one month, with its decision-record reference; the unique (`document_id`, `run_month`) key |
| `document` | P5 | Read: class, stored date, storage reference, write-once flag. Write: state and the two scan attributes of an upload |
| `document_intake` | P5 | Read: the item and its reference. Write: `scan_result` and `scanned_at` |
| `document_type` | P5 | Read only: the class and the table version of a type |
| `document_custody` | P5 | Read only: the location and the due-back date of a document out on custody, for its review-list row |
| decision-record library table | PLT library, created in `rwb_document` | The DOCRET record, in the archive transaction |
| outbox and idempotency library tables | PLT library, created in `rwb_document` | The RetentionApplied and decision-record rows; the idempotency row of `POST /scans` |

No foreign-schema table is read (DP-01). The interaction ledger is not named: it is P1's and this story owns no ledger table (DP-18). No ACE view is read.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case case fake (`GET /cases/{caseId}`) | RWB-P3-E1018-CON | The hold read of AC3, AC4, AC5 and AC10, its 2 s timeout and the X9 path |
| reference-data fake (`GET /admin/lists/{listCode}`) | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-RETENTION, LOV-SCAN-RESULT, LOV-RETENTION-ACTION and LOV-RETENTION-END |
| decision-record fake | RWB-PLT-E1027-CON | The DOCRET record write and the publish on `rwb.decision-record.v1` |
| central ledger fake | RWB-P7-E1027-CON | The collection of the DOCRET record into the central ledger |
| scanning service stub | this story | CLEAN on a synthetic file; INFECTED on the EICAR signature; no answer for AC6 |
| workflow kit test double | RWB-PLT-E1071-CON | The Schedule start, the activity retry and the continue-as-new boundary of AC8 |
| storage stub of the store | RWB-P5-E1024-APP | The quarantine move, the archive move and the review-list file of AC1, AC3 and AC4 |
| Drools kit | not used | No rule package is evaluated in this story |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 8, consumed 2 | The scan request, the two scan-status reads, the two retention-rule reads and the three class-load operations; the case read and the list read of `rwb-case` |
| Kafka | Published 1 event and 1 decision record; consumed 0 | `rwb.document.events.v1`, `rwb.decision-record.v1` |
| Temporal | 1 workflow owned and 1 contributed; 7 activities | `RetentionWorkflow` with six activities, and `scanIntakeItem` in `DocumentIntakeWorkflow`; the `retention-monthly` Schedule |
| File | 3 moves through the store | The quarantine move, the archive-tier move and `retention/review/{runDate}.csv`; this story writes no byte itself |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, modules `document/retention` and `document/scan`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RetentionAdminController | Controller | The three class-load operations and the two rule reads of 12.1; Reference data rights C and A; refuses an invalid load in full |
| ScanController | Controller | `POST /scans` and the two scan-status reads; maps the engine answer, the timeout and the alert counter |
| ScanClient | Client | Calls the bank scanning service; maps CLEAN, INFECTED and the timeout to the answers of 14; the provider is a property, not a constant |
| ScanActivity | Temporal activity | `scanIntakeItem`: the scan, the quarantine move, the two intake columns, the audit entry |
| RetentionWorkflowImpl | Temporal workflow | `RetentionWorkflow` on queue `rwb-document`, from the workflow kit's "Scheduled job" template |
| RetentionActivities | Temporal activities | `selectDueDocuments`, `checkLegalHold`, `archiveDocument`, `listForReview`, `writeReviewList` |
| RetentionRuleLoader | Service | The class load of table RETENTION_CLASS: row checks, version uniqueness, approve and its separation of duty |
| RetentionRuleRepository | Repository | Reads and writes `retention_rule` only, in the version in force by `valid_from` and `valid_to` |
| RetentionActionRepository | Repository | Writes `retention_action` only; the unique (`document_id`, `run_month`) key is the run's idempotency |
| RetentionReviewWriter | Service | Builds `retention/review/{runDate}.csv` and the run counts |
| RetentionStatePanel | React component | Reads the scan and retention states through the gateway-bff composite route for SCR-44 and SCR-47 |

**Database.**

- One migration in the per-service Flyway sequence (DP-15): `V1041_1__retention_and_scan.sql` creates `retention_rule` (id, product_code varchar(25), table_name varchar(60), record_class varchar(20), retention_months integer, age_basis_field varchar(60), end_action varchar(12), rule_version varchar(20), valid_from date, valid_to date, approved_by uuid, load_id uuid, standard columns) with unique (`table_name`, `record_class`, `rule_version`), check `retention_months between 1 and 600` and check `end_action in ('ARCHIVE','REVIEW')`.
- The same migration creates `retention_action` (id, document_id, run_month char(7), action varchar(12), retention_class varchar(10), rule_version varchar(20), decided_entry_id uuid, standard columns) with unique (`document_id`, `run_month`) and adds `document.scan_result` varchar(10) null and `document.scanned_at` timestamptz null.
- Indexes: `ix_document_retention ON document (retention_class, created_at) WHERE is_active`; `ix_retention_action_run_month ON retention_action (run_month)`; `ix_document_scan_result ON document (scan_result)`.

**Configuration and reference data.**

- Retention classes RET-2026.11, loaded through the class load and approved, owned by Compliance (DL26; the periods are not set by any source and the legacy values are carried as the Compliance default, ASM-1770).
- Properties `rwb.document.container.quarantine` and `rwb.document.scan.timeout-seconds` = 30.
- Decision code DOCRET, assumed; the LOV-DECISION list is loaded by the data steward.
- Feature flags `rwb.document.malware-scan` and `rwb.document.retention`. With the scan flag off, intake items stay unscanned and are not read, and uploads are refused with 503 and MSG-P5-022. With the retention flag off, the run lists due documents and archives none.

**Build steps**

1. Write the migration and the entities; test the two check constraints, the unique version key and the unique run key.
2. Build the scan client against a stub that flags the EICAR signature; test AC1, the timeout and the upload call.
3. Build `scanIntakeItem` with the quarantine move, the audit entry and the two-failure alert; test AC6.
4. Build the class loader with validation and the approve step; test AC9 and the separation of duty.
5. Build the rule reads and the class-in-force rule; unit test the boundary of a valid-from and valid-to date.
6. Build the run selection, the expiry computation and the hold check; unit test AC5, AC7 and AC10 on fixed dates.
7. Add archive with the DOCRET record, the review list and the event row; integration test AC3, AC4 and AC8.
8. Test the access refusal (TC-E1-041-11) and the failed decision record (TC-E1-041-12).
9. Register the `retention-monthly` Schedule through the workflow kit and test one start, one restart and one rerun of the same month.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the two legacy retention tables into `rwb_document` and stops every cross-module read: the hold is no longer read from a case table but from the `rwb-case` contract, which is DP-11 and the C dependency of the legacy story. DP-03 replaces the in-process decision-log writer with the local library, so the DOCRET record, the action row and the event row share one transaction and the record is published on the shared topic. DP-07 keeps the four lists out of the code while the class rows stay in this service's own `retention_rule`, which the Ownership Map gives to P5. DP-10 replaces the Quartz schedule of JOB-17 and the job-step trigger of the scan with a Schedule, a workflow and activities of the workflow kit. DP-13 gives the service its own base. DP-15 puts the two-table migration in the service's own sequence. DP-18 keeps the interaction ledger with `rwb-source-data`: the legacy audit write is an audit entry here and the legacy interaction-ledger position is a call to the P1 owner, never a local table and never a local row. DP-19 puts the two screen reads behind the gateway-bff composite route. The platform event library is not DP-09 in this story: the envelope and the relay are the library's and the schema is RWB-P5-E1041-CON's, so this story only writes the event row inside the DP-03 transaction.

**Done when.** The tests in section 16 pass, the boundary test on `rwb_document` passes, the EICAR file is quarantined in SIT on every intake path, one run of `retention-monthly` archives and lists the expected documents and writes `retention/review/{runDate}.csv`, and `rwb.document.RetentionApplied.v1` is on the topic once per action with no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-016 | Malware found | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P3-027 | Retention class load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P5-022 | Scanning service unavailable on upload | The malware scan is not available, so the file was not stored. Try again in a few minutes. |
| MSG-P7-003 | Decision record write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-006 | The case contract or a store call does not answer | {system} is not available. Your request is queued and will be retried. |

The HTTP mapping is fixed by RWB-P5-E1041-CON: 422 for MSG-P5-016, 422 and 409 for MSG-P3-027, 503 for MSG-P5-022, MSG-P7-003 and MSG-GEN-006, 403 for MSG-P4-002. Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. For MSG-P3-027 the {table} value is RETENTION_CLASS, {error} names the failing check and {row} the row number. For MSG-GEN-006 the {system} value is "Case service" for a case-contract timeout and "Document storage" for a store call.

### 15. Screens and states

No screen of its own in this story. The compliance and PDPA officer reads the review-list file and the run counts; SCR-47 Personal data, which shows retention classes, comes in Epic 8. The platform administrator sees the scan alerts and the run results on SCR-44 Interface and job monitor through the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON):

| State | What the user sees |
|---|---|
| Running | The run of the month in progress with the counts so far |
| Failed | The run stopped with MSG-GEN-006 or MSG-P7-003 and the document that stopped it |
| Complete | The counts of due, archived, listed, held and exceptions, and the review-list file of the month |
| Scan alert | The `MALWARE_BLOCKED` alert of a branch or mailroom item, with the intake ID and the source and no file name |

An uploader sees MSG-P5-016 or MSG-P5-022 in the upload dialog of SCR-30, which belongs to RWB-P5-E1026-APP; this story fixes the two answers, not the dialog.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-041-12 | Principle 5 | NFR | Decision record write forced to fail during an archive; the document unchanged, MSG-P7-003 in the run log, incident raised |
| TC-E1-041-11 | Access | Component | Case owner (RW-CASEOWN, Reference data R only) loads RETENTION_CLASS; refused with MSG-P4-002 |
| TC-E1-041-01 | AC1, BR1 | End to end | EICAR test file from a branch scanner path |
| TC-E1-041-02 | AC2, BR2 | End to end | Synthetic demand letter |
| TC-E1-041-03 | AC3, BR3, BR8 | End to end | Appraisal report stored 1 November 2021, run 6 December 2026 |
| TC-E1-041-04 | AC4, BR5 | End to end | Court notice stored 1 November 2016 |
| TC-E1-041-05 | AC5, BR4 | End to end | Case RW-2026-000789 with legal_hold true |
| TC-E1-041-06 | AC6, BR1 | End to end | Scanning service stub with no answer |
| TC-E1-041-07 | AC7, BR6 | End to end | Document with class OLD03Y |
| TC-E1-041-08 | AC8 | End to end | Rerun on 7 December 2026 |
| TC-E1-041-09 | AC9, BR3 | End to end | Load with period 0 and end action DELETE |
| TC-E1-041-10 | AC10, BR8 | End to end | Appraisal report stored 6 December 2021 |

The legacy level System maps to End to end, Access to Component and Resilience to NFR. No integration harness story exists for this key, so no test case is copied with the `-ITG` suffix; the cross-service proof of the hold and the two lists sits in the wave-1 harness of RWB-E1-049 and in the contract tests of RWB-P5-E1041-CON. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the periods, the end actions, the rule version, the four lists, the scan timeout and the container names are data rows, list values or properties.
- No personal data in the event, the workflow input, the decision record, the audit entry or the log: the `MALWARE_BLOCKED` entry carries the intake ID and the source only, never a file name and never a customer value; `document_custody.held_by` is never read; the review-list file carries IDs, classes and dates only; test files are synthetic.
- No read of another service's tables (DP-01). The hold is read through the `rwb-case` contract, one hop, 2 s timeout, with a mock and a breaker.
- No ledger row (DP-18): the interaction ledger is `rwb-source-data`'s and is reached only through the P1 contract if a ledger entry is ever required.
- The scanning engine's own state, capacity and queue are never stored or queried: the result, the time and the quarantine reference are the only three values this service keeps.
- No document is deleted and no blob is overwritten: the run changes a state and moves a blob to the archive tier; a write-once blob is never touched.
- The run is idempotent twice over: the unique (`document_id`, `run_month`) key, and the run month as the Schedule input.
- The decision record is written in the same transaction as the action row and the event row; a failure archives nothing (R-UNI-39).
- The feature flags `rwb.document.malware-scan` and `rwb.document.retention` remove either capability without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-010 | Every document carries a retention class; intake runs a virus scan before storage | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-18, FEAT-DCM-17 | L2 13.3 Store and retain documents | R-WO-48, R-UNI-39 | TC-E1-041-01 to TC-E1-041-04, TC-E1-041-06 to TC-E1-041-12 |
| REQ-DCM-016 | A legal hold stops deletion and expiry, overriding the class | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-17 | L2 13.3 Store and retain documents | None | TC-E1-041-05 |
| REQ-DCM-019 | Records retention runs by class, and a disposal or an extension is a recorded decision, never silent | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-17 | L2 13.3 Store and retain documents | R-UNI-39 | TC-E1-041-03, TC-E1-041-04, TC-E1-041-12 (the disposal decision itself is Epic 2) |

| Legacy reference | Where it is kept |
|---|---|
| Retention class table version RET-2026.11 and the classes LEGAL10Y 120 months REVIEW, GENERAL05Y 60 months ARCHIVE | Background, sections 3, 4, 8, 13, 16 |
| Legacy jobs JOB-12 scan step and JOB-17 retention | Sections 3, 4, 12.5, 12.6, 16 |
| Event MALWARE_BLOCKED and the decision code DOCRET | Sections 4, 8, 12.3, 13 |
| Messages MSG-P5-016, MSG-P5-022, MSG-P3-027, MSG-P7-003, MSG-P4-002 | Section 14, exception paths |
| Containers rwb-quarantine, the write-once container and the archive tier | Sections 1, 3, 4, 12.9, 13 |
| Review list path `retention/review/{runDate}.csv` and the run counts | Sections 4, 12.5, 12.7, 15 |
| Rules R-UNI-39, R-WO-48, NFR-028, NFR-072, NFR-074, DL26, DL27, DL01 | Sections 2, 3, 8, 9, 17, 18 |
| Legacy key RWB-E1-041, story RWB-P5-E1041-APP, self-tests TC-E1-041-01 to TC-E1-041-12 | Metadata, sections 3, 12, 16 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Only `rwb_document` tables; the case and the lists consumed through their owners |
| DP-03 | The DOCRET record of an archive and of a listed disposal |
| DP-07 | The four lists through the reference-data contract and its fake |
| DP-10 | The `retention-monthly` Schedule and the scan activity of the intake workflow |
| DP-11 | The case and hold read with one hop, a 2 s timeout and a fake |
| DP-13 | Base `/api/recovery/document/v1` on all eight operations |
| DP-15 | One migration step in `rwb_document` |
| DP-18 | No ledger table and no ledger row; the audit entry stays local |
| DP-19 | SCR-44 and SCR-47 behind gateway-bff |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login (name not specified) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |

### 19. Out of scope

- Disposal or extension of a document at the end of its class by a recorded decision (Epic 2, REQ-DCM-019).
- Applying retention on case closure (FEAT-COM-08, Epic 4).
- Placing or lifting a legal hold: that is `rwb-case`'s operation and this story only reads the flag.
- The retention and personal data screen SCR-47 (Epic 8) and the upload dialog of SCR-30 (RWB-P5-E1026-APP).
- The run resource, its read and its rerun as a REST operation (RWB-P5-E1017-APP); the class panel reads of the SCR-31 and SCR-32 route (RWB-P5-AD021-CON).
- The document store, its containers and the storage product (RWB-P5-E1024-APP), and the OCR, classification and extraction steps after the scan (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP).
- The scanning engine itself, its licences, its capacity and its own console: only the result, the time and the quarantine reference are this service's.
- Retention of the decision record and of the interaction ledger (RWB-E1-014, RWB-E2-034; the ledger is P1's, DP-18).
- The published contract documents of this service, their fakes and their versioning, and the Helm chart, the retry policy values, the topic and DLT provisioning, the metrics, the alerts and the runbook: the contract is RWB-P5-E1041-CON.

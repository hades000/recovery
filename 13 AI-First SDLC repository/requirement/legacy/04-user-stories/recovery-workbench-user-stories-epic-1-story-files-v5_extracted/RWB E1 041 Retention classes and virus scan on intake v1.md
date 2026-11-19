<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 041 Retention classes and virus scan on intake v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 041 Retention classes and virus scan on intake v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-041 Retention classes and virus scan on intake

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-041 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-17 Apply retention classes to stored documents; FEAT-DCM-18 Virus scan every document on intake |
| Requirement IDs | REQ-DCM-010, REQ-DCM-016 |
| BRD section | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence; L2 13.3 Store and retain documents |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-024, RWB-E1-049 |
| Status | Ready for build |

## 1. Story

As a **compliance and PDPA officer (RW-COMPLY)**, I want **every uploaded or scanned file checked for malware before it is stored, and a retention class per document type that the store applies and a monthly job acts on**, so that **the store holds only safe files and keeps each document for the time the policy sets, never removing one silently or while a legal hold is in place**.

## 2. Business rationale

Files reach the bank from branches, partners and email; one infected file in the store reaches every user who opens it. Documents also have no retention rule today, so nothing shows when a document may be archived (FSD P5 A2.17, A2.18). This story scans every file before storage and quarantines a failed file, holds the retention classes as data, and runs JOB-17 to archive documents past their class or list them for the Compliance review. It meets REQ-DCM-010 and REQ-DCM-016 (legal hold overrides retention), with NFR-028, NFR-072 and NFR-074.

## 3. Preconditions

- RWB-E1-024 is done: documents carry retention_class and write_once from the type table.
- RWB-E1-049 is done: document_intake and JOB-12 Document intake exist.
- The quarantine container exists (RWB-TE-012) and the bank malware scanning service is reachable through MalwareScanClient under SY-OCR (assumed: the scanning service of the ACE storage pattern, DL27).
- Retention class table loaded through POST /api/recovery/v1/admin/reference-loads, table RETENTION_CLASS, version RET-2026.11: LEGAL10Y 120 months, end action REVIEW; GENERAL05Y 60 months, end action ARCHIVE (assumed; DL26).
- The P3 published interface CaseDirectory returns legal_hold for a case.
- Feature flags rwb.dochub.malware-scan and rwb.dochub.retention are on.

## 4. Flow

1. JOB-12 Document intake: runs scanStep first, before ocrStep.
2. ScanStep: selects intake items with no scan_result and sends each file to MalwareScanClient.
3. ScanStep: on CLEAN, sets scan_result CLEAN and scanned_at, so ocrStep may read the item; on INFECTED, moves the file to the quarantine container, sets scan_result INFECTED, writes the audit event MALWARE_BLOCKED and alerts the platform administrator; the file is never stored.
4. Upload (RWB-E1-026): calls MalwareScanService.scanNow before DocumentStore.store; INFECTED returns 422 MSG-P5-016; if the scanning service does not answer, the call returns 503 MSG-P5-022 and nothing is kept.
5. DocumentStore (RWB-E1-024): stores clean files with the retention class of the type; legal types go to the write-once container.
6. JOB-17 Retention job: runs on the first Sunday of each month; for each active document computes expiry date = stored date plus period_months of its class.
7. RetentionJob: skips a document whose case has legal_hold true and counts it as held.
8. RetentionJob: for a due document with end action ARCHIVE, writes the decision log entry DOCRET, moves the blob to the archive tier and sets the document state ARCHIVED; for end action REVIEW, adds it to the review list for Compliance and changes nothing.
9. RetentionJob: writes the review list to retention/review/{runDate}.csv in the standard container and the counts (due, archived, listed, held, exceptions) to the job record.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The scan finds malware on an intake file | File quarantined, not stored, audit event, platform administrator alerted | MSG-P5-016 | AC1 |
| X2 | The scanning service does not answer | Intake item stays unscanned and is not read by OCR; retried in the next run; alert after two failed runs; an upload returns 503 and nothing is stored | MSG-P5-022 | AC6 |
| X3 | A due document is on a case with a legal hold | Not archived, not listed; counted as held | None | AC5 |
| X4 | A document carries a class not in the retention table | Listed as an exception RETENTION_CLASS_MISSING; nothing changes | None | AC7 |
| X5 | JOB-17 runs again in the same month | Documents already archived or listed for that month are not acted on again | None | AC8 |
| X6 | A retention class load holds an end action other than ARCHIVE or REVIEW, or a period of 0 months | Load refused in full | MSG-P3-027 | AC9 |
| X7 | The decision log write fails for an archive | The document stays as it is; picked up by the next run; incident raised (R-UNI-39) | MSG-P7-003 | TC-E1-041-12 (Principle 5) |
| X8 | A role without Reference data C loads retention classes | Refused with 403 | MSG-P4-002 | TC-E1-041-11 (Access) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-E1-024) and the intake (RWB-E1-049); the upload (RWB-E1-026) calls this scan |
| Negotiable | Retention periods and end actions are data under DL26; the scanning service is reached through an adapter |
| Valuable | No infected file reaches a user; every document has a retention rule from day one |
| Estimable | One job step, one monthly job, one table, one adapter |
| Small | Fits within one week with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Retention classes and virus scan on intake

  Background:
    Given retention class table version "RET-2026.11" is in force
    Given class "LEGAL10Y" has period 120 months and end action "REVIEW"
    Given class "GENERAL05Y" has period 60 months and end action "ARCHIVE"

  Scenario: AC1 Malware blocked
    Given a test file "eicar-0002.pdf" with the EICAR signature as an intake item from a branch scanner
    When JOB-12 runs the scan step
    Then the item has scan_result "INFECTED" and the file is in the quarantine container
    Then no document row exists for the file and the OCR step does not read it
    Then the system writes the audit event "MALWARE_BLOCKED" with the intake ID and the source, and the platform administrator is alerted

  Scenario: AC2 Retention class
    Given a demand letter of type "DEMAND_LETTER" with class "LEGAL10Y" in the type table
    When the document is stored on case "RW-2026-000123"
    Then the document row carries retention class "LEGAL10Y" and write_once true
    Then the file is in the write-once container

  Scenario: AC3 Expiry with end action archive
    Given an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000123" with no legal hold
    When JOB-17 runs on 6 December 2026
    Then the document has state "ARCHIVED" and its blob is in the archive tier
    Then one decision log entry "DOCRET" names the document, class "GENERAL05Y", version "RET-2026.11" and expiry date 1 November 2026

  Scenario: AC4 Expiry with end action review
    Given a court notice of class "LEGAL10Y" stored on 1 November 2016 on case "RW-2026-000456"
    When JOB-17 runs on 6 December 2026
    Then the system lists the court notice in "retention/review/2026-12-06.csv" with its class and expiry date
    Then the document and its blob are unchanged

  Scenario: AC5 Legal hold overrides the class
    Given an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000789" with legal_hold true
    When JOB-17 runs on 6 December 2026
    Then the system does not archiv the document and not listed
    Then the job record counts it as held

  Scenario: AC6 Scanning service unavailable
    Given the scanning service stub returns no answer
    When JOB-12 runs twice with 3 unscanned intake items
    Then the 3 items have no scan_result and the OCR step reads none of them
    Then the system alerts the platform administrator after the second run
    Then an upload during the outage returns 503 with MSG-P5-022 and no document row or blob is written

  Scenario: AC7 Class not in the retention table
    Given a document with retention class "OLD03Y" that is not in version "RET-2026.11"
    When JOB-17 runs
    Then the system lists the document as exception "RETENTION_CLASS_MISSING" in the review list
    Then the document is unchanged

  Scenario: AC8 Second run in the same month
    Given JOB-17 ran on 6 December 2026 and archived 4 documents and listed 9
    When JOB-17 is rerun on 7 December 2026
    Then the system archives no document again, no second "DOCRET" entry is written and the review list still holds 9 rows

  Scenario: AC9 Invalid retention class load
    Given a load file for table "RETENTION_CLASS" with class "TEMP01M" at period 0 months and end action "DELETE"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P3-027 naming both errors
    Then version "RET-2026.11" stays in force

  Scenario: AC10 Expiry on the run date
    Given an appraisal report of class "GENERAL05Y" stored on 6 December 2021
    When JOB-17 runs on 6 December 2026
    Then the system archives the document , because its expiry date equals the run date
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every file is scanned for malware before it is stored; an infected file is quarantined and never stored | REQ-DCM-010; FEAT-DCM-18 |
| BR2 | Every document carries a retention class from its type | REQ-DCM-010; NFR-028 |
| BR3 | Retention periods and end actions are data owned by Compliance | Retention classes reference table; DL26 |
| BR4 | A legal hold stops archive and expiry for as long as it is in place | REQ-DCM-016; NFR-072; recovery_case.legal_hold |
| BR5 | No document is removed by the retention job; an end action REVIEW lists it for a recorded decision | NFR-074; REQ-DCM-019 (Epic 2) |
| BR6 | A document with a class missing from the table is listed as an exception | R-WO-48 |
| BR7 | An archive that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39 |
| BR8 | A document is due when its expiry date is on or before the run date | Retention classes reference table; JOB-17 |

## 9. State transitions

None. This story does not change a case status. It changes the intake item scan result (none to CLEAN or INFECTED) and the document state (STORED to ARCHIVED for end action ARCHIVE).

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Runs the scan step (Documents CRU) |
| RW-COMPLY, compliance and PDPA officer | Owns the retention classes; reads the review list and the job counts |
| RW-REFADM, reference data administrator | Loads the retention class table (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today; assumed granted to the compliance and PDPA officer as table owner (DL01) |
| RW-PLATADM, platform administrator | Receives scan alerts; reruns JOB-12 and JOB-17 |
| SY-DECLOG, decision log writer | Writes the DOCRET entry |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-006 | document | storage_ref | Read |
| DF-DOC-009 | document | retention_class | Read |
| DF-DOC-010 | document | write_once | Read |
| Standard column | document | state | Write |
| Standard column | document | created_at | Read, as the stored date |
| DF-CAS-020 | recovery_case | legal_hold | Read, through CaseDirectory |
| DF-DOC-058 | document_intake | scan_result | Write |
| DF-DOC-059 | document_intake | scanned_at | Write |
| DF-DOC-057 | document_intake | intake_ref | Write |
| DF-REF-116 to DF-REF-127 | retention_rule | all fields | Write (this story creates the record) |
| DF-DOC-091 to DF-DOC-095 | retention_action | all fields | Write (this story creates the record) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through DecisionLogWriter |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Job: scan step**

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake, step scanStep, first step |
| Job name | JOB-12 Document intake |
| Schedule | Every 15 minutes in business hours |
| Input | Intake items with no scan_result |
| Output | scan_result per item; quarantined files; audit events; alert after two failed runs |
| Events published | None |
| Idempotency key | Intake item ID; an item with a scan_result is not scanned again |
| Restart behavior | Unscanned items are taken by the next run |

**Job: retention**

| Item | Value |
|---|---|
| Trigger | Quartz schedule of JOB-17 |
| Job name | JOB-17 Retention job |
| Schedule | Monthly, first Sunday, Asia/Bangkok |
| Input | Active documents with their class; retention class version in force; legal hold per case |
| Output | Archived documents; review list file; job counts |
| Events published | None |
| Idempotency key | Document ID and the run month; a document acted on in that month is not acted on again |
| Restart behavior | A stopped run resumes from the last committed chunk of 500 documents; rerun from SCR-44 through POST /api/recovery/v1/admin/jobs/{jobId}/rerun |

**POST /api/recovery/v1/admin/reference-loads** (table RETENTION_CLASS)

| Item | Value |
|---|---|
| Request | multipart/form-data: file, table = "RETENTION_CLASS", validFrom |
| Response | 201 ReferenceLoad |
| Errors | 401; 403 (MSG-P4-002); 409 version already loaded (MSG-P3-027); 422 row errors (MSG-P3-027); 503 |
| Authorization | Reference data, right C; approval with right A |
| Idempotency | Table code and table version |

**Published interface (P5, used by RWB-E1-026 and RWB-E1-057)**

```java
public interface MalwareScanService {
    ScanResult scanNow(BlobRef file, Duration timeout);   // CLEAN or INFECTED; throws ScanUnavailableException
}
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/retention` and `recovery/dochub/scan`, Java packages `recovery.dochub.retention` and `recovery.dochub.scan`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| ScanStep | Job | First step of JOB-12; scan, quarantine, audit, alert |
| MalwareScanService, MalwareScanClient | Service | Calls the scanning service; maps results and timeouts |
| QuarantineMover | Service | Moves an infected file from the intake container to the quarantine container |
| RetentionJob | Job | JOB-17; expiry computation, hold check, archive or list |
| RetentionClassLoader | Service | Implements ReferenceTableLoader for RETENTION_CLASS |
| RetentionClassRepository | Repository | Reads and writes retention_class only |
| RetentionReviewWriter | Service | Writes the review list file |

**Database.**
- Flyway migration `V1_5_041__retention_class.sql` creates retention_class (id, class_code varchar(10), period_months integer, end_action varchar(12), table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (class_code, table_version), check period_months > 0 and check end_action in ('ARCHIVE','REVIEW'); adds to document_intake: scanned_at timestamptz, the time of the malware scan (scan_result is created in RWB-E1-049).
- Adds table retention_action (id, document_id, run_month char(7), action varchar(12), decided_entry_id uuid, standard columns) with unique (document_id, run_month) for the idempotency key.
- Index ix_document_retention on document (retention_class, created_at) where is_active.

**Configuration and reference data.**
- Retention classes RET-2026.11, loaded by the reference data administrator and owned by Compliance (DL26).
- Properties rwb.dochub.container.quarantine and rwb.dochub.scan.timeout-seconds = 30.
- Decision code DOCRET, assumed; LOV-DECISION is loaded by the data steward.

**Build steps.**
1. Write the migration; test the constraints and the unique run key.
2. Build MalwareScanClient against a stub that flags the EICAR signature; test AC1 and the upload call.
3. Build ScanStep with quarantine, audit and the two-failure alert; test AC6.
4. Build RetentionClassLoader with validation; test AC9.
5. Build RetentionJob expiry and hold rules; unit test AC5, AC7 and AC10 on fixed dates.
6. Add archive with the decision log entry and the review list; integration test AC3, AC4 and AC8.
7. Test the access and the decision log failure paths.

**Feature flags.** `rwb.dochub.malware-scan` and `rwb.dochub.retention`. With the scan flag off, intake items stay unscanned and are not read; uploads are refused with 503 and MSG-P5-022. With the retention flag off, JOB-17 lists due documents and archives none.

**Done when.** The tests in section 16 pass and the EICAR file is quarantined in SIT on every intake path.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-016 | Malware found | This file was not stored because the malware scan found a threat. It is held in quarantine. |
| MSG-P3-027 | Retention class load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P5-022 | Scanning service unavailable on upload | The malware scan is not available, so the file was not stored. Try again in a few minutes. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

No screen in this story. The compliance and PDPA officer reads the review list file and the JOB-17 counts; SCR-47 Personal data, which shows retention classes, comes in Epic 8. The platform administrator sees scan alerts and job results on SCR-44 Interface and job monitor (states Running; failed; complete). An uploader sees MSG-P5-016 or MSG-P5-022 in the upload dialog of SCR-30.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-041-01 | AC1, BR1 | System | EICAR test file from a branch scanner path |
| TC-E1-041-02 | AC2, BR2 | System | Synthetic demand letter |
| TC-E1-041-03 | AC3, BR3, BR8 | System | Appraisal report stored 1 November 2021, run 6 December 2026 |
| TC-E1-041-04 | AC4, BR5 | System | Court notice stored 1 November 2016 |
| TC-E1-041-05 | AC5, BR4 | System | Case RW-2026-000789 with legal_hold true |
| TC-E1-041-06 | AC6, BR1 | System | Scanning service stub with no answer |
| TC-E1-041-07 | AC7, BR6 | System | Document with class OLD03Y |
| TC-E1-041-08 | AC8 | System | Rerun on 7 December 2026 |
| TC-E1-041-09 | AC9, BR3 | System | Load with period 0 and end action DELETE |
| TC-E1-041-10 | AC10, BR8 | System | Appraisal report stored 6 December 2021 |
| TC-E1-041-11 | Access | Access | Case owner (RW-CASEOWN, Reference data R only) loads RETENTION_CLASS; refused with MSG-P4-002 |
| TC-E1-041-12 | Principle 5 | Resilience | Decision log write forced to fail during an archive; document unchanged, MSG-P7-003 in the job log, incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: periods, end actions and the scan timeout are data or properties.
- No personal data in logs, tests or prompts: audit events carry the intake ID and the source, never the file name or content; test files are synthetic.
- No read of another module's tables: legal hold comes through CaseDirectory.
- The retention job never deletes a blob and never changes a write-once blob's content.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-010 | Every document carries a retention class; intake runs a virus scan before storage | Business Requirements Epic 1, section 3.5 | FEAT-DCM-18, FEAT-DCM-17 | L2 13.3 Store and retain documents | R-WO-48, R-UNI-39 | TC-E1-041-01 to TC-E1-041-04, TC-E1-041-06 to TC-E1-041-12 |
| REQ-DCM-016 | A legal hold stops deletion and expiry, overriding the class | Business Requirements Epic 1, section 3.5 | FEAT-DCM-17 | L2 13.3 Store and retain documents | None | TC-E1-041-05 |

## 19. Out of scope

- Disposal or extension of a document at the end of its class by a recorded decision (Epic 2, REQ-DCM-019).
- Applying retention on case closure (FEAT-COM-08, Epic 4).
- Placing or lifting a legal hold (P3, POST /api/recovery/v1/cases/{caseId}/legal-hold).
- The retention and personal data screen SCR-47 (Epic 8).
- Retention of the decision log and the interaction ledger (RWB-E1-014, RWB-E2-034).

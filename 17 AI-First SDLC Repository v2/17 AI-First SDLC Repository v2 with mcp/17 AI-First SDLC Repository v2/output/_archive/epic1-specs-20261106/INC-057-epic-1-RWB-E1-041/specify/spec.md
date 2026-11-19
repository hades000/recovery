# Technical Specification — RWB-E1-041 Retention classes and virus scan on intake

| Field | Value |
|---|---|
| Story | RWB-E1-041 — Retention classes and virus scan on intake |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-057-epic-1-RWB-E1-041` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-015); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 041 Retention classes and virus scan on intake v1.md`; FSD P5 A2.17, A2.18; TSD P5 T3.1 |
| Upstream IDs | BRD-RWB-005; FR-RWB-015; REQ-DCM-010, REQ-DCM-016; US-RWB-E1-041; CTX-FEATURE-005; CTL-12; NFR-028, NFR-072, NFR-074; DL01, DL11, DL26, DL27 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Compliance and PDPA officer (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The compliance officer reads the review list file and JOB-17 counts; SCR-47 and SCR-44 belong to Epic 8 and Epic 2/E8. |
| Logic In Scope | `YES` — malware scan step, quarantine, scan-unavailable handling, retention class load, expiry calculation, legal hold, archive, review list and idempotency. |
| API In Scope | `NO` — no new or changed endpoint. The story adds the table code `RETENTION_CLASS` to the existing P4 reference-load endpoint and two Quartz jobs. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-12 Document intake (`scanStep` first); `document_intake` (RWB-E1-049); `document` (RWB-E1-024); `recovery_case.legal_hold` through `CaseDirectory`; `retention_class` and `retention_action` (new tables); quarantine container (RWB-TE-012). |
| New Nodes Required | `YES` — `ScanStep`, `MalwareScanService`, `MalwareScanClient`, `QuarantineMover`, `RetentionJob`, `RetentionClassLoader`, `RetentionClassRepository`, `RetentionReviewWriter`. |
| Inherited Existing Behavior | Document store (RWB-E1-024); intake and OCR (RWB-E1-049); containers and managed identity (RWB-TE-012); decision log writer (RWB-E1-027); reference data load (P4); case legal hold (P3). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every file is scanned for malware before it is stored; an infected file is quarantined and never stored. | SPEC-RWB-E1-041-001, SPEC-RWB-E1-041-004, SPEC-RWB-E1-041-005 | DIRECT | `ScanStep` runs first; upload scans synchronously. | COVERED |
| BR2 | Every document carries a retention class from its type. | SPEC-RWB-E1-041-008 | DIRECT | `document.retention_class` copied from the type table by RWB-E1-024. | COVERED |
| BR3 | Retention periods and end actions are data owned by Compliance. | SPEC-RWB-E1-041-007 | DIRECT | `retention_class` table, `RET-2026.11` (assumed; DL26). | COVERED |
| BR4 | A legal hold stops archive and expiry for as long as it is in place. | SPEC-RWB-E1-041-010 | DIRECT | `CaseDirectory.legalHold(caseId)`; counted as held. | COVERED |
| BR5 | No document is removed by the retention job; an end action REVIEW lists it for a recorded decision. | SPEC-RWB-E1-041-012 | DIRECT | Review list CSV; no state or blob change. | COVERED |
| BR6 | A document with a class missing from the table is listed as an exception. | SPEC-RWB-E1-041-013 | DIRECT | `RETENTION_CLASS_MISSING`. | COVERED |
| BR7 | An archive that cannot be written to the decision log does not proceed. | SPEC-RWB-E1-041-011 | DIRECT | `DOCRET` log write before the state change. | COVERED |
| BR8 | A document is due when its expiry date is on or before the run date. | SPEC-RWB-E1-041-009 | DIRECT | `created_at::date + period_months <= runDate`. | COVERED |
| AC1 | An EICAR intake item is `INFECTED`; the file is in quarantine; no document row; OCR does not read it; `MALWARE_BLOCKED` and an alert. | SPEC-RWB-E1-041-004 | DIRECT | Scan step; quarantine; audit. | COVERED |
| AC2 | A demand letter carries `LEGAL10Y` and write-once true; the file is in the write-once container. | SPEC-RWB-E1-041-008 | DIRECT | Type lookup; store container. | COVERED |
| AC3 | An appraisal report stored 1 November 2021, class `GENERAL05Y`, is `ARCHIVED` on 6 December 2026 with a `DOCRET` entry naming class, version and expiry 1 November 2026. | SPEC-RWB-E1-041-009, SPEC-RWB-E1-041-011 | DIRECT | 60 months; run date after expiry. | COVERED |
| AC4 | A court notice stored 1 November 2016, class `LEGAL10Y`, is listed in `retention/review/2026-12-06.csv`; document and blob unchanged. | SPEC-RWB-E1-041-012 | DIRECT | REVIEW end action. | COVERED |
| AC5 | A held appraisal report is neither archived nor listed; the job counts it as held. | SPEC-RWB-E1-041-010 | DIRECT | Hold check before action. | COVERED |
| AC6 | Scanning service unavailable for two runs leaves items unscanned, OCR reads none, alert on the second run; upload returns 503 MSG-P5-022 and writes nothing. | SPEC-RWB-E1-041-006 | DIRECT | Retry and alert; synchronous upload refusal. | COVERED |
| AC7 | A document with class `OLD03Y` is listed as exception `RETENTION_CLASS_MISSING`; unchanged. | SPEC-RWB-E1-041-013 | DIRECT | Missing class branch. | COVERED |
| AC8 | A rerun in the same month archives no document again, writes no second `DOCRET`, and the review list still holds 9 rows. | SPEC-RWB-E1-041-014 | DIRECT | Unique (`document_id`, `run_month`). | COVERED |
| AC9 | A load with period 0 and end action `DELETE` is refused whole naming both errors; `RET-2026.11` stays. | SPEC-RWB-E1-041-007 | DIRECT | Check constraints and loader validation. | COVERED |
| AC10 | A document whose expiry equals the run date is archived. | SPEC-RWB-E1-041-009 | DIRECT | `<=` boundary. | COVERED |
| X1 | Malware found on an intake file. | SPEC-RWB-E1-041-004 | DIRECT | Quarantine; MSG-P5-016; alert. | COVERED |
| X2 | Scanning service does not answer. | SPEC-RWB-E1-041-006 | DIRECT | Unscanned; retry; 503 on upload. | COVERED |
| X3 | Due document on a case with legal hold. | SPEC-RWB-E1-041-010 | DIRECT | Held; no action. | COVERED |
| X4 | Class not in the retention table. | SPEC-RWB-E1-041-013 | DIRECT | Exception row. | COVERED |
| X5 | JOB-17 runs twice in the same month. | SPEC-RWB-E1-041-014 | DIRECT | Idempotent by document and month. | COVERED |
| X6 | Invalid end action or zero period. | SPEC-RWB-E1-041-007 | DIRECT | Load refused whole. | COVERED |
| X7 | Decision log write fails for an archive. | SPEC-RWB-E1-041-011 | DIRECT | Document unchanged; next run; incident. | COVERED |
| X8 | Role without Reference data C loads retention classes. | SPEC-RWB-E1-041-017 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **compliance and PDPA officer (RW-COMPLY)**, I want **every uploaded or scanned file checked for malware before it is stored, and a retention class per document type that the store applies and a monthly job acts on**, so that **the store holds only safe files and keeps each document for the time the policy sets, never removing one silently or while a legal hold is in place**.

The story adds the first step of JOB-12 (scan) and the monthly JOB-17 (retention). It holds the retention classes as data owned by Compliance, computes expiry from the stored date, honours a case legal hold, archives only when the class says ARCHIVE, and lists REVIEW cases for a person. It never deletes a blob. It adds no screen and no endpoint.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-12 Document intake every 15 minutes (scan step first); JOB-17 Retention job on the first Sunday of each month, Asia/Bangkok; an upload calls the scan synchronously. |
| Preconditions | RWB-E1-024 done; RWB-E1-049 done; quarantine container exists (RWB-TE-012); malware scanning service reachable through `MalwareScanClient` under SY-OCR (assumed; DL27); `RETENTION_CLASS` version `RET-2026.11` loaded (assumed; DL26); `CaseDirectory` returns `legal_hold`; `rwb.dochub.malware-scan` and `rwb.dochub.retention` flags on. |
| Input | Intake items with no `scan_result`; active documents with class and `created_at`; retention class version in force; case legal hold. |
| Output | `scan_result` and `scanned_at`; quarantined files; audit `MALWARE_BLOCKED`; archived documents; review CSV; job counts; `DOCRET` entries. |
| Feature flags | `rwb.dochub.malware-scan`: off means items stay unscanned and uploads are refused with 503 MSG-P5-022. `rwb.dochub.retention`: off means JOB-17 lists due documents and archives none. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_intake` | `scan_result` | Scan step | System writes | `CLEAN` or `INFECTED`; null before the scan |
| `document_intake` | `scanned_at` | Scan step | System writes | Set when a result is recorded |
| `document_intake` | `intake_ref` | Scan step | System writes | Updated when the file moves to quarantine |
| `document` | `retention_class` | Type table (RWB-E1-024) | Read-only | Must exist in the retention class version in force |
| `document` | `state` | Store | System writes | `STORED` to `ARCHIVED` only |
| `document` | `created_at` | Store | Read-only | The stored date used for expiry |
| `retention_class` | `class_code` | Load file | New version only | Unique within the version; `LEGAL10Y`, `GENERAL05Y` (assumed; DL26) |
| `retention_class` | `period_months` | Load file | New version only | Greater than 0 |
| `retention_class` | `end_action` | Load file | New version only | `ARCHIVE` or `REVIEW` |
| `retention_action` | `document_id`, `run_month`, `action` | JOB-17 | System writes | Unique (`document_id`, `run_month`); action `ARCHIVED`, `LISTED`, `HELD`, `EXCEPTION` |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Scan step | Service returns CLEAN | `scan_result=CLEAN` | `scanned_at`; OCR may read |
| None | Scan step | Service returns INFECTED | `scan_result=INFECTED` | File quarantined; `MALWARE_BLOCKED`; alert; OCR skips |
| None | Scan step | Service unavailable | No `scan_result` | Item retried next run; alert after two failed runs |
| `STORED` | JOB-17 | Due, no hold, class `GENERAL05Y` | `ARCHIVED` | Blob archive tier; `DOCRET`; `retention_action` |
| `STORED` | JOB-17 | Due, no hold, class `LEGAL10Y` | `STORED` | Listed in review CSV; `retention_action` LISTED |
| `STORED` | JOB-17 | Case `legal_hold=true` | `STORED` | Counted held; no action |
| `STORED` | JOB-17 | Class missing | `STORED` | Exception `RETENTION_CLASS_MISSING` |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Malware found | Quarantine; no document row; OCR skips; audit and alert | MSG-P5-016; `MALWARE_BLOCKED` |
| X2 | Scanning service unavailable | Item unscanned; retried; alert after two runs; upload 503 and nothing stored | MSG-P5-022 |
| X3 | Legal hold on the case | Not archived, not listed; counted held | None |
| X4 | Class not in the table | Listed as exception; unchanged | `RETENTION_CLASS_MISSING` |
| X5 | Same-month rerun | No second archive, `DOCRET` or review row | None |
| X6 | Invalid class load | Refused whole; version unchanged | MSG-P3-027 |
| X7 | Decision log write fails for an archive | Document unchanged; next run picks it up; incident | MSG-P7-003 |
| X8 | Role without Reference data C | 403; nothing loaded | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/reference-loads` (P4; table `RETENTION_CLASS`); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (P1) for JOB-12 and JOB-17. |
| Contract delta | None. The table code is a request value; the rerun endpoint already accepts a job ID. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load and A to approve; Platform administration U to rerun. 401, 403 MSG-P4-002, 409 MSG-P3-027, 422 MSG-P3-027, 503 MSG-GEN-006. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label changes; SCR-47 and SCR-44 are other releases. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-010, REQ-DCM-016; SPEC-RWB-E1-041-001..018 | New scan step, adapter, quarantine mover, retention job, loader and repositories. | Scan CLEAN/INFECTED/unavailable; quarantine move; upload refusal; class load invalid; expiry boundary; hold; archive and review; missing class; same-month rerun; decision log failure; access refusal. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ScanStep` | Job | First step of JOB-12; scan, quarantine, audit and alert. |
| `MalwareScanService`, `MalwareScanClient` | Service | Calls the scanning service; maps results and timeouts. |
| `QuarantineMover` | Service | Moves an infected file from the intake container to quarantine. |
| `RetentionJob` | Job | JOB-17; expiry, hold check, archive or list. |
| `RetentionClassLoader` | Service | Implements `ReferenceTableLoader` for `RETENTION_CLASS`. |
| `RetentionClassRepository` | Repository | Reads and writes `retention_class` only. |
| `RetentionReviewWriter` | Service | Writes `retention/review/{runDate}.csv`. |

### Package and boundaries

Folders `recovery/dochub/retention` and `recovery/dochub/scan`, Java packages
`recovery.dochub.retention` and `recovery.dochub.scan`. Legal hold and case status are read through
`CaseDirectory`; the decision log is written through `DecisionLogWriter`; the quarantine container is
reached through `DocumentStorage`/`DocumentContainers`. No module table is read directly.

### Data and migration

Flyway `V1_5_041__retention_class.sql` creates `retention_class` (`id`, `class_code varchar(10)`,
`period_months integer`, `end_action varchar(12)`, `table_version varchar(20)`, `valid_from`, `valid_to`,
`load_id`, standard columns) with unique (`class_code`, `table_version`), check `period_months > 0` and
check `end_action in ('ARCHIVE','REVIEW')`; adds `document_intake.scanned_at timestamptz` (`scan_result`
is created by RWB-E1-049); creates `retention_action` (`id`, `document_id`, `run_month char(7)`,
`action varchar(12)`, `decision_log_id uuid`, standard columns) with unique (`document_id`,
`run_month`); creates index `ix_document_retention` on `document (retention_class, created_at)` where
`is_active`. The story data table names the same table `retention_rule` (DF-REF-116..127); the solution
plan and this spec use `retention_class` as the physical name.

### Scan flow

1. JOB-12 runs `scanStep` before `ocrStep`.
2. Select intake items with no `scan_result`.
3. Send each file to `MalwareScanClient` with the 30-second timeout.
4. CLEAN: set `scan_result='CLEAN'` and `scanned_at`; OCR may read the item.
5. INFECTED: move the file to `rwb-quarantine`; set `scan_result='INFECTED'` and `scanned_at`; write
   `MALWARE_BLOCKED` with the intake ID and source; alert the platform administrator; no document row.
6. Unavailable: leave `scan_result` null; retry next run; alert after two failed runs.
7. An upload calls `MalwareScanService.scanNow` before `DocumentStore.store`; INFECTED returns 422
   MSG-P5-016; unavailable returns 503 MSG-P5-022 and nothing is kept.

### Retention flow

1. JOB-17 runs on the first Sunday of each month.
2. For each active document, resolve its class in the version in force and compute
   `expiry = created_at::date + period_months`.
3. Skip and count a document whose case has `legal_hold=true`.
4. Due when `expiry <= runDate`.
5. `ARCHIVE`: write the `DOCRET` decision log entry naming document, class, version and expiry; set the
   blob to the archive access tier; set `document.state='ARCHIVED'`; write `retention_action` ARCHIVED.
6. `REVIEW`: add the document to `retention/review/{runDate}.csv` with class and expiry; change nothing;
   write `retention_action` LISTED.
7. Missing class: write `retention_action` EXCEPTION `RETENTION_CLASS_MISSING`; change nothing.
8. Write counts (due, archived, listed, held, exceptions) to the job record.

### Retention class load

`RetentionClassLoader` validates the whole file before staging: `class_code` unique within the version,
`period_months` greater than 0, `end_action` one of `ARCHIVE` or `REVIEW`, and a valid-from date. Any
invalid row refuses the load whole with MSG-P3-027 naming every bad row; the version in force is
unchanged. The table also carries check constraints for the same rules.

### Idempotency and restart

- `retention_action` unique (`document_id`, `run_month`) is the idempotency key. A second run in the same
  month sees the row and does not act again; the review CSV keeps its rows.
- A stopped run resumes from the last committed chunk of 500 documents; a rerun from SCR-44 uses
  `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`.

### Transaction and events

Each document is one transaction: decision log, state, blob tier and `retention_action` commit together.
A failed decision log write rolls back and leaves the document unchanged. No domain event is published.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-OCR OCR and extraction pipeline | Documents CRU; runs the scan step | All |
| RW-COMPLY Compliance and PDPA officer | Owns the classes; reads the review list and counts | All |
| RW-REFADM Reference data administrator | Reference data C; loads the class table | All |
| Approver with Reference data A | Approves the load; assumed granted to the compliance officer as table owner (DL01) | All |
| RW-PLATADM Platform administrator | Receives scan alerts; reruns JOB-12 and JOB-17 | All |
| SY-DECLOG | Writes the `DOCRET` entry | All |

### Observability and operations

- Job records for JOB-12 scan and JOB-17 retention with counts and duration.
- Metrics: files scanned, infected, quarantined, scan failures; documents due, archived, listed, held,
  exceptions.
- Alerts: malware found; scanning service failed twice; JOB-17 failed; decision log failure; class
  missing for an active document.
- Logs carry intake ID, document ID and counts; never file names or content.

### Performance

- Scan: one call per item; 30-second timeout; items processed in the existing JOB-12 worker model.
- Retention: chunks of 500 documents; `ix_document_retention` supports the due scan.
- The review CSV is written once per run; archive tier changes are per blob.

### Feature flags and rollback

- `rwb.dochub.malware-scan`: off means items stay unscanned and uploads are refused with 503.
- `rwb.dochub.retention`: off means JOB-17 lists due documents and archives none.
- Rollback: turn the flags off; redeploy the previous tag. The migration is forward-only and additive.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-041-01 | AC1, BR1 | System | EICAR file from a branch scanner | `INFECTED`; quarantined; no row; `MALWARE_BLOCKED`; alert |
| TC-E1-041-02 | AC2, BR2 | System | Synthetic demand letter | `LEGAL10Y`; write-once; legal container |
| TC-E1-041-03 | AC3, BR3, BR8 | System | Appraisal report stored 1 Nov 2021; run 6 Dec 2026 | `ARCHIVED`; archive tier; `DOCRET` expiry 1 Nov 2026 |
| TC-E1-041-04 | AC4, BR5 | System | Court notice stored 1 Nov 2016 | Listed in `retention/review/2026-12-06.csv`; unchanged |
| TC-E1-041-05 | AC5, BR4 | System | Case `RW-2026-000789` with `legal_hold=true` | Not archived or listed; counted held |
| TC-E1-041-06 | AC6, BR1 | System | Scan stub returns no answer twice | No `scan_result`; OCR skips; alert; upload 503 MSG-P5-022 |
| TC-E1-041-07 | AC7, BR6 | System | Document with class `OLD03Y` | Exception `RETENTION_CLASS_MISSING`; unchanged |
| TC-E1-041-08 | AC8 | System | Rerun on 7 Dec 2026 | No second archive or `DOCRET`; 9 review rows |
| TC-E1-041-09 | AC9, BR3 | System | Load with period 0 and end action `DELETE` | Refused whole; both errors; `RET-2026.11` stays |
| TC-E1-041-10 | AC10, BR8 | System | Appraisal report stored 6 Dec 2021; run 6 Dec 2026 | Archived; expiry equals run date |
| TC-E1-041-11 | X8 | Security | RW-CASEOWN loads `RETENTION_CLASS` | 403 MSG-P4-002 |
| TC-E1-041-12 | X7 | Resilience | Decision log write forced to fail during archive | Document unchanged; MSG-P7-003 in the job log; incident |
| TC-E1-041-U1 | BR3, BR4, BR8, AC5, AC10 | Unit | Expiry on the run date; hold true; class with period 0; missing class | Archived on equality; held skipped; load refused; exception row |

## Guardrails

- No business value in code: periods, end actions and the scan timeout are data or properties.
- No personal data in logs, tests or prompts: audit events carry the intake ID and the source, never the
  file name or content; test files are synthetic.
- No read of another module's tables: legal hold comes through `CaseDirectory`.
- The retention job never deletes a blob and never changes a write-once blob's content.

## Out of scope

- Disposal or extension of a document at the end of its class by a recorded decision (Epic 2,
  REQ-DCM-019).
- Applying retention on case closure (FEAT-COM-08, Epic 4).
- Placing or lifting a legal hold (P3, `POST /api/recovery/v1/cases/{caseId}/legal-hold`).
- The retention and personal data screen SCR-47 (Epic 8).
- Retention of the decision log and the interaction ledger (RWB-E1-014, RWB-E2-034).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-010 | Every document carries a retention class; intake runs a virus scan before storage | Business Requirements Epic 1, section 3.5 | FEAT-DCM-18, FEAT-DCM-17 | L2 13.3 Store and retain documents | R-WO-48, R-UNI-39 | TC-E1-041-01..04, 06..12 |
| REQ-DCM-016 | A legal hold stops deletion and expiry, overriding the class | Business Requirements Epic 1, section 3.5 | FEAT-DCM-17 | L2 13.3 Store and retain documents | None | TC-E1-041-05 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3; SPEC-007 | Are the retention periods final? | Expiry dates. | `RET-2026.11`: `LEGAL10Y` 120 months with REVIEW, `GENERAL05Y` 60 months with ARCHIVE (assumed; DL26). They are data owned by Compliance. | RESOLVED | SPEC-007 |
| CLAR-002 | BR1; SPEC-002 | Which malware scanning service is used? | Adapter target. | The scanning service of the ACE storage pattern, reached through `MalwareScanClient` under SY-OCR (assumed; DL27). | RESOLVED | SPEC-002 |
| CLAR-003 | AC3; SPEC-011 | What does "moves the blob to the archive tier" mean? | Storage operation. | Set the blob's access tier to Archive and keep its path and `storage_ref`; no copy to another container. | RESOLVED | SPEC-011 |
| CLAR-004 | AC4; SPEC-012 | Does the REVIEW action change the document? | State and blob. | No. It lists the document with class and expiry and changes nothing; a person decides later (BR5). | RESOLVED | SPEC-012 |
| CLAR-005 | BR4; SPEC-010 | Where is legal hold read from? | Hold check. | Case-level `recovery_case.legal_hold` through `CaseDirectory`; the story does not add a document-level hold. | RESOLVED | SPEC-010 |
| CLAR-006 | AC4; SPEC-012 | Which columns does the review CSV hold? | Reviewer usability. | Document ID, case ID, class code, expiry date and reason; the story requires class and expiry, the other columns identify the document. Implementation decision. | RESOLVED | SPEC-012 |
| CLAR-007 | Authority; SPEC-017 | Who approves a retention class load? | Separation of duty. | No role holds Reference data A today; assumed granted to the compliance and PDPA officer as table owner (DL01). | RESOLVED | SPEC-017 |
| CLAR-008 | AC6; SPEC-002 | Is the scan timeout 30 seconds? | Failure timing. | Yes; property `rwb.dochub.scan.timeout-seconds = 30` (story §13). | RESOLVED | SPEC-002 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the named decision log
entries or the ACE storage pattern. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this batch story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New malware scan step, quarantine, retention classes and monthly retention job; no screen and no contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: two batch jobs and a reference table with no endpoint delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 10 acceptance criteria, 8 exception paths and 7 scan/retention states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

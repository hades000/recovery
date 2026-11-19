# Technical Specification — RWB-E1-051 Legacy feed jobs on ADF and Control-M

| Field | Value |
|---|---|
| Story | RWB-E1-051 — Legacy feed jobs on ADF and Control-M |
| Epic / module | E1 / P2 Integration |
| RUN_ID | `INC-017-epic-1-RWB-E1-051` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 051 Legacy feed jobs on ADF and Control M v1.md`; REQ-DRI-008, REQ-RDF-002..004; BRD Epic 1 §3.2; BRD Program §5.1, §5.2 |
| Upstream IDs | REQ-DRI-008; REQ-RDF-002..004; FEAT-RDF-22; INT-01, 07, 10, 11; ADR-005; DL11; DL12 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Data steward and data product owner; platform administrator; see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Run rows are read through `GET /admin/jobs` and the Log Analytics workbook; SCR-44 is Epic 2. |
| Logic In Scope | `YES` — four feed schedules, JOB-01 retry window, run recording, failure alerts, duplicate handling and layout contract tests. |
| API In Scope | `NO` — no endpoint or schema change. The story reuses `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun` (P1, E1). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-01 COLLINS intake (new); JOB-09 file loads (RWB-E1-007); `interface_run` and `interface_config` (RWB-E1-007); P1 loaders; Log Analytics; Control-M and ADF. |
| New Nodes Required | `YES` — `FeedRunRecorder`; `LayoutContractImpl`; `FeedContractTest`; `CollinsIntakeJob`; Control-M and ADF definitions; `JobFailureAlert`. |
| Inherited Existing Behavior | File adapters and `interface_run` (RWB-E1-007); P1 loaders and data-product status (RWB-E1-003/004/009/015); ACE scheduler; reference data (RWB-E1-043); run books (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | ALS and EFS data arrive only through the COLLINS daily batch; CCMS and SVAF only through file loads. | SPEC-RWB-E1-051-001..003 | DIRECT | Control-M extracts to COLLINS; ADF moves files to SFTP; no direct call. | COVERED |
| BR2 | JOB-01 starts at 05:00 and retries hourly to 09:00; after that the previous load stays and products are stale. | SPEC-RWB-E1-051-004, SPEC-RWB-E1-051-011 | DIRECT | Five attempts; MISSING after 09:00. | COVERED |
| BR3 | JOB-09 runs CCMS and SVAF weekly on Monday 04:00. | SPEC-RWB-E1-051-005 | DIRECT | Quartz cron from `rwb.jobs.files.weekly-cron`. | COVERED |
| BR4 | Each run writes a run record and a failure alerts the data steward and the platform administrator. | SPEC-RWB-E1-051-006, SPEC-RWB-E1-051-007 | DIRECT | `FeedRunRecorder`; `rwb.integration.job.failed`; MSG-P2-004. | COVERED |
| BR5 | A changed source field fails the contract test and names the field. | SPEC-RWB-E1-051-008, SPEC-RWB-E1-051-009 | DIRECT | Layout files under `contracts/`; `LayoutContract`. | COVERED |
| BR6 | A repeat load for the same business date is not loaded twice. | SPEC-RWB-E1-051-010 | DIRECT | `interface_id + business_date`; run DUPLICATE. | COVERED |
| AC1 | Four jobs scheduled: JOB-01 writes INT-01/INT-07 LOADED from 05:00; JOB-09 writes INT-10/INT-11 LOADED from 04:00; each row has date, count, start and end. | SPEC-RWB-E1-051-001..006 | DIRECT | SIT business date 2026-11-15; Monday 2026-11-16. | COVERED |
| AC4 | ADF CCMS fails Sunday 2026-11-22; JOB-09 on 2026-11-23 shows INT-10 MISSING; data steward and platform administrator receive MSG-P2-004 within 15 minutes. | SPEC-RWB-E1-051-007, SPEC-RWB-E1-051-011 | DIRECT | Failure event and alert rule. | COVERED |
| AC5 | No COLLINS load by 09:00 on 2026-11-24: INT-01/INT-07 MISSING; account/arrears product shows MSG-P1-001 with 2026-11-23. | SPEC-RWB-E1-051-004, SPEC-RWB-E1-051-011 | DIRECT | Retry 06:00–09:00; stale marker. | COVERED |
| AC6 | EFS load LOADED at 05:10; a second run at 05:40 writes DUPLICATE and loads nothing. | SPEC-RWB-E1-051-010 | DIRECT | Idempotency key interface + date. | COVERED |
| X1 | A Control-M or ADF job fails. | SPEC-RWB-E1-051-007 | DIRECT | Scheduler alerts; Workbench run MISSING; MSG-P2-004. | COVERED |
| X2 | COLLINS load not arrived by 09:00. | SPEC-RWB-E1-051-004, SPEC-RWB-E1-051-011 | DIRECT | Stop retrying; stale; MSG-P1-001. | COVERED |
| X3 | A source field changes name, type or length. | SPEC-RWB-E1-051-009 | DIRECT | Contract test fails; merge blocked; MSG-P2-002. | COVERED |
| X4 | A scheduler starts the same feed twice for one date. | SPEC-RWB-E1-051-010 | DIRECT | DUPLICATE; nothing loaded. | COVERED |
| X5 | A role without the right reruns a feed job. | SPEC-RWB-E1-051-013 | DIRECT | 403; MSG-P4-002. | COVERED |
> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story.

## User story intent interpretation
As a **data steward and data product owner (RW-DATASTEW)**, I want **the ALS, EFS, CCMS and SVAF feed jobs scheduled on Control-M and ADF, each writing a run record and alerting on failure**, so that **the squad loads run every day or week without a manual step**.

The story puts the four feeds on the bank schedulers, records every run in the Workbench, and tests each file layout in the pipeline. The Workbench never calls ALS, EFS, CCMS or SVAF; the bank scheduler delivers to COLLINS and to the inbound folder. The story adds no screen; the platform administrator and data steward read run rows through the existing admin endpoint and the Log Analytics workbook.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Control-M ALS/EFS extracts after COLLINS end of day; ADF CCMS/SVAF moves by Sunday 23:00; JOB-01 daily 05:00 with hourly retries to 09:00; JOB-09 Monday 04:00. |
| Preconditions | RWB-E1-001 and RWB-E1-007 done; SCB IT grants Control-M folder and ADF factory access in DEV/SIT; `interface_config` for INT-01/07/10/11 version `IF-2026.11`; layout files in `contracts/`; synthetic samples in `src/test/resources/contracts/`. |
| Input | COLLINS load for INT-01/INT-07; CCMS and SVAF files; layout files; scheduler definitions. |
| Output | `interface_run` rows; `rwb.integration.job.failed` event; alert; contract-test result; run book entries. |
| Feature flag | `rwb.integration.legacy-feeds`. Off: JOB-01 and JOB-09 do not run; no run row is written; existing data stays. |
## Field-level behaviour matrix
| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `interface_config` | `interface_id`, `inbound_path`, `file_pattern`, `data_product`, `alert_role` | Reference data | Read-only | Version in force |
| `interface_run` | `interface_id`, `business_date`, `status`, `record_count`, `started_at`, `ended_at`, `checks` | `FeedRunRecorder` | System writes | Status LOADED, MISSING, FAILED, REFUSED, DUPLICATE |
| `loan_account` | `data_as_of` | P1 load | Read-only | Used to show the stale date |
| Layout file | `field`, `type`, `length`, `mandatory`, `position` | `contracts/` | Editable by pull request | One per interface; versioned with the code |
| Control-M / ADF definition | `job_name`, `schedule`, `source`, `target`, `retry` | `ops/control-m/`, `ops/adf/` | Editable by platform administrator | Names proposed until DL12 |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| — | JOB-01 starts | COLLINS load present | `LOADED` | Run row for INT-01 and INT-07 with counts and times |
| — | JOB-01 attempt | Load absent, before 09:00 | Retry | Next hourly attempt; no run row yet |
| — | JOB-01 last attempt | Load absent at 09:00 | `MISSING` | Previous load stays; products stale; MSG-P1-001 |
| — | JOB-09 runs | File present, checks pass | `LOADED` | Run row; records to P1 |
| — | JOB-09 runs | File absent | `MISSING` | Stale next business day; MSG-P2-004 |
| — | JOB-09 runs | Same interface and date already loaded | `DUPLICATE` | Nothing loaded |
| — | JOB-09 runs | A check fails | `REFUSED` | Previous load stays; stale; MSG-P1-002 |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Control-M/ADF job fails | Bank scheduler alerts; Workbench run MISSING | MSG-P2-004 |
| X2 | COLLINS load absent at 09:00 | Stop retrying; products stale; previous load stays | MSG-P1-001 |
| X3 | Source field changes | Contract test fails naming the field; merge blocked | MSG-P2-002 |
| X4 | Same feed started twice | DUPLICATE run; nothing loaded | None |
| X5 | Role without Platform administration U reruns | 403; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` (Platform administration R); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (Platform administration U). Both are P1, first in E1. |
| Contract delta | None. The story reads and reruns jobs through the existing operations. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R/U; 403 MSG-P4-002. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P2-006 (job running); 503. |
| Versioning | No version change. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; run rows are read through an existing endpoint and workbook. | Existing front-end tests stay green; no new front-end test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR6; SPEC-RWB-E1-051-001..018 | New `CollinsIntakeJob`, `FeedRunRecorder`, `LayoutContractImpl` and contract tests. | Unit tests cover the retry window, MISSING after 09:00, each layout check, duplicate detection, run-row fields and alert payload. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `FeedRunRecorder` | Service | Writes the `interface_run` row at start and end; writes the failure event. |
| `LayoutContractImpl` | Service | Reads a layout file (field, type, length, mandatory) and checks a sample file. |
| `FeedContractTest` | Test | One parameterized test per interface: INT-01, INT-07, INT-10, INT-11. |
| `CollinsIntakeJob` | Job | JOB-01; hourly retry from 05:00 to 09:00; writes MISSING after the last attempt. |
| `FileLoadJob` | Job | JOB-09; reuses RWB-E1-007. |
| `JobFailureAlert` | Rule table | Log Analytics alert on `rwb.integration.job.failed`; email to `alert_role` and RW-PLATADM. |

### Scheduler definitions
Control-M jobs `RWB_ALS_EXTRACT` and `RWB_EFS_EXTRACT`; ADF pipelines `rwb-ccms-file-move` and `rwb-svaf-file-move`; JSON in `ops/control-m/` and `ops/adf/`, validated and deployed by the pipeline. Names are proposed until SCB IT issues the bank standard (DL12). The ADF move lands the file in the Workbench SFTP inbound folder by Sunday 23:00 (assumed; DL12).

### Data and migration
No migration. Reads and writes `interface_run` and reads `interface_config`, both created by RWB-E1-007. Reads `loan_account.data_as_of` through the P1 published interface for the stale date. No new table.

### Rules
1. JOB-01 runs at `rwb.jobs.collins.start` (05:00) and retries hourly to `rwb.jobs.collins.last-retry` (09:00). Each attempt checks for the COLLINS load for the business date.
2. After the 09:00 attempt without a load, write `MISSING` for INT-01 and INT-07; keep the previous load; mark the products stale with the previous business date.
3. JOB-09 runs on `rwb.jobs.files.weekly-cron` (Monday 04:00) for INT-10 and INT-11; it uses the RWB-E1-007 adapter and checks.
4. Every run writes interface, business date, status, record count, start and end.
5. A failure writes `rwb.integration.job.failed` with job, interface, business date and time; the alert rule emails the data steward and platform administrator with MSG-P2-004.
6. The layout contract test compares each sample file with its layout and names the first field that differs (MSG-P2-002).
7. A repeat run for an already-LOADED key writes `DUPLICATE` and loads nothing.

### Transaction and events
One run row per interface and attempt outcome. P1 publishes `LoadCompleted` (EV-26) or `LoadRefused` (EV-27); P2 publishes no event of its own. A failed run writes the alert event in the same transaction as the run row. The rerun is idempotent by interface and business date.

### Security and authority
| Actor | Right | Scope |
|---|---|---|
| RW-PLATADM | Platform administration U; maintains Control-M/ADF definitions; reruns | All |
| RW-DATASTEW | Platform administration R; receives alerts | All |
| SY-DATALOAD | Runs JOB-01/JOB-09; writes run rows | All |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-SECADM | Platform administration R | All |

No direct call from the Workbench to ALS, EFS, CCMS or SVAF. The scheduler delivers to COLLINS and to the inbound folder.

### Observability and operations
- Log Analytics workbook "Recovery jobs": last run, status, duration, record count per interface.
- Alert rules: `rwb.integration.job.failed`; file missing; load late.
- Run book: JOB-01 and JOB-09 with six sections; restart steps name `RWB_ALS_EXTRACT`, `RWB_EFS_EXTRACT`, `rwb-ccms-file-move`, `rwb-svaf-file-move`.
- Metrics: run status count, record count, duration, missing files.

### Performance
- JOB-01 completes its intake after COLLINS; NFR-013 target: COLLINS load complete by 07:00.
- JOB-09 reads the weekly files after the ADF move; no numeric throughput target is stated (DL11).
- Contract tests run on every merge and parse the synthetic samples only.

### Feature flag and rollback
`rwb.integration.legacy-feeds`. Off: JOB-01/JOB-09 do not run; the scheduler definitions remain but no Workbench run row is written. Rollback: turn the flag off and disable the Control-M/ADF definitions; no schema change.

### No UI change
No screen. Run rows are read through `GET /admin/jobs` and the Log Analytics workbook. SCR-44 is Epic 2. Alerts arrive by email.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-051-01 | AC1, BR1–BR3 | System | Synthetic COLLINS load and CCMS/SVAF files for 2026-11-15 | Four LOADED rows; dates, counts, start/end |
| TC-E1-051-03 | BR5 | System | SVAF sample with `Appraised Value` as text | Contract test fails; MSG-P2-002; merge blocked |
| TC-E1-051-04 | AC4, BR4 | System | ADF CCMS forced to fail | INT-10 MISSING; MSG-P2-004 within 15 minutes |
| TC-E1-051-05 | AC5, BR2 | System | No COLLINS load on 2026-11-24 | MISSING at 09:00; MSG-P1-001 with 2026-11-23 |
| TC-E1-051-06 | AC6, BR6 | System | EFS load started twice on 2026-11-25 | DUPLICATE; no second load |
| TC-E1-051-07 | X5 | Security | RW-CASEOWN calls rerun | 403; MSG-P4-002 |
| TC-E1-051-08 | BR2, BR5 | Unit | Retry window 05:00–09:00; layout field type mismatch | MISSING only after 09:00; field named |
## Guardrails
- No business value in code: times, folders and retry windows are configuration rows or properties.
- No personal data in logs, tests or prompts; sample files are synthetic and run rows hold counts only.
- No read of another module's tables; records reach P1 only through its loaders.
- No direct call from the Workbench to ALS, EFS, CCMS or SVAF.
## Out of scope
- The loaders and record checks for each data product: RWB-E1-003, RWB-E1-004 and RWB-E1-009.
- AMIS, RPS and GL feeds: Epic 3 and Epic 6.
- Run books for every other Epic 1 job: RWB-E1-056.
- The SCR-44 monitor screen: Epic 2.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-008 | Data moves by COLLINS or a file load | Epic 1 §3.2; Program §5.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, 06 |
| REQ-RDF-002 | Account data current to the previous working day | Program §5.1; Epic 1 §3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, 05 |
| REQ-RDF-003 | EFS history reaches the case | Program §5.1; Epic 1 §3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, 06 |
| REQ-RDF-004 | Collateral and appraisals without a lookup in CCMS or SVAF | Program §5.1; Epic 1 §3.2 | FEAT-RDF-22 | All recovery processes | None | TC-E1-051-01, 03, 04 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §12; SPEC-001 | Control-M and ADF job names are proposed. | A name change is a configuration edit, not code. | Use the proposed names until SCB IT issues the bank standard (DL12). | RESOLVED | SPEC-001 |
| CLAR-002 | §4; SPEC-002 | The ADF move time is assumed. | Determines when JOB-09 finds the file. | Sunday 23:00 (DL12); a late move produces MISSING and an alert. | RESOLVED | SPEC-002 |
| CLAR-003 | AC4; SPEC-007 | The 15-minute alert target is assumed. | Determines the alert rule evaluation window. | 15 minutes (DL11); record the SIT result as the baseline. | RESOLVED | SPEC-007 |
| CLAR-004 | §12; SPEC-013 | Does the rerun endpoint restart the Control-M/ADF job? | Two different systems; a wrong assumption would mislead operations. | No — it reruns the Workbench job (JOB-01 or JOB-09) from its failed step. The bank scheduler job is restarted in Control-M/ADF per the run book. | RESOLVED | SPEC-013 |
| CLAR-005 | AC1; SPEC-005 | 2026-11-15 is a Sunday; the AC expects CCMS/SVAF moved that day and JOB-09 on Monday 2026-11-16. | Confirms the calendar. | 2026-11-15 is a Sunday; the move is by 23:00 and JOB-09 runs 2026-11-16 04:00. | RESOLVED | SPEC-005 |
| CLAR-006 | BR6; SPEC-010 | What is the idempotency key for JOB-01? | Determines duplicate behaviour. | `interface_id + business_date`; a LOADED key writes DUPLICATE. | RESOLVED | SPEC-010 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, the batch schedule or DL11/DL12.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend feed story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New Control-M/ADF feed scheduling, run recording, failure alerts and layout contract tests; existing job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: scheduled feeds and contract tests, no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 4 acceptance criteria, 5 exception paths and 8 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

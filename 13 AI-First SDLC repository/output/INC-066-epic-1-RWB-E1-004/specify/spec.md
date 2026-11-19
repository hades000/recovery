# Technical Specification — RWB-E1-004 EFS extract load

| Field | Value |
|---|---|
| Story | RWB-E1-004 — EFS extract load |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-066-epic-1-RWB-E1-004` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-003); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 004 EFS extract load v1.md`; FSD P1 A2.4; TSD P1 T3.1 (`collections_history`), T5.1 (INT-07) |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1; Program 5.1; REQ-RDF-003; FEAT-RDF-04; US-RWB-E1-004; DQ-036..DQ-042; R-UNI-40; CTL-02, CTL-11; DL11, DL25, DL29; NFR-014 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The data steward reads runs through the job endpoint; the team manager sees the latest contact on the Power BI case list. |
| Logic In Scope | `YES` — INT-07 checks, mapping approval, named action-code filter, upsert by record key, movement check, freshness stamp, window check and case-list enrichment. |
| API In Scope | `NO` — no new or changed endpoint. The story uses existing `GET /api/recovery/v1/admin/jobs` (API-P1-001) and `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (API-P1-002). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `collections_history` (new); `load_run` (checks and mapping version); `dq_exception` (DQ-040/041); `case_list_row` (`last_contact_at`, `last_action_code`); `source_field_map` (`approval_ref`); JOB-01. |
| New Nodes Required | `YES` — `EfsLoadStepConfig`, `EfsWindowCheck`, `CollectionsHistory`, `CollectionsHistoryRepository`, `CollectionsHistoryService`, `CaseListLastContactEnricher`. |
| Inherited Existing Behavior | Load framework, load_run, dq_exception, mapping tables (RWB-E1-003); case list step (RWB-E1-002); freshness stamp (RWB-E1-015); reference data load (RWB-E1-043). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Contact history before day 90 comes from EFS through COLLINS. | SPEC-RWB-E1-004-001 | DIRECT | INT-07 staging records only; no EFS call. | COVERED |
| BR2 | A load is refused in full on a failed business date, structure, control total or key check, or an unapproved mapping. | SPEC-RWB-E1-004-002, 003 | DIRECT | DQ-036–DQ-039; mapping approval. | COVERED |
| BR3 | Records with unknown references or codes are held; above 0.50 percent the load is refused. | SPEC-RWB-E1-004-004 | DIRECT | DQ-040/041; `load.hold.tolerance.pct`. | COVERED |
| BR4 | Only action codes in the named list are kept. | SPEC-RWB-E1-004-005 | DIRECT | `efs.history.action.codes`; skipped and counted. | COVERED |
| BR5 | INT-07 must be complete by 08:00, or the load is LATE and the product stale. | SPEC-RWB-E1-004-008, 009 | DIRECT | `load.window.end.INT-07`; freshness check. | COVERED |
| BR6 | A record already held is not written twice. | SPEC-RWB-E1-004-006 | DIRECT | Unique `efs_record_key`; ON CONFLICT DO NOTHING. | COVERED |
| BR7 | The latest contact per case is the latest `contact_at` across the case's accounts. | SPEC-RWB-E1-004-010 | DIRECT | Enricher aggregates by case. | COVERED |
| BR8 | Free-text notes are not loaded; only codes, dates and amounts. | SPEC-RWB-E1-004-006 | DIRECT | No notes column; synthetic test data. | COVERED |
| AC1 | 9,450 rows, 1,320 with promise; load_run 9,450 read/loaded COMPLETED; case row shows last contact 2026-11-30 15:42 and action PTP. | SPEC-RWB-E1-004-001, 006, 010 | DIRECT | Load and enrichment. | COVERED |
| AC2 | The job shows mapping version EFS-MAP-1; `source_field_map` carries approved_on 2026-11-18 and approval ref. | SPEC-RWB-E1-004-002 | DIRECT | Mapping version on the run. | COVERED |
| AC3 | No INT-07 by 08:00: LATE; LoadRefused failedCheck LATE; DP05 STALE; MSG-P1-001; 2026-11-27 rows unchanged. | SPEC-RWB-E1-004-008, 009, 011 | DIRECT | Window check and freshness. | COVERED |
| AC4 | Unapproved mapping EFS-MAP-2: MSG-P1-002; no rows written. | SPEC-RWB-E1-004-002 | DIRECT | Approval gate. | COVERED |
| AC5 | 40 unknown account keys (0.42 percent): 9,410 rows; 40 DQ-040 exceptions. | SPEC-RWB-E1-004-004 | DIRECT | Hold within tolerance. | COVERED |
| AC6 | 6 records with result R99: 6 DQ-041 exceptions; 9,444 rows. | SPEC-RWB-E1-004-004 | DIRECT | Code-map hold. | COVERED |
| AC7 | 120 records with action SYS01 not in the named list: not written, not held; `SKIPPED_ACTION_CODE = 120`. | SPEC-RWB-E1-004-005 | DIRECT | Skip and count. | COVERED |
| AC8 | Record key EFS-77001234 delivered twice: one row; `REPEATED = 1`. | SPEC-RWB-E1-004-006 | DIRECT | Unique key. | COVERED |
| AC9 | Missing "Call Result" column: refused at DQ-037 with MSG-P1-002; LoadRefused failedCheck DQ-037. | SPEC-RWB-E1-004-003 | DIRECT | Structure check. | COVERED |
| AC10 | Rerun of a COMPLETED load: 409 MSG-P1-011; history unchanged. | SPEC-RWB-E1-004-012 | DIRECT | Job guard. | COVERED |
| X1 | No complete INT-07 delivery by 08:00. | SPEC-RWB-E1-004-009 | DIRECT | LATE; LoadRefused; stale. | COVERED |
| X2 | Mapping version has no approval. | SPEC-RWB-E1-004-002 | DIRECT | Refused in full. | COVERED |
| X3 | Unknown account keys at or below 0.50 percent. | SPEC-RWB-E1-004-004 | DIRECT | Held; rest loaded. | COVERED |
| X4 | Code missing from the code map. | SPEC-RWB-E1-004-004 | DIRECT | Record held. | COVERED |
| X5 | Action code not in the named list. | SPEC-RWB-E1-004-005 | DIRECT | Skipped and counted. | COVERED |
| X6 | A record already held is delivered again. | SPEC-RWB-E1-004-006 | DIRECT | Not inserted; repeated count. | COVERED |
| X7 | Structure, control total or key check fails. | SPEC-RWB-E1-004-003 | DIRECT | Refused in full. | COVERED |
| X8 | Rerun of a completed load. | SPEC-RWB-E1-004-012 | DIRECT | 409 MSG-P1-011. | COVERED |
| X9 | A role without Platform administration U asks for a rerun. | SPEC-RWB-E1-004-013 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **the EFS contacts and promises for accounts at 90 days past due loaded each working day from the COLLINS daily batch**, so that **the contact history is on the case from its first day**.

The story loads INT-07 into `collections_history`, checks it like every other load and puts the latest
contact and action on the case list. It does not copy the history into the interaction ledger; P3 does
that at case entry. It does not build a screen.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-01 COLLINS load check and intake, INT-07 step, at each hourly attempt after INT-01 completes; window check at 08:00. |
| Preconditions | RWB-E1-003 framework and DP01 loaded; RWB-E1-002 case list; RWB-E1-015 freshness; COLLINS INT-07 staging and trailer; mapping EFS-MAP-1 approved with sign-off; code maps loaded; parameters `load.window.end.INT-07` 08:00 and `efs.history.action.codes` (assumed, DL11, DL29). |
| Input | INT-07 staging records and trailer (`rwb.p1.collins.int07.table`); mapping and code maps. |
| Output | `collections_history`; `load_run`; `dq_exception`; DP05 freshness stamp; `case_list_row.last_contact_at`/`last_action_code`; LoadCompleted/LoadRefused. |
| Feature flag | `rwb.p1.efs-load`. Off: JOB-01 skips the INT-07 step and the window check. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `collections_history` | `efs_record_key` | INT-07 | System writes | Unique; repeat not inserted |
| `collections_history` | `account_no` | INT-07 | System writes | Must match `loan_account`; else held |
| `collections_history` | `contact_at` | INT-07 | System writes | Required; timestamptz |
| `collections_history` | `action_code` | INT-07 + code map | System writes | In the named list; else skipped |
| `collections_history` | `contact_result` | INT-07 + code map | System writes | Code map; else held |
| `collections_history` | `promise_amount`, `promise_date` | INT-07 | System writes | Optional; THB two decimals |
| `collections_history` | `business_date` | Job | System writes | Required |
| `load_run` | `mapping_version` | Job | System writes | `EFS-MAP-1` |
| `load_run` | `check_results` | Job | System writes | `SKIPPED_ACTION_CODE`, `REPEATED` |
| `case_list_row` | `last_contact_at`, `last_action_code` | Enricher | System writes | Latest across the case accounts |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `load_run` (INT-07) | — | Step starts | `RUNNING` | Row opened with interface INT-07 |
| `load_run` | `RUNNING` | Checks pass and write commits | `COMPLETED` | Counts, mapping version, checks; stamp; LoadCompleted |
| `load_run` | `RUNNING` | Blocking check or mapping fails | `REFUSED` | Nothing written; LoadRefused |
| `load_run` | `RUNNING` | Window check at 08:00 | `LATE` | LoadRefused failedCheck LATE; DP05 stale |
| DP05 freshness | `LOADED` | LoadRefused | `STALE` | Handled by RWB-E1-015 |

No case status changes.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No complete INT-07 by 08:00 | LATE; LoadRefused; DP05 stale; prior history stays | MSG-P1-001 |
| X2 | Mapping version has no approval | Refused in full | MSG-P1-002 |
| X3 | Unknown account keys at or below 0.50 percent | Records held; rest loaded | Count on the run |
| X4 | Action code or result missing from the code map | Record held; rest loaded | Count on the run |
| X5 | Action code not in the named list | Skipped and counted; not held | None |
| X6 | Record already held delivered again | Not inserted; counted | None |
| X7 | Structure, control total or key check fails | Refused in full; nothing written | MSG-P1-002 |
| X8 | Rerun of a completed load | 409; nothing changes | MSG-P1-011 |
| X9 | Role without Platform administration U asks for a rerun | 403 | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` with `type=INT-07`; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`. |
| Contract delta | None. The Job already carries `mappingVersion` and `checks`. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R for the listing; Platform administration U for rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P1-011; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; the Power BI case list is built by RW-BIANAL. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-003; SPEC-RWB-E1-004-001..015 | New batch step, window check, entity, repository, service and enricher. | Checks pass/fail; mapping approval; hold boundary 0.50; skip count; repeat key; movement; late; enricher across two accounts; rerun. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `EfsLoadStepConfig` | Spring Batch step in JOB-01 | Checks, maps and writes INT-07. |
| `EfsWindowCheck` | Quartz trigger at 08:00 | Marks INT-07 LATE and publishes LoadRefused when not complete. |
| `CollectionsHistory` | Entity | Maps `collections_history`. |
| `CollectionsHistoryRepository` | Repository | Inserts with ON CONFLICT (`efs_record_key`) DO NOTHING; returns inserted count. |
| `CollectionsHistoryService` | Service and published interface | Implements `CollectionsHistoryApi`. |
| `LoadCheckRunner`, `SourceMappingService` | Service (RWB-E1-003) | Run DQ-036–DQ-042; map through EFS-MAP-1 and the code maps. |
| `CaseListLastContactEnricher` | Service | Writes `last_contact_at` and `last_action_code` per case. |

Package `recovery.dataengine.load.efs`.

### Data and migration

Migration `V1_004__collections_history.sql` creates `collections_history` (`account_no` varchar(20),
`efs_record_key` varchar(40) unique, `contact_at` timestamptz, `action_code` varchar(10),
`action_contact_status` varchar(20), `contact_result` varchar(20), `promise_amount` numeric(18,2),
`promise_date` date, `business_date` date, standard columns) with index (`account_no`, `contact_at
desc`); adds `approval_ref` varchar(200) to `source_field_map`; adds `last_contact_at` timestamptz and
`last_action_code` varchar(10) to `case_list_row`.

### Load algorithm

1. Open `load_run` for INT-07; check the mapping version in force is approved.
2. Run DQ-036 business date, DQ-037 structure, DQ-038 control total, DQ-039 keys; any failure refuses
   the load.
3. Run DQ-040 references and DQ-041 lists of values; above 0.50 percent refuse; otherwise hold the
   failing records.
4. Skip records whose action code is not in `efs.history.action.codes`; count them.
5. Insert the remaining records by `efs_record_key` in one transaction; a key already held is not
   inserted again and is counted as repeated.
6. Write held records to `dq_exception`; run DQ-042 movement; call
   `FreshnessStampService.recordLoad("DP05", ...)`; set COMPLETED; publish LoadCompleted.
7. The case list step reads the latest contact per case across its accounts and writes the two columns.
8. At 08:00, if INT-07 is not COMPLETED, mark LATE and publish LoadRefused with failedCheck LATE.

**Transaction.** The INT-07 insert of one business date is one transaction; a blocking-check failure
writes nothing. The case-list enrichment runs in the case-list step's transaction. Publishes
`LoadCompleted` (EV-26) on success and `LoadRefused` (EV-27) on refusal or LATE.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-DATALOAD | Runs INT-07; writes history, load_run, exceptions and case list columns | All |
| RW-PLATADM | Platform administration R; rerun U | All |
| RW-DATASTEW | Platform administration R; records the EFS owner's sign-off | All |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Platform administration R | All |

### Observability and operations

- Job record: rows read, loaded, held, skipped, repeated; mapping version; checks.
- Metrics: rows loaded; held; skipped; repeated; duration; late count.
- Alerts: LATE; refusal; DP05 stale.
- Run book entry under RWB-E1-056.

### Performance

- Set-based insert per business date; unique key prevents duplicates.
- INT-07 runs inside the JOB-01 window before 08:00.
- The enricher aggregates the case accounts in one pass.

### Feature flag and rollback

`rwb.p1.efs-load`. Off: JOB-01 skips the INT-07 step and the window check. Rollback: turn the flag off;
the new table and columns remain and are harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-004-01 | AC1, BR1, BR7 | System | 9,450 records at 06:30; case RW-2026-000123 with two accounts | 9,450 rows; 1,320 promises; COMPLETED; last contact 15:42 and PTP |
| TC-E1-004-02 | AC2, BR2 | System | Completed load under EFS-MAP-1 | Mapping version and approval ref shown |
| TC-E1-004-03 | AC3, BR5 | System | No INT-07 by 08:00 | LATE; LoadRefused; DP05 STALE; MSG-P1-001; prior rows unchanged |
| TC-E1-004-04 | AC4, BR2 | System | EFS-MAP-2 without approval | MSG-P1-002; no rows |
| TC-E1-004-05 | AC5, BR3 | System | 40 of 9,450 unknown accounts (0.42 percent) | 9,410 rows; 40 DQ-040 |
| TC-E1-004-06 | AC6, BR3 | System | 6 records with R99 | 6 DQ-041; 9,444 rows |
| TC-E1-004-07 | AC7, BR4 | System | 120 records with SYS01 | Not written; `SKIPPED_ACTION_CODE = 120` |
| TC-E1-004-08 | AC8, BR6 | System | EFS-77001234 on two dates | One row; `REPEATED = 1` |
| TC-E1-004-09 | AC9, BR2 | System | Staging without "Call Result" | Refused DQ-037; LoadRefused |
| TC-E1-004-10 | AC10, X8 | System | Completed load; rerun | 409 MSG-P1-011; unchanged |
| TC-E1-004-11 | X9 | Security | RW-DATASTEW reruns | 403 MSG-P4-002 |
| TC-E1-004-12 | BR3 | Unit | Hold ratio 0.49, 0.50, 0.51 percent | Hold, hold, refuse |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3; SPEC-004 | What is the hold tolerance? | Determines hold vs refuse. | `load.hold.tolerance.pct` 0.50, assumed under DL25; data, not code. | RESOLVED | SPEC-004 |
| CLAR-002 | BR4; SPEC-005 | Which action codes are in the named list? | Determines skipped records. | `efs.history.action.codes`; assumed every code until the business lead names the list (DL29). | RESOLVED | SPEC-005 |
| CLAR-003 | BR5; SPEC-009 | What is the INT-07 window end? | Determines LATE. | 08:00 via `load.window.end.INT-07`, assumed under DL11 and NFR-014. | RESOLVED | SPEC-009 |
| CLAR-004 | BR2; SPEC-002 | How is the mapping approval proved? | Determines the gate. | `source_field_map.approved_on` and `approval_ref`; EFS-SIGN-2026-11-18. | RESOLVED | SPEC-002 |
| CLAR-005 | BR8; SPEC-006 | Are free-text notes loaded? | Determines field scope. | No; codes, dates and amounts only (mapping rule "Personal data"; CTL-11). | RESOLVED | SPEC-006 |
| CLAR-006 | BR7; SPEC-010 | How is the latest contact chosen across accounts? | Determines the case-list value. | Latest `contact_at` across the case's accounts (story BR7). | RESOLVED | SPEC-010 |
| CLAR-007 | UI; SPEC-010 | Is a Workbench screen built? | Determines UI scope. | No; the case list is Power BI. | RESOLVED | SPEC-010 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or DL25/DL29. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend/reporting story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New INT-07 EFS load, case-list enrichment and freshness stamp; existing job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new batch load with no contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 10 acceptance criteria, 9 exception paths and 4 run transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

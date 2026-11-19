# Technical Specification — RWB-TE-008 Decision log hash chain check

| Field | Value |
|---|---|
| Story | RWB-TE-008 — Decision log hash chain check |
| Epic / module | E1 / P7 Decision center and log |
| RUN_ID | `INC-029-epic-1-RWB-TE-008` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-017, BR-RWB-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 008 Decision log hash chain check v1.md` |
| Upstream IDs | BRD-RWB-007; FR-RWB-017; BR-RWB-008; REQ-DRI-003; US-RWB-TE-008; FEAT-DRI-01; NFR-035; CTL-06; JOB-14; JOB-13; RWB-E1-008; RWB-TE-007; `GET /admin/jobs`; `POST /admin/jobs/{jobId}/rerun` |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author / approval | Technical Specifier (agent run) / Product Owner (TBC); Compliance Reviewer |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route or label. Run records show on the job monitor through `GET /admin/jobs`; SCR-44 is Epic 2. |
| Logic In Scope | `YES` — schedule, dependency wait, fixed range, batched verification, failure counting, run record, three reports, rerun and concurrency guard. |
| API In Scope | `NO` — no endpoint is added or changed. Reuses `GET /api/recovery/v1/admin/jobs` and `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`, both owned by P1. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `HashChainVerifier`, `CanonicalEntryForm`, `ChainBreakNotifier` (RWB-E1-008 — verifier extended to count every failing entry); Quartz and job run records (RWB-TE-007); JOB-13 (RWB-E1-014); ACE notification and incident paths; job catalog and run book (RWB-E1-056). |
| New Nodes Required | `YES` — `HashChainCheckJob`, `ChainCheckReporter`, `JobRunRecorder`; JOB-14 catalog entry and run book. |
| Inherited Existing Behavior | Hash computation, canonical form and store reads (RWB-E1-008); Quartz scheduling, concurrency guard and run records (RWB-TE-007); notification groups (ACE); run book standard (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The whole chain is recomputed every night; a break is reported to Compliance the same day. | SPEC-RWB-TE-008-001, SPEC-RWB-TE-008-007, SPEC-RWB-TE-008-008 | DIRECT | Nightly JOB-14; MSG-P7-007 intact, MSG-P7-008 break. | COVERED |
| BR2 | Each `entry_hash` is recomputed from the canonical form; each `prev_hash` is compared with the entry before. | SPEC-RWB-TE-008-004 | DIRECT | Reuses `CanonicalEntryForm`. | COVERED |
| BR3 | A run covers `chain_seq` 1 to the highest at its start. | SPEC-RWB-TE-008-003 | DIRECT | End sequence fixed before verification. | COVERED |
| BR4 | JOB-14 runs after JOB-13 for the same business date, starting no later than 04:00. | SPEC-RWB-TE-008-002, SPEC-RWB-TE-008-012 | DIRECT | Poll every 5 minutes; latest-start parameter; copy end time recorded. | COVERED |
| BR5 | A run that does not complete is reported with the date of the last complete check. | SPEC-RWB-TE-008-009, SPEC-RWB-TE-008-020 | DIRECT | `FAILED`; MSG-P7-013; last intact date from run records. | COVERED |
| BR6 | Only one run is active at a time; a rerun is a new run record. | SPEC-RWB-TE-008-001, SPEC-RWB-TE-008-011 | DIRECT | `@DisallowConcurrentExecution`; `rerun = true`; 409 while active. | COVERED |
| BR7 | Start times and batch size are parameters, not code. | SPEC-RWB-TE-008-012 | DIRECT | `rwb.decision.chaincheck.*`. | COVERED |
| AC1 | 48,210 unchanged entries: record type JOB-14, previous business date, `COMPLETED`/`INTACT`; checks hold count, last seq and hash; MSG-P7-007 to Compliance. | SPEC-RWB-TE-008-001, SPEC-RWB-TE-008-006, SPEC-RWB-TE-008-007 | DIRECT | Full range; run record; report with count and hash. | COVERED |
| AC2 | Entry 30,005 changed: `BROKEN`, first break seq and ID; incident; MSG-P7-008 before 08:00. | SPEC-RWB-TE-008-005, SPEC-RWB-TE-008-008, SPEC-RWB-TE-008-020 | DIRECT | First failure retained; timestamp recorded. | COVERED |
| AC3 | Connection closed after 20,000: `FAILED`, count 20,000; platform administrator alert; MSG-P7-013 with last complete date. | SPEC-RWB-TE-008-006, SPEC-RWB-TE-008-009 | DIRECT | Partial count persisted; last intact run date. | COVERED |
| AC4 | Rerun of a failed 2 December run: new record `rerun = true`; report marked rerun; second start refused while running. | SPEC-RWB-TE-008-011 | DIRECT | New record; scheduler guard; 409. | COVERED |
| AC5 | Empty log: `INTACT`, count 0, last hash 64 zeros. | SPEC-RWB-TE-008-010 | DIRECT | Genesis hash when no entry. | COVERED |
| AC6 | JOB-13 ends 02:25: check starts then and records the end time; if not ended by 04:00, starts at 04:00 with note. | SPEC-RWB-TE-008-002 | DIRECT | Poll every 5 minutes; latest start; note. | COVERED |
| AC7 | Entries 12,001 and 40,350 changed: first break 12,001, failing count 2; one incident and one report name both. | SPEC-RWB-TE-008-005, SPEC-RWB-TE-008-008 | DIRECT | Continue after first failure; collect all IDs. | COVERED |
| AC8 | 37 entries appended during the run: checked 48,210, last 48,210; next night 48,247. | SPEC-RWB-TE-008-003, SPEC-RWB-TE-008-013 | DIRECT | Fixed end sequence. | COVERED |
| X1 | Entry does not match hash or `prev_hash`. | SPEC-RWB-TE-008-005, SPEC-RWB-TE-008-008 | DIRECT | `BROKEN`; first break, count, incident, report. | COVERED |
| X2 | Run stops on an error. | SPEC-RWB-TE-008-009 | DIRECT | `FAILED`; admin alert; MSG-P7-013. | COVERED |
| X3 | Rerun for the same business date. | SPEC-RWB-TE-008-011 | DIRECT | New record; rerun marker; no second scheduled run. | COVERED |
| X4 | Log is empty. | SPEC-RWB-TE-008-010 | DIRECT | `INTACT`, count 0, genesis. | COVERED |
| X5 | JOB-13 has not ended at 02:00. | SPEC-RWB-TE-008-002 | DIRECT | Wait to 04:00, then run and record. | COVERED |
| X6 | Entries appended while the job runs. | SPEC-RWB-TE-008-003, SPEC-RWB-TE-008-013 | DIRECT | Outside the range; next night. | COVERED |

## User story intent interpretation

As an **internal auditor (RW-AUDIT)**, I want **a nightly job that recomputes the whole decision log hash chain, records the result with the last hash, and reports a break to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

This is a backend scheduled-job story. It turns the on-demand verifier from RWB-E1-008 into JOB-14, adds the dependency on the decision log copy, records each run with its last hash, and reports intact, broken or incomplete to Compliance. It adds no screen or API; the platform administrator reruns through the existing job monitor endpoints.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger / schedule | Quartz cron `0 0 2 * * ?` in Asia/Bangkok for the previous business date; latest start 04:00; after JOB-13. |
| Preconditions | RWB-E1-008 complete; RWB-TE-007 complete; JOB-13 scheduled at 01:00; parameters `rwb.decision.chaincheck.start`, `.latest-start`, `.batch-size`; Compliance and platform administrator groups set in the ACE notification path. |
| Input / output | In: `decision_log_entry` in `chain_seq` order, 1 to the highest at run start. Out: JOB-14 run record with status, checks, counts and hash; MSG-P7-007/008/013 to Compliance; incident on break or failure. |
| Feature flag | `rwb.decision.hash-check`. Off: JOB-14 does not schedule; the on-demand verifier remains. |

## Field-level behaviour matrix

| Entity | Field | Source | Editable | Constraint |
|---|---|---|---|---|
| Job run record | `type`, `businessDate` | Job catalog / previous day | No | `JOB-14`; date of the log checked |
| Job run record | `status` | Run lifecycle | `WAITING` → `RUNNING` → `COMPLETED`/`FAILED` | One terminal state |
| Job run record | `checks.entriesChecked`, `lastSeq` | Verifier | Written at end or failure | 0 to fixed end; equal to end on success |
| Job run record | `checks.lastHash` | Last verified hash or genesis | Written at end | 64 hex characters |
| Job run record | `checks.result` | Verification | `INTACT`/`BROKEN` | Absent when `FAILED` |
| Job run record | `checks.breakSeq`, `breakEntryId`, `failingCount` | First failing entry; verifier count | Written on break | First failure only; count of all |
| Job run record | `checks.rerun`, `copyJobEndedAt`, `note` | Rerun; JOB-13 record; job logic | No | `true` on rerun; null with note if JOB-13 not ended |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `WAITING` | JOB-14 fires | JOB-13 not ended | `WAITING` | Poll every 5 minutes; no log read |
| `WAITING` | JOB-13 ends | Before 04:00 | `RUNNING` | Record `copyJobEndedAt`; fix end sequence |
| `WAITING` | 04:00 reached | JOB-13 still not ended | `RUNNING` | Note `JOB-13 not ended`; fix end sequence |
| `RUNNING` | Verification completes | No break / one or more breaks | `COMPLETED` | `INTACT` + MSG-P7-007, or `BROKEN` + incident + MSG-P7-008 |
| `RUNNING` | Error stops the run | Any error | `FAILED` | Partial count; admin alert; MSG-P7-013 |
| `COMPLETED`/`FAILED` | Rerun by RW-PLATADM | No active run | New `RUNNING` record | `rerun = true`; report marked rerun |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Entry does not match hash or `prev_hash` | `BROKEN`; first break and failing count; incident; Compliance told | MSG-P7-008 |
| X2 | Run stops on an error | `FAILED`; platform administrator alerted; Compliance told | MSG-P7-013 |
| X3 | Rerun for the same business date | New record; report says rerun; no second scheduled run | MSG-P7-007 or MSG-P7-008 |
| X4 | Log is empty | `INTACT`, count 0, genesis hash | MSG-P7-007 |
| X5 | JOB-13 has not ended at 02:00 | Wait to 04:00, then run and record the late copy | MSG-P7-007 or MSG-P7-008 |
| X6 | Entries appended during the run | Outside the run; checked next night | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` (Platform administration R) lists runs; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (Platform administration U) reruns; both owned by P1. |
| Contract delta / compatibility | None. The run record is an ACE job record; no recovery table or endpoint is added; no version change. |
| Authorization / errors | Platform administration R to read; U to rerun; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 when active; 503 MSG-GEN-006. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; job monitor is SCR-44 in Epic 2. | Existing tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-017; BR-RWB-008; SPEC-RWB-TE-008-001..021 | New Quartz job, dependency wait, reporter, run recorder; verifier extension. | Intact; break; multiple breaks; empty; failed; wait and latest start; rerun; append during run; access refusal. |

## Detailed design

### Components and schedule (SPEC-RWB-TE-008-001, SPEC-RWB-TE-008-019)

| Component | Type | Responsibility |
|---|---|---|
| `HashChainCheckJob` | Quartz job | JOB-14; `@DisallowConcurrentExecution`; waits for JOB-13; fixes the end sequence; runs the verifier; writes the run record. |
| `HashChainVerifier` | Service | From RWB-E1-008; extended to count every failing entry and continue after the first. |
| `ChainCheckReporter` | Service | Sends MSG-P7-007/008/013 to Compliance; raises the break incident. |
| `JobRunRecorder` | Service | Writes the ACE job run record through the RWB-TE-007 interface. |

JOB-14 fires at 02:00 Asia/Bangkok for the previous business date. It checks whether JOB-13 for that date has reached a terminal state. If not, it waits and checks every 5 minutes until 04:00, then runs and records `JOB-13 not ended`. The record captures `copyJobEndedAt` when JOB-13 has ended. A failed JOB-13 is terminal; JOB-14 still checks the live log and records its end time and status.

### Range and verification (SPEC-RWB-TE-008-003, SPEC-RWB-TE-008-004, SPEC-RWB-TE-008-005, SPEC-RWB-TE-008-013)

The job reads the highest `chain_seq` at the start and fixes it as the end; later appends are checked the next night. It calls `HashChainVerifier` over 1 to the fixed end in batches of 1,000, recomputing each `entry_hash` from the canonical form and comparing each `prev_hash` with the entry before. It counts every failing entry, keeps the first, and collects all failing IDs for the report.

### Run record and reporting (SPEC-RWB-TE-008-006, SPEC-RWB-TE-008-007, SPEC-RWB-TE-008-008, SPEC-RWB-TE-008-009, SPEC-RWB-TE-008-020)

The record holds type `JOB-14`, business date, status, start/end, and checks `entriesChecked`, `lastSeq`, `lastHash`, `result`, `breakSeq`, `breakEntryId`, `failingCount`, `rerun`, `copyJobEndedAt`, `note`. It is written on success and failure, with the count reached before an error. It is an ACE job record, not a recovery table.

| Condition | Message | Recipient | Timing |
|---|---|---|---|
| Intact | MSG-P7-007 with date, count, last hash | Compliance group | On completion, same day |
| Broken | MSG-P7-008 with date and entry ID, plus incident | Compliance group | Before 08:00 on the run date |
| Failed | MSG-P7-013 with date and last confirmed date | Compliance group | On failure, same day |

A rerun report carries the rerun marker. A break report names the first entry and every failing ID. The ACE notification path is used; no recovery template is added.

### Rerun, data and security (SPEC-RWB-TE-008-011, SPEC-RWB-TE-008-014, SPEC-RWB-TE-008-018, SPEC-RWB-TE-008-021)

`@DisallowConcurrentExecution` prevents a second scheduled start. A platform administrator rerun creates a new record with `rerun = true` and starts from `chain_seq` 1; a failed run is not resumed. While active, the rerun endpoint returns 409 MSG-GEN-004. No migration: the job reads `decision_log_entry` by the unique `chain_seq` index and writes only the ACE job record; it never writes to the log or repairs an entry. Authority: SY-DECLOG reads through the store; RW-COMPLY owns the job and receives reports; RW-AUDIT reads run records (Platform administration R) but may not rerun; RW-PLATADM reruns (U) and receives failure alerts; RW-SECADM receives the break incident with Compliance.

### Observability, performance and rollback (SPEC-RWB-TE-008-015, SPEC-RWB-TE-008-016, SPEC-RWB-TE-008-017)

Metrics: duration, entries checked, result, failing count, notifications sent and latency. Alerts: failed run, run not complete by 08:00, break, notification failure. Run book: purpose, schedule, owner (RW-COMPLY), failure signs, rerun steps, escalation (RWB-E1-056). Timing check on 10 million synthetic entries against a 60-minute budget (assumed; DL11); batches of 1,000 bound memory. Flag `rwb.decision.hash-check`; off removes the JOB-14 schedule; no schema change to reverse. No screen or API change: run records show through the P1 job monitor; SCR-44 is Epic 2.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-008-01 | AC1, BR1, BR2 | System | 48,210 unchanged entries | `COMPLETED`/`INTACT`; count, last seq/hash; MSG-P7-007 |
| TC-TE-008-02 | AC2, BR1 | System | Entry 30,005 changed | `BROKEN`; first break 30,005; incident; MSG-P7-008 before 08:00 |
| TC-TE-008-03 | AC3, BR5 | System | Connection closed after 20,000 | `FAILED`; count 20,000; admin alert; MSG-P7-013 with last date |
| TC-TE-008-04 | AC4, BR6 | System | Failed run; rerun at 08:30 | New record `rerun = true`; report marked rerun; second start refused |
| TC-TE-008-05 | AC5 | System | Empty log | `INTACT`; count 0; last hash 64 zeros |
| TC-TE-008-06 | AC6, BR4 | System | JOB-13 ends 02:25; and not ended by 04:00 | Start 02:25 with end time; or start 04:00 with note |
| TC-TE-008-07 | AC7, BR2 | System | Entries 12,001 and 40,350 changed | First break 12,001; failing count 2; one report names both |
| TC-TE-008-08 | AC8, BR3 | System | 37 entries appended during the run | Checked 48,210; last 48,210; next night 48,247 |
| TC-TE-008-09 | Access | Access | Role without Platform administration U reruns | 403; MSG-P4-002 |
| TC-TE-008-10 | BR5 | Unit | Last intact run lookup | Correct last confirmed date returned |
| TC-TE-008-11 | BR2, BR3 | Unit | Changed field; append after start | Mismatch at the changed entry; appended entry excluded |

## Guardrails

- No business value in code: times and batch size are parameters. No personal data in logs, tests or prompts; reports name entry IDs and `chain_seq` only.
- No read of another module's tables; the job reads only `decision_log_entry`. It never writes to the log and never repairs an entry; one canonical form is shared with the store.
- A rerun never overwrites a prior run record.

## Out of scope

- The store, hash computation and on-demand verifier (RWB-E1-008); per-entry checks in audit queries (RWB-E2-005).
- The data lake copy (RWB-E1-014, JOB-13); control-breach detection through administration screens (Epic 8, FEAT-ADM-10).

## Traceability

`REQ-DRI-003` → FEAT-DRI-01 (store this job checks) → BR1 to BR7 → SPEC-RWB-TE-008-001..021 → TC-TE-008-01..11. BRD Epic 1, 3.7; L3 process 17 Run the decision center.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4; SPEC-RWB-TE-008-002 | Does "JOB-13 ended" include a failed JOB-13? | Wait or run. | Yes — ended means terminal (completed or failed); the record captures end time and status. AC6 covers only the running case. | RESOLVED | SPEC-RWB-TE-008-002 |
| CLAR-002 | Contract; SPEC-RWB-TE-008-004 | Live log or lake copy? | Data source. | The live `decision_log_entry`; JOB-13 only gates the start. | RESOLVED | SPEC-RWB-TE-008-004 |
| CLAR-003 | AC3; SPEC-RWB-TE-008-009 | How is the last complete check date resolved? | Warning content. | The last `COMPLETED` run with result `INTACT`; if none, state no prior confirmation. Message content only. | RESOLVED | SPEC-RWB-TE-008-009 |
| CLAR-004 | AC2; SPEC-RWB-TE-008-020 | Deadline: 08:00 or 15 minutes? | Alert path. | AC2 requires before 08:00; the 15-minute deadline is the on-demand verifier in RWB-E1-008. | RESOLVED | SPEC-RWB-TE-008-020 |
| CLAR-005 | AC4; SPEC-RWB-TE-008-011 | Rerun during an active run? | API response. | 409 MSG-GEN-004; one run continues (story §12). | RESOLVED | SPEC-RWB-TE-008-011 |
| CLAR-006 | AC5; SPEC-RWB-TE-008-010 | Last hash for an empty log? | Result shape. | 64 zeros (genesis), count 0 (AC5). | RESOLVED | SPEC-RWB-TE-008-010 |
| CLAR-007 | BR7; SPEC-RWB-TE-008-012 | Start, latest start and batch size? | Schedule. | 02:00, 04:00, 1,000, Asia/Bangkok, owned by RW-COMPLY (assumed; story §3). | RESOLVED | SPEC-RWB-TE-008-012 |
| CLAR-008 | Contract; SPEC-RWB-TE-008-001 | Business date of a 02:00 run? | Run record. | The previous day's business date (story §4 step 1, AC1). | RESOLVED | SPEC-RWB-TE-008-001 |
| CLAR-009 | BR6; SPEC-RWB-TE-008-011 | Is a failed run resumed? | Restart. | No — a rerun starts from `chain_seq` 1 (story §12). | RESOLVED | SPEC-RWB-TE-008-011 |
| CLAR-010 | Guardrail; SPEC-RWB-TE-008-014 | Does the job write to the log? | Immutability. | No — reads only, never repairs (story §17). | RESOLVED | SPEC-RWB-TE-008-014 |

`CLARIFICATION_STATUS: RESOLVED` — all 10 items are answered from the story, TSD, FSD, rules or decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend scheduled-job story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New nightly hash chain check job, run record and Compliance reporting; no UI or API contract change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new Quartz job and reporting; existing job monitor endpoints reused]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria and 6 exception paths are mapped; 6 job state transitions are defined.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

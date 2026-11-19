# Technical Specification — RWB-E1-020 Allocation and assignment engine v1

| Field | Value |
|---|---|
| Story | RWB-E1-020 — Allocation and assignment engine v1 |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-043-epic-1-RWB-E1-020` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-005); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 020 Allocation and assignment engine v1 v1.md`; worked example v6 as the pattern |
| Upstream IDs | BRD-RWB-003; FR-RWB-005; BR-RWB-002..005; US-RWB-E1-020; CTX-FEATURE-003; CTX-RULE-002, 003; REQ-CWC-007..009, 016 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no new or changed screen in this story. The case list (SCR-02) and exception queue (SCR-09) display the result; their behaviour is unchanged. |
| Logic In Scope | `YES` — allocation, assignment, cap, overflow, exception, deviation branch, decision log and idempotency. |
| API In Scope | `NO` — no new or changed API contract. The story uses existing `GET /api/recovery/v1/cases/{caseId}` and `POST /api/recovery/v1/admin/jobs/{jobId}/rerun`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `JOB-03 Morning allocation` (new job); `AllocationService` (new published interface); `recovery_case`, `queue`, `queue_member`, `assignment`, `outbox`, `decision_log_entry` (new or extended tables). |
| New Nodes Required | `YES` — `AllocationJob`, `AllocationServiceImpl`, `AllocationRuleEvaluator`, `AssignmentEngine`, `OwnerLoadRepository`, `CaseAndWorkflowRepository`, `AllocationSummaryBuilder`, `AllocationRuleTable`. |
| Inherited Existing Behavior | Case creation (RWB-E1-018), roles/teams/queues (RWB-E1-019), decision log writer (RWB-E1-027), service levels/timers (RWB-E1-028), rule load (RWB-E1-029), queue/owner case list (RWB-E1-031), configuration (RWB-E1-042), reference data (RWB-E1-043), migrations (RWB-E1-044). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A case is allocated by the first allocation row, in row order, whose product group, region and exposure band match; "Any" matches every value. | SPEC-RWB-E1-020-005 | DIRECT | `AllocationRuleEvaluator` reads rows in force and returns the first match; `Any` is a wildcard. | COVERED |
| BR2 | The owner is chosen by the queue's `assignment_method`: ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER or SKILL. | SPEC-RWB-E1-020-006..009 | DIRECT | `AssignmentEngine` dispatches on the method; unsupported method is an error. | COVERED |
| BR3 | An owner at or above the queue's caseload cap is skipped; open cases are cases in the queue owned by the person with status other than CLOSED. | SPEC-RWB-E1-020-010 | DIRECT | `OwnerLoadRepository` counts open cases; cap is data (DL23). | COVERED |
| BR4 | A case that cannot be given an owner goes to the overflow queue of its queue. | SPEC-RWB-E1-020-011 | DIRECT | `queue.overflow_queue_id`; if null, exception queue with `NO_OVERFLOW_QUEUE`. | COVERED |
| BR5 | A case that matches no row goes to the exception queue, and the gap is logged; R-UNI-41 handles it once a person decides. | SPEC-RWB-E1-020-012 | DIRECT | `RWB-EXC`; decision log final call `RULE_GAP`; `CaseAllocationFailed` reason `NO_ROW_MATCHED`. | COVERED |
| BR6 | A case with an open deviation goes to the deviation handler queue. | SPEC-RWB-E1-020-004 | DIRECT | `R-DEV-01`; queue code from `allocation.deviation.queue.code`; no owner. | COVERED |
| BR7 | A decision that cannot be written to the decision log does not proceed. | SPEC-RWB-E1-020-013 | DIRECT | `DecisionLogWriter.write` is the last step before commit; failure rolls back. | COVERED |
| BR8 | A case is allocated at most once per business date. | SPEC-RWB-E1-020-002, SPEC-RWB-E1-020-026 | DIRECT | `last_allocation_date` check; idempotency key `caseId + businessDate`; `SKIPPED` outcome. | COVERED |
| BR9 | Each allocation records the rule row and the table version. | SPEC-RWB-E1-020-014, SPEC-RWB-E1-020-017 | DIRECT | `recovery_case.rule_version`, assignment row, decision log entry, job counts. | COVERED |
| AC1 | A new case is placed in the queue its row names. | SPEC-RWB-E1-020-005, SPEC-RWB-E1-020-014 | DIRECT | First matching row; case queue/team/region updated. | COVERED |
| AC2 | The owner is chosen by the queue's method (round robin example). | SPEC-RWB-E1-020-006 | DIRECT | Round-robin cursor; last owner U-02; next U-03. | COVERED |
| AC3 | An owner at the caseload cap is skipped. | SPEC-RWB-E1-020-010 | DIRECT | Cap 150; next owner below cap. | COVERED |
| AC4 | Every owner is at the cap: overflow queue, status NEW, no owner, summary MSG-P3-011. | SPEC-RWB-E1-020-010, SPEC-RWB-E1-020-011, SPEC-RWB-E1-020-016 | DIRECT | Overflow queue; summary per team. | COVERED |
| AC5 | No allocation row matches: exception queue, status NEW, decision log RULE_GAP, `caseAllocationFailed`, summary MSG-P3-012. | SPEC-RWB-E1-020-012, SPEC-RWB-E1-020-013, SPEC-RWB-E1-020-015, SPEC-RWB-E1-020-016 | DIRECT | Exception queue; rule gap; event. | COVERED |
| AC6 | Every allocation is logged with rule ID/version, queue, owner and inputs; a failed log write prevents the allocation. | SPEC-RWB-E1-020-013, SPEC-RWB-E1-020-014 | DIRECT | Log write last; rollback on failure; MSG-P3-013 on the job record. | COVERED |
| AC7 | A case with an open deviation goes to the deviation handler queue; no owner; status NEW. | SPEC-RWB-E1-020-004 | DIRECT | Deviation branch before rule evaluation. | COVERED |
| AC8 | A repeated run for the same date has no further effect; one assignment and one log entry; 1 case skipped. | SPEC-RWB-E1-020-002, SPEC-RWB-E1-020-026 | DIRECT | `last_allocation_date` check; job count `skipped`. | COVERED |
| AC9 | A run with no new cases completes with 0 read and 0 overflow/exception. | SPEC-RWB-E1-020-002, SPEC-RWB-E1-020-017 | DIRECT | Empty result set; summary zero. | COVERED |
| AC10 | JOB-03 waits for JOB-02; job monitor shows waiting with MSG-P1-001; cases stay NEW. | SPEC-RWB-E1-020-001, SPEC-RWB-E1-020-018, SPEC-RWB-E1-020-027 | DIRECT | Dependency check; job monitor; no allocation. | COVERED |
| AC11 | Two runs at the same time allocate each case once. | SPEC-RWB-E1-020-003, SPEC-RWB-E1-020-026 | DIRECT | `FOR UPDATE SKIP LOCKED`; per-case transaction; idempotency. | COVERED |
| AC12 | An owner one case below the cap gets the case. | SPEC-RWB-E1-020-010 | DIRECT | Count < cap; assignment. | COVERED |
| AC13 | A queue with no overflow queue sends the case to the exception queue with `NO_OVERFLOW_QUEUE`. | SPEC-RWB-E1-020-011, SPEC-RWB-E1-020-012 | DIRECT | Null overflow queue; exception reason. | COVERED |
| X1 | Every owner at the cap. | SPEC-RWB-E1-020-010, SPEC-RWB-E1-020-011 | DIRECT | Overflow. | COVERED |
| X2 | No allocation row matches. | SPEC-RWB-E1-020-012 | DIRECT | Exception. | COVERED |
| X3 | Decision log write fails. | SPEC-RWB-E1-020-013 | DIRECT | Rollback; retry next run. | COVERED |
| X4 | Case has `deviation_open = true`. | SPEC-RWB-E1-020-004 | DIRECT | Deviation queue. | COVERED |
| X5 | Run repeated for the same business date. | SPEC-RWB-E1-020-002, SPEC-RWB-E1-020-026 | DIRECT | Skip. | COVERED |
| X6 | No case has status NEW. | SPEC-RWB-E1-020-002, SPEC-RWB-E1-020-017 | DIRECT | Zero counts. | COVERED |
| X7 | JOB-02 has not completed. | SPEC-RWB-E1-020-001, SPEC-RWB-E1-020-018 | DIRECT | Wait; MSG-P1-001. | COVERED |
| X8 | A rerun starts while the first run holds a case. | SPEC-RWB-E1-020-003 | DIRECT | Row lock; skip. | COVERED |
| X9 | The overflow queue is not set. | SPEC-RWB-E1-020-011, SPEC-RWB-E1-020-012 | DIRECT | Exception `NO_OVERFLOW_QUEUE`. | COVERED |
| X10 | A user without the right reruns JOB-03. | SPEC-RWB-E1-020-019 | DIRECT | 403; MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **every new recovery case placed in a queue and given an
owner by the allocation and assignment rule tables on the morning it arrives**, so that **each case
at 90 days past due has one owner from its first day and nobody allocates cases by hand**.

The story is a backend batch story. It does not add a screen. It makes the case list (SCR-02) show a
queue and an owner after the run, and the exception queue (SCR-09) show cases that matched no row or
could not be given an owner. The team manager receives an allocation summary. The case owner reads
the cases given to them. The platform administrator can rerun the job from the job monitor.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-03 Morning allocation`, after `JOB-02` completes for the business date. |
| Schedule | Daily after JOB-02; complete by 07:00 Asia/Bangkok. |
| Preconditions | `JOB-02` completed for the business date; allocation table version `ALLOC-2026.11` loaded and approved (DL24); queues, queue members and caps loaded (RWB-E1-019); parameters `allocation.exception.queue.code` and `allocation.deviation.queue.code` loaded (RWB-E1-042); decision log writer available (RWB-E1-027); run book and job monitor (RWB-E1-056). |
| Input | Cases with status `NEW` and `last_allocation_date` before the business date; allocation rows in force; queues and queue members. |
| Output | Case queue, team, owner, status and rule version; assignment rows; decision log entries; allocation summary per team; job record with counts; `CaseAllocated` / `CaseAllocationFailed` events. |
| Feature flag | `rwb.p3.allocation`. Off: JOB-03 does not run and cases stay `NEW`. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `status` | `NEW` from case creation | System writes `ASSIGNED`; stays `NEW` on overflow/exception/deviation | One state at a time; `NEW`/`ASSIGNED` only in this story |
| `recovery_case` | `owner_user_id` | Null before the run | System writes the chosen owner; null on overflow/exception/deviation | Must be a queue member below the cap |
| `recovery_case` | `queue_id` | Null before the run | System writes the target, overflow, exception or deviation queue | Must be a valid queue |
| `recovery_case` | `team_code` | Null before the run | System writes the target queue's team | Must match the queue |
| `recovery_case` | `stage_clock_start` | Null before the run | System writes the business date/time | Starts the stage clock |
| `recovery_case` | `rule_version` | Null before the run | System writes the allocation table version | Must be the version in force |
| `recovery_case` | `last_allocation_date` | Null before the run | System writes the business date | Prevents a second allocation on the same date |
| `queue` | `rr_cursor_user_id` | Last owner | System writes the last owner after assignment | Only for ROUND_ROBIN |
| `assignment` | All fields | New row | System writes | One row per allocation |
| `decision_log_entry` | All fields | New row | System writes | Append-only, hash-chained |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `NEW` | Allocation rule matched | Row matched and an owner below the cap | `ASSIGNED` | Queue, team, owner, stage clock, rule version, assignment row, decision log, `CaseAllocated` |
| `NEW` | Allocation rule matched | Row matched and every owner at the cap | `NEW` in the overflow queue | Queue set to overflow; no owner; summary; no `CaseAllocated` |
| `NEW` | Allocation rule matched | No row matched | `NEW` in the exception queue | Queue set to exception; rule gap logged; `CaseAllocationFailed` |
| `NEW` | `DEVIATION_FLAGGED` (R-DEV-01) | `deviation_open = true` | `NEW` in the deviation handler queue | No owner; deviation branch; no `CaseAllocated` |
| `NEW` | Run repeated for the same date | `last_allocation_date = businessDate` | Unchanged | `SKIPPED`; no second assignment or log |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Every owner at the cap | Overflow queue; status `NEW`; no owner; summary | MSG-P3-011 |
| X2 | No allocation row matches | Exception queue; status `NEW`; rule gap; decision log `RULE_GAP` | MSG-P3-012; `CaseAllocationFailed` `NO_ROW_MATCHED` |
| X3 | Decision log write fails | Rollback; case stays `NEW`; no queue change; retry next run | MSG-P3-013 |
| X4 | `deviation_open = true` | Deviation handler queue; no owner; status `NEW` | R-DEV-01 |
| X5 | Run repeated for the same date | Skip; one assignment and one log entry | Job count `skipped` |
| X6 | No `NEW` case | Complete with 0 counts; summary 0 | MSG-P3-011/012 with 0 |
| X7 | JOB-02 not complete | JOB-03 does not start; job monitor shows waiting; cases stay `NEW` | MSG-P1-001 |
| X8 | Concurrent rerun on the same case | Row lock; second worker skips | Job count `skipped` |
| X9 | No overflow queue set | Exception queue with `NO_OVERFLOW_QUEUE` | MSG-P3-012 |
| X10 | User without Platform administration U reruns | 403; nothing runs | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases/{caseId}` (read the result); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (rerun JOB-03). |
| Contract delta | None. The response fields (`queueId`, `teamCode`, `ownerUserId`, `status`, `ruleVersion`) already exist in the case response. |
| Backward compatibility | Unchanged. |
| Authorization | Case record R with scope; Platform administration U for the rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label changes. SCR-02 and SCR-09 display existing fields. | Existing frontend tests remain green; no new frontend test is required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-005; SPEC-RWB-E1-020-001..028 | New job, service, rule evaluator, assignment engine, repositories and summary builder. | Positive, negative, boundary and error-path tests: rule match/no match/Any; each assignment method; cap boundary 149/150; overflow; exception; deviation; log failure; idempotency; concurrency; empty run; wait for JOB-02. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AllocationJob` | Quartz job | JOB-03; selects `NEW` cases; calls `AllocationService` per case; builds the summary; writes job counts. `@DisallowConcurrentExecution`. |
| `AllocationService` | Published interface | `allocate(caseId, businessDate)`; lock, deviation branch, rule match, owner choice, decision log write, case update, outbox event. |
| `AllocationRuleEvaluator` | Service | Reads rows in force; returns the first match in row order; `Any` wildcard. |
| `AssignmentEngine` | Service | ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL; cap skipping; round-robin cursor. |
| `OwnerLoadRepository` | Repository | Counts open cases per owner in a queue using `ix_case_owner_status`. |
| `CaseAndWorkflowRepository` | Repository | Reads and updates `recovery_case`, `queue`, `queue_member`, `assignment`. |
| `AllocationSummaryBuilder` | Service | Counts overflow and exception cases per team; fills MSG-P3-011 and MSG-P3-012. |
| `AllocationRuleTable` | Rule table | Rows with `rule_table = ALLOCATION`, read through `RuleTableReader`. |

### Package and boundaries

`src/main/java/.../recovery/casewf/allocation`, package `recovery.casewf.allocation`. The service is
published; other modules call it only through the interface. No module reads another module's tables.
The decision log writer is called through its published interface (RWB-E1-027). The rule table is read
through `RuleTableReader` (P4).

### Data and migration

- Reads: `recovery_case` (`id`, `case_no`, `product_group`, `region_code`, `exposure_band`,
  `deviation_open`, `status`, `last_allocation_date`), `queue` (`id`, `queue_code`, `team_code`,
  `role_code`, `assignment_method`, `capacity_cap`, `overflow_queue_id`), `queue_member` (`user_id`,
  `capacity`).
- Writes: `recovery_case` (`status`, `owner_user_id`, `queue_id`, `team_code`, `stage_clock_start`,
  `rule_version`, `last_allocation_date`, `version`), `queue` (`rr_cursor_user_id`), `assignment`
  (all columns), `outbox`.
- Lock: `SELECT ... FROM recovery_case WHERE id = ? AND status = 'NEW' FOR UPDATE SKIP LOCKED`;
  optimistic `version` on update.
- Migration in this story: `V020_1__allocation_columns.sql` adds `recovery_case.last_allocation_date`
  (date) and `queue.rr_cursor_user_id` (uuid). `queue_member` is created by RWB-E1-019.
- No hard-coded business values: queue codes, caps, methods, exception/deviation queue codes and the
  allocation table version are reference data.

### Allocation rule evaluation

1. `RuleTableReader.rowsInForce("ALLOCATION", businessDate)` returns rows in `row_order`.
2. For each row, compare `product_group`, `region_code`, `exposure_band`; `Any` matches every value.
3. The first match wins. If no row matches, return `NO_MATCH`.
4. The rule row and table version are recorded on the case, assignment and decision log.

### Assignment methods

| Method | Behaviour | Boundary |
|---|---|---|
| `ROUND_ROBIN` | Start after `queue.rr_cursor_user_id`; pick the next queue member below the cap; update the cursor. | If the cursor owner is not a member, start at the first member. |
| `LOWEST_LOAD` | Pick the member with the fewest open cases; tie-break by `user_id` for determinism. | If all at the cap, overflow. |
| `NAMED_OWNER` | Pick the named owner on the queue or case; if absent or at the cap, overflow. | Named owner must be a queue member. |
| `SKILL` | Pick the member whose skill matches the case product/route; tie-break by load then `user_id`. | If no skill match, overflow. |

Open cases = cases in the queue owned by the person with status other than `CLOSED`. The cap is
`queue.capacity_cap`; the value is data (DL23).

### Transaction and decision log

One transaction per case:

1. Lock the case row (`FOR UPDATE SKIP LOCKED`).
2. If `last_allocation_date = businessDate`, return `SKIPPED`.
3. If `deviation_open = true`, set the deviation queue and return `DEVIATION_QUEUE`.
4. Evaluate the rule; if no match, set the exception queue, write the decision log with
   `final_call = RULE_GAP`, publish `CaseAllocationFailed`, return `EXCEPTION`.
5. Choose the owner; if none below the cap, set the overflow queue and return `OVERFLOW`.
6. Update the case, insert the assignment and the outbox event.
7. Call `DecisionLogWriter.write` as the last step before commit. If it throws, roll back the whole
   transaction and return `FAILED_LOG`.

### Events

| Event | Payload | When |
|---|---|---|
| `CaseAllocated` (EV-02) | `caseId`, `queueId`, `ownerId`, `ruleId`, `ruleVersion` | After a successful assignment. |
| `CaseAllocationFailed` (EV-03) | `caseId`, `reason`, `ruleGap` | No row matched, no overflow queue, or a rule gap. |

Events are written to the outbox in the same transaction; the outbox publisher delivers them with
retry and idempotency.

### Summary and messages

- Per team: cases read, assigned, overflow, exception, deviation, skipped, failed.
- MSG-P3-011 for overflow; MSG-P3-012 for no row; MSG-P3-013 for a log failure; MSG-P1-001 for a
  waiting job; MSG-P4-002 for a forbidden rerun.
- Thai text follows DL10.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-RULES | Rules and parameters R | All |
| SY-CASEWF | Case record CRU; Queue and allocation CRU | All |
| SY-DECLOG | Decision log C | All |
| RW-TEAMMGR | Queue and allocation R | Team |
| RW-CASEOWN | Case record R | Own |
| RW-PLATADM | Platform administration U | All |
| RW-REFADM | Reference data C/U | All |

Every endpoint and job action is checked with Spring Security method security. The job runs under
`SY-CASEWF`; the rule evaluation under `SY-RULES`; the decision log write under `SY-DECLOG`.

### Observability and operations

- Job record: id, type, business date, status, counts, start/end, checks.
- Job monitor: JOB-03 status, last run, waiting on JOB-02, rerun action.
- Metrics: cases read/assigned/overflow/exception/deviation/skipped/failed; run duration; log
  failures; event publish failures.
- Alerts: job late (not complete by 07:00), job failed, log write failure, hash-chain break.
- Run book: purpose, schedule, owner, failure signs, restart steps, escalation (RWB-E1-056).

### Performance

- Target: 3,110 synthetic cases inside 15 minutes in SIT (assumed target; DL11).
- Per-case transaction; chunk commit per case; no long-running transaction across the run.
- Index `ix_case_owner_status` supports the open-case count.
- The job is `@DisallowConcurrentExecution`; a rerun skips locked cases.

### Feature flag and rollback

- `rwb.p3.allocation`. Off: JOB-03 does not run and cases stay `NEW`.
- Rollback: turn the flag off; redeploy the previous tag; the migration is forward-only, so the
  added columns remain nullable and harmless.

### No UI change

No new screen. SCR-02 Case list shows queue, owner and status after the run; SCR-09 Exception queue
shows `RWB-EXC` cases. Queue screens are Epic 2 (SCR-07). The team manager receives the summary
through the ACE notification path.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-020-01 | AC1, BR1 | System | One case per product group and region | Case in the row's target queue; team/region set |
| TC-E1-020-02 | AC2, BR2 | System | Three owners 120/95/140; last owner U-02 | U-03 gets the case; status `ASSIGNED`; assignment reason `ALLOCATION`; rule ID `ALLOC-014` |
| TC-E1-020-03 | AC3, BR3 | System | Next owner at 150 | Next owner below the cap gets the case |
| TC-E1-020-04 | AC4, BR4 | System | Every owner at 150 | Overflow queue; status `NEW`; no owner; MSG-P3-011 count 1 |
| TC-E1-020-05 | AC5, BR5 | System | SSME/NE3 with no row | Exception queue; `RULE_GAP`; `CaseAllocationFailed` `NO_ROW_MATCHED`; MSG-P3-012 |
| TC-E1-020-06 | AC6, BR9 | System | Run over the set; log write forced to fail for one case | One log entry per case; failed case not allocated; MSG-P3-013 |
| TC-E1-020-07 | AC7, BR6 | System | `deviation_open = true` | Deviation queue; no owner; status `NEW` |
| TC-E1-020-08 | AC8, BR8 | System | Repeat the run for 2026-12-01 | One assignment; one log entry; 1 skipped |
| TC-E1-020-09 | AC9 | System | No `NEW` cases | 0 read; 0 overflow/exception |
| TC-E1-020-10 | AC10 | System | JOB-02 not complete | JOB-03 waits; MSG-P1-001; cases `NEW` |
| TC-E1-020-11 | AC11, BR8 | System | Two workers on the same case | One assignment; one log entry |
| TC-E1-020-12 | AC12, BR3 | System | Next owner at 149 | Owner gets the case; now 150 |
| TC-E1-020-13 | AC13 | System | No overflow queue; all at cap | Exception `NO_OVERFLOW_QUEUE`; status `NEW` |
| TC-E1-020-14 | X10 | Security | Role without Platform administration U | 403; MSG-P4-002 |
| TC-E1-020-15 | BR1, BR2 | Unit | `Any` values; all four methods | First match; method behaviour; boundary |

## Guardrails

- No allocation value is written in code. Product groups, regions, bands, queues, methods, caps and
  queue codes are read from tables and parameters.
- No personal data in the allocation summary, the logs, the events or the test data. Cases are named
  by case number only.
- The service never reads tables owned by another module. Rule rows come through `RuleTableReader`
  (P4); the decision log through `DecisionLogWriter` (P7).
- The decision log entry is written in the same transaction as the case change; a failed write
  leaves the case unchanged.

## Out of scope

- Manual transfer and reassignment screens (RWB-E2-011, RWB-E2-012).
- Reallocation when an owner leaves or passes the cap (R-UNI-18 and R-UNI-19, Epic 2; daily
  rebalancing in RWB-E1-030).
- The values of the caseload caps and the service levels (DL22, DL23).
- Loading and validating the allocation table (RWB-E1-029).
- Placement on a queue by a model or an agent (RWB-E2-036).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 18.3.2 | R-DEV-01 | TC-E1-020-01, TC-E1-020-02, TC-E1-020-09 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07, FEAT-CWC-09 | 18.3.2 | R-UNI-41 | TC-E1-020-01, TC-E1-020-05, TC-E1-020-07 |
| REQ-CWC-009 | Round robin, lowest load, named owner, cap and overflow | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-08 | 18.3.2 | R-UNI-19 | TC-E1-020-02, TC-E1-020-03, TC-E1-020-04, TC-E1-020-12, TC-E1-020-13 |
| REQ-CWC-016 | Every allocation logged with rule ID and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-07 | 6.1 | R-UNI-39, R-UNI-40 | TC-E1-020-06, TC-E1-020-08, TC-E1-020-11, TC-E1-020-15 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1; SPEC-005 | Is the allocation table version `ALLOC-2026.11` approved? | The version is data; the run must use the version in force. | Yes — loaded and approved under DL24; the version is reference data. | RESOLVED | SPEC-005 |
| CLAR-002 | X1, X9; SPEC-011 | Are `RWB-EXC` and `DEV-HANDLER` the approved queue codes? | The codes are parameters, not code. | They are the assumed values under DL23; load them as parameters and confirm before go-live. | RESOLVED | SPEC-011, SPEC-024 |
| CLAR-003 | Contract; SPEC-001 | Is JOB-03 scheduled after JOB-02 and complete by 07:00? | Determines the trigger and the waiting behaviour. | Yes — Batch and Scheduling Design v2 and the story contract. | RESOLVED | SPEC-001 |
| CLAR-004 | API assessment; SPEC-019 | Does the allocation job need a new API? | If yes, a contract delta is required. | No — the job is scheduled; the existing case read and job rerun endpoints are reused. | RESOLVED | SPEC-019 |
| CLAR-005 | BR7; SPEC-013 | Is the decision log write synchronous before commit? | Determines rollback behaviour. | Yes — ADR-009 and story §4.7; a failed write rolls back. | RESOLVED | SPEC-013 |
| CLAR-006 | X9; SPEC-011 | What if a queue has no overflow queue? | Determines the fallback. | Exception queue `RWB-EXC` with reason `NO_OVERFLOW_QUEUE`; story AC13. | RESOLVED | SPEC-011, SPEC-012 |
| CLAR-007 | BR2, BR3; SPEC-006..010 | Are the cap 150 and `ROUND_ROBIN` fixed? | They are data, not code. | Data values; the example uses 150 and ROUND_ROBIN. Use them as test fixtures, not constants. | RESOLVED | SPEC-006..010 |
| CLAR-008 | Events; SPEC-015 | What are the event names and payloads? | Determines the outbox contract. | `CaseAllocated` (EV-02) and `CaseAllocationFailed` (EV-03), per Event and Messaging Design v2. | RESOLVED | SPEC-015 |
| CLAR-009 | Job order; SPEC-025 | In what order does the job process cases? | Affects the round-robin cursor and replay determinism. | Process in ascending `created_at`, then `case_id`; record the order in the job run log. This is an implementation decision; the ACs are per-case. | RESOLVED | SPEC-025 |

`CLARIFICATION_STATUS: RESOLVED` — all 9 items are answered from the story, the architecture or the
decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend batch capability; no UI or API contract change; existing case read and job rerun endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: new allocation/assignment job with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 13 acceptance criteria, 10 exception paths and 4 state transitions are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

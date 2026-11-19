# Technical Specification — RWB-E1-030 Daily rebalancing and queue measures

| Field | Value |
|---|---|
| Story | RWB-E1-030 — Daily rebalancing and queue measures |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-056-epic-1-RWB-E1-030` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-005, FR-RWB-018); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 030 Daily rebalancing and queue measures v1.md` |
| Upstream IDs | BRD-RWB-003, BRD-RWB-009; FR-RWB-005, FR-RWB-018; REQ-CWC-015, REQ-RDF-012; US-RWB-E1-030; CTX-FEATURE-003, CTX-FEATURE-009; R-UNI-18, R-UNI-19, R-UNI-30; NFR-001 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no new screen. SCR-02 and SCR-09 show the new owner and cases left without an owner through their existing components; the team view SCR-07 is Epic 2 and the Power BI queue page is built by RW-BIANAL. |
| Logic In Scope | `YES` — rebalancing selection, cap enforcement, hold/deviation skip, decision log, idempotency, queue measure snapshot and reconciliation, breach alert. |
| API In Scope | `NO` — no new or changed contract. The story reuses `GET /cases` (API-P3-001) for the reconciliation test and `POST /admin/jobs/{jobId}/rerun` (P1) for JOB-06. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `CaseAndWorkflowRepository`; `recovery_case`, `assignment`, `queue`, `queue_member`, `timer`; `AssignmentEngine` (RWB-E1-020); `DecisionLogWriter` (P7); JOB-15 reporting extract (P9); API-P3-001; job rerun (P1). |
| New Nodes Required | `YES` — `RebalanceJob`, `RebalanceService`, `QueueMeasureService`, `TimerBreachNotifier`, `queue_measure` table, `queue_member.row_order`. |
| Inherited Existing Behavior | Allocation and assignment (RWB-E1-020); timers and TimerBreached (RWB-E1-028); decision log writer (RWB-E1-027); queues, members and caps (RWB-E1-019); case list (RWB-E1-031); job monitor and run book (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Cases with no owner are assigned by the queue's method within the cap. | SPEC-RWB-E1-030-002 | DIRECT | `AssignmentEngine` with the queue's `assignment_method` and `capacity_cap`. | COVERED |
| BR2 | An owner above the cap loses the newest cases until inside the cap. | SPEC-RWB-E1-030-003 | DIRECT | Select by newest `assigned_at`; stop at the cap. | COVERED |
| BR3 | Cases with an open deviation or a legal hold are not moved. | SPEC-RWB-E1-030-004 | DIRECT | Filter `deviation_open = false AND legal_hold = false`. | COVERED |
| BR4 | A queue with no cap is reported and not rebalanced. | SPEC-RWB-E1-030-011 | DIRECT | Null `capacity_cap`; no move; snapshot still taken. | COVERED |
| BR5 | A move keeps the case status and the clocks. | SPEC-RWB-E1-030-006 | DIRECT | Only owner and assignment change; no status or timer write. | COVERED |
| BR6 | Measures publish only when queue depths reconcile to the case list with zero difference. | SPEC-RWB-E1-030-008, -009 | DIRECT | One REPEATABLE READ transaction; a difference holds the snapshot with MSG-P3-029. | COVERED |
| BR7 | Every move is logged before it takes effect. | SPEC-RWB-E1-030-006 | DIRECT | Decision log is the last step of the per-case transaction. | COVERED |
| BR8 | A breach raises an alert to the escalation role; the case does not move. | SPEC-RWB-E1-030-010 | DIRECT | `TimerBreachNotifier` on TimerBreached; MSG-P3-028. | COVERED |
| AC1 | 12 unassigned cases go 8 to U-61 and 4 to U-62 by lowest load, ties to the first member; each has reason REBALANCE and a decision log entry. | SPEC-RWB-E1-030-002, -005, -006 | DIRECT | Lowest load; deterministic member order; per-case transaction. | COVERED |
| AC2 | The snapshot depth equals the case list count at 06:52; TDR-BKK-CO shows depth 296, unassigned 0, average age 41 days. | SPEC-RWB-E1-030-008, -009 | DIRECT | One snapshot per queue at one time; reconcile before publish. | COVERED |
| AC3 | A breach in TDR-BKK-CO sends MSG-P3-028 with count 1 to the team manager; the next snapshot shows 1 breach. | SPEC-RWB-E1-030-010, -008 | DIRECT | Notifier on TimerBreached; `breached` count in the snapshot. | COVERED |
| AC4 | Every member at 150 with 5 unassigned: the 5 keep no owner; MSG-P3-011 count 5. | SPEC-RWB-E1-030-012 | DIRECT | No capacity; no move; summary. | COVERED |
| AC5 | Queue WO-BKK-CO has no cap: no move; the snapshot still reports the queue. | SPEC-RWB-E1-030-011 | DIRECT | Null cap; snapshot row. | COVERED |
| AC6 | Owner U-63 at 153, log failure on the second of 3 newest: 2 move, 1 stays; the job record lists MSG-P7-003. | SPEC-RWB-E1-030-006 | DIRECT | Continue on failure; per-case rollback. | COVERED |
| AC7 | A second JOB-06 run on 2026-12-02 moves nothing and writes no decision log entry. | SPEC-RWB-E1-030-007 | DIRECT | Idempotency key `caseId + businessDate`; balanced queue. | COVERED |
| AC8 | Owner U-64 at 152 with the 2 newest held: those 2 stay; the next 2 newest move. | SPEC-RWB-E1-030-004 | DIRECT | Skip held; continue selection. | COVERED |
| AC9 | Snapshot depth 88 against count 87: not published; data steward receives MSG-P3-029 with the check. | SPEC-RWB-E1-030-009 | DIRECT | Hold; alert. | COVERED |
| AC10 | Owner U-65 at exactly 150: no case moves off. | SPEC-RWB-E1-030-003 | DIRECT | Boundary exclusive: move only when count > cap. | COVERED |
| X1 | No member of the queue has capacity. | SPEC-RWB-E1-030-012 | DIRECT | No move; MSG-P3-011. | COVERED |
| X2 | No caseload cap loaded. | SPEC-RWB-E1-030-011 | DIRECT | Report only. | COVERED |
| X3 | Decision log write fails for a case. | SPEC-RWB-E1-030-006 | DIRECT | That case stays; run continues. | COVERED |
| X4 | JOB-06 runs again the same day. | SPEC-RWB-E1-030-007 | DIRECT | No further moves. | COVERED |
| X5 | A case has an open deviation or a legal hold. | SPEC-RWB-E1-030-004 | DIRECT | Not moved. | COVERED |
| X6 | Snapshot depth differs from the case count. | SPEC-RWB-E1-030-009 | DIRECT | Held; MSG-P3-029. | COVERED |
| X7 | An owner holds exactly the cap. | SPEC-RWB-E1-030-003 | DIRECT | No move. | COVERED |
| X8 | A role without Platform administration U reruns JOB-06. | SPEC-RWB-E1-030-014 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **a daily job that assigns unassigned cases and moves the newest
cases off owners above the cap by the assignment rules, and queue counts, ageing and service level breaches
published to Power BI**, so that **queues stay balanced and every team manager sees the same numbers as the
case list**.

The story is a backend batch and reporting story. It does not add the My queue/Team queues screens
(SCR-07, Epic 2), the steering dashboard (Epic 2), the reallocation when an owner leaves (R-UNI-18, Epic 2)
or the Power BI report layout (P9, RW-BIANAL).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Quartz `JOB-06 Daily rebalancing` at 06:30, or when JOB-03 completes for the business date if that is later. |
| Preconditions | RWB-E1-020 done (AssignmentEngine and CapacityService); RWB-E1-028 done (timers EXPIRED on a breach); RWB-E1-027 done (decision log); caps loaded (DL23); JOB-03 completed; JOB-06 runs as SY-CASEWF; JOB-15 copies the snapshot to the lake. |
| Input | Queues in force; members and capacity; open cases per owner; cases with no owner; EXPIRED service-level timers. |
| Output | Assignments with reason REBALANCE; decision log entries; one `queue_measure` snapshot per queue; `CaseTransferred` per move; job counts. |
| Feature flag | `rwb.p3.rebalance`. Off: JOB-06 does not move cases; the snapshot still runs. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `owner_user_id` | Null or the over-cap owner | System-written | Must be a queue member below the cap |
| `recovery_case` | `queue_id` | Current queue | Unchanged | A rebalance stays in the same queue |
| `recovery_case` | `status`, `stage_clock_start`, `prescription_date` | Current values | Unchanged | A move never resets them |
| `assignment` | `ended_at` | Null on the open row | System-written | Set when the move succeeds |
| `assignment` | `reason` | REBALANCE | System-written | LOV-ASSIGN-REASON |
| `queue_member` | `row_order` | QUEUE_MEMBER sheet order | System-written by the load | Deterministic tie-break |
| `queue_measure` | `depth`, `unassigned`, `avg_age_days`, `max_age_days`, `owner_min`, `owner_max`, `breached` | Snapshot query | System-written | One row per queue per `as_of` |
| `queue_measure` | `status` | TAKEN | System-written | PUBLISHED or HELD after the check |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| No snapshot | JOB-06 completes the measure query | None | TAKEN | Counts written |
| TAKEN | Reconciliation passes | Depth equals the case count for every queue | PUBLISHED | Visible to JOB-15 and Power BI |
| TAKEN | Reconciliation fails | Any queue differs | HELD | MSG-P3-029 to the data steward; not published |

No case status changes. The case owner and assignment change; the status and clocks do not.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No member has capacity | Cases keep no owner; counted in the summary | MSG-P3-011 |
| X2 | No cap loaded for a queue | No move; the queue is still reported | None |
| X3 | Decision log fails for a case | That case stays; the run continues; the job record lists it | MSG-P7-003 |
| X4 | JOB-06 runs again the same day | Balanced queues give no moves; no decision log entry | None |
| X5 | Case has an open deviation or a legal hold | Not moved | None |
| X6 | Snapshot depth differs from the case count | Snapshot HELD; not published; data steward told | MSG-P3-029 |
| X7 | Owner exactly at the cap | No case moved off | None |
| X8 | Role without Platform administration U reruns JOB-06 | 403; nothing runs | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases` (API-P3-001) for the reconciliation test; `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (P1) for JOB-06. |
| Contract delta | None. The published `QueueMeasureService` is an internal Java interface for P9, not an HTTP contract. |
| Backward compatibility | Unchanged. |
| Authorization | Case record R for the reconciliation read; Platform administration U for the rerun. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-GEN-004 when the job is running; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change. SCR-02/09 and Power BI display the result. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-015, REQ-RDF-012; SPEC-RWB-E1-030-001..020 | New job, rebalance service, measure service, notifier, table and index. | Over-cap selection; cap boundary; hold skip; no cap; no capacity; log failure; rerun; snapshot reconciliation; breach count; scope and authority. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `RebalanceJob` | Job | JOB-06; selects cases and owners; calls `RebalanceService`; writes counts. |
| `RebalanceService` | Service | R-UNI-19 selection, hold checks, owner choice, decision log, assignment swap. |
| `QueueMeasureService` | Published interface | Takes, reconciles and publishes the snapshot; `latestPublished(businessDate)` for P9. |
| `TimerBreachNotifier` | Listener | Sends MSG-P3-028 to the team manager on TimerBreached. |
| `CaseAndWorkflowRepository` | Repository | `recovery_case`, `assignment`, `queue`, `queue_member`, `timer`, `queue_measure`. |

### Rebalance algorithm

1. Wait for JOB-03 to complete for the business date; 06:30 is the earliest slot.
2. List queues in force; skip a queue with a null `capacity_cap` and record it.
3. Select unassigned cases in the queue with status NEW or ASSIGNED.
4. For each owner with open cases > cap, select the newest cases by `assigned_at` until the owner is inside the cap; skip `deviation_open` or `legal_hold`.
5. For each selected case, pick an owner below the cap in the same queue through `AssignmentEngine`; ties use `queue_member.row_order`, then `user_id`.
6. In one transaction per case: write the decision log, end the old assignment, insert the new assignment with reason REBALANCE, update the owner, publish `CaseTransferred`.
7. A failure on one case rolls back that case and the run continues.

### Queue measure snapshot

1. Open one REPEATABLE READ transaction.
2. For each queue: depth = open cases in the queue; unassigned = open cases with no owner; age in days from `entry_date` to `as_of`; owner spread = min/max open cases per owner; breached = EXPIRED SERVICE_LEVEL timers.
3. Write one `queue_measure` row per queue with `status = TAKEN`.
4. Compare each depth with the case count for the same queue and time; if every queue matches, set PUBLISHED; otherwise set HELD and send MSG-P3-029 to the data steward.
5. P9 reads only PUBLISHED rows through `QueueMeasureService`.

### Data and migration

- Writes `assignment`, `recovery_case.owner_user_id`, `queue_measure`, `outbox`.
- Migration `V030_1__queue_measure.sql` creates `queue_measure` (`id`, `queue_id`, `as_of`, `depth`, `unassigned`, `avg_age_days`, `max_age_days`, `owner_min`, `owner_max`, `breached`, `status`, standard columns; unique `(queue_id, as_of)`) and adds `queue_member.row_order` (integer) for the deterministic tie-break.
- Snapshot query uses one REPEATABLE READ transaction so depth and the case count are read at the same time.
- No personal data in the snapshot: counts only.

### Events

| Event | Payload | When |
|---|---|---|
| `CaseTransferred` (EV-04) | `caseId`, `fromOwner`, `toOwner`, `reasonCode = REBALANCE` | After each successful move |
| `TimerBreached` consumed | `timerId`, `caseId`, `escalateTo` | Triggers MSG-P3-028 to the team manager |

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-CASEWF | Case record CRU; Queue and allocation CRU | All |
| SY-DECLOG | Decision log C | All |
| RW-TEAMMGR | Queue and allocation R; receives summaries and alerts | Team |
| RW-BIANAL | Reporting CRUD on the snapshot | All |
| RW-DATASTEW | Receives the reconciliation break | All |
| RW-PLATADM | Platform administration U; reruns JOB-06 | All |

### Observability and operations

- Job record: id, business date, cases moved, owners rebalanced, queues skipped, snapshot status, failures.
- Metrics: moves; no-cap queues; no-capacity cases; log failures; snapshot held; breach alerts; run duration.
- Alerts: JOB-06 late or failed; snapshot held; reconciliation difference; decision log failure.
- Run book entry under RWB-E1-056.

### Performance

- Target: JOB-06 completes before the business day starts; snapshot for every queue inside the run window.
- Indexed owner counts (`ix_case_owner_status`); one transaction per case; one snapshot transaction.
- Test with 26,500 open cases and 12 queues in SIT.

### Feature flag and rollback

- `rwb.p3.rebalance`. Off: JOB-06 does not move cases; the snapshot still runs.
- Rollback: turn the flag off; the migration is forward-only and the added table/column remain harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-030-01 | AC1, BR1, BR7 | System | 12 unassigned; U-61 140, U-62 144 | 8 and 4; reason REBALANCE; decision log per case |
| TC-E1-030-02 | AC2, BR6 | System | Snapshot at 06:52 | Depth equals the case count; TDR-BKK-CO 296/0/41 |
| TC-E1-030-03 | AC3, BR8 | System | One breach in TDR-BKK-CO | MSG-P3-028 count 1; next snapshot breached 1 |
| TC-E1-030-04 | AC4, X1 | System | Every member at 150; 5 unassigned | 5 keep no owner; MSG-P3-011 count 5 |
| TC-E1-030-05 | AC5, BR4 | System | WO-BKK-CO with no cap | No move; queue reported |
| TC-E1-030-06 | AC6, BR7 | System | U-63 at 153; log fails on the second newest | 2 move; 1 stays; MSG-P7-003 on the job record |
| TC-E1-030-07 | AC7, X4 | System | JOB-06 twice on 2026-12-02 | No move; no decision log entry |
| TC-E1-030-08 | AC8, BR3 | System | U-64 at 152; 2 newest held | Held 2 stay; next 2 move |
| TC-E1-030-09 | AC9, BR6 | System | Depth 88 against count 87 | HELD; MSG-P3-029 with the check |
| TC-E1-030-10 | AC10, BR2 | System | U-65 at exactly 150 | No move |
| TC-E1-030-11 | X8 | Security | RW-CASEOWN reruns JOB-06 | 403 MSG-P4-002 |
| TC-E1-030-12 | BR7 | Resilience | Decision log fails for every move | No case moves; job lists each failure |

## Guardrails

- No business value in code: caps, methods and measure definitions are data.
- No personal data in the snapshot, alerts, logs or tests; the snapshot holds counts only.
- No read of another module's tables: P9 reads the snapshot through `QueueMeasureService`.
- A move never resets the stage clock or the prescription date.

## Out of scope

- Reallocation when an owner leaves or is absent (R-UNI-18, Epic 2).
- The team queues screen (SCR-07, Epic 2) and the steering dashboard (Epic 2).
- The Power BI report layout (P9, RW-BIANAL).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1; SPEC-002 | `queue_member` has no order column, so "first in the queue list" is undefined. | Determines the tie-break when loads are equal. | The QUEUE_MEMBER sheet row order is the queue list order; this story adds `queue_member.row_order` and RWB-E1-019 loads it. Until it is populated, the tie-break is `user_id` ascending. The AC's 8/4 split is unaffected because the loads differ. | RESOLVED | SPEC-002 |
| CLAR-002 | §4; SPEC-001 | Does JOB-06 start at 06:30 if JOB-03 has not completed? | Determines the dependency. | No; JOB-06 waits for JOB-03 for the business date. 06:30 is the earliest slot, not a hard start. | RESOLVED | SPEC-001 |
| CLAR-003 | BR5; SPEC-006 | Does a rebalance change the case status or the queue? | Determines side effects. | No; only the owner and assignment change. The case stays in the same queue and keeps its status and clocks. | RESOLVED | SPEC-006 |
| CLAR-004 | BR6; SPEC-008, -009 | What exactly is compared for reconciliation? | Determines when the snapshot is published. | Queue depth against the case list count for the same queue at the same `as_of`, in one REPEATABLE READ transaction; zero difference for every queue publishes. | RESOLVED | SPEC-008, SPEC-009 |
| CLAR-005 | AC3; SPEC-010 | Is the breach alert per case or per queue? | Determines the message count. | Per queue with a count; MSG-P3-028 carries `{count}` and `{queue}`. | RESOLVED | SPEC-010 |
| CLAR-006 | AC5; SPEC-011 | What happens to a queue with no cap? | Determines the move and the snapshot. | No case is moved; the queue is still reported in the snapshot. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the architecture or the decision
log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; no UI change in this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend rebalancing job and queue measure snapshot; no UI or API contract change; existing case read and job rerun endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: daily rebalancing and queue measures with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 10 acceptance criteria and 8 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

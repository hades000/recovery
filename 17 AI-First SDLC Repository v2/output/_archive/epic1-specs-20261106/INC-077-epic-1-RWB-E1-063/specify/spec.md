# Technical Specification — RWB-E1-063 Agent monitoring dashboard v1 [E2c]

| Field | Value |
|---|---|
| Story | RWB-E1-063 — Agent monitoring dashboard v1 [E2c] |
| Epic / module | E1 / P10 Agent runtime |
| RUN_ID | `INC-077-epic-1-RWB-E1-063` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-019); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 063 Agent monitoring dashboard v1 E2c v1.md` |
| Upstream IDs | BRD-RWB-010; FR-RWB-019; AC-RWB-019; BR-RWB-013; REQ-DRI-009; US-RWB-E1-063; FEAT-AGT-06; R-UNI-33, R-UNI-35, R-UNI-40; NFR-068; DL11, DL25, DL33; JOB-15 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no Workbench screen, route or React component. The Power BI report "Agent monitor v1" is a reporting artefact built by RW-BIANAL on the data lake table; SCR-46 is E2 (RWB-E2-031). |
| Logic In Scope | `YES` — daily aggregation, evaluation join, lake write, count check, cost alert, notification retry and rerun idempotency. |
| API In Scope | `NO` — no new or changed REST contract. The story adds a step to JOB-15 and reuses `GET /admin/jobs` and `POST /admin/jobs/{jobId}/rerun`. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | JOB-15 Reporting extract (adds `agentRunDaily` step); `agent_run`, `agent_policy`, `agent_evaluation` (read); new `agent_alert` table; data lake table `agent_run_daily`; P6 notification path and JOB-11 outbox sender. |
| New Nodes Required | `YES` — `AgentRunExtractSource`, `AgentMonitorService`, `AgentRunExtractStep`, `CostAlertService`, `AgentAlertRepository`, Power BI report "Agent monitor v1". |
| Inherited Existing Behavior | Agent platform (RWB-E1-058), report/proposal (RWB-E1-061), data lake copy path (RWB-E1-014), integration adapters (RWB-E1-007), Quartz jobs (RWB-TE-007), job monitor (RWB-E1-056), migrations (RWB-E1-044). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The dashboard reads the data lake copy, never the live tables. | SPEC-RWB-E1-063-004, SPEC-RWB-E1-063-015 | DIRECT | Power BI reads `agent_run_daily` only. | COVERED |
| BR2 | A copy is published only when its row count and run sum match the source. | SPEC-RWB-E1-063-005 | DIRECT | Zero tolerance; hold the date on mismatch. | COVERED |
| BR3 | A cost alert is raised when the cost of an agent on a business date is above `daily_cost_cap_thb` (2,000, assumed; DL33). | SPEC-RWB-E1-063-006 | DIRECT | Strictly greater than; cap from the policy. | COVERED |
| BR4 | One alert per agent, type and business date. | SPEC-RWB-E1-063-007 | DIRECT | Unique `(agent_code, alert_type, segment, business_date)`; `ALL` for agent-level. | COVERED |
| BR5 | Fallback rate = runs with fallback / runs, 4 decimals. | SPEC-RWB-E1-063-002 | DIRECT | 9/120 = 0.0750. | COVERED |
| BR6 | Alerts go to the policy alert role and RW-RISK within 15 minutes of the step end (target, DL11). | SPEC-RWB-E1-063-008 | DIRECT | P6 notification; outbox retry. | COVERED |
| AC1 | Each agent shows runs, fallback rate, median/p95 latency, cost and the latest evaluation score by version; INTAKE 120 runs, 0.0750; acceptance/override show "no L1 runs". | SPEC-RWB-E1-063-002, SPEC-RWB-E1-063-003, SPEC-RWB-E1-063-009 | DIRECT | Aggregate rows and fixed no-L1 label. | COVERED |
| AC2 | SCREENING above cap raises one `COST_CAP` alert with measured 2,310.5000 and threshold 2,000; MSG-P10-004 to RW-COE and RW-RISK; no INTAKE alert. | SPEC-RWB-E1-063-006, SPEC-RWB-E1-063-007, SPEC-RWB-E1-063-008 | DIRECT | Strict comparison; role from policy. | COVERED |
| AC3 | A lake write with 1 row for 2 groups is held; report shows 2026-11-30; step failed in GET /admin/jobs; data steward alerted. | SPEC-RWB-E1-063-005, SPEC-RWB-E1-063-010, SPEC-RWB-E1-063-014 | DIRECT | No publish; previous date stays; MSG-P2-004. | COVERED |
| AC4 | A rerun for 2026-12-01 leaves the same 2 rows and no second alert or notification. | SPEC-RWB-E1-063-004, SPEC-RWB-E1-063-007, SPEC-RWB-E1-063-013 | DIRECT | Replace-by-date; unique alert key. | COVERED |
| AC5 | EXTRACT with no runs shows runs 0 and cost 0.0000; no alert. | SPEC-RWB-E1-063-011 | DIRECT | Left join from approved policies. | COVERED |
| AC6 | Cost exactly 2,000.0000 raises no alert. | SPEC-RWB-E1-063-006 | DIRECT | Strict `>`. | COVERED |
| AC7 | Notification path down keeps the alert row with `sent_at` empty and retries through the outbox. | SPEC-RWB-E1-063-008 | DIRECT | Outbox retry; sent time set on success. | COVERED |
| X1 | Row count or run sum mismatch. | SPEC-RWB-E1-063-005, SPEC-RWB-E1-063-014 | DIRECT | Hold; previous day visible; job failed; alert. | COVERED |
| X2 | JOB-15 rerun for the same date. | SPEC-RWB-E1-063-004, SPEC-RWB-E1-063-013 | DIRECT | Replace, no duplicate alert. | COVERED |
| X3 | Agent with no runs. | SPEC-RWB-E1-063-011 | DIRECT | Row with 0; no alert. | COVERED |
| X4 | Cost equal to the cap. | SPEC-RWB-E1-063-006 | DIRECT | No alert. | COVERED |
| X5 | Notification interface unavailable. | SPEC-RWB-E1-063-008 | DIRECT | `sent_at` empty; retry. | COVERED |
| X6 | Role without Reporting R. | SPEC-RWB-E1-063-012 | DIRECT | Workspace refuses; MSG-P4-002. | COVERED |

## User story intent interpretation

As a **risk and model risk officer (RW-RISK)**, I want **a dashboard with runs, acceptance, override, fallback, latency, cost and evaluation score per agent and version, and an alert when an agent's daily cost passes its limit**, so that **every agent is watched from its first shadow run**.

The story is the reporting and alerting side of the platform. It adds no Workbench screen. It writes a
daily copy to the lake, checks the copy against the source, and raises one cost alert per agent and
date. RW-RISK and RW-COE read the Power BI report; RW-PLATADM can rerun JOB-15.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | JOB-15 Reporting extract at 01:30 Asia/Bangkok for the previous business date; manual rerun through `POST /admin/jobs/{jobId}/rerun`. |
| Preconditions | RWB-E1-058 run and policy tables; RWB-E1-014 lake copy path; RWB-E1-007 outbound adapters; JOB-15 exists; each approved policy has `daily_cost_cap_thb` (2,000 assumed; DL33) and `alert_role` (RW-COE assumed); RW-BIANAL built the report; RW-RISK and RW-COE hold Reporting R. |
| Input | `agent_run` rows for the business date; approved `agent_policy`; latest DONE `agent_evaluation` per agent and version. |
| Output | `agent_run_daily` rows; `agent_alert` rows; MSG-P10-004 notifications; JOB-15 step status. |
| Feature flag | `rwb.agent.monitor`. Off: JOB-15 skips the `agentRunDaily` step. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `agent_run` | `run_at`, `agent_code`, versions, `status`, `fallback`, `latency_ms`, tokens, `cost_thb` | Run | Read-only | Grouped by agent and version for the date. |
| `agent_policy` | `daily_cost_cap_thb` | Approved policy | Read-only | 2,000 assumed; DL33. |
| `agent_policy` | `alert_role` | Approved policy | Read-only | RW-COE assumed. |
| `agent_alert` | `alert_type` | Cost check | System-written | `COST_CAP`; `DRIFT` is E3. |
| `agent_alert` | `segment` | Policy / `ALL` | System-written | Product group and region, or `ALL` (DF-AGT-106). |
| `agent_alert` | `measured_value`, `threshold_value` | Cost / cap | System-written | 4 decimals. |
| `agent_alert` | `sent_to_role`, `sent_at` | Policy / sender | `sent_at` empty then set | Unique per agent, type, segment and date. |
| `agent_run_daily` | All columns | Aggregation | System-written | Replace-by-date; one row per agent and version group. |
| `agent_run_daily` | `eval_score` | Latest DONE evaluation | System-written | Null when no DONE evaluation. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | JOB-15 step starts | Flag on | `RUNNING` | Reads the date's runs. |
| `RUNNING` | Count check passes | Rows and run sum match | `SUCCEEDED` | Date published; alerts evaluated. |
| `RUNNING` | Count check fails | Mismatch | `FAILED` | Publish held; previous date stays; alert. |
| None | Cost above cap | Strictly greater | `agent_alert` created | `sent_at` empty; notification queued. |
| `agent_alert` | Notification succeeds | P6 accepts | `sent_at` set | No duplicate on rerun. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Row count or run sum mismatch | Publish held; previous date visible; step failed; data steward and RW-PLATADM alerted | MSG-P1-001 banner; MSG-P2-004 |
| X2 | Rerun for the same date | Rows replaced; no second alert or notification | None to a user |
| X3 | Agent with no runs | Row with runs 0 and cost 0.0000; no alert | None to a user |
| X4 | Cost equal to the cap | No alert | None to a user |
| X5 | Notification interface unavailable | Alert row kept; `sent_at` empty; outbox retries | None to a user |
| X6 | Role without Reporting R | Workspace refuses; nothing changes | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/admin/jobs` (step status); `POST /api/recovery/v1/admin/jobs/{jobId}/rerun` (rerun JOB-15). |
| Contract delta | None. JOB-15 and its step status already exist; the new step is internal. |
| Backward compatibility | Unchanged. |
| Authorization | Platform administration R to read; U to rerun; Reporting R for the Power BI workspace. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 when a run is already active; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No Workbench screen, component, route, state or label. The Power BI page is a BI artefact reconciled by system test. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-019; SPEC-RWB-E1-063-001..016 | New extract step, aggregation, cost alert and repository. | Positive, negative, boundary and error-path tests: 270-run fixture, 0-run agent, strict cap, rerun, mismatch, notification down, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `AgentRunExtractSource` | Published interface | Daily rows and cost alerts for JOB-15. |
| `AgentMonitorService` | Service | Aggregates runs; joins the latest DONE evaluation score. |
| `AgentRunExtractStep` | Job | Spring Batch step in JOB-15: write, count check, publish or hold. |
| `CostAlertService` | Service | Compares cost with the cap; writes `agent_alert`; calls P6. |
| `AgentAlertRepository` | Repository | `agent_alert` reads and writes. |
| Agent monitor v1 | Power BI report | One page per agent with version filters on `agent_run_daily`. |

### Package and boundaries

`recovery.agent.monitor`. JOB-15 calls the P10 published interface `AgentRunExtractSource`; the step
does not read another module's table. The Power BI report reads only the data lake table.

### Data and migration

`V10_006__agent_alert.sql` creates `agent_alert` with the standard record columns and unique
`(agent_code, alert_type, segment, business_date)`; index `agent_run (run_at)`. The data lake table
`agent_run_daily` has `business_date, agent_code, policy_version, prompt_version, model_version, runs,
answered, fallback, latency_p50_ms, latency_p95_ms, tokens, cost_thb, eval_score`. The table is a
reporting copy, not an operational table; the story §12 is its definition (TSD T3 omits it, F-02).

### Aggregation and count check

- Group `agent_run` by agent, policy version, prompt version and model version for the date.
- `runs`, `answered`, `fallback`, median and p95 `latency_ms`, token sums, `cost_thb`.
- Fallback rate = fallback / runs, 4 decimals; 9/120 = 0.0750.
- Latest DONE `agent_evaluation` per agent and version gives `eval_score`; no DONE leaves it null.
- Write one row per group, deleting the date's existing rows in the same transaction.
- Compare rows written and sum of runs with the source; zero tolerance. Mismatch holds the publish,
  leaves the previous date visible, marks the step failed and alerts.

### Cost alert and notification

- Read `daily_cost_cap_thb` and `alert_role` from the approved policy.
- Raise only when cost is strictly greater than the cap; equality raises nothing.
- `segment` = `ALL` for an agent-level policy, or `<product_group>:<region>` when the policy is
  segment-specific (DF-AGT-106).
- One row per agent, type, segment and date; a rerun finds the existing row and sends no second notice.
- Send MSG-P10-004 through P6 to the alert role and RW-RISK; if P6 is down, leave `sent_at` empty and
  let JOB-11 outbox sender retry.
- On a count mismatch, alert the data steward and RW-PLATADM with MSG-P2-004 (job failed) and the JOB-15
  run book.

### Dashboard

The Power BI report "Agent monitor v1" shows per agent and version: runs, fallback rate, median and p95
latency, cost, latest evaluation score. Acceptance and override show "no L1 runs" in Epic 1 because no
agent runs at L1. The report has two states: loaded (latest published date) and stale (MSG-P1-001 banner
naming the date shown). It never reads the live agent tables.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-RISK | Reporting R; receives alerts | All |
| RW-COE | Reporting R; receives alerts as policy role | All |
| RW-BIANAL | Reporting CRUD; builds the report | All |
| RW-PLATADM | Platform administration R/U; reruns JOB-15 | All |
| RW-DATASTEW | Receives the count-mismatch alert | All |

### Observability, performance and rollback

- Metrics: rows written, run sum, groups, step duration, alerts raised, notifications sent, retries.
- Alerts: count mismatch, step failed, notification backlog, cost cap breach.
- Performance: 270 runs in the fixture; one date scan with the `run_at` index; JOB-15 window 01:30–02:00.
- Feature flag `rwb.agent.monitor`: off skips the step.
- Rollback: flag off; redeploy the previous tag; `agent_alert` is additive and the lake write stops.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-063-01 | AC1, BR5 | System | INTAKE 120/9; SCREENING 150/21 on 2026-12-01 | Runs, 0.0750, latency, cost, eval score; no-L1 label |
| TC-E1-063-02 | AC2, BR3, BR6 | System | SCREENING 2,310.5000; cap 2,000 | One COST_CAP alert; MSG-P10-004 to RW-COE and RW-RISK; none for INTAKE |
| TC-E1-063-03 | AC3, BR2 | System | Lake write 1 row for 2 groups | Publish held; report shows 2026-11-30; step failed; data steward alerted |
| TC-E1-063-04 | AC4, BR4 | System | Rerun 2026-12-01 | Same 2 rows; no second alert or notification |
| TC-E1-063-05 | AC5 | System | EXTRACT with no runs | Runs 0; cost 0.0000; no alert |
| TC-E1-063-06 | AC6, BR3 | System | INTAKE cost 2,000.0000 | No alert |
| TC-E1-063-07 | AC7 | System | P6 down at 01:40 | Alert row with `sent_at` empty; retry succeeds |
| TC-E1-063-08 | X6 | Security | RW-CASEOWN opens the workspace | Refused MSG-P4-002 |
| TC-E1-063-09 | BR1 | System | Stop the live tables; open the report | Figures still load from the lake |
| TC-E1-063-10 | BR4 | Unit | Two alerts for the same agent/type/date | Second is not inserted |
| TC-E1-063-11 | AC3 | System | Count check with equal rows but wrong run sum | Publish held |

## Guardrails and out of scope

- No business value in code: caps and alert roles come from the approved policy.
- No personal data in logs, tests, the lake table or the alert; rows hold counts, times and amounts.
- No read of another module's table; JOB-15 calls the P10 interface.
- The dashboard never reads the live agent tables.
- Out of scope: acceptance and override per segment, drift alerts and SCR-46 (RWB-E2-031); drift
  detection with a raised decision (FEAT-AGT-13, E3); the steering dashboard (RWB-E2-009).

## Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-009 | Copied to the data lake daily for reporting, with row counts matched | Program 5.7 | FEAT-AGT-06 | 15 Manage performance, data and AI | R-UNI-33, R-UNI-35, R-UNI-40 | TC-E1-063-01..11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR4, AC2; SPEC-007 | What `segment` value does a COST_CAP alert use? | Unique key and row content. | `ALL` for an agent-level policy; `<product_group>:<region>` when the policy is segment-specific (DF-AGT-106). | RESOLVED | SPEC-007 |
| CLAR-002 | AC3, X1; SPEC-014 | Which message alerts the data steward on a count mismatch? | Notification content. | MSG-P2-004 (job failed) with JOB-15 and its run book; the step also reports failed in GET /admin/jobs. | RESOLVED | SPEC-014 |
| CLAR-003 | BR2, AC3; SPEC-005 | How does the step read back the lake rows to compare counts? | Count check. | The lake writer returns rows written and run sum in the same transaction; compare before commit; a mismatch rolls back and holds the date. | RESOLVED | SPEC-005 |
| CLAR-004 | AC1; SPEC-009 | Where do acceptance and override come from when no agent runs at L1? | Dashboard content. | A fixed "no L1 runs" state in Epic 1; the measures arrive with L1 feedback in E2. | RESOLVED | SPEC-009 |
| CLAR-005 | BR6, AC2; SPEC-008 | Who receives the cost alert? | Recipients. | The policy `alert_role` (RW-COE assumed) and RW-RISK. | RESOLVED | SPEC-008 |
| CLAR-006 | AC4, BR4; SPEC-013 | Does a rerun send a second alert? | Idempotency. | No; the unique key finds the existing row and no second notification is sent. | RESOLVED | SPEC-013 |
| CLAR-007 | BR3; SPEC-006 | Is 2,000 baht the approved cap? | Alert threshold. | An assumed value (DL33) held in each policy row; tests use 2,000 as a fixture. | RESOLVED | SPEC-006 |
| CLAR-008 | §12; SPEC-004 | `agent_run_daily` is not in TSD T3. Where is it defined? | Data lake schema. | It is a reporting copy defined in story §12; it is not an operational P10 table and no module reads it except the Power BI report. | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the data dictionary or the
message standard. No item changes a business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this reporting story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New daily agent reporting step, cost alert and Power BI report; no Workbench screen or contract change; job endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: batch reporting and alerting with no Workbench screen or API delta]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 7 acceptance criteria, 6 exception paths and 5 job/alert states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

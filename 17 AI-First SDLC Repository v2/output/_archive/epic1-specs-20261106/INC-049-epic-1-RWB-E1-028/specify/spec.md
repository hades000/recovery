# Technical Specification — RWB-E1-028 Service levels, timers, escalation and prescription dates

| Field | Value |
|---|---|
| Story | RWB-E1-028 — Service levels, timers, escalation and prescription dates |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-049-epic-1-RWB-E1-028` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-007); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 028 Service levels timers escalation and prescription dates v1.md` |
| Upstream IDs | BRD-RWB-003; FR-RWB-007; REQ-CWC-011, REQ-CWC-012, REQ-CWC-016; US-RWB-E1-028; CTX-FEATURE-003; R-UNI-30, R-UNI-43, R-DEV-01, R-UNI-20; NFR-001 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no new or changed screen. SCR-03 already carries the prescription date in its header (RWB-E1-023); the service-level timer panel is Epic 2 (RWB-E2-015). SCR-09 lists cases with MSG-P3-026 through its existing list. |
| Logic In Scope | `YES` — timer start/stop, working-day calculation, warning, breach and escalation, prescription date, deviation pause, catch-up and idempotency. |
| API In Scope | `NO` — no new or changed contract. The story uses existing `GET /cases/{caseId}/timers` (API-P3-013) and `GET /cases/{caseId}` (API-P3-002). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `CaseAndWorkflowController`; `CaseAndWorkflowRepository`; `timer`, `recovery_case`, `outbox`; API-P3-013; `DecisionLogWriter` (P7); `ProductParameterService` (RWB-E1-045); `ReferenceDataService` (RWB-E1-043); `RecoveryDataQuery` (P1). |
| New Nodes Required | `YES` — `TimerStarter`, `PrescriptionService`, `TimerPauseHandler`, `TimerCheckJob`, `WorkingDayCalculator`, `TimerService`. |
| Inherited Existing Behavior | Case creation (RWB-E1-018); allocation and transfer events (RWB-E1-020, RWB-E1-021); decision log writer (RWB-E1-027); service-level parameters (RWB-E1-045); legal periods and holidays (RWB-E1-043); job monitoring and run book (RWB-E1-056). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A SERVICE_LEVEL timer starts each time the case enters a queue or status, from the SERVICE_LEVEL row for its product group and status. | SPEC-RWB-E1-028-001, -002 | DIRECT | `TimerStarter` listens to CaseAllocated, CaseTransferred and CaseStateChanged; stops the running timer first. | COVERED |
| BR2 | The warning is raised at the warning percentage of the service level. | SPEC-RWB-E1-028-004 | DIRECT | `warn_at = started_at + (limit × warning percent)`, working days; 80 assumed (DL22). | COVERED |
| BR3 | A breach is raised to the named escalation role; the case does not move. | SPEC-RWB-E1-028-005 | DIRECT | `TimerBreached` with `escalateTo`; case queue, owner and status unchanged. | COVERED |
| BR4 | The prescription date is the earliest last-payment-plus-legal-period over the linked accounts; the contract date applies when no payment exists. | SPEC-RWB-E1-028-006 | DIRECT | `PrescriptionService` reads account dates through P1 and LEGAL_PERIOD through P3. | COVERED |
| BR5 | The prescription timer never pauses. | SPEC-RWB-E1-028-007 | DIRECT | `TimerPauseHandler` filters on `timer_type = SERVICE_LEVEL`. | COVERED |
| BR6 | A deviation pauses the stage clock; clearing it resumes the clock and recomputes the timers. | SPEC-RWB-E1-028-011 | DIRECT | DeviationRaised → PAUSED; DeviationCleared → RUNNING with dates moved by the paused working days. | COVERED |
| BR7 | A legal hold keeps the clocks running and visible. | SPEC-RWB-E1-028-012 | DIRECT | No listener changes timers on legal hold; the read endpoint still returns them. | COVERED |
| BR8 | Service levels count working days from the HOLIDAY table. | SPEC-RWB-E1-028-003 | DIRECT | `WorkingDayCalculator` reads HOLIDAY through `ReferenceDataService`. | COVERED |
| BR9 | Each timer start, warning and breach is logged with its rule and version. | SPEC-RWB-E1-028-010 | DIRECT | `DecisionLogWriter` in the same transaction; rule R-UNI-30 on the breach. | COVERED |
| AC1 | A timer starts at 2026-12-01 09:00 with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00; the read endpoint returns it. | SPEC-RWB-E1-028-001, -002, -003, -014 | DIRECT | 5 working days, 80%; holidays 2026-12-05..07. | COVERED |
| AC2 | The owner receives MSG-P3-003 at the warning; at expiry the breach goes to RW-TEAMMGR with TimerBreached and level 1; the case keeps its queue and owner; both have a decision log entry. | SPEC-RWB-E1-028-004, -005, -010 | DIRECT | Warning once; breach once; case not moved. | COVERED |
| AC3 | A new hire purchase case with last payment 2026-03-15 has prescription 2028-03-15 and a PRESCRIPTION timer with warn_at 2027-09-17; the case read shows it. | SPEC-RWB-E1-028-006, -007, -014 | DIRECT | 2 years from last payment; 180 calendar days warning. | COVERED |
| AC4 | No SERVICE_LEVEL version in force: no timer; the case is listed with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED". | SPEC-RWB-E1-028-002 | DIRECT | Missing row is recorded as a gap; no timer. | COVERED |
| AC5 | No LEGAL_PERIOD row for SSME: prescription empty; the case is listed with MSG-P3-026 for "legal period" and "SSME". | SPEC-RWB-E1-028-006 | DIRECT | Null prescription; gap recorded. | COVERED |
| AC6 | No last payment date: the contract date is used; contract 2025-06-30 gives prescription 2027-06-30. | SPEC-RWB-E1-028-006 | DIRECT | Fallback per BR4. | COVERED |
| AC7 | A missed 40-minute check raises three breaches on the next run. | SPEC-RWB-E1-028-008 | DIRECT | Catch-up orders by `expires_at`; one breach per timer. | COVERED |
| AC8 | A second run after a breach publishes no second TimerBreached; level stays 1. | SPEC-RWB-E1-028-009 | DIRECT | Skip when status EXPIRED or escalation level ≥ 1. | COVERED |
| AC9 | Decision log unavailable at expiry: timer stays RUNNING with level 0; job record carries MSG-P7-003; the next run raises the breach. | SPEC-RWB-E1-028-010 | DIRECT | Rollback the timer update; retry next run. | COVERED |
| AC10 | Deviation from 2026-12-02 to 2026-12-04 pauses the SERVICE_LEVEL timer and moves its dates by 2 working days; the PRESCRIPTION timer keeps its date. | SPEC-RWB-E1-028-011 | DIRECT | Pause window; no change to PRESCRIPTION. | COVERED |
| AC11 | A 5-day timer from Monday 2026-12-14 08:00 warns once on Friday 2026-12-18 at 08:05, not at 07:55. | SPEC-RWB-E1-028-003, -004 | DIRECT | 4 working days = warn point; boundary test. | COVERED |
| X1 | No SERVICE_LEVEL version in force. | SPEC-RWB-E1-028-002 | DIRECT | No timer; MSG-P3-026. | COVERED |
| X2 | No legal period for the product. | SPEC-RWB-E1-028-006 | DIRECT | Empty prescription; MSG-P3-026. | COVERED |
| X3 | An account has no last payment date. | SPEC-RWB-E1-028-006 | DIRECT | Contract date fallback. | COVERED |
| X4 | JOB-05 did not run for 40 minutes. | SPEC-RWB-E1-028-008 | DIRECT | Catch-up. | COVERED |
| X5 | The timer check runs again after a breach. | SPEC-RWB-E1-028-009 | DIRECT | No second breach. | COVERED |
| X6 | Decision log write fails at a breach. | SPEC-RWB-E1-028-010 | DIRECT | Timer stays RUNNING; retry. | COVERED |
| X7 | A deviation is raised. | SPEC-RWB-E1-028-011 | DIRECT | Pause stage clock only. | COVERED |
| X8 | The warning point is 4 of 5 working days. | SPEC-RWB-E1-028-004 | DIRECT | Warning once, at the first check after the point. | COVERED |
| X9 | A role without Case record R reads the timers. | SPEC-RWB-E1-028-015 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **a service level per queue and status, a timer on every case, a
warning to the owner and a breach raised to the named escalation point by rule, and a prescription date set
from the legal periods**, so that **no case waits past its limit unseen and no legal claim expires unnoticed**.

The story is a backend timing story. It starts and stops stage clocks on case events, runs JOB-05 every five
minutes, warns and escalates without moving the case, and sets the prescription date at creation. It does not
add the timer panel or escalation state to the case view (RWB-E2-015) or the prescription-review workflow
(R-UNI-31, Epic 2).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Case events (`CaseCreated`, `CaseAllocated`, `CaseTransferred`, `CaseStateChanged`, `DeviationRaised`, `DeviationCleared`) and Quartz `JOB-05 Timer check` every 5 minutes. |
| Preconditions | RWB-E1-020 done (CaseAllocated); RWB-E1-045 done (SERVICE_LEVEL row); RWB-E1-043 done (LEGAL_PERIOD and HOLIDAY); RWB-E1-027 done (decision log); SERVICE_LEVEL and LEGAL_PERIOD values loaded (DL22); HOLIDAY loaded; JOB-05 runs as SY-CASEWF. |
| Input | Case product group, status, queue, owner, linked accounts and their `last_payment_date`/`contract_date`; SERVICE_LEVEL rows; LEGAL_PERIOD and HOLIDAY rows; RUNNING timers whose `warn_at` or `expires_at` has passed. |
| Output | `timer` rows; `recovery_case.prescription_date`; decision log entries; `TimerDue` and `TimerBreached` events; job counts. |
| Feature flag | `rwb.p3.timers`. Off: no timers start and JOB-05 does nothing. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `timer` | `timer_type` | SERVICE_LEVEL or PRESCRIPTION | System-written | LOV-TIMER |
| `timer` | `started_at` | Case event time or case creation | System-written | Not null |
| `timer` | `expires_at` | Working-day calculation or legal period | System-written | Moved only by a deviation pause for SERVICE_LEVEL |
| `timer` | `warn_at` | Warning percentage or 180 days before | System-written | Optional; null when no warning |
| `timer` | `paused` | false | System-written | True only for a paused SERVICE_LEVEL timer |
| `timer` | `status` | RUNNING | System-written | LOV-TIMER-STATUS |
| `timer` | `escalation_level` | 0 | System-written | 0 or 1 in this story |
| `timer` | `warned_at` | Null | System-written | Set once, at the warning |
| `timer` | `escalated_to_role`, `escalated_at` | Null | System-written | Set at the breach |
| `recovery_case` | `prescription_date` | Null | System-written | Earliest legal period; null when no row |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | CaseAllocated, CaseTransferred, CaseStateChanged | Service level found | RUNNING | `expires_at` and `warn_at` set; decision log |
| RUNNING | CaseTransferred or CaseStateChanged | New queue or status | STOPPED | New timer starts for the new queue/status |
| RUNNING | DeviationRaised | `timer_type = SERVICE_LEVEL` | PAUSED | Pause start recorded |
| PAUSED | DeviationCleared | None | RUNNING | `expires_at` and `warn_at` moved by the paused working days |
| RUNNING | JOB-05 | `expires_at` passed | EXPIRED | `TimerBreached` for SERVICE_LEVEL, `TimerDue` otherwise; escalation level 1 |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No SERVICE_LEVEL row in force | No timer; the case is listed with the gap | MSG-P3-026 |
| X2 | No LEGAL_PERIOD row | Prescription null; the case is listed with the gap | MSG-P3-026 |
| X3 | No last payment date | Contract date used | None |
| X4 | JOB-05 missed runs | One pass raises every missed warning and breach once | None |
| X5 | JOB-05 runs again after a breach | No second `TimerBreached`; level stays 1 | None |
| X6 | Decision log write fails at expiry | Timer stays RUNNING with level 0; job record carries the error; next run retries | MSG-P7-003 |
| X7 | Deviation raised | SERVICE_LEVEL PAUSED; PRESCRIPTION unchanged | MSG-P3-004 |
| X8 | Warning point reached between checks | Warning sent once at the first check after the point | MSG-P3-003 |
| X9 | Caller lacks Case record R | 403 before the read | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases/{caseId}/timers` (API-P3-013); `GET /api/recovery/v1/cases/{caseId}` (API-P3-002) for `prescriptionDate`. |
| Contract delta | None. The timer response already carries `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status` and `escalationLevel`. |
| Backward compatibility | Unchanged. |
| Authorization | Case record R with scope. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503 store unavailable. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state changes. SCR-03 and SCR-09 display stored values through existing components. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-011, REQ-CWC-012, REQ-CWC-016; SPEC-RWB-E1-028-001..020 | New listeners, job, calculator, prescription service and timer service; migration. | Working-day boundaries; 80% warning; breach once; catch-up; deviation pause/resume; prescription earliest/fallback/missing; log failure rollback; scope and authority. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `TimerStarter` | Listener | Stops the running SERVICE_LEVEL timer and starts a new one on CaseAllocated, CaseTransferred or CaseStateChanged. |
| `PrescriptionService` | Listener | Sets the prescription date and the PRESCRIPTION timer on CaseCreated. |
| `TimerPauseHandler` | Listener | Pauses and resumes SERVICE_LEVEL timers on DeviationRaised and DeviationCleared. |
| `TimerCheckJob` | Job | JOB-05; warns, breaches and expires timers; catch-up; job counts. |
| `WorkingDayCalculator` | Service | Adds working days using the HOLIDAY table. |
| `TimerService` | Published interface | `timersFor(caseId)` and `prescriptionDate(caseId)` for other modules. |
| `CaseAndWorkflowController` | Controller | `GET /cases/{caseId}/timers`; access check. |
| `CaseAndWorkflowRepository` | Repository | `timer`, `recovery_case`, `outbox`. |

### Timer calculation

1. `started_at` is the case event time.
2. `expires_at` = `started_at` + `limit` working days, same time of day; the start day is day 0.
3. `warn_at` = `started_at` + `limit × warning_percent / 100` working days, same time of day.
4. Working days skip Saturday, Sunday and every date in the HOLIDAY table.
5. A SERVICE_LEVEL timer that is PAUSED has its `expires_at` and `warn_at` moved by the number of working days in the pause window when it resumes.
6. The PRESCRIPTION timer uses calendar days and never pauses; `warn_at` = `expires_at` − `legal.prescription.warn.days` (180 assumed).

### Prescription calculation

- Read the linked accounts through `RecoveryDataQuery.accountDates`.
- For each account: `last_payment_date` if present, otherwise `contract_date`; add the LEGAL_PERIOD for the product group.
- The earliest result is the prescription date.
- If no LEGAL_PERIOD row exists, leave the date null and record the gap; do not invent a period.
- One PRESCRIPTION timer per case; the date is set at creation and is not changed by a transfer or a deviation.

### JOB-05 transaction and idempotency

One transaction per timer:

1. Select RUNNING timers with `warn_at <= now` or `expires_at <= now`, ordered by `expires_at`.
2. Warning branch: if `warned_at` is null, set it and send MSG-P3-003 once; write the decision log.
3. Expiry branch: set EXPIRED, escalation level 1 and `escalated_at`; write `TimerBreached` to the outbox for SERVICE_LEVEL, `TimerDue` for other types; write the decision log as the last step.
4. If the decision log write fails, roll back the timer change; the next run retries.
5. A timer already EXPIRED or already warned is skipped; the idempotency key is `timerId` plus `WARN` or `EXPIRE`.

### Events

| Event | Payload | When |
|---|---|---|
| `TimerDue` (EV-18) | `timerId`, `caseId`, `timerType` | A non-SERVICE_LEVEL timer expires |
| `TimerBreached` (EV-19) | `timerId`, `caseId`, `escalateTo` | A SERVICE_LEVEL timer expires |

Events are written to the outbox in the same transaction. The case does not move on a breach (R-UNI-30).

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| SY-CASEWF | Case record CRU; Queue and allocation CRU | All |
| SY-DECLOG | Decision log C | All |
| RW-CASEOWN | Case record R | Own |
| RW-TEAMMGR | Case record R; receives the breach | Team |
| RW-LEGAL | Owns LEGAL_PERIOD rows | All |
| Every role with Case record R | Case record R | Its scope |

### Observability and operations

- Job record: id, business date, timers checked, warnings, breaches, expiries, failures, start/end.
- Metrics: timers started/stopped/paused/expired; warnings; breaches; catch-up count; log failures.
- Alerts: JOB-05 not complete for 10 minutes; decision log failure; breach spike.
- Run book entry under RWB-E1-056.

### Performance

- Target: all 26,500 open cases' timers inside one 5-minute cycle (NFR-001 volume).
- Index `ix_timer_due (expires_at) WHERE status = 'RUNNING'`; add `ix_timer_warn (warn_at) WHERE status = 'RUNNING'`.
- Catch-up processes in `expires_at` order; one transaction per timer.

### Feature flag and rollback

- `rwb.p3.timers`. Off: no timers start and JOB-05 does nothing.
- Rollback: turn the flag off; the migration is forward-only and the added index/column remain harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-028-01 | AC1, BR1, BR8 | System | Case in LIT-BKK-OFF at 2026-12-01 09:00 | RUNNING; expires 2026-12-09 09:00; warn 2026-12-08 09:00; read endpoint returns it |
| TC-E1-028-02 | AC2, BR2, BR3 | System | Timer passing warn_at and expires_at | MSG-P3-003 once; TimerBreached to RW-TEAMMGR with level 1; case unchanged |
| TC-E1-028-03 | AC3, BR4 | System | HP account, last payment 2026-03-15 | Prescription 2028-03-15; PRESCRIPTION warn 2027-09-17 |
| TC-E1-028-04 | AC4, BR1 | System | NPA-BKK-CO with no SERVICE_LEVEL | No timer; MSG-P3-026 for service level |
| TC-E1-028-05 | AC5, BR4 | System | SSME with no LEGAL_PERIOD | Null prescription; MSG-P3-026 for legal period |
| TC-E1-028-06 | AC6, BR4 | System | No last payment, contract 2025-06-30 | Prescription 2027-06-30 |
| TC-E1-028-07 | AC7, X4 | System | JOB-05 stopped 40 minutes; three timers expire | Three breaches on the next run |
| TC-E1-028-08 | AC8, X5 | System | Timer already EXPIRED at level 1 | No second TimerBreached; level stays 1 |
| TC-E1-028-09 | AC9, X6 | System | Decision log store down at expiry | Timer RUNNING at level 0; MSG-P7-003; next run breaches |
| TC-E1-028-10 | AC10, BR5, BR6 | System | Deviation 2026-12-02 to 2026-12-04 | SERVICE_LEVEL paused and dates moved 2 working days; PRESCRIPTION unchanged |
| TC-E1-028-11 | AC11, BR2 | System | 5 days from 2026-12-14 08:00 | Warning at 2026-12-18 08:05, not 07:55 |
| TC-E1-028-12 | X9 | Security | RW-REFADM calls GET /timers | 403 MSG-P4-002 |
| TC-E1-028-13 | BR9 | Resilience | Decision log forced to fail for every breach | No timer changes; job lists every failure |

## Guardrails

- No business value in code: service levels, warning percent, escalation roles, legal periods and holidays are data.
- No personal data in logs, tests, events or notifications; cases are named by case number.
- No read of another module's tables: account dates through `RecoveryDataQuery` (P1); legal periods and holidays through `ReferenceDataService` (P3).
- A breach never moves the case; the prescription timer never pauses.

## Out of scope

- The prescription warning forcing a litigation review (R-UNI-31, CTL-18, Epic 2).
- The timer panel and escalation state on the case view (RWB-E2-015).
- Notice period, cure period, offer validity and other stage-specific timers (route stories, Epic 3 to Epic 6).
- The service level values themselves (DL22).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1; SPEC-001 | Does a timer start on case creation with status NEW? | Determines the trigger set. | No; the SERVICE_LEVEL timer starts on CaseAllocated, CaseTransferred or CaseStateChanged. CaseCreated starts only the PRESCRIPTION timer. Story §4. | RESOLVED | SPEC-001, SPEC-007 |
| CLAR-002 | BR2; SPEC-003, -004 | Does the working-day count include the start day? | Determines `expires_at`. | No; the start day is day 0. AC1 (2026-12-01 to 2026-12-09) and AC11 (2026-12-14 to 2026-12-21) fix this. | RESOLVED | SPEC-003, SPEC-004 |
| CLAR-003 | BR4; SPEC-006 | Is the prescription warning 180 working or calendar days? | Determines `warn_at`. | Calendar days; 2028-03-15 − 180 = 2027-09-17 (AC3). `legal.prescription.warn.days` = 180 assumed. | RESOLVED | SPEC-006 |
| CLAR-004 | AC4, AC5; SPEC-002, -006 | Where is a missing service level or legal period recorded? | Determines the exception queue listing. | The case is listed on SCR-09 with MSG-P3-026; the gap is recorded against the case; no timer or date is invented. | RESOLVED | SPEC-002, SPEC-006 |
| CLAR-005 | §15; SPEC-014 | Does this story add the timer due date to SCR-03? | Determines UI scope. | No; SCR-03 already carries the prescription date (RWB-E1-023). The timer panel and the service-level due date come with RWB-E2-015. The read endpoint is delivered here. | RESOLVED | SPEC-014 |
| CLAR-006 | BR3; SPEC-005 | Does a breach move the case or change its owner? | Determines the side effects. | No; R-UNI-30 and story AC2: the case keeps its queue and owner. | RESOLVED | SPEC-005 |
| CLAR-007 | AC10; SPEC-011 | How is the pause duration counted? | Determines the moved dates. | By working days in the pause window, using the HOLIDAY table; the story AC10 expects 2 working days for 2026-12-02 to 2026-12-04. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the architecture or the decision
log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; no UI change in this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend timer and prescription capability; no UI or API contract change; existing timer and case read endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: timer listeners, JOB-05 and prescription calculation with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 9 business rules, 11 acceptance criteria and 9 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

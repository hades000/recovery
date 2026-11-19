# Technical Specification — RWB-E1-021 Transfer rules and engine v1

| Field | Value |
|---|---|
| Story | RWB-E1-021 — Transfer rules and engine v1 |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-055-epic-1-RWB-E1-021` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-006); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 021 Transfer rules and engine v1 v1.md` |
| Upstream IDs | BRD-RWB-003; FR-RWB-006; REQ-CWC-010, REQ-CWC-016; US-RWB-E1-021; CTX-FEATURE-003; R-UNI-20, R-UNI-21, R-UNI-39, R-UNI-40 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. SCR-02 and SCR-03 show the new queue, owner and hold banner through their existing components; the transfer screen SCR-05 is Epic 2 (RWB-E2-012). |
| Logic In Scope | `YES` — rule evaluation, eight triggers, manual transfer, legal hold, cap, overflow, idempotency, version lock, decision log. |
| API In Scope | `YES` — `POST /cases/{caseId}/transfer` gains `transferReasonCode`; `POST /cases/{caseId}/legal-hold` is delivered in E1 behind the flag. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `CaseAndWorkflowController`; `CaseAndWorkflowRepository`; `recovery_case`, `assignment`, `queue`; API-P3-006, API-P3-007; `AssignmentEngine` (RWB-E1-020); `DecisionLogWriter` (P7); `RuleTableReader` (P4); `TimerService` (RWB-E1-028). |
| New Nodes Required | `YES` — `TransferListener`, `TransferRuleEvaluator`, `TransferService`, `LegalHoldService`, `processed_event` table, `ux_assignment_open_case` index. |
| Inherited Existing Behavior | Allocation and assignment (RWB-E1-020); timer events (RWB-E1-028); decision log writer (RWB-E1-027); transfer rows (RWB-E1-029); transfer reasons (RWB-E1-043); queues (RWB-E1-019). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A case moves by the first transfer row, in row order, whose trigger and condition match. | SPEC-RWB-E1-021-002 | DIRECT | `TransferRuleEvaluator` reads rows in force and returns the first match. | COVERED |
| BR2 | The eight triggers are stage change, route decided, timer expired, deviation raised, deviation cleared, approval needed, document received and payment missed, plus manual request. | SPEC-RWB-E1-021-001 | DIRECT | `TransferListener` reads the seven event types; `CaseStateChanged` carries `ROUTE_APPROVED` as its event code. | COVERED |
| BR3 | A manual transfer needs a transfer reason from the list. | SPEC-RWB-E1-021-004 | DIRECT | `transferReasonCode` required; 422 MSG-P3-001. | COVERED |
| BR4 | A transfer to an owner at the cap is refused. | SPEC-RWB-E1-021-005 | DIRECT | `AssignmentEngine` cap check; 422 MSG-P3-002. | COVERED |
| BR5 | A case is in exactly one queue with one open assignment. | SPEC-RWB-E1-021-012 | DIRECT | Partial unique index `ux_assignment_open_case`; version lock. | COVERED |
| BR6 | No automated transfer while a legal hold is in force. | SPEC-RWB-E1-021-008 | DIRECT | Skip and log; no assignment change. | COVERED |
| BR7 | Lifting a hold returns the case to the status it paused in. | SPEC-RWB-E1-021-007 | DIRECT | `status_before_hold`; 409 on a double hold. | COVERED |
| BR8 | An event with the same ID is processed once. | SPEC-RWB-E1-021-010 | DIRECT | `processed_event` unique key; idempotency hit count. | COVERED |
| BR9 | Every transfer is logged with rule ID and version before it takes effect. | SPEC-RWB-E1-021-009 | DIRECT | Decision log write is the last step; rejection is also logged. | COVERED |
| BR10 | A transfer keeps the case status and the clocks. | SPEC-RWB-E1-021-013 | DIRECT | No status, stage clock or prescription write. | COVERED |
| AC1 | A route R4 decision moves the case to LIT-BKK-OFF with owner U-31, ends the old assignment, records reason TRANSFER and rule TRF-007/TRF-2026.11. | SPEC-RWB-E1-021-002, -003, -009 | DIRECT | First matching row; lowest load; assignment swap. | COVERED |
| AC2 | A manual transfer with reason R03 sets owner U-22 and records R03 on the assignment and decision log. | SPEC-RWB-E1-021-004, -003 | DIRECT | Manual path with the same transaction. | COVERED |
| AC3 | A rule transfer and a manual transfer in the same second leave one queue; the second is refused with MSG-GEN-004 and logged TRANSFER_REJECTED. | SPEC-RWB-E1-021-003, -012, -009 | DIRECT | Optimistic version check; rejection entry. | COVERED |
| AC4 | Each of the eight trigger rows moves the case to its target queue and records the row ID. | SPEC-RWB-E1-021-001, -002 | DIRECT | One listener; event code and condition match. | COVERED |
| AC5 | A reassign to U-23 and a legal hold place/lift return the case to IN_PROGRESS; each call has a decision log entry. | SPEC-RWB-E1-021-004, -005, -007 | DIRECT | Hold uses `status_before_hold`. | COVERED |
| AC6 | A manual transfer without a reason is refused with 422 MSG-P3-001; queue and owner unchanged. | SPEC-RWB-E1-021-004 | DIRECT | Validation before the lock. | COVERED |
| AC7 | A transfer to U-24 at 150 is refused with 422 MSG-P3-002 naming U-24. | SPEC-RWB-E1-021-005 | DIRECT | Cap check on the target owner. | COVERED |
| AC8 | A transfer of a CLOSED case is refused with 409 MSG-P3-005. | SPEC-RWB-E1-021-006 | DIRECT | Status guard before the move. | COVERED |
| AC9 | A decision log failure refuses a manual transfer with 503 MSG-P7-003; the case is unchanged. | SPEC-RWB-E1-021-009 | DIRECT | Rollback. | COVERED |
| AC10 | A legal hold stops an automated TimerDue transfer; the skip is logged with R-UNI-20. | SPEC-RWB-E1-021-008 | DIRECT | Hold check before the rule evaluation. | COVERED |
| AC11 | A repeated PaymentMissed event ID moves the case once and counts an idempotency hit. | SPEC-RWB-E1-021-010 | DIRECT | `processed_event`. | COVERED |
| AC12 | When every member of the target queue is at 150, the case goes to LIT-BKK-OVF with no owner and MSG-P3-011. | SPEC-RWB-E1-021-011 | DIRECT | Overflow queue from the target queue. | COVERED |
| AC13 | A second legal hold on a case already on hold is refused with 409 MSG-P3-005. | SPEC-RWB-E1-021-007 | DIRECT | State guard. | COVERED |
| AC14 | No transfer row matches DocumentStored: the case keeps its queue and owner and no decision log entry is written. | SPEC-RWB-E1-021-002 | DIRECT | No match is not a decision. | COVERED |
| X1 | Two transfers in the same second. | SPEC-RWB-E1-021-003, -012 | DIRECT | Version check; MSG-GEN-004. | COVERED |
| X2 | Manual transfer without a reason. | SPEC-RWB-E1-021-004 | DIRECT | 422 MSG-P3-001. | COVERED |
| X3 | Named target owner at the cap. | SPEC-RWB-E1-021-005 | DIRECT | 422 MSG-P3-002. | COVERED |
| X4 | Transfer of a closed case. | SPEC-RWB-E1-021-006 | DIRECT | 409 MSG-P3-005. | COVERED |
| X5 | Decision log write fails. | SPEC-RWB-E1-021-009 | DIRECT | 503 manual; event retry for rule. | COVERED |
| X6 | Rule trigger while legal_hold is true. | SPEC-RWB-E1-021-008 | DIRECT | Skip logged. | COVERED |
| X7 | The same event arrives twice. | SPEC-RWB-E1-021-010 | DIRECT | One transfer. | COVERED |
| X8 | No owner below the cap in the target queue. | SPEC-RWB-E1-021-011 | DIRECT | Overflow; MSG-P3-011. | COVERED |
| X9 | Hold on a case already on hold. | SPEC-RWB-E1-021-007 | DIRECT | 409 MSG-P3-005. | COVERED |
| X10 | No transfer row matches. | SPEC-RWB-E1-021-002 | DIRECT | No transfer, no log. | COVERED |
| X11 | A role without Queue and allocation U calls transfer. | SPEC-RWB-E1-021-016 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **cases moved between queues and roles by the transfer rule table
on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document
received, payment missed, or a manual request with a reason**, so that **hand-offs between teams run without
email**.

The story delivers the backend transfer engine and the two programmatic endpoints before the Epic 2 screens.
It does not add SCR-05, the queue history panel (RWB-E2-012, RWB-E2-016), reallocation when an owner leaves
(Epic 2, R-UNI-18) or the route decision itself (Epic 4).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | An outbox event (CaseStateChanged with ROUTE_APPROVED, TimerDue, DeviationRaised, DeviationCleared, ApprovalRequested, DocumentStored, PaymentMissed) or a manual `POST /transfer` / `POST /legal-hold`. |
| Preconditions | RWB-E1-020 done (AssignmentEngine and queues); RWB-E1-028 done (TimerDue); RWB-E1-027 done (decision log); transfer rows `TRF-2026.11` loaded (RWB-E1-029); LOV-TRANSFER-REASON R01..R06 loaded (DL23); caller holds Queue and allocation U or Case record U as applicable. |
| Input | Event ID, event code, case ID and case snapshot; transfer rows in force; manual request fields; legal-hold request. |
| Output | Updated queue/team/owner; ended and new assignment; decision log entry; `CaseTransferred`; `CaseStateChanged` for hold/release; `processed_event` row. |
| Feature flag | `rwb.p3.transfer`. Off: no rule transfers; the two endpoints return 404. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `queue_id`, `team_code`, `owner_user_id` | Target queue and chosen owner | System-written | Must be a valid queue; owner must be a member below the cap |
| `recovery_case` | `status` | Current status | System-written only by legal hold | ON_HOLD on place; `status_before_hold` on lift |
| `recovery_case` | `legal_hold` | false | System-written | true on place; false on lift |
| `recovery_case` | `status_before_hold` | Null | System-written | Set on place; cleared on lift |
| `recovery_case` | `rule_version` | Transfer table version | System-written | `TRF-2026.11` |
| `assignment` | `ended_at` | Null on the open row | System-written | Set when the transfer succeeds |
| `assignment` | `reason` | TRANSFER or MANUAL | System-written | LOV-ASSIGN-REASON |
| `assignment` | `rule_id` | Row ID for a rule transfer | System-written | Null for a manual transfer |
| `assignment` | `transfer_reason_code` | R01..R06 | System-written | Required for a manual transfer |
| `processed_event` | `event_id` | Event ID | System-written | Unique; one consumer |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| New, Assigned, In progress, any Waiting | LEGAL_HOLD_PLACED (R-UNI-20) | Placed through the legal-hold endpoint | On hold | `legal_hold = true`; `status_before_hold` set; decision log; `CaseStateChanged` |
| On hold | LEGAL_HOLD_LIFTED (R-UNI-21) | Lifted through the legal-hold endpoint | The status it paused in | `legal_hold = false`; `status_before_hold` cleared; decision log; `CaseStateChanged` |
| Any active status | Rule or manual transfer | A row matches or a manual request is valid | Unchanged | Queue, team and owner change; status and clocks unchanged |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Two transfers on one case in the same second | First commits; second fails the version check and is logged TRANSFER_REJECTED | MSG-GEN-004 |
| X2 | Manual transfer without a reason | 422; nothing changes | MSG-P3-001 |
| X3 | Target owner at the cap | 422; nothing changes | MSG-P3-002 |
| X4 | Closed case | 409; nothing changes | MSG-P3-005 |
| X5 | Decision log write fails | Manual: 503 and rollback. Rule: event retried, case unchanged | MSG-P7-003 |
| X6 | Rule trigger with `legal_hold = true` | No automated transfer; skip logged with R-UNI-20 | None |
| X7 | Duplicate event ID | Second ignored; one transfer; idempotency hit | None |
| X8 | No owner below the cap in the target queue | Case in the target queue's overflow queue with no owner; team manager told | MSG-P3-011 |
| X9 | Hold on a case already on hold | 409; nothing changes | MSG-P3-005 |
| X10 | No transfer row matches | No transfer; no decision log entry | None |
| X11 | Caller lacks Queue and allocation U | 403 before any read or write | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` |
| Existing endpoints changed | `POST /api/recovery/v1/cases/{caseId}/transfer` (API-P3-006) adds required `transferReasonCode` (LOV-TRANSFER-REASON); `POST /api/recovery/v1/cases/{caseId}/legal-hold` (API-P3-007) is delivered in E1 behind the flag. |
| Contract delta | Additive `transferReasonCode` on `TransferRequest`; no field removed. The transfer response remains `Assignment`; the legal-hold response remains `Case`. |
| Backward compatibility | Compatible; the field is required only for a new manual transfer call. |
| Authorization | Queue and allocation U with scope for transfer; Case record U with scope for legal hold. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P3-005 or MSG-GEN-004; 422 MSG-P3-001 or MSG-P3-002; 503 MSG-P7-003. |
| Versioning | No version bump; additive request field. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change; SCR-02 and SCR-03 display the result. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-010, REQ-CWC-016; SPEC-RWB-E1-021-001..020 | New listener, evaluator, transfer service, legal-hold service, dedupe table and index. | Each of the eight triggers; first match and no match; manual reason and cap; closed status; double hold; legal-hold skip; duplicate event; overflow; version conflict; log failure rollback. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `TransferListener` | Listener | Reads the seven trigger event types from the outbox; deduplicates by event ID; calls `transferByRule`. |
| `TransferRuleEvaluator` | Service | Returns the first transfer row in row order for an event and a case snapshot. |
| `TransferService` | Published interface | Lock, hold check, owner choice, decision log, assignment swap, event. |
| `LegalHoldService` | Service | Place and lift with `status_before_hold`. |
| `CaseAndWorkflowController` | Controller | `POST /transfer` and `POST /legal-hold`; access checks; problem responses. |
| `CaseAndWorkflowRepository` | Repository | `recovery_case`, `assignment`, `queue`, `processed_event`. |
| `TransferRuleTable` | Rule table | Rows with `rule_table = TRANSFER` through `RuleTableReader` (P4). |

### Transfer algorithm

1. Receive the event once; insert `processed_event(event_id, consumer)`; a duplicate is an idempotency hit.
2. If `legal_hold = true`, record the skip with R-UNI-20 and stop.
3. Evaluate the transfer rows in force in `row_order`; the first row whose trigger and condition match wins. No match ends the flow with no log.
4. Lock the case by `version`; if the version changed, reject with MSG-GEN-004 and log TRANSFER_REJECTED.
5. Check the move is allowed from the case status; a closed case returns 409 MSG-P3-005.
6. Pick the owner in the target queue through `AssignmentEngine`; if none is below the cap, use the overflow queue and no owner.
7. In one transaction: end the open assignment, insert the new assignment with reason TRANSFER or MANUAL and the rule/reason, update queue, team and owner, write `CaseTransferred`.
8. As the last step before commit, write the decision log entry with the row ID, version, from/to queue and owner, trigger and reason.

### Legal hold

- Place: require reason; if already on hold, 409 MSG-P3-005; set `status_before_hold = status`, `status = ON_HOLD`, `legal_hold = true`; log; publish `CaseStateChanged`.
- Lift: if not on hold, 409; restore `status_before_hold`, clear `legal_hold`; log; publish `CaseStateChanged`.
- A legal hold never stops the timers (R-UNI-20); the clocks keep running.

### Data and migration

- Writes `recovery_case` (`queue_id`, `team_code`, `owner_user_id`, `status`, `legal_hold`, `status_before_hold`, `rule_version`, `version`), `assignment` (end the open row, insert the new row), `processed_event`, `outbox`.
- Update with `WHERE id = ? AND version = ?`; zero rows updated means the version changed (MSG-GEN-004).
- Migration `V021_1__transfer.sql` adds `recovery_case.status_before_hold`, `assignment.transfer_reason_code`, the partial unique index `ux_assignment_open_case ON assignment (case_id) WHERE ended_at IS NULL AND task_id IS NULL`, and `processed_event (event_id uuid primary key, consumer varchar(60), processed_at timestamptz)`.
- No hard-coded trigger, queue or reason values.

### Events

| Event | Payload | When |
|---|---|---|
| `CaseTransferred` (EV-04) | `caseId`, `fromOwner`, `toOwner`, `reasonCode` | After a successful rule or manual transfer |
| `CaseStateChanged` (EV-05) | `caseId`, `fromStatus`, `toStatus`, `eventCode` | Legal hold place or lift |

Consumed: CaseStateChanged (EV-05), DeviationRaised (EV-06), DeviationCleared (EV-07), ApprovalRequested (EV-09), PaymentMissed (EV-12), DocumentStored (EV-16), TimerDue (EV-18).

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-TEAMMGR | Queue and allocation U | Team |
| RW-CAPACITY | Queue and allocation U | All |
| RW-LITOFF and other roles with Case record U | Case record U | Its scope |
| RW-CASEOWN | Queue and allocation R; may not transfer | Own |
| SY-RULES | Rules and parameters R | All |
| SY-CASEWF | Queue and allocation CRU | All |
| SY-DECLOG | Decision log C | All |

### Observability and operations

- Metrics: events consumed; idempotency hits; transfers by trigger; rejections by reason; overflow; hold skips; log failures.
- Alerts: event lag; rejection spike; decision log failure; version conflicts.
- Run book entry under RWB-E1-056.

### Performance

- Target: a rule transfer inside the event consumer's wait; no long transaction across a batch.
- Index `ix_assignment_case_id`; `processed_event` primary key; one transaction per transfer.
- Test the eight triggers and a 500-event replay in SIT.

### Feature flag and rollback

- `rwb.p3.transfer`. Off: no rule transfers; the two endpoints return 404; cases stay as they are.
- Rollback: turn the flag off; the migration is forward-only and the added columns/index remain harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-021-01 | AC1, BR1 | System | Case in TDR-BKK-CO; route R4 approved | LIT-BKK-OFF, owner U-31; old assignment ended; TRANSFER/TRF-007; decision log |
| TC-E1-021-02 | AC2, BR3 | System | Manual transfer with R03 to U-22 | Owner U-22; R03 on assignment and log |
| TC-E1-021-03 | AC3, BR5 | System | Rule and manual transfer on version 7 | One queue; second 409 MSG-GEN-004; TRANSFER_REJECTED logged |
| TC-E1-021-04 | AC4, BR2 | System | Eight trigger rows | Each moves to its target queue; row ID logged |
| TC-E1-021-05 | AC5, BR7 | System | Reassign, place hold, lift hold | U-23 owner; ON_HOLD then IN_PROGRESS; three log entries |
| TC-E1-021-06 | AC6, BR3 | System | No transfer reason | 422 MSG-P3-001; unchanged |
| TC-E1-021-07 | AC7, BR4 | System | U-24 at 150 | 422 MSG-P3-002 naming U-24 |
| TC-E1-021-08 | AC8 | System | CLOSED case | 409 MSG-P3-005 |
| TC-E1-021-09 | AC9, BR9 | System | Decision log down for a manual call | 503 MSG-P7-003; unchanged |
| TC-E1-021-10 | AC10, BR6 | System | `legal_hold = true` and TimerDue | No move; skip logged with R-UNI-20 |
| TC-E1-021-11 | AC11, BR8 | System | Event EVT-88120 twice | One transfer; idempotency hit |
| TC-E1-021-12 | AC12, X8 | System | Every member of LIT-BKK-OFF at 150 | LIT-BKK-OVF, no owner; MSG-P3-011 |
| TC-E1-021-13 | AC13, X9 | System | Hold on a case on hold | 409 MSG-P3-005 |
| TC-E1-021-14 | AC14, X10 | System | DocumentStored with no row | No move; no log |
| TC-E1-021-15 | X11 | Security | RW-CASEOWN calls transfer | 403 MSG-P4-002 |
| TC-E1-021-16 | BR9 | Resilience | Decision log fails for a rule transfer | Event retried; case unchanged |

## Guardrails

- No business value in code: triggers, target queues and the reason list are data.
- No personal data in logs, events, tests or prompts.
- No read of another module's tables: trigger events arrive through the outbox; rule rows through `RuleTableReader` (P4).
- A transfer never resets the stage clock or the prescription date.

## Out of scope

- The transfer screen and queue history on the case (RWB-E2-012, RWB-E2-016).
- Reallocation when an owner leaves or passes the cap (Epic 2, R-UNI-18, R-UNI-19).
- Escalation of a breached timer without moving the case (RWB-E1-028).
- The route decision itself (Epic 4).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR2; SPEC-001 | How is the ROUTE_APPROVED trigger distinguished from a stage change, since both arrive as CaseStateChanged? | Determines the rule match. | `CaseStateChanged` carries `eventCode`; the transfer row matches `event_code = ROUTE_APPROVED`. The other seven triggers are their own event types. | RESOLVED | SPEC-001 |
| CLAR-002 | AC3; SPEC-012 | What stops two transfers leaving the case in two queues? | Determines concurrency. | The case `version` check and the partial unique index on the open assignment; the second call returns MSG-GEN-004. | RESOLVED | SPEC-012 |
| CLAR-003 | BR10; SPEC-013 | Does a transfer restart the stage clock or the prescription timer? | Determines side effects. | No; the status and clocks are unchanged. RWB-E1-028 starts a new SERVICE_LEVEL timer only on the queue/status event it receives. | RESOLVED | SPEC-013 |
| CLAR-004 | AC5, BR7; SPEC-007 | Does lifting a legal hold restore the exact prior status? | Determines `status_before_hold`. | Yes; the status paused in is stored and restored; a double hold or a lift when not on hold is 409. | RESOLVED | SPEC-007 |
| CLAR-005 | API; SPEC-015 | The TSD lists API-P3-006/007 as E2; is delivering them in E1 a contract change? | Determines API impact. | The endpoints are already specified; E1 delivers them behind `rwb.p3.transfer`, and `TransferRequest` gains `transferReasonCode`. No version bump. | RESOLVED | SPEC-015 |
| CLAR-006 | X5; SPEC-009 | Does a rule transfer retry when the decision log fails? | Determines the failure path. | Yes; the event stays in the outbox and is retried. A manual call returns 503 and changes nothing. | RESOLVED | SPEC-009 |
| CLAR-007 | BR3; SPEC-004 | Is a transfer reason required for a rule transfer too? | Determines validation. | No; a rule transfer records reason TRANSFER and the rule ID. `transferReasonCode` is required only for a manual transfer. | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the architecture or the decision
log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; no UI change in this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend transfer engine and legal-hold service; existing transfer and legal-hold contracts extended with transferReasonCode.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: transfer rule engine plus an additive transferReasonCode field]
REQUIREMENT_COVERAGE_SUMMARY: All 10 business rules, 14 acceptance criteria and 11 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 10] [COVERED_RULES: 10] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

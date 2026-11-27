# RWB-P3-E6017-APP Route the population to the committee and schedule it

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E6017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P3-AU |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-S7-E6017-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-017 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P3-E6017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member (RW-WOCOMM)**, I want **the answer that the write-off service sends when it routes a pack to move my case to WITH_COMMITTEE, place it on the committee queue, store the meeting reference and its date and hold that date as a durable timer, while a case with an open deviation is held out of the population and moved to CASE_REMOVED_BY_TEAM**, so that **the committee meets on the date that was booked and no case with an open deviation reaches the committee because a step between the two services was skipped**.

This story owns the case of record and nothing of the write-off. The committee, the write-off pack, the amount, the tax criteria and the committee approval stay with rwb-writeoff (S7); the deviation stays with rwb-deviation (S8). rwb-case applies the routing answer of RWB-S7-E6017-CON, performs the R-WO-11 or the R-WO-06 transition on its own case row, places the case on the committee queue or on the deviation handler's queue, stores the meeting reference and its date, holds the date as a durable timer inside CaseWorkflow, and writes the local decision record in the same transaction as the state change.

### 2. Business rationale

R-WO-11 routes the pack to the committee and schedules the meeting before the scheduled meeting; R-WO-06 holds a case with an open deviation out of the population and routes it to the deviation handler. Both rules are rows of the write-off route set, and both land on facts that belong to the case: its stage, its queue, its meeting and its owner. In the monolith the scan, the route, the case move and the meeting booking were four statements in one process. In the target the scan and the route are rwb-writeoff's and the case, the queue and the timer are rwb-case's, so the answer has to cross one service boundary and be applied exactly once.

The case side is where the failure is visible. If the answer is dropped, the pack is routed and the case stays in PACK_PREPARED: the committee meets on a pack whose case is still in the recovery officer's queue, so two people work the same balance. If the answer is applied twice in one meeting month, the case carries two meeting clocks and the committee meets on the wrong date. If a deviation is raised after the population is proposed and the case side does not read its own `deviation_open` flag, a case under review by a complaint handler is booked into the committee. Each of those is a wrong decision on a charged-off balance, and none of them appears as an error.

The case side is also where the boundary must hold. The meeting belongs to the committee and the write-off record belongs to rwb-writeoff; rwb-case keeps the meeting reference and its date so that a screen, a task and a timer can name the meeting, and keeps nothing else. It reads no write-off row and holds no copy of the pack (DP-01). The date is not a scheduler job: it is a durable timer of CaseWorkflow, so it survives a worker restart and needs no Quartz table and no five-minute check (Temporal and Drools Design v1 slide 14). The case is served on `/api/recovery/case/v1` (DP-13), the screen composes the case and the write-off through the gateway-bff composite route (DP-19), and the decision is written locally and published on `rwb.decision-record.v1` (DP-03).

The P3 side of the legacy story carries no acceptance criterion that can be tested inside one service: the four legacy criteria of RWB-E6-017 describe the route, the deviation hold-out, the decision record and access across S7 and P3. They are proved end to end by RWB-ITG-E6017-ITG and by the S7 slice RWB-S7-E6017-APP; the eight criteria of section 7 are new and test only the case-side deliverable of the title.

### 3. Preconditions

- RWB-S7-E6017-CON is published: the routing-answer resource with the pack reference, the decision, the rule ID, the rule version, the package version and, on a route, the meeting reference and its date; its operation, its error envelope and its contract fake. The operation path and the field names are Not specified in the source documents (GAP-0738; ASM-1331), because that contract story fixes them; this story builds against the contract and its fake and never against a write-off table.
- The `rwb_case` schema baseline and the case of record exist from the Epic 1 case story (RWB-P3-E1018-APP): `recovery_case`, `queue`, `assignment`, `task`, `timer`, the local decision-record table and the outbox, inbox and idempotency objects.
- CaseWorkflow runs one per case on task queue `rwb-case` with the workflow ID equal to the case ID (RWB-P3-E1018-APP), and the workflow kit holds durable timers, so this story adds a timer to it and no workflow, no activity and no Schedule.
- The committee queue row is in force in the rwb-case reference data with role RW-WOCOMM, and the committee-meeting timer type is in force in LOV-TIMER; the committee queue code and the timer type value are Not specified in the source documents (GAP-0738; ASM-1329), because LOV-TIMER holds no committee-meeting row and no list in the sources names the committee queue.
- The deviation handler queue `DEV-HANDLER` exists, the queue that rule R-DEV-01 and the P3 allocation story place a case with an open deviation in.
- Package rows R-WO-11 (PACK_PREPARED, PACK_ROUTED, WITH_COMMITTEE) and R-WO-06 (POPULATION_PROPOSED, CASE_HAS_OPEN_DEVIATION, CASE_REMOVED_BY_TEAM) are in force, and the version in force per environment is named in the routing answer; the write-off route set is evaluated by rwb-writeoff and not by this story.
- `POST /api/recovery/access/v1/authorise` answers the Case record right and the scope, cached by the platform guard library (DP-08).
- The committee meeting calendar, its cadence and its booking target are Not specified in the source documents (GAP-0738; ASM-1328). The meeting reference format, the field IDs of the two new case fields and the requirement IDs of the legacy story are Not specified in the source documents (GAP-0738; ASM-1333).
- No build dependency. Day 1, against the S7 contract fake; the C dependency RWB-S7-E6017-CON never blocks the lane.

### 4. Flow

1. rwb-writeoff routes the pack of the case under R-WO-11 and sends the routing answer to rwb-case through the operation of RWB-S7-E6017-CON: one hop, 2 s timeout and a breaker per downstream (DP-11). The path, the method and the field names are fixed by that contract story, not here.
2. The case router of rwb-case consumes the answer, dedupes it through its inbox on the pack reference and the message key, and starts the committee-routing step for the case. A duplicate never acts twice (R-UNI-40).
3. The step reads the case row of `recovery_case` in `rwb_case` (DP-01): its stage code, which is PACK_PREPARED or POPULATION_PROPOSED, its `deviation_open` flag (DF-CAS-019) and its queue and owner.
4. The step validates the answer: a pack reference and a rule ID are present, MSG-GEN-001 names the field when one is missing, the rule ID is R-WO-11 or R-WO-06, a route answer carries the meeting reference and its date, and the answer names a rule version in force. An answer with no rule version in force is a refusal, `NoPackageInForce` with MSG-P3-027, and the case does not move.
5. A case whose own `deviation_open` flag is true takes the hold-out path, whatever the answer proposes: R-WO-06 moves the case to CASE_REMOVED_BY_TEAM, places it in queue `DEV-HANDLER` for the deviation handler, writes no committee placement and no committee-meeting timer, and records one decision with R-WO-06. The deviation rows themselves stay in `rwb_deviation` with S8 and are never read here.
6. Every other case takes the route path: R-WO-11 moves it to WITH_COMMITTEE, places it on the committee queue with a task for the committee, and stores the meeting reference and its date from the answer.
7. RecordAndApply: in one `rwb_case` transaction the step writes the stage code, the queue and the assignment, the task with its due date, the timer row, `committee_meeting_ref` and `committee_meeting_date`, the local decision record with the rule ID R-WO-11 or R-WO-06 and the rule version in force, and inserts CaseStateChanged (EV-05) and DecisionRecorded in the outbox (DP-03, DP-09). A failed write rolls the whole transaction back, so nothing moves.
8. The step signals CaseWorkflow with the meeting date. CaseWorkflow holds that date as a durable timer of the workflow kit and raises TimerBreached through its own state when the date passes; no Temporal Schedule, no Quartz row and no five-minute timer check is involved.
9. A repeated answer for the same pack reference and the same meeting is ignored by the inbox: no second row, no second placement, no second timer and no second event.
10. Committee member and case owner read: `GET /api/recovery/case/v1/cases/{caseId}` returns the stage code, the queue, `committeeMeetingRef`, `committeeMeetingDate` and the committee-meeting timer; the read is guarded by the Case record right and the scope through `POST /api/recovery/access/v1/authorise`, cached.
11. SCR-27: the gateway-bff composite route calls rwb-case for the case, its queue and the meeting date and rwb-writeoff for the pack state, one hop each, and merges them into the screen model (DP-19); the browser calls one route and no owner service.
12. Nothing of the write-off record, the pack, the amount, the tax criteria, the posting or the committee approval is written or served by rwb-case; those stay S7's and the case answer carries none of them.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same routing answer arrives twice for one pack | The inbox ignores the second answer and records the idempotency hit; no row, no placement, no timer and no event is written twice | None | AC4 |
| X2 | The answer names no rule version in force | `NoPackageInForce` is raised, the case does not move, no placement and no timer is written, and the case goes to the exception queue for role RW-TEAMMGR | MSG-P3-027 | AC5 |
| X3 | The local decision record cannot be written | The transaction rolls back: the stage code, the queue, the meeting reference and the timer do not change, and the answer is retried | MSG-P7-003 | AC6 |
| X4 | The case carries `deviation_open` true while the answer proposes a route to the committee | The flag wins: the hold-out of R-WO-06 is applied, no committee placement is written, and the refusal is recorded with the rule the answer carried | None | AC2 |
| X5 | A route answer carries no meeting reference or no meeting date | The answer is refused, no state changes and the missing field is named | MSG-GEN-001 | AC1 |
| X6 | The rwb-writeoff answer does not arrive within 2 s or the service is unavailable | Nothing moves and the answer is retried by the sender; the case keeps its stage and its queue | None | AC1 |
| X7 | The write-off service reports that the scan is on hold for the missing tax criteria and sends no answer | The case stays where it is and the reason carried by the answer is passed through to the case answer unchanged | MSG-S7-001 | AC8 |
| X8 | A role without the Case record right reads a routed case | Refused; nothing is returned and nothing is written | MSG-P4-002 | AC7 |
| X9 | A case outside the caller's scope is read | Refused as not found; nothing is returned and nothing is written | MSG-P4-003 | AC7 |

X1 is the duplicate-event rule R-UNI-40 and X3 is the no-unlogged-action rule R-UNI-39; both are platform behaviour applied through the inbox and the decision-record library, and neither is caught and turned into a success. The exception of X2 is the same `NoPackageInForce` refusal the embedded kit raises in the services that evaluate a package, and it is never a default move.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the rwb-writeoff contract fake of RWB-S7-E6017-CON, the access contract and the workflow kit; no work order sits inside another team's lane |
| Negotiable | The committee queue, the timer type, the meeting calendar, the warning point, the rule version and the field names are rows, parameters or contract fields; the story fixes the behaviour |
| Valuable | The committee meets on the booked date and no case with an open deviation is booked into it |
| Estimable | One consumer, one routing step, one transaction, one durable timer, one read operation and one panel |
| Small | Fits two weeks with its tests |
| Testable | Each of the eight criteria of section 7 is one automated test, and every cross-service answer is stubbed in the S7 contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Route the population to the committee and schedule it on the case

  Background:
    Given case "RW-2026-000617" is open in the write-off population for cut-off date "2026-07-03"
    Given rule rows R-WO-11 and R-WO-06 are in force with version "WO-2026.07"
    Given the committee queue row is in force in the rwb-case reference data with role "RW-WOCOMM"
    Given the committee meeting calendar holds meeting date "2026-07-15" for meeting month "2026-07"

  Scenario: AC1 A routed pack moves the case to WITH_COMMITTEE and books the meeting (new, D-RCV-60)
    Given case "RW-2026-000617" is in stage "PACK_PREPARED" with deviation_open false
    Given the rwb-writeoff contract mock returns the routing answer of R-WO-11 for pack "PK-2026-07-0617" with meeting reference "WOCMTG-2026-07-15" and meeting date 2026-07-15
    When the committee-routing step applies the answer for case "RW-2026-000617"
    Then the case stage code is "WITH_COMMITTEE" by R-WO-11
    Then the case is placed on the committee queue with a task for the committee and is no longer in the recovery officer's queue
    Then the case holds committee_meeting_ref "WOCMTG-2026-07-15" and committee_meeting_date 2026-07-15
    Then CaseWorkflow holds 2026-07-15 as a durable timer and no Schedule, no Quartz row and no timer-check job is created
    Then one decision record names R-WO-11 and the rule version "WO-2026.07"
    Then the decision record, the state change and the outbox rows of rwb.case.CaseStateChanged.v1 and rwb.decision-record.DecisionRecorded.v1 commit in one rwb_case transaction

  Scenario: AC2 A case with an open deviation is held out of the population (new, D-RCV-60)
    Given case "RW-2026-000617" is in stage "POPULATION_PROPOSED" with deviation_open true
    Given the rwb-writeoff contract mock returns the deviation answer of R-WO-06 for pack "PK-2026-07-0617"
    When the committee-routing step applies the answer for the case
    Then the case stage code is "CASE_REMOVED_BY_TEAM" by R-WO-06
    Then the case is placed in queue "DEV-HANDLER" for the deviation handler
    Then no committee placement and no committee meeting timer is written
    Then one decision record names R-WO-06 and the rule version "WO-2026.07"

  Scenario: AC3 The committee, the meeting and the write-off stay the write-off service's (new, D-RCV-60)
    Given the routing answer of AC1 has been applied to case "RW-2026-000617"
    Then rwb-case holds only the stage code, the queue, committee_meeting_ref and committee_meeting_date
    Then rwb_case holds no rwb_writeoff table and no copy of the pack, and no foreign key crosses into that schema
    When GET /api/recovery/case/v1/cases/{caseId} is served for the case
    Then the answer names no amount, no tax criteria, no posting reference and no committee approval
    Then the step reads no write-off row and calls no write-off read operation beyond the routing answer of the contract

  Scenario: AC4 A repeated routing answer changes nothing (new, D-RCV-60)
    Given the routing answer of R-WO-11 for pack "PK-2026-07-0617" has been applied to case "RW-2026-000617"
    When the same answer arrives again with the same pack reference and the same meeting
    Then the inbox dedupes it on the pack reference and the message key
    Then no second queue placement, no second task, no second timer row and no second decision record is written
    Then no second CaseStateChanged event is published and the case stays in "WITH_COMMITTEE"

  Scenario: AC5 No rule version in force refuses the routing answer (new, D-RCV-60)
    Given case "RW-2026-000617" is in stage "PACK_PREPARED"
    Given the rwb-writeoff contract mock returns a routing answer of R-WO-11 that names no rule version in force
    When the committee-routing step applies the answer for the case
    Then NoPackageInForce is raised with MSG-P3-027 for rule "R-WO-11"
    Then the case stays in "PACK_PREPARED" and no queue placement and no committee meeting timer is written
    Then no decision record is written and the case is placed in the exception queue for role "RW-TEAMMGR"

  Scenario: AC6 A routing that cannot be recorded does not move the case (new, D-RCV-60)
    Given the local decision-record store is unavailable
    When the routing answer of R-WO-11 arrives for case "RW-2026-000617"
    Then the stage code, the queue, committee_meeting_ref and committee_meeting_date do not change
    Then no CaseStateChanged event is published and the user sees MSG-P7-003
    Then the retried answer writes one decision record and one state change

  Scenario: AC7 The case read is refused without the right or outside the scope (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /api/recovery/case/v1/cases/{caseId} for a case routed to the committee
    Then the call is refused with status 403 and MSG-P4-002
    Given a case owner whose scope is "Own" and a case owned by another person
    When the case owner calls the same operation for it
    Then the response is 404 with message MSG-P4-003
    Then the read writes nothing and raises no event

  Scenario: AC8 SCR-27 shows the write-off state, the committee queue and the meeting date (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-27 for case "RW-2026-000617"
    Given the case is in "WITH_COMMITTEE" on the committee queue with meeting date 2026-07-15
    When the write-off committee member opens SCR-27
    Then the screen shows the state "In committee", the committee queue and the meeting date 2026-07-15
    And the browser calls one composite route and no owner service directly
    Then the screen is read only: it offers no routing action, no meeting change and no committee decision
    Then the amount, the tax criteria and the posting stay with the write-off service and are not served by rwb-case
```

AC1 to AC8 are new for the rwb-case slice: the four legacy criteria of RWB-E6-017 are proved end to end by RWB-ITG-E6017-ITG and by the S7 slice RWB-S7-E6017-APP, so this story owns no legacy criterion and copies none. The rule version label "WO-2026.07", the pack and meeting references and the case ID are synthetic test fixtures of the same kind as the legacy "SYN" values; the version in force, the meeting reference and its date of a real case come from the S7 routing answer (GAP-0738; ASM-1335).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | When the amount is inside the write-off committee limit, the pack is routed to the committee and the meeting is scheduled before the scheduled meeting, and the case moves from PACK_PREPARED to WITH_COMMITTEE | R-WO-11 |
| BR2 | A case with an open deviation in X1 to X7 is held out of the population, routed to the deviation handler and moved from POPULATION_PROPOSED to CASE_REMOVED_BY_TEAM | R-WO-06 |
| BR3 | The case stage, the queue, the task and the timer are rwb-case's and are never written by the caller that routes the pack | Architecture v5 slide 41 (P3 owns case, CMMN state, queues, tasks, allocation, timers); DP-01 |
| BR4 | The committee, the write-off pack, the amount, the tax criteria and the committee approval are rwb-writeoff's; rwb-case holds the meeting reference and its date and nothing of the write-off record | Architecture v5 slide 41 (S7 owns eligibility, committee, posting, recovery after charge-off); slide 20 S7 DB line |
| BR5 | The case's own `deviation_open` flag drives the hold-out, so a deviation raised after the population is proposed still keeps the case out of the committee | DF-CAS-019; R-WO-06 |
| BR6 | A route answer must name the rule ID, a rule version in force, the meeting reference and its date; an answer with no version in force is refused as NoPackageInForce and no state changes | D-RCV-36 T7 (no package in force is a refusal); MSG-P3-027 |
| BR7 | The booking is held as a durable timer of CaseWorkflow, not as a Temporal Schedule, a Quartz job or a five-minute check, so the meeting date survives a worker restart | Temporal and Drools Design v1 slide 14; Architecture v5 slide 44 |
| BR8 | The decision record, the state change and the outbox rows are one transaction: a decision that cannot be recorded does not proceed | Principle 5; R-UNI-39; DP-03 |
| BR9 | The same answer arriving twice writes no row and raises no event a second time | R-UNI-40 |
| BR10 | The routing step names the rule ID and the rule version on every decision record; the rule ID and the version arrive in the answer and are never written in code | R-WO-11; R-WO-06; DF-REF-001 to DF-REF-015 |
| BR11 | The stage move and the queue placement are one move: a case is never on the committee queue in one stage and off it in the next | R-WO-11; R-WO-06; P3 queue ownership |
| BR12 | The read of a case is guarded by the Case record right and the scope, and a read writes nothing | DP-08; MSG-P4-002; MSG-P4-003 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PACK_PREPARED | PACK_ROUTED | The amount is inside the committee limit, the answer names R-WO-11 and a meeting date, and `deviation_open` is false | WITH_COMMITTEE |
| POPULATION_PROPOSED | CASE_HAS_OPEN_DEVIATION | `deviation_open` is true and the answer names R-WO-06 | CASE_REMOVED_BY_TEAM |
| PACK_PREPARED | The answer names no rule version in force | NoPackageInForce | PACK_PREPARED, unchanged |
| PACK_PREPARED | The decision record cannot be written | The transaction rolls back | PACK_PREPARED, unchanged |

These are the case stage code of `recovery_case` (`stage_code`, in the range DF-CAS-001 to DF-CAS-023); the case status stays IN_PROGRESS through both moves. The story also writes `committee_meeting_ref` and `committee_meeting_date`, which are facts of the meeting booking and not stages. A case on the hold-out path is returned to the next monthly scan by R-WO-08 once the deviation is cleared, and that return is rwb-writeoff's scan and not this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Applies the routing answer, moves the stage, places the case on the committee queue or on `DEV-HANDLER`, writes the task, the timer, the meeting reference and the decision record |
| CaseWorkflow | Holds the committee-meeting durable timer and raises TimerBreached through its own state; moves no stage by itself |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |
| RW-WOCOMM, write-off committee member | Reads the committee queue, the case and the meeting date (Case record R) |
| RW-WRITEOFF, write-off team | Runs the scan and the route in rwb-writeoff; reads the case and its stage (Case record R) |
| RW-CREDITAD, RW-PRODHEAD, RW-FINANCE | Hold the committee decision (Write-off and posting A); they read the case and take the decision in the write-off service, not here |
| RW-TEAMMGR, team manager | Receives the case in the exception queue on the no-package path (Case record R) |
| RW-COE | Owns the committee queue row, the committee-meeting timer type and the meeting calendar as reference data |
| RW-REFADM | Holds no Case record right; refused on the case read with MSG-P4-002 |

The committee decision itself, the Write-off and posting A right and the DoA limit are answered in rwb-writeoff and are outside this story.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and the rest of the range | Read, and `stage_code`, `queue_id` and `owner_user_id` written with the move |
| DF-CAS-019 | recovery_case | deviation_open | Read, decides the hold-out and the refusal |
| Not specified in the source documents (GAP-0738; ASM-1333) | recovery_case | committee_meeting_ref, committee_meeting_date (two new fields, no field ID in the Logical Data Model v8) | Write |
| DF-WRK-001 to DF-WRK-008 | queue | id, queue_code, queue_name, team_code, role_code, assignment_method and the rest of the range | Read, for the committee queue and `DEV-HANDLER` |
| DF-WRK-018, DF-WRK-019, DF-WRK-024 | task | case_id, task_code, due_at | Write, the committee task of the booking |
| DF-WRK-030, DF-WRK-031, DF-WRK-032, DF-WRK-035 | timer | timer_type, started_at, expires_at, status | Write, the projection of the meeting date behind the timers read; the clock is the durable timer |
| DF-CAS-036 to DF-CAS-045 | deviation (rwb_deviation, owner S8) | id, case_id, deviation_code, raised_at, raised_by, paused_state and the rest of the range | Not read and not written: the case's own `deviation_open` flag stands in, and the rows are S8's |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | all fields | Write locally; the central entry is sealed by rwb-decision |
| DF-REF-001 to DF-REF-015 | rule_row (rwb_decision, owner P7) | rule_id, rule_version, from_state, event_code, to_state and the rest of the range | Not read here: the rule ID and the rule version arrive in the routing answer |

Field IDs are those in the Logical Data Model and Data Dictionary v9. `deviation`, `write_off` (with its `committee_date`, DF-FIN-015), `rule_row` and `decision_log_entry` are other services' tables and are not read or written directly; `rwb_case` holds no foreign key into another schema (DP-01). The committee meeting reference and its date are the only facts of the committee that rwb-case keeps, and the amount, the tax criteria and the posting are never copied.

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no operation: the case of record is served by the existing `GET /api/recovery/case/v1/cases/{caseId}` and the queue by the existing `GET /api/recovery/case/v1/queues/{queueId}/cases` of rwb-case, both extended only by the optional fields `committeeMeetingRef`, `committeeMeetingDate` and `stageCode` on the Case resource, which the Epic 1 contract already carries.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| Not specified in the source documents (GAP-0738; ASM-1331) | Not specified in the source documents (GAP-0738; ASM-1331) | rwb-writeoff (S7) | The committee routing answer of RWB-S7-E6017-CON: pack reference, decision, rule ID R-WO-11 or R-WO-06, rule version, package version and, on a route, the meeting reference and its date (DP-11, built against the RWB-S7-E6017-CON fake) | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | The Case record right and the scope before a case read, cached by the guard library (DP-08) | One hop, 2 s |

Two calls, no chain. The rwb-case side is called by rwb-writeoff and makes no call back, so a route never becomes a cycle of two services. The path and the field names of the first row are fixed by the S7 contract story and not by this one.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 | caseId | caseId, fromStageCode, toStageCode, eventCode (PACK_ROUTED or CASE_HAS_OPEN_DEVIATION), ruleId, ruleVersion, packRef, meetingRef |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | caseId | decision record reference, rule ID R-WO-11 or R-WO-06, rule version, business date |

Both are written to the outbox in the same transaction as the stage change and relayed with the CloudEvents envelope; no personal data is carried and no amount is in any payload (DP-09).

#### 12.4 Events consumed

None. The routing answer arrives as a call of the S7 contract and is not a Kafka subscription of this story: `DeviationRaised` and `DeviationCleared` are consumed by the case router of the Epic 1 and Epic 2 stories into the `deviation_open` flag, and this story reads the flag and subscribes to nothing.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Receives the meeting date and other state signals and holds the committee-meeting date as a durable timer of the workflow kit |
| CommitteeRoutingStep | Step of the case router | `rwb-case` | Validates the answer, chooses R-WO-11 or R-WO-06, records and applies, and signals CaseWorkflow |
| RecordAndApply | Transactional step (decision-record library) | `rwb-case` | Writes the stage, the queue, the task, the timer, the meeting reference, the decision record and the outbox rows in one transaction |

No other activity is added, and no child workflow: the committee approval child of the write-off stage belongs to rwb-writeoff.

#### 12.6 Schedules

None added by this story. The meeting date is a durable timer of CaseWorkflow and not a Temporal Schedule, because a booking is one date for one case and not a cadence; no Schedule, no Quartz row and no timer-check job is created. The monthly eligibility scan JOB-16 stays a Temporal Schedule in rwb-writeoff (monthly, third working day), and the committee meeting calendar stays the write-off service's. Whether a committee meeting cadence should also be a Schedule is Not specified in the source documents (GAP-0738; ASM-1328).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | The story writes `stage_code`, `queue_id` and `owner_user_id` on the move and adds `committee_meeting_ref` and `committee_meeting_date` |
| queue, assignment | P3 (rwb_case) | The placement on the committee queue and on `DEV-HANDLER` |
| task | P3 (rwb_case) | The committee task with its `task_code` and `due_at` |
| timer | P3 (rwb_case) | The projection of the meeting date behind the timers read; the clock is the durable timer of CaseWorkflow |
| decision_record | PLT library, created in rwb_case | The local record of the routing decision, hash-linked, written in the same transaction (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |

`write_off` is S7's (rwb_writeoff) and `deviation` is S8's (rwb_deviation): this story holds no foreign key into either schema, no cross-schema join and no copy of a row (DP-01). `decision_log_entry` and `rule_row` are rwb-decision's and are reached only through its contracts.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-writeoff WireMock | The S7 contract of RWB-S7-E6017-CON | The routing answer of R-WO-11 with pack "PK-2026-07-0617", meeting reference "WOCMTG-2026-07-15" and meeting date 2026-07-15; the open-deviation answer of R-WO-06; an answer with no rule version in force; an answer with no meeting reference; a delayed answer beyond 2 s; an unreadable answer |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing it for RW-REFADM, and excluding a case from an Own scope |
| gateway-bff composite route (WireMock) | The DP-19 route of SCR-27 | The merged screen model of AC8: the stage, the committee queue, the meeting date and the write-off state of the pack |
| Committee and deviation queue fixture | The rwb-case reference data | The committee queue row with role RW-WOCOMM, whose code comes from the reference-data fixture and not from code, and queue `DEV-HANDLER`; the wave 4 integration run uses its own fixture code for the same queue |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 2 consumed | The S7 routing answer and the P4 authorise consumed; one hop, 2 s, breaker per downstream |
| Kafka | 2 published, none consumed | `rwb.case.events.v1` and `rwb.decision-record.v1` published through the outbox |
| Temporal | 1 workflow | CaseWorkflow, extended with the committee-meeting durable timer; two steps and no child workflow |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `committeerouting`, Java package `th.co.scb.ace.workbench.recovery.case.committeerouting`; front end `src/modules/recovery/case/CommitteeRoutingPanel.tsx`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | The monolith base path of the legacy API (Template and Rules §R5.5, DP-13) | `/api/recovery/case/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The two H dependencies this table adds are held by the platform contract stories and are not repeated in the metadata rows, which carry only the contract dependency of the legacy route: RWB-S7-E6017-CON (ASM-1330). The committee queue row, the timer type and the meeting calendar are reference data of rwb-case and are read as rows, not as code (ASM-1329).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RoutingAnswerController | Controller | The rwb-case side of the S7 contract: accepts the routing answer, applies the access check of the caller identity and hands it to the step |
| RoutingAnswerValidator | Service | Checks the pack reference, the rule ID, the rule version in force and, on a route, the meeting reference and its date; refuses with NoPackageInForce, MSG-P3-027 or MSG-GEN-001 |
| CommitteeRoutingStep | Step of the case router | Reads the case, chooses R-WO-11 or R-WO-06 from the answer and the `deviation_open` flag, and drives the record and the apply |
| CaseStageRepository | Repository | Writes `stage_code`, `queue_id`, `owner_user_id`, `committee_meeting_ref` and `committee_meeting_date` in schema rwb_case only |
| CommitteeQueuePlacer | Service | Places the case on the committee queue or on `DEV-HANDLER` and writes the task with its due date; holds no queue code in code |
| MeetingTimerWriter | Service | Writes the timer projection row and signals CaseWorkflow with the meeting date |
| DecisionRecordWriter | Library adapter | Writes the local decision record with the rule ID and the rule version, hash-linked, in the same transaction (DP-03) |
| InboxDedupe | Library adapter | Dedupes the answer on the pack reference and the message key (DP-09) |
| CaseCommitteePanel | React component | Shows the stage, the committee queue and the meeting date on SCR-27, read only |

**Database and migrations**

- Migration `V6017_1__committee_meeting.sql` adds `committee_meeting_ref` varchar(40) and `committee_meeting_date` date to `recovery_case` and one reference row type for the committee-meeting timer in LOV-TIMER; no database check constraint holds a list value.
- No new table: the queue, the assignment, the task, the timer, the decision record and the library objects already exist in `rwb_case`.
- One index for the read: `ix_recovery_case_stage_committee ON recovery_case (stage_code) WHERE stage_code = 'WITH_COMMITTEE'`, so the committee queue page is read without a scan.
- The migration runs in the rwb-case Flyway sequence of the service's own schema; no other schema is touched (DP-01).

**Configuration and reference data**

- The committee queue row (RW-COE) with role RW-WOCOMM, and the committee-meeting timer type in LOV-TIMER; the code and the value are Not specified in the source documents (GAP-0738; ASM-1329).
- The deviation handler queue `DEV-HANDLER`, from the P3 queue template and rule R-DEV-01.
- The committee meeting calendar rows (meeting month, meeting date, meeting reference), read as data by rwb-writeoff and carried in the routing answer; rwb-case stores the reference and the date it is given and holds no calendar.
- The rule version in force per environment is the one named in the routing answer; rwb-case holds no package and evaluates no rule, so no KieBase and no lock file is involved.

**Build steps**

1. RoutingAnswerController and RoutingAnswerValidator against the S7 contract fake, with the refusal of the no-version path; tests for AC1 and AC5.
2. InboxDedupe on the pack reference and the message key; test for AC4.
3. CaseStageRepository and CommitteeQueuePlacer with the committee queue and `DEV-HANDLER`, one transaction with the decision record; tests for AC1 and AC2.
4. MeetingTimerWriter, the timer row and the CaseWorkflow signal; test for AC1 and the no-Schedule assertion.
5. The hold-out path from the `deviation_open` flag, including the case where the answer proposes a route; tests for AC2 and AC3.
6. The failed decision-record write and the rollback; tests for AC6 and the NFR case.
7. The read path with the access guard and the scope, and the composite-route contract test of SCR-27; tests for AC7 and AC8.
8. Contract-fake run of every S7 answer in isolation, so the story builds before rwb-writeoff lands.

**Feature switch.** `rwb.p3.committee-routing`, a service configuration value read as a parameter. Off: the answer is stored as a pending inbox entry, no stage moves and no placement is written; on: the routing step applies the answer.

**Done when.** The tests in section 16 pass, the S7 contract tests stay green, every routed case carries exactly one meeting reference, one meeting date and one committee-meeting timer, and no case in the SIT run with an open deviation has reached WITH_COMMITTEE.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The write-off service reports that the scan is on hold for the missing tax criteria and sends no routing answer | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | The routing answer carries no pack reference, no rule ID, or no meeting reference on a route | Enter {field}. |
| MSG-P3-027 | The routing answer names no rule version in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The local decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the Case record right reads a routed case | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the caller's scope | This case is not in your scope. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the rule ID "R-WO-11" and the business date only, never a case fact. For MSG-GEN-001, {field} is the name of the field the answer left empty, such as "packRef" or "meetingRef". MSG-S7-001 is rwb-writeoff's message and this story passes it through unchanged; it owns none of these texts.

### 15. Screens and states

SCR-27 Write-off proposal, states Scan, proposed, in committee and approved: this story serves the case-side facts of that screen, which are the stage code, the committee queue and the meeting reference with its date, and it serves them read only. The amount, the tax criteria, the posting reference and the committee approval are read from rwb-writeoff on the same composite route.

SCR-27 is composed by the gateway-bff composite route, which calls rwb-case and rwb-writeoff in parallel, one hop each, and merges the answers into the screen model (DP-19); the browser calls one route and no owner service. The screen field order, the masking and the merge order are Not specified in the source documents (GAP-0738; ASM-1334). The full write-off screen, its buttons and the committee decision remain with RWB-S7-E6017-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-017-01 | AC1, AC3, AC8 | Component | S7 stub routes pack PK-2026-07-0617 with meeting WOCMTG-2026-07-15 and date 2026-07-15 |
| TC-E6-017-02 | AC1, AC5 | Component | S7 stub returns an answer of R-WO-11 with no rule version in force on 2026-07-03 |
| TC-E6-017-03 | AC2, AC4 | Component | Case in POPULATION_PROPOSED with `deviation_open` true, and the same answer delivered twice |
| TC-E6-017-04 | AC6 | Component | Decision-record store stopped on the R-WO-11 route |
| TC-E6-017-05 | AC7 | Component | RW-REFADM without the Case record right calls the case read; refused with MSG-P4-002 |
| TC-E6-017-06 | AC6 | NFR | Decision-record write forced to fail on the R-WO-11 route; stage, queue and meeting date unchanged |

The legacy levels map System to Component, Access to Component and Resilience to NFR, because the cross-service behaviour of this key is proved by RWB-ITG-E6017-ITG. The `-ITG` copy of each case is held by RWB-ITG-E6017-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the committee queue code, the timer type, the meeting calendar, the rule ID and the rule version are rows, reference data or contract fields.
- No personal data in logs, tests, workflow history or prompts: logs hold case IDs, pack references and meeting references, never account numbers, names or identity numbers; the workflow payloads pass the payload codec.
- No read of another service's tables and no ACE view: the routing answer comes from the S7 contract, the rights from rwb-access, and `rwb_case` holds no foreign key into another schema (DP-01).
- The committee decision, the amount, the tax criteria and the posting are not stored, echoed or validated by rwb-case.
- A read of a routed case writes nothing and raises no event.
- The decision record is written before the stage moves, in one transaction with it; a failed write rolls the whole move back (R-UNI-39).
- NoPackageInForce is never caught and turned into a default move; the case goes to the exception queue.
- The meeting date is a durable timer and not a Schedule; no Quartz row and no timer-check job is added.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only (DP-09).

### 18. Traceability

The Epics 3 to 8 story RWB-E6-017 carries no requirement ID, so this story claims none (GAP-0738; ASM-1332). The trace goes through the legacy feature, the two rules that the story applies and the test cases it holds.

| Requirement ID | Requirement (short) | Source section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (the legacy story carries no requirement ID) | Route the population to the committee and schedule it | Recovery Workbench User Stories Epics 3 to 8 v4, RWB-E6-017, lines 9829 to 9924 | FEAT-WOF-05 | 9 Write-off (D9) | R-WO-11 | TC-E6-017-01, TC-E6-017-02, TC-E6-017-05 |
| None (the legacy story carries no requirement ID) | Hold a case with an open deviation out of the population | The same, AC3 and the data block of RWB-E6-017 | FEAT-WOF-05 | 9 Write-off (D9) | R-WO-06 | TC-E6-017-03 |
| D-RCV-60 DP-01 | The case, the queue and the timer are rwb-case's; the committee and the write-off are rwb-writeoff's, with no cross-schema read | Template and Rules §R5.5; Architecture v5 slide 41 | FEAT-WOF-05 | 9 Write-off (D9) | R-WO-11; R-WO-06 | TC-E6-017-01, TC-E6-017-04 |
| D-RCV-60 DP-03 | The decision is recorded locally in the same transaction and published on `rwb.decision-record.v1` | Template and Rules §R5.5; Architecture v5 slide 20 | FEAT-WOF-05 | 9 Write-off (D9) | R-WO-11; R-WO-06; R-UNI-39 | TC-E6-017-01, TC-E6-017-04, TC-E6-017-06 |
| D-RCV-60 DP-19 | SCR-27 is a gateway-bff composite route over rwb-case and rwb-writeoff, read only | Template and Rules §R5.5; Architecture v5 slide 20 | FEAT-WOF-05 | 9 Write-off (D9) | R-WO-11 | TC-E6-017-01, TC-E6-017-05 |

The legacy endpoints of RWB-E6-017 (`POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` and `POST /api/recovery/writeoff/v1/write-off-scans`) are rwb-writeoff's and are not re-published here; this story provides no write operation of its own. The six legacy test cases are copied in section 16 in their legacy order, and the four legacy criteria are proved by RWB-ITG-E6017-ITG and RWB-S7-E6017-APP.

### 19. Out of scope

- The scan, the eligibility rules, the tax criteria, the pack build and the route itself, and the S7 side of the contract (RWB-S7-E6017-CON, RWB-S7-E6017-APP).
- The committee decision, the DoA limit, the posting to ALS and GL and the provision release that follow it.
- The write-off record and its `committee_date`: rwb-writeoff's table, with no read operation published for it.
- The deviation records, the screening, the pause and the resume (rwb-deviation, S8) and the clearing that returns a removed case to the next scan.
- The committee meeting calendar, its cadence and its booking target.
- The four legacy acceptance criteria of RWB-E6-017, which stay with the S7 slice and the integration proof.
- The editable states of SCR-27: the routing buttons, the meeting change and the committee decision (RWB-S7-E6017-APP).
- The full case record view and the timer and deviation sections (RWB-P3-E1023-APP, RWB-P3-E2015-APP).
- The deployment of this capability: chart values, queue and topic provisioning, dashboards and the runbook.

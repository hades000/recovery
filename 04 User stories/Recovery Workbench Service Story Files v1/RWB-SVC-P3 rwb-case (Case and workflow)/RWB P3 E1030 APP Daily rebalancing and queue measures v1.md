# RWB-P3-E1030-APP Daily rebalancing and queue measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1030-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1020-APP |
| Depends on (build) | RWB-P3-E1030-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1020-APP, RWB-P3-E1028-CON |
| Contract dependencies | RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P3-E1030-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-017, FR-P3-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-030 for rwb-case. The daily rebalance keeps its selection, its cap rule, its hold checks and its measure snapshot, and moves three mechanisms: the Quartz start becomes a Temporal Schedule, the decision log write becomes the local decision record on `rwb.decision-record.v1`, and the data-lake extract of the snapshot is removed under DP-17. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a daily run that assigns unassigned cases and moves the newest cases off owners above the cap by the assignment rules, and queue counts, ageing and service level breaches published to Power BI**, so that **queues stay balanced and every team manager sees the same numbers as the case list**.

Inside `rwb-case` this is the rebalancing and measure capability of the case service:

- Service `rwb-case`, schema `rwb_case`, REST base `/api/recovery/case/v1`, topic `rwb.case.events.v1` with event names `rwb.case.<Event>.v1`, Temporal task queue `rwb-case` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.case`.
- The run is a step of the `DailyCaseRun` workflow on queue `rwb-case`, started by the Schedule `rwb-case-rebalance-daily` at 06:30. The allocation step runs first, so the rebalance always sees an allocated caseload for the business date.
- The run consists of two activities: `rebalance` (select, move, record) and `takeQueueMeasures` (snapshot, reconcile, publish). Each case's move, its decision record and its outbox row commit in one transaction.
- The decision record is written locally by the decision-record library of DP-03 and published on `rwb.decision-record.v1`; `rwb-decision` collects it into the central ledger. This story no longer writes another module's decision log table.
- The owner choice is the assignment engine of RWB-P3-E1020-APP, called in process inside the same service. No rule package is evaluated: the method, the cap and the member capacity are rows of `rwb_case.queue` and `rwb_case.queue_member` (DP-01, DP-07).

The legacy behaviour is unchanged: the same trigger time, the same selection order (newest first, R-UNI-19), the same hold and legal-hold skips, the same owner choice by lowest load with the cap, the same reason REBALANCE, the same `CaseTransferred` event per move, the same measure fields, the same zero-difference reconciliation rule, and the same five messages.

### 2. Business rationale

Team managers rebalance work by hand today and count queues from spreadsheets that do not match. This story moves cases left in overflow or without an owner each morning, takes owners above the cap back inside it (R-UNI-19), and publishes depth, ageing, owner spread and breaches as one snapshot that reconciles to the case list. It meets REQ-CWC-015 and REQ-RDF-012.

The realignment changes three mechanisms and no business rule:

1. **Start.** The Quartz trigger of JOB-06 becomes the Temporal Schedule `rwb-case-rebalance-daily` (DP-10) feeding the existing `DailyCaseRun` workflow. The 06:30 time and the "after the allocation for the business date" order are kept, the latter by the step order inside one workflow run rather than by a job dependency.
2. **Record.** The decision log write becomes the decision record of the platform library, written in the same transaction as the move and published on `rwb.decision-record.v1` for the central ledger. A case whose record cannot be written is not moved, as before (principle 5, R-UNI-39).
3. **Measures.** There is no data lake in Arch v5 (DP-17): the nightly JOB-15 copy of the snapshot and the INT-19 and INT-20 outbound batch are removed, and no file leaves the service. The snapshot row stays in `rwb_case.queue_measure` and is served to the case-side screens by `GET /queues`; `rwb-reporting` builds its own queue, ageing and breach measures from the events into its projection. The measure definitions remain the business owner's (REQ-RDF-012, RW-COE).

The published Java interface `QueueMeasureService` of the monolith was read in process by P9. With no data lake there is no cross-service consumer left for it, so the interface disappears and no contract of another service is consumed (DP-11 row, DP-17 row).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P3-E1030-CON | The published read contract and its fake: the queue measure read, the case read used by the reconciliation, and the `CaseTransferred` message (DP-11) |
| RWB-P3-E1020-APP | The assignment engine: lowest load, the member list order and the cap check |
| RWB-P3-E1028-CON | The timer contract: `TimerBreached` is raised by the durable timer inside this service, and the expired `SERVICE_LEVEL` timers of a queue are readable |
| RWB-PLT-E1027-CON | The decision-record library and `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client and `rwb-case`'s own reference-data contract (DP-07) |
| RWB-PLT-TE006-CON | Outbox, inbox and idempotency library (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit: `DailyCaseRun`, Schedules, activity registration and retry policy (DP-10) |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON | Topic naming library (DP-14) and the per-service Flyway sequence (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that serves the case list and the queue reads (DP-19) |

Business preconditions carried from RWB-E1-030:

- Caseload caps are loaded in `rwb_case.queue.capacity_cap` and `rwb_case.queue_member.capacity` (DL23). A queue with no cap is reported and moves nothing (AC5).
- The queues, their assignment method and their member order are rows in force; queue `TDR-BKK-CO` is `LOWEST_LOAD` with cap 150 in the tests.
- `GET /cases` with the queue filter is served for the business date, so the reconciliation can compare a snapshot depth with the case list count at the same time.
- Hold and legal-hold flags on the case are current: a case with `deviation_open` or `legal_hold` true is not moved (AC8).

The delivery path of the alert messages MSG-P3-028 and MSG-P3-011 and of MSG-P3-029 is Not specified in the source documents (GAP-2205; ASM-3621).

### 4. Flow

1. Schedule `rwb-case-rebalance-daily` fires at 06:30 and starts `DailyCaseRun` for the business date. The allocation step runs first; the rebalance step therefore starts when the allocation for the date is complete, which is the legacy "06:30, or when JOB-03 completes if that is later" (R-UNI-19 start condition unchanged).
2. `rebalance` activity: lists, per queue in the run's scope, the cases with no owner and status NEW or ASSIGNED, the owners whose open cases exceed their capacity, the member list with capacity, and the `SERVICE_LEVEL` timers in `EXPIRED`.
3. `rebalance`: for each owner above the cap, selects the newest cases by assignment time until the owner is inside the cap (R-UNI-19). An owner exactly at the cap loses no case (AC10); a queue with no cap moves nothing and is still reported (AC5).
4. `rebalance`: skips cases with `deviation_open` or `legal_hold` true and takes the next newest instead (AC8).
5. `rebalance`: asks the assignment engine for an owner below the cap in the same queue for each selected or unassigned case, by the queue's method; when no member has capacity the cases keep no owner and are counted for MSG-P3-011 (AC4).
6. `rebalance`: per case, one transaction — the decision record (reason REBALANCE, the queue and owner identifiers, the rule reference of the queue's assignment row, the idempotency key of case and business date), the end of the old assignment, the new assignment with reason REBALANCE, `recovery_case.owner_user_id`, and the outbox row of `rwb.case.CaseTransferred.v1`. A case whose record cannot be written is left where it is, named in the activity's result with MSG-P7-003, and the run continues (AC6). The activity result is the run record; no other artifact holds the failed-case list, and the legacy job monitor is retired (GAP-2205; ASM-3622).
7. `takeQueueMeasures`: at the end of the run, one snapshot per queue in one REPEATABLE READ transaction: depth, unassigned, age in days from the entry date, owner minimum and maximum, and the count of `SERVICE_LEVEL` timers `EXPIRED`. The snapshot is written with status `TAKEN`.
8. `takeQueueMeasures`: compares each queue's depth with the case list count for the same queue read at the same time. When every queue matches with zero difference the snapshot moves to `PUBLISHED`; a difference holds it at `HELD`, publishes nothing for that queue, and names the check for the data steward with MSG-P3-029 (AC9).
9. `publishBreachAlert`: on `rwb.case.TimerBreached.v1`, sends the team manager of the queue's team MSG-P3-028 with the queue's breach count, and the next snapshot carries that count for the queue (AC3). The case does not move (R-UNI-30).
10. A second run on the same business date finds balanced queues: no case is selected, no decision record is written (AC7). The snapshot of the second run is a new row for its own as-of time.
11. Reporting: `rwb-reporting` builds the queue, ageing and breach measures from the events into its projection; this story publishes no measure feed and writes no file (DP-17). The replacement of the lake copy is Not specified in the source documents (GAP-2205; ASM-3620).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No member of the queue has capacity | Cases stay where they are; counted in the summary | MSG-P3-011 | AC4 |
| X2 | No caseload cap is loaded for the queue | The queue is reported and nothing is moved | None | AC5 |
| X3 | Decision record write fails for a case | That case is not moved; the run continues | MSG-P7-003 | AC6 |
| X4 | The run fires again the same day | Already balanced queues give no further moves | None | AC7 |
| X5 | A case has an open deviation or a legal hold | Not moved | None | AC8 |
| X6 | The snapshot depth differs from the case count | Snapshot not published; break listed for the data steward | MSG-P3-029 | AC9 |
| X7 | An owner holds exactly the cap | No case is moved off them | None | AC10 |
| X8 | A role without Platform administration U triggers the Schedule | Refused with 403 | MSG-P4-002 | Access test TC-E1-030-11 |

Two target-service paths:

- A move whose transaction fails after the decision record is written cannot happen: the record, the assignment swap and the outbox row commit together or not at all (R-UNI-39).
- The run stops if the snapshot transaction cannot be opened; the workflow retries the activity with the kit's policy, and a snapshot already written for the same queue and as-of time is not written twice (unique key of `queue_measure`).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the assignment engine, the timer contract, the decision-record library, the workflow kit and the contract of this key; no screen is built |
| Negotiable | Caps, methods, member order and measure definitions are data |
| Valuable | Removes daily hand rebalancing and gives one set of queue numbers |
| Estimable | One workflow step, two activities, one table, one read |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures

  Background:
    Given queue "TDR-BKK-CO" uses "LOWEST_LOAD" with cap 150
    Given the business date is 2026-12-02

  Scenario: AC1 Rebalance (legacy RWB-E1-030 AC1)
    Given queue "TDR-BKK-CO" has 12 cases with no owner
    Given members U-61 and U-62 hold 140 and 144 open cases
    Given the rwb-decision contract mock returns a decision record accepted for each move
    When JOB-06 runs
    Then the system assigns the 12 cases , 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list
    Then each assignment has reason "REBALANCE" and a decision log entry

  Scenario: AC2 Measures reconcile (legacy RWB-E1-030 AC2)
    Given the snapshot taken at 2026-12-02 06:52
    When the queue report refreshes
    Then the depth of each queue equals the case list count for that queue at 06:52
    Then queue "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days

  Scenario: AC3 Breach alert (legacy RWB-E1-030 AC3)
    Given case RW-2026-000501 in queue "TDR-BKK-CO" passes its service level
    When the timer check raises the breach
    Then the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO"
    Then the next snapshot shows 1 breach for "TDR-BKK-CO" in Power BI

  Scenario: AC4 No member has capacity (legacy RWB-E1-030 AC4)
    Given every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner
    When JOB-06 runs
    Then the 5 cases keep no owner
    Then the team manager receives MSG-P3-011 with count 5

  Scenario: AC5 No cap loaded (legacy RWB-E1-030 AC5)
    Given queue "WO-BKK-CO" has no capacity cap
    When JOB-06 runs
    Then the system moves no case in "WO-BKK-CO"
    Then the snapshot still reports "WO-BKK-CO"

  Scenario: AC6 Decision log unavailable for one case (legacy RWB-E1-030 AC6)
    Given owner U-63 holds 153 open cases and the decision log write fails for the second of the 3 newest cases
    Given the rwb-decision contract mock returns MSG-P7-003 for the second of the 3 newest cases
    When JOB-06 runs
    Then the system moves 2 cases off U-63 and 1 stays
    Then the job record lists the case that stayed with MSG-P7-003

  Scenario: AC7 A repeated run (legacy RWB-E1-030 AC7)
    Given JOB-06 has balanced "TDR-BKK-CO" on 2026-12-02
    When JOB-06 runs again on 2026-12-02
    Then the system moves no case
    Then the system writes no decision log entry

  Scenario: AC8 Held cases are not moved (legacy RWB-E1-030 AC8)
    Given owner U-64 holds 152 open cases and the 2 newest have deviation_open = true
    When JOB-06 runs
    Then those 2 cases stay with U-64 and the next 2 newest are moved

  Scenario: AC9 A count difference holds the snapshot (legacy RWB-E1-030 AC9)
    Given the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87
    When the snapshot is checked
    Then the system does not publish it
    Then the data steward receives MSG-P3-029 with check "queue depth against case list"

  Scenario: AC10 Owner exactly at the cap (legacy RWB-E1-030 AC10)
    Given owner U-65 holds 150 open cases
    When JOB-06 runs
    Then the system moves no case off U-65
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Cases with no owner are assigned by the queue's method within the cap | queue.assignment_method, queue.capacity_cap; FEAT-CWC-17 |
| BR2 | An owner above the cap loses the newest cases until inside the cap | R-UNI-19 |
| BR3 | Cases with an open deviation or a legal hold are not moved | R-UNI-20; R-DEV-01 |
| BR4 | A queue with no cap is reported and not rebalanced | DL23 |
| BR5 | A move keeps the case status and the clocks | R-UNI-18 |
| BR6 | Measures publish only when queue depths reconcile to the case list with zero difference | DL25; REC-01 |
| BR7 | Every move is logged before it takes effect | Principle 5; R-UNI-39 |
| BR8 | A breach raises an alert to the escalation role; the case does not move | R-UNI-30 |

Target-service statements that make the rules hold in `rwb-case`:

- BR1 and BR2 are executed by the assignment engine inside the `rebalance` activity; no method, cap or member order is written in code (BR-P3-017).
- BR3 reads `recovery_case.deviation_open` and `recovery_case.legal_hold` in this schema; no other service is asked.
- BR6 is a count read in the same REPEATABLE READ transaction as the snapshot, so depth and case count are taken at one time.
- BR7 is the single transaction of step 6 of section 4: the record, the assignment swap and the event either all commit or none does.
- BR8 is raised on `rwb.case.TimerBreached.v1`; the alert never changes the queue, the owner or the status of the case.

### 9. State transitions

None for the case. This story does not change a case status. It changes the owner and the assignment of a case (reason REBALANCE), and the status of a measure snapshot.

| From | Event | To |
|---|---|---|
| (no snapshot) | the run's measure step completes | `TAKEN` |
| `TAKEN` | every queue's depth equals the case list count at the same time | `PUBLISHED`, served by `GET /queues` |
| `TAKEN` | one queue's depth differs from the case count | `HELD`, MSG-P3-029 to the data steward, not served |
| `PUBLISHED` | a later run takes a new snapshot for a later as-of time | `PUBLISHED` for the new row; the earlier row stays as taken |

Workflow states of the capability:

| From | Event | To |
|---|---|---|
| `DailyCaseRun` allocation step done | the rebalance step is scheduled | `rebalance` activity running |
| `rebalance` done | moves committed or listed with MSG-P7-003 | `takeQueueMeasures` scheduled |
| `takeQueueMeasures` done | snapshot `PUBLISHED` or `HELD` | the run ends; the next firing is the next business date |
| `rebalance` or `takeQueueMeasures` fails | the kit's retry policy is exhausted | the run is marked failed on the workflow; no partial snapshot is served |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF | Moves cases and takes the snapshot |
| SY-DECLOG | Writes the decision records and publishes them on the shared topic |
| RW-TEAMMGR | Receives the summaries and alerts; reads queues in team scope (Queue and allocation CRUA) |
| RW-BIANAL | Builds the Power BI report on the measures of its own projection (Reporting CRUD) |
| RW-DATASTEW | Receives the reconciliation break |
| RW-PLATADM | Triggers the Schedule again (Platform administration U) |
| RW-CASEOWN | Reads the case and the queue; may not rebalance (Queue and allocation R) |

The authorisation decision is the cached permission decision the service holds from `rwb-access`; this story adds no REST operation consumption and no guard of its own. The refusal shape is 403 with MSG-P4-002, as in the legacy rerun path. Where the Schedule trigger is reached is Not specified in the source documents (GAP-2205; ASM-3622).

### 11. Data

| BR Field ID | Table in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` | id | Read |
| DF-CAS-005 | `recovery_case` | status | Read |
| DF-CAS-009 | `recovery_case` | owner_user_id | Write |
| DF-CAS-010 | `recovery_case` | queue_id | Read |
| DF-CAS-013 | `recovery_case` | entry_date | Read |
| DF-CAS-019 | `recovery_case` | deviation_open | Read |
| DF-CAS-020 | `recovery_case` | legal_hold | Read |
| DF-WRK-001 | `queue` | id | Read |
| DF-WRK-002 | `queue` | queue_code | Read |
| DF-WRK-004 | `queue` | team_code | Read |
| DF-WRK-006 | `queue` | assignment_method | Read |
| DF-WRK-007 | `queue` | capacity_cap | Read |
| DF-WRK-048 | `queue_member` | capacity | Read |
| DF-WRK-009 to DF-WRK-016 | `assignment` | all fields | Write |
| DF-WRK-028 | `timer` | case_id | Read |
| DF-WRK-030 | `timer` | timer_type | Read |
| DF-WRK-035 | `timer` | status | Read |
| DF-RPT-020 to DF-RPT-030 | `queue_measure` | all fields | Write |
| DF-DEC-001 to DF-DEC-018 | decision-record library table in `rwb_case` | all fields | Write |
| (outbox) | outbox library table in `rwb_case` | `CaseTransferred` rows | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. The decision record replaces the legacy `decision_log_entry` write of another module (DP-03); the central ledger entry is written by `rwb-decision` from the record on `rwb.decision-record.v1`. No table of another service is read (DP-01), and the snapshot holds counts only, never a party, a name or an amount.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/case/v1/queues` | P3 | The latest published measure per queue: depth, unassigned, average and maximum age, owner minimum and maximum, breaches, as-of time; scoped to the caller's queues |

Contract-defined in RWB-P3-E1030-CON. The reconciliation read `GET /api/recovery/case/v1/cases` with the queue filter is the case read of the case record stories, used unchanged here.

#### 12.2 REST operations consumed

None. The owner choice is an in-process call of the assignment engine inside this service (DP-11 row replaced by an in-process component, no contract). The authorisation decision is the cached permission decision from `rwb-access` that the service template's guard already holds.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.case.CaseTransferred.v1` (EV-04) | `rwb.case.events.v1` | P3 | caseId | caseId, fromOwner, toOwner, reasonCode |
| decision record | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained decision record |

CloudEvents 1.0 envelope. One `CaseTransferred` per move, published after its transaction commits; no payload carries personal data.

#### 12.4 Events consumed

| Event | Topic | Owner | Note |
|---|---|---|---|
| `rwb.case.TimerBreached.v1` (EV-19) | `rwb.case.events.v1` | P3 | Raised by the durable timer of this service; drives the breach alert (AC3) |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DailyCaseRun` | Workflow, started by the Schedule | `rwb-case` | Runs the allocation step, then the rebalance step, for one business date |
| `rebalance` | Activity | `rwb-case` | Selection, hold checks, owner choice, per-case transaction with the record and the outbox |
| `takeQueueMeasures` | Activity | `rwb-case` | One snapshot per queue, the reconciliation check and the status |
| `publishBreachAlert` | Activity | `rwb-case` | The queue breach count and MSG-P3-028 to the escalation role |

#### 12.6 Schedules

| Schedule | Workflow | Cron | Zone | Note |
|---|---|---|---|---|
| `rwb-case-rebalance-daily` | `DailyCaseRun` | 06:30 daily | the business time zone of the values file, Not specified in the source documents (GAP-2207; ASM-3623) | Created by RWB-P3-E1030-OPS; replaces the Quartz trigger of JOB-06 |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `recovery_case` | P3 | Owner, queue, status, entry date, deviation flag, legal hold |
| `assignment` | P3 | End the old row, insert the new row with reason REBALANCE |
| `queue` | P3 | Method, cap, team |
| `queue_member` | P3 | Member capacity and member order |
| `timer` | P3 | Count of `SERVICE_LEVEL` timers `EXPIRED` per queue |
| `queue_measure` | P3 | One snapshot per queue and as-of time, with its status |
| decision-record, outbox and inbox tables | PLT library, created in `rwb_case` | Written in the same transaction as the move |

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case queue and case read fake | RWB-P3-E1030-CON | The controller, the reconciliation read and the measure view |
| decision-record fake | RWB-PLT-E1027-CON | The local record write and the topic publish |
| decision contract fake | RWB-P7-E1027-CON | The central ledger's collection of the record |
| assignment engine stub | RWB-P3-E1020-APP | Lowest load, member order and the cap check in unit and component tests |
| timer contract stub | RWB-P3-E1028-CON | The `EXPIRED` timers and the `TimerBreached` message |
| workflow kit test environment | RWB-PLT-E1071-CON | The Schedule and the two activities under a test server |
| reference-data fake | RWB-P3-E1043-CON | The queue and member rows in force |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 0 | `GET /queues`; the case read is an own operation |
| Kafka | Published 1 event and 1 decision record; consumed 1 event | `rwb.case.events.v1`, `rwb.decision-record.v1` |
| Temporal | 1 workflow, 3 activities, 1 Schedule | `DailyCaseRun`, `rebalance`, `takeQueueMeasures`, `publishBreachAlert` |
| File | None | The JOB-15 lake file is removed (DP-17); no file input or output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `case/rebalance`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RebalanceActivity | Temporal activity | Selection by R-UNI-19, hold checks, owner choice, per-case transaction, the run result |
| RebalanceService | Service | The selection and the move logic shared by the activity and the component tests |
| QueueMeasureActivity | Temporal activity | The snapshot in one REPEATABLE READ transaction, the reconciliation and the status |
| QueueMeasureService | Service | The snapshot query, the difference check and the `PUBLISHED` or `HELD` decision |
| BreachAlertListener | Listener and activity | Consumes `TimerBreached`, aggregates per queue, sends MSG-P3-028 |
| QueueController | Controller | `GET /queues` with the caller's scope, with the access check |
| CaseAndWorkflowRepository | Repository | `recovery_case`, `assignment`, `queue`, `queue_member`, `timer`, `queue_measure`; no foreign table |

**Database**

- Writes `assignment`, `recovery_case.owner_user_id`, `queue_measure`, the decision record and the outbox.
- The snapshot query runs in one REPEATABLE READ transaction so depth and the case count are read at the same time.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V1030_1__queue_measure.sql` creates `queue_measure` (id, queue_id, as_of, depth, unassigned, avg_age_days, max_age_days, owner_min, owner_max, breached, status, standard columns; unique (queue_id, as_of)) and adds the partial index `ix_timer_queue_expired ON timer (case_id, timer_type) WHERE status = 'EXPIRED'` for the breach count.

**Configuration and reference data**

- Caps and member capacity from `rwb_case.queue` and `rwb_case.queue_member` (RWB-E1-019 data, DL23).
- Measure definitions agreed with the Tribe (REQ-RDF-012), owned by RW-COE; they are the field list of `queue_measure` and of `GET /queues`, not code.
- Feature flag `rwb.p3.rebalance`. Off: the rebalance step moves no case; the snapshot still runs.

**Build steps**

1. Owner-over-cap selection by newest assignment; unit tests AC8, AC10.
2. `RebalanceService` with the assignment engine and the hold checks; tests AC1, AC4, AC5.
3. One transaction per case with the decision record as its last step; continue on failure; test AC6.
4. Idempotent rerun; test AC7.
5. `QueueMeasureService` snapshot and reconciliation; tests AC2, AC9.
6. `BreachAlertListener` with MSG-P3-028; test AC3.
7. `GET /queues` with the access check and the scope; access test.
8. The Schedule wiring in `DailyCaseRun`, exercised in the workflow kit test environment.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; the replacement feed is Not specified in the source documents (GAP-2205; ASM-3620) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The DP-11 row: the legacy in-process call is `QueueMeasureService.latestPublished`, read by P9. With no data lake the consumer disappears, so no contract is consumed; the story's one contract dependency is the decision contract RWB-P7-E1027-CON, which collects the record this story publishes.

**Done when.** The tests in section 16 pass, `DailyCaseRun` moves the 12 cases of AC1 in SIT, every move has one decision record naming reason REBALANCE and one `CaseTransferred` on the topic, a held snapshot raises MSG-P3-029, a balanced rerun moves nothing, and the queue page of the reporting projection shows the 2026-12-02 snapshot on 2026-12-03.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Cases left without an owner | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-028 | Service level breach alert | {count} cases in {queue} are past their service level. |
| MSG-P3-029 | Snapshot does not reconcile | The queue measures for {date} were not published: {check}. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three alert messages are delivered on the ACE notification path at wave 1, with the message ID as the template key; the path is Not specified in the source documents (GAP-2205; ASM-3621). `GET /queues` answers the RFC 9457 problem envelope with the ID above for 401, 403 and 503.

### 15. Screens and states

No new screen. SCR-02 Case list (filtered) shows the new owner; SCR-09 Exception queue (list) shows cases left without an owner. The team view SCR-07 comes in Epic 2; the queue measures appear on the reporting queue page, built from the events by RW-BIANAL, and on `GET /queues` for the case-side screens.

States this story makes visible: the snapshot status (`TAKEN`, `PUBLISHED`, `HELD`) per queue and as-of time; the owner after a rebalance; the overflow marker for a case with no owner.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-030-11 | Access | Component | RW-CASEOWN triggers the Schedule and is refused with MSG-P4-002 |
| TC-E1-030-01 | AC1, BR1, BR7 | End to end | 12 unassigned cases, owners at 140 and 144 |
| TC-E1-030-02 | AC2, BR6 | End to end | Snapshot at 06:52 |
| TC-E1-030-03 | AC3, BR8 | End to end | One breach in TDR-BKK-CO |
| TC-E1-030-04 | AC4 | End to end | Every member at 150, 5 unassigned |
| TC-E1-030-05 | AC5, BR4 | End to end | Queue WO-BKK-CO with no cap |
| TC-E1-030-06 | AC6, BR7 | End to end | Owner at 153, record fails for one case |
| TC-E1-030-07 | AC7 | End to end | The run twice on 2026-12-02 |
| TC-E1-030-08 | AC8, BR3 | End to end | Owner at 152 with 2 held cases |
| TC-E1-030-09 | AC9, BR6 | End to end | Depth 88 against count 87 |
| TC-E1-030-10 | AC10, BR2 | End to end | Owner at exactly 150 |
| TC-E1-030-12 | Principle 5 | NFR | Decision record write forced to fail for every move in the run |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end, Access to Component and Resilience to NFR.

### 17. Guardrails

- No business value in code: caps, methods, member order and measure definitions are data; BR-P3-017.
- No personal data in the snapshot, the alerts, the logs or the tests; the snapshot holds counts only.
- No read of another service's table (DP-01): queues, members, cases and timers are rows of `rwb_case`.
- No file leaves the service and no data-lake copy is written (DP-17); reporting projects from events.
- A move never resets the stage clock or the prescription date (BR5).
- The reconciliation is a read at one time in one transaction; a count taken while the run is still writing is a held snapshot, not a passing one.
- The run is idempotent by state: a balanced queue selects nothing, and a repeat writes no decision record.
- The feature flag `rwb.p3.rebalance` removes the moves without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-015 | Daily rebalancing; queue counts, ageing and breaches reported | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-17, FEAT-CWC-18, FEAT-WKM-11 | All recovery processes | R-UNI-19, R-UNI-30 | TC-E1-030-01, TC-E1-030-03 to TC-E1-030-10, TC-E1-030-12 |
| REQ-RDF-012 | Baseline measures for cases by queue and age published | Epic 1, 3.3; Program, 5.1 | FEAT-RPT-02 | 15 Manage performance, data and AI | None | TC-E1-030-02, TC-E1-030-09 |

| Legacy reference | Where it is kept |
|---|---|
| JOB-06 Daily rebalancing, daily 06:30 | Metadata, sections 3, 4, 12.6, 16 |
| Event CaseTransferred (EV-04) | Sections 4, 12.3, 17 |
| MSG-P3-011, MSG-P3-028, MSG-P3-029, MSG-P7-003, MSG-P4-002 | Section 14, exception paths |
| `queue_measure` snapshot with status TAKEN, PUBLISHED, HELD | Sections 9, 11, 12.7 |
| Feature flag `rwb.p3.rebalance` | Sections 13, 17 |
| Legacy key RWB-E1-030, contract RWB-P3-E1030-CON, deployment RWB-P3-E1030-OPS | Metadata, sections 3, 12 |

### 19. Out of scope

- Reallocation when an owner leaves or is absent (R-UNI-18, Epic 2).
- The team queues screen (SCR-07, Epic 2) and the steering dashboard (Epic 2).
- The Power BI report layout and its own projection (P9, RW-BIANAL).
- The assignment engine itself (RWB-P3-E1020-APP) and the timer capability (RWB-P3-E1028-APP).
- The central decision ledger and its own contract (rwb-decision).
- The contract document and its fakes (RWB-P3-E1030-CON); the chart, the Schedule creation, the alerts and the runbook (RWB-P3-E1030-OPS).
- The access, ledger, reporting and integration slices of the same legacy key in rwb-access, rwb-decision, rwb-reporting and the wave-1 harness.

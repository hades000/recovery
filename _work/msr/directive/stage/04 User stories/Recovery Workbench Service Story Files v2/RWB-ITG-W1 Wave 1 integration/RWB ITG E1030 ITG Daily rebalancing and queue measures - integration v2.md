# RWB-ITG-E1030-ITG Daily rebalancing and queue measures

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1030-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; INVEST Small: fits two weeks |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1030-APP, RWB-P7-E1030-APP (build not done yet) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-CWC-015, REQ-RDF-012) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-030 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E1030-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-030 daily rebalancing and queue measures across P3 rwb-case (the JOB-06 Schedule, assignment, queue_measure, decision records), P7 rwb-decision (the central ledger) and P9 rwb-reporting (the published measures), with P1 rwb-source-data serving the job catalogue**, so that **rebalancing, reconciliation and measures are proved on the real wave 1 services before the wave exits**.

### 2. Business rationale

The legacy story moves work left in overflow or without an owner each morning, takes owners above the cap back inside it (R-UNI-19), and takes one snapshot per queue at one time: depth, unassigned, age in days from the entry date, owner spread and SERVICE_LEVEL timers EXPIRED. It runs JOB-06 on Quartz at 06:30, copies the snapshot to the data lake by JOB-15, and publishes the interface `recovery.casewf.rebalance.QueueMeasureService`, which P9 reads for Power BI (RWB-E1-030 sections 4 and 12). Every move is logged with the decision record written before it takes effect, and the measures publish only when every queue depth reconciles to the case list with zero difference.

The target changes the mechanism and the delivery path, not the behaviour. DP-10 replaces Quartz with a Temporal Schedule in rwb-case (Arch v5 slide 44, JOB-06 at 06:30, overlap SKIP, catch-up window), so the run belongs to the service that owns the cases and the ACE shared Quartz tables are no longer used. DP-03 makes each move write a local decision record in rwb_case in the same transaction as the assignment change and publish `DecisionRecorded` to `rwb.decision-record.v1`, collected by P7 rwb-decision within five minutes (ADR-022). DP-17 removes the data lake: the measures reach P9 rwb-reporting as a projection from events, JOB-13 ingests the decision records continuously and JOB-15 is an Airflow trigger with no lake copy. DP-13 and DP-14 rename the base to `/api/recovery/<short>/v1` and the topic to `rwb.<short>.events.v1`. DP-01 keeps `queue_measure` in `rwb_case`, where the case and the assignment live.

The target split of the legacy key is therefore: RWB-P3-E1030-APP owns the Schedule, the assignment and cap logic, the hold checks, the snapshot and its reconciliation, the breach alert and the local decision record; RWB-P7-E1030-APP owns the central ledger and its collection of `rwb.decision-record.v1`. This integration story owns no legacy acceptance criterion: legacy AC1 to AC10 sit at component level with those two app stories, and the scenarios of section 7 are the integration proof that the same behaviour holds when the three services and the two topics are wired together in SIT. One consumed operation needs a word here. The job catalogue of P1 rwb-source-data — `GET /api/recovery/source-data/v1/admin/jobs` and `POST /api/recovery/source-data/v1/admin/jobs/JOB-06/rerun` — is a CON-level platform contract with no APP story in this lane, so it is not in the integration dependency list, and the measure read of P9 rwb-reporting is the wave 1 reporting projection of the same legacy measures, not an APP story of this legacy key.

Where the sources do not fix the details the suite needs, the suite asserts through the owners' contracts and records the open point: the Schedule identifier and the exact rerun façade at the nominal run time (GAP-0354; ASM-0448), the event that marks a measure as published (GAP-0354; ASM-0449), and the scope of the test-only fault switch on the decision-record library (GAP-0354; ASM-0450). Release 30 November 2026 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P3-E1030-APP is done: the JOB-06 Schedule, the assignment and cap logic, the hold checks, the one-transaction move with its decision record, `queue_measure`, the snapshot reconciliation and the breach alert are in SIT on rwb-case.
- RWB-P7-E1030-APP is done: the central ledger collects `rwb.decision-record.v1` idempotently and the ledger query answers by case, decision code and date.
- The published contracts of P3 rwb-case, P7 rwb-decision and P9 rwb-reporting, and the P1 rwb-source-data job catalogue, are deployed under their per-service bases behind gateway-bff, and the harness RWB-ITG-W1J01-ITG is available with its synthetic cases, queues, members and caps for business date 2026-12-02.
- The capacity caps are loaded as data rows (DL23), with the queue method LOWEST_LOAD of queue TDR-BKK-CO a configuration row and not code, and the queue and member reference data and the measure definitions are read through the P3 parameters and reference-data contracts with the codes sent as data.
- SIT is in place: namespace `rwb-recovery`, the task queues `rwb-case`, `rwb-decision` and `rwb-reporting`, and the topics `rwb.case.events.v1`, `rwb.decision-record.v1` and `rwb.reporting.events.v1` with their retry and `.dlt` topics, and the clock control of the harness can move the nominal Schedule time to 06:30 on 2026-12-02 and restore it afterwards.
- The agreed test-only fault switch on the P3 decision-record library can fail the record write for one case (AC6) and for every move (AC11), and it is agreed with the service owner.
- No production data is used and no production connection is opened; the suite refuses an environment that is not SIT, and release 30 November 2026 is tentative.
- This story has no build dependency, so it is ready on Day 1 under Template and Rules §R5.7; the Schedule identifier in SIT and the exact rerun façade at the nominal run time are Not specified in the source documents (GAP-0354; ASM-0448).

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, queues, members and caps of the harness RWB-ITG-W1J01-ITG for business date 2026-12-02, with cap 150 on TDR-BKK-CO, members U-61 and U-62 at 140 and 144 open cases and 12 cases with no owner; no production data is used.
2. Harness: reads `GET /api/recovery/case/v1/queues` and `GET /api/recovery/case/v1/queues/{queueId}/cases` before the run, records the queue depth, the unassigned count and the owner spread, and moves the clock to 06:30 on business date 2026-12-02 so the JOB-06 Schedule fires.
3. System: rwb-case assigns the unassigned cases and moves the newest cases off owners above the cap, skipping cases with `deviation_open` or `legal_hold` true, with reason REBALANCE, writing the assignment and the local decision record in one transaction.
4. Harness: reads the queues and their cases after the run, reads `GET /api/recovery/case/v1/cases/{caseId}` for each moved case and asserts the new owner with the same status and stage, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` for case RW-2026-000501 to take the expired service-level timer as the breach the next snapshot must count.
5. Harness: waits on `rwb.case.CaseTransferred.v1` on `rwb.case.events.v1` for one event per move and on `rwb.case.TimerBreached.v1` for the breach, and asserts the CloudEvents envelope and the case ID key.
6. Harness: waits on `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for every move, reads `GET /api/recovery/decision/v1/decision-log` and measures the elapsed collection of each record against the five-minute target.
7. Harness: takes the snapshot at 2026-12-02 06:52, reads `GET /api/recovery/reporting/v1/reports/measures` for the business date and reconciles every queue depth to `GET /api/recovery/case/v1/cases` at the snapshot time, with zero difference.
8. Harness: triggers a rerun through `POST /api/recovery/source-data/v1/admin/jobs/JOB-06/rerun` and asserts that no case moves and no decision record is written on the same business date.
9. Harness: runs the negative cases — no member with capacity, no cap, held cases and the owner exactly at the cap, a failed record for one case, every record failing, a snapshot depth that differs from the case list, and a caller without Platform administration U — records every status, message and count, proves from the call set of the run that no lake endpoint is called, then writes the evidence report, removes the synthetic fixtures and restores the clock.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No member of the queue has capacity | The cases keep no owner and are counted in the run summary | MSG-P3-011 | AC4 |
| X2 | No capacity cap is loaded for the queue | The queue is reported and no case in it is moved | None | AC5 |
| X3 | The local decision record write fails for one case | That case stays with its owner, the run continues for the other cases, and the run record names the case that stayed | MSG-P7-003 | AC6 |
| X4 | JOB-06 runs again on the same business date | An already balanced queue gives no further move and no further record | None | AC7 |
| X5 | A case has an open deviation or a legal hold | The case is not moved and the next newest case is taken instead | None | AC8 |
| X6 | The snapshot depth differs from the case count at the same time | The snapshot is held, nothing is published for the date, and the break is listed for the data steward | MSG-P3-029 | AC9 |
| X7 | An owner holds exactly the cap | No case is moved off that owner | None | AC8 |
| X8 | A role without Platform administration U reruns JOB-06 | Refused with status 403, no run starts and no case moves | MSG-P4-002 | AC10 |
| X9 | The decision record write fails for every move of the run | Nothing moves, no partial run is left and every case of the run is reported | MSG-P7-003 | AC11 |
| X10 | A consumed call exceeds the 2 s timeout or returns a server error | The call is retried once under the suite policy and the evidence report records it; no assertion is made on data that was not read | None | AC1, AC2 |
| X11 | The fixture set does not match the harness expectations, or the clock control cannot move the nominal Schedule time | The suite fails as a harness fault and names the element; no service defect is raised | None | AC1, AC3 |

X1 to X9 are the exception paths of the legacy story read on the wave 1 services; X10 and X11 are the suite's own failure modes, so that a timeout never becomes a pass and a fixture or clock fault is reported as a harness fault rather than as a service defect.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the two APP stories and the published contracts of P1, P3, P7 and P9, not their source code |
| Negotiable | The fixture sizes, the clock control, the wait windows and the rerun façade are properties of the harness; the story fixes the assertions, the values and the call set |
| Valuable | Rebalancing, the ledger and the measures are proved on the real services, and the five-minute collection and the reconciliation are measured rather than assumed, before wave 1 exits |
| Estimable | One suite module, one fixture pack, one clock control, two assertions (reconciliation and ledger completeness) and one evidence report |
| Small | Eleven scenarios over four services, three topics and one Schedule; no service code and no schema change |
| Testable | Every scenario asserts a contract response, an event, a status, a message or a count; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Daily rebalancing and queue measures, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-case, rwb-decision and rwb-reporting are deployed in SIT with their published contracts behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic cases, queues, members and caps are loaded and no production data is used
    Given the business date is 2026-12-02

  Scenario: AC1 The 06:30 Schedule rebalances through the case contract (new, D-RCV-60)
    Given queue "TDR-BKK-CO" uses "LOWEST_LOAD" with cap 150
    Given 12 cases with no owner
    Given members U-61 and U-62 hold 140 and 144 open cases
    When the rebalancing Schedule fires at 06:30
    Then the 12 cases are assigned, 8 to U-61 and 4 to U-62, by lowest load with ties going to the member first in the queue list
    Then each case read through GET /api/recovery/case/v1/cases/{caseId} shows its new owner with the same status and stage
    Then one CaseTransferred event is published on rwb.case.events.v1 for each move

  Scenario: AC2 The measures reconcile and reach reporting without a lake (new, D-RCV-60)
    Given the snapshot is taken at 2026-12-02 06:52
    When the queue measures are published
    Then GET /api/recovery/reporting/v1/reports/measures for 2026-12-02 shows for every queue a depth equal to the case count of that queue at 06:52
    Then "TDR-BKK-CO" shows depth 296, unassigned 0 and an average age of 41 days
    Then no lake endpoint is called and the measures reach rwb-reporting only through its published topic (DP-17)

  Scenario: AC3 A service-level breach reaches the team manager (new, D-RCV-60)
    Given case RW-2026-000501 in "TDR-BKK-CO" passes its service level
    When the timer check raises the breach
    Then the team manager of "TDR-BKK" receives MSG-P3-028 with count 1 and queue "TDR-BKK-CO"
    Then the next snapshot shows 1 breach for that queue

  Scenario: AC4 No member has capacity (new, D-RCV-60)
    Given every member of "TDR-BKK-CO" holds 150 open cases and 5 cases have no owner
    When the rebalancing Schedule runs
    Then the 5 cases keep no owner
    Then the team manager receives MSG-P3-011 with count 5

  Scenario: AC5 No cap loaded (new, D-RCV-60)
    Given queue "WO-BKK-CO" has no capacity cap
    When the rebalancing Schedule runs
    Then no case in "WO-BKK-CO" is moved
    Then the snapshot still reports "WO-BKK-CO"

  Scenario: AC6 A failed decision record stops that case only (new, D-RCV-60)
    Given owner U-63 holds 153 open cases and the local decision record write fails for the second of the 3 newest cases
    When the rebalancing Schedule runs
    Then 2 cases move off U-63 and 1 stays
    Then the run record lists the case that stayed with MSG-P7-003
    Then each moved case has one entry in GET /api/recovery/decision/v1/decision-log within five minutes

  Scenario: AC7 A repeated run (new, D-RCV-60)
    Given the rebalancing Schedule has balanced "TDR-BKK-CO" on 2026-12-02
    When the rebalancing Schedule runs again on the same business date
    Then no case is moved
    Then no decision record is written

  Scenario: AC8 Held cases and the cap edge (new, D-RCV-60)
    Given owner U-64 holds 152 open cases and the 2 newest have deviation_open = true
    When the rebalancing Schedule runs
    Then those 2 cases stay with U-64 and the next 2 newest are moved
    Then owner U-65 holding exactly 150 open cases loses no case

  Scenario: AC9 A count difference holds the snapshot (new, D-RCV-60)
    Given the snapshot depth for "DIL-BKK-CO" is 88 and the case count at the same time is 87
    When the snapshot is checked
    Then it is not published
    Then the data steward receives MSG-P3-029 with check "queue depth against case list"

  Scenario: AC10 A role without the right cannot rerun (new, D-RCV-60)
    Given test user "U-7101" holds RW-CASEOWN
    When the user calls POST /api/recovery/source-data/v1/admin/jobs/JOB-06/rerun
    Then the call returns status 403 with MSG-P4-002
    Then no run starts and no case moves

  Scenario: AC11 Every record failing means nothing moves (new, D-RCV-60)
    Given the local decision record write is switched to fail for every move by the agreed test-only fault switch
    When the rebalancing Schedule runs
    Then no assignment changes and no partial run is left
    Then no decision record exists for the business date
    Then each case is reported with MSG-P7-003

  Scenario: AC12 A move keeps the status and clocks and the run rules hold (new, D-RCV-60)
    Given case RW-2026-000501 has a status, a stage and running clocks before the rebalancing Schedule runs
    When the rebalancing run moves the case on the Schedule that fires at 06:30 with overlap SKIP and catch-up
    Then the case keeps its status, its stage and its clocks
    Then the move is written to the local decision record in rwb_case in the same transaction and DecisionRecorded is published
    Then the queue measures reach rwb-reporting only through the published topic and no lake endpoint is called
    Then every cross-service call of the run is one hop with a 2 s timeout

  Scenario: AC13 A retried or timed-out activity does not move a case twice (new, D-RCV-60)
    Given an activity of the rebalancing run for 2026-12-02 times out (activity timeout: Not specified in the source documents (NEWAC-RWB-ITG-E1030-ITG-AC13)) after moving case RW-2026-000501
    When the activity is retried for the same business date
    Then the case is not moved again
    Then no second decision record is written for that move

  Scenario: AC14 A consumed call that fails or does not answer leaves the case unchanged (new, D-RCV-60)
    Given a call the rebalancing run consumes for case RW-2026-000501 (call: Not specified in the source documents (NEWAC-RWB-ITG-E1030-ITG-AC14)) does not answer within 2 s
    When the rebalancing Schedule runs
    Then the case keeps its owner and no decision record is written for it
    Then the run record lists the case as not moved

  Scenario: AC15 A status change the model does not allow is refused (new, D-RCV-60)
    Given case RW-2026-000501 is in a status and stage of the case status model
    When a caller requests a status change the model does not allow through the case contract
    Then the call is refused and the case keeps its status and stage
    Then no decision record is written for the refused change
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
| BR9 | JOB-06 is a Temporal Schedule in rwb-case at 06:30 (business time zone: Not specified in the source documents (GAP-2207)) with overlap SKIP and catch-up (catch-up window: Not specified in the source documents (GAP-2207)), replacing Quartz | DP-10; Arch v5 slide 44 |
| BR10 | Each move writes its local decision record in rwb_case in the same transaction and publishes DecisionRecorded, and P7 collects it within five minutes | DP-03; ADR-022 |
| BR11 | Queue measures reach rwb-reporting as a projection from events, and a measure publishes only when reconciled with zero difference, with no data lake | DP-17; DL25 |
| BR12 | Every cross-service call is one hop with a 2 s timeout | ADR-020; DP-11 |

Open decisions applied: DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863), DL23 (ASM-1232, ASM-1237, ASM-1259, ASM-1560) and DL25 (ASM-0728, ASM-0735, ASM-0743, ASM-2602). Each is closed by its recommended resolution, and its assumptions are confirmed by the programme directive.

### 9. State transitions

None for the case status. This story does not change a case status. It observes the owner of a case and its assignment moving with reason REBALANCE, and the state of a measure snapshot moving from TAKEN to PUBLISHED or to HELD, all of them read through the owners' contracts and the owner topics and none of them changed directly.

| Object | State | Meaning |
|---|---|---|
| Assignment (rwb_case) | Moved to a new owner | The old assignment ends and a new one is written with reason REBALANCE in the same transaction as the local decision record; `recovery_case.owner_user_id` names the new owner, read through `GET /api/recovery/case/v1/cases/{caseId}`, and the case status, the stage and the clocks are unchanged (R-UNI-18) |
| Measure snapshot (rwb_case) | TAKEN | One snapshot per queue at one time: depth, unassigned, average age in days from the entry date, owner spread and expired SERVICE_LEVEL timers |
| Measure snapshot (rwb_case) | PUBLISHED | Every queue depth reconciles to the case list with zero difference; the measures are projected into rwb-reporting and published for the business date |
| Measure snapshot (rwb_case) | HELD | At least one queue differs from the case list at the same time; nothing is published for the date and the data steward receives MSG-P3-029 |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, moves the test clock, reads the evidence report |
| SY-CASEWF Case and workflow system | Moves cases, writes the assignment and the local decision record, takes and publishes the snapshot |
| SY-DECLOG Decision log writer | Writes the local record of every move and every snapshot decision |
| RW-TEAMMGR Team manager | Receives MSG-P3-011 and MSG-P3-028; reads the queues in team scope |
| RW-BIANAL Reporting and BI analyst | Builds the Power BI queue page on the P9 measures; changes no value |
| RW-DATASTEW Data steward | Receives the reconciliation break of MSG-P3-029 |
| RW-PLATADM Platform administrator | Reruns JOB-06 (Platform administration U); reads the run record |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Write by P3 rwb-case; read back through the contract |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-013 | recovery_case | entry_date | Read |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-020 | recovery_case | legal_hold | Read |
| DF-WRK-001 | queue | id | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-006 | queue | assignment_method | Read |
| DF-WRK-007 | queue | capacity_cap | Read |
| DF-WRK-048 | queue_member | capacity | Read |
| DF-WRK-009 to DF-WRK-016 | assignment | all fields | Write by P3 rwb-case; read back through the contract |
| DF-WRK-028 | timer | case_id | Read |
| DF-WRK-030 | timer | timer_type | Read |
| DF-WRK-035 | timer | status | Read |
| DF-RPT-020 to DF-RPT-030 | queue_measure | all fields | Computed and published by P3 rwb-case on the business date; P9 rwb-reporting projects them and computes none; read back through the P3 snapshot and the P9 measures |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write by P3 rwb-case locally and by P7 rwb-decision in the ledger; read through the ledger query |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E1-030. The legacy story writes these tables in the monolith. In the target `queue_measure`, `assignment`, `recovery_case` and `timer` stay in `rwb_case` (DP-01), the local decision record is written in `rwb_case` and collected into the ledger of `rwb_decision` (DP-03), and the measures are a projection in `rwb_reporting` (DP-17). The suite reads every one of them only through the contracts of section 12.2, or through an event of section 12.4, and writes no schema of its own and no row of another service.

### 12. Contract

Contract version: v1, the /v1 path given in section 12.2.

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no rwb_integration table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/queues | P3 rwb-case | Read the queues, their method, their cap and the team before and after the run |
| GET /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | Read the cases of a queue with their owner and assignment time before and after the run |
| GET /api/recovery/case/v1/cases | P3 rwb-case | Read the case list of the business date for the reconciliation of every queue depth at the snapshot time |
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read one moved case: the new owner with the same status and stage |
| GET /api/recovery/case/v1/cases/{caseId}/timers | P3 rwb-case | Read the expired service-level timer of the breach case |
| GET /api/recovery/case/v1/admin/parameters | P3 rwb-case | Read the parameters and the queue reference data as rows, not as code |
| GET /api/recovery/source-data/v1/admin/jobs and POST /api/recovery/source-data/v1/admin/jobs/JOB-06/rerun | P1 rwb-source-data, job catalogue | Read the job catalogue and trigger one rerun of JOB-06; the exact façade is Not specified in the source documents (GAP-0354; ASM-0448) |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Confirm the collection of every decision record of the run and measure the elapsed time against five minutes |
| GET /api/recovery/reporting/v1/reports/measures | P9 rwb-reporting | Read the published measures of business date 2026-12-02 for the reconciliation and the breach count |

Every call is one hop to the owning service on its own base with a 2 s timeout (ADR-020, DP-11, DP-13); the P1 job catalogue is a CON-level platform contract with no APP story in this lane, and it is consumed here for the catalogue read and the rerun.

#### 12.3 Events published

None. The suite publishes no event. Every event asserted in this story is produced by a service and is listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.case.CaseTransferred.v1 | rwb.case.events.v1 | P3 rwb-case | One event per move; the suite counts the moves of the run against it |
| rwb.case.TimerBreached.v1 | rwb.case.events.v1 | P3 rwb-case | The breach the next snapshot must count for the queue |
| rwb.decision.DecisionRecorded.v1 | rwb.decision-record.v1 | every service, with the ledger owned by P7 rwb-decision | The record of each move; the suite measures the collection against the five-minute target |
| rwb.reporting.ReportPublished.v1 | rwb.reporting.events.v1 | P9 rwb-reporting | Marks the measures of the business date as published; whether P9 signals one event per measure or per snapshot is Not specified in the source documents (GAP-0354; ASM-0449) |

All four are consumed in the CloudEvents 1.0 envelope, keyed caseId, with the inbox dedupe of the consumer and the retry and `.dlt` topics of the owner (ADR-015; Arch v5 slides 42 and 43). The suite asserts on IDs and facts only and writes no payload of its own.

#### 12.5 Workflows and activities

| Name | Type | Queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent per case | rwb-case | Holds the case; the suite observes its record through the case read and takes no part in its order of steps |
| DailyCaseRun | Workflow started by AceDataReady and by its Schedule | rwb-case | Runs JOB-03 as a step, so the business date is allocated before the JOB-06 run |
| JOB-06 Schedule | Temporal Schedule | rwb-case | Fires the rebalancing at 06:30 with overlap SKIP; the schedule identifier and catch-up window are Not specified in the source documents (GAP-0354); the suite moves the test clock to the nominal time |
| allocate, transfer, rebalance | Activities | rwb-case | Read the queue and the members, choose the owner, write the assignment and the local decision record in one transaction |

All four are registered by RWB-P3-E1030-APP; this story starts the Schedule only through its nominal time and the rerun, and it adds no workflow and no activity of its own.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| JOB-06 Daily rebalancing | Daily at 06:30, overlap SKIP, catch-up window per platform default | Registered by the rwb-case release on task queue `rwb-case` in namespace `rwb-recovery`; the Schedule identifier in SIT is Not specified in the source documents (GAP-0354; ASM-0448) | JOB-06 Rebalancing (Arch v5 slide 44) |
| JOB-03 Morning allocation | A step of DailyCaseRun, started by AceDataReady, after 02 and by 07:00 | Runs in rwb-case, not a Schedule of its own | JOB-03 Morning allocation (Arch v5 slide 44) |

The suite starts no Schedule, moves no Schedule and waits for no Schedule of its own. It moves its own test clock to 06:30 on 2026-12-02 so the nominal fire time is reached, and for the rerun cases it calls the job-catalogue rerun of section 12.2. The exact rerun façade at the nominal run time is Not specified in the source documents (GAP-0354; ASM-0448).

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises belong to `rwb_case`, `rwb_decision` and `rwb_reporting` and are listed in section 11 with their owners.

#### 12.8 Contract fakes

None. No service contract is faked: every call in section 12.2 and every event in 12.4 is made to the real SIT service and the real topic. Two interventions are agreed, and they are the only ones in a running service:

| Intervention | Stands in for | Note |
|---|---|---|
| Test-only fault switch on the P3 decision-record library | A record write that fails | Fails one case in AC6 and every move in AC11; its exact scope and reset are Not specified in the source documents (GAP-0354; ASM-0450) |
| Clock control | The passage of time to 06:30 | Moves the nominal Schedule fire time for the business date and is restored after the run; it changes no business rule |

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 9 |
| Kafka | 0 | 4 |
| Temporal | 0 | 1 observed (the JOB-06 Schedule) |
| File | 0 | 0 |

### 13. Solution plan

| Component | Type | Responsibility |
|---|---|---|
| Suite module for RWB-ITG-W1, reusing harness RWB-ITG-W1J01-ITG | Integration suite | Runs the eleven scenarios against SIT and holds no service code |
| Fixture pack | Test data | Synthetic cases, queues, members and caps for business date 2026-12-02, with the caps loaded as data rows (DL23) |
| Clock control | Harness control | Moves the nominal Schedule time to 06:30, holds the snapshot time at 06:52 and restores both after the run |
| Reconciliation assertion | Assertion | Compares every queue depth of the P9 measures with the case list of the P3 contract at the snapshot time and fails on any difference |
| Ledger completeness assertion | Assertion | Polls the P7 decision log until the record of each move appears and measures the elapsed time against the five-minute target |
| Evidence report | Report | Records per scenario the queue, the owner, the case, the event ids, the statuses, the messages and the elapsed ledger time |

Decoupling patterns applied (Template and Rules v1 §R5.5):

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | `queue_measure`, `assignment`, `recovery_case` and `timer` stay in `rwb_case`; the ledger is in `rwb_decision`; the suite asserts through contracts only; rwb_case is owned by P3 rwb-case, rwb_decision by P7 rwb-decision and rwb_reporting by P9 rwb-reporting, and the suite owns no schema |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | On RWB-P3-E1030-APP, which writes the local record and publishes it; not a build dependency of this suite, which only waits for the ledger entry |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP stories for the queue methods and the measure definitions; the suite sends and reads the codes as data |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On RWB-P3-E1030-APP and RWB-P7-E1030-APP for CaseTransferred, TimerBreached and DecisionRecorded; the suite consumes the topics only |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | On RWB-P3-E1030-APP, which registers the JOB-06 Schedule; the suite moves the clock and triggers one rerun |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The nine consumed REST operations of section 12.2 |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path in section 12.2 |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON | On RWB-P3-E1030-APP for `rwb.case.events.v1`; the suite asserts the topic name and publishes nothing |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P3-E1030-APP and RWB-P7-E1030-APP for their own sequences; the suite owns no schema |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data | The lake step of JOB-15 is absent; AC2 asserts that no lake endpoint is called and that the measures arrive as a projection; the publish marker is rwb.reporting.ReportPublished.v1 and the collection measure is the five-minute ledger target |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The suite enters through gateway-bff; no screen is in scope, and the case list is read through the P3 contract |

The H and C dependencies in the table above belong to the owning APP stories: they record what the services the suite proves had to build, not what the suite waits for. This story's H, C and X lists are exactly the metadata rows — no H, no C and no X — and its I list is the two integration dependencies RWB-P3-E1030-APP and RWB-P7-E1030-APP. An ITG story builds against published contracts and blocks no build of its own (Template and Rules §R5.4 and §R5.7).

Build steps:

1. Create the suite module next to harness RWB-ITG-W1J01-ITG, wire it to the SIT endpoints of P1, P3, P7 and P9 through gateway-bff, and write the preflight: the four services answer, the three topics and their retry and `.dlt` topics exist, the three task queues are registered in `rwb-recovery` and the JOB-06 Schedule is present.
2. Build the fixture pack: synthetic cases, queues, members and caps for 2026-12-02, with the caps read as data rows through the P3 parameters and reference contracts, and add the clock control with its restore step.
3. Implement AC1: the clock at 06:30, the queues read before and after, the 8 and 4 assignment, the same status and stage on the case read, and one CaseTransferred event per move.
4. Implement AC2: the snapshot at 06:52, the measures read for the business date, the depth 296, unassigned 0 and average age 41 days of TDR-BKK-CO, the reconciliation to the case list and the proof that no lake endpoint is called.
5. Implement AC3: case RW-2026-000501, its expired timer, MSG-P3-028 with count 1 and the breach count of the next snapshot.
6. Implement AC4, AC5, AC7 and AC8: no member with capacity, no cap, the repeated run, the held cases and the owner exactly at the cap, with the exact counts and messages.
7. Implement AC6 and AC11 through the agreed test-only fault switch on the P3 decision-record library, and the ledger completeness assertion that measures each collection against five minutes.
8. Implement AC9 and AC10, prove over the call set that no lake endpoint is called, write the evidence report, remove the fixtures, restore the clock and run the suite in SIT against the wave 1 release candidate.

Done when: all twelve test cases pass in SIT against the published wave 1 contracts of P1, P3, P7 and P9, the 06:30 Schedule moves the cases by the queue method with one record per move, every queue measure of 2026-12-02 reconciles to the case list and reaches rwb-reporting with no lake call, every decision record is collected inside the five-minute target, the evidence report is published to the wave 1 exit gate, and no service code or schema was changed by this story apart from the agreed test-only fault switch.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-011 | Cases left without an owner | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-028 | Service level breach alert | {count} cases in {queue} are past their service level. |
| MSG-P3-029 | Snapshot does not reconcile | The queue measures for {date} were not published: {check}. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The reconciliation and collection result is reported as one line of the evidence report and carries no message ID: {collected} of {expected} queue measures of business date {date} were reconciled and published, the slowest in {seconds} seconds. The message IDs and wording are copied from RWB-E1-030. No new message ID is added by this story. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built or tested by this story. SCR-02 Case list (states: empty, loading, filtered; error and no access: Not specified in the source documents (CG-ALL-305)) shows the new owner after a move, and the suite reads the same owner through `GET /api/recovery/case/v1/cases/{caseId}`. SCR-09 Exception queue (states: list, loading; empty, error and no access: Not specified in the source documents (CG-ALL-307)) shows the cases left without an owner behind MSG-P3-011, which the suite asserts on the message and the count. The Power BI queue page is built by RW-BIANAL from the P9 measures read in section 12.2, not by this story. SCR-07 team queues (states: loading; empty, error and no access: Not specified in the source documents (CG-ALL-306)) and the steering dashboard come in Epic 2 and are out of scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-030-01-ITG | AC1, BR1, BR7 | Integration | 12 cases with no owner, U-61 at 140 and U-62 at 144 open cases; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-02-ITG | AC2, BR6 | Integration | Synthetic snapshot at 2026-12-02 06:52, depth 296 and average age 41 days for TDR-BKK-CO; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-03-ITG | AC3, BR8 | Integration | One breach in TDR-BKK-CO on case RW-2026-000501; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-04-ITG | AC4 | Integration | Every member at 150 open cases, 5 cases with no owner; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-05-ITG | AC5, BR4 | Integration | Queue WO-BKK-CO with no cap; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-06-ITG | AC6, BR7 | Integration | Owner U-63 at 153 open cases, the record write failing for one case; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-07-ITG | AC7 | Integration | The rebalancing Schedule run twice on 2026-12-02; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-08-ITG | AC8, BR3 | Integration | Owner U-64 at 152 open cases with 2 held cases; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-09-ITG | AC9, BR6 | Integration | Depth 88 against case count 87 for DIL-BKK-CO; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-10-ITG | AC8, BR2 | Integration | Owner U-65 at exactly 150 open cases; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-11-ITG | AC10 | Component | RW-CASEOWN test user U-7101 reruns the rebalancing run and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-12-ITG | AC11 | NFR | The decision-record write forced to fail for every move in the run; end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-13-ITG | §12.2, §12.4 | Contract | Every operation in section 12.2 and every event in 12.4 called and published on the real SIT service; no new numeric business values |
| TC-E1-030-14-ITG | AC12, BR5, BR9, BR10, BR11, BR12 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1030-ITG-AC12); end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-15-ITG | AC13 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1030-ITG-AC13); end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-16-ITG | AC14, BR7, BR12 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1030-ITG-AC14); end-to-end: real services on the wave 1 contracts; no new numeric business values |
| TC-E1-030-17-ITG | AC15, BR5 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E1030-ITG-AC15); end-to-end: real services on the wave 1 contracts; no new numeric business values |

The twelve legacy test case IDs of RWB-E1-030 are kept as ITG copies with the suffix `-ITG`, in their legacy order. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case id.

### 17. Guardrails

- No business value in code: caps, queue methods and measure definitions are data rows read through the parameters and reference contracts (DL23, DL25).
- No personal data in the snapshot, the alerts, the events, the logs, the evidence or the fixtures; the snapshot holds counts and ages only.
- No cross-service table read and no schema change: every assertion is a contract response or an event, every write is a call to the owner's own path (DP-01), and the only change in a running service is the agreed test-only fault switch of section 12.8.
- One hop and a 2 s timeout on every call (ADR-020, DP-11), and a timeout is never retried into a pass.
- The harness clock is the test input and the durable timers inside CaseWorkflow are the service's own; the suite moves only its own, and it never starts, moves or stops the Schedule, because the rerun goes through the owner's job catalogue.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG and reset to its fixture state after a run, with no production access of any kind from the suite or its configuration; the suite refuses an environment that is not SIT.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-015 | Daily rebalancing; queue counts, ageing and breaches reported | The JOB-06 Schedule, `GET /api/recovery/case/v1/queues`, `/queues/{queueId}/cases`, `/cases`, `/cases/{caseId}`, `/cases/{caseId}/timers`, MSG-P3-011, MSG-P3-028 | TC-E1-030-01-ITG, TC-E1-030-03-ITG, TC-E1-030-04-ITG, TC-E1-030-05-ITG, TC-E1-030-06-ITG, TC-E1-030-07-ITG, TC-E1-030-08-ITG, TC-E1-030-10-ITG, TC-E1-030-11-ITG |
| REQ-RDF-012 | Baseline measures for cases by queue and age published | `GET /api/recovery/reporting/v1/reports/measures`, `GET /api/recovery/case/v1/cases`, rwb.reporting.ReportPublished.v1, MSG-P3-029 | TC-E1-030-02-ITG, TC-E1-030-09-ITG |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The JOB-06 Schedule at 06:30 with overlap SKIP, and the rerun through the P1 job catalogue | TC-E1-030-01-ITG, TC-E1-030-07-ITG, TC-E1-030-10-ITG |
| ADR-022 | Local decision record plus central ledger | rwb.decision.DecisionRecorded.v1 on `rwb.decision-record.v1` and `GET /api/recovery/decision/v1/decision-log` within five minutes | TC-E1-030-06-ITG, TC-E1-030-12-ITG |
| DP-17 | No data lake; reporting from events into rwb-reporting | The measured projection on the P9 contract and the absence of a lake endpoint in the call set | TC-E1-030-02-ITG |
| DP-01 | Owner's schema, never another service's tables | One writer per schema; the suite asserts through contracts | All |

The legacy AC1 to AC10 at component level belong to RWB-P3-E1030-APP and RWB-P7-E1030-APP, not to this story.

### 19. Out of scope

- The P3 and P7 APP builds and their unit and component tests, including the Schedule registration, the assignment and cap logic, the snapshot and the ledger consumer.
- The CON, DB and OPS stories of P1, P3, P7 and P9.
- Quartz, the ACE shared batch tables and the data lake copy of the snapshot, all removed from the target (DP-10, DP-17).
- SCR-07 team queues, the steering dashboard of Epic 2 and the Power BI report layout, which RW-BIANAL owns on the P9 measures.
- The build of the harness RWB-ITG-W1J01-ITG, which is a precondition here and not a deliverable, and NFR load and performance testing of the non-functional epic RWB-ITG-NFR.

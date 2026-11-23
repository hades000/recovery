# RWB-ITG-E6017-ITG Route the population to the committee and schedule it

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6017-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S7-E6017-APP, RWB-P3-E6017-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-017 as the wave 4 integration proof that the write-off pack reaches the committee queue, that the case and its meeting clock are set in rwb-case, and that the decision is in the ledger. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member**, I want **a wave 4 harness that proves the pack for a cut-off date reaches the committee queue, that the case state and its meeting clock are set by rwb-case, and that the route decision is in the central ledger with its rule version, against the owning services' published contracts and their fakes**, so that **no write-off waits in the wrong queue or misses its meeting because a cross-service step failed silently between the scan and the committee**.

This story builds the harness and the evidence, and nothing else. The scan, the pack and the route are S7's, built in RWB-S7-E6017-APP; the committee queue, the case state and the meeting clock are P3's, built in RWB-P3-E6017-APP; the central ledger is P7's and the deviation is S8's. The story builds no production endpoint, no table, no workflow, no schedule and no screen. It drives the population from the one operation the Ownership Map publishes for a scan, and asserts only what is observable through the owners' published operations.

This story owns no legacy acceptance criterion. All four legacy acceptance criteria of RWB-E6-017 sit with RWB-S7-E6017-APP and RWB-P3-E6017-APP; the six criteria in section 7 are new and test the cross-service wiring alone.

### 2. Business rationale

R-WO-11 says a pack inside the committee limit is routed to the committee and the meeting is scheduled before the scheduled meeting. The rule is one row in a routing table, but it lands in three services at once: rwb-writeoff builds and routes the pack, rwb-case moves the case to WITH_COMMITTEE and places it in the committee queue with a meeting clock, and the route is written to the local decision record and to the central ledger with its rule version. Each service can pass its own tests while the seam between them fails.

The failure is quiet, which is why the seam needs its own proof. A case can sit in WITH_COMMITTEE and still be in the recovery officer's queue, so the officer keeps working a case the committee already owns. A pack can be routed twice in one meeting month and the case can carry two meeting clocks, so the committee meets on the wrong date. A route can be taken with no ledger entry, so the decision exists in the workflow and nowhere that an auditor, a complaint handler or a reporting measure can find it. A deviation raised after the population is proposed can reach the committee because nothing on the seam re-reads the case before the route. Each of these is a wrong decision on a charged-off balance, and none of them shows up as an error in a service log.

The harness is decoupled the way the services are. Every path is the owner's published operation on `/api/recovery/<short>/v1` (DP-13), one hop and a 2 s budget (DP-11, ADR-020), and no service reads another service's schema (DP-01). The route decision goes through the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03), and where a screen would compose the queue, the case and the clock the path would be the gateway-bff composite route (DP-19). It carries REQ-S7-002, REQ-S7-003 and REQ-S7-004 into evidence rather than restating them.

The map publishes no read operation for a write-off record and no meeting-booking operation. This story states that plainly and does not invent one: the harness identifies the case through the DP13 records read of P1 and the case contract of P3, and it observes the routing through the state, the queue, the clock and the ledger rather than through a write-off read.

### 3. Preconditions

- The published contracts of S7 rwb-writeoff (the scan and the committee decision), P3 rwb-case (case, queues, queue cases, timers), P7 rwb-decision (the decision log), S8 rwb-deviation (deviations), P1 rwb-source-data (DP13 records) and P4 rwb-access (session) are in the contract registry, and a stub set is generated from each one with its version pinned.
- The case under test is in PACK_PREPARED for cut-off date 2026-07-03, with the pack built under R-WO-05 (PACK_BUILT to PACK_PREPARED) and the balance and the provision carried in the pack read from DP13 Money and closure.
- The write-off committee queue WO-COMM-MTG exists in rwb-case with role RW-WOCOMM, and the recovery officer queue MTG-BKK-CO exists as the queue the case came from.
- The committee meeting calendar fixture holds one meeting date, 2026-07-15, for meeting month 2026-07, and it is read as data.
- RWB-S7-E6017-APP and RWB-P3-E6017-APP own the scan, the route, the queue placement and the meeting clock. Until they land, the stubs of section 12.8 answer in their place on Day 1.
- The harness environment and base hosts, the committee queue code in the real environment, the committee meeting calendar, the shape of the scan answer and how the population and its removals are listed, the timer type and warning settings of the meeting clock, the evidence format and retention, the pass or fail gate, and the synthetic case keys: Not specified in the source documents (GAP-0455; ASM-0647).
- No build dependency. Day 1, with the stubs in place from the first run; the two I stories replace their stubs and never block the lane.

### 4. Flow

1. Harness: loads the fixture for cut-off date 2026-07-03: case RW-2026-000617 in PACK_PREPARED, its balance and provision carried from DP13 Money and closure, queue WO-COMM-MTG for the committee, the source queue MTG-BKK-CO, and the meeting date 2026-07-15 for meeting month 2026-07.
2. Harness: posts the population for the cut-off date through `POST /api/recovery/writeoff/v1/write-off-scans` with the cut-off date, the meeting month and one Idempotency-Key. On Day 1 the stub of section 12.8 answers in place of RWB-S7-E6017-APP.
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the state before the route is PACK_PREPARED and after it is WITH_COMMITTEE (R-WO-11).
4. Harness: reads `GET /api/recovery/case/v1/queues` to find queue WO-COMM-MTG by its code, then `GET /api/recovery/case/v1/queues/{queueId}/cases` and asserts case RW-2026-000617 is in the committee queue and is no longer returned for queue MTG-BKK-CO.
5. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts exactly one committee meeting timer, with expires_at equal to the booked meeting date 2026-07-15 and status running.
6. Harness: reads the money carried in the pack through `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` and asserts the balance and the provision are the ones the fixture holds. The write-off record has no published read operation in the map, so the case is identified through DP13 and the rwb-case contract and never through a write-off read.
7. Harness: posts the same cut-off date again for the same meeting month with the same Idempotency-Key, and asserts that no second timer and no second queue placement is written for the case.
8. Harness: raises the deviation path: a deviation on the case (rwb.deviation.DeviationRaised.v1 on rwb.deviation.events.v1, whose consumer is rwb-case) holds the case out of the next population, moves it to CASE_REMOVED_BY_TEAM (R-WO-06), names the deviation owner on the case, and keeps it out of WITH_COMMITTEE.
9. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts exactly one entry for the routing of the case, with rule R-WO-11 and its rule version, hash-chained to the previous entry of the case.
10. Harness: forces the failure path: with the central ledger and the local decision record unavailable, the route is not taken, the case stays in PACK_PREPARED, no queue placement and no timer is written, and the answer carries MSG-P7-003.
11. Harness: reads `GET /api/recovery/access/v1/me/session` for the caller and posts the scan as a synthetic caller with role RW-OFF and no Write-off and posting C, and asserts 403 with MSG-P4-002 and no scan started.
12. Harness: writes one run report keyed by story and cut-off date, naming the contract version of each hop, whether the hop was a stub or the owner, the meeting month, the queue, the clock, the ledger entry and the six criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-017-01-ITG (ITG AC1) |
| X2 | The pack under test is not in PACK_PREPARED when the route runs | The run fails on AC1 and the report names the case and the state it read; a route with no prepared pack is never reported as routed | None | TC-E6-017-01-ITG (ITG AC1) |
| X3 | The case is in the committee queue and still in the officer queue | The run fails on AC1 and the report names both queue codes and the case, so a double placement is a failure and not a pass | None | TC-E6-017-01-ITG (ITG AC1) |
| X4 | A second route in one meeting month adds a second timer or a second placement | The run fails on AC2 and the report names the meeting month, the two timer rows and the two placements | None | TC-E6-017-02-ITG (ITG AC2) |
| X5 | A case with an open deviation reaches WITH_COMMITTEE | The run fails on AC3 and the report names the deviation code, the deviation owner and the state it read | None | TC-E6-017-03-ITG (ITG AC3) |
| X6 | The route is taken with no ledger entry, or the chain does not link to the previous entry | The run fails on AC4 and the report names the case, the operation and the chain position; an unrecorded route is never reported as recorded | MSG-P7-003 (expected, and missing) | TC-E6-017-04-ITG (ITG AC5) |
| X7 | A caller without Write-off and posting C starts a scan | The run fails on AC6 and the report names the caller role and the operation; a scan that started is reported as started | MSG-P4-002 (expected, and missing) | TC-E6-017-05-ITG (ITG AC6) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only waits are RWB-S7-E6017-APP and RWB-P3-E6017-APP, and their stubs answer until they land |
| Negotiable | The fixture layout, the queue code, the meeting calendar, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The seam from the scan to the committee queue, the meeting clock and the ledger is proven once, end to end, before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, four assertions and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion runs against the stubs and again against the real owners as the two I stories land |

### 7. Acceptance criteria

```gherkin
Feature: Route the population to the committee and schedule it - wave 4 committee routing harness

  Background:
    Given the population for cut-off date "2026-07-03" has proposed case "RW-2026-000617" and its pack is in "PACK_PREPARED"
    Given the pack for case "RW-2026-000617" carries the balance and the provision of DP13 "Money and closure"
    Given the write-off committee queue "WO-COMM-MTG" exists in rwb-case with role "RW-WOCOMM"
    Given the recovery officer queue "MTG-BKK-CO" holds case "RW-2026-000617"
    Given the committee meeting calendar fixture holds meeting date "2026-07-15" for meeting month "2026-07"

  Scenario: AC1 The pack reaches the committee queue and the case waits there (new, D-RCV-60)
    Given case "RW-2026-000617" is in state "PACK_PREPARED" under "PACK_BUILT" of rule "R-WO-05"
    When the route step runs for the case against rule "R-WO-11" and its rule version
    Then the case read through "GET /api/recovery/case/v1/cases/{caseId}" is in state "WITH_COMMITTEE"
    And "GET /api/recovery/case/v1/queues/{queueId}/cases" for queue "WO-COMM-MTG" returns case "RW-2026-000617"
    And queue "MTG-BKK-CO" no longer returns case "RW-2026-000617"

  Scenario: AC2 The meeting is booked once and the case carries the meeting clock (new, D-RCV-60)
    Given case "RW-2026-000617" has been routed to the committee for meeting month "2026-07"
    When "GET /api/recovery/case/v1/cases/{caseId}/timers" is read for the case
    Then the answer holds one committee meeting timer
    And its expires_at equals the booked meeting date "2026-07-15"
    And its status is "RUNNING"
    When the same case is routed again for meeting month "2026-07"
    Then no second timer is added and no second queue placement is written

  Scenario: AC3 An open deviation holds the case out of the population (new, D-RCV-60)
    Given case "RW-2026-000617" is in state "POPULATION_PROPOSED"
    And a deviation is raised on the case and "rwb.deviation.DeviationRaised.v1" is published
    When the scan runs for the next cut-off date
    Then the case is left out of the population
    And the case read through "GET /api/recovery/case/v1/cases/{caseId}" is in state "CASE_REMOVED_BY_TEAM"
    And the deviation owner is named on the case
    And the case never reaches "WITH_COMMITTEE"

  Scenario: AC4 The decision is recorded with the rule version and the ledger holds it once (new, D-RCV-60)
    Given case "RW-2026-000617" has been routed to the committee under rule "R-WO-11"
    When the route decision is written
    Then the entry carries rule "R-WO-11" and its rule version
    And "GET /api/recovery/decision/v1/decision-log?caseId={caseId}" returns exactly one entry for the case and the routing
    And the entry is hash-chained to the previous entry of the case

  Scenario: AC5 The route is not taken when the decision cannot be recorded (new, D-RCV-60)
    Given case "RW-2026-000617" is in state "PACK_PREPARED"
    And the central ledger and the local decision record are both unavailable
    When the route step runs for the case
    Then the case stays in "PACK_PREPARED"
    And no queue placement and no timer is written
    And the answer carries "MSG-P7-003"

  Scenario: AC6 A caller without the right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Write-off and posting C
    When the caller posts a population for cut-off date "2026-07-03"
    Then the answer is 403 with "MSG-P4-002"
    And no scan starts
```

The four legacy acceptance criteria belong to RWB-S7-E6017-APP and RWB-P3-E6017-APP, and the six criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A pack inside the committee limit is routed to the committee and its meeting is scheduled before the scheduled meeting | R-WO-11 |
| BR2 | A prepared pack is prepared from case and provision data with no manual assembly, and PACK_BUILT leaves it in PACK_PREPARED | R-WO-05; REQ-S7-002 |
| BR3 | A case with an open deviation in X1 to X7 is held out of the population, routed to the deviation handler and moved to CASE_REMOVED_BY_TEAM | R-WO-06; REQ-S7-004 |
| BR4 | The committee decision is recorded against the case, and the route that put it there is recorded with its rule version | R-WO-11; REQ-S7-003 |
| BR5 | The case state and the queue placement are held by rwb-case, never written by the caller of the scan | Arch v5 slide 41; DP-01 |
| BR6 | The route decision is written locally and published as DecisionRecorded on the shared topic, and the ledger is rwb-decision's | Arch v5 slides 20 and 42; DP-03 |
| BR7 | The scan runs from JOB-16 on the 3rd working day of the month | Arch v5 slide 44; JOB-16 |

The harness asserts these rules and changes none of them.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PACK_PREPARED | PACK_ROUTED | The pack is inside the committee limit and the meeting is scheduled | WITH_COMMITTEE (R-WO-11) |
| POPULATION_PROPOSED | CASE_HAS_OPEN_DEVIATION | A deviation in X1 to X7 is open on the case | CASE_REMOVED_BY_TEAM (R-WO-06) |
| POPULATION_PROPOSED | PACK_BUILT | The pack is prepared from case and provision data | PACK_PREPARED (R-WO-05) |
| PACK_PREPARED | The route cannot be recorded | The central ledger and the local decision record are unavailable | PACK_PREPARED, unchanged |

The harness changes no state. Every change in the table is made by the owner: S7 rwb-writeoff scans, builds and routes the pack, P3 rwb-case moves the case, places it in the queue and sets the meeting clock, S8 rwb-deviation raises the deviation, and P7 rwb-decision holds the central ledger. The harness reads and asserts, and the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WOCOMM, write-off committee member | Reads the committee queue and the meeting clock of a case; the role the committee queue is worked by |
| RW-WRITEOFF | Holds Write-off and posting C and runs the population for a cut-off date |
| RW-CREDITAD, RW-PRODHEAD, RW-FINANCE | Hold Write-off and posting A and the committee decision; they sit outside this story and its out of scope |
| RW-OFF, recovery officer | Reads the case and its queue; the synthetic caller of AC6 holds this role and no Write-off and posting C |
| RW-TRIBE, RW-PLATADM | Read the same run report and the queue configuration; they hold no write-off right |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S7 rwb-writeoff scans and routes, P3 rwb-case holds the case, the queue and the timer, P7 rwb-decision holds the ledger, S8 rwb-deviation raises the deviation, P1 rwb-source-data answers DP13 and P4 rwb-access answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; the authorisation is answered by rwb-access and the committee decision is out of scope |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, status, stage_code, route_state, owner_user_id, queue_id, deviation_open, rule_version | Read through the rwb-case contract |
| DF-CAS-036 to DF-CAS-045 | deviation | case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, cleared_at, outcome | Read through the rwb-deviation contract; S8 owns the table |
| DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038 | queue | queue_code, queue_name, team_code, role_code, assignment_method | Read through the rwb-case contract |
| DF-WRK-045 to DF-WRK-052 | queue_member | queue_id, user_id, capacity, skill_codes | Read through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036, DF-WRK-041 to DF-WRK-044 | timer | case_id, timer_type, started_at, expires_at, warn_at, paused, status | Read through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018, DF-DEC-028 to DF-DEC-031 | decision_log_entry | case_id, decision_code, rule_id, rule_version, inputs_ref, final_call, prev_hash, entry_hash, chain_seq | Read through the rwb-decision contract; P7 owns the ledger |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code, to_state, owner_role, timer_spec | Read through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8. queue, queue_member and timer are P3's tables; deviation is S8's; decision_log_entry and rule_row are P7's; recovery_case is P3's. The harness owns no table and writes no row. The balance and the provision carried in the pack are read from DP13 Money and closure through the rwb-source-data data-product contract, never from a view and never from a table.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/writeoff/v1/write-off-scans` | S7 rwb-writeoff | The population for a cut-off date, with one Idempotency-Key (AC1, AC2, AC3, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The state of the case, PACK_PREPARED, WITH_COMMITTEE or CASE_REMOVED_BY_TEAM (AC1, AC3, AC5) |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | The committee queue and the officer queue, by queue_code (AC1) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | The case in the committee queue and its absence from the officer queue (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The meeting clock: one committee meeting timer, its expires_at and its status (AC2, AC5) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | Exactly one ledger entry for the routing, the rule version and the hash chain (AC4) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The balance and the provision carried in the pack (AC1, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's role and rights before the scan (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13, ADR-020). No operation is invented in this story: each path is the owner's published operation. The map publishes no read operation for a write-off record and no meeting-booking operation, so the harness identifies the case through DP13 and rwb-case and observes the booking through the timers of rwb-case. Where a screen would compose these calls the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Consumers in the sources | Use in this run |
|---|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | rwb-comms, rwb-reporting | Waits for the move to WITH_COMMITTEE and to CASE_REMOVED_BY_TEAM (AC1, AC3) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, rwb-writeoff for this route | rwb-decision, rwb-reporting | Waits for the route decision to be published before the ledger is read (AC4) |

The harness also observes `rwb.deviation.DeviationRaised.v1` on `rwb.deviation.events.v1`, produced by S8 rwb-deviation with rwb-case, rwb-comms and rwb-treatment as consumers, to know that the deviation is open before the scan (AC3). The harness neither produces nor consumes that event itself; the move of the case is rwb-case's.

#### 12.5 Workflows and activities

Observed, not built here. `WriteOffWorkflow` runs on task queue `rwb-writeoff` in namespace `rwb-recovery` and carries the monthly write-off stages: the scan proposes the population (R-WO-01 and R-WO-03), the pack is built in 3 working days (R-WO-05), the pack is routed and the committee decides (R-WO-11 to R-WO-17), and the later posting and provision steps follow. The harness triggers the first stage through the owner's scan operation and observes the route and committee stage through the case state, the queue, the clock and the ledger. It builds no workflow, no activity and no child workflow; the committee approval child of rwb-decision is out of scope.

#### 12.6 Schedules

JOB-16, observed and not changed: a Temporal Schedule in rwb-writeoff that runs the write-off scan monthly on the 3rd working day (Architecture v5 slide 44; Temporal and Drools Design v1 slide 23; Ownership Map). The harness runs its population for a cut-off date through the scan operation and sets no cron; it neither creates, pauses nor changes the Schedule. The committee meeting cadence and the booking target behind the meeting clock are Not specified in the source documents (GAP-0455; ASM-0647).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). queue, queue_member and timer are P3's, recovery_case is P3's, deviation is S8's, decision_log_entry and rule_row are P7's, and the pack's money comes from P1's DP13.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-writeoff | `POST /write-off-scans` and `POST /write-offs/{writeOffId}/committee-decision` | Accepts one population per cut-off date and Idempotency-Key, proposes case RW-2026-000617, and records the route for meeting month 2026-07; refuses a caller without Write-off and posting C with 403 and MSG-P4-002; answers MSG-P7-003 when the decision record cannot be written |
| Stub for rwb-case | `GET /cases/{caseId}`, `/queues`, `/queues/{queueId}/cases`, `/cases/{caseId}/timers` | The case RW-2026-000617 moving from PACK_PREPARED to WITH_COMMITTEE, or to CASE_REMOVED_BY_TEAM on the deviation path; queue WO-COMM-MTG holding the case and queue MTG-BKK-CO not; one committee meeting timer with expires_at 2026-07-15 and status RUNNING |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | Exactly one entry for the routing of case RW-2026-000617 with rule R-WO-11 and its rule version, prev_hash equal to the entry_hash of the previous entry of the case, and an empty answer when the ledger is forced unavailable |
| Stub for rwb-deviation | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` | Raises one deviation on the case with its code, its raised_at and a handler, and publishes the deviation as open for the scan |
| Stub for rwb-source-data | `GET /data-products/DP13/records?caseId={caseId}` | The balance and the provision of DP13 Money and closure for case RW-2026-000617, with the business date and the load time |
| Stub for rwb-access | `GET /me/session` | Allows RW-WRITEOFF with Write-off and posting C; answers RW-OFF with the role and without Write-off and posting C |
| Committee calendar fixture | The committee meeting calendar | One meeting date, 2026-07-15, for meeting month 2026-07, and no second meeting inside the month |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the committee queue code in the real environment, the committee meeting calendar, the shape of the scan answer, the timer type and warning settings of the meeting clock, the evidence format and retention, the pass or fail gate, and the synthetic case keys are Not specified in the source documents (GAP-0455; ASM-0647).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, CaseStateChanged and DecisionRecorded, and DeviationRaised observed through its consumer rwb-case |
| Temporal | None added; WriteOffWorkflow on task queue `rwb-writeoff` is exercised through the scan operation, and JOB-16 is observed and not changed |
| File | The committee calendar fixture and the run report, both read or written as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependency that DP-03 adds, RWB-PLT-E1027-CON, is a platform story delivered by the platform wave and is not repeated in the metadata H field of this story, which stays empty; the same holds for RWB-PLT-N001-CON from DP-19. The two blocking dependencies are the I stories RWB-S7-E6017-APP and RWB-P3-E6017-APP, which replace their stubs; until they are live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for a cut-off date and holds the run lock |
| StubSet | Fake | The six stubs of section 12.8 generated from the published contracts, with each contract version pinned |
| CommitteeCalendarFixture | Fixture | The meeting date 2026-07-15 for meeting month 2026-07, and the queue codes of the committee and the officer queue |
| StateAssertion | Service | Reads the case state and both queue member lists and names any case that is in two queues or in none |
| ClockAssertion | Service | Reads the timers of the case: one committee meeting timer, its expires_at equal to the booked meeting, its status running, and no second timer on a repeated route |
| LedgerAssertion | Service | Reads the decision log for the case: exactly one entry for the routing, the rule and its version, and the hash chain to the previous entry |
| EvidenceReport | Service | Writes one report per cut-off date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the two I stories land, on synthetic case RW-2026-000617, cut-off date 2026-07-03, meeting month 2026-07, meeting date 2026-07-15, committee queue WO-COMM-MTG, officer queue MTG-BKK-CO, role RW-WOCOMM for the committee queue and a synthetic RW-OFF caller for the refusal path. Every value is fixture data and none is written in code. The harness environment and base hosts, the committee queue code, the committee meeting calendar, the shape of the scan answer, the timer type and warning settings, the evidence format and retention, the pass or fail gate, and the synthetic case keys are Not specified in the source documents (GAP-0455; ASM-0647). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the six stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CommitteeCalendarFixture and prove the meeting date and the queue codes are read as data for cut-off date 2026-07-03.
3. Build the JourneyRunner for AC1: post the population for the cut-off date with one Idempotency-Key, read the state through rwb-case, and assert it reaches WITH_COMMITTEE (X2).
4. Add StateAssertion for AC1: the case is in queue WO-COMM-MTG through `/queues/{queueId}/cases` and no longer in queue MTG-BKK-CO (X3).
5. Add ClockAssertion for AC2: one committee meeting timer with expires_at 2026-07-15 and status running, and a repeated route for the same meeting month adds no second timer and no second placement (X4).
6. Add AC3: raise the deviation, post the next population, and assert the case is out of the population, in CASE_REMOVED_BY_TEAM, with the deviation owner named and never in WITH_COMMITTEE (X5).
7. Add LedgerAssertion for AC4 and the failure path of AC5: one entry with rule R-WO-11 and its version, hash-chained to the previous entry, and with the ledger and the local record forced unavailable the case stays in PACK_PREPARED with MSG-P7-003 and no placement or timer (X6).
8. Add the access path for AC6 through `GET /api/recovery/access/v1/me/session` and the scan as a synthetic RW-OFF caller, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S7-E6017-APP and RWB-P3-E6017-APP when they land, and the wave entry check holds a run report keyed by story and cut-off date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S7-001 is asserted when the scan is held for the unpublished tax criteria, MSG-GEN-001 on a scan posted without its cut-off date, MSG-P4-002 on the refusal of AC6 and MSG-P7-003 on the route that cannot be recorded in AC5.

### 15. Screens and states

No screen is built. The states are read through rwb-case and the write-off record the owner holds.

| State | What the harness reads |
|---|---|
| Scan | The population is proposed for the cut-off date and the case is in POPULATION_PROPOSED |
| Proposed | The pack is built and the case is in PACK_PREPARED with its balance and provision carried |
| In committee | The case is in WITH_COMMITTEE, in queue WO-COMM-MTG, with one committee meeting timer |
| Approved | The committee decision is taken on the write-off; the route into it is in the ledger |

The four states are the ones SCR-27 Write-off proposal shows. That screen belongs to RWB-S7-E6017-APP and is out of scope here, and the committee view is not built in this story either. What the wave entry check looks at instead is the run report; its environment, layout and retention are the same missing values named in section 3 and section 12.8.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-017-01-ITG | ITG AC1 | Integration | one scan for a cut-off date with a pack in PACK_PREPARED |
| TC-E6-017-02-ITG | ITG AC2 | Integration | the same case routed twice for one meeting month |
| TC-E6-017-03-ITG | ITG AC3 | Integration | a case in POPULATION_PROPOSED with a deviation raised (X1 to X7) |
| TC-E6-017-04-ITG | ITG AC5 | Integration | a forced decision-record and ledger failure at the route |
| TC-E6-017-05-ITG | Access; ITG AC6 | Component | RW-OFF caller without Write-off and posting C |
| TC-E6-017-06-ITG | Principle 5; ITG AC5 | Integration | a forced decision-record failure stops the route with MSG-P7-003 |

The AC column names the ITG AC each copy asserts, and the four legacy ACs stay with the two APP stories.

### 17. Guardrails

- No business value in code: the case key, the cut-off date, the meeting month and date, the queue codes, the rule version and the report layout are data.
- No personal data in logs, fixtures, events or reports: every key is synthetic and no customer record is read at all.
- ACE data only through the P1 contract, and no read of another service's schema or tables: the case, the queues and the timers come from rwb-case, the ledger from rwb-decision, the deviation from rwb-deviation, and the money from DP13 through rwb-source-data (DP-01, DP-03).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-017 Route the population to the committee and schedule it | Recovery Workbench User Stories Epics 3 to 8 v3, lines 9829 to 9924 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC1 to AC4, and the legacy endpoints and test cases | The same, lines 9848 to 9870, 9882 to 9888 and 9913 to 9920 | No legacy AC is owned here: all four stay with RWB-S7-E6017-APP and RWB-P3-E6017-APP (section 19), the two published S7 paths are in section 12.2, and the six legacy test cases are copied as -ITG in section 16 |
| R-WO-05, R-WO-06 and R-WO-11 | Business Rules and Routing Logic v4, lines 336, 337 and 342 | Sections 7, 8 and 9 |
| JOB-16 write-off scan, monthly on the 3rd working day | Architecture v5 slides 20 and 44; Temporal and Drools Design v1 slide 23; Ownership Map | Sections 12.6 and 13 |
| REQ-S7-002, REQ-S7-003 and REQ-S7-004 | Business Requirements Program v4, lines 393 to 395 | Section 8, BR2 to BR4 |
| DF-CAS, DF-WRK, DF-DEC and DF-REF field IDs | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015 (Kafka with outbox, inbox and CloudEvents) and ADR-020 (contract-first REST, one hop, 2 s) | Architecture Decision Records | Sections 12.2, 12.4 and 13 |
| The write-off pack, its money and the refusal path | Legacy story; DP13 Money and closure | Sections 4, 11 and 12.2 |

No legacy acceptance criterion is owned by this story; the six criteria in section 7 are new and tagged (new, D-RCV-60).

### 19. Out of scope

- RWB-S7-E6017-CON and RWB-S7-E6017-APP: the scan, the pack build, the route, the committee step and the write-off contract.
- RWB-P3-E6017-APP: the case state, the committee queue, the queue placement and the meeting clock.
- The four legacy acceptance criteria of RWB-E6-017, which stay with those two stories.
- The scan and the eligibility rules (RWB-E6-013) and the tax criteria (RWB-E6-014).
- The pack build (RWB-E6-015) and the removal from the population by the team (RWB-E6-016).
- The committee decision (RWB-E6-018 to RWB-E6-020), the posting and the provision release that follow it.
- SCR-27 Write-off proposal and the committee view.
- The committee meeting calendar itself, its cadence and its booking target.
- Platform deployment and configuration.

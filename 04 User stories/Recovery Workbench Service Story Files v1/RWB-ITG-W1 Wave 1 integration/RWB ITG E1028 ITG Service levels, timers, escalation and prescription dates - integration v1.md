# RWB-ITG-E1028-ITG Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-028 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1028-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E1028-APP, RWB-P4-E1028-APP, RWB-P7-E1028-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020, FR-PLT-022, FR-PLT-023) |
| Status | Draft (realignment v1) |

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-028 clocks across rwb-case (P3, the owner of the timer and of the CaseWorkflow), rwb-access (P4, the refusal) and rwb-decision (P7, the decision record) in SIT**, so that **the durable timer, the warning, the escalation, the prescription date, the missing-parameter paths, the catch-up after a worker outage and the stage-clock pause are proved on real wave 1 services before the wave exits**.

### 2. Business rationale

The legacy story starts a SERVICE_LEVEL timer each time a case enters a queue and status, warns the owner at the warning percentage, raises a breach to the named escalation role without moving the case, and sets the prescription date at case creation from the last payment date, the contract date and the legal period for the product. It runs the check in JOB-05 on Quartz every five minutes, publishes `TimerBreached` and `TimerDue`, pauses the stage clock on `DeviationRaised` and resumes it on `DeviationCleared`, and reads the timers through `GET /cases/{caseId}/timers` (RWB-E1-028 sections 4, 12 and 13).

The target keeps the behaviour and changes the machinery. Under ASM-0078 the clock is a **durable Temporal timer inside `CaseWorkflow`** on `rwb-case`, so the timer survives a restart, a release and a Continue-As-New, and a fire that fell inside an outage is satisfied on recovery from history. **JOB-05 and its five-minute Quartz schedule are retired, and the `TimerDue` event with it**: event catalogue #18 is marked retired as "timer inside the workflow" (Architecture v5 slide 42) and the job map shows JOB-05 as "durable timers (retired)" (slide 44). The `timer` row stays as a **P3 projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`**, so the screens and the read contract do not change. **`TimerBreached` stays on `rwb.case.events.v1`**, produced by rwb-case, with gateway-bff as the inbox consumer (event catalogue #19). Service levels and the timer parameters come from the **P3 parameter contract** (DP-06); the legal periods, the list values and the holiday calendar come from the **P3 reference-data contract** (DP-07). Account dates — the last payment date and the contract date — are reachable only through P1 rwb-source-data under DP-05, which is exercised inside RWB-P3-E1028-APP and is not called by this suite. The deviation service is wave 2, so at wave 1 the stage-clock pause is triggered **through the P3 case action contract** and the `DeviationRaised` path is proved in RWB-ITG-W2. Every consumed call is one hop with a 2 s timeout (ADR-020), every topic carries the owner's name (DP-14), and the two screens are read through gateway-bff (DP-19).

The target split of the legacy key is therefore: **RWB-P3-E1028-APP** owns the durable timer in `CaseWorkflow`, the timer projection, the warning, the breach, the catch-up, the prescription calculator and the pause; **RWB-P4-E1028-APP** owns the Case record R right and its refusal; **RWB-P7-E1028-APP** owns the decision record and the read of the central ledger. **The twelve legacy acceptance criteria AC1 to AC12 stay with RWB-P3-E1028-APP and the access side stays with RWB-P4-E1028-APP.** This integration story owns no legacy acceptance criterion: it owns the twelve new scenarios of section 7, which test only the cross-service deliverable and assert what no single service can assert alone — that the timer the workflow holds is the timer the projection shows, that the breach reaches the team manager on the P3 topic with exactly one decision record, that a decision log failure holds the escalation at level 0 and that the pause moves one clock and not the other.

Where the sources do not publish the exact surface the suite needs, the suite asserts through the owners' contracts and records the open point as GAP-0353 and ASM-0447: the Temporal timer visibility surface, the departure of the P1 account-date and holiday input from this slice, and the move of the wave 1 pause onto the P3 case action contract. Release 30 November 2026 stays tentative, and a date is never a condition of this story.

### 3. Preconditions

- RWB-P3-E1028-APP is done: the durable SERVICE_LEVEL and PRESCRIPTION timers inside `CaseWorkflow`, the timer projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, the warning and breach branches, the catch-up on recovery, the prescription calculator, the pause and resume, and the publication of `TimerBreached` on `rwb.case.events.v1`.
- RWB-P4-E1028-APP is done: the Case record R right and its 403 refusal with MSG-P4-002 are enforced by rwb-access on the case and timer reads.
- RWB-P7-E1028-APP is done: the decision record of a warning and of a breach is written, collected into the central ledger and readable through `GET /api/recovery/decision/v1/decision-log` with the rule ID and version.
- The published contracts of P3 rwb-case, P4 rwb-access and P7 rwb-decision are deployed in SIT under `/api/recovery/<short>/v1` behind gateway-bff, and the harness RWB-ITG-W1J01-ITG is available with its synthetic case and account set.
- The SERVICE_LEVEL row for product group `HIRE_PURCHASE` and status `ASSIGNED` is loaded as a parameter row (5 working days, warning percent 80, escalation role RW-TEAMMGR) through the P3 parameter contract, and the LEGAL_PERIOD row for `HIRE_PURCHASE` (2 years from the last payment date) and the legal-period warning parameter are loaded as reference rows through the P3 reference-data contract; the non-working days 2026-12-05 to 2026-12-07 are loaded in the same calendar.
- SIT is in place: namespace `rwb-recovery`, the task queues `rwb-case`, `rwb-access` and `rwb-decision`, and the topics `rwb.case.events.v1`, `rwb.decision-record.v1` and `rwb.decision.events.v1` with their retry and `.dlt` topics.
- The agreed Temporal test-time control (time skipping) can move the workflow clock to the warning point, to the expiry and to 2028-03-15 and restore it afterwards, and the suite can stop and restart the rwb-case worker for the catch-up scenario.
- No production data is used and no production connection is opened; the suite refuses an environment that is not SIT, and release 30 November 2026 is tentative.
- This story has no build dependency, so it is ready on Day 1 under Template and Rules §R5.7; the exact Temporal timer visibility surface and the timer read at a past fire are Not specified in the source documents (GAP-0353; ASM-0447).

### 4. Flow

1. QA integration engineer: seeds the synthetic cases, accounts and reference rows of the harness RWB-ITG-W1J01-ITG, with case RW-2026-000401 in queue `LIT-BKK-OFF` at 2026-12-01 09:00, owner U-31, team `LIT-BKK`, and the SERVICE_LEVEL and LEGAL_PERIOD rows in force; no production data is used.
2. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` before the allocation, and confirms that the case carries no SERVICE_LEVEL timer.
3. System: rwb-case receives `rwb.case.CaseAllocated.v1` from `rwb.case.events.v1`, and `CaseWorkflow` cancels the running SERVICE_LEVEL timer of the case, reads the service level for the new queue and status through the P3 parameter contract, and starts a durable Temporal timer with `expires_at` 2026-12-09 09:00 and `warn_at` 2026-12-08 09:00, counting working days from the P3 reference calendar.
4. System: `CaseWorkflow` writes the local decision record of the timer start in the same transaction as the timer projection row and publishes to `rwb.decision-record.v1`; the projection is served by `GET /api/recovery/case/v1/cases/{caseId}/timers`.
5. Harness: moves the workflow clock through the warning point and reads MSG-P3-003 for owner U-31, then to the expiry and reads `rwb.case.TimerBreached.v1` on `rwb.case.events.v1` for RW-TEAMMGR of team `LIT-BKK` with escalation level 1, then reads `GET /api/recovery/decision/v1/decision-log` for both points and asserts rule R-UNI-30 on the breach.
6. Harness: asserts that the case keeps queue `LIT-BKK-OFF` and owner U-31 through `GET /api/recovery/case/v1/cases/{caseId}`, that the timer projection shows EXPIRED with escalation level 1, and that no `TimerDue` event was produced on any topic.
7. Harness: for case RW-2026-000402, reads the prescription date 2028-03-15 through the case read, the PRESCRIPTION timer with `warn_at` 2027-09-17 through the timer projection, and asserts that the PRESCRIPTION timer keeps its `expires_at` when the stage clock is paused.
8. Harness: runs the negative paths — no SERVICE_LEVEL version in force, no legal period, no last payment date with contract date 2025-06-30 — and asserts the empty timer, the empty prescription date, the exception queue entry with MSG-P3-026 and the contract-date prescription 2027-06-30.
9. Harness: stops the rwb-case worker from 10:00 to 10:40 with three timers passing `expires_at`, restarts it at 10:45 and asserts three breaches, one for each timer, raised once from history; then checks the same timer again and asserts that no second `TimerBreached` is published and that escalation level stays 1.
10. Harness: fails the decision record write at the expiry of case RW-2026-000407, asserts the timer stays RUNNING with escalation level 0 and MSG-P7-003 is recorded, restores the ledger and asserts that the breach is raised by the first run after recovery.
11. Harness: pauses case RW-2026-000408 through `POST /api/recovery/case/v1/cases/{caseId}/actions` on 2026-12-02 and resumes it through the same contract on 2026-12-04, asserts PAUSED for the SERVICE_LEVEL timer with `expires_at` moved by 2 working days, the unchanged PRESCRIPTION timer, and the case record showing MSG-P3-004 with the prescription date.
12. Harness: calls the timer read with a test user holding a role without Case record R and asserts the 403 with MSG-P4-002 from the owning service, then writes the evidence report, removes the synthetic fixtures and restores the clock and the worker.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No SERVICE_LEVEL version is in force on the date | No timer starts, the timer projection is empty for the type, and the case is listed on the exception queue | MSG-P3-026 | AC4 |
| X2 | No legal period for the product | The prescription date is not set, no PRESCRIPTION timer starts, and the case is listed on the exception queue | MSG-P3-026 | AC5 |
| X3 | An account has no last payment date | The contract date is used for the prescription date | None | AC6 |
| X4 | The rwb-case worker is down for 40 minutes and three timers pass `expires_at` | The workflow resumes from history after the restart and raises every missed breach once | None | AC7 |
| X5 | The timer is checked again after a breach | No second `TimerBreached` is published and the escalation level is unchanged | None | AC8 |
| X6 | The decision record cannot be written at the expiry | The timer stays RUNNING with escalation level 0, the workflow records MSG-P7-003, and the breach is raised by the first run after the ledger is back | MSG-P7-003 | AC9 |
| X7 | The stage clock is paused on the case | The SERVICE_LEVEL timer is PAUSED and the PRESCRIPTION timer keeps running | MSG-P3-004 | AC10 |
| X8 | The warning point is 4 of 5 working days | The warning is sent once, at the first fire after 4 working days have passed | MSG-P3-003 | AC2 |
| X9 | A role without Case record R reads the timers | The owning service refuses the read with 403 | MSG-P4-002 | AC11 |
| X10 | A class outside the P3 timer boundary writes or updates the timer row | The build fails on the P3 boundary test and no timer row is changed at run time; the repair goes through the workflow only | None | AC12 |
| X11 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X12 | The Temporal test-time control cannot move the workflow clock, or the worker cannot be stopped and restarted | The suite fails as a harness fault and names the element; no timer, breach or date is asserted | None | AC1, AC7 |
| X13 | The synthetic case and account set does not match the harness RWB-ITG-W1J01-ITG expectations | The suite fails as a fixture fault and names the mismatched element; no service defect is raised | None | AC1, AC3 |
| X14 | A consumed call exceeds the 2 s budget or returns a server error | The call is retried once under the suite policy and the evidence report records it; no assertion is made on data that was not read | None | AC1, AC2 |
| X15 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | Section 17 |

X1 to X10 are the legacy exception paths read on the wave 1 services — X4 and X6 are re-stated on the durable timer and the decision record instead of JOB-05 — and X11 to X15 are the cross-service and harness failures that only appear when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is its own module and reuses the harness RWB-ITG-W1J01-ITG; it needs the three APP stories and the published contracts of P3, P4 and P7, not their source code, and it owns no schema and no table |
| Negotiable | The fixture sizes, the time-skip step, the worker control and the poll windows are properties of the harness; the values, the message IDs and the rules are the legacy ones |
| Valuable | Proves across services what one service cannot prove: the timer the workflow holds is the timer the projection shows, one breach per timer on the P3 topic, one decision record per point, the level stays 0 when the ledger is down, and the pause moves one clock only |
| Estimable | One suite module, one fixture pack, one time control, one worker control, four contract probes and one evidence report |
| Small | Twelve scenarios over three services, four events and one workflow; no service code and no schema change |
| Testable | Every scenario asserts a contract response, an event, a workflow state, a message or a decision record; all data is synthetic |

### 7. Acceptance criteria

```gherkin
Feature: Service levels, timers, escalation and prescription dates, end-to-end across wave 1 services

  Background:
    Given the wave 1 services rwb-case, rwb-access and rwb-decision are deployed in SIT with their published contracts behind gateway-bff
    Given the RWB-ITG-W1J01-ITG synthetic case and account set is loaded and no production data is used
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" and "ASSIGNED" is 5 working days with warning percent 80 and escalation role RW-TEAMMGR
    Given the LEGAL_PERIOD row for "HIRE_PURCHASE" is 2 years from the last payment date
    Given 2026-12-05 to 2026-12-07 are not working days in the calendar served by the P3 reference-data contract

  Scenario: AC1 The timer starts on CaseAllocated and is a durable Temporal timer (new, D-RCV-60)
    Given hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00
    When rwb.case.CaseAllocated.v1 arrives on rwb.case.events.v1
    Then CaseWorkflow starts a SERVICE_LEVEL durable timer for the case
    Then GET /api/recovery/case/v1/cases/{caseId}/timers returns the timer RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00
    Then the timer is held inside the workflow and no TimerDue event is produced

  Scenario: AC2 A passed warning and a passed expiry reach the owner and the team manager once (new, D-RCV-60)
    Given the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at
    When the durable timer fires at each point
    Then owner U-31 receives MSG-P3-003 at the warning point, once
    Then the system raises at expiry the breach to RW-TEAMMGR of team "LIT-BKK" with TimerBreached on rwb.case.events.v1 and escalation level 1
    Then the case keeps queue "LIT-BKK-OFF" and owner U-31
    Then both the warning and the breach have a decision record in GET /api/recovery/decision/v1/decision-log, the breach with rule R-UNI-30

  Scenario: AC3 The prescription date and its timer come from the legal period (new, D-RCV-60)
    Given a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15
    When the case is created
    Then the prescription date is 2028-03-15
    Then a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17
    Then GET /api/recovery/case/v1/cases/{caseId} shows prescription date 2028-03-15
    Then the PRESCRIPTION timer is durable inside CaseWorkflow and is never paused

  Scenario: AC4 No service level for the queue and status (new, D-RCV-60)
    Given no SERVICE_LEVEL version is in force on 2026-12-01
    When case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01
    Then no SERVICE_LEVEL timer starts and the timer read returns no SERVICE_LEVEL timer
    Then the system lists the case on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED"

  Scenario: AC5 No legal period for the product (new, D-RCV-60)
    Given the LEGAL_PERIOD reference rows have no row for "SSME"
    When SSME case RW-2026-000404 is created
    Then the prescription date is empty and no PRESCRIPTION timer starts
    Then the system lists the case on the exception queue with MSG-P3-026 for "legal period" and "SSME"

  Scenario: AC6 No payment ever made uses the contract date (new, D-RCV-60)
    Given a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30
    When the case is created
    Then the prescription date is 2027-06-30

  Scenario: AC7 A worker outage raises every missed breach once on recovery (new, D-RCV-60)
    Given the rwb-case worker is stopped from 10:00 to 10:40 and three timers pass expires_at in that time
    When the worker restarts at 10:45 and the workflows resume from history
    Then the system raises three breaches, one for each timer, once each
    Then no missed fire is lost and no TimerDue event is produced

  Scenario: AC8 A breach is raised once (new, D-RCV-60)
    Given the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1
    When the timer is checked again after the breach
    Then the system publishes no second TimerBreached for the timer
    Then escalation level stays 1

  Scenario: AC9 The decision log unavailable at expiry holds the escalation at level 0 (new, D-RCV-60)
    Given the decision record cannot be written
    When the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at
    Then the timer stays RUNNING with escalation level 0
    Then the workflow records MSG-P7-003 for the timer
    Then the breach is raised by the first run after the decision log is available

  Scenario: AC10 The stage clock pauses and the prescription clock does not (new, D-RCV-60)
    Given case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer
    When the case is paused through POST /api/recovery/case/v1/cases/{caseId}/actions on 2026-12-02 and resumed through the same contract on 2026-12-04
    Then the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days
    Then the PRESCRIPTION timer stayed RUNNING with the same expires_at
    Then the case record shows MSG-P3-004 with the prescription date while the pause was open

  Scenario: AC11 A role without Case record R is refused by the owning service (new, D-RCV-60)
    Given test user "U-7101" holds a role without Case record R
    When the user calls GET /api/recovery/case/v1/cases/{caseId}/timers
    Then rwb-case refuses the call with status 403 and MSG-P4-002
    Then no timer is returned

  Scenario: AC12 Durable timers replace JOB-05 (new, D-RCV-60)
    Given the wave 1 release is deployed with the timers held inside CaseWorkflow
    When the case events of RW-2026-000409 are processed
    Then no TimerDue event is produced on any topic and no Quartz job runs for the timer check
    Then JOB-05 and its 5-minute Quartz schedule are absent from the deployment
    Then the timer state is read only through the P3 projection and the Temporal history of the case workflow
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A SERVICE_LEVEL timer starts each time the case enters a queue or a status, from the SERVICE_LEVEL row for its product group and status, read through the P3 parameter contract | RWB-E1-028 BR1; SERVICE_LEVEL row; DL22; DP-06 |
| BR2 | The warning is raised at the warning percentage of the service level, once | RWB-E1-028 BR2; warning percent 80 assumed (DL22) |
| BR3 | A breach is raised to the named escalation role and the case does not move | RWB-E1-028 BR3; R-UNI-30; REQ-CWC-011; FEAT-CWC-13 |
| BR4 | The prescription date is the earliest of last payment date plus the legal period over the linked accounts, and the contract date applies when no payment exists; the legal periods are read through the P3 reference-data contract | RWB-E1-028 BR4; LEGAL_PERIOD row; REQ-CWC-012; DP-07 |
| BR5 | The PRESCRIPTION timer never pauses | RWB-E1-028 BR5; R-DEV-01; FEAT-DVH-03 |
| BR6 | A pause stops the stage clock only; the resume recomputes the stage dates and leaves the prescription date alone | RWB-E1-028 BR6; R-UNI-04, R-UNI-43 |
| BR7 | A legal hold keeps the clocks running and visible | RWB-E1-028 BR7; R-UNI-20 |
| BR8 | Service levels count working days from the holiday calendar served by the P3 reference-data contract | RWB-E1-028 BR8; DP-07 |
| BR9 | Each timer start, warning and breach is logged with its rule and version | RWB-E1-028 BR9; REQ-CWC-016; Principle 5 |
| BR10 | Timer scheduling goes only through the P3 timer boundary inside `CaseWorkflow`: no caller writes or updates the timer row, and the projection is written by the workflow only | RWB-E1-028 BR10; ASM-0078; ADR-011 |
| BR11 | The clock is a durable Temporal timer inside `CaseWorkflow` on `rwb-case`, so a fire survives a restart, a release and a Continue-As-New | ASM-0078; Temporal and Drools design slides 13 and 24; DP-10 |
| BR12 | The `timer` row stays a P3 projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`; it is the read model, not the clock | ASM-0078; Architecture v5 slide 42 |
| BR13 | `TimerBreached` is produced by rwb-case on `rwb.case.events.v1` with gateway-bff as the inbox consumer (event catalogue #19) | Architecture v5 slide 42; DP-09; DP-14 |
| BR14 | `TimerDue` and JOB-05 are retired: no event of that name is published and no Quartz timer check runs | Architecture v5 slides 42 and 44; ASM-0078 |
| BR15 | Every cross-service call is one hop with a 2 s timeout, and every topic carries the owner's name | ADR-020; DP-11; DP-14 |
| BR16 | No personal data in events, workflow history, logs, the evidence or the fixtures; the case is named by its case number and the owner by user ID | RWB-E1-028 section 17; ADR-015 |

### 9. State transitions

The case status does not change in this story. The timer status does (LOV-TIMER-STATUS), and in the target it is the state of the durable timer inside `CaseWorkflow` as the P3 projection reports it:

| From | Event | Condition | To |
|---|---|---|---|
| None | CaseAllocated, CaseTransferred, CaseStateChanged | Service level found for the new queue and status | RUNNING |
| RUNNING | CaseTransferred or CaseStateChanged | New queue or status | STOPPED |
| RUNNING | The stage-clock pause is posted through the P3 case action contract | Timer type SERVICE_LEVEL | PAUSED |
| PAUSED | The resume is posted through the same contract | None | RUNNING, expires_at and warn_at recomputed |
| RUNNING | The durable timer fires | expires_at passed and the decision record is written | EXPIRED, TimerBreached on rwb.case.events.v1 |
| RUNNING | The durable timer fires | expires_at passed and the decision record cannot be written | RUNNING, escalation level 0, MSG-P7-003, retaken by the first run after recovery |

The states the run observes across the services:

| Item | States |
|---|---|
| Durable timer in CaseWorkflow | Set, waiting on the warning point, waiting on the expiry, paused, fired, cancelled by a later `CaseTransferred` or `CaseStateChanged` |
| Timer projection (rwb_case) | RUNNING, PAUSED, STOPPED, EXPIRED, absent when no service level is in force |
| Escalation level | 0 (not raised, or held because the decision record failed), 1 (breach raised) |
| Case | Queue `LIT-BKK-OFF` and owner U-31 unchanged through the warning and the breach; the case status itself is out of scope |
| Suite run | Not started, running, passed, failed with the failing test case named |

The `DeviationRaised` and `DeviationCleared` transitions of the legacy table belong to the deviation service of wave 2 and are proved in RWB-ITG-W2; at wave 1 the same pause and resume are driven through the P3 case action contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Runs the suite, seeds the synthetic fixtures, moves the workflow clock, stops and restarts the rwb-case worker, reads the evidence report |
| SY-CASEWF Case and workflow system | Starts, pauses, resumes, stops and expires the durable timers inside `CaseWorkflow`; writes the timer projection; sets the prescription date |
| SY-DECLOG Decision log writer | Writes the decision record of each timer start, warning and breach |
| RW-CASEOWN Case owner | Reads the timers on their cases within scope and receives MSG-P3-003 |
| RW-TEAMMGR Team manager | Receives the breach as the escalation point and reads the timers in team scope |
| RW-LEGAL Legal | Owns the LEGAL_PERIOD rows, loaded as reference data through the P3 reference-data contract |
| Business lead | Owns the service level values (DL22) |
| Every role with Case record R | Reads the timers within scope |
| No role | Reads a service schema directly, writes a timer row, or publishes `TimerDue` |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3 rwb-case) | id | Read |
| DF-CAS-003 | recovery_case (P3 rwb-case) | product_group | Read |
| DF-CAS-005 | recovery_case (P3 rwb-case) | status | Read |
| DF-CAS-009 | recovery_case (P3 rwb-case) | owner_user_id | Read |
| DF-CAS-010 | recovery_case (P3 rwb-case) | queue_id | Read |
| DF-CAS-017 | recovery_case (P3 rwb-case) | prescription_date | Write by P3 rwb-case; read back through the contract |
| DF-CAS-019 | recovery_case (P3 rwb-case) | deviation_open | Read |
| DF-CAS-026 | case_account (P3 rwb-case) | account_key | Read |
| DF-ACE-007 | v_ace_account (P1 rwb-source-data) | contract_date | Read through the P1 contract; exercised by RWB-P3-E1028-APP, not called by this suite |
| DF-ACE-026 | v_ace_account (P1 rwb-source-data) | last_payment_date | Read through the P1 contract; exercised by RWB-P3-E1028-APP, not called by this suite |
| DF-WRK-002 | queue (P3 rwb-case) | queue_code | Read |
| DF-WRK-004 | queue (P3 rwb-case) | team_code | Read |
| DF-WRK-027 to DF-WRK-036 | timer (P3 rwb-case) | all fields | Write by the `CaseWorkflow` timer projection only; read back through the timer contract |
| DF-WRK-041 | timer (P3 rwb-case) | warned_at | Write by the `CaseWorkflow` timer projection only; read back through the timer contract |
| DF-REF-184 | reference_row (P3 rwb-case) | row_data | Read through the P3 reference-data contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7 rwb-decision) | all fields | Write by P7 rwb-decision; read through the ledger query |
| Cross-service account-date and holiday input, and the Temporal timer visibility surface | v_ace_account and the holiday calendar behind P3, and the workflow history of `CaseWorkflow` | last_payment_date, contract_date, non-working days, timer visibility | Not specified in the source documents (GAP-0353; ASM-0447) |

The field IDs are copied unchanged from RWB-E1-028 and are those of the Logical Data Model and Data Dictionary. The legacy story writes the `timer` rows directly from the Quartz check; in the target the durable timer inside `CaseWorkflow` is the clock and the `timer` row is its P3 projection (ASM-0078), so the row is written by the workflow only and read by the suite through the contract. `recovery_case` and `timer` stay in `rwb_case`, `reference_row` stays in `rwb_case` under the R-PREC default ruling, and the decision log stays in `rwb_decision`. The suite reads every row of this table through a contract of section 12.2, an event of section 12.4 or the workflow history, and writes no schema of its own. The account dates and the holiday calendar are behind P1 and P3 and are exercised by RWB-P3-E1028-APP; the exact surface on which a past fire and the timer state inside the workflow are read is the one open point of this story.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration` and `rwb_integration` — are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method and path | Owner | Use |
|---|---|---|
| GET /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | Read the queue, the owner, the prescription date and the deviation flag before and after each point |
| GET /api/recovery/case/v1/cases/{caseId}/timers | P3 rwb-case | Read the timer projection: type, status, expires_at, warn_at, paused and escalation level |
| POST /api/recovery/case/v1/cases/{caseId}/actions | P3 rwb-case | The wave 1 pause and resume of the stage clock, and the queue move that restarts a timer |
| GET /api/recovery/decision/v1/decision-log | P7 rwb-decision | Read the decision record of the timer start, the warning and the breach, the breach with rule R-UNI-30 |

Every call is one hop to the owning service on its own base with a 2 s budget (ADR-020, DP-11, DP-13). The refusal of AC11 is returned by rwb-case on its own read, with the right and the scope resolved by rwb-access through the P4 authorise contract inside that hop; the suite calls no service through another service.

#### 12.3 Events published

None. The suite publishes no business event; it observes the events of the owning services, listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| rwb.case.CaseCreated.v1 | rwb.case.events.v1 | P3 rwb-case | The creation that starts the PRESCRIPTION timer and sets the prescription date |
| rwb.case.CaseAllocated.v1 | rwb.case.events.v1 | P3 rwb-case | The allocation that starts the SERVICE_LEVEL timer |
| rwb.case.CaseTransferred.v1 | rwb.case.events.v1 | P3 rwb-case | The move that stops the running timer and starts the next one |
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | P3 rwb-case | The status change that restarts the timer |
| rwb.deviation.DeviationRaised.v1 | rwb.deviation.events.v1 | S8 rwb-deviation | Wave 2 only: named here, not consumed at wave 1 (see the gap) |
| rwb.deviation.DeviationCleared.v1 | rwb.deviation.events.v1 | S8 rwb-deviation | Wave 2 only: named here, not consumed at wave 1 (see the gap) |

The four case events are consumed in the CloudEvents 1.0 envelope keyed caseId, with the inbox dedupe of the consumer and the retry and `.dlt` topics of the owner (ADR-015; DP-09; Arch v5 slide 42). The two deviation events belong to the deviation service of wave 2 and their path is proved in RWB-ITG-W2; at wave 1 the pause and resume of AC10 are driven through the P3 case action contract, and the suite sends neither deviation event.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent per case | rwb-case | Holds the durable SERVICE_LEVEL and PRESCRIPTION timers from entry to closure; the suite reads its history and observes its fires |
| EvaluateRules | Activity | rwb-case | Resolves the service-level escalation and the timer decision from the package in force, with the rule ID and version (DP-04) |
| RecordAndApply | Activity | rwb-case | Writes the decision record, the timer projection and the outbox row in one transaction, and fails as one unit |
| TimerCheckJob | Retired | — | Not deployed: JOB-05 and its Quartz implementation are retired (Architecture v5 slides 42 and 44; ASM-0078) |

The three live entries are registered by RWB-P3-E1028-APP. This story adds no workflow and no activity: it moves the workflow clock, stops and restarts the worker, and reads the result through the contracts of 12.2 and the events of 12.4. The exact surface on which the timer state and a past fire are read from the workflow history is Not specified in the source documents (GAP-0353; ASM-0447).

#### 12.6 Schedules

| Job | Name | When | Owner | Use |
|---|---|---|---|---|
| JOB-06 | Rebalancing | 06:30 daily | P3 rwb-case, Temporal Schedule | Observed only: it moves cases and therefore restarts timers; the suite asserts the timer after a move |
| JOB-20 | Rule promote | 00:01 daily | P7 rwb-decision, Temporal Schedule | Observed only: the rule version in force on the decision record of the breach |
| JOB-05 | Timer check | Every 5 minutes on Quartz | Retired | Not run and not asserted as a job: the clock is the durable timer inside `CaseWorkflow` (Architecture v5 slides 42 and 44; ASM-0078) |

The suite starts no Schedule. It moves its own workflow clock through the Temporal test-time control so the warning point, the expiry and 2028-03-15 are reached without waiting, and it restores the clock after each scenario.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The tables it exercises belong to `rwb_case` and `rwb_decision` and are listed in section 11 with their owners.

#### 12.8 Contract fakes

External stubs only:

| Stub | Use |
|---|---|
| Synthetic case and account set RWB-ITG-W1J01-ITG | The cases, owners, accounts and service-level and legal-period rows of the run; stands in for the ACE ingestion that the bank owns outside the nineteen services |
| Temporal test-time control (time skipping) | Moves the workflow clock to the warning point, the expiry and 2028-03-15, and restores it |
| Mock Entra sign-in | Gives the run its synthetic test identities, including the user without Case record R |

No service contract is faked: every P3, P4 and P7 call in 12.2 goes to the real service in SIT, and a run that needs a fake for one of them fails the preflight.

#### 12.9 Call-type summary

| Call type | Provided by the suite | Consumed by the suite |
|---|---|---|
| REST | 0 | 4 |
| Kafka | 0 | 4 case events at wave 1; 2 deviation events named only |
| Temporal | 0 | 1 workflow (CaseWorkflow) and 2 activities (EvaluateRules, RecordAndApply) observed; 2 Schedules (JOB-06, JOB-20) observed |
| File | 0 | 0 |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture pack for the cases, owners and reference rows, a time control for the workflow clock, a worker control for the catch-up scenario, four contract probes, an event probe and an evidence report with one verdict per test case. No service code and no schema change.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts, run order, report and exit code |
| Fixture pack | Test data | Synthetic cases, owners, service-level rows, legal-period rows and non-working days of the W1J01 set |
| Clock control | Harness control | Moves the workflow clock through the warning point, the expiry and 2028-03-15 with the Temporal test-time control, and restores it |
| Worker control | Harness control | Stops the rwb-case worker for 40 minutes of workflow time, restarts it and waits for the history replay |
| TimerProbe | Test harness | Reads the case and the timer projection and asserts type, status, expires_at, warn_at, paused and escalation level |
| CaseEventProbe | Test harness | Consumes the four case events and asserts the envelope, the key and that no TimerDue event exists on any topic |
| DecisionProbe | Test harness | Reads the P7 ledger and asserts one record per point, the rule ID and version, and R-UNI-30 on the breach |
| FaultStep | Test harness | Fails the decision record write at one expiry and restores the ledger, and calls the timer read with the user without Case record R |
| ReportWriter | Test harness | One row per scenario with the case, the timer state, the events, the messages and the elapsed time |

**Database.** None of its own. The suite writes no service table and no schema object, and it reads the `timer` projection only through the P3 contract (ASM-0078).

**Configuration and reference data**

- The SIT endpoints of P3, P4 and P7, the topic names, the task queues, the namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic case numbers, owners and account keys of the W1J01 set, and the business dates 2026-12-01, 2026-12-02 and 2026-12-04.
- The SERVICE_LEVEL row (5 working days, warning percent 80, escalation role RW-TEAMMGR) through the P3 parameter contract (DP-06), and the LEGAL_PERIOD row, the legal-period warning parameter and LOV-TIMER-STATUS through the P3 reference-data contract (DP-07).
- The non-working days 2026-12-05 to 2026-12-07, loaded as reference data and never as code.
- The 2 s client budget, the poll windows and the time-skip step.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | `recovery_case`, `timer` and `reference_row` stay in `rwb_case`, the ledger in `rwb_decision`; the suite asserts through contracts only |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | On RWB-P3-E1028-APP, which writes the local record and publishes it; not a build dependency of this suite, which only reads the ledger |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | The last payment date, the contract date and the holiday calendar stay behind P1 and P3 and are exercised by RWB-P3-E1028-APP; this suite calls neither |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | On the APP story for the service levels and the timer parameters; the suite reads the values as data rows |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | On the APP story for the legal periods, the list values and the holiday calendar; the suite reads the codes as data |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | On RWB-P3-E1028-APP for the case events and `TimerBreached`; the suite consumes the topics only |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON | On RWB-P3-E1028-APP: the timer is a durable Temporal timer in `CaseWorkflow`, so JOB-05 and Quartz are gone and only JOB-06 and JOB-20 are observed |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The four consumed REST operations of section 12.2 |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every consumed path in section 12.2 |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON | On RWB-P3-E1028-APP for `rwb.case.events.v1`; the suite asserts the topic name and publishes nothing |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | On RWB-P3-E1028-APP, RWB-P4-E1028-APP and RWB-P7-E1028-APP for their own sequences; the suite owns no schema |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The two screens of section 15 are read through gateway-bff; the suite enters through the same route where a screen is asserted |

The dependency-added column records what the owning APP stories had to build. **An ITG story carries no H, C or X dependency**: its `Depends on (build)` row is None, its `Contract dependencies` row is None and its `External dependencies` row is None, and **its I dependencies are the three APP stories** — RWB-P3-E1028-APP, RWB-P4-E1028-APP and RWB-P7-E1028-APP (Template and Rules §R5.4 and §R5.7). An integration story builds against published contracts and blocks no build of its own.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Case set of the clocks | RW-2026-000401 in `LIT-BKK-OFF` at 2026-12-01 09:00 with owner U-31 and team `LIT-BKK`; RW-2026-000402 with last payment 2026-03-15; RW-2026-000403 in `NPA-BKK-CO`; RW-2026-000404 as SSME; RW-2026-000405 with contract date 2025-06-30 and no payment; RW-2026-000406, 000407, 000408 and 000409 | AC1 to AC12 |
| Service-level rows | `HIRE_PURCHASE` / `ASSIGNED` 5 working days, warning percent 80, escalation role RW-TEAMMGR; and a run with no version in force for 2026-12-01 | AC1, AC2, AC4 |
| Legal-period rows | `HIRE_PURCHASE` 2 years from the last payment date with the warning parameter; no row for `SSME` | AC3, AC5, AC6 |
| Calendar rows | 2026-12-05 to 2026-12-07 as non-working days | AC1, AC10 |
| Fault state | The decision record write failing at one expiry, and the test user without Case record R | AC9, AC11 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG, wire it to the SIT endpoints of P3, P4 and P7, and write the preflight: the three services answer, the topics and their retry and `.dlt` topics exist, the task queues are registered in `rwb-recovery`, and the JOB-05 timer check is absent from the deployment.
2. Build the fixture pack and the two reference contracts' readers: the service-level row, the legal-period rows, the warning parameter and the non-working days, all as data rows.
3. Build the clock control and the worker control, with the restore step and the proof that the workflow resumes from history after a restart.
4. Implement AC1 and AC2: `CaseAllocated` starts the durable timer, the projection shows RUNNING with the two dates, the warning reaches U-31 once, the breach reaches RW-TEAMMGR of `LIT-BKK` with escalation level 1, the case keeps its queue and owner, and both points have a decision record with R-UNI-30 on the breach.
5. Implement AC3 and AC4 to AC6: the prescription date 2028-03-15 and its timer at 2027-09-17, no service level, no legal period and the contract-date fallback 2027-06-30.
6. Implement AC7 to AC9: the 40-minute worker outage with three timer fires, the single breach, and the decision-record failure that holds the escalation at level 0 with MSG-P7-003 and the recovery run.
7. Implement AC10: the pause through the P3 case action contract on 2026-12-02, the resume on 2026-12-04, the 2 working days moved on the stage clock, the unchanged prescription `expires_at`, and MSG-P3-004 on the case record.
8. Implement AC11 and AC12: the 403 with MSG-P4-002 from the owning service, and the proof over the call set and the topics that no `TimerDue` is produced and no Quartz timer check runs.
9. Write the evidence report, remove the fixtures, restore the clock and the worker, and run the suite in SIT against the wave 1 release candidate.

**Done when.** The fourteen test cases of section 16 are dispositioned — the twelve owned scenarios pass on the real services in SIT, the two regression copies are green, and the contract-level copy of the boundary test passes — the timer the projection shows is the timer the workflow holds, exactly one `TimerBreached` and one decision record exist per breach with R-UNI-30, no `TimerDue` event was published in the run, no service table was read, the synthetic set is cleaned up, and the evidence report names every scenario with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | Warning point reached | {timer} ends on {date}. |
| MSG-P3-004 | Case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-026 | No service level or legal period found | No {item} is set for {scope}. The timer did not start. |
| MSG-P7-003 | Decision log write failed at a breach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The five IDs and their wording are copied unchanged from RWB-E1-028. No new message ID is added by this story. MSG-P3-004 keeps its legacy wording; at wave 1 the hold is set through the P3 case action contract and the deviation wording is the text of the legacy message (GAP-0353; ASM-0447). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-03 Case record (read only; on hold) shows the prescription date and the due date of the running service level, and the suite asserts the same two facts through `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers`. SCR-09 Exception queue (Loading; list) lists the cases with MSG-P3-026 for a missing service level or a missing legal period, which the suite asserts on the message and the case list. Both screens are read through the gateway-bff composite route (DP-19), and the suite enters by the same route where a screen is asserted. The timer panel with the stage clock and the escalation state on the case view comes in Epic 2 (RWB-E2-015) and is out of scope here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-028-12-ITG | AC11 | Integration | Test user U-7101 holds RW-REFADM and calls GET /api/recovery/case/v1/cases/{caseId}/timers, refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-01-ITG | AC1, BR1, BR8 | Integration | Case placed in LIT-BKK-OFF at 2026-12-01 09:00, expires 2026-12-09 09:00 and warns 2026-12-08 09:00 with 2026-12-05 to 2026-12-07 non-working; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-02-ITG | AC2, BR2, BR3 | Integration | Timer passing warn_at and expires_at, owner U-31, team LIT-BKK, rule R-UNI-30; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-03-ITG | AC3, BR4 | Integration | HP account, last payment 2026-03-15, prescription 2028-03-15, warning 2027-09-17; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-04-ITG | AC4, BR1 | Integration | Queue NPA-BKK-CO with no service level on 2026-12-01; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-05-ITG | AC5, BR4 | Integration | SSME with no legal period; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-06-ITG | AC6, BR4 | Integration | No last payment, contract date 2025-06-30, prescription 2027-06-30; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-07-ITG | AC7 | Integration | rwb-case worker stopped from 10:00 to 10:40 with three timers passing expires_at; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-08-ITG | AC8 | Integration | Timer already EXPIRED with escalation level 1; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-09-ITG | AC9, BR9 | Integration | Decision record write failing at one expiry, case RW-2026-000407; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-10-ITG | AC10, BR5, BR6 | Integration | Pause from 2026-12-02 to 2026-12-04 on case RW-2026-000408; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-11-ITG | AC2, BR2 | Integration | 5 working days from Monday 2026-12-14, warning checked on Friday 2026-12-18; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-13-ITG | AC9, BR9 | NFR | Decision record write forced to fail for every breach in a run; end-to-end: real services on the wave 1 contracts |
| TC-E1-028-14-ITG | AC12, BR10 | Contract | A class outside the P3 timer boundary writes the timer row directly; the boundary test of RWB-P3-E1028-APP fails and no row changes at run time; end-to-end: real services on the wave 1 contracts |

The fourteen test case IDs of RWB-E1-028 are kept as ITG copies with the suffix `-ITG`, in their legacy order, and each one is mapped to the scenario it covers in section 7. TC-E1-028-11-ITG, TC-E1-028-13-ITG and TC-E1-028-14-ITG additionally carry the component evidence of RWB-P3-E1028-APP AC11, AC13 and AC12, which that story owns: the warning point of a 5-day level and the level 1 escalation on the real services, the record failure forced for every breach of a run, and the timer boundary of the projection. They are run here on the real services so that a change in one service cannot pass unnoticed. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the legacy Resilience level becomes NFR and the legacy Build level becomes Contract. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the service levels, the warning point, the escalation role, the legal periods, the warning parameter and the holiday calendar are data rows read through the P3 parameter and reference-data contracts (DL22, DP-06, DP-07).
- No personal data in the events, the workflow history, the logs, the evidence report or the fixtures; the case is named by its case number and the owner by user ID only.
- No cross-service table read and no schema change: every assertion is a contract response, an event or the workflow history, and the `timer` projection is read behind the P3 contract only (DP-01, ASM-0078).
- No `TimerDue` and no Quartz: the run asserts the absence of the retired event and of the retired job, and the only clock is the durable timer inside `CaseWorkflow`.
- A breach never moves the case and the prescription timer never pauses.
- One hop and a 2 s budget on every call (ADR-020, DP-11), and a timeout is never retried into a pass.
- The clock the suite moves is the Temporal test-time control of its own run; the service's durable timers are never shortened in a shared environment, and the clock is restored after every scenario.
- Synthetic data only, loaded by the harness RWB-ITG-W1J01-ITG; the suite ships with no client for a service schema, refuses an environment that is not SIT, and opens no production connection of any kind.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | The durable timer in `CaseWorkflow`, `GET /api/recovery/case/v1/cases/{caseId}/timers`, `POST /api/recovery/case/v1/cases/{caseId}/actions`, `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1`, `TimerBreached` on `rwb.case.events.v1`, MSG-P3-003, MSG-P3-026, MSG-P4-002 | TC-E1-028-01-ITG, TC-E1-028-02-ITG, TC-E1-028-04-ITG, TC-E1-028-07-ITG, TC-E1-028-08-ITG, TC-E1-028-10-ITG, TC-E1-028-11-ITG, TC-E1-028-12-ITG, TC-E1-028-14-ITG |
| REQ-CWC-012 | Prescription date from the legal periods at creation | `rwb.case.CaseCreated.v1`, `GET /api/recovery/case/v1/cases/{caseId}` prescription date, the PRESCRIPTION timer in the P3 projection, MSG-P3-026, MSG-P3-004 | TC-E1-028-03-ITG, TC-E1-028-05-ITG, TC-E1-028-06-ITG, TC-E1-028-10-ITG |
| REQ-CWC-016 | Every timer event logged with rule and version | The local decision record on `rwb.decision-record.v1` and `GET /api/recovery/decision/v1/decision-log`, the breach with R-UNI-30, MSG-P7-003 | TC-E1-028-02-ITG, TC-E1-028-09-ITG, TC-E1-028-13-ITG |
| DP-05 | Marker `AceSourceQuery`, `v_ace_*`, `account_ext`; read through rwb-source-data's contract or the service's own ACE views | The last payment date, the contract date and the holiday calendar behind P1 and P3, exercised by RWB-P3-E1028-APP and not called by this suite | TC-E1-028-03-ITG, TC-E1-028-06-ITG |
| DP-06 | Parameters contract of rwb-case | The SERVICE_LEVEL row and the timer parameters read as data | TC-E1-028-01-ITG, TC-E1-028-04-ITG |
| DP-07 | Reference-data contract of rwb-case | The LEGAL_PERIOD rows, the warning parameter, LOV-TIMER-STATUS and the non-working days read as reference data | TC-E1-028-03-ITG, TC-E1-028-05-ITG, TC-E1-028-10-ITG |
| DP-09 | Outbox and inbox, Kafka topic of the owner, CloudEvents | The four case events and `TimerBreached` on the owner's topic with the inbox dedupe | TC-E1-028-02-ITG, TC-E1-028-07-ITG, TC-E1-028-08-ITG |
| DP-10 | Marker `Quartz`, `JOB-nn`; Temporal Schedule or event-started workflow through the workflow kit | The durable timer in `CaseWorkflow`, the retirement of JOB-05, and the observed JOB-06 and JOB-20 | TC-E1-028-07-ITG, TC-E1-028-14-ITG |
| DP-14 | Naming library; `rwb.<short>.events.v1` | `rwb.case.events.v1` and `rwb.decision.events.v1` on every consumed event | TC-E1-028-01-ITG, TC-E1-028-02-ITG |
| ADR-011 | Reusable Temporal layer and the case workflow | `CaseWorkflow` on task queue `rwb-case` in namespace `rwb-recovery` | TC-E1-028-01-ITG, TC-E1-028-07-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The CloudEvents envelope, the caseId key and the consumer inbox dedupe | TC-E1-028-02-ITG, TC-E1-028-08-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed REST operations of section 12.2 and the preflight contract test | TC-E1-028-01-ITG, TC-E1-028-11-ITG, TC-E1-028-12-ITG |
| ASM-0078 | `timer` stays with P3 as the screen projection while the clock is a durable Temporal timer in `CaseWorkflow`; TimerDue and JOB-05 retired | The timer projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, `TimerBreached` on `rwb.case.events.v1`, and the absence of `TimerDue` and Quartz | TC-E1-028-07-ITG, TC-E1-028-14-ITG |
| RWB-E1-028 (legacy story) | Service levels, timers, escalation and prescription dates: the values, the messages and the rules | The four REST operations, the four case events, `CaseWorkflow` and the two activities of section 12 | All fourteen copies of section 16 |

The twelve legacy acceptance criteria AC1 to AC12 stay with **RWB-P3-E1028-APP**, which owns the durable timer, the projection, the warning, the breach, the catch-up, the prescription calculator and the pause at component level; the access side stays with **RWB-P4-E1028-APP**, which owns the Case record R right and its refusal. This story owns the twelve new scenarios of section 7 and no legacy criterion.

### 19. Out of scope

- The three application builds this run depends on: RWB-P3-E1028-APP, RWB-P4-E1028-APP and RWB-P7-E1028-APP, and their unit, component and contract tests.
- The CON, DB, OPS and INF stories of the legacy key and of P3, P4 and P7.
- The P1 account-date and holiday path at component level, which RWB-P3-E1028-APP exercises through DP-05 and which this suite does not call.
- The deviation service of wave 2: `DeviationRaised` and `DeviationCleared` are named in section 12.4 and proved in RWB-ITG-W2, not here.
- The prescription warning forcing a litigation review (R-UNI-31, CTL-18, Epic 2).
- The timer panel and the escalation state on the case view (RWB-E2-015), and SCR-07 team queues.
- The notice period, cure period, offer validity and other stage-specific timers, which belong to their route stories in Epics 3 to 6.
- JOB-05, Quartz, its five-minute schedule and the `TimerDue` event, all retired from the target (Architecture v5 slides 42 and 44; ASM-0078).
- The build of the harness RWB-ITG-W1J01-ITG, which is a precondition here and not a deliverable, and the non-functional epic RWB-ITG-NFR.

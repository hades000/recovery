# RWB-P3-E1028-APP Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1045-APP, RWB-P3-E1020-APP |
| Depends on (build) | RWB-P3-E1028-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1045-APP, RWB-P3-E1020-APP |
| Contract dependencies | RWB-P7-E1027-CON (contract version v1, the /v1 path of each endpoint) |
| Integration dependencies | None |
| External dependencies | RWB-P3-E1028-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-012, FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025, FR-P3-030) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-028 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 20 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a service level per queue and status held as data, a durable timer on every case that warns the owner and raises a breach to the named escalation point, and a prescription date set at creation from the legal periods, all served by rwb-case from its own schema and its own workflow**, so that **no case waits past its limit unseen and no legal claim expires unnoticed**.

The clause "by rule" is delivered without Drools in this story: the escalation role, the warning percentage and the service level come from the parameter row in force (DP-06) and the legal periods and list values from the reference row in force (DP-07), so the decision is a read of versioned data, not a rule package evaluation.

### 2. Business rationale

Deadlines are tracked in personal diaries today, and audit found litigation not filed for debtors meeting the criteria (CTL-18). This story starts a service level timer each time a case enters a queue and status, warns the owner at the warning point, raises a breach to the escalation role without moving the case, and sets the prescription date at case creation from the legal period of the product. It meets REQ-CWC-011, REQ-CWC-012 and REQ-CWC-016 and serves the measure "cases inside the service level" (target set with DL22).

In the monolith the clock was a five-minute Quartz job (`JOB-05`) behind a published `TimerScheduler` port, and its only failure signal was a job exception. In the target the clock is a **durable Temporal timer inside `CaseWorkflow`** on task queue `rwb-case` (DP-10), so a fire set in 2028 survives a restart, a release and a Continue-As-New, and a fire that fell inside a worker outage is satisfied once on recovery from history. The `timer` row stays as the P3 projection behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, so no reader changes (ASM-0078).

Two elements of the legacy design are retired with the job. **`JOB-05` and its five-minute schedule go**, and the **`TimerDue` event (EV-18) goes with it**: the event catalogue marks #18 as retired as "timer inside the workflow" and the job map shows `JOB-05` as durable timers retired (Architecture v5 slides 42 and 44). **`TimerBreached` stays**, as event #19 of `rwb.case.events.v1`, published by rwb-case with gateway-bff as the inbox consumer. Each timer start, warning and breach writes one local decision record through the shared library and `rwb.decision-record.v1` (DP-03), which the central ledger in rwb-decision seals, so the deadline is defensible two years later.

The service is also the owner of the parameter and reference data the whole workbench reads (DP-06, DP-07), so the levels, the warning percentage, the escalation roles, the legal periods and the calendar are rows with a version in force, never code.

### 3. Preconditions

- RWB-P3-E1028-CON is published: the OpenAPI document of `GET /cases/{caseId}/timers` and `GET /cases/{caseId}` with the Timer and Case resources, the error envelope and the fakes.
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, so `CaseWorkflow` polls `rwb-case` and holds the durable timers (DP-10).
- RWB-PLT-E1027-CON and RWB-P7-E1027-CON are published: the local decision-record library, the shared topic `rwb.decision-record.v1` and the ledger contract the record is written against (DP-03).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract of rwb-case and its client library, so `SERVICE_LEVEL` and `legal.prescription.warn.days` are read as versioned rows (DP-06).
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case and its client library, so `LEGAL_PERIOD`, `LOV-TIMER` and `LOV-TIMER-STATUS` are read as versioned rows (DP-07). `LOV-TIMER` (9 values) and `LOV-TIMER-STATUS` (4 values) are closed lists (Reference Data v5 Lists rows 19 and 20): their values stay the fixed set of the schema of rwb-case, a new value is a list change and not a data row (R-00724, R-00725).
- RWB-PLT-TE006-CON is published: the outbox and inbox library, CloudEvents 1.0, and the retry and `.dlt` topics of `rwb.case.events.v1` (DP-09). RWB-PLT-E1047-CON fixed the topic and event names (DP-14) and RWB-PLT-E1044-CON the per-service Flyway sequence in `rwb_case` (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-03 and SCR-09 (DP-19); this story fixes only the answers rwb-case returns.
- RWB-P3-E1045-APP is done: the `SERVICE_LEVEL` row for a product group and a case status is served with its limit, unit, warning percent and escalation role.
- RWB-P3-E1020-APP is done: `rwb.case.CaseAllocated.v1` is published when a case gets a queue and an owner, and `rwb.case.CaseStateChanged.v1` on every status change.
- The reference rows are loaded with a version in force: `SERVICE_LEVEL` product group `HIRE_PURCHASE`, status `ASSIGNED`, 5 working days, warning percent 80, escalation role `RW-TEAMMGR`; `LEGAL_PERIOD` `HIRE_PURCHASE` 2 years from the last payment date; the parameter `legal.prescription.warn.days` = 180 (assumed, owner Legal); non-working days 2026-12-05 to 2026-12-07 (synthetic test values). The values themselves are the business lead's (DL22) and Legal's.
- The account dates and the holiday calendar are reachable only through the rwb-source-data contract (DP-05): the exact paths for the account dates and for the non-working days are Not specified in the source documents (GAP-2202; ASM-3616).
- The deviation pause arrives as `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` from S8, which is wave 2; at wave 1 the same pause is reachable through the P3 case action contract, and AC10 is proved against the rwb-deviation contract mock (GAP-2202; ASM-3617).
- The login is the rwb-case login (DP-02): one login and one connection pool, grants on schema `rwb_case` only. The case is in the caller's scope and the caller holds Case record R; rwb-access answers through its authorise contract, cached per request.

### 4. Flow

1. `CaseEventRouter` consumes `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1` and `rwb.case.CaseStateChanged.v1` from `rwb.case.events.v1`, dedupes through the inbox of `rwb_case`, and signals `CaseWorkflow` with the case ID (DP-09).
2. `CaseWorkflow` cancels the running `SERVICE_LEVEL` durable timer of the case, reads the `SERVICE_LEVEL` row for the new queue and status through the parameters contract (DP-06), computes `expires_at` in working days and `warn_at` at the warning percentage, and sets a durable timer for each point.
3. `RecordAndApply` writes the `timer` projection row, the local decision record with its rule ID and version, and the outbox row in one transaction; the record is published on `rwb.decision-record.v1` and sealed by rwb-decision.
4. On `rwb.case.CaseCreated.v1`, `PrescriptionCalculator` reads the last payment date and the contract date of each linked account through the rwb-source-data contract (DP-05), reads the `LEGAL_PERIOD` row in force (DP-07) and sets the earliest result as `recovery_case.prescription_date`.
5. `PrescriptionCalculator` sets a `PRESCRIPTION` durable timer with `expires_at` on the prescription date and `warn_at` 180 days before, from the parameter row; a `PRESCRIPTION` timer never pauses.
6. The durable timer fires at `warn_at`: `CaseWorkflow` writes the decision record, sets `timer.warned_at`, and sends MSG-P3-003 to the case owner once.
7. The durable timer fires at `expires_at` of a `SERVICE_LEVEL` timer: `CaseWorkflow` writes the decision record with rule `R-UNI-30`, sets the timer `EXPIRED` with escalation level 1 and `escalated_to_role`, publishes `rwb.case.TimerBreached.v1` on `rwb.case.events.v1`, and leaves the case in its queue and with its owner.
8. The durable timer fires at `expires_at` of any other timer type: the timer is set `EXPIRED` and the decision record is written; no `TimerDue` event is published, because that event is retired.
9. `DeviationSignalRouter` consumes `rwb.deviation.DeviationRaised.v1` and signals a pause: the `SERVICE_LEVEL` durable timer is paused and its `expires_at` and `warn_at` move by the paused working days when the resume arrives on `rwb.deviation.DeviationCleared.v1` (R-UNI-43). The `PRESCRIPTION` timer is untouched.
10. A worker outage is not a lost fire: on restart the workflow resumes from history, satisfies the timer at `expires_at`, and raises each missed breach once.
11. `TimersController` serves `GET /api/recovery/case/v1/cases/{caseId}/timers` and `GET /api/recovery/case/v1/cases/{caseId}` from the projection and the case row; it authorises through the rwb-access contract and applies the scope.
12. Case owner: reads the timers and the prescription date on SCR-03; the exception cases of a missing service level or legal period are listed on SCR-09.
13. No caller writes or updates the `timer` row: every schedule, cancel, pause and resume goes through the timer boundary inside `CaseWorkflow` (BR10), and the read path writes nothing.
14. `JOB-06` Rebalancing and the other Schedules of the service stay where they are; this story registers no Schedule and no Quartz trigger.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No `SERVICE_LEVEL` version is in force on the date | No timer; the case is listed on the exception queue | MSG-P3-026 | AC4 |
| X2 | No legal period for the product | Prescription date not set and no `PRESCRIPTION` timer; the case is listed on the exception queue | MSG-P3-026 | AC5 |
| X3 | An account has no last payment date, or the rwb-source-data answer omits it | The contract date is used | None | AC6 |
| X4 | The rwb-case worker is down for 40 minutes with three timers passing `expires_at` | The workflows resume from history and raise every missed breach once | None | AC7 |
| X5 | The timer is checked again after a breach | No second `TimerBreached` is published and the escalation level is unchanged | None | AC8 |
| X6 | The decision record cannot be written at a breach | The timer stays `RUNNING` with escalation level 0 and the breach is raised by the first run after the ledger is back | MSG-P7-003 | AC9 |
| X7 | A deviation is raised on the case | The `SERVICE_LEVEL` timer is paused; the `PRESCRIPTION` timer keeps running | MSG-P3-004 | AC10 |
| X8 | The warning point is 4 of 5 working days | One warning, at the first fire after 4 working days have passed | MSG-P3-003 | AC11 |
| X9 | A role without Case record R reads the timers | Refused with 403 by rwb-case on the rwb-access answer | MSG-P4-002 | AC13 |
| X10 | A class outside the timer boundary writes or updates the `timer` row | The build fails on the boundary test; no row is changed at run time | None | AC12 |
| X11 | The rwb-source-data contract does not answer inside 2 s | One retry with jitter, then the breaker; the prescription date is left empty and the case is listed for retry, never set from a stale date | None | AC3, AC6, AC16 |
| X12 | The case ID is unknown or outside the caller's scope | 404 from the read; no partial timer list | MSG-P4-003 | AC14 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the parameters and reference-data contracts of its own service and the rwb-source-data, rwb-decision and rwb-access contracts and their fakes; the deviation service is not needed until wave 2 |
| Negotiable | The levels, the warning percentage, the escalation roles, the legal periods, the warning days and the holidays are data; the story fixes the behaviour |
| Valuable | Every case and every legal claim carries a visible, durable deadline that survives a release |
| Estimable | One timer boundary, one workflow, three activities, one prescription calculator, one working-day calculator, two read operations |
| Small | Fits one sprint with its tests |
| Testable | Every owned criterion has a test case in section 16; the P1, P7 and S8 answers are stubbed in the contract fakes and real in SIT |

### 7. Acceptance criteria

```gherkin
Feature: Service levels, timers, escalation and prescription dates

  Background:
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" and "ASSIGNED" is 5 working days with warning percent 80 and escalation role RW-TEAMMGR
    Given the LEGAL_PERIOD row for "HIRE_PURCHASE" is 2 years from the last payment date
    Given 2026-12-05 to 2026-12-07 are not working days in v_ace_holiday

  Scenario: AC1 Timer starts (legacy RWB-E1-028 AC1)
    Given hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00
    When the case arrives
    Then a SERVICE_LEVEL timer is RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00
    Then GET /cases/{caseId}/timers returns the timer with its due date

  Scenario: AC2 Warning and escalation (legacy RWB-E1-028 AC2)
    Given the rwb-decision contract mock returns the sealed decision record of the warning and of the breach with rule R-UNI-30
    Given the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at
    When the timer check runs after each point
    Then owner U-31 receives MSG-P3-003 at the warning point
    Then the system raises at expiry the breach to RW-TEAMMGR of team "LIT-BKK" with TimerBreached and escalation level 1
    Then the case keeps queue "LIT-BKK-OFF" and owner U-31
    Then both the warning and the breach have a decision record entry, the breach with rule R-UNI-30

  Scenario: AC3 Prescription date (legacy RWB-E1-028 AC3)
    Given the rwb-source-data contract mock returns last payment date 2026-03-15 for the account of case RW-2026-000402
    Given a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15
    When the case is created
    Then the prescription date is 2028-03-15
    Then a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17
    Then GET /cases/{caseId} shows prescription date 2028-03-15

  Scenario: AC4 No service level for the queue and status (legacy RWB-E1-028 AC4)
    Given no SERVICE_LEVEL version is in force on 2026-12-01
    When case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01
    Then no SERVICE_LEVEL timer starts
    Then the system lists the case on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED"

  Scenario: AC5 No legal period for the product (legacy RWB-E1-028 AC5)
    Given the LEGAL_PERIOD table has no row for "SSME"
    When SSME case RW-2026-000404 is created
    Then the prescription date is empty
    Then the system lists the case on the exception queue with MSG-P3-026 for "legal period" and "SSME"

  Scenario: AC6 No payment ever made (legacy RWB-E1-028 AC6)
    Given the rwb-source-data contract mock returns account of case RW-2026-000405 with no last payment date and contract date 2025-06-30
    Given a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30
    When the case is created
    Then the prescription date is 2027-06-30

  Scenario: AC7 Missed timer check runs (legacy RWB-E1-028 AC7)
    Given the timer check did not run from 10:00 to 10:40 and three timers passed expires_at in that time
    When the timer check runs at 10:45
    Then the system raises three breaches, one for each timer

  Scenario: AC8 A breach is raised once (legacy RWB-E1-028 AC8)
    Given the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1
    When the timer check runs again
    Then the system publishes no second TimerBreached for the timer
    Then escalation level stays 1

  Scenario: AC9 Decision log unavailable at a breach (legacy RWB-E1-028 AC9)
    Given the decision-record library of rwb-case fails its write and the rwb-decision contract mock returns an unavailable answer
    Given the decision record store is unavailable
    When the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at
    Then the timer stays RUNNING with escalation level 0
    Then the workflow history entry carries MSG-P7-003 for the timer
    Then the system raises the breach by the first run after the store is back

  Scenario: AC10 A deviation pauses the stage clock and not the prescription clock (legacy RWB-E1-028 AC10)
    Given the rwb-deviation contract mock returns DeviationRaised on 2026-12-02 and DeviationCleared on 2026-12-04
    Given case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer
    When DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04
    Then the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days
    Then the PRESCRIPTION timer stayed RUNNING with the same expires_at
    Then the case record shows MSG-P3-004 with the prescription date while the deviation was open

  Scenario: AC11 The warning point on a 5-day service level (legacy RWB-E1-028 AC11)
    Given a SERVICE_LEVEL timer of 5 working days started on Monday 2026-12-14 at 08:00
    When the timer check runs on Friday 2026-12-18 at 08:05
    Then the system sends the warning MSG-P3-003 once in that run, with end date Monday 2026-12-21
    Then no warning was sent by the run on Friday 2026-12-18 at 07:55

  Scenario: AC12 Timer scheduling goes only through TimerScheduler (legacy RWB-E1-028 AC12)
    Given case RW-2026-000409 has a RUNNING SERVICE_LEVEL timer
    When CaseStateChanged moves the case to queue "NPA-BKK-CO" and DeviationRaised arrives on the same day
    Then TimerStarter cancels the old timer through TimerScheduler.cancel and schedules the new timer through TimerScheduler.schedule
    Then TimerPauseHandler pauses and resumes the timer through TimerScheduler.pause and TimerScheduler.resume
    Then the timer row carries the paused time and the new expires_at and warn_at, and the durable timer inside CaseWorkflow fires at the new expires_at with no timer-check job
    Then the boundary test fails any class outside recovery.casewf.timers that writes or updates the timer table

  Scenario: AC13 A role without Case record R is refused the timers (from exception X9) (new, D-RCV-60)
    Given the rwb-access contract mock returns no Case record R for role RW-REFADM
    Given case RW-2026-000409 has a RUNNING SERVICE_LEVEL timer
    When RW-REFADM calls GET /cases/RW-2026-000409/timers
    Then the read is refused with 403
    Then the response carries MSG-P4-002

  Scenario: AC14 The case ID is unknown or outside the caller's scope (from exception X12) (new, D-RCV-60)
    Given the case ID of the call is unknown or outside the caller's scope
    When the caller calls GET /cases/{caseId}/timers
    Then the read answers 404 with no partial timer list
    Then the response carries MSG-P4-003

  Scenario: AC15 A legal hold keeps the clocks running and visible (from rule BR7) (new, D-RCV-60)
    Given a case with a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer
    When a legal hold is placed on the case
    Then both timers stay RUNNING with the same expires_at
    Then the case record shows the legal hold

  Scenario: AC16 The rwb-source-data contract does not answer inside 2 s (from exception X11) (new, D-RCV-60)
    Given the rwb-source-data contract mock does not answer inside 2 s for the account of a hire purchase case
    When the case is created
    Then the rwb-source-data call is retried once with jitter and then the breaker opens
    Then the prescription date is left empty and the case is listed for retry

  Scenario: AC17 A status change the model does not allow is refused (new, D-RCV-60)
    Given a timer whose status is EXPIRED with escalation level 1
    When a status change outside the transitions of section 9 is attempted on the timer
    Then the change is refused and the timer keeps its status and escalation level
    Then no TimerBreached is published by the refused change
```

**Note.** The twelve criteria are the legacy ones with their values unchanged, each carrying its origin tag. The added Givens stand in for the three answers rwb-case does not own: the account dates of P1 rwb-source-data, the two deviation events of S8 and the sealed record of P7 — in the target the port of AC12 is the timer boundary inside `CaseWorkflow`, `JOB-05` is retired, and the phrase "the timer check runs" is satisfied by the durable timer firing, while "the job record" of AC9 is the workflow history entry. The wave 1 harness RWB-ITG-E1028-ITG copies these criteria with the `-ITG` suffix. AC13 and AC14 come from exceptions X9 and X12, AC15 from rule BR7 and AC16 from exception X11; they have no legacy origin, and AC17 is new.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A `SERVICE_LEVEL` timer starts each time the case enters a queue or a status, from the `SERVICE_LEVEL` row in force for its product group and status | `SERVICE_LEVEL` (RWB-P3-E1045-APP); DL22; VR-P3-011-1; DP-06 |
| BR2 | The warning is raised at the warning percentage of the service level, once per timer | `SERVICE_LEVEL` warning percent, 80 assumed (DL22; open; ASM-1162, ASM-1304, ASM-2217, ASM-2569) |
| BR3 | A breach is raised to the named escalation role. The case does not move | R-UNI-30; REQ-CWC-011; FEAT-CWC-13 |
| BR4 | The prescription date is the earliest of last payment date plus the legal period over the linked accounts; the contract date applies when no payment exists | `LEGAL_PERIOD` (RWB-P3-E1043-APP); REQ-CWC-012; DP-07 |
| BR5 | The prescription timer never pauses, whatever pauses the stage clock | R-DEV-01; FEAT-DVH-03 |
| BR6 | A deviation pauses the stage clock; clearing it resumes the clock and recomputes the timer dates | R-UNI-04, R-UNI-43 |
| BR7 | A legal hold keeps the clocks running and visible | R-UNI-20 |
| BR8 | Service levels count working days from the calendar served by rwb-source-data and the parameter rows | `v_ace_holiday` through P1 (RWB-P1 contract); DP-05 |
| BR9 | Each timer start, warning and breach writes one decision record with its rule and version, sealed in the central ledger | REQ-CWC-016; DP-03 |
| BR10 | Timer scheduling goes only through the timer boundary inside `CaseWorkflow`; no caller writes or updates the `timer` row | ADR-011; ADR-016; FEAT-CWC-11 |
| BR11 | The clock is a durable Temporal timer, so a fire survives a restart, a release and a Continue-As-New | ADR-016; DP-10 |
| BR12 | `TimerBreached` is published once per timer type on `rwb.case.events.v1`; `TimerDue` is retired and no timer-check job exists | Architecture v5 slides 42 and 44; DP-09, DP-14 |

### 9. State transitions

None on the case. This story does not change a case status. It changes the state of the durable timer and its projection (LOV-TIMER-STATUS):

| From | Event | Condition | To |
|---|---|---|---|
| None | CaseAllocated, CaseTransferred, CaseStateChanged | Service level found for the new queue and status | RUNNING |
| RUNNING | CaseTransferred or CaseStateChanged | New queue or status | STOPPED |
| RUNNING | DeviationRaised | Timer type `SERVICE_LEVEL` | PAUSED |
| PAUSED | DeviationCleared | None | RUNNING, `expires_at` and `warn_at` recomputed |
| RUNNING | The durable timer fires at `expires_at` and the record is written | None | EXPIRED, `TimerBreached` published, escalation level 1 |
| RUNNING | The durable timer fires at `expires_at` and the record cannot be written | None | RUNNING, escalation level 0, MSG-P7-003, retaken after recovery |

The escalation level is 0 (not raised, or held) or 1 (breach raised). The `PRESCRIPTION` timer moves from RUNNING to EXPIRED only at its own date and is never PAUSED.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow identity | Starts, pauses, resumes, stops and expires the durable timers inside `CaseWorkflow`; writes the projection; sets the prescription date |
| SY-DECLOG, decision log writer | Writes the local decision record of each timer start, warning and breach and publishes it on `rwb.decision-record.v1` |
| RW-CASEOWN, case owner | Reads the timers on their cases and receives the warning (Case record R, scope Own) |
| RW-TEAMMGR, team manager | Receives the breach as the escalation point; reads timers in team scope |
| RW-LEGAL, legal counsel | Owns the `LEGAL_PERIOD` rows, loaded through the reference-data contract |
| Business lead | Owns the service level values (DL22) |
| Every role with Case record R | Reads the timers within scope |
| No role | Writes a `timer` row, a `recovery_case.prescription_date` or an event outside the workflow |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-009 | recovery_case | owner_user_id | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-CAS-017 | recovery_case | prescription_date | Write |
| DF-CAS-019 | recovery_case | deviation_open | Read |
| DF-CAS-026 | case_account | account_key | Read |
| DF-ACE-007 | v_ace_account (P1 rwb-source-data) | contract_date | Read, through the rwb-source-data contract |
| DF-ACE-026 | v_ace_account (P1 rwb-source-data) | last_payment_date | Read, through the rwb-source-data contract |
| DF-ACE-155, DF-ACE-159 | v_ace_holiday (P1 rwb-source-data) | holiday_date, holiday_weekday | Read, through the rwb-source-data contract |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Write |
| DF-WRK-041 | timer | warned_at | Write |
| DF-WRK-043 | timer | escalated_to_role | Write |
| DF-WRK-044 | timer | escalated_at | Write |
| DF-REF-184 | reference_row | row_data | Read, through the reference-data contract |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | `SERVICE_LEVEL`, `legal.prescription.warn.days` in force | Read, through the parameters contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7 rwb-decision) | all fields | Written by the local library and the ledger; read back through the P7 contract |

Field IDs are those of the Logical Data Model and Data Dictionary. The `timer` row is the projection of the durable timer: type, case, `started_at`, `expires_at`, `warn_at`, `warned_at`, paused flag, status, escalation level and the two escalation values map to DF-WRK-027 to DF-WRK-036, DF-WRK-041 and DF-WRK-043 to DF-WRK-044; no table and no field beyond those is written. No `v_ace_*` view is read directly: the account dates and the calendar come only through rwb-source-data (DP-05).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | `/cases/{caseId}/timers` | The clocks on a case: `id`, `caseId`, `timerType`, `startedAt`, `expiresAt`, `warnAt`, `paused`, `status`, `escalationLevel`, `escalatedToRole`, `escalatedAt`, ordered by `expiresAt` | Case record R, scope applied |
| GET | `/cases/{caseId}` | One case; the answer carries `prescriptionDate` beside `caseNo`, `productGroup`, `status`, `queueId`, `ownerUserId`, `deviationOpen`, `legalHold` | Case record R, scope applied |

Errors for both: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 unknown or out of scope (MSG-P4-003), 503 store down. Idempotency is not applicable to a read. The case read itself is the resource owned by RWB-P3-E1018-CON; this story adds `prescriptionDate` to its answer and writes that field only.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/source-data/v1/accounts/{accountId}` | P1 rwb-source-data | Contract date, last payment date and data as of of a linked account (GAP-2202; ASM-3616) | One hop, 2 s, GET retry once with jitter |
| GET | `/api/recovery/source-data/v1/calendar/holidays?from={from}&to={to}` | P1 rwb-source-data | The non-working days of `v_ace_holiday` for the working-day count (GAP-2202; ASM-3616) | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Case record R and scope check on both reads, cached per request | One hop, 2 s |

Three calls, no chain. The calendar answer is cached for the business date, so a case creation does not repeat it.

#### 12.3 Events published

| Event | Topic | Payload | Key |
|---|---|---|---|
| `rwb.case.TimerBreached.v1` (event 19) | `rwb.case.events.v1` | caseId, timerId, escalateTo | caseId |
| `rwb.decision.DecisionRecorded.v1` (event 08) | `rwb.decision-record.v1` | The record of a timer start, warning or breach: reference, ruleId, ruleVersion, decidedAt, escalateTo | caseId |

`TimerDue` (EV-18) is retired and is not published: the clock is inside the workflow. The outbox relay publishes both rows from `rwb_case` in CloudEvents 1.0 with no personal data (DP-09).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | Sets the prescription date and the `PRESCRIPTION` timer |
| `rwb.case.CaseAllocated.v1` | `rwb.case.events.v1` | P3 rwb-case | Starts the `SERVICE_LEVEL` timer for the new queue and status |
| `rwb.case.CaseTransferred.v1` | `rwb.case.events.v1` | P3 rwb-case | Stops the running timer and starts the next |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Stops the running timer and starts the next |
| `rwb.deviation.DeviationRaised.v1` (event 06) | `rwb.deviation.events.v1` | S8 rwb-deviation | Pauses the `SERVICE_LEVEL` timer and sets `deviation_open` (wave 2) |
| `rwb.deviation.DeviationCleared.v1` (event 07) | `rwb.deviation.events.v1` | S8 rwb-deviation | Resumes the timer and recomputes its dates (wave 2) |

The two deviation rows are consumed from wave 2; at wave 1 the same pause is reachable through the P3 case action contract (GAP-2202; ASM-3617). Every row has its inbox dedupe and its retry and `.dlt` path (DP-09).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case-{caseId} (ADR-011) | `rwb-case` | Holds the durable `SERVICE_LEVEL` and `PRESCRIPTION` timers from entry to closure, cancels and replaces them, and runs the catch-up from history |
| EvaluateRules | Activity | `rwb-case` | Resolves the service level, the warning point and the escalation role from the parameter and reference rows in force, and carries the rule ID and version |
| RecordAndApply | Activity | `rwb-case` | Writes the decision record, the `timer` projection row, `recovery_case.prescription_date` where it belongs, and the outbox rows in one transaction, and fails as one unit |

No Schedule and no Quartz job is registered by this story.

The durable timer is authoritative; the `timer` row is its audit copy, written by RecordAndApply in the same transaction as the state and read back on a reopen. The timer is read through GET /api/recovery/case/v1/cases/{caseId}/timers and the breach is published as TimerBreached on rwb.case.events.v1. No TimerDue is asserted, the deviation pause is a P3 case action at wave 1, and the P1 account-date and holiday inputs are not proved in this story; the Givens of the criteria stand in for them.

#### 12.6 Schedules

None. `JOB-05` Timer check and its five-minute Quartz schedule are retired with the `TimerDue` event (Architecture v5 slides 42 and 44; ASM-0078). This story registers no Temporal Schedule; `JOB-02`, `JOB-03` and `JOB-06` keep their owners in this service and are not touched here.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The projection: type, start, expiry, warning point, warning time, paused flag, status, escalation level, escalated role and time |
| recovery_case | P3 (rwb_case) | `prescription_date` written here; product group, status, queue, owner, deviation flag read |
| queue | P3 (rwb_case) | `queue_code` and `team_code` of the escalation role's team |
| case_account | P3 (rwb_case) | The account keys whose dates are read through P1 |
| reference_version, reference_row | P3 (rwb_case) | `LEGAL_PERIOD`, `LOV-TIMER`, `LOV-TIMER-STATUS` read through the reference-data contract |
| parameter_catalog, parameter_value | P3 (rwb_case) | `SERVICE_LEVEL` and `legal.prescription.warn.days` read through the parameters contract |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The envelope of the two published events and the inbox dedupe |

`v_ace_account` and `v_ace_holiday` belong to ACE; they are read only through rwb-source-data, and `rwb_case` holds no foreign key into another schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The P1 contract | Accounts of RW-2026-000402 (last payment 2026-03-15), RW-2026-000405 (no payment, contract date 2025-06-30), an account with no dates, and a delayed answer beyond 2 s; the calendar with 2026-12-05 to 2026-12-07 as non-working |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R, refusing RW-REFADM, and refusing a case outside the caller's scope |
| rwb-decision record double | The P7 contract | The sealed record of a warning and of a breach with `R-UNI-30`, and an unavailable answer |
| rwb-deviation event fixture | The S8 contract | `DeviationRaised` on 2026-12-02 and `DeviationCleared` on 2026-12-04 for RW-2026-000408 |
| Temporal test-time control | The workflow kit | Moves the workflow clock to the warning point, the expiry and 2028-03-15 and restores it |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | Timers and case provided; account dates, calendar and authorise consumed; one hop, 2 s |
| Kafka | 2 published, 6 consumed | TimerBreached and DecisionRecorded published; four case events and two deviation events consumed |
| Temporal | 1 workflow, 2 activities, no Schedule | CaseWorkflow with the durable timers; EvaluateRules and RecordAndApply |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.casewf.timers`, module `timers`. The segment is `casewf`, the timer boundary named in AC12 and section 17, because `case` is a Java reserved word; the rest of the name is unchanged.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The same-service CON baseline RWB-P3-E1028-CON and the sibling APP stories RWB-P3-E1045-APP and RWB-P3-E1020-APP are class H dependencies of this story and are not DP rows. No pattern is claimed for Drools (DP-04): the service level is a parameter row, not a rule package.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseEventRouter | Consumer and listener | Consumes the four case events, dedupes in the inbox and signals `CaseWorkflow` |
| TimerCommandHandler | Command inside the workflow | Cancels, schedules, pauses and resumes the durable timer; the only writer of the `timer` row through `RecordAndApply` |
| EvaluateRules | Activity | Reads the parameter and reference rows in force and returns the level, the warning point and the escalation role with the rule ID and version |
| PrescriptionCalculator | Activity | Earliest last payment plus legal period over the linked accounts, with the contract-date fallback |
| WorkingDayCalculator | Service | Adds working days with the calendar from rwb-source-data, cached per business date |
| RecordAndApply | Activity | One transaction for the record, the projection and the outbox; fails as one unit |
| DeviationSignalRouter | Consumer | Consumes the two deviation events and signals pause and resume |
| TimersController | Controller | The two read operations, the authorisation and the 404 for an unknown or out-of-scope case |
| TimerProjectionRepository | Repository | Reads and writes `timer`, `recovery_case`, `queue` in `rwb_case` only |
| AccountDatesClient, CalendarClient, AccessCheckClient | Clients | The P1 and P4 contracts with the 2 s budget, the retry and the breaker |
| TimerReadPanel | Data contract only | The fields SCR-03 shows; the panel itself belongs to RWB-P3-E2015-APP |

**Database.** One Flyway step in the per-service sequence of `rwb_case` (DP-15): `timer.escalated_to_role` (DF-WRK-043, varchar(30)) and `timer.escalated_at` (DF-WRK-044, timestamptz), both nullable, plus `ix_timer_due ON timer (expires_at) WHERE status = 'RUNNING'`, `ix_timer_warn ON timer (warn_at) WHERE status = 'RUNNING'` and the partial unique index `ux_timer_sl_running ON timer (case_id) WHERE timer_type = 'SERVICE_LEVEL' AND status IN ('RUNNING','PAUSED')`. `timer.warned_at` (DF-WRK-041) already exists. No table and no column beyond these is added.

**Configuration and reference data.** The `SERVICE_LEVEL` rows (business lead, DL22) and `legal.prescription.warn.days` = 180 (assumed, owner Legal) are read through the parameters contract; `LEGAL_PERIOD`, `LOV-TIMER` and `LOV-TIMER-STATUS` through the reference-data contract; the calendar through rwb-source-data. The two client timeouts and the retry policy are service configuration values, never code.

**Build steps**

1. Extend the generated types and the contract tests against RWB-P3-E1028-CON; the two read operations answer from the projection.
2. Flyway step: the two escalation columns and the three indexes; the boundary test that fails any class outside the timer boundary writing `timer`.
3. `EvaluateRules` over the parameters and reference contracts, with the rule ID and version on the answer; tests for AC1, AC4, AC11.
4. `WorkingDayCalculator` over the calendar answer; tests for AC1 and AC11 with 2026-12-05 to 2026-12-07 non-working.
5. `TimerCommandHandler` with cancel and schedule on each case event and the pause and resume on the deviation events; tests for AC1, AC4, AC10, AC12.
6. `PrescriptionCalculator` with the earliest-date rule and the contract-date fallback; tests for AC3, AC5, AC6 and the slow P1 answer of X11.
7. The warning fire with `warned_at` and one MSG-P3-003; tests for AC2 warning and AC11.
8. The expiry fire: `EXPIRED`, level 1, `escalated_to_role`, the record, `TimerBreached` in the outbox, one transaction; tests for AC2, AC8, AC9.
9. The catch-up from history after a worker outage, ordered by `expires_at`, each breach once; test for AC7. Then the two reads with the access check.

**Feature switch.** `rwb.p3.timers`. Off: no timer starts, the projection is not written and the two reads answer without timer rows; on: the behaviour above.

**Done when.** Every test in section 16 passes, the timers of 26,500 open cases are held and read inside the wave 1 volume of NFR-001, a fire that fell inside a 40-minute worker outage is satisfied exactly once from history in SIT, and the contract tests of RWB-P3-E1028-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | Warning point reached | {timer} ends on {date}. |
| MSG-P3-004 | Case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-026 | No service level or legal period found | No {item} is set for {scope}. The timer did not start. |
| MSG-P7-003 | Decision record write failed at a breach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-001 | No session on a read | Your session is not valid or you have no Recovery Workbench role. Sign in again or ask your team manager to request one. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case unknown or outside the scope | This case is not in your scope. |

The five legacy IDs keep their wording unchanged; MSG-P4-001 and MSG-P4-003 are the platform envelope texts of the two read errors. Thai text follows DL10 (open; ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

SCR-03 Case record in its Read only and On hold states shows the prescription date and the due date of the running service level from the two reads of section 12.1. SCR-03 Loading state per Screen Specifications v1; Empty, Error and No access states: Not specified in the source documents (CG-ALL-3619). SCR-09 Exception queue in its Loading and List states lists the cases with MSG-P3-026 for a missing service level or legal period. SCR-09 Empty, Error and No access states: Not specified in the source documents (CG-ALL-3620). Both screens are served by the gateway-bff composite route (DP-19) and both panels are built by RWB-P3-E2015-APP; this story fixes the two answers they read and no screen of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-028-01 | AC1, BR1, BR8 | End to end | Case placed in LIT-BKK-OFF at 2026-12-01 09:00 |
| TC-E1-028-02 | AC2, BR2, BR3 | End to end | Timer passing warn_at and expires_at |
| TC-E1-028-03 | AC3, BR4 | End to end | HP account, last payment 2026-03-15 |
| TC-E1-028-04 | AC4, BR1 | End to end | Queue NPA-BKK-CO with no service level |
| TC-E1-028-05 | AC5, BR4 | End to end | SSME with no legal period |
| TC-E1-028-06 | AC6, BR4 | End to end | No last payment, contract date 2025-06-30 |
| TC-E1-028-07 | AC7, BR11 | End to end | The rwb-case worker stopped for 40 minutes with three timers passing expires_at |
| TC-E1-028-08 | AC8, BR12 | End to end | Timer already EXPIRED |
| TC-E1-028-09 | AC9, BR9 | End to end | Decision record write failing at expiry |
| TC-E1-028-10 | AC10, BR5, BR6 | End to end | Deviation from 2026-12-02 to 2026-12-04 |
| TC-E1-028-11 | AC11, BR2 | End to end | 5 working days from Monday 2026-12-14 |
| TC-E1-028-12 | AC13, Access, BR10 | Component | RW-REFADM calls GET /cases/{caseId}/timers and is refused with MSG-P4-002 |
| TC-E1-028-13 | Principle 5, BR9 | NFR | Decision record write forced to fail for every breach in a run |
| TC-E1-028-14 | AC12, BR10 | Component | A class outside the timer boundary writes the timer row directly; boundary test of the service |
| TC-E1-028-15 | AC14, §12 operations, events and activities | Component | Contract test of RWB-P3-E1028-CON for each operation, event and activity of §12, with an unknown case ID |
| TC-E1-028-16 | §12.7 tables (ASM-3438) | Component | Boundary test of each table of §12.7 and of no other table |
| TC-E1-028-17 | AC15, BR7 | End to end | Legal hold placed on a case with RUNNING SERVICE_LEVEL and PRESCRIPTION timers |
| TC-E1-028-18 | AC13, X9 | Component | RW-REFADM with no Case record R calls GET /cases/RW-2026-000409/timers; refused with 403 and MSG-P4-002 |
| TC-E1-028-19 | AC14, X12 | Component | Unknown case ID on GET /cases/{caseId}/timers; 404 with MSG-P4-003 and no partial list |
| TC-E1-028-20 | AC16, X11 | NFR | rwb-source-data contract does not answer inside 2 s; one retry with jitter, then the breaker |
| TC-E1-028-21 | AC17 | Component | A timer status change outside the transitions of section 9 |

The legacy levels map as the rest of this story set maps them: System to End to end, Access to Component, Resilience to NFR and Build to Component. TC-E1-028-12 and TC-E1-028-14 prove a component boundary rather than a business journey and TC-E1-028-13 proves resilience, so they carry those levels. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same ID.

### 17. Guardrails

- No business value in code: service levels, the warning percentage, escalation roles, legal periods, the warning days and the holidays are data, read with the version in force.
- The P2 fields this story reads or writes (the case owner ID and the account dates of section 11, among others) are classed as personal data: they stay in `rwb_case` and in the contracted answers, and no personal data appears in logs, tests, workflow history, events or prompts; cases are named by case number and people by user ID.
- No read of another service's table and no direct ACE view: account dates and the calendar through rwb-source-data, authorisation through rwb-access, the ledger through rwb-decision (DP-01, DP-05).
- A breach never moves the case; the prescription timer never pauses.
- Timer scheduling goes only through the timer boundary inside `CaseWorkflow`; no class outside `recovery.casewf.timers` writes or updates the `timer` row.
- One hop and 2 s per consumed call, a breaker per downstream, and GET retried once with jitter.
- No `TimerDue` event, no timer-check job and no timer-check Schedule is created; a release that adds one fails the retired-element check.
- Every answer carries IDs, codes, dates and amounts only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-11, FEAT-CWC-13 | All recovery processes | R-UNI-30, R-UNI-43 | TC-E1-028-01, TC-E1-028-02, TC-E1-028-04, TC-E1-028-07, TC-E1-028-08, TC-E1-028-10, TC-E1-028-11, TC-E1-028-14 |
| REQ-CWC-012 | Prescription date from the legal periods at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-12 | 08 Litigate and enforce | R-DEV-01, R-UNI-20 | TC-E1-028-03, TC-E1-028-05, TC-E1-028-06, TC-E1-028-10 |
| REQ-CWC-016 | Every timer event logged with rule and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-13 | All recovery processes | R-UNI-39 | TC-E1-028-02, TC-E1-028-09, TC-E1-028-13 |
| ADR-011, ADR-016 | Durable timers in Temporal replace the Quartz job behind the same boundary | Architecture v5 slide 44; Temporal and Drools design | All three features | All recovery processes | R-UNI-30 | TC-E1-028-07, TC-E1-028-14 |

### 19. Out of scope

- The contract baseline of the two read operations, the event schema and the fakes (RWB-P3-E1028-CON).
- The deployment, the consumer groups, the dashboards, the alerts and the runbook (RWB-P3-E1028-OPS).
- The Case record R right and its refusal (RWB-P4-E1028-APP); the central ledger, its chain and its read (RWB-P7-E1028-APP).
- The prescription warning that forces a litigation review (R-UNI-31, CTL-18, Epic 2) and the timer panel with the escalation state on the case view (RWB-P3-E2015-APP).
- The notice period, cure period, offer validity and other stage-specific timers (their route stories, waves 2 to 4).
- Raising, handling and clearing deviations (S8 rwb-deviation).
- The service level values themselves (DL22) and the legal period values (Legal).
- The cross-service journey harness and its evidence (RWB-ITG-E1028-ITG).

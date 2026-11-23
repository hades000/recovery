<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 028 Service levels timers escalation and prescription dates v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!RWB E1 028 Service levels timers escalation and prescription dates v2.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-028 Service levels, timers, escalation and prescription dates

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-028 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-11 Set service levels and stage timers; FEAT-CWC-12 Set and track prescription dates; FEAT-CWC-13 Escalate a breached timer to the named point |
| Requirement IDs | REQ-CWC-011, REQ-CWC-012, REQ-CWC-016 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| L3 process | All recovery processes; 06 Take over and own the case; 08 Litigate and enforce |
| Decision | D-RCV-36 (T1, T2); ADR-011 |
| Priority | Must |
| Depends on | RWB-E1-045, RWB-E1-020, RWB-E1-027, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **a service level per queue and status, a timer on every case, a warning to the owner and a breach raised to the named escalation point by rule, and a prescription date set from the legal periods**, so that **no case waits past its limit unseen and no legal claim expires unnoticed**.

## 2. Business rationale

Deadlines are tracked in personal diaries today, and audit found litigation not filed for debtors meeting the criteria (CTL-18). This story starts a service level timer each time a case enters a queue and status, warns the owner at the warning point, raises a breach to the escalation role without moving the case, and sets the prescription date at case creation from the legal period for the product. It meets REQ-CWC-011, REQ-CWC-012 and REQ-CWC-016 and serves the measure "cases inside the service level" (target set with DL22).

Timers stay rows in the timer table. Every caller schedules, pauses, resumes and cancels a timer through the published TimerScheduler port, and TimerCheckJob (JOB-05, Quartz) is the Epic 1 implementation of that port. Epic 3 therefore replaces the implementation with Temporal durable timers without changing a caller (D-RCV-36 T2; ADR-011).

## 3. Preconditions

- RWB-E1-020 is done: CaseAllocated is published when a case gets a queue and owner.
- RWB-E1-045 is done: ProductParameterService serves the SERVICE_LEVEL row for a product group and a case status, with limit, unit, warning percent and escalation role.
- RWB-E1-043 is done: ReferenceDataService serves the LEGAL_PERIOD table in force, and the holiday calendar is read from v_ace_holiday over the ACE Bank of Thailand table bot_holiday.
- RWB-E1-027 is done: the decision log writer is available.
- The published TimerScheduler port exists in the module (package recovery.casewf.timers) and TimerCheckJob (JOB-05, Quartz) implements it (D-RCV-36 T2).
- SERVICE_LEVEL row, values assumed until the business sets them (DL22): product group HIRE_PURCHASE, status ASSIGNED, limit 5 working days, warning percent 80, escalation role RW-TEAMMGR.
- LEGAL_PERIOD row owned by Legal: HIRE_PURCHASE 2 years from the last payment date (assumed value from the current story; other products loaded by Legal). Parameter `legal.prescription.warn.days` = 180 (assumed) from RWB-E1-042.
- v_ace_holiday marks 2026-12-05 to 2026-12-07 as non-working days (synthetic test values).
- JOB-05 runs every 5 minutes as SY-CASEWF through the TimerScheduler port of section 12.

## 4. Flow

1. TimerStarter: on CaseAllocated, CaseTransferred or CaseStateChanged, cancels the running SERVICE_LEVEL timer of the case through TimerScheduler.cancel(timerId).
2. TimerStarter: reads the service level for the new queue and status and calls TimerScheduler.schedule(TimerSpec) with started_at, expires_at in working days and warn_at at the warning percentage; the port writes the timer row.
3. PrescriptionService: on CaseCreated, reads the last payment date of each linked account through the P1 interface and the legal period for the product, and sets the earliest result as the prescription date.
4. PrescriptionService: schedules a PRESCRIPTION timer through TimerScheduler.schedule with expires_at on the prescription date and warn_at 180 days before; a PRESCRIPTION timer never pauses.
5. TimerCheckJob (JOB-05): every 5 minutes finds RUNNING timers whose warn_at or expires_at has passed.
6. TimerCheckJob: for a passed warn_at, writes the decision log entry and sends MSG-P3-003 to the case owner once.
7. TimerCheckJob: for a passed expires_at of a SERVICE_LEVEL timer, writes the decision log entry with rule R-UNI-30, sets the timer EXPIRED with escalation level 1, and publishes TimerBreached with the escalation role; the case keeps its queue and owner.
8. TimerCheckJob: for a passed expires_at of any other timer type, sets it EXPIRED and publishes TimerDue.
9. TimerPauseHandler: on DeviationRaised calls TimerScheduler.pause(timerId); on DeviationCleared calls TimerScheduler.resume(timerId), which moves expires_at and warn_at by the paused time (R-UNI-43).
10. Case owner or team manager: reads the timers through GET /cases/{caseId}/timers and the prescription date through GET /cases/{caseId}.
11. No caller writes or updates the timer table directly: every schedule, cancel, pause and resume goes through TimerScheduler (BR10).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No SERVICE_LEVEL version is in force on the date | No timer; the case is listed on the exception queue | MSG-P3-026 | AC4 |
| X2 | No legal period for the product | Prescription date not set; the case is listed on the exception queue | MSG-P3-026 | AC5 |
| X3 | An account has no last payment date | The contract date is used | None | AC6 |
| X4 | JOB-05 did not run for 40 minutes | The next run raises every missed warning and breach once | None | AC7 |
| X5 | The timer check runs again after a breach | The breach is not raised twice | None | AC8 |
| X6 | Decision log write fails at a breach | The timer stays RUNNING and the breach is raised by the next run | MSG-P7-003 | AC9 |
| X7 | A deviation is raised on the case | Service level timer paused; prescription timer keeps running | MSG-P3-004 | AC10 |
| X8 | The warning point is 4 of 5 working days | Warning sent once, at the first check after 4 working days have passed | MSG-P3-003 | AC11 |
| X9 | A role without Case record R reads the timers | Refused with 403 | MSG-P4-002 | Access test TC-E1-028-12 |
| X10 | A class outside `recovery.casewf.timers` writes or updates the timer table | The build fails on the boundary test; no timer row is changed at run time | None | AC12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Listens to case events from RWB-E1-018 and RWB-E1-020; values from RWB-E1-043 and RWB-E1-045 |
| Negotiable | Service levels, the warning point, escalation roles and legal periods are parameters |
| Valuable | Every case and every legal claim carries a visible deadline |
| Estimable | One timer service, one port, one job, one prescription calculator, one read endpoint |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Service levels, timers, escalation and prescription dates

  Background:
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" and "ASSIGNED" is 5 working days with warning percent 80 and escalation role RW-TEAMMGR
    Given the LEGAL_PERIOD row for "HIRE_PURCHASE" is 2 years from the last payment date
    Given 2026-12-05 to 2026-12-07 are not working days in v_ace_holiday

  Scenario: AC1 Timer starts
    Given hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00
    When the case arrives
    Then a SERVICE_LEVEL timer is RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00
    Then GET /cases/{caseId}/timers returns the timer with its due date

  Scenario: AC2 Warning and escalation
    Given the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at
    When the timer check runs after each point
    Then owner U-31 receives MSG-P3-003 at the warning point
    Then the system raises at expiry the breach to RW-TEAMMGR of team "LIT-BKK" with TimerBreached and escalation level 1
    Then the case keeps queue "LIT-BKK-OFF" and owner U-31
    Then both the warning and the breach have a decision log entry, the breach with rule R-UNI-30

  Scenario: AC3 Prescription date
    Given a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15
    When the case is created
    Then the prescription date is 2028-03-15
    Then a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17
    Then GET /cases/{caseId} shows prescription date 2028-03-15

  Scenario: AC4 No service level for the queue and status
    Given no SERVICE_LEVEL version is in force on 2026-12-01
    When case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01
    Then no SERVICE_LEVEL timer starts
    Then the system lists the case on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED"

  Scenario: AC5 No legal period for the product
    Given the LEGAL_PERIOD table has no row for "SSME"
    When SSME case RW-2026-000404 is created
    Then the prescription date is empty
    Then the system lists the case on the exception queue with MSG-P3-026 for "legal period" and "SSME"

  Scenario: AC6 No payment ever made
    Given a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30
    When the case is created
    Then the prescription date is 2027-06-30

  Scenario: AC7 Missed timer check runs
    Given JOB-05 did not run from 10:00 to 10:40 and three timers passed expires_at in that time
    When JOB-05 runs at 10:45
    Then the system raises three breaches, one for each timer

  Scenario: AC8 A breach is raised once
    Given the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1
    When JOB-05 runs again
    Then the system publishes no second TimerBreached for the timer
    Then escalation level stays 1

  Scenario: AC9 Decision log unavailable at a breach
    Given the decision log store is unavailable
    When the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at
    Then the timer stays RUNNING with escalation level 0
    Then the job record carries MSG-P7-003 for the timer
    Then the system raises the breach by the first run after the store is back

  Scenario: AC10 A deviation pauses the stage clock and not the prescription clock
    Given case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer
    When DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04
    Then the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days
    Then the PRESCRIPTION timer stayed RUNNING with the same expires_at
    Then the case record shows MSG-P3-004 with the prescription date while the deviation was open

  Scenario: AC11 The warning point on a 5-day service level
    Given a SERVICE_LEVEL timer of 5 working days started on Monday 2026-12-14 at 08:00
    When the timer check runs on Friday 2026-12-18 at 08:05
    Then the system sends the warning MSG-P3-003 once in that run, with end date Monday 2026-12-21
    Then no warning was sent by the run on Friday 2026-12-18 at 07:55

  Scenario: AC12 Timer scheduling goes only through TimerScheduler
    Given case RW-2026-000409 has a RUNNING SERVICE_LEVEL timer
    When CaseStateChanged moves the case to queue "NPA-BKK-CO" and DeviationRaised arrives on the same day
    Then TimerStarter cancels the old timer through TimerScheduler.cancel and schedules the new timer through TimerScheduler.schedule
    Then TimerPauseHandler pauses and resumes the timer through TimerScheduler.pause and TimerScheduler.resume
    Then the timer row carries the paused time and the new expires_at and warn_at, and JOB-05 finds the due timer on its next 5-minute run
    Then the boundary test fails any class outside recovery.casewf.timers that writes or updates the timer table
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A SERVICE_LEVEL timer starts each time the case enters a queue or a status, from the SERVICE_LEVEL row for its product group and status | SERVICE_LEVEL table (RWB-E1-045); DL22; VR-P3-011-1 |
| BR2 | The warning is raised at the warning percentage of the service level | SERVICE_LEVEL warning percent, 80 assumed (DL22) |
| BR3 | A breach is raised to the named escalation role. The case does not move | R-UNI-30; REQ-CWC-011; FEAT-CWC-13 |
| BR4 | The prescription date is the earliest of last payment date plus the legal period over the linked accounts; the contract date applies when no payment exists | LEGAL_PERIOD table (RWB-E1-043); REQ-CWC-012 |
| BR5 | The prescription timer never pauses | R-DEV-01; FEAT-DVH-03; Timer.paused description in api.yaml |
| BR6 | A deviation pauses the stage clock; clearing it resumes the clock and recomputes the timers | R-UNI-04, R-UNI-43 |
| BR7 | A legal hold keeps the clocks running and visible | R-UNI-20 |
| BR8 | Service levels count working days from the holiday calendar in v_ace_holiday | v_ace_holiday over public.bot_holiday (RWB-E1-043) |
| BR9 | Each timer start, warning and breach is logged with its rule and version | REQ-CWC-016; Principle 5 |
| BR10 | Timer scheduling goes only through TimerScheduler: every caller schedules, pauses, resumes and cancels a timer through the port, and no caller writes or updates the timer table | D-RCV-36 T2; ADR-011; FEAT-CWC-11 |

## 9. State transitions

None. This story does not change a case status. It changes the timer status (LOV-TIMER-STATUS):

| From | Event | Condition | To |
|---|---|---|---|
| None | CaseAllocated, CaseTransferred, CaseStateChanged | Service level found | RUNNING |
| RUNNING | CaseTransferred or CaseStateChanged | New queue or status | STOPPED |
| RUNNING | DeviationRaised | Timer type SERVICE_LEVEL | PAUSED |
| PAUSED | DeviationCleared | None | RUNNING, expires_at recomputed |
| RUNNING | JOB-05 | expires_at passed | EXPIRED, TimerBreached or TimerDue |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF | Starts, pauses, resumes, stops and expires timers through TimerScheduler; sets the prescription date |
| SY-DECLOG | Writes the entries |
| RW-CASEOWN | Reads the timers on their cases and receives the warning |
| RW-TEAMMGR | Receives the breach as the escalation point; reads timers in team scope |
| RW-LEGAL | Owns the LEGAL_PERIOD rows; they are loaded through RWB-E1-043 |
| Business lead | Owns the service level values (DL22) |
| Every role with Case record R | Reads the timers within scope |

## 11. Data

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
| DF-ACE-007 | v_ace_account | contract_date | Read |
| DF-ACE-026 | v_ace_account | last_payment_date | Read |
| DF-WRK-002 | queue | queue_code | Read |
| DF-WRK-004 | queue | team_code | Read |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Write |
| DF-WRK-041 | timer | warned_at | Write |
| DF-REF-184 | reference_row | row_data | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write |

reference_row is a new entity of RWB-E1-043, read through ReferenceDataService and ProductParameterService. Field IDs are those in the Logical Data Model and Data Dictionary.

Timer rows stay the record of a timer: the TimerSpec of the TimerScheduler port names the timer type, the case, started_at, expires_at and warn_at, and those values map to DF-WRK-027 to DF-WRK-036 and DF-WRK-041. The port writes no new table and no new field.

## 12. Contract

**Job**

| Item | Value |
|---|---|
| Trigger | Quartz schedule |
| Job name | JOB-05 Timer check |
| Engine | Quartz; this job is the Epic 1 implementation of the TimerScheduler port (D-RCV-36 T2), with no Temporal schedule |
| Schedule | Every 5 minutes |
| Input | RUNNING timers with warn_at or expires_at before now (index ix_timer_due) |
| Output | Warnings, breaches, expired timers, decision log entries |
| Events published | TimerBreached (EV-19: timerId, caseId, escalateTo); TimerDue (EV-18: timerId, caseId, timerType) |
| Idempotency key | timerId and the point (WARN or EXPIRE); a timer already EXPIRED or already warned is skipped |
| Restart | The next run picks up every missed timer (batch.txt JOB-05) |

**Events consumed.** CaseCreated (EV-01), CaseAllocated (EV-02), CaseTransferred (EV-04), CaseStateChanged (EV-05), DeviationRaised (EV-06), DeviationCleared (EV-07).

**GET /api/recovery/v1/cases/{caseId}/timers**

| Item | Value |
|---|---|
| Request | Path caseId (uuid) |
| Response | Timer[]: id, caseId, timerType, startedAt, expiresAt, warnAt, paused, status, escalationLevel |
| Errors | 401 (MSG-P4-001); 403 no Case record R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

GET /api/recovery/v1/cases/{caseId} returns prescriptionDate (Case schema).

**Published interfaces** (package `recovery.casewf.timers`)

```java
// P3, package recovery.casewf.timers (published)
public interface TimerScheduler { void schedule(TimerSpec t); void cancel(UUID timerId); void pause(UUID timerId); void resume(UUID timerId); }

// P3, package recovery.casewf.timers (published)
public interface TimerService {
    List<TimerView> timersFor(UUID caseId);
    Optional<LocalDate> prescriptionDate(UUID caseId);
}
// P3 (RWB-E1-045) and P3 (RWB-E1-043), used by this story
ServiceLevel serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);   // ProductParameterService
VersionedRows rows(String tableCode, LocalDate businessDate);                                // ReferenceDataService: LEGAL_PERIOD
// P1, used by this story
public interface RecoveryDataQuery {
    List<AccountDates> accountDates(List<UUID> accountIds);   // contract_date, last_payment_date, data_as_of
    List<LocalDate> holidays(LocalDate from, LocalDate to);   // the non-working dates of v_ace_holiday
}
```

Every caller schedules, cancels, pauses and resumes a timer through TimerScheduler and no caller writes a timer row directly. TimerCheckJob (JOB-05, Quartz) is the Epic 1 implementation: schedule, cancel, pause and resume write or change the timer row, and the 5-minute fire runs the warning, breach and expiry check. Epic 3 replaces that implementation with Temporal durable timers and no caller changes (ADR-011).

## 13. Solution plan

**Package.** `recovery/casewf/timers`, Java package `recovery.casewf.timers`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TimerStarter | Listener | Starts and stops SERVICE_LEVEL timers on case events through TimerScheduler |
| PrescriptionService | Listener | Sets the prescription date and schedules the PRESCRIPTION timer through TimerScheduler on CaseCreated |
| TimerPauseHandler | Listener | Pauses and resumes SERVICE_LEVEL timers through TimerScheduler on deviation events |
| TimerCheckJob | Job | JOB-05 on Quartz; implements TimerScheduler (schedule, cancel, pause, resume) and runs the warning, breach and expiry checks |
| TimerScheduler | Published interface | The port every caller uses to schedule, cancel, pause and resume a timer; the Epic 1 implementation is TimerCheckJob |
| WorkingDayCalculator | Service | Adds working days with the holiday calendar from v_ace_holiday |
| TimerService | Published interface | Reads timers and the prescription date for other modules |
| CaseAndWorkflowController | Controller | GET /cases/{caseId}/timers |
| CaseAndWorkflowRepository | Repository | timer, recovery_case |

**Database**

- Writes timer (all columns) through the TimerScheduler implementation only, recovery_case.prescription_date, outbox.
- Reads with index ix_timer_due (expires_at WHERE status = 'RUNNING'); add `ix_timer_warn ON timer (warn_at) WHERE status = 'RUNNING'` in migration `V028_1__timer_warn_index.sql`, plus column timer.warned_at (New) to record the single warning.
- One running SERVICE_LEVEL timer per case: partial unique index `ux_timer_sl_running ON timer (case_id) WHERE timer_type = 'SERVICE_LEVEL' AND status IN ('RUNNING','PAUSED')`.

**Configuration and reference data**

- SERVICE_LEVEL rows (business lead, DL22) through ProductParameterService (RWB-E1-045).
- LEGAL_PERIOD rows through ReferenceDataService (RWB-E1-043), owned by Legal; the holiday calendar through v_ace_holiday (DF-ACE-155 holiday_date, DF-ACE-159 holiday_weekday).
- Parameter legal.prescription.warn.days = 180 (assumed; owner Legal) through RWB-E1-042.
- LOV-TIMER and LOV-TIMER-STATUS.

**Build steps**

1. Build the TimerScheduler port and its Quartz implementation in TimerCheckJob: schedule, cancel, pause and resume write the timer row; test AC12 with the boundary test.
2. WorkingDayCalculator with the holiday calendar from v_ace_holiday; unit tests for AC1 and AC11.
3. TimerStarter with cancel and schedule on each case event through TimerScheduler; test AC1, AC4, AC12.
4. PrescriptionService with the earliest-date rule and the contract date fallback; tests AC3, AC5, AC6.
5. TimerCheckJob warning branch with warned_at; test AC2 warning, AC11.
6. TimerCheckJob expiry branch: EXPIRED, TimerBreached in the outbox and the decision log write in one transaction; tests AC2, AC8, AC9.
7. Catch-up of missed runs in one pass ordered by expires_at; test AC7.
8. TimerPauseHandler with pause and resume through TimerScheduler and recomputed dates; test AC10.
9. GET /cases/{caseId}/timers with access check.

**Feature flag.** `rwb.p3.timers`. Off: no timers start, the TimerScheduler implementation is not registered and JOB-05 does nothing.

**Done when.** The tests in section 16 pass and JOB-05 handles 26,500 open cases' timers inside one 5-minute cycle in SIT (NFR-001 volume).

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-003 | Warning point reached | {timer} ends on {date}. |
| MSG-P3-004 | Case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P3-026 | No service level or legal period found | No {item} is set for {scope}. The timer did not start. |
| MSG-P7-003 | Decision log write failed at a breach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

SCR-03 Case record (read only; on hold) shows the prescription date and the due date of the running service level. SCR-09 Exception queue (Loading; list) lists cases with MSG-P3-026. The timer panel with the stage clock comes in Epic 2 (RWB-E2-015).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-028-01 | AC1, BR1, BR8 | System | Case placed in LIT-BKK-OFF at 2026-12-01 09:00 |
| TC-E1-028-02 | AC2, BR2, BR3 | System | Timer passing warn_at and expires_at |
| TC-E1-028-03 | AC3, BR4 | System | HP account, last payment 2026-03-15 |
| TC-E1-028-04 | AC4, BR1 | System | Queue NPA-BKK-CO with no service level |
| TC-E1-028-05 | AC5, BR4 | System | SSME with no legal period |
| TC-E1-028-06 | AC6, BR4 | System | No last payment, contract date 2025-06-30 |
| TC-E1-028-07 | AC7 | System | JOB-05 stopped for 40 minutes |
| TC-E1-028-08 | AC8 | System | Timer already EXPIRED |
| TC-E1-028-09 | AC9, BR9 | System | Decision log store down at expiry |
| TC-E1-028-10 | AC10, BR5, BR6 | System | Deviation from 2026-12-02 to 2026-12-04 |
| TC-E1-028-11 | AC11, BR2 | System | 5 working days from Monday 2026-12-14 |
| TC-E1-028-12 | Access | Access | RW-REFADM calls GET /cases/{caseId}/timers and is refused with MSG-P4-002 |
| TC-E1-028-13 | Principle 5 | Resilience | Decision log write forced to fail for every breach in a run |
| TC-E1-028-14 | AC12, BR10 | Build | A class outside recovery.casewf.timers writes the timer table directly; boundary test of RWB-TE-001 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: service levels, the warning point, escalation roles, legal periods and holidays are data.
- No personal data in logs, tests, workflow history or prompts; cases are named by case number.
- No read of another module's tables; ACE data only through recovery.v_ace_* views: account dates through RecoveryDataQuery (P1).
- A breach never moves the case; the prescription timer never pauses.
- Timer scheduling goes only through TimerScheduler; no class outside recovery.casewf.timers writes or updates the timer table.
- No Temporal schedule and no Temporal durable timer in Epic 1: JOB-05 stays on Quartz behind the port (D-RCV-36 T2).

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-11, FEAT-CWC-13 | All recovery processes | R-UNI-30, R-UNI-43 | TC-E1-028-01, TC-E1-028-02, TC-E1-028-04, TC-E1-028-07, TC-E1-028-08, TC-E1-028-10, TC-E1-028-11, TC-E1-028-14 |
| REQ-CWC-012 | Prescription date from the legal periods at creation | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-12 | 08 Litigate and enforce | R-DEV-01, R-UNI-20 | TC-E1-028-03, TC-E1-028-05, TC-E1-028-06, TC-E1-028-10 |
| REQ-CWC-016 | Every timer event logged with rule and version | Epic 1, 3.3; Program, 5.3 | FEAT-CWC-13 | All recovery processes | R-UNI-39 | TC-E1-028-02, TC-E1-028-09, TC-E1-028-13 |

## 19. Out of scope

- The prescription warning forcing a litigation review (R-UNI-31, CTL-18, Epic 2).
- The timer panel and escalation state on the case view (RWB-E2-015).
- The notice period, cure period, offer validity and other stage-specific timers (their route stories, Epic 3 to Epic 6).
- Temporal durable timers replace the Quartz implementation in Epic 3 (ADR-011).
- The service level values themselves (DL22).

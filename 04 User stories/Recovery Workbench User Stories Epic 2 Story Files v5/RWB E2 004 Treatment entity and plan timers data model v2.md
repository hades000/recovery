# RWB-E2-004 Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E2-004 |
| Epic | E2, release 31 December 2026 |
| Module | P3 Case and workflow, with P1 Recovery data engine for the data product |
| Feature | FEAT-CHO-06 Hold the treatment entity and plan timers |
| Requirement IDs | REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 |
| BRD section | Business Requirements Epic 2, sections 3.3 and 4; Business Requirements Program, sections 5.1 and 5.3 |
| L3 process | 7.3 Negotiate settlement or deed in lieu |
| Decision | D-RCV-36; ADR-011; ADR-012 |
| Priority | Must |
| Depends on | RWB-E1-018, RWB-E1-028, RWB-E1-045, RWB-E1-072, RWB-E2-042 |
| Status | Ready for build |

## 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the treatment record (TDR, settlement, deed in lieu: terms, approval, booking, outcome) and its plan timers held in the Workbench, with the treatment data product for reporting**, so that **TDR and deed in lieu run inside the Workbench from Epic 2 and every plan has a record and a clock**.

## 2. Business rationale

Today a restructure plan is agreed in ACE and NLEADS, and nothing in recovery holds its terms or watches its payment dates, so a missed installment is found late. About 3,000 restructure accounts a month reach the restructure process (NFR-005) and deed in lieu is planned at 1,000 cases a month in 2027 (NFR-006). This story creates the treatment record with its terms and approval, starts the installment timer from the first due date and starts the cure period when a payment is missed. It meets REQ-CHO-006, REQ-CHO-007 and REQ-RDF-014. The measure is that every approved plan has one treatment row and a running installment timer the day it is recorded.

The plan rules R-RES-25 and R-RES-27 are rows of package RESTRUCTURE under ADR-012, fixed by D-RCV-36 on 16 November 2026, and the plan timers are scheduled through the TimerScheduler port (D-RCV-36 T2). JOB-05 stays the Quartz implementation in Epics 1 and 2, so Epic 3 can swap in Temporal durable timers (ADR-011) without changing a caller.

## 3. Preconditions

- RWB-E1-018 is done: the case record exists with its route state.
- RWB-E1-028 is done: the timer engine runs and JOB-05 Timer check is the Quartz implementation of TimerScheduler, so every caller schedules, pauses, resumes and cancels through TimerScheduler.
- RWB-E1-045 is done: CURE_PERIOD_DAYS and `plan.warn-days` are product parameters in force (values per DL22; `plan.warn-days` assumed 3).
- RWB-E1-072 is done: RuleEvaluator, RuleCatalog and the rule package store exist.
- RWB-E2-042 is done: package RESTRUCTURE is in force with rows R-RES-25 and R-RES-27, and each row carries action_text, owner_role and timer_spec.
- The decision log writer of RWB-E1-027 is available through the P7 published interface.
- LOV-TIMER carries the value INSTALLMENT_DUE (new list value, see Additions), loaded by the reference data administrator.
- The approval of the plan is already written to the decision log by its approver's flow (P7), so a decision log entry ID exists.
- The caller of `TreatmentRecords.recordApproved(...)` is the ACE plan status reader (RWB-E2-002) under SY-CASEWF, or a test harness in SIT.

## 4. Flow

1. ACE plan status reader (SY-CASEWF): calls `TreatmentRecords.recordApproved(...)` with the case ID, treatment type, terms, approval level, the approval's decision log entry ID and the first due date.
2. Treatment service: checks the case exists and is open through the P3 case interface, and that the decision log entry exists and names an approver through the P7 interface.
3. Treatment service: checks the required fields and the list values; writes one `treatment` row and the TreatmentApproved event (EV-10) in the outbox, in one transaction.
4. Plan timer listener (P3): consumes TreatmentApproved; finds the case in route state BOOKED_IN_ALS_NLEADS and the terms carrying a first due date (event SCHEDULE_SET).
5. SY-RULES: builds PlanTimerFacts for the case (treatment type, product group, route state, first due date, installments) and calls RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate); the R-RES-25 row returns the action "start the plan timers", the to state PLAN_RUNNING, the package version and the timer spec.
6. Plan timer listener: writes the decision log entry with rule R-RES-25 and the package version; only after that succeeds calls TimerScheduler.schedule with the INSTALLMENT_DUE TimerSpec, sets the route state to PLAN_RUNNING and publishes CaseStateChanged (EV-05).
7. JOB-05 Timer check, the Quartz implementation of TimerScheduler: at the timer's expiry publishes TimerDue (EV-18) with the timer type and the treatment ID, and sets the timer status to EXPIRED.
8. Payment matching (P8, JOB-07): publishes PaymentMissed (EV-12) when no payment matched the installment.
9. Plan timer listener: consumes PaymentMissed; calls RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate) for R-RES-27; writes the decision log entry with the rule ID and the package version, then calls TimerScheduler.schedule with the CURE_PERIOD TimerSpec built from CURE_PERIOD_DAYS for the product, and sets the route state to PLAN_CURE_PERIOD.
10. JOB-15 Reporting extract: each night reads changed treatments through `TreatmentRecords.changedSince(...)` and writes the treatment data product (DP04) with each treatment's status.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is missing (type, approval level, decision log entry, first due date for a restructure) | The record is refused; nothing is written | MSG-GEN-001 | AC4 |
| X2 | The decision log entry does not exist or has no approver | The record is refused | MSG-GEN-001 | AC5 |
| X3 | The first due date is before the proposed date | The record is refused | MSG-GEN-003 | AC6 |
| X4 | The case is not in route state BOOKED_IN_ALS_NLEADS when the event arrives | No timer; the case goes to the exception queue with the gap | MSG-P3-005 | AC7 |
| X5 | The same TreatmentApproved event arrives twice | The second is ignored and counted; one timer only | None | AC8 |
| X6 | The decision log write fails when the timer would start | No timer and no state change; the event is retried, then sent to the exception queue | MSG-P7-003 | AC9 |
| X7 | The nightly extract fails | The data product keeps the previous date and shows it as stale | MSG-P1-001 | AC10 |
| X8 | The case is closed | The record is refused | MSG-P3-005 | AC11 |
| X9 | No RESTRUCTURE version is IN_FORCE on the business date | NoPackageInForce; no decision log entry, no timer and no route state change; the case goes to the exception queue for a person | MSG-P3-027 | AC13 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the case record, the timer engine, the product parameters, the evaluator of RWB-E1-072 and the RESTRUCTURE package of RWB-E2-042 |
| Negotiable | Timer lengths and warning days are product parameters; the story fixes the record and the timer behavior |
| Valuable | Every approved plan has a record, a due date and a cure period that starts by rule |
| Estimable | One table, one service, one listener, one extract step, one rule package |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is one test against a PostgreSQL test container with a controlled clock |

## 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers data model

  Background:
    Given the business date is 2026-12-01
    Given case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"
    Given decision log entry "DLE-9001" records the approval of a restructure at level "L4" by user "U-APR-01"
    Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25 and R-RES-27

  Scenario: AC1 Treatment created
    Given a TDR plan approved for "RW-2026-000201" with 36 installments, offer amount 850000.00 baht, approval level "L4" and decision log entry "DLE-9001"
    When the record is written
    Then one treatment exists with type "RESTRUCTURE", installments 36, offer amount 850000.00, approval level "L4", decision log entry "DLE-9001" and the case link
    Then booked at is empty until the booking is confirmed
    Then one TreatmentApproved event is in the outbox with the treatment ID and the case ID

  Scenario: AC2 Timer set
    Given a plan with the first payment due on 2026-12-31
    When the record is written and the plan timer listener processes TreatmentApproved
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-01) returns rule R-RES-25 and package version "RES-2026.12"
    Then one decision log entry with rule "R-RES-25" and version "RES-2026.12" is written first
    Then one "INSTALLMENT_DUE" timer exists with expires at 2026-12-31 23:59 Asia/Bangkok, warn at 2026-12-28 and status "RUNNING", scheduled through TimerScheduler
    Then the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"
    Then when the clock passes 2026-12-31 23:59 and JOB-05, the Quartz implementation of TimerScheduler, runs, the system publishes a TimerDue event with timer type "INSTALLMENT_DUE" and the treatment ID
    Then the timer status is "EXPIRED"

  Scenario: AC3 Data product
    Given ten treatments recorded on 2026-12-01 across "MORTGAGE", "HIRE_PURCHASE" and "SSME"
    Given two of them have a booked at date
    When the reporting extract runs at 01:30 on 2026-12-02
    Then the treatment data product holds ten rows for business date 2026-12-01
    Then eight show status "APPROVED" and two show status "BOOKED"

  Scenario: AC4 Required field missing
    Given a restructure plan for "RW-2026-000201" with no first due date
    When the record is written
    Then the system refuses it with MSG-GEN-001 naming "first due date"
    Then no treatment and no event are written

  Scenario: AC5 Approval not in the decision log
    Given a plan that names decision log entry "DLE-0000" which does not exist
    When the record is written
    Then the system refuses it with MSG-GEN-001 naming "decision log entry"

  Scenario: AC6 First due date before the proposal
    Given a plan proposed on 2026-12-01 with the first due date 2026-11-30
    When the record is written
    Then the system refuses it with MSG-GEN-003 naming "first due date" and "proposed at"

  Scenario: AC7 Case not in the booked state
    Given case "RW-2026-000202" in route state "WITH_FCR_OFFICER"
    When a TreatmentApproved event with a first due date arrives for it
    Then the system writes no timer
    Then the system places the case in the exception queue with MSG-P3-005 naming "PLAN_RUNNING" and "WITH_FCR_OFFICER"

  Scenario: AC8 Event delivered twice
    Given the TreatmentApproved event for the AC1 treatment was processed
    When the same event with the same event ID arrives again
    Then no second timer and no second decision log entry are written
    Then the system counts the repeat as an idempotency hit

  Scenario: AC9 Decision log write fails
    Given the decision log store is unavailable
    When the plan timer listener processes TreatmentApproved for "RW-2026-000201"
    Then the system writes no timer and the route state stays "BOOKED_IN_ALS_NLEADS"
    Then the system retries the event 3 times and then placed in the exception queue with an incident and MSG-P7-003

  Scenario: AC10 Extract fails
    Given the reporting extract of 2026-12-02 fails
    When a reporting and BI analyst reads the treatment data product
    Then it shows business date 2026-12-01 with MSG-P1-001

  Scenario: AC11 Case closed
    Given case "RW-2026-000203" with status "CLOSED"
    When a plan is recorded for it
    Then the system refuses it with MSG-P3-005

  Scenario: AC12 Payment missed starts the cure period
    Given the AC2 timer expired on 2026-12-31
    When a PaymentMissed event arrives for the treatment with due date 2026-12-31 on business date 2027-01-01
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2027-01-01) returns rule R-RES-27 and package version "RES-2026.12"
    Then the system writes a decision log entry with rule "R-RES-27" and version "RES-2026.12" first
    Then one "CURE_PERIOD" timer exists with expires at 2027-01-31, scheduled through TimerScheduler
    Then the case route state is "PLAN_CURE_PERIOD"

  Scenario: AC13 No RESTRUCTURE version in force
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-01
    When the plan timer listener processes TreatmentApproved for "RW-2026-000201"
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry, no timer and no route state change are written
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap

  Scenario: AC14 Plan timers go only through TimerScheduler
    Given the plan timer listener holds an "INSTALLMENT_DUE" TimerSpec for case "RW-2026-000201"
    When the listener schedules the timer
    Then the timer is created by TimerScheduler and carries the case ID, the treatment ID, the timer type and the expiry
    Then a component that inserts into the timer table without TimerScheduler fails the boundary test and the build
    Then JOB-05, the Quartz implementation of TimerScheduler, is the only code that expires the timer
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every offer approved for a customer has one treatment row with its type, terms, approval level, the approval's decision log entry and its outcome | REQ-CHO-006; LOV-TREATMENT |
| BR2 | A restructure needs installments above 0 and a first due date on or after the proposed date | R-RES-25 (condition first_due_date set) |
| BR3 | The plan timers start when the schedule is set on a booked plan, and the case moves to PLAN_RUNNING | R-RES-25 |
| BR4 | When a due date passes with no payment matched, the cure period starts with CURE_PERIOD_DAYS from reference data | R-RES-27; RWB-E1-045 |
| BR5 | The warning is raised `plan.warn-days` before the due date (assumed 3; DL22) | REQ-CWC-011 |
| BR6 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 |
| BR7 | A repeated event with the same key is ignored and counted | R-UNI-40; events.txt Rules |
| BR8 | The treatment data product carries one row per treatment with its status: APPROVED (no booked at), BOOKED, RUNNING, BROKEN, COMPLETED, CANCELED (from outcome) | REQ-RDF-014; LOV-TRT-OUTCOME |
| BR9 | A plan whose case is not in the state the rule expects goes to the exception queue for a person | R-RES-35 pattern; R-UNI-41 |
| BR10 | R-RES-25 and R-RES-27 are rows of package RESTRUCTURE, evaluated by RuleEvaluator; the result names the rule and the package version, and the action text, owner role and timer spec come from RuleCatalog | D-RCV-36 T5, T6, T7; ADR-012 |
| BR11 | A plan timer is scheduled, paused, resumed and cancelled only through TimerScheduler; JOB-05 is its Quartz implementation in Epics 1 and 2 | D-RCV-36 T2; RWB-E1-028 |
| BR12 | No RESTRUCTURE version in force is a refusal (NoPackageInForce), never a default timer or move | R-UNI-41; D-RCV-36 T7 |

## 9. State transitions

The case status does not change (it stays In progress). The route state changes:

| From | Event | Condition | To |
|---|---|---|---|
| BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set (R-RES-25) | PLAN_RUNNING |
| PLAN_RUNNING | PAYMENT_MISSED | due date passed and no payment matched (R-RES-27) | PLAN_CURE_PERIOD |

Timer status: RUNNING to EXPIRED when the INSTALLMENT_DUE timer passes its expiry, through TimerScheduler and its Quartz implementation JOB-05.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Records the treatment through the published interface; schedules the plan timers through TimerScheduler and writes the route state (Case record CRU; Treatment and offer R through the interface) |
| SY-RULES, Drools evaluator | Evaluates R-RES-25 and R-RES-27 in package RESTRUCTURE and reads the catalog row |
| SY-DECLOG, decision log writer | Writes the entries (Decision log C) |
| RW-RESTRUCT, restructuring officer | Reads the treatment (Treatment and offer CRUA) |
| RW-CASEOWN, case owner | Reads the treatment and the timers (Treatment and offer CRU; Case record R) |
| RW-BIANAL, reporting and BI analyst | Reads the treatment data product (Reporting CRUD) |

The approval itself is made at the level set by the delegation of authority (doa.txt, item 2.1.1, levels 1 to 6) before this story runs.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment | all fields | Write |
| DF-TRT-029 | treatment | first_due_date | Write |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Write |
| DF-WRK-042 | timer | treatment_id | Write |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Write |
| DF-CAS-021 | recovery_case | rule_version | Write |
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-296 | rule_row | package_version_id | Read |
| DF-REF-298 | rule_row | outputs | Read |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P7 interface |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the P7 interface, for the approval entry |

Field IDs are those in the Logical Data Model and Data Dictionary. The rule_row fields are read by rule ID and package version through the evaluation result and RuleCatalog; the story reads no drl_source and no workbook.

## 12. Contract

**GET /api/recovery/v1/treatments/{treatmentId}** (S2 endpoint; reads this story's record)

| Item | Value |
|---|---|
| Request | Path `treatmentId` (uuid) |
| Response | 200 `Treatment`: `id`, `caseId`, `decisionLogId`, `treatmentType`, `proposedBy`, `proposedAt`, `offerAmount`, `haircutAmount`, `installments`, `validUntil`, `approvalLevel`, `bookedAt`, `outcome`, `outcomeAt` |
| Errors | 401 (MSG-P4-001); 403 no Treatment and offer R (MSG-P4-002); 404 not found or out of scope (MSG-P4-003); 503 |
| Authorization | Treatment and offer, right R |
| Idempotency | Not applicable |

**GET /api/recovery/v1/cases/{caseId}/timers** (P3) returns `Timer[]`; Case record R. Used to check AC2, AC12 and AC14.

**Rule evaluation.** RuleEvaluator.evaluate("RESTRUCTURE", facts, businessDate) for R-RES-25 and R-RES-27, with the rule ID and the package version written to the decision log. The package is loaded, approved and rolled back through RWB-E1-073 and RWB-E2-042; this story only evaluates it.

**Published interface** (S2 package `recovery.treatment.record.api`; the treatment table belongs to S2 per TSD S2, and this story builds its first version):

```java
public interface TreatmentRecords {
    Treatment recordApproved(RecordTreatmentCommand command);
    Optional<Treatment> find(UUID treatmentId);
    List<TreatmentSnapshot> changedSince(LocalDate businessDate);
}

public record RecordTreatmentCommand(UUID caseId, String treatmentType, String proposedBy,
        Instant proposedAt, BigDecimal offerAmount, BigDecimal haircutAmount, Integer installments,
        LocalDate validUntil, String approvalLevel, UUID decisionLogId, LocalDate firstDueDate,
        UUID idempotencyKey) {}
```

**Published interfaces called** (package recovery.casewf.rules and package recovery.casewf.timers):

```java
RuleResult RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
RuleRow RuleCatalog.row(String ruleId, String packageVersion);
void TimerScheduler.schedule(TimerSpec t);
void TimerScheduler.cancel(UUID timerId);
```

**Events**

| Event | Direction | Payload used |
|---|---|---|
| TreatmentApproved (EV-10) | Published by the treatment service; consumed by the plan timer listener | treatmentId, caseId, terms (firstDueDate, installments) |
| CaseStateChanged (EV-05) | Published | caseId, fromState, toState, ruleId, decisionLogEntryId |
| TimerDue (EV-18) | Published by JOB-05 | timerId, caseId, timerType |
| PaymentMissed (EV-12) | Consumed | treatmentId, dueDate, amountDue |

**Jobs.** JOB-05 Timer check (every 5 minutes) is the Quartz implementation of TimerScheduler and raises TimerDue for INSTALLMENT_DUE timers. JOB-15 Reporting extract (nightly 01:30) adds the DP04 treatment extract; idempotency key is the business date; a rerun replaces that date's extract.

## 13. Solution plan

**Package.** S2 package `recovery.treatment.record` for the treatment record; P3 package `recovery.casewf.plan` for the plan timer listener; P1 package `recovery.data.products.treatment` for the extract step.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TreatmentEntity | Entity | Maps `treatment` with the standard columns and `first_due_date` |
| TreatmentRepository | Repository | Reads and writes `treatment` only |
| TreatmentRecordService | Service | Validates the command, writes the row and the TreatmentApproved outbox row in one transaction |
| TreatmentRecords | Published interface | The interface in section 12 |
| PlanTimerListener | Listener | Consumes TreatmentApproved and PaymentMissed; calls RuleEvaluator; writes the decision log entry, then the timer through TimerScheduler and the route state |
| PlanTimerService | Service | Builds the INSTALLMENT_DUE and CURE_PERIOD TimerSpecs from the due date and the product parameters and schedules them through TimerScheduler |
| PlanTimerFacts | Fact builder | Builds the facts for one case: treatment type, product group, route state, first due date and installments |
| TreatmentExtractStep | Job | Spring Batch step in JOB-15 writing DP04 rows with the derived status |

**Database.** Flyway migration `V<next>__rwb_e2_004_treatment.sql` creates `treatment` as in Recovery Workbench Physical Schema v6 plus `first_due_date date`, with `ix_treatment_case_id` and `ix_treatment_decision_log_id`; adds `timer.treatment_id uuid` with index `ix_timer_treatment_id`. Unique index `ix_timer_plan_due` on `(treatment_id, timer_type, expires_at)` stops a second timer for the same due date.

**Configuration and reference data.** LOV-TIMER value INSTALLMENT_DUE (reference data administrator). CURE_PERIOD_DAYS per product and `plan.warn-days` (center of excellence, RWB-E1-045; values DL22). Package RESTRUCTURE rows R-RES-25 and R-RES-27 (center of excellence, RWB-E2-042). Event consumer retry limit 3 (NFR-026). The package version in force per environment is recorded in `config/rule-packages.lock`; the values in this story are as at 16 November 2026.

**Build steps**

1. Write the migration; prove the table, the new columns and the unique timer index.
2. Build `TreatmentRecordService` with the checks of X1, X2, X3 and X8, the outbox write and the published interface.
3. Build `PlanTimerService` with the due date, warning and cure period calculation through `ProductParameterService`, returning TimerSpecs for TimerScheduler.
4. Build `PlanTimerListener` for TreatmentApproved: idempotency on the event ID, RuleEvaluator evaluation of R-RES-25, decision log first, then TimerScheduler.schedule, the route state and CaseStateChanged.
5. Add the X4 path and the X9 path: no rule match or no package in force sends the case to the exception queue with MSG-P3-005 or MSG-P3-027.
6. Add PaymentMissed handling with R-RES-27 through RuleEvaluator and the cure period timer through TimerScheduler.
7. Build `TreatmentExtractStep` in JOB-15 with the status derivation of BR8.
8. Add the boundary test that refuses a direct write to the timer table outside TimerScheduler.
9. Write the tests in section 16 with a controlled clock.

**Feature flag.** `rwb.p3.plan-timers`. Off: treatments are recorded and no plan timers start.

**Done when.** The tests in section 16 pass, and the SIT run of 50 synthetic plans shows 50 treatment rows, 50 INSTALLMENT_DUE timers and 50 DP04 rows the next morning, with the rule ID and the package version on every plan decision log entry.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-P3-005 | The case is closed, or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-003 | The installment timer is inside its warning period, shown on the case | {timer} ends on {date}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-002 | A role without Treatment and offer R reads a treatment | You cannot {action} here. Your role does not include it. |

For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "RESTRUCTURE" and the business date only, never a case fact.

## 15. Screens and states

No new screen. SCR-14 Treatment record (Epic 2 record view) shows the treatment in state Approved or Booked; SCR-03 Case record shows the INSTALLMENT_DUE and CURE_PERIOD timers with their due dates (RWB-E2-015). A case sent to the exception queue under X4 or X9 shows on SCR-09.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01 | AC1, BR1 | System | Restructure, 36 installments, 850000.00 baht, entry DLE-9001 |
| TC-E2-004-02 | AC2, BR3, BR5, BR10, BR11 | System | First due date 2026-12-31; clock moved past expiry |
| TC-E2-004-03 | AC3, BR8 | System | Ten treatments over three products, two booked |
| TC-E2-004-04 | AC4, BR2 | System | Restructure with no first due date |
| TC-E2-004-05 | AC5, BR1 | System | Unknown decision log entry DLE-0000 |
| TC-E2-004-06 | AC6, BR2 | System | First due date one day before the proposal |
| TC-E2-004-07 | AC7, BR9 | System | Case in route state WITH_FCR_OFFICER |
| TC-E2-004-08 | AC8, BR7 | System | Same TreatmentApproved event twice |
| TC-E2-004-09 | AC9, BR6 | System | Decision log store stopped in the test container |
| TC-E2-004-10 | AC10 | System | JOB-15 forced to fail on 2026-12-02 |
| TC-E2-004-11 | AC11 | System | Closed case |
| TC-E2-004-12 | AC12, BR4, BR10 | System | PaymentMissed for due date 2026-12-31 |
| TC-E2-004-13 | AC13, BR12 | System | No RESTRUCTURE version in force on 2026-12-01 |
| TC-E2-004-14 | AC14, BR11 | System | A component that inserts into the timer table without TimerScheduler |
| TC-E2-004-15 | Access | Access | RW-PHONECOL (no Treatment and offer right) reads `GET /treatments/{treatmentId}`; refused with MSG-P4-002 |
| TC-E2-004-16 | Principle 5 | Resilience | Decision log write forced to fail at timer start; no timer, no state change |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Periods, warning days and the rules are reference rows or package rows; treatment types and outcomes come from LOV-TREATMENT and LOV-TRT-OUTCOME.
- No personal data in logs, tests, workflow history or prompts beyond the IDs in the payload. Amounts are synthetic in tests.
- No read of another module's tables; ACE data only through recovery.v_ace_* views. P3 reaches the treatment only through `TreatmentRecords`; S2 reaches the case only through the P3 case interface; P1 reads treatments only through `changedSince`.
- The decision log entry is written before the timer and the route state; never the other way round.
- Plan timers are scheduled, paused, resumed and cancelled only through TimerScheduler; no class writes the timer table directly.
- The treatment row is never deleted; a cancellation is an outcome.
- The rule package is loaded and approved through RWB-E1-073; this story evaluates it and never reads drl_source or the workbook.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-01, TC-E2-004-04 to TC-E2-004-06, TC-E2-004-11, TC-E2-004-15 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40 | TC-E2-004-02, TC-E2-004-07 to TC-E2-004-09, TC-E2-004-12 to TC-E2-004-14, TC-E2-004-16 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-03, TC-E2-004-10 |

## 19. Out of scope

- The offer builder, treatment screens and submission for approval (S2, Epic 3, FEAT-TRT-01).
- Reading the ACE plan status that calls this interface (RWB-E2-002).
- Booking confirmation from the ALS load and the booked at date (RWB-E2-007).
- Payment matching that raises PaymentMissed (P8, JOB-07).
- Broken plan handling after the cure period (R-RES-29 to R-RES-32, Epic 3).
- Temporal durable timers that replace the Quartz implementation in Epic 3 (ADR-011); the TimerScheduler port is the seam.
- Authoring, approval and rollback of package RESTRUCTURE (RWB-E2-042 and RWB-E1-073).

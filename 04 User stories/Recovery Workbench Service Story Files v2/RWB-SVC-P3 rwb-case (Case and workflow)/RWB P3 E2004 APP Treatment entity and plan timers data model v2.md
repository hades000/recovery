# RWB-P3-E2004-APP Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E2004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P3-E2004-APP-16) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-F |
| Ready to start | After RWB-P3-E1018-APP, RWB-P3-E1045-APP, RWB-P3-E2042-APP |
| Depends on (build) | RWB-P3-E2004-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P3-E1018-APP, RWB-P3-E1045-APP, RWB-P3-E2042-APP, RWB-P3-E1028-CON |
| Contract dependencies | H: RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON; C: RWB-P10-E2032-CON, RWB-P3-E1042-CON, RWB-P3-E1043-CON, the P4 authorise call contract, not yet published (CG-ALL-3990) |
| Contract version | v1: every API path and event in this story is /v1, for example `/api/recovery/treatment/v1/treatments/{treatmentId}` and `rwb.case.CaseStateChanged.v1` |
| Integration dependencies | None |
| External dependencies | RWB-P3-E2004-OPS |
| Integration harness | Repository: Not specified in the source documents (GAP-0389). Environments: Not specified in the source documents (GAP-0389). Gateway-bff composite case-record route path and merge order: Not specified in the source documents (GAP-0389). |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-014, FR-P3-015, FR-P3-016, FR-P3-022, FR-P3-025, FR-P3-033, FR-P3-034) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-004 for rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 34 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the approved plan of a treatment to run on the case inside rwb-case — the installment due date and the cure period shown as plan timers behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, the route state moved to PLAN_RUNNING and then to PLAN_CURE_PERIOD on the rule answer, and each wait held as a durable Temporal timer inside CaseWorkflow — while the treatment record itself (terms, approval, booking, outcome) is written and owned by S2 rwb-treatment and read here only through its contract**, so that **TDR and deed in lieu run inside the Workbench from Epic 2, every plan has a record in its owner and a clock on its case, and a missed installment starts the cure period on the day it is found**.

This story is the case-side half of RWB-E2-004. The treatment entity and its lifecycle are RWB-S2-E2004-APP; the package version and the rule ID are rwb-decision's (RWB-P7-E2004-APP); the DP04 treatment data product is rwb-source-data's; and the durable-timer behaviour is the workflow kit's (RWB-PLT-E1071-CON). What this story builds is the seam that turns an approved treatment into a running plan clock on `rwb_case`, and the two read answers the case record and the timer list are served from.

### 2. Business rationale

Today a restructure plan is agreed in ACE and NLEADS, and nothing in recovery holds its terms or watches its payment dates, so a missed installment is found late. About 3,000 restructure accounts a month reach the restructure process (NFR-005) and deed in lieu is planned at 1,000 cases a month in 2027 (NFR-006). The legacy story created the treatment record with its terms and approval, started the installment timer from the first due date and started the cure period when a payment was missed. It meets REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 and REQ-CWC-011. The measure is unchanged: every approved plan has one treatment row and a running installment timer the day it is recorded.

The realignment moves ownership of the data model and keeps the behaviour. Architecture v5 slide 41 gives S2 rwb-treatment "treatments, contracts, settlement and deed-in-lieu agreements, plan timers", and slide 18 gives S2 the schema `rwb_treatment` with those tables. The same slide gives P3 rwb-case "case, CMMN state, queues, tasks, allocation, timers". The Ownership Map resolves the two statements per table: `treatment` belongs to S2; `timer` stays with P3 as the screen projection behind `GET /cases/{caseId}/timers`, while the clock itself is a durable Temporal timer inside CaseWorkflow, and TimerDue (event 18) and JOB-05 are retired (Architecture v5 slides 42 and 44; ASM-0078); the five-minute next-action scan is a Temporal Schedule in rwb-case, the legacy TimerScheduler and JOB-05 wording is superseded, and neither JOB-05 nor TimerDue is built. The split itself — the treatment moving out of the Epic 2 data model and rwb-case consuming TreatmentApproved, which the event catalogue lists for rwb-comms and rwb-payment, with rwb-case added as a consumer by the catalogue change in GAP-0703 — carries GAP-0703 and ASM-1250. `dp_treatment` belongs to P1 as the dated DP04 copy built from events, because the data lake is removed (DP-17; ADR-018; ASM-0080). rwb_case therefore holds **no treatment table**: the treatment is written once by S2 and announced on `rwb.treatment.events.v1`, and this story consumes that announcement.

Three consequences shape the work. First, the five-minute Quartz check `TimerScheduler` shipped with is gone (DP-10; ADR-016): a plan timer is a durable timer of the workflow kit inside CaseWorkflow on task queue `rwb-case`, so a due date in 2027 survives restarts and releases, and nothing polls the timer table. Second, the rule answer still comes from package RESTRUCTURE, but it is evaluated by the embedded Drools kit inside an activity of the owning service, on the model version rwb-decision has in force, and the answer is written as a local decision record before the state moves (DP-04; DP-03; ADR-017; ADR-022). Third, the treatment data product is a read-only copy that rwb-source-data builds from the treatment events and that the 01:30 extract of business date + 1 loads; the case side reads it and never writes it, and a late or failed load shows as stale rather than as a wrong number (DP-17; ADR-018).

### 3. Preconditions

- RWB-P3-E2004-CON is published: the two consumed event contracts, the timer projection shape behind `GET /api/recovery/case/v1/cases/{caseId}/timers`, the S2 treatment read, the P7 rule and version read, the inbox and outbox envelope, the 2 s budget and the error codes.
- RWB-P3-E1018-APP is done: the case record, its route state, its status and the case ID are in `rwb_case`, and CaseWorkflow is the parent workflow of the case.
- RWB-P3-E1045-APP is done: CURE_PERIOD_DAYS per product and `plan.warn-days` are product parameters in force (values per DL22; `plan.warn-days` assumed 3), read through the parameters contract.
- RWB-P3-E2042-APP is done: the embedded Drools kit, the model cache and the `EvaluateRules` activity are in place, so package RESTRUCTURE version "RES-2026.12" with rows R-RES-25 and R-RES-27 is evaluated locally under the version rwb-decision has in force.
- RWB-P3-E1028-CON is published: the timer resource, its fields, its ordering and the durable-timer projection RWB-P3-E1028-APP writes for the stage clocks, so the plan timers use one timer shape and not a second one.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03).
- RWB-PLT-E1072-CON is published: the embedded Drools kit contract with `RuleResult`, the cache bound and the non-retryable `NoPackageInForce` (DP-04).
- RWB-PLT-E1042-CON and RWB-P3-E1042-CON are published: the parameters contract of rwb-case and its client library (DP-06), so CURE_PERIOD_DAYS and `plan.warn-days` are read as versioned data and never as code.
- RWB-PLT-E1043-CON and RWB-P3-E1043-CON are published: the reference-data contract of rwb-case (DP-07), so LOV-TIMER carries INSTALLMENT_DUE and CURE_PERIOD with their version.
- RWB-PLT-TE006-CON is published: the outbox and inbox library with the CloudEvents 1.0 envelope (DP-09).
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, with the durable timer, the `EvaluateRules` and `RecordAndApply` activities and the retry policy (DP-10).
- RWB-PLT-E1047-CON is published: the naming library (DP-14). RWB-PLT-E1044-CON is published: the per-service Flyway sequence in schema `rwb_case` (DP-15). RWB-PLT-N001-CON is published: the gateway-bff composite route that serves the case record (DP-19).
- A treatment exists in S2 with an approval recorded in a decision log entry, and `rwb.treatment.TreatmentApproved.v1` is consumable with its treatment ID, case ID and terms.
- Feature switch `rwb.p3.plan-timers` is on. Off: a treatment is recorded by S2 and no plan timer starts.
- The caller holds a role with Case record R or Case record CRU in the case's scope, checked through the rwb-access contract.

### 4. Flow

1. rwb-treatment (S2) writes the approved treatment in `rwb_treatment` with its terms, approval level, decision log entry and first due date, in one transaction with its local decision record and its outbox row, and publishes `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` (EV-10) with the treatment ID, the case ID and the terms (RWB-S2-E2004-APP).
2. The case router in rwb-case consumes the event through its inbox, deduplicated on the CloudEvents `id`, and calls `signalWithStart` on CaseWorkflow with workflow ID case-{caseId} (ADR-011; DP-09; Architecture v5 slide 25).
3. CaseWorkflow's plan-timer step reads `recovery_case` for the case: product group, status, route state and rule version.
4. The plan-timer step reads the treatment through `GET /api/recovery/treatment/v1/treatments/{treatmentId}`, one hop with a 2 s timeout, and takes the treatment type, the installments, the offer amount, the approval level, the decision log entry and `first_due_date`; it holds no copy of the row (DP-11; DP-01).
5. The plan-timer step validates what rwb-case needs before it may move: a treatment type, an approval level, a decision log entry, and a first due date for a restructure, and a first due date on or after the proposed date (X1, X3). A closed case is refused (X8).
6. The plan-timer step calls the `EvaluateRules` activity with package "RESTRUCTURE", the plan facts (treatment type, product group, route state, first due date, installments) and the business date. The kit returns `RuleResult` with rule R-RES-25, the package version "RES-2026.12" and the outputs (DP-04).
7. The plan-timer step calls `RecordAndApply`: it writes the local decision record with rule R-RES-25 and version "RES-2026.12" to `rwb.decision-record.v1` through the DP-03 library, and in the same local transaction writes the `timer` projection row of type INSTALLMENT_DUE, `escalated_at` untouched, `treatment_id` = the S2 treatment ID, `expires_at` = 2026-12-31 23:59 Asia/Bangkok, `warn_at` = 2026-12-28 from `plan.warn-days`, status RUNNING; it sets `recovery_case.route_state` = PLAN_RUNNING and `recovery_case.rule_version` = "RES-2026.12"; and it writes the outbox row for `rwb.case.CaseStateChanged.v1` (DP-03; DP-09).
8. CaseWorkflow arms the durable timer for the projection row: the timer waits until `expires_at` inside the workflow on task queue `rwb-case`, and its ID, its expiry and its treatment ID are recorded on the workflow history. No Quartz trigger, no job class and no scheduler factory exists anywhere in the path (DP-10).
9. At `expires_at` the durable timer fires: the expiry produces the timer-due fact on the workflow history with timer type INSTALLMENT_DUE and the treatment ID, and the projection row moves to status EXPIRED. TimerDue (event 18) has no Kafka topic in the target, so no event is published for the expiry itself (Architecture v5 slide 42 row 18).
10. The case status stays IN_PROGRESS. The route state is the only case field the plan moves.
11. rwb-payment's payment matching (JOB-07) finds no payment for the installment and publishes `rwb.payment.PaymentMissed.v1` on `rwb.payment.events.v1` (EV-12) with the treatment ID, the due date and the amount due (P8 rwb-payment).
12. The case router signals CaseWorkflow with the missed payment. The plan-timer step evaluates R-RES-27 on the business date, writes the local decision record with rule R-RES-27 and version "RES-2026.12", then, in the same transaction, writes the CURE_PERIOD `timer` row with `expires_at` = 2027-01-31 from CURE_PERIOD_DAYS of 30 calendar days for "MORTGAGE", `paused` false and status RUNNING, sets the route state to PLAN_CURE_PERIOD and publishes CaseStateChanged.
13. CaseWorkflow arms the durable timer for the cure period; a customer payment that arrives before 2027-01-31 ends the wait early through the same signal path and moves the row to STOPPED (R-RES-28, Epic 3).
14. Readers see the result on the case: `GET /api/recovery/case/v1/cases/{caseId}/timers` returns the plan timers with their type, treatment ID, expiry, warning point and status, and `GET /api/recovery/case/v1/cases/{caseId}` returns route state PLAN_RUNNING or PLAN_CURE_PERIOD and the rule version. Neither read recomputes a date and neither writes (RWB-P3-E2015-APP).
15. rwb-source-data builds the DP04 treatment copy from the treatment events, and the 01:30 extract of JOB-15, owned by rwb-reporting and triggered by the bank Airflow, loads it for the business date (Architecture v5 slide 44; DP-17). This story reads that product through the P1 contract and writes none of it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is missing (type, approval level, decision log entry, first due date for a restructure) | The plan-timer step refuses the move; no timer, no record and no route change are written; the case goes to the exception queue | MSG-GEN-001 | AC4 |
| X2 | The decision log entry does not exist or has no approver | The plan-timer step refuses the move; nothing is written | MSG-GEN-001 | AC5 |
| X3 | The first due date is before the proposed date | The plan-timer step refuses the move; nothing is written | MSG-GEN-003 | AC6 |
| X4 | The case is not in route state BOOKED_IN_ALS_NLEADS when the event arrives | No timer; the case goes to the exception queue with the gap | MSG-P3-005 | AC7 |
| X5 | The same TreatmentApproved event arrives twice | The inbox ignores the second delivery and counts it; one timer and one local decision record only | None | AC8 |
| X6 | The local decision record cannot be written when the timer would start | No timer and no state change; the activity is retried with the kit policy and then the case goes to the exception queue with an incident | MSG-P7-003 | AC9 |
| X7 | The 01:30 extract of the data product fails | The DP04 copy keeps the previous business date and shows it as stale; the case and its timers are unaffected | MSG-P1-001 | AC10 |
| X8 | The case is closed | The move is refused; nothing is written | MSG-P3-005 | AC11 |
| X9 | No RESTRUCTURE version is IN_FORCE on the business date | `NoPackageInForce`; no local decision record, no timer and no route state change; the case goes to the exception queue for a person; the activity is not retried | MSG-P3-027 | AC13 |
| X10 | The S2 treatment read does not answer inside 2 s | The plan-timer step fails the activity with the retry policy of the kit; a breaker per downstream opens; no partial move is written | MSG-GEN-006 | AC2, AC12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Consumes the S2 treatment event and read, the P7 package version, the rwb-case parameters and reference data and the workflow kit; none of them is built here |
| Negotiable | Timer lengths, warning days and the cure period are product parameters and package rows; the story fixes the projection, the route moves and the evaluation order |
| Valuable | Every approved plan has a record in its owner, a due date on its case and a cure period that starts by rule |
| Estimable | One consumed event pair, one projection table's plan columns, one activity, one workflow wait, one rule package evaluated, one data product read |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion is one test against a PostgreSQL test container and a Temporal test environment with a controlled clock, with the S2 and P7 answers stubbed in the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers data model

  Background:
    Given the business date is 2026-12-01
    Given case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"
    Given decision log entry "DLE-9001" records the approval of a restructure at level "L4" by user "U-APR-01"
    Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25 and R-RES-27

  Scenario: AC1 Treatment created (legacy RWB-E2-004 AC1)
    Given the rwb-treatment contract mock returns treatment "T-0401" for case "RW-2026-000201" with type "RESTRUCTURE", 36 installments, offer amount 850000.00, approval level "L4" and decision log entry "DLE-9001"
    Given a TDR plan approved for "RW-2026-000201" with 36 installments, offer amount 850000.00 baht, approval level "L4" and decision log entry "DLE-9001"
    When the record is written
    Then one treatment exists with type "RESTRUCTURE", installments 36, offer amount 850000.00, approval level "L4", decision log entry "DLE-9001" and the case link
    Then booked at is empty until the booking is confirmed
    Then one TreatmentApproved event is in the outbox with the treatment ID and the case ID

  Scenario: AC2 Timer set (legacy RWB-E2-004 AC2)
    Given the rwb-decision contract mock returns rule "R-RES-25" and package version "RES-2026.12"
    Given a plan with the first payment due on 2026-12-31
    When the record is written and the plan timer listener processes TreatmentApproved
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2026-12-01) returns rule R-RES-25 and package version "RES-2026.12"
    Then one decision log entry with rule "R-RES-25" and version "RES-2026.12" is written first
    Then one "INSTALLMENT_DUE" timer exists with expires at 2026-12-31 23:59 Asia/Bangkok, warn at 2026-12-28 and status "RUNNING", scheduled through TimerScheduler
    Then the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"
    Then when the clock passes 2026-12-31 23:59 the durable timer of CaseWorkflow expires and the workflow history records the expiry fact with timer type "INSTALLMENT_DUE" and the treatment ID
    Then the timer status is "EXPIRED"

  Scenario: AC3 Data product (legacy RWB-E2-004 AC3)
    Given the rwb-treatment contract mock returns ten treatments recorded on 2026-12-01 across "MORTGAGE", "HIRE_PURCHASE" and "SSME"
    Given ten treatments recorded on 2026-12-01 across "MORTGAGE", "HIRE_PURCHASE" and "SSME"
    Given two of them have a booked at date
    When the reporting extract runs at 01:30 on 2026-12-02
    Then the treatment data product holds ten rows for business date 2026-12-01
    Then eight show status "APPROVED" and two show status "BOOKED"

  Scenario: AC4 Required field missing (legacy RWB-E2-004 AC4)
    Given the rwb-treatment contract mock returns a restructure plan for "RW-2026-000201" with no first due date
    Given a restructure plan for "RW-2026-000201" with no first due date
    When the record is written
    Then the system refuses it with MSG-GEN-001 naming "first due date"
    Then no treatment and no event are written

  Scenario: AC5 Approval not in the decision log (legacy RWB-E2-004 AC5)
    Given the rwb-decision contract mock returns no decision log entry for "DLE-0000"
    Given a plan that names decision log entry "DLE-0000" which does not exist
    When the record is written
    Then the system refuses it with MSG-GEN-001 naming "decision log entry"

  Scenario: AC6 First due date before the proposal (legacy RWB-E2-004 AC6)
    Given the rwb-treatment contract mock returns a plan proposed on 2026-12-01 with the first due date 2026-11-30
    Given a plan proposed on 2026-12-01 with the first due date 2026-11-30
    When the record is written
    Then the system refuses it with MSG-GEN-003 naming "first due date" and "proposed at"

  Scenario: AC7 Case not in the booked state (legacy RWB-E2-004 AC7)
    Given the rwb-treatment contract mock returns treatment "T-0402" for case "RW-2026-000202" with first due date 2026-12-31
    Given case "RW-2026-000202" in route state "WITH_FCR_OFFICER"
    When a TreatmentApproved event with a first due date arrives for it
    Then the system writes no timer
    Then the system places the case in the exception queue with MSG-P3-005 naming "PLAN_RUNNING" and "WITH_FCR_OFFICER"

  Scenario: AC8 Event delivered twice (legacy RWB-E2-004 AC8)
    Given the TreatmentApproved event for the AC1 treatment was processed
    When the same event with the same event ID arrives again
    Then no second timer and no second decision log entry are written
    Then the system counts the repeat as an idempotency hit

  Scenario: AC9 Decision log write fails (legacy RWB-E2-004 AC9)
    Given the rwb-decision contract mock does not answer within 2 seconds for the decision record of "RW-2026-000201"
    Given the decision log store is unavailable
    When the plan timer listener processes TreatmentApproved for "RW-2026-000201"
    Then the system writes no timer and the route state stays "BOOKED_IN_ALS_NLEADS"
    Then the system retries the event 3 times and then placed in the exception queue with an incident and MSG-P7-003

  Scenario: AC10 Extract fails (legacy RWB-E2-004 AC10)
    Given the rwb-treatment contract mock returns the treatments of business date 2026-12-01
    Given the reporting extract of 2026-12-02 fails
    When a reporting and BI analyst reads the treatment data product
    Then it shows business date 2026-12-01 with MSG-P1-001

  Scenario: AC11 Case closed (legacy RWB-E2-004 AC11)
    Given the rwb-treatment contract mock returns a plan for closed case "RW-2026-000203"
    Given case "RW-2026-000203" with status "CLOSED"
    When a plan is recorded for it
    Then the system refuses it with MSG-P3-005

  Scenario: AC12 Payment missed starts the cure period (legacy RWB-E2-004 AC12)
    Given the rwb-decision contract mock returns rule "R-RES-27" and package version "RES-2026.12"
    Given the AC2 timer expired on 2026-12-31
    When a PaymentMissed event arrives for the treatment with due date 2026-12-31 on business date 2027-01-01
    Then RuleEvaluator.evaluate("RESTRUCTURE", facts, 2027-01-01) returns rule R-RES-27 and package version "RES-2026.12"
    Then the system writes a decision log entry with rule "R-RES-27" and version "RES-2026.12" first
    Then one "CURE_PERIOD" timer exists with expires at 2027-01-31, scheduled through TimerScheduler
    Then the case route state is "PLAN_CURE_PERIOD"

  Scenario: AC13 No RESTRUCTURE version in force (legacy RWB-E2-004 AC13)
    Given the rwb-decision contract mock returns NoPackageInForce for package "RESTRUCTURE" on 2026-12-01
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-01
    When the plan timer listener processes TreatmentApproved for "RW-2026-000201"
    Then NoPackageInForce is thrown with MSG-P3-027 for package "RESTRUCTURE"
    Then no decision log entry, no timer and no route state change are written
    Then the case goes to the exception queue for role "RW-TEAMMGR" with the gap

  Scenario: AC14 Plan timers go only through TimerScheduler (legacy RWB-E2-004 AC14)
    Given the rwb-treatment contract mock returns treatment "T-0401" for case "RW-2026-000201"
    Given the plan timer listener holds an "INSTALLMENT_DUE" TimerSpec for case "RW-2026-000201"
    When the listener schedules the timer
    Then the timer is created by TimerScheduler and carries the case ID, the treatment ID, the timer type and the expiry
    Then a component that inserts into the timer table without TimerScheduler fails the boundary test and the build
    Then the durable timer of CaseWorkflow is the only mechanism that expires the timer

  Scenario: AC15 Timer projection holds the treatment as a value (new, D-RCV-60)
    Given the plan timer listener holds an "INSTALLMENT_DUE" TimerSpec for case "RW-2026-000201" with treatment ID "T-0401"
    When the listener writes the timer projection row
    Then rwb_case.timer holds treatment_id as a uuid value with no foreign key and no join into rwb_treatment
    Then the case reads its plan timers from the timer projection only

  Scenario: AC16 Error answers of the provided operations (new, D-RCV-60)
    Given user with no Treatment and offer right (role code Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC16))
    When the user reads a treatment through the rwb-treatment provided operation
    Then the operation answers 403 and the system refuses it with MSG-P4-002
    Given a treatment ID that does not exist
    When the operation reads that treatment ID
    Then the operation answers 404

  Scenario: AC17 Activity retry and timeout (new, D-RCV-60)
    Given the rwb-decision contract mock does not answer within the timeout not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC17) for the decision record of "RW-2026-000201"
    When the EvaluateRules activity calls the decision record
    Then the activity times out after the timeout not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC17) and its retry count is Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC17)
    Then the retry ends with the case in the exception queue with its message ID not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC17)
    Given no RESTRUCTURE version is in force (MSG-P3-027)
    When the EvaluateRules activity runs
    Then the retry behaviour is Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC17)

  Scenario: AC18 Status change the model does not allow is refused (no legacy criterion) (new, D-RCV-60)
    Given case "RW-2026-000201" with status "IN_PROGRESS"
    When a status change that the model does not allow is requested for the case
    Then the system refuses the status change with a message not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC18)
    Then the case status stays "IN_PROGRESS"
```

**Note on the target reading of these fourteen criteria.** The legacy wording is kept word for word. In the target the names in it mean the following, and nothing else changes: the treatment record of AC1, AC4, AC5, AC6 and AC11 is written, validated and owned by **S2 rwb-treatment** (`rwb_treatment.treatment`), so those criteria are exercised here through the rwb-treatment contract mock and the `rwb.treatment.TreatmentApproved.v1` event rwb-case consumes; `TimerScheduler` in AC2, AC12 and AC14 is the workflow kit's durable timer, armed inside **CaseWorkflow** on task queue `rwb-case`, and the projection row is written by the plan-timer step of that workflow — no Quartz job, no `TimerScheduler` implementation and no JOB-05 exists (DP-10; Architecture v5 slide 44; ASM-0078); the `TimerDue` event of AC2 is the timer-due fact on the workflow history, because event 18 has no topic in the target (Architecture v5 slide 42 row 18); `RuleEvaluator` in AC2, AC12 and AC13 is the embedded Drools kit called from the `EvaluateRules` activity, on the version rwb-decision has in force (DP-04; ADR-017); and the treatment data product of AC3 and AC10 is the DP04 copy owned by **P1 rwb-source-data** and built from events with no data lake, read here through the P1 contract (DP-17; ADR-018; ASM-0080). The `given the rwb-… contract mock returns …` lines are the stubs that stand in for those two owners; every legacy value — 36 installments, 850000.00, "L4", "DLE-9001", R-RES-25, R-RES-27, "RES-2026.12", 2026-12-31 23:59, 2026-12-28, 2027-01-31, 30 calendar days — is unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every offer approved for a customer has one treatment row with its type, terms, approval level, the approval's decision log entry and its outcome, and that row is S2 rwb-treatment's | REQ-CHO-006; LOV-TREATMENT; Ownership Map `treatment` |
| BR2 | A restructure needs installments above 0 and a first due date on or after the proposed date | R-RES-25 (condition first_due_date set) |
| BR3 | The plan timers start when the schedule is set on a booked plan, and the case moves to PLAN_RUNNING | R-RES-25 |
| BR4 | When a due date passes with no payment matched, the cure period starts with CURE_PERIOD_DAYS from the parameters in force | R-RES-27; RWB-P3-E1045-APP |
| BR5 | The warning is raised `plan.warn-days` before the due date (assumed 3; DL22) | REQ-CWC-011 |
| BR6 | A decision that cannot be written to the decision log does not proceed: the local decision record is written before the timer and the route state, never after | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR7 | A repeated event with the same CloudEvents id is ignored and counted through the inbox; one timer and one record result | R-UNI-40; DP-09 |
| BR8 | The treatment data product carries one row per treatment with its status: APPROVED (no booked at), BOOKED, RUNNING, BROKEN, COMPLETED, CANCELED (from outcome), and it is P1's read-only copy built from events | REQ-RDF-014; LOV-TRT-OUTCOME; DP-17 |
| BR9 | A plan whose case is not in the state the rule expects goes to the exception queue for a person | R-RES-35 pattern; R-UNI-41 |
| BR10 | R-RES-25 and R-RES-27 are rows of package RESTRUCTURE, evaluated by the embedded Drools kit; the result names the rule and the package version, and the action text, owner role and timer spec come from the rule catalogue of rwb-decision | D-RCV-36 T5, T6, T7; DP-04; ADR-017 |
| BR11 | A plan timer exists only as a durable timer of the workflow kit inside CaseWorkflow plus its projection row in `rwb_case.timer`; TimerScheduler, its Quartz implementation JOB-05 and the five-minute timer check are retired | DP-10; ADR-016; Architecture v5 slide 44 |
| BR12 | No RESTRUCTURE version in force is a refusal (`NoPackageInForce`), never a default timer or a default move, and the refusal is not retried | R-UNI-41; D-RCV-36 T7 |
| BR13 | The timer projection is what the case reads; `treatment_id` is an S2 identifier carried as a value, and `rwb_case` holds no foreign key and no join into `rwb_treatment` | DP-01; ADR-014; Ownership Map `timer` ruling |
| BR14 | Only rwb-case writes `rwb_case.timer`, `rwb_case.recovery_case.route_state` and `rwb_case.recovery_case.rule_version`; no other service writes them and this service writes no other schema | DP-01; Architecture v5 slide 29 |
| BR15 | A late or failed 01:30 load of the treatment data product shows as stale with its business date and never as a fresh number | REQ-RDF-014; DP-17; MSG-P1-001 |

BR1 to BR12 are the legacy rules of RWB-E2-004 carried forward with the ownership and mechanism the target fixes in BR11; BR13 to BR15 are the realignment rules this story implements.

### 9. State transitions

The case status does not change (it stays IN_PROGRESS). The route state changes:

| From | Event | Condition | To |
|---|---|---|---|
| BOOKED_IN_ALS_NLEADS | SCHEDULE_SET | first_due_date set (R-RES-25) | PLAN_RUNNING |
| PLAN_RUNNING | PAYMENT_MISSED | due date passed and no payment matched (R-RES-27) | PLAN_CURE_PERIOD |

Timer status: RUNNING to EXPIRED when the INSTALLMENT_DUE durable timer of CaseWorkflow reaches `expires_at`; RUNNING to STOPPED when a payment ends the cure-period wait early (Epic 3, R-RES-28). Both changes are applied by the workflow to the projection row in `rwb_case.timer`; nothing else expires or stops a plan timer.

| Observed fact | Written by | Where it is observed |
|---|---|---|
| `timer` row INSTALLMENT_DUE, `expires_at` 2026-12-31 23:59 Asia/Bangkok, `warn_at` 2026-12-28, RUNNING | The plan-timer step of CaseWorkflow in one transaction with the local decision record and the route state | `GET /api/recovery/case/v1/cases/{caseId}/timers` |
| `timer` row CURE_PERIOD, `expires_at` 2027-01-31, RUNNING | The same step after R-RES-27 | `GET /api/recovery/case/v1/cases/{caseId}/timers` |
| Route state PLAN_RUNNING then PLAN_CURE_PERIOD, `rule_version` "RES-2026.12" | The same step | `GET /api/recovery/case/v1/cases/{caseId}` |
| Treatment row with its terms, level and entry | S2 rwb-treatment, not this story | `GET /api/recovery/treatment/v1/treatments/{treatmentId}` |
| DP04 treatment row with its derived status | P1 rwb-source-data from the treatment events, through the 01:30 extract | `GET /api/recovery/source-data/v1/data-products/DP04/records` |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow identity | Runs the plan-timer step of CaseWorkflow: evaluates the rules, writes the local decision record, the timer projection, the route state and the outbox row, and arms the durable timer (Case record CRU; Treatment and offer R through the S2 contract) |
| SY-RULES, embedded Drools kit | Evaluates R-RES-25 and R-RES-27 in package RESTRUCTURE inside the `EvaluateRules` activity and returns the rule ID, the package version and the outputs |
| rwb-treatment (S2) | Owns and writes the treatment and publishes TreatmentApproved; this story reads it and never writes it |
| rwb-payment (P8) | Publishes PaymentMissed when no payment matched the installment |
| rwb-decision (P7) | Owns the package versions in force and the central decision ledger; this story reads the version and the rule row and publishes its local record |
| RW-RESTRUCT, restructuring officer | Reads the treatment, the plan timers and the route state (Treatment and offer CRUA; Case record R) |
| RW-CASEOWN, case owner | Reads the treatment and the timers (Treatment and offer CRU; Case record R) |
| RW-BIANAL, reporting and BI analyst | Reads the treatment data product through the P1 contract (Reporting CRUD) |
| RW-TEAMMGR, team manager | Receives the exception-queue entry of an X4 or X9 refusal |

The approval itself is made at the level set by the delegation of authority (levels 1 to 6) before this story runs, and its decision log entry is P7's.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment | all fields | Read, through the S2 contract; written by S2, never here |
| DF-TRT-029 | treatment | first_due_date | Read, through the S2 contract |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Write |
| DF-WRK-042 | timer | treatment_id | Write (the S2 identifier as a value; no foreign key) |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-007 | recovery_case | route_state | Write |
| DF-CAS-021 | recovery_case | rule_version | Write |
| DF-REF-002 | rule_row | rule_id | Read, through the P7 contract and the evaluation result |
| DF-REF-003 | rule_row | rule_version | Read, through the P7 contract and the evaluation result |
| DF-REF-296 | rule_row | package_version_id | Read, through the P7 contract |
| DF-REF-298 | rule_row | outputs | Read, through the P7 contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write through the DP-03 local record; the approval entry is read through the P7 contract |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read, through the P7 contract, for entry "DLE-9001" |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | CURE_PERIOD_DAYS and `plan.warn-days` in force | Read, through the parameters contract |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-TIMER values INSTALLMENT_DUE and CURE_PERIOD | Read, through the reference-data contract |
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields, including the treatment link and the derived status | Read, through the P1 data-product contract; never written here |

Field IDs are those in the Logical Data Model and Data Dictionary. The rule row fields are read by rule ID and package version through the evaluation result and the rule catalogue; this story reads no `drl_source` and no workbook. `rwb_case` holds no treatment column, no treatment table and no key into `rwb_treatment`.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3). The story adds plan-timer content to two operations that already exist in the Ownership Map; it declares no new path.

| Method | Path | Purpose | Added in this story | Access |
|---|---|---|---|---|
| GET | `/cases/{caseId}/timers` | Read the clocks on a case | The plan timers of the case: `timerType` INSTALLMENT_DUE and CURE_PERIOD with `treatmentId`, `expiresAt` 2026-12-31 23:59 Asia/Bangkok, `warnAt` 2026-12-28, `status` and `paused`, beside the stage and service-level timers of RWB-P3-E2015-APP | Case record R, scope applied |
| GET | `/cases/{caseId}` | Read one case | `routeState` PLAN_RUNNING and PLAN_CURE_PERIOD and `ruleVersion` "RES-2026.12" on the Case resource, with the status unchanged | Case record R, scope applied |

Both operations answer 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 unknown or out of scope (MSG-P4-003) and 503 store down. A read takes no Idempotency-Key.

#### 12.2 REST operations consumed

| Method | Path | Owner | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment record: type, terms, installments, offer amount, approval level, decision log entry, `firstDueDate` and booked at | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The approval entry "DLE-9001" and its approver, before the first move (X2, AC5) | One hop, 2 s (DP-11) |
| GET | `/api/recovery/decision/v1/rule-catalog/{ruleId}?packageVersion=` | P7 rwb-decision | The action text, owner role and timer spec of R-RES-25 and R-RES-27 for the version in force | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/data-products/DP04/records` | P1 rwb-source-data | The DP04 treatment rows of a business date and their staleness (AC3, AC10; the read path and the freshness element carry GAP-0704) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and Case record right check, cached per request | One hop, 2 s (DP-11) |

Five calls, no chain: rwb-case calls each owner once and returns. The treatment read is made by the plan-timer step and by the case record answer; the decision log and catalogue reads are made by the plan-timer step. The rule evaluation itself is not a REST call: it runs in the embedded Drools kit inside the `EvaluateRules` activity of rwb-case on the model version fetched by RWB-P3-E2042-APP.

#### 12.3 Events published

| Event | Topic | Payload | Key |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | caseId, fromState BOOKED_IN_ALS_NLEADS or PLAN_RUNNING, toState PLAN_RUNNING or PLAN_CURE_PERIOD, ruleId | caseId |

CloudEvents 1.0, written to the outbox in the same transaction as the projection row and the route state, and relayed by the outbox relay (DP-09; DP-14). The event carries IDs, codes, dates and amounts only. No event is published for the timer expiry: TimerDue (event 18) is retired and the expiry stays a fact of the workflow history.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract element |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (event 10) | `rwb.treatment.events.v1` | S2 rwb-treatment | CloudEvents 1.0, key caseId; treatmentId, caseId, treatmentType, approvalLevel, decisionLogId, firstDueDate, installments, offerAmount; inbox dedupe on `id`; starts the plan-timer step (AC1, AC2, AC7, AC8) |
| `rwb.payment.PaymentMissed.v1` (event 12) | `rwb.payment.events.v1` | P8 rwb-payment | CloudEvents 1.0, key caseId; treatmentId, dueDate 2026-12-31, amountDue, businessDate 2027-01-01; inbox dedupe; starts the cure-period step (AC12) |

Both are consumed by the case router, which turns them into signals on CaseWorkflow (Architecture v5 slide 25). `rwb.decision.RulePackageInForce.v1` (event 30) is consumed by RWB-P3-E2042-APP into the model cache, not by this story.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow, parent, one per case, workflow ID = case-{caseId} | `rwb-case` | Holds the plan-timer step, the INSTALLMENT_DUE and CURE_PERIOD durable timers, the expiry fact and the route moves; Continue-As-New at every stage end and at least every 28 days |
| PlanTimerStep | Activity | `rwb-case` | Input: caseId, treatmentId, businessDate. Reads the case, the treatment and the parameters; evaluates the package; writes the local decision record, the projection row, the route state and the outbox row; returns the timer ID and the expiry it armed |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | Input: packageCode "RESTRUCTURE", facts, businessDate. Output: `RuleResult(packageCode, packageVersion, ruleId, outputs)`; raises `NoPackageInForce`, non-retryable (DP-04) |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Input: the decision record, the timer row, the route state and the outbox rows; one local transaction, no partial write (DP-03) |

The durable timer is the workflow's own wait between step 8 and step 9 and step 13; no Schedule, no cron and no polling job is registered.

#### 12.6 Schedules

None. JOB-05 Timer check and its five-minute Quartz trigger are retired (DP-10; Architecture v5 slide 44; ASM-0078), and this story registers no Schedule, no cron entry and no job name. The 01:30 extract JOB-15 that loads the DP04 copy is P9 rwb-reporting's, triggered by the bank Airflow (Architecture v5 slide 44); it is read here through the P1 contract and never started, paused or changed by rwb-case.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| timer | P3 (rwb_case) | The plan projection row: `timer_type` INSTALLMENT_DUE or CURE_PERIOD, `started_at`, `expires_at`, `warn_at`, `paused`, `status`, `escalation_level` and `treatment_id` |
| recovery_case | P3 (rwb_case) | `route_state` and `rule_version` of the plan move; status read only |
| task | P3 (rwb_case) | Read for the owner role of the next step the plan timer carries, where a task exists |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | The outbox row of CaseStateChanged, the inbox dedupe of the two consumed events and the idempotency key of the step (DP-09) |

`treatment` is S2's in `rwb_treatment` and `dp_treatment` is P1's in `rwb_source_data`; neither is read directly, neither is joined and neither has a foreign key from `rwb_case` (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-treatment WireMock | The S2 contract | `GET /treatments/{treatmentId}` for "T-0401" (RESTRUCTURE, 36 installments, 850000.00, "L4", "DLE-9001", booked at empty), "T-0402" on RW-2026-000202, the plan with no first due date, the plan of 2026-11-30 and the closed case; and `rwb.treatment.TreatmentApproved.v1` for these treatments |
| rwb-decision WireMock | The P7 contract | `GET /decision-log/{entryId}` with "DLE-9001" and "U-APR-01" and a 404 for "DLE-0000"; `GET /rule-catalog/{ruleId}?packageVersion=` for R-RES-25 and R-RES-27 at "RES-2026.12"; the no-version answer of X9; a delayed answer beyond 2 s |
| rwb-payment WireMock | The P8 event and REST contracts | `rwb.payment.PaymentMissed.v1` for due date 2026-12-31 on business date 2027-01-01, and its absence before the due date |
| rwb-source-data WireMock | The P1 contract | `GET /data-products/DP04/records` with ten rows for 2026-12-01 (eight APPROVED, two BOOKED) and the stale answer with MSG-P1-001 |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R and refusing a role without it and a case out of scope |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | Case and timers provided; treatment, decision log, rule catalogue, DP04 records and authorise consumed; one hop, 2 s timeout, breaker per downstream |
| Kafka | 1 published, 2 consumed | CaseStateChanged published on `rwb.case.events.v1`; TreatmentApproved and PaymentMissed consumed with inbox dedupe |
| Temporal | 1 workflow, 3 activities, no Schedule | CaseWorkflow with the plan-timer step, the EvaluateRules and RecordAndApply activities of the kit, and the durable INSTALLMENT_DUE and CURE_PERIOD timers |
| File | None | No file is read or written |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.case.plantimer`, module `plantimer`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.case.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 adds nothing here: this story reads no ACE view, because the ACE plan status reaches the case through RWB-P3-E2002-APP and the treatment through the S2 contract. The same-service CON baselines RWB-P3-E2004-CON and RWB-P3-E1028-CON are class H dependencies and are not DP rows.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PlanTimerListener | Listener | Consumes TreatmentApproved and PaymentMissed through the inbox, dedupes on the CloudEvents id and signals CaseWorkflow |
| PlanTimerStep | Activity | Reads the case, the treatment and the parameters; validates the move; calls EvaluateRules; writes the record, the projection, the route state and the outbox row; returns the expiry it armed |
| PlanTimerService | Service | Builds the timer projection from `first_due_date`, `plan.warn-days` and CURE_PERIOD_DAYS: `expires_at` at 23:59 Asia/Bangkok, `warn_at`, the cure-period end date and the timer type from LOV-TIMER |
| PlanTimerPolicy | Domain | The X1, X3 and X8 validations and the X4 route-state check, with their message IDs |
| TimerProjectionWriter | Repository | Writes and updates the `timer` rows of the case in schema `rwb_case`; no other table and no foreign key |
| CaseRouteWriter | Repository | Writes `recovery_case.route_state` and `rule_version` and the CaseStateChanged outbox row in the same transaction |
| TreatmentClient | Client | Calls the S2 treatment read with the 2 s timeout and the breaker; never reads `rwb_treatment`, which S2 owns |
| ApprovalClient | Client | Calls the P7 decision log for the approval entry, once, with the 2 s timeout |
| RuleCatalogClient | Client | Reads the R-RES-25 and R-RES-27 catalogue rows for the version in force |
| DataProductClient | Client | Reads the DP04 treatment rows and their staleness through the P1 contract for AC3 and AC10 |

**Database.** One Flyway step in schema `rwb_case` for the plan projection: `timer.treatment_id uuid` (DF-WRK-042) with `ix_timer_treatment_id`, and the unique index `ix_timer_plan_due` on `(treatment_id, timer_type, expires_at)` so a second timer for the same due date cannot exist (DP-15). The LOV-TIMER values INSTALLMENT_DUE and CURE_PERIOD already exist in the reference data of RWB-P3-E1043-CON and no value row is added here. No treatment column, no treatment table and no key into another schema is created.

**Configuration and reference data.** CURE_PERIOD_DAYS per product and `plan.warn-days` are read through the parameters contract with their version (RWB-P3-E1045-APP; values per DL22, which is open, with assumptions ASM-1162, ASM-1304, ASM-2217 and ASM-2569; `plan.warn-days` assumed 3). LOV-TIMER and LOV-TIMER-STATUS are read through the reference-data contract. Package RESTRUCTURE rows R-RES-25 and R-RES-27 are authored and approved by RWB-P3-E2042-APP and RWB-P7-E2042-APP; this story evaluates them and never edits them. Consumer retry is the kit policy (1 s initial interval, back-off 2, 10 attempts) and the legacy consumer retry limit is 3 attempts before the exception queue (NFR-026). Feature switch `rwb.p3.plan-timers`, a service configuration value: off, a treatment is recorded by S2 and no plan timer starts.

**Build steps**

1. Add the migration for `timer.treatment_id` and the unique plan-due index; prove the projection, the index and the absence of any treatment object in `rwb_case`.
2. Build PlanTimerListener with the inbox dedupe on `id`, the signalWithStart to CaseWorkflow and the two event payloads of §12.4; tests for AC8.
3. Build TreatmentClient, ApprovalClient and RuleCatalogClient with the 2 s timeout, the GET retry with jitter and the breaker; tests for the X10 and X2 paths.
4. Build PlanTimerStep: the reads, the X1, X3 and X4 validations, the EvaluateRules call, and the ordered write of the local decision record, the projection row, the route state and the outbox row; tests for AC2, AC4, AC5, AC6, AC7 and AC11.
5. Build the durable timer arming in CaseWorkflow and the expiry handling that moves the projection to EXPIRED and records the timer-due fact; tests for AC2 with a controlled clock and a worker restart.
6. Add the X9 path: `NoPackageInForce` is non-retryable, writes nothing, publishes nothing and puts the case in the exception queue for RW-TEAMMGR; test for AC13.
7. Add the PaymentMissed path with R-RES-27 and the CURE_PERIOD projection computed from CURE_PERIOD_DAYS; tests for AC12.
8. Add the boundary test that fails the build on any insert into `timer` outside PlanTimerStep, any read of `rwb_treatment` (owned by S2) and any Quartz, JOB-05 or `TimerScheduler` symbol in the module; test for AC14.
9. Add the DP04 read through the P1 contract and the stale answer of MSG-P1-001; tests for AC3 and AC10.
10. Extend the two read answers with the plan fields and contract-test them against RWB-P3-E2004-CON; browser test of the case record with a plan.

**Done when.** The twenty-two tests of §16 pass in SIT on the contract fakes for S2, P7, P8, P1 and P4; a synthetic run of 50 plans produces 50 treatment rows in `rwb_treatment` (S2), 50 INSTALLMENT_DUE projection rows in `rwb_case.timer`, 50 CURE_PERIOD rows after a missed installment at the moved clock, 50 DP04 rows of the next business date and 50 local decision records naming R-RES-25 or R-RES-27 with version "RES-2026.12"; a worker restart in the middle of a 2027 due date leaves the timer on time; and the contract tests of RWB-P3-E2004-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-GEN-006 | A consumed call does not answer in time | {system} is not available. Your request is queued and will be retried. |
| MSG-P3-005 | The case is closed, or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-003 | The installment timer is inside its warning period, shown on the case | {timer} ends on {date}. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The {table} load was refused: {check}. The version in force is unchanged. |
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A role without the right calls an operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |

For MSG-P3-027 the {check} value is "no package in force" and {table} names the package code "RESTRUCTURE" only, never a case fact. For MSG-GEN-006 the {system} value names the owner that failed ("Treatment and offer" on the S2 read, "Decision center" on the P7 read). MSG-P3-003 is raised where the timer is written, from `warn_at`, and is shown by RWB-P3-E2015-APP; this story never re-computes it in a screen.

### 15. Screens and states

No new screen. SCR-14 Treatment record (Epic 2 record view, S2) shows the treatment in state Approved or Booked. SCR-03 Case record shows the INSTALLMENT_DUE and CURE_PERIOD timers with their due date, warning point and status (RWB-P3-E2015-APP renders them). A case sent to the exception queue under X1, X2, X4, X8 or X9 shows on SCR-09. The plan timers are read only: no screen of this story writes a timer, a route state or a treatment.

| Screen | State | What the user does |
|---|---|---|
| SCR-03 Case record | Read only | Reads the plan timers of the case and the route state PLAN_RUNNING or PLAN_CURE_PERIOD |
| SCR-03 Case record | Degraded | Reads the timers and the case while the DP04 section carries MSG-P1-001; the plan timers are unaffected |
| SCR-03 Case record | Empty | Not specified in the source documents (CG-ALL-4002) |
| SCR-03 Case record | Loading | Not specified in the source documents (CG-ALL-4002) |
| SCR-03 Case record | Error | Not specified in the source documents (CG-ALL-4002) |
| SCR-03 Case record | No access | Not specified in the source documents (CG-ALL-4002) |
| SCR-09 Exception queue | To handle | Picks up a case refused under X1, X2, X4, X8 or X9 with its message ID and its gap |
| SCR-09 Exception queue | Empty | Not specified in the source documents (CG-ALL-4003) |
| SCR-09 Exception queue | Loading | Not specified in the source documents (CG-ALL-4003) |
| SCR-09 Exception queue | Error | Not specified in the source documents (CG-ALL-4003) |
| SCR-09 Exception queue | No access | Not specified in the source documents (CG-ALL-4003) |
| SCR-14 Treatment record | Approved or Booked | Reads the treatment, read only |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-4004) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-4004) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-4004) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-4004) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01 | AC1, BR1 | End to end | Restructure, 36 installments, 850000.00 baht, entry DLE-9001, read through the S2 fake |
| TC-E2-004-02 | AC2, BR3, BR5, BR10, BR11 | End to end | First due date 2026-12-31; the durable timer's clock moved past expiry |
| TC-E2-004-03 | AC3, BR8, BR15 | End to end | Ten treatments over three products, two booked, read through the P1 DP04 fake |
| TC-E2-004-04 | AC4, BR2 | End to end | Restructure with no first due date |
| TC-E2-004-05 | AC5, BR1 | End to end | Unknown decision log entry DLE-0000 |
| TC-E2-004-06 | AC6, BR2 | End to end | First due date one day before the proposal |
| TC-E2-004-07 | AC7, BR9 | End to end | Case in route state WITH_FCR_OFFICER |
| TC-E2-004-08 | AC8, BR7 | End to end | Same TreatmentApproved event twice, same CloudEvents id |
| TC-E2-004-09 | AC9, BR6 | End to end | Decision record store stopped in the test container |
| TC-E2-004-10 | AC10 | End to end | JOB-15 forced to fail on 2026-12-02; the DP04 fake answers stale |
| TC-E2-004-11 | AC11 | End to end | Closed case |
| TC-E2-004-12 | AC12, BR4, BR10 | End to end | PaymentMissed for due date 2026-12-31 on business date 2027-01-01 |
| TC-E2-004-13 | AC13, BR12 | End to end | No RESTRUCTURE version in force on 2026-12-01 |
| TC-E2-004-14 | AC14, BR11 | Component | A component that inserts into the timer table outside PlanTimerStep; a Quartz or JOB-05 symbol in the module |
| TC-E2-004-15 | Access, BR14 | Component | RW-PHONECOL (no Treatment and offer right) reads the treatment through the S2 fake; refused with MSG-P4-002 |
| TC-E2-004-16 | Principle 5, BR6 | NFR | Decision record write forced to fail at timer start; no timer, no state change, no event; the retry is bounded and the case goes to the exception queue |
| TC-E2-004-17 | §12 operations, events and activities, BR14 | Component | Contract test of every operation, event and activity of section 12 against RWB-P3-E2004-CON with the contract fakes |
| TC-E2-004-18 | §12.7 tables, ASM-3438, BR13, BR14 | Component | Boundary test: after migration each table of section 12.7 sits in its owner's schema, `rwb_case` holds no foreign key or join to `rwb_treatment`, and `treatment_id` is a uuid value |
| TC-E2-004-19 | AC15, BR13 | Component | Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC15) |
| TC-E2-004-20 | AC16 | Component | Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC16) |
| TC-E2-004-21 | AC17, BR12 | NFR | Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC17) |
| TC-E2-004-22 | AC18 | Component | Not specified in the source documents (NEWAC-RWB-P3-E2004-APP-AC18) |

The legacy levels map System to End to end, Access to Component and Resilience to NFR. The sixteen legacy IDs are kept unchanged, in this order, with the level of each stated here; TC-E2-004-17 to TC-E2-004-22 are added by the realignment.

### 17. Guardrails

- No business value in code. Periods, warning days and the rules are parameter rows or package rows; treatment types and outcomes come from LOV-TREATMENT and LOV-TRT-OUTCOME, and the timer types from LOV-TIMER.
- No personal data in logs, tests, workflow history, events or prompts beyond the IDs in the payload. Amounts are synthetic in tests.
- No read of another service's tables. The treatment is reached only through the S2 contract, the approval and the rule only through the P7 contract, and the DP04 copy only through the P1 contract (DP-01, DP-11).
- `rwb_case` holds no treatment row, no treatment column and no foreign key into `rwb_treatment`; the timer's `treatment_id` is a value, not a key.
- The local decision record is written before the timer and the route state; never the other way round (BR6).
- A plan timer exists only through the plan-timer step of CaseWorkflow; no class writes `rwb_case.timer` directly and no Quartz, JOB-05 or `TimerScheduler` symbol exists in the module (BR11).
- The treatment row is never deleted and never copied; a cancellation is an outcome in its owner.
- The rule package is authored, approved and rolled back through RWB-P3-E2042-APP and rwb-decision; this story evaluates it and never reads `drl_source` or a workbook.
- The timers read and the case read write nothing and publish nothing.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-01, TC-E2-004-04 to TC-E2-004-06, TC-E2-004-11, TC-E2-004-15 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40 | TC-E2-004-02, TC-E2-004-07 to TC-E2-004-09, TC-E2-004-12 to TC-E2-004-14, TC-E2-004-16 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-03, TC-E2-004-10 |
| REQ-CWC-011 | Warning thresholds and escalation targets are data and a breach raises an event without moving the case | Business Requirements Epic 1, section 4; Program, section 5.3 | FEAT-CHO-06, FEAT-CWC-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-E2-004-02, TC-E2-004-12 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | Architecture Decision Records | Template and Rules §R8.4 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-02, TC-E2-004-14, TC-E2-004-16 |
| ADR-018 | No data lake; rwb-reporting read model from events | Architecture Decision Records | Template and Rules §R8.4 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-004-03, TC-E2-004-10 |

### 19. Out of scope

- The treatment entity, its lifecycle, the treatment write and the TreatmentApproved publication (S2, RWB-S2-E2004-APP).
- The offer builder, treatment screens and submission for approval (S2, Epic 3, FEAT-TRT-01).
- Reading the ACE plan status that starts the plan (RWB-P3-E2002-APP).
- Booking confirmation from the ALS load and the booked at date (RWB-P3-E2007-APP).
- Payment matching that raises PaymentMissed (P8, JOB-07).
- Broken plan handling after the cure period (R-RES-29 to R-RES-32, Epic 3).
- The rule package authoring, approval and rollback (RWB-P3-E2042-APP; RWB-P3-E1073-APP) and the package registry (P7).
- The DP04 treatment data product, its 01:30 load and its freshness stamps (P1 rwb-source-data and P9 rwb-reporting, JOB-15). The story reads the product through the P1 contract only (GAP-0704; ASM-1251).
- The stage service-level, prescription and notice timers and their escalation (RWB-P3-E1028-APP; RWB-P3-E2015-APP).
- The contract baseline itself (RWB-P3-E2004-CON).
- The Helm values, the consumer groups, the dashboards, the alerts and the runbook (RWB-P3-E2004-OPS).
- The cross-service journey harness and its evidence (RWB-ITG-E2004-ITG).

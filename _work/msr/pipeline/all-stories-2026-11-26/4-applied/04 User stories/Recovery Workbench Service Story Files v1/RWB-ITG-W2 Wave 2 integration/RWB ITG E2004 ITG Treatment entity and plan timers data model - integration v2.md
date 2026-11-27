# RWB-ITG-E2004-ITG Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2004-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2004-APP, RWB-P7-E2004-APP, RWB-S2-E2004-APP, RWB-P4-E2004-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020, FR-PLT-022, FR-PLT-023) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-004 for the wave 2 integration harness. The harness proves the cross-service treatment-entity and plan-timer deliverable on the owners' own endpoints: the treatment written once by rwb-treatment in `rwb_treatment` with its local decision record written first and one TreatmentApproved published, the package version fetched from the rwb-decision registry and the rule evaluated in the owning service's embedded Drools, the INSTALLMENT_DUE and CURE_PERIOD timers created and expired as durable timers of the workflow kit instead of the retired Quartz job JOB-05, the route state moved by rwb-case on `rwb_case`, the DP04 rows read as a read-only copy built from events through rwb-source-data, every refusal and the exception queue, the duplicate event left with one timer and one record, and the schema, one-hop and topic-name boundary the run enforces, with one evidence report per run. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E2004-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and test team (QA)**, I want **a repeatable cross-service harness that drives the treatment record, the plan timers and the treatment data product through rwb-treatment, rwb-case, rwb-decision, rwb-source-data and rwb-access, that reads every value back through its owner's contract, and that writes one evidence report per run**, so that **an approved plan is proved to have exactly one treatment row, one approved package version on its decision record, one durable INSTALLMENT_DUE timer and one cure-period timer that survive a restart, a DP04 copy that is built from events and never written by the treatment service, and the refusals and the exception queue the legacy story defined — across services, on Day 1 and on every release after**.

This story is the wave 2 integration harness for the legacy key. It builds no production endpoint, table, workflow or schedule and it owns no table. The behaviour under test is owned by the four I stories: RWB-S2-E2004-APP (the treatment entity, its lifecycle and the write of the treatment in `rwb_treatment`), RWB-P3-E2004-APP (the case route state, the task and the timer record in `rwb_case`), RWB-P7-E2004-APP (the embedded Drools evaluation, the local decision record and the package version it read) and RWB-P4-E2004-APP (the rights and scope check). The harness builds the runner, the fakes, the seeds and the evidence, and it owns the nine acceptance criteria listed in section 7.

The timer in the target design is not the legacy one. DP-10 replaces TimerScheduler and its Quartz implementation JOB-05 with a durable timer of the workflow kit inside the workflow that owns the wait: the TreatmentWorkflow of S2 rwb-treatment runs the restructure stage, and the CaseWorkflow of P3 rwb-case holds the case route state and the durable timers whose records sit in `rwb_case`. The plan timer is therefore a durable timer, not a row polled by a five-minute Quartz check, and the harness asserts exactly that.

### 2. Business rationale

Today a restructure plan is agreed in ACE and NLEADS, and nothing in recovery holds its terms or watches its payment dates, so a missed installment is found late. The legacy story put the treatment record with its terms, approval, booking and outcome in the Workbench, started the installment timer from the first due date, started the cure period when a payment was missed and published the treatment data product for reporting.

In the target architecture that one journey is served by five services. rwb-treatment owns the treatment and its contract, and writes it with its own local decision record in one transaction. rwb-case owns the case route state, the task and the timer record. rwb-decision governs package RESTRUCTURE and the version in force, while the evaluation itself runs inside the owning service's embedded Drools and never on a shared rule server. rwb-source-data owns the stage 2 data products and reads the ACE views. rwb-access answers the rights and scope check. A defect at any of those seams would only appear with a live case: a treatment written without its decision record, a rule answer that names no package version, a timer created outside the workflow kit, a cure period counted from the wrong date, a DP04 row written by the treatment service, or a refusal that returns data.

This story is that exercise. It drives the plan from the treatment write to the cure period in one run per business date, reproduces every refusal and the exception queue of the legacy story in the same run, and attaches one evidence report per run keyed by story and business date, so the plan journey can be shown to hold before the wave is accepted and after every change. It meets REQ-CHO-006, REQ-CHO-007, REQ-RDF-014 and REQ-CWC-011 at the integration level, and it leaves every business rule, every screen behaviour and every table with the owning stories.

### 3. Preconditions

- The four I stories are published and deployed in the SIT environment as they land: RWB-S2-E2004-APP (the treatment entity, its lifecycle, the treatment write and the TreatmentApproved event), RWB-P3-E2004-APP (the case route state, the task, the timer record and the plan-timer step), RWB-P7-E2004-APP (the embedded Drools evaluation, the local decision record and the package version it read) and RWB-P4-E2004-APP (the rights and scope check).
- gateway-bff is deployed with the composite case-record route of DP-19 available, so the treatment and plan sections, the timer view and the deviation view are read as one gateway answer and not by the browser calling each service. The composite route path and its merge order are Not specified in the source documents (GAP-0389; ASM-0564).
- The contract fakes of §12.8 are published from the owning services' OpenAPI documents, so the harness runs green from Day 1 before any I story lands.
- The synthetic seeds of the legacy story exist and are loaded through the owners' contracts or their fakes: case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"; decision log entry "DLE-9001" recording the approval of a restructure at level "L4" by user "U-APR-01"; CURE_PERIOD_DAYS for "MORTGAGE" of 30 calendar days and `plan.warn-days` of 3; package "RESTRUCTURE" version "RES-2026.12" in force with rows R-RES-25, R-RES-27, R-RES-29, R-RES-30 and R-RES-31; the ten treatments of business date 2026-12-01 over "MORTGAGE", "HIRE_PURCHASE" and "SSME", eight APPROVED and two BOOKED; case "RW-2026-000202" in route state "WITH_FCR_OFFICER"; case "RW-2026-000203" with status "CLOSED".
- The seeding of the case, the treatment, the package versions and the business clock, and the harness repository and its SIT and UAT environments, are Not specified in the source documents (GAP-0389; ASM-0564). The business date of the run is a harness setting, and the clock is moved only by the harness, so a due date of 2026-12-31 and a business date of 2027-01-01 are reproducible.
- The reference data and parameters the journey reads are loaded by their owners through their contracts: LOV-TIMER with INSTALLMENT_DUE, LOV-TREATMENT, LOV-TRT-OUTCOME, CURE_PERIOD_DAYS per product and `plan.warn-days`; the harness holds no copy of any of them.
- Feature `rwb.p3.plan-timers`, the legacy switch of this story, is on in the harness environment, so the plan timers start; the harness reads the flag through the platform library and asserts the off state, where the treatment is recorded and no plan timer starts.
- No build dependency: the harness starts on Day 1 against the fakes, and each fake is replaced by the real service as its I story lands.

### 4. Flow

1. Harness: starts a run for the story and the business date, takes the run lock, and records the build under test, the harness pack version, the business clock and the fake or real mode of each of the owning services it touches.
2. Harness: seeds the run through the contract of each owning service, or through the fake in fake mode — the cases "RW-2026-000201", "RW-2026-000202" and "RW-2026-000203", the approval entry "DLE-9001" at level "L4" by "U-APR-01", the parameters CURE_PERIOD_DAYS 30 and `plan.warn-days` 3, package "RESTRUCTURE" version "RES-2026.12" with its five rows, and the ten treatments of 2026-12-01.
3. Harness: posts the approved plan for "RW-2026-000201" — 36 installments, offer amount 850000.00, approval level "L4", entry "DLE-9001", first payment due 2026-12-31 — to `POST /api/recovery/treatment/v1/cases/{caseId}/treatments` and asserts the treatment of AC1 through `GET /api/recovery/treatment/v1/treatments/{treatmentId}`, with booked at empty, the local decision record written first and exactly one `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` (AC1).
4. Harness: waits for the plan-timer step of rwb-case, asserts the package answer of `GET /api/recovery/decision/v1/admin/rule-packages/RESTRUCTURE/versions`, the R-RES-25 answer under version "RES-2026.12", the INSTALLMENT_DUE timer with expiry 2026-12-31 23:59 Asia/Bangkok and warn 2026-12-28 read through `GET /api/recovery/case/v1/cases/{caseId}/timers`, the route state PLAN_RUNNING read through `GET /api/recovery/case/v1/cases/{caseId}` with status still IN_PROGRESS, and that the timer came from a durable timer of the workflow kit and not from Quartz (AC2).
5. Harness: moves the business clock to 2026-12-31 23:59 Asia/Bangkok, asserts the expiry and the timer status EXPIRED, then delivers the missed installment of due date 2026-12-31 on business date 2027-01-01 through the rwb-payment fake and asserts the R-RES-27 answer under version "RES-2026.12", the decision record written first, the CURE_PERIOD timer to 2027-01-31 and the route state PLAN_CURE_PERIOD (AC3).
6. Harness: reads the DP04 rows of business date 2026-12-01 through `GET /api/recovery/source-data/v1/data-products/DP04/records`, asserts ten rows with eight APPROVED and two BOOKED, and asserts that rwb-treatment holds no reporting table and wrote none of the rows (AC4).
7. Harness: sends the three invalid plans of AC5 — no first due date, an unknown entry "DLE-0000", and a first due date of 2026-11-30 before the proposal of 2026-12-01 — and asserts MSG-GEN-001 naming "first due date", MSG-GEN-001 naming "decision log entry" and MSG-GEN-003 naming "first due date" and "proposed at", with no treatment and no event written (AC5).
8. Harness: delivers a TreatmentApproved with a first due date for case "RW-2026-000202" in WITH_FCR_OFFICER and asserts no timer, MSG-P3-005 naming "PLAN_RUNNING" and "WITH_FCR_OFFICER" and the exception queue; then posts a plan for the closed case "RW-2026-000203" and asserts the refusal with MSG-P3-005 (AC6).
9. Harness: replays the TreatmentApproved event of step 3 with the same event id and asserts one timer, one local decision record and one idempotency hit (AC7).
10. Harness: removes every RESTRUCTURE version in force through the P7 fake, delivers TreatmentApproved for "RW-2026-000201" and asserts NoPackageInForce with MSG-P3-027, no record, no timer, no route change, no retry and the exception queue for role RW-TEAMMGR (AC8).
11. Harness: runs the boundary assertions of AC9 over the run trace, the schema grants and the topic names, and fails the run on a direct insert into the timer table, a cross-schema read or key, a second hop or a topic that is not the owner's (AC9).
12. Harness: publishes the evidence report keyed by story id and business date with one row per criterion, the seam each row exercised, the service or fake that answered, the record or timer observed and the pass or fail result; the evidence format and its retention, and the pass/fail gate, are Not specified in the source documents (GAP-0389; ASM-0564).
13. Harness: releases the run lock and, on any failed criterion, fails the run and names the criterion, the seam and the observed value.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field of the treatment is missing | No treatment and no event are written; the refusal names the field | MSG-GEN-001 | AC5; TC-E2-004-04-ITG |
| X2 | The named decision log entry does not exist or has no approver | No treatment is written; the refusal names the entry | MSG-GEN-001 | AC5; TC-E2-004-05-ITG |
| X3 | The first due date is before the proposal date | No treatment is written; the refusal names both fields | MSG-GEN-003 | AC5; TC-E2-004-06-ITG |
| X4 | The case is not in the route state the rule expects when the event arrives | No timer; the case sits in the exception queue with the gap | MSG-P3-005 | AC6; TC-E2-004-07-ITG |
| X5 | The same TreatmentApproved event arrives twice | One timer, one record, and the repeat counted as an idempotency hit | None | AC7; TC-E2-004-08-ITG |
| X6 | The decision record cannot be written when the timer would start | Nothing moves; the route state stays unchanged; the retry is bounded and then the exception queue is used | MSG-P7-003 | AC2; TC-E2-004-09-ITG, TC-E2-004-16-ITG |
| X7 | The 01:30 extract fails | The DP04 copy keeps the previous business date and shows it as stale | MSG-P1-001 | AC4; TC-E2-004-10-ITG |
| X8 | The case is closed | The plan is refused; nothing is written | MSG-P3-005 | AC6; TC-E2-004-11-ITG |
| X9 | No RESTRUCTURE version is in force on the business date | NoPackageInForce; no record, no timer and no route change; the case sits in the exception queue for a person | MSG-P3-027 | AC8; TC-E2-004-13-ITG |

The harness asserts the status, the message id and the substituted values of every refusal, and never rewrites a message text. X6 is asserted through the fakes, because the harness never stops a production store.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the four I stories are deployed; until then it runs against the §12.8 fakes, with no work order inside another team's lane |
| Negotiable | The seeds, the fakes, the clock, the evidence format and the gate are configuration and data; the criteria are the legacy behaviour at the cross-service seam |
| Valuable | The plan journey is proved across rwb-treatment, rwb-case, rwb-decision, rwb-source-data and rwb-access, with one timer source and one version on every answer |
| Estimable | One runner, one fake pack, one seed set, one evidence publisher and one gate |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each of the sixteen `-ITG` test cases of section 16 is one run of the harness and one row of the evidence report |

### 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers data model - wave 2 integration harness

  Background:
    Given the business date is 2026-12-01
    Given case "RW-2026-000201" with product group "MORTGAGE", status "IN_PROGRESS" and route state "BOOKED_IN_ALS_NLEADS"
    Given decision log entry "DLE-9001" records the approval of a restructure at level "L4" by user "U-APR-01"
    Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25, R-RES-27, R-RES-29, R-RES-30 and R-RES-31

  Scenario: AC1 The treatment is written once across the two services and published once (new, D-RCV-60)
    Given a TDR plan approved for "RW-2026-000201" with 36 installments, offer amount 850000.00, approval level "L4" and decision log entry "DLE-9001"
    When the harness posts it to POST /api/recovery/treatment/v1/cases/{caseId}/treatments
    Then one treatment exists with type "RESTRUCTURE", installments 36, offer amount 850000.00, approval level "L4", decision log entry "DLE-9001" and the case link, read through GET /api/recovery/treatment/v1/treatments/{treatmentId}
    And booked at is empty until the booking is confirmed
    And the local decision record of rwb-treatment is written before the treatment row is committed, in the same transaction and in the same schema
    And exactly one rwb.treatment.TreatmentApproved.v1 is observed on rwb.treatment.events.v1 with the treatment ID and the case ID
    And the approval entry "DLE-9001" is read through GET /api/recovery/decision/v1/decision-log and names "U-APR-01" at level "L4"
    And the treatment row is in rwb_treatment and no other service writes it

  Scenario: AC2 The timer is created through the workflow kit and not by Quartz (new, D-RCV-60)
    Given a plan with the first payment due on 2026-12-31
    When the plan-timer step of rwb-case consumes rwb.treatment.TreatmentApproved.v1
    Then rwb-decision answers package "RESTRUCTURE" version "RES-2026.12" through GET /api/recovery/decision/v1/admin/rule-packages/RESTRUCTURE/versions
    And R-RES-25 is evaluated in the embedded Drools of rwb-case under version "RES-2026.12"
    And the local decision record of rwb-case is written first, with rule "R-RES-25" and version "RES-2026.12"
    And one "INSTALLMENT_DUE" timer exists on rwb-case with expiry 2026-12-31 23:59 Asia/Bangkok, warn 2026-12-28 and status "RUNNING", read through GET /api/recovery/case/v1/cases/{caseId}/timers
    And the timer is a durable timer of the workflow kit inside CaseWorkflow, and no JOB-05 timer check and no Quartz schedule exists in the run
    And the case route state is "PLAN_RUNNING" and its status stays "IN_PROGRESS"

  Scenario: AC3 The timer expires and a missed payment starts the cure period (new, D-RCV-60)
    Given the "INSTALLMENT_DUE" timer of AC2 has reached its expiry of 2026-12-31 23:59 Asia/Bangkok
    When the durable timer fires and the payment matching of rwb-payment reports the installment of due date 2026-12-31 unpaid on business date 2027-01-01
    Then the expiry produces the timer-due fact with timer type "INSTALLMENT_DUE" and the treatment ID, observed on the workflow history of the case because TimerDue has no Kafka topic
    And the timer status is "EXPIRED"
    And rwb.payment.PaymentMissed.v1 is observed on rwb.payment.events.v1 for the treatment with due date 2026-12-31
    And rwb-decision answers package "RESTRUCTURE" version "RES-2026.12" and R-RES-27 is evaluated under that version
    And the local decision record with rule "R-RES-27" and version "RES-2026.12" is written first
    And one "CURE_PERIOD" timer exists with expiry 2027-01-31, created by a durable timer of the workflow kit
    And the case route state is "PLAN_CURE_PERIOD" and its status stays "IN_PROGRESS"

  Scenario: AC4 The data product is a read-only copy built from events (new, D-RCV-60)
    Given ten treatments are recorded on 2026-12-01 across "MORTGAGE", "HIRE_PURCHASE" and "SSME"
    Given two of them have a booked at date
    When the 01:30 extract of business date 2026-12-02 has run
    Then GET /api/recovery/source-data/v1/data-products/DP04/records returns ten rows for business date 2026-12-01
    And eight show status "APPROVED" and two show status "BOOKED"
    And the rows are a read-only copy built from the treatment events, and rwb-treatment holds no reporting table and writes no row
    And the harness starts no extract, writes no row and reads no other service's schema

  Scenario: AC5 The required fields and the unknown decision entry are refused (new, D-RCV-60)
    Given a restructure plan for "RW-2026-000201" with no first due date
    When the harness posts it to POST /api/recovery/treatment/v1/cases/{caseId}/treatments
    Then the system refuses it with MSG-GEN-001 naming "first due date"
    And no treatment and no event are written
    Given a plan that names decision log entry "DLE-0000" which does not exist
    When the harness posts it
    Then the system refuses it with MSG-GEN-001 naming "decision log entry"
    And no treatment and no event are written
    Given a plan proposed on 2026-12-01 with the first due date 2026-11-30
    When the harness posts it
    Then the system refuses it with MSG-GEN-003 naming "first due date" and "proposed at"
    And no treatment and no event are written

  Scenario: AC6 A case not in the booked state and a closed case are refused (new, D-RCV-60)
    Given case "RW-2026-000202" in route state "WITH_FCR_OFFICER"
    When a TreatmentApproved event with a first due date arrives for it
    Then the system writes no timer
    And the system places the case in the exception queue with MSG-P3-005 naming "PLAN_RUNNING" and "WITH_FCR_OFFICER"
    Given case "RW-2026-000203" with status "CLOSED"
    When the harness posts a plan for it
    Then the system refuses it with MSG-P3-005
    And no treatment and no timer are written

  Scenario: AC7 The same event delivered twice leaves one timer and one record (new, D-RCV-60)
    Given the rwb.treatment.TreatmentApproved.v1 of AC1 was processed with its event id
    When the same event with the same event id is delivered again
    Then no second INSTALLMENT_DUE timer and no second local decision record are written
    And one timer and one decision record exist for the treatment
    And the inbox of rwb-case counts the repeat as one idempotency hit
    And no event is published by the repeat

  Scenario: AC8 No RESTRUCTURE version in force stops the plan (new, D-RCV-60)
    Given no "RESTRUCTURE" version is in force on 2026-12-01
    When the plan-timer step of rwb-case consumes rwb.treatment.TreatmentApproved.v1 for "RW-2026-000201"
    Then NoPackageInForce is raised with MSG-P3-027 for package "RESTRUCTURE"
    And no local decision record, no timer and no route state change are written
    And the case is placed in the exception queue for role "RW-TEAMMGR" with the gap
    And the activity is not retried, because NoPackageInForce is non-retryable
    And no rule is evaluated without the version answer of the registry

  Scenario: AC9 The boundary the harness enforces (new, D-RCV-60)
    Given the harness holds the run trace, the schema grants of the run and the topic names observed
    Then the run fails when a component inserts into the timer table outside the workflow kit
    And the run fails when anything other than rwb-treatment writes rwb_treatment treatment
    And the run fails when anything other than rwb-case writes rwb_case timer
    And the run fails on a cross-schema read or on a foreign key between rwb_treatment and rwb_case
    And every call in the trace is one hop with a 2 s timeout
    And every topic is the owner's rwb.<short>.events.v1 and every event is the owner's rwb.<short>.<Event>.v1
```

These nine criteria are new for the ITG harness. The legacy criteria AC1 to AC14 of RWB-E2-004 stay with the app stories and are not restated here.

### 8. Business rules

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
| BR13 | The plan timer is a durable timer of the workflow kit inside the workflow that owns the wait; TimerScheduler and its Quartz implementation JOB-05 are retired, and the five-minute timer check has no replacement | DP-10; Arch v5 slide 44 (JOB-05 retired); ADR-016 |
| BR14 | The rule package and the version come from the rwb-decision registry, and the evaluation runs in the owning service's embedded Drools; every answer names the package version it read and no evaluation runs without one | DP-04; Arch v5 slide 27; ADR-017 |
| BR15 | The treatment is rwb-treatment's and the timer record is rwb-case's; no service reads, joins or holds a key to another service's schema, and the data product is a read-only copy built from events | DP-01; Arch v5 slide 29; ADR-014, ADR-018 |
| BR16 | The treatment data product is read through rwb-source-data's contract by every caller; there is no data lake and no Power BI feed | DP-05; DP-17; ADR-018 |

BR1 to BR12 are the legacy rules of RWB-E2-004 copied word for word with their sources. BR13 to BR16 are the realignment rules this harness proves; the harness asserts them against the owning services and the published contracts and re-implements none of them.

### 9. State transitions

None. This story changes no case status and no case state; the harness drives the owning services and asserts records only, and it adds no transition of its own. The case status stays IN_PROGRESS through both route moves, as BR3 and the legacy state table require. The facts below are caused by the owning services and are observed and asserted by the harness.

| Observed fact | Caused by | Asserted as |
|---|---|---|
| Treatment recorded with its terms, level and entry | rwb-treatment, in one transaction with its local decision record and its outbox row | One treatment row with type RESTRUCTURE, 36 installments, 850000.00, level "L4" and entry "DLE-9001" (TC-E2-004-01-ITG) |
| Timer created | rwb-case, by a durable timer of CaseWorkflow after the R-RES-25 record | One INSTALLMENT_DUE timer with expiry 2026-12-31 23:59 Asia/Bangkok and warn 2026-12-28 (TC-E2-004-02-ITG) |
| Timer expired | The durable timer of the workflow kit firing, not a Quartz check | The timer-due fact with the treatment ID and the timer status EXPIRED (TC-E2-004-02-ITG) |
| Route moved | rwb-case, on the rule answer it recorded first | Route state PLAN_RUNNING and then PLAN_CURE_PERIOD, with status IN_PROGRESS unchanged (TC-E2-004-02-ITG, TC-E2-004-12-ITG) |
| Data product row written | rwb-source-data, from the treatment events, through the 01:30 extract | Ten DP04 rows for 2026-12-01, eight APPROVED and two BOOKED (TC-E2-004-03-ITG) |
| Exception raised | rwb-case, when the case is not in the state the rule expects or no version is in force | The case in the exception queue with MSG-P3-005 or MSG-P3-027 (TC-E2-004-07-ITG, TC-E2-004-13-ITG) |

The harness writes no treatment, no timer, no decision record and no DP04 row; when a step is refused it records the refusal and leaves the stores exactly as they were.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Reads the treatment, the timers and the route state of cases in scope (Treatment and offer CRU; Case record R); the synthetic user the harness drives |
| RW-COE, center of excellence analyst | Reads the treatment and the package version it recorded (Treatment and offer R; Reference data R); changes nothing |
| RW-TEAMMGR, team manager | Receives the exception-queue entry of an AC8 refusal (Case record R) |
| RW-PHONECOL, phone collector | Holds no Treatment and offer right; the access case proves the refusal |
| RW-DATASTEW, data steward | Reads the DP04 rows and their business date through the rwb-source-data contract (Reporting R) |
| RW-PLATADM, platform administrator | Reads the run trace, the workflow history and the schema grants for a platform check |
| QA lead | Owns the harness pack, the seeds, the clock, the evidence format and the gate |
| Integration lead | Owns the fake pack, the run of record and the replacement of each fake by its I story |
| Platform workflow owner | Owns the durable-timer behaviour of the workflow kit that the run observes |
| No approval applies | The story takes no decision; the approval "DLE-9001" is seeded and the harness asserts the decisions of the owning stories |

### 11. Data

The harness owns no table (DP-01). It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary. Every table named here belongs to an app story: `treatment` in schema `rwb_treatment` is S2 rwb-treatment's (RWB-S2-E2004-APP); `recovery_case`, `timer`, `task` and `queue` in schema `rwb_case` are P3 rwb-case's (RWB-P3-E2004-APP); `decision_log_entry`, `rule_package`, `rule_package_version` and `rule_row` in schema `rwb_decision` are P7 rwb-decision's (RWB-P7-E2004-APP); and the DP04 rows `dp_treatment`, `data_product` and `data_product_load` in schema `rwb_source_data` are P1 rwb-source-data's, read here through the P1 contract.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment | all fields | Read through the S2 contract, asserted on the treatment of AC1 |
| DF-TRT-029 | treatment | first_due_date | Read through the S2 contract |
| DF-WRK-027 to DF-WRK-036 | timer | all fields | Read through the P3 contract |
| DF-WRK-042 | timer | treatment_id | Read through the P3 contract |
| DF-CAS-001 | recovery_case | id | Read through the P3 contract |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 contract |
| DF-CAS-005 | recovery_case | status | Read through the P3 contract |
| DF-CAS-007 | recovery_case | route_state | Read through the P3 contract |
| DF-CAS-021 | recovery_case | rule_version | Read through the P3 contract |
| DF-REF-002 | rule_row | rule_id | Read through the P7 contract, from the evaluation result |
| DF-REF-003 | rule_row | rule_version | Read through the P7 contract, from the evaluation result |
| DF-REF-296 | rule_row | package_version_id | Read through the P7 contract |
| DF-REF-298 | rule_row | outputs | Read through the P7 contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 contract |
| DF-DEC-010 | decision_log_entry | approver_user_id | Read through the P7 contract, for entry "DLE-9001" |
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields, including the treatment link and the derived status | Read through the P1 data-product contract; written by the P1 data-product story, never by the harness |

The fields of `timer` and `recovery_case` are read through `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers`; the fields of `decision_log_entry`, `rule_package` and `rule_package_version` through `GET /api/recovery/decision/v1/decision-log` and `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`; and the DP04 rows through `GET /api/recovery/source-data/v1/data-products/DP04/records`. The harness joins nothing and holds no copy of any row. `rule_row` is read by rule ID and package version through the evaluation result and the catalog; the harness reads no `drl_source` and no workbook.

Test data is synthetic. No production case, party, account, treatment or payment is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness provides no REST operation; it calls the owning services and their fakes.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/treatment/v1/cases/{caseId}/treatments` | S2 rwb-treatment | The approved plan the harness posts, and the three refusals of AC5 and the closed case of AC6 (AC1, AC5, AC6) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment read back with its type, terms, level, entry and booked at (AC1, AC7) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case facts, the route state and the status after each move (AC2, AC3, AC6, AC8) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The INSTALLMENT_DUE and CURE_PERIOD timers with their expiry, warn and status (AC2, AC3, AC6, AC8) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The approval entry "DLE-9001" and the local decision records with rule and version (AC1, AC2, AC3, AC8) |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The package "RESTRUCTURE" version in force, version "RES-2026.12", and the no-version state of AC8 (AC2, AC3, AC8) |
| GET | `/api/recovery/source-data/v1/data-products/DP04/records` | P1 rwb-source-data | The ten DP04 rows of business date 2026-12-01 (AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The role, the scope and the Treatment and offer right of the reader, asserted on the access case |

The case deviation read is not listed because the ownership map holds no deviations operation for rwb-case: the exception queue is asserted on the case facts of `GET /api/recovery/case/v1/cases/{caseId}` and on the timer list, not through a deviations path. The treatment and plan sections, the timer view and the deviation view are read by a screen through the gateway-bff composite case-record route (DP-19), owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order are Not specified in the source documents (GAP-0389; ASM-0564).

#### 12.3 Events published

None. The harness publishes no Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| rwb.treatment.TreatmentApproved.v1 | rwb.treatment.events.v1 | S2 rwb-treatment (EV-10) | Exactly one event is published for the treatment of AC1, with the treatment ID and the case ID, and a second delivery of the same event id leaves one timer and one record (AC1, AC7) |
| rwb.payment.PaymentMissed.v1 | rwb.payment.events.v1 | P8 rwb-payment (EV-12) | The missed installment of due date 2026-12-31 arrives on business date 2027-01-01 with the treatment ID, and starts the R-RES-27 evaluation of AC3 (AC3) |
| TimerDue (EV-18) | None: retired as a Kafka event (Architecture v5 slide 42 row 18) | PLT: the durable-timer behaviour of the workflow kit, observed on the workflow history of the case | The expiry of the INSTALLMENT_DUE timer names timer type "INSTALLMENT_DUE" and the treatment ID, and the timer status moves to EXPIRED (AC3) |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 | P7 rwb-decision owns the topic and the central ledger; every service publishes its own local record (EV-08) | The R-RES-25, R-RES-27 and refusal records reach the central ledger with rule ID and package version "RES-2026.12", and no record exists where AC8 wrote none (AC1, AC2, AC3, AC8) |

The harness consumes these topics as a test consumer with its own group and asserts the records through the P7 and P3 contracts; it holds no inbox table of its own, gets no production record, and publishes nothing. No case event is consumed: the route state and the case status are read through the P3 contract, and the event design gives the route move no event that this run needs.

#### 12.5 Workflows and activities

None added. The harness starts no Temporal workflow, calls no activity and uses no queue `rwb-treatment` or `rwb-case`. It observes the two workflows of the journey and the rule evaluation they call:

| Observed | Queue | Owner | What the harness asserts |
|---|---|---|---|
| TreatmentWorkflow, the restructure stage | rwb-treatment | S2 rwb-treatment (RWB-S2-E2004-APP) | The treatment write of AC1, its local decision record written first and the one TreatmentApproved that leaves the stage (AC1, AC7) |
| CaseWorkflow, the case, its route state and its durable timers | rwb-case | P3 rwb-case (RWB-P3-E2004-APP) | The INSTALLMENT_DUE and CURE_PERIOD timers, the expiry, the two route moves, the duplicate tolerance and the exception queue (AC2, AC3, AC6, AC7, AC8) |

The rule evaluation the stages call is an activity in the owning service (EvaluateRules on the owner's queue) with the package and the version fetched from P7 rwb-decision's registry; the harness reads the local decision record the activity wrote and never evaluates a rule itself. No TimerScheduler call, no Quartz job and no timer check of JOB-05 exists in the run.

#### 12.6 Schedules

None added and none started. The harness reads one schedule it depends on: the 01:30 extract, JOB-15, owned by P9 rwb-reporting and triggered by the bank Airflow in the job map (no data lake), which loads the DP04 rows into `rwb_source_data` and is read back through the rwb-source-data contract. The harness never starts it, never pauses it and never changes it, and the rows it asserts are the ones the owner loaded.

#### 12.7 Tables owned

None. The harness owns no table and no schema (DP-01; DP-15 resolves to no migration). The tables it reads are owned as stated in section 11: `treatment` in `rwb_treatment` by RWB-S2-E2004-APP; `recovery_case`, `timer`, `task` and `queue` in `rwb_case` by RWB-P3-E2004-APP; `decision_log_entry`, `rule_package`, `rule_package_version` and `rule_row` in `rwb_decision` by RWB-P7-E2004-APP; `dp_treatment`, `data_product` and `data_product_load` in `rwb_source_data` by the P1 data-product stories.

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-treatment (WireMock, from its OpenAPI) | `POST /api/recovery/treatment/v1/cases/{caseId}/treatments` and `GET /api/recovery/treatment/v1/treatments/{treatmentId}`, with the treatment of "RW-2026-000201" — RESTRUCTURE, 36 installments, 850000.00, level "L4", entry "DLE-9001", booked at empty — the refusal answers of AC5, the closed-case refusal of AC6 and the ten treatments of 2026-12-01 | AC1, AC4, AC5, AC6, AC7 |
| rwb-case (WireMock, from its OpenAPI) | `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` with route state BOOKED_IN_ALS_NLEADS, then PLAN_RUNNING, then PLAN_CURE_PERIOD, status IN_PROGRESS throughout, the INSTALLMENT_DUE timer with expiry 2026-12-31 23:59 Asia/Bangkok and warn 2026-12-28, the CURE_PERIOD timer to 2027-01-31, the EXPIRED status after the expiry, the exception-queue entries of AC6 and AC8, and the case "RW-2026-000202" in WITH_FCR_OFFICER and "RW-2026-000203" CLOSED | AC2, AC3, AC6, AC7, AC8, AC9 |
| rwb-decision (WireMock, from its OpenAPI) | `GET /api/recovery/decision/v1/decision-log` with entry "DLE-9001" at level "L4" by "U-APR-01", the R-RES-25 and R-RES-27 records at version "RES-2026.12", and `GET /api/recovery/decision/v1/admin/rule-packages/RESTRUCTURE/versions` with "RES-2026.12" in force and its five rows, then the no-version state of AC8 | AC1, AC2, AC3, AC8 |
| rwb-source-data (WireMock, from its OpenAPI) | `GET /api/recovery/source-data/v1/data-products/DP04/records` with ten rows for business date 2026-12-01, eight APPROVED and two BOOKED, and the stale answer of MSG-P1-001 for the failed extract of TC-E2-004-10-ITG | AC4 |
| rwb-payment (WireMock, from its Kafka and REST contracts) | `rwb.payment.PaymentMissed.v1` for due date 2026-12-31 on business date 2027-01-01, and its absence before the due date | AC3 |
| rwb-access (WireMock, from its OpenAPI) | `GET /api/recovery/access/v1/me/session` for RW-CASEOWN with the Treatment and offer right, for RW-COE and RW-DATASTEW in scope, and for RW-PHONECOL without the right | The access case; AC1 |
| gateway-bff composite case-record route (WireMock) | The one gateway answer the treatment and plan sections, the timer view and the deviation view are read from | AC2, AC3, AC4, AC6 |

The fakes are published from the owning services' OpenAPI documents, are versioned with the harness pack and are replaced by the real service as each I story lands. The harness repository, the SIT and UAT environments, the seeding of the case, the treatment, the package versions and the business clock, the evidence format and retention, the gate and the composite route detail are Not specified in the source documents (GAP-0389; ASM-0564).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, each one hop on the owner's `/api/recovery/<short>/v1` base with a 2 s timeout (DP-11, DP-13) |
| Kafka | 0 published, 4 consumed: `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1`, `rwb.payment.PaymentMissed.v1` on `rwb.payment.events.v1`, `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, and the retired TimerDue observed on the workflow history instead of a topic |
| Temporal | None started: no workflow, no activity, no queue created; two workflows observed on `rwb-treatment` and `rwb-case`, with the durable timers of the workflow kit inside them |
| File | None |

### 13. Solution plan

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
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies the table adds — RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, C RWB-P7-E1073-CON, RWB-PLT-E1042-CON, C RWB-P3-E1042-CON, RWB-PLT-E1043-CON, C RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — are held by the service and platform stories and are not repeated in the metadata columns, which stay None. DP-15 resolves to no migration because the harness owns no schema. DP-10 is the ruling this harness proves: the plan timer is a durable timer of the workflow kit inside the workflow that owns the wait, JOB-05 and its Quartz check are retired, and the harness fails a run whose trace shows a timer created or expired anywhere else. The blocking dependencies of this story are the four I stories, which replace the fakes with the real behaviour; they gate the done state, not the Day-1 start.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| PlanJourneyRunner | Test harness | Runs the sixteen `-ITG` cases of §16 in one run per business date, in fake or real mode per service, moves the business clock, and stops at the first failed assertion with the trace |
| TreatmentClient | Harness adapter | Calls the eight consumed operations of §12.2 with the case, treatment, package and business-date parameters, and records each answer |
| TreatmentSeedLoader | Service | Seeds the three cases, the approval entry, the parameters, the package version with its five rows and the ten treatments through the owner's contract or the fake |
| TreatmentAsserter | Assertion | Asserts the treatment type, installments, offer amount, level, entry, case link and the empty booked at, and that the row is written once |
| DecisionRecordAsserter | Assertion | Asserts that the local decision record is committed before the state change, that it names rule "R-RES-25" or "R-RES-27" with version "RES-2026.12", and that no record exists where AC8 wrote none |
| TimerAsserter | Assertion | Asserts the INSTALLMENT_DUE and CURE_PERIOD timers with their expiry, warn and status, the expiry of 2026-12-31 23:59 Asia/Bangkok, the CURE_PERIOD expiry of 2027-01-31 and the EXPIRED status |
| DurableTimerGuard | Assertion | Fails the run when a component inserts into the timer table outside the workflow kit, when a Quartz job or a JOB-05 check appears in the trace, or when a timer is expired by anything other than its workflow |
| IdempotencyCheck | Assertion | Replays the TreatmentApproved event with its event id and asserts one timer, one record and one inbox hit |
| VersionAsserter | Assertion | Asserts that every evaluation names the package version read from the registry, and that NoPackageInForce stops the step with no record, no timer and no route change |
| DataProductAsserter | Assertion | Asserts the ten DP04 rows, eight APPROVED and two BOOKED, for business date 2026-12-01 and that rwb-treatment wrote none of them |
| RefusalAsserter | Assertion | Asserts the status, the message id and the substituted values of MSG-GEN-001, MSG-GEN-003, MSG-P3-005, MSG-P3-027, MSG-P7-003 and MSG-P1-001, and the exception-queue entry |
| SchemaBoundaryCheck | Assertion | Fails the run on any cross-schema read, any foreign key between `rwb_treatment` and `rwb_case` and any trace deeper than one hop, and checks that every topic is the owner's |
| FakePack | WireMock project | Serves the seven fakes of §12.8 from the published OpenAPI documents |
| RunLock | Service | One run at a time in the harness environment |
| EvidenceReportPublisher | Reporter | Writes the per-run evidence report keyed by story id and business date and attaches it to the release record |
| JourneyGate | Assertion | Passes the run only when every owned criterion passes; fails and names the criterion, the seam and the observed value |

**Database.** None. The harness owns no schema, runs no Flyway migration and holds no table; seeds and assertions go through the contracts (DP-01, DP-15).

**Environment and test data.** SIT for the run of record and UAT for the acceptance run, with `rwb.p3.plan-timers` on in both. The data are the synthetic seeds of the legacy story: case "RW-2026-000201" with product group MORTGAGE, status IN_PROGRESS and route state BOOKED_IN_ALS_NLEADS; entry "DLE-9001" at level "L4" by "U-APR-01"; CURE_PERIOD_DAYS 30 and `plan.warn-days` 3; package "RESTRUCTURE" version "RES-2026.12" with rows R-RES-25, R-RES-27, R-RES-29, R-RES-30 and R-RES-31; the plan of 36 installments, 850000.00, first payment due 2026-12-31; the ten treatments of 2026-12-01 over MORTGAGE, HIRE_PURCHASE and SSME, eight APPROVED and two BOOKED; case "RW-2026-000202" in WITH_FCR_OFFICER; case "RW-2026-000203" CLOSED; business dates 2026-12-01 and 2027-01-01 with the clock moved by the harness only. Each run starts from the seeded state, so a repeated run is deterministic. The harness repository, the environments, the seeding of the case, the treatment, the package versions and the clock, the evidence format and retention and the gate are Not specified in the source documents (GAP-0389; ASM-0564).

**Build steps**

1. Build PlanJourneyRunner and TreatmentClient against the published OpenAPI documents of the owning services and the gateway-bff route.
2. Publish FakePack for the seven fakes of §12.8 from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Write TreatmentSeedLoader and the seed files, with the run lock, the business clock and the fake or real mode per service.
4. Write TreatmentAsserter and DecisionRecordAsserter for AC1, with a unit test on fixtures for the empty booked at, the case link and the record-before-row order.
5. Write TimerAsserter and DurableTimerGuard for AC2 and AC3, including the expiry, the warn date, the cure-period expiry and the absence of any Quartz or JOB-05 path.
6. Write VersionAsserter and RefusalAsserter for AC5, AC6 and AC8, including the three field refusals, the closed case, the not-booked case, the exception queue and the non-retryable NoPackageInForce.
7. Write IdempotencyCheck and DataProductAsserter for AC7 and AC4, including the one-hit count and the ten rows with their two statuses.
8. Write SchemaBoundaryCheck and the boundary assertions of AC9, then replace each fake with the real service as its I story lands, in the order rwb-treatment, rwb-case, rwb-decision, rwb-source-data, rwb-access, and rerun in UAT.
9. Write JourneyGate and EvidenceReportPublisher, and attach the report to the release record for the build under test.

**Feature switch.** `rwb.p3.plan-timers`, the legacy switch of this story: on in SIT and UAT. The harness asserts the off state on the fakes — the treatment is recorded, no plan timer starts, the route state stays BOOKED_IN_ALS_NLEADS and no CURE_PERIOD timer appears — and asserts that the treatment row and its decision record are unchanged in that state.

**Done when.** The sixteen `-ITG` test cases of section 16 pass in SIT and UAT with the four I stories in place and not only against the fakes; the evidence report for the run is attached to the release record with the nine owned criteria green; every plan decision record in the run names its rule and package version; no timer in the trace was created or expired outside the workflow kit; and the access case, the three refusals, the not-booked and closed cases and the no-version case are green with the messages of section 14.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-P3-005 | The case is closed, or not in the state the rule expects | This case cannot move to {state} from {current}. |
| MSG-P7-003 | The decision log write fails | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The treatment data product is stale | {product} is from {date}. Today's load has not arrived. |
| MSG-P3-027 | No RESTRUCTURE version is in force | The rule version was refused at the {check} check: {detail}. |

These six rows are the legacy messages of RWB-E2-004 copied word for word. The harness asserts the message id, the rendered text and the substituted values of each row, and it never rewrites a text. For MSG-P3-027 in this story, {check} is "no package in force" and {detail} names the package code "RESTRUCTURE" and the business date only, never a case fact. The access case of TC-E2-004-15-ITG carries the legacy message MSG-P4-002 from the legacy message table and asserts it unchanged. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-14 Treatment record | Approved | The treatment section of the case record is read through the composite route and shows type RESTRUCTURE, 36 installments, 850000.00, level "L4" and entry "DLE-9001", with booked at empty |
| SCR-03 Case record | Plan running | The plan section shows the INSTALLMENT_DUE timer with its due date 2026-12-31 and its warning of 2026-12-28, and the route state PLAN_RUNNING with status IN_PROGRESS |
| SCR-03 Case record | Cure period | The plan section shows the CURE_PERIOD timer to 2027-01-31 after the missed payment of due date 2026-12-31, and the route state PLAN_CURE_PERIOD |
| SCR-03 Case record | Timer view | The timer view returns the INSTALLMENT_DUE timer as EXPIRED after the expiry of 2026-12-31 23:59 Asia/Bangkok |
| SCR-09 Exception queue | Deviation view | The case "RW-2026-000202" in WITH_FCR_OFFICER and the case of the AC8 refusal are in the exception queue with MSG-P3-005 and MSG-P3-027 |

The harness builds no screen and renders no page: it asserts the composite route answer the screen consumes, and screen-level behaviour stays with RWB-S2-E2004-APP and RWB-P3-E2004-APP. The decision log query screen SCR-38 is not referenced by this legacy key and is not asserted here; it belongs to RWB-E2-005. The composite route path and merge order are Not specified in the source documents (GAP-0389; ASM-0564).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-004-01-ITG | AC1, BR1; ITG AC1 | Integration | Restructure, 36 installments, 850000.00 baht, entry DLE-9001 |
| TC-E2-004-02-ITG | AC2, BR3, BR5, BR10, BR11; ITG AC2 | Integration | First due date 2026-12-31; clock moved past expiry |
| TC-E2-004-03-ITG | AC3, BR8; ITG AC4 | Integration | Ten treatments over three products, two booked |
| TC-E2-004-04-ITG | AC4, BR2; ITG AC5 | Integration | Restructure with no first due date |
| TC-E2-004-05-ITG | AC5, BR1; ITG AC5 | Integration | Unknown decision log entry DLE-0000 |
| TC-E2-004-06-ITG | AC6, BR2; ITG AC5 | Integration | First due date one day before the proposal |
| TC-E2-004-07-ITG | AC7, BR9; ITG AC6 | Integration | Case in route state WITH_FCR_OFFICER |
| TC-E2-004-08-ITG | AC8, BR7; ITG AC7 | Integration | Same TreatmentApproved event twice |
| TC-E2-004-09-ITG | AC9, BR6; ITG AC2 | Integration | Decision log store stopped in the test container |
| TC-E2-004-10-ITG | AC10; ITG AC4 | Integration | JOB-15 forced to fail on 2026-12-02 |
| TC-E2-004-11-ITG | AC11; ITG AC6 | Integration | Closed case |
| TC-E2-004-12-ITG | AC12, BR4, BR10; ITG AC3 | Integration | PaymentMissed for due date 2026-12-31 |
| TC-E2-004-13-ITG | AC13, BR12; ITG AC8 | Integration | No RESTRUCTURE version in force on 2026-12-01 |
| TC-E2-004-14-ITG | AC14, BR11; ITG AC9 | Integration | A component that inserts into the timer table without TimerScheduler |
| TC-E2-004-15-ITG | Access; ITG AC1 | Component | RW-PHONECOL (no Treatment and offer right) reads `GET /treatments/{treatmentId}`; refused with MSG-P4-002 |
| TC-E2-004-16-ITG | Principle 5; ITG AC2 | NFR | Decision log write forced to fail at timer start; no timer, no state change |

The sixteen `-ITG` cases keep the legacy Covers text and the legacy Data text under the same base id and add the cross-service seam each one exercises; the `ITG AC` column names the criterion of section 7 that the copy proves. The legacy criteria of RWB-E2-004 stay with the app stories: this story owns none of them, and the `-ITG` cases add the seam only. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the treatment types, the outcomes, the cure period, the warning days, the timer types and the package rows are reference data and package rows held by the owning services; the harness reads them and never holds a copy.
- No personal data in logs, tests, traces, workflow history or reports: the harness uses synthetic case, account and user identifiers, amounts are synthetic, and no production case, party or payment is copied into a fixture.
- No read of another service's schema: every read goes through the owner's contract, the SchemaBoundaryCheck fails the run on a cross-schema reference or a key between `rwb_treatment` and `rwb_case`, and only rwb-source-data reads the ACE views (DP-01, DP-05).
- No code inserts into the timer table outside the workflow kit: the DurableTimerGuard fails the run on a direct insert, on a Quartz job, on a JOB-05 timer check and on any expiry that is not the workflow's own durable timer (DP-10).
- No rule evaluation without the registry version: the VersionAsserter fails the run on an answer that names no package version, and NoPackageInForce stops the step instead of falling back to a default timer or move (DP-04).
- The decision record is written before the state change: the harness asserts the order on the treatment write and on both plan-timer steps, and asserts that a failed record leaves nothing moved.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner, and asserts the 2 s budget on every call (DP-11).
- Topic names follow the library: every topic is the owner's `rwb.<short>.events.v1` and every event its `rwb.<short>.<Event>.v1` (DP-14).
- No production data and no outside system: the harness calls only the owning services and their fakes, never a production endpoint or an outside gateway.
- The harness owns no table, no endpoint, no screen, no workflow and no schedule (DP-01, DP-15); it is test and evidence only.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25; BR1; BR2 | TC-E2-004-01-ITG, TC-E2-004-04-ITG, TC-E2-004-05-ITG, TC-E2-004-06-ITG, TC-E2-004-11-ITG, TC-E2-004-15-ITG |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25; R-RES-27; R-UNI-39; R-UNI-40 | TC-E2-004-02-ITG, TC-E2-004-07-ITG, TC-E2-004-08-ITG, TC-E2-004-09-ITG, TC-E2-004-12-ITG, TC-E2-004-13-ITG, TC-E2-004-14-ITG, TC-E2-004-16-ITG |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | BR8; BR15; BR16 | TC-E2-004-03-ITG, TC-E2-004-10-ITG |
| REQ-CWC-011 | Service levels, warnings and escalation as data; a breach does not move the case | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-13 | 06 Take over and own the case | BR5; BR13 | TC-E2-004-02-ITG, TC-E2-004-12-ITG |

The three requirements the legacy story tabulates keep their legacy BRD section and rule text. REQ-CWC-011 is tabulated here because the legacy warning rule BR5 names it and the plan warning is what AC2 and AC3 assert; its section, feature and rule text are those of the Epic 1 requirement and no new requirement ID is added. This story traces all four at the integration level only.

### 19. Out of scope

- The four owning I stories and everything they build: RWB-S2-E2004-APP (the treatment entity, its lifecycle, the treatment write and its event), RWB-P3-E2004-APP (the case route state, the task, the timer record and the plan-timer step), RWB-P7-E2004-APP (the embedded Drools evaluation, the local decision record and the package version it read) and RWB-P4-E2004-APP (the rights and scope check).
- The legacy criteria AC1 to AC14 of RWB-E2-004 and their legacy test cases, which stay with the app stories; this story owns none of them.
- Production code in any service: the harness is test and evidence only.
- The contract baselines of rwb-treatment, rwb-case, rwb-decision, rwb-source-data, rwb-payment and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON), the durable-timer behaviour of the workflow kit (RWB-PLT-E1071-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The content, the authoring, the approval and the rollback of package RESTRUCTURE and its rows R-RES-25, R-RES-27, R-RES-29, R-RES-30 and R-RES-31, which stay with the rule package work (RWB-P3-E2042-APP); this run evaluates the package and never loads or changes it.
- Booking confirmation from the ALS load and the booked at date (RWB-E2-007), and the payment matching that raises PaymentMissed (P8, JOB-07), which the run consumes from its fake and never builds.
- Broken plan handling after the cure period (R-RES-29 to R-RES-32) and the neighbouring integration stories RWB-E2-002, RWB-E2-006 and RWB-E2-008.
- The treatment data product build of the stage 2 data products and its access rows, which stay with RWB-E2-010 and the P1 data-product stories.
- The screens of the treatment offer builder and the case record beyond the states of section 15, which stay with the owning APP stories.

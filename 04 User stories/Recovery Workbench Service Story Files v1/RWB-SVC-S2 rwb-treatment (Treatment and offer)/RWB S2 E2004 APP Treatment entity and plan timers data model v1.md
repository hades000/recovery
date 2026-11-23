# RWB-S2-E2004-APP Treatment entity and plan timers data model

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-004 for rwb-treatment (S2). The treatment entity is created in schema `rwb_treatment` by this service's own Flyway sequence (DP-01, DP-15); the plan clock is no longer a `timer` row with a Quartz check but a durable Temporal timer inside `CaseWorkflow` of rwb-case (DP-10), so this service holds the plan facts the clock is built from and publishes them on `rwb.treatment.events.v1` (DP-09, DP-14); the base becomes `/api/recovery/treatment/v1` (DP-13) and the record is reached through the gateway-bff composite route (DP-19). No legacy acceptance criterion is carried: AC1 to AC14 of the legacy story stay with RWB-P3-E2004-APP, the primary slice, and this story writes new criteria for the data model it owns. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S2-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E2004-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (FR-S2-024) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the treatment entity held as the `treatment` table of schema `rwb_treatment` — terms, approval, booking, outcome and plan facts of one offer in one row, with the standard record columns, the list-value checks, the indexes and the one-running-plan guard, written in one transaction with its local decision record and its outbox row and announced on `rwb.treatment.events.v1` with the first due date and the installments the plan clock is built from** — so that **every approved plan has one record in its owner, the case side raises the installment and cure-period timers from a fixed event instead of reading this service's tables, and a missed installment is found on the day it happens**.

This is the data-model slice of legacy RWB-E2-004. It owns the table from DF-TRT-001 to DF-TRT-033 with the seven standard record columns (DP-01, DP-15); the plan facts on that row (`first_due_date`, `installments`, `installment_amount`, `installments_paid`, `installment_shortfall`, `valid_until`, `booked_at`, `outcome`, `outcome_at`) and the state derived from them; the two operations on `/api/recovery/treatment/v1` (DP-13), the local decision record of the write in the same transaction (DP-03) and its outbox row (DP-09); and the publication `rwb.treatment.TreatmentApproved.v1` (DP-14), the only channel by which the case side learns the terms and the due date (Contract dependency RWB-P3-E2004-CON).

It does not own the plan clock, the `timer` projection and the case route state (rwb-case, RWB-P3-E2004-APP); the RESTRUCTURE package and its versions (rwb-decision, RWB-P7-E2004-APP); the DP04 treatment copy (rwb-source-data, from the events; GAP-2687); the roles and rights data (rwb-access); the screens and composite routes (DP-19); or the offer builder, the submission for approval and the booking confirmation, which are later slices of the same legacy key.

### 2. Business rationale

A restructure, a settlement and a deed in lieu all end in one artefact: a treatment with terms, an approval and an outcome. The legacy story held that artefact, its plan timers and its reporting extract in one `recovery` schema, so record, clock and reporting copy moved together by construction. The objective is unchanged: about 3,000 restructure accounts a month reach the restructure process (NFR-005) and every approved plan needs one record and a running clock the day it is recorded (REQ-CHO-006, REQ-CHO-007, REQ-RDF-014, REQ-CWC-011).

The realignment separates the three things the monolith glued. The record is S2's, in `rwb_treatment` (DP-01; Architecture v5 slide 18). The clock is rwb-case's: a durable Temporal timer inside `CaseWorkflow`, projected behind the case timers operation, with `TimerScheduler`, JOB-05 and the TimerDue event retired (DP-10; ASM-4432). The reporting copy is rwb-source-data's, built from events with no data lake (DP-17). What is left to this story is the entity plus the plan facts that make the clock possible in its owner: a first due date, a number of installments, an installment amount and a paid counter. rwb-case never reads `rwb_treatment` and this service never reads `rwb_case`; the seam is one event keyed on the case, one read operation and a state that follows the case signals rather than driving them (DP-01, DP-11). Every value a business person may change is a listed value or a parameter, never a constant in code (DP-06, DP-07; FSD S2 BR-S2-001).

### 3. Preconditions

- RWB-P3-E2004-CON is published: it declares `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` with the payload this story produces, the treatment read it consumes, `rwb.payment.PaymentMissed.v1`, and the rule that no consumer re-words a message (DP-09, DP-11).
- The `rwb_treatment` schema and its login exist, and the service Flyway sequence is at the version that carries the platform library tables; this story adds one version and edits no applied one (DP-01, DP-15).
- The decision-record library RWB-PLT-E1027-CON and the outbox and inbox library RWB-PLT-TE006-CON are on the template; the WP lists no build dependency, so they are taken as present (ASM-4433; DP-03, DP-09).
- The parameters read (CURE_PERIOD_DAYS, `plan.warn-days`) and the reference-data read for the six lists of TSD S2 T3.2 reach the service through the client library (ASM-4433; DP-06, DP-07).
- The workflow kit runs on task queue `rwb-treatment` in namespace `rwb-recovery`, and `CaseWorkflow` starts `TreatmentWorkflow` as a child on that queue (ASM-4432; DP-10).
- The gateway-bff composite route that serves SCR-14 is published (DP-19; RWB-PLT-N001-CON), and feature switch `rwb.treatment.plan-model` exists and is off outside production until the migration is applied (ASM-4434).

### 4. Flow

1. rwb-case, or the officer's screen through the composite route, calls `POST /cases/{caseId}/treatments` with a `TreatmentRequest` and an `Idempotency-Key` (DP-13, DP-19).
2. The controller validates type, proposer, approval level, decision log entry and, for a plan, the first due date against the contract and the list values; a refusal under X1, X2 or X3 opens no transaction.
3. The service resolves the package version in force for the business date; with none it refuses with `NoPackageInForce` and assumes no default version or default timer (X6).
4. `recordTreatment` builds the row: the terms and plan facts of the command, `installments_paid` zero for a plan that has not started, `state` APPROVED and the standard record columns.
5. In one `rwb_treatment` transaction the service writes the `treatment` row, the local `decision_record` through `DecisionRecordWriter.record`, the `outbox_event` row of `rwb.treatment.TreatmentApproved.v1` and the inbox row of the `Idempotency-Key`; a failure of any rolls all back (DP-03, DP-09).
6. The relay publishes the event after the commit, keyed by `caseId`, with the treatment ID, the case ID, the type, the approval level, the decision log entry, the first due date, the installments and the offer amount (DP-14). rwb-case raises the INSTALLMENT_DUE timer from that due date and `plan.warn-days` and reports the route state on `rwb.case.CaseStateChanged.v1`; this service stores nothing about the clock (ASM-4432).
7. This service consumes the case and payment events through its inbox, deduplicated on the CloudEvents `id`, and applies the moves of section 9: BOOKED on the booking confirmation, RUNNING on PLAN_RUNNING or PLAN_CURE_PERIOD, BROKEN on PLAN_BROKEN, and the missed due date of `rwb.payment.PaymentMissed.v1` on the plan facts. A completion or a cancellation is written as the outcome and the outcome date; a row is never deleted and a state never moves backwards.
8. `GET /treatments/{treatmentId}` answers from `rwb_treatment` alone, with scope applied, and is the only path by which another service reads the record (DP-11). A repeated `POST` with the same `Idempotency-Key`, and a repeated event with the same CloudEvents `id`, return the first result and are counted; no second row, record or outbox row is written.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required field is missing (type, proposer, approval level, decision log entry, first due date for a restructure) | 422; nothing is written and no event is published | MSG-GEN-001 | AC3 |
| X2 | The decision log entry of the approval does not exist or names no approver | 422; the row is refused | MSG-GEN-001 | AC3 |
| X3 | The first due date is before the proposed date | 422 with both values named | MSG-GEN-003 | AC3 |
| X4 | The case is closed, or not in the route state the record needs | The write is refused and the case is left untouched | MSG-P3-005 | AC5 |
| X5 | The same `Idempotency-Key` or CloudEvents `id` arrives twice | The first answer or effect stands and the repeat is counted | None | AC3 |
| X6 | No package version is in force on the business date | `NoPackageInForce`; no row, no record, no outbox row; the case goes to the exception queue | MSG-P3-027 | AC9 |
| X7 | The local decision record cannot be written | The transaction rolls back; the caller retries with the same key | MSG-P7-003 | AC3 |
| X8 | A role without Treatment and offer R, or a treatment out of the caller's scope | 403, or 404 so existence is not disclosed | MSG-P4-002 | AC7 |
| X9 | The migration targets another schema, or a statement reaches another service's table | The schema lint and the boundary test fail the build | None | AC6, AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on Day 1 against the RWB-P3-E2004-CON fake, the platform library fakes and a PostgreSQL test container; needs no live rwb-case, rwb-payment or rwb-decision |
| Negotiable | Index names, the partial-index guard, the state vocabulary of the row and the flag name are this story's choice; fields, list values, messages and the event payload are fixed |
| Valuable | One record per approved plan in its owner, with the plan facts the clock needs, and no reader of another service's table |
| Estimable | One table, one migration, one repository, one service, two operations, one event producer, two event consumers |
| Small | Fits one sprint with its tests |
| Testable | Each criterion of section 7 is one automated test against the schema, the transaction, the payload or the operations; the clock, the rules and the reporting copy are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Treatment entity and plan timers data model

  Background:
    Given the business date is 2026-12-01
    Given schema rwb_treatment and its login exist and the service Flyway sequence is at the version that carries the platform library tables
    Given package "RESTRUCTURE" version "RES-2026.12" is in force with rows R-RES-25 and R-RES-27
    Given CURE_PERIOD_DAYS for "MORTGAGE" is 30 calendar days and plan.warn-days is 3

  Scenario: AC1 The treatment table is created in rwb_treatment with the fields of the module data model (new, D-RCV-60)
    Given the migration of this story has been applied
    When the treatment table is inspected
    Then it carries id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at, offer_amount, haircut_amount, installments, valid_until, approval_level, booked_at, outcome, outcome_at, nleads_ref, credit_result, credit_result_reason, credit_result_at, interest_rate, booking_difference, first_due_date, signature_status, installment_amount, installments_paid and installment_shortfall
    Then it carries the seven standard record columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then treatment_type is varchar(20) checked against LOV-TREATMENT, proposed_by varchar(10) against LOV-PROPOSER, approval_level varchar(4) against LOV-APPROVAL-LEVEL, outcome varchar(12) against LOV-TRT-OUTCOME, signature_status varchar(12) against LOV-TRT-SIGNATURE and credit_result varchar(10) against LOV-CREDIT-RESULT
    Then case_id, treatment_type, proposed_by, proposed_at and installments_paid are not null
    Then no member of those six lists is written in the migration as a constant

  Scenario: AC2 The plan facts are held on the row and one running plan per case is enforced (new, D-RCV-60)
    Given the treatment table and its indexes
    When the migration is inspected
    Then ix_treatment_case_id on case_id and ix_treatment_decision_log_id on decision_log_id exist
    Then ux_treatment_running_plan is a partial unique index on case_id where state = 'RUNNING'
    Then a second treatment row for the same case in state "RUNNING" is refused by the database
    Then first_due_date, installments, installment_amount, installments_paid and installment_shortfall hold the plan terms of DF-TRT-009 and DF-TRT-029 to DF-TRT-033
    Then the row holds no timer type, no timer expiry, no timer status and no key into a timer row, because the clock is not this service's (ASM-4432)

  Scenario: AC3 The approved write is one transaction of row, decision record, outbox row and inbox row (new, D-RCV-60)
    Given the treatment contract fake answers the create with a treatment ID
    When POST /cases/{caseId}/treatments is called with an Idempotency-Key for a restructure with 36 installments, offer amount 850000.00 and first due date 2026-12-31
    Then one treatment row in state "APPROVED" with booked_at empty, one decision_record row written through the RWB-PLT-E1027-CON writer, one outbox_event row for rwb.treatment.TreatmentApproved.v1 and one inbox row of the Idempotency-Key exist in rwb_treatment
    Then the decision record is written before the commit and carries the rule ID and the package version "RES-2026.12"
    Then the same Idempotency-Key sent again returns the first answer, writes no second row, record or outbox row, and the repeat is counted
    Then a forced failure of the decision record write leaves no treatment row and no outbox row

  Scenario: AC4 TreatmentApproved carries the terms the clock needs and no personal data (new, D-RCV-60)
    Given a treatment row in state "APPROVED" for case "RW-2026-000201"
    When the outbox relay publishes it
    Then rwb.treatment.TreatmentApproved.v1 is published on rwb.treatment.events.v1 in the CloudEvents 1.0 envelope with id, source, type, specversion, time, subject and datacontenttype
    Then the payload carries treatmentId, caseId, treatmentType, approvalLevel, decisionLogId, firstDueDate, installments and offerAmount, and the event is keyed by caseId
    Then the payload carries no name, address, identity number, contact point or account number
    Then the event is published only after the commit, and a rolled-back transaction publishes nothing

  Scenario: AC5 The state follows the case and payment signals and never drives them (new, D-RCV-60)
    Given a treatment in state "APPROVED" with no booked_at
    When rwb.case.CaseStateChanged.v1 reports route state BOOKED_IN_ALS_NLEADS for the case
    Then booked_at is set and the state is "BOOKED"
    When rwb.case.CaseStateChanged.v1 then reports PLAN_RUNNING
    Then the state is "RUNNING" and no clock, expiry or timer status is written by this service
    When rwb.payment.PaymentMissed.v1 reports a missed installment for the treatment
    Then the missed due date is recorded on the plan facts and the state stays "RUNNING", because the cure period is rwb-case's timer
    When the case signal then reports PLAN_BROKEN
    Then the state is "BROKEN"; a row is never deleted, and an outcome COMPLETED or CANCELED moves the state to "COMPLETED" or "CANCELED" instead

  Scenario: AC6 The migration is one version of this service's own sequence in one schema (new, D-RCV-60)
    Given the migration folder of rwb-treatment
    When the versions are inspected
    Then this story adds exactly one version after the platform baseline version and edits no applied version
    Then every statement is unqualified or qualified with rwb_treatment, and none names another Recovery schema
    Then the rollback script drops only the objects this version created
    Then the schema lint fails a migration that creates a table in a second schema

  Scenario: AC7 The treatment read answers from rwb_treatment alone (new, D-RCV-60)
    Given a treatment in state "APPROVED"
    When GET /api/recovery/treatment/v1/treatments/{treatmentId} is called by a role holding Treatment and offer R
    Then the answer carries id, caseId, decisionLogId, treatmentType, proposedBy, proposedAt, offerAmount, haircutAmount, installments, validUntil, approvalLevel, bookedAt, outcome and outcomeAt, with firstDueDate, installmentAmount, installmentsPaid and installmentShortfall
    Then the answer is served from rwb_treatment with no call to rwb-case, rwb-payment or rwb-decision
    Then a caller without Treatment and offer R is refused with MSG-P4-002, and a treatment out of scope answers 404 with MSG-P4-003

  Scenario: AC8 The retired timer mechanism is absent from the schema and the code (new, D-RCV-60)
    Given the published schema, the migration and the component scan of rwb-treatment
    When the absence test runs
    Then rwb_treatment holds no timer table, no timer type column, no timer status column and no reference to a timer row of rwb_case
    Then no TimerScheduler port, no Quartz trigger, no JOB-05 entry, no timer-check task queue and no TimerDue event or topic is declared
    Then no data-lake, Power BI or extract operation is declared, because the DP04 copy is built by rwb-source-data from the events
    Then the absence test fails a build that declares any of them

  Scenario: AC9 No package version in force is a refusal and never a default (new, D-RCV-60)
    Given no RESTRUCTURE version is IN_FORCE on 2026-12-01
    When a plan treatment is written or a plan fact is changed on that business date
    Then NoPackageInForce is raised with MSG-P3-027 naming package "RESTRUCTURE" and the business date only
    Then no treatment row, no decision record and no outbox row are written
    Then the case is placed in the exception queue for role "RW-TEAMMGR" with the gap, and no default version, terms or timer is assumed
```

These nine criteria are new for the split and test only the data model this story owns; the fourteen legacy criteria of RWB-E2-004 and their sixteen test cases stay with RWB-P3-E2004-APP (ASM-4435; GAP-2687).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every approved offer has exactly one `treatment` row with its type, terms, approval level, the approval's decision log entry and its outcome | REQ-CHO-006; LOV-TREATMENT |
| BR2 | A restructure needs installments above zero and a first due date on or after the proposed date | R-RES-25 (condition `first_due_date` set) |
| BR3 | The plan facts a clock needs are the first due date, the installments, the installment amount and the paid counter; they are held here and published, and the clock is rwb-case's | FSD S2 A2.10.3.1; ASM-4432 |
| BR4 | The cure period and the warning are data: CURE_PERIOD_DAYS per product and `plan.warn-days` from the parameters contract | R-RES-27; DP-06 |
| BR5 | A decision that cannot be recorded does not proceed: row, record and outbox row commit or roll back together | R-UNI-39; CTL-06; DP-03 |
| BR6 | A repeated key is ignored and counted, on the request and on the consumed event | R-UNI-40; DP-09 |
| BR7 | The state follows the case and payment signals; this service never moves a case state and never writes a timer | DP-01, DP-10; ASM-4432 |
| BR8 | One state vocabulary: APPROVED when no booking exists, BOOKED, RUNNING, BROKEN, COMPLETED and CANCELED from the outcome | REQ-RDF-014; LOV-TRT-OUTCOME |
| BR9 | No package version in force is a refusal, never a default; every plan write stores the rule ID and the package version | R-UNI-41; D-RCV-36 T7 |
| BR10 | No list value and no parameter is written in code or in a migration; each is read with its version | FSD S2 BR-S2-001; DP-06, DP-07 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| None | Treatment recorded | approval in force and validation passes | APPROVED |
| APPROVED | Booking confirmed | booked_at written from the case signal | BOOKED |
| BOOKED | Plan started | case route state PLAN_RUNNING or PLAN_CURE_PERIOD | RUNNING |
| RUNNING | Plan broken | case route state PLAN_BROKEN | BROKEN |
| RUNNING, BROKEN | Outcome recorded | outcome COMPLETED | COMPLETED |
| APPROVED, BOOKED, RUNNING | Outcome recorded | outcome CANCELED or DECLINED | CANCELED |

A row is never deleted and a state never moves backwards. The plan clock has no state here: its INSTALLMENT_DUE and CURE_PERIOD timers live in `CaseWorkflow` and are read behind the case timers operation (ASM-4432).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | Creates and reads the treatment (Treatment and offer CRUA, TSD S2 T6.1) |
| RW-CASEOWN, case owner | Reads the treatment and its plan facts (CRU) |
| RW-SPECIAL, hardship and vulnerability specialist | Creates and reads the treatment (CRU) |
| RW-TEAMMGR, team manager | Reads the treatment; receives the exception row of a refused plan (R) |
| rwb-case, through its service identity | Reads the treatment and consumes the announcement (Treatment and offer R) |
| rwb-source-data, through its service identity | Consumes the treatment events for the DP04 copy; no table access |

The approval of the terms is made before this story runs, at the level the delegation of authority sets; this story stores the approval level and the decision log entry it is given and approves nothing itself.

### 11. Data

| BR Field ID | Table | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 to DF-TRT-014 | treatment | type, terms, approval level, booking and outcome | Write |
| DF-TRT-023 to DF-TRT-028 | treatment | NLEADS and credit references, interest rate, booking difference | Write |
| DF-TRT-029 | treatment | first_due_date | Write |
| DF-TRT-030 to DF-TRT-033 | treatment | signature status, installment amount, installments paid, shortfall | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record | the local record of the write with the rule ID and the package version | Write, same transaction (DP-03) |
| — | outbox_event, inbox_event | the announcement row and the dedupe row | Write, same transaction (DP-09) |
| DF-CAS-001, DF-CAS-003, DF-CAS-005, DF-CAS-007 | recovery_case of rwb_case | id, product group, status, route state | Read only as the case signal; no table access (DP-01, DP-05) |
| DF-REF-002, DF-REF-003, DF-REF-296 | rule_row of rwb-decision | rule ID, rule version, package version | Read only through the rule-package and catalogue reads |
| — | dp_treatment | the DP04 treatment copy | Not owned: built by rwb-source-data from the events (GAP-2687) |

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/treatment/v1`; owner rwb-treatment; rights from TSD S2 T6.1; every operation applies scope and answers the platform error envelope.

| Operation | Purpose | Right | Notes |
|---|---|---|---|
| POST /cases/{caseId}/treatments | Write the treatment and its plan facts | Treatment and offer C | `Idempotency-Key` required; 201 with the Treatment resource; 409 on a repeat, 422 on a value outside its list |
| GET /treatments/{treatmentId} | Read the treatment with its terms, plan facts and outcome | Treatment and offer R | The only read another service uses; 404 out of scope, so existence is not disclosed |

`PATCH /treatments/{treatmentId}` and `POST /treatments/{treatmentId}/submit` are provided by this service but first used in Epic 3; this story publishes the two rows above and the E3 slices widen the document additively (section 19).

#### 12.2 REST operations consumed

| Operation | Owner | Purpose | Budget |
|---|---|---|---|
| the parameters read for CURE_PERIOD_DAYS and `plan.warn-days` | rwb-case (P3) | cure days and warning days as data | one hop, 2 s, GET retried once, breaker (DP-06, DP-11); operation name Not specified in the source documents (GAP-2688; ASM-4433) |
| the reference-data read for the six lists of section 3 | rwb-case (P3) | list members and their version | one hop, 2 s, GET retried once, breaker (DP-07, DP-11); operation name Not specified in the source documents (GAP-2688; ASM-4433) |

#### 12.3 Events published

| Event | Topic | Key | Payload used |
|---|---|---|---|
| rwb.treatment.TreatmentApproved.v1 (EV-10) | rwb.treatment.events.v1, with the retry and `.dlt` topics | caseId | treatmentId, caseId, treatmentType, approvalLevel, decisionLogId, firstDueDate, installments, offerAmount |
| rwb.decision-record.DecisionRecorded.v1 | rwb.decision-record.v1 (shared) | decisionRecordId | ruleId, ruleVersion, finalCall, decidedAt, written by the DP-03 library in the caller's transaction |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| rwb.case.CaseStateChanged.v1 | rwb.case.events.v1 | rwb-case (P3) | the route state that moves the treatment state; deduped on the CloudEvents id (DP-09) |
| rwb.payment.PaymentMissed.v1 | rwb.payment.events.v1 | rwb-payment (P8) | the missed due date recorded on the plan facts |
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | rwb-decision (P7) | the package version kept for the next write; its absence refuses with NoPackageInForce (DP-04) |

#### 12.5 Workflows and activities

| Element | Kind | Purpose |
|---|---|---|
| TreatmentWorkflow | Child workflow of CaseWorkflow, task queue rwb-treatment, namespace rwb-recovery | Runs the treatment stage; started by rwb-case (ASM-4432) |
| recordTreatment | Activity | Writes the row, the decision record, the outbox row and the inbox row in one transaction |
| applyCaseSignal | Activity | Applies a case or payment signal to the state and the plan facts, idempotently |

#### 12.6 Schedules

None. No Quartz trigger, no JOB-05 timer check and no Temporal Schedule is declared: the plan clock is a durable timer inside `CaseWorkflow` of rwb-case and its expiry stays a fact of that history (DP-10; GAP-2687).

#### 12.7 Tables owned

| Table | Schema | Notes |
|---|---|---|
| treatment | rwb_treatment | DF-TRT-001 to DF-TRT-033 plus the seven standard columns; ix_treatment_case_id, ix_treatment_decision_log_id, ux_treatment_running_plan |
| decision_record | rwb_treatment | Platform library table of DP-03, created by the baseline version |
| outbox_event, inbox_event | rwb_treatment | Platform library tables of DP-09; dedupe on the CloudEvents id and the `Idempotency-Key` |
| timer | not owned | rwb_case's projection behind the case timers operation; this service holds no timer row and no key into it (ASM-4432) |

#### 12.8 Contract fakes

| Fake | Answers | Used by |
|---|---|---|
| treatment fake | POST /cases/{caseId}/treatments and GET /treatments/{treatmentId} of section 12.1 | the app tests of this story and the S2 siblings |
| case-signal fake | rwb.case.CaseStateChanged.v1 payloads with a route state, a rule ID and a version | AC5, TC-S2-E2004-APP-06 |
| payment-signal fake | rwb.payment.PaymentMissed.v1 with treatmentId, dueDate, amountDue and businessDate | AC5, TC-S2-E2004-APP-06 |
| package fake | rwb.decision.RulePackageInForce.v1 and the refusal with NoPackageInForce | AC9, TC-S2-E2004-APP-10 |
| parameters and reference-data fake | CURE_PERIOD_DAYS 30, plan.warn-days 3 and the six lists of section 3 | AC1, AC5 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST provided | 2 | POST /cases/{caseId}/treatments, GET /treatments/{treatmentId} |
| REST consumed | 2 | the parameters read and the reference-data read of rwb-case, one hop, 2 s (DP-06, DP-07, DP-11) |
| Kafka published | 2 | rwb.treatment.TreatmentApproved.v1, rwb.decision-record.DecisionRecorded.v1 |
| Kafka consumed | 3 | rwb.case.CaseStateChanged.v1, rwb.payment.PaymentMissed.v1, rwb.decision.RulePackageInForce.v1 |
| Temporal | 3 | TreatmentWorkflow, recordTreatment, applyCaseSignal on task queue rwb-treatment |
| File | None | no file in or out; the DP04 copy is built by rwb-source-data from the events |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `record` for the entity and `plan` for the plan facts.

| Component | Type | Responsibility |
|---|---|---|
| TreatmentEntity | Entity | Maps `treatment` with the standard columns and the plan facts |
| TreatmentRepository | Repository | Reads and writes `treatment` only |
| TreatmentRecordService | Service | Validates the command, resolves the package version, writes row, record and outbox row in one transaction |
| TreatmentController | REST | The two operations of section 12.1, the problem mapping and the `Idempotency-Key` |
| TreatmentApprovedPublisher | Outbox producer | Builds rwb.treatment.TreatmentApproved.v1 with the payload of section 12.3 |
| TreatmentSignalListener | Listener | Consumes the three events of section 12.4 through the inbox and applies the moves of section 9 |
| TreatmentState | Domain | The vocabulary of BR8 and the allowed moves of section 9 |

**Database.** One version on the service sequence, `V<next>__rwb_treatment_treatment.sql`: `treatment` from DF-TRT-001 to DF-TRT-033 with the seven standard columns, the six list checks read from reference data, `ix_treatment_case_id`, `ix_treatment_decision_log_id` and the partial unique index `ux_treatment_running_plan` on `case_id` where `state = 'RUNNING'` (DP-15; ASM-4434). The legacy `timer` columns, `ix_timer_treatment_id` and `ix_timer_plan_due` are not created (ASM-4432). The six lists of TSD S2 T3.2 are reference-data rows with a version; CURE_PERIOD_DAYS per product and `plan.warn-days` are parameter rows (values per DL22; `plan.warn-days` assumed 3); package RESTRUCTURE rows R-RES-25 and R-RES-27 come from rwb-decision and are never edited here (DP-06, DP-07).

**Build steps**

1. Write the migration; prove the table, the columns, the two indexes and the partial unique index against a PostgreSQL test container.
2. Build the entity, the repository and the schema lint that refuses a second schema and another service's table.
3. Build the service with the validations of X1 to X4, the refusal of X6 and the one transaction of AC3.
4. Build the controller for the two operations with scope, rights, `Idempotency-Key` and the problem mapping of section 14.
5. Build the outbox producer, the signal listener with the inbox dedupe and the moves of section 9, and prove that no personal field can enter the payload.
6. Add the absence test of AC8 and the tests of section 16 with a controlled clock.

**Feature flag.** `rwb.treatment.plan-model` (ASM-4434). Off: the treatment is recorded without the plan facts and no announcement is published.

**Done when.** The tests of section 16 pass; a run of 50 synthetic plans leaves 50 treatment rows with their plan facts, 50 decision records, 50 outbox rows and 50 published announcements, and no row, column or statement outside `rwb_treatment`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field or the decision log entry is missing | Enter {field}. |
| MSG-GEN-003 | The first due date is before the proposed date | {field} cannot be before {other}. |
| MSG-P3-005 | The case is closed, or not in the state the record expects | This case cannot move to {state} from {current}. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-027 | No package version is in force | The rule version was refused at the {check} check: {detail}. |
| MSG-P4-002 | A role without Treatment and offer R or C calls an operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The treatment does not exist or is out of scope | The record was not found. |

For MSG-P3-027 the {check} is "no package in force" and the {detail} names the package code and the business date only, never a case fact. No consumer re-words a message text.

### 15. Screens and states

No new screen. SCR-14 Treatment record reads the row through the composite route and shows the state APPROVED, BOOKED, RUNNING, BROKEN, COMPLETED or CANCELED with the plan facts; the plan timers themselves are shown on SCR-03 Case record from the case timers operation, not from this service (DP-19; ASM-4432). A record refused under X4 or X6 shows on the case exception queue, SCR-09.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E2004-APP-01 | AC1 | Component | Migration on a PostgreSQL test container; the twenty-five fields, the seven standard columns and the six list checks |
| TC-S2-E2004-APP-02 | AC2 | Component | Two rows for one case in state RUNNING; the second refused |
| TC-S2-E2004-APP-03 | AC3 | Component | Restructure, 36 installments, 850000.00, first due date 2026-12-31, `Idempotency-Key` sent twice |
| TC-S2-E2004-APP-04 | AC3, BR5 | Component | Decision-record writer forced to fail; no row and no outbox row |
| TC-S2-E2004-APP-05 | AC4 | Contract | The payload against the RWB-P3-E2004-CON event schema, plus the personal-data scan |
| TC-S2-E2004-APP-06 | AC5 | Component | Case signal BOOKED_IN_ALS_NLEADS, then PLAN_RUNNING, then PaymentMissed, then PLAN_BROKEN |
| TC-S2-E2004-APP-07 | AC6 | Component | Flyway report of the service sequence; schema lint over the migration and the code |
| TC-S2-E2004-APP-08 | AC7 | Component | Read by RW-RESTRUCT, then by RW-PHONECOL without the right, then a treatment out of scope |
| TC-S2-E2004-APP-09 | AC8 | Component | Component and schema scan for the retired timer elements and the data-lake extract |
| TC-S2-E2004-APP-10 | AC9, BR9 | Component | No RESTRUCTURE version in force on 2026-12-01 |

The sixteen legacy test cases TC-E2-004-01 to TC-E2-004-16 test the fourteen legacy criteria and stay with RWB-P3-E2004-APP, the primary slice; they are not re-tagged here (ASM-4435).

### 17. Guardrails

- No business value in code or in a migration: periods, warning days and list members are parameter and reference-data rows with a version (DP-06, DP-07).
- No personal data in events, workflow inputs, tests or logs beyond the identifiers of the payload; amounts and names in tests are synthetic.
- ACE data only through the owner's contract or the `v_ace_*` views of rwb-source-data; this service reads no ACE table and no view of another module (DP-05).
- No read of another service's table and no key into another service's schema: the case arrives as a signal, the treatment only through section 12.1 (DP-01, DP-11).
- The decision record is written before the commit, never after; a record that cannot be written refuses the write (DP-03; BR5).
- No timer is written, scheduled or cancelled here; the clock belongs to `CaseWorkflow` of rwb-case (DP-10; ASM-4432).
- The row is never deleted, a cancellation is an outcome, and the state never moves backwards.
- The rule package is loaded and approved in rwb-decision; this service reads its version and never a rule source or a workbook (DP-04).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record for every offer with type, terms, approval and outcome | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-S2-E2004-APP-01, TC-S2-E2004-APP-03, TC-S2-E2004-APP-08 |
| REQ-CHO-007 | Plan timers run from the treatment; a missed payment raises an event | Business Requirements Epic 2, section 3.3; Program, section 5.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25, R-RES-27, R-UNI-39, R-UNI-40 | TC-S2-E2004-APP-04, TC-S2-E2004-APP-05, TC-S2-E2004-APP-06, TC-S2-E2004-APP-09 |
| REQ-RDF-014 | Stage 2 data products for plans and treatments exist before the first treatment | Business Requirements Epic 2, section 4; Program, section 5.1 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | None | TC-S2-E2004-APP-05 |
| REQ-CWC-011 | The warning is raised before the due date from a parameter | Business Requirements Epic 2, section 3.3 | FEAT-CHO-06 | 7.3 Negotiate settlement or deed in lieu | R-RES-25 | TC-S2-E2004-APP-02, TC-S2-E2004-APP-06 |

The fourteen legacy criteria AC1 to AC14 are owned and traced by RWB-P3-E2004-APP; the plan clock, the DP04 copy, the rule package and the rights are traced in their owner stories (GAP-2687; ASM-4435).

### 19. Out of scope

- The plan clock, its INSTALLMENT_DUE and CURE_PERIOD timers, the `timer` projection and the route states, which are rwb-case's (RWB-P3-E2004-APP).
- The RESTRUCTURE package, its rows, its versions and its catalogue answers (RWB-P7-E2004-APP), and the DP04 treatment copy and its nightly build (rwb-source-data).
- The offer builder, the terms change, the submission for approval and the settlement range, which are the Epic 3 slices of this service (RWB-S2-E3001-APP onwards).
- The booking confirmation and booked at date (RWB-S2-E2007-APP), the payment matching that raises PaymentMissed (RWB-S2-E2008-APP) and the broken-plan handling after the cure period (R-RES-29 to R-RES-32).
- The roles, rights and scope data (rwb-access), the screens and composite routes (DP-19) and the platform deployment of the schema and login.

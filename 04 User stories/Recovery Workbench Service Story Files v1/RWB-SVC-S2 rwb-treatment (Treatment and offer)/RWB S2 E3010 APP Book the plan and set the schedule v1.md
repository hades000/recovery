# RWB-S2-E3010-APP Book the plan and set the schedule

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-010 for rwb-treatment (S2, Treatment and offer). The booking step leaves the monolith's in-process stage of `rwb-case` and becomes the booking branch of `TreatmentWorkflow`, the stage child that `CaseWorkflow` starts on task queue `rwb-treatment` (DP-12); the booking acknowledgement arrives as `rwb.payment.TreatmentBooked.v1` (EV-11) on the service's own inbox and is decided by the BOOKING_MATCH package in force instead of an in-process callback; the schedule is written on `treatment` in `rwb_treatment` and the booking facts are read from `v_ace_plan`, `v_ace_payment` and `v_ace_account`, never copied (DP-01, DP-05); the plan timers become durable Temporal timers inside the workflow instead of `timer` rows, which are rwb-case's; the local decision record is written in the same transaction through RWB-PLT-E1027-CON (DP-03); the booking and schedule body is published by RWB-S2-E3010-CON under base `/api/recovery/treatment/v1` (DP-13); SCR-14 is reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-U |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3010-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the Workbench to send the plan to NLEADS and ALS through the outbound interface and set the payment schedule and the plan timers from the booking facts ACE holds**, so that **restructures and settlements reach booking in days**.

This is the application slice of legacy RWB-E3-010. It owns:

- the three legacy acceptance criteria the Work Package assigns to this story — AC2 (R-RES-22), AC3 (R-RES-25) and AC4 (not recorded) — copied verbatim with their origin tag, and the data rows, the messages and the two rules they depend on;
- the booking branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery` — the stage child that `CaseWorkflow` of rwb-case starts for a restructure, with the four steps of every stage: receive, ask Drools, record and apply in one transaction, then wait (DP-12; Architecture v5 slide 18, "TMP TreatmentWorkflow · settlement and DIL sagas"; Temporal and Drools Design slide 18, steps 5 "Customer signs, ops books — R-RES-16/21/22 · EV-11" and 6 "Payment plan timers — R-RES-25");
- the booking acknowledgement as an event of rwb-payment: `rwb.payment.TreatmentBooked.v1` (EV-11) is consumed through this service's inbox, because Architecture v5 slide 42 names rwb-treatment as a consumer of EV-11 and the Temporal and Drools Design names BOOKING_MATCH, "booking confirmed", as the Drools package that decides it (Architecture v5 slide 42 event 11; Temporal and Drools Design slides 13 and 18);
- the schedule written on `treatment` in schema `rwb_treatment` — `booked_at`, `nleads_ref`, `first_due_date`, `installment_amount`, `installments`, `installments_paid` and `booking_difference` — inside the apply step of the workflow (DP-01; TSD S2 T3.1);
- the booking facts read from the SELECT-only ACE views `v_ace_plan`, `v_ace_payment` and `v_ace_account` at the moment of confirmation, copied nowhere and joined to no table of another service (DP-05; D-RCV-35; ADR-010);
- the plan timers of R-RES-25: durable timers inside `TreatmentWorkflow`, one per due date of the schedule it sets, started in the same apply step that sets the schedule, with no `timer` row written (ASM-4380; DP-10);
- the stage outcome of R-RES-22 and R-RES-25 reported to the parent `CaseWorkflow`, which moves the case to `BOOKED_IN_ALS_NLEADS` and then to `PLAN_RUNNING` (ASM-3062; DP-01);
- the local decision record of the booking and of the schedule, written in the same transaction as the schedule columns through the library of RWB-PLT-E1027-CON (DP-03; ADR-022).

It does not own: AC1 of the legacy story, the end-to-end path from the approved treatment through NLEADS and ALS to a running plan, which the Work Package assigns to no story of this pair and which is carried by the wave 2 integration harness (section 18); the published booking and schedule body, which is RWB-S2-E3010-CON; the plan offer, its band and its offer clock, which are RWB-S2-E3004-APP and RWB-S2-E3004-CON; the treatment record and its states, which are RWB-S2-E3001-APP and its contract; the broken-plan detection and the cure period, which are RWB-E3-011's stories; the booking itself in ALS and NLEADS, which operations perform and which the FSD keeps out of scope (FSD S2 A1.1); the posting to GL, which is rwb-payment's; the case status, the assignment and the `timer` table, which are rwb-case's (DP-01); the ACE batch, its load and the `v_ace_*` views behind it, which are rwb-source-data's (DP-05); the decision-record library, which is RWB-PLT-E1027-CON; and the real cross-service proof, which is the wave 2 integration harness.

### 2. Business rationale

The FSD measures S2 by one number: restructure turnaround of 5 days, measured from the decision log and the Workbench records, reviewed monthly, against today's 23 to 26 days tracked by hand (FSD S2 v3, section A2.10.1). Booking is where that number is either banked or lost: until the plan is booked in ALS and NLEADS, the schedule is set and the plan clock runs, nothing the officer agreed on the offer exists in the systems of record. Two requirements carry the value. REQ-S2-008 asks that booked terms, settled accounts and released collateral be posted to their systems of record without re-keying. REQ-CHO-008 asks that booked terms be recorded on the case and that the booking be confirmed from the next business date's ACE account data in `v_ace_account` — which is exactly the read path this story takes, and the reason no account or payment copy exists in the Workbench (D-RCV-35 U1 and U4; ADR-010).

In the monolith this step was an in-process stage: one schema, one `recovery_case` status write, one callback from the booking, one `timer` row per clock and one decision log table. Architecture v5 moves all five facts. The stage becomes a child workflow of the service that owns treatments and plan timers (Architecture v5 slide 18 and 41, "S2 · rwb-treatment … treatments, contracts, settlement and deed-in-lieu agreements, plan timers"); the case status stays rwb-case's and is moved by the parent when this stage reports its outcome (ASM-3062); the callback becomes the business event `rwb.payment.TreatmentBooked.v1`, whose consumers the catalogue names as rwb-case and rwb-treatment (Architecture v5 slide 42 event 11); the clock becomes a durable timer, because the catalogue retires `TimerDue` as "durable timer — retired: timer inside the workflow" (Architecture v5 slide 42 event 18); and the decision record becomes a local row written with the change in one transaction (DP-03).

The third fact is the one this story cannot move: the booking instruction itself. The FSD keeps booking in the core bank out of scope and says the officer does it, and TSD S2 T5.1 gives INT-03 as "Booked by the officer; confirmed on the next day's load" and INT-26 as "Submitted by the officer in NLEADS" (FSD S2 A1.1; TSD S2 T5.1). Legacy AC1 asks the Workbench to send the agreed terms to NLEADS and ALS through the outbound interface, and AC1 is not assigned to this story; what remains here is the confirmation, the schedule and the clocks. The target therefore reads the outbound interface as the one path S2 has outside the 19 services — the ACE common module, reached by Temporal Nexus, which Architecture v5's connection matrix gives S2 as its only external cell — and records the reading as a conflict with the FSD and TSD wording (GAP-2667; ASM-4382; Architecture v5 slide 13).

### 3. Preconditions

- RWB-S2-E3010-CON is published: the `PlanBooking` element, its required and optional properties, its validation against the `treatment` field set of TSD S2 T3.1, the acknowledgement rule of R-RES-22, the timer rule of R-RES-25, the versioning rule and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, the refusal `MSG-P7-009`, the failure `MSG-P7-003`, and the DDL template of `decision_record` applied by this service's own Flyway sequence in `rwb_treatment` (DP-03, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14, one hop per call (DP-19).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with the 33 fields of TSD S2 T3.1 and the seven standard columns of T3.0, and the `rwb_treatment` login holds rights in that schema only (DP-01, DP-02).
- The SELECT-only ACE views `v_ace_plan`, `v_ace_payment` and `v_ace_account` are readable by the `rwb_treatment` login and are owned by rwb-source-data; the booking facts of TSD S2 T3.1 sources are read there and stored nowhere (DP-05; ADR-010).
- The BOOKING_MATCH package and its version are the ones announced by `rwb.decision.RulePackageInForce.v1` (EV-30), and the embedded Drools runtime is the service template's wave-0 capability, so this story adds no Drools dependency of its own (ASM-4379; Temporal and Drools Design slides 13, 15 and 18).
- The restructure stage is open: `TreatmentWorkflow` is running for a case whose route decision is R1 and whose offer was signed and routed to operations, so the case status the parent reports is `WITH_OPS_BOOKING` (TSD S2 T4 R-RES-16 and R-RES-22; ASM-3062).
- The event `rwb.payment.TreatmentBooked.v1` is published by rwb-payment with the case key and the CloudEvents envelope, and this service's inbox dedupes it by cloud event id (DP-09; Architecture v5 slide 42 event 11 and its notes).
- The access guard, the outbox and inbox library and the workflow kit are the platform library's; the capability area and the right are declared here and checked there (ASM-3064; DP-19).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3010-CON when its tests pass, and this story runs in Draft (realignment v1) until it does.

### 4. Flow

1. rwb-payment publishes `rwb.payment.TreatmentBooked.v1` (EV-11) once the booking it matched is recorded on its side; the event carries the case key and identifiers, no personal data (Architecture v5 slide 42 event 11; DP-09).
2. The inbox of the outbox library receives the event, dedupes it by cloud event id, and signals the running `TreatmentWorkflow` of that case on task queue `rwb-treatment`; a redelivery signals nothing twice (DP-09; Temporal and Drools Design slide 13).
3. Step 1, receive: the workflow takes the case status and the booking identifiers from the signal. It reads no `recovery_case` row and no other service's table (DP-01; ASM-3062).
4. Step 2, ask Drools: the `EvaluateRules` activity runs the BOOKING_MATCH package in force, at the version announced by EV-30, under 300 ms in the owning service (ASM-4379). R-RES-22 fires on `WITH_OPS_BOOKING` with `BOOKING_CONFIRMED` when ALS and NLEADS both acknowledge, and answers `BOOKED_IN_ALS_NLEADS` (TSD S2 T4 R-RES-22; Routing Logic v4 R-RES-22).
5. `readBookingFacts` activity: reads the booking date and the plan reference from `v_ace_plan`, the schedule basis from `v_ace_payment` and the account identifiers from `v_ace_account`, SELECT only, within the batch freshness rule VR-S2-010-1; nothing is copied into a Workbench table (DP-05; D-RCV-35; FSD A2.10.3.1).
6. Step 3, record and apply: `setPlanSchedule` writes the schedule on the `treatment` row — `booked_at` from the plan, `nleads_ref` from the acknowledgement, `first_due_date`, `installment_amount`, `installments`, `installments_paid` and `booking_difference` — and validates the body against RWB-S2-E3010-CON (DP-01; TSD S2 T3.1 DF-TRT-009, -012, -023, -028, -029, -031, -032).
7. `recordAndApply` activity, in one transaction: the decision record of R-RES-22 is written through `DecisionRecordWriter.record(DecisionRecord)` with `MANDATORY` so it joins this transaction and opens none, its `DecisionRecorded` event is written to this service's outbox by the library, and the stage outcome is reported so the parent moves the case to `BOOKED_IN_ALS_NLEADS` (DP-03, DP-09; ADR-022).
8. R-RES-25 fires on `BOOKED_IN_ALS_NLEADS` with `SCHEDULE_SET` when `first_due_date` is set: the plan timers start and the plan moves to running (TSD S2 T4 R-RES-25; Routing Logic v4 R-RES-25).
9. The plan timers are durable timers inside `TreatmentWorkflow`, one per due date of the schedule just written, started in the same apply step; the workflow waits on the earliest one or on the next signal, and no `timer` row is written (ASM-4380; DP-10; Temporal and Drools Design slide 18 step 6).
10. The stage outcome of R-RES-25 is reported in the same transaction, and the parent moves the case to `PLAN_RUNNING` (ASM-3062).
11. The officer and the case owner see the booked schedule on SCR-14 Treatment record through the gateway-bff composite route, one hop, 2 s timeout (DP-19; DP-13).
12. A missed payment after booking is EV-12 and belongs to the broken-plan story of the same legacy family; this stage has already handed the plan clock over and takes no part in the cure period (Temporal and Drools Design slide 18 step 7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right in capability area Treatment and offer reads the booked schedule | 403 before any read of the treatment; the refusal is the guard library's and is logged by it | MSG-P4-002 | TC-E3-010-05 |
| X2 | The decision record cannot be written | The transaction rolls back, the schedule columns are not stored, the plan timers are not started, and the user sees MSG-P7-003 | MSG-P7-003 | AC4, TC-E3-010-04, TC-E3-010-06 |
| X3 | The ACE data behind `v_ace_plan` or `v_ace_payment` is older than the freshness rule | The confirmation is refused, the case stays in `WITH_OPS_BOOKING` and the date is named | MSG-P1-001 | TC-S2-E3010-CON-04 |
| X4 | ALS or NLEADS has not both acknowledged | R-RES-22 does not fire; the case stays in `WITH_OPS_BOOKING` and the booking stays with operations | None | TC-S2-E3010-CON-03 |
| X5 | `first_due_date` is absent from the plan facts | R-RES-25 does not fire; the case stays in `BOOKED_IN_ALS_NLEADS` and no clock starts | None | TC-S2-E3010-CON-02 |
| X6 | The booking facts disagree with the agreed terms | `booking_difference` records the difference and the booking is held in `WITH_OPS_BOOKING` for operations | None | TC-S2-E3010-CON-01 |
| X7 | EV-11 is redelivered, or two events for one booking arrive | The inbox dedupes by cloud event id: one schedule, one decision record and one timer set | None | TC-E3-010-02 |
| X8 | A field of the record is refused by the library | Nothing changes and the field is named; the case stays where it was | MSG-P7-009 | TC-S2-E3010-CON-05 |

X1 and X2 are the exception paths of RWB-E3-010 carried onto the split; X3 to X8 are the paths that the event trigger, the published `PlanBooking` body and the `MANDATORY` record add (GAP-2665; ASM-4380). R-RES-23 (a rejected booking) and R-RES-24 (a missing NLEADS callback) both keep the case in `WITH_OPS_BOOKING` and belong to the operations queue, so this stage takes no branch for them (Routing Logic v4 R-RES-23 and R-RES-24).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3010-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON with their fakes, on `treatment` in its own schema and the read-only `v_ace_*` views; needs no live rwb-payment, no live rwb-case and no live ALS to start |
| Negotiable | The activity names, the timer structure and the metric and log fields are this story's choice; the schedule columns, the two rules, the `MANDATORY` record and the no-copy rule for the ACE facts are fixed |
| Valuable | The plan reaches booking, the schedule is set and the plan clock runs, with the booking date provable from the record, which is the 5-day turnaround of the FSD metric |
| Estimable | One workflow branch, three activities, one repository, one timer set and one test set |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, EV-11 events and view fixtures through the contract fakes, plus one component test of the access answer and the record rollback |

### 7. Acceptance criteria

```gherkin
Feature: Book the plan and set the schedule

  Scenario: AC2 Rule R-RES-22 (legacy RWB-E3-010 AC2)
    Given the rwb-case contract mock returns case status WITH_OPS_BOOKING
    Given a case in state WITH_OPS_BOOKING
    When booking confirmed
    Then record the booking date from v_ace_plan and set the payment schedule from v_ace_payment
    Then the case moves to BOOKED_IN_ALS_NLEADS

  Scenario: AC3 Rule R-RES-25 (legacy RWB-E3-010 AC3)
    Given the rwb-case contract mock returns case status BOOKED_IN_ALS_NLEADS
    Given a case in state BOOKED_IN_ALS_NLEADS
    When schedule set
    Then start the plan timers and move the plan to running
    Then the case moves to PLAN_RUNNING

  Scenario: AC4 Not recorded (legacy RWB-E3-010 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line and value above is copied character for character, including the legacy repetition of `Then`; what changes is where it runs, who owns each fact and how it is reached. The two case states of AC2 and AC3 are rwb-case's and reach the stage on the case signal the parent `CaseWorkflow` forwards (EV-29); the `rwb-case contract mock` line stands for the case-status answer on that signal, not for a REST call and not for a table read, and the status move is the parent's (ASM-3062; Architecture v5 slide 43 event 29; Temporal and Drools Design slide 13). "Booking confirmed" of AC2 is EV-11 `rwb.payment.TreatmentBooked.v1` decided by the BOOKING_MATCH package in force, whose version arrives on EV-30, and its outcome is R-RES-22 (Architecture v5 slide 42 event 11; Temporal and Drools Design slide 18). `v_ace_plan` and `v_ace_payment` of AC2 are the SELECT-only ACE views read under DP-05; the booking date is `booked_at` (DF-TRT-012) and the schedule is the `treatment` columns of section 11, not a Workbench copy of the plan or the payments (DP-05; D-RCV-35; ADR-010). "The plan timers" of AC3 are durable timers inside `TreatmentWorkflow`, one per due date, with no `timer` row, because that table is rwb-case's and the catalogue retires `TimerDue` (ASM-4380; Architecture v5 slide 42 event 18). The decision log of AC4 is the local `decision_record` written with `MANDATORY`, failing with MSG-P7-003; `decision_log_entry` is P7's central ledger and is neither written nor read here (DP-03, DP-01).

AC1 of the legacy story — the approved treatment taken through NLEADS and ALS to a running plan, with the decision log row carrying the rule version — is not repeated here: the Work Package assigns AC2, AC3 and AC4 to this story and AC1 to no story of this pair, and its end-to-end path belongs to the wave 2 integration harness (section 18; WP B2-S2-005).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On `WITH_OPS_BOOKING` with `BOOKING_CONFIRMED`, when ALS and NLEADS both acknowledge, the booking reference is recorded and the payment schedule is set; the case moves to `BOOKED_IN_ALS_NLEADS` | TSD S2 T4 R-RES-22; Routing Logic v4 R-RES-22; FSD A2.10.3.1 |
| BR2 | On `BOOKED_IN_ALS_NLEADS` with `SCHEDULE_SET`, when `first_due_date` is set, the plan timers start and the plan moves to running; the case moves to `PLAN_RUNNING` | TSD S2 T4 R-RES-25; Routing Logic v4 R-RES-25; FSD A2.10.3.1 |
| BR3 | The booking facts are read from `v_ace_plan`, `v_ace_payment` and `v_ace_account` at the moment of confirmation; no account, payment or plan fact is copied into `rwb_treatment` | DP-05; D-RCV-35; ADR-010; FSD A2.10.3.1 |
| BR4 | No value a business person may change is written in code: the schedule basis, the due dates and the timer values are read as values in force with their version | FSD A2.10.3.1 BR-S2-010; ASM-4380 |
| BR5 | The decision record is written in the same transaction as the schedule columns, or neither is stored and the user is told the action was not taken | ADR-022; REQ-DRI-005; DP-03 |
| BR6 | The case status stays rwb-case's: the stage reports the outcome of R-RES-22 and R-RES-25 to the parent `CaseWorkflow` and the parent moves the status; no case table is read or written here | ASM-3062; DP-01; Architecture v5 slide 43 event 29 |
| BR7 | Booking in ALS and NLEADS is operations' act: the FSD keeps it out of scope and the TSD records it as booked by the officer. This service sends the instruction through the one outbound path it has, the ACE common module by Temporal Nexus, and confirms from the ACE read | GAP-2667; ASM-4382; FSD S2 A1.1; TSD S2 T5.1 INT-03, INT-26 |
| BR8 | The plan timers are durable timers inside `TreatmentWorkflow` and a schedule row is not a clock; no `timer` row and no Schedule is created | ASM-4380; DP-10; Architecture v5 slide 42 event 18 |
| BR9 | The schedule is written only on the columns of TSD S2 T3.1; the ALS booking reference has no column and is a request-context fact carried on the booking record and the decision record | GAP-2665; ASM-4380; TSD S2 T3.1 |
| BR10 | The booking acknowledgement is EV-11 consumed through the inbox: a redelivery produces one schedule, one record and one timer set | DP-09; Architecture v5 slide 42 event 11 and its notes |

**Where each rule lives in the target.** BR1 and BR2 are the two rule outcomes this workflow reports: the BOOKING_MATCH package decides them and the parent applies them, so AC2 and AC3 assert the outcome report and the mock case status, not a local status write (ASM-3062). BR3 is the reason the three views are named in section 11 and no Workbench table is added for the plan or the payments. BR4 is the reason the due dates and the timer values come from the parameters and the package, never from a constant. BR5 is the `MANDATORY` propagation: the library joins this transaction or the apply step fails. BR6 is the boundary with rwb-case, BR7 the boundary with the core bank and NLEADS, BR8 the clock mechanism, and BR9 and BR10 are the two contract facts this story takes from its own contract and from the event envelope.

### 9. State transitions

None of this story's own: the case status is rwb-case's (DP-01; ASM-3062), and the `treatment` lifecycle states (Draft, submitted, approved, booked, broken) are set by the treatment and approval stories. This story reports an outcome for each rule and changes the state of its own `TreatmentWorkflow` execution and of its durable timers.

| From | Rule and event | Condition | To (reported to the parent) |
|---|---|---|---|
| `WITH_OPS_BOOKING` | R-RES-22, `BOOKING_CONFIRMED` | ALS and NLEADS both acknowledge | `BOOKED_IN_ALS_NLEADS`; the booking date and the schedule are stored |
| `BOOKED_IN_ALS_NLEADS` | R-RES-25, `SCHEDULE_SET` | `first_due_date` is set | `PLAN_RUNNING`; the plan timers start |
| `WITH_OPS_BOOKING` | R-RES-23, `BOOKING_REJECTED` | ALS rejects the booking | No move: the case stays with operations (not this story's branch) |
| `WITH_OPS_BOOKING` | R-RES-24, `NLEADS_CALLBACK_MISSING` | `callback_age` above the callback limit | No move: the booking is held (not this story's branch) |

| Workflow state | Meaning |
|---|---|
| RUNNING, waiting on the booking event | The stage is open and the plan is with operations |
| RUNNING, waiting on the plan timer | The schedule is set and the plan clock runs |
| COMPLETED | The stage ended; the plan runs, breaks or closes under a later rule |
| FAILED | The record write or the contract validation failed and the apply step rolled back |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Primary: reads the booked schedule on SCR-14, rights C, R, U and A of capability area Treatment and offer |
| RW-CASEOWN, case owner | Reads the booked schedule, rights C, R and U |
| Operations (booking) | Owns the booking act in ALS and NLEADS; the system acts for them only through R-RES-22 and R-RES-25 |
| RW-TEAMMGR, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT | Read only, right R (TSD S2 T6.1) |
| RW-PRODHEAD, RW-CREDCOMM | Read and approve, rights R and A; no approval is taken in this story |
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the three activities, the repository and the timer set |
| rwb-case (P3) | Owns the case, the status, the assignment and the `timer` table; answers the case signal this stage receives |
| rwb-payment (P8) | Owns the booking match and the producer side of EV-11 |
| rwb-source-data (P1) | Owns the ACE ingestion and the `v_ace_*` views this story reads |
| The platform workflow owner | Owns the `rwb-treatment` task queue, the namespace and the worker registration |
| No delegation of authority level applies | The story records and applies the outcome of two rules; no credit or price decision is taken here |

The access check itself is the platform guard library's and is declared here as the capability area and the right only (ASM-3064; TSD S2 T6.1). No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry case IDs, treatment IDs, codes, dates and amounts only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-009 | treatment | installments | Write |
| DF-TRT-012 | treatment | booked_at | Write |
| DF-TRT-023 | treatment | nleads_ref | Write |
| DF-TRT-028 | treatment | booking_difference | Write |
| DF-TRT-029 | treatment | first_due_date | Write |
| DF-TRT-031 | treatment | installment_amount | Write |
| DF-TRT-032 | treatment | installments_paid | Write |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key and the account facts of the view | Read |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount and the schedule basis | Read |
| DF-ACE-160 to DF-ACE-177 | v_ace_plan | plan_ref, plan_status, booked_at, approved_at and the plan facts | Read |
| DF-DEC-001 to DF-DEC-018 | decision_record | the local record shape declared by RWB-PLT-E1027-CON | Write |
| DF-REF-001 to DF-REF-015 | rule_row | rule ID, rule version and the labels the evaluated rule reports | Read |
| DF-WRK-027 to DF-WRK-036 | timer | Not used: the plan timers are durable Temporal timers, and the `timer` table is rwb-case's | Not read or written |
| DF-CAS-001 to DF-CAS-023 | recovery_case | the case status, read from the case signal only | Read (from the signal) |

The seven schedule columns of `treatment` are the only business columns this story writes (TSD S2 T3.1). The three `v_ace_*` views are read SELECT only, under the freshness rule VR-S2-010-1, and no plan, account or payment fact is copied into `rwb_treatment` (DP-05; ADR-010). `decision_record` is written through the library and never by a repository of this story (DP-03, DP-01). `recovery_case` and `timer` are P3's: the case status arrives on the signal and the clocks are durable timers, so no row of either table is read or written here (Ownership Map; ASM-3062, ASM-4380). `rule_row` is P7's and is read through the rule-package path, not from its table. Field identifiers are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None of its own. The booking step is event-started and has no screen action of its own: the four operations of this service (TSD S2 T-A.1 API-S2-001 to API-S2-004) belong to the treatment, offer and approval stories, and the treatment read `GET /treatments/{treatmentId}` that shows the booked schedule is RWB-S2-E3001-CON's. This story writes the schedule and the record behind that read and declares no path, no request and no response of its own; the booking and schedule body it validates is RWB-S2-E3010-CON's, published under base `/api/recovery/treatment/v1` (DP-13).

#### 12.2 REST operations consumed

None. The case status arrives on the case signal the parent `CaseWorkflow` forwards (EV-29), the booking acknowledgement arrives as EV-11 on the inbox, the rule package version arrives on EV-30, and the three `v_ace_*` views are SQL reads of this service's own login, not a REST call (DP-05; Architecture v5 slides 42 and 43; ASM-3062). The outbound booking instruction goes through the ACE common module by Temporal Nexus and is described in 12.5, not here (GAP-2667; ASM-4382).

#### 12.3 Events published

None of its own. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14); its events `TreatmentApproved` (EV-10) and `TreatmentClosed` belong to the approval and closure stories. The booking writes no outbox row of its own: the `DecisionRecorded` event on the shared topic `rwb.decision-record.v1` is written to this service's outbox by the decision-record library in the booking's transaction, and its envelope and key are that contract's (DP-03, DP-09; Architecture v5 slide 42 event 08). The catalogue carries no booking event of this service: `TreatmentBooked` is rwb-payment's (EV-11).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.payment.TreatmentBooked.v1` | `rwb.payment.events.v1` | P8 rwb-payment | The booking acknowledgement: numbers the signal that lets R-RES-22 fire on `WITH_OPS_BOOKING` (EV-11; Architecture v5 slide 42 event 11) |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Announces the BOOKING_MATCH package and its version; the workflow evaluates the version in force and stamps it on the booking's record (EV-30) |

Both are consumed through the inbox of the outbox library, so a redelivery does not swap a package twice for one version and does not book one plan twice. EV-11 has two consumers in the catalogue: rwb-case forwards it to the case router as a signal, and rwb-treatment subscribes in its own right because the booking is its own fact — the subscription declared here is the direct one and no case table is read behind it (Architecture v5 slide 42 event 11; ASM-3062). `rwb.payment.PaymentMissed.v1` (EV-12) belongs to the broken-plan story of the same family, and `rwb.deviation.DeviationRaised.v1` (EV-06) is consumed by rwb-case's case router and reaches the stage as a forwarded signal (Architecture v5 slides 42 and 43).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage, with the four steps receive, evaluate, record and apply, wait | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, route set, case status on the signal; holds the booking identifiers, the schedule it sets and the plan timers; output: the stage outcomes of R-RES-22 and R-RES-25 |
| `readBookingFacts` | Activity | `rwb-treatment` | The plan reference and the account key; the booking date from `v_ace_plan`, the schedule basis from `v_ace_payment` and the account facts from `v_ace_account`, read SELECT only (BR3) |
| `setPlanSchedule` | Activity | `rwb-treatment` | The `PlanBooking` body of RWB-S2-E3010-CON and the treatment ID; the seven schedule columns, the validation answer and the refusal with MSG-GEN-001 (BR9) |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: the schedule columns on `treatment`, the decision record through the library, the outbox row of the record event and the stage outcome reported to the parent (BR5) |

The workflow is the stage child of Architecture v5 slide 18 and the Temporal and Drools Design slide 18 for rwb-treatment; the three activity names are this story's design choice and are fixed by no source document (GAP-2665; ASM-4380). The retry policy is the workflow kit's: 1 s initial interval, back-off 2, 10 attempts, and no retry on a refused record. The outbound booking instruction, when the booking is sent from the Workbench side, is one Temporal Nexus operation into the `ace-collection` namespace, the only external cell Architecture v5's matrix gives S2 (GAP-2667; ASM-4382; Architecture v5 slide 13). The plan timers are durable timers in this workflow and not a Schedule.

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` and advanced by EV-11, by EV-30 and by its own durable timers; it owns no Temporal Schedule and no legacy Quartz job, and the plan clock that the monolith kept as a five-minute timer check is retired in favour of durable timers (ASM-4380; DP-10; Architecture v5 slide 42 event 18).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Created by the treatment story's Flyway version with the fields of TSD S2 T3.1; this story writes the seven schedule columns inside `recordAndApply` and creates no column |
| `decision_record` | `rwb_treatment` | PLT, a library object | Written through `DecisionRecordWriter.record(...)` in the same transaction; the shape and the DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Never read and never written here; the central ledger is P7's (DP-01) |
| `timer`, `recovery_case` | `rwb_case` | P3 | Never read and never written here; the case status arrives on the signal and the plan clock is a durable timer (ASM-3062, ASM-4380) |
| `v_ace_plan`, `v_ace_payment`, `v_ace_account` | ACE views, read-only | P1 rwb-source-data | Read SELECT only through the `rwb_treatment` login; created by no migration of this service (DP-05) |

No table of another service is read and no foreign key crosses a schema (DP-01). The views are not tables of this service and no Workbench copy of the plan, the payments or the account is created (BR3).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3010-CON booking fake | The `PlanBooking` element and the schedule body | A complete body; a body with a missing required property; a body with no acknowledgement reference; a body whose booking date is older than the freshness rule; a body carrying a booking difference |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with a chain sequence and an entry hash; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003; the outbox row present and absent after a rollback |
| EV-11 event fixture | The booking acknowledgement | One `rwb.payment.TreatmentBooked.v1` for a synthetic case; the same event twice for the dedupe test; an event for a case with no open stage |
| `v_ace_*` view fixtures | The three ACE reads | A booked plan with a schedule basis and a first due date; a plan not yet visible after the batch; a stale batch date; a plan with a booking difference |
| rwb-case case-status mock | The case-status line of AC2 and AC3 | `WITH_OPS_BOOKING` for AC2 and `BOOKED_IN_ALS_NLEADS` for AC3, on the forwarded signal; no case table and no case REST call |
| RWB-PLT-N001-CON route fake | The composite route of SCR-14 | The booked-schedule answer of the screen, one hop |

The booking fake is the published contract of RWB-S2-E3010-CON, the record fake is RWB-PLT-E1027-CON's, the view fixtures stand for the ACE reads until the views are granted in SIT, and the case-status mock is test-only and is the signal answer recorded with ASM-3062 (GAP-2665; ASM-4380).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | None | No path of its own; the booked schedule is read on the treatment operation of RWB-S2-E3001-CON |
| Kafka | None of its own | 2 events (`rwb.payment.TreatmentBooked.v1`, `rwb.decision.RulePackageInForce.v1`) | Own topic `rwb.treatment.events.v1` for the service's own events; inbox dedupe by cloud event id; the record event goes out through the library's outbox |
| Temporal | None | `TreatmentWorkflow` and 3 activities on `rwb-treatment`; 1 Nexus operation into `ace-collection` | Namespace `rwb-recovery`; one timer set per schedule; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `booking` and `schedule`, with the published types in `...treatment.api` (DP-13, DP-14). Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule this story is built on: the schedule columns and the record are one commit or neither is. DP-05 is the read path: the booking date, the schedule basis and the account facts are taken from the three views and copied nowhere. DP-13 fixes the base under which the booking body is published, and DP-19 is the route by which the booked schedule is seen. The other patterns of the service — the owner schema, the workflow kit, the outbox — are service-template capabilities and add no dependency of this story (ASM-4379, ASM-3064).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (booking branch) | Workflow | The four steps, the booking state, the plan timer set and the outcome report to the parent |
| `readBookingFacts` | Activity | Reads `v_ace_plan`, `v_ace_payment` and `v_ace_account` under the freshness rule (BR3) |
| `setPlanSchedule` | Activity | Maps and validates the `PlanBooking` body against the seven schedule columns (BR9) |
| `recordAndApply` | Activity | One transaction: the schedule columns, the decision record, the outbox row and the outcome (BR5) |
| `TreatmentRepository` | Repository | Reads and updates the schedule columns of `treatment` in `rwb_treatment` (DP-01) |
| `PlanClock` | Workflow timer set | The durable timers from the first due date of the schedule (BR8) |
| `BookingConsumer` | Event consumer | The inbox subscription of EV-11 and its signal to the stage (BR10) |
| `Migrations` | Migration | The schedule columns on the per-service sequence where they are missing (DP-15) |

**Database.** `treatment` holds the schedule in `booked_at`, `nleads_ref`, `first_due_date`, `installment_amount`, `installments`, `installments_paid` and `booking_difference` (DF-TRT-012, -023, -029, -031, -009, -032, -028). The ALS booking reference has no column and is carried on the booking record and the decision record (BR9). `decision_record` is the library object applied by this service's own Flyway sequence in `rwb_treatment`. There is no `timer` row for the plan clock, because the clock is a durable timer inside the workflow (BR8).

**Configuration and reference data.** The timer values, the due-date rule and the callback limit are values in force of the parameters and the BOOKING_MATCH package, never constants (BR4; Routing Logic v4 R-RES-22 to R-RES-25). The BOOKING_MATCH package and its version arrive on `rwb.decision.RulePackageInForce.v1` (EV-30). The status and treatment-type lists are reference data read through the owner's contract. The capability area "Treatment and offer" and the rights C, R, U and A are the access rows of the platform guard library, not constants of this story.

**Build steps**

1. The Flyway version that carries the schedule columns the treatment story leaves to this one and the library's `decision_record` (BR9, DP-15).
2. `TreatmentWorkflow`'s booking branch and its input record, registered on `rwb-treatment`, with the four steps and the outcome report to the parent (BR6).
3. The `BookingConsumer` subscription of EV-11 with the inbox dedupe and the signal to the running stage (BR10).
4. The `EvaluateRules` call with the BOOKING_MATCH package version from EV-30, and the R-RES-22 outcome mapping (BR1).
5. `readBookingFacts` with the three views and the freshness rule (BR3, AC2).
6. `setPlanSchedule` with the `PlanBooking` validation and the seven columns (BR9, AC2).
7. `recordAndApply` with the schedule columns, the `MANDATORY` record write and the outbox row (AC2, AC4).
8. The plan timer set, its start on R-RES-25 and its recalculation when a due date changes (BR2, BR8, AC3).
9. Tests for AC2 to AC4 against the fakes, the event fixture and the view fixtures.

**Feature flag.** `rwb.treatment.plan-booking`.

**Done when.** The tests in section 16 pass, `TreatmentWorkflow` books a synthetic plan on one EV-11 and reports R-RES-22 and R-RES-25, the seven schedule columns and one `decision_record` are committed together, the plan clock fires on the first due date with no `timer` row, a stale batch date holds the case with MSG-P1-001, a forced record failure leaves nothing behind with MSG-P7-003, and SCR-14 shows the booked schedule through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the right in Treatment and offer reads the booked schedule | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required booking property is missing or out of its domain | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. |
| MSG-P1-001 | The ACE data behind `v_ace_plan` or `v_ace_payment` is older than the freshness rule | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S2-001 | A settlement offer falls below the floor and goes for approval (legacy text carried, raised by the settlement stories) | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | The payoff a plan rests on is older than the freshness rule (legacy text carried) | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | The offer to the customer reaches its validity date (legacy text carried, raised by the offer story) | The offer to the customer ends on {date}. |

The legacy texts are carried unchanged: MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the legacy story's, MSG-GEN-001 and MSG-P4-002 are the form and guard answers, and MSG-P7-003 and MSG-P7-009 are the record library's (RWB-PLT-E1027-CON; TSD S2 T6.1). MSG-P1-001 is the freshness message of VR-S2-010-1 and MSG-S2-001, MSG-S2-002 and MSG-S2-003 stay named because the legacy story carries them. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record, with the states Draft, submitted, approved, booked and broken, is the one screen of this story: its booked state shows the booking date, the NLEADS reference, the first due date and the schedule the story writes, and its broken state is the broken-plan story's. It is reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment in parallel, one hop each (DP-19; RWB-PLT-N001-CON). The booking step itself runs unattended, so no screen action is declared and no field of this story is editable: the officer reads the outcome. The screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-010-01 | AC1 | End to end | Book the plan and set the schedule |
| TC-E3-010-02 | AC2 | End to end | Rule R-RES-22 |
| TC-E3-010-03 | AC3 | End to end | Rule R-RES-25 |
| TC-E3-010-04 | AC4 | End to end | Not recorded |
| TC-E3-010-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-010-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy level "System" maps to "End to end" for the four criteria and to "Component" for the Access and Principle 5 cases, as in the other stories of this run. TC-E3-010-01 covers AC1, which this story does not own: the case is executed end to end by the wave 2 integration harness and the row is kept here so that no legacy id is renumbered (section 18). Where the legacy Covers names `Access`, the criterion is the published answer of the platform guard library on the treatment read; where it names `Principle 5`, the criterion is the `MANDATORY` record write of RWB-PLT-E1027-CON rolling the apply step back. The booking, record, route and view fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the timer values, the due-date rule, the callback limit and the rule version are values in force read from the parameters and the package, never constants (BR4; TSD S2 T6.1).
- No personal data in logs, events, workflow inputs or the fixture: the rows carry case IDs, treatment IDs, codes, dates and amounts only; test data is synthetic and the case subject is never in a payload (DP-09).
- No read of another service's table: the case status arrives on the forwarded signal, the booking arrives as EV-11 and the rule package version as EV-30; `recovery_case`, `timer` and `rule_row` are never named in SQL (DP-01, ASM-3062).
- ACE data only through the owner's views: `v_ace_plan`, `v_ace_payment` and `v_ace_account` are read SELECT only and no plan, account or payment fact is copied into `rwb_treatment` (BR3; DP-05).
- The decision record is written in the same transaction as the schedule columns, with `MANDATORY`; a forced failure leaves nothing behind and shows MSG-P7-003 (DP-03, BR5).
- The plan timers are durable timers inside `TreatmentWorkflow`: no `timer` row, no five-minute check and no Schedule (BR8).
- No booking is made by this service in ALS or NLEADS: the booking stays operations' act, and the service sends only the instruction it is given and reads the confirmation back (BR7; ASM-4382).
- An applied migration is never edited: a correction to the schedule columns is a new version on the service sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Program, 5.9 | FEAT-TRT-10 | 07 Route, settle and claim | R-RES-22; R-RES-25 | TC-E3-010-02, TC-E3-010-03 |
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next business date's ACE account data in `v_ace_account` | Program, 5.2 | FEAT-TRT-10 | 07 Route, settle and claim | R-RES-22; BR3 | TC-E3-010-01, TC-E3-010-02 |
| Legacy test set RWB-E3-010 | TC-E3-010-01, TC-E3-010-02, TC-E3-010-03, TC-E3-010-04, TC-E3-010-05, TC-E3-010-06 | Program, 5.9 | FEAT-TRT-10 Book the plan and set the schedule | 07 Route, settle and claim | R-RES-22, R-RES-25 | TC-E3-010-01 is executed by the wave 2 integration harness; the rest here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3010-CON | Contract | H: declares the `PlanBooking` element, its validation, its fakes and the timer contract |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and its `MANDATORY` transaction rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 |
| RWB-S2-E3004-APP | App development | The plan offer, the band and the offer clock this story runs the plan after |
| RWB-S2-E3001-APP | App development | The treatment record, its states and its read operation |
| RWB-E3-011's stories | App development | The broken plan, the cure period and EV-12 after this story hands the clock over |
| P8 rwb-payment | App development | The booking match and the producer of EV-11 |
| P1 rwb-source-data | App development | The ACE ingestion and the `v_ace_*` views this story reads |
| The wave 2 integration harness | Integration | I: the end-to-end proof of AC1 and of the same legacy key against the live owners |

### 19. Out of scope

- AC1 of the legacy story and its end-to-end path from the approved treatment through NLEADS and ALS to a running plan: the wave 2 integration harness.
- The published `PlanBooking` element, its required set, the acknowledgement rule, the timer contract and the fakes: RWB-S2-E3010-CON.
- The plan offer, the band and the offer clock: RWB-S2-E3004-APP and RWB-S2-E3004-CON.
- The treatment record, its states and the read operation that shows the booked schedule: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The broken plan, the cure period and the missed-payment path: RWB-E3-011's stories; the payment matching behind EV-11: P8 rwb-payment.
- The booking itself in ALS and NLEADS, and the credit approval in NLEADS: operations and the credit approval flow (FSD S2 A1.1).
- The posting to GL and the posting files: P8 rwb-payment.
- The decision-record library, its DDL template and its exceptions: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP; the central ledger: RWB-P7-E1027-APP.
- The rule package registry and the rule version labels: P7 rwb-decision, RWB-P7-E1073-CON.
- The case status, the assignment and the `timer` table: rwb-case (P3), RWB-P3-E2004-APP and its contract.
- The ACE ingestion, the batch and the `v_ace_*` views: P1 rwb-source-data, RWB-P1-E1007-APP and its contract.
- SCR-14 and its composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the booking body, the schedule and the record: the wave 2 integration harness.

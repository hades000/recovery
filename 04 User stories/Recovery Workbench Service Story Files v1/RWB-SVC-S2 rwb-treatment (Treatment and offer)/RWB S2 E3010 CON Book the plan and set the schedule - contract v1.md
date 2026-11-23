# RWB-S2-E3010-CON Book the plan and set the schedule - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-010 for rwb-treatment (S2, Treatment and offer). This document publishes the booking and schedule body of the plan — the `PlanBooking` element, its eight properties and their mapping to the `treatment` field set of TSD S2 T3.1, the required and optional rules, the acknowledgement rule of R-RES-22 (ALS and NLEADS both), the timer contract of R-RES-25 (a first due date and durable timers, never a `timer` row), the rule that the ALS booking reference and the booking difference are carried as facts and not as new columns, the versioning rule and the fakes — under base `/api/recovery/treatment/v1` (DP-13), with the ACE facts read from the `v_ace_*` views (DP-05), the screens reached through the gateway-bff composite route (DP-19) and the decision record written through the library of RWB-PLT-E1027-CON (DP-03). The legacy acceptance criteria stay with RWB-S2-E3010-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3010-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner of rwb-treatment**, I want **the published booking and schedule body of the plan — the `PlanBooking` element, its eight properties and their mapping to the `treatment` field set, the required and optional rules, the acknowledgement rule of R-RES-22, the timer contract of R-RES-25, the versioning rule and the fakes — instead of the monolith's in-process booking callback and its `timer` rows**, so that **the booking story, the screens and the wave 2 integration harness can build against one frozen booking and schedule body from Day 1, and no plan clock is ever a database row again**.

The contract covers exactly six things:

- the `PlanBooking` element and its eight properties, with the seven that map to a `treatment` column named by field identifier and the one that maps to nothing carried as a fact (DP-01; TSD S2 T3.1);
- the required set — the seven facts without which a booking cannot be confirmed, including both the ALS and the NLEADS acknowledgement — and the optional set, with the reason written into the document (GAP-2666; ASM-4381);
- the acknowledgement rule of R-RES-22: the stage confirms only when ALS and NLEADS both acknowledge, one reference per system, and holds in `WITH_OPS_BOOKING` otherwise (TSD S2 T4; Routing Logic v4 R-RES-22);
- the timer contract of R-RES-25: `firstDueDate` is the condition that starts the plan timers, the timers are durable timers inside `TreatmentWorkflow` (names, cadence source and start rule fixed here), and no `timer` row and no Schedule is created (ASM-4380; DP-10);
- the versioning rule and the pinning rule that let the booking story, the screens and the integration harness pin v1 and raise a change request rather than a private variant;
- the fakes: a booking fake, a decision-record fake, a route fake, an EV-11 event fixture, a case-status mock and the `v_ace_*` view fixtures, all answering from one example set, with the drift test that fails a build on any difference from this document.

It does not own: the booking branch of the workflow, the three activities, the schedule write, the timer set and the record write, which are RWB-S2-E3010-APP; the booking act in ALS and NLEADS, which operations perform (FSD S2 A1.1; TSD S2 T5.1); the outbound path to those systems, which is the ACE common module's by Temporal Nexus (GAP-2667; ASM-4382); the plan offer and its band, which are RWB-S2-E3004-APP and its contract; the treatment entity and its other fields, which are RWB-S2-E3001-APP and its contract; the decision-record library and its DDL template, which are RWB-PLT-E1027-CON; the broken plan and the cure period, which are RWB-E3-011's stories; the case status and the `timer` table, which are rwb-case's (DP-01; ASM-3062); and the screens, which are the platform edge story's and the screen owners' (DP-19).

### 2. Business rationale

A booking is the moment a plan stops being an agreement and becomes a schedule the bank bills against. The FSD measures FEAT-TRT-10 by restructure turnaround of 5 days, measured from the decision log and the Workbench records (FSD S2 v3, section A2.10.1), and the two requirements behind the step are REQ-S2-008, that booked terms are posted to their systems of record without re-keying, and REQ-CHO-008, that booked terms are recorded on the case and the booking is confirmed from the next business date's ACE data in `v_ace_account`. Both fail if the booking and its schedule have no agreed shape: one team records a booking date, another records a reference, a third starts a clock from a date it invented, and the decision record proves none of them.

In the monolith the booking was an in-process callback and the clock was a `timer` row: one schema, one decision table, one row per clock. Architecture v5 changes both facts at once. rwb-treatment owns the treatments, contracts, agreements and plan timers in `rwb_treatment` (Architecture v5 slide 41), the booking acknowledgement arrives as `rwb.payment.TreatmentBooked.v1` from rwb-payment (EV-11; slide 42 event 11), the plan timers become durable timers, because the catalogue retires `TimerDue` as "durable timer — retired: timer inside the workflow" (slide 42 event 18), and the decision record is a local row in the same transaction (DP-03). A published body is therefore the only place where the ACE facts, the operations booking, the officer's screen and the clock meet.

Two facts make the contract urgent rather than tidy. The first is the acknowledgement. R-RES-22 says a booking is confirmed when ALS and NLEADS both acknowledge, and TSD S2 T3.1 has a NLEADS reference (`nleads_ref`) but no ALS reference at all: left to the implementers, one team drops the ALS reference, one stores it in a text column nobody reads, and the "both acknowledge" condition becomes unprovable — which is exactly what AC2 and AC3 turn on. The contract therefore fixes both references as required facts, maps the NLEADS one to its column and carries the ALS one on the booking record and the decision record, with no column created (GAP-2666; ASM-4381). The second is the clock. "Start the plan timers" reads as a row to anyone who knew the monolith's `timer` table, and that table is rwb-case's: the contract fixes the timers as durable timers inside `TreatmentWorkflow`, with `firstDueDate` as the one condition that starts them and the cadence read as a value in force (GAP-2665; ASM-4380).

The fake is the Day-1 unblocker. RWB-S2-E3010-APP, the screen story and the wave 2 integration harness can build and test the confirmation path, the hold when one system has not acknowledged, the stale-batch refusal and the clock start before a single environment is booked or a single view is granted (Template and Rules §R5.4 class C, §R5.7).

### 3. Preconditions

- The schedule columns are fixed by TSD S2 T3.1: `installments` (DF-TRT-009, integer), `booked_at` (DF-TRT-012, timestamptz), `nleads_ref` (DF-TRT-023, varchar(30)), `booking_difference` (DF-TRT-028, jsonb), `first_due_date` (DF-TRT-029, date), `installment_amount` (DF-TRT-031, numeric(18,2)) and `installments_paid` (DF-TRT-032, integer), on `treatment` in schema `rwb_treatment`, owned by S2 (DP-01; Architecture v5 slide 41).
- No source defines a booking element, an acknowledgement element or a schedule element; the properties, the required set, the ALS reference's home and the timer names are this contract's working read, published with the gap and the assumption (GAP-2666; ASM-4381).
- The booking confirmation arrives as EV-11 `rwb.payment.TreatmentBooked.v1` on `rwb.payment.events.v1`, produced by rwb-payment with the case key and the CloudEvents envelope; rwb-treatment is a named consumer (Architecture v5 slide 42 event 11; DP-09).
- The booking facts are read from `v_ace_plan`, `v_ace_payment` and `v_ace_account`, SELECT only, and no plan, account or payment fact is copied into `rwb_treatment` (DP-05; D-RCV-35; ADR-010).
- The rules are R-RES-22 and R-RES-25 of the BOOKING_MATCH package in force, whose version arrives on `rwb.decision.RulePackageInForce.v1` (EV-30); the embedded Drools runtime is the service template's wave-0 capability (ASM-4379).
- The decision record is written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_record` is a library object in `rwb_treatment` and `decision_log_entry` is P7's (DP-03, DP-01).
- The gateway-bff composite route of RWB-PLT-N001-CON exists, so the screen's binding to the body is named and not declared here (DP-19).
- The access rule is the platform guard library's: capability area "Treatment and offer", right R for the booked schedule and right U for any correction, with RW-RESTRUCT holding CRUA and RW-CASEOWN CRU (TSD S2 T6.1; ASM-3064).
- The legacy message texts this body can raise are kept unchanged: MSG-GEN-001 and MSG-P4-002, with MSG-P7-003 and MSG-P7-009 on the record path and MSG-P1-001 on the stale-batch path.
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element: `PlanBooking` with its eight properties, their types taken from TSD S2 T3.1 and their field identifiers, and nothing else.
2. The author fixes the required and optional rule: the seven facts without which a booking cannot be confirmed — both acknowledgement references, the booking date, the first due date, the installment count, the installment amount and the installments paid — are required, the booking difference is optional, and the reasoning and its gap reference are written into the document.
3. The author writes the validation section: the property domains, the cross-property rules (a first due date not before the booking date, a paid count not above the count, an acknowledgement reference present for each system), the refusal of an unknown property including any new clock column, and the error set with the message identifiers.
4. The author writes the acknowledgement section: R-RES-22 confirms only when both references are present, and the one that is missing is named; a booking with one acknowledgement holds the case in `WITH_OPS_BOOKING`.
5. The author writes the timer section: R-RES-25 starts on `firstDueDate`, the timers are durable timers inside `TreatmentWorkflow` with the names and the cadence source fixed here, and `rwb_treatment` gains no clock table and no clock column beyond `first_due_date`.
6. The author writes the versioning and pinning section: major version 1, the compatible-versus-breaking rule and the pinning obligation of the three consumers.
7. The schema and lint steps run: the body validated against the element and against the `treatment` field set, the example scanned for personal data, and a body naming a new clock column refused.
8. The fake set is generated from the same example set: the booking fake, the decision-record fake, the route fake, the EV-11 fixture, the case-status mock and the view fixtures.
9. The drift test runs the fakes against the document on every change and fails the build on any difference.
10. The document and the fakes are published at v1, and RWB-S2-E3010-APP, the screen story and the wave 2 integration harness pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The body is published without one of the seven required facts, or with a property that is not in the element | The schema validation fails the build; the element holds exactly eight properties and the required set is fixed | None | AC1, AC2 |
| X2 | A body names a clock column or a schedule table that TSD S2 T3.1 does not have | The request is refused as a contract violation; the clock is a durable timer and the table gains no column | MSG-GEN-001 | AC3, AC4 |
| X3 | A property carries a value outside its type or domain, or the cross-property rules fail | The request is refused with the field named; nothing is written | MSG-GEN-001 | AC2, AC4 |
| X4 | One acknowledgement reference is missing | The booking is not confirmed, the field is named and the case holds in `WITH_OPS_BOOKING` | None | AC3 |
| X5 | A breaking change is made to a property, a required rule, the acknowledgement rule or the timer rule | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consuming story ships without the drift test, or a schema change breaks a consumer | The drift test fails the build of that consumer and the registry refuses the change | None | AC6 |
| X7 | A value the consumers need is named by no source — the element, the required set, the ALS reference's home or the timer names | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2666; ASM-4381) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The example values, the property order and the description texts are open until v1 is frozen; the eight properties, the required set, the acknowledgement rule and the timer rule are fixed |
| Valuable | Unblocks the booking story, the screen story and the integration harness with one booking body on Day 1 |
| Estimable | One element, one validation section, one acknowledgement section, one timer section, one versioning rule and six fakes |
| Small | One sprint for the document, the schema, the fakes and the drift test |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Booking and schedule contract

  Background:
    Given the rwb-treatment contract document is published at major version 1
    Given the treatment table carries the 33 fields of TSD S2 T3.1 in schema rwb_treatment
    Given the booking body declares no path of its own and is carried by the stage workflow of RWB-S2-E3010-APP

  Scenario: AC1 The PlanBooking element is published with eight properties (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes PlanBooking with exactly eight properties: nleadsRef, alsBookingRef, bookedAt, firstDueDate, installmentCount, installmentAmount, installmentsPaid and bookingDifference
    Then seven of them name a field identifier of TSD S2 T3.1 and alsBookingRef names none
    Then the element declares no path, no method and no response of its own, and the stage that carries it is RWB-S2-E3010-APP's
    Then the access is capability area Treatment and offer with right R for the booked schedule and right U for a correction, declared here as the right only and checked by the platform guard library

  Scenario: AC2 The required set is fixed against the treatment field set (new, D-RCV-60)
    Given the element section and the treatment field set of TSD S2 T3.1
    When every property is compared to its column and to its type
    Then nleadsRef is required and maps to DF-TRT-023 nleads_ref, varchar(30)
    Then bookedAt is required and maps to DF-TRT-012 booked_at, timestamptz
    Then firstDueDate is required and maps to DF-TRT-029 first_due_date, date
    Then installmentCount is required and maps to DF-TRT-009 installments, integer
    Then installmentAmount is required and maps to DF-TRT-031 installment_amount, numeric(18,2)
    Then installmentsPaid is required and maps to DF-TRT-032 installments_paid, integer
    Then bookingDifference is optional and maps to DF-TRT-028 booking_difference, jsonb
    Then alsBookingRef is required and maps to no column, and the document states that TSD S2 T3.1 has no ALS reference field

  Scenario: AC3 The acknowledgement rule of R-RES-22 is published (new, D-RCV-60)
    Given the acknowledgement section of the document
    When a booking body is presented for confirmation
    Then the booking is confirmed only when both the ALS reference and the NLEADS reference are present
    Then a body missing either reference is refused, the missing reference is named and the case holds in WITH_OPS_BOOKING
    Then a missing NLEADS callback is not a confirmation, and the escalation of R-RES-24 stays outside this contract
    Then the rule version that confirmed the booking is carried on the decision record and not on the body

  Scenario: AC4 The timer contract of R-RES-25 is published and no clock is a row (new, D-RCV-60)
    Given the timer section of the document and the DDL of rwb_treatment
    When the timer contract and the migration set are compared
    Then firstDueDate is the condition that starts the plan timers and a body without it is refused
    Then the timers are published as durable timers inside TreatmentWorkflow, named planInstallmentClock and planEndTimer, started on the first due date and on the last due date of the schedule
    Then the cadence of planInstallmentClock is the value in force of the parameters and the package, never a constant
    Then no timer table, no timer column beyond first_due_date and no Temporal Schedule is created, because the timer table is rwb-case's
    Then a migration or a body that adds a clock column fails the schema lint and the drift test

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published property or rule
    Then an added optional property keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a change to a property name, a type, a required rule, the acknowledgement rule or the timer rule raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3010-APP, the screen story and the wave 2 integration harness pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test fails on any difference (new, D-RCV-60)
    Given the fake set generated from the same example set as the document
    When the contract test runs the booking fake, the decision-record fake, the route fake, the EV-11 fixture, the case-status mock and the view fixtures
    Then the booking fake answers a complete body, a refused body with MSG-GEN-001 and its field, and a body with one acknowledgement reference missing
    Then the view fixtures answer a booked plan, a plan not yet visible after the batch and a stale batch date with MSG-P1-001
    Then the EV-11 fixture answers one event and the same event twice, and the decision-record fake answers an accepted record, a refusal with MSG-P7-009 and a failure with MSG-P7-003
    Then the drift test of every consuming story fails the build on any difference from section 12 and section 13
```

These criteria are new: no legacy acceptance criterion is repeated here — **AC2, AC3 and AC4 of RWB-E3-010 stay with RWB-S2-E3010-APP** — and every identifier comes from the legacy story, Architecture v5, the TSD or the Temporal and Drools Design, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The booking body is one element of eight properties, carried by the stage workflow of the same service; this contract declares no path, no response and no error code of its own | TSD S2 T-A.1; RWB-S2-E3010-APP; DP-13 |
| BR2 | Seven facts are required — both acknowledgement references, the booking date, the first due date, the installment count, the installment amount and the installments paid — and the booking difference is optional | TSD S2 T3.1; GAP-2666; ASM-4381 |
| BR3 | The NLEADS reference maps to `nleads_ref`; the ALS reference has no column in TSD S2 T3.1 and is carried on the booking record and the decision record; no column is created for it | GAP-2666; ASM-4381; DP-01 |
| BR4 | A booking is confirmed only when ALS and NLEADS both acknowledge; one acknowledgement holds the case in `WITH_OPS_BOOKING` and names the missing system | TSD S2 T4 R-RES-22; Routing Logic v4 R-RES-22 |
| BR5 | `firstDueDate` is the condition that starts the plan timers; the timers are durable timers inside `TreatmentWorkflow` and no `timer` row, no clock table and no Schedule is created | TSD S2 T4 R-RES-25; ASM-4380; DP-10 |
| BR6 | No value a business person may change is written in code: the cadence, the due-date rule and the callback limit are values in force with their version | FSD A2.10.3.1 BR-S2-010; ASM-4380 |
| BR7 | The booking facts are read from the `v_ace_*` views and copied nowhere; the body carries the facts of the moment of confirmation, not a Workbench copy of the plan | DP-05; D-RCV-35; ADR-010 |
| BR8 | A refused body names its field with MSG-GEN-001 before any write; the record path fails with MSG-P7-003 and the apply step rolls back | Legacy RWB-E3-010 validation table; DP-03; RWB-PLT-E1027-CON |
| BR9 | The access of the schedule view is capability area Treatment and offer, right R, and a correction needs right U, checked by the platform guard library | TSD S2 T6.1; ASM-3064 |
| BR10 | A published version is never edited: a backward-compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R5.4 class C; §R7.2 |
| BR11 | The body carries facts and identifiers only: no customer, account or document value, and no personal data | DP-09; Template and Rules §R7.2 s17 |

### 9. State transitions

None of its own: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3010-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Booking body | Received | The body arrived with the evidence that a booking exists and no rule has run |
| Booking body | Acknowledged | Both the ALS reference and the NLEADS reference are present |
| Booking body | Partly acknowledged | One reference is missing; the field is named and the case holds in `WITH_OPS_BOOKING` |
| Booking body | Refused | A property failed its type, domain or cross-property rule; the field is named and nothing is written |
| Booking body | Scheduled | The schedule columns, the decision record and the outbox row were committed together and the plan timers started |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

The case statuses of the booking — `WITH_OPS_BOOKING`, `BOOKED_IN_ALS_NLEADS`, `PLAN_RUNNING` — are rwb-case's vocabulary and are named here only as the context the body is presented in (DP-01; ASM-3062).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element, the validation section, the acknowledgement section and the fakes |
| The rwb-treatment tech lead | Approves a breaking change and freezes a version of the booking body |
| The operations booking owner | Confirms the acknowledgement facts of ALS and NLEADS and the meaning of a missing reference |
| The ACE data owner (P1) | Confirms the freshness rule of the `v_ace_*` views the body draws on |
| The platform workflow owner | Confirms the timer names and the durable-timer start rule of R-RES-25 |
| The service team of rwb-treatment (RW-TRIBE) | Consumes the contract in RWB-S2-E3010-APP, pins the version and raises a change request rather than a private variant |
| The screen owners, RW-RESTRUCT and RW-CASEOWN | Bind the booked schedule through the gateway-bff composite route; RW-RESTRUCT holds CRUA and RW-CASEOWN CRU in capability area Treatment and offer |
| RW-PLATADM | Receives the incident that a refused or failed record raises |
| No delegation of authority level applies | A booking body is a technical artefact, not a credit decision; the DoA approval happened on the offer |

No personal name, no email address and no credential appears in the document, an example or a fake. Where an actor must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes a body, its property types, the field identifiers of the `treatment` columns it maps to and the message identifiers it raises; no customer, account or case value appears |
| Booking body published | The eight properties of section 12.1, with the field identifiers DF-TRT-023, DF-TRT-012, DF-TRT-029, DF-TRT-009, DF-TRT-031, DF-TRT-032 and DF-TRT-028 for the seven that map to a column |
| ALS reference published | One required property, `alsBookingRef`, with no field identifier and no column: its home is Not specified in the source documents (GAP-2666; ASM-4381) |
| Timer contract published | Two timer names, `planInstallmentClock` and `planEndTimer`, their start condition and their cadence source; no table and no column is created for either (GAP-2665; ASM-4380) |
| Personal data | None. The body carries references, a date, a count and amounts; the case is identified by its ID outside the body |
| Tables published | `treatment` only, as the field set the body validates against; this contract creates no table and adds no column, and `decision_record` is RWB-PLT-E1027-CON's |
| Retention | Not applicable: the contract stores nothing. The retention of the schedule columns and of the decision record belongs to the table owners |

### 12. Contract

#### 12.1 REST operations provided

None of its own. The booking step is event-started and its body is carried inside the stage workflow; the four operations of this service (TSD S2 T-A.1 API-S2-001 to API-S2-004) belong to the treatment, offer and approval stories, and the treatment read that shows the booked schedule is RWB-S2-E3001-CON's. This contract therefore declares no method, no path, no response and no error code, and publishes only the element below, under base `/api/recovery/treatment/v1` (DP-13; GAP-2666; ASM-4381).

| Property | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `nleadsRef` | varchar(30) | Yes | DF-TRT-023 `nleads_ref` | The NLEADS side of the acknowledgement of R-RES-22 |
| `alsBookingRef` | varchar(40) | Yes | none | The ALS side of the acknowledgement; carried on the booking record and the decision record, with no column (BR3) |
| `bookedAt` | timestamptz | Yes | DF-TRT-012 `booked_at` | The booking date read from `v_ace_plan` |
| `firstDueDate` | date | Yes | DF-TRT-029 `first_due_date` | The condition that starts the plan timers under R-RES-25 |
| `installmentCount` | integer | Yes | DF-TRT-009 `installments` | The number of installments of the booked plan |
| `installmentAmount` | numeric(18,2) | Yes | DF-TRT-031 `installment_amount` | The amount of one installment |
| `installmentsPaid` | integer | Yes | DF-TRT-032 `installments_paid` | The installments paid at the moment of booking |
| `bookingDifference` | jsonb | No | DF-TRT-028 `booking_difference` | The difference between the booked terms and the agreed terms, when the two disagree |

The required set is this contract's working read. TSD S2 T3.1 marks `booked_at`, `first_due_date`, `installment_amount`, `installments` and `installments_paid` as not required at column level and no source fixes a booking body, so the seven facts without which a booking cannot be confirmed are made required here, and the reason is published with the gap and the assumption (GAP-2666; ASM-4381). The ALS reference has no column at all: TSD S2 T3.1 carries `nleads_ref` only, while R-RES-22 confirms on both acknowledgements, so the reference is carried as a fact and the absence of a column is recorded rather than repaired by a private migration (BR3).

#### 12.2 REST operations consumed

None. The contract calls no service. The booking facts arrive from the `v_ace_*` views of rwb-source-data as values the booking story reads, the acknowledgement arrives as EV-11 from rwb-payment, the case status stays rwb-case's and reaches the stage on the case signal, and the decision record is written in process through RWB-PLT-E1027-CON (DP-03, DP-05; ASM-3062, ASM-4380).

#### 12.3 Events published

None. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its events `TreatmentApproved` (EV-10) and `TreatmentClosed` belong to the approval and closure stories. The catalogue carries no booking event of rwb-treatment: `TreatmentBooked` is rwb-payment's (EV-11, Architecture v5 slide 42 event 11), so this contract declares no event of its own, no producer and no payload, and the record event of the booking is the library's `DecisionRecorded` on `rwb.decision-record.v1` written to this service's outbox in the booking's transaction (DP-03, DP-09).

#### 12.4 Events consumed

None. The booking acknowledgement EV-11 is consumed by RWB-S2-E3010-APP's inbox, and the rule package version on `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed by its workflow; neither is a subscription of this contract, which only requires that the body carry the acknowledgement references EV-11 reports and that the confirmed version be recorded with the booking (BR4, BR6).

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity; it fixes the body and the timer contract that the stage uses. The booking branch of `TreatmentWorkflow`, its three activities `readBookingFacts`, `setPlanSchedule` and `recordAndApply`, and the timer set live in RWB-S2-E3010-APP on task queue `rwb-treatment` in namespace `rwb-recovery` (ASM-4380). Two timer names are fixed here so that no consumer invents its own: `planInstallmentClock`, one occurrence per due date of the schedule from `firstDueDate` at the cadence in force, and `planEndTimer`, at the last due date of the schedule.

#### 12.6 Schedules

None. The plan timers are durable timers inside `TreatmentWorkflow`, started by R-RES-25 on `firstDueDate`; this contract declares no Temporal Schedule, no Quartz job and no job row, and the legacy five-minute timer check is retired with the `timer` table (ASM-4380; DP-10; Architecture v5 slide 42 event 18).

#### 12.7 Tables owned

| Table | Schema | Owner | This contract |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | The field set the body validates against: the seven schedule columns of TSD S2 T3.1; no column is created or changed here, and no clock column exists beyond `first_due_date` |
| `decision_record` | `rwb_treatment` | PLT, a library object | Named only: the shape and the DDL template are RWB-PLT-E1027-CON's, and the ALS reference is recorded there (DP-03; BR3) |
| `decision_log_entry` | `rwb_decision` | P7 | Named only: the central ledger is never read and never written by a consumer of this contract (DP-01) |
| `timer` | `rwb_case` | P3 | Named only as the table this contract does not use: the plan clock is a durable timer (BR5; ASM-3062) |
| `v_ace_plan`, `v_ace_payment`, `v_ace_account` | ACE views, read-only | P1 rwb-source-data | Named as the read path of the facts the body carries; no row is copied and no view is created here (DP-05) |

The contract declares no foreign key and no reference across a service boundary, and it creates nothing in another service's schema (DP-01). The ALS reference has no row and no column: it is a required fact of the body, recorded with the booking on the decision record (BR3).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Booking fake | The `PlanBooking` element and its validation | A complete body; a body missing one of the seven required facts with MSG-GEN-001 and the field; a body with a property outside its domain with the same refusal; a body naming a clock column with the same refusal; a body with one acknowledgement reference absent |
| Decision-record fake | RWB-PLT-E1027-CON | An accepted record with chain sequence and entry hash, a refusal with MSG-P7-009 and the field, and a failure with MSG-P7-003 |
| Route fake | The gateway-bff composite route of RWB-PLT-N001-CON | The SCR-14 booked-schedule answer, one hop, built from the same example body |
| EV-11 fixture | `rwb.payment.TreatmentBooked.v1` | One booking event for a synthetic case, the same event twice for the dedupe test, and an event for a case with no open stage |
| Case-status mock | The case status on the forwarded case signal | `WITH_OPS_BOOKING` and `BOOKED_IN_ALS_NLEADS`, the two statuses the criteria of RWB-S2-E3010-APP name |
| `v_ace_*` view fixtures | The three ACE reads the body draws its facts from | A booked plan with a schedule basis and a first due date; a plan not yet visible after the batch; a stale batch date; a plan with a booking difference |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The case-status mock is test-only and stands for the signal answer recorded with ASM-3062; no case table and no case REST call exists behind it.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The element is a schema fragment merged into the service document of RWB-S2-E3001-CON; no path is declared |
| Kafka | 0 | 0 | The service topic and its two events belong to other stories, and the booking event is rwb-payment's |
| Temporal | 0 | 0 | No workflow and no activity; the timer names are fixed for RWB-S2-E3010-APP's workflow |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the `PlanBooking` type in `th.co.scb.ace.workbench.recovery.treatment.api`, the schema fragment merged into the service document, and the validation, acknowledgement, timer and versioning sections in the contract document. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13, DP-14). The implementation is RWB-S2-E3010-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The four rows are referred to here, not carried: this contract builds against nothing, and the three H dependencies are the consuming story's, which is why its own build list is empty by rule (Template and Rules §R5.7). DP-03 fixes the transaction rule the record path must satisfy, DP-05 fixes the read path the facts come from, DP-13 fixes the base the element is published under, and DP-19 is the route through which SCR-14 binds the body.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PlanBooking` | Published type | The eight properties, their types and their mapped field identifiers (BR1, BR2, BR3) |
| PlanBookingSchema | Resource | The schema fragment merged into the service document of RWB-S2-E3001-CON (BR1) |
| ValidationSpecification | Document | The type, domain and cross-property rules and the refusal set (BR8) |
| AcknowledgementSpecification | Document | The both-systems rule of R-RES-22 and the hold when one is missing (BR4) |
| TimerSpecification | Document | `firstDueDate` as the start condition, the two timer names and the cadence source (BR5) |
| VersioningSpecification | Document | Major version 1, the compatible versus breaking rule and the pinning rule (BR10) |
| Fake set and fixtures | Test asset | The booking fake, the record fake, the route fake, the EV-11 fixture, the case-status mock and the view fixtures (AC6) |

**Database.** No change. The seven schedule columns already exist on `treatment` in `rwb_treatment` (DF-TRT-009, -012, -023, -028, -029, -031, -032), and the contract requires that no migration adds a clock column, a schedule table or a booking table, and that no column is renamed to carry the ALS reference (BR3, BR5; GAP-2666; ASM-4381). `decision_record` is the library's object; this contract neither creates nor alters it.

**Configuration and reference data.** None of its own. The cadence of `planInstallmentClock`, the due-date rule and the callback limit are values in force of the parameters and the BOOKING_MATCH package, not of this contract (BR6). The status and treatment-type lists are reference data read through the owner's contract, and the capability area and rights are the platform guard library's rows (BR9; ASM-3064).

**Build steps**

1. Write the `PlanBooking` type with the eight properties and their types from TSD S2 T3.1 (AC1, AC2).
2. Write the schema fragment and merge it into the service document of RWB-S2-E3001-CON; assert no path and no marker of a second operation (AC1).
3. Write the required and optional rule with the field mapping, the ALS reference's home and the gap reference (AC2).
4. Write the acknowledgement section with the both-systems rule and the hold on one missing (AC3).
5. Write the timer section with the two names, the start condition and the no-clock-row rule, and assert the absence of a clock column and a clock table in the migration set (AC4).
6. Write the validation and the error set, with the field naming and the rollback rule (AC2, AC4).
7. Write the versioning and pinning section with the compatible and breaking examples (AC5).
8. Generate the six fakes from the example set and write the drift test into the build of every consuming story (AC6).
9. Publish v1 and record the pinned version of RWB-S2-E3010-APP, the screen story and the wave 2 integration harness (AC5).

**Feature flag.** `rwb.treatment.plan-booking-contract`.

**Done when.** The element and the fragment validate against the service document, a complete body is accepted and each refusal answers with MSG-GEN-001 and its field, the migration set proves no clock column and no clock table, the six fakes answer every example, the drift test is green on RWB-S2-E3010-APP's build, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing or a value is outside its type or domain | Enter {field}. | 422 with the field name, before any write |
| MSG-P4-002 | The caller's role does not hold the right in Treatment and offer | You cannot {action} here. Your role does not include it. | The guard library's answer, before any read of the treatment |
| MSG-P7-009 | A record field is refused (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. | The library's `DecisionLogRecordInvalidException`, RWB-PLT-E1027-CON |
| MSG-P7-003 | The record cannot be written and the schedule is not stored | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 of the stage action, the library's `DecisionLogUnavailableException` |
| MSG-P1-001 | The ACE data behind the booking facts is older than the freshness rule (raised by the booking story, named here for the body) | {product} is from {date}. Today's ACE batch has not arrived. | The booking story reports it and the case holds in `WITH_OPS_BOOKING` |

The five texts are the legacy texts carried unchanged and this contract adds no message identifier of its own; MSG-GEN-001 and MSG-P4-002 are the legacy body's, MSG-P7-003 and MSG-P7-009 are the record library's, and MSG-P1-001 is the freshness message of VR-S2-010-1, which the booking story reports. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story and none declared. SCR-14 Treatment record, with the states Draft, submitted, approved, booked and broken, shows the booking date, the NLEADS reference, the first due date and the schedule the body carries; it binds the `PlanBooking` properties through the gateway-bff composite route and is not built here (DP-19; RWB-PLT-N001-CON). The ALS reference is shown as a read-only fact of the booking and is never an editable field, because it is an acknowledgement of another system and has no column (BR3). The screen field list and the composite route specification belong to the platform edge story and the screen owners.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3010-CON-01 | AC1, AC2 | Contract | The element validated against the service document: eight properties, their types, the seven field identifiers, the required set, the optional booking difference and the ALS reference with no column; no path and no second operation |
| TC-S2-E3010-CON-02 | AC2, AC4 | Component | The required set compared to the migration set: no clock column beyond `first_due_date`, no clock table and no Schedule; a migration that adds one is refused |
| TC-S2-E3010-CON-03 | AC3 | Contract | A body with both references accepted; a body with either reference missing refused with the field named and the case held; a booking with one acknowledgement not confirmed |
| TC-S2-E3010-CON-04 | AC4 | Component | A body with a first due date accepted and the two timers named; a body without it refused; a stale batch date answered with MSG-P1-001 |
| TC-S2-E3010-CON-05 | AC5, AC6 | Contract | A compatible change accepted in BACKWARD mode; a renamed property, a changed type and a changed acknowledgement rule each raising major version 2; the six fakes answering every example; the drift test failing on a one-property difference |

The legacy test set of RWB-E3-010 is carried by RWB-S2-E3010-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the body: the cadence, the due-date rule and the callback limit are values in force of the parameters and the package, and the contract fixes only types and rules (BR6).
- No clock column, no clock table and no Schedule: the timers are durable timers inside `TreatmentWorkflow` and the `timer` table is rwb-case's (BR5; ASM-4380).
- No new column for the ALS reference and no private migration: the reference is a required fact of the body, recorded with the booking on the decision record (BR3).
- No personal data in the schema, an example, a fake or a log: the body carries references, a date, a count and amounts, and the case is identified by its ID outside the body; the scan fails the build otherwise (BR11).
- No path, no response and no error code of this contract's own: the stage carries the body and the treatment read belongs to RWB-S2-E3001-CON (BR1).
- No cross-schema reference and no foreign key across services; the boundary test fails the build (DP-01).
- No case table read: the case status stays rwb-case's and reaches the stage on the case signal, and the case-status mock is test-only (ASM-3062).
- ACE facts only through the owner's views: the body's booking date and schedule basis are the `v_ace_*` values of the moment of confirmation and no copy is created (BR7; DP-05).
- No record written outside the library's `MANDATORY` transaction, and no ledger row: `decision_log_entry` is P7's and is named here only (DP-03; DP-01).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Program, 5.9 | FEAT-TRT-10 | 07 Route, settle and claim | R-RES-22; BR4 | TC-S2-E3010-CON-01, TC-S2-E3010-CON-03 |
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next business date's ACE account data in `v_ace_account` | Program, 5.2 | FEAT-TRT-10 | 07 Route, settle and claim | R-RES-22; BR7 | TC-S2-E3010-CON-02, TC-S2-E3010-CON-04 |
| Legacy test set RWB-E3-010 | TC-E3-010-01, TC-E3-010-02, TC-E3-010-03, TC-E3-010-04, TC-E3-010-05, TC-E3-010-06 | Program, 5.9 | FEAT-TRT-10 Book the plan and set the schedule | 07 Route, settle and claim | R-RES-22, R-RES-25 | Executed by RWB-S2-E3010-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3010-APP | App development | H consumer: builds the booking branch, the schedule write, the timer set and the record write against this contract and its fakes |
| RWB-S2-E3001-CON | Contract | Referred to: the service document and the treatment read that shows the booked schedule; this contract adds no build dependency of its own |
| RWB-S2-E3004-APP, RWB-S2-E3004-CON | App development, Contract | Referred to: the plan offer and its band, whose terms this booking confirms |
| RWB-PLT-E1027-CON | Contract | DP-03: the local decision-record library that records the acknowledgement and the booking |
| RWB-PLT-N001-CON | Contract | DP-19: the gateway-bff composite route through which SCR-14 binds the body |
| P1 rwb-source-data | App development | The ACE ingestion and the `v_ace_*` views the facts come from |
| P8 rwb-payment | App development | The producer of EV-11, the booking acknowledgement |
| The wave 2 integration harness | Integration | I: the end-to-end proof of AC1 and of the same legacy key against the live owners |

### 19. Out of scope

- The booking branch of the workflow, the three activities, the schedule write, the timer set and the record write: RWB-S2-E3010-APP.
- The booking act in ALS and NLEADS and the outbound path to them: operations and the ACE common module (GAP-2667; ASM-4382).
- The plan offer, its band, its validity and its offer clock: RWB-S2-E3004-APP and RWB-S2-E3004-CON.
- The treatment entity, its other fields and its states: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The broken plan, the cure period and the missed-payment path: RWB-E3-011's stories; the payment match that produces EV-11: P8 rwb-payment.
- The decision-record library, its DDL template, its envelope and its exceptions: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP; the central ledger: RWB-P7-E1027-APP.
- The rule package registry, the BOOKING_MATCH package and the rule version labels: P7 rwb-decision, RWB-P7-E1073-CON.
- The case status, the assignment, the operations queue and the `timer` table: rwb-case (P3), RWB-P3-E2004-APP and its contract.
- The ACE ingestion, the batch, the freshness rule and the `v_ace_*` views: P1 rwb-source-data, RWB-P1-E1007-APP and its contract.
- SCR-14 and its composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the booking body, the schedule and the record: the wave 2 integration harness.

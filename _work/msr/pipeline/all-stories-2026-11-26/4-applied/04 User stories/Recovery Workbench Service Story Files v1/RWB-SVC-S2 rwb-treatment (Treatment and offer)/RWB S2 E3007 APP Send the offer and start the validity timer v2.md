# RWB-S2-E3007-APP Send the offer and start the validity timer

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-007 for rwb-treatment (S2, Treatment and offer). The send leaves the monolith's in-process call out of `rwb-case` and becomes the release branch of `TreatmentWorkflow`, the stage child that `CaseWorkflow` starts on task queue `rwb-treatment` (DP-12); the offer is dispatched by the service's own event on `rwb.treatment.events.v1`, which rwb-comms consumes to issue the letter (DP-09, DP-14); the validity clock becomes a durable Temporal timer inside that workflow instead of a `timer` row; the local decision record is written in the same transaction as the release through RWB-PLT-E1027-CON (DP-03); the release body is published by RWB-S2-E3007-CON under base `/api/recovery/treatment/v1` (DP-13); the ACE customer facts the legacy send read for the letter are not read here (DP-05); the screens are reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3007-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3007-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-R |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3007-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the Workbench to send the offer to the customer and start the validity clock**, so that **restructures and settlements reach booking in days**.

This is the application slice of legacy RWB-E3-007. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the data rows, the messages and the two rules they depend on, plus R-RES-15 which the feature section of the FSD names for the counter-offer;
- the release branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery` — the stage child that rwb-case's `CaseWorkflow` starts for a restructure or a settlement, with the four steps of every stage: receive the signal, ask Drools, record and apply in one transaction, then wait (DP-12; Architecture v5 slides 18 and 41; Temporal and Drools Design slides 13 and 18);
- the release step itself: the offer the officer prepared is released to the customer on R-RES-11 when `final_call = approved`, and the offer-preparation clock starts on R-RES-04 when the case is picked up;
- the dispatch: one event, `rwb.treatment.TreatmentApproved.v1` (EV-10), published on `rwb.treatment.events.v1` with key `caseId` through this service's outbox, consumed by rwb-comms to issue the offer letter on the consented channel and by rwb-payment to expect the money (DP-09, DP-14; Architecture v5 slide 13, S2 row, and slide 42 row 10);
- the validity date written on `treatment.valid_until` (DF-TRT-010) and the durable validity timer that runs to it, with MSG-S2-003 naming the date; the wait is a timer and never a routed state;
- the local decision record of the release, written in the same transaction as `valid_until` and the outbox row through the library of RWB-PLT-E1027-CON (DP-03);
- the stage outcome of R-RES-04 and R-RES-11 reported to the parent `CaseWorkflow`, which moves the case status (ASM-4367; DP-01);
- the DP-05 boundary: no `v_ace_*` view and no `account_ext` row is read to send the letter, because the customer facts the legacy story took from `v_ace_customer` belong to the letter's owner and reach it through the owner's own path (ASM-4366).

It does not own: the treatment entity, its states and its other fields, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the plan terms and the band, which are RWB-S2-E3004-APP and RWB-S2-E3005-APP; the settlement range, the floor and the below-floor approval, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the `OfferRelease` element, the validity rule, the event body and the fakes, which are RWB-S2-E3007-CON; the case status, the assignment and the `timer` table, which are rwb-case's (DP-01); the letter template, the channel and the consent check, which are rwb-comms' (P6); the decision-record library, which is RWB-PLT-E1027-CON; the screens and their composite route, which are the platform edge story and the screen owners (DP-19); and the real cross-service proof, which is the wave 2 integration harness.

### 2. Business rationale

The FSD measures the feature by one number: restructure turnaround of 5 days, measured from the decision log and the Workbench records, reviewed monthly, against today's 23 to 26 days tracked by hand (FSD S2 v3, section A2.7.1). The offer is the step where that number is decided, and the sentence that describes it is exact: the Workbench sends the offer to the customer and starts the validity clock, and the wait is a timer, not a routed state (FSD S2 v3, section A2.7.2). A routed state is what the monolith had: a case parked in `OFFER_WITH_CUSTOMER` until a batch found it. A timer is what the target has, and the event catalogue retires `TimerDue` for exactly that reason — the clock lives inside the workflow, not in a row and not in a queue (Architecture v5 slide 42, event 18; Temporal and Drools Design slides 13 and 18, "Clocks: Offer 14 days").

Two facts of the legacy story move. The first is the send. The legacy process called the notification path from inside one deployable; Architecture v5 slide 13 shows no REST line from S2 to rwb-comms, and shows rwb-comms listening to S2's events instead, so the send becomes the service's own event and the letter becomes the consumer's job. That is also the only arrangement that keeps the rule "no personal data in events" satisfiable: the event carries the case, the treatment, the amounts and the validity date, and the letter's addressee is resolved where the letter is built (DP-09; Template and Rules §R7.2 s17). The second is the customer data. The legacy data table lists `v_ace_customer` because the monolith filled the letter from it; in the target the 30 `recovery.v_ace_*` views are read only by rwb-source-data (Architecture v5 slide 8, notes), so this story removes that marker rather than copying a view into `rwb_treatment` (DP-05; ASM-4366).

No business value moves. REQ-S2-002 asks that an offer carry a validity period and that expiry return the case to the status it came from; the validity period is a value in force and never a constant, and the expiry move stays the parent's (BR-S2-007; TSD S2 T4 R-RES-18). The offer-preparation clock and the validity period are both read, not written, in this code (ASM-4368).

### 3. Preconditions

- RWB-S2-E3007-CON is published: the `OfferRelease` element, the validity rule, the EV-10 body, the no-personal-data rule and the fakes are baselined and handed to this story.
- The offer operation `POST /treatments/{treatmentId}/offer` on base `/api/recovery/treatment/v1` is declared by RWB-S2-E3002-CON of the same service; this story adds the release form of that operation and redeclares no path, no envelope and no status code (DP-13; Architecture v5 slide 18).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, the refusal MSG-P7-009, the failure MSG-P7-003, and the DDL template of `decision_record` applied by this service's own Flyway sequence in `rwb_treatment` (DP-03, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and SCR-15, one hop per call (DP-19).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with the 33 fields of TSD S2 T3.1 and the seven standard columns of T3.0, and the `rwb_treatment` login holds rights in that schema only (DP-01, DP-02).
- The RESTRUCTURE package is in force: `TreatmentWorkflow` exists for a case whose route decision is R1, the package and its version arrive on `rwb.decision.RulePackageInForce.v1` (EV-30), and the embedded Drools runtime is the service template's capability, so this story adds no build dependency for it (ASM-4368).
- The validity period and the offer-preparation clock length are values in force: the routing workbook states an offer validity of 14 days for R-RES-09, R-RES-11 and R-SET-06 and a 2-working-day clock for R-RES-04, and no parameter key is defined for either (GAP-2658; ASM-4368).
- RWB-S2-E3004-APP is the sibling that builds and submits the offer; until it is built the offer facts arrive from its workflow-state fixture and no term is assumed (ASM-4369).
- The outbox and inbox library, the workflow kit and the access guard are the service template's, and the capability area and the right are declared here and checked there (ASM-4367).
- No approval is needed to build against a Draft contract baseline; this story runs in Draft (realignment v1) until RWB-S2-E3007-CON is tagged.

### 4. Flow

1. rwb-case's `CaseWorkflow` starts `TreatmentWorkflow` as its child on task queue `rwb-treatment` when the route decision for R1 reaches the case; the parent forwards the case event to the running child as a signal and never calls the service directly (DP-12; Temporal and Drools Design slide 13, notes).
2. Step 1, receive: the workflow takes the case status and the facts it needs from the signal. It reads no case table and no `recovery_case` row (DP-01; ASM-4367).
3. Step 2, ask Drools: `EvaluateRules` runs the RESTRUCTURE package in force at the version announced by EV-30. R-RES-04 fires on `IN_FCR_QUEUE` with `CASE_PICKED_UP` when the allocation rule matched and an officer is available, and answers `WITH_FCR_OFFICER` (TSD S2 T4 R-RES-04).
4. Step 3 on R-RES-04: `recordAndApply` writes the stage outcome and reports it to the parent, which assigns the case and moves the status to `WITH_FCR_OFFICER`; the same apply step arms the offer-preparation clock as a durable Temporal timer for the value in force (ASM-4367, ASM-4368).
5. The officer prepares the offer — the plan terms of RWB-S2-E3004-APP or the settlement terms of RWB-S2-E3002-APP. Where the offer falls outside the approved range the case sits in `AWAITING_CREDIT_APPROVAL` under R-RES-10, and the credit answer arrives on the case signal.
6. Step 2 again on R-RES-11: `credit approved` fires on `AWAITING_CREDIT_APPROVAL` when `final_call = approved`, and the rule answers `OFFER_WITH_CUSTOMER` — release the offer and send it to the customer (TSD S2 T4 R-RES-11; Routing Logic v4 row R-RES-11).
7. `releaseOffer` activity: takes the offer facts, the release instant and the validity period in force, computes `validUntil` — the release date plus the period, a calendar-date addition — and returns the release facts. No date and no period is a constant (RWB-S2-E3007-CON; ASM-4368).
8. `recordAndApply` activity, one transaction: `valid_until` is written on the `treatment` row together with `decision_log_id`, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with `MANDATORY` so it joins this transaction and opens none, the EV-10 row is written to this service's outbox by the library, and the stage outcome for R-RES-11 is reported so the parent moves the case to `OFFER_WITH_CUSTOMER` (DP-03, DP-09; ADR-022).
9. `publishRelease` activity, after the commit: the outbox relay publishes `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` with key `caseId`; rwb-comms issues the letter on the consented channel and rwb-payment expects the money. The event carries no customer value (EV-10; DP-09).
10. Step 4, wait: `TreatmentWorkflow` waits on the durable validity timer or on the next signal, with MSG-S2-003 naming the date for the officer. On expiry the timer fires and the offer ends; the case move for expiry (R-RES-18) is the parent's. A customer counter-offer outside the current range raises R-RES-15: the case returns to the officer with the counter-offer and the gap, the validity date is recomputed from the new offer, and the same workflow carries it (Routing Logic v4 R-RES-15).
11. A repeat release for the same treatment answers the first result: one `valid_until`, one decision record, one timer and one event, never a second of each; the workflow ID and the Idempotency-Key of the operation carry the identity.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right U in capability area Treatment and offer calls the release | 403 before any read of the treatment; the refusal is the guard library's and is logged by it | MSG-P4-002 | TC-E3-007-05 |
| X2 | The release facts are incomplete: no offer amount, no release instant or no validity period in force | The release is refused before any write, with the field named; nothing changes | MSG-GEN-001 | TC-E3-007-01, TC-S2-E3007-CON-03 |
| X3 | The decision record cannot be written | The transaction rolls back, `valid_until` is not stored, no event leaves the outbox, the timer is not armed, and the user sees MSG-P7-003 | MSG-P7-003 | AC4, TC-E3-007-04, TC-E3-007-06 |
| X4 | A record field is refused by the library | Nothing changes and the field is named; the offer is not released | MSG-P7-009 | TC-S2-E3007-CON-04 |
| X5 | The rule answer is `CREDIT_DECLINED` under R-RES-12, or the customer declines or the offer expires under R-RES-17 and R-RES-18 | No release, no event and no timer; the case moves to `DECLINED_BY_CREDIT` or `RETURNED_TO_COLLINS` on the parent's move | None | Section 9 |
| X6 | The validity date is reached and no signature has arrived | The durable timer fires, the offer ends and the date is named; the expiry move is the parent's | MSG-S2-003 | TC-E3-007-01 |
| X7 | A consumer redelivers EV-10, or the same release arrives twice with one `Idempotency-Key` | The inbox dedupes by cloud event id and the workflow answers the first result: one release, one event, one timer | None | TC-E3-007-01 |

X1, X3, X6 and X7 are the exception paths of RWB-E3-007 carried onto the split; X2, X4 and X5 are the paths that the published release body, the `MANDATORY` record and the rule answers add (GAP-2658; ASM-4368).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3007-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON with their fakes, on `treatment` in its own schema; needs no live rwb-case, no live rwb-comms and no live ACE to start |
| Negotiable | The activity names, the timer field names and the log fields are this story's choice; the two rules, the `MANDATORY` record, the event name and the no-personal-data rule are fixed |
| Valuable | The offer reaches the customer and a validity date exists that both the officer and the record can prove, which is the 5-day turnaround of the FSD metric |
| Estimable | One workflow branch, four activities, one controller method, one repository and one timer |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, offer facts and case signals through the contract fakes, plus one component test of the release and the access answer |

### 7. Acceptance criteria

```gherkin
Feature: Send the offer and start the validity timer

  Scenario: AC1 Send the offer and start the validity timer (legacy RWB-E3-007 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the offer to the customer and starts the validity clock. The wait is a timer, not a routed state
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-04 (legacy RWB-E3-007 AC2)
    Given the rwb-case contract mock returns case status IN_FCR_QUEUE
    Given a case in state IN_FCR_QUEUE
    When case picked up
    Then assign the case to a restructuring officer and start the offer clock
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC3 Rule R-RES-11 (legacy RWB-E3-007 AC3)
    Given the rwb-case contract mock returns case status AWAITING_CREDIT_APPROVAL
    Given a case in state AWAITING_CREDIT_APPROVAL
    When credit approved
    Then release the offer and send it to the customer
    Then the case moves to OFFER_WITH_CUSTOMER

  Scenario: AC4 Not recorded (legacy RWB-E3-007 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line and every legacy value above is kept character for character, including the repeated `Then` of the legacy form; what changes is where it runs, who owns the fact and how it is reached. The trigger of AC1 is the case signal that reports R-RES-11 for a released offer, and the send is the EV-10 publication that rwb-comms consumes; the validity clock is a durable Temporal timer inside `TreatmentWorkflow`, armed in the same apply step that stores `valid_until`, and never a `timer` row or a case state (ASM-4368; Architecture v5 slide 42, event 18; Temporal and Drools Design slide 18). The decision log of AC1 and AC4 is the local `decision_record` written through `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_log_entry` is P7's central ledger and is neither written nor read here (DP-03, DP-01; Architecture v5 slides 20 and 42). The case states of AC2 and AC3 are rwb-case's and reach the stage on the case signal the parent forwards (EV-29); the `rwb-case contract mock` line stands for the case-status answer on that signal, not for a REST call and not for a table read, the assignment of AC2 is the parent's and the status move is the parent's (ASM-4367; DP-01). "Case picked up" of AC2 is R-RES-04 and "credit approved" of AC3 is R-RES-11 of the RESTRUCTURE package in force, whose version arrives on `rwb.decision.RulePackageInForce.v1` (EV-30) and is stamped on the record (ASM-4368). The offer clock that AC2 starts is the offer-preparation clock of R-RES-04 — two working days in the routing workbook — and the validity clock of AC1 and AC3 is the offer validity of fourteen days that R-RES-11 states; both are values in force and neither is a constant (GAP-2658; ASM-4368). The customer of AC1 and AC3 is reached through the letter that rwb-comms issues from EV-10: this story sends no customer field and reads no `v_ace_customer` row (GAP-2658; ASM-4366; DP-05).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On `IN_FCR_QUEUE` with `CASE_PICKED_UP`, when the allocation rule matched and an officer is available, the case is assigned to a restructuring officer and the offer clock starts; the case moves to `WITH_FCR_OFFICER` | TSD S2 T4 R-RES-04; Routing Logic v4 R-RES-04; FSD A2.7.3.1 |
| BR2 | On `AWAITING_CREDIT_APPROVAL` with `CREDIT_APPROVED`, when `final_call = approved`, the offer is released and sent to the customer; the case moves to `OFFER_WITH_CUSTOMER` | TSD S2 T4 R-RES-11; Routing Logic v4 R-RES-11; FSD A2.7.3.1 |
| BR3 | On `OFFER_WITH_CUSTOMER` with `CUSTOMER_COUNTER_OFFERED`, when `counter_amount` is outside the current range, the case returns to the officer with the counter-offer and the gap and a new validity date is computed | TSD S2 T4 R-RES-15; FSD A2.7.3.1 |
| BR4 | An offer carries a validity period; `valid_until` is the release date plus the period in force, and expiry returns the case to the status it came from through R-RES-18 | REQ-S2-002; TSD S2 T4 R-RES-18; RWB-S2-E3007-CON |
| BR5 | The wait is a timer, not a routed state: the validity clock is a durable Temporal timer inside `TreatmentWorkflow`, armed in the apply step and cancelled by a signature, a decline or a new offer | FSD A2.7.2; Architecture v5 slide 42 event 18; ASM-4368 |
| BR6 | No value a business person may change is written in code: the validity period, the offer-preparation clock and the rule version are read as values in force with their version | FSD A2.7.3.1 BR-S2-007; ASM-4368 |
| BR7 | The decision record is written in the same transaction as `valid_until` and the outbox row, or neither is stored and the officer is told the action was not taken | ADR-022; REQ-DRI-005; DP-03 |
| BR8 | The case status and the assignment are not rwb-treatment's to move: the stage reports the outcome of R-RES-04 and R-RES-11 to the parent `CaseWorkflow` and the parent moves the status, while the durable timers of this workflow are this story's | ASM-4367; DP-01 |
| BR9 | The offer is sent through EV-10 on `rwb.treatment.events.v1`: rwb-comms issues the letter and rwb-payment expects the money, and no customer value crosses the event | DP-09, DP-14; EV-10; ASM-4366 |
| BR10 | No ACE view is read to send the offer: the customer facts of the letter stay with the letter's owner and the letter resolves them on its own path | DP-05; Architecture v5 slide 8; ASM-4366 |

**Where each rule lives in the target.** BR1 and BR2 are the two rule outcomes this workflow reports: the RESTRUCTURE package decides them, the stage applies the release and the parent applies the status, so AC2 and AC3 assert the outcome report, the mock case status and the stored release, not a local status write (ASM-4367). BR3 is the counter-offer branch that rebuilds the offer inside the same workflow. BR4 and BR5 are the validity date and the timer: the period is a parameter and the timer is Temporal's, so a restart, a release or a Continue-As-New never loses the clock. BR6 is why no date, no period and no clock length appears as a literal. BR7 is the `MANDATORY` propagation of the record write. BR8 is the boundary with rwb-case. BR9 is the dispatch, and BR10 is the DP-05 boundary that retires the legacy `v_ace_customer` read.

### 9. State transitions

None of this story's own for the case: the case status is rwb-case's (DP-01; ASM-4367), and the `treatment` row's lifecycle states (Draft, submitted, approved, booked, broken) are set by RWB-S2-E3001-APP and the approval and booking stories. This story reports an outcome for each rule, writes `valid_until` and changes the state of its own `TreatmentWorkflow` execution and its durable timer.

| From | Rule and event | Condition | To (reported to the parent) |
|---|---|---|---|
| `IN_FCR_QUEUE` | R-RES-04, `CASE_PICKED_UP` | The allocation rule matched and an officer is available | `WITH_FCR_OFFICER`; the offer-preparation clock starts |
| `AWAITING_CREDIT_APPROVAL` | R-RES-11, `CREDIT_APPROVED` | `final_call = approved` | `OFFER_WITH_CUSTOMER`; the offer is released and EV-10 is published |
| `OFFER_WITH_CUSTOMER` | R-RES-15, `CUSTOMER_COUNTER_OFFERED` | `counter_amount` is outside the current range | `WITH_FCR_OFFICER`; the validity date is recomputed from the new offer |
| `OFFER_WITH_CUSTOMER` | validity timer fires | The validity date is reached with no signature | The offer ends and the date is named; the expiry move (R-RES-18) is the parent's |

| Workflow state | Meaning |
|---|---|
| RUNNING, waiting on the case signal | The stage is open and no offer has been released |
| RUNNING, waiting on the validity timer | An offer is in force with a `valid_until` date |
| COMPLETED | The stage ended: the customer signed, declined, or the offer expired |
| FAILED | The record write or the release validation failed and the apply step rolled back |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Primary: releases the offer, right U and A of capability area Treatment and offer (TSD S2 T6.1) |
| RW-CASEOWN, case owner | Also uses the treatment record and the offer, rights C, R and U |
| RW-SPECIAL, RW-GUARANT | Use the treatment record, rights C, R and U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT | Read only, right R |
| RW-PRODHEAD, RW-CREDCOMM | Read and approve, rights R and A; the approval itself is the credit approval child workflow's |
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the four activities, the controller method, the repository and the timer |
| rwb-case (P3) | Owns the case, the status, the assignment and the `timer` table; answers the case signal this stage receives |
| rwb-decision (P7) | Owns the rule package registry and the rule versions |
| rwb-comms (P6) | Owns the letter template, the channel and the consent check that turn EV-10 into the offer the customer receives |
| rwb-payment (P8) | Owns the expectation of the money that a released offer sets up |
| The platform workflow owner | Owns the `rwb-treatment` task queue, the namespace and the worker registration |
| No delegation of authority level applies | The story releases an offer that a person or a committee already approved; it makes no credit decision of its own |

The access check itself is the platform guard library's and is declared here as the capability area and the right only (ASM-4367; TSD S2 T6.1). No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry case IDs, treatment IDs, codes, dates and amounts only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-010 | treatment | valid_until | Write |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-030 | treatment | signature_status | Read |
| DF-DEC-001 to DF-DEC-018 | decision_record | the local record shape declared by RWB-PLT-E1027-CON | Write |
| DF-CAS-001 to DF-CAS-023 | recovery_case | the case status, read from the case signal only | Read (from the signal) |
| DF-WRK-009 to DF-WRK-016 | assignment | Not used: the assignment is written by rwb-case on this stage's outcome | Not read or written |
| DF-WRK-027 to DF-WRK-036 | timer | Not used: both clocks are durable Temporal timers | Not read or written |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer | Not used: the letter's addressee is resolved by rwb-comms, and no ACE view is read here | Not read or written |

The only business column this story writes is `valid_until` — with `decision_log_id`, which the record library sets (TSD S2 T3.1). The terms of the offer itself are written by the stories that build it. `decision_record` is written through the library and never by a repository of this story (DP-03, DP-01). `recovery_case`, `assignment` and `timer` are P3's: the case status arrives on the signal, the assignment is the parent's and both clocks are durable timers, so no row of those three tables is read or written (Ownership Map; ASM-4367). `v_ace_customer` is named in the legacy data table and is not read here: the 30 `recovery.v_ace_*` views are read only by rwb-source-data, and the letter's addressee is the consumer's concern (GAP-2658; ASM-4366; DP-05). Field identifiers are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story supplies the release form of the offer operation that RWB-S2-E3002-CON declares and the `OfferRelease` body that RWB-S2-E3007-CON declares; it declares no path, no envelope and no status code of its own.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/treatments/{treatmentId}/offer` (the release form) | Request `OfferRelease` of RWB-S2-E3007-CON — `treatmentId`, `releasedAt`, `validityDate` and the offer facts it names; response `Treatment` with `valid_until`; the operation, the envelope and the error set are those of RWB-S2-E3002-CON | Treatment and offer, right U, scope applied | `Idempotency-Key` header |
| GET | `/treatments/{treatmentId}` | `Treatment` of RWB-S2-E3002-CON; read to show the validity date the release stored, with the legacy row of the story's endpoint table | Treatment and offer, right R, scope applied | Not applicable |

The legacy story's endpoint table lists the treatment read and the treatment submit; the submit semantics named by API Specification v4 and TSD S2 T-A.1 API-S2-004 are carried by the offer operation that RWB-S2-E3002-CON publishes, and that form is not republished here (GAP-2659; ASM-4369). The errors are 400 or 422 with MSG-GEN-001 and the field name, 403 with MSG-P4-002, 404, 409, 503, and MSG-P7-003 and MSG-P7-009 on the record path; the envelope texts are RWB-S2-E3002-CON's and are not restated here.

#### 12.2 REST operations consumed

None. This story calls no service in its own name. The case status arrives on the case signal the parent `CaseWorkflow` forwards (EV-29), the rule package version arrives on `rwb.decision.RulePackageInForce.v1` (EV-30), and the offer facts arrive from the sibling workflow of RWB-S2-E3004-APP or RWB-S2-E3002-APP. The access answer is the guard library's in-process, and the decision record is written in process inside this transaction and calls nothing (DP-03). The `rwb-case contract mock` of AC2 and AC3 is the test-only stand-in for the case-status answer on the signal and adds no consumed operation, which is why the contract dependencies of this story are None (ASM-4367).

#### 12.3 Events published

| Event | Topic | Key | Body | Use |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | treatmentId, caseId, treatmentType, offerAmount, validityDate, approvalLevel, approverRole, finalCall, decidedAt, ruleId, ruleVersion — the body published by RWB-S2-E3007-CON | EV-10: tells rwb-comms to issue the released offer and rwb-payment to expect the money (Architecture v5 slide 42 row 10; DP-14) |

The event is written to this service's outbox in the same transaction as `valid_until` and the decision record, and the relay publishes it after the commit, as a CloudEvent of the platform envelope (DP-09; ADR-015). It carries no customer value: no name, no address, no account and no document (Template and Rules §R7.2 s17; DP-09). The same event is published by RWB-S2-E3003-APP on the below-floor approval path and by this story on the R-RES-11 release path; both use the one body this service publishes. A refused, declined or expired offer publishes nothing.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Announces the RESTRUCTURE package and its version; the workflow evaluates the version in force and stamps it on the release's record (EV-30) |

The event is consumed through the inbox of the outbox library, so a redelivery does not swap a package twice for one version. `rwb.payment.PaymentMissed.v1` (EV-12), `rwb.payment.TreatmentBooked.v1` (EV-11) and `rwb.deviation.DeviationRaised.v1` (EV-06) are consumed by rwb-case's case router and reach this stage as forwarded signals, not as subscriptions of this story (Architecture v5 slides 42 and 43; Temporal and Drools Design slide 13 notes).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage, with the four steps receive, evaluate, record and apply, wait | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, route set, case status on the signal; holds the offer facts, the validity date, the rule version and the durable validity timer; output: the stage outcomes of R-RES-04, R-RES-11 and R-RES-15 |
| `releaseOffer` | Activity | `rwb-treatment` | The offer facts and the validity period in force; `validUntil`, the release facts and the refusal with MSG-GEN-001 |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: `valid_until` on `treatment`, the decision record through the library, the EV-10 outbox row and the stage outcome reported to the parent |
| `publishRelease` | Activity | `rwb-treatment` | The post-commit check that the EV-10 row left the outbox; it writes no business row |
| `armValidityTimer` | Workflow timer | `rwb-treatment` | The durable validity timer from the release instant to `valid_until`, with MSG-S2-003 at expiry |

The workflow is the stage child named by Architecture v5 slide 18 and the Temporal and Drools Design slide 13 for rwb-treatment; the activity names are this story's design choice and are fixed by no source document (GAP-2658; ASM-4368). The retry policy is the workflow kit's: 1 s initial interval, back-off 2, 10 attempts, and no retry on a refused record (Temporal and Drools Design slide 14). The validity clock is a durable timer and not a Schedule, and the legacy timer check is retired with the `timer` table (ASM-4368; DP-10).

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` and advanced by signals and by its own durable timer; it owns no Temporal Schedule and no legacy Quartz job. The validity clock and the offer-preparation clock are durable timers inside the workflow, which is why no schedule entry and no polling job exists for them (ASM-4368; DP-10; Architecture v5 slide 42, event 18).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Created by the treatment story's Flyway version with the fields of TSD S2 T3.1; this story writes `valid_until` inside `recordAndApply` and creates no column |
| `decision_record` | `rwb_treatment` | PLT, a library object | Written through `DecisionRecordWriter.record(...)` in the same transaction; the shape and the DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Never read and never written here; the central ledger is P7's (DP-01) |
| `timer`, `recovery_case`, `assignment` | `rwb_case` | P3 | Never read and never written here; the case status arrives on the signal and both clocks are durable timers (ASM-4367) |

No table of another service is read and no foreign key crosses a schema (DP-01). The letter, its template and its addressee are rwb-comms' and are not stored here; the release leaves the treatment ID, the case ID and the validity date behind, and nothing else (BR9, BR10).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3007-CON release fake | The `OfferRelease` element, the validity rule and the EV-10 body | A complete release; a release missing the validity period; a release with a validity date before the release instant; the EV-10 envelope with its key |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with a chain sequence and an entry hash; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003; the outbox row present and absent after a rollback |
| rwb-case case-status mock | The case-status line of AC2 and AC3 | `IN_FCR_QUEUE` for AC2 and `AWAITING_CREDIT_APPROVAL` for AC3, on the forwarded signal; no case table and no case REST call |
| rwb-comms consumer stub | The EV-10 publication | A consumer that records the envelope and asserts the absence of a customer field; a redelivery of the same cloud event id |
| RWB-PLT-N001-CON route fake | The composite route of SCR-14 and SCR-15 | The two screen answers of the release, one hop each |

The release and decision-record fakes are the published contracts of those two stories, the consumer stub is test-only and stands for rwb-comms' subscription until the integration harness proves it live, and the route fake is the platform edge contract's (GAP-2658; ASM-4366).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/treatment/v1`, both declared elsewhere | None | OpenAPI 3.1; the controller validates and maps errors to problem responses |
| Kafka | 1 event (`rwb.treatment.TreatmentApproved.v1`, EV-10) | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic `rwb.treatment.events.v1` with retry and `.dlt`; inbox dedupe by cloud event id; the event leaves through the outbox |
| Temporal | None | `TreatmentWorkflow` and 4 activities on `rwb-treatment` | Namespace `rwb-recovery`; two durable timers; no Schedule |
| File | None | None | No file is read or written; the letter is rwb-comms' |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `offer` and `release`, with the published types in `...treatment.api` (DP-13, DP-14). Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this story reads none, because the letter's owner resolves its own addressee | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the release is built on: `valid_until`, the record and the outbox row are one commit or none is. DP-05 is applied by removal: the legacy send read `v_ace_customer` in process, and in the target no ACE view is read by this service because the views belong to rwb-source-data and the letter belongs to rwb-comms (BR10; ASM-4366). DP-13 fixes the base of the two operations, and DP-19 is the route by which the officer reaches SCR-14 and SCR-15. The other patterns of the service — the owner schema, the workflow kit, the outbox, the topic naming — are service-template capabilities and add no dependency of this story (ASM-4367).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (release branch) | Workflow | The four steps, the release state, the two durable timers and the outcome report to the parent |
| `releaseOffer` | Activity | Computes `validUntil` from the release instant and the period in force (BR4) |
| `recordAndApply` | Activity | One transaction: `valid_until`, the decision record, the outbox row and the outcome (BR7) |
| `publishRelease` | Activity | Confirms the EV-10 row left the outbox after the commit (BR9) |
| `TreatmentReleaseController` | Controller | The release form of the offer and the treatment read, with the access right and the error map (12.1) |
| `TreatmentRepository` | Repository | Reads the release facts and updates `valid_until` in `rwb_treatment` (DP-01) |
| `ValidityTimer` | Workflow timer | The durable validity clock from the release to the validity date (BR5) |
| `Migrations` | Migration | The `valid_until` column where the treatment story leaves it to this one, and no clock column (DP-15) |

**Database.** `treatment` holds the validity date in `valid_until` (DF-TRT-010) and the record reference in `decision_log_id` (DF-TRT-003). No send-date, channel or clock column exists: the release instant is a request-context fact recorded on the decision record, because TSD S2 T3.1 gives it no column (GAP-2658; ASM-4369). `decision_record` is the library object applied by this service's own Flyway sequence in `rwb_treatment`. There is no `timer` row for either clock, because both are durable timers inside the workflow (ASM-4368).

**Configuration and reference data.** The validity period of the offer and the length of the offer-preparation clock are values in force — the routing workbook gives fourteen days for the offer validity of R-RES-11 and two working days for the R-RES-04 clock — and are read as parameters and rule-package values, never as constants (BR6; ASM-4368). The RESTRUCTURE package and its version arrive on EV-30. The treatment-type, outcome and signature lists are reference data read through the owner's contract. The capability area "Treatment and offer" and the rights R and U are the access rows of the platform guard library, not constants of this story.

**Build steps**

1. The Flyway version that carries `valid_until` where the treatment story leaves it to this one and the library's `decision_record`, with no clock or send-date column (ASM-4369; DP-15).
2. `TreatmentWorkflow`'s release branch and its input record, registered on `rwb-treatment`, with the four steps and the outcome report to the parent (BR8).
3. The `EvaluateRules` call with the RESTRUCTURE package version from EV-30 and the R-RES-04, R-RES-11 and R-RES-15 outcome mapping (BR1, BR2, BR3).
4. `releaseOffer` with the validity rule and its refusal set (BR4; AC1).
5. `recordAndApply` with `valid_until`, the `MANDATORY` record write and the EV-10 outbox row (AC1, AC4).
6. `publishRelease` and the CloudEvent envelope with key `caseId`, asserted to carry no customer field (BR9).
7. The two durable timers, the recomputation on a counter-offer, and the expiry announcement (BR5; AC1).
8. The controller for the release form of the offer and the treatment read, with the access right and the error map (12.1).
9. Tests for AC1 to AC4 against the fakes and the offer fixture.

**Feature flag.** `rwb.treatment.offer-release-validity`.

**Done when.** The tests in section 16 pass, `TreatmentWorkflow` starts for a synthetic restructure case and reports R-RES-04 and R-RES-11, a released offer stores `valid_until` and one `decision_record` and one EV-10 row in one commit, the event carries no customer value, the validity timer fires at the validity date with MSG-S2-003, a forced record failure leaves nothing behind with MSG-P7-003, and SCR-14 shows the validity date through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-003 | The offer reaches its validity date | The offer to the customer ends on {date}. |
| MSG-GEN-001 | A release fact is missing or outside its type or domain | Enter {field}. |
| MSG-P4-002 | A role without the right in Treatment and offer calls the release | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. |
| MSG-S2-002 | The payoff the offer rests on is older than the freshness rule | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-001 | A settlement offer falls below the floor and goes for approval | The offer is below the floor of {floor}. It has been sent for approval. |

The seven texts are the legacy texts carried unchanged; MSG-S2-001 and MSG-S2-002 are raised by the settlement and payoff paths of the sibling stories and are named here because the legacy story carries them, MSG-P7-009 and MSG-P7-003 are the record library's, and MSG-P4-002 is the guard library's answer (RWB-PLT-E1027-CON; TSD S2 T6.1). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record with the states Draft, submitted, approved, booked and broken, and SCR-15 Settlement offer with the states Draft, below floor, approved, sent and accepted, show the validity date this story writes and the release state the officer works in. Both are reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment in parallel, one hop each (DP-19; RWB-PLT-N001-CON). SCR-14 shows the validity date, the days left and MSG-S2-003 when the date is reached; SCR-15 shows the same facts for a settlement offer. The screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-007-01 | AC1 | End to end | Send the offer and start the validity timer |
| TC-E3-007-02 | AC2 | End to end | Rule R-RES-04 |
| TC-E3-007-03 | AC3 | End to end | Rule R-RES-11 |
| TC-E3-007-04 | AC4 | End to end | Not recorded |
| TC-E3-007-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-007-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy level "System" maps to "End to end" for the four criteria and to "Component" for the Access and Principle 5 cases, as in the other stories of this run. Where the legacy Covers names `Access`, the criterion is the published answer of the platform guard library on the release; where it names `Principle 5`, the criterion is the `MANDATORY` record write of RWB-PLT-E1027-CON rolling the apply step back. The release fake, the decision-record fake, the rwb-comms consumer stub and the route fake of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the validity period, the offer-preparation clock, the dates and the rule version are values in force read from the parameters, the rule package and the reference data, never constants (BR6).
- No personal data in logs, events, workflow inputs or the fixture: the EV-10 body carries the case, the treatment, the amounts and the validity date only, and the letter's addressee is resolved by rwb-comms (DP-09; Template and Rules §R7.2 s17).
- No read of another service's table: the case status arrives on the forwarded signal, the rule package version on its event, and `recovery_case`, `assignment` and `timer` are never named in SQL (DP-01; ASM-4367).
- No read of an ACE view and no copied customer fact: `v_ace_customer` is retired from this path and the views stay with rwb-source-data (DP-05; ASM-4366).
- The decision record is written in the same transaction as `valid_until`, with `MANDATORY`; a forced failure leaves nothing behind and shows MSG-P7-003 (DP-03; BR7).
- The validity clock is a durable timer inside `TreatmentWorkflow`: no `timer` row, no polling job and no Schedule (BR5; ASM-4368).
- One release, one event: the outbox relay publishes EV-10 once per released offer and the consumers dedupe by cloud event id, so no second letter leaves on a retry (BR9).
- An applied migration is never edited: a correction to `valid_until` or to the record link is a new version on the service sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | Program, 5.9 | FEAT-TRT-07 | 07 Route, settle and claim | R-RES-04; R-RES-11; R-RES-18 | TC-E3-007-01, TC-E3-007-02, TC-E3-007-03 |
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Program, 5.9 | FEAT-TRT-07 | 07 Route, settle and claim | R-RES-04 | TC-E3-007-01, TC-E3-007-05 |
| REQ-S2-003 | A signed offer routes to operations for booking, and an unsigned or declined offer returns the case to its prior status | Program, 5.9 | FEAT-TRT-07 | 07 Route, settle and claim | R-RES-17; R-RES-18 | TC-E3-007-04, TC-E3-007-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3007-CON | Contract | H: declares the `OfferRelease` element, the validity rule, the EV-10 body and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and its `MANDATORY` transaction rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-15 |
| RWB-S2-E3003-CON | Contract | The same service's contract that declares the treatment offer rules of the below-floor path; named, not redeclared |
| RWB-S2-E3001-APP | App development | The treatment record, its states and `valid_until`'s column are that story's |
| RWB-S2-E3004-APP, RWB-S2-E3005-APP | App development | The plan offer, the affordability result and the band this story releases |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP | App development | The settlement offer, the range and the below-floor approval of the same feature family |
| RWB-P7-E1073-CON | Contract | The rule package registry that announces the RESTRUCTURE version on EV-30 |
| rwb-case (P3) | App development | The `CaseWorkflow` parent, the case status, the assignment and the `timer` table |
| rwb-comms (P6) | App development | The letter template, the channel and the consent check that turn EV-10 into the offer the customer receives |
| rwb-payment (P8) | App development | The expectation of the money a released offer sets up |
| The wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners |

### 19. Out of scope

- The `OfferRelease` element, the validity rule, the EV-10 body, the versioning rule and the fakes: RWB-S2-E3007-CON.
- The offer operation itself, the `Treatment` response and the error envelope: RWB-S2-E3002-CON.
- The treatment entity, its other fields and its states: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The plan offer, the affordability calculation and the band: RWB-S2-E3004-APP and RWB-S2-E3005-APP.
- The settlement range, the floor, the below-floor approval and the payoff freshness: RWB-S2-E3002-APP and RWB-S2-E3003-APP.
- The letter template, the consented channel, the consent check and the delivery evidence: rwb-comms (P6).
- The letter's addressee and the ACE customer facts behind it: rwb-source-data (P1) through its own contract; no view is read here.
- The decision-record library, its DDL template and the central ledger: RWB-PLT-E1027-CON, RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The rule package registry and the rule version labels: P7 rwb-decision, RWB-P7-E1073-CON.
- The case status, the assignment, the repair of a case to its prior status and the `timer` table: rwb-case (P3) and its stories, including R-RES-17 and R-RES-18.
- SCR-14 and SCR-15, their field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the release, the event and the letter: the wave 2 integration harness.

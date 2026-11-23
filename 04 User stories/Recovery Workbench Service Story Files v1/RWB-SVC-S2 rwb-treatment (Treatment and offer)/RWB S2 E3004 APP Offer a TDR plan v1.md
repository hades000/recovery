# RWB-S2-E3004-APP Offer a TDR plan

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-004 for rwb-treatment (S2, Treatment and offer). The plan offer leaves the monolith's in-process stage of `rwb-case` and becomes the plan branch of `TreatmentWorkflow`, the stage child that `CaseWorkflow` starts on task queue `rwb-treatment` (DP-12); the offer clock becomes a durable Temporal timer inside that workflow instead of a `timer` row; the band and the rule version arrive with the ACE affordability result of RWB-S2-E3005 and are applied, never written as constants; the local decision record is written in the same transaction as the plan terms through RWB-PLT-E1027-CON (DP-03); the plan body is published by RWB-S2-E3004-CON on the offer operation of RWB-S2-E3002-CON, under base `/api/recovery/treatment/v1` (DP-13); the screens are reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S2-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3004-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the Workbench to let the restructuring officer build and send the plan offer, with the band and the rule version applied**, so that **restructures and settlements reach booking in days**.

This is the application slice of legacy RWB-E3-004. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the data rows, the messages and the three rules they depend on;
- the plan branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery` — the stage child that `CaseWorkflow` of rwb-case starts for a restructure, with the four steps of every stage: receive the signal, ask Drools, record and apply in one transaction, then wait (DP-12; Architecture v5 slide 18, "TMP TreatmentWorkflow · settlement and DIL sagas"; Temporal and Drools Design slide 13, "Treatment · rwb-treatment · RES 37 · SET 27 · DIL 37", and slide 18);
- the plan form of `POST /treatments/{treatmentId}/offer` on base `/api/recovery/treatment/v1`: this story supplies the plan body and the plan steps, the `PlanOffer` element is declared by RWB-S2-E3004-CON and the operation itself is declared by RWB-S2-E3002-CON (DP-13; Architecture v5 slide 18);
- the plan terms written on `treatment` in schema `rwb_treatment` — `installments`, `installment_amount`, `interest_rate`, `first_due_date` and `valid_until` — inside the apply step of the workflow (DP-01);
- the band and the rule version applied from the ACE affordability result that RWB-S2-E3005 returns, and recorded with the offer, never as a column and never as a constant (GAP-1873; ASM-3069);
- the offer clock: a durable Temporal timer inside `TreatmentWorkflow`, started on the case signal that reports R-RES-04 and running to the validity date of the offer, with no `timer` row written (ASM-3069; Temporal and Drools Design slide 13, step 4 "Wait: durable timer or next signal", and slide 18, "Offer sent, valid 14 days");
- the stage outcome of R-RES-04 and R-RES-07 reported to the parent `CaseWorkflow`, which moves the case status (ASM-3062; DP-01);
- the local decision record of the offer, written in the same transaction as the plan terms through the library of RWB-PLT-E1027-CON (DP-03).

It does not own: the published shape of the offer operation, which is RWB-S2-E3002-CON, nor the published shape of the `PlanOffer` element, which is RWB-S2-E3004-CON; the ACE affordability calculation and its band, which are RWB-S2-E3005-APP and RWB-S2-E3005-CON; the settlement range check and the below-floor approval, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the treatment record creation and its contract, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the credit approval child workflow and the DoA levels, which are rwb-decision's; the case status, the assignment and the `timer` table, which are rwb-case's (DP-01); the decision-record library, which is RWB-PLT-E1027-CON and its APP story; the screens and their composite route, which are the platform edge story and the screen owners (DP-19); and the real cross-service proof, which is the wave 2 integration harness.

### 2. Business rationale

The FSD measures this feature by one number: restructure turnaround of 5 days, measured from the decision log and the Workbench records, reviewed monthly, against today's 23 to 26 days tracked by hand (FSD S2 v3, section A2.4.1). The plan offer is the step where that number is won or lost. The officer has to build the offer from the affordability result the ACE calculation returns, send it with a band and a validity period, and be able to prove afterwards which rule version produced which figure. Everything the officer needs therefore has to be in one place, in one transaction, when the offer leaves.

The legacy story did this inside `rwb-case`'s process: one schema, one decision log table, one `timer` row per clock and one in-process call to the affordability calculation. Architecture v5 moves each of those four facts. The stage becomes a child workflow of the service that owns treatments and plan timers (Architecture v5 slides 18 and 41, "S2 · rwb-treatment … treatments, contracts, settlement and deed-in-lieu agreements, plan timers"); the table becomes `treatment` in `rwb_treatment`; the clock becomes a durable timer inside the workflow, because the event catalogue retires `TimerDue` as "durable timer — retired: timer inside the workflow" (Architecture v5 slide 42, event 18); and the decision record becomes a local row written with the change in one transaction (DP-03; Architecture v5 slide 28). The band is not a Workbench value at all: it comes out of the ACE calculation and is applied at the moment of the offer, which is why the target records it with the offer and creates no column for it.

Two requirements carry the business value and no business value moves in this split. REQ-S2-001 asks that a restructure proposed in the collections system reach the restructuring officer with the case, and that the case not leave the Workbench; that is R-RES-04 and the stage hand-over. REQ-S2-002 asks that an offer carry a validity period and that expiry return the case to the status it came from; that is the offer clock of this story together with R-RES-18, which is the parent's move. The two rules, R-RES-04 and R-RES-07, are data rows of the route set held by the rule package in force, and the offer clock's length and the validity period are values in that package and in the parameters, never constants in this code (BR4; DP-04 is the service template's capability, ASM-3063).

### 3. Preconditions

- RWB-S2-E3004-CON is published: the `PlanOffer` element, its required and optional properties, its validation against the `treatment` field set of TSD S2 T3.1, the no-column rule for the band, the versioning rule and the fakes are baselined and handed to this story.
- The offer operation `POST /treatments/{treatmentId}/offer` is declared by RWB-S2-E3002-CON of the same service, on base `/api/recovery/treatment/v1` (DP-13; Architecture v5 slide 18). The Work Package's build list for this story is RWB-S2-E3004-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON, and this story adds nothing to it; the operation is named here, never redeclared.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, the refusal `MSG-P7-009`, the failure `MSG-P7-003`, and the DDL template of `decision_record` applied by this service's own Flyway sequence in `rwb_treatment` (DP-03, DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and SCR-15, one hop per call (DP-19).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with the 33 fields of TSD S2 T3.1 and the seven standard columns of T3.0, and the `rwb_treatment` login holds rights in that schema only (DP-01, DP-02).
- The restructure route set is in force: `TreatmentWorkflow` exists for a case whose route decision is R1, the RESTRUCTURE package and its version are the ones announced by `rwb.decision.RulePackageInForce.v1` (EV-30), and the embedded Drools runtime is the service template's wave-0 capability, so this story adds no build dependency of its own for it (ASM-3063; Temporal and Drools Design slides 13 and 15).
- RWB-S2-E3005-APP is the sibling that returns the ACE affordability result with its band and its rule version; until it is built, the result arrives from its workflow-state fixture and no band is ever assumed (GAP-1873; ASM-3069).
- The access guard is the platform guard library's, the outbox and inbox library and the workflow kit are the service template's, and the capability area and the right are declared here and checked there (ASM-3064; DP-19).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3004-CON when its tests pass, and this story runs in Draft (realignment v1) until it does.

### 4. Flow

1. rwb-case's `CaseWorkflow` starts `TreatmentWorkflow` as its child on task queue `rwb-treatment` when the route decision for R1 (restructure) reaches the case; the workflow ID is derived from the case and the stage, the child survives the parent's Continue-As-New because the parent close policy is ABANDON, and the search attributes are `CaseId`, `Stage`, `ProductGroup` and `QueueCode` (DP-12; Temporal and Drools Design slide 13).
2. The parent forwards the case event to the running child as a signal — EV-29, "CaseEvent (signal)" of Architecture v5 slide 43, from the case router, never a direct service call (Temporal and Drools Design slide 13, notes).
3. Step 1, receive: the workflow takes the case status and the facts it needs from the signal. It reads no case table and no `recovery_case` row (DP-01; ASM-3062).
4. Step 2, ask Drools: the `EvaluateRules` activity runs the RESTRUCTURE package in force, at the version announced by EV-30, under 300 ms in the owning service (ASM-3063; Temporal and Drools Design slide 15). R-RES-04 fires on `IN_FCR_QUEUE` with `CASE_PICKED_UP` when the allocation rule matched and an officer is available, and answers `WITH_FCR_OFFICER`.
5. Step 3, record and apply: the workflow writes the stage outcome for R-RES-04 and reports it to the parent, which assigns the case to the restructuring officer and moves the status to `WITH_FCR_OFFICER`; the workflow starts the offer clock as a durable Temporal timer for the validity period of the offer in the same apply step (ASM-3062, ASM-3069; TSD S2 T4 R-RES-04; Temporal and Drools Design slide 18, "Offer sent, valid 14 days" and "Clocks: Offer 14 days").
6. The case moves to `AFFORDABILITY_IN_ACE` under R-RES-06 (which is the affordability story's to raise); RWB-S2-E3005 returns the calculated plan with its band low and band high, the affordability outcome and the rule version that produced it.
7. R-RES-07 fires on `AFFORDABILITY_IN_ACE` with `AFFORDABILITY_PASSED`: the calculated plan is returned to the officer and the offer is built. The band is taken from that result at this moment and never read from a column (GAP-1873; ASM-3069; TSD S2 T4 R-RES-07).
8. The restructuring officer opens SCR-14 Treatment record or SCR-15 Settlement offer through the gateway-bff composite route, confirms the plan terms — installment count, installment amount, interest rate, first due date and validity date — and submits the plan on `POST /treatments/{treatmentId}/offer` with the `PlanOffer` body, one hop and 2 s timeout (DP-13, DP-19).
9. `buildPlanOffer` activity: maps the body to the plan columns of `treatment`, checks the required and optional properties of RWB-S2-E3004-CON, refuses a body that names a band column, and returns the record to apply.
10. `applyBand` activity: attaches the band, the affordability outcome and the rule version from the affordability result to the offer facts handed to the record step; the band is a request-context fact and is written nowhere but into the decision record (ASM-3069).
11. `recordAndApply` activity, in one transaction: the plan terms are written on the `treatment` row, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with `MANDATORY` so it joins this transaction and opens none, its `DecisionRecorded` event is written to this service's outbox by the library, and the stage outcome for R-RES-07 is reported so the parent moves the case to `WITH_FCR_OFFICER` (DP-03, DP-09; ADR-022).
12. Step 4, wait: the workflow waits on the durable offer timer or on the next signal. When the offer's validity date is reached the timer fires, the offer ends and MSG-S2-003 names the date; the case move for expiry (R-RES-18) is the parent's.
13. A customer counter-offer outside the current range raises `CUSTOMER_COUNTER_OFFERED` on `OFFER_WITH_CUSTOMER`; R-RES-15 returns the case to the officer with the counter-offer and the gap, the offer clock is recalculated from the new validity date, and a new offer is built on the same workflow (TSD S2 T4 R-RES-15; Business Rules and Routing Logic v4 row R-RES-15).
14. A repeat submit with the same `Idempotency-Key` returns the first answer: one offer, one decision record and one timer, never a second of each.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A role without the right in capability area Treatment and offer calls the offer | 403 before any read of the treatment; the refusal is the guard library's and is logged by it | MSG-P4-002 | TC-E3-004-05 |
| X2 | A required plan property is missing or out of its domain | 422 before any write, with the field named; nothing changes | MSG-GEN-001 | TC-E3-004-01, TC-S2-E3004-CON-04 |
| X3 | The body names a band column or a band as a stored value | The request is refused as a contract violation; the band is a request-context fact only | MSG-GEN-001 | TC-S2-E3004-CON-03 |
| X4 | The decision record cannot be written | The transaction rolls back, the plan terms are not stored, the offer is not sent, the timer is cancelled, and the user sees MSG-P7-003 | MSG-P7-003 | AC4, TC-E3-004-04, TC-E3-004-06 |
| X5 | A record field is refused by the library | Nothing changes and the field is named; the offer stays a draft | MSG-P7-009 | TC-S2-E3004-CON-04 |
| X6 | The affordability result is absent, superseded or carries no band | The offer cannot be built; the case stays in `AFFORDABILITY_IN_ACE` and the officer is asked to re-run the check; no band is assumed | None | Section 8, BR4 |
| X7 | The offer clock reaches the validity date | The durable timer fires, the offer ends and the date is named; the case move is the parent's | MSG-S2-003 | TC-E3-004-01 |
| X8 | The same submit arrives twice with one `Idempotency-Key` | One offer, one decision record and one timer; the first answer is returned | None | TC-E3-004-01 |

X1, X4 and X7 are the exception paths of RWB-E3-004 carried onto the split; X2, X3, X5 and X8 are the paths that the published `PlanOffer` contract and its `MANDATORY` record add, and X6 is the path the band being a request-context fact creates (GAP-1873; ASM-3069).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3004-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON with their fakes, on `treatment` in its own schema; needs no live rwb-case, no live rwb-decision and no live ACE to start |
| Negotiable | The activity names, the timer reset rule of a counter-offer and the metric and log fields are this story's choice; the plan columns, the two rules, the `MANDATORY` record and the no-column rule for the band are fixed |
| Valuable | The officer builds and sends a plan offer with the band and the rule version applied and can prove both afterwards, which is the 5-day turnaround of the FSD metric |
| Estimable | One workflow branch, three activities, one controller method, one repository, one timer and one test set |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on synthetic treatments, affordability results and case signals through the contract fakes, plus one component test of the controller and the access answer |

### 7. Acceptance criteria

```gherkin
Feature: Offer a TDR plan

  Scenario: AC1 Offer a TDR plan (legacy RWB-E3-004 AC1)
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the restructuring officer build and send the plan offer, with the band and the rule version applied
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-04 (legacy RWB-E3-004 AC2)
    Given the rwb-case contract mock returns case status IN_FCR_QUEUE
    Given a case in state IN_FCR_QUEUE
    When case picked up
    Then assign the case to a restructuring officer and start the offer clock
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC3 Rule R-RES-07 (legacy RWB-E3-004 AC3)
    Given the rwb-case contract mock returns case status AFFORDABILITY_IN_ACE
    Given a case in state AFFORDABILITY_IN_ACE
    When affordability passed
    Then return the calculated plan to the officer and build the offer
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC4 Not recorded (legacy RWB-E3-004 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line and every legacy value above is kept character for character, including the legacy repetition of `Then`; what changes is where it runs, who owns the fact and how it is reached. The screen of AC1 is SCR-14 Treatment record or SCR-15 Settlement offer, reached through the gateway-bff composite route (DP-19; Architecture v5 slides 18 and 41). The action of AC1 is the plan form of `POST /treatments/{treatmentId}/offer` on base `/api/recovery/treatment/v1` (DP-13): the operation is declared by RWB-S2-E3002-CON and the `PlanOffer` body is declared by RWB-S2-E3004-CON, and the legacy story's own endpoint table lists only `GET /treatments/{treatmentId}`, so its write path is published nowhere and the `/offer` form is the working read (GAP-1874; ASM-3070). The band of AC1 is the band the ACE affordability result returns, applied at the offer and recorded with it; it is not a column of `treatment` and never a constant, and the ACE calculation that produces it is RWB-S2-E3005-APP's (GAP-1873; ASM-3069; FSD S2 v3 section A2.4.3.1, BR-S2-004). The decision log of AC1 and AC4 is the local `decision_record` written through `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_log_entry` is P7's central ledger and is neither written nor read here (DP-03, DP-01; Architecture v5 slides 20 and 42). The case states of AC2 and AC3 are rwb-case's and reach the stage on the case signal the parent `CaseWorkflow` forwards (EV-29); the `rwb-case contract mock` line stands for the case-status answer on that signal, not for a REST call and not for a table read, and the status move itself is the parent's (ASM-3062; Architecture v5 slide 43, event 29; Temporal and Drools Design slide 13). "Case picked up" of AC2 is R-RES-04 of the RESTRUCTURE package in force, whose version arrives on `rwb.decision.RulePackageInForce.v1` (EV-30); the package and the embedded Drools runtime are the service template's wave-0 capability, so no build dependency is added for them (ASM-3063; TSD S2 T4 R-RES-04; Temporal and Drools Design slide 15). "Start the offer clock" of AC2 and the validity period of AC1 are one durable Temporal timer inside `TreatmentWorkflow`, not a `timer` row, because the `timer` table is rwb-case's and the five-minute timer check is retired (ASM-3069; Architecture v5 slide 42, event 18; Temporal and Drools Design slide 13, step 4, and slide 18, "Offer sent, valid 14 days"). "Affordability passed" and the calculated plan of AC3 are R-RES-07: the plan comes back from the ACE calculation with its band and its rule version, and the offer is built from it. The access answer behind the refusal path is the platform guard library's, and the story declares only the capability area and the right (ASM-3064; TSD S2 T6.1). The parent and child naming, the signal route and the four steps are Temporal and Drools Design slide 13, the stage content is slide 18, and the service contract rows are Architecture v5 slides 18 and 41.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | On `IN_FCR_QUEUE` with `CASE_PICKED_UP`, when the allocation rule matched and an officer is available, the case is assigned to a restructuring officer and the offer clock starts; the case moves to `WITH_FCR_OFFICER` | TSD S2 T4 R-RES-04; Routing Logic v4 R-RES-04; FSD A2.4.3.1 |
| BR2 | On `AFFORDABILITY_IN_ACE` with `AFFORDABILITY_PASSED`, when `affordability_result = pass`, the calculated plan is returned to the officer and the offer is built; the case moves to `WITH_FCR_OFFICER` | TSD S2 T4 R-RES-07; Routing Logic v4 R-RES-07; FSD A2.4.3.1 |
| BR3 | On `OFFER_WITH_CUSTOMER` with `CUSTOMER_COUNTER_OFFERED`, when `counter_amount` is outside the current range, the case returns to the officer with the counter-offer and the gap | TSD S2 T4 R-RES-15; Routing Logic v4 R-RES-15 |
| BR4 | No value a business person may change is written in code; the band, the validity period, the offer clock and the rule version are read as values in force with their version | FSD A2.4.3.1 BR-S2-004; ASM-3069 |
| BR5 | An offer carries a validity period, and expiry returns the case to the status it came from | REQ-S2-002; TSD S2 T4 R-RES-18 |
| BR6 | The decision record is written in the same transaction as the plan terms, or neither is stored and the officer is told the action was not taken | ADR-022; REQ-DRI-005; DP-03 |
| BR7 | The case status stays rwb-case's: the stage reports the outcome of R-RES-04 and R-RES-07 to the parent `CaseWorkflow` and the parent moves the status; no case table is read or written here | ASM-3062; DP-01; Architecture v5 slide 43 event 29 |
| BR8 | The plan terms are the columns of TSD S2 T3.1; the band arrives with the affordability result and is recorded with the offer, and no band column is created | GAP-1873; ASM-3069 |
| BR9 | The plan is submitted through `POST /treatments/{treatmentId}/offer`; `/treatments/{treatmentId}/submit` is not published | GAP-1874; ASM-3070 |

**Where each rule lives in the target.** BR1 and BR2 are the two rule outcomes this workflow reports: the RESTRUCTURE package decides them and the parent applies them, so AC2 and AC3 assert the outcome report and the mock case status, not a local status write (ASM-3062). BR3 is the counter-offer branch that rebuilds the offer inside the same workflow. BR4 is the reason `installment_amount`, `interest_rate`, the validity period and the offer clock length are read from the parameters and the rule package and never from a constant, and the reason the band arrives with the affordability result instead of being configured here. BR5 is the offer timer and the expiry path. BR6 is the `MANDATORY` propagation of the record write: the library joins this transaction or the apply step fails. BR7 is the boundary with rwb-case, and BR8 and BR9 are the two published-contract facts this story takes from its two sibling contracts.

### 9. State transitions

None of this story's own: the case status is rwb-case's (DP-01; ASM-3062), and the `treatment` row's lifecycle states (Draft, submitted, approved, booked, broken) are set by the contract story RWB-S2-E3001-APP and by the booking and approval stories. This story reports an outcome for each rule and changes the state of its own `TreatmentWorkflow` execution and its durable timer.

| From | Rule and event | Condition | To (reported to the parent) |
|---|---|---|---|
| `IN_FCR_QUEUE` | R-RES-04, `CASE_PICKED_UP` | The allocation rule matched and an officer is available | `WITH_FCR_OFFICER`; the offer clock starts |
| `AFFORDABILITY_IN_ACE` | R-RES-07, `AFFORDABILITY_PASSED` | `affordability_result = pass` | `WITH_FCR_OFFICER`; the offer is built from the calculated plan |
| `OFFER_WITH_CUSTOMER` | R-RES-15, `CUSTOMER_COUNTER_OFFERED` | `counter_amount` is outside the current range | `WITH_FCR_OFFICER`; the clock is recalculated from the new validity date |
| `OFFER_WITH_CUSTOMER` | offer timer fires | The validity date of the offer is reached | The offer ends and the date is named; the expiry move (R-RES-18) is the parent's |

| Workflow state | Meaning |
|---|---|
| RUNNING, waiting on the case signal | The stage is open and no offer has been built |
| RUNNING, waiting on the offer timer | An offer is in force with its validity date |
| COMPLETED | The stage ended; the offer was approved, expired or withdrawn by a later rule |
| FAILED | The record write or the contract validation failed and the apply step rolled back |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Primary: builds and sends the plan offer, right C, R, U and A of capability area Treatment and offer |
| RW-CASEOWN, case owner | Also uses the treatment record and the offer, rights C, R and U |
| RW-SPECIAL, RW-GUARANT | Use the treatment record, rights C, R and U (TSD S2 T6.1) |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE, SY-CASEWF, SY-RULES, SY-AGENT | Read only, right R |
| RW-PRODHEAD, RW-CREDCOMM | Read and approve, rights R and A |
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the three activities, the controller method, the repository and the timer |
| rwb-case (P3) | Owns the case, the status, the assignment and the `timer` table; answers the case signal this stage receives |
| rwb-decision (P7) | Owns the rule package registry, the rule versions and the credit approval child workflow |
| rwb-valuation (S1) | Owns the route decision that starts the restructure stage |
| The platform workflow owner | Owns the `rwb-treatment` task queue, the namespace and the worker registration |
| No delegation of authority level applies | The story applies the plan terms the officer confirms and the band the calculation returns; the DoA approval is the approval child workflow's |

The access check itself is the platform guard library's and is declared here as the capability area and the right only (ASM-3064; TSD S2 T6.1). No credential and no personal name appears in the workflow input, the activity payloads or the logs, which carry case IDs, treatment IDs, codes, dates and amounts only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-009 | treatment | installments | Write |
| DF-TRT-010 | treatment | valid_until | Write |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-012 | treatment | booked_at | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-014 | treatment | outcome_at | Read |
| DF-TRT-027 | treatment | interest_rate | Write |
| DF-TRT-029 | treatment | first_due_date | Write |
| DF-TRT-031 | treatment | installment_amount | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record | the local record shape declared by RWB-PLT-E1027-CON | Write |
| DF-REF-001 to DF-REF-015 | rule_row | rule ID, rule version and the labels the evaluated rule reports | Read |
| DF-WRK-027 to DF-WRK-036 | timer | Not used: the offer clock is a durable Temporal timer, and the `timer` table is rwb-case's | Not read or written |
| DF-CAS-001 to DF-CAS-023 | recovery_case | the case status, read from the case signal only | Read (from the signal) |
| DF-WRK-009 to DF-WRK-016 | assignment | Not used: the assignment is written by rwb-case on this stage's outcome | Not read or written |

The plan columns of `treatment` are the only business columns this story writes, and they are the five the `PlanOffer` element maps to: `installments`, `installment_amount`, `interest_rate`, `first_due_date` and `valid_until` (TSD S2 T3.1). The band is not a column: it arrives with the ACE affordability result and is recorded on the decision record with the offer (GAP-1873; ASM-3069). `decision_record` is written through the library and never by a repository of this story (DP-03, DP-01). `recovery_case`, `assignment` and `timer` are P3's: the case status arrives on the signal, the assignment is the parent's and the clock is a durable timer, so no row of those three tables is read or written here (Ownership Map; ASM-3062). `rule_row` is P7's and is read through the rule-package path, not from its table. Field identifiers are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story supplies the plan body and the plan steps of the offer operation that RWB-S2-E3002-CON declares, and the `PlanOffer` element that RWB-S2-E3004-CON declares; it declares neither of them again.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/treatments/{treatmentId}/offer` (the plan form) | Request `PlanOffer` of RWB-S2-E3004-CON — `installmentCount`, `installmentAmount`, `interestRate`, `firstDueDate`, `validUntil`, `bandLow`, `bandHigh`; response `Treatment` with the plan terms of section 11; the operation, the envelope and the error set are those of RWB-S2-E3002-CON | Treatment and offer, right U, scope applied | `Idempotency-Key` header |
| GET | `/treatments/{treatmentId}` | `Treatment` of RWB-S2-E3002-CON; read to show the plan terms the offer stored, with the legacy row of the story's endpoint table | Treatment and offer, right R, scope applied | Not applicable |

The two paths carry no operation of their own beyond the two contracts named above. The legacy story's endpoint table lists only the GET, while Architecture v5 slide 18 names `POST /treatments/{id}/offer` and API Specification v4 with TSD S2 T-A.1 API-S2-004 name `POST /treatments/{treatmentId}/submit`; the plan is submitted through `/offer` with the `PlanOffer` body and the TSD form is recorded as superseded (GAP-1874; ASM-3070). The errors are 400 or 422 with MSG-GEN-001 and the field name, 403 with MSG-P4-002, 404, 409, 503, and MSG-P7-003 when the record cannot be written; the envelope texts are RWB-S2-E3002-CON's and are not restated here.

#### 12.2 REST operations consumed

None. This story calls no service in its own name. The case status arrives on the case signal the parent `CaseWorkflow` forwards (EV-29), the affordability result arrives from the sibling workflow of RWB-S2-E3005, the band arrives with that result, and the rule package version arrives on `rwb.decision.RulePackageInForce.v1` (ASM-3062, ASM-3069; Architecture v5 slide 43 event 29). The access answer is the guard library's in-process; the decision record is written in process inside this transaction and calls nothing (DP-03). The `rwb-case contract mock` of AC2 and AC3 is the test-only stand-in for the case-status answer on the signal and adds no consumed operation to the Work Package's list, which fixes the contract dependencies of this story as None.

#### 12.3 Events published

None of this story's own. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14); its two service events `TreatmentApproved` and `TreatmentClosed` belong to the approval and closure stories. The offer writes no outbox row itself: the `DecisionRecorded` event on the shared topic `rwb.decision-record.v1` is written to this service's outbox by the decision-record library in the offer's transaction, and its envelope and key are that contract's (DP-03, DP-09; Architecture v5 slide 42, event 08).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Announces the RESTRUCTURE package and its version; the workflow evaluates the version in force and stamps it on the offer's record (EV-30) |

The event is consumed through the inbox of the outbox library, so a redelivery does not swap a package twice for one version. `rwb.payment.TreatmentBooked.v1` (EV-11), `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.deviation.DeviationRaised.v1` (EV-06) are consumed by rwb-case's case router and reach this stage as forwarded signals, not as subscriptions of this story (Architecture v5 slides 42 and 43; Temporal and Drools Design slide 13 notes).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage, with the four steps receive, evaluate, record and apply, wait | `rwb-treatment` in namespace `rwb-recovery` | Input: case ID, stage, route set, case status on the signal; holds the offer plan, the band, the rule version and the durable offer timer; output: the stage outcomes of R-RES-04, R-RES-07 and R-RES-15 |
| `buildPlanOffer` | Activity | `rwb-treatment` | The `PlanOffer` body and the treatment ID; the mapped plan columns, the validation answer and the refusal with MSG-GEN-001 |
| `applyBand` | Activity | `rwb-treatment` | The affordability result and the offer facts; the band low, the band high, the affordability outcome and the rule version attached to the record facts, written nowhere |
| `recordAndApply` | Activity | `rwb-treatment` | One transaction: the plan terms on `treatment`, the decision record through the library, the outbox row of the record event and the stage outcome reported to the parent |

The workflow is the stage child named by Architecture v5 slide 18 and the Temporal and Drools Design slide 13 for rwb-treatment; the three activity names are this story's design choice and are fixed by no source document (GAP-1873; ASM-3069). The retry policy is the workflow kit's: 1 s initial interval, back-off 2, 10 attempts, and no retry on a refused record (Temporal and Drools Design slide 14). The offer clock is a durable timer in this workflow and not a Schedule, and the legacy five-minute timer check is retired with the `timer` table (ASM-3069).

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` and advanced by signals and by its own durable timer; it owns no Temporal Schedule and no legacy Quartz job, and the timer check that the legacy build ran every five minutes is retired in favour of durable timers (ASM-3069; DP-10; Architecture v5 slide 42, event 18).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Created by the treatment story's Flyway version with the fields of TSD S2 T3.1; this story writes the five plan columns inside `recordAndApply` and creates no column |
| `decision_record` | `rwb_treatment` | PLT, a library object | Written through `DecisionRecordWriter.record(...)` in the same transaction; the shape and the DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Never read and never written here; the central ledger is P7's (DP-01) |
| `timer`, `recovery_case`, `assignment` | `rwb_case` | P3 | Never read and never written here; the case status arrives on the signal and the offer clock is a durable timer (ASM-3062) |

Architecture v5 slide 41 names contracts, settlement and deed-in-lieu agreements and plan timers in `rwb_treatment` as well, but TSD S2 T3.1 gives them no field list and the plan timer is a durable timer inside `TreatmentWorkflow`, not a row: this story therefore creates no table for them (GAP-1873; ASM-3069). No table of another service is read and no foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3004-CON plan-offer fake | The `PlanOffer` element and the plan form of the offer | A complete plan body; a body with a missing required property; a body naming a band column; a counter-offer outside the range |
| RWB-PLT-E1027-CON decision-record fake | The record write | An accepted record with a chain sequence and an entry hash; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003; the outbox row present and absent after a rollback |
| rwb-case case-status mock | The case-status line of AC2 and AC3 | `IN_FCR_QUEUE` for AC2 and `AFFORDABILITY_IN_ACE` for AC3, on the forwarded signal; no case table and no case REST call |
| RWB-PLT-N001-CON route fake | The composite route of SCR-14 and SCR-15 | The two screen answers of the plan offer, one hop each |
| Affordability result fixture | The result of RWB-S2-E3005 | A passed result with a calculated plan, a band low and high and a rule version; a result with no band; a failed result |

The plan-offer and decision-record fakes are the published contracts of those two stories, the route fake is the platform edge contract's, and the affordability fixture stands in for the sibling workflow of RWB-S2-E3005 until it is built; the case-status mock is test-only and is the signal answer recorded with ASM-3062 (GAP-1873; ASM-3069).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/treatment/v1`, both declared elsewhere | None | OpenAPI 3.1; the controller validates and maps errors to problem responses |
| Kafka | None of its own | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic `rwb.treatment.events.v1` for the service's own events; inbox dedupe by cloud event id; the record event goes out through the library's outbox |
| Temporal | None | `TreatmentWorkflow` and 3 activities on `rwb-treatment` | Namespace `rwb-recovery`; one durable offer timer; no Schedule |
| File | None | None | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `plan` and `offer`, with the published types in `...treatment.api` (DP-13, DP-14). Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule this story is built on: the plan terms and the record are one commit or neither is. DP-13 fixes the base of the two operations, and DP-19 is the route by which the officer reaches SCR-14 and SCR-15. The other patterns of the service — the owner schema, the workflow kit, the outbox — are service-template capabilities and add no dependency of this story (ASM-3063, ASM-3064).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` (plan branch) | Workflow | The four steps, the offer state, the durable offer timer and the outcome report to the parent |
| `buildPlanOffer` | Activity | Maps and validates the `PlanOffer` body against the plan columns (BR8) |
| `applyBand` | Activity | Attaches the band, the affordability outcome and the rule version from the affordability result (BR4) |
| `recordAndApply` | Activity | One transaction: the plan columns, the decision record, the outbox row and the outcome (BR6) |
| `TreatmentOfferController` | Controller | The plan form of the offer and the treatment read, with the access right and the error map (BR9) |
| `TreatmentRepository` | Repository | Reads and updates the plan columns of `treatment` in `rwb_treatment` (DP-01) |
| `OfferTimer` | Workflow timer | The durable offer clock from the case signal to the validity date (BR5) |
| `Migrations` | Migration | The plan columns on the per-service sequence where they are missing, and no band column (DP-15) |

**Database.** `treatment` holds the plan terms in `installments`, `installment_amount`, `interest_rate`, `first_due_date` and `valid_until` (DF-TRT-009, DF-TRT-031, DF-TRT-027, DF-TRT-029, DF-TRT-010). No band column exists: `bandLow` and `bandHigh` are request-context facts recorded on the decision record (BR8). `decision_record` is the library object applied by this service's own Flyway sequence in `rwb_treatment`. There is no `timer` row for the offer clock, because the clock is a durable timer inside the workflow (ASM-3069).

**Configuration and reference data.** The validity period of the offer and the length of the offer clock are values in force — the Temporal and Drools Design gives 14 days for the offer clock of S2 — and are read as parameters and rule-package values, never as constants (BR4; Temporal and Drools Design slide 18, "Offer 14 days"). The RESTRUCTURE package and its version arrive on `rwb.decision.RulePackageInForce.v1` (EV-30). The status and treatment-type lists are reference data read through the owner's contract (DP-07 is a service-template capability, ASM-3064). The capability area "Treatment and offer" and the rights C, R, U and A are the access rows of the platform guard library, not constants of this story.

**Build steps**

1. The Flyway version that carries the plan columns the treatment story leaves to this one and the library's `decision_record`, with no band column (BR8, DP-15).
2. `TreatmentWorkflow`'s plan branch and its input record, registered on `rwb-treatment`, with the four steps and the outcome report to the parent (BR7).
3. The `EvaluateRules` call with the RESTRUCTURE package version from EV-30, and the R-RES-04 and R-RES-07 outcome mapping (BR1, BR2).
4. `buildPlanOffer` with the `PlanOffer` validation and the refusal of a band column (BR8, AC1).
5. `applyBand` with the affordability result and the rule version (AC3).
6. `recordAndApply` with the plan columns, the `MANDATORY` record write and the outbox row (AC1, AC4).
7. The durable offer timer, its recalculated start on a counter-offer, and the expiry path (BR5).
8. The controller for the plan form of the offer and the treatment read, with the access right and the error map (BR9).
9. Tests for AC1 to AC4 against the fakes and the affordability fixture.

**Feature flag.** `rwb.treatment.tdr-plan-offer`.

**Done when.** The tests in section 16 pass, `TreatmentWorkflow` starts for a synthetic restructure case and reports R-RES-04, a submitted `PlanOffer` stores the five plan columns and one `decision_record` in one commit, the band and the rule version appear on the record and nowhere in `treatment`, the offer timer fires at the validity date with MSG-S2-003, a forced record failure leaves nothing behind with MSG-P7-003, and SCR-14 shows the plan terms through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the right in Treatment and offer calls the offer | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required plan property is missing or out of its domain | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. |
| MSG-S2-003 | The offer reaches its validity date | The offer to the customer ends on {date}. |
| MSG-S2-002 | The payoff the offer rests on is older than the freshness rule | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-001 | A settlement offer falls below the floor and goes for approval | The offer is below the floor of {floor}. It has been sent for approval. |

The seven texts are the legacy texts carried unchanged; MSG-S2-001 and MSG-S2-002 are raised by the settlement and payoff paths of the sibling stories and are named here because the legacy story carries them, MSG-P7-009 and MSG-P7-003 are the record library's, and MSG-P4-002 is the guard library's answer (RWB-PLT-E1027-CON; TSD S2 T6.1). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record with the states Draft, submitted, approved, booked and broken, and SCR-15 Settlement offer with the states Draft, below floor, approved, sent and accepted, carry the plan terms this story writes and the plan body the officer submits. Both are reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment in parallel, one hop each (DP-19; RWB-PLT-N001-CON). The plan form of SCR-14 shows the calculated plan the officer confirms, the band as a read-only fact of the affordability result, the validity date and the offer clock; the below-floor state of SCR-15 belongs to the settlement stories. The screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-004-01 | AC1 | End to end | Offer a TDR plan |
| TC-E3-004-02 | AC2 | End to end | Rule R-RES-04 |
| TC-E3-004-03 | AC3 | End to end | Rule R-RES-07 |
| TC-E3-004-04 | AC4 | End to end | Not recorded |
| TC-E3-004-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-004-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy level "System" maps to "End to end" for the four criteria and to "Component" for the Access and Principle 5 cases, as in the other stories of this run. Where the legacy Covers names `Access`, the criterion is the published answer of the platform guard library on the offer; where it names `Principle 5`, the criterion is the `MANDATORY` record write of RWB-PLT-E1027-CON rolling the apply step back. The plan-offer, decision-record and route fakes of section 12.8 stand behind every case, and the affordability fixture replaces the sibling workflow. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No business value in code: the validity period, the offer clock length, the band and the rule version are values in force read from the parameters, the rule package and the affordability result, never constants (BR4; TSD S2 T6.1).
- No personal data in logs, events, workflow inputs or the fixture: the rows carry case IDs, treatment IDs, codes, dates and amounts only; test data is synthetic and the case subject is never in a payload (DP-09).
- No read of another service's table: the case status arrives on the forwarded signal, the affordability result comes from the sibling workflow and the rule package version from its event; `recovery_case`, `assignment`, `timer` and `rule_row` are never named in SQL (DP-01, ASM-3062).
- No band column and no band constant: the band is the affordability result's fact, recorded with the offer and applied at the offer (BR8).
- The decision record is written in the same transaction as the plan terms, with `MANDATORY`; a forced failure leaves nothing behind and shows MSG-P7-003 (DP-03, BR6).
- The offer clock is a durable timer inside `TreatmentWorkflow`: no `timer` row, no five-minute check and no Schedule (ASM-3069).
- ACE data only through the owner's contract or the `v_ace_*` views: the affordability result and the restructure calculator are reached through their published paths and copied nowhere (DP-05 is a service-template capability, ASM-3064).
- An applied migration is never edited: a correction to the plan columns is a new version on the service sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Program, 5.9 | FEAT-TRT-04 | 07 Route, settle and claim | R-RES-04; R-RES-07 | TC-E3-004-01, TC-E3-004-02, TC-E3-004-03 |
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | Program, 5.9 | FEAT-TRT-04 | 07 Route, settle and claim | R-RES-15; BR5 | TC-E3-004-01, TC-E3-004-04, TC-E3-004-05, TC-E3-004-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3004-CON | Contract | H: declares the `PlanOffer` element, its validation and its fakes |
| RWB-S2-E3002-CON | Contract | The same service's contract that declares the offer operation and the `Treatment` response; named, not redeclared, and not added to the Work Package's build list |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and its `MANDATORY` transaction rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route of SCR-14 and SCR-15 |
| RWB-S2-E3001-APP | App development | The treatment record, its states and its own contract are that story's |
| RWB-S2-E3005-APP | App development | The ACE affordability calculation, the band and the rule version this story applies |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP | App development | The settlement range check and the below-floor approval of the same feature family |
| RWB-P7-E1073-CON | Contract | The rule package registry that announces the RESTRUCTURE version on EV-30 |
| rwb-case (P3) | App development | The `CaseWorkflow` parent, the case status, the assignment and the `timer` table |
| The wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners |

### 19. Out of scope

- The published `PlanOffer` element, its validation and its fakes: RWB-S2-E3004-CON.
- The offer operation itself, the `Treatment` response and the error envelope: RWB-S2-E3002-CON.
- The ACE affordability calculation, its band and its rule version: RWB-S2-E3005-APP and RWB-S2-E3005-CON.
- The treatment record creation, its states and its transitions: RWB-S2-E3001-APP; the settlement range check and the below-floor approval: RWB-S2-E3002-APP and RWB-S2-E3003-APP.
- The case status, the assignment, the queues and the `timer` table: rwb-case (P3), RWB-P3-E2004-APP and its contract; the case moves of R-RES-08, R-RES-09, R-RES-17 and R-RES-18.
- The credit approval child workflow and the DoA levels: rwb-decision (P7) and its approval contract.
- The decision-record library, its DDL template and its envelope: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP; the central ledger and its reads: RWB-P7-E1027-APP.
- The document child workflow, the e-sign and the contract document: rwb-document (P5) and its contract.
- The screens, their field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The offer of a settlement inside the range and the approval below the floor, and the deed-in-lieu and booking stages of `TreatmentWorkflow`: the sibling stories of this service.
- The real cross-service proof of the case signal, the affordability result and the record against the live owners: the wave 2 integration harness.

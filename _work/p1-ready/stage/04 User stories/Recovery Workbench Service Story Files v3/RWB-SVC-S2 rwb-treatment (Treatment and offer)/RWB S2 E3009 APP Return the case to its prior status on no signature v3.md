# RWB-S2-E3009-APP Return the case to its prior status on no signature

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-009 for rwb-treatment. The no-signature step leaves the monolith's in-process module call and becomes the no-signature branch of `TreatmentWorkflow` on this service's own task queue; the two rules R-RES-17 and R-RES-18 are evaluated locally from the RESTRUCTURE package in force; the prior status held in COLLINS arrives on the case answer of rwb-case and the outward restore of COLLINS and EFS is one hop on the contract rwb-integration publishes (DP-16 marker, no class C row on this key); the result is recorded on the treatment in `rwb_treatment` with its local decision record in the same transaction (DP-03); no ACE view is read by this story (DP-05); this story declares no REST operation of its own, so the legacy monolith base is not carried (DP-13); the two screens are reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3009-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-S2-E3009-APP-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-T |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3009-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-S2-E3009-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the no-signature branch of `TreatmentWorkflow` to evaluate R-RES-17 on a declined offer and R-RES-18 on an expired one, record the prior status the case held in COLLINS, return that status through the restore path rwb-integration publishes, and report `RETURNED_TO_COLLINS` to the parent case workflow** — so that **a restructure or settlement that the customer declines or lets lapse is back in its COLLINS status in days instead of after 23 to 26 days of hand tracking, and the route decision can re-open with the position written down**.

This is the application slice of legacy RWB-E3-009. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, data rows and messages they depend on;
- the no-signature branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`: the step that evaluates the RESTRUCTURE package, reports R-RES-17 from `OFFER_WITH_CUSTOMER` on `CUSTOMER_DECLINED` — `declined = Y` — and R-RES-18 from `OFFER_WITH_CUSTOMER` on `OFFER_EXPIRED` — `signed = N and offer_validity passed` — and reports the stage outcome to the parent `CaseWorkflow` (Business Rules and Routing Logic v4, Rules sheet rows R-RES-17 and R-RES-18; TSD S2 T4);
- the `restorePriorStatus` activity and the outward call it makes: one hop on the restore operation rwb-integration publishes, with the case ID, the prior status, the return reason and the rule version in the request and the restore reference in the answer (FSD A2.9.2 "Integration points: COLLINS, Workbench"; DP-16; ASM-4375);
- the prior status recorded against the treatment row in schema `rwb_treatment`, with the outcome event of the branch and the decision record in one transaction (DF-TRT-013, DF-TRT-014; DP-03);
- the local decision record of the step, written through `DecisionRecordWriter.record(DecisionRecord)` in the caller's transaction (DP-03; RWB-PLT-E1027-CON);
- the refusal path when the record cannot be written — nothing changes and the caller sees MSG-P7-003 — and the information message MSG-S2-003 that the offer ends on a date.

It does not own: the published contract of the restore element and the two consumed rows, which is RWB-S2-E3009-CON; the offer and its validity timer, which are RWB-S2-E3007-APP and start the clock this branch reacts to; the signed-offer route to operations, which is RWB-S2-E3008-APP; the treatment record and its read, which are RWB-S2-E3001-APP; the case, its status column and the parent `CaseWorkflow`, which are rwb-case's; the rule authoring and publication of the RESTRUCTURE package, which are P7 rwb-decision's; the COLLINS and EFS adapter itself, which is rwb-integration's and has no story on this key; the two screens and their composite route, which are the platform edge story's under DP-19; and the settlement expiry rule R-SET-11, which belongs to the settlement slice of this service and not to the restructure rules named here.

### 2. Business rationale

In the monolith the no-signature step was a method of `TdrSettlementAndDeedInLieuService` that wrote back to COLLINS through the module's outbound path and wrote the outcome into the `treatment` row and into `decision_log_entry`, inside the same process and the same `recovery` schema (TSD S2 T1 and T2; T5.1 INT-03 "Core bank (ALS)" and INT-26 "NLEADS"). The FSD gives the feature one sentence — "Sends the case back to the status it held in COLLINS when the customer declines or the offer expires" (A2.9.1) — and the routing logic gives the two rules, their from state and their to state, with `COLLINS, EFS, Workbench` as the systems column (rows R-RES-17 and R-RES-18).

What D-RCV-60 changes is the call type and the owner of the status, and nothing else. The status of a case is rwb-case's in v5: each stage is a child workflow on its owner's queue and reports its outcome, and the parent applies the rule to the status column (Temporal and Drools Design slide 13; Architecture v5 slide 3 "Step 2 Take over — rwb-case"). The outward write is not one of the 19 services' REST contracts: the module boundary of the monolith is replaced by the integration adapter rwb-integration, whose contract is the one place the external estate is reached (DP-16). And the result becomes a recorded fact on the treatment with its rule version, instead of a value in one module's memory and a row in a shared log.

Serves the A2.9.1 target of the FSD — restructure turnaround 5 days, measured from the decision log and the Workbench records — and the return leg of the route decision: R-RES-20 restores the status held before the restructure and re-opens the route decision, which is what makes a declined offer a next step rather than a dead case. No business value moves: the state names, the two rule IDs, the condition texts, the reason codes and the messages are the values of the routing logic, held as rule rows and reference data, never as code constants.

### 3. Preconditions

- RWB-S2-E3009-CON is published: the `PriorStatusRestore` element, its required and optional fields, the two consumed rows, the failure answer and the fakes. The build starts against the Draft baseline, as every CON story of this run publishes on Day 1 at status Draft (realignment v1; ASM-4378).
- The restore operation of rwb-integration, its request and answer fields and its 2 s budget are the working read of ASM-4375, because no source publishes them: the FSD names the integration points as "COLLINS, Workbench" (A2.9.2) and the routing logic names the systems as "COLLINS, EFS, Workbench", while the ownership rows of S2 carry no integration row (GAP-2663). The rwb-integration owner confirms both at the wave 2 contract freeze.
- RWB-PLT-E1027-CON is in place: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` transaction rule, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is in place, so the outcome reaches SCR-14 and SCR-15 through the gateway-bff composite route (DP-19).
- The service template's wave-0 capabilities are in place: the embedded Drools runtime and the rule-package loader that swaps a package on `rwb.decision.RulePackageInForce.v1`, the access guard library and the outbox and inbox library. This story adds no build dependency of its own for them, because the work package lists none.
- The `treatment` table exists on the per-service Flyway sequence of rwb-treatment with DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, and `decision_record` is created as the platform library object in `rwb_treatment`.
- The RESTRUCTURE package is in force in this service's rule cache at the version the answer names and carries R-RES-17, R-RES-18 and R-RES-20 with their conditions as rule rows, not as code.
- The case status is readable only as the stage sees it: the parent `CaseWorkflow` of rwb-case forwards the case signal to the running child, so the stage reacts to `OFFER_WITH_CUSTOMER` and to the prior status the answer carries, without reading the case table and without writing a case status (ASM-4376; DP-01).
- No approval stop: a Draft contract baseline is enough to build and test, and nothing in this story needs a human sign-off to start on Day 1.

### 4. Flow

1. RWB-S2-E3007-APP has sent the offer and started the validity clock as a durable timer of `TreatmentWorkflow`; the case is at `OFFER_WITH_CUSTOMER` and `treatment.valid_until` holds the date the offer ends (DF-TRT-010; MSG-S2-003).
2. Either event reaches the stage on the case signal: `CUSTOMER_DECLINED` with `declined = Y`, or `OFFER_EXPIRED` with `signed = N` once `offer_validity` has passed. The inbox dedupes by the cloud event id of the signal.
3. `EvaluateRules` runs the RESTRUCTURE package in force: `CUSTOMER_DECLINED` returns R-RES-17, `OFFER_EXPIRED` returns R-RES-18, each with its action "Return the case to its prior status in COLLINS" and the to state `RETURNED_TO_COLLINS`.
4. The stage reads the prior status from the case answer — the status the case held before the restructure — and the return reason the rule names. It does not read a COLLINS table, an ACE view or the case table (DP-05; ASM-4376).
5. `restorePriorStatus` calls the restore operation of rwb-integration with the case ID, the prior status, the return reason and the rule version, synchronously, inside the 2 s budget of the one-hop rule, and receives the restore reference.
6. `RecordAndApply`, one transaction: `treatment.outcome` and `treatment.outcome_at` take the branch's outcome, the `PriorStatusRestore` element is recorded against the treatment, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with the rule ID and the rule version in the final call, and the parent receives the stage report `RETURNED_TO_COLLINS` with the prior status and the restore reference.
7. rwb-case applies R-RES-17 or R-RES-18 for the status and moves the case to `RETURNED_TO_COLLINS`; this service writes no case row and publishes no case event for it (ASM-4376).
8. When the restore is confirmed, the stage reports `PRIOR_STATUS_RESTORED`; the parent applies R-RES-20, restores the status held before the restructure and re-opens the route decision at `BACK_TO_ROUTE_DECISION`. The route decision itself is rwb-valuation's and rwb-case's, not this stage's.
9. The adapter does not answer inside the budget: the activity is retried by the workflow's retry policy; when the attempts are exhausted the stage stays in `OFFER_WITH_CUSTOMER`, nothing is written and the caller sees MSG-GEN-006 naming rwb-integration. A second signal for the same branch does not cause a second restore.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The restore operation does not answer inside the 2 s budget, or the adapter is unavailable | The workflow retries per its policy; when the attempts are exhausted the stage stays in `OFFER_WITH_CUSTOMER`, nothing is written and the case does not move | MSG-GEN-006 | AC1, AC3 |
| X2 | The decision record cannot be written | The transaction rolls back: no outcome, no restore element, no stage report and no outward restore | MSG-P7-003 | AC4 |
| X3 | The record is refused for a missing field | Nothing is written, the field is named and the incident carries MSG-P7-009 | MSG-P7-009 | AC5, Section 12.8 |
| X4 | The case answer carries no prior status | The stage does not invent one: it reports the gap to the parent, keeps the case where it is and raises a task for the case owner | MSG-GEN-006 | AC2, AC3 |
| X5 | A role without the right tries to trigger the branch or read its outcome | 403 from the access guard and nothing changes; the run itself is unattended under the service identity and is not a user action | MSG-P4-002 | AC1, AC2, AC3 |
| X6 | The RESTRUCTURE package is not in force, or its checksum does not match | `EvaluateRules` answers `NoPackageInForce`; the workflow does not retry that answer and the stage does not call the adapter | MSG-GEN-006 | AC6, Section 12.4 |
| X7 | The offer is inside its validity and the customer has neither declined nor signed | Neither rule fires: the branch waits on the durable timer of RWB-S2-E3007-APP and writes nothing | None | AC7, Section 4 |
| X8 | A second `CUSTOMER_DECLINED` or `OFFER_EXPIRED` signal arrives after the restore | The inbox dedupes by cloud event id and the restore call is idempotent on the case and the rule version, so no second restore is made | None | AC8, Section 12.5 |
| X9 | The customer counters before the offer lapses | R-RES-15 takes the case back to the officer; this branch does not fire and writes nothing | None | AC9, Section 9 |

X1, X2, X5 and X7 are the legacy paths of RWB-E3-009 carried onto the split; X2 and X3 are the record library's refusal and failure paths, X4 is the split's new path for a status the case cannot supply, X6 is the rule loader's no-package answer, and X8 and X9 are the inbox dedupe and the counter-offer rule on the same state.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3009-CON, the decision-record library and the gateway route; the restore adapter is mocked and never called live, so the story needs no COLLINS or EFS connection to start |
| Negotiable | The activity name, the record shape of the stage report and the retry numbers are this story's choice; the two rules, their conditions, the states, the reason codes and the messages are fixed |
| Valuable | A declined or lapsed offer returns the case to its COLLINS status in days and the position is written down with its rule version |
| Estimable | One workflow branch, one activity, one adapter client, one outcome write, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic case and an adapter fake, plus one component test of the refusal path and one of the missing prior status |

### 7. Acceptance criteria

```gherkin
Feature: Return the case to its prior status on no signature

  Background:
    Given treatment "TRT-SYN-0901" of case "RW-2026-000909" is a RESTRUCTURE offer and the case is at OFFER_WITH_CUSTOMER
    Given the RESTRUCTURE rule package in force is version "RESTRUCTURE-2026.11" and carries R-RES-17, R-RES-18 and R-RES-20

  Scenario: AC1 Return the case to its prior status on no signature (legacy RWB-E3-009 AC1)
    Given the rwb-integration contract mock returns the prior status held in COLLINS with its restore reference
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the case back to the status it held in COLLINS when the customer declines or the offer expires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-17 (legacy RWB-E3-009 AC2)
    Given the rwb-case contract mock returns case status OFFER_WITH_CUSTOMER and the prior status the case held
    Given a case in state OFFER_WITH_CUSTOMER
    When customer declined
    Then return the case to its prior status in COLLINS
    Then the case moves to RETURNED_TO_COLLINS

  Scenario: AC3 Rule R-RES-18 (legacy RWB-E3-009 AC3)
    Given the rwb-case contract mock returns case status OFFER_WITH_CUSTOMER and the prior status the case held
    Given a case in state OFFER_WITH_CUSTOMER
    When offer expired
    Then return the case to its prior status in COLLINS
    Then the case moves to RETURNED_TO_COLLINS

  Scenario: AC4 Not recorded (legacy RWB-E3-009 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 A record refused for a missing field writes nothing and raises MSG-P7-009 (new, D-RCV-60)
    Given the decision record is refused for a missing field
    When the action is taken
    Then nothing is written, the field is named and the incident carries MSG-P7-009

  Scenario: AC6 A RESTRUCTURE package not in force is refused without a retry (new, D-RCV-60)
    Given the RESTRUCTURE rule package is not in force or its checksum does not match
    When the stage evaluates the rules
    Then EvaluateRules answers NoPackageInForce, the workflow does not retry and the stage does not call the adapter
    Then the user sees MSG-GEN-006

  Scenario: AC7 An offer inside validity with no decline and no signature waits (new, D-RCV-60)
    Given the offer is inside its validity and the customer has neither declined nor signed
    When the stage evaluates the rules
    Then neither rule fires, the branch waits on the durable timer of RWB-S2-E3007-APP and writes nothing

  Scenario: AC8 A repeated decline or expiry after the restore makes no second restore (new, D-RCV-60)
    Given the case has been restored by this branch
    When a second CUSTOMER_DECLINED or OFFER_EXPIRED signal arrives
    Then the inbox dedupes by cloud event id and no second restore is made

  Scenario: AC9 A counter-offer returns the case to the officer and this branch does not fire (new, D-RCV-60)
    Given a case in state OFFER_WITH_CUSTOMER
    When the customer counters before the offer lapses
    Then R-RES-15 takes the case back to the officer and this branch writes nothing

  Scenario: AC10 A prior status restored from RETURNED_TO_COLLINS re-opens the route decision (new, D-RCV-60)
    Given a case in state RETURNED_TO_COLLINS
    When PRIOR_STATUS_RESTORED arrives on any condition
    Then the route decision re-opens at BACK_TO_ROUTE_DECISION and the status move stays with rwb-case

  Scenario: AC11 A case answer without a prior status is not guessed (new, D-RCV-60)
    Given the rwb-case contract mock returns case status OFFER_WITH_CUSTOMER and no prior status
    When customer declined
    Then the stage does not invent a prior status, reports the gap to the parent and keeps the case where it is
    Then the user sees MSG-GEN-006

  Scenario: AC12 A redelivered consumed event makes no second restore (new, D-RCV-60)
    Given the case has been restored by this branch
    When the same CUSTOMER_DECLINED or OFFER_EXPIRED cloud event is redelivered
    Then the inbox dedupes by cloud event id and no second restore is made

  Scenario: AC13 A restore that does not answer in budget is retried and then stops (new, D-RCV-60)
    Given the restore operation does not answer inside the time budget of X1
    When the restore activity runs
    Then the workflow retries per its policy and, when the attempts are exhausted, the stage stays in OFFER_WITH_CUSTOMER and nothing is written
    Then the user sees MSG-GEN-006

  Scenario: AC14 A status change the model does not allow is refused (new, D-RCV-60)
    Given the case is in a state the branch does not start from
    When CUSTOMER_DECLINED or OFFER_EXPIRED arrives
    Then the transition is refused and nothing changes
```

**Target reading.** Every legacy line keeps its wording; what changes is where it runs, who owns the status and how the outward write is reached. "Sends the case back to the status it held in COLLINS" is no longer a method of the monolith's module writing through its own outbound path: the case status is rwb-case's and is moved by the parent `CaseWorkflow` on the stage report `RETURNED_TO_COLLINS` (ASM-4376), while the outward restore of COLLINS and EFS is one hop on the operation rwb-integration publishes, faked in every test (DP-16; ASM-4375). rwb-integration owns the COLLINS and EFS interface, its retries and its exception queue, so this service holds the prior status and never writes to COLLINS directly (GAP-1697). "Writes the result to the decision log with the rule version" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction with MSG-P7-003 on failure (DP-03), and `decision_log_entry` stays P7's and is never written here. "Customer declined" and "offer expired" are the two rule events of the routing logic with their conditions `declined = Y` and `signed = N and offer_validity passed`; no threshold, date or reason code is a code constant. The prior status is a value on the case answer and the restore reference is a value on the adapter's answer, and neither is read from an ACE view: DP-05 applies here as the rule that the service reads no ACE table and no `v_ace_*` view of its own for this step.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | From `OFFER_WITH_CUSTOMER`, on `CUSTOMER_DECLINED`, when `declined = Y`, the case is returned to its prior status in COLLINS and moves to `RETURNED_TO_COLLINS` | R-RES-17; TSD S2 T4 |
| BR2 | From `OFFER_WITH_CUSTOMER`, on `OFFER_EXPIRED`, when `signed = N and offer_validity passed`, the case is returned to its prior status in COLLINS and moves to `RETURNED_TO_COLLINS` | R-RES-18; TSD S2 T4 |
| BR3 | From `RETURNED_TO_COLLINS`, on `PRIOR_STATUS_RESTORED`, on any condition, the status held before the restructure is restored and the route decision re-opens at `BACK_TO_ROUTE_DECISION`; the status move is rwb-case's and the re-decision is rwb-valuation's | R-RES-20 |
| BR4 | The prior status is the status the case held before the restructure; it arrives on the case answer and is recorded, never guessed and never read from ACE or COLLINS directly | ASM-4376; DP-05 |
| BR5 | The outward restore of COLLINS and EFS is one hop on the restore operation rwb-integration publishes, inside the 2 s budget; this service owns no external connection and no adapter | DP-16; ASM-4375 |
| BR6 | The outcome and the restore element are written with their decision record in one transaction; if the record cannot be written, nothing changes and MSG-P7-003 is shown | DP-03; RWB-PLT-E1027-CON; ADR-022 |
| BR7 | The rule version that decided is written on the record and on the restore element; no rule ID, state name, reason code, validity period or timer value is written in code, it is read from the package in force and from reference data | BR-S2-009 of FSD A2.9.3.1; EV-30 |
| BR8 | A counter-offer takes the case back to the officer under R-RES-15 and this branch does not fire; the two branches are mutually exclusive on one state | R-RES-15 |

**Covered by.** BR1 AC2; BR2 AC3; BR3 AC10; BR4 AC11; BR5 AC1; BR6 AC4; BR7 AC1; BR8 AC9. The test cases for these criteria are in section 16.

**Where each rule lives in the target.** BR1 and BR2 are the two rows of the RESTRUCTURE decision table this story evaluates; the states they name are rwb-case's, and the stage reacts to the state it is signalled and reports the outcome (ASM-4376). BR3 is the restart rule: its from state is the state this branch produces, so the table row is read here but applied by the parent. BR4 is the split's data rule and the reason X4 exists — a case answer without a prior status stops the branch rather than fabricating one. BR5 is the call type of `restorePriorStatus`. BR6 is the `MANDATORY` propagation of the library write. BR7 is why the package version is an input of the call and a field of the element. BR8 is the guard that keeps the two offer outcomes apart.

### 9. State transitions

None of the case statuses below is this service's. The table shows the three rules as the stage reports them and names the owner of the status column, so a reader can see what this story sends and what it never writes.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-RES-17 | `OFFER_WITH_CUSTOMER` | `CUSTOMER_DECLINED` | `declined = Y` | Evaluates the rule, calls the restore adapter, records the outcome and the element, reports `RETURNED_TO_COLLINS` with the prior status | `RETURNED_TO_COLLINS` |
| R-RES-18 | `OFFER_WITH_CUSTOMER` | `OFFER_EXPIRED` | `signed = N and offer_validity passed` | Same branch on the expiry event, with the validity date recorded | `RETURNED_TO_COLLINS` |
| R-RES-20 | `RETURNED_TO_COLLINS` | `PRIOR_STATUS_RESTORED` | Any | Reports the confirmed restore; the parent restores the status held before the restructure | `BACK_TO_ROUTE_DECISION` |
| R-RES-15 | `OFFER_WITH_CUSTOMER` | `CUSTOMER_COUNTER_OFFERED` | `counter_amount outside the current range` | Does nothing: the counter-offer branch of the offer story takes the case | `WITH_FCR_OFFICER` |

The states of this story's own objects are the treatment's (`Draft`, `submitted`, `approved`, `booked`, `broken`, as SCR-14 shows them) and they belong to the sibling stories of this service; `treatment.outcome` takes the outcome event of the branch from LOV-TRT-OUTCOME where a value fits and stays empty where the reference data has none, and the reason code is carried on the restore element. The `TreatmentWorkflow` execution of a case has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the adapter call is an activity and not a workflow-local computation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the activity, the adapter client, the outcome write and the tests |
| RW-RESTRUCT, restructuring officer (FCR) | Holds right R on the capability area and sees the outcome on the treatment; the branch itself runs unattended |
| RW-CASEOWN, RW-TEAMMGR and the read-only roles of TSD S2 T6.1 | Right R only: they read the outcome and the restore reference and cannot trigger the branch |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity; the stage reports to the parent and takes no status of its own |
| rwb-case (P3) | Owns the case, its status and the status column of R-RES-17, R-RES-18 and R-RES-20; forwards the case signal to this child workflow |
| rwb-integration (P2) | Owns the restore operation, the COLLINS and EFS adapters and their availability (DP-16) |
| P7 rwb-decision | Owns the RESTRUCTURE package, its approval, its effective date and the central ledger |
| The platform workflow owner | Owns the `rwb-treatment` task queue, the namespace and the retry policy of the kit |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right R on each entry point and calls the guard, and it implements no rule of its own. No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the treatment ID, codes, dates, the prior status and the rule version only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read (the row this step records against) |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-010 | treatment | valid_until | Read (the offer end, MSG-S2-003) |
| DF-TRT-013 | treatment | outcome | Write (from LOV-TRT-OUTCOME, where a value fits) |
| DF-TRT-014 | treatment | outcome_at | Write |
| DF-TRT-030 | treatment | signature_status | Read (`NOT_SIGNED` on the expiry branch) |
| DF-DEC-002 to DF-DEC-016 | decision_record | the seven field groups | Write |
| Not specified in the source documents (GAP-2663; ASM-4376) | treatment | the prior status held in COLLINS and the restore reference | Write |

`treatment` is this service's own table, written in `rwb_treatment` through its own repository and login; it is never read from another service (DP-01). The prior status and the restore reference have no field in TSD S2 T3.1 and no BR Field ID in the Logical Data Model, so their names are the working read of ASM-4376 and their identifiers wait for the contract freeze (GAP-2663). `decision_record` is the platform library object created in this schema and written only through `DecisionRecordWriter`; `decision_log_entry` is P7's and is never named in SQL here (DP-03). The case, its status and the prior status are not read from a table: they arrive on the case signal the parent forwards (ASM-4376).

### 12. Contract

#### 12.1 REST operations provided

None. This story declares no REST operation of its own and adds no path to base `/api/recovery/treatment/v1` (DP-13): the branch is triggered by the case signal and its outcome is read through the treatment read owned by the sibling story RWB-S2-E3001-APP (API-S2-002 of TSD S2 T-A.1). The element, the consumed rows and the fakes are declared by RWB-S2-E3009-CON and are not restated here.

#### 12.2 REST operations consumed

None as an OpenAPI operation of the 19 services. The two rows this story reads are one hop each on the contract their owner publishes, with a 2 s budget and no chain, and neither operation name is published in a source: the case row is the case answer of rwb-case and the restore row is the operation rwb-integration publishes for the COLLINS and EFS write (DP-16; DP-11; ASM-4375). Until those names are published the clients are built against the documented use of section 12.8 and their fakes.

#### 12.3 Events published

None. The service's topic is `rwb.treatment.events.v1` with names `rwb.treatment.<Event>.v1` (DP-14), and its event EV-10 `TreatmentApproved` belongs to the offer story of this service. This story publishes no event and writes no outbox row of its own; the stage report to the parent is a Temporal signal inside the case, not a Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Loads the RESTRUCTURE package, verifies its checksum, swaps it atomically and keeps the last good package on failure; EV-30 |

The event is consumed by the service template's rule loader, and this story reads the version it put in force. `rwb.payment.PaymentMissed.v1` and `rwb.deviation.DeviationRaised.v1` are the other consumed events the service has available; they drive the cure-period and deviation branches, which belong to the closure and deviation stories and not to this one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (the no-signature branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-treatment` in namespace `rwb-recovery` | Input: the case ID, the treatment ID, the case status on the signal, the prior status, the event. Output: the stage report `RETURNED_TO_COLLINS` or `PRIOR_STATUS_RESTORED` with the restore reference |
| `EvaluateRules` | Activity of the template | `rwb-treatment` | The RESTRUCTURE package version in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `restorePriorStatus` | Activity | `rwb-treatment` | The request of 12.2 of RWB-S2-E3009-CON: case ID, prior status, return reason, rule version; the answer: the restore reference and the restored status; one hop on rwb-integration's operation, 2 s budget, retried by the workflow |
| `RecordAndApply` | Activity of the template | `rwb-treatment` | The outcome, the restore element, the decision record and the stage report in one transaction |

The workflow name is fixed by the target design and the three activity names by this story. The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts); `NoPackageInForce` is not retryable. The restore call is idempotent on the case ID and the rule version, so a replay never restores twice.

#### 12.6 Schedules

None. The step is signal-driven from the case and owns no Temporal Schedule and no legacy Quartz job; the offer validity clock is the durable timer of the workflow started by RWB-S2-E3007-APP, not a schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Created by the per-service Flyway sequence and written here for the outcome and the restore element; DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1 |
| `decision_record` | `rwb_treatment` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). The reference data read here is the outcome list LOV-TRT-OUTCOME under the reference-data contract of DP-06, and the parameters are read under the parameter contract of DP-07; their keys are Not specified in the source documents (DOR-RWB-S2-E3009-APP-20). The case table of rwb-case, the rule tables of rwb-decision and the adapter's own store are never named in SQL: the case arrives on the signal, the package on the event, and the restore through the integration contract.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Restore adapter fake (RWB-S2-E3009-CON) | The restore operation rwb-integration publishes | A restored answer with the prior status and a restore reference; a refusal with a reason; a timeout inside and beyond the 2 s budget |
| rwb-case case-answer fake | The case status on the case signal | `OFFER_WITH_CUSTOMER` with a prior status, a case that counters at the same moment, and a case answer with no prior status (X4) |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Rule-package fake | The RESTRUCTURE package in force | Version `RESTRUCTURE-2026.11` with R-RES-17, R-RES-18 and R-RES-20; a version with no matching row; a checksum mismatch |
| Element fake (RWB-S2-E3009-CON) | The `PriorStatusRestore` shape | A complete element for each branch; one element per missing required field |

The adapter fake is the Day-1 unblocker: the build and every test run against it, and no test calls COLLINS, EFS or the live adapter.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 2 documented rows: the rwb-case case answer and rwb-integration's restore operation | Neither name is published; faked in every test; one hop and 2 s each |
| Kafka | 0 | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic, no row written by this story; inbox dedupe by cloud event id |
| Temporal | `TreatmentWorkflow` and 3 activities on `rwb-treatment` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; no Schedule; retry policy of the kit |
| Nexus | 0 | 0 | No namespace is entered from this story |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `offer` and `workflow`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13; §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied as a prohibition here: the prior status and the offer date come from the case and the treatment, so this story reads no ACE view and no `v_ace_*` table, and the outward COLLINS write is the adapter's. DP-03 is the record write of the step, DP-13 the base this story adds no path to, and DP-19 the route through which the officer sees the outcome.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `NoSignatureBranch` | Workflow | The branch of `TreatmentWorkflow` that reacts to `CUSTOMER_DECLINED` and `OFFER_EXPIRED`, calls the adapter, reports the stage outcome and waits |
| `EvaluateRules` | Activity | Runs the RESTRUCTURE package in force and returns the rule ID, the action and the to state |
| `restorePriorStatus` | Activity | Assembles the request, calls the restore operation inside the 2 s budget, maps the answer or the failure |
| `IntegrationRestoreClient` | Client | The one hop on rwb-integration's restore operation, its request and answer of RWB-S2-E3009-CON |
| `TreatmentOutcomeRepository` | Repository | Writes the outcome, the outcome time and the restore element against the treatment row |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report for the parent and the messages of the warning and refusal paths |
| `Migrations` | Migration | No new column for the prior status until the contract freeze fixes it; `treatment` and `decision_record` are already on the sequence |

**Database.** The `treatment` row gains no column in this story: the outcome and its time use DF-TRT-013 and DF-TRT-014, and the prior status and the restore reference live in the element of RWB-S2-E3009-CON, whose field IDs are not yet allocated (GAP-2663). `decision_record` is the library object of DP-03. No ACE view and no copy of a COLLINS status table is read.

**Configuration and reference data.** The restore operation name, its request shape and the 2 s budget are configuration of the client and are the working read of ASM-4375 until the rwb-integration owner confirms them. The rule package version is data and is read from the package in force. The capability area "Treatment and offer" and the right R are the access data of P4, read through the guard library.

**Build steps**

1. The branch of `TreatmentWorkflow` on `rwb-treatment`, its input record, its signal names and its stage report (AC2, AC3).
2. `EvaluateRules` against the package fake, with R-RES-17, R-RES-18 and R-RES-20 as rule rows and the `NoPackageInForce` answer (AC2, AC3).
3. `restorePriorStatus` and the integration client against the adapter fake, with the 2 s budget and the request and answer of RWB-S2-E3009-CON (AC1).
4. `TreatmentOutcomeRepository`, the outcome write and the element (AC1, AC2, AC3).
5. `RecordAndApply` with the decision record in the same transaction, and the rollback path of MSG-P7-003 (AC4).
6. The missing-prior-status path X4, the counter-offer guard X9 and the inbox dedupe X8.
7. The timeout path: the stage stays in `OFFER_WITH_CUSTOMER`, nothing is written, MSG-GEN-006 (Section 5, X1).
8. Tests for AC1 to AC4 against the fakes, and the component tests of the refusal and missing-status paths.

**Feature flag.** `rwb.treatment.return-to-collins`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the adapter faked, the outcome and the element appear on the treatment, the record is written in the same transaction and rolls back with the action, a missing prior status stops the branch, the timeout leaves the case where it was with MSG-GEN-006, and the officer sees the outcome on SCR-14 through the gateway route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-003 | The offer is with the customer and its validity date is set | The offer to the customer ends on {date}. |
| MSG-GEN-006 | The restore operation does not answer, the package is not in force, or the case carries no prior status | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-001 | A required field of the branch is empty | Enter {field}. |
| MSG-P7-009 | A decision record is refused for a missing field | Not specified in the source documents (DOR-RWB-S2-E3009-APP-9) |

The five texts are copied unchanged from RWB-E3-009 and the platform message set. MSG-P7-009 is added for X3 with its text Not specified in the source documents (DOR-RWB-S2-E3009-APP-9). MSG-S2-001 (below the floor) and MSG-S2-002 (stale payoff) of the legacy table belong to the settlement offer and the payoff and are raised by the offer stories of this service, not here. MSG-GEN-006 names the system of the failed call. Thai text for each message follows decision DL10, on assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

SCR-14 Treatment record shows the outcome of the branch on the treatment: the outcome, the outcome time, the prior status, the return reason and the restore reference, with the treatment states Draft, submitted, approved, booked and broken as the sibling stories maintain them. The empty, loading, error and no access states of SCR-14 are Not specified in the source documents (CG-ALL-8608). SCR-15 Settlement offer shows the same facts where the treatment was a settlement and the offer lapsed, with the states Draft, below floor, approved, sent and accepted. The empty, loading, error and no access states of SCR-15 are Not specified in the source documents (CG-ALL-8609). Both are reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment and composes the answer (DP-19). The screen field lists and the composite route specification belong to the platform edge story and the screen owners; this story fixes what the service records and what the sibling story's read returns. A refusal, a timeout or a missing prior status is shown as the message on the treatment screen and raises an incident, never as a silent empty state. Screen states for SCR-14 and SCR-15: error is the refusal, timeout or missing prior status message above (timeout: MSG-GEN-006). Empty, loading and no-access states for SCR-14 and SCR-15: Not specified in the source documents (DOR-RWB-S2-E3009-APP-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-009-01 | AC1 | End to end | Return the case to its prior status on no signature |
| TC-E3-009-02 | AC2 | End to end | Rule R-RES-17 |
| TC-E3-009-03 | AC3 | End to end | Rule R-RES-18 |
| TC-E3-009-04 | AC4 | End to end | Not recorded |
| TC-E3-009-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-009-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-E3-009-07 | Contract (section 12) | Component | Operations, events and activities of section 12 match the contract |
| TC-E3-009-08 | Boundary (section 12.7) | Component | Tables of section 12.7 are written only by this service and only in the caller's transaction |
| TC-E3-009-09 | AC5 | Component | A record refused for a missing field writes nothing and carries MSG-P7-009 |
| TC-E3-009-10 | AC6 | Component | A RESTRUCTURE package not in force is refused without a retry |
| TC-E3-009-11 | AC7 | Component | An offer inside validity with no decline and no signature waits |
| TC-E3-009-12 | AC8 | Component | A repeated decline or expiry after the restore makes no second restore |
| TC-E3-009-13 | AC9 | Component | A counter-offer returns the case to the officer and this branch writes nothing |
| TC-E3-009-14 | AC10 | Component | A prior status restored from RETURNED_TO_COLLINS re-opens the route decision |
| TC-E3-009-15 | AC11 | Component | A case answer without a prior status is not guessed |
| TC-E3-009-16 | AC12 | Component | A redelivered consumed event makes no second restore |
| TC-E3-009-17 | AC13 | Component | A restore that does not answer in budget is retried and then stops |
| TC-E3-009-18 | AC14 | Component | A status change the model does not allow is refused |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The adapter, case-answer, decision-record, rule-package and element fakes of section 12.8 stand behind every case. The `-ITG` copies of these cases belong to the wave 2 integration harness (RWB-ITG-W2) and are not listed here. The contract's own tests are TC-S2-E3009-CON-01 to -05 and are owned by RWB-S2-E3009-CON.

### 17. Guardrails

- No value that a business person may change is written in code: the rule IDs, the two states, the condition texts, the reason codes, the validity period and the message texts are data rows, reference data or the package in force (BR-S2-009; BR7).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the treatment ID, codes, dates, the prior status and the rule version only, and the fixture is synthetic.
- No read of another service's tables and no case table here: the case status and the prior status arrive on the case signal and the case record is rwb-case's (DP-01; ASM-4376).
- No ACE data read: this story reads no `v_ace_*` view and no ACE table; a status or an account fact needed later comes through rwb-source-data's contract (DP-05).
- No external connection of this service: the COLLINS and EFS write is one hop on rwb-integration's contract and is faked in every test (DP-16; BR5).
- No business value in the record or the report: the `DecisionRecord` carries the rule ID, the rule version, the final call and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule, so a replay can never move a case twice (BR3).
- No restore on a case the customer has countered: the two branches are exclusive on one state, and the counter-offer rule takes the case (X9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| Not specified in the source documents (GAP-2663; ASM-4376) | A restructure or settlement that the customer declines or lets lapse returns the case to the status it held in COLLINS and re-opens the route decision | Pending (C1) | FEAT-TRT-09 | 07 Route, settle and claim | R-RES-17; R-RES-18; R-RES-20 | TC-E3-009-01 to TC-E3-009-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3009-CON | Contract | H: declares the `PriorStatusRestore` element, the two consumed rows, the failure answer and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library this story writes through, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-14 and SCR-15 show the outcome |
| RWB-S2-E3007-APP | App development | Sibling: the offer and its validity timer, whose expiry event this branch reacts to |
| RWB-S2-E3008-APP | App development | Sibling: the signed-offer route to operations, the other outcome of the same state |
| RWB-S2-E3001-APP | App development | Sibling: the treatment record and the treatment read that show the outcome |
| P3 rwb-case | Service | The case, its status, the prior status on the case answer and the parent `CaseWorkflow`; R-RES-17, R-RES-18 and R-RES-20 apply there |
| P2 rwb-integration | Service | The restore operation, the COLLINS and EFS adapters and their availability (DP-16) |
| P7 rwb-decision | Service | The RESTRUCTURE package, its version and the central ledger; EV-30 is consumed here |
| RWB-ITG-W2 | Integration | I: the cross-service proof of this legacy key against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published contract of the restore element, the two consumed rows, the failure answer and the fakes: RWB-S2-E3009-CON.
- The offer, its build and its validity timer: RWB-S2-E3007-APP; the signed-offer route to operations: RWB-S2-E3008-APP.
- The treatment record, its create operation, its read operation and its own states: RWB-S2-E3001-APP; the published read is what shows this outcome.
- The settlement expiry rule R-SET-11 and the settlement offer: the settlement slice of this service.
- The case, its status, the status column of R-RES-17, R-RES-18 and R-RES-20, the prior status value and the parent `CaseWorkflow`: rwb-case (P3), reached only on the forwarded case signal.
- The rule authoring, the four-eyes approval, the effective date, the rollback and the central ledger: rwb-decision (P7); this story consumes the package and the version.
- The restore operation, the COLLINS and EFS adapters, their availability and their retry: rwb-integration (P2) and its own contract; no story of this plan is created for it on this key (GAP-2663).
- The route decision re-opened by R-RES-20: rwb-valuation (S1) and rwb-case.
- The screens SCR-14 and SCR-15, their field lists and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The access rule, the roles and the masking: P4 rwb-access and the guard library; this story declares the capability area and the right only.
- The real cross-service proof of the adapter call, the case signal and the record write against the live owners: RWB-ITG-W2, which also owns the `-ITG` copies of the legacy cases.

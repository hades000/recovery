# RWB-S2-E2027-APP Payment matching rules with the data team

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the S2 rwb-treatment slice of legacy RWB-E2-027 is split out of the payment key. The `PAYMENT_MATCH` rows, the row order, the matching engine, the proceeds row, the exception list and the matching job stay with rwb-payment (P8) in `RWB-P8-E2027-APP` and `RWB-P8-E2027-CON`; the payment and account reads stay with rwb-source-data (P1). This story delivers only the plan consequence of a match inside rwb-treatment: the installment advanced, the partial shortfall held on the treatment row of `rwb_treatment`, the cure period of a missed installment run as a durable timer of `TreatmentWorkflow` on queue `rwb-treatment`, the plan broken when the cure period passes unpaid, a local decision record naming the rule ID and the rule version in force, the parameters and list reads of rwb-case, the read on `/api/recovery/treatment/v1` and the plan on SCR-14 through the gateway-bff composite route. The story owns no legacy acceptance criterion and keeps the thirteen legacy test case IDs on the treatment side. No source publishes the match-consequence operation of rwb-payment or the plan state names on the treatment row (GAP-2705; ASM-4487), and none names the rule set, the parameter codes or the signal that announces a plan state change (GAP-2706; ASM-4488). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-S2-J |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P8-E2027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-CHO-009) |
| Status | Draft (realignment v1) |

### 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the consequence of a payment match held on the plan of a treatment — the installment the match reports advanced, the shortfall of a partial payment held on the treatment row of `rwb_treatment`, the cure period of a missed installment run as a durable timer of `TreatmentWorkflow`, and the plan broken when the cure period passes unpaid — with every step naming the rule and the rule version that decided it**, so that **a plan that is being paid is kept alive and a plan that has stopped being paid is known the morning the match runs, instead of being found by a person reading an exception list**.

This is the secondary slice of legacy RWB-E2-027. The legacy story owns the matching rules themselves — the EXACT, WINDOW and PARTIAL rows of the `PAYMENT_MATCH` package, the row order, the tolerance, the window, the grace, the partial floor, the exception list and the matching job — and every one of its acceptance criteria is owned by `RWB-P8-E2027-APP` and by the contract `RWB-P8-E2027-CON`, not here. This story owns no legacy criterion: it tests only what a match does to the plan, and the values it uses are the ones the legacy story already carries (ASM-4485, ASM-4487).

What this story owns:

- the plan consequence of a match on `treatment` in `rwb_treatment`: `installments_paid` (DF-TRT-032) advanced by one, `installment_shortfall` (DF-TRT-033) held for the due date of the installment, `state` (TSD S2 T3.0), `outcome` (DF-TRT-013) and `outcome_at` (DF-TRT-014), and `decision_log_id` (DF-TRT-003), all under this service's own login and Flyway sequence (DP-01, DP-15);
- the cure period of a missed installment as a durable timer inside `TreatmentWorkflow`, the stage child of `CaseWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, with the activities `EvaluateRules` and `RecordAndApply` (DP-10; Architecture v5 slides 11 and 13 via the context pack);
- the match consequence read from `RWB-P8-E2027-CON` — the payment, the installment and its due date, the match type, the rule ID, the package code and version and the shortfall — one hop with a 2 s timeout against a mock (DP-11);
- the rule answer: `R-RES-27` (missed installment starts the cure period), `R-RES-28` (a late payment inside the cure period ends the wait), `R-RES-29` (break count incremented, plan broken), `R-RES-30` (return to the route decision with reason `broken_plan`) and `R-RES-31` (further restructure barred at `restructure.max_breaks = 2`), evaluated with the embedded Drools runtime from the package in force (DP-04);
- the local decision record of every step, written through the decision-record library and the shared topic `rwb.decision-record.v1`, before the treatment row changes and in the same `rwb_treatment` transaction (DP-03, DP-14);
- the parameters read (`CURE_PERIOD_DAYS`, `restructure.max_breaks`) and the reference-data read (`LOV-TRT-OUTCOME`) of rwb-case at their version (DP-06, DP-07);
- the read of the plan consequence on base `/api/recovery/treatment/v1` (DP-13) and on SCR-14 through the gateway-bff composite route (DP-19).

It does not own: the matching of payments to plans, the `PAYMENT_MATCH` rows and their versions, the tolerance, window and partial floor, the exception list, MSG-P8-001, the proceeds row and the matching job — those are `RWB-P8-E2027-APP` and `RWB-P8-E2027-CON` (P8); the rule registry, the package load and the approval that gives a version force — those are rwb-decision's (P7); the payment, account and batch-status reads — those are rwb-source-data's (P1); the case status, the case task of R-RES-30 and `CaseWorkflow` — those are rwb-case's (P3); the treatment record, the offer, the settlement range and the plan offer — those are `RWB-S2-E3001-APP` to `RWB-S2-E3011-APP`.

### 2. Business rationale

The legacy story fixed the gap plainly: the exact rule of RWB-E2-008 left short and late installments on the exception list, a person matched them by hand each morning, and a plan that had quietly stopped being paid sat in the same list. Its objective carries over unchanged — most payments match without a person, every match names its rule and its package version so it can be explained later, and the plan on the case tells the truth about where the customer stands (REQ-CHO-009; CTL-41; FSD P8 measure "receipts matched the same day").

What D-RCV-60 changes is which half of that sentence belongs to which service. A match is a payment fact: it reads the payments of the business date, applies the package rows in row order, writes the proceeds row and the exception list. A plan is a treatment fact: `installment_amount`, `installments`, `first_due_date`, `installments_paid` and `installment_shortfall` are columns of `treatment` in `rwb_treatment`, and the plan clock is named as this service's own workflow in the service catalogue (TSD S2 T3.1; context pack ownership rows).

So the value crosses one boundary and lands where the fact lives. rwb-payment decides which installment a payment matched and what is missing; rwb-treatment holds the plan, so rwb-treatment applies the consequence, starts the cure period, and breaks the plan when the cure period passes unpaid. The moment this service read a payment table or a proceeds row for itself, two services would own one match and the rule that no match exists without its record could be bypassed by a query (DP-01, DP-05; legacy guardrails).

Two consequences are designed rather than left to discipline. The rule set is data: the tolerance, the window, the grace, the partial floor, the cure period and the break limit are columns of a row or parameter values in force, read at evaluation time, so the only numbers in this module are column names and field IDs (legacy BR10; D-RCV-36 T10; DP-06). And the clock is a timer, not a scan: the legacy build discovered a plan late by polling a timer table, while the target runs the cure period as a durable timer inside the workflow, so a plan is never found late by a job and no other service's timer row is read (DP-10). Nothing moves without its record either: the record is written before the row, with the rule ID and the version in force, and an earlier step keeps the version that decided it (legacy BR6, BR8; R-UNI-38, R-UNI-39, R-UNI-41).

It serves REQ-CHO-009 on the treatment side: the plan is kept current by the match and is closed when it breaks. No business value is invented or moved.

### 3. Preconditions

- `RWB-P8-E2027-CON` is published: the match consequence of a business date for a case and its plans, carrying the payment, the installment, the due date, the match type, the rule ID, the package code and version and the shortfall, one hop with a 2 s timeout behind a breaker (DP-11). The operation name and the payload member names are not published by any source (GAP-2705; ASM-4487). This story builds against the contract and its fake on Day 1 and never against a payment, proceeds or rule table.
- The `rwb_treatment` schema and login exist from the platform database story, and the `treatment` table exists with the columns of TSD S2 T3.1 (DF-TRT-001 to DF-TRT-033) and the standard record columns of T3.0, including `state`, `version`, `outcome` (DF-TRT-013) and `outcome_at` (DF-TRT-014) with LOV-TRT-OUTCOME.
- A treatment of the restructure, settlement or deed in lieu route is booked for the case, with its plan terms `installments` (DF-TRT-009), `installment_amount` (DF-TRT-031), `first_due_date` (DF-TRT-029) and `installments_paid` (DF-TRT-032) written by `RWB-S2-E3010-APP`, in state `PLAN_RUNNING` with the plan states of TSD S2 T4 (ASM-4489).
- The workflow kit is in place on task queue `rwb-treatment` in namespace `rwb-recovery`, and `CaseWorkflow` of rwb-case starts this stage as a child on that queue and passes the payment signal to it (DP-10; ASM-4487).
- A rule package holds the RES rule set of the route at a version in force for the business date, and the embedded Drools runtime of the service template evaluates it inside an activity (DP-04; ASM-4488).
- The parameters read of rwb-case is available through its client library: `CURE_PERIOD_DAYS` and `restructure.max_breaks` are values in force with their version, and the reference-data read serves LOV-TRT-OUTCOME (DP-06, DP-07; ASM-4488). The parameter codes and the package code are not published by any source (GAP-2706; ASM-4488).
- The decision-record library is published: it writes the row in the caller's transaction and refuses with MSG-P7-003 when it cannot (DP-03; ASM-4490).
- No approval is needed to build against a Draft contract baseline, and a C dependency never blocks: this story starts on Day 1 with only `RWB-P8-E2027-CON` as its contract dependency.

### 4. Flow

1. rwb-payment matches the payments of the business date against the running plans and publishes or holds the result of each installment; the row order, the tolerance, the window and the partial floor are its own (P8; not this story).
2. rwb-case signals `CaseWorkflow`, which passes the payment signal to `TreatmentWorkflow` on queue `rwb-treatment` for the treatment of the plan (ASM-4487).
3. `TreatmentWorkflow`: the `EvaluateRules` activity reads the match consequence of the plan for that business date from `RWB-P8-E2027-CON` (DP-11) and the rule version in force for the date.
4. `EvaluateRules`: the embedded Drools runtime fires the first row of the RES rule set in force; the answer names the rule ID and the package version that decided (DP-04).
5. `RecordAndApply`: the decision record is written with the rule ID, the package version and the inputs — payment code, due date, amount, shortfall — and no personal data (DP-03).
6. `RecordAndApply`: on a matched installment, `installments_paid` is advanced by one and the shortfall held for that due date is cleared; on a PARTIAL match, the difference between `installment_amount` and the matched amount is held in `installment_shortfall` for that due date (legacy AC1, AC2 values).
7. `TreatmentWorkflow`: on a missed installment the cure timer starts for `CURE_PERIOD_DAYS` of the product; a match inside the cure period cancels the timer early; when the timer fires unpaid, the break count is incremented, the plan is marked broken and the stage reports the outcome to `CaseWorkflow` (R-RES-27 to R-RES-30).
8. RW-CREDITAD: reads the plan on SCR-14 through the gateway-bff composite route, with the state, the installments paid, the shortfall and the rule and version each step named (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A partial payment below the partial floor | rwb-payment raises no match for the installment; nothing reaches this service; the plan state and the shortfall are unchanged; the exception list and its message stay with P8 | MSG-P8-001 (P8) | AC3 |
| X2 | A late payment outside the window | No match is raised; the cure timer keeps running and fires unpaid | None | AC5 |
| X3 | No rule version in force for the business date | The step refuses with `NoPackageInForce`; no treatment row and no record is written for that date | MSG-P3-027 | AC6 |
| X4 | The decision record cannot be written | The treatment row is not changed; the step retries on the workflow policy and nothing is applied without its record | MSG-P7-003 | AC7 |
| X5 | A late payment arrives while the cure timer is firing | The answer that is committed first wins; the record names the rule that decided and the second answer finds the state already moved | None | AC4 |
| X6 | The caller holds no right on the treatment read | The read is refused; no plan consequence is returned | MSG-P4-002 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the match consequence read of RWB-P8-E2027-CON and this service's own `treatment` row only |
| Negotiable | The cure period and the break limit are parameter values; the story fixes the order of the record and the row and the state names |
| Valuable | A plan that is paid stays alive and a plan that has stopped being paid is known the morning the match runs |
| Estimable | One read, one rule evaluation, one record and one row write per step, plus one durable timer |
| Small | One activity pair and its tests; it fits in a wave-2 sprint |
| Testable | Each criterion runs against the contract fakes and a rule version loaded for the business date |

### 7. Acceptance criteria

```gherkin
Feature: Payment matching rules with the data team

  Background:
    Given the rwb-payment contract mock returns the match result for business date 2026-12-15
    Given case "RC-2026-000555" has running plan "T-0701" with installment amount 12,500.00 THB, next installment date 2026-12-15 and installments_paid "3"
    Given rule package version "PM-2026.12" is in force from 2026-12-01, naming the rows "EXACT", "WINDOW" and "PARTIAL"

  Scenario: AC1 A missed installment starts the cure period as a durable timer (new, D-RCV-60)
    Given the rwb-payment contract mock returns a missed installment for plan "T-0701" and due date 2026-12-15
    When TreatmentWorkflow applies the result
    Then the plan state is PLAN_CURE_PERIOD and a durable timer of 30 calendar days (CURE_PERIOD_DAYS for MORTGAGE) is running in the workflow
    Then the decision record of the step names rule "R-RES-27" and the rule version in force
    Then installments_paid and installment_shortfall are unchanged

  Scenario: AC2 A matched installment advances the plan (new, D-RCV-60)
    Given the rwb-payment contract mock returns payment "PAY-91001" of 12,500.00 THB matched to "INSTALLMENT" for plan "T-0701", due date 2026-12-15, rule "EXACT" and version "PM-2026.12"
    When TreatmentWorkflow applies the result
    Then installments_paid is "4" and no shortfall is held for due date 2026-12-15
    Then the decision record names rule "EXACT" and rule version "PM-2026.12"
    Then the plan state stays PLAN_RUNNING

  Scenario: AC3 A partial payment holds the shortfall on the plan (new, D-RCV-60)
    Given the rwb-payment contract mock returns payment "PAY-91002" of 11,875.00 THB matched to "INSTALLMENT" for plan "T-0701", due date 2026-12-15, rule "PARTIAL" and version "PM-2026.12"
    When TreatmentWorkflow applies the result
    Then installment_shortfall is 625.00 for due date 2026-12-15 and installments_paid is "4"
    Then the decision record names rule "PARTIAL" and rule version "PM-2026.12"
    Then a payment below the partial floor writes no shortfall and leaves the plan unchanged

  Scenario: AC4 A late payment inside the cure period ends the wait early (new, D-RCV-60)
    Given plan "T-0701" is in state PLAN_CURE_PERIOD with the cure timer running
    Given the rwb-payment contract mock returns payment "PAY-91004" of 12,500.00 THB matched 3 days after due date 2026-12-15, rule "WINDOW"
    When TreatmentWorkflow applies the result
    Then the cure timer is cancelled and the plan returns to PLAN_RUNNING under rule "R-RES-28"
    Then installments_paid is advanced by one and the decision record names rule "R-RES-28" and the version in force
    Then the first committed answer stands and the second finds the state already moved

  Scenario: AC5 A cure period that passes unpaid breaks the plan (new, D-RCV-60)
    Given plan "T-0701" is in state PLAN_CURE_PERIOD and the 30-day cure timer fires with no matched payment
    When the timer fires
    Then the break count is incremented and the plan is marked PLAN_BROKEN under rule "R-RES-29"
    Then the stage reports the case back to the route decision with reason "broken_plan" under rule "R-RES-30"
    Then where the break count reaches restructure.max_breaks = 2 a further restructure is barred under rule "R-RES-31"
    Then no case status is written by this service

  Scenario: AC6 No rule version in force is a refusal (new, D-RCV-60)
    Given the rule package read returns no RES rule version in force for 2027-02-01
    When TreatmentWorkflow evaluates the plan step for that date
    Then the evaluation throws NoPackageInForce and MSG-P3-027 is shown for the package in force check
    Then no treatment row and no decision record is written for 2027-02-01

  Scenario: AC7 Nothing moves without its record (new, D-RCV-60)
    Given the decision-record library is unavailable during the step
    When TreatmentWorkflow applies a matched installment
    Then the treatment row is unchanged and MSG-P7-003 is shown
    Then the step is retried and no state, shortfall or installments paid is written without its record

  Scenario: AC8 The plan consequence is read under the caller's right (new, D-RCV-60)
    Given the rwb-access contract mock returns no "Treatment and offer R" right for the caller
    When the caller reads GET /api/recovery/treatment/v1/treatments/{treatmentId}
    Then the response is status 403 with MSG-P4-002
    Then no plan consequence is returned and nothing changes
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The match consequence is read from rwb-payment and never re-computed here: the match type, the rule ID, the package version and the shortfall are the payer's answer | Legacy story scope; DP-11 |
| BR2 | A matched installment advances `installments_paid` by one and clears the shortfall held for that due date | Legacy AC1, AC2 (recordInstallmentPaid); DF-TRT-032 |
| BR3 | A PARTIAL match holds the difference between the installment amount and the matched amount as `installment_shortfall` for that due date | Legacy BR4, AC2; DF-TRT-033 |
| BR4 | A missed installment starts the cure period; a match inside it ends the wait and returns the plan to running | R-RES-27, R-RES-28 |
| BR5 | The cure period and the break limit are parameter values in force, read at evaluation time, never code | D-RCV-36 T10; legacy BR10; DP-06 |
| BR6 | When the cure period passes unpaid the break count increments and the plan is broken; below the limit the case returns to the route decision; at `restructure.max_breaks = 2` a further restructure is barred | R-RES-29, R-RES-30, R-RES-31 |
| BR7 | Every step writes a decision record with the rule ID and the version in force; an earlier step keeps the version that decided it | Legacy BR6; R-UNI-38 |
| BR8 | A step whose record cannot be written is not applied | Legacy BR8; R-UNI-39 |
| BR9 | No version in force is a refusal, never a default | Legacy BR9; R-UNI-41 |

### 9. State transitions

None of the case status. This story moves the plan state on its own `treatment` row (ASM-4489):

| From | Event | Condition | To |
|---|---|---|---|
| PLAN_RUNNING | missed installment applied | no match for the installment of the due date | PLAN_CURE_PERIOD (R-RES-27) |
| PLAN_CURE_PERIOD | match inside the cure period | matched amount at or above the floor of the row that fires | PLAN_RUNNING (R-RES-28) |
| PLAN_CURE_PERIOD | cure timer fires | no matched payment in the cure period | PLAN_BROKEN (R-RES-29) |
| PLAN_BROKEN | stage report | break count below `restructure.max_breaks` | case returns to the route decision (R-RES-30), by rwb-case |

The case status itself is moved by `CaseWorkflow` of rwb-case on the stage report; this service writes no case row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration officer | Reads the plan consequence on the treatment screen; owns the cure and break values through the parameters, not in code |
| RW-RESTRUCT, restructuring officer | Reads the plan after a break; the case task of R-RES-30 is rwb-case's |
| RW-COE, center of excellence analyst | Authors the RES rule rows that decide the step, with rwb-decision (P7) |
| RW-RISK | Approves the rule version; the author cannot |
| RW-FINANCE, Finance and CFO delegate | Reads the plan consequence |
| The recovery service identity | Runs `TreatmentWorkflow` and its activities |
| SY-RULES, Drools evaluator | Evaluates the row in force and names the rule and the version |
| SY-DECLOG, decision record writer | Writes the record of the step |
| SY-CASEWF, case workflow | Starts the stage and reads its outcome |

Separating duty: the analyst who authors a rule row does not approve it; the approval is rwb-decision's.

### 11. Data

| Entity and field | Field ID | Read or write | Where it comes from |
|---|---|---|---|
| treatment.id | DF-TRT-001 | Read | Own schema `rwb_treatment` |
| treatment.case_id | DF-TRT-002 | Read | Own schema |
| treatment.decision_log_id | DF-TRT-003 | Write | Own schema |
| treatment.installments | DF-TRT-009 | Read | Own schema |
| treatment.outcome | DF-TRT-013 | Write | Own schema, LOV-TRT-OUTCOME |
| treatment.outcome_at | DF-TRT-014 | Write | Own schema |
| treatment.first_due_date | DF-TRT-029 | Read | Own schema |
| treatment.installment_amount | DF-TRT-031 | Read | Own schema |
| treatment.installments_paid | DF-TRT-032 | Write | Own schema |
| treatment.installment_shortfall | DF-TRT-033 | Write | Own schema |
| treatment.state, version | TSD S2 T3.0 | Write | Own schema |
| decision record, all fields | DF-DEC-001 to DF-DEC-018 | Write | Through the decision-record library |
| the match consequence: payment code, due date, match type, rule ID, package code and version, shortfall | Not specified in the source documents (GAP-2705; ASM-4487) | Read | `RWB-P8-E2027-CON`, no field IDs published |
| CURE_PERIOD_DAYS, restructure.max_breaks | Not specified in the source documents (GAP-2706; ASM-4488) | Read | Parameters read of rwb-case |
| LOV-TRT-OUTCOME members | TSD S2 T3.2 | Read | Reference-data read of rwb-case |

The legacy reads of `recovery.v_ace_payment` and `recovery.v_ace_account` are not repeated here. Under DP-05 the payment is read through its owner's contract and the plan facts live in this service's own schema, so this story opens no other schema and no `v_ace_*` view.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | Read the plan consequence: state, installments paid, shortfall, outcome and the decision record of the last step | None | Treatment, with `installment_amount`, `installments_paid`, `installment_shortfall`, `state`, `outcome`, `outcome_at`, `decision_log_id` | 401, 403 (MSG-P4-002), 404, 503 |

The shape of the operation is declared by `RWB-S2-E3001-CON`; this story serves the plan-consequence elements under the rights of TSD S2 T-A.2 (Treatment and offer, right R, scope applied).

#### 12.2 REST operations consumed

| Contract | Owner | Operation | Purpose | Call type |
|---|---|---|---|---|
| RWB-P8-E2027-CON | rwb-payment | Not specified in the source documents (GAP-2705; ASM-4487) | The match consequence of a business date for a case and its plans | REST, one hop, 2 s timeout |
| RWB-P3-E1042-CON | rwb-case | Not specified in the source documents (GAP-2706; ASM-4488) | `CURE_PERIOD_DAYS` and `restructure.max_breaks` at their version | REST, 2 s timeout |
| RWB-P3-E1043-CON | rwb-case | Not specified in the source documents (GAP-2706; ASM-4488) | LOV-TRT-OUTCOME at its version | REST, 2 s timeout |
| RWB-P7-E1073-CON | rwb-decision | Not specified in the source documents (GAP-2706; ASM-4488) | The RES rule package version in force for the business date | REST, 2 s timeout |

#### 12.3 Events published

None. This story writes the `treatment` row and the decision record and raises no event of its own. The service's owned event EV-10 is `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` (TSD S2 T5.3) and is raised by the offer and booking stories, not here.

#### 12.4 Events consumed

None. The match reaches this service through the stage signal of `CaseWorkflow` and the match-consequence read of `RWB-P8-E2027-CON`, so this story subscribes to no topic and needs no consumer group (ASM-4487). Both inputs are supplied by contract fakes.

#### 12.5 Workflows and activities

| Name | Queue | Role | Retry and timeout |
|---|---|---|---|
| `TreatmentWorkflow` | `rwb-treatment` | Stage child of `CaseWorkflow`; holds the plan clock and the cure timer | One execution per treatment, durable across restarts |
| `EvaluateRules` activity | `rwb-treatment` | Reads the match consequence and evaluates the RES row in force | Default policy; the read fails at 2 s and is retried |
| `RecordAndApply` activity | `rwb-treatment` | Writes the decision record, then the treatment row, in one transaction | Default policy; a record failure fails the activity |
| cure timer | `rwb-treatment` | Durable timer of `CURE_PERIOD_DAYS` for the product; cancelled by a match inside it | Cancelled on the match; fires the break step |

#### 12.6 Schedules

None. DP-10 replaces the polled timer check with a durable workflow timer, and the context pack gives S2 no job (Jobs 0). No Temporal Schedule and no batch window is created by this story.

#### 12.7 Tables owned

| Schema | Table | Columns used | Access |
|---|---|---|---|
| `rwb_treatment` | `treatment` | DF-TRT-001, 002, 003, 009, 013, 014, 029, 031, 032, 033, `state`, `version`, `updated_at`, `updated_by` | Read and write under the `rwb_treatment` login only; no other schema is opened |

#### 12.8 Contract fakes

| Fake | Contract | Covers | Used by |
|---|---|---|---|
| match-consequence fake | RWB-P8-E2027-CON | matched, partial and missed installments with the rule ID and the version; a timeout | AC2 to AC5 |
| parameters fake | RWB-P3-E1042-CON | `CURE_PERIOD_DAYS`, `restructure.max_breaks`, a missing value | AC1, AC5 |
| reference-data fake | RWB-P3-E1043-CON | LOV-TRT-OUTCOME | AC4, AC5 |
| rules fake | RWB-P7-E1073-CON | a version in force, and `NoPackageInForce` | AC6 |
| platform fakes named by the DP table | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1071-CON, RWB-PLT-E1072-CON, RWB-PLT-N001-CON | decision record, parameters and reference clients, topic naming, workflow kit, Drools kit, edge route | build (ASM-4486) |

#### 12.9 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | 1 | 4 |
| Kafka | 0 published | 0 consumed |
| Temporal | 1 workflow, 2 activities, 1 timer | stage signal from `CaseWorkflow` (rwb-case) |
| File | 0 | 0 |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `treatment/plan-consequence`.

| Component | Type | Responsibility |
|---|---|---|
| `MatchConsequenceReader` | Service | Reads the match consequence of the plan for the business date through `RWB-P8-E2027-CON`, one hop with a 2 s timeout |
| `PlanConsequenceRules` | Service | Evaluates the RES row in force with the embedded Drools runtime and returns the rule ID and the version |
| `PlanConsequenceApplier` | Service | Applies the answer to `installments_paid`, `installment_shortfall`, `state`, `outcome` and `outcome_at` |
| `PlanDecisionRecorder` | Service | Builds the record with the rule ID, the version and the inputs, and writes it before the row |
| `CureTimerActivities` | Activity | Starts, cancels and fires the cure timer of `TreatmentWorkflow` |
| `TreatmentPlanResource` | REST | Serves the plan-consequence elements of the treatment read |

**Patterns applied.**

| DP | How it lands here | Dependency |
|---|---|---|
| DP01 | Only `rwb_treatment` is opened; no other service's table is read | none |
| DP03 | Local decision record plus `rwb.decision-record.v1`, written in the same transaction | H RWB-PLT-E1027-CON |
| DP04 | Embedded Drools kit; the RES package comes from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP05 | No `v_ace_*` read; the payment comes through rwb-payment's contract | none |
| DP06 | `CURE_PERIOD_DAYS` and `restructure.max_breaks` from the parameters contract | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP07 | LOV-TRT-OUTCOME from the reference-data contract | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP10 | The cure wait is a durable workflow timer, not a Quartz job or a polled row | H RWB-PLT-E1071-CON |
| DP11 | The match consequence is a REST contract with a mock, one hop, 2 s | C RWB-P8-E2027-CON |
| DP13 | The read is served on `/api/recovery/treatment/v1` | none |
| DP14 | `rwb.treatment.events.v1` and `rwb.decision-record.v1` names come from the naming library | H RWB-PLT-E1047-CON |
| DP15 | Columns and rows live on this service's own Flyway sequence in `rwb_treatment` | H RWB-PLT-E1044-CON |
| DP19 | SCR-14 is reached through the gateway-bff composite route | H RWB-PLT-N001-CON |

**Database.** No new table and no new column: `installments_paid`, `installment_shortfall`, `state`, `outcome` and `outcome_at` come with the `treatment` table from `RWB-S2-E3001-APP`, and the rule ID and the version live in the decision record linked by `decision_log_id` (ASM-4490). DP-15 is applied by keeping every write on this service's own sequence and login.

**Configuration.** `CURE_PERIOD_DAYS` and `restructure.max_breaks` are parameter values in force, loaded and approved through rwb-decision and rwb-case; the design example reads 30 calendar days for MORTGAGE and `restructure.max_breaks = 2` (ASM-4488). The package code of the RES rule set is not published by any source (GAP-2706).

**Build steps.**

1. Read the match consequence through the contract fake and map it to the plan facts; test AC2 and AC3.
2. Evaluate the RES row in force and return the rule ID and the version; test AC1 and AC6.
3. Write the record before the row in one transaction and fail closed; test AC7.
4. Start and cancel the cure timer; test AC1 and AC4.
5. Fire the cure timer, increment the break count, break the plan and report the stage outcome; test AC5.
6. Serve the plan consequence on the treatment read under the caller's right; test AC8.

**Feature flag.** `rwb.treatment.plan-consequence`, this story's own. Off: no match consequence is applied and the plan is read as written by the earlier stories. The payment-side flag `rwb.payments.matching-rules` stays with P8.

**Done when.** The tests of section 16 pass, and a synthetic month of plans shows every applied step with a decision record naming a rule ID and a version in force.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | No rule version is in force for the business date | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller holds no right on the read | You cannot {action} here. Your role does not include it. |
| MSG-P8-001 | Raised by rwb-payment, not here: unmatched payments of the run | {count} payments for {date} matched no plan and are on the exception list. |

For MSG-P3-027 the {check} value is package in force, and {detail} names the package code only, never a payment or a person. Thai text follows DL10 (legacy section 14).

### 15. Screens and states

SCR-14 shows the treatment with its plan consequence: the state, the installments paid, the shortfall of the current due date, and the rule ID and version of the last step from its decision record (states Loading; plan running; cure period; broken). The matched and unmatched receipt list stays SCR-28 with rwb-payment and is not re-cut here. The route is reached through the gateway-bff composite route (DP-19); the rule version in force shows on the rules screen with rwb-decision.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-027-01 | AC2 | Component | `PAY-91001` 12,500.00; version `PM-2026.12` |
| TC-E2-027-02 | AC3 | Component | `PAY-91002` 11,875.00; shortfall 625.00 |
| TC-E2-027-03 | AC2, AC3 | Contract | `PM-2027.01` from 2027-01-01; `PAY-91003` 4 days late |
| TC-E2-027-04 | AC4, AC5 | Component | `PAY-91004` 3 days late, `PAY-91005` 4 days late |
| TC-E2-027-05 | AC3, AC5 | Component | `PAY-91006` 10,000.00, below the floor |
| TC-E2-027-06 | AC6 | Contract | A version refused at the schema check stays out of force |
| TC-E2-027-07 | AC7 | Component | Decision-record library stubbed unavailable |
| TC-E2-027-08 | AC3 | Component | `PAY-91007` 13,000.00, above the tolerance |
| TC-E2-027-09 | AC2 | Component | `PAY-91008` matched by two rows; the lower row order decides |
| TC-E2-027-10 | AC6 | Contract | No version in force on 2027-02-01 |
| TC-E2-027-11 | AC8 | Contract | RW-CASEOWN reads the treatment; refused with MSG-P4-002 |
| TC-E2-027-12 | AC8 | Contract | RW-CASEOWN attempts the rule-package load; the endpoint stays with rwb-decision and rwb-payment, refused with MSG-P4-002 |
| TC-E2-027-13 | AC7 | NFR | Record write forced to fail for 50 steps; no treatment row changed |
| TC-S2-E2027-APP-01 | AC1 | Component | Missed installment; `CURE_PERIOD_DAYS` 30 for MORTGAGE |
| TC-S2-E2027-APP-02 | AC4 | Component | Match on the last day of the cure period; timer cancelled |
| TC-S2-E2027-APP-03 | AC5 | Component | Timer fires unpaid; break count 1, then 2 at the limit |
| TC-S2-E2027-APP-04 | AC8 | Contract | Read of the plan consequence with and without the right |

The full legacy tests, with their Given, When and Then, are in Recovery Workbench Test Cases under the same legacy test case ID; the four `TC-S2-E2027-APP` cases are written with this story.

### 17. Guardrails

- No business value in code: the cure period, the break limit and every column of the rule rows are data in force, read at evaluation time.
- No personal data in events, records, workflow inputs or logs: the record holds the payment code, the due date, the amount, the shortfall, the rule ID and the version only.
- ACE data only through its owner's contract: this story opens no `recovery.v_ace_*` view and no other service's table (DP-01, DP-05).
- The decision record is written before the treatment row, and no plan change exists without it.
- One evaluator: the step calls the rule engine and reads no rule table, workbook or `drl_source`.
- The plan clock is a workflow timer: no Quartz job, no polled timer row and no scheduled scan (DP-10).
- The treatment read is served under the caller's right and scope; a refusal changes nothing.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-009 | Payments matched to the plan and their consequence held on the plan; unmatched items listed by the payer | Business Requirements Epic 2, sections 3.8 and 4 | FEAT-OCC-10, FEAT-PAY-01 | 7.3 Negotiate settlement or deed in lieu | R-RES-27, R-RES-28, R-RES-29, R-RES-30, R-RES-31, R-UNI-38, R-UNI-39, R-UNI-41 | TC-E2-027-01 to TC-E2-027-13, TC-S2-E2027-APP-01 to TC-S2-E2027-APP-04 |

Legacy RWB-E2-027 keeps its full traceability with `RWB-P8-E2027-APP` and `RWB-P8-E2027-CON`, which own the matching rules and the exception list.

### 19. Out of scope

- The `PAYMENT_MATCH` rows, the row order, the tolerance, the window, the grace and the partial floor (P8, `RWB-P8-E2027-APP`).
- The matching run, the proceeds row, the exception list, MSG-P8-001 and the matching job (P8).
- The load, the checks, the approval and the rollback of a rule package version (P7, with `RWB-P7-E1073-CON`).
- The payment, account and batch-status reads and the ACE views (P1).
- The case status, the case task of R-RES-30 and the case timers (P3).
- The treatment record, the offer, the settlement range and the plan offer (S2, E3 stories).
- The manual matching of a receipt and the reconciliation agent that works the exception list (later epics, as in legacy section 19).

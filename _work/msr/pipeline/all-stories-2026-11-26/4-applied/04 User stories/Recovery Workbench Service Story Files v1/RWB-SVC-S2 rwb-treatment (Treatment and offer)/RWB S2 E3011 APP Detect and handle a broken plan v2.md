# RWB-S2-E3011-APP Detect and handle a broken plan

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-011 split out for rwb-treatment. The break step leaves the monolith's method of `TdrSettlementAndDeedInLieuService` and becomes the break branch of `TreatmentWorkflow` on this service's own task queue; the missed-payment evidence is read at the ACE batch date from this service's own SELECT-only `recovery.v_ace_payment` view and is never copied (DP-05); the break count and the break limit are composed per calculation and the mark is written on the treatment with its local decision record in the same transaction (DP-03); the case is returned to the route decision by the stage report to the parent `CaseWorkflow`, never by writing a case row; the four legacy criteria this story owns are copied word for word with their origin tag; the broken state is read on SCR-14 through the gateway-bff composite route (DP-19); this story declares no REST path of its own, so the legacy base `/api/recovery/v1` is not carried (DP-13). No source gives the break count a field or the break limit a governed row (GAP-2668; ASM-4383), publishes the event a broken plan is said to raise (GAP-2669; ASM-4384), says where the plan status is held after the split (GAP-2670; ASM-4385) or names the payment window and the cure-period set (GAP-2671; ASM-4386). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3011-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-V |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3011-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the break step of a treatment to run as the break branch of `TreatmentWorkflow` — the missed payments counted against the break rule from the payment view at the ACE batch date, the plan marked broken on the treatment with the rule version that decided, and the case returned to the route decision with reason broken_plan where the break count is below the limit** — so that **a restructure that fails does not sit in a plan state and is worked again in days instead of being tracked by hand for 23 to 26 days**.

This is the application slice of legacy RWB-E3-011. It owns:

- the four legacy acceptance criteria this story is given (AC1 to AC4), copied verbatim with their origin tag, and the rules, data rows and messages they carry;
- the break branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`: the step that evaluates the rule set in force at the cure-period expiry of the plan, records the answer and reports the stage outcome to the parent `CaseWorkflow` (Temporal and Drools Design slides 5 and 11);
- the detection activity: the installments due of the plan and the payments of its accounts read at the ACE batch date from this service's own SELECT-only views `recovery.v_ace_payment` and `recovery.v_ace_batch_status`, compared over the cure window of the plan (DP-05; R-RES-29 condition "no payment and cure_period passed");
- the break count and the break limit: composed per calculation from the case's own treatment rows and the rule row in force, never held as a column and never written as a constant (GAP-2668; ASM-4383);
- the three answers of the rule set: R-RES-29 (increment the break count and mark the plan broken, to `PLAN_BROKEN`), R-RES-30 (return the case to the route decision with reason `broken_plan`, to `BACK_TO_ROUTE_DECISION`) and R-RES-31 (bar a further restructure, to `RESTRUCTURE_BARRED`), plus the R-RES-36 hold when the break count is missing or not a number;
- the `PlanBreak` element of RWB-S2-E3011-CON written against the treatment row in `rwb_treatment` — `outcome` and `outcome_at` among the TSD S2 T3.1 fields — and the local decision record of the step written through `DecisionRecordWriter.record(DecisionRecord)` in the caller's transaction (DP-03; RWB-PLT-E1027-CON);
- the return to the route decision and the 5 working day case owner task of R-RES-30 ordered by the stage report to the parent, because the case status, the case tasks and the case timers are rwb-case's;
- the refusal and failure paths: no record, nothing changes and MSG-P7-003; a stale data product blocks with MSG-P1-001; a missing value is named with MSG-GEN-001.

It does not own: the published element, the read rule of the payment view, the break-count rule, the versioning rule and the fakes, which are RWB-S2-E3011-CON; the cure period opened by R-RES-27 and cleared by R-RES-28 and the plan timers set by R-RES-25, which are RWB-S2-E3010-APP and the payment-missed branch of this service; the treatment record, its create and read operations and its states, which are RWB-S2-E3001-APP; the offer, its validity and its return to the prior status, which are RWB-S2-E3007-APP and RWB-S2-E3009-APP; the route decision, its scoring and its approval, which are S1 rwb-valuation's; the case, its status, its tasks and its timers, which are rwb-case's and arrive on the case signal the parent forwards; the payment matching that finds a missed installment, which is rwb-payment's under EV-12; the ACE views and their content, which are ACE's; the rule package, its approval and the central ledger, which are P7 rwb-decision's; the screen and its composite route, which are the platform edge story's and the screen owner's under DP-19.

### 2. Business rationale

In the monolith the break step was a method of `TdrSettlementAndDeedInLieuService`: it read the payments from the `recovery` schema, read the break threshold from `rule_row`, wrote the outcome into `treatment` and the decision into `decision_log_entry`, all inside one process and one schema (TSD S2 T2 and T3.1). Two things followed. The threshold could only change by a code release, and the count of breaks a case had carried was recomputed by whoever read the module's tables, so two readers could disagree about whether a third restructure was allowed.

D-RCV-60 changes the source of each input and nothing else. The payment stays in ACE and is read at the ACE batch date through this service's own SELECT-only view, with the data product's date on the answer (DP-05; D-RCV-35, ADR-010). The break limit is a governed value of the rule row in force, read with the version that decided, so a change of policy is a rule release and not a build (R-RES-30 and R-RES-31 conditions; the run's default rulings). The decision is recorded locally in the same transaction as the mark, so a break that cannot be recorded does not happen (DP-03; ADR-022).

The step is a branch of the stage workflow the service already owns: one child workflow per case on the owner's queue, `rwb-treatment`, with the rules evaluated from the package in force (Temporal and Drools Design slide 11; Architecture v5 slide 18). The rules that name the behaviour are the RESTRUCTURE rows R-RES-29, R-RES-30, R-RES-31 and R-RES-36, whose states, events, condition terms — `cure_period`, `break_count`, `max_breaks`, `broken_plan` — and timer are carried into the split unchanged (Business Rules and Routing Logic v4).

What it does not change is the officer's work or the case. The count is still a count of breaks, the limit is still the limit, and the case still returns to the route decision with the reason the rule names. Nothing about a case status is this service's: the stage reports and the parent applies the rule (BR8).

Delivery is EP03 in wave 2 on release 31 January 2027 (tentative). REQ-S2-009 of FSD S2 names this feature — "a broken plan raises an event and returns the case to a decision rather than leaving it in a plan state" — and is the requirement this story and its contract trace to; TSD S2 T8 maps the same ID to FEAT-TRT-01, so the trace carries both (Section 18).

### 3. Preconditions

- RWB-S2-E3011-CON is published: the `PlanBreak` element, its required and optional fields, the read rule of the payment view, the break-count rule, the messages and the fakes. The build starts against the Draft baseline, as every CON story of this run publishes on Day 1 at status Draft (realignment v1).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` propagation, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 from the case read and this service's read (DP-19).
- The `rwb_treatment` schema and its login exist from the platform database story, the `treatment` table is on the per-service Flyway sequence with DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, and `decision_record` is created as the platform library object in the same schema (DP-01; DP-15).
- SELECT on `recovery.v_ace_payment` and `recovery.v_ace_batch_status` is granted to this service's login and on no other ACE object. Architecture v5 slide 8 says the 30 `recovery.v_ace_*` views are read only by rwb-source-data while DP-05 allows the service's own SELECT-only views; the grant is the working read of ASM-4362, which this story reuses rather than re-raises, and the Work Package records no contract dependency on P1 (GAP-2654).
- The treatment carries a booked plan with its schedule, `installment_amount`, `installments`, `installments_paid`, `first_due_date` and `outcome` (DF-TRT-031, DF-TRT-009, DF-TRT-032, DF-TRT-029, DF-TRT-013), and the case is in `PLAN_CURE_PERIOD` on the case signal with the products of the case.
- The rule package and route set in force are in this service's rule cache at the version the answer names; their identifiers, conditions and the `max_breaks` limit are rule rows, not code (EV-30; BR-S2-011).
- No approval stop: the FSD S2 and TSD S2 documents carry status "In review" and nothing in this story needs a human sign-off to start on Day 1 (ASM-4387).

### 4. Flow

1. rwb-case: the parent `CaseWorkflow` forwards the case signal to the `TreatmentWorkflow` child of the case when the plan's cure period expires, carrying the case status `PLAN_CURE_PERIOD`, the break count the case holds and the plan reference (R-RES-29 from state; EV-29).
2. `TreatmentWorkflow`: the break branch opens the step, calls `EvaluateRules` and the rule set in force returns the `RESTRUCTURE` row that applies to `CURE_PERIOD_EXPIRED`, with the rule ID and the package version (R-RES-29; R-RES-36 where the count is missing).
3. `detectBrokenPlan` activity, step one: reads `recovery.v_ace_batch_status` and compares the data product date with today's business date; a product older than today's ACE batch stops the step with MSG-P1-001 naming the product and its date (VR-S2-011-1).
4. Step two: reads the installments due of the plan and the payments of its accounts from `recovery.v_ace_payment` at the batch date — `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and the rest of DF-ACE-043 to DF-ACE-054 — read only, one hop, inside the 2 s budget, keeping no copy (DP-05).
5. Step three: compares the payments with the cure window of the plan and decides "no payment and cure_period passed" as R-RES-29 states it; a payment inside the window is R-RES-28's outcome and belongs to the payment-missed branch, so the step reports "payment found" and moves nothing (GAP-2671; ASM-4386).
6. Step four: composes the break count and tests it against the limit: `break_count < max_breaks` answers R-RES-30, `break_count >= max_breaks` answers R-RES-31, and a count that is missing or not a number answers R-RES-36 (GAP-2668; ASM-4383).
7. `RecordAndApply` activity, one transaction: the `PlanBreak` element is written against the treatment row, `outcome` takes `BROKEN` and `outcome_at` the business date (LOV-TRT-OUTCOME), the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with the rule ID, the rule version and the break count and limit applied, and the stage report goes to the parent (DP-03).
8. The stage reports `BREAK_RECORDED` with the reason `broken_plan` and the 5 working day owner task of R-RES-30; the parent applies the case status — `PLAN_BROKEN`, then `BACK_TO_ROUTE_DECISION` or `RESTRUCTURE_BARRED` — and raises the case task and its timer (R-RES-30; R-RES-31; GAP-2670; ASM-4385).
9. The officer reads the broken state, the break count and the reason on SCR-14 through the gateway-bff composite route and through the treatment read of RWB-S2-E3001-APP, and the case owner works the returned case (DP-19).
10. The route decision runs again on the returned case: R1 is excluded when R-RES-32 applies and the case is worked on another route, which is S1's and rwb-case's work and not this step's.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A data product the step reads is older than today's ACE batch | The step blocks, names the product and its date, and decides nothing | MSG-P1-001 | AC1; VR-S2-011-1 |
| X2 | A payment of the plan is found inside the cure window | The step reports "payment found", writes nothing and leaves the clear to R-RES-28 | None | Section 4 |
| X3 | The break count is missing or not a number | The step holds the case in `UNMATCHED_EXCEPTION`, names the field and raises a case owner task; no element is written | MSG-GEN-001 | R-RES-36; AC1 |
| X4 | The decision record cannot be written | The transaction rolls back: no element, no outcome, no stage report; the caller sees MSG-P7-003 and an incident is raised | MSG-P7-003 | AC4 |
| X5 | The record is refused for a missing or invalid field | Nothing is written, the field is named, the stage stays where it was | MSG-P7-009 | Section 12.8 |
| X6 | A role without the right tries to re-run the step or read its result | 403 from the access guard and nothing changes; the step itself runs unattended under the service identity | MSG-P4-002 | Section 10 |
| X7 | A second case signal arrives while the branch is running | The inbox dedupes by the cloud event id of the case signal and the activity is idempotent on the treatment, the rule version and the break count, so no second mark is written | None | Section 12.5 |
| X8 | The payment view is not reachable | The activity is retried by the workflow's retry policy; when the attempts are exhausted the stage stays where it was and the caller sees MSG-GEN-006 naming the product | MSG-GEN-006 | AC1 |

X1, X3 and X4 are the legacy paths of RWB-E3-011 carried onto the split, with X6 and the missing-value path the legacy validation table already names. X2 is R-RES-28's answer, X5 the platform library's refusal, X7 the inbox dedupe and X8 the availability path of the ACE read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3011-CON and its fakes, the decision-record library and the gateway route; the payment view is replaced by a fixture and the rule package by a fake, so no deployment of P1, P7, ACE or rwb-case is needed |
| Negotiable | The activity name, the shape of the stage report and the retry numbers are this story's choice; the element, the rules, the condition terms and the messages are fixed |
| Valuable | A failed restructure leaves the plan state the same day, with the reason, the count and the version of the policy that decided, and the case is worked again |
| Estimable | One workflow branch, one detection activity, two view reads, one mark, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic case, a payment view fixture and a rule-package fake, plus one component test of the stale-input, the missing-count and the refusal paths |

### 7. Acceptance criteria

```gherkin
Feature: Detect and handle a broken plan

  Background:
    Given treatment "TRT-SYN-0701" of case "RW-2026-000711" is a RESTRUCTURE plan in state PLAN_CURE_PERIOD
    Given the rule package in force is version "RESTRUCTURE-2026.11"

  Scenario: AC1 Detect and handle a broken plan (legacy RWB-E3-011 AC1)
    Given the rwb-case contract mock returns the case signal in state PLAN_CURE_PERIOD with break_count "1" and max_breaks "2"
    Given the ACE payment view returns no payment of the plan inside the cure period
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then counts missed payments against the break rule and moves the case to the point the rule names
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-29 (legacy RWB-E3-011 AC2)
    Given the rwb-case contract mock returns the case in state PLAN_CURE_PERIOD with break_count "1"
    Given a case in state PLAN_CURE_PERIOD
    When cure period expired
    Then increment the break count and mark the plan broken
    Then the case moves to PLAN_BROKEN

  Scenario: AC3 Rule R-RES-30 (legacy RWB-E3-011 AC3)
    Given the rwb-case contract mock returns the case in state PLAN_BROKEN with break_count "1" and max_breaks "2"
    Given a case in state PLAN_BROKEN
    When break recorded
    Then return the case to the route decision with reason broken_plan
    Then the case moves to BACK_TO_ROUTE_DECISION

  Scenario: AC4 Not recorded (legacy RWB-E3-011 AC4)
    Given the decision-record library mock returns the failure MSG-P7-003
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line above keeps its wording; what changes is where it runs, which service holds each fact and how it is reached. "Counts missed payments against the break rule and moves the case to the point the rule names" is no longer a method of `TdrSettlementAndDeedInLieuService` reading the `recovery` schema and `rule_row`: the count is composed by the `detectBrokenPlan` activity of `TreatmentWorkflow` on queue `rwb-treatment` from the installments due and the payments of the plan read read-only at the ACE batch date through `recovery.v_ace_payment` (DP-05; DF-ACE-043 to DF-ACE-054) and from the break count and the limit the rule row in force carries. "The point the rule names" is the to state of the answered row, reported to the parent and applied by rwb-case: `PLAN_BROKEN` from R-RES-29, `BACK_TO_ROUTE_DECISION` from R-RES-30 and `RESTRUCTURE_BARRED` from R-RES-31, three case statuses this service never writes (BR8).

"Writes the result to the decision log with the rule version" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction as the mark, with MSG-P7-003 on failure (DP-03; RWB-PLT-E1027-CON); `decision_log_entry` stays P7's and is never written here, and the version written is the rule version in force. "Increment the break count" and "mark the plan broken" are one write on the treatment row — `outcome = BROKEN` and `outcome_at`, DF-TRT-013 and DF-TRT-014 — together with the `PlanBreak` element, because no source gives the count a column of its own and the count is composed from the case's own treatment rows (GAP-2668; ASM-4383). "Return the case to the route decision with reason broken_plan" is the stage report to the parent with the reason and the 5 working day owner task of R-RES-30; the case status and the task row are rwb-case's (GAP-2670; ASM-4385). "Its trigger arrives" is the case signal the parent `CaseWorkflow` forwards at the cure-period expiry, because the FSD names "a completed ACE batch, an event or a timer" and no source names which one.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No value a business person may change is written in code: the break limit, the cure window, the rule IDs, the condition texts and the messages are rule rows, governed rows or package content | BR-S2-011 of FSD A2.11.3.1 |
| BR2 | The break count is composed per calculation from the case's own treatment rows whose outcome is `BROKEN` and from the count the case signal carries; there is no break-count column in `rwb_treatment` | GAP-2668; ASM-4383; LOV-TRT-OUTCOME |
| BR3 | The limit is the `max_breaks` value of the rule row in force, read with its version; `break_count < max_breaks` answers R-RES-30 and `break_count >= max_breaks` answers R-RES-31 | R-RES-30; R-RES-31 |
| BR4 | Payments are read only, at the ACE batch date, from this service's own SELECT-only view, one hop inside the 2 s budget, and no payment is copied into `rwb_treatment` | DP-05; VR-S2-011-1; D-RCV-35; ADR-010 |
| BR5 | A data product older than today's ACE batch blocks the step and is named with its date; nothing is decided on a stale input | VR-S2-011-1; MSG-P1-001 |
| BR6 | The mark, the element and the decision record are written in one transaction; if the record cannot be written nothing changes and MSG-P7-003 is shown | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR7 | The case status, the case task and the case timer are never this service's: the stage reports the outcome and the reason and the parent applies the rule | DP-01; ASM-4385 |
| BR8 | A payment inside the cure window is not a break: the step reports "payment found" and leaves the clear, its state move and its record to R-RES-28 | R-RES-28; R-RES-29 condition |

**Where each rule lives in the target.** BR1 is why the limits and the window are inputs of the activity; BR2 is the count in the activity and the reason the schema gains no column; BR3 is the two condition tests of the answered row; BR4 is the SELECT-only grant and the as-at date on the element; BR5 is the guard before the comparison; BR6 is the `MANDATORY` propagation of the library write; BR7 is the boundary to rwb-case; BR8 is the reason the "payment found" answer exists instead of a silent no-op.

### 9. State transitions

None of the case statuses below is this service's; the table shows what the stage reports and what it never writes, so a reader can see the boundary of this story.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-RES-29 | `PLAN_CURE_PERIOD` | `CURE_PERIOD_EXPIRED` | no payment and cure_period passed | Reads the payments at the batch date, composes the count, marks the plan broken, records, reports `PLAN_BROKEN` | `PLAN_BROKEN` |
| R-RES-30 | `PLAN_BROKEN` | `BREAK_RECORDED` | `break_count < max_breaks` | Reports the reason `broken_plan` and the 5 working day owner task | `BACK_TO_ROUTE_DECISION` |
| R-RES-31 | `PLAN_BROKEN` | `BREAK_RECORDED` | `break_count >= max_breaks` | Reports the bar and writes nothing else; R-RES-32 excludes R1 on the next decision | `RESTRUCTURE_BARRED` |
| R-RES-36 | `PLAN_BROKEN` | `BREAK_RECORDED` | `break_count` is missing or not a number | Holds, names the field, raises a case owner task same day | `UNMATCHED_EXCEPTION` |
| R-RES-28 (read only) | `PLAN_CURE_PERIOD` | `PAYMENT_RECEIVED_LATE` | payment received inside the cure period | Answers "payment found" and moves nothing; the clear is the payment-missed branch's | `PLAN_RUNNING` |

The states of this story's own object are the treatment's: `outcome` takes `KEPT`, `BROKEN`, `COMPLETED`, `CANCELED` or `DECLINED` (LOV-TRT-OUTCOME) and the break step writes `BROKEN` once per broken plan with `outcome_at`. The `PlanBreak` element has no state machine either: it is written once per break and is not rewritten, because a second break is a second treatment and a second count. The `TreatmentWorkflow` execution has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the read and the write are activities and not workflow-local computation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the detection activity, the two reads, the mark and the tests |
| RW-CASEOWN, case owner | Owns the answered state and the returned case; works the task R-RES-30 raises in 5 working days; holds rights C, R and U on the capability area |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the broken state, the count and the reason on SCR-14; holds rights C, R and U |
| RW-TEAMMGR, RW-SPECIAL, RW-GUARANT | Hold rights C, R and U and see the mark on the treatment |
| RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the read-only roles of TSD S2 T6.1 | Right R only: they read the mark and cannot trigger a re-run |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity and reports to the parent |
| rwb-case (P3) | Owns the case, its status, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Owns the rule package, the four RESTRUCTURE rows, their approval, their effective date and the central ledger |
| ACE and its DBA | Own the `recovery.v_ace_*` views, their grants and the batch that dates them |
| The platform workflow and data owners | Own the task queue, the namespace, the ACE PostgreSQL grants and the decision-record library |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right R, C or U on each entry point. No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the treatment ID, account keys, dates, amounts, a count and versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Write (the row the element and the mark are recorded against) |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-009 | treatment | installments | Read |
| DF-TRT-013 | treatment | outcome | Write (`BROKEN`) |
| DF-TRT-014 | treatment | outcome_at | Write |
| DF-TRT-029 | treatment | first_due_date | Read |
| DF-TRT-031 | treatment | installment_amount | Read |
| DF-TRT-032 | treatment | installments_paid | Read |
| DF-TRT-033 | treatment | installment_shortfall | Read |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Read only |
| DF-ACE-001 to DF-ACE-042 | v_ace_batch_status | the product date of the ACE batch | Read only |
| DF-REF-001 to DF-REF-015 | rule_row | the RESTRUCTURE rows in force, their conditions, `cure_period` and `max_breaks` | Read |
| DF-DEC-002 to DF-DEC-016 | decision_record | the seven field groups | Write |
| DF-CAS-046 to DF-CAS-048 | recovery_case | plan_ref, plan_status, plan_status_as_of | Read on the case signal only |

`treatment` and `decision_record` are this service's own objects in `rwb_treatment`, written through its own repository and login (DP-01). The payment columns are read through the read-only view at the batch date and are not copied into any column of this service: there is no payment field and no balance field in `rwb_treatment`, and the element of RWB-S2-E3011-CON is the only shape the evidence takes. The case fields arrive on the case signal the parent forwards and are never read from a table; the rule rows are read through the rule loader and are never joined to this service's tables. The break count has no field, no identifier and no column in the Logical Data Model (GAP-2668; ASM-4383).

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no path to base `/api/recovery/treatment/v1` (DP-13): the mark and the element are read through the treatment read of RWB-S2-E3001-APP, `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (API-S2-002 of TSD S2 T-A.1), and the shape, the required fields, the versioning and the fakes of the element are declared by RWB-S2-E3011-CON and are not restated here. The step is signal-driven and unattended; it has no command of its own.

#### 12.2 REST operations consumed

None. The case status, the break count and the plan reference arrive on the case signal the parent `CaseWorkflow` forwards, not on a REST read (DP-11 is not applied: there is no in-process call left to replace). The payment evidence is a SQL read of the view in 12.7, not a REST read, and the rule rows arrive on the package event of 12.4. No source publishes an operation for this step and none is invented (GAP-2668; ASM-4383).

#### 12.3 Events published

None. The service's topic is `rwb.treatment.events.v1` with names `rwb.treatment.<Event>.v1` (DP-14), and its one catalogued event EV-10 `rwb.treatment.TreatmentApproved.v1` belongs to the offer story of this service (TSD S2 T5.3). REQ-S2-009 says a broken plan "raises an event"; in this slice the event is the `BREAK_RECORDED` stage report delivered to the parent `CaseWorkflow` as a Temporal signal inside the case, and no Kafka event is published, because the plan gives this story no DP-09 dependency (H RWB-PLT-TE006-CON) and the ownership rows give S2 one event only (GAP-2669; ASM-4384).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Loads the RESTRUCTURE package and route set in force, verifies the checksum, swaps them atomically and keeps the last good set on failure; EV-30 |
| `rwb.payment.PaymentMissed.v1` | `rwb.payment.events.v1` | P8 rwb-payment | Carries `treatmentId`, `dueDate` and `amountDue`; it opens the cure period at R-RES-27 and is read by the payment-missed branch, which is RWB-S2-E3010-APP; this story's branch is entered at the cure-period expiry of the same plan (EV-12) |

Both subscriptions are the service template's inbox and rule loader; this story adds no subscription of its own. The service listens to P7 and P8 events on the connection matrix of Architecture v5 slide 13.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (the break branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-treatment` in namespace `rwb-recovery` | Input: the case ID, the treatment ID, the case status on the signal, the break count and the plan reference. Output: the stage report with the break count, the limit, the reason, the rule version |
| `EvaluateRules` | Activity of the template | `rwb-treatment` | The package and route set in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `detectBrokenPlan` | Activity | `rwb-treatment` | The payment view read at the batch date, the plan terms on the treatment and the break count in; the `PlanBreak` of RWB-S2-E3011-CON out; retried by the workflow, with the stale guard non-retryable |
| `RecordAndApply` | Activity of the template | `rwb-treatment` | The element, the outcome and the decision record in one transaction, then the stage report |

The workflow name is fixed by Temporal and Drools Design slides 5 and 11; the three activity names are this story's choice. The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts; `NoPackageInForce` and a stale product non-retryable). A replay never re-reads the view: the answer is recorded by the activity and read from history, and the branch is idempotent on the treatment, the rule version and the count, so a repeated signal writes no second mark.

#### 12.6 Schedules

None. The step is signal-driven from the case and owns no Temporal Schedule and no legacy Quartz job; the ownership rows give S2 no job. The cure-period expiry that enters the branch and the 5 working day task of R-RES-30 are timers of the case and the treatment (`timer.treatment_id`, DF-WRK-042), driven by the workflow platform and created by rwb-case, not a schedule of this service.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Created by the per-service Flyway sequence and written here for `outcome`, `outcome_at` and the element; DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, with no break-count, payment or limit column |
| `decision_record` | `rwb_treatment` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). Two `recovery.v_ace_*` views of the ACE database are read, `v_ace_payment` and `v_ace_batch_status`, read only at the ACE batch date and with no copy kept; the case table and the task and timer rows of rwb-case, the rule tables of rwb-decision and the payment tables of rwb-payment are never named in SQL.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3011-CON element fake | The `PlanBreak` shape | A complete element; one per missing required field; an element with and without the rule version |
| ACE payment view fixture | `v_ace_payment` and `v_ace_batch_status` | No payment in the cure window; a payment inside it; a partial payment; a product dated yesterday; an unreachable view |
| Case-signal fake | The signal the parent forwards | `PLAN_CURE_PERIOD` with a break count; a count that is missing; `PLAN_BROKEN` with a count below, at and above the limit |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Rule-package fake | The package and RESTRUCTURE rows in force | Version `RESTRUCTURE-2026.11` with R-RES-29, R-RES-30, R-RES-31 and R-RES-36; a set with no matching row; a checksum mismatch |

The payment fixture and the case-signal fake are the Day-1 unblockers: the build and every test run against them, and no test reads a production view or needs a live case.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The step is signal-driven; the mark rides the treatment read of RWB-S2-E3001-APP |
| Kafka | 0 | 2 events (`rwb.decision.RulePackageInForce.v1`, `rwb.payment.PaymentMissed.v1`) | Own topic, no row written by this story; inbox dedupe by cloud event id |
| Temporal | `TreatmentWorkflow` and 3 activities on `rwb-treatment` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; no Schedule |
| SQL view | 0 | 2 (`recovery.v_ace_payment`, `recovery.v_ace_batch_status`) | Read only, at the batch date, no copy |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `planbreak` and `workflow`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13; §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only view, because the Work Package records no contract dependency on P1; the reading and the conflict with Architecture v5 slide 8 are in GAP-2654 and ASM-4362. DP-03 is the record of the mark, DP-13 the base this story declares nothing on, and DP-19 the path the broken state is read on.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PlanBreakBranch` | Workflow | The branch of `TreatmentWorkflow` that opens the step, reports the outcome and waits |
| `EvaluateRules` | Activity | Runs the package and route set in force and returns the rule ID, the action and the next event |
| `detectBrokenPlan` | Activity | Reads the view, applies the stale guard, composes the break count and the limit test, builds the element |
| `AcePaymentReader` | Repository | The two read-only view queries; no entity and no cache beyond the request |
| `PlanBreakRepository` | Repository | Writes `outcome`, `outcome_at` and the element against the treatment row |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report with the reason, the count and the 5 working day task, and the officer messages |

**Database.** No new table and no new column: the step writes `treatment.outcome` (DF-TRT-013) and `treatment.outcome_at` (DF-TRT-014) in `rwb_treatment`, and `decision_record` is the library object of DP-03. A break-count column is deliberately not added; if the count must be persisted it becomes a field of the Logical Data Model first (GAP-2668; ASM-4383).

**Configuration and reference data.** The break limit, the cure window and the four rule rows are data of rwb-decision with a version and are read, never configured here. The retry numbers, the activity name and the 2 s budget are configuration of the activity. The capability area "Treatment and offer" and the rights are access data of P4 read through the guard library.

**Build steps**

1. The branch of `TreatmentWorkflow` on `rwb-treatment`, its input record and the stage report with the reason.
2. `EvaluateRules` against the package fake, with R-RES-29, R-RES-30, R-RES-31 and R-RES-36 as rule rows and the `NoPackageInForce` answer.
3. `AcePaymentReader` against the view fixture, with the batch-date test and MSG-P1-001 (AC1, X1).
4. `detectBrokenPlan` with the count, the limit test and the "payment found" answer (AC1, AC2, AC3, X2).
5. The `PlanBreak` element of RWB-S2-E3011-CON and the mark of `outcome` and `outcome_at` (AC2, AC3).
6. `RecordAndApply` with the record in the same transaction and the rollback path of MSG-P7-003 (AC4).
7. The missing-count path with MSG-GEN-001 and the case owner task (X3).
8. Tests for AC1 to AC4 against the fakes, the component tests of X1, X2, X5 and X8, and the replay test of X7.

**Feature flag.** `rwb.treatment.plan-break`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the view and the package faked, the treatment shows `outcome = BROKEN` with its date and its element, the record is written in the same transaction and rolls back with the action, the stale product path blocks with MSG-P1-001, and the case returns to the route decision on the report with the 5 working day task.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product the step reads is older than today's ACE batch | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A required value is missing, for example the break count, and the step cannot decide | Enter {field}. |
| MSG-GEN-006 | The payment view does not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

The texts are copied unchanged from the legacy story, FSD S2 A2.11.3.1 and the platform message set, and this story adds no message ID. MSG-S2-001, MSG-S2-002 and MSG-S2-003 of the legacy validation table are the offer floor, the stale payoff and the offer end date and are raised by the offer stories of this service, not here. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record shows the treatment, its terms, its status and the booking confirmation, in the states `Draft`, `submitted`, `approved`, `booked` and `broken`. This story makes the `broken` state visible: the outcome, its date, the break count against the limit and the reason `broken_plan` are read on the same screen through the gateway-bff composite route, which calls rwb-case and rwb-treatment and composes the answer (DP-19; Architecture v5 slide 41). The screen field list and the route specification belong to the platform edge story and the screen owner; this story fixes what the service marks and what the sibling story's read returns. A blocked step is shown as its message with the product and its date, never as a broken plan.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-011-01 | AC1 | End to end | Detect and handle a broken plan |
| TC-E3-011-02 | AC2 | End to end | Rule R-RES-29 |
| TC-E3-011-03 | AC3 | End to end | Rule R-RES-30 |
| TC-E3-011-04 | AC4 | End to end | Not recorded |
| TC-E3-011-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-011-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The legacy test case IDs, their Covers and their Data are kept in order and character for character; the story level "System" of the legacy suite is carried as "End to end" and the two exception cases as "Component", as in the other stories of this run. TC-E3-011-05 and TC-E3-011-06 restate the same guard as the legacy suite, so they run once each. The payment-view, case-signal, element, decision-record and rule-package fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The `-ITG` copies (TC-E3-011-01-ITG to TC-E3-011-06-ITG) belong to the wave 2 integration harness (RWB-ITG-W2) and are not written by this story. The contract's own tests are TC-S2-E3011-CON-01 to -05 and are owned by RWB-S2-E3011-CON.

### 17. Guardrails

- No value a business person may change is written in code: the break limit, the cure window, the rule IDs, the condition texts and the six messages are rule rows or package content, never constants (BR-S2-011; BR1, BR3).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the treatment ID, account keys, dates, amounts, a count and versions only, and the fixture is synthetic.
- No read of another service's tables: the case arrives on the signal, the rule rows on the package event, and nothing joins across a schema (DP-01).
- No copy of ACE data: the payment view is read at the batch date and no payment or balance column exists in `rwb_treatment` (BR4; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only two views with SELECT granted to this service's login (ASM-4362).
- No live view and no live rule package in any test: the fixture and the fake are the only endpoints, so a red test never depends on the ACE batch or on P7's estate.
- No business value in the record: the `DecisionRecord` carries the rule ID, the rule version, the count, the limit and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule (BR7).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-009 | A broken plan raises an event and returns the case to a decision rather than leaving it in a plan state | Business Requirements Program, section 5.9; FSD S2 requirements | FEAT-TRT-11 | 05 Restructure; 07 Route, settle and claim | R-RES-29; R-RES-30; R-RES-31; R-RES-36 | TC-E3-011-01, TC-E3-011-02, TC-E3-011-03, TC-E3-011-04, TC-E3-011-05, TC-E3-011-06 |

REQ-S2-009 is the one requirement whose text names this behaviour, so the trace runs on it; TSD S2 T8 maps the same ID to FEAT-TRT-01, which is the "written one epic ahead" placeholder of the module, and the feature code is carried alongside until the C1 PRD settles the mapping (Section 19). The legacy key also names FEAT-OCC-11 as its prerequisite; no requirement of this module references that prerequisite, so it is not carried as a row.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3011-CON | Contract | H: declares the `PlanBreak` element, the read rule of the payment view, the break-count rule, the versioning rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-14 shows the broken state |
| RWB-S2-E3010-APP | App development | Sibling: books the plan, sets the schedule and opens the cure period at R-RES-27; this branch starts where that one leaves the plan |
| RWB-S2-E3001-APP | App development | Sibling: the treatment record and the read that returns the element and the outcome |
| RWB-S2-E3007-APP, RWB-S2-E3009-APP | App development | Siblings: the offer with its validity and the return to the prior status, which use the same stage report |
| S1 rwb-valuation | Service | The route decision the case is returned to; it re-scores the open routes when the case arrives |
| P3 rwb-case | Service | The case, its status, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Service | The rule package and the four RESTRUCTURE rows; EV-30 is consumed here |
| P8 rwb-payment | Service | The payment matching and EV-12 `rwb.payment.PaymentMissed.v1` |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the read and the report against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published element, the read rule of the payment view, the break-count rule, the versioning and the fakes: RWB-S2-E3011-CON.
- The cure period, its open at R-RES-27 and its clear at R-RES-28, and the plan timers of R-RES-25: RWB-S2-E3010-APP and the payment-missed branch of this service.
- The treatment record, its create and read operations, its states and its read representation: RWB-S2-E3001-APP.
- The offer, its validity and the return to the prior status: RWB-S2-E3007-APP and RWB-S2-E3009-APP.
- The route decision, its scoring, its approval and the exclusion of R1 at R-RES-32: S1 rwb-valuation and rwb-case.
- The case, its status, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3), reached only through the forwarded case signal and the stage report.
- The payment matching that finds a missed installment, the payment posting and `rwb.payment.PaymentMissed.v1`: P8 rwb-payment.
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA (GAP-2654).
- The rule authoring, the four-eyes approval, the effective date, the rollback of the RESTRUCTURE rows and the central ledger: rwb-decision (P7).
- A Kafka event for a broken plan, its name, its schema and its consumers: not published by this story; raised as GAP-2669 and ASM-4384.
- SCR-14, its field list and the gateway-bff composite route: the platform edge story and the screen owner (DP-19).
- The real cross-service proof against the live owners and the `-ITG` copies of the legacy cases: RWB-ITG-W2.

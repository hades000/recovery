# RWB-S2-E3005-APP Pre-assess affordability through ACE

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-005 for rwb-treatment. The affordability step leaves the monolith's in-process module call and becomes the affordability branch of `TreatmentWorkflow` on this service's own task queue; the ACE Common restructure calculator is reached as one Temporal Nexus operation into the `ace-collection` namespace and is no longer a module interface call; the result is an `AffordabilityResult` recorded against the treatment in `rwb_treatment` with its local decision record written in the same transaction (DP-03); this story declares no REST operation of its own, so the legacy monolith base is not carried (DP-13); the two screens are reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S2-P |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3005-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the affordability step of a TDR restructure to run as the affordability branch of `TreatmentWorkflow` — rules R-RES-06 and R-RES-07 evaluated in this service, one Nexus operation into `ace-collection` for the ACE Common restructure calculator with the plan inputs of the case, and the `AffordabilityResult` recorded against the treatment together with its decision record** — so that **the officer receives the calculated plan and builds the offer in days instead of chasing a hand-tracked affordability check for 23 to 26 days**.

This is the application slice of legacy RWB-E3-005. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the business rules, data rows and messages they depend on;
- the affordability branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`: the step that evaluates the RESTRUCTURE package, reports R-RES-06 from `WITH_FCR_OFFICER` and R-RES-07 from `AFFORDABILITY_IN_ACE`, calls the calculator, records the answer and reports the stage outcome to the parent `CaseWorkflow` (Temporal and Drools Design slides 13 and 18; Architecture v5 slide 18);
- the `calculateAffordability` activity and the Nexus binding it calls: one operation, `calculateRestructurePlan`, in the `ace-collection` namespace, with the case ID, the plan inputs and the rule version in the request and the affordability result, the plan reference, the installment amount, the installment count and the calculated-at time in the answer (Architecture v5 slide 18, OUT line "NEXUS ACE Common: restructure calculator (Nexus)"; ASM-3071);
- the `AffordabilityResult` recorded against the treatment row in schema `rwb_treatment`, with no affordability or band column copied out of ACE, and the treatment terms the answer carries (`installment_amount`, `installments`) written on the same row (DF-TRT-009, DF-TRT-031; DP-01);
- the local decision record of the step, written through `DecisionRecordWriter.record(DecisionRecord)` in the caller's transaction (DP-03; RWB-PLT-E1027-CON);
- the refusal path when the calculator does not answer — the stage stays in `AFFORDABILITY_IN_ACE`, nothing is written and the caller sees MSG-GEN-006 — and the stale-input path, MSG-S2-002 for a stale payoff.

It does not own: the published contract of the affordability element and the Nexus binding, which is RWB-S2-E3005-CON; the treatment record, its create operation and its read operation, which are RWB-S2-E3001-APP; the settlement offer and its floor rules, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the offer build and the plan installment range, which are RWB-S2-E3004-APP; the case record and every case status, which are rwb-case's and arrive on the case signal the parent forwards; the rule authoring, approval and publication of the RESTRUCTURE package, which are P7 rwb-decision's; the two screens and their composite route, which are the platform edge story's and the screen owners' under DP-19; and the ACE Common restructure calculator itself, which is an existing ACE capability with its own owner.

### 2. Business rationale

In the monolith the affordability check was a call from `TdrSettlementAndDeedInLieuService` into the ACE common module through a published Java interface, inside the same process and the same `recovery` schema, and the result was written against the offer and into `decision_log_entry` (TSD S2 T1 and T2; INT-34 "ACE common module — published module interface"). Two facts made the legacy step expensive: the call was in-process, so no service could be built, tested or released without the other side; and the result had no contract, so nothing downstream could read it without reading the module's tables.

Architecture v5 changes the call type. The service catalogue on slide 18 gives rwb-treatment one OUT line for the calculator — "NEXUS ACE Common: restructure calculator (Nexus)" — and slide 39 lists the restructure calculator (Nexus) among the ACE Common contracts the ACE team owns. The Temporal and Drools Design fixes the shape of that call: the shared cluster runs namespace `rwb-recovery` with one task queue per service, `ace-collection` is ACE's namespace and is "reached through Nexus (for example the restructure calculator)", with Temporal 1.30+ for Nexus (Temporal and Drools Design slide 11 notes; Architecture v5 slide 39 decision 3). So the calculator is neither a REST contract of the 19 services nor a table, and it is not one of the 19 services.

What D-RCV-60 changes is therefore three things and nothing else. The step becomes a branch of the stage workflow the service owns (slide 13: each stage is a child workflow on the owner's queue, and S2's child is `TreatmentWorkflow` with REST 37, SET 27 and DIL 37 rules). The rules that decide the branch are evaluated locally from the RESTRUCTURE package in force, and the package version is named on the answer, so the version that decided is readable afterwards (EV-30; slide 15). And the result becomes a recorded fact on the treatment, with its decision record in the same transaction, instead of a value in one module's memory and a row in a shared log.

Serves REQ-S2-001 (a restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench) and the A2.5.1 target of the FSD: restructure turnaround 5 days, measured from the decision log and the Workbench records. No business value moves: the state names, the rule IDs, the two-working-day timer of R-RES-06 and the messages are the legacy values, held as data and as rule rows, never as code constants.

### 3. Preconditions

- RWB-S2-E3005-CON is published: the `AffordabilityResult` element, its required and optional fields, the Nexus operation name, request and response, the 2 s budget, the failure answer and the fakes are baselined and handed to this story. The build starts against the Draft baseline, as every CON story of this run publishes on Day 1 at status Draft (realignment v1).
- The `ace-collection` namespace, the Nexus endpoint of the ACE Common restructure calculator and the operation name are the working read of ASM-3071, because Architecture v5 slide 18 names the calculator by call type only and TSD S2 T5.1 gives INT-34 as a "published module interface" with no operation (GAP-1875). The ACE Common owner and the platform workflow owner confirm both at the wave 2 contract freeze.
- RWB-PLT-E1027-CON is in place: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` transaction rule, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is in place, so the answer reaches SCR-14 and SCR-15 through the gateway-bff composite route (DP-19).
- The service template's wave-0 capabilities are in place: the embedded Drools runtime and the rule-package loader that swaps a package on `rwb.decision.RulePackageInForce.v1`, the access guard library, and the outbox and inbox library (ASM-3063; ASM-3064). This story adds no build dependency of its own for them, because the Work Package lists none.
- The `treatment` table exists on the per-service Flyway sequence of rwb-treatment with DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, and `decision_record` is created as the platform library object in `rwb_treatment`.
- The RESTRUCTURE package is in force in this service's rule cache at the version the answer names; the package carries R-RES-06 and R-RES-07 and their conditions (`treatment_type = TDR`, `affordability_result = pass`) as rule rows, not as code.
- The case status is readable only as the stage sees it: the parent `CaseWorkflow` of rwb-case forwards the case signal to the running child, so the stage reacts to `WITH_FCR_OFFICER` and to `AFFORDABILITY_IN_ACE` without reading the case table and without writing a case status (EV-29; ASM-3062; DP-01).
- No approval stop: a Draft contract baseline is enough to build and test, and nothing in this story needs a human sign-off to start on Day 1.

### 4. Flow

1. rwb-case: the case reaches `WITH_FCR_OFFICER` through R-RES-04 and the parent `CaseWorkflow` forwards the case signal to the `TreatmentWorkflow` child of that case (Temporal and Drools Design slide 13 notes; EV-29).
2. `TreatmentWorkflow`: the event `AFFORDABILITY_REQUIRED` arrives on the case signal with `treatment_type = TDR`; the step calls `EvaluateRules` and the RESTRUCTURE package in force returns R-RES-06 with its action "Send the case to ACE for affordability and plan calculation".
3. `calculateAffordability` activity: assembles the request — the case ID, the plan inputs of the case and the version of the rule package in force — and calls the Nexus operation `calculateRestructurePlan` in the `ace-collection` namespace, synchronously, inside the 2 s budget of the one-hop rule.
4. The calculator answers `affordabilityResult`, `planRef`, `installmentAmount`, `installmentCount` and `calculatedAt`, with the rule ID and the rule version it applied where it reports one of its own (ASM-3071).
5. `RecordAndApply` activity, one transaction: the `AffordabilityResult` is written against the treatment, `treatment.installment_amount` and `treatment.installments` take the accepted plan terms, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with the rule ID and the rule version and the `affordability_result` in the final call, and the parent receives the stage report `AFFORDABILITY_IN_ACE` with the plan reference.
6. rwb-case: the parent applies R-RES-06 for the status and moves the case to `AFFORDABILITY_IN_ACE`; this service writes no case row and publishes no case event for it (ASM-3062).
7. The calculator answers `pass`: `EvaluateRules` returns R-RES-07, the stage reports `AFFORDABILITY_PASSED` with the calculated plan, and the parent applies the rule to return the case to `WITH_FCR_OFFICER`. The plan reference and the accepted terms are what the officer sees on SCR-14 and reads through the treatment read of RWB-S2-E3001-APP.
8. The calculator does not answer inside the budget: the activity is retried by the workflow's retry policy; when the attempts are exhausted the stage stays in `AFFORDABILITY_IN_ACE`, nothing is written, and the caller sees MSG-GEN-006 naming the ACE Common system.
9. A stale payoff reaches the step (a settlement figure whose `payoff_date` is older than the case's allowed age): the step reports the warning MSG-S2-002, requests a fresh figure, and does not call the calculator until a figure inside the age is on the case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The calculator does not answer inside the 2 s budget, or the Nexus endpoint is unavailable | The workflow retries per its policy; when the attempts are exhausted the stage stays in `AFFORDABILITY_IN_ACE`, nothing is written and the case does not move | MSG-GEN-006 | AC1, AC3 |
| X2 | The calculator answers `fail` | R-RES-07 does not fire; the stage reports `AFFORDABILITY_FAILED` and the parent applies R-RES-08 to return the case to the route decision with reason `affordability_failed`; no offer is built | None | Section 8 |
| X3 | The decision record cannot be written | The transaction rolls back: no affordability result, no plan terms, no stage report; the caller sees MSG-P7-003 and an incident is raised | MSG-P7-003 | AC4 |
| X4 | The record is refused for a missing field | Nothing is written and the field is named; the stage stays where it was and the incident names MSG-P7-009 | MSG-P7-009 | Section 12.8 |
| X5 | A role without the right tries to trigger the step or read its result | 403 from the access guard, nothing changes; the step run itself is unattended under the service identity and is not a user action | MSG-P4-002 | AC1, AC2, AC3 |
| X6 | The RESTRUCTURE package is not in force, or its checksum does not match | `EvaluateRules` answers `NoPackageInForce`; the workflow does not retry that answer and the step does not call the calculator | MSG-GEN-006 | Section 12.4 |
| X7 | The payoff figure on the case is stale | The step warns, requests a fresh figure and does not call the calculator until a figure inside the age is on the case | MSG-S2-002 | Section 4 |
| X8 | A second `AFFORDABILITY_REQUIRED` arrives while the branch is waiting on the calculator | The inbox dedupes by the cloud event id of the case signal and the workflow start is idempotent, so no second call is made in the same step | None | Section 12.5 |

X1, X3, X5 and X7 are the legacy paths of RWB-E3-005 carried onto the split. X2 is the legacy R-RES-08 answer on the same branch. X4 is the platform library's refusal path, X6 is the rule loader's no-package answer, and X8 is the inbox dedupe of the service template.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3005-CON and its fakes, the decision-record library and the gateway route; the calculator is mocked and never called live, so the story needs no ACE Common deployment to start |
| Negotiable | The activity name, the record shape of the stage report and the retry numbers are this story's choice; the two rules, their conditions, the operation name and the failure answer are fixed |
| Valuable | The restructure reaches the officer with a calculated plan in days, and the affordability result is a recorded fact with its rule version |
| Estimable | One workflow branch, one activity, one Nexus client, one result repository, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic case and a calculator fake, plus one contract test of the binding and one component test of the refusal path |

### 7. Acceptance criteria

```gherkin
Feature: Pre-assess affordability through ACE

  Background:
    Given treatment "TRT-SYN-0501" of case "RW-2026-000512" is a RESTRUCTURE plan and the case is at WITH_FCR_OFFICER
    Given the RESTRUCTURE rule package in force is version "RESTRUCTURE-2026.11" and carries R-RES-06 and R-RES-07

  Scenario: AC1 Pre-assess affordability through ACE (legacy RWB-E3-005 AC1)
    Given the ACE Common contract mock returns a passed affordability result and the calculated plan
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then calls the ACE affordability calculation and records the result against the offer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-06 (legacy RWB-E3-005 AC2)
    Given the rwb-case contract mock returns case status WITH_FCR_OFFICER
    Given a case in state WITH_FCR_OFFICER
    When affordability required
    Then send the case to ACE for affordability and plan calculation
    Then the case moves to AFFORDABILITY_IN_ACE

  Scenario: AC3 Rule R-RES-07 (legacy RWB-E3-005 AC3)
    Given the rwb-case contract mock returns case status AFFORDABILITY_IN_ACE
    Given a case in state AFFORDABILITY_IN_ACE
    When affordability passed
    Then return the calculated plan to the officer and build the offer
    Then the case moves to WITH_FCR_OFFICER

  Scenario: AC4 Not recorded (legacy RWB-E3-005 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line above keeps its wording; what changes is where it runs, who produces the fact and how it is reached. "Calls the ACE affordability calculation" in AC1 is no longer an in-process call into the ACE common module under INT-34: it is one Temporal Nexus operation, `calculateRestructurePlan`, into the `ace-collection` namespace, and Architecture v5 slide 18 fixes that call type on the OUT side of rwb-treatment ("NEXUS ACE Common: restructure calculator (Nexus)") while slide 39 lists the restructure calculator (Nexus) among the ACE Common contracts (Temporal and Drools Design slide 11 notes: "ace-collection is ACE's namespace, reached through Nexus (for example the restructure calculator)"). It is therefore not a REST contract of the 19 services and not a direct call to a TDR system: the "ACE and TDR" integration of FSD A2.5.2 is the calculator speaking to ACE, and the Workbench's only edge is the Nexus operation. The operation name, the request and response fields, the 2 s budget, the failure answer and the fields of the answer are not specified in any source document and are the working read of ASM-3071 (GAP-1875); the operation is faked in every test and never called live. "Records the result against the offer" is the `AffordabilityResult` of RWB-S2-E3005-CON written against the `treatment` row in `rwb_treatment`, with its plan terms on the same row and no affordability or band column copied from ACE (DP-01). "Writes the result to the decision log" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction with MSG-P7-003 on failure (DP-03; RWB-PLT-E1027-CON), and `decision_log_entry` stays P7's and is never written here. The state of AC2 and AC3 is rwb-case's: the stage sees it on the case signal the parent `CaseWorkflow` forwards (EV-29; Temporal and Drools Design slide 13) and reports the outcome back, so "the case moves to AFFORDABILITY_IN_ACE" and "moves to WITH_FCR_OFFICER" are the parent applying R-RES-06 and R-RES-07, and no case table is read or written here (ASM-3062; DP-01). The rules themselves are evaluated from the RESTRUCTURE package in force, which arrives through `rwb.decision.RulePackageInForce.v1` from P7 and is the service template's wave-0 capability (ASM-3063). The screens that show the result are SCR-14 and SCR-15, reached through the gateway-bff composite route (DP-19; Architecture v5 slides 41 and 42), and the result is read there through the treatment read of RWB-S2-E3001-APP (DP-13).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | From `WITH_FCR_OFFICER`, on `AFFORDABILITY_REQUIRED`, when `treatment_type = TDR`, the case is sent for affordability and plan calculation and moves to `AFFORDABILITY_IN_ACE`, inside a two-working-day timer | R-RES-06; TSD S2 T4 |
| BR2 | From `AFFORDABILITY_IN_ACE`, on `AFFORDABILITY_PASSED`, when `affordability_result = pass`, the calculated plan is returned to the officer and the offer is built, and the case returns to `WITH_FCR_OFFICER` | R-RES-07; TSD S2 T4 |
| BR3 | On `AFFORDABILITY_FAILED` the stage reports the failure and the parent returns the case to the route decision with reason `affordability_failed`; this service builds no offer and moves no status itself | R-RES-08; ASM-3062 |
| BR4 | The calculator is the ACE Common restructure calculator, reached as one Nexus operation in the `ace-collection` namespace and never as a table, a shared schema or a REST contract of the 19 services | INT-34; Architecture v5 slides 18 and 39; Temporal and Drools Design slides 11 and 13 |
| BR5 | The affordability result is recorded against the treatment, and no affordability band, score or result column is copied from ACE into `rwb_treatment` | DP-01; ASM-3071 |
| BR6 | The result and the plan terms are written with their decision record in one transaction; if the record cannot be written, nothing changes and MSG-P7-003 is shown | DP-03; RWB-PLT-E1027-CON; ADR-022 |
| BR7 | The rule version that decided is written on the record and on the answer; no rule ID, state name, threshold or timer value is written in code, it is read from the package in force and from the reference data | BR-S2-005 of FSD A2.5.3.1; EV-30; Temporal and Drools Design slide 15 |
| BR8 | A stale payoff is not used: the step warns with MSG-S2-002, requests a fresh figure and waits | RWB-E3-005 validation and messages; R-SET-03 |

**Where each rule lives in the target.** BR1 and BR2 are the two rows of the RESTRUCTURE decision table this story evaluates, and the states they name belong to rwb-case: the stage reacts to the state it is signalled and reports the outcome, while the status change is the parent's (ASM-3062; DP-01). BR3 is the failure branch of the same table. BR4 is the call type of the `calculateAffordability` activity and the reason the calculator is faked rather than stubbed as a service. BR5 is the schema rule: the `treatment` row keeps DF-TRT-009 and DF-TRT-031 from the answer and gains no band column. BR6 is the `MANDATORY` propagation of the library write. BR7 is why the package version is an input of the activity and a field of the record. BR8 is the guard before the call, and it is the only legacy warning this story raises of its own.

### 9. State transitions

None of the case statuses below is this service's. The table shows the two rules as the stage reports them and names the owner of the status column, so a reader can see what this story sends and what it never writes.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-RES-06 | `WITH_FCR_OFFICER` | `AFFORDABILITY_REQUIRED` | `treatment_type = TDR` | Evaluates the rule, calls the calculator, records the result, reports `AFFORDABILITY_IN_ACE` with the plan reference | `AFFORDABILITY_IN_ACE` |
| R-RES-07 | `AFFORDABILITY_IN_ACE` | `AFFORDABILITY_PASSED` | `affordability_result = pass` | Reports the calculated plan and the accepted terms to the parent and to the officer | `WITH_FCR_OFFICER` |
| R-RES-08 | `AFFORDABILITY_IN_ACE` | `AFFORDABILITY_FAILED` | `affordability_result = fail` | Reports the failure with the calculator's answer; no offer is built | `BACK_TO_ROUTE_DECISION` |

The states of this story's own objects are the treatment's (`Draft`, `submitted`, `approved`, `booked`, `broken`, as SCR-14 shows them) and they belong to the sibling stories of this service; the `AffordabilityResult` has no state machine of its own — it is written once per calculation and replaced only by a later calculation on the same treatment. The `TreatmentWorkflow` execution of a case has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the calculator call is an activity and not a workflow-local computation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the activity, the Nexus client, the result record and the tests |
| RW-RESTRUCT, restructuring officer (FCR) | Triggers the step through the case and reads the calculated plan and the offer; holds right C, R and U on the capability area |
| RW-CASEOWN, RW-SPECIAL, RW-GUARANT | Hold right C, R and U on the capability area and see the result on the treatment |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the read-only roles of TSD S2 T6.1 | Right R only: they read the result and cannot trigger a recalculation |
| RW-PRODHEAD, RW-CREDCOMM | Right R and right A: they approve, and they read the result |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity; the stage reports to the parent and takes no status of its own |
| rwb-case (P3) | Owns the case, its status and the two rules' state column; forwards the case signal to this child workflow |
| P7 rwb-decision | Owns the RESTRUCTURE package, its approval, its effective date and the central ledger |
| The ACE Common owner | Owns the restructure calculator, its namespace and its Nexus endpoint |
| The platform workflow owner | Owns the `rwb-treatment` task queue, the namespace and the Nexus binding the activity uses |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right C, R or U on each entry point and calls the guard, and it implements no rule of its own (ASM-3064). No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the treatment ID, codes, amounts and the rule version only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Write (the row this step records against) |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-009 | treatment | installments | Write (from the calculator's `installmentCount`) |
| DF-TRT-011 | treatment | approval_level | Read |
| DF-TRT-013 | treatment | outcome | Read |
| DF-TRT-031 | treatment | installment_amount | Write (from the calculator's `installmentAmount`) |
| DF-TRT-032 | treatment | installments_paid | Read |
| DF-TRT-033 | treatment | installment_shortfall | Read |
| DF-DEC-002 to DF-DEC-016 | decision_record | the seven field groups | Write |
| Not specified in the source documents (GAP-1875; ASM-3071) | treatment | the affordability result fields (`affordabilityResult`, `planRef`, `calculatedAt`) | Write |

`treatment` is this service's own table, written in `rwb_treatment` through its own repository and login; it is never read from another service (DP-01). The affordability result has no field in TSD S2 T3.1 and no BR Field ID in the Logical Data Model, so the element and its field names are the working read of ASM-3071 and the identifiers wait for the contract freeze (GAP-1875). `decision_record` is the platform library object created in this schema and written only through `DecisionRecordWriter`; `decision_log_entry` is P7's and is never named in SQL here (DP-03). The case, its status and its plan inputs are not read from a table: they arrive on the case signal the parent forwards (ASM-3062).

### 12. Contract

#### 12.1 REST operations provided

None. This story declares no REST operation of its own and adds no path to base `/api/recovery/treatment/v1` (DP-13): the affordability step is triggered by the case signal and its result is read through the treatment read owned by the sibling story RWB-S2-E3001-APP (API-S2-002 of TSD S2 T-A.1). The shape of the answer, the Nexus binding and the fakes are declared by RWB-S2-E3005-CON and are not restated here.

#### 12.2 REST operations consumed

None as a REST contract. The one cross-boundary call of this story is the Nexus operation named in 12.5; it is not an OpenAPI operation and is not reached through the gateway. The case status is not consumed as a REST read either: it arrives on the case signal the parent `CaseWorkflow` forwards (EV-29; ASM-3062).

#### 12.3 Events published

None. The service's topic is `rwb.treatment.events.v1` with names `rwb.treatment.<Event>.v1` (DP-14), and its two events `TreatmentApproved` and `TreatmentClosed` belong to the offer and closure stories of this service. This story publishes no event and writes no outbox row of its own; the stage report to the parent is a Temporal signal inside the case, not a Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Loads the RESTRUCTURE package, verifies its checksum, swaps it atomically and keeps the last good package on failure; EV-30 |

The event is consumed by the service template's rule loader, and this story reads the version it put in force (ASM-3063; Temporal and Drools Design slides 11 and 15). `rwb.payment.TreatmentBooked.v1` (EV-11), `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.deviation.DeviationRaised.v1` (EV-06) are the other consumed events the service has available; they drive the booking, cure-period and deviation branches of `TreatmentWorkflow`, which belong to the offer and closure stories of this epic and not to this one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (the affordability branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-treatment` in namespace `rwb-recovery` | Input: the case ID, the treatment ID, the case status on the signal, the event. Output: the stage report `AFFORDABILITY_IN_ACE` or `AFFORDABILITY_PASSED` with the plan reference |
| `EvaluateRules` | Activity of the template | `rwb-treatment` | The RESTRUCTURE package version in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `calculateAffordability` | Activity | `rwb-treatment` | The request of 12.2 of RWB-S2-E3005-CON: case ID, plan inputs, rule version; the answer: `affordabilityResult`, `planRef`, `installmentAmount`, `installmentCount`, `calculatedAt`, `ruleId`, `ruleVersion`; one Nexus operation `calculateRestructurePlan` in namespace `ace-collection`, 2 s synchronous budget, retried by the workflow |
| `RecordAndApply` | Activity of the template | `rwb-treatment` | The result, the plan terms, the decision record and the stage report in one transaction |

The workflow and activity names are the target design and are fixed by Temporal and Drools Design slides 13 and 18 for the workflow and by this story for the three activities (ASM-3071). The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts; `NoPackageInForce` non-retryable, slide 14 notes). A replay never re-calls the calculator: the answer is recorded by the activity and read from history.

#### 12.6 Schedules

None. The step is signal-driven from the case and owns no Temporal Schedule and no legacy Quartz job; the two-working-day timer of R-RES-06 is the durable timer of the workflow, not a schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Created by the per-service Flyway sequence and written here for the result and the plan terms; DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, with no affordability or band column |
| `decision_record` | `rwb_treatment` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). The case table of rwb-case, the rule tables of rwb-decision and the calculator's own store are never named in SQL: the case arrives on the signal, the package arrives on the event, and the calculator through Nexus.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| ACE Common calculator fake (RWB-S2-E3005-CON) | The Nexus operation `calculateRestructurePlan` | A passed answer with a plan reference, an installment amount, a count and a calculated-at time; a failed answer; a timeout inside and beyond the 2 s budget; an answer with no plan reference |
| RWB-S2-E3005-CON element fake | The `AffordabilityResult` shape | A complete element; one missing required field; a version label |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| rwb-case status fake | The case status on the case signal | `WITH_FCR_OFFICER`, `AFFORDABILITY_IN_ACE`, and a case that moved away before the answer arrived |
| Rule-package fake | The RESTRUCTURE package in force | Version `RESTRUCTURE-2026.11` with R-RES-06 and R-RES-07; a version with no matching row; a checksum mismatch |

The calculator fake is the Day-1 unblocker: the build and every test run against it, and no test calls the live calculator. The decision-record, rule-package and case fakes are the platform library's and the published contracts of their owners.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The result is read through the sibling story's treatment read; nothing of this story is an OpenAPI operation |
| Kafka | 0 | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic, no row written by this story; inbox dedupe by cloud event id |
| Temporal | `TreatmentWorkflow` and 3 activities on `rwb-treatment` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; no Schedule; retry policy of the kit |
| Nexus | 0 | 1 operation `calculateRestructurePlan` into `ace-collection` | Synchronous, 2 s budget, faked, never called live in a test |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `affordability` and `workflow`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`, and the Nexus client to namespace `ace-collection` (DP-13; §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record write of the step: the result, the plan terms and the record commit together or not at all. DP-13 fixes the base this story adds no path to, since its answer is read through the sibling story. DP-19 is how the officer sees the result on SCR-14 and SCR-15.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AffordabilityBranch` | Workflow | The branch of `TreatmentWorkflow` that reacts to `AFFORDABILITY_REQUIRED` and to `AFFORDABILITY_ANSWERED`, reports the stage outcome and waits |
| `EvaluateRules` | Activity | Runs the RESTRUCTURE package in force and returns the rule ID and the action |
| `calculateAffordability` | Activity | Assembles the request, calls the Nexus operation inside the 2 s budget, maps the answer or the failure |
| `AceCalculatorNexusClient` | Client | The one Nexus binding: namespace `ace-collection`, operation `calculateRestructurePlan`, request and answer of RWB-S2-E3005-CON |
| `AffordabilityResultRepository` | Repository | Writes the result against the treatment row in `rwb_treatment`, without a band column |
| `TreatmentRepository` | Repository | Reads the treatment terms and writes `installment_amount` and `installments` |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report for the parent and the officer message of the warning path |
| `Migrations` | Migration | No new table for the result fields is written until the contract freeze fixes them; the treatment and `decision_record` tables are already on the sequence |

**Database.** The `treatment` row gains no column: the result and the plan terms live in the columns TSD S2 T3.1 already gives (DF-TRT-009, DF-TRT-031) and in the element of RWB-S2-E3005-CON, whose field IDs are not yet allocated (GAP-1875). `decision_record` is the library object of DP-03. No view of ACE is read and no copy of the calculator's bands is stored.

**Configuration and reference data.** The operation name, the namespace, the 2 s budget and the retry numbers are configuration of the Nexus client and are the working read of ASM-3071 until the ACE Common owner confirms them. The rule package version is data, not configuration, and is read from the package in force. The capability area "Treatment and offer" and the rights C, R and U are the access data of P4 and are read through the guard library (ASM-3064).

**Build steps**

1. The branch of `TreatmentWorkflow` on `rwb-treatment`, its input record, its signal names and its stage report (AC2, AC3).
2. `EvaluateRules` against the package fake, with R-RES-06 and R-RES-07 as rule rows and the `NoPackageInForce` answer (AC2, AC3).
3. `calculateAffordability` and the Nexus client against the calculator fake, with the 2 s budget and the request and answer of RWB-S2-E3005-CON (AC1).
4. `AffordabilityResultRepository` and the plan terms on the treatment row (AC1).
5. `RecordAndApply` with the decision record in the same transaction, and the rollback path of MSG-P7-003 (AC4).
6. The failure path: the stage stays in `AFFORDABILITY_IN_ACE`, nothing is written, MSG-GEN-006 (Section 5, X1).
7. The stale-input guard and MSG-S2-002 (Section 5, X7).
8. Tests for AC1 to AC4 against the fakes, and the component test of the refusal path.

**Feature flag.** `rwb.treatment.affordability-nexus`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the calculator faked, the result and the plan terms appear on the treatment, the record is written in the same transaction and rolls back with the action, the timeout path leaves the stage in `AFFORDABILITY_IN_ACE` with MSG-GEN-006, and the officer sees the calculated plan on SCR-14 through the gateway route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-002 | The payoff figure on the case is older than the age the case allows | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-006 | The calculator does not answer, or the package is not in force | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

The five texts are copied unchanged from RWB-E3-005, RWB-PLT-E1027-CON and the platform message set, and this story adds no message ID. MSG-S2-001 and MSG-S2-003 of the legacy validation table belong to the settlement offer and the offer expiry and are raised by the offer stories of this service, not here. MSG-GEN-006 names the system of the failed call, so the timeout of the calculator reads "ACE Common is not available" and a missing package names the rules component. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record shows the calculated plan on the treatment: the plan reference, the installment amount, the installment count, the calculated-at time and the affordability result, with the treatment states Draft, submitted, approved, booked and broken as the offer stories maintain them. SCR-15 Settlement offer shows the same result where a settlement was the treatment and the offer is built from it, with the states Draft, below floor, approved, sent and accepted. Both are reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment and composes the answer (DP-19; Architecture v5 slide 41). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this story fixes what the service records and what the sibling story's read returns. A refusal or a timeout is shown as the message on the treatment screen and raises an incident, never as a silent empty state.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-005-01 | AC1 | End to end | Pre-assess affordability through ACE |
| TC-E3-005-02 | AC2 | End to end | Rule R-RES-06 |
| TC-E3-005-03 | AC3 | End to end | Rule R-RES-07 |
| TC-E3-005-04 | AC4 | End to end | Not recorded |
| TC-E3-005-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-005-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. The calculator, element, decision-record, case-status and rule-package fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID. The `-ITG` copies of these cases belong to the wave 2 integration harness (RWB-ITG-W2) and are not listed here. The contract's own tests are TC-S2-E3005-CON-01 to -05 and are owned by RWB-S2-E3005-CON.

### 17. Guardrails

- No value that a business person may change is written in code: the rule IDs, the two states, the condition texts, the two-working-day timer and the message texts are data rows, reference data or the package in force, never constants (BR-S2-005; BR7).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the treatment ID, codes, amounts and the rule version only, and the fixture is synthetic.
- No read of another service's tables and no case table here: the case status arrives on the case signal and the case record is rwb-case's (DP-01; ASM-3062).
- No copy of ACE data: the calculator is called through the one Nexus operation and nothing it holds is copied into `rwb_treatment` — no band, no score and no threshold (BR5; DP-01).
- ACE data only through the owner's contract or the `v_ace_*` views; this story reads neither, because the plan inputs arrive on the case and the calculator answers the rest.
- No live calculator in any test or build: the fake is the only endpoint, so a red test never depends on the ACE Common estate.
- No business value in the record or the report: the `DecisionRecord` carries the rule ID, the rule version, the final call and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule, so a replay can never move a case twice (BR3).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Business Requirements Program, section 5.9 | FEAT-TRT-05 | 07 Route, settle and claim | R-RES-06; R-RES-07 | TC-E3-005-01 to TC-E3-005-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3005-CON | Contract | H: declares the `AffordabilityResult` element, the Nexus binding, the 2 s budget, the failure answer and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library this story writes through, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-14 and SCR-15 show the result |
| RWB-S2-E3001-APP | App development | Sibling: the treatment record and the treatment read that show the result; the create and read operations are its own |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP | App development | Siblings: the settlement offer and the below-floor approval, which use the same result where the treatment is a settlement |
| RWB-S2-E3004-APP | App development | Sibling: the offer build and the plan installment range, which consume the calculated plan this step records |
| P3 rwb-case | Service | The case, its status and the parent `CaseWorkflow`; R-RES-06 and R-RES-07 apply there, and the signal reaches this stage |
| P7 rwb-decision | Service | The RESTRUCTURE package, its version and the central ledger; EV-30 is consumed here |
| ACE Common restructure calculator | External capability, existing | The one Nexus operation; owned by the ACE Common owner, not a story of this plan |
| RWB-ITG-W2 | Integration | I: the cross-service proof of this legacy key against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published contract of the affordability element, the Nexus binding, the budget, the failure answer and the fakes: RWB-S2-E3005-CON.
- The treatment record, its create operation, its read operation and its own states: RWB-S2-E3001-APP; the published read is what shows this result.
- The settlement offer, its range and the below-floor approval: RWB-S2-E3002-APP and RWB-S2-E3003-APP.
- The offer build, the plan installment range and the two events `TreatmentApproved` and `TreatmentClosed`: RWB-S2-E3004-APP.
- The case, its status, the status column of R-RES-06 and R-RES-07, and the parent `CaseWorkflow`: rwb-case (P3), reached only on the forwarded case signal (ASM-3062).
- The rule authoring, the four-eyes approval, the effective date, the rollback and the central ledger: rwb-decision (P7) and its own stories; this story consumes the package and the version.
- The ACE Common restructure calculator itself — its operation shape, its calculations, its availability and its namespace: the ACE Common owner and the platform workflow owner (ASM-3071; GAP-1875).
- The screens SCR-14 and SCR-15, their field lists and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The access rule, the roles and the masking: P4 rwb-access and the guard library; this story declares the capability area and the right only (ASM-3064).
- The real cross-service proof of the Nexus call, the case signal and the record write against the live owners: RWB-ITG-W2, which also owns the `-ITG` copies of the legacy cases.

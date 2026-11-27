# RWB-S3-E4019-APP Close the case when a guarantee clears the debt

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-019 split out for rwb-guarantee. The close leaves the monolith's method of `GuaranteesAndGuarantorsService` and becomes the close branch of `GuaranteeClaimWorkflow` on this service's own task queue; the account balance and the guarantee payments are read at the ACE batch date from this service's own SELECT-only `recovery.v_ace_account` and `recovery.v_ace_payment` views and are never copied (DP-05); the claim outcome and the closing position are written against `guarantee_claim` with a local decision record in the same transaction (DP-03); the case status — `RESIDUAL_TO_ROUTE` or `GUARANTEE_CLOSED` — is applied by rwb-case from the stage report and never written here; the four legacy criteria this story owns are copied word for word with their origin tag; the closed state is read on SCR-17 through the gateway-bff composite route (DP-19); the two legacy operations of TSD S3 T-A.1 are re-based to `/api/recovery/guarantee/v1` (DP-13) and the claim result rides the claim contract of this service. No source gives the guaranteed share or the balance after it a field or a governed row (GAP-2731; ASM-4537), gives `LOV-CLAIM-STATUS` a closed value (GAP-2732; ASM-4538), gives the subrogation position a record (GAP-2733; ASM-4539), names the trigger of the feature (GAP-2734; ASM-4540) or resolves which login reads the ACE views (GAP-2735; ASM-4541). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4019-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S3-E4019-APP-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4019-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-S3-E4019-CON (not yet published) |
| Contract version | 5.0.0 (rwb-guarantee.yaml, Recovery Workbench API Specification v5; REST base /api/recovery/guarantee/v1) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **guarantee officer (RW-GUARANT)**, I want **the Workbench to close the guarantee and the case when a guarantee payment clears the balance in full — the balance after the guaranteed share read at the ACE batch date, the claim outcome and the closing position written on the claim with the rule version that decided, and the case closed or returned to the route decision on the stage report** — so that **no guarantee claim misses its deadline and a case whose debt a guarantee has cleared is not left open while the deadline goes on being tracked by hand**.

This is the application slice of legacy RWB-E4-019. It owns:

- the four legacy acceptance criteria this story is given (AC1 to AC4), copied verbatim with their origin tag, and the rules, data rows and messages they carry;
- the close branch of `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery`: the step that evaluates the GUARANTEE route set in force (32 rules over 17 states, TSD S3 T4), records the answer and reports the stage outcome to the parent `CaseWorkflow` (context pack slides 5 and 13);
- the close activity: the account balance and the guarantee payments read at the ACE batch date from this service's own SELECT-only views `recovery.v_ace_account`, `recovery.v_ace_payment` and `recovery.v_ace_batch_status`, with no copy kept (DP-05);
- the balance after the guaranteed share: composed per calculation from the read balance and the guaranteed share the answer names, tested against zero, never held as a column and never written as a constant (GAP-2731; ASM-4537);
- the three answers of the route set: R-GUA-19 (close the guarantee and return the full balance to the route decision, to `RESIDUAL_TO_ROUTE`), R-GUA-26 (close the guarantee and close the case, to `GUARANTEE_CLOSED`) and R-GUA-27 (return the full balance to the route decision and close the guarantee on a recorded loss, to `RESIDUAL_TO_ROUTE`), with R-GUA-25 left to the sibling story at the same state;
- the claim result: `guarantee_claim.status` within its published list (LOV-CLAIM-STATUS, DF-TRT-022), `paid_amount` (DF-TRT-021) and the `GuaranteeClose` element of RWB-S3-E4019-CON, written against the claim row in `rwb_guarantee` with the local decision record of the step in the same transaction (DP-03; RWB-PLT-E1027-CON);
- the stage report to the parent: the outcome, the reason code of the answered row and the 5 working day owner task of R-GUA-27, ordered here and created by rwb-case, because the case status, the case tasks and the case timers are rwb-case's;
- the refusal and failure paths: no record, nothing changes and MSG-P7-003; a stale data product blocks with MSG-P1-001; a missing value is named with MSG-GEN-001; a role without the right is refused with MSG-P4-002.

It does not own: the published element, the read rule of the two ACE views, the close rule set, the versioning rule and the fakes, which are RWB-S3-E4019-CON; the claim representation, its create and result operations and its states, which are the claim stories of this service (RWB-S3-E4015-APP and RWB-S3-E4015-CON); the preparation of the claim, its submission and its tracking, which are RWB-S3-E4013-APP, RWB-S3-E4014-APP and RWB-S3-E4015-APP; the subrogation position entered by R-GUA-23 and R-GUA-24 and the residual of R-GUA-25, which are RWB-S3-E4016-APP; the guarantor notices, which are RWB-S3-E4017-APP; the negotiation with a guarantor, which is RWB-S3-E4018-APP; the insurance claim, which is RWB-S3-E4020-APP; the case, its status, its tasks, its timers and the parent `CaseWorkflow`, which are rwb-case's; the posting and the booking in ALS core and GL, which are rwb-payment's and the core bank's; the ACE views and their content, which are ACE's; the rule package, its approval and the central ledger, which are P7 rwb-decision's; the screen and its composite route, which are the platform edge story's and the screen owner's under DP-19.

### 2. Business rationale

In the monolith the close was a method of `GuaranteesAndGuarantorsService`: it read the balance and the payments live from the `recovery` schema, read the GUARANTEE rows from `rule_row`, wrote the claim status into `guarantee_claim` and the decision into `decision_log_entry`, all in one process (TSD S3 T1 and T2). Two things followed. The close could only be exercised with a live ACE balance, and the claim's result, the position and the case status were written by the same code, so no reader could tell which of them was authoritative.

D-RCV-60 changes the source of each input and nothing else. The balance and the payment stay in ACE and are read at the ACE batch date through this service's own SELECT-only views, with the product's date on the answer (DP-05; D-RCV-35, ADR-010). The closing decision is a governed row of the GUARANTEE route set, read with the version that decided, so a change of policy is a rule release and not a build (R-GUA-19, R-GUA-26, R-GUA-27). The decision is recorded locally in the same transaction as the claim result, so a close that cannot be recorded does not happen (DP-03; ADR-022). And the case is closed or returned by rwb-case from the report, because the case is the case service's after the split (DP-01).

The step is a branch of the stage workflow the service already owns: one child workflow per case on the owner's queue, `rwb-guarantee`, with the rules evaluated from the package in force (context pack slides 5 and 13; Architecture v5 slide 18). What it does not change is the officer's work or the deadline: the guarantees that are not claimed in time are still lost claims, and the metric of the feature is unchanged — "claims filed inside the deadline, 100 percent, decision log and Workbench records, monthly" (FSD S3 A2.7.1).

Delivery is EP04 in wave 3 on release 28 February 2027 (tentative). REQ-S3-003 of FSD S3 names this feature — "a guarantee payment that clears the balance closes the case and records the subrogation position" — and is the requirement this story and its contract trace to; TSD S3 T8 maps the same set of IDs to FEAT-GUA-01, so the trace carries both (Section 18).

### 3. Preconditions

- RWB-S3-E4019-CON is published: the `GuaranteeClose` element, its required and optional fields, the read rule of the three ACE views, the close rule set, the stage report, the messages and the fakes. The build starts against the Draft baseline, as every CON story of this run publishes on Day 1 at status Draft (realignment v1).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` propagation, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-17 from the case read and this service's claim read (DP-19).
- The `rwb_guarantee` schema and its login exist from the platform database story, the `guarantee_claim` table is on the per-service Flyway sequence with DF-TRT-015 to DF-TRT-022 of TSD S3 T3.1, and `decision_record` is created as the platform library object in the same schema (DP-01; DP-15).
- SELECT on `recovery.v_ace_account`, `recovery.v_ace_payment` and `recovery.v_ace_batch_status` is granted to this service's login and on no other ACE object. Architecture v5 slide 8 says the `recovery.v_ace_*` views are read only by rwb-source-data while DP-05 allows the service's own SELECT-only views; the Work Package records no contract dependency on P1, so the grant is the working read of ASM-4541, and the conflict is GAP-2735.
- The claim exists in `rwb_guarantee` with `claim_type`, `claim_deadline`, `claimed_amount` and `status` (DF-TRT-017 to DF-TRT-022), and the case is in `CLAIM_REJECTED`, `SUBROGATION_POSITION` or `DEADLINE_MISSED` on the case signal with the claim id and the payment reference.
- The GUARANTEE route set in force is in this service's rule cache at the version the answer names; its rules, conditions and to states are rule rows, not code (BR-S3-007).
- No approval stop: the FSD S3 v3 and TSD S3 v2 documents carry status "In review" and nothing in this story needs a human sign-off to start on Day 1 (ASM-4542).

### 4. Flow

1. rwb-case: the parent `CaseWorkflow` forwards the case signal to the `GuaranteeClaimWorkflow` child of the case when the claim result of the case arrives, carrying the case status, the claim id and the payment reference (R-GUA-19, R-GUA-26 and R-GUA-27 from state).
2. `GuaranteeClaimWorkflow`: the close branch opens the step, calls `EvaluateRules` and the GUARANTEE route set in force returns the row that applies, with the rule ID and the package version (R-GUA-19 for `RESUBMISSION_NOT_POSSIBLE`, R-GUA-26 for `BALANCE_SATISFIED`, R-GUA-27 for `LOSS_RECORDED`). The lists and parameters it reads are the GUARANTEE route set in force and LOV-CLAIM-STATUS of TSD S3 T3.2, read under the reference-data contract of DP-06 and DP-07; no parameter key is named in the source documents (DOR-RWB-S3-E4019-APP-20).
3. `closeGuarantee` activity, step one: reads `recovery.v_ace_batch_status` and compares the data product date with today's business date; a product older than today's ACE batch stops the step with MSG-P1-001 naming the product and its date (VR-S3-007-1).
4. Step two: reads the balance of the accounts of the case from `recovery.v_ace_account` — `account_key`, `account_code`, `account_status`, `contract_no`, `product_category_efs`, `total_balance` and the rest of DF-ACE-001 to DF-ACE-042 — and the guarantee payments from `recovery.v_ace_payment` — `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and the rest of DF-ACE-043 to DF-ACE-054 — read only, one hop, inside the 2 s budget, keeping no copy (DP-05).
5. Step three: composes the balance after the guaranteed share from the balance read and the guaranteed share the answer names, and tests it against zero (GAP-2731; ASM-4537). Zero answers R-GUA-26; a balance above zero answers R-GUA-25, which is the sibling's and moves nothing here.
6. Step four: composes the claim result — `status` within LOV-CLAIM-STATUS and `paid_amount` where the payment is recorded — and builds the `GuaranteeClose` element of RWB-S3-E4019-CON (GAP-2732; ASM-4538).
7. `RecordAndApply` activity, one transaction: the claim result and the element are written against the claim row in `rwb_guarantee`, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with the rule ID, the rule version and the balance tested, and the stage report goes to the parent (DP-03).
8. The stage reports `GUARANTEE_CLOSED` for R-GUA-26, or `RESIDUAL_TO_ROUTE` with the full balance for R-GUA-19 and R-GUA-27 and the 5 working day owner task of R-GUA-27; the parent applies the case status, closes the case or returns it to the route decision, and raises the case task and its timer (R-GUA-19; R-GUA-26; R-GUA-27).
9. The officer reads the claim result, the position and the case status on SCR-17 through the gateway-bff composite route and through the claim read of this service, and works the returned case where the residual went back to the route decision (DP-19). SCR-17 has four states: empty, loading, error and no access; their texts are Not specified in the source documents (DOR-RWB-S3-E4019-APP-10; CG-ALL-8944).
10. The route decision runs again on a case returned at R-GUA-19 or R-GUA-27, which is S1's work and not this step's; the case closed at R-GUA-26 takes no further route.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A data product the step reads is older than today's ACE batch | The step blocks, names the product and its date, and decides nothing | MSG-P1-001 | AC1; VR-S3-007-1 |
| X2 | The balance after the guaranteed share is above zero on the R-GUA-26 path | The step answers R-GUA-25 and moves nothing; the residual is the sibling story's at the same state | None | AC5 |
| X3 | The rejection reason is curable and the deadline has not passed | R-GUA-19 does not apply; the resubmission path of the claim story runs and the claim stays open | None | AC2 |
| X4 | The decision record cannot be written | The transaction rolls back: no claim result, no element, no stage report; the caller sees MSG-P7-003 and an incident is raised | MSG-P7-003 | AC4 |
| X5 | The record is refused for a missing or invalid field | Nothing is written, the field is named, the claim stays where it was | MSG-P7-009 | AC6 |
| X6 | A role without the right tries to re-run the step or read its result | 403 from the access guard and nothing changes; the step itself runs unattended under the service identity | MSG-P4-002 | AC7 |
| X7 | A second case signal arrives while the branch is running | The inbox dedupes by the cloud event id of the case signal and the activity is idempotent on the claim, the rule version and the batch date, so no second result is written | None | AC8 |
| X8 | An ACE view is not reachable | The activity is retried by the workflow's retry policy; when the attempts are exhausted the stage stays where it was and the caller sees MSG-GEN-006 naming the system | MSG-GEN-006 | AC1 |

X1, X4 and the missing-value path are the legacy paths of RWB-E4-019 carried onto the split, with X6 the access path the legacy permission table already names. X2, X3 and X5 are the routing logic's other answers, the platform library's refusal, and X7, X8 the inbox dedupe and the availability path of the ACE read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S3-E4019-CON and its fakes, the decision-record library and the gateway route; the three views are replaced by a fixture and the rule package by a fake, so no deployment of P1, P7, ACE or rwb-case is needed |
| Negotiable | The activity name, the shape of the stage report and the retry numbers are this story's choice; the element, the rules, the conditions, the to states and the messages are fixed |
| Valuable | A guarantee that clears the debt closes the claim and the case the same day, with the position and the version of the policy that decided, and the deadline stops being tracked by hand |
| Estimable | One workflow branch, one close activity, three view reads, one claim result, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic claim, an ACE fixture and a rule-package fake, plus one component test of the stale-input, the refusal and the unreachable-view paths |

### 7. Acceptance criteria

```gherkin
Feature: Close the case when a guarantee clears the debt

  Background:
    Given guarantee claim "GCL-SYN-0419" of case "RW-2026-000419" is a claim in schema rwb_guarantee
    Given the GUARANTEE rule package in force is version "GUA-2026.11"

  Scenario: AC1 Close the case when a guarantee clears the debt (legacy RWB-E4-019 AC1)
    Given the rwb-case contract mock returns the case signal with the claim in state CLAIM_SUBMITTED and the balance after the guaranteed share at zero
    Given the rwb-source-data contract fake serves the ACE data and the rule version this feature needs are in place
    When its trigger arrives
    Then closes the case and records the position when a guarantee payment clears the balance in full
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-19 (legacy RWB-E4-019 AC2)
    Given the rwb-case contract mock returns the case in state CLAIM_REJECTED with claim_deadline passed
    Given a case in state CLAIM_REJECTED
    When resubmission not possible
    Then close the guarantee and return the full balance to the route decision
    Then the case moves to RESIDUAL_TO_ROUTE

  Scenario: AC3 Rule R-GUA-26 (legacy RWB-E4-019 AC3)
    Given the rwb-case contract mock returns the case in state SUBROGATION_POSITION with the balance after the guaranteed share at zero
    Given a case in state SUBROGATION_POSITION
    When balance satisfied
    Then close the guarantee and close the case
    Then the case moves to GUARANTEE_CLOSED

  Scenario: AC4 Not recorded (legacy RWB-E4-019 AC4)
    Given the decision-record library mock returns the failure MSG-P7-003
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 The balance above zero after the share is not closed (new, D-RCV-60)
    Given the rwb-source-data contract fake returns a balance above zero after the guaranteed share
    Given a case in state SUBROGATION_POSITION
    When the step tests the balance after the guaranteed share
    Then the step answers R-GUA-25 and moves nothing

  Scenario: AC6 A decision record refused for a missing field is not written (new, D-RCV-60)
    Given the decision-record writer fake refuses the record with MSG-P7-009 and the field
    When the claim result is recorded
    Then nothing is written, the field is named and the claim stays where it was

  Scenario: AC7 A role without the right is refused (new, D-RCV-60)
    Given a user whose role does not include the right to re-run the step or read its result
    When the user re-runs the step or reads its result
    Then the access guard returns 403 with MSG-P4-002 and nothing changes

  Scenario: AC8 A second case signal with the same cloud event id is deduped (new, D-RCV-60)
    Given the branch is running on the case signal
    When a second case signal with the same cloud event id arrives
    Then the inbox dedupes it and no second result is written

  Scenario: AC9 Rule IDs, conditions and messages come from rule rows (new, D-RCV-60)
    Given the rule-package fake serves a rule package version
    When the step runs
    Then the rule IDs, conditions, to states and messages are read from rule rows and no value a business person may change is written in code

  Scenario: AC10 The balance after the share is composed, not stored (new, D-RCV-60)
    Given the rwb-source-data contract fake returns the balance and the guaranteed share
    When the step composes the balance after the guaranteed share
    Then the balance is computed per call and no balance, share or position column is written to rwb_guarantee

  Scenario: AC11 The close is one of three answers of the route set (new, D-RCV-60)
    Given the rule-package fake serves a rule package version with R-GUA-19, R-GUA-25, R-GUA-26 and R-GUA-27
    When the step tests the balance against zero
    Then R-GUA-19 and R-GUA-27 return the full balance to the route decision and R-GUA-26 closes the guarantee and the case

  Scenario: AC12 The balance and payments are read only, one hop, inside the budget (new, D-RCV-60)
    Given the rwb-source-data contract fake serves the balance and the payments at the ACE batch date
    When the step reads them
    Then the reads are read only, one hop and inside the 2 s budget, and nothing is copied into rwb_guarantee

  Scenario: AC13 A stale data product blocks the step (new, D-RCV-60)
    Given the rwb-source-data contract fake serves a product dated yesterday
    When the step runs
    Then the step blocks, names the product and its date with MSG-P1-001 and decides nothing

  Scenario: AC14 The claim result, the element and the decision record are written in one transaction (new, D-RCV-60)
    Given the decision-record writer fake accepts the record with its chain sequence
    When the step records the result
    Then the claim result, the element and the decision record are committed together

  Scenario: AC15 The case status and the case task are never written here (new, D-RCV-60)
    Given the case-signal fake delivers the case signal
    When the stage reports the outcome
    Then the stage reports the outcome, the reason and the task due date, and the parent applies the case status, the closure, the task and the timer

  Scenario: AC16 The claim status stays inside its published list (new, D-RCV-60)
    Given LOV-CLAIM-STATUS of TSD S3 T3.2 is the published list
    When the close is recorded
    Then the status stays within PREPARING, FILED, DEFECT, PAID and REJECTED and the closing basis is carried in the element

  Scenario: AC17 An ACE read that does not answer or answers after the 2 s budget is retried and then stops the step (new, D-RCV-60)
    Given the rwb-source-data contract fake does not answer the ACE read or answers after the 2 s budget
    When the activity runs
    Then the workflow retry policy retries the activity and, when the attempts are exhausted, the stage stays where it was and MSG-GEN-006 names the system
```

**Target reading.** Every legacy line above keeps its wording; what changes is where it runs, which service holds each fact and how it is reached. "Closes the case and records the position when a guarantee payment clears the balance in full" is no longer a method of `GuaranteesAndGuarantorsService` reading the `recovery` schema and `rule_row`: the balance after the guaranteed share is composed by the `closeGuarantee` activity of `GuaranteeClaimWorkflow` on queue `rwb-guarantee` from the balance read at the ACE batch date through `recovery.v_ace_account` (DF-ACE-001 to DF-ACE-042) and the payments read through `recovery.v_ace_payment` (DF-ACE-043 to DF-ACE-054), and the test is the condition of the answered row (DP-05).

"Records the position" is the `GuaranteeClose` element of RWB-S3-E4019-CON recorded against the claim row, with the closing basis and the balance tested; the position as a subrogation record belongs to RWB-S3-E4016-APP and has no field of its own yet (GAP-2733; ASM-4539). "Closes the case" and "the case moves to RESIDUAL_TO_ROUTE / GUARANTEE_CLOSED" are the stage report to the parent and the status rwb-case applies from it: `guarantee_claim` has no closed value in LOV-CLAIM-STATUS, so the close of the guarantee is recorded as the claim result and the close of the case is the case's own status (GAP-2732; ASM-4538). "Writes the result to the decision log with the rule version" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction as the claim result, with MSG-P7-003 on failure (DP-03); `decision_log_entry` stays P7's and is never written here. "Its trigger arrives" is the case signal the parent `CaseWorkflow` forwards, because the FSD names "a completed ACE batch, an event or a timer" and no source names which one (GAP-2734; ASM-4540).



### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No value a business person may change is written in code: the rule IDs, the conditions, the to states, the rights and the messages are rule rows, governed rows or package content | BR-S3-007 of FSD A2.7.3.1 |
| BR2 | The balance after the guaranteed share is composed per calculation from the balance read at the batch date and the guaranteed share the answered row names; there is no balance, share or position column in `rwb_guarantee` | GAP-2731; ASM-4537 |
| BR3 | The close is one of three answers of the GUARANTEE route set in force: R-GUA-19 and R-GUA-27 return the full balance to the route decision and R-GUA-26 closes the guarantee and the case; R-GUA-25 keeps the residual route open and is not this step's | R-GUA-19; R-GUA-25; R-GUA-26; R-GUA-27 |
| BR4 | The balance and the payments are read only, at the ACE batch date, from this service's own SELECT-only views, one hop inside the 2 s budget, and nothing is copied into `rwb_guarantee` | DP-05; VR-S3-007-1; D-RCV-35; ADR-010 |
| BR5 | A data product older than today's ACE batch blocks the step and is named with its date; nothing is decided on a stale input | VR-S3-007-1; MSG-P1-001 |
| BR6 | The claim result, the element and the decision record are written in one transaction; if the record cannot be written nothing changes and MSG-P7-003 is shown | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR7 | The case status, the case closure, the case task and the case timer are never this service's: the stage reports the outcome, the reason and the task due date and the parent applies the rule | DP-01; ASM-4538 |
| BR8 | The claim status stays inside its published list, PREPARING, FILED, DEFECT, PAID and REJECTED; the close adds no value to LOV-CLAIM-STATUS and the closing basis is carried in the element | LOV-CLAIM-STATUS of TSD S3 T3.2; GAP-2732 |

**Where each rule lives in the target.** BR1 is why the rules and the rights are inputs of the activity; BR2 is the composition and the reason the schema gains no column; BR3 is the three condition tests of the answered row; BR4 is the SELECT-only grant and the as-at date on the element; BR5 is the guard before the comparison; BR6 is the `MANDATORY` propagation of the library write; BR7 is the boundary to rwb-case; BR8 is the reason the close is an element and a case status rather than a new claim status.

### 9. State transitions

None of the case statuses below is this service's; the table shows what the stage reports and what it never writes, so a reader can see the boundary of this story.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-GUA-19 | `CLAIM_REJECTED` | `RESUBMISSION_NOT_POSSIBLE` | the reason is not curable, or `claim_deadline` has passed | Writes the claim result and the element, reports the full balance | `RESIDUAL_TO_ROUTE` |
| R-GUA-26 | `SUBROGATION_POSITION` | `BALANCE_SATISFIED` | the balance after the guaranteed share is zero | Writes the claim result and the element, reports the closure | `GUARANTEE_CLOSED` |
| R-GUA-27 | `DEADLINE_MISSED` | `LOSS_RECORDED` | the loss amount and the reason are recorded | Writes the claim result and the element, reports the balance and the 5 working day owner task | `RESIDUAL_TO_ROUTE` |
| R-GUA-25 (read only) | `SUBROGATION_POSITION` | `RESIDUAL_REMAINS` | the balance after the guaranteed share is greater than zero | Answers "residual remains" and moves nothing; the return is the sibling story's | `RESIDUAL_TO_ROUTE` |
| R-GUA-22 (read only) | `CLAIM_SUBMITTED` | `FULL_PAYMENT_RECEIVED` | `claim_amount_paid = guaranteed_amount` | Nothing; it is the entry the payment side takes and it opens the subrogation position | `CLAIM_PAID` |

The states of this story's own object are the claim's: `status` takes `PREPARING`, `FILED`, `DEFECT`, `PAID` or `REJECTED` (LOV-CLAIM-STATUS) and the close writes the value the answered row leaves in force with `paid_amount` where the payment is recorded. `RESIDUAL_TO_ROUTE` and `GUARANTEE_CLOSED` are rwb-case case statuses and are not values of LOV-CLAIM-STATUS. The `GuaranteeClose` element has no state machine: it is written once per closed claim and is not rewritten, because a second close is a second case signal and the inbox dedupes it. The `GuaranteeClaimWorkflow` execution has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the reads and the write are activities and not workflow-local computation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the close activity, the reads, the claim result and the tests |
| RW-GUARANT, guarantee officer | Holds rights C, R and U on the capability area "Treatment and offer"; reads the claim result and the position on SCR-17; works a claim the deadline has put at risk |
| RW-CASEOWN, case owner | Owns the answered state; works the case returned at R-GUA-19 and R-GUA-27 and the 5 working day task of R-GUA-27; holds rights C, R and U |
| RW-RESTRUCT, restructuring officer (FCR); RW-SPECIAL, hardship and vulnerability specialist | Hold rights C, R and U and see the closed claim and the returned case |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the read-only roles of TSD S3 T6.1 | Right R only: they read the result and cannot trigger a re-run |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity and reports to the parent |
| rwb-case (P3) | Owns the case, its status, its closure, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Owns the rule package, the GUARANTEE rows, their approval, their effective date and the central ledger |
| P8 rwb-payment and ALS core and GL | Own the posting and the booking of the guarantee payment; this stage reads the result and never posts |
| ACE and its DBA | Own the `recovery.v_ace_*` views, their grants and the batch that dates them |
| The platform workflow and data owners | Own the task queue, the namespace, the ACE PostgreSQL grants and the decision-record library |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right U, C or R on each entry point. No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the claim ID, account keys, dates, amounts, a basis code and versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim | id | Write (the row the result and the element are recorded against) |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read (the R-GUA-19 condition) |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read (the share basis of the answer) |
| DF-TRT-020 | guarantee_claim | filed_at | Read |
| DF-TRT-021 | guarantee_claim | paid_amount | Write |
| DF-TRT-022 | guarantee_claim | status | Write (within LOV-CLAIM-STATUS) |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Read only |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Read only |
| Not specified in the source documents (CG-ALL-8939) | v_ace_batch_status | the product date of the ACE batch | Read only |
| DF-DEC-002 to DF-DEC-016 | decision_record | the seven field groups | Write |
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Read on the case signal only |
| DF-WRK-027 to DF-WRK-036 | timer | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Read on the case signal only; never written |

`guarantee_claim` and `decision_record` are this service's own objects in `rwb_guarantee`, written through its own repository and login (DP-01). The account and payment columns are read through the read-only views at the batch date and are not copied into any column of this service: there is no balance field, no share field and no position field in `rwb_guarantee`, and the element of RWB-S3-E4019-CON is the only shape the evidence takes. The case and timer rows are rwb-case's and arrive on the case signal; they are never read from a table and never written (BR7; ASM-4538). The guaranteed share and the balance after it have no field identifier and no column in the Logical Data Model (GAP-2731; ASM-4537).

### 12. Contract

#### 12.1 REST operations provided

None of its own. The service publishes the two operations of TSD S3 T-A.1 on base `/api/recovery/guarantee/v1` (DP-13): `POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` (API-S3-001, right C) opens a claim and belongs to the claim story that creates it, and `PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}` (API-S3-002, right U) records the claim result, which is the operation the close lands on. Its representation, its required fields, its errors and its idempotency are declared by the claim contract of this service and by RWB-S3-E4019-CON for the `GuaranteeClose` component, and are not restated here. The step itself is signal-driven and unattended; it has no command of its own.

#### 12.2 REST operations consumed

None. The case status, the claim id and the payment reference arrive on the case signal the parent `CaseWorkflow` forwards, not on a REST read (DP-11 is not applied: there is no in-process call left to replace). The balance and the payment evidence are SQL reads of the views in 12.7, not REST reads, and the rule rows arrive with the package in force. No source publishes an operation for this step and none is invented (GAP-2734; ASM-4540).

#### 12.3 Events published

None. The service's topic is `rwb.guarantee.events.v1` with names `rwb.guarantee.<Event>.v1` and its retry and `.dlt` topics (DP-14), and the ownership rows give S3 no event (TSD S3 T5.3, "None"). The close is delivered as the stage report to the parent `CaseWorkflow`, a Temporal signal inside the case, because a Kafka event would need a name, a payload, an outbox row and the event platform of DP-09, which the plan does not give this legacy key. The report of a closed guarantee reaches reporting through the case, whose status the parent applies; if an S3 event is wanted it is a new name and a new dependency, not this story's (ASM-4538).

#### 12.4 Events consumed

None of its own. The service's subscriptions are the template's inbox and the rule loader; the connection matrix of Architecture v5 slide 13 shows S3 listening to P6 and P8 events, calling P7 by Temporal activity, and publishing nothing that P9 reads by name in this story. The payment that clears the balance reaches the step on the case signal the parent forwards, not on a subscription this story adds. No event is named here that the service does not own (GAP-2734).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` (the close branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case ID, the claim ID, the case status on the signal and the payment reference. Output: the stage report with the outcome, the reason code and the rule version |
| `EvaluateRules` | Activity of the template | `rwb-guarantee` | The GUARANTEE route set in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `closeGuarantee` | Activity | `rwb-guarantee` | The three view reads at the batch date, the claim row and the guaranteed share in; the `GuaranteeClose` of RWB-S3-E4019-CON out; retried by the workflow, with the stale guard non-retryable |
| `RecordAndApply` | Activity of the template | `rwb-guarantee` | The claim result, the element and the decision record in one transaction, then the stage report |

The workflow name is fixed by the ownership rows and the context pack; the three activity names are this story's choice. The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts; `NoPackageInForce` and a stale product non-retryable). A replay never re-reads the views: the answer is recorded by the activity and read from history, and the branch is idempotent on the claim, the rule version and the batch date, so a repeated signal writes no second result.

#### 12.6 Schedules

None. The step is signal-driven from the case and owns no Temporal Schedule and no legacy Quartz job; the ownership rows give S3 no job and the legacy scheduler is retired. The claim deadline that the feature is measured on is a case timer of rwb-case, driven by the workflow platform and created by the case, not a schedule of this service.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 rwb-guarantee | Created by the per-service Flyway sequence and written here for `status`, `paid_amount` and the element; DF-TRT-015 to DF-TRT-022 of TSD S3 T3.1, with no balance, share or position column |
| `decision_record` | `rwb_guarantee` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). Three `recovery.v_ace_*` views of the ACE database are read, `v_ace_account`, `v_ace_payment` and `v_ace_batch_status`, read only at the ACE batch date and with no copy kept (ASM-4541); the case table, the task and timer rows of rwb-case, the rule tables of rwb-decision and the posting tables of rwb-payment are never named in SQL.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S3-E4019-CON element fake | The `GuaranteeClose` shape | A complete element; one per missing required field; an element with and without the rule and set versions |
| rwb-source-data contract fake (ACE balance and payment fixture) | `v_ace_account`, `v_ace_payment` and `v_ace_batch_status` | A cleared balance; a balance above zero after the share; a payment inside the batch; a product dated yesterday; an unreachable view |
| Case-signal fake | The signal the parent forwards | `CLAIM_REJECTED` with the deadline passed; `SUBROGATION_POSITION` with a zero balance; `DEADLINE_MISSED` with a recorded loss |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Rule-package fake | The GUARANTEE route set in force | Version `GUA-2026.11` with R-GUA-19, R-GUA-25, R-GUA-26 and R-GUA-27; a set with no matching row; a checksum mismatch |

The balance fixture and the case-signal fake are the Day-1 unblockers: the build and every test run against them, and no test reads a production view or needs a live case.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The step is signal-driven; the result rides the claim representation of API-S3-002 |
| Kafka | 0 | 0 | Own topic with no catalogued event; inbox dedupe by cloud event id |
| Temporal | `GuaranteeClaimWorkflow` and 3 activities on `rwb-guarantee` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; no Schedule |
| SQL view | 0 | 3 (`recovery.v_ace_account`, `recovery.v_ace_payment`, `recovery.v_ace_batch_status`) | Read only, at the batch date, no copy |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, modules `close` and `workflow`, with the published types in `...guarantee.api`. Service base `/api/recovery/guarantee/v1`, schema `rwb_guarantee`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery` (DP-13; context pack).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only views, because the Work Package records no contract dependency on P1 and the grant is the working read of ASM-4541 (GAP-2735). DP-03 is the record of the close, DP-13 the base the claim operations sit on, and DP-19 the path the closed claim is read on.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeCloseBranch` | Workflow | The branch of `GuaranteeClaimWorkflow` that opens the step, reports the outcome and waits |
| `EvaluateRules` | Activity | Runs the GUARANTEE route set in force and returns the rule ID, the action and the next event |
| `closeGuarantee` | Activity | Reads the views, applies the stale guard, composes the balance after the share, builds the element |
| `AceBalanceReader` | Repository | The three read-only view queries; no entity and no cache beyond the request |
| `GuaranteeCloseRepository` | Repository | Writes `status`, `paid_amount` and the element against the claim row |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report with the reason and the task due date, and the officer messages |

**Database.** No new table and no new column: the step writes `guarantee_claim.status` (DF-TRT-022) and `guarantee_claim.paid_amount` (DF-TRT-021) in `rwb_guarantee`, and `decision_record` is the library object of DP-03. A balance, share or position column is deliberately not added; if one must be persisted it becomes a field of the Logical Data Model first (GAP-2731; ASM-4537).

**Configuration and reference data.** The share basis, the conditions and the three rule rows are data of rwb-decision with a version and are read, never configured here. The retry numbers, the activity name and the 2 s budget are configuration of the activity. The capability area "Treatment and offer" and the rights are access data of P4 read through the guard library.

**Build steps**

1. The branch of `GuaranteeClaimWorkflow` on `rwb-guarantee`, its input record and the stage report with the reason.
2. `EvaluateRules` against the package fake, with R-GUA-19, R-GUA-25, R-GUA-26 and R-GUA-27 as rule rows and the `NoPackageInForce` answer.
3. `AceBalanceReader` against the view fixture, with the batch-date test and MSG-P1-001 (AC1, X1).
4. `closeGuarantee` with the balance composition and the zero test (AC1, AC2, AC3).
5. The `GuaranteeClose` element of RWB-S3-E4019-CON and the claim result within LOV-CLAIM-STATUS (AC1, AC3).
6. `RecordAndApply` with the record in the same transaction and the rollback path of MSG-P7-003 (AC4).
7. The missing-value path with MSG-GEN-001, the refusal with MSG-P7-009 and the unreachable-view path with MSG-GEN-006 (X5, X8).
8. Tests for AC1 to AC4 against the fakes, the component tests of X1, X2, X5 and X8, and the replay test of X7.

**Feature flag.** `rwb.guarantee.guarantee-close`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the views and the package faked, the claim shows its result and its element, the record is written in the same transaction and rolls back with the action, the stale product path blocks with MSG-P1-001, and the case is closed or returned to the route decision on the report.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product the step reads is older than today's ACE batch | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | A required value is missing, for example the claim deadline, and the step cannot decide | Enter {field}. |
| MSG-GEN-006 | An ACE view does not answer | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

The texts are copied unchanged from the legacy story, FSD S3 A2.7.3.1 and the platform message set, and this story adds no message ID. MSG-GEN-001 is the required-field rule VR-S3-007-1's neighbour in the legacy validation table and covers a missing claim value; MSG-GEN-006 and MSG-P7-009 are the platform library's answers. Thai text for each message follows decision DL10, which is open and rests on assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 (DOR-RWB-S3-E4019-APP-18).

### 15. Screens and states

SCR-17 Guarantee claim shows the guarantee, the claim deadline, the checklist and the claim result, in the states `Not due`, `due`, `submitted`, `paid` and `refused`. This story makes the end of that life visible: the claim result, the closing basis, the balance tested at its batch date and the case status `GUARANTEE_CLOSED` or `RESIDUAL_TO_ROUTE` are read on the same screen through the gateway-bff composite route, which calls rwb-case and rwb-guarantee and composes the answer (DP-19; Architecture v5 slide 41). The screen field list and the route specification belong to the platform edge story and the screen owner; this story fixes what the service writes and what the claim read returns. A blocked step is shown as its message with the product and its date, never as a closed claim. The empty, loading, error and no-access states of SCR-17 are not in Screen Specifications v1, so they are Not specified in the source documents (CG-ALL-8944).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-019-01 | AC1 | End to end | Close the case when a guarantee clears the debt |
| TC-E4-019-02 | AC2 | End to end | Rule R-GUA-19 |
| TC-E4-019-03 | AC3 | End to end | Rule R-GUA-26 |
| TC-E4-019-04 | AC4 | End to end | Not recorded |
| TC-E4-019-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-019-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |
| TC-E4-019-07 | Operations, events and activities of section 12 | Component | The GuaranteeClose element and the claim contract against the RWB-S3-E4019-CON element fake |
| TC-E4-019-08 | Tables of section 12.7 (ASM-3438) | Component | Only guarantee_claim and decision_record are written; the three ACE views are read at the batch date; no other table is named |
| TC-E4-019-09 | AC5 | Component | A balance above zero after the share answers R-GUA-25 and moves nothing |
| TC-E4-019-10 | AC6 | Component | A refused record with MSG-P7-009 and the field; nothing is written |
| TC-E4-019-11 | AC7 | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-019-12 | AC8 | Component | A second case signal with the same cloud event id is deduped |
| TC-E4-019-13 | AC9 (BR1) | Component | Rule IDs, conditions and messages are read from rule rows |
| TC-E4-019-14 | AC10 (BR2) | Component | The balance is composed per call; no balance, share or position column is written |
| TC-E4-019-15 | AC11 (BR3) | Component | The three condition tests of the answered row |
| TC-E4-019-16 | AC12 (BR4) | Component | Read only, one hop, inside the 2 s budget, nothing copied |
| TC-E4-019-17 | AC13 (BR5) | Component | A product dated yesterday blocks the step with MSG-P1-001 |
| TC-E4-019-18 | AC14 (BR6) | Component | The claim result, the element and the decision record commit together |
| TC-E4-019-19 | AC15 (BR7) | Component | The stage reports the outcome and the parent applies the case status |
| TC-E4-019-20 | AC16 (BR8) | Component | The status stays within LOV-CLAIM-STATUS and the closing basis is in the element |
| TC-E4-019-21 | AC17 | Component | An ACE read that does not answer is retried and then stops the step with MSG-GEN-006 |

The legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy suite's story level is carried as "End to end" and the two exception cases as "Component", as in the other stories of this run. TC-E4-019-05 and TC-E4-019-06 restate the same guard as the legacy suite, so they run once each. The view, case-signal, element, decision-record and rule-package fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases, tab Story test cases, under the same ID. The `-ITG` copies (TC-E4-019-01-ITG to TC-E4-019-06-ITG) belong to the wave 3 integration harness (RWB-ITG-W3) and are not written by this story. The contract's own tests are TC-S3-E4019-CON-01 to -06 and are owned by RWB-S3-E4019-CON.

### 17. Guardrails

- No value a business person may change is written in code: the rule IDs, the conditions, the to states, the share basis and the six messages are rule rows or package content, never constants (BR-S3-007; BR1, BR3).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the claim ID, account keys, dates, amounts, a basis code and versions only, and the fixture is synthetic.
- No read of another service's tables: the case arrives on the signal, the rule rows with the package, and nothing joins across a schema (DP-01).
- No copy of ACE data: the balance and the payments are read at the batch date and no balance, share or position column exists in `rwb_guarantee` (BR4; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only three views with SELECT granted to this service's login (ASM-4541).
- No live view and no live rule package in any test: the fixture and the fake are the only endpoints, so a red test never depends on the ACE batch or on P7's estate.
- No business value in the record: the `DecisionRecord` carries the rule ID, the rule version, the balance tested, the basis code and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule and closes the case (BR7; BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-003 | A guarantee payment that clears the balance closes the case and records the subrogation position | Business Requirements Program; FSD S3 requirements served | FEAT-GUA-07 | 07 Route, settle and claim; 08 Guarantee claim | R-GUA-19; R-GUA-25; R-GUA-26; R-GUA-27 | TC-E4-019-01, TC-E4-019-02, TC-E4-019-03, TC-E4-019-04, TC-E4-019-05, TC-E4-019-06 |

REQ-S3-003 is the one requirement whose text names this behaviour, so the trace runs on it; TSD S3 T8 maps the same set of IDs to FEAT-GUA-01, which is the module's "written one epic ahead" placeholder, and the feature code is carried alongside until the C1 PRD settles the mapping (Section 19). The legacy key also names FEAT-GUA-03 as its prerequisite; no requirement of this module references that prerequisite, so it is not carried as a row.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4019-CON | Contract | H: declares the `GuaranteeClose` element, the read rule of the three views, the close rule set, the versioning rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-17 shows the claim result |
| RWB-S3-E4015-APP, RWB-S3-E4015-CON | App development, Contract | Siblings: the claim representation, the result operation the close lands on and the states it leaves |
| RWB-S3-E4013-APP, RWB-S3-E4014-APP | App development | Siblings: the prepared and submitted claim this step closes |
| RWB-S3-E4016-APP | App development | Sibling: the subrogation position entered by R-GUA-23 and R-GUA-24 and the residual of R-GUA-25 |
| RWB-S3-E4017-APP, RWB-S3-E4018-APP, RWB-S3-E4020-APP | App development | Siblings: the guarantor notices, the negotiation and the insurance claim of the same module |
| S1 rwb-valuation | Service | The route decision the case is returned to at R-GUA-19 and R-GUA-27 |
| P3 rwb-case | Service | The case, its status, its closure, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Service | The rule package and the GUARANTEE rows that answer the step |
| P8 rwb-payment | Service | The posting and the booking of the guarantee payment in ALS core and GL |
| RWB-ITG-W3 | Integration | I: the cross-service proof of the reads and the report against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published element, the read rule of the three views, the close rule set, the versioning and the fakes: RWB-S3-E4019-CON.
- The claim representation, its create and result operations and its states: RWB-S3-E4015-APP and RWB-S3-E4015-CON, with RWB-S3-E4013-APP and RWB-S3-E4014-APP for the preparation and the submission.
- The subrogation position at R-GUA-23 and R-GUA-24 and the residual at R-GUA-25: RWB-S3-E4016-APP.
- The guarantor notices, the negotiation and the insurance claim: RWB-S3-E4017-APP, RWB-S3-E4018-APP and RWB-S3-E4020-APP.
- The case, its status, its closure, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3), reached only through the forwarded case signal and the stage report.
- The posting, the booking and the reconciliation of the guarantee payment in ALS core and GL: P8 rwb-payment and the core bank.
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA (GAP-2735).
- The GUARANTEE rows, their authoring, four-eyes approval, effective date and rollback, and the central ledger: rwb-decision (P7).
- A Kafka event for a closed guarantee, its name, its schema and its consumers: not published by this story; recorded as ASM-4538.
- SCR-17, its field list and the gateway-bff composite route: the platform edge story and the screen owner (DP-19).
- The real cross-service proof against the live owners and the `-ITG` copies of the legacy cases: RWB-ITG-W3.

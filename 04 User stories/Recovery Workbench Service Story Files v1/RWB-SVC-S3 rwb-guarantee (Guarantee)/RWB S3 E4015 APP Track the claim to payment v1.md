# RWB-S3-E4015-APP Track the claim to payment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S3-E4015-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4015-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice split from RWB-E4-015 for rwb-guarantee (S3). The claim is followed inside `GuaranteeClaimWorkflow` on task queue `rwb-guarantee`, the child of `CaseWorkflow`; the deadline is a durable timer of that workflow and not a `timer` row of rwb-case; the claim row is `guarantee_claim` in `rwb_guarantee`; the decision is written through the local decision-record library before any change (DP-03); the payment facts of `v_ace_payment` are read on the rwb-source-data contract and never from a view of this service (DP-05); the base becomes `/api/recovery/guarantee/v1` (DP-13) and SCR-17 Guarantee claim is reached through the gateway-bff composite route (DP-19). The four legacy acceptance criteria are copied verbatim, with one case mock line added to AC2 and AC3. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **guarantee officer (RW-GUARANT)**, I want **the claim followed through its states inside `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` — the claim held in one `guarantee_claim` row of `rwb_guarantee` with its type, deadline, claimed amount, filed date, paid amount and status, the claim deadline held as a durable timer of the same workflow, and the lost claim, its reason and its amount recorded with the service level breach raised to the case of record and to the officer when the deadline passes —**, so that **no guarantee claim misses its deadline**.

This is the application slice of legacy RWB-E4-015, and it owns the tracking step of the guarantee route. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the messages, the screen and the data rows they depend on;
- `GuaranteeClaimWorkflow`, the S3 stage child of `CaseWorkflow` (rwb-case) on this service's own queue `rwb-guarantee` in namespace `rwb-recovery`, with its `recordAndApply` and `armClaimDeadline` activities (Temporal and Drools Design slides 5 and 13; Architecture v5 slides 5 and 19);
- the claim deadline of R-GUA-01 as a durable timer of that workflow, re-armed on every new `claim_deadline`, and never a `timer` row and never a Schedule;
- the evaluation of the GUARANTEE route set rows of this feature — R-GUA-05, R-GUA-09 and R-GUA-12 — at their version in force, and the payment rows that move the claim row when a payment fact arrives (R-GUA-20 and R-GUA-22), each with its rule ID and its package version;
- the writer of `guarantee_claim` in schema `rwb_guarantee`, from DF-TRT-015 to DF-TRT-022, and `PATCH /guarantee-claims/{claimId}` on base `/api/recovery/guarantee/v1` that records the claim result (DP-13);
- the local decision record of every state change, written through the RWB-PLT-E1027-CON library inside the caller's transaction (DP-03);
- the stage outcome reported to the parent `CaseWorkflow` — DEADLINE_MISSED for the two lost-claim rows and the other targets of the route set — with the rule ID and the version; this service writes no case row (DP-01);
- the breach raise: one service level breach per lost claim, carried to the case of record and to the guarantee officer's task list.

It does not own: the published shape of the two claim operations and of `guarantee_claim`, the error set and the fakes, which are RWB-S3-E4015-CON; the preparation of the claim and the scheme checklist, which are RWB-S3-E4013-APP; the submission to the TCG portal and the submission reference, which are RWB-S3-E4014-APP; the subrogation position and R-GUA-23 to R-GUA-25, which are RWB-S3-E4016-APP; the guarantor notices, which are RWB-S3-E4017-APP; the closing of the guarantee, which is RWB-S3-E4019-APP; the case, its stage state, its `timer` and `task` rows and its parent workflow, which are rwb-case's (P3); the GUARANTEE package and its rows, which are rwb-decision's (P7); the payment facts of ACE, which are rwb-source-data's (P1); the roles, rights and scope data, which are rwb-access's (P4); the gateway-bff composite route and the screen field list, which are the platform edge story's.

### 2. Business rationale

Guarantee and TCG claims are late because deadlines are not tracked (FSD S3 A1.3), and the module measure is exactly that: claims filed inside the deadline, 100 percent, measured on the decision log and the Workbench records, reviewed monthly (FSD S3 A2.3.1). The legacy story answers it inside the monolith: one service method reads the case, moves the case state, writes a `timer` row, writes a `guarantee_claim` row and copies a decision-log entry, all in the one `recovery` schema. The business objective is unchanged — follow the claim through its states and raise the service level breach if it stalls.

What D-RCV-60 changes is where the claim lives, who owns the clock, who owns the payment facts and how the case moves.

- **The claim row is this service's.** `guarantee_claim` is S3's table in `rwb_guarantee` (Ownership Map; Architecture v5 slide 41; TSD S3 T3.1), with the seven standard record columns of T3.0. No other service writes it.
- **The deadline is a timer, not a table row.** The legacy `timer` row (DF-WRK-027 to DF-WRK-036) is P3's screen projection; in the target the claim deadline is a durable timer of `GuaranteeClaimWorkflow`, which is what the design calls the S3 pattern — "Claim deadline timer; missed deadline = lost claim" (Temporal and Drools Design slide 5; Architecture v5 slide 5). No `timer` row, no Quartz job and no Schedule is written by this service: the Ownership Map gives S3 no job at all.
- **The case state is answered, not written.** The GUARANTEE machine's 17 states of TSD S3 T4 live on the case of record as the stage state; this story reports each target state to the parent `CaseWorkflow`, which moves it (ASM-4512; DP-01). The claim row carries its own `status` from LOV-CLAIM-STATUS — PREPARING, FILED, DEFECT, PAID, REJECTED — which is a different vocabulary from the 17 stage states and is never used as one.
- **The payment facts stay with the owner of ACE.** The legacy data table reads `v_ace_payment`; in the target only rwb-source-data reads the `recovery.v_ace_*` views (Architecture v5 slides 29 and 37), so DP-05 applies as a prohibition: the payment fact arrives on the owner's contract, with the payment code, the account key, the date, the amount, the channel and the capital amount, and no view and no account table of ACE is read here.
- **The decision record is local.** The monolith wrote `decision_log_entry` in the same schema and copied it to a data lake that the target does not have; the target writes a local `decision_record` in `rwb_guarantee` in the same transaction as the claim row and publishes it on `rwb.decision-record.v1` to the central ledger of P7 (DP-03; ADR-022).
- **The base and the screen move.** `/api/recovery/v1` becomes `/api/recovery/guarantee/v1` (DP-13), so the claim no longer shares a path namespace with the case, the payment and the treatment services, and SCR-17 Guarantee claim is composed by the gateway-bff composite route rather than by a screen reading one database (DP-19).

Three values the story needs have no number in any source read for this key, and none is invented: the stall horizon and the warning window behind "raises the service level breach", the operation by which a stage outcome and a breach reach rwb-case, and the operation by which the GUARANTEE package and the lists are read (GAP-2714, GAP-2715, GAP-2716). They are recorded with their assumptions and the story builds against documented use and a placeholder.

No REQ-S3 identifier is given for this key by any source: TSD S3 T8 maps REQ-S3-001 to REQ-S3-007 to FEAT-GUA-01, and the Epics 3 to 8 specification carries feature IDs only, so the story traces to FEAT-GUA-03 until the PRD adds the identifiers (GAP-2718).

### 3. Preconditions

- RWB-S3-E4015-CON is published: base `/api/recovery/guarantee/v1`, `POST /cases/{caseId}/guarantee-claims` with `GuaranteeClaimRequest` and `GuaranteeClaim`, `PATCH /guarantee-claims/{claimId}` with `GuaranteeClaimUpdate`, the error set with the RFC 9457 problem body, the `Idempotency-Key` rule, the `guarantee_claim` DDL template with the standard columns and the fakes. This story builds against that contract and never against rwb-case, rwb-decision or rwb-source-data.
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` declared `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003, and the `decision_record` DDL template applied in this service's own schema (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-17 Guarantee claim from the case read and the guarantee-claim read, one hop each, read only (DP-19).
- The `rwb_guarantee` schema and login exist from the platform database story, and this service's Flyway sequence carries `guarantee_claim` from the contract template; an applied migration is never edited (DP-15).
- The workflow kit is in place on task queue `rwb-guarantee` in namespace `rwb-recovery`, and `CaseWorkflow` of rwb-case starts this stage as a child on that queue with parent close policy ABANDON (Temporal and Drools Design slide 13). The kit contract is the platform's, so it adds no build dependency of its own.
- Package GUARANTEE is in force for the business date with its 32 rows over the 17 states of TSD S3 T4, each row carrying its condition, action text and timer; the rows of this story are R-GUA-05, R-GUA-09 and R-GUA-12. The package is authored and published by rwb-decision (P7), and no dependency row of this slice names it (GAP-2716; ASM-4514), so it is consumed on a documented read and a test fixture.
- The lists LOV-CLAIM-STATUS and LOV-CLAIM-TYPE are values in force read with their version (TSD S3 T3.2; BR-S3-003), on the reference data of rwb-case. DP-07 is not in this story's pattern set and the read carries no dependency row (GAP-2716; ASM-4514).
- The payment facts of the case are consumed on rwb-source-data (P1) and faked: this service holds no `v_ace_*` grant and reads no ACE view (DP-05; GAP-2717; ASM-4515).
- The case state, the case reference and the stage outcome answer are consumed on rwb-case (P3) and faked; no source publishes the operation of the stage outcome (GAP-2714; ASM-4512).
- No approval is needed to build against a Draft contract baseline: the story starts on Day 1 with only CON build dependencies (§R5.7 rule 1 and 8).

### 4. Flow

1. R-GUA-01 has already started the claim deadline from the date the scheme default conditions are met, leaving the stage in DEADLINE_TIMER_RUNNING; the parent `CaseWorkflow` starts or signals `GuaranteeClaimWorkflow` on queue `rwb-guarantee` with the case and the claim reference (Business Rules and Routing Logic v4; Temporal and Drools Design slide 13).
2. The workflow takes the GUARANTEE package version in force, evaluates the rows with the case facts and the claim facts the signal carries, and stamps the rule ID and the version on every record it writes.
3. `armClaimDeadline` reads `claim_deadline` (DF-TRT-018) of the claim and arms one durable timer on it in the workflow. The timer is the claim deadline of R-GUA-01 and is re-armed when the deadline changes; no `timer` row is written (GAP-2714; ASM-4512).
4. The officer, or the stage itself, records the claim result on `PATCH /guarantee-claims/{claimId}` with `GuaranteeClaimUpdate` — `status`, `filed_at`, `paid_amount` — with right U of Treatment and offer and the scope applied, and reads the same claim back from the answer (DP-13; TSD S3 T-A.2).
5. While the claim is in CLAIM_PREPARATION and the checklist completes, R-GUA-12 fires on CLAIM_APPROVED: the claim is submitted through the TCG claim channel by the officer at D6.5 and the stage target is CLAIM_SUBMITTED. The submission itself and its reference belong to RWB-S3-E4014-APP.
6. The claim `status` moves to FILED on the same row when the submission is recorded, and the stage keeps waiting on the deadline timer and on the TCG answers that arrive as signals.
7. The timer fires, or a redelivered signal names the same deadline: `recordAndApply` evaluates R-GUA-05 from DEADLINE_TIMER_RUNNING where `claim_deadline` has passed and `claim_status` is not submitted, and R-GUA-09 from CLAIM_PREPARATION where `claim_deadline` passed before submission. Both actions are the same three facts — the lost claim, its reason and its amount — and both targets are DEADLINE_MISSED.
8. `recordAndApply` writes, in one `rwb_guarantee` transaction: the `guarantee_claim` row with its reason, its lost amount and its status, the local `decision_record` through `DecisionRecordWriter.record` with the rule ID and the package version, and the outbox rows of the library. A failed record write changes nothing (DP-03; legacy AC4).
9. `raiseBreach` raises one service level breach for the lost claim to the case of record and to the guarantee officer's task list, with the claim reference, the deadline, the reason and the amount. The breach clock, its task and its escalation are rwb-case's (GAP-2714; ASM-4512).
10. The stage outcome — DEADLINE_MISSED for the two lost-claim rows, GUARANTEE_CLOSED or RESIDUAL_TO_ROUTE where a sibling story's row fires — is returned to the parent `CaseWorkflow`, which moves the case stage state. This service writes no case row and no case column.
11. Where a payment fact arrives for the claim, the payment rows of the route set fire: R-GUA-20 on a part payment and R-GUA-22 on a full payment move the claim row to its paid status with `paid_amount`; the subrogation consequence of R-GUA-22 and the rows R-GUA-23 to R-GUA-25 are RWB-S3-E4016-APP's. The payment fact itself is read on the rwb-source-data contract, never from `v_ace_payment` (DP-05).
12. SCR-17 Guarantee claim shows the claim, its deadline, the checklist and the result through the gateway-bff composite route, which composes the case read of rwb-case and this service's claim read in one hop each (DP-19).
13. A repeated request with the same `Idempotency-Key` returns the first answer and writes no second row, no second record and no second breach.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction rolls back: the claim row, its record and the outbox rows are all unchanged, and no breach is raised | MSG-P7-003 | AC4, TC-E4-015-04, TC-E4-015-06 |
| X2 | The caller's role does not hold Treatment and offer U on the claim operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E4-015-05 |
| X3 | The claim ID names no row in the caller's scope | 404 with the problem body; nothing is written and no breach is raised | None | Section 12.1 |
| X4 | The request carries no `status`, or a value outside LOV-CLAIM-STATUS, or a `paid_amount` on a claim that is not FILED | 422 naming the field; the row is not written | MSG-GEN-001 | AC1 |
| X5 | No GUARANTEE version is in force for the business date, or the package does not answer inside the budget | The stage waits and retries; nothing is written and no target state is reported; the case keeps its state | None | AC1 |
| X6 | The rwb-case answer or the rwb-source-data payment read does not answer inside 2 s, or its breaker is open | The stage holds, the breach is not raised twice and the timer is unchanged; the caller sees the platform envelope 503 | None | AC1, AC2 |
| X7 | The deadline timer fires for a claim whose `claim_deadline` has since moved, or whose `status` is already submitted | No lost-claim record and no breach; the timer is re-armed on the new deadline | None | AC2, AC3 |
| X8 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR4 |

X1 to X4 are the legacy paths carried onto the split, X5 to X7 are the paths the target's package, call and timer model add, and X8 is the DP-01 and DP-05 boundary. The stall horizon, the warning window and the breach escalation behind AC1 and AC2 are values in force of the rule package and of rwb-case, so none of them is a constant of this story (GAP-2715; ASM-4513).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the RWB-S3-E4015-CON fake, the decision-record writer fake, the composite-route fake and the case, payment and package fixtures; needs no live rwb-case, rwb-decision or rwb-source-data |
| Negotiable | The activity names, the workflow ID derivation, the breach payload and the flag name are this story's choice; the rules, the states, the lists, the rights and the messages are fixed |
| Valuable | Every claim carries its deadline as a live clock, and a missed deadline becomes a recorded lost claim with a raised breach instead of a silent lapse |
| Estimable | One child workflow, two activities, one operation, one repository, one library adapter, three clients and one read-only screen fragment |
| Small | Fits two weeks with its tests |
| Testable | Each criterion of section 7 is one automated test; the parent, the package, the payment read and the guard are stubbed |

### 7. Acceptance criteria

```gherkin
Feature: Track the claim to payment

  Scenario: AC1 Track the claim to payment (legacy RWB-E4-015 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then follows the claim through its states and raises the service level breach if it stalls
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-05 (legacy RWB-E4-015 AC2)
    Given the rwb-case contract mock returns the case state "DEADLINE_TIMER_RUNNING" for "RC-2026-000115"
    Given a case in state DEADLINE_TIMER_RUNNING
    When claim deadline missed
    Then record the lost claim, the reason and the amount, and report the breach
    Then the case moves to DEADLINE_MISSED

  Scenario: AC3 Rule R-GUA-09 (legacy RWB-E4-015 AC3)
    Given the rwb-case contract mock returns the case state "CLAIM_PREPARATION" for "RC-2026-000115"
    Given a case in state CLAIM_PREPARATION
    When claim deadline missed
    Then record the lost claim and the reason, and report the breach
    Then the case moves to DEADLINE_MISSED

  Scenario: AC4 Not recorded (legacy RWB-E4-015 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line is kept character for character, including the legacy repetition of `Then` and the wording of `the action is taken`; the only additions are the origin tag on each `Scenario:` line and, in AC2 and AC3, one `Given the rwb-case contract mock returns the case state ...` line. The two state values are TSD S3 T4 states of the GUARANTEE machine, and in the target the stage state lives on the case of record: the workflow reports the target state and the parent `CaseWorkflow` applies it, so "the case moves to DEADLINE_MISSED" is asserted against the parent and this service holds no case column (ASM-4512; DP-01). "The data and the rule version this feature needs are in place" is the GUARANTEE package version in force and the two lists in force, with the read recorded once (GAP-2716; ASM-4514). "The system writes the result to the decision log with the rule version" is the local `decision_record` row written in the same `rwb_guarantee` transaction through RWB-PLT-E1027-CON and published on `rwb.decision-record.v1` (DP-03). "Report the breach" is the one service level breach per lost claim, carried to the case and to the officer's task list; its clock and escalation are rwb-case's and their values are not stated (GAP-2715; ASM-4513). The decision-log failure of AC4 is the library's MSG-P7-003 and "nothing changes" is the rollback of one transaction that also holds the claim row and the outbox rows. The operation sits on base `/api/recovery/guarantee/v1` (DP-13) and SCR-17 reaches it through the gateway-bff composite route (DP-19).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-GUA-05 | Guarantee claim | D6.5, D6.6 | DEADLINE_TIMER_RUNNING | CLAIM_DEADLINE_MISSED | claim_deadline passed and claim_status is not submitted | Record the lost claim, the reason and the amount, and report the breach | DEADLINE_MISSED | Guarantee officer | Workbench, Workbench scheduler | None |
| R-GUA-09 | Guarantee claim | D6.5, D6.6 | CLAIM_PREPARATION | CLAIM_DEADLINE_MISSED | claim_deadline passed before submission | Record the lost claim and the reason, and report the breach | DEADLINE_MISSED | Guarantee officer | Workbench, Workbench scheduler | None |
| R-GUA-12 | Guarantee claim | D6.5, D6.6 | CLAIM_APPROVAL | CLAIM_APPROVED | the guarantee officer verifies the claim at D6.5 | Submit the claim through the TCG claim channel | CLAIM_SUBMITTED | TCG | Workbench, TCG claim channel | 2 working days |

The three rows are the rows of the Business Rules and Routing Logic v4 for this feature, copied character for character, and their owner column is a business role, not a service: the stage state is moved by rwb-case on this story's answer, the claim row is written here, the submission itself is RWB-S3-E4014-APP's, and the timer column names the clock this story arms as a durable timer. The payment rows that move the claim row (R-GUA-20, R-GUA-22) and the subrogation rows (R-GUA-23 to R-GUA-25) are rows of the same route set and are named in section 19 as the sibling stories'.

| ID | Rule | Source |
|---|---|---|
| BR1 | The claim is one `guarantee_claim` row of this service: `claim_type`, `claim_deadline`, `claimed_amount`, `filed_at`, `paid_amount` and `status`, written on that row and nowhere else | TSD S3 T3.1, T3.2; Architecture v5 slide 41 |
| BR2 | The decision is written before the row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S3 T2; legacy AC1 and AC4 |
| BR3 | The claim deadline is a durable timer of `GuaranteeClaimWorkflow`: no `timer` row, no Quartz job and no Schedule is written or registered by this service | Temporal and Drools Design slide 5; Architecture v5 slides 5 and 44; Ownership Map jobs (0 for S3) |
| BR4 | The stage state stays rwb-case's: this story reports the target state and the breach to the parent, which moves the case, and this service writes no case row and no case column | ASM-4512; DP-01 |
| BR5 | The payment facts stay with rwb-source-data: no `v_ace_*` view, no ACE table and no account table is read, and the payment arrives on the owner's contract | DP-05; Architecture v5 slides 29 and 37; GAP-2717 |
| BR6 | The claim status takes only the values of LOV-CLAIM-STATUS in force and the claim type only those of LOV-CLAIM-TYPE; the stall horizon, the warning window and the escalation are rule rows and reference rows with a version, never code | TSD S3 T3.2; BR-S3-003; GAP-2715 |
| BR7 | The right is declared and not re-implemented: the read and the patch need Treatment and offer, and the check answers from the platform guard | TSD S3 T6.1; Template and Rules §R5.5 DP-08 as a template capability |
| BR8 | The same request twice, or the same `Idempotency-Key` twice, writes once and raises one breach, and the repeat is counted | TSD S3 T-A.2 |
| BR9 | No personal data: the row, the record, the breach, the log and every call carry identifiers, codes, dates and amounts only | TSD S3 T3.1; Template and Rules §R7.2 s17 |
| BR10 | A claim row exists only with its decision record, and a claim never leaves a state without its record and its reported outcome | DP-03; REQ-S3-002 |

**Where each rule lives in the target.** BR1 is the repository and the contract element. BR2 is the library adapter and the one transaction. BR3 is `armClaimDeadline` and the workflow's durable timer. BR4 is the child-workflow return and the parent. BR5 is the payment client and the absent grant. BR6 is the two lists and the reference rows. BR7 is the contract's `security` section and the guard. BR8 is the idempotency key. BR9 is the guardrail set of section 17 and BR10 is the transactional boundary of `recordAndApply`.

### 9. State transitions

The 17 stage states of the GUARANTEE machine are TSD S3 T4 and are moved by rwb-case on this story's answer; the claim row's `status` is this service's and moves on the same step. The two are different objects and are never used one for the other.

| From (stage state on the signal) | Event | Condition | Reported target state |
|---|---|---|---|
| DEADLINE_TIMER_RUNNING | CLAIM_DEADLINE_MISSED | R-GUA-05: `claim_deadline` passed and `claim_status` is not submitted | DEADLINE_MISSED |
| CLAIM_PREPARATION | CLAIM_DEADLINE_MISSED | R-GUA-09: `claim_deadline` passed before submission | DEADLINE_MISSED |
| CLAIM_APPROVAL | CLAIM_APPROVED | R-GUA-12: the officer verifies the claim at D6.5 | CLAIM_SUBMITTED, recorded by RWB-S3-E4014-APP |
| DEADLINE_TIMER_RUNNING, CLAIM_PREPARATION, CLAIM_APPROVAL | no row fired | The signal names a state or an event no row of the package expects | None reported; the stage waits |
| DEADLINE_MISSED | LOSS_RECORDED | R-GUA-27: the loss amount and the reason are recorded | RESIDUAL_TO_ROUTE, RWB-S3-E4019-APP's row |
| CLAIM_SUBMITTED | FULL_PAYMENT_RECEIVED | R-GUA-22: `claim_amount_paid = guaranteed_amount` | CLAIM_PAID, with the subrogation position RWB-S3-E4016-APP's |

| `guarantee_claim.status` (this service) | Event | Condition | To |
|---|---|---|---|
| PREPARING | The claim result is recorded on the patch | `status` is a value of LOV-CLAIM-STATUS and the record is written | FILED, DEFECT or REJECTED as the value carries |
| FILED | A payment fact arrives for the claim | `paid_amount` is written from the payment fact | PAID |
| PREPARING or FILED | The deadline passes and no submission is recorded | R-GUA-05 or R-GUA-09 fires | The lost-claim value of LOV-CLAIM-STATUS in force, with the reason and the lost amount on the row |

The claim `status` is declared varchar(12) with no check constraint in the DDL template, so a new value is a data change and not a contract change. The stage execution itself is RUNNING, COMPLETED or FAILED in the workflow history, retried on the platform policy with the package refusal non-retryable, and the run continues as new at every stage end and at least every 28 days.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-GUARANT, guarantee officer (CRU) | Reads the claim, records the claim result, and sees and acknowledges the breach; the primary role of the feature |
| RW-CASEOWN, case owner (CRU) | Reads the claim of a case in scope and records the claim result |
| RW-RESTRUCT, restructuring officer (CRUA); RW-SPECIAL, hardship and vulnerability specialist (CRU) | Read the claim of a case in scope and, where the case is theirs, record the result |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-PRODHEAD, RW-CREDCOMM, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (R or RA) | Read the claim and its state in scope; none of them records a result here |
| SY-CASEWF, SY-RULES, SY-AGENT (R) | Read as service identities through the same checks; the workflow and the agent act under their own identity |
| rwb-case (P3) | Owns the case of record, the stage state, the `timer` and `task` rows, the parent `CaseWorkflow` and the breach clock; applies the state this stage reports |
| rwb-decision (P7) | Owns the GUARANTEE package, its 32 rows and its versions, and the central ledger |
| rwb-source-data (P1) | Owns the ACE payment facts and answers them on its contract |
| rwb-access (P4) | Owns the roles, the rights and the scope data the guard answers with |
| No delegation of authority level applies | The story tracks a claim and records its result; it approves nothing and moves no money |

No personal name, no address, no contact value and no credential appears in the claim, the record, the workflow input, the breach or the logs: the claim carries the case, the claim type, the deadline, the amounts and the status, and the guarantor is reached only as a party key by the services that own the party.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim (S3, `rwb_guarantee`) | id | Write on create by RWB-S3-E4013-APP; read as the reference of every answer |
| DF-TRT-016 | guarantee_claim (S3) | case_id | Write on create; read on every call |
| DF-TRT-017 | guarantee_claim (S3) | claim_type | Write, a value of LOV-CLAIM-TYPE |
| DF-TRT-018 | guarantee_claim (S3) | claim_deadline | Write on create and on a deadline change; the input of the durable timer |
| DF-TRT-019 | guarantee_claim (S3) | claimed_amount | Write on create; read by the lost-claim action |
| DF-TRT-020 | guarantee_claim (S3) | filed_at | Write on the submission result |
| DF-TRT-021 | guarantee_claim (S3) | paid_amount | Write when a payment fact is matched to the claim |
| DF-TRT-022 | guarantee_claim (S3) | status | Write, a value of LOV-CLAIM-STATUS |
| Standard columns | guarantee_claim (S3) | is_active, state, version, created_at, created_by, updated_at, updated_by | Write, with the optimistic lock of `version` (TSD S3 T3.0) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_guarantee`) | rule ID, rule version, inputs reference, outcome, decided at and the hashes | Write through the local library, before the row changes (DP-03) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case state and the reference arrive on the case contract (DP-01) |
| DF-WRK-027 to DF-WRK-036 | timer (P3, `rwb_case`) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not written: the deadline is a durable timer of this service's workflow (BR3) |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Not read: the payment fact arrives on the rwb-source-data contract (DP-05) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read directly: the evaluated package returns the row outputs and their version |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7, `rwb_decision`) | the central ledger entry | Not written and not read here: P7 seals it from the shared topic (DP-03) |

Field IDs are those of TSD S3 T3.1 and the Logical Data Model and Data Dictionary v8; the case, timer, payment, ledger and rule rows are the rows the legacy story lists in its Data table, with their owners changed by the target. `guarantee_claim` is the only table this story writes and it arrives with the DDL template of RWB-S3-E4015-CON, applied by this service's own Flyway sequence (DP-15); `decision_record` and `idempotency_key` are library objects created in `rwb_guarantee` by the library's migration (DP-03). No foreign key crosses a schema and no row of another service's table is joined (DP-01).

**No personal data.** The rows this story writes carry identifiers, codes, dates and amounts. The borrower, the guarantor, the address, the contact value and the identity number never enter `rwb_guarantee`; they are held by ACE and reached only through rwb-source-data by the services that need them, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). The service provides two operations on the guarantee-claim resource, and this story supplies the patch; the create is the resource's and is served by RWB-S3-E4013-APP. Their published shape, error set and fakes are declared by RWB-S3-E4015-CON.

| ID | Method | Path | Request and response | Access | Idempotency |
|---|---|---|---|---|---|
| API-S3-001 | POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest` in, `GuaranteeClaim` out; served by RWB-S3-E4013-APP | Treatment and offer C, scope applied | `Idempotency-Key` header required |
| API-S3-002 | PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` in, `GuaranteeClaim` out; this story | Treatment and offer U, scope applied | Not applicable |

The errors are 401, 403 with MSG-P4-002, 404 with the problem body, 409 where the claim's state refuses the patch, 422 with MSG-GEN-001 or MSG-P7-009 naming the field, and 503 with the platform envelope. The two operations, their rights and their idempotency are those of TSD S3 T-A.1 and T-A.2 for API-S3-001 and API-S3-002, with the base renamed by DP-13 and nothing else changed.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The case read of rwb-case, operation Not specified in the source documents (GAP-2714; ASM-4512) | P3 rwb-case | The case reference, the stage state and the product group the evaluation needs; read only, faked |
| The stage outcome and breach answer of rwb-case, operation Not specified in the source documents (GAP-2714; ASM-4512) | P3 rwb-case | Carries the target state and the one breach of a lost claim with the rule ID and its version; on the workflow boundary it is the child-workflow return the parent applies |
| The payment fact read of rwb-source-data, operation Not specified in the source documents (GAP-2717; ASM-4515) | P1 rwb-source-data | The payment code, account key, date, amount, channel and capital amount of the case; read only, faked; no `v_ace_*` view is read here (DP-05) |
| The GUARANTEE package and reference read of rwb-decision and rwb-case, operation Not specified in the source documents (GAP-2716; ASM-4514) | P7 rwb-decision; P3 rwb-case | The rule rows of the route set at their version in force and the LOV-CLAIM-STATUS and LOV-CLAIM-TYPE members |

Every row is one hop with a 2 s timeout and a breaker per downstream (ADR-020); where a row crosses a service boundary the answer is faked until its owner publishes it. None of the four rows is a dependency of this slice's plan, which is why the metadata carries no C row and the absence is recorded with the assumptions (GAP-2714, -3, -4).

#### 12.3 Events published

None. The Ownership Map gives S3 no event, and this story adds none: no outbox row of its own is written and no topic outside the service's own is named. The `DecisionRecorded` element of the local decision-record library is written inside the caller's transaction and published by the library on `rwb.decision-record.v1` (DP-03), and its payload is the library's, not this service's. The service topic `rwb.guarantee.events.v1` is named for completeness only (DP-14); no producer is declared here.

#### 12.4 Events consumed

None. The stage is reached by a Temporal signal the parent `CaseWorkflow` forwards and by the TCG answers as signals; the GUARANTEE package version and the two lists are read on their contracts at the start of a run (12.2), and no Kafka subscription, no consumer group and no inbox row is held by this story.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow, the S3 stage child of `CaseWorkflow`, one execution per case and stage, continues-as-new | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case reference, the claim reference, the business date, the package version in force; the deadline timer; output: the stage outcome and the breach of section 9 |
| `recordAndApply` | Activity | `rwb-guarantee` | The claim row, the local decision record and the outbox rows in one transaction (the design's `RecordAndApply`) |
| `armClaimDeadline` | Activity | `rwb-guarantee` | `claim_deadline` in, the durable timer armed or re-armed out; no `timer` row |
| `raiseBreach` | Activity | `rwb-guarantee` | The lost claim, its reason and its amount in; the breach accepted by rwb-case out |

The evaluation of the package runs inside the workflow step through the service's embedded Drools runtime and the design's `EvaluateRules` contract is its name; this story adds no activity for it. The workflow name is fixed by the design (`GuaranteeClaimWorkflow` on `rwb-guarantee`); the activity names outside `recordAndApply` are this story's choice.

#### 12.6 Schedules

None. The claim deadline is a durable timer inside `GuaranteeClaimWorkflow`, not a Temporal Schedule and not a Quartz job; the Ownership Map gives S3 no job, and the retired `TE-007` scheduler has no successor here. No Schedule of Architecture v5 slide 44 is owned, moved or registered by this story.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 | Written and read; DF-TRT-015 to DF-TRT-022 and the standard columns (BR1) |
| `decision_record` | `rwb_guarantee` | PLT library object applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction (DP-03) |
| `idempotency_key` | `rwb_guarantee` | PLT library object applied in this schema | The key of the claim create and the answer it holds (BR8) |

Not owned and never written or read as a table: `recovery_case`, `timer`, `task` and `assignment` (P3), `rule_row`, `decision_log_entry` and the approval items (P7), the payment rows of `rwb_payment` (P8), the party and ACE rows behind the `v_ace_*` views (P1). No foreign key leaves `rwb_guarantee` (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| RWB-S3-E4015-CON guarantee-claim fake | A claim in PREPARING and one in FILED with their deadlines and amounts; a 403, a 404, a 409, a 422 and a 503 answer; a repeated key answering the first result | AC1, AC2, AC3, X2 to X4 |
| RWB-PLT-E1027-CON writer fake | An accepted record with its chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable store raising MSG-P7-003 | AC4, X1 |
| rwb-case case fixture | Case `RC-2026-000115` at the stage state DEADLINE_TIMER_RUNNING and at CLAIM_PREPARATION; the stage outcome and the breach accepted; a refused answer; a delayed answer | AC2, AC3, X5, X6 |
| rwb-source-data payment fixture | A part payment and a full payment for the case with the payment code, the date, the amount and the capital amount; no payment; a stale answer | AC1, Section 9 |
| GUARANTEE package fixture | Version in force with rows R-GUA-05, R-GUA-09 and R-GUA-12, their conditions and their timers; a version with no row for the state | AC1, AC2, AC3 |
| RWB-PLT-N001-CON composite-route fake | The merged SCR-17 answer for `RC-2026-000115`, with the case read and the claim read in one hop each | AC1 |

The fakes are test-only and are replaced by the real services in SIT; the drift between a fake and RWB-S3-E4015-CON, or between a client and its owner's document, is a build failure. The case, payment and package fixtures stand in for their owners' absent operations and are recorded with GAP-2714, -3 and -4.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided by this story (2 by the service), 4 consumed | API-S3-002 provided here and API-S3-001 by RWB-S3-E4013-APP, both on `/api/recovery/guarantee/v1`; the case read, the outcome and breach answer, the payment read and the package and reference read; one hop, 2 s |
| Kafka | None published, none consumed | The library publishes the record on `rwb.decision-record.v1` (12.3); no subscription is held (12.4) |
| Temporal | 1 workflow and 3 activities, no child workflow, no Schedule | `GuaranteeClaimWorkflow`, `recordAndApply`, `armClaimDeadline` and `raiseBreach` on `rwb-guarantee` |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, module `claim`, Java package `th.co.scb.ace.workbench.recovery.guarantee.claim`; front end `src/modules/recovery/guarantee/GuaranteeClaim.tsx`, the fragment SCR-17 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The payment fact read on rwb-source-data's contract, and no `v_ace_*` grant of this service | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/guarantee/v1`; the two claim operations keep API-S3-001 and API-S3-002 | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 carries legacy AC1's "writes the result to the decision log with the rule version" and legacy AC4's fail-closed behaviour. DP-05 is the prohibition this key turns on `v_ace_payment`: the payment fact is read on the owner's contract and no ACE view is opened. DP-13 renames the base and keeps the operation IDs, so the legacy endpoint block of RWB-E4-015 keeps both of its paths under the new base. DP-19 covers SCR-17 only. DP-10 is not applied because the service owns no job: the deadline is a durable timer inside the workflow, askable of no Schedule and of no job table.

**Dependencies the pattern table adds and the plan does not hold.** The table adds the two H rows the metadata also carries and nothing else. Four capabilities the story leans on have no row: the case read and the outcome and breach answer (P3), the payment read (P1), the GUARANTEE package (P7) and the two lists (P3). They are recorded as GAP-2714, -3 and -4 with their assumptions, and the story builds against their fakes on Day 1 with no C dependency blocking it (§R5.7 rule 2).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimWorkflow` | Workflow | The stage child: receives the signal, asks the package, calls the activities, waits on the deadline timer, reports the outcome and the breach |
| `ClaimController` | Controller | API-S3-002 and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| `ClaimService` | Service | The claim result, the status vocabulary in force and the state of the row |
| `ClaimValidator` | Service | The claim reference and its scope, `status` against LOV-CLAIM-STATUS, `paid_amount` only on a filed claim |
| `ClaimRepository` | Repository | Reads and writes `guarantee_claim` in `rwb_guarantee` only |
| `ClaimDecisionWriter` | Library adapter | One hash-linked record with the rule ID and the version, before the row changes (DP-03) |
| `PaymentFactClient` | Client | The payment read of rwb-source-data, one hop, 2 s, breaker, stale marker |
| `CaseAnswerClient` | Client | The case read and the stage outcome and breach answer to rwb-case |
| `ClaimScreen` | React component | Shows the claim, its deadline and its result on SCR-17, read only, with the refusal, not-recorded and lost states |

**Database.** `guarantee_claim` is created from the RWB-S3-E4015-CON template with the physical types of TSD S3 T3.1 — `claim_type` varchar(25), `claim_deadline` date, `claimed_amount` numeric(18,2), `filed_at` date, `paid_amount` numeric(18,2), `status` varchar(12), `case_id` uuid — on the primary key `id`, with `case_id` a cross reference with an index and no foreign key, and the seven standard columns of T3.0. `decision_record` and `idempotency_key` are library objects on the same sequence (DP-15). No `timer`, no `task` and no case table is created here.

**Configuration and reference data.**

- The stall horizon, the warning window and the escalation behind "raises the service level breach": versioned rule and reference rows, content Not specified in the source documents (GAP-2715; ASM-4513).
- LOV-CLAIM-STATUS and LOV-CLAIM-TYPE at their version in force (TSD S3 T3.2).
- The GUARANTEE package and its rows, read at their version in force and stamped on every record (GAP-2716; ASM-4514).
- The decision code of each step and of the breach, read as a value in force; no code list is written here.
- The 2 s budget and the single hop are the platform rule of ADR-020, not a value of this story.

**Build steps**

1. The claim slice of `ClaimController`, `ClaimService` and `ClaimRepository` over the contract fake; test AC1 and X2 to X4.
2. `ClaimDecisionWriter` and the one transaction of `recordAndApply`, with the rollback path; test AC1 and AC4.
3. `GuaranteeClaimWorkflow` registered on `rwb-guarantee` and the child registration on `CaseWorkflow`; test AC2 and AC3.
4. `armClaimDeadline` and the durable timer, with the re-arm and the stale-fire path; test AC2, AC3 and X7.
5. `PaymentFactClient` against the payment fake, with the part, full, absent and stale answers; test AC1 and section 9.
6. `CaseAnswerClient` and `raiseBreach` against the case fake, with the accepted, refused and delayed answers; test AC2, AC3 and X6.
7. `ClaimScreen` read through the composite-route fake; test AC1.
8. The boundary test: no statement outside `rwb_guarantee`, no `v_ace_*` read, no `recovery_case`, `timer` or `task` write; test BR3, BR4 and BR5.

**Feature flag.** `rwb.guarantee.claim-tracking-v1`, read as a flag of the platform library; off means the workflow does not start, the claim answers read only and the deadline timer is not armed.

**Done when.** The tests of section 16 pass, the contract tests of RWB-S3-E4015-CON stay green, one synthetic case signal writes one claim row with its record in the same transaction, the deadline timer fires once and raises one breach, a forced record failure leaves no row and no breach, and SCR-17 shows the claim through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the request is missing or invalid (X4) | Enter {field}. |
| MSG-P4-002 | The caller's role does not hold Treatment and offer U on the operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the claim changes (X1, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The payment product the stage reads is stale after a late or failed ACE batch (VR-S3-003-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The four texts are the legacy and FSD wording carried unchanged; MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are the three the legacy story names, and MSG-P1-001 is VR-S3-003-1 of FSD S3 A2.3.3.1, whose freshness check belongs to rwb-source-data: this service shows the marker and raises nothing of its own. MSG-P4-002 is the guard library's answer and MSG-P7-003 the library's. The breach of a lost claim carries no message of this set: it is a task and a state on rwb-case, and its wording and its clock are that service's (GAP-2715; ASM-4513). Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | States | What this story puts on it |
|---|---|---|
| SCR-17 Guarantee claim | Not due; due; submitted; paid; refused | The claim with its type, deadline, claimed amount, filed date, paid amount and status, and the lost claim with its reason and its amount |
| SCR-17 Guarantee claim | Loading | The placeholder while the composite route answers |
| SCR-17 Guarantee claim | Refused | MSG-P4-002 with the right the role lacks named |
| SCR-17 Guarantee claim | Not recorded | MSG-P7-003 with the claim unchanged and the retry offered |
| SCR-17 Guarantee claim | Stale payment | MSG-P1-001 with the stale marker while the claim itself answers |

The five legacy states of the screen — Not due; due; submitted; paid; refused — are the states SCR-17 shows, and they are presented from the claim row and the stage state, not stored as a second vocabulary. SCR-17 is served by the gateway-bff composite route, which composes the case read of rwb-case with the claim read of this service, one hop each, read only (DP-19); the browser calls no owner service directly. The screen field list, the composite route specification and the layout belong to the platform edge story, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-015-01 | AC1 | End to end | Track the claim to payment |
| TC-E4-015-02 | AC2 | End to end | Rule R-GUA-05 |
| TC-E4-015-03 | AC3 | End to end | Rule R-GUA-09 |
| TC-E4-015-04 | AC4 | Component | Not recorded |
| TC-E4-015-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-015-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy table carries no level column, so the two deadline cases and the whole-step case map to `End to end`, the not-recorded and access cases to `Component`, and the forced failure of Principle 5 to `NFR`. The claim, library, case, payment, package and composite-route fakes of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000115`, the claim of 2026-12-01 with its deadline and its amounts — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies TC-E4-015-01-ITG to TC-E4-015-06-ITG belong to the wave 3 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the rules, the states, the lists, the stall horizon, the warning window and the message texts are rule rows, reference rows or values in force with a version.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry case and claim identifiers, codes, dates and amounts only, the guarantor is a party key of another service, and the fixture is synthetic.
- No read of another module's tables: the case state arrives on its contract, the payment on rwb-source-data's contract, the package on its own read, and `rwb_guarantee` holds no foreign key into another schema (DP-01, DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view and holds no such grant, so a statement on `v_ace_payment` is refused by the database (BR5).
- The case stays with rwb-case: no `recovery_case`, `timer`, `task` or `assignment` row is written here, and the deadline is a durable timer of this service's workflow (BR3, BR4).
- The central ledger is never written or read here: `decision_log_entry` and `rule_row` are P7's, and the record reaches them on `rwb.decision-record.v1` (DP-03).
- The decision record is written in the same transaction as the claim row, and a failed write rolls the whole step back with MSG-P7-003.
- One base, one topic, one queue and one login per service: this story names no other service's base or topic as its own (DP-13, DP-14).
- A published version is never edited in place: a correction to `guarantee_claim` is a new Flyway version on the service sequence (DP-15).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| No REQ-S3 identifier is given for this key by any source read: TSD S3 T8 maps REQ-S3-001 to REQ-S3-007 to FEAT-GUA-01, and the Epics 3 to 8 specification carries feature IDs only (GAP-2718; ASM-4516) | The claim is followed through its states and the service level breach is raised if it stalls; claim status, payment and any shortfall are recorded on the case (FSD S3 A2.3, REQ-S3-002) | FEAT-GUA-03 | R-GUA-05, R-GUA-09, R-GUA-12 | TC-E4-015-01 to TC-E4-015-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4015-CON | Contract | H: declares the base, the two claim operations, the three schemas, the `guarantee_claim` DDL template, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the record is written through in the same transaction |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-17 |
| RWB-S3-E4013-APP | App development | Sibling and predecessor: the claim is prepared and opened there, on API-S3-001 |
| RWB-S3-E4014-APP | App development | Sibling and predecessor: the submission to the TCG portal and R-GUA-12's officer step |
| RWB-S3-E4016-APP | App development | Sibling: the subrogation position and R-GUA-23 to R-GUA-25 |
| RWB-S3-E4017-APP | App development | Sibling: the guarantor and co-borrower notices |
| RWB-S3-E4019-APP | App development | Sibling: the closing of the guarantee and R-GUA-26 and R-GUA-27 |
| P3 rwb-case | App development | The parent `CaseWorkflow`, the stage state, the `timer` and `task` rows and the breach clock the case mock stands for |
| P7 rwb-decision | App development | The GUARANTEE package, its 32 rows and its version |
| P1 rwb-source-data | App development | The ACE payment facts, read on its contract |
| RWB-ITG-W3 | Integration | The cross-service proof of the stage against the live parent, package and source data, held by the wave 3 harness |

### 19. Out of scope

- The published shape of the two operations, the three schemas, the `guarantee_claim` DDL template, the error set and the fakes: RWB-S3-E4015-CON.
- The preparation of the claim, the scheme checklist and R-GUA-04: RWB-S3-E4013-APP.
- The submission to the TCG portal, its reference and R-GUA-21: RWB-S3-E4014-APP.
- The subrogation position, R-GUA-22's subrogation consequence and R-GUA-23 to R-GUA-25: RWB-S3-E4016-APP.
- The guarantor and co-borrower notices and R-GUA-06: RWB-S3-E4017-APP.
- The negotiation with a guarantor and R-GUA-28 to R-GUA-32: RWB-S3-E4018-APP.
- The closing of the guarantee and R-GUA-26 and R-GUA-27: RWB-S3-E4019-APP.
- The insurance claim on a collateral event: RWB-S3-E4020-APP.
- The case of record, its stage state, the `timer` and `task` rows, the parent `CaseWorkflow` and the breach clock: rwb-case (P3), with the outcome and breach shape recorded once (GAP-2714; ASM-4512).
- The GUARANTEE package, its rows and its versions, and the central ledger: rwb-decision (P7).
- The ACE payment facts and every `v_ace_*` view: rwb-source-data (P1); this service holds no such grant (DP-05).
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout of SCR-17: the platform edge story (DP-19).
- The money: the posting, the matching of a receipt to the ledger and the balance belong to rwb-payment (P8); this story reads a payment fact and writes no money row.
- The value of the stall horizon, of the warning window and of the breach escalation (GAP-2715; ASM-4513).
- The real cross-service proof of the stage against the live parent, package and source data: the wave 3 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.

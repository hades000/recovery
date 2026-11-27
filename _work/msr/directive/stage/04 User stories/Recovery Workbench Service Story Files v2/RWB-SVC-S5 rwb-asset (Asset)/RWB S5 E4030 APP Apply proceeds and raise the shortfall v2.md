# RWB-S5-E4030-APP Apply proceeds and raise the shortfall

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4030-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-030 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-V |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S5-E4030-APP-16) |
| Depends on (build) | RWB-S5-E4030-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | v1, from the /v1 path in section 12.2 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 23 November 2026: the application slice of RWB-E4-030 for rwb-asset. The four legacy criteria are kept word for word with their origin tag and the six legacy test cases keep their IDs. The step becomes the proceeds-and-shortfall branch of `AssetDisposalWorkflow` on queue `rwb-asset`: it consumes EV-25 `ProceedsMatched` from `rwb.payment.events.v1`, evaluates R-DIS-54 and then R-DIS-55 on the DISPOSAL package in force, writes the sale outcome in `rwb_asset`, records each outcome through the local decision-record library before the row changes (DP-03) and answers the case moves to rwb-case. The legacy `v_ace_account` and `v_ace_npa_sale` reads leave the service for the rwb-source-data data product (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). Gaps: the consumed names are not published and the plan carries no C row (GAP-2944; ASM-4840); EV-25's consumer list does not name this service (GAP-2945; ASM-4841); no S5-to-P1 edge exists for the two ACE facts (GAP-2946; ASM-4842); no element holds the residual (GAP-2947; ASM-4843); the balance application is FEAT-PAY-10's (GAP-2948; ASM-4844); the vendor fee has no element here (GAP-2949; ASM-4845); five adjacent rules own no legacy criterion (GAP-2950; ASM-4846); no requirement id (GAP-2951; ASM-4847); the screen states do not match the lists (GAP-2952; ASM-4848); DP-09 and DP-04 sit outside the pattern set (GAP-2953; ASM-4849). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4030-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 24 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **the Workbench to apply the sale money to the balance and raise any residual to the next decision**, so that **assets sell sooner at approved prices** (legacy RWB-E4-030, word for word).

This is the application slice of legacy RWB-E4-030. It owns:

- the four legacy criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one proceeds-and-shortfall branch of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, a stage child of the case workflow (Architecture v5 slides 13 and 19);
- the consumption of EV-25 `ProceedsMatched` on `rwb.payment.events.v1` through an inbox and a consumer group of this service;
- the evaluation of R-DIS-54 on a sold asset and then R-DIS-55 on the residual of the case, with the DISPOSAL package version in force;
- the write of the sale outcome on `asset_sale` in schema `rwb_asset`, including the `gain_loss` formula element, and the record of the residual where the sources allow (GAP-2947; ASM-4843);
- the local decision record of each rule outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03);
- the answers to rwb-case for the case moves `PROCEEDS_APPLIED` and `SHORTFALL_RAISED`, with the rule and the version that produced them;
- the two reads behind SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two reads, the consumed rows, the subscription, the case-move answer, the decision-record element, the error set and the fakes, which are RWB-S5-E4030-CON; the sale, the award, the payment term and the title transfer, which are FEAT-AST-18 to FEAT-AST-20's stories; the application of the money to the loan account and its posting, which are FEAT-PAY-10 of rwb-payment (P8) (GAP-2948; ASM-4844); the case of record, the states `ASSET_SOLD`, `PROCEEDS_APPLIED` and `SHORTFALL_RAISED`, the parent `CaseWorkflow` and the stage timers, which are rwb-case's (P3); the D9 decision and the residual routing to write-off or debt sale, which are R-DIS-57 and R-DIS-58 of the write-off route (S7) (GAP-2950; ASM-4846); the account and NPA-sale facts of ACE, which are rwb-source-data's (P1); the rule package and its version, which are rwb-decision's (P7); and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E4-030 was the step between a completed asset sale and the next decision: the sale money was applied, any residual was raised, and the case moved on instead of stalling between the auction platform, finance and the write-off desk. The FSD keeps the feature as FEAT-AST-21 "Apply proceeds and raise the shortfall" in module S5, run unattended, with FEAT-PAY-10 of P8 as its prerequisite (FSD S5 A2.21.2; Epics 3 to 8 Specification v3, E4 row FEAT-AST-21).

What D-RCV-60 changes is who owns the sale outcome, the money and the case.

- **The sale outcome is this service's.** `asset_sale` carries the sale, its price, its fees and its `gain_loss` formula (DF-SAL-009 to DF-SAL-019) in `rwb_asset`, and the sale row is written here and nowhere else (Ownership Map; TSD S5 T3.1).
- **The money stays with rwb-payment (P8).** `proceeds` is P8's row (Ownership Map, table `proceeds` owner P8), the application to the balance is FEAT-PAY-10, and the loan-account and GL posting is P8's. This story reads the proceeds fact on the owner's boundary and consumes the owner's event; it never posts (GAP-2948; ASM-4844).
- **The case of record stays with rwb-case (P3).** `recovery_case` and its states are P3's; this story evaluates, writes the sale outcome, records the decision and **answers** the move.
- **The ACE facts stay with rwb-source-data (P1).** The legacy data table names `v_ace_account` and `v_ace_npa_sale`; in the target the 30 `recovery.v_ace_*` views are read only by rwb-source-data, so DP-05 applies as a prohibition and both facts arrive on the owner's data product (GAP-2946; ASM-4842).
- **The decision is recorded first**, one record per outcome, in the transaction of the sale row: that is what AC1 asked for and AC4 tested.

The metric of the feature is the review of applied proceeds and raised residuals, so no business value moves: the residual is derived from the proceeds fact, the sale record and the rule package, each read with its version and never written in code.

### 3. Preconditions

- RWB-S5-E4030-CON is published: the two reads, the consumed rows, the `ProceedsMatched` subscription with its consumer group and inbox, the decision-record element, the error set and the fakes are baselined and tagged.
- EV-25 `ProceedsMatched` is published by rwb-payment on `rwb.payment.events.v1` with a CloudEvents envelope, an event id, an idempotency key and the retry and `.dlt` topics, and its fake can emit the same fact twice (Template and Rules v1 §R4; Event and Messaging Design v5, EV-25).
- The rwb-payment proceeds-fact activity and the rwb-case case-state read and case-move answer are behind fakes; no source publishes their operation names (GAP-2944; ASM-4840).
- The rwb-source-data data product that carries the account balance and the NPA sale facts is published with its fake; the legacy `v_ace_account` and `v_ace_npa_sale` rows are not read here (GAP-2946; ASM-4842).
- The DISPOSAL package is in force at its version with R-DIS-54 and R-DIS-55, loaded through the service template; DP-04 is outside the pattern set of this story (GAP-2953; ASM-4849).
- `asset_sale` exists in `rwb_asset` with the TSD S5 T3.1 columns including `gain_loss`; no column holds the residual and none is added (GAP-2947; ASM-4843).
- The lists `LOV-HOLDING`, `LOV-LISTING`, `LOV-SALE-CHANNEL` and `LOV-SEGMENT` are reference data with their version (TSD S5 T3.2).
- RWB-PLT-E1027-CON writes in the caller's transaction and a failed write stops the action (DP-03); RWB-PLT-N001-CON serves SCR-21 and SCR-22, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass (ASM-4850).

### 4. Flow

1. The sale is agreed and settled; the asset is `ASSET_SOLD` and rwb-case holds the state. The proceeds fact arrives as EV-25 `ProceedsMatched` on `rwb.payment.events.v1`, read by the inbox of this service and handed to `AssetDisposalWorkflow` as a signal.
2. The workflow confirms the case state and the sale on the rwb-case contract and on `asset_sale`, then runs the `applyProceeds` activity: receive, evaluate, record, apply, answer.
3. `ProceedsEvaluator` loads the DISPOSAL package in force and evaluates R-DIS-54 from `ASSET_SOLD` on `PROCEEDS_POSTED`: the sale outcome is applied to the case side, the vendor fee is matched from the proceeds fact and the case moves to `PROCEEDS_APPLIED`.
4. `AssetDecisionRecordWriter` writes one record, with the rule id and the package version, **before any row changes**; a failed write stops the activity and the message is MSG-P7-003 (DP-03; AC1, AC4).
5. `SaleOutcomeWriter` writes the settled sale in one transaction with the record and the idempotency row: the price, the fee, `gain_loss` and the standard columns of `asset_sale`; the optimistic lock `version` is checked.
6. `CaseMoveAnswer` answers `PROCEEDS_APPLIED` with the sale, the proceeds reference and the rule version; rwb-case applies the state (GAP-2944; ASM-4840).
7. `ShortfallEvaluator` then evaluates R-DIS-55 from `PROCEEDS_APPLIED` on `SHORTFALL_CALCULATED` with `shortfall_amount above 0`: the residual is raised for the D9 decision.
8. A second record is written, the residual is held with the sale outcome where the sources allow and is Not specified in the source documents elsewhere (GAP-2947; ASM-4843), and `CaseMoveAnswer` answers `SHORTFALL_RAISED`.
9. Where the residual is at or below zero, R-DIS-56 is not this story's: the answer carries the computed `shortfall_amount` and the no-shortfall close is the adjacent step (GAP-2950; ASM-4846).
10. A repeated event or key writes once and is counted; a case in another state does not fire the rule and the state is reported. The workflow returns to its durable timer and continues as new at each stage end and at least every 28 days.
11. The sale officer reads the result on SCR-22 Asset record through the gateway-bff route: the sale, its price, the fee, the proceeds state and the residual (DP-13, DP-19).

Screen states: SCR-21 shows empty, error and no access states; SCR-22 shows empty, loading, error and no access states. The no access state is the 403 of §12.1 (MSG-P4-002); the empty and error messages are Not specified in the source documents (DOR-RWB-S5-E4030-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered, the sale and the residual unchanged | MSG-P7-003 | AC4, TC-E4-030-04, TC-E4-030-06 |
| X2 | The role lacks the Asset and disposal right on a read | 403 before any read | MSG-P4-002 | AC1, TC-E4-030-05 |
| X3 | The case is not in `ASSET_SOLD` or `PROCEEDS_APPLIED` | The rule does not fire, nothing written, the state reported | None | AC2, AC3 |
| X4 | The event does not reach the workflow inside the budget | The inbox retries, then the retry topic and the `.dlt` topic; the case waits at `ASSET_SOLD` | None (platform log) | AC1, AC3 |
| X5 | The same event id or idempotency key arrives twice | One sale outcome, one record, one answer; the repeat is counted | None | AC1 |
| X6 | The proceeds fact is missing, stale or carries no sale | The step does not fire; the data product date is shown | MSG-P1-001 family | AC3 |
| X7 | The vendor fee has no match on the proceeds fact | The match is held and named on the case task; the sale outcome is not reversed | None | AC3, GAP-2949 |
| X8 | A contract misses 2 s or its breaker is open | The activity retries on the workflow schedule; 503 in the platform envelope | None | AC1, AC2 |
| X9 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | AC5, TC-E4-030-09, TC-E4-030-19 |
| X10 | The residual routes nowhere because `residual_route` is unset | The case is held in `UNMATCHED_EXCEPTION` by R-DIS-71, which is the adjacent step and not owned here | MSG-GEN-001 on the task | AC6, TC-E4-030-10, TC-E4-030-20 |

X1 to X3 are the legacy paths on the split; X4 to X8 are what the subscription, the boundaries and the fee match add; X9 is the DP-01 and DP-05 boundary; X10 is the adjacent rule the feature names; AC6 covers only its hand-off and does not own the route.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the fakes; no live P1, P3 or P8 |
| Negotiable | The activity name, the record shape and the fixture data are ours; rules, messages, screens, rows and reads are fixed |
| Valuable | A settled sale reaches its next decision the same day and the residual is raised without a manual reconciliation |
| Estimable | One branch, two evaluators, one record per outcome, two row changes, two answers, three clients, one screen fragment |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases, plus the access, wrong-state, repeat, stale-proceeds and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Apply proceeds and raise the shortfall

  Background:
    Given case "RC-2026-000593" holds asset "AST-2026-000593" with sale record "AS-2026-000593"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-54 and R-DIS-55
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Apply proceeds and raise the shortfall (legacy RWB-E4-030 AC1)
    Given the rwb-payment contract mock returns ProceedsMatched for case "RC-2026-000593" with its proceeds fact and no unmatched vendor fee
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then applies the sale money to the balance and raises any residual to the next decision
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-55 (legacy RWB-E4-030 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000593" in state PROCEEDS_APPLIED
    Given a case in state PROCEEDS_APPLIED
    When shortfall calculated
    Then raise the residual for the D9 decision
    Then the case moves to SHORTFALL_RAISED

  Scenario: AC3 Rule R-DIS-54 (legacy RWB-E4-030 AC3)
    Given the rwb-case contract mock returns the case "RC-2026-000593" in state ASSET_SOLD
    Given the rwb-payment contract mock returns the proceeds of "AS-2026-000593" with its vendor fee matched
    Given a case in state ASSET_SOLD
    When proceeds posted
    Then apply the proceeds to the case and the loan account, and match the vendor fee
    Then the case moves to PROCEEDS_APPLIED

  Scenario: AC4 Not recorded (legacy RWB-E4-030 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Boundary refuses a statement outside the owned schema (X9; DP-01, DP-05) (new, D-RCV-60)
    Given a statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails

  Scenario: AC6 Residual with no route is answered and not routed (X10) (new, D-RCV-60)
    Given the case "RC-2026-000593" is in state SHORTFALL_RAISED with residual_route unset
    When the residual is answered to rwb-case
    Then the answer carries the shortfall_amount and no route
    Then the hold in UNMATCHED_EXCEPTION is the adjacent step's R-DIS-71 and is not claimed here

  Scenario: AC7 Sale outcome is written and the money is not (BR1, BR3) (new, D-RCV-60)
    Given the rwb-payment contract mock returns ProceedsMatched for case "RC-2026-000593" with its proceeds fact
    When the sale outcome is recorded
    Then asset_sale holds the price, the fee and gain_loss
    Then no balance, posting or proceeds row is written by this story

  Scenario: AC8 Case move is answered and not written (BR4) (new, D-RCV-60)
    Given the case "RC-2026-000593" is in state PROCEEDS_APPLIED
    When the move is answered to rwb-case
    Then the answer carries the outcome and the residual, and no state is written here

  Scenario: AC9 One event is consumed and a repeat is counted (BR8, BR9) (new, D-RCV-60)
    Given ProceedsMatched for case "RC-2026-000593" arrives twice with the same event id
    When the second delivery is processed
    Then one sale outcome and one answer are written, the repeat is counted, and no event is published

  Scenario: AC10 Activity retry and timeout write one outcome (new, D-RCV-60)
    Given the applyProceeds activity for case "RC-2026-000593" times out and is retried
    When the retried activity completes
    Then one sale outcome and one answer are written and the timed-out attempt writes no second row

  Scenario: AC11 A consumed call fails or does not answer (X8) (new, D-RCV-60)
    Given a consumed contract call for case "RC-2026-000593" fails or does not answer within the budget
    When the call is made
    Then the activity retries on the workflow schedule and the answer is 503 in the platform envelope

  Scenario: AC12 A status change the model does not allow is refused (X3) (new, D-RCV-60)
    Given the case "RC-2026-000593" is in state ASSET_SOLD with a shortfall_amount above 0
    When R-DIS-55 is evaluated
    Then the rule does not fire, nothing is written, and the state is reported



  Scenario: AC13 Each business rule of section 8 holds (BR1 to BR10) (new, D-RCV-60)
    Given the rwb-payment contract mock returns ProceedsMatched for case "RC-2026-000593" with its proceeds fact
    When the sale outcome is processed
    Then the outcomes of BR1 to BR10 hold as their rows in section 8 state

  Scenario: AC14 Error answers of the provided operations (401, 403, 404) (new, D-RCV-60)
    Given a request is made to each provided operation of section 12.1
    When the request has no valid login, a role without the Asset and disposal right, or an unknown path
    Then the answer is 401, 403 or 404 respectively, in the platform envelope, and a 403 carries MSG-P4-002

```

The four criteria are the legacy criteria word for word with the origin tag added: the repeated `Then`, `its trigger arrives`, `shortfall calculated`, `proceeds posted` and `the action is taken` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-case writes the two moves, rwb-payment posts the money and answers the fact, and this story evaluates the two rules, writes the sale outcome, records the decision and answers. AC3's "apply the proceeds to the case and the loan account" is FEAT-PAY-10 of rwb-payment; this story applies the case side and answers the move (GAP-2948; ASM-4844). The vendor fee's match is read from the proceeds fact: the fee is matched against transfer_fee and recorded as the rule outcome, and an unmatched fee is held on the case task without reversing the sale (GAP-2949; ASM-4845). AC5 to AC10 carry no legacy tag: AC5 is the boundary of X9, AC6 the residual hand-off of X10, AC7 to AC9 the business rules BR1, BR3, BR4, BR8 and BR9 of section 8, and AC10 the retry and timeout of the activity. R-DIS-56, R-DIS-57, R-DIS-58, R-DIS-71 and R-DIS-72 own no criterion here; the no-shortfall close, the residual routing and the unmatched exception are not covered by this story (GAP-2950; ASM-4846).

### 8. Business rules

| Rule ID | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-54 | Asset disposal | D8.1 to D8.3 | ASSET_SOLD | PROCEEDS_POSTED | Any | Apply the proceeds to the case and the loan account, and match the vendor fee | PROCEEDS_APPLIED | Workbench | ALS core and GL, Agent Runtime | same day |
| R-DIS-55 | Asset disposal | D8.1 to D8.3 | PROCEEDS_APPLIED | SHORTFALL_CALCULATED | shortfall_amount above 0 | Raise the residual for the D9 decision | SHORTFALL_RAISED | Write-off team | Rules component | None |

Both rows are copied character for character from the Business Rules and Routing Logic v4 and carry the BR IDs BR11 (R-DIS-54) and BR12 (R-DIS-55) in the table below. Their owner column is a business role, so the case stays in these states and moves in rwb-case on this story's answer, while `asset_sale` is written here. R-DIS-56 (no shortfall), R-DIS-57 and R-DIS-58 (residual to write-off or debt sale), R-DIS-71 and R-DIS-72 (residual route unset, manual decision) are named by FSD S5 A2.21 but carried by no legacy criterion, so they are adjacent and not owned (GAP-2950; ASM-4846). The "Agent Runtime" system of R-DIS-54 is not claimed: DP-20 is outside the pattern set (GAP-2948).

| ID | Rule | Source |
|---|---|---|
| BR1 | The sale outcome is this service's: `asset_sale` in `rwb_asset`, with the price, the fee and `gain_loss` | Ownership Map; TSD S5 T3.1; AC7, TC-E4-030-11 |
| BR2 | The record precedes the change, one per outcome, with the rule and package version; a failed write changes nothing | DP-03; AC1, AC4; TC-E4-030-04, TC-E4-030-06 |
| BR3 | The money is P8's: no balance application, no posting and no `proceeds` row is written here | Ownership Map (`proceeds`, P8); GAP-2948; GAP-1759; AC7, TC-E4-030-11 |
| BR4 | The case move is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2944; AC8, TC-E4-030-12 |
| BR5 | No element holds the residual: it is recorded with the decision outcome and answered to rwb-case, and no column is invented | GAP-2947; ASM-4843; GAP-1912; AC6, TC-E4-030-10 |
| BR6 | The vendor fee is matched from the proceeds fact; a missing match is named on the task and does not reverse the sale | GAP-2949; ASM-4845; GAP-1912; AC3, TC-E4-030-14 |
| BR7 | ACE data only through the owner's contract: no `v_ace_account` and no `v_ace_npa_sale` read here | DP-05; GAP-2946; AC5, TC-E4-030-09 |
| BR8 | One event is consumed and none is published; EV-22 `AssetTakenOn` and the sale event belong to other stories | Event and Messaging Design v5 (EV-22, EV-25); GAP-2945; AC9, TC-E4-030-13 |
| BR9 | A repeated event id or key writes once, answers once and is counted | Event and Messaging Design v5 (Duplicates, R-UNI-40); AC9, TC-E4-030-13 |
| BR10 | No cross-schema join and no foreign key leaves `rwb_asset`; no personal data in a row, a record, a log or a workflow input | DP-01; Template and Rules v1 §R7.2 (s17); AC5, TC-E4-030-09 |
| BR11 | Rule row R-DIS-54 above: the proceeds are applied to the case and the loan account and the vendor fee is matched, from ASSET_SOLD to PROCEEDS_APPLIED | Business Rules and Routing Logic v4; AC3, TC-E4-030-14 |
| BR12 | Rule row R-DIS-55 above: a shortfall above 0 raises the residual for the D9 decision, from PROCEEDS_APPLIED to SHORTFALL_RAISED | Business Rules and Routing Logic v4; AC2, TC-E4-030-15 |

### 9. State transitions

The case state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR4).

| From (case state) | Event | Condition | To |
|---|---|---|---|
| ASSET_SOLD | `PROCEEDS_POSTED` under R-DIS-54 | Any | PROCEEDS_APPLIED, answer `PROCEEDS_APPLIED` |
| PROCEEDS_APPLIED | `SHORTFALL_CALCULATED` under R-DIS-55 | `shortfall_amount` above 0 | SHORTFALL_RAISED, answer `SHORTFALL_RAISED` |
| PROCEEDS_APPLIED | `NO_SHORTFALL` under R-DIS-56 | `shortfall_amount` at or below 0 | CASE_CLOSED_NO_SHORTFALL, adjacent and not owned (GAP-2950) |
| SHORTFALL_RAISED | `RESIDUAL_ROUTED` under R-DIS-57 or R-DIS-58 | `residual_route` is write_off or debt_sale | TO_WRITEOFF or TO_DEBT_SALE, adjacent (GAP-2950) |
| SHORTFALL_RAISED | `RESIDUAL_ROUTED` under R-DIS-71 | `residual_route` is not set | UNMATCHED_EXCEPTION, adjacent (GAP-2950) |
| Any | Another state, a repeated event or a stale proceeds fact | X3, X5, X6 | Unchanged |

| `asset_sale` state | Event | Condition | To |
|---|---|---|---|
| Settled at the sale | The proceeds fact arrives | R-DIS-54 fires | Settled, proceeds applied, fee matched |
| Settled, proceeds applied | The residual is above 0 | R-DIS-55 fires | Settled, residual raised |
| Any | The record fails or the fact is stale | X1, X6 | Unchanged |

The case states are the DISPOSAL machine's (TSD S5 T4); the sale's columns are the TSD S5 T3.1 elements, and the screen states are read as the `LOV-HOLDING` and `LOV-LISTING` rows of T3.2 (GAP-2952; ASM-4848).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, RW-TEAMMGR, RW-NPAMGR | Asset and disposal R: read the sale, the proceeds state and the residual on SCR-21 and SCR-22 |
| RW-CASEOWN, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-ENFORCE and the further roles of the read row | Asset and disposal R, in scope (legacy permission table) |
| RW-HEADNPA, RW-HEADASL, RW-PRODHEAD | Asset and disposal R, with the residual in view |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal R on their own sales |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the branch; no grant on another schema and no `v_ace_*` grant |

The rights are the rows of the legacy permission table and TSD S5 T6.1, nothing wider; the step itself runs unattended and its only acting role is the read. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability. The rwb-access authorise check of each read operation is Not specified in the source documents (DOR-RWB-S5-E4030-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, gain_loss, incentive_amount | Write: the settled sale, the fee, `gain_loss` |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | sale_channel, start_price, floor_price, round_no, listed_at, status | Read: the listing of the sale |
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | asset_ref, asset_type, book_value, holding_status and 11 more | Read: the asset of the sale |
| Standard columns | asset_sale, listing (S5, `rwb_asset`) | state, version, is_active, created_at/by, updated_at/by | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| Not specified in the source documents (GAP-2947; ASM-4843; GAP-1912) | none | the residual, its route and its D9 hand-off | No element; recorded with the outcome and answered to rwb-case |
| DF-FIN-001 to DF-FIN-009 | proceeds (P8) | id, case_id, treatment_id, payment_code, source, amount and 3 more | Not written: read as the proceeds fact (BR3) |
| DF-ACE-001 to DF-ACE-042 | `v_ace_account` (P1) | account_key, account_code, total_balance and 39 more | Not read: rwb-source-data product (BR7) |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, sale_date, sale_price, transfer_fee and 7 more | Not read: rwb-source-data product (BR7) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 19 more | Not read as a table: rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read: rwb-decision package |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no column, no migration**: the tables come with the DB story, a residual column missing from `asset_sale` is added there in its own Flyway sequence (GAP-1912), and `decision_record`, `idempotency_key` and `inbox` are library objects in `rwb_asset`. **No personal data**: identifiers, codes, amounts, dates and a rule version only; every fixture is synthetic. Reference data is read only as the DISPOSAL package in force: the rule rows DF-REF-001 to DF-REF-015 through the rwb-decision package contract (DP-06, DP-07), with the parameters package version and the shortfall threshold of 0 in R-DIS-55 (DOR-RWB-S5-E4030-APP-20).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4030-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the sale and the proceeds state of each asset (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its sale, its fee, its proceeds state and its residual (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |

No write operation is provided: the step runs unattended and its writes belong to the `applyProceeds` activity inside the workflow. `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` are the pricing, listing and round stories' and are not changed here; the `{assetKey}` read variants of the Ownership Map are not declared in this slice. Errors: 400 with Not specified in the source documents (CG-ALL-10182), 401 with Not specified in the source documents (CG-ALL-10182), 403 with MSG-P4-002, 404 with Not specified in the source documents (CG-ALL-10182), 422 with MSG-GEN-001, 503 with Not specified in the source documents (CG-ALL-10182) when a library or a contract does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (Temporal activity on queue `rwb-case`) | `/api/recovery/case/v1` | P3 rwb-case | The case state before a rule fires; faked |
| Case-move answer (name Not specified in the source documents (GAP-2944; ASM-4840)) | rwb-case (P3), Temporal | P3 rwb-case | `PROCEEDS_APPLIED` and `SHORTFALL_RAISED` with the rule and its version; faked |
| Proceeds-fact activity (name Not specified in the source documents (GAP-2944; ASM-4840)) | queue `rwb-payment` | P8 rwb-payment | The proceeds, the vendor fee and the balance state, in place of the legacy `v_ace_account` read; faked |
| Account and NPA-sale data product (name Not specified in the source documents (GAP-2946; ASM-4842)) | rwb-source-data (P1) | P1 rwb-source-data | The account balance and the NPA sale facts, in place of the legacy `v_ace_account` and `v_ace_npa_sale` reads; faked |

One hop or one activity, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). The plan carries no C row and no I row for this pair, because the legacy "Depends on FEAT-PAY-10" is a consumed contract and not a build gate; the wave 3 harness holds the real journey (GAP-2944; ASM-4840).

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's and the sale event belongs to the sale and auction stories; this step writes no outbox row and adds nothing to `rwb.asset.events.v1`. Its outward surface is the case-move answer and its own reads. A build that publishes here fails the absence test.

#### 12.4 Events consumed

| Event | Topic | Envelope | Subscription | Idempotency | Owner |
|---|---|---|---|---|---|
| EV-25 `ProceedsMatched` (proceedsId, caseId, amount) | `rwb.payment.events.v1`, event `rwb.payment.ProceedsMatched.v1`, with `.retry` and `.dlt` | CloudEvents, schema version, event id, correlation reference | Consumer group `rwb-asset`, inbox row in `rwb_asset`, then a signal to `AssetDisposalWorkflow` | Event id and idempotency key; a repeat is ignored and counted (BR9) | rwb-payment (P8) |

EV-25 stands as published by Payments and posting with "Case and workflow" as its only named consumer, while Architecture v5 slide 13 gives S5 an event subscription to P8; the catalogue slide wins under R-PREC and the subscription is declared here (GAP-2945; ASM-4841). No other topic is consumed: the litigation events of the matrix's S4 column serve other steps of this service. The operation names of the rwb-payment proceeds and vendor-fee read, the rwb-case case-move answer and the rwb-source-data account and sale data product are Not specified in the source documents (GAP-1911); each owner publishes its name before the wave 3 tag, and RWB-S5-E4030-CON replaces the placeholder in a minor version.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new across the holding | `rwb-asset` | Input: case, route, asset, sale, package in force; signals: `ProceedsMatched`, residual computed, package in force |
| `applyProceeds` | Activity, the one step of this slice | `rwb-asset` | The case, the sale and the proceeds fact in; rule IDs with versions, the sale outcome, the residual and the case move out, in one transaction |

No child workflow and no second queue. The activity name is a design choice of this story; the two boundary activities run on the owners' queues. The three boundary rows (case move, proceeds fact and source-data product) are consumed contracts, built on day one against their documents and fakes; their operation names are Not specified in the source documents (GAP-2944), and the plan C list stays empty. The balance and NPA sale facts are read from rwb-source-data or from the rwb-case case view; no v_ace_* grant sits in rwb_asset (GAP-2946). The residual is held as the outcome of the R-DIS-55 decision record and as the stage outcome answered to rwb-case, computed from the proceeds fact, the sale record and the rule rows with their versions; no column is added in this wave (GAP-2947). rwb-payment applies the receipt to the balance and posts it; rwb-asset evaluates the case side of R-DIS-54 and writes the sale outcome; the vendor fee is matched as a fact of the proceeds row; no agent call is made in this wave (GAP-2948). The inbox and the outbox are platform capabilities of the event platform, and the DISPOSAL package is loaded through the service template; no new H row is claimed in this wave (GAP-2953). The sale is published as AssetSold on rwb.asset.events.v1, a CloudEvent keyed by asset and case; its EV number is Not specified in the source documents (GAP-1753).

Workflow ID form: Not specified in the source documents (CG-ALL-10184). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-10184).

#### 12.6 Schedules

None. The step is event-started; it owns no Temporal Schedule and no Quartz job. The single Schedule of the service is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The settled sale, its price, its fee and `gain_loss`; written here |
| listing | S5 (`rwb_asset`) | Read for the channel and the price of the sale |
| asset | S5 (`rwb_asset`) | Read for the asset of the sale |
| decision_record | PLT library in `rwb_asset` | One record per outcome (DP-03) |
| idempotency_key, inbox | PLT library in `rwb_asset` | The dedupe of the event and the key (GAP-2953; ASM-4849) |

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `proceeds` (P8), `decision_log_entry`, `rule_row`, `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8), every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | `ASSET_SOLD` and `PROCEEDS_APPLIED` for the fixture cases; a case in another state | AC2, AC3, X3 |
| rwb-case move fake | The two moves accepted; a move refused for an unexpected state | AC1 to AC3 |
| rwb-payment proceeds-fact fake | A posted sale with its fee matched; a fee with no match; a stale fact; no answer inside 2 s | AC1, AC3, X6, X7 |
| rwb-payment `ProceedsMatched` fake | One event, the same event id twice, an event with no sale, an event past the retry budget | AC1, X4, X5 |
| rwb-source-data data-product fake | The account balance and the NPA sale of the fixture cases; a stale business date | AC3, X6 |
| rwb-decision package fake | The DISPOSAL package at its version with R-DIS-54 and R-DIS-55 | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Composite route fake | The merged SCR-21 and SCR-22 answer for `RC-2026-000593` | AC1 |

The fakes are test-only; the placeholder rows carry their gap until their owners confirm the names (GAP-2944; ASM-4840).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two asset reads on `/api/recovery/asset/v1`; the case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 1 consumed | EV-25 `ProceedsMatched` on `rwb.payment.events.v1` through the inbox of `rwb-asset`, with retry and `.dlt` |
| Temporal | 1 workflow, 1 activity owned, 2 consumed | `AssetDisposalWorkflow` and `applyProceeds` on `rwb-asset`; the proceeds-fact activity on `rwb-payment` and the case activity on `rwb-case`; no Schedule |
| File | None | No file element; the sale's papers belong to the document hub |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.proceeds`; front end `src/modules/recovery/asset/SaleOutcome.tsx`, the fragment SCR-22 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition here: the legacy `v_ace_account` and `v_ace_npa_sale` reads leave the service for the rwb-source-data product and no `v_ace_*` grant is kept. DP-03 is the transaction rule of the sale write, DP-13 moves the base and DP-19 is how the screens reach the service. The subscription's inbox and the package load are platform capabilities and claim no new H row (GAP-2953; ASM-4849).

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` proceeds branch | Workflow | Waits on the event and the timer, loads the package in force, reports to the parent |
| `applyProceeds` | Activity | The one step: receive, evaluate, record, write, answer |
| `ProceedsEvaluator` | Service | R-DIS-54 on the sale, the proceeds fact and the fee |
| `ShortfallEvaluator` | Service | R-DIS-55 on `shortfall_amount`; reports the no-shortfall branch without claiming it |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per outcome before any change (DP-03) |
| `SaleOutcomeWriter` | Repository | `asset_sale` in one transaction with the record, the inbox row and the lock |
| `ProceedsEventConsumer` | Listener | The inbox row, the dedupe, the retry and `.dlt` hand-off, then the signal |
| `CaseMoveAnswer`, `CaseStateClient`, `ProceedsFactActivity`, `SourceDataProductClient` | Clients | The two answers and the boundary calls, one hop, 2 s |
| `AssetSaleController` | Controller | The two reads, the rights and the 400/401/403/404/422/503 map |
| `SaleOutcome` | React component | The sale, its fee, the proceeds state and the residual on SCR-22, read only |

**Database.** No Flyway file: the tables come with the DB story and the library objects with the library's migration; no residual column is added (GAP-2947).

**Configuration.** The DISPOSAL package and its version from rwb-decision; the lists at their version (TSD S5 T3.2); the capability rows from rwb-access; the consumer group, the retry and `.dlt` topics and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the branch and its input record; (2) `ProceedsEventConsumer` with the inbox and the dedupe (AC1, X4, X5); (3) `ProceedsEvaluator` with R-DIS-54 (AC3, X3); (4) `ShortfallEvaluator` with R-DIS-55 and the no-shortfall report (AC2); (5) the record writer against the stub (AC1, AC4, X1); (6) `SaleOutcomeWriter` with the lock and the fee match (AC3, X7); (7) `CaseMoveAnswer` and the case-state client (AC2, AC3); (8) the two boundary clients against their fakes (AC3, X6); (9) `AssetSaleController` with the rights and the error map (AC1, X2); (10) the screen fragment through the route fake; (11) the boundary test (X9, BR7, BR8).

**Feature flag.** `rwb.asset.proceeds-v1`; off means the event stays in the inbox, nothing is written and no move is answered.

**Done when.** §16 passes, an applied sale moves the case to `PROCEEDS_APPLIED` and records its outcome in SIT, an above-zero residual answers `SHORTFALL_RAISED`, a repeat writes once, a forced record failure changes nothing, no case row and no `v_ace_*` read exists, and SCR-21 and SCR-22 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | A sale price or a floor under the approver's limit is read at the step | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | The appraisal behind the price is more than a year old | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required element of the event, the request or the signal is absent (X3, X10) | Enter {field}. |
| MSG-P4-002 | A role without the right reads the sale (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the sale changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The proceeds fact is missing, stale or carries no sale (X6) | Not specified in the source documents (DOR-RWB-S5-E4030-APP-9) |

The five IDs are the legacy set, copied unchanged; no message is reworded. The stale-data message MSG-P1-001 is the data product's and is shown with its own ID (X6); its text is Not specified in the source documents (DOR-RWB-S5-E4030-APP-9).

### 15. Screens and states

SCR-21 Asset list (loading; list; empty, error and no access: Not specified in the source documents (CG-ALL-10189)) and SCR-22 Asset record (take-on; held; listed; sold; empty, loading, error and no access: Not specified in the source documents (CG-ALL-10190)) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, the sale, the fee and the residual, rwb-case for the state and rwb-payment for the proceeds. This story fixes the rwb-asset answers only; the route and the field list are RWB-PLT-N001-CON.

The states it produces are the sale state of SCR-22 — settled, proceeds applied, fee matched, residual raised — and the refused, not-recorded, wrong-state and stale-proceeds states with MSG-P4-002, MSG-P7-003, MSG-GEN-001 and the data product's message. The legacy states "take-on", "held", "listed" and "sold" do not all correspond to a `LOV-HOLDING` value, and `PROCEEDS_APPLIED` and `SHORTFALL_RAISED` are case states rather than holding states; the screen shows the holding state from LOV-HOLDING and the case state beside it; take-on is read as the ASSET_ON_BOOKS and ASSET_HELD pair, and the legacy wording stays as the business description of the screen (GAP-2952; ASM-4848).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-030-01 | AC1 | Component | Case `RC-2026-000593` with a settled sale; the event, the record, the sale outcome and the two answers on the fakes |
| TC-E4-030-02 | AC2 | Component | Case at `PROCEEDS_APPLIED` with a residual above 0; R-DIS-55 fires, the record is written and `SHORTFALL_RAISED` is answered |
| TC-E4-030-03 | AC3 | Integration | Case at `ASSET_SOLD` with a posted sale; R-DIS-54 fires across the rwb-payment and rwb-case fakes, the fee is matched and `PROCEEDS_APPLIED` is answered |
| TC-E4-030-04 | AC4 | Component | Record stub stopped; nothing written, no move answered, MSG-P7-003 shown |
| TC-E4-030-05 | Access | Component | A role without the right; 403 with MSG-P4-002, no read |
| TC-E4-030-06 | Principle 5 | Component | A forced record failure at the sale write; no row, no answer, no event |
| TC-E4-030-07 | §12 contract (12.1, 12.5) | Contract | Each REST operation of §12.1, the `applyProceeds` activity and the `ProceedsMatched` signal checked against the RWB-S5-E4030-CON shapes; no write operation exposed |
| TC-E4-030-08 | §12.7 tables | Component | Boundary values on the owned tables of §12.7 (ASM-3438): asset_sale, listing, asset, decision_record, idempotency_key, inbox; no read of a table not owned |
| TC-E4-030-09 | AC5 (X9; BR7, BR10) | Component | A statement on a v_ace_* view, recovery_case or a foreign schema is refused by the grant and fails the build |
| TC-E4-030-10 | AC6 (X10; BR5) | Component | A residual with residual_route unset is answered to rwb-case with the shortfall_amount and no route |
| TC-E4-030-11 | AC7 (BR1, BR3) | Component | The sale outcome is written in asset_sale and no balance, posting or proceeds row is written by this service |
| TC-E4-030-12 | AC8 (BR4) | Component | The case move is answered and no case state is written in rwb-asset |
| TC-E4-030-13 | AC9 (BR8, BR9) | Component | One event is consumed, none is published, and a repeat is counted and writes once |
| TC-E4-030-14 | AC3 (BR6, BR11) | Component | The vendor fee is matched from the proceeds fact and a missing match is named without reversing the sale |
| TC-E4-030-15 | AC2 (BR12) | Component | A shortfall above 0 raises the residual and moves the case to SHORTFALL_RAISED |
| TC-E4-030-16 | AC10 (no legacy tag) | Component | Case `RC-2026-000593` with the applyProceeds activity timed out and retried; one sale outcome and one answer on the fakes |
| TC-E4-030-17 | AC11 (X8) | Component | Case `RC-2026-000593` with a consumed contract call that fails or does not answer; retry on the workflow schedule and 503 on the fakes |
| TC-E4-030-18 | AC12 (X3) | Component | Case `RC-2026-000593` at `ASSET_SOLD` with a shortfall_amount above 0; R-DIS-55 does not fire, nothing written, state reported |
| TC-E4-030-19 | AC5 (X9; BR7, BR10) | Component | A statement on a v_ace_* view, recovery_case or a foreign schema; grant refuses it, build fails, pipeline log records it |
| TC-E4-030-20 | AC6 (X10; BR5) | Component | Case `RC-2026-000593` at `SHORTFALL_RAISED` with residual_route unset; no route written and MSG-GEN-001 on the task |
| TC-E4-030-21 | AC13 (BR1 to BR10) | Component | Case `RC-2026-000593` with a posted sale; each rule row of section 8 holds on the fakes |
| TC-E4-030-22 | AC14 (401, 403, 404) | Component | Each provided operation of section 12.1 called with no login, with a role lacking the right, and with an unknown path; 401, 403 with MSG-P4-002, 404 |
| TC-E4-030-23 | AC9 (X5; BR9) | Component | ProceedsMatched for case `RC-2026-000593` redelivered with the same idempotency key; one outcome, one answer, repeat counted |

The six legacy cases keep their order with the Level column added; TC-E4-030-07 and -08 are added for the §12 contract and the §12.7 boundary: TC-E4-030-03 runs `Integration` because it crosses two boundaries, the rest `Component` on their fakes. The full text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness, which carries the real payment and source-data calls.

### 17. Guardrails

- No business value in code: the package, its version, the fee, the lists and every threshold stay rule rows or reference data with a version.
- No personal data in the schema, a workflow input, an event or a log; a buyer is a code, the sale is an asset and every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant and no ACE read (DP-05, BR7; AC5).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case` row and no `proceeds` row here (BR3, BR4).
- No ALS interface and no general-ledger interface here: every posting goes to rwb-payment through `postProceeds`, the cost of carry travels with its period, and the result is recorded from `ProceedsMatched` (GAP-1759).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base, no data-lake export of a sale.
- The record precedes the change and a repeated event is deduped (DP-03, BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| No requirement id for this slice | FEAT-AST-21 of FSD S5 A2.21 and the epic BRD row for it: the sale money is applied and any residual is raised to the next decision (GAP-2951; ASM-4847) | The proceeds branch, the sale write, the two answers | TC-E4-030-01 to -03 | FEAT-AST-21 | Not specified in the source documents (DOR-RWB-S5-E4030-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-asset owns the sale outcome | TC-E4-030-01 | FEAT-AST-21 | Not specified in the source documents (DOR-RWB-S5-E4030-APP-2) |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-030-06 | FEAT-AST-21 | Not specified in the source documents (DOR-RWB-S5-E4030-APP-2) |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The inbox row and the `ProceedsMatched` subscription | TC-E4-030-01 | FEAT-AST-21 | Not specified in the source documents (DOR-RWB-S5-E4030-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s | The four consumed rows and the boundaries | TC-E4-030-01, -03 | FEAT-AST-21 | Not specified in the source documents (DOR-RWB-S5-E4030-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record before the change | TC-E4-030-04, -06 | FEAT-AST-21 | Not specified in the source documents (DOR-RWB-S5-E4030-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-030, Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word |
| Test cases | TC-E4-030-01 to TC-E4-030-23 |
| Feature and screens | FEAT-AST-21, SCR-21 and SCR-22 |
| Rules | R-DIS-54 and R-DIS-55, governed in rwb-decision; R-DIS-56 to -58, -71 and -72 adjacent |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The shape of the reads, the consumed rows, the subscription, the record element, the error set and the fakes: RWB-S5-E4030-CON.
- The sale, the award, the five-day payment term and the title transfer: FEAT-AST-18 to FEAT-AST-20's stories (R-DIS-47 to R-DIS-53).
- The payment matching, the balance application, the loan-account posting and the vendor-fee posting: FEAT-PAY-04 and FEAT-PAY-10 of rwb-payment (P8) (GAP-2948).
- The no-shortfall close and the residual routing to write-off or debt sale: R-DIS-56 to R-DIS-58 of the write-off route (S7) (GAP-2950).
- The residual-route task and the manual decision: R-DIS-71 and R-DIS-72, adjacent (GAP-2950).
- The case of record, its states, the stage clock and the parent workflow: rwb-case (P3).
- The account and NPA-sale facts of ACE: rwb-source-data (P1) (GAP-2946).
- The rule rows, the package version and their approval: rwb-decision (P7) (GAP-2953).
- The agent reference of R-DIS-54's systems column: not claimed, DP-20 outside the pattern set (GAP-2948).
- The composite route and the field list: RWB-PLT-N001-CON and the edge stories.
- The real payment, case and source-data calls and their evidence: the wave 3 harness.
- The deployment, the flag, the dashboards and the runbook: the operations story of this legacy key.

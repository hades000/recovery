# RWB-S6-E6012-APP Apply the debt sale cap

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP19 |
| Parallel lane | L-S6-P |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S6-E6012-APP-16) |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the cap slice of RWB-E6-012 split out for rwb-debtsale. Both legacy acceptance criteria are kept word for word with their origin tag; holding the sale population inside the policy cap and reporting the headroom is now the cap step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, which reads the cap row and the reference data in force on the rwb-case parameters contract, evaluates the cap test of R-DS-19 and R-DS-23 against the Debt sale package read from rwb-decision, reads the exposure of the population on the rwb-source-data contract, records the verdict and the headroom through the local decision-record library before anything changes (DP-03), answers the lot build and award steps with the verdict and serves the headroom element on `/api/recovery/debtsale/v1` for SCR-26 Award through the gateway-bff composite route (DP-19). No case state and no award is written here. The plan's empty C row, the absent DP-04, DP-06, DP-07, DP-08 and DP-09 rows, the unpublished trigger, the unnamed cap row and the missing headroom column are recorded as GAP-3015 with ASM-4996 to ASM-5003. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E6012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer**, I want **the Workbench to hold the sale population inside the policy cap and report the headroom**, so that **debt sales run on approved lots and masked data**.

This is the cap slice of legacy RWB-E6-012, the FEAT-DBS-16 step of the S6 Debt sale module. It owns:

- the two legacy acceptance criteria, copied verbatim with their origin tag, and the messages, screen and rules they depend on;
- the cap step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, as the stage child of `CaseWorkflow` owned by rwb-case (Temporal and Drools Design slide 13; Architecture v5 slide 19);
- the cap test of R-DS-19 and R-DS-23 of the Debt sale route set, evaluated with the package version in force, and the position of the sale population against the cap row of FEAT-DBS-16;
- the headroom of the population, computed over the lot and account facts of `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale` and over the exposure read on the rwb-source-data contract;
- the local decision record of the verdict, the cap row version and the headroom, written through RWB-PLT-E1027-CON before any change (DP-03), which is what legacy AC1 and AC4 of the sibling stories test and what AC2 here tests by its failure;
- the answer to the lot build and award steps of this service, and the headroom element served read only for SCR-26 Award through the gateway-bff composite route (DP-19).

It does not own: the published shape of the headroom element, the consumed rows, the error set and the fakes, which belong to the contract baseline of this legacy key and are not in the plan (GAP-3015); the eligibility selection (RWB-S6-E5023-APP); the lot build, the price estimate and the reserve (RWB-S6-E5024-APP, RWB-S6-E6001-APP); the award, the price test against the reserve and the case moves to `AWARD_PENDING` and `LOT_AWARDED` (RWB-S6-E6005-APP); the case of record and its route states (P3); the cap parameter and its reference data (P3, default ruling of §R3); the rule rows and their approval (P7); the rights and the scope (P4); the documents and notices (P5, P6); the ACE exposure data (P1); and the deployment of this step, which is the operations story of this legacy key.

### 2. Business rationale

The cap is a limit, not a target: the epic BRD keeps it as BR-050, "The debt sale population is held inside the policy cap and the headroom is reported", priority Must, with the note that it "is a regulatory and board limit, not a target" (Recovery Workbench Business Requirements Epics 3 to 8 v1; FEAT-DBS-16). The metric is unchanged: the debt sale turnaround of 45 days is measured on the decision log and the Workbench records and reviewed monthly (FSD S6 A2.16.1).

What D-RCV-60 changes is where each fact of the cap lives:

- **the cap value is not this service's.** Template and Rules §R3 puts parameters and reference data with P3 rwb-case (E1-042, E1-043), so the cap row and its version are read on that contract and are never a constant. Only one figure is published, "the 54 percent cap" of R-DS-19, R-DS-23 and FSD S6 A2.1; the row that holds it, its basis and its owner are named by no source (GAP-3015; ASM-4998, ASM-4999).
- **the population is the service's own.** The lots and their accounts are `debt_sale_lot` and `debt_sale_account` in `rwb_debtsale`, and the exposure behind them arrives on the rwb-source-data contract.
- **the rule rows stay with rwb-decision (P7).** The package and its version are read, never authored here; the DEBTSALE set of 41 rules over 29 states is governed there (TSD S6 T4).
- **no case state moves here.** R-DS-19 moves `BIDS_RECEIVED` to `AWARD_PENDING` and R-DS-23 `AWARD_PENDING` to `LOT_AWARDED`; both are the award step's, and this step returns the verdict that step consumes (GAP-3015; ASM-5000).
- **the trigger is not published.** FSD S6 A2.16.2 step 1 names "a completed ACE batch, an event or a timer", A2.16.4.4 declares "No background event", and the context pack lists 0 jobs for S6; the step therefore runs inside `DebtSaleWorkflow` and registers no Schedule and no event (GAP-3015; ASM-5000).
- **no cap rule of its own exists.** FSD S6 A2.16.3.1 lists only VR-S6-016-1 and BR-S6-016, and the only rows naming the cap are R-DS-19 and R-DS-23 at the award, so the cap is a parameter test inside the package (GAP-3015; ASM-4997).
- **the wave is EP06's.** EP06 maps to wave 4 (§R5.6) and the plan gives wave 4 while rwb-debtsale is created in wave 3; the story keeps the plan's wave and the tentative release date (§U7).

### 3. Preconditions

- The Debt sale package is in force at its version with R-DS-19 and R-DS-23, authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- The rwb-case parameters contract publishes the cap row of FEAT-DBS-16 with its version, and the reference-data contract publishes `LOV-SEGMENT`, `LOV-LOT-STATUS`, `LOV-BUYER-CLASS` and `LOV-PUTBACK`. Neither operation is named by a source; both carry the placeholder (GAP-3015; ASM-4996).
- The rwb-source-data exposure read of the sale population is published with its fake; its operation name is Not specified in the source documents (GAP-3015; ASM-4996). No `v_ace_*` view is read by this service.
- The rwb-case case list is available for the fake, so the population of a cycle can be taken on Day 1; its operation name is Not specified in the source documents (GAP-3015; ASM-4996).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-26 Award reaches the headroom element through the gateway-bff composite route, one hop, and no screen calls the service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_debtsale` and holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_decision`, `rwb_access` or `rwb_source_data` is refused by the database.

### 4. Flow

1. The lot build step of this service (`RWB-S6-E5023-APP`, `RWB-S6-E5024-APP`) or its award step (`RWB-S6-E6005-APP`) calls the cap step of `DebtSaleWorkflow` on queue `rwb-debtsale`, with the cycle, the lot, the case set and the population it proposes. The trigger is a step of that workflow: no event, no batch job and no Schedule of this story fires it (GAP-3015; ASM-5000).
2. The step loads the Debt sale package version in force from rwb-decision, read only, one hop with a 2 s budget and a breaker.
3. It reads the cap row of FEAT-DBS-16 and the reference data in force on the rwb-case parameters and reference-data contracts, with the version of each row (GAP-3015; ASM-4996).
4. It reads the population of the cycle from this service's own rows: the `debt_sale_lot` lots of status BUILDING, OFFERED, AWARDED or TRANSFERRED of `LOV-LOT-STATUS` and their `debt_sale_account` rows, with `outstanding` (DF-SAL-035) and `selling_price` (DF-SAL-036).
5. It reads the exposure behind those accounts on the rwb-source-data contract, so the population position is measured against the base the cap names. The base and the denominator of the cap are not published; the step records the basis it used and the placeholder (GAP-3015; ASM-4999).
6. `DebtSaleCapEvaluator` applies the cap test of R-DS-19 and R-DS-23: the population after the proposed change against the cap row. The verdict is one of three: the population is inside the cap and the headroom is reported, the population reaches the cap exactly, or the proposed change would take it over the cap and the proposal is held.
7. `CapDecisionRecordWriter` writes one decision record through the local decision-record library, **before anything changes**: the cycle, the lot, the case set, the rule ID with its version, the cap row with its version, the population figure, the cap figure, the verdict and the headroom. A failed write changes nothing and the caller sees MSG-P7-003 (DP-03; legacy AC2).
8. The step answers the caller with the verdict, the headroom and the rule and cap versions. A hold is applied by the caller: the lot build holds the accounts and the award step holds the award, in their own stories; this step writes no lot status, no case state and no award (GAP-3015; ASM-5000).
9. The headroom element of the lot is served read only on `/api/recovery/debtsale/v1` for SCR-26 Award, with the population figure, the cap figure, the headroom, the verdict, the rule and cap versions and the decided-at time, and no personal data, reached through the gateway-bff composite route (DP-19).
10. A repeated call for the same cycle, lot and rule and cap version writes no second record and no second answer; the repeat is counted, and a change of the cap row, of its version or of the package starts a new evaluation.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no verdict and no answer leaves the service | MSG-P7-003 | AC2, TC-E6-012-02, TC-E6-012-04 |
| X2 | The caller's identity does not hold the right in the capability area | 403 before any read or write; nothing changes | MSG-P4-002 | AC3, TC-E6-012-03, TC-E6-012-07 |
| X3 | The cap row of FEAT-DBS-16 is absent, or its version is not published | No cap test runs: the step holds, writes nothing and reports the reason; no message of the legacy set fits the case, so the reason is recorded in the decision record only | None (the message for an absent cap row is Not specified in the source documents (GAP-3015; ASM-4999)) | AC1 |
| X4 | The ACE data behind the population is stale after a late or failed batch | The step holds, writes nothing and reports the data date with its message | MSG-P1-001 | AC1 |
| X5 | The rwb-case, rwb-decision or rwb-source-data contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 | None | AC1 |
| X6 | The exposure of an account in the population is absent, or the cap basis cannot be measured | The step holds the lot, writes nothing and names the missing fact | MSG-GEN-001 | AC1 |
| X7 | The same cycle, lot and rule and cap version arrive twice | One record, one answer; the repeat is counted | None | AC1 |
| X8 | A component, a statement or a test reaches another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC4, TC-E6-012-06, TC-E6-012-08 |

X1 and X2 are the exception paths of RWB-E6-012 carried onto the split, X3 to X7 are the paths the target call types add, and X8 is the DP-01 boundary. No threshold, basis or percentage is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the decision-record stub, the composite route fake and the rwb-case, rwb-decision, rwb-access and rwb-source-data fakes, on its own schema, and needs no live P3, P4, P7 or P1 |
| Negotiable | The activity name, the decision code and the shape of the headroom element are this story's choice; the rules, the messages, the screen, the cap row and the two tables are fixed |
| Valuable | The population is held inside the cap and the headroom is reported with the rule and cap versions, before a lot is offered or an award is confirmed |
| Estimable | One workflow step, one evaluator, one record write, one aggregate read, four clients and one read-only screen element |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic lots and a synthetic cap row through the fakes, plus the failed record write and the absent cap row |

### 7. Acceptance criteria

```gherkin
Feature: Apply the debt sale cap

  Background:
    Given case "RC-2026-000842" carries the debt sale lot "LOT-2026-000042" of segment "RETAIL"
    Given the Debt sale rule package is in force at its version and carries R-DS-19 and R-DS-23
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Apply the debt sale cap (legacy RWB-E6-012 AC1)
    Given the rwb-case contract mock returns the Debt sale parameters in force, with the 54 percent cap of R-DS-19 as the policy cap row of FEAT-DBS-16
    Given the rwb-source-data contract mock returns the exposure of the population at today's business date
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then holds the sale population inside the policy cap and reports the headroom
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-012 AC2)
    Given the rwb-decision decision-record contract mock returns a failed write
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 An identity without the Debt sale right is refused before any read or write (new, D-RCV-60)
    Given the caller's identity does not hold the Debt sale right in the capability area
    When the cap step is called
    Then the step answers 403 with MSG-P4-002 and nothing changes

  Scenario: AC4 A statement that reaches another service's schema or a v_ace_* view is refused (new, D-RCV-60)
    Given a component issues a statement against another service's schema or a `v_ace_*` view
    When the build runs the boundary test
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC5 A lot status write the model does not allow is refused (new, D-RCV-60)
    Given the debt sale lot is in status TRANSFERRED of LOV-LOT-STATUS
    When a caller asks this step to write the lot status
    Then the step refuses the write and changes nothing

  Scenario: AC6 The cap value is read at run time from its row and fixed nowhere (new, D-RCV-60)
    Given the rwb-case contract mock returns the cap row at a version other than the one in the fixture
    When the cap step runs
    Then the verdict uses the value read from that row at run time and no default cap applies

  Scenario: AC7 The decision record carries the figures and versions before the answer (new, D-RCV-60)
    When the cap step returns a verdict
    Then the decision record holds the rule ID, the package version, the cap row and its version, the population figure, the cap figure, the verdict and the headroom, and it is written before the answer leaves the service

  Scenario: AC8 The population is read from this service's own rows (new, D-RCV-60)
    Given the population of the cycle is held in debt_sale_lot and debt_sale_account
    When the cap step measures the population
    Then the exposure arrives on the rwb-source-data contract and no table, view or foreign key of another owner is read

  Scenario: AC9 A changed version starts a new evaluation and a repeat writes nothing (new, D-RCV-60)
    Given an evaluation was recorded for the package version and the cap row version in force
    When the package or the cap row changes version, or the same versions are called again
    Then a changed version starts a new evaluation, and the same versions write no second record

  Scenario: AC10 No personal data enters the step, the record or a log (new, D-RCV-60)
    Given the population includes accounts whose source data carries personal identifiers
    When the cap step runs and writes its decision record
    Then only identifiers, codes, amounts, dates and versions are written, and no name, identity number, contact value or unmasked account identifier enters rwb_debtsale, the record, a log or a workflow input

  Scenario: AC11 A consumed contract that does not answer inside 2 s is retried and writes nothing (new, D-RCV-60)
    Given the rwb-case contract mock does not answer inside 2 s
    When the cap step is called
    Then the step times out and retries, nothing is written and the caller's response is Not specified in the source documents (NEWAC-RWB-S6-E6012-APP-AC8)

  Scenario: AC12 A consumed call that fails returns no verdict and writes nothing (new, D-RCV-60)
    Given the rwb-source-data contract mock returns a failed response for the exposure
    When the cap step is called
    Then the step holds, writes nothing and returns no verdict
```

The two criteria are the legacy criteria of RWB-E6-012 word for word, with their origin tag added and the legacy term 'decision log' replaced by 'decision record' in the two places it occurs, and nothing else changed: the repetition of `Then`, `its trigger arrives`, `the action is taken` and `the decision record cannot be written` all stand. The new criteria AC3 to AC12 cover the exception paths X2 and X8, the business rules BR1 to BR11 of section 8, and the timeout and failed-call paths of AC11 and AC12. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines and AC2 one, and those added lines are the only additions to the legacy text. In the target the cap row and the reference data are rwb-case's, read at their version; the package and its rows are rwb-decision's; the exposure is rwb-source-data's; the population is this service's own rows; and the decision is recorded locally before the verdict is returned. Two points are recorded rather than smoothed over: the cap row is named by no source, so the fixture is a synthetic row and the placeholder stands (GAP-3015; ASM-4998); and the case states that R-DS-19 and R-DS-23 move are written by the award step, not here (GAP-3015; ASM-5000).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-19 (BR10) | Debt sale | D8.4 | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | best_bid at or above reserve_price | Test the price against the reserve and the 54 percent cap, and route the award | AWARD_PENDING | Debt sale officer | Case Workspace, Committee View | 2 working days |
| R-DS-23 (BR11) | Debt sale | D8.4 | AWARD_PENDING | AWARD_CONFIRMED | price tested against the reserve and the 54 percent cap, and recorded | Award the lot and generate the sale agreement and the customer notices | LOT_AWARDED | Debt sale officer | Document Hub, buyer portal | None |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character except for the BR ID in the Rule cell: they are the only rows of the DEBTSALE set that name the 54 percent cap, and FSD S6 A2.16.3.1 adds no route rule of its own. Their owner column is a business role, not a service: the case moves to `AWARD_PENDING` and `LOT_AWARDED` are written by rwb-case on the award step's answer, the award itself and the agreement are RWB-S6-E6005-APP's, and this story evaluates the cap condition they carry, records the verdict and reports the headroom (GAP-3015; ASM-4997).

| ID | Rule | Source |
|---|---|---|
| BR1 | The cap is data: the cap row of FEAT-DBS-16 and its version are read from the rwb-case parameters and reference-data contracts, and no percentage, basis or threshold is a constant, a default or a branch of this build | Template and Rules v1 §R3 default rulings and §R5.5 DP-06, DP-07; FSD S6 BR-S6-016; legacy Guardrails |
| BR2 | The decision is recorded before anything changes, with the rule ID, the package version, the cap row and its version, the population figure, the verdict and the headroom; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy RWB-E6-012 AC1 and AC2 |
| BR3 | The population is this service's own: the lots and accounts of `debt_sale_lot` and `debt_sale_account` are read and written here, and the exposure behind them is read on the rwb-source-data contract, never as a table or a `v_ace_*` view | Architecture v5 slide 41; TSD S6 T3.1; DP-01, DP-05 |
| BR4 | No case state, no lot status and no award is written here: the moves of R-DS-19 and R-DS-23 and the award are RWB-S6-E6005-APP's, and this step returns the verdict | Ownership Map (`recovery_case` owner P3); GAP-3015; ASM-5000 |
| BR5 | The cap test runs against the package version in force; a change of the package or of the cap row starts a new evaluation, and a repeat of the same versions writes nothing | FSD S6 A2.16.2 step 1; DP-04; GAP-3015; ASM-4997 |
| BR6 | The headroom is reported with the population figure, the cap figure and the versions that produced them, so a reviewer can reconstruct the position from the decision record alone | FSD S6 A2.16.1; BR-050; GAP-3015; ASM-5001 |
| BR7 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `buyer_partner_id`, `account_id` and the cap row are identifiers of other owners' facts | DP-01; TSD S6 T3.3 |
| BR8 | No person name, identity number, contact value or unmasked account identifier enters `rwb_debtsale`, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 (masked tape under PDPA) |
| BR9 | The cap value of "the 54 percent cap" is copied from R-DS-19 and R-DS-23 and read at run time from its row; it is never written in the build, the tests or the fixtures as a business default | FSD S6 A2.1 and A2.16; Business Rules and Routing Logic v4 R-DS-19 and R-DS-23; legacy Guardrails |
| BR10 | The cap condition of R-DS-19, the best bid tested against the reserve and the 54 percent cap, is evaluated here on the cap row read in force; the route itself is the award story's | Business Rules and Routing Logic v4 R-DS-19; FSD S6 A2.16.2 step 1 |
| BR11 | The cap condition of R-DS-23, the price tested against the reserve and the 54 percent cap and recorded, is evaluated and recorded here; the award and the agreement are RWB-S6-E6005-APP's | Business Rules and Routing Logic v4 R-DS-23 |

Coverage of the eleven rules by criteria and test cases: BR1, BR9 and BR10 by AC6 and TC-E6-012-10; BR2, BR6 and BR11 by AC7 and TC-E6-012-11; BR3 and BR7 by AC8 and TC-E6-012-12; BR4 by AC5 and TC-E6-012-09; BR5 by AC9 and TC-E6-012-13; BR8 by AC10 and TC-E6-012-14.

### 9. State transitions

No DEBTSALE route state belongs to this story: `BIDS_RECEIVED`, `AWARD_PENDING` and `LOT_AWARDED` are rwb-case's and are moved by the award step (BR4). What this story owns is the cap position of the population and the state of its own step.

| From (cap position of the population) | Event | Condition | To |
|---|---|---|---|
| Not measured in the cycle | The step is called by the lot build or the award step | The package and the cap row in force are loaded | Measured, the verdict and the headroom recorded |
| Measured | The proposed population is inside the cap | Population after the change below the cap row | Inside the cap, the headroom reported and the proposal released to its caller |
| Measured | The proposed population reaches the cap exactly | Population after the change equal to the cap row | At the cap, the headroom of zero reported and the proposal released to its caller |
| Measured | The proposed population would pass the cap | Population after the change above the cap row | Over the cap, the proposal held by its caller, nothing written on the lot |
| Measured, At the cap, Over the cap | The same cycle, lot and versions arrive again | X7 | Unchanged, the repeat counted |
| Measured, At the cap, Over the cap | The cap row, its version or the package changes | A new evaluation | Measured again, a new record |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A call arrives for a cycle and a population | The package in force is loaded | Evaluating |
| Evaluating | The cap row and the reference data answer | The exposure of the population answers | Deciding |
| Deciding | The rule conditions are met | The record is written | Answered |
| Deciding | The cap row is absent or its version is unpublished | X3 | Held, nothing written and the reason recorded |
| Answered | The verdict and the headroom are returned and the element is served | The transaction commits | Waiting for the next call |
| Answered | The record write or the transaction fails | X1 | Waiting, nothing changed |

The lot status values `BUILDING`, `OFFERED`, `AWARDED`, `TRANSFERRED` and `CLOSED` are those of `LOV-LOT-STATUS` and the segment values `RETAIL`, `SSME` and `CORPORATE` those of `LOV-SEGMENT` in TSD S6 T3.2; both are read as reference data, and the cap row is read with its own version (GAP-3015; ASM-4998).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary business role of the feature and the one that reads the headroom on SCR-26 Award; it holds no act in this step, which runs unattended |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Debt sale RA: reads the headroom and the cap position; the approval of a lot and the DoA act are other stories' and rwb-decision's |
| RW-HEADASL, Head of Asset Liquidity | Debt sale RA: reads the headroom and the cap position of a lot, as the legacy permission row gave the case record read to the sale roles |
| SY-RULES, SY-CASEWF, SY-AGENT | Debt sale R as the TSD S6 T6.1 matrix gives the service identities; the step runs under the service identity and is subject to the same checks |
| rwb-debtsale service identity | Runs the step, evaluates the cap test, writes the decision record, answers the caller and serves the headroom element; it holds no grant on another schema |

The rights above are the rows of TSD S6 T6.1 and nothing wider. The legacy permission table gives the capability area "Case record" right R to a long role list and declares no debt sale right for the feature, because the work runs unattended; in the target the population is read under the Debt sale capability area of rwb-access and the read of the headroom on SCR-26 Award follows the screen's right. DP-08 is not in the pattern set of this key, so the capability area and the right are declared per surface and the guard is a service-template capability; the row is absent from the plan and recorded (GAP-3015; ASM-5002).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020, DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | id, lot_no | Read, the lot the population is measured on |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Read, the cycle the lot belongs to |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Read, against `LOV-SEGMENT`, the segment the cap position is reported by |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Read only, for context of the award step; not changed here |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Read, against `LOV-LOT-STATUS`, the business status the screen shows; never written by this story. The routing state held in `state` is not read here and is never inferred from `status` |
| DF-SAL-031, DF-SAL-032, DF-SAL-033 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id | Read, the account set the population figure is built from |
| DF-SAL-035 | debt_sale_account (S6, `rwb_debtsale`) | outstanding | Read, the exposure figure per account |
| DF-SAL-036 | debt_sale_account (S6, `rwb_debtsale`) | selling_price | Read, the price figure per account where the population is measured on price |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, cap row and version, population figure, cap figure, verdict, headroom, decided at | Write through the local library, before anything changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code, condition | Not read as a table: the rows arrive in the package in force from rwb-decision |
| The cap row of FEAT-DBS-16 (E1-042) and the reference data rows (E1-043) | parameters and reference data (P3) | the cap value with its version, `LOV-SEGMENT`, `LOV-LOT-STATUS`, `LOV-BUYER-CLASS`, `LOV-PUTBACK` | Not read as a table: the rows and their versions arrive on the rwb-case contracts. The field names, the row key and the basis of the cap are Not specified in the source documents (GAP-3015; ASM-4998) |
| The exposure of the population | rwb-source-data (P1) | outstanding and exposure per account of the sale population | Not read as a table and not through a `v_ace_*` view: the figure arrives on the rwb-source-data contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code | Not read as a table: the case set arrives on the rwb-case contract and no state is written |

Field IDs are those of TSD S6 Debt sale v2 T3.1 and the Logical Data Model and Data Dictionary v9. The legacy Data table names `decision_log_entry` (DF-DEC-001 to DF-DEC-018) and `rule_row` (DF-REF-001 to DF-REF-015); in the target the first is the local decision record created in `rwb_debtsale` by the library and centralised by rwb-decision, and the second is the package row read from rwb-decision. **No new table, no new column and no migration**: the headroom has no column in TSD S6 T3.1, so it is recorded in the decision record (GAP-3015; ASM-5001).

**No personal data.** The rows and the record carry identifiers, codes, amounts, dates and versions. No name, identity number, date of birth, address or contact value enters `rwb_debtsale`, the record, a log, an event or a workflow input, and every fixture is synthetic.

### 12. Contract

Contract version: v1, the major version in the path /api/recovery/debtsale/v1; the minor version is Not specified in the source documents (DOR-RWB-S6-E6012-APP-23).

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module, API-S6-001 `POST /debt-sale-lots`, API-S6-002 `GET /debt-sale-lots/{lotId}`, API-S6-003 `POST /debt-sale-lots/{lotId}/award`, API-S6-004 `GET /partner/data-room/{lotId}` and API-S6-005 `POST /partner/data-room/{lotId}/bids`, and none of them is a cap or headroom operation; the legacy story itself declares "None. The work runs as a service or a scheduled job inside the recovery module." The headroom is served as an element of the SCR-26 Award answer on base `/api/recovery/debtsale/v1` through the gateway-bff composite route (DP-19), and it is embedded in the lot read API-S6-002, which RWB-S6-E5023-APP, RWB-S6-E5024-APP and RWB-S6-E6001-APP declare. This story claims no operation and fixes only the element. The absence is recorded as GAP-3015.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The cap and reference-data read (operation name Not specified in the source documents (GAP-3015; ASM-4996)) | `/api/recovery/case/v1` | P3 rwb-case | The cap row of FEAT-DBS-16 with its version and the `LOV-SEGMENT`, `LOV-LOT-STATUS`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` values in force; read only, faked |
| The case list read (operation name Not specified in the source documents (GAP-3015; ASM-4996)) | `/api/recovery/case/v1` | P3 rwb-case | The cases and accounts of the cycle the population is taken from; read only, faked |
| The exposure read of the sale population (operation name Not specified in the source documents (GAP-3015; ASM-4996)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The exposure per account behind the population, at today's business date; read only, faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The Debt sale package at its version with R-DS-19 and R-DS-23; read only, faked |
| The authorise call and the capability area read (operation name Not specified in the source documents (GAP-3015; ASM-4996)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Debt sale", the right of the caller and the scope of its lots; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-3015 with ASM-4996.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (event 23) and `AccountsTransferred`, and neither is produced by this step: `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's. The decision record reaches the shared topic `rwb.decision-record.v1` through the platform library, not through a producer of this story, and DP-09 is not in its pattern set. A build that opens a producer here fails the absence test (GAP-3015; ASM-5003).

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-debtsale the event `ProceedsMatched`, which is the settlement step's, and no event of the module carries a cap call; FSD S6 A2.16.4.4 declares "No background event" for the feature, so the step holds no consumer group, no subscription and no inbox row. A build that adds one fails the absence test (GAP-3015; ASM-5000).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga with pivot = transfer | `rwb-debtsale` | Input: the cycle, the lot, the case set, the proposed population and the rule and cap versions in force; signals: the case list answer, the exposure answer, the cap and reference-data answer and the package in force |
| `applyDebtSaleCap` | Activity, the one cap step of this story | `rwb-debtsale` | The cycle, the lot and the population in; the verdict, the population figure, the cap figure, the headroom and the versions out, with the decision record written before the answer |

Start rule of `DebtSaleWorkflow` (Temporal Catalog v1, Workflows row): it starts when the monthly sale cycle opens or a residual arrives from disposal (R-DS-01). The workflow ID form and the duplicate-start policy (start or signalWithStart) are Not specified in the source documents (CG-ALL-10828).

No child workflow and no Schedule exists for this step. The activity name is a target design choice and is fixed by no source document. The saga steps of the workflow, reserve accounts, approve sale, buyer pays, transfer accounts, post proceeds, close cases and tell customers, belong to the award, settlement and transfer stories of this service; this story owns the cap step alone.

#### 12.6 Schedules

None. The context pack lists 0 jobs for S6, DP-10 is not in the pattern set of this key, and the only trigger wording of the feature is FSD S6 A2.16.2 step 1, "a completed ACE batch, an event or a timer", against A2.16.4.4, "No background event"; the step therefore runs inside `DebtSaleWorkflow` at the lot build and the award, and registers no Temporal Schedule and no legacy Quartz job (GAP-3015; ASM-5000).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lots of the population, their segment and their status; read only here |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of the lot with their outstanding and selling price; read only here |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked record of the verdict, the versions and the headroom (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated call for a cycle and a lot |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object exists; this step writes no row to it (GAP-3015; ASM-5003) |

Not owned and never read as a table: `recovery_case`, `case_list` and `timer` (P3), the parameters and reference-data rows (P3), `decision_log_entry` and `rule_row` (P7), `role`, `permission` and the scope rows (P4), `partner` (S9), `document` (P5), `notice` (P6), the source-data exposure rows (P1) and every `v_ace_*` view. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case parameters and reference-data fake | The cap row of FEAT-DBS-16 at its version, carrying the 54 percent cap, and the `LOV-SEGMENT`, `LOV-LOT-STATUS`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` values in force; a missing cap row and an unpublished version | AC1, X3 |
| rwb-case case-list fake | The cases and accounts of cycle `CYC-2026-000004`, of which lot `LOT-2026-000042` is one; an empty cycle and an out-of-scope case | AC1 |
| rwb-source-data exposure fake | The exposure of the population at today's business date; a stale date and an absent account | AC1, X4, X6 |
| rwb-decision rule-package fake | The Debt sale package at its version in force with R-DS-19 and R-DS-23 | AC1 |
| rwb-access authorise fake | The capability area "Debt sale" with right C, R, U or A for `RW-DEBTSALE`, `RW-PRODHEAD` and `RW-HEADASL`; an identity without the right | X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-26 Award answer for lot `LOT-2026-000042` and case `RC-2026-000842`, with the headroom element read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case parameter and case-list reads, the rwb-source-data exposure read and the rwb-access authorise call are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3015; ASM-4996).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The rwb-case parameter and reference-data read, the rwb-case case-list read, the rwb-source-data exposure read, the rwb-decision package read and the rwb-access authorise call; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `LotAwarded` and `AccountsTransferred` are sibling stories', and the decision-record topic is written by the platform library |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and its `applyDebtSaleCap` step on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; INT-25 Debt buyers is untouched by this step |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.debtsale`, module `debtsalecap`, Java package `th.co.scb.ace.workbench.recovery.debtsale.debtsalecap`; front end `src/modules/recovery/debtsale/CapHeadroom.tsx`, the SCR-26 Award element, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record is written before the verdict leaves the service, and a failed write stops it with nothing changed. DP-19 is how SCR-26 Award reaches the headroom element, one hop through the gateway, and it is the only surface this story adds.

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-3015 with ASM-4996. DP-04 is absent although the step evaluates the Debt sale package; DP-06 and DP-07 are absent although the cap and the lists are rwb-case's parameter and reference-data rows; DP-08 is absent although the RBAC matrix declares a capability area per surface; DP-09 is absent although the library object `outbox_event` exists in the schema; DP-10 is absent although the legacy work "runs as a service or a scheduled job". None is added to the metadata rows, and each is named here and in the registers (GAP-3015; ASM-4997, ASM-4998, ASM-5000, ASM-5002).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` cap branch | Workflow | The branch that waits for the call of the lot build or the award step and reports the verdict to it |
| `applyDebtSaleCap` | Activity | The one step: read the cap row, the lists, the package, the population and the exposure, evaluate, record and answer |
| `DebtSaleCapEvaluator` | Service | The cap test of R-DS-19 and R-DS-23 against the package version in force, with the cap row version and the population position |
| `PopulationPositionReader` | Repository | The aggregate of `debt_sale_lot` and `debt_sale_account` of the cycle, by segment and status, with no cross-schema join |
| `CapDecisionRecordWriter` | Library adapter | Writes the verdict, the versions and the headroom before anything changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `ParametersClient` | Client | The cap row and the reference data in force of rwb-case (P3), one hop, 2 s, breaker |
| `CaseListClient` | Client | The cases and accounts of the cycle of rwb-case (P3), one hop, 2 s |
| `ExposureClient` | Client | The exposure of the population of rwb-source-data (P1), one hop, 2 s |
| `RulePackageClient` | Client | The Debt sale package in force of rwb-decision (P7), one hop, 2 s |
| `AccessGuardClient` | Client | The capability area and the right of rwb-access (P4), through the service-template guard |
| `CapHeadroomController` | Controller | The read-only headroom element on the service base, the rights and the problem mapping of 400, 401, 403, 404, 422 and 503; it declares no operation that TSD S6 T-A does not publish (GAP-3015) |
| `CapHeadroom` | React component | Shows the population figure, the cap figure, the headroom and the verdict on SCR-26 Award, read only |

**Database and migrations.** No Flyway file of this story. `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, the decision record and the idempotency key are library objects created in `rwb_debtsale` by the library's migration (DP-03), and no cap position or headroom column is added here (GAP-3015; ASM-5001).

**Configuration and reference data.**

- The cap row of FEAT-DBS-16 and its version, read from rwb-case at run time; the "54 percent" figure is copied from R-DS-19 and R-DS-23 and is never a constant of the build.
- `LOV-SEGMENT`, `LOV-LOT-STATUS`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2).
- The Debt sale package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The capability area "Debt sale" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget and the single hop are the platform rule of ADR-020; no other parameter is named for the step by a source.

**Build steps**

1. The cap branch of `DebtSaleWorkflow` and its input record on `rwb-debtsale`, with the call of the lot build and the award step as its triggers (AC1).
2. `ParametersClient` and `CaseListClient` against their fakes, with the 2 s budget, the breaker and the absent cap row (AC1, X3, X5).
3. `ExposureClient` and `RulePackageClient` against their fakes, with the stale and the absent-answer paths (AC1, X4, X5, X6).
4. `AccessGuardClient` and the capability area, with the refusal path (X2).
5. `DebtSaleCapEvaluator` over the package, with the three verdicts, the cap row version and the no-constant rule (AC1, BR9).
6. `CapDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
7. `PopulationPositionReader` with the aggregate and the idempotency row (AC1, X7).
8. `CapHeadroomController` and `CapHeadroom` through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_debtsale`, no read of `recovery_case`, `rule_row`, the parameter rows or a `v_ace_*` view (X8, BR3, BR7).

**Feature flag.** `rwb.debtsale.cap-v1`, read as a flag of the platform library; off means the step is not called, the lot build and the award run without a cap verdict and the element shows no headroom, and no other story is affected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic lot build in SIT, each of the three verdicts produces its record and its headroom, the 54 percent figure appears nowhere in the build, a forced record failure changes nothing, no `recovery_case`, `rule_row` or `v_ace_*` read exists in the build, and SCR-26 Award answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this story raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required fact of the call or of the population is absent, or the exposure cannot be measured (X6) | Enter {field}. |
| MSG-P4-002 | An identity without the right of the capability area calls the step or reads the element (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the verdict leaves the service (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data behind the population is stale after a late or failed batch (X4, VR-S6-016-1) | {product} is from {date}. Today's load has not arrived. |

The five IDs are those of the legacy message set and of FSD S6 A2.16.3.1, and the text is the legacy and FSD wording, copied unchanged except MSG-P1-001, whose text is copied from the Error and Message Standard v4 section 4; no other message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of the feature, and no path of this story raises it. No message is published for an absent cap row, so X3 records its reason in the decision record only (GAP-3015; ASM-4999).

### 15. Screens and states

SCR-26 Award in its open, closed, awarded and transferred states is served through the gateway-bff composite route (DP-19) and shows the headroom element of this story next to the bids, the reserve and the award decision of the award story. The route calls rwb-debtsale for the lot and the headroom, rwb-case for the case and its route state, rwb-partner for the buyer and rwb-decision for the approval rows; this story fixes the headroom element only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy story names the same screen and the same four states, so the screen is carried unchanged.

The states this story produces on the element are the inside, at-cap and over-cap positions of §9, with the population figure, the cap figure, the headroom and the rule and cap versions, and it shows the failure states it reads: refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001, and a missing fact with MSG-GEN-001. The award states of SCR-26 belong to the award story and are read from the same route. Against the four screen states, empty and loading are not named by Screen Specifications v1 and are Not specified in the source documents (CG-ALL-10833); error is the not-recorded state with MSG-P7-003 (X1); no access is the refused state with MSG-P4-002 (X2, TC-E6-012-03).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-012-01 | AC1 | Component | Cycle `CYC-2026-000004` with lot `LOT-2026-000042`, the cap row at its version and the exposure at today's date; the verdict, the headroom and the record asserted on the fakes |
| TC-E6-012-02 | AC2 | Component | The decision-record stub stopped; nothing written, no verdict returned and MSG-P7-003 shown |
| TC-E6-012-03 | Access | Component | An identity without the Debt sale right; 403 with MSG-P4-002 and no read |
| TC-E6-012-04 | Principle 5 | Component | A forced decision record write failure at the moment of the verdict; no record, no answer and no second attempt |
| TC-E6-012-05 | Contract of section 12 | Component | Each operation, event and activity named in section 12 checked against the contract version stated in section 12 |
| TC-E6-012-06 | Boundary of section 12.7 | Component | Each table of section 12.7 read and written only at its owner; no foreign key and no read of a table not owned (DP-01; ASM-3438) |
| TC-E6-012-07 | AC3 | Component | An identity without the Debt sale right calls the cap step; 403 with MSG-P4-002 and no read or write |
| TC-E6-012-08 | AC4 | Component | A statement against another service's schema and against a `v_ace_*` view; the grant refuses both and the boundary test fails the build |
| TC-E6-012-09 | AC5 | Component | A lot in status TRANSFERRED; a caller asks the step to write the lot status; the write is refused and nothing changes |
| TC-E6-012-10 | AC6 | Component | The cap row fixture at a changed version; the verdict uses the value read at run time and no fixed default |
| TC-E6-012-11 | AC7 | Component | A verdict on the fakes; the decision record content and its write before the answer are asserted |
| TC-E6-012-12 | AC8 | Component | The population read on the fakes of debt_sale_lot, debt_sale_account and rwb-source-data; no other read asserted |
| TC-E6-012-13 | AC9 | Component | The same versions called twice, then a changed cap row version; one record per version |
| TC-E6-012-14 | AC10 | Component | Source accounts with synthetic personal identifiers; the record and the log are checked for none of them |
| TC-E6-012-15 | AC11 | Component | The rwb-case contract mock does not answer inside 2 s; the step retries, nothing is written and the response is Not specified in the source documents (NEWAC-RWB-S6-E6012-APP-AC8) |
| TC-E6-012-16 | AC12 | Component | The rwb-source-data contract mock returns a failed response; nothing is written and no verdict is returned |

The four legacy cases are the legacy cases of RWB-E6-012 in their legacy order, with the Level column added: the two criterion cases and the forced-failure case map to `Component` because the step is tested on its fakes, and the access case to `Component` because the guard is faked. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. This is an APP story, so no `-ITG` copy is written here; a copy of a case for the wave 4 harness would take the suffix `-ITG` and is not part of this file.

### 17. Guardrails

- No business value in code: the 54 percent cap, its basis, the lists and the rule rows stay a parameter row, reference data or the package, read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, amounts, dates and versions only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service reads no ACE table and no `v_ace_*` view, and a build that adds one fails the boundary test (BR3).
- The case stays with rwb-case, the parameters with rwb-case, the central ledger with rwb-decision and the access with rwb-access: no `recovery_case` row, no parameter row, no role row and no `decision_log_entry` row is written here (BR4).
- No case state, no lot status and no award is written by this step; a build that writes one fails the review (BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own.
- No operation of a sibling is claimed: the lot read and the award path are other stories', and this story fixes only the headroom element (GAP-3015).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no data lake and no second event on the topic.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| BR-050 | The debt sale population is held inside the policy cap and the headroom is reported (Recovery Workbench Business Requirements Epics 3 to 8 v1, priority Must) | The cap test, the verdict and the headroom element | TC-E6-012-01 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |
| REQ-S6-001 | Accounts eligible for sale are selected by rule against the policy cap (FSD S6 requirements served); the plan carries no requirement id for this slice, so the row is cited and the absence recorded (GAP-3015) | The cap position of the population and the headroom | TC-E6-012-01 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |
| FEAT-DBS-16 | Apply the debt sale cap, system, first in E6, depends on FEAT-DBS-01 (FSD S6 A1.2 and A2.16; Epics 3 to 8 Specification v3) | The whole story | TC-E6-012-01, TC-E6-012-02 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the population | TC-E6-012-01 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | TC-E6-012-04 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget | TC-E6-012-01 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record written before the verdict leaves | TC-E6-012-02, TC-E6-012-04 | FEAT-DBS-16 | Not specified in the source documents (DOR-RWB-S6-E6012-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-012, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Test cases | TC-E6-012-01 to TC-E6-012-04 |
| Feature and screen | FEAT-DBS-16 Apply the debt sale cap, SCR-26 Award |
| Rules | R-DS-19 and R-DS-23, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |
| Screen states | SCR-26 Award: no access shows 403 with MSG-P4-002 (TC-E6-012-03) and error shows MSG-P7-003 when the decision-record stub stops (TC-E6-012-02); the empty and loading states are Not specified in the source documents (DOR-RWB-S6-E6012-APP-10) |

### 19. Out of scope

- The published shape of the headroom element, the consumed rows, the error set and the fakes: the contract baseline of this legacy key, which the plan does not carry (GAP-3015).
- The selection of the eligible accounts and the 54 percent cap check of the eligibility step: RWB-S6-E5023-APP and FEAT-DBS-01.
- The lot build, the price estimate and the reserve: RWB-S6-E5024-APP.
- The approval of the lot, the reserve and the tiered terms: RWB-S6-E6001-APP.
- The award of the lot, the price test against the reserve, the case moves to `AWARD_PENDING` and `LOT_AWARDED`, and event EV-23: RWB-S6-E6005-APP.
- The case of record, the case list, the route states and the parent `CaseWorkflow`: rwb-case (P3) (GAP-3015).
- The cap row, the reference data rows and their versions: rwb-case (P3), read on its contracts and faked here (GAP-3015; ASM-4998).
- The rule rows, the package, its approval and its versioning, and the central decision ledger: rwb-decision (P7).
- The capability area, the rights and the scope rows: rwb-access (P4) (GAP-3015; ASM-5002).
- The exposure data products and the ACE views: rwb-source-data (P1) (GAP-3015).
- The sale documents, agreement and notices: rwb-document (P5) and rwb-comms (P6); the partner panel and the buyers: rwb-partner (S9).
- The gateway-bff composite route and the screen field list of SCR-26: RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this step, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

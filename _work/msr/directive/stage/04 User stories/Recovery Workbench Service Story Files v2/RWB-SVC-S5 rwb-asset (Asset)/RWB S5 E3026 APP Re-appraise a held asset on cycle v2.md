# RWB-S5-E3026-APP Re-appraise a held asset on cycle

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-I |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S5-E3026-APP-16) |
| Contract version | v1, the version of the consumed bases in section 12.2 (DOR-RWB-S5-E3026-APP-23) |
| Depends on (build) | RWB-S5-E3026-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (traces to REQ-S5-003) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-026 split out for rwb-asset. The legacy acceptance criteria it owns are kept word for word with their origin tag; the cycle is now one step of `AssetDisposalWorkflow` on task queue `rwb-asset`, driven by the monthly Schedule JOB-19 Re-appraisal monthly, which writes the decision through the local decision-record library before anything else (DP-03), places the re-appraisal order on the valuation owner's contract, and answers the case move `REAPPRAISAL_ORDERED` or `RELISTED` to rwb-case. The legacy `v_ace_valuation` and `v_ace_npa_asset` reads are retired as service reads because rwb-asset holds no ACE view grant, so the appraisal and asset facts arrive on the rwb-source-data contract (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-23 read through the gateway-bff composite route (DP-19). The plan's pattern set carries no DP-10 although JOB-19 is the service's single job, the re-appraisal order has no planned contract row and the module model holds no re-appraisal table, all three recorded (GAP-2869; ASM-4757 to ASM-4763). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (23 resolved, 14 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to raise the re-appraisal order when the holding period passes the re-appraisal interval, and to re-list an asset that closed a round with no bid, each with its decision recorded**, so that **assets sell sooner at approved prices and none sits on the books on a stale appraisal**.

This is the application slice of legacy RWB-E3-026. It owns:

- the three legacy acceptance criteria assigned to it (AC1, AC2 and AC4), copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the re-appraisal cycle step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Temporal and Drools Design slide 13);
- the monthly Schedule JOB-19 Re-appraisal monthly, as one Temporal Schedule of this service, which starts that step for the held assets whose cycle is due (JOB-19 is the single job of the S5 ownership rows; the plan carries no DP-10 row, ASM-4759);
- the evaluation of R-DIS-15 on an `ASSET_HELD` case and of R-DIS-44 on a `NO_BID_AT_FLOOR` case, with the DISPOSAL package version in force;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before anything else (DP-03);
- the re-appraisal order placed on the valuation owner's contract, and the case-move answer `REAPPRAISAL_ORDERED` or `RELISTED` sent to rwb-case;
- the two reads behind SCR-21 Asset list and SCR-23 Listing and price on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two reads, the appraisal element, the order element, the case-move answer, the error set and the fakes, which are RWB-S5-E3026-CON; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the appraisal value, the valuer and the SVAF order itself, which are rwb-valuation (S1) under API-S5-003 and ASM-0043; the ACE valuation and NPA asset facts, which are rwb-source-data's (P1); the DISPOSAL package and its rule rows, which are authored and governed in rwb-decision (P7); AC3 and its end-to-end evidence, which the plan gives to the wave 2 harness RWB-ITG-E3026-ITG (ASM-4762); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E3-026 raised the re-appraisal order when the holding period passed the re-appraisal interval, and re-listed an asset that closed a round with no bid, so that the asset is not priced on an appraisal nobody has refreshed. The FSD keeps the objective and the metric unchanged: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, and moves from 1,486 days to a target of 1,095 days (FSD S5 A2.9.1). The program states the requirement the step serves: REQ-S5-003, "Holding age drives re-appraisal and the provision step by rule" (Must, E3).

What D-RCV-60 changes is who owns the asset, the appraisal, the order and the case:

- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the step's own writes, which is what legacy AC1 asked for and what legacy AC4 tested.
- **the case state stays with rwb-case (P3).** `recovery_case` and the route states `ASSET_HELD`, `NO_BID_AT_FLOOR`, `REAPPRAISAL_ORDERED` and `RELISTED` are P3's; this story evaluates the rule, records the decision and **answers** the move (ASM-4760).
- **the appraisal and the order stay with their owners.** The valuation, the valuer and the SVAF exchange are rwb-valuation's: TSD S5 T-A.1 lists API-S5-003 `POST /assets/{assetId}/valuations` "Order or record a valuation", the Ownership Map ruling ASM-0043 gives that operation to rwb-valuation, and the target path is not published (ASM-4758). The legacy `v_ace_valuation` and `v_ace_npa_asset` reads are P1's: only rwb-source-data reads the 30 `recovery.v_ace_*` views, so DP-05 applies to this story as a **prohibition** and the facts arrive on the owner's contract (ASM-4757).
- **the cycle is a Schedule, not a Quartz row.** JOB-19 is the service's single job in the S5 ownership rows, and DP-10 replaces Quartz with a Temporal Schedule through the workflow kit. The plan's pattern set for this key does not carry DP-10, so the library `RWB-PLT-E1071-CON` is a real dependency the H row does not name (ASM-4759).
- **nothing new is stored.** The module model has no re-appraisal table and no appraisal-date, one-year-flag or re-list-count column, so the cycle lives in the Schedule and in durable workflow state, the rule inputs arrive on the owners' contracts, and the outcome is the decision record plus the case move (ASM-4761).

No business value moves: 12 months, the one-year flag, the re-list limit, the 10-working-day target of R-DIS-15, the route states, the message text and the closed lists stay values of the rule package, of reference data or of the owners' facts, read with their version and never written in code.

### 3. Preconditions

- RWB-S5-E3026-CON is published: the two read operations, the appraisal and asset elements, the re-appraisal order element, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data contract that answers the ACE valuation and NPA asset facts is published with its fake, so a held asset can be evaluated on Day 1. Its operation and data-product names are Not specified in the source documents (GAP-2869; ASM-4757), and the row is not in this story's contract-dependency list, which is None.
- The rwb-valuation operation API-S5-003 is published with its fake: the order names the asset reference, the appraisal reference, the reason code of the rule and the rule version, one hop with a 2 s timeout. Its target path is Not specified in the source documents (GAP-2869; ASM-4758).
- The case state read and the case-move answer of rwb-case are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-2869; ASM-4760).
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the record commits with the order request or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-23 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The Temporal workflow kit and the Schedule capability of RWB-PLT-E1071 are available on queue `rwb-asset`, because JOB-19 is registered as a Schedule and not as a Quartz row; the library is not in this story's H row (GAP-2869; ASM-4759).
- `asset` and `listing` exist in schema `rwb_asset` from the DB story of this service; this story adds no table, no column and no migration (ASM-4761).
- The DISPOSAL rule package is in force at its version with R-DIS-15, R-DIS-44 and R-DIS-06; it is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_valuation` or `rwb_case` is refused by the database and fails the boundary test (DP-05; ASM-4757).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3026-CON when its tests pass, and this story stays in Draft (ASM-4764).

### 4. Flow

1. The Schedule JOB-19 Re-appraisal monthly fires on `rwb-asset` at the reference time in force and starts the cycle step of `AssetDisposalWorkflow` for the held assets whose appraisal age reaches the re-appraisal interval. A case in `NO_BID_AT_FLOOR` also enters the step when its round closes with no bid.
2. The step reads the asset, its reference and its holding status from `asset` in `rwb_asset`, and the appraisal and asset facts of the case on the rwb-source-data contract: `appraisal_date`, `one_year_rule_applied`, `appraised_value`, the appraisal reference and type, the asset reference, the asset key and the book value, one hop with a 2 s budget and a breaker (ASM-4757).
3. The step reads the case state and the case reference on the rwb-case contract (`GET /cases/{caseId}` family), read only, to confirm `ASSET_HELD` or `NO_BID_AT_FLOOR` and to take the reference the answer carries.
4. `ReappraisalEvaluator` loads the DISPOSAL package version in force from rwb-decision and evaluates R-DIS-44 first where the case is in `NO_BID_AT_FLOOR` (relist_count below the re-list limit), otherwise R-DIS-15 on `ASSET_HELD` (appraisal_date older than 12 months and one_year_rule_applied = N) (FSD S5 A2.9.3.1; Business Rules and Routing Logic v4).
5. The evaluation answers the rule ID, the package version, the action and the case move the rule names; the 12-month interval, the one-year flag and the re-list limit are values of the package and never constants of the build.
6. Where no rule fires, the step changes nothing, writes no record and reports the reason to the parent.
7. `ReappraisalDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case reference, the asset reference, the appraisal reference, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. Where the cycle is due, `ReappraisalOrderClient` places the re-appraisal order on the valuation owner's contract (API-S5-003, rwb-valuation, path placeholder) with the asset reference, the appraisal reference, the reason code of the rule, the rule version and the `Idempotency-Key`; this service writes no valuation, no appraisal value and no price, and SVAF is reached by rwb-valuation and not by this step (ASM-4758).
9. `CaseMoveAnswer` answers rwb-case with `REAPPRAISAL_ORDERED` (R-DIS-15) or `RELISTED` (R-DIS-44), the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither (ASM-4760).
10. A repeated cycle for the same asset and the same appraisal reference, or the same `Idempotency-Key` twice, places no second order, sends no second answer and counts the repeat.
11. SCR-21 Asset list and SCR-23 Listing and price read the asset, its holding status, the appraisal age and the re-appraisal state from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no order is placed and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E3-026-04, TC-E3-026-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E3-026-05 |
| X3 | The case is in neither `ASSET_HELD` nor `NO_BID_AT_FLOOR` | 409 and nothing is written; the cycle is not re-evaluated on a case that has already moved | None | AC1, AC2 |
| X4 | The appraisal product is stale after a late or failed load | The step holds, writes nothing and shows the date of the product; it resumes on the next fresh answer | None | AC1 |
| X5 | A consumed contract does not answer inside 2 s, its breaker is open, or the valuation owner refuses the order | The step waits and retries on the workflow's own schedule; no case move is answered and the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X6 | The fact does not satisfy the rule condition (appraisal inside 12 months, the one-year flag already applied, or the re-list limit reached) | No rule fires: nothing changes, no record is written and the case keeps its state | None | AC1, AC2 |
| X7 | The same cycle, asset and appraisal reference arrives twice | One record, one order and one answer; the repeat is counted | None | AC1, AC2 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, AC5, BR2, BR6 |

X1 to X3 are the exception paths of RWB-E3-026 carried onto the split; X4 to X7 are the paths the target call types and the Schedule add; X8 is the DP-05 and DP-01 boundary. The 12-month interval, the one-year flag, the re-list limit and the 10-working-day target are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3026-CON, the rwb-source-data, rwb-case and rwb-valuation fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or S1 |
| Negotiable | The activity name, the Schedule reference time, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two reads and the consumed rows are fixed |
| Valuable | A held asset is re-appraised when its appraisal is older than the interval, and a no-bid asset is re-listed, each with its decision recorded and the case moved in the service that owns it |
| Estimable | One Schedule, one workflow step, one evaluator, one record write, one order request, one case-move answer, one controller and two screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and appraisal facts through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Re-appraise a held asset on cycle

  Background:
    Given case "RC-2026-000511" holds asset "AST-2026-000511" in the recovery journey
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-15, R-DIS-44 and R-DIS-06
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Re-appraise a held asset on cycle (legacy RWB-E3-026 AC1)
    Given the rwb-source-data contract mock returns the appraisal of asset "AST-2026-000511" with appraisal_date older than 12 months and one_year_rule_applied = N
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for "RC-2026-000511"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then raises the re-appraisal order when the holding period passes the re-appraisal interval
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-44 (legacy RWB-E3-026 AC2)
    Given the rwb-case contract mock returns the case state "NO_BID_AT_FLOOR" for "RC-2026-000511"
    Given a case in state NO_BID_AT_FLOOR
    When relist rule applied
    Then re-list the asset and order a re-appraisal where the cycle is due
    Then the case moves to RELISTED

  Scenario: AC4 Not recorded (legacy RWB-E3-026 AC4)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 Boundary: no ACE view read and no foreign-schema write (new, D-RCV-60)
    Given the rwb-asset service build is under test
    When a component, a statement or a test reaches a v_ace_* view, a recovery_case row or another service's schema
    Then the grant refuses the statement
    Then the boundary test fails the build and nothing is released

  Scenario: AC6 Business rules BR1 to BR9 each have a check (new, D-RCV-60)
    Given the rwb-asset service build is under test
    When the build is checked against the rules BR1 to BR9 of section 8
    Then each rule has a passing check and a failing rule fails the build

  Scenario: AC7 Error answers 401, 403 and 404 of the provided operations (new, D-RCV-60)
    Given a provided operation of rwb-asset is called
    When the caller is not authenticated, the caller lacks the right of the operation or the asset is not found
    Then the answer is 401, 403 or 404 respectively

  Scenario: AC8 Activity retry and timeout (new, D-RCV-60)
    Given a consumed contract does not answer inside 2 s
    When the activity is run
    Then the activity retries on the workflow's own schedule and no case move is answered

  Scenario: AC9 Consumed call fails (new, D-RCV-60)
    Given a consumed contract answers with an error
    When the activity is run
    Then the activity fails and no case move is answered

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the status model does not allow the requested change
    When the change is requested
    Then the change is refused and nothing is written
```

The three criteria are the legacy criteria of RWB-E3-026 word for word, with their origin tag added and the decision log wording changed to decision record (CG-ALL-9835); AC5 to AC10 are the added criteria, AC5 for exception X8. In the legacy criteria: the repetition of `Then`, the legacy wording of `the action is taken` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry one `Given the <service> contract mock returns <x>` line, and those added lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-source-data answers the appraisal and asset facts; this story evaluates R-DIS-15 or R-DIS-44, writes the decision record, places the order on the valuation owner's contract and answers the case move; and rwb-case writes `REAPPRAISAL_ORDERED` or `RELISTED`. Two notes are recorded rather than smoothed over: AC3, Rule R-DIS-15's own criterion, is assigned by the plan to the wave 2 harness RWB-ITG-E3026-ITG, so this story keeps the component proof of R-DIS-15 under AC1 and the harness owns the end-to-end evidence (ASM-4762); and AC2's rule is the re-list rule of FEAT-AST-17, tabled here because the plan gives this slice that criterion and because the same cycle step raises both orders (GAP-2869).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-44 (BR10) | Asset disposal | D8.1 to D8.3 | NO_BID_AT_FLOOR | RELIST_RULE_APPLIED | relist_count below the re-list limit | Re-list the asset and order a re-appraisal where the cycle is due | RELISTED | Sale officer | Workbench, SVAF | None |
| R-DIS-15 (BR11) | Asset disposal | D8.1 to D8.3 | ASSET_HELD | REAPPRAISAL_CYCLE_DUE | appraisal_date older than 12 months and one_year_rule_applied = N | Order the re-appraisal through SVAF | REAPPRAISAL_ORDERED | Valuer | SVAF | 10 working days |
| R-DIS-06 (BR12) | Asset disposal | D8.1 to D8.3 | ASSET_ON_BOOKS | ASSET_RECORD_CONFIRMED | title_status in (clear, under_transfer) | Start the holding age clock and the provision step clock, and charge cost of carry monthly | ASSET_HELD | Sale officer | Workbench, Finance provision feed | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: `REAPPRAISAL_ORDERED` and `RELISTED` are written by rwb-case on this story's answer, the order is placed on rwb-valuation's contract and SVAF is reached there, and the holding clock and cost of carry of R-DIS-06 are the sibling stories' (RWB-S5-E3023-APP for the clock, rwb-payment for the posting). R-DIS-06 is tabled because the FSD lists it in the rule set of this feature and because R-DIS-15 is only reachable on an `ASSET_HELD` case.

| ID | Rule | Source |
|---|---|---|
| BR1 | The cycle is driven by one Schedule of this service and by the workflow's durable state; no Quartz row, no shared job table and no batch table is written | DP-10; S5 ownership rows (JOB-19); Architecture v5 slide 44; ASM-4759 |
| BR2 | The appraisal and NPA asset facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table and takes the facts on the owner's contract only | DP-05; Architecture v5 slides 29, 37 and 45; ASM-4757 |
| BR3 | The decision is recorded before anything else, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 |
| BR4 | The re-appraisal order is rwb-valuation's operation and the valuation is never created here: API-S5-003 is owned by rwb-valuation under ASM-0043 and SVAF is reached by that owner, and the accepted value and its date are read back on the rwb-source-data contract (BR2) | TSD S5 T-A.1 and T-A.2; Ownership Map ruling ASM-0043; ASM-4758 |
| BR5 | The case move is answered and not written: `recovery_case` and the route states `ASSET_HELD`, `NO_BID_AT_FLOOR`, `REAPPRAISAL_ORDERED` and `RELISTED` are rwb-case's | Ownership Map (recovery_case owner P3); ASM-4760 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and the appraisal and asset references are identifiers of other services' facts | DP-01; TSD S5 T3.3 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: the 12-month interval, the one-year flag, the re-list limit, the 10-working-day target, `LOV-HOLDING` and the route states | TSD S5 T3.2; FSD S5 BR-S5-009; legacy Guardrails |
| BR8 | The same cycle, asset and appraisal reference twice, or the same `Idempotency-Key` twice, places one order, sends one answer and counts the repeat | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, an order or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's: the step answers the move and the parent `CaseWorkflow` applies it (BR5). What this story owns is the state of the step and the reason it carries.

| From (case route state, P3) | Event | Condition | To (answered) |
|---|---|---|---|
| ASSET_HELD | REAPPRAISAL_CYCLE_DUE | appraisal_date older than 12 months and one_year_rule_applied = N | REAPPRAISAL_ORDERED, from R-DIS-15 |
| NO_BID_AT_FLOOR | RELIST_RULE_APPLIED | relist_count below the re-list limit | RELISTED, from R-DIS-44 |
| NO_BID_AT_FLOOR | RELIST_RULE_APPLIED | relist_count at or above the re-list limit | Unchanged, no rule fires (X6) |
| Any other route state | The Schedule fires | X3 | Unchanged, nothing written |
| ASSET_HELD or NO_BID_AT_FLOOR | The same cycle twice | X7 | Unchanged, the repeat is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | JOB-19 fires, or a round closes with no bid | The package in force is loaded | Evaluating |
| Evaluating | R-DIS-15 or R-DIS-44 fires | The decision record is written | Applying |
| Applying | The order is placed and the case-move answer is sent | The transaction commits | Waiting for the next cycle |
| Applying | The record write fails, the order is refused or a contract does not answer | X1, X5 | Waiting, nothing changed |
| Waiting | The appraisal product is stale | X4 | Held, until a fresh answer |

The downstream states of `REAPPRAISAL_ORDERED` — `REAPPRAISAL_RECEIVED`, the value accepted or rejected under R-DIS-16 to R-DIS-18 — and the valuation value itself belong to rwb-valuation and are not entered here; the `REAPPRAISAL_ORDERED` and `RELISTED` values are those of the DISPOSAL machine of TSD S5 T4.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1: the role of R-DIS-44 and the primary person on the no-bid path, reading the asset, its appraisal age and its re-appraisal state |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the asset and its appraisal, and confirms a re-appraisal order where a person is needed |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset and the order on the enforcement-auction route |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA: read, and approve through the approval path where a re-list or a price needs it |
| PT-VALUER, PT-AUCTION, PT-RAMC | Asset and disposal R or RU as the TSD S5 T6.1 matrix gives it: the valuation party sees its own order through the partner gateway, never the case decision |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step under the same checks |
| rwb-asset service identity | Fires the Schedule, evaluates the rules, writes the decision record, places the order and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the sale officer as also-user (FSD S5 A2.9.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the sale officer, the NPA and asset manager and the valuer are the roles of the person paths on SCR-21 and SCR-23. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the rwb-access authorise check on the capability area Asset and disposal and its right is stated here and not built here, for each operation of section 13.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028, DF-COL-031, DF-COL-029, DF-COL-041 | asset (S5, `rwb_asset`) | id, asset_ref, case_id, holding_status | Read, to identify the asset, its case and whether it is held |
| DF-SAL-006, DF-SAL-008 | listing (S5, `rwb_asset`) | round_no and status | Read, for the no-bid path of R-DIS-44; the round itself is written by the auction story |
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | appraisal_no, appraisal_type, appraised_value, appraisal_date, asset_key and the one-year flag | Not read as a view: taken on the rwb-source-data contract (BR2) |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, from_segment, book_value and transfer-in facts | Not read as a view: taken on the rwb-source-data contract (BR2) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the state arrives on the rwb-case read and the move on its answer |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before anything else |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read and not written: the rule rows are governed in rwb-decision and arrive in the package |
| Not in the model | the re-appraisal order and the cycle state | the order reference and the cycle date | Not stored: the cycle is the Schedule and the workflow's durable state, and the order is rwb-valuation's row (ASM-4761) |

Field IDs are those of the TSD S5 Assets and auction v2 T3.1 and the Logical Data Model and Data Dictionary v9 (DF-COL-028, DF-COL-029, DF-COL-031 and DF-COL-041 are not yet in that model), and the ACE rows are the rows the legacy story lists in its Data table, with their owner changed to P1 by the target. **No new table, no new column and no migration**: this story reads `asset` and the listing round, writes the decision record and the idempotency row through the platform libraries, and adds nothing to the schema. The three rule inputs the legacy Data table implies and the model does not hold — `appraisal_date`, `one_year_rule_applied` and `relist_count` — arrive on the owners' facts and are carried as inputs of the decision record (GAP-2869; ASM-4761). The decision log wording of AC1 and AC4 is the decision record above; the legacy wording stays in section 7.

**No personal data.** The rows this story touches carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, an order request or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes are declared by RWB-S5-E3026-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its appraisal references and its re-appraisal state (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter, and 503 when the decision library or a consumed contract does not answer. The operation IDs are those of TSD S5 T-A.1 and are not redefined here. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under ASM-0043 and is consumed, not provided; `POST /assets/{assetId}/listings` (API-S5-004) and `POST /listings/{listingId}/rounds` (API-S5-005) belong to the pricing and auction stories of this service.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the ACE valuation and NPA asset fact (operation and data-product names Not specified in the source documents (GAP-2869; ASM-4757)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | `appraisal_date`, `one_year_rule_applied`, `appraised_value`, the appraisal reference and type, the asset reference, the asset key and the book value (FSD source field names `v_ace_npa_asset.asset_key`, `asset_ref`, `asset_code`, `transfer_in_type`, `from_segment`, `transfer_in_date`, `v_ace_collateral.asset_key`, `v_ace_asset.asset_type`, carried as contract field names), with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2869; ASM-4760)) | rwb-case (P3) | P3 rwb-case | `REAPPRAISAL_ORDERED` or `RELISTED` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| `POST` of the valuation order (API-S5-003; target path Not specified in the source documents (GAP-2869; ASM-4758)) | rwb-valuation (S1) | S1 rwb-valuation | The re-appraisal order: asset reference, appraisal reference, reason code, rule version; `Idempotency-Key`; faked |

Every row is one hop with a 2 s timeout, a breaker per downstream, and a GET retried once with jitter (ADR-020). All four rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2869 with ASM-4757, ASM-4758 and ASM-4760. The E3 criteria that rest on the E4 valuation features are built against the published valuation contract and its fake (GAP-1479).

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset the topic `rwb.asset.events.v1` with `AssetTakenOn` and `AssetSold`, and both belong to the take-on and the sale stories; the S5 ownership row lists the single event EV-22, which is `AssetTakenOn`. The outcome of this step reaches rwb-case as the stage answer and its evidence reaches rwb-payment and rwb-reporting through the rating of the case, so this story adds no event, no producer and no outbox row.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is the re-appraisal cycle or the case state: the trigger is the Schedule JOB-19 and the workflow's own round result. This story therefore holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the holding | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference and the rule package in force; signals: the case state answered by rwb-case, the package in force and the approval answer |
| `orderReappraisal` | Activity, the one cycle step of this story | `rwb-asset` | The case, the asset and the appraisal fact in; the rule ID with its package version, the order reference and the case move out, with the decision record written first and the order request in the same step |

No child workflow for the case and no workflow for the valuation exists in this service. The workflow ID form and start rule of `AssetDisposalWorkflow` are Not specified in the source documents (DOR-RWB-S5-E3026-APP-8). The activity name is a target design choice and is fixed by no source document; the trigger is read as the Schedule fire and the round result, because the FSD declares no background event for the feature (FSD S5 A2.9.4.4, "No background event").

#### 12.6 Schedules

| Schedule | Cadence | Owner | What it does |
|---|---|---|---|
| JOB-19 Re-appraisal monthly | Monthly, at the reference time in force; the day and time are Not specified in the source documents (GAP-2869; ASM-4759) | rwb-asset (S5), through the workflow kit `RWB-PLT-E1071-CON` of DP-10 | Starts `orderReappraisal` for the held assets whose appraisal age reaches the re-appraisal interval |

JOB-19 is the single job of the S5 ownership rows and replaces its legacy Quartz row. DP-10 is not in the plan's pattern set for this key, so `RWB-PLT-E1071-CON` is named here and not added to the H row (GAP-2869; ASM-4759). No other Schedule, no Quartz row, no shared job table and no batch table is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | Read only here: the asset reference, its case and its holding status (ASM-4761) |
| listing | S5 (`rwb_asset`) | Read only here: the round number and the round result of the no-bid path; written by the auction story |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated cycle and the answer it holds |

Not owned and never read as a table: `recovery_case` (P3), every `v_ace_*` view (P1), `valuation` and the order (S1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `proceeds` (P8). No foreign key leaves the schema and `asset.case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data valuation fake | The appraisal of asset `AST-2026-000511` with `appraisal_date` older than 12 months and `one_year_rule_applied` = N; the same fact inside 12 months; the flag already applied; a stale product with its date; no answer beyond 2 s | AC1, X4, X5, X6 |
| rwb-case state and move fake | The states `ASSET_HELD` and `NO_BID_AT_FLOOR` of case `RC-2026-000511`; the moves `REAPPRAISAL_ORDERED` and `RELISTED` accepted; a move refused; a case in another state | AC1, AC2, X3 |
| rwb-valuation order fake | The order accepted with its order reference; an order refused; no answer beyond 2 s | AC1, AC2, X5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-15, R-DIS-44 and R-DIS-06; a package whose re-list limit is reached | AC1, AC2, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Temporal Schedule stub (`RWB-PLT-E1071-CON`) | A Schedule that fires the step for the due assets, and one that is paused | AC1, X5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for asset `AST-2026-000511` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data read, of the case-move answer and of the valuation order are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2869).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-source-data fact read, the rwb-case state read, the case-move answer and the rwb-valuation order; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; EV-22 `AssetTakenOn` belongs to RWB-S5-E3019-APP and `AssetSold` to the sale stories |
| Temporal | 1 workflow, 1 activity, 1 Schedule | `AssetDisposalWorkflow`, `orderReappraisal` and JOB-19 on `rwb-asset` |
| File | None | No file is read, built or delivered here; the SVAF exchange is rwb-valuation's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `reappraisal`, Java package `th.co.scb.ace.workbench.recovery.asset.reappraisal`; front end `src/modules/recovery/asset/AssetReappraisal.tsx`, the fragment SCR-21 and SCR-23 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the appraisal facts are the ones the rwb-source-data contract answers (BR2). DP-03 is the transaction rule of the step: the record and the order request commit together or not at all. DP-13 moves the base of the two reads and nothing else. DP-19 is how SCR-21 and SCR-23 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The four consumed rows (rwb-source-data, rwb-case state, rwb-case move and rwb-valuation order) are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-2869). DP-10 is not in the pattern set although JOB-19 is a job of this service, so the Schedule library `RWB-PLT-E1071-CON` is named as the wave 0 row the step needs and is not added to the H row (ASM-4759).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` re-appraisal branch | Workflow | The stage that waits for the Schedule fire or the round result, loads the package in force and reports the outcome to the parent |
| `orderReappraisal` | Activity | The one step: read the facts and the case, evaluate R-DIS-15 or R-DIS-44, write the record, place the order, answer the case move |
| `ReappraisalEvaluator` | Service | The rule evaluation against the DISPOSAL package version in force, with the interval, the flag and the re-list limit as package values |
| `ReappraisalDecisionRecordWriter` | Library adapter | Writes the decision record before anything else, hash-linked, and refuses the step when the write fails (DP-03) |
| `ReappraisalOrderClient` | Client | The valuation order of API-S5-003 on rwb-valuation, one hop, 2 s, `Idempotency-Key`, breaker |
| `SourceDataAppraisalClient` | Client | The read of the ACE valuation and NPA asset fact on the rwb-source-data contract, one hop, 2 s, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `ReappraisalSchedule` | Schedule registrar | Registers JOB-19 on `rwb-asset` through the workflow kit and starts the step for the due assets |
| `AssetController` | Controller | The two reads, the capability area and right, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 |
| `AssetReappraisal` | React component | Shows the appraisal age and the re-appraisal state on SCR-21 and SCR-23, read only, with the refusal, not-recorded and stale-data states |

**Database and migrations.** No Flyway file. `asset` and `listing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No column is added for the appraisal date, the one-year flag, the re-list count or the order: those are the owners' facts and the workflow's state (ASM-4761).

**Configuration and reference data.**

- `LOV-HOLDING` and the DISPOSAL route states at their version in force (TSD S5 T3.2), read as reference data and never as constants.
- The reference-data contract is the DISPOSAL rule package of rwb-decision (P7), read on `RulePackageInForce`; the parameters read through it by name are the 12-month interval, the one-year flag, the re-list limit and the 10-working-day target (BR7). DP-06 and DP-07 are not in this story's pattern set, so the package read is the contract stated here.
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the 12-month interval, the one-year flag, the re-list limit and the 10-working-day target are values of the package.
- The reference time and day of JOB-19, which no source gives, carried as a parameter with the placeholder.
- The re-appraisal interval (12 months, the value of R-DIS-15 in the package) and the provision step thresholds, steps and percentages are versioned parameters owned by the NPA and asset manager; the provision values are Not specified in the source documents (GAP-1468), and the criteria read the loaded version with its value shown on the asset record.
- The fixed clock, the JOB-19 window control, the SVAF interface ID and its file pattern, the field ID of the one-year flag, the harness seeding set and the evidence format are not in any source read (GAP-0427); they are assigned to the wave 2 entry check.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The re-appraisal branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`.
2. `ReappraisalSchedule` and JOB-19, with the paused and the fired paths and the due-asset selection (AC1, X5).
3. `SourceDataAppraisalClient` and `CaseStateClient` against their fakes, with the 2 s budget, the breaker, the stale path and the no-answer path (AC1, X4, X5).
4. `ReappraisalEvaluator` over the DISPOSAL package, with R-DIS-15, R-DIS-44, the limit-reached path and the no-fire path (AC1, AC2, X6).
5. `ReappraisalDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `ReappraisalOrderClient` with the `Idempotency-Key`, the accepted and refused answers and the repeat rule (AC1, AC2, X7).
7. `CaseMoveAnswer` and the parent signal, with the two moves (AC1, AC2, X3).
8. `AssetController` and the two reads with the rights, the pagination and the problem mapping (AC1).
9. `AssetReappraisal` on SCR-21 and SCR-23 through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, and no write to `rwb_case` (owner rwb-case), `rwb_valuation` (owner rwb-valuation) or `rwb_decision` (owner rwb-decision), each reached only on its owner's contract (X8, BR2, BR6).

**Feature flag.** `rwb.asset.reappraisal-cycle-v1`, read as a flag of the platform library; off means the Schedule is paused and the step places no order and answers no move, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic appraisal fact and from a synthetic no-bid round in SIT, each of the two rules produces its record, its order and its move, a repeated cycle places one order, a forced record failure changes nothing, JOB-19 is registered as a Schedule and not as a Quartz row, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-23 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-002 | The appraisal of the asset is older than a year, which is the trigger of R-DIS-15; raised on SCR-21 and SCR-23 as a warning (VR-S5-009-1) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are values of the pricing story, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-GEN-001 | A required field of a read request is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset or the listing (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the order is placed (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are those of the legacy message set and of FSD S5 A2.9.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-21 Asset list in its loading and list states, with its empty, error and no access states Not specified in the source documents (CG-ALL-9836), and SCR-23 Listing and price in its draft, below-limit, approved and published states, with its empty, loading, error and no access states Not specified in the source documents (CG-ALL-9837), are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status, its appraisal age and its re-appraisal state, rwb-case for the case and its route state, rwb-source-data for the appraisal fact and rwb-valuation for the valuation references; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the warning and re-appraisal-order state of SCR-21 — the asset with an appraisal older than the interval, the order raised and its reason — and the not-recorded and refused states on the same screens: refused with MSG-P4-002, not recorded with MSG-P7-003. The price ladder, the below-limit approval and the publication of SCR-23 belong to the pricing and auction stories of this service and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-026-01 | AC1 | Component | The appraisal of asset `AST-2026-000511` older than 12 months with the one-year flag not applied; the record, the order and the `REAPPRAISAL_ORDERED` answer asserted on the fakes |
| TC-E3-026-02 | AC2 | Component | Case `RC-2026-000511` at `NO_BID_AT_FLOOR` with the re-list count below the limit; the `RELISTED` answer and the re-appraisal order of the same cycle asserted |
| TC-E3-026-03 | run by RWB-ITG-E3026-ITG | Integration | The `ASSET_HELD` case with the cycle due, run end to end with rwb-source-data, rwb-case and rwb-valuation in SIT: the end-to-end evidence of R-DIS-15 is owned by RWB-ITG-E3026-ITG, and this story keeps the component half under TC-E3-026-01 |
| TC-E3-026-04 | AC4 | Component | The decision-record stub stopped; no order, no answer and MSG-P7-003 shown |
| TC-E3-026-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E3-026-06 | Principle 5 | Component | A forced decision record write failure at the moment of the order; nothing written |
| TC-E3-026-07 | Section 12 operations, events and activities | Contract | The operations, events and activities of section 12 checked against the consumed bases of section 12.2 and the workflow and activity rows of section 12.5; the test fails on any name outside those rows |
| TC-E3-026-08 | Section 12.7 tables | Component | Boundary test of the tables of section 12.7: `asset` and `listing` read only; `decision_record` and `idempotency_key` written only through the platform libraries; a write to any other table or any `v_ace_*` read fails |
| TC-E3-026-09 | AC5 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3026-APP-AC5) |
| TC-E3-026-10 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3026-APP-AC6) |
| TC-E3-026-11 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3026-APP-AC7) |
| TC-E3-026-12 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3026-APP-AC8) |
| TC-E3-026-13 | AC10 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3026-APP-AC10) |
| TC-E3-026-14 | AC9 | Component | A consumed contract fake answering with an error for case `RC-2026-000511`; no case move answered, asserted on the fakes |

The six legacy cases are the legacy cases of RWB-E3-026 in their legacy order, with the Level column added: a case that runs on the fakes maps to `Component`, and TC-E3-026-03 maps to `Integration` because it crosses the rwb-source-data, rwb-case and rwb-valuation boundaries and because the plan gives AC3 to the wave 2 harness. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness, which copies none of the other criteria.

### 17. Guardrails

- No business value in code: the 12-month interval, the one-year flag, the re-list limit, the 10-working-day target, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in an order request, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case and the valuation with rwb-valuation: no `recovery_case` row, no valuation row, no appraisal value, no price and no SVAF call is written here (BR4, BR5).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base `/api/recovery/v1`, no second topic and no event of this step.
- The decision is recorded before the order and the order carries its `Idempotency-Key`; a build that places an order outside the step or without a record fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule (FSD S5 requirements served, Must, E3); the split plan carries no requirement id for this slice (GAP-2869; ASM-4763) | FEAT-AST-09 | Not specified in the source documents (DOR-RWB-S5-E3026-APP-2) | The Schedule, the evaluator, the order and the case move | TC-E3-026-01, TC-E3-026-02, TC-E3-026-04 |
| ADR-013 | 19 services inside ACE | FEAT-AST-09 | Not specified in the source documents (DOR-RWB-S5-E3026-APP-2) | rwb-asset as the owner of the asset and the cycle | TC-E3-026-01 |
| ADR-014 | Schema and login per service | FEAT-AST-09 | Not specified in the source documents (DOR-RWB-S5-E3026-APP-2) | `rwb_asset` and its own login | TC-E3-026-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | FEAT-AST-09 | Not specified in the source documents (DOR-RWB-S5-E3026-APP-2) | JOB-19 as a Temporal Schedule | TC-E3-026-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | FEAT-AST-09 | Not specified in the source documents (DOR-RWB-S5-E3026-APP-2) | The four consumed rows with their budget | TC-E3-026-03 |
| ADR-022 | Local decision record plus central ledger | FEAT-AST-09 | Not specified in the source documents (DOR-RWB-S5-E3026-APP-2) | The decision record written before the order | TC-E3-026-04, TC-E3-026-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-026, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC4, owned word for word by this story; AC3 is the harness's (RWB-ITG-E3026-ITG) |
| Test cases | TC-E3-026-01 to TC-E3-026-06 |
| Feature and screens | FEAT-AST-09, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-44, R-DIS-15 and R-DIS-06, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Job | JOB-19 Re-appraisal monthly, the single job of the service |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two reads, the appraisal and order elements, the case-move answer, the consumed rows, the error set and the fakes: RWB-S5-E3026-CON.
- AC3 and its end-to-end evidence across rwb-source-data, rwb-case and rwb-valuation: RWB-ITG-E3026-ITG (ASM-4762).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (ASM-4760).
- The valuation itself: the valuer, the SVAF exchange, the appraisal value, R-DIS-16 to R-DIS-18 and API-S5-003 as a provided operation belong to rwb-valuation (S1) (ASM-4758).
- The ACE valuation and NPA asset facts and the freshness of the data product: rwb-source-data (P1) (ASM-4757).
- The holding-age clock, the provision steps and the monthly cost of carry: RWB-S5-E3023-APP, with the posting in rwb-payment (P8).
- The listing, the price ladder, the auction rounds, the five-day payment term and the sale: the pricing and auction stories of this service, API-S5-004 and API-S5-005.
- The authoring, testing, approval and versioning of the DISPOSAL package and of R-DIS-15, R-DIS-44 and R-DIS-06: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its Schedule pause, its dashboards, its alerts and its runbook: the operations story of this legacy key.

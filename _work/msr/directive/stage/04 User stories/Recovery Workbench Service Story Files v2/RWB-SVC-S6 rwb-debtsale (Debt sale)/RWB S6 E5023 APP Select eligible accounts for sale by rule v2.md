# RWB-S6-E5023-APP Select eligible accounts for sale by rule

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 (lot features with EP05 on the S6 service; award, transfer and posting features in a later wave, wave number Not specified in the source documents (GAP-1484), with EP06 on the same service and schema) |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-A |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S6-E5023-APP-16); the squad sizes the story at refinement |
| Depends on (build) | RWB-S6-E5023-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-case case list and case-move answer; rwb-source-data COLLINS score product; rwb-decision DEBTSALE package read (class C, operation names as placeholders; GAP-2973; GAP-1947); rwb-decision rules component and approval routing by limit (FEAT-DRI-07, FEAT-APD-01, P7 contract); rwb-source-data access control per data product (FEAT-RDF-15, P1 contract); FSD dependency codes FEAT-DBS-05 and FEAT-DBS-16 |
| Contract version | v1 (base path /api/recovery/debtsale/v1) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S6-E5023-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Source modules | FSD S6 Debt sale v3: 03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-s6-debt-sale-v3.md; TSD S6 Debt sale v2: 05-technical-architecture (v5_extracted folder)/recovery-workbench-tsd-s6-debt-sale-v2.md (read directly; no S6 extract in _work/msr/extract) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the eligibility slice of RWB-E5-023 in rwb-debtsale. The three legacy criteria are kept word for word with their origin tag; the step evaluates the DEBTSALE package (R-DS-01, with R-DS-02 and R-DS-03 on the exclusion paths), writes the `debt_sale_lot` and `debt_sale_account` rows of the selected population in `rwb_debtsale`, records the decision through the local decision-record library before any row changes (DP-03), answers rwb-case for the case move `LOT_BUILT` and serves API-S6-001 and API-S6-002 on base `/api/recovery/debtsale/v1` (DP-13), reached from SCR-25 through the gateway-bff composite route (DP-19). The 54 percent cap named in AC1 is carried by FEAT-DBS-16 and by rule R-DS-19, both of E6 and of RWB-S6-E6005-APP; the case list, the COLLINS score product and the package read are consumed rows the plan's None C row does not name; DP-09 is absent although the service owns a topic; `deviation_open` and `fraud_flag` have no field in any source. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E5023-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (42 resolved, 13 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer (RW-DEBTSALE)**, I want **the Workbench to apply the eligibility rules, including the 54 percent cap, to pick the sale population**, so that **debt sales run on approved lots and masked data**.

This is the eligibility slice of legacy RWB-E5-023. It owns:

- the three legacy criteria this story owns (AC1, AC2, AC3), copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, as the stage child of `CaseWorkflow` and as the step that runs ahead of the saga's pivot, the transfer (Temporal and Drools Design slide 5, S6 "monthly sale cycle"; slide 12, saga runner for S6; slide 13); the lot is identified by its lot number for the sale steps, and the case side is moved by rwb-case on the events LotAwarded and AccountsTransferred of the topic, which later stories publish, never by a write into the case schema (GAP-1780).
- the read of the case list of a monthly cycle and the evaluation of R-DS-01, R-DS-02 and R-DS-03 against the DEBTSALE package version in force (FSD S6 A2.1; TSD S6 T4);
- the creation of the `debt_sale_lot` row of the population and one `debt_sale_account` row per selected account in `rwb_debtsale`, within the columns of DF-SAL-020 to DF-SAL-037 that this step fills;
- the local decision record of each outcome, written through RWB-PLT-E1027-CON before the rows change (DP-03), with the rule ID, the package version and the case move;
- the answer to rwb-case for `LOT_BUILT`, and for `CASE_EXCLUDED` or `BACK_TO_CASE_LIST` on the exclusion paths, with the rule and its version;
- the eligibility half of API-S6-001 `POST /debt-sale-lots` and the lot-built answer of API-S6-002 `GET /debt-sale-lots/{lotId}` on base `/api/recovery/debtsale/v1`, and the selection state of SCR-25 Lot builder behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two operations, the `LotRequest` and `DebtSaleLot` elements, the fields DF-SAL-020 to DF-SAL-037, the four closed lists, the consumed rows, the case-move answer, the error set and the fakes, which are RWB-S6-E5023-CON; the grouping and pricing of the population and the minimum lot size test of R-DS-05, which are RWB-S6-E5024-APP; the masked tape (RWB-S6-E5025-APP), the data room (RWB-S6-E5026-APP), the committee approval (RWB-S6-E6001-APP), the buyer qualification (RWB-S6-E6002-APP), the award with the cap test of R-DS-19 (RWB-S6-E6005-APP) and the transfer (RWB-S6-E6007-APP); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the COLLINS scores and the ACE data products, which are rwb-source-data's (P1); the DEBTSALE package, which is rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the Workbench applies the eligibility rules to the case list of a cycle to pick the sale population (FSD S6 A2.1.1), because debt sales run on spreadsheets with no baseline turnaround (FSD S6 A1.3), and the turnaround is measured on the decision log and the Workbench records against a target of 45 days, reviewed monthly (FSD S6 A2.1.1). The requirement is REQ-S6-001, "Accounts eligible for sale are selected by rule against the policy cap" (FSD S6 Requirements served). What D-RCV-60 changes is who owns the population, the case list, the score and the package.

- **The population is this service's.** `debt_sale_lot` and `debt_sale_account` are S6's two tables in `rwb_debtsale` (context pack, ownership rows owned by S6; TSD S6 T3.1), so the selected population is recorded here and nowhere else.
- **The case list stays with rwb-case.** `recovery_case` and the route state `LOT_CANDIDATE_SELECTED` are P3's; this step reads the list, evaluates the rule, writes its rows, records the decision and **answers** the case move to `LOT_BUILT` (ASM-4888).
- **The COLLINS score stays with rwb-source-data.** The FSD names the integration point as ACE with the COLLINS scores ingested by ACE and read through `v_ace_score`, and in the target only rwb-source-data holds those views, so the score arrives on the owner's data-product contract and no `v_ace_*` grant is requested here (ASM-4883).
- **The package is read, not embedded.** The DEBTSALE route set is 41 rules over 29 states (TSD S6 T4), authored, tested and approved in rwb-decision; DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-4884).
- **The decision is recorded first**, in the same transaction as the lot and account rows, which is what legacy AC1 asked for and legacy AC3 tested.
- **The cap is a rule fact, not this step's test.** AC1 says the eligibility step applies the 54 percent cap, while no row of R-DS-01, R-DS-02 or R-DS-03 tests it: the only cap row of the route set is R-DS-19 at `BIDS_RECEIVED` to `AWARD_PENDING`, and the measure itself has its own feature, FEAT-DBS-16 "Apply the debt sale cap", first in E6. Both belong to RWB-S6-E6005-APP. This story reads the cap value from the package and records it with its version, and does not claim the cap test (ASM-4886).
- **The eligibility inputs have no named owner.** R-DS-01 tests `deviation_open = none` and R-DS-02 tests `deviation_open in (X1 to X7) or fraud_flag = Y`, yet neither the S6 field list (TSD S6 T3.1) nor the legacy Data table names those fields, so they are consumed rule inputs with a placeholder (ASM-4887).

No business value moves: the eligibility condition, the deviation codes X1 to X7, the cap, the monthly cycle and the four closed lists are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S6-E5023-CON is published: the two operations, the `LotRequest` and `DebtSaleLot` elements, the fields DF-SAL-020 to DF-SAL-037, the four closed lists, the consumed rows, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case case-list read is published with its fake, so the cases of the cycle can be read on Day 1: the case reference, the case number, the product group, the segment, the account link and the state. The operation name and the row that carries the eligibility facts are Not specified in the source documents (GAP-2973; ASM-4883, ASM-4887).
- The rwb-source-data data-product contract that carries the COLLINS score is published with its fake, with the as-of date of the product; its operation name is Not specified in the source documents (GAP-2973; ASM-4883), and the row is in this story's contract-dependency list (GAP-2973).
- The rwb-decision rule-package read is published with its fake and answers the DEBTSALE package at its version in force, with R-DS-01, R-DS-02 and R-DS-03 among its 41 rules over 29 states; its operation name is Not specified in the source documents (GAP-2973; ASM-4883, ASM-4884).
- The case-move answer of rwb-case is available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2973; ASM-4888). The case boundary is declared as the input, the signals and the stage outcome of the child workflow (GAP-2974).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so the lot and account rows and their record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-25 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The DEBTSALE package is in force at its version and is read on its package read; the rule rows, the deviation codes X1 to X7 and the reference data of the four lists are governed in rwb-decision and are not a build item of this story.
- The service runs as its own login on schema `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_score` or `rwb_case` is refused by the database and fails the boundary test (ASM-4883).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S6-E5023-CON when its tests pass.
- The four consumed rows of this step (the rwb-case case list, the rwb-source-data COLLINS score, the rwb-decision package read and the rwb-case case-move answer) are declared in section 12.2 with the operation-name placeholder and the fakes of section 12.8; the DEBTSALE package is read as data on the owner's read and is not embedded in this service (GAP-1947).
- RWB-PLT-TE006-CON, the outbox and inbox library, is the wave 0 library the service's topic rwb.debtsale.events.v1 needs; RWB-PLT-E1072-CON is the rule kit the evaluation needs, its second story key Not specified in the source documents (CG-ALL-10325); the 54 percent cap value is read from the package and its test stays with RWB-S6-E6005-APP with FEAT-DBS-16; REQ-S6-001 is the traceability reference from the FSD (GAP-2973).

### 4. Flow

1. The monthly debt sale cycle opens and ACE has ingested the COLLINS scores of the population. rwb-source-data publishes the score as a data product with its business date; this service reads no ACE view and runs no inbound load (FSD S6 A1.4; FSD S6 A2.1.2 step 1).
2. The eligibility step of `DebtSaleWorkflow` on queue `rwb-debtsale` receives its trigger from the Temporal Schedule or event-started workflow that opens the monthly cycle (schedule name: Not specified in the source documents (GAP-1781)), recording the cycle date it ran for, read as the opening of the cycle for a case list in `LOT_CANDIDATE_SELECTED` because R-DS-01 carries "per monthly cycle" as its timer and the FSD declares no background event (FSD S6 A2.1.4.4).
3. The step reads the version of the DEBTSALE package in force from rwb-decision, with its rule rows, the cap value and the reference data the rules need, one hop with a 2 s budget and a breaker (ASM-4883, ASM-4884).
4. The step reads the case list of the cycle on the rwb-case contract: the cases in `LOT_CANDIDATE_SELECTED` with their case reference, case number, product group, segment, account link and the eligibility facts of the rule, read only; it never reads `recovery_case` (ASM-4883, ASM-4887).
5. The step reads the COLLINS score of those cases on the rwb-source-data data-product contract, with the as-of date. A product that is stale after a late or failed ACE batch holds the step with VR-S6-001-1 and MSG-P1-001, and nothing is written (ASM-4883).
6. `EligibilityEvaluator` evaluates R-DS-01 on each case: where the eligibility rule passes and `deviation_open = none`, the case is selected for sale. Where `deviation_open in (X1 to X7)` or `fraud_flag = Y`, R-DS-02 removes the account from the pool with a recorded reason and it is reported with MSG-S6-001. Where an excluded account is clear on a later cycle, R-DS-03 returns it to the case list (FSD S6 A2.1.3.1; Business Rules and Routing Logic v4).
7. The evaluation answers the rule ID, the package version, the action of the rule, the cap value the package carries and the case move the rule names. Where no rule fires, the step changes nothing for that case and reports the reason to the parent.
8. `DebtSaleDecisionRecordWriter` writes one decision record per outcome through the local decision-record library, **before any change**: the case reference, the account reference, the rule ID with its package version, the inputs reference with the as-of date of the score product and the version of the case list, the cap value in force, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3). Where the central ledger confirmation is strict, the activity waits for the ledger acknowledgement on the retry policy of section 7 with a timeout Not specified in the source documents (GAP-2018); on timeout the workflow fails with an incident and does not repeat a completed step.
9. `SaleLotWriter` inserts the `debt_sale_lot` row in one `rwb_debtsale` transaction with the decision record and the idempotency row, filling the lot columns of §11 and setting `status` to `BUILDING` of `LOV-LOT-STATUS` as the business status and `state` to `LOT_BUILT` of the routing ladder as the workflow state, both recorded on the lot and neither inferred from the other; the reserve, the terms, the buyer and the authority stay empty, as they belong to RWB-S6-E5024-APP, RWB-S6-E6001-APP and the award stories.
10. `SaleLotAccountWriter` inserts one `debt_sale_account` row per selected account in the same transaction, filling the account columns of §11 with `outstanding` from the COLLINS-fed balance and `put_back_status` at `NONE` of `LOV-PUTBACK`; `selling_price` stays empty until RWB-S6-E5024-APP writes the estimate.
11. `CaseMoveAnswer` answers rwb-case for each case of the list with the move the rule names — `LOT_BUILT` for a selected case, `CASE_EXCLUDED` for an account removed under R-DS-02 and `BACK_TO_CASE_LIST` for one returned under R-DS-03 — with the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row; this service writes neither the row nor the state (ASM-4888).
12. A repeated trigger with the same cycle, cut-off date and case-list version writes no second lot, no second account row and no second record, sends no second answer and counts the repeat; the `Idempotency-Key` of a repeated POST answers the lot it created.
13. SCR-25 Lot builder shows the population in its selection state — the selected accounts, the excluded accounts with their reason, the segment and the cut-off date — from this service through the gateway-bff composite route, read only, next to the case state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no lot row, no account row and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E5-023-03, TC-E5-023-05 |
| X2 | The role does not hold the Debt sale right of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC4, TC-E5-023-04, TC-E5-023-08 |
| X3 | The case is not in `LOT_CANDIDATE_SELECTED`, or has left the case list since it was read | 409 and nothing is written for that case; a case that has already moved is not re-evaluated | Not specified in the source documents (GAP-2974) | AC2, X6 |
| X4 | The COLLINS data product is stale after a late or failed ACE batch | The step holds, writes nothing and shows the data date; the selection resumes on the next fresh answer | MSG-P1-001 | AC1, X5 |
| X5 | The rwb-case, rwb-source-data or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | Not specified in the source documents (GAP-2974) | AC1, X6 |
| X6 | The case carries an open deviation or a fraud flag, or satisfies no rule of the package | R-DS-02 removes the account with a recorded reason, or no rule fires and the case keeps its state; the population is written without it | MSG-S6-001 | AC1, AC2, X3 |
| X7 | A repeated trigger for the same cycle, cut-off date and case-list version, or the same `Idempotency-Key` twice | One lot, one set of account rows, one record and one answer per case; the repeat is counted and the key answers the lot that exists | Not specified in the source documents (GAP-2974) | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC5, TC-E5-023-07, Section 17, BR3, BR5 |

X1 to X3 are the legacy exception paths carried onto the slice, X4 to X7 are the paths the target call types and the once-per-cycle trigger add, and X8 is the ACE and schema boundary. The deviation codes X1 to X7 of R-DS-02 are codes of the rule package and are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E5023-CON, the rwb-case, rwb-source-data and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the two operations and the table columns are fixed |
| Valuable | The population of a cycle is selected by rule with its decision recorded and the case moves in the service that owns it, so the 45-day turnaround is measurable |
| Estimable | One workflow step, one evaluator, one record write, two row writers, one case-move answer, three clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic case list and synthetic COLLINS scores through the contract fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Select eligible accounts for sale by rule

  Background:
    Given case "RC-2026-000601" is one of 340 cases in state "LOT_CANDIDATE_SELECTED" on the case list of the monthly debt sale cycle
    Given the DEBTSALE rule package is in force at its version and carries R-DS-01, R-DS-02 and R-DS-03
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Select eligible accounts for sale by rule (legacy RWB-E5-023 AC1)
    Given the rwb-source-data contract mock returns the COLLINS score data product of the 340 cases with as-of date "2026-11-30"
    Given the rwb-case contract mock returns the case list of the cycle with 340 cases in state "LOT_CANDIDATE_SELECTED"
    Given the data and the rule version this feature needs are in place
    Given the rwb-decision contract mock returns the DEBTSALE package at its version in force
    Given the rwb-source-data contract mock returns the COLLINS score with its as-of date
    When its trigger arrives
    Then applies the eligibility rules, including the 54 percent cap, to pick the sale population
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DS-01 (legacy RWB-E5-023 AC2)
    Given the rwb-case contract mock returns the case state "LOT_CANDIDATE_SELECTED" for "RC-2026-000601" and accepts the move "LOT_BUILT"
    Given a case in state LOT_CANDIDATE_SELECTED
    When debt sale cycle opened
    Then select the accounts for sale from the case list
    Then the case moves to LOT_BUILT

  Scenario: AC3 Not recorded (legacy RWB-E5-023 AC3)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 Access (exception X2) (new, D-RCV-60)
    Given the role does not hold the Debt sale right of the operation
    When the lot selection is requested
    Then nothing changes and the caller sees 403 with MSG-P4-002

  Scenario: AC5 Statement boundary (exception X8) (new, D-RCV-60)
    Given a component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails

  Scenario: AC6 Business rule guardrails (BR1 to BR10) (new, D-RCV-60)
    Given the rwb-debtsale service and its schema are built
    When the guardrail and boundary checks run
    Then each of BR1 to BR10 holds and the build fails when one does not

  Scenario: AC7 Error answers of the provided operations (new, D-RCV-60)
    Given a call to API-S6-001 or API-S6-002 without a valid token, without the right, or to a path that does not exist
    When the call is answered
    Then the caller sees 401, 403 or 404 with the platform error envelope and nothing is read or written

  Scenario: AC8 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given a write with an Idempotency-Key has already been answered for the cycle and case-list version
    When the same Idempotency-Key is sent again
    Then one lot, one set of account rows, one record and one answer per case exist and the key answers the lot that exists

  Scenario: AC9 Activity retry and timeout (new, D-RCV-60)
    Given a consumed call takes longer than 2 s
    When the workflow activity times out and is retried on its own schedule
    Then nothing is written on the timed-out attempt and the retry writes one set of rows

  Scenario: AC10 Failed consumed call (new, D-RCV-60)
    Given a consumed contract fails or does not answer inside 2 s or its breaker is open
    When the step runs
    Then it holds, nothing is written, no move is answered and the caller sees 503 with the platform error envelope

  Scenario: AC11 Disallowed status change (new, D-RCV-60)
    Given a status change is requested that no row of section 8 allows
    When the change is requested
    Then the change is refused, nothing is written and no move is answered
```

The three criteria are the legacy criteria of RWB-E5-023 word for word, with their origin tag added and the two `decision log` phrases changed to `decision record` (CG-ALL-10336): the repeated `Then`, the wording of `its trigger arrives`, `debt sale cycle opened` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry one to three `Given the <service> contract mock returns <x>` lines, and those are the only additions. What the legacy lines describe happens in four places now: rwb-case answers the case list and writes the move; rwb-source-data answers the COLLINS score, which the FSD named as `v_ace_score`; rwb-decision holds the package at its version; and this story evaluates the rules, writes the record and the rows and answers the move. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_debtsale`, with the central `decision_log_entry` ledger of rwb-decision behind it. Two points are recorded rather than smoothed over: AC1 names the 54 percent cap, which no row of R-DS-01 to R-DS-03 tests and which R-DS-19 and FEAT-DBS-16 carry at the award (ASM-4886); and AC1 reads as the outcome of the cycle while AC2 reads the same step at the case, so one step produces both and neither duplicates the other.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DS-01 | Debt sale | D8.4 | LOT_CANDIDATE_SELECTED | DEBT_SALE_CYCLE_OPENED | eligibility rule passes and deviation_open = none | Select the accounts for sale from the case list | LOT_BUILT | Debt sale officer | Rules component, Recovery Data Store | per monthly cycle |
| R-DS-02 | Debt sale | D8.4 | LOT_CANDIDATE_SELECTED | ACCOUNT_EXCLUDED | deviation_open in (X1 to X7) or fraud_flag = Y | Remove the account from the pool with a recorded reason | CASE_EXCLUDED | Case owner | Workbench, Aric | None |
| R-DS-03 | Debt sale | D8.4 | CASE_EXCLUDED | EXCLUSION_CLEARED | deviation_open = none | Return the account to the case list for the next cycle | BACK_TO_CASE_LIST | Debt sale officer | Workbench | next cycle |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target the "Rules component" is the DEBTSALE package read from rwb-decision (P7) and evaluated here, the "Recovery Data Store" is `rwb_debtsale`, "Workbench" is SCR-25 and "Aric" is the collection system whose deviation flag ACE carries. The case moves are written by rwb-case on this story's answer, and the lot and account rows are written here. R-DS-19, the only row that tests the 54 percent cap, is not tabled here (ASM-4886).

| ID | Rule | Source |
|---|---|---|
| BR1 | The population is this service's: `debt_sale_lot` and `debt_sale_account` are rows of `rwb_debtsale`, and no other service writes them | Context pack ownership rows (both S6); TSD S6 T3.1; FSD S6 A2.1.2 |
| BR2 | The decision is recorded before the lot and account rows change, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2 ("writes the decision log entry before any change"); legacy AC1 and AC3 |
| BR3 | The COLLINS score stays with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the score on the owner's contract with its as-of date | DP-05 as a prohibition; FSD S6 A2.1.2; ASM-4883 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states `LOT_CANDIDATE_SELECTED`, `LOT_BUILT`, `CASE_EXCLUDED` and `BACK_TO_CASE_LIST` are rwb-case's | ASM-4888; TSD S6 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `account_id` is an identifier of another service's fact | DP-01; TSD S6 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: the eligibility condition, the deviation codes X1 to X7, the cap, the cycle and `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` | TSD S6 T3.2; FSD S6 BR-S6-001; legacy Guardrails |
| BR7 | The eligibility inputs `deviation_open` and `fraud_flag`, and the cap value, are read as rule inputs and never as constants | FSD S6 A2.1.3.1; Business Rules and Routing Logic v4; ASM-4886, ASM-4887 |
| BR8 | The same trigger twice, or the same `Idempotency-Key` twice, writes one lot, one set of account rows, one record and one answer per case | TSD S6 T-A.2 |
| BR9 | No person name, address, contact value or identity number enters `rwb_debtsale`, the decision record, a log or a workflow input; `borrower_code` and `account_id` are codes and not identities, so they are classed as non-personal data | Template and Rules §R7.2 (s17); TSD S6 T6.2 |
| BR10 | The lot status vocabulary is closed: a lot created from a selection is `BUILDING` of `LOV-LOT-STATUS`, and this step writes no priced, approved or awarded state | TSD S6 T3.2, T4 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the lot status of `debt_sale_lot` and the state of the step.

| From (`debt_sale_lot.status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | A selection under R-DS-01 | eligibility rule passes and deviation_open = none | A row in `BUILDING`, with the answer `LOT_BUILT` per selected case |
| None, no row | An exclusion under R-DS-02 | deviation_open in (X1 to X7) or fraud_flag = Y | No row for the account, its reason recorded, the answer `CASE_EXCLUDED` |
| None, no row | A clear under R-DS-03 | deviation_open = none on a later cycle | No row yet: the account returns to the case list with the answer `BACK_TO_CASE_LIST` |
| BUILDING | The lot build and price step | lot agent estimate returned with COLLINS | `BUILDING` unchanged until RWB-S6-E5024-APP writes the reserve and the terms |
| BUILDING | The committee approval of R-DS-06 | reserve and terms approved inside the delegation | `OFFERED`, by RWB-S6-E6001-APP |
| BUILDING | A repeated trigger for the same cycle, cut-off date and case-list version | X7 | Unchanged, the repeat is counted |
| None, no row | A case that satisfies no rule of the package | X6 | No row, no record and no answer |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The cycle opens for a case list in `LOT_CANDIDATE_SELECTED` | The package in force is read | Evaluating |
| Evaluating | R-DS-01 or R-DS-02 fires on the case | The decision record is written | Applying |
| Applying | The lot and account rows are written and the answers sent | The transaction commits | Waiting for the next cycle |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Evaluating | The COLLINS data product is stale | X4 | Held, until a fresh answer |

The route states are those of the DEBTSALE machine of TSD S6 T4 and live on the case of record. The lot status values are those of `LOV-LOT-STATUS` in TSD S6 T3.2; this step writes `BUILDING` only, and `OFFERED`, `AWARDED`, `TRANSFERRED` and `CLOSED` are the later stories'.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary role, creating the lot from the selection, reading it and re-running a cycle |
| RW-PRODHEAD, product head | Debt sale RA: reads the population and approves through the approval path where the delegation reaches it |
| RW-HEADASL, head of Asset Liquidity | Debt sale RA: reads the population and approves through the same path |
| RW-SALEOFF, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, PT-RAMC | Debt sale R in this step: the partner reaches its own lot through the partner gateway of the data room, never the selection |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-debtsale service identity | Runs the step, reads the case list, the score and the package, writes the record and the rows and answers the moves; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S6 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the debt sale officer as also-user (FSD S6 A2.1.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the officer is the primary role when a person acts, on SCR-25 and on a re-run of a cycle. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here. Each of API-S6-001 and API-S6-002 is guarded by the rwb-access authorise check against the right of the table above; the operation name of that check is Not specified in the source documents (DOR-RWB-S6-E5023-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Write, the lot reference of the row and the answer |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Write, from the lot numbering of the cycle |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Write, the cut-off date of the population |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Write, against `LOV-SEGMENT` |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Not written here: RWB-S6-E5024-APP |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Not written here: the award and buyer stories |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Not written here: RWB-S6-E5024-APP |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Not written here: the award story |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Not written here: RWB-S6-E6001-APP |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Not written here: RWB-S6-E5024-APP and RWB-S6-E6001-APP |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, against `LOV-LOT-STATUS` (`BUILDING`) |
| DF-SAL-031 | debt_sale_account (S6, `rwb_debtsale`) | id | Write, one row per selected account |
| DF-SAL-032 | debt_sale_account (S6, `rwb_debtsale`) | lot_id | Write, the lot of the row |
| DF-SAL-033 | debt_sale_account (S6, `rwb_debtsale`) | account_id | Write, from the case list of the cycle |
| DF-SAL-034 | debt_sale_account (S6, `rwb_debtsale`) | borrower_code | Write, the code the case list carries; no name |
| DF-SAL-035 | debt_sale_account (S6, `rwb_debtsale`) | outstanding | Write, from the COLLINS-fed balance of the account |
| DF-SAL-036 | debt_sale_account (S6, `rwb_debtsale`) | selling_price | Not written here: RWB-S6-E5024-APP |
| DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | put_back_status | Write, `NONE` of `LOV-PUTBACK` at insert; the claim paths are the put-back stories' |
| Standard columns | both tables (S6, `rwb_debtsale`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the rows change |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case list and the state arrive on the rwb-case contract |
| `v_ace_score` (P1) | the COLLINS score and its as-of date | Not read: no `v_ace_*` grant. Field IDs Not specified in the source documents (GAP-2973; ASM-4883) |
| `deviation_open`, `fraud_flag` | the eligibility inputs of R-DS-01 and R-DS-02 | Consumed rule inputs of the rwb-case case row and of the score product, with the field names as the placeholder; the field and its owner are Not specified in the source documents (GAP-1951; GAP-2973; ASM-4887), to be confirmed before the contract is tagged |
| decision_log_entry, rule_row (P7) | the central ledger and the rule rows | Not written and not read here: the local record is this service's and the rule rows arrive on the package read |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model and Data Dictionary, and the ACE and ledger rows are the rows the legacy Data table lists, with their owners changed to P1 and P7 by the target. The field `account_id` of DF-SAL-033 and the `decision_record` library object are not in the Logical Data Model v9 or Data Classification v5; their registration is Cross-document (Logical Data Model v9). **No new table, no new column and no migration**: the two tables arrive with the DB story of this service, this story writes eleven of their existing columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_debtsale` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3). RWB-PLT-TE006-CON is the wave 0 library the service's topic and the award and transfer stories need; this step declares no consumed event and no published event (§12.3, §12.4).

**No personal data.** The rows carry identifiers, codes, amounts, dates, list values and a rule version. No name, address, contact value or identity number enters `rwb_debtsale`, the record, a log or a workflow input, and the fixtures are synthetic. The borrower is represented by `borrower_code`, a code of the source system; `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13). This story supplies the behaviour behind the eligibility half of the create and the lot-built answer of the read, whose shapes RWB-S6-E5023-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/debt-sale-lots` | LotRequest in, DebtSaleLot out, the lot created from the selected accounts with its accounts, its segment and its cut-off date (API-S6-001) | Debt sale, right C, scope applied | `Idempotency-Key` header |
| GET | `/debt-sale-lots/{lotId}` | DebtSaleLot out, with its accounts and their status (API-S6-002) | Debt sale, right R, scope applied | Not applicable |

The errors are 401, 403 with MSG-P4-002, 409 for a repeated or conflicting lot, 422 with MSG-GEN-001 for an invalid request and 503 when the library or a consumed contract does not answer, on the create, and 401, 403, 404 and 503 on the read, as TSD S6 T-A.2 gives them. The reserve, the terms, the buyer class and the per-account price are written by RWB-S6-E5024-APP on the same two operations; `POST /debt-sale-lots/{lotId}/award` (API-S6-003) is RWB-S6-E6005-APP's, and `GET /partner/data-room/{lotId}` (API-S6-004) and `POST /partner/data-room/{lotId}/bids` (API-S6-005) are RWB-S6-E5026-APP's and the bidding stories'; none of the three is built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case list of the cycle in `LOT_CANDIDATE_SELECTED`: case reference, case number, product group, segment, account link and the eligibility facts the rule tests; read only, faked |
| The read of the COLLINS score data product (operation name Not specified in the source documents (GAP-2973; ASM-4883)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score of each case and the as-of date of the product; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-2973; ASM-4883)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEBTSALE package at its version, with R-DS-01, R-DS-02 and R-DS-03 among its 41 rules over 29 states and the cap value; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2973; ASM-4888)) | rwb-case (P3) | P3 rwb-case | The move `LOT_BUILT`, `CASE_EXCLUDED` or `BACK_TO_CASE_LIST` with the rule and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-2973; ASM-4883).

#### 12.3 Events published

None. The service publishes on `rwb.debtsale.events.v1` (event `EV-23`, `LotAwarded`, with `AccountsTransferred` beside it in the service's event set), and neither belongs to this step: the selection awards nothing and transfers no account. `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's, so this story declares no event, no producer group and no outbox row of its own, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-4885).

#### 12.4 Events consumed

None. The service subscribes to `ProceedsMatched` of rwb-payment in the settlement and transfer steps of the saga (context pack connection matrix, row S6), and it does not belong to the selection: no proceeds exist before a lot is awarded. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The trigger of the step is the ACE batch, the event or the timer of the cycle, and the FSD declares no background event for the feature (FSD S6 A2.1.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per sale cycle, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` | Input: the cycle, the cut-off date, the case-list reference and the package in force; signals: the case list answered by rwb-case, the package in force and the approval answer. This step sits before the pivot, so it needs no compensation |
| `selectEligibleAccounts` | Activity, the one eligibility step | `rwb-debtsale` | The case list, the cut-off date and the score in; the rule ID with its package version, the lot reference, the selected and excluded accounts, the cap value and the case moves out, with the record and the two row sets written in one transaction |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document; the trigger is the opening of the cycle for a case list in `LOT_CANDIDATE_SELECTED`, because R-DS-01 carries "per monthly cycle" as its timer and the FSD declares no background event. Workflow ID form: Not specified in the source documents (CG-ALL-10330). Start rule: the monthly sale cycle opens or a residual arrives from disposal (R-DS-01); start mode and duplicate-start policy: Not specified in the source documents (CG-ALL-10330).

#### 12.6 Schedules

None. The step runs from the opening of the cycle and from the case signal the parent forwards, and owns no Temporal Schedule and no legacy Quartz job. The monthly cycle of R-DS-01 is a clock of the route — its timer column reads "per monthly cycle" — and not a Schedule of this service; no Job identifier for the selection is named in the sources.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot of the population; this story inserts the row and writes the columns of §11 |
| debt_sale_account | S6 (`rwb_debtsale`) | An account in a lot; this story inserts one row per selected account |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `v_ace_score` and every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), and the later stories' data-room, bid and transfer tables of this service. No foreign key leaves the schema and `account_id` is an identifier, not a foreign key across schemas (DP-01). The COLLINS score and the ACE batch status reach this step only through the rwb-source-data contract, under the source field names v_ace_score.*, v_ace_account.* and v_ace_batch_status.*; no view and no ACE table is read here.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-list fake | The case list of the cycle with 340 cases in `LOT_CANDIDATE_SELECTED`, `RC-2026-000601` among them, with the segment, the account link and the eligibility facts; a case that has left the list | AC1, AC2, X3 |
| rwb-source-data COLLINS data-product fake | The score of the 340 cases with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s | AC1, X4, X5 |
| rwb-decision rule-package fake | The DEBTSALE package at its version in force with R-DS-01, R-DS-02 and R-DS-03, the cap value and the four closed lists | AC1, AC2 |
| rwb-case case-move fake | The moves `LOT_BUILT`, `CASE_EXCLUDED` and `BACK_TO_CASE_LIST` accepted for `RC-2026-000601`; a move refused because the case is not in the expected state | AC2, X3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-25 answer for `RC-2026-000601`, in its selection state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the score read, the package read and the case-move answer carry the placeholder until their owners confirm them (GAP-2973; ASM-4883, ASM-4888).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two lot operations on `/api/recovery/debtsale/v1`; the case-list read, the score read, the package read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` belong to later stories and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and its eligibility step on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.debtsale`, module `eligibility`; front end `src/modules/recovery/debtsale/LotBuilder.tsx`, the fragment SCR-25 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the lot row and its account rows commit together or not at all. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-25 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library) and DP-05 (the ACE read) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-2973; ASM-4883, ASM-4884, ASM-4885).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and a second story key Not specified in the source documents (CG-ALL-10325); the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the later stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` eligibility branch | Workflow | Waits for the cycle to open, reads the package in force and reports the outcome to the parent |
| `selectEligibleAccounts` | Activity | Reads the case list and the score, evaluates R-DS-01 to R-DS-03, writes the record and the rows, answers the moves |
| `EligibilityEvaluator` | Service | The rule evaluation over the package in force, with the deviation codes, the fraud flag, the cap value and the no-fire path |
| `DebtSaleDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `SaleLotWriter` | Repository | Inserts the lot and its account rows in one `rwb_debtsale` transaction with the idempotency row and the optimistic lock |
| `CaseListClient` | Client | The case-list read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `SourceDataScoreClient` | Client | The COLLINS score read of rwb-source-data with the as-of date and the stale path |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The case-move answer to rwb-case, one answer per case of the list |
| `DebtSaleLotController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `LotBuilder` | React component | Shows the population and the selection state on SCR-25, read only, with the refusal, stale-data, empty, loading, error and no-access states |

**Database and migrations.** No Flyway file. The two tables arrive with the DB story of this service, and the record and idempotency key are library objects created in `rwb_debtsale` by the library's migration (DP-03). No column is added for the score, the deviation flag, the case or the rule row: those are facts and rows of their owners and are referenced, not copied.

**Configuration and reference data.**

- `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants. `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-SEGMENT` are closed lists in Reference Data v5 Lists, so a new value needs a change to the enum of `rwb-debtsale.yaml` (CG-ALL-10326, CG-ALL-10327, CG-ALL-10328).
- The eligibility condition, the deviation codes X1 to X7, the fraud flag rule and the cap: rule rows of the package with their version, never written in code (ASM-4886, ASM-4887).
- The capability area "Debt sale" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the monthly cycle is the rule's timer and not a parameter of this build.
- Parameters and reference-data contract (DP-06, DP-07): the parameter keys this step reads and the reference-data contract that serves the lists above are Not specified in the source documents (DOR-RWB-S6-E5023-APP-20).

**Build steps**

1. The eligibility branch of `DebtSaleWorkflow` and its input record, registered on `rwb-debtsale` as the stage child of `CaseWorkflow`, with the cycle opening as its trigger.
2. `CaseListClient` and `SourceDataScoreClient` against their fakes, with the 2 s budget, the breaker, the as-of date, the stale path, the out-of-list path and the no-answer path (AC1, AC2, X3, X4, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `EligibilityEvaluator` over the package, with R-DS-01 to R-DS-03, the deviation codes, the fraud flag, the cap value and the no-fire path (AC1, AC2, X6).
5. `DebtSaleDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
6. `SaleLotWriter` with the one transaction, the lot row, the account rows, the idempotency row and the optimistic lock (AC1, X7).
7. `CaseMoveAnswer` with the three moves, one per case of the list (AC2, X3).
8. `DebtSaleLotController` with the rights, the `Idempotency-Key` and the problem mapping of the declared errors, and `LotBuilder` on SCR-25 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no write to any other service's tables (X8, BR3, BR5).

**Feature flag.** `rwb.debtsale.eligibility-v1`, a flag of the platform library; off means the step holds the cycle, writes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic case list in SIT, R-DS-01 selects the population, R-DS-02 excludes an account with its reason and R-DS-03 returns it, a repeated trigger writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-25 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | An account of the case list has an open deviation and is removed by R-DS-02 (X6) | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of the request or of the case list is absent or invalid (X5, X6) | Enter {field}. |
| MSG-P4-002 | A role without the Debt sale right calls the create or the read (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The COLLINS data product of the case list is stale after a late or failed ACE batch (X4, VR-S6-001-1) | {product} is from {date}. Today's load has not arrived. |

The five IDs are those of the legacy message set and of FSD S6 A2.1.3.1, and the text is the legacy and FSD wording for four of them and the Error and Message Standard v4 §4 wording for MSG-P1-001; no message is reworded and no new one is added. MSG-S6-001 is raised here on the R-DS-02 path, and MSG-P1-001 by the freshness check of the score product.

### 15. Screens and states

SCR-25 Lot builder, in its empty, loading, error and no access states and its selection state, is served through the gateway-bff composite route (DP-19); the empty, loading, error and no access states are Not specified in the source documents (CG-ALL-10337), as Screen Specifications v1 lists none of them. The route calls rwb-debtsale for the population, its accounts and its segment, rwb-case for the case and its route state and rwb-source-data for the score and its as-of date; this story fixes the rwb-debtsale answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The state this story produces is the selection state of SCR-25: the selected accounts of the cycle, the excluded accounts with their reason and the cut-off date, on a lot at `BUILDING`. The legacy screen table gives the states "Draft; priced; approved"; the priced state belongs to RWB-S6-E5024-APP and the approved state to RWB-S6-E6001-APP, and the selection state is this story's reading of "Draft". The refusal, not-recorded and stale-data states read the messages of section 14. PRT-05 Data room belongs to RWB-S6-E5026-APP and reads from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-023-01 | AC1 | Component | The 340-case list of the cycle with the COLLINS score on the fakes; the lot row, the account rows, the record and the answers asserted |
| TC-E5-023-02 | AC2 | Component | Case `RC-2026-000601` at `LOT_CANDIDATE_SELECTED`; the selection answered and the `LOT_BUILT` move asserted on the fake |
| TC-E5-023-03 | AC3 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E5-023-04 | Access | Component | A role without the Debt sale right; 403 with MSG-P4-002 and no read |
| TC-E5-023-05 | Principle 5 | Component | A forced decision record write failure inside the transaction; no lot row, no account row and no answer |
| TC-E5-023-06 | §12 operations, events and activities | Contract | The rwb-debtsale v1 operations API-S6-001 and API-S6-002 checked against the published contract; the responses and events of §12 asserted |
| TC-E5-023-07 | AC5, §12.7 tables (ASM-3438) | Component | A statement outside `rwb_debtsale`, a `v_ace_*` read or a write to a table not owned in §12.7; the grant refuses it and the build fails |
| TC-E5-023-08 | AC4 | Component | The lot selection screen opened by a role without the Debt sale right; the action is not offered and the request returns 403 with MSG-P4-002 |
| TC-E5-023-09 | AC6 | Component | Each of BR1 to BR10 checked against the package, the schema and the contract: owner, write path, reference-data read and the closed `LOV-LOT-STATUS` vocabulary asserted |
| TC-E5-023-10 | AC7 | Contract | A call to API-S6-001 and API-S6-002 without a valid token, without the right, and to a path that does not exist; 401, 403 and 404 with the platform error envelope and no read or write |
| TC-E5-023-11 | AC8 | Component | The same `Idempotency-Key` sent twice for one cycle and case-list version; one lot, one set of account rows, one record and one answer per case |
| TC-E5-023-12 | AC9 | Component | An activity that times out past 2 s and is retried on the workflow schedule; nothing written on the timed-out attempt and one set of rows after the retry |
| TC-E5-023-13 | AC10 | Component | A consumed call that fails or does not answer inside 2 s; the step holds, nothing is written, no move is answered and 503 with the platform error envelope is returned |
| TC-E5-023-14 | AC11 | Component | A requested status change that no row of section 8 allows; the change is refused, nothing is written and no move is answered |

The five legacy cases are those of RWB-E5-023 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 3 harness.

### 17. Guardrails

- No business value in code: the eligibility condition, the deviation codes X1 to X7, the fraud flag rule, the cap, the monthly cycle, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, amounts, dates, list values and a rule version only, `borrower_code` is a code, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR3).
- The case stays with rwb-case: no `recovery_case` row, no case route-state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_score` view read.
- The decision is recorded before the change; a build that writes the lot outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S6-001 | Accounts eligible for sale are selected by rule against the policy cap (FSD S6 Requirements served); the split plan carries no requirement id for this slice (GAP-2973) | FEAT-DBS-01 | Not specified in the source documents (DOR-RWB-S6-E5023-APP-2) | The eligibility step, the two table rows and the case move | TC-E5-023-01, TC-E5-023-02, TC-E5-023-05 |
| ADR-013 | 19 services inside ACE | FEAT-DBS-01 | Not specified in the source documents (DOR-RWB-S6-E5023-APP-2) | rwb-debtsale as the owner of the population | TC-E5-023-01 |
| ADR-014 | Schema and login per service | FEAT-DBS-01 | Not specified in the source documents (DOR-RWB-S6-E5023-APP-2) | `rwb_debtsale` and its own login | TC-E5-023-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | FEAT-DBS-01 | Not specified in the source documents (DOR-RWB-S6-E5023-APP-2) | The four consumed rows with their budget and breaker | TC-E5-023-01, TC-E5-023-02 |
| ADR-022 | Local decision record plus central ledger | FEAT-DBS-01 | Not specified in the source documents (DOR-RWB-S6-E5023-APP-2) | The record written before the change | TC-E5-023-03, TC-E5-023-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-023, disposition Split (rework); feature FEAT-DBS-01 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story; the 54 percent cap test is R-DS-19 and FEAT-DBS-16, owned by RWB-S6-E6005-APP |
| Source text | Legacy RWB-E5-023; FSD S6 Debt sale v3 A2.1 and TSD S6 Debt sale v2 T3, T4, T6 and T-A; Business Rules and Routing Logic v4 rows R-DS-01 to R-DS-03 and R-DS-19 |
| Test cases | TC-E5-023-01 to TC-E5-023-05 |
| Feature and screens | FEAT-DBS-01, SCR-25 Lot builder |
| Rules | R-DS-01, R-DS-02 and R-DS-03, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two operations, the elements, the fields DF-SAL-020 to DF-SAL-037, the four lists, the consumed rows, the error set and the fakes: RWB-S6-E5023-CON.
- The grouping and pricing, the reserve, the tiered terms, the buyer class, the per-account price and the minimum lot size test of R-DS-05: RWB-S6-E5024-APP.
- The masked data tape (RWB-S6-E5025-APP); the data room and the bids (RWB-S6-E5026-APP and the bidding stories); the buyer qualification (RWB-S6-E6002-APP).
- The committee approval and the tiered terms that become binding: RWB-S6-E6001-APP.
- The award, the 54 percent cap test of R-DS-19 and FEAT-DBS-16, `LotAwarded`, the settlement, `AccountsTransferred`, the derecognition and the posting: RWB-S6-E6005-APP, RWB-S6-E6007-APP, with the money in rwb-payment (P8).
- The eligibility inputs `deviation_open` and `fraud_flag` as fields: their owner and their contract row, which no source names (ASM-4887).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the COLLINS score and the ACE data products: rwb-source-data (P1); the DEBTSALE package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-25: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

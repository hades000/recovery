# RWB-S5-E3027-APP Recommend the disposal route

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3027-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-027 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3027-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-027 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag; the route recommendation is now one signal-driven step of `AssetDisposalWorkflow` on task queue `rwb-asset` that evaluates R-DIS-19 with the DISPOSAL package version in force, records the outcome through the local decision-record library before anything changes (DP-03), and answers the case moves of R-DIS-19, R-DIS-14 and R-DIS-08 to rwb-case. The legacy `v_ace_npa_asset` and `v_ace_score` reads are retired as service reads because rwb-asset holds no ACE view grant, so the ACE asset fact and the COLLINS economics arrive on the rwb-source-data data-product contracts (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). The pricing, listing and auction steps that consume the recommendation are RWB-S5-E3028-APP and the later stories of this service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E3027-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to propose auction, broker, RAMC, buy-back or rental with the expected return on each**, so that **assets sell sooner at approved prices, instead of the NPA sales cycle running to 1,486 days on listings and floors that are still checked by hand**.

This is the application slice of legacy RWB-E3-027. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19, "Temporal AssetDisposalWorkflow"; Temporal and Drools Design slide 13);
- the evaluation of R-DIS-19 on a held asset that is ready to sell, and of R-DIS-08 and R-DIS-14, which release a blocked or an evicted asset back to hold and to the disposal route, with the DISPOSAL package version in force;
- the local decision record of the recommendation, its ranked routes, its reasons and the expected return on each, written through RWB-PLT-E1027-CON before anything changes (DP-03);
- the answer to rwb-case for the case moves `ROUTE_RECOMMENDED` and `ASSET_HELD`, with the rule ID and the version that produced them;
- the two reads behind SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19), which expose the recommendation of the last step.

It does not own: the published shape of the recommendation element, the route vocabulary and the two reads, which are RWB-S5-E3027-CON; the opening price and the floor and the `listing` row, which are RWB-S5-E3028-APP; the auction rounds and the sale, which are the later stories of this service; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the ACE NPA asset and COLLINS score facts, which are rwb-source-data's (P1); the rule rows and the package sign-off, which are rwb-decision's (P7); and the deployment of this build, which is the wave 2 harness.

### 2. Business rationale

Legacy RWB-E3-027 asked one system step to propose auction, broker, RAMC, buy-back or rental with the expected return on each, and the FSD keeps the objective and the metric unchanged: the NPA sales cycle is measured on the decision log and the Workbench records, reviewed monthly, from 1,486 days to a target of 1,095 days (FSD S5 A2.10.1). The problem the feature answers is that listings and floor prices are checked by hand (FSD S5 A2.10.1), so the recommendation has to be a recorded, versioned decision that a person can approve, not a screen calculation.

What D-RCV-60 changes is where the recommendation lives and who owns each fact it needs:

- **the recommendation is the decision of this service.** R-DIS-19 ("Pricing agent recommends the disposal route with reasons and the COLLINS economics") moves a held asset from `ASSET_HELD` to `ROUTE_RECOMMENDED`, so the step, the record and the answer to the case belong to rwb-asset, which Architecture v5 slide 41 gives "assets taken on, holding, floor price, listings, auction rounds".
- **the case stays with rwb-case (P3).** `recovery_case` and the route states `EVICTION_REQUIRED`, `TITLE_BLOCKED`, `ASSET_HELD` and `ROUTE_RECOMMENDED` are P3's; this story evaluates the rule and **answers** the move. The legacy data table names `recovery_case`; the target never writes it (GAP-2872; ASM-4768).
- **the ACE facts stay with rwb-source-data (P1).** The legacy data table names `v_ace_npa_asset` and the FSD names `v_ace_score` for the COLLINS economics (FSD S5 A2.10.2). Only rwb-source-data reads the 30 `recovery.v_ace_*` views (Architecture v5 slides 29, 37 and 45), so DP-05 applies here as a **prohibition** and both facts arrive on the owner's data-product contracts (GAP-2872; ASM-4768).
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the recommendation, which is what legacy AC1 asks and what legacy AC4 tests.
- **the recommendation is not an event.** Architecture v5 slide 19 OUT gives rwb-asset `AssetTakenOn` and `AssetSold`; the recommendation surfaces as the case state and as the answer the parent applies, so the step publishes nothing and this story's Kafka surface is empty (GAP-2871; ASM-4766).

No business value moves with the split. The five route words, the expected return, the reasons, the two-working-day target of R-DIS-19 and the lists the step reads are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S5-E3027-CON is published: the recommendation element, its route vocabulary and its return unit, the additive property on the two reads, the consumed rows, the error set and the fakes are baselined and handed to this story.
- The rwb-source-data data-product contracts of DP06 Collateral and assets and of the COLLINS score fact (the `v_ace_score` row of the legacy data model) are published with their fakes, so the asset fact and the economics can be read on Day 1. Their operation names are Not specified in the source documents (GAP-2872; ASM-4768), and neither row is in this story's contract-dependency list, which is None.
- The case state, the case signal and the case-move answer of rwb-case are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies (GAP-2872; ASM-4768).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the recommendation and its record stand or fall together (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The DISPOSAL rule package is in force at its version with R-DIS-08, R-DIS-14 and R-DIS-19; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows and the reference data of the route words are governed there and are not listed for this story.
- `asset`, `listing` and `asset_sale` exist in schema `rwb_asset` from the DB story of this service, with the columns of TSD S5 T3.1 and the standard record columns of T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset`, `recovery.v_ace_score` or `rwb_case` is refused by the database and fails the boundary test (DP-05; GAP-2872; ASM-4768).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E3027-CON when its tests pass.

### 4. Flow

1. A held asset becomes ready to sell, or is released back to hold: the possession is taken after an eviction (R-DIS-14), the title is cleared after a block (R-DIS-08), or the appraisal is current and the title clear (R-DIS-19). Each fact reaches the case as a signal the parent `CaseWorkflow` forwards to the stage child on queue `rwb-asset`; nothing of it is read as a table here, and no inbound load, load run or data-quality exception exists in this module (GAP-2871; ASM-4766).
2. The step of `AssetDisposalWorkflow` receives the signal for a case in `EVICTION_REQUIRED`, `TITLE_BLOCKED` or `ASSET_HELD` and reads the case state, the appraisal currency and the title status the rule needs on the rwb-case contract, read only, one hop with a 2 s budget and a breaker (GAP-2872; ASM-4768).
3. The step reads the asset fact of the case — asset reference, asset type, book value, holding status — and the COLLINS economics on the rwb-source-data contracts: the DP06 Collateral and assets read and the score product read, one hop each, with the freshness stamp of each product (DP-05; GAP-2872).
4. `RouteRecommendationEvaluator` loads the DISPOSAL package version in force from rwb-decision and evaluates the three rules on the fact, in the order the machine of TSD S5 T4 gives them:
   - R-DIS-14 on `EVICTION_REQUIRED` and `POSSESSION_TAKEN` with `occupancy_status = vacant`;
   - R-DIS-08 on `TITLE_BLOCKED` and `TITLE_CLEARED` with `title_status = clear`;
   - R-DIS-19 on `ASSET_HELD` and `READY_TO_SELL` with `current_appraisal = Y and title_status = clear`.
5. For R-DIS-19 the evaluation ranks the five routes of the criterion — auction, broker, RAMC, buy-back and rental — with the expected return on each and the reasons, as the rule action and the package give them. For R-DIS-14 and R-DIS-08 the evaluation returns the release action and no ranking. Where no rule fires, the step changes nothing and reports the reason to the parent.
6. `AssetDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the asset reference, the rule ID with its version, the inputs reference, the recommended route, the ranked returns and reasons, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. `RouteRecommendationWriter` commits the recommendation in the same `rwb_asset` transaction as the record and the idempotency row. The recommendation is held in the decision record, not in a new column: no source gives a recommendation table or a return column, and `listing` is written only when the floor is set (GAP-2871; ASM-4767). `asset.holding_status` stays what it was — `HELD` — on all three rules.
8. `CaseMoveAnswer` answers rwb-case with the move `ROUTE_RECOMMENDED` under R-DIS-19, or `ASSET_HELD` under R-DIS-14 and R-DIS-08, with the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-2872; ASM-4768).
9. A repeated signal with the same case, asset reference and rule writes nothing, sends no second answer and counts the repeat.
10. `RouteRecommendationReader` serves the recommendation of the last step of the case to SCR-22 through the gateway-bff composite route, read only, next to the case and its route state of rwb-case (DP-19).
11. The pricing step of RWB-S5-E3028-APP reads the recommended channel of the same case from this service and writes the `listing` row; this story opens no listing and sets no price.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no recommendation is recorded and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E3-027-04, TC-E3-027-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E3-027-05 |
| X3 | The case is not in the state the rule expects | 409 and nothing is written; no rule is re-evaluated on a case that has already moved | None | AC2, AC3 |
| X4 | An ACE data product is stale after a late or failed batch | The step holds, writes nothing and reports the product date; it resumes on the next fresh answer | MSG-P1-001 | AC1, AC2, AC3 |
| X5 | The rwb-source-data, rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered | None | AC1, AC3 |
| X6 | The fact does not satisfy any of the three conditions | No rule fires: nothing changes, no record is written and the case keeps its state | None | AC1 |
| X7 | An appraisal older than the year rule, or a floor asked for before the recommendation exists | The step records nothing; the appraisal is ordered by the re-appraisal step and the floor by the pricing step of this service | MSG-S5-002, MSG-S5-001 | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 and X2 are the legacy paths of RWB-E3-027 carried onto the split, X3 to X7 are the paths the target call types add, and X8 is the DP-05 and DP-01 boundary. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature; their values belong to the pricing and re-appraisal steps, so no happy path of this story raises them.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3027-CON, the rwb-source-data, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity names, the decision code per rule and the shape of the ranked returns are this story's choice; the rules, the messages, the screens, the two reads and the route words are fixed |
| Valuable | A held asset gets a recorded, versioned route recommendation with its economics on the day it is ready to sell, and the case moves in the service that owns it |
| Estimable | One workflow step, one evaluator, one record write, one read surface, two clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and ACE facts through the contract fakes, plus the access case and the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Recommend the disposal route

  Background:
    Given case "RC-2026-000511" holds asset "AST-2026-000511" at holding status "HELD"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-08, R-DIS-14 and R-DIS-19
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Recommend the disposal route (legacy RWB-E3-027 AC1)
    Given the rwb-source-data contract mock returns the asset fact and the COLLINS economics of asset "AST-2026-000511"
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for "RC-2026-000511" with a current appraisal and the title cleared
    Given the rwb-decision rule-package fake returns the DISPOSAL package at its version in force
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then proposes auction, broker, RAMC, buy-back or rental with the expected return on each
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-14 (legacy RWB-E3-027 AC2)
    Given the rwb-case contract mock returns the signal POSSESSION_TAKEN for a case in "EVICTION_REQUIRED" with the occupancy vacant
    Given a case in state EVICTION_REQUIRED
    When possession taken
    Then return the asset to hold and resume the disposal route
    Then the case moves to ASSET_HELD

  Scenario: AC3 Rule R-DIS-08 (legacy RWB-E3-027 AC3)
    Given the rwb-case contract mock returns the signal TITLE_CLEARED for a case in "TITLE_BLOCKED" with the title clear
    Given a case in state TITLE_BLOCKED
    When title cleared
    Then release the asset to hold and to the disposal route
    Then the case moves to ASSET_HELD

  Scenario: AC4 Not recorded (legacy RWB-E3-027 AC4)
    Given the local decision-record library stub is stopped
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-14 | Asset disposal | D8.1 to D8.3 | EVICTION_REQUIRED | POSSESSION_TAKEN | occupancy_status = vacant | Return the asset to hold and resume the disposal route | ASSET_HELD | Sale officer | Workbench, LIT | None |
| R-DIS-08 | Asset disposal | D8.1 to D8.3 | TITLE_BLOCKED | TITLE_CLEARED | title_status = clear | Release the asset to hold and to the disposal route | ASSET_HELD | Sale officer | CCMS, the Land Office, SCIS | None |
| R-DIS-19 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | READY_TO_SELL | current_appraisal = Y and title_status = clear | Pricing agent recommends the disposal route with reasons and the COLLINS economics | ROUTE_RECOMMENDED | Sale officer | Agent Runtime, COLLINS | 2 working days |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case moves are written by rwb-case on this story's answer, and the recommendation is recorded here. The Systems column names the agent runtime and COLLINS of the legacy design; in the target the economics arrive on the rwb-source-data contract and the agent path is recorded as a gap, because this key's pattern set and contract row carry neither (GAP-2872; ASM-4768).

| ID | Rule | Source |
|---|---|---|
| BR1 | The recommendation is this service's: it is evaluated here and recorded here, and no other service computes or stores it | Architecture v5 slide 41; TSD S5 T2; R-DIS-19 |
| BR2 | The decision is recorded before anything changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2 ("writes the decision log entry before any change"); legacy RWB-E3-027 AC1 and AC4 |
| BR3 | The ACE asset and COLLINS score facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes both facts on the owner's contracts only | DP-05; Architecture v5 slides 29, 37 and 45; FSD S5 A2.10.2; GAP-2872 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-2872 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and the case reference are identifiers of another service's fact | DP-01; TSD S5 T3.3 |
| BR6 | Every value a business person may change is reference data or a rule row read with its version: the five route words, `LOV-SALE-CHANNEL`, `LOV-HOLDING`, `LOV-ASSET-TYPE`, the return rule and the two-working-day target | TSD S5 T3.2; FSD S5 BR-S5-010; legacy Guardrails; GAP-2871 |
| BR7 | The recommendation adds no column and no table: the record holds the route, the ranked returns and the reasons, and the `listing` row is written only by the pricing step | GAP-2871; ASM-4767 |
| BR8 | The same signal twice, or the same `Idempotency-Key` twice, writes once and answers the case move once | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR9 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |
| BR10 | The expected return is compared and shown with its currency; where a source product is stale, no recommendation is recorded | VR-S5-010-1; FSD S5 A2.10.3.1; GAP-2871 |

### 9. State transitions

The case route state is rwb-case's and is not written here: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4).

| From (case route state, rwb-case) | Event | Condition | To | This service's effect |
|---|---|---|---|---|
| `EVICTION_REQUIRED` | `POSSESSION_TAKEN` | occupancy_status = vacant | `ASSET_HELD` | Record R-DIS-14; holding status unchanged |
| `TITLE_BLOCKED` | `TITLE_CLEARED` | title_status = clear | `ASSET_HELD` | Record R-DIS-08; holding status unchanged |
| `ASSET_HELD` | `READY_TO_SELL` | current_appraisal = Y and title_status = clear | `ROUTE_RECOMMENDED` | Record R-DIS-19 with the ranked routes and their returns |
| Any of the three | A fact that satisfies no condition | X6 | Unchanged | No record, no answer |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A signal arrives for a case in one of the three states | The package in force is loaded | Evaluating |
| Evaluating | A rule fires | The fact is fresh and the case is in the state the rule expects | Recording |
| Recording | The decision record is written | The write succeeds | Answering |
| Answering | The case-move answer is sent | The record is committed | Waiting for the next signal |
| Recording | The record write fails | X1 | Waiting, nothing changed |
| Waiting | A data product is stale or a contract does not answer | X4, X5 | Held, until a fresh answer |

The route states are those of the DISPOSAL machine of TSD S5 T4 and of the legacy criteria; they live on the case of record. `holding_status` stays in `HELD` of `LOV-HOLDING` through all three rules, because the sale is opened by the pricing step and the listing, not here. The step states are the target design of this story and are not named by any source.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1: the primary role of the feature after the step has run, reading the recommendation and its returns on SCR-22 |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the recommendation and corrects the asset facts the rule reads |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the release of an evicted asset and the recommendation that follows |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE, PT-VALUER, PT-AUCTION, PT-RAMC | Asset and disposal R or RU as TSD S5 T6.1 gives it: read the asset and its recommendation in scope, and the partner sees its own assets through the partner gateway |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA: read, and approve the route on the approval path where the delegation of authority requires it (R-DIS-20, the next story) |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-asset service identity | Runs the step, evaluates the rules, writes the decision record, answers the case move and serves the two reads; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S5 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the sale officer as also-user (FSD S5 A2.10.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the sale officer is the reader of the outcome and the actor of the approval path. DP-08 is not in this key's pattern set, so the capability area and the right are declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 | asset (S5, `rwb_asset`) | id | Read, the asset reference the record and the answer carry |
| DF-COL-029 | asset (S5, `rwb_asset`) | case_id | Read, the case reference |
| DF-COL-031 | asset (S5, `rwb_asset`) | asset_ref | Read, the asset reference of the recommendation |
| DF-COL-033 | asset (S5, `rwb_asset`) | asset_type | Read, against `LOV-ASSET-TYPE`, the class the economics are compared on |
| DF-COL-037 | asset (S5, `rwb_asset`) | book_value | Read, the opening book value the return is shown against |
| DF-COL-041 | asset (S5, `rwb_asset`) | holding_status | Read, `HELD` of `LOV-HOLDING`; not changed by this step |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Not written here: the pricing step of RWB-S5-E3028-APP writes them from the recommended channel |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before anything changes; the recommended route, the ranked returns and the reasons are the outcome |
| Standard columns | decision_record (PLT library) | `state`, `version`, `created_at`, `created_by` | Write, with the hash link of the chain |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and the location facts | Not read: this service holds no `v_ace_*` grant; the fact arrives on the DP06 contract (BR3) |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Not read: the COLLINS economics arrive on the rwb-source-data score contract (BR3) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the state arrives on the rwb-case read and the move on its answer |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the package version in force arrives from rwb-decision |

Field IDs are those of the TSD S5 Assets and auction v2 T3.1, the Logical Data Model and Data Dictionary v9 and the legacy data table of RWB-E3-027. **No new table, no new column and no migration**: the recommendation is the decision record, `listing` and `asset_sale` are written by the later stories, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_asset` by the library's own migration (DP-03). The `asset` row is not in the Ownership Map table list, which gives S5 `asset_sale` and `listing` only; its owner is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2872; ASM-4768).

**No personal data.** The record, the answer and the reads carry identifiers, codes, amounts with their currency, dates and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, a workflow input or an event, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes are declared by RWB-S5-E3019-CON and extended additively by RWB-S5-E3027-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding status and its `route_recommendation` element (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors are 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter, and 503 when the decision library or a consumed contract does not answer. No operation is added for the recommendation: it runs unattended and has no caller (FSD S5 A2.10.3.3, "None; runs unattended"); its shape is the element RWB-S5-E3027-CON fixes (GAP-2871; ASM-4767). `POST /assets/{assetId}/listings` (API-S5-004) and `POST /listings/{listingId}/rounds` (API-S5-005) belong to the pricing and auction stories of this service; `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's.

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE asset fact of the case: asset reference, asset type, book value, holding status, transfer-in type and the location fact, with the freshness stamp; faked |
| The read of the COLLINS score product (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The economics the recommendation is priced on: score key, model code, model version, score value and estimate value, with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the appraisal currency and the title status; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | rwb-case (P3) | P3 rwb-case | The answer that carries `ROUTE_RECOMMENDED` or `ASSET_HELD` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | rwb-decision (P7) | P7 rwb-decision | The DISPOSAL package at the version in force with R-DIS-08, R-DIS-14 and R-DIS-19; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). None of the five rows is in this story's contract-dependency list, which is None, although all five are class C in fact; the absence is recorded as GAP-2872 with ASM-4768 and the build uses the fakes on Day 1.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset `AssetTakenOn` and `AssetSold`, and the Ownership Map gives the service event EV-22: neither is the recommendation, which surfaces as the case state on the rwb-case answer. This story therefore writes no outbox row, and a build that adds an event for the recommendation fails the absence test.

#### 12.4 Events consumed

None. Architecture v5 slide 13 puts an E in the row of S5 under S4, but no source names a litigation event, so this story declares no consumer group, no subscription and no inbox row; the possession and title facts arrive as signals the parent `CaseWorkflow` forwards, and the absence of a named event is recorded (GAP-2871; ASM-4766). A build that adds a subscription fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the holding | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the asset reference, the stage state and the rule package in force; signals: the case signal the parent forwards, the package in force and the approval answer |
| `recommendDisposalRoute` | Activity, the step of R-DIS-19 | `rwb-asset` | The case, the asset and the economics in; the ranked routes with their returns, the reasons, the rule ID with its version and the case move out |
| `releaseAssetToHold` | Activity, the step of R-DIS-14 and R-DIS-08 | `rwb-asset` | The case, the asset and the release fact in; the release action, the rule ID with its version and the `ASSET_HELD` move out |
| `recordRouteRecommendation` | Activity, the platform `RecordAndApply` of the kit | `rwb-asset` | The decision record, the idempotency row and the case-move answer written in one transaction |

The two step activities are the L4 contract of this service on queue `rwb-asset`; the rule evaluation itself is the kit's `EvaluateRules` activity, which runs the embedded Drools package of the owning service (Temporal and Drools Design slides 12 and 13; ADR-017). The activity names are a target design choice of this story and are fixed by no source document.

#### 12.6 Schedules

None. The step is signal-driven and owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP; the two-working-day target of R-DIS-19 is the rule's own timer inside the workflow, not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT library, created in `rwb_asset` | The route recommendation, its ranked returns, its reasons and the rule version (DP-03); the row this step writes |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal and the answer it holds |
| asset | S5 (`rwb_asset`) | Read only here: the asset reference, the type, the book value and the holding status; written by the take-on and holding stories |
| listing | S5 (`rwb_asset`) | Not written here: the pricing step of RWB-S5-E3028-APP writes it from the recommended channel |
| asset_sale | S5 (`rwb_asset`) | Not written here: the sale and auction stories |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `collateral`, `v_ace_npa_asset` and `v_ace_score` (P1), `decision_log_entry` and `rule_row` (P7). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data asset fake | The asset fact of `AST-2026-000511` for case `RC-2026-000511` at `HELD` with book value and asset type; the same asset with the title still blocked; a stale product with its date; no answer beyond 2 s | AC1, AC2, AC3, X4, X5 |
| rwb-source-data score fake | The COLLINS economics of the case with its model version and estimate; a stale score product; no answer beyond 2 s | AC1, X4 |
| rwb-case case-state fake | The case at `ASSET_HELD` with a current appraisal and the title clear, at `EVICTION_REQUIRED` with the occupancy vacant, at `TITLE_BLOCKED` with the title clear, and a case in none of the three | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The moves `ROUTE_RECOMMENDED` and `ASSET_HELD` accepted; a move refused because the case is not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-08, R-DIS-14 and R-DIS-19; a package version one step behind | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000511`, with the recommendation read once from this service | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-source-data reads, the case-move answer and the rule-package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2872; ASM-4768).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The two asset reads on `/api/recovery/asset/v1`; the two rwb-source-data product reads, the rwb-case state read, the case-move answer and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The recommendation is not an event; the service's events belong to the take-on and sale stories |
| Temporal | 1 workflow, 3 activities | `AssetDisposalWorkflow` with `recommendDisposalRoute`, `releaseAssetToHold` and `recordRouteRecommendation` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `route`, Java package `th.co.scb.ace.workbench.recovery.asset.route`; front end `src/modules/recovery/asset/AssetRouteRecommendation.tsx`, the fragment SCR-22 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant and reads no ACE view and no ACE table, so the asset fact and the COLLINS economics are the ones the rwb-source-data contracts answer (Architecture v5 slides 29 and 41; GAP-2872; ASM-4768). DP-03 is the transaction rule of the step: the record, the idempotency row and the answer commit together or not at all. DP-13 moves the base of the two reads and nothing else. DP-19 is how SCR-21 and SCR-22 reach the recommendation, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The five consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2872 with ASM-4768. The agent path R-DIS-19 names (Agent Runtime, and DP-20 in the DP table) is not added: the recommendation is the rule outcome and the economics arrive from rwb-source-data, and step D1 decides whether a P10 row is raised (GAP-2872; ASM-4768).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` route branch | Workflow | The stage step that waits for the release or ready-to-sell signal, loads the package in force and reports the outcome to the parent |
| `recommendDisposalRoute` | Activity | The R-DIS-19 step: read the fact, the case and the economics, evaluate the rule, return the ranked routes with their returns and reasons |
| `releaseAssetToHold` | Activity | The R-DIS-14 and R-DIS-08 step: evaluate the release and return the `ASSET_HELD` move |
| `RouteRecommendationEvaluator` | Service | The evaluation of the three rules against the DISPOSAL package in force, with the route words of reference data and the return comparison |
| `AssetDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteRecommendationWriter` | Repository | Commits the record, the recommendation outcome and the idempotency row in one `rwb_asset` transaction; writes no asset column and no listing row |
| `RouteRecommendationReader` | Repository | Reads the last recommendation of a case for the two reads, with its rule version |
| `SourceDataProductClient` | Client | The DP06 asset read and the score read of `RWB-P1`, one hop each, 2 s, breaker, no retry of its own |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `RulePackageClient` | Client | The DISPOSAL package read of rwb-decision at the version in force, one hop, 2 s |
| `AssetController` | Controller | The two reads with the `route_recommendation` element, the capability area and right, the pagination and the problem mapping |
| `AssetRouteRecommendation` | React component | Shows the recommended route, the ranked returns and the reasons on SCR-22, read only, with the refusal, not-recorded and stale-data states |

**Database and migrations.** No Flyway file. `asset`, `listing` and `asset_sale` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No column is added for the route, the return or the reasons: they are facts of the decision record, and a build that adds a column fails the review (BR7).

**Configuration and reference data.**

- The five route words and their mapping to `LOV-SALE-CHANNEL` (`DUTCH_AUCTION`, `BROKER`, `DIRECT`, `LED_AUCTION`, `RAMC`), `LOV-HOLDING`, `LOV-ASSET-TYPE` and the currency of the asset book value, each at its version in force (TSD S5 T3.2), read as reference data and never as constants (GAP-2871; ASM-4767).
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the two-working-day target, the return rule and the reasons are values of the package, not of this build.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget and the single hop are the platform rule of ADR-020; no parameter of the step is named by any source.

**Build steps**

1. The route branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`, with the three signals as its triggers.
2. `SourceDataProductClient`, `CaseStateClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the stale-product path and the no-answer path (AC1, X4, X5).
3. `RouteRecommendationEvaluator` over the DISPOSAL package, with R-DIS-08, R-DIS-14 and R-DIS-19, the route words and the no-fire path (AC1, AC2, AC3, X6).
4. `AssetDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `RouteRecommendationWriter` with the one transaction, the idempotency row and the optimistic lock (AC1, X7).
6. `CaseMoveAnswer` and the parent signal, with the three moves (AC1, AC2, AC3).
7. `RouteRecommendationReader` and `AssetController` with the rights, the pagination and the problem mapping (AC1).
8. `AssetRouteRecommendation` and the two screens through the composite route fake (AC1, AC2, AC3).
9. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_case` or `rwb_decision` (X8, BR3, BR5).

**Feature flag.** `rwb.asset.route-recommendation-v1`, read as a flag of the platform library; off means the step holds the signal, writes nothing and answers no move, and the pricing and auction stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic signal in SIT, each of the three rules produces its record and its move, the five routes are ranked with their returns, a repeated signal writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-22 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's values, so no path of this story raises it (X7) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so this story raises it only on a stale recommendation request (X7) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or of the fact is absent or invalid (X3, X6) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset list or the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the recommendation (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | An ACE data product of the case is stale after a late or failed batch (X4, VR-S5-010-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are those of the legacy message set and of FSD S5 A2.10.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. VR-S5-010-1 is declared with its message and its check stays with rwb-source-data, which owns the batch status.

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its recommendation, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact and rwb-valuation for the valuation references; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces on SCR-22 are the held state with the recommendation and the ranked returns, and the failure states it shows: refused with MSG-P4-002, not recorded with MSG-P7-003, stale data with MSG-P1-001. The take-on, listed and sold states of the same screen belong to the take-on, pricing and sale stories of this service and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-027-01 | AC1 | Component | The asset fact and the COLLINS economics of `AST-2026-000511`; the record, the five ranked routes with their returns and the `ROUTE_RECOMMENDED` move asserted on the fakes |
| TC-E3-027-02 | AC2 | Component | Case `RC-2026-000511` at `EVICTION_REQUIRED` with the occupancy vacant; the R-DIS-14 record, the release and the `ASSET_HELD` move |
| TC-E3-027-03 | AC3 | Component | Case `RC-2026-000511` at `TITLE_BLOCKED` with the title clear; the R-DIS-08 record, the release and the `ASSET_HELD` move |
| TC-E3-027-04 | AC4 | Component | The decision-record stub stopped; nothing recorded, no move answered and MSG-P7-003 shown |
| TC-E3-027-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E3-027-06 | Principle 5 | Component | A forced decision log write failure at the moment of the recommendation; no record, no move and no change |

The six legacy cases are the legacy cases of RWB-E3-027 in their legacy order, with the Level column added: legacy level `System` maps to `Component` because the step is tested on its fakes, and the access and forced-failure cases map to `Component` for the same reason. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the wave 2 harness carries the `-ITG` copies (`TC-E3-027-01-ITG` to `TC-E3-027-06-ITG`) where a real P1, P3 or P7 is called.

### 17. Guardrails

- No business value in code: the five route words, the return rule, the two-working-day target, the lists and the rule rows stay reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in a workflow input or in a log: identifiers, codes, amounts with their currency, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, and no event invented for the recommendation.
- The decision is recorded before the change and the recommendation adds no column and no table; a build that adds either fails the review (DP-03, BR7).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| FEAT-AST-10 | Recommend the disposal route: proposes auction, broker, RAMC, buy-back or rental with the expected return on each, runs unattended (Epics 3 to 8 Specification v3; FSD S5 A2.10) | The three rules, the ranked returns, the record and the two moves | TC-E3-027-01, TC-E3-027-02, TC-E3-027-03 |
| REQ-S5-004 | A start price and a floor price are proposed for every asset, and the floor is approved by the named role (the pricing step that consumes this recommendation; the story master carries no requirement id for this key, GAP-2873; ASM-4769) | The recommended route and its return, consumed by RWB-S5-E3028-APP | TC-E3-027-01 |
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval (the routes this recommendation ranks, approved in the next story) | The ranked RAMC, buy-back and rental routes with their returns | TC-E3-027-01 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the recommendation | TC-E3-027-01 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The package version in force evaluated in the step activity | TC-E3-027-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget | TC-E3-027-02 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the recommendation | TC-E3-027-04, TC-E3-027-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-027, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E3-027-01 to TC-E3-027-06 |
| Feature and screens | FEAT-AST-10, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-08, R-DIS-14 and R-DIS-19, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the recommendation element, its route vocabulary, its return unit, the additive property on the two reads, the consumed rows, the error set and the fakes: RWB-S5-E3027-CON.
- The approval of the recommendation by the delegation of authority and the route submission: R-DIS-20 and R-DIS-27, the next story of this service.
- The opening price, the floor and the `listing` row: RWB-S5-E3028-APP, which reads the recommended channel from this service.
- The auction rounds, the sealed bids and the sale: the auction stories of this service, with the proceeds in rwb-payment (P8).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (GAP-2872).
- The ACE NPA asset, collateral and COLLINS score facts and the freshness of each data product: rwb-source-data (P1) (GAP-2872; ASM-4768).
- The agent-assisted pricing advice named in R-DIS-19: rwb-agent (P10) and DP-20, which this key's pattern set does not carry (GAP-2872; ASM-4768).

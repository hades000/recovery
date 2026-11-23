# RWB-S5-E4026-APP Re-list on no bid

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-R |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4026-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-026 for rwb-asset. The four legacy criteria are kept word for word with their origin tag and the six legacy test cases keep their IDs. The re-list becomes the no-bid branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: it evaluates R-DIS-38 and R-DIS-29 on the DISPOSAL package in force, writes the next round and its price on `listing` in `rwb_asset`, fixes the floor as the reserve and the step schedule by asset class, records each outcome before the row changes (DP-03), answers `ROUND_OPEN` and `FLOOR_APPROVED` to rwb-case and publishes nothing. The `v_ace_*` reads arrive on the rwb-source-data contract (DP-05), the base becomes `/api/recovery/asset/v1` (DP-13), and the screens read through the gateway-bff route (DP-19). Gaps: R-DIS-38 shared with the ladder story (GAP-2918; ASM-4816); R-DIS-29 shared with the pricing story (GAP-2919; ASM-4817); no re-list count or limit (GAP-2920; ASM-4818); consumed operation names (GAP-2921; ASM-4819); no declared portal re-publication (GAP-2922; ASM-4820); REQ-S5-006 mapped to another feature (GAP-2923; ASM-4821); DP-04 outside the pattern set (GAP-2924; ASM-4796). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **the Workbench to put the asset back on the schedule at the next price step when a round closes with no bid**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E4-026. It owns the four legacy criteria with their origin tag; the no-bid re-list edge of `AssetDisposalWorkflow` on `rwb-asset` as a child of the case workflow (Architecture v5 slide 13); R-DIS-38 on a round closed with no bid and R-DIS-29 on the officer's floor approval, on the package in force; the next round number and its price and the reserve and step schedule on `listing` in `rwb_asset`; the decision record before each change (DP-03) and the answers `ROUND_OPEN` and `FLOOR_APPROVED`; and the reads of SCR-23 and SCR-21 on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the shapes, the consumed rows and the fakes, which are RWB-S5-E4026-CON; the ladder step of FEAT-AST-13 (RWB-S5-E4022); the setting of the start price and the head of NPA's approval of the floor (FEAT-AST-11); the publication of the listing to HOME.SCB and the portals (FEAT-AST-12, INT-27); the rounds, the bids and the award (RWB-E4-024, API-S5-005); the re-appraisal cycle and R-DIS-44 (FEAT-AST-09, JOB-19); the case and its states (rwb-case, P3); the ACE facts (rwb-source-data, P1); the rule package (rwb-decision, P7); and the deployment (the operations story of this key).

### 2. Business rationale

Legacy RWB-E4-026 closed a gap in the ladder: when a round ended with no bid the asset stayed listed at a price nobody bid for, and the sale officer re-listed it by hand on the next rung. The FSD keeps the behaviour as FEAT-AST-17 in module S5, running unattended, with the NPA sales cycle as the measure it serves (FSD S5 A2.17; REQ-S5-006).

What D-RCV-60 changes:

- **the schedule is this service's.** `listing` is S5's in `rwb_asset` (Ownership Map; Architecture v5 slide 41); the ladder, its step and the asset class schedule are reference data with a version, never a constant.
- **the value stays with rwb-source-data (P1).** Only that service reads the `recovery.v_ace_*` views (Architecture v5 slide 8), so DP-05 is a **prohibition** and the asset class, title status and appraised value arrive on the owner's product with a freshness stamp.
- **the case stays with rwb-case (P3).** The rule decides and this story **answers** the move; it writes no case row.
- **the decision is recorded first**, one per outcome, in the row's transaction — what AC1 asked and AC4 tested.
- **the public surface does not grow.** EV-22 `AssetTakenOn` is the take-on story's (TSD S5 T5.3) and the re-published round reaches the portals through FEAT-AST-12, which no operation covers today (GAP-2922).

### 3. Preconditions

- RWB-S5-E4026-CON tagged: reads, listings write, consumed rows, record and package elements, error set, fakes.
- `listing` and `asset` exist in `rwb_asset` with the TSD S5 T3.1 and T3.0 columns; no column holds the re-list count or the limit, which stay placeholders (GAP-2920; ASM-4818).
- The DISPOSAL package is in force with R-DIS-38 and R-DIS-29 from rwb-decision (P7), loaded through the service template; DP-04 is outside the pattern set (GAP-2924; ASM-4796).
- The ladder, its step and unit, the asset-class step schedule and the `LOV-*` lists are reference data with a version (TSD S5 T3.2).
- The rwb-case state read and the case-move answers sit behind fakes; the answers' names are not published (GAP-2921; ASM-4819).
- The rwb-source-data product with the asset class, title status, appraised value and book value is published with a fake and a freshness stamp; its name is not published (GAP-2921).
- The round-close fact and the floor approval arrive as workflow signals from the rounds story and the approval step; no subscription is added.
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass.

### 4. Flow

1. A round of a live listing closes with no bid; the rounds step signals `AssetDisposalWorkflow` with case, asset, listing and round.
2. The workflow confirms the case state on the rwb-case contract: `ROUND_OPEN`.
3. It reads the listing: start price, floor, round number, sale channel, status, and the re-list count where a column is named (GAP-2920).
4. It reads the asset and valuation facts on the rwb-source-data product, one hop, 2 s: asset class, title status, appraised value, book value.
5. `RelistEvaluator` loads the package in force and evaluates R-DIS-38: from `ROUND_OPEN`, on `ROUND_CLOSED_NO_BID`, with `bid_count = 0` and the round price above the floor, the price steps down and the next round opens, the case staying in `ROUND_OPEN` (Business Rules and Routing Logic v4).
6. `AssetDecisionRecordWriter` writes one record **before any change**; a failed write stops the step (DP-03; AC1, AC4).
7. `ListingWriter` writes the next round number, its price, the status and the listed-at time in one transaction with the record and the idempotency row; where no column holds the round price the value is Not specified in the source documents (GAP-2920).
8. `CaseMoveAnswer` answers `ROUND_OPEN` with the round number, the new price, the rule and its version; rwb-case writes the case.
9. Where the round price is already at the floor, R-DIS-38 does not fire: nothing is written and the floor case is reported to the parent, which is the re-list-limit and re-appraisal path of FEAT-AST-09 (R-DIS-44).
10. On the officer's floor approval R-DIS-29 applies in `FloorReserveEvaluator`: from `PRICE_PROPOSED`, on `FLOOR_APPROVED_BY_OFFICER` with `officer_approved = Y`, the floor is fixed as the reserve, the step schedule is set by asset class, and the case moves to `FLOOR_APPROVED`.
11. A second record is written before the reserve and the schedule commit; no event and no outbox row leaves the service (§12.3).
12. A repeated signal or `Idempotency-Key` writes once and is counted; the step returns to its durable timer and the workflow continues as new at each stage end and at least every 28 days.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered | MSG-P7-003 | AC4, TC-E4-026-04, -06 |
| X2 | The role lacks the right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-026-05 |
| X3 | The case is in another state | The rule does not fire; nothing written, the state reported | None | AC2, AC3 |
| X4 | The round price is at the floor | No step, no record, no move; the floor case reported to the parent | MSG-S5-001 where under the limit | AC2 |
| X5 | A contract misses 2 s or its breaker is open | Retry on the workflow schedule; 503 | None | AC1, AC3 |
| X6 | The ACE product is stale | Held, nothing written, the data date shown | MSG-P1-001 | AC3 |
| X7 | The appraisal is more than a year old | The floor is not fixed; a new appraisal is asked for | MSG-S5-002 | AC3 |
| X8 | The same signal arrives twice | One step, one answer, no second record | None | AC1, AC2 |
| X9 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | §17, BR6 |

X1 to X3 are the legacy paths on the split, X4 to X8 what the floor, the call types and the appraisal age add, and X9 the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the fakes; no live P1, P3 or P7 |
| Negotiable | Activity names, decision code and outcome shape are ours; rules, messages, screens, row and reads are fixed |
| Valuable | A no-bid round returns to the schedule at the approved next price without a manual re-list |
| Estimable | One workflow edge, two evaluators, one record, one row change, two answers, two clients |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, floor and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Re-list on no bid

  Background:
    Given case "RC-2026-000526" holds asset "AST-2026-000526" in listing "LS-2026-000526"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-38 and R-DIS-29
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Re-list on no bid (legacy RWB-E4-026 AC1)
    Given the rwb-source-data contract mock returns the NPA asset "AST-2026-000526" of case "RC-2026-000526" with its asset class and appraised value
    Given the rwb-case contract mock returns the case state ROUND_OPEN for "RC-2026-000526"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then puts the asset back on the schedule at the next price step when a round closes with no bid
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-38 (legacy RWB-E4-026 AC2)
    Given the rwb-case contract mock returns the case state ROUND_OPEN for "RC-2026-000527"
    Given a case in state ROUND_OPEN
    When round closed no bid
    Then step the price down on the published schedule and open the next round
    Then the case moves to ROUND_OPEN

  Scenario: AC3 Rule R-DIS-29 (legacy RWB-E4-026 AC3)
    Given the rwb-case contract mock returns the case state PRICE_PROPOSED for "RC-2026-000528"
    Given a case in state PRICE_PROPOSED
    When floor approved by officer
    Then fix the floor as the reserve and set the step schedule by asset class
    Then the case moves to FLOOR_APPROVED

  Scenario: AC4 Not recorded (legacy RWB-E4-026 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria word for word with the origin tag added: the repeated `Then`, `the action is taken`, `its trigger arrives` and `the decision log cannot be written` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-source-data answers the facts, rwb-case writes the moves, and this story evaluates, writes, records and answers. AC2 states the same rule row that RWB-S5-E4022 carries for the ladder step; this story owns the no-bid outcome and that story the step itself, and the duplicate is GAP-2918. AC3 is also the pricing story's path (FEAT-AST-11) and is kept here because the legacy story owns it; GAP-2919 records the split.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-38 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | ROUND_CLOSED_NO_BID | bid_count = 0 and price_at_round above floor_price | Step the price down on the published schedule and open the next round | ROUND_OPEN | Workbench | Rules component, Workbench scheduler | per schedule |
| R-DIS-29 | Asset disposal | D8.1 to D8.3 | PRICE_PROPOSED | FLOOR_APPROVED_BY_OFFICER | officer_approved = Y | Fix the floor as the reserve and set the step schedule by asset class | FLOOR_APPROVED | Workbench | Rules component | None |

Both rows are copied character for character from the Business Rules and Routing Logic v4; their owner column is a business role, so rwb-case holds the states on this story's answers while the `listing` row is written here. FSD S5 A2.17 also lists R-DIS-30 (vendor allocation, moving to `VENDOR_ALLOCATED`); it belongs to the vendor story and is not evaluated here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The schedule is this service's: start price, floor, round number, status and listed-at are `listing` elements in `rwb_asset` | Ownership Map; Architecture v5 slide 41; TSD S5 T3.1 |
| BR2 | The record precedes the change, one per outcome, with the rule and package version | DP-03; AC1, AC4 |
| BR3 | The ladder, the asset-class step schedule, the floor rule and the appraisal test are reference data or rule rows with a version | TSD S5 T3.2; legacy Guardrails |
| BR4 | The case state is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2921 |
| BR5 | The re-list count and the re-list limit are held only where a column or a reference row is named | TSD S5 T3.1; GAP-2920 |
| BR6 | The asset and valuation facts stay with rwb-source-data; no `v_ace_*` read here | DP-05; Architecture v5 slide 8 |
| BR7 | No event is published; EV-22 `AssetTakenOn` is the take-on story's and the sale event the sale story's | TSD S5 T5.3 |
| BR8 | A repeated signal or key writes once, answers once and is counted | TSD S5 T-A.2 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset` | DP-01; TSD S5 T3.3 |
| BR10 | No personal data in the schema, a record, a log or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answers (BR4).

| From (`listing` status) | Event | Condition | To |
|---|---|---|---|
| Live, round closed with no bid | `ROUND_CLOSED_NO_BID` under R-DIS-38 | Bid count 0 and round price above the floor | Live at the stepped price with the next round open; answer `ROUND_OPEN` |
| Live, round closed with no bid | `ROUND_CLOSED_NO_BID` under R-DIS-38 | Round price at the floor | Unchanged, the floor case reported (X4) |
| Draft, floor approved by the officer | `FLOOR_APPROVED_BY_OFFICER` under R-DIS-29 | `officer_approved = Y` and the appraisal inside a year | Floor fixed as the reserve, the step schedule set; answer `FLOOR_APPROVED` |
| Draft, floor approved by the officer | `FLOOR_APPROVED_BY_OFFICER` under R-DIS-29 | Appraisal more than a year old | Unchanged, the approval held (X7) |
| Any | The same signal again, or an unexpected state | X8, X3 | Unchanged |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting on the timer | A round-close or floor-approval signal | The package in force is loaded | Evaluating |
| Evaluating | A rule fires | The record is written | Applying |
| Applying | The row is written and the answer sent | The transaction commits | Waiting |
| Applying | The record or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The product is stale | X6 | Held |

The statuses are the `LOV-LISTING` rows of TSD S5 T3.2; the route states are the DISPOSAL machine's (TSD S5 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal C and R: approves the floor and re-lists the round |
| RW-ENFORCE, RW-NPAMGR, SY-DATALOAD | Asset and disposal C: the listing and price write |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL and the further roles of the read row | Asset and disposal R, in scope |
| PT-AUCTION, PT-RAMC | Asset and disposal R on their own listings |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA where a floor needs approval; the approval fact, not the write |
| SY-CASEWF, SY-RULES, SY-AGENT | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the step; no foreign schema grant and no `v_ace_*` grant |

The rights are the rows of TSD S5 T6.1 and the legacy permission table, nothing wider. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Write: round number, price, status, listed-at |
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | id, case_id, asset_ref, asset_type, transfer_in_type, book_value, holding_status and 8 more | Read |
| Not specified in the source documents (GAP-2920; ASM-4818) | listing (S5, `rwb_asset`) | `relist_count` and the re-list limit as R-DIS-44 and the FSD name them | Write where a column is named |
| Standard columns | listing (S5, `rwb_asset`) | state, version, created_at/by, updated_at/by, is_active | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, transfer_in_type, from_segment, book_value and 7 more | Not read: rwb-source-data contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 19 more | Not read: rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read or written: rwb-decision |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v8. **No new table, no column, no migration**: the tables come with the DB story, and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03). **No personal data**: identifiers, codes, amounts, dates and a rule version only; every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4026-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with the listing, the round number, its price and the floor (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | The same answer on the business key of the Ownership Map | Asset and disposal, R, scope applied | Not applicable |
| POST | `/assets/{assetId}/listings` | The next round and its price, the floor, the reserve and the step schedule in; the listing and round out (API-S5-004) | Asset and disposal, C, scope applied | Idempotency-Key |
| POST | `/assets/{assetKey}/listings` | The same write on the business key | Asset and disposal, C, scope applied | Idempotency-Key |

The listings write is shared with the pricing story (FEAT-AST-11) and the ladder story (RWB-S5-E4022) and no source splits it (GAP-2919; ASM-4817). `POST /listings/{listingId}/rounds` (API-S5-005) is the rounds story's and is not declared here. Errors: 400, 401, 403 with MSG-P4-002, 404, 409 for a listing in the wrong state, 422 with MSG-GEN-001 or MSG-S5-001, 503.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| Asset and valuation product (name Not specified in the source documents (GAP-2921; ASM-4819)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | Asset class, title status, appraised value and book value with the freshness stamp; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state the rules check; faked |
| Case-move answer (name Not specified in the source documents (GAP-2921; ASM-4819)) | rwb-case (P3) | P3 rwb-case | `ROUND_OPEN` and `FLOOR_APPROVED` with the rule and its version; faked |

One hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). They are class C rows the plan does not carry, the C row of this slice being None (GAP-2921).

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's and the sale event the sale story's; a re-listed round writes no outbox row and adds nothing to `rwb.asset.events.v1`. The re-published price reaches the auction portals through FEAT-AST-12, which no operation covers today (GAP-2922). A build that publishes here fails the absence test.

#### 12.4 Events consumed

None. The round-close fact and the floor approval are signals of `AssetDisposalWorkflow`: no subscription, no consumer group, no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new | `rwb-asset` in `rwb-recovery` | Input: case, route, asset, listing, package in force; signals: round-close fact, floor approval |
| `relistOnNoBid` | Activity, the no-bid re-list | `rwb-asset` | Case, listing and round in; rule ID with version, price and round before and after, case move out, one transaction |
| `fixFloorAsReserve` | Activity, the floor approval | `rwb-asset` | Case, listing and approval fact in; reserve, asset-class step schedule, case move out, one transaction |

No child workflow and no second queue. The two activity names are design choices of this story.

#### 12.6 Schedules

None. R-DIS-38 runs "per schedule" as a durable timer inside the workflow; the step owns no Temporal Schedule and no Quartz job. The service's single Schedule is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing; this story writes the next round, its price, the floor, the reserve and the step schedule |
| asset | S5 (`rwb_asset`) | Read only here |
| decision_record | PLT library in `rwb_asset` | One record per outcome (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated signal or request |

Not owned and never read as a table: `asset_sale` (the sale story's), `recovery_case`, `assignment`, `task`, `timer` (P3), `decision_log_entry`, `rule_row`, `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8), every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data product fake | Asset `AST-2026-000526` with its class and title status and the appraisal value and date; an old appraisal; a stale product; no answer inside 2 s | AC1, AC3, X5 to X7 |
| rwb-case state fake | `ROUND_OPEN` and `PRICE_PROPOSED`; a case in another state | AC1 to AC3, X3 |
| rwb-case move fake | The two answers accepted; an answer refused for an unexpected state | AC2, AC3 |
| rwb-decision package fake | The DISPOSAL package at its version with the two rules | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Composite route fake | The merged SCR-23 and SCR-21 answer for `RC-2026-000526` | AC1 |
| Ladder and re-list data fake | A round price above the floor, one at the floor and one under the approver's limit (MSG-S5-001) | AC2, X4 |

The fakes are test-only; the placeholder rows carry their gap until their owners confirm the names (GAP-2921).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 3 consumed | The asset reads and the listings write on `/api/recovery/asset/v1`; the product read, the case state read and the case-move answers; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The round-close fact and the floor approval are workflow signals |
| Temporal | 1 workflow, 2 activities | `AssetDisposalWorkflow`, `relistOnNoBid` and `fixFloorAsReserve` on `rwb-asset`; no Schedule |
| File | None | The portal and HOME.SCB publication is FEAT-AST-12's (GAP-2922) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.relist`; front end `src/modules/recovery/asset/AssetRelist.tsx`, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition; DP-03 is the transaction rule of both activities; DP-13 moves the base; DP-19 is how the screens reach the service. The consumed rows are built on documents and fakes on Day 1 (GAP-2921) and the package is loaded through the service template without the DP-04 row (GAP-2924).

| Component | Type | Responsibility |
|---|---|---|
| No-bid edge of `AssetDisposalWorkflow` | Workflow | Waits on the timer and signals, loads the package in force, reports to the parent |
| `relistOnNoBid` | Activity | Read, evaluate R-DIS-38, write the next round, answer |
| `fixFloorAsReserve` | Activity | Read, evaluate R-DIS-29, write the reserve and the schedule, answer |
| `RelistEvaluator` / `FloorReserveEvaluator` | Services | R-DIS-38 on bid count, round price and floor; R-DIS-29 on the approval and the asset class |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per outcome before any change (DP-03) |
| `ListingWriter` | Repository | `listing` in one transaction with the idempotency row and the lock |
| `CaseMoveAnswer`, `CaseStateClient`, `SourceDataProductClient` | Clients | The two answers and the two reads, one hop, 2 s |
| `AssetController` | Controller | The reads and the write, rights, key and the 400/401/403/404/409/422/503 map |
| `AssetRelist` | React component | The next round, its price, the reserve and the step schedule on SCR-23 |

**Database.** No Flyway file: tables from the DB story, library objects from the library's migration, no column for the re-list count (GAP-2920).

**Configuration.** The ladder, its step and unit, the asset-class step schedule and the `LOV-*` lists at their version; the DISPOSAL package from rwb-decision; the capability rows from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the no-bid edge and its input record; (2) `RelistEvaluator` with the floor and no-fire paths (AC2, X3, X4); (3) `FloorReserveEvaluator` with the age path (AC3, X7); (4) the clients against their fakes (AC1, AC3, X5, X6); (5) the record writer against the stub (AC4, X1); (6) `ListingWriter` (AC2, X8); (7) `CaseMoveAnswer` (AC2, AC3); (8) `AssetController` (AC1); (9) the screen fragment (AC1); (10) the boundary test (X9, BR6, BR7).

**Feature flag.** `rwb.asset.relist-no-bid-v1`; off means the signal is held, nothing is written and no answer is sent.

**Done when.** §16 passes, a closed round re-lists at the next price and answers `ROUND_OPEN` in SIT, an approved floor answers `FLOOR_APPROVED`, a price at the floor re-lists nothing, a repeat writes once, a forced record failure changes nothing, no case row and no `v_ace_*` read exists, and the screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | A floor under the approver's limit on the floor write (X4) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | An appraisal more than a year old at the floor write (X7) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or signal is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the right reads or writes (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the listing changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE product is stale after a late or failed batch (X6) | {product} is from {date}. Today's ACE batch has not arrived. |

The six IDs are the legacy and platform sets, copied unchanged; no message is reworded and none is added.

### 15. Screens and states

SCR-23 Listing and price (draft, below limit, approved, published) and SCR-21 Asset list (loading, list) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, the listing, the round number and price, the floor and the reserve, rwb-case for the state and rwb-source-data for the appraisal. This story fixes the rwb-asset answers only; the route and field list are RWB-PLT-N001-CON.

The states it produces are the re-listed round of SCR-23 — next round number, its price, the reserve and the step schedule — and the refusal, not-recorded, at-floor, old-appraisal and stale states with MSG-P4-002, MSG-P7-003, MSG-S5-001, MSG-S5-002 and MSG-P1-001. Draft, below-limit and published are the pricing and publication stories'.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-026-01 | AC1 | Component | Case `RC-2026-000526` with a live listing and a closed round; the price, the record and the answer on the fakes |
| TC-E4-026-02 | AC2 | Component | Case `RC-2026-000527` at `ROUND_OPEN`, round closed with no bid above the floor |
| TC-E4-026-03 | AC3 | Component | Case `RC-2026-000528` at `PRICE_PROPOSED` with an approved floor and an asset class |
| TC-E4-026-04 | AC4 | Component | Record stub stopped; nothing written, MSG-P7-003 shown |
| TC-E4-026-05 | Access | Component | A role without the right; 403 with MSG-P4-002, no read and no write |
| TC-E4-026-06 | Principle 5 | Component | A forced record failure at the listing write; no row, no answer, no event |

The six cases are the legacy cases in their order with the Level column added: each runs `Component` on its own fakes, because no case here crosses a live boundary. The full text is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the ladder, the asset-class schedule, the floor rule and the appraisal test stay reference data or rule rows with a version.
- No personal data in the schema, a workflow input or a log; every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE read (DP-05).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row here (BR4).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base.
- The record precedes the change and the repeated signal is deduped (DP-03, BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-006 | Auction rounds run down the price ladder to the floor, and a round with no bid re-lists by rule (FSD S5 T8 maps REQ-S5-006 to FEAT-AST-08 while the text names this behaviour: GAP-2923; ASM-4821) | The no-bid edge, the write, the two answers | TC-E4-026-01 to -03 |
| ADR-013 | 19 services inside ACE | rwb-asset owns the listing and its price | TC-E4-026-02 |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-026-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable timer and the signals; no Quartz row | TC-E4-026-02 |
| ADR-020 | Contract-first REST, one hop, 2 s | The three consumed rows | TC-E4-026-01, -03 |
| ADR-022 | Local decision record plus central ledger | The record before the change | TC-E4-026-04, -06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-026, Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word |
| Test cases | TC-E4-026-01 to TC-E4-026-06 |
| Feature and screens | FEAT-AST-17, SCR-23 and SCR-21 |
| Rules | R-DIS-38 and R-DIS-29, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |

### 19. Out of scope

- The shapes, the consumed rows, the record and package elements, the error set and the fakes: RWB-S5-E4026-CON.
- The ladder step itself and R-DIS-17: RWB-S5-E4022 (GAP-2918).
- The start price, the head of NPA's approval and the floor limit: FEAT-AST-11's pricing story (GAP-2919).
- The publication to HOME.SCB, the EASY app and the portal, and the re-publication of a stepped round: FEAT-AST-12, INT-27, rwb-document (P5) (GAP-2922).
- The rounds, the bids and the award, and API-S5-005: the rounds story of RWB-E4-024.
- The re-appraisal cycle, R-DIS-44 and the re-list limit as a reference row: FEAT-AST-09's story and JOB-19 (GAP-2920).
- The case, its states and the parent workflow: rwb-case (P3).
- The asset and valuation facts and the freshness stamp: rwb-source-data (P1).
- The rule rows and the package version: rwb-decision (P7) (GAP-2924).
- The composite route and field list: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey: the wave 3 harness.
- The deployment, flag, dashboards and runbook: the operations story of this key.

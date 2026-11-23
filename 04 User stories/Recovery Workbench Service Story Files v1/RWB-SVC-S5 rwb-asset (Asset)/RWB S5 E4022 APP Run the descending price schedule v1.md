# RWB-S5-E4022-APP Run the descending price schedule

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4022-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-022 for rwb-asset. The four legacy criteria are kept word for word with their origin tag and the six legacy test cases keep their IDs. The step becomes the ladder branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: it evaluates R-DIS-38 and R-DIS-17 on the DISPOSAL package in force, writes the next price and the reset inputs on `listing` in `rwb_asset`, records each outcome before the row changes (DP-03), answers `ROUND_OPEN` and `ASSET_HELD` to rwb-case and publishes nothing. The `v_ace_*` reads arrive on the rwb-source-data contract (DP-05), the base becomes `/api/recovery/asset/v1` (DP-13), and the screens read through the gateway-bff route (DP-19). Gaps: consumed operation names (GAP-2895; ASM-4792); no round-price column (GAP-2896; ASM-4793); API-S5-004 shared by two stories (GAP-2897; ASM-4794); no requirement id (GAP-2898; ASM-4795); DP-04 outside the pattern set (GAP-2899; ASM-4796). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **the Workbench to step the price down on the ladder at each round until a bid clears the floor**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E4-022. It owns the four legacy criteria with their origin tag; the ladder branch of `AssetDisposalWorkflow` on `rwb-asset` as a child of the case workflow (Architecture v5 slide 13); R-DIS-38 on a round closed with no bid and R-DIS-17 on an accepted re-appraisal, on the package in force; the next price and round number and the reset list and floor inputs on `listing` in `rwb_asset`; the decision record before each change (DP-03) and the answers `ROUND_OPEN` and `ASSET_HELD`; and the reads of SCR-23 and SCR-21 on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the shapes, the consumed rows and the fakes, which are RWB-S5-E4022-CON; the start price, the floor and its approval (FEAT-AST-11's story); the listing publication (FEAT-AST-12); the rounds and bids (the rounds story of RWB-E4-024); the appraisal order (rwb-valuation, S1); the case and its states (rwb-case, P3); the ACE facts (rwb-source-data, P1); the rule package (rwb-decision, P7); and the deployment (the operations story of this key).

### 2. Business rationale

Legacy RWB-E4-022 kept a listing moving: on a round with no bid the price stepped down the approved ladder, the next round opened, and an accepted re-appraisal rewrote the list and floor inputs. The FSD keeps it as FEAT-AST-13 in module S5, running unattended with the sale officer as acting role, against an NPA sales cycle of 1,095 days (FSD S5 A2.13).

What D-RCV-60 changes:

- **the price is this service's.** `listing` is S5's in `rwb_asset` (Ownership Map; Architecture v5 slide 41); the ladder is reference data with a version, never a constant.
- **the value stays with rwb-source-data (P1).** Only that service reads the `recovery.v_ace_*` views (Architecture v5 slide 8), so DP-05 is a **prohibition** and the facts arrive on the owner's product with a freshness stamp.
- **the case stays with rwb-case (P3).** This story evaluates, writes, records and **answers** the move; it writes no case row.
- **the decision is recorded first**, one per outcome, in the row's transaction — what AC1 asked and AC4 tested.
- **nothing is published.** EV-22 `AssetTakenOn` is the take-on story's (TSD S5 T5.3); §12.3 states the absence and a build that adds an event fails it.

### 3. Preconditions

- RWB-S5-E4022-CON tagged: reads, listings write, consumed rows, record element, error set, fakes.
- `listing` and `asset` exist in `rwb_asset` with the TSD S5 T3.1 and T3.0 columns; no column is added for the round price (GAP-2896; ASM-4793).
- The DISPOSAL package is in force with the two rules from rwb-decision (P7), loaded through the service template; DP-04 is outside the pattern set (GAP-2899; ASM-4796).
- The ladder, its step and unit and the `LOV-*` lists are reference data with a version (TSD S5 T3.2).
- The rwb-case state read and the case-move answer sit behind fakes; the move's name is not published (GAP-2895; ASM-4792).
- The rwb-source-data product with the appraisal and asset facts is published with a fake and a freshness stamp; its name is not published (GAP-2895).
- The round-close fact arrives as a workflow signal from the rounds story; no subscription is added.
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass.

### 4. Flow

1. A round of a live listing closes with no bid; the rounds story signals the workflow with case, asset, listing and round, and the step confirms the case state on the rwb-case contract.
2. The step reads the listing: start price, floor, round number, sale channel, status.
3. It reads the appraisal and asset facts on the rwb-source-data product, one hop, 2 s: appraised value, appraisal date, outlier flag, book value.
4. `LadderEvaluator` loads the package in force and evaluates R-DIS-38: from `ROUND_OPEN`, on `ROUND_CLOSED_NO_BID`, with `bid_count = 0` and the round price above the floor, the price steps down and the next round opens, the case staying in `ROUND_OPEN` (Business Rules and Routing Logic v4).
5. `AssetDecisionRecordWriter` writes one record **before any change**; a failed write stops the step (DP-03; AC1, AC4).
6. `ListingWriter` writes the next price and round number in one transaction with the record and the idempotency row; where no column holds the round price the value is Not specified in the source documents (GAP-2896).
7. `CaseMoveAnswer` answers `ROUND_OPEN` with the round number, the new price, the rule and its version; rwb-case writes the case.
8. Where the round price is already at the floor, R-DIS-38 does not fire: nothing is written and the floor is reported to the parent (X4).
9. On an accepted re-appraisal R-DIS-17 applies: from `REAPPRAISAL_RECEIVED`, on `VALUE_ACCEPTED`, with the outlier flag clear or the value accepted by an officer, the appraised value is written, the list and floor inputs are reset, and the case moves to `ASSET_HELD`.
10. A second record is written before the reset commits; no event and no outbox row leaves the service (§12.3).
11. A repeated signal or `Idempotency-Key` writes once and is counted; the step returns to its durable timer and the workflow continues as new at each stage end and at least every 28 days.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered | MSG-P7-003 | AC4, TC-E4-022-04, -06 |
| X2 | The role lacks the right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-022-05 |
| X3 | The case is in another state | The rule does not fire; nothing written, state reported | None | AC2, AC3 |
| X4 | The round price is at the floor | No step, no record, no move; floor reported | MSG-S5-001 where under the limit | AC2 |
| X5 | A contract misses 2 s or its breaker is open | Retry on the workflow schedule; 503 | None | AC1, AC3 |
| X6 | The ACE product is stale | Held, nothing written, the data date shown | MSG-P1-001 | AC3 |
| X7 | The appraisal is more than a year old | The reset is held and a new appraisal asked for | MSG-S5-002 | AC3 |
| X8 | The same signal arrives twice | One step, one answer, no second record | None | AC1, AC2 |
| X9 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | §17, BR6 |

X1 to X3 are the legacy paths on the split, X4 to X8 what the ladder, the call types and the appraisal age add, and X9 the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the fakes; no live P1, P3 or P7 |
| Negotiable | Activity name, decision code and outcome shape are ours; rules, messages, screens, row and reads are fixed |
| Valuable | The price steps the approved ladder the day the round closes |
| Estimable | One branch, two evaluators, one record, one row change, one answer, two clients |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, floor and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Run the descending price schedule

  Background:
    Given case "RC-2026-000531" holds asset "AST-2026-000531" in listing "LS-2026-000531"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-38 and R-DIS-17
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Run the descending price schedule (legacy RWB-E4-022 AC1)
    Given the rwb-source-data contract mock returns the appraisal "AP-2026-000531" and the NPA asset "AST-2026-000531" of case "RC-2026-000531"
    Given the rwb-case contract mock returns the case state ROUND_OPEN for "RC-2026-000531"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then steps the price down on the ladder at each round until a bid clears the floor
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-38 (legacy RWB-E4-022 AC2)
    Given the rwb-case contract mock returns the case state ROUND_OPEN for "RC-2026-000532"
    Given a case in state ROUND_OPEN
    When round closed no bid
    Then step the price down on the published schedule and open the next round
    Then the case moves to ROUND_OPEN

  Scenario: AC3 Rule R-DIS-17 (legacy RWB-E4-022 AC3)
    Given the rwb-source-data contract mock returns the appraisal "AP-2026-000533" of asset "AST-2026-000533" with the outlier flag clear
    Given the rwb-case contract mock returns the case state REAPPRAISAL_RECEIVED for "RC-2026-000533"
    Given a case in state REAPPRAISAL_RECEIVED
    When value accepted
    Then update the appraised value and reset the list and floor price inputs
    Then the case moves to ASSET_HELD

  Scenario: AC4 Not recorded (legacy RWB-E4-022 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria word for word with the origin tag added: the repeated `Then`, `the action is taken`, `its trigger arrives` and `the decision log cannot be written` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-source-data answers the facts, rwb-case writes the moves, and this story evaluates, writes, records and answers. AC3 resets the inputs; the floor itself is approved by the head of NPA in FEAT-AST-11's story (GAP-2897; ASM-4794).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-38 | Asset disposal | D8.1 to D8.3 | ROUND_OPEN | ROUND_CLOSED_NO_BID | bid_count = 0 and price_at_round above floor_price | Step the price down on the published schedule and open the next round | ROUND_OPEN | Workbench | Rules component, Workbench scheduler | per schedule |
| R-DIS-17 | Asset disposal | D8.1 to D8.3 | REAPPRAISAL_RECEIVED | VALUE_ACCEPTED | outlier_flag = N or officer_accepted = Y | Update the appraised value and reset the list and floor price inputs | ASSET_HELD | Workbench | SVAF, Workbench | None |

Both rows are copied character for character from the Business Rules and Routing Logic v4; their owner column is a business role, so rwb-case holds the states on this story's answer while the `listing` row is written here. FSD S5 A2.13 also lists R-DIS-28 (the pricing agent's proposal, moving to `PRICE_PROPOSED`); it is FEAT-AST-11's and is not evaluated here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The price is this service's: start price, floor, round number, status and appraised value are `listing` elements in `rwb_asset` | Ownership Map; Architecture v5 slide 41; TSD S5 T3.1 |
| BR2 | The record precedes the change, one per outcome, with the rule and package version | DP-03; AC1, AC4 |
| BR3 | The ladder, floor rule and outlier test are reference data or rule rows with a version | TSD S5 T3.2; legacy Guardrails |
| BR4 | The case move is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2895 |
| BR5 | The round price is held only where a column is named | TSD S5 T3.1; GAP-2896 |
| BR6 | The appraisal and asset facts stay with rwb-source-data; no `v_ace_*` read here | DP-05; Architecture v5 slide 8 |
| BR7 | No event is published; EV-22 `AssetTakenOn` is the take-on story's | TSD S5 T5.3 |
| BR8 | A repeated signal or key writes once, answers once and is counted | TSD S5 T-A.2 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset` | DP-01; TSD S5 T3.3 |
| BR10 | No personal data in the schema, a record, a log or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR4).

| From (`listing` status) | Event | Condition | To |
|---|---|---|---|
| Live, round closed with no bid | `ROUND_CLOSED_NO_BID` under R-DIS-38 | Bid count 0 and round price above the floor | Live at the stepped price; answer `ROUND_OPEN` |
| Live, round closed with no bid | `ROUND_CLOSED_NO_BID` under R-DIS-38 | Round price at the floor | Unchanged (X4) |
| Live, re-appraisal accepted | `VALUE_ACCEPTED` under R-DIS-17 | Outlier flag clear or officer accepted | Live, inputs reset; answer `ASSET_HELD` |
| Live, re-appraisal accepted | `VALUE_ACCEPTED` under R-DIS-17 | Appraisal more than a year old | Unchanged, reset held (X7) |
| Any | The same signal again, or an unexpected state | X8, X3 | Unchanged |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting on the timer | A round-close signal for a live listing | The package in force is loaded | Evaluating |
| Evaluating | A rule fires | The record is written | Applying |
| Applying | The row is written and the answer sent | The transaction commits | Waiting |
| Applying | The record or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The product is stale | X6 | Held |

The statuses are the `LOV-LISTING` rows of TSD S5 T3.2; the route states are the DISPOSAL machine's (TSD S5 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal C and R: sets the next round price, reads the ladder |
| RW-ENFORCE, RW-NPAMGR, SY-DATALOAD | Asset and disposal C: the listing and price write |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL and the further roles of the read row | Asset and disposal R, in scope |
| PT-AUCTION, PT-RAMC | Asset and disposal R on their own listings |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA where a floor needs approval; none here |
| SY-CASEWF, SY-RULES, SY-AGENT | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the step; no foreign schema grant and no `v_ace_*` grant |

The rights are the rows of TSD S5 T6.1 and the legacy permission table, nothing wider. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Write: next price, round number, status |
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | id, case_id, asset_ref, asset_type, transfer_in_type, book_value, holding_status and 8 more | Read |
| Not specified in the source documents (GAP-2896; ASM-4793) | listing (S5, `rwb_asset`) | `price_at_round` as the rule names it | Write where a column is named |
| Standard columns | listing (S5, `rwb_asset`) | state, version, created_at/by, updated_at/by, is_active | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | valuation_key, asset_key, appraisal_no, appraised_value, appraisal_date and 4 more | Not read: rwb-source-data contract |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, transfer_in_type, from_segment, book_value and 7 more | Not read: rwb-source-data contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and 19 more | Not read: rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 10 more | Not read or written: rwb-decision |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v8. **No new table, no column, no migration**: the tables come with the DB story, and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03). **No personal data**: identifiers, codes, amounts, dates and a rule version only; every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4022-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with title, listing, round price, floor and round number (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | The same answer on the business key of the Ownership Map | Asset and disposal, R, scope applied | Not applicable |
| POST | `/assets/{assetId}/listings` | Price of the round and floor in, listing and round out (API-S5-004) | Asset and disposal, C, scope applied | Idempotency-Key |
| POST | `/assets/{assetKey}/listings` | The same write on the business key | Asset and disposal, C, scope applied | Idempotency-Key |

The listings write is shared with FEAT-AST-11's pricing story and no source splits it (GAP-2897; ASM-4794). `POST /listings/{listingId}/rounds` (API-S5-005) is the rounds story's. Errors: 400, 401, 403 with MSG-P4-002, 404, 409 for a listing in the wrong state, 422 with MSG-GEN-001 or MSG-S5-001, 503.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| Appraisal and asset product (name Not specified in the source documents (GAP-2895; ASM-4792)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | Appraised value, date, outlier flag, book value with the freshness stamp; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state the rules check; faked |
| Case-move answer (name Not specified in the source documents (GAP-2895; ASM-4792)) | rwb-case (P3) | P3 rwb-case | `ROUND_OPEN` and `ASSET_HELD` with the rule and its version; faked |

One hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). They are class C rows the plan does not carry, the C row of this slice being None (GAP-2895).

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's and the sale event the sale story's; a stepped price writes no outbox row and adds nothing to `rwb.asset.events.v1`. A build that publishes here fails the absence test.

#### 12.4 Events consumed

None. The round-close fact is a signal of `AssetDisposalWorkflow` from the rounds story: no subscription, no consumer group, no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new | `rwb-asset` in `rwb-recovery` | Input: case, route, asset, listing, package in force; signals: round-close fact, accepted appraisal |
| `stepDownPrice` | Activity, the ladder step | `rwb-asset` | Case, listing and fact in; rule IDs with versions, price before and after, round number and case move out, one transaction |

No child workflow and no second queue. The activity name is a design choice of this story.

#### 12.6 Schedules

None. R-DIS-38 runs "per schedule" as a durable timer inside the workflow; the step owns no Temporal Schedule and no Quartz job. The service's single Schedule is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing; this story writes its price, round number and status |
| asset | S5 (`rwb_asset`) | Read only here |
| decision_record | PLT library in `rwb_asset` | One record per outcome (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated signal or request |

Not owned and never read as a table: `asset_sale` (the sale story's), `recovery_case`, `assignment`, `task`, `timer` (P3), `decision_log_entry`, `rule_row`, `approval` (P7), `valuation` (S1), `document` (P5), `deviation` (S8), every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data product fake | Appraisal `AP-2026-000531` of asset `AST-2026-000531` with value, date and a clear outlier flag, plus the NPA asset book value; an old appraisal; a stale product; no answer inside 2 s | AC1, AC3, X5 to X7 |
| rwb-case state fake | `ROUND_OPEN` and `REAPPRAISAL_RECEIVED`; a case in another state | AC1 to AC3, X3 |
| rwb-case move fake | The two moves accepted; a move refused for an unexpected state | AC2, AC3 |
| rwb-decision package fake | The DISPOSAL package at its version with the two rules | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Composite route fake | The merged SCR-23 and SCR-21 answer for `RC-2026-000531` | AC1 |

The fakes are test-only; the placeholder rows carry their gap until their owners confirm the names (GAP-2895).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 5 provided, 2 consumed | The asset reads and the listings write on `/api/recovery/asset/v1`; the product read, the state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The round-close fact is a workflow signal |
| Temporal | 1 workflow, 1 activity | `AssetDisposalWorkflow` and `stepDownPrice` on `rwb-asset`; no Schedule |
| File | None | The portal and HOME.SCB publication is FEAT-AST-12's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.pricing`; front end `src/modules/recovery/asset/AssetPriceLadder.tsx`, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition (no `v_ace_*` grant, no ACE read); DP-03 is the transaction rule of the step; DP-13 moves the base; DP-19 is how the screens reach the service. The three consumed rows are class C and the plan's C row is None, so they are built on documents and fakes on Day 1 (GAP-2895). The package in force is loaded through the service template without the DP-04 platform row (GAP-2899).

| Component | Type | Responsibility |
|---|---|---|
| Ladder branch of `AssetDisposalWorkflow` | Workflow | Waits on the timer and signals, loads the package in force, reports to the parent |
| `stepDownPrice` | Activity | Read, evaluate, write, answer |
| `LadderEvaluator` / `ReappraisalEvaluator` | Services | R-DIS-38 on bid count, round price and floor; R-DIS-17 on the value, outlier flag and age |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per outcome before any change (DP-03) |
| `ListingWriter` | Repository | `listing` in one transaction with the idempotency row and the lock |
| `CaseMoveAnswer`, `CaseStateClient`, `SourceDataProductClient` | Clients | The two moves and the two reads, one hop, 2 s |
| `AssetController` | Controller | The reads and the write, rights, key and the 400/401/403/404/409/422/503 map |
| `AssetPriceLadder` | React component | The ladder, round prices, floor and reset value on SCR-23 |

**Database.** No Flyway file: tables from the DB story, library objects from the library's migration, no column for the round price (GAP-2896).

**Configuration.** The ladder, step and unit and the `LOV-*` lists at their version; the DISPOSAL package from rwb-decision; the capability rows from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the ladder branch and its input record; (2) `LadderEvaluator` with the floor and no-fire paths (AC2, X3, X4); (3) `ReappraisalEvaluator` with the outlier and age paths (AC3, X7); (4) the clients against their fakes (AC1, AC3, X5, X6); (5) the record writer against the stub (AC4, X1); (6) `ListingWriter` (AC2, X8); (7) `CaseMoveAnswer` (AC2, AC3); (8) `AssetController` (AC1); (9) the screen fragment (AC1); (10) the boundary test (X9, BR6, BR7).

**Feature flag.** `rwb.asset.price-ladder-v1`; off means the signal is held, nothing is written and no move is answered.

**Done when.** §16 passes, a closed round steps the price and answers `ROUND_OPEN` in SIT, an accepted appraisal answers `ASSET_HELD`, a price at the floor steps nothing, a repeat writes once, a forced record failure changes nothing, no case row and no `v_ace_*` read exists, and the screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | A floor under the approver's limit on the price write (X4) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | An appraisal more than a year old at the reset (X7) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or signal is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the right reads or writes (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the listing changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE product is stale after a late or failed batch (X6) | {product} is from {date}. Today's ACE batch has not arrived. |

The six IDs are the legacy and platform sets, copied unchanged; no message is reworded and none is added.

### 15. Screens and states

SCR-23 Listing and price (draft, below limit, approved, published) and SCR-21 Asset list (loading, list) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, listing, round prices and floor, rwb-case for the state and rwb-source-data for the appraisal. This story fixes the rwb-asset answers only; the route and field list are RWB-PLT-N001-CON.

The states it produces are the published ladder state of SCR-23 — round number, round price, floor, reset value — and the refusal, not-recorded, at-floor, old-appraisal and stale states with MSG-P4-002, MSG-P7-003, MSG-S5-001, MSG-S5-002 and MSG-P1-001. Draft, below-limit and approved are the pricing story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-022-01 | AC1 | Component | Case `RC-2026-000531` with a live listing and a closed round; price, records and move on the fakes |
| TC-E4-022-02 | AC2 | Component | Case `RC-2026-000532` at `ROUND_OPEN`, round closed with no bid above the floor |
| TC-E4-022-03 | AC3 | Integration | Case `RC-2026-000533` at `REAPPRAISAL_RECEIVED` with an accepted appraisal, across the two fakes |
| TC-E4-022-04 | AC4 | Component | Record stub stopped; nothing written, MSG-P7-003 shown |
| TC-E4-022-05 | Access | Component | A role without the right; 403 with MSG-P4-002, no read and no write |
| TC-E4-022-06 | Principle 5 | Component | A forced record failure at the listing write; no row, no answer, no event |

The six cases are the legacy cases in their order with the Level column added: TC-E4-022-03 runs `Integration` because it crosses two boundaries, the rest `Component` on their fakes. The full text is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the ladder, floor rule, outlier test and statuses stay reference data or rule rows with a version.
- No personal data in the schema, a workflow input or a log; every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE read (DP-05).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row here (BR4).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base.
- The record precedes the change and the repeated signal is deduped (DP-03, BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | FEAT-AST-13 of FSD S5 A2.13 and BR-027 of the epic BRD: a round with no bid re-lists at the next step until a bid clears the floor (GAP-2898; ASM-4795) | The ladder branch, the write, the moves | TC-E4-022-01 to -03 |
| ADR-013 | 19 services inside ACE | rwb-asset owns the listing and its price | TC-E4-022-02 |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-022-06 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable timer and the signal; no Quartz row | TC-E4-022-02 |
| ADR-020 | Contract-first REST, one hop, 2 s | The three consumed rows | TC-E4-022-01, -03 |
| ADR-022 | Local decision record plus central ledger | The record before the change | TC-E4-022-04, -06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-022, Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word |
| Test cases | TC-E4-022-01 to TC-E4-022-06 |
| Feature and screens | FEAT-AST-13, SCR-23 and SCR-21 |
| Rules | R-DIS-38 and R-DIS-17, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |

### 19. Out of scope

- The shapes, the consumed rows, the record element, the error set and the fakes: RWB-S5-E4022-CON.
- The start price, the floor and the head of NPA's approval: FEAT-AST-11's story (GAP-2897).
- The publication to HOME.SCB, the EASY app and the portal: FEAT-AST-12, INT-27 and rwb-document (P5).
- The rounds, bids and award: the rounds story of RWB-E4-024 and API-S5-005.
- The appraisal order and cycle: rwb-valuation (S1) and the re-appraisal story with JOB-19.
- The case, its states and the parent workflow: rwb-case (P3).
- The appraisal and asset facts and the freshness stamp: rwb-source-data (P1).
- The rule rows and the package version: rwb-decision (P7) (GAP-2899).
- The composite route and field list: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey: the wave 3 harness.
- The deployment, flag, dashboards and runbook: the operations story of this key.

# RWB-S5-E4023-APP Allocate the asset to an auction vendor by distance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4023-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-023 split out for rwb-asset. The four legacy acceptance criteria are kept word for word with their origin tag; the allocation becomes the vendor branch of `AssetDisposalWorkflow` on task queue `rwb-asset`, signalled `VENDOR_REQUIRED` at `FLOOR_APPROVED` and `VENDOR_UNAVAILABLE` at `VENDOR_ALLOCATED`, evaluates R-DIS-30 and then R-DIS-31 with the DISPOSAL package version in force, reads the asset and scorecard facts on the rwb-source-data data-product contract and the vendor panel, its capacity and its panel status on the rwb-partner activity (DP-05), records each rule outcome through the local decision-record library before the case move leaves the service (DP-03) and answers `VENDOR_ALLOCATED` to rwb-case. The legacy `v_ace_npa_asset` and `v_ace_score` reads are retired as service reads because rwb-asset holds no ACE view grant; the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-23 read through the gateway-bff composite route (DP-19). The feature describes the basis as "distance and capacity" while R-DIS-30 and R-DIS-31 allocate on the scorecard price, which is recorded rather than smoothed (GAP-2900; ASM-4797); the trigger, the partner panel read and the four-vendor list have no published operation and no plan row (GAP-2901; ASM-4798, ASM-4799); the allocation has no column and no list value to be written to (GAP-2902; ASM-4800); no requirement covers vendor allocation (GAP-2903; ASM-4801). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4023-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **the Workbench to pick one of the four vendors by distance and capacity, as the current rule does**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E4-023. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- one vendor-allocation branch of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, as a stage of the workflow whose parent the case owns (Architecture v5 slide 13, "Asset disposal · rwb-asset · DIS 72");
- the evaluation of R-DIS-30 at `FLOOR_APPROVED` on `VENDOR_REQUIRED`, and of R-DIS-31 at `VENDOR_ALLOCATED` on `VENDOR_UNAVAILABLE`, with the DISPOSAL package version in force;
- the asset facts of the case (`asset_type`, `asset_ref`, `book_value`) and the scorecard predicted price of each vendor, taken on the rwb-source-data data-product contract (DP-05);
- the vendor panel of four, its capacity flag and its panel status, taken on the rwb-partner activity of queue `rwb-partner`, which is the call type the connection matrix gives S5→S9 (Architecture v5 slide 13, row S5 Asset, column S9; GAP-2901; ASM-4799);
- the local decision record of each rule outcome, written through RWB-PLT-E1027-CON before any move leaves the service (DP-03);
- the answer to rwb-case for the move `VENDOR_ALLOCATED`, with the rule ID, the vendor reference and the version that produced them;
- the reads behind SCR-21 Asset list and SCR-23 Listing and price on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two reads, the consumed rows, the case-move answer, the decision-record element, the error set and the fakes, which are RWB-S5-E4023-CON; the start price, the floor price, the listing and the auction rounds, which are the pricing, listing and auction stories of this service (API-S5-004, API-S5-005); the vendor panel, its capacity, its panel status, the partner instruction and the vendor scorecard, which are rwb-partner's (S9); the case of record, the states `FLOOR_APPROVED` and `VENDOR_ALLOCATED`, the parent `CaseWorkflow` and the case timers, which are rwb-case's (P3); the ACE asset and scorecard facts, which are rwb-source-data's (P1); the rule rows, the package and its version, which are rwb-decision's (P7); the parameter and reference-data rows of FEAT-PRM-03, which are read with the rule package and the reference-data contract; and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E4-023 placed the asset with a vendor after the floor price was approved, and the workbench chose among the four vendors of the panel instead of leaving the choice to a telephone round of calls. The FSD keeps the feature as FEAT-AST-14 "Allocate the asset to an auction vendor by distance" in module S5, system-run, with the sale officer as the using role and the NPA sales cycle of 1,486 days against a target of 1,095 days as its metric (FSD S5 A2.14.1, A2.14.3.3).

What D-RCV-60 changes is who owns the choice, the panel and the record.

- **the choice is this service's.** The allocation is the outcome of a DISPOSAL rule evaluated here, and the decision record is written here before the case moves; the service is the owner of the asset disposal stage (Architecture v5 slide 13).
- **the panel is rwb-partner's (S9).** The four vendors, `vendor_capacity` and `panel_status` are partner facts. The connection matrix gives S5→S9 a Temporal call and no REST, and shared capabilities are reached through Temporal and never REST (Architecture v5 slide 13 notes), so the panel is read on the partner activity and never as a table (GAP-2901; ASM-4799).
- **the asset and its score are rwb-source-data's (P1).** The legacy data table names `v_ace_npa_asset` and `v_ace_score`; in the target only rwb-source-data reads the `recovery.v_ace_*` views, so DP-05 applies as a **prohibition** and both facts arrive on the owner's data-product contract.
- **the case stays with rwb-case (P3).** `recovery_case`, `assignment` and the route states live there. This story evaluates the rules and **answers** the move `VENDOR_ALLOCATED`; it writes no case row and no assignment row (GAP-2901; ASM-4799).
- **the allocation itself is a record, not a row.** The target's S5 tables are `asset_sale` and `listing`, and neither carries a vendor, a distance or an allocation state (GAP-2902; ASM-4800). The chosen vendor, the basis and the score are held as facts of the decision record, and the listing is created later by the pricing and listing story.
- **the basis is the rule's, and the feature wording differs.** FEAT-AST-14 and AC1 say "by distance and capacity, as the current rule does", while R-DIS-30 and R-DIS-31 allocate on the highest predicted price of the scorecard, "not by distance" (Business Rules and Routing Logic v4). The conflict is recorded, the rule decides, and the distance and capacity remain reference-data inputs of the rule rather than a second selection path in code (GAP-2900; ASM-4797).

No business value moves: the panel size, the capacity codes, the panel statuses and the score thresholds stay reference data or rule rows read with their version.

### 3. Preconditions

- RWB-S5-E4023-CON is published: the two reads, the consumed rows, the workflow signal elements, the case-move answer, the decision-record element, the error set and the fakes are baselined and handed to this story.
- The case is in `FLOOR_APPROVED` and the parent `CaseWorkflow` has forwarded `VENDOR_REQUIRED` to the asset disposal child; or the case is in `VENDOR_ALLOCATED` and the parent has forwarded `VENDOR_UNAVAILABLE` (Business Rules and Routing Logic v4 R-DIS-30, R-DIS-31). No source names a published operation or event that carries either signal: the trigger is Not specified in the source documents (GAP-2901; ASM-4798).
- The DISPOSAL rule package is in force at its version with R-DIS-30 and R-DIS-31; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The parameter and reference-data rows that FEAT-PRM-03 names (the four-vendor panel, the capacity codes, the panel statuses) are read with their version and are not written in code (GAP-2901; ASM-4799).
- The rwb-source-data data product that carries the asset fact and the scorecard predicted price (`v_ace_npa_asset` and `v_ace_score` in the legacy) is published with its fake. Its operation names are Not specified in the source documents (GAP-2901; ASM-4798).
- The rwb-partner vendor-panel activity of queue `rwb-partner` is published with its fake: the four vendors, each with its capacity flag, its panel status and its distance to the asset. The activity name is Not specified in the source documents (GAP-2901; ASM-4799).
- The rwb-case case state read (`GET /cases/{caseId}` family) and the case-move answer are available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent applies (GAP-2901; ASM-4798).
- RWB-PLT-E1027-CON is published with its writer fake: the decision record writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the record and the case-move answer commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-23 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `asset_sale` and `listing` exist in schema `rwb_asset` from the DB story of this service; this story adds no table, no column and no migration. Where the vendor reference would need a column of its own it is Not specified in the source documents (GAP-2902; ASM-4800).
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset`, `recovery.v_ace_score` or `rwb_case` is refused by the database and fails the boundary test (DP-05).
- No approval is needed to build against a Draft contract baseline, and the missing approval of the realigned stories is recorded rather than waited for (GAP-2904; ASM-4802); the contract is tagged by RWB-S5-E4023-CON when its tests pass.

### 4. Flow

1. The floor price of the asset is approved and the parent `CaseWorkflow` forwards `VENDOR_REQUIRED` to the asset disposal child on queue `rwb-asset`; the case is in `FLOOR_APPROVED` (R-DIS-30).
2. The allocation branch of `AssetDisposalWorkflow` starts with the case reference, the asset reference and the rule package in force, and reads the case state on the rwb-case contract to confirm `FLOOR_APPROVED` (GAP-2901; ASM-4798).
3. The step reads the asset fact of the case on the rwb-source-data data product: `asset_ref`, `asset_type`, `transfer_in_type`, `book_value` and the freshness stamp (GAP-2901; ASM-4798).
4. The step reads the vendor panel on the rwb-partner activity of queue `rwb-partner`: the four vendors, each with its capacity flag, its panel status and its distance to the asset (GAP-2901; ASM-4799).
5. The step reads the scorecard predicted price of each vendor of the panel on the rwb-source-data data product (`v_ace_score` in the legacy), read only with its version (GAP-2901; ASM-4798).
6. `VendorAllocationEvaluator` loads the DISPOSAL package version in force and evaluates R-DIS-30 on the combined fact: from `FLOOR_APPROVED`, on `VENDOR_REQUIRED`, with `asset_type = vehicle`, the asset is allocated to the vendor with the highest predicted price on the scorecard, not by distance, and the case moves to `VENDOR_ALLOCATED` (Business Rules and Routing Logic v4). Distance and capacity are inputs of the rule and never a second selection path in code (GAP-2900; ASM-4797).
7. `AssetDecisionRecordWriter` writes one decision record through the local decision-record library **before the move leaves the service**: the case reference, the asset reference, the rule ID with its version, the inputs reference, the chosen vendor, the basis, the score and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `CaseMoveAnswer` answers rwb-case with `VENDOR_ALLOCATED`, the rule ID, the vendor reference and the decided-at time; rwb-case writes the `recovery_case` row and its route state, and this service writes neither.
9. Where the chosen vendor reports `vendor_capacity = N` or `panel_status = suspended`, the parent forwards `VENDOR_UNAVAILABLE` and `VendorReallocationEvaluator` evaluates R-DIS-31: from `VENDOR_ALLOCATED`, the asset is re-allocated to the next vendor on the scorecard and the case stays in `VENDOR_ALLOCATED` (Business Rules and Routing Logic v4). A second decision record is written for the second outcome, again before the move (DP-03).
10. Where every vendor of the panel is unavailable, the step exhausts the scorecard and reports the panel to the parent; no fourth state is invented and no value is written (GAP-2901; ASM-4799).
11. No event is published and none is consumed: the two triggers are signals of the DISPOSAL machine, and `rwb.asset.events.v1` carries `AssetTakenOn` (EV-22) and `AssetSold`, both other stories' (§12.3, §12.4).
12. A repeated `VENDOR_REQUIRED` or `VENDOR_UNAVAILABLE` signal for the same case and rule writes once, answers once and counts the repeat; the workflow id keeps one execution per case per stage.
13. SCR-21 Asset list and SCR-23 Listing and price read the asset, its allocation and its chosen vendor from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no record, no case-move answer and no allocation fact leaves the service | MSG-P7-003 | AC4, TC-E4-023-04, TC-E4-023-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E4-023-05 |
| X3 | The case is not in `FLOOR_APPROVED` for R-DIS-30, or not in `VENDOR_ALLOCATED` for R-DIS-31 | The rule does not fire: nothing is written and the step reports the state to the parent | None | AC2, AC3 |
| X4 | The rwb-source-data, rwb-partner or rwb-case answer does not arrive inside 2 s, or the partner activity fails | The step retries on the workflow's own schedule; nothing is written and no move is answered | None | AC1, AC3 |
| X5 | The ACE data product is stale after a late or failed ACE batch | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 (VR-S5-014-1) | AC1, AC3 |
| X6 | The panel returns no vendor with `vendor_capacity = Y` on a permitted panel status | Nothing is allocated, nothing is written, and the step reports the exhausted panel; no vendor is invented | None | AC3 |
| X7 | A repeated signal for the same case and rule | One change, one answer, no second decision record; the repeat is counted | None | AC1, AC3 |
| X8 | The asset is not a vehicle | R-DIS-30 does not fire and no scorecard allocation is made; the distance-and-capacity basis of FEAT-AST-14 has no rule row in the sources and is Not specified in the source documents | None | AC2 |
| X9 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, an `assignment` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR6 |

X1 to X3 are the exception paths of RWB-E4-023 carried onto the split, X4 to X6 are the paths the target call types and the panel add, X7 and X8 are the repeat and the unstated basis, and X9 is the DP-05 and DP-01 boundary (GAP-2900, GAP-2901; ASM-4797, ASM-4799).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E4023-CON, the rwb-source-data, rwb-partner and rwb-case fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or S9 |
| Negotiable | The activity name, the decision code per rule outcome and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two reads and the panel are fixed |
| Valuable | The asset reaches a vendor the day its floor is approved, and the choice is on the decision log rather than on a round of calls |
| Estimable | One workflow branch, two evaluators, one record write, one panel activity, two clients, one case-move answer and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, assets, panels and scores through the contract fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Allocate the asset to an auction vendor by distance

  Background:
    Given case "RC-2026-000623" carries asset "AST-2026-000623" and the floor of that asset is approved
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-30 and R-DIS-31
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Allocate the asset to an auction vendor by distance (legacy RWB-E4-023 AC1)
    Given the rwb-source-data contract mock returns the asset fact of "AST-2026-000623" with its type and the scorecard predicted price of each vendor
    Given the rwb-partner contract mock returns the four vendors of the panel with their capacity and their panel status
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then picks one of the four vendors by distance and capacity, as the current rule does
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-30 (legacy RWB-E4-023 AC2)
    Given the rwb-case contract mock returns the case state "FLOOR_APPROVED" for "RC-2026-000623"
    Given the rwb-source-data contract mock returns the scorecard predicted price of each vendor of the panel
    Given a case in state FLOOR_APPROVED
    When vendor required
    Then allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance
    Then the case moves to VENDOR_ALLOCATED

  Scenario: AC3 Rule R-DIS-31 (legacy RWB-E4-023 AC3)
    Given the rwb-case contract mock returns the case state "VENDOR_ALLOCATED" for "RC-2026-000623"
    Given the rwb-partner contract mock returns the allocated vendor with capacity N and the remaining three vendors of the panel available
    Given a case in state VENDOR_ALLOCATED
    When vendor unavailable
    Then re-allocate to the next vendor on the scorecard
    Then the case moves to VENDOR_ALLOCATED

  Scenario: AC4 Not recorded (legacy RWB-E4-023 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E4-023 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the legacy wording of `the action is taken`, `its trigger arrives`, `vendor required` and `vendor unavailable` all stand. The cross-service parts are mocked, so AC1, AC2 and AC3 each carry one or two `Given the rwb-source-data contract mock returns <x>`, `Given the rwb-partner contract mock returns <x>` or `Given the rwb-case contract mock returns <x>` lines, and those added lines are the only additions to the legacy text. Three notes are recorded rather than smoothed over. AC1 says the Workbench "picks one of the four vendors by distance and capacity, as the current rule does", while AC2 and R-DIS-30 allocate on the scorecard price "not by distance": both statements are kept, the rule decides, and the distance and the capacity remain inputs of the rule (GAP-2900; ASM-4797). AC3 says the case "moves to VENDOR_ALLOCATED" from `VENDOR_ALLOCATED`, which is the re-allocation the rule row gives as a self-transition, so the move is answered and no new state is invented. AC4 names the decision log, which in the target is the local decision record written through RWB-PLT-E1027-CON before the move, relayed to the central ledger by the library (DP-03).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-30 | Asset disposal | D8.1 to D8.3 | FLOOR_APPROVED | VENDOR_REQUIRED | asset_type = vehicle | Allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance | VENDOR_ALLOCATED | Auction and remarketing vendor | Rules component, Partner Portal | 2 working days |
| R-DIS-31 | Asset disposal | D8.1 to D8.3 | VENDOR_ALLOCATED | VENDOR_UNAVAILABLE | vendor_capacity = N or panel_status = suspended | Re-allocate to the next vendor on the scorecard | VENDOR_ALLOCATED | Partner and agency manager | Rules component, Partner Portal | None |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case moves to `VENDOR_ALLOCATED` are written by rwb-case on this story's answer, the decision record is written here, the rule rows and their version are governed in rwb-decision, and the panel facts of the condition and of the scorecard are rwb-partner's and rwb-source-data's.

| ID | Rule | Source |
|---|---|---|
| BR1 | The allocation outcome is this service's: the chosen vendor, the basis, the score and the case move are facts of the decision record written in `rwb_asset`, and no other service writes them; no `asset_sale` and no `listing` row changes on this step | TSD S5 T3.1; GAP-2902; ASM-4800 |
| BR2 | The decision is recorded before the move leaves the service, one record per rule outcome, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; legacy RWB-E4-023 AC1 and AC4 |
| BR3 | The panel stays with rwb-partner: the four vendors, `vendor_capacity`, `panel_status` and the distance are read on the partner activity of queue `rwb-partner` and are never written or recomputed here | Architecture v5 slide 13 (S5→S9 Temporal; route services reach shared capabilities through Temporal, never REST); GAP-2901 |
| BR4 | The case move is answered and not written: `recovery_case`, `assignment` and the states `FLOOR_APPROVED` and `VENDOR_ALLOCATED` are rwb-case's, and this story sends the move with the rule and its version | Ownership rows of S5 (two tables, `asset_sale` and `listing`); GAP-2901 |
| BR5 | The allocation is a decision-record fact: the target keeps no vendor, distance or allocation column, so nothing is invented as a column of this service | GAP-2902; ASM-4800 |
| BR6 | The ACE asset and scorecard facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes both facts on the owner's data-product contract only, with its freshness stamp | DP-05; VR-S5-014-1 |
| BR7 | The basis is the rule's: R-DIS-30 and R-DIS-31 allocate on the scorecard predicted price, and the distance and capacity of FEAT-AST-14 are rule inputs read with their version and never a second selection path in code | GAP-2900; ASM-4797 |
| BR8 | No event is published and none is consumed by this step: `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` only, and the two triggers are signals of the DISPOSAL machine | Architecture v5 slide 19 OUT; TSD S5 T5.3 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset`; the case reference, the asset reference and the vendor reference are identifiers of other services' facts | DP-01; TSD S5 T3.3 |
| BR10 | Every value a business person may change is reference data or a rule row read with its version: the capacity flags, the panel statuses, the panel size and the score rows | TSD S5 T3.2; FSD S5 A2.14.3.1 VR-S5-014-1 and BR-S5-014; legacy Guardrails |
| BR11 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story owns is the state of the allocation step and the decision it records.

| From (case, answered) | Event | Condition | To |
|---|---|---|---|
| `FLOOR_APPROVED` | `VENDOR_REQUIRED` under R-DIS-30 | `asset_type = vehicle`; at least one vendor of the panel is available | `VENDOR_ALLOCATED`, with the highest predicted price |
| `FLOOR_APPROVED` | `VENDOR_REQUIRED` under R-DIS-30 | `asset_type` is not a vehicle | Unchanged; the rule does not fire and no allocation is made (X8) |
| `VENDOR_ALLOCATED` | `VENDOR_UNAVAILABLE` under R-DIS-31 | `vendor_capacity = N` or `panel_status = suspended` | `VENDOR_ALLOCATED`, with the next vendor on the scorecard |
| `VENDOR_ALLOCATED` | `VENDOR_UNAVAILABLE` under R-DIS-31 | Every vendor of the panel is unavailable | Unchanged; the panel is reported and nothing is written (X6) |
| Any | The same signal again | X7 | Unchanged; the repeat is counted |
| Any | A state the rule does not expect | X3 | Unchanged; no record and no answer |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A `VENDOR_REQUIRED` or `VENDOR_UNAVAILABLE` signal forwarded by the parent | The package in force is loaded | Reading |
| Reading | The asset fact, the panel and the scores answer | All three inside 2 s and the product is fresh | Evaluating |
| Evaluating | The rule fires | The decision record is written | Answered |
| Answered | The record and the case-move answer commit | The transaction commits | Waiting for the next signal |
| Reading or Evaluating | A read fails, the product is stale or the record write fails | X1, X4, X5 | Waiting, nothing changed |

The route states `FLOOR_APPROVED` and `VENDOR_ALLOCATED` are those of the DISPOSAL machine and of the legacy criteria, and they live on the case of record. The target declares no allocation state of its own, because no table of this service holds one (GAP-2902; ASM-4800).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal C in the legacy permission table, and the using role of the feature: reads the allocation and may act on the correction paths of the sibling stories |
| RW-ENFORCE, RW-NPAMGR | Asset and disposal C: read the allocation and act where the enforcement or NPA desk owns the asset |
| SY-DATALOAD | Asset and disposal C for the data-load identity; the step itself runs under the service identity |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| RW-PRODHEAD | Asset and disposal RA where a route or a floor needs an approval; no approval is taken on this step |
| PT-AUCTION, PT-RAMC | Asset and disposal RU where the auction vendor or the asset manager acts: both appear as members of the panel, which is rwb-partner's, and no operation of this step is theirs |
| SY-CASEWF, SY-RULES, SY-AGENT | Asset and disposal R or C as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-asset service identity | Runs the branch, reads the asset, the panel and the scores on the owners' contracts, evaluates the two rules, writes the decision records and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs unattended as the FSD gives it ("None; runs unattended", FSD S5 A2.14.3.3), with the sale officer as the primary person role when a person does read or correct, and the 30 read roles of the legacy table are not narrowed. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | Rule id, rule version, inputs reference, chosen vendor reference, basis, score, outcome and decided-at | Write through the local library, one record per rule outcome, before the case-move answer |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table: the case state and its reference arrive on the rwb-case contract |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not read and not written: the vendor task, where one is raised, is created by rwb-case on the stage answer |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read: this service holds no `v_ace_*` grant; taken on the rwb-source-data data product |
| DF-ACE-270 to DF-ACE-279 | `v_ace_score` (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Not read: taken on the rwb-source-data data product, with its version |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read and not written: the rule rows are governed in rwb-decision and loaded with the package |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Not written on this step: the listing is created and priced by the pricing and listing story |
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price and 5 more | Not written on this step: the sale record is the sale story's |
| Not specified in the source documents (GAP-2901; ASM-4799) | vendor panel (S9) | The four vendors, each with its capacity flag, its panel status and its distance to the asset | Read on the rwb-partner activity, never as a table |
| Not specified in the source documents (GAP-2902; ASM-4800) | allocation (S5) | The vendor reference, the basis and the distance, where a column must hold them | Held as facts of the decision record; no column is named by any source |

Field IDs are those of the TSD S5 Assets and auction v2 T3.1 and the Logical Data Model and Data Dictionary v9, and the case, assignment, ACE, decision and rule rows are the rows the legacy story lists in its Data table, with their owners changed by the target. **No new table, no new column and no migration**: `asset_sale` and `listing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_asset` by the library's own migration (DP-03).

**No personal data.** The rows this story writes carry identifiers, codes, a score, a basis and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the decision record, a log, an event payload or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes are declared by RWB-S5-E4023-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its allocation, the chosen vendor and the basis (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The step itself adds no REST operation: its surface is the two triggers of the DISPOSAL machine and the case-move answer. `POST /assets/{assetId}/listings` (API-S5-004) is the legacy endpoint row of this key and belongs to the listing and pricing baseline of this service, because the allocation step creates no listing; `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under ASM-0043. The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter, and 503 when the decision library or a consumed contract does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the case state `FLOOR_APPROVED` or `VENDOR_ALLOCATED` the rule checks before it fires; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2901; ASM-4798)) | rwb-case (P3) | P3 rwb-case | The answer that carries `VENDOR_ALLOCATED` with the rule, the vendor reference and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The read of the asset and scorecard data product (operation name Not specified in the source documents (GAP-2901; ASM-4798)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset fact (`v_ace_npa_asset`) and the scorecard predicted price of each vendor (`v_ace_score`), with the freshness stamp; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2901 with ASM-4798. The vendor panel is not a REST row: the connection matrix gives S5→S9 a Temporal call and no REST, so it is declared in 12.5.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` (EV-22) and `AssetSold`. `AssetTakenOn` is published by the take-on story when the asset record opens and `AssetSold` by the sale story when the sale completes; this step publishes nothing, writes no outbox row and adds no event to `rwb.asset.events.v1`. A build that publishes an event here fails the absence test.

#### 12.4 Events consumed

None. The two triggers are signals of the DISPOSAL machine that the parent `CaseWorkflow` forwards to the asset disposal child at `FLOOR_APPROVED` and `VENDOR_ALLOCATED`; no source gives this step a Kafka event, and the four events Architecture v5 slide 19 IN gives rwb-asset (`JudgmentRecorded`, `AuctionResult`, `ProceedsMatched`, `PartnerResultSubmitted`) serve the litigation, auction, proceeds and partner-result steps and none of them is the vendor-required or vendor-unavailable signal. DP-09 is therefore held as a prohibition for this step and no consumer group and no inbox row are registered (GAP-2901; ASM-4798).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new across the years of the holding | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference and the rule package in force; signals: `VENDOR_REQUIRED`, `VENDOR_UNAVAILABLE`, the case state answered by rwb-case and the rule package in force |
| `allocateVendor` | Activity, the vendor-allocation step of this story | `rwb-asset` | The case and the asset reference in; the chosen vendor, the basis, the score, the rule IDs with their package versions and the case move out, with the decision records written in the same transaction |
| The rwb-partner vendor-panel activity (name Not specified in the source documents (GAP-2901; ASM-4799)) | Activity on the owner's queue, called by this step | `rwb-partner` | The asset reference, its region and its type in; the four vendors with their capacity flag, their panel status and their distance out; one call per evaluation, no child workflow and no Nexus |

No child workflow for the case and no workflow for the panel exists in this service. The activity names are target design choices of this story and are fixed by no source document; the trigger is read as the two DISPOSAL events because the legacy criteria name `vendor required` and `vendor unavailable` and the FSD declares no background event (FSD S5 A2.14.2, A2.14.4.4).

#### 12.6 Schedules

None. The step runs from the signals the parent forwards and owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to the re-appraisal story of this service (Architecture v5 slide 44). No other job is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record, one per rule outcome, holding the chosen vendor, the basis and the score (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated signal and the answer it holds |

Not owned and never read as a table: `recovery_case` and `assignment` (P3), `decision_log_entry` and `rule_row` (P7), `proceeds` (P8), the vendor panel (S9), every `v_ace_*` view (P1), and `asset_sale` and `listing`, which are this service's but are not changed by this step. No foreign key leaves the schema and the case reference is an identifier, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data asset and score data-product fake | The asset `AST-2026-000623` with its type, transfer-in type and book value and the scorecard predicted price of each vendor of the panel; a stale product with its date; no answer beyond 2 s | AC1, AC2, AC3, X4, X5 |
| rwb-partner vendor-panel fake | The four vendors with their capacity flag, their panel status and their distance; the allocated vendor with capacity N; a panel where every vendor is unavailable; an activity that fails | AC1, AC3, X4, X6 |
| rwb-case case-state fake | The case state `FLOOR_APPROVED` and `VENDOR_ALLOCATED` of case `RC-2026-000623`; a case in another state | AC2, AC3, X3 |
| rwb-case case-move fake | The move `VENDOR_ALLOCATED` accepted, including the self-transition of the re-allocation; a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-30 and R-DIS-31 and the panel and capacity reference rows | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000623`, with the asset and its allocation read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The names of the rwb-source-data data product, of the partner activity and of the case-move answer are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2901; ASM-4798, ASM-4799).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two reads of the asset on `/api/recovery/asset/v1`; the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | Nothing on `rwb.asset.events.v1` and no consumer group; the two triggers are workflow signals |
| Temporal | 1 workflow, 1 owned activity, 1 partner activity | `AssetDisposalWorkflow` and `allocateVendor` on `rwb-asset`; the rwb-partner vendor-panel activity on `rwb-partner`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `allocation`, Java package `th.co.scb.ace.workbench.recovery.asset.allocation`; front end `src/modules/recovery/asset/AssetAllocation.tsx`, the fragment SCR-23 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the asset and scorecard facts are the ones the rwb-source-data contract answers. DP-03 is the transaction rule of the step: each record commits with the answer it authorises or not at all, and the case-move answer leaves only after the record is written. DP-13 moves the base of the two reads and nothing else. DP-19 is how SCR-21 and SCR-23 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The three consumed rows and the partner activity are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2901. DP-09 and DP-10 stay prohibitions: no event and no Schedule (ASM-4798).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` vendor branch | Workflow | The branch of the journey that waits for `VENDOR_REQUIRED` or `VENDOR_UNAVAILABLE`, loads the package in force and reports the outcome to the parent |
| `allocateVendor` | Activity | The one step: read the asset, the panel and the scores, evaluate R-DIS-30, write the record and answer the move |
| `VendorAllocationEvaluator` | Service | The R-DIS-30 evaluation on the asset type and the scorecard predicted price of each available vendor |
| `VendorReallocationEvaluator` | Service | The R-DIS-31 evaluation on the capacity flag and the panel status of the allocated vendor, and the next vendor of the scorecard |
| `AssetDecisionRecordWriter` | Library adapter | Writes one decision record per rule outcome before any answer, hash-linked, and refuses the step when the write fails (DP-03) |
| `CaseMoveAnswer` | Client | Answers rwb-case with `VENDOR_ALLOCATED`, the rule and the vendor reference, one hop, 2 s |
| `CaseStateClient` | Client | The case state read of rwb-case, one hop, 2 s |
| `SourceDataProductClient` | Client | The asset and scorecard data-product read of rwb-source-data, one hop, 2 s, with the freshness stamp |
| `PartnerPanelClient` | Temporal client | Calls the rwb-partner vendor-panel activity on queue `rwb-partner` and maps its answer to the rule inputs |
| `AssetController` | Controller | The two reads, the capability area and right, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 |
| `AssetAllocation` | React component | Shows the asset, the chosen vendor and the basis on SCR-23, read only, with the refusal and hold states |

**Database and migrations.** No Flyway file. `asset_sale` and `listing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No column is added for the vendor, the basis or the distance: where no source names one, the value is held as a decision-record fact and raised as GAP-2902 rather than invented.

**Configuration and reference data.**

- The four-vendor panel, the capacity flags, the panel statuses and the panel size at their version in force (FEAT-PRM-03), read as reference data and never as constants.
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the selection basis and the score rules are values of the package and not of this build.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the Temporal activity timeout are the platform rules of ADR-020 and the workflow kit.
- No parameter is named in the sources for the step itself.

**Build steps**

1. The vendor branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset`, with the two signals as its triggers.
2. `CaseStateClient` and `SourceDataProductClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, AC2, X4, X5).
3. `PartnerPanelClient` and the partner activity fake, with the available, the suspended, the at-capacity and the failed-call paths (AC1, AC3, X4, X6).
4. `VendorAllocationEvaluator` over the DISPOSAL package with R-DIS-30, the vehicle path and the no-fire path (AC2, X3, X8).
5. `AssetDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `VendorReallocationEvaluator` and R-DIS-31, with the self-transition, the exhausted panel and the repeat (AC3, X6, X7).
7. `CaseMoveAnswer` and the parent signal, with the move and its refusal (AC2, AC3).
8. `AssetController` with the rights, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 (AC1).
9. `AssetAllocation` and the two screens through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_partner`, no outbox row and no consumer group (X9, BR3, BR6).

**Feature flag.** `rwb.asset.vendor-allocation-v1`, read as a flag of the platform library; off means the branch holds the signal, writes no record and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic `VENDOR_REQUIRED` and `VENDOR_UNAVAILABLE` in SIT, each rule produces its record and its move, an exhausted panel writes nothing, a repeated signal writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-23 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| VR-S5-014-1 | The ACE data product of the case is stale after a late or failed batch for its source (`v_ace_batch_status`) (X5) | MSG-P1-001 {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-001 | Raised by VR-S5-014-1 on the stale data product: the step holds and writes nothing | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's values, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or of a data-product fact is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset list or the asset, or attempts the step (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the move leaves the service (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The message IDs are those of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged; no message is reworded and no new text is added. VR-S5-014-1 is the validation rule row of FSD S5 A2.14.3.1 and raises the platform message MSG-P1-001 that the same row names.

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-23 Listing and price in its draft, below-limit, approved and published states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset and its allocation and rwb-case for the case and its route state; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

This step produces no one of the four SCR-23 states: the draft, below-limit, approved and published states are the pricing and listing story's, and the floor approval that precedes the allocation is the route approval of rwb-case. What the step adds to the screen is the allocation fragment — the chosen vendor, the basis and the score of the rule outcome — read from the decision record, plus the states it can show: held while the data product is stale (MSG-P1-001), refused (MSG-P4-002), not recorded (MSG-P7-003) and panel exhausted.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-023-01 | AC1 | Integration | Case `RC-2026-000623` at `FLOOR_APPROVED` with the asset and score facts from rwb-source-data and the panel from rwb-partner; the allocation record and the move asserted end to end on the fakes |
| TC-E4-023-02 | AC2 | Component | Case at `FLOOR_APPROVED` with a vehicle asset and four vendors whose predicted prices differ; the R-DIS-30 record, the chosen vendor and the `VENDOR_ALLOCATED` answer asserted |
| TC-E4-023-03 | AC3 | Component | Case at `VENDOR_ALLOCATED` with the allocated vendor at capacity N; the R-DIS-31 record, the next vendor and the self-transition asserted |
| TC-E4-023-04 | AC4 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E4-023-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E4-023-06 | Principle 5 | Component | A forced decision log write failure at the moment of the allocation; no record and no move answered |

The six legacy cases are the legacy cases of RWB-E4-023 in their legacy order, with the Level column added: TC-E4-023-01 maps to `Integration` because it crosses the rwb-source-data and rwb-partner boundaries, and the other five map to `Component` where the step is tested on its fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the panel size, the capacity flags, the panel statuses, the score rules and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in a workflow input, in a decision record or in a log: identifiers, codes, a score, a basis, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The panel stays with rwb-partner and the case with rwb-case: no vendor, capacity or panel status is stored or recomputed here, and no `recovery_case` or `assignment` row is written.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base, topic or queue as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no consumed event and no `v_ace_*` read.
- The decision is recorded before the move and a repeated signal writes once; a build that answers a move before its record fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice and no requirement of the module names vendor allocation; the requirement is FEAT-AST-14 of the FSD S5 A2.14, that one of the four vendors is chosen by the rule so that the NPA sales cycle shortens (GAP-2903; ASM-4801) | The allocation step, the decision record and the case move | TC-E4-023-01, TC-E4-023-02, TC-E4-023-03 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the allocation outcome | TC-E4-023-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E4-023-06 |
| ADR-016 | Reusable Temporal layer | The vendor branch of `AssetDisposalWorkflow` and the partner activity | TC-E4-023-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed REST rows with their budget | TC-E4-023-01 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the move, one per rule outcome | TC-E4-023-04, TC-E4-023-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-023, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E4-023-01 to TC-E4-023-06 |
| Feature and screens | FEAT-AST-14, SCR-23 Listing and price and SCR-21 Asset list |
| Rules | R-DIS-30 and R-DIS-31, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two reads, the consumed rows, the workflow signal elements, the case-move answer, the decision-record element, the error set and the fakes: RWB-S5-E4023-CON.
- The start price, the floor price, the floor approval and the listing: the pricing, listing and approval stories of this service, API-S5-004.
- The auction rounds, the bids, the award and the payment term: the auction story of this service, API-S5-005.
- The vendor panel, its capacity, its panel status, its distance and the partner instruction: rwb-partner (S9) (GAP-2901; ASM-4799).
- The asset and scorecard facts of ACE and the freshness of the data product: rwb-source-data (P1).
- The case of record, the states `FLOOR_APPROVED` and `VENDOR_ALLOCATED`, `assignment`, and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version and its approval: rwb-decision (P7).
- The parameter and reference-data rows of FEAT-PRM-03: their owners under the default ruling, read with their version.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

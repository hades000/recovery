# RWB-S5-E4032-APP Arrange a customer buy-back

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-X |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S5-E4032-APP-16) |
| Depends on (build) | RWB-S5-E4032-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (REQ-S5-010) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 23 November 2026: the application slice of legacy RWB-E4-032 split out for rwb-asset. The three legacy acceptance criteria are kept word for word with their origin tag; the buy-back becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset` that opens the buy-back `listing` and the `asset_sale` terms in `rwb_asset` at the template price once the approval the limit requires is given (R-DIS-24), writes the local decision record before any row changes (DP03), evaluates R-DIS-66 on a raised deviation and calls rwb-deviation instead of writing the `deviation` table, answers the moves `ROUTE_APPROVED_BUYBACK` and `DISPOSAL_PAUSED_DEVIATION` to rwb-case, and publishes no event of its own. The base becomes `/api/recovery/asset/v1` (DP13) and SCR-21 and SCR-22 read through the gateway-bff composite route (DP19); the legacy `v_ace_customer` and `v_ace_npa_sale` reads are retired as service reads, the former owner arriving as a party key of the owner's contract only (DP05). No source publishes the operation names of the rwb-deviation raise, of the rwb-case answer or of the rwb-decision approval, and none gives a limit value or the field that holds the template price (GAP-2960; ASM-4857). Legacy AC1 gives no from state while R-DIS-24 starts at `ROUTE_WITH_APPROVER`, and the FSD lists only R-DIS-66 among the rules of FEAT-AST-23 while the rule set gives the buy-back route R-DIS-24 (GAP-2962, GAP-2963; ASM-4859). The FSD also-user "Customer (borrower)" has no row in the rights matrix (GAP-2964; ASM-4861). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4032-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 21 cross-document, 7 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **to open the buy-back where the former owner repurchases, with the approval the limit requires**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E4-032. It owns:

- AC1 to AC3 of the legacy story, copied word for word, and the rules, messages and screens they use;
- one buy-back step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, the stage child that `CaseWorkflow` starts on rwb-case (Temporal and Drools Design slide 13; context pack, "Workflows (1)");
- the evaluation of R-DIS-24 (`route = buy_back` and `second_signature given`) and of R-DIS-66, with the DISPOSAL package version in force;
- the buy-back `listing` row and the `asset_sale` terms in schema `rwb_asset`, in the columns DF-SAL-001 to DF-SAL-019 and no new column;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the rows change (DP03);
- the call that raises the deviation in rwb-deviation and the answer to rwb-case for the two case moves;
- the two reads behind SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP13, DP19);
- no event of its own: `rwb.asset.events.v1` carries `AssetTakenOn` (RWB-S5-E3019-APP) and `AssetSold` (RWB-S5-E4030-APP), and neither comes from this step.

It does not own: the published shape of the two reads, the buy-back element and its closed lists, the consumed rows, the decision-record element, the error set and the fakes, which are RWB-S5-E4032-CON; the case and its route states, which are rwb-case's; the approval, its limit and its answer, which are rwb-decision's and rwb-access's; the deviation record, its pause and its return, which are rwb-deviation's; the template and its price, which are rwb-comms'; the former owner and the ACE NPA facts, which are rwb-source-data's; the money, the buy-back signature and its funding (R-DIS-61, R-DIS-62), which are rwb-payment's and RWB-S5-E4030-APP's; and the schema build and the deployment, which are the DB and OPS stories of this legacy key.

### 2. Business rationale

Legacy RWB-E4-032 gave the Workbench the step that opens a buy-back: the former owner repurchases the asset the bank took on, at the price the governed template carries, once the approver the delegated limit names has signed. The FSD keeps the feature as FEAT-AST-23 "Arrange a customer buy-back" in module S5, with the sale officer acting and the approval the limit requires as its condition (FSD S5 A2.23.1, A2.23.2). The program keeps the requirement: REQ-S5-010, "A transfer to the asset management company, a buy-back and a rental each follow a recorded approval" (Business Requirements Program v5). The objective of the module is unchanged, "assets sell sooner at approved prices", and the metric stays the NPA sales cycle on the decision log and the Workbench records, reviewed monthly, from 1,486 days to a target of 1,095 days (FSD S5 A2.23.1).

What D-RCV-60 changes is who owns the listing, the terms, the case, the approval and the deviation.

- **The buy-back listing and its terms are this service's.** `listing` and `asset_sale` are S5's tables in `rwb_asset` (context pack, "Tables owned by S5"; TSD S5 T3.1). The buy-back is opened as a listing of the asset with its price and as the sale terms of that listing, and no other service writes either row. Which of the two rows holds the template price, and whether a third row is needed, no source settles (GAP-2960; ASM-4857).
- **The case of record stays with rwb-case (P3).** `recovery_case`, `assignment`, `task` and `timer` are P3's, and the four route states of this step live there. This story evaluates the rules, writes the listing and the terms, records the decision and **answers** the case moves; the answer's operation name is not published (GAP-2960; ASM-4857).
- **The approval stays with rwb-decision (P7).** R-DIS-24 makes `second_signature given` the condition; the signature is the approval child workflow of the kit on rwb-decision, and the limit behind it is a delegated-authority row of rwb-access (P4) read at its version (Temporal and Drools Design slide 12, "Approval (DoA)"). No source gives a limit value and this story writes none (GAP-2960; ASM-4860).
- **The deviation stays with rwb-deviation (S8).** AC2 is R-DIS-66: on `DEVIATION_RAISED` in `ASSET_HELD`, with a deviation open in X1, X2, X3, X4, X5 or X7, the disposal is paused, contact stops where required and the case routes to the deviation owner. `deviation` is S8's table and `DeviationWorkflow` is S8's workflow, which can start at any time and pauses the stage clock. This story therefore calls the raise and never writes the record.
- **The template stays with rwb-comms (P6).** `template` is P6's and the governed template price of R-DIS-24 and R-DIS-61 is read from it, never copied into a constant of this build.
- **The party facts stay with rwb-source-data (P1).** The legacy data table names `v_ace_customer` and `v_ace_npa_sale`; in the target only rwb-source-data reads the `recovery.v_ace_*` views, so DP05 applies as a **prohibition**: the former owner enters this step as a party key the owner's contract answers, and no name, address or identity number enters `rwb_asset`.
- **Nothing is published.** `rwb.asset.events.v1` carries two events and neither is this step's, so the buy-back writes no outbox row; the absence is stated in §12.3.

Two source defects are recorded and not invented away: legacy AC1 gives no from state while R-DIS-24 starts at `ROUTE_WITH_APPROVER` (GAP-2962; ASM-4859), and the FSD rule list of A2.23 omits R-DIS-24, which the rule set assigns to the buy-back route (GAP-2963; ASM-4859).

### 3. Preconditions

- RWB-S5-E4032-CON is published: the two reads, the buy-back element and its closed lists, the consumed rows, the decision-record element, the error set and the fakes are baselined and tagged.
- `asset`, `listing` and `asset_sale` exist in schema `rwb_asset` from the DB story of S5, with the columns of TSD S5 T3.1 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration.
- The case state is readable on the rwb-case fake (`GET /api/recovery/case/v1/cases/{caseId}`), and the case-move answer is answered by the same fake. The published name of a case-move operation is Not specified in the source documents (GAP-2960; ASM-4857).
- The rwb-deviation raise is answered by its fake with the deviation reference and the accepted pause; its operation name is Not specified in the source documents (GAP-2960; ASM-4857).
- The approval the limit requires is answered by the approval-child fake on rwb-decision, with an approved and a refused answer; its element names are Not specified in the source documents (GAP-2960; ASM-4860).
- The template price is read from rwb-comms at its version. No source publishes the read operation or names the price field (GAP-2960; ASM-4857).
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each (DP19).
- The DISPOSAL rule package is in force at its version with R-DIS-24 and R-DIS-66; the package is authored, tested and approved in rwb-decision and loaded here on the package-in-force signal.
- The service runs as its own login on `rwb_asset`: it holds no grant on another `rwb_*` schema, no grant on `rwb_deviation` and no `v_ace_*` grant, so a statement on `recovery_case`, on `deviation` or on a `v_ace_*` view is refused by the database (DP05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E4032-CON when its tests pass.

### 4. Flow

| # | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens SCR-22 Asset record for a case the rwb-case mock returns in `ROUTE_WITH_APPROVER` and chooses the buy-back route | The composite route reads `GET /api/recovery/asset/v1/assets/{assetId}`; the case id and the state come from the rwb-case fake |
| 2 | Workbench | Signals the buy-back step of `AssetDisposalWorkflow` on `rwb-asset` | The step reads the DISPOSAL package version in force and the template version |
| 3 | Workbench | Asks the approval child on rwb-decision for the signature the limit requires | The answer carries approved or refused and the approver role; no limit value is held here |
| 4 | Workbench | Records the decision through the local decision-record library | The row carries case, asset, rule ID R-DIS-24, rule version and template version (DP03) |
| 5 | Workbench | In one transaction writes the `listing` row of the buy-back and the `asset_sale` terms at the template price | Commit or roll back together with step 4; a failed record stops the action with MSG-P7-003 |
| 6 | Workbench | Answers the case move `ROUTE_APPROVED_BUYBACK` to rwb-case | The parent `CaseWorkflow` applies the move; no `recovery_case` row is written here |
| 7 | Workbench | On `DEVIATION_RAISED`, evaluates R-DIS-66 against the open deviation codes read from the rwb-deviation fake | If X1, X2, X3, X4, X5 or X7 is open: records the decision, calls the raise, holds the step and answers `DISPOSAL_PAUSED_DEVIATION` |
| 8 | Workbench | Waits on its durable timer or the next signal | The return (R-DIS-68) is rwb-deviation's and rwb-case's; the step resumes where it paused and re-evaluates |

The two writes of step 5 happen only on an approved answer and a healthy decision record; the step is idempotent on case id, rule version and template version, so a repeated signal writes no second listing.

### 5. Exception paths

| Condition | What happens | Message or answer | Owner of the fix | Covered by |
|---|---|---|---|---|
| The decision record cannot be written | Nothing changes: no listing, no terms and no case move | MSG-P7-003 to the user | This story (AC3) | AC3 |
| The user's role lacks the right | The call is refused before the service is reached | MSG-P4-002 | Edge and the rights matrix | None (edge rights check) |
| `second_signature given` is false | R-DIS-24 does not fire; the step keeps waiting, nothing is written | None | rwb-decision (approval) | None |
| The approver refuses | The route refusal is R-DIS-27 and belongs to the route-approval slice; this step writes nothing and ends | MSG-P4-002 only where the role also lacks the right | RWB-S5-E3027-APP (route recommendation) | None (other slice) |
| The template price cannot be read | The step holds and retries; no row is written and no case move is answered | No business message is published for it (GAP-2960; ASM-4857) | rwb-comms and this story | None |
| The deviation raise is unavailable | The step holds, raises an incident and does not answer the pause until the raise is accepted | None published (GAP-2960; ASM-4857) | rwb-deviation | None |
| The asset is not in `ROUTE_WITH_APPROVER` | The rule does not fire; the step rejects the signal and records the reason | None | This story; the from state is a source defect (GAP-2962; ASM-4859) | None |
| The same signal arrives twice | The second run finds the listing of the same case, rule version and template version and writes nothing | None | This story (AC5) | AC5 |
| A `v_ace_*` view or another owner's table is queried | The database refuses the statement; the boundary test fails the build | None | This story (AC4) | AC4 |

### 6. INVEST check

| Letter | Result | Evidence |
|---|---|---|
| Independent | Yes | Builds against RWB-S5-E4032-CON, RWB-PLT-E1027-CON and RWB-PLT-N001-CON only; no C, I or X dependency. |
| Negotiable | Yes | The operation names and the price field are open (GAP-2960); the two source defects are recorded, not decided here. |
| Valuable | Yes | REQ-S5-010 and the module metric, NPA sales cycle from 1,486 to 1,095 days. |
| Estimable | Yes | One workflow step, two owned tables, one record call, two consumed answers, two reads. |
| Small | Yes | One step of one stage workflow; the approval, the deviation, the case and the money stay with their owners. |
| Testable | Yes | Five acceptance criteria and seven test cases, four of them at component level against the fakes. |

### 7. Acceptance criteria

Rule R-DIS-24 is the rule of the buy-back step: route = buy_back and second_signature given, agreeing the terms at the template price (source: Business Rules and Routing Logic v4; TSD S5 T4). The customer (borrower) is a party of the case and not a Workbench role; this slice grants no right to it, and the portal question is recorded with the P4 and S9 owners (GAP-2964).

```gherkin
Feature: Arrange a customer buy-back

  Scenario: AC1 Arrange a customer buy-back (legacy RWB-E4-032 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns the case in ROUTE_WITH_APPROVER and the rwb-decision contract mock returns the approval granted with its limit
    When the user acts on the screen
    Then opens the buy-back where the former owner repurchases, with the approval the limit requires
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-66 (legacy RWB-E4-032 AC2)
    Given a case in state ASSET_HELD
    Given the rwb-deviation contract mock returns the deviation raised for X1, X2, X3, X4, X5, X7
    When deviation raised
    Then pause the disposal, stop contact where required and route to the deviation owner
    Then the case moves to DISPOSAL_PAUSED_DEVIATION

  Scenario: AC3 Not recorded (legacy RWB-E4-032 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 Boundary held (new, D-RCV-60)
    Given the buy-back step has run to its commit on the rwb-case, rwb-deviation, rwb-decision and rwb-comms fakes
    When the schema grants and the topic of the service are inspected
    Then no statement touches recovery_case, deviation or a v_ace_* view and no outbox row is written
    Then the only rows written are listing and asset_sale in rwb_asset

  Scenario: AC5 One buy-back per case, rule version and template version (new, D-RCV-60)
    Given a buy-back step that already committed its listing and terms
    When the same signal is delivered a second time with the same rule version and template version
    Then no second listing row and no second asset_sale row is written and the recorded decision is unchanged

  Scenario: AC6 Provided operations answer 401, 403 and 404 (new, D-RCV-60)
    Given the provided operations of rwb-asset are exposed through the gateway
    When a call arrives without a valid identity, from a role without the right on the operation, or for an asset or case that does not exist
    Then the operation answers 401, 403 or 404 respectively and writes no row

  Scenario: AC7 Activity retry and timeout (new, D-RCV-60)
    Given an activity of AssetDisposalWorkflow fails or runs past its timeout
    When the activity is retried
    Then the retry runs under the retry and timeout settings of the activity and no listing row or asset_sale row is written twice (AC5)

  Scenario: AC8 Consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed call to rwb-deviation, rwb-case or rwb-decision fails or does not answer
    When the buy-back step makes that call
    Then the step stops, nothing is committed and no row in rwb_asset changes

  Scenario: AC9 Disallowed status change is refused (new, D-RCV-60)
    Given the case is in a status the state model does not allow for the buy-back
    When the buy-back step attempts the status change
    Then the change is refused and nothing changes
```

### 8. Business rules

| Rule ID | Rule (copied) | From | Event | To | Source | BR ID |
|---|---|---|---|---|---|---|
| R-DIS-24 | Agree the buy-back terms at the template price, when `route = buy_back and second_signature given` | ROUTE_WITH_APPROVER | ROUTE_APPROVED | ROUTE_APPROVED_BUYBACK | Business Rules and Routing Logic v4 | BR-S5-024 |
| R-DIS-66 | Pause the disposal, stop contact where required and route to the deviation owner, when `deviation_open in (X1, X2, X3, X4, X5, X7)` | ASSET_HELD | DEVIATION_RAISED | DISPOSAL_PAUSED_DEVIATION | Business Rules and Routing Logic v4; FSD S5 A2.23.3.1 | BR-S5-025 |
| VR-S5-023-1 | Floor price below the approver's limit → MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. | Declared, not evaluated by this step | None | None | FSD S5 A2.23.3.1 | BR-S5-026 |
| BR-S5-023 | No value a business person may change is written in code; it is read from reference data with its version | Any | Any | None | FSD S5 A2.23.3.1 | BR-S5-023 |
| R-DIS-61 | Complete the buy-back at the governed template price, when `customer_funded = Y` | ROUTE_APPROVED_BUYBACK | BUYBACK_TERMS_SIGNED | SALE_AGREED | Adjacent; RWB-S5-E4030-APP | BR-S5-027 |
| R-DIS-62 | Return the asset to hold and review the route, when `customer_funded = N` | ROUTE_APPROVED_BUYBACK | BUYBACK_FUNDING_FAILED | ASSET_HELD | Adjacent; RWB-S5-E4030-APP | BR-S5-028 |

R-DIS-61 and R-DIS-62 are tabled for context only: they start where this step ends, and neither is evaluated here. The FSD rule list of A2.23 does not carry R-DIS-24 (GAP-2963; ASM-4859). The DISPOSAL package holds 72 rules and this story owns two of them; the other 70 are other slices' and are not listed.

### 9. State transitions

| From | Event | To | Rule | Who holds the state |
|---|---|---|---|---|
| ROUTE_WITH_APPROVER | ROUTE_APPROVED (`route = buy_back`, `second_signature given`) | ROUTE_APPROVED_BUYBACK | R-DIS-24 | rwb-case; this step answers the move |
| ASSET_HELD | DEVIATION_RAISED (`deviation_open` in X1, X2, X3, X4, X5, X7) | DISPOSAL_PAUSED_DEVIATION | R-DIS-66 | rwb-case (state), rwb-deviation (pause and owner) |
| DISPOSAL_PAUSED_DEVIATION | DEVIATION_CLEARED (`deviation_open = none`) | ASSET_HELD (the state it paused in) | R-DIS-68 | rwb-deviation and rwb-case; not this story |
| ROUTE_APPROVED_BUYBACK | BUYBACK_TERMS_SIGNED / BUYBACK_FUNDING_FAILED | SALE_AGREED / ASSET_HELD | R-DIS-61 / R-DIS-62 | RWB-S5-E4030-APP; not this story |

The step itself has no state of its own beyond the workflow run: `listing.status` moves in the closed list LOV-LISTING and `asset.holding_status` in LOV-HOLDING, and neither carries a buy-back value that a source names (GAP-2960; ASM-4857).

### 10. Authority

| Capability area | Right | Roles that hold it | Where declared |
|---|---|---|---|
| Asset and disposal | C (open the buy-back and write its terms) | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD | Contract of RWB-S5-E4032-CON; legacy permission checks of RWB-E4-032; TSD S5 T6.1 |
| Asset and disposal | R (the two reads behind SCR-21 and SCR-22) | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more | TSD S5 T6.1 |
| Delegated authority for the approval limit | Approval | The approver the delegated-authority row names | rwb-access (P4) delegated-authority rows at their version; the approval is the kit's approval child workflow on rwb-decision; no limit value in code, test or fixture (GAP-1923) |

The right is declared on the operation and enforced at the edge; DP08 is not in this slice's pattern set, so the authorise contract of rwb-access is not a build dependency of this story. The FSD also-user "Customer (borrower)" has no row in the rights matrix and is recorded, not granted (GAP-2964; ASM-4861).

### 11. Data

| Entity | Owner | Use here | Fields | Field IDs |
|---|---|---|---|---|
| listing | rwb-asset (S5) | Written: the buy-back listing; sale_channel and status read from LOV-SALE-CHANNEL and LOV-LISTING at their version, buy-back values a placeholder until the reference-data owner publishes them | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | DF-SAL-001 to DF-SAL-008 |
| asset_sale | rwb-asset (S5) | Written: the buy-back terms | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, gain_loss, incentive_amount | DF-SAL-009 to DF-SAL-019 |
| asset | rwb-asset (S5) | Read: holding status, book value and asset type of the listing; holding status is not written by this step | id, asset_type, book_value, holding_status, holding_cost_to_date | DF-COL-028 to DF-COL-042 |
| recovery_case | rwb-case (P3) | Read through the fake; the two moves are answered, never written | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | DF-CAS-001 to DF-CAS-023 |
| assignment | rwb-case (P3) | Read through the fake: who holds the case task | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | DF-WRK-009 to DF-WRK-016 |
| deviation | rwb-deviation (S8) | Called, never written: the open codes, the pause and the owner | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | DF-CAS-036 to DF-CAS-045 |
| decision_log_entry | rwb-decision (P7) | Written through the local decision-record library (DP03) | id, case_id, decision_code, rule_id, rule_version, model_version and 12 more | DF-DEC-001 to DF-DEC-018 |
| v_ace_customer | rwb-source-data (P1) | Not read here (DP05 prohibition); the former owner arrives as a party key | person_key, cif_no, first_name, last_name, date_of_birth, customer_status and 14 more | DF-ACE-055 to DF-ACE-074 |
| v_ace_npa_sale | rwb-source-data (P1) | Not read here (DP05 prohibition) | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee and 5 more | DF-ACE-220 to DF-ACE-230 |

No listing column is added for the buy-back: its eight columns of TSD S5 T3.1 carry it, and the buy-back terms sit on `asset_sale` with `listing_id` set to the buy-back listing, `sale_price` taking the template price with its template version; the price field and its read operation belong to rwb-comms (P6) (GAP-1922). No personal data enters `rwb_asset`; the party key is a reference, not a name.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Right | Purpose | Published by |
|---|---|---|---|---|
| GET | /api/recovery/asset/v1/assets | Asset and disposal R | Asset list behind SCR-21, with age, holding cost and sale status | RWB-S5-E4032-CON (API-S5-001) |
| GET | /api/recovery/asset/v1/assets/{assetId} | Asset and disposal R | Asset record behind SCR-22, with the buy-back listing and its terms | RWB-S5-E4032-CON (API-S5-002) |

The buy-back itself is opened by the workflow and needs no REST write: the legacy endpoint list of RWB-E4-032 names one asset read and one listing write under the old monolith base, and no source names a buy-back operation (GAP-2960; ASM-4857).

#### 12.2 REST operations consumed

| Method | Path or operation | Owner | Use | Timeout |
|---|---|---|---|---|
| GET | /api/recovery/case/v1/cases/{caseId} | rwb-case (P3) | Case state and scope before the step acts | 2 s |
| POST | Case-move answer (operation name Not specified in the source documents (GAP-2960; ASM-4857)) | rwb-case (P3) | Applies `ROUTE_APPROVED_BUYBACK` and `DISPOSAL_PAUSED_DEVIATION` | 2 s |
| POST | Raise deviation, on the rwb-deviation path `POST /cases/{caseId}/deviations`; operation name Not specified in the source documents (GAP-2960; ASM-4857) | rwb-deviation (S8) | Raises the deviation that R-DIS-66 pauses on | 2 s |
| GET | Template price read (operation name Not specified in the source documents (GAP-2960; ASM-4857)) | rwb-comms (P6) | The governed template price of R-DIS-24 | 2 s |

#### 12.3 Events published

None. `rwb.asset.events.v1` carries `AssetTakenOn` (RWB-S5-E3019-APP) and `AssetSold` (RWB-S5-E4030-APP); the buy-back step writes no outbox row. A reporting subscriber therefore learns of the buy-back from the case move and the decision record only, which is stated for rwb-reporting.

#### 12.4 Events consumed

None on the topic. The step is started or signalled through the case router of rwb-case, and a cleared deviation reaches it as the R-DIS-68 resume, which is rwb-deviation's and rwb-case's.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Purpose |
|---|---|---|---|
| AssetDisposalWorkflow | Workflow (stage child) | rwb-asset | Holds the run from take-on to sale; this story adds the buy-back step |
| openBuyBack | Activity of this story | rwb-asset | Validate, evaluate R-DIS-24, write listing and terms, answer the case move |
| EvaluateRules | Activity (kit, L4) | rwb-asset | Runs the DISPOSAL package, R-DIS-24 and R-DIS-66, with the package version |
| RecordAndApply | Activity (kit, L4) | rwb-asset | Record, state and outbox in one transaction; the record is the decision record here |
| requestDeviation | Activity (this story's call) | rwb-deviation | Raises the deviation; name Not specified in the source documents (GAP-2960; ASM-4857) |
| ApprovalWorkflow | Child workflow (kit, L3) | rwb-decision | Maker-checker with the DoA limit as a parameter |
| answerCase | Signal or activity | rwb-case | Delivers the stage outcome to the parent `CaseWorkflow` |

#### 12.6 Schedules

None. No schedule starts this step; it is signalled by the case and by the approval answer.

#### 12.7 Tables owned

| Table | Schema | Written by this story | Owner service |
|---|---|---|---|
| listing | rwb_asset | Yes | rwb-asset |
| asset_sale | rwb_asset | Yes | rwb-asset |
| asset | rwb_asset | No; read only | rwb-asset |

#### 12.8 Contract fakes

| Fake | Covers | Used in |
|---|---|---|
| rwb-case fake | Case read, case-move answer, stage outcome | AC1, AC2, AC5; TC-E4-032-01, -02 |
| rwb-decision fake | Approval child answer (approved, refused) and the decision-record writer | AC1, AC3; TC-E4-032-01, -03, -05 |
| rwb-deviation fake | Open deviation codes and the raise answer | AC2; TC-E4-032-02 |
| rwb-comms fake | Template price at a version | AC1, AC5; TC-E4-032-01 |
| gateway-bff fake | Composite route for SCR-21 and SCR-22 | AC4; TC-S5-E4032-APP-01 |

#### 12.9 Call-type summary

| Call type | Out | In |
|---|---|---|
| REST | 4 consumed (case read, case-move answer, deviation raise, template price) | 2 provided (the two reads) |
| Kafka | 0 published, 0 consumed on `rwb.asset.events.v1` | Not applicable |
| Temporal | 1 activity of the step, 2 kit activities, 1 child workflow on rwb-decision, 1 answer to rwb-case | Signalled by the case router |
| File | None | None |

### 13. Solution plan

| Task | Component | Work | DP |
|---|---|---|---|
| T1 | AssetsAndAuctionController | Two reads on base `/api/recovery/asset/v1` with the right, the scope and the page shape of the contract | DP13 |
| T2 | BuyBackService | Validate the case state, the template version and the approval answer; refuse a second signature that is absent | — |
| T3 | BuyBackService | Evaluate R-DIS-24 and R-DIS-66 through EvaluateRules with the DISPOSAL package version | — |
| T4 | AssetsAndAuctionRepository | Insert `listing` and `asset_sale` in `rwb_asset` in one transaction with the record | DP03 |
| T5 | DecisionRecordClient | Call the local decision-record library before any row change; map a failed write to MSG-P7-003 | DP03 |
| T6 | CaseClient and DeviationClient | Read the case, raise the deviation, answer the two case moves with the rule ID and version | DP05, DP11 |
| T7 | AssetDisposalWorkflow | Add the buy-back step, its timer and its idempotency key (case id, rule version, template version) | DP12 |
| T8 | Edge and screens | SCR-21 and SCR-22 through the gateway-bff composite route; no direct service call from a browser | DP19 |
| T9 | Tests | The seven cases of §16, the boundary test of AC4 and the schema grants | DP05 |

The legacy monolith components map one to one: `AssetsAndAuctionController`, `AssetsAndAuctionService`, `AssetsAndAuctionRepository` and the published interface of TSD S5 T2 become the controller, the service, the repository and the two clients; the Quartz job of the module is not this story's.

### 14. Validation and messages

| ID | Type | Message (copied) | Raised by |
|---|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. | Declared for the slice; this step writes no floor of its own |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. | Declared for the slice; the re-appraisal slice raises it (RWB-S5-E3026-APP) |
| MSG-GEN-001 | Error | Enter {field}. | The buy-back element when a required field is empty |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | Edge, on a role without the right |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on a failed decision record (AC3) |

### 15. Screens and states

| Screen | States | Read by this story | Note |
|---|---|---|---|
| SCR-21 Asset list | Loading; list; empty, error, no access: Not specified in the source documents (CG-ALL-10231) | GET /api/recovery/asset/v1/assets | Through the gateway-bff composite route (DP19) |
| SCR-22 Asset record | Take-on; held; listed; sold; loading, empty, error, no access: Not specified in the source documents (CG-ALL-10232) | GET /api/recovery/asset/v1/assets/{assetId} | Carries the buy-back block; its element states are not in a closed list (GAP-2960; ASM-4857) |

The screen states are the legacy ones and are unchanged. The buy-back block shows the approval answer, the template version and the two row identifiers the step writes; it offers no control when the case is in `DISPOSAL_PAUSED_DEVIATION`.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-032-01 | AC1 | Component | Case in `ROUTE_WITH_APPROVER` on the fake, asset held, approval approved, DISPOSAL package version in force, template version current |
| TC-E4-032-02 | AC2 | Component | Case in `ASSET_HELD`, deviation open in X1 to X7 on the fake, raise accepted |
| TC-E4-032-03 | AC3 | Component | Decision record store forced to fail; no listing and no terms after the run |
| TC-E4-032-04 | Access | Contract | A role without the right on the operation; 403 with MSG-P4-002 |
| TC-E4-032-05 | Principle 5 | Component | Forced record write failure inside the transaction; both rows rolled back, MSG-P7-003 |
| TC-S5-E4032-APP-01 | AC4 | Component | Schema grants of the service login; outbox table inspected after the run |
| TC-S5-E4032-APP-02 | AC5 | Component | The same signal delivered twice with the same rule and template version |
| TC-S5-E4032-APP-03 | Boundary of §12.7 tables (ASM-3438) | Component | Attempt to write to `asset`; `listing` and `asset_sale` are the only tables written |
| TC-S5-E4032-APP-04 | AC6 | Contract | Call without identity, call from a role without the right, call for an unknown asset or case; 401, 403 and 404 answered, no row written |
| TC-S5-E4032-APP-05 | AC7 | Component | Activity forced to fail and to exceed its timeout; retry under the activity settings; timeout value Not specified in the source documents (NEWAC-RWB-S5-E4032-APP-AC7) |
| TC-S5-E4032-APP-06 | AC8 | Component | rwb-deviation, rwb-case or rwb-decision fake fails or does not answer; no row in rwb_asset changed |
| TC-S5-E4032-APP-07 | AC9 | Component | Case in a status the state model does not allow for the buy-back; change refused, nothing changed |

No `-ITG` copy is written: no integration story of RWB-E4-032 exists in this WP, and the cross-service paths are covered here by fakes.

### 17. Guardrails

- No business value in code: the template price, the deviation codes, the approval limit and the closed lists are reference and governed rows read at their version (BR-S5-023).
- No personal data in events, workflow inputs or logs: the former owner is a party key, never a name or a number.
- ACE data only through the owner's contract or a `v_ace_*` view of rwb-source-data; this service holds no `v_ace_*` grant and reads no other `rwb_*` schema (DP05).
- The decision record is written before any row changes, in the same transaction (DP03).
- One hop per REST call, 2 s timeout, no retry that duplicates a write.
- No issue-tracker reference in this story.

### 18. Traceability

| Legacy AC | This story's AC | Feature | L3 process | Rule | TC | Requirement |
|---|---|---|---|---|---|---|
| AC1 | AC1 | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | R-DIS-24 | TC-E4-032-01 | REQ-S5-010 |
| AC2 | AC2 | FEAT-AST-23 | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | R-DIS-66 | TC-E4-032-02 | REQ-S5-010 |
| AC3 | AC3 | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | BR-S5-023, P7 record rule | TC-E4-032-03, TC-E4-032-05 | REQ-S5-010 |
| — | AC4 | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | DP05 boundary | TC-S5-E4032-APP-01 | REQ-S5-010 |
| — | AC5 | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | DP03 and idempotency | TC-S5-E4032-APP-02 | REQ-S5-010 |
| Access and Principle 5 rows of the legacy story | — | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4032-APP-2) | Rights matrix, P7 record rule | TC-E4-032-04, TC-E4-032-05 | REQ-S5-010 |

Sources: legacy story RWB-E4-032; FSD S5 A2.23; TSD S5 T3.1, T4, T6.1, T-A; Business Rules and Routing Logic v4; Business Requirements Program v5 (REQ-S5-010); Epics 3 to 8 Specification v3 (FEAT-AST-23); context pack S5.

### 19. Out of scope

- The approval, its limit, its answer and the maker-checker workflow, which are rwb-decision's and rwb-access's.
- The deviation record, its screening, its pause, its owner and its return (R-DEV-18, R-DIS-68), which are rwb-deviation's.
- The case of record, its states, its tasks, its timers and the parent `CaseWorkflow`, which are rwb-case's.
- The completion of the buy-back, its signature and its funding (R-DIS-61, R-DIS-62), the money and the posting, which are rwb-payment's and RWB-S5-E4030-APP's.
- The template, its price and its version, which are rwb-comms'.
- The former owner and the ACE NPA facts, which are rwb-source-data's, and every `v_ace_*` read.
- The AMIS, ALS and GL posting named by the FSD integration points, which is rwb-integration's and rwb-payment's.
- The schema, the grants and the migration, which are the DB story; the deployment, the topic and the queue, which are the OPS story.
- The other 70 rules of the DISPOSAL package and the other disposal routes.

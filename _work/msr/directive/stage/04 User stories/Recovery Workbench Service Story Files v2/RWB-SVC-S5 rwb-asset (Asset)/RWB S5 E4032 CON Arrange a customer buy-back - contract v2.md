# RWB-S5-E4032-CON Arrange a customer buy-back - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4032-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S5-E4032-CON-16); the squad sizes it at refinement |
| Contract version | Baseline v1, tagged before any consumer builds |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped; traced to REQ-S5-010 in the Requirement row) |
| Requirement | REQ-S5-010 |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 23 November 2026: the contract slice of legacy RWB-E4-032 for rwb-asset, written first and alone. It publishes the two reads of SCR-21 and SCR-22 on base `/api/recovery/asset/v1` with the buy-back element of FEAT-AST-23, the closed lists of the element, the rows the step consumes with their owners, the decision-record element of the platform library, the error set and one fake per consumed row, so that RWB-S5-E4032-APP can build and test on Day 1 against a tagged baseline. The topic name `rwb.asset.events.v1` and the queue name `rwb-asset` are fixed here for the slice, and the slice publishes no event of its own. No source publishes the operation names of the consumed rows, the field that holds the template price or the buy-back value of the two closed lists (GAP-2961; ASM-4858). The split plan gives this story no dependency, and the contract baseline is therefore tagged before any consumer builds (GAP-2961). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4032-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (28 resolved, 17 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **solution architect of rwb-asset**, I want **the published contract of a customer buy-back baselined with its reads, its element, its closed lists, its consumed rows and its fakes**, so that **the application story can build on Day 1 without waiting for another service**.

This story owns the contract artefacts of legacy RWB-E4-032 and nothing that runs:

- the two reads behind SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, with the buy-back element of FEAT-AST-23 and its closed lists (DP13);
- the declaration of the rows the buy-back step consumes, each with its owner and a 2 s timeout, and of the two rows it writes (DP05, DP11);
- the decision-record element of the platform library as the only record shape the step may use (DP03);
- the error set, the five messages of the legacy story and the right that each operation declares;
- one fake per consumed row, plus the gateway-bff fake for the composite route (DP19);
- the names of the slice: base `/api/recovery/asset/v1`, schema `rwb_asset`, topic `rwb.asset.events.v1`, queue `rwb-asset`.

It does not own: the code that runs the buy-back step, the listing and the terms rows, the workflow and its tests, which are RWB-S5-E4032-APP; the case contract of rwb-case; the approval child of rwb-decision and the delegated limit of rwb-access; the raise contract of rwb-deviation; the template read of rwb-comms; the party read of rwb-source-data; and the schema build of S5.

### 2. Business rationale

The legacy story asked for one behaviour, a buy-back opened with the approval the limit requires (RWB-E4-032 AC1), and the FSD keeps it as FEAT-AST-23 with the sale officer acting (FSD S5 A2.23.2). In the target, that behaviour crosses five owners: the listing and the terms are rwb-asset's, the case is rwb-case's, the approval is rwb-decision's with the limit in rwb-access, the pause is rwb-deviation's and the price is rwb-comms'. Contract-first is what keeps them apart: R5.4 class C says another service's contract is built against its published shape and its fake, and it never blocks a build.

- **One baseline, two consumers.** RWB-S5-E4032-APP and the screens read the same shapes; the edge reads them for SCR-21 and SCR-22. A single tagged baseline stops the element drifting between the read, the fake and the screen (GAP-2961; ASM-4858).
- **The names are fixed by the platform rules.** Base `/api/recovery/asset/v1` (DP13), schema `rwb_asset`, topic `rwb.asset.events.v1` (DP14 naming rules of the context pack), queue `rwb-asset`. No story chooses them again.
- **DP05 is a prohibition, not a read.** The legacy data table lists `v_ace_customer` and `v_ace_npa_sale`; in the target the former owner is a party key on the owner's contract, and the baseline publishes no field that would need a `v_ace_*` grant.
- **DP03 keeps one record shape.** The decision record is the platform library's element and the shared topic `rwb.decision-record.v1`; the baseline references it and defines no local copy.
- **What is missing is named, not invented.** The consumed operation names, the field that holds the template price and the buy-back value of the two closed lists have no source (GAP-2961; ASM-4858), and each carries the placeholder of §R9.

The business value is the one the legacy story carried and REQ-S5-010 keeps: a buy-back only happens with a recorded approval. The contract baseline makes that condition testable before any service is built.

### 3. Preconditions

- The platform naming rules of the context pack are adopted: one schema, one login, one base, one topic and one queue per service.
- The ownership rows of S5 are known: `listing` and `asset_sale` are S5's tables, and the six REST operations of the service are its own (context pack, "Ownership rows owned by S5").
- The table columns of TSD S5 T3.1 are the field basis for the two written rows, with the standard record columns of TSD S5 T3.0.
- The closed lists of TSD S5 T3.2 (LOV-LISTING, LOV-SALE-CHANNEL, LOV-HOLDING, LOV-ASSET-TYPE) are the only allowed values in the element; no source adds a buy-back value (GAP-2961; ASM-4858).
- The rights matrix of TSD S5 T6.1 gives the right each operation declares.
- RWB-PLT-E1027-CON is published, so the decision-record element can be referenced rather than defined (DP03).
- RWB-PLT-N001-CON is published, so the composite route of SCR-21 and SCR-22 is a named contract (DP19).
- The five messages of the legacy story (MSG-S5-001, MSG-S5-002, MSG-GEN-001, MSG-P4-002, MSG-P7-003) are the error text of the baseline; no new message is invented.
- No approval is needed to tag a Draft baseline; the tuple is tagged when the seven criteria of §7 pass.

### 4. Flow

| # | Step | Actor | Result |
|---|---|---|---|
| 1 | Take the field basis | Contract owner | The two written rows keep the columns of TSD S5 T3.1 and no new column |
| 2 | Shape the two reads | Contract owner | Page and item of the asset, with the buy-back element of FEAT-AST-23 and the closed lists of T3.2 |
| 3 | Declare the consumed rows | Contract owner | Case read, case-move answer, deviation raise, approval child, template price, each with its owner and a 2 s timeout |
| 4 | Reference the record element | Contract owner | The decision-record element of RWB-PLT-E1027-CON, with rule ID, rule version, template version and case |
| 5 | Freeze the errors | Contract owner | 401, 403, 404, 409, 422 and 503 mapped to the five messages |
| 6 | Build the fakes | Contract owner | One fake per consumed row plus the gateway-bff fake, each answering the criteria of the APP story |
| 7 | Tag the baseline | Contract owner | Baseline v1 tagged; RWB-S5-E4032-APP and the edge may build |
| 8 | Keep the placeholders visible | Contract owner | Each unnamed value carries the §R9 placeholder and its gap row; no default is silent |

### 5. Exception paths

| Condition | What happens | Who resolves | Covered by |
|---|---|---|---|
| A field of the payload is not in TSD S5 T3.1 | The baseline is rejected; the field is raised as a gap, never added by the consumer | Contract owner (this story) | AC1 |
| A closed list has no value for the buy-back channel or the listing status | The element carries the placeholder and the gap row; the value is not invented | Contract owner; rwb-case reference data owns the list (GAP-2961) | AC2 |
| A consumed operation has no published name | The table carries the §R9 placeholder and a 2 s timeout; the consumer builds against the fake | Contract owner (this story) | AC3 |
| The decision-record element is redefined locally | The baseline is rejected: the platform element is referenced, never copied (DP03) | This story | AC6 |
| A payload field would need a `v_ace_*` read | The field is dropped and the reference is carried as a party key (DP05) | This story | AC7 |
| A consumer asks for a version that is not tagged | The consumer builds against the last tagged baseline; no hot edit is allowed | This story and the consumer | Not specified in the source documents (DOR-RWB-S5-E4032-CON-3) |
| A fake answers a value the source does not give | The fake is rejected: it answers only what the baseline declares | This story | AC5 |
| SCR-21 or SCR-22 is opened without the right | 403 with MSG-P4-002; the no-access state is shown | Contract owner (this story) | AC4 |
| SCR-21 or SCR-22 has no asset to show | Empty state: Not specified in the source documents (DOR-RWB-S5-E4032-CON-10) | Contract owner (this story) | Not specified in the source documents (DOR-RWB-S5-E4032-CON-3) |
| SCR-21 or SCR-22 read fails | 503 answered; error state: Not specified in the source documents (DOR-RWB-S5-E4032-CON-10) | Contract owner (this story) | AC4 |
| SCR-21 or SCR-22 waits for its read | Loading state: Not specified in the source documents (DOR-RWB-S5-E4032-CON-10) | Contract owner (this story) | Not specified in the source documents (DOR-RWB-S5-E4032-CON-3) |

### 6. INVEST check

| Letter | Result | Evidence |
|---|---|---|
| Independent | Yes | No dependency at all: lane CG-W3, Day 1, no H, C, I or X row. |
| Negotiable | Yes | The three unnamed values stay placeholders; the shape is what is agreed. |
| Valuable | Yes | Unblocks RWB-S5-E4032-APP and the edge reads of SCR-21 and SCR-22 on Day 1. |
| Estimable | Yes | Two reads, one element, six consumed declarations, one error set, six fakes. |
| Small | Yes | Documents and fakes only; no table, no migration, no workflow. |
| Testable | Yes | Seven criteria of §7 and nine test cases of §16, six of them at contract level. |

### 7. Acceptance criteria

```gherkin
Feature: Arrange a customer buy-back - contract

  Scenario: AC1 The two reads are published (new, D-RCV-60)
    Given the baseline is built from TSD S5 T3.1 and the ownership rows of S5
    When the contract is read
    Then the asset list and the asset record are published on base /api/recovery/asset/v1 with their page and item shapes
    Then the asset record carries the buy-back element of FEAT-AST-23 with the listing and the terms of the buy-back

  Scenario: AC2 The closed lists and the names are fixed (new, D-RCV-60)
    Given the naming rules of the context pack and the lists of TSD S5 T3.2
    When the contract is read
    Then every value of the element belongs to the closed lists and schema rwb_asset, topic rwb.asset.events.v1 and queue rwb-asset are the only names used

  Scenario: AC3 The consumed rows are declared with their owners (new, D-RCV-60)
    Given the buy-back step calls five owners
    When the contract is read
    Then each consumed row names its owner, its purpose and a 2 s timeout
    Then each unnamed operation carries the placeholder of the source rules and a gap row

  Scenario: AC4 The error set is closed (new, D-RCV-60)
    Given the operations of the baseline
    When each failure is provoked on the fake
    Then the answers are 401, 403, 404, 409, 422 and 503 only
    Then the text of each error is one of the five messages of the legacy story

  Scenario: AC5 The fakes answer every declared row (new, D-RCV-60)
    Given the fakes of the baseline
    When the criteria AC1 to AC5 of RWB-S5-E4032-APP are run against them
    Then each consumed row is answered by its fake and no fake calls a real service

  Scenario: AC6 The record element is the platform's (new, D-RCV-60)
    Given the decision-record element used by the baseline
    When it is compared with RWB-PLT-E1027-CON
    Then the shape is the library's, with rule ID, rule version, template version and case
    Then no local copy of a decision-record table is declared

  Scenario: AC7 No field needs a v_ace_* read (new, D-RCV-60)
    Given the payload of the element and the two rows
    When the fields are checked against the views of ACE
    Then the former owner is a party key and no personal field is published
    Then no field requires a v_ace_* grant of this service

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given the status model of the buy-back is the baseline's
    When a status change the model does not allow is requested on the fake
    Then the change is refused with one of the closed error answers of AC4
    Then no status of the case is changed
```

### 8. Business rules

| Rule ID | Rule | Effect on the contract | Source |
|---|---|---|---|
| BR-S5-023 | No value a business person may change is written in code; it is read from reference data with its version | Every list and every price is a published field, never a constant of the baseline | FSD S5 A2.23.3.1 |
| R-DIS-24 | Agree the buy-back terms at the template price, when `route = buy_back and second_signature given` | The element carries the template version and the approval answer as fields | Business Rules and Routing Logic v4 |
| R-DIS-66 | Pause the disposal, stop contact where required and route to the deviation owner, when `deviation_open in (X1, X2, X3, X4, X5, X7)` | The element carries the deviation reference and the paused state | Business Rules and Routing Logic v4 |
| R4 naming | Base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1`, queue `rwb-<short>`, schema `rwb_<name>` | The names of the slice are fixed and not negotiable | Template and Rules v1 §R4; context pack |
| DP13 | `/api/recovery/v1` becomes `/api/recovery/<short>/v1` | The base of both reads | Template and Rules v1 §R5.5 |
| DP19 | A screen is a gateway-bff composite route | Both reads are reached through the composite route, not directly | Template and Rules v1 §R5.5 |

The closed lists of TSD S5 T3.2 are quoted unchanged in the element; the buy-back has no value in LOV-SALE-CHANNEL or LOV-LISTING (GAP-2961; ASM-4858).

The lists are read from reference data; the parameters are Not specified in the source documents (DOR-RWB-S5-E4032-CON-20).

### 9. State transitions

| Element | State field | Allowed values | Source |
|---|---|---|---|
| listing | status | DRAFT, LIVE, UNDER_OFFER, SOLD, WITHDRAWN | LOV-LISTING, TSD S5 T3.2 |
| listing | sale_channel | DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION, RAMC | LOV-SALE-CHANNEL, TSD S5 T3.2 |
| asset | holding_status | HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED, RENTED | LOV-HOLDING, TSD S5 T3.2 |
| case (read only) | state | The 40 states of the DISPOSAL machine, of which `ROUTE_WITH_APPROVER`, `ROUTE_APPROVED_BUYBACK`, `ASSET_HELD` and `DISPOSAL_PAUSED_DEVIATION` are used | TSD S5 T4; Business Rules and Routing Logic v4 |

No value is added to a list by this story; where the buy-back has no value the element carries the placeholder and the gap row.

### 10. Authority

| Operation | Capability area | Right | Roles | Source |
|---|---|---|---|---|
| GET /api/recovery/asset/v1/assets | Asset and disposal | R | RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and 23 more | TSD S5 T6.1 |
| GET /api/recovery/asset/v1/assets/{assetId} | Asset and disposal | R | as above | TSD S5 T6.1 |
| Buy-back step (internal, not a REST operation) | Asset and disposal | C | RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, SY-DATALOAD | Legacy permission checks of RWB-E4-032; TSD S5 T6.1 |

Each operation declares its area and right in the baseline and the edge enforces them; a refused call answers 403 with MSG-P4-002. DP08 is not in this slice's pattern set, so the authorise contract of rwb-access is not referenced. The buy-back is an element of the Asset answer and not an operation; the four consumed rows are placeholders, confirmed with their owners before the baseline is tagged (GAP-1921; GAP-1928). The step requires the case in ROUTE_WITH_APPROVER with the buy-back route for R-DIS-24, read on the rwb-case contract; the asset is held while the route is with the approver, and the case-move answer carries ROUTE_APPROVED_BUYBACK (GAP-1925).

### 11. Data

| Payload row | Basis | Fields | Field IDs |
|---|---|---|---|
| AssetPage, Asset | TSD S5 T3.1 `asset` | id, case_id, collateral_id, asset_ref, asset_code, asset_type, transfer_in_type, from_segment, transfer_in_date, book_value, holding_status, holding_cost_to_date | DF-COL-028 to DF-COL-042 |
| BuyBack element | TSD S5 T3.1 `listing` and `asset_sale`; buy-back terms written on asset_sale with listing_id pointing at the buy-back listing and sale_price taken from the template price reference with its template version (price field and read operation owned by rwb-comms, P6) | listing: id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status; sale: id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, gain_loss, incentive_amount | DF-SAL-001 to DF-SAL-008; DF-SAL-009 to DF-SAL-019 |
| ApprovalAnswer | The approval child of the kit on rwb-decision; the limit is read from the delegated-authority rows of rwb-access at their version | approved, approver role, limit reference, answer date; element names Not specified in the source documents (GAP-2961; ASM-4858); the fake is derived from the rwb-decision kit and held under the drift test (GAP-1929) | Not specified in the source documents (DOR-RWB-S5-E4032-CON-7) |
| DecisionRecord | RWB-PLT-E1027-CON | case, asset, decision code, rule ID, rule version, template version, actor role, timestamp | DF-DEC-001 to DF-DEC-018 |
| DeviationRef | rwb-deviation contract | deviation reference and paused state; element names Not specified in the source documents (GAP-2961; ASM-4858) | DF-CAS-036 to DF-CAS-045 |

The former owner enters as a party key only; no name, address or identity number is published, and no field needs a `v_ace_*` grant (DP05). The buy-back sale channel and listing status are carried as a placeholder read from LOV-SALE-CHANNEL and LOV-LISTING at their version until the reference-data owner publishes a buy-back value; the asset holding status is not changed in this step (GAP-1924).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Right | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /api/recovery/asset/v1/assets | Asset and disposal R | Query: type, status, region, page, size | AssetPage | 401, 403, 503 |
| GET | /api/recovery/asset/v1/assets/{assetId} | Asset and disposal R | None | Asset, with the buy-back element | 401, 403, 404, 503 |

#### 12.2 REST operations consumed

| Consumer step | Owner | Path or operation | Timeout | Notes |
|---|---|---|---|---|
| Read the case and its state | rwb-case (P3) | GET /api/recovery/case/v1/cases/{caseId} | 2 s | Published |
| Answer the case move | rwb-case (P3) | Operation name Not specified in the source documents (GAP-2961; ASM-4858) | 2 s | Carries the rule ID and version |
| Raise the deviation | rwb-deviation (S8) | POST on the rwb-deviation path `/cases/{caseId}/deviations`; name Not specified in the source documents (GAP-2961; ASM-4858) | 2 s | Returns the deviation reference |
| Ask the approval | rwb-decision (P7) | Approval child workflow on queue `rwb-decision` | 2 s | Maker-checker with the DoA limit as a parameter |
| Read the template price | rwb-comms (P6) | Operation name Not specified in the source documents (GAP-2961; ASM-4858) | 2 s | Returns the price and the template version; the fake is derived from the rwb-comms document and held under the drift test (GAP-1929; GAP-2960) |

#### 12.3 Events published

None for this slice. The topic of the service is `rwb.asset.events.v1`; its events are `AssetTakenOn` (RWB-S5-E3019-APP) and `AssetSold` (RWB-S5-E4030-APP). The baseline declares no event of the buy-back and no field of an event head.

#### 12.4 Events consumed

None. The step is signalled through the case router of rwb-case and through the approval answer; the baseline declares no subscription.

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contract surface |
|---|---|---|---|
| AssetDisposalWorkflow | Workflow, stage child | rwb-asset | The step `openBuyBack` and its inputs: case id, asset id, template version |
| ApprovalWorkflow | Child workflow of the kit | rwb-decision | Input: the DoA limit reference; output: approved or refused |
| requestDeviation | Activity | rwb-deviation | Input: case, asset, codes; output: deviation reference |

#### 12.6 Schedules

None. No schedule starts or continues the buy-back step.

#### 12.7 Tables owned

| Table | Schema | Service | Owner | Columns in the element | Field IDs |
|---|---|---|---|---|---|
| listing | rwb_asset | rwb-asset | Not specified in the source documents (DOR-RWB-S5-E4032-CON-24) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | DF-SAL-001 to DF-SAL-008 |
| asset_sale | rwb_asset | rwb-asset | Not specified in the source documents (DOR-RWB-S5-E4032-CON-24) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, gain_loss, incentive_amount | DF-SAL-009 to DF-SAL-019 |

#### 12.8 Contract fakes

| Fake | Answers | Criteria it serves |
|---|---|---|
| rwb-case fake | Case read in `ROUTE_WITH_APPROVER` and `ASSET_HELD`; the case-move answer | AC1, AC2, AC3 of the APP story |
| rwb-decision fake | Approval approved and refused; the decision-record writer, success and forced failure | AC1, AC3 of the APP story |
| rwb-deviation fake | The open codes and the raise answer | AC2 of the APP story |
| rwb-comms fake | The template price at a version | AC1 and AC5 of the APP story |
| gateway-bff fake | The composite route of SCR-21 and SCR-22 | AC4 of the APP story |
| rwb-source-data fake | The party key of the former owner | AC7 of this story |

#### 12.9 Call-type summary

| Call type | Provided | Consumed |
|---|---|---|
| REST | 2 reads on `/api/recovery/asset/v1` | 3 (case read, case-move answer, deviation raise) |
| Kafka | 0 on `rwb.asset.events.v1` | 0 |
| Temporal | 1 workflow and 1 activity on `rwb-asset` | 1 child workflow on `rwb-decision` |
| File | None | None |

### 13. Solution plan

| Task | Work | DP |
|---|---|---|
| T1 | Freeze the two reads on base `/api/recovery/asset/v1` from TSD S5 T3.1 and appendices T-A | DP13 |
| T2 | Define the buy-back element from `listing` and `asset_sale`, with the lists of T3.2 and the placeholders of §R9 | — |
| T3 | Declare the five consumed rows with owners and 2 s timeouts; keep the unnamed operations as placeholders | DP11 |
| T4 | Reference the decision-record element of RWB-PLT-E1027-CON and nothing local | DP03 |
| T5 | Freeze the error set and map it to the five legacy messages | — |
| T6 | Publish no field that would need a `v_ace_*` grant; carry the owner as a party key | DP05 |
| T7 | Build the six fakes, each answering only declared values | — |
| T8 | Tag baseline v1 and hand it to RWB-S5-E4032-APP and the edge | DP19 |

### 14. Validation and messages

| ID | Type | Message (copied) | Where it appears in the baseline |
|---|---|---|---|
| MSG-S5-001 | Error | The floor is {pct} of fair market value, below the {limit} this level may approve. | Declared; raised when a floor below the approver's limit is refused (FSD S5 VR-S5-011-1); raised by the pricing slice, not by this one |
| MSG-S5-002 | Warning | The appraisal is from {date}, more than a year ago. Order a new one before pricing. | Declared; raised when a price is requested on an appraisal older than a year (FSD S5 VR-S5-009-1; PRD FR-S5-019 refuses the price); not raised by this slice |
| MSG-GEN-001 | Error | Enter {field}. | The buy-back element, required field empty → 422 (standard: required field empty, FSD P4 VR-P4-003-1) |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | 403 on both reads and on the step (standard: role without the right, FSD P4 AC-EXC-P4-001-05) |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 409 on a failed decision record (FSD P4 AC-EXC-P4-004-04) |

A payload that does not match the element answers 422 with MSG-GEN-001; a version clash answers 409 with MSG-P7-003 where the record is the cause.

### 15. Screens and states

| Screen | Route | Element it reads | States it must render |
|---|---|---|---|
| SCR-21 Asset list | gateway-bff composite route | AssetPage | Loading; list; empty, error and no access: Not specified in the source documents (CG-ALL-10243) |
| SCR-22 Asset record | gateway-bff composite route | Asset with the buy-back element | Take-on; held; listed; sold; and the paused state carried by the case read; empty, loading, error and no access: Not specified in the source documents (CG-ALL-10244) |

The element exposes the two row identifiers, the approval answer, the template version and the deviation reference. A screen shows no control when the case read gives `DISPOSAL_PAUSED_DEVIATION`; the value of a buy-back channel or a buy-back listing status is not in a closed list and stays a placeholder (GAP-2961; ASM-4858). Criterion AC1 is read from the state ROUTE_WITH_APPROVER of R-DIS-24 and adds no state of its own; the refusal of R-DIS-27 belongs to the route-approval slice (GAP-2962).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-032-01 | AC1 of the APP story, schema conformance | Contract | A valid buy-back payload of the baseline; the published schema file |
| TC-E4-032-02 | AC2 of the APP story, deviation element | Contract | A payload with the deviation reference and the paused state |
| TC-E4-032-03 | AC3 of the APP story, error mapping | Contract | A failed record write on the fake; 409 with MSG-P7-003 |
| TC-E4-032-04 | Access | Contract | A role without the right on each read; 403 with MSG-P4-002 |
| TC-E4-032-05 | Principle 5, the closed error set | Contract | Each failure provoked; only 401, 403, 404, 409, 422 and 503 returned |
| TC-S5-E4032-CON-01 | AC1, AC2 | Contract | Schema validation of the two reads against the element and the four closed lists |
| TC-S5-E4032-CON-02 | AC3 | Contract | One consumed row per owner; each with a 2 s timeout; each unnamed operation carrying its placeholder |
| TC-S5-E4032-CON-03 | AC5 | Contract | The five fakes run against the criteria of the APP story; no real call recorded |
| TC-S5-E4032-CON-04 | AC6, AC7 | Contract | The record element compared with RWB-PLT-E1027-CON; the payload scanned for a personal field and for a `v_ace_*` need |
| TC-S5-E4032-CON-05 | AC4; boundary of the tables of §12.7 (Not specified in the source documents (DOR-RWB-S5-E4032-CON-12)) | Contract | Boundary values of each column of the listing and asset_sale tables of §12.7 |
| TC-S5-E4032-CON-06 | AC4, error set closed | Contract | Each failure provoked on the fake; only 401, 403, 404, 409, 422 and 503 returned; each text one of the five legacy messages |
| TC-S5-E4032-CON-07 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S5-E4032-CON-AC8) |

The five legacy test cases are kept with their identifiers; no `-ITG` copy is written, because no integration story of RWB-E4-032 exists in this WP.

### 17. Guardrails

- No business value in the baseline: lists, prices and limits are fields with a version, never constants (BR-S5-023).
- No personal data in the element, the fakes or the test data; the former owner is a party key.
- No field that would need a `v_ace_*` grant; no cross-schema reference in the payload (DP05).
- The decision-record element is the platform library's; no local record table is declared (DP03).
- The names of the slice come from §R4 only: base `/api/recovery/asset/v1`, schema `rwb_asset`, topic `rwb.asset.events.v1`, queue `rwb-asset`.
- The fakes answer declared values only and never call a real service.
- No issue-tracker reference in this story.

### 18. Traceability

| Legacy artefact | This story | Baseline section | Test |
|---|---|---|---|
| RWB-E4-032 endpoints (one asset read, one listing write) | AC1, AC2 | 12.1, 12.7 | TC-S5-E4032-CON-01 |
| RWB-E4-032 data table (case, deviation, assignment, decision log, ACE views) | AC3, AC7 | 11, 12.2 | TC-S5-E4032-CON-02, TC-S5-E4032-CON-04 |
| RWB-E4-032 messages (five) | AC4 | 14 | TC-E4-032-03, TC-E4-032-05 |
| RWB-E4-032 permission checks | AC1 | 10 | TC-E4-032-04 |
| FSD S5 A2.23 (FEAT-AST-23) | AC1, AC2 | 11, 15 | TC-S5-E4032-CON-01 |
| TSD S5 T3.1, T3.2, T6.1, T-A | AC1, AC2, AC4 | 11, 12.1, 12.7 | TC-S5-E4032-CON-01 |
| Business Requirements Program v5, REQ-S5-010 | AC1 | 12.5 | TC-S5-E4032-CON-03 |

### 19. Out of scope

- The code of the buy-back step, its workflow, its repository and its tests, which are RWB-S5-E4032-APP.
- The case contract, the approval child, the delegated limit, the deviation raise contract and the template read; each is its owner's and is referenced here only.
- The schema, its grants and its migration, which are the DB story of S5; the topic, the queue and the deployment, which are the OPS story.
- The event catalogue of `rwb.asset.events.v1`, which belongs to the take-on and the sale slices and to the platform event story.
- The AMIS, ALS and GL posting named by the FSD integration points, which is rwb-integration's and rwb-payment's.
- Any new closed-list value, business message or personal field.

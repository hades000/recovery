# RWB-S5-E4025-APP Accept a bid below the floor with a second signature

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-S5-E4025-APP-16); no size value is given in the source documents |
| Contract version | Not specified in the source documents (DOR-RWB-S5-E4025-APP-23); base is /api/recovery/asset/v1 |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4025-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | Pending (C1); FEAT-AST-16 of the Epics 3 to 8 Specification v3 and FSD S5 A2.16 until the PRD allocates requirement IDs |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-025 for rwb-asset. The four legacy criteria are kept word for word with their origin tag and the six legacy test cases keep their IDs. The step becomes the below-floor branch of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery`: it evaluates R-DIS-41 on a bid under the floor and R-DIS-42 on a given second signature against the DISPOSAL package in force, raises the second signature as an approval on rwb-decision's queue (P7), writes the agreed sale on `asset_sale` in `rwb_asset`, records each outcome before the row changes (DP-03), answers `SECOND_SIGNATURE_PENDING` and `SALE_AGREED` to rwb-case and publishes nothing. The `v_ace_*` facts arrive on the rwb-source-data contract (DP-05), the base becomes `/api/recovery/asset/v1` (DP-13), and the screens read through the gateway-bff route (DP-19). Gaps: consumed operation names (GAP-2912; ASM-4810); no field for the bid or the signature (GAP-2913; ASM-4811); the accept surface conflicts with the legacy endpoints table (GAP-2914; ASM-4812); no published operation raises the approval (GAP-2915; ASM-4813); no requirement id (GAP-2916; ASM-4814); DP-04 and the approval template outside the pattern set (GAP-2917; ASM-4815). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4025-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **to route any bid under the floor for a second approval before it can be accepted**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E4-025. It owns the four legacy criteria with their origin tag; the below-floor branch of `AssetDisposalWorkflow` on `rwb-asset` as a child of the case workflow (Architecture v5 slide 13); R-DIS-41 on a bid under the floor and R-DIS-42 on a signature given, on the package in force; the second-signature approval item and its two-working-day clock on rwb-decision's queue; the decision record before each change (DP-03); the agreed sale on `asset_sale` in `rwb_asset`; the answers `SECOND_SIGNATURE_PENDING` and `SALE_AGREED`; and the reads of SCR-23 Listing and price and SCR-21 Asset list on `/api/recovery/asset/v1` through the gateway-bff route (DP-13, DP-19).

It does not own: the shapes, the consumed rows and the fakes, which are RWB-S5-E4025-CON; the rounds, the bids and the award (the rounds story of RWB-E4-024); the descending price schedule (RWB-E4-022); the re-list after a refusal, which is R-DIS-43 and the re-list story of RWB-E4-026; the floor and its approval (FEAT-AST-11); the case and its states (rwb-case, P3); the approval record, the DoA levels and limits (rwb-decision, P7, and rwb-access, P4); the ACE asset facts (rwb-source-data, P1); the rule package (rwb-decision); and the deployment (the operations story of this key).

### 2. Business rationale

Legacy RWB-E4-025 kept a below-floor bid from being accepted on one signature: a bid under the floor moved the case to a second-signature queue, and only a given signature agreed the sale. The FSD keeps it as FEAT-AST-16 in module S5, run by the sale officer against an NPA sales cycle of 1,095 days (FSD S5 A2.16).

What D-RCV-60 changes:

- **the sale is this service's.** `asset_sale` and `listing` are S5's in `rwb_asset` (Ownership Map; Architecture v5 slide 41); the floor, the levels and the two clocks are values in force, never constants.
- **the approval stays with rwb-decision (P7).** The `approval` record and the DoA routing are P7's, and the stage reaches them over Temporal, never REST (Architecture v5 slide 13; TSD S5 T5.2).
- **the value stays with rwb-source-data (P1).** Only that service reads the `recovery.v_ace_*` views (Architecture v5 slide 8), so DP-05 is a **prohibition** and the facts arrive on the owner's product with a freshness stamp.
- **the case stays with rwb-case (P3).** This story evaluates, writes, records and **answers** the two moves; it writes no case row.
- **the decision is recorded first**, one per outcome, in the row's transaction — what AC1 asked and AC4 tested.
- **nothing is published.** EV-22 `AssetTakenOn` is the take-on story's (TSD S5 T5.3); §12.3 states the absence and a build that adds an event fails it.

### 3. Preconditions

- RWB-S5-E4025-CON tagged: reads, the round write, consumed rows, record element, error set, fakes.
- `listing` and `asset_sale` exist in `rwb_asset` with the TSD S5 T3.1 and T3.0 columns; no column is added for the bid or for the signature (GAP-2913; ASM-4811).
- The DISPOSAL package is in force with R-DIS-41 and R-DIS-42 from rwb-decision (P7), loaded through the service template; DP-04 is outside the pattern set (GAP-2917; ASM-4815).
- The floor, the `LOV-LISTING` and `LOV-SALE-CHANNEL` lists and the two clocks are reference data with a version (TSD S5 T3.2).
- The round, its bid and its bidder arrive from the rounds story of RWB-E4-024 inside this service; no bid column is named by a source (GAP-2913).
- The rwb-case state read and the case-move answer sit behind fakes; neither name is published (GAP-2912; ASM-4810).
- The rwb-source-data product with the appraisal and asset facts is published with a fake and a freshness stamp; its name is not published (GAP-2912).
- The second signature is raised as an approval on rwb-decision's queue; no published operation creates an approval item (GAP-2915; ASM-4813).
- RWB-PLT-E1027-CON writes in the caller's transaction (DP-03); RWB-PLT-N001-CON serves the screens, one hop each (DP-19).
- The service holds its own login on `rwb_asset`, no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-01, DP-05).
- No approval is needed to build against a Draft baseline; the contract is tagged when its tests pass.

### 4. Flow

1. The rounds story records a round and its bid on a live listing and signals the workflow with case, asset, listing, round and the bid; the step confirms the case state on the rwb-case contract.
2. The step reads the listing: start price, floor, round number, sale channel, status.
3. It reads the appraisal and asset facts on the rwb-source-data product, one hop, 2 s: appraised value, appraisal date, outlier flag, book value.
4. `BelowFloorEvaluator` loads the package in force and evaluates R-DIS-41: from `BID_RECEIVED`, on `BID_BELOW_FLOOR`, with the bid amount below the floor, the bid is routed for a second signature and the case state answer becomes `SECOND_SIGNATURE_PENDING` (Business Rules and Routing Logic v4).
5. `AssetDecisionRecordWriter` writes one record **before any change**; a failed write stops the step (DP-03; AC1, AC4).
6. `SecondSignatureRequester` raises the approval with the amount, the floor, the asset reference, the rule and its version, and the two-working-day clock of R-DIS-41; the approval item and its routing are rwb-decision's (GAP-2915).
7. The workflow waits on a durable timer. On a given signature, R-DIS-42 applies: from `SECOND_SIGNATURE_PENDING`, on `SECOND_SIGNATURE_GIVEN`, with a signature present, the bid is accepted and the sale agreed.
8. A second record is written, `SaleWriter` writes the agreed sale on `asset_sale` in one transaction with the record and the idempotency row, the listing status follows `LOV-LISTING`, and `CaseMoveAnswer` answers `SALE_AGREED` with the sale reference, the rule and its version; rwb-case writes the case.
9. A refused signature (R-DIS-43) is not this story's: the step answers the refusal state and the re-list story of RWB-E4-026 carries the asset back to the schedule (§19).
10. A repeated signal or `Idempotency-Key` writes once and is counted; the stage returns to its durable timer and the parent continues as new at each stage end and at least every 28 days.
11. No event and no outbox row leaves the service (§12.3).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record cannot be written | Nothing written, no move answered | MSG-P7-003 | AC4, TC-E4-025-04, -06 |
| X2 | The role lacks the right | 403 before any read or write | MSG-P4-002 | AC1, TC-E4-025-05 |
| X3 | The case is in another state | The rule does not fire; nothing written, state reported | None | AC2, AC3 |
| X4 | The bid is at or above the floor | R-DIS-41 does not fire; the bid is accepted on one signature by the rounds and sale path | None | AC3 |
| X5 | The floor is under the approver's limit | The accept is held and the floor is reported for the level it needs | MSG-S5-001 | AC1, AC2 |
| X6 | The appraisal is more than a year old | The accept is held and a new appraisal is asked for | MSG-S5-002 | AC1, AC3 |
| X7 | The approval expires or is refused | No sale, nothing written, the refusal state answered | None | AC2 |
| X8 | A contract misses 2 s or its breaker is open | Retry on the workflow schedule; 503 | None | AC1, AC3 |
| X9 | The ACE product is stale | Held, nothing written, the data date shown | MSG-P1-001 | AC3 |
| X10 | A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema | The grant refuses it and the boundary test fails the build | None (pipeline log) | AC5, TC-E4-025-09 |

X1 to X3 are the legacy paths on the split, X4 to X9 what the floor, the appraisal, the call types and the approval clock add, and X10 the DP-01 and DP-05 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the CON baseline and the fakes; no live P1, P3 or P7 |
| Negotiable | Activity names, decision codes and outcome shape are ours; rules, messages, screens, rows and reads are fixed |
| Valuable | A below-floor bid cannot be accepted on one signature, and the sale agrees the day the second one is given |
| Estimable | One branch, two evaluators, one approval request, two records, two row writes, two answers, three clients |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion on synthetic cases through the fakes, plus the access, at-floor, old-appraisal and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Accept a bid below the floor with a second signature

  Background:
    Given case "RC-2026-000541" holds asset "AST-2026-000541" in listing "LS-2026-000541"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-41 and R-DIS-42
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Accept a bid below the floor with a second signature (legacy RWB-E4-025 AC1)
    Given the rwb-case contract mock returns the case state BID_RECEIVED for "RC-2026-000541"
    Given the rwb-source-data contract mock returns the appraisal "AP-2026-000541" of asset "AST-2026-000541"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then routes any bid under the floor for a second approval before it can be accepted
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-42 (legacy RWB-E4-025 AC2)
    Given the rwb-decision contract mock returns the second signature of approval "A-2026-000542" for "RC-2026-000542"
    Given a case in state SECOND_SIGNATURE_PENDING
    When second signature given
    Then accept the bid below the floor and agree the sale
    Then the case moves to SALE_AGREED

  Scenario: AC3 Rule R-DIS-41 (legacy RWB-E4-025 AC3)
    Given the rwb-case contract mock returns the case state BID_RECEIVED for "RC-2026-000543"
    Given the rwb-decision contract mock returns an open approval item for the second signature of "RC-2026-000543"
    Given a case in state BID_RECEIVED
    When bid below floor
    Then route the bid for a second signature
    Then the case moves to SECOND_SIGNATURE_PENDING

  Scenario: AC4 Not recorded (legacy RWB-E4-025 AC4)
    Given the rwb-decision contract mock answers the approval item and the decision-record stub is stopped
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC5 A statement reaches a v_ace view, recovery_case or a foreign schema (X10) (new, D-RCV-60)
    Given the rwb-asset login holds no grant on a v_ace_* view, on recovery_case or on a foreign schema
    When a statement reaches one of them
    Then the grant refuses it and the boundary test fails the build

  Scenario: AC6 A repeated signal is written once and answered once (BR9) (new, D-RCV-60)
    Given the same signal or key of the accept arrives a second time
    When the repeated signal is received
    Then the decision record is written once, the answer is given once and the repeat is counted

  Scenario: AC7 The floor and the approver's limit are reference data at a version (BR3) (new, D-RCV-60)
    Given the floor and the approver's limit are held as reference data at a version
    When the accept is evaluated
    Then both are read at that version and no value is held in code

  Scenario: AC8 The rules of section 8 hold (BR1 to BR10) (new, D-RCV-60)
    Given every rule BR1 to BR10 of section 8 is in force as stated there
    When the story is built and its boundary and contract checks run
    Then each rule BR1 to BR10 holds as stated in section 8 and the checks pass

  Scenario: AC9 Error answers of the provided operations (401, 403, 404) (new, D-RCV-60)
    Given a caller without a valid credential, a caller without the right, or a request for an absent case
    When a provided operation is called
    Then it answers 401, 403 or 404 as the case requires and nothing is read or written

  Scenario: AC10 A replay of a write with the same idempotency key (BR9) (new, D-RCV-60)
    Given a write has been accepted under an idempotency key
    When a replay arrives with the same key
    Then the decision record is not written again, the first answer is returned and the replay is counted

  Scenario: AC11 Activity retry and timeout (X8) (new, D-RCV-60)
    Given a contract call misses 2 s or its breaker is open
    When the workflow activity runs
    Then it is retried on the workflow schedule and 503 is answered

  Scenario: AC12 A consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed contract call fails or does not answer
    When the workflow activity makes the call
    Then nothing is written and no move is answered
```

The four legacy criteria, AC1 to AC4, are word for word with the origin tag added, except the AC1 decision-record line (DP-03) and the AC4 decision-record line (CG-ALL-10055); AC5 to AC12 are the story's own. The legacy phrases are kept: `the action is taken`, `the user acts on the screen`, `bid below floor` and `the decision record cannot be written` stand, and the `Given the <service> contract mock returns <x>` lines are the only additions. The work happens in three places: rwb-decision raises and answers the approval, rwb-case writes the two moves, and this story evaluates, writes, records and answers. A bid at or above the floor never reaches this step (X4), and a refused signature is the re-list story's (R-DIS-43, §19).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-41 (BR11) | Asset disposal | D8.1 to D8.3 | BID_RECEIVED | BID_BELOW_FLOOR | bid_amount below floor_price | Route the bid for a second signature | SECOND_SIGNATURE_PENDING | Committee | Committee View | 2 working days |
| R-DIS-42 (BR12) | Asset disposal | D8.1 to D8.3 | SECOND_SIGNATURE_PENDING | SECOND_SIGNATURE_GIVEN | second_signature_by present | Accept the bid below the floor and agree the sale | SALE_AGREED | Sale officer | Case Workspace, Decision Log | None |

Both rows are copied character for character from the Business Rules and Routing Logic v4, with the BR ID added to the ID cell: BR11 is R-DIS-41, covered by AC3 and TC-E4-025-03, and BR12 is R-DIS-42, covered by AC2 and TC-E4-025-02; their owner column is a business role, so rwb-case holds the states on this story's answer while the `asset_sale` and `listing` rows are written here. FSD S5 A2.16 also lists R-DIS-17 (the accepted re-appraisal, moving to `ASSET_HELD`); it is the re-appraisal story's and is not evaluated here. R-DIS-43 (a refused signature, moving to `RELISTED`) and R-DIS-40 (a bid at or above the floor) are not this story's either.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The sale is this service's: the agreed sale and the listing status are `asset_sale` and `listing` rows in `rwb_asset` | Ownership Map; Architecture v5 slide 41; TSD S5 T3.1 | AC2; TC-E4-025-02 |
| BR2 | The record precedes the change, one per outcome, with the rule and package version | DP-03; AC1, AC4 | AC1, AC4; TC-E4-025-01, -04 |
| BR3 | The floor, the approver's limit, the clocks and the lists are reference data or rule rows with a version; the parameters are the floor_price of listing, the approver's limit, the 2 working days of R-DIS-41 and the one-year appraisal age (X6); their parameter keys and the reference-data contract are Not specified in the source documents (DOR-RWB-S5-E4025-APP-20); DP-06 and DP-07 are not in the pattern set | TSD S5 T3.2; legacy Guardrails | AC7; TC-E4-025-11 |
| BR4 | The case move is answered, not written; the states are rwb-case's | Ownership Map (P3); GAP-2912 | AC2, AC3; TC-E4-025-02, -03 |
| BR5 | The bid amount and the signature have no column here; they are held where their owner names them and carried as the placeholder until then | TSD S5 T3.1; GAP-2913 | AC3; TC-E4-025-03 |
| BR6 | The appraisal and asset facts stay with rwb-source-data; no `v_ace_*` read here | DP-05; Architecture v5 slide 8 | AC5; TC-E4-025-09 |
| BR7 | The approval, its routing, the DoA levels and the limits are rwb-decision's and rwb-access's: named, never joined | DP-01; Ownership Map rows `approval` and `delegation_limit` | AC3; TC-E4-025-03 |
| BR8 | No event is published; EV-22 `AssetTakenOn` is the take-on story's | TSD S5 T5.3 | AC4; TC-E4-025-06 |
| BR9 | A repeated signal or key writes once, answers once and is counted | TSD S5 T-A.2 | AC6; TC-E4-025-10 |
| BR10 | No cross-schema join and no foreign key leaves `rwb_asset`; no personal data in a row, a record, a log or a workflow input | DP-01; TSD S5 T3.3; Template and Rules v1 §R7.2 (s17) | AC5; TC-E4-025-08, -09 |

### 9. State transitions

The case route state is rwb-case's and is applied by the parent `CaseWorkflow` on this story's answer (BR4).

| From (`listing` status) | Event | Condition | To |
|---|---|---|---|
| Live, bid received | `BID_BELOW_FLOOR` under R-DIS-41 | Bid amount below the floor | Live, the price unchanged; answer `SECOND_SIGNATURE_PENDING` |
| Live, bid received | `BID_BELOW_FLOOR` under R-DIS-41 | Floor under the approver's limit, or an appraisal more than a year old | Unchanged, held (X5, X6) |
| Live, bid received | `BID_AT_OR_ABOVE_FLOOR` under R-DIS-40 | Bid at or above the floor | Not this step (X4) |
| Live, second signature pending | `SECOND_SIGNATURE_GIVEN` under R-DIS-42 | A signature is present | `UNDER_OFFER`, answer `SALE_AGREED` |
| Live, second signature pending | `SECOND_SIGNATURE_REFUSED` under R-DIS-43 | No signature | Not this step (X7); the re-list story's |
| Any | The same signal again, or an unexpected state | BR9, X3 | Unchanged |

| Approval element | State | Meaning here |
|---|---|---|
| Second signature | Absent | No below-floor bid has been routed; the listing carries no approval reference |
| Second signature | Open | The approval item is with the level or the committee rwb-decision routed it to, inside its two-working-day clock |
| Second signature | Given | The signature is present; R-DIS-42 accepts the bid and agrees the sale |
| Second signature | Refused or expired | No sale; the refusal state is answered and the asset returns to the schedule through R-DIS-43 |

The statuses are the `LOV-LISTING` rows of TSD S5 T3.2; the route states are the DISPOSAL machine's (TSD S5 T4). `SALE_AGREED` is the answer to rwb-case under R-DIS-42, not a listing status, so it adds no value to `LOV-LISTING`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal C, R and U: reads the listing and the round, accepts the bid once the signature is given |
| RW-ENFORCE, RW-NPAMGR | Asset and disposal C and U within the disposal work; no approval right |
| RW-HEADNPA, RW-PRODHEAD | Asset and disposal RA: holds the approval the second signature is given at, in rwb-decision's queue |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL and the further roles of the read row | Asset and disposal R, in scope |
| PT-AUCTION, PT-RAMC | Asset and disposal R on their own listings |
| SY-CASEWF, SY-RULES, SY-AGENT | The matrix's right, under the same checks as a person |
| rwb-asset service identity | Runs the step; no foreign schema grant and no `v_ace_*` grant |

The rights are the rows of TSD S5 T6.1 and the legacy permission table, nothing wider. No role approves in this service: the approval is rwb-decision's, and this story only asks for it and reads its outcome. DP-08 is not in the pattern set: the right is declared per operation and the guard is a service-template capability. Each REST operation of §12 is checked against these rows by the rwb-access authorise check, whose name is Not specified in the source documents (DOR-RWB-S5-E4025-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | id, asset_id, listing_id, contract_date, sale_date, sale_price, transfer_fee, specific_business_tax, corporate_income_tax, gain_loss, incentive_amount | Write: the agreed sale |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Write: status |
| DF-COL-028 to DF-COL-042 (not in LDM v9; DOR-RWB-S5-E4025-APP-7) | asset (S5, `rwb_asset`; the ACE asset extension) | id, case_id, asset_ref, asset_type, transfer_in_type, book_value, holding_status and 8 more | Read |
| Not specified in the source documents (GAP-2913; ASM-4811) | listing (S5, `rwb_asset`) | `bid_amount` and the bidder of the round, as the rules name them | Not read until the owner names the column; `bid_amount` is not an LDM v9 field (DOR-RWB-S5-E4025-APP-7) |
| Not specified in the source documents (GAP-2913; ASM-4811) | approval (P7, `rwb_decision`) | `second_signature_by`, the approver and the decided-at time (the name is not an LDM v9 field, DOR-RWB-S5-E4025-APP-7) | Not read: rwb-decision's |
| Standard columns | asset_sale, listing (S5, `rwb_asset`) | state, version, created_at/by, updated_at/by, is_active | Write, with the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the library, before the change |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee and 5 more | Not read: rwb-source-data contract |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, transfer_in_type, from_segment, book_value and 7 more | Not read: rwb-source-data contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read: rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read or written: rwb-decision |

Field IDs follow TSD S5 T3.1 and the Logical Data Model and Data Dictionary v9; `v_ace_npa_sale`, `recovery_case`, `decision_log_entry` and `rule_row` carry the IDs of the legacy story's data table. **No new table, no column, no migration**: the tables come with the DB story, and `decision_record` and `idempotency_key` are library objects in `rwb_asset` (DP-03; PLT library, not a dictionary entity; neither name is an LDM v9 or Data Classification v5 field, DOR-RWB-S5-E4025-APP-7). **Personal data**: identifiers, codes, amounts, dates and a rule version; the bidder of the round is carried as a reference, never as a name, and its class is Not specified in the source documents (DOR-RWB-S5-E4025-APP-11); every fixture is synthetic.

### 12. Contract

The accept is declared as API-S5-005 of TSD S5 T-A.2; the conflict with the legacy endpoints table is recorded as GAP-2914 with ASM-4812 below. The posted fields are agreed at the tag.

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the shapes of RWB-S5-E4025-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out with title, listing, round price, floor and round number (API-S5-002) | Asset and disposal, R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | The same answer on the business key of the Ownership Map | Asset and disposal, R, scope applied | Not applicable |
| POST | `/listings/{listingId}/rounds` | AuctionRoundRequest in; AssetSale out for an accepted bid, 409 when the round or the listing is not in the state the write expects, 422 with MSG-S5-001 or MSG-S5-002 (API-S5-005) | Asset and disposal, U, scope applied | Idempotency-Key header |

The round write is declared once for two stories: the rounds story of RWB-E4-024 records the round and its bids, and this slice records the accepted bid and the sale it agrees. The legacy endpoints table of RWB-E4-025 names `POST /assets/{assetId}/listings` instead, and no source splits the accept from either write; the conflict is recorded as GAP-2914 with ASM-4812. Errors: 400 with Not specified in the source documents (CG-ALL-10047), 401 with Not specified in the source documents (CG-ALL-10047), 403 with MSG-P4-002, 404 with Not specified in the source documents (CG-ALL-10047), 409 with Not specified in the source documents (CG-ALL-10047), 422 with MSG-GEN-001, MSG-S5-001 or MSG-S5-002, and 503 when the decision library or a consumed contract does not answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| Appraisal and asset product (name Not specified in the source documents (GAP-2912; ASM-4810)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | Appraised value, date, outlier flag, book value with the freshness stamp; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state the rules check before they fire; faked |
| Case-move answer (name Not specified in the source documents (GAP-2912; ASM-4810)) | rwb-case (P3) | P3 rwb-case | `SECOND_SIGNATURE_PENDING` and `SALE_AGREED` with the rule and its version; on the workflow boundary it is the outcome the parent applies; faked |

One hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). The approval is not a consumed row: it is raised and answered on rwb-decision's queue over Temporal (§12.5).

#### 12.3 Events published

None. EV-22 `AssetTakenOn` is the take-on story's, and the agreed sale is announced to no consumer by this slice: no source names an `AssetSold` event (TSD S5 T5.3). A build that publishes here, or writes an outbox row, fails the absence test.

#### 12.4 Events consumed

None. The round, the bid, the second signature and the case state do not arrive as events: the round and the bid are this service's own rows and a signal of `AssetDisposalWorkflow`, the signature is the approval child's result, and the case state is the parent's. No subscription, no consumer group, no inbox row (DP-14).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one per case per stage, continues-as-new; workflow ID Not specified in the source documents (CG-ALL-10049); start rule Not specified in the source documents (CG-ALL-10049) | `rwb-asset` | Input: case, route, asset, listing, package in force; signals: the round and its bid, the second signature, the accepted re-appraisal |
| `assessBelowFloorBid` | Activity, R-DIS-41 | `rwb-asset` | Case, listing and bid in; rule IDs with versions, the approval request and the case move out, one transaction |
| `agreeSale` | Activity, R-DIS-42 | `rwb-asset` | Case, listing, bid and the given signature in; the sale reference, the rule with its version and the case move out, one transaction |
| `ApprovalWorkflow` (the workflow kit's approval) | Child workflow | rwb-decision (P7) | The approval item: the amount, the floor, the asset reference, the rule and its version, the level and the two-working-day clock of R-DIS-41 |

No second queue and no Schedule. The child runs on rwb-decision's queue because the approval, its routing and its record are P7's (BR7); the two activity names are a design choice of this story. The three consumed operation names are declared as `Not specified in the source documents (GAP-2912; ASM-4810)` for the rwb-source-data appraisal and asset read, the rwb-case case-state read and the case-move answer; they are built on their documented shapes and fakes on Day 1 and published by P1 and P3 at the tag of RWB-S5-E4025-CON. The approval item is raised by the `ApprovalWorkflow` child on rwb-decision's queue, its elements are a reference in the baseline, and no REST row is added for the request (GAP-2915; ASM-4813).

#### 12.6 Schedules

None. R-DIS-41's two-working-day clock is the approval's timer on rwb-decision's side and the stage's wait is a durable timer inside the workflow, so the step owns no Temporal Schedule and no Quartz job. The single Schedule of the service is JOB-19, the re-appraisal story's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The agreed sale: price, dates, fees, taxes and gain or loss |
| listing | S5 (`rwb_asset`) | Read; this story writes its status |
| decision_record | PLT library in `rwb_asset` | One record per outcome (DP-03) |
| idempotency_key | PLT library in `rwb_asset` | The key of the repeated signal or request |
| asset | S5 (`rwb_asset`), named only | The ACE asset extension of TSD S5 T3.1; read on the asset answer, never written here |

Entity groups of `rwb_asset` named here, with no physical table until the DB story (GAP-1752): the auction round, the bid and the holding-cost movement.

Not owned and never read as a table: `recovery_case`, `assignment`, `task`, `timer` (P3), `approval`, `delegation_limit`, `decision_log_entry`, `rule_row` (P7 and P4), `valuation` (S1), `document` (P5), `deviation` (S8), every `v_ace_*` view (P1). No bid table and no signature column is declared: the value stays Not specified in the source documents until its owner names it (GAP-2913; ASM-4811), and no foreign key leaves the schema (DP-01). The bid is held on the round row of the rounds story (RWB-E4-024) and the signature is read from the rwb-decision approval outcome; no column is added to `rwb_asset` for either.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data product fake | Appraisal `AP-2026-000541` of asset `AST-2026-000541` with its value, date and a clear outlier flag, plus the NPA asset book value; an appraisal more than a year old; a stale product; no answer inside 2 s | AC1, AC3, X6, X8, X9 |
| rwb-case state fake | `BID_RECEIVED` and `SECOND_SIGNATURE_PENDING` for the fixture cases; a case in another state | AC1 to AC3, X3 |
| rwb-case move fake | The two moves accepted; a move refused for a state the rule does not expect | AC2, AC3 |
| rwb-decision approval fake | An approval item open at the committee level with its clock; a given signature; a refused signature; an expired clock | AC1 to AC4, X7 |
| rwb-decision package fake | The DISPOSAL package at its version with R-DIS-41 and R-DIS-42 | AC1 to AC3 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| Composite route fake | The merged SCR-23 and SCR-21 answer for `RC-2026-000541` | AC1 |

Each fake answers only what its owner documents; the placeholder rows carry their gap until their owners confirm the names (GAP-2912; GAP-2915).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 2 consumed | The three asset reads and the round write on `/api/recovery/asset/v1`; the product read and the case state and case-move rows; one hop, 2 s |
| Kafka | 0 published, 0 consumed | Nothing is published; no subscription is added |
| Temporal | 1 workflow, 2 activities, 1 approval child | `AssetDisposalWorkflow`, `assessBelowFloorBid` and `agreeSale` on `rwb-asset`; the approval on rwb-decision's queue; no Schedule |
| File | None | No file crosses this step |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset.disposal`; front end `src/modules/recovery/asset/ListingAccept.tsx`, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is a prohibition (no `v_ace_*` grant, no ACE read); DP-03 is the transaction rule; DP-13 moves the base; DP-19 is how the screens reach the service. The package in force is loaded through the service template and the approval runs on the kit's template, neither of which adds an H row to this slice (GAP-2917; ASM-4815); the next realignment of the pattern set confirms this reading. The two consumed rows of P3 are class C and the plan's C row is None, so they are built on documents and fakes on Day 1 (GAP-2912).

| Component | Type | Responsibility |
|---|---|---|
| Below-floor branch of `AssetDisposalWorkflow` | Workflow | Waits on the timer and the signature, loads the package in force, reports to the parent |
| `assessBelowFloorBid`, `agreeSale` | Activities | Read, evaluate, write, answer |
| `BelowFloorEvaluator` / `SignatureEvaluator` | Services | R-DIS-41 on the amount and the floor; R-DIS-42 on the signature, the amount and the age of the appraisal |
| `SecondSignatureRequester` | Temporal client | Raises the approval child with the item and its clock; reads its outcome |
| `AssetDecisionRecordWriter` | Library adapter | One hash-linked record per outcome before any change (DP-03) |
| `SaleWriter` | Repository | `asset_sale` and the listing status in one transaction with the idempotency row and the lock |
| `CaseMoveAnswer`, `CaseStateClient`, `SourceDataProductClient` | Clients | The two moves and the two reads, one hop, 2 s |
| `AssetController` | Controller | The three reads and the round write, rights, key and the 400/401/403/404/409/422/503 map |
| `ListingAccept` | React component | The bid, the floor, the second-signature state and the agreed sale on SCR-23 |

**Database.** No Flyway file: tables from the DB story, library objects from the library's migration, no column for the bid and none for the signature (GAP-2913).

**Configuration.** The floor and the approver's limit, the two clocks and the `LOV-*` lists at their version; the DISPOSAL package from rwb-decision; the capability rows from rwb-access; the flag and the 2 s budget as platform configuration (ADR-020).

**Build steps.** (1) the below-floor branch and its input record; (2) `BelowFloorEvaluator` with the at-floor and held paths (AC3, X4 to X6); (3) `SecondSignatureRequester` against the approval fake (AC1, AC3, X7); (4) `SignatureEvaluator` and `SaleWriter` (AC2); (5) the record writer against the stub (AC4, X1); (6) the clients against their fakes (AC1, X8, X9); (7) `CaseMoveAnswer` (AC2, AC3); (8) `AssetController` (AC1); (9) the screen fragment (AC1); (10) the boundary test (X10, BR6, BR8).

**Feature flag.** `rwb.asset.below-floor-second-signature-v1`; off means the signal is held, nothing is written, no approval is raised and no move is answered.

**Done when.** §16 passes, a below-floor bid answers `SECOND_SIGNATURE_PENDING` in SIT on a live approval, a given signature agrees the sale and answers `SALE_AGREED`, a bid at the floor never reaches the step, a repeat writes once, a forced record failure changes nothing, no approval row and no `v_ace_*` read exists here, and the screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | The floor on the accepted bid is below the approver's limit (X5) | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | The appraisal is more than a year old at the accept (X6) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or a signal is absent or invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the right reads or writes (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the sale is agreed (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE product is stale after a late or failed batch (X9) | {product} is from {date}. Today's ACE batch has not arrived. |

The six IDs are the legacy and platform sets; the MSG-P1-001 text is taken from FSD P1 VR-P1-001-1; no other message is reworded and none is added.

### 15. Screens and states

SCR-23 Listing and price (draft, below limit, approved, published; empty, loading, error and no access: Not specified in the source documents (CG-ALL-10057)) and SCR-21 Asset list (loading, list; empty, error and no access: Not specified in the source documents (CG-ALL-10056)) are served through the gateway-bff route (DP-19), which calls rwb-asset for the asset, listing, round price and floor, rwb-case for the state and rwb-decision for the approval item. This story fixes the rwb-asset answers only; the route and the field list are RWB-PLT-N001-CON.

The states it produces are the second-signature state of SCR-23 — the bid, the floor, the gap, the approver level, the clock and the agreed sale — and the refusal, not-recorded, at-floor, old-appraisal, expired-signature and stale states with MSG-P4-002, MSG-P7-003, MSG-S5-001, MSG-S5-002 and MSG-P1-001. Draft, below-limit and approved are the pricing story's; the published ladder is RWB-E4-022's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-025-01 | AC1 | Component | Case `RC-2026-000541` with a live listing, a bid under the floor and the approval on its fake; records, approval request and move |
| TC-E4-025-02 | AC2 | Integration | Case `RC-2026-000542` at `SECOND_SIGNATURE_PENDING` with a given signature; the sale written and the move answered |
| TC-E4-025-03 | AC3 | Component | Case `RC-2026-000543` at `BID_RECEIVED` with a bid under the floor; the approval raised and the state answered |
| TC-E4-025-04 | AC4 | Component | Decision-record stub stopped; nothing written, MSG-P7-003 shown |
| TC-E4-025-05 | Access | Component | A role without the right; 403 with MSG-P4-002, no read and no write |
| TC-E4-025-06 | Principle 5 | Component | A forced record failure at the sale write; no row, no answer, no event |
| TC-E4-025-07 | §12 operations, events and activities | Component | Contract test: each operation, event and activity of §12 checked against the owner's published contract |
| TC-E4-025-08 | §12.7 tables (ASM-3438) | Component | Boundary test: each table of §12.7 written only by its owner schema; no foreign key and no cross-schema join |
| TC-E4-025-09 | AC5 (X10) | Component | A statement against a `v_ace_*` view, `recovery_case` or a foreign schema under the rwb-asset login; refused and the build fails |
| TC-E4-025-10 | AC6 (BR9) | Component | A repeated accept signal with one key; one record, one answer and the repeat counted |
| TC-E4-025-11 | AC7 (BR3) | Component | Floor and approver's limit at a version in reference data; evaluated at that version, none held in code |
| TC-E4-025-12 | AC8 (BR1 to BR10) | Component | Contract and boundary checks of each rule BR1 to BR10 against its owner's contract, with the boundary tests of TC-E4-025-08 and -09 |
| TC-E4-025-13 | AC9 | Component | Unauthenticated call (401), role without the right (403, as X2) and absent case (404) on a provided operation; no read and no write |
| TC-E4-025-14 | AC10 (BR9) | Component | Accept written under one idempotency key, then replayed with the same key; one decision record, the first answer returned and the replay counted |
| TC-E4-025-15 | AC11 (X8) | Component | Contract call that misses 2 s and an open breaker; retry on the workflow schedule and 503 answered |
| TC-E4-025-16 | AC12 | Component | Consumed call that fails or does not answer; nothing written, no move answered. Proposed test: Not specified in the source documents (NEWAC-RWB-S5-E4025-APP-AC10) |

The six legacy cases are kept in their order with the Level column added, and TC-E4-025-07 to -16 are the story's own, for §12, §12.7 and AC5 to AC12: TC-E4-025-02 runs `Integration` because it crosses the approval boundary, the rest `Component` on their fakes. The full text is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the floor, the approver's limit, the two clocks and the statuses stay reference data or rule rows with a version.
- No personal data in the schema, a workflow input or a log: the bidder is a reference; every fixture is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant, no ACE read (DP-05).
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row here (BR4).
- The approval stays with rwb-decision: no approval row, no DoA level and no limit is read or written here (BR7).
- One base, one topic, one queue and one login per service (DP-13, DP-14).
- No retired element returns: no shared job table, no Quartz row, no monolith base.
- The record precedes the change and the repeated signal is deduped (DP-03, BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| No requirement id for this slice | FEAT-AST-16 of the Epics 3 to 8 Specification v3 and FSD S5 A2.16: a bid under the floor is routed for a second signature before it can be accepted (GAP-2916; ASM-4814) | The below-floor branch, the approval request, the sale write and the two moves | TC-E4-025-01 to -04 | FEAT-AST-16 | Not specified in the source documents (DOR-RWB-S5-E4025-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-asset owns the sale and the listing status | TC-E4-025-02 | FEAT-AST-16 | Not specified in the source documents (DOR-RWB-S5-E4025-APP-2) |
| ADR-014 | Schema and login per service | `rwb_asset` and its login | TC-E4-025-06 | FEAT-AST-16 | Not specified in the source documents (DOR-RWB-S5-E4025-APP-2) |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable timer and the approval child; no Quartz row | TC-E4-025-01, -02 | FEAT-AST-16 | Not specified in the source documents (DOR-RWB-S5-E4025-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s | The two consumed rows | TC-E4-025-01, -03 | FEAT-AST-16 | Not specified in the source documents (DOR-RWB-S5-E4025-APP-2) |
| ADR-022 | Local decision record plus central ledger | The record before each change | TC-E4-025-04, -06 | FEAT-AST-16 | Not specified in the source documents (DOR-RWB-S5-E4025-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-025, Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word |
| Test cases | TC-E4-025-01 to TC-E4-025-06 |
| Feature and screens | FEAT-AST-16, SCR-23 and SCR-21 |
| Rules | R-DIS-41 and R-DIS-42, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |

### 19. Out of scope

- The shapes, the consumed rows, the record element, the error set and the fakes: RWB-S5-E4025-CON.
- The rounds, the bids and the award of the round: the rounds story of RWB-E4-024 and API-S5-005's round and bid rows (GAP-2914).
- The descending price schedule and the re-list at the next step: RWB-E4-022 and RWB-E4-026.
- A refused signature and the return of the asset to the schedule: R-DIS-43 and the re-list story of RWB-E4-026.
- The start price, the floor and the head of NPA's approval of the floor: FEAT-AST-11's story.
- The approval record, the DoA levels and limits, the routing and its escalation: rwb-decision (P7) and rwb-access (P4) (GAP-2915).
- The workflow kit's approval template and the rules kit: RWB-PLT-WF and the platform epics (GAP-2917).
- The purchase, the five-day payment term, the transfer and the proceeds: the sale, registration and proceeds stories of this service.
- The case, its states and the parent workflow: rwb-case (P3).
- The appraisal and asset facts and the freshness stamp: rwb-source-data (P1).
- The composite route and the screen field list: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards and the runbook: the operations story of this key.

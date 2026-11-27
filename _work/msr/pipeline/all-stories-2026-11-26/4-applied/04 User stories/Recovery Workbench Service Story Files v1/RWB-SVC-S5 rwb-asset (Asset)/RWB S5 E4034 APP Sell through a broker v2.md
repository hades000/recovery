# RWB-S5-E4034-APP Sell through a broker

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-034 split out for rwb-asset. The four legacy criteria are kept word for word with their origin tag; the broker route becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset` that opens the route with its fee and terms on a `listing` row of `rwb_asset`, evaluates R-DIS-24, R-DIS-25 and R-DIS-26 with the DISPOSAL package version in force, records the decision through the local decision-record library before any change (DP-03), instructs the broker through the rwb-partner `Partner.issueInstruction` activity, answers the case move to rwb-case and publishes no event of its own. The base becomes `/api/recovery/asset/v1` (DP-13) and SCR-21 and SCR-23 read through the gateway-bff composite route (DP-19). The legacy `v_ace_npa_sale` and `recovery_case` reads are retired as service reads because rwb-asset holds no ACE-view grant and no case-schema grant (DP-05). The broker fee and terms have no rule row and no column set; the instruction element, the case-move answer, the template price read and the auto-debit request have no published shape; the legacy feature is titled for the broker while two of its criteria are the buy-back and rental rules; the module event list gives one published event where the catalogue gives two; the rule package is pushed to four services and not to this one; and the plan carries no requirement id and no contract row for either slice (GAP-2967 to GAP-2971; ASM-4870 to ASM-4879). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4034-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S5-E4034-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-Z |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4034-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to open the broker route with its fee and its terms and to track it to the sale, with every route approval recorded against its rule version**, so that **a held asset leaves the books sooner through a broker at a price the bank approved instead of waiting for an auction ladder**.

This is the application slice of legacy RWB-E4-034. It owns the four legacy criteria of the key, the route step of `AssetDisposalWorkflow` on queue `rwb-asset` in namespace `rwb-recovery` as the stage child of `CaseWorkflow`, the evaluation of R-DIS-24, R-DIS-25 and R-DIS-26 with the DISPOSAL package version in force, the `listing` row that opens the route with its fee and terms, the broker instruction on rwb-partner's queue, the decision record written before any change, the answer to rwb-case for the moves `ROUTE_APPROVED_BUYBACK`, `RENTAL_ACTIVE` and `BROKER_INSTRUCTED`, and the two reads behind SCR-21 and SCR-23 on base `/api/recovery/asset/v1`.

It does not own the published shapes of RWB-S5-E4034-CON, the approval itself (`ApprovalWorkflow` and the `approval` row of rwb-decision), the case of record and its route states (rwb-case), the ACE sale and asset facts (rwb-source-data), the broker and its instruction row (rwb-partner), the template and its price (rwb-comms), the rental terms and the auto-debit as a build (RWB-S5-E4033-APP, with the money in rwb-payment), the sale, the proceeds and `AssetSold` (the sale and proceeds stories of this service), the publishing of the listing and the floor approval (FEAT-AST-11 and FEAT-AST-12 stories), or the deployment of this build (the operations story of this key).

### 2. Business rationale

The FSD keeps the objective and the metric unchanged: the broker route opens with its fee and terms and is tracked to the sale, and the NPA sales cycle read on the decision log and the Workbench records moves from 1,486 days to a target of 1,095 days, reviewed monthly (FSD S5 A2.25.1). The program keeps REQ-S5-010, a transfer to the asset management company, a buy-back and a rental each follow a recorded approval, and BR-030 of the Epics 3 to 8 BRD adds the broker sale to the same rule (Business Requirements Program v5; Business Requirements Epics 3 to 8 v1).

What D-RCV-60 changes is who owns the listing, the case, the broker, the template and the money. In the monolith one process held the route, the asset, the case row, the rule rows, the template and the decision log in one `recovery` schema. In the target the listing and its prices are this service's (`listing` and `asset_sale`, TSD S5 T3.1; Architecture v5 slide 41 gives rwb-asset "holdings, floor price, listings, auction rounds"), the case and its route states are P3's, the broker and its instruction are S9's, the template and its price are P6's, the auto-debit and the posting are P8's, and the rules, the approval and the rule rows are P7's. Every crossing becomes one contract: the case state and move, the template read, the auto-debit request, the package in force and the instruction activity.

One boundary is deliberate and recorded: this step publishes no event and consumes none. The take-on story owns `AssetTakenOn` and the sale story owns `AssetSold`, and the module event list that carries only the first is recorded against the catalogue (GAP-1942; ASM-4873). No business value moves: the fee, the term, the template price, the start and floor prices and the list values are route data, template data, reference data or rule rows read with their version, never a constant of this build.

### 3. Preconditions

- RWB-S5-E4034-CON is published: the two reads and the listing create with the `Listing` element and its closed lists, the round element, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes.
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-23 reach this service through the gateway-bff composite route, and no screen calls a service directly (DP-19).
- The rwb-case case state read and the case-move answer are available with their fakes. On the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2967; ASM-4870).
- The rwb-partner `Partner.issueInstruction` activity is declared on queue `rwb-partner` with its fake; the activity name is the one Architecture v5 gives, and the property list of its request and answer is Not specified in the source documents (GAP-2967; ASM-4870).
- The rwb-comms template read and the rwb-payment auto-debit request are available with their fakes; their operation names and the binding that carries the buy-back price are Not specified in the source documents (GAP-2967; ASM-4870).
- The DISPOSAL package is in force at its version with R-DIS-24, R-DIS-25 and R-DIS-26, authored and approved in rwb-decision (P7) and fetched here at the version in force, because no event pushes it to this service (GAP-1944; ASM-4874).
- The route approval is available as the `ApprovalWorkflow` child on `rwb-decision` with its fake; the `approval` row stays P7's.
- `listing`, `asset_sale` and `asset` exist in `rwb_asset` from the DB story of this service with the columns of TSD S5 T3.1 and the standard record columns; the additive broker fee and terms columns are that story's under DP-15, and this story adds no table, no column and no migration (GAP-2967; ASM-4879).
- The service runs as its own login on `rwb_asset`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_sale`, `rwb_case` or `rwb_partner` is refused by the database and fails the boundary test (DP-05; ASM-4872).
- The missing approval of the sources is recorded rather than waited on (GAP-2971; ASM-4876).

### 4. Flow

1. The case is in `ROUTE_WITH_APPROVER` on a held asset and the recommended route carries the broker option or one of the two other routes of this step's rules (FSD S5 A2.25; TSD S5 T4).
2. The route step of `AssetDisposalWorkflow` on queue `rwb-asset` starts on the stage trigger the parent `CaseWorkflow` forwards, reads the case state and the case reference on the rwb-case contract, read only, and waits on the `ApprovalWorkflow` child of rwb-decision for the approval answer.
3. `ListingRouteEvaluator` loads the DISPOSAL package at its version in force and evaluates the rule of the approved route: R-DIS-24 for `route = buy_back` with the second signature given, R-DIS-25 for `route = rental`, and R-DIS-26 for `route = broker` with an asset type in the two the rule names (Business Rules and Routing Logic v4).
4. The evaluation answers the rule ID, the package version, the action and the case move. Where no rule fires, the step changes nothing and reports the reason to the parent.
5. `BrokerTermsResolver` reads the fee and the terms of the route: the fee percentage or amount, its basis and its currency, the instruction term and the terms reference, as the approval and the governed route data give them. No source gives them a column set or a rule row, so they are read with their version and never as a constant (GAP-2967; ASM-4870).
6. On R-DIS-24, the buy-back terms are agreed at the template price read from rwb-comms with the template code, its language and its version; the price is the owner's data (GAP-2967; ASM-4870).
7. `RouteDecisionRecordWriter` writes one decision record through the local library **before any change**: case reference, asset reference, listing or route reference, rule ID with its version, approval reference, inputs reference, outcome, case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `ListingWriter` inserts the `listing` row in one `rwb_asset` transaction with the record and the idempotency row: `id` (DF-SAL-001), `asset_id` (DF-SAL-002), `sale_channel` (DF-SAL-003) set to `BROKER` of `LOV-SALE-CHANNEL` on this route, `start_price` (DF-SAL-004), `floor_price` (DF-SAL-005), `round_no` (DF-SAL-006), `listed_at` (DF-SAL-007) and `status` (DF-SAL-008) set to `DRAFT` of `LOV-LISTING`. The fee and terms go on the additive route columns, which are Not specified in the source documents (GAP-2967; ASM-4870).
9. `AssetHoldingWriter` sets `holding_status` (DF-COL-041) to `LISTED` of `LOV-HOLDING` in the same transaction, because a live listing puts the asset in the listed state (ASM-4878).
10. `PartnerInstructionClient` calls `Partner.issueInstruction` on queue `rwb-partner` with the instruction type, the partner reference, the asset and listing references and the fee and term; the worker of rwb-partner executes it and writes the `partner_instruction` row in `rwb_partner` (Architecture v5 slides 19 and 24). This service writes no partner row.
11. On R-DIS-25, the rental terms and the auto-debit are set on the route and requested from rwb-payment; the rental build itself is RWB-S5-E4033-APP's on the same step, and this story answers the move from the outcome that step writes (GAP-2968; ASM-4871).
12. `CaseMoveAnswer` answers rwb-case with `ROUTE_APPROVED_BUYBACK`, `RENTAL_ACTIVE` or `BROKER_INSTRUCTED`, the rule ID, its version and the decided-at time; rwb-case writes the case row and its route state (ASM-4877).
13. The step tracks the listing it opened: the rounds under element API-S5-005, the status of `LOV-LISTING`, and the broker result and term of R-DIS-64 and R-DIS-65, up to the sale; the `asset_sale` row, the proceeds and `AssetSold` are the sale story's.
14. A repeated approval with the same case, route and listing reference writes nothing, issues no second instruction and counts the repeat.
15. SCR-21 and SCR-23 read the asset, its listing and its status from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no listing row, no holding change, no instruction and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E4-034-04, TC-E4-034-06 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes, no instruction is issued and no record is written | MSG-P4-002 | AC1, TC-E4-034-05 |
| X3 | The route is not approved, or the approval is not the one the rule expects | 409 and nothing is written; the step reports the state to the parent and the case keeps its state | None | AC2, AC3 |
| X4 | The rwb-comms template is not in force, or its version is not the one the buy-back terms name | The buy-back route holds and writes nothing; the officer sees the template reference and the missing version | MSG-GEN-001 | AC2 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow schedule inside the Temporal budget; nothing is written and no move is answered | None | AC1, AC2, AC3 |
| X6 | No rule of the DISPOSAL package fires on the approved route | Nothing changes, no record is written, no instruction is sent and the case keeps its state | None | AC1, AC2, AC3 |
| X7 | A listing already exists for the case, the asset and the route reference | One row, one instruction and one answer; the repeat is counted and no second record is written | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `partner_instruction` row or another schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17, BR1, BR3, BR5 |

X1 to X4 are the paths of the legacy key carried onto the split, X5 to X7 are the paths the target call types and the broker instruction add, and X8 is the DP-01 and DP-05 boundary. The fee, the term and the template price are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E4034-CON, the rwb-case, rwb-partner, rwb-comms and rwb-payment fakes, the approval fake and the record stub, on its own schema, and needs no live P3, P6, P7, P8 or S9 |
| Negotiable | The activity name of the step, the decision code per rule, the shape of the stage outcome and the ordering of the instruction inside the transaction are this story's choice; the rules, the messages, the screens, the listing columns and the closed lists are fixed |
| Valuable | A held asset is offered through a broker with an approved fee and term on the day the route is approved, and the case moves in the service that owns it |
| Estimable | One workflow step, one evaluator, one terms resolver, one record write, one listing insert, one holding update, one instruction, one case-move answer, three clients and two read-only screen fragments |
| Small | Two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and route data through the fakes, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Sell through a broker

  Background:
    Given case "RC-2026-000534" holds asset "AST-2026-000534" with listing "LS-2026-000534" not yet opened
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-24, R-DIS-25 and R-DIS-26
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Sell through a broker (legacy RWB-E4-034 AC1)
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for "RC-2026-000534"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the broker route with its fee and terms, and tracks it to the sale
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-24 (legacy RWB-E4-034 AC2)
    Given the rwb-case contract mock returns the case state "ROUTE_WITH_APPROVER" for "RC-2026-000534"
    Given the rwb-comms contract mock returns the buy-back template at its price
    Given a case in state ROUTE_WITH_APPROVER
    When route approved
    Then agree the buy-back terms at the template price
    Then the case moves to ROUTE_APPROVED_BUYBACK

  Scenario: AC3 Rule R-DIS-25 (legacy RWB-E4-034 AC3)
    Given the rwb-case contract mock returns the case state "ROUTE_WITH_APPROVER" for "RC-2026-000534"
    Given the rwb-payment contract mock returns the auto-debit set for the case
    Given a case in state ROUTE_WITH_APPROVER
    When route approved
    Then set the rental terms and the auto-debit, and hold the asset as rented
    Then the case moves to RENTAL_ACTIVE

  Scenario: AC4 Not recorded (legacy RWB-E4-034 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E4-034 word for word, with their origin tag added: the repetition of `Then`, and the legacy wording of `the user acts on the screen`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so the `Given the <service> contract mock returns <x>` lines are the only additions, and every value of the legacy lines is kept. What they describe happens in four places: rwb-case answers the state and applies the move, rwb-comms answers the template and its price, rwb-payment answers the auto-debit, rwb-partner executes the instruction and writes its own row, and this story evaluates the rules, records the decision, writes the listing, sets the holding status and answers the move.

Two notes are recorded rather than smoothed over. First, the feature is titled for the broker route while two of its four criteria are the buy-back rule R-DIS-24 and the rental rule R-DIS-25; the broker rule R-DIS-26 has no criterion of its own beyond AC1, so this step owns all three routes of one disposal step (GAP-2968; ASM-4871). Second, R-DIS-25 is the criterion legacy RWB-E4-033 also carries; each APP story owns its own copy, the rental build is RWB-S5-E4033-APP's, and R-DIS-24 is carried by this legacy key alone because FEAT-AST-23's criteria test R-DIS-66 (GAP-2968; ASM-4871).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-24 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = buy_back and second_signature given | Agree the buy-back terms at the template price | ROUTE_APPROVED_BUYBACK | Sale officer | Calculation Service, Case Workspace | None |
| R-DIS-25 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = rental | Set the rental terms and the auto-debit, and hold the asset as rented | RENTAL_ACTIVE | Sale officer | ATS | None |
| R-DIS-26 | Asset disposal | D8.1 to D8.3 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | route = broker and asset_type in (commercial_property, land) | Instruct the broker on the portal for a fixed term | BROKER_INSTRUCTED | Broker | Partner Portal | per instruction term |
| R-DIS-64 | Asset disposal | D8.1 to D8.3 | BROKER_INSTRUCTED | BROKER_SOLD | sale price at or above the approved floor | Complete the sale and pay the broker fee on acceptance | SALE_AGREED | Sale officer | Partner Portal, ALS core and GL | None |
| R-DIS-65 | Asset disposal | D8.1 to D8.3 | BROKER_INSTRUCTED | BROKER_TERM_EXPIRED | instruction_term passed and no sale | Withdraw the instruction and review the route | ROUTE_RECOMMENDED | Sale officer | Partner Portal | None |

The five rows are the rows of the Business Rules and Routing Logic v4, copied character for character; the FSD S5 A2.25.3.1 names the first three of them for FEAT-AST-25. The owner column is a business role and not a service: the moves are written by rwb-case on this story's answer, the listing and its terms are written here, the template price is read from rwb-comms, the auto-debit, the rent and the fee posting are rwb-payment's, and the instruction and its term are rwb-partner's. R-DIS-24, R-DIS-25 and R-DIS-26 are the rules the criteria test; R-DIS-64 and R-DIS-65 are tabled because AC1 tracks the route to the sale, and neither carries a criterion of this key (GAP-2968; ASM-4871). R-DIS-26 carries no fee and no term, so the fee and the terms are route data (GAP-2967; ASM-4870).

| ID | Rule | Source |
|---|---|---|
| BR1 | The listing is this service's: its identifier, asset link, sale channel, prices, round, listed date and status are columns of `listing` in `rwb_asset`, and no other service writes them | Architecture v5 slide 41; Ownership Map (`listing`, `asset_sale` owner S5); TSD S5 T3.1 |
| BR2 | The decision is recorded before the listing changes, with the rule ID, the package version in force and the approval reference; a failed write changes nothing and shows MSG-P7-003 | DP-03; TSD S5 T2; legacy AC1 and AC4 |
| BR3 | The ACE sale and asset facts stay with rwb-source-data: no `v_ace_*` view and no ACE table is read here | DP-05; ASM-4872 |
| BR4 | The case move is answered and not written: `recovery_case` and every route state are rwb-case's, and the move carries the rule and its version | Ownership Map (`recovery_case` owner P3); ASM-4877 |
| BR5 | The broker instruction is rwb-partner's: the step calls the `Partner.issueInstruction` activity on queue `rwb-partner`, and this service holds no grant on `rwb_partner` | Architecture v5 slides 19 and 24; Ownership Map (`partner_instruction`, `partner` owner S9) |
| BR6 | The route approval is rwb-decision's: the `ApprovalWorkflow` child and the `approval` row are P7's and are consumed as a signal, never as a row | Architecture v5 slides 19 and 24; Ownership Map (`approval` owner P7) |
| BR7 | The template price is rwb-comms' data, read on the owner's contract with its template version; no price, fee or term is a constant or a default of this build | Ownership Map (`template` owner P6, DF-REF-045 to DF-REF-051); FSD S5 BR-S5-025 |
| BR8 | The money stays with rwb-payment: the auto-debit, the rent charge, the fee posting and the proceeds are P8's, and this story requests them and posts nothing | Ownership Map (`proceeds` owner P8); Architecture v5 slide 13 S5 row |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset`; `asset_id`, `case_id` and every partner reference are other services' identifiers | DP-01; TSD S5 T3.3 |
| BR10 | Every value a business person may change is reference data, template data or a rule row read with its version: `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING`, `LOV-ASSET-TYPE`, the fee, the term and the DISPOSAL package | TSD S5 T3.2; FSD S5 BR-S5-025; legacy Guardrails |
| BR11 | No event is published by this step: `AssetTakenOn` is the take-on story's and `AssetSold` the sale story's | Architecture v5 slides 19 OUT and 43; TSD S5 T5.3; GAP-1942 |
| BR12 | No person name, address, contact value or identity number enters `rwb_asset`, the record, a log, an instruction or a workflow input | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case route state is rwb-case's and is not changed here: the step answers the move and the parent applies it (BR4). What this story owns is the listing status, the holding status of the asset and the state of the step.

| From (`listing.status`) | Event | Condition | To |
|---|---|---|---|
| None, no row | The broker route approved under R-DIS-26 | route = broker and asset_type in the two the rule names | A row in `DRAFT`, answer `BROKER_INSTRUCTED` |
| `DRAFT` | The listing published by the publishing story | The floor is the approved one | `LIVE`, with `asset.holding_status` `LISTED` |
| `LIVE` | A bid or an offer under API-S5-005 | A bid or an offer is recorded | `UNDER_OFFER` |
| `UNDER_OFFER` | The sale recorded by the sale story | R-DIS-64, at or above the approved floor | `SOLD`, with `holding_status` `SOLD` |
| `LIVE`, `UNDER_OFFER` | The route refused or withdrawn (R-DIS-27, R-DIS-65) | approver_decision = refused, or the instruction term passed | `WITHDRAWN`, asset back to `HELD` |
| Any | The decision record cannot be written | X1 | Unchanged |
| None, no row | A route that fires no rule | X6 | No row, no record, no instruction, no answer |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The stage trigger arrives for a case in `ROUTE_WITH_APPROVER` | The package in force is loaded | Evaluating |
| Evaluating | The rule of the approved route fires | The fee, the terms or the template price resolve | Recording |
| Recording | The record is written | The write commits | Applying |
| Applying | The listing, the holding change, the instruction and the answer commit | The transaction succeeds | Tracking |
| Tracking | The sale is recorded by the sale story | The listing is `SOLD` | Waiting for the next route |
| Applying, Recording | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The route is not approved, or no rule fires | X3, X6 | Waiting, nothing changed |

The route states are those of the DISPOSAL machine (TSD S5 T4) and of the three rules, and they live on the case of record. The listing values are `LOV-LISTING` and the holding values `LOV-HOLDING` (TSD S5 T3.2); the legacy SCR-23 states do not map one to one onto `LOV-LISTING`, and the mapping is recorded (ASM-4878).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA (TSD S5 T6.1): the primary role, holding C on the listing create, R on the reads and A on the approval path |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the asset and its listing and corrects the route facts |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the asset, its listing and its route outcome |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal RA: read, and approve through the approval path |
| The Broker role of R-DIS-26 | The partner side only, through the partner gateway of rwb-partner: the broker sees its own instruction and answers it, never the decision, the case state or an internal row |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal RU or R as TSD S5 T6.1 gives it: the partner sees its own assets, never the route decision |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives: the service identities run the step under the same checks |
| rwb-asset service identity | Runs the step, evaluates the rules, writes the record, the listing and the holding change, calls the instruction and answers the move; no grant outside `rwb_asset` |

The rights are the rows of TSD S5 T6.1 and nothing wider, with the Broker role the R-DIS-26 owner column names and the partner-side scope of the partner gateway. DP-08 is not in this story's pattern set, so the capability area and the right are declared per operation and the guard is a service-template capability: the check is stated here and not built here. The two legacy asset paths carry right R and right C, and the same rights hold on the paths this story serves (ASM-4872).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-001 | listing (S5, `rwb_asset`) | id | Write, the listing reference of the row, the instruction and the answer |
| DF-SAL-002 | listing (S5, `rwb_asset`) | asset_id | Write, the identifier of this service's asset row |
| DF-SAL-003 | listing (S5, `rwb_asset`) | sale_channel | Write, against `LOV-SALE-CHANNEL` (`BROKER` on this route) |
| DF-SAL-004 | listing (S5, `rwb_asset`) | start_price | Write, the approved start price of the route |
| DF-SAL-005 | listing (S5, `rwb_asset`) | floor_price | Write, the approved floor price of the route |
| DF-SAL-006 | listing (S5, `rwb_asset`) | round_no | Write, the first round of the listing |
| DF-SAL-007 | listing (S5, `rwb_asset`) | listed_at | Write, the time the route was opened |
| DF-SAL-008 | listing (S5, `rwb_asset`) | status | Write, against `LOV-LISTING` (`DRAFT`) |
| DF-COL-041 | asset (S5, `rwb_asset`) | holding_status | Write, against `LOV-HOLDING` (`LISTED`); `SOLD` and `TRANSFERRED` are the sale story's |
| DF-COL-031, DF-COL-033, DF-COL-037 | asset (S5, `rwb_asset`) | asset_ref, asset_type, book_value | Read, to place the listing and the route |
| The broker fee and terms | asset_sale or listing (S5, `rwb_asset`) | the fee, its basis and currency, the instruction term and the terms reference | Write on the additive route columns; their table and columns are Not specified in the source documents (GAP-2967; ASM-4870) |
| DF-SAL-009 to DF-SAL-019 | asset_sale (S5, `rwb_asset`) | contract date, sale date, sale price, transfer fee, taxes, gain or loss, incentive | Not written here: the sale story inserts the row and this step tracks it |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, approval reference, inputs reference, outcome, decided at | Write through the library, before the listing row changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule id, rule version, route set, from state, event code and the rest | Not read as a table: the rules arrive with the DISPOSAL package |
| DF-REF-045 to DF-REF-051 | template (P6) | template code, version, language, product group, body reference, price | Not read as a table: the template and its price arrive on the rwb-comms contract |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, npa_asset_key, contract date, sale date, sale price, transfer fee and the rest | Not read: no `v_ace_*` grant (BR3) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, status, stage_code, route state | Not read as a table: the state and the move arrive on the rwb-case contract |

Field IDs are those of TSD S5 T3.1 and T3.2 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `listing`, `asset_sale` and `asset` arrive with the DB story, this story writes the eight columns of `listing`, one column of `asset` and the route's fee and terms columns that the DB story adds under DP-15, and `decision_record` and `idempotency_key` are library objects created in `rwb_asset` by the library's migration (DP-03; ASM-4879). The five entities of the legacy Data table belong to other owners in the target: `recovery_case` to P3, `v_ace_npa_sale` to P1, `decision_log_entry` and `rule_row` to P7 and `template` to P6 (GAP-2969; ASM-4872).

**No personal data.** The rows carry identifiers, codes, amounts, dates and a rule version; no name, address, contact value or identity number enters `rwb_asset`, the record, a log, an instruction or a workflow input, and every fixture is synthetic. The broker, its users and its panel data are S9's rows and are referenced by identifier only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the reads and the listing create whose shapes RWB-S5-E4034-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetKey}` | Asset of status 200 out, with title, condition, valuations, costs and listing references | Asset and disposal, right R, scope applied | Not applicable |
| POST | `/assets/{assetKey}/listings` | `ListingRequest` in, `Approval` out of status 201 or 202 | Asset and disposal, right C, scope applied | `Idempotency-Key` required |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 409 when the route is not the one the rule expects, 422 with MSG-GEN-001, and 503 when the library or a consumed contract does not answer. The operation IDs are those of TSD S5 appendix T-A.1. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's and is not declared here. `POST /listings/{listingId}/rounds` (API-S5-005) is this service's but its behaviour is the auction stories'; this step records the first round number and runs no round. The two asset paths carry the business-key form the later API versions use, while the Ownership Map and TSD S5 T-A.1 keep the asset-id form, and the difference is recorded (GAP-2969; ASM-4872).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the product group; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2967; ASM-4870)) | `/api/recovery/case/v1` | P3 rwb-case | The answer that carries `ROUTE_APPROVED_BUYBACK`, `RENTAL_ACTIVE` or `BROKER_INSTRUCTED` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The template read of R-DIS-24 (operation name Not specified in the source documents (GAP-2967; ASM-4870)) | `/api/recovery/comms/v1` | P6 rwb-comms | The template code, its language, its version and the price; faked |
| The auto-debit request of R-DIS-25 (operation name Not specified in the source documents (GAP-2967; ASM-4870)) | `/api/recovery/payment/v1` | P8 rwb-payment | The auto-debit set for the case against the rental terms; faked |
| The package in force (operation name Not specified in the source documents (GAP-1944; ASM-4874)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DISPOSAL package at its version in force with R-DIS-24, R-DIS-25 and R-DIS-26; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because the C row of both slices is None (GAP-2967, GAP-1944; ASM-4870, ASM-4874). The broker instruction is not a REST row: it is the Temporal activity of 12.5.

#### 12.3 Events published

None. This step publishes no event of its own. `AssetTakenOn` belongs to RWB-S5-E3019-APP and `AssetSold` to the sale story that records the sale, so this step writes no outbox row and `rwb.asset.events.v1` is not used by this build. TSD S5 T5.3 names `AssetTakenOn` as the module's only published event and omits `AssetSold`, which Architecture v5 slides 19 and 43 carry, and the difference is recorded rather than resolved here (GAP-1942; ASM-4873).

#### 12.4 Events consumed

None. The step is triggered by the stage trigger the parent forwards and by the approval answer of the `ApprovalWorkflow` child, not by an event: Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none is the route approval. The broker result arrives as the answer of the activity it calls, and `PartnerResultSubmitted` on `rwb.partner.events.v1` is consumed by the tracking and sale stories, not at this step. This story holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the asset reference, the approval reference and the package in force; signals: the approval answer, the case state and the package version |
| `openBrokerRoute` | Activity, the route step of this story | `rwb-asset` | The case, the approved route and the asset in; the rule ID with its package version, the listing reference, the instruction reference and the case move out, with the record, the listing row and the holding change in one transaction |
| `Partner.issueInstruction` | Activity, rwb-partner's, called by this step | `rwb-partner` in namespace `rwb-recovery` | The instruction type, the partner reference, the asset and listing references, the fee and the term in; the instruction reference and the issued-at time out; the property list is Not specified in the source documents (GAP-2967; ASM-4870) |

The name `Partner.issueInstruction` is the one Architecture v5 slides 19 and 24 give, and the call pattern is the one slide 24 describes: the workflow calls the activity on rwb-partner's queue, its worker executes it and writes its own schema. The name `openBrokerRoute` is a target design choice that no source fixes (ASM-4879). No child workflow for the case and none for the money exists in this service; the approval child runs on rwb-decision.

#### 12.6 Schedules

None. The step runs from the stage trigger and the approval answer and owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP (Architecture v5 slide 44). The R-DIS-26 timer "per instruction term" is a timer of the instruction in rwb-partner and of the workflow's own wait, not a Schedule of this service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| listing | S5 (`rwb_asset`) | The offer of the asset with its channel, prices, round and status; this story inserts the row |
| asset_sale | S5 (`rwb_asset`) | The sale row, inserted by the sale story; this step writes the broker fee and terms on its additive columns and reads the row to track the sale |
| asset | S5 (`rwb_asset`) | The held asset; this story writes `holding_status` only |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated approval and the answer it holds |

Not owned and never read as a table: `recovery_case` and `task` (P3), `collateral` and every `v_ace_*` view (P1), `document` (P5), `template` and `notice` (P6), `proceeds` (P8), `decision_log_entry`, `rule_row` and `approval` (P7), `partner_instruction` and `partner` (S9). No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | The states `ASSET_HELD`, `ROUTE_WITH_APPROVER` and the three states the moves produce for case `RC-2026-000534`; a case not in the state the rule expects | AC1, AC2, AC3, X3 |
| rwb-case case-move fake | The three moves accepted, and a move refused because the case is not in the expected state | AC2, AC3, X3 |
| rwb-comms template fake | The buy-back template at its version with its price and language; a version not in force | AC2, X4 |
| rwb-partner instruction fake | The instruction accepted with its reference and issued-at time; an instruction refused because the partner is not on the panel; no answer beyond 2 s | AC1, X5 |
| rwb-payment auto-debit fake | The auto-debit set for case `RC-2026-000534` with its mandate reference; no answer beyond 2 s | AC3, X5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with the three rules | AC1, AC2, AC3, X6 |
| rwb-decision approval fake | The `ApprovalWorkflow` answer approved with its reference, and an approval refused or returned | AC1, AC2, AC3, X3 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000534` | AC1 |

The fakes are test-only and are replaced in SIT. The operation names of the case-move answer, the template read, the auto-debit and the package read, and the property list of the instruction, carry the placeholder until their owners confirm them (GAP-2967, GAP-1944; ASM-4870, ASM-4874).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 5 consumed | The two reads and the listing create on `/api/recovery/asset/v1`; the case read and move answer, the template read, the auto-debit request and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | This step writes no outbox row and subscribes to nothing; the record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 2 activities, one of them rwb-partner's | `AssetDisposalWorkflow`, `openBrokerRoute` and `Partner.issueInstruction`; the approval child on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `brokerroute`, Java package `th.co.scb.ace.workbench.recovery.asset.brokerroute`; front end `src/modules/recovery/asset/ListingAndPrice.tsx`, the fragment SCR-23 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: no `v_ace_*` grant, no ACE view and no ACE table is read (ASM-4872). DP-03 is the transaction rule of the step. DP-13 moves the base of the three operations and nothing else. DP-19 is how SCR-21 and SCR-23 reach this service, one hop through the gateway.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` route branch | Workflow | Waits for the approval, loads the package in force, calls the step and reports the outcome to the parent |
| `openBrokerRoute` | Activity | Reads the case and the approval, evaluates the rule, resolves the fee, the terms and the template price, writes the record, the listing and the holding change, instructs the broker, answers the move |
| `ListingRouteEvaluator` | Service | The rule evaluation for R-DIS-24, R-DIS-25 and R-DIS-26 against the package version in force, with the closed lists |
| `BrokerTermsResolver` | Service | The fee, its basis and currency, the instruction term and the terms reference, read as route data with its version; it writes no default |
| `RouteDecisionRecordWriter` | Library adapter | Writes the record with the rule and version before any change and refuses the step when the write fails (DP-03) |
| `ListingWriter` | Repository | Inserts `listing` and writes its eight columns in one transaction, with the idempotency row and the optimistic lock |
| `AssetHoldingWriter` | Repository | Sets `holding_status` of `asset` in the same transaction |
| `PartnerInstructionClient` | Temporal client | Calls `Partner.issueInstruction` on `rwb-partner`, one hop, 2 s budget and breaker |
| `TemplateClient` | Client | The rwb-comms template read with its version and price |
| `AutoDebitClient` | Client | The rwb-payment auto-debit request of R-DIS-25 |
| `CaseStateClient` | Client | The case state read and the case-move answer |
| `ListingController` | Controller | The two reads and the listing create, the right, the `Idempotency-Key` rule and the problem mapping 400 to 503 |
| `ListingAndPrice` | React component | Shows the listing, its price, its status and the refusal and failure states on SCR-23, read only |

**Database and migrations.** No Flyway file. `listing`, `asset_sale` and `asset` arrive with the DB story, the additive fee and terms columns are that story's under DP-15, and the record and idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03; ASM-4879).

**Configuration.** `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING` and `LOV-ASSET-TYPE` at their version (TSD S5 T3.2); the DISPOSAL package at its version in force with R-DIS-24, R-DIS-25 and R-DIS-26, fetched from rwb-decision (GAP-1944; ASM-4874); the fee, the term and the template price as data of the route, the template and the package; the capability area "Asset and disposal" and its rights as access rows of rwb-access; the 2 s budget and the single hop as ADR-020.

**Build steps**

1. The route branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child, with the approval answer as trigger.
2. `CaseStateClient` and the approval fake, with the budget, the breaker and the state paths (AC1, AC2, AC3, X3).
3. `ListingRouteEvaluator` with the three rules and the no-fire path (AC1, AC2, AC3, X6).
4. `BrokerTermsResolver`, `TemplateClient` and the fee, term and price reads, with the template-not-in-force path (AC1, AC2, X4).
5. `RouteDecisionRecordWriter` against the stub, with the failed-write path (AC4, X1).
6. `ListingWriter` and `AssetHoldingWriter` with the one transaction, the eight columns, the holding change, the idempotency row and the optimistic lock (AC1, X7).
7. `PartnerInstructionClient` and the instruction on `rwb-partner` (AC1).
8. `AutoDebitClient` and the R-DIS-25 path through the sibling story (AC3).
9. `CaseMoveAnswer` and the parent signal with the three moves (AC2, AC3).
10. `ListingController` and `ListingAndPrice` with the rights, the `Idempotency-Key` rule and the composite route fake (AC1).
11. The boundary test: nothing outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_case`, `rwb_partner`, `rwb_comms`, `rwb_payment` or `rwb_decision` (X8, BR3, BR5).

**Feature flag.** `rwb.asset.broker-route-v1`; off means the step holds the approval, writes nothing, issues no instruction and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of §16 pass, the step runs from a synthetic approved route, each of the three rules produces its record, its listing or terms outcome, its instruction and its move, a repeated approval writes once, a forced record failure changes nothing, no `recovery_case` row, no `partner_instruction` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-23 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy set of this key; it names the floor and the approval limit, which are the pricing story's, so no path here raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy set; it names the age of an appraisal, which is the re-appraisal story's, so no path here raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of the route, the listing or the template reference is absent or invalid (X4, X6) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset or the listing, or creates a listing (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the listing row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five IDs are the legacy message set of RWB-E4-034, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this story raises them. The refusal of FSD S5 A2.25.4.3 is the same MSG-P4-002 and the same MSG-P7-003, and no separate FSD message is added.

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-23 Listing and price in its draft, below-limit, approved and published states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its listing, rwb-case for the case and its route state, rwb-valuation for the valuation the floor is set against and rwb-partner for the instruction reference; this story fixes the rwb-asset answers only, and the route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the listing states of SCR-23 — the offer opened, its start and floor price, its channel, its round and its status — and the refusal and failure states it shows: refused with MSG-P4-002, not recorded with MSG-P7-003, field invalid with MSG-GEN-001. The legacy states "Draft; below limit; approved; published" are business conditions of the pricing and approval stories rather than values of `LOV-LISTING`, which carries `DRAFT`, `LIVE`, `UNDER_OFFER`, `SOLD` and `WITHDRAWN`; the below-limit and approved conditions are shown from the approval answer and the floor check, not as new list values (ASM-4878).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-034-01 | AC1 | Component | Case `RC-2026-000534` holding asset `AST-2026-000534` with an approved broker route; the listing row, the holding status, the instruction and the record asserted on the fakes |
| TC-E4-034-02 | AC2 | Integration | Case `RC-2026-000534` at `ROUTE_WITH_APPROVER` with `route = buy_back` and the second signature given; the template price and the `ROUTE_APPROVED_BUYBACK` move asserted end to end on the fakes |
| TC-E4-034-03 | AC3 | Integration | Case `RC-2026-000534` at `ROUTE_WITH_APPROVER` with `route = rental`; the rental terms, the auto-debit and the `RENTAL_ACTIVE` move asserted end to end on the fakes |
| TC-E4-034-04 | AC4 | Component | The record stub stopped; nothing written, no instruction issued and MSG-P7-003 shown |
| TC-E4-034-05 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read and no write |
| TC-E4-034-06 | Principle 5 | Component | A forced decision log write failure at the moment of the listing insert; no row, no holding change, no instruction and no answer |

The six legacy cases are the legacy cases of RWB-E4-034 in their legacy order, with the Level column added: the cases that stay inside the step on its fakes map to `Component`, and TC-E4-034-02 and TC-E4-034-03 map to `Integration` because they cross the rwb-comms and rwb-payment boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the fee, its basis and currency, the instruction term, the template price, the start and floor prices, the list values and the rule rows stay route data, template data, reference data or the package, never a constant, a default or a branch.
- No personal data in `rwb_asset`, in an instruction, a workflow input or a log: identifiers, codes, amounts, dates and a rule version only; fixtures are synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant and no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case, the broker with rwb-partner, the template with rwb-comms and the money with rwb-payment: no `recovery_case`, `partner_instruction`, `template` or posting row is written here (BR4, BR5, BR7, BR8).
- The decision is recorded before the change and the step writes nothing outside its one transaction; a build that issues the instruction before the record commits fails the review (DP-03).
- One base, one topic, one queue and one login per service; no document or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no second event on the topic and no Schedule for the instruction term.
- No new event is invented: `AssetSold` is the sale story's and `AssetTakenOn` the take-on story's, and this step writes no outbox row (BR11).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval (Business Requirements Program v5; BR-030 of the Epics 3 to 8 BRD adds the broker sale; FSD S5 requirements served); the broker route has no requirement text of its own, the split plan carries no requirement id for this slice, and the absence is named rather than filled (GAP-2968, GAP-2970; ASM-4871, ASM-4875) | The route step, the record, the listing and the case-move answer | TC-E4-034-01, TC-E4-034-02, TC-E4-034-03, TC-E4-034-04 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the listing and the route step | TC-E4-034-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login, with no grant on another schema | TC-E4-034-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows and the instruction activity with their budget | TC-E4-034-02, TC-E4-034-03 |
| ADR-022 | Local decision record plus central ledger | The record written before the listing change | TC-E4-034-04, TC-E4-034-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-034, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E4-034-01 to TC-E4-034-06 |
| Feature and screens | FEAT-AST-25, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-24, R-DIS-25 and R-DIS-26 tested; R-DIS-64 and R-DIS-65 tabled for the tracking of the sale; all governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the reads and the listing create, the `Listing` element with its fee and terms properties and its closed lists, the round element, the consumed rows, the error set and the fakes: RWB-S5-E4034-CON.
- The approval itself, the `ApprovalWorkflow` child and the `approval` row: rwb-decision (P7) (BR6).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this story consumes and fakes (ASM-4877).
- The broker, its panel, its users and its instruction and result rows: rwb-partner (S9) (BR5).
- The template, its text, its merge fields and its price: rwb-comms (P6) (BR7).
- The auto-debit, the rent charge, the fee posting and the proceeds: rwb-payment (P8), with the rental terms themselves built by RWB-S5-E4033-APP (BR8).
- The sale, the `asset_sale` row as a build, the proceeds application and the `AssetSold` event: the sale and proceeds stories of this service (GAP-1942).
- The ACE NPA sale and asset facts and the freshness of the data product: rwb-source-data (P1) (BR3).
- The publishing of the listing, the floor approval and the price ladder: FEAT-AST-11 and FEAT-AST-12's stories, API-S5-004's approval flow and API-S5-005's rounds.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

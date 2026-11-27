# RWB-S6-E5024-APP Build the lots and estimate the price

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E5024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S6-E5024-APP-16) |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S6-B |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S6-E5024-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the lot build and price slice of RWB-E5-024 in rwb-debtsale. The two legacy criteria are kept word for word with their origin tag; the step groups the population into lots under R-DS-05, takes the estimate from rwb-agent and the COLLINS lot economics from rwb-source-data, writes the two tables of `rwb_debtsale`, records the decision first (DP-03) and serves the two lot operations on `/api/recovery/debtsale/v1` (DP-13) behind SCR-25 through the gateway-bff route (DP-19). R-DS-04's criterion and the move to `LOT_WITH_COMMITTEE` are RWB-S6-E6001-APP's; the estimate, the COLLINS product and the package are consumed rows the plan's empty C row does not name; the minimum lot size, the tiered terms and the reserve policy have no value in any source. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S6-E5024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 20 cross-document, 5 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer (RW-DEBTSALE)**, I want **the Workbench to group the accounts into lots and estimate the price from the COLLINS lot economics**, so that **debt sales run on approved lots and masked data**.

This is the lot build and price slice of legacy RWB-E5-024. It owns:

- the two legacy criteria of the story (AC1 and AC2), copied verbatim with their origin tag, and the rules, messages and screen states they depend on;
- one step of `DebtSaleWorkflow` on task queue `rwb-debtsale`, the stage child of `CaseWorkflow`, ahead of the saga's pivot, the transfer (context pack, Temporal and Drools slides 5, 12 and 13);
- the grouping of the cycle population into lots: the segment of each account against `LOV-SEGMENT` and the size test of R-DS-05;
- the price estimate from the COLLINS lot economics of rwb-source-data and the pricing agent of rwb-agent, which fills `reserve_price` (DF-SAL-024), `buyer_class` (DF-SAL-026), `payment_terms` (DF-SAL-029) and the per-account `selling_price` (DF-SAL-036);
- the lot and account row writes in schema `rwb_debtsale`, in one transaction with the decision record (DP-03);
- the `LOT_PRICED` fact that R-DS-04's condition names, handed to the parent as a stage outcome for RWB-S6-E6001-APP to route to the committee;
- the build half of API-S6-001 `POST /debt-sale-lots` and the priced answer of API-S6-002 `GET /debt-sale-lots/{lotId}` on base `/api/recovery/debtsale/v1`, and the priced state of SCR-25 through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two operations, the `LotRequest` and `DebtSaleLot` elements, the fields DF-SAL-020 to DF-SAL-037, the four closed lists, the consumed rows, the error set and the fakes, which are RWB-S6-E5024-CON; the selection and exclusion of the population (R-DS-01 to R-DS-03), which is RWB-S6-E5023-APP; the committee approval, the reserve decision and the binding tiered terms (R-DS-06), and R-DS-04's own criterion with them, which are RWB-S6-E6001-APP; the masked tape (RWB-S6-E5025-APP), the data room (RWB-S6-E5026-APP), the buyer qualification (RWB-S6-E6002-APP), the award with the cap test of R-DS-19 (RWB-S6-E6005-APP) and the transfer (RWB-S6-E6007-APP); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the COLLINS lot economics and scores, which are rwb-source-data's (P1); the pricing model and its estimate, which are rwb-agent's (P10); the DS package, which is rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The objective, the problem and the metric are unchanged from the legacy story and the module FSD: the Workbench groups the accounts into lots and estimates the price from the COLLINS lot economics (FSD S6 A2.2.1), because debt sales run on spreadsheets with no baseline turnaround (FSD S6 A1.3), and the turnaround is measured on the decision log and the Workbench records against 45 days, reviewed monthly (FSD S6 A2.2.1). The requirement is REQ-S6-002, "Lots are built with an estimated price, and the reserve price is approved before the lot is offered" (FSD S6 Requirements served). What D-RCV-60 changes is who owns the lot, the estimate, the COLLINS fact and the case.

- **The lot is this service's.** `debt_sale_lot` and `debt_sale_account` are S6's two tables in `rwb_debtsale` (context pack ownership rows; TSD S6 T3.1), so the grouping and the price are written here and nowhere else.
- **The COLLINS lot economics stay with rwb-source-data.** The FSD names ACE with the scores ingested by ACE and read through `v_ace_score`; in the target only rwb-source-data holds those views, so the fact arrives as a data product with its as-of date and no `v_ace_*` grant is requested here (FSD S6 A2.2.2; ASM-4890).
- **The estimate is rwb-agent's.** The FSD names a Model gateway as the second integration point; in the target the estimate is the pricing agent's answer on the rwb-agent contract, carrying its model version, and this service holds no model (ASM-4891).
- **The case stays with rwb-case.** `recovery_case` and the route states `LOT_BUILT`, `LOT_TOO_THIN`, `LOT_PRICED` and `LOT_WITH_COMMITTEE` are P3's: this step produces the priced fact and RWB-S6-E6001-APP routes it (ASM-4892).
- **The decision is recorded first**, in the same transaction as the lot and price rows, which is what legacy AC1 asked for and legacy AC2 tested (DP-03).
- **The grouping threshold is data.** R-DS-05 tests `account_count` against a minimum lot size, and no source gives the value: it is a rule row read with its version and never a constant (ASM-4894). The value of the minimum lot size, the reserve basis, the payment-terms ladder and the buyer-class rule is Not specified in the source documents (GAP-1957); each is read from the package as a versioned rule row with a placeholder.

No business value moves: the minimum lot size, the tiered terms, the reserve policy, the buyer class and the four closed lists are reference data or rule rows read with their version.

### 3. Preconditions

- RWB-S6-E5024-CON is published: the two operations with the priced properties of `DebtSaleLot`, the account list, the fields DF-SAL-020 to DF-SAL-037, the four closed lists, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The population of the cycle is on the workflow input: the lot or lots in `LOT_BUILT` with their accounts, recorded by the selection step of R-DS-01 (RWB-S6-E5023-APP). The plan carries no build row between the two lanes, so the population arrives as a stage input and this story needs no live selection build (ASM-4897).
- The rwb-source-data data-product contract that carries the COLLINS score and the lot economics is published with its fake and with the as-of date of the product; its operation name and its field IDs are Not specified in the source documents (GAP-2975; GAP-1954; ASM-4890). The COLLINS fact is read on this contract only, and rwb-debtsale holds no v_ace_* grant.
- The rwb-agent estimate is published with its fake: the lot estimate with the model version in force; its operation name is Not specified in the source documents (GAP-2975; ASM-4891). The run is consumed from P10 rwb-agent under a contract Not specified in the source documents (GAP-1953), with a 60 s budget, the schema-check verdict and the rule fallback (GAP-1953); the DP-20 row the build will need is Not specified in the source documents (GAP-1953).
- The rwb-decision package read is published with its fake and answers the DS package at its version in force, with R-DS-04 and R-DS-05 among its 41 rules over 29 states and the minimum lot size among its rows; its operation name is Not specified in the source documents (GAP-2975; ASM-4893).
- The rwb-case case-list read is published with its fake: the case reference, product group, segment, account link and the outstanding balance of the account; its operation name is Not specified in the source documents (GAP-2975; ASM-4890). The case-move answer has no published operation name, so the step reads it as the workflow stage outcome (GAP-1952).
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-25 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- RWB-PLT-TE006-CON is the wave 0 outbox and inbox library that the topic rwb.debtsale.events.v1 of EV-23 needs; the DP-04 and DP-09 rows are kept in this register, not the metadata table (GAP-2975; GAP-1952).
- `debt_sale_lot` and `debt_sale_account` exist in schema `rwb_debtsale` from the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037 and the standard record columns of TSD S6 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on `rwb_debtsale`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_score` fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the baseline is tagged by RWB-S6-E5024-CON when its tests pass.

### 4. Flow

1. The monthly cycle opens and ACE has ingested the COLLINS scores; rwb-source-data publishes the score and the lot economics as a data product with its business date (FSD S6 A2.2.2; FSD S6 A1.4).
2. The lot build and price step of `DebtSaleWorkflow` on queue `rwb-debtsale` receives its trigger — a completed ACE batch, an event or the timer of the cycle — while the population of the cycle sits in `LOT_BUILT` (FSD S6 A2.2.2 step 1; FSD S6 A2.2.4.4 declares no background event).
3. The step reads the version of the DS package in force: R-DS-04, R-DS-05 and their rows, the minimum lot size, the tiered terms, the buyer class mapping and the reserve policy, one hop with a 2 s budget and a breaker (ASM-4893, ASM-4894).
4. It reads the COLLINS score and the lot economics of the accounts on the rwb-source-data contract, with the as-of date. A product that is stale after a late or failed ACE batch holds the step with VR-S6-002-1 and MSG-P1-001, and nothing is written (ASM-4890).
5. It reads the case facts of those accounts on the rwb-case contract: case reference, product group, segment, account link and the outstanding balance, read only; it never reads `recovery_case`.
6. `LotGrouper` applies the grouping: the segment of each account against `LOV-SEGMENT` decides the lot it belongs to, and R-DS-05 tests `account_count` against the minimum lot size. Where the count is below it the accounts merge into the next lot and no priced lot is produced; where the count clears it the lot keeps its `lot_no`, `cut_off_date` and `segment` and is priced.
7. `PriceEstimateClient` asks the pricing agent of rwb-agent for the estimate of the lot from the COLLINS lot economics and receives the estimate with the model version that produced it (ASM-4891).
8. `LotPriceWriter` fills `reserve_price`, `buyer_class` against `LOV-BUYER-CLASS`, `payment_terms` and the per-account `selling_price` from the estimate and the rule rows; `status` stays `BUILDING` of `LOV-LOT-STATUS` and the approval authority, the buyer and the signing date stay empty (ASM-4896).
9. `DebtSaleDecisionRecordWriter` writes one decision record per priced lot through the local library, **before any row changes**: the lot reference, the rule IDs with the package version, the model version of the estimate, the inputs reference with the as-of date, the minimum lot size in force, the estimate and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC2).
10. The lot row, the account prices and the idempotency row commit in one `rwb_debtsale` transaction with the optimistic lock of `version`.
11. The step produces the `LOT_PRICED` fact of the lot — the condition R-DS-04 names — and hands it to the parent as a stage outcome, with the rule IDs and the versions. R-DS-04's transition to `LOT_WITH_COMMITTEE`, the committee routing and its 5 working days are RWB-S6-E6001-APP's: this step writes no case state and answers no move (ASM-4892).
12. A repeated trigger for the same population, cut-off date and package version writes no second lot, no second price and no second record, and counts the repeat; the `Idempotency-Key` of a repeated POST answers the lot it priced.
13. SCR-25 Lot builder shows the priced state of the lot — the accounts, the segment, the cut-off date, the reserve, the tiered terms, the buyer class and the per-account price — from this service through the gateway-bff composite route, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no lot change, no price and no priced fact leaves the service | MSG-P7-003 | AC2, TC-E5-024-02, TC-E5-024-04 |
| X2 | The role does not hold the Debt sale right of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC3, TC-E5-024-03, TC-S6-E5024-APP-09 |
| X3 | The lot is not in `LOT_BUILT`, or has left the population since it was read | 409 and nothing is written for that lot; a lot already priced is not priced twice | None | AC1, X6 |
| X4 | The COLLINS data product is stale after a late or failed ACE batch | The step holds, writes nothing and shows the data date; it resumes on the next fresh answer | MSG-P1-001 | AC1, TC-S6-E5024-APP-02 |
| X5 | The rwb-case, rwb-source-data, rwb-agent or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no fact is produced; the caller sees 503 with the platform envelope | None | AC1, X6 |
| X6 | The account count of the lot is below the minimum lot size of R-DS-05 | The accounts merge into the next lot and the lot is not priced; no estimate is asked and no row is written | None | AC1, TC-S6-E5024-APP-01 |
| X7 | A repeated trigger for the same population, cut-off date and package version, or the same `Idempotency-Key` twice | One priced lot, one set of prices, one record and one fact; the repeat is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, another service's schema or a model binary | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC4, Section 17, BR3, BR4, BR6, TC-S6-E5024-APP-03, TC-S6-E5024-APP-05 |

X1 and X2 are the legacy exception paths carried onto the slice, X3 to X7 are the paths the target call types and the once-per-cycle trigger add, and X8 is the ACE, schema and model boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S6-E5024-CON, the rwb-case, rwb-source-data, rwb-agent and rwb-decision fakes and the decision-record stub, on its own schema; no live P1, P3, P7 or P10 is needed |
| Negotiable | The activity name, the decision code per rule and the shape of the priced fact are this story's choice; the rules, the messages, the screen, the two operations and the table columns are fixed |
| Valuable | A lot of the cycle is grouped and priced from the COLLINS lot economics with its decision recorded, so the 45-day turnaround is measurable |
| Estimable | One workflow step, one grouper, one estimate client, one record write, two row writers, four clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic population and a synthetic estimate through the contract fakes, plus the access, stale-data and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Build the lots and estimate the price

  Background:
    Given the cycle population holds 340 accounts in state "LOT_BUILT" on segment "RETAIL"
    Given the DS rule package is in force at its version and carries R-DS-04 and R-DS-05
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Build the lots and estimate the price (legacy RWB-E5-024 AC1)
    Given the rwb-source-data contract mock returns the score and the COLLINS lot economics of the 340 accounts with as-of date "2026-11-30"
    Given the rwb-agent contract mock returns the lot estimate with the model version in force
    Given the rwb-case contract mock returns the case facts of the 340 accounts in state "LOT_BUILT"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then groups the accounts into lots and estimates the price from the COLLINS lot economics
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E5-024 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 Role without the Debt sale right is refused (new, D-RCV-60)
    Given the role does not hold the Debt sale right of the operation
    When the operation is called
    Then the system answers 403 with MSG-P4-002 and nothing is read or written

  Scenario: AC4 No ACE data tier, case row or foreign schema is reached (new, D-RCV-60)
    Given the build is tested by the boundary test
    When a statement, a test or a component reaches the ACE data tier, a recovery_case row or another service's schema
    Then the grant refuses the statement and the build fails; nothing is released

  Scenario: AC5 A consumed call fails or does not answer (new, D-RCV-60)
    Given a consumed contract mock fails or does not answer
    When its trigger arrives
    Then nothing is written and the message is Not specified in the source documents (NEWAC-RWB-S6-E5024-APP-AC10)

  Scenario: AC6 A status change the model does not allow is refused (new, D-RCV-60)
    Given the lot is in a state that does not allow the requested status change
    When the status change is requested
    Then the change is refused, nothing is written and the message is Not specified in the source documents (NEWAC-RWB-S6-E5024-APP-AC11)

  Scenario: AC7 Error answers of the provided operations (401, 403, 404) (new, D-RCV-60)
    Given a provided operation is called without a valid credential, by a role without the Debt sale right, or on a lot that does not exist
    When the operation is called
    Then the system answers 401, 403 or 404 as the case requires and nothing is read or written; a 403 shows MSG-P4-002 and the other messages are Not specified in the source documents (NEWAC-RWB-S6-E5024-APP-AC7)

  Scenario: AC8 Replay of a write with the same idempotency key (new, D-RCV-60)
    Given a write has been completed once with an Idempotency-Key
    When the same write is sent again with the same Idempotency-Key
    Then one priced lot, one set of prices, one record and one fact remain, and the repeat is counted

  Scenario: AC9 Activity retry and timeout (new, D-RCV-60)
    Given a consumed contract does not answer inside 2 s or its breaker is open, or the rwb-agent estimate does not answer within 60 s
    When its trigger arrives
    Then the step retries on the workflow's own schedule, nothing is written and no fact is produced; the caller sees 503 with the platform envelope, and the rule result is the fallback for the estimate
```

The first two criteria (AC1 and AC2) are the legacy criteria of RWB-E5-024 word for word, with their origin tag added and only the decision log wording changed to decision record (CG-ALL-10370): the repeated `Then`, `its trigger arrives` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines, and those are the only additions. What the legacy lines describe happens in four places now: rwb-source-data answers the COLLINS lot economics, which the FSD named as `v_ace_score`; rwb-agent (P10 rwb-agent) answers the estimate through the agent run of the kit, with a 60 s limit and the rule result as the fallback, and the agent, model and prompt versions are recorded with the estimate (the Model gateway named by the FSD is not a service); rwb-case answers the case facts and keeps the route state; and this story groups, prices, records and produces the priced fact. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_debtsale`, with the central `decision_log_entry` ledger of rwb-decision behind it. AC3 to AC9 are new, with no legacy text: AC3 is the Debt sale right of X2, AC4 is the boundary of X8, and AC5 to AC9 cover the consumed-call, status, error, replay and retry cases. R-DS-04's criterion belongs to RWB-S6-E6001-APP AC3; this story tables the rule as BR11 with the state and the fields it produces, and the split is recorded in the traceability of both stories.

### 8. Business rules

| BR ID | Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BR10 | R-DS-05 | Debt sale | D8.4 | LOT_BUILT | LOT_TOO_THIN | account_count below the minimum lot size | Merge the accounts into the next lot | LOT_BUILT | Debt sale officer | Workbench | None |
| BR11 | R-DS-04 | Debt sale | D8.4 | LOT_BUILT | LOT_PRICED | lot agent estimate returned with COLLINS | Propose the lots, the tiered buyer terms and the reserve price | LOT_WITH_COMMITTEE | Committee | Agent Runtime, COLLINS, Case Workspace | 5 working days |

Both rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner and systems columns name business roles and systems, not services: in the target "Agent Runtime" is the rwb-agent estimate, "COLLINS" is the rwb-source-data data product, "Case Workspace" is rwb-case and SCR-25, and "Workbench" is this service. R-DS-05 is applied here in full. Of R-DS-04 this story produces the condition — the estimate returned — and fills the lot it names; its transition, its criterion and its 5 working days are RWB-S6-E6001-APP's (ASM-4892). R-DS-19, the cap row at the award, is not tabled here.

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and the price are this service's: `debt_sale_lot` and `debt_sale_account` are rows of `rwb_debtsale`, and no other service writes them | Context pack ownership rows (both S6); TSD S6 T3.1; FSD S6 A2.2.2 |
| BR2 | The decision is recorded before the lot and price rows change, with the rule IDs, the package version and the model version; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S6 T2; legacy AC1 and AC2 |
| BR3 | The COLLINS lot economics and the score stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the fact on the owner's contract with its as-of date | DP-05 as a prohibition; FSD S6 A2.2.2; ASM-4890 |
| BR4 | The case stays with rwb-case: no `recovery_case` row, no route-state column and no case write here; the priced fact leaves as a stage outcome | ASM-4892; TSD S6 T4 |
| BR5 | The estimate is the pricing agent's, held as an input with its model version; no model binary, no threshold and no scoring formula is built, stored or shipped here | ASM-4891; FSD S6 A2.2.2 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_debtsale`; `account_id` and `buyer_partner_id` are identifiers of other services' facts | DP-01; TSD S6 T3.3 |
| BR7 | Every value a business person may change is reference data or a rule row read with its version: the minimum lot size, the tiered terms, the reserve policy, the buyer class mapping and the four closed lists | TSD S6 T3.2; FSD S6 BR-S6-002; legacy Guardrails |
| BR8 | The same trigger twice, or the same `Idempotency-Key` twice, prices one lot once | TSD S6 T-A.2 |
| BR9 | The lot status vocabulary is closed: a priced lot is still `BUILDING`; `OFFERED` arrives with the committee approval and no other value is written here | TSD S6 T3.2; ASM-4896 |

Coverage: BR1 by TC-S6-E5024-APP-05; BR2 by AC2, TC-E5-024-02, TC-E5-024-04; BR3 by AC4, TC-S6-E5024-APP-03; BR4 by AC4; BR5 by TC-S6-E5024-APP-03; BR6 by AC4, TC-S6-E5024-APP-05; BR7 by TC-E5-024-01, TC-S6-E5024-APP-01; BR8 by TC-S6-E5024-APP-06; BR9 by TC-E5-024-01; BR10 by AC1, TC-S6-E5024-APP-01; BR11 by AC1, TC-E5-024-01.

### 9. State transitions

The case route state is rwb-case's and is not changed here: the step produces the `LOT_PRICED` fact and RWB-S6-E6001-APP applies R-DS-04 (BR4). What this story owns is the lot row and the state of the step.

| From (`debt_sale_lot`) | Event | Condition | To |
|---|---|---|---|
| `BUILDING`, populated by R-DS-01 | The size test of R-DS-05 | account_count below the minimum lot size | Unchanged, the accounts merged into the next lot, no price written |
| `BUILDING`, population clears the size test | The estimate returned for the lot | lot agent estimate returned with COLLINS | `BUILDING` with `reserve_price`, `buyer_class`, `payment_terms` and the per-account `selling_price` written |
| `BUILDING` priced | The committee approval of R-DS-06 | reserve and terms approved inside the delegation | `OFFERED`, by RWB-S6-E6001-APP |
| `BUILDING` priced | A repeated trigger for the same population and package version | X7 | Unchanged, the repeat is counted |
| `BUILDING` priced | The estimate or the decision record fails | X1, X5 | Unchanged, nothing committed |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The cycle population is in `LOT_BUILT` and the package in force is read | The trigger arrives | Grouping |
| Grouping | The lot clears the size test | R-DS-05 does not merge it | Estimating |
| Grouping | The lot is below the minimum lot size | R-DS-05 | Waiting for the next lot |
| Estimating | The estimate and the decision record are written and committed | The transaction commits | Waiting for the committee |
| Estimating | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Estimating | The COLLINS data product is stale | X4 | Held, until a fresh answer |

The route states are those of the DEBTSALE machine of TSD S6 T4 and live on the case of record. The lot status values are those of `LOV-LOT-STATUS`; that list has no "priced" value, so the priced state of SCR-25 is a lot at `BUILDING` with its reserve and terms filled (ASM-4896).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DEBTSALE, debt sale officer | Debt sale CRUA in TSD S6 T6.1: the primary role, building and pricing a lot and re-running the step |
| RW-PRODHEAD, product head; RW-HEADASL, head of Asset Liquidity | Debt sale RA: read the lot and approve through the committee path where the delegation reaches it |
| RW-SALEOFF, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Debt sale R: read only, in scope |
| PT-BUYER, PT-RAMC | Debt sale R in this step: the partner reaches its own lot through the partner gateway of the data room, never the build or the price |
| SY-CASEWF, SY-RULES, SY-AGENT | Debt sale R as the matrix gives it; the service identities run the step under the same checks |
| rwb-debtsale service identity | Runs the step, reads the case facts, the COLLINS product, the estimate and the package, writes the record and the rows and produces the priced fact; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S6 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the debt sale officer as also-user (FSD S6 A2.2.3.3), and both statements hold: the step runs under the service identity with no officer task on the happy path, and the officer is the primary role when a person acts on SCR-25 or re-runs a cycle. Each operation calls the rwb-access authorise check for the capability area "Debt sale" and its right through the access guard before any read or write; the access guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 | debt_sale_lot (S6, `rwb_debtsale`) | id | Read and written as the lot reference of the row and the fact |
| DF-SAL-021 | debt_sale_lot (S6, `rwb_debtsale`) | lot_no | Write, the lot numbering of the cycle |
| DF-SAL-022 | debt_sale_lot (S6, `rwb_debtsale`) | cut_off_date | Write, the cut-off date of the population |
| DF-SAL-023 | debt_sale_lot (S6, `rwb_debtsale`) | segment | Write, against `LOV-SEGMENT`, the grouping key |
| DF-SAL-024 | debt_sale_lot (S6, `rwb_debtsale`) | reserve_price | Write, from the estimate and the reserve row |
| DF-SAL-025 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_partner_id | Not written here: the award and buyer stories |
| DF-SAL-026 | debt_sale_lot (S6, `rwb_debtsale`) | buyer_class | Write, against `LOV-BUYER-CLASS`, from the tiered terms |
| DF-SAL-027 | debt_sale_lot (S6, `rwb_debtsale`) | signing_date | Not written here: the approval and award stories |
| DF-SAL-028 | debt_sale_lot (S6, `rwb_debtsale`) | approval_authority | Not written here: RWB-S6-E6001-APP |
| DF-SAL-029 | debt_sale_lot (S6, `rwb_debtsale`) | payment_terms | Write, the tiered buyer terms of the estimate |
| DF-SAL-030 | debt_sale_lot (S6, `rwb_debtsale`) | status | Write, `BUILDING` of `LOV-LOT-STATUS`, unchanged by this step |
| DF-SAL-031 to DF-SAL-034 | debt_sale_account (S6, `rwb_debtsale`) | id, lot_id, account_id, borrower_code | Read and written as the account rows of the lot; `borrower_code` is a code, no name |
| DF-SAL-035 | debt_sale_account (S6, `rwb_debtsale`) | outstanding | Read and written from the COLLINS-fed balance of the account |
| DF-SAL-036 | debt_sale_account (S6, `rwb_debtsale`) | selling_price | Write, the per-account price of the estimate |
| DF-SAL-037 | debt_sale_account (S6, `rwb_debtsale`) | put_back_status | Read; `NONE` of `LOV-PUTBACK` until the put-back stories |
| Standard columns | both tables (S6, `rwb_debtsale`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_debtsale`) | rule id, rule version, model version, inputs reference, estimate, outcome, decided at | Write through the local library, before the rows change |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case facts arrive on the rwb-case contract |
| `v_ace_score` and the COLLINS lot economics (P1) | the score, the lot economics and the as-of date | Not read: no `v_ace_*` grant. Field IDs Not specified in the source documents (GAP-2975; ASM-4890) |
| The estimate and its model version (P10) | the lot estimate | Read on the rwb-agent row; no column of `rwb_debtsale` holds it beyond `reserve_price`, `payment_terms`, `buyer_class` and `selling_price` (ASM-4891) |
| The minimum lot size, the tiered terms and the reserve policy (P7) | rule rows | Read with their version; the value of the minimum lot size is Not specified in the source documents (GAP-2975; ASM-4894) |

Field IDs are those of TSD S6 T3.1 and the Logical Data Model and Data Dictionary. **No new table, no new column and no migration**: this story writes existing columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_debtsale` by the library's own migration (DP-03). `outbox_event` sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, codes, amounts, dates, list values and versions. No name, address, contact value or identity number enters `rwb_debtsale`, the record, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

`account_count` is counted at the step from the account rows of the lot and is not stored. `account_id` is the identifier of the other service's fact and `decision_record` is the library object of DP-03; their field and entity IDs are Not specified in the source documents (DOR-RWB-S6-E5024-APP-7).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-debtsale (S6); base `/api/recovery/debtsale/v1` (DP-13). This story supplies the grouping and pricing behaviour behind the build half of the create and the priced answer of the read, whose shapes RWB-S6-E5024-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/debt-sale-lots` | LotRequest in, DebtSaleLot out, the lot built from the population and priced from the estimate (API-S6-001) | Debt sale, right C, scope applied | `Idempotency-Key` header |
| GET | `/debt-sale-lots/{lotId}` | DebtSaleLot out, with its accounts, their prices, the reserve, the terms and the status (API-S6-002) | Debt sale, right R, scope applied | Not applicable |

The errors are 401, 403 with MSG-P4-002, 409 for a lot that is not in `LOT_BUILT` or a repeated lot, 422 with MSG-GEN-001 and 503 when the library or a consumed contract does not answer, as TSD S6 T-A.2 gives them. `POST /debt-sale-lots/{lotId}/award` (API-S6-003) is RWB-S6-E6005-APP's, and `GET /partner/data-room/{lotId}` (API-S6-004) and `POST /partner/data-room/{lotId}/bids` (API-S6-005) are RWB-S6-E5026-APP's and the bidding stories'.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case-list read (operation name Not specified in the source documents (GAP-2975; ASM-4890)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, product group, segment, account link and outstanding balance of the lot accounts; faked |
| The COLLINS lot-economics and score read (operation name Not specified in the source documents (GAP-2975; ASM-4890)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The score, the lot economics and the as-of date of the product; faked |
| The price-estimate ask (operation name Not specified in the source documents (GAP-2975; ASM-4891)) | `/api/recovery/agent/v1` | P10 rwb-agent | The lot estimate with its model version; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-2975; ASM-4893)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DS package at its version, with R-DS-04 and R-DS-05 among its 41 rules over 29 states, the minimum lot size, the tiered terms and the reserve policy; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). Each row builds against the v1 contract of its path shown above, so the contract version is fixed at /v1. The four rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-2975; ASM-4890, ASM-4891, ASM-4893).

#### 12.3 Events published

None. The service publishes on `rwb.debtsale.events.v1`, whose event set carries `LotAwarded` (event `EV-23`) with `AccountsTransferred` beside it, and neither belongs to this step: pricing a lot awards nothing and transfers no account. `LotAwarded` is RWB-S6-E6005-APP's and `AccountsTransferred` is RWB-S6-E6007-APP's, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The priced fact is a stage outcome of the workflow and not an event; the outbox library that relays the topic is the DP-09 dependency the plan does not carry for this key (ASM-4895).

#### 12.4 Events consumed

None. The service subscribes to `ProceedsMatched` of rwb-payment in the settlement and transfer steps of the saga (context pack connection matrix, row S6), and it does not belong to the build and price: no proceeds exist before a lot is awarded. This story therefore holds no consumer group, no subscription and no inbox row. The trigger of the step is the completed ACE batch, the event or the timer of the cycle, and the FSD declares no background event for the feature (FSD S6 A2.2.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per sale cycle, the child of `CaseWorkflow`, a saga whose pivot is the transfer, continues-as-new at each stage end | `rwb-debtsale` | Input: the cycle, the cut-off date, the population reference and the package in force; signals: the estimate answer and the approval answer. This step sits before the pivot, so it needs no compensation |
| `buildLotsAndEstimatePrice` | Activity, the one grouping and pricing step | `rwb-debtsale` | The population, the COLLINS product, the estimate and the package in; the priced lots, the rule IDs with their versions, the model version, the priced fact and the decision record out, written in one transaction |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document; the trigger is the opening of the build for a population in `LOT_BUILT`, because R-DS-05 and R-DS-04 carry no clock of their own and the FSD declares no background event.

Workflow ID form: Not specified in the source documents (CG-ALL-10364). Start rule (Temporal Catalog v1): DebtSaleWorkflow starts when the monthly sale cycle opens or a residual arrives from disposal (R-DS-01); the duplicate-start policy is Not specified in the source documents (CG-ALL-10364).

#### 12.6 Schedules

None. The step runs from the cycle's build trigger and from the stage signal the parent forwards, and owns no Temporal Schedule and no legacy Quartz job: the context pack lists no job for this service and R-DS-04's timer of 5 working days belongs to the committee routing of RWB-S6-E6001-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot of the population; this story groups it, writes the segment, the reserve, the terms, the buyer class and the status, and leaves it `BUILDING` |
| debt_sale_account | S6 (`rwb_debtsale`) | An account in a lot; this story writes its `selling_price` and reads its balance and put-back status |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_debtsale` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), `v_ace_*` and every `v_ace_score` row (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), and the later stories' data-room, bid and transfer tables of this service. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-facts fake | The case facts of the 340 accounts in `LOT_BUILT`, `RC-2026-000601` among them, with the segment, the account link and the balance; a lot that has left the population | AC1, X3 |
| rwb-source-data COLLINS data-product fake | The score and the lot economics of the 340 accounts with as-of date `2026-11-30`; a stale product with its date; no answer beyond 2 s | AC1, X4, X5 |
| rwb-agent estimate fake | The lot estimate with the model version in force; an answer without a model version, refused as malformed | AC1, TC-S6-E5024-APP-03 |
| rwb-decision package fake | The DS package at its version with R-DS-04, R-DS-05, the minimum lot size, the tiered terms and the reserve policy | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-25 answer for the lot in its priced state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-2975; ASM-4890, ASM-4891, ASM-4893).

The COLLINS score and lot economics are read only through the rwb-source-data contract, under the source field names `v_ace_score.*`, `v_ace_account.*` and `v_ace_batch_status.*`; no ACE view or ACE table is read by this build. The path is to be confirmed with P1 (REST for the screen, activity inside the workflow) before the wave 3 system test (GAP-1770).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two lot operations on `/api/recovery/debtsale/v1`; the case-facts read, the COLLINS read, the estimate ask and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` belong to later stories and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `DebtSaleWorkflow` and its grouping and pricing step on `rwb-debtsale`; no Schedule |
| File | None | No file is read, built or delivered here; the data tape and the buyer file are RWB-S6-E5025-APP's and RWB-S6-E6007-APP's |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.debtsale`, module `lotsale`; front end `src/modules/recovery/debtsale/LotBuilder.tsx`, the fragment SCR-25 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the lot change, the prices and the priced fact commit together or not at all. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-25 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-05 (the ACE read), DP-20 (the agent client) and DP-09 (the outbox library) are real dependencies of this step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-2975; ASM-4890, ASM-4891, ASM-4895).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C in fact, and the plan's C row is None. DP-20 would add `RWB-P10-TE013-CON` for the estimate and DP-09 would add `RWB-PLT-TE006-CON` for the topic; the plan's H row stands unchanged and both are tracked.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DebtSaleWorkflow` build-and-price branch | Workflow | Waits for the build trigger, reads the package in force and reports the priced fact to the parent |
| `buildLotsAndEstimatePrice` | Activity | Reads the case facts, the COLLINS product, the estimate and the package, groups, prices, records and commits |
| `LotGrouper` | Service | The segment grouping and the size test of R-DS-05, with the merge into the next lot |
| `PriceEstimateClient` | Client | The estimate ask to rwb-agent with the model version, one hop, 2 s, breaker |
| `SourceDataEconomyClient` | Client | The COLLINS lot economics and score read with the as-of date and the stale path |
| `RulePackageClient` | Client | The package read at its version in force, with the minimum lot size, the tiered terms and the reserve policy |
| `LotPriceWriter` | Repository | Writes the lot columns, the per-account prices, the idempotency row and the optimistic lock in one transaction |
| `DebtSaleDecisionRecordWriter` | Library adapter | Writes the record with the rule and model versions before any change; refuses the step on failure |
| `DebtSaleLotController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `LotBuilder` | React component | Shows the grouped and priced lot on SCR-25, read only, with the refusal and stale-data states |

**Database and migrations.** No Flyway file. The tables arrive with the DB story of this service, and the record and idempotency key are library objects created in `rwb_debtsale` by the library's migration (DP-03). No column is added for the estimate, the model version, the score or the case: those are facts and versions of their owners and are referenced, not copied.

**Configuration and reference data.** Parameters read here: the four LOV lists, the minimum lot size, the tiered buyer terms and the reserve policy. Reference-data contract (DP-06, DP-07): Not specified in the source documents (DOR-RWB-S6-E5024-APP-20).

- `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-LOT-STATUS` and `LOV-PUTBACK` at their version in force (TSD S6 T3.2), read as reference data and never as constants.
- The minimum lot size, the tiered buyer terms and the reserve policy: rule rows with their version, never written in code (ASM-4894).
- The capability area "Debt sale" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020.

**Build steps**

1. The build-and-price branch of `DebtSaleWorkflow` and its input record on `rwb-debtsale`, with the build trigger.
2. `SourceDataEconomyClient` and the case-facts client against their fakes, with the 2 s budget, the as-of date, the stale path and the no-answer path (AC1, X4, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `LotGrouper` with the segment grouping and the R-DS-05 merge and size test (AC1, X6).
5. `PriceEstimateClient` against its fake, with the model version carried into the record and the fact (AC1).
6. `LotPriceWriter` with the one transaction, the lot columns, the per-account prices and the optimistic lock (AC1, X7).
7. `DebtSaleDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC2, X1).
8. `DebtSaleLotController` with the rights, the `Idempotency-Key` and the problem mapping, and `LotBuilder` on SCR-25 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_debtsale`, no `v_ace_*` read, no model binary and no write to any other service's schema (X8, BR3, BR5).

**Feature flag.** `rwb.debtsale.lotprice-v1`, a flag of the platform library; off means the step holds the build, writes nothing and produces no priced fact.

**Done when.** The tests of section 16 pass, the step runs from a synthetic population in SIT, a lot is grouped and priced from the estimate, R-DS-05 merges a thin lot, the model version is in the record, a repeated trigger prices once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-25 answers the priced state through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the request or of the estimate answer is absent or invalid (X5) | Enter {field}. |
| MSG-P4-002 | A role without the Debt sale right calls the create or the read (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The COLLINS data product of the population is stale after a late or failed ACE batch (X4, VR-S6-002-1) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S6-001 | An account of the population has an open deviation and cannot be sold; raised on the exclusion path of the selection, not here (X6) | {account} has an open deviation and cannot be sold. |

The five IDs are the message set of the legacy story and of FSD S6 A2.2.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S6-001 is carried because it is in the message set of this feature; the exclusion that raises it is R-DS-02 and RWB-S6-E5023-APP's.

### 15. Screens and states

SCR-25 Lot builder, in its loading and priced states, is served through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot, its accounts, the reserve, the terms and the prices, rwb-case for the case and its route state, rwb-source-data for the score and its as-of date, and rwb-agent for the estimate and its model version; this story fixes the rwb-debtsale answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The state this story produces is the priced state of SCR-25: the grouped accounts, the segment, the cut-off date, the reserve, the tiered terms, the buyer class and the per-account price, on a lot at `BUILDING`. The legacy screen table gives the states "Draft; priced; approved": the draft state belongs to RWB-S6-E5023-APP and the approved state to RWB-S6-E6001-APP. The refusal, not-recorded, stale-data and thin-lot states read the messages of section 14. PRT-05 Data room belongs to RWB-S6-E5026-APP and is served through the partner gateway; this service publishes only data and commands to the routes. SCR-26 Award is served through the gateway-bff composite route in the same way as SCR-25. The screen owner of SCR-25, SCR-26 and PRT-05 is to be named in the edge story RWB-PLT-N001-CON. The empty, loading, error and no access states of SCR-25 are Not specified in the source documents (CG-ALL-10371); the no access case is the 403 refusal of section 16.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-024-01 | AC1 | Component | The 340-account population, the COLLINS product and the estimate on the fakes; the lot row, the prices, the record and the priced fact asserted |
| TC-E5-024-02 | AC2 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E5-024-03 | Access, AC3 | Component | A role without the Debt sale right; 403 with MSG-P4-002 and no read |
| TC-E5-024-04 | Principle 5 | Component | A forced decision record write failure inside the transaction; no lot change, no price and no fact |
| TC-S6-E5024-APP-01 | AC1, X6 | Component | A population of 12 accounts under the minimum lot size; the merge by R-DS-05, no estimate asked and no row written |
| TC-S6-E5024-APP-02 | AC1, X4 | Component | A stale COLLINS product with its date; the step held with MSG-P1-001 and nothing written |
| TC-S6-E5024-APP-03 | AC1, AC4, X8 | Component | An estimate answer without a model version, refused; a build that reaches the ACE data tier by any grant or loads a model binary fails |
| TC-S6-E5024-APP-04 | AC1, section 12 contract | Component | The operations, events and activities of section 12 called on the fakes of their owners; each request and answer matched to its published contract, and the no-event rule of 12.3 asserted |
| TC-S6-E5024-APP-05 | AC4, BR1, BR6, section 12.7 | Component | The tables of section 12.7 on the schema of `rwb_debtsale`: the owned tables written, no foreign key and no join out of the schema, no read of an unowned table (ASM-3438) |
| TC-S6-E5024-APP-06 | AC1, X7, BR8 | Component | The same trigger and the same `Idempotency-Key` sent twice; one priced lot, one set of prices, one record and one fact, and the repeat counted |
| TC-S6-E5024-APP-07 | AC5 | Component | A consumed contract mock that fails or does not answer; nothing written; the message is Not specified in the source documents (NEWAC-RWB-S6-E5024-APP-AC10) |
| TC-S6-E5024-APP-08 | AC6 | Component | A lot in a state that does not allow the requested status change; the change refused and nothing written; the message is Not specified in the source documents (NEWAC-RWB-S6-E5024-APP-AC11) |
| TC-S6-E5024-APP-09 | AC3, X2 | Component | A role without the Debt sale right calling each lot operation; 403 with MSG-P4-002 and no read or write |
| TC-S6-E5024-APP-10 | AC7 | Component | A call without a valid credential, by a role without the Debt sale right, and on a lot that does not exist; 401, 403 and 404 answered, nothing read or written, MSG-P4-002 shown for the 403 |
| TC-S6-E5024-APP-11 | AC8, X7 | Component | The same write sent twice with the same Idempotency-Key; one priced lot, one set of prices, one record and one fact, and the repeat counted |
| TC-S6-E5024-APP-12 | AC9, X5 | Component | A consumed contract that does not answer inside 2 s and an rwb-agent estimate not answered within 60 s; the step retries, nothing written, no fact, 503 with the platform envelope and the rule result as the fallback |

The four legacy cases are those of RWB-E5-024 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The twelve `TC-S6-E5024-APP-nn` cases are new and test only this build. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 3 harness.

SCR-25 states: no access is TC-E5-024-03 (403, MSG-P4-002); a stale product held is TC-S6-E5024-APP-02 (MSG-P1-001); a decision record unavailable is TC-E5-024-02 (MSG-P7-003). The empty and loading states are Not specified in the source documents (DOR-RWB-S6-E5024-APP-10).

### 17. Guardrails

- No business value in code: the minimum lot size, the tiered terms, the reserve policy, the buyer class mapping, the lists and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch.
- No personal data in `rwb_debtsale`, in a workflow input or in a log: identifiers, codes, amounts, dates, list values and versions only, `borrower_code` is a code, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table (BR3).
- No model in this service: the estimate is an input with its model version, and no binary, weight or scoring formula is shipped, cached or logged here (BR5).
- The case stays with rwb-case: no `recovery_case` row, no route-state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `v_ace_score` view read.
- The decision is recorded before the change; a build that writes the price outside the record's transaction fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Feature | L3 process | Test cases |
|---|---|---|---|---|---|
| REQ-S6-002 | Lots are built with an estimated price, and the reserve price is approved before the lot is offered (FSD S6 Requirements served); the split plan carries no requirement id for this slice (GAP-2975) | The grouping, the estimate and the lot and price rows | FEAT-DBS-02 | Not specified in the source documents (DOR-RWB-S6-E5024-APP-2) | TC-E5-024-01, TC-E5-024-04, TC-S6-E5024-APP-01 |
| ADR-013 | 19 services inside ACE | rwb-debtsale as the owner of the lot and the price | FEAT-DBS-02 | Not specified in the source documents (DOR-RWB-S6-E5024-APP-2) | TC-E5-024-01 |
| ADR-014 | Schema and login per service | `rwb_debtsale` and its own login | FEAT-DBS-02 | Not specified in the source documents (DOR-RWB-S6-E5024-APP-2) | TC-S6-E5024-APP-03 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The DS package read at its version | FEAT-DBS-02 | Not specified in the source documents (DOR-RWB-S6-E5024-APP-2) | TC-E5-024-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | FEAT-DBS-02 | Not specified in the source documents (DOR-RWB-S6-E5024-APP-2) | TC-E5-024-01, TC-S6-E5024-APP-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | FEAT-DBS-02 | Not specified in the source documents (DOR-RWB-S6-E5024-APP-2) | TC-E5-024-02, TC-E5-024-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-024, disposition Split (rework); feature FEAT-DBS-02 |
| Legacy criteria | AC1 and AC2, owned word for word by this story; the R-DS-04 criterion is RWB-S6-E6001-APP AC3 |
| Source text | Legacy RWB-E5-024; FSD S6 Debt sale v3 A1.3, A1.4, A2.2 and Requirements served; TSD S6 Debt sale v2 T2, T3, T4, T5, T6 and T-A; Business Rules and Routing Logic v4 rows R-DS-04 and R-DS-05; Epics 3 to 8 Specification v3 FEAT-DBS-01 and FEAT-DBS-02 |
| Test cases | TC-E5-024-01 to TC-E5-024-04 and TC-S6-E5024-APP-01 to -03 |
| Feature and screens | FEAT-DBS-02, SCR-25 Lot builder (priced state) |
| Rules | R-DS-05 applied here; R-DS-04 produced here and transitioned by RWB-S6-E6001-APP; both governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two operations, the elements, the fields DF-SAL-020 to DF-SAL-037, the four lists, the consumed rows, the error set and the fakes: RWB-S6-E5024-CON.
- The selection and exclusion of the population, R-DS-01 to R-DS-03 and the 54 percent cap: RWB-S6-E5023-APP and RWB-S6-E6005-APP.
- The committee approval, the reserve decision, the binding tiered terms, R-DS-04's own criterion and the case move to `LOT_WITH_COMMITTEE`: RWB-S6-E6001-APP.
- The masked data tape (RWB-S6-E5025-APP); the data room (RWB-S6-E5026-APP); the buyer qualification (RWB-S6-E6002-APP).
- The award, the cap test of R-DS-19, `LotAwarded`, the settlement, `AccountsTransferred`, the derecognition and the posting: RWB-S6-E6005-APP, RWB-S6-E6007-APP, with the money in rwb-payment (P8).
- The value of the minimum lot size, of the tiered terms and of the reserve policy: rule rows of rwb-decision with the placeholder (ASM-4894).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the COLLINS lot economics and scores: rwb-source-data (P1); the pricing model and the estimate: rwb-agent (P10); the DS package: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-25: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

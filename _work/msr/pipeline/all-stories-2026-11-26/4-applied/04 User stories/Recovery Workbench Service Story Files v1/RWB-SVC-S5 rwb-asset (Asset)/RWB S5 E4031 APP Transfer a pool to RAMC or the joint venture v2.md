# RWB-S5-E4031-APP Transfer a pool to RAMC or the joint venture

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4031-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-W |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E4031-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of legacy RWB-E4-031 split out for rwb-asset. The three legacy acceptance criteria are kept word for word with their origin tag; the transfer becomes one step of `AssetDisposalWorkflow` on task queue `rwb-asset` that evaluates R-DIS-59 with the DISPOSAL package version in force, writes the transfer record as the `asset_sale` rows of the pool with their `listing` references, records the decision through the local decision-record library before any of those rows change (DP-03), instructs the transfer through rwb-partner's `issueInstruction` activity as a Temporal child call, answers the case move `RAMC_TRANSFER_PENDING` to rwb-case and publishes no event of its own, because the topic of this service carries only `AssetTakenOn` and `AssetSold`. The ACE NPA sale fact of the legacy data table is retired as a service read because rwb-asset holds no `v_ace_*` grant, so DP-05 applies as a prohibition; the base becomes `/api/recovery/asset/v1` (DP-13); PRT-06 and SCR-21 read through the gateway-bff composite route (DP-19). The pool reference, the transfer price and its template version, the approval reference, the partner element names, the case-move name and the "per agreement" timer have no source and carry the placeholder (GAP-2954; ASM-4852, ASM-4853, ASM-4856); the legacy endpoints name operations of other steps (GAP-2955; ASM-4851); the plan carries no requirement id (GAP-2956; ASM-4855); `asset` is read as S5 (GAP-2957; ASM-4854); the sources are in review and no approval exists (GAP-2958; ASM-4802). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4031-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer (RW-SALEOFF)**, I want **the Workbench to take a pool of assets to RAMC or the joint venture once the committee has approved the route, record the transfer at the governed price and instruct it on the partner portal**, so that **an approved pool leaves the book on the approval decision instead of waiting on a hand-checked listing and a hand-typed floor, and the NPA sales cycle moves from 1,486 days toward its 1,095-day target**.

This is the application slice of legacy RWB-E4-031. It owns:

- the three legacy acceptance criteria, copied verbatim with their origin tag, and the rule, messages, screens and rights they depend on;
- one transfer step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-DIS-59 from `ROUTE_APPROVED_RAMC` on `TRANSFER_INSTRUCTED`, with the DISPOSAL package version in force;
- the transfer record in schema `rwb_asset`: one `asset_sale` row per asset of the pool with its `listing_id`, the dates, the transfer price as the sale price, the fee and the taxes, and no new column;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before any of those rows change (DP-03);
- the instruction of the transfer through rwb-partner's `issueInstruction` activity as a Temporal child call, never as a POST of this service;
- the answer to rwb-case for the case move `RAMC_TRANSFER_PENDING`, with the rule ID and the version that produced it;
- the two reads behind PRT-06 Transfer confirmation and SCR-21 Asset list on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the reads, the transfer element, the instruction element, the consumed rows, the error set and the fakes, which are RWB-S5-E4031-CON; the committee approval, its workflow, its decision and its four-eyes rule, which are rwb-decision's (P7); the partner panel, the instruction, its portal, its result and its fee, which are rwb-partner's (S9); the case of record, its route states, the parent `CaseWorkflow` and the case router, which are rwb-case's (P3); the ACE asset and sale facts, which are rwb-source-data's (P1); the governed template the transfer price is produced from, which is rwb-comms's (P6) and the Calculation Service's; the posting of the transfer and any balance, which are rwb-payment's (P8); the closing row R-DIS-60 and the asset's `TRANSFERRED` status, which belong to the step that posts the transfer; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E4-031 gave the Workbench one step that took a pool of assets to the asset management company or to the joint venture and recorded the transfer. The FSD keeps the objective, the problem and the metric unchanged: the feature "takes a pool of assets to RAMC with committee approval, and records the transfer"; the problem it closes is that "the NPA sales cycle is 1,486 days; listings and floor prices are checked by hand"; and the metric is the NPA sales cycle at 1,095 days, measured on the decision log and the Workbench records and reviewed monthly (FSD S5 A2.22.1). The legacy priority is Must and its dependency is FEAT-APD-01, the approval feature.

What D-RCV-60 changes is who owns the transfer record, the instruction, the approval and the price.

- **the transfer record is this service's.** `asset_sale` and `listing` are S5's rows of `rwb_asset` in the Ownership Map, and Architecture v5 slide 41 gives rwb-asset "assets taken on, holding, floor price, listings, auction rounds". The `asset` row is absent from the Ownership Map table list and is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1, on the same reading the take-on story records (GAP-2957; ASM-4854).
- **the instruction is rwb-partner's.** Architecture v5 slide 19 gives rwb-asset the partner activity `issueInstruction` and the Ownership Map gives the `partner` and `partner_instruction` tables and the partner paths to S9. This service calls the instruction on the partner's queue and never posts it, never holds the instruction row and never reads it (GAP-2954; ASM-4851).
- **the committee approval stays with rwb-decision (P7).** Slide 19 gives rwb-asset "Decision: child: approval", the Temporal and Drools Design puts `ApprovalWorkflow` on queue `rwb-decision` from the kit, and the Ownership Map gives the `approval` table to P7. The approval is the R-DIS-23 route decision (`route = RAMC and committee approved`) that has already moved the case to `ROUTE_APPROVED_RAMC`; this step consumes its answer and approves nothing (GAP-2954; ASM-4851).
- **the case of record stays with rwb-case (P3).** `recovery_case`, `assignment` and `timer` are P3's; this step answers the move instead of writing a case row.
- **the price stays governed.** R-DIS-59's condition is "transfer_price from the template version", its systems are the partner portal and the Calculation Service, and the `template` table is P6's. This story writes the price it is given and never computes it, never holds a default and never writes a percentage (GAP-2954; ASM-4856).
- **no event of its own.** The topic `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` and neither is the RAMC transfer; R-DIS-59's outcome is a case move, answered to rwb-case and not published (ASM-4851).

No business value moves: the transfer price, the fee and the tax treatment are values of the governed template version and of the rule package, read with their versions.

### 3. Preconditions

- RWB-S5-E4031-CON is published: the two read operations, the transfer element, the instruction element, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The DISPOSAL rule package is in force at its version with R-DIS-59, and R-DIS-23 is the row that produced `ROUTE_APPROVED_RAMC`. The package is authored, tested and approved in rwb-decision and loaded here on `RulePackageInForce`; the rule rows and the timer specification stay there (DP-04, DP-06).
- The committee approval is the `ApprovalWorkflow` child of rwb-decision and its answer reaches this step as a workflow signal. No source publishes a REST approval operation and none is called here (GAP-2954; ASM-4851).
- The rwb-partner `issueInstruction` activity is published with its fake, so the transfer can be instructed on Day 1 without a live partner. Its input and output element names and its acceptance codes are Not specified in the source documents (GAP-2954; ASM-4852).
- The rwb-case case-state read and the case-move answer are available for the fake. On the workflow boundary the answer is the stage outcome the parent applies; where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2954; ASM-4852).
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the transfer rows and their record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: PRT-06 and SCR-21 reach this service through the gateway-bff composite route, one hop each (DP-19).
- `asset_sale` and `listing` exist in schema `rwb_asset` from the DB story of this service with the columns of DF-SAL-001 to DF-SAL-019, and `asset` with the columns of DF-COL-028 to DF-COL-042; this story adds no table, no column and no migration (ASM-4853, ASM-4854).
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_sale`, `rwb_case`, `rwb_partner` or `rwb_decision` is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline, and the missing approval of the realigned stories is recorded rather than waited for (GAP-2958; ASM-4802).

### 4. Flow

1. R-DIS-23 has already run: the route is `route = RAMC and committee approved`, the committee has approved through the rwb-decision child workflow, and the case of record sits in `ROUTE_APPROVED_RAMC` (Business Rules and Routing Logic v4 R-DIS-23).
2. The case event `TRANSFER_INSTRUCTED` reaches the case router in rwb-case, which signals the parent `CaseWorkflow`; the parent forwards it to the child `AssetDisposalWorkflow` on queue `rwb-asset` (ASM-4851).
3. The step reads the case state on the rwb-case contract, read only, to confirm `ROUTE_APPROVED_RAMC` and to take the case reference, the account link and the route outcome the signal carries, one hop with a 2 s budget and a breaker.
4. The step takes the pool from its own rows: the `asset` rows of the case with `holding_status` `HELD` or `LISTED`, and for each of them its `listing` row against the `LOV-SALE-CHANNEL` value `RAMC`. No row of another schema is read (DP-01).
5. `RamcTransferEvaluator` loads the DISPOSAL package version in force and evaluates R-DIS-59 — from `ROUTE_APPROVED_RAMC` on `TRANSFER_INSTRUCTED`, condition "transfer_price from the template version" — and answers the rule ID, the package version, the action and the case move the rule names (TSD S5 T4).
6. Where no rule fires, or the transfer price with its template version is absent from the facts of the case, the step changes nothing and reports the reason to the parent (VR-S5-022-1, MSG-GEN-001).
7. `RamcTransferDecisionRecordWriter` writes one decision record through the local library **before any change**: the case reference, the pool reference, the rule ID and the package version, the inputs reference with the template version of the price, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
8. `RamcTransferWriter` writes the transfer record in one `rwb_asset` transaction with the decision record, the idempotency row and the optimistic lock: one `asset_sale` row per asset of the pool — `id` (DF-SAL-009), `asset_id` (DF-SAL-010), `listing_id` (DF-SAL-011) where the asset has a listing, `contract_date` (DF-SAL-012), `sale_date` (DF-SAL-013), `sale_price` (DF-SAL-014) set to the transfer price in force, `transfer_fee` (DF-SAL-015), `specific_business_tax` (DF-SAL-016), `corporate_income_tax` (DF-SAL-017), `gain_loss` (DF-SAL-018) by its formula and `incentive_amount` (DF-SAL-019) where the facts give one. No `asset` and no `listing` status changes here, because R-DIS-60 posts the transfer.
9. The step calls rwb-partner's `issueInstruction` activity on the partner's queue with the case reference, the pool reference, the partner that receives the pool, the transfer price with its template version and the approval reference. The answer carries the partner's instruction reference and its acceptance and is recorded in the workflow history and the step outcome, because `asset_sale` has no column for it (GAP-2954; ASM-4852).
10. `CaseMoveAnswer` answers rwb-case with `RAMC_TRANSFER_PENDING`, the rule ID, its version, the template version of the price, the pool reference and the instruction reference. rwb-case writes the case row and its route state; this service writes neither.
11. A repeated `TRANSFER_INSTRUCTED` for the same case, pool and template version writes nothing, calls no second instruction, sends no second answer and counts the repeat; the replay reuses the first recorded activity result.
12. PRT-06 Transfer confirmation in its pending and confirmed states and SCR-21 Asset list in its loading and list states read the transfer record, the pool and its prices from this service through the gateway-bff composite route, read only, next to the case state of rwb-case and the instruction state of rwb-partner (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no `asset_sale` row, no record, no instruction and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E4-031-03, TC-E4-031-05 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC1, TC-E4-031-04 |
| X3 | The case is not in `ROUTE_APPROVED_RAMC` | 409 and nothing is written; the transfer is not re-evaluated on a case that has already moved | None | AC2 |
| X4 | The transfer price or its template version is absent from the facts of the case | No rule fires: nothing changes, no record is written, the case keeps its state and the reason goes to the parent | MSG-GEN-001 | AC1, AC2 |
| X5 | The rwb-partner activity exhausts its retry policy, or the rwb-case read does not answer inside 2 s | The workflow retries on the platform policy of 1 s, back-off 2, 10 attempts; the rows stay as written and no move is answered until the call succeeds; a screen read answers 503 with the envelope | None | AC2 |
| X6 | The partner refuses the instruction | The refusal is recorded as the outcome in a second decision record, no move is answered and the case stays in `ROUTE_APPROVED_RAMC`; the refusal code is Not specified in the source documents (GAP-2954; ASM-4852) | None | AC2 |
| X7 | A repeated `TRANSFER_INSTRUCTED` for the same case, pool and template version | One set of rows, one record, one instruction and one answer; the repeat is counted | None | AC1, AC2 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, a `partner_instruction` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 to X4 are the exception paths of RWB-E4-031 and of FSD S5 A2.22.4.3 carried onto the split, X5 to X7 are the paths the target call types and the instruction add, and X8 is the DP-01 and DP-05 boundary. The transfer price, the fee and the tax treatment of X4 and X6 are values in force, so none of them is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E4031-CON, the rwb-partner, rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live S9, P3, P6, P7 or P8 |
| Negotiable | The step activity name, the decision code per outcome and the shape of the stage outcome are this story's choice; the rule, the messages, the screens, the two reads and the `asset_sale` columns are fixed |
| Valuable | An approved pool is instructed to RAMC or the joint venture and its transfer is on the record at the governed price in the same step that moves the case |
| Estimable | One workflow step, one evaluator, one record write, one set of `asset_sale` rows, one child call, one case-move answer, one client and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and pools through the contract fakes, plus the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Transfer a pool to RAMC or the joint venture

  Background:
    Given case "RC-2026-000512" carries the pool "POOL-2026-000512" of assets "AST-2026-000512" and "AST-2026-000513"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-59
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Transfer a pool to RAMC or the joint venture (legacy RWB-E4-031 AC1)
    Given the rwb-case contract mock returns the case state "ROUTE_APPROVED" for "RC-2026-000512"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes a pool of assets to RAMC with committee approval, and records the transfer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-59 (legacy RWB-E4-031 AC2)
    Given the rwb-partner contract mock returns the RAMC transfer instruction accepted with its reference "INS-2026-000512"
    Given the rwb-case contract mock returns the case state "ROUTE_APPROVED_RAMC" for "RC-2026-000512"
    Given a case in state ROUTE_APPROVED_RAMC
    When transfer instructed
    Then instruct the RAMC or joint venture transfer on the portal
    Then the case moves to RAMC_TRANSFER_PENDING

  Scenario: AC3 Not recorded (legacy RWB-E4-031 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E4-031 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the legacy wording of `the user acts on the screen`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry the `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions. What the legacy lines describe happens in four places in the target: rwb-case holds the case and its route states; rwb-decision holds the committee approval and the rule package and its answer reaches the step as a signal; this story evaluates R-DIS-59, writes the record and the `asset_sale` rows and answers the move; rwb-partner instructs the transfer and answers with its reference. AC1's "records the transfer" is the `asset_sale` rows of the pool, AC1's "with committee approval" is the R-DIS-23 approval the case already carries, and AC2's move is answered and never written here (GAP-2954; ASM-4851). The legacy `v_ace_npa_sale` read is not reproduced as a service read anywhere in this story (BR3).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-59 | Asset disposal | D8.1 to D8.3 | ROUTE_APPROVED_RAMC | TRANSFER_INSTRUCTED | transfer_price from the template version | Instruct the RAMC or joint venture transfer on the portal | RAMC_TRANSFER_PENDING | RAMC | Partner Portal, Calculation Service | per agreement |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its owner column is a business role and not a service: the partner is the role "RAMC", the portal is rwb-partner's surface, the calculation is the Calculation Service's, and the case move is written by rwb-case on this story's answer. The timer cell says "per agreement" and names no duration, so the step reads the timer specification of the rule row in force as governed data and holds no value of its own (GAP-2954; ASM-4856).

| ID | Rule | Source |
|---|---|---|
| BR1 | The transfer record is this service's: the `asset_sale` rows and their `listing` references are columns of `rwb_asset`, and no other service writes them | Architecture v5 slide 41; TSD S5 T3.1 |
| BR2 | The decision is recorded before any transfer row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S5 T2; legacy AC1 and AC3 |
| BR3 | The ACE NPA sale and asset facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the facts on the owner's data-product contract only | DP-05; Architecture v5 slides 29, 37 and 45 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (`recovery_case` owner P3) |
| BR5 | The instruction is rwb-partner's: this service calls the partner's activity and holds no `partner` row, no `partner_instruction` row and no partner user | Ownership Map (`partner`, `partner_instruction` owner S9); DP-01 |
| BR6 | The approval is rwb-decision's: `approval`, `decision_log_entry` and `rule_row` are P7's, and this story consumes the approval answer and the package and approves nothing | Ownership Map; Architecture v5 slide 19 |
| BR7 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id`, `asset_id` and `listing_id` are identifiers, not foreign keys across schemas | DP-01; TSD S5 T3.3 |
| BR8 | Every value a business person may change is reference data, a rule row or a template version read with its version: the transfer price and the fee, `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING`, `LOV-SEGMENT` and the timer specification of R-DIS-59 | TSD S5 T3.2; FSD S5 BR-S5-022; legacy Guardrails |
| BR9 | The step publishes no event: `AssetTakenOn` and `AssetSold` are the service's only two, and a build that adds a third on the topic fails the absence test | Architecture v5 slide 19; slide 43 |
| BR10 | The same pool under the same template version writes once, instructs once and answers once | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR11 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, the instruction input, a log or a workflow history | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent applies it (BR4). What this story owns is the transfer record of the pool and the state of the step.

| From (`asset_sale` of the pool) | Event | Condition | To |
|---|---|---|---|
| No row for the asset of the pool | `TRANSFER_INSTRUCTED` under R-DIS-59 | transfer_price from the template version present | One `asset_sale` row per asset with its `listing_id`, and the case-move answer `RAMC_TRANSFER_PENDING` |
| A row for the same case, pool and template version | The same `TRANSFER_INSTRUCTED` | X7 | Unchanged, the repeat counted, no second instruction |
| No row for the asset of the pool | `TRANSFER_INSTRUCTED` without a transfer price or its template version | X4 | No row, no record and no answer |
| A row for the pool | The partner refuses the instruction | X6 | The rows stay, the refusal is recorded, no move is answered |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | `TRANSFER_INSTRUCTED` for a case in `ROUTE_APPROVED_RAMC` | The package in force is loaded | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | The `asset_sale` rows are written and the transaction commits | The commit succeeds | Instructing |
| Instructing | The partner answer carries its reference and its acceptance | The answer is recorded | Answering the case move, then waiting |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Instructing | The partner activity exhausts its retries | X5 | Waiting, the rows written, no move answered |

`ROUTE_APPROVED_RAMC` and `RAMC_TRANSFER_PENDING` are states of the DISPOSAL machine of TSD S5 T4 and live on the case of record. The closing row R-DIS-60 (`RAMC_TRANSFER_PENDING` → `ASSET_TRANSFERRED` on `TRANSFER_COMPLETED`) is not this story's and is named only to show where the `TRANSFERRED` holding status comes from.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1: the primary role of the feature, holding C, R, U and A and acting on PRT-06 and SCR-21 |
| RW-NPAMGR, NPA and asset manager | Asset and disposal CRU: reads the pool and corrects the transfer facts, and is the "Head of NPA" also-user of FSD S5 A2.22.3.3 |
| RW-ENFORCE, enforcement owner | Asset and disposal CRU: reads the pool and the transfer record |
| RW-HEADNPA, RW-HEADASL, RW-PRODHEAD | Asset and disposal RA: read, and approve through the approval path where a committee level is needed |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-LEGAL, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| PT-RAMC, RAMC user | Asset and disposal RU as the matrix gives it: the receiving partner confirms its own instruction on the partner portal and never reads the Workbench transfer record |
| PT-AUCTION, PT-VALUER | Asset and disposal RU or R as the matrix gives it: read of the pool through the partner gateway only |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step under the same checks |
| rwb-asset service identity | Runs the step, evaluates the rule, writes the record and the rows, calls the partner activity and answers the move; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S5 T6.1 and the roles of FSD S5 A2.22.3.3, and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-SAL-009 | asset_sale (S5, `rwb_asset`) | id | Write, the transfer record of one asset of the pool |
| DF-SAL-010 | asset_sale (S5, `rwb_asset`) | asset_id | Write, the asset of the pool |
| DF-SAL-011 | asset_sale (S5, `rwb_asset`) | listing_id | Write, the listing the pool is offered through, where one exists |
| DF-SAL-012 | asset_sale (S5, `rwb_asset`) | contract_date | Write, the contract date of the transfer, from AMIS per TSD S5 T3.1 |
| DF-SAL-013 | asset_sale (S5, `rwb_asset`) | sale_date | Write, the date of the transfer |
| DF-SAL-014 | asset_sale (S5, `rwb_asset`) | sale_price | Write, the transfer price in force with its template version |
| DF-SAL-015 | asset_sale (S5, `rwb_asset`) | transfer_fee | Write, where the facts of the case give the fee |
| DF-SAL-016 | asset_sale (S5, `rwb_asset`) | specific_business_tax | Write, where the facts give the tax |
| DF-SAL-017 | asset_sale (S5, `rwb_asset`) | corporate_income_tax | Write, where the facts give the tax |
| DF-SAL-018 | asset_sale (S5, `rwb_asset`) | gain_loss | Write, by its formula from the sale price and the book value |
| DF-SAL-019 | asset_sale (S5, `rwb_asset`) | incentive_amount | Write, where the facts give an incentive |
| DF-SAL-001 to DF-SAL-008 | listing (S5, `rwb_asset`) | id, asset_id, sale_channel, start_price, floor_price, round_no, listed_at, status | Read only: the pool's listing and its `RAMC` sale channel; no listing row changes here |
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | id, case_id, asset_ref, asset_type, holding_status and the other columns | Read only: which assets form the pool and their book value; no asset row changes here |
| Standard columns | asset_sale and listing (S5, `rwb_asset`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write for the `asset_sale` rows, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the transfer rows change |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the route state | Not read as a table: the state and the route outcome arrive on the rwb-case read and on the signal |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | the officer assignment of the case | Not read and not written: the screen shows it from rwb-case |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code, action_text, timer_spec and the rest | Not read as a table: the rule and its timer specification arrive on the package in force |
| DF-ACE-220 to DF-ACE-230 | `v_ace_npa_sale` (P1) | npa_sale_key, npa_asset_key, contract_date, sale_date, sale_price, transfer_fee and five more | Not read: this service holds no `v_ace_*` grant, the fields are the `asset_sale` columns written here, and DP-05 applies as a prohibition (BR3) |

Field IDs are those of TSD S5 Assets and auction v2 T3.1 and of the Logical Data Model and Data Dictionary; the ACE row is the row the legacy Data table lists, with its owner changed to P1 by the target. **No new table, no new column and no migration**: the three tables arrive with the DB story of this service, this story writes eleven `asset_sale` columns, and `decision_record` and `idempotency_key` are library objects created in `rwb_asset` by the library's migration (DP-03). The pool, the transfer price reference and the approval reference have no column of their own: the pool is the set of `asset_sale` rows of the case, the price reference is its template version carried in the decision record, and the approval and instruction references ride in the decision record and the workflow history (GAP-2954; ASM-4853).

**No personal data.** The rows carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_asset`, the record, the instruction input, a log or a workflow history, and every fixture is synthetic. The partner, its users and its fees are rwb-partner's and are referenced by identifier, not copied.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes RWB-S5-E4031-CON declares, and it provides no operation that issues the transfer.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated, with the sale channel and the transfer state of the pool (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and its `asset_sale` references (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors are 400, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 and 503 when the decision library or a consumed contract does not answer. The operation IDs are those of TSD S5 T-A.1. `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's under the Ownership Map ruling ASM-0043; `POST /assets/{assetId}/listings` (API-S5-004) and `POST /listings/{listingId}/rounds` (API-S5-005) belong to the pricing and auction stories of this service; `POST /cases/{caseId}/instructions` is rwb-partner's (S9). None is built or declared here, and the legacy endpoints table names the first two although this step calls neither (GAP-2955; ASM-4851).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state `ROUTE_APPROVED_RAMC`, the case reference, the account link and the route outcome with the transfer price and its template version; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2954; ASM-4852)) | rwb-case (P3) | P3 rwb-case | The answer that carries `RAMC_TRANSFER_PENDING` with the rule, its version, the pool and the instruction reference; on the workflow boundary it is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2954 (ASM-4851).

#### 12.3 Events published

None. The topic `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` and neither is the RAMC or joint venture transfer. R-DIS-59's outcome is a case move answered to rwb-case, so this step writes no outbox row, joins no consumer group, and a build that publishes a third event on the topic fails the absence test (BR9; ASM-4851).

#### 12.4 Events consumed

None. Architecture v5 slide 19 gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is the committee approval, the transfer price or the case state. `PartnerResultSubmitted` belongs to the step that closes the transfer under R-DIS-60. `TRANSFER_INSTRUCTED` reaches this step as the case event the parent forwards, on the case router's subscription in rwb-case, so this story holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | Input: the case, the route, the pool reference and the package in force; signals: the case state from rwb-case, the package in force, the R-DIS-23 route outcome with the transfer price and its template version, and the approval answer |
| `transferToRamc` | Activity, the one transfer step | `rwb-asset` | The case, the pool and the route outcome in; the rule ID with its package version, the transfer rows, the instruction reference and the case move out, with the record and the rows written in one transaction |
| `issueInstruction` | Activity of rwb-partner (S9), called as a Temporal child call; Architecture v5 slide 19 gives it to this service | `rwb-partner` | In: the case reference, the pool reference, the partner, the transfer price with its template version and the approval reference. Out: the instruction reference and the acceptance. Element names Not specified in the source documents (GAP-2954; ASM-4852) |
| `ApprovalWorkflow` | Workflow of rwb-decision (P7), started by the route step under R-DIS-23 and not by this story | `rwb-decision` | Its answer reaches this step as a signal; no REST approval operation is published by any source (GAP-2954; ASM-4851) |

The step activity name is a target design choice fixed by no source. The trigger is read as the case event `TRANSFER_INSTRUCTED` forwarded by the parent, because the legacy story runs the step once the route is approved and the FSD declares no background event for the feature (FSD S5 A2.22.4.4). No child workflow for the case and none for the money exists in this service.

#### 12.6 Schedules

None. The step runs from the case event and from the signals the parent forwards, and owns no Temporal Schedule and no legacy Quartz job. The R-DIS-59 timer cell "per agreement" is a governed timer specification read with the rule row in force, not a Schedule of this service (GAP-2954; ASM-4856). The single Schedule of this service is JOB-19 re-appraisal monthly, owned by RWB-S5-E3026-APP.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The transfer record of each asset of the pool; this story inserts the rows and writes the columns of §11 |
| listing | S5 (`rwb_asset`) | The listing the pool is offered through; read only here, written by the pricing stories |
| asset | S5 (`rwb_asset`) | The assets of the pool; read only here, no holding status changes in this step (GAP-2957; ASM-4854) |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated event and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `partner` and `partner_instruction` (S9), `template` (P6), `proceeds` (P8), `document` (P5) and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | The state `ROUTE_APPROVED_RAMC` of case `RC-2026-000512` with the pool reference and the transfer price with its template version; the state `ROUTE_APPROVED`; a case already moved to `RAMC_TRANSFER_PENDING` | AC1, AC2, X3 |
| rwb-case case-move fake | The move `RAMC_TRANSFER_PENDING` accepted, carrying the pool and the instruction reference; a move refused because the case is not in `ROUTE_APPROVED_RAMC` | AC2, X3 |
| rwb-partner instruction fake | The instruction of pool `POOL-2026-000512` accepted with its reference `INS-2026-000512`; a refusal with its code; no answer beyond the retry policy | AC2, X5, X6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-59 and the timer specification of its row | AC1, AC2, X4 |
| rwb-decision approval fake | The committee approval of the RAMC route for case `RC-2026-000512`, with its approval reference and the transfer price it approved | AC1, AC2 |
| rwb-source-data data-product fake | The ACE NPA asset fact of each asset of the pool with its reference, type, segment and book value, and a stale product with its date | AC1, X4 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged PRT-06 and SCR-21 answer for case `RC-2026-000512`, with the transfer facts read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case read and of the case-move answer and the element names of the partner instruction are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2954; ASM-4852).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two reads on `/api/recovery/asset/v1`; the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `AssetTakenOn` and `AssetSold` stay the service's only two |
| Temporal | 1 workflow, 1 step activity, 1 partner child call, 1 approval answer as a signal | `AssetDisposalWorkflow`, `transferToRamc` on `rwb-asset`, `issueInstruction` on `rwb-partner`, the `ApprovalWorkflow` answer on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `transfer`, package `th.co.scb.ace.workbench.recovery.asset.transfer`; front end `src/modules/recovery/asset/AssetTransfer.tsx`, the fragment PRT-06 and SCR-21 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the asset facts are the ones the rwb-source-data contract answers or the ones this step writes itself. DP-03 is the transaction rule of the step: the record and the rows commit together or not at all. DP-13 moves the base of the two reads and nothing else. DP-19 is how PRT-06 and SCR-21 reach this service, one hop through the gateway. DP-09 is not in the pattern set and is not needed, because the step publishes no event.

**Dependencies the tables add and the plan does not hold.** The rwb-case rows, the rwb-partner activity and the rwb-decision approval are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2954 (ASM-4851). The two platform rows, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, are the ones the plan's H row already carries.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` transfer branch | Workflow | Waits for `TRANSFER_INSTRUCTED`, loads the package in force, calls the partner and reports the outcome to the parent |
| `transferToRamc` | Activity | The one step: read the case and the pool, evaluate R-DIS-59, write the record and the rows, call the partner, answer the move |
| `RamcTransferEvaluator` | Service | The rule evaluation against the package version in force, with the transfer price, its template version and the timer specification |
| `RamcTransferDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked, and refuses the step on a failed write (DP-03) |
| `RamcTransferWriter` | Repository | Inserts the `asset_sale` rows with their `listing_id` references in one transaction, with the idempotency row and the optimistic lock |
| `PartnerInstructionClient` | Client | The `issueInstruction` child call on `rwb-partner`, with the platform retry policy, the refusal path and no second instruction on a repeat |
| `CaseStateClient` | Client | The case state read and the case-move answer of rwb-case, one hop, 2 s |
| `AssetController` | Controller | The two reads, the capability area and right, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 |
| `AssetTransfer` | React component | Shows the pool, its transfer state and its prices on PRT-06 and SCR-21, read only, with the refusal and failure states |

**Database and migrations.** No Flyway file. The three tables arrive with the DB story, and the record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No column is added for the pool, the price reference, the approval reference or the instruction reference (GAP-2954; ASM-4853).

**Configuration and reference data.**

- `LOV-SALE-CHANNEL` (the `RAMC` value of the listing), `LOV-LISTING`, `LOV-HOLDING` and `LOV-SEGMENT` at their version in force, read as reference data and never as constants.
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision and loaded on `RulePackageInForce`; the timer specification of R-DIS-59 and the transfer price rule of R-DIS-23 are values of the package and of the governed template, not of this build.
- The governed template version the transfer price is produced from is P6's `template` row and the Calculation Service's output; this service reads the price and its version and computes neither.
- The capability area "Asset and disposal" and its rights are access rows, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020, and the child call uses the platform retry policy of 1 s, back-off 2, 10 attempts.

**Build steps**

1. The transfer branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset` as the stage child of `CaseWorkflow`, with `TRANSFER_INSTRUCTED` as its trigger.
2. `CaseStateClient` against its fake, with the 2 s budget, the breaker, the wrong-state path and the no-answer path (AC1, AC2, X3, X5).
3. `RamcTransferEvaluator` over the package, with R-DIS-59, the transfer price and its template version, the timer specification and the no-fire path (AC1, AC2, X4).
4. `RamcTransferDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X1).
5. `RamcTransferWriter` with the one transaction, the eleven columns, the `listing_id` references, the idempotency row and the optimistic lock (AC1, X7).
6. `PartnerInstructionClient` against the partner fake, with the acceptance, the refusal and the retry exhaustion (AC2, X5, X6).
7. `CaseMoveAnswer` and the parent signal, with the one move `RAMC_TRANSFER_PENDING` (AC2).
8. `AssetController` with the rights, the pagination and the problem mapping (AC1).
9. `AssetTransfer` and the two screens through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_case`, `rwb_partner`, `rwb_decision` or `rwb_payment` (X8, BR3, BR5).

**Feature flag.** `rwb.asset.ramc-transfer-v1`, a flag of the platform library; off means the step holds the event, writes nothing, calls no partner and answers no move.

**Done when.** The tests of section 16 pass, the step runs from a synthetic `TRANSFER_INSTRUCTED` in SIT, the pool's rows and their record are written, the instruction is accepted on the partner fake, the move is answered, a repeated event writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and PRT-06 and SCR-21 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's values, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of the transfer facts is absent or invalid: the price, its template version, the pool reference or the approval reference (X4, VR-S5-022-1) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset list or the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the transfer rows change (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are those of the legacy message set and of FSD S5 A2.22.3.1, and the text is copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the set of the feature, and no path of this story raises them. The refusal code of the partner instruction (X6) has no message in any source and is Not specified in the source documents (GAP-2954; ASM-4852).

### 15. Screens and states

PRT-06 Transfer confirmation in its pending and confirmed states and SCR-21 Asset list in its loading and list states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the pool, its transfer record and its prices, rwb-case for the case and its route state, rwb-decision for the approval reference and rwb-partner for the instruction state; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. PRT-06 is the partner portal's confirmation surface, which the partner gateway serves with rwb-partner, and the Workbench reads the same state through the composite route; no source names the service that owns its field list (GAP-2954; ASM-4852).

The states this story produces are the transfer state of PRT-06 — instructed and pending, or confirmed on the partner's answer — and the refusal and failure states: refused with MSG-P4-002, not recorded with MSG-P7-003 and an absent price with MSG-GEN-001. The confirmed state closes under R-DIS-60 and belongs to the step that posts the transfer.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-031-01 | AC1 | Component | Case `RC-2026-000512` with pool `POOL-2026-000512` of two assets; the `asset_sale` rows, the decision record and the case move asserted on the fakes |
| TC-E4-031-02 | AC2 | Integration | The `TRANSFER_INSTRUCTED` event end to end: the rwb-case state read, the R-DIS-59 answer, the instruction accepted with `INS-2026-000512` and the `RAMC_TRANSFER_PENDING` move answered |
| TC-E4-031-03 | AC3 | Component | The decision-record stub stopped; nothing written, no instruction sent and MSG-P7-003 shown |
| TC-E4-031-04 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E4-031-05 | Principle 5 | Component | A forced decision log write failure at the moment of the insert; no row, no instruction and no answer |

The five legacy cases are the legacy cases of RWB-E4-031 in their legacy order, with the Level column added: the legacy `System` level maps to `Component` where the step is tested on its fakes, and TC-E4-031-02 maps to `Integration` because it crosses the rwb-partner and rwb-case boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the transfer price and the fee, the tax treatment, the timer specification, the four list values and the rule rows stay data, reference data, a governed template version or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in the partner instruction input, in a workflow input or history, or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the asset facts arrive on the rwb-source-data contract (DP-05).
- The case stays with rwb-case, the approval and the rule rows with rwb-decision, the partner and its instruction with rwb-partner, and the money with rwb-payment: no `recovery_case` row, no `approval` row, no `partner_instruction` row, no posting and no balance is written here (BR4, BR5, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No event is published by this step, and no retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no third event on the topic (BR9).
- The decision is recorded before the change; a build that writes the rows before the record, or calls the partner before the record, fails the review (DP-03).
- The instruction is a child call and never a POST of this service: a build that adds a partner path to this service's document or controller fails the boundary test (BR5).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-2956; ASM-4855) | The plan carries no requirement id for this slice and TSD S5 T8 maps its rows to FEAT-AST-01 and FEAT-AST-08 only; the feature is FEAT-AST-22 "Transfer a pool to RAMC or the joint venture" with the objective, problem and metric of FSD S5 A2.22.1, and the legacy requirement it serves is RWB-E4-031 | The transfer step, the `asset_sale` rows and the case-move answer | TC-E4-031-01, TC-E4-031-02, TC-E4-031-03 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the transfer record | TC-E4-031-01 |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E4-031-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget | TC-E4-031-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the change | TC-E4-031-03, TC-E4-031-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-031, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by this story |
| Test cases | TC-E4-031-01 to TC-E4-031-05 |
| Feature and screens | FEAT-AST-22, PRT-06 Transfer confirmation and SCR-21 Asset list |
| Rules | R-DIS-59, governed in rwb-decision; R-DIS-23 and R-DIS-60 are the rows before and after this step and are not owned here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two reads, the transfer element, the instruction element, the consumed rows, the error set and the fakes: RWB-S5-E4031-CON.
- The committee approval, the `ApprovalWorkflow` child, the `approval` table and R-DIS-23: rwb-decision (P7) (GAP-2954).
- The partner panel, the instruction, its portal, its result, its fee and its scorecard: rwb-partner (S9).
- The case of record, its route states, the parent `CaseWorkflow` and the case router: rwb-case (P3).
- The governed template the transfer price is produced from and the Calculation Service: rwb-comms (P6).
- The ACE NPA asset and sale facts, the correctness and the freshness of the data product: rwb-source-data (P1).
- R-DIS-60 and the posting of the transfer, the proceeds and any balance: the step that completes the transfer and rwb-payment (P8).
- The listing, the floor price and the auction rounds: the pricing and auction stories of this service, API-S5-004 and API-S5-005.
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043 (GAP-2955).
- The gateway-bff composite route and the field lists of PRT-06 and SCR-21: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

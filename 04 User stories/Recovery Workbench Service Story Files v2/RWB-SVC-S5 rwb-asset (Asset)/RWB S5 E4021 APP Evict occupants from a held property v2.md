# RWB-S5-E4021-APP Evict occupants from a held property

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-M |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S5-E4021-APP-16) |
| Depends on (build) | RWB-S5-E4021-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version built against | Not specified in the source documents (DOR-RWB-S5-E4021-APP-23) |
| Contract fake library version | Not specified in the source documents (DOR-RWB-S5-E4021-APP-22) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs; TSD S5 v2 T8 maps REQ-S5-006 to REQ-S5-010 to FEAT-AST-08; the split plan has no requirement row yet for RWB-S5-E4021-APP or RWB-S5-E4021-CON, GAP-2890 and GAP-2894; ASM-4787) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-021 split out for rwb-asset. The three legacy acceptance criteria are kept word for word with their origin tag; the step becomes the eviction branch of `AssetDisposalWorkflow` on task queue `rwb-asset`, takes the occupancy refusal the parent forwards after the sale officer records it, evaluates R-DIS-13 with the DISPOSAL package version in force, writes the eviction status and its instruction reference in `rwb_asset`, records the outcome through the local decision-record library before the row changes (DP-03), answers the case move to rwb-case with the instruction to Legal and publishes no event of its own. The legacy `v_ace_npa_asset` read is retired as a service read and arrives on the rwb-source-data data-product contract (DP-05); the base becomes `/api/recovery/asset/v1` (DP-13); SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). No source names a table, a column or an element for the occupancy refusal and the eviction record (GAP-2888; ASM-4785), no source publishes an operation for the officer action, the case answer or the instruction to Legal (GAP-2889; ASM-4786), the split plan carries no requirement row for this slice (GAP-2890; ASM-4787) and the legacy screen list has no eviction state (GAP-2891; ASM-4788). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (25 resolved, 12 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **sale officer**, I want **to open and track the eviction, which needs Legal and has no legal owner today**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E4-021. It owns:

- the three legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rule, the messages and the screens they depend on;
- one eviction step of `AssetDisposalWorkflow` on task queue `rwb-asset` in namespace `rwb-recovery`, as a stage branch of the workflow the case owns the parent of (Architecture v5 slide 13, "Asset disposal rwb-asset");
- the evaluation of R-DIS-13 on the occupancy fact of the held asset, with the DISPOSAL package version in force;
- the eviction record of the case and the asset in schema `rwb_asset`: its status and its instruction reference, written against the `asset` row where the sources give a column (GAP-2888; ASM-4785);
- the local decision record of the rule outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03);
- the answer to rwb-case for the case move `EVICTION_REQUIRED`, with the instruction to Legal, the rule ID and the version that produced them;
- the two reads behind SCR-21 Asset list and SCR-22 Asset record on base `/api/recovery/asset/v1`, reached through the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the two reads, the stage signal, the case-move answer, the decision-record element, the error set and the fakes, which are RWB-S5-E4021-CON; the case of record, the route states `ASSET_HELD` and `EVICTION_REQUIRED`, the parent `CaseWorkflow`, the case timers and the routing of the instruction to rwb-litigation, which are rwb-case's (P3); the eviction itself, its legal steps and their outcome, which are rwb-litigation's (S4); the return to hold after possession is taken, which is the disposal-route story's under R-DIS-14 (FSD S5 A2.10); the holding costs, the work orders and the custody of the property, which are the held-property story's of this service (FEAT-AST-07); the ACE NPA asset facts, which are rwb-source-data's (P1); the rule package and its version, which are authored and approved in rwb-decision (P7); the partner-instruction surface, which is neither named by a source read here nor S5's (GAP-2889; ASM-4786); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E4-021 gave the Workbench the one step of the disposal journey that no service owned: an occupant refuses possession, the sale officer opens an eviction, the file goes to Legal and the asset sits on the books until possession is taken. The FSD keeps the feature as FEAT-AST-08 "Evict occupants from a held property" in module S5, with the sale officer as the acting role and the eviction instruction as its outcome (FSD S5 A2.8). The declared objective of the module is unchanged: assets sell sooner at approved prices, and the step is closed on the decision log instead of on a side file.

What D-RCV-60 changes is who owns the decision, the case and the legal act.

- **the decision is this service's.** R-DIS-13 sits in the DISPOSAL route set of rwb-asset (Architecture v5 slide 13, "rwb-asset · DIS 72"). The rule is evaluated here, the outcome is recorded here, and the eviction status of the asset is written here.
- **the case stays with rwb-case (P3).** `recovery_case`, `assignment`, `task` and `timer` are P3's and the states `ASSET_HELD` and `EVICTION_REQUIRED` live there. This story evaluates the rule and **answers** the case move; it writes no case row.
- **Legal stays with rwb-litigation (S4).** The instruction is raised here and is acted on there; the enforcement, its deadlines and its outcome are S4's, and this service neither performs a legal step nor holds a partner instruction of its own (GAP-2889; ASM-4786).
- **the ACE facts stay with rwb-source-data (P1).** The legacy data table names `v_ace_npa_asset`; in the target only rwb-source-data reads the `recovery.v_ace_*` views (Architecture v5 slides 29 and 37), so DP-05 applies as a **prohibition** and the asset facts arrive on the owner's contract and are held on this service's own `asset` row.
- **the decision is recorded first**, through the local decision-record library of DP-03, in the same transaction as the eviction row. That is what legacy AC1 asks for and what legacy AC3 tests.
- **nothing is published.** Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` and `AssetSold`, so this step publishes nothing and the absence is stated in §12.3.

No business value moves in this story: the occupancy fact, the eviction instruction and the statuses are read from the signal, from reference data and from the rule package, each with its version, and none is written in code.

### 3. Preconditions

- RWB-S5-E4021-CON is published: the two asset reads, the stage signal, the case-move answer, the decision-record element, the error set and the fakes are baselined and handed to this story.
- The case workflow boundary is in force: `CaseWorkflow` on `rwb-case` runs one child per stage on the owner's queue, and the child here is `AssetDisposalWorkflow` on `rwb-asset` in namespace `rwb-recovery` (Architecture v5 slide 13).
- The occupancy refusal is recorded by the sale officer on the case and reaches the running child as a signal from the case router; no source publishes the operation name of the officer action or of the signal, so both are stubbed from their documents (GAP-2889; ASM-4786).
- The possession result reaches the same child the same way, from the case router, and the eviction is tracked to that point. No event subscription of this service carries it (GAP-2889; ASM-4786).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the eviction row and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-21 and SCR-22 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `asset` exists in schema `rwb_asset` from the DB story of this service, with the columns of TSD S5 T3.1 and the standard record columns of TSD S5 T3.0; this story adds no table, no column and no migration. The TSD S5 T3.1 gives the `asset` object no occupancy and no eviction field, and no source names one (GAP-2888; ASM-4785).
- The DISPOSAL rule package is in force at its version with R-DIS-13; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows and the reference data behind them are governed there and are not listed for this story.
- The service runs as its own login on schema `rwb_asset`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset`, `rwb_case` or `rwb_litigation` is refused by the database and fails the boundary test (DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S5-E4021-CON when its tests pass.

### 4. Flow

1. The case is in `ASSET_HELD` and its `AssetDisposalWorkflow` child runs on `rwb-asset`. The sale officer finds the property occupied and records the refusal on the case in the case workspace; the case router of rwb-case forwards the occupancy fact to the running child as a signal with the case reference, the asset reference, the occupancy status and the recorded-at time (Architecture v5 slide 13; GAP-2889; ASM-4786).
2. The eviction step reads the asset of the case from its own `asset` row: the asset reference, the asset type, the transfer-in type, the holding status and the case link (TSD S5 T3.1). No `v_ace_*` view and no neighbour's row is read (DP-05).
3. The step loads the DISPOSAL package version in force and reads the R-DIS-13 row with its condition set.
4. `EvictionEvaluator` evaluates R-DIS-13 on the fact: from `ASSET_HELD`, on `OCCUPANTS_REFUSE_POSSESSION`, when `occupancy_status = occupied`, it raises the eviction instruction to Legal and the case moves to `EVICTION_REQUIRED` (Business Rules and Routing Logic v4).
5. `AssetDecisionRecordWriter` writes one decision record through the local decision-record library **before any change**: the case reference, the asset reference, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
6. `EvictionWriter` writes the eviction status of the asset and its instruction reference in one `rwb_asset` transaction with the decision record, the inbox row and the idempotency row, against the `asset` row where the sources give a column (GAP-2888; ASM-4785).
7. `CaseMoveAnswer` answers rwb-case with `EVICTION_REQUIRED` and the instruction to Legal it carries: the case reference, the asset reference, the instruction reference, the rule ID and the version, and the decided-at time. rwb-case writes the `recovery_case` row and its route state and routes the instruction to rwb-litigation; this service writes neither (GAP-2889; ASM-4786).
8. The eviction is tracked from the same boundary: a second signal from the case router carries the possession result, the step records it against the same row and closes or re-opens the eviction, and the return of the asset to hold under R-DIS-14 is the disposal-route story's, not this step's (FSD S5 A2.10).
9. No event is published: the outbox holds nothing for this step, because Architecture v5 slide 19 OUT gives rwb-asset only `AssetTakenOn` and `AssetSold` (§12.3).
10. A repeated occupancy signal, or the same `Idempotency-Key` twice, writes once, answers once and counts the repeat.
11. SCR-21 Asset list and SCR-22 Asset record read the asset, its holding status and its eviction state from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no eviction change and no case-move answer leaves the service | MSG-P7-003 | AC3, TC-E4-021-03, TC-E4-021-05 |
| X2 | The role does not hold the Asset and disposal right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E4-021-04 |
| X3 | The occupancy status is not `occupied`, or the case is not in `ASSET_HELD` | The rule does not fire: nothing is written and the step reports the state to the parent | None | AC2 |
| X4 | The occupancy fact arrives without an occupancy status or without the case reference | The step holds, writes nothing and the caller is told which field is absent | MSG-GEN-001 | AC2 |
| X5 | The rwb-case answer or the package load does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X6 | The officer withdraws the refusal, or possession is recorded before an instruction exists | Nothing is raised: no R-DIS-13 record and no `EVICTION_REQUIRED` move | None | AC2, AC3 |
| X7 | The same occupancy signal arrives twice for the same case and asset | One change, one answer, no second decision record; the repeat is counted | None | AC1, AC3 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC4, TC-E4-021-08, Section 17, BR3, BR6 |

X1 to X3 are the exception paths of RWB-E4-021 carried onto the split, X4 to X7 are the paths the target boundary and the signal add, and X8 is the DP-05 and DP-01 boundary. The occupancy value, the instruction period and the statuses are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E4021-CON, the rwb-case stage-signal and case-move fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or S4 |
| Negotiable | The activity name, the eviction status names and the shape of the stage outcome are this story's choice; the rule, the messages, the screens, the two reads and the state the case moves to are fixed |
| Valuable | The eviction is opened and tracked on the day the occupancy refusal is recorded, and the file reaches Legal with its decision on record |
| Estimable | One workflow branch, one evaluator, one record write, one row change, one case-move answer, two clients and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and occupancy facts through the contract fakes, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Evict occupants from a held property

  Background:
    Given case "RC-2026-000521" carries the held property "AST-2026-000521" in state "ASSET_HELD"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-13
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Evict occupants from a held property (legacy RWB-E4-021 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-000521" in state "ASSET_HELD"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens and tracks the eviction, which needs Legal and has no legal owner today
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DIS-13 (legacy RWB-E4-021 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-000522" in state "ASSET_HELD"
    Given a case in state ASSET_HELD
    When occupants refuse possession
    Then raise the eviction instruction to Legal
    Then the case moves to EVICTION_REQUIRED

  Scenario: AC3 Not recorded (legacy RWB-E4-021 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 A statement that reaches a v_ace view or another service's schema is refused (new, D-RCV-60)
    Given a component or a test issues a statement against a v_ace view or a recovery_case row
    When the statement reaches the database
    Then the grant refuses the statement and the boundary test fails the build

  Scenario: AC5 Each business rule BR1 to BR11 of section 8 holds in its own test (new, D-RCV-60)
    Given the rules BR1 to BR11 of section 8 are the rules this story must hold
    When the component, contract and boundary tests of section 16 run
    Then each rule holds in its test and a rule without a passing test fails the build

  Scenario: AC6 A provided operation answers 401, 403 or 404 when the call is refused or not found (new, D-RCV-60)
    Given a caller sends a request to a provided operation of section 12
    When the caller is not authenticated, lacks the Asset and disposal right, or names an asset or case that does not exist
    Then the operation answers 401, 403 or 404 respectively with the platform error envelope

  Scenario: AC7 A retried or timed-out activity waits and retries on the workflow's own schedule (new, D-RCV-60)
    Given the rwb-case answer or the package load does not answer inside 2 s
    When the activity runs
    Then the step waits and retries on the workflow's own schedule and nothing is written

  Scenario: AC8 A consumed call that fails or does not answer writes nothing and answers 503 (new, D-RCV-60)
    Given a consumed call fails, does not answer, or its breaker is open
    When the step runs
    Then nothing is written, no case move is answered and the caller sees 503 with the platform error envelope

  Scenario: AC9 A move the rule row does not allow is refused (new, D-RCV-60)
    Given a case not in state ASSET_HELD
    When the occupancy refusal reaches the step
    Then the move is refused, nothing is written and the state is reported to the parent
```

The three criteria are the legacy criteria of RWB-E4-021 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `the action is taken` and `the decision log cannot be written` all stand. AC1 and AC2 each carry one added `Given the rwb-case contract mock returns <x>` line because the case of record and the case move are rwb-case's, and that line is the only addition to the legacy text. What the legacy lines describe happens in three places in the target: rwb-case records the occupancy refusal and applies the move to `EVICTION_REQUIRED`; this story evaluates R-DIS-13, writes the eviction status, records the decision and answers the move with the instruction to Legal; and rwb-litigation acts on the instruction. One note is recorded rather than smoothed over: AC2 says the instruction is raised to Legal, and Legal's work is S4's, so this story raises the instruction on its answer and the case carries it to rwb-litigation, while the eviction record kept here is the status and the reference of the instruction (GAP-2889; ASM-4786).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-13 | Asset disposal | D8.1 to D8.3 | ASSET_HELD | OCCUPANTS_REFUSE_POSSESSION | occupancy_status = occupied | Raise the eviction instruction to Legal | EVICTION_REQUIRED | Litigation officer | LIT, Partner Portal | None |

The row is the row of the Business Rules and Routing Logic v4, copied character for character; it is rule BR12 in the table below. Its owner column is a role of the business and not a service: the case move to `EVICTION_REQUIRED` is written by rwb-case on this story's answer, the eviction record is written here, and the instruction is acted on by rwb-litigation. R-DIS-14, the return to hold when possession is taken, is listed in FSD S5 A2.10 and belongs to the disposal-route story of this service; it is carried in §9 as a state note only. The legacy screen list names no eviction state for SCR-22, so the eviction state of the asset on SCR-22 is shown in §9 and its name and presentation are Not specified in the source documents (GAP-2891; ASM-4788).

| ID | Rule | Source |
|---|---|---|
| BR1 | The eviction record is this service's: the status of the eviction and its instruction reference are held in `rwb_asset` against the `asset` row, and no other service writes them | Architecture v5 slide 13 (rwb-asset owns the asset disposal stage); TSD S5 T3.1; GAP-2888 |
| BR2 | The decision is recorded before the eviction row changes, one record per rule outcome, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; legacy RWB-E4-021 AC1 and AC3 |
| BR3 | The case move is answered and not written: `recovery_case`, `assignment`, `task` and `timer` and the states `ASSET_HELD` and `EVICTION_REQUIRED` are rwb-case's, and this story sends the move with the rule and its version | Architecture v5 slide 13; GAP-2889 |
| BR4 | The legal act is rwb-litigation's: this story raises the instruction and tracks it, and performs no enforcement step, holds no legal deadline and owns no partner instruction | FSD S5 A2.8 (integration points LIT); GAP-2889; ASM-4786 |
| BR5 | The occupancy fact is an input of the step and not a column of this service: where no source names a column for it, the value is held as Not specified in the source documents and is never invented as a column of `asset` | TSD S5 T3.1; GAP-2888; ASM-4785 |
| BR6 | The ACE NPA asset facts stay with rwb-source-data: this story reads no `v_ace_*` view and no ACE table, and takes the facts on the owner's contract only | DP-05; Architecture v5 slides 29 and 37 |
| BR7 | No event is published by this step: `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` only | Architecture v5 slide 19 OUT; GAP-2889 |
| BR8 | The same occupancy fact twice, or the same `Idempotency-Key` twice, writes once, answers once and counts the repeat | TSD S5 T-A.2; Architecture v5 slide 11 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` is an identifier of another service's fact | DP-01; TSD S5 T3.3 |
| BR10 | Every value a business person may change is reference data or a rule row read with its version: the occupancy statuses, the eviction statuses and the instruction period | TSD S5 T3.2; FSD S5 A2.8; legacy Guardrails |
| BR11 | No person name, address, contact value or identity number enters `rwb_asset`, the decision record, a log or a workflow input, and no occupant is identified as a person anywhere | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |
| BR12 | The rule R-DIS-13 of section 8 is evaluated with the DISPOSAL package version in force, and its outcome is the one its rule row gives | Business Rules and Routing Logic v4 (R-DIS-13 row in section 8) |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story does own is the eviction status of the asset and the state of the step.

| From (case route) | Event | Condition | To |
|---|---|---|---|
| ASSET_HELD | `OCCUPANTS_REFUSE_POSSESSION` under R-DIS-13 | `occupancy_status = occupied` | EVICTION_REQUIRED, with the case-move answer and the instruction reference |
| ASSET_HELD | `OCCUPANTS_REFUSE_POSSESSION` under R-DIS-13 | The occupancy status is vacant or absent | Unchanged, nothing written (X3, X4) |
| EVICTION_REQUIRED | `POSSESSION_TAKEN` under R-DIS-14 | The possession result is recorded | The return to hold is the disposal-route story's move; this step only closes the eviction record |
| Any | The same occupancy fact again | X7 | Unchanged, the repeat is counted |
| Any | A state the rule does not expect | X3 | Unchanged, no record and no answer |

| Eviction record | Event | Condition | To |
|---|---|---|---|
| None | R-DIS-13 fires and the record write commits | The decision record is written | Open, with the instruction reference |
| Open | The case answers the instruction accepted | The reference is returned | Instructed |
| Instructed | The possession result arrives | The status is recorded | Possession taken |
| Instructed | The officer withdraws the refusal | X6 | Closed without an instruction, nothing answered to the case |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | An occupancy fact for a case in `ASSET_HELD` | The package in force is loaded | Evaluating |
| Evaluating | R-DIS-13 fires | The decision record is written | Applying |
| Applying | The eviction row and the idempotency row are written and the case-move answer is sent | The transaction commits | Waiting for the possession result |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The case answer does not arrive inside 2 s | X5 | Waiting, retried on the workflow's schedule |

The case states are those of the DISPOSAL machine of TSD S5 T4 and of the legacy criteria. The eviction statuses are reference data; where the TSD S5 T3.2 gives no list for them, the values are read as configuration and the absence is recorded (GAP-2888; ASM-4785).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SALEOFF, sale officer | Asset and disposal CRUA in TSD S5 T6.1 and R in the legacy permission table; the acting role of the feature: records the refusal, opens and tracks the eviction |
| RW-LEGAL, legal counsel | Asset and disposal R: reads the eviction and its instruction; the FSD names legal counsel as an also-user of the feature |
| RW-LITOFF, RW-ENFORCE | Asset and disposal R and CRU: read the eviction and act on the instruction in rwb-litigation, not here |
| RW-NPAMGR, RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal R or RA: read the held asset, its occupancy and its eviction in scope |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-CONDUCT, RW-HEADLIT, RW-RISK, RW-COE, RW-FINANCE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Asset and disposal R: read only, in scope |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal R or RU as the matrix gives it: read the asset and its eviction state, never open or close an eviction |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-asset service identity | Runs the step, evaluates the rule, writes the decision record and the eviction status, answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S5 T6.1 and of the legacy permission table of this key, and nothing wider. The step runs under the service identity with no officer task on the happy path, and the sale officer is the primary role when a person does act, on SCR-22 and on the refusal and withdrawal paths. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here. The rwb-access authorise check of each operation: Not specified in the source documents (DOR-RWB-S5-E4021-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-028 to DF-COL-042 | asset (S5, `rwb_asset`) | The asset reference, its type, its transfer-in type, its book value, its holding status and its holding cost to date | Read, and write the holding status where the eviction changes it |
| Not specified in the source documents (GAP-2888; ASM-4785) | asset (S5, `rwb_asset`) | The occupancy status, the eviction status and the instruction reference | Write and read as configuration, held against the `asset` row until the S5 data owner names the columns (GAP-2888) |
| Standard columns | asset (S5, `rwb_asset`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the eviction row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table: the case reference and the case state arrive on the stage signal and the answer goes back on the case-move boundary |
| DF-WRK-009 to DF-WRK-016 | assignment (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not read and not written: the officer task is rwb-case's |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (owner not S5) | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | Not read and not written: the instruction to Legal is raised on the case answer and no partner instruction is owned here (GAP-2889) |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Not read: this service holds no `v_ace_*` grant; the facts arrive on the rwb-source-data contract and are held on `asset` (BR6) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read and not written: the rule rows are governed in rwb-decision and loaded with the package |

Field IDs are those of the TSD S5 Assets and auction v2 T3.1 and the Logical Data Model and Data Dictionary v9, and the ACE, case, assignment, partner, decision and rule rows are the rows the legacy story lists in its Data table, with their owners changed by the target. **No new table, no new column and no migration**: `asset` arrives with the DB story of this service, and `decision_record`, `inbox_event` and `idempotency_key` are platform library objects created in `rwb_asset` by the library's own migration (DP-03, DP-09). The eviction record has no table of its own in any source: it is held against the `asset` row where a column exists, and otherwise the value and its store are Not specified in the source documents (GAP-2888; ASM-4785).

**No personal data.** The rows this story writes carry identifiers, codes, statuses, a reference and a rule version. No name, address, contact value or identity number of an occupant or of a borrower enters `rwb_asset`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes are declared by RWB-S5-E4021-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, its holding status, its occupancy and its eviction status (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The step itself adds no REST operation: the sources name none for the eviction step, whose surface is the stage signal and the case-move answer (GAP-2889; ASM-4786). The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 for an invalid filter, and 503 when the decision library or a consumed contract does not answer. The other ownership rows of this service — `GET /assets/{assetKey}`, `POST /assets/{assetId}/listings`, `POST /assets/{assetKey}/listings` and `POST /listings/{listingId}/rounds` — are the pricing and auction stories'; none is supplied here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case-move answer (operation name Not specified in the source documents (GAP-2889; ASM-4786)) | rwb-case (P3) | P3 rwb-case | The answer that carries `EVICTION_REQUIRED`, the instruction reference and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state the step checks before a rule fires; read only; faked |

The stage signal is not a REST row: the occupancy fact and the possession result arrive as signals the parent forwards to the running child, which is the workflow boundary of Architecture v5 slide 13. Every REST row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2889 with ASM-4786.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` and `AssetSold`. This step publishes neither: the take-on story publishes the first and the sale story the second, and the eviction raises no event of its own. A build that publishes an event here fails the absence test.

#### 12.4 Events consumed

None. The occupancy refusal and the possession result reach the step as stage signals through the case router of rwb-case, which is how every event of another service reaches a stage (Architecture v5 slide 13); this step subscribes to no topic of its own. No source names an eviction or possession event for this service, and none is declared here (GAP-2889; ASM-4786). The litigation and auction feeds this service does listen to belong to the auction and litigation-result stories.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, continues-as-new across the years of the holding | `rwb-asset` | Input: the case, the route, the asset reference and the rule package in force; signals: the occupancy fact, the possession result and the rule package in force |
| `openEviction` | Activity, the one eviction step of this story | `rwb-asset` | The case, the asset and the occupancy fact in; the rule ID with its package version, the eviction status, the instruction reference and the case move out, with the decision record and the row written in one transaction |

No child workflow for the case and no workflow for the legal act exists in this service. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the arrival of the occupancy fact for a case in `ASSET_HELD`, because the legacy story says the eviction is opened when the occupants refuse possession. Workflow ID form, start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-9952; DOR-RWB-S5-E4021-APP-8). Activity `openEviction` is not in Temporal Catalog v1; it stays a story-local name until that catalog entry is added. The signal and case-move element names are Not specified in the source documents (GAP-2889; ASM-4786) until rwb-case publishes them; only the adapter changes then. How the eviction instruction reaches rwb-litigation: Not specified in the source documents (GAP-2889).

#### 12.6 Schedules

None. The step runs from the stage signal the parent forwards and owns no Temporal Schedule and no legacy Quartz job. The single Schedule of this service is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP (Architecture v5 slide 44). No other Job of slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The held asset; this story writes its holding status and the eviction state and reference where a column exists |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record, one per rule outcome (DP-03) |
| inbox_event | PLT library, created in `rwb_asset` | The row of the forwarded fact and its dedupe key (DP-09) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated fact and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `partner_instruction` (not S5's; see GAP-2889), `template` (P6), `deviation` (S8), `document` and `document_custody` (P5), `proceeds` (P8), every `v_ace_*` view (P1), and `listing` and `asset_sale`, which are this service's but the pricing and sale stories'. No foreign key leaves the schema and `asset.case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case stage-signal fake | The occupancy fact of case `RC-2026-000521` and asset `AST-2026-000521` with `occupancy_status = occupied`; the same fact twice; the possession result | AC1, AC2, X7 |
| rwb-case case-state fake | The case state `ASSET_HELD` of `RC-2026-000521`; a case in `EVICTION_REQUIRED` and a case in another state | AC2, AC3, X3 |
| rwb-case case-move fake | The move `EVICTION_REQUIRED` accepted with its instruction reference; a move refused because the case is not in the state the rule expects | AC1, AC2, X3 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-13 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000521`, with the asset and its eviction state read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the case-move answer and of the officer action that starts the signal are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2889; ASM-4786).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The two reads of the asset on `/api/recovery/asset/v1`; the rwb-case case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | Nothing published and nothing subscribed; the facts arrive as stage signals |
| Temporal | 1 workflow and 1 activity | `AssetDisposalWorkflow` and its eviction step on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `eviction`, Java package `th.co.scb.ace.workbench.recovery.asset.eviction`; front end `src/modules/recovery/asset/AssetEviction.tsx`, the fragment SCR-22 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the NPA asset facts the feature shows are the ones the rwb-source-data contract answers and the take-on story holds on `asset` (GAP-2888). DP-03 is the transaction rule of the step: the record, the `asset` row and the idempotency row commit together or not at all. DP-13 moves the base of the two reads and nothing else. DP-19 is how SCR-21 and SCR-22 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The two consumed rows (the rwb-case case state read and the case-move answer) are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2889. The stage signal is the workflow boundary of Architecture v5 slide 13 and adds no H row.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` eviction branch | Workflow | The step of the journey that waits for the occupancy fact, loads the package in force and reports the outcome to the parent |
| `openEviction` | Activity | The one step: read the asset and the fact, evaluate R-DIS-13, write the record and the row, answer the case move |
| `EvictionSignalHandler` | Workflow adapter | Takes the occupancy fact and the possession result the parent forwards, dedupes on the fact reference and signals the workflow |
| `EvictionEvaluator` | Service | The R-DIS-13 evaluation against the DISPOSAL package version in force |
| `AssetDecisionRecordWriter` | Library adapter | Writes one decision record per rule outcome before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `EvictionWriter` | Repository | Writes the holding status, the eviction status and the instruction reference against the `asset` row in one `rwb_asset` transaction, with the idempotency row and the optimistic lock |
| `CaseMoveAnswer` | Client | Answers rwb-case with `EVICTION_REQUIRED` and the instruction reference, one hop, 2 s |
| `CaseStateClient` | Client | The case state read of rwb-case, one hop, 2 s |
| `AssetController` | Controller | The two reads, the capability area and right, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 |
| `AssetEviction` | React component | Shows the occupancy, the eviction status and the instruction reference on SCR-22, read only, with the refusal and hold states; the empty, loading, error and no-access states of SCR-21 and SCR-22 are Not specified in the source documents (CG-ALL-9957; CG-ALL-9958) |

**Database and migrations.** No Flyway file. `asset` arrives with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). No column is added for the occupancy or the eviction: where the TSD S5 T3.1 names none, the value is Not specified in the source documents and is raised as GAP-2888 rather than invented.

**Configuration and reference data.**

- The occupancy statuses, the eviction statuses and the instruction period at their version in force, read as reference data and never as constants; where TSD S5 T3.2 names no list for them, the values are configuration and the absence is recorded (GAP-2888). The reference-data contract that DP-06 and DP-07 require, and the parameters the lists are read from, are Not specified in the source documents (DOR-RWB-S5-E4021-APP-20).
- The DISPOSAL package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the condition and the move of R-DIS-13 are values of the package and not of this build.
- The capability area "Asset and disposal" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The eviction branch of `AssetDisposalWorkflow` and its input record, registered on `rwb-asset`, with the occupancy fact as its trigger.
2. `EvictionSignalHandler` and the forwarded fact, with the duplicate and redelivery paths (AC1, X7).
3. `CaseStateClient` and `CaseMoveAnswer` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, AC2, X5).
4. `EvictionEvaluator` over the DISPOSAL package, with R-DIS-13, the vacant and absent occupancy paths and the unexpected-state path (AC2, X3, X4).
5. `AssetDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X1).
6. `EvictionWriter` with the one transaction, the status columns, the idempotency row and the optimistic lock (AC1, AC2, X7).
7. `CaseMoveAnswer` and the parent signal, with the move and its instruction reference (AC1, AC2).
8. `AssetController` with the rights, the pagination and the problem mapping of 400, 401, 403, 404, 422 and 503 (AC1).
9. `AssetEviction` and the two screens through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_asset`, no `v_ace_*` read, no write to any other service's schema, and no outbox row (X8, BR3, BR7).

**Feature flag.** `rwb.asset.eviction-v1`, read as a flag of the platform library; off means the handler holds the fact, writes nothing and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic occupancy fact in SIT, R-DIS-13 produces its record and its move, a vacant or absent occupancy raises nothing, a repeated fact writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-21 and SCR-22 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the occupancy fact is absent or invalid: the case reference, the asset reference or the occupancy status (X4) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the asset list or the asset, or attempts the step (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the eviction row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are values of the pricing story of this service, so no path of this story raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this story raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |

The five message IDs are those of the legacy message set of this key and of the platform set, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this story raises them.

### 15. Screens and states

SCR-21 Asset list in its loading and list states, with its empty, error and no access states Not specified in the source documents (CG-ALL-9957), and SCR-22 Asset record in its take-on, held, listed and sold states are served through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its eviction state, and rwb-case for the case and its route state; this story fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The state this story produces is the eviction state of the held asset on SCR-22: occupied, eviction instructed with its reference, and possession taken, next to the refusal, withdrawal and failure states it shows (refused with MSG-P4-002, not recorded with MSG-P7-003, absent field with MSG-GEN-001, held while rwb-case does not answer). The legacy screen list gives SCR-22 the four states take-on, held, listed and sold and names no eviction state, so the state name and its presentation are Not specified in the source documents (GAP-2891; ASM-4788) and are recorded rather than invented. The take-on, listed and sold states belong to the take-on, pricing and sale stories of this service and are read from the same route. The empty, loading, error and no access states of SCR-22 are Not specified in the source documents (CG-ALL-9958).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-021-01 | AC1 | Component | Case `RC-2026-000521` with an occupancy fact of `occupied`; the eviction row, the decision record and the case move asserted on the fakes |
| TC-E4-021-02 | AC2 | Component | Case `RC-2026-000522` at `ASSET_HELD` with `occupancy_status = occupied`; the R-DIS-13 record, the instruction reference and the `EVICTION_REQUIRED` move asserted |
| TC-E4-021-03 | AC3 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E4-021-04 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E4-021-05 | Principle 5 | Component | A forced decision log write failure at the moment of the eviction write; no row, no answer and no event |
| TC-E4-021-06 | Section 12 (operations, events and activities) | Contract | Each operation, event and activity of section 12 checked against its published contract with the contract fake; no operation outside the contract |
| TC-E4-021-07 | Section 12.7 tables (ASM-3438) | Component | Each table of section 12.7 read and written only by its owner; a statement on any other table fails the build |
| TC-E4-021-08 | AC4 | Component | A statement against a v_ace view or a recovery_case row from a component or a test; the grant refuses it and the boundary test fails the build |
| TC-E4-021-09 | AC5 | Component | Each rule BR1 to BR11 of section 8 checked on the fake or stub of its own owner; a rule without a passing test fails the build |
| TC-E4-021-10 | AC6 | Contract | Each provided operation of section 12 called unauthenticated, without the right and for an unknown identifier; 401, 403 and 404 returned with the platform error envelope |
| TC-E4-021-11 | AC7 | Component | The rwb-case answer or the package load held past 2 s; no write, no case move, retry on the workflow's own schedule |
| TC-E4-021-12 | AC8 | Component | A consumed call stub that fails or does not answer, and an open breaker; nothing written, no case move answered, 503 with the platform error envelope |
| TC-E4-021-13 | AC9 | Component | A case at a state other than ASSET_HELD with an occupancy refusal; move refused, nothing written, state reported to the parent |

The five legacy cases are the legacy cases of RWB-E4-021 in their legacy order, with the Level column added: the two `System`-style cases run as `Component` on their fakes, and no legacy case of this key crosses a live boundary, so no `-ITG` copy is created here; the cross-service copies belong to the wave 3 harness and end in `-ITG`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the occupancy statuses, the eviction statuses, the instruction period and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_asset`, in a workflow input or in a log: identifiers, codes, statuses and a rule version only, no occupant is identified, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case and the legal act with rwb-litigation: no `recovery_case`, `assignment`, `task` or `timer` row and no enforcement step is written here (BR3, BR4).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.
- The decision is recorded before the change and the forwarded fact is deduped; a build that publishes or that changes a row before its record fails the review (DP-03, DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S5-006 to REQ-S5-010 | The five requirements TSD S5 T8 maps to FEAT-AST-08, the eviction being one of them; the split plan carries no requirement row for this slice, so the trace rests on the module requirement (GAP-2890; ASM-4787) | The eviction step, the eviction record and the case move | TC-E4-021-01, TC-E4-021-02 | FEAT-AST-08 | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the eviction record | TC-E4-021-02 | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) |
| ADR-014 | Schema and login per service | `rwb_asset` and its own login | TC-E4-021-05 | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | No subscription and no publication; the inbox row of the forwarded fact | TC-E4-021-01 | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two consumed rows with their budget | TC-E4-021-01 | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change | TC-E4-021-03, TC-E4-021-05 | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) | Not specified in the source documents (DOR-RWB-S5-E4021-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-021, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by this story |
| Test cases | TC-E4-021-01 to TC-E4-021-05 |
| Feature and screens | FEAT-AST-08, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-13, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the two reads, the stage signal, the case-move answer, the decision-record element, the error set and the fakes: RWB-S5-E4021-CON.
- The case of record, its route states, `assignment`, `task`, `timer`, the parent `CaseWorkflow` and the routing of the instruction to rwb-litigation: rwb-case (P3) (GAP-2889).
- The eviction itself, its legal steps, its deadlines and its outcome: rwb-litigation (S4).
- The return of the asset to hold after possession is taken, R-DIS-14: the disposal-route story of this service (FSD S5 A2.10).
- The holding costs, insurance, custody and work orders of the property: the held-property story of this service (FEAT-AST-07).
- The ACE NPA asset facts and the freshness of the data product: rwb-source-data (P1).
- The rule rows, the package version and its approval: rwb-decision (P7).
- The partner-instruction surface and any external legal instruction file: not S5's and not named by a source read here (GAP-2889).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-22: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

# RWB-S5-E3023-APP Track holding age against the provision steps

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3023-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-023 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S5-E3023-APP-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S5-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S5-E3023-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version fixed | v1 (the `/v1` paths in section 12.2) |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| Workflow start rule | AssetDisposalWorkflow is started by rwb-case when a repossession completes, a deed in lieu transfer is registered, or the bank takes the property at the enforcement auction (PRD S5 rwb-asset v1). Workflow ID form: Not specified in the source documents (CG-ALL-9735) |
| Personal-data classes of carried fields | The eight asset catalog fields (asset_key, asset_ref, asset_code, asset_type, transfer_in_type, from_segment, transfer_in_date and the collateral key) are not personal data (PRD S5 rwb-asset v1, FSD marking). Bidder and party fields are personal data; this story carries none of them. |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Requirement | REQ-S5-003, Holding age drives re-appraisal and the provision step by rule (Business Requirements Program v5, Must, Epic E3) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-023 split out for rwb-asset. The three legacy criteria are kept word for word with their origin tag; the clocks become durable timers of `AssetDisposalWorkflow` on queue `rwb-asset`, the outcome is recorded through the local decision-record library before anything changes (DP-03), the ACE asset fact arrives on the rwb-source-data contract instead of a `v_ace_*` read (DP-05), the base becomes `/api/recovery/asset/v1` (DP-13) and SCR-21 and SCR-22 read through the gateway-bff composite route (DP-19). The thresholds, the step percentages and the cost-of-carry rate are rule and reference values of rwb-decision and are in no source available to this file (GAP-2855; ASM-4726). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3023-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 23 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **nPA and asset manager**, I want **the Workbench to count the days held and apply the provision step the policy sets at each threshold**, so that **assets sell sooner at approved prices**.

This is the application slice of legacy RWB-E3-023. It owns the three legacy criteria; R-DIS-06 on the confirmed record and R-DIS-09 at the next provision step date, with the DISPOSAL package in force; the two clocks as durable timers of `AssetDisposalWorkflow`; the monthly cost-of-carry request on queue `rwb-payment`; the record of every step; the `ASSET_HELD` move answer; and the holding facts the two screens read (Architecture v5 slide 19; Temporal and Drools Design slide 13).

It does not own the shapes of RWB-S5-E3023-CON; the take-on and the `asset` row (RWB-S5-E3019-APP, -E3020-APP, -E3021-APP); the case, its route states, the parent `CaseWorkflow` and the `timer` row (rwb-case, P3); the ACE asset fact (rwb-source-data, P1); the posting and the ledger (rwb-payment, P8); the thresholds, the percentages and the rate (rwb-decision, P7); or the deployment (the operations story of this key).

### 2. Business rationale

The program keeps the requirement as **REQ-S5-003, "Holding age drives re-appraisal and the provision step by rule"** (Business Requirements Program v5, Must, Epic E3), and the feature extract keeps FEAT-AST-05 with the same scope: it counts the days held, applies the provision step at each threshold, runs unattended, touches AMIS, ALS and GL, and depends on FEAT-AST-01 (Epics 3 to 8 Specification v3).

What D-RCV-60 changes is who owns the asset, the case, the money and the policy. In the monolith the clock, the step, the charge and the log row were one process in one `recovery` schema. In the target the holding facts are this service's (slide 41 gives rwb-asset "assets taken on, holding, floor price, listings, auction rounds"), the case and the `timer` row are P3's, the money is P8's (the S5 row of slide 13 gives P8 a Temporal call, never a posting here), and the policy is versioned rule and reference data read with its version, never written in code.

The case move is not carried by a consumed event: slide 19 IN gives `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, none of them a case state, so the state is taken on the rwb-case contract one hop with a 2 s budget. The feature's measure, the NPA sales cycle read on the decision log, does not move.

### 3. Preconditions

- RWB-S5-E3023-CON is published: the two reads, the holding and provision elements, the provision input, the move answer shape, the error set and the fakes are baselined.
- The rwb-source-data data-product contract of DP06 Collateral and assets and the rwb-case state read and move answer are published with their fakes; the operation names are Not specified in the source documents (GAP-2856; ASM-4730).
- The rwb-payment cost-of-carry activity is published on queue `rwb-payment` with its fake, because the S5 row of slide 13 gives P8 a Temporal call and the charge is P8's; its name is Not specified in the source documents (GAP-2856; ASM-4729).
- RWB-PLT-E1027-CON is published with its writer fake: the record is written in the caller's transaction and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the two screens reach this service through the gateway-bff composite route (DP-19).
- `asset` exists in `rwb_asset` from the DB story with the columns of DF-COL-031 to DF-COL-040 and the standard record columns; this story adds no table, no column and no migration (GAP-2855; ASM-4726).
- The DISPOSAL package is in force at its version with R-DIS-06 and R-DIS-09, governed in rwb-decision (P7); the thresholds, the percentages and the rate are its values and appear in no source available to this file (GAP-2855; ASM-4727).
- The service runs as its own login on `rwb_asset` with no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_npa_asset` or `rwb_case` fails the boundary test (DP-05; ASM-4731).
- The Finance provision feed is reachable through the route its owner publishes; the transport and the element name are Not specified in the source documents (GAP-2856; ASM-4729).
- The missing approval of the sources is recorded rather than waited on (GAP-2858; ASM-4734).

### 4. Flow

1. The take-on step confirms the asset record: the `asset` row exists in `HELD` with its stock date, book value and asset facts; no ACE data is read as a table here (RWB-S5-E3019-APP; DP-05).
2. The holding branch of `AssetDisposalWorkflow` receives the confirmation for a case in `ASSET_ON_BOOKS` and reads the case state, the case reference and the title status on the rwb-case contract, read only (ASM-4730).
3. `HoldingAgeEvaluator` loads the package in force and evaluates R-DIS-06 on the asset fact and title_status in (clear, under_transfer).
4. The evaluation answers the rule ID, the package version, the holding start date, the next provision step date and the case move; where no rule fires the step changes nothing and reports the reason.
5. `HoldingDecisionRecordWriter` writes one record through the library **before any change**: case, asset, rule ID with its version, inputs reference, holding start date and move; a failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
6. `HoldingClockArmer` arms the holding age clock from the holding start date and the provision step clock to the next provision step date, both as durable timers that survive a restart, a redeploy and a Continue-As-New (ASM-4726).
7. `CostOfCarryRequester` asks rwb-payment for the monthly charge on queue `rwb-payment` with the case, asset, month, book value and rule version, and writes the cost to date where the DB story publishes a column (ASM-4729).
8. `HoldingWriter` updates `asset` in one `rwb_asset` transaction with the record, the idempotency row and the fields the dictionary gives (DF-COL-031 to DF-COL-040), leaving what the model does not give empty rather than inventing it (GAP-2855).
9. `CaseMoveAnswer` answers rwb-case with `ASSET_HELD`, the rule ID, the version and the decided-at time; rwb-case writes the `recovery_case` row and its route state (ASM-4730).
10. The provision step clock fires when the age reaches the next step date: `ProvisionStepEvaluator` evaluates R-DIS-09, records the outcome before any change, applies the step and hands the input to the Finance provision feed (GAP-2856; ASM-4729).
11. The step rearms the clock for the next threshold and repeats while the case is in `ASSET_HELD`; a deviation pause holds it until the case resumes (ASM-4732).
12. A repeated confirmation with the same case, asset and holding start date writes nothing, arms no clock, answers nothing and counts the repeat.
13. SCR-21 and SCR-22 read the asset, its age, its cost to date and its next step date through the composite route, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no asset change, no clock armed, no cost-of-carry request, no provision input, no answer | MSG-P7-003 | AC3, TC-E3-023-03, TC-E3-023-05 |
| X2 | The role does not hold the Asset and disposal right | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | AC4, TC-E3-023-04, TC-E3-023-10 |
| X3 | The case is not in `ASSET_ON_BOOKS` on the confirmation, or not in `ASSET_HELD` when the clock fires | 409 and nothing is written; the step is not re-evaluated on a case that has moved | None | AC2 |
| X4 | The title status is neither clear nor under transfer | No rule fires under R-DIS-06: nothing changes, no clock starts | None | AC2 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow schedule; nothing is written and no move is answered, and the caller sees 503 | None | AC1 |
| X6 | The Finance provision feed refuses the provision input | The step records the refusal, keeps the asset unchanged, retries, and raises a task after the retry limit; no threshold is skipped | None | AC1 |
| X7 | The same confirmation or the same threshold arrives twice | One record, one asset change and one answer; the repeat is counted | None | AC1 |
| X8 | A component or a test reaches a `v_ace_*` view, a `recovery_case` row, a `timer` row or another schema | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | AC5, TC-E3-023-11, Section 17, BR4, BR6 |

X1 to X4 are the legacy exception paths carried onto the split, X5 to X7 are the paths the target call types and the two clocks add, and X8 is the DP-01, DP-05 and DP-10 boundary. No threshold and no rate is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S5-E3023-CON, the three owner fakes and the record stub, on its own schema, with no live P1, P3, P7 or P8 |
| Negotiable | The activity names, the decision code per rule and the stage outcome are this story's choice; the rules, messages, screens, reads and timers are fixed |
| Valuable | A held asset carries one holding age and one provision step at a time, recorded with its rule version, and the step reaches Finance without a person |
| Estimable | One workflow branch, two evaluators, one record write, one row update, one cost-of-carry request, one provision input, one move answer, two read fragments |
| Small | Two weeks with its tests on the fakes; the timer rearm loop is the only state it adds |
| Testable | Each criterion runs on synthetic cases and asset facts through the fakes with a shortened interval, plus the access and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Track holding age against the provision steps

  Background:
    Given case "RC-2026-000511" holds asset "AST-2026-000511"
    Given the DISPOSAL rule package is in force at its version and carries R-DIS-06 and R-DIS-09
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Track holding age against the provision steps (legacy RWB-E3-023 AC1)
    Given the rwb-source-data contract mock returns the asset facts of asset "AST-2026-000511" with the stock date and the book value
    Given the rwb-payment contract mock returns the monthly cost of carry recorded for "RC-2026-000511"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then counts the days held and applies the provision step the policy sets at each threshold
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Rule R-DIS-06 (legacy RWB-E3-023 AC2)
    Given the rwb-case contract mock returns the case state "ASSET_ON_BOOKS" for "RC-2026-000511"
    Given the rwb-case contract mock returns the title status "clear" for "RC-2026-000511"
    Given the rwb-payment contract mock returns the monthly cost of carry recorded for "RC-2026-000511"
    Given a case in state ASSET_ON_BOOKS
    When asset record confirmed
    Then start the holding age clock and the provision step clock, and charge cost of carry monthly
    Then the case moves to ASSET_HELD

  Scenario: AC3 Not recorded (legacy RWB-E3-023 AC3)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC4 Access refused (exception X2) (new, D-RCV-60)
    Given the role does not hold the Asset and disposal right
    When the action is taken
    Then the request is refused with 403 and the user sees MSG-P4-002, and nothing changes and no record is written

  Scenario: AC5 Boundary refused (exception X8) (new, D-RCV-60)
    Given a component or a test reaches a v_ace_* view, a recovery_case row, a timer row or another schema
    When the boundary test runs
    Then the grant refuses the statement and the build fails

  Scenario: AC6 Business rules BR1 to BR11 hold (new, D-RCV-60)
    Given the rwb-source-data contract mock returns the asset facts of an asset with the stock date and the book value (test data: Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC6))
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for a case
    When the rules of section 8 are applied to the asset and the case
    Then the holding age and the provision step are computed here from the dates and the package, and the thresholds are read as rule rows with their version
    Then a deviation pause holds the step and the age is still counted from dates, and no cross-schema join, no foreign key and no person name, address, contact value or identity number enters the asset, the record, a log, a workflow input or a provision input

  Scenario: AC7 Error answers of the provided operations (new, D-RCV-60)
    Given a request to a provided operation carries no valid credential
    Given a request to a provided operation names a case or an asset that does not exist
    When the request is made
    Then the answer is 401 for no valid credential, 403 for a role without the Asset and disposal right and 404 for an unknown case or asset, and nothing changes

  Scenario: AC8 Activity retried or timed out (new, D-RCV-60)
    Given an activity of AssetDisposalWorkflow fails or does not answer within its timeout
    When the activity is retried
    Then the retry runs under the workflow's retry policy, and when the retries are spent nothing changes and no record is written

  Scenario: AC9 Consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-payment contract mock fails or does not answer for a case
    When the charge is requested
    Then the call is not taken as answered, the asset does not change and no record is written

  Scenario: AC10 Disallowed status change refused (new, D-RCV-60)
    Given the rwb-case contract mock returns the case state "ASSET_HELD" for a case
    When a status change the model does not allow is requested
    Then the change is refused and nothing changes
```

The three criteria are the legacy criteria of RWB-E3-023 word for word, with their origin tag added and only the decision-log wording changed to decision record: the repetition of `Then` and the legacy wording of `the action is taken` and `its trigger arrives` all stand. The cross-service parts are mocked, so the `Given the <service> contract mock returns <x>` lines are the only additions. What they describe happens in four places: rwb-source-data answers the asset fact, rwb-case answers the state, the title status and the move, rwb-payment records the monthly charge, and this story counts the age, applies the step, records the decision, updates the asset and answers the move. AC1 names the provision step of R-DIS-09 and AC2 names R-DIS-06; this story owns both. AC2 is also a legacy criterion of RWB-E3-019, whose story owns its copy for the take-on while this one owns the clocks, and only RWB-S5-E3023-APP runs the R-DIS-06 clocks, so neither runs a second clock (GAP-2855; ASM-4726; GAP-2837).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DIS-06 (BR1, BR2, BR3, BR5, BR7, BR8) | Asset disposal | D8.1 to D8.3 | ASSET_ON_BOOKS | ASSET_RECORD_CONFIRMED | title_status in (clear, under_transfer) | Start the holding age clock and the provision step clock, and charge cost of carry monthly | ASSET_HELD | Sale officer | Workbench, Finance provision feed | None |
| R-DIS-09 (BR1, BR2, BR5, BR11) | Asset disposal | D8.1 to D8.3 | ASSET_HELD | PROVISION_STEP_DUE | holding_age reaches next_provision_step_date | Apply the provision step and send the input to Finance | ASSET_HELD | Workbench | Finance provision feed, ALS core and GL | None |

Both rows are the rows of the Business Rules and Routing Logic v4, copied character for character. The owner column is a business role, not a service: rwb-case writes the case move on this story's answer, the asset and its holding facts are written here, and the posting and the feed are P8's and the feed owner's.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The holding age and the provision step are this service's facts, derived from the asset dates and the package; no other service computes them | Architecture v5 slide 41; FEAT-AST-05; REQ-S5-003 | AC1, AC6, TC-E3-023-01 |
| BR2 | The decision is recorded before the asset changes, with the rule ID and the version in force; a failed write changes nothing and shows MSG-P7-003 | DP-03; legacy AC1 and AC3 | AC1, AC3, AC6, TC-E3-023-03, TC-E3-023-05 |
| BR3 | The clocks are durable timers of the workflow: no Quartz job, no job table, no Schedule, and a redeploy or Continue-As-New neither loses nor restarts a clock | DP-10 as a prohibition; ASM-4726 | AC2, AC6, TC-E3-023-02 |
| BR4 | The `timer` row is P3's: the clocks live in the workflow, are projected on the screens and write no `timer` row | Ownership Map; ASM-4728 | AC5, AC6, TC-E3-023-07 |
| BR5 | The thresholds, the percentages and the rate are rule rows and reference data read with their version, never a constant, a default or a branch | FEAT-AST-05; BR2; GAP-2855 | AC1, AC6, TC-E3-023-01 |
| BR6 | The ACE asset fact stays with rwb-source-data: no `v_ace_*` view and no ACE table is read here | DP-05; ASM-4731 | AC5, AC6, TC-E3-023-07 |
| BR7 | The case move is answered and not written; `recovery_case` and the route states are rwb-case's | Ownership Map; ASM-4730 | AC2, AC6, TC-E3-023-02 |
| BR8 | The money is rwb-payment's: the charge and the ledger effect are requested on its queue and no posting, balance or ledger row is written here | Architecture v5 slide 13; ASM-4729 | AC2, AC6, TC-E3-023-02 |
| BR9 | No cross-schema join and no foreign key leaves `rwb_asset`; `case_id` and the collateral identifier are other services' identifiers | DP-01 | AC5, AC6, TC-E3-023-07 |
| BR10 | A deviation pause of R-DIS-66 holds the step until R-DIS-68 resumes the asset, and the age computed from dates neither stops nor resets | R-DIS-66 and R-DIS-68; ASM-4732 | AC6, TC-E3-023-08 |
| BR11 | No person name, address, contact value or identity number enters the asset, the record, a log, a workflow input or a provision input | Template and Rules v1 §R7.2 (s17) | AC6, TC-E3-023-08 |

### 9. State transitions

The case route state is rwb-case's: the step answers the move and the parent applies it (BR7). What this story owns is the clock and step state of the asset.

| From (`asset.holding_status`) | Event | Condition | To |
|---|---|---|---|
| HELD, no clock | The confirmation under R-DIS-06 | title_status in (clear, under_transfer) | HELD unchanged, both clocks armed, answer `ASSET_HELD` |
| HELD, clock armed | The clock fires under R-DIS-09 | holding_age reaches next_provision_step_date | HELD unchanged, step applied, record written, clock rearmed |
| HELD, clock armed | The case pauses on a deviation | R-DIS-66 | HELD unchanged, step holds, clock state kept (BR10) |
| HELD, step held | The deviation clears | R-DIS-68 | HELD unchanged, step resumes where it paused |
| HELD, clock armed | A second confirmation or the same threshold | X7 | Unchanged, the repeat is counted |
| LISTED, UNDER_OFFER, RENTED, SOLD, TRANSFERRED | The clock fires late | The asset has left the hold | No step applied; the firing is recorded and dropped |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The confirmation arrives for a case in `ASSET_ON_BOOKS` | The package is loaded | Evaluating |
| Evaluating | R-DIS-06 fires | The record is written | Arming |
| Arming | The clocks are armed, the charge is answered and the asset is updated | The transaction commits | Waiting for the provision clock, answer sent |
| Waiting | The clock fires for a case in `ASSET_HELD` | R-DIS-09 fires and the input is accepted | Waiting, rearmed |
| Arming or Waiting | The record write, the transaction or the feed fails | X1, X6 | Waiting, nothing changed, retry scheduled |
| Waiting | The case is in `DISPOSAL_PAUSED_DEVIATION` | R-DIS-66 | Waiting, held |

No new holding-status value is introduced: the story writes no holding status of its own (GAP-2855).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-NPAMGR, NPA and asset manager | The primary role: reads the holding age, the cost to date and the provision step |
| RW-CASEOWN, RW-TEAMMGR, RW-FIELDCOL, RW-COMPLAIN, RW-LITOFF, RW-ENFORCE, RW-LEGAL, RW-SALEOFF and the roles the access matrix adds | Asset and disposal R: read only, in scope |
| RW-PRODHEAD, RW-HEADNPA, RW-HEADASL | Asset and disposal R, and the approval path where a step needs it |
| PT-AUCTION, PT-RAMC, PT-VALUER | Asset and disposal R only, through the partner gateway; never the provision step |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Asset and disposal R, C or U as the matrix gives: the service identities run the step under the same checks |
| rwb-asset service identity | Runs the step, evaluates the rules, writes the record and the asset, requests the charge, sends the input and answers the move; no grant outside `rwb_asset` |

The legacy permission table gives the Asset and disposal area the right R and no C right, and that is the whole authority of the story: the feature runs unattended with the NPA and asset manager as the reader. DP-08 is not in this pattern set, so the check is stated here and not built here: each read and write is preceded by the rwb-access authorise check on the Asset and disposal capability area at right R, and the contract of that check is Not specified in the source documents (DOR-RWB-S5-E3023-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-COL-031 | asset (S5, `rwb_asset`) | asset_ref | Read, the reference of the asset and the answer |
| DF-COL-032 | asset (S5, `rwb_asset`) | asset_code | Read |
| DF-COL-033 | asset (S5, `rwb_asset`) | asset_type | Read |
| DF-COL-034 | asset (S5, `rwb_asset`) | transfer_in_type | Read |
| DF-COL-035 | asset (S5, `rwb_asset`) | from_segment | Read |
| DF-COL-036 | asset (S5, `rwb_asset`) | transfer_in_date | Read, one input of the holding age |
| DF-COL-037 | asset (S5, `rwb_asset`) | book_value | Read, the base of the step and of the charge |
| DF-COL-038 | asset (S5, `rwb_asset`) | auction_purchase_price | Read where present |
| DF-COL-039 | asset (S5, `rwb_asset`) | repossessed_date | Read, one input of the holding age |
| DF-COL-040 | asset (S5, `rwb_asset`) | stock_date | Read, the holding start date the clock is armed from |
| The holding and provision fields | asset (S5, `rwb_asset`) | cost to date, holding age, next provision step date | Not specified in the source documents (GAP-2855; ASM-4726): kept as workflow and reference facts, written only where the DB story publishes a column |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_asset`) | rule id, rule version, inputs reference, holding start date, threshold, outcome, decided at | Write through the library, before the asset changes |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | the two clocks | Not read and not written: durable workflow timers, and the row is P3's (BR4) |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and the rest | Not read: no `v_ace_*` grant (BR6) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code, route state | Not read as a table: the state arrives on the contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, route_set, from_state, event_code and the rest | Not read: the rows arrive in the package |

Field IDs are those of the Logical Data Model and Data Dictionary v9 and of the legacy Data table. The FSD S5 and TSD S5 files that would carry the rest of the field set are not in `_work/msr/extract` for this WP, so the asset columns are the ten the dictionary gives and the remaining fields carry the placeholder (GAP-2855; ASM-4726). **No new table, no new column and no migration**: the existing columns are written, and `decision_record` and `idempotency_key` are library objects created by the library's own migration (DP-03).

**No personal data.** Rows carry identifiers, codes, amounts, dates and a rule version; no name, address, contact value or identity number enters the asset, the record, a log, a workflow input or a provision input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). This story supplies the behaviour behind the two reads whose shapes RWB-S5-E3023-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its holding age, its cost to date, its next provision step date and its listing references | Asset and disposal, right R, scope applied | Not applicable |

The errors are 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 when the record library or a consumed contract does not answer. The operation IDs are the ones the CON baseline fixes and are not redefined here. `POST /assets/{assetId}/listings` and `POST /listings/{listingId}/rounds` belong to the pricing and auction stories and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2856; ASM-4730)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset fact: stock date, book value, asset type, transfer-in type and segment, with the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the title status; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2856; ASM-4730)) | rwb-case (P3) | P3 rwb-case | The move `ASSET_HELD` with the rule and its version; on the workflow boundary it is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are class C dependencies in fact that the plan's C row does not carry (GAP-2856; ASM-4730). The cost-of-carry request is a Temporal activity, not a REST row (12.5).

#### 12.3 Events published

None. Slide 19 OUT gives rwb-asset `AssetTakenOn` and `AssetSold`, neither of them a holding event, and slide 43 lists event 22 and no second event. The provision input leaves on the Finance provision feed, not on a Kafka topic, so this step writes no outbox row and a build that adds an event fails the absence test (GAP-2856; ASM-4727).

#### 12.4 Events consumed

None. Slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, none of which starts this step; it starts from the confirmation the parent forwards and from its own timer. This story holds no consumer group, no subscription and no inbox row.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new across the years of a holding; workflow ID: Not specified in the source documents (CG-ALL-9735); start rule: as stated in the Workflow start rule row of the header | `rwb-asset` | Input: the case, the route, the asset reference and the package in force; signals: the confirmation, the case state, the package in force; timers: the holding age and provision step clocks |
| `applyHoldingStep` | Activity, the confirmation step | `rwb-asset` | The case and the confirmation in; the rule ID with its version, the holding start date, the next step date, the cost to date and the case move out |
| `applyProvisionStep` | Activity, the provision step | `rwb-asset` | The case, the threshold and the asset in; the rule ID with its version, the step applied, the feed reference and the next threshold out |
| `requestCostOfCarry` | Activity on the owner's queue | `rwb-payment` | The case, the asset, the month, the book value and the rule version in; the posted amount and its reference out (ASM-4729) |

No child workflow for the case and none for the money exists in this service, and no activity is registered on another service's queue. This service posts nothing to ALS or the general ledger: every posting of the cost of carry, the proceeds and the fees is made by rwb-payment, and the cost of carry is requested from it for its month. The activity names are a target design choice that no source fixes (ASM-4735).

#### 12.6 Schedules

None. The clocks are durable timers inside the workflow, not Schedules, and this story owns no Schedule and no Quartz job (BR3). The service's single Schedule is JOB-19 Re-appraisal monthly, which belongs to RWB-S5-E3026-APP (Architecture v5 slide 44; Ownership Map jobs JOB-19).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| asset | S5 (`rwb_asset`) | The held asset; this story reads the columns of §11 and writes the holding facts the DB story publishes |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated confirmation and the threshold it holds |

Not owned and never read as a table: `recovery_case`, `timer` and `task` (P3), `collateral` and every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry`, `rule_row` and `rule_package` (P7), `listing` and `asset_sale` (S5, later stories'). No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The asset facts of asset `AST-2026-000511` with stock date, book value, type and transfer-in type; a stale product with its date; no answer beyond 2 s | AC1, X5 |
| rwb-case case-state fake | The states `ASSET_ON_BOOKS`, `ASSET_HELD` and `DISPOSAL_PAUSED_DEVIATION` with title status `clear`, `under_transfer` and `encumbered` | AC2, X3, X4 |
| rwb-case case-move fake | The move `ASSET_HELD` accepted and refused | AC2, X3 |
| rwb-payment cost-of-carry fake | The monthly charge recorded with its posting reference; no answer beyond 2 s | AC1, AC2, X5 |
| Finance provision feed fake | The provision input accepted with its reference, and the feed refusing it | AC1, X6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version with R-DIS-06 and R-DIS-09 | AC1, AC2 |
| Local decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer for case `RC-2026-000511` | AC1 |

The fakes are test-only and are replaced in SIT. The operation names of the rwb-source-data read, of the case-move answer and of the feed carry the placeholder until their owners confirm them (GAP-2856; ASM-4730, ASM-4735).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the source-data read, the case read and the move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event on this step; the provision input leaves on the feed |
| Temporal | 1 workflow, 3 activities | `AssetDisposalWorkflow` with two steps on `rwb-asset` and `requestCostOfCarry` on `rwb-payment`; two durable timers; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `holding`, package `th.co.scb.ace.workbench.recovery.asset.holding`; front end `src/modules/recovery/asset/AssetHolding.tsx`, the fragment the two screens embed, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: no `v_ace_*` grant, no ACE view and no ACE table is read here (ASM-4731). DP-03 is the transaction rule of both steps. DP-13 moves the base and nothing else. DP-19 is how the two screens reach this service. DP-10 is held as a prohibition and not listed: the legacy clocks were scheduled work and are durable workflow timers in the target, so no Schedule library and no job row is introduced (BR3).

**Dependencies.** The two H rows the table adds are already in the plan's build list. The three consumed reads and the rwb-payment activity are C dependencies in fact while the plan's C row is None, so the story builds on their fakes on Day 1 and the absence is recorded (GAP-2856; ASM-4729, ASM-4730).

| Component | Type | Responsibility |
|---|---|---|
| `AssetDisposalWorkflow` holding branch | Workflow | Waits for the confirmation, arms the two clocks, fires the provision step and reports to the parent |
| `applyHoldingStep` | Activity | Reads the fact and the case, evaluates R-DIS-06, writes the record, arms the clocks, requests the charge, updates the asset, answers the move |
| `applyProvisionStep` | Activity | Evaluates R-DIS-09 at the threshold, writes the record, applies the step, sends the input and rearms |
| `HoldingAgeEvaluator` | Service | The rule evaluation against the package in force, with the thresholds read as its values |
| `HoldingDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and version before any change and refuses the step when the write fails (DP-03) |
| `HoldingClockArmer` | Workflow helper | Arms, holds and rearms the two durable timers across Continue-As-New |
| `CostOfCarryClient` | Activity client | The monthly request on `rwb-payment`, with its timeout and no posting of its own |
| `ProvisionFeedClient` | Client | Hands the provision input to the feed with its reference, its retry and its refusal path |
| `CaseStateClient` | Client | The case state read and the move answer of rwb-case, one hop, 2 s |
| `HoldingWriter` | Repository | Updates `asset` with the holding facts in one transaction, with the idempotency row and the optimistic lock |
| `AssetController` | Controller | The two reads, the right, the pagination and the problem mapping of 400 to 503 |
| `AssetHolding` | React component | Shows the age, the cost to date and the next step on the two screens, read only |

**Database and migrations.** No Flyway file. `asset` arrives with the DB story, and the record and the idempotency key are library objects created in `rwb_asset` by the library's migration (DP-03). The model gives no age, next-date or cost column, so the age and the next date are workflow and reference facts (GAP-2855; ASM-4726). The schemas `rwb_case`, `rwb_decision` and `rwb_payment` named in the build steps belong to rwb-case, rwb-decision and rwb-payment; this story writes none of them and reads none of them as a table.

**Configuration.** The DISPOSAL package at its version in force with R-DIS-06 and R-DIS-09; the thresholds, the step percentages, the cost-of-carry rate and the held-asset re-appraisal interval as its values and as reference data, tested through the test profile (BR5). They are versioned parameters owned by the NPA and asset manager role, loaded with the package version and shown on the asset record, and no value of them is stated in this file (GAP-1468). The parameters are the threshold, the step percentage and the cost-of-carry rate; the reference-data contract that carries them is Not specified in the source documents (DOR-RWB-S5-E3023-APP-20; DP-06, DP-07). Which date opens the clock is Not specified in the source documents (GAP-2855; ASM-4726), so the value is read and never hard-coded. The capability area "Asset and disposal" and right R are access rows of rwb-access. The 2 s budget and the single hop are ADR-020.

**Build steps**

1. The holding branch and its input record, registered on `rwb-asset` as the stage child, with the confirmation as trigger.
2. `CaseStateClient` and the fakes with the budget, the breaker and the no-answer path (AC2, X5).
3. `HoldingAgeEvaluator` with R-DIS-06, the title condition and the no-fire path (AC2, X4).
4. `HoldingDecisionRecordWriter` against the stub with the failed-write path (AC3, X1).
5. `HoldingClockArmer` with a shortened test interval, a Continue-As-New mid-hold and a redeploy mid-hold (AC2, BR3).
6. `requestCostOfCarry` and `HoldingWriter` with one transaction and the idempotency row (AC1, AC2, X7).
7. `applyProvisionStep` with R-DIS-09, the threshold test, the record, the input and the rearm (AC1, X6).
8. `ProvisionFeedClient` with the retry, the refusal and the task-after-limit path (X6).
9. `CaseMoveAnswer` and the parent signal with the `ASSET_HELD` move (AC2).
10. `AssetController` and `AssetHolding` with the right, the pagination and the problem mapping (AC1).
11. The boundary test: nothing outside `rwb_asset`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision`, `rwb_payment` or `timer` (X8, BR4, BR6).

**Feature flag.** `rwb.asset.holding-v1`; off means the step holds the confirmation, arms no clock and answers no move, and the take-on and sale stories are unaffected.

**Done when.** The tests of §16 pass, the step runs from a synthetic confirmation, R-DIS-06 produces its record, its clocks, its charge and its move, R-DIS-09 produces its record, its input and its rearm, a repeat writes once, a forced record failure changes nothing, a redeploy mid-hold keeps both clocks, no `recovery_case` row, no `timer` row and no `v_ace_*` read exists in the build, and the two screens answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy set of this key; it names the floor and the approval limit, which are the pricing story's, so no path here raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy set; it names the age of an appraisal, which is the re-appraisal story's, so no path here raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request or of the asset fact is absent or invalid (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the Asset and disposal right reads the list or the asset (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written before the asset changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are the legacy message set of RWB-E3-023, copied unchanged; no message is reworded and no new one is added. The feed refusal of X6 has no message ID in any source available to this file, so it is logged with its reference and shown as a task (GAP-2856).

### 15. Screens and states

SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its take-on, held, listed and sold states are served through the gateway-bff composite route (DP-19). SCR-21 empty, error and no access states: Not specified in the source documents (CG-ALL-9742). SCR-22 empty, loading, error and no access states: Not specified in the source documents (CG-ALL-9743). The route calls rwb-asset for the asset and its holding facts, rwb-case for the case and its route state and rwb-source-data for the ACE asset fact; this story fixes the rwb-asset answers only, and the route specification and the screen field list belong to RWB-PLT-N001-CON.

The states this story produces are the held state of SCR-22 — the age in days, the cost to date, the next step date and the rule version of the last step — and the refusal and failure states it shows: refused with MSG-P4-002 and not recorded with MSG-P7-003. The take-on, listed and sold states belong to the take-on and sale stories and are read from the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-023-01 | AC1 | Component | Asset `AST-2026-000511` for case `RC-2026-000511` with stock date, book value and title cleared; the age, the step, the record and the feed input asserted on the fakes with a shortened interval |
| TC-E3-023-02 | AC2 | Component | Case `RC-2026-000511` at `ASSET_ON_BOOKS` with title cleared; both clocks armed, the charge answered and the `ASSET_HELD` move sent |
| TC-E3-023-03 | AC3 | Component | The record stub stopped; nothing written, no clock armed and MSG-P7-003 shown |
| TC-E3-023-04 | Access | Component | A role without the Asset and disposal right; 403 with MSG-P4-002 and no read |
| TC-E3-023-05 | Principle 5 | Component | A forced record failure at the moment of the asset update; no asset change, no charge request and no answer |
| TC-E3-023-06 | Section 12 | Contract | Each operation, event and activity of section 12 checked against the published contract of its owner, with its fake answering the published shape and no field outside the contract |
| TC-E3-023-07 | Section 12.7; AC5 | Boundary | The tables of section 12.7 and the statements of the build: a statement against a `v_ace_*` view, a `recovery_case` row, a `timer` row or another schema is refused and fails the build |
| TC-E3-023-08 | BR10, BR11 | Component | Asset with a DISPOSAL_PAUSED_DEVIATION case state; the step is held, the age is still counted from dates, and no name, address, contact value or identity number appears in the record, the log or the provision input |
| TC-E3-023-09 | AC10 | Component | Case at `ASSET_HELD` with a status change the model does not allow; the change refused, nothing written and no record; data: Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC10) |
| TC-E3-023-10 | AC4, X2 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC4); 403 with MSG-P4-002 and no record written |
| TC-E3-023-11 | AC5, X8 | Boundary | Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC5); the grant refuses the statement and the build fails |
| TC-E3-023-12 | AC6 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC6); the rules of section 8 asserted on the fakes |
| TC-E3-023-13 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC7); the 401, 403 and 404 answers asserted with nothing changed |
| TC-E3-023-14 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC8); a failing and a timed-out activity with the retry and the stop asserted |
| TC-E3-023-15 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-S5-E3023-APP-AC9); a failed and an unanswered rwb-payment call with nothing changed |

The five legacy cases are the legacy cases in their legacy order, with the Level column added: `System` maps to `Component` because every path runs on its fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in code: the thresholds, the percentages, the rate, the lists and the rule rows stay data, reference data or the package, never a constant, a default or a branch.
- No personal data in the asset, a provision or charge input, a workflow input or a log: identifiers, codes, amounts, dates and a rule version only; fixtures are synthetic.
- ACE data only through the owner's contract: no `v_ace_*` grant and no ACE table, and a build that adds one fails the boundary test (DP-05).
- The case stays with rwb-case and the money with rwb-payment: no `recovery_case` row, no `timer` row, no posting, no balance and no ledger row here (BR4, BR7, BR8).
- The clocks are workflow timers: no Quartz row, no job table, no Schedule and no second clock for the same asset.
- The decision is recorded before the change; a build that changes the asset first fails the review (DP-03).
- One base, one topic, one queue and one login per service; no document or test names another service's base, topic or queue as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no data-lake extract of the step and no shared scheduler.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Story element | Test cases |
|---|---|---|---|---|---|
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule (Business Requirements Program v5, Must, E3); the plan carries no requirement id for this slice (GAP-2857; ASM-4733) | FEAT-AST-05 | Not specified in the source documents (DOR-RWB-S5-E3023-APP-2) | The two clocks, the provision step and the record | TC-E3-023-01, TC-E3-023-02, TC-E3-023-03 |
| ADR-013 | 19 services inside ACE | FEAT-AST-05 | Not specified in the source documents (DOR-RWB-S5-E3023-APP-2) | rwb-asset as the owner of the holding facts | TC-E3-023-02 |
| ADR-014 | Schema and login per service | FEAT-AST-05 | Not specified in the source documents (DOR-RWB-S5-E3023-APP-2) | `rwb_asset` and its own login | TC-E3-023-05 |
| ADR-016 | Temporal layer; Schedules replace Quartz | FEAT-AST-05 | Not specified in the source documents (DOR-RWB-S5-E3023-APP-2) | The two durable timers | TC-E3-023-02 |
| ADR-020 | Contract-first REST, one hop, 2 s | FEAT-AST-05 | Not specified in the source documents (DOR-RWB-S5-E3023-APP-2) | The three consumed rows | TC-E3-023-01 |
| ADR-022 | Local decision record plus central ledger | FEAT-AST-05 | Not specified in the source documents (DOR-RWB-S5-E3023-APP-2) | The record written before the change | TC-E3-023-03, TC-E3-023-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-023, disposition Split (rework) |
| Legacy criteria | AC1 to AC3, owned word for word by this story |
| Test cases | TC-E3-023-01 to TC-E3-023-05 |
| Feature and screens | FEAT-AST-05, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-06 and R-DIS-09, governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of RWB-S5-E3023-CON: the two reads, the holding and provision elements, the provision input, the consumed rows, the error set and the fakes.
- The take-on of the asset, the `asset` row and the confirmation of the record: RWB-S5-E3019-APP, RWB-S5-E3020-APP and RWB-S5-E3021-APP.
- The case of record, its route states, the parent `CaseWorkflow` and the `timer` row: rwb-case (P3) (GAP-2856).
- The ACE asset fact and the freshness of the data product: rwb-source-data (P1) (ASM-4731).
- The posting, the ledger effect and the balance, and the transport and ownership of the Finance provision feed: rwb-payment (P8) and the feed's owner (GAP-2856).
- The DISPOSAL package, R-DIS-06, R-DIS-09 and the values of the thresholds and the rate: rwb-decision (P7).
- The re-appraisal cycle and its order: RWB-S5-E3026-APP and rwb-valuation (S1).
- The listing, the floor price, the rounds and the sale; the documents and their custody; the composite route and the screen field list (RWB-PLT-N001-CON); the cross-service journey (the wave 2 harness); and the deployment, flag, dashboards and runbook of this capability (the operations story of this key).

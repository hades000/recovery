# RWB-S4-E5019-APP Follow the LED auction ladder

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5019-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-019 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-T |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5019-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-019 for rwb-litigation. The three legacy acceptance criteria are kept word for word with their origin tag and now run as the LED auction step of `LitigationWorkflow` on task queue `rwb-litigation`; the four ladder rules R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67 are evaluated against the package in force; the legal action is opened on `POST /cases/{caseId}/legal-actions`, each round result is recorded on `PATCH /legal-actions/{legalActionId}` and the action is read on `GET /legal-actions/{legalActionId}` over the base `/api/recovery/litigation/v1` (DP-13); the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the step acts (DP-03); the case route state and the enforcement task are answered to rwb-case (P3), so this story writes no `recovery_case`, no `assignment` and no `task` row; SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19); the auction round, the price basis, the official value and the round result have no column, and the trigger, the auction-date timer and the three consumed owner contracts have no single source, so they are carried as inputs, record facts and the working read of the assumptions (GAP-2826; ASM-4673 to ASM-4678). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5019-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **enforcement owner (RW-ENFORCE)**, I want **the Workbench to open the LED auction from the reported seizure, follow the 100, 90, 80 and 70 percent steps of official value round by round from the LED result entered on the partner portal or received on the LIT interface, record each step and its decision and refer an asset unsold at 70 percent to the enforcement owner**, so that **enforcement runs for years without a spreadsheet, every round is recorded against the rule version in force, and an exhausted ladder reaches a named owner instead of an open file**.

This is the application slice of legacy RWB-E5-019. It owns:

- all three legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the LED auction step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67 on the round result and the price basis of official value;
- the stage states `LED_AUCTION`, `PROCEEDS_MATCHED` and `NO_BID_AT_70`, reported to the case of record as a case move, and the enforcement task request that R-LIT-67 opens for the enforcement owner;
- `POST /cases/{caseId}/legal-actions` (API-S4-002) to open the LED auction legal action at round 1, `GET /legal-actions/{legalActionId}` (API-S4-003) and `PATCH /legal-actions/{legalActionId}` (API-S4-004) to record each round, on base `/api/recovery/litigation/v1`, under capability area "Litigation" with the rights C, R and U (DP-13);
- the local decision record of each ladder step, written through RWB-PLT-E1027-CON before the step acts (DP-03);
- SCR-20 Enforcement workspace in its seized and auctioned states and SCR-19 Litigation workspace in its judgment state, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the three operations, the auction element, the vocabularies, the error set and the fakes, which are RWB-S4-E5019-CON; the writ and the seizure that open the auction, which are R-LIT-54 and the sibling seizure story of this service; the matching and posting of the sale proceeds under R-LIT-65, which are RWB-S4-E5022-APP and rwb-payment (P8); the case of record, its route state, the parent `CaseWorkflow` and the enforcement task row, which are rwb-case (P3); the authoring, testing and approval of the four rules, which are rwb-decision (P7); the LED portal and LIT interfaces, which are entered by the Legal Execution Department and the firm through the partner portal and loaded by rwb-integration (P2); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-019 gave the Workbench one step that tracked the enforcement auction through the 100, 90, 80 and 70 percent steps of official value. The functional specification keeps the same sentence as the business objective and keeps the metric: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today (FSD S4 A2.19.1). The program keeps the requirement REQ-S4-007, "Enforcement after judgment has one named owner from judgment to the end of enforcement", which is exactly what AC2 asks when the exhausted ladder is referred to the enforcement owner (GAP-2826; ASM-4675).

What D-RCV-60 changes is where the parts of the step live. In the monolith one process held the legal action, the case row, the assignment, the decision log entry and the rule row in one `recovery` schema. In the target:

- **the auction facts are the LED's and the firm's.** The round, the price basis of official value, the official value, the round result, the bid amount and the auction date arrive as the Legal Execution Department's result on the partner portal or on the LIT interface (INT-09, INT-33); this service records them. The context pack gives this service two tables, `legal_action` and `hearing`, and neither carries an auction column, so the facts are inputs of the operation and facts of the decision record rather than new columns (GAP-2826; ASM-4673);
- **the case, its route state and the enforcement task are rwb-case's.** `recovery_case`, `assignment` and `task` are P3's rows; `LED_AUCTION`, `PROCEEDS_MATCHED` and `NO_BID_AT_70` are answered as a case move and never written here (GAP-2826; ASM-4673);
- **the rules are governed elsewhere.** R-LIT-63 to R-LIT-67 are rows of the LITIGATION route set, authored, tested and approved in rwb-decision and loaded here on the package in force; this story evaluates them and declares none (GAP-2826; ASM-4653);
- **the money stays with rwb-payment.** R-LIT-65 matches the proceeds of a sold round; this story records the sold result and answers the move `PROCEEDS_MATCHED`, and the match, the application to the balance and the posting are RWB-S4-E5022-APP and rwb-payment (P8). No `proceeds` row and no ledger entry is written here (GAP-2826; ASM-4678);
- **the decision is recorded first**, in the same transaction as the stage change and the action update, which is what legacy AC1 asked for and legacy AC3 tested.

Two facts the legacy wording implies but no source stores. First, the ladder has four rounds with a price basis of 100, 90, 80 and 70 percent of official value; the values are the rule rows, not constants, and no table holds the round. Second, "ladder exhausted" is a stage of the journey, not a legal-action status: `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED and WITHDRAWN and names no auction step, so the action stays `ENFORCING` while the stage moves (GAP-2826; ASM-4673).

The metric of the feature is unchanged and no business value moves: the D7 route set, the day counts of R-LIT-65 and R-LIT-67, the four price bases, the state names and the message texts are values in force in reference data and in the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S4-E5019-CON is published: the three operations, the auction element, the vocabularies, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read and case-move answer are available with their fake, so the route state and the enforcement task request can be exercised on Day 1. Neither row is in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2826; ASM-4653).
- The rwb-decision rule-package read is available with its fake: the LITIGATION package at its version with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67. No source names the operation, so it is Not specified in the source documents (GAP-2826; ASM-4653).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the stage change, the action update and their record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 and SCR-20 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` exists in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-014 and the standard record columns of TSD S4 T3.0; `hearing` exists for the judgment facts the enforcement follows; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version with the four rules and the D7 route set. The package, its rule rows, the four price bases and the day counts are authored, tested and approved in rwb-decision and in reference data; this story declares none of them (GAP-2826; ASM-4653).
- The LED round result is entered on the partner portal by the Legal Execution Department or by the panel firm under `PT-LAWFIRM`, and the LIT lawsuit facts arrive on the LIT interface (INT-09, daily end of day, COLLINS batch) through rwb-integration (P2). This service reads no `v_ace_*` view and holds no grant on one (GAP-2826; ASM-4677).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_decision`, `rwb_payment` or `rwb_reporting` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5019-CON when its tests pass, and the story stays at status Draft until the verification loop collects the sign-offs (GAP-2826; ASM-4676).

### 4. Flow

1. The auction opens. The asset is seized and the seizure is reported, and either the firm enters the result on the partner portal through this service's own operations or the LIT interface of the overnight chain updates the action. Both paths end in an auction signal of `LitigationWorkflow` on task queue `rwb-litigation`; no source names the signal and no event and no Schedule is declared (GAP-2826; ASM-4674).
2. On R-LIT-63 the step opens the LED auction at round 1 with the price basis of 100 percent of official value: `POST /cases/{caseId}/legal-actions` (API-S4-002) creates the legal action of type `LED_AUCTION` of `LOV-LEGAL-TYPE` with `status` `ENFORCING` of `LOV-LEGAL-STATUS`, the case reference and the action type, and the stage moves to `LED_AUCTION` (AC1).
3. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, `status` (DF-LEG-014), `claim_amount` (DF-LEG-009), `judgment_date` and `judgment_amount` (DF-LEG-011, DF-LEG-012) and the court facts.
4. The step reads the auction element of the request: the auction round (1 to 4), `auction_price_basis` (100, 90, 80 or 70 percent of official value), `official_value`, `round_result` (sold or no bid), `bid_amount` where the round sold, the auction date and the LED reference. No value is computed here and none is defaulted (GAP-2826; ASM-4673).
5. `AuctionLadderEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates the round in the state in force: `LED_AUCTION` for R-LIT-65, R-LIT-66 and R-LIT-67, and `WRIT_AND_SEIZURE` for R-LIT-63. A result on a case in any other state fires no rule and is refused (X4).
6. `AuctionDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the round, the price basis, the official value, the round result, the bid amount, the auction date, the inputs reference and the stage outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
7. `recordAuctionRound` writes the round inside one transaction with the record: `PATCH /legal-actions/{legalActionId}` (API-S4-004) carries the round element, and the action keeps `status` `ENFORCING`. No auction column is written, because `legal_action` has none (GAP-2826; ASM-4673).
8. On R-LIT-66 (no bid and round below 4) the stage stays `LED_AUCTION` and `armNextAuctionDate` arms one durable timer to the next auction date, read as the LED's date for the round. No `timer` row, no Schedule and no Quartz row is created (GAP-2826; ASM-4674).
9. On R-LIT-65 (sold at 100, 90, 80 or 70 percent) the stage moves to `PROCEEDS_MATCHED` and the move is answered to rwb-case with the rule ID and its version. The matching and the posting of the proceeds are RWB-S4-E5022-APP and rwb-payment (P8); this service records the sold result and answers the move (GAP-2826; ASM-4678).
10. On R-LIT-67 (no bid at the 70 percent basis) the unsold result is recorded, the stage moves to `NO_BID_AT_70`, the case move is answered and an enforcement task is requested from rwb-case for RW-ENFORCE with the task code, the due date from the 5 working days of R-LIT-67 and the rule ID with its version. rwb-case writes the `recovery_case` row, its route state and the `task` row; this service writes none of the three (GAP-2826; ASM-4673).
11. A repeated round result with the same case, action, round and reference writes nothing, sends no second case-move answer and no second task request, and counts the repeat; the stored answer is returned.
12. SCR-20 shows the auction step as seized or auctioned with the round, the price basis and the rule version; SCR-19 shows the judgment the ladder follows, read through the gateway-bff composite route (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the action keeps its columns and status, no case move and no task request leaves the service | MSG-P7-003 | AC3, TC-E5-019-03, TC-E5-019-05 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | TC-E5-019-04 |
| X3 | The legal action does not exist, or it is outside the caller's scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC1, AC2 |
| X4 | The action is `CLOSED` or `WITHDRAWN`, the stage is not `LED_AUCTION` or `WRIT_AND_SEIZURE`, the round is not the next one on the ladder, or a result is recorded twice for the same round | 409 and nothing changes; no rule fires on a closed action or on a round out of order | None | AC1, AC2 |
| X5 | A required element of the round is absent or invalid (no round, a round outside 1 to 4, no price basis, no round result, a negative official value or bid) | 422 and nothing is written; no rule is evaluated and no record is written | MSG-GEN-001 | AC1, AC2 |
| X6 | The case read, the case-move answer or the rule package does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC3 |
| X7 | The same round, the same case move or the same task request arrives twice | One write, one case-move answer and one task request; the repeat is counted and no second decision record is written | None | AC1, AC2 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1, AC2 |
| X9 | A component, a statement or a test reaches a `recovery_case` row, an `assignment` row, a `task` row, a `rule_row`, a `decision_log_entry`, a proceeds row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR6 |

X1 to X4 are the exception paths of RWB-E5-019 carried onto the split, X5 to X8 are the paths the target call types add, and X9 is the DP-01 boundary. The four price bases, the day counts of R-LIT-65 and R-LIT-67 and the D7 route set are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5019-CON and the consumed fakes, on the tables of its own schema, and needs no live rwb-case, rwb-decision, rwb-payment or rwb-integration |
| Negotiable | The activity names, the decision code per rule and the shape of the enforcement task request are this story's choice; the rules, the messages, the screens, the three operations and the state names are fixed |
| Valuable | Four auction rounds and an exhausted ladder reach the action, the stage and the enforcement owner with each decision recorded, instead of a spreadsheet per asset |
| Estimable | One workflow branch, one evaluator, one record write, one action create or update, one case-move answer with its task request, one timer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and round results through the contract fakes, plus the component case of the access answer and the NFR case of the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Follow the LED auction ladder

  Background:
    Given case "RC-2026-000719" carries the enforcement legal action "LA-2026-000719" at the stage "LED_AUCTION"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Follow the LED auction ladder (legacy RWB-E5-019 AC1)
    Given the rwb-case contract mock returns the case state "LED_AUCTION" for case "RC-2026-000719"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67 at its version
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tracks the enforcement auction through the 100, 90, 80 and 70 percent steps of official value
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-67 (legacy RWB-E5-019 AC2)
    Given the rwb-case contract mock returns the case state "LED_AUCTION" for case "RC-2026-000719"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67 at its version
    Given a case in state LED_AUCTION
    When ladder exhausted
    Then record the unsold result and refer it to the enforcement owner
    Then the case moves to NO_BID_AT_70

  Scenario: AC3 Not recorded (legacy RWB-E5-019 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E5-019 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the lower-case opening of the second `Then` in AC1, the legacy wording of `its trigger arrives`, `ladder exhausted` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 and AC2 carry the `Given the <service> contract mock returns <x>` lines above, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-case holds the case of record, its route state and the enforcement task; rwb-decision governs the four rules and their package; and this story opens the action, records each round, records the decision with the rule version and answers the case move. The legacy `recovery_case` and `assignment` writes are not reproduced here (GAP-2826; ASM-4673).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-63 | Litigation | D7 | WRIT_AND_SEIZURE | SEIZURE_EXECUTED | the asset is seized and the seizure reported | Open the LED auction at round 1 | LED_AUCTION | Legal Execution Department | Partner Portal, LED | To the auction date |
| R-LIT-65 | Litigation | D7 | LED_AUCTION | ROUND_SOLD | round_result = sold at 100, 90, 80 or 70 percent of official value | Match the proceeds to the case | PROCEEDS_MATCHED | Workbench | LED, ALS core | 2 working days |
| R-LIT-66 | Litigation | D7 | LED_AUCTION | ROUND_NO_BID | round_result = no bid and auction_round < 4 | Step the price to the next round on the ladder | LED_AUCTION | Legal Execution Department | LED, Partner Portal | To the next auction date |
| R-LIT-67 | Litigation | D7 | LED_AUCTION | LADDER_EXHAUSTED | round_result = no bid and auction_price_basis = 70 percent | Record the unsold result and refer it to the enforcement owner | NO_BID_AT_70 | Enforcement owner | LED, Partner Portal | 5 working days |

The four rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: "Legal Execution Department" is the external LED, "Workbench" is the record this story writes on the action, and "Enforcement owner" is the RW-ENFORCE task owner that the case of record assigns. R-LIT-64 (the seizure obstructed, 10 working days) is the seizure story's and is named here only because it shares the `WRIT_AND_SEIZURE` state.

| ID | Rule | Source |
|---|---|---|
| BR1 | The LED auction step and the legal action are this service's: the stage states `LED_AUCTION`, `PROCEEDS_MATCHED` and `NO_BID_AT_70` are states of the LITIGATION machine on `LitigationWorkflow`, and the action type and status are columns of `legal_action` in `rwb_litigation` | FSD S4 A2.19; TSD S4 T4; context pack (legal_action and hearing owner S4) |
| BR2 | The decision is recorded before the step acts, with the rule ID and the package version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-019 AC1 and AC3 |
| BR3 | The case of record, its route state and the enforcement task stay with rwb-case: this story answers the move and requests the task, and writes no `recovery_case` row, no `assignment` row and no `task` row | context pack (recovery_case and task owner P3); TSD S4 T5.2; GAP-2826 |
| BR4 | The ladder is four rounds at 100, 90, 80 and 70 percent of official value and is never derived: a no bid below round 4 steps the price under R-LIT-66, a no bid at the 70 percent basis exhausts the ladder under R-LIT-67, and a sold round at any of the four bases takes R-LIT-65 | Business Rules and Routing Logic v4 (R-LIT-65 to R-LIT-67) |
| BR5 | Only `status` and the standard record columns are written on the action; the round, the price basis, the official value, the round result, the bid amount and the auction date have no column and are carried as inputs and as decision-record facts | TSD S4 T3.1 (DF-LEG-001 to DF-LEG-014); GAP-2826; ASM-4673 |
| BR6 | The proceeds of a sold round are never written here: R-LIT-65 answers the move `PROCEEDS_MATCHED` and the match, the application to the balance and the posting are RWB-S4-E5022-APP and rwb-payment (P8) | context pack (payment rows owner P8); FSD S4 A2.22; GAP-2826 |
| BR7 | The next auction date is one durable timer of `LitigationWorkflow`, armed from the LED's date; no `timer` row, no Temporal Schedule and no Quartz row is created | GAP-2826; ASM-4674; DP-10 held as a prohibition |
| BR8 | The same round, case move or task request twice writes once and counts the repeat | TSD S4 T-A.2; legacy AC1 |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case references, action references, codes, dates, percentages and amounts | Template and Rules v1 §R7.2 (s17); TSD S4 T6.2 |

**Where each rule lives in the target.** R-LIT-63 is the opening step: the seizure is reported, the LED auction action is created at round 1 with the 100 percent basis, the status is `ENFORCING` and the stage is `LED_AUCTION`. R-LIT-66 is the stepping step: a no bid below round 4 keeps the stage and arms the next auction date. R-LIT-65 is the sold step: the round result is recorded, the stage moves to `PROCEEDS_MATCHED` and the move is answered for the money story. R-LIT-67 is the exhausted step: the unsold result is recorded, the stage moves to `NO_BID_AT_70` and the enforcement task is requested. VR-S4-019-1 of the FSD (a stale data product after a late or failed ACE batch, MSG-P1-001) is carried in section 14 and is raised by the ACE-fed reads of P1, not by a path of this story.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story does own is the stage of `LitigationWorkflow` and the round of the ladder.

| From (stage of `LitigationWorkflow`) | Event | Condition | To |
|---|---|---|---|
| `WRIT_AND_SEIZURE` | SEIZURE_EXECUTED under R-LIT-63 | The seizure is reported | `LED_AUCTION` at round 1 and the 100 percent basis, with the case-move answer `LED_AUCTION` |
| `LED_AUCTION`, round 1 to 3 | ROUND_NO_BID under R-LIT-66 | round_result = no bid and auction_round < 4 | `LED_AUCTION` at the next round and basis, with the next auction date armed |
| `LED_AUCTION`, any round | ROUND_SOLD under R-LIT-65 | round_result = sold at 100, 90, 80 or 70 percent of official value | `PROCEEDS_MATCHED`, with the case-move answer `PROCEEDS_MATCHED` |
| `LED_AUCTION`, round 4 at the 70 percent basis | LADDER_EXHAUSTED under R-LIT-67 | round_result = no bid and auction_price_basis = 70 percent | `NO_BID_AT_70`, with the enforcement task requested for RW-ENFORCE |
| `WRIT_AND_SEIZURE` | SEIZURE_BLOCKED under R-LIT-64 | The seizure is obstructed, or the asset has moved | `ENFORCEMENT_DECISION`: the seizure story's, not written here |
| Any other stage | Any round event | The stage is not the one the rule expects | Unchanged, refused with 409 (X4) |
| Any | A round on an action that is `CLOSED` or `WITHDRAWN`, or a round out of order | X4 | Unchanged, refused with 409 |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | An auction signal arrives for a case at `WRIT_AND_SEIZURE` or `LED_AUCTION` | The package in force is loaded | Evaluating |
| Evaluating | One of the four rules fires | The round element is valid and the decision record is written | Applying |
| Applying | The action create or update, the stage move and the case-move answer commit | The transaction commits | Waiting for the next round |
| Applying | The record write, the action update or the move fails | X1, X6 | Waiting, nothing changed |
| Applying | A round element is absent or invalid | X5 | Waiting, refused with 422 and nothing changed |

The action status is `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED` or `WITHDRAWN` (TSD S4 T3.2). The LED auction action is created at `ENFORCING` under R-LIT-63 and stays `ENFORCING` through all four rounds; `CLOSED` belongs to R-LIT-51 and R-LIT-70 of RWB-S4-E5022-APP, and `WITHDRAWN` belongs to the withdrawal step. The ladder's own states are stages of the journey, not list values (GAP-2826; ASM-4673).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix: opens and reads the auction action and works the step on SCR-19 and SCR-20 |
| RW-ENFORCE, enforcement owner | Litigation CRU: the "also uses" role of the FSD and the owner of R-LIT-67; reads the ladder and receives the unsold referral and its task |
| PT-LAWFIRM, law firm user | Litigation RU: enters the round result, the price basis, the official value, the bid and the auction date on the partner portal through this service's operations, scoped to its own cases |
| RW-LEGAL, Head of Litigation (RW-HEADLIT), product head (RW-PRODHEAD) | Litigation RA or R as the T6.1 matrix gives it: read and approve; no round is recorded by this step on their right |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| SY-DATALOAD, SY-CASEWF, SY-RULES, SY-AGENT | Litigation U or R as the T6.1 matrix gives it: the LIT load and the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the four rules, writes the decision record and the action, holds the stage and the timer and answers the case move; it holds no grant on another schema |

The rights above are the rows of TSD S4 T6.1 and the legacy permission table of this key: Litigation `C` for RW-LITOFF and RW-ENFORCE, Litigation `U` for RW-LITOFF, RW-ENFORCE, PT-LAWFIRM and SY-DATALOAD, and the read row of 23 roles and more for `R`. The FSD S4 A2.19.3.3 states that the step "runs unattended" with the enforcement owner as also-user, while the legacy story names an enforcement owner and gives the create right to the litigation and enforcement roles; both statements hold because the round result arrives from the LED and the firm and the officer confirms it, so no person is required for the step to run and none is excluded from it (GAP-2826; ASM-4674). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the record and of the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case-move answer and the task request |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read and written at creation against `LOV-LEGAL-TYPE`: the auction action is `LED_AUCTION` |
| DF-LEG-005, DF-LEG-006, DF-LEG-008 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no, court_name | Read, as the court facts of the enforcement action; not changed |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Read, as the amount enforced that the official value is measured against |
| DF-LEG-011, DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_date, judgment_amount | Read, as the judgment the enforcement follows; not changed |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write `ENFORCING` at creation; unchanged through the four rounds (BR5) |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by` | Write through the repository; `version` is the optimistic lock of the round |
| DF-LEG-024 to DF-LEG-029 | hearing (S4, `rwb_litigation`) | hearing_date, hearing_type, outcome, next_date | Read only, as the judgment hearing of the action; no hearing row is written here |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the route state comes back on the case-move answer (BR3) |
| DF-WRK-009 to DF-WRK-016 | assignment (P3, `rwb_case`) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not written: the enforcement task and its assignment are requested on the case-move answer |
| DF-WRK-017 to DF-WRK-026 | task (P3, `rwb_case`) | id, case_id, task_code, element_type, discretion, status and 4 more | Not written: the unsold referral task is requested from P3 (BR3) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the action changes (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule package in force and never as a table |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1, the legacy story Data table and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). The auction round, the price basis, the official value, the round result, the bid amount and the auction date have no column and are not given one (BR5). The test fixtures are synthetic: case `RC-2026-000719`, action `LA-2026-000719`, a round sold at the 90 percent basis and a fourth round with no bid at the 70 percent basis.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind three operations whose shapes are declared by RWB-S4-E5019-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in with the LED auction action type and the round element, LegalAction of status 201 out (API-S4-002) | Litigation, right C, scope applied | Idempotency-Key header |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in with the round element, LegalAction of status 200 out (API-S4-004) | Litigation, right U, scope applied | Not applicable |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts, its judgment and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The auction is opened on the POST, each round is recorded on the PATCH, whose documented purpose is "record a filing, judgment or enforcement step" (TSD S4 T-A.2), and the action is read on the GET. Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed or wrong-stage action or a round out of order, 422 with MSG-GEN-001 for a missing or invalid round element, and 503 when the decision library, a consumed contract or the rule package does not answer. `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) belong to the sibling stories of this service and are not declared by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2826; ASM-4653)) | rwb-case (P3) | P3 rwb-case | The route state of the case, which must be the one R-LIT-63 to R-LIT-67 expect; faked |
| The case-move answer and the enforcement task request (operation name Not specified in the source documents (GAP-2826; ASM-4653)) | rwb-case (P3) | P3 rwb-case | The moves `LED_AUCTION`, `PROCEEDS_MATCHED` and `NO_BID_AT_70` and the task request of R-LIT-67 for the enforcement owner; the row and the route state are P3's, and on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule package in force (operation name Not specified in the source documents (GAP-2826; ASM-4653)) | rwb-decision (P7) | P7 rwb-decision | The LITIGATION package at its version with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All three are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2826 with ASM-4653.

#### 12.3 Events published

None. The service's topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its ownership rows list no event of this service. DP-09 is not in this story's pattern set: the step writes no outbox row, and its outputs are the local decision record of DP-03, the case-move answer and the task request. The auction result is a fact of this service and of the case of record, and reporting reads it from the event of its owner on the reporting contract, not from this topic.

#### 12.4 Events consumed

None. The ownership rows of this service list no consumed event either, so the round result arrives as a signal of `LitigationWorkflow` entered on the partner portal or on the LIT interface, and the case and the package arrive on their owners' contracts of 12.2 (GAP-2826; ASM-4674). This story holds no consumer group, no subscription and no inbox of its own, and a build that adds a consumer to `rwb.litigation.events.v1` or a subscription to another topic fails the absence test of the CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the seizure report, the round result, the rule package in force and the timer fire; outcome: the stage move for the parent |
| `openLedAuction` | Activity, the opening step of this story under R-LIT-63 | `rwb-litigation` | The seizure result in; the LED auction action at round 1 with the 100 percent basis, the decision record and the case-move answer out, in one transaction |
| `recordAuctionRound` | Activity, the stepping and sold steps under R-LIT-66 and R-LIT-65 | `rwb-litigation` | The round element in; the round fact, the decision record, the action update, the next auction date and the case-move answer out |
| `closeUnsoldLadder` | Activity, the exhausted step under R-LIT-67 | `rwb-litigation` | The fourth no-bid round in; the unsold fact, the decision record, the case move and the enforcement task request out |

The activity names are target design choices and are fixed by no source document; the trigger of the step is read as an auction signal, because the legacy story says the auction is tracked while the FSD says the step runs unattended and the LED result is entered on the partner portal (GAP-2826; ASM-4674). No cross-service call is made inside a workflow: each is an activity of the queue above.

#### 12.6 Schedules

None. The step runs from the auction signal and from the round result's arrival. The next auction date of R-LIT-66 is a durable timer of the workflow, read from the LED's date for the round, not a Schedule and not the `timer` row of rwb-case; this story registers no Temporal Schedule, no Quartz row and no shared job table, and no Job of the batch catalogue is owned or moved here (GAP-2826; ASM-4674).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Created and updated: `action_type` at creation, `status` `ENFORCING`, and the standard record columns; no auction column exists (BR5) |
| hearing | S4 (`rwb_litigation`) | Read only, as the judgment hearing the enforcement follows; no hearing row is written here |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of each ladder step (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated round and the answer it holds |

Not owned and never read as a table: `recovery_case`, `task` and `assignment` (P3), `rule_row` and `decision_log_entry` (P7), the proceeds and ledger rows (P8), `treatment` (S2) and `document` (P5). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read fake | The route state `WRIT_AND_SEIZURE` and `LED_AUCTION` of case `RC-2026-000719`, another state, and no answer beyond 2 s | AC1, AC2, X4 |
| rwb-case case-move fake | The moves `LED_AUCTION`, `PROCEEDS_MATCHED` and `NO_BID_AT_70` accepted with the enforcement task created for the enforcement owner, and a move refused because the case is not in the state the rule expects | AC1, AC2, X7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67, and a second version | AC1, AC2, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-20 answer in the seized and auctioned states and the SCR-19 answer in the judgment state for case `RC-2026-000719` | AC1, AC2 |
| Partner-portal entry fake | The Legal Execution Department's and the firm's round entry under `PT-LAWFIRM` through the PATCH operation, and a refused entry for an action outside the entry's scope | AC1, X2, X5 |

The fakes are test-only and are replaced by the real services in SIT. The three consumed rows carry the placeholder of 12.2 until their owners publish an operation name (GAP-2826; ASM-4653).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The action create, the action read and the action update on `/api/recovery/litigation/v1`; the case read, the case move with the task request and the rule package; one hop, 2 s each |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 3 activities, 1 durable timer | `LitigationWorkflow` with `openLedAuction`, `recordAuctionRound` and `closeUnsoldLadder` on `rwb-litigation`, and the next auction date; no Schedule |
| File | None | No file is read, built or delivered here; the LED and LIT data arrives as the Legal Execution Department's entry and on the P2 contract |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `auction`, Java package `th.co.scb.ace.workbench.recovery.litigation.auction`; front end `src/modules/recovery/litigation/FollowLedAuction.tsx`, the fragment SCR-20 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the action create or update and the stage change commit together or not at all, and the record is written before the case move leaves the service. DP-13 moves the base of the three operations and nothing else. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway. DP-05 is held as a prohibition because the service holds no `v_ace_*` grant, DP-09 and DP-10 because no event and no Schedule is declared, and DP-04 because the four rules are read from the package of P7 and evaluated by the embedded runtime of the service template (GAP-2826; ASM-4653, ASM-4677).

**Dependencies the tables add and the plan does not hold.** The three H rows are the plan's. The three consumed contracts of 12.2 are class C dependencies in fact and are not in the metadata row, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2826 with ASM-4653. No H row points to RWB-S4-E5018-APP (the writ and seizure, FEAT-LIT-18, the legacy Depends on) or to RWB-S4-E5022-APP (the proceeds match), and this story starts at `LED_AUCTION` on Day 1 as the plan requires (ASM-4678).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` auction branch | Workflow | The step that waits for the seizure and the round results, loads the package in force, arms the next auction date and reports the stage move to the parent |
| `openLedAuction` | Activity | Reads the seizure and the case state, evaluates R-LIT-63, creates the LED auction action at round 1 and answers the move `LED_AUCTION` |
| `recordAuctionRound` | Activity | Records the round, evaluates R-LIT-66 or R-LIT-65, writes the record, the action and the next timer or the move `PROCEEDS_MATCHED` |
| `closeUnsoldLadder` | Activity | Evaluates R-LIT-67, records the unsold result and the move to `NO_BID_AT_70`, and requests the enforcement task |
| `AuctionLadderEvaluator` | Service | The evaluation of the round and the price basis against the LITIGATION package version in force, with the state names of the LITIGATION machine |
| `AuctionDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `LegalActionRepository` | Repository | Creates and reads the action and writes `status` and the standard columns with the optimistic lock, on `rwb_litigation` only |
| `CaseMoveAnswer` and `EnforcementTaskRequest` | Signal reporter | Answer rwb-case with the move, the rule, the version and the task request; they report, they never change a case row |
| `LegalActionController` | Controller | The three operations, the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `FollowLedAuction` | React component | Shows the round, the price basis, the official value, the round result and the rule version on SCR-20, read only |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the round, the price basis, the official value, the round result, the bid amount or the auction date (BR5; GAP-2826; ASM-4673).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants; no auction or ladder value is added to the status list.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the four price bases, the 2 and 5 working days of R-LIT-65 and R-LIT-67 and the auction-date values are values of the package and of reference data, not of this build (GAP-2826; ASM-4653).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The auction branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the seizure and round signals as its trigger (ASM-4674).
2. `LegalActionRepository` over `legal_action` and `hearing`, with the creation of the LED auction action and the optimistic lock (AC1, AC2).
3. `AuctionLadderEvaluator` over the LITIGATION package, with R-LIT-63, R-LIT-65, R-LIT-66, R-LIT-67, the four rounds and the no-fire path (AC1, AC2, X4).
4. `AuctionDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X1).
5. `CaseMoveAnswer` and `EnforcementTaskRequest` with the three moves and the task request (AC1, AC2, X7).
6. The next auction date as a durable timer, read from the LED's date for the round (AC1).
7. `LegalActionController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, X2, X3, X5).
8. `FollowLedAuction` and the two workspaces through the composite route fake (AC1, AC2).
9. The boundary test: no statement outside `rwb_litigation`, no write to `rwb_case`, `rwb_decision`, `rwb_payment` or `rwb_reporting` (X9, BR3, BR6).

**Feature flag.** `rwb.litigation.led-auction-v1`, read as a flag of the platform library; off means the step holds the seizure and round signals, writes no action, no record and no timer and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic seizure and four synthetic rounds in SIT, R-LIT-63 creates the action at round 1, R-LIT-66 steps 100 to 90 to 80, R-LIT-65 records a sold round and answers `PROCEEDS_MATCHED`, R-LIT-67 records the unsold result and requests the enforcement task, a repeated round writes once, a forced record failure changes nothing, no `recovery_case` row and no `task` row is written from this service, and SCR-19 and SCR-20 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription story of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required element of the round is absent or invalid (X5) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or records the auction (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the action changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | VR-S4-019-1: a data product of the ACE-fed read is stale after a late or failed batch; the check belongs to P1 and this step reads the action of its own schema | {product} is from {date}. Today's ACE batch has not arrived. |

The five legacy texts are the legacy wording of RWB-E5-019 section 14 and of the FSD S4 A2.19 message list, copied unchanged; no message is reworded and no new message is added. `MSG-P1-001` is the FSD validation rule of the feature and is raised by the owner of the read, not here. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X6) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No new screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-20 Enforcement workspace | Requested | The enforcement step opened by the judgment story, its owner RW-ENFORCE and the action at `ENFORCING`, read only |
| SCR-20 Enforcement workspace | Seized | The LED auction action at round 1, its 100 percent price basis, the official value, the auction date and the rule R-LIT-63 with its version |
| SCR-20 Enforcement workspace | Auctioned | The round, the price basis, the official value, the round result and the bid, the rule R-LIT-65 or R-LIT-66 with its version, and the stage `LED_AUCTION` or `PROCEEDS_MATCHED` |
| SCR-20 Enforcement workspace | Closed | The unsold referral at `NO_BID_AT_70`, its enforcement task, the rule R-LIT-67 and its version; the later close is the proceeds story's, read only |
| SCR-19 Litigation workspace | Judgment | The judgment date, the amount and the court facts of the sibling story, read only, as the facts the enforcement follows |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |

The route merges this service's answer with rwb-case for the case, its route state and its task; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-019-01 | AC1 | End to end | Follow the LED auction ladder |
| TC-E5-019-02 | AC2 | End to end | Rule R-LIT-67 |
| TC-E5-019-03 | AC3 | Component | Not recorded |
| TC-E5-019-04 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-019-05 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The five legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 and AC2, the "System" level of the sibling legacy stories) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The case, package and route fakes of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000719`, action `LA-2026-000719` at `LED_AUCTION`, a round sold at the 90 percent basis and a fourth round with no bid at the 70 percent basis — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the four price bases, the day counts of R-LIT-65 and R-LIT-67, the list values and the message texts are values and reference rows with a version; no list value, state name, percentage or day count appears in Java.
- No personal data in logs, workflow inputs, prompts or the fixture: the rows carry case references, action references, codes, dates, percentages and amounts only, and the test data is synthetic.
- The case stays with rwb-case: no `recovery_case` row, no route state, no `assignment` row and no `task` row is written here, and the move and the task are requested with the rule and its version (BR3).
- The money stays with rwb-payment: no proceeds row, no ledger entry and no balance change is written here, and R-LIT-65 answers only the move (BR6).
- Only `action_type`, `status` and the standard columns are written on the action, and no auction or ladder value is added to a list to express a state that is a stage (BR5).
- ACE data only through its owner: no component of this story reads a `v_ace_*` view or an ACE table; the LED and LIT facts arrive on the entry of the Legal Execution Department and the P2 contract (GAP-2826; ASM-4677).
- No read of another service's tables and no cross-schema join: `recovery_case`, `task`, `assignment`, `rule_row`, `decision_log_entry`, `treatment` and `document` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second round.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing (12.3, 12.4).
- SCR-19 and SCR-20 are read only; the round result is posted through the service, and the Legal Execution Department's and the firm's entry on the partner portal uses the same operations under `PT-LAWFIRM`.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement, which this story does by following the ladder and referring an unsold asset at 70 percent to RW-ENFORCE (FSD S4 Requirements served) | FEAT-LIT-19 | 08 Litigate and enforce | R-LIT-63, R-LIT-65, R-LIT-66, R-LIT-67 | TC-E5-019-01, TC-E5-019-02, TC-E5-019-03 |

The legacy story master of RWB-E5-019 carries no requirement ID and the plan's requirement list for this slice is empty; the trace is the requirement the FSD S4 serves for enforcement after judgment, which is the outcome of the auction ladder (GAP-2826; ASM-4675).

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-019 | The three legacy criteria word for word, the four ladder rules, the two screens, the messages and the five test cases; the `recovery_case` and `assignment` writes of the legacy data table are P3's |
| RWB-S4-E5019-CON | H: the three operations, the auction element, the vocabularies, the error set and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| rwb-case (P3) and rwb-decision (P7) contracts | C in fact and not in the metadata row: the case read, the case move with the task request and the rule package, faked (GAP-2826) |
| FEAT-LIT-19, FEAT-LIT-18, SCR-19, SCR-20 | The feature, its seizure prerequisite and the two screens of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Temporal layer with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation and rwb-case, with the `-ITG` copies of the five cases |

### 19. Out of scope

- The published shape of the three operations, the auction element, the vocabularies, the error set and the fakes: RWB-S4-E5019-CON.
- The writ, the seizure and the obstruction (R-LIT-54, R-LIT-64), which open the ladder and share the `WRIT_AND_SEIZURE` state: the seizure story of this service (RWB-S4-E5018-APP).
- The matching and posting of the sale proceeds under R-LIT-65, which answers `PROCEEDS_MATCHED` here and is completed there: RWB-S4-E5022-APP and rwb-payment (P8) on RWB-P8-E4044-CON and RWB-P8-E4049-CON.
- The case of record, its route state, the parent `CaseWorkflow`, the assignment and the enforcement task row: rwb-case (P3), which creates the task on this story's request (GAP-2826; ASM-4673).
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-63, R-LIT-65, R-LIT-66 and R-LIT-67, and the price-basis values: rwb-decision (P7) and the reference-data owner (GAP-2826; ASM-4653).
- The LED portal, the LIT interface and the partner portal's own contract, and the ACE views: rwb-integration (P2), rwb-source-data (P1) and rwb-partner (S9); this service holds no `v_ace_*` grant (GAP-2826; ASM-4677).
- The notice, the pack, the firm instruction, the filing, the hearings and the prescription warning: the sibling stories of S4, rwb-document (P5) and rwb-comms (P6).
- The enforcement deferral, the bankruptcy petition and the write-off routing: RWB-S4-E5020-APP, RWB-S4-E5021-APP and rwb-writeoff (S7).
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access (P4) and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

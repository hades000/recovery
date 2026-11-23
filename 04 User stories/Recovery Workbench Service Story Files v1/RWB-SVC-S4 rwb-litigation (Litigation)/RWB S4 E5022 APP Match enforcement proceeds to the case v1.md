# RWB-S4-E5022-APP Match enforcement proceeds to the case

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5022-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S4-W |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5022-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-022 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the money is matched and posted by rwb-payment (P8) and arrives on the two P8 contracts, so the legacy `proceeds` write and the `v_ace_account` and `v_ace_payment` reads are retired (DP-05, prohibition); the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the legal action changes (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19); the trigger and the case-move answer have no source specification and are declared as the working read of the assumption (GAP-1891, GAP-1892, GAP-1893, GAP-1896; ASM-3106, ASM-3107, ASM-3108, ASM-3111). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **enforcement owner (RW-ENFORCE)**, I want **the Workbench to evaluate the payment-after-judgment or auction outcome of a case against R-LIT-51, R-LIT-65 and R-LIT-70, close the enforcement legal action, record the decision with the rule version before anything changes and answer rwb-case for the case move**, so that **a judgment or an LED auction closes in one recorded step on the money that rwb-payment has already matched and posted, instead of an officer re-keying a payment that another service owns**.

This is the application slice of legacy RWB-E5-022. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- one enforcement-matching step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19, "LitigationWorkflow (years; continues-as-new)"; Temporal and Drools Design slides 13 and 20);
- the evaluation of R-LIT-51, R-LIT-65 and R-LIT-70 on the matched money fact and on the judgment facts of the legal action, with the LITIGATION package version in force;
- `POST /cases/{caseId}/legal-actions` (API-S4-002), `GET /legal-actions/{legalActionId}` (API-S4-003) and `PATCH /legal-actions/{legalActionId}` (API-S4-004) on base `/api/recovery/litigation/v1`, under capability area "Litigation" with the rights C, R and U (DP-13; TSD S4 T-A.1);
- the writer of the `legal_action` status of the enforcement action and of the LED auction ladder entry, in schema `rwb_litigation`, with the columns of DF-LEG-001 to DF-LEG-014 and no new column;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the legal action changes (DP-03);
- the answer to rwb-case for the case move `CASE_CLOSED` or `PROCEEDS_MATCHED`, with the rule ID and the version that produced it;
- the two screens SCR-19 and SCR-20 as this service's answers, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the three operations, the action types, the match and close request and answer shapes, the error set and the fakes, which are RWB-S4-E5022-CON; the matching of the payment or the proceeds and the application of the money to the balance, which are rwb-payment (P8) on RWB-P8-E4044-CON and RWB-P8-E4049-CON; the case of record, its route state `CASE_CLOSED` or `PROCEEDS_MATCHED`, the parent `CaseWorkflow` and the case timers, which are rwb-case (P3); the approval of a close above a delegated limit, which is rwb-decision (P7) on its approval contract; the ACE account and payment facts, which are rwb-source-data's (P1); the document and retention of the closed file, which are rwb-document's (P5); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-022 gave the Workbench one step that matched money from the LED or the firm to the case and applied it to the balance, and it kept two rule outcomes: R-LIT-51 closed the enforcement and the case when a payment after judgment covered the balance and the costs, and R-LIT-65 matched the proceeds when the LED round sold at 100, 90, 80 or 70 percent of official value. The functional specification keeps the objective and its metric — a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today — and the program keeps the requirement: REQ-S4-010, "Proceeds from enforcement are matched to the case and posted" (FSD S4 A2.22 and its requirements-served list; Business Requirements Program v4).

What D-RCV-60 changes is who owns the money and who owns the case. In the monolith the match, the proceeds row, the balance application, the case state and the decision log row sat in one `recovery` schema and one process. In the target:

- **the money is matched and posted by rwb-payment (P8).** `proceeds` is P8's table, `matchPayments` and `postProceeds` are P8's activities, and the `ProceedsMatched` event is published by rwb-payment (Ownership Map: proceeds owner P8; Architecture v5 slides 17, 41 and 43). This story writes no `proceeds` row, makes no posting and changes no balance; it reads the matched fact on the owner's contracts `RWB-P8-E4044-CON` and `RWB-P8-E4049-CON` and on their fakes (GAP-1891; ASM-3106);
- **the case of record stays with rwb-case (P3).** `recovery_case`, its route state and the parent `CaseWorkflow` are P3's; the route states `CASE_CLOSED` and `PROCEEDS_MATCHED` are written there and not here. This story evaluates the rule, closes the enforcement legal action, records the decision and **answers** rwb-case for the case move (GAP-1891; ASM-3106);
- **the enforcement action, the enforcement step and the LED auction ladder entry stay with rwb-litigation (S4).** `legal_action` and `hearing` are S4's tables, and Architecture v5 slide 41 gives rwb-litigation "legal actions, hearings, judgments, enforcement, LED auction ladder" (Ownership Map: legal_action and hearing owner S4);
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the legal action change, which is what legacy AC1 asked for and what legacy AC4 tested;
- **no ACE view is read here.** The legacy data table lists `v_ace_account` and `v_ace_payment`; in the target rwb-litigation holds no `v_ace_*` grant (Architecture v5 slide 29, "rwb-litigation · schema rwb_payment: no grant, refused"; slide 41 gives the ACE view contract to P1), so DP-05 applies to this story as a prohibition and the payment facts arrive on the owner's contract only (GAP-1897; ASM-3112).

The case move is not carried by an event. Architecture v5 slide 43 gives `ProceedsMatched` exactly five consumers — rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee — and rwb-litigation is not one of them, while the S4 IN row of slide 19 lists only `NoticeDelivered` and `PartnerResultSubmitted`; DP-09 is not in this story's pattern set either. The fact therefore arrives on the P8 contract synchronously, one hop with a 2 s budget, and this story publishes and consumes nothing (GAP-1892; ASM-3107). The agreement between the legacy wording and the target is exactly this: the money is matched and posted by rwb-payment (P8), and this story evaluates the rule, closes the enforcement action and answers the case move.

The metric of the feature is unchanged and is the review of the closed enforcement files, so no business value moves: the 100, 90, 80 and 70 percent ladder, the balance and costs test and the D7 approval limit are values in force in reference data and in the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S4-E5022-CON is published: the three legal-action operations, the action types `ENFORCEMENT`, `LED_AUCTION` and `CIVIL_CASE`, the match and close request and answer shapes, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- `RWB-P8-E4044-CON` "Match auction and enforcement proceeds" and `RWB-P8-E4049-CON` "Apply proceeds to the case balance" are published with their fakes, so the matched money fact and the application to the balance can be read on Day 1. Neither is in this story's contract-dependency row, which is None, and the two rows are recorded as missing C dependencies (GAP-1891; ASM-3106).
- The case-move answer of rwb-case is available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies to the case of record, and where rwb-case publishes a REST case-move operation for another caller its name is Not specified in the source documents (GAP-1891, GAP-1896; ASM-3106, ASM-3111).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the legal action change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 Litigation workspace and SCR-20 Enforcement workspace reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `legal_action` and `hearing` exist in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-029 and the standard record columns of TSD S4 T3.0; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version, with R-LIT-51, R-LIT-65 and R-LIT-70 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The rule rows of the three rules and the D7 approval of a close above the delegated limit are governed there and are not listed for this story (GAP-1895; ASM-3110).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery.v_ace_account`, `recovery.v_ace_payment` or `rwb_payment` is refused by the database and fails the boundary test (DP-05; GAP-1897; ASM-3112).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5022-CON when its tests pass.

### 4. Flow

1. rwb-payment (P8) matches the payment that came after judgment, or the auction proceeds, to the case and posts it; `proceeds` is written in `rwb_payment` and no fact of it enters `rwb_litigation` except through the owner's contract (GAP-1891; ASM-3106).
2. The money fact arrives at this service: the step of `LitigationWorkflow` on task queue `rwb-litigation` reads the match on `RWB-P8-E4044-CON` and the application on `RWB-P8-E4049-CON` with the case reference, the proceeds or payment reference, the amount, the value date and the source, LED or firm, one hop with a 2 s budget and a breaker. Where the case is an LED auction, the fact also carries the round result and the percentage of official value (GAP-1896; ASM-3111).
3. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, the status, `claim_amount` (DF-LEG-009), `judgment_date` (DF-LEG-011) and `judgment_amount` (DF-LEG-012), and the LED auction ladder entry where the action type is `LED_AUCTION`.
4. `EnforcementMatchEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates R-LIT-51, R-LIT-65 or R-LIT-70 on the fact and on the judgment facts: a payment after judgment that covers the balance and the costs, a round sold at 100, 90, 80 or 70 percent of official value, or proceeds that cover the judgment total and the costs (FSD S4 A2.22.3.1; Business Rules and Routing Logic v4).
5. The evaluation answers the rule ID, the package version, the action of the rule and the case move the rule names.
6. `EnforcementDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. `EnforcementActionWriter` patches the legal action on `PATCH /legal-actions/{legalActionId}` (API-S4-004) in one `rwb_litigation` transaction with the decision record and the idempotency row: `status` (DF-LEG-014) to `CLOSED` under R-LIT-51 and R-LIT-70, and no status change under R-LIT-65, which matches the proceeds and leaves the enforcement open until R-LIT-70. No other column of the action changes and no column is added.
8. `CaseMoveAnswer` answers rwb-case with the case move the rule names: `CASE_CLOSED` under R-LIT-51 and R-LIT-70, `PROCEEDS_MATCHED` under R-LIT-65, with the rule ID, the version, the decided-at time and the enforcement closure. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-1891; ASM-3106).
9. Under R-LIT-70 the record of the closed enforcement is retained after close: nothing is deleted, archived or moved out of `rwb_litigation`, and the retention of the case documents stays with rwb-document (P5).
10. A repeated fact with the same case, payment or proceeds reference and value date writes nothing, sends no second case-move answer and counts the repeat.
11. SCR-19 Litigation workspace and SCR-20 Enforcement workspace read the legal action, its status and its match outcome from this service through the gateway-bff composite route, read only, next to the case and the route state of rwb-case and the money of rwb-payment (DP-19).
12. Where a close falls above the delegated limit, the stage raises the D7 approval on the rwb-decision approval contract and waits; the close is written only on the approval answer (GAP-1895; ASM-3110).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the legal action keeps its status and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E5-022-04, TC-E5-022-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC2, AC3, TC-E5-022-05 |
| X3 | The legal action does not exist or is outside the scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC2, AC3 |
| X4 | The legal action is already `CLOSED` or `WITHDRAWN`, or is not the action type the rule needs | 409 and nothing changes; the match is not evaluated again on a closed action | None | AC2, AC3 |
| X5 | The P8 match or apply contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X6 | The matched amount does not satisfy the rule condition (the payment does not cover the balance and the costs, or the round did not sell at 100, 90, 80 or 70 percent) | No rule fires: nothing changes, no decision record is written and the case keeps its state | None | AC2, AC3 |
| X7 | The same fact arrives twice with the same reference and value date, or the same `Idempotency-Key` is replayed | One write and one case-move answer; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | The rule package in force is not the one the enforcement step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | A close falls above the delegated limit and no approval is answered | The step waits on the approval; the legal action is not closed and no case move is answered | None | AC2 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `proceeds` row, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 to X4 are the exception paths of RWB-E5-022 carried onto the split, X5 to X9 are the paths the target call types add, and X10 is the DP-05 and DP-01 boundary. The ladder percentages of X6 and the delegated limit of X9 are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5022-CON, the two P8 contracts and the case-move fake, on the tables of its own schema, and needs no live rwb-payment, no live rwb-case and no live rwb-decision |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the three operations and the action types are fixed |
| Valuable | An enforcement step closes on the money that is already matched and posted, in one recorded step, and the case moves in the service that owns it |
| Estimable | One workflow step, one evaluator, one record write, one action write, one case-move answer, one client and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and money facts through the contract fakes, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Match enforcement proceeds to the case

  Background:
    Given case "RC-2026-000702" carries the judgment-recorded enforcement legal action "LA-2026-000702" of action type "ENFORCEMENT" with status "ENFORCING"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-51, R-LIT-65 and R-LIT-70
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Match enforcement proceeds to the case (legacy RWB-E5-022 AC1)
    Given the rwb-payment contract mock returns the matched payment of 2026-12-09 for case "RC-2026-000702"
    Given the rwb-case contract mock returns the case state "JUDGMENT_RECORDED" for "RC-2026-000702"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then matches money from the LED or the firm to the case and applies it to the balance
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-51 (legacy RWB-E5-022 AC2)
    Given the rwb-case contract mock returns the case state "JUDGMENT_RECORDED" for "RC-2026-000702"
    Given the rwb-payment contract mock returns the matched payment of 2026-12-09 that covers the balance and the costs of case "RC-2026-000702"
    Given a case in state JUDGMENT_RECORDED
    When debtor paid after judgment
    Then match the payment, close the enforcement and close the case
    Then the case moves to CASE_CLOSED

  Scenario: AC3 Rule R-LIT-65 (legacy RWB-E5-022 AC3)
    Given the rwb-case contract mock returns the case state "LED_AUCTION" for "RC-2026-000702"
    Given the rwb-payment contract mock returns the round sold at 90 percent of official value for legal action "LA-2026-000702"
    Given a case in state LED_AUCTION
    When round sold
    Then match the proceeds to the case
    Then the case moves to PROCEEDS_MATCHED

  Scenario: AC4 Not recorded (legacy RWB-E5-022 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-022 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1 to AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-payment matches the payment or the proceeds and applies the money to the balance; this story evaluates R-LIT-51, R-LIT-65 or R-LIT-70, writes the decision record with the rule version and closes the enforcement legal action; and rwb-case writes the case move to `CASE_CLOSED` or `PROCEEDS_MATCHED`. The legacy `proceeds` write and the `v_ace_account` and `v_ace_payment` reads of the legacy data table are not reproduced anywhere in this story (GAP-1891, GAP-1897; ASM-3106, ASM-3112).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-51 | Litigation | D7 | JUDGMENT_RECORDED | DEBTOR_PAID_AFTER_JUDGMENT | a payment after judgment covers the balance and costs | Match the payment, close the enforcement and close the case | CASE_CLOSED | Case owner | ALS core and GL | None |
| R-LIT-65 | Litigation | D7 | LED_AUCTION | ROUND_SOLD | round_result = sold at 100, 90, 80 or 70 percent of official value | Match the proceeds to the case | PROCEEDS_MATCHED | Workbench | LED, ALS core | 2 working days |
| R-LIT-70 | Litigation | D7 | PROCEEDS_MATCHED | BALANCE_SATISFIED | proceeds cover the judgment total and the costs | Close the enforcement and the case, and retain the record after close | CASE_CLOSED | Case owner | ALS core and GL | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the case owner of R-LIT-51 and R-LIT-70 is the owner of the case of record, and the move to `CASE_CLOSED` is written by rwb-case on this story's answer; the `Workbench` owner of R-LIT-65 is the record this story writes on the legal action. The systems column names ALS core and GL, which are posted by rwb-payment and never by this service.

| ID | Rule | Source |
|---|---|---|
| BR1 | The enforcement legal action, the enforcement step and the LED auction ladder entry are this service's: the action type, its status and its match outcome are columns of `legal_action` in `rwb_litigation`, and no other service writes them | Architecture v5 slide 41 (rwb-litigation owns legal actions, hearings, judgments, enforcement, LED auction ladder); Ownership Map (legal_action and hearing owner S4); TSD S4 T3.1 |
| BR2 | The decision is recorded before the legal action changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-022 AC1 and AC4 |
| BR3 | The money stays with rwb-payment: this story writes no `proceeds` row, no posting, no booking and no balance change, and it reads the matched fact on `RWB-P8-E4044-CON` and `RWB-P8-E4049-CON` only | Ownership Map (proceeds owner P8); Architecture v5 slide 17 (P8 card: `Act: matchPayments`, `Act: postProceeds`); GAP-1891 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states `CASE_CLOSED` and `PROCEEDS_MATCHED` are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-1891 |
| BR5 | No ACE view and no ACE table is read or written here, and no cross-schema join is made: the payment facts arrive on the owner's contract and the judgment facts are this service's own columns | DP-05; Architecture v5 slide 29 (no grant on `rwb_payment`, no `v_ace_*` grant for rwb-litigation) and slide 41 (ACE view contract to P1) |
| BR6 | The same fact twice, or the same `Idempotency-Key` twice, writes once, answers the case move once and counts the repeat | TSD S4 T-A.2 (Idempotency-Key on the write operations); Architecture v5 slide 11 |
| BR7 | The vocabulary is closed: `LOV-LEGAL-TYPE` is NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION, LED_AUCTION; `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN; no state name and no list value is written in code | TSD S4 T3.2; BR-S4-022 (FSD S4 A2.22.3.1) |
| BR8 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or an event: the step carries case references, legal action references, codes, dates and amounts | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes (events carry IDs and facts, never personal data) |

**Where each rule lives in the target.** R-LIT-51 and R-LIT-70 are the two outcomes that close the enforcement: the evaluator tests the fact the P8 contract answers against the judgment facts of `legal_action`, the record is written, the status goes to `CLOSED`, and the case-move answer carries `CASE_CLOSED`. R-LIT-65 is the outcome that matches the proceeds and leaves the enforcement open: the status does not change, the ladder entry records the round result, and the case-move answer carries `PROCEEDS_MATCHED` for R-LIT-70 to be evaluated on the next fact. VR-S4-022-1 of the FSD tests the freshness of the ACE batch of the source and raises MSG-P1-001; this service holds no `v_ace_batch_status` read, so the check belongs to the owner of the data product and the message is carried in section 14 without a path here (GAP-1897; ASM-3112).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the status of the legal action and the state of the step.

| From (`legal_action.status`) | Event | Condition | To |
|---|---|---|---|
| ENFORCING, action type `ENFORCEMENT` | DEBTOR_PAID_AFTER_JUDGMENT under R-LIT-51 | A payment after judgment covers the balance and costs | `CLOSED`, with the case-move answer `CASE_CLOSED` |
| ENFORCING, action type `LED_AUCTION` | ROUND_SOLD under R-LIT-65 | round_result = sold at 100, 90, 80 or 70 percent of official value | `ENFORCING` unchanged, with the ladder entry recording the round result and the case-move answer `PROCEEDS_MATCHED` |
| ENFORCING, after the case is at `PROCEEDS_MATCHED` | BALANCE_SATISFIED under R-LIT-70 | Proceeds cover the judgment total and the costs | `CLOSED`, with the case-move answer `CASE_CLOSED` and the record retained |
| CLOSED or WITHDRAWN | Any of the three rules | X4 | Unchanged, refused with 409 |
| ENFORCING | A matched fact that does not satisfy the rule condition | X6 | Unchanged, no rule fires and no record is written |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The P8 match answers for a case with an open enforcement action | The package in force is loaded | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | The legal action is patched and the case-move answer is sent | The transaction commits | Waiting for the next fact |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Applying | The close is above the delegated limit | X9 | Waiting on the approval answer |

The route states `JUDGMENT_RECORDED`, `LED_AUCTION`, `PROCEEDS_MATCHED` and `CASE_CLOSED` of the legacy criteria are case route states and are read from rwb-case and asserted on its answer, not on a column of this service. The action types `ENFORCEMENT`, `LED_AUCTION` and `CIVIL_CASE` are the `LOV-LEGAL-TYPE` values of TSD S4 T3.2, and the action status values are those of `LOV-LEGAL-STATUS`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-ENFORCE, enforcement owner | Litigation CRU in the TSD S4 T6.1 matrix: the primary role of the feature, named as "Also uses" by the FSD and holding C, R and U on the legal action |
| RW-LITOFF, litigation officer | Litigation CRUA: reads the action, patches the enforcement step and reads the match outcome in scope |
| RW-LEGAL, legal counsel | Litigation RA: reads the action, its status and its match outcome; records no close |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| RW-PRODHEAD, RW-HEADLIT | Litigation RA: read, and approve through the approval path where the close is above the delegated limit |
| PT-LAWFIRM, law firm user | Litigation RU: reads its own action and records the result that produces a fact where the firm is the source, through the partner gateway |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record and the legal action, and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the enforcement owner as also-user, and both statements hold: the step runs under the service identity with no officer task on the happy path, and the enforcement owner is the primary role when a person does act, on SCR-20 and on the deferral and approval paths of the sibling stories. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the answer and of the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case-move answer |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`: `ENFORCEMENT`, `LED_AUCTION` or `CIVIL_CASE` |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Read, for the balance test of R-LIT-51 and R-LIT-70 |
| DF-LEG-011 | legal_action (S4, `rwb_litigation`) | judgment_date | Read, as the judgment fact the payment follows |
| DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_amount | Read, for the balance and costs test of R-LIT-51 and R-LIT-70 |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write, against `LOV-LEGAL-STATUS` (`CLOSED`), under R-LIT-51 and R-LIT-70 |
| DF-LEG-024 to DF-LEG-029 | hearing (S4, `rwb_litigation`) | the hearing rows | Neither read nor written by this story: the hearing calendar is the sibling stories' |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the legal action changes |
| DF-FIN-001 to DF-FIN-009 | proceeds (P8, `rwb_payment`) | id, case_id, treatment_id, payment_code, source, amount and 3 more | Read only through the P8 owner's contract and never written, joined or stored here (BR3) |
| DF-ACE-001 to DF-ACE-054 | `v_ace_account` and `v_ace_payment` (P1) | the account and payment facts | Not read: this service holds no `v_ace_*` grant, and DP-05 applies as a prohibition (BR5) |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1 and the Logical Data Model and Data Dictionary v8, and the `proceeds` row is the row the legacy story lists in its Data table, with its owner changed to P8 by the target. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, this story writes four of the existing `legal_action` columns, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). `recovery_case` (P3), `document` (P5), `decision_log_entry` (P7), `rule_row` (P7) and `proceeds` (P8) are not created, not written and not read as tables. The LED round result, the percentage of official value and the proceeds source code have no column in `legal_action` and no field list of their own in any source, so they are carried as facts of the P8 answer and marked with the placeholder (GAP-1896; ASM-3111).

**No personal data.** The rows this story writes carry identifiers, amounts, dates, list values and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind three operations whose shapes are declared by RWB-S4-E5022-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its judgment facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in, LegalAction out, carrying the match outcome (API-S4-004) | Litigation, right U, scope applied | Not applicable |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-type action, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the decision library, the P8 contract or the rule package does not answer. The operation IDs are those of TSD S4 T-A.1 and are not redefined here; API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belongs to the hearing stories of this service and is not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The match operation of `RWB-P8-E4044-CON` (operation name Not specified in the source documents (GAP-1896; ASM-3111)) | `/api/recovery/payment/v1` | P8 rwb-payment | The matched auction or enforcement proceeds of the case: the proceeds reference, the case reference, the amount, the value date, the source LED or firm and, for an auction, the round result and the percentage of official value; faked |
| The apply operation of `RWB-P8-E4049-CON` (operation name Not specified in the source documents (GAP-1896; ASM-3111)) | `/api/recovery/payment/v1` | P8 rwb-payment | The application of the proceeds to the case balance that R-LIT-51 and R-LIT-70 test; the balance and the posting are P8's and this story writes neither; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-1891; ASM-3106)) | rwb-case (P3) | P3 rwb-case | The answer that carries `CASE_CLOSED` or `PROCEEDS_MATCHED` with the rule and its version; the row and the route state are P3's, and on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The two P8 rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-1891 with ASM-3106; the case-move row carries the same gap for its operation name.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This story publishes none of them: DP-09 is not in its pattern set, it writes no outbox row, and its two outputs are the local decision record of DP-03 and the case-move answer of 12.2. The catalogue is not widened and a build that adds a fourth event to this service fails the absence test.

#### 12.4 Events consumed

None. `ProceedsMatched` is event 25 of `rwb.payment.events.v1`, produced by rwb-payment, and its consumers are rwb-case, rwb-asset, rwb-debtsale, rwb-writeoff and rwb-guarantee; rwb-litigation is not one of them, and the S4 IN row of Architecture v5 slide 19 lists only `NoticeDelivered` and `PartnerResultSubmitted` (GAP-1892; ASM-3107). The matched money therefore arrives on the P8 contract of 12.2, synchronously, and this story holds no consumer, no inbox row of its own and no subscription. The case route state it needs is answered by rwb-case on the same call pattern.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the case state answered by rwb-case, the rule package in force and the approval answer |
| `matchEnforcementOutcome` | Activity, the one enforcement-matching step of this story | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the action of the rule and the case move out, with the decision record and the legal action written in one transaction |

`matchPayments` and `postProceeds` are rwb-payment's activities on queue `rwb-payment` (Architecture v5 slide 17) and are not registered, called or redeclared here; no child workflow for the money exists in this service. The activity name is a target design choice of this story and is fixed by no source document; the trigger of the step is read as the arrival of the P8 fact for a case with an open enforcement or LED auction action, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-1893; ASM-3108).

#### 12.6 Schedules

None. The step runs from the arrival of the money fact and from the case signal the parent forwards, and owns no Temporal Schedule and no legacy Quartz job. The prescription clock, the proof window and the trace window of the journey are durable timers of the workflow and belong to the sibling stories; no Job of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The enforcement action and its LED auction ladder entry; this story writes `status` (DF-LEG-014) and the standard record columns |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated fact and the answer it holds |

Not owned and never read as a table: `recovery_case` (P3), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7), `document` (P5), `hearing` (S4, read only by the sibling stories), and every `v_ace_*` view (P1). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-payment match fake (`RWB-P8-E4044-CON`) | The matched payment of 2026-12-09 for case `RC-2026-000702`; the round sold at 90 percent of official value for action `LA-2026-000702`; a fact that does not cover the balance and costs; no answer beyond 2 s; an unreadable answer | AC1, AC2, AC3, X5, X6 |
| rwb-payment apply fake (`RWB-P8-E4049-CON`) | The proceeds applied to the balance of case `RC-2026-000702` with its posting reference; a refused apply; no answer beyond 2 s | AC1, AC2, X5 |
| rwb-case case-move fake | The case state `JUDGMENT_RECORDED`, `LED_AUCTION` and `PROCEEDS_MATCHED` of case `RC-2026-000702`; the case move `CASE_CLOSED` accepted, the move `PROCEEDS_MATCHED` accepted and a move refused because the case is not in the state the rule expects | AC1, AC2, AC3, X9 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-51, R-LIT-65 and R-LIT-70, and an approval answer for a close above the delegated limit | AC1, AC2, X8, X9 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 and SCR-20 answer for case `RC-2026-000702`, with the legal action facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the two P8 rows, the round result and the percentage of official value of the match fake, and the case-move answer are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-1896, GAP-1891; ASM-3111, ASM-3106).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The create, read and patch of the legal action on `/api/recovery/litigation/v1`; the match and apply of `RWB-P8-E4044-CON` and `RWB-P8-E4049-CON`, and the case-move answer; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity | `LitigationWorkflow` and its one enforcement-matching step on `rwb-litigation`; no Schedule and no child workflow for the money |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `enforcement`, Java package `th.co.scb.ace.workbench.recovery.litigation.enforcement`; front end `src/modules/recovery/litigation/EnforcementMatch.tsx`, the fragment SCR-19 and SCR-20 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the payment facts are the ones the rwb-payment contract answers (Architecture v5 slides 29 and 41; GAP-1897; ASM-3112). DP-03 is the transaction rule of the step: the record and the `legal_action` row commit together or not at all. DP-13 moves the base of the three operations and nothing else. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The two consumed P8 contracts are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-1891 with ASM-3106. The same applies to the case-move answer of rwb-case.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` enforcement branch | Workflow | The step of the journey that waits for the money fact, loads the package in force and reports the outcome to the parent |
| `matchEnforcementOutcome` | Activity | The one step: read the legal action, read the money fact, evaluate R-LIT-51, R-LIT-65 or R-LIT-70, write the record and the action, answer the case move |
| `EnforcementMatchEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the action types `ENFORCEMENT`, `LED_AUCTION` and `CIVIL_CASE` |
| `EnforcementDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `EnforcementActionWriter` | Repository | Writes `status` (DF-LEG-014) and the standard columns of `legal_action` in one `rwb_litigation` transaction, with the idempotency row and the optimistic lock |
| `PaymentFactClient` | Client | The match and apply calls of `RWB-P8-E4044-CON` and `RWB-P8-E4049-CON`, one hop, 2 s, breaker, and no retry of its own |
| `EnforcementController` | Controller | The three operations, the capability area and right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `CaseMoveAnswer` | Signal reporter | Answers rwb-case with the case move, the rule and the version; it reports, it never changes a case row |
| `EnforcementMatch` | React component | Shows the legal action status and the match outcome on SCR-19 and SCR-20, read only, with the refusal states |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the round result, the official value or the case move: those are facts of the request and of the answer, and storing them would copy another service's facts into this schema (GAP-1896; ASM-3111).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the ladder percentages, the balance and costs test and the D7 limit are values of the package and of reference data, not of this build (BR-S4-022).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The enforcement branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the P8 fact as its trigger (GAP-1893; ASM-3108).
2. `PaymentFactClient` against the two P8 fakes, with the 2 s budget, the breaker and the no-answer path (AC1, X5).
3. `EnforcementMatchEvaluator` over the LITIGATION package, with the three rules, the action types and the no-fire path (AC1, AC2, AC3, X6).
4. `EnforcementDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `EnforcementActionWriter` with the one transaction, the status vocabulary and the idempotency row (AC2, AC3, X7).
6. `CaseMoveAnswer` and the parent signal, with the two moves (AC2, AC3).
7. `EnforcementController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, AC2).
8. `EnforcementMatch` and the two screens through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_payment`, `rwb_case` or `rwb_decision` (X10, BR3, BR5).

**Feature flag.** `rwb.litigation.enforcement-match-v1`, read as a flag of the platform library; off means the step holds the fact and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic money fact in SIT, each of the three rules produces its record and its move, a repeated fact writes once, a forced record failure changes nothing, no `proceeds` row and no `recovery_case` row is written from this service, and SCR-19 and SCR-20 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service and its screen text, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid (X2, X4 of the contract) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or patches the legal action (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-022-1 (FSD S4 A2.22.3.1). This service holds no ACE batch status read, so the check is the owner's and the message is carried here (GAP-1897; ASM-3112) | {product} is from {date}. Today's ACE batch has not arrived. |

The six texts are the legacy wording of RWB-E5-022 section 14 and of the FSD S4 A2.22 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X5) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Pack | The pack states of the sibling stories next to the legal action of the case, read only |
| SCR-19 Litigation workspace | Instructed | The law firm instruction and the action status `ENFORCING`, read only |
| SCR-19 Litigation workspace | Filed | The filing date and the action status, read only |
| SCR-19 Litigation workspace | Hearing | The hearing dates of `hearing`, read only, owned by the sibling stories |
| SCR-19 Litigation workspace | Judgment | `judgment_date` (DF-LEG-011), `judgment_amount` (DF-LEG-012) and `claim_amount` (DF-LEG-009), and the match outcome of this story |
| SCR-20 Enforcement workspace | Requested | The enforcement step opened with its action status `ENFORCING`, read only |
| SCR-20 Enforcement workspace | Seized | The seizure and the writ of the sibling stories, read only |
| SCR-20 Enforcement workspace | Auctioned | The LED auction ladder entry with the round result and the match outcome under R-LIT-65 |
| SCR-20 Enforcement workspace | Closed | The action status `CLOSED`, the rule that closed it with its version, and the case move answered to rwb-case under R-LIT-51 or R-LIT-70 |
| SCR-20 Enforcement workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-20 Enforcement workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-20 Enforcement workspace | Stale data | The message MSG-P1-001 shown where the owner reports the stale data product of the source |

The route merges the answer of this service with rwb-case for the case and its route state and with rwb-payment for the money and the posting; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here. The two state lists are the legacy lists of RWB-E5-022 ("pack; instructed; filed; hearing; judgment" and "requested; seized; auctioned; closed") with the refusal and failure states this story adds.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-022-01 | AC1 | End to end | Match enforcement proceeds to the case |
| TC-E5-022-02 | AC2 | End to end | Rule R-LIT-51 |
| TC-E5-022-03 | AC3 | End to end | Rule R-LIT-65 |
| TC-E5-022-04 | AC4 | Component | Not recorded |
| TC-E5-022-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-022-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3, the "System" level of the sibling legacy stories) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The two P8 fakes, the case-move fake, the rule-package fake and the decision-record stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000702`, action `LA-2026-000702`, the matched payment of 2026-12-09 and the round sold at 90 percent of official value — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the ladder percentages, the balance and costs test, the D7 limit, the lists and the message texts are values and reference rows with a version; no list value, state name, percentage or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry identifiers, amounts, dates, codes and a rule version only, and the test data is synthetic.
- The money stays with rwb-payment: no `proceeds` row, no posting, no booking and no balance change is written here (BR3; DP-01).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR4).
- ACE data only through the owner's contract: no component of this story reads a `v_ace_*` view or an ACE table, and the service holds no `v_ace_*` grant (DP-05).
- No read of another service's tables and no cross-schema join: `proceeds`, `recovery_case`, `rule_row`, `decision_log_entry` and `document` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second post.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing, and the catalogue of the service is not widened (12.3, 12.4).
- The two screens are read only; SCR-20 posts nothing and its deferral and approval actions belong to the sibling stories.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-010 | Proceeds from enforcement are matched to the case and posted, which this story does on the money rwb-payment has matched and posted by evaluating the rule, closing the enforcement and answering the case move (FSD S4 requirements served; Business Requirements Program v4); the legacy story master carries no requirement ID (GAP-1894; ASM-3109) | FEAT-LIT-22 | 08 Litigate and enforce | R-LIT-51, R-LIT-65, R-LIT-70 | TC-E5-022-01, TC-E5-022-02, TC-E5-022-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-022 | The four legacy criteria word for word, the three rules, the two screens, the messages and the six test cases; the `proceeds` write and the `v_ace_*` reads of the legacy data table are retired |
| RWB-S4-E5022-CON | H: the three operations, the action types, the match and close shapes, the case-move answer and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| RWB-P8-E4044-CON and RWB-P8-E4049-CON | C in fact and not in the metadata row: the matched money fact and its application, faked (GAP-1891) |
| rwb-case (P3) and its case-move answer | The case of record and the route states `CASE_CLOSED` and `PROCEEDS_MATCHED`, answered and never written (GAP-1891) |
| RWB-S4-E5022-APP and RWB-S4-E5022-CON siblings of this key | The enforcement and LED action ownership of this service, and the contract half of the same legacy key |
| FEAT-LIT-22, SCR-19, SCR-20 | The feature and the two screens of the legacy story |
| DP-03, DP-05, DP-13, DP-19 | The decision record, the ACE prohibition, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the event platform this story adds no producer or consumer to, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-payment and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the three operations, the action types, the match and close shapes, the case-move answer, the error set and the fakes: RWB-S4-E5022-CON.
- The matching of the payment or the proceeds and the application of the money to the balance, the posting and the balance change: rwb-payment (P8), `RWB-P8-E4044-APP` and `RWB-P8-E4049-APP`. **The money is matched and posted by rwb-payment, and this story evaluates the rule, closes the enforcement action and answers the case move** (GAP-1891; ASM-3106).
- The case of record, its route state `CASE_CLOSED` or `PROCEEDS_MATCHED`, the parent `CaseWorkflow`, the case router and the case timers: rwb-case (P3).
- The creation of the legal action and its pack, the hearing calendar, the filing and the judgment: the sibling stories of this service, `RWB-S4-E5021-APP` and the pack and hearing stories of the same legacy family.
- The approval of a close above the delegated limit, the approval matrix and the D7 limit: rwb-decision (P7), its approval contract and the rule package.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-51, R-LIT-65 and R-LIT-70: rwb-decision (P7), with the embedded runtime as a service-template capability (GAP-1895; ASM-3110).
- The ACE account, payment and batch facts, the freshness stamp of the data product and the interaction ledger: rwb-source-data (P1); VR-S4-022-1 is its check and MSG-P1-001 is carried here only (GAP-1897; ASM-3112).
- The document of the closed enforcement file, its custody and its retention after close: rwb-document (P5); this story deletes and archives nothing.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

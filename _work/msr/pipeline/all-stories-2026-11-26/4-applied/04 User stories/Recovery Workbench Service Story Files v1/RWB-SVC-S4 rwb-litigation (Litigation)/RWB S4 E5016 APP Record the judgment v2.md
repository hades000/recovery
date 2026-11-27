# RWB-S4-E5016-APP Record the judgment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5016-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-016 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as the judgment step of `LitigationWorkflow` on task queue `rwb-litigation`; the judgment is recorded through `PATCH /legal-actions/{legalActionId}` on the base `/api/recovery/litigation/v1` (DP-13) and the step reads the action on `GET /legal-actions/{legalActionId}`; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the step acts (DP-03); the case move and the enforcement task are answered to rwb-case (P3), so this story writes no `recovery_case` row and no `task` row; the judgment fact named by the feature extract as a `v_ace_lawsuit` read has no grant and no ownership row in this service and is declared as a prohibition; SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19); the judgment type, the appeal window, the enforcement task and the trigger have no source specification and are declared as the working read of the assumptions (GAP-2811, GAP-2812; ASM-4651 to ASM-4657). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5016-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **enforcement owner (RW-ENFORCE)**, I want **the Workbench to write the judgment date and the judgment amount onto the legal action of the case, to record a dismissal and open the appeal window, and to open the enforcement step under one named owner**, so that **a case that has been heard reaches enforcement without a re-keyed judgment, with the date, the amount and the decision recorded against the rule version in force**.

This is the application slice of legacy RWB-E5-016. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the judgment step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-44 and R-LIT-45 on the judgment type, on the judgment date and amount and on the D7 appeal window;
- the stage states `IN_HEARING`, `JUDGMENT_RECORDED` and `JUDGMENT_DISMISSED`, reported to the case of record as a case move, and the enforcement task request that R-LIT-44 opens for the enforcement owner;
- `GET /legal-actions/{legalActionId}` (API-S4-003) and `PATCH /legal-actions/{legalActionId}` (API-S4-004) on base `/api/recovery/litigation/v1`, the second being the operation whose purpose is "record a filing, judgment or enforcement step" (TSD S4 T-A.2), under capability area "Litigation" with the rights R and U (DP-13);
- the local decision record of the judgment or the dismissal, written through RWB-PLT-E1027-CON before the step acts (DP-03);
- SCR-19 Litigation workspace in its judgment state and SCR-20 Enforcement workspace in its requested state, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the judgment element, the appeal-window element, the error set and the fakes, which are RWB-S4-E5016-CON; the judgment reading of the court through LIT and the firm, which arrives on the LIT interface and the partner portal; the case of record, its route state and the enforcement task row, which are rwb-case (P3); the authoring, testing and approval of R-LIT-44 and R-LIT-45, which are rwb-decision (P7); the traced assets, the writ, the seizure, the auction and the payment match after judgment, which are the sibling stories of this service and rwb-asset (S5) and rwb-payment (P8); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-016 gave the Workbench one step that wrote the judgment date and amount onto the case, recorded a dismissal where the judgment went against the bank, and opened the enforcement step. The functional specification keeps the objective to the same sentence ("writes the judgment date and amount onto the case and opens the enforcement step", FSD S4 A2.16) and keeps the feature metric: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today. The program keeps the requirement: REQ-S4-007, "Enforcement after judgment has one named owner from judgment to the end of enforcement" (FSD S4 Requirements served), which is exactly what AC1's "opens the enforcement step" asks for (GAP-2813; ASM-4656).

What D-RCV-60 changes is where the parts of the step live. In the monolith one process held the legal action, the case row, the task row, the decision log entry and the rule row in one `recovery` schema. In the target:

- **the judgment fact is the court's, read through LIT.** The feature extract of the thin story says the judgment is written "from the firm or the LIT lawsuit read through `v_ace_lawsuit`" (Epics 3 to 8 Specification v3). This service holds no `v_ace_*` grant and the ownership rows list two tables and no view, so the view is declared as a prohibition and the judgment reaches `legal_action` on the LIT interface (INT-09) — `judgment_date` and `judgment_amount` carry Source LIT in the TSD (DF-LEG-011, DF-LEG-012) (GAP-2812; ASM-4655);
- **the case and the enforcement task are rwb-case's.** `recovery_case` and `task` are P3's rows, and the enforcement task that R-LIT-44 opens for the enforcement owner is asked for on the case-move answer, never written here (GAP-2811; ASM-4652);
- **the rules are governed elsewhere.** R-LIT-44 and R-LIT-45 are rows of the LITIGATION route set, authored, tested and approved in rwb-decision and loaded here on the package in force; this story evaluates them and declares neither (GAP-2812; ASM-4653);
- **the decision is recorded first**, in the same transaction as the stage change and the column update, which is what legacy AC1 asked for and what legacy AC4 tested;
- **the judgment type has no column.** `legal_action` carries `judgment_date` (DF-LEG-011) and `judgment_amount` (DF-LEG-012) and the court numbers, but neither DF-LEG-001 to DF-LEG-014 nor any source gives a `judgment_type` column, a dismissal flag or an appeal-window end; those are inputs of the operation and facts of the decision record, and the action status moves to `JUDGMENT` of `LOV-LEGAL-STATUS` (GAP-2811; ASM-4651).

The last change is the one the legacy wording makes explicit: **"open the enforcement step"** and **"open the appeal window"**. `LOV-LEGAL-STATUS` has JUDGMENT, ENFORCING and CLOSED but no state that means "appeal open", and no source gives an appeal-window column, so the two are a **stage state** (`JUDGMENT_RECORDED`, `JUDGMENT_DISMISSED`) answered to the case of record plus a **durable timer** whose end value is a reference row (GAP-2811; ASM-4652). No column is added to express either.

The metric of the feature is unchanged and no business value moves: the D7 route set, the 5 working days of R-LIT-44, the appeal window end of R-LIT-45 and the state names are values in force in reference data and in the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S4-E5016-CON is published: the two operations, the judgment element, the appeal-window element, the action status vocabulary, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read and case-move answer are available with their fake, so the route state and the enforcement task request can be exercised on Day 1. Neither row is in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2812; ASM-4653).
- The rwb-decision rule-package read is available with its fake: the LITIGATION package at its version with R-LIT-44 and R-LIT-45. No source names the operation, so it is Not specified in the source documents (GAP-2812; ASM-4653).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the stage change, the column update and their record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 and SCR-20 reach this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` exists in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-014 and the standard record columns of TSD S4 T3.0; `hearing` exists for the hearing facts the judgment closes; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version with R-LIT-44 and R-LIT-45 in it. The package, its rule rows and the appeal window value are authored, tested and approved in rwb-decision and in reference data; this story declares none of them (GAP-2812; ASM-4653).
- The judgment arrives on the LIT interface (INT-09, daily end of day, COLLINS batch) and through the firm on the partner portal. This service reads no `v_ace_*` view and holds no grant on one (GAP-2812; ASM-4655).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_decision`, `rwb_reporting` or `rwb_payment` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5016-CON when its tests pass, and the story stays at status Draft until the verification loop collects the sign-offs (GAP-2814; ASM-4658).

### 4. Flow

1. The judgment arrives. Either the firm enters the outcome on the partner portal through this service's own `PATCH /legal-actions/{legalActionId}` under `PT-LAWFIRM`, or the LIT lawsuit read of the overnight chain updates the action fields of the case. Both paths end in a judgment signal of `LitigationWorkflow` on task queue `rwb-litigation`; no source names the signal and no event and no Schedule is declared (GAP-2812; ASM-4654).
2. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, `status` (DF-LEG-014), `lawsuit_no`, `black_case_no` (DF-LEG-005, DF-LEG-006), `court_name` (DF-LEG-008) and `claim_amount` (DF-LEG-009).
3. The step reads the judgment element of the request: the judgment type (a value of `full`, `partial`, `default` or `dismissed` as R-LIT-44 and R-LIT-45 name them), the judgment date, the judgment amount, the red case number where the court gives one (DF-LEG-007) and the appeal window end where the judgment went against the bank. No value is computed here and none is defaulted (GAP-2811; ASM-4651).
4. `JudgmentEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates the judgment type in the state in force: `IN_HEARING` for both rules. A judgment on a case in any other state does not fire either rule and is refused (R-LIT-44, R-LIT-45; X4).
5. `JudgmentDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the judgment type, the judgment date, the judgment amount, the inputs reference and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
6. `recordJudgment` writes the judgment onto the action inside one transaction with the record: `judgment_date` (DF-LEG-011), `judgment_amount` (DF-LEG-012), `red_case_no` (DF-LEG-007) where the court gives one, the standard record columns of TSD S4 T3.0, and `status` to `JUDGMENT` of `LOV-LEGAL-STATUS`. `filed_date`, `lawsuit_no`, `black_case_no` and `court_name` are not changed (R-LIT-44; legacy AC2).
7. On R-LIT-44 the case move `JUDGMENT_RECORDED` is answered to rwb-case together with the enforcement task request: the task code, the owner role RW-ENFORCE, the due date from the 5 working days of R-LIT-44 and the rule ID with its version. rwb-case writes the `recovery_case` row, its route state and the `task` row; this service writes none of the three (GAP-2811; ASM-4652).
8. On R-LIT-45 the dismissal is recorded instead of the judgment amount, the stage moves to `JUDGMENT_DISMISSED`, the case move is answered to rwb-case, and `armAppealWindow` arms one durable timer to the appeal window end, read as a reference value at its version. No `timer` row, no Schedule and no Quartz row is created (GAP-2811; ASM-4652).
9. The action keeps its status `JUDGMENT` on both paths and is not set to `ENFORCING`: the enforcement and the appeal are stages of the case and of `LitigationWorkflow`, and `LOV-LEGAL-STATUS` is written by the enforcement and the write-off steps of the sibling stories (TSD S4 T3.2; ASM-4651).
10. A repeated judgment with the same case, action and judgment reference writes nothing, sends no second task request, sends no second case-move answer and counts the repeat; the stored answer is returned.
11. SCR-19 shows the judgment, its date and amount and the rule version; SCR-20 shows the enforcement step as requested, under the enforcement owner, read through the gateway-bff composite route (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the action keeps its columns and status, no case move and no task request leaves the service | MSG-P7-003 | AC4, TC-E5-016-04, TC-E5-016-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | TC-E5-016-05 |
| X3 | The legal action does not exist, or it is outside the caller's scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC2, AC3 |
| X4 | The action is already `CLOSED` or `WITHDRAWN`, or the stage is not `IN_HEARING`, or a judgment is recorded twice for the same action | 409 and nothing changes; neither rule fires on a closed or already-judged action | None | AC2, AC3 |
| X5 | A required element of the judgment is absent or invalid (no judgment type, no date, a negative or non-numeric amount) | 422 and nothing is written; no rule is evaluated and no record is written | MSG-GEN-001 | AC1 |
| X6 | The case read, the case-move answer or the rule package does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC3 |
| X7 | The same judgment, the same case move or the same task request arrives twice | One write, one case-move answer and one task request; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | A component, a statement or a test reaches a `recovery_case` row, a `task` row, a `rule_row`, a `decision_log_entry` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 to X4 are the exception paths of RWB-E5-016 carried onto the split, X5 to X8 are the paths the target call types add, and X9 is the DP-01 boundary. The 5 working days of R-LIT-44, the appeal window end and the D7 route set are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5016-CON and the consumed fakes, on the tables of its own schema, and needs no live rwb-case, rwb-decision or rwb-integration |
| Negotiable | The activity names, the decision code per rule and the shape of the enforcement task request are this story's choice; the rules, the messages, the screens, the two operations and the state names are fixed |
| Valuable | A judgment reaches the action, the stage and the enforcement owner in one step with its decision recorded, instead of a re-keyed judgment and an unowned enforcement file |
| Estimable | One workflow branch, one evaluator, one record write, one action update, one case-move answer with its task request, one timer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and judgments through the contract fakes, plus the component case of the access answer and the NFR case of the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Record the judgment

  Background:
    Given case "RC-2026-000716" carries the filed civil-case legal action "LA-2026-000716" at the stage "IN_HEARING"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-44 and R-LIT-45
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record the judgment (legacy RWB-E5-016 AC1)
    Given the rwb-case contract mock returns the case state "IN_HEARING" for case "RC-2026-000716"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-44 and R-LIT-45 at its version
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then writes the judgment date and amount onto the case and opens the enforcement step
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-44 (legacy RWB-E5-016 AC2)
    Given the rwb-case contract mock returns the case state "IN_HEARING" for case "RC-2026-000716"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-44 and R-LIT-45 at its version
    Given a case in state IN_HEARING
    When judgment for the bank
    Then record the judgment date and amount and open the enforcement task
    Then the case moves to JUDGMENT_RECORDED

  Scenario: AC3 Rule R-LIT-45 (legacy RWB-E5-016 AC3)
    Given the rwb-case contract mock returns the case state "IN_HEARING" for case "RC-2026-000716"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-44 and R-LIT-45 at its version
    Given a case in state IN_HEARING
    When judgment against the bank
    Then record the dismissal and open the appeal window
    Then the case moves to JUDGMENT_DISMISSED

  Scenario: AC4 Not recorded (legacy RWB-E5-016 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-016 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the lower-case opening of the third `Then`, the legacy wording of `its trigger arrives`, `judgment for the bank`, `judgment against the bank` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 to AC3 carry the `Given the <service> contract mock returns <x>` lines above, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-case holds the case of record, its route state and the enforcement task; rwb-decision governs the two rules and their package; and this story writes the judgment onto the action, records the decision with the rule version and answers the case move. The legacy `recovery_case` and `task` writes are not reproduced here (GAP-2811; ASM-4652).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-44 | Litigation | D7 | IN_HEARING | JUDGMENT_FOR_THE_BANK | judgment_type in (full, partial, default) | Record the judgment date and amount and open the enforcement task | JUDGMENT_RECORDED | Enforcement owner | LIT, Partner Portal | 5 working days |
| R-LIT-45 | Litigation | D7 | IN_HEARING | JUDGMENT_AGAINST_THE_BANK | judgment_type = dismissed | Record the dismissal and open the appeal window | JUDGMENT_DISMISSED | Litigation officer | LIT, Partner Portal | To the appeal window end |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: "Enforcement owner" is the RW-ENFORCE task owner that the case of record assigns, and "Litigation officer" is RW-LITOFF. The systems column names LIT and the Partner Portal: the judgment is entered by the firm on the partner portal through this service's `PATCH` operation or arrives on the LIT interface, and LIT is read by the integration service of P2, never by a view of this service (GAP-2812; ASM-4655).

| ID | Rule | Source |
|---|---|---|
| BR1 | The judgment step and the legal action are this service's: the stage states `IN_HEARING`, `JUDGMENT_RECORDED` and `JUDGMENT_DISMISSED` are states of the LITIGATION machine on `LitigationWorkflow`, and the judgment facts written are columns of `legal_action` in `rwb_litigation` | FSD S4 A2.16; TSD S4 T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision is recorded before the step acts, with the rule ID and the package version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-016 AC1 and AC4 |
| BR3 | The case of record, its route state and the enforcement task stay with rwb-case: this story answers the move and requests the task, and writes no `recovery_case` row and no `task` row | Ownership Map (recovery_case and task owner P3); TSD S4 T5.2; GAP-2811 |
| BR4 | The judgment type decides the path and is never derived: `full`, `partial` and `default` take R-LIT-44, `dismissed` takes R-LIT-45, and no other value fires either rule | Business Rules and Routing Logic v4 (R-LIT-44, R-LIT-45); GAP-2811 |
| BR5 | Only `judgment_date`, `judgment_amount`, `red_case_no` and `status` are written on the action; `judgment_type`, the dismissal and the appeal window end have no column and are carried as inputs and as decision-record facts | TSD S4 T3.1 (DF-LEG-001 to DF-LEG-014); GAP-2811; ASM-4651 |
| BR6 | The action status moves to `JUDGMENT` of `LOV-LEGAL-STATUS` and never to `ENFORCING` in this step: enforcement and appeal are stages of the case and of the workflow | TSD S4 T3.2; ASM-4651 |
| BR7 | The appeal window is one durable timer of `LitigationWorkflow` armed from a reference value at its version; no `timer` row, no Temporal Schedule and no Quartz row is created | GAP-2811; ASM-4652; Template and Rules §R5.5 DP-10 held as a prohibition |
| BR8 | The same judgment, case move or task request twice writes once and counts the repeat | TSD S4 T-A.2; legacy AC1 |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case references, action references, codes, dates and amounts | Template and Rules v1 §R7.2 (s17); TSD S4 T6.2 |

**Where each rule lives in the target.** R-LIT-44 is the judgment-for-the-bank step: the judgment type is one of `full`, `partial` and `default`, the date and the amount are written onto the action, the status goes to `JUDGMENT`, the stage goes to `JUDGMENT_RECORDED` and the enforcement task is requested from rwb-case. R-LIT-45 is the dismissal step: the dismissal is recorded, the stage goes to `JUDGMENT_DISMISSED`, the case move is answered and the appeal window is armed; the appeal itself is R-LIT-46 to R-LIT-49 and belongs to RWB-S4-E5014-APP. VR-S4-016-1 of the FSD (a stale data product after a late or failed ACE batch, MSG-P1-001) is carried in section 14 and is raised by the ACE-fed reads of P1, not by a path of this story.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story does own is the stage of `LitigationWorkflow` and the state of the step.

| From (stage of `LitigationWorkflow`) | Event | Condition | To |
|---|---|---|---|
| `IN_HEARING` | JUDGMENT_FOR_THE_BANK under R-LIT-44 | judgment_type in (full, partial, default) | `JUDGMENT_RECORDED`, with the case-move answer `JUDGMENT_RECORDED` and the enforcement task requested |
| `IN_HEARING` | JUDGMENT_AGAINST_THE_BANK under R-LIT-45 | judgment_type = dismissed | `JUDGMENT_DISMISSED`, with the case-move answer `JUDGMENT_DISMISSED` and the appeal window armed |
| `HEARING_ADJOURNED` | Either judgment event | R-LIT-34 and R-LIT-35 have not returned the case to `IN_HEARING` | Unchanged, refused with 409 (X4) |
| Any other stage | Either judgment event | The stage is not the one the rule expects | Unchanged, refused with 409 (X4) |
| Any | A judgment on an action that is `CLOSED` or `WITHDRAWN` | X4 | Unchanged, refused with 409 |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A judgment signal arrives for a case at `IN_HEARING` | The package in force is loaded | Evaluating |
| Evaluating | R-LIT-44 or R-LIT-45 fires | The judgment element is valid and the decision record is written | Applying |
| Applying | The action columns, the stage move and the case-move answer commit | The transaction commits | Waiting for the next signal |
| Applying | The record write, the action update or the move fails | X1, X6 | Waiting, nothing changed |
| Applying | A judgment element is absent or invalid | X5 | Waiting, refused with 422 and nothing changed |

The action status is `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED` or `WITHDRAWN` (TSD S4 T3.2). The filed action moves to `JUDGMENT` on both paths, whether the judgment is for the bank or against it, because `LOV-LEGAL-STATUS` has no dismissed value; the dismissal is a state of the stage and a fact of the decision record. `ENFORCING` belongs to R-LIT-54 and the writ step, which is a sibling story, and `CLOSED` belongs to R-LIT-51 and R-LIT-70, which are rwb-payment and rwb-writeoff's (BR6; GAP-2811; ASM-4651).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix: records the filing facts, reads the action and works the judgment step on SCR-19; the owner of R-LIT-45 |
| RW-ENFORCE, enforcement owner | Litigation CRU: the "also uses" role of the FSD and the owner of R-LIT-44; reads the judgment and works the enforcement step on SCR-20 |
| PT-LAWFIRM, law firm user | Litigation RU: enters the judgment, its date, its amount and the court numbers on the partner portal through the `PATCH` operation, scoped to its own cases |
| RW-LEGAL, Head of Litigation (RW-HEADLIT), product head (RW-PRODHEAD) | Litigation RA or R as the T6.1 matrix gives it: read and approve; no judgment is recorded by this step on their right |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| SY-DATALOAD, SY-CASEWF, SY-RULES, SY-AGENT | Litigation U or R as the T6.1 matrix gives it: the LIT load and the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the two rules, writes the decision record and the action columns, holds the stage and answers the case move; it holds no grant on another schema |

The rights above are the rows of TSD S4 T6.1 and the legacy permission table of this key: Litigation `U` for RW-LITOFF, RW-ENFORCE, PT-LAWFIRM and SY-DATALOAD, Litigation `C` for RW-LITOFF and RW-ENFORCE, and the read row of 23 roles and more for `R`. The FSD S4 A2.16.3.3 states that the step "runs unattended" with the enforcement owner as also-user, while the legacy story names an enforcement owner who records the judgment; both statements hold because the judgment arrives from the firm and from LIT and the officer or the firm confirms it, so no person is required for the step to run and none is excluded from it (GAP-2812; ASM-4654). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the record and of the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case-move answer and the task request |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`: the judged action of this step is `CIVIL_CASE` |
| DF-LEG-005, DF-LEG-006, DF-LEG-008 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no, court_name | Read, as the court facts the judgment is recorded against; not changed |
| DF-LEG-007 | legal_action (S4, `rwb_litigation`) | red_case_no | Write where the court gives one at judgment |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Read, as the amount sued for that the judgment amount is measured against |
| DF-LEG-011, DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_date, judgment_amount | Write, from the judgment element of the request; Source LIT of the TSD |
| DF-LEG-013 | legal_action (S4, `rwb_litigation`) | lit_status | Read only: the court status text arrives on the LIT interface and is not written by this step |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write to `JUDGMENT` of `LOV-LEGAL-STATUS`; never to `ENFORCING` here (BR6) |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by` | Write through the repository on the update; `version` is the optimistic lock of the step |
| DF-LEG-024 to DF-LEG-029 | hearing (S4, `rwb_litigation`) | hearing_date, hearing_type, outcome, next_date | Read, as the hearing the judgment closes; the `JUDGMENT_READING` type and the `JUDGMENT` outcome are values of `LOV-HEARING` and `LOV-HEARING-OUTCOME` |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the route state comes back on the case-move answer (BR3) |
| DF-WRK-017 to DF-WRK-026 | task (P3, `rwb_case`) | id, case_id, task_code, element_type, discretion, status and 4 more | Not written: the enforcement task is requested on the case-move answer and P3 creates it (BR3) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the action changes (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule package in force and never as a table |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1, the legacy story Data table and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). The `judgment_type`, the dismissal and the appeal window end have no column and are not given one (BR5). The test fixtures are synthetic: case `RC-2026-000716`, action `LA-2026-000716`, a judgment for the bank and a judgment against it.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S4-E5016-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in with the judgment element, LegalAction of status 200 out (API-S4-004) | Litigation, right U, scope applied | Not applicable |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts, its judgment and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The step reads the action on the GET and writes the judgment on the PATCH, whose documented purpose is "record a filing, judgment or enforcement step" (TSD S4 T-A.2). Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-stage action, 422 with MSG-GEN-001 for a missing or invalid judgment element, and 503 when the decision library, a consumed contract or the rule package does not answer. `POST /cases/{caseId}/legal-actions` (API-S4-002), `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) belong to the sibling stories of this service and are not declared by this story.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2812; ASM-4653)) | rwb-case (P3) | P3 rwb-case | The route state of the case, which must be the one R-LIT-44 and R-LIT-45 expect; faked |
| The case-move answer and the enforcement task request (operation name Not specified in the source documents (GAP-2812; ASM-4653)) | rwb-case (P3) | P3 rwb-case | The moves `JUDGMENT_RECORDED` and `JUDGMENT_DISMISSED` and the task request of R-LIT-44 for the enforcement owner; the row and the route state are P3's, and on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule package in force (operation name Not specified in the source documents (GAP-2812; ASM-4653)) | rwb-decision (P7) | P7 rwb-decision | The LITIGATION package at its version with R-LIT-44 and R-LIT-45; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All three are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2812 with ASM-4653.

#### 12.3 Events published

None. The service's topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its ownership rows list no event of this service (context pack, ownership rows). DP-09 is not in this story's pattern set: the step writes no outbox row, its outputs are the local decision record of DP-03, the case-move answer and the task request. The judgment is a fact of this service and of the case of record, and reporting reads it from the event of its owner on the reporting contract, not from this topic.

#### 12.4 Events consumed

None. The ownership rows of this service list no consumed event either, so the judgment arrives as a signal of `LitigationWorkflow` and the case and the package arrive on their owners' contracts of 12.2 (GAP-2812; ASM-4654). This story holds no consumer group, no subscription and no inbox of its own, and a build that adds a consumer to `rwb.litigation.events.v1` or a subscription to another topic fails the absence test of the CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the judgment, the rule package in force and the timer fire; outcome: the stage move for the parent |
| `recordJudgment` | Activity, the judgment-for-the-bank step of this story | `rwb-litigation` | The judgment element in; the rule ID with its package version, the action columns, the decision record and the case move with the task request out, in one transaction |
| `armAppealWindow` | Activity, the dismissal step of this story | `rwb-litigation` | The dismissal and the appeal window end in; the dismissal fact, the decision record, the case move and one durable timer out |

The activity names are target design choices and are fixed by no source document; the trigger of the step is read as a judgment signal, because the legacy story says the judgment is recorded while the FSD says the step runs unattended and the firm enters it on the partner portal (GAP-2812; ASM-4654, ASM-4657). No cross-service call is made inside a workflow: each is an activity of the queue above.

#### 12.6 Schedules

None. The step runs from the judgment signal and from the LIT interface's arrival. The appeal window of R-LIT-45 is a durable timer of the workflow, not a Schedule and not the `timer` row of rwb-case; this story registers no Temporal Schedule, no Quartz row and no shared job table, and no Job of the batch catalogue is owned or moved here (GAP-2811; ASM-4652).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read and updated: `judgment_date`, `judgment_amount`, `red_case_no` and `status` are written (BR5) |
| hearing | S4 (`rwb_litigation`) | Read only, as the hearing the judgment closes; no hearing row is written here |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the judgment or the dismissal (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated judgment and the answer it holds |

Not owned and never read as a table: `recovery_case` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `treatment` (S2), `document` (P5) and the payment rows (P8). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read fake | The route state `IN_HEARING` of case `RC-2026-000716`, another state, and no answer beyond 2 s | AC1, AC2, AC3, X4 |
| rwb-case case-move fake | The moves `JUDGMENT_RECORDED` and `JUDGMENT_DISMISSED` accepted with the enforcement task created for the enforcement owner, and a move refused because the case is not in the state the rule expects | AC1, AC2, AC3, X7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-44 and R-LIT-45, and a second version | AC1, AC2, AC3, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 answer in the judgment state and the SCR-20 answer in the requested state for case `RC-2026-000716` | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT. The three consumed rows carry the placeholder of 12.2 until their owners publish an operation name (GAP-2812; ASM-4653).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The action read and the action update on `/api/recovery/litigation/v1`; the case read, the case move with the task request and the rule package; one hop, 2 s each |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 2 activities, 1 durable timer | `LitigationWorkflow` with `recordJudgment` and `armAppealWindow` on `rwb-litigation`, and the appeal window; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `judgment`, Java package `th.co.scb.ace.workbench.recovery.litigation.judgment`; front end `src/modules/recovery/litigation/RecordJudgment.tsx`, the fragment SCR-19 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the action columns and the stage change commit together or not at all, and the record is written before the case move leaves the service. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway. DP-05 is held as a prohibition because the service holds no `v_ace_*` grant, DP-09 and DP-10 because no event and no Schedule is declared, and DP-04 because the two rules are read from the package of P7 and evaluated by the embedded runtime of the service template (GAP-2812; ASM-4655).

**Dependencies the tables add and the plan does not hold.** The three H rows are the plan's. The three consumed contracts of 12.2 are class C dependencies in fact and are not in the metadata row, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2812 with ASM-4653.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` judgment branch | Workflow | The step that waits for the judgment, loads the package in force, arms the appeal window and reports the stage move to the parent |
| `recordJudgment` | Activity | Reads the action and the judgment element, evaluates R-LIT-44, writes the record and the columns and answers the move to `JUDGMENT_RECORDED` with the task request |
| `armAppealWindow` | Activity | Evaluates R-LIT-45, records the dismissal and the move to `JUDGMENT_DISMISSED`, and arms one durable timer |
| `JudgmentEvaluator` | Service | The evaluation of the judgment type against the LITIGATION package version in force, with the state names of the LITIGATION machine |
| `JudgmentDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `LegalActionRepository` | Repository | Reads the action and writes the four columns of BR5 with the optimistic lock, on `rwb_litigation` only |
| `CaseMoveAnswer` and `EnforcementTaskRequest` | Signal reporter | Answer rwb-case with the move, the rule, the version and the task request; they report, they never change a case row |
| `JudgmentController` | Controller | The two operations, the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RecordJudgment` | React component | Shows the judgment, its date and amount, the rule and its version, and the enforcement step as requested on SCR-19 and SCR-20, read only |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the judgment type, the dismissal or the appeal window (BR5; GAP-2811; ASM-4651).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE`, `LOV-LEGAL-STATUS`, `LOV-HEARING` and `LOV-HEARING-OUTCOME` at their version in force (TSD S4 T3.2), read as reference data and never as constants; no dismissed or appeal value is added to the status list.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the 5 working days of R-LIT-44 and the appeal window end of R-LIT-45 are values of the package and of reference data, not of this build (GAP-2811; ASM-4653).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The judgment branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the judgment signal as its trigger (ASM-4654).
2. `LegalActionRepository` over `legal_action` and `hearing`, with the four written columns and the optimistic lock (AC2, AC3).
3. `JudgmentEvaluator` over the LITIGATION package, with R-LIT-44, R-LIT-45, the four judgment types and the no-fire path (AC2, AC3, X4).
4. `JudgmentDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `CaseMoveAnswer` and `EnforcementTaskRequest` with the two moves and the task request (AC2, AC3, X7).
6. `armAppealWindow` and the durable timer, with the window end read as a reference value (AC3).
7. `JudgmentController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, X2, X3, X5).
8. `RecordJudgment` and the two workspaces through the composite route fake (AC1, AC2).
9. The boundary test: no statement outside `rwb_litigation`, no write to `rwb_case`, `rwb_decision` or `rwb_reporting` (X9, BR3, BR5).

**Feature flag.** `rwb.litigation.record-judgment-v1`, read as a flag of the platform library; off means the step holds the judgment signal, writes no column and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic judgment in SIT, R-LIT-44 writes the date and the amount and requests the enforcement task, R-LIT-45 records the dismissal and arms the appeal window, a repeated judgment writes once, a forced record failure changes nothing, no `recovery_case` row and no `task` row is written from this service, and SCR-19 and SCR-20 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription story of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required element of the judgment is absent or invalid (X5) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or records the judgment (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the action changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | VR-S4-016-1: a data product of the ACE-fed read is stale after a late or failed batch; the check belongs to P1 and this step reads the action of its own schema | {product} is from {date}. Today's ACE batch has not arrived. |

The five legacy texts are the legacy wording of RWB-E5-016 section 14 and of the FSD S4 A2.16 message list, copied unchanged; no message is reworded and no new message is added. `MSG-P1-001` is the FSD validation rule of the feature and is raised by the owner of the read, not here. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X6) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No new screen is built in this story. Two existing surfaces show what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed; hearing | The pack, the instruction and the hearing of the sibling stories, read only, and the action at `IN_HEARING` |
| SCR-19 Litigation workspace | Judgment | The judgment date, the judgment amount, the red case number where the court gives one, the rule R-LIT-44 or R-LIT-45 with its version, and the action at `JUDGMENT` |
| SCR-19 Litigation workspace | Dismissed | The dismissal, the appeal window end and the return to the appeal step of the sibling story, read only |
| SCR-20 Enforcement workspace | Requested | The enforcement step opened by R-LIT-44, its owner RW-ENFORCE and the stage `JUDGMENT_RECORDED` |
| SCR-20 Enforcement workspace | Seized; auctioned; closed | The later enforcement states of the sibling stories, read only; this story writes none of them |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |

The route merges this service's answer with rwb-case for the case and its route state and its task; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-016-01 | AC1 | End to end | Record the judgment |
| TC-E5-016-02 | AC2 | End to end | Rule R-LIT-44 |
| TC-E5-016-03 | AC3 | End to end | Rule R-LIT-45 |
| TC-E5-016-04 | AC4 | Component | Not recorded |
| TC-E5-016-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-016-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3, the "System" level of the sibling legacy stories) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The case, package and route fakes of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000716`, action `LA-2026-000716` at `IN_HEARING`, a judgment for the bank and a judgment against it — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the 5 working days, the appeal window end, the judgment type values, the lists and the message texts are values and reference rows with a version; no list value, state name, day count or date appears in Java.
- No personal data in logs, workflow inputs, prompts or the fixture: the rows carry case references, action references, codes, dates and amounts only, and the test data is synthetic.
- The case stays with rwb-case: no `recovery_case` row, no route state and no `task` row is written here, and the move and the task are requested with the rule and its version (BR3).
- Only the four columns of BR5 are written on the action, and no dismissed or appeal value is added to a list to express a state that is a stage.
- ACE data only through its owner: no component of this story reads a `v_ace_*` view or an ACE table, and the `v_ace_lawsuit` read of the feature extract is held as a prohibition (GAP-2812; ASM-4655).
- No read of another service's tables and no cross-schema join: `recovery_case`, `task`, `rule_row`, `decision_log_entry`, `treatment` and `document` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second judgment.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing (12.3, 12.4).
- SCR-19 and SCR-20 are read only; the judgment is posted through the service, and the firm's entry on the partner portal uses the same operation under `PT-LAWFIRM`.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement, which this story does by recording the judgment and opening the enforcement task for RW-ENFORCE (FSD S4 Requirements served) | FEAT-LIT-16 | 08 Litigate and enforce | R-LIT-44, R-LIT-45 | TC-E5-016-01, TC-E5-016-02, TC-E5-016-03 |

The legacy story master of RWB-E5-016 carries no requirement ID and the plan's requirement list for this slice is empty; the trace is the requirement the FSD S4 serves for enforcement after judgment, which is the outcome of the judgment step (GAP-2813; ASM-4656).

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-016 | The four legacy criteria word for word, the two rules, the two screens, the messages and the six test cases; the `recovery_case` and `task` writes of the legacy data table are P3's |
| RWB-S4-E5016-CON | H: the two operations, the judgment and appeal-window elements, the error set and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| rwb-case (P3) and rwb-decision (P7) contracts | C in fact and not in the metadata row: the case read, the case move with the task request and the rule package, faked (GAP-2812) |
| FEAT-LIT-16, FEAT-LIT-11, SCR-19, SCR-20 | The feature, its hearing prerequisite and the two screens of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Temporal layer with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the two operations, the judgment and appeal-window elements, the error set and the fakes: RWB-S4-E5016-CON.
- The case of record, its route state, the parent `CaseWorkflow` and the enforcement task row: rwb-case (P3), which creates the task on this story's request (GAP-2811; ASM-4652).
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-44 and R-LIT-45, and the appeal window value: rwb-decision (P7) and the reference-data owner (GAP-2811; ASM-4653).
- The LIT lawsuit read and the ACE views: rwb-integration (P2) and rwb-source-data (P1); this service holds no `v_ace_*` grant (GAP-2812; ASM-4655).
- The hearing scheduling and the adjournment before judgment (R-LIT-33 to R-LIT-35): RWB-S4-E5011-APP.
- The appeal after a dismissal (R-LIT-46 to R-LIT-49): RWB-S4-E5014-APP.
- The traced assets (R-LIT-50, R-LIT-52), the writ and seizure (R-LIT-54), the auction and the payment match (R-LIT-51, R-LIT-70): the enforcement stories of this service, rwb-asset (S5) and rwb-payment (P8).
- The enforcement deferral and the write-off routing: RWB-S4-E5020-APP and rwb-writeoff (S7).
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access (P4) and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

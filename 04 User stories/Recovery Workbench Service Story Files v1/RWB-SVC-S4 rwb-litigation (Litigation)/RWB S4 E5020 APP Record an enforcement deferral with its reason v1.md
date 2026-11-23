# RWB-S4-E5020-APP Record an enforcement deferral with its reason

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5020-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-U |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5020-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-020 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as the enforcement-deferral step of `LitigationWorkflow` on task queue `rwb-litigation`; the deferral is recorded through `PATCH /legal-actions/{legalActionId}` on base `/api/recovery/litigation/v1` (DP-13) and reads the action on `GET /legal-actions/{legalActionId}`; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the step acts (DP-03); the queue, the assignment and the task rows of the legacy data table are rwb-case's (P3) and the re-queue on the review date is a durable timer of the workflow, not the monolith scheduler; SCR-20 reads through the gateway-bff composite route (DP-19); the reason code list, the review date, the re-queue schedule and the `R-LIT-44` overlap with RWB-E5-016 have no source specification and are declared as the working read of the assumptions (GAP-2828, GAP-2830, GAP-2831; ASM-4681, ASM-4683, ASM-4684). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **enforcement owner (RW-ENFORCE)**, I want **the Workbench to let the enforcement owner defer the enforcement decision with a coded reason and a review date, to record the reason and the date against the rule version in force, and to bring the case back to the enforcement decision on that date**, so that **enforcement after judgment has one named owner from judgment to the end of enforcement, and no case waits on a spreadsheet or on an unowned file**.

This is the application slice of legacy RWB-E5-020. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the enforcement-deferral step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-55 on the deferral reason and the review date, and of R-LIT-44 as the legacy criterion carries it;
- the stage states `ENFORCEMENT_DECISION` and `DEFERRAL_RECORDED`, reported to the case of record as a case move, and the durable timer that brings the case back on the review date;
- `PATCH /legal-actions/{legalActionId}` (API-S4-004) and `GET /legal-actions/{legalActionId}` (API-S4-003) on base `/api/recovery/litigation/v1`, under capability area "Litigation" with the rights U and R (DP-13);
- the local decision record of the deferral, written through RWB-PLT-E1027-CON before the step acts (DP-03);
- SCR-20 Enforcement workspace in its enforcement-decision and deferred reading, through the gateway-bff composite route (DP-19).

It does not own: the published shape of the operations, the deferral element, the review-date element, the error set and the fakes, which are RWB-S4-E5020-CON; the case of record, its stage state, the queue, the assignment, the task row and the re-queue, which are rwb-case (P3); the authoring and approval of R-LIT-55 and R-LIT-44, which are rwb-decision (P7); the judgment write itself, which is RWB-S4-E5016-APP; the asset trace, the writ, the seizure and the auction, which are the sibling stories of this service and rwb-asset (S5); the return on the review date under R-LIT-56 and the routing to write-off under R-LIT-57 as separate behaviours; and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-020 gave the Workbench one step in which the enforcement owner deferred the enforcement decision with a reason and a review date. The functional specification keeps the objective and the problem to the same words ("lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today", FSD S4 A2.20) and keeps the feature metric: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today. The requirement the feature serves is REQ-S4-007, "Enforcement after judgment has one named owner from judgment to the end of enforcement" (FSD S4 Requirements served), which is the sentence AC1's problem statement repeats (GAP-2833; ASM-4686).

What D-RCV-60 changes is where the parts of the step live:

- **the deferral is a state and a decision, not a column.** `legal_action` carries DF-LEG-001 to DF-LEG-014 and no deferral column, `LOV-LEGAL-STATUS` has no deferred value, and no source gives a code list for the reason or a field list for the review date. The reason and the date are inputs of the operation and facts of the decision record, and the deferral is a stage state of `LitigationWorkflow` (GAP-2828; ASM-4681);
- **the queue, the assignment and the task are rwb-case's.** The legacy data table lists `recovery_case`, `queue`, `assignment`, `task`, `decision_log_entry` and `rule_row`; three of those are P3's rows and two are P7's, so this story answers a case move and requests the queue placement, it writes no case row, no queue row, no assignment row and no task row (BR3);
- **the re-queue on the review date is a durable timer.** The monolith used the Workbench scheduler; the target has no job table, the ownership rows list no Job for this service, DP-10 is not in the pattern set of this key, and the review date is one durable timer of `LitigationWorkflow` that answers the case move when it fires (GAP-2831; ASM-4684);
- **the rules are governed elsewhere.** R-LIT-55 and R-LIT-44 are rows of the LITIGATION route set, authored, tested and approved in rwb-decision and loaded here on the package in force; this story evaluates them and declares neither;
- **the decision is recorded first**, in the same transaction as the stage change, which is what legacy AC1 asked for and legacy AC4 tested;
- **the judgment of AC3 is built once.** `judgment_date` and `judgment_amount` and the stage move of R-LIT-44 are the deliverable of RWB-S4-E5016-APP on the same action and the same base. Legacy E5-020 repeats the criterion, so AC3 is owned here word for word and proved here as a regression against the same published contract; no second judgment path and no second write is built (GAP-2830; ASM-4683).

No business value moves: the D7 route set, the deferral stage names, the review date and the message texts are values in reference data and in the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S4-E5020-CON is published: the two operations, the deferral element, the review-date element, the stage vocabulary, the error set and the fakes are baselined and handed to this story.
- The rwb-case case read and case-move answer are available with their fake, so the stage state, the queue placement and the task request can be exercised on Day 1. Neither row is in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2829; ASM-4682).
- The rwb-decision rule-package read is available with its fake: the LITIGATION package at its version with R-LIT-55 and R-LIT-44. No source names the operation (GAP-2829; ASM-4682).
- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the stage change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-20 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` and `hearing` exist in schema `rwb_litigation` from the DB story of this service; this story adds no table, no column and no migration.
- The enforcement action of the case is at `ENFORCEMENT_DECISION` when the deferral is taken, and the deferral reason and the review date are supplied on the request. The reason list, the date rule and the default review date are Not specified in the source documents (GAP-2828; ASM-4681).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema, so a statement on `rwb_case`, `rwb_decision` or `rwb_reporting` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the story stays at status Draft until the verification loop collects the sign-offs (GAP-2829; ASM-4682).

### 4. Flow

1. The step starts on the enforcement-decision signal of `LitigationWorkflow`: the case has reached `ENFORCEMENT_DECISION` after the asset trace of the sibling story returned no asset (R-LIT-53) or after the review date of an earlier deferral fired. No source names the signal and no event and no Schedule is declared (GAP-2829; ASM-4682).
2. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): `action_type` of `LOV-LEGAL-TYPE`, which is `ENFORCEMENT` for this step, `status` (DF-LEG-014), `case_id` (DF-LEG-002) and the court facts.
3. The step reads the deferral element of the request: the coded reason (`deferral_reason`) and the review date (`deferral_review_date`). Both are required by R-LIT-55; neither is defaulted, computed or read from a list of this service (GAP-2828; ASM-4681).
4. `DeferralEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates R-LIT-55 in the state in force: the stage must be `ENFORCEMENT_DECISION` and both elements must be present. A deferral on a case in any other stage does not fire the rule and is refused (R-LIT-55; X4).
5. `DeferralDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the deferral reason, the review date, the inputs reference and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
6. `recordEnforcementDeferral` commits the record, the stage move and the case-move answer in one transaction: the stage goes to `DEFERRAL_RECORDED`, and the answer to rwb-case carries the move, the rule ID, the package version and the queue placement request for the review date. No column of `legal_action` changes and the status is left as it stands (GAP-2828; ASM-4681).
7. `armReviewDate` arms one durable timer to the review date. When it fires, the workflow answers the case move back to `ENFORCEMENT_DECISION` under R-LIT-56, which returns the case to the enforcement decision; the timer is a workflow timer, not a Schedule and not the monolith scheduler (GAP-2831; ASM-4684).
8. On a judgment for the bank (R-LIT-44, the criterion legacy AC3 carries), the judgment date and amount are written onto the action, the enforcement task is requested and the case moves to `JUDGMENT_RECORDED`; that path is the behaviour of RWB-S4-E5016-APP on the same contract and is re-proved here, not rebuilt (GAP-2830; ASM-4683).
9. A repeated deferral with the same case, action and review date writes nothing, sends no second move and no second queue request, and counts the repeat; the stored answer is returned.
10. SCR-20 shows the enforcement decision, the deferral with its reason and its review date and the rule version, read through the gateway-bff composite route (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the stage, the case and the queue are unchanged | MSG-P7-003 | AC4, TC-E5-020-04, TC-E5-020-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E5-020-05 |
| X3 | The legal action does not exist, or it is outside the caller's scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC1, AC2 |
| X4 | The stage is not `ENFORCEMENT_DECISION`, or the action is closed or withdrawn | 409 and nothing changes; R-LIT-55 does not fire | None | AC2 |
| X5 | The reason or the review date is absent, or the review date is not in the future | 422 and nothing is written; no rule is evaluated and no record is written | MSG-GEN-001 | AC1, AC2 |
| X6 | The case read, the case answer or the rule package does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X7 | The same deferral, move or queue request arrives twice | One record, one move answer and one queue request; the repeat is counted | None | AC1 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | A component, a statement or a test reaches a `recovery_case`, `queue`, `assignment` or `task` row, a `rule_row`, a `decision_log_entry` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 to X4 are the exception paths of RWB-E5-020 carried onto the split, X5 to X8 are the paths the target call types add, and X9 is the DP-01 boundary. The review date, the reason list and the D7 route set are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5020-CON and the consumed fakes, on the tables of its own schema, and needs no live rwb-case or rwb-decision |
| Negotiable | The activity names, the decision code of R-LIT-55 and the shape of the queue request are this story's choice; the rules, the messages, the screen, the two operations and the stage names are fixed |
| Valuable | A deferral carries a reason and a date, reaches the case of record and the queue, and returns on its own date, instead of an unowned enforcement file |
| Estimable | One workflow branch, one evaluator, one record write, one case-move answer with the queue request, one timer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and deferrals through the contract fakes, plus the component case of the access answer and the NFR case of the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Record an enforcement deferral with its reason

  Background:
    Given case "RC-2026-000820" carries the enforcement legal action "LA-2026-000820"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-55 and R-LIT-44
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Record an enforcement deferral with its reason (legacy RWB-E5-020 AC1)
    Given the rwb-case contract mock returns the case state "ENFORCEMENT_DECISION" for case "RC-2026-000820"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-55 and R-LIT-44 at its version
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the enforcement owner defer with a coded reason and a review date. Enforcement after judgment has no owner today
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-55 (legacy RWB-E5-020 AC2)
    Given the rwb-case contract mock returns the case state "ENFORCEMENT_DECISION" for case "RC-2026-000820"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-55 and R-LIT-44 at its version
    Given a case in state ENFORCEMENT_DECISION
    When defer recorded
    Then record the deferral and re-queue the case on the review date
    Then the case moves to DEFERRAL_RECORDED

  Scenario: AC3 Rule R-LIT-44 (legacy RWB-E5-020 AC3)
    Given the rwb-case contract mock returns the case state "IN_HEARING" for case "RC-2026-000820"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-55 and R-LIT-44 at its version
    Given a case in state IN_HEARING
    When judgment for the bank
    Then record the judgment date and amount and open the enforcement task
    Then the case moves to JUDGMENT_RECORDED

  Scenario: AC4 Not recorded (legacy RWB-E5-020 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-020 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the lower-case opening of the third `Then` of AC1, the legacy wording of `the user acts on the screen`, `defer recorded` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 to AC3 carry the `Given the <service> contract mock returns <x>` lines above, and those added `Given` lines are the only additions to the legacy text. AC3 is the criterion legacy E5-020 shares with RWB-E5-016; the judgment path behind it is built once, by RWB-S4-E5016-APP, and is proved here as a regression on the same contract, not rebuilt (GAP-2830; ASM-4683).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-55 | Litigation | D7 | ENFORCEMENT_DECISION | DEFER_RECORDED | deferral_reason and deferral_review_date are both present | Record the deferral and re-queue the case on the review date | DEFERRAL_RECORDED | Enforcement owner | Workbench, Workbench scheduler | To the review date |
| R-LIT-44 | Litigation | D7 | IN_HEARING | JUDGMENT_FOR_THE_BANK | judgment_type in (full, partial, default) | Record the judgment date and amount and open the enforcement task | JUDGMENT_RECORDED | Enforcement owner | LIT, Partner Portal | 5 working days |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character, and they are the two rules of FSD S4 A2.20.3.1. Their owner column is a role of the business and not a service: "Enforcement owner" is the RW-ENFORCE task owner that the case of record assigns. The systems column names the Workbench and the Workbench scheduler: the first is this service and the screen, and the second is read here as the durable timer of `LitigationWorkflow`, because the target has no scheduler row for this service (GAP-2831; ASM-4684).

| ID | Rule | Source |
|---|---|---|
| BR1 | The enforcement deferral and the legal action are this service's: `ENFORCEMENT_DECISION` and `DEFERRAL_RECORDED` are states of the LITIGATION machine on `LitigationWorkflow`, and the action is the row of `rwb_litigation` the step reads | FSD S4 A2.20; TSD S4 T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision is recorded before the step acts, with the rule ID and the package version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S4 T2; legacy RWB-E5-020 AC1 and AC4 |
| BR3 | The case of record, its stage state, the queue, the assignment and the task stay with rwb-case: this story answers the move and requests the queue placement, and writes none of those rows | Ownership Map (recovery_case, queue, assignment and task owner P3); TSD S4 T5.2; GAP-2829 |
| BR4 | The deferral exists only when both the coded reason and the review date are present; no default reason, no default date and no derived date is applied here | Business Rules and Routing Logic v4 R-LIT-55; GAP-2828 |
| BR5 | `deferral_reason` and `deferral_review_date` have no column and no list value of this service: they are inputs of the operation and facts of the decision record, and no column is added for them | TSD S4 T3.1 (DF-LEG-001 to DF-LEG-014); GAP-2828; ASM-4681 |
| BR6 | No business column of `legal_action` is changed by the deferral: the action keeps its status and its court facts, and the deferral is carried by the stage and the record | TSD S4 T3.1, T3.2; ASM-4681 |
| BR7 | The re-queue on the review date is one durable timer of `LitigationWorkflow`; no Temporal Schedule, no Quartz row, no `timer` row and no shared job table is created | GAP-2831; ASM-4684; Template and Rules §R5.5 DP-10 held as a prohibition |
| BR8 | The same deferral, case move or queue request twice writes once and counts the repeat | TSD S4 T-A.2; legacy AC1 |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case references, action references, codes, dates and amounts | Template and Rules v1 §R7.2 (s17); TSD S4 T6.2 |

**Where each rule lives in the target.** R-LIT-55 is the deferral: the reason and the review date are read from the request, the record is written, the stage moves to `DEFERRAL_RECORDED`, the move is answered to rwb-case with the queue placement, and one timer is armed to the review date. R-LIT-44 is the judgment-for-the-bank step: it is owned and built by RWB-S4-E5016-APP, and this story keeps the criterion and the regression only (GAP-2830; ASM-4683). R-LIT-51 (the payment match and the close) is the payment story of this service and rwb-payment's, and R-LIT-56 with R-LIT-57 are the return and the second-deferral routing, neither of which an AC of this key covers (GAP-2831; ASM-4684).

### 9. State transitions

The case stage is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story owns is the stage of `LitigationWorkflow` and the state of the step.

| From (stage of `LitigationWorkflow`) | Event | Condition | To |
|---|---|---|---|
| `ENFORCEMENT_DECISION` | DEFER_RECORDED under R-LIT-55 | the reason and the review date are both present | `DEFERRAL_RECORDED`, with the case-move answer `DEFERRAL_RECORDED`, the queue placement and one timer to the review date |
| `DEFERRAL_RECORDED` | The review-date timer fires under R-LIT-56 | the date is reached | `ENFORCEMENT_DECISION`, answered to rwb-case; the return is the timer's own continuation and no AC of this key covers it |
| `IN_HEARING` | JUDGMENT_FOR_THE_BANK under R-LIT-44 | judgment_type in (full, partial, default) | `JUDGMENT_RECORDED`, the behaviour of RWB-S4-E5016-APP on the same contract (AC3) |
| Any other stage | DEFER_RECORDED | the stage is not `ENFORCEMENT_DECISION` | Unchanged, refused with 409 (X4) |
| Any | A deferral on a closed or withdrawn action, or a second deferral for the same stage and date | X4, X7 | Unchanged, refused with 409 or answered from the stored result |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The enforcement-decision signal arrives | The package in force is loaded | Evaluating |
| Evaluating | R-LIT-55 fires | Both elements are valid and the record is written | Applying |
| Applying | The stage move and the case-move answer commit | The transaction commits | Waiting for the review date |
| Applying | The record write or the move fails | X1, X6 | Waiting, nothing changed |
| Applying | An element is absent or invalid | X5 | Waiting, refused with 422 and nothing changed |

The action status is `OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED` or `WITHDRAWN` (TSD S4 T3.2) and is not written by this step: `LOV-LEGAL-STATUS` has no deferred value, so the deferral is the stage and the record and not a status (BR6; ASM-4681).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-ENFORCE, enforcement owner | Litigation U and C in the legacy permission table: records the deferral with its reason and its review date on SCR-20, and is the owner of R-LIT-55 |
| RW-LITOFF, litigation officer | Litigation U and C: works the same step on the enforcement workspace |
| PT-LAWFIRM, law firm user | Litigation U: enters the deferral facts through the `PATCH` operation on the partner portal, scoped to its own cases |
| SY-DATALOAD, SY-CASEWF, SY-RULES, SY-AGENT | Litigation U or R as the TSD S4 T6.1 matrix gives it: the service identities run the step and are subject to the same checks |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-LEGAL and the further roles of the read row | Litigation R: read only |
| rwb-litigation service identity | Runs the step, evaluates the rule, writes the record, holds the stage and answers the case move; it holds no grant on another schema |

The rights above are the legacy permission table of this key and the TSD S4 T6.1 matrix: Litigation `U` for RW-LITOFF, RW-ENFORCE, PT-LAWFIRM and SY-DATALOAD, and Litigation `C` for RW-LITOFF and RW-ENFORCE. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the record and of the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case-move answer and the queue request |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`: the action of this step is `ENFORCEMENT` |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read only: the status is not written by the deferral (BR6) |
| DF-LEG-005, DF-LEG-006, DF-LEG-008, DF-LEG-009 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no, court_name, claim_amount | Read, as the court facts the enforcement decision is taken against; not changed |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by` | Read; the deferral writes no business column, so the optimistic lock is read and not consumed |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule id, rule version, inputs reference, deferral reason, review date, outcome, decided at | Write through the local library, before the stage changes (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule package in force and never as a table |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the stage state comes back on the case answer (BR3) |
| DF-WRK-001 to DF-WRK-008 | queue (P3, `rwb_case`) | id, queue_code, queue_name, team_code, role_code, assignment_method and 2 more | Not written: the queue placement is requested on the case answer (BR3) |
| DF-WRK-009 to DF-WRK-016 | assignment (P3, `rwb_case`) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at and 2 more | Not written: rwb-case assigns on the review date (BR3) |
| DF-WRK-017 to DF-WRK-026 | task (P3, `rwb_case`) | id, case_id, task_code, element_type, discretion, status and 4 more | Not written: the task is requested on the case answer (BR3) |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1, the legacy story Data table and the Logical Data Model and Data Dictionary v8. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in `rwb_litigation` by the library's own migration (DP-03). `deferral_reason` and `deferral_review_date` have no column and are not given one (BR5). The test fixtures are synthetic: case `RC-2026-000820`, action `LA-2026-000820`.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S4-E5020-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in with the deferral element, LegalAction of status 200 out (API-S4-004) | Litigation, right U, scope applied | Not applicable |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its action type, its status and its court facts (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The step reads the action on the GET and records the deferral on the PATCH, whose documented purpose is "record a filing, judgment or enforcement step" (TSD S4 T-A.2). Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-stage action, 422 with MSG-GEN-001 for a missing or invalid deferral element, and 503 when the decision library, a consumed contract or the rule package does not answer. `POST /cases/{caseId}/legal-actions` (API-S4-002), `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) belong to the sibling stories of this service and are not declared here; the create of the legal action in the legacy endpoint list is API-S4-002 and stays with RWB-S4-E5004-APP.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2829; ASM-4682)) | `/api/recovery/case/v1` | P3 rwb-case | The stage state of the case, which must be `ENFORCEMENT_DECISION` for R-LIT-55; faked |
| The case-move answer with the queue placement and the task request (operation name Not specified in the source documents (GAP-2829; ASM-4682)) | rwb-case (P3) | P3 rwb-case | The move `DEFERRAL_RECORDED` and, when the timer fires, the return to `ENFORCEMENT_DECISION` under R-LIT-56, with the queue code, the team, the role `RW-ENFORCE` and the review date; the rows are P3's; faked |
| The rule package in force (operation name Not specified in the source documents (GAP-2829; ASM-4682)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-55 and R-LIT-44; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All three are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2829 with ASM-4682.

#### 12.3 Events published

None. The service's topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its ownership rows list no event of this service (context pack, ownership rows). DP-09 is not in this story's pattern set: the step writes no outbox row, and its outputs are the local decision record of DP-03, the case-move answer and the timer. A deferral is a state of the case and a fact of the record, and a consumer that needs it reads the state on the case contract.

#### 12.4 Events consumed

None. The ownership rows of this service list no consumed event either, so the step starts on a signal of `LitigationWorkflow` and the case and the package arrive on their owners' contracts of 12.2 (GAP-2829; ASM-4682). This story holds no consumer group, no subscription and no inbox of its own, and a build that adds a consumer to `rwb.litigation.events.v1` fails the absence test of the CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the enforcement-decision signal, the rule package in force and the timer fire; outcome: the stage move for the parent |
| `recordEnforcementDeferral` | Activity, the deferral step of this story | `rwb-litigation` | The deferral element in; the rule ID with its package version, the decision record, the stage move and the case-move answer with the queue request out, in one transaction |
| `armReviewDate` | Activity, the review-date step of this story | `rwb-litigation` | The review date in; one durable timer out, and on the fire the case move back to `ENFORCEMENT_DECISION` |

The activity names are target design choices and are fixed by no source document; the trigger of the step is read as a workflow signal, because no source names an event or a Schedule for it (GAP-2829; ASM-4682). No cross-service call is made inside a workflow: each is an activity of the queue above.

#### 12.6 Schedules

None. The step starts on the enforcement-decision signal, and the review date is a durable timer of the workflow, not a Schedule and not the `timer` row of rwb-case; this story registers no Temporal Schedule, no Quartz row and no shared job table, and no Job of the batch catalogue is owned or moved here (GAP-2831; ASM-4684).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read only for the deferral: no business column is written and the status is unchanged (BR6) |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of the deferral, with the reason, the review date and the rule version (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated deferral and the answer it holds |

`hearing` is this service's but is not read by this step. Not owned and never read as a table: `recovery_case`, `queue`, `assignment` and `task` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5) and the payment rows (P8). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read fake | The stage state `ENFORCEMENT_DECISION` of case `RC-2026-000820`, another state, and no answer beyond 2 s | AC1, AC2, X4 |
| rwb-case case-move fake | The move `DEFERRAL_RECORDED` accepted with the queue placement and the task for `RW-ENFORCE`, the return to `ENFORCEMENT_DECISION` on the review date, and a move refused because the case is not in the state the rule expects | AC2, X7 |
| rwb-decision rule-package fake | The LITIGATION package at its version with R-LIT-55 and R-LIT-44, and a second version | AC1, AC2, AC3, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain that answers MSG-P7-003 | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-20 model in the enforcement-decision state and in the deferred state for case `RC-2026-000820` | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT. The three consumed rows carry the placeholder of 12.2 until their owners publish an operation name (GAP-2829; ASM-4682).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The action read and the action update on `/api/recovery/litigation/v1`; the case read, the case answer with the queue request and the rule package; one hop, 2 s each |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 2 activities, 1 durable timer | `LitigationWorkflow` with `recordEnforcementDeferral` and `armReviewDate` on `rwb-litigation`, and the review-date timer; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `enforcement`, Java package `th.co.scb.ace.workbench.recovery.litigation.enforcement`; front end `src/modules/recovery/litigation/RecordEnforcementDeferral.tsx`, the fragment SCR-20 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the stage change commit together or not at all. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-20 reaches this service, one hop through the gateway. DP-05 is held as a prohibition because the service holds no `v_ace_*` grant, DP-01 because only `rwb_litigation` is reachable, DP-09 because no event is declared and DP-10 because the review date is a workflow timer and not a Schedule (GAP-2831; ASM-4684).

**Dependencies the tables add and the plan does not hold.** The three H rows are the plan's. The three consumed contracts of 12.2 are class C dependencies in fact and are not in the metadata row, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2829 with ASM-4682.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` enforcement branch | Workflow | The step that waits for the enforcement-decision signal, loads the package in force, arms the review date and reports the stage move to the parent |
| `recordEnforcementDeferral` | Activity | Reads the action and the deferral element, evaluates R-LIT-55, writes the record and answers the move to `DEFERRAL_RECORDED` with the queue request |
| `armReviewDate` | Activity | Arms one durable timer to the review date and answers the return to `ENFORCEMENT_DECISION` when it fires (R-LIT-56) |
| `DeferralEvaluator` | Service | The evaluation of the deferral against the LITIGATION package version in force, with the state names of the LITIGATION machine |
| `DeferralDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `LegalActionRepository` | Repository | Reads the action on `rwb_litigation` only; the step updates no column |
| `CaseMoveAnswer` and `QueuePlacementRequest` | Signal reporter | Answer rwb-case with the move, the rule, the version, the queue code, the role `RW-ENFORCE` and the review date; they report, they never change a case row |
| `EnforcementDeferralController` | Controller | The two operations, the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RecordEnforcementDeferral` | React component | Shows the enforcement decision, the deferral with its reason and its review date and the rule version on SCR-20, read only |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the reason or the review date (BR5; GAP-2828; ASM-4681).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants; no deferred or deferral-reason value is added to either list.
- The LITIGATION package and its version, authored and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the review-date rule and the D7 route set are values of the package and of reference data, not of this build (GAP-2828; ASM-4681).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The enforcement branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow` (AC1).
2. `LegalActionRepository` reads over `legal_action`, with the action type and the status (AC1, AC2).
3. `DeferralEvaluator` over the LITIGATION package, with R-LIT-55, the two required elements and the no-fire path (AC1, AC2, X4).
4. `DeferralDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `CaseMoveAnswer` and `QueuePlacementRequest` with the move `DEFERRAL_RECORDED` and the queue request (AC2, X7).
6. `armReviewDate` and the durable timer, with the return to `ENFORCEMENT_DECISION` (AC2).
7. `EnforcementDeferralController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, X2, X3, X5).
8. `RecordEnforcementDeferral` and the workspace through the composite route fake (AC1).
9. The regression case of AC3 on the judgment path of RWB-S4-E5016-APP through the same contract (AC3).
10. The boundary test: no statement outside `rwb_litigation`, no write to `rwb_case` or `rwb_decision` (X9, BR3, BR5).

**Feature flag.** `rwb.litigation.enforcement-deferral-v1`, read as a flag of the platform library; off means the step holds the enforcement-decision signal, writes no record and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic enforcement decision in SIT, R-LIT-55 records the reason and the review date and answers the move and the queue request, the timer returns the case on the review date, a repeated deferral writes once, a forced record failure changes nothing, no case, queue, assignment or task row is written from this service, and SCR-20 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription story of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required element of the deferral is absent or invalid (X5), which is VR-S4-020-1 of the FSD | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or records the deferral (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the stage changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-020 section 14 and of the FSD S4 A2.20 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X6) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No new screen is built in this story. One existing surface shows what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-20 Enforcement workspace | Requested | The enforcement step opened after judgment, its owner RW-ENFORCE and the stage `ENFORCEMENT_DECISION`, read only |
| SCR-20 Enforcement workspace | Deferred | The deferral with its coded reason, its review date and the rule R-LIT-55 with its version; the stage `DEFERRAL_RECORDED` |
| SCR-20 Enforcement workspace | Judgment; seized; auctioned; closed | The later states of the sibling stories, read only; this story writes none of them |
| SCR-20 Enforcement workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-20 Enforcement workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |

The legacy state list of SCR-20 is "Requested; seized; auctioned; closed" and carries no deferred state; the deferred reading above is the state this story adds to the screen model, and no screen field list is given by any source for the reason or the review date (GAP-2832; ASM-4685). The route merges this service's answer with rwb-case for the case, its stage and its task; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-020-01 | AC1 | End to end | Record an enforcement deferral with its reason |
| TC-E5-020-02 | AC2 | End to end | Rule R-LIT-55 |
| TC-E5-020-03 | AC3 | End to end | Rule R-LIT-44 |
| TC-E5-020-04 | AC4 | Component | Not recorded |
| TC-E5-020-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-020-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The case, package and route fakes of section 12.8 stand behind every case, and the fixture — case `RC-2026-000820`, action `LA-2026-000820` at `ENFORCEMENT_DECISION`, and case `RC-2026-000716` at `IN_HEARING` for the judgment regression of AC3 — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the review-date rule, the route set, the state names, the lists and the message texts are values and reference rows with a version; no list value, state name or date appears in Java.
- No personal data in logs, workflow inputs, prompts or the fixture: the rows carry case references, action references, codes, dates and amounts only, and the test data is synthetic.
- The case stays with rwb-case: no `recovery_case`, `queue`, `assignment` or `task` row is written here, and the move and the queue placement are requested with the rule and its version (BR3).
- No business column of the action is written by the deferral, and no deferred or deferral-reason value is added to a list to express a state that is a stage (BR5, BR6).
- ACE data only through its owner: no component of this story reads a `v_ace_*` view or an ACE table.
- No read of another service's tables and no cross-schema join: `recovery_case`, `queue`, `assignment`, `task`, `rule_row` and `decision_log_entry` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second deferral.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing (12.3, 12.4).
- SCR-20 is read only; the deferral is posted through the service, and the firm's entry on the partner portal uses the same operation under `PT-LAWFIRM`.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement, which this story does by naming the enforcement owner on the deferral and keeping the case in his queue until the review date (FSD S4 Requirements served) | FEAT-LIT-20 | 08 Litigate and enforce | R-LIT-55, R-LIT-44 | TC-E5-020-01, TC-E5-020-02, TC-E5-020-03 |

The legacy story master of RWB-E5-020 carries no requirement ID and the plan's requirement list for this slice is empty; the trace is the requirement the FSD S4 serves for enforcement after judgment, which is the outcome the feature states (GAP-2833; ASM-4686).

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-020 | The four legacy criteria word for word, the two rules, the screen, the messages and the six test cases; the `recovery_case`, `queue`, `assignment` and `task` rows of the legacy data table are P3's |
| RWB-S4-E5020-CON | H: the two operations, the deferral and review-date elements, the stage vocabulary, the error set and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-20 |
| rwb-case (P3) and rwb-decision (P7) contracts | C in fact and not in the metadata row: the case read, the case answer with the queue request and the rule package, faked (GAP-2829) |
| FEAT-LIT-20, FEAT-LIT-16, SCR-20, SCR-19 | The feature, its judgment prerequisite and the screens of the legacy story |
| RWB-S4-E5016-APP | The judgment write behind R-LIT-44, which AC3 proves as a regression (GAP-2830) |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Temporal layer with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the two operations, the deferral and review-date elements, the error set and the fakes: RWB-S4-E5020-CON.
- The case of record, its stage state, the parent `CaseWorkflow`, the queue, the assignment and the task rows: rwb-case (P3), which creates them on this story's request (GAP-2829; ASM-4682).
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-55 and R-LIT-44: rwb-decision (P7) (GAP-2828; ASM-4681).
- The reason code list, its values and its owner in reference data, which no source names (GAP-2828; ASM-4681).
- The judgment write itself and its criteria beyond the regression of AC3: RWB-S4-E5016-APP (GAP-2830; ASM-4683).
- The return on the review date under R-LIT-56 as a separate behaviour, and the second deferral with no asset that routes the case to write-off under R-LIT-57: the timer continuation of this story and rwb-writeoff (S7) (GAP-2831; ASM-4684).
- The asset trace, the writ, the seizure, the auction and the payment match (R-LIT-50 to R-LIT-54, R-LIT-51, R-LIT-65): the enforcement stories of this service, rwb-asset (S5) and rwb-payment (P8).
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-20: rwb-access (P4), RWB-PLT-N001-CON and GAP-2832 (ASM-4685).
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

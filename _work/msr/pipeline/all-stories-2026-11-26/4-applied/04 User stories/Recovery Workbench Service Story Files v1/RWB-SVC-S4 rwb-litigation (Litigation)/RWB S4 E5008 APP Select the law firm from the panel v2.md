# RWB-S4-E5008-APP Select the law firm from the panel

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S4-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5008-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-008 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the panel, the scorecard and the firm decline come from rwb-partner (S9) on its published contract, because `partner` and `partner_instruction` are S9's tables and not this service's; the legacy `recovery_case` route states `FIRM_SELECTION` and `FIRM_DECLINED` stay with rwb-case (P3) and are answered, not written; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the legal action changes (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19); the legacy `v_ace_score` read has no grant here, so DP-05 applies as a prohibition (GAP-2778; ASM-4612). The panel read, the decline read and the case-move answer have no contract story in the plan and no C row (GAP-2773; ASM-4607). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5008-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer**, I want **the Workbench to pick the firm by the panel rule: scorecard, capacity, court and conflict, so that cases reach court faster with complete packs**.

This is the application slice of legacy RWB-E5-008. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the firm-selection step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19, "LitigationWorkflow (years; continues-as-new)"; Temporal and Drools Design slides 5, 7 and 20);
- the evaluation of R-LIT-23 on the pack-verified fact and of R-LIT-27 on the decline fact, with the LITIGATION package version in force;
- the write of `law_firm_id` (DF-LEG-003) on the `legal_action` of the case in schema `rwb_litigation`, once per selection and once per re-selection, with no new column;
- the local decision record of the selection with the rule ID and the version, written through RWB-PLT-E1027-CON before the legal action changes (DP-03);
- the answer to rwb-case for the case move `FIRM_SELECTION` or `FIRM_DECLINED`, with the rule and the version that produced it;
- `GET /legal-actions/{legalActionId}` and `PATCH /legal-actions/{legalActionId}` on base `/api/recovery/litigation/v1` under capability area "Litigation" with the rights R and U (DP-13; TSD S4 T-A.1);
- SCR-19 Litigation workspace in its pack and instructed states, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the three legal-action operations, the `law_firm_id` element, the panel and case-move rows, the error set and the fakes, which are RWB-S4-E5008-CON; the panel, its scorecard, its capacity, its court coverage and its conflict status, which are rwb-partner's (S9); the issue of the instruction itself and the partner clock, which are `RWB-S4-E5009-APP`'s and rwb-partner's; the case of record and the route states `FIRM_SELECTION` and `FIRM_DECLINED`, which are rwb-case's (P3); the authoring and approval of the LITIGATION package and of the two rule rows, which are rwb-decision's (P7); the pack and its documents, which are rwb-document's (P5); and the deployment, the flag and the runbook, which are the operations story of this legacy key.

### 2. Business rationale

Legacy RWB-E5-008 gave the Workbench one unattended step that read the panel, scored the firms, weighed capacity, court and conflict and picked the firm, and it kept two rule outcomes: R-LIT-23 selected the firm by rule once `pack_verified_at` was set, and R-LIT-27 recorded the decline and re-selected the next firm on the scorecard. The functional specification keeps the objective and its metric — a litigation turnaround of 6 days against the 21 days a filing takes today, measured on the decision log and the Workbench records, reviewed monthly — and the program keeps the requirement: REQ-S4-004, "A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal" (FSD S4 A2.8 and its requirements-served list).

What D-RCV-60 changes is who owns the panel and who owns the case. In the monolith the panel row, the instruction row, the case state and the decision log row sat in one `recovery` schema and one process. In the target:

- **the panel is rwb-partner's (S9).** `partner` and `partner_instruction` are S9's tables, and the panel status, the scorecard, the capacity, the court coverage and the conflict check are answered there (Ownership Map: partner and partner_instruction owner S9; TSD S9 T3.1 and API-S9-001 "List partners with panel status and score"). This story reads them on the owner's contract and its fake, holds no panel row and writes none (GAP-2778; ASM-4612);
- **the case of record stays with rwb-case (P3).** `recovery_case` and the route states `FIRM_SELECTION` and `FIRM_DECLINED` are P3's; this story evaluates the rule, writes the selected firm on its own legal action, records the decision and **answers** rwb-case for the case move (GAP-2773; ASM-4607);
- **the legal action and the selected firm stay with rwb-litigation (S4).** `legal_action.law_firm_id` (DF-LEG-003) is this service's column and the firm reference it holds is the S9 partner reference, an identifier and not a foreign key across schemas (DP-01);
- **the selection rule is rwb-decision's.** The rule rows of R-LIT-23 and R-LIT-27, the package version and the scorecard weights are authored, tested and approved in rwb-decision (P7) and loaded here; no weight, threshold, window or role is a constant of this build (GAP-2777; ASM-4611);
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the legal action change, which is what legacy AC1 asked for and legacy AC4 tested;
- **no ACE view is read here.** The legacy data table lists `v_ace_score`; the ACE view contract and the score facts are rwb-source-data's (P1) and the scorecard of a panel firm is S9's, so DP-05 applies to this story as a prohibition and the service holds no `v_ace_*` grant (GAP-2778; ASM-4612).

The decline is not carried by an event here. rwb-partner produces `PartnerResultSubmitted`, whose consumer row lists rwb-litigation, but DP-09 is not in this story's pattern set, it writes no inbox row, and the S4 IN row of the service card names the event without assigning it to this step; the decline therefore arrives on the rwb-partner contract, one hop with a 2 s budget, and this story publishes and consumes nothing (GAP-2774; ASM-4608). The agreement between the legacy wording and the target is exactly this: the panel and the scorecard are rwb-partner's, the case route state is rwb-case's, and this story evaluates the rule, writes the firm on its legal action and answers the case move.

No business value moves. The scorecard weights, the capacity test, the court coverage set, the conflict check, the 2-working-day window of R-LIT-27 and the D7 decision level are values and reference rows with a version, read from the package and from reference data.

### 3. Preconditions

- RWB-S4-E5008-CON is published: the three legal-action operations, the `law_firm_id` element of `LegalAction` and `LegalActionUpdate`, the panel and case-move rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The panel list operation of rwb-partner (API-S9-001 `GET /partners` "List partners with panel status and score", on base `/api/recovery/partner/v1`) and the instruction read that answers a decline (API-S9-003/API-S9-004 of the partner set) are published with their fakes. Neither names a contract story in the plan and neither operation shape is fixed for the S9 side: the operation names are Not specified in the source documents (GAP-2773; ASM-4607).
- The case-move answer of rwb-case is available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies to the case of record, and where rwb-case publishes a REST case-move operation its name is Not specified in the source documents (GAP-2773; ASM-4607).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the legal action change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 Litigation workspace reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` exists in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-014 and the standard record columns of TSD S4 T3.0; this story writes one of the existing columns and adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version, with R-LIT-23 and R-LIT-27 in it. The rule rows, the scorecard weights, the capacity test, the court coverage set, the conflict check and the 2-working-day accept window have no content in any source read for this key and are governed in rwb-decision (GAP-2777; ASM-4611).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_partner`, `rwb_case` or `v_ace_score` is refused by the database and fails the boundary test (DP-05; GAP-2778; ASM-4612).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5008-CON when its tests pass.

### 4. Flow

1. The pack of the case is verified and approved in the pack stories of this service; the fact that starts the selection is the arrival of the pack-approved fact for a case in `PACK_VERIFIED` (R-LIT-23). The legacy story says the step runs unattended and the FSD declares no background event, so the trigger is this story's design and is carried as the working read of the assumption (GAP-2775; ASM-4609).
2. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, `case_id` (DF-LEG-002), `court_name` (DF-LEG-008) and the current `law_firm_id` (DF-LEG-003).
3. `PanelClient` reads the panel on the rwb-partner contract (API-S9-001): for each firm its partner reference, `partner_type` (DF-PRT-004), `panel_status` (DF-PRT-005), contract end (DF-PRT-007), its score and its capacity, court coverage and conflict status, one hop with a 2 s budget and a breaker (GAP-2778; ASM-4612).
4. `FirmSelectionEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates R-LIT-23 on the pack-verified fact and on the panel answer: the firm is scored, it has capacity, it covers the court of the case and it passes the conflict check.
5. The evaluation answers the rule ID, the package version, the selected firm reference, the ranked shortlist and the case move the rule names (FSD S4 A2.8.3.1; Business Rules and Routing Logic v4).
6. `SelectionDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the ranked shortlist reference, the selected firm and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
7. `LegalActionFirmWriter` patches the legal action on `PATCH /legal-actions/{legalActionId}` (API-S4-004) in one `rwb_litigation` transaction with the decision record and the idempotency row: `law_firm_id` (DF-LEG-003) becomes the selected firm reference. No other column changes; `status` stays `OPEN` until a filing is recorded, and `hearing` is untouched.
8. `CaseMoveAnswer` answers rwb-case with the case move `FIRM_SELECTION`, the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither.
9. On R-LIT-27 the decline of the instruction arrives on the rwb-partner contract: the step records the decline on the decision record, re-selects the next firm on the ranked shortlist of the scorecard with the same evaluation, patches `law_firm_id` to the next firm, and answers the case move `FIRM_DECLINED` with the rule and the version.
10. A repeated pack-approved fact, or the same `Idempotency-Key`, writes nothing, sends no second case-move answer and counts the repeat.
11. SCR-19 Litigation workspace shows the selected firm, the ranked shortlist and the case state through the gateway-bff composite route, read only, next to the case and the route state of rwb-case and the instruction of rwb-partner (DP-19).
12. Where no panel firm covers the court, has capacity, or passes the conflict check, no rule of this story fires: the case is escalated by R-LIT-25 on the sibling story of this service and this step writes nothing.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: `law_firm_id` keeps its value and no case-move answer leaves the service | MSG-P7-003 | AC4, TC-E5-008-04, TC-E5-008-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC2, AC3, TC-E5-008-05 |
| X3 | The legal action does not exist or is outside the scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC2, AC3 |
| X4 | The legal action is `CLOSED` or `WITHDRAWN`, or is not the action type the rule needs | 409 and nothing changes; no firm is selected on a closed action | None | AC2, AC3 |
| X5 | The rwb-partner panel read or the rwb-case answer does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no case move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X6 | No panel firm covers the court, has capacity, or passes the conflict check | No rule fires: nothing changes, no decision record is written, and the escalation of R-LIT-25 is the sibling story's | None | AC1, AC2 |
| X7 | The instruction is declined, or is not accepted inside the window of R-LIT-27 | The decline is recorded on the decision record, the next firm on the scorecard is selected and the case move `FIRM_DECLINED` is answered | None | AC3 |
| X8 | The same pack-approved fact or the same `Idempotency-Key` arrives twice | One write and one case-move answer; the repeat is counted and no second decision record is written | None | AC1 |
| X9 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X10 | A component, a statement or a test reads a `partner` or `partner_instruction` row, a `recovery_case` row, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR8 |

X1 to X4 and X7 are the exception paths of RWB-E5-008 carried onto the split, X5, X6, X8 and X9 are the paths the target call types and the rule package add, and X10 is the DP-05 and DP-01 boundary. The weights, the window and the court set of X6 and X7 are values in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5008-CON, the rwb-partner and rwb-case fakes and the rule-package fake, on the table of its own schema, and needs no live rwb-partner, no live rwb-case and no live rwb-decision |
| Negotiable | The activity name, the decision code per rule, the shape of the ranked shortlist and the stage outcome are this story's choice; the rules, the messages, the screens, the operations and the `law_firm_id` element are fixed |
| Valuable | The firm is picked once by rule, with the reason and the version recorded, and the case moves in the service that owns it |
| Estimable | One workflow step, one evaluator, one record write, one column write, one case-move answer, two clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and panel answers through the contract fakes, plus the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Select the law firm from the panel

  Background:
    Given case "RC-2026-000805" carries the legal action "LA-2026-000805" of action type "CIVIL_CASE" with status "OPEN" and no firm selected
    Given the LITIGATION rule package is in force at its version and carries R-LIT-23 and R-LIT-27
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Select the law firm from the panel (legacy RWB-E5-008 AC1)
    Given the rwb-partner contract mock returns the panel of firms with their scorecard, capacity, court coverage and conflict status
    Given the rwb-case contract mock returns the case state "PACK_VERIFIED" for "RC-2026-000805"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then picks the firm by the panel rule: scorecard, capacity, court and conflict
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-23 (legacy RWB-E5-008 AC2)
    Given the rwb-case contract mock returns the case state "PACK_VERIFIED" for "RC-2026-000805"
    Given the rwb-partner contract mock returns the panel firm selected for legal action "LA-2026-000805"
    Given a case in state PACK_VERIFIED
    When pack approved
    Then select the law firm by rule from the panel
    Then the case moves to FIRM_SELECTION

  Scenario: AC3 Rule R-LIT-27 (legacy RWB-E5-008 AC3)
    Given the rwb-case contract mock returns the case state "FIRM_INSTRUCTED" for "RC-2026-000805"
    Given the rwb-partner contract mock returns the instruction declined and the next firm on the scorecard for legal action "LA-2026-000805"
    Given a case in state FIRM_INSTRUCTED
    When instruction declined
    Then record the decline and re-select the next firm on the scorecard
    Then the case moves to FIRM_DECLINED

  Scenario: AC4 Not recorded (legacy RWB-E5-008 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-008 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1 to AC3 each carry their `Given the <service> contract mock returns <x>` lines and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-partner answers the panel, the scorecard and the decline; this story evaluates R-LIT-23 or R-LIT-27, writes the decision record with the rule version and the selected firm on the legal action; and rwb-case writes the case move to `FIRM_SELECTION` or `FIRM_DECLINED`. No `partner`, `partner_instruction`, `recovery_case` or `v_ace_score` row is read or written as a table here (GAP-2773, GAP-2778; ASM-4607, ASM-4612).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-23 | Litigation | D7 | PACK_VERIFIED | PACK_APPROVED | pack_verified_at set | Select the law firm by rule from the panel | FIRM_SELECTION | Workbench | Rules component, partner performance data | Same day |
| R-LIT-27 | Litigation | D7 | FIRM_INSTRUCTED | INSTRUCTION_DECLINED | the firm declines, or does not accept inside the window | Record the decline and re-select the next firm on the scorecard | FIRM_DECLINED | Workbench | Partner Portal | 2 working days |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character, and they are the two rules the legacy criteria of this story name. Their owner column is a role of the business and not a service: the `Workbench` of both rows is the record this story writes on the legal action and on the decision record, while the to state is a case route state of rwb-case and is answered, not written. The systems column names the Rules component, which is rwb-decision, and the partner performance data and the Partner Portal, which are rwb-partner's.

| ID | Rule | Source |
|---|---|---|
| BR1 | The legal action and the selected firm are this service's: `law_firm_id` (DF-LEG-003) is a column of `legal_action` in `rwb_litigation`, and no other service writes it | Architecture v5 slide 41 (rwb-litigation owns legal actions, hearings, judgments); Ownership Map (legal_action owner S4); TSD S4 T3.1 |
| BR2 | The decision is recorded before the legal action changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-008 AC1 and AC4 |
| BR3 | The panel stays with rwb-partner: this story holds no `partner` or `partner_instruction` row, reads them on the owner's contract only, and writes no score, no panel status and no decline | Ownership Map (partner and partner_instruction owner S9); TSD S9 T3.1 and API-S9-001; GAP-2778 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states `FIRM_SELECTION` and `FIRM_DECLINED` are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-2773 |
| BR5 | No ACE view and no ACE table is read or written here, and no cross-schema join is made: the scorecard and the score facts arrive on the owners' contracts, and the court facts are this service's own columns | DP-05; Architecture v5 slides 29 and 41 (the ACE view contract is P1's); GAP-2778 |
| BR6 | One firm per selection, and one re-selection per decline: a second selection without a decline or a new pack-approved fact writes nothing | R-LIT-23 and R-LIT-27 of the Business Rules and Routing Logic v4; TSD S4 T4 |
| BR7 | The same fact twice, or the same `Idempotency-Key` twice, writes once and answers the case move once | TSD S4 T-A.2 (Idempotency-Key on the write operations); Architecture v5 slide 11 |
| BR8 | The vocabulary is closed: `LOV-LEGAL-TYPE` is NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION, LED_AUCTION and `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN; no state name, list value, weight, window or threshold is written in code | TSD S4 T3.2; BR-S4-008 (FSD S4 A2.8.3.1); Template and Rules v1 §R7.2 (s17) |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or an event: the step carries case references, partner references, codes, dates and scores | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes (events carry IDs and facts, never personal data) |

**Where each rule lives in the target.** R-LIT-23 is the selection: the evaluator tests the panel answer against the court, capacity and conflict facts of the case, the record is written, `law_firm_id` takes the selected firm and the case-move answer carries `FIRM_SELECTION`. R-LIT-27 is the re-selection: the decline answered on the rwb-partner contract is recorded, the next firm on the ranked shortlist is written to `law_firm_id` and the case-move answer carries `FIRM_DECLINED`. VR-S4-008-1 of the FSD tests the freshness of the ACE batch of the source and raises MSG-P1-001; this service holds no `v_ace_batch_status` read, so the check belongs to the owner of the data product and the message is carried in section 14 without a path here (GAP-2779; ASM-4613).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the firm on the legal action and the state of the step.

| From (`legal_action.law_firm_id`) | Event | Condition | To |
|---|---|---|---|
| Empty, action type `CIVIL_CASE` or `NOTICE` | PACK_APPROVED under R-LIT-23 | A panel firm is scored, has capacity, covers the court and passes the conflict check | The selected firm reference, with the case-move answer `FIRM_SELECTION` |
| A firm reference, after the case is at `FIRM_INSTRUCTED` | INSTRUCTION_DECLINED under R-LIT-27 | The firm declines, or does not accept inside the window | The next firm on the scorecard, with the decline recorded and the case-move answer `FIRM_DECLINED` |
| CLOSED or WITHDRAWN | Any of the two rules | X4 | Unchanged, refused with 409 |
| Empty | A panel answer with no firm that covers the court, has capacity or passes the conflict check | X6 | Unchanged, no rule fires and no record is written |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The pack-approved fact arrives for a case in `PACK_VERIFIED` | The package in force is loaded | Evaluating |
| Evaluating | The rule fires | The decision record is written | Applying |
| Applying | `law_firm_id` is patched and the case-move answer is sent | The transaction commits | Waiting for the next fact |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Waiting | The instruction is declined | X7 | Evaluating on the next firm |

`status` (DF-LEG-014) is not moved by this story: it stays `OPEN` until a filing writes `FILED`. The route states `PACK_VERIFIED`, `FIRM_SELECTION`, `FIRM_INSTRUCTED` and `FIRM_DECLINED` of the legacy criteria are case route states and are read from rwb-case and asserted on its answer, not on a column of this service.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| None; runs unattended (the feature of FSD S4 A2.8.3.3) | The primary actor: the step runs under the service identity with no officer task on the happy path |
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix and "Also uses" in the FSD: reads the action and the shortlist, patches the selection and the re-selection, reads the case move |
| RW-LEGAL, legal counsel | Litigation RA: reads the action, the selected firm and the outcome; records no selection |
| RW-HEADLIT, Head of Litigation | Litigation RA: reads, and acts on the nomination and panel-widening paths of the sibling stories, not here |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-PRODHEAD, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU on its own instruction, through the partner gateway: it records the decline that produces the fact of R-LIT-27, which is read here on the rwb-partner contract |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it: the service identities are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record and the firm on the legal action, and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the litigation officer as also-user, and both statements hold: the step runs under the service identity, and the officer acts on SCR-19 and on the re-selection path. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the answer and of the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case-move answer |
| DF-LEG-003 | legal_action (S4, `rwb_litigation`) | law_firm_id | Write, with the selected firm reference and with the next firm of a re-selection |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`, to test that the action is one the rules apply to |
| DF-LEG-008 | legal_action (S4, `rwb_litigation`) | court_name | Read, for the court coverage test of R-LIT-23 |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read, to refuse a closed or withdrawn action (X4); not written here |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the legal action changes |
| DF-PRT-001 to DF-PRT-007 | partner (S9, `rwb_partner`) | id, partner_code, partner_name, partner_type, panel_status, contract_end and 1 more | Read only through the S9 owner's contract and never written, joined or stored here |
| DF-PRT-008 to DF-PRT-016 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id, instruction_type, instructed_at, due_at and 3 more | Read only through the S9 owner's contract, for the decline fact of R-LIT-27 |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | the case and its route state | Not read as a table: the state is answered by rwb-case on the case-move call |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule id, rule version, route set, from state, event code | Not read as a table: the rules arrive on `RulePackageInForce` |
| DF-ACE-270 to DF-ACE-279 | v_ace_score (P1) | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Not read: this service holds no `v_ace_*` grant, and DP-05 applies as a prohibition (BR5) |
| The scorecard facts | panel answer of rwb-partner (S9) | the score, the capacity, the court coverage and the conflict status of a panel firm | Read on the owner's contract; their field list is Not specified in the source documents (GAP-2778; ASM-4612) |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1 and T3.2 and the Logical Data Model and Data Dictionary v9; the `partner` and `partner_instruction` rows are the rows the legacy story lists in its Data table, with their owner changed to S9 by the target. **No new table, no new column and no migration**: `legal_action` arrives with the DB story of this service, this story writes one existing column, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). The scorecard weights, the capacity test, the court coverage set and the conflict check have no field list and no value in any source, so they are carried as facts of the rwb-partner answer and of the rule package and marked with the placeholder (GAP-2777, GAP-2778; ASM-4611, ASM-4612).

**No personal data.** The rows this story writes carry identifiers, codes, scores, dates and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind the read and the patch; the create is the sibling stories' and is listed because the legacy endpoint table of the key names it.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with `law_firm_id`, `court_name` and `status` (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in with `law_firm_id`, LegalAction out (API-S4-004) | Litigation, right U, scope applied | Not applicable |
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-type action, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the decision library, the partner contract or the rule package does not answer. The operation IDs are those of TSD S4 T-A.1 and are not redefined here; API-S4-001 `POST /notices/{noticeId}/approve` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the notice and hearing stories of this service and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The panel list operation, API-S9-001 `GET /partners` (operation name of the S9 contract Not specified in the source documents (GAP-2773; ASM-4607)) | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The panel with its panel status, type and contract end, and the score, capacity, court coverage and conflict status of each firm; faked |
| The instruction read that answers a decline, API-S9-003 and API-S9-004 of the partner set (operation name Not specified in the source documents (GAP-2773; ASM-4607)) | `/api/recovery/partner/v1` | S9 rwb-partner | The decline of the firm instruction of the case, which is the fact of R-LIT-27; the instruction itself is `RWB-S4-E5009-APP`'s; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2773; ASM-4607)) | rwb-case (P3) | P3 rwb-case | The answer that carries `FIRM_SELECTION` or `FIRM_DECLINED` with the rule and its version; the row and the route state are P3's; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). None of the three is in this story's contract-dependency row, which is None, so each is a class C dependency in fact and the absence is recorded as GAP-2773 with ASM-4607; the partner rows additionally carry the absence of a contract story for S9 in the plan.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This story publishes none of them: DP-09 is not in its pattern set, it writes no outbox row, and its two outputs are the local decision record of DP-03 and the case-move answer of 12.2. The catalogue is not widened and a build that adds a fourth event to this service fails the absence test.

#### 12.4 Events consumed

None. `PartnerResultSubmitted` is produced by rwb-partner on `rwb.partner.events.v1` and its consumer row lists rwb-litigation, rwb-asset and rwb-case, but DP-09 is not in this story's pattern set, the S4 IN row of Architecture v5 slide 19 names the event without assigning it to this step, and no source states that the decline of an instruction is its trigger. The decline therefore arrives on the rwb-partner contract of 12.2, synchronously, and this story holds no consumer, no inbox row of its own and no subscription (GAP-2774; ASM-4608). The case route state it needs is answered by rwb-case on the same call pattern.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the pack-approved fact, the case state answered by rwb-case, the decline answered by rwb-partner and the rule package in force |
| `selectPanelFirm` | Activity, the one firm-selection step of this story | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the selected firm, the ranked shortlist and the case move out, with the decision record and the legal action written in one transaction |

`issueInstruction` is rwb-partner's activity on queue `rwb-partner` (Architecture v5 slide 41 notes) and is not registered, called or redeclared here; the instruction and its clock are `RWB-S4-E5009-APP`'s and the partner stories'. The activity name is a target design choice of this story and is fixed by no source document; the trigger of the step is read as the arrival of the pack-approved fact for a case in `PACK_VERIFIED`, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2775; ASM-4609).

#### 12.6 Schedules

None. The step runs from the pack-approved fact and from the decline the partner contract answers, and owns no Temporal Schedule and no legacy Quartz job. The 2-working-day window of R-LIT-27 is a durable timer of the step, not a Schedule, and the prescription clock, the proof window and the trace window of the journey are durable timers of the workflow and belong to the sibling stories; no Job of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The action and the selected firm; this story writes `law_firm_id` (DF-LEG-003) and the standard record columns |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the selection and of the decline (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated fact and the answer it holds |

Not owned and never read as a table: `partner` and `partner_instruction` (S9), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `document` (P5), `hearing` (S4, read only by the sibling stories), and every `v_ace_*` view (P1). No foreign key leaves the schema and `legal_action.law_firm_id` and `legal_action.case_id` are identifiers, not foreign keys across schemas (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-partner panel fake (API-S9-001) | The panel of firms for case `RC-2026-000805`: a firm with the best score that covers the court and has capacity; a firm that fails the conflict check; a firm that fails the capacity test; no firm that covers the court; no answer beyond 2 s | AC1, AC2, X5, X6 |
| rwb-partner instruction fake | The instruction of `LA-2026-000805` declined by the selected firm, with the next firm on the scorecard; an instruction accepted inside the window; a refusal for a firm outside the panel | AC3, X7 |
| rwb-case case-move fake | The case state `PACK_VERIFIED` and `FIRM_INSTRUCTED` of case `RC-2026-000805`; the move `FIRM_SELECTION` accepted, the move `FIRM_DECLINED` accepted and a move refused because the case is not in the state the rule expects | AC1, AC2, AC3 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-23 and R-LIT-27, and the earlier version of the package | AC1, AC2, X9 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 answer for case `RC-2026-000805`, with the selected firm, the shortlist and the legal action facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The panel and decline operation names, the score, capacity, court coverage and conflict fields, and the case-move answer are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2773, GAP-2778; ASM-4607, ASM-4612).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | The read, the patch and the create of the legal action on `/api/recovery/litigation/v1`; the panel read and the decline read of rwb-partner, and the case-move answer; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity | `LitigationWorkflow` and its one firm-selection step on `rwb-litigation`; no Schedule, and the R-LIT-27 window is the step's durable timer |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `firmselection`, Java package `th.co.scb.ace.workbench.recovery.litigation.firmselection`; front end `src/modules/recovery/litigation/FirmSelection.tsx`, the fragment SCR-19 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: this service holds no `v_ace_*` grant, reads no ACE view and no ACE table, and the score and panel facts are the ones the rwb-partner contract answers (Architecture v5 slides 29 and 41; GAP-2778; ASM-4612). DP-03 is the transaction rule of the step: the record and the `legal_action` row commit together or not at all. DP-13 moves the base of the three operations and nothing else. DP-19 is how SCR-19 reaches this service, one hop through the gateway.

**Dependencies the tables add and the plan does not hold.** The panel read, the decline read and the case-move answer are class C dependencies in fact and the plan's C row is None; no contract story of rwb-partner exists in the plan at all, so the owner document of the two partner rows has no story key. The story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2773 with ASM-4607.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` selection branch | Workflow | The step of the journey that waits for the pack-approved fact and the decline, loads the package in force and reports the outcome to the parent |
| `selectPanelFirm` | Activity | The one step: read the legal action, read the panel, evaluate R-LIT-23 or R-LIT-27, write the record and the firm, answer the case move |
| `FirmSelectionEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the ranked shortlist and the re-selection on a decline |
| `SelectionDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `LegalActionFirmWriter` | Repository | Writes `law_firm_id` (DF-LEG-003) and the standard columns of `legal_action` in one `rwb_litigation` transaction, with the idempotency row and the optimistic lock |
| `PanelClient` | Client | The panel and instruction reads of rwb-partner, one hop, 2 s, breaker, and no retry of its own |
| `CaseMoveAnswer` | Signal reporter | Answers rwb-case with the case move, the rule and the version; it reports, it never changes a case row |
| `FirmSelectionController` | Controller | The read and the patch of the legal action with the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `FirmSelection` | React component | Shows the selected firm and the ranked shortlist on SCR-19, read only, with the refusal states |

**Database and migrations.** No Flyway file. `legal_action` arrives with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the score, the capacity, the court coverage, the conflict status or the ranked shortlist: those are facts of the request and of the answer, and storing them would copy another service's facts into this schema (GAP-2778; ASM-4612).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the scorecard weights, the capacity test, the court coverage set, the conflict check and the 2-working-day window are values of the package and of reference data, not of this build (BR-S4-008).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The selection branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the pack-approved fact as its trigger (GAP-2775; ASM-4609).
2. `PanelClient` against the rwb-partner panel and instruction fakes, with the 2 s budget, the breaker and the no-answer path (AC1, X5).
3. `FirmSelectionEvaluator` over the LITIGATION package, with the two rules, the ranked shortlist, the re-selection and the no-fire path (AC1, AC2, AC3, X6, X7).
4. `SelectionDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `LegalActionFirmWriter` with the one transaction, the `law_firm_id` write and the idempotency row (AC2, AC3, X8).
6. `CaseMoveAnswer` and the parent signal, with the two moves (AC2, AC3).
7. `FirmSelectionController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, AC2).
8. `FirmSelection` and SCR-19 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no read of `rwb_partner` or `rwb_case`, no write to `rwb_decision` (X10, BR3, BR5).

**Feature flag.** `rwb.litigation.firm-selection-v1`, read as a flag of the platform library; off means the step holds the pack-approved fact and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic pack-approved fact in SIT, each of the two rules produces its record, its firm and its move, a declined instruction re-selects the next firm, a repeated fact writes once, a forced record failure changes nothing, no `partner`, `partner_instruction` or `recovery_case` row is written from this service, and SCR-19 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service and its screen text, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid (X5 of the contract) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or patches the legal action (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-008-1 (FSD S4 A2.8.3.1). This service holds no ACE batch status read, so the check is the owner's and the message is carried here (GAP-2779; ASM-4613) | {product} is from {date}. Today's ACE batch has not arrived. |

The six texts are the legacy wording of RWB-E5-008 and of the FSD S4 A2.8 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X5) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. One existing surface shows what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Pack | The pack states of the sibling stories next to the legal action of the case, read only |
| SCR-19 Litigation workspace | Selected | The selected firm by reference and code, its score and the case move `FIRM_SELECTION`, read only after the step |
| SCR-19 Litigation workspace | Declined | The decline recorded, the next firm on the scorecard and the case move `FIRM_DECLINED` |
| SCR-19 Litigation workspace | Instructed | The instruction of `RWB-S4-E5009-APP` and the action status `OPEN`, read only |
| SCR-19 Litigation workspace | Filed | The filing date and the action status `FILED`, read only, owned by the filing story |
| SCR-19 Litigation workspace | Hearing | The hearing dates of `hearing`, read only, owned by the sibling stories |
| SCR-19 Litigation workspace | Judgment | The judgment facts of `legal_action`, read only, owned by the sibling stories |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Stale data | The message MSG-P1-001 shown where the owner reports the stale data product of the source |

The route merges the answer of this service with rwb-case for the case and its route state and with rwb-partner for the panel and the instruction; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here. The five state names of the legacy list ("pack; instructed; filed; hearing; judgment") are kept and the selected, declined, not-recorded, refused and stale states are the ones this story adds.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-008-01 | AC1 | End to end | Select the law firm from the panel |
| TC-E5-008-02 | AC2 | End to end | Rule R-LIT-23 |
| TC-E5-008-03 | AC3 | End to end | Rule R-LIT-27 |
| TC-E5-008-04 | AC4 | Component | Not recorded |
| TC-E5-008-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-008-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The partner panel and instruction fakes, the case-move fake, the rule-package fake and the decision-record stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000805`, action `LA-2026-000805`, the panel of the firm with the best score and the decline of the selected firm — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the scorecard weights, the capacity test, the court coverage set, the conflict check, the 2-working-day window, the lists and the message texts are values and reference rows with a version; no list value, state name, weight or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry identifiers, codes, scores, dates and a rule version only, and the test data is synthetic.
- The panel stays with rwb-partner: no `partner` row, no `partner_instruction` row, no score, no panel status and no decline is written here (BR3; DP-01).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR4).
- ACE data only through the owner's contract: no component of this story reads a `v_ace_*` view or an ACE table, and the service holds no `v_ace_*` grant (DP-05).
- No read of another service's tables and no cross-schema join: `partner`, `partner_instruction`, `recovery_case`, `rule_row` and `decision_log_entry` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second selection.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing, and the catalogue of the service is not widened (12.3, 12.4).
- SCR-19 is read only; the screen posts nothing and its pack, filing, hearing and approval actions belong to the sibling stories.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal; this story performs the selection and answers the case move, and the instruction is `RWB-S4-E5009-APP`'s (FSD S4 requirements served; Business Requirements Program v5); the legacy story master carries no requirement ID (GAP-2776; ASM-4610) | FEAT-LIT-08 | 08 Litigate and enforce | R-LIT-23, R-LIT-27 | TC-E5-008-01, TC-E5-008-02, TC-E5-008-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-008 | The four legacy criteria word for word, the two rules, the screen, the messages and the six test cases; the `partner` and `partner_instruction` writes and the `v_ace_score` read of the legacy data table are retired |
| RWB-S4-E5008-CON | H: the three operations, the `law_firm_id` element, the panel and case-move rows and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 |
| rwb-partner (S9) and its panel and instruction reads | C in fact and not in the metadata row: the panel, the scorecard, the capacity, the court coverage, the conflict status and the decline, faked (GAP-2773) |
| rwb-case (P3) and its case-move answer | The case of record and the route states `FIRM_SELECTION` and `FIRM_DECLINED`, answered and never written (GAP-2773) |
| RWB-S4-E5008-APP and RWB-S4-E5008-CON siblings of this key | The selection ownership of this service, and the contract half of the same legacy key |
| FEAT-LIT-08, SCR-19 | The feature and the screen of the legacy story |
| DP-03, DP-05, DP-13, DP-19 | The decision record, the ACE prohibition, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-015, ADR-017, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the event platform this story adds no producer or consumer to, the embedded Drools runtime, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-partner and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the three operations, the `law_firm_id` element, the panel and case-move rows, the error set and the fakes: RWB-S4-E5008-CON.
- The panel, the scorecard, the capacity, the court coverage, the conflict check, the panel status and the decline record: rwb-partner (S9), its panel and instruction operations and its own stories. **The panel is answered by rwb-partner, and this story evaluates the rule, writes the selected firm and answers the case move** (GAP-2773, GAP-2778; ASM-4607, ASM-4612).
- The issue of the instruction, the pack sent with it and the partner clock: `RWB-S4-E5009-APP` and rwb-partner.
- The case of record, its route states `FIRM_SELECTION` and `FIRM_DECLINED`, the parent `CaseWorkflow` and the case timers: rwb-case (P3).
- The escalation of R-LIT-25 where no panel firm is available, and the nomination and panel-widening paths of R-LIT-26: the sibling stories of this service and the Head of Litigation path they own.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-23 and R-LIT-27, and their weights, thresholds and window: rwb-decision (P7), with the embedded runtime as a service-template capability (GAP-2777; ASM-4611).
- The pack and its documents: rwb-document (P5). The ACE score and batch facts, the freshness stamp of the data product and the interaction ledger: rwb-source-data (P1); VR-S4-008-1 is its check and MSG-P1-001 is carried here only (GAP-2779; ASM-4613).
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

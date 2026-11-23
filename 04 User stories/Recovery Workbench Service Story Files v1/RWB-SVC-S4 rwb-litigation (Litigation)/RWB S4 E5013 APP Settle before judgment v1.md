# RWB-S4-E5013-APP Settle before judgment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5013-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-013 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as the settlement step of `LitigationWorkflow` on task queue `rwb-litigation`; the agent proposal of R-LIT-36 is consumed on the rwb-agent contract, the treatment of R-LIT-37 is booked by rwb-treatment (S2) and the case move is answered to rwb-case (P3), so this story writes no `treatment` row, no `recovery_case` row and no column of `legal_action`; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the step acts (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 reads through the gateway-bff composite route (DP-19); the trigger, the cost-and-effect shape and the storage of the hold have no source specification and are declared as the working read of the assumptions (GAP-2798, GAP-2799, GAP-2800; ASM-4635 to ASM-4640). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the Workbench to take a settlement proposed during the case to the approver named by the delegated limit, to hold the litigation instead of withdrawing it when the settlement is approved, and to record the decision with the rule version before anything else changes**, so that **a case that can settle before judgment does so on an approved treatment with the court case still live, instead of a withdrawn action and a re-keyed settlement**.

This is the application slice of legacy RWB-E5-013. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the settlement step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-36, R-LIT-37 and R-LIT-38 on the proposal, on the D7.4 delegated limit and on the approval answer, with the LITIGATION package version in force;
- the stage states `IN_HEARING`, `SETTLEMENT_OFFERED_AT_COURT` and `LITIGATION_HELD`, reported to the case of record as a case move;
- `GET /legal-actions/{legalActionId}` (API-S4-003) and `POST /cases/{caseId}/legal-actions` (API-S4-002) on base `/api/recovery/litigation/v1` under capability area "Litigation" with the rights R and C (DP-13; TSD S4 T-A.1);
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the step acts (DP-03);
- the request to rwb-treatment (S2) that books the approved settlement, and the answer to rwb-case (P3) that carries the case move;
- SCR-19 Litigation workspace as this service's answer, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the settlement request and answer elements, the error set and the fakes, which are RWB-S4-E5013-CON; the treatment, its plan, its documents and its posting, which are rwb-treatment (S2); the approval named by the limit and the DoA matrix, which are rwb-decision (P7); the case of record and its route state, which are rwb-case (P3); the agent proposal of the next step, which is rwb-agent (P10); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-013 gave the Workbench one screen step that took a settlement proposed during the case to the approver named by the limit, booked the treatment when it was approved, and held the litigation rather than withdrawing it. The functional specification keeps the objective — "takes a settlement during the case to the approver named by the limit, and books it if approved" (FSD S4 A2.13) — and keeps the feature metric: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today. The program keeps the requirement: REQ-S4-006, "Settlement before judgment, an appeal and fee payment each need approval inside the delegation" (FSD S4 Requirements served).

What D-RCV-60 changes is where the four parts of the step live. In the monolith one process held the proposal, the treatment row, the approval, the case state and the decision log row in one `recovery` schema. In the target:

- **the proposal is the agent's.** R-LIT-36 says "the agent proposes the step with its cost and effect"; in the target the next-step proposal is an answer of rwb-agent (P10) consumed on its published contract, and this story routes it to the approver and never computes a cost or an effect of its own (GAP-2798; ASM-4635);
- **the approval is the decision service's.** "The approver named by the limit" is a delegated-authority approver of the DoA matrix, not a Litigation role row; the limit, the approver and the approval are governed in rwb-decision (P7) and consumed here as an answer (context pack slide 3 notes: an approver within their delegated authority, DoA Matrix v2; GAP-2800; ASM-4639);
- **the treatment stays with rwb-treatment (S2).** `treatment` and its plan are S2's rows: this story sends the booking request for the approved settlement and reads the answer, and writes no treatment row, no plan and no posting (GAP-2798; ASM-4635);
- **the case of record stays with rwb-case (P3).** `recovery_case` and its route state are P3's; `SETTLEMENT_OFFERED_AT_COURT` and `LITIGATION_HELD` are answered, never written here (GAP-2798; ASM-4638);
- **the litigation stage and the legal action stay with rwb-litigation (S4).** The stage states of the LITIGATION machine, the legal action, its court facts and the decision record are this service's, which is what legacy AC2 and AC3 assert;
- **the decision is recorded first**, in the same transaction as the stage change, which is what legacy AC1 asked for and what legacy AC4 tested.

The last change is the one the legacy wording makes explicit: **"hold the litigation rather than withdraw it."** `LOV-LEGAL-STATUS` has no held value, and no source gives a hold column, so the hold is a **stage state** (`LITIGATION_HELD`) answered to the case of record, and the legal action keeps its status `FILED` and is deliberately **not** set to `WITHDRAWN` — which is exactly R-LIT-37's instruction and the opposite of R-LIT-39, where a completed settlement withdraws the case (GAP-2799; ASM-4638). No column is added to express it.

The metric of the feature is unchanged and is the review of the settled files, so no business value moves: the D7.4 limit, the 3 and 2 working-day task timers and the state names are values in force in reference data and in the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S4-E5013-CON is published: the two operations, the settlement request and answer elements, the action status vocabulary, the error set and the fakes are baselined and handed to this story.
- The rwb-agent proposal contract is published with its fake, so the next-step proposal with its cost and effect can be read on Day 1. Neither it nor the other three consumed contracts is in this story's contract-dependency row, which is None, and the four rows are recorded as missing C dependencies (GAP-2798; ASM-4635, ASM-4636).
- The rwb-treatment booking contract of S2, the rwb-decision approval contract of P7 and the rwb-case case-move answer are available for their fakes. No source names a published operation for any of the three, so their names are Not specified in the source documents (GAP-2798; ASM-4636).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the stage change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 Litigation workspace reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` exists in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-014 and the standard record columns of TSD S4 T3.0; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version with R-LIT-36, R-LIT-37 and R-LIT-38 in it. The package, its rule rows and the D7.4 limit are authored, tested and approved in rwb-decision and loaded here on `RulePackageInForce`; this story declares none of them (GAP-2799; ASM-4639).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema, so a statement on `rwb_treatment`, `rwb_case` or `rwb_decision` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5013-CON when its tests pass.

### 4. Flow

1. The settlement is proposed during the case — by the customer, by the firm or by the officer on SCR-19. The proposal arrives at this service as a signal of `LitigationWorkflow` on task queue `rwb-litigation`; no source names its arrival, and no event and no Schedule is declared (GAP-2799; ASM-4637).
2. The step reads the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, `status` (DF-LEG-014), `lawsuit_no` (DF-LEG-005), `black_case_no` (DF-LEG-006), `court_name` (DF-LEG-008) and `claim_amount` (DF-LEG-009).
3. The step reads the proposal of rwb-agent (P10) on its contract: the next step, its cost and its effect. The proposal is read, never computed or re-worded here (R-LIT-36; GAP-2798; ASM-4635).
4. `SettlementOfferEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates R-LIT-36: a settlement proposed before judgment moves the stage to `SETTLEMENT_OFFERED_AT_COURT` and routes the proposal to the approver named by the D7.4 limit (FSD S4 A2.13.3.1; Business Rules and Routing Logic v4).
5. `SettlementDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the inputs reference and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
6. On approval, `SettlementOutcomeApplier` evaluates R-LIT-37 against the D7.4 limit and the approval answer: inside the limit, or with the committee's approval above it, the settlement is booked and the litigation is held.
7. The booking request goes to rwb-treatment (S2) with the case reference, the legal action reference, the approved settlement amount and the rule ID with its version; S2 writes the `treatment` row and its plan and answers the treatment reference. This service writes none of it (GAP-2798; ASM-4635).
8. The hold is applied on the stage: `LITIGATION_HELD`, with the legal action left at its status `FILED` and **not** withdrawn. No column of `legal_action` changes on this path (GAP-2799; ASM-4638).
9. `CaseMoveAnswer` answers rwb-case with the move `SETTLEMENT_OFFERED_AT_COURT` after step 4 and `LITIGATION_HELD` after step 8, with the rule ID, the version and the decided-at time. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-2798; ASM-4638).
10. On rejection with a reason, R-LIT-38 returns the stage to `IN_HEARING`, continues the case to judgment, records the reason and answers the same move to rwb-case; nothing is booked in rwb-treatment.
11. A repeated proposal or a repeated approval with the same case, action and offer reference writes nothing, sends no second booking request, sends no second case-move answer and counts the repeat.
12. SCR-19 Litigation workspace reads the action, its court facts and the stage outcome from this service through the gateway-bff composite route, read only, next to the case of rwb-case and the treatment of rwb-treatment (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the stage keeps its state, no booking request leaves the service and no case-move answer is sent | MSG-P7-003 | AC4, TC-E5-013-04, TC-E5-013-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | TC-E5-013-05 |
| X3 | The legal action does not exist or is outside the scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC2, AC3 |
| X4 | The legal action is already `CLOSED` or `WITHDRAWN`, or the stage is not the one the rule expects | 409 and nothing changes; the offer is not evaluated again on a closed action | None | AC2, AC3 |
| X5 | The agent proposal, the approval answer, the treatment booking or the case-move answer does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2, AC3 |
| X6 | The proposal is above the D7.4 limit and no committee approval is answered, or the approver rejects with a reason | Above the limit the step waits on the approval; on a rejection R-LIT-38 returns the stage to `IN_HEARING` and nothing is booked | None | AC2, AC3 |
| X7 | The same proposal, the same approval or the same offer reference arrives twice | One write, one booking request and one case-move answer; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | A component, a statement or a test reaches a `treatment` row, a `recovery_case` row, a `rule_row` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR3, BR5 |

X1 to X6 are the exception paths of RWB-E5-013 carried onto the split, X7 and X8 are the paths the target call types add, and X9 is the DP-01 boundary. The D7.4 limit of X6 and the task timers are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5013-CON and the four consumed fakes, on the tables of its own schema, and needs no live rwb-agent, rwb-treatment, rwb-decision or rwb-case |
| Negotiable | The activity names, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screens, the two operations and the state names are fixed |
| Valuable | A settlement before judgment is approved, booked and recorded in one step, and the case stays live in court instead of being withdrawn |
| Estimable | One workflow branch, one evaluator, one record write, one booking client, one case-move answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and approvals through the contract fakes, plus the component case of the access answer and the NFR case of the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Settle before judgment

  Background:
    Given case "RC-2026-000713" carries the filed civil-case legal action "LA-2026-000713" at the stage "IN_HEARING"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-36, R-LIT-37 and R-LIT-38
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Settle before judgment (legacy RWB-E5-013 AC1)
    Given the rwb-agent contract mock returns the step with its cost and effect for case "RC-2026-000713"
    Given the rwb-decision contract mock returns the approver at "D7.4" for case "RC-2026-000713"
    Given the rwb-treatment contract mock returns the treatment booked for case "RC-2026-000713"
    Given the rwb-case contract mock returns the case state "IN_HEARING" for "RC-2026-000713"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then takes a settlement during the case to the approver named by the limit, and books it if approved
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-36 (legacy RWB-E5-013 AC2)
    Given the rwb-agent contract mock returns the step with its cost and effect for case "RC-2026-000713"
    Given the rwb-case contract mock returns the case state "IN_HEARING" for "RC-2026-000713"
    Given a case in state IN_HEARING
    When settlement proposed
    Then the agent proposes the step with its cost and effect, and routes it to the approver
    Then the case moves to SETTLEMENT_OFFERED_AT_COURT

  Scenario: AC3 Rule R-LIT-37 (legacy RWB-E5-013 AC3)
    Given the rwb-decision contract mock returns the approval at "D7.4" for case "RC-2026-000713"
    Given the rwb-treatment contract mock returns the treatment booked for case "RC-2026-000713"
    Given the rwb-case contract mock returns the case state "SETTLEMENT_OFFERED_AT_COURT" for "RC-2026-000713"
    Given a case in state SETTLEMENT_OFFERED_AT_COURT
    When settlement approved
    Then book the treatment and hold the litigation rather than withdraw it
    Then the case moves to LITIGATION_HELD

  Scenario: AC4 Not recorded (legacy RWB-E5-013 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-013 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the lower-case opening of the third `Then`, the legacy wording of `the user acts on the screen`, `settlement proposed`, `settlement approved` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 to AC3 carry the `Given the <service> contract mock returns <x>` lines above, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in four places in the target: rwb-agent proposes the step with its cost and effect; rwb-decision names the approver and answers the approval at D7.4; rwb-treatment books the treatment; and this story holds the stage, records the decision with the rule version and answers the case move to rwb-case. The legacy `treatment` write is not reproduced here (GAP-2798; ASM-4635).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-36 | Litigation | D7 | IN_HEARING | SETTLEMENT_PROPOSED | the customer or the firm proposes a settlement before judgment | The agent proposes the step with its cost and effect, and routes it to the approver | SETTLEMENT_OFFERED_AT_COURT | Approver at D7.4 | Workbench, Committee View | 3 working days |
| R-LIT-37 | Litigation | D7 | SETTLEMENT_OFFERED_AT_COURT | SETTLEMENT_APPROVED | inside the D7.4 limit, or the committee approves above it | Book the treatment and hold the litigation rather than withdraw it | LITIGATION_HELD | Restructuring officer, FCR | Workbench, ALS core | 2 working days |
| R-LIT-38 | Litigation | D7 | SETTLEMENT_OFFERED_AT_COURT | SETTLEMENT_REJECTED | the approver rejects with a reason | Continue the case to judgment | IN_HEARING | Panel law firm | Workbench, Committee View | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the "Approver at D7.4" of R-LIT-36 and R-LIT-37 is a delegated-authority approver of the DoA matrix governed in rwb-decision, and the "Restructuring officer, FCR" of R-LIT-37 is the role that books the treatment in rwb-treatment (S2). The systems column names ALS core, which is posted by rwb-treatment and never by this service.

| ID | Rule | Source |
|---|---|---|
| BR1 | The settlement step and the legal action are this service's: the stage states `IN_HEARING`, `SETTLEMENT_OFFERED_AT_COURT` and `LITIGATION_HELD` are states of the LITIGATION machine on `LitigationWorkflow`, and the action facts read by the step are columns of `legal_action` in `rwb_litigation` | FSD S4 A2.13; TSD S4 T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision is recorded before the step acts, with the rule ID and the package version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-013 AC1 and AC4 |
| BR3 | The treatment stays with rwb-treatment: this story sends the booking request and reads the treatment reference, and writes no `treatment` row, no plan, no document and no posting | Ownership Map (treatment owner S2); TSD S4 T5.2; GAP-2798 |
| BR4 | The case move is answered and not written: `recovery_case` and the route states are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); GAP-2798 |
| BR5 | The litigation is held and **not withdrawn**: `legal_action.status` keeps `FILED` on this path and is never set to `WITHDRAWN` by this step, and no held value is added to `LOV-LEGAL-STATUS` | TSD S4 T3.2; R-LIT-37 and R-LIT-39 of the Business Rules and Routing Logic v4; GAP-2799 |
| BR6 | The approver and the limit are the decision service's: the step routes the proposal to the approver the DoA matrix names at D7.4 and reads the approval answer, and the limit is a value of the rule package and of reference data | GAP-2800; ASM-4639; context pack slide 3 notes (DoA Matrix v2) |
| BR7 | The same proposal, approval or offer reference twice writes once, sends one booking request, one case-move answer and one decision record, and counts the repeat | TSD S4 T-A.2; legacy AC1 |
| BR8 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case references, action references, codes, dates and amounts | Template and Rules v1 §R7.2 (s17); TSD S4 T6.2 |

**Where each rule lives in the target.** R-LIT-36 is the routing step: the proposal of rwb-agent is read, the approver of the DoA matrix is named by rwb-decision, the record is written and the stage and the case move go to `SETTLEMENT_OFFERED_AT_COURT`. R-LIT-37 is the booking step: inside the limit or with the committee's approval above it, rwb-treatment books the treatment, the stage moves to `LITIGATION_HELD`, the action stays `FILED` and the case move is answered. R-LIT-38 is the rejection step: the stage returns to `IN_HEARING`, the reason is recorded and nothing is booked. VR-S4-013-1 (pack incomplete at filing) and VR-S4-013-2 (prescription date near) of the FSD are carried in section 14 and belong to the pack and prescription stories of this service; no path of this story raises them (GAP-2799; ASM-4639).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story does own is the stage of `LitigationWorkflow` and the state of the step.

| From (stage of `LitigationWorkflow`) | Event | Condition | To |
|---|---|---|---|
| `IN_HEARING` | SETTLEMENT_PROPOSED under R-LIT-36 | A settlement is proposed before judgment | `SETTLEMENT_OFFERED_AT_COURT`, with the case-move answer `SETTLEMENT_OFFERED_AT_COURT` |
| `SETTLEMENT_OFFERED_AT_COURT` | SETTLEMENT_APPROVED under R-LIT-37 | Inside the D7.4 limit, or the committee approves above it | `LITIGATION_HELD`, with the case-move answer `LITIGATION_HELD` and the treatment booked by S2 |
| `SETTLEMENT_OFFERED_AT_COURT` | SETTLEMENT_REJECTED under R-LIT-38 | The approver rejects with a reason | `IN_HEARING`, with the case-move answer `IN_HEARING` and nothing booked |
| Any of the three | Any event | X4: the action is `CLOSED` or `WITHDRAWN`, or the stage is not the one the rule expects | Unchanged, refused with 409 |
| Any of the three | A proposal above the limit with no approval | X6 | Unchanged, waiting on the approval answer |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A proposal signal arrives for a case at `IN_HEARING` | The package in force is loaded | Evaluating |
| Evaluating | R-LIT-36 or R-LIT-38 fires | The decision record is written | Applying |
| Applying | The stage moves, the booking request is sent and the case-move answer leaves the service | The transaction commits | Waiting for the next signal |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Applying | The proposal is above the D7.4 limit | X6 | Waiting on the approval answer |

The legal action keeps its status: `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN (TSD S4 T3.2), the filed civil-case action stays `FILED` through `SETTLEMENT_OFFERED_AT_COURT` and `LITIGATION_HELD`, and the withdrawal belongs to R-LIT-39, where a completed settlement withdraws the case — a sibling story of this service, not this one. The hold therefore has no column and no list value, and that is deliberate (BR5; GAP-2799; ASM-4638).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix: the primary role of the feature, named by the FSD; records the proposal, reads the action and works the step on SCR-19 |
| RW-ENFORCE, enforcement owner | Litigation CRU: records the proposal and reads the action where the enforcement and the settlement run together |
| RW-HEADLIT, Head of Litigation | Litigation RA: read, and the also-user the FSD names for this feature |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Litigation RA: read, and the also-user the FSD names for this feature |
| RW-LEGAL, legal counsel | Litigation RA: reads the action, the proposal and the outcome; records no offer and no hold |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU: reads its own action and records the firm's proposal where the firm is the source, through the partner gateway |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record, holds the stage and answers the case move; it holds no grant on another schema |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The FSD names the Head of Litigation and the product head as also-users while the legacy permission table names only `C` on the feature, and both statements hold: the officer records the proposal, and the **approval** is not a Litigation right at all but a delegated-authority approval of the DoA matrix answered by rwb-decision (GAP-2800; ASM-4639). DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the record, the booking request and the case move |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the booking request and the case-move answer |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`: the filed action of this step is `CIVIL_CASE` |
| DF-LEG-005, DF-LEG-006, DF-LEG-008 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no, court_name | Read, as the court facts the offer and the hold are recorded against |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Read, as the amount sued for that the approved settlement is measured against |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read, and **never written on this path**: it keeps `FILED` and is not set to `WITHDRAWN` (BR5) |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by`, `is_active` | Not written by this story: no column of the action changes |
| DF-TRT-001 to DF-TRT-014 | treatment (S2, `rwb_treatment`) | id, case_id, decision_log_id, treatment_type, proposed_by, proposed_at and 8 more | Written by rwb-treatment on this story's booking request and read back as the treatment reference; never written, joined or stored here (BR3) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status and 18 more | Not read as a table and not written: the case and its route state come back on the case-move answer (BR4) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the stage changes (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule package in force and never as a table |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1, the legacy story Data table and the Logical Data Model and Data Dictionary v8. **No new table, no new column and no migration**: `legal_action` arrives with the DB story of this service, `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03), and the `treatment` row of the legacy data table is S2's (GAP-2798; ASM-4635). The test fixtures are synthetic: case `RC-2026-000713`, action `LA-2026-000713`, and an approved settlement inside the D7.4 limit.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S4-E5013-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The step reads the action on the GET. The POST is the operation through which the filed action of the case is opened by the sibling stories of this service, and this story declares it and does not create an action on the settlement path: the offer is a treatment of rwb-treatment (S2) and the hold is a stage state, so neither is a new action. Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-stage action, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the decision library, a consumed contract or the rule package does not answer. `PATCH /legal-actions/{legalActionId}` (API-S4-004) records filing, judgment and enforcement steps and belongs to the sibling stories; this story patches no column (BR5).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The next-step proposal (operation name Not specified in the source documents (GAP-2798; ASM-4636)) | rwb-agent (P10) | P10 rwb-agent | The step proposed with its cost and its effect for the case before judgment, which R-LIT-36 routes to the approver; read, never computed here; faked |
| The approval named by the limit (operation name Not specified in the source documents (GAP-2798; ASM-4636)) | rwb-decision (P7) | P7 rwb-decision | The approver the DoA matrix names at D7.4 and the approval or the rejection with its reason; the limit and the approver are P7's; faked |
| The booking of the approved settlement (operation name Not specified in the source documents (GAP-2798; ASM-4636)) | rwb-treatment (S2) | S2 rwb-treatment | The booking of the treatment for the approved settlement and the treatment reference it answers; the row, the plan and the posting are S2's; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2798; ASM-4635)) | rwb-case (P3) | P3 rwb-case | The move `SETTLEMENT_OFFERED_AT_COURT`, `LITIGATION_HELD` or `IN_HEARING` with the rule and its version; the row and the route state are P3's, and on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All four are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2798 with ASM-4635 and ASM-4636.

#### 12.3 Events published

None. The service's topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its ownership rows list no event of this service (context pack, ownership rows). DP-09 is not in this story's pattern set: the step writes no outbox row, its outputs are the local decision record of DP-03, the booking request and the case-move answer. A settlement booked by S2 is S2's fact on S2's topic, not this service's.

#### 12.4 Events consumed

None. The ownership rows of this service list no consumed event either, so the proposal arrives as a signal of `LitigationWorkflow` and the approval and the booking answers arrive on their owners' contracts of 12.2 (GAP-2799; ASM-4637). This story holds no consumer group, no subscription and no inbox of its own, and a build that adds a consumer to `rwb.litigation.events.v1` or a subscription to another topic fails the absence test of the CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the proposal, the approval answer and the rule package in force; outcome: the stage move for the parent |
| `routeSettlementOffer` | Activity, the routing step of this story | `rwb-litigation` | The case, the legal action and the proposal in; the rule ID with its package version, the approver and the case move out |
| `applySettlementHold` | Activity, the booking and hold step of this story | `rwb-litigation` | The approval answer in; the treatment reference of S2, the hold, the decision record and the case move out, in one transaction |

The agent's proposal is not an activity of this service: it is an answer of rwb-agent (P10) read on the owner's contract, and no model call is made here. The activity names are target design choices and are fixed by no source document; the trigger of the step is read as a proposal signal, because the legacy story says the user acts on the screen while R-LIT-36 names the customer or the firm as the source of the proposal (GAP-2799; ASM-4637). No cross-service call is made inside a workflow: each is an activity of the queue below.

#### 12.6 Schedules

None. The step runs from the proposal signal and from the approval answer the parent forwards. The 3 and 2 working-day task timers of R-LIT-36 and R-LIT-37 are durable timers of the workflow, not a Schedule; this story registers no Temporal Schedule, no Quartz row and no shared job table, and no Job of the batch catalogue is owned or moved here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read by this story and **not written**: the action keeps `FILED` and is not withdrawn (BR5) |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated proposal or approval and the answer it holds |

Not owned and never read as a table: `treatment` (S2), `recovery_case` (P3), `rule_row` and `decision_log_entry` (P7), `hearing` (S4, the sibling stories') and `document` (P5). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-agent proposal fake | The step with its cost and its effect for case `RC-2026-000713` before judgment; an answer beyond 2 s | AC1, AC2, X5 |
| rwb-decision approval fake | The approver at `D7.4` for case `RC-2026-000713`; an approval inside the limit, a committee approval above it and a rejection with a reason; no answer beyond 2 s | AC1, AC3, X6 |
| rwb-treatment booking fake | The treatment booked for case `RC-2026-000713` with its treatment reference, and a booking refused | AC1, AC3, X5 |
| rwb-case case-move fake | The case state `IN_HEARING` and `SETTLEMENT_OFFERED_AT_COURT` of case `RC-2026-000713`; the moves `SETTLEMENT_OFFERED_AT_COURT`, `LITIGATION_HELD` and `IN_HEARING` accepted, and a move refused because the case is not in the state the rule expects | AC1, AC2, AC3, X4 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 answer for case `RC-2026-000713`, with the legal action facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The four consumed rows carry the placeholder of 12.2 until their owners publish an operation name (GAP-2798; ASM-4636).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the agent proposal, the approval, the treatment booking and the case-move answer; one hop, 2 s each |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 2 activities | `LitigationWorkflow` with `routeSettlementOffer` and `applySettlementHold` on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `settlement`, Java package `th.co.scb.ace.workbench.recovery.litigation.settlement`; front end `src/modules/recovery/litigation/SettleBeforeJudgment.tsx`, the fragment SCR-19 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the stage change commit together or not at all, and the record is written before the booking request leaves the service. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-19 reaches this service, one hop through the gateway. DP-09 and DP-20 are not in the pattern set of this key, which is why no event is declared and why the agent proposal is a consumed contract of its owner rather than a client of this build (GAP-2798; ASM-4635).

**Dependencies the tables add and the plan does not hold.** The three H rows are the plan's. The four consumed contracts of 12.2 are class C dependencies in fact and are not in the metadata row, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2798 with ASM-4635 and ASM-4636.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` settlement branch | Workflow | The step that waits for the proposal, loads the package in force and reports the stage move to the parent |
| `routeSettlementOffer` | Activity | Reads the action and the proposal, evaluates R-LIT-36, writes the record and answers the move to `SETTLEMENT_OFFERED_AT_COURT` |
| `applySettlementHold` | Activity | Reads the approval answer, evaluates R-LIT-37 or R-LIT-38, requests the booking, writes the record and the stage move |
| `SettlementOfferEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the D7.4 limit and the state names of the LITIGATION machine |
| `SettlementDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `TreatmentBookingClient` | Client | The booking request of `S2` after R-LIT-37, one hop, 2 s, breaker, no retry of its own |
| `ApprovalClient` and `AgentProposalClient` | Client | The approver and the approval answer of P7 and the proposal of P10, one hop each |
| `CaseMoveAnswer` | Signal reporter | Answers rwb-case with the move, the rule and the version; it reports, it never changes a case row |
| `SettlementController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `SettleBeforeJudgment` | React component | Shows the proposal, its cost and effect, the approver and the outcome on SCR-19, read only, with the refusal states |

**Database and migrations.** No Flyway file. `legal_action` arrives with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the hold, the offer or the settlement amount: the hold is a stage state, the offer and its amount are S2's and the amount is a fact of the request (BR5; GAP-2799; ASM-4638).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants; no held value is added to either list.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the D7.4 limit and the 3 and 2 working-day timers are values of the package and of reference data, not of this build (GAP-2799; ASM-4639).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The settlement branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the proposal signal as its trigger (ASM-4637).
2. `AgentProposalClient` and `ApprovalClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, AC2, X5, X6).
3. `SettlementOfferEvaluator` over the LITIGATION package, with R-LIT-36, R-LIT-37 and R-LIT-38, the D7.4 limit and the no-fire path (AC2, AC3, X6).
4. `SettlementDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `TreatmentBookingClient` and the booking request after R-LIT-37, with the refused booking (AC3, X5).
6. `CaseMoveAnswer` and the parent signal, with the three moves (AC2, AC3).
7. `SettlementController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, X2, X3, X4).
8. `SettleBeforeJudgment` and SCR-19 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_litigation`, no write to `rwb_treatment`, `rwb_case` or `rwb_decision` (X9, BR3, BR4).

**Feature flag.** `rwb.litigation.settle-before-judgment-v1`, read as a flag of the platform library; off means the step holds the proposal, sends no booking request and answers no move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic proposal in SIT, R-LIT-36 and R-LIT-37 produce their record and their move, R-LIT-38 returns the stage to `IN_HEARING`, a repeated proposal writes once, a forced record failure changes nothing, no `treatment` row and no `recovery_case` row is written from this service, `legal_action.status` is never `WITHDRAWN` on this path, and SCR-19 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case (VR-S4-013-2), which is the prescription story of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid (X3, X4 of the contract) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads the legal action or records a proposal (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the stage changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-013 section 14 and of the FSD S4 A2.13 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X5) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No new screen is built in this story. One existing surface shows what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Pack; instructed; filed | The pack, the firm instruction and the filing of the sibling stories, and the action status `FILED`, read only |
| SCR-19 Litigation workspace | Hearing | The hearing dates of `hearing`, read only, and the proposal of this step with its cost and effect, the approver at D7.4 and the case at `SETTLEMENT_OFFERED_AT_COURT` |
| SCR-19 Litigation workspace | Judgment | The out-of-court settlement facts of the sibling stories, read only; the hold is shown as `LITIGATION_HELD` with the treatment reference of S2 |
| SCR-19 Litigation workspace | Held | The approved settlement, the treatment booked in rwb-treatment, the rule and its version, and the action still `FILED` — not withdrawn (BR5) |
| SCR-19 Litigation workspace | Rejected | The rejection reason, the return to `IN_HEARING` and nothing booked |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |

The legacy screen table names SCR-18 Notice approval for this feature, and that screen carries the states generated, approved, sent, delivered and unserved and no settlement state at all; it is carried here read-only as the notice context of the case and the step is worked on SCR-19 (GAP-2800; ASM-4640). The route merges this service's answer with rwb-case for the case and its route state and with rwb-treatment for the treatment; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-013-01 | AC1 | End to end | Settle before judgment |
| TC-E5-013-02 | AC2 | End to end | Rule R-LIT-36 |
| TC-E5-013-03 | AC3 | End to end | Rule R-LIT-37 |
| TC-E5-013-04 | AC4 | Component | Not recorded |
| TC-E5-013-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-013-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3, the "System" level of the sibling legacy stories) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The agent, approval, treatment-booking and case-move fakes of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000713`, action `LA-2026-000713`, an approved settlement inside the D7.4 limit and a treatment booked by S2 — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the D7.4 limit, the 3 and 2 working-day timers, the lists and the message texts are values and reference rows with a version; no list value, state name, limit or date appears in Java.
- No personal data in logs, workflow inputs, prompts or the fixture: the rows carry case references, action references, codes, dates and amounts only, and the test data is synthetic.
- The treatment stays with rwb-treatment: no `treatment` row, no plan, no document and no posting is written here (BR3).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR4).
- The litigation is held and never withdrawn by this step: `status` keeps `FILED`, no held value is added to `LOV-LEGAL-STATUS` and no column is added to express it (BR5).
- The cost and the effect of the proposal are the agent's: no model call is made here and no amount is computed here (GAP-2798).
- ACE data only through its owner: no component of this story reads a `v_ace_*` view or an ACE table, and the feature needs none (DP-05 as a rule, not a pattern of this key).
- No read of another service's tables and no cross-schema join: `treatment`, `recovery_case`, `rule_row`, `decision_log_entry` and `document` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second booking.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing (12.3, 12.4).
- SCR-19 is read only; the proposal action posts through the service and the approval is the decision service's.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-006 | Settlement before judgment, an appeal and fee payment each need approval inside the delegation, which this story does by routing the proposal to the approver the DoA matrix names at D7.4, holding the litigation on approval and recording the decision (FSD S4 Requirements served) | FEAT-LIT-13 | 08 Litigate and enforce | R-LIT-36, R-LIT-37, R-LIT-38 | TC-E5-013-01, TC-E5-013-02, TC-E5-013-03 |

The legacy story master of RWB-E5-013 carries no requirement ID; the trace is the requirement the FSD S4 serves for the settlement, the appeal and the fee approval of the same feature set.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-013 | The four legacy criteria word for word, the three rules, the two screens, the messages and the six test cases; the `treatment` write of the legacy data table is S2's and no `treatment` row is written here |
| RWB-S4-E5013-CON | H: the two operations, the settlement request and answer elements, the error set and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 |
| rwb-agent (P10), rwb-decision (P7), rwb-treatment (S2) and rwb-case (P3) contracts | C in fact and not in the metadata row: the proposal, the approval, the booking and the case move, faked (GAP-2798) |
| FEAT-LIT-13, SCR-19, SCR-18 | The feature and the two screens of the legacy story; SCR-18 is read-only context (GAP-2800) |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Temporal layer with Schedules for batch and durable timers for the step, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-agent, rwb-decision, rwb-treatment and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the two operations, the settlement request and answer elements, the error set and the fakes: RWB-S4-E5013-CON.
- The next-step proposal with its cost and its effect, and the model that produces it: rwb-agent (P10), whose contract is consumed here and whose build is RWB-P10-TE013-APP.
- The DoA matrix, the D7.4 limit, the approver and the approval answer: rwb-decision (P7); this story routes the proposal and reads the answer (GAP-2800; ASM-4639).
- The treatment of the approved settlement, its plan, its documents, its posting and its completion: rwb-treatment (S2), which books the row on this story's request. **The treatment is booked by rwb-treatment** (GAP-2798; ASM-4635).
- The case of record, its route state and the parent `CaseWorkflow`: rwb-case (P3), whose case-move answer this story sends and never writes.
- The withdrawal of the case on a completed settlement (R-LIT-39), the appeal (R-LIT-46 to R-LIT-49), the fee approval (R-LIT-41) and the judgment (R-LIT-44): the sibling stories of this service.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-36, R-LIT-37 and R-LIT-38: rwb-decision (P7), with the embedded runtime as a service-template capability (GAP-2799; ASM-4639).
- The pack, the filing, the hearings and the prescription warning: the pack, filing and hearing stories of this service.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-18: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

# RWB-S4-E5012-APP Recommend the next litigation step

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-012 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-M |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5012-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-012 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the rule that proposes the next step is the LITIGATION package of rwb-decision (P7) and the cost and effect of a step come from rwb-agent (P10) with the rule as fallback; the case move and the officer task are answered to rwb-case (P3), the template status of R-LIT-04 and the notice are rwb-comms (P6), the pack index is rwb-document (P5); the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before anything changes (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-18 and SCR-19 read through the gateway-bff composite route (DP-19); the recommendation has no table, no operation and no vocabulary in any source (GAP-2793 to -5; ASM-4631 to -5). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5012-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer**, I want **the Workbench to propose the next step with reasons, for the officer or the approver to decide**, so that **cases reach court faster with complete packs**.

This is the application slice of legacy RWB-E5-012 and it owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens, data rows and test cases they depend on;
- the next-step step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case;
- the evaluation of R-LIT-04 and R-LIT-16 and the reading of the LITIGATION package version in force, with the reasons the proposal carries: the rule, its condition and the facts that satisfied it;
- the cost and the effect of the proposed step, read on rwb-agent's contract under R-LIT-36 with the rule as fallback when the agent answers nothing;
- the local decision record of the proposal, written through RWB-PLT-E1027-CON before anything changes (DP-03);
- the answer to rwb-case for the case move, the case-stage timer and the officer task, and the answer to rwb-comms that holds the notice generation under R-LIT-04;
- the two surfaces SCR-18 Notice approval in its generated and blocked states and SCR-19 Litigation workspace in its pack state, as this service's answers through the gateway-bff composite route (DP-19).

It does not own: the shape of the consumed facts, the recommendation element, the reasons and the errors, which are RWB-S4-E5012-CON; the case of record, its route state, the parent `CaseWorkflow`, the officer task and the case-stage timer, which are rwb-case (P3); the notice, its template and its template status, which are rwb-comms (P6); the document index and the pack documents, which are rwb-document (P5); the rule rows, the package and the version that governs them, which are rwb-decision (P7); the model that writes the reasons, which is rwb-agent (P10); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-012 put a proposal in front of the officer instead of an empty screen: the litigation journey is long and rule-bound, so the Workbench named the next step, said why, and left the decision to the officer or to the approver the delegation names. It carried two rule outcomes — R-LIT-04 held notice generation and raised a task when the template was withdrawn, and R-LIT-16 presented a complete pack for verification — plus R-LIT-36, where the agent proposes a step with its cost and effect before judgment. The functional specification keeps the objective and its metric: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today (FSD S4 A2.12.1).

What D-RCV-60 changes is who owns each fact of the step. In the monolith the case row, the task row, the notice row, the rule row and the decision log row sat in one `recovery` schema and one process. In the target:

- **the case, its route state and the officer task are rwb-case (P3).** `recovery_case` and `task` (DF-WRK-017 to DF-WRK-026) are P3's; this story answers the move `NOTICE_BLOCKED` or `PACK_VERIFIED`, the case-stage timer and the officer task, and writes no case row and no task row;
- **the notice and its template are rwb-comms (P6).** `notice` (DF-LEG-015 to DF-LEG-023) is P6's row and the template status of R-LIT-04 is a fact of the template, not of this schema; this story reads it and answers a hold, it never writes it;
- **the pack index is rwb-document (P5).** The defect list item of R-LIT-16 is a document of the pack, and TSD S4 T5.2 gives documents to P5; this story reads the index and decides;
- **the rules are rwb-decision's (P7) and the runtime is embedded.** The proposal is decided by the LITIGATION package at its version in force, so the reasons are a rule ID, a condition and the facts behind it, not a sentence a developer wrote (GAP-2797; ASM-4568);
- **the cost and the effect come from rwb-agent (P10).** R-LIT-36 says the agent proposes the step with its cost and its effect, and the FSD names the Model gateway as an integration point; the agent is a non-blocking contract with a fake, and when it does not answer the rule's own proposal stands (GAP-2793; ASM-4631);
- **the proposal is not a business row.** No owned table of this service carries a recommendation: `legal_action` (DF-LEG-001 to DF-LEG-014) has no such field and `hearing` has none. The proposal lives in the decision record, in the workflow state and in the task request, which is what legacy AC1 asked for ("the result to the decision log with the rule version") and what legacy AC4 tested.

The step is not carried by an event. The pack gives this service zero events, DP-09 is not in its pattern set, and the legacy trigger wording — "a completed ACE batch, an event or a timer" — is read as the workflow signals of this service's own pack and hearing steps (GAP-2794; ASM-4632).

### 3. Preconditions

- RWB-S4-E5012-CON is published: the recommendation element, its reasons, the cost-and-effect element, the case read and answer, the template read, the pack read, the decision-record element, the error set and the fakes are baselined and handed to this story.
- The rwb-case contract that reads the case route state and answers the move, the case-stage timer and the officer task is available with its fake; the operation names are Not specified in the source documents (GAP-2794; ASM-4632).
- The rwb-comms contract that answers the notice and its template status is available with its fake; the template status has no owner field and no published operation in any source read for this key (GAP-2795; ASM-4633).
- The rwb-document pack-index read is available with its fake: the document index of the case and the defect list items it holds (TSD S4 T5.2, "P5 for documents"). The operation name is Not specified in the source documents (GAP-2795; ASM-4633).
- The rwb-agent recommendation read is available with its fake: the cost and the effect of the proposed step, and a no-answer path that leaves the rule's own proposal standing (GAP-2793; ASM-4631).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-18 and SCR-19 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The LITIGATION rule package is in force at its version with R-LIT-04, R-LIT-16 and R-LIT-36 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce` (GAP-2797; ASM-4568).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_comms`, `rwb_document` or `rwb_decision` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5012-CON when its tests pass.

### 4. Flow

1. A step of the same service raises the signal that the step waits for: the pack-complete result of the pack and defect-list steps (FEAT-LIT-04, FEAT-LIT-05) or the withdrawal of the notice template; a repeated signal for the same case, state and payload is counted and changes nothing (GAP-2794; ASM-4632).
2. The next-step step of `LitigationWorkflow` on queue `rwb-litigation` reads the case on the rwb-case contract: the case reference, its route state (`NOTICE_GENERATED`, `PACK_ASSEMBLY` and the other LIT states), the stage and the legal action of the case.
3. The step reads what the candidate rules need: the notice and its template status on rwb-comms (R-LIT-04), and the document index of the pack on rwb-document (R-LIT-16).
4. `NextStepEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates the rules whose from-state and condition the facts satisfy.
5. `AgentCostEffectClient` asks rwb-agent for the cost and the effect of the proposed step; when the agent does not answer inside 2 s or its confidence check fails, the proposal stands on the rule alone and the step records which of the two answered.
6. `RecommendationBuilder` composes the proposal: the next step the rule names, the reasons (the rule ID, its condition and the facts that satisfied it), the cost and effect, the role that must decide — the litigation officer under R-LIT-04 and R-LIT-16, the approver at D7.4 under R-LIT-36 — and the rule's own clock (1 working day under R-LIT-04, 2 working days under R-LIT-16).
7. `RecommendationDecisionRecordWriter` writes one decision record through the local decision-record library **before any change**: the case and legal-action references, the rule ID with its package version, the inputs reference, the proposal, the cost and effect with its source, and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. Under R-LIT-04 the step answers rwb-case the move `NOTICE_BLOCKED`, the case-stage timer of 1 working day and the officer task, and answers rwb-comms that the generation is held for the case, naming the rule and its version.
9. Under R-LIT-16 the step answers rwb-case the move `PACK_VERIFIED`, the case-stage timer of 2 working days and the officer task to verify the pack, and sets its own state to `PACK_VERIFIED`.
10. When no rule fires the step writes no record, answers no move, raises no task and keeps the case where it is; the proposal of the nearest open step is offered to the screen as a read of the rule rows and not as a decision.
11. SCR-18 Notice approval shows the generated and blocked states and SCR-19 Litigation workspace shows the pack state with the proposal, its reasons and its cost and effect, read only through the gateway-bff composite route (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: no move is answered, no task is raised and the case keeps its state | MSG-P7-003 | AC4, TC-E5-012-04, TC-E5-012-06 |
| X2 | A role without the Litigation right opens the proposal on a screen, or decides it without right A | The read or the decision is refused at the edge before any service call; nothing changes | MSG-P4-002 | TC-E5-012-05 |
| X3 | The case is in a state that no candidate rule names | No rule fires: nothing changes and no record is written (step 10) | None | AC1 |
| X4 | The case, the notice or the pack is unknown to its owner or outside the caller's scope | 404 on the read; the step stops and nothing is written | None | AC1, AC2, AC3 |
| X5 | A consumed contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered | None | AC1, AC3 |
| X6 | rwb-agent answers nothing or fails its confidence check | The proposal stands on the rule alone, the source of the cost and effect is recorded as the rule and the step continues (step 5) | None | AC1 |
| X7 | The template status of R-LIT-04 cannot be read for the product and notice type | R-LIT-04 does not fire, no task is raised and the case keeps `NOTICE_GENERATED`; the step waits on the fact | None | AC2 |
| X8 | A required field of the read, the proposal or the answer is absent or invalid | The step stops with nothing changed and the field is named | MSG-GEN-001 | AC1, AC2, AC3 |
| X9 | The same signal arrives twice for the same case, state and payload | One record, one move, one task; the repeat is counted | None | AC1, AC2, AC3 |
| X10 | A component, a statement or a test reaches a `notice` row, a `recovery_case` row, a `task` row, a `rule_row` or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR7 |

X1 to X4 are the exception paths of RWB-E5-012 carried onto the split, X5 to X9 are the paths the target call types add, and X10 is the DP-01 boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5012-CON and the fakes of rwb-case, rwb-comms, rwb-document, rwb-decision and rwb-agent, on its own schema, and needs no live service. The hearing facts of FEAT-LIT-11 (RWB-S4-E5011-APP) reach the step as a signal of the same workflow, so the plan's H rows name no in-lane predecessor |
| Negotiable | The activity name, the state names of the step and the shape of the case answer are this story's choice; the rules, the messages, the screens, the moves and the officer tasks are fixed |
| Valuable | The officer sees the next step with the rule and the facts behind it, one click from the decision, and neither the case nor the notice is written by this service |
| Estimable | One workflow step, one evaluator, one agent client, one record write, one case answer and two read-only screen fragments |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, notices and pack indexes through the contract fakes, plus the component cases of the refused right and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Recommend the next litigation step

  Background:
    Given case "RC-2026-001212" carries the legal action "LA-2026-001212"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-04, R-LIT-16 and R-LIT-36
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Recommend the next litigation step (legacy RWB-E5-012 AC1)
    Given the rwb-case contract mock returns the case "RC-2026-001212" in state PACK_ASSEMBLY
    Given the rwb-agent contract mock returns the cost and the effect of the proposed step
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then proposes the next step with reasons, for the officer or the approver to decide
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-04 (legacy RWB-E5-012 AC2)
    Given the rwb-case contract mock returns the case "RC-2026-001212" in state NOTICE_GENERATED
    Given the rwb-comms contract mock returns the notice "NTC-2026-001212" of the case with template status withdrawn
    Given a case in state NOTICE_GENERATED
    When template withdrawn
    Then hold generation and raise a task to the litigation officer
    Then the case moves to NOTICE_BLOCKED

  Scenario: AC3 Rule R-LIT-16 (legacy RWB-E5-012 AC3)
    Given the rwb-case contract mock returns the case "RC-2026-001212" in state PACK_ASSEMBLY
    Given the rwb-document contract mock returns the document index of the case with every defect list item present
    Given a case in state PACK_ASSEMBLY
    When pack complete
    Then present the pack to the litigation officer for verification
    Then the case moves to PACK_VERIFIED

  Scenario: AC4 Not recorded (legacy RWB-E5-012 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-012 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `its trigger arrives`, `template withdrawn` and `pack complete` all stand. The cross-service parts are mocked, so AC1 to AC3 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions. What the legacy lines describe happens in four places in the target: rwb-case holds the case, its move and the officer task, rwb-comms holds the notice and its template status, rwb-document holds the pack, and this story evaluates the rule, writes the record and answers the move.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-04 | Litigation | D7 | NOTICE_GENERATED | TEMPLATE_WITHDRAWN | template_status = withdrawn | Hold generation and raise a task to the litigation officer | NOTICE_BLOCKED | Litigation officer | Workbench, the Workbench document hub | 1 working day |
| R-LIT-16 | Litigation | D7 | PACK_ASSEMBLY | PACK_COMPLETE | every defect list item present | Present the pack to the litigation officer for verification | PACK_VERIFIED | Litigation officer | Document Hub, CCMS, LHS, the Workbench document hub | 2 working days |
| R-LIT-36 | Litigation | D7 | IN_HEARING | SETTLEMENT_PROPOSED | the customer or the firm proposes a settlement before judgment | The agent proposes the step with its cost and effect, and routes it to the approver | SETTLEMENT_OFFERED_AT_COURT | Approver at D7.4 | Workbench, Committee View | 3 working days |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business: the litigation officer who receives the task of R-LIT-04 and R-LIT-16, and the approver at D7.4 who decides the settlement step of R-LIT-36. The systems column maps to the target as follows: the Workbench is this service and its screens, the Workbench document hub and CCMS and LHS and the Document Hub are rwb-document (P5) and rwb-comms (P6), and the Committee View is the approver screen of rwb-access and the edge.

| ID | Rule | Source |
|---|---|---|
| BR1 | The next-step step of the litigation journey is this service's: the evaluation of R-LIT-04, R-LIT-16 and R-LIT-36, the reasons, the cost and effect and the decision record are `rwb_litigation` objects and workflow state, and no other service evaluates them | Architecture v5 slide 41 (rwb-litigation owns litigation, hearings, judgments, enforcement); context pack ownership rows (workflow `LitigationWorkflow`, queue `rwb-litigation`); FSD S4 A2.12.3.1 |
| BR2 | The decision is recorded before anything changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy RWB-E5-012 AC1 and AC4 |
| BR3 | The case move, the route states `NOTICE_BLOCKED` and `PACK_VERIFIED`, the case-stage timer and the officer task stay with rwb-case (P3); this story answers them and writes no case row and no task row | Context pack (workflow ownership and the case of record); TSD S4 T5.2 ("P3 for the case"); GAP-2794 |
| BR4 | The notice, its template and its template status stay with rwb-comms (P6); this story reads them and answers a hold, and writes none of them | Context pack (ownership rows of S4 name `hearing` and `legal_action` only); Architecture v5 slide 10 ("Notices — rwb-comms"); GAP-2795 |
| BR5 | The defect list items of the pack are documents of rwb-document (P5); this story reads the index and never a document, a blob or a document row | TSD S4 T5.2 ("P5 for documents"); TSD S4 T-A.1; FSD S4 A2.12 |
| BR6 | The cost and the effect of a proposed step are read on rwb-agent's contract; when the agent does not answer, the rule's own proposal stands and the record says so | Business Rules and Routing Logic v4 R-LIT-36; FSD S4 A2.12.2 ("Integration points. Workbench, Model gateway"); Architecture v5 slide 5 (agent with rule fallback); GAP-2793 |
| BR7 | No table of another service is read or written and no cross-schema join is made: the case, the notice, the pack and the rules are reached only through their owners' contracts | DP-01; context pack (ACE data only through the owner's contract or `v_ace_*` views) |
| BR8 | The same signal twice writes once, answers once, raises one task and counts the repeat | TSD S4 T-A.2 (idempotency rule of the write paths); Architecture v5 slide 11 |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case references, codes, dates, a rule version and a proposal of step names | Template and Rules v1 §R7.2 (s17); FSD S4 A2.12 field catalogue |

**Where each rule lives in the target.** R-LIT-04 holds generation, answers `NOTICE_BLOCKED` with the officer task and the 1-working-day clock. R-LIT-16 presents the pack, answers `PACK_VERIFIED` with the officer task and the 2-working-day clock. R-LIT-36 composes the settlement proposal with the agent's cost and effect and routes it to the approver at D7.4 with the 3-working-day clock; its case move `SETTLEMENT_OFFERED_AT_COURT` is answered and written by rwb-case when the approver decides. VR-S4-012-1 of the FSD tests the freshness of the ACE batch of the source and raises MSG-P1-001; this service holds no ACE batch status read, so the check belongs to the owner of the data product and the message is carried in section 14 without a path here.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3).

| From (case route state) | Event | Condition | To (answered, written by rwb-case) |
|---|---|---|---|
| NOTICE_GENERATED | TEMPLATE_WITHDRAWN under R-LIT-04 | template_status = withdrawn | `NOTICE_BLOCKED`, with the 1-working-day case-stage timer and the officer task |
| PACK_ASSEMBLY | PACK_COMPLETE under R-LIT-16 | every defect list item present | `PACK_VERIFIED`, with the 2-working-day case-stage timer and the officer task to verify the pack |
| IN_HEARING | SETTLEMENT_PROPOSED under R-LIT-36 | the customer or the firm proposes a settlement before judgment | `SETTLEMENT_OFFERED_AT_COURT`, answered only when the approver at D7.4 decides |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The pack-complete or the template-withdrawn signal arrives | The case, the notice and the pack index are read | Evaluating |
| Evaluating | A candidate rule fires | The agent answer or its fallback is in hand | Recording |
| Recording | The decision record is written | The case answer and the notice answer are accepted | Waiting for the next signal |
| Recording | The record write, the answer or the timer fails | X1, X5, X8 | Waiting, nothing changed |

No column of this service changes on the case in this story: `legal_action` is read for the case reference and its pack, and the durable state of the step is the workflow state and the rule's own clock.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-litigation service identity | Runs the step, evaluates the rules, asks the agent, writes the decision record and answers the case move, the timer, the officer task and the notice hold; it holds no grant on another schema |
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix and the role of the task under R-LIT-04 and R-LIT-16: receives the proposal, verifies the pack and decides the step |
| RW-ENFORCE, enforcement owner | Litigation CRU: reads the proposal of a case in scope and takes the enforcement steps |
| RW-LEGAL, RW-PRODHEAD, RW-HEADLIT | Litigation RA: read the proposal and decide it inside their delegation (right A of the legacy permission table) |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU as TSD S4 T6.1 gives it: no part of this step is taken by a firm user |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it; the service identities run the step and are subject to the same checks |

The FSD declares the feature "runs unattended" with the litigation officer as also-user, and both statements hold: the step composes the proposal under the service identity, and the officer or the approver decides it with right A. The legacy permission table gives right A to RW-LITOFF, RW-LEGAL, RW-PRODHEAD and RW-HEADLIT and right C to RW-LITOFF and RW-ENFORCE, which is the matrix used on the two surfaces. DP-08 is not in this story's pattern set: the right is declared per operation on the contract and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Read as the case and its route state on the rwb-case answer, and never written |
| DF-WRK-017 to DF-WRK-026 | task (P3, `rwb_case`) | id, case_id, task_code, element_type, discretion, status and 4 more | Not written: the officer task is answered to rwb-case, which writes the row |
| DF-LEG-001 to DF-LEG-014 | legal_action (S4, `rwb_litigation`) | id, case_id, law_firm_id, action_type, lawsuit_no, black_case_no and 8 more | Read for the case reference and the pack; no column of the recommendation is added |
| DF-LEG-015 to DF-LEG-023 | notice (P6, `rwb_comms`) | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | Read only on the P6 contract: the notice, its type and its template status, whose field identifier is Not specified in the source documents (GAP-2795; ASM-4633) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before anything changes |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | id, rule_id, rule_version, route_set and 11 more | Read as the LITIGATION package in force, never written |
| No published field ID for the pack index | document index (P5, `rwb_document`) | the documents of the case and the defect list items | Read only on the P5 contract; the recommendation itself has no field identifier (GAP-2793; ASM-4631) |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1 and the legacy data table of RWB-E5-012. **No new table, no new column and no migration**: this story writes no business row, `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). `recovery_case` and `task` (P3), `notice` (P6), `document` (P5) and `rule_row` and `decision_log_entry` (P7) are not created, not written and not read as tables.

**No personal data.** The rows and the record carry identifiers, dates, list values, step names and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input; the fixture of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The next-step step publishes no operation of its own: it is an unattended workflow step and the ownership rows give rwb-litigation five operations (API-S4-001 to API-S4-005, TSD S4 T-A.1), none of which proposes a step. The proposal reaches the screens as an element of the answer of API-S4-003 `GET /legal-actions/{legalActionId}` — an owned operation of this service, first in E5, whose shape the legal-action story of this key family fixes — and this story adds no sixth operation (GAP-2793; ASM-4631).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2794; ASM-4632)) | `/api/recovery/case/v1` | P3 rwb-case | The case, its route state `NOTICE_GENERATED` or `PACK_ASSEMBLY`, its stage and its legal action; faked |
| The case-stage answer (operation name Not specified in the source documents (GAP-2794; ASM-4632)) | rwb-case (P3) | P3 rwb-case | The move `NOTICE_BLOCKED` or `PACK_VERIFIED`, the case-stage timer of 1 or 2 working days, the officer task and the rule ID with its version; faked |
| The notice and template read (operation name Not specified in the source documents (GAP-2795; ASM-4633)) | `/api/recovery/comms/v1` | P6 rwb-comms | The notice of the case and its template status for R-LIT-04; faked |
| The notice hold (operation name Not specified in the source documents (GAP-2795; ASM-4633)) | `/api/recovery/comms/v1` | P6 rwb-comms | The hold on generation for the case under R-LIT-04, with the rule and its version; faked |
| The pack-index read (operation name Not specified in the source documents (GAP-2793; ASM-4631)) | `/api/recovery/document/v1` | P5 rwb-document | The document index of the case and the defect list items of R-LIT-16; faked |
| The rule package read (operation name Not specified in the source documents (GAP-2797; ASM-4568)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version in force with R-LIT-04, R-LIT-16 and R-LIT-36; faked |
| The cost-and-effect read (operation name Not specified in the source documents (GAP-2793; ASM-4631)) | `/api/recovery/agent/v1` | P10 rwb-agent | The cost and the effect of the proposed step under R-LIT-36, with a no-answer path that leaves the rule's proposal standing; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All seven rows are contract dependencies of class C in fact that this story's metadata row does not carry, because the plan's C row is None; the two platform rows of the pattern set (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are its only H rows beside its own contract (GAP-2793, GAP-2794, GAP-2795, GAP-2797).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of this service publish zero events. DP-09 is not in this story's pattern set, so it writes no outbox row and widens no topic; the only record it relays is the local decision record on the shared `rwb.decision-record.v1` of DP-03, which is the library's topic and not an event of this service (GAP-2794; ASM-4632).

#### 12.4 Events consumed

None. `TEMPLATE_WITHDRAWN`, `PACK_COMPLETE` and `SETTLEMENT_PROPOSED` are the event names of the state machine and the names of the workflow signals that start the rules, not Kafka subscriptions: this service has no consumer group, no subscription and no inbox of its own. The pack-complete and template-withdrawn signals are raised inside this service's workflow, the case and the notice arrive on their owners' contracts, and the agent answer is synchronous (GAP-2794; ASM-4632).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4 and the legal action; signals: the pack-complete result, the template-withdrawn result, the case state answered by rwb-case, the rule package in force; the rule's own clock as a durable timer |
| `recommendNextStep` | Activity, the one next-step step of this story | `rwb-litigation` | The case, the notice, the pack index and the agent answer in; the proposal with its reasons, the cost and effect with its source, the rule ID with its package version and the case move out, with the decision record written in the same transaction |

The activity name and the workflow state names are target design choices of this story and are fixed by no source document; the trigger of the step is read as the arrival of a pack-complete or a template-withdrawn signal for a case in `PACK_ASSEMBLY` or `NOTICE_GENERATED`, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2794; ASM-4632). No job of Architecture v5 is owned or registered here.

#### 12.6 Schedules

None. The two clocks of the rules — 1 working day under R-LIT-04 and 2 working days under R-LIT-16, with 3 working days under R-LIT-36 — are durable timers of `LitigationWorkflow` and are answered to rwb-case as the case-stage timer. No Temporal Schedule, no Quartz row and no shared job table is declared, and no batch window is read or set by this story (GAP-2794; ASM-4632).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | This service's action row; read for the case reference and the pack, no column added |
| hearing | S4 (`rwb_litigation`) | This service's hearing row; not touched by this story |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the proposal (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated signal |

Not owned and never read as a table: `recovery_case` and `task` (P3), `notice` (P6), `document` (P5), `rule_row` and `decision_log_entry` (P7), and every `v_ace_*` view (P1). No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case fake | Case `RC-2026-001212` in `NOTICE_GENERATED` and in `PACK_ASSEMBLY`, a case in another state, the moves `NOTICE_BLOCKED` and `PACK_VERIFIED` accepted and a move refused | AC1, AC2, AC3, X3, X4 |
| rwb-comms fake | Notice `NTC-2026-001212` of the case with template status withdrawn and with a current template, the hold accepted, and an unknown notice | AC2, X4, X7 |
| rwb-document fake | The document index of the case with every defect list item present, with one item missing, and no answer beyond 2 s | AC3, X5 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-04, R-LIT-16 and R-LIT-36, and a package at a second version | AC1, AC2, AC3 |
| rwb-agent fake | The cost and the effect of the proposed step, a low-confidence answer, and no answer | AC1, X6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-18 and SCR-19 answer for case `RC-2026-001212`, with the proposal read once | AC1, AC3 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the seven consumed rows, the template-status field and the step vocabulary of the proposal carry the placeholder until their owners confirm them (GAP-2793, GAP-2794, GAP-2795, GAP-2797).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 7 consumed | The case read, the case-stage answer, the notice and template read, the notice hold, the pack-index read, the rule package read and the agent read; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity, 3 rule clocks | `LitigationWorkflow`, `recommendNextStep`, the 1-, 2- and 3-working-day clocks; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `recommendation`, Java package `th.co.scb.ace.workbench.recovery.litigation.recommendation`; front end `src/modules/recovery/litigation/NextStep.tsx`, the fragment SCR-18 and SCR-19 embed, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the case answer, the notice hold and the timer commit together or not at all. DP-13 fixes the base of this service and this story provides no operation on it. DP-19 is how SCR-18 and SCR-19 reach this service, one hop through the gateway. DP-09 and DP-14 are outside the pattern set, so nothing is published or consumed; DP-20 is not in the set either, and the agent row of 12.2 is a consumed contract the C row does not carry (GAP-2793).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan already carries. The seven consumed contracts are class C in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-2793, GAP-2794, GAP-2795, GAP-2797).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` next-step branch | Workflow | The stage that waits for the pack-complete or template-withdrawn signal, holds the rule's clock and reports the outcome to the parent |
| `recommendNextStep` | Activity | The one step: read the case, the notice and the pack index, evaluate the rules, ask the agent, write the record and answer the case and the notice |
| `NextStepEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the candidate set and the no-fire path |
| `AgentCostEffectClient` | Client | The cost-and-effect read on the P10 contract, one hop, 2 s, breaker, and the fallback that keeps the rule's proposal |
| `RecommendationBuilder` | Service | The proposal: the step, the reasons, the cost and effect with its source, the deciding role and the clock |
| `RecommendationDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before anything changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `CaseAnswer` | Client and signal reporter | The case read and the case-stage answer to rwb-case, with the move, the timer and the officer task |
| `NoticeHoldClient` | Client | The hold on generation to rwb-comms under R-LIT-04 and the notice read of the same call |
| `NextStep` | React component | Shows the proposal, its reasons and its cost and effect on SCR-18 and SCR-19, read only, with the refusal, failure and fallback states |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). This story writes no business row, so no column is added for the proposal, the reasons or the cost: they are facts of the decision record, and storing them would duplicate a rule version and an agent answer in this schema (GAP-2793).

**Configuration and reference data.**

- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce` (GAP-2797).
- The step vocabulary the proposal uses, read as reference data with a version and never as a constant; its content is Not specified in the source documents (GAP-2793; ASM-4631).
- The agent threshold that decides whether the agent's cost and effect is used, read as a parameter of the platform library, with the rule as fallback.
- The capability area "Litigation" and its rights A, C and R are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The next-step branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the two signals as its trigger (GAP-2794; ASM-4632).
2. `CaseAnswer` and `NoticeHoldClient` against their fakes, with the 2 s budget, the breaker and the no-answer path (AC1, AC2, X4, X5).
3. `NextStepEvaluator` over the LITIGATION package, with R-LIT-04, R-LIT-16, R-LIT-36 and the no-fire path (AC1, AC2, AC3, X3, X7).
4. `AgentCostEffectClient` and `RecommendationBuilder`, with the fallback of X6 (AC1, X6).
5. `RecommendationDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `CaseAnswer` with the move, the case-stage timer and the officer task of AC2 and AC3 (AC2, AC3).
7. `NextStep` and the two screens through the composite route fake (AC1, AC3).
8. The boundary test: no statement outside `rwb_litigation`, no write to `rwb_case`, `rwb_comms`, `rwb_document` or `rwb_decision` (X10, BR7).

**Feature flag.** `rwb.litigation.next-step-v1`, read as a flag of the platform library; off means the step records nothing, answers no move and raises no task, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic pack-complete signal in SIT, each of the three rules produces its record, its clock and its answer, the agent fallback leaves the rule's proposal standing, a repeated signal writes once, a forced record failure changes nothing, no case row, task row, notice row or document row is written from this service, and SCR-18 and SCR-19 answer through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of the read, the proposal or the answer is absent or invalid (X8) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right opens the proposal or decides it (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-012-1 (FSD S4 A2.12.3.1). This service holds no ACE batch status read, so the check is the owner's and the message is carried here | {product} is from {date}. Today's ACE batch has not arrived. |

The six texts are the legacy wording of RWB-E5-012 section 14 and of the FSD S4 A2.12 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X5), a notice that is not found (X4) and a case in a state no rule names (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it proposes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-18 Notice approval | Generated | The notice generated for the case and the proposal to hold or dispatch, read only |
| SCR-18 Notice approval | Approved | The dispatch approval of API-S4-001, read only |
| SCR-18 Notice approval | Sent | `sent_date` of the notice on the P6 answer, read only |
| SCR-18 Notice approval | Blocked | The template status withdrawn, the proposal of R-LIT-04, the officer task and the 1-working-day clock |
| SCR-19 Litigation workspace | Pack | The proposal of R-LIT-16, its reasons and the defect list items it names, read only |
| SCR-19 Litigation workspace | Instructed, filed, hearing, judgment | The proposal of the next step for the state of the case, read only, with its cost and effect under R-LIT-36 |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Agent unavailable | The proposal stands on the rule, and the record shows that the cost and effect came from the rule (X6) |
| SCR-19 Litigation workspace | Stale data | The message MSG-P1-001 shown where the owner reports the stale data product of the source |

The route merges the answer of this service with rwb-case for the case and its route state and rwb-comms for the notice; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here. The two state lists are the legacy lists of RWB-E5-012 ("generated; approved; sent; delivered; unserved" and "pack; instructed; filed; hearing; judgment") with the refusal, failure, fallback and stale-data states this story adds.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-012-01 | AC1 | End to end | Recommend the next litigation step |
| TC-E5-012-02 | AC2 | End to end | Rule R-LIT-04 |
| TC-E5-012-03 | AC3 | End to end | Rule R-LIT-16 |
| TC-E5-012-04 | AC4 | Component | Not recorded |
| TC-E5-012-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-012-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 to AC3, the "System" level of the legacy story) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The fakes and the stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-001212`, legal action `LA-2026-001212`, notice `NTC-2026-001212`, the 1-, 2- and 3-working-day clocks — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the step vocabulary, the three clocks, the agent threshold and the message texts are values and reference rows with a version; no step name, day count or state name appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the step carries references, dates, codes, step names and a rule version only, and the test data is synthetic.
- The case stays with rwb-case: no `recovery_case` row, no route state, no case-stage timer row and no `task` row is written here, and the move is answered with the rule and its version (BR3).
- The notice stays with rwb-comms: no notice row, no template status and no barcode is written or set here; the hold is requested, never applied (BR4).
- The pack stays with rwb-document: the index is read, no document, blob or document row is touched (BR5).
- No read of another service's tables and no cross-schema join: `recovery_case`, `task`, `notice`, `document`, `rule_row` and `decision_log_entry` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second answer.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- The agent never decides: its answer supplies the cost and the effect, the rule supplies the proposal, and the officer or the approver decides.
- No event, no topic, no outbox row and no Schedule: this story publishes nothing, consumes nothing and registers no job, and the catalogue of the service is not widened (12.3, 12.4, 12.6).
- The two screens are read only; SCR-18 posts nothing and its approval action is API-S4-001 of the notice story.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| Not specified in the source documents (GAP-2796; ASM-4634) | The legacy story master carries no requirement ID and the FSD S4 requirements table names no requirement for this feature; the nearest is REQ-S4-005, "Court state, hearing dates, deadlines and fees are tracked on the case without a person reading an email", whose facts this step reads to propose the next step (FSD S4 requirements served; Business Requirements Program v5) | FEAT-LIT-12 | 08 Litigate and enforce | R-LIT-04, R-LIT-16, R-LIT-36 | TC-E5-012-01, TC-E5-012-02, TC-E5-012-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-012 | The four legacy criteria word for word, the three rules, the two screens, the messages and the six test cases; the `recovery_case`, `task` and `notice` rows of the legacy data table are retired to their owners |
| RWB-S4-E5012-CON | H: the recommendation element, the reasons, the cost and effect, the consumed facts, the errors and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-18 and SCR-19 |
| rwb-case (P3), rwb-comms (P6), rwb-document (P5), rwb-decision (P7) and rwb-agent (P10) contracts | C in fact and not in the metadata row: the case read and answer, the notice and its template, the pack index, the rule package and the cost and effect, all faked (GAP-2793, GAP-2794, GAP-2795, GAP-2797) |
| RWB-S4-E5012-APP and RWB-S4-E5012-CON siblings of this key | The application and contract halves of the same legacy key |
| FEAT-LIT-12, SCR-18, SCR-19 | The feature and the two screens of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the event platform this story adds no producer or consumer to, Temporal with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-case, rwb-comms and rwb-document, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the recommendation element, the reasons, the cost and effect, the consumed facts, the errors and the fakes: RWB-S4-E5012-CON.
- The case of record, its route states `NOTICE_BLOCKED` and `PACK_VERIFIED`, the parent `CaseWorkflow`, the case-stage timer and the officer task: rwb-case (P3) and its slice of this legacy key (GAP-2794; ASM-4632).
- The notice, its template, the template status of R-LIT-04 and the generation it holds: rwb-comms (P6) and its slice of this legacy key (GAP-2795; ASM-4633).
- The pack, its documents and its defect list items: rwb-document (P5), the pack and defect-list stories of this service (FEAT-LIT-04, FEAT-LIT-05).
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-04, R-LIT-16 and R-LIT-36: rwb-decision (P7), with the embedded runtime as a service-template capability (GAP-2797; ASM-4568).
- The model, the prompt and the confidence check behind the cost and effect: rwb-agent (P10) and its contract (GAP-2793; ASM-4631).
- The step vocabulary the proposal uses: the reference-data owner of rwb-case and the business owner of S4; the story reads the rows and carries the placeholder (GAP-2793; ASM-4631).
- The settlement itself, its approval and the booking of the treatment under R-LIT-36: FEAT-LIT-13 of this module, the sibling story of this key family.
- The tracking of hearings, deadlines and fees that feeds the proposal: FEAT-LIT-11 and RWB-S4-E5011-APP of this service.
- The decision of the officer or the approver and the authority behind it: rwb-access (P4) and the approver screens of the edge.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-18 and SCR-19: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

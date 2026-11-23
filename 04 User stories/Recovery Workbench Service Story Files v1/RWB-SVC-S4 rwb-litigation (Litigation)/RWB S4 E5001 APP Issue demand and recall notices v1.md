# RWB-S4-E5001-APP Issue demand and recall notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-B |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5001-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-001 for rwb-litigation. The three legacy acceptance criteria are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the notices themselves are generated, approved and dispatched by rwb-comms (P6), which is the notice owner of TSD S4 T5.2, so this story evaluates R-LIT-03, writes the legal action of action type `NOTICE` and the local decision record of RWB-PLT-E1027-CON (DP-03), and asks P6 to generate and send; the base becomes `/api/recovery/litigation/v1` (DP-13) and SCR-18 reads through the gateway-bff composite route (DP-19); the notice ownership, the consumed operation names, the case answer, the requirement trace and the approval gate have no single source statement and are declared as the working read of one gap and its assumptions (GAP-2742; ASM-4558 to ASM-4563). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the Workbench to evaluate R-LIT-03 on the Legal-approved template in force, generate the demand and recall notices by rule with no manual drafting and no manual dispatch, write the decision record and the notice legal action before anything changes and answer rwb-case for the stage move**, so that **cases reach court faster with complete packs, on notices that no person typed and no person posted**.

This is the application slice of legacy RWB-E5-001. It owns:

- all three legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rule, message, screen and data rows they depend on;
- one notice step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19; Temporal and Drools Design slide 5, "S4 Litigation — notices, court dates, years");
- the evaluation of R-LIT-03 on the template fact and on the case product of the action, with the LITIGATION package version in force;
- `POST /cases/{caseId}/legal-actions` (API-S4-002), `GET /legal-actions/{legalActionId}` (API-S4-003) and `POST /notices/{noticeId}/approve` (API-S4-001) on base `/api/recovery/litigation/v1`, under capability area "Litigation" with the rights C, R and A (DP-13; TSD S4 T-A.1);
- the `legal_action` row of action type `NOTICE` in schema `rwb_litigation`, with the columns of DF-LEG-001 to DF-LEG-014 and no new column;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the legal action or the notice changes (DP-03);
- the answer to rwb-case for the stage move `NOTICE_DISPATCHED`, with the rule ID and the version that produced it;
- SCR-18 Notice approval as this service's answer, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the three operations, the notice action type and status vocabulary, the request and answer shapes, the error set and the fakes, which are RWB-S4-E5001-CON; the notice row, the template, the rendering of the letter and the WIN dispatch, which are rwb-comms (P6) on its notice contract; the case of record, its route state and the parent `CaseWorkflow`, which are rwb-case (P3); the approval routing, the delegation of authority and the decision ledger, which are rwb-decision (P7); the proof of delivery and the notice period timer, which are the sibling stories of this service; the document of the notice pack, which is rwb-document (P5); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-001 gave the Workbench one step that produced and sent the statutory notices by rule. Notices are prepared by hand today, a demand fee notice sent incomplete is a Bank of Thailand finding, and litigation takes 21 days to file. The functional specification keeps the objective, the metric and the requirement: a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days of today; and REQ-S4-001, "Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed" (FSD S4 A2.1 and its requirements-served list; Business Requirements Program v4). The legacy master itself carries no requirement row, which is recorded (GAP-2742; ASM-4562).

What D-RCV-60 changes is who owns what, and the sources have answered the three questions:

- **the notice is rwb-comms' (P6).** TSD S4 T5.2 says the module reaches other modules "P6 for notices"; the FSD P6 module table gives P6 "E1 notices; E2 dispatch" with the scope "letters, notices, SMS, LINE, proof of delivery", its dispatch job JOB-10 at 16:00 writes the WIN file, and its notice types are DEMAND and RECALL. The Ownership Map gives S4 two tables, `legal_action` and `hearing`, and no notice table. This story therefore writes no notice row: it evaluates the rule, writes the notice legal action and the decision, and asks P6 to generate and send (GAP-2742; ASM-4558);
- **the case of record stays with rwb-case (P3).** `recovery_case`, its route state and the parent `CaseWorkflow` are P3's; the stage states `NOTICE_GENERATED` and `NOTICE_DISPATCHED` of the legacy criterion are states of the LITIGATION machine (TSD S4 T4) held by `LitigationWorkflow`, reported to the parent as the stage outcome, and applied to the case by rwb-case (GAP-2742; ASM-4559);
- **the legal action of action type `NOTICE` is this service's.** `legal_action` and its `action_type` value `NOTICE` of `LOV-LEGAL-TYPE` are S4's (Ownership Map; TSD S4 T3.1 and T3.2), and the action is what the filing, judgment and enforcement stories of this service build on;
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the legal action change, which is what legacy AC1 asked for and what legacy AC3 tested;
- **the template is not read here.** The rule condition is `template_status = current for product and notice_type`; the template status and version arrive on the P6 notice fact, so no template row is read in `rwb_litigation` and no `rwb_template` table is created (GAP-2742; ASM-4560).

The approval is the one statement of the legacy story that does not settle by itself. AC1 says "with no person in the path", while the D7.1 approval of a generated demand or recall notice is a built Epic 2 capability (RWB-E2-014, on `POST /notices/{noticeId}/approve`, which the Ownership Map lists as an operation of S4). The two are read together: no person drafts, renders, addresses or posts a notice in this story, and the step raises no officer task of its own; the D7.1 approval stands as a gate of the notice service that the step waits on, and it is neither rebuilt nor bypassed here (GAP-2742; ASM-4561).

The step publishes and consumes nothing. DP-09 is not in this story's pattern set, the event catalogue of `rwb.litigation.events.v1` holds `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` and none of them is a notice event, and `NoticeDelivered` on the S4 IN row of Architecture v5 slide 19 is the fact of the proof-of-delivery sibling, which starts the notice period timer there and not here (GAP-2742; ASM-4563).

### 3. Preconditions

- RWB-S4-E5001-CON is published: the three operations, the `NOTICE` action type, the stage vocabulary, the request and answer shapes, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-comms (P6) notice contract is published with its fake, so a notice can be generated and sent on Day 1. It is a contract dependency of class C in fact and is not in this story's C row, which is None; the name of the operations is Not specified in the source documents (GAP-2742; ASM-4558).
- The stage-outcome answer of rwb-case is available for the fake. No source names a published operation that moves a case state on behalf of a stage: on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation for another caller its name is Not specified in the source documents (GAP-2742; ASM-4559).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003, so the legal action change and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-18 Notice approval reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` exists in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-014 and the standard record columns of TSD S4 T3.0; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version with R-LIT-03 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce` (GAP-2742; ASM-4561).
- The template facts the rule condition needs are answered by the P6 notice contract: the template code, its Legal-approved version and its status for the product and the notice type. No `template` row (DF-REF-045 to DF-REF-051) is read in `rwb_litigation`, and DP-07 is not in this story's pattern set (GAP-2742; ASM-4560).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement outside its schema is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5001-CON when its tests pass.

### 4. Flow

1. The route R4 of the case is approved and the litigation stage opens: `LitigationWorkflow` starts on task queue `rwb-litigation` as the child of `CaseWorkflow`, with the case, the product group and the rule package in force as its input.
2. The step reads the notice legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): the action type, the product group through the case reference and the status. Where the stage has no `NOTICE` action yet, it creates one on `POST /cases/{caseId}/legal-actions` (API-S4-002) with the action type `NOTICE` of `LOV-LEGAL-TYPE`, the case reference and the claim amount, and the create is idempotent on its `Idempotency-Key`.
3. The step reads the template fact the rule tests on the P6 notice contract: the template code, its version approved by Legal, its status for the product and the notice type (`DEMAND` or `RECALL`), one hop with a 2 s budget and a breaker (GAP-2742; ASM-4558).
4. `NoticeRuleEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates R-LIT-03: where `template_status = current` for the product and the notice type, the demand and recall notices are generated from the Legal-approved template and the stage moves to `NOTICE_DISPATCHED` (FSD S4 A2.1.3.1; Business Rules and Routing Logic v4).
5. The evaluation answers the rule ID, the package version, the template code and version it used, and the stage move.
6. `NoticeDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the template version, the inputs reference, the outcome and the stage move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
7. `NoticeClient` asks rwb-comms (P6) to generate the demand and recall notices from the named template version and to send them on the dispatch run: the case reference, the notice type, the template code and version, the addressee role and the legal action reference. P6 renders the letter, holds it for the D7.1 approval where the approval is in force, writes it to the WIN file (JOB-10) and owns the notice state `Generated`, `Approved`, `Sent`, `Delivered` or `Unserved` (GAP-2742; ASM-4558).
8. `NoticeActionWriter` writes the standard columns of the `NOTICE` legal action in one `rwb_litigation` transaction with the decision record and the idempotency row. No business column of the action changes: `action_type` is `NOTICE`, `claim_amount` (DF-LEG-009) is read for the notice body, and `status` (DF-LEG-014) is left to the filing stories, which move it to `FILED` when the court filing is recorded.
9. The step answers the parent `CaseWorkflow` with the stage move `NOTICE_DISPATCHED`, the rule ID, the version, the template version, the notice reference P6 returned and the decided-at time. rwb-case writes the case of record and its route state; this service writes neither (GAP-2742; ASM-4559).
10. Where the template status is not current, the rule does not fire: the stage holds, a task is raised to the litigation officer with the message of the hold, and nothing is dispatched. That hold path is R-LIT-04 and is owned by the pack stories of this service; this step only reports it (FSD S4 A2.4.3.1).
11. A repeated trigger with the same case, legal action and template version writes nothing, sends no second notice request and counts the repeat.
12. The step sets a durable timer for the 1 working day of R-LIT-03, so a dispatch that has not answered inside the rule's window raises the stage on the workflow and never on a Quartz job.
13. SCR-18 Notice approval reads the notice, its template version, the case facts it was built from and the rule with its version from this service and from rwb-comms through the gateway-bff composite route, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the legal action keeps its state, no notice is requested and no stage move is answered | MSG-P7-003 | AC3, TC-E5-001-03, TC-E5-001-05 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E5-001-04 |
| X3 | The legal action does not exist or is outside the scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC1 |
| X4 | The action is not of action type `NOTICE`, or the case has no open litigation stage | 409 and nothing changes; no notice is requested | None | AC1 |
| X5 | The P6 notice contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written, no notice is requested and no stage move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC3 |
| X6 | The template status is not current for the product and the notice type | R-LIT-03 does not fire: nothing changes, no decision record is written, no notice is requested, and the hold task is the pack story's | MSG-P6-003 | AC2 |
| X7 | The same case, legal action and template version arrive twice, or the same `Idempotency-Key` is replayed | One write and one notice request; the repeat is counted and no second decision record is written | None | AC1 |
| X8 | The rule package in force is not the one the step was started on | The step re-evaluates on the package named on `RulePackageInForce` and records the version it used | None | AC1 |
| X9 | A required field of the create or of the approval is absent or invalid | 422 and nothing is written | MSG-GEN-001 | AC2 |
| X10 | A component, a statement or a test reaches another service's schema, a `notice` row or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR4, BR6 |

X1 to X4 are the exception paths of RWB-E5-001 carried onto the split, X5 to X9 are the paths the target call types add, and X10 is the DP-01 boundary. The template statuses and the notice types of X6 are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5001-CON, the P6 notice contract and the case answer fake, on the table of its own schema, and needs no live rwb-comms, no live rwb-case and no live rwb-decision |
| Negotiable | The activity name, the decision code and the shape of the stage outcome are this story's choice; the rule, the messages, the screen, the three operations and the action type are fixed |
| Valuable | A demand or recall notice is generated and sent by rule in one recorded step, with the template version on the decision record and no re-typing of a notice |
| Estimable | One workflow step, one evaluator, one record write, one action write, one client, one approval operation and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and template facts through the contract fakes, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Issue demand and recall notices

  Background:
    Given case "RC-2026-000501" carries the litigation legal action "LA-2026-000501" of action type "NOTICE"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-03
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Issue demand and recall notices (legacy RWB-E5-001 AC1)
    Given the rwb-comms contract mock returns the demand and recall notice generated from the Legal-approved template in force
    Given the rwb-case contract mock returns the case route state "NOTICE_GENERATED" for case "RC-2026-000501"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces and sends the statutory notices by rule, with no person in the path
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-03 (legacy RWB-E5-001 AC2)
    Given the rwb-comms contract mock returns template "DEMAND-MTG" at its Legal-approved version with template_status "current" for the product and the notice type
    Given a case in state NOTICE_GENERATED
    When template selected
    Then generate the demand and recall notices from the Legal-approved template
    Then the case moves to NOTICE_DISPATCHED

  Scenario: AC3 Not recorded (legacy RWB-E5-001 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E5-001 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry one or two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-comms renders, approves and dispatches the notice; this story evaluates R-LIT-03, writes the decision record with the rule version and writes the `NOTICE` legal action; and rwb-case writes the stage move on the case of record. The legacy `notice` write of the data table is not reproduced anywhere in this story (GAP-2742; ASM-4558).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-03 | Litigation | D7 | NOTICE_GENERATED | TEMPLATE_SELECTED | template_status = current for product and notice_type | Generate the demand and recall notices from the Legal-approved template | NOTICE_DISPATCHED | Workbench | Rules component, letter engine, the Workbench document hub | 1 working day |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its owner column is a role of the business and not a service: `Workbench` is the litigation stage, and in the target the letter engine and the document hub of the systems column are rwb-comms (P6) and rwb-document (P5), each reached on its own contract.

| ID | Rule | Source |
|---|---|---|
| BR1 | The notice legal action is this service's: the action type `NOTICE` and the columns of `legal_action` are written in `rwb_litigation`, and no other service writes them | Architecture v5 slide 41; Ownership Map (legal_action owner S4); TSD S4 T3.1 and T3.2 |
| BR2 | The decision is recorded before the legal action changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2; legacy RWB-E5-001 AC1 and AC3 |
| BR3 | The notice stays with rwb-comms: the row, the template, the rendering, the approval gate and the WIN dispatch are P6's, and this story reads the notice and asks for it on the P6 contract only | TSD S4 T5.2 ("P6 for notices"); FSD P6 v3 (scope, JOB-10, notice types DEMAND and RECALL); GAP-2742 |
| BR4 | No `notice` row, no `template` row and no `document` row is read or written here, and the service holds no grant outside `rwb_litigation` | DP-01; Ownership Map; Architecture v5 slide 29 |
| BR5 | The stage move is answered and not written: `recovery_case` and its route state are rwb-case's, and the stage state `NOTICE_GENERATED` or `NOTICE_DISPATCHED` is held by `LitigationWorkflow` and reported to the parent | Ownership Map (recovery_case owner P3); Architecture v5 slide 19; GAP-2742 |
| BR6 | No ACE view and no ACE table is read or written here, and no cross-schema join is made | DP-01; Architecture v5 slide 29 |
| BR7 | The same case, action and template version twice, or the same `Idempotency-Key` twice, writes once, requests one notice and counts the repeat | TSD S4 T-A.2; Architecture v5 slide 11 |
| BR8 | The vocabulary is closed: the action type is `NOTICE` of `LOV-LEGAL-TYPE` (NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION, LED_AUCTION) and the notice states are the notice service's; no state name and no list value is written in code | TSD S4 T3.2; BR-S4-001 (FSD S4 A2.1.3.1) |
| BR9 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or an event: the step carries case references, action references, codes, dates and amounts | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

**Where each rule lives in the target.** R-LIT-03 is the one rule this story evaluates: the template fact answers the condition, the record is written, P6 is asked to generate and send, and the stage move `NOTICE_DISPATCHED` is answered. The hold rules of the same from-state — R-LIT-04 on a withdrawn template and R-LIT-05 on a contact stop — are named here and are the pack and deviation stories' to build; this step reports the hold and dispatches nothing. VR-S4-001-1 of the FSD tests the freshness of the ACE batch of the source and raises MSG-P1-001; this service holds no `v_ace_batch_status` read, so the check belongs to the owner of the data product and the message is carried in section 14 without a path here (GAP-2742; ASM-4560).

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR5). What this story does own is the state of the litigation stage and of the step.

| From (stage state) | Event | Condition | To |
|---|---|---|---|
| NOTICE_GENERATED | TEMPLATE_SELECTED under R-LIT-03 | template_status = current for product and notice_type | `NOTICE_DISPATCHED`, with the stage move answered and the notice requested |
| NOTICE_GENERATED | TEMPLATE_WITHDRAWN under R-LIT-04 | A hold of the pack story | Unchanged here: no rule of this story fires, nothing is dispatched |
| NOTICE_GENERATED | CONTACT_STOP_APPLIED under R-LIT-05 | A hold of the deviation story | Unchanged here: no rule of this story fires, nothing is dispatched |
| NOTICE_DISPATCHED | Proof of delivery or proof window expiry | The sibling stories of this service | Unchanged here: the notice period and its timer are not this story's |
| A stage other than NOTICE_GENERATED | The step is triggered | X4 | Unchanged, refused with 409 |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The litigation stage opens for route R4 | The package in force is loaded | Evaluating |
| Evaluating | R-LIT-03 fires | The decision record is written | Sending |
| Sending | P6 is asked to generate and send | The notice reference is returned and the transaction commits | Waiting for the next stage event |
| Sending | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Sending | The 1 working day of R-LIT-03 passes with no dispatch answer | The rule's own timer | Waiting, the stage raised on the workflow |

The stage states `NOTICE_GENERATED`, `NOTICE_DISPATCHED`, `NOTICE_BLOCKED` and `NOTICE_UNSERVED` are the states of the LITIGATION machine of TSD S4 T4. The action status values are those of `LOV-LEGAL-STATUS` and this story moves none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix: the primary role of the feature, holding the create right C, the read right R and the approval right A |
| RW-LEGAL, legal counsel | Litigation RA: reads the action and the notice, and approves a notice for dispatch |
| RW-PRODHEAD and RW-HEADLIT | Litigation RA: read, and approve through the D7.1 approval path where the notice needs it |
| RW-ENFORCE, enforcement owner | Litigation CRU: reads the action and creates it, with no approval right |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU: reads its own action and its notices, through the partner gateway |
| SY-CASEWF, SY-RULES, SY-DATALOAD, SY-AGENT | Litigation R as the TSD S4 T6.1 matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the rule, writes the decision record and the legal action, asks P6 for the notice and answers the stage move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The legacy permission table names RW-LITOFF, RW-LEGAL, RW-PRODHEAD and RW-HEADLIT for right A and RW-LITOFF and RW-ENFORCE for right C, and both statements agree. The FSD says the feature "runs unattended" and that the litigation officer "also uses" it, and both hold here: the step runs under the service identity with no officer task on the generation path, and the officer acts on the approval operation and on SCR-18. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Write on the create, and read as the legal action reference of the answer |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Write on the create, and sent on the stage answer |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Write, against `LOV-LEGAL-TYPE`: `NOTICE` |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Read, for the notice body and the case facts of SCR-18 |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read only: the filing stories move it to `FILED` |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `updated_at`, `updated_by`, `is_active` | Write, with the optimistic lock of `version` |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, template version, inputs reference, outcome, decided at | Write through the local library, before the legal action changes |
| DF-LEG-015 to DF-LEG-023 | notice (P6, `rwb_comms`) | id, case_id, document_id, notice_type, sent_date, barcode and 3 more | Not read and not written as a table: the notice is reached on the P6 contract only (GAP-2742; ASM-4558) |
| DF-REF-045 to DF-REF-051 | template (reference data, owner Not specified in the source documents (GAP-2742; ASM-4560)) | template_code, template_version, language, product_group, status | Not read: the template fact arrives on the P6 contract |
| DF-ACE-001 to DF-ACE-054 | `v_ace_*` views (P1) | the account and customer facts | Not read: this service holds no `v_ace_*` grant (BR6) |

Field IDs are those of TSD S4 Litigation and enforcement v2 T3.1 and the Logical Data Model and Data Dictionary v8; the `notice` and `template` rows are the rows the legacy story lists in its Data table, with their owners outside this service. **No new table, no new column and no migration**: `legal_action` arrives with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7) are not created, not written and not read as tables.

**No personal data.** The rows this story writes carry identifiers, an amount, dates, list values and a rule version. The addressee of a notice is a role and a contact point of the notice service, never a value of this schema; no name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind three operations whose shapes are declared by RWB-S4-E5001-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its action type and status (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| POST | `/notices/{noticeId}/approve` | No request body, the notice reference out, status 200 (API-S4-001) | Litigation, right A, scope applied | `Idempotency-Key` header required |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action or notice, 409 for a wrong-type action or a stage that is not `NOTICE_GENERATED`, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the decision library, the P6 contract or the rule package does not answer. The operation IDs are those of TSD S4 T-A.1 and are not redefined here. The notice row behind API-S4-001 is rwb-comms' and is not declared as this service's table (GAP-2742; ASM-4558).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The generate and send operation of the rwb-comms notice contract (operation name Not specified in the source documents (GAP-2742; ASM-4558)) | `/api/recovery/comms/v1` | P6 rwb-comms | The demand or recall notice generated from the named template version and sent on the dispatch run: the case reference, the notice type, the template code and version, the addressee role and the legal action reference in; the notice reference and its state out; faked |
| The stage-outcome answer (operation name Not specified in the source documents (GAP-2742; ASM-4559)) | rwb-case (P3) | P3 rwb-case | The answer that carries `NOTICE_DISPATCHED` with the rule and its version; the row and the route state are P3's, and on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). Both rows are contract dependencies of class C in fact while the C row of this slice is None, and the absence is recorded as GAP-2742 with ASM-4558 and ASM-4559.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result; none of them is a notice event. This story publishes none of them: DP-09 is not in its pattern set, it writes no outbox row, and its two outputs are the local decision record of DP-03 and the stage answer of 12.2. The catalogue is not widened and a build that adds a fourth event to this service fails the absence test.

#### 12.4 Events consumed

None. `NoticeDelivered` is the one notice fact on the S4 IN row of Architecture v5 slide 19, and in the target it is the proof of delivery that starts the notice period: that is the sibling story of this legacy family, not this one. With DP-09 outside this story's pattern set, no consumer, no inbox row and no subscription is declared here; the template fact and the notice reference arrive on the P6 contract of 12.2, synchronously (GAP-2742; ASM-4563).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the case state answered by rwb-case, the rule package in force and the approval answer; one durable timer of 1 working day for R-LIT-03 |
| `issueDemandAndRecallNotices` | Activity, the one notice step of this story | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the template version, the notice reference and the stage move out, with the decision record and the legal action written in one transaction |

The activity name is a target design choice of this story and is fixed by no source document. The step is triggered by the opening of the litigation stage for route R4, which is the event `ROUTE_APPROVED` of R-LIT-01, because the legacy story says the step runs with no person in the path while the FSD declares no background event (GAP-2742; ASM-4561).

#### 12.6 Schedules

None. The dispatch run JOB-10 at 16:00 is rwb-comms' and is not registered here; the 1 working day of R-LIT-03 is a durable timer of the workflow and not a Temporal Schedule, and no Job of Architecture v5 slide 44 is owned, moved or registered by this story.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | The `NOTICE` action: this story creates it and writes its standard record columns; no business column of the action moves |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated create, approval and stage answer, and the answer it holds |

Not owned and never read as a table: `notice` and `template` (P6 rwb-comms), `recovery_case` (P3), `document` (P5), `decision_log_entry` and `rule_row` (P7), `hearing` (S4, read only by the sibling stories), and every `v_ace_*` view (P1). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms notice fake | The notice generated from template `DEMAND-MTG` at its Legal-approved version with status `current` for case `RC-2026-000501`, with the notice reference and the state `Approved` or `Sent`; a template status `withdrawn`; an unreadable answer; no answer beyond 2 s | AC1, AC2, X5, X6 |
| rwb-case stage fake | The case route state `NOTICE_GENERATED` of case `RC-2026-000501`; the stage move `NOTICE_DISPATCHED` accepted and a move refused because the stage is not in the state the rule expects | AC1, AC2, X4 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-03 and the approval answer of a held notice | AC1, AC2, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-18 answer for case `RC-2026-000501`, with the notice facts of this service and of rwb-comms read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the P6 row, the notice reference shape and the stage-outcome answer are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2742; ASM-4558, ASM-4559).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | The create, read and notice approval on `/api/recovery/litigation/v1`; the P6 notice request and the stage answer; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity | `LitigationWorkflow` and its one notice step on `rwb-litigation`, with one durable timer; no Schedule |
| File | None | No file is read, built or delivered here; the WIN file of JOB-10 is rwb-comms' and rwb-integration's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `notice`, Java package `th.co.scb.ace.workbench.recovery.litigation.notice`; front end `src/modules/recovery/litigation/NoticeApproval.tsx`, the fragment SCR-18 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `legal_action` row commit together or not at all, and a failed write stops the dispatch request. DP-13 moves the base of the three operations and nothing else. DP-19 is how SCR-18 reaches this service, one hop through the gateway. DP-01 applies as the schema boundary and adds no dependency; DP-07 is absent from the pattern set, which is why the template fact is consumed on the P6 contract and no reference-data table is read (GAP-2742; ASM-4560).

**Dependencies the tables add and the plan does not hold.** The P6 notice contract and the rwb-case stage answer are class C dependencies of this story in fact, and the plan's C row is None; the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2742 with ASM-4558 and ASM-4559.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` notice branch | Workflow | The step of the journey that opens on route R4, loads the package in force, runs the notice step and reports the stage to the parent |
| `issueDemandAndRecallNotices` | Activity | The one step: read or create the legal action, read the template fact, evaluate R-LIT-03, write the record and the action, ask P6, answer the stage move |
| `NoticeRuleEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the template condition and the notice types `DEMAND` and `RECALL` |
| `NoticeDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `NoticeActionWriter` | Repository | Creates the `NOTICE` action and writes its standard columns in one `rwb_litigation` transaction, with the idempotency row and the optimistic lock |
| `NoticeClient` | Client | The P6 generate and send call, one hop, 2 s, breaker, and no retry of its own |
| `NoticeApprovalController` | Controller | The three operations, the capability area and right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `StageOutcomeReporter` | Signal reporter | Answers the parent with the stage move, the rule and the version; it reports, it never changes a case row |
| `NoticeApproval` | React component | Shows the generated notice, the case facts it was built from, the template version and the rule on SCR-18, read only, with the hold, refusal and failure states |

**Database and migrations.** No Flyway file. `legal_action` arrives with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the notice reference, the template version or the stage move: those are facts of the request and of the answer, and storing them would copy another service's facts into this schema (GAP-2742; ASM-4558).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the template statuses, the notice types and the 1 working day of the rule are values of the package and of the notice service, not of this build (BR-S4-001).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- The 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The notice branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the opening of the litigation stage as its trigger (GAP-2742; ASM-4561).
2. `NoticeClient` against the P6 fake, with the 2 s budget, the breaker and the no-answer path (AC1, X5).
3. `NoticeRuleEvaluator` over the LITIGATION package, with R-LIT-03 and the no-fire path (AC1, AC2, X6).
4. `NoticeDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X1).
5. `NoticeActionWriter` with the create, the one transaction and the idempotency row (AC1, AC2, X7).
6. `StageOutcomeReporter` and the parent signal, with the stage move (AC1, AC2).
7. `NoticeApprovalController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, AC2, X2, X9).
8. `NoticeApproval` and SCR-18 through the composite route fake (AC1).
9. The boundary test: no statement outside `rwb_litigation`, no `notice`, `template` or `v_ace_*` read, no write to `rwb_case`, `rwb_comms` or `rwb_decision` (X10, BR3, BR4, BR6).

**Feature flag.** `rwb.litigation.notice-issue-v1`, read as a flag of the platform library; off means the step holds the case at `NOTICE_GENERATED`, requests no notice and answers no stage move, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic template fact in SIT, R-LIT-03 produces its record, its notice request and its stage move, a repeated trigger writes once, a forced record failure changes nothing, no `notice` row and no `recovery_case` row is written from this service, and SCR-18 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service, so no path of this story raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid (X9) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads, creates or approves (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the legal action changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The data product of the source is stale after a late or failed ACE batch, which is VR-S4-001-1 (FSD S4 A2.1.3.1). This service holds no ACE batch status read, so the check is the owner's and the message is carried here (GAP-2742; ASM-4560) | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P6-003 | The template was withdrawn after generation (X6). The text is the notice service's and is displayed on SCR-18 as it comes from P6 | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |

The first six texts are the legacy wording of RWB-E5-001 section 14 and of the FSD S4 A2.1 message list, copied unchanged; the seventh is the hold message of the FSD P6 message set and is displayed, not raised, here. No message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X5) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. One existing surface shows what it writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-18 Notice approval | Generated | The demand or recall notice generated from the Legal-approved template, with the template code and version and the case facts it was built from, read only |
| SCR-18 Notice approval | Approved | The D7.1 approval of the notice, its approver role and time, and the rule with its version |
| SCR-18 Notice approval | Sent | The notice state `Sent` on the dispatch run, with the legal action of this service beside it |
| SCR-18 Notice approval | Delivered | The proof-of-delivery state of the sibling story, read only |
| SCR-18 Notice approval | Unserved | The unserved state of the sibling story, read only, with the notice period not started |
| SCR-18 Notice approval | Blocked | The template is withdrawn or a contact stop is on: the stage `NOTICE_BLOCKED`, MSG-P6-003 and nothing dispatched |
| SCR-18 Notice approval | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-18 Notice approval | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-18 Notice approval | Stale data | The message MSG-P1-001 shown where the owner reports the stale data product of the source |

The five legacy states "Generated; approved; sent; delivered; unserved" are kept as they stand and the refusal, hold and failure states are the ones this story adds. The legacy row for SCR-20 Enforcement workspace ("Requested; seized; auctioned; closed") is carried by the enforcement stories of this service and is not shown here. The route merges the answer of this service with rwb-comms for the notice and rwb-case for the case; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-001-01 | AC1 | End to end | Issue demand and recall notices |
| TC-E5-001-02 | AC2 | End to end | Rule R-LIT-03 |
| TC-E5-001-03 | AC3 | Component | Not recorded |
| TC-E5-001-04 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-001-05 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The five legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1 and AC2) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The P6 fake, the case fake, the rule-package fake and the decision-record stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000501`, action `LA-2026-000501` and template `DEMAND-MTG` at its Legal-approved version — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the template statuses, the notice types, the lists, the 1 working day of the rule and the message texts are values and reference rows with a version; no list value, state name, period or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry identifiers, an amount, dates, codes and a rule version only, the addressee is a role, and the test data is synthetic.
- The notice stays with rwb-comms: no `notice` row, no template, no rendering and no WIN dispatch is written or triggered here (BR3; DP-01).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR5).
- ACE data only through the owner's contract: no component of this story reads a `v_ace_*` view or an ACE table, and the service holds no `v_ace_*` grant (BR6).
- No read of another service's tables and no cross-schema join: `notice`, `template`, `recovery_case`, `document`, `rule_row` and `decision_log_entry` are reached only through their owners' contracts.
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second dispatch request.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing, and the catalogue of the service is not widened (12.3, 12.4).
- SCR-18 is read only; the approval it shows is the D7.1 gate of the notice service and is never bypassed by this step.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed; this story owns the generation and the dispatch request, and the notice period is the sibling story's (FSD S4 requirements served; Business Requirements Program v4); the legacy story master carries no requirement ID (GAP-2742; ASM-4562) | FEAT-LIT-01 | 08 Litigate and enforce | R-LIT-03 | TC-E5-001-01, TC-E5-001-02 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-001 | The three legacy criteria word for word, R-LIT-03, SCR-18, the message set and the five test cases; the `notice` write of the legacy data table is retired to P6 |
| RWB-S4-E5001-CON | H: the three operations, the notice action type, the stage vocabulary, the request and answer shapes and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-18 |
| rwb-comms (P6) notice contract | C in fact and not in the metadata row: the notice generated, approved and dispatched, faked (GAP-2742) |
| rwb-case (P3) and its stage answer | The case of record and its route state `NOTICE_DISPATCHED`, answered and never written (GAP-2742) |
| RWB-S4-E5001-CON sibling of this key | The contract half of the same legacy key |
| FEAT-LIT-01, SCR-18 | The feature and the screen of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the event platform this story adds no producer or consumer to, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-comms and rwb-case, with the `-ITG` copies of the five cases |

### 19. Out of scope

- The published shape of the three operations, the notice action type, the stage vocabulary, the request and answer shapes, the error set and the fakes: RWB-S4-E5001-CON.
- The notice row, the templates, the rendering of the letter, the D7.1 approval of a notice, the dispatch run JOB-10 and the WIN file: rwb-comms (P6) and rwb-decision (P7). **The notices are generated, approved and dispatched by rwb-comms, and this story evaluates the rule, writes the legal action and the decision and asks for the notice** (GAP-2742; ASM-4558).
- The case of record, its route state `NOTICE_DISPATCHED`, the parent `CaseWorkflow`, the case router and the case timers: rwb-case (P3) (ASM-4559).
- The proof of delivery, the notice period and its timer, the pack and the filing: the sibling stories of this service, RWB-E5-002, RWB-E5-003 and the pack stories.
- The authoring, testing, approval and versioning of the LITIGATION package and of the row of R-LIT-03, and the approval matrix and delegation of authority: rwb-decision (P7).
- The template reference data and the freshness stamp of the data product: the reference-data owner and rwb-source-data (P1); VR-S4-001-1 is its check and MSG-P1-001 is carried here only (GAP-2742; ASM-4560).
- The document of the notice pack, its custody and its retention: rwb-document (P5); this story stores no document.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-18: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

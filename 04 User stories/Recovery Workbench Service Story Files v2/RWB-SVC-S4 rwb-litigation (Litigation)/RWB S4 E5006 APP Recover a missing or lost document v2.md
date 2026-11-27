# RWB-S4-E5006-APP Recover a missing or lost document

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-G |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S4-E5006-APP-16); the squad sizes it at refinement |
| Depends on (build) | RWB-S4-E5006-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | P5 rwb-document (API-P5-008 of RWB-P5-E1040-APP; API-P5-002 of RWB-P5-E1026-APP); P8 rwb-payment and P10 rwb-agent (contract stories not named in the source documents; GAP-1737) |
| Contract version | Not specified in the source documents (DOR-RWB-S4-E5006-APP-23) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S4-E5006-APP-14) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped; traced to REQ-S4-002 and FEAT-LIT-06, GAP-2762) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-006 for rwb-litigation. The two legacy acceptance criteria are kept word for word with their origin tag and now run as one step of `LitigationWorkflow` on task queue `rwb-litigation`; the `document` row is rwb-document's (P5), so the legacy read and write of the document and its pack item become consumed calls on the P5 contract and no `document` row is read or written here (DP-01); the supplied item is handed back to the defect check of R-LIT-18, which is RWB-S4-E5005-APP's, and this step owns only the unrecoverable and prescription outcomes of R-LIT-19 and R-LIT-20; the legacy `decision_log_entry` write becomes the local decision record of RWB-PLT-E1027-CON written before the case move (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 reads through the gateway-bff composite route (DP-19); the recovery element and the reason list and the CCMS path have no source specification and are carried as the working read of the assumptions (GAP-2760, GAP-2761, GAP-2762, GAP-2763, GAP-2764; ASM-4594, ASM-4595, ASM-4596, ASM-4597, ASM-4598). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S4-E5006-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (27 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the Workbench to open the recovery path for a document the pack needs and the bank cannot find — read the checklist the pack is checked against, record that the item cannot be re-created and hand a supplied item back to the defect check, record the decision with its rule version before anything moves and answer rwb-case for the case move**, so that **a pack that is short of one document moves forward in one recorded step, with the affidavit route named where the item cannot be re-created, instead of the officer chasing the document outside the case**.

This is the application slice of legacy RWB-E5-006. It owns:

- both legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- one pack-recovery step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19, "TMP LitigationWorkflow (years; continues-as-new)"; Temporal and Drools Design slide 13);
- Workflow ID form and start rule of `LitigationWorkflow`: Not specified in the source documents (CG-ALL-9119).
- the evaluation of R-LIT-19 and R-LIT-20 of the LITIGATION package on the recovery outcome of an item and on the remaining prescription days, with the package version in force, and the hand-back of a supplied item to the defect check of R-LIT-18, which is RWB-S4-E5005-APP's;
- `GET /legal-actions/{legalActionId}` (API-S4-003) and `POST /cases/{caseId}/legal-actions` (API-S4-002) on base `/api/recovery/litigation/v1`, under capability area "Litigation" with the rights R and C (DP-13; TSD S4 T-A.1);
- the read of the case checklist and of the case documents from rwb-document, on the P5 contract and its fake;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the case move (DP-03);
- the answer to rwb-case for the case move `PACK_VERIFIED`, with the rule ID and the version that produced it;
- SCR-19 Litigation workspace in its pack state, as this service's answers, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the recovery element, the outcome vocabulary, the error set and the fakes, which are RWB-S4-E5006-CON; the `document`, the checklist item, the retrieval request, the custody of the file and its retention, which are rwb-document (P5); the case of record, the route states `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `PACK_VERIFIED` and the parent `CaseWorkflow`, which are rwb-case (P3); the defect check itself and its re-run on a supplied item (R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32), which are RWB-S4-E5005-APP's; the authoring and approval of the LITIGATION package and the Head of Litigation approval of R-LIT-19 and R-LIT-20, which are rwb-decision (P7); the CCMS path of the external system, whose owner is not specified (GAP-2764; ASM-4598); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-006 gave the Workbench one user step that opened the recovery path for a document the pack needs and the bank cannot find. The functional specification keeps the objective and its metric — a litigation turnaround of 6 days, measured on the decision log and the Workbench records, reviewed monthly, against the 21 days a filing takes today — and its problem statement names the cause it addresses: packs are incomplete and law firm progress is not tracked (FSD S4 A2.6.1 and A1.3). The module requirements carry the same intent: REQ-S4-002, "a litigation pack is assembled and checked against the document checklist, and missing documents are requested" (FSD S4 requirements served; Business Requirements Program v5).

What D-RCV-60 changes is who owns the document and who owns the case. In the monolith the pack, the document row, the case state and the decision log row sat in one `recovery` schema and one process. In the target:

- **the document is rwb-document's (P5).** The `document` table of the legacy data table (DF-DOC-001 to DF-DOC-011), the checklist item, the retrieval request, the stored file, the OCR text and the retention class are P5's; Architecture v5 slide 41 gives rwb-document "metadata, custody, OCR text and fields, signatures, retention" (Ownership Map: `document` owner P5). This story reads the checklist and the case documents on the owner's contract and its fake, and it writes no `document` row, no file, no retention class and no retrieval request (GAP-2760; ASM-4594);
- **the case of record stays with rwb-case (P3).** `recovery_case`, its route state and the parent `CaseWorkflow` are P3's; `PACK_DEFECT_HOLD`, `PACK_ASSEMBLY` and `PACK_VERIFIED` are written there and not here. This story evaluates the rule, records the decision and **answers** the case move (GAP-2760; ASM-4594);
- **the recovery decision stays with rwb-litigation (S4).** The judgement that an item cannot be re-created, the referral to Legal for the affidavit route and the escalation of a pack that is close to prescription are S4's, and `legal_action` and `hearing` are S4's tables (Ownership Map; Architecture v5 slide 41);
- **the defect check stays with its own story.** The check of the pack against the defect list and the re-run on a supplied item are R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32, which RWB-S4-E5005-APP owns; this step hands a supplied item back to that check and answers no move of its own (BR9);
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the case-move answer, which is what legacy AC1 asked for and what legacy AC2 tested;
- **no ACE view is read here.** rwb-litigation holds no `v_ace_*` grant and no grant on another `rwb_*` schema (Architecture v5 slides 29 and 41), so the case facts arrive on the P3 answer and the document facts on the P5 contract only.

The recovery vocabulary is the rule vocabulary and not a new one. R-LIT-19 fires on `DOCUMENT_UNRECOVERABLE` — "the document cannot be re-created" — refers to Legal for the affidavit route, records the gap with a reason and moves to `PACK_VERIFIED`; R-LIT-20 is the escape when 90 days or less remain to prescription and the Head of Litigation approves filing with the gap recorded, also to `PACK_VERIFIED` (Business Rules and Routing Logic v4; TSD S4 T4). The step carries those two event codes as its outcome values, and `DOCUMENT_RETRIEVED` of R-LIT-18 as the value that hands the item back to the sibling check; the reason list of R-LIT-19 has no source specification and is carried as a gap (GAP-2761; ASM-4595).

Nothing is published and nothing is consumed as an event. Architecture v5 slide 43 gives rwb-litigation three catalogue events — `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` — and none of them is the recovery of a pack item, while the S4 IN row of slide 19 lists `NoticeDelivered` and `PartnerResultSubmitted`, which belong to the notice and partner-result stories. DP-09 is not in this story's pattern set, so the document fact arrives on the P5 contract synchronously and the case state on the P3 answer; the missing event assignment is recorded (GAP-2763; ASM-4597).

No business value moves: the 10 working days of R-LIT-19, the 90-day prescription warning of R-LIT-20 and the reason list are values in force in the rule package and in reference data, read with their version and never written in code (BR-S4-006).

### 3. Preconditions

- RWB-S4-E5006-CON is published: the two legal-action operations, the recovery element, the outcome vocabulary, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The P5 contract is available with its fake: `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008) of RWB-P5-E1040-APP and `GET /api/recovery/document/v1/cases/{caseId}/documents` (API-P5-002) of RWB-P5-E1026-APP are consumed one hop with a 2 s budget. No P5 contract story carries either as its own baseline, so both are class C dependencies in fact while this story's contract row is None (GAP-2760; ASM-4594).
- The case-move answer of rwb-case is available for the fake. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome that the parent `CaseWorkflow` applies, and where rwb-case publishes a REST case-move operation for another caller its name is Not specified in the source documents (GAP-2760; ASM-4594).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the case-move answer and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 Litigation workspace reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `legal_action` and `hearing` exist in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-029 and the standard record columns of TSD S4 T3.0; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version, with R-LIT-18, R-LIT-19 and R-LIT-20 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`. The Head of Litigation approval of R-LIT-19 and R-LIT-20 is routed on the rwb-decision approval contract and is not built here.
- RWB-S4-E5005-APP holds the defect check and its re-run; the hand-back of a supplied item is a signal to that step and not a second check in this one (BR9).
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on `rwb_document`, `rwb_case` or any other `rwb_*` schema and no `v_ace_*` grant, so a statement on `document`, `document_checklist_item` or `recovery_case` is refused by the database and fails the boundary test (DP-01, DP-05).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5006-CON when its tests pass.

### 4. Flow

1. A case reaches `PACK_DEFECT_HOLD` under R-LIT-17 of RWB-S4-E5005-APP with at least one missing item, and the parent `CaseWorkflow` forwards the stage to the litigation child on task queue `rwb-litigation`.
2. The step reads the legal action on `GET /legal-actions/{legalActionId}` (API-S4-003): the case reference `case_id` (DF-LEG-002), the action type `action_type` (DF-LEG-004) and the status `status` (DF-LEG-014), so the pack it repairs is the pack of a live action.
3. The step reads the case checklist on API-P5-008 and the documents stored on the case on API-P5-002, one hop each with a 2 s budget and a breaker: the item, its document type (`LOV-DOC-TYPE`, DF-DOC-004) and whether the item is still missing (FSD S4 A2.6.2 step 1).
4. The officer opens the recovery path on SCR-19 for one missing item and records the outcome of the attempt: the item was supplied, re-signed or re-created, or it cannot be re-created. The retrieval request itself is raised by rwb-document and its hub on the same checklist answer, not here (FSD S4 A2.6.2 step 2; BR1).
5. Where the item was supplied, the step hands the item back to the defect check of R-LIT-18, which re-reads the checklist and answers its own move; this step writes no record and answers no move for that outcome (BR9).
6. `PackRecoveryEvaluator` loads the LITIGATION package version in force from rwb-decision and evaluates the outcome: R-LIT-19 on `DOCUMENT_UNRECOVERABLE`, and R-LIT-20 when `prescription_days_remaining` is 90 or less and the pack is still on hold (Business Rules and Routing Logic v4).
7. The evaluation answers the rule ID, the package version, the action of the rule and the case move the rule names: `PACK_VERIFIED` under R-LIT-19 and R-LIT-20.
8. `PackRecoveryDecisionRecordWriter` writes one decision record through the local decision-record library, **before any move**: the case reference, the legal action reference, the document type of the item, the outcome, the reason where the item is unrecoverable, the rule ID with its version and the decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC2).
9. Under R-LIT-19 the gap is recorded with its reason on the record of step 8 and referred to Legal for the affidavit route; under R-LIT-20 the Head of Litigation approves filing with the gap recorded on the rwb-decision approval contract, and the step waits for that answer.
10. `PackRecoveryAnswer` answers rwb-case with the case move `PACK_VERIFIED` and its rule, in one transaction with the decision record and the idempotency row. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-2760; ASM-4594).
11. A repeated answer for the same case, document type and rule version writes nothing and sends no second case-move answer; the repeat is counted.
12. SCR-19 Litigation workspace reads the legal action, the checklist state and the recovery outcome from this service and from rwb-document through the gateway-bff composite route, read only, next to the case and its route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing and no case-move answer leaves the service | MSG-P7-003 | AC2, TC-E5-006-02, TC-E5-006-04 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | AC1, TC-E5-006-03 |
| X3 | The legal action does not exist or is outside the scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC1 |
| X4 | The legal action is `CLOSED` or `WITHDRAWN`, or the case is not at `PACK_DEFECT_HOLD` | 409 and nothing changes; no pack is recovered on a closed action | None | AC1 |
| X5 | The P5 checklist read or the case document page does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and no move is answered, and the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X6 | The item names a document type outside `LOV-DOC-TYPE`, or a required field of the request is absent | 422 with MSG-GEN-001; nothing is written and no record is made | MSG-GEN-001 | AC1 |
| X7 | The outcome is `DOCUMENT_UNRECOVERABLE` and no reason is given | 422 with MSG-GEN-001: R-LIT-19 records the gap with a reason, so the step refuses an unrecoverable outcome without one | MSG-GEN-001 | AC1, TC-E5-006-01 |
| X8 | The outcome is `DOCUMENT_UNRECOVERABLE` or `PRESCRIPTION_WARNING` and the Head of Litigation has not answered the approval | The step waits on the approval; no gap is recorded as accepted and no case move is answered | None | AC1 |
| X9 | The same case, document type and rule version arrives twice | One record, one answer; the repeat is counted and no second decision record is written | None | AC1 |
| X10 | A component, a statement or a test reaches a `document` row, a checklist item, a `recovery_case` row, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC3, TC-E5-006-07, Section 17, BR3, BR6 |

X1 to X4 are the exception paths of RWB-E5-006 carried onto the split, X5 to X9 are the paths the target call types and rules add, and X10 is the DP-01 and DP-05 boundary. The 90-day warning of R-LIT-20 and the reason set of R-LIT-19 are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5006-CON, the two P5 reads and the case-move fake, on the tables of its own schema, and needs no live rwb-document, no live rwb-case and no live rwb-decision |
| Negotiable | The activity name, the decision code per rule and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the two operations and the outcome vocabulary are fixed |
| Valuable | A pack that is short of one document moves forward in one recorded step, with the affidavit route named where the item cannot be re-created |
| Estimable | One workflow step, one evaluator, one record write, one client, one case-move answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases and checklist items through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Recover a missing or lost document

  Background:
    Given case "RC-2026-000606" is at "PACK_DEFECT_HOLD" and carries legal action "LA-2026-000606" of action type "CIVIL_CASE" with status "OPEN"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-18, R-LIT-19 and R-LIT-20
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Recover a missing or lost document (legacy RWB-E5-006 AC1)
    Given the rwb-document contract mock returns the checklist of case "RC-2026-000606" with one item of LOV-DOC-TYPE missing and no document row for it
    Given the rwb-case contract mock returns the case state "PACK_DEFECT_HOLD" for "RC-2026-000606"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then opens the recovery path for a document the pack needs and the bank cannot find
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E5-006 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A statement that reaches another schema is refused and fails the build (new, D-RCV-60)
    Given a statement of this service reads a row of rwb_document or rwb_case, or a v_ace_* view
    When the boundary test runs
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC4 The same case, document type and rule version arrives twice (new, D-RCV-60)
    Given the same case, document type and rule version arrives a second time with the same Idempotency-Key
    When the step runs for both requests
    Then one decision record is written, one case move is answered and the repeat is counted

  Scenario: AC5 A supplied item is handed back to the defect check and no record is made here (new, D-RCV-60)
    Given the document is supplied with the outcome DOCUMENT_RETRIEVED
    When the step receives the supplied item
    Then the item is handed back to the defect check of RWB-S4-E5005-APP and no decision record is written and no case move is answered

  Scenario: AC6 The decision record carries no person name, address, contact value or identity number (new, D-RCV-60)
    Given a decision is recorded for case "RC-2026-000606"
    When the decision record is read
    Then it carries case references, document type codes, dates, reason codes and a rule version only

  Scenario: AC7 A provided operation answers 403 or 404 and writes nothing; its 401 answer is Not specified in the source documents (new, D-RCV-60)
    Given a call to a provided operation has no valid identity, or its role does not hold the Litigation right of the operation, or its legal action does not exist or is outside the scope
    When the call is made
    Then the operation answers 403 for the missing right or 404 for the action out of scope, the answer for the missing identity is Not specified in the source documents (NEWAC-RWB-S4-E5006-APP-AC5), and nothing is written

  Scenario: AC8 A workflow step that waits on a consumed call is retried on the workflow's own schedule (new, D-RCV-60)
    Given the P5 checklist read does not answer inside 2 s or its breaker is open
    When the step runs
    Then the step waits and retries on the workflow's own schedule, nothing is written and no case move is answered

  Scenario: AC9 A consumed call that fails or does not answer writes nothing and answers no move (new, D-RCV-60)
    Given the case document page does not answer inside 2 s, or its breaker is open
    When the step runs
    Then nothing is written, no case move is answered and the caller sees 503 with the platform error envelope

  Scenario: AC10 A status change the model does not allow is refused with 409 and nothing changes (new, D-RCV-60)
    Given the rwb-case contract mock returns a case state other than PACK_DEFECT_HOLD for case RC-2026-000606
    When the outcome DOCUMENT_UNRECOVERABLE is recorded
    Then the step answers 409 and nothing changes
```

The two criteria are the legacy criteria of RWB-E5-006 with their origin tag added; the wording `decision log` is changed to `decision record`, and nothing else is changed: the repeated `Then`, the legacy wording of `the action is taken`, `the decision record cannot be written` and `the user acts on the screen` all stand. The cross-service parts are mocked, so AC1 carries two `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-document supplies the checklist and the case documents; this story evaluates R-LIT-19 or R-LIT-20, writes the decision record with the rule version and answers the case move to `PACK_VERIFIED`, and hands a supplied item back to the defect check of R-LIT-18 in RWB-S4-E5005-APP; and rwb-case writes the move. The legacy `document` row of the legacy data table is not read or written as a table anywhere in this story (GAP-2760, GAP-2761; ASM-4594, ASM-4595).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-19 (BR5) | Litigation | D7 | PACK_DEFECT_HOLD | DOCUMENT_UNRECOVERABLE | the document cannot be re-created | Refer to Legal for the affidavit route and record the gap with a reason | PACK_VERIFIED | Head of Litigation | Workbench, the Workbench document hub | 10 working days |
| R-LIT-20 (BR5) | Litigation | D7 | PACK_DEFECT_HOLD | PRESCRIPTION_WARNING | prescription_days_remaining <= 90 | Escalate; the Head of Litigation approves filing with the gap recorded | PACK_VERIFIED | Head of Litigation | Workbench, Workbench scheduler | To the prescription date |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character. Their owner column is a role of the business and not a service: the Head of Litigation approves on the rwb-decision approval contract, and the case move is written by rwb-case on this story's answer. The systems column names the Workbench document hub, which is rwb-document (P5) in the target. **R-LIT-18 (`PACK_DEFECT_HOLD` → `DOCUMENT_RETRIEVED` → `PACK_ASSEMBLY`) is not this story's**: the re-run of the defect check on a supplied item is RWB-S4-E5005-APP's, and this step hands the item back to it.

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The pack-recovery decision and the legal action it repairs are this service's; the document, the checklist item, the retrieval request and the custody of the file are rwb-document's and are read on the owner's contract only | Architecture v5 slide 41; Ownership Map (`document` owner P5; `legal_action` and `hearing` owner S4); TSD S4 T3.1 | AC1, AC3, TC-E5-006-07 |
| BR2 | The decision is recorded before the case move, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 | AC2, TC-E5-006-02, TC-E5-006-04 |
| BR3 | The case move is answered and not written: `recovery_case` and the route states `PACK_DEFECT_HOLD`, `PACK_ASSEMBLY` and `PACK_VERIFIED` are rwb-case's, and this story sends the move with the rule and its version | Ownership Map (`recovery_case` owner P3); Architecture v5 slide 41; GAP-2760 | AC1, AC3, TC-E5-006-07 |
| BR4 | The outcome vocabulary is the rule vocabulary: `DOCUMENT_UNRECOVERABLE` for R-LIT-19, `PRESCRIPTION_WARNING` for R-LIT-20 and `DOCUMENT_RETRIEVED` as the hand-back value of the sibling R-LIT-18; no state name and no list value is written in code | Business Rules and Routing Logic v4; TSD S4 T4; BR-S4-006 (FSD S4 A2.6.3.1) | AC1, TC-E5-006-01 |
| BR5 | The gap of an unrecoverable item is recorded with a reason and referred to Legal for the affidavit route, and a pack close to prescription is escalated to the Head of Litigation, never filed on this step's own authority | R-LIT-19 and R-LIT-20; FSD S4 A2.6.3.1 (VR-S4-006-1) | AC1, TC-E5-006-01 |
| BR6 | No ACE view and no ACE table is read, and no cross-schema join is made: this service holds no `v_ace_*` grant and no grant on `rwb_document` or `rwb_case` | DP-05; Architecture v5 slides 29 and 41 | AC3, TC-E5-006-07 |
| BR7 | The same case, document type and rule version twice, or the same `Idempotency-Key` twice, writes once, answers the move once and counts the repeat | TSD S4 T-A.2 (`Idempotency-Key` on the write operations); Architecture v5 slide 11 | AC4, TC-E5-006-08 |
| BR8 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or an event: the step carries case references, document type codes, dates, reason codes and a rule version | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes | AC6, TC-E5-006-10 |
| BR9 | The defect check and its re-run are not rebuilt here: a supplied item is handed back to R-LIT-18 of RWB-S4-E5005-APP, and this step writes no record and answers no move for that outcome | R-LIT-18 (Business Rules and Routing Logic v4); RWB-S4-E5005-APP sections 1 and 4 | AC5, TC-E5-006-09 |

**Where each rule lives in the target.** R-LIT-19 is the outcome that closes the hold on an item that cannot be re-created, and R-LIT-20 the outcome that closes it when the prescription is 90 days or less away. The timer column of the two rows (10 working days, to the prescription date) is a value of the rule package and of the case timers, not of this build: this story owns no timer and reads the remaining days from the P3 answer. VR-S4-006-1 of the FSD raises MSG-S4-001 when a pack is incomplete at filing; the message is carried in section 14 and raised by the filing story, not by this step.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR3). What this story owns is the decision record and the state of the step.

| From (case route state, rwb-case) | Event | Condition | To |
|---|---|---|---|
| PACK_DEFECT_HOLD | DOCUMENT_UNRECOVERABLE under R-LIT-19 | The document cannot be re-created and the gap is recorded with a reason | `PACK_VERIFIED`, answered by this story |
| PACK_DEFECT_HOLD | PRESCRIPTION_WARNING under R-LIT-20 | prescription_days_remaining <= 90 | `PACK_VERIFIED`, answered by this story on the Head of Litigation approval |
| PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED under R-LIT-18 | The item is supplied, re-signed or re-created | `PACK_ASSEMBLY`, answered by RWB-S4-E5005-APP and not by this step |
| PACK_DEFECT_HOLD | An unrecoverable outcome with no reason, or a document type outside `LOV-DOC-TYPE` | X6, X7 | Unchanged, refused with 422 and MSG-GEN-001 |
| CLOSED, WITHDRAWN or a case not on hold | Any outcome | X4 | Unchanged, refused with 409 |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The parent forwards the stage with at least one missing item | The package in force is loaded | Reading the pack |
| Reading the pack | The P5 checklist and document page answer and the legal action is open | The officer records one item outcome | Evaluating |
| Evaluating | The item was supplied | BR9 | Waiting, handed back to the defect check |
| Evaluating | R-LIT-19 or R-LIT-20 fires | The decision record is written | Answering |
| Answering | The case-move answer is sent | The transaction commits | Waiting for the stage end |
| Answering | The record write or the transaction fails | X1 | Waiting, nothing changed |
| Answering | The outcome needs the Head of Litigation approval | X8 | Waiting on the approval answer |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix and the primary role of the FSD A2.6.3.3: opens the recovery path, records the outcome of an item and reads the pack |
| RW-ENFORCE, enforcement owner | Litigation CRU: reads the pack and records an item outcome in scope |
| RW-LEGAL, legal counsel | Litigation RA: the "also uses" role of the FSD; receives the affidavit route of R-LIT-19 and records its outcome |
| RW-PRODHEAD, RW-HEADLIT | Litigation RA: read, and approve through the approval path of R-LIT-19 and R-LIT-20 |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU: reads its own action and supplies an item through the partner gateway |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it; the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record and answers the case move; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S4 T6.1 and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard of the access service is a service-template capability, so the check is stated here and not built here. The authorise check is a call to rwb-access made at the guard of each operation; its operation name is Not specified in the source documents (DOR-RWB-S4-E5006-APP-6).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the answer and of the record |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the request and on the case-move answer |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`, to refuse a pack on the wrong kind of action |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read, against `LOV-LEGAL-STATUS`: a `CLOSED` or `WITHDRAWN` action is refused with 409 |
| DF-DOC-002, DF-DOC-004 | document (P5, `rwb_document`) | case_id, document_type | Read only through API-P5-008 and API-P5-002: the item of the pack and its type from `LOV-DOC-TYPE` |
| DF-DOC-003, DF-DOC-006, DF-DOC-009, DF-DOC-010 | document (P5, `rwb_document`) | person_key, storage_ref, retention_class, write_once | Not read and not written here: the custody, the file, the retention class and the write-once rule are P5's (BR1) |
| DF-CAS-001, DF-CAS-006, DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, status, stage_code | Read from the P3 answer only, never from a column of this service |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, reason, decided at | Write through the local library, before the case move |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule id, rule version, route set, from_state, event_code and 9 more | Read as the version in force on `RulePackageInForce`, never as a table |
| DF-ACE-001 to DF-ACE-054 | `v_ace_*` views (P1) | the ACE facts | Not read: this service holds no `v_ace_*` grant (BR6) |

Field IDs are those of the TSD S4 Litigation and enforcement v2 T3.1, the Physical Schema and the Logical Data Model and Data Dictionary v9, and the `document` rows are the rows the legacy story lists in its Data table, with their owner changed to P5 by the target. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). The **`document` row, the checklist item, the retrieval request and the file are not created, written or read as tables**; `recovery_case` (P3), `decision_log_entry` (P7) and `rule_row` (P7) are not read as tables either. The recovery element and the "gap with a reason" have no column in `legal_action` and no field list of their own in any source, so they are carried as elements of the CON with the placeholder (GAP-2761; ASM-4595). The fields of this story carry the personal-data class that Data Classification v5 gives them; this story restates no class of its own (DOR-RWB-S4-E5006-APP-11).

**No personal data.** The records this story writes carry identifiers, a document type code, a reason code, dates and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S4-E5006-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, with the action type of `LOV-LEGAL-TYPE` and its pack (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its action type, its status and its pack (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed, withdrawn or wrong-state action, 422 with MSG-GEN-001 for a missing or invalid field, and 503 when the decision library, the P5 contract or the rule package does not answer. API-S4-004 `PATCH /legal-actions/{legalActionId}` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the sibling stories of this service and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008 of `RWB-P5-E1040-APP`) | P5 rwb-document | The checklist of the case type with its version and each item with its document type against `LOV-DOC-TYPE` and its present count; faked |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` (API-P5-002 of `RWB-P5-E1026-APP`) | P5 rwb-document | The documents stored on the case, paged with `type`, `page` and `size`: identifier, document type, stored date; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2760; ASM-4594)) | rwb-case (P3) | P3 rwb-case | The move of the case of record to `PACK_VERIFIED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The P5 rows are contract dependencies listed in this story's contract-dependency row (GAP-1737); the P3 case-move row is recorded as GAP-2760 with ASM-4594. The retrieval request of a missing item is raised by rwb-document and its hub on the same checklist answer and is not a call of this service (BR1). The CCMS path of the FSD integration points is not declared here because no source assigns it an owner (GAP-2764; ASM-4598).

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its three catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result (Architecture v5 slides 19 and 43). This story publishes none of them: DP-09 is not in its pattern set, it writes no outbox row, and its two outputs are the local decision record of DP-03 and the case-move answer of 12.2. No event of a recovered, re-created or unrecoverable document exists on any topic in the catalogue, and the recovery outcome stays on the P5 contract and in the local decision record, so this story publishes none of it (GAP-2763; ASM-4597).

#### 12.4 Events consumed

None. The S4 IN row of Architecture v5 slide 19 lists `NoticeDelivered` and `PartnerResultSubmitted`, which belong to the notice and partner-result stories of this service, and `ProceedsMatched` does not list rwb-litigation among its consumers (slide 43). The document fact therefore arrives on the P5 contract of 12.2, synchronously, and the case state on the P3 answer; this story holds no consumer group, no subscription and no inbox row of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new across the years of the journey; workflow ID form Not specified in the source documents (CG-ALL-9119); start rule and duplicate-start policy Not specified in the source documents (CG-ALL-9119) | `rwb-litigation` | Input: the case, the route R4, the legal action, the missing checklist items and the rule package in force; signals: the case state answered by rwb-case, the rule package in force and the approval answer |
| `recoverMissingDocument` | Activity, the one pack-recovery step of this story | `rwb-litigation` | The case, the legal action and the checklist item in; the rule ID with its package version, the outcome, the reason, the action of the rule and the case move out, with the decision record written before the answer |

The activity name is a target design choice of this story and is fixed by no source document; the defect list check itself, and its re-run on a supplied item, are the step of RWB-S4-E5005-APP and are signalled to, not re-implemented. No timer is registered by this story: the 10 working days and the prescription date are durable timers of the journey's sibling stories (GAP-2761; ASM-4595).

#### 12.6 Schedules

None. The step starts from the parent `CaseWorkflow` when the pack stage finds a missing item, and owns no Temporal Schedule and no legacy Quartz job. The defect check of the pack, the notice timers and the prescription clock of the journey belong to the sibling stories; no Job of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read only in this story: the action type, the status and the case reference; no column is written and none is added |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated request and the answer it holds |

Not owned and never read as a table: `document` and `document_checklist_item` (P5), `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `hearing` (S4, the sibling stories'), and every `v_ace_*` view (P1). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01, DP-05). The `document` row that the legacy story lists is P5's and this story writes no part of it.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document checklist fake (API-P5-008) | The checklist of case `RC-2026-000606` at its version with one item of `LOV-DOC-TYPE` missing; a checklist with every item present; a case with no checklist; no answer beyond 2 s | AC1, X5 |
| rwb-document document-page fake (API-P5-002) | The stored documents of case `RC-2026-000606` paged, with the item absent and with the item present after retrieval; no answer beyond 2 s | AC1, X5 |
| rwb-case case-move fake | The case state `PACK_DEFECT_HOLD` of case `RC-2026-000606`; the move `PACK_VERIFIED` accepted; a move refused because the case is not on hold | AC1, X4 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-18, R-LIT-19 and R-LIT-20, and an approval answer for an unrecoverable item | AC1, X8 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-19 answer for case `RC-2026-000606`, with the legal action and checklist facts read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The case-move answer is stubbed from the published documents and carries the placeholder until its owner confirms it (GAP-2760; ASM-4594).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The create and read of the legal action on `/api/recovery/litigation/v1`; the checklist read, the case document page and the case-move answer; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity | `LitigationWorkflow` and its one pack-recovery step on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here; the stored file is P5's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `pack`, Java package `th.co.scb.ace.workbench.recovery.litigation.pack` with `...pack.recovery`; front end `src/modules/recovery/litigation/PackRecovery.tsx`, the fragment SCR-19 embeds, read and act only on the pack state.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the case-move answer commit together or not at all. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-19 reaches this service, one hop through the gateway. DP-01 and DP-05 apply as prohibitions. Ownership of the schemas named here: `rwb_document` is owned by rwb-document (P5) and `rwb_case` by rwb-case (P3); `rwb_litigation` is this service's own schema. This service holds no grant that would let it read either table (BR1, BR6).

**Dependencies the table adds and the plan does not hold.** The two platform contracts of the pattern table, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`, are in the build list; the three consumed rows of 12.2 are class C dependencies in fact; the contract-dependency row names the P5 and the P8 and P10 edges (GAP-1737), so the story builds against their documents and fakes on Day 1, and the P3 case-move row is recorded as GAP-2760 with ASM-4594. The three consumed rows of 12.2 are carried as non-blocking consumed contracts: the checklist read and the case document page are read through API-P5-008 of RWB-P5-E1040-APP and API-P5-002 of RWB-P5-E1026-APP, and the case-move answer of rwb-case is confirmed by the rwb-case owner when its contract story is written. The metadata rows are unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` pack branch | Workflow | The step of the journey that waits for the checklist, the item outcome and the approval, and reports the outcome to the parent |
| `recoverMissingDocument` | Activity | The one step: read the legal action and the checklist, take the item outcome, evaluate R-LIT-19 or R-LIT-20, write the record and answer the case move |
| `PackRecoveryEvaluator` | Service | The rule evaluation against the LITIGATION package version in force, with the outcome codes `DOCUMENT_UNRECOVERABLE` and `PRESCRIPTION_WARNING` |
| `PackRecoveryDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID, the version and the reason before any answer, hash-linked, and refuses the step when the write fails (DP-03) |
| `DocumentChecklistClient` | Client | The checklist read and the case document page of the P5 contract, one hop, 2 s, breaker, and no retry of its own; the CCMS leg of the item request is reached only through this contract (GAP-2764) |
| `PackRecoveryAnswer` | Signal reporter | Answers rwb-case with the case move, the rule and the version; it reports, it never changes a case row |
| `PackRecoveryController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `PackRecovery` | React component | Shows the pack, the missing items and the outcome on SCR-19, with the refusal and failure states |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the request, the item state or the reason: those are facts of the request and of the answer, and storing them would copy another service's facts into this schema (GAP-2761; ASM-4595).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE`, `LOV-LEGAL-STATUS` and `LOV-DOC-TYPE` at their version in force (TSD S4 T3.2; reference data of the module), read as reference data and never as constants.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the working-day timers, the 90-day warning and the reason set are values of the package and of reference data, not of this build (BR-S4-006).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The pack branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`.
2. `DocumentChecklistClient` against the two P5 fakes, with the 2 s budget, the breaker and the no-answer path (AC1, X5).
3. The recovery path on SCR-19 and the item outcome it records, with `LOV-DOC-TYPE` and the 422 paths (AC1, X6, X7).
4. `PackRecoveryEvaluator` over the LITIGATION package, with the two rules and their outcome codes (AC1).
5. `PackRecoveryDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `PackRecoveryAnswer` and the parent signal, with the move and the approval wait (AC1, X8).
7. The hand-back of a supplied item to the defect check of RWB-S4-E5005-APP, with no record and no move of this step (BR9).
8. `PackRecoveryController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1).
9. `PackRecovery` and SCR-19 through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no read or write of `rwb_document` or `rwb_case` (X10, BR1, BR6).

**Feature flag.** `rwb.litigation.pack-recovery-v1`, read as a flag of the platform library; off means the pack stays on hold, the screen shows the read-only pack and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic checklist in SIT, R-LIT-19 and R-LIT-20 each produce their record and their move, a repeated answer writes once, a forced record failure changes nothing, no `document` row and no `recovery_case` row is written from this service, and SCR-19 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set of this key (VR-S4-006-1). It names a missing item of the litigation pack at filing, which is the filing story of this service, so no path of this step raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which is the prescription fact of this service and its screen text, so no path of this step raises it | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid, a document type is outside `LOV-DOC-TYPE`, or an unrecoverable outcome carries no reason (X6, X7) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or opens the pack (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case move (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are the message set of the legacy story, copied unchanged; no message is reworded and no new one is added. No source gives the wording of a retrieval failure on the P5 side, so that path answers the platform error envelope and carries no message of its own (GAP-2761; ASM-4595).

### 15. Screens and states

SCR-19 Litigation workspace carries the pack in its `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `PACK_VERIFIED` states, which are rwb-case's route states read from its answer, and the recovery path of this story is visible only in `PACK_DEFECT_HOLD`. The screen reads the legal action, the checklist and the item outcomes from this service and from rwb-document through the gateway-bff composite route (DP-19), one hop per call; the composite route specification and the screen field list belong to RWB-PLT-N001-CON. SCR-20 Enforcement workspace is listed by the legacy story and is not touched by this step: it reads the legal action and its enforcement facts, which are the sibling stories' answers. The refusal and failure states the officer sees — refused, not on hold, no reason, not recorded — read the messages of section 14 on the same route. The empty, loading, error and no access states of SCR-19 are Not specified in the source documents (CG-ALL-9124), because Screen Specifications v1 lacks them. The empty, loading, error and no access states of SCR-20 are Not specified in the source documents (CG-ALL-9125), because Screen Specifications v1 lacks them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-006-01 | AC1 | End to end | Case `RC-2026-000606`, legal action `LA-2026-000606`, one checklist item of `LOV-DOC-TYPE` missing on the P5 fakes; the unrecoverable path records the reason and answers `PACK_VERIFIED`, and the supplied path hands the item back to the defect check |
| TC-E5-006-02 | AC2 | Component | The decision-record stub stopped; nothing changes and the officer sees MSG-P7-003 |
| TC-E5-006-03 | Access | Component | RW-AUDIT holds Litigation R only; the attempt to record an item outcome is refused with MSG-P4-002 and nothing changes |
| TC-E5-006-04 | Principle 5 | NFR | A forced decision-record write failure stops the step with MSG-P7-003; no record, no move and no `document` row |
| TC-E5-006-05 | Contract of section 12 (operations, events, activities) | Contract | The contract fakes of section 12.8 behind the operations, events and activities of section 12.5; no new fixture value |
| TC-E5-006-06 | Boundary of the section 12.7 tables (ASM-3438) | Component | Each table of section 12.7 at its boundary, including the `decision_record` and `idempotency_key` library tables |
| TC-E5-006-07 | AC3 boundary: a statement that reaches rwb_document, rwb_case or a v_ace_* view is refused | Component | Grant refusal and failed build for each such statement (X10, BR1, BR3, BR6) |
| TC-E5-006-08 | AC4 repeat of the same case, document type and rule version | Component | One decision record, one case move answer and a counted repeat (X9, BR7) |
| TC-E5-006-09 | AC5 supplied item handed back to the defect check of R-LIT-18 | Component | No decision record and no case move from this step for DOCUMENT_RETRIEVED (BR9) |
| TC-E5-006-10 | AC6 decision record carries no personal data | Component | The record holds case references, codes, dates, reason codes and a rule version only (BR8) |
| TC-E5-006-11 | AC7 provided operation answers 403 or 404 and writes nothing; its 401 answer is Not specified in the source documents | Component | Not specified in the source documents (NEWAC-RWB-S4-E5006-APP-AC5) |
| TC-E5-006-12 | AC8 consumed call waits and is retried on the workflow's schedule | Component | Not specified in the source documents (NEWAC-RWB-S4-E5006-APP-AC7) |
| TC-E5-006-13 | AC9 consumed call that fails or does not answer writes nothing | Component | Not specified in the source documents (NEWAC-RWB-S4-E5006-APP-AC8) |
| TC-E5-006-14 | AC10 disallowed status change is refused with 409 | Component | Not specified in the source documents (NEWAC-RWB-S4-E5006-APP-AC9) |

The four legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step (AC1, the "System" level of the legacy story) maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The fakes and the stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000606`, legal action `LA-2026-000606`, the case on `PACK_DEFECT_HOLD` and one missing checklist item — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the 10 working days, the 90-day prescription warning, the reason set and the lists stay data, reference data or the rule package, never a constant (BR-S4-006).
- No personal data in a record, a log, a workflow input or a test: identifiers, a document type code, a reason code, dates and a rule version only; every fixture is synthetic.
- The document stays with rwb-document: this story writes no `document` row, no checklist item, no retrieval request, no file, no retention class and no write-once flag (BR1).
- The case stays with rwb-case: this story writes no `recovery_case` row and no route state, and it answers the move with its rule and version (BR3).
- The defect check is not duplicated: a supplied item is handed back to R-LIT-18 of RWB-S4-E5005-APP and this step answers no move for it (BR9).
- ACE data only through the owner's contract: no `v_ace_*` view, no ACE table and no grant on another `rwb_*` schema; the boundary test fails a build that adds one (DP-05, BR6).
- One base, one topic, one queue and one login per service; a class that names another service's base, topic or queue fails the review (DP-13, DP-14).
- No retired element is reintroduced: the absence test fails a build that declares an event, a Schedule, a Quartz row or a shared job table for this step.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested (FSD S4 requirements served; Business Requirements Program v5). The legacy story master carries no requirement ID and the key is mapped to this requirement of the module (GAP-2762; ASM-4596) | The pack-recovery step, the two rules and the case-move answer | TC-E5-006-01, TC-E5-006-02 | FEAT-LIT-06 | Not specified in the source documents (DOR-RWB-S4-E5006-APP-2) |
| FEAT-LIT-06 | Recover a missing or lost document, the feature of FSD S4 A2.6 and of the Epics 3 to 8 specification (row E5, S4) | The whole story | TC-E5-006-01 to TC-E5-006-04 | FEAT-LIT-06 | Not specified in the source documents (DOR-RWB-S4-E5006-APP-2) |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows of 12.2 with their budget and breaker | TC-E5-006-01 | FEAT-LIT-06 | Not specified in the source documents (DOR-RWB-S4-E5006-APP-2) |
| ADR-022 | Local decision record plus the central ledger | The record written before the case move | TC-E5-006-02, TC-E5-006-04 | FEAT-LIT-06 | Not specified in the source documents (DOR-RWB-S4-E5006-APP-2) |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E5-006, disposition Split (rework) |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word here |
| Test cases | TC-E5-006-01 to TC-E5-006-04, kept from the legacy story |
| Feature and screens | FEAT-LIT-06, SCR-19 Litigation workspace and SCR-20 Enforcement workspace |
| Rules | R-LIT-19 and R-LIT-20 from the Business Rules and Routing Logic v4, governed in rwb-decision; R-LIT-18 is RWB-S4-E5005-APP's |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |
| Screen states | SCR-19 and SCR-20 empty, loading, error and no-access states: Not specified in the source documents (DOR-RWB-S4-E5006-APP-10) |
| Reference data | LOV-DOC-TYPE for the checklist item type and the LITIGATION rule package in force from rwb-decision; parameters Not specified in the source documents (DOR-RWB-S4-E5006-APP-20); reference-data contract under DP-06 and DP-07 |

### 19. Out of scope

- The published shape of the two operations, the recovery element, the outcome vocabulary, the error set and the fakes: RWB-S4-E5006-CON.
- The document, the checklist item and the checklist per case type, the retrieval request, the intake, the OCR text, the custody, the stored file, the retention class and the write-once rule: rwb-document (P5), on the contract of 12.2. **This story writes no part of them** (GAP-2760; ASM-4594).
- The case of record, its route states `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `PACK_VERIFIED`, the case timers and the parent `CaseWorkflow`: rwb-case (P3), whose answer this story calls and never writes.
- The defect list check and its re-run on a supplied item (FEAT-LIT-05, R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32): RWB-S4-E5005-APP, to which this step hands a supplied item.
- The assembly of the pack (FEAT-LIT-04), the verification of the pack and the approval of the filing (FEAT-LIT-07), the notice path and the law firm instruction: the sibling stories of this service, including `RWB-S4-E5021-APP`.
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-19 and R-LIT-20, and the Head of Litigation approval: rwb-decision (P7).
- The CCMS path of the FSD integration points: no source assigns it an owner in the target (GAP-2764; ASM-4598).
- The ACE account, customer and batch facts and the freshness check: rwb-source-data (P1); this service holds no `v_ace_*` grant.
- The gateway-bff composite route and the screen field list of SCR-19 and SCR-20: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

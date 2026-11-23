# RWB-S4-E5005-APP Check the pack against the defect list

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5005-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5005-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-005 for rwb-litigation. The four legacy acceptance criteria are kept word for word with their origin tag. The known defect list is the document checklist of rwb-document (FEAT-DCM-16, API-P5-008) and the pack documents are that service's case document page (API-P5-002), so the legacy `document` row and the legacy `rule_row` read are retired and the two facts arrive on the owner's contracts; the case route states `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `FILING_REJECTED` stay with rwb-case and are answered, never written here; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the pack state changes (DP-03); the base becomes `/api/recovery/litigation/v1` (DP-13); SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19). The identity of the defect list with the P5 checklist, the trigger of the check and the missing element shapes are carried as the working read of the assumption (GAP-2758, GAP-2759; ASM-4588, ASM-4590, ASM-4592). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the Workbench to test the litigation pack of a case against the known defect list, name every item that is missing and record the result with the rule version before the pack state moves**, so that **a pack reaches court complete in 6 days instead of 21, and no filing is rejected for a document a person could have seen was absent**.

This is the application slice of legacy RWB-E5-005. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- one pack-defect check step of `LitigationWorkflow` on task queue `rwb-litigation` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case (Architecture v5 slide 19);
- the evaluation of R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 on the checklist of the case type and on the documents actually stored on the case, with the LITIGATION package version in force;
- the two operations of this key on base `/api/recovery/litigation/v1`: `POST /cases/{caseId}/legal-actions` (API-S4-002) and `GET /legal-actions/{legalActionId}` (API-S4-003), under capability area "Litigation" with the rights C and R (DP-13; TSD S4 T-A.1);
- the local decision record of the check, written through RWB-PLT-E1027-CON before the pack state changes (DP-03);
- the answer to rwb-case for the case move `PACK_DEFECT_HOLD` or `PACK_ASSEMBLY`, with the rule ID and the version that produced it;
- the pack state and the named missing items on SCR-19 Litigation workspace, read through the gateway-bff composite route (DP-19).

It does not own: the published shape of the two operations, the missing-item element, the consumed rows, the error set and the fakes, which are RWB-S4-E5005-CON; the document checklist per case type and the stored documents of the case, which are rwb-document (P5) on API-P5-008 and API-P5-002; the retrieval request, the re-signed or re-created document and the CCMS exchange, which are the document hub's; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the LITIGATION package and its rule rows, which are rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key and the wave 3 harness.

### 2. Business rationale

Legacy RWB-E5-005 gave the Workbench one step that tested a pack against a known defect list and named what was missing, and it kept four rule outcomes: R-LIT-16 presented the pack for verification when every defect list item was present, R-LIT-17 held the pack when one or more items were missing, R-LIT-18 re-ran the check when the missing items were supplied, re-signed or re-created, and R-LIT-31 and R-LIT-32 returned a court-rejected filing to rework and re-ran the check before re-filing. The functional specification keeps the objective and its metric — a litigation turnaround of 6 days against the 21 days a filing takes today, measured on the decision log and the Workbench records, reviewed monthly (FSD S4 A2.5.1) — and the program keeps the requirement: REQ-S4-002, "A litigation pack is assembled and checked against the document checklist, and missing documents are requested" (FSD S4 Requirements served; Business Requirements Program v4).

What D-RCV-60 changes is where the list and the documents live. In the monolith the pack, the documents, the defect list and the decision log row sat in one `recovery` schema and one process. In the target:

- **the defect list is reference data of rwb-document (P5).** FEAT-DCM-16 holds the document checklist per case type, "so completeness is checked against data rather than memory" (FSD P5 A2.16), and that story states that the checklist is the source the pack checks of Epics 4 and 5 read (R-LIT-16, R-LIT-17). The check therefore reads `GET /cases/{caseId}/document-checklist` (API-P5-008) and the stored documents of the case on `GET /cases/{caseId}/documents` (API-P5-002) and holds no list of its own (GAP-2758; ASM-4588);
- **the case of record stays with rwb-case (P3).** `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD`, `PACK_VERIFIED` and `FILING_REJECTED` are route states of the case of record, written there and not here. This story evaluates the rule, records the decision and **answers** the case move (GAP-2758; ASM-4589);
- **the pack state, the retrieval request and the documents stay with rwb-document and rwb-case.** This service holds `legal_action` and `hearing` only (Ownership Map), so it writes no document row, no document type and no checklist version;
- **the decision is recorded first**, through the local decision-record library of DP-03 in the same transaction as the case answer, which is what legacy AC1 asked for and legacy AC4 tested;
- **no ACE view is read here.** rwb-litigation holds no `v_ace_*` grant (Architecture v5 slide 29) and the legacy data table of this key lists no ACE row, so DP-05 is not in the pattern set and the story declares no such read.

The check is not carried by an event. DP-09 is not in this story's pattern set, the S4 IN row of Architecture v5 slide 19 lists only `NoticeDelivered` and `PartnerResultSubmitted`, and the `DocumentStored` event of rwb-document lists its consumers elsewhere. The re-run of AC2 and AC3 is therefore started inside the workflow: the parent `CaseWorkflow` forwards the case stage signal, and the step re-reads the checklist and the documents from their owners (GAP-2759; ASM-4590).

No business value moves. The checklist items, their required flag and their order are rows of `document_checklist_item` with a version and a valid-from date, read with their version and never written in code; the packaging of the file, the item labels and the sort order are the hub's data.

### 3. Preconditions

- RWB-S4-E5005-CON is published: the two legal-action operations, the pack and missing-item elements, the consumed rows, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-document reads of this key are published by their owner: `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` (API-P5-008) of RWB-P5-E1040-APP and `GET /api/recovery/document/v1/cases/{caseId}/documents` (API-P5-002) of RWB-P5-E1026-APP. No P5 contract story carries either operation as its own baseline, so both are class C dependencies of this story in fact while its contract-dependency row is None, and the absence is recorded (GAP-2758; ASM-4589).
- The case read and the case-move answer of rwb-case are available for the fake. No source names a published operation that moves a case state on behalf of a stage, and the name is Not specified in the source documents (GAP-2758; ASM-4589); on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies.
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003, so the record and the case answer commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-19 Litigation workspace and SCR-20 Enforcement workspace reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- `legal_action` and `hearing` exist in schema `rwb_litigation` from the DB story of this service, with the columns of DF-LEG-001 to DF-LEG-029 and the standard record columns of TSD S4 T3.0; this story adds no table, no column and no migration.
- The LITIGATION rule package is in force at its version, with R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 in it; the package is authored, tested and approved in rwb-decision (P7) and loaded here on `RulePackageInForce`.
- The service runs as its own login on schema `rwb_litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_document`, `rwb_case` or a `v_ace_*` view is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S4-E5005-CON when its tests pass (GAP-2759; ASM-4593).

### 4. Flow

1. A case enters `PACK_ASSEMBLY` under R-LIT-15 or R-LIT-11; the parent `CaseWorkflow` forwards the stage to the litigation child on task queue `rwb-litigation`.
2. The step opens the legal action of the case on `GET /legal-actions/{legalActionId}` (API-S4-003): its action type of `LOV-LEGAL-TYPE`, its status and its case reference. Where the case has no litigation legal action yet, `POST /cases/{caseId}/legal-actions` (API-S4-002) opens it and its pack (GAP-2759; ASM-4592).
3. `ChecklistClient` reads the checklist of the case type on API-P5-008: the checklist version, the stage code, and each item with its document type, label, required flag and present count. Where the stage has no checklist rows, the answer carries the empty state and no count, and that state is recorded, not invented.
4. `PackDocumentClient` reads the documents stored on the case on API-P5-002, one page at a time, and keeps the document type and the document reference of each; it reads no field value and no content.
5. `PackDefectEvaluator` loads the LITIGATION package version in force and evaluates R-LIT-16, R-LIT-17, R-LIT-18 or R-LIT-32 on the two answers: every required item present, one or more missing, the missing items now supplied, or a court-rejected defect corrected.
6. The evaluation answers the rule ID, the package version, the missing items with their document type and label, and the case move the rule names.
7. `PackDefectDecisionRecordWriter` writes one decision record through the local library, **before any change**: the case reference, the legal action reference, the rule ID with its version, the checklist version, the inputs reference, the missing item count and the outcome. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `PackDefectAnswer` sends the summary to the pack surface and answers rwb-case with the case move `PACK_DEFECT_HOLD` under R-LIT-17 or `PACK_ASSEMBLY` under R-LIT-18 and R-LIT-32, with the rule ID, the version and the missing item count. rwb-case writes the `recovery_case` row and its route state; this service writes neither (GAP-2758; ASM-4589).
9. The officer reads the pack on SCR-19: the checklist version, each required item marked present or missing, and MSG-S4-001 naming the missing item before a filing is attempted (legacy AC1; FSD S4 A2.5.3.1 VR-S4-005-1).
10. Under R-LIT-17 the retrieval requests of the missing items are raised by rwb-document and the hub, not here; when the document arrives the parent forwards the stage again and step 3 re-runs the check on the same version (legacy AC2; R-LIT-18).
11. Under R-LIT-31 the court returns the filing for a defect: the filing story records the defect and the case reaches `FILING_REJECTED`; on `PACK_REWORKED` this step re-runs the check and answers `PACK_ASSEMBLY` so the pack can be re-filed (legacy AC3; R-LIT-32).
12. A repeated stage signal for the same case, rule and checklist version writes nothing, sends no second case answer and counts the repeat.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing: the pack state keeps its value and no case answer leaves the service | MSG-P7-003 | AC4, TC-E5-005-04, TC-E5-005-06 |
| X2 | The role does not hold the Litigation right of the operation | 403 before any read or write; nothing changes and no decision record is written | MSG-P4-002 | TC-E5-005-05 |
| X3 | The legal action does not exist or is outside the scope | 404 and nothing is written; the caller cannot tell an out-of-scope action from a missing one | None | AC1, AC2 |
| X4 | The checklist read does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is answered and the caller sees 503 with the platform error envelope | None | AC1, AC2 |
| X5 | The case type has no checklist rows | The check states the empty checklist, writes the record with that state and answers no pack move; the pack stays where it is | None | AC1 |
| X6 | A required item is missing at filing | The pack is held and the missing item is named before the filing is attempted | MSG-S4-001 | AC1, AC2 |
| X7 | The claim on the case is inside the prescription warning window | The message is displayed; the warning itself is raised by the prescription rules of the sibling stories | MSG-S4-002 | AC2, AC3 |
| X8 | The same case, rule and checklist version arrive twice | One record, one case answer; the repeat is counted and no second record is written | None | AC1, AC2 |
| X9 | A component, a statement or a test reaches a `rwb_document`, `rwb_case` or `v_ace_*` object | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5 |

X1 to X2 are the exception paths of RWB-E5-005 carried onto the split, X4 and X9 are the paths the target call types and schemas add, and X3, X5 to X8 are the pack conditions the FSD states.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S4-E5005-CON, the two rwb-document reads, the rwb-case answer and the decision-record stub; needs no live rwb-document, no live rwb-case and no live rwb-decision |
| Negotiable | The activity name, the decision code and the shape of the missing-item answer are this story's choice; the rules, the messages, the two operations and the route states are fixed |
| Valuable | A pack is checked against data the hub owns, the missing items are named before filing, and the result is recorded with the rule version in one step |
| Estimable | One workflow step, one evaluator, one record write, two clients, one case answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, checklists and document sets through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Check the pack against the defect list

  Background:
    Given case "RC-2026-000705" carries the litigation legal action "LA-2026-000705" on base "/api/recovery/litigation/v1"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Check the pack against the defect list (legacy RWB-E5-005 AC1)
    Given the rwb-document contract mock returns the checklist of case "RC-2026-000705" with its items and the documents stored on it
    Given the rwb-case contract mock returns the case state "PACK_ASSEMBLY" for "RC-2026-000705"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then tests the pack against the known defect list and names what is missing
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-18 (legacy RWB-E5-005 AC2)
    Given the rwb-document contract mock returns the missing item now stored for case "RC-2026-000705"
    Given the rwb-case contract mock returns the case state "PACK_DEFECT_HOLD" for "RC-2026-000705"
    Given a case in state PACK_DEFECT_HOLD
    When document retrieved
    Then re-run the defect list check
    Then the case moves to PACK_ASSEMBLY

  Scenario: AC3 Rule R-LIT-32 (legacy RWB-E5-005 AC3)
    Given the rwb-document contract mock returns the corrected item for case "RC-2026-000705"
    Given the rwb-case contract mock returns the case state "FILING_REJECTED" for "RC-2026-000705"
    Given a case in state FILING_REJECTED
    When pack reworked
    Then re-run the defect list check and re-file
    Then the case moves to PACK_ASSEMBLY

  Scenario: AC4 Not recorded (legacy RWB-E5-005 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E5-005 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the action is taken`, `the decision log cannot be written`, `document retrieved` and `its trigger arrives` all stand. The cross-service parts are mocked, so AC1 to AC3 each carry `Given the <service> contract mock returns <x>` lines, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: this story evaluates R-LIT-16, R-LIT-17, R-LIT-18 or R-LIT-32 and writes the decision record with the rule version; rwb-document answers the checklist, the stored documents and the retrieval request; and rwb-case writes the case move. The legacy `document` and `rule_row` rows of the legacy data table are not read as tables anywhere in this story (GAP-2758; ASM-4588).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-16 | Litigation | D7 | PACK_ASSEMBLY | PACK_COMPLETE | every defect list item present | Present the pack to the litigation officer for verification | PACK_VERIFIED | Litigation officer | Document Hub, CCMS, LHS, the Workbench document hub | 2 working days |
| R-LIT-17 | Litigation | D7 | PACK_ASSEMBLY | PACK_INCOMPLETE | one or more defect list items missing | Raise retrieval requests and hold the pack | PACK_DEFECT_HOLD | Litigation officer | Document Hub, the Workbench document hub | 5 working days |
| R-LIT-18 | Litigation | D7 | PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED | missing items supplied, re-signed or re-created | Re-run the defect list check | PACK_ASSEMBLY | Workbench | Document Hub, the Workbench document hub | 1 working day |
| R-LIT-31 | Litigation | D7 | FILED_IN_COURT | COURT_REJECTED_FILING | the court returns the filing for a defect | Record the defect and return the pack for rework | FILING_REJECTED | Litigation officer | Partner Portal, LIT | 5 working days |
| R-LIT-32 | Litigation | D7 | FILING_REJECTED | PACK_REWORKED | the defect is corrected | Re-run the defect list check and re-file | PACK_ASSEMBLY | Workbench | Document Hub | 3 working days |

The five rows are the rows of the Business Rules and Routing Logic v4, copied character for character. R-LIT-31 is carried because it is the only way a case reaches `FILING_REJECTED`; its record is the filing story's and this story only re-runs the check on R-LIT-32. The owner column is a role of the business and not a service: the case move is written by rwb-case on this story's answer, and the "Workbench" owner of R-LIT-18 and R-LIT-32 is the record this story writes.

| ID | Rule | Source |
|---|---|---|
| BR1 | The defect list is the document checklist of rwb-document and is never copied here: the check reads the checklist and the stored documents of the case on the owner's operations and holds no list row of its own | FEAT-DCM-16 (FSD P5 A2.16; Epics 3 to 8 specification); RWB-P5-E1040-APP section 12 (API-P5-008); GAP-2758 |
| BR2 | The decision is recorded before the pack state changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S4 T2 ("writes the decision log entry before any change"); legacy AC1 and AC4 |
| BR3 | The case move is answered and not written: `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `FILING_REJECTED` are rwb-case's route states, and this story sends the move with the rule and its version | Ownership Map (recovery_case owner P3); Architecture v5 slide 41; GAP-2758 |
| BR4 | A missing required item is named before a filing is attempted, and it names the item the checklist version in force requires | FSD S4 A2.5.3.1 VR-S4-005-1 (MSG-S4-001); R-LIT-17; FEAT-DCM-16 |
| BR5 | No document row, checklist row, case row or ACE view is read or written here: the facts arrive on the owner's contract and the service holds no grant on another schema | DP-01; Architecture v5 slide 29 (no `v_ace_*` grant for rwb-litigation) |
| BR6 | The same case, rule and checklist version twice writes once, answers the case move once and counts the repeat | TSD S4 T-A.2 (`Idempotency-Key` on the create); Architecture v5 slide 11 |
| BR7 | The vocabulary is closed: `LOV-LEGAL-TYPE` is NOTICE, CIVIL_CASE, APPEAL, ENFORCEMENT, BANKRUPTCY_PETITION, LED_AUCTION; `LOV-LEGAL-STATUS` is OPEN, FILED, JUDGMENT, ENFORCING, CLOSED, WITHDRAWN; no state name and no list value is written in code | TSD S4 T3.2; BR-S4-005 (FSD S4 A2.5.3.1) |
| BR8 | No personal data enters `rwb_litigation`, the decision record, a log or a workflow input: the step carries case and legal action references, checklist and document type codes, counts, dates and a rule version | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |

**Where each rule lives in the target.** R-LIT-16 and R-LIT-17 are the two outcomes of the first pass: the evaluator compares the required items of the checklist version in force with the document types stored on the case, the record is written, and the case answer carries `PACK_VERIFIED` when nothing is missing or `PACK_DEFECT_HOLD` when something is. R-LIT-18 and R-LIT-32 are the two re-runs: the check is repeated on the same or a newer checklist version and the case answer carries `PACK_ASSEMBLY`. The checklist version, the required flag and the item order are rows with a valid-from date and are read with their version; the 2, 5, 1, 5 and 3 working-day service levels are timers of rwb-case and of the hub, not of this step.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story owns is the state of its own step.

| From (case of record) | Event | Condition | To |
|---|---|---|---|
| PACK_ASSEMBLY | PACK_COMPLETE under R-LIT-16 | Every defect list item present | `PACK_VERIFIED`, with the verification task raised by rwb-case |
| PACK_ASSEMBLY | PACK_INCOMPLETE under R-LIT-17 | One or more defect list items missing | `PACK_DEFECT_HOLD`, with MSG-S4-001 naming the item |
| PACK_DEFECT_HOLD | DOCUMENT_RETRIEVED under R-LIT-18 | Missing items supplied, re-signed or re-created | `PACK_ASSEMBLY`, and the check re-runs |
| FILING_REJECTED | PACK_REWORKED under R-LIT-32 | The defect is corrected | `PACK_ASSEMBLY`, and the check re-runs before the re-filing |
| Any of the four | The same stage signal twice for the same rule and checklist version | X8 | Unchanged, one record and one answer |
| PACK_ASSEMBLY | The checklist read does not answer | X4 | Unchanged, nothing recorded and no answer sent |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The parent forwards `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` or `FILING_REJECTED` | The package in force is loaded | Reading |
| Reading | The checklist and the document page answer | The evaluator runs | Evaluating |
| Evaluating | A rule fires | The decision record is written | Answering |
| Answering | The record is committed and the case answer is sent | The transaction commits | Waiting for the next stage |
| Answering | The record write or the transaction fails | X1 | Waiting, nothing changed |

The state names are the LITIGATION states of the Business Rules and Routing Logic v4 and of TSD S4 T4; no state is added, renamed or written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix: opens and reads the legal action, reads the pack and the missing items, and acts on the verification task of the sibling story |
| RW-ENFORCE, enforcement owner | Litigation CRU: reads the pack of the case and the missing items of an enforcement action |
| RW-LEGAL, legal counsel | Litigation RA: reads the pack, the checklist version and the missing items |
| RW-PRODHEAD, RW-HEADLIT | Litigation RA: read, and approve through the approval path where a rule routes to them |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| PT-LAWFIRM, law firm user | Litigation RU: reads its own action and the pack it was instructed with, through the partner gateway |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Litigation R or U as the TSD S4 T6.1 matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-litigation service identity | Runs the step, evaluates the rules, writes the decision record and answers the case move; it holds no grant on another schema |

The rights above are the rows of TSD S4 T6.1 and nothing wider. The FSD says the feature "runs unattended" with the litigation officer as also-user, and both statements hold: the step runs under the service identity with no officer task on the happy path, and the litigation officer is the primary role when a person reads the pack or acts on a held item. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation, and the guard of rwb-access is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Read, as the legal action reference of the record and of the answer |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Read, and sent on the case answer |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Read, against `LOV-LEGAL-TYPE`, to know that the action is a litigation action |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Read only: this step changes no legal action status |
| DF-LEG-024 to DF-LEG-029 | hearing (S4, `rwb_litigation`) | the hearing rows | Neither read nor written: the hearing calendar is the sibling stories' |
| DF-DOC-001 to DF-DOC-011 | document (P5, `rwb_document`) | id, document_type, case_id and 8 more | Read only on API-P5-002; the type of each stored document is what the check compares |
| DF-REF-234 to DF-REF-243 | document_checklist_item (P5, `rwb_document`) | stage_code, route_code, document_type, required, sort_order, table_version, valid_from and 3 more | Read only on API-P5-008; the required flag and the item order drive the result |
| DF-DOC-036 to DF-DOC-044 | case_document_check (P5, `rwb_document`) | case_id, checklist_version, required_count, present_count, missing_types, complete and 3 more | Read only on the same answer: the hub's own completeness flag is not recomputed or stored here |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, status, stage_code and 19 more | Read only through the case answer; the route state is written by rwb-case |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | rule id, rule version, inputs reference, outcome, decided at and 13 more | Write through the local library, before the case answer |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read: the rule package arrives on `RulePackageInForce` from rwb-decision |

Field IDs are those of TSD S4 Litigation and enforcement v2 T3.1, TSD P5 and the Logical Data Model and Data Dictionary v8. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, this story writes no column of them, and `decision_record` and `idempotency_key` are platform library objects created in `rwb_litigation` by the library's own migration (DP-03). The legacy data rows of this key for `document`, `decision_log_entry` and `rule_row` are read on their owners' contracts or not at all.

**No personal data.** The rows this story reads and writes carry identifiers, document type codes, counts, dates, list values and a rule version. No name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). This story supplies the behaviour behind two operations whose shapes are declared by RWB-S4-E5005-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in, LegalAction of status 201 out, opening the action and its pack with the action type of `LOV-LEGAL-TYPE` (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` header required |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with the pack element: the checklist version, the items, the missing items and the outcome of the last check (API-S4-003) | Litigation, right R, scope applied | Not applicable |

The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope action, 409 for a closed or withdrawn action, 422 with MSG-GEN-001 for a missing or invalid field and MSG-S4-001 for a held pack, and 503 when the decision library, the rwb-document read or the rule package does not answer. The operation IDs are those of TSD S4 T-A.1 and are not redefined here; API-S4-004 `PATCH /legal-actions/{legalActionId}` and API-S4-005 `POST /legal-actions/{legalActionId}/hearings` belong to the filing, judgment and hearing stories of this service and are not built here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/cases/{caseId}/document-checklist` (API-P5-008) | P5 rwb-document | The checklist of the case type: the checklist version, the stage and the items with their document type, label, required flag and present count; faked |
| GET | `/cases/{caseId}/documents` (API-P5-002) | P5 rwb-document | The documents stored on the case, page by page, with their document type and reference; the retrieval request of R-LIT-17 is the hub's, not this story's; faked |
| The case read and the case-move answer (operation name Not specified in the source documents (GAP-2758; ASM-4589)) | rwb-case (P3) | P3 rwb-case | The case reference and the route state, and the answer that carries `PACK_DEFECT_HOLD` or `PACK_ASSEMBLY` with the rule and its version; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The rows are contract dependencies of class C in fact, because the plan's contract-dependency row of this story is None, and the absence is recorded as GAP-2758 with ASM-4589. The two P5 operations are published by the app stories of the hub and no P5 contract story carries them as a baseline, which is the same gap.

#### 12.3 Events published

None. The topic of the service is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and its catalogue events `LawsuitFiled`, `JudgmentRecorded` and `AuctionResult` belong to the stories that own the filing, the judgment and the auction result. This story publishes none of them: DP-09 is not in its pattern set, it writes no outbox row, and its two outputs are the local decision record of DP-03 and the case answer of 12.2.

#### 12.4 Events consumed

None. The re-run of AC2 and AC3 and the first pass of AC1 start inside `LitigationWorkflow` from the stage the parent `CaseWorkflow` forwards, and the step re-reads the checklist and the documents on the owner's operations; DP-09 is not in this story's pattern set, and the S4 IN row of Architecture v5 slide 19 lists only `NoticeDelivered` and `PartnerResultSubmitted` (GAP-2759; ASM-4590). `DocumentStored` of `rwb.document.events.v1` therefore has no subscription here, and a build that adds one fails the absence test.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-litigation` in namespace `rwb-recovery` | Input: the case, the route R4, the legal action and the rule package in force; signals: the case stage forwarded by the parent, the rule package in force and the approval answer |
| `checkPackDefects` | Activity, the one pack-defect check step of this story | `rwb-litigation` | The case and the legal action in; the rule ID with its package version, the checklist version, the missing items and the case move out, with the decision record written in one transaction |

The activity name is a target design choice of this story and is fixed by no source document; the trigger of the step is read as the case stage forwarded by the parent, because the legacy story says the step runs unattended while the FSD declares no background event (GAP-2759; ASM-4590).

#### 12.6 Schedules

None. The step runs from the case stage signal the parent forwards and owns no Temporal Schedule and no legacy Quartz job. The checklist refresh, the intake Schedule and the file jobs of the hub are rwb-document's; no Job of Architecture v5 slide 44 is owned, moved or registered here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Read by this story on the two operations; no column is written by the pack check |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated create and the answer it holds |

`hearing` is this service's and the sibling stories'; `document`, `document_checklist_item` and `case_document_check` are P5's; `recovery_case` is P3's; `rule_row` and `decision_log_entry` are P7's. None of them is read as a table here, no foreign key leaves the schema, and `legal_action.case_id` is an identifier and not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document checklist fake (API-P5-008) | The checklist of case `RC-2026-000705` at version `CHK-2026.11` with its required items and their present counts; a stage with no checklist rows; no answer beyond 2 s | AC1, AC2, X4, X5 |
| rwb-document document-page fake (API-P5-002) | The documents stored on case `RC-2026-000705`, paged; the missing item stored after retrieval; a page with no document of a required type | AC1, AC2, AC3 |
| rwb-case case fake and case-move answer | The case states `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `FILING_REJECTED`; the moves `PACK_DEFECT_HOLD` and `PACK_ASSEMBLY` accepted, and a move refused because the case is not in the state the rule expects | AC1, AC2, AC3 |
| rwb-decision rule-package fake | The LITIGATION package at its version in force with R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 | AC1, AC2, AC3 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-19 answer for case `RC-2026-000705`, with the pack facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The case-move answer and the element names the sources do not fix are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2758, GAP-2759; ASM-4589, ASM-4592).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The create and read of the legal action with its pack on `/api/recovery/litigation/v1`; the checklist and the case document page of rwb-document, and the rwb-case read and move answer; one hop, 2 s |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow and 1 activity | `LitigationWorkflow` and its one pack-defect check step on `rwb-litigation`; no Schedule |
| File | None | No file is read, built or delivered here; the documents themselves are the hub's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `pack`, Java package `th.co.scb.ace.workbench.recovery.litigation.pack`; front end `src/modules/recovery/litigation/PackDefects.tsx`, the fragment SCR-19 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the case answer commit together or not at all. DP-13 moves the base of the two operations and nothing else. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway. DP-09 is not in the pattern set, and 12.3 and 12.4 are None because of it.

**Dependencies the tables add and the plan does not hold.** The pattern table adds exactly the two H rows the plan already carries, so no H row is missing. The three consumed reads are class C in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2758 with ASM-4589.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` pack branch | Workflow | The stage of the journey that receives the case stage, runs the check and reports the outcome to the parent |
| `checkPackDefects` | Activity | The one step: read the legal action, read the checklist and the documents, evaluate the rule, write the record, answer the case move |
| `ChecklistClient` | Client | API-P5-008 of rwb-document, one hop, 2 s, breaker, and the empty-checklist answer treated as a state |
| `PackDocumentClient` | Client | API-P5-002 of rwb-document, paged, document type and reference only, no field value and no content |
| `PackDefectEvaluator` | Service | The evaluation of R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32 against the checklist version in force |
| `PackDefectDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, and refuses the step when the write fails (DP-03) |
| `PackDefectController` | Controller | The two operations, the capability area and right, the `Idempotency-Key` and the problem mapping |
| `PackDefectAnswer` | Signal reporter | Answers rwb-case with the case move, the rule and the missing item count; it reports, it never changes a case row |
| `PackDefects` | React component | Shows the checklist version and each item present or missing on SCR-19, read only, with the refusal states |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the checklist version, the missing items or the pack state: the first two are facts of the request and the answer, and the third is a route state of rwb-case; storing any of them would copy another service's facts into this schema (GAP-2758).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants.
- The checklist rows are reference data of rwb-document with a version and a valid-from date, read through API-P5-008 and cached for the call; no item, no required flag and no label is a constant of this build.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`.
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.

**Build steps**

1. The pack branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` as the stage child of `CaseWorkflow`, with the case stage as its trigger (AC1, AC2, AC3; GAP-2759).
2. `ChecklistClient` and `PackDocumentClient` against the two P5 fakes, with the 2 s budget, the breaker, the paging and the empty-checklist path (AC1, X4, X5).
3. `PackDefectEvaluator` over the LITIGATION package with the four rules and the no-fire path (AC1, AC2, AC3).
4. `PackDefectDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
5. `PackDefectAnswer` and the parent signal, with the two moves and the idempotent repeat (AC2, AC3, X8).
6. `PackDefectController` with the rights, the `Idempotency-Key` rule and the problem mapping (AC1, X2, X3).
7. `PackDefects` and the pack state of SCR-19 through the composite route fake, with MSG-S4-001 on each missing item (AC1).
8. The boundary test: no statement outside `rwb_litigation`, no `v_ace_*` read, no write to `rwb_document`, `rwb_case` or `rwb_decision` (X9, BR5).

**Feature flag.** `rwb.litigation.pack-defects-v1`, read as a flag of the platform library; off means the step holds the case stage, answers no move and writes no record, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic case in SIT, each of the four rules produces its record and its answer, a repeated stage signal writes once, a forced record failure changes nothing, no document, checklist or case row is written from this service, and SCR-19 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | A required item of the checklist version in force is not among the documents stored on the case, at the check and before a filing (VR-S4-005-1; X6) | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key. It names the expiry of the claim on the case, which the prescription rules of the sibling stories raise; no path of this story raises it (X7) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | A required field of a request is absent or invalid (X3, and the create of step 2) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right reads or creates the legal action (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the pack state changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-005 and of the FSD S4 A2.5 message list, copied unchanged; no message is reworded and no new message is added. `MSG-GEN-001` is displayed with the field it names, and `MSG-S4-001` with the item the checklist version requires. A downstream that does not answer (X4) and an action that is not found (X3) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show what it reads and answers, through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-19 Litigation workspace | Pack | The checklist version in force, each required item marked present or missing, and MSG-S4-001 on a missing item |
| SCR-19 Litigation workspace | Pack held | The case at `PACK_DEFECT_HOLD` with the missing items named, read from this service and from rwb-document |
| SCR-19 Litigation workspace | Instructed | The law firm instruction of the sibling stories next to the pack result, read only |
| SCR-19 Litigation workspace | Filed | The filing facts of the filing story and the outcome of the last check, read only |
| SCR-19 Litigation workspace | Hearing | The hearing dates of `hearing`, owned by the sibling stories |
| SCR-19 Litigation workspace | Judgment | The judgment facts of the sibling stories, read only |
| SCR-20 Enforcement workspace | Requested | The pack of an enforcement action and its missing items, read only |
| SCR-20 Enforcement workspace | Seized, Auctioned, Closed | The enforcement facts of the sibling stories, read only |
| SCR-19 Litigation workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-19 Litigation workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | No checklist | The case type has no checklist rows, and the pack shows that state with no count |

The route merges the answer of this service with rwb-document for the checklist and the documents and rwb-case for the case and its route state; the route path, the screen-model field list and the merge order belong to RWB-PLT-N001-CON and the edge stories, not here. The two state lists are the legacy state lists of RWB-E5-005 ("pack; instructed; filed; hearing; judgment" and "requested; seized; auctioned; closed") with the held, empty and failure states this story adds.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-005-01 | AC1 | End to end | Check the pack against the defect list |
| TC-E5-005-02 | AC2 | End to end | Rule R-LIT-18 |
| TC-E5-005-03 | AC3 | End to end | Rule R-LIT-32 |
| TC-E5-005-04 | AC4 | Component | Not recorded |
| TC-E5-005-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-005-06 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step maps to `End to end`, the not-recorded case to `Component`, the access case to `Component` and the forced failure of Principle 5 to `NFR`. The checklist fake, the document-page fake, the case fake, the rule-package fake and the decision-record stub of section 12.8 stand behind every case, and the fixture data — case `RC-2026-000705`, action `LA-2026-000705`, checklist version `CHK-2026.11` — is synthetic. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the checklist items, their required flag and order, the lists and the message texts are versioned rows and reference data; no item, state name, count or date appears in Java.
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry identifiers, type codes, counts, dates and a rule version only, and the test data is synthetic.
- The defect list stays with rwb-document: this service holds no checklist row, no document type row and no completeness flag (BR1; DP-01).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is answered with the rule and its version (BR3).
- ACE data only through the owner's contract: no component of this story reads a `v_ace_*` view or an ACE table, and the service holds no `v_ace_*` grant.
- No read of another service's tables and no cross-schema join: the checklist, the documents, the case and the rule rows are reached only through their owners' contracts.
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry of the step is the workflow's own and never a silent second post.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing, and the catalogue of the service is not widened (12.3, 12.4).
- The pack surface is read only; the verification, the rejection and the rework actions belong to the sibling stories.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested, which this story does on the checklist and the documents rwb-document owns (FSD S4 Requirements served; Business Requirements Program v4); the legacy story master carries no requirement ID and the plan's requirement row for this key is empty (GAP-2759; ASM-4591) | FEAT-LIT-05 | 08 Litigate and enforce | R-LIT-16, R-LIT-17, R-LIT-18, R-LIT-32 | TC-E5-005-01, TC-E5-005-02, TC-E5-005-03 |

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-005 | The four legacy criteria word for word, the four rules of the check, the two screens, the messages and the six test cases |
| RWB-S4-E5005-CON | H: the two operations, the pack and missing-item elements, the consumed rows and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| rwb-document (P5), API-P5-008 and API-P5-002 | C in fact and not in the metadata row: the checklist per case type and the stored documents, faked (GAP-2758) |
| rwb-case (P3) and its case read and move answer | The case of record, the route states `PACK_ASSEMBLY`, `PACK_DEFECT_HOLD` and `FILING_REJECTED`, answered and never written (GAP-2758) |
| rwb-decision (P7) | The LITIGATION package and its rule rows, governed there and named here |
| FEAT-LIT-05, FEAT-DCM-16, SCR-19, SCR-20 | The feature, the hub feature that holds the checklist, and the two screens of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-document and rwb-case, with the `-ITG` copies of the six cases |

### 19. Out of scope

- The published shape of the two operations, the pack and missing-item elements, the consumed rows, the error set and the fakes: RWB-S4-E5005-CON.
- The document checklist per case type, the stored documents, the retrieval request, the re-signed or re-created document and the CCMS exchange: rwb-document (P5), FEAT-DCM-16 and the hub stories. **The list is the hub's, and this story reads it and holds no copy** (GAP-2758; ASM-4588).
- The case of record, its route states, the parent `CaseWorkflow`, the case router and the case timers: rwb-case (P3).
- The assembly of the pack, the verification and the approval of the filing, the law firm instruction, the filing and the court receipt, the hearing calendar and the judgment: the sibling stories of this service.
- The authoring, testing and approval of the LITIGATION package and of the rule rows of R-LIT-16, R-LIT-17, R-LIT-18 and R-LIT-32: rwb-decision (P7), with the embedded runtime as a service-template capability.
- The rights, roles, scope and masking data themselves, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access and RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

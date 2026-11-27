# RWB-S4-E5018-APP Apply for the writ and seizure

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S4-E5018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S4-S |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S4-E5018-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E5-018 for rwb-litigation (S4). The writ and the seizure are held as a legal action of action type `ENFORCEMENT` opened on `/api/recovery/litigation/v1` (DP-13) and updated as the firm reports the filing and the court references; the legacy `DecisionLogWriter` write becomes the local decision record of RWB-PLT-E1027-CON written before the row moves (DP-03); the case route states `ENFORCEMENT_DECISION` and `WRIT_AND_SEIZURE`, the enforcement decision, the traced asset, the firm and the Legal Execution Department stay with rwb-case, rwb-decision, RWB-S4-E5017-APP and rwb-partner, are consumed and faked, and are recorded with the writ deadline and the missing writ value as gaps; SCR-19 and SCR-20 read through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S4-E5018-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **law firm user (PT-LAWFIRM)**, with the **enforcement owner (RW-ENFORCE)** acting on the same legal action, I want **the instruction to apply for the writ and the seizure recorded on a legal action of action type `ENFORCEMENT`, one decision record written with the rule version before the row moves, the writ deadline held as a durable timer, and the filing and the court references reported back and readable**, so that **an approved enforcement leaves the enforcement decision with the firm instructed and the writ trackable to execution instead of in a spreadsheet of the firm's own**.

This story owns the enforcement legal action of the writ and the seizure and the evaluation of R-LIT-54, and nothing else:

- the two legal-action operations the legacy story names, `POST /cases/{caseId}/legal-actions` (API-S4-002) and `GET /legal-actions/{legalActionId}` (API-S4-003), plus the update `PATCH /legal-actions/{legalActionId}` (API-S4-004) that the FSD flow needs and the TSD declares, on base `/api/recovery/litigation/v1` (DP-13; GAP-2825; ASM-4671);
- the `legal_action` row of schema `rwb_litigation` with its columns DF-LEG-001 to DF-LEG-014, the writ carried as `ENFORCEMENT` of `LOV-LEGAL-TYPE` (GAP-2821; ASM-4665);
- the evaluation of R-LIT-54 in state `ENFORCEMENT_DECISION` on the event `ENFORCE_APPROVED`, with the one decision record written before the row moves, with the rule ID and the version in force (DP-03);
- the durable timer of the writ deadline of R-LIT-54 on `LitigationWorkflow`, and the announce of the case move `WRIT_AND_SEIZURE` to rwb-case;
- the call that asks rwb-partner to instruct the panel firm for the writ and the seizure, the case read and the case move, and the rule package read; all three are consumed and faked.

It does not own the case, the enforcement decision, the traced asset, the firm or the seizure. `recovery_case` and the route states `ENFORCEMENT_DECISION` and `WRIT_AND_SEIZURE` are rwb-case's (P3), and the enforcement decision and its D7.5 authority are the case of record's with the delegation of authority held by rwb-decision (P7). The traced asset and the economic test that R-LIT-54 turns on are `RWB-S4-E5017-APP`'s and the rule package's (GAP-2824; ASM-4666, ASM-4672). The firm panel selection and the civil-case instruction are `RWB-S4-E5008-APP` and `RWB-S4-E5009-APP`'s. The seizure executed into the LED auction and the obstruction are R-LIT-63 and R-LIT-64, which are `RWB-S4-E5019-APP`'s. No component of this story writes a `recovery_case`, `decision_log_entry`, `rule_row` or `partner` row, and none reads a `v_ace_*` view.

### 2. Business rationale

Enforcement after judgment is the step the module names as the one with no owner today, and the programme asks for one owner from judgment to the end of enforcement (REQ-S4-007). The writ and the seizure are that owner's first act and the longest wait of the route: R-LIT-54 instructs the firm "to the writ deadline", the Legal Execution Department then executes, and the writ runs for years rather than days. The FSD keeps the objective to the legacy sentence — "instructs the writ and the seizure through the firm and tracks it to execution" (FSD S4 A2.18) — and the measure: a litigation turnaround of 6 days against the 21 days a filing takes today, read on the decision log and the Workbench records.

In the monolith one process held the legal action, the case row, the decision log entry and the rule row in one schema, so the legacy story could name `recovery_case`, `decision_log_entry` and `rule_row` in its Data table (legacy RWB-E5-018 Data and Endpoints blocks). In the target the same step is cut in five:

- **the legal action is this service's.** `legal_action` (DF-LEG-001 to DF-LEG-014) is S4's row and the writ is one action type of it, so the instruction, the filing, the court references and the status are written here and nowhere else (GAP-2821; ASM-4665);
- **the case route state is rwb-case's.** `ENFORCEMENT_DECISION` and `WRIT_AND_SEIZURE` are states of the 38-state LITIGATION machine that rwb-case holds; this service announces the move and accepts the answer, and writes no case row (GAP-2824; ASM-4666);
- **the decision is recorded first.** The record is written in this service's own transaction **before** the row changes, and a failed write changes nothing — this is legacy AC3 and the old `DecisionLogWriter` position of the module technical specification (DP-03);
- **the firm and its instruction are rwb-partner's.** The panel, its instruction and its result are S9's, reached in one hop on a published contract; the instruction this story asks for is the enforcement instruction, not the civil-case one of `RWB-S4-E5009-APP` (GAP-2819; ASM-4667);
- **the traced asset is not this service's.** R-LIT-54 turns on "an asset is traced and enforcement is economic", and both facts belong to the asset-trace story and to the rule package; `legal_action` carries no asset reference and none is added (GAP-2824; ASM-4672).

Two values have no home in any source read for this key. `LOV-LEGAL-TYPE` names `ENFORCEMENT` but no writ value, so the writ is carried as the enforcement type of the same list, and `legal_action` carries no writ, seizure or deadline column (GAP-2821; ASM-4665). The writ deadline of R-LIT-54 is given as a service level and no interval is written anywhere, so it is a versioned reference row held as a durable timer (GAP-2823; ASM-4669). Neither is invented here.

The story serves FEAT-LIT-18 and holds the legacy prerequisite FEAT-LIT-17 by reading the traced asset rather than re-implementing it. The three legacy criteria AC1, AC2 and AC3 belong to this story and are copied word for word in section 7. The legacy key carries no requirement id and the plan carries none for this slice, so the story traces to the requirement of the module that names the owner of enforcement (GAP-2820; ASM-4670).

### 3. Preconditions

- `RWB-S4-E5018-CON` is published: the three operations on `/api/recovery/litigation/v1`, the `LegalActionRequest`, `LegalAction` and `LegalActionUpdate` schemas with the enforcement element, the error envelope, the `Idempotency-Key` rule and the fakes. It is the first build dependency, so the story starts on Day 1.
- `legal_action` exists in schema `rwb_litigation` with the columns DF-LEG-001 to DF-LEG-014 of TSD S4 T3.1 and the standard columns of T3.0; this story adds no table, no column and no migration. A column for the traced asset, the writ or the seizure exists in no source and is not added (GAP-2821, GAP-2824; ASM-4665, ASM-4672).
- `RWB-PLT-E1027-CON` is live: the local decision-record library writes in the caller's transaction and a failed write stops the step with MSG-P7-003 (DP-03).
- The rwb-case case read and case-move answer are published and faked, carrying `ENFORCEMENT_DECISION`, `ENFORCE_APPROVED` and `WRIT_AND_SEIZURE`; no source names the operations, so they carry the placeholder `Not specified in the source documents (GAP-2819; ASM-4667)`.
- The rwb-partner instruction contract is published and faked: the instruction of the panel firm for the writ and the seizure, its pack and its service level. Its operation name is given by no source and carries the same placeholder (GAP-2819; ASM-4667).
- The rwb-decision underwriting rules of R-LIT-54 are in force at their version and are read through the rule package; this service evaluates them and declares none (GAP-2819; ASM-4668).
- The traced asset and the economic test of R-LIT-54 are read as inputs of the rule package and of `RWB-S4-E5017-APP`; no threshold and no asset field is defined in any source read here (GAP-2824; ASM-4672).
- `RWB-PLT-N001-CON` serves SCR-19 Litigation workspace and SCR-20 Enforcement workspace through the gateway-bff composite route, one hop, so both read surfaces exist from Day 1 (DP-19).
- `LOV-LEGAL-TYPE`, `LOV-LEGAL-STATUS` and `LOV-HEARING` of TSD S4 T3.2 are read as values in force with their version; DP-07 is not in this story's pattern set and the read carries no dependency row (GAP-2819; ASM-4667).
- The caller holds a Workbench role with the Litigation right of the operation it calls (TSD S4 T6.1). DP-08 is not in this story's pattern set: the right is declared per operation and the guard is a service-template capability.
- The service runs as its own login on schema `rwb_litigation` (DP-01, DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant.
- No approval is needed to build against a Draft baseline; both stories stay at status Draft until the verification loop collects the sign-offs (GAP-2822; ASM-4658).

### 4. Flow

1. The traced asset is recorded by `RWB-S4-E5017-APP` and rwb-case moves the case to `ENFORCEMENT_DECISION` under R-LIT-52 or R-LIT-53, owner enforcement owner, decision point D7.5.
2. The enforcement owner approves enforcement on SCR-20 Enforcement workspace through the composite route (DP-19); the case contract answers the fact `ENFORCE_APPROVED` to `LitigationWorkflow` on task queue `rwb-litigation`.
3. `WritActionValidator` checks the case reference, the caller's scope and the required elements of the instruction (case, amount, court where given); a failed check answers 422 or 404 and nothing is written.
4. `EnforcementRule` loads the LITIGATION package version in force and evaluates R-LIT-54: from `ENFORCEMENT_DECISION`, event `ENFORCE_APPROVED`, condition "an asset is traced and enforcement is economic", action "instruct the firm to apply for the writ and seizure", to `WRIT_AND_SEIZURE`, owner "Panel law firm", systems "Partner Portal, LED", service level "to the writ deadline". The condition is met by the inputs of the package and not by a value of this story (GAP-2824; ASM-4672).
5. If the rule does not fire, the answer is 409 and nothing is written: no row, no instruction and no move (exception X5).
6. `WritDecisionRecordWriter` writes one decision record through the local library **before** the row changes: case reference, legal action reference, rule ID `R-LIT-54` with the version in force, the inputs reference that carries the traced asset and the economic test, the outcome and the decision code read with its version. A failed write stops the step with MSG-P7-003 (legacy AC3).
7. `LegalActionWriter` writes, in one `rwb_litigation` transaction with the record, the `legal_action` row on `POST /cases/{caseId}/legal-actions` (API-S4-002): `case_id`, `action_type = ENFORCEMENT`, `court_name`, `claim_amount`, `law_firm_id`, `status` from `LOV-LEGAL-STATUS`, plus the idempotency key of the request.
8. `FirmInstructionClient` asks rwb-partner, one hop with a 2 s timeout and a breaker, to instruct the panel firm to apply for the writ and the seizure, carrying the legal action reference, the case reference and the rule ID with its version. The instruction, its pack and its service level are the partner service's (GAP-2819; ASM-4667).
9. `WritDeadlineTimer` starts the writ deadline of R-LIT-54 as one durable timer on `LitigationWorkflow`; its length is `Not specified in the source documents (GAP-2823; ASM-4669)`. `CaseMoveAnswer` announces `WRIT_AND_SEIZURE` with rule R-LIT-54 and its version; rwb-case writes the case and this service writes no case row (GAP-2824; ASM-4666).
10. The firm reports the filing through `PATCH /legal-actions/{legalActionId}` (API-S4-004) with `LegalActionUpdate`: `lawsuit_no`, `black_case_no`, `court_name`, `filed_date` and, where the court gives one, `red_case_no`; the row status moves to `FILED` in the same transaction, and the patch is idempotent on its `Idempotency-Key` (GAP-2825; ASM-4671).
11. The legal action is read on `GET /legal-actions/{legalActionId}` (API-S4-003) by SCR-19 and SCR-20 through the composite route: the action type, the status, the court references, the claim amount and the writ deadline of the timer, read only (DP-19).
12. The seizure executed into the LED auction and the obstruction are R-LIT-63 and R-LIT-64 and belong to `RWB-S4-E5019-APP`; this story only lets the case move and records nothing of them.
13. A repeated create with the same case, action type and amount, or with the same `Idempotency-Key`, writes nothing and sends no second instruction; the stored answer is returned and the repeat is counted.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The request carries no case, no amount or no action type, or a value of `action_type` outside `LOV-LEGAL-TYPE` | 422 and nothing is written; no rule is evaluated and no record is written | MSG-GEN-001 | AC1 |
| X2 | The case ID names no case in the caller's scope, or the legal action ID names no row | 404 and nothing is written; an out-of-scope case cannot be told from a missing one | None | AC1 |
| X3 | The legal action already exists for the case with the same action type and amount, or its status is `CLOSED` or `WITHDRAWN` | The stored answer is returned with 200, or 409; nothing changes | None | AC1 |
| X4 | The claim of the case expires inside the filing window | MSG-S4-002 is shown with the date and nothing is blocked; the prescription date is a fact of the case of record | MSG-S4-002 | AC1 |
| X5 | The route state is not `ENFORCEMENT_DECISION`, or no asset is traced, or R-LIT-54's economic test fails | R-LIT-54 does not fire; 409, nothing written and no instruction asked | None | AC2 |
| X6 | A role without the Litigation right records, reads or patches the writ | Refused before any read or write; nothing changes and no record is written | MSG-P4-002 | AC1 |
| X7 | The local decision-record write fails | The transaction writes nothing: no row, no status change, no instruction and no case move | MSG-P7-003 | AC3 |
| X8 | The firm declines the instruction, or the writ deadline passes with no filing | The instruction is recorded as not accepted and the case is told; re-selection of the firm stays with `RWB-S4-E5008-APP` under R-LIT-27 to R-LIT-29 | None | AC2 |
| X9 | The case, partner or rule-package contract does not answer inside 2 s, or its breaker is open | 503 with the platform error envelope; the step writes nothing and the caller repeats the same `Idempotency-Key` | None | AC1 |
| X10 | A component, a statement or a test reaches another `rwb_*` schema, a `v_ace_*` view or an ACE table | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17 |

X1 to X4 are the validation paths of VR-S4-018-1 and of the legacy message set; X5 is the no-fire path of R-LIT-54; X7 is legacy AC3; X8 to X10 are the paths the target call types add. The writ deadline, the economic test and the D7.5 authority are values in force, so none is a constant here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the contract, the decision-record library and the composite route; the case, partner and rule-package contracts are consumed and faked |
| Negotiable | The writ deadline, the economic test, the authority and the list values are versioned reference data; the story fixes behaviour and shapes, not values |
| Valuable | The writ is instructed, timed and trackable on one legal action with a decision record before it moves, which is the named owner REQ-S4-007 asks for |
| Estimable | Three operations, one validator, one rule evaluation, one library write, one repository write, two clients, one durable timer and one read-only screen fragment |
| Small | Fits two weeks with its tests as the primary slice of the legacy key |
| Testable | Each of the three criteria of section 7 is one end-to-end test with the cross-service answers stubbed; the contract half is proved by `RWB-S4-E5018-CON` |

### 7. Acceptance criteria

```gherkin
Feature: Apply for the writ and seizure, in rwb-litigation

  Background:
    Given the enforcement legal action "LA-2026-001018" exists on case "RC-2026-001018" with action type "ENFORCEMENT"
    Given the LITIGATION rule package is in force at its version and carries R-LIT-54
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Apply for the writ and seizure (legacy RWB-E5-018 AC1)
    Given the rwb-case contract mock returns the case state "ENFORCEMENT_DECISION" for case "RC-2026-001018"
    Given the rwb-partner contract mock returns the firm instruction "INSTRUCTED" for legal action "LA-2026-001018"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-54 at its version
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then instructs the writ and the seizure through the firm and tracks it to execution
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-LIT-54 (legacy RWB-E5-018 AC2)
    Given the rwb-case contract mock returns the case state "ENFORCEMENT_DECISION" for case "RC-2026-001018"
    Given the rwb-partner contract mock returns the firm instruction "INSTRUCTED" for legal action "LA-2026-001018"
    Given the rwb-decision contract mock returns the LITIGATION package with R-LIT-54 at its version
    Given a case in state ENFORCEMENT_DECISION
    When enforce approved
    Then instruct the firm to apply for the writ and seizure
    Then the case moves to WRIT_AND_SEIZURE

  Scenario: AC3 Not recorded (legacy RWB-E5-018 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E5-018 word for word, with the origin tag added and nothing else changed: the repeated `Then`, the lower-case opening of "instructs" and "tracks", and the legacy wording of "the user acts on the screen", "enforce approved" and "the action is taken" all stand. The cross-service parts are mocked, so AC1 and AC2 carry the `Given the <service> contract mock returns <x>` lines above, and those added `Given` lines are the only additions to the legacy text. What the legacy lines describe happens in three places in the target: rwb-case holds the case and its route state, rwb-partner holds the firm and the instruction, and this story writes the legal action, records the decision with the rule version and announces the move (GAP-2824; ASM-4666).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-LIT-54 | Litigation | D7 | ENFORCEMENT_DECISION | ENFORCE_APPROVED | an asset is traced and enforcement is economic | Instruct the firm to apply for the writ and seizure | WRIT_AND_SEIZURE | Panel law firm | Partner Portal, LED | To the writ deadline |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its owner column is a role of the business and not a service: "Panel law firm" is the firm that rwb-partner holds and instructs. Its systems column names the Partner Portal and the LED: the instruction goes to the firm through the partner portal and the Legal Execution Department enters the execution through the firm, so neither system is called by this service directly (GAP-2819; ASM-4667).

| ID | Rule | Source |
|---|---|---|
| BR1 | The writ and the seizure are one legal action of this service: the instruction, the filing, the court references and the status are columns of `legal_action` in `rwb_litigation` | FSD S4 A2.18; TSD S4 T3.1, T4; Ownership Map (legal_action and hearing owner S4) |
| BR2 | The decision is recorded before the row moves, with the rule ID and the version in force; a failed write changes nothing and the user sees MSG-P7-003 | DP-03; TSD S4 T2; legacy RWB-E5-018 AC1 and AC3 |
| BR3 | The case of record and its route state stay with rwb-case: this story announces `WRIT_AND_SEIZURE` and writes no `recovery_case` row and no route state | Ownership Map (recovery_case owner P3); TSD S4 T5.2; GAP-2824 |
| BR4 | The writ is carried as `ENFORCEMENT` of `LOV-LEGAL-TYPE`, because the list names no writ value, and no column is added for the writ, the seizure or the deadline | TSD S4 T3.1, T3.2; GAP-2821; ASM-4665 |
| BR5 | R-LIT-54 fires only from `ENFORCEMENT_DECISION` on `ENFORCE_APPROVED` and only on the condition of the rule; the traced asset and the economic test are inputs and are never derived here | Business Rules and Routing Logic v4 (R-LIT-54); FSD S4 A2.18.3.1; GAP-2824 |
| BR6 | The writ deadline is one durable timer of `LitigationWorkflow` armed from a versioned reference value; no `timer` row, no Temporal Schedule and no Quartz row is created | GAP-2823; ASM-4669; Template and Rules §R5.5 DP-10 held as a prohibition |
| BR7 | The firm and its instruction are rwb-partner's: this story asks for the instruction in one hop and stores no firm data of its own beyond the `law_firm_id` reference | Ownership Map (partner owner S9); TSD S4 T5.2; GAP-2819 |
| BR8 | The same create, the same instruction or the same patch twice writes once, sends one instruction and counts the repeat | TSD S4 T-A.2 (`Idempotency-Key`); legacy AC1 |
| BR9 | No value a business person may change is written in code; it is read from reference data with its version (BR-S4-018 of the module) | FSD S4 A2.18.3.1 (BR-S4-018); Template and Rules §R7.2 (s17) |
| BR10 | No person name, address, contact value or identity number enters `rwb_litigation`, the decision record, a log or a workflow input | Template and Rules §R7.2 (s17); TSD S4 T6.2 |

**Where the rule lives in the target.** R-LIT-54 is the instruction step: the case is at `ENFORCEMENT_DECISION` with an asset traced and the test of the rule met, the firm is instructed through rwb-partner, the action is written with `ENFORCEMENT` and `OPEN`, the record is written first, the writ deadline is armed and the case move `WRIT_AND_SEIZURE` is announced. The filing that follows is the `PATCH` of the same action, and the seizure itself is R-LIT-63 and R-LIT-64 of `RWB-S4-E5019-APP`.

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step announces the move and the parent `CaseWorkflow` applies it (BR3). What this story owns is the stage of `LitigationWorkflow` and the status of its own legal action.

| From (stage of `LitigationWorkflow`) | Event | Condition | To |
|---|---|---|---|
| `ENFORCEMENT_DECISION` | ENFORCE_APPROVED under R-LIT-54 | An asset is traced and enforcement is economic | `WRIT_AND_SEIZURE`, with the case-move answer of the same name |
| `ENFORCEMENT_DECISION` | ENFORCE_APPROVED under R-LIT-54 | The condition is not met | Unchanged, refused with 409 (X5) |
| `ASSET_TRACE` | ENFORCE_APPROVED | R-LIT-52 or R-LIT-53 has not moved the case to the decision | Unchanged, refused with 409 (X5) |
| Any other stage | ENFORCE_APPROVED | The stage is not the one the rule expects | Unchanged, refused with 409 (X5) |

| Legal action status (`LOV-LEGAL-STATUS`) | Event | Condition | To |
|---|---|---|---|
| None | `POST /cases/{caseId}/legal-actions` under R-LIT-54 | The record is written and the firm is instructed | `OPEN` |
| `OPEN` | The firm reports the filing on `PATCH` | The court reference and the filed date are present | `FILED` |
| `FILED` | The firm reports the execution | The seizure steps of R-LIT-63 and R-LIT-64, which are `RWB-S4-E5019-APP`'s | `ENFORCING` |
| `OPEN` or `FILED` | The writ is withdrawn | A step of the sibling stories | `WITHDRAWN` |

`CLOSED` belongs to R-LIT-51 and R-LIT-70, which are rwb-payment and rwb-writeoff's, and no status change to `CLOSED` is written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in the TSD S4 T6.1 matrix: creates, reads and patches the action and works SCR-19 |
| RW-ENFORCE, enforcement owner | Litigation CRU: the "also uses" role of the FSD A2.18.3.3 and the owner of the enforcement decision; approves on SCR-20 |
| PT-LAWFIRM, law firm user | Litigation RU: the primary actor of the FSD; reports the filing and the court references on the partner portal through the `PATCH` operation, scoped to its own cases |
| RW-LEGAL, RW-HEADLIT, RW-PRODHEAD | Litigation RA or R as the T6.1 matrix gives it: read and approve; no writ is instructed on their right |
| RW-CASEOWN, RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-WRITEOFF, RW-CREDITAD, RW-GUARANT, RW-AGENCYMG, RW-CONDUCT, RW-HEADNPA, RW-HEADASL, RW-RISK, RW-COE, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE | Litigation R: read only |
| SY-DATALOAD, SY-CASEWF, SY-RULES, SY-AGENT | Litigation U or R as the T6.1 matrix gives it: the service identities run the step under the same checks |
| rwb-litigation service identity | Runs the step, evaluates R-LIT-54, writes the record and the action, holds the timer and announces the move; it holds no grant on another schema |

The rights are the rows of TSD S4 T6.1 and the legacy permission table of this key: Litigation `C` for RW-LITOFF and RW-ENFORCE, `R` for the read row of 22 roles and more. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard is a service-template capability.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-001 | legal_action (S4, `rwb_litigation`) | id | Write on create, read on the read path |
| DF-LEG-002 | legal_action (S4, `rwb_litigation`) | case_id | Write on create, and sent on the case-move answer |
| DF-LEG-003 | legal_action (S4, `rwb_litigation`) | law_firm_id | Write from the instruction answer of rwb-partner; a reference, not firm data |
| DF-LEG-004 | legal_action (S4, `rwb_litigation`) | action_type | Write `ENFORCEMENT` of `LOV-LEGAL-TYPE` (BR4) |
| DF-LEG-005, DF-LEG-006 | legal_action (S4, `rwb_litigation`) | lawsuit_no, black_case_no | Write when the firm reports them on `PATCH` |
| DF-LEG-007 | legal_action (S4, `rwb_litigation`) | red_case_no | Write where the court gives one after judgment |
| DF-LEG-008 | legal_action (S4, `rwb_litigation`) | court_name | Write on create and on `PATCH` |
| DF-LEG-009 | legal_action (S4, `rwb_litigation`) | claim_amount | Write on create, as the amount the writ is applied for |
| DF-LEG-010 | legal_action (S4, `rwb_litigation`) | filed_date | Write when the firm reports the filing |
| DF-LEG-011, DF-LEG-012 | legal_action (S4, `rwb_litigation`) | judgment_date, judgment_amount | Read, as the judgment the enforcement follows; not changed here |
| DF-LEG-013 | legal_action (S4, `rwb_litigation`) | lit_status | Read only: the court status arrives on the LIT interface |
| DF-LEG-014 | legal_action (S4, `rwb_litigation`) | status | Write `OPEN` on create and `FILED` on the filing (`LOV-LEGAL-STATUS`) |
| Standard columns | legal_action (S4, `rwb_litigation`) | `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write through the repository; `version` is the optimistic lock |
| DF-LEG-024 to DF-LEG-029 | hearing (S4, `rwb_litigation`) | hearing_date, hearing_type, outcome, next_date | Read, as the hearings the judgment closed before enforcement |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the route state comes back on the case-move answer (BR3) |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_litigation`) | decision code, rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the action changes (DP-03) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read through the rule package in force and never as a table |

Field IDs are those of TSD S4 T3.1, the legacy story Data table and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `legal_action` and `hearing` arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in `rwb_litigation` by the library's own migration (DP-03). The writ, the seizure and its deadline have no column and are not given one (BR4; GAP-2821). The fixtures are synthetic: case `RC-2026-001018`, action `LA-2026-001018`, one traced asset fact and one enforcement that is economic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1` (DP-13). The shapes are declared by RWB-S4-E5018-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | LegalActionRequest in with the enforcement element, LegalAction of status 201 out (API-S4-002) | Litigation, right C, scope applied | `Idempotency-Key` |
| GET | `/legal-actions/{legalActionId}` | LegalAction of status 200 out with its court facts, its hearings and its status (API-S4-003) | Litigation, right R, scope applied | Not applicable |
| PATCH | `/legal-actions/{legalActionId}` | LegalActionUpdate in with the filing element, LegalAction of status 200 out (API-S4-004) | Litigation, right U, scope applied | Not applicable |

Errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case or action, 409 for a wrong route state, a duplicate or a closed action, 422 with MSG-GEN-001 for a missing or invalid element, and 503 when the decision library, a consumed contract or the rule package does not answer. `POST /legal-actions/{legalActionId}/hearings` (API-S4-005) and `POST /notices/{noticeId}/approve` (API-S4-001) belong to the sibling stories and are not declared here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-2819; ASM-4667)) | `/api/recovery/case/v1` | P3 rwb-case | The route state `ENFORCEMENT_DECISION` and the enforcement decision; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2819; ASM-4667)) | `/api/recovery/case/v1` | P3 rwb-case | The move `WRIT_AND_SEIZURE` with rule R-LIT-54 and its version; faked |
| The firm instruction (operation name Not specified in the source documents (GAP-2819; ASM-4667)) | `/api/recovery/partner/v1` | S9 rwb-partner | The instruction of the panel firm for the writ and the seizure, its pack and its result; faked |
| The rule package in force (operation name Not specified in the source documents (GAP-2819; ASM-4667)) | `/api/recovery/decision/v1` | P7 rwb-decision | The LITIGATION package at its version with R-LIT-54; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). All four are contract dependencies of class C in fact and the metadata row carries None, because the plan carries none for this slice; the absence is recorded as GAP-2819 with ASM-4667.

#### 12.3 Events published

None. The service topic is `rwb.litigation.events.v1` with event names `rwb.litigation.<Event>.v1` (DP-14), and the ownership rows of S4 list zero events. DP-09 is not in this story's pattern set: the step writes no outbox row, and its outputs are the local decision record of DP-03, the instruction, the case-move answer and the timer.

#### 12.4 Events consumed

None. The ownership rows list no consumed event either, so the approval arrives as a signal of `LitigationWorkflow` and the case, the firm and the package arrive on the contracts of 12.2 (GAP-2819; ASM-4668). This story holds no consumer group and no inbox, and a build that adds a subscription fails the absence test of the CON.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `LitigationWorkflow` | Workflow, one execution per case per stage, child of `CaseWorkflow`, continues-as-new across years | `rwb-litigation` in namespace `rwb-recovery` | Input: case, route R4, legal action and package in force; signals: the enforcement approval and the package in force; outcome: the stage move for the parent |
| `openWritAction` | Activity, the create and instruction step | `rwb-litigation` | The enforcement element in; the record, the `legal_action` row, the instruction, the case move and the timer out, in one transaction |
| `recordWritFiling` | Activity, the filing reported by the firm | `rwb-litigation` | The filing element in; the court references, `filed_date` and `FILED` out, with the record |
| `armWritDeadline` | Activity, the timer of R-LIT-54 | `rwb-litigation` | The rule and the version in; one durable timer to the writ deadline out |

The activity names are target design choices and are fixed by no source; the trigger is read as a signal, because the ownership rows declare no event and the FSD declares no background event (GAP-2819; ASM-4668, ASM-4671). No cross-service call is made inside a workflow: each is an activity of the queue above.

#### 12.6 Schedules

None. The step runs from the approval signal, and the writ deadline of R-LIT-54 is a durable timer of the workflow, not a Schedule and not a `timer` row; this story registers no Temporal Schedule, no Quartz row and no shared job table, and no Job of the batch catalogue is owned or moved here (GAP-2823; ASM-4669).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| legal_action | S4 (`rwb_litigation`) | Written on create and on the filing; read on the read path (BR1) |
| hearing | S4 (`rwb_litigation`) | Read only, as the hearings before enforcement; no hearing row is written here |
| decision_record | PLT library, created in `rwb_litigation` | The local hash-linked record of the instruction and of the filing (DP-03) |
| idempotency_key | PLT library, created in `rwb_litigation` | The key of the repeated create and patch, and the answer it holds |

Not owned and never read as a table: `recovery_case` and `task` (P3), `partner` and its instruction (S9), `rule_row` and `decision_log_entry` (P7), `document` (P5) and the payment rows (P8). No foreign key leaves the schema and `legal_action.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case read fake | The route state `ENFORCEMENT_DECISION`, another state, and no answer beyond 2 s | AC1, AC2, X5 |
| rwb-case case-move fake | The move `WRIT_AND_SEIZURE` accepted with rule R-LIT-54 and its version, and a move refused because the case is not in the state the rule expects | AC2, X5 |
| rwb-partner instruction fake | The instruction `INSTRUCTED` with the firm reference, a decline, and a timeout beyond 2 s | AC1, AC2, X8, X9 |
| rwb-decision rule-package fake | The LITIGATION package with R-LIT-54 at its version, a second version, and a package without the rule | AC1, AC2, X5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain that answers MSG-P7-003 | AC3, X7 |
| gateway-bff composite route fake | The merged SCR-19 model in the writ state and the SCR-20 model in the requested state for case `RC-2026-001018` | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners publish them (GAP-2819; ASM-4667).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | The create, the read and the patch on `/api/recovery/litigation/v1`; the case read, the case-move answer, the firm instruction and the rule package; one hop, 2 s each |
| Kafka | None | No event published and none consumed by this story (12.3, 12.4) |
| Temporal | 1 workflow, 3 activities, 1 durable timer | `LitigationWorkflow` with `openWritAction`, `recordWritFiling` and `armWritDeadline` on `rwb-litigation`, and the writ deadline; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.litigation`, module `enforcement`, Java package `th.co.scb.ace.workbench.recovery.litigation.enforcement`; front end `src/modules/recovery/litigation/ApplyWrit.tsx`, the fragment SCR-20 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the action row and the stage move commit together or not at all, and the record is written before the instruction leaves the service. DP-13 re-bases the three operations and nothing else. DP-19 is how SCR-19 and SCR-20 reach this service, one hop through the gateway. DP-05 is held as a prohibition because the service holds no `v_ace_*` grant, DP-09 and DP-10 because no event and no Schedule is declared, and DP-04 because R-LIT-54 is read from the package of P7 and evaluated by the embedded runtime of the service template (GAP-2819; ASM-4668).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationWorkflow` enforcement branch | Workflow | Waits for the approval, loads the package in force, arms the writ deadline and reports the stage move to the parent |
| `WritActionValidator` | Service | Checks the case reference, the scope, the action type against `LOV-LEGAL-TYPE` and the required elements |
| `EnforcementRule` | Service | The evaluation of R-LIT-54 against the package version in force, with the state and event names of the LITIGATION machine |
| `WritDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `LegalActionWriter` and `LegalActionRepository` | Repository | Write the row and the filing columns with the optimistic lock, on `rwb_litigation` only |
| `FirmInstructionClient` | Client | Asks rwb-partner for the enforcement instruction, one hop, 2 s, breaker |
| `WritDeadlineTimer` and `CaseMoveAnswer` | Workflow adapter | Arm the durable timer and announce `WRIT_AND_SEIZURE` with the rule and its version |
| `LegalActionController` | Controller | The three operations, the capability area and right, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `ApplyWrit` | React component | Shows the action, its type, its status, its court references and the writ deadline, read only |

**Database and migrations.** No Flyway file. `legal_action` and `hearing` arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in `rwb_litigation` by the library's migration (DP-03). No column is added for the writ, the seizure or the deadline (BR4; GAP-2821).

**Configuration and reference data.**

- `LOV-LEGAL-TYPE` and `LOV-LEGAL-STATUS` at their version in force (TSD S4 T3.2), read as reference data and never as constants; no writ value is added to the type list.
- The LITIGATION package and its version, authored, tested and approved in rwb-decision (P7) and loaded on the package in force; the writ deadline of R-LIT-54 and the economic test are values of the package and of reference data (GAP-2819, GAP-2823; ASM-4669).
- The capability area "Litigation" and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the step itself; the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The enforcement branch of `LitigationWorkflow` and its input record, registered on `rwb-litigation` with the approval signal as its trigger (AC1, AC2).
2. `LegalActionRepository` over `legal_action` and `hearing`, with the create and filing columns and the optimistic lock (AC1, AC2).
3. `EnforcementRule` over the package in force, with R-LIT-54, the state and event names and the no-fire path (AC2, X5).
4. `WritDecisionRecordWriter` against the library stub, with the failed-write path (AC3, X7).
5. `FirmInstructionClient` against the partner fake, with the decline and the timeout (AC1, X8, X9).
6. `armWritDeadline` and `CaseMoveAnswer` with the timer and the move (AC2).
7. `LegalActionController` with the rights and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (AC1, X1, X2, X3, X6).
8. `ApplyWrit` and the two workspaces through the composite route fake (AC1, AC2).
9. The boundary test: no statement outside `rwb_litigation`, no write to `rwb_case`, `rwb_partner` or `rwb_decision` (X10, BR3, BR7).

**Feature flag.** `rwb.litigation.apply-writ-v1`, read as a flag of the platform library; off means the step holds the approval, writes no row and asks no instruction, and the sibling stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic approval in SIT, R-LIT-54 writes the action, records the decision, instructs the firm, arms the deadline and moves the case, the filing moves the status to `FILED`, a repeated create writes once, a forced record failure changes nothing, no `recovery_case` row is written from this service, and SCR-19 and SCR-20 answer through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S4-001 | Carried from the legacy message set. It names a missing item of the litigation pack, which is the pack story of this service, so no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | The claim of the case expires inside the filing window (X4) | The claim on this case expires on {date}. File before then. |
| MSG-GEN-001 | VR-S4-018-1: a required element of the instruction or of the filing is absent or invalid (X1) | Enter {field}. |
| MSG-P4-002 | A role without the Litigation right creates, reads or patches the writ (X6) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the action changes (X7) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five texts are the legacy wording of RWB-E5-018, of the FSD S4 A2.18 message list and of the legacy message table, copied unchanged; no message is reworded and no new one is added. `MSG-GEN-001` is displayed with the field it names. A downstream that does not answer (X9) and an action that is not found (X2) carry no message of this set, and the platform error envelope is displayed as it is.

### 15. Screens and states

No new screen is built. Two existing surfaces show what this story writes, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees |
|---|---|---|
| SCR-20 Enforcement workspace | Requested | The enforcement decision, the traced asset of `RWB-S4-E5017-APP` and the writ instruction as requested, under RW-ENFORCE |
| SCR-20 Enforcement workspace | Seized; auctioned; closed | The later enforcement states of `RWB-S4-E5019-APP` and of rwb-payment, read only; this story writes none of them |
| SCR-19 Litigation workspace | Pack; instructed; filed | The instruction of the sibling stories, and the writ action with its court references and `FILED` |
| SCR-19 Litigation workspace | Hearing; judgment | The hearings and the judgment the enforcement follows, read only |
| SCR-20 Enforcement workspace | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-20 Enforcement workspace | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |

The route merges this service's answer with rwb-case for the case and its route state; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON` and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-018-01 | AC1 | End to end | Apply for the writ and seizure |
| TC-E5-018-02 | AC2 | End to end | Rule R-LIT-54 |
| TC-E5-018-03 | AC3 | Component | Not recorded |
| TC-E5-018-04 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E5-018-05 | Principle 5 | NFR | A forced decision log write failure stops the action with MSG-P7-003 |

The five legacy test case IDs, their Covers and their Data are kept in order and character for character. The legacy table carries no level column, so a case that exercises the whole step maps to `End to end`, the access and the not-recorded cases to `Component`, and the forced failure of Principle 5 to `NFR`. The fixtures of section 12.8 stand behind every case, and the data is synthetic: case `RC-2026-001018`, action `LA-2026-001018`, one traced asset and one enforcement that is economic. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies belong to the wave 3 harness and are not listed here.

### 17. Guardrails

- No business value in code: the writ deadline, the economic test, the list values and the message texts are values and reference rows with a version; no list value, state name, day count or date appears in Java (BR9).
- No personal data in logs, workflow inputs, prompts or the fixture: the rows carry case references, action references, codes, dates and amounts only, and the test data is synthetic (BR10).
- The case stays with rwb-case: no `recovery_case` row and no route state is written here, and the move is announced with the rule and its version (BR3).
- The firm stays with rwb-partner: `law_firm_id` is a reference and no firm, panel or instruction data is copied into `rwb_litigation` (BR7).
- Only the columns of section 11 are written, and no writ, seizure or deadline column is added (BR4; GAP-2821).
- ACE data only through its owner: no component of this story reads a `v_ace_*` view or an ACE table.
- No read of another service's tables and no cross-schema join: `recovery_case`, `partner`, `rule_row` and `decision_log_entry` are reached only through their owners' contracts (DP-01).
- One hop and a 2 s budget on each consumed call, with a breaker per downstream and no call chain; the retry is the workflow's own and never a silent second instruction.
- The decision is never recorded after the effect: the record is written first through the library, and a failed write stops the step (DP-03, MSG-P7-003).
- No event, no topic, no outbox row and no Schedule: this story publishes nothing and consumes nothing (12.3, 12.4).
- SCR-19 and SCR-20 are read only; the filing is posted through the service, and the firm's entry on the partner portal uses the same operation under `PT-LAWFIRM`.

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement, which this story does by opening and tracking the writ action under RW-ENFORCE (FSD S4 Requirements served) | FEAT-LIT-18 | 08 Litigate and enforce | R-LIT-54 | TC-E5-018-01, TC-E5-018-02, TC-E5-018-03 |

The legacy story master of RWB-E5-018 carries no requirement ID and the plan's requirement list for this slice is empty; the trace is the requirement of the module that names the owner of enforcement, which is the outcome of the writ step (GAP-2820; ASM-4670).

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E5-018 | The three legacy criteria word for word, R-LIT-54, the two screens, the messages and the five test cases; the `recovery_case`, `decision_log_entry` and `rule_row` rows of the legacy data table are other owners' |
| RWB-S4-E5018-CON | H: the three operations, the enforcement and filing elements, the error set and the fakes |
| RWB-PLT-E1027-CON | H: the local decision-record library written in the caller's transaction before the change |
| RWB-PLT-N001-CON | H: the gateway-bff composite route behind SCR-19 and SCR-20 |
| rwb-case (P3), rwb-partner (S9), rwb-decision (P7) contracts | C in fact and not in the metadata row: the case read, the case move, the firm instruction and the rule package, faked (GAP-2819) |
| FEAT-LIT-18, FEAT-LIT-17, SCR-19, SCR-20 | The feature, its traced-asset prerequisite and the two screens of the legacy story |
| DP-03, DP-13, DP-19 | The decision record, the service base and the composite route |
| DP-01, DP-14 | The owner's schema and the naming of the topic and the queue, which this story declares and does not use |
| ADR-013, ADR-014, ADR-016, ADR-020, ADR-022 | 19 services inside ACE, schema and login per service, the Temporal layer with durable timers, contract-first REST with one hop, and the local decision record with the central ledger |
| Wave 3 harness | The end-to-end proof of the same legacy key across rwb-litigation, rwb-case and rwb-partner, with the `-ITG` copies of the five cases |

### 19. Out of scope

- The published shapes of the three operations, the enforcement and filing elements, the error set and the fakes: `RWB-S4-E5018-CON`.
- The case of record, its route state, the parent `CaseWorkflow` and the enforcement decision: rwb-case (P3) (GAP-2824; ASM-4666).
- The traced asset and the economic test of R-LIT-54: `RWB-S4-E5017-APP`, the rule package and the reference-data owner (GAP-2824; ASM-4672).
- The firm, the panel, its selection and the instruction mechanics: `RWB-S4-E5008-APP`, `RWB-S4-E5009-APP` and rwb-partner (S9) (GAP-2819; ASM-4667).
- The authoring, testing, approval and versioning of the LITIGATION package and of R-LIT-54: rwb-decision (P7).
- The seizure, the obstruction and the LED auction ladder (R-LIT-63 to R-LIT-67): `RWB-S4-E5019-APP`.
- The enforcement deferral and the bankruptcy petition (R-LIT-55 to R-LIT-62): `RWB-S4-E5020-APP` and `RWB-S4-E5021-APP`.
- The matching and posting of the enforcement proceeds (R-LIT-65, R-LIT-70): rwb-payment (P8) and `RWB-S4-E5022-APP`.
- The rights, roles, scope and masking data, and the screen field list and merge order of SCR-19 and SCR-20: rwb-access (P4) and `RWB-PLT-N001-CON`.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

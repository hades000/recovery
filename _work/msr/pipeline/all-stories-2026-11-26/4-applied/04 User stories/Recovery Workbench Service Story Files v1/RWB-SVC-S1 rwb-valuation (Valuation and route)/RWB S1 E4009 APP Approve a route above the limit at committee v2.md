# RWB-S1-E4009-APP Approve a route above the limit at committee

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4009-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S1-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4009-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-009 split out for rwb-valuation. Both legacy criteria of the key, AC1 and AC2, are copied word for word with their origin tags, and the cross-service parts of AC1 are mocked as added `Given` lines. The committee approval becomes the `escalateToCommittee` branch of `RouteDecisionWorkflow` on task queue `rwb-valuation`: it takes the recommendation of FEAT-VAL-07 as it stands, reads the case state on rwb-case, the delegation-of-authority limit, the level and the rule version in force on rwb-decision and the caller's right on rwb-access, escalates the item above the limit under R-UNI-15, records the committee's final call through the local decision-record library before anything is answered (DP-03), answers the case moves `ESCALATED` and `ROUTE_D6_REOPEN` to rwb-case and returns `Approval` on `POST /cases/{caseId}/route` at base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19), and publishes no event, because the ownership rows give S1 none. The element sets of `RouteRequest` and `Approval` and the committee elements are not published (GAP-2633; ASM-4337); the delegation limit, its boundaries and the row that answers them are not published and their owner is read two ways in this run (GAP-2634; ASM-4338); no D6 route-decision rule row is in force and no S1 rule package is published (GAP-2635; ASM-4339); the store of the committee resolution is not named by any source (GAP-2636; ASM-4340); the legacy permission table gives right U to four officer roles and names no right for the committee that answers (GAP-2637; ASM-4341). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S1-E4009-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As the **Credit approval committee member**, I want **to take the route to the credit committee when it is beyond the case owner's limit**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-009. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the rules, messages and screen they name;
- the above-limit branch of `RouteDecisionWorkflow`, the one workflow the ownership rows give S1, on task queue `rwb-valuation` in namespace `rwb-recovery`, with its activities `checkDelegation`, `escalateToCommittee` and `recordCommitteeAnswer`;
- the comparison of the route amount with the case owner's limit in force, read as data with its version and never written in code;
- the escalation of the item to the credit committee (R-UNI-15), carrying the recommended route, the amount, the expected return by route with its model version, the gap to the limit, the level and the delegation version;
- the committee's final call, its coded reason and its level, reported to the parent `CaseWorkflow` as the `ESCALATED` and `ROUTE_D6_REOPEN` moves of the case of record (R-UNI-15, R-UNI-41);
- the read of the case state and the answer of the case move on rwb-case, of the rule, the limit and the limit version on rwb-decision, and of the right on rwb-access, one hop and 2 s each;
- the decision record of the answer, written through RWB-PLT-E1027-CON in the caller's transaction before the answer, under decision code D6 with the rule or limit version applied (DP-03);
- the committee elements of the route command and answer on `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, with its right and its `Idempotency-Key` (API-S1-001; DP-13);
- the states of SCR-13 Route decision that this branch produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the consumed rows, the committee element set, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4009-CON; the inside-limit approval and its override reason, which are RWB-S1-E4008-APP; the appraisal, its age and its order, which are RWB-S1-E4001-APP; the route scoring, the expected return and the reasons of FEAT-VAL-05 to FEAT-VAL-07, and the reconsideration of FEAT-VAL-11, which are sibling stories; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows, the authority matrix, the limit versions, the approval record and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The route decision chooses between seven routes that cost the bank different money and take different time, and FEAT-VAL-08 lets the case owner sign the recommendation inside their delegated limit. FEAT-VAL-09 is the point where that authority runs out: the route is beyond the limit, the case owner may not sign it, and it goes to the credit committee. Architecture v5 slide 3 states the target in one line: "valuation and rules propose a route; an approver within their delegated authority (DoA Matrix v2) signs it off; the decision is logged (P7)". REQ-S1-006 carries the same requirement: the route decision is approved inside the delegation of authority, and above the limit it reaches the committee.

The monolith did this inside one S1 process: it read the DoA table on its own connection, compared the amount, wrote `decision_log_entry` in the same transaction and moved the case in the same schema. In the 19-service target the facts around that act belong to different owners, and this story is what keeps them apart while the rule stays the same.

- **above the limit means not the owner's call.** R-UNI-15 refuses a change outside the user's limit and raises the request to the approver named in the matrix, with a one-working-day clock; that raise is this story, and the inside-the-limit path is RWB-S1-E4008-APP under R-UNI-14 (GAP-2637).
- **the limit is policy data.** BR-S1-009 forbids writing a value a business person may change in code, and the delegation of authority is a governed matrix administered by rwb-access and versioned with its limit rows by rwb-decision, as the sibling inside-limit story of this service records; the row itself and its boundaries are not in the read sources and its owner is read two ways in this run (GAP-2634; ASM-4338).
- **the case stays with rwb-case.** `ESCALATED` and `ROUTE_D6_REOPEN` are case states of the D6 route set; this story answers the moves and writes no case row.
- **the decision is recorded first, and locally.** AC2 is the rule that makes the branch trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the committee's answer, with R-UNI-38 fixing which version was in force and R-UNI-39 forbidding an action that is not logged (GAP-2635; ASM-4339).
- **the resolution is a record, not a new table.** No source names where the committee's resolution and its reference are stored, and the ownership rows give S1 no table, so the resolution lives in the decision record and the schema stays as the DB story creates it (GAP-2636; ASM-4340).
- **nothing is published.** The ownership rows give S1 no event, so the branch adds no name to `rwb.valuation.events.v1`; its outward facts are the route answer, the case move and the decision record, which the library sends to `rwb.decision-record.v1` (ASM-4342).

The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records. The limit, the level, the clock and the coded reasons stay data of their owners and are read with their version, never asserted as constants.

### 3. Preconditions

- RWB-S1-E4009-CON is published: the committee element set of the route answer, the escalation and final-call elements, the four consumed rows, the rights, the error envelope and the fakes are baselined and handed to this story (H).
- RWB-PLT-E1027-CON is published (DP-03): the local decision-record writer joins the caller's transaction, and a failed write stops the branch with MSG-P7-003 (H).
- RWB-PLT-N001-CON is published (DP-19): SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (H).
- RWB-S1-E4008-APP is the inside-limit path of the same operation: the two stories split on the limit and share the workflow, the element set and the screen, and neither is a build dependency of the other because each builds against its own contract.
- The rwb-decision row that carries the rule in force, the delegation limit and its version is available for its fake; its operation name is Not specified in the source documents (GAP-2634; ASM-4338).
- The rwb-case case-state read is `GET /cases/{caseId}` on `/api/recovery/case/v1`, and the rwb-access `POST /authorise` answers the right; both are available for their fakes.
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `rule_row`, `approval` or a view is refused by the database and fails the boundary test.
- The route amount, the recommended route and the expected return by route arrive as elements of the request this branch answers, produced by the recommendation step of the sibling stories; this story reads them and recomputes nothing.
- The capability area is Treatment and offer: right U for the officer roles of the legacy permission table and right RA for the committee member and the product head of TSD S1 T6.1 (GAP-2637; ASM-4341).
- No D6 route-decision rule row is in force and no S1 rule package is published, so the record carries the decision code D6, the delegation version and the rule id where the decision owner provides one (GAP-2635; ASM-4339).
- Where the committee's resolution and its reference are stored is not fixed by any source, so the record holds them and no table is added (GAP-2636; ASM-4340).
- No approval is needed to build against a Draft contract baseline; RWB-S1-E4009-CON tags the version when its tests pass.

### 4. Flow

1. A case sits at `ROUTE_D6` with a recommendation: the expected return by route with its model version, the recommended route, the amount and the confidence. The case owner submits the decision, or the committee member opens the item, on SCR-13 through the gateway-bff composite route (DP-19).
2. The submission arrives on `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1` and continues `RouteDecisionWorkflow` on `rwb-valuation`; the above-limit branch starts where the recommendation is complete (API-S1-001; DP-13).
3. `checkDelegation` reads the delegation limit, the level and the version in force for the product, the decision code D6 and the amount, one hop with a 2 s budget and a breaker, and compares the amount with the limit (GAP-2634; ASM-4338).
4. At or below the limit the branch ends without an escalation and reports the inside-limit outcome, which RWB-S1-E4008-APP owns; no committee item is raised and nothing is escalated (X6).
5. Above the limit, `escalateToCommittee` raises the item with the case, the recommended route, the amount, the expected return by route with its model version, the gap to the limit, the level and the delegation version; R-UNI-15 answers the move `ESCALATED` with its one-working-day clock, and the stage reports that move to the parent `CaseWorkflow`, which moves the case of record (BR2, BR3).
6. The committee member — right RA of Treatment and offer — approves or refuses on SCR-13, with a coded reason where the answer departs from the recommendation; a role without RA is refused before the item is read (BR4, X2).
7. `recordCommitteeAnswer`, one transaction: the decision record is written with the decision code D6, the rule id and version where the decision owner provides one, the delegation version, the route, the amount, the level, the elapsed clock, the final call, the coded reason and the role of the decider — and the idempotency row with it. A failed write leaves the case where it is and shows MSG-P7-003 (AC2).
8. On a grant the branch reports the approved route, which the workflow answers to the screen and hands to the route-flow step of the sibling story; on a refusal it reports `ROUTE_D6_REOPEN` with the coded reason and the case returns to the route decision for a fresh recommendation (R-UNI-41).
9. The route operation answers `Approval` with the committee elements of the baseline. A repeat of the same `Idempotency-Key` returns the stored answer and raises no second item and no second record (R-UNI-40).
10. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own (ASM-4342).
11. SCR-13 shows the escalated item, its clock, the limit and the level, the committee's answer and its reason, read through the gateway-bff composite route, read only (DP-19).
12. Where the recommendation changes while the item is open — a new value, a payment or a deviation — the stage withdraws the open item with its reason, records the withdrawal and reports `ROUTE_D6_REOPEN`; a new item is raised only from a new recommendation.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written, or is refused for a missing element | The transaction writes nothing, the committee's answer is not applied and the case does not move | MSG-P7-003 | AC2, TC-E4-009-02, TC-E4-009-04 |
| X2 | The role does not hold the right of the operation (U to submit, RA to answer) | 403 before any read or write, no item is raised and no record is written | MSG-P4-002 | TC-E4-009-03 |
| X3 | The case is not at `ROUTE_D6`, or the amount or the recommended route is absent | The branch does not run, nothing is escalated and the missing element is named | MSG-GEN-001 | TC-E4-009-01 |
| X4 | No delegation row covers the product, the decision and the amount, or the row is stale | The branch holds, names the missing value and raises a task; no item is escalated on an unknown limit | MSG-GEN-001 | TC-E4-009-01, TC-S1-E4009-APP-02 |
| X5 | rwb-decision, rwb-case or rwb-access does not answer inside 2 s, or its breaker is open | The branch waits and retries on the workflow's schedule; nothing is written and the caller sees 503 with the platform envelope | None | TC-E4-009-01 |
| X6 | The amount is at or below the limit | The branch ends and the inside-limit story applies; no committee item and no escalation | None | TC-E4-009-01 |
| X7 | The committee refuses | The refusal and its coded reason are recorded and the case returns to `ROUTE_D6_REOPEN` under R-UNI-41 | None | TC-E4-009-01 |
| X8 | The item or the submission is repeated with the same `Idempotency-Key` | One record, one item, and the stored answer is returned; the repeat is counted | None | TC-S1-E4009-APP-02 |
| X9 | The recommendation changes while the item is open | The open item is withdrawn with its reason, the withdrawal is recorded and the case returns to `ROUTE_D6_REOPEN` | None | TC-S1-E4009-APP-02 |
| X10 | A component, a statement or a test reaches `recovery_case`, `delegation_limit`, another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR8, BR10, TC-S1-E4009-APP-01 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X9 are the paths the target call types and the delegation rule add, and X10 is the DP-01 boundary. Every limit, level, clock and coded reason is a value in force, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4009-CON, the rwb-decision, rwb-case and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P3, P7 or P4 |
| Negotiable | The activity names, the decision code and the shape of the branch's own elements are this story's choice; the operation, the rights, the messages, the states and the screen are fixed |
| Valuable | A route beyond the owner's limit reaches the committee with its gap, its level and its reasons, and the answer is provable with the version that made it |
| Estimable | One workflow branch, three activities, three clients, one record write, two case moves and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic limits, amounts and answers through the contract fakes, plus the stopped record write, the missing delegation row, the withdrawal and the duplicate submission |

### 7. Acceptance criteria

```gherkin
Feature: Approve a route above the limit at committee

  Scenario: AC1 Approve a route above the limit at committee (legacy RWB-E4-009 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns the case state "ROUTE_D6" for "RC-2027-000409"
    Given the rwb-decision contract mock returns the rule id and the delegation-of-authority limit in force for the case owner, with the level that covers the route amount
    Given the rwb-access contract mock returns the Treatment and offer right RA accepted for "RW-CREDCOMM"
    When the user acts on the screen
    Then takes the route to the credit committee when it is beyond the case owner's limit
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-009 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E4-009 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `the action is taken`, `the decision log cannot be written` and `takes the route to the credit committee when it is beyond the case owner's limit` all stand. The cross-service parts of AC1 are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and those added `Given` lines are the only additions to the legacy text; AC2 needs none, because the decision-record library is local to this service. "The decision log" of both criteria is the local decision record of DP-03 on its way to `rwb.decision-record.v1`, and `decision_log_entry` stays P7's ledger and is neither written nor read here. Neither criterion carries a limit, a level or a clock: those are data in force of their owners (GAP-2634; GAP-2635).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-009-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-009 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-14 | An authorized user overrides the route inside the delegation: record the coded reason, move the case to the chosen route | None |
| R-UNI-15 | The override is outside the user's limit: refuse the change and raise the request to the approver named in the matrix, one working day | None |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |
| R-UNI-41 | A person decides and names the missing data: return the case to the route decision and log the rule gap | None |

The two VR and BR rows are the rows of FSD S1 A2.9.3.1, copied character for character. The six universal rules are the rows of the Business Rules and Routing Logic v4 that this branch depends on: R-UNI-15 is the escalation this story builds, R-UNI-41 is the return after a refusal and after a withdrawal, R-UNI-39 is AC2 and R-UNI-38 is why the record carries the version in force.

| ID | Rule | Source |
|---|---|---|
| BR1 | A route whose amount is above the case owner's limit in force is not signed by the case owner: the item is escalated to the credit committee with the gap, the level and the reasons, and the case moves to `ESCALATED` | R-UNI-15; FSD S1 A2.9.1; REQ-S1-006 |
| BR2 | The limit, the level, the holders and the validity dates are read with their version; no limit, boundary, threshold or level is a constant, a default or a branch of the build | BR-S1-009; FSD S1 A2.9.3.1; GAP-2634 |
| BR3 | The case state is rwb-case's: this story reports `ESCALATED` and `ROUTE_D6_REOPEN` to the parent `CaseWorkflow` and writes no `recovery_case`, `assignment`, `task` or `timer` row | DP-01; Ownership Map (`recovery_case` owner P3) |
| BR4 | The committee answers under right RA of Treatment and offer, with a coded reason where the answer departs from the recommendation; a role without the right is refused with MSG-P4-002 | TSD S1 T6.1; AC1; GAP-2637 |
| BR5 | The committee's answer is recorded before anything is answered, under decision code D6 with the delegation version and the rule version in force; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; AC2 |
| BR6 | One item per case and recommendation: a repeated command with the same `Idempotency-Key` and a repeated fact with the same key raise no second item and no second record | API-S1-001; R-UNI-40; ASM-4340 |
| BR7 | No new table and no new column are created for the resolution: the level, the final call, the coded reason and the reference live in the local decision record, and the schema stays as the DB story creates it | GAP-2636; ASM-4340 |
| BR8 | The branch adds no scoring call and no route of its own: the recommendation, the amount and the expected return by route are the ones FEAT-VAL-05 to FEAT-VAL-07 produced in this workflow, and the branch reads them and recomputes nothing | Epics 3 to 8 Specification v3 FEAT-VAL-09; FSD S1 A2.9.2 |
| BR9 | No event is published and no Schedule is declared: the ownership rows give S1 no event and no job, and the one-working-day clock is a workflow timer on the open item | context pack S1 ownership rows; ASM-4342 |
| BR10 | No foreign key leaves `rwb_valuation` and no statement reaches another schema or a `v_ace_*` view: the case, the limit, the rule and the route are identifiers and values of other owners' facts | DP-01; TSD S1 T3.3 |
| BR11 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input; the record names the decider's role, and the decider's identity stays with the case and the access layer | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case states below are rwb-case's and are not changed by this story: the stage reports its outcome and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story owns is the state of the committee item and the record of its answer.

| From (case, on rwb-case) | Event | Condition | To |
|---|---|---|---|
| `ROUTE_D6` | OVERRIDE_REFUSED | The route amount is above the case owner's limit in force | `ESCALATED`, with the item raised and its clock started (R-UNI-15) |
| `ROUTE_D6` | ROUTE_OVERRIDDEN | The amount is inside the limit and the reason is coded | The chosen route, on the inside-limit path of RWB-S1-E4008-APP (R-UNI-14) |
| `ESCALATED` | Committee approved | The final call is approved | The route's own approved state, handed to the route-flow step |
| `ESCALATED` | Committee refused | The final call is refused | `ROUTE_D6_REOPEN` with the coded reason (R-UNI-41) |
| `ESCALATED` | The recommendation changes | A value, a payment or a deviation moves the picture | `ROUTE_D6_REOPEN`, the open item withdrawn with its reason (R-UNI-41) |
| `ROUTE_D6_REOPEN` | A fresh recommendation | The route decision runs again | `ROUTE_D6`, and the branch is re-tested against the limit |
| Any of the above | The record cannot be written | X1 | Unchanged, nothing applied and no answer (AC2) |

| Item state (this story) | Event | Condition | To |
|---|---|---|---|
| Not assessed | The command of a case at `ROUTE_D6` | The workflow reaches the branch | Reading the delegation row |
| Reading the delegation row | The limit, the level and the version answer | The amount is above the limit | Escalated to the committee |
| Reading the delegation row | The limit, the level and the version answer | The amount is at or below the limit | Closed, inside-limit path (X6) |
| Escalated to the committee | The committee's final call | The record and the idempotency row commit | Answered, both moves reported |
| Escalated to the committee | A change of the recommendation | X9 | Withdrawn, the reason recorded |
| Any | The record write fails, or the delegation row is absent | X1, X4 | Unchanged, held and named |

The state names `ROUTE_D6`, `ESCALATED` and `ROUTE_D6_REOPEN` are the rows of the D6 route set of the case of record, and no S1 route rule is in force for this branch, because the S1 package is Phase 2 (GAP-2635; ASM-4339).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDCOMM, credit approval committee member | Treatment and offer RA in TSD S1 T6.1 and the primary role of FSD S1 A2.9.3.3: approves or refuses the escalated route and records the committee's answer |
| RW-PRODHEAD, product head (Mortgage, HP, SSME) | Treatment and offer RA: the "also uses" role of A2.9.3.3, answering at the level the matrix names for the product |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the route decision and read the item, the answer and the record; they do not answer above their own limit |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU), RW-TEAMMGR (R), RW-COMPLAIN (R), RW-FRAUD (R), RW-LITOFF (R), RW-LEGAL (R), RW-CONDUCT (R), RW-RISK (R), RW-COE (R), RW-AUDIT (R), RW-BIANAL (R), RW-TRIBE (R) | TSD S1 T6.1 rows for the capability area: read the recommendation, the item and the record in scope, and change nothing |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks as people |
| rwb-valuation service identity | Runs the branch, reads the case state, the rule, the limit and the right, answers the two case moves, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. The legacy table gives right U to four officer roles and names no right for the committee that this story's approval needs, which is recorded as GAP-2637 with ASM-4341 and not smoothed over. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read or written as a table: the case state arrives on the rwb-case row and the two moves are answered |
| DF-WRK-009 to DF-WRK-016 | `assignment` (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at | Not read or written: the task behind the committee item is rwb-case's |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule id and its version arrive on the rwb-decision row, where one is in force |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | decision code, rule id, rule version, inputs reference, level, final call, coded reason, decided at, decider role | Write, one record per answer, before anything is answered |
| The delegation limit, its level and its version (no Field ID published) | The authority matrix in force: administered by rwb-access and versioned with its limit rows by rwb-decision, as the sibling stories of this service read it; the row is Not specified in the source documents (GAP-2634; ASM-4338) | The limit, the level L1 to L6, the holder's role, the valid-from date and the matrix version | Consumed on the owner's row, recorded in the decision record, never stored as a column |
| The route recommendation and the amount (no Field ID published) | FEAT-VAL-05 to FEAT-VAL-07, in this workflow | The route, the expected return by route with its model version, the amount, the confidence and the alternatives | Read from the workflow state; its element set is carried by GAP-2633 and ASM-4337 |
| DF-ACE-187 to DF-ACE-195 | `v_ace_valuation` (P1) | appraised_value, appraisal_date, appraisal_type | Not read here: the value behind the band is the appraisal stories' read of this service |
| DF-EXT-036 to DF-EXT-049 | `valuation_ext` (P1 data product) | accepted, accepted_at | Not read here: the acceptance that fixes the band is written by the accept story of this service |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S1 T3.1 and of the legacy Data table of the key, with the owners changed by the target. **No new table, no new column and no migration**: the ownership rows give S1 no table, `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). The committee's resolution, its reference and the level applied live in the record, and GAP-2636 carries the open point.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates, levels and versions. No name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, a workflow input or an answer; the decider is a role on the record, and the decider's identity stays with the case and the access layer.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the above-limit branch of the one operation the legacy Endpoints table names, and its shape is baselined by RWB-S1-E4009-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the submission, the recommendation, the amount and, on this branch, the escalation, the level and the delegation version, the final call and the coded reason (API-S1-001) | Treatment and offer, right U to submit and right RA to answer, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second item and no second record are raised |

The element list of `RouteRequest` and `Approval` is not published: TSD S1 T-A.2 names the two types and no field table, and the committee elements this branch adds are the baseline's (GAP-2633; ASM-4337). The branch adds no operation of its own. The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed row does not answer. The appraisal branch and the inside-limit branch of the same path are RWB-S1-E4001-APP and RWB-S1-E4008-APP; the slices share one path and one element set, additively versioned.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The rule-in-force, delegation-limit and level read (operation name Not specified in the source documents (GAP-2634; ASM-4338)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and version in force, the delegation limit for the product, the decision and the amount, the level and the matrix version; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and the route under approval, checked before an item is raised; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right U or RA and the scope of the caller; faked |
| The delegation-row read, where the owner confirms it on rwb-access (operation name Not specified in the source documents (GAP-2634; ASM-4338)) | `/api/recovery/access/v1` | P4 rwb-access | The same limit, level and version, read on the access service if its owner confirms the row; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The plan gives this slice no class C dependency, so each row is built against its document and its fake and the metadata row stays None. The fourth row is the open ownership point of GAP-2634 and is not called twice at run time: the branch reads the limit on one row, whichever owner confirms it at the tag.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR9). The one publication of the branch is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the answer (ASM-4342).

#### 12.4 Events consumed

None. The branch is reached inside `RouteDecisionWorkflow` from the route command, and no source publishes an event name for a route, a limit or an approval of this service; the ownership rows give S1 no job and no event. A redelivered command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per decision, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the route set, the amount and the rule and delegation versions; signals: the committee's answer and a change of the recommendation; carries the above-limit branch |
| `checkDelegation` | Activity, this story | `rwb-valuation` | The product, the decision code, the amount and the business date in; the limit, the level, the delegation version and the above-limit flag out |
| `escalateToCommittee` | Activity, this story | `rwb-valuation` | The case, the route, the amount, the expected return by route, the gap to the limit and the level in; the item reference and the reported case move out |
| `recordCommitteeAnswer` | Activity, this story | `rwb-valuation` | The final call, the coded reason and the level in; the decision record, the idempotency row and the answer out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1; the three activities are this branch's and the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice, fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The branch runs inside the workflow from the route command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. The one-working-day clock of R-UNI-15 is a workflow timer on the open item, read as a value in force, and not a Schedule.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the committee resolution is carried by the record and by GAP-2636 |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record of DP-03, one per answer |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `delegation_limit` (P4), `proceeds` (P8), `template` (P6), `deviation` (S8), `document` (P5), and every `v_ace_*` view and `valuation_ext` (P1). No foreign key leaves `rwb_valuation`: the case, the limit, the rule and the route are identifiers and values, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule and limit fake | The rule id and version in force, the delegation limit of `DOA-2026.11` for product `MTG` and decision `D6`, one row below the amount and one row above it with its level; no row for the product and the decision; no answer beyond 2 s | AC1, X4, X6, TC-S1-E4009-APP-02 |
| rwb-case case-state fake | Case `RC-2027-000409` at `ROUTE_D6` with its route under approval; the same case in `ESCALATED`; a case in another state | AC1, X3 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused, and right RA accepted and refused | TC-E4-009-03, X2 |
| rwb-access delegation fake, where the owner confirms the row | The same limit, level and matrix version as the rwb-decision fake, so that the branch answers the same either way | X4, GAP-2634 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2027-000409`, with the item, its clock, the limit, the level and the answer read once | TC-E4-009-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2634; ASM-4338).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed at run time | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-decision rule and limit row, the rwb-case state row and the rwb-access authorise row; one hop, 2 s. The access delegation row is a documented alternative and is not called twice |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 3 activities | `RouteDecisionWorkflow`, `checkDelegation`, `escalateToCommittee` and `recordCommitteeAnswer` on `rwb-valuation`; no Schedule, one timer |
| File | None of this service | The branch writes no file and calls no external system |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `routeapproval`, Java package `th.co.scb.ace.workbench.recovery.valuation.routeapproval`; front end `src/modules/recovery/valuation/RouteApproval.tsx`, the fragment SCR-13 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the branch: the record, the idempotency row and the answer commit together or not at all. DP-13 moves the base of the one operation and keeps the monolith path out of the build. DP-19 is how SCR-13 reaches this service, one hop through the gateway, and why the screen section fixes only the committee elements this branch adds to the merged answer. No other DP applies: the branch reads no ACE view (no DP-05), publishes no event (no DP-09) and runs no job (no DP-10).

**Dependencies the tables add and the plan does not hold.** The three consumed rows are class C dependencies in kind and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2634 (ASM-4338). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19; no other H row is added, so the lane stays at depth two.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` approval branch | Workflow | The above-limit branch: waits for the command, tests the limit, escalates, waits for the answer and reports both moves to the parent |
| `checkDelegation` | Activity | Reads the delegation limit, the level and the version, compares the amount and returns the above-limit flag |
| `escalateToCommittee` | Activity | Builds the item with its gap and its reasons, starts its clock and returns the item reference |
| `recordCommitteeAnswer` | Activity | Writes the decision record and the idempotency row in one transaction and returns the answer |
| `LimitClient` | Client | The rule, limit and level read of rwb-decision, one hop, 2 s, breaker, with the no-row path |
| `CaseStateClient` | Client | The case state and the route read of rwb-case, one hop, 2 s |
| `RouteApprovalRecordWriter` | Library adapter | Writes one record per answer, hash-linked, and refuses the branch when the write fails (DP-03) |
| `RouteApprovalController` | Controller | The above-limit branch of the route operation, its rights, its `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteApproval` | React component | Shows the item, its clock, the limit and the level, the answer and its reason, and the refused, held, withdrawn and not-recorded states on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the level, the final call or the reference: they live in the record (BR7).

**Configuration and reference data.**

- The delegation limit, the levels L1 to L6, the holders' roles, the valid-from dates and the matrix version, read as rows in force (GAP-2634).
- The one-working-day clock of R-UNI-15 and the coded reasons of R-UNI-14 and R-UNI-41, read as values in force and never as constants.
- The capability area Treatment and offer and its rights U and RA, as access rows read through the guard.
- The decision code D6 and the route codes of `LOV-ROUTE` are referenced with their identifiers and never enumerated in code.
- No S1 rule package is in force and no D6 rule row is published (GAP-2635).

**Build steps**

1. The approval branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, entered from the route command.
2. `LimitClient` against its fake, with the 2 s budget, the breaker, the no-row path and the no-answer path (X4, X5).
3. `checkDelegation`, with the above-limit, at-the-limit and below-the-limit paths (X6).
4. `escalateToCommittee` and the item's clock, with the withdrawal path (X9).
5. `CaseStateClient` and the state guard of the branch (X3).
6. `recordCommitteeAnswer` and the record with the decision code, the delegation version and the rule version where one exists (AC1).
7. `RouteApprovalRecordWriter` against the library stub, with the failed-write path (AC2, X1).
8. The idempotency row and the repeat of the same command (X8).
9. `RouteApprovalController` with the two rights, the `Idempotency-Key` and the problem mapping (TC-E4-009-03).
10. `RouteApproval` and SCR-13 through the composite route fake, and the boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to a foreign schema, no outbox row (X10, BR9, BR10).

**Feature flag.** `rwb.valuation.route-committee-v1`, read as a flag of the platform library; off means an above-limit route holds at the route decision with its gap shown and no committee item is raised.

**Done when.** The tests of section 16 pass, an above-limit route raises exactly one item in SIT with its level and its version, an at-limit route raises none, a missing delegation row holds with the missing value named, a forced record failure changes nothing and shows MSG-P7-003, a withdrawal closes the open item with its reason, no case row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the request, of the recommendation or of the delegation row is absent or invalid (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the right of the operation calls it, or a role without RA answers the item (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the answer is applied (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three message IDs are the rows of the legacy Validation and messages table of this key and of FSD S1 A2.9.3.1, and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. No message carries a limit, a level or a clock.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the committee part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Loading while the delegation row is read; recommendation with the route, the amount and the limit; overridden with the coded reason of an answer inside the delegation, which is the sibling story's path; submitted with the approved route. Plus escalated with the item, its level and its clock; refused with the reason and the return to the route decision; not recorded with MSG-P7-003; held with the missing value named |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the committee element list and the four service states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-009-01 | AC1: a route above the limit is escalated with its gap and its level, the answer is recorded and the moves are reported; a route at or below the limit escalates nothing; a missing delegation row holds | Component | Case `RC-2027-000409` with an amount above, at and below the limit of `DOA-2026.11`, and a product with no delegation row |
| TC-E4-009-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no answer applied, and MSG-P7-003 shown |
| TC-E4-009-03 | Access: a role without the right is refused with MSG-P4-002 | Component | An officer role without U, and a role without RA answering the item; 403 before any read |
| TC-E4-009-04 | Principle 5: a forced decision log write failure stops the action | NFR | A forced failure at the moment of the answer; no item applied, no record and no event |
| TC-S1-E4009-APP-01 | The boundary: no foreign schema write, no `v_ace_*` read and no published event | Component | The build scan of step 10, plus an outbox that must stay empty |
| TC-S1-E4009-APP-02 | The delegation edge: the version, the level and the gap on the record; the withdrawal of an open item; the duplicate submission | Component | Two matrix versions of the same product, an amount between them, a recommendation that changes while the item is open, and the same `Idempotency-Key` twice |

The four legacy case IDs are the legacy cases of RWB-E4-009 in their legacy order, with the Level column added. TC-E4-009-01 is Component because the branch is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness, which owns the cross-service journey of this key.

### 17. Guardrails

- No business value in code: the limit, the level, the holders, the clock and the coded reasons stay rows read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a workflow input, in an answer or in a log: identifiers, codes, amounts, dates, levels and versions only, and the record names the decider's role and never the decider.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- The case stays with rwb-case and the limit with its owner: no `recovery_case`, `assignment`, `task`, `timer` or `delegation_limit` row is written, and the case moves are answered and not applied (BR3, BR10).
- The answer is recorded before it applies and the command is idempotent; a build that applies an answer before its record fails the review (DP-03, BR5, BR6).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no DoA table read on a direct connection, no event published by this branch.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-009, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-VAL-09 Approve a route above the limit at committee, module S1, epic E4, depends on FEAT-APD-05 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.9.2 steps and integration points; A2.9.3.1 VR-S1-009-1 and BR-S1-009; A2.9.3.3 roles; A2.9.4.3 exception flows; requirements REQ-S1-001 to REQ-S1-008, REQ-S1-006 in particular; SCR-13 | 2, 3, 4, 5, 8, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 lists; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights, including RW-CREDCOMM RA; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| Epics 3 to 8 Specification v3 | The feature row of FEAT-VAL-09 with its role and its dependency on FEAT-APD-05 | 1, 2, 3, 8 |
| Logical data model | DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049 | 11 |
| Routing logic | R-UNI-14, R-UNI-15, R-UNI-38, R-UNI-39, R-UNI-40 and R-UNI-41; no D6 route-decision rule row is published | 4, 5, 8, 9, 14 |
| Architecture v5 | Slide 3, the route decision D6 and the delegation of authority; slide 8, the schema, base, topic and queue of the service | 2, 3 |
| Sibling stories | RWB-S1-E4008-APP and -CON, which split the same operation on the limit; RWB-S1-E4001-APP and -CON, which own the appraisal branch and the element set the route answer starts from | 1, 2, 3, 9, 12 |
| Patterns | DP-03, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2633 to -5; ASM-4337 to -6 | 1, 3, 4, 7, 8, 9, 11, 12, 13, 14, 16 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published element set of the committee answer, the consumed rows, the rights, the error envelope and the fakes: RWB-S1-E4009-CON.
- The inside-limit approval and its override reason: RWB-S1-E4008-APP and RWB-S1-E4008-CON.
- The appraisal, its age, its order and the acceptance: RWB-S1-E4001-APP, RWB-S1-E4002-APP and the appraisal stories of this service.
- The recommendation, the COLLINS return by route, the payoff and the settlement range: the sibling route stories of this service.
- The delegation matrix, its levels, its holders, its substitutes, its validity dates and its limit versions: their owners at the tag (GAP-2634). The D6 rule row and the S1 package: GAP-2635.
- The case of record, its states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval, the `approval` record and the central ledger: rwb-decision (P7).
- Where the committee resolution and its reference are stored: GAP-2636. The committee's right in the legacy permission table: GAP-2637.
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, its merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.

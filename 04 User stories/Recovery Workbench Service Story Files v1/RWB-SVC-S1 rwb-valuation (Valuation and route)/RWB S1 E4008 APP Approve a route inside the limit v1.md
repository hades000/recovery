# RWB-S1-E4008-APP Approve a route inside the limit

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S1-H |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4008-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-008 split out for rwb-valuation. Both legacy criteria of the key (AC1 and AC2) are copied word for word with their origin tags, and the cross-service parts they touch are mocked. The approval becomes the `approveRouteInsideLimit` step of `RouteDecisionWorkflow` on task queue `rwb-valuation`: it takes the recommendation of FEAT-VAL-07, reads the case state on rwb-case, the rule id, the rule version and the delegation-of-authority limit in force on rwb-decision and the caller's right on rwb-access, writes the decision record through the local library before anything is answered (DP-03), answers the case move to rwb-case and returns `Approval` on `POST /cases/{caseId}/route` at base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). The delegation limit, its boundaries and the authority-matrix row are not published (GAP-2629; ASM-4332); the four consumed rows and the case move publish no operation name and the plan carries no C row (GAP-2630; ASM-4333); the recommendation and `Approval` element sets are not published (GAP-2631; ASM-4334); no S1 rule package is in force for the approval (GAP-2632; ASM-4335). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to let the case owner approve the recommended route within their delegated limit**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-008. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the rules, messages and screen they name;
- the approval step `approveRouteInsideLimit` of `RouteDecisionWorkflow` on `rwb-valuation`, run when the case owner submits the route decision of a case whose recommendation is inside their limit;
- the approval elements of the route command and answer on `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, with its right and its `Idempotency-Key` (API-S1-001; DP-13);
- the comparison of the recommended route with the delegation-of-authority limit in force, read as data with its version and never written in code;
- the read of the case state and the answer of the case move on rwb-case, of the rule in force and the limit on rwb-decision, and of the right on rwb-access, one hop and 2 s each;
- the decision record of the approval, written through RWB-PLT-E1027-CON in the caller's transaction before the answer, with the rule id, the rule version and the limit applied (DP-03);
- the states of SCR-13 Route decision that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the consumed rows, the approval element set, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4008-CON; the route scoring, the expected return and the reasons of FEAT-VAL-05 to FEAT-VAL-07, which are the sibling route stories; the above-limit committee approval of FEAT-VAL-09 and the reconsideration of FEAT-VAL-11, which are sibling stories; the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case's (P3); the rule rows, the authority matrix, the limit versions and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The route decision chooses between restructure, settlement, guarantee claim, litigation, asset sale, debt sale and write-off. FEAT-VAL-07 scores those routes and recommends one with its reasons; FEAT-VAL-08 is the point where a person accepts that recommendation and is accountable for it. The FSD keeps the feature as FEAT-VAL-08 in module S1: the case owner approves the recommended route within their delegated limit, and the result is written to the decision log with the rule version.

Under D-RCV-60 the ownership of the facts around that act changes, and that is what this story carries.

- **the recommendation is already in the workflow.** FEAT-VAL-05 to FEAT-VAL-07 compute the expected return by route and the recommendation inside the same `RouteDecisionWorkflow`; the approval reads that result and adds no second scoring call and no second operation.
- **the limit is policy data.** BR-S1-008 forbids writing a value a business person may change in code, and the delegation of authority is a governed matrix. The step therefore reads the limit in force with its version and asserts no boundary; the limit value, its boundaries and the matrix row are not in the read sources (GAP-2629; ASM-4332).
- **inside means inside.** R-UNI-14 records a route overridden by an authorized user inside the delegation, and R-UNI-15 refuses an override outside the user's limit and raises it to the approver named in the matrix. This step is the inside-the-limit path; the above-limit path is FEAT-VAL-09.
- **the case stays with rwb-case.** The route states and the move that follows `ROUTE_APPROVED` are case states of the D6 route set; this story answers the move and writes no case row.
- **the decision is recorded first.** Legacy AC2 makes the step trustworthy: when the record cannot be written nothing changes and the user sees MSG-P7-003. Under DP-03 the record is local, hash-linked and written in the same transaction as the approval, and R-UNI-39 forbids any action that is not logged.
- **nothing is published.** The ownership rows give S1 no event, so the approval adds no name to `rwb.valuation.events.v1`; its outward facts are the route answer, the case move and the decision record, which the library sends to `rwb.decision-record.v1`.

The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records. The requirement the step serves is REQ-S1-006, that the route decision is approved inside the delegation of authority and above the limit reaches the committee.

### 3. Preconditions

- RWB-S1-E4008-CON is published: the route operation with its approval elements, the four consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story.
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The recommendation of FEAT-VAL-07 is available in the workflow state: the recommended route, the expected return by route, the reasons, the confidence and the alternatives. No source publishes the element set of that recommendation (GAP-2631; ASM-4334).
- The rwb-case case-state read and case-move answer are available for their fakes, the rwb-decision rule-in-force, limit and ledger read is available for its fake, and the rwb-access authorise operation is available for its fake; their operation names are Not specified in the source documents (GAP-2630; ASM-4333) and none is in this story's contract-dependency list, which is None.
- The delegation-of-authority limit in force is read as a governed data row with its version. The limit, its boundaries, the authority-matrix row that carries it, its owner and the rule id of this step are Not specified in the source documents (GAP-2629; ASM-4332); no S1 rule package is in force (GAP-2632; ASM-4335).
- The case is at the route decision with a recommendation inside the limit; a recommendation above the limit is routed to FEAT-VAL-09 and not approved here.
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case`, `rwb_decision`, `rwb_access` or a `recovery.v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-05 is not applied as a read path here).
- The legacy story, the FSD S1 v3 and the TSD S1 v2 carry status "In review" and no approval of them is recorded for this run; they are treated as a Draft baseline and this story stays at Draft (realignment v1) (ASM-4336).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4008-CON when its tests pass.

### 4. Flow

1. The case is at the route decision with a recommendation from FEAT-VAL-07; the case owner opens SCR-13 Route decision through the gateway-bff composite route and submits the approval through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1` (API-S1-001; DP-13, DP-19).
2. The controller checks the capability area Treatment and offer and its right U against the caller's scope, and forwards the command with its `Idempotency-Key`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` in namespace `rwb-recovery`.
3. The approval step `approveRouteInsideLimit` reads the recommendation from the workflow state: the route, the expected return by route, the reasons, the confidence and the alternatives considered. It makes no new model call and starts no new assessment (FEAT-VAL-05 to FEAT-VAL-07).
4. The step reads the case on rwb-case, one hop with a 2 s budget and a breaker: the case reference, its state and the asset link; a case not at the route decision is refused and nothing is written.
5. The step reads the rule and the delegation-of-authority limit in force on rwb-decision, one hop with a 2 s budget: the rule id, the rule version, the matrix row for the caller's role and the limit with its version. A missing answer leaves the step held and nothing is written (GAP-2629).
6. The step validates the command against VR-S1-008-1: the case, the chosen route and the acknowledgement of the reasons are required, and an absent or invalid element is refused with MSG-GEN-001 naming the field, with nothing written.
7. The step compares the chosen route and its amount with the limit in force for the caller: inside the limit it proceeds; above the limit it refuses the approval with its reason and routes the case to the committee story FEAT-VAL-09, recording no approval here (R-UNI-15).
8. Where the chosen route departs from the recommendation, the step requires the coded override reason and records it; the override inside the delegation is the R-UNI-14 path and the answer is marked overridden (R-UNI-14).
9. Before anything is answered, `RouteApprovalDecisionRecordWriter` writes one decision record through the local library: the case, the route, the expected return, the recommended route where it differs, the override reason, the rule id, the rule version, the limit applied with its version and the outcome. A failed write stops the step with nothing changed and nothing answered (DP-03; AC2, R-UNI-39).
10. The step answers the workflow with the approval; rwb-case applies the move from `ROUTE_D6` on `ROUTE_APPROVED` to the route's own approved state (R-RES-01, R-SET-01, R-DIL-01 and R-LIT-01 name the per-route states), and this service writes no case row.
11. The route operation answers `Approval` with the approved route, the expected return, the reasons, the limit applied and its version, and a repeat of the same `Idempotency-Key` returns the stored answer and records no second approval (R-UNI-40).
12. SCR-13 Route decision shows the recommendation, the approved or overridden state, the reasons and the limit applied, read only through the composite route; a later change of value, payment or deviation reopens the decision as a fresh one (REQ-S1-008, FEAT-VAL-11).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, no approval is answered and the case does not move | MSG-P7-003 | AC2, TC-E4-008-02, TC-E4-008-04 |
| X2 | The caller does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-008-03 |
| X3 | A required element of the command is absent or invalid | Nothing is written and the field is named | MSG-GEN-001 | TC-E4-008-01 |
| X4 | The chosen route is above the caller's limit in force | The approval is refused with its reason and the case is routed to FEAT-VAL-09; no approval is recorded | None (reason on the record) | TC-E4-008-01 |
| X5 | The chosen route departs from the recommendation and the override reason is absent | Nothing is written and the coded reason is required | MSG-GEN-001 | TC-E4-008-01 |
| X6 | The case is not at the route decision, or the recommendation is not on the case | The step does not run, nothing is approved and the state is reported to the parent | None | TC-E4-008-01 |
| X7 | rwb-case, rwb-decision or rwb-access does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 in the platform envelope | None | TC-E4-008-01 |
| X8 | The same approval is submitted twice with the same `Idempotency-Key` | One record, one answer and no second move; the repeat is counted | None | TC-S1-E4008-APP-02 |
| X9 | A component, a statement or a test reaches a `recovery_case` row, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR8, TC-S1-E4008-APP-01 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 to X8 are the paths the target call types and the decision add, and X9 is the DP-01 boundary. No band, threshold or limit is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4008-CON, the rwb-case, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P3, P7 or P4 |
| Negotiable | The activity names, the decision code and the shape of the step outcome are this story's choice; the operation, the rules, the messages, the screen and the approval elements are fixed by the baseline |
| Valuable | The case owner approves the recommendation they were shown, inside a limit that can be defended, with the record showing why and under which version |
| Estimable | One workflow step, two activities, three clients, one record write, one case move answer and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each path runs on synthetic cases through the contract fakes, plus the stopped record write, the above-limit route, the missing override reason and the duplicate command |

### 7. Acceptance criteria

```gherkin
Feature: Approve a route inside the limit

  Scenario: AC1 Approve a route inside the limit (legacy RWB-E4-008 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns the case state "ROUTE_D6" for "RC-2026-000408"
    Given the rwb-decision contract mock returns the rule id and the delegation-of-authority limit in force for the case owner
    Given the rwb-access contract mock returns the Treatment and offer right U accepted for "RW-CASEOWN"
    When the user acts on the screen
    Then lets the case owner approve the recommended route within their delegated limit
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-008 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E4-008 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `the action is taken`, `the decision log cannot be written` and `lets the case owner approve the recommended route within their delegated limit` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and those lines are the only additions to the legacy text. AC1 says the result is written "to the decision log with the rule version", which is the local decision record of DP-03 on its way to `rwb.decision-record.v1`. The criterion carries no limit value: the limit, its boundaries and the matrix row are data in force (GAP-2629; ASM-4332).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-008 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-14 | An authorized user overrides the route inside the delegation: record the coded reason, move the case to the chosen route | None |
| R-UNI-15 | The override is outside the user's limit: refuse the change, raise the request to the approver named in the matrix | None |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The two VR and BR rows are the rows of FSD S1 A2.8.3.1, copied character for character. The five universal rules are the rows of the Business Rules and Routing Logic v4 that this step depends on; R-UNI-14 and R-UNI-15 are the inside and outside of the delegation this story splits on.

| ID | Rule | Source |
|---|---|---|
| BR1 | The approval is inside the delegation or it is not an approval: a route above the caller's limit in force is refused with its reason and routed to FEAT-VAL-09 | R-UNI-15; FSD S1 A2.8.1 |
| BR2 | The limit is read from the authority matrix in force with its version; no limit, boundary, threshold or default is a constant of the build | FSD S1 A2.8.3.1 BR-S1-008; GAP-2629 |
| BR3 | The recommendation is the one FEAT-VAL-07 produced in this workflow; the approval adds no scoring call and no route of its own | Epics 3 to 8 Specification v3 FEAT-VAL-08 |
| BR4 | An override of the recommendation inside the delegation carries the coded reason; without the reason the command is refused | R-UNI-14; VR-S1-008-1 |
| BR5 | The approval is recorded before anything is answered, with the case, the route, the expected return, the recommended route, the override reason, the rule id, the rule version and the limit applied with its version; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR6 | The case is not this service's: no `recovery_case`, `assignment`, `task`, `timer` or `route` row is written here, and the case move is answered and not applied | Ownership Map (`recovery_case` owner P3) |
| BR7 | The authority matrix is administered by rwb-access and its limit version by rwb-decision; this story neither sets nor approves a limit | FSD S1 A2.8.3.3; FEAT-ADM-03 context |
| BR8 | One approval per case per recommendation: a repeated command with the same `Idempotency-Key`, and a repeated fact with the same key, raise no second record and no second move | API-S1-001; R-UNI-40 |
| BR9 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the rule, the limit and the route are identifiers of other owners' facts | DP-01; TSD S1 T3.3 |
| BR10 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows |
| BR11 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input; the approving user is an identifier held by the case and the access layer | Template and Rules v1 §R7.2 (s17) |

### 9. State transitions

The case state is rwb-case's and is not changed by this story: the step reports its outcome and rwb-case applies it to the case of record (BR6). What this story owns is the state of the approval step.

| From (case, on rwb-case) | Event | Condition | To |
|---|---|---|---|
| ROUTE_D6 | ROUTE_APPROVED | The recommendation is approved by the case owner inside the limit in force | The route's own approved state (R-RES-01, R-SET-01, R-DIL-01 and R-LIT-01 name the per-route states) |
| ROUTE_D6 | ROUTE_OVERRIDDEN | The case owner picks another route inside the delegation with a coded reason | ROUTE_D6_REOPEN, with the chosen route recorded (R-UNI-14) |
| ROUTE_D6 | OVERRIDE_REFUSED | The chosen route or its amount is above the caller's limit | ESCALATED to the approver named in the matrix, and FEAT-VAL-09 handles it (R-UNI-15) |
| ROUTE_D6 | The record cannot be written | X1 | Unchanged, nothing answered and no record (AC2) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The route command of a case at the route decision | The workflow is started on `rwb-valuation` | Reading the recommendation |
| Reading the recommendation | The recommendation is present in the workflow state | The case is at ROUTE_D6 | Reading the limit |
| Reading the limit | The rule and the limit answer with their versions | The route is inside the limit | Validating the command |
| Validating the command | The command is complete and the override reason is present where needed | The record is written and the transaction commits | Waiting, with the case move answered |
| Any | The record write, the transaction or a consumed row fails | X1, X7 | Waiting, nothing changed |

The state names are the rows of the D6 route set and live on the case of record. No S1 rule row is in force for this step, because the S1 package is Phase 2 (GAP-2632; ASM-4335).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: submit the approval and read the recommendation, the limit and the record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area; the FSD gives the case owner the primary use and the product head (Mortgage, HP, SSME) also uses it |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: they approve above the limit and at committee, which is FEAT-VAL-09 and not this step |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step, reads the case, the rule, the limit and the right, answers the case move, writes the decision record and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, status, stage_code | Not read or written as a table: the case state arrives on the rwb-case row and the move is answered |
| DF-WRK-009 to DF-WRK-016 | `assignment` (P3) | id, case_id, task_id, assignee_user_id | Not read or written: no task is raised by the approval |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the rwb-decision row |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | rule id, rule version, inputs reference, outcome, decided at | Write, one record per approval, before anything is answered |
| The delegation-of-authority limit and its matrix row (no Field ID published) | The authority matrix in force; its owner and row are Not specified in the source documents (GAP-2629; ASM-4332) | The limit applied to the caller, and the version of the matrix it was read under | Consumed as data, recorded in the decision record, never stored as a column |
| The route recommendation (no Field ID published) | FEAT-VAL-05 to FEAT-VAL-07, in this workflow | The route, the expected return by route, the reasons, the confidence and the alternatives | Read from the workflow state; its element set is Not specified in the source documents (GAP-2631; ASM-4334) |

Field IDs are those of the Logical Data Model and Data Dictionary v8, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). The ownership rows give S1 no table, so the approval, the limit applied and the override reason live in the decision record and in the answer to the case.

**No personal data.** The rows this story reads and writes carry identifiers, codes, amounts, dates and a rule version. The identity of the approving user is an identifier held by the case and the access layer; no name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy Endpoints table names, and its shape is baselined by RWB-S1-E4008-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the chosen route, the override reason where the answer departs from the recommendation, and the limit applied in the answer (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second approval is recorded |

The element list of `RouteRequest` and `Approval` is not published: TSD S1 T-A.2 names the two types and no field table (GAP-2631; ASM-4334). The approval adds no operation of its own. The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element or a missing override reason, and 503 when the decision library or a consumed row does not answer. The two valuation operations of the map belong to the appraisal-intake slice of RWB-S1-E4002-CON and are not touched here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state at the route decision and the route recommended on it; checked before an approval is recorded; read only; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2630; ASM-4333)) | `/api/recovery/case/v1` | P3 rwb-case | The move from `ROUTE_D6` on `ROUTE_APPROVED` or `ROUTE_OVERRIDDEN`, applied by the case of record; faked |
| The rule-in-force, delegation-limit and decision-log read (operation name Not specified in the source documents (GAP-2630; ASM-4333)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, the authority-matrix row and the limit with its version, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The limit is administered under the authority matrix and no source says whether its row travels on the rule-in-force answer, on a reference-data answer or through rwb-access; the step reads it on the answer its owner publishes and asserts no boundary (GAP-2629; ASM-4332). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2630 with ASM-4333.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR10). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. The approval is started by the case owner's command on the route operation and by nothing else; the ownership rows give S1 no event and no job, FSD S1 A2.8.4.4 declares no background event for the feature, and no source publishes a name for a route-recommended notice. The recommendation arrives in the workflow state of FEAT-VAL-07 and not as a subscription. A duplicate of the command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the asset key, the route set and the rule package in force; signals: the recommendation ready and the case-move answer |
| `approveRouteInsideLimit` | Activity, the approval of this story | `rwb-valuation` | The case, the recommended route, the expected return, the rule and the limit in force, the caller and the override reason in; the route, the limit applied with its version and the step outcome out |
| `recordRouteApproval` | Activity, the record of this story | `rwb-valuation` | The decision record, the idempotency row and the case-move answer out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the two activities are this story's; the scoring and intake activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The step runs inside the workflow from the case owner's command and owns no Temporal Schedule and no legacy Quartz job, because the ownership rows give S1 no job. No reminder or re-review timer is built here: the review of a held route decision belongs to FEAT-VAL-10 and to rwb-case's timers.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table; the store of the limit applied and the override reason is the decision record |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per approval (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `authority matrix` rows (P7), and every `v_ace_*` view (P1). No foreign key leaves `rwb_valuation`: the case, the rule, the limit and the route are identifiers, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | Case `RC-2026-000408` at `ROUTE_D6` with its asset link and recommended route; a case in another state | AC1, X6 |
| rwb-case move-answer fake | The move from `ROUTE_D6` on `ROUTE_APPROVED` accepted with its reference, and on `ROUTE_OVERRIDDEN` with its reason; refused with its reason | TC-E4-008-01 |
| rwb-decision rule and limit fake | The rule id and version in force for the business date; the authority-matrix row and the limit with its version for `RW-CASEOWN`; a limit below the route; the record the ledger holds | AC1, X4, X5 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-008-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000408`, with the recommendation, the reasons and the approved route elements read once | AC1, TC-E4-008-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2630; ASM-4333).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-case case-state and move rows, the rwb-decision rule and limit row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `approveRouteInsideLimit` and `recordRouteApproval` on `rwb-valuation`; no Schedule |
| File | None of this service | The route recommendation is computed in the workflow and no file is read or written here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `approval`, Java package `th.co.scb.ace.workbench.recovery.valuation.approval`; front end `src/modules/recovery/valuation/RouteApproval.tsx`, the fragment SCR-13 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the idempotency row and the case-move answer commit together or not at all. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway. No ACE view, data product or foreign schema is read, so DP-05 is not part of this pattern set.

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2630 (ASM-4333). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` approval branch | Workflow | Waits for the command, runs the approval, answers the case move and reports the outcome to the parent |
| `approveRouteInsideLimit` | Activity | Reads the recommendation from the state, reads the case, the rule and the limit, validates the command, tests the limit and the override reason |
| `recordRouteApproval` | Activity | Writes the decision record and the idempotency row, answers the case move and returns the limit applied and the outcome |
| `CaseStateClient` | Client | The case state, the recommended route and the move answer of rwb-case, one hop, 2 s |
| `RuleAndLimitClient` | Client | The rule id, the rule version and the authority-matrix limit at their version in force, from rwb-decision, one hop, 2 s |
| `AccessClient` | Client | The capability area, the right and the scope of the caller, one hop, 2 s |
| `RouteApprovalDecisionRecordWriter` | Library adapter | Writes one record per approval before anything else changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteApproval` | React component | Shows the recommendation, the approved or overridden route, the reasons and the limit applied on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the limit applied or the override reason: they are recorded in the decision record and answered to the case.

**Configuration and reference data.**

- The authority matrix and the limit versions are governed rows read through rwb-decision with their version; the limit, its boundaries and its row are not published (GAP-2629; ASM-4332).
- The route codes of `LOV-ROUTE` at their version in force (TSD S1 T3.2), read as data and never as constants.
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- No parameter is named in the sources for the limit or for the step, and no S1 rule package is in force (GAP-2632; ASM-4335).

**Build steps**

1. The approval branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the route command as its trigger.
2. `CaseStateClient` against its fake, with the 2 s budget, the breaker and the state guard (X6, X7).
3. `AccessClient` and the right check, with the refused path (X2).
4. `approveRouteInsideLimit` with the required-element and missing-override-reason paths (X3, X5).
5. `RuleAndLimitClient` and the limit test against the version in force, with the above-limit refusal (X4, BR1, BR2).
6. `recordRouteApproval` and `RouteApprovalDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
7. The idempotency row and the repeat of the same command (X8).
8. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-008-03).
9. `RouteApproval` and SCR-13 through the composite route fake (TC-E4-008-01).
10. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_access`, and no outbox row (X9, BR9, BR10).

**Feature flag.** `rwb.valuation.route-approval-v1`, read as a flag of the platform library; off means the approval is refused with its reason and the route decision stays on the recommendation it holds.

**Done when.** The tests of section 16 pass, an approval inside the limit fixes one route and records the limit with its version in SIT, an above-limit route is refused and escalated, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the command is absent or invalid, or the override reason is missing (X3, X5) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the approval changes anything (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three messages of the legacy key are copied unchanged from its message set. No message is reworded and no new one is added; the above-limit refusal carries its reason on the decision record and in the screen state, and no source publishes a message text for it (GAP-2629; ASM-4332).

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the approval part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Loading while the case and the limit are read; recommendation with the route, the expected return by route, the reasons, the confidence and the alternatives; overridden with the owner's coded reason; submitted with the approved route and the limit applied. Plus refused with MSG-P4-002, not recorded with MSG-P7-003, invalid or missing reason with MSG-GEN-001, and above the limit with its reason and the committee hand-off |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the approval element list and the states above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-008-01 | AC1: the case owner approves the recommended route inside the limit and the result is recorded with the rule version; a route above the limit is refused and escalated, and an override without a reason is refused | Component | Case `RC-2026-000408`, recommended route `R2`, a limit in force, one route inside it, one above it and one override without a reason |
| TC-E4-008-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no case move and MSG-P7-003 shown |
| TC-E4-008-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-008-04 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the approval; no record, no move and no event |
| TC-S1-E4008-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write and no published event | Component | The build scan of step 10, plus an outbox that must stay empty |
| TC-S1-E4008-APP-02 | Idempotency: the same command twice under one key records one approval and answers the stored answer | Component | The same command repeated within the key's life, and a second command under a new key |

The four legacy case IDs are the legacy cases of RWB-E4-008 in their legacy order, with the Level column added. TC-E4-008-01 is Component because the step is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the limit, its boundaries, the authority matrix and the route codes stay governed data or a rule row read with their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the move is answered and not applied (BR6).
- The decision is recorded before the change and the command is idempotent; a build that answers a move before its record fails the review (DP-03, BR5, BR8).
- The limit is not set, approved or overridden here: a build that writes a limit or a boundary fails the review (BR7).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-008, disposition Split (rework); AC1 and AC2 owned word for word by this story | 1, 7, 16 |
| Feature | FEAT-VAL-08 Approve a route inside the limit, module S1, epic E4, depends on FEAT-APD-02 and FEAT-VAL-07 | 1, 2, 3, 8 |
| FSD S1 v3 | A1.4 preconditions; A2.8.2 steps and integration points; A2.8.3.1 VR-S1-008-1 and BR-S1-008; A2.8.3.2 field catalog; A2.8.3.3 roles; A2.8.4.1 to A2.8.4.4; REQ-S1-006; SCR-13 | 2, 3, 4, 5, 8, 11, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-ROUTE`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| Logical data model | DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | 11 |
| Routing logic | R-UNI-14, R-UNI-15, R-UNI-38, R-UNI-39 and R-UNI-40; R-RES-01, R-SET-01, R-DIL-01 and R-LIT-01 name the per-route approved states; no S1 route rule is in force, because the S1 package is Phase 2 | 4, 8, 9, 14 |
| Patterns | DP-03, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2629 to -4; ASM-4332 to -5 | 1, 3, 4, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published shape of the route operation, the approval element set, the four consumed rows, the decision-record element, the workflow elements, the error set and the fakes: RWB-S1-E4008-CON.
- The scoring, the expected return by route, the reasons and the alternatives of FEAT-VAL-05 to FEAT-VAL-07: the sibling route stories of this service.
- The above-limit committee approval of FEAT-VAL-09 and the reconsideration of FEAT-VAL-11: sibling stories of this service.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the authority matrix, the limit versions, their approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right, and the administration of the authority matrix: rwb-access (P4) and FEAT-ADM-03.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.

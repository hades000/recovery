# RWB-S1-E4010-APP Hold the case and set a review date

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4010-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S1-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S1-E4010-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-010 split out for rwb-valuation. Both legacy criteria of the key (AC1 and AC2) are copied word for word with their origin tags. The hold becomes the `holdRouteDecision` step of `RouteDecisionWorkflow` on task queue `rwb-valuation`: it confirms the case on the rwb-case answer, reads the rule version in force, writes the hold and its review date to the local decision record through RWB-PLT-E1027-CON before anything is answered (DP-03), answers the case move to rwb-case, sets the review date as a workflow timer instead of a Quartz job, and returns the held state on the route operation at base `/api/recovery/valuation/v1` (DP-13), reached by SCR-13 through the gateway-bff composite route (DP-19). No event is published, because the ownership rows give S1 none. Where the hold, its reason and its review date are persisted is not published and the service owns no table (GAP-2638; ASM-4343); the review date has no clock owner, no rule row and no Schedule, and the prerequisite FEAT-CWC-11 is named without a name or an owner (GAP-2639; ASM-4344, ASM-4347); the field catalog of the feature carries the valuation fields and no hold field, and no hold-reason list or date bound is published (GAP-2640; ASM-4346, ASM-4348); the hold elements of the route operation have no published field table and the four consumed rows no published operation name (GAP-2641; ASM-4349). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S1-E4010-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner**, I want **the Workbench to let the owner hold a case where no route is right yet, with a date the hold is reviewed**, so that **the route is chosen on expected return with reasons**.

This is the application slice of legacy RWB-E4-010. It owns:

- the two legacy criteria of the key, AC1 and AC2, copied verbatim with their origin tags, and the messages, the rules and the screen they name;
- the hold step `holdRouteDecision` of `RouteDecisionWorkflow` on `rwb-valuation`, run when the case owner submits a hold instead of a route, and the `liftHold` wake the review date produces;
- the hold elements of the route command and of its answer on `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`, with its right and its `Idempotency-Key` (API-S1-001; DP-13);
- the decision record of the hold, written through RWB-PLT-E1027-CON in the caller's transaction before the answer, carrying the reason, the review date and the rule version in force (DP-03);
- the model of the hold's own waiting: the review date is a workflow timer of `RouteDecisionWorkflow`, not a Quartz job and not a Temporal Schedule, because the ownership rows give S1 no job;
- the states of SCR-13 Route decision that this step produces, reached through the gateway-bff composite route (DP-19).

It does not own: the published shape of the route operation, the hold element set, the consumed rows, the workflow elements, the rights, the error set and the fakes, which are RWB-S1-E4010-CON; the route recommendation, the COLLINS return, the payoff and the approvals of FEAT-VAL-05 to FEAT-VAL-09, which are the sibling route stories of this service; the re-scoring of the route on new information of FEAT-VAL-11, which is the sibling reconsideration story; the case of record, its held state, its timers and the parent `CaseWorkflow`, which are rwb-case's (P3), including the feature FEAT-CWC-11 the FSD names as the prerequisite; the rule rows, the package version and the central ledger, which are rwb-decision's (P7); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the field list of SCR-13, which are RWB-PLT-N001-CON; and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

Some cases reach the route decision with no route that is right yet: a value is still being challenged, a payment is expected, a document is outstanding or the expected return of every open route sits below the policy the case is priced against. Today the officer simply keeps the case, and nothing records why it is waiting or when it must be looked at again. FEAT-VAL-10 of module S1 makes that wait a decision: the case owner holds the case, names the reason, sets the date the hold is reviewed, and the Workbench records the hold with the rule version and brings the case back on that date.

Under D-RCV-60 four things change, and they are what this story carries.

- **the record is local and hash-linked.** The ownership rows give S1 no table, so the hold, its reason and its review date live in the local decision record of DP-03 with the rule version in force, and the record reaches `rwb.decision-record.v1` through the library. Where a durable column would sit is recorded, not invented (GAP-2638; ASM-4343).
- **the wait is Temporal's.** The legacy module ran its clocks on Quartz and the target replaces them with Temporal. A hold set for a date months away is exactly what a durable workflow waits for, so the review date is a timer of `RouteDecisionWorkflow` on `rwb-valuation`; no job, no Schedule and no polling row is added, because the ownership rows give S1 no job (GAP-2639; ASM-4344).
- **the case stays with rwb-case.** The held state is a state of the case of record and this service answers the move and does not apply it (ASM-4345). The FSD names FEAT-CWC-11 as the prerequisite of the feature, which is the case-and-workflow capability, and its identifiers are not published in the read sources (GAP-2639; ASM-4347).
- **nothing is published.** The ownership rows give S1 no event, so the hold adds no name to `rwb.valuation.events.v1`; its outward facts are the route answer, the case move and the decision record (ASM-4343).

The measure of the module is unchanged: recommendations accepted, read monthly from the decision log and the Workbench records. A hold that is reviewed on its date and then becomes a decided route is one of the ways that measure is earned. No requirement row of FSD S1 T8 carries the hold, and the absence is recorded rather than filled with an invented identifier (GAP-2638).

### 3. Preconditions

- RWB-S1-E4010-CON is published: the route operation with the hold elements, the four consumed rows, the decision-record element, the workflow elements, the rights, the error set and the fakes are baselined and handed to this story. The element set of `RouteRequest` and `Approval` is Not specified in the source documents beyond its two type names (GAP-2641; ASM-4349).
- RWB-PLT-E1027-CON is published with its writer stub: the local decision-record library writes in the caller's transaction, and a failed write stops the step with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-13 Route decision reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- The rwb-case case-state read and hold-move answer are available for their fakes; the hold state, its name and its transitions are rwb-case's and no source publishes the name (GAP-2638; ASM-4345).
- The rwb-decision rule-in-force read and ledger read are available for their fakes; their operation names and the rule id of this step are Not specified in the source documents (GAP-2639; GAP-2641; ASM-4349).
- The review date is a workflow timer of `RouteDecisionWorkflow` in namespace `rwb-recovery`; no Temporal Schedule and no Quartz job is declared for it, and no rule row of the routing logic fires a review date for the route decision (GAP-2639; ASM-4344).
- The hold reason arrives as a coded value from the screen; the code list is not published and the step asserts none of its values (GAP-2640; ASM-4346).
- No source places a bound on the review date: no minimum interval, no maximum hold and no hold limit exists for this feature, so the step tests that the date is present and records it as given (GAP-2640; ASM-4348).
- The service runs as its own login on schema `rwb_valuation`, holds the library objects `decision_record` and `idempotency_key`, holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case`, `assignment`, `decision_log_entry` or `rule_row` is refused by the database and fails the boundary test (DP-01).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S1-E4010-CON when its tests pass.

### 4. Flow

1. The case is at the route decision and no route is right yet; the case owner opens SCR-13 Route decision through the gateway-bff composite route and submits a hold with its reason and its review date through `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1` (API-S1-001; DP-13, DP-19).
2. The controller checks the capability area Treatment and offer and its right U against the caller's scope, and forwards the command with its `Idempotency-Key`; the command starts `RouteDecisionWorkflow` on task queue `rwb-valuation` in namespace `rwb-recovery`.
3. The hold step `holdRouteDecision` reads the case state on the rwb-case answer, one hop with a 2 s budget and a breaker, to confirm that the case is at the route decision and that no route is approved for it (ASM-4345).
4. The step validates the command against VR-S1-010-1: the hold reason and the review date are required, and an absent element is refused with MSG-GEN-001 naming the field, with nothing written.
5. The step reads the rule id and the version in force for the business date on the rwb-decision answer, so that the record can cite the version the decision was taken under (R-UNI-38 where the routing logic publishes it, and the legacy "with the rule version" of AC1 either way).
6. Where the case is not at the route decision, where a route is already approved, or where the caller is out of scope for the case, the step refuses and nothing changes.
7. Before anything is answered, `HoldDecisionRecordWriter` writes one decision record through the local library: the case, the hold reason code, the review date, the rule id and the version in force, the caller as an identifier and the outcome. A failed write stops the step with nothing changed and nothing answered (DP-03; AC2).
8. The step answers the workflow with the hold, and rwb-case applies the move to its held state on the case of record; this service writes no case row (ASM-4345).
9. The workflow sets its review timer to the review date and sleeps; on that date `liftHold` wakes the workflow, writes the lift to a second decision record with the reason `review_date_reached` and answers rwb-case with the move back to the route decision and a task for the case owner. The re-scoring of the route that follows is FEAT-VAL-11's, not this step's.
10. The route operation answers `Approval` with the held state, the reason, the review date and the record's rule version of the baseline, and a repeat of the same `Idempotency-Key` returns the stored answer and records no second hold.
11. The decision record reaches `rwb.decision-record.v1` through the library of DP-03, keyed by the case, with no personal data on it; this service publishes no event of its own.
12. SCR-13 Route decision shows the held state with the reason, the review date and the record, read only through the composite route, and the hold can be replaced by a decided route from the same screen.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | The transaction writes nothing, the hold is not answered and the case does not move | MSG-P7-003 | AC2, TC-E4-010-02, TC-E4-010-04 |
| X2 | The caller does not hold the Treatment and offer right of the operation | 403 before any read or write, and no record is written | MSG-P4-002 | TC-E4-010-03 |
| X3 | The hold reason or the review date is absent or invalid | Nothing is written and the field is named | MSG-GEN-001 | TC-E4-010-01 |
| X4 | The case is not at the route decision, or a route is already approved for it | The step refuses and no record is written | None (reason on the answer) | TC-E4-010-01 |
| X5 | The caller is out of scope for the case | The case is not shown as known and nothing is written | None (404 envelope) | TC-E4-010-01 |
| X6 | The hold reason code is not in the code list of the business date | The step refuses the code and names the field; no record is written | MSG-GEN-001 | TC-E4-010-01, GAP-2640 |
| X7 | rwb-case or rwb-decision does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 in the platform envelope | None | TC-E4-010-01 |
| X8 | The same hold is submitted twice with the same `Idempotency-Key` | One record, one answer and no second move; the repeat is counted | None | TC-E4-010-01 |
| X9 | The review date arrives while the case has already moved to a decided route | `liftHold` records the obsolete wake, writes no lift record and raises no task | None | TC-E4-010-01 |
| X10 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | s17, BR8, BR9 |

X1 and X2 are the exception paths of the legacy key carried onto the split, X3 and X6 are the two validation paths of the feature, X4, X5, X7, X8 and X9 are the paths the target call types and the timer add, and X10 is the schema boundary. No hold limit, interval or code value is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S1-E4010-CON, the rwb-case, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P1, P3, P7 or P4 |
| Negotiable | The activity names, the decision code and the shape of the step outcome are this story's choice; the operation, the rules, the messages, the screen and the hold elements are fixed by the baseline |
| Valuable | A case with no right route waits on a recorded reason and a recorded date, and comes back to the owner on that date instead of being forgotten |
| Estimable | One workflow step, one timer wake, two activities, three clients, two record writes, one case move answer and one screen fragment |
| Small | Finished inside two weeks with its tests on the fakes, including a timer test that does not wait |
| Testable | Each path runs on synthetic cases through the contract fakes, plus the stopped record write, the wrong case state, the unknown code, the duplicate command and an obsolete wake |

### 7. Acceptance criteria

```gherkin
Feature: Hold the case and set a review date

  Scenario: AC1 Hold the case and set a review date (legacy RWB-E4-010 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns the case "RC-2026-000410" at the route decision with no route approved
    Given the rwb-decision contract mock returns the rule id and the version in force for the business date
    Given the rwb-access contract mock returns the Treatment and offer right U for the caller
    When the user acts on the screen
    Then lets the owner hold a case where no route is right yet, with a date the hold is reviewed
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-010 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E4-010 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `the action is taken`, `the decision log cannot be written` and `lets the owner hold a case` all stand. The cross-service parts are mocked, so AC1 carries three `Given the <service> contract mock returns <x>` lines and those lines are the only additions to the legacy text. In the target the "date the hold is reviewed" is answered to rwb-case and held as a workflow timer, and the result is written "to the decision log with the rule version", which is the local decision record of DP-03 on its way to `rwb.decision-record.v1`. Neither criterion carries a business value: the reason codes, the date bound and the rule version are data in force (GAP-2640; ASM-4346, ASM-4348).

### 8. Business rules

| ID | Rule | Message |
|---|---|---|
| VR-S1-010-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-010 | No value a business person may change is written in code; it is read from reference data with its version | None |
| R-UNI-38 | A new rule version reaches its effective date: apply it to decisions taken from that date; open cases keep the version they were decided under | None |
| R-UNI-39 | The decision log entry cannot be written: block the action and raise an incident; no action proceeds unlogged | MSG-P7-003 |
| R-UNI-40 | The same event arrives twice with the same key: ignore the second, record the idempotency hit | None |

The two VR and BR rows are the rows of FSD S1 A2.10.3.1, copied character for character. The three universal rules are the rows of the Business Rules and Routing Logic v4 that this step depends on; R-UNI-38 is why the record carries the version in force on the business date and R-UNI-39 is the rule behind legacy AC2.

| ID | Rule | Source |
|---|---|---|
| BR1 | The held state is the case of record's: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the move is answered and not applied | Ownership Map (`recovery_case` owner P3); ASM-4345 |
| BR2 | The hold, its reason code and its review date are recorded before anything is answered, with the rule id and the version in force; a failed write changes nothing and shows MSG-P7-003 | DP-03; R-UNI-39; legacy AC2 |
| BR3 | The review date is waited for, not polled: the wait is a timer of `RouteDecisionWorkflow`, and no job, Schedule or polling row is added because the ownership rows give S1 no job | context pack S1 ownership rows; ASM-4344 |
| BR4 | The reason is a coded value of reference data read with its version; no code, list or bound is a constant of the build, and no source publishes a bound on the review date | FSD S1 A2.10.3.1 BR-S1-010; GAP-2640; ASM-4346, ASM-4348 |
| BR5 | One hold per case per command: a repeated command with the same `Idempotency-Key`, and a repeated wake with the same key, raise no second record and no second move | API-S1-001; R-UNI-40 |
| BR6 | A hold is taken only where no route is approved: a case that already holds a decided route is refused and nothing is recorded | FSD S1 A2.10.1; legacy AC1 |
| BR7 | No event is published: the ownership rows give S1 no event, and the step adds no name to `rwb.valuation.events.v1` | context pack S1 ownership rows; ASM-4343 |
| BR8 | No foreign key leaves `rwb_valuation` and no statement reaches another schema: the case, the rule and the reason code are identifiers of other owners' facts | DP-01 |
| BR9 | No person name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log or a workflow input; the caller is an identifier held by the case | Template and Rules v1 §R7.2 (s17) |
| BR10 | The lift on the review date writes its own record and answers its own move, and a wake that arrives on a case already decided records nothing | FSD S1 A2.10.4.4; GAP-2639 |

### 9. State transitions

The case state is rwb-case's and is not changed by this story: the step reports its outcome and rwb-case applies it to the case of record (BR1). What this story owns is the state of its own step and of its timer. **No source publishes a state name for a held route decision**: the States sheet of the routing logic covers the ten route sets and no route-decision set, so the table below names the state `held` and marks the name as open (GAP-2638; ASM-4345).

| From (case, on rwb-case) | Event | Condition | To |
|---|---|---|---|
| At the route decision, no route approved | The hold command is accepted | The reason and the review date are present and the record is written | `held`, with the review date and the record |
| `held` | `REVIEW_DATE_REACHED` | The workflow timer reaches the review date | Back at the route decision, with a task for the case owner |
| `held` | The reconsideration of FEAT-VAL-11 | A value, a payment or a deviation changes the picture | The hold is lifted and the route decision re-opens |
| `held` | The record cannot be written | X1 | Unchanged, nothing answered and no record (AC2) |
| `held` | A decided route is submitted for the same case | X9 | The wake records nothing and the decided route stands |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The route command of a case at the route decision | The workflow is started on `rwb-valuation` | Reading the case state |
| Reading the case state | The case is at the route decision and no route is approved | The rule version in force is loaded | Validating and recording |
| Validating and recording | The elements are present and the record commits | The case move is answered | Holding, with the review timer set |
| Holding | `REVIEW_DATE_REACHED`, or a reconsideration, or a decided route | X9 is not met | Waiting, with the lift answered |
| Any | The record write, the transaction or a consumed row fails | X1, X7 | Waiting, nothing changed |

The state names are rwb-case's and live on the case of record; `REVIEW_DATE_REACHED` is an event code the routing logic publishes for the litigation and write-off sets and no route-decision rule row consumes it, so the timer and not a rule raises the wake (GAP-2639).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT | Treatment and offer U in the legacy permission table of the key: take the hold, give the reason and the review date, and read the hold and its record |
| RW-CASEOWN (CRU), RW-RESTRUCT (CRUA), RW-SPECIAL (CRU), RW-GUARANT (CRU) | TSD S1 T6.1 rows for the capability area; FSD S1 A2.10.3.3 gives the case owner the primary use and the team manager also uses it |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Treatment and offer R: read only, in scope |
| RW-PRODHEAD, RW-CREDCOMM | Treatment and offer RA: they approve a route and set the policy the routes are priced against, which is not this step |
| SY-CASEWF, SY-RULES, SY-AGENT | Treatment and offer R: the service identities read the step and are subject to the same checks |
| rwb-valuation service identity | Runs the step and the timer, reads the case state and the rule version, answers the case move, writes both decision records and answers the route operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S1 T6.1 and of the legacy permission table of this key, and nothing wider. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_valuation`) | the case, the hold reason code, the review date, the rule id, the rule version, the caller identifier, the outcome and the decided-at time | Write, one record per hold and one per lift, before anything is answered |
| The hold reason and the review date (no Field ID published) | The record of this step | the code of the reason and the date the hold is reviewed | Written to the decision record; a column has no published shape (GAP-2638; ASM-4343) |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule_id, rule_version, route_set, from_state, event_code | Not read as a table: the rule and its version arrive on the rwb-decision row |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (P3) | id, case_no, product_group, primary_person_key, status, stage_code | Not read or written: the case state arrives on the rwb-case row and the move is answered |
| DF-WRK-009 to DF-WRK-016 | `assignment` (P3) | id, case_id, task_id, assignee_user_id, assigned_at, ended_at | Not read or written: the task of the review date is rwb-case's and is answered, not created |
| DF-CAS-036 to DF-CAS-045 | `deviation` (P3) | deviation_code, raised_at, paused_state | Not read: a deviation that lifts this hold is FEAT-VAL-11's signal and rwb-case's state |
| The hold reason code list | Reference data of the business date | the codes the screen may send | Consumed as data, recorded in the decision record, never enumerated in the build (GAP-2640; ASM-4346) |

Field IDs are those of the Logical Data Model and Data Dictionary v9, of TSD S1 T3.1 and of the legacy Data table, with the owners changed by the target. The legacy Data table of this key names `recovery_case`, `assignment`, `decision_log_entry` and `rule_row` and no hold or review-date field, so the hold is carried by the decision record and not by a column of this service. **No new table, no new column and no migration**: the schema `rwb_valuation` and its login arrive with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in it by the library's migration (DP-03). Where the data owner confirms a hold or review-date column on a table of this service, the DB story adds it and this story's writer fills it (GAP-2638; ASM-4343).

**No personal data.** The rows this story reads and writes carry identifiers, codes, dates and a rule version. The identity of the caller is an identifier held by the case and the access layer; no name, address, contact value or identity number enters `rwb_valuation`, the decision record, a log, an interface input or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story supplies the behaviour behind the one operation the legacy Endpoints table names, and its shape is baselined by RWB-S1-E4010-CON.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the hold reason and the review date in the command and the held state, the reason, the review date and the record's rule version in the answer (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat, and no second hold is recorded |

The element list of `RouteRequest` and `Approval` is not published: TSD S1 T-A.2 names the two types and no field table (GAP-2641; ASM-4349). The hold adds no operation of its own; where a hold needs a write of its own, no owner publishes one and the baseline declares none. The errors are 400 for a malformed request, 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid or unknown element, and 503 when the decision library or a consumed row does not answer. The two valuation operations of the map belong to the appraisal-intake slice of RWB-S1-E4002-CON and are not touched here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, its route state and the scope check, before a hold is recorded; read only; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2641; ASM-4349)) | `/api/recovery/case/v1` | P3 rwb-case | The move to the held state with the review date, the lift back to the route decision and the task for the case owner; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2641; ASM-4349)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, the reason code list where it is carried there, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The reason code list is read as reference data of the business date and no source says which answer carries it, so the step reads it on the answer its owner publishes and asserts no code (GAP-2640; ASM-4346). These rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, and the absence is recorded as GAP-2641 with ASM-4349.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event, so this story adds no name, no outbox row and no payload to `rwb.valuation.events.v1`, and a build that publishes one here fails the absence test (BR7). The one publication of the step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1` in the transaction of the step.

#### 12.4 Events consumed

None. The hold is started by the case owner's command on the route operation and woken by its own timer; the ownership rows give S1 no event and no job, and FSD S1 A2.10.4.4 declares no background event for the feature. A duplicate of the command is caught by the idempotency row and not by a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the route set and the rule package in force; signals: the hold command, the review-date wake and the case-move answer |
| `holdRouteDecision` | Activity, the hold of this story | `rwb-valuation` | The case, the reason code, the review date, the rule id and the version in force in; the held outcome and the move out |
| `recordHold` | Activity, the record of this story | `rwb-valuation` | The decision record, the idempotency row and the case-move answer out, in one transaction |
| `liftHold` | Activity, the wake of the review date | `rwb-valuation` | The case, the review date and the record of the hold in; the lift record, the move back to the route decision and the task answer out |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1, and the three activities are this story's; the remaining activities of the route decision belong to the sibling stories. The activity names are a target design choice and are fixed by the baseline so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and the review date is waited for inside `RouteDecisionWorkflow` as a durable timer rather than as a Temporal Schedule or a Quartz job (BR3; ASM-4344). No source names a Schedule, a cut-off or a batch for the hold or for the review of a held case; the timer is the only clock of this story (GAP-2639).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table, so the hold, its reason and its review date live in the decision record and on the case of record (GAP-2638; ASM-4343) |
| decision_record | PLT library, created in `rwb_valuation` | The local hash-linked decision record, one per hold and one per lift (DP-03) |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

Not owned and never read as a table: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `deviation` (P3) and every `v_ace_*` view (P1). No foreign key leaves `rwb_valuation`: the case, the rule and the reason code are identifiers, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case-state fake | Case `RC-2026-000410` at the route decision with no route approved; the same case with a route approved; a case out of the caller's scope; no answer beyond 2 s | AC1, X4, X5, X7 |
| rwb-case move-answer fake | The move to the held state with the review date accepted with its reference, the lift back to the route decision accepted, and each refused with its reason | TC-E4-010-01 |
| rwb-decision rule and log fake | The rule id, the reason codes and their version in force for the business date; the record the ledger holds, once and twice | AC1, TC-E4-010-01 |
| rwb-access authorise fake | Treatment and offer, right U accepted and refused | TC-E4-010-03, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC2, X1 |
| Temporal test environment | A timer that can be skipped forward to the review date, and a wake that arrives on a decided case | TC-E4-010-01, TC-S1-E4010-APP-02, X9 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000410`, with the held state, the reason and the review date read once | AC1, TC-E4-010-01 |

The fakes are test-only and are replaced by the real services in SIT. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2641; ASM-4349).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-case state and move rows, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow, 3 activities and 1 timer | `RouteDecisionWorkflow`, `holdRouteDecision`, `recordHold` and `liftHold` on `rwb-valuation`; the review date is a workflow timer and not a Schedule |
| File | None of this service | The hold is command-driven and writes no file, and no source names a document for it |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.valuation`, module `hold`, Java package `th.co.scb.ace.workbench.recovery.valuation.hold`; front end `src/modules/recovery/valuation/RouteHold.tsx`, the fragment SCR-13 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record, the idempotency row and the case-move answer commit together or not at all, for the hold and for the lift. DP-13 moves the base of the one operation. DP-19 is how SCR-13 reaches this service, one hop through the gateway. DP-10 is not in this story's pattern set: the review date is a workflow timer of the one workflow S1 owns, and no Schedule is declared (ASM-4344).

**Dependencies the tables add and the plan does not hold.** The four consumed rows are class C dependencies of this story and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded as GAP-2641 (ASM-4349). The three H rows of the metadata are the contract of this key and the two platform contracts of DP-03 and DP-19, and no other H row is added.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RouteDecisionWorkflow` hold branch | Workflow | Waits for the hold command, runs the hold, sets the review timer, wakes on it and reports the outcome to the parent |
| `holdRouteDecision` | Activity | Reads the case state and the rule version, validates the command, refuses an unknown reason code and answers the hold |
| `recordHold` | Activity | Writes the decision record and the idempotency row, answers the case move and returns the held outcome |
| `liftHold` | Activity | Wakes on the review date, writes the lift record, answers the move back to the route decision and raises the task, and records nothing on a decided case |
| `CaseStateClient` | Client | The case state, the route state, the scope check and the move answer of rwb-case, one hop, 2 s |
| `RuleInForceClient` | Client | The rule id, the version in force and the reason codes, from rwb-decision, one hop, 2 s |
| `AccessClient` | Client | The capability area, the right and the scope of the caller, one hop, 2 s |
| `HoldDecisionRecordWriter` | Library adapter | Writes one record per hold and one per lift before anything else changes, hash-linked, and refuses the step when the write fails (DP-03) |
| `RouteController` | Controller | The route operation, its capability area and right, the `Idempotency-Key`, and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `RouteHold` | React component | Shows the held state, the reason, the review date and the refused, invalid and stale states on SCR-13, read only |

**Database and migrations.** No Flyway file. `rwb_valuation` and its login arrive with the DB story of this service, and the decision record and the idempotency key are library objects created in it by the library's migration (DP-03). No column is added for the hold reason or the review date: they are recorded in the decision record and answered to the case, and the store is GAP-2638 until its owner names it.

**Configuration and reference data.**

- The hold reason code list and the rule version in force of the business date, read as data and never as constants (GAP-2640; ASM-4346).
- The capability area Treatment and offer and its rights are access rows of rwb-access, read through the guard.
- The consumer of the library's topic `rwb.decision-record.v1` is the ledger's; this service only writes the record.
- No parameter is named in the sources for a hold interval, a maximum hold or a review bound, and no S1 rule package is in force (GAP-2639, GAP-2640; ASM-4348).

**Build steps**

1. The hold branch of `RouteDecisionWorkflow` and its input record, registered on `rwb-valuation`, with the route command as its trigger.
2. `CaseStateClient` against its fake, with the 2 s budget, the breaker, the scope path and the no-answer path (X5, X7).
3. `AccessClient` and the right check, with the refused path (X2).
4. `holdRouteDecision` with the required-element and the unknown-code paths (X3, X6).
5. `RuleInForceClient` and the rule version recorded with the hold (BR2).
6. `recordHold` and `HoldDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
7. The review timer of the workflow and `liftHold`, on a test environment whose clock can be skipped to the review date (BR3, TC-S1-E4010-APP-02).
8. The obsolete-wake path: a wake on a case that has a decided route records nothing (X9).
9. The idempotency row and the repeat of the same command (X8).
10. `RouteController` with the right, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 (TC-E4-010-03).
11. `RouteHold` and SCR-13 through the composite route fake (TC-E4-010-01).
12. The boundary test: no statement outside `rwb_valuation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_access`, and no outbox row (X10, BR7, BR8).

**Feature flag.** `rwb.valuation.hold-v1`, read as a flag of the platform library; off means the hold is refused with its reason and the case owner keeps the case at the route decision.

**Done when.** The tests of section 16 pass, a hold is recorded with its reason, its review date and its rule version in SIT, the review date wakes the case without any job or Schedule, a decided case ignores an obsolete wake, a forced record failure changes nothing and shows MSG-P7-003, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-13 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the command is absent or invalid, or the reason code is not in the list of the business date (X3, X6) | Enter {field}. |
| MSG-P4-002 | A role without the Treatment and offer right calls the route operation (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the hold changes anything (X1, AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The three messages of the legacy key are copied unchanged from its message set, and no message is reworded and no new one is added. The hold adds no message of its own: an unknown reason code is a required-field failure of MSG-GEN-001, and the refusals of X4, X5 and X9 are answers of the operation and not messages of the screen.

### 15. Screens and states

SCR-13 Route decision is served through the gateway-bff composite route (DP-19), and this story fixes the hold part of its answer and the states it can show.

| Screen | States | What this story sets |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | Loading while the case state is read; recommendation with the routes and, where none is right yet, the hold action with its reason and review date; overridden with the owner's reason; submitted with the decided route. Plus held with the reason, the review date and the record, refused with MSG-P4-002, not recorded with MSG-P7-003, invalid or unknown code with MSG-GEN-001, and refused on a case that already holds a decided route |

The screen's route elements, its merge order and its field list belong to RWB-PLT-N001-CON and the sibling route stories of this service; the hold elements and the held state above are this story's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-010-01 | AC1: the hold is taken with its reason and its review date and recorded with the rule version; an invalid element, an unknown code, a wrong case state and an out-of-scope case write nothing; the review date wakes the case | Component | Case `RC-2026-000410` at the route decision, a reason code, a review date, an absent date, an unknown code, a case with a route approved and the timer skipped to the review date |
| TC-E4-010-02 | AC2: the decision log cannot be written | Component | The decision-record stub stopped; nothing written, no case move and MSG-P7-003 shown |
| TC-E4-010-03 | Access: a role without the right | Component | A role without Treatment and offer U; 403 with MSG-P4-002 and no read |
| TC-E4-010-04 | Principle 5: a forced decision log write failure | NFR | A forced failure at the moment of the hold; no record, no move and no event |
| TC-S1-E4010-APP-01 | The boundary: no `v_ace_*` read, no foreign schema write and no published event | Component | The build scan of step 12, plus an outbox that must stay empty |
| TC-S1-E4010-APP-02 | The review timer: the wake fires on the review date, answers the lift and a decided case ignores an obsolete wake | Component | A workflow whose clock is skipped to the review date; the same wake on a case with a decided route |

The four legacy case IDs are the legacy cases of RWB-E4-010 in their legacy order, with the Level column added. TC-E4-010-01 is Component because the step is tested on its fakes; the legacy wording of the case is kept in the Test Cases workbook, where the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases. The `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in code: the reason codes and the rule version stay reference data read with their version, and no hold interval, maximum hold or date bound is a constant, a default or a branch of the build.
- No personal data in `rwb_valuation`, in a workflow input or in a log: identifiers, codes, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test.
- The case stays with rwb-case: no `recovery_case`, `assignment`, `task` or `timer` row is written here, and the move is answered and not applied (BR1).
- The decision is recorded before the change and the command is idempotent; a build that answers a move before its record fails the review (DP-03, BR2, BR5).
- The wait is Temporal's: a build that adds a Quartz job, a Temporal Schedule or a polling table for the review date fails the review (BR3).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base `/api/recovery/v1`, no event published by this step, no `v_ace_*` read.

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-010, disposition Split (rework); AC1 and AC2 owned word for word by this story; TC-E4-010-01 to -04; feature FEAT-VAL-10, depends on FEAT-CWC-11 | 1, 7, 16 |
| FSD S1 v3 | A1.4 preconditions; A2.10.1 intent and metric; A2.10.2 steps and integration points; A2.10.3.1 VR-S1-010-1 and BR-S1-010; A2.10.3.2 field catalog; A2.10.3.3 roles; A2.10.4.1 to A2.10.4.4; SCR-13 | 2, 3, 4, 5, 8, 11, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.3 relationships; T4 no state machine; T5.2 and T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 13, 16 |
| Epics 3 to 8 specification v3 | FEAT-VAL-10 with its primary role, its systems and its prerequisite; the APIs sheet gives S1 the one route operation | 2, 3, 12 |
| Logical data model | DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-016, DF-CAS-036 to DF-CAS-045 | 11 |
| Routing logic | R-UNI-38, R-UNI-39 and R-UNI-40; the `REVIEW_DATE_REACHED` event code; the States sheet carries no route-decision set and no held state; no S1 rule row fires the review date | 8, 9, 12.4, 12.6, 14 |
| Patterns | DP-03, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2638, -2, -3 and -4; ASM-4343 to -7 | 1, 2, 3, 4, 8, 9, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The published shape of the route operation, the hold element set, the four consumed rows, the decision-record element, the workflow elements, the error set and the fakes: RWB-S1-E4010-CON.
- The COLLINS return by route, the payoff and settlement range, the route agent and the approvals inside and above the limit of FEAT-VAL-05 to FEAT-VAL-09: the sibling route stories of this service.
- The reconsideration of the route on a new value, payment or deviation and the re-scoring that follows a lift: FEAT-VAL-11, the sibling reconsideration story of this service.
- The case of record, its held state, its name, its timers, `assignment` and `task`, the parent `CaseWorkflow` and FEAT-CWC-11: rwb-case (P3) (GAP-2638; ASM-4345, ASM-4347).
- The durable store of the hold reason and the review date, where a column is confirmed: the data owner of this service (GAP-2638).
- The reason code list, its identifiers and its values: the reference-data owner (GAP-2640; ASM-4346).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

# RWB-S7-E6017-APP Route the population to the committee and schedule it

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-E |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6017-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the committee-routing slice of legacy RWB-E6-017 split out for rwb-writeoff. The four legacy acceptance criteria are kept word for word with their origin tag; routing the prepared pack to the committee is now the routing branch of `WriteOffWorkflow` on task queue `rwb-writeoff`, which evaluates R-WO-11 (and R-WO-10 where the pack arrives from the pack check) and R-WO-06 of the WO package, records the decision through the local decision-record library before `write_off` changes (DP-03), writes the WRITEOFF state `WITH_COMMITTEE` or `CASE_REMOVED_BY_TEAM` and the record reference on the `write_off` row, assigns the committee queue and answers rwb-case for the case move on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). The two operations of this key, API-S7-001 and API-S7-002, belong to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP, so this step provides no routing operation of its own and its only read carries the placeholder, and the meeting booking, the five consumed contracts and the empty plan rows are recorded as GAP-3025 with ASM-5034 to -9. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member**, I want **the Workbench to send the pack to the committee queue and book it into the monthly meeting**, so that **write-offs follow the criteria and the committee's decision**.

This is the routing slice of legacy RWB-E6-017. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screens they depend on;
- the routing branch of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (context pack workflow row, `WriteOffWorkflow`; Temporal and Drools Design slide 13, "Write-off · rwb-writeoff · WO 51");
- the evaluation of R-WO-11 on the prepared pack, of R-WO-10 where the pack arrives from the pack check, and of R-WO-06 on an open deviation, with the WO package version in force (Business Rules and Routing Logic v4; TSD S7 T4, "51 rules over 27 states");
- the WRITEOFF transition of `write_off.state`, `PACK_PREPARED` to `WITH_COMMITTEE` and `POPULATION_PROPOSED` to `CASE_REMOVED_BY_TEAM`, and the write of `write_off.decision_log_id` with the record of the outcome, in schema `rwb_writeoff`;
- the local decision record of the outcome, written through RWB-PLT-E1027-CON before the row changes (DP-03), which is what legacy AC1 and AC4 require;
- the assignment of the pack to the write-off committee queue and the meeting booking, carried with the outcome;
- the answer to rwb-case for the case move `WITH_COMMITTEE` or `CASE_REMOVED_BY_TEAM` with the rule ID and its version, and the route of the held case to rwb-deviation.

It does not own: the published shapes of the consumed rows and of the `write_off` element, the state vocabulary, the rights, the error set and the fakes, which are RWB-S7-E6017-CON; the monthly eligibility scan and the tax criteria, API-S7-001 and the scan job JOB-16, which are RWB-S7-E6013-APP and RWB-S7-E6014-APP; the pack itself, its documents and its check, which are RWB-S7-E6015-APP; the removal by the team under R-WO-07, which is RWB-S7-E6016-APP; the committee decision act, API-S7-002, and the approve, reject and defer outcomes, which are RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP; the case of record, its route states and the queue table, which are rwb-case's (P3); the deviation facts and their handler, which are rwb-deviation's (S8); the rule package, the approval chain and the ledger, which are rwb-decision's (P7); the documents, which are rwb-document's (P5); and the deployment of this build, which is the operations story of this legacy key and the wave 4 harness.

### 2. Business rationale

Legacy RWB-E6-017 gave the Workbench one step that sent the committee pack to the committee queue and booked it into the monthly meeting, so that write-offs follow the criteria and the committee's decision. The FSD keeps the objective unchanged — "Sends the pack to the committee queue and books it into the monthly meeting" (FSD S7 A2.5.1) — against the module metric "write-off packs accepted first time, rising each month", measured on the decision log and the Workbench records and reviewed monthly. The problem is unchanged as well: write-off populations are assembled by hand each month.

What D-RCV-60 changes is where the pack, the queue, the state and the decision live:

- **the write-off is this service's.** `write_off` is S7's only table, in `rwb_writeoff` (context pack ownership row `write_off`; TSD S7 T3.1, DF-FIN-010 to DF-FIN-020), so the state of the write-off stage and the record reference are written here and nowhere else.
- **the case and the queue are not this service's.** `recovery_case`, its route states and the work queues are rwb-case's (P3); the legacy Data table names `recovery_case` and `queue` and this story reads them on the rwb-case contract and **answers** the case move. The queue table and every qualification of the committee queue are P3's (GAP-3025; ASM-5034).
- **the deviation is not this service's.** R-WO-06 holds a case out of the population when `deviation_open in (X1 to X7)` and routes it to the deviation handler; the deviation fact and the handler are rwb-deviation's (S8) (ASM-5034).
- **the rule package and the ledger are not this service's.** The 51 rules over 27 states are governed in rwb-decision (P7) and read here at their version; the ledger entry is P7's, and this service keeps the local decision record of DP-03 (ASM-5005, ASM-5040).
- **the step provides no routing operation.** The two operations the legacy story lists are the scan (API-S7-001) and the committee decision (API-S7-002), which the split gives to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP; the routing runs on the arrival of the prepared pack. DP-13 moves the key's base to `/api/recovery/writeoff/v1`, and the only element this story provides on it is the read behind SCR-27, whose path and operation ID are unpublished and carry the placeholder; DP-19 composes the screen from it (GAP-3025; ASM-5038).
- **the step publishes nothing.** The service's event EV-24 `WriteOffApproved` is the committee's approval, which is RWB-S7-E6018-APP's, not the routing (ASM-5036).

The binding values are unchanged and are not written in code: the write-off committee limit that R-WO-11 tests, the deviation codes X1 to X7 and the meeting calendar are rows of the package, of reference data and of parameters, read with their version.

The delivery is the plan's: this key is EP06 and therefore wave 4, and rwb-writeoff is created in wave 4 (Architecture v5), so the two agree and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5035).

### 3. Preconditions

- RWB-S7-E6017-CON is published: the `write_off` element, the WRITEOFF state vocabulary, the consumed rwb-case, rwb-deviation and rwb-decision rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-case contract is available for the fake: the case state read (`GET /cases/{caseId}` family) and the case-move answer. No source publishes an operation that moves a case state on behalf of a stage, so the answer is the stage outcome the parent `CaseWorkflow` applies and any REST name is Not specified in the source documents (GAP-3025; ASM-5034).
- The committee-queue assignment is available for the fake. The legacy Data table names `queue` (DF-WRK-001 to DF-WRK-008) and the queue belongs to rwb-case, and the operation that assigns a queue item is Not specified in the source documents (GAP-3025; ASM-5034).
- The rwb-deviation read of the open deviation and its handler route are available for the fake; the operation names are Not specified in the source documents (GAP-3025; ASM-5034).
- The rwb-decision WO package read is available for the fake: R-WO-06, R-WO-10 and R-WO-11 at their version with the write-off committee limit; the operation name is Not specified in the source documents (GAP-3025; ASM-5034, ASM-5005).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 Write-off proposal reaches this service and rwb-case through the gateway-bff composite route, one hop each (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case.recovery_case`, `rwb_deviation.deviation`, `rwb_decision.rule_row` or a `v_ace_batch_status` read is refused by the database and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6017-CON when its tests pass.

### 4. Flow

1. RWB-S7-E6015-APP prepares the pack and the case sits in `PACK_PREPARED` on the write-off stage; this story receives the prepared pack and does not build it.
2. The routing branch of `WriteOffWorkflow` on queue `rwb-writeoff` receives the prepared pack and reads the case state on the rwb-case contract, one hop with a 2 s budget and a breaker.
3. The branch reads the `write_off` row in `rwb_writeoff`: the case reference, the amount, the tax criteria flag and the pack reference, and the rule version in force from rwb-decision, so the package can be applied to the fact the pack step produced.
4. `WriteOffRoutingEvaluator` applies R-WO-06 first: where rwb-deviation reports an open deviation of code X1 to X7, the case is held out of the population, the outcome is `CASE_REMOVED_BY_TEAM` and the pack is routed to the deviation handler.
5. Where no deviation is open, the evaluator applies R-WO-11: where the amount is inside the write-off committee limit, the pack is routed to the committee and the meeting is scheduled, and the outcome is `WITH_COMMITTEE`. R-WO-10 is applied on the same branch when the pack arrives from the pack check with `provision_carried` and the pack document present, and it produces the same outcome.
6. Where the amount is outside the limit, R-WO-11 does not fire: the pack is not routed by this step and the escalation path R-WO-12 belongs to RWB-S7-E6018-APP; the branch records that no rule routed the pack and raises the task that the routing needs a person (legacy exception path).
7. `WriteOffDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**, with the case reference, the write-off reference, the rule ID and its version, the inputs reference, the outcome and the case move. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC4).
8. `WriteOffRoutingWriter` updates the `write_off` row in one `rwb_writeoff` transaction with the record, the idempotency row and the optimistic lock of `version`: `state` becomes `WITH_COMMITTEE` (R-WO-11, R-WO-10) or `CASE_REMOVED_BY_TEAM` (R-WO-06), and `decision_log_id` (DF-FIN-012) holds the identifier the library returns. `committee_date` (DF-FIN-015), `posted_date` and the GL columns are not written by this step.
9. `CommitteeQueueClient` places the pack on the write-off committee queue with the meeting date the routing produced, and on R-WO-06 answers the deviation handler instead; both are rwb-case and rwb-deviation answers and neither writes a queue row here.
10. `CaseMoveAnswer` answers rwb-case with the move `WITH_COMMITTEE` or `CASE_REMOVED_BY_TEAM`, the rule ID, the version and the decided-at time; rwb-case writes the case of record.
11. A repeated pack for the same write-off, rule and outcome writes nothing, sends no second queue item and no second case move, and counts the repeat.
12. SCR-27 Write-off proposal in its proposed, in-committee and removed states reads the population through the gateway-bff composite route, next to the case route state of rwb-case and the decision records of this service (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no state, no record reference, no queue item and no case move | MSG-P7-003 | AC4, TC-E6-017-04, TC-E6-017-06 |
| X2 | The role does not hold the Write-off and posting right of the read or of the act | 403 before any read or write, and the queue item and the screen refuse the action | MSG-P4-002 | AC1, TC-E6-017-05 |
| X3 | The write-off is not in `PACK_PREPARED` for R-WO-11, or not in `POPULATION_PROPOSED` for R-WO-06 | 409 and nothing is written; the step is not re-evaluated on a case that has already moved | None | AC2, AC3 |
| X4 | The amount is outside the write-off committee limit, or the limit is not in the package | R-WO-11 does not fire: no state change, no queue item and no meeting booking; the escalation is R-WO-12 at RWB-S7-E6018-APP | None | AC2 |
| X5 | The pack is stale after a late or failed ACE batch for its source | The step holds the pack and raises the freshness message; the freshness fact arrives with the pack, which reads it on the rwb-source-data contract, and this service reads no `v_ace_*` view | MSG-P1-001 | AC1, TC-E6-017-01 |
| X6 | The pack document or the carried provision is absent | R-WO-10 does not fire and the case stays in its pack state; the pack step owns the pack content and its check | None | AC1 |
| X7 | The rwb-case, rwb-deviation or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step waits and retries on the workflow's own schedule; nothing is written, no queue item and no case move is answered, and the caller sees 503 | None | AC1, AC2, AC3 |
| X8 | The same pack arrives twice for the same write-off, rule and outcome | One record, one update, one queue item and one case-move answer; the repeat is counted | None | AC1 |
| X9 | A component, a statement or a test reaches another service's schema, a queue table or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR6 |

X1 to X3 are the exception paths of RWB-E6-017 carried onto the split, X4 to X8 are the paths the rule package, the freshness and the call types add, and X9 is the DP-01, DP-02 boundary. The limit of X4, the deviation codes of AC3 and the meeting calendar are values in force in the package and in reference data, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6017-CON, the rwb-case, rwb-deviation and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P3, P7 or S8 |
| Negotiable | The activity name, the decision code and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the state values and the `write_off` columns are fixed |
| Valuable | A prepared pack reaches the committee queue with its meeting booking, or leaves the population with its reason, and the outcome is recorded in one place |
| Estimable | One workflow branch, one evaluator, three clients, one queue client, one record write, one row update, one case-move answer and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic packs and deviation facts through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Route the population to the committee and schedule it

  Background:
    Given write-off "WO-2027-000318" carries the prepared pack of case "RC-2027-000712"
    Given the WO rule package is in force at its version and carries R-WO-06, R-WO-10 and R-WO-11
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Route the population to the committee and schedule it (legacy RWB-E6-017 AC1)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-10 and R-WO-11 and the write-off committee limit
    Given the rwb-case contract mock returns the write-off committee queue for case "RC-2027-000712"
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then sends the pack to the committee queue and books it into the monthly meeting
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-11 (legacy RWB-E6-017 AC2)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-11 and a write-off committee limit above the amount of "WO-2027-000318"
    Given the rwb-case contract mock returns the case state "PACK_PREPARED" for "RC-2027-000712"
    Given the rwb-case contract mock returns the accepted move "WITH_COMMITTEE" and the committee queue item for "RC-2027-000712"
    Given a case in state PACK_PREPARED
    When pack routed
    Then route the pack to the committee and schedule the meeting
    Then the case moves to WITH_COMMITTEE

  Scenario: AC3 Rule R-WO-06 (legacy RWB-E6-017 AC3)
    Given the rwb-deviation contract mock returns an open deviation of code X4 for case "RC-2027-000712"
    Given the rwb-deviation contract mock returns the accepted route to the deviation handler for case "RC-2027-000712"
    Given the rwb-case contract mock returns the case state "POPULATION_PROPOSED" for "RC-2027-000712"
    Given a case in state POPULATION_PROPOSED
    When case has open deviation
    Then hold the case out of the population and route it to the deviation handler
    Then the case moves to CASE_REMOVED_BY_TEAM

  Scenario: AC4 Not recorded (legacy RWB-E6-017 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-017 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `its trigger arrives`, `pack routed`, `case has open deviation` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 carries two and AC2 and AC3 carry three `Given the <service> contract mock returns <x>` lines each; those added `Given` lines are the only additions. What the legacy lines describe now happens in four places: rwb-decision owns the WO package and the limit it carries, rwb-case owns the case state, the case move and the committee queue, rwb-deviation owns the open deviation and its handler, and this story evaluates R-WO-06, R-WO-10 and R-WO-11, records the decision and writes `state` and `decision_log_id` on the `write_off` row. Legacy AC2 and AC3 say "the case moves to …": the case route state is rwb-case's and is answered, while the named values are also the WRITEOFF states this service writes on `write_off.state` (ASM-5037). AC1's "decision log" is read as the local decision record of DP-03 written before the row changes, plus the ledger entry P7 writes (ASM-5040).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-11 | Write-off | D9 | PACK_PREPARED | PACK_ROUTED | amount inside the write-off committee limit | Route the pack to the committee and schedule the meeting | WITH_COMMITTEE | Write-off committee | Committee View, Workbench scheduler | before the scheduled meeting |
| R-WO-10 | Write-off | D9 | PACK_INCOMPLETE | PACK_COMPLETED | provision_carried and the pack document are present | Route the pack to the committee | WITH_COMMITTEE | Write-off committee | Case and Workflow Service, Committee View | None |
| R-WO-06 | Write-off | D9 | POPULATION_PROPOSED | CASE_HAS_OPEN_DEVIATION | deviation_open in (X1 to X7) | Hold the case out of the population and route it to the deviation handler | CASE_REMOVED_BY_TEAM | Deviation owner | Workbench, Decision Log | None |

The three rows are the rows of the Business Rules and Routing Logic v4, copied character for character, and they are the rows of the WRITEOFF machine of TSD S7 T4. Their owner column is a role of the business and not a service: the case move is answered to rwb-case, the deviation route is answered to rwb-deviation, the meeting scheduler row is read as the step's own scheduling answer, and the limit of R-WO-11 is a value of the package. R-WO-07, the removal by the team, is RWB-S7-E6016-APP's, and R-WO-12, the escalation above the limit, is RWB-S7-E6018-APP's.

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off stage state and the record reference are this service's: `state` and `decision_log_id` are columns of `write_off` in `rwb_writeoff`, and no other service writes them | Context pack ownership row `write_off`; TSD S7 T3.1 (DF-FIN-012, T3.0 `state`); DP-01 |
| BR2 | The decision is recorded before the `write_off` row changes, with the rule ID and the package version in force; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy RWB-E6-017 AC1 and AC4 |
| BR3 | The case, its route states and the queues stay with rwb-case: this service reads the state, answers the move and asks for the queue item, and writes no `recovery_case` row and no queue row | Context pack ownership rows; legacy Data table `recovery_case` and `queue`; ASM-5034 |
| BR4 | The deviation fact and its handler stay with rwb-deviation: this service reads the open deviation and answers the route, and stores no deviation column | Business Rules and Routing Logic v4 R-WO-06; ASM-5034 |
| BR5 | The rule package, its version and the ledger stay with rwb-decision: this service reads the package in force and writes its local decision record, and no rule row and no ledger entry of its own | DP-03; DP-04 (recorded, not claimed); ASM-5005 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_writeoff`; the case reference, the queue reference and the deviation reference are identifiers of other services' facts | DP-01, DP-02; TSD S7 T3.3 |
| BR7 | Only the two routing outcomes are written here: `committee_date`, `posted_date`, `gl_product`, `responsibility_center`, `cost_center` and `recovered_after` keep their values until the approval and the posting stories write them | TSD S7 T3.1; FSD S7 A2.5.3.2 field catalog; ASM-5040 |
| BR8 | Every value a business person may change is reference data, parameters or a rule row read with its version: the write-off committee limit, the deviation codes X1 to X7, the meeting calendar and the state list | FSD S7 A2.5.3.1 BR-S7-005; Template and Rules v1 §R3 default rulings; ASM-5039 |
| BR9 | A pack the rules do not route is not written: no state change, no queue item and no meeting booking, and the exception is raised on the case | R-WO-11 condition; FSD S7 A2.5.3.1 |
| BR10 | The same pack twice, or the same `Idempotency-Key` twice, writes once, queues once and answers the case move once | TSD S7 T-A.2; Architecture v5 slide 11 |
| BR11 | No person name, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR3). What this story writes is the WRITEOFF state of the `write_off` row.

| From (WRITEOFF, `write_off.state`) | Event | Condition | To |
|---|---|---|---|
| `PACK_PREPARED` | `PACK_ROUTED` under R-WO-11 | amount inside the write-off committee limit | `WITH_COMMITTEE`, with the record reference written and the queue item requested |
| `PACK_INCOMPLETE` | `PACK_COMPLETED` under R-WO-10 | provision_carried and the pack document are present | `WITH_COMMITTEE`, on the same branch and with the same write |
| `POPULATION_PROPOSED` | `CASE_HAS_OPEN_DEVIATION` under R-WO-06 | deviation_open in (X1 to X7) | `CASE_REMOVED_BY_TEAM`, with the record reference written and the deviation route answered |
| Any state the rule does not name | Any pack | X3, X4 | Unchanged, the repeat or the exception is counted |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The prepared pack arrives | The package in force is loaded | Evaluating |
| Evaluating | R-WO-06 fires, or it does not and R-WO-11 fires | The outcome is `CASE_REMOVED_BY_TEAM` or `WITH_COMMITTEE` | Applying |
| Applying | The record, the `write_off` row, the queue item and the case move are written | The transaction commits | Waiting for the next pack |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

The 27 states of the WRITEOFF machine are those of TSD S7 T4 and of the legacy criteria; `SCAN_DUE`, `SCAN_HELD`, `POPULATION_PROPOSED`, `PACK_PREPARED`, `PACK_INCOMPLETE`, `WITH_COMMITTEE`, `CASE_REMOVED_BY_TEAM`, `APPROVED`, `ESCALATED_TO_CREDIT_COMMITTEE`, `DEFERRED`, `POSTING_PENDING`, `POSTED` and `CASE_CLOSED` are the ones this key's stories read or write. No published list of case route states exists for the write-off route, so the case-side values are read from rwb-case on its contract and the two story-side values are the WRITEOFF states (ASM-5037).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU in TSD S7 T6.1: reads the population and the routing outcome; the C right it holds in the legacy table is exercised on the scan story |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: reads the population and the routing outcome; the A right is exercised on the committee decision story |
| RW-WOCOMM, write-off committee member | Write-off and posting RA: reads the pack in its committee state; the A right is exercised on API-S7-002 at RWB-S7-E6018-APP |
| RW-PRODHEAD, product head | Write-off and posting RA: reads the pack and its routing outcome |
| RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: reads the pack and its routing outcome |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Runs the branch, evaluates the rules, writes the record and the `write_off` row, asks for the queue item and answers the case move; no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S7 T6.1 and the two rows of the legacy Permission checks table, and nothing wider. The legacy table gives the A right to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the C right to RW-WRITEOFF and RW-CREDITAD, which is what T6.1's RA, CRUA and CRU rows say; no role of this story holds the A right on an operation, because the routing is unattended and the act is taken on API-S7-002 (ASM-5038). FSD S7 A2.5.3.3 names "None; runs unattended" as the primary user and "Write-off committee member" as the other user, which is the reading used here. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference of the row, the record and the answer |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case reference the move and the deviation route carry |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision-record library returns (ASM-5040) |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the value R-WO-11 tests against the write-off committee limit |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the tax criteria result of RWB-S7-E6014-APP |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: it is the committee approval date and belongs to RWB-S7-E6018-APP (BR7) |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: RWB-S7-E6021-APP writes it |
| DF-FIN-017, DF-FIN-018, DF-FIN-019, DF-FIN-020 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product, recovered_after | Not written here: the posting and the post charge-off stories write them |
| Standard columns | write_off (S7, `rwb_writeoff`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `state`, `updated_at`, `updated_by` and the optimistic lock of `version` on the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, outcome, decided at | Write through the local library, before the `write_off` row changes |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the rest | Not read as a table: the case state arrives on the rwb-case read and the move is answered (GAP-3025) |
| DF-CAS-036 to DF-CAS-045 | deviation (S8) | id, case_id, deviation_code, raised_at, raised_by, paused_state and the rest | Not read as a table: the open deviation arrives on the rwb-deviation contract (GAP-3025) |
| DF-WRK-001 to DF-WRK-008 | queue (P3) | id, queue_code, queue_name, team_code, role_code, assignment_method and the rest | Not read or written as a table: the queue item is requested on the rwb-case contract (GAP-3025) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | id, case_id, decision_code, rule_id, rule_version, model_version and the rest | Not written here: P7 writes the ledger entry; this service keeps the local record (ASM-5040) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the rule rows are governed in rwb-decision and loaded here as the package in force |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary v9. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes two of its existing columns, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_writeoff` by the library's own migration (DP-03). The legacy Data table lists five entities; three of them are other services' and are consumed on their contracts as the rows above state.

**No personal data.** The rows this story writes carry identifiers, an amount, a code and a rule version. No name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story provides one read and no routing operation.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-3025; ASM-5038) | The `write_off` element of section 11 with its `state`, its `decision_log_id` and the meeting booking, one write-off per read | Write-off and posting, right R, scope applied | Not declared |

The path, the operation ID and the element name of the read are not published: the API Specification v4 gives this service only `/write-off-scans` (API-S7-001) and `/write-offs/{writeOffId}/committee-decision` (API-S7-002), and the first is RWB-S7-E6013-APP's and the second RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. The read answers 400, 401, 403 with MSG-P4-002, 404 and 503 on the base above, and it is the leg of the gateway-bff composite route that SCR-27 renders (DP-19). A build that declares a routing operation on this base fails the absence test of the contract (GAP-3025; ASM-5038).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the stage the pack belongs to; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3025; ASM-5034)) | rwb-case (P3) | P3 rwb-case | The move `WITH_COMMITTEE` or `CASE_REMOVED_BY_TEAM` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The committee-queue assignment (operation name Not specified in the source documents (GAP-3025; ASM-5034)) | rwb-case (P3) | P3 rwb-case | The queue item of the write-off committee queue with the meeting date; the `queue` row is P3's; faked |
| The open-deviation read and the deviation-handler route (operation names Not specified in the source documents (GAP-3025; ASM-5034)) | `/api/recovery/deviation/v1` | S8 rwb-deviation | `deviation_open` of codes X1 to X7 for the case, and the route of the held case to the deviation handler; faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3025; ASM-5034, ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows R-WO-06, R-WO-10 and R-WO-11 with the write-off committee limit; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3025 with ASM-5034 and ASM-5005.

#### 12.3 Events published

None. The service owns event EV-24 `WriteOffApproved` on topic `rwb.writeoff.events.v1`, and it is the committee's approval, which is RWB-S7-E6018-APP's outcome and not the routing. This step therefore writes no outbox row, holds no producer of its own and fails the absence test if it adds an event (DP-09 is not in this story's pattern set; ASM-5036).

#### 12.4 Events consumed

None. No source gives rwb-writeoff a consumed event for this step: the pack arrives from RWB-S7-E6015-APP inside the same service, and the case and the deviation facts arrive on their owners' contracts. This story holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test (ASM-5036).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case, the write-off, the pack, the amount, the tax criteria flag and the package in force; signals: the prepared pack, the case state and the deviation answer |
| The routing branch of `WriteOffWorkflow` | Workflow branch, the step from the prepared pack to the committee queue or the deviation handler | `rwb-writeoff` | Applies R-WO-06, then R-WO-10 or R-WO-11, writes the record and the row, asks for the queue item and reports the stage outcome to the parent |
| `routePackToCommittee` | Activity, the one step of this story | `rwb-writeoff` | The case, the write-off and the package answer in; the rule ID with its version, the state, the record reference, the queue item and the case move out, in one transaction |

No child workflow of this service and no approval workflow exists in this step: the committee's act is the `ApprovalWorkflow` of the kit on the P7 queue, started by the approval story RWB-S7-E6018-APP. The activity name is a target design choice of this story and is fixed by no source document; the trigger is read as the arrival of the prepared pack for a write-off in `PACK_PREPARED`, because the FSD declares the scan as the only background event of the module (FSD S7 A2.5.4.4).

#### 12.6 Schedules

None. The step runs from the prepared pack and owns no Temporal Schedule, no Quartz row and no shared job table. JOB-16, the monthly write-off scan on the third working day on the ACE batch-complete record for ALS, is the scan story's (RWB-S7-E6013-APP) and is not owned, moved or registered here. The monthly committee meeting the step books the pack into has no published calendar, no `write_off` column and no Schedule element: the meeting date is carried in the decision record and in the queue item, and the calendar that produces it is Not specified in the source documents (GAP-3025; ASM-5039).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story updates `state` and `decision_log_id` |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated pack and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library and used by the stories that publish; this step writes no row of it (12.3) |

Not owned and never read as a table: `recovery_case`, `queue` and `timer` (P3), `deviation` (S8), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema and `write_off.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | The states `PACK_PREPARED`, `POPULATION_PROPOSED` and `WITH_COMMITTEE` of case `RC-2027-000712`; a case in a state the rule does not name | AC2, AC3, X3 |
| rwb-case case-move fake | The moves `WITH_COMMITTEE` and `CASE_REMOVED_BY_TEAM` accepted, and a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-case queue fake | The write-off committee queue item accepted with a meeting date, and a queue that refuses an item outside the committee queue | AC1, AC2 |
| rwb-deviation fake | An open deviation of code X1 to X7 for the case, no open deviation, and the handler route accepted; no answer beyond 2 s | AC3, X5, X7 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-06, R-WO-10 and R-WO-11 and the write-off committee limit above and below the amount | AC1, AC2, X4 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off `WO-2027-000318`, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the case move, the queue assignment, the deviation route and the package read are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3025; ASM-5034).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The write-off read behind SCR-27 on `/api/recovery/writeoff/v1`, with its path and operation ID on the placeholder; the rwb-case state read, the case-move answer and the queue item, the rwb-deviation read and route, and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval story's; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity | `WriteOffWorkflow` and its routing branch on `rwb-writeoff`, with its `routePackToCommittee` activity; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the pack documents are rwb-document's (P5) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.writeoff`, module `routing`, Java package `th.co.scb.ace.workbench.recovery.writeoff.routing`; front end `src/modules/recovery/writeoff/WriteOffRouting.tsx`, the fragment SCR-27 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the `write_off` update commit together or not at all, and the failed write is MSG-P7-003. DP-13 moves the base of the key's two operations, neither of which this story provides, so it adds no element here. DP-19 is how SCR-27 reaches this service and rwb-case, one hop through the gateway, and this story fixes the screen fragment only. No other pattern is claimed: the case, the queue, the deviation and the package are consumed contracts, so DP-05, DP-08, DP-09 and DP-10 stay off this table and their absence from the plan's rows is recorded in the registers (GAP-3025; ASM-5005, ASM-5036, ASM-5039).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. The five consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1 and the absence is recorded (GAP-3025; ASM-5034).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` routing branch | Workflow | Waits for the prepared pack, loads the package in force, applies R-WO-06 and then R-WO-10 or R-WO-11 and reports the outcome to the parent |
| `routePackToCommittee` | Activity | The one step: read the case and the write-off, evaluate the rules, write the record and the row, ask for the queue item and answer the case move |
| `WriteOffRoutingEvaluator` | Service | The rule evaluation against the WO package version in force, with the committee limit, the deviation codes and the state list read as package values and reference data |
| `CaseStateClient` | Client | The case state read, the case-move answer and the queue item of rwb-case; one hop, 2 s, breaker |
| `DeviationClient` | Client | The open-deviation read and the handler route of rwb-deviation; one hop, 2 s, breaker |
| `RulePackageClient` | Client | The WO package version in force of rwb-decision; one hop, 2 s, breaker |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID and the version before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `WriteOffRoutingWriter` | Repository | Updates `state` and `decision_log_id` in one `rwb_writeoff` transaction, with the idempotency row and the optimistic lock |
| `WriteOffRoutingController` | Controller | The read behind the SCR-27 fragment, with its path and operation ID on the placeholder (12.1), the capability area and right, the scope and the problem mapping of 400, 401, 403, 404 and 503 |
| `WriteOffRouting` | React component | Shows the pack, its routing state, its committee state and the removal reason on SCR-27, read only, with the refusal and failed-record states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the decision record, the idempotency key and the outbox are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the routing: `state` is the standard record column of TSD S7 T3.0 and `decision_log_id` is DF-FIN-012.

**Configuration and reference data.**

- The write-off committee limit and the state list of the WRITEOFF machine, read as package values and reference data at their version, never as constants.
- The deviation codes X1 to X7, read as reference data of rwb-deviation through the package and the deviation contract.
- The monthly meeting calendar, read as a parameter or a reference row; its source is Not specified in the source documents (GAP-3025; ASM-5039).
- The capability area "Write-off and posting" and its rights are access rows of rwb-access, read through the guard; no parameter is named in the sources for the step itself, and the 2 s budget and the single hop are the platform rule of ADR-020.

**Build steps**

1. The routing branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the prepared pack as its trigger.
2. `CaseStateClient` against its fake, with the state read, the move answer, the queue item, the 2 s budget and the no-answer path (AC1, AC2, X7).
3. `DeviationClient` against its fake, with the open-deviation read and the handler route (AC3, X5).
4. `RulePackageClient` and `WriteOffRoutingEvaluator` over the WO package, with R-WO-06, R-WO-10 and R-WO-11 and the no-fire path (AC1, AC2, AC3, X4).
5. `WriteOffDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `WriteOffRoutingWriter` with the one transaction, the two columns, the idempotency row and the optimistic lock (AC2, AC3, X8).
7. `CaseMoveAnswer` and the parent signal, with the two moves (AC2, AC3).
8. The read behind the SCR-27 fragment, with the rights, the scope and the problem mapping (AC1).
9. `WriteOffRouting` and the screen fragment through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_deviation`, `rwb_decision` or a queue table (X9, BR3, BR6).

**Feature flag.** `rwb.writeoff.committee-routing-v1`, read as a flag of the platform library; off means the branch holds the prepared pack, writes nothing, queues nothing and answers no move, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic prepared pack in SIT, R-WO-06 and R-WO-11 each produce their record, their state and their answer, a repeated pack writes once, a forced record failure changes nothing, no `recovery_case`, `deviation`, `queue` or `rule_row` row and no `v_ace_*` read exists in the build, and SCR-27 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate (R-WO-03) and RWB-S7-E6013-APP's path, so no path of this story raises it | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of the pack or of a consumed request is absent or invalid | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the population or the pack, or tries the act (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the `write_off` row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The pack's source data is stale after a late or failed ACE batch (VR-S7-005-1), and the freshness arrives with the pack (X5) | {product} is from {date}. Today's ACE batch has not arrived. |

The first four message IDs are those of the legacy message set of this key, and MSG-P1-001 is the message of VR-S7-005-1 in FSD S7 A2.5.3.1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added. MSG-S7-001 is carried because it is in the message set of the feature, and no path of this story raises it.

### 15. Screens and states

SCR-27 Write-off proposal — "the monthly population, the pack per case and removals with reasons", first in E6 (FSD S7 Screens) — is the screen of this step, in its scan, proposed, in-committee and approved states on the legacy screen table. It is served through the gateway-bff composite route (DP-19): the route calls this service for the write-off row and its routing state, rwb-case for the case and its route state and for the committee queue, and rwb-decision for the decision records. This story fixes the write-off answer and the screen fragment; the composite route specification and the screen field list belong to RWB-PLT-N001-CON, and the population operation behind the list is a placeholder (ASM-5038).

The states this story produces are the routing state of the write-off on SCR-27 — in committee with its meeting booking, or removed from the population with its reason — and the states it shows: refused with MSG-P4-002, not recorded with MSG-P7-003, held as stale with MSG-P1-001, and routed to the deviation handler under R-WO-06. The approved state of SCR-27 belongs to the committee decision stories of this service.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-017-01 | AC1 | Component | The prepared pack of write-off `WO-2027-000318` of case `RC-2027-000712`; the state, the record and the queue item asserted on the fakes |
| TC-E6-017-02 | AC2 | Integration | R-WO-11 with the committee limit above the amount; the `WITH_COMMITTEE` state, the record, the queue item and the case move asserted across the rwb-decision and rwb-case fakes |
| TC-E6-017-03 | AC3 | Integration | An open deviation of code X1 to X7; the `CASE_REMOVED_BY_TEAM` state, the record and the handler route asserted across the rwb-deviation and rwb-case fakes |
| TC-E6-017-04 | AC4 | Component | The decision-record stub stopped; nothing written, no queue item, no move answered and MSG-P7-003 shown |
| TC-E6-017-05 | Access | Component | A role without the Write-off and posting right; 403 with MSG-P4-002 and no read |
| TC-E6-017-06 | Principle 5 | Component | A forced decision log write failure at the moment of the row update; no column changed, no queue item and no move answered |

The six legacy cases are the legacy cases of RWB-E6-017 in their legacy order, with the Level column added: TC-E6-017-01, -04, -05 and -06 map to `Component` because the step is tested on its fakes, and -02 and -03 map to `Integration` because they cross the rwb-decision, rwb-case and rwb-deviation boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the write-off committee limit, the deviation codes, the meeting calendar, the state list and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, an amount, a code and a rule version only, and every fixture is synthetic.
- The ACE data only through an owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-01, DP-02).
- The case, its route states and the queues stay with rwb-case, the deviation with rwb-deviation, and the package and the ledger with rwb-decision: no `recovery_case` row, no queue row, no deviation column, no rule row and no ledger entry is written here (BR3, BR4, BR5).
- The scan, the pack, the removal by the team and the committee decision stay with their own stories of this service: this step declares no operation, no event and no rule of theirs (ASM-5036, ASM-5038).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no second event on the topic and no approval or queue table of this service's own.
- The decision is recorded before the change and the record and the update commit together; a build that writes the row first fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly (Must, E6; FSD S7 requirements served); this step routes the prepared pack and prepares none of it, and the requirement row for the routing step is empty in the plan and in the FSD (GAP-3025; ASM-5038) | The routing branch, the state and the queue item | TC-E6-017-01, TC-E6-017-02 |
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (Must, E6); this step records the routing outcome that precedes it and leaves the decision act to API-S7-002 (ASM-5038) | The decision record written before the row change | TC-E6-017-01, TC-E6-017-04 |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off row and its routing state | TC-E6-017-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-017-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget | TC-E6-017-02, TC-E6-017-03 |
| ADR-022 | Local decision record plus central ledger | The decision record written before the change, with the ledger entry in P7 | TC-E6-017-04, TC-E6-017-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-017, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-017-01 to TC-E6-017-06 |
| Feature and screens | FEAT-WOF-05, SCR-27 Write-off proposal |
| Rules | R-WO-06, R-WO-10 and R-WO-11, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the `write_off` element, the state vocabulary, the consumed rows, the rights, the error set and the fakes: RWB-S7-E6017-CON.
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001 with `ScanRequest` and `WriteOffScan`: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The pack, its documents, its carried provision and its check, under R-WO-05 and R-WO-10's pack half: RWB-S7-E6015-APP.
- The removal of a case by the team under R-WO-07 and API-S7-002's removal path: RWB-S7-E6016-APP.
- The committee decision act, API-S7-002 with `CommitteeDecision`, the approve, reject and defer outcomes and the escalation R-WO-12: RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP.
- The case of record, its route states, the queue table and the queue assignment: rwb-case (P3), whose state, move and queue answers this story consumes and fakes (GAP-3025).
- The deviation facts, the codes X1 to X7 and the deviation handler: rwb-deviation (S8) (GAP-3025).
- The WO rule package, its version, the approval chain and the ledger: rwb-decision (P7) (ASM-5034, ASM-5005).
- The freshness of the source data and the `v_ace_batch_status` read: rwb-source-data (P1), whose freshness fact arrives with the pack (ASM-5041).
- The pack documents and their custody: rwb-document (P5); the notices to customers: rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories (ASM-5038).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

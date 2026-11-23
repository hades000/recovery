# RWB-S7-E6018-APP Approve a write-off inside the limit

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6018-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6018-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the committee-approval slice of legacy RWB-E6-018 reworked for rwb-writeoff. The four legacy acceptance criteria are kept word for word with their origin tag; approving a write-off inside the delegation is now the committee branch of `WriteOffWorkflow` on task queue `rwb-writeoff`, which evaluates R-WO-15 and R-WO-12 of the WO package, records the final call, the approver and the limit applied through the local decision-record library before `write_off` changes (DP-03), writes the WRITEOFF state `APPROVED` or `ESCALATED_TO_CREDIT_COMMITTEE` and the record reference on the `write_off` row, publishes `WriteOffApproved` on `rwb.writeoff.events.v1`, and serves `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). The delegation limit, the credit committee outcome of R-WO-13 and R-WO-14, the placement of the approver and of the limit applied, and the plan's empty rows are recorded as GAP-3027 with ASM-5042 to -10. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off committee member**, I want **the Workbench to let the committee approve within its delegation and record the limit applied**, so that **write-offs follow the criteria and the committee's decision**.

This is the approval slice of legacy RWB-E6-018. It owns:

- the four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages and screen they depend on;
- the committee branch of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` owned by rwb-case (context pack workflow row `WriteOffWorkflow`; Temporal and Drools Design slide 13, "Write-off · rwb-writeoff · WO 51");
- the evaluation of R-WO-15 on the delegation, and of R-WO-12 where the amount is above the write-off committee limit, with the WO package version in force (Business Rules and Routing Logic v4; TSD S7 T4, "51 rules over 27 states");
- the operation `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, Write-off and posting right A) on `/api/recovery/writeoff/v1`, with `CommitteeDecision` in and the decision record out (TSD S7 T-A.1 and T-A.2);
- the WRITEOFF transition of `write_off.state` from `WITH_COMMITTEE` to `APPROVED`, and from `PACK_PREPARED` to `ESCALATED_TO_CREDIT_COMMITTEE`, with `write_off.decision_log_id` and `write_off.committee_date` in schema `rwb_writeoff`;
- the local decision record of the final call, the approver and the limit applied, written through RWB-PLT-E1027-CON before the row changes (DP-03), which is what legacy AC1, AC2 and AC4 require;
- the publication of `WriteOffApproved` (`EV-24`) on `rwb.writeoff.events.v1` in its `rwb.writeoff.WriteOffApproved.v1` shape, after the commit, through the outbox;
- the answer to rwb-case that releases the case to posting (`APPROVED`) or escalates it (`ESCALATED_TO_CREDIT_COMMITTEE`), with the rule ID and its version.

It does not own: the published shapes of the `write_off` element, of `CommitteeDecision`, of the consumed rows, the state vocabulary, the rights, the error set and the fakes, which are RWB-S7-E6018-CON; the monthly scan, the tax criteria and JOB-16, which are RWB-S7-E6013-APP and RWB-S7-E6014-APP; the pack and its check, which are RWB-S7-E6015-APP; the removal by the team, which is RWB-S7-E6016-APP; the routing to the committee queue, which is RWB-S7-E6017-APP; the reject and the defer, which are RWB-S7-E6019-APP and RWB-S7-E6020-APP; the posting to ALS and the general ledger, the provision release and the settlement of the escalated pack, which are RWB-S7-E6021-APP and the credit approval committee's own step (ASM-5044); the delegation table and the approval-inside-the-limit capability, which belong to rwb-case's reference data and to rwb-decision's FEAT-APD-02 (ASM-5043); the case of record, its route states and the queue table, which are rwb-case's (P3); the ledger entry, which is rwb-decision's (P7); the documents, which are rwb-document's (P5); and the deployment of this build, which is the operations story of this legacy key and the wave 4 harness.

### 2. Business rationale

Legacy RWB-E6-018 gave the Workbench one step that let the write-off committee approve within its delegation and recorded the limit applied. The FSD keeps the objective unchanged — "Lets the committee approve within its delegation and records the limit applied" (FSD S7 A2.6.1) — against the module metric "write-off packs accepted first time, rising each month", measured on the decision log and the Workbench records and reviewed monthly. The problem is unchanged as well: write-off populations are assembled by hand each month.

What D-RCV-60 changes is where the act, the delegation, the state and the record live:

- **the write-off is this service's.** `write_off` is S7's only table, in `rwb_writeoff` (context pack ownership row `write_off`; TSD S7 T3.1, DF-FIN-010 to DF-FIN-020), so the stage state, the record reference and the committee date are written here and nowhere else.
- **the delegation is not this service's.** "Inside the delegation" is the condition of R-WO-15 and the limit applied is a value of `delegation_limit` (DF-REF-016 to DF-REF-026, reference data) and of the approval-inside-the-limit capability FEAT-APD-02; both are read at their version and neither becomes a constant (ASM-5043).
- **the case and the queue are not this service's.** `recovery_case`, the route states and the work queues are rwb-case's (P3); the step answers the case move and reads the case state on that contract.
- **the approval chain and the ledger are not this service's.** The committee acts inside `ApprovalWorkflow` of the workflow kit on the P7 queue; the ledger entry is P7's, and this service keeps the local decision record of DP-03 (ASM-5049).
- **the escalation is this service's, its settlement is not.** R-WO-12 routes the pack to the credit approval committee chaired by the product head with Risk, and the write-off state becomes `ESCALATED_TO_CREDIT_COMMITTEE`; the credit committee's own approve or reject (R-WO-13, R-WO-14) is claimed by no story of this key and is recorded (ASM-5044).
- **the event is this service's.** The service owns topic `rwb.writeoff.events.v1` and event EV-24 `WriteOffApproved`, which is this approval's outcome; DP-09 is not in the plan's pattern set, so the outbox and inbox library row is absent and recorded (ASM-5045).

The binding values are unchanged and are not written in code: the write-off committee limit, the delegation limits per approval level and product group, the committee calendar and the rule rows are reference data, parameters and package rows read with their version.

The delivery is the plan's: this key is EP06 and therefore wave 4, and rwb-writeoff is created in wave 4 (Architecture v5), so the two agree and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5051).

### 3. Preconditions

- RWB-S7-E6018-CON is published: the `write_off` element, the `CommitteeDecision` and record elements, the WRITEOFF state vocabulary, the consumed rwb-case, rwb-decision and rwb-access rows, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-case contract is available for the fake: the case state read and the case-move answer. No source publishes an operation that moves a case state on behalf of a stage, so the answer is the stage outcome the parent `CaseWorkflow` applies and any REST name is Not specified in the source documents (GAP-3027; ASM-5047).
- The rwb-case reference-data contract is available for the fake: `delegation_limit` by decision code, approval level and product group with its versions (DF-REF-016 to DF-REF-026); the operation name is Not specified in the source documents (GAP-3027; ASM-5043).
- The rwb-decision WO package read is available for the fake: R-WO-12 and R-WO-15 at their version with the write-off committee limit; the operation name is Not specified in the source documents (GAP-3027; ASM-5043, ASM-5049).
- The rwb-access authorise answer is available for the fake: the capability area "Write-off and posting" and the right A for the act (TSD S7 T6.1); the operation name is Not specified in the source documents (GAP-3027; ASM-5048).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 Write-off proposal reaches this service and rwb-case through the gateway-bff composite route, one hop each (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case.recovery_case`, `rwb_decision.rule_row` or a `v_ace_*` view is refused by the database and fails the boundary test (DP-01, DP-02).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6018-CON when its tests pass.

### 4. Flow

1. The committee acts on the pack on SCR-27 and the gateway-bff composite route forwards the request to `POST /write-offs/{writeOffId}/committee-decision` with a `CommitteeDecision` body and an `Idempotency-Key` (DP-19, DP-13).
2. `WriteOffCommitteeController` validates the body, resolves the write-off and declares the capability area "Write-off and posting" with right A; a role without the right sees MSG-P4-002 and nothing is read further.
3. The committee branch of `WriteOffWorkflow` on queue `rwb-writeoff` is signalled with the request and loads the `write_off` row of `rwb_writeoff`: the case reference, the amount, the tax criteria flag and the current state.
4. `WriteOffCommitteeEvaluator` reads the WO package version in force from rwb-decision and the `delegation_limit` row for the decision code, the approval level and the product group from reference data, then applies R-WO-15: where the amount is approved inside the delegation, the outcome is `APPROVED`.
5. R-WO-12 is applied where the amount is above the write-off committee limit: the pack is routed to the credit approval committee chaired by the product head with Risk and the outcome is `ESCALATED_TO_CREDIT_COMMITTEE`; the case does not stop here, and the credit committee's own approve or reject is not this story's (ASM-5044).
6. `WriteOffCommitteeDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**, with the case reference, the write-off reference, the rule ID and its version, the approver identity, the limit applied, the inputs reference and the outcome. A failed write stops the act with nothing changed (DP-03; legacy AC1, AC2 and AC4).
7. `WriteOffCommitteeWriter` updates the `write_off` row in one `rwb_writeoff` transaction with the record, the idempotency row and the optimistic lock of `version`: `state` becomes `APPROVED` (R-WO-15) or `ESCALATED_TO_CREDIT_COMMITTEE` (R-WO-12), `decision_log_id` (DF-FIN-012) holds the identifier the library returns, and `committee_date` (DF-FIN-015) holds the committee approval date on the approved path (ASM-5046).
8. On the approved path `WriteOffOutboxWriter` writes one outbox row in the same transaction, and the relay publishes `WriteOffApproved` (`EV-24`) as `rwb.writeoff.WriteOffApproved.v1` on `rwb.writeoff.events.v1` with `writeOffId`, `caseId` and `amount`, consumed by rwb-payment (ASM-5045).
9. `CaseMoveAnswer` answers rwb-case with the move `APPROVED` or `ESCALATED_TO_CREDIT_COMMITTEE`, the rule ID, the version and the decided-at time; rwb-case writes the case of record and releases or escalates it.
10. The answer of API-S7-002 returns the decision record to the caller with status 200 and the `Idempotency-Key` stored; a repeated key returns the same record and writes nothing.
11. SCR-27 in its in-committee and approved states shows the outcome and the record through the composite route, next to the case route state of rwb-case (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing is written: no state, no record reference, no committee date, no outbox row and no case move | MSG-P7-003 | AC4, TC-E6-018-04, TC-E6-018-06 |
| X2 | The role does not hold the Write-off and posting right A | 403 before any read or write, and the screen refuses the action | MSG-P4-002 | AC1, TC-E6-018-05 |
| X3 | The write-off is not in `WITH_COMMITTEE` for R-WO-15, or not in `PACK_PREPARED` for R-WO-12 | 409 and nothing is written; the act is not re-evaluated on a write-off that has already moved | None | AC2, AC3 |
| X4 | The delegation limit, the approval level or the product group has no row in reference data | R-WO-15 does not fire and nothing is written; the act is refused and raised to the rule owner, never defaulted to a local value | MSG-GEN-001 | AC1, AC2 |
| X5 | A required field of `CommitteeDecision` is absent or invalid | 422 with the field name and nothing is written | MSG-GEN-001 | AC1 |
| X6 | The escalation is recorded and the credit committee's own outcome never arrives | The write-off stays in `ESCALATED_TO_CREDIT_COMMITTEE` and is reported as open; R-WO-13 and R-WO-14 are owned by no story of this key | None | AC3 |
| X7 | The rwb-case, rwb-decision, rwb-access or reference-data contract does not answer inside 2 s, or its breaker is open | The act waits and retries on the workflow's own schedule; nothing is written and the caller sees 503 | None | AC1, AC2, AC3 |
| X8 | The same request or the same `Idempotency-Key` arrives twice | One record, one update, one event and one case-move answer; the repeat is returned and counted | None | AC2 |
| X9 | A component, a statement or a test reaches another service's schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR6 |

X1 to X3 are the exception paths of RWB-E6-018 carried onto the split, X4 to X8 are the paths the delegation, the escalation, the call types and the idempotency add, and X9 is the DP-01, DP-02 boundary. The limits of X4, the delegation table of AC2 and the committee calendar are values in force in reference data and in the package, so none is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6018-CON, the rwb-case, rwb-decision and rwb-access fakes and the decision-record stub, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity name, the decision code and the shape of the stage outcome are this story's choice; the rules, the messages, the screen, the state values and the `write_off` columns are fixed |
| Valuable | The committee's call is made inside its delegation and recorded once, the case is released to posting or escalated, and the limit applied is provable from the record |
| Estimable | One operation, one workflow branch, one evaluator, four clients, one record write, one row update, one outbox row and one case-move answer |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic packs, delegation rows and package versions through the contract fakes, plus the component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Approve a write-off inside the limit

  Background:
    Given write-off "WO-2027-000318" carries the committee pack of case "RC-2027-000712"
    Given the WO rule package is in force at its version and carries R-WO-12 and R-WO-15
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Approve a write-off inside the limit (legacy RWB-E6-018 AC1)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-15 and the write-off committee limit
    Given the rwb-case contract mock returns the delegation limit row for the decision code, the approval level and the product group of case "RC-2027-000712"
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the committee approve within its delegation and records the limit applied
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-15 (legacy RWB-E6-018 AC2)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-15 and a write-off committee limit above the amount of "WO-2027-000318"
    Given the rwb-case contract mock returns the case state "WITH_COMMITTEE" for "RC-2027-000712" and accepts the move "APPROVED"
    Given a case in state WITH_COMMITTEE
    When committee approved
    Then record the final call, the approver and the limit applied, and release to posting
    Then the case moves to APPROVED

  Scenario: AC3 Rule R-WO-12 (legacy RWB-E6-018 AC3)
    Given the rwb-decision contract mock returns the WO package in force with R-WO-12 and a write-off committee limit below the amount of "WO-2027-000318"
    Given the rwb-case contract mock returns the case state "PACK_PREPARED" for "RC-2027-000712" and accepts the move "ESCALATED_TO_CREDIT_COMMITTEE"
    Given a case in state PACK_PREPARED
    When limit exceeded
    Then route the pack to the credit approval committee chaired by the product head with Risk
    Then the case moves to ESCALATED_TO_CREDIT_COMMITTEE

  Scenario: AC4 Not recorded (legacy RWB-E6-018 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The four criteria are the legacy criteria of RWB-E6-018 word for word, with their origin tag added and nothing else changed: the repetition of `Then`, the legacy wording of `the user acts on the screen`, `committee approved`, `limit exceeded` and `the action is taken` all stand. The cross-service parts are mocked, so AC1 carries two, AC2 carries two and AC3 carries two `Given the <service> contract mock returns <x>` or accepted-move lines; those added `Given` lines and the feature Background are the only additions. What the legacy lines describe now happens in four places: rwb-decision owns the WO package and the write-off committee limit, rwb-case owns the delegation row, the case state and the case move, and this story evaluates R-WO-15 and R-WO-12, records the final call, the approver and the limit applied, and writes `state`, `decision_log_id` and `committee_date` on the `write_off` row. Legacy AC2 and AC3 say "the case moves to …": the case route state is rwb-case's and is answered, while the named values are also the WRITEOFF states this service writes on `write_off.state` (ASM-5047). AC1's "decision log" is read as the local decision record of DP-03 written before the row changes, plus the ledger entry P7 writes (ASM-5049).

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-15 | Write-off | D9 | WITH_COMMITTEE | COMMITTEE_APPROVED | approved inside the delegation | Record the final call, the approver and the limit applied, and release to posting | APPROVED | Credit Administration | Committee View, Decision Log | None |
| R-WO-12 | Write-off | D9 | PACK_PREPARED | LIMIT_EXCEEDED | amount above the write-off committee limit | Route the pack to the credit approval committee chaired by the product head with Risk | ESCALATED_TO_CREDIT_COMMITTEE | Credit approval committee | Committee View, Reference data | before the scheduled meeting |

The two rows are the rows of the Business Rules and Routing Logic v4, copied character for character, and they are the rows of the WRITEOFF machine of TSD S7 T4. Their owner column is a role of the business and not a service: the case move is answered to rwb-case, the ledger entry is P7's, and the limit of R-WO-15 and of R-WO-12 is a value of the package and of reference data. R-WO-13 and R-WO-14, the credit committee's own approve and reject out of `ESCALATED_TO_CREDIT_COMMITTEE`, are not claimed by this story; R-WO-11, the routing to the committee, is RWB-S7-E6017-APP's, and R-WO-16 and R-WO-17, the reject and the defer, are RWB-S7-E6019-APP's and RWB-S7-E6020-APP's (ASM-5044).

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off stage state, the record reference and the committee date are this service's: `state`, `decision_log_id` and `committee_date` are columns of `write_off` in `rwb_writeoff`, and no other service writes them | Context pack ownership row `write_off`; TSD S7 T3.1 (DF-FIN-012, DF-FIN-015, T3.0 `state`); DP-01 |
| BR2 | The decision is recorded before the `write_off` row changes, with the rule ID, the package version in force, the approver and the limit applied; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy RWB-E6-018 AC1, AC2 and AC4 |
| BR3 | The delegation is reference data: the limit applied is the `delegation_limit` row of the decision code, the approval level and the product group, read at its version, and never a constant, a default or a branch of the build | FSD S7 A2.6.3.1 R-WO-15; legacy Data table `delegation_limit` (DF-REF-016 to DF-REF-026); ASM-5043 |
| BR4 | The case, its route states and the queues stay with rwb-case: this service reads the state, answers the move and writes no `recovery_case` row | Context pack ownership rows; legacy Data table `recovery_case`; ASM-5047 |
| BR5 | The rule package and the ledger stay with rwb-decision: this service reads the package in force and writes its local decision record, and no rule row and no ledger entry of its own | DP-03; DP-04 (recorded, not claimed); ASM-5049 |
| BR6 | No cross-schema join and no foreign key leaves `rwb_writeoff`; the case reference is an identifier of another service's fact | DP-01, DP-02; TSD S7 T3.3 |
| BR7 | The approval writes `APPROVED` and the escalation writes `ESCALATED_TO_CREDIT_COMMITTEE`; `posted_date`, `gl_product`, `responsibility_center`, `cost_center` and `recovered_after` keep their values until the posting story writes them | TSD S7 T3.1; FSD S7 A2.6.3.2 field catalog; ASM-5046 |
| BR8 | The approver is the identity of the approval chain and the limit applied is the matched reference row; neither is a free-text field of the request and neither carries a person name | Legacy AC2; FSD S7 A2.6.3.2; Template and Rules v1 §R7.2 (s17); ASM-5046 |
| BR9 | An act outside the delegation neither approves nor escalates locally: R-WO-15 does not fire, nothing is written and the act is raised, never defaulted | R-WO-15 condition; FSD S7 A2.6.3.1; X4 |
| BR10 | The same request, or the same `Idempotency-Key` twice, writes once, publishes once and answers the case move once | TSD S7 T-A.2; Architecture v5 slide 11 |
| BR11 | No person name, contact value or identity number enters `rwb_writeoff`, the decision record, the event, a log or a workflow input | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it to the case of record (BR4). What this story writes is the WRITEOFF state of the `write_off` row.

| From (WRITEOFF, `write_off.state`) | Event | Condition | To |
|---|---|---|---|
| `WITH_COMMITTEE` | `COMMITTEE_APPROVED` under R-WO-15 | approved inside the delegation | `APPROVED`, with the record reference and the committee date written, the case released to posting and `WriteOffApproved` published |
| `PACK_PREPARED` | `LIMIT_EXCEEDED` under R-WO-12 | amount above the write-off committee limit | `ESCALATED_TO_CREDIT_COMMITTEE`, with the record reference written and the case escalated; no event |
| `WITH_COMMITTEE` | `COMMITTEE_APPROVED` where no delegation row matches | X4 | Unchanged, the act is refused and raised |
| Any state the rule does not name | Any decision | X3 | Unchanged, the 409 is returned |
| `ESCALATED_TO_CREDIT_COMMITTEE` | `CREDIT_COMMITTEE_APPROVED` or `CREDIT_COMMITTEE_REJECTED` under R-WO-13 and R-WO-14 | Approved inside the delegation with Risk, or a decision reason present | `APPROVED` or `RETURNED_TO_PURSUE`: not this story's step (ASM-5044) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | The committee request arrives on API-S7-002 | The package and the delegation row in force are loaded | Evaluating |
| Evaluating | R-WO-15 fires, or R-WO-12 fires instead | The outcome is `APPROVED` or `ESCALATED_TO_CREDIT_COMMITTEE` | Applying |
| Applying | The record, the `write_off` row, the outbox row and the case move are written | The transaction commits | Waiting for the next act |
| Applying | The record write or the transaction fails | X1 | Waiting, nothing changed |

The 27 states of the WRITEOFF machine are those of TSD S7 T4 and of the legacy criteria; `PACK_PREPARED`, `WITH_COMMITTEE`, `APPROVED`, `ESCALATED_TO_CREDIT_COMMITTEE`, `RETURNED_TO_PURSUE`, `DEFERRED` and `POSTED` are the ones this key's stories read or write. No published list of case route states exists for the write-off route, so the case-side values are read from rwb-case on its contract and the story-side values are the WRITEOFF states (ASM-5047).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WOCOMM, write-off committee member | Write-off and posting RA in TSD S7 T6.1 and right A in the legacy table: takes the committee decision on API-S7-002 |
| RW-PRODHEAD, product head | Write-off and posting RA: takes the decision and chairs the credit approval committee the pack escalates to |
| RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: takes the decision as the legacy permission table gives it |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: holds the A right; receives the released case for posting |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the pack and the outcome; holds no A right on this operation |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R: the service identities are subject to the same checks; the act itself is a person's |
| rwb-writeoff service identity | Runs the branch, evaluates the rules, writes the record, the row, the outbox row and the case move; no grant on another schema and no `v_ace_*` grant |

The rights above are the rows of TSD S7 T6.1 and the two rows of the legacy Permission checks table, and nothing wider. The legacy table gives the A right to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE, which the RA and CRUA rows of T6.1 carry; the C right to RW-WRITEOFF and RW-CREDITAD belongs to the scan, which is RWB-S7-E6013-APP's. FSD S7 A2.6.3.3 names "Write-off committee member" as the primary user and "Finance and CFO delegate" as the other user. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the guard of the access service is a service-template capability, so the check is stated here and built by the platform (ASM-5048).

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference of the request, the record and the case move |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case reference the move carries |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Write, the identifier the local decision-record library returns (ASM-5049) |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the value R-WO-15 and R-WO-12 test against the limits, and the value the event carries |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the tax criteria result of RWB-S7-E6014-APP |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Write on the approved path, the committee approval date (ASM-5046) |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: RWB-S7-E6021-APP writes it |
| DF-FIN-017, DF-FIN-018, DF-FIN-019, DF-FIN-020 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product, recovered_after | Not written here: the posting and the post charge-off stories write them |
| Standard columns | write_off (S7, `rwb_writeoff`) | `state`, `version`, `updated_at`, `updated_by`, `created_at`, `created_by`, `is_active` | Write `state`, `updated_at`, `updated_by` and the optimistic lock of `version` on the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, approver, limit applied, inputs reference, outcome, decided at | Write through the local library, before the `write_off` row changes |
| DF-FIN-010 to DF-FIN-020 | outbox event (PLT library, created in `rwb_writeoff`) | writeOffId, caseId, amount, event type, occurred at | Write one row in the same transaction on the approved path; no personal data in the payload |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, status, stage_code and the rest | Not read as a table: the case state arrives on the rwb-case read and the move is answered (GAP-3027) |
| DF-REF-016 to DF-REF-026 | delegation_limit (reference data) | decision_code, approval_level, product_group, principal_limit, loss_pct_limit and 5 more | Not read as a table: the row arrives on the reference-data contract at its version (ASM-5043) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7) | id, case_id, decision_code, rule_id, rule_version, model_version and the rest | Not written here: P7 writes the ledger entry; this service keeps the local record (ASM-5049) |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | rule_id, rule_version, from_state, event_code and the rest | Not read as a table: the rule rows are governed in rwb-decision and loaded here as the package in force |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary v8. **No new table, no new column and no migration**: `write_off` arrives with the DB story of this service, this story writes three of its existing columns, and `decision_record`, `idempotency_key` and `outbox_event` are platform library objects created in `rwb_writeoff` by the library's own migration (DP-03, ASM-5045). The legacy Data table lists four entities; three of them are other services' and are consumed on their contracts as the rows above state.

**No personal data.** The rows this story writes carry identifiers, an amount, a code, a rule version and an approval identity. No name, address, contact value or identity number enters `rwb_writeoff`, the decision record, the event, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/committee-decision` (API-S7-002) | `CommitteeDecision` in, the decision record of status 200 out, carrying the case, the rule `R-WO-15` or `R-WO-12` with its version, the approver, the limit applied and the state `APPROVED` or `ESCALATED_TO_CREDIT_COMMITTEE` | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The operation answers 401, 403 with MSG-P4-002, 404 for a write-off that is not found, 409 for a write-off that has left the state the rule expects, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14 (TSD S7 T-A.2). The request and answer element names the TSD publishes are `CommitteeDecision` and `DecisionLogEntry`; the answer is read as the decision record this service returns, and the name is fixed by the contract baseline (ASM-5042, ASM-5049). The module's other published operation, `POST /write-off-scans` (API-S7-001, right C), belongs to RWB-S7-E6013-APP and is not declared here. The reject and the defer are decisions of the same operation and are RWB-S7-E6019-APP's and RWB-S7-E6020-APP's; this story declares the approve and the escalation outcomes.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the stage the pack belongs to; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3027; ASM-5047)) | rwb-case (P3) | P3 rwb-case | The move `APPROVED` or `ESCALATED_TO_CREDIT_COMMITTEE` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The delegation-limit read (operation name Not specified in the source documents (GAP-3027; ASM-5043)) | `/api/recovery/case/v1` | P3 rwb-case | The `delegation_limit` row of the decision code, the approval level and the product group, with the principal limit, the loss percentage limit and the limit version; faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3027; ASM-5043, ASM-5049)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows R-WO-12 and R-WO-15 with the write-off committee limit; faked |
| The authorise check (operation name Not specified in the source documents (GAP-3027; ASM-5048)) | `/api/recovery/access/v1` | P4 rwb-access | The capability area "Write-off and posting" and the right A for the act, with the scope; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter, a breaker per downstream and no retry of its own (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3027 with ASM-5043, ASM-5047 and ASM-5048.

#### 12.3 Events published

| Event | Name | Topic | Payload | Consumer |
|---|---|---|---|---|
| `WriteOffApproved` (`EV-24`) | `rwb.writeoff.WriteOffApproved.v1` | `rwb.writeoff.events.v1`, with its retry and `.dlt` topics | `writeOffId`, `caseId`, `amount`, the rule ID with its version and the decided-at time; CloudEvents envelope, no personal data | rwb-payment (P8), which posts the write-off, and rwb-reporting (P9) |

The row is written to the outbox in the same `rwb_writeoff` transaction as the state change and relayed after the commit; a failed relay is retried and then sent to the `.dlt` topic (DP-09 as a pattern of the service, recorded as an absent plan row). The event is published only on the approved path: the escalation changes a state and records a decision but approves nothing, so it publishes nothing (ASM-5045).

#### 12.4 Events consumed

None. No source gives rwb-writeoff a consumed event for the committee act: the pack arrives from RWB-S7-E6015-APP inside the same service, the routing from RWB-S7-E6017-APP, the request from the committee on API-S7-002, and the case, the delegation and the package facts arrive on their owners' contracts. This story holds no consumer group, no subscription and no inbox row of its own, and a build that adds one fails the absence test (ASM-5045).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case, the write-off, the amount, the tax criteria flag and the package in force; signals: the committee request, the case state and the delegation row |
| The committee branch of `WriteOffWorkflow` | Workflow branch, the step from the committee request to `APPROVED` or `ESCALATED_TO_CREDIT_COMMITTEE` | `rwb-writeoff` | Applies R-WO-15, or R-WO-12 where the amount is above the limit, writes the record, the row and the outbox row, and reports the stage outcome to the parent |
| `approveWriteOffInLimit` | Activity, the one step of this story | `rwb-writeoff` | The case, the write-off, the delegation row and the package answer in; the rule ID with its version, the approver, the limit applied, the state, the record reference and the case move out, in one transaction |

The committee's act is taken inside the `ApprovalWorkflow` of the workflow kit on the P7 queue, started from the package and the delegation row; this service hosts the decision step, not the approval chain. The activity name is a target design choice of this story and is fixed by no source document.

#### 12.6 Schedules

None. The act is committee-driven on API-S7-002 and owns no Temporal Schedule, no Quartz row and no shared job table. JOB-16, the monthly write-off scan, is RWB-S7-E6013-APP's and is not owned, moved or registered here. The monthly committee meeting the pack was booked into at RWB-S7-E6017-APP has no published calendar and no `write_off` column; the meeting date carried by that story is a parameter, and its source is Not specified in the source documents (GAP-3027; ASM-5051).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story updates `state`, `decision_log_id` and `committee_date` |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the final call, the approver and the limit applied (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the record it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The row of `WriteOffApproved` on the approved path (12.3) |

Not owned and never read as a table: `recovery_case` and `queue` (P3), `delegation_limit` and `rule_row` (reference data and P7), `decision_log_entry` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1). No foreign key leaves the schema and `write_off.case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state fake | The states `WITH_COMMITTEE` and `PACK_PREPARED` of case `RC-2027-000712`; a case in a state the rule does not name | AC2, AC3, X3 |
| rwb-case case-move fake | The moves `APPROVED` and `ESCALATED_TO_CREDIT_COMMITTEE` accepted, and a move refused because the case is not in the state the rule expects | AC2, AC3, X3 |
| rwb-case delegation fake | A `delegation_limit` row with the principal limit and the loss percentage limit above and below the amount, its version, and no row for the decision code | AC1, AC2, AC3, X4 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-12 and R-WO-15 and the write-off committee limit above and below the amount; no answer beyond 2 s | AC1, AC2, AC3, X7 |
| rwb-access authorise fake | The capability area "Write-off and posting" with right A granted, and a role that does not hold it | AC1, X2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off `WO-2027-000318`, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished names of the case move, the delegation read, the package read and the authorise check are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-3027; ASM-5043, ASM-5047, ASM-5048).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) on the write-off base; the case state read, the case-move answer, the delegation read, the package read and the authorise check; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `rwb.writeoff.WriteOffApproved.v1` (`EV-24`) on `rwb.writeoff.events.v1` through the outbox; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity | `WriteOffWorkflow` and its committee branch on `rwb-writeoff`, with its `approveWriteOffInLimit` activity; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the pack documents are rwb-document's (P5) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.writeoff`, module `committee`, Java package `th.co.scb.ace.workbench.recovery.writeoff.committee`; front end `src/modules/recovery/writeoff/WriteOffCommittee.tsx`, the fragment SCR-27 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record of the final call, the approver and the limit applied commits with the `write_off` update or not at all, and the failed write is MSG-P7-003. DP-13 moves the base of API-S7-002 and gives the operation its home. DP-19 is how SCR-27 reaches this service and rwb-case, one hop through the gateway. No other pattern is claimed: the case, the delegation, the package and the access check are consumed contracts, so DP-05, DP-06, DP-07, DP-08, DP-09 and DP-14 stay off this table and their absence from the plan's rows is recorded (GAP-3027; ASM-5043, ASM-5045, ASM-5048).

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows the plan already carries, `RWB-PLT-E1027-CON` and `RWB-PLT-N001-CON`. The five consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs is absent from the H row and is tracked (ASM-5045).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` committee branch | Workflow | Waits for the committee request, loads the package and the delegation row, applies R-WO-15 or R-WO-12 and reports the outcome to the parent |
| `approveWriteOffInLimit` | Activity | The one step: read the case and the write-off, evaluate the rules, write the record, the row and the outbox row and answer the case move |
| `WriteOffCommitteeEvaluator` | Service | The rule evaluation against the WO package version in force and the `delegation_limit` row, with the write-off committee limit, the approval levels and the state list read as package values and reference data |
| `CaseStateClient` | Client | The case state read, the case-move answer and the delegation read of rwb-case; one hop, 2 s, breaker |
| `RulePackageClient` | Client | The WO package version in force of rwb-decision; one hop, 2 s, breaker |
| `AccessCheckClient` | Client | The capability area and right A check of rwb-access; one hop, 2 s, breaker |
| `WriteOffCommitteeDecisionRecordWriter` | Library adapter | Writes the decision record with the rule ID, the version, the approver and the limit applied before any change, hash-linked, and refuses the step when the write fails (DP-03) |
| `WriteOffCommitteeWriter` | Repository | Updates `state`, `decision_log_id` and `committee_date` in one `rwb_writeoff` transaction, with the idempotency row and the optimistic lock |
| `WriteOffOutboxWriter` | Library adapter | Writes the outbox row of `WriteOffApproved` in the same transaction on the approved path |
| `WriteOffCommitteeController` | Controller | API-S7-002, the capability area and right, the scope, the `Idempotency-Key` and the problem mapping of 400, 401, 403, 404, 409, 422 and 503 |
| `WriteOffCommittee` | React component | Shows the pack, the delegation headroom and the outcome on SCR-27, with the refusal, the failed-record and the escalated states |

**Database and migrations.** No Flyway file. `write_off` arrives with the DB story of this service, and the decision record, the idempotency key and the outbox are library objects created in `rwb_writeoff` by the library's migration (DP-03, ASM-5045). No column is added for the approval: `state` is the standard record column of TSD S7 T3.0, and `decision_log_id` (DF-FIN-012) and `committee_date` (DF-FIN-015) exist.

**Configuration and reference data.**

- The write-off committee limit and the state list of the WRITEOFF machine, read as package values at their version, never as constants.
- The delegation limits per decision code, approval level and product group, read as reference data at their version; a missing row is X4 and never a local default (ASM-5043).
- The committee meeting calendar, read as a parameter produced by RWB-S7-E6017-APP; its source is Not specified in the source documents (GAP-3027; ASM-5051).
- The capability area "Write-off and posting" and its rights A, C, R and U are access rows of rwb-access, read through the guard; the 2 s budget and the single hop are the platform rule of ADR-020.
- The feature flag of the step, read from the platform library, never a build constant.

**Build steps**

1. API-S7-002 on the write-off base, with `CommitteeDecision` in, the record out, the rights, the `Idempotency-Key` and the six error answers (AC1, X2, X5, X8).
2. The committee branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the committee request as its signal.
3. `CaseStateClient` against its fake, with the state read, the move answer, the delegation read, the 2 s budget and the no-answer path (AC1, AC2, AC3, X7).
4. `RulePackageClient`, `AccessCheckClient` and `WriteOffCommitteeEvaluator` over the WO package and the delegation row, with R-WO-15, R-WO-12 and the no-row path (AC1, AC2, AC3, X4).
5. `WriteOffCommitteeDecisionRecordWriter` against the library stub, with the failed-write path (AC4, X1).
6. `WriteOffCommitteeWriter` with the one transaction, the three columns, the idempotency row and the optimistic lock (AC2, AC3, X8).
7. `WriteOffOutboxWriter` and the relay test for `WriteOffApproved` (AC2).
8. `CaseMoveAnswer` and the parent signal, with the two moves (AC2, AC3).
9. `WriteOffCommittee` and the screen fragment through the composite route fake (AC1).
10. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or `rwb_access` (X9, BR6).

**Feature flag.** `rwb.writeoff.committee-approval-v1`, read as a flag of the platform library; off means API-S7-002 answers unavailable, the branch holds the committee request, writes nothing and publishes nothing, and the other stories of the service are unaffected.

**Done when.** The tests of section 16 pass, the branch runs from a synthetic committee request in SIT, R-WO-15 and R-WO-12 each produce their record, their state and their answer, `WriteOffApproved` is published once on the approved path, a repeated key writes once, a forced record failure changes nothing, no `recovery_case`, `delegation_limit`, `rule_row` or `decision_log_entry` row and no `v_ace_*` read exists in the build, and SCR-27 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate (R-WO-03) and RWB-S7-E6013-APP's path, so no path of this story raises it (ASM-5050) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of `CommitteeDecision` is absent or invalid (X5), or no delegation row matches (X4) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right A takes or reads the decision (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the `write_off` row changes (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are those of the legacy message set of this key, and the text is the legacy and FSD wording, copied unchanged; no message is reworded or added (FSD S7 A2.6.3.1 and A2.6.4.3).

### 15. Screens and states

SCR-27 Write-off proposal — "the monthly population, the pack per case and removals with reasons", first in E6 (FSD S7 Screens) — is the screen of this step, in its scan, proposed, in-committee and approved states on the legacy screen table. It is served through the gateway-bff composite route (DP-19): the route calls this service for the write-off row, its state and its limit applied, rwb-case for the case and its route state, and rwb-decision for the decision records. This story fixes the write-off answer and the committee fragment; the composite route specification and the screen field list belong to RWB-PLT-N001-CON, and the operation behind the population list is a placeholder (GAP-3027; ASM-5048).

The states this story produces are the in-committee state with its delegation headroom, the approved state with the limit applied and the record, and the escalated state addressed to the credit approval committee. The states it shows are refused with MSG-P4-002, not recorded with MSG-P7-003, refused for a missing delegation row with MSG-GEN-001, and already decided with the 409. The scan, proposed and removed states belong to RWB-S7-E6013-APP, RWB-S7-E6015-APP and RWB-S7-E6016-APP, and the rejected and deferred states to RWB-S7-E6019-APP and RWB-S7-E6020-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-018-01 | AC1 | Component | The committee request on `WO-2027-000318` of case `RC-2027-000712`; the delegation row, the limit applied, the record and the answer asserted on the fakes |
| TC-E6-018-02 | AC2 | Integration | R-WO-15 with the committee limit and the delegation above the amount; the `APPROVED` state, the record with the approver and the limit, the committee date, `WriteOffApproved` and the case move asserted across the rwb-case and rwb-decision fakes |
| TC-E6-018-03 | AC3 | Integration | R-WO-12 with the limit below the amount; the `ESCALATED_TO_CREDIT_COMMITTEE` state, the record and the case move asserted across the rwb-decision and rwb-case fakes, with no event |
| TC-E6-018-04 | AC4 | Component | The decision-record stub stopped; nothing written, no committee date, no outbox row, no move answered and MSG-P7-003 shown |
| TC-E6-018-05 | Access | Component | A role without the Write-off and posting right A; 403 with MSG-P4-002 and no read |
| TC-E6-018-06 | Principle 5 | Component | A forced decision log write failure at the moment of the row update; no column changed, no event published and no move answered |

The six legacy cases are the legacy cases of RWB-E6-018 in their legacy order, with the Level column added: TC-E6-018-01, -04, -05 and -06 map to `Component` because the step is tested on its fakes, and -02 and -03 map to `Integration` because they cross the rwb-case, rwb-decision and outbox boundaries. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the write-off committee limit, the delegation limits and approval levels, the meeting calendar, the state list and the rule rows stay data, reference data or the rule package, never a constant, a default or a branch of the build.
- No personal data in `rwb_writeoff`, in the event, in a workflow input or in a log: identifiers, an amount, a code, a rule version and an approval identity only, and every fixture is synthetic.
- The ACE data only through an owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (DP-01, DP-02).
- The case and its route states stay with rwb-case, the delegation row with its reference-data owner, and the package and the ledger with rwb-decision: no `recovery_case` row, no `delegation_limit` row, no rule row and no ledger entry is written here (BR4, BR5).
- An approval is never derived locally: where no delegation row matches, the act is refused and raised, never defaulted to an approve or an escalation (BR9, X4).
- The scan, the pack, the removal, the routing, the reject and the defer stay with their own stories of this service: this step declares no operation, no event and no rule of theirs.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no second event on the topic and no approval or queue table of this service's own.
- The decision is recorded before the change and the record, the update and the outbox row commit together; a build that writes the row first fails the review (DP-03).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (Must, E6); this story records the approve and the escalation, and the reject and the defer are RWB-S7-E6019-APP's and RWB-S7-E6020-APP's | The committee branch, the decision record and the state | TC-E6-018-01, TC-E6-018-02, TC-E6-018-03 |
| REQ-S7-004 | The write-off exception loop has one named owner and a time limit (Must, E6); not this step, and the retry-limit path R-WO-24 stays with the posting story | None in this story | Not tested here |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off row and its committee state | TC-E6-018-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-018-06 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | `WriteOffApproved` written to the outbox in the same transaction | TC-E6-018-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget | TC-E6-018-02, TC-E6-018-03 |
| ADR-022 | Local decision record plus central ledger | The record of the final call, the approver and the limit applied, with the ledger entry in P7 | TC-E6-018-04, TC-E6-018-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-018, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by this story |
| Test cases | TC-E6-018-01 to TC-E6-018-06 |
| Feature and screens | FEAT-WOF-06, SCR-27 Write-off proposal |
| Rules | R-WO-15 and R-WO-12, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the `write_off` element, of `CommitteeDecision` and the record, the state vocabulary, the consumed rows, the rights, the error set and the fakes: RWB-S7-E6018-CON.
- The monthly eligibility scan, the tax criteria and JOB-16: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The pack, its documents, its carried provision and its check: RWB-S7-E6015-APP. The removal by the team: RWB-S7-E6016-APP. The routing to the committee queue and its meeting booking: RWB-S7-E6017-APP.
- The reject and the defer, R-WO-16, R-WO-17 and R-WO-18: RWB-S7-E6019-APP and RWB-S7-E6020-APP.
- The credit approval committee's own approve and reject out of `ESCALATED_TO_CREDIT_COMMITTEE`, R-WO-13 and R-WO-14: claimed by no story of this key and recorded as open (ASM-5044).
- The posting to ALS and the general ledger, the provision release, the retry and the exception path R-WO-24, and the settlement of the escalated pack: RWB-S7-E6021-APP and the posting stories of this key.
- The case of record, its route states and the case-move operation name: rwb-case (P3), whose state and move answers this story consumes and fakes (GAP-3027).
- The `delegation_limit` table and its versions, and reference data at large: the reference-data owner of rwb-case under the default ruling, whose row this story consumes and fakes (GAP-3027; ASM-5043).
- The WO rule package, its version, the approval chain and the ledger: rwb-decision (P7) (ASM-5049). The capability area and the guard: rwb-access (P4) (ASM-5048).
- The pack documents and their custody: rwb-document (P5); the notices to customers: rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories (ASM-5048).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

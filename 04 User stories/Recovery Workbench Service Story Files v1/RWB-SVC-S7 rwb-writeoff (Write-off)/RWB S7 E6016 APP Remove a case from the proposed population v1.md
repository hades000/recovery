# RWB-S7-E6016-APP Remove a case from the proposed population

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S7-D |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6016-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the removal slice of RWB-E6-016 in rwb-writeoff. The three legacy criteria are kept word for word with their origin tag; the step evaluates R-WO-07 (with R-WO-08 as the exit of the state it writes), records the decision through the local decision-record library before any change (DP-03), answers rwb-case for the move `CASE_REMOVED_BY_TEAM` with the reason, and serves the removal of a proposed case on base `/api/recovery/writeoff/v1` (DP-13), reached from SCR-27 through the gateway-bff composite route (DP-19). No source publishes a removal operation: TSD S7 T-A.1 lists only `POST /write-off-scans` and `POST /write-offs/{writeOffId}/committee-decision`, and the legacy Endpoints table repeats those same two rows for every S7 story, so the removal operation is this baseline's one new operation and it carries a placeholder path (GAP-3023; ASM-5028). `removal_reason` appears in no field list, no column and no list of values (ASM-5030), the population state lives on the case and not on `write_off` (ASM-5031), and the split plan carries no requirement id for the slice (ASM-5032). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **write-off team member (RW-WRITEOFF)**, I want **the Workbench to let the write-off team take a case out of the proposed population before committee, with a reason**, so that **write-offs follow the criteria and the committee's decision**.

This is the removal slice of legacy RWB-E6-016. It owns:

- the three legacy criteria this story owns (AC1, AC2, AC3), copied verbatim with their origin tag, and the rule, message and screen they depend on;
- one step of `WriteOffWorkflow` on task queue `rwb-writeoff` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` and as the step that runs between the scan and the pack (Temporal and Drools Design slide 5, S7 "monthly scan, posting"; slide 13);
- the evaluation of R-WO-07 against the WO package version in force, from `POPULATION_PROPOSED` on `TEAM_REMOVED_CASE` with `removal_reason` present (FSD S7 A2.4.3.1; Business Rules and Routing Logic v4);
- the local decision record of the removal, written through RWB-PLT-E1027-CON before any change (DP-03), with the rule ID, the package version, the case reference, the reason and the case move;
- the answer to rwb-case for `CASE_REMOVED_BY_TEAM`, with the reason the rule records, so that the case of record moves and no pack is built for it;
- the removal operation of a proposed case on base `/api/recovery/writeoff/v1` and the removal state of SCR-27 Write-off proposal behind the gateway-bff composite route (DP-13, DP-19).

It does not own: the published shape of the removal operation, the `RemovalRequest` and `WriteOffRemoval` elements, the reason field, the consumed rows, the error set and the fakes, which are RWB-S7-E6016-CON; the monthly scan and the population of R-WO-01 (RWB-S7-E6013-APP), the tax criteria (RWB-S7-E6014-APP) and the pack of R-WO-05 (RWB-S7-E6015-APP); the deviation hold of R-WO-06 and the committee routing of R-WO-11, which are RWB-S7-E6017-APP's; the approve, reject and defer decisions (RWB-S7-E6018-APP to RWB-S7-E6020-APP) and the posting with `WriteOffApproved` (RWB-S7-E6021-APP); the case of record, its route states and the parent `CaseWorkflow`, which are rwb-case (P3); the ACE data products and the ALS and GL extracts, which are rwb-source-data's (P1); the WO package and its 51 rules, which are rwb-decision's (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: the team takes a case out of the proposed population before committee with a reason, because write-off populations are assembled by hand each month (FSD S7 A1.3, A2.4.1), and the packs accepted first time are measured on the decision log and the Workbench records against a target that rises each month, reviewed monthly (FSD S7 A2.4.1). What D-RCV-60 changes is who owns the population, the case, the package and the screen.

- **The removal is this service's step.** `write_off` is S7's only table in `rwb_writeoff` (context pack, ownership rows owned by S7; TSD S7 T3.1), and the WO route set of 51 rules over 27 states is the write-off stage's (TSD S7 T4); the removal is a transition of that stage and runs here.
- **The case stays with rwb-case.** `recovery_case`, the route state `POPULATION_PROPOSED` and the state the removal writes, `CASE_REMOVED_BY_TEAM`, are P3's; this step evaluates the rule, records the decision and **answers** the case move (ASM-5029).
- **The package is read, not embedded.** The WO route set is governed in rwb-decision, and DP-04 is not in this key's pattern set, so the package arrives on its read with the version in force and the version is recorded with the outcome (ASM-5005).
- **The decision is recorded first**, in the call that answers the move, which is what legacy AC1 asked for and legacy AC3 tested; a removal with no record is no removal.
- **The reason is the condition.** R-WO-07 fires only where `removal_reason` is present, and the FSD's own validation row names no other condition (FSD S7 A2.4.3.1); the reason is therefore the one input this step validates, and no source gives it a column, a field ID or a list of values (ASM-5030).
- **The removal is not the deviation hold.** R-WO-06 removes a case because a deviation is open (`deviation_open in (X1 to X7)`) and routes it to the deviation handler; that row belongs to RWB-S7-E6017-APP's AC3, and this step neither tests nor writes it (ASM-5033).
- **The removal is reversible by rule.** R-WO-08 returns a `CASE_REMOVED_BY_TEAM` case to `SCAN_DUE` once the reason is resolved, and this story writes the state R-WO-08 leaves; the clearing step itself is claimed by no story of this split (GAP-3023; ASM-5031).

No business value moves: the reason, the from and to states, the rule ID and the package version are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S7-E6016-CON is published: the removal operation, the `RemovalRequest` and `WriteOffRemoval` elements, the reason field with its placeholder, the consumed rows, the case-move answer, the `Idempotency-Key` rule, the error set and the fakes are baselined and handed to this story.
- The rwb-case read of the proposed population is published with its fake: the case reference, the case number, the product group, the stage and the state `POPULATION_PROPOSED`. The operation name is Not specified in the source documents (GAP-3023; ASM-5029).
- The case-move answer of rwb-case is available for the fake: the move `CASE_REMOVED_BY_TEAM` with the reason and the rule version. No source names a published operation that moves a case state on behalf of a stage; on the workflow boundary the answer is the stage outcome the parent `CaseWorkflow` applies (GAP-3023; ASM-5029).
- The rwb-decision rule-package read is published with its fake and answers the WO package at its version in force, with R-WO-07 and R-WO-08 among its 51 rules over 27 states (GAP-3023; ASM-5005).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so no move is answered and nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-27 reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `write_off` exists in schema `rwb_writeoff` from the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020 and the standard record columns of TSD S7 T3.0; this story adds no table, no column and no migration.
- The WO package is in force at its version and is read on its package read; the rule rows, the removal reason and the states are governed in rwb-decision and are not a build item of this story.
- The service runs as its own login on schema `rwb_writeoff`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S7-E6016-CON when its tests pass.

### 4. Flow

1. The monthly scan of R-WO-01 has proposed the population and the case sits at `POPULATION_PROPOSED`; that scan, its tax criteria and its ALS and GL extracts are RWB-S7-E6013-APP's and RWB-S7-E6014-APP's, and this story reads its outcome only (FSD S7 A2.1; TSD S7 T4).
2. The write-off team member opens SCR-27 Write-off proposal through the gateway-bff composite route and reads the proposed population of the cut-off date, one hop (DP-19).
3. The member selects one case and gives the removal reason. The reason is the only input this step requires; the screen sends the case reference, the reason, the member's identity and an `Idempotency-Key`.
4. The removal step of `WriteOffWorkflow` on queue `rwb-writeoff` receives the request as a signal to the running stage, with the case reference, the reason and the package version read from rwb-decision in force (DP-12; ASM-5005).
5. The step reads the case on the rwb-case contract: the case reference, its product group, its stage and its state. A case that is not at `POPULATION_PROPOSED` is refused with 409 and nothing is written (ASM-5029).
6. `RemovalEvaluator` evaluates R-WO-07: from `POPULATION_PROPOSED`, on `TEAM_REMOVED_CASE`, where `removal_reason` is present, the action is "Remove the case from the proposed population with the reason recorded" and the state is `CASE_REMOVED_BY_TEAM`. Where the reason is absent, no rule fires and the caller sees MSG-GEN-001 (FSD S7 A2.4.3.1; Business Rules and Routing Logic v4).
7. The evaluation answers the rule ID, the package version, the action of the rule, the recorded reason and the case move the rule names.
8. `WriteOffDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the rule ID `R-WO-07` with its package version, the reason, the from state, the to state and the decided-at time. A failed write stops the step with nothing changed (DP-03; legacy AC1 and AC3).
9. `CaseMoveAnswer` answers rwb-case with the move `CASE_REMOVED_BY_TEAM`, the reason and the rule version. rwb-case writes the `recovery_case` row and the state; this service writes neither the row nor the state, and the population of the next scan is P3's fact (ASM-5029).
10. No pack is built for a removed case: R-WO-05 of RWB-S7-E6015-APP reads the population, and a case at `CASE_REMOVED_BY_TEAM` is not in it.
11. A repeated request with the same `Idempotency-Key` answers the removal it created, writes no second record and sends no second answer; a removal of a case already removed answers 409 with no change.
12. SCR-27 shows the case in its removal state — the case reference, the reason and the removal time — from this service and the case state of rwb-case, read only, next to the population of the cut-off date (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no move is answered, the case stays at `POPULATION_PROPOSED` and no record exists | MSG-P7-003 | AC3, TC-E6-016-03, TC-E6-016-05 |
| X2 | The role does not hold the Write-off and posting right C | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E6-016-04 |
| X3 | The reason is absent or blank | 422 and nothing is recorded; the case is not removed | MSG-GEN-001 | AC2, X6 |
| X4 | The case is not at `POPULATION_PROPOSED`, or has already been removed | 409 and nothing is written for that case; a case that has moved is not removed twice | None | AC2, X3 |
| X5 | The rwb-case or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written and no move is answered; the caller sees 503 with the platform error envelope | None | AC1, X2 |
| X6 | The case carries an open deviation | R-WO-06 is not this story's rule; a deviation removal is RWB-S7-E6017-APP's AC3 and this step writes no removal for it | MSG-GEN-001 | AC2 |
| X7 | A repeated `Idempotency-Key`, or the same case removed twice | One record and one answer; the repeat answers the removal that exists and is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR6 |

X1 to X4 are the legacy exception paths carried onto the slice, X5 to X7 are the paths the target call types and the interactive trigger add, and X8 is the ACE and schema boundary. The deviation codes X1 to X7 of R-WO-06 are codes of the rule package and are not the path identifiers of this table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S7-E6016-CON, the rwb-case and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live P1, P3 or P7 |
| Negotiable | The activity name, the decision code of R-WO-07 and the shape of the stage outcome are this story's choice; the rule, the messages, the screen, the operation and the two states are fixed |
| Valuable | A case leaves the proposed population with a reason recorded and the case moves in the service that owns it, so the committee sees only the population the team stands behind |
| Estimable | One workflow step, one evaluator, one record write, one case-move answer, one operation, three clients and one read-only screen fragment |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic proposed population through the contract fakes, plus the access, missing-reason and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Remove a case from the proposed population

  Background:
    Given case "RC-2026-000716" is one of 120 cases in state "POPULATION_PROPOSED" on the population of the monthly write-off scan
    Given the WO rule package is in force at its version and carries R-WO-07
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Remove a case from the proposed population (legacy RWB-E6-016 AC1)
    Given the rwb-case contract mock returns the population of the cut-off date with "RC-2026-000716" in state "POPULATION_PROPOSED"
    Given the rwb-decision contract mock returns the WO package at its version in force with R-WO-07
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then lets the write-off team take a case out of the population before committee, with a reason
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-07 (legacy RWB-E6-016 AC2)
    Given the rwb-case contract mock returns the case state "POPULATION_PROPOSED" for "RC-2026-000716" and accepts the move "CASE_REMOVED_BY_TEAM"
    Given a case in state POPULATION_PROPOSED
    When team removed case
    Then remove the case from the proposed population with the reason recorded
    Then the case moves to CASE_REMOVED_BY_TEAM

  Scenario: AC3 Not recorded (legacy RWB-E6-016 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The three criteria are the legacy criteria of RWB-E6-016 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `the user acts on the screen`, `team removed case`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service parts are mocked, so AC1 and AC2 each carry `Given the <service> contract mock returns <x>` lines, and those are the only additions. What the legacy lines describe happens in three places now: rwb-case answers the population and writes the move, rwb-decision holds the package at its version, and this story evaluates R-WO-07, writes the record and answers the move. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_writeoff`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-WO-07 | Write-off | D9 | POPULATION_PROPOSED | TEAM_REMOVED_CASE | removal_reason present | Remove the case from the proposed population with the reason recorded | CASE_REMOVED_BY_TEAM | Write-off team | Case Workspace, Decision Log | None |

The row is the row of the Business Rules and Routing Logic v4, copied character for character. Its owner and systems columns name a business role and systems, not services: in the target the "Case Workspace" is the case of rwb-case and its route state, the "Decision Log" is the local record of DP-03 in `rwb_writeoff` with the rwb-decision ledger behind it, and the "Write-off team" holds the Write-off and posting right C. R-WO-08, the row that returns a removed case to `SCAN_DUE`, is not tabled here because it is not the removal: this story writes the state R-WO-08 leaves (ASM-5031).

| ID | Rule | Source |
|---|---|---|
| BR1 | The removal is a transition of the write-off stage: it runs in `WriteOffWorkflow` on `rwb-writeoff` and writes no column of `write_off` | TSD S7 T3.1, T4; context pack ownership rows (table and workflow); FSD S7 A2.4.2 |
| BR2 | The decision is recorded before the case moves, with the rule ID, the package version, the reason and the two states; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S7 T2 ("writes the decision log entry before any change"); legacy AC1 and AC3 |
| BR3 | Only a case at `POPULATION_PROPOSED` is removed, and only with a reason: another state is refused, and a reason that is present is the whole condition of the rule | Business Rules and Routing Logic v4 row R-WO-07; FSD S7 A2.4.3.1 |
| BR4 | The removal is answered, not written: `recovery_case` and every route state are rwb-case's, and this service answers `CASE_REMOVED_BY_TEAM` with the rule and its version | ASM-5029; TSD S7 T4 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_writeoff`; `case_id` and `decision_log_id` are identifiers of another service's fact | DP-01; TSD S7 T3.3 |
| BR6 | ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and the ALS and GL facts are the scan's | DP-05 as a prohibition; FSD S7 A1.1; TSD S7 T1 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: R-WO-07, its states, the reason and the package version | FSD S7 BR-S7-004; legacy Guardrails |
| BR8 | The same request twice, or the same `Idempotency-Key` twice, writes one record and sends one answer; a case already removed is refused with 409 | TSD S7 T-A.2 |
| BR9 | No person name, address, contact value or identity number enters `rwb_writeoff`, the decision record, a log or a workflow input; the case reference is a number and not an identity | Template and Rules §R7.2 (s17); TSD S7 T6.2 |

### 9. State transitions

The case route state is rwb-case's and is not changed by this story: the step answers the move and the parent `CaseWorkflow` applies it (BR4). What this story owns is the step and the record; the states it writes are the ones of the WO machine.

| From (case state, rwb-case) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `POPULATION_PROPOSED` | `TEAM_REMOVED_CASE` | `removal_reason` present | `CASE_REMOVED_BY_TEAM` | rwb-case, on this story's answer |
| `POPULATION_PROPOSED` | `TEAM_REMOVED_CASE` | `removal_reason` absent | Unchanged | none; MSG-GEN-001 |
| `POPULATION_PROPOSED` | `TEAM_REMOVED_CASE` | The case is not at `POPULATION_PROPOSED` | Unchanged | none; 409 |
| `CASE_REMOVED_BY_TEAM` | `REMOVAL_CLEARED` | The reason is resolved | `SCAN_DUE` | rwb-case, on the clearing path that no story of this split claims (R-WO-08) |
| `CASE_REMOVED_BY_TEAM` | The pack step of R-WO-05 | The case is removed | No pack is built | RWB-S7-E6015-APP reads the population |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A removal request for a case of the population | The package in force is read | Evaluating |
| Evaluating | R-WO-07 fires | The reason is present and the case is at `POPULATION_PROPOSED` | Recording |
| Evaluating | R-WO-07 does not fire | The reason is absent, or the state is not the rule's | Waiting, nothing changed |
| Recording | The record is written and the answer sent | The transaction commits | Waiting for the next request |
| Recording | The record write fails | X1 | Waiting, nothing changed |

The states `POPULATION_PROPOSED`, `CASE_REMOVED_BY_TEAM` and `SCAN_DUE` are those of the WO machine of TSD S7 T4 and live on the case of record; this step writes none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-WRITEOFF, write-off team member | Write-off and posting CRU in TSD S7 T6.1: the primary role, removing a case from the proposed population and reading the removal state |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: removes a case and reads the record |
| RW-WOCOMM, write-off committee member; RW-PRODHEAD, product head; RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: read the removal state and the reason, and act on the committee path of the later stories |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE | Write-off and posting R: read only, in scope |
| SY-CASEWF, SY-RULES, SY-AGENT, SY-DATALOAD | Write-off and posting R or U as the matrix gives it: the service identities run the step and are subject to the same checks |
| rwb-writeoff service identity | Evaluates the rule, writes the record, answers the move and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S7 T6.1 and nothing wider, and the right this story needs is C — the right the legacy permission table gives to RW-WRITEOFF and RW-CREDITAD for a change of the population, not the A of the committee decision. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 | write_off (S7, `rwb_writeoff`) | id | Read, the write-off reference of the case where the scan has created the row |
| DF-FIN-011 | write_off (S7, `rwb_writeoff`) | case_id | Read, the case of the proposal |
| DF-FIN-012 | write_off (S7, `rwb_writeoff`) | decision_log_id | Read, the record reference the scan set |
| DF-FIN-013 | write_off (S7, `rwb_writeoff`) | amount | Read, the amount the population carries; not changed by a removal |
| DF-FIN-014 | write_off (S7, `rwb_writeoff`) | tax_criteria_met | Read, the result RWB-S7-E6014-APP wrote |
| DF-FIN-015 | write_off (S7, `rwb_writeoff`) | committee_date | Not written here: RWB-S7-E6018-APP |
| DF-FIN-016 | write_off (S7, `rwb_writeoff`) | posted_date | Not written here: RWB-S7-E6021-APP |
| DF-FIN-017 to DF-FIN-019 | write_off (S7, `rwb_writeoff`) | responsibility_center, cost_center, gl_product | Not written here: RWB-S7-E6021-APP |
| DF-FIN-020 | write_off (S7, `rwb_writeoff`) | recovered_after | Not written here: the recovery stories |
| Standard columns | write_off (S7, `rwb_writeoff`) | `is_active`, `state`, `version`, `created_at`, `created_by`, `updated_at`, `updated_by` | Write, the optimistic lock and the audit columns of the row this step reads |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_writeoff`) | rule id, rule version, inputs reference, reason, from and to state, decided at | Write through the local library, before the case moves |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the population and the state arrive on the rwb-case contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the rule arrives on the package read |
| `removal_reason` | the removal reason of R-WO-07 | Read as a request input and recorded in the decision record; the field, its column, its list and its owner are Not specified in the source documents (GAP-3023; ASM-5030) |

Field IDs are those of TSD S7 T3.1 and the Logical Data Model and Data Dictionary, and the case, ledger and rule rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, this story reads its columns and writes none of them, and `decision_record` and `idempotency_key` are library objects created in `rwb_writeoff` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, amounts, dates, list values, a reason, a rule version and a state. No name, address, contact value or identity number enters `rwb_writeoff`, the record, a log or a workflow input, and the fixtures are synthetic. The reason is free text a staff member writes; it is reviewed for personal data before it is stored, and `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This story supplies the behaviour behind the removal of a proposed case, whose shape RWB-S7-E6016-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/removal` (proposed path; no source names this operation — GAP-3023; ASM-5028) | `RemovalRequest` in with the reason, `WriteOffRemoval` out with the case, the reason, the rule `R-WO-07` and its version and the state `CASE_REMOVED_BY_TEAM` | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a case that is not in the population, 409 for a case that has left `POPULATION_PROPOSED`, 422 with MSG-GEN-001 for a missing reason and 503 when the library or a consumed contract does not answer. TSD S7 T-A.1 publishes only two operations for the module — `POST /write-off-scans` (API-S7-001, right C) and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) — and the legacy Endpoints table of RWB-E6-016 repeats those same two rows for the removal, so the removal operation is the one operation this baseline adds and it carries a placeholder path, a proposed request element and the declared rights (GAP-3023; ASM-5028). The scan is RWB-S7-E6013-APP's and the committee decision is RWB-S7-E6018-APP's; neither is built or declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The read of the proposed population (operation name Not specified in the source documents (GAP-3023; ASM-5029)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the cases at `POPULATION_PROPOSED`; read only, faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3023; ASM-5029)) | rwb-case (P3) | P3 rwb-case | The move `CASE_REMOVED_BY_TEAM` with the reason and the rule version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3023; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-07 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan does not carry, because this story's C row is None; the absence is recorded (GAP-3023; ASM-5029, ASM-5005).

#### 12.3 Events published

None. The service publishes on `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, with `writeOffId`, `caseId` and `amount`, consumed by Posting), and that event belongs to the posting step of R-WO-20 and R-WO-21, which is RWB-S7-E6021-APP's. A removal approves nothing, posts nothing and changes no amount, so this story declares no event, no producer group and no outbox row, and a build that publishes one fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry for this key (ASM-5031).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7: REST and events to P1, Temporal and events to P8), and none belongs to the removal: a removal reads no ACE extract and moves no money. This story therefore holds no consumer group, no subscription and no inbox row, and a build that adds one fails the absence test. The trigger of the step is the officer's request on SCR-27 through the composite route, and the FSD declares no background event for the feature beyond the monthly scan of R-WO-01 (FSD S7 A2.4.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` in namespace `rwb-recovery` | Input: the case reference, the cut-off date and the package in force; signals: the removal request and the population answered by rwb-case; outcome for the parent: the case move |
| `removeCaseFromPopulation` | Activity, the one removal step | `rwb-writeoff` | The case reference, the reason and the package version in; the rule ID with its version, the reason recorded and the case move out, with the record written before the answer |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document; the step runs from the officer's request, and the monthly scan is the Schedule of RWB-S7-E6013-APP (§12.6).

#### 12.6 Schedules

None. The removal is an officer-driven step and owns no Temporal Schedule. `JOB-16`, the write-off scan job of the context pack and TSD S7, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and nothing of it is built or declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; this story reads the row of the proposal and writes none of its columns |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the removal (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case population fake | The population of the cut-off date with 120 cases at `POPULATION_PROPOSED`, `RC-2026-000716` among them; a case that has moved; a case that is not in the population | AC1, AC2, X3, X4 |
| rwb-case case-move fake | The move `CASE_REMOVED_BY_TEAM` accepted for `RC-2026-000716` with the reason and the rule version; a move refused because the case is not in the expected state | AC2, X4 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-07 and R-WO-08 among its 51 rules over 27 states | AC1, AC2 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC3, X1 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000716`, in its removal state | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the population read, the case-move answer and the package read carry the placeholder until their owners confirm them (GAP-3023; ASM-5029, ASM-5005).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The removal operation on `/api/recovery/writeoff/v1`; the population read, the case-move answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (`EV-24`) belongs to RWB-S7-E6021-APP and no event is consumed here (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `WriteOffWorkflow` and its removal step on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.writeoff`, module `population`; front end `src/modules/recovery/writeoff/WriteOffProposal.tsx`, the fragment SCR-27 embeds, read only for this story's state.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the answer commit together or not at all. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the removal operation its home. DP-19 is how SCR-27 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-09 (the outbox and inbox library) and DP-05 (the ACE read) are real dependencies of the stage that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3023; ASM-5005, ASM-5031).

**Dependencies the tables add and the plan does not hold.** The three consumed rows are class C dependencies in fact and the plan's C row is None, so the story builds against their documents and fakes on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `WriteOffWorkflow` removal branch | Workflow | Receives the removal signal on the running stage, reads the package in force and reports the outcome to the parent |
| `removeCaseFromPopulation` | Activity | Reads the case, evaluates R-WO-07, writes the record, sends the answer |
| `RemovalEvaluator` | Service | The rule evaluation over the package in force, with the reason test, the state test and the no-fire path |
| `WriteOffDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the version before any change, hash-linked; refuses the step when the write fails |
| `RemoveCaseController` | Controller | The removal operation, the capability area and right C, the `Idempotency-Key` and the problem mapping |
| `CasePopulationClient` | Client | The population and case read of rwb-case, one hop, 2 s, breaker, no retry of its own |
| `RulePackageClient` | Client | The WO package read of rwb-decision at its version in force |
| `CaseMoveAnswer` | Client | The `CASE_REMOVED_BY_TEAM` answer with the reason and the rule version |
| `WriteOffProposal` | React component | Shows the population and the removal state with its reason on SCR-27, read only |

**Database and migrations.** No Flyway file. The `write_off` table arrives with the DB story of this service, and the record and idempotency key are library objects created in `rwb_writeoff` by the library's migration (DP-03). No column is added for the reason, the case state or the rule row: the reason is a decision-record input with a placeholder, and the state and the rule row are facts and rows of their owners (ASM-5030).

**Configuration and reference data.**

- R-WO-07, its from and to states and the reason condition: rule rows of the WO package with their version, never written in code (ASM-5005).
- The reason itself: a free-text value with no list of values in any source, validated as present and stored with the record (ASM-5030).
- The capability area "Write-off and posting" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the removal has no timer.

**Build steps**

1. The removal branch of `WriteOffWorkflow` and its input record, registered on `rwb-writeoff` as the stage child of `CaseWorkflow`, with the officer's request as its signal.
2. `CasePopulationClient` against its fake, with the 2 s budget, the breaker, the out-of-population path and the moved-case path (AC1, AC2, X4, X5).
3. `RulePackageClient` against its fake, with the version in force recorded with the outcome (AC1).
4. `RemovalEvaluator` over the package, with R-WO-07, the reason test and the no-fire path (AC1, AC2, X3).
5. `WriteOffDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC3, X1).
6. `CaseMoveAnswer` with the `CASE_REMOVED_BY_TEAM` move and the reason (AC2, X4).
7. `RemoveCaseController` with the rights, the `Idempotency-Key` and the problem mapping of the declared errors, and `WriteOffProposal` on SCR-27 through the composite route fake (AC1, X2, X7).
8. The boundary test: no statement outside `rwb_writeoff`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or any other schema (X8, BR5, BR6).

**Feature flag.** `rwb.writeoff.removal-v1`, a flag of the platform library; off means the removal operation answers 503 with no write and SCR-27 hides the action, and the scan, the pack and the committee stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic population in SIT, R-WO-07 removes a case with its reason recorded, a missing reason and a moved case are refused, a repeated key writes once, a forced record failure changes nothing, no `recovery_case` row and no `v_ace_*` read exists in the build, and SCR-27 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of RWB-E6-016: the scan is held for an absent tax criteria version (R-WO-03), so no population exists and no case can be removed. Raised by RWB-S7-E6013-APP, not by this step | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | The reason is absent or blank, or a required element of the request is invalid (X3) | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right C calls the removal (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case moves (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. MSG-S7-001 is kept because the legacy table of RWB-E6-016 lists it and because it is the only reason a proposed case is not there to remove; it is not raised by this step, whose own validation is the presence of the reason.

### 15. Screens and states

SCR-27 Write-off proposal, in its loading state and its removal state, is served through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the population, the removal state and the reason, and rwb-case for the case and its route state; this story fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved". This story produces the removal state, read from "proposed": a case removed while the screen is in its proposed state shows the removal, its reason and its time, and is no longer part of the pack population. The scan state is RWB-S7-E6013-APP's, the in-committee state RWB-S7-E6017-APP's and the approved state RWB-S7-E6018-APP's. The refusal, missing-reason and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-016-01 | AC1 | Component | The 120-case population on the fake with `RC-2026-000716` at `POPULATION_PROPOSED`; the record, the answer and the removal state asserted |
| TC-E6-016-02 | AC2 | Component | `RC-2026-000716` at `POPULATION_PROPOSED` with a reason; the `CASE_REMOVED_BY_TEAM` answer with the reason asserted on the case-move fake |
| TC-E6-016-03 | AC3 | Component | The decision-record stub stopped; nothing written, no answer sent and MSG-P7-003 shown |
| TC-E6-016-04 | Access | Component | A role without the Write-off and posting right C; 403 with MSG-P4-002 and no read |
| TC-E6-016-05 | Principle 5 | Component | A forced decision log write failure inside the transaction; the case stays at `POPULATION_PROPOSED` and no record exists |

The five legacy cases are those of RWB-E6-016 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: R-WO-07, its states, the reason condition, the package version and the capability rights stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_writeoff`, in a workflow input or in a log: identifiers, amounts, dates, states, a reason and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table, and a build that adds one fails the boundary test (BR6).
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here (BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `recovery_log` write.
- The decision is recorded before the change; a build that answers the move outside the record's transaction fails the review (DP-03).
- The reason is stored as staff-entered text: it is screened for personal data before it is written, and no identity value is ever copied into the record.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-3023; ASM-5032) | The eight REQ-S7 rows of FSD S7 cover eligibility, the pack, the committee decision, the exception loop, posting, post charge-off treatment, recoveries and closure; none covers a removal from the proposed population, and the split plan carries no requirement id for this slice | The removal step, the record and the case-move answer | TC-E6-016-01, TC-E6-016-02, TC-E6-016-03, TC-E6-016-05 |
| ADR-013 | 19 services inside ACE | rwb-writeoff as the owner of the write-off stage | TC-E6-016-01 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-E6-016-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-E6-016-01, TC-E6-016-02 |
| ADR-022 | Local decision record plus central ledger | The record written before the case moves | TC-E6-016-03, TC-E6-016-05 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-016, disposition Split (rework); feature FEAT-WOF-04 |
| Legacy criteria | AC1, AC2 and AC3, owned word for word by this story; the deviation hold of R-WO-06 is RWB-S7-E6017-APP's AC3 |
| Source text | Legacy RWB-E6-016; FSD S7 Write-off and recovery v3 A2.4 and Screens; TSD S7 Write-off and recovery v2 T2, T3, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-07 and R-WO-08 |
| Test cases | TC-E6-016-01 to TC-E6-016-05 |
| Feature and screens | FEAT-WOF-04, SCR-27 Write-off proposal |
| Rules | R-WO-07, with R-WO-08 as the exit of its state, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shape of the removal operation, the `RemovalRequest` and `WriteOffRemoval` elements, the reason field, the consumed rows, the error set and the fakes: RWB-S7-E6016-CON.
- The monthly scan, the population of R-WO-01, the ALS and GL extracts and the Schedule of `JOB-16`: RWB-S7-E6013-APP.
- The tax criteria and the scan hold of R-WO-02 to R-WO-04: RWB-S7-E6014-APP.
- The pack of R-WO-05: RWB-S7-E6015-APP. The deviation hold of R-WO-06 and the committee routing of R-WO-11: RWB-S7-E6017-APP.
- The approve, reject and defer decisions of R-WO-12 to R-WO-19: RWB-S7-E6018-APP to RWB-S7-E6020-APP.
- The posting, `WriteOffApproved` (`EV-24`), the provision release and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The clearing path of R-WO-08 as a step: no story of this split claims it, and only the state it leaves is written here (ASM-5031).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3); the ACE data products: rwb-source-data (P1); the WO package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

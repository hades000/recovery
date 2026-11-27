# RWB-S7-E6016-CON Remove a case from the proposed population - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- Start rule: `WriteOffWorkflow` waits for `AceDataReady` with `sourceSystem` `ALS` and `status` `COMPLETED` (RD-P1-040); event record key and payload per RD-P1-003.

| Item | Value |
|---|---|
| Story key | RWB-S7-E6016-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6016-CON-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | `rwb-case` (P3, `/api/recovery/case/v1`, two operations in 12.2); `rwb-decision` (P7, `/api/recovery/decision/v1`, one operation in 12.2) |
| Contract version | v1, the `/v1` base of the operations in 12.1 and 12.2 |
| Readiness decisions | RD-P1-003, RD-P1-040 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the removal step of rwb-writeoff, split from RWB-E6-016. It fixes the removal operation on `/api/recovery/writeoff/v1` (DP-13) — an operation no source publishes, carried with a placeholder path and a proposed element set — the `RemovalRequest` and `WriteOffRemoval` elements over the fields DF-FIN-010 to DF-FIN-020, the reason as free text with no list of values because TSD S7 T3.2 is empty, the consumed rows of the rwb-case population and case-move answer and the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S7 T6.1, the fakes and the absence tests. DP-04 and DP-09 are not in the plan's pattern set although the stage evaluates a package and the service owns a topic, and the three consumed rows are absent from the plan's None C row. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6016-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 16 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the removal step of rwb-writeoff — the removal operation on `/api/recovery/writeoff/v1`, the removal and write-off elements with their required flags, the reason field, the three consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a reason rule, a consumed row or an answer shape can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy removal of RWB-E6-016 crossed three boundaries at once: the case of record, the rule version and a screen, and its Endpoints table named only the scan and the committee decision, because the monolith served the removal through the case workspace with no published contract of its own. The target splits them: rwb-case owns the case and its route states, rwb-decision owns the WO package, and rwb-writeoff owns the write-off stage, its record and the removal of a proposed case. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition.

Four points are carried as gaps and assumptions rather than decided quietly: no source publishes a removal operation, so the baseline adds one with a placeholder path (ASM-5028); `removal_reason` has no column, no field ID and no list of values, and TSD S7 T3.2 publishes no list at all (ASM-5030); the plan's C row is None while the step consumes three rows, and DP-04 and DP-09 are absent from the pattern set (ASM-5029, ASM-5005, ASM-5031); and the split plan carries no requirement id for the slice (ASM-5032).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case population row and case-move answer and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3024; ASM-5029, ASM-5005).
- The removal operation itself has no owner document: TSD S7 T-A.1 publishes API-S7-001 and API-S7-002 only, and the legacy Endpoints table of RWB-E6-016 repeats those two rows. The baseline therefore declares one new operation with a placeholder path, and the placeholder stands until the solution architect confirms the path (GAP-3024; ASM-5028).
- The WO package and its rows for R-WO-07 and R-WO-08 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration. `removal_reason` has no column in it (ASM-5030).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step: the removal operation with its request and answer elements, the rights and the error responses.
2. Fix the `WriteOffRemoval` element over the write-off columns of DF-FIN-010 to DF-FIN-020, and the `RemovalRequest` element with the case reference, the reason and the request reference.
3. Fix the consumed rows: the population and case read of rwb-case, the case-move answer of rwb-case and the package read of rwb-decision with its version, marking with the placeholder what the sources do not give.
4. Record the decision-record element of DP-03, written before the case moves.
5. Record the rights of the operation, the naming baseline and the rule that no value is a constant of the code; record that the service publishes no list of values because TSD S7 T3.2 is empty and the reason is free text.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
8. Tag the baseline and hand it to RWB-S7-E6016-APP, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | The reason is declared as an enumeration or a closed list | The vocabulary test fails the build: no list of values exists in TSD S7 T3.2, so the reason is free text | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC7 |
| X7 | The document declares an event published by this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S7 T6.1 gives the capability area for a change | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The operation path, the element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the base, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6016-APP, SCR-27 and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, five fakes and eleven contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the removal step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The removal operation is declared on the write-off base with its shape and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-offs/{writeOffId}/removal with a RemovalRequest body in and a WriteOffRemoval answer of status 200, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then the operation declares the path parameter writeOffId, the Idempotency-Key header and the repeated key answering the removal it created
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then the path and the element names carry the placeholder Not specified in the source documents (GAP-3024; ASM-5028) until the solution architect confirms them
    Then no operation of the scan or of the committee decision is declared by this document

  Scenario: AC2 The write-off and removal elements and the free-text reason are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S7 T3.1 and T3.2
    Then the WriteOffRemoval element declares the write-off properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then it declares the removal properties: the case reference, the reason, the rule ID R-WO-07 with its rule version, the from state POPULATION_PROPOSED, the to state CASE_REMOVED_BY_TEAM and the decided-at time
    Then the RemovalRequest element declares the case reference and the reason as required, and the reason as a free-text string of unstated length
    Then the reason declares no enumeration and the document publishes no list of values, because TSD S7 T3.2 lists none and the legacy field lists none
    Then committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after are optional and owned by RWB-S7-E6018-APP and RWB-S7-E6021-APP
    Then no property is added for a deviation, an open deviation code, an ACE extract or a ledger row

  Scenario: AC3 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the population read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the stage and the case state
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move CASE_REMOVED_BY_TEAM carrying the reason, the rule ID and its version
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version and its 51 rules over 27 states
    Then the operation names of the three rows are Not specified in the source documents (GAP-3024; ASM-5029, ASM-5005) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no rule_row property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T-A.1 and T6.1
    Then the removal declares Write-off and posting right C with the scope applied, because a removal changes the population and is not the A of the committee decision
    Then RW-WRITEOFF holds CRU and RW-CREDITAD holds CRUA on the capability area, and they are the two roles the right C names
    Then RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA and read the removal state and the reason without the right C
    Then every other role and every SY-* service identity of TSD S7 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and written before the case moves (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema and with TSD S7 T2
    Then one decision record is declared per rule outcome with the case reference, the rule ID R-WO-07, the package version in force, the reason, the from state, the to state and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the case-move answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the record carries no rule row, no state threshold as a literal and no personal data

  Scenario: AC6 The five fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case population fake answers the population of the cut-off date with 120 cases at POPULATION_PROPOSED, a case that has moved and a case that is not in the population
    Then the rwb-case case-move fake answers CASE_REMOVED_BY_TEAM accepted and refused
    Then the rwb-decision fake answers the WO package at its version with R-WO-07 and R-WO-08
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer in its removal state
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names WriteOffApproved (EV-24) as RWB-S7-E6021-APP's and JOB-16 as RWB-S7-E6013-APP's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule or a v_ace_* read (ASM-5031)
```

These seven criteria and AC8 are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6016-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The removal is a case move before committee: no amount is approved, no provision is released and no posting is declared here (ASM-5033).

Scenario: AC8 Every rule of section 8 has a criterion, a guardrail or a boundary test (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The removal is rwb-writeoff's, and the contract declares the fields and the required flags on the `WriteOffRemoval` element and on the `RemovalRequest` element only | TSD S7 T3.1; context pack ownership rows (table `write_off`) |
| BR2 | The decision record is declared as an element written before the case moves, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC3 |
| BR3 | The case stays with rwb-case: the contract declares the population read and the case-move answer as consumed, declares no `recovery_case` property and describes no case row write | ASM-5029; TSD S7 T4 |
| BR4 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule version as a property | DP-05 as a prohibition for ACE data; ASM-5005 |
| BR5 | No event of this step is declared: `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5031; TSD S7 T5.3 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer | TSD S7 T-A.2 |
| BR7 | The reason is declared as free-text `removal_reason` with no enumeration, because TSD S7 T3.2 publishes no list of values and no legacy field list names one | ASM-5030; FSD S7 A2.4.3.1, A2.4.3.2 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, a reason and a rule version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The operation path and the two element names are placeholders fixed by this baseline, not copied from a source, because no source publishes a removal operation | GAP-3024; ASM-5028 |
| BR13 | The rights of the removal are the capability area's change right: C, held by RW-WRITEOFF and RW-CREDITAD, and not the A of the committee decision | TSD S7 T6.1; legacy permission table of RWB-E6-016 |
| BR14 | The states `POPULATION_PROPOSED` and `CASE_REMOVED_BY_TEAM` are declared as the vocabulary of the answer and of rwb-case's machine, and move no case | ASM-5031; TSD S7 T4; Business Rules and Routing Logic v4 row R-WO-07 |
| BR15 | Each error answer of the removal operation is bound to one message id of section 14, and the path and the two element names are confirmed before the tag | GAP-3024; ASM-5028 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the reason rule, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the wave 4 harness and the owners of rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | The path is confirmed | The solution architect replaces the placeholder path with the confirmed one inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reference or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the reason becomes an enumeration | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `POPULATION_PROPOSED` and `CASE_REMOVED_BY_TEAM` are route states of rwb-case (TSD S7 T4), and `SCAN_DUE` is the state R-WO-08 leaves. This baseline fixes the vocabulary and the answer shape and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves the placeholder path and elements of the removal operation, a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the three consumed rows and the absent DP-04 and DP-09 rows |
| Consuming teams (the app story, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| rwb-access service owner | Owns the rwb-access authorise check that the removal operation calls for the rights in BR13 (DP-08) |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product` and `recovered_after` |
| Removal element | The case reference, `removal_reason`, the rule ID `R-WO-07`, the rule version, the from state `POPULATION_PROPOSED`, the to state `CASE_REMOVED_BY_TEAM` and the decided-at time |
| Required flags | The case reference and the reason required on the request; `id`, `case_id`, `amount` and `tax_criteria_met` required on the write-off element; the other properties optional |
| Lists | None: TSD S7 T3.2 publishes no list of values, so the baseline declares no enumeration, and the reason is free text (ASM-5030) |
| Event data | None of this step: no event is declared (§12.3) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the case moves (DP-03) |
| Case and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3 and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) |
| Consumed fields with no source | The operation names of the population read, the case-move answer and the package read, the length of `removal_reason` and the path of the removal operation: Not specified in the source documents (GAP-3024; ASM-5028, ASM-5029, ASM-5030, ASM-5005) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the reason rule of AC2 and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story. None of the nine rows above carries a BR Field ID: `removal_reason` is not a field or entity in Logical Data Model v9 or Data Classification v5, so its field ID is Not specified in the source documents (DOR-RWB-S7-E6016-CON-7; ASM-5030).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/removal` (proposed path; no source names it) | `RemovalRequest` in, `WriteOffRemoval` of status 200 out, carrying the case, the reason, the rule `R-WO-07` with its version and the state `CASE_REMOVED_BY_TEAM` | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The operation answers 400, 401, 403 with MSG-P4-002, 404 for a case that is not in the population, 409 for a case that has left `POPULATION_PROPOSED`, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The path and the two element names carry the placeholder until the solution architect confirms them (GAP-3024; ASM-5028). The module's two published operations, `POST /write-off-scans` (API-S7-001, right C) and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A), belong to RWB-S7-E6013-APP and RWB-S7-E6018-APP and are not declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of the proposed population (operation name Not specified in the source documents (GAP-3024; ASM-5029)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the cases at `POPULATION_PROPOSED`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3024; ASM-5029)) | rwb-case (P3) | P3 rwb-case | The move `CASE_REMOVED_BY_TEAM` with the reason, the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3024; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-07 and R-WO-08 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3024; ASM-5029, ASM-5005).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, `writeOffId`, `caseId`, `amount`, consumed by Posting), which belongs to the posting step of R-WO-20 and R-WO-21, declared by RWB-S7-E6021-APP. A removal approves nothing, posts nothing and changes no amount, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that relays the event is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5031).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7), not in the removal: a removal reads no ACE extract and moves no money. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one. The trigger of the step is the officer's request on SCR-27 through the composite route, because the FSD declares no background event for the feature beyond the monthly scan (FSD S7 A2.4.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end; workflow ID form: Not specified in the source documents (CG-ALL-10934); start rule: JOB-16 on the third working day after AceDataReady with `sourceSystem` `ALS` and `status` `COMPLETED` (R-WO-01); duplicate-start policy: Not specified in the source documents (CG-ALL-10934) | `rwb-writeoff` | The stage that hosts the removal step; its signals and its outcome for the parent are declared, not built |
| `removeCaseFromPopulation` | Activity, the one removal step | `rwb-writeoff` | The case reference, the reason and the package version in; the rule ID with its version, the reason recorded and the case move out |

No child workflow for the case and none for the money exists in this service. The activity name is a target design choice, and the step runs from the officer's request. No activity is registered by this story.

#### 12.6 Schedules

None. The removal is an officer-driven step; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. `JOB-16`, the write-off scan, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP and is named here only as another story's.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its fields and its dates; the table the answer element is drawn from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the removal (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case population fake | The population of the cut-off date with 120 cases at `POPULATION_PROPOSED`, `RC-2026-000716` among them; a case that has moved; a case that is not in the population | AC1, AC3, AC6 |
| rwb-case case-move fake | The move `CASE_REMOVED_BY_TEAM` accepted with the reason and the rule version, and a move refused | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-07 and R-WO-08 among its 51 rules over 27 states | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000716`, in its removal state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the population read, the case-move answer and the package read carry the placeholder until their owners confirm them (GAP-3024; ASM-5029, ASM-5005).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 3 consumed | The removal operation on `/api/recovery/writeoff/v1`; the population read, the case-move answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the decision record is the library's on `rwb.decision-record.v1` and not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 0 registered | `WriteOffWorkflow` and `removeCaseFromPopulation` on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no amount and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the case moves. DP-13 moves the base of the legacy paths and gives the removal operation its home. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-05 and DP-09 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE extract as another service's data and never a view, and the outbox as an absent library row rather than an event of this step (GAP-3024; ASM-5005, ASM-5031).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, and the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule evaluation would add; no story file of key `RWB-P7-E1073-CON` exists, so it is not held as a dependency. The three consumed rows are C dependencies in fact and are named in the contract dependencies row of the header.

**Deliverables and build steps**

1. Write the removal operation and validate the additive rule of AC1 in the pipeline.
2. Write the `WriteOffRemoval` and `RemovalRequest` elements, their required flags and the free-text reason of AC2, with the placeholder where a type or a length is unstated.
3. Record the population row, the case-move row and the package row of AC3 with their owner, their budget and their placeholders.
4. Record the rights and the error envelope of AC4.
5. Record the decision-record element of AC5 and validate it against the library schema.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the two elements, the contract README rows for the three consumed rows and their placeholders, and the five fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eleven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The contract describes the held-scan state from which no case can be removed (R-WO-03), raised by RWB-S7-E6013-APP and not by this operation | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, the reason among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right C the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case moves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its loading and removal states through the gateway-bff composite route (DP-19). Screen Specifications v1 gives SCR-27 no empty, error or no-access state, so those states are Not specified in the source documents (CG-ALL-10939); the loading state is served as written here. The route calls rwb-writeoff for the population, the removal state and the reason, rwb-case for the case and its route state, and rwb-document for the pack per case; this baseline fixes the rwb-writeoff answers only, the owner of the screen is Not specified in the source documents (GAP-1814), and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved": the removal state is this step's reading of "proposed", the scan state belongs to RWB-S7-E6013-APP, the in-committee state to RWB-S7-E6017-APP and the approved state to RWB-S7-E6018-APP. The refusal, missing-reason and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-016-01 | AC1, AC3, BR4 | Contract | The 120-case population on the fake; the contract half answers the removal operation, the population row and the package row |
| TC-E6-016-02 | AC2, AC3, BR14 | Contract | `RC-2026-000716` at `POPULATION_PROPOSED`; the contract half answers the two elements and the `CASE_REMOVED_BY_TEAM` move shape |
| TC-E6-016-03 | AC5, AC7, BR2 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-E6-016-04 | AC4, BR13 | Contract | A role without the right C and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E6-016-05 | AC4, AC5, BR13 | Contract | RW-WRITEOFF holds CRU and RW-CREDITAD holds CRUA; the contract half answers the rights and the decision element |
| TC-S7-E6016-CON-01 | AC1, BR6, BR12 | Contract | The document validates; the operation, the base, the `Idempotency-Key` and the seven error answers are present |
| TC-S7-E6016-CON-02 | AC2, BR1, BR7 | Contract | The `WriteOffRemoval` element validates with its eleven write-off properties, its six removal properties, the required flags and the free-text reason |
| TC-S7-E6016-CON-03 | AC3, AC4, BR3, BR4, BR11 | Contract | The three consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case` and no-rule-row boundary; the rights |
| TC-S7-E6016-CON-04 | AC5, AC6, BR2, BR8 | Contract | The decision-record element matches the library schema; the five fakes match the document and a drifted fake fails the build |
| TC-S7-E6016-CON-05 | AC7, BR5, BR9 | Contract | The naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a Schedule |
| TC-S7-E6016-CON-06 | AC7 | Contract | The four tables of section 12.7 and their boundary: only the owned tables are declared, no foreign key leaves the schema, and no row is declared in `outbox_event` (ASM-3438) |
| TC-S7-E6016-CON-07 | AC1, BR10 | Contract | An additive field within major version 1 passes; a breaking change without a new major version fails the build |
| TC-S7-E6016-CON-08 | AC8, BR15 | Contract | Not specified in the source documents (NEWAC-RWB-S7-E6016-CON-AC8) |

The five legacy cases are those of RWB-E6-016 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6016-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The eight cases `TC-S7-E6016-CON-01` to `-08` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: R-WO-07, its states, the reason rule and the package version stay rule rows and reference data, never a schema default, an enumeration member or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, a reason and a rule version only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `recovery_case` property, no case row write and no case state write (BR3).
- ACE data stays with rwb-source-data: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read.
- The money stays with rwb-payment and the ledger with rwb-decision: the document declares no posting, no proceeds and no rule row.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a Quartz row.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-3024; ASM-5032) | The eight REQ-S7 rows of FSD S7 cover eligibility, the pack, the committee decision, the exception loop, posting, post charge-off treatment, recoveries and closure; none covers a removal, and the split plan carries no requirement id for this slice | The removal operation, the two elements and the three consumed rows | TC-E6-016-01, TC-E6-016-02, TC-S7-E6016-CON-01, TC-S7-E6016-CON-02, TC-S7-E6016-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6016-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S7-E6016-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed rows with their budget and breaker | TC-S7-E6016-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6016-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-016, disposition Split (rework); feature FEAT-WOF-04 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S7-E6016-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-016; FSD S7 Write-off and recovery v3 A2.4, A2.4.2, A2.4.3 and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 row R-WO-07 |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S7-E6016-CON-01 to -05 |
| Feature and screens | FEAT-WOF-04, SCR-27 Write-off proposal |
| Rules | R-WO-07, governed in rwb-decision; R-WO-08 named as the exit of its state |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the removal operation, the evaluation of R-WO-07, the decision record and the case-move answer: RWB-S7-E6016-APP.
- The case of record, its route states, the population and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5029).
- The authoring, testing, approval and versioning of the WO package and of the rule rows: rwb-decision (P7) (ASM-5005).
- The search for a published removal operation: none exists in TSD S7 T-A.1 or in the legacy Endpoints table, and the placeholder path is confirmed by the solution architect at the baseline review (ASM-5028).
- The column, list and owner of `removal_reason`: no source names them (ASM-5030).
- The monthly scan, the tax criteria and the pack: RWB-S7-E6013-APP to RWB-S7-E6015-APP. The deviation hold and the committee routing: RWB-S7-E6017-APP.
- The approve, reject and defer decisions: RWB-S7-E6018-APP to RWB-S7-E6020-APP. The posting, `WriteOffApproved` (`EV-24`) and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

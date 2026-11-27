# RWB-S7-E6024-CON Work the write-off exception loop - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Start rule of `WriteOffWorkflow` / JOB-16: only the `AceDataReady` event with `sourceSystem` ALS and `status` COMPLETED counts; the event is published once per source system and business date (RD-P1-003, RD-P1-040).

| Item | Value |
|---|---|
| Story key | RWB-S7-E6024-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S7-E6024-CON-16); the squad sizes it at refinement |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (base /api/recovery/writeoff/v1; openapi/rwb-writeoff-v1.yaml) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-003, RD-P1-040 |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the write-off exception loop of rwb-writeoff, split from RWB-E6-024. It fixes the one correction operation on `/api/recovery/writeoff/v1` (DP-13), the `CorrectionRequest` and `WriteOffCorrection` elements, the `WriteOff` element with the field IDs DF-FIN-010 to DF-FIN-020 and their required list, the consumed rows of the rwb-case case read, case-move answer and correction task, the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S7 T6.1, the fakes and the absence tests. No source publishes a correction operation, the loop's owner or its time limit; TSD S7 T3.2 publishes no list of values and the service owns no exception table. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S7-E6024-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (14 resolved, 10 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the write-off exception loop of rwb-writeoff — the correction operation on `/api/recovery/writeoff/v1`, the request and answer elements, the `WriteOff` element, the four consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27, the case workspace and the wave 4 harness build against one fixed, testable contract on Day 1, and a property, a consumed row or a correction code can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy exception loop of RWB-E6-024 crossed four boundaries at once: the case state, the task and its assignment, the rule package with its retry limit, and a screen. The target splits them: rwb-case owns the case, its route states, the task and the assignment, rwb-decision owns the WO package and the retry limit, and rwb-writeoff owns the write-off row, the raise and the correction. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the properties of the correction request and answer, the eleven properties of `WriteOff` with their required list, the three case rows, the package row and the record of the decision.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition and the case facts are consumed on the owner's contract only.

Three points are carried as gaps and assumptions rather than decided quietly: no source publishes a correction operation or its elements, while TSD S7 T-A.1 publishes two operations for the module and the legacy Endpoints table repeats them for every S7 story (ASM-5092); the loop's owner and its service level, which REQ-S7-004 demands, are unconfirmed in the routing logic (ASM-5093); and the correction vocabulary is the rule event column of the state, because no list of values publishes one (ASM-5094).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `write_off` is S7's, `recovery_case`, `task` and `assignment` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-case case row, case-move answer and task row and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3040).
- The human-task template of the workflow kit is the platform dependency of the correction task and its service level; the plan's H row for this key does not carry it (ASM-5093).
- The outbox and inbox library of DP-09 is the platform dependency of the service's topic; this story declares no event and the plan's H row does not carry the library.
- The WO package and its rows for R-WO-24 and R-WO-44 to R-WO-46, with the retry limit among its facts, are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step: the correction operation with its request and answer elements, its rights and its error responses.
2. Fix the `CorrectionRequest` element: the correction taken from the three rule events of the exit, and the optional `correctionReason`, with the requiredness the sources do not give.
3. Fix the `WriteOffCorrection` element: the write-off, the case, the correction, the rule ID with its version, the from state `WRITEOFF_EXCEPTION`, the to state and the decided-at time.
4. Fix the `WriteOff` element: the eleven properties of DF-FIN-010 to DF-FIN-020, their types, their lengths and the required list API Specification v5 publishes.
5. Fix the consumed rows: the case read, the case-move answer and the correction task of rwb-case, and the package read of rwb-decision, marking with the placeholder what the sources do not give.
6. Record the decision-record element of DP-03, written before the row and the answer change.
7. Record the rights of the operation, the naming baseline, the task's timer and the rule that no value is a constant of the code.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case`, `task` or `assignment` write, the drift between a fake and the document, and the absence of a published event.
10. Tag the baseline and hand it to RWB-S7-E6024-APP, SCR-27, the case workspace and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A property is declared that the sources do not publish, for example a retry-count column, an exception table or a correction list of values | The review fails the baseline and the absence test fails the build | None | AC2, AC5, AC7 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case`, `task` or `assignment` row, or a rule row | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares an event of this step or a second topic | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones the legacy permission table and TSD S7 T6.1 declare | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6024-APP, SCR-27, the case workspace and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the write-off exception loop of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case, task and assignment is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The correction operation is declared on the write-off base with its shape and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-offs/{writeOffId}/correction-decision with a CorrectionRequest body in and a WriteOffCorrection answer of status 200, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then the operation declares the path parameter writeOffId, the Idempotency-Key header and the repeated key answering the decision it created
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then the path and the two element names carry the placeholder Not specified in the source documents (GAP-3040; ASM-5092) until the solution architect confirms them
    Then no operation of the scan or of the committee decision is declared by this document

  Scenario: AC2 The correction, write-off and decision elements are fixed and no vocabulary is invented (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with API Specification v5, TSD S7 T3.1 and T3.2 and the event column of the routing logic
    Then the CorrectionRequest element declares correction as required and correctionReason as optional, and nothing else
    Then the correction enumeration is the three rule events of the state, CORRECTION_REPOST, CORRECTION_RETURN_TO_SCAN and CORRECTION_REFER_TO_COMMITTEE, copied character for character and named as the only vocabulary the sources give (ASM-5094)
    Then correctionReason is a free-text string of unstated length with no enumeration
    Then the WriteOffCorrection element declares the write-off reference, the case reference, the correction, the rule ID with its rule version, the from state WRITEOFF_EXCEPTION, the to state and the decided-at time
    Then the WriteOff element declares the eleven properties of DF-FIN-010 to DF-FIN-020 with the required list of API Specification v5: id, caseId, amount, taxCriteriaMet and recoveredAfter
    Then responsibilityCenter, costCenter and glProduct keep their maximum length of 10
    Then the document declares no property for a retry count, a retry limit, an exception row, an owner or a service level, and no table of values beyond the three rule events

  Scenario: AC3 The consumed rows of rwb-case are declared and the case, the task and the assignment stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack and the LDM work-management rows
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the write-off reference, the stage and the case state POSTING_REJECTED
    Then the case-move answer is declared as consumed from P3 rwb-case, with the moves WRITEOFF_EXCEPTION, POSTING_PENDING, SCAN_DUE and WITH_COMMITTEE carrying the rule ID and its version
    Then the correction task is declared as consumed from P3 rwb-case, with the owner, the queue, the service level, the task identity and its outcome, and assignment remains P3's (DF-WRK-009 to DF-WRK-016)
    Then the operation names of the three rows and the queue code are Not specified in the source documents (GAP-3040; ASM-5096) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case, task or assignment property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The package row, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-decision as the owner of the rule rows and with the legacy permission table and TSD S7 T6.1
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version, its 51 rules over 27 states, R-WO-24 and R-WO-44 to R-WO-46 among them and the retry limit among its facts, and its operation name is Not specified in the source documents (GAP-3040; ASM-5095)
    Then the document declares no rule row, no retry limit and no threshold as a property, and both are read from the package
    Then the correction declares the capability area Write-off and posting with right A and the scope applied, because a correction is a decision on the write-off and takes the A the legacy table gives to RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE (ASM-5092)
    Then RW-WRITEOFF and RW-CREDITAD hold the right C of the loop and every other role and every SY-* service identity of TSD S7 T6.1 holds R
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC5 The decision-record element is declared and the exception state has no table of its own (new, D-RCV-60)
    Given the decision and data sections of the baseline
    When they are compared with the library schema, TSD S7 T3.1 and the ownership rows of S7
    Then one decision record is declared per raise and per correction, with the case reference, the write-off reference, the rule ID, the package version in force, the retry count and the limit in force as inputs, the correction where there is one, the from and to states and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the row state and the answer change, and a failed write leaves them unchanged with MSG-P7-003
    Then the record carries no rule row, no limit as a literal, no actor name and no personal data
    Then the state column of write_off is declared as carrying WRITEOFF_EXCEPTION and the state the correction names, because no list of values publishes a write-off state vocabulary (ASM-5094)
    Then the document declares no table of this service beyond write_off, decision_record, idempotency_key and outbox_event, and no exception table, task table or assignment table

  Scenario: AC6 The six fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers the case with write-off "WO-2026-000311" in POSTING_REJECTED, a case in WRITEOFF_EXCEPTION and a case that has left the stage
    Then the rwb-case case-move fake answers the four moves accepted and one refused, and the task fake answers an accepted raise with its owner and service level, a refused assignment and an unreadable answer
    Then the rwb-decision fake answers the WO package at its version with R-WO-24, R-WO-44 to R-WO-46 and the retry limit
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer in its exception state
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the trigger and the boundary are fixed and no event is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, task, assignment, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and are consumed only through their contracts
    Then the trigger is declared as the posting step of WriteOffWorkflow and the correction task's timer, and nothing is registered by this story
    Then the document declares no event published by this step and no second topic, and it names WriteOffApproved (EV-24) as the approval story's
    Then the absence test fails a build that adds a published event, a second topic, a registered Schedule, a v_ace_* read, an exception table or a retry-count column (ASM-5095)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6024-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The loop's owner and time limit that REQ-S7-004 requires are not declared as properties: they are reference and rule values named in §12.6 and carried as unconfirmed (ASM-5093).

Scenario: AC8 Each business rule BR1 to BR13 of section 8 is covered by a criterion and a test case row, and a rule that is an architecture constraint is proved by a guardrail or boundary test (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The exception state of the write-off is rwb-writeoff's, and the contract declares the fields, the required list and the optionality of the `WriteOff` element only | TSD S7 T3.1; API Specification v5, `WriteOff`; context pack ownership row (table `write_off`) | AC2 (TC-S7-E6024-CON-02) |
| BR2 | The decision record is declared as an element written before the row and the answer change, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC3 | AC5 (TC-S7-E6024-CON-04) |
| BR3 | The ACE data and the ALS posting stay with rwb-source-data and the posting story: the contract declares no `v_ace_*` property and no posting path read | DP-05 as a prohibition; FSD S7 A2.12.2; ASM-5095 | AC3 (TC-S7-E6024-CON-03) |
| BR4 | The case, the route states, the task and the assignment are consumed and not written: the contract declares the three rows and declares no `recovery_case`, `task` or `assignment` property and no case row write | ASM-5096; TSD S7 T4; LDM v8 `assignment` | AC3 (TC-S7-E6024-CON-03) |
| BR5 | No event of this step is declared: `WriteOffApproved` (EV-24) is the approval story's, and the outbox and inbox library of DP-09 is recorded as an absent H row | Context pack ownership rows (event EV-24); TSD S7 T5.3 | AC7 (TC-S7-E6024-CON-05) |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; no other operation is declared on this base by this story | Platform API rule (ADR-020); TSD S7 T-A.2 | AC1 (TC-S7-E6024-CON-01) |
| BR7 | The correction vocabulary is the event column of the three exit rules and nothing else; no list of values is published for this module | BRRL v4 rows R-WO-44 to R-WO-46; TSD S7 T3.2 (empty); ASM-5094 | AC2 (TC-S7-E6024-CON-02) |
| BR8 | No personal data in a schema, an example or a fake: identifiers, an amount, dates, a state, a retry count and a rule version only | Template and Rules §R7.2 (s17); TSD S7 T6.2 | AC6 (TC-S7-E6024-CON-04) |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 | AC7 (TC-S7-E6024-CON-05) |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) | AC1 (TC-S7-E6024-CON-01) |
| BR11 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 | AC6 (TC-S7-E6024-CON-04) |
| BR12 | The rule rows of R-WO-24 and R-WO-44 to R-WO-46, the retry limit, the loop's owner and the task's service level are governed in rwb-decision and in reference data and are named here, never declared here | BRRL v4; FSD S7 A2.12.3.1; ASM-5093, ASM-5095 | AC3 (TC-S7-E6024-CON-03) |
| BR13 | The trigger is declared and not registered: the posting step and the correction task's timer are named as the loop's trigger, and this story creates neither | TSD S7 T4; ASM-5093 | AC7 (TC-S7-E6024-CON-05) |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the three elements, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the case workspace, the wave 4 harness and the owners of rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional answer field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, the required list changes, or a correction code is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC5 and AC7 fail: an exception table, a retry-count column, a `v_ace_*` view, a `recovery_case` property or a published event | In review |

The state machine the document describes is the app story's and rwb-case's: `POSTING_REJECTED`, `WRITEOFF_EXCEPTION`, `POSTING_PENDING`, `SCAN_DUE` and `WITH_COMMITTEE` are route states of rwb-case (TSD S7 T4; BRRL v4, States sheet). This baseline fixes the vocabulary of the request and the answer and moves no case and no row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves the proposed path and element names, a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the four consumed rows and the unconfirmed owner and service level |
| Consuming teams (the app story, SCR-27, the case workspace, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the outbox library and the human-task template this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

Each POST is authorised through the rwb-access check of DP-08 for the rights in the table above; the check's name and its request shape are Not specified in the source documents (DOR-RWB-S7-E6024-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Request element | `correction` required, enumerated as the three rule events of the exit, and `correctionReason` optional free text; no property list is published in any source (ASM-5092, ASM-5094) | BR7 |
| Answer element | The write-off reference, the case reference, the correction, the rule ID with its rule version, the from state `WRITEOFF_EXCEPTION`, the to state and the decided-at time | BR6 |
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `caseId`, `decisionLogId`, `amount`, `taxCriteriaMet`, `committeeDate`, `postedDate`, `responsibilityCenter`, `costCenter`, `glProduct` and `recoveredAfter` | BR1 |
| Required list | `id`, `caseId`, `amount`, `taxCriteriaMet` and `recoveredAfter`, as API Specification v5 publishes them; this baseline copies them and adds no required property to the two new elements | BR1 |
| Lengths | `responsibilityCenter`, `costCenter` and `glProduct` at a maximum length of 10, as the source gives them | BR1 |
| Lists | The three correction events only; no other enumeration, because TSD S7 T3.2 publishes no list of values for this module (ASM-5094) | BR7 |
| Event data | None of this step: no event is declared (§12.3) | BR5 |
| Correction operation | One correction operation on the write-off base (BR6); its path segment is Not specified in the source documents (GAP-3039), and its request and answer elements are the placeholders above | BR6, BR7 |
| Retry count and limit | The retry count and the retry limit are Not specified in the source documents (GAP-3040); the limit is governed in rwb-decision and reference data (BR12), and no retry-count column is added | BR12 |
| Reference data | The owner and service level of the correction task, and the retry limit, are read from reference data under DP-06 and DP-07; the parameter names are Not specified in the source documents (DOR-RWB-S7-E6024-CON-20) | BR12 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row and the answer change (DP-03) | BR2 |
| Case, task and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case`, DF-WRK-009 to DF-WRK-016 of `assignment` in P3, and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | BR4 |
| Not declared here | `recovery_case`, `task` and `assignment` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `proceeds` (P8), an exception table, a retry-count column and the later stories' data | BR3, BR4, BR12 |

The field-level types of the two added elements are settled in the baseline review; this story fixes the property names, the required list and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/correction-decision` (proposed path; no source names this operation - GAP-3040; ASM-5092) | `CorrectionRequest` in, `WriteOffCorrection` of status 200 out, the write-off, the case, the correction, the rule ID with its version and the from and to states | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The operation declares 400, 401, 403 with MSG-P4-002, 404, 409 for a write-off that is not in `WRITEOFF_EXCEPTION`, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. TSD S7 T-A.1 publishes only `POST /write-off-scans` (API-S7-001, right C) and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, process answer `DecisionLogEntry`, right A), and the legacy Endpoints table of RWB-E6-024 repeats those two rows, so the correction is the one operation this baseline adds and its path and element names carry the placeholder (GAP-3040; ASM-5092).

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of a write-off case (operation name Not specified in the source documents (GAP-3040; ASM-5096)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, write-off reference, stage and state `POSTING_REJECTED`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3040; ASM-5096)) | rwb-case (P3) | P3 rwb-case | The moves `WRITEOFF_EXCEPTION`, `POSTING_PENDING`, `SCAN_DUE` and `WITH_COMMITTEE` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The correction task raise and its answer (operation names and queue code Not specified in the source documents (GAP-3040; ASM-5093, ASM-5096)) | `/api/recovery/case/v1` | P3 rwb-case | The human task with its owner, its queue, its service level, its identity and its outcome; the `assignment` row stays P3's; faked |
| The WO rule-package read in force (operation name Not specified in the source documents (GAP-3040; ASM-5095)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-24 and R-WO-44 to R-WO-46 among its 51 rules over 27 states and the retry limit among its facts; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3040).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (event `EV-24`, `writeOffId`, `caseId`, `amount`, consumed by posting), which the approval story RWB-S7-E6018-APP publishes when the committee approves; the exception raises nothing. This baseline therefore declares no event published by this step, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that will relay EV-24 is the platform library object of DP-09, which the pattern set for this key does not carry.

#### 12.4 Events consumed

None of this step's own. The loop is started by the posting step of the same `WriteOffWorkflow`, not by an event; the connection matrix gives row S7 a subscription to rwb-payment and one to rwb-source-data, and both belong to the post-charge-off recovery story RWB-S7-E6027-APP (`ProceedsMatched`, `EV-25`, and the ACE data-ready fact, `EV-26`). Where a retry count is later published by its owner, the inbox of DP-09 receives it and that library is the recorded missing H row. This baseline declares a subscription of no kind.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case in the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end; started by JOB-16 on the third working day after AceDataReady (R-WO-01) (counted only for the event with `sourceSystem` = `ALS` and `status` = `COMPLETED`, RD-P1-040); workflow ID form and duplicate-start policy Not specified in the source documents (CG-ALL-11150) | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the raise and the correction; its input, its signals and its outcome for the parent are declared, not built |
| `raiseWriteOffException` | Activity, the raise | `rwb-writeoff` | The case, the write-off, the retry count and the package version in; the rule ID with its version, the row state and the case move out |
| `recordCorrection` | Activity, the working of the loop | `rwb-writeoff` | The correction, the rule ID of the chosen exit with its version and the actor in; the record, the row state and the case move out |

No child workflow for the case and none for the money exists in this service, and the correction task is the workflow kit's human-task template. The activity names are a target design choice. No workflow and no activity is registered by this story.

#### 12.6 Schedules

None registered. The loop is not a schedule: it is started by the posting step of `WriteOffWorkflow` and worked by a person, and the legacy JOB-16 scan and its Temporal Schedule stay RWB-S7-E6013-APP's. The one timer this baseline declares is the service level of the correction task, given by the human-task template of the workflow kit and read from a reference row at run time; its value, the loop's owner and the task's queue code are Not specified in the source documents (GAP-3040; ASM-5093). This baseline declares no Quartz row, no shared job table and no batch table.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a case, its fields, its required list and its state column, which carries `WRITEOFF_EXCEPTION` and the state the correction names |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the raise and the correction (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated decision and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case`, `task` and `assignment` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `proceeds` (P8), an exception table, a retry-count column and the later stories' data are not owned by this baseline; it names them only as answers, task facts or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | Case `RC-2026-000701` with write-off `WO-2026-000311` in `POSTING_REJECTED`, a case in `WRITEOFF_EXCEPTION` and a case that has left the stage | AC1, AC3, AC6 |
| rwb-case case-move fake | The four moves accepted, and a move refused because the case is not in the expected state | AC3, AC6 |
| rwb-case task fake | A raise accepted with its owner, queue and service level, a refused assignment and an unreadable answer | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-24, R-WO-44 to R-WO-46 and the retry limit | AC2, AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for the write-off, in its exception state | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3040; ASM-5093, ASM-5095, ASM-5096).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /write-offs/{writeOffId}/correction-decision` on `/api/recovery/writeoff/v1`; the case read, the case-move answer, the task raise and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `WriteOffApproved` (EV-24) is the approval story's and the payment and ACE subscriptions are RWB-S7-E6027-APP's |
| Temporal | 1 workflow and 2 activities declared, 0 registered, 0 Schedules | `WriteOffWorkflow`, `raiseWriteOffException` and `recordCorrection` on `rwb-writeoff`, plus the human-task timer declared as a reference row |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no row, no task and no package. What it publishes is one OpenAPI 3.1 document, nine contract tables and six fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row and the answer change, twice in the loop. DP-13 moves the base and gives the correction operation its home. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-09 and DP-18 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the inbox as an absent library row, and the interaction ledger as its owner's fact.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON`, the Drools kit rows `RWB-PLT-E1072-CON` and Not specified in the source documents (CG-ALL-11148), and the human-task template of the workflow kit. The four consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the operation and validate the additive rule of AC1 in the pipeline.
2. Write the `CorrectionRequest`, `WriteOffCorrection` and `WriteOff` elements, the required list, the three correction events and the lengths of AC2, with the placeholder where a type is unstated.
3. Record the three rwb-case rows of AC3 with their owner, their budget and their placeholders.
4. Record the rwb-decision row, the rights and the error envelope of AC4.
5. Record the decision-record element of AC5, the state column and the absent exception table.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline, the trigger and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the three elements, the contract README rows for the four consumed rows and their placeholders, the declared trigger and the six fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27, the case workspace and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of a request is absent or invalid, the correction is not one of the three events, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row and the answer change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-S7-001 | Not bound by this document: it is the message of the R-WO-03 scan hold, carried in the legacy message set of the key | The scan is on hold until Finance publishes the tax criteria. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 stands in the set because the legacy table lists it for every S7 story and no path of this baseline reaches it.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its exception state through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off, its retry count, the limit in force, the rule and version and the three corrections, and rwb-case for the case, its route state and the open task; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives the states "Scan; proposed; in committee; approved" and names no exception state, while the routing logic gives the case `WRITEOFF_EXCEPTION`. This baseline declares the state as a value of the row and of the answer and takes no screen-state list from a source that has none; the missing vocabulary is part of the gap recorded for the key (ASM-5094). The refusal and not-recorded states read the messages of section 14 on the same route. The empty, loading, error and no access states of SCR-27 are Not specified in the source documents (CG-ALL-11155): Screen Specifications v1 gives none of them, so the story declares none.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-024-01 | AC1, AC2 | Contract | The correction operation and the three elements; the contract half answers the request, the answer and the write-off shape |
| TC-E6-024-02 | AC2, AC3 | Contract | Case `RC-2026-000701` and write-off `WO-2026-000311` in `POSTING_REJECTED`; the contract half answers the three correction events and the four move shapes |
| TC-E6-024-03 | AC5, AC7 | Contract | The decision-record stub stopped and an absent exception table; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-E6-024-04 | AC4 | Contract | A role without the Write-off and posting right A and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 422 of the envelope |
| TC-E6-024-05 | AC4, AC5 | Contract | RW-WOCOMM, RW-CREDITAD, RW-PRODHEAD and RW-FINANCE hold right A; the contract half answers the rights and the decision element |
| TC-S7-E6024-CON-01 | AC1 | Contract | The document validates; the operation, the base, the `Idempotency-Key` and the seven error answers are present |
| TC-S7-E6024-CON-02 | AC2 | Contract | `CorrectionRequest`, `WriteOffCorrection` and `WriteOff` validate with their properties, the required list, the three lengths and the three correction events only |
| TC-S7-E6024-CON-03 | AC3, AC4 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-task and no-rule-row boundary |
| TC-S7-E6024-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the six fakes match the document and a drifted fake fails the build |
| TC-S7-E6024-CON-05 | AC7 | Contract | The naming baseline, the tables owned, the declared trigger and the absence of a published event, a second topic and a registered Schedule |
| TC-S7-E6024-CON-06 | AC7 | Contract | The four tables of §12.7 at their boundary: each has its named owner, no foreign key leaves the schema, and no other table is owned by this baseline |
| TC-S7-E6024-CON-07 | AC8 | Contract | Each rule row BR1 to BR13 of section 8 with its covering criterion and test; an architecture-constraint rule is proved by a guardrail or boundary test |

The five legacy cases are those of RWB-E6-024 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6024-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S7-E6024-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the retry limit, the loop's owner, the service level and the row states stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, an amount, dates, a state, a retry count and a rule version only, and every example is synthetic.
- The case, the task and the assignment stay with rwb-case: the document declares no `recovery_case`, `task` or `assignment` property and no case row write (BR4).
- The posting stays with the posting story and the money with rwb-payment: the document declares no posting, no ALS reference, no proceeds and no ledger property.
- The schedule stays declarative: this story registers no Schedule, creates no Quartz row and no job table, and declares the task's timer as a reference value.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the outbox library and the human-task template come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-004 | The write-off exception loop has one named owner and a time limit; the contract fixes the operation, the correction vocabulary and the consumed rows on which the loop is built, and names the owner and the service level as reference and rule values it does not declare (FSD S7 Requirements served; GAP-3040; ASM-5093) | The three elements and the four consumed rows | TC-E6-024-01, TC-E6-024-02, TC-S7-E6024-CON-01, TC-S7-E6024-CON-02, TC-S7-E6024-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6024-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as the approval story's | TC-S7-E6024-CON-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The posting step and the task timer declared as the trigger | TC-S7-E6024-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows and the correction operation | TC-S7-E6024-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element, twice in the loop | TC-S7-E6024-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-024, disposition Split (rework); feature FEAT-WOF-12 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S7-E6024-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-024; FSD S7 Write-off and recovery v3 A2.9, A2.12 and Requirements served; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T3.3, T4, T5.3, T6.1 and T-A; API Specification v5, `WriteOff`; BRRL v4 rows R-WO-24 and R-WO-44 to R-WO-46 and the States sheet; Epics 3 to 8 Specification v3 row FEAT-WOF-12 |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S7-E6024-CON-01 to -05 |
| Feature and screens | FEAT-WOF-12, SCR-27 Write-off proposal and the case workspace task |
| Rules | R-WO-24, R-WO-44, R-WO-45 and R-WO-46, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the operation, the evaluation of R-WO-24, the decision record, the row states, the task raise and the case-move answers: RWB-S7-E6024-APP.
- The case of record, its route states, the task, the assignment and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5096).
- The posting to ALS and the general ledger, its retries and the re-post action of R-WO-44: RWB-S7-E6021-APP, with the money in rwb-payment (P8).
- The authoring, testing, approval and versioning of the WO package, the rule rows and the retry limit: rwb-decision (P7) (ASM-5095).
- The scan operation API-S7-001 and the committee decision API-S7-002: RWB-S7-E6013-APP and RWB-S7-E6018-APP.
- The other two entries to `WRITEOFF_EXCEPTION`: R-WO-41 with RWB-S7-E6027-APP and R-WO-43 with RWB-S7-E6023-APP (ASM-5097).
- The owner of the loop and its time limit, which REQ-S7-004 requires and no source names: carried as unconfirmed (ASM-5093).
- The gateway-bff composite route, the screen field list and the screen-state vocabulary of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

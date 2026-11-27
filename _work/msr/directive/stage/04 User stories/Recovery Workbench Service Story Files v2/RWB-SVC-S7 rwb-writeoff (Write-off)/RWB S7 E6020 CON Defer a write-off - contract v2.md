# RWB-S7-E6020-CON Defer a write-off - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6020-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Contract version | API Specification v5 (rwb-writeoff.yaml), base `/api/recovery/writeoff/v1` |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S7-E6020-CON-16); the squad sizes it at refinement |
| Depends on (build) | RWB-PLT-E1027-CON (DP-03); RWB-PLT-N001-CON (DP-19) |
| Contract dependencies | The consumed rows of section 12.2: the case read, the two case-move answers and the timer answer of rwb-case (P3), and the rule-package read of rwb-decision (P7) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the deferral of rwb-writeoff, split from RWB-E6-020. It fixes the defer branch of the published `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) on `/api/recovery/writeoff/v1` (DP-13) with the `CommitteeDecision` request and the `DecisionLogEntry` answer of TSD S7 T-A.2, the published `decision` set with its `defer` member, the review-date addition the request does not publish, the consumed rows of the rwb-case case read, the case-move answers and the timer answer and of the rwb-decision package read, the decision-record element of DP-03, the rights of TSD S7 T6.1, the fakes and the absence tests. The plan's C row is empty although the baseline declares four consumed rows, DP-04, DP-09 and DP-10 are absent from the pattern set, and no source publishes the review-date property, the timer element name or a message ID per error condition (GAP-3032; ASM-5059 to ASM-5058). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S7-E6020-CON-L84, X20 RWB-S7-E6020-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 11 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the deferral of rwb-writeoff — the defer branch of the committee-decision operation on `/api/recovery/writeoff/v1`, the request and answer elements with their required flags, the review-date addition, the four consumed rows, the review-timer element, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a review date, a consumed row or an answer shape can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy deferral of RWB-E6-020 crossed three boundaries at once: the case of record, its review timer, the rule version and a screen, and its single committee-decision endpoint carried approve, reject and defer with no element published for any of them. The target splits them: rwb-case owns the case, its route states and its timer row, rwb-decision owns the WO package, and rwb-writeoff owns the write-off stage, its record and the deferral of a case inside the limit. Each boundary is a contract another team builds against, so each is fixed before the app story starts.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case`, so DP-05 is declared as a prohibition (ASM-5063).

Three points are carried as gaps and assumptions rather than decided quietly: R-WO-17 requires `review_date present` and R-WO-18 refuses a defer without it, yet the published request has no review-date property and `write_off` has no column for it, so the property is an additive declaration with a placeholder (ASM-5060); the review timer has no published element name and the legacy `timer` row is rwb-case's, so the timer is declared as a durable workflow timer plus an rwb-case answer (ASM-5062); and the plan's C row is None while the baseline consumes four rows, with DP-04, DP-09 and DP-10 absent from the pattern set (ASM-5063, ASM-5064, ASM-5065).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `payment` is P8's. This document never declares another service's table or operation as its own.
- The committee-decision operation is published: TSD S7 T-A.1 gives API-S7-002 `POST /write-offs/{writeOffId}/committee-decision` with the request `CommitteeDecision`, the answer `DecisionLogEntry`, right A and the idempotency rule, and T-A.2 gives the error set as 401, 403, 404, 409, 422 and 503. The defer branch is declared inside it and needs no new path; what the sources do not give is the review-date property and a message ID per condition (GAP-3032; ASM-5059, ASM-5060).
- The published `CommitteeDecision` element of API Specification v4 is the baseline of the request: its `decision` enumeration already carries `approve`, `reject` and `defer`, with `resolutionReference` and `membersPresent`.
- The rwb-case case row, case-move answers and timer answer and the rwb-decision package row are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3032; ASM-5062, ASM-5063, ASM-5064).
- The WO package and its rows for R-WO-17, R-WO-18 and R-WO-19 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration, and the review date has no column in it.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the defer branch of the OpenAPI 3.1 document of rwb-writeoff for API-S7-002: the operation with its path parameter, its request and answer elements, its rights and its error responses.
2. Fix the `CommitteeDecision` element as API Specification v5 publishes it — `decision` with its three members, `resolutionReference` and `membersPresent` — and add `reviewDate` as the one additive optional property the rules require, with its placeholder.
3. Fix the `DecisionLogEntry` element over the ledger properties of DF-DEC-001 to DF-DEC-018 and the write-off reference of DF-FIN-010, with the required list the specification publishes.
4. Fix the consumed rows: the case read and the two case-move answers of rwb-case, the review-timer answer of rwb-case and the package read of rwb-decision with its version, marking with the placeholder what the sources do not give.
5. Record the decision-record element of DP-03, written before the case moves and before the timer is armed.
6. Record the rights of the operation, the naming baseline, the durable review timer and the rule that no value is a constant of the code; record that TSD S7 T3.2 publishes no list of values.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case`, `timer` or rule-row write, the drift between a fake and the document, and the absence of a published event and of a registered Schedule.
9. Tag the baseline and hand it to RWB-S7-E6020-APP, the approval and rejection stories that share the operation, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A field is renamed or removed within major version 1, or a required flag changes | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC5 |
| X5 | A property, a timer element or a state list is declared that no source publishes | The review fails the baseline and the absence test fails the build | None | AC2, AC5, AC7 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a `timer` row or a rule row | The review fails the baseline and the boundary test fails the build | None | AC3, AC7 |
| X7 | The document declares an event of this step, a consumed event, a second topic or a registered Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of the operation are not the ones TSD S7 T-A.1 and T6.1 give the committee decision | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices, API Specification v5 and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The review-date property name, the timer element name, the example values and the fake fixtures are settled in the baseline review; the operation, the base, the rights, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6020-APP, the approval and rejection stories that share the operation, SCR-27 and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and twelve contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the deferral of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case and timer is P3, of every v_ace_* view is P1 and of decision_log_entry and rule_row is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The defer branch of the committee-decision operation is declared on the writeoff base with its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /write-offs/{writeOffId}/committee-decision as API-S7-002 with a CommitteeDecision body in and a DecisionLogEntry answer of status 200, under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff
    Then the operation declares the path parameter writeOffId of format uuid, the Idempotency-Key header and the repeated key answering the deferral it recorded
    Then the defer branch is declared inside the one operation as the defer member of the request decision, with no second path, and the approve and reject branches of the same operation are named as RWB-S7-E6018-APP's and RWB-S7-E6019-APP's
    Then the answers 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation of the scan, of the pack or of the posting is declared by this document

  Scenario: AC2 The request and answer elements, the defer member and the review date are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with API Specification v5, TSD S7 T3.1, T3.2 and T-A.2
    Then the CommitteeDecision element declares decision of type string with the published enumeration approve, reject and defer, resolutionReference of type string and membersPresent as an array of strings, copied exactly
    Then it declares reviewDate of format date as the one additive optional property, because R-WO-17 requires review_date present and no published property carries it, and the property is marked with the placeholder (GAP-3032; ASM-5060)
    Then the DecisionLogEntry element declares the ledger properties of DF-DEC-001 to DF-DEC-018 and the write-off reference, with the required list the specification publishes: id, decisionCode, inputsRef, finalCall, decidedAt, prevHash, entryHash and chainSeq
    Then the elements declare the rule R-WO-17 with its rule version, the from state WITH_COMMITTEE and the to state DEFERRED in the answer of a deferral, and the rule R-WO-19 with the states DEFERRED and SCAN_DUE in the answer of the review date
    Then the document declares no list of values beyond the published decision set, because TSD S7 T3.2 publishes none and no source gives a review-date range, a timer type or a decision code set (GAP-3032; ASM-5059)
    Then no property is added for a timer row, a review reason, a balance, a rule row or a scan reference

  Scenario: AC3 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read is declared as consumed from P3 rwb-case, with the case reference, the case number, the product group, the stage and the case state
    Then the case-move answer is declared as consumed from P3 rwb-case, with the move DEFERRED carrying the review date, the rule ID and its version, and the move SCAN_DUE carrying the rule R-WO-19 and its version
    Then the review-timer answer is declared as consumed from P3 rwb-case, with the timer row of DF-WRK-027 to DF-WRK-036 created and cancelled by its owner
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version and its 51 rules over 27 states
    Then the operation names of the four rows are Not specified in the source documents (GAP-3032; ASM-5062, ASM-5063, ASM-5064) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property, no timer property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T-A.1, T-A.2 and T6.1
    Then the committee decision declares Write-off and posting right A with the scope applied, on API-S7-002 as T-A.1 gives it
    Then RW-WOCOMM holds RA and RW-CREDITAD holds CRUA on the capability area, RW-PRODHEAD and RW-FINANCE hold RA, and they are the four roles the legacy permission table gives right A
    Then RW-WRITEOFF holds CRU and reads the deferral and its review date without the right A
    Then every other role and every SY-* service identity of TSD S7 T6.1 holds R or U as the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition, with 422 bound to MSG-GEN-001 for an absent review date under R-WO-18

  Scenario: AC5 The decision-record element and the review timer are declared (new, D-RCV-60)
    Given the decision, data and workflow sections of the baseline
    When they are compared with the library schema, TSD S7 T2 and T4 and the ownership rows of S7 and P3
    Then one decision record is declared per rule outcome with the case reference, the write-off reference, the decision, the rule ID R-WO-17 or R-WO-19, the package version in force, the review date, the from state, the to state and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the case-move answer leaves the service, and a failed write leaves everything unchanged with MSG-P7-003
    Then the review timer is declared as a durable timer of WriteOffWorkflow on rwb-writeoff and not as a Schedule, and its row is declared as P3's, created and cancelled by rwb-case on this service's answer (GAP-3032; ASM-5062)
    Then the record carries no rule row, no review-date range as a literal and no personal data, and membersPresent is a list of identifiers in the ledger and not copied into this service's answer
    Then the document declares no table of this service beyond write_off, decision_record, idempotency_key and outbox_event

  Scenario: AC6 The six fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers the case at WITH_COMMITTEE with its pack and limit, a case that has moved and a case that is not in the pack
    Then the rwb-case case-move fake answers DEFERRED accepted and refused and SCAN_DUE accepted and refused, and the timer fake answers the row created and cancelled
    Then the rwb-decision fake answers the WO package at its version with R-WO-17, R-WO-18 and R-WO-19
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer in its in-committee and deferred states
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and neither event nor Schedule is declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no consumed event, no second topic and no Schedule, and it names WriteOffApproved (EV-24) as RWB-S7-E6021-APP's, JOB-16 as RWB-S7-E6013-APP's and JOB-05 as rwb-case's (ASM-5062, ASM-5065)
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a registered Schedule, a v_ace_* read, a timer row write or a review-date column
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6020-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The review date is the one property the baseline adds beyond the published element, and it is added as an optional additive property with a placeholder rather than as an invented required field (ASM-5060).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The deferral is a branch of rwb-writeoff's committee decision, and the contract declares the fields, the required list and the optionality of the `CommitteeDecision` and `DecisionLogEntry` elements only | TSD S7 T3.1, T-A.2; API Specification v5, `CommitteeDecision` and `DecisionLogEntry`; context pack ownership row (table `write_off`) |
| BR2 | The decision record is declared as an element written before the case moves and before the timer is armed, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC3 |
| BR3 | The case, the two moves and the timer row stay with rwb-case: the contract declares them as consumed, declares no `recovery_case` property and no `timer` property, and describes no case or timer row write | ASM-5062, ASM-5063; TSD S7 T4 |
| BR4 | The package is rwb-decision's: the contract declares the package read as consumed and declares no rule row, no threshold and no rule version as a property set | ASM-5064 |
| BR5 | No event of this step is declared: `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5065; TSD S7 T5.3 |
| BR6 | A POST declares the `Idempotency-Key` and stores its answer; no other operation is declared on this base by this story | TSD S7 T-A.2 |
| BR7 | The review date is declared as an optional additive property of the request with a placeholder, because R-WO-17 requires it and neither the published element nor `write_off` carries it; the document declares no other list of values than the published decision set | ASM-5060; FSD S7 A2.8.3.1, A2.8.3.2; TSD S7 T3.1, T3.2 |
| BR8 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, a state and a rule version only, and every example is synthetic | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR9 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR10 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR11 | The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR12 | The defer is a branch of the one published operation and not a second path; the approve and reject branches of the same operation are named as other stories' | TSD S7 T-A.1; ASM-5059 |
| BR13 | The review timer is declared and not registered: it is a durable timer of the stage workflow, no Schedule, Quartz row or job table is declared, and the timer row is P3's | Batch and Scheduling Design v5, JOB-05 and JOB-16; ASM-5062 |
| BR14 | The states `WITH_COMMITTEE`, `DEFERRED` and `SCAN_DUE` are declared as the vocabulary of the answers and of rwb-case's machine, and move no case | TSD S7 T4; Business Rules and Routing Logic v4 rows R-WO-17 and R-WO-19 |

### 9. State transitions

The lifecycle of this document, not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the review-date addition, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the approval and rejection stories, SCR-27, the wave 4 harness and the owners of rwb-case and rwb-decision accept the document and the fakes | Baselined |
| Baselined | The review-date property is confirmed | The business lead and rwb-case confirm the date property and the timer answer inside major version 1 | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional reference or a filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the optional review date becomes required | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC5 and AC7 fail: a timer property, a `v_ace_*` view, a `recovery_case` property, a second path, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `WITH_COMMITTEE`, `DEFERRED` and `SCAN_DUE` are route states of rwb-case (TSD S7 T4), R-WO-18 keeps a case at `WITH_COMMITTEE` when the review date is absent, and R-WO-19 returns a deferred case to `SCAN_DUE` at the review date. This baseline fixes the vocabulary and the answer shape and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the review-date addition and the correction of the plan rows the baseline consumes, including the four consumed rows and the absent DP-04, DP-09 and DP-10 rows |
| Business lead | Confirms the review-date property and the decision set that the placeholder describes |
| Consuming teams (the app story, the approval and rejection stories, SCR-27, the wave 4 harness and the owners of rwb-case, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

The rwb-access authorise check that the operation calls is Not specified in the source documents (DP-08; DOR-RWB-S7-E6020-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Request element | `CommitteeDecision`: `decision` of type string with the published members `approve`, `reject` and `defer`, `resolutionReference` of type string, `membersPresent` as an array of strings, copied exactly from API Specification v4 (ASM-5061), plus `reviewDate` of format date as the one additive optional property | BR1, BR7 |
| Answer element | `DecisionLogEntry`: the ledger properties of DF-DEC-001 to DF-DEC-018 and the write-off reference, with the required list `id`, `decisionCode`, `inputsRef`, `finalCall`, `decidedAt`, `prevHash`, `entryHash` and `chainSeq` | BR1 |
| Review date | No property, field ID, length, list or column in any source: declared as an optional `reviewDate` of format date and carried in the decision record and the case-move answer (GAP-3032; ASM-5060) | BR7 |
| Wait-off element | The write-off row the answer refers to: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, read only; `committee_date`, `posted_date`, the GL columns and `recovered_after` are not set by a deferral | BR1 |
| Lists | The published `decision` set only: `approve`, `reject`, `defer`. TSD S7 T3.2 publishes no list of values and no source gives a review-date range or a timer type (ASM-5059) | BR7 |
| Event data | None of this step: no event is declared (§12.3) | BR5 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the case moves and before the timer is armed (DP-03) | BR2 |
| Case, timer and rule facts | DF-CAS-001 to DF-CAS-023 of `recovery_case`, DF-WRK-027 to DF-WRK-036 of `timer` in P3, and DF-REF-001 to DF-REF-015 of `rule_row` in P7, read only through the owners' rows and never written, copied or joined here | BR3, BR4 |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8) | BR3, BR4 |
| Consumed fields with no source | The operation names of the case read, the two case-move answers, the timer answer and the package read, and the message ID of each error condition: Not specified in the source documents (GAP-3032; ASM-5062, ASM-5063, ASM-5064) | BR3, BR4 |

Screens: this contract declares no screen. The empty, loading, error and no-access states of SCR-27 belong to the app story RWB-S7-E6020-APP and are not declared here (DOR-RWB-S7-E6020-CON-10).

Personal data: none of the fields in this table is classed as personal data; the data steward confirms this in §10 (BR8).

Reference data: the only list read is the published `decision` set above. This story names no parameter key from parameter-catalog.csv; the review period of R-WO-17 is Not specified in the source documents (DOR-RWB-S7-E6020-CON-20), and the reference-data contract of DP-06 and DP-07 is not applied (Patterns applied: DP03, DP13, DP19).

The field-level types of the added property and the required flags of the two elements are settled in the baseline review; this story fixes the property names, the published enumeration and the optionality rule of BR10. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-offs/{writeOffId}/committee-decision` (API-S7-002) | `CommitteeDecision` in with the decision `defer` and the review date, `DecisionLogEntry` of status 200 out, carrying the rule `R-WO-17` with its version, the review date and the state `DEFERRED`, or the rule `R-WO-19` with the state `SCAN_DUE` | Write-off and posting, right A, scope applied | `Idempotency-Key` header |

The operation answers 400, 401, 403 with MSG-P4-002, 404 for a write-off that is not in the pack, 409 for a case that has left `WITH_COMMITTEE`, 422 with MSG-GEN-001 for an absent review date under R-WO-18 and 503, each with the error envelope and one message ID of section 14. The path, the operation ID, the two element names, the right and the error codes are published in TSD S7 T-A.1 and T-A.2 and API Specification v5; the review-date property and the message per condition carry the placeholder (GAP-3032; ASM-5059, ASM-5060). The approve and reject branches of the same operation belong to RWB-S7-E6018-APP and RWB-S7-E6019-APP, and the module's other published operation, `POST /write-off-scans` (API-S7-001, right C), belongs to RWB-S7-E6013-APP; none of them is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3032; ASM-5063)) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, case number, product group, stage and state of the case at `WITH_COMMITTEE`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3032; ASM-5063)) | rwb-case (P3) | P3 rwb-case | The move `DEFERRED` with the review date and the rule version, and the move `SCAN_DUE` under R-WO-19; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The review-timer answer (operation name Not specified in the source documents (GAP-3032; ASM-5062)) | rwb-case (P3) | P3 rwb-case | The `timer` row of DF-WRK-027 to DF-WRK-036 created for the review date and cancelled on R-WO-19; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3032; ASM-5064)) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO package at its version, with R-WO-17, R-WO-18 and R-WO-19 among its 51 rules over 27 states; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3032; ASM-5062, ASM-5063, ASM-5064).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (`EV-24`, `writeOffId`, `caseId`, `amount`, consumed by Posting), which belongs to the posting step of R-WO-20 and R-WO-21, declared by RWB-S7-E6021-APP. A deferral approves nothing, posts nothing and changes no amount, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that will relay EV-24 is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5065).

#### 12.4 Events consumed

None. The service listens to the rwb-source-data and rwb-payment events in its scan and recovery steps (context pack connection matrix, row S7), not in the deferral: a deferral reads no ACE extract and moves no money, and its wait is a workflow timer. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one. The trigger of the step is the committee member's decision on SCR-27 through the composite route; the FSD declares no background event for the feature (FSD S7 A2.8.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case at the write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` | The stage that hosts the deferral; its signals, its durable review timer and its outcome for the parent are declared, not built |
| `recordCommitteeDeferral` | Activity, the deferral step, with R-WO-17, the R-WO-18 refusal and the R-WO-19 firing | `rwb-writeoff` | The case reference, the decision `defer`, the review date and the package version in; the rule ID with its version, the decision recorded, the timer set and the case move out |
| `ReviewTimer` | Durable workflow timer | `rwb-writeoff` | Armed with the review date of R-WO-17, fired once for R-WO-19 and cancelled if the case leaves `DEFERRED` |

No child workflow for the case and none for the money exists in this service. The activity and timer names are target design choices fixed by no source document. No workflow, activity or timer is registered by this story (ASM-5062).

The catalog gives the trigger as JOB-16; its timing against AceDataReady, the workflow ID form, the start rule and the duplicate-start policy of WriteOffWorkflow are Not specified in the source documents (CG-ALL-11045).

#### 12.6 Schedules

None. The deferral is a member-driven step and the review wait is a durable timer of the stage workflow, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. `JOB-16`, the write-off scan, becomes the Temporal Schedule of R-WO-01 in RWB-S7-E6013-APP, and `JOB-05` Timer check, which implements TimerScheduler for every caller (Batch and Scheduling Design v5, JOB-05), is rwb-case's; both are named here only as other stories' (ASM-5062).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case; the row the answer refers to and the row a deferral does not change |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the deferral and of the review-date return (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated request and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6) and `payment` (P8) are not owned by this baseline; it names them only as answers, rule versions or another story's data, and no foreign key leaves the schema (DP-01). The review date has no column in `write_off` and no field ID in TSD S7 T3.1, which is the gap the additive property carries (GAP-3032; ASM-5060).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | The case of record at `WITH_COMMITTEE` with its pack and limit, `RC-2026-000732` among 40 cases; a case that has moved; a case that is not in the pack | AC1, AC3, AC6 |
| rwb-case case-move fake | The moves `DEFERRED` and `SCAN_DUE` accepted with the review date and the rule version, and a move refused | AC3, AC6 |
| rwb-case review-timer fake | The `timer` row created for the review date and cancelled on R-WO-19; a case that is no longer at `DEFERRED` | AC3, AC5, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-17, R-WO-18 and R-WO-19 among its 51 rules over 27 states | AC2, AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000732`, in its in-committee and deferred states | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the four consumed rows carry the placeholder until their owners confirm them (GAP-3032; ASM-5062, ASM-5063, ASM-5064).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `POST /write-offs/{writeOffId}/committee-decision` on `/api/recovery/writeoff/v1` (defer branch); the case read, the two case-move answers, the timer answer and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; `WriteOffApproved` (`EV-24`) is RWB-S7-E6021-APP's, and the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 1 activity and 1 durable timer declared, 0 registered | `WriteOffWorkflow`, `recordCommitteeDeferral` and `ReviewTimer` on `rwb-writeoff`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no timer, no amount and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and six fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the case moves. DP-13 moves the base of the legacy paths and gives the defer branch its home. DP-19 sits behind SCR-27, whose screen model is the edge contract's. DP-04, DP-05, DP-09 and DP-10 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the ACE facts as another service's data and never views, the outbox as an absent library row, and the review timer as a durable workflow timer rather than a registered Schedule (GAP-3032; ASM-5062, ASM-5064, ASM-5065).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule evaluation would add, and the scheduler kit `RWB-PLT-E1071-CON` that a Schedule would add. The four consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the defer branch of API-S7-002 and validate the additive rule of AC1 in the pipeline.
2. Write the `CommitteeDecision` element exactly as published, with the `defer` member, and the `reviewDate` addition with its placeholder (AC2).
3. Write the `DecisionLogEntry` element with its ledger properties and the published required list (AC2).
4. Record the four consumed rows of AC3 with their owner, their budget and their placeholders.
5. Record the rights and the error envelope of AC4, with 422 bound to MSG-GEN-001.
6. Record the decision-record element and the durable review timer of AC5, and declare that no timer row is written here.
7. Publish the six fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the two elements and the review-date addition, the contract README rows for the four consumed rows and their placeholders, the declared timer and the six fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the twelve contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the approval and rejection stories, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The contract describes the held-scan state from which no pack reaches the committee (R-WO-03), raised by RWB-S7-E6013-APP and not by this operation | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, the review date on a defer among them, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right A the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the case moves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. No source publishes a message for a review date in the past, and none is bound to one here (GAP-3032).

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its in-committee and deferred states through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the pack, the decision and the review date, and rwb-case for the case and its route state; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The legacy screen table gives the states "Scan; proposed; in committee; approved": the deferred state is this step's, the scan state belongs to RWB-S7-E6013-APP, the proposed state to RWB-S7-E6015-APP, the routing to RWB-S7-E6017-APP, the approved state to RWB-S7-E6018-APP and the rejected state to RWB-S7-E6019-APP. The refusal, missing-review-date and not-recorded states read the messages of section 14 on the same route. The empty, loading, error and no-access states of SCR-27 are Not specified in the source documents (CG-ALL-11050), because Screen Specifications v1 gives none of them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-020-01 | AC1, AC3 | Contract | The 40-case in-committee population on the fake; the contract half answers the operation, the case row and the package row |
| TC-E6-020-02 | AC2, AC5, BR14 | Contract | `RC-2026-000732` at `WITH_COMMITTEE`; the contract half answers the two elements, the review date and the decision element |
| TC-E6-020-03 | AC5, AC7, BR2 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path, the declared timer and the absence tests |
| TC-E6-020-04 | AC4 | Contract | A role without the right A and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 422 of the envelope |
| TC-E6-020-05 | AC4, AC5, BR13 | Contract | RW-WOCOMM holds RA and RW-CREDITAD holds CRUA; the contract half answers the rights and the timer declaration |
| TC-S7-E6020-CON-01 | AC1, BR6, BR10, BR12 | Contract | The document validates; the operation, the base, the defer branch, the `Idempotency-Key` and the six error answers are present |
| TC-S7-E6020-CON-02 | AC2, BR1, BR7 | Contract | The `CommitteeDecision` and `DecisionLogEntry` elements validate with the published members, the review-date addition and the required list |
| TC-S7-E6020-CON-03 | AC3, AC4, BR3, BR4, BR11 | Contract | The four consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-`timer` and no-rule-row boundary; the rights |
| TC-S7-E6020-CON-04 | AC5, AC6 | Contract | The decision-record element matches the library schema; the six fakes match the document and a drifted fake fails the build |
| TC-S7-E6020-CON-05 | AC7, BR5, BR9, BR13 | Contract | The naming baseline, the tables owned and the absence of a published event, a consumed event, a second topic and a registered Schedule |
| TC-S7-E6020-CON-06 | AC7, BR8 | Contract | The four tables of §12.7 are the only tables owned, with no foreign key out of the schema; no schema, example or fake carries a personal data field (Not specified in the source documents (DOR-RWB-S7-E6020-CON-4)) |

The five legacy cases are those of RWB-E6-020 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6020-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The six cases `TC-S7-E6020-CON-01` to `-06` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: R-WO-17 to R-WO-19, their states, the review-date condition, the decision set and the package version stay rule rows and reference data, never a schema default, an invented enumeration or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, a state and a rule version only, and every example is synthetic.
- The case and the timer stay with rwb-case: the document declares no `recovery_case` property, no `timer` property, no case row write and no timer row write (BR3).
- ACE data stays with rwb-source-data: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read.
- The money stays with rwb-payment and the ledger with rwb-decision: the document declares no posting, no proceeds and no rule row.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-writeoff; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- The wait stays declarative: the review timer is declared as a durable workflow timer, and no Schedule, Quartz row or job table is registered.
- No retired element is reintroduced: the absence tests fail a build that declares a published event of this step, a consumed event, a second topic, a Schedule or a review-date column.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (FSD S7 Requirements served); the deferral shares the row with the approval and rejection stories (ASM-5066) | The defer branch of API-S7-002, the two elements, the review-date addition and the four consumed rows | TC-E6-020-01, TC-E6-020-02, TC-S7-E6020-CON-01, TC-S7-E6020-CON-02, TC-S7-E6020-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6020-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as a later story's | TC-S7-E6020-CON-05 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The durable review timer declared as a workflow timer | TC-S7-E6020-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S7-E6020-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6020-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-020, disposition Split (rework); feature FEAT-WOF-08 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S7-E6020-APP; this baseline copies none of them |
| Wave and release | Wave 4 and release 30 April 2027 (tentative), copied unchanged from the plan; EP06 and the service wave agree at 4, so no W-MAP conflict is raised (ASM-5058) |
| Source text | Legacy RWB-E6-020; FSD S7 Write-off and recovery v3 A2.8, Requirements served and Screens; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; API Specification v5, `CommitteeDecision` and `DecisionLogEntry`; Business Rules and Routing Logic v4 rows R-WO-17, R-WO-18 and R-WO-19; Batch and Scheduling Design v5, JOB-05 and JOB-16 |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S7-E6020-CON-01 to -05 |
| Feature and screens | FEAT-WOF-08, SCR-27 Write-off proposal |
| Rules | R-WO-17 and R-WO-19, with R-WO-18 as the refusal of a defer with no review date, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-016, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the defer branch, the evaluation of R-WO-17 to R-WO-19, the records, the timer and the two case-move answers: RWB-S7-E6020-APP.
- The case of record, its route states and the `timer` row: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5062, ASM-5063).
- The authoring, testing, approval and versioning of the WO package and of the rule rows: rwb-decision (P7) (ASM-5064).
- The review-date property and the timer answer: the business lead and rwb-case confirm them at the baseline review and the placeholder stands until then (GAP-3032; ASM-5060).
- The approve branch of the same operation and the credit-committee escalation: RWB-S7-E6018-APP. The reject branch: RWB-S7-E6019-APP.
- The monthly scan, the tax criteria, the pack and the routing into committee: RWB-S7-E6013-APP to RWB-S7-E6017-APP.
- The posting, `WriteOffApproved` (`EV-24`), the provision release and the reconciliation: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- A list of values, a review-date range or a message for a date in the past: no source gives one (ASM-5059, ASM-5060).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

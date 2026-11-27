# RWB-S8-E7004-CON Run X4 fraud end to end - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Contract version | v1 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S8-E7004-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the X4 fraud deviation of rwb-deviation, split from RWB-E7-004. It fixes the two operations on `/api/recovery/deviation/v1` (DP-13), the `DeviationRequest`, `DeviationOutcome` and `Deviation` elements with the field IDs DF-CAS-036 to DF-CAS-045 and the three lists, the consumed rows of rwb-case and rwb-decision, the two events of the service on `rwb.deviation.events.v1`, the decision-record element of DP-03, the rights of TSD S8 T6.1, the fakes and the absence tests. No operation re-assigns or clears a deviation by hand, because the map publishes two operations and the patch body carries an outcome and a note only. DP-04, DP-05, DP-09 and DP-16 are not in the plan's pattern set although the step evaluates a package, consumes an event and reaches no external system. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S8-E7004-CON-L55, HELD-RWB-S8-E7004-CON-L82, X20 RWB-S8-E7004-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 13 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the X4 deviation of rwb-deviation — the two operations on `/api/recovery/deviation/v1`, the request, outcome and deviation elements, the two events, the consumed rows, the decision-record element, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-06, SCR-08 and the wave 4 harness build against one fixed, testable contract on Day 1, and a property, a consumed row or an event shape can never drift between rwb-deviation, rwb-case, rwb-decision and rwb-comms without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy X4 flow of RWB-E7-004 crossed four boundaries at once: the case and its two clocks, the rule version and the record, the referral to the fraud team and two screens. The target splits them: rwb-case owns the case, the route states and the timers; rwb-decision owns the rule rows and the central ledger; rwb-deviation owns the deviation row, the two operations and the two events; rwb-comms and rwb-treatment consume the events for the contact rules. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the shapes of the request and the outcome, the ten properties of `Deviation` with their required list and their three enumerations, the two events with their data and their consumers, and the consumed case and rule rows.

The baseline also fixes the naming the checks require: schema and login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with its retry and `.dlt` topics, task queue `rwb-deviation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.deviation` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_decision`, so DP-05 is declared as a prohibition and the case and rule facts are consumed on their owners' contracts only (ASM-5162). The four open points are the ones section 13 lists: the five consumed rows against an empty C row and the absent DP-04, DP-09 and DP-16 rows, the absent library and kit rows, the Aric referral that is P4's, and the missing state vocabulary and clear operation.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `deviation` is S8's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's, `notice` is P6's and `write_off` is S7's. This document never declares another service's table or operation as its own.
- The rwb-case case read and timers read and the rwb-decision package and decision-log reads are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3058; ASM-5162, ASM-5163).
- The outbox and inbox library of DP-09 is the platform dependency of the topic and of the consumed case event; the plan's H row for this key does not carry it (ASM-5164).
- The DEVIATIONS route set of 22 rules over 9 states and the UNIVERSAL package of 50 rules are governed in rwb-decision (P7), with R-UNI-08, R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21 among them; this baseline names them and declares none of them.
- The `deviation` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-deviation for this key: the two operations with their request and answer elements, their rights and their error responses.
2. Fix the `DeviationRequest` element: `deviationCode` in the seven values, `reason` and `documentIds`, as API Specification v5 publishes them, with the requiredness the source does not give.
3. Fix the `DeviationOutcome` element: `outcome` in the three values and `note`, which is the whole published surface of a manual action on a deviation.
4. Fix the `Deviation` element: the ten properties of DF-CAS-036 to DF-CAS-045, the three enumerations, the three maximum lengths and the required list API Specification v5 publishes.
5. Fix the two events: `DeviationRaised` (EV-06) with `caseId`, `deviationCode` and `raisedBy`, and `DeviationCleared` (EV-07) with `caseId`, `deviationCode` and `outcome`, on `rwb.deviation.events.v1` with its retry and `.dlt` topics, and their consumers.
6. Fix the consumed rows: the case read, the timers read, the stage pause and resume signal, the package read and the decision-log read, marking with the placeholder what the sources do not give.
7. Record the decision-record element of DP-03, written before the row and the state change, and the rights of TSD S8 T6.1 and the legacy permission table.
8. Record the naming baseline, the absence of a job and of an Aric operation, and the rule that no value is a constant of the code.
9. Publish the contract tables of section 12, the fakes of 12.8 and the contract tests, then tag the baseline and hand it to RWB-S8-E7004-APP, SCR-06, SCR-08 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or answer body fails schema validation | The build fails on the schema lint; a deployed service answers 422 or 500 with the error envelope | MSG-GEN-001 | AC1, AC6 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | The `Deviation` element is declared without the required list or with a different enumeration | The schema test fails the build | None | AC2 |
| X4 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X5 | A consumed row has a name or a field list the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC4, AC5 |
| X6 | A property is declared that no source publishes, for example an assignment field, a clear operation or a case property | The review fails the baseline and the absence test fails the build | None | AC1, AC4, AC7 |
| X7 | The document declares another service's operation or table as provided, or a `v_ace_*` view | The review fails the baseline and the boundary test fails the build | None | AC4, AC7 |
| X8 | The document declares an Aric operation, a second topic or a job | The absence test fails the build | None | AC5, AC7 |
| X9 | The rights of an operation are not the ones TSD S8 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S8 appendices, API Specification v5 and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S8-E7004-APP, SCR-06, SCR-08, the wave 4 harness and the rwb-comms and rwb-treatment consumers on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and eight contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the X4 deviation of rwb-deviation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of deviation is S8, of recovery_case and timer is P3, of decision_log_entry and rule_row is P7 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two deviation operations are declared on the deviation base and no third is invented (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /cases/{caseId}/deviations with a DeviationRequest body in and a Deviation answer of status 200, under the base /api/recovery/deviation/v1 and owned by rwb-deviation
    Then it declares PATCH /deviations/{deviationId} with a DeviationOutcome body in and a Deviation answer, under the same base
    Then the create declares the Idempotency-Key header and the answers 401, 403, 404, 409, 422 and 503 with one envelope and one message ID per condition, as TSD S8 T-A.2 gives the error set of API-S8-001 and API-S8-002
    Then the patch declares no Idempotency-Key, as TSD S8 T-A.2 gives it, and a repeated outcome is described as 409
    Then no clear operation, no GET /deviations, no assignment operation and no Aric operation is declared, because the map publishes these two operations only (GAP-3058; ASM-5163, ASM-5168)

  Scenario: AC2 The request, outcome and deviation elements are fixed with their lists and their required list (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with API Specification v5 and TSD S8 T3.1 and T3.2
    Then the DeviationRequest element declares deviationCode in the seven values X1 to X7, reason of type string and documentIds as an array of uuid, and nothing else
    Then the DeviationOutcome element declares outcome in RETURNED, RE_ROUTED and CASE_ENDED and note of type string, and nothing else
    Then the Deviation element declares the ten properties of DF-CAS-036 to DF-CAS-045: id, caseId, deviationCode, raisedAt, raisedBy, pausedState, handlerUserId, contactStop, clearedAt and outcome
    Then its required list is id, caseId, deviationCode, raisedAt, raisedBy, pausedState and contactStop, as API Specification v5 publishes it
    Then deviationCode keeps maxLength 3, raisedBy maxLength 20 and pausedState maxLength 60, and the three enumerations are the lists LOV-DEVIATION, LOV-RAISED-BY and LOV-DEV-OUTCOME
    Then no property is added for a case state, a timer, a clock, a rule row or a handler role

  Scenario: AC3 The two events are declared with their data and their consumers (new, D-RCV-60)
    Given the event section of the baseline
    When it is compared with TSD S8 T5.3 and the event catalogue rows 06 and 07
    Then DeviationRaised is declared as EV-06 on rwb.deviation.events.v1 as rwb.deviation.DeviationRaised.v1, with caseId, deviationCode and raisedBy and no personal data
    Then DeviationCleared is declared as EV-07 on the same topic as rwb.deviation.DeviationCleared.v1, with caseId, deviationCode and outcome and no personal data
    Then the topic carries its retry and .dlt topics, and the two events are the only events of this key
    Then the consumers are declared as rwb-case, rwb-comms and rwb-treatment, and no consumer is added
    Then the document declares no event of an assignment and no third event, and names the target names as the naming rule's while the catalogue publishes the monolith names (GAP-3058; ASM-5164)

  Scenario: AC4 The consumed rows of rwb-case and rwb-decision are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack
    Then the case read and the timers read are declared as consumed from P3 rwb-case, with the case state, the paused state, the handler, the stage clock, the prescription clock and the deviation service level
    Then the stage pause and the stage resume are declared as the signal the parent CaseWorkflow applies on the workflow boundary, and no REST path is invented for them
    Then the DEVIATIONS route set and the UNIVERSAL package are declared as consumed from P7 rwb-decision at their version in force, with R-UNI-08 and R-DEV-01 to R-DEV-21 among their rows
    Then the decision record of the case is declared as consumed from P7 rwb-decision with its rule version and its central confirmation
    Then the operation names of the five rows are Not specified in the source documents (GAP-3058; ASM-5162, ASM-5163) and the rows carry the placeholder
    Then the document declares no v_ace_* path, no recovery_case property, no timer property and no grant on any rwb_* schema of another owner
    Then each row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The decision-record element, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the decision, access and error sections of the baseline
    When they are compared with the library schema and with TSD S8 T-A.1 and T6.1
    Then one decision record is declared per action with the case reference, the deviation reference, the rule ID, the package version in force, the code, the raised-by value, the paused state, the outcome, the case move and the decided-at time
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the row and the state change, and a failed write leaves them unchanged with MSG-P7-003
    Then the record carries no rule row, no threshold as a literal and no personal data
    Then the two operations declare the capability area Case record with right U and the scope applied
    Then RW-FRAUD and RW-CASEOWN hold RU, RW-TEAMMGR holds R, and every other role and every SY-* service identity of TSD S8 T6.1 holds the right the matrix gives it
    Then a role without the right is described as refused with MSG-P4-002, and the error envelope carries one message ID per condition

  Scenario: AC6 The seven fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case case fake answers ANY_STATE, DEV_FLAGGED, DEV_WITH_OWNER with the fraud team, DEV_REROUTE and ROUTE_D6 for case "RW-2026-001204", and a case already closed
    Then the rwb-case timers fake answers the stage clock paused, the prescription clock running and a pause refused because no timer runs, and the pause and resume fake accepts the signal
    Then the rwb-decision fakes answer the package at its version in force and an absent version, the decision record with its rule version and a ledger that does not confirm
    Then the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-06 and SCR-08 answers
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline, the absent trigger and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_deviation, the login is rwb_deviation, the base is /api/recovery/deviation/v1, the topic is rwb.deviation.events.v1 with its retry and .dlt topics, the queue is rwb-deviation in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the tables named as owned are deviation and the library objects decision_record, idempotency_key, outbox_event and inbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and are consumed only through their contracts
    Then no job and no Schedule is declared, because the context pack gives S8 none and the service level of R-DEV-20 is a durable timer inside the workflow
    Then no Aric operation, endpoint, topic or status word is declared, and the referral of INT-31 is named as FEAT-ADM-13 in P4 and not available today (ASM-5165)
    Then the absence test fails a build that adds a published property, a clear operation, an assignment operation, a job, a v_ace_* read or an Aric call
```

These eight criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S8-E7004-APP and copy no criterion of the legacy story: legacy AC2 stays with the app story word for word and legacy AC1 stays with RWB-ITG-E7004-ITG, and this baseline copies neither.

Scenario: AC8 Each business rule BR1 to BR13 has its own test row, and a rule without a row fails the build (new, D-RCV-60)
    Given the business rules BR1 to BR13 of section 8 are the rules of this contract
    When the test rows of section 16 are read
    Then each rule BR1 to BR13 is covered by a test row in section 16

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The deviation is rwb-deviation's, and the contract declares the fields, the required list and the enumerations of the `Deviation` element only | TSD S8 T3.1 and T3.2; API Specification v5, `Deviation`; context pack ownership row (table `deviation`) |
| BR2 | The decision record is declared as an element written before the row and the state change, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S8 T2; legacy AC2 |
| BR3 | The case and the two clocks stay with rwb-case: the contract declares the reads and the boundary signal as consumed, and declares no case property, no timer property and no pause operation | R-DEV-01; ASM-5163 |
| BR4 | The rule rows and the central ledger stay with rwb-decision: the contract declares the package read and the decision-log read, and declares no rule, no threshold and no service level as a property | ASM-5162 |
| BR5 | No Aric operation is declared: INT-31 is not available today and the referral is FEAT-ADM-13 in P4 | Epics 3 to 8 Specification v3, INT-31 and FEAT-ADM-13; ASM-5165 |
| BR6 | The two events are the two published in TSD S8 T5.3 and the catalogue rows 06 and 07, with their data and their consumers; no third event and no second topic | TSD S8 T5.3; Event and Messaging Design v5; ASM-5164 |
| BR7 | A create declares the `Idempotency-Key` and stores its answer; the patch declares none, as TSD S8 T-A.2 gives it, and a repeated outcome is a conflict | TSD S8 T-A.2 |
| BR8 | The lists are the three published by TSD S8 T3.2 and no enumeration is invented: no list of values exists for the deviation state, which the contract therefore does not declare | TSD S8 T3.2; ASM-5167 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, a code, a date, a state and a rule version only | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR10 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR12 | The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided | DP-01, DP-11 |
| BR13 | R-UNI-08 and R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21 are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; FSD S8 A2.13.3.1; ASM-5162 |

### 9. State transitions

The lifecycle of this document, not of a deviation:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the three elements, the two events, the consumed rows, the decision element and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-06, SCR-08, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-comms and rwb-treatment accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional answer field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or the required list or an enumeration changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1 and AC7 fail: a clear operation, an assignment or Aric operation, a case property, a `v_ace_*` view, a job or a third event | In review |

The state machine the document describes is the app story's and rwb-case's: `DEV_FLAGGED`, `DEV_WITH_OWNER`, `DEV_REROUTE` and `ROUTE_D6` are the states of TSD S8 T4 and of the case of record. This baseline fixes the vocabulary of the request, the outcome, the answer and the two events, and moves no case and no row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the five consumed rows and the absent DP-04, DP-09 and DP-16 rows |
| Consuming teams (the app story, SCR-06, SCR-08, the wave 4 harness, and the owners of rwb-case, rwb-decision, rwb-comms and rwb-treatment) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the outbox and inbox library and the CloudEvents envelope this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element, an event or a fake |

The per-service login behind the security scheme is named "the rwb-deviation login (DP-02)" and is not part of this baseline. The referral of Aric is not this baseline's to sign off: it is FEAT-ADM-13 in P4. Every operation is authorised through the check of DP-08; its name and the rights it reads: Not specified in the source documents (DOR-RWB-S8-E7004-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

BR Field ID for each row of the table below: Not specified in the source documents (DOR-RWB-S8-E7004-CON-7).

| Item | Content |
|---|---|
| Request element | `deviationCode` in X1 to X7, `reason` of type string and `documentIds` as an array of uuid, as API Specification v5 publishes them; the source publishes no required list |
| Outcome element | `outcome` in `RETURNED`, `RE_ROUTED` and `CASE_ENDED` and `note` of type string, which is the whole published surface of a manual action on a deviation |
| Deviation element | The ten properties of DF-CAS-036 to DF-CAS-045: `id`, `caseId`, `deviationCode`, `raisedAt`, `raisedBy`, `pausedState`, `handlerUserId`, `contactStop`, `clearedAt` and `outcome` |
| Required list | `id`, `caseId`, `deviationCode`, `raisedAt`, `raisedBy`, `pausedState` and `contactStop`, as API Specification v5 publishes them |
| Lengths and formats | `deviationCode` at maxLength 3, `raisedBy` at maxLength 20, `pausedState` at maxLength 60, `id`, `caseId` and `handlerUserId` of format uuid, `raisedAt` and `clearedAt` of format date-time |
| Lists | `LOV-DEVIATION`, `LOV-RAISED-BY` and `LOV-DEV-OUTCOME` of TSD S8 T3.2 and no other; no list of values exists for the deviation state, so no enumeration is declared for it (ASM-5167). Reference data: the reference-data contract of DP-06 and DP-07; parameters read: Not specified in the source documents (DOR-RWB-S8-E7004-CON-20) |
| Event data | `DeviationRaised`: `caseId`, `deviationCode`, `raisedBy`; `DeviationCleared`: `caseId`, `deviationCode`, `outcome`; no personal data in either |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row and the state change (DP-03) |
| Case and rule facts | DF-CAS-001 to DF-CAS-023 and DF-WRK-027 to DF-WRK-036 of P3, and DF-REF-001 to DF-REF-015 of P7, read only through the owners' rows and never written, copied or joined here |
| Not declared here | `recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `write_off` (S7), an Aric operation and the later stories' data |
| Consumed fields with no source | The operation names of the five consumed rows and the REST path of the stage pause and resume: Not specified in the source documents (GAP-3058; ASM-5162, ASM-5163) |

The field-level types of the consumed rows are settled in the baseline review; this story fixes the property names, the required list, the three enumerations and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | DeviationRequest in, Deviation of status 200 out, the raise of the deviation (API-S8-001) | Case record, right U, scope applied | `Idempotency-Key` header |
| PATCH | `/deviations/{deviationId}` | DeviationOutcome in, Deviation out, the outcome and the case move (API-S8-002) | Case record, right U, scope applied | None declared, as TSD S8 T-A.2 gives it; a repeated outcome is 409 |

The operations answer 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14, as TSD S8 T-A.2 gives the error set of both operation IDs. The map publishes these two operations and no more: there is no clear operation, no `GET /deviations` and no assignment operation, so the assignment of R-DEV-04 is the rule's inside the raise and the clear is the outcome of R-DEV-13 and R-DEV-14 through the patch (ASM-5163, ASM-5168).

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use in the baseline |
|---|---|---|---|
| The case read (operation name Not specified in the source documents (GAP-3058; ASM-5163)) | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state, the paused state and the handler after each step; faked |
| The timers read (operation name Not specified in the source documents (GAP-3058; ASM-5163)) | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The stage clock, the prescription clock and the deviation service level; faked |
| The stage pause and resume signal (no REST path is published) | the parent `CaseWorkflow` on `rwb-case` | P3 rwb-case | The pause at the raise and the resume at the clear, as the boundary element the parent applies; faked |
| The DEVIATIONS route set and the UNIVERSAL package in force (operation name Not specified in the source documents (GAP-3058; ASM-5162)) | `/api/recovery/decision/v1` | P7 rwb-decision | The 22 rules over 9 states with R-UNI-08, at their version; faked |
| The decision log of the case (operation name Not specified in the source documents (GAP-3058; ASM-5164)) | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The record and its central confirmation; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3058; ASM-5162).

#### 12.3 Events published

| Event | Topic | Data | Consumers |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | `caseId`, `deviationCode`, `raisedBy` | rwb-case, rwb-comms, rwb-treatment |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | `caseId`, `deviationCode`, `outcome` | rwb-case, rwb-comms, rwb-treatment |

The two events are the service's event set in TSD S8 T5.3 and the catalogue rows 06 and 07, and their target names follow the naming rule of §R4 while the catalogue publishes the monolith names (ASM-5164). Each is written to the outbox in the same transaction as the `deviation` row and the record, and relayed as a CloudEvent (DP-09, ADR-015). The outbox and inbox library `RWB-PLT-TE006-CON` is the platform dependency the plan does not carry for this key.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the baseline |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | The state of record the resume point is taken from; consumed through the inbox, one processed row per event; the target name follows the naming rule and is published in no source document (GAP-3058; ASM-5164) |

One subscription and nothing else. The events of rwb-payment and rwb-agent that the connection matrix gives row S8 belong to the other deviation stories. The inbox is the DP-09 library object the plan's H row does not hold.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, the child of `CaseWorkflow`, started at any time in the case, continues-as-new at each stage end | `rwb-deviation` | Its input, its signals and its outcome for the parent are declared, not built; it pauses the stage timer through the parent and never the prescription timer |
| `EvaluateDeviationRules` | Activity | `rwb-deviation` | The case and the code in; the rule ID with its package version and the case move out |
| `RecordAndApplyDeviation` | Activity | `rwb-deviation` | The rule outcome in; the record, the row, the outbox row and the case-move answer out, in one transaction |

Workflow ID form: Not specified in the source documents (CG-ALL-11524). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-11524). No child workflow for the case exists in this service. The three names are a target design choice and no workflow or activity is registered by this story.

#### 12.6 Schedules

None. The context pack gives S8 no job, and the X4 flag arrives as a request or an event and never on a cron; the service level of R-DEV-20 is a durable timer inside the workflow. This baseline declares no Quartz row, no shared job table and no batch table, and the absence test of AC7 fails a build that registers a Schedule.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation of a case, its ten fields, its required list and its state column |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the create and the answer it holds |
| outbox_event | PLT library, created in `rwb_deviation` | The row of the two published events (§12.3) |
| inbox_event | PLT library, created in `rwb_deviation` | The one processed row per consumed case event (§12.4) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `notice` (P6), `write_off` (S7), an Aric referral table and the later stories' data are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case case fake | Case `RW-2026-001204` in `ANY_STATE`, `DEV_FLAGGED`, `DEV_WITH_OWNER` with the fraud team, `DEV_REROUTE`, `ROUTE_D6`; a case already closed | AC1, AC4, AC6 |
| rwb-case timers fake | The stage clock paused, the prescription clock running, the deviation service level running; a pause refused because no timer runs | AC4, AC6 |
| rwb-case pause and resume fake | The parent `CaseWorkflow` accepting the signal, and a signal to a workflow that has ended | AC4, AC6 |
| rwb-decision package fake | The DEVIATIONS route set at its version in force with R-UNI-08 and R-DEV-01 to R-DEV-21; an absent version | AC2, AC4, AC6 |
| rwb-decision decision-log fake | The record of each action with its rule version and the central confirmation; a ledger that does not confirm | AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-06 and SCR-08 answers for the case, in their form, saved, loading and list states | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the five consumed rows carry the placeholder until their owners confirm them (GAP-3058; ASM-5162, ASM-5163).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` on `/api/recovery/deviation/v1`; the case read and the timers read; one hop, 2 s |
| Kafka | 2 published, 1 consumed | `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) on `rwb.deviation.events.v1`; `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` |
| Temporal | 1 workflow, 2 activities and 1 boundary signal declared, 0 registered | `DeviationWorkflow`, `EvaluateDeviationRules` and `RecordAndApplyDeviation` on `rwb-deviation` |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no case, no row and no package. What it publishes is one OpenAPI 3.1 document, nine contract tables and seven fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the row and the state change. DP-13 moves the base and nothing else. DP-19 sits behind SCR-06 and SCR-08, whose screen models are the edge contract's. DP-04, DP-05, DP-09 and DP-16 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the case facts as consumed data and never views, the outbox and inbox as an absent library row, and Aric as out of scope rather than an adapter (GAP-3058; ASM-5162, ASM-5164, ASM-5165).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the outbox and inbox library `RWB-PLT-TE006-CON`, the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`, the access guard `RWB-PLT-E1037-CON` and `RWB-P4-E1037-CON`, and the integration adapter `RWB-P2-E1007-CON`. The five consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the `DeviationRequest`, `DeviationOutcome` and `Deviation` elements, the required list, the three enumerations and the three lengths of AC2, with the placeholder where a requiredness is unstated.
3. Publish the two events and their consumers of AC3 on the naming rule's names.
4. Record the two rwb-case rows, the boundary signal and the two rwb-decision rows of AC4 with their owner, their budget and their placeholders.
5. Record the decision-record element, the rights and the error envelope of AC5.
6. Publish the seven fakes of AC6 and the drift test.
7. Record the naming baseline, the absent trigger and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-deviation-v1.yaml`, the three elements, the contract README rows for the five consumed rows and their placeholders, the two events, and the seven fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the eight contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-06, SCR-08, the wave 4 harness and the consumers of the two events have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | The contract describes the information answer of the raise, which the app story returns with the deviation and the handler | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the row and the state change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The escalation of R-DEV-20 and the unmapped code of R-DEV-21 have no message ID in any source and are not bound to one here (GAP-3058).

### 15. Screens and states

The contract serves SCR-06 Raise deviation in its form and saved states (empty, loading, error and no access: Not specified in the source documents (CG-ALL-11529)) and SCR-08 Deviation queue in its loading and list states (empty, error and no access: Not specified in the source documents (CG-ALL-11530)), through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation and its state, rwb-case for the case and its route state and rwb-decision for the record; this baseline fixes the rwb-deviation answers only, and the composite route specification and the screen field lists belong to RWB-PLT-N001-CON. The refusal, not-recorded and re-routed states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-004-01 | AC1, AC4 | Contract | Case `RW-2026-001204` with the package in force; the contract half answers the raise, the outcome, the case read and the timers read |
| TC-E7-004-02 | AC5 | Contract | The decision-record stub stopped and the decision-record fake not confirming; the contract half answers the MSG-P7-003 path |
| TC-E7-004-03 | AC5 | Contract | A role without the Case record right U; the contract half answers the 403 with MSG-P4-002 |
| TC-E7-004-04 | AC5 | Contract | A forced decision record write failure described on every action; the contract half answers the refusal and the single envelope |
| TC-S8-E7004-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the `Idempotency-Key` of the create and the six error answers are present, and no third operation is declared |
| TC-S8-E7004-CON-02 | AC2, AC3 | Contract | The three elements validate with their properties, the required list, the three enumerations and the three lengths; the two events validate with their data and consumers |
| TC-S8-E7004-CON-03 | AC4 | Contract | The five consumed rows and their placeholders; the no-`v_ace_*`, no-`recovery_case`, no-`timer` and no-rule-row boundary |
| TC-S8-E7004-CON-04 | AC6 | Contract | The seven fakes match the document and a drifted fake fails the build |
| TC-S8-E7004-CON-05 | AC7 | Contract | The naming baseline, the tables owned, the absent job and the absence of an Aric operation and of a third event |
| TC-S8-E7004-CON-06 | AC7 | Contract | Boundary of 12.7: the five owned tables are the only tables declared; a sixth table or a foreign key to a table not owned fails the build |
| TC-S8-E7004-CON-07 | BR1 | Contract | The Deviation element declares only its ten properties, its required list and its enumerations; an extra property fails |
| TC-S8-E7004-CON-08 | BR2 | Contract | The decision record is declared as written before the row and the state change; a failed write leaves the row and the state unchanged |
| TC-S8-E7004-CON-09 | BR3 | Contract | The case and timer reads and the boundary signal are declared as consumed; a declared case, timer or pause property fails |
| TC-S8-E7004-CON-10 | BR4 | Contract | The package read and the decision-log read are declared; a rule, threshold or service level property fails |
| TC-S8-E7004-CON-11 | BR5 | Contract | No Aric operation is declared; an Aric path in the document fails |
| TC-S8-E7004-CON-12 | BR6 | Contract | The two events are declared; a third event or a second topic fails |
| TC-S8-E7004-CON-13 | BR7 | Contract | The create declares the Idempotency-Key and the patch declares none; a repeated outcome answers as a conflict |
| TC-S8-E7004-CON-14 | BR8 | Contract | Only the three published lists are declared; no enumeration for the deviation state is declared |
| TC-S8-E7004-CON-15 | BR9 | Contract | No personal data field in a schema, an example or a fake |
| TC-S8-E7004-CON-16 | BR10 | Contract | One REST base, one topic, one queue, one schema and one login; another service's base or topic fails |
| TC-S8-E7004-CON-17 | BR11 | Contract | A breaking schema change within major version 1 fails the build |
| TC-S8-E7004-CON-18 | BR12 | Contract | Only operations owned by rwb-deviation are listed; a consumed operation described as provided fails |
| TC-S8-E7004-CON-19 | BR13 | Contract | R-UNI-08 and R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21 are named and never declared |
| TC-S8-E7004-CON-20 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S8-E7004-CON-AC8) |

The four legacy cases are those of RWB-E7-004 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business behaviour of each is proved by RWB-S8-E7004-APP or by RWB-ITG-E7004-ITG. The legacy level maps to `Contract` here because the artefact under test is the contract. The twenty cases `TC-S8-E7004-CON-01` to `-20` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story.

The X4 integration harness environment, base hosts, fixture layout, synthetic keys, referral fixture shape and status words, evidence format and retention, and the pass or fail gate: Not specified in the source documents (GAP-0469).

### 17. Guardrails

- No business value in the contract: the codes, the raised-by list, the outcome list, the state names, the service level and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration invented here.
- No personal data in a schema, an example, an event or a fake: identifiers, a code, a date, a state and a rule version only, and every example is synthetic.
- The case and the two clocks stay with rwb-case and the rule rows with rwb-decision: the document declares no `v_ace_*` path, no `recovery_case` property, no `timer` property and no rule row (BR3, BR4).
- The money stays with rwb-payment and the write-off route with rwb-writeoff: the document declares no posting, no settlement and no write-off property.
- No Aric operation is invented: INT-31 is not available today and the referral is FEAT-ADM-13 in P4 (BR5).
- The schedule stays absent: this story registers no Schedule and creates no Quartz row and no job table.
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-deviation; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S8-001 | Each of X1 to X7 runs end to end with its own flow, approver, contact rules and return point; the contract fixes the two operations, the elements and the consumed rows on which the X4 flow is built (FSD S8 Requirements served) | The three elements, the two events and the five consumed rows | TC-E7-004-01, TC-S8-E7004-CON-01, TC-S8-E7004-CON-02, TC-S8-E7004-CON-03 |
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared | The outcome element and the two event data sets that carry the branch | TC-E7-004-01, TC-S8-E7004-CON-02 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-S8-E7004-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The two events and the consumed case event | TC-S8-E7004-CON-02, TC-S8-E7004-CON-05 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The two provided and the five consumed rows | TC-S8-E7004-CON-01, TC-S8-E7004-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S8-E7004-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-004, disposition Split (rework); feature FEAT-DVF-04 |
| Legacy criteria | AC2 of the legacy story, owned word for word by RWB-S8-E7004-APP, and AC1, owned word for word by RWB-ITG-E7004-ITG; this baseline copies none of them |
| Source text | Legacy RWB-E7-004; FSD S8 Deviation handling v3 A2.13, Screens and Requirements served; TSD S8 Deviation handling v2 T2, T3.1, T3.2, T4, T5.3, T6.1, T6.2 and T-A.1 and T-A.2; API Specification v5, `DeviationRequest`, `DeviationOutcome` and `Deviation`; Business Rules and Routing Logic v4 rows R-UNI-08 and R-DEV-01 to R-DEV-21; Event and Messaging Design v5, EV-06 and EV-07; Epics 3 to 8 Specification v3, FEAT-DVF-04 and INT-31 |
| Test cases | The four legacy cases as the contract half, and the five new contract cases TC-S8-E7004-CON-01 to -05 |
| Feature and screens | FEAT-DVF-04, SCR-06 Raise deviation, SCR-08 Deviation queue |
| Rules | R-UNI-08 and R-DEV-01, R-DEV-04, R-DEV-13, R-DEV-14, R-DEV-19, R-DEV-20 and R-DEV-21, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the two operations, the evaluation of the eight rules, the decision record, the `deviation` rows, the two events and the case-move answer: RWB-S8-E7004-APP.
- The legacy success criterion AC1 and the end-to-end proof across the real services: RWB-ITG-E7004-ITG.
- The case of record, its route states, the two clocks and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5163).
- The authoring, testing, approval and versioning of the DEVIATIONS route set, of the UNIVERSAL package and of the central ledger: rwb-decision (P7) (ASM-5162).
- The referral of INT-31 Aric and FEAT-ADM-13: P4's story in Epic 8 (ASM-5165).
- The write-off route of R-DEV-13 (S7), the route decision of R-DEV-19 (S1), and the contact-stop rules of rwb-comms for X1 to X3.
- The list of values of the deviation state and any clear or assignment operation: no source publishes them (ASM-5167, ASM-5168).
- The gateway-bff composite route and the screen field lists of SCR-06 and SCR-08: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

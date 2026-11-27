# RWB-S7-E6017-CON Route the population to the committee and schedule it - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6017-CON |
| Work type | CON (Contract) |
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
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the committee-routing step of rwb-writeoff, split from RWB-E6-017. It fixes the `write_off` element and its DF-FIN fields, the WRITEOFF state vocabulary, the consumed rwb-case state, move and queue rows, the rwb-deviation row, the rwb-decision package row, the decision-record element of DP-03, the rights, the fakes and the absence tests, on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). It provides no REST operation: the two operations of this legacy key are RWB-S7-E6013-APP's and RWB-S7-E6018-APP's, the plan's C and X rows are empty while the step consumes three services, and the meeting booking has no published element (GAP-3026; ASM-5034, ASM-5038, ASM-5039). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6017-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the committee-routing step of rwb-writeoff — the `write_off` element with its DF-FIN fields and the WRITEOFF state vocabulary, the consumed rwb-case state, move and queue answers, the consumed rwb-deviation deviation and handler route, the consumed rwb-decision package row, the decision-record element, the rights, the tables and the fakes**, so that **the app story, the SCR-27 fragment and the case and deviation answers build against one fixed, testable contract on Day 1, and a field, a state value, a consumed shape or an answer can never drift between rwb-writeoff, rwb-case, rwb-deviation and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares one element of this service and one read with a placeholder name, and it describes the boundaries the routing crosses. It declares no routing operation, no event and no queue table of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy routing of RWB-E6-017 crossed four boundaries at once — a case state, a committee queue, a deviation handler and a decision log — inside one process and one schema. The target splits them: rwb-case owns the case, its route states and the queues; rwb-deviation owns the deviation and its handler; rwb-decision owns the rule package and the ledger; rwb-writeoff owns the write-off row. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the `write_off` fields, the WRITEOFF state values, the case state read, the case-move answer, the queue item, the deviation read and route, the package row and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_writeoff`, login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules v1 §R4; context pack service row). It records that rwb-writeoff holds no grant on `rwb_case`, `rwb_deviation` or `rwb_decision`, so those three are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the plan's C and X rows are empty while the step consumes three services and most consumed operation names are unpublished (GAP-3026), the step provides no routing operation and its only read carries a placeholder (ASM-5038), the state values of the legacy criteria are read as the WRITEOFF state on `write_off.state` while the case route state is answered to rwb-case (ASM-5037), and the meeting booking has no calendar, column or Schedule element in any source (ASM-5039).

The wave and the date are the plan's and the legacy epic's: this key is EP06, wave 4, release 30 April 2027, and rwb-writeoff is created in wave 4, so the two agree and the date is copied unchanged and marked tentative (ASM-5035).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `write_off` is S7's, `recovery_case` and `queue` are P3's, `deviation` is S8's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's, `notice` is P6's. This document never declares another service's table or operation as its own.
- The rwb-case state, move and queue rows, the rwb-deviation rows and the rwb-decision package row are published with their fakes, so each consumed row names a real owner document; they are not in this story's dependency rows, which are None, and the absence is recorded (GAP-3026; ASM-5034).
- The WO rule package and its rows for R-WO-06, R-WO-10 and R-WO-11 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The two operations of this legacy key, API-S7-001 and API-S7-002, are outside this baseline and belong to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP (ASM-5038).
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step, record that it declares no routing operation, declare the one read behind SCR-27 with the placeholder, and name the two operations of the key as other stories'.
2. Fix the `write_off` element: the properties of DF-FIN-010 to DF-FIN-020 with their types, lengths, required flags and the state each value is declared against.
3. Fix the WRITEOFF state vocabulary of TSD S7 T4 and mark the values the table does not print with the placeholder.
4. Fix the consumed rwb-case rows: the state read, the case-move answer and the queue item, with the placeholder on the names the sources do not publish.
5. Fix the consumed rwb-deviation rows: the open-deviation read of codes X1 to X7 and the handler route.
6. Fix the consumed rwb-decision row: the WO package version in force with R-WO-06, R-WO-10 and R-WO-11 and the write-off committee limit.
7. Record the decision-record element of DP-03, written before the `write_off` row changes, and the meeting-booking element of the outcome.
8. Publish the contract tables of section 12, the rights and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shape, the error set, the rights, the drift between a fake and the document, the absence of an operation, of an event, of a Schedule and of a foreign table.
10. Tag the baseline and hand it to RWB-S7-E6017-APP, the SCR-27 fragment and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside the state vocabulary | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2, AC7 |
| X2 | A field is renamed or removed within major version 1, or a state value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | The document declares an operation, an event, a Schedule, a queue table or another service's object as its own | The absence test and the boundary test fail the build | None | AC1, AC7 |
| X6 | The rights of the read and of the consumed acts are not the ones TSD S7 T6.1 and T-A.1 declare | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | The meeting booking is declared with a date, a column or a calendar the sources do not give | The review fails the baseline; the element carries the placeholder | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-case, rwb-deviation and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the state values, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S7-E6017-APP, the SCR-27 fragment and the wave 4 harness on Day 1, and the rwb-case, rwb-deviation and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the committee-routing step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case and queue is P3, of deviation is S8 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides one read with a placeholder name and no routing operation, and records the key's two operations as other stories' (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the routing of the prepared pack to the committee
    Then it declares one GET read on the base /api/recovery/writeoff/v1 for the write-off element behind SCR-27, with its path, its operation ID and its element name Not specified in the source documents (GAP-3026; ASM-5038)
    Then it records POST /write-off-scans (API-S7-001) as RWB-S7-E6013-APP's and POST /write-offs/{writeOffId}/committee-decision (API-S7-002) as RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP (ASM-5038)
    Then the read declares the answers 400, 401, 403 with MSG-P4-002, 404 and 503 with one message ID per condition
    Then the absence test fails a build that declares a routing operation, a second base or a second topic

  Scenario: AC2 The write_off element and the WRITEOFF state vocabulary are declared (new, D-RCV-60)
    Given the write-off section of the baseline
    When it is compared with TSD S7 T3.0, T3.1 and T4 and with the API Specification's WriteOff element
    Then the write_off element declares the properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then id, case_id, amount, tax_criteria_met and recovered_after are required and the other six are optional, responsibility_center, cost_center and gl_product are strings of at most 10 characters, amount and recovered_after are numeric(18,2) and the two dates are dates
    Then state is declared as the standard record column of TSD S7 T3.0 with the WRITEOFF values SCAN_DUE, SCAN_HELD, POPULATION_PROPOSED, PACK_PREPARED, PACK_INCOMPLETE, WITH_COMMITTEE, CASE_REMOVED_BY_TEAM, ESCALATED_TO_CREDIT_COMMITTEE, APPROVED, RETURNED_TO_PURSUE, DEFERRED, POSTING_PENDING, POSTED, POSTING_REJECTED, WRITEOFF_EXCEPTION, PROVISION_RELEASED, RETENTION_RUNNING and CASE_CLOSED, and the values of the 27-state machine that T4 does not print carry the placeholder (GAP-3026; ASM-5037)
    Then the element records that committee_date is the committee approval date and is written by RWB-S7-E6018-APP, and that the meeting booking has no column of its own (GAP-3026; ASM-5039)

  Scenario: AC3 The consumed rwb-case state, move and queue rows are declared (new, D-RCV-60)
    Given the consumed rows and the case boundary of the baseline
    When they are compared with rwb-case as the owner of recovery_case and queue
    Then the case state read is declared as consumed from P3 rwb-case on the GET /cases/{caseId} family, with the case reference and the state of the write-off stage
    Then the case-move answer is declared as consumed from P3 with the move WITH_COMMITTEE or CASE_REMOVED_BY_TEAM carrying the rule ID and its version, and its operation name is Not specified in the source documents (GAP-3026; ASM-5034)
    Then the committee-queue assignment is declared as consumed from P3 with the queue item and the meeting date, its name is Not specified in the source documents, and the queue table of DF-WRK-001 to DF-WRK-008 is named as P3's and never declared as this service's (GAP-3026; ASM-5034)
    Then the document declares no recovery_case property, no queue property and no write of a case or queue row from rwb-writeoff

  Scenario: AC4 The consumed rwb-deviation and rwb-decision rows are declared (new, D-RCV-60)
    Given the consumed rows of the deviation and the rule package
    When they are compared with rwb-deviation as the owner of deviation and with rwb-decision as the owner of rule_row
    Then the open-deviation read is declared as consumed from S8 rwb-deviation with the case reference and deviation_open of codes X1 to X7, and its name is Not specified in the source documents (GAP-3026; ASM-5034)
    Then the deviation-handler route is declared as consumed from S8 with the held case, the deviation code and the reason, and its name is Not specified in the source documents
    Then the WO rule package version in force is declared as consumed from P7 rwb-decision with the rows R-WO-06, R-WO-10 and R-WO-11 and the write-off committee limit, and its operation name is Not specified in the source documents (GAP-3026; ASM-5034, ASM-5005)
    Then the document declares no deviation property, no rule_row property and no ledger entry of its own, and records that DP-04 and DP-05 are not in this key's pattern set
    Then each consumed row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The rights, the roles and the scope are fixed on the read and on the consumed acts (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T6.1 and T-A.1 and with the legacy permission rows
    Then the read declares Write-off and posting right R with the scope applied, RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, and RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA
    Then the document records the legacy A holders RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the legacy C holders RW-WRITEOFF and RW-CREDITAD, and declares no A right on an operation of this story (ASM-5038)
    Then the document records that the routing runs under the service identity and that FSD S7 A2.5.3.3 names no primary person for it
    Then the document declares that an act taken on API-S7-002 is the committee decision story's and is consumed, never provided

  Scenario: AC6 The decision-record element, the meeting booking and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the element it serves
    Then one decision record is declared per rule outcome with the case reference, the write-off reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move, the queue item and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the write_off row changes, and a failed write leaves the row unchanged with MSG-P7-003
    Then the meeting booking is declared as an attribute of the record and of the queue item, with the meeting date Not specified in the source documents (GAP-3026; ASM-5039)
    Then the rwb-case fake answers the three case states, an accepted and a refused move and a queue item, the rwb-deviation fake answers an open deviation of code X1 to X7 and no deviation and a handler route, and the rwb-decision fake answers the package at its version with the limit above and below the amount
    Then the rwb-writeoff fake answers the write-off WO-2027-000318 of case RC-2027-000712 with its state and its record reference
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1, the queue is rwb-writeoff and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, queue, deviation, rule_row, decision_log_entry, document, notice, proceeds and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names WriteOffApproved (EV-24) as RWB-S7-E6018-APP's (ASM-5036)
    Then the document declares no Schedule, no Quartz row and no shared job table, and names JOB-16 as RWB-S7-E6013-APP's (ASM-5039)
    Then the document records that the plan's C and X rows are empty although the step consumes three services, and that the S7 module files were read from the extract folder (GAP-3026; ASM-5034)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6017-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off row and its state are rwb-writeoff's, and the contract declares their fields and state values on the `write_off` element only | Context pack ownership row `write_off`; TSD S7 T3.0 and T3.1; DP-01 |
| BR2 | The decision record is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy RWB-E6-017 AC1 and AC4 |
| BR3 | The case, its route states and the queues stay with rwb-case: the contract declares the state read, the move answer and the queue item as consumed and declares no `recovery_case` and no `queue` property | Context pack ownership rows; legacy Data table; ASM-5034 |
| BR4 | The deviation and its handler stay with rwb-deviation: the contract declares the read and the route as consumed and declares no deviation property | Business Rules and Routing Logic v4 R-WO-06; ASM-5034 |
| BR5 | The rule package and the ledger stay with rwb-decision: the contract names R-WO-06, R-WO-10 and R-WO-11 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5005 |
| BR6 | No event belongs to this step: the contract declares no published event and no consumed event, and names `WriteOffApproved` (EV-24) as the approval story's | Event and Messaging Design v5 EV-24; ASM-5036 |
| BR7 | No Schedule belongs to this step: the meeting booking is an attribute of the record and of the queue item, and JOB-16 is the scan story's | Batch and Scheduling Design v5 JOB-16; ASM-5039 |
| BR8 | The state vocabulary is closed: the WRITEOFF values are published as an enumeration of `state` and no state value is a constant of the code | TSD S7 T3.0 and T4; ASM-5037 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, an amount, a code and a rule version only | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules v1 §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes (BACKWARD compatibility) |
| BR12 | The document declares only operations owned by rwb-writeoff: the one read behind SCR-27 with its placeholder name, and no routing operation, because the routing runs on the prepared pack | Ownership rows; DP-11; ASM-5038 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the state vocabulary, the consumed rows, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-27 fragment, the wave 4 harness and the rwb-case, rwb-deviation and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a state value is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence and boundary tests of AC1 and AC7 fail: an operation, an event, a Schedule, a queue table or a foreign table | In review |

The WRITEOFF machine the document describes is the app story's: `PACK_PREPARED`, `PACK_INCOMPLETE`, `POPULATION_PROPOSED`, `WITH_COMMITTEE` and `CASE_REMOVED_BY_TEAM` are the values this step reads and writes, and the case route state that rwb-case holds is answered, not declared here. This baseline fixes the vocabulary and moves no write-off and no case (ASM-5037).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the consumed rows |
| Consuming teams (the app story, the SCR-27 fragment, the wave 4 harness and the owners of rwb-case, rwb-deviation and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product`, `recovered_after` |
| Required flags | `id`, `case_id`, `amount`, `tax_criteria_met` and `recovered_after` required; the other six optional, as the API Specification's `WriteOff` element declares them |
| State | `state` of TSD S7 T3.0 against the WRITEOFF vocabulary of T4, published as an enumeration and read as reference data |
| Record reference | `decision_log_id` holds the identifier the local decision-record library returns, and the P7 ledger entry id is not stored here (ASM-5040) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Consumed shapes | The case state, move and queue rows of P3, the deviation read and route of S8, and the package row of P7, each declared as consumed and faked |
| Not declared here | `recovery_case`, `queue` and `timer` (P3), `deviation` (S8), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), every `v_ace_*` view (P1), and the two operations API-S7-001 and API-S7-002 (other stories of this service) |
| Consumed fields with no source | The operation names of the case move, the queue item, the deviation read and route and the package read, the values of the WRITEOFF table that T4 does not print, and the meeting date: Not specified in the source documents (GAP-3026; ASM-5034, ASM-5037, ASM-5039) |

The field-level formats of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This baseline declares one read, with a placeholder name, and no routing operation.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-3026; ASM-5038) | The `write_off` element of section 11 with its `state`, its `decision_log_id` and the meeting booking | Write-off and posting, right R, scope applied | Not declared |

The path, the operation ID and the element name carry the placeholder because the API Specification v4 gives the service only `/write-off-scans` (API-S7-001) and `/write-offs/{writeOffId}/committee-decision` (API-S7-002). Those two are other stories' of the same service: the first is RWB-S7-E6013-APP's, and the second carries the approve outcome at RWB-S7-E6018-APP and the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. The read answers 400, 401, 403 with MSG-P4-002, 404 and 503 on the base above, and it is the leg of the gateway-bff composite route that SCR-27 renders (DP-19). A build that declares a routing operation on this base fails the absence test of AC1 (GAP-3026; ASM-5038).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the state of the write-off stage; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3026; ASM-5034)) | rwb-case (P3) | P3 rwb-case | The move `WITH_COMMITTEE` or `CASE_REMOVED_BY_TEAM` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The committee-queue assignment (operation name Not specified in the source documents (GAP-3026; ASM-5034)) | rwb-case (P3) | P3 rwb-case | The queue item of the write-off committee queue with the meeting date; the `queue` rows of DF-WRK-001 to DF-WRK-008 are P3's; faked |
| The open-deviation read and the handler route (operation names Not specified in the source documents (GAP-3026; ASM-5034)) | `/api/recovery/deviation/v1` | S8 rwb-deviation | `deviation_open` of codes X1 to X7, and the route of the held case to the deviation handler; faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3026; ASM-5034, ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows R-WO-06, R-WO-10 and R-WO-11 with the write-off committee limit; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3026 with ASM-5034 and ASM-5005.

#### 12.3 Events published

None. The service owns `WriteOffApproved` (EV-24) on topic `rwb.writeoff.events.v1` with payload `writeOffId`, `caseId` and `amount`, and it is the committee's approval, which RWB-S7-E6018-APP publishes. This baseline therefore declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5036).

#### 12.4 Events consumed

None. No source gives rwb-writeoff a consumed event for this step: the pack arrives inside the same service and the case and deviation facts arrive on their owners' contracts. This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one (ASM-5036).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the routing branch; its input, its signals and its outcome for the parent are declared, not built |
| The routing branch of `WriteOffWorkflow` | Workflow branch | `rwb-writeoff` | The step from the prepared pack to the committee queue or the deviation handler: R-WO-06, then R-WO-10 or R-WO-11, the record, the row, the queue item and the stage outcome |
| `routePackToCommittee` | Activity, the one step | `rwb-writeoff` | The case, the write-off and the package answer in; the rule ID with its version, the state, the record reference, the queue item and the case move out |

No child workflow of this service exists in this step and the committee's act is not run here: it is the `ApprovalWorkflow` of the kit on the P7 queue, started by RWB-S7-E6018-APP. The activity name is a target design choice and the trigger is read as the arrival of the prepared pack for a write-off in `PACK_PREPARED`, because the FSD declares the scan as the module's only background event (FSD S7 A2.5.4.4). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the prepared pack; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-16, the monthly write-off scan on the third working day on the ACE batch-complete record for ALS, is RWB-S7-E6013-APP's. The monthly committee meeting the step books into has no published calendar, no `write_off` column and no Schedule element, and the meeting date carries the placeholder (GAP-3026; ASM-5039).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its DF-FIN fields, its `state` and its record reference; the table the element answers from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated pack and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library for the stories that publish; no row of it belongs to this step |

`recovery_case`, `queue` and `timer` (P3), `deviation` (S8), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), `proceeds` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers or rule versions of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state, move and queue fake | The states `PACK_PREPARED`, `POPULATION_PROPOSED` and `WITH_COMMITTEE` of case `RC-2027-000712`; an accepted and a refused move; a queue item accepted and a queue that refuses an item outside the committee queue; no answer beyond 2 s | AC3, AC6 |
| rwb-deviation fake | An open deviation of code X1 to X7, no open deviation, a handler route accepted and a route refused; no answer beyond 2 s | AC4, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-06, R-WO-10 and R-WO-11 and the write-off committee limit above and below the amount | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-writeoff write-off fake | The write-off `WO-2027-000318` of case `RC-2027-000712` with its amount, its tax criteria flag, its state and its record reference | AC2, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for the write-off, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished operation names and the meeting date are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3026; ASM-5034, ASM-5039).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | The write-off read behind SCR-27 on `/api/recovery/writeoff/v1`, with its path and operation ID on the placeholder; the rwb-case state read, the case-move answer and the queue item, the rwb-deviation read and route, and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval story's; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch and 1 activity declared, 0 registered | `WriteOffWorkflow` and its routing branch on `rwb-writeoff`, with its `routePackToCommittee` activity; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the pack documents are rwb-document's (P5) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no write-off, no case, no deviation and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the read and six fakes.

**Deliverables.** The additive document `openapi/rwb-writeoff-v1.yaml`, the `write_off` element and the state enumeration, the contract README rows for the five consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the row changes, on the shared `rwb.decision-record.v1`. DP-13 moves the base of the key's two operations and of the read behind SCR-27; this step owns no routing operation. DP-19 is behind SCR-27, whose screen model is the edge contract's, and this baseline fixes the write-off answer only. No other pattern is claimed: the case, the queue, the deviation and the package are consumed contracts, so DP-04, DP-05, DP-09 and DP-10 stay off this table and their absence is recorded in the registers (GAP-3026; ASM-5005, ASM-5036, ASM-5039).

**Build steps**

1. Record the absence of a routing operation, the placeholder read behind SCR-27 and the two key operations as other stories', with the absent-operation test of AC1.
2. Write the `write_off` element, its required flags, its lengths and its state enumeration of AC2, with the unprinted state values and the meeting-booking note.
3. Record the rwb-case rows of AC3 with their owner, their budget and the placeholder.
4. Record the rwb-deviation and rwb-decision rows of AC4 with their owners and the placeholder.
5. Record the rights, the roles and the scope of AC5, with the legacy A and C holder disposition.
6. Record the decision-record element and the meeting-booking attribute of AC6 and validate them against the library schema.
7. Publish the six fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the SCR-27 fragment and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate, so no path of this step raises it | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a body is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the read declares, and a role without the right of a consumed act tries it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the write-off row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The pack's source data is stale after a late or failed ACE batch (VR-S7-005-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The first four message IDs are those of the legacy message set of this key and MSG-P1-001 is the message of VR-S7-005-1 in FSD S7 A2.5.3.1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added. MSG-S7-001 is carried because it is in the message set of this feature, and the check itself belongs to the scan story of this service.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its scan, proposed, in-committee, approved and removed states, through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off and its routing state, rwb-case for the case, its route state and the committee queue, and rwb-decision for the decision records; this baseline fixes the rwb-writeoff answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The population operation behind the list is a placeholder, because no source publishes it (ASM-5038). The refused, not-recorded and stale states of the app story read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-017-01 | AC1, AC2 | Contract | The prepared pack of write-off `WO-2027-000318`; the contract half answers the element, its state and the absent routing operation |
| TC-E6-017-02 | AC2, AC3 | Contract | R-WO-11 with the limit above the amount; the contract half answers the state value, the record reference, the queue item and the `WITH_COMMITTEE` move shape |
| TC-E6-017-03 | AC3, AC4 | Contract | An open deviation of code X1 to X7; the contract half answers the deviation row, the handler route and the `CASE_REMOVED_BY_TEAM` move shape |
| TC-E6-017-04 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E6-017-05 | AC5 | Contract | A role without the Write-off and posting right; the contract half answers the 403 with MSG-P4-002 and the rights of the read |
| TC-E6-017-06 | AC6, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the record path and the absence tests |
| TC-S7-E6017-CON-01 | AC1 | Contract | The document validates; no routing operation, no second base and no second topic are declared, and the two operations of the key are named as other stories' |
| TC-S7-E6017-CON-02 | AC2 | Contract | The `write_off` element validates with its eleven properties, its five required flags and the WRITEOFF state enumeration |
| TC-S7-E6017-CON-03 | AC3 | Contract | The case state, move and queue rows and their placeholders; the no-`recovery_case` and no-`queue` boundary |
| TC-S7-E6017-CON-04 | AC4 | Contract | The deviation read and route and the package row with their placeholders; no deviation property, no rule row and no ledger entry |
| TC-S7-E6017-CON-05 | AC5 | Contract | RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA, and the legacy A and C holders are recorded |
| TC-S7-E6017-CON-06 | AC6 | Contract | The six fakes match the document and a drifted fake fails the build |
| TC-S7-E6017-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |

The six legacy cases are the legacy cases of RWB-E6-017 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6017-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S7-E6017-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the write-off committee limit, the deviation codes, the meeting calendar, the state values and the rule rows stay package values, reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, an amount, a code and a rule version only; every example is synthetic.
- The case, its route states and the queues stay with rwb-case, the deviation with rwb-deviation, and the package and the ledger with rwb-decision: the document declares no `recovery_case`, `queue`, `deviation`, `rule_row` or ledger property and no row write of any of them (BR3, BR4, BR5).
- This step owns no routing operation: the document declares one read behind SCR-27 with its path and operation ID on the placeholder, and records the two operations of the key as other stories' (BR12, ASM-5038).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The document lists only operations owned by rwb-writeoff and describes a consumed element as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly (Must, E6); the contract fixes the state, the record reference and the answers on which the routing is built, and the plan and the FSD carry no requirement row for the routing step (GAP-3026; ASM-5038) | The `write_off` element, the state enumeration and the consumed rows | TC-E6-017-01, TC-E6-017-02, TC-S7-E6017-CON-01, TC-S7-E6017-CON-02 |
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (Must, E6); the contract fixes the record element the routing writes and the decision act it consumes | The decision-record element | TC-S7-E6017-CON-06 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6017-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S7-E6017-CON-03, TC-S7-E6017-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and the ledger entry of P7 | TC-S7-E6017-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-017, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S7-E6017-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the seven new contract cases TC-S7-E6017-CON-01 to -07 |
| Feature and screens | FEAT-WOF-05, SCR-27 Write-off proposal |
| Rules | R-WO-06, R-WO-10 and R-WO-11, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-WO-06, R-WO-10 and R-WO-11, the decision record, the state, the record reference, the queue item and the case-move answer: RWB-S7-E6017-APP.
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The pack, its documents, its carried provision and its check: RWB-S7-E6015-APP; the removal by the team under R-WO-07: RWB-S7-E6016-APP.
- The committee decision act, API-S7-002, and the approve, reject and defer outcomes: RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP (ASM-5038).
- The case of record, its route states, the queue table and the queue assignment: rwb-case (P3), whose answers this baseline declares as consumed and faked (GAP-3026).
- The deviation facts, the codes X1 to X7 and the deviation handler: rwb-deviation (S8) (GAP-3026).
- The WO rule package, its version and the ledger: rwb-decision (P7) (ASM-5005).
- The freshness of the source data and the `v_ace_batch_status` read: rwb-source-data (P1) (ASM-5041).
- The pack documents and their custody: rwb-document (P5); the notices to customers: rwb-comms (P6).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

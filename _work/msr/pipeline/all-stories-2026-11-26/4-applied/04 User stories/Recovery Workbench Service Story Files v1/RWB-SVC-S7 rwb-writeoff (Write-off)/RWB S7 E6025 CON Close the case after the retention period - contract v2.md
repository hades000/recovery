# RWB-S7-E6025-CON Close the case after the retention period - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6025-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-025 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the closure step of rwb-writeoff, split from RWB-E6-025. It fixes the `write_off` element and its DF-FIN fields, the two state values the closure writes, the consumed rwb-case state, case-move and timer rows, the consumed rwb-decision package row, the placement read, the closing-entry element of DP-03, the rights, the fakes and the absence tests, on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). It provides no REST operation, because the two operations of this legacy key are other stories' of the same service, the closure is unattended, and the plan's C and X rows are empty while the step consumes two services; the retention period has no value in any source and the placement read and the closing amounts have no published element (GAP-3042; ASM-5098, ASM-5101, ASM-5102, ASM-5103). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6025-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the closure step of rwb-writeoff — the `write_off` element with its DF-FIN fields, the two state values the closure writes, the consumed rwb-case state, case-move and timer answers, the consumed rwb-decision package row, the placement read, the closing-entry element, the rights, the tables and the fakes**, so that **the app story, the SCR-27 fragment and the case, timer and package answers build against one fixed, testable contract on Day 1, and a field, a state value, a consumed shape or a closing amount can never drift between rwb-writeoff, rwb-case and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, one entry and the boundaries the closure crosses. It declares no operation, no event and no queue table of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy closure of RWB-E6-025 crossed four boundaries at once — a case state, a case timer, a document retention class and a decision log — inside one process and one schema. The target splits them: rwb-case owns the case, its route states and the timers; rwb-document owns the retention class of a document; rwb-decision owns the rule package and the ledger; rwb-writeoff owns the write-off row and the closing entry. Each boundary is a contract another team builds against, so each has to be fixed before the app story starts: the `write_off` fields, the two state values, the case state read, the two moves, the timer stop, the package row and the entry's amounts.

The baseline also fixes the naming the checks require: schema `rwb_writeoff`, login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules v1 §R4; context pack service row). It records that rwb-writeoff holds no grant on `rwb_case`, `rwb_document` or `rwb_decision`, so those three are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the plan's C and I rows are empty while the step consumes two services and most consumed operation names are unpublished (GAP-3042; ASM-5098), the retention period has no value in any source and is open under DL26 so it is published as reference data with a placeholder (ASM-5102), the placement record of `PLACED_WITH_AGENCY` has neither a column here nor a published owner operation and the connection matrix gives S7 no row to rwb-partner (ASM-5101), and the closing entry's cash recovered and loss have no column of `write_off` and no published element (ASM-5103).

The wave and the date are the plan's and the legacy epic's: this key is EP06, wave 4, release 30 April 2027, and rwb-writeoff is created in wave 4, so the two agree and the date is copied unchanged and marked tentative (ASM-5035).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `write_off` is S7's, `recovery_case` and `timer` are P3's, `rule_row` and `decision_log_entry` are P7's, `partner` is S9's, `document` is P5's. This document never declares another service's table or operation as its own.
- The rwb-case state, move and timer rows and the rwb-decision package row are published with their fakes, so each consumed row names a real owner document; they are not in this story's dependency rows, which are None, and the absence is recorded (GAP-3042; ASM-5098).
- The WO rule package and its rows for R-WO-36, R-WO-47 and R-WO-48 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The retention period and the retention classes are reference data with their version; no source sets a period, so the element carries a placeholder and never a default (GAP-3042; ASM-5102).
- The `write_off` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The two operations of this legacy key, API-S7-001 and API-S7-002, are outside this baseline and belong to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to RWB-S7-E6020-APP.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step and record that it declares no operation for it, with the two operations of the key named as other stories'.
2. Fix the `write_off` element: the properties of DF-FIN-010 to DF-FIN-020 with their types, lengths, required flags and the state each value is declared against.
3. Fix the state values the closure writes, `RETENTION_RUNNING` and `CASE_CLOSED`, against the WRITEOFF vocabulary already published by RWB-S7-E6017-CON, and record that TSD S7 T4 prints neither rule's row.
4. Fix the consumed rwb-case rows: the state read, the two moves and the timer read and stop, with the placeholder on the names the sources do not publish.
5. Fix the consumed rwb-decision row: the WO package version in force with R-WO-36, R-WO-47 and R-WO-48.
6. Fix the placement read of `PLACED_WITH_AGENCY`, its `ends_at` and its `recovered_amount`, and record that no source publishes it (ASM-5101).
7. Record the closing-entry element of DP-03, written before the `write_off` row changes, with cash recovered and loss as its attributes and the retention period as reference data with a placeholder (ASM-5102, ASM-5103).
8. Publish the contract tables of section 12, the rights and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shape, the error set, the rights, the drift between a fake and the document, the absence of an operation, of an event, of a Schedule and of a foreign table.
10. Tag the baseline and hand it to RWB-S7-E6025-APP, the SCR-27 fragment and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside the state vocabulary | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2, AC7 |
| X2 | A field is renamed or removed within major version 1, or a state value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | The document declares an operation, an event, a Schedule, a queue table or another service's object as its own | The absence test and the boundary test fail the build | None | AC1, AC7 |
| X6 | The rights of the read and of the consumed acts are not the ones TSD S7 T6.1 and T-A.1 declare, or the unattended identity is given a user right | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | A period, an amount or a retention class is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC2, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the state values, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S7-E6025-APP, the SCR-27 fragment and the wave 4 harness on Day 1, and the rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the closure step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case and timer is P3, of partner is S9, of document is P5 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no operation for the closure and records the key's two operations as other stories' (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the closure of a case after its retention period
    Then it records POST /write-off-scans (API-S7-001) as RWB-S7-E6013-APP's and POST /write-offs/{writeOffId}/committee-decision (API-S7-002) as RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP (ASM-5098)
    Then the read of the closure state behind SCR-27 carries the placeholder, with an error set of 400, 401, 403 with MSG-P4-002, 404 and 503 and one message ID per condition (GAP-3042; ASM-5098)
    Then the absence test fails a build that declares a closure operation, a second base or a second topic

  Scenario: AC2 The write_off element and the two state values of the closure are declared (new, D-RCV-60)
    Given the write-off section of the baseline
    When it is compared with TSD S7 T3.0, T3.1 and T4, with the API Specification's WriteOff element and with the state enumeration of RWB-S7-E6017-CON
    Then the write_off element declares the properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then id, case_id, amount, tax_criteria_met and recovered_after are required and the other six are optional, responsibility_center, cost_center and gl_product are strings of at most 10 characters, amount and recovered_after are numeric(18,2) and the two dates are dates
    Then state is declared as the standard record column of TSD S7 T3.0 against the WRITEOFF vocabulary of RWB-S7-E6017-CON, and the closure writes RETENTION_RUNNING and CASE_CLOSED and no other value
    Then the element records that R-WO-36 and R-WO-47 are not printed in TSD S7 T4 and are taken from the Business Rules and Routing Logic v4, that the retention period is reference data with its version and Not specified in the source documents (GAP-3042; ASM-5100, ASM-5102), and that the loss and the cash recovered are attributes of the closing entry and not columns of the element (ASM-5103)

  Scenario: AC3 The consumed rwb-case state, move and timer rows are declared (new, D-RCV-60)
    Given the consumed rows and the case boundary of the baseline
    When they are compared with rwb-case as the owner of recovery_case and timer
    Then the case state read is declared as consumed from P3 rwb-case on the GET /cases/{caseId} family, with the case reference and the state of the write-off stage at PLACED_WITH_AGENCY, RETENTION_RUNNING and CASE_CLOSED
    Then the case-move answer is declared as consumed from P3 with the moves RETENTION_RUNNING and CASE_CLOSED carrying the rule ID, its version and the closing amounts, and its operation name is Not specified in the source documents (GAP-3042; ASM-5098)
    Then the timer read and stop is declared as consumed from P3 with the timer item of DF-WRK-027 to DF-WRK-036, its name is Not specified in the source documents, and the timer table is named as P3's and never declared as this service's (GAP-3042; ASM-5098)
    Then the document declares no recovery_case property, no timer property and no write of a case or timer row from rwb-writeoff

  Scenario: AC4 The consumed rwb-decision package row and the placement read are declared (new, D-RCV-60)
    Given the consumed rows of the rule package and of the placement
    When they are compared with rwb-decision as the owner of rule_row and with the ownership rows of the context pack
    Then the WO rule package version in force is declared as consumed from P7 rwb-decision with the rows R-WO-36, R-WO-47 and R-WO-48, and its operation name is Not specified in the source documents (GAP-3042; ASM-5005)
    Then the placement read is declared as consumed with the placement of PLACED_WITH_AGENCY, its ends_at and its recovered_amount, its operation name and its owner are Not specified in the source documents, and the document records that the connection matrix gives S7 no row to rwb-partner (S9) (GAP-3042; ASM-5101)
    Then the document declares no rule_row property, no ledger entry and no partner property of its own, and records that DP-04 and DP-05 are not in this key's pattern set
    Then each consumed row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The rights, the roles and the unattended identity are fixed on the read and on the consumed acts (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T6.1 and T-A.1 and with the legacy permission rows
    Then the read declares Write-off and posting right R with the scope applied, RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, and RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA
    Then the document records that the closure runs under the service identity and that FSD S7 A2.13.3.3 names no primary person for it, while the legacy permission rows hold right A for RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and right C for RW-WRITEOFF and RW-CREDITAD
    Then the document declares no A right on an operation of this story and records that an act taken on API-S7-002 is the committee decision story's and is consumed, never provided (ASM-5098)
    Then a build that gives the unattended identity a user right fails the access test

  Scenario: AC6 The closing-entry element and the fakes answer the document (new, D-RCV-60)
    Given the entry section and the fakes of the baseline
    When each is compared with the library schema and with the element it serves
    Then one closing entry is declared per closure with the case reference, the write-off reference, the rule ID, the package version in force, the inputs reference, cash recovered, loss, the from and to state and the closed-at time
    Then the entry is written through the library on the shared rwb.decision-record.v1 before the write_off row changes, and a failed write leaves the row unchanged with MSG-P7-003
    Then the retention period and the retention class are declared as reference data with their version and no value, and the two amounts carry the placeholder where no source binds them to a column (GAP-3042; ASM-5102, ASM-5103)
    Then the rwb-case fake answers the three case states, the two moves accepted and refused, and open and closed timers, the rwb-decision fake answers the package at its version with the three rows, and the placement fake answers a term passed with nothing recovered and a term passed with an amount recovered
    Then the rwb-writeoff fake answers the write-off WO-2027-000402 of case RC-2026-000884 with its state and its record reference
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1, the queue is rwb-writeoff and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, partner, document, rule_row, decision_log_entry, notice, payment and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names WriteOffApproved (EV-24) as RWB-S7-E6018-APP's and RWB-S7-E6021-APP's (ASM-5099)
    Then the document declares no Schedule, no Quartz row, no shared job table and no batch table, records that the retention wait is a durable timer of the workflow, and names JOB-16 as RWB-S7-E6013-APP's (ASM-5100)
    Then the document records that the plan's C and I rows are empty although the step consumes two services, and that the S7 module files were read from the extract folder (GAP-3042; ASM-5098)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6025-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off row and its state are rwb-writeoff's, and the contract declares their fields and the two closure values on the `write_off` element only | Context pack ownership row `write_off`; TSD S7 T3.0 and T3.1; DP-01 |
| BR2 | The closing entry is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy RWB-E6-025 AC1 and AC4 |
| BR3 | The case, its route states and the timers stay with rwb-case: the contract declares the state read, the two moves and the timer stop as consumed and declares no `recovery_case` and no `timer` property | Context pack ownership rows; legacy Data table; ASM-5098 |
| BR4 | The rule package and the ledger stay with rwb-decision: the contract names R-WO-36, R-WO-47 and R-WO-48 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5005 |
| BR5 | The placement and the agency record stay with their owner: the contract declares the read as consumed with the placeholder and declares no partner property | Legacy Data table (`partner`, DF-PRT-001 to DF-PRT-007); context pack connection matrix; ASM-5101 |
| BR6 | No event belongs to this step: the contract declares no published event and no consumed event, and names `WriteOffApproved` (EV-24) as the approval and posting stories' | Event and Messaging Design v5 EV-24; ASM-5099 |
| BR7 | No Schedule belongs to this step: the retention wait is a durable timer of the workflow and JOB-16 is the scan story's | Batch and Scheduling Design v5 JOB-16; context pack Temporal slides; ASM-5100 |
| BR8 | The state vocabulary is closed: the two closure values are published against the enumeration RWB-S7-E6017-CON already declares, and no state value is a constant of the code | TSD S7 T3.0 and T4; Business Rules and Routing Logic v4 state table |
| BR9 | No personal data in a schema, an example or a fake: identifiers, an amount, a code, a class and a rule version only | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules v1 §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes (BACKWARD compatibility) |
| BR12 | The document declares only operations owned by rwb-writeoff, and this step owns none; a consumed element is described as consumed and faked, never as provided | Ownership rows; DP-11; ASM-5098 |
| BR13 | No period, no amount and no class is a schema default or a constant: the period is reference data with a version and the two amounts are entry attributes | FSD S7 BR-S7-013; Program BRD v4 NFR-031; ASM-5102, ASM-5103 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the two state values, the consumed rows, the entry and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-27 fragment, the wave 4 harness and the rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a state value is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence and boundary tests of AC1 and AC7 fail: an operation, an event, a Schedule, a queue table or a foreign table | In review |

The WRITEOFF machine the document describes is the app story's: `PLACED_WITH_AGENCY`, `RETENTION_RUNNING` and `CASE_CLOSED` are the values this step reads and writes, and the case route state that rwb-case holds is answered, not declared here. This baseline fixes the vocabulary and moves no write-off and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the consumed rows |
| Consuming teams (the app story, the SCR-27 fragment, the wave 4 harness and the owners of rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |
| Compliance and Legal | Confirm the retention period and the retention classes the element names as reference data, which are open under DL26 |

The per-service login behind the security scheme of the document is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product`, `recovered_after` |
| Required flags | `id`, `case_id`, `amount`, `tax_criteria_met` and `recovered_after` required; the other six optional, as the API Specification's `WriteOff` element declares them |
| State | `state` of TSD S7 T3.0 against the WRITEOFF vocabulary; this step declares the two values `RETENTION_RUNNING` and `CASE_CLOSED` and no other |
| Record reference | `decision_log_id` holds the identifier the local decision-record library returns, and the P7 ledger entry id is not stored here (ASM-5040) |
| Closing entry | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03), with cash recovered and loss as attributes and no column of `write_off` for either (ASM-5103) |
| Retention period and class | Reference data and parameters with a version; the period value and the class list are Not specified in the source documents (GAP-3042; ASM-5102) |
| Consumed shapes | The case state, the two moves and the timer rows of P3, the package row of P7 and the placement facts, each declared as consumed and faked |
| Not declared here | `recovery_case` and `timer` (P3), `partner` (S9), `document` (P5), `rule_row` and `decision_log_entry` (P7), `notice` (P6), `payment` (P8), every `v_ace_*` view (P1), and the two operations API-S7-001 and API-S7-002 (other stories of this service) |
| Consumed fields with no source | The operation names of the case read, the case-move answer, the timer read and stop, the package read and the placement read, and the period and the class values: Not specified in the source documents (GAP-3042; ASM-5098, ASM-5101, ASM-5102) |

The field-level formats of the added elements are settled in the baseline review; this story fixes the element names, the two state values of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This step provides no operation and this baseline declares none for it, because the closure runs unattended from a durable timer. The two operations of this legacy key are other stories' of the same service: `POST /write-off-scans` (API-S7-001, right C) is RWB-S7-E6013-APP's, and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) carries the approve outcome at RWB-S7-E6018-APP and the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. The read of the closure state behind SCR-27 is Not specified in the source documents and carries the placeholder (GAP-3042; ASM-5098). A build that declares a closure operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the state of the write-off stage at `PLACED_WITH_AGENCY`, `RETENTION_RUNNING` and `CASE_CLOSED`; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3042; ASM-5098)) | rwb-case (P3) | P3 rwb-case | The moves `RETENTION_RUNNING` and `CASE_CLOSED` with the rule ID, its version and the closing amounts; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The timer read and stop (operation name Not specified in the source documents (GAP-3042; ASM-5098)) | rwb-case (P3) | P3 rwb-case | The timer item of DF-WRK-027 to DF-WRK-036 with its task, its type and its expiry, and its close; faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3042; ASM-5005)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows R-WO-36, R-WO-47 and R-WO-48; faked |
| The placement read (operation name and owner Not specified in the source documents (GAP-3042; ASM-5101)) | rwb-case (P3) or the agency record's owner | The placement of `PLACED_WITH_AGENCY`, its `ends_at` and its `recovered_amount`; the connection matrix gives S7 no row to rwb-partner (S9); faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The five rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3042 with ASM-5098, ASM-5005 and ASM-5101.

#### 12.3 Events published

None. The service owns `WriteOffApproved` (EV-24) on topic `rwb.writeoff.events.v1` with payload `writeOffId`, `caseId` and `amount`, and it is the committee's approval, which RWB-S7-E6018-APP publishes and RWB-S7-E6021-APP posts. This baseline therefore declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5099).

#### 12.4 Events consumed

None. No source gives rwb-writeoff a consumed event for this step: the two triggers are timers of the stage and the case facts arrive on their owner's contract. This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one (ASM-5099).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the retention branch; its input, its signals and its outcome for the parent are declared, not built |
| The retention branch of `WriteOffWorkflow` | Workflow branch | `rwb-writeoff` | The step from `PLACED_WITH_AGENCY` or `RETENTION_RUNNING` to the closure: R-WO-36, the timer, R-WO-47 with the R-WO-48 hold, the entry, the row and the stage outcome |
| `closeAfterRetention` | Activity, the one step | `rwb-writeoff` | The case, the write-off and the package answer in; the rule ID with its version, the state, the record reference and the case move out |
| `retentionTimer` | Durable timer | `rwb-writeoff` | The period of the reference data with its version; the expiry is the event `RETENTION_TIMER_EXPIRED` |

No child workflow of this service exists in this step and no timer table is declared here: the `timer` rows are P3's and are stopped on its contract. The activity and branch names are target design choices and no source document fixes them; no activity is registered by this story.

#### 12.6 Schedules

None. The retention wait is a durable timer inside `WriteOffWorkflow`, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-16, the monthly write-off scan on the third working day on the ACE batch-complete record for ALS, is RWB-S7-E6013-APP's. The "Workbench scheduler" of R-WO-36 and R-WO-47 is read as that durable timer, and DP-10 is not in this key's pattern set (ASM-5100).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its DF-FIN fields, its `state` and its record reference; the table the element answers from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked closing entry (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated expiry and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library for the stories that publish; no row of it belongs to this step |

`recovery_case` and `timer` (P3), `partner` (S9), `document` (P5), `rule_row` and `decision_log_entry` (P7), `notice` (P6), `payment` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or records of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The states `PLACED_WITH_AGENCY`, `RETENTION_RUNNING` and `CASE_CLOSED` of case `RC-2026-000884`; the two moves accepted and refused; no answer beyond 2 s | AC3, AC6 |
| rwb-case timer fake | Two open timers of the case closed in one answer, a timer already closed, and a refused close | AC3, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-36, R-WO-47 and R-WO-48 | AC4, AC6 |
| Placement fake | A placement with `ends_at` passed and `recovered_amount = 0`, and one with an amount recovered; the read carries the placeholder | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-writeoff write-off fake | The write-off `WO-2027-000402` of case `RC-2026-000884` with its amount, its tax criteria flag, its state and its record reference | AC2, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for the write-off, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished operation names, the period and the class values and the placement owner are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3042; ASM-5098, ASM-5101, ASM-5102).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 5 consumed | The case state read, the case-move answer, the timer read and stop, the package read and the placement read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval and posting stories'; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 1 activity and 1 durable timer declared, 0 registered | `WriteOffWorkflow` and its retention branch on `rwb-writeoff`, with its `closeAfterRetention` activity and the retention timer; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no write-off, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the read and six fakes.

**Deliverables.** The additive document `openapi/rwb-writeoff-v1.yaml`, the `write_off` element and the two closure state values, the contract README rows for the five consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the row changes, on the shared `rwb.decision-record.v1`. DP-13 moves the base of the key's two operations and adds none, because this step owns no operation. DP-19 is behind SCR-27, whose screen model is the edge contract's, and this baseline fixes the write-off answer only. No other pattern is claimed: the case, the timer, the package and the placement are consumed contracts, so DP-04, DP-05, DP-09 and DP-10 stay off this table and their absence is recorded in the registers (GAP-3042; ASM-5005, ASM-5099, ASM-5100).

**Build steps**

1. Record the absence of a closure operation and the two operations as other stories', with the absent-operation test of AC1.
2. Write the `write_off` element, its required flags, its lengths and the two closure state values of AC2, with the unprinted rule rows and the period placeholder.
3. Record the rwb-case rows of AC3 with their owner, their budget and the placeholder.
4. Record the rwb-decision package row and the placement read of AC4 with their owners and the placeholder.
5. Record the rights, the roles and the unattended identity of AC5.
6. Record the closing-entry element of AC6, with the two amounts and the period as reference data, and validate it against the library schema.
7. Publish the six fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the SCR-27 fragment and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate, so no path of this step raises it | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a body is absent or invalid, or a body fails schema validation, or a period has no version in force | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the read declares, and a role without the right of a consumed act tries it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The closing entry cannot be written before the write-off row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are those of the legacy message set of this key; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added. MSG-S7-001 is carried because it is in the message set of this feature, and the check itself belongs to the scan story of this service.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its retention and its closed state, through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off, its state and its closing entry, rwb-case for the case, its route state and its timers, and rwb-decision for the decision records; this baseline fixes the rwb-writeoff answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The closure read behind the list is a placeholder, because no source publishes it (ASM-5098). The legacy screen table's four states, scan, proposed, in committee and approved, are the earlier stories' of this key; the hold, refused, not-recorded and unavailable states of the app story read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-025-01 | AC1, AC2 | Contract | The retained case `RC-2026-000884`; the contract half answers the element, its state and the absent closure operation |
| TC-E6-025-02 | AC2, AC3 | Contract | R-WO-36 with the placement term passed and nothing recovered; the contract half answers the state value, the `RETENTION_RUNNING` move shape and the timer start shape |
| TC-E6-025-03 | AC3, AC4 | Contract | A retained case with nothing open and every document classed; the contract half answers the `CASE_CLOSED` move shape, the timer close and the entry element |
| TC-E6-025-04 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the entry element |
| TC-E6-025-05 | AC5 | Contract | A role without the Write-off and posting right; the contract half answers the 403 with MSG-P4-002, the rights of the read and the unattended identity |
| TC-E6-025-06 | AC6, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the entry path and the absence tests |
| TC-S7-E6025-CON-01 | AC1 | Contract | The document validates; no closure operation, no second base and no second topic are declared, and the two operations of the key are named as other stories' |
| TC-S7-E6025-CON-02 | AC2 | Contract | The `write_off` element validates with its eleven properties, its five required flags and the two closure state values against the published enumeration |
| TC-S7-E6025-CON-03 | AC3 | Contract | The case state, the two moves and the timer rows with their placeholders; the no-`recovery_case` and no-`timer` boundary |
| TC-S7-E6025-CON-04 | AC4 | Contract | The package row and the placement read with their placeholders; no rule row, no ledger entry and no partner property |
| TC-S7-E6025-CON-05 | AC5 | Contract | RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA, and the unattended identity holds no user right |
| TC-S7-E6025-CON-06 | AC6 | Contract | The six fakes match the document, the two amounts and the period carry their placeholder, and a drifted fake fails the build |
| TC-S7-E6025-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |

The six legacy cases are the legacy cases of RWB-E6-025 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6025-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S7-E6025-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the retention period, the retention classes, the closure conditions, the state values and the rule rows stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, an amount, a code, a class and a rule version only; every example is synthetic and no agency name is used.
- The case and the timers stay with rwb-case, the package and the ledger with rwb-decision, the placement with its owner and the class with rwb-document: the document declares no `recovery_case`, `timer`, `partner`, `document`, `rule_row` or ledger property and no row write of any of them (BR3, BR4, BR5).
- This step owns no operation and no event: the document declares none for it and records the two operations of the key as other stories' (BR6, BR12).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table (BR7).
- The period is never a default: a period or a class with no version in force is refused at the boundary (X7, BR13).
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-008 | A case closes after its retention period, and reopening a closed case needs a written rule, a reason and an approver (Must, E6) | The `write_off` element, the two closure state values, the case-move and timer rows and the entry | TC-E6-025-01, TC-E6-025-02, TC-E6-025-03, TC-S7-E6025-CON-02, TC-S7-E6025-CON-03 |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period (Open, DL26) | The period and the retention class as reference data with their version and a placeholder | TC-S7-E6025-CON-02, TC-S7-E6025-CON-06 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6025-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S7-E6025-CON-03, TC-S7-E6025-CON-04 |
| ADR-022 | Local decision record plus central ledger | The closing-entry element and the ledger entry of P7 | TC-S7-E6025-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-025, disposition Split (rework); feature FEAT-WOF-13 |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S7-E6025-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the seven new contract cases TC-S7-E6025-CON-01 to -07 |
| Feature and screens | FEAT-WOF-13, SCR-27 Write-off proposal |
| Rules | R-WO-36 and R-WO-47, with R-WO-48 as the hold, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-WO-36 and R-WO-47, the R-WO-48 hold, the state write, the entry and the two moves: RWB-S7-E6025-APP.
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001: RWB-S7-E6013-APP and RWB-S7-E6014-APP; the pack, the removal and the routing: RWB-S7-E6015-APP to RWB-S7-E6017-APP.
- The committee decision act, API-S7-002, and the approve, reject and defer outcomes: RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP.
- The posting, `WriteOffApproved` (EV-24), the provision release, the Finance feed and the reconciliation, including the second road into `RETENTION_RUNNING` under R-WO-42: RWB-S7-E6021-APP to RWB-S7-E6023-APP.
- The placement and the post charge-off sale that precede the closure: RWB-S7-E6026-APP and RWB-S7-E6028-APP; the payment on a closed case under R-WO-49: RWB-S7-E6027-APP.
- The case of record, its route states and the timer rows: rwb-case (P3), whose answers this baseline declares as consumed and faked (GAP-3042).
- The WO rule package, its version and the ledger: rwb-decision (P7) (ASM-5005).
- The placement and the agency record: S9 rwb-partner, whose read no source publishes (GAP-3042; ASM-5101).
- The retention class of a document, its disposal and the Document Hub task: rwb-document (P5).
- The ACE data products: rwb-source-data (P1); the gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

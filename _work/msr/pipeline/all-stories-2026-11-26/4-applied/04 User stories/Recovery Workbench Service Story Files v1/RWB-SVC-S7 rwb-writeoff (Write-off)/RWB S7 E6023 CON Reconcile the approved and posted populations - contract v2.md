# RWB-S7-E6023-CON Reconcile the approved and posted populations - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6023-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-023 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the reconciliation step of rwb-writeoff, split from RWB-E6-023. It fixes the `write_off` element and its DF-FIN fields, the WRITEOFF state vocabulary of the reconciliation, the consumed rwb-source-data posting row (INT-16, DF-ACE-261 to DF-ACE-269), the consumed rwb-case state and move rows, the consumed rwb-decision package row, the reconciliation-result element and the decision record of DP-03, the rights, the fakes and the absence tests, on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). It provides no REST operation: the two operations of this legacy key are RWB-S7-E6013-APP's and RWB-S7-E6018-APP's, the plan's C and X rows are empty while the step consumes three services, and the posting-product operation, its event and the matching cross-reference have no published name (GAP-3038; ASM-5084, ASM-5085, ASM-5089). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6023-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the reconciliation step of rwb-writeoff — the `write_off` element with its DF-FIN fields and the reconciliation state values, the consumed rwb-source-data GL posting row, the consumed rwb-case state and move answers, the consumed rwb-decision package row, the reconciliation-result element, the rights, the tables and the fakes**, so that **the app story, the SCR-27 fragment, rwb-reporting and the wave 4 harness build against one fixed, testable contract on Day 1, and a field, a state value, a consumed shape or an answer can never drift between rwb-writeoff, rwb-source-data, rwb-case and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, the result element its record carries, and the boundaries the comparison crosses. It declares no operation, no published event and no Schedule of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy reconciliation of RWB-E6-023 crossed three boundaries at once — a case state, a rule package and a GL posting read through a view — inside one process and one schema. The target splits them: rwb-source-data owns the `v_ace_*` views and the product over the GL postings, rwb-case owns the case and its timer, rwb-decision owns the rule package and the ledger, and rwb-writeoff owns the write-off row and the reconciliation result. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the `write_off` fields, the two state values the comparison writes, the posting row, the case state and move, the package row, the result element and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_writeoff`, login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules v1 §R4; context pack service row). It records that rwb-writeoff holds no grant on `rwb_source_data`, `rwb_case` or `rwb_decision` and none on any `recovery.v_ace_*` view, so the postings, the case and the package are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the plan's C and X rows are empty while the step consumes three services and most consumed names are unpublished (GAP-3038), the step provides no operation because the key's two operations belong to other stories (ASM-5089), the cross-reference between `write_off.id` and `v_ace_write_off.write_off_key` is published nowhere (ASM-5085), and no event or read carries the completeness result to rwb-reporting (ASM-5088).

The wave and the date are the plan's and the legacy epic's: this key is EP06, wave 4, release 30 April 2027, and rwb-writeoff is created in wave 4, so the two agree and the date is copied unchanged and marked tentative (ASM-5090).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `write_off` is S7's, `recovery_case` and `timer` are P3's, `rule_row` and `decision_log_entry` are P7's, `gl_write_off` and `v_ace_write_off` are ACE's and read by P1, `proceeds` is P8's. This document never declares another service's table, view or operation as its own.
- The rwb-source-data posting row, the rwb-case rows and the rwb-decision package row are published with their fakes, so each consumed row names a real owner document; they are not in this story's dependency rows, which are None, and the absence is recorded (GAP-3038; ASM-5084).
- The WO rule package and its rows for R-WO-13, R-WO-15, R-WO-42 and R-WO-43 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `write_off` table and its columns arrive with the DB story of this service, and the WRITEOFF vocabulary is published by RWB-S7-E6017-CON; this baseline narrows the vocabulary to the reconciliation values and creates no table, no column and no migration.
- The two operations of this legacy key, API-S7-001 and API-S7-002, are outside this baseline and belong to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP (ASM-5089).
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this step and record that it declares no operation for it, with the two operations of the key named as other stories'.
2. Fix the `write_off` element: the properties of DF-FIN-010 to DF-FIN-020 with their types, lengths, required flags and the state each value is declared against.
3. Fix the reconciliation values of the WRITEOFF vocabulary — `POSTED`, `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` — against TSD S7 T4 and the vocabulary of RWB-S7-E6017-CON.
4. Fix the consumed rwb-source-data row: the monthly GL write-off posting product of INT-16 with its nine fields, its `data_as_of` and its staleness rule, with the placeholder on the operation and event names.
5. Fix the consumed rwb-case rows: the case state read, the case-move answer with the retention entry, and the retention timer's owner.
6. Fix the consumed rwb-decision row: the WO package version in force with R-WO-13, R-WO-15, R-WO-42 and R-WO-43 and the count-and-amount tolerance.
7. Record the reconciliation-result element and the decision-record element of DP-03, written before the `write_off` rows change, with the two populations and the difference list.
8. Publish the contract tables of section 12, the rights and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shape, the error set, the rights, the drift between a fake and the document, the absence of an operation, of a published event, of a Schedule and of a foreign table or view.
10. Tag the baseline and hand it to RWB-S7-E6023-APP, the SCR-27 fragment, the reporting read of the period and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside the state vocabulary | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2, AC7 |
| X2 | A field is renamed or removed within major version 1, or a state value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | The document declares an operation, a published event, a Schedule, a queue or timer table, a view or another service's object as its own | The absence test and the boundary test fail the build | None | AC1, AC7 |
| X6 | The rights of the read are not the ones TSD S7 T6.1 and REC-06 give | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | The matching cross-reference, the posting-product operation or its event is declared with a name the sources do not give | The review fails the baseline; the row carries the placeholder | None | AC3, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-source-data, rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the state values, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S7-E6023-APP, the SCR-27 fragment, the reporting read of the period and the wave 4 harness on Day 1, and the rwb-source-data, rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the reconciliation step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case and timer is P3, of rule_row and decision_log_entry is P7, and of gl_write_off and v_ace_write_off is ACE read by P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no operation for the reconciliation and records the key's two operations as other stories' (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the comparison of the approved and posted populations, and the reconciliation report read carries the placeholder (GAP-3038; ASM-5089)
    Then it records POST /write-off-scans (API-S7-001) as RWB-S7-E6013-APP's and POST /write-offs/{writeOffId}/committee-decision (API-S7-002) as RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP
    Then the read behind SCR-27 carries an error set of 400, 401, 403 with MSG-P4-002, 404 and 503 and one message ID per condition
    Then the absence test fails a build that declares a reconciliation operation, a second base or a second topic

  Scenario: AC2 The write_off element and the reconciliation state values are declared (new, D-RCV-60)
    Given the write-off section of the baseline
    When it is compared with TSD S7 T3.0, T3.1 and T4 and with the API Specification's WriteOff element
    Then the write_off element declares the properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then id, case_id, amount, tax_criteria_met and recovered_after are required and the other six are optional, responsibility_center, cost_center and gl_product are strings of at most 10 characters, amount and recovered_after are numeric(18,2) and the two dates are dates
    Then decision_log_id is declared as the record reference the local library returns, committee_date as the approval date of the approved side and posted_date as the posting date matched against the GL row (ASM-5086)
    Then state is declared as the standard record column of TSD S7 T3.0 against the WRITEOFF vocabulary of RWB-S7-E6017-CON, and this step declares that it writes only POSTED, RETENTION_RUNNING and WRITEOFF_EXCEPTION and no other value (ASM-5087)

  Scenario: AC3 The consumed rwb-source-data posting row is declared (new, D-RCV-60)
    Given the consumed rows and the data boundary of the baseline
    When they are compared with rwb-source-data as the reader of v_ace_write_off and with the INT-16 flow
    Then the monthly GL write-off posting product is declared as consumed from P1 rwb-source-data with write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system and data_as_of (DF-ACE-261 to DF-ACE-269), and its operation name is Not specified in the source documents (GAP-3038; ASM-5084)
    Then the product-ready event is declared as consumed on rwb.source-data.events.v1, its name is Not specified in the source documents (GAP-3038; ASM-5084), and the connection matrix cell that gives S7 an event subscription on P1 is recorded as its basis
    Then data_as_of is declared as the staleness field bound to VR-S7-011-1 and MSG-P1-001
    Then the matching cross-reference between write_off.id and the posting's write_off_key is declared as consumed or as a column of this service, and it is Not specified in the source documents (GAP-3038; ASM-5085)
    Then the document declares no v_ace_write_off property and no SQL view of its own, and records that rwb-writeoff holds no recovery.v_ace_* grant (DP-01, DP-05)

  Scenario: AC4 The consumed rwb-case and rwb-decision rows are declared (new, D-RCV-60)
    Given the consumed rows of the case and the rule package
    When they are compared with rwb-case as the owner of recovery_case and timer and with rwb-decision as the owner of rule_row
    Then the case state read is declared as consumed from P3 rwb-case on the GET /cases/{caseId} family, with the case reference and the state of the write-off stage
    Then the case-move answer is declared as consumed from P3 with the moves RETENTION_RUNNING and WRITEOFF_EXCEPTION carrying the rule ID, its version and the retention class, and its operation name is Not specified in the source documents (GAP-3038; ASM-5087)
    Then the retention timer is declared as P3's row and as RWB-S7-E6025-APP's step, and this baseline declares no timer property and no timer write
    Then the WO package version in force is declared as consumed from P7 rwb-decision with the rows R-WO-13, R-WO-15, R-WO-42 and R-WO-43 and the count-and-amount tolerance, and its operation name is Not specified in the source documents (GAP-3038; ASM-5086)
    Then each consumed row is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The rights, the roles and the scope are fixed on the read (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S7 T6.1 and T-A.1, with REC-06 and with the legacy permission rows
    Then the read declares Write-off and posting right R with the scope applied, RW-CREDITAD holds CRUA, RW-WRITEOFF holds CRU, and RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA
    Then the document records the legacy A holders RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the legacy C holders RW-WRITEOFF and RW-CREDITAD, and declares no A right on an operation of this story because the step is unattended (ASM-5089)
    Then the document records that the comparison runs under the service identity, that REC-06 names Credit Administration as the owner of the check, and that FSD S7 A2.11.3.3 names "None; runs unattended" as the primary user
    Then an act taken on API-S7-002 is the committee decision story's and is consumed, never provided

  Scenario: AC6 The reconciliation-result element, the decision record and the fakes answer the document (new, D-RCV-60)
    Given the result and decision sections and the fakes of the baseline
    When each is compared with the library schema and with the element it serves
    Then one result is declared per audit period with the approved count and amount, the posted count and amount, the difference count and amount, the tolerance in force and the reconciled flag, and one decision record per period and per difference through the local library on the shared rwb.decision-record.v1
    Then the record is written before the write_off rows change, and a failed write leaves the rows unchanged with MSG-P7-003
    Then the rwb-source-data fake answers a product at today's business date, a stale product, a product with an unmatched write-off key and no answer beyond 2 s
    Then the rwb-case fake answers the states APPROVED, POSTED and RETENTION_RUNNING of case RC-2027-000712, an accepted and a refused move, and the rwb-decision fake answers the package at its version with the tolerance above and below the difference
    Then the rwb-writeoff fake answers the write-off WO-2027-000318 of case RC-2027-000712 in POSTED with its amount and its record reference
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1, the queue is rwb-writeoff and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, rule_row, decision_log_entry, gl_write_off, v_ace_write_off, proceeds and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the document declares no published event and names WriteOffApproved (EV-24) as RWB-S7-E6018-APP's, and it records that no completeness event is catalogued (ASM-5088)
    Then the document declares no Schedule and no Quartz row, and records that no job of the batch design covers reconciliation and that JOB-16 is RWB-S7-E6013-APP's (GAP-3038; ASM-5084)
    Then the document records that the plan's C and X rows are empty although the step consumes three services, and that the S7 module files were read from the extract folder
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6023-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off row, its state and its approved amount are rwb-writeoff's, and the contract declares their fields and state values on the `write_off` element only | Context pack ownership row `write_off`; TSD S7 T3.0 and T3.1; DP-01 |
| BR2 | The posted population is ACE data read by rwb-source-data: the contract declares the posting product as consumed and declares no `gl_write_off` or `v_ace_write_off` property and no view of its own | Architecture v5 slide 8; LDM v8 DF-ACE-261 to DF-ACE-269; DP-01, DP-05 (recorded); ASM-5084 |
| BR3 | The comparison is count and amount inside the tolerance in force; the tolerance and the period are package values and reference data, never schema defaults | REC-06; R-WO-42 and R-WO-43; BR-S7-011 |
| BR4 | The decision record is declared as an element written before the rows change, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy RWB-E6-023 AC1 and AC4 |
| BR5 | The case, its route state and the `timer` row stay with rwb-case: the contract declares the state read and the move answer as consumed and declares no `recovery_case` and no `timer` property | Context pack ownership rows; legacy Data table; ASM-5087 |
| BR6 | The rule package and the ledger stay with rwb-decision: the contract names R-WO-13, R-WO-15, R-WO-42 and R-WO-43 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5086 |
| BR7 | No published event belongs to this step: the contract declares no producer and names `WriteOffApproved` (EV-24) as the approval story's, and it records a consumed product-ready event of P1 with a placeholder name | Event and Messaging Design v5 EV-24; context pack connection-matrix row S7; ASM-5084, ASM-5088 |
| BR8 | No Schedule belongs to this step: no job of the batch design covers reconciliation, JOB-16 is the scan story's, and the period arrives with the product | Batch and Scheduling Design v5 JOB-16; ASM-5084 |
| BR9 | The state vocabulary is closed: the WRITEOFF values are published as an enumeration of `state`, this step writes three of them, and no state value is a constant of the code | TSD S7 T3.0 and T4; RWB-S7-E6017-CON; ASM-5087 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, amounts, a code and a rule version only, and the populations are compared by reference, never by party | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or view as its own | DP-13; Template and Rules v1 §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version, and the document declares only operations owned by rwb-writeoff, of which this step owns none | Architecture v5 slide 11 notes (BACKWARD compatibility); Ownership rows; ASM-5089 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the reconciliation values, the consumed rows, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-27 fragment, the reporting read and the rwb-source-data, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a state value is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence and boundary tests of AC1 and AC7 fail: an operation, a published event, a Schedule, a view or a foreign table | In review |

The WRITEOFF machine the document describes is the app story's: `POSTED`, `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` are the values this step reads and writes, and the case route state that rwb-case holds is answered, not declared here. This baseline fixes the vocabulary and moves no write-off and no case (ASM-5087).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the consumed rows |
| Consuming teams (the app story, the SCR-27 fragment, the reporting read and the owners of rwb-source-data, rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Credit Administration, as the owner role of REC-06 | Confirms the count-and-amount comparison and the tolerance the read exposes |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product`, `recovered_after` |
| Required flags | `id`, `case_id`, `amount`, `tax_criteria_met` and `recovered_after` required; the other six optional, as the API Specification's `WriteOff` element declares them |
| State | `state` of TSD S7 T3.0 against the WRITEOFF vocabulary of T4 and of RWB-S7-E6017-CON, published as an enumeration; this step writes `POSTED`, `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` |
| Record reference | `decision_log_id` holds the identifier the local decision-record library returns, and the P7 ledger entry id is not stored here (ASM-5086) |
| Approved side | `amount`, `committee_date` and the record of the final call, the approver and the limit applied that R-WO-13 and R-WO-15 produce are read as the approved side of the comparison (ASM-5083) |
| Result element | `approvedCount`, `approvedAmount`, `postedCount`, `postedAmount`, `differenceCount`, `differenceAmount`, `tolerance`, `reconciled` and the audit period, carried in the decision record and exposed on the read; the names are this baseline's choice (ASM-5085) |
| Consumed shapes | The rwb-source-data posting product of INT-16 (DF-ACE-261 to DF-ACE-269), the rwb-case state and move, and the rwb-decision package row, each declared as consumed and faked |
| Not declared here | `recovery_case` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `gl_write_off` and `v_ace_write_off` (ACE, read by P1), `proceeds` (P8), every `v_ace_*` view, and the two operations API-S7-001 and API-S7-002 (other stories of this service) |
| Consumed fields with no source | The posting-product operation and event names, the matching cross-reference, the case-move operation name, the package read name and the completeness publication path: Not specified in the source documents (GAP-3038; ASM-5084, ASM-5085, ASM-5087, ASM-5088) |

The field-level formats of the added elements are settled in the baseline review; this story fixes the element names, the three state values of AC2 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This step provides no operation and this baseline declares none for it. The two operations of this legacy key are other stories' of the same service: `POST /write-off-scans` (API-S7-001, right C) is RWB-S7-E6013-APP's, and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) carries the approve outcome at RWB-S7-E6018-APP and the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. The reconciliation report read and the completeness read are Not specified in the source documents (GAP-3038; ASM-5088, ASM-5089) and carry the placeholder. A build that declares a reconciliation operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The monthly GL write-off posting product read (operation name Not specified in the source documents (GAP-3038; ASM-5084)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The postings of INT-16 for the period with their nine fields and `data_as_of`; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the state of the write-off stage; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3038; ASM-5087)) | rwb-case (P3) | P3 rwb-case | The moves `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` with the rule ID, its version and the retention class; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3038; ASM-5086)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the rows R-WO-13, R-WO-15, R-WO-42 and R-WO-43 with the count-and-amount tolerance; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3038 with ASM-5084, ASM-5086 and ASM-5087.

#### 12.3 Events published

None. The service owns `WriteOffApproved` (EV-24) on topic `rwb.writeoff.events.v1` with payload `writeOffId`, `caseId` and `amount`, and it is the committee's approval, which RWB-S7-E6018-APP publishes. No source catalogues a completeness event, so R-WO-42's "publish completeness" is declared as the result element of section 11 available to rwb-reporting, and the event that would carry it is Not specified in the source documents (GAP-3038; ASM-5088). This baseline therefore declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one.

#### 12.4 Events consumed

| Event | Topic | Owner | Use in the baseline |
|---|---|---|---|
| The monthly GL write-off posting product ready event (event name Not specified in the source documents (GAP-3038; ASM-5084)) | `rwb.source-data.events.v1` | P1 rwb-source-data | The signal that the postings of the period have landed, which starts the branch; the connection matrix gives S7 an event subscription on P1; faked |

One consumer group on `rwb-writeoff`, CloudEvents envelope and an inbox row in `rwb_writeoff`. No other event is consumed: the case and the package arrive on their owners' contracts, and the decision record is the library's on the shared `rwb.decision-record.v1`, not an event of this service.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the reconciliation branch; its input, its signals and its outcome for the parent are declared, not built |
| The reconciliation branch of `WriteOffWorkflow` | Workflow branch | `rwb-writeoff` | The step from the posted population to `RETENTION_RUNNING` or `WRITEOFF_EXCEPTION`: R-WO-42, or R-WO-43 with the difference list, the records, the rows, the move and the stage outcome |
| `reconcilePopulations` | Activity, the one step | `rwb-writeoff` | The two populations and the package answer in; the counts, the amounts, the difference list, the state, the record references and the case move out |

No child workflow of this service exists in this step, and the retention timer that R-WO-42 signals is RWB-S7-E6025-APP's under R-WO-47. The activity name is a target design choice and the trigger is read as the arrival of the monthly posting product for the open period. No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the monthly posting product; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. No job of the Batch and Scheduling Design v4 covers reconciliation, JOB-16 is the monthly write-off scan of RWB-S7-E6013-APP, and whether the step needs a Schedule of its own is Not specified in the source documents (GAP-3038; ASM-5084).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its DF-FIN fields, its `state` and its record reference; the table the element answers from and the approved population of the comparison |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the period and of each difference (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated product and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library for the stories that publish; no row of it belongs to this step |

`recovery_case` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `gl_write_off` and `v_ace_write_off` (ACE, read by P1), `proceeds` (P8) and every `v_ace_*` view are not owned by this baseline; it names them only as answers, rule versions or data products of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data posting fake | The product of `2027-04` at today's business date, the same product dated stale, a product with an unmatched write-off key, and no answer beyond 2 s | AC3, AC6 |
| rwb-case state and move fake | The states `APPROVED`, `POSTED`, `POSTING_REJECTED` and `RETENTION_RUNNING` of case `RC-2027-000712`; the moves `RETENTION_RUNNING` and `WRITEOFF_EXCEPTION` accepted and refused; no answer beyond 2 s | AC4, AC6 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-13, R-WO-15, R-WO-42 and R-WO-43, the delegation limits and the tolerance above and below the difference | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-writeoff write-off fake | The write-off `WO-2027-000318` of case `RC-2027-000712` in `POSTED`, with its amount, its posted date and its record reference | AC2, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for the write-off, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished operation and event names and the matching cross-reference are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3038; ASM-5084, ASM-5085).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-source-data posting product, the rwb-case state read and move answer, and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 1 consumed | The rwb-source-data product-ready event on `rwb.source-data.events.v1`; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch and 1 activity declared, 0 registered | `WriteOffWorkflow` and its reconciliation branch on `rwb-writeoff`, with its `reconcilePopulations` activity; no Schedule and no child workflow |
| File | None | The monthly GL file of INT-16 is received by ACE ingestion and lands in ACE; this service reads no file |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no write-off, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the read and six fakes.

**Deliverables.** The additive document `openapi/rwb-writeoff-v1.yaml`, the `write_off` element, the state enumeration of the three reconciliation values, the result element, the contract README rows for the four consumed rows and their placeholders, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the rows change, on the shared `rwb.decision-record.v1`. DP-13 moves the base of the key's two operations and adds none, because this step owns no operation. DP-19 is behind SCR-27, whose screen model is the edge contract's, and this baseline fixes the write-off answer only. DP-05 is not in this story's pattern set although the comparison reads the GL postings; the row is declared as consumed from rwb-source-data and no view grant is claimed (GAP-3038; ASM-5084). DP-09 and DP-10 stay off this table although one event is consumed and the retention entry is signalled (ASM-5088).

**Build steps**

1. Record the absence of a reconciliation operation and the two operations as other stories', with the absent-operation test of AC1.
2. Write the `write_off` element, its required flags, its lengths and the three reconciliation state values of AC2.
3. Record the rwb-source-data posting row, its nine fields, `data_as_of` and the consumed event of AC3, with their placeholders and the cross-reference.
4. Record the rwb-case state and move rows and the rwb-decision package row of AC4, with their owners and the placeholder.
5. Record the rights, the roles and the scope of AC5, with the legacy A and C holder disposition.
6. Record the result element, the decision-record element and the six fakes of AC6, and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the SCR-27 fragment, the reporting read and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate, so no path of this step raises it | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a body is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the read declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the write-off rows change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The posting product is stale after a late or failed ACE batch (VR-S7-011-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The first four message IDs are those of the legacy message set of this key and MSG-P1-001 is the message of VR-S7-011-1 in FSD S7 A2.11.3.1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added. MSG-S7-001 is carried because it is in the message set of this feature, and the check itself belongs to the scan story of this service.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its scan, proposed, in-committee, approved and reconciled states, through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off and its reconciliation state, rwb-case for the case and its route state, and rwb-reporting for the completeness of the period; this baseline fixes the rwb-writeoff answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The reconciliation report read behind the list is a placeholder, because no source publishes it (ASM-5089). The refused, not-recorded and stale states of the app story read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-023-01 | AC1, AC2 | Contract | The closing period `2027-04`; the contract half answers the element, the three state values, the result shape and the absent reconciliation operation |
| TC-E6-023-02 | AC2, AC4 | Contract | R-WO-13 with the credit committee approval; the contract half answers the `APPROVED` state value, the final-call shape and the move shape |
| TC-E6-023-03 | AC2, AC4 | Contract | R-WO-15 with the committee approval; the contract half answers the approver and limit shapes and the `RETENTION_RUNNING` move shape |
| TC-E6-023-04 | AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E6-023-05 | AC5 | Contract | A role without the Write-off and posting right; the contract half answers the 403 with MSG-P4-002 and the rights of the read |
| TC-E6-023-06 | AC6, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the record path and the absence tests |
| TC-S7-E6023-CON-01 | AC1 | Contract | The document validates; no reconciliation operation, no second base and no second topic are declared, and the two operations of the key are named as other stories' |
| TC-S7-E6023-CON-02 | AC2 | Contract | The `write_off` element validates with its eleven properties, its five required flags and the three reconciliation state values |
| TC-S7-E6023-CON-03 | AC3 | Contract | The posting row with its nine fields, `data_as_of`, the consumed event, the cross-reference placeholder and the no-view boundary |
| TC-S7-E6023-CON-04 | AC4 | Contract | The case state and move rows and the package row with their placeholders; no `recovery_case`, `timer`, rule row or ledger property |
| TC-S7-E6023-CON-05 | AC5 | Contract | RW-CREDITAD holds CRUA, RW-WRITEOFF holds CRU, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA, and the legacy A and C holders are recorded |
| TC-S7-E6023-CON-06 | AC6 | Contract | The six fakes match the document, the result element matches the record, and a drifted fake fails the build |
| TC-S7-E6023-CON-07 | AC7 | Contract | The naming baseline; the absence test for a published event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |

The six legacy cases are the legacy cases of RWB-E6-023 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6023-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S7-E6023-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the tolerance, the audit period, the retention class, the state values and the rule rows stay package values, reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, a code and a rule version only, and the populations are compared by reference, never by party; every example is synthetic.
- The case, its route state and the `timer` row stay with rwb-case, the package and the ledger with rwb-decision, and the GL postings and their views with ACE and rwb-source-data: the document declares no `recovery_case`, `timer`, `rule_row`, `gl_write_off` or `v_ace_write_off` property and no row write of any of them (BR2, BR5, BR6).
- This step owns no operation: the document declares none for it and records the two operations of the key as other stories' (BR12, ASM-5089).
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or view as its own fails the review (DP-13).
- The document lists only operations owned by rwb-writeoff and describes a consumed element as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event, a second topic, a Schedule, a Quartz row, a shared job table or a data-lake extract (DP-17).
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (Must, E6; FSD S7 Requirements served); the contract fixes the result element and the state values the completeness rides on, and the plan's reqs row for the slice is empty (GAP-3038; ASM-5091) | The `write_off` element, the state enumeration and the result element | TC-E6-023-01, TC-S7-E6023-CON-01, TC-S7-E6023-CON-02 |
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account (Must, E6); the contract fixes the record reference and the approved-side fields it reads | The `decision_log_id`, `committee_date` and `amount` properties | TC-S7-E6023-CON-02, TC-S7-E6023-CON-06 |
| REC-06 | Write-offs approved in the Workbench against the postings in `recovery.v_ace_write_off`, by count and amount, tolerance zero, monthly, owner Credit Administration | The posting row, the tolerance and the period | TC-S7-E6023-CON-03, TC-S7-E6023-CON-05 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6023-CON-07 |
| ADR-018 | No data lake; rwb-reporting read model from events | The result element and the completeness note | TC-S7-E6023-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S7-E6023-CON-03, TC-S7-E6023-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and the ledger entry of P7 | TC-S7-E6023-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-023, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S7-E6023-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the seven new contract cases TC-S7-E6023-CON-01 to -07 |
| Feature and screens | FEAT-WOF-11, SCR-27 Write-off proposal |
| Rules | R-WO-13, R-WO-15, R-WO-42 and R-WO-43, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-018 (no data lake), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the evaluation of R-WO-42 and R-WO-43, the records, the state, the record reference, the case move and the exception list: RWB-S7-E6023-APP.
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The pack: RWB-S7-E6015-APP; the removal by the team: RWB-S7-E6016-APP; the committee routing: RWB-S7-E6017-APP.
- The committee act, API-S7-002, and the approve, reject and defer outcomes: RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP (ASM-5089).
- The posting to ALS and the ledger, R-WO-20 to R-WO-23: RWB-S7-E6021-APP; the provision feed, R-WO-25 to R-WO-28: RWB-S7-E6022-APP.
- The write-off exception loop: RWB-S7-E6024-APP; the retention timer and the closure, R-WO-47 and R-WO-48: RWB-S7-E6025-APP (ASM-5087).
- The case of record, its route states and the `timer` row: rwb-case (P3), whose answers this baseline declares as consumed and faked (GAP-3038).
- The GL write-off postings, `gl_write_off` and `v_ace_write_off`, the INT-16 ingestion and the product over them: ACE and rwb-source-data (P1) (GAP-3038; ASM-5084).
- The WO rule package, its version, the delegation limits and the ledger: rwb-decision (P7) (ASM-5086).
- The completeness read model and its report: rwb-reporting (P9) (ASM-5088); the gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

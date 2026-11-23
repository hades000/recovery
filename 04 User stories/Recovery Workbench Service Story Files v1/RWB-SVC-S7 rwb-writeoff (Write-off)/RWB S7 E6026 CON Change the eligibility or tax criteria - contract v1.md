# RWB-S7-E6026-CON Change the eligibility or tax criteria - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6026-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-026 |
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

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the criteria-change step of rwb-writeoff, split from RWB-E6-026. It fixes the criteria-version element of `POST /write-off-scans` on `/api/recovery/writeoff/v1` (DP-13), the version state of SCR-27 behind the gateway-bff composite route (DP-19), the decision-record element of the acceptance written before the pin (DP-03), the consumed package read and case-boundary rows, the rights of TSD S7 T6.1, the fakes and the absence tests. No source publishes a field list for the criteria-version element, a call type or operation name for the package read, or a home for `tax_criteria_version`; the plan's C row is None although the step consumes three rows. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the criteria-change step of rwb-writeoff — the criteria-version element of the scan operation, the version state of SCR-27, the accepted-version and pin elements, the decision-record element, the consumed package read and case-boundary rows, the rights, the error envelope, the tables and the fakes**, so that **the app story, SCR-27 and the wave 4 harness build against one fixed, testable contract on Day 1, and a version, a rule set, a consumed row or a state shape can never drift between rwb-writeoff, rwb-decision and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and route services reach the shared capabilities through Temporal and not through a second REST hop (connection matrix). The legacy criteria change of RWB-E6-026 crossed four boundaries at once: a screen, a rule set, a version and a case state. The target splits them: rwb-decision owns the rule set, its versions and the authoring approval; rwb-case owns the case and its route states; rwb-writeoff owns the accepted version, the pin of a cut-off and the record of each outcome. Each boundary is a contract another team builds against, so each is fixed before the app story starts: the criteria-version element, the version state, the record of the acceptance and the three consumed rows.

The baseline also fixes the naming the checks require: schema and login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules §R4; context pack). It records that this service holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_decision`, so DP-05 is declared as a prohibition and the package and the case are consumed on their owner's boundary only.

Four points are carried as gaps and assumptions rather than decided quietly: the criteria change has no screen, no operation and no write right of its own in this service, and no source gives the version a table, a key or an owner (GAP-3044; ASM-5104 to ASM-5108); the connection matrix gives S7 a Temporal line to rwb-decision and none to rwb-case, so the package read is declared on the owner's queue and the case boundary is a stage outcome (ASM-5108, ASM-5110); no source publishes the field list of the criteria-version element or of the version state (GAP-3044); and the pattern set carries neither DP-04 nor DP-06, DP-07, DP-09 or DP-10 although the step lives on a rule package, a parameter and reference-data set, an outbox and a monthly scan (ASM-5109).

One boundary is stated rather than left to the reader: the scan operation is shared with the population half of RWB-E6-013 and the tax-criteria half of RWB-E6-014 as RWB-S7-E6013-CON and RWB-S7-E6014-CON, so this baseline fixes the criteria-version element and the edition of the answer and replaces neither document; the three are same-service baselines of one operation and are reconciled at the same contract freeze (ASM-5112).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL and RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it says so.
- Ownership is taken from the context pack and the Ownership Map only: `recovery_case` and `timer` are P3's, `write_off` is S7's, `decision_log_entry` and `rule_row` are P7's, every `v_ace_*` view is P1's, `document` is P5's and `proceeds` is P8's. This document never declares another service's table or operation as its own.
- The rwb-decision package read and the rwb-case boundary rows are published with their fakes, so every consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3044; ASM-5108, ASM-5110).
- The outbox and inbox library of DP-09 and the schedule row of DP-10 are the platform dependencies of the service's topic and of `JOB-16`; the plan's H row for this key does not carry them, and this baseline declares no event and no Schedule and records the absence (ASM-5109).
- The WO criteria set, its 51 rules over 27 states, R-WO-01, R-WO-03, R-WO-04 and `tax_criteria_version` are governed in rwb-decision (P7) with the authoring story RWB-P7-E1073; this baseline names them and declares none of them (ASM-5104, ASM-5105).
- The screen the change is made on is not named by any source; SCR-27 Write-off proposal is the only screen of the module, so the version state is declared on it (GAP-3044; ASM-5106).
- The `write_off` table arrives with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration, and adds no column for the version (BR6).
- No build dependency: this story is Day 1 and sits in contract group `CG-W4` by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the additions of the OpenAPI 3.1 document of rwb-writeoff for this step: the criteria-version property of the scan request, the pinned version and the run state of the answer, and the version-state answer the composite route reads.
2. Fix the criteria-version element: the version label, its hash, the rule set it carries, the cut-off it is pinned to and the run state, with the placeholder where the sources give no field.
3. Fix the decision-record element of DP-03: the acceptance record written before the pin, and the version recorded on each outcome of R-WO-01.
4. Fix the consumed rows: the package read of rwb-decision with its rule set and `tax_criteria_version`, the population read and the case-move answer of rwb-case on the workflow boundary, with the placeholder on the operation names, the call type of the package read and the home of the version.
5. Record the closed vocabulary of the run state and of the route states this step answers, the rights of TSD S7 T6.1, the naming baseline and the rule that no criterion is a constant of the code.
6. Publish the contract tables of section 12 and the fakes of 12.8.
7. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read, of a `recovery_case` write, of a version column, of a published event, of a consumed event and of a Schedule, and the drift between a fake and the document.
8. Tag the baseline and hand it to RWB-S7-E6026-APP, SCR-27 and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1, AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | An element or a consumed row has a field the sources do not give | The row carries the placeholder and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside the closed run-state or route-state list appears in the document or an example | The vocabulary test fails the build | None | AC2, AC5 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a rule row or a version column of `write_off` | The review fails the baseline and the boundary test fails the build | None | AC4, AC7 |
| X7 | The document declares an event of this step, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones TSD S7 T-A.1 and T6.1 declare, or the document grants this service a write on the criteria | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack, the FSD and TSD S7 appendices and the published owner contracts of rwb-decision and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operation, the base, the topic, the queue and the schema are fixed by the architecture |
| Valuable | Unblocks RWB-S7-E6026-APP, SCR-27 and the wave 4 harness on Day 1, and the rwb-decision and rwb-case teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, five fakes and ten contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the criteria-change step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of every v_ace_* view is P1, of decision_log_entry and rule_row is P7 and of the WO rule package is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The criteria-version element is declared on the scan operation with its shapes and its errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then POST /write-off-scans is declared under the base /api/recovery/writeoff/v1 and owned by rwb-writeoff, with the criteria-version property in ScanRequest and the pinned version and run state in WriteOffScan
    Then the operation declares the Idempotency-Key header and the repeated key answering the scan it ran
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then no operation that changes a criterion is declared, because none is published for this service

  Scenario: AC2 The criteria-version element and the run-state vocabulary are fixed (new, D-RCV-60)
    Given the element section of the baseline
    When it is compared with TSD S7 T3.1, T3.2 and T4 and with FSD S7 A2.14
    Then the criteria-version element declares the version label, its hash, the rule set it carries, the cut-off it is pinned to and the run state
    Then the run state is one of SCAN_DUE, SCAN_HELD, POPULATION_PROPOSED and CASE_CLOSED, and the document adds no fifth state and no free text
    Then the element declares tax_criteria_version as the version the tax criteria were tested with, and an absent version as the held state and not as a default
    Then the element declares no threshold, no criteria value, no eligibility condition and no list of accounts of its own
    Then no property is added for a person name, an address, a contact value or an identity number
    Then a property the sources do not give carries the placeholder (GAP-3044; ASM-5104)

  Scenario: AC3 The consumed rows of rwb-decision and rwb-case are declared and the facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the ownership of the context pack and the connection matrix row of S7
    Then the package read is declared as consumed from P7 rwb-decision, with the WO package, its version, its 51 rules over 27 states, R-WO-01, R-WO-03, R-WO-04, the eligibility rule on both tracks and tax_criteria_version
    Then the package read is declared as a Temporal activity on the rwb-decision queue, because the matrix gives S7 a Temporal line to P7 and no REST line
    Then the population read and the case-move answer are declared as consumed from P3 rwb-case on the child-workflow boundary, with the cases in SCAN_DUE and the moves POPULATION_PROPOSED and SCAN_HELD, because the matrix gives S7 no line to P3
    Then the operation names, the call type of the package read and the owner of tax_criteria_version are Not specified in the source documents (GAP-3044; ASM-5108, ASM-5110)
    Then the document declares no v_ace_* path, no v_ace_* property, no recovery_case property and no grant on any rwb_* schema of another owner
    Then each row carries a budget, a breaker and the retry rule of the platform, and no row is a second hop (ADR-020)

  Scenario: AC4 The accepted-version, pin and decision-record elements are declared and written before the outcome (new, D-RCV-60)
    Given the decision and pin sections of the baseline
    When they are compared with the library schema and with TSD S7 T2 and T4
    Then one decision record is declared per acceptance and per outcome with the case reference, the rule ID, the package version, tax_criteria_version, the inputs reference, the outcome and the case move
    Then the record is declared as written through the local library on the shared rwb.decision-record.v1 before the version is pinned and before the outcome exists, and a failed write leaves everything unchanged with MSG-P7-003
    Then the pin is declared as the version, its hash, the package reference and the cut-off, held for the length of a run and released at its end, with no table and no column of its own
    Then the version is declared as recorded on the outcome and not on a column of write_off, and the document adds no version column

  Scenario: AC5 The error envelope, the messages and the rights are fixed (new, D-RCV-60)
    Given the error and access sections of the baseline
    When they are compared with TSD S7 T-A.1, T-A.2 and T6.1 and with FSD S7 A2.14.3.3
    Then the operation declares Write-off and posting right C with the scope applied, and the version state is read under right R
    Then a missing or incomplete criteria version is described as 422 with MSG-S7-001, a role without the right as 403 with MSG-P4-002, a failed record write as 503 with MSG-P7-003 and a missing required field as 422 with MSG-GEN-001
    Then RW-COE holds R on the capability area, RW-FINANCE, RW-PRODHEAD, RW-WOCOMM and RW-RISK hold RA, RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA and the other roles and SY-* identities hold R as TSD S7 T6.1 gives them
    Then the document grants no write on a criterion and no authoring right to any role of this service, and the conflict with FSD S7 A2.14.3.3 is recorded (GAP-3044; ASM-5107)
    Then the error envelope carries one message ID per condition and the four messages are the legacy and FSD wording, unchanged

  Scenario: AC6 The five fakes answer the document and the drift test fails a build (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-decision package fake answers the version 2026-11 with R-WO-01, R-WO-03, R-WO-04 and tax_criteria_version 2026-11, a version 2026-12 published mid-run, an incomplete version and an absent version
    Then the rwb-case population fake answers the population of the cut-off with 120 cases in SCAN_DUE, the case-move fake answers the two moves accepted and refused, the decision-record stub answers a healthy chain and a stopped chain, and the gateway-bff fake answers the merged SCR-27 answer with the version state
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event and no Schedule are declared (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1 with its retry and .dlt topics, the queue is rwb-writeoff in namespace rwb-recovery and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the table named as owned is write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, every v_ace_* view, decision_log_entry and rule_row are named as other owners' and are consumed only through their contracts
    Then the document declares no event of this step, no consumed event, no second topic and no Schedule, and it names WriteOffApproved (EV-24) as the committee story's and JOB-16 as the scan story's
    Then the absence test fails a build that adds a published event, a consumed event, a second topic, a Schedule, a v_ace_* read or a version column (ASM-5109)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6026-APP and copy no criterion of the legacy story, whose three criteria stay with the app story word for word. The criteria themselves are not a property of this document: the document carries a version, a hash and a run state, and the criteria are rule facts of the WO package (ASM-5104).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off and its population are rwb-writeoff's, and the contract declares the fields and the required flags of `write_off` only | TSD S7 T3.1; context pack ownership rows (table `write_off`) |
| BR2 | The decision record is declared as an element written before the pin and before the outcome, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy AC1 and AC3 |
| BR3 | The case facts stay with rwb-case: the contract declares the population read and the case-move answer as consumed, declares no `recovery_case` property and describes no ACE table read | DP-05 as a prohibition; ASM-5110 |
| BR4 | The criteria set, its versions, `tax_criteria_version` and the authoring approval are consumed package facts of rwb-decision; the document declares no criterion value, threshold or default and no authoring operation | FSD S7 A2.14, VR-S7-014-1 and BR-S7-014; ASM-5104, ASM-5105 |
| BR5 | The accepted version is pinned per cut-off and recorded on each outcome; the pin is a run-scoped element and not a table, a column or a second write-off | ASM-5104; TSD S7 T3.1 |
| BR6 | No version column and no version table is added to `write_off` or to any schema of this service | TSD S7 T3.1; GAP-3044 |
| BR7 | No event of this step is declared: `WriteOffApproved` (EV-24) is the committee story's, and the outbox library of DP-09 is recorded as an absent H row | ASM-5109; TSD S7 T5.3 |
| BR8 | No Schedule is declared: `JOB-16` is the scan story's and the schedule row of DP-10 is recorded as absent | ASM-5109; context pack job row |
| BR9 | A POST declares the `Idempotency-Key` and stores its answer | TSD S7 T-A.2 |
| BR10 | The vocabulary is closed: the run state and the route states are the values of TSD S7 T4, and no list value is a constant of the code | TSD S7 T3.2 and T4; FSD S7 BR-S7-014 |
| BR11 | No personal data in a schema, an example or a fake: identifiers, amounts, dates, a version and a hash only | Template and Rules §R7.2 (s17); TSD S7 T6.2 |
| BR12 | One REST base, one topic, one queue, one schema and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR13 | A schema change is additive within major version 1; a breaking change is a new major version | Platform API rule (ADR-020) |
| BR14 | The document lists only operations owned by rwb-writeoff; a consumed operation or activity is described as consumed and faked, never as provided | DP-01, DP-11 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The operation, the elements, the consumed rows, the decision and pin elements and the fakes are described | In review |
| In review | Consumer sign-off | The app story, SCR-27, the wave 4 harness and the owners of rwb-decision and rwb-case accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional run property or a new filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC4 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a version column, a published or consumed event, a second topic or a Schedule | In review |

The state machine the document describes is the app story's and rwb-case's: `SCAN_DUE`, `SCAN_HELD`, `POPULATION_PROPOSED` and `CASE_CLOSED` are route states of the WRITEOFF machine of TSD S7 T4 and live on the case of record. This baseline fixes the vocabulary and the enums and moves no write-off and no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the plan rows the baseline consumes, including the three consumed rows, the absent DP-04, DP-06, DP-07, DP-09 and DP-10 rows, and the conflict of the change right |
| Consuming teams (the app story, SCR-27, the wave 4 harness and the owners of rwb-decision, rwb-case and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox and inbox library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-writeoff login (DP-02)" and is not part of this baseline. No row of this table may author a criterion: the authoring right belongs to the rwb-decision capability and to its own baseline (ASM-5105, ASM-5107).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Criteria-version element | The version label, its hash, the rule set it carries, the cut-off it is pinned to and the run state; the field list beyond these is Not specified in the source documents (GAP-3044; ASM-5104) |
| Run state | One of `SCAN_DUE`, `SCAN_HELD`, `POPULATION_PROPOSED`, `CASE_CLOSED` from TSD S7 T4, closed and without free text |
| Tax criteria | `tax_criteria_version` as the version the tax criteria were tested with, recorded beside the outcome and never a threshold or a criteria value |
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020 as the sibling baselines fix them; this document adds no property to `write_off` and no version column |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the pin and before the outcome (DP-03) |
| Case facts | DF-CAS-001 to DF-CAS-023 of `recovery_case` in P3, read only on the workflow boundary and never written, copied or joined here |
| Event data | None of this step: no event is declared (§12.3) |
| Lists | None is named for this step by TSD S7 T3.2, which leaves the list table empty; a value this step records is a version, a hash, a state name or a date |
| Not declared here | `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `proceeds` (P8) and the later stories' tables of this service |
| Consumed facts with no source | The operation names of the three consumed rows, the call type of the package read and the table, owner and key of `tax_criteria_version`: Not specified in the source documents (GAP-3044; ASM-5108, ASM-5110) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the closed state list and the optionality rule of BR13. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/write-off-scans` | ScanRequest in with the criteria version of the cut-off, WriteOffScan of status 201 out with the pinned version, its hash and the run state, the population tested under it (API-S7-001) | Write-off and posting, right C, scope applied | `Idempotency-Key` header |

The operation answers 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 or MSG-S7-001 and 503 with MSG-P7-003, each with the error envelope and one message ID of section 14. The operation ID is that of TSD S7 T-A.1 and the path is that of the target base, not the monolith form. No operation that changes a criterion is declared, because TSD S7 T-A.1 publishes two and none of them does, and the change is authored and approved in rwb-decision (GAP-3044; ASM-5105). The population half of this operation is RWB-S7-E6013-CON's and the tax-criteria half is RWB-S7-E6014-CON's; this baseline adds the criteria-version element and the edition of the answer, and the three are reconciled at the wave 4 contract freeze (ASM-5112). `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002) is the approve, reject and defer stories' and is not declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The WO criteria package read at its version (name and call type Not specified in the source documents (GAP-3044; ASM-5108)) | The `rwb-decision` task queue as a Temporal activity, per the connection matrix row S7 to P7 = T | P7 rwb-decision | The WO package at its version with its 51 rules over 27 states, R-WO-01, R-WO-03, R-WO-04, the eligibility rule on both tracks and `tax_criteria_version`; faked |
| The population read (name Not specified in the source documents (GAP-3044; ASM-5110)) | rwb-case (P3), on the child-workflow boundary | P3 rwb-case | The cases in `SCAN_DUE` for the cut-off, with the case reference, product group, balance, account link and state; read only, faked |
| The case-move answer (name Not specified in the source documents (GAP-3044; ASM-5110)) | rwb-case (P3), on the child-workflow boundary | P3 rwb-case | The move `POPULATION_PROPOSED` or `SCAN_HELD` with the rule ID and the pinned version; the stage outcome the parent `CaseWorkflow` applies; faked |

The matrix gives this service a Temporal line to rwb-decision and no line to rwb-case, so the package is declared on the owner's queue and the case on the workflow boundary; where an owner publishes a REST contract instead, the row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The three rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded (GAP-3044; ASM-5108, ASM-5110).

#### 12.3 Events published

None. The service owns the topic `rwb.writeoff.events.v1` and its event set carries `WriteOffApproved` (event `EV-24`) with the retry and `.dlt` topics of the platform (TSD S7 T5.3; DP-14), and it does not belong to this step, because an accepted version approves no write-off and moves no balance. `WriteOffApproved` is declared as the committee story's, so this baseline declares no event, no producer group and no outbox row, and the absence test of AC7 fails a build that adds one. The outbox that would relay it is the platform library object of DP-09, which the pattern set for this key does not carry (ASM-5109).

#### 12.4 Events consumed

None. The step is started by the monthly scan of the cut-off and by the package publication it reads, and no event in the matrix carries a criteria version: the S7 listen lines run to rwb-source-data and rwb-payment, neither of which publishes one. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one (ASM-5109).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per write-off stage, the child of `CaseWorkflow`, continues-as-new at each stage end | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the criteria step; its input, signals and outcome for the parent are declared, not built |
| `acceptCriteriaVersion` | Activity, the acceptance and the pin | `rwb-writeoff` | The cut-off and the package version in; the accepted version, its hash, the rule set, the record reference and the pin out |
| `evaluateCriteria` | Activity, the R-WO-01 run of the cut-off under the pinned version | `rwb-writeoff` | The population, the pinned version and the package in; the rule ID with its version, the outcome and the moves out |
| The package read | Remote activity on the owner's queue, consumed per the matrix row S7 to P7 = T | `rwb-decision` | The version in force with its rule set and `tax_criteria_version`; its name and its payload are Not specified in the source documents (GAP-3044; ASM-5108) |

No child workflow for the case and none for the money exists in this service. The activity names are target design choices, and the step waits on the monthly scan and on the package publication. No activity is registered by this story.

#### 12.6 Schedules

None. The monthly write-off scan is job `JOB-16` in the legacy and becomes a Temporal Schedule of the scan story (`RWB-S7-E6013-APP`) that opens the cut-off this step accepts a version for; this baseline declares no Schedule, no Quartz row, no shared job table and no batch table, and records that DP-10 and its `RWB-PLT-E1071-CON` row are absent from the plan (ASM-5109).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of a balance on a case, its fields and its required flags, as the sibling baselines fix them; this document adds no property and no version column |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the acceptance and of each outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated trigger and the answer it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object present in the schema; this step declares no row in it (§12.3) |

`recovery_case` and `timer` (P3), `decision_log_entry` and `rule_row` (P7), every `v_ace_*` view (P1), `document` (P5), `proceeds` (P8) and the later stories' tables of this service are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01). No object of this schema holds a criterion or a version (BR6).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision criteria package fake | The package at version `2026-11` with R-WO-01, R-WO-03, R-WO-04, the eligibility rule on both tracks and `tax_criteria_version "2026-11"`; a version `2026-12` published mid-run; an incomplete version; an absent version | AC2, AC3, AC6 |
| rwb-case population fake | The population of the cut-off with 120 cases in `SCAN_DUE`, `RC-2026-000914` among them, with the product group, the balance, the account link and the state; a case that has left the population | AC3, AC6 |
| rwb-case case-move fake | The moves `POPULATION_PROPOSED` and `SCAN_HELD` accepted for `RC-2026-000914`; a move refused because the case is not in the expected state | AC3, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC4, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for `RC-2026-000914`, with the version in force and the run state | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the three consumed rows and the call type of the package read carry the placeholder until their owners confirm them (GAP-3044; ASM-5108, ASM-5110).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 0 consumed | `POST /write-off-scans` on `/api/recovery/writeoff/v1` with the criteria-version element; no REST row is consumed by this step |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 3 activities | `WriteOffWorkflow`, `acceptCriteriaVersion` and `evaluateCriteria` on `rwb-writeoff`, and the package read as a remote activity on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and changes no criterion, no write-off and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and five fakes.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is declared as the element of the decision record written before the pin and the outcome. DP-13 moves the base and nothing else. DP-19 sits behind SCR-27, whose screen model and field list are the edge contract's, and whose version state this baseline fixes in shape only. DP-04, DP-05, DP-06, DP-07, DP-09 and DP-10 are not in the pattern set: the package is declared as a consumed row rather than an embedded kit, the case as a consumed boundary and never a table, the parameters and reference data as package facts, the outbox as an absent library row rather than an event of this step, and `JOB-16` as the scan story's Schedule rather than this one's (GAP-3044; ASM-5109).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan carries; it leaves out the schedule row `RWB-PLT-E1071-CON` that `JOB-16` needs, the outbox and inbox library `RWB-PLT-TE006-CON` that the topic needs, the Drools kit rows `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON` that a rule package and its authoring add, and the parameters and reference-data rows `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`. The three consumed rows are C dependencies in fact and not in the metadata row.

**Deliverables and build steps**

1. Write the criteria-version element and the version property of the scan request, and validate the additive rule of AC1 in the pipeline.
2. Write the criteria-version element, the closed run state and the tax-criteria reading of AC2, with the placeholder where a field is unstated.
3. Record the package row, the population row and the case-move row of AC3 with their owner, their call type, their budget and their placeholders.
4. Record the decision-record element, the pin and the no-version-column rule of AC4 and validate them against the library schema.
5. Record the error envelope, the four messages and the rights of AC5, including the authoring-right boundary.
6. Publish the five fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

The deliverables are `openapi/rwb-writeoff-v1.yaml`, the two elements, the contract README rows for the three consumed rows and their placeholders, and the five fakes of 12.8.

**Done when.** The OpenAPI document validates in the pipeline, the ten contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, SCR-27 and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | The document describes the held state of R-WO-03 when no criteria version is in force or the published one is incomplete, which the app story raises while the rule runs | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the operation declares, or lacks the authoring right the change needs | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the pin and the outcome | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S7-001 is the only condition that is this feature's own, and it is carried on the held answer of the operation and on the version state of SCR-27.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its scan and held states through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the version in force, the cut-off and the run state, and rwb-case for the case and its route state; this baseline fixes the rwb-writeoff answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

No screen of its own is named for the criteria change by any source, and the authoring screen of the rule set belongs to rwb-decision (GAP-3044; ASM-5106). The legacy screen table gives the states "Scan; proposed; in committee; approved": the version state sits inside the scan state, the proposed, in-committee and approved states belong to the population and committee stories, and the held state is the reading of MSG-S7-001. The refusal and not-recorded states read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-026-01 | AC1, AC2 | Contract | The document half answers the scan operation, the criteria-version element and the acceptance record |
| TC-E6-026-02 | AC2, AC3 | Contract | The version `2026-11` and the case `RC-2026-000914` in `SCAN_DUE`; the contract half answers the version element, the population row and the `POPULATION_PROPOSED` shape |
| TC-E6-026-03 | AC3, AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the pin shape |
| TC-E6-026-04 | AC5 | Contract | A role without the Write-off and posting right and a malformed request; the 403 with MSG-P4-002 and the 422 envelope |
| TC-E6-026-05 | AC4, AC5 | Contract | An absent and an incomplete criteria version; the contract half answers the held state with MSG-S7-001 and the no-version-column rule |
| TC-S7-E6026-CON-01 | AC1 | Contract | The document validates; the operation, the base, the `Idempotency-Key`, the version property and the seven error answers are present |
| TC-S7-E6026-CON-02 | AC2 | Contract | The criteria-version element validates with its five properties, the closed run state and the tax-criteria reading |
| TC-S7-E6026-CON-03 | AC3 | Contract | The three consumed rows, their call types and their placeholders; the no-`v_ace_*` and no-`recovery_case` boundary |
| TC-S7-E6026-CON-04 | AC4, AC5, AC6 | Contract | The record and pin elements against the library schema; the four messages; the rights of TSD S7 T6.1; a drifted fake fails the build |
| TC-S7-E6026-CON-05 | AC7 | Contract | The naming baseline, the table owned, the no-version-column rule and the absence of a published event, a consumed event, a second topic and a Schedule |

The five legacy cases are those of RWB-E6-026 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6026-APP. The legacy level maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S7-E6026-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the criteria set, `tax_criteria_version`, the eligibility and hold conditions, the run state and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, amounts, dates, a version and a hash only, and every example is synthetic.
- The case stays with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property, no case row write and no ACE table read (BR3).
- The criteria stay with rwb-decision: the document declares no criterion value, no threshold, no authoring operation and no approval of a criterion (BR4).
- The money and the posting reference stay with rwb-payment and the posting story: the document declares no posting, no proceeds and no settlement property.
- No version column and no version table is declared: the pin is a run-scoped element and the record carries the version (BR5, BR6).
- One base, one topic, one queue, one schema and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the outbox library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks; the contract fixes the operation, the version element and the consumed rows on which the test is built (FSD S7 Requirements served); the split plan carries no requirement id for this slice (GAP-3044) | The criteria-version element of the scan and the three consumed rows | TC-E6-026-01, TC-E6-026-02, TC-S7-E6026-CON-01, TC-S7-E6026-CON-02, TC-S7-E6026-CON-03 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6026-CON-05 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The topic and the outbox library, declared as the committee story's | TC-S7-E6026-CON-05 |
| ADR-017 | Embedded Drools per service; rule registry in rwb-decision | The package read as a consumed row and the no-authoring rule | TC-S7-E6026-CON-03, TC-S7-E6026-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed rows with their budget and breaker | TC-S7-E6026-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S7-E6026-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-026, disposition Split (rework); feature FEAT-WOF-14 |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S7-E6026-APP; this baseline copies none of them |
| Source text | Legacy RWB-E6-026; FSD S7 Write-off and recovery v3 A1, A2.14; TSD S7 Write-off and recovery v2 T2, T3.1, T3.2, T4, T5.3, T6.1 and T-A; Business Rules and Routing Logic v4 rows R-WO-01, R-WO-03 and R-WO-04; Epics 3 to 8 Specification v3 feature row FEAT-WOF-14; context pack S7 connection matrix |
| Test cases | The five legacy cases as the contract half, and the five new contract cases TC-S7-E6026-CON-01 to -05 |
| Feature and screens | FEAT-WOF-14, SCR-27 Write-off proposal in its version state |
| Rules | R-WO-01, R-WO-03 and R-WO-04, governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-017, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the criteria-version element, the acceptance, the pin, the record and the case-move answer: RWB-S7-E6026-APP.
- The authoring, validation, test scenarios, approval and rollback of the WO package, the home and the key of `tax_criteria_version`, and the authoring screen: rwb-decision (P7) and the rule authoring story RWB-P7-E1073 (ASM-5104, ASM-5105).
- The case of record, its route states, the population and the parent `CaseWorkflow`: rwb-case (P3), whose rows this baseline declares as consumed and faked (ASM-5110).
- The monthly scan Schedule from `JOB-16` and the eligibility test on both tracks: the scan story of RWB-E6-013 (ASM-5109).
- The tax-criteria test of the population and the post charge-off remittance path: RWB-S7-E6014-APP and RWB-S7-E6014-CON.
- The committee decision of API-S7-002, the pack, the routing, the approve, the reject and the defer: FEAT-WOF-03 and FEAT-WOF-05 to 08.
- The posting, the provision release, the Finance feed, the reconciliation, the exception loop, the retention closure and the post charge-off sale: FEAT-WOF-09 to 13 and FEAT-WOF-16.
- The money, the remittance source and the posting reference: rwb-payment (P8) and the debt sale route (S6), neither of which publishes a row this baseline declares.
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

# RWB-S8-E7010-CON Handle a contact sent while a block is on - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7010-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the contact-breach path of rwb-deviation, split from RWB-E7-010. It fixes the breach-entry element, the consumed interaction-ledger row of rwb-source-data, the rights and the error set of the act, the fakes, and the three absences the path has — no operation, no event and no column of its own — on the base `/api/recovery/deviation/v1` (DP-13) behind the gateway-bff composite route (DP-19). The `deviation` element and its ten fields are declared unchanged, because no field of TSD S8 T3.1 carries a breach, its handler or its clock, and the two operations of the service are RWB-S8-E7001-APP's. The ledger read has no published operation name, the plan's C row is empty although the path consumes rwb-source-data and rwb-case, and the service level of the clock is set with DL22 while the rule row carries 10 working days (GAP-3071; ASM-5226 to ASM-5229). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S8-E7010-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the contact-breach path of rwb-deviation — the breach-entry element, the unchanged `deviation` element, the consumed interaction-ledger row, the rights and the error set of the act, the fakes and the three absences**, so that **the app story and the SCR-08 breach slice build against one fixed, testable contract on Day 1, and a field, a ledger shape or a right can never drift between rwb-deviation, rwb-source-data and rwb-case without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, one consumed row and the absences the path has. It declares no operation, no event and no Schedule of its own.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy breach path of RWB-E7-010 ran inside one process and one schema: it read the outbound contact, the contact stop, the case and the decision log without a boundary. The target splits them: rwb-source-data owns the interaction ledger, rwb-case owns the case, its contact hold and its timers, rwb-comms owns the block that failed, rwb-decision owns the packages and the central ledger, and rwb-deviation owns the deviation and the breach record. Each boundary is a contract another team builds against, so the shapes have to be fixed before the app story starts: the ledger entry the breach tests, the stop it reads, the entry it writes and the rights of the act.

The baseline also fixes the naming the checks require: schema `rwb_deviation`, login `rwb_deviation`, base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with its retry and `.dlt` topics, task queue `rwb-deviation` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.deviation` (Template and Rules v1 §R4; context pack service row). It records that rwb-deviation holds no grant on `rwb_source_data`, `rwb_case` or `rwb_decision`, so the ledger and the case are consumed on their owners' contracts only.

Four points are carried as gaps and assumptions rather than decided quietly: the baseline declares no operation for the breach, because the only two the Ownership Map gives S8 belong to RWB-S8-E7001-APP and the breach read is unpublished (GAP-3071; ASM-5226); no column of `deviation` carries the breach, so the element is unchanged and the breach lives on its entry (ASM-5227); the ledger read carries a placeholder because no source publishes its operation name and DP-18 is not in the pattern set (ASM-5228); and the service level of the clock is set with DL22 while R-DEV-20's timer column carries 10 working days (ASM-5229).

The wave and the date are the plan's: this key is EP07, wave 4, release 31 May 2027, and rwb-deviation is created in wave 2, so the business wave is later than the service wave and is kept as the plan gives it, with the date copied unchanged and marked tentative (ASM-5229).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `deviation` is S8's, `interaction` is P1's, `recovery_case`, `queue`, `assignment` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, `document` is P5's and `notice` is P6's. This document never declares another service's table or operation as its own.
- The interaction-ledger read is published with a fake so the consumed row names a real owner document; it is not a row of this story's dependency list, which is None, and the absence is recorded (GAP-3071; ASM-5228).
- The DEV and UNIVERSAL packages and the rows R-DEV-20, R-UNI-30 and R-UNI-39 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- TSD S8 T6.1 is the only rights source for this service, and it gives RW-CONDUCT R on Case record while FSD S8 A2.19.3.3 names the conduct officer primary; the conflict is fixed here and not widened (GAP-3071; ASM-5228).
- The `deviation` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The two operations of this legacy key, API-S8-001 and API-S8-002, are outside this baseline and belong to RWB-S8-E7001-APP.
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-deviation for this step and record that it declares no operation for the breach, with the two operations of the service named as RWB-S8-E7001-APP's.
2. Declare the `deviation` element exactly as TSD S8 T3.1 gives it, and record that no field of it carries the breach, its handler or its clock.
3. Declare the consumed interaction-ledger row of rwb-source-data with the fields the breach tests, and record that its operation name is unpublished.
4. Fix the breach-entry element of DP-03 with its attributes, its write order and its failure behaviour.
5. Publish the rights of the act and of the read, and record the conduct-officer conflict between FSD S8 and TSD S8 T6.1.
6. Publish the error set, the status codes and the message IDs of the act and of the read.
7. Publish the fakes of 12.8 and the three absence tests: no operation, no event and no column.
8. Fix the naming baseline and the boundary, then tag the baseline and hand it to RWB-S8-E7010-APP, the SCR-08 breach slice and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside a list of values | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC2, AC4, AC7 |
| X2 | A field is renamed or removed within major version 1, or a list value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3 |
| X5 | The document declares an operation, an event, a Schedule, a queue table, a foreign table property or a new column of `deviation` | The absence and boundary tests fail the build | None | AC1, AC2, AC7 |
| X6 | The rights of the act and of the read are not the ones TSD S8 T6.1 declares, or the unattended identity is given a user right | The access test fails the build | MSG-P4-002 | AC5 |
| X7 | The service level, an escalation point or a conduct-check value is declared with a value no source gives, or as a schema default | The review fails the baseline; the element carries the placeholder | None | AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-source-data and rwb-case only |
| Negotiable | The element attribute names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S8-E7010-APP, the SCR-08 breach slice and the wave 4 harness on Day 1, and the rwb-source-data team on the same day |
| Estimable | One OpenAPI document, nine contract tables, six fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the contact-breach path of rwb-deviation

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of deviation is S8, of interaction is P1, of recovery_case and timer is P3 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no operation for the breach and records the two operations of the service as another story's (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-deviation is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the breach path of a contact sent while a contact stop is in force
    Then it records POST /cases/{caseId}/deviations (API-S8-001) and PATCH /deviations/{deviationId} (API-S8-002) as RWB-S8-E7001-APP's, both on Case record right U, and the Ownership Map as giving S8 no third operation
    Then the read of the breach state behind SCR-08 carries the placeholder, with an error set of 400, 401, 403 with MSG-P4-002, 404 and 503 and one message ID per condition (GAP-3071; ASM-5226)
    Then the absence test fails a build that declares a breach operation, a second base or a second topic

  Scenario: AC2 The deviation element is declared unchanged and carries no breach column (new, D-RCV-60)
    Given the deviation section of the baseline
    When it is compared with TSD S8 T3.0, T3.1 and T3.2 and with the API Specification's Deviation element
    Then the deviation element declares the ten properties of DF-CAS-036 to DF-CAS-045: id, case_id, deviation_code, raised_at, raised_by, paused_state, handler_user_id, contact_stop, cleared_at and outcome, with the types and lengths TSD S8 T3.1 gives them
    Then id, case_id, deviation_code, raised_at, raised_by, paused_state and contact_stop are required and handler_user_id, cleared_at and outcome are optional, and state is declared as the standard record column of TSD S8 T3.0 against the 9 DEVIATION states of TSD S8 T4
    Then deviation_code is declared against LOV-DEVIATION, raised_by against LOV-RAISED-BY and outcome against LOV-DEV-OUTCOME, with the values TSD S8 T3.2 gives and none added
    Then the document records that no property of the element carries a breach, a second handler or a breach clock, that this step adds no column and no migration, and that the breach is carried on its entry (GAP-3071; ASM-5227)

  Scenario: AC3 The consumed interaction-ledger row is declared with its fields and its placeholder (new, D-RCV-60)
    Given the consumed rows and the ledger boundary of the baseline
    When they are compared with rwb-source-data as the owner of the interaction ledger under the R3 default ruling
    Then the outbound-contact read is declared as consumed from P1 rwb-source-data with the fields DF-INT-001, DF-INT-002, DF-INT-004 to DF-INT-006, DF-INT-012 and DF-INT-028: id, case_id, occurred_at, channel, direction, conduct_check and delivery_status
    Then direction is declared against LOV-DIRECTION, channel against LOV-CHANNEL, conduct_check against LOV-CONDUCT with PASSED, BLOCKED and NOT_APPLICABLE, and delivery_status against LOV-SEND-STATUS
    Then the operation name is Not specified in the source documents, the read is one hop with a 2 s budget and a breaker, and the document records that DP-18 is not in this key's pattern set although the ledger is consumed (GAP-3071; ASM-5228)
    Then the document declares no interaction property, no contact value, no contact number and no contact address, and records that no rwb-comms event reaches S8 because the connection matrix gives it no row to P6

  Scenario: AC4 The breach-entry element is declared and written before anything else (new, D-RCV-60)
    Given the entry section of the baseline
    When it is compared with the local decision-record library and with R-UNI-39
    Then one breach entry is declared per breach with the case reference, the deviation reference, the interaction reference, the channel, the sent-at instant, the rule IDs R-DEV-20 and R-UNI-39 with their package versions, the handler, the clock start and the escalation point
    Then the entry is written through the library on the shared rwb.decision-record.v1 before the handler and the clock are answered, and a failed write leaves everything unchanged with MSG-P7-003
    Then the handler is the Conduct and QA officer, the escalation point is the team manager, and the clock length is declared as the deviation service level of R-DEV-20's timer column read with its version and never a default
    Then the document records that the clock is set with DL22 and that R-DEV-20's row carries 10 working days, so the value is reference data and Not specified in the source documents (GAP-3071; ASM-5229)

  Scenario: AC5 The rights, the roles and the unattended identity are fixed on the act and on the read (new, D-RCV-60)
    Given the access section of the baseline
    When it is compared with TSD S8 T6.1 and with FSD S8 A2.19.3.3 and A2.19.4.3
    Then the act declares Case record right U, held by RW-CASEOWN CRU, RW-RESTRUCT, RW-COMPLAIN, RW-SPECIAL, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-DEBTSALE and RW-GUARANT RU, and the read declares Case record right R
    Then the document records that TSD S8 T6.1 gives RW-CONDUCT R only while FSD S8 A2.19.3.3 names the Conduct and QA officer primary and RW-COMPLY as also using, that the write is therefore taken by a role holding U and the conduct officer reads, and that no right is widened here (GAP-3071; ASM-5228)
    Then the document records that the breach branch runs under the rwb-deviation service identity on the workflow boundary and holds no user right of its own
    Then the access test fails a build that gives the unattended identity a user right or the conduct officer a write right the matrix does not give

  Scenario: AC6 The entry element and the fakes answer the document (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the element it serves
    Then the ledger fake answers an outbound SMS contact of a synthetic case with conduct_check BLOCKED, the same contact with PASSED, an inbound contact and no answer inside 2 s
    Then the deviation fake answers the same deviation with contact_stop true at DEV_WITH_OWNER, at DEV_FLAGGED and at DEV_RESOLVED, and a deviation with contact_stop false
    Then the package fake answers the DEV and UNIVERSAL packages at their versions with R-DEV-20, R-UNI-30 and R-UNI-39 and a package with no version in force, the entry stub answers a healthy chain and a stopped chain, and the case fake answers an accepted and a refused NO_CLOCK_CHANGE
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_deviation, the login is rwb_deviation, the base is /api/recovery/deviation/v1, the topic is rwb.deviation.events.v1, the queue is rwb-deviation and the Java package is th.co.scb.ace.workbench.recovery.deviation
    Then the tables named as owned are deviation and the library objects decision_record, idempotency_key and outbox_event, and interaction, recovery_case, queue, assignment, timer, rule_row, decision_log_entry, document and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names DeviationRaised (EV-06) and DeviationCleared (EV-07) as RWB-S8-E7001-APP's (ASM-5226)
    Then the document declares no Schedule, no Quartz row and no shared job table, records that the breach clock is a durable timer of the workflow, and records that the Ownership Map gives S8 no job
    Then the document records that the plan's C row is empty although the path consumes rwb-source-data and rwb-case (GAP-3071; ASM-5226)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S8-E7010-APP and they copy no criterion of the legacy story, whose two criteria stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `deviation` element is this service's and is declared exactly as TSD S8 T3.1 gives it, with no breach column and no second handler | Context pack ownership row `deviation`; TSD S8 T3.1 and T3.2; DP-01 |
| BR2 | The breach is declared as an entry written before anything else, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S8 T2; R-UNI-39; legacy RWB-E7-010 AC1 and AC2 |
| BR3 | The interaction ledger stays with rwb-source-data: the contract declares the read as consumed and declares no `interaction` property and no contact value | R3 default ruling; DP-18; LDM v8 DF-INT-001 to DF-INT-029; ASM-5228 |
| BR4 | The case, its route state, its contact hold and its timers stay with rwb-case: the contract declares no `recovery_case` and no `timer` property and no case write | Context pack ownership rows; R-UNI-30; ASM-5226 |
| BR5 | The packages and the central ledger stay with rwb-decision: the contract names R-DEV-20, R-UNI-30 and R-UNI-39 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5229 |
| BR6 | No event belongs to this step: the contract declares no published event and no consumed event, and names `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) as the raise and resolution story's | Event and Messaging Design v5 EV-06 and EV-07; TSD S8 T5.3; ASM-5226 |
| BR7 | No Schedule belongs to this step: the breach clock is a durable timer of the workflow and the Ownership Map gives S8 no job | Context pack ownership rows (Jobs 0); FSD S8 A2.19.4.4; ASM-5229 |
| BR8 | The rights are TSD S8 T6.1's and nothing wider: Case record U for the act, R for the read, and the conduct officer keeps R | TSD S8 T6.1; FSD S8 A2.19.3.3 and A2.19.4.3; ASM-5228 |
| BR9 | The state vocabulary is closed: the nine DEVIATION states of TSD S8 T4 are declared and this step adds none | TSD S8 T4; ASM-5227 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, a channel code, an instant, a rule version and a state only | Template and Rules v1 §R7.2 (s17); LDM v8 |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules v1 §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes |
| BR13 | No service level, no escalation point and no conduct-check value is a schema default or a constant | FSD S8 BR-S8-019; ASM-5229 |

### 9. State transitions

The lifecycle of this document, not of a breach:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The entry, the unchanged element, the consumed row and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-08 breach slice, the wave 4 harness and the rwb-source-data owner accept the document and the fakes | Baselined |
| Baselined | Additive change | An attribute is added within major version 1 | Baselined |
| Baselined | Breaking change | An attribute is removed, renamed or retyped, or a list value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | An operation, an event, a Schedule, a new column or a foreign table property | In review |

The DEVIATION machine of TSD S8 T4 is the app story's and this baseline declares it without moving any deviation: the states are the vocabulary on which the `state` property is declared, and the breach adds no state value.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-deviation | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the correction of the consumed row and the reading of the conduct-officer conflict |
| Consuming teams (the app story, the SCR-08 breach slice, the wave 4 harness and the rwb-source-data owner) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field and no contact value is declared in an entry or a fake |
| Compliance and PDPA officer | Confirms the service level the clock names as reference data, which is set with DL22 |

The per-service login behind the security scheme of the document is named "the rwb-deviation login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Deviation element | The ten columns of DF-CAS-036 to DF-CAS-045 as TSD S8 T3.1 gives them, unchanged: `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state`, `handler_user_id`, `contact_stop`, `cleared_at`, `outcome` |
| Required flags | `id`, `case_id`, `deviation_code`, `raised_at`, `raised_by`, `paused_state` and `contact_stop` required; `handler_user_id`, `cleared_at` and `outcome` optional |
| Lists of values | `LOV-DEVIATION` with X1 to X7, `LOV-RAISED-BY` with SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT, `LOV-DEV-OUTCOME` with RETURNED, RE_ROUTED and CASE_ENDED, all as TSD S8 T3.2 gives them |
| Breach entry | The DP-03 entry attributes: case reference, deviation reference, interaction reference, channel, sent-at instant, rule IDs with their package versions, handler, clock start and escalation point; no column of `deviation` carries any of them (ASM-5227) |
| Consumed ledger shape | DF-INT-001, DF-INT-002, DF-INT-004 to DF-INT-006, DF-INT-012 and DF-INT-028 of the `interaction` element, with `LOV-CONDUCT` PASSED, BLOCKED and NOT_APPLICABLE, declared as consumed and faked |
| Clock and escalation | The deviation service level of R-DEV-20's timer column and its owner column, read from the package at its version; the length is set with DL22 and is Not specified in the source documents (GAP-3071; ASM-5229) |
| Consumed fields with no source | The operation name of the ledger read: Not specified in the source documents (GAP-3071; ASM-5228) |
| Not declared here | `interaction` (P1), `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), every `v_ace_*` view (P1), and the two operations API-S8-001 and API-S8-002 (RWB-S8-E7001-APP) |

The field-level formats of the entry are settled in the baseline review; this story fixes the element names, the unchanged `deviation` element, the consumed fields and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). The Ownership Map gives this service exactly two operations, `POST /cases/{caseId}/deviations` (API-S8-001, Case record U) and `PATCH /deviations/{deviationId}` (API-S8-002, Case record U), and both are writes of the deviation itself, which belong to RWB-S8-E7001-APP. The breach act arrives as a signal on the running workflow and the read of the breach state behind SCR-08 is Not specified in the source documents and carries the placeholder (GAP-3071; ASM-5226). A build that declares a breach operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of the outbound contacts of a case from the interaction ledger (operation name Not specified in the source documents (GAP-3071; ASM-5228)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The contact the breach tests: its reference, its case, its `occurred_at`, `channel`, `direction`, `conduct_check` and `delivery_status`; read only, faked |

The row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020, DP-11). It is a contract dependency of class C that the plan's C row does not carry, and the absence is recorded as GAP-3071 with ASM-5228. The case boundary is Temporal on the parent-and-child line (P3 starts the child on `rwb-deviation`), so it is declared in 12.5 and not as a REST row.

#### 12.3 Events published

None. The service owns `DeviationRaised` (EV-06) and `DeviationCleared` (EV-07) on `rwb.deviation.events.v1` — `caseId`, `deviationCode` and `raisedBy` for the first and `caseId`, `deviationCode` and `outcome` for the second — and both are the raise and the resolution of a deviation, published by RWB-S8-E7001-APP (Event and Messaging Design v5; TSD S8 T5.3). A breach raises no deviation and clears none, so this baseline declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5226).

#### 12.4 Events consumed

None. No source gives rwb-deviation a consumed event for this step: the breach arrives on the Temporal boundary from the case router, and the connection matrix gives S8 no row to rwb-comms (P6), which is why the contact is read on the ledger. This baseline declares no consumer group, no subscription and no inbox of its own (ASM-5226, ASM-5228).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per case, started at any time, the stage child of `CaseWorkflow` | `rwb-deviation` in namespace `rwb-recovery` | The stage that hosts the breach branch; its input, its signals and its outcome for the parent are declared, not built |
| The `contactBreach` branch of `DeviationWorkflow` | Workflow branch | `rwb-deviation` | The path from the contact-breach signal to the entry, the handler, the clock and the stage answer `NO_CLOCK_CHANGE` |
| `readBreachFacts` | Activity | `rwb-deviation` | The ledger entry and the deviation in; the paired breach facts out |
| `evaluateBreachRules` | Activity | `rwb-deviation` | The packages in force in; the rule IDs, their versions and the condition that fired out |
| `recordAndApplyBreach` | Activity | `rwb-deviation` | The entry, the handler, the clock start and the answer out, one transaction |
| `breachClock` | Durable timer | `rwb-deviation` | The service level of the rule row with its version; the expiry is the escalation |

No child workflow of this service exists in this step and no timer table is declared here: the `timer` rows are P3's. The branch and activity names are target design choices and no source document fixes them; no activity is registered by this story.

#### 12.6 Schedules

None. The Ownership Map gives S8 no job and FSD S8 A2.19.4.4 declares no background event for the feature, so this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The breach clock is a durable timer inside the branch (ASM-5229).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `deviation` | S8 (`rwb_deviation`) | The deviation of the case and its `contact_stop`; the element the baseline declares unchanged and the app story reads |
| `decision_record` | PLT library, created in `rwb_deviation` | The local hash-linked breach entry (DP-03) |
| `idempotency_key` | PLT library, created in `rwb_deviation` | The key of the repeated signal and the outcome it holds |
| `outbox_event` | PLT library, created in `rwb_deviation` | Created in this schema by the library for the stories that publish; no row of it belongs to this step |

`interaction` (P1), `recovery_case`, `queue`, `assignment` and `timer` (P3), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or records of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data interaction-ledger fake | An outbound SMS contact of case `RW-2026-000710` at `2026-12-11T09:30:00Z` with `conduct_check` BLOCKED and `delivery_status` sent; the same contact with PASSED; an inbound contact; no answer inside 2 s; the operation name carries the placeholder (GAP-3071; ASM-5228) | AC3, AC6 |
| rwb-deviation deviation fake | The deviation `DEV-2026-000710` of code X1 with `contact_stop` true at `DEV_WITH_OWNER`, at `DEV_FLAGGED` and at `DEV_RESOLVED`, and a deviation with `contact_stop` false | AC2, AC6 |
| rwb-decision package fake | The DEV package at its version in force with R-DEV-20 and the UNIVERSAL package with R-UNI-30 and R-UNI-39; a package with no version in force | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC4, AC6 |
| rwb-case workflow fake | The case with its open deviation, an accepted and a refused `NO_CLOCK_CHANGE` answer | AC6 |
| gateway-bff composite route fake | The merged SCR-08 answer for the case, with the breach slice of this service read once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The ledger operation name is derived from the published documents and carries the placeholder until its owner confirms it (GAP-3071; ASM-5228).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 1 consumed | The interaction-ledger read of rwb-source-data; one hop, 2 s |
| Kafka | 0 published, 0 consumed | EV-06 and EV-07 are the raise and resolution story's; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch, 3 activities and 1 durable timer declared, 0 registered | `DeviationWorkflow` and its `contactBreach` branch on `rwb-deviation`; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no deviation, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the act and the read, and six fakes.

**Deliverables.** The additive document `openapi/rwb-deviation-v1.yaml` with the unchanged `deviation` element and no breach operation, the contract README rows for the consumed ledger row and its placeholder, the breach-entry schema of the library, and the six WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before anything else is answered. DP-13 moves the base of the service and adds no operation, because this step owns none. DP-19 is behind SCR-08, whose screen model is the edge contract's. No other pattern is claimed: the ledger is a consumed contract (DP-18, recorded and not claimed) and the lists of values are read at a version (DP-07, recorded and not claimed), so neither appears in the metadata row and both are in the registers (GAP-3071; ASM-5228).

**Build steps**

1. Record the absence of a breach operation and the two operations as RWB-S8-E7001-APP's, with the absent-operation test of AC1.
2. Publish the `deviation` element unchanged with its ten properties, its required flags and its three lists, and record the no-breach-column rule of AC2.
3. Record the consumed ledger row of AC3 with its owner, its fields, its lists, its budget and the placeholder.
4. Publish the breach-entry element of AC4, with the rule IDs, the handler, the clock and the escalation, and validate it against the library schema.
5. Record the rights, the roles and the unattended identity of AC5, with the conduct-officer conflict.
6. Publish the six fakes of AC6 and the drift test.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every path and the drift test is green, and the app story, the SCR-08 breach slice and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | Carried from the legacy message set of this key. It confirms the raise of a deviation and the handler it went to, so no path of this step raises it | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required field of an element is absent or invalid, or a body fails schema validation, or a list value is outside its enumeration | Enter {field}. |
| MSG-P4-002 | The role lacks the Case record right of the act or of the read, and a role without the right of the consumed act tries it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The breach entry cannot be written before anything else | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four message IDs are those of the legacy message set of this key; the text is the legacy and FSD S8 wording, copied unchanged, and no message is reworded or added. MSG-S8-001 is carried because it is in the message set of this feature, and the raise itself belongs to RWB-S8-E7001-APP.

### 15. Screens and states

The contract serves the breach slice of SCR-08 Deviation queue through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviation and its breach entry, rwb-case for the case, its owner and its timers, and rwb-decision for the decision records; this baseline fixes the rwb-deviation answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON (ASM-5226). The breach read behind the list is a placeholder, because no source publishes it. The legacy screen table's two screens are accounted for: SCR-06 Raise deviation and its form-and-saved states belong to RWB-S8-E7001-APP, because a breach raises no deviation, and this story answers the breach, escalated, refused, not-recorded and unavailable states of SCR-08 on the same route with the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-010-01 | AC1, AC2 | Contract | The synthetic case `RW-2026-000710`; the contract half answers the unchanged element, the absent breach operation and the breach entry shape |
| TC-E7-010-02 | AC4 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the entry element |
| TC-E7-010-03 | AC5 | Contract | A role without the Case record right and the conduct officer's R right; the contract half answers the 403 with MSG-P4-002 and the rights of the act and the read |
| TC-E7-010-04 | AC4, AC6 | Contract | A forced record failure and a drifted fake; the contract half answers the entry path and the drift test |
| TC-S8-E7010-CON-01 | AC1 | Contract | The document validates; no breach operation, no second base and no second topic are declared, and the two operations are named as RWB-S8-E7001-APP's |
| TC-S8-E7010-CON-02 | AC2 | Contract | The `deviation` element validates with its ten properties, its seven required flags and its three lists; no breach column and no added state value |
| TC-S8-E7010-CON-03 | AC3 | Contract | The ledger row with its seven fields, its four lists and its placeholder; no interaction property and no contact value |
| TC-S8-E7010-CON-04 | AC4 | Contract | The entry element with R-DEV-20 and R-UNI-39, the handler, the clock and the escalation; the service level carries its placeholder |
| TC-S8-E7010-CON-05 | AC5 | Contract | Case record U for the act and R for the read; RW-CONDUCT keeps R, and the unattended identity holds no user right |
| TC-S8-E7010-CON-06 | AC6 | Contract | The six fakes match the document and a drifted fake fails the build |
| TC-S8-E7010-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |

The four legacy cases are the legacy cases of RWB-E7-010 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S8-E7010-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S8-E7010-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the service level, the escalation point, the conduct-check values, the lists and the rule rows stay reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, a channel code, an instant, a rule version and a state only; no contact value, number or address appears anywhere in the document.
- The interaction ledger stays with rwb-source-data, the case and its timers with rwb-case and the packages and the ledger with rwb-decision: the document declares no `interaction`, `recovery_case`, `timer`, `rule_row` or ledger property (BR3, BR4, BR5).
- This step owns no operation and no event: the document declares none for it and records the two operations of the service as RWB-S8-E7001-APP's (BR6, AC1).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- The `deviation` element is declared unchanged: a build that adds a breach column, a second handler or a breach clock to it fails the absence test (BR1, ASM-5227).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table (BR7).
- The rights are TSD S8 T6.1's and are never widened in a contract; the conduct-officer conflict is recorded, not resolved by invention (BR8, ASM-5228).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DVH-011 | The full deviation flows with their approvers, contact stops and return points run end to end (Must, E7) | The breach-entry element, the consumed ledger row and the no-operation baseline | TC-E7-010-01, TC-S8-E7010-CON-01, TC-S8-E7010-CON-03, TC-S8-E7010-CON-04 |
| REQ-DVH-004 | Contact stops apply automatically for a dispute or complaint, a vulnerable or hardship case, and a deceased customer (Must, E2) | The `contact_stop` property the element declares and the conduct-check condition of the ledger | TC-S8-E7010-CON-02, TC-S8-E7010-CON-03 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-S8-E7010-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The consumed ledger row with its budget and breaker | TC-S8-E7010-CON-03 |
| ADR-022 | Local decision record plus central ledger | The breach-entry element and the central ledger of P7 | TC-S8-E7010-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-010, disposition Split (rework); feature FEAT-DVF-10 |
| Legacy criteria | AC1 and AC2 of the legacy story, owned word for word by RWB-S8-E7010-APP; this baseline copies none of them |
| Test cases | The four legacy cases as the contract half, and the seven new contract cases TC-S8-E7010-CON-01 to -07 |
| Feature and screens | FEAT-DVF-10, SCR-08 Deviation queue and SCR-06 Raise deviation |
| Rules | R-DEV-20 and R-UNI-39 named from the Business Rules and Routing Logic v4 and governed in rwb-decision, with R-UNI-30 and R-DEV-01 read |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the element, the pairing of contact and stop, the entry, the handler, the clock and the answer: RWB-S8-E7010-APP.
- The raise and the resolution of a deviation, its outcome and the two operations of the service: RWB-S8-E7001-APP and the X1 to X7 stories.
- The matching of a complaint to the preceding contact: RWB-S8-E7009-APP.
- The block of an outbound contact when a stop is in force and the conduct check before every send: FEAT-OCC-06 and FEAT-OCC-05, rwb-comms (P6), built in Epic 2.
- The lift of a contact stop and the return of the case to its paused state: R-UNI-44 and the deviation resolution stories, with rwb-case.
- The interaction ledger, its contact values and the masked contact point: rwb-source-data (P1), whose operation name this baseline does not publish (GAP-3071).
- The case of record, its route state, its contact hold and the `timer` rows: rwb-case (P3).
- The DEV and UNIVERSAL packages, their rule rows, the central ledger and the service level set with DL22: rwb-decision (P7) and the registers (ASM-5229).
- The gateway-bff composite route and the screen field list of SCR-08: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
